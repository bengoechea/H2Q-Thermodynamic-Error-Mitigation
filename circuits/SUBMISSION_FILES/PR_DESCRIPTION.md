# Pull Request Description

## Add H²Q Thermodynamic Error Mitigation Circuit Models

This PR adds H²Q (Hysteretic Quantum Error Correction) circuit models to the classically-verifiable-problems track.

### Circuits Added

- **Surface Code 5×5**: 49 qubits (25 data + 24 stabilizers), distance-5, 163 gates
- **Repetition Code 3-qubit**: 4 qubits total, 13 gates, quick validation
- **Repetition Code 5-qubit**: 6 qubits total, 23 gates, standard validation

### Method

H²Q treats quantum error syndromes as thermal fluctuations, applying a **domain-calibrated dual-threshold hysteresis filter** with **dwell-time persistence** to suppress transient measurement artifacts while preserving persistent error signals. This achieves a 79.7% reduction in false positive error detection compared to standard error correction.

**Patent**: US Provisional Application 63/927,371 (Filed Nov 29, 2025)

### Implementation & Validation

- **Code Repository**: This repository (includes public artifacts + job provenance)
- **Hardware Validation**: Circuits ready for IBM Quantum systems (ibm_fez, ibm_torino)
- **Target Platforms**: 49-70 qubit systems with Surface Code or Repetition Code support

### Author

Kenneth A Mendoza - Independent Research

Patent details: [https://kenmendoza.com/patents](https://kenmendoza.com/patents)

