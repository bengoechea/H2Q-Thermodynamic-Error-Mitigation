# Results Summary

**Last Updated:** December 5, 2025  
**Patent Reference:** US Provisional Application 63/927,371

---

## Hardware Validation Results

### Primary Metrics

| Metric | Value | Hardware | Job Reference |
|--------|-------|----------|---------------|
| False Positive Reduction | **79.7%** | ibm_fez, ibm_torino | d4lutmiv0j9c73e5nvt0 |
| Logical Fidelity | **97.63%** | ibm_fez (156-qubit) | d4lutmiv0j9c73e5nvt0 |
| Cross-Code Improvement | **895.72%** | Multiple backends | Aggregate |
| τ-Holevo χ Correlation | **r = 0.434** | ibm_fez | d4lutmiv0j9c73e5nvt0 |
| Hardware Runs | **15/15** | ibm_fez, ibm_torino | 100% success |

### Detailed Run Log

| Run | Backend | Qubits | Code | Baseline Error | H²Q Error | Reduction | Status |
|-----|---------|--------|------|----------------|-----------|-----------|--------|
| 1 | ibm_fez | 156 | [[5,1,3]] | 12.1% | 2.4% | 80.2% | ✅ |
| 2 | ibm_fez | 156 | [[5,1,3]] | 12.8% | 2.6% | 79.7% | ✅ |
| 3 | ibm_fez | 156 | [[7,1,3]] | 14.5% | 3.0% | 79.3% | ✅ |
| 4 | ibm_fez | 156 | [[7,1,3]] | 13.9% | 2.8% | 79.9% | ✅ |
| 5 | ibm_fez | 156 | Steane | 11.6% | 2.3% | 80.2% | ✅ |
| 6 | ibm_fez | 156 | Steane | 12.0% | 2.5% | 79.2% | ✅ |
| 7 | ibm_torino | 133 | [[5,1,3]] | 12.3% | 2.5% | 79.7% | ✅ |
| 8 | ibm_torino | 133 | [[5,1,3]] | 12.6% | 2.6% | 79.4% | ✅ |
| 9 | ibm_torino | 133 | [[7,1,3]] | 14.1% | 2.9% | 79.4% | ✅ |
| 10 | ibm_torino | 133 | [[7,1,3]] | 14.4% | 2.9% | 79.9% | ✅ |
| 11 | ibm_fez | 156 | [[5,1,3]] | 12.4% | 2.5% | 79.8% | ✅ |
| 12 | ibm_fez | 156 | [[7,1,3]] | 14.0% | 2.8% | 80.0% | ✅ |
| 13 | ibm_fez | 156 | Steane | 11.9% | 2.4% | 79.8% | ✅ |
| 14 | ibm_torino | 133 | Steane | 11.7% | 2.4% | 79.5% | ✅ |
| 15 | ibm_torino | 133 | Steane | 12.0% | 2.5% | 79.2% | ✅ |

**Average Reduction: 79.7% ± 0.4%**

### Observable Estimation (Quantum Advantage Tracker)

| Observable | Estimate | Error Low | Error High | Quantum (s) | Classical (s) | Device |
|------------|----------|-----------|------------|-------------|---------------|--------|
| Loschmidt Echo | 0.685 | 0.678 | 0.692 | 4100 | 1800 | ibm_pittsburgh |

---

## Thermodynamic Metrics

| Metric | Pre-H²Q | Post-H²Q | Change |
|--------|---------|----------|--------|
| Distribution Entropy | 4.82 bits | 2.71 bits | -43.7% |
| Free Energy (proxy) | 1.00 | 0.65 | -35.0% |
| Signal-to-Noise | 1.00× | 2.97× | +197% |
| States Retained | 100% | 6.5% | 93.5% filtered |

---

## Hysteresis Configuration

```
θ_on  = 0.8   (activation threshold)
θ_off = 0.3   (deactivation threshold)
τ     = 10    (dwell time in cycles)
```

---

## Reproducibility

All results reproducible with:
- IBM Quantum account (100+ qubit access)
- This repository's code
- Same hysteresis parameters

**Primary Job ID for verification:** `d4lutmiv0j9c73e5nvt0`

---

## Contact

Kenneth Mendoza  
ken@kenmendoza.com  
US Patent App 63/927,371
