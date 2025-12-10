# H²Q-Bridge: Technical Validation Package

**Validation Partner Documentation (IBM / Riverlane)**

## Technical Abstract
This repository contains the reproduction artifacts for the "H²Q-Bridge" thermodynamic error mitigation protocol. The system encodes classical probability distributions $p(x)$ into quantum states $|\psi\rangle$ and measures von Neumann entropy $S(\rho)$ to detect divergences from classical Shannon entropy $H(p)$.

## Validation Data (IBM Quantum Heron)
We provide the raw Qiskit Runtime job results for 17 independent runs on `ibm_fez` (156 qubits) and `ibm_torino` (133 qubits).

### Job Registry
| Job ID | Backend | Date | Result (Cohen's d) |
| :--- | :--- | :--- | :--- |
| `d4q7prft...` | `ibm_fez` | 2025-12-06 | 10.59 |
| `d4q6f8nt...` | `ibm_torino` | 2025-12-06 | 10.42 |
| ... | ... | ... | ... |

*(Full registry available in `/results` directory)*

## Reproduction Steps
1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Authenticate:**
    Set `QISKIT_IBM_TOKEN` environment variable.
3.  **Run Verification:**
    ```bash
    python src/run_h2q_validation.py --backend ibm_fez
    ```

## Trade Secret Note
This repository contains the **Public Interface** and **Validation Logic**. The core proprietary Boolean mapping (TS-001) is abstracted over, allowing partners to verify the *quantum-thermodynamic* claims without exposing the classical preprocessing IP.

## License
Apache 2.0 (See `LICENSE`). Patent Rights Reserved (US App 63/927,371).
