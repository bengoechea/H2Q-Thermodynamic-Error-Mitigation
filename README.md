# H²Q Thermodynamic Error Mitigation: Quantum Advantage Tracker Benchmark

**Patent Reference:** US application 63/927,371  
**Patent Details:** https://kenmendoza.com/patents

## Overview
- Implements patent-backed thermodynamic error mitigation for the operator_loschmidt_echo_70x1872 observable estimation (part of the IBM Quantum Advantage Tracker).
- Demonstrates quantum expectation estimation with physically-grounded confidence bounds.
- Publishes all code and results for open verification and benchmarking.

## Method
See `/src/h2q_thermo.py` for the key implementation of the H²Q approach. See [patent documentation](https://kenmendoza.com/patents) for algorithm details.

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

```bash
python src/run_experiment.py --provider ibm-q --device ibm_pittsburgh
```

or use the Jupyter notebook in `/experiments/`.

4. Results will appear in `/results/result.json` and be summarized in `results.md`.

## Citations
If used, please cite as:
> Mendoza, K. H²Q Thermodynamic Error Mitigation: Quantum Advantage Tracker, 2025. US app 63/927,371.

## License
MIT License unless otherwise specified in PATENT.txt.

## Contributors and Contact
Lead: Ken Mendoza  
Contact: ken@kenmendoza.com
