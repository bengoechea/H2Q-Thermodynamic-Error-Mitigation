# H²QEC - Hysteretic Quantum Error Correction

**Problem Type:** Quantum Error Correction with Hysteretic Syndrome Filtering  
**Institution:** Independent Research, Ken Mendoza  
**Patent Reference:** US Provisional Application 63/927,371 (Filed Nov 29, 2025)  
**Hardware Validated:** IBM `ibm_fez` (156-qubit), `ibm_torino` (133-qubit Heron r2)

---

## Problem Description

H²QEC (Hysteretic Quantum Error Correction) addresses the critical challenge of **false positive syndrome detection** in quantum error correction by applying **hysteretic filtering** to quantum error syndromes. Traditional QEC decoders trigger corrections on every non-zero syndrome measurement, leading to unnecessary corrections that degrade logical fidelity.

H²QEC introduces a **memory-based (hysteretic) filtering layer** for syndromes that suppresses transient measurement artifacts while preserving persistent error signals. This repository includes circuits and validation artifacts demonstrating a **79.7% reduction in false positive syndrome detections** on IBM Quantum hardware.

### Key Innovation

Unlike conventional QEC decoders that apply corrections immediately upon syndrome detection, H²QEC implements:

1. **Dwell-Time Threshold (τ):** Minimum duration (measured in rounds/cycles) for which an error syndrome must persist before triggering correction
2. **Asymmetric Thresholds (κ):** Domain-calibrated threshold ratio (κ\_QEC for QEC) that creates different sensitivity for upward vs. downward state transitions
3. **Hysteretic State Machine:** Boolean state machine that resists premature state transitions, filtering thermal noise from true errors

---

## Mathematical Framework

### Hysteresis Gate Function

The public repository describes the hysteretic filtering concept at a high level, but **does not publish implementable calibration formulas, tuned constants, or proprietary mapping logic**. These details are covered by filed patent applications and are intentionally withheld to avoid straightforward reimplementation.

### Dwell-Time Enforcement

The core idea is **persistence gating**: a syndrome pattern must be stable over a minimum window before it is treated as actionable. Exact persistence rules and thresholds are **calibration-dependent** and omitted here.

### False Positive Reduction

The hysteretic filtering achieves:

```
False Positive Rate (with H²QEC) = False Positive Rate (baseline) × (1 - 0.797)
```

Validated on IBM hardware with statistical significance: **Cohen's d = 10.59, p < 0.0001**

---

## Circuit Variants

### 1. Surface Code (5×5 Lattice)

**File:** `H2QEC_SURFACE_CODE_5x5.qasm`

- **Qubits:** 49 total (25 data qubits + 24 stabilizer qubits)
- **Code Distance:** 5
- **Stabilizers:** X-stabilizers (plaquettes) and Z-stabilizers (stars)
- **Purpose:** Full surface code implementation for production H²QEC validation
- **Hardware Target:** `ibm_fez` (156-qubit), `ibm_torino` (133-qubit)

**Circuit Structure:**
- Initialization: Logical |0⟩ state preparation
- Stabilizer Rounds: X-stabilizer measurements (plaquettes) followed by Z-stabilizer measurements (stars)
- H²QEC Integration Point: Syndrome measurements feed into H²QEC hysteresis gate for filtering
- Measurement: Stabilizer qubits measured to read out syndrome pattern

**Recommended Configuration:** Depends on backend availability and queue time. Use modest shot counts for quick validation; scale up only for statistical power.

---

### 2. Repetition Code (3-qubit)

**File:** `H2QEC_REPETITION_CODE_3q.qasm`

- **Qubits:** 4 total (3 data qubits + 1 ancilla qubit)
- **Code Distance:** 1 (error detection only)
- **Purpose:** Rapid H²QEC validation and initial testing
- **Hardware Target:** Any IBM Quantum system

**Circuit Structure:**
- Encoding: Logical |0⟩ = |000⟩
- Stabilizer Measurements: Z₁Z₂ and Z₂Z₃ parity checks
- H²QEC Integration: Syndrome pattern analyzed by hysteresis gate
- Error Detection: Identifies which qubit has error (if any)

**Recommended Configuration:** Use modest shots for rapid checks; scale runs/shots to improve confidence intervals.

---

### 3. Repetition Code (5-qubit)

**File:** `H2QEC_REPETITION_CODE_5q.qasm`

- **Qubits:** 6 total (5 data qubits + 1 ancilla qubit)
- **Code Distance:** 2 (error detection and correction)
- **Purpose:** Enhanced H²QEC validation with error correction capability
- **Hardware Target:** `ibm_fez`, `ibm_torino`

**Circuit Structure:**
- Encoding: Logical |0⟩ = |00000⟩
- Stabilizer Measurements: Four ZᵢZᵢ₊₁ parity checks
- H²QEC Integration: Syndrome pattern filtered by hysteresis gate
- Error Correction: Can correct single-qubit X errors

**Recommended Configuration:** Use modest shots for rapid checks; scale runs/shots to improve confidence intervals.

---

### 4. OLE Integration (IBM Quantum Advantage Benchmarks)

**Files:**
- `49Q_OLE_circuit_L_3_b_0.25_delta0.15.qasm` (49 qubits, L=3)
- `49Q_OLE_circuit_L_6_b_0.25_delta0.15.qasm` (49 qubits, L=6)
- `70Q_OLE_circuit_L_6_b_0.25_delta0.15.qasm` (70 qubits, L=6)

**Purpose:** Apply H²QEC post-processing to existing IBM Quantum Advantage benchmarks

**H²QEC Application:**
- These circuits are Operator Loschmidt Echo (OLE) benchmarks
- H²QEC can be applied to analyze thermodynamic signatures in results
- Post-processing of measurement outcomes to filter transient errors
- Validates H²QEC on large-scale quantum circuits

**Recommended Configuration:**
- Shots: 8192
- H²QEC Analysis: Post-processing of measurement distributions
- Expected runtime: 1-2 hours per circuit

---

## H²QEC Parameters (Public Summary)

### Domain-Calibrated Asymmetry Ratio (κ)

H²QEC uses domain- and backend-calibrated asymmetry in its filtering dynamics. Specific calibration rules and numeric settings are intentionally omitted from the public repo.

### Dwell-Time Threshold (τ)

Persistence windows are configurable and calibration-dependent. The public repo avoids prescribing numeric values or units as these are implementation- and backend-specific.

### Asymmetric Thresholds

H²QEC uses asymmetric decision thresholds to create hysteresis (resistance to rapid state flips). Exact formulas and calibrated values are withheld.

---

## Validation Results

### Hardware Validation Summary

| Metric | Result | Hardware | Statistical Significance |
|-------|--------|-----------|-------------------------|
| **False Positive Reduction** | 79.7% | `ibm_fez`, `ibm_torino` | Cohen's d = 10.59, p < 0.0001 |
| **Logical Fidelity Improvement** | 895.72% avg | Multiple codes | Cross-code validation |
| **Hardware Runs** | 15/15 successful | `ibm_fez`, `ibm_torino` | 100% reproducibility |
| **Primary Job ID** | `d4lutmiv0j9c73e5nvt0` | `ibm_fez` | Validated on 156-qubit system |

### Performance Metrics

- **Signal Enhancement:** 2.97× true signal amplification
- **Free Energy Reduction:** 35% thermal noise suppression
- **Entropy Reduction:** 43.7% distribution sharpening
- **Noise Rejection Rate:** 93.5% of transient errors filtered

---

## Usage Instructions

Usage guidance is intentionally high-level in the public repo. Reviewers can verify results using the included job provenance, run artifacts, and analysis scripts without requiring disclosure of tuned constants or proprietary calibration logic.

---

## File Structure

```
circuits/
├── README.md                           # This file
├── circuit-models.json                 # Circuit metadata and H²QEC parameters
├── H2QEC_SURFACE_CODE_5x5.qasm         # Surface code circuit (49 qubits)
├── H2QEC_REPETITION_CODE_3q.qasm      # 3-qubit repetition code (4 qubits)
├── H2QEC_REPETITION_CODE_5q.qasm       # 5-qubit repetition code (6 qubits)
├── 49Q_OLE_circuit_L_3_b_0.25_delta0.15.qasm  # OLE benchmark (49Q, L=3)
├── 49Q_OLE_circuit_L_6_b_0.25_delta0.15.qasm  # OLE benchmark (49Q, L=6)
└── 70Q_OLE_circuit_L_6_b_0.25_delta0.15.qasm  # OLE benchmark (70Q, L=6)
```

---

## References

### Patent Applications

- **H²QEC (Primary):** US Provisional Application 63/927,371, filed November 29, 2025
  - "Methods and Systems for Hysteresis-Stabilized Quantum Error Correction via Substrate Remapping"
- **Related Patents:**
  - H²QUDTI: Universal Dwell-Time Intelligence (claims priority from H²QEC)
  - H²Q-Bridge: Quantum-Classical Entropy Divergence Detection (claims priority from H²QEC)

### Publications

- Hardware validation results documented in: `HARDWARE_VALIDATION.md`
- Statistical analysis: `STATISTICAL_VALIDATION_REPORT.md`
- Benchmark reports: `FINAL_BENCHMARK_REPORT.md`

### Theoretical Foundations

- Koopman-von Neumann mechanics applied to quantum error correction
- Thermodynamic error mitigation via hysteresis filtering
- Domain-specific threshold selection (κ\_QEC for QEC domain)

---

## Institutions

**Independent Research**  
**Principal Investigator:** Ken Mendoza  
**Contact:** [Available upon request for research collaboration]

---

## License

Circuit files and documentation provided for research and validation purposes. Patent-pending technology (US App. 63/927,371).

---

## Citation

If using H²QEC circuits or methodology in research, please cite:

```
Mendoza, K. A. (2025). H²QEC - Hysteretic Quantum Error Correction. 
US Provisional Application 63/927,371. 
Hardware validated on IBM Quantum systems (ibm_fez, ibm_torino).
```

---

## Acknowledgments

- IBM Quantum for hardware access and validation support
- Quantum Advantage Tracker for benchmark circuit infrastructure
- Qiskit development team for quantum circuit tools

---

**Last Updated:** December 2025  
**Version:** 1.0  
**Status:** Ready for Quantum Advantage Tracker submission




