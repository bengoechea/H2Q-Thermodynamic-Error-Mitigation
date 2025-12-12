# H²QEC Circuit Catalog

**Last Updated:** December 2025  
**Purpose:** Catalog of QASM circuit files for H²QEC validation and testing

---

## Existing QASM Circuit Files

### ✅ Found: 3 OLE (Overlap-Localized Error) Circuits

| Circuit | File | Qubits | Depth | Purpose |
|---------|------|--------|-------|---------|
| **OLE 49Q L=3** | `49Q_OLE_circuit_L_3_b_0.25_delta0.15.qasm` | 49 | ~1872 | IBM Quantum Advantage benchmark |
| **OLE 49Q L=6** | `49Q_OLE_circuit_L_6_b_0.25_delta0.15.qasm` | 49 | ~3744 | IBM Quantum Advantage benchmark (deeper) |
| **OLE 70Q L=6** | `70Q_OLE_circuit_L_6_b_0.25_delta0.15.qasm` | 70 | ~3744 | IBM Quantum Advantage benchmark (larger) |

**Location:** `./circuits/` (from repo root)

**Note:** These are OLE circuits, not standard QEC codes. H²QEC can be applied post-processing to analyze thermodynamic signatures.

---

## ✅ Generated: H²QEC-Specific QEC Circuits

### 1. Surface Code Circuit (5x5 Lattice)

**File:** `H2QEC_SURFACE_CODE_5x5.qasm`

- **Qubits:** 49 total
  - 25 data qubits (5×5 lattice)
  - 24 stabilizer qubits (X and Z stabilizers)
- **Code Distance:** 5
- **Purpose:** Full surface code implementation for H²QEC validation
- **Hardware Target:** `ibm_fez` (156-qubit), `ibm_torino` (133-qubit)
- **H²QEC Features:**
  - Hysteresis-based syndrome filtering
  - Dwell-time threshold (τ)
  - Asymmetric threshold (κ\_QEC; domain-calibrated)
  - False positive reduction (target: 79.7% per patent claims)

**Recommended Shots:** 8192 for production validation

---

### 2. Repetition Code (3-qubit)

**File:** `H2QEC_REPETITION_CODE_3q.qasm`

- **Qubits:** 3 data + 1 ancilla = 4 total
- **Code Distance:** 1 (error detection only)
- **Purpose:** Rapid H²QEC validation and testing
- **Hardware Target:** Any IBM system
- **H²QEC Features:**
  - Minimal overhead
  - Fast execution
  - Good for initial validation
- **Depth:** ~10-15 gates

**Recommended Shots:** 1024 for quick validation

---

### 3. Repetition Code (5-qubit)

**File:** `H2QEC_REPETITION_CODE_5q.qasm`

- **Qubits:** 5 data + 1 ancilla = 6 total
- **Code Distance:** 2 (error detection and correction)
- **Purpose:** Enhanced H²QEC validation with error correction
- **Hardware Target:** `ibm_fez`, `ibm_torino`
- **H²QEC Features:**
  - Better error correction than 3-qubit
  - Still manageable size
  - Good for comprehensive testing
- **Depth:** ~20-30 gates

**Recommended Shots:** 2048 for standard validation

---

## Circuit Size Recommendations

### For Quick Validation
- **Circuit:** 3-qubit Repetition Code
- **Qubits:** 3-4
- **Shots:** 1024
- **Time:** ~1-2 minutes
- **Use Case:** Initial H²QEC hysteresis gate testing

### For Standard Validation
- **Circuit:** 5-qubit Repetition Code
- **Qubits:** 5-6
- **Shots:** 2048
- **Time:** ~5-10 minutes
- **Use Case:** Comprehensive H²QEC testing with error correction

### For Production Validation
- **Circuit:** 5×5 Surface Code
- **Qubits:** 49
- **Shots:** 8192
- **Time:** ~30-60 minutes
- **Use Case:** Full H²QEC validation on realistic QEC code

### For Benchmark Integration
- **Circuits:** OLE circuits (49Q, 70Q)
- **Qubits:** 49-70
- **Shots:** 8192
- **Time:** ~1-2 hours
- **Use Case:** Apply H²QEC post-processing to IBM Quantum Advantage benchmarks

---

## circuit-models.json Entry

A complete `circuit-models.json` file has been created at:
`./circuits/circuit-models.json`

This JSON file includes:
- All circuit metadata
- H²QEC-specific parameters (κ\_QEC, dwell-time thresholds)
- Validation metrics and targets
- Circuit recommendations for different use cases
- Hardware target information

---

## H²QEC Parameters

### Domain-Calibrated Asymmetry Ratio (κ)
- Calibration-dependent and backend-specific. Implementable calibration formulas and tuned constants are withheld in the public repo.

### Dwell-Time Threshold (τ)
- Persistence gating is configurable (units depend on the experimental/control setting). Numeric settings and selection procedures are withheld in the public repo.

### Asymmetric Thresholds
- Asymmetric decision thresholds create hysteresis (resistance to rapid state flips). Implementable formulas and tuned constants are withheld in the public repo.

---

## Validation Targets

Based on H²QEC patent claims:
- **False Positive Reduction:** 79.7% (validated on `ibm_fez`)
- **Hardware Validated:** `ibm_fez` (156-qubit), `ibm_torino` (133-qubit)
- **Statistical Significance:** Cohen's d = 10.59, p < 0.0001

---

## Usage Instructions

### Loading Circuits in Python

```python
from qiskit import QuantumCircuit
from qiskit.qasm3 import loads as load_qasm3

# Load H²QEC Surface Code
with open('circuits/H2QEC_SURFACE_CODE_5x5.qasm', 'r') as f:
    qasm_content = f.read()
circuit = load_qasm3(qasm_content)

print(f"Qubits: {circuit.num_qubits}")
print(f"Depth: {circuit.depth()}")
```

### Using circuit_loader.py

The existing `circuit_loader.py` can be extended to load H²QEC circuits:

```python
from src.circuit_loader import load_benchmark_circuit

# Load H²QEC circuits (add to CIRCUIT_FILES dict)
circuit = load_benchmark_circuit("H2QEC_Surface_5x5", circuits_dir="circuits")
```

---

## Next Steps

1. **Test Generated Circuits:**
   - Run 3-qubit repetition code on IBM hardware
   - Validate H²QEC hysteresis gate functionality
   - Measure false positive reduction

2. **Extend circuit_loader.py:**
   - Add H²QEC circuits to CIRCUIT_FILES mapping
   - Update load_benchmark_circuit() function

3. **Run Validation Experiments:**
   - Execute on `ibm_fez` or `ibm_torino`
   - Compare with/without H²QEC hysteresis filtering
   - Measure 79.7% false positive reduction target

4. **Document Results:**
   - Update validation reports
   - Add to IBM Quantum Advantage application materials

---

## File Locations

| File | Location |
|------|----------|
| **OLE Circuits** | `QEC-IBM-Quantum-Advantage/circuits/` |
| **H²QEC Surface Code** | `QEC-IBM-Quantum-Advantage/circuits/H2QEC_SURFACE_CODE_5x5.qasm` |
| **H²QEC Repetition 3q** | `QEC-IBM-Quantum-Advantage/circuits/H2QEC_REPETITION_CODE_3q.qasm` |
| **H²QEC Repetition 5q** | `QEC-IBM-Quantum-Advantage/circuits/H2QEC_REPETITION_CODE_5q.qasm` |
| **circuit-models.json** | `QEC-IBM-Quantum-Advantage/circuits/circuit-models.json` |
| **This Catalog** | `QEC-IBM-Quantum-Advantage/circuits/H2QEC_CIRCUIT_CATALOG.md` |

---

**Document prepared:** December 2025  
**For questions:** Refer to H²QEC patent specification (US App. 63/927,371)




