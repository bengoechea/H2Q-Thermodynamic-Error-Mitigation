# H²Q Thermodynamic Error Mitigation

**Patent Reference:** US Provisional Application 63/927,371 (Filed Nov 29, 2025)  
**Patent Details:** https://kenmendoza.com/patents

## Overview

H²Q implements **thermodynamic error mitigation** for quantum computing, treating syndrome measurement errors as thermal fluctuations that can be filtered using hysteresis-based controls derived from the Koopman-von Neumann formalism.

**Key Innovation:** First practical application of Koopman-von Neumann mechanics to quantum error correction in 94 years.

## Hardware Validation Summary

| Metric | Result | Hardware | Notes |
|--------|--------|----------|-------|
| **False Positive Reduction** | 79.7% | ibm_fez, ibm_torino | Syndrome error filtering |
| **Logical Fidelity** | 97.63% | ibm_fez (156-qubit) | Post-mitigation |
| **Cross-Code Improvement** | 895.72% avg | Multiple codes | vs. unmitigated baseline |
| **Hardware Runs** | 15/15 successful | ibm_fez, ibm_torino | 100% reproducibility |
| **τ-Holevo χ Correlation** | r = 0.434 | Hardware-validated | Dwell time ↔ channel capacity |

**Primary Job ID:** `d4lutmiv0j9c73e5nvt0`


## Current Status & Roadmap

### ✅ Validated (December 2024)
- **QEC Performance**: 79.7% false positive reduction on IBM Eagle r3/Heron processors
- **Hardware Validation**: 15/15 runs across ibm_fez (127-qubit) and ibm_torino backends
- **Cross-Code Universality**: 895.72% improvement across multiple QEC codes
- **Statistical Rigor**: 15 independent hardware runs with 100% reproducibility

### 🔄 In Progress / Planned
**Phase 1 (Critical for full advantage claim):**
- [ ] Baseline method comparisons (ZNE, CDR, TEM, NRE)
- [ ] VQE H₂ circuit validation (chemistry workload)
- [ ] Ground truth simulation comparisons
- [ ] Higher shot counts (8192-16384 vs current 4096)

**Phase 2 (Publication readiness):**
- [ ] Multi-circuit benchmark suite (QAOA, random circuits)
- [ ] Extended statistical validation (20+ runs minimum)
- [ ] Utility-scale demonstrations (100+ qubit circuits)

### ⚠️ Current Limitations
**This repository demonstrates:**
- Control-layer improvements for quantum error correction
- Hardware-agnostic approach applicable to multiple platforms
- Measurable improvements in QEC-specific metrics

**This repository does NOT yet claim:**
- Full "quantum advantage" by IBM/QOBLIB standards
- Direct comparison to industry-standard error mitigation (ZNE/CDR)
- Performance validation across diverse circuit types (VQE, QAOA, optimization)
- Utility-scale (100+ qubit) demonstrations

**Status**: This is a **control-layer infrastructure contribution** toward quantum advantage, not a completed advantage demonstration.

## Method

The H²Q approach applies thermodynamic error mitigation by:

1. **Hysteresis Filtering:** Measurement outcomes filtered using dual thresholds (`θ_on`, `θ_off`) that distinguish stable ground states from thermal noise
2. **Free Energy Minimization:** Error distribution "cooled" to reveal true signal
3. **Entropy-Based Confidence:** Physically-grounded intervals from Shannon entropy of filtered distribution

See `/src/h2q_mitigation.py` for implementation. See [patent documentation](https://kenmendoza.com/patents) for theoretical foundations.

### The |H−S| Criterion

The framework uses the divergence between Shannon entropy (H) and von Neumann entropy (S) as a quality metric:

```
Q = 1 − |H(p) − S(ρ)| / H_max
```

When |H−S| < ε, the system admits efficient quantum representation—this criterion routes problems to their optimal computational substrate.

## Repository Structure

| Folder/File | Purpose |
|-------------|----------|
| `/src/` | Core implementation (Python, Qiskit, H²Q modules) |
| `/experiments/` | Jupyter notebooks for demos and validation |
| `/data/` | Raw measurement data and calibration files |
| `/results/` | Output data, plots, reproducibility logs |
| `/docs/` | Method documentation and references |
| `HARDWARE_VALIDATION.md` | Detailed hardware results with job IDs |

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Running Experiments

**Simulation mode (testing):**
```bash
python src/experiment_runner.py --mode simulation --qubits 10
```

**Hardware mode (requires IBM Quantum account):**
```bash
python src/experiment_runner.py --mode hardware --backend ibm_fez --qubits 70
```

Results output to `/results/results.json` and summarized in `HARDWARE_VALIDATION.md`.

## Performance Analysis

### Empirical Results (Hardware-Validated)

At moderate noise levels (δ² ≈ 0.02), H²Q demonstrates:

| Metric | Value | Interpretation |
|--------|-------|----------------|
| Signal Enhancement | 2.97× | True signal amplification |
| Free Energy Reduction | 35% | Thermal noise suppression |
| Entropy Reduction | 43.7% | Distribution sharpening |
| States Filtered | 93.5% | Noise rejection rate |

### Theoretical Basis

The hysteresis thresholds derive from thermodynamic stability analysis:
- `θ_on = 0.8`: Activation threshold (high-probability = low-energy = stable)
- `θ_off = 0.3`: Deactivation threshold (low-probability = high-energy = noise)
- `τ = 10`: Dwell time for state confirmation

These values are empirically validated across multiple IBM Quantum backends and can be tuned for specific hardware noise profiles.

## Citation

If using this work, please cite:

```bibtex
@misc{mendoza2025h2q,
  author = {Mendoza, Kenneth},
  title = {H²Q Thermodynamic Error Mitigation: Quantum Advantage Tracker},
  year = {2025},
  note = {US Provisional Patent Application 63/927,371},
  url = {https://github.com/bengoechea/H2Q-Thermodynamic-Error-Mitigation}
}
```

## License

Apache License 2.0 with patent grant. See LICENSE and PATENT.txt.

**Patent Notice:** This software implements methods covered by U.S. Patent Application 63/927,371. Patent rights are granted under Apache 2.0, subject to license termination provisions.

For commercial licensing: ken@kenmendoza.com

## Contact

**Lead:** Kenneth Mendoza  
**Email:** ken@kenmendoza.com
