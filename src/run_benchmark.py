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
            
            # Extract counts
            counts = result[0].data.meas.get_counts()
            all_counts.append(counts)
            
            print(f"Done. Job ID: {job.job_id()}")
    
    return all_counts

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
        
        # Apply H²Q mitigation
        mitigated_probs = mitigator.apply_correction(counts)
        
        # Convert probabilities back to counts for observable calculation
        total = sum(counts.values())
        mitigated_counts = {k: int(v * total) for k, v in mitigated_probs.items() if v > 0}
        
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

def save_results(results: dict, config: dict, output_dir: str = "results"):
    """Save results in tracker-compatible format."""
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Full results
    full_output = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "circuit": config["circuit"],
            "backend": config["backend"],
            "shots": config["shots"],
            "n_runs": config["n_runs"],
            "observable": "Z_52 Z_59 Z_72",
            "method": "H2Q Thermodynamic Error Mitigation",
            "patent": "US Provisional 63/927,371",
        },
        "results": results,
        "h2q_config": {
            "theta_on": config["theta_on"],
            "theta_off": config["theta_off"],
            "tau": config["tau"],
        }
    }
    
    filename = f"ole_results_{config['circuit']}_{config['backend']}_{timestamp}.json"
    filepath = Path(output_dir) / filename
    
    with open(filepath, "w") as f:
        json.dump(full_output, f, indent=2)
    
    print(f"\nResults saved to: {filepath}")
    
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
    print("H²Q BENCHMARK RESULTS SUMMARY")
    print("="*60)
    print(f"Circuit: {config['circuit']}")
    print(f"Backend: {config['backend']}")
    print(f"Shots per run: {config['shots']}")
    print(f"Number of runs: {config['n_runs']}")
    print("-"*60)
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
        choices=["70Q", "49Q_L6", "49Q_L3"],
        default="49Q_L3",
        help="Circuit to run (default: 49Q_L3 for testing)"
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
        
        # Run
        all_counts = run_hardware(transpiled, backend, args.shots, args.n_runs)
    
    # Setup mitigator
    mitigator = H2QMitigator(
        theta_on=args.theta_on,
        theta_off=args.theta_off,
        tau=args.tau
    )
    
    # Analyze
    results = analyze_results(all_counts, mitigator)
    
    # Save
    config = {
        "circuit": args.circuit,
        "backend": backend_name,
        "shots": args.shots,
        "n_runs": args.n_runs,
        "theta_on": args.theta_on,
        "theta_off": args.theta_off,
        "tau": args.tau,
    }
    
    save_results(results, config)
    
    # Print summary
    print_summary(results, config)

if __name__ == "__main__":
    main()

