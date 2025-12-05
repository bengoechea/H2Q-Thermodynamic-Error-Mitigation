"""H²Q Experiment Runner

Patent reference: US application 63/927,371
Contact: ken@kenmendoza.com
"""

import json
import os
import argparse

from h2q_thermo import ThermodynamicErrorMitigation


def build_operator_loschmidt_echo_circuit():
    """Build or load the operator_loschmidt_echo_70x1872 circuit.

    TODO: Replace this placeholder with the actual circuit construction
    or loading from IBM's Quantum Advantage Tracker assets.
    """
    from qiskit import QuantumCircuit
    qc = QuantumCircuit(1)
    qc.h(0)
    qc.measure_all()
    return qc


def run_on_backend(circuit, backend_name="ibm_pittsburgh", provider_name="ibm-q"):
    """Execute circuit on the chosen backend and return raw result objects.

    TODO: Replace with real IBM Quantum runtime / provider logic.
    """
    from qiskit_aer import AerSimulator
    from qiskit import transpile

    sim = AerSimulator()
    tcirc = transpile(circuit, sim)
    job = sim.run(tcirc, shots=4096)
    result = job.result()
    return result


def estimate_observable_from_counts(counts):
    """Placeholder observable estimator from bitstring counts.

    TODO: Replace with the proper operator_loschmidt_echo_70x1872 observable.
    """
    shots = sum(counts.values())
    ones = sum(c for b, c in counts.items() if b.endswith("1"))
    return ones / shots if shots > 0 else 0.0


def main():
    parser = argparse.ArgumentParser(
        description="H²Q Thermodynamic Error Mitigation experiment runner"
    )
    parser.add_argument("--provider", type=str, default="ibm-q")
    parser.add_argument("--device", type=str, default="ibm_pittsburgh")
    parser.add_argument("--shots", type=int, default=4096)
    args = parser.parse_args()

    os.makedirs("results", exist_ok=True)

    circuit = build_operator_loschmidt_echo_circuit()
    raw_result = run_on_backend(
        circuit, backend_name=args.device, provider_name=args.provider
    )

    counts = raw_result.get_counts()
    raw_obs = estimate_observable_from_counts(counts)

    mitigator = ThermodynamicErrorMitigation(
        metadata={"device": args.device, "provider": args.provider}
    )
    mitigator.calibrate_from_data(counts)

    mitigated, (low, high) = mitigator.mitigate_expectation(
        raw_obs, raw_counts=counts
    )

    out = {
        "device": args.device,
        "provider": args.provider,
        "raw_observable": raw_obs,
        "mitigated_observable": mitigated,
        "error_low": low,
        "error_high": high,
        "shots": sum(counts.values()),
    }

    with open("results/result.json", "w") as f:
        json.dump(out, f, indent=2)

    print("Saved results to results/result.json")


if __name__ == "__main__":
    main()
