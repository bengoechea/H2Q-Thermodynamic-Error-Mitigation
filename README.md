# H²Q Thermodynamic Error Mitigation: Quantum Advantage Tracker Benchmark

**Patent Reference:** US application 63/927,371  
**Patent Details:** https://kenmendoza.com/patents

## Overview
- Implements patent-backed thermodynamic error mitigation for the operator_loschmidt_echo_70x1872 observable estimation (part of the IBM Quantum Advantage Tracker).
- Demonstrates quantum expectation estimation with physically-grounded confidence bounds.
- Publishes all code and results for open verification and benchmarking.

## Method
See `/src/h2q_mitigation.py` for the key implementation of the H²Q approach. See [patent documentation](https://kenmendoza.com/patents) for algorithm details.

The H²Q method applies thermodynamic error mitigation by:
- Filtering measurement outcomes using hysteresis thresholds (`theta_on`, `theta_off`)
- Minimizing free energy of the error distribution
- Providing physically-grounded confidence intervals based on thermodynamic entropy

## Repo Contents
| Folder/File      | Purpose                                                              |
|------------------|----------------------------------------------------------------------|
| /src/            | All source code (Python, Qiskit, H²Q modules)                        |
| /experiments/    | Jupyter notebooks for demo and tests                                 |
| /data/           | Raw measurement data and sample input files                          |
| /results/        | Output data, plots and reproducibility logs                          |
| /docs/           | Optional: detailed method docs, references, supplementary notes      |

## How To Run
1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set up IBM Quantum API access (see Qiskit docs).

3. Run the main experiment:

**Simulation mode (for testing):**
```bash
python src/experiment_runner.py --mode simulation --qubits 10
```

**Hardware mode (requires IBM Quantum account):**
```bash
python src/experiment_runner.py --mode hardware --backend ibm_pittsburgh --qubits 70
```

or use the Jupyter notebook in `/experiments/`.

4. Results will appear in `/results/results.json` and be summarized in `results.md`.

## Performance Analysis

The repository includes performance visualizations comparing H²Q with other error mitigation methods:

- **Empirical Results**: Measured H²Q performance at δ² = 0.02 (moderate noise level)
  - Signal enhancement: 2.97x improvement
  - Free energy reduction: 35%
  - Entropy reduction: 43.7%
  - Noise filtering: 93.5% of states removed

- **Theoretical Model**: Predicted H²Q performance across noise levels based on thermodynamic framework
  - Model documented in methodology
  - Based on hysteresis threshold behavior
  - Optimal performance at δ² ≈ 0.02

**Note**: Visualizations distinguish between empirical (measured) and theoretical (model-based) results. All theoretical components are clearly labeled and methodology is provided.

## Citations
If used, please cite as:
> Mendoza, K. H²Q Thermodynamic Error Mitigation: Quantum Advantage Tracker, 2025. US app 63/927,371.

## License

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

**Patent Notice**: This software implements methods covered by U.S. Patent
Application 63/927,371. Patent rights are granted under the Apache License 2.0,
subject to the license termination provisions. For commercial licensing
inquiries, contact ken@kenmendoza.com.

See PATENT.txt for additional patent information.

## Contributors and Contact
Lead: Ken Mendoza  
Contact: ken@kenmendoza.com
