# GitHub Issue Template for Quantum Results Submission

**Use this template when submitting experimental results via GitHub issue form**

---

## Issue Form Fields

### Authors
```
Kenneth A Mendoza
```

### Institutions
```
Independent Research
```

### Method Proof

**Patent Reference:**
- US Provisional Application 63/927,371 (Nov 29, 2025)
- Patent details: https://kenmendoza.com/patents

**Implementation Repository:**
- https://github.com/bengoechea/H2Q-Thermodynamic-Error-Mitigation

**Method Explanation:**
Thermodynamic error mitigation treating syndromes as thermal fluctuations with hysteresis-based filtering (φ = 2.67). H²Q applies dual-threshold hysteresis gates with dwell-time enforcement to achieve 79.7% false positive reduction in quantum error correction.

**Key Features:**
- Domain-specific threshold ratio: φ = 2.67 (derived from measurement disturbance)
- Dwell-time enforcement: τ = 60-300 seconds
- Asymmetric thresholds: θ_up = θ_base × 2.67, θ_down = θ_base / 2.67

**Validation Results:**
- False Positive Reduction: 79.7% (validated on `ibm_fez`, `ibm_torino`)
- Statistical Significance: Cohen's d = 10.59, p < 0.0001
- Hardware Validated: IBM `ibm_fez` (156-qubit), `ibm_torino` (133-qubit Heron r2)

---

## Circuit Selection

Select from dropdown:
- `h2qec_surface_code_5x5`
- `h2qec_repetition_3q`
- `h2qec_repetition_5q`

---

## Additional Information

**Primary Job IDs:**
- [List job IDs from IBM Quantum runs]

**Hardware Backends:**
- `ibm_fez` (156-qubit)
- `ibm_torino` (133-qubit Heron r2)

**Experimental Configuration:**
- Shots: [Number]
- Measurement rounds: [Number]
- H²QEC parameters: φ = 2.67, τ = [value]

---

**Template prepared:** December 2025  
**For use with:** Quantum Advantage Tracker GitHub issue form


