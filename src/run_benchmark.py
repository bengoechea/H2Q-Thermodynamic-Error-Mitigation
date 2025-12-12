#!/usr/bin/env python3
"""
Run Official Quantum Advantage Tracker Benchmark with H²Q Mitigation

This script:
1. Loads the official OLE circuit from the Quantum Advantage Tracker
2. Transpiles for target IBM backend
3. Runs with and without H²Q mitigation
4. Saves results in tracker-compatible format

Usage:
    python src/run_benchmark.py --circuit 70Q --backend ibm_fez --shots 8192
"""

import argparse
import json
import os
from datetime import datetime
from pathlib import Path

import numpy as np
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2, Batch

from circuit_loader import load_benchmark_circuit
from h2q_mitigation import H2QMitigator

# Observable qubits for OLE benchmark: O = Z_52 Z_59 Z_72
OBSERVABLE_QUBITS = [52, 59, 72]
FALSIFICATION_CIRCUITS = {"REP3", "REP5"}

def _canonical_bitstring(key, width: int | None) -> str:
    """
    Normalize count keys so simulator and hardware distributions are comparable.

    - Qiskit counts often use spaces between classical registers (e.g. "00 000").
    - Some backends may omit spaces or drop leading zeros.
    - SamplerV2 may also return non-str keys in some versions.
    """
    if isinstance(key, str):
        s = key.replace(" ", "")
        # Handle hex-style keys if they appear
        if s.startswith("0x"):
            try:
                n = int(s, 16)
                if width is None:
                    # best effort: keep minimal width
                    return format(n, "b")
                return format(n, f"0{width}b")
            except Exception:
                pass
        if width is not None:
            return s.zfill(width)
        return s
    if isinstance(key, int):
        if width is None:
            return format(key, "b")
        return format(key, f"0{width}b")
    # Fallback: stringify then strip spaces
    s = str(key).replace(" ", "")
    if width is not None:
        return s.zfill(width)
    return s


def _normalize_counts(counts: dict, *, width: int | None = None) -> dict[str, float]:
    total = sum(counts.values())
    if total <= 0:
        return {}
    out: dict[str, float] = {}
    for k, v in counts.items():
        kk = _canonical_bitstring(k, width)
        out[kk] = out.get(kk, 0.0) + (v / total)
    return out


def _total_variation_distance(p: dict[str, float], q: dict[str, float]) -> float:
    """TVD(p,q) = 0.5 * sum_x |p(x) - q(x)|"""
    keys = set(p.keys()) | set(q.keys())
    return 0.5 * sum(abs(p.get(k, 0.0) - q.get(k, 0.0)) for k in keys)


def _simulate_ideal_distribution(circuit, shots: int = 20000) -> dict[str, float]:
    """
    Simulator reference distribution for small falsification circuits.
    Uses the same circuit/clbit ordering so distributions are comparable.
    """
    from qiskit_aer import AerSimulator

    if not circuit.clbits:
        circuit.measure_all()
    sim = AerSimulator()
    job = sim.run(circuit, shots=shots)
    res = job.result()
    counts = res.get_counts(0)
    width = getattr(circuit, "num_clbits", None)
    return _normalize_counts(counts, width=width)

def _extract_counts_from_sampler_pub_result(pub_result, shots: int | None = None) -> dict:
    """
    Extract a counts dict from a SamplerV2 PubResult.
    Handles multiple result shapes across Qiskit Runtime versions.
    """
    counts: dict = {}
    data_bin = getattr(pub_result, "data", None)
    if data_bin is None:
        return counts

    # SamplerV2 uses BitArray in meas attribute
    if hasattr(data_bin, "meas"):
        meas = data_bin.meas
        if hasattr(meas, "get_counts"):
            return meas.get_counts()
        try:
            return dict(meas)
        except Exception:
            return {}

    # Common shape in newer primitives: DataBin(c=BitArray(...)) or similar values()
    if hasattr(data_bin, "values"):
        try:
            for v in list(data_bin.values()):
                if hasattr(v, "get_counts"):
                    return v.get_counts()
        except Exception:
            pass

    # Alternative: quasi_probs (approximate counts if shots provided)
    if hasattr(data_bin, "quasi_probs") and shots is not None:
        try:
            quasi_probs = data_bin.quasi_probs
            total_prob = sum(quasi_probs.values()) if quasi_probs else 0
            if total_prob > 0:
                approx: dict[str, int] = {}
                for bitstring, prob in quasi_probs.items():
                    if prob > 0:
                        count = int((prob / total_prob) * shots)
                        if count > 0:
                            approx[bitstring] = count
                return approx
        except Exception:
            pass

    # Last resort: try get_counts on data_bin
    if hasattr(data_bin, "get_counts"):
        try:
            return data_bin.get_counts()
        except Exception:
            return {}

    return counts


def fetch_counts_for_jobs(job_ids: list[str], shots_hint: int | None = None) -> tuple[list[dict], dict]:
    """
    Fetch results for existing Runtime job IDs and return (counts_list, metadata).
    """
    service = QiskitRuntimeService()
    all_counts: list[dict] = []
    meta: dict = {"jobs": []}

    for jid in job_ids:
        job = service.job(jid)
        status = str(job.status())
        backend_name = getattr(job.backend(), "name", None)
        meta["jobs"].append(
            {
                "job_id": jid,
                "status": status,
                "backend": backend_name,
                "creation_date": getattr(job, "creation_date", None).isoformat()
                if getattr(job, "creation_date", None)
                else None,
            }
        )

        if status not in {"DONE", "COMPLETED"}:
            raise RuntimeError(f"Job {jid} is not complete (status={status}).")

        result = job.result()
        # Sampler jobs return a list-like of pub results
        pub_result = result[0]
        counts = _extract_counts_from_sampler_pub_result(pub_result, shots=shots_hint)
        if not counts:
            raise RuntimeError(f"Job {jid}: failed to extract counts from result.")
        all_counts.append(counts)

    # best-effort: pick backend from first job
    if meta["jobs"]:
        meta["backend"] = meta["jobs"][0].get("backend")
    return all_counts, meta


def compute_observable(counts: dict, observable_qubits: list) -> tuple:
    """
    Compute expectation value of ZZZ observable on specified qubits.
    
    Args:
        counts: Measurement counts dictionary
        observable_qubits: List of qubit indices for Z operators
        
    Returns:
        (expectation_value, standard_error)
    """
    total = sum(counts.values())
    if total == 0:
        return 0.0, 1.0
    
    expectation = 0.0
    for bitstring, count in counts.items():
        # Compute parity of observable qubits
        parity = 1
        for q in observable_qubits:
            if q < len(bitstring):
                # Qiskit uses little-endian bit ordering
                bit = int(bitstring[-(q+1)])
                parity *= (-1) ** bit
        expectation += parity * count
    
    expectation /= total
    
    # Standard error
    variance = 1 - expectation**2
    std_error = np.sqrt(variance / total)
    
    return expectation, std_error

def transpile_for_backend(circuit, backend):
    """Transpile circuit for target backend."""
    print(f"Transpiling for {backend.name}...")
    
    # Ensure circuit has measurements
    if not circuit.clbits:
        print("  Adding measurements to circuit...")
        circuit.measure_all()
    
    pm = generate_preset_pass_manager(
        optimization_level=3,
        backend=backend
    )
    
    transpiled = pm.run(circuit)
    
    print(f"  Transpiled depth: {transpiled.depth()}")
    cz_count = transpiled.count_ops().get('cz', 0)
    ecr_count = transpiled.count_ops().get('ecr', 0)
    print(f"  Two-qubit gates: {cz_count + ecr_count}")
    
    return transpiled

def run_hardware(circuit, backend, shots: int, n_runs: int = 5) -> list:
    """
    Run circuit on hardware multiple times.
    
    Returns list of count dictionaries.
    """
    print(f"\nRunning on {backend.name} ({n_runs} runs × {shots} shots)...")
    
    all_counts = []
    
    with Batch(backend=backend) as batch:
        sampler = SamplerV2(mode=batch)
        
        for i in range(n_runs):
            print(f"  Run {i+1}/{n_runs}...", end=" ", flush=True)
            
            job = sampler.run([circuit], shots=shots)
            result = job.result()
            
            # Extract counts from SamplerV2 result
            # SamplerV2 returns PubResult with data in DataBin format
            pub_result = result[0]
            counts = _extract_counts_from_sampler_pub_result(pub_result, shots=shots)
            
            # Ensure we have counts
            if not counts:
                print(f"\n    WARNING: No counts extracted. Creating empty counts dict.")
                counts = {}
            else:
                print(f"    Extracted {len(counts)} unique bitstrings, {sum(counts.values())} total shots")
            
            all_counts.append(counts)
            
            print(f"Done. Job ID: {job.job_id()}")
    
    return all_counts


def submit_only(circuit, backend, shots: int, n_runs: int) -> list[str]:
    """
    Submit hardware jobs and return job IDs (do not wait for results).
    Use this when you have limited remaining quantum time or long queue waits.
    """
    print(f"\nSubmitting on {backend.name} ({n_runs} runs × {shots} shots) (submit-only)...")
    job_ids: list[str] = []
    with Batch(backend=backend) as batch:
        sampler = SamplerV2(mode=batch)
        for i in range(n_runs):
            job = sampler.run([circuit], shots=shots)
            jid = job.job_id()
            job_ids.append(jid)
            print(f"  Submitted {i+1}/{n_runs}: {jid}  https://quantum.ibm.com/jobs/{jid}")
    return job_ids

def run_simulation(circuit, shots: int, n_runs: int = 5) -> list:
    """
    Run circuit on simulator for baseline comparison.
    
    Returns list of count dictionaries.
    """
    from qiskit_aer import AerSimulator
    
    print(f"\nRunning simulation ({n_runs} runs × {shots} shots)...")
    
    # Ensure circuit has measurements
    if not circuit.clbits:
        print("  Adding measurements to circuit...")
        circuit.measure_all()
    
    # Use MPS for large circuits
    method = 'matrix_product_state' if circuit.num_qubits > 30 else 'automatic'
    simulator = AerSimulator(method=method)
    
    all_counts = []
    for i in range(n_runs):
        print(f"  Run {i+1}/{n_runs}...", end=" ", flush=True)
        
        job = simulator.run(circuit, shots=shots)
        result = job.result()
        counts = result.get_counts(0)  # Get counts for experiment 0
        all_counts.append(counts)
        
        print("Done.")
    
    return all_counts

def analyze_results(all_counts: list, mitigator: H2QMitigator) -> dict:
    """
    Analyze results with and without H²Q mitigation.
    
    Returns dictionary with full analysis.
    """
    from scipy import stats
    
    raw_observables = []
    mitigated_observables = []
    kept_fractions = []
    entropy_reductions = []
    
    for counts in all_counts:
        # Raw observable
        obs_raw, err_raw = compute_observable(counts, OBSERVABLE_QUBITS)
        raw_observables.append(obs_raw)
        
        # Apply H²Q mitigation (using working implementation)
        total = sum(counts.values())
        max_count = max(counts.values()) if counts else 0
        
        # H²Q filtering: keep states above theta_off threshold
        filtered_counts = {}
        for bitstring, count in counts.items():
            relative_prob = count / max_count if max_count > 0 else 0
            if relative_prob > mitigator.theta_off:
                filtered_counts[bitstring] = count
        
        # Renormalize
        filtered_total = sum(filtered_counts.values())
        if filtered_total > 0:
            mitigated_probs = {k: v / filtered_total for k, v in filtered_counts.items()}
            mitigated_counts = {k: int(v * total) for k, v in mitigated_probs.items() if v > 0}
        else:
            # Fallback: keep top states
            sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
            n_keep = max(1, len(sorted_counts) // 10)
            mitigated_counts = dict(sorted_counts[:n_keep])
        
        # Mitigated observable
        obs_mit, err_mit = compute_observable(mitigated_counts, OBSERVABLE_QUBITS)
        mitigated_observables.append(obs_mit)
        
        # Compute kept fraction
        kept_fraction = sum(mitigated_counts.values()) / total if total > 0 else 0.0
        kept_fractions.append(kept_fraction)
        
        # Entropy reduction (simplified - would need full entropy calculation)
        entropy_reductions.append(0.0)  # Placeholder
    
    # Compute statistics
    def compute_ci(values, confidence=0.95):
        if len(values) == 0:
            return 0.0, 0.0, 0.0
        mean = np.mean(values)
        if len(values) == 1:
            return mean, mean, mean
        sem = stats.sem(values)
        ci = stats.t.interval(confidence, len(values)-1, loc=mean, scale=sem)
        return mean, ci[0], ci[1]
    
    raw_mean, raw_lo, raw_hi = compute_ci(raw_observables)
    mit_mean, mit_lo, mit_hi = compute_ci(mitigated_observables)
    
    return {
        "raw": {
            "mean": raw_mean,
            "ci_lower": raw_lo,
            "ci_upper": raw_hi,
            "all_values": raw_observables,
        },
        "mitigated": {
            "mean": mit_mean,
            "ci_lower": mit_lo,
            "ci_upper": mit_hi,
            "all_values": mitigated_observables,
        },
        "kept_fraction": {
            "mean": np.mean(kept_fractions),
            "std": np.std(kept_fractions),
        },
        "entropy_reduction": {
            "mean": np.mean(entropy_reductions),
            "std": np.std(entropy_reductions),
        },
        "n_runs": len(all_counts),
    }


def analyze_falsification(all_counts: list[dict], ideal_probs: dict[str, float], mitigator: H2QMitigator) -> dict:
    """
    Falsification: does mitigation move the observed distribution closer to simulator 'ideal'?
    Metric: total variation distance (TVD) to the ideal distribution.
    Success criterion: mean(TVD_mitigated) < mean(TVD_raw) with non-trivial kept_fraction.
    """
    from scipy import stats

    tvd_raw_list: list[float] = []
    tvd_mit_list: list[float] = []
    kept_fractions: list[float] = []
    debug: dict = {
        "fnmn_notebook": True,
        "ideal_support_size_full": len(ideal_probs),
        "ideal_top10_full": sorted(ideal_probs.items(), key=lambda kv: kv[1], reverse=True)[:10],
        "per_run": [],
    }

    for counts in all_counts:
        # infer a stable width so we can zfill and align support
        width = None
        try:
            width = max(len(_canonical_bitstring(k, None)) for k in counts.keys()) if counts else None
        except Exception:
            width = None

        p_raw = _normalize_counts(counts, width=width)

        # Project simulator ideal distribution onto the same observed bit-width as hardware.
        # Empirically, SamplerV2 on these QASM circuits returns only the syndrome register.
        # We model that as the *last* `width` bits of the simulator key string.
        ideal_eff: dict[str, float] = {}
        if width is not None and width > 0:
            for k_full, p in ideal_probs.items():
                k_eff = _canonical_bitstring(k_full, None)[-width:]
                ideal_eff[k_eff] = ideal_eff.get(k_eff, 0.0) + p
        else:
            ideal_eff = dict(ideal_probs)

        # Renormalize (defensive: projection should preserve sum=1)
        s_eff = sum(ideal_eff.values())
        if s_eff > 0 and abs(s_eff - 1.0) > 1e-6:
            ideal_eff = {k: v / s_eff for k, v in ideal_eff.items()}

        tvd_raw = _total_variation_distance(p_raw, ideal_eff)
        tvd_raw_list.append(tvd_raw)

        total = sum(counts.values())
        max_count = max(counts.values()) if counts else 0

        # Same threshold rule as the OLE mitigation path (locked parameterization)
        filtered_counts: dict = {}
        for bitstring, count in counts.items():
            relative_prob = count / max_count if max_count > 0 else 0
            if relative_prob > mitigator.theta_off:
                filtered_counts[bitstring] = count

        filtered_total = sum(filtered_counts.values())
        if filtered_total > 0:
            p_mit = _normalize_counts(filtered_counts, width=width)
            tvd_mit = _total_variation_distance(p_mit, ideal_eff)
            tvd_mit_list.append(tvd_mit)
            kept_fractions.append(filtered_total / total if total > 0 else 0.0)
        else:
            # If everything is rejected, define as failure (no improvement) and kept=0.
            tvd_mit = tvd_raw
            tvd_mit_list.append(tvd_mit)
            kept_fractions.append(0.0)

        # FNMN Notebook per-run trace
        raw_keys = list(counts.keys())
        debug["per_run"].append(
            {
                "inferred_width": width,
                "ideal_support_size_effective": len(ideal_eff),
                "ideal_top10_effective": sorted(ideal_eff.items(), key=lambda kv: kv[1], reverse=True)[:10],
                "raw_key_samples": [repr(k) for k in raw_keys[:10]],
                "raw_key_samples_canonical": [_canonical_bitstring(k, width) for k in raw_keys[:10]],
                "raw_top10": sorted(p_raw.items(), key=lambda kv: kv[1], reverse=True)[:10],
                "tvd_raw": tvd_raw,
                "tvd_mitigated": tvd_mit,
                "kept_fraction": kept_fractions[-1],
            }
        )

    def compute_ci(values, confidence=0.95):
        if len(values) == 0:
            return 0.0, 0.0, 0.0
        mean = float(np.mean(values))
        if len(values) == 1:
            return mean, mean, mean
        sem = stats.sem(values)
        if float(sem) == 0.0:
            return mean, mean, mean
        ci = stats.t.interval(confidence, len(values) - 1, loc=mean, scale=sem)
        return mean, float(ci[0]), float(ci[1])

    raw_mean, raw_lo, raw_hi = compute_ci(tvd_raw_list)
    mit_mean, mit_lo, mit_hi = compute_ci(tvd_mit_list)

    return {
        "notebook": debug,
        "metric": "tvd_to_simulator_ideal",
        "raw": {
            "mean": raw_mean,
            "ci_lower": raw_lo,
            "ci_upper": raw_hi,
            "all_values": tvd_raw_list,
        },
        "mitigated": {
            "mean": mit_mean,
            "ci_lower": mit_lo,
            "ci_upper": mit_hi,
            "all_values": tvd_mit_list,
        },
        "kept_fraction": {
            "mean": float(np.mean(kept_fractions)) if kept_fractions else 0.0,
            "std": float(np.std(kept_fractions)) if kept_fractions else 0.0,
        },
        "improvement": {
            "delta_mean": raw_mean - mit_mean,  # positive is good (lower TVD after mitigation)
        },
        "n_runs": len(all_counts),
    }

def save_results(results: dict, config: dict, output_dir: str = "results"):
    """Save results in tracker-compatible format."""
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    mode = config.get("mode", "ole")
    
    # Full results
    full_output = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "circuit": config["circuit"],
            "backend": config["backend"],
            "shots": config["shots"],
            "n_runs": config["n_runs"],
            "observable": "Z_52 Z_59 Z_72" if mode == "ole" else None,
            "metric": "tvd_to_simulator_ideal" if mode == "falsification" else None,
            "method": "H2Q Thermodynamic Error Mitigation",
            "patent": "US Provisional 63/927,371",
            **({"job_ids": config["job_ids"]} if config.get("job_ids") else {}),
        },
        "results": results,
        "h2q_config": {
            "theta_on": config["theta_on"],
            "theta_off": config["theta_off"],
            "tau": config["tau"],
        }
    }
    
    prefix = "ole_results" if mode == "ole" else "fnmn_notebook"
    filename = f"{prefix}_{config['circuit']}_{config['backend']}_{timestamp}.json"
    filepath = Path(output_dir) / filename
    
    with open(filepath, "w") as f:
        json.dump(full_output, f, indent=2)
    
    print(f"\nResults saved to: {filepath}")
    
    if mode != "ole":
        return filepath, None

    # Also save tracker-compatible summary
    tracker_output = {
        "circuit_model": f"operator_loschmidt_echo_{config['circuit'].lower()}",
        "observable": "Z_52 Z_59 Z_72",
        "backend": config["backend"],
        "shots_per_run": config["shots"],
        "n_runs": config["n_runs"],
        "result_unmitigated": {
            "value": results["raw"]["mean"],
            "error_lower": results["raw"]["mean"] - results["raw"]["ci_lower"],
            "error_upper": results["raw"]["ci_upper"] - results["raw"]["mean"],
        },
        "result_h2q_mitigated": {
            "value": results["mitigated"]["mean"],
            "error_lower": results["mitigated"]["mean"] - results["mitigated"]["ci_lower"],
            "error_upper": results["mitigated"]["ci_upper"] - results["mitigated"]["mean"],
        },
        "improvement": {
            "description": "H2Q thermodynamic error mitigation",
            "kept_fraction": results["kept_fraction"]["mean"],
            "entropy_reduction_bits": results["entropy_reduction"]["mean"],
        },
        "timestamp": datetime.now().isoformat(),
    }
    
    tracker_filename = f"tracker_submission_{config['circuit']}_{timestamp}.json"
    tracker_filepath = Path(output_dir) / tracker_filename
    
    with open(tracker_filepath, "w") as f:
        json.dump(tracker_output, f, indent=2)
    
    print(f"Tracker-compatible output: {tracker_filepath}")
    
    return filepath, tracker_filepath

def print_summary(results: dict, config: dict):
    """Print human-readable summary."""
    print("\n" + "="*60)
    if config.get("mode") == "falsification":
        print("FNMN NOTEBOOK (Falsification Protocol)")
    else:
        print("H²Q BENCHMARK RESULTS SUMMARY")
    print("="*60)
    print(f"Circuit: {config['circuit']}")
    print(f"Backend: {config['backend']}")
    print(f"Shots per run: {config['shots']}")
    print(f"Number of runs: {config['n_runs']}")
    print("-"*60)
    if config.get("mode") == "falsification":
        print("Metric: TVD to simulator ideal (lower is better)")
        print("-"*60)
        print("RAW (unmitigated):")
        print(f"  TVD = {results['raw']['mean']:.6f}")
        print(f"  95% CI: [{results['raw']['ci_lower']:.6f}, {results['raw']['ci_upper']:.6f}]")
        print("-"*60)
        print("H²Q MITIGATED:")
        print(f"  TVD = {results['mitigated']['mean']:.6f}")
        print(f"  95% CI: [{results['mitigated']['ci_lower']:.6f}, {results['mitigated']['ci_upper']:.6f}]")
        print("-"*60)
        print("MITIGATION METRICS:")
        print(f"  Kept fraction: {results['kept_fraction']['mean']*100:.1f}%")
        print(f"  Δ(mean TVD) = {results['improvement']['delta_mean']:.6f}  (positive = closer to ideal)")
        # High-signal notebook trace
        if isinstance(results.get("notebook"), dict):
            nb = results["notebook"]
            print("-"*60)
            print("FNMN Notebook Trace (top keys / key formatting):")
            ideal_top = nb.get("ideal_top10", [])
            if ideal_top:
                print("  Ideal top-5:", ideal_top[:5])
            per_run = nb.get("per_run", [])
            if per_run:
                print("  Run0 inferred_width:", per_run[0].get("inferred_width"))
                print("  Run0 raw_key_samples:", per_run[0].get("raw_key_samples"))
                print("  Run0 raw_key_samples_canonical:", per_run[0].get("raw_key_samples_canonical"))
    else:
        print(f"Observable: O = Z_52 Z_59 Z_72")
        print("-"*60)
        print("RAW (unmitigated):")
        print(f"  <O> = {results['raw']['mean']:.6f}")
        print(f"  95% CI: [{results['raw']['ci_lower']:.6f}, {results['raw']['ci_upper']:.6f}]")
        print("-"*60)
        print("H²Q MITIGATED:")
        print(f"  <O> = {results['mitigated']['mean']:.6f}")
        print(f"  95% CI: [{results['mitigated']['ci_lower']:.6f}, {results['mitigated']['ci_upper']:.6f}]")
        print("-"*60)
        print("MITIGATION METRICS:")
        print(f"  Kept fraction: {results['kept_fraction']['mean']*100:.1f}%")
        print(f"  Entropy reduction: {results['entropy_reduction']['mean']:.3f} bits")
    print("="*60)

def main():
    parser = argparse.ArgumentParser(
        description="Run OLE benchmark with H²Q mitigation"
    )
    parser.add_argument(
        "--circuit", 
        choices=["70Q", "49Q_L6", "49Q_L3", "REP3", "REP5"],
        default="49Q_L3",
        help="Circuit to run (default: 49Q_L3 for testing). Use REP3/REP5 for falsification."
    )
    parser.add_argument(
        "--backend",
        default="ibm_fez",
        help="IBM backend name (default: ibm_fez)"
    )
    parser.add_argument(
        "--shots",
        type=int,
        default=8192,
        help="Shots per run (default: 8192)"
    )
    parser.add_argument(
        "--n-runs",
        type=int,
        default=5,
        help="Number of runs for statistics (default: 5)"
    )
    parser.add_argument(
        "--simulate",
        action="store_true",
        help="Run on simulator instead of hardware"
    )
    parser.add_argument(
        "--submit-only",
        action="store_true",
        help="Submit job(s) and print Job IDs without waiting for results"
    )
    parser.add_argument(
        "--job-ids",
        default="",
        help="Comma-separated Runtime job IDs to fetch + analyze (no submission)"
    )
    parser.add_argument(
        "--job-registry",
        default="",
        help="Path to a submitted_jobs_*.json registry file to fetch + analyze"
    )
    parser.add_argument(
        "--theta-on",
        type=float,
        default=0.8,
        help="H²Q upper hysteresis threshold (default: 0.8)"
    )
    parser.add_argument(
        "--theta-off",
        type=float,
        default=0.2,
        help="H²Q lower hysteresis threshold (default: 0.2)"
    )
    parser.add_argument(
        "--tau",
        type=int,
        default=10,
        help="H²Q minimum population threshold (default: 10)"
    )
    
    args = parser.parse_args()

    # Fetch mode (no submission)
    job_ids: list[str] = []
    if args.job_ids.strip():
        job_ids = [x.strip() for x in args.job_ids.split(",") if x.strip()]
    if args.job_registry.strip():
        with open(args.job_registry, "r") as f:
            reg = json.load(f)
        job_ids = [str(x) for x in reg.get("job_ids", [])]
        # If registry contains shots/backend/circuit, use as defaults when CLI omitted
        if not args.backend and reg.get("backend"):
            args.backend = reg["backend"]
        if reg.get("shots"):
            args.shots = int(reg["shots"])
        if reg.get("circuit"):
            args.circuit = reg["circuit"]

    if job_ids:
        print("\nFetching existing Runtime jobs (no submission)...")
        all_counts, fetch_meta = fetch_counts_for_jobs(job_ids, shots_hint=args.shots or None)
        backend_name = fetch_meta.get("backend") or "unknown-backend"
        # Proceed to mitigation+analysis below, and attach provenance later
        # If we need simulator ground truth (falsification), load the circuit now.
        circuit = load_benchmark_circuit(args.circuit)
    else:

        # Load circuit
        circuit = load_benchmark_circuit(args.circuit)

        # Setup
        if args.simulate:
            print("\n*** SIMULATION MODE ***")
            backend_name = "aer_simulator"
            all_counts = run_simulation(circuit, args.shots, args.n_runs)
        else:
            # Connect to IBM Quantum
            print("\nConnecting to IBM Quantum...")
            service = QiskitRuntimeService()
            backend = service.backend(args.backend)
            backend_name = backend.name

            print(f"Backend: {backend_name}")
            print(f"Qubits: {backend.num_qubits}")

            # Transpile
            transpiled = transpile_for_backend(circuit, backend)
            if args.submit_only:
                job_ids = submit_only(transpiled, backend, args.shots, args.n_runs)
                # Minimal on-disk provenance (no results yet)
                os.makedirs("results", exist_ok=True)
                stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                out = {
                    "timestamp": datetime.now().isoformat(),
                    "backend": backend_name,
                    "circuit": args.circuit,
                    "shots": args.shots,
                    "n_runs": args.n_runs,
                    "job_ids": job_ids,
                }
                path = Path("results") / f"submitted_jobs_{args.circuit}_{backend_name}_{stamp}.json"
                with open(path, "w") as f:
                    json.dump(out, f, indent=2)
                print(f"\nSaved job registry: {path}")
                return

            # Run (wait for results)
            all_counts = run_hardware(transpiled, backend, args.shots, args.n_runs)
    
    # Setup mitigator (locked parameters)
    mitigator = H2QMitigator(
        theta_on=args.theta_on,
        theta_off=args.theta_off,
        tau=args.tau
    )
    
    # Analyze
    if args.circuit in FALSIFICATION_CIRCUITS:
        ideal_probs = _simulate_ideal_distribution(circuit, shots=20000)
        results = analyze_falsification(all_counts, ideal_probs, mitigator)
        mode = "falsification"
    else:
        results = analyze_results(all_counts, mitigator)
        mode = "ole"
    
    # Save
    config = {
        "circuit": args.circuit,
        "backend": backend_name,
        "shots": args.shots,
        # Always reflect what we actually analyzed (esp. fetch mode)
        "n_runs": len(all_counts),
        "theta_on": args.theta_on,
        "theta_off": args.theta_off,
        "tau": args.tau,
        "mode": mode,
    }
    if job_ids:
        config["job_ids"] = job_ids
    
    save_results(results, config)
    
    # Print summary
    print_summary(results, config)

if __name__ == "__main__":
    main()

