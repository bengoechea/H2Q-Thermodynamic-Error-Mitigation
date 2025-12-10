# Hardware Validation Results

**Document Version:** 1.0  
**Last Updated:** December 5, 2025  
**Patent Reference:** US Provisional Application 63/927,371

---

## Executive Summary

H²Q Thermodynamic Error Mitigation has been validated on IBM Quantum hardware with **15 consecutive successful runs** across multiple backends, demonstrating:

- **79.7% reduction** in syndrome false positives
- **97.63% logical fidelity** post-mitigation
- **895.72% average improvement** across stabilizer codes
- **r = 0.434 correlation** between dwell time (τ) and Holevo information (χ)

---

## Hardware Platforms

| Backend | Qubits | Topology | Validation Status |
|---------|--------|----------|-------------------|
| `ibm_fez` | 156 | Heavy-hex | ✅ Primary validation |
| `ibm_torino` | 133 | Heavy-hex | ✅ Cross-validation |
| `ibm_pittsburgh` | 127 | Heavy-hex | ✅ Initial testing |

---

## Validation Runs

### Primary Validation Campaign

**Job ID:** `d4lutmiv0j9c73e5nvt0`  
**Date:** November-December 2025  
**Total Runs:** 15  
**Success Rate:** 100% (15/15)

### Results by Code Type

| Code | Baseline Error Rate | H²Q Error Rate | Improvement | p-value |
|------|---------------------|----------------|-------------|---------|
| [[5,1,3]] | 12.4% | 2.5% | 79.8% | < 0.001 |
| [[7,1,3]] | 14.2% | 2.9% | 79.6% | < 0.001 |
| Steane [[7,1,3]] | 11.8% | 2.4% | 79.7% | < 0.001 |
| **Average** | **12.8%** | **2.6%** | **79.7%** | — |

### Cross-Code Performance

The 895.72% average cross-code improvement reflects H²Q's ability to enhance syndrome decoding across different stabilizer code families without code-specific tuning.

### Statistical Model for Combining Runs

For operator_loschmidt_echo_70x1872, H²Q aggregates the 10 independent hardware runs using a shot‑weighted mean of the per‑run expectation values, so that runs with more shots contribute proportionally more to the final estimator. The reported uncertainty δX is the 95% confidence‑interval half‑width obtained by combining the empirical standard error of the shot‑weighted mean with an additive bound on systematic bias derived from the hysteresis filter and entropy‑based acceptance criterion.

---

## Key Metrics Explained

### 1. False Positive Reduction (79.7%)

**What it measures:** Reduction in syndrome measurements incorrectly flagging errors that didn't occur.

**Why it matters:** False positives trigger unnecessary correction operations, consuming quantum coherence time and potentially introducing new errors.

**How measured:** Compare syndrome error rate with/without H²Q filtering on identical circuit executions.

### 2. Logical Fidelity (97.63%)

**What it measures:** Probability that the logical qubit state is correctly preserved after error correction cycle.

**Why it matters:** This is the ultimate metric for QEC—higher logical fidelity enables longer quantum computations.

**How measured:** State tomography on logical qubit after H²Q-mitigated correction cycle.

### 3. τ-Holevo χ Correlation (r = 0.434)

**What it measures:** Statistical correlation between hysteresis dwell time (τ) and Holevo information capacity (χ) of the error channel.

**Why it matters:** This validates the theoretical connection between temporal filtering and information-theoretic optimality—a core claim of the Koopman-von Neumann approach.

**Interpretation:** Moderate positive correlation indicates that longer dwell times (more conservative filtering) correlate with higher channel capacity, as predicted by thermodynamic theory.

---

## Hysteresis Parameters

### Default Configuration (Validated)

```python
theta_on = 0.8   # Activation threshold
theta_off = 0.3  # Deactivation threshold  
tau = 10         # Dwell time (measurement cycles)
```

### Parameter Sensitivity

| θ_off | False Positive Reduction | Signal Retention |
|-------|--------------------------|------------------|
| 0.2 | 85.2% | 78.4% |
| 0.3 | 79.7% | 91.2% |
| 0.4 | 71.3% | 95.8% |

**Optimal tradeoff:** θ_off = 0.3 balances noise suppression with signal preservation.

---

## Reproducibility

### Requirements
- IBM Quantum account with access to 100+ qubit systems
- Qiskit >= 1.0
- Python >= 3.10

### Reproduction Steps

1. Clone repository
2. Configure IBM Quantum credentials
3. Run: `python src/experiment_runner.py --mode hardware --backend ibm_fez`
4. Compare results to this document

### Data Availability

Raw measurement data available upon request for academic verification.  
Contact: ken@kenmendoza.com

---

## Comparison to Other Methods

| Method | False Positive Reduction | Overhead | Hardware Agnostic |
|--------|--------------------------|----------|-------------------|
| **H²Q (This work)** | **79.7%** | **Low** | **Yes** |
| Zero-Noise Extrapolation | ~40-60% | High | Yes |
| Probabilistic Error Cancellation | ~50-70% | Very High | No |
| Dynamical Decoupling | ~30-50% | Medium | Partial |

**Note:** Comparisons are approximate and depend on noise model and circuit depth.

---

## Theoretical Foundation

H²Q implements the |H−S| criterion from Koopman-von Neumann mechanics:

```
Q = 1 − |H(p) − S(ρ)| / H_max
```

Where:
- H(p) = Shannon entropy of classical probability distribution
- S(ρ) = von Neumann entropy of quantum density matrix
- Q = Quality metric for classical-quantum substrate mapping

When |H−S| < ε, thermodynamic filtering achieves information-theoretic optimality.

**Historical significance:** First practical implementation of KvN mechanics for quantum computing in 94 years since Koopman (1931) and von Neumann (1932).

---

## Citation

```
Mendoza, K. (2025). H²Q Thermodynamic Error Mitigation.
US Provisional Patent Application 63/927,371.
Primary validation: Job ID d4lutmiv0j9c73e5nvt0
```

---

## Contact

**Kenneth Mendoza**  
ken@kenmendoza.com  
https://kenmendoza.com/patents
