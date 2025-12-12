# H²Q-Bridge: Thermodynamic Error Mitigation

**Verification Engine for the "Omni-Field" Architecture**

## Overview
This repository contains the experimental validation data for the **H²Q-Bridge**, a patent-pending quantum-classical hybrid system (US Patent App. No. 63/927,371) that uses thermodynamic entropy divergence to detect anomalies in critical data streams.

Unlike traditional variational algorithms (VQE/QAOA) that suffer from "Barren Plateaus" and require thousands of iterations, the H²Q-Bridge employs a **Single-Shot Verification** method based on Koopman-von Neumann mechanics.

## Key Results
*   **Platform:** IBM Quantum Heron (`ibm_fez`, `ibm_torino`)
*   **Metric:** Thermodynamic Divergence $D = |H(p) - S(\rho)|$
*   **Statistical Significance:** $p < 0.0001$ (Cohen's d = 10.59)
*   **Speedup:** O(1) single-shot measurement vs. O(N) iterative optimization

## Public Disclosure Note (IP & Reproducibility)
This repository is intentionally published as a **verification and reproduction package**. It includes job artifacts, raw outputs, and a public reference interface sufficient to validate the reported results.

To avoid disclosing implementation details that enable straightforward reimplementation, **tuned constants, calibration heuristics, and proprietary mapping logic are not published here**. The method is covered by filed provisional patent applications referenced elsewhere in this repository. Researchers and reviewers can still independently verify outcomes using the included results, job provenance, and analysis scripts.

**Job registry & audit trail:** see `IBM_QUANTUM_RUNS_DOCUMENTATION.md` and `HARDWARE_VALIDATION.md`.

## FNMN Notebook: Beyond Best Practices Validation Battery
This project follows a “FNMN Notebook” standard: we compensate for intentionally withheld implementation details by publishing a **systemic falsification-first validation battery** that would *fail loudly* if the method were only post-selection or overfitting.

### What is locked (pre-registered)
*   **Evaluation metric(s)** and pass/fail criteria are fixed before runs.
*   **Run configuration** (backend, shots, number of repeats) is recorded.
*   **Reporting includes kept-fraction** so improvements cannot be achieved by silently discarding most outcomes.

### Falsification gates (designed to break the method)
1. **Simulator vs simulator gate**: the pipeline should not create “improvement” when the data are already ideal.
2. **Noise-injection gate**: under controlled injected noise, the method should move results toward a clean/simulator-constrained reference.
3. **Cross-backend / cross-day gate**: the same locked settings should remain directionally consistent under device drift and different noise realizations.

### Baselines and negative results
*   We compare against simple baselines (e.g., naive thresholding / top-k style filters) and report when the method does **not** help. This is deliberate: it reduces narrative flexibility and increases reviewer trust.

### How reviewers can verify without needing proprietary details
*   **Job provenance** is provided via `results/submitted_jobs_*.json` registries and the analysis scripts support fetching by Job ID.
*   The public repo focuses on *verification artifacts* (job IDs, run summaries, audit logs) rather than publishing a complete “how to tune and reproduce” recipe.

## Repository Structure
*   `/results`: Raw JSON output from 17 independent validation runs on IBM Hardware.
*   `/src`: Reference Python implementation of the H²Q-Bridge entropy engine.
*   `/experiments`: Jupyter notebooks demonstrating the "Barren Plateau" avoidance.

## Field of Application
This engine serves as the "Truth Layer" for the H² Ecosystem, including:
1.  **H²M (Materials):** Battery thermal runaway prevention.
2.  **H²QSense:** Quantum sensor network routing.
3.  **H²DeepFake:** Generative AI hallucination detection.

## Contact
**Kenneth Mendoza**
*Inventor & Independent Researcher*
ken@kenmendoza.com
