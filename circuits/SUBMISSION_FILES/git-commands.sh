#!/bin/bash
# Git commands for Quantum Advantage Tracker submission
# Execute these commands in your quantum-advantage-tracker repository root

# Navigate to repo (update path as needed)
# cd /path/to/quantum-advantage-tracker

# Create branch
git checkout -b add-h2qec-circuits

# Create directory structure
mkdir -p data/classically-verifiable-problems/circuit-models/h2qec

# Copy circuit files
cp ../QEC-IBM-Quantum-Advantage/circuits/H2QEC_SURFACE_CODE_5x5.qasm data/classically-verifiable-problems/circuit-models/h2qec/
cp ../QEC-IBM-Quantum-Advantage/circuits/H2QEC_REPETITION_CODE_3q.qasm data/classically-verifiable-problems/circuit-models/h2qec/
cp ../QEC-IBM-Quantum-Advantage/circuits/H2QEC_REPETITION_CODE_5q.qasm data/classically-verifiable-problems/circuit-models/h2qec/
cp ../QEC-IBM-Quantum-Advantage/circuits/SUBMISSION_FILES/README.md data/classically-verifiable-problems/circuit-models/h2qec/

# Stage files
git add data/classically-verifiable-problems/circuit-models/h2qec/
git add data/classically-verifiable-problems/circuit-models.json
git add .github/ISSUE_TEMPLATE/03-submission-path-classically-verifiable-problems.yml

# Commit
git commit -m "Add H²Q Thermodynamic Error Mitigation circuit models

Author: Kenneth A Mendoza
- Surface Code 5×5 (49 qubits, 163 gates)
- Repetition Code 3-qubit (4 qubits, 13 gates)
- Repetition Code 5-qubit (6 qubits, 23 gates)
- Hysteretic syndrome filtering with a domain-calibrated asymmetry ratio (κ_QEC)
- Target: 79.7% false positive reduction
- Patent: US Provisional 63/927,371

Implementation: this repository (public artifacts + job provenance; tuned calibration details withheld)"

echo "✅ Files staged and committed. Ready to push and create PR!"

