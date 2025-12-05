import argparse
import json
import time
import os
import numpy as np
from datetime import datetime
from qiskit import transpile
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import QiskitRuntimeService

from circuit_loader import load_benchmark_circuit
from h2q_mitigation import H2QMitigator

def run_experiment(mode='simulation', shots=1024, backend_name=None, num_qubits=70):
    """
    Runs the Quantum Advantage experiment.
    """
    print(f"--- Starting Experiment in {mode.upper()} mode ---")
    start_time = time.time()
    
    # 1. Load Circuit
    qc = load_benchmark_circuit(num_qubits=num_qubits)
    print(f"Circuit loaded: {qc.name} ({qc.num_qubits} qubits)")
    
    # 2. Setup Backend
    if mode == 'hardware':
        try:
            service = QiskitRuntimeService()
            if backend_name:
                backend = service.backend(backend_name)
            else:
                backend = service.least_busy(operational=True, simulator=False, min_num_qubits=qc.num_qubits)
            print(f"Connected to IBM Quantum backend: {backend.name}")
        except Exception as e:
            print(f"Error connecting to IBM Quantum: {e}")
            print("Falling back to simulation.")
            mode = 'simulation'
            # Use MPS for large qubit counts in simulation
            method = 'matrix_product_state' if num_qubits > 30 else 'automatic'
            backend = AerSimulator(method=method)
    else:
        # Use MPS for large qubit counts in simulation
        method = 'matrix_product_state' if num_qubits > 30 else 'automatic'
        backend = AerSimulator(method=method)
        print(f"Using Qiskit Aer Simulator (method={method})")

    # 3. Transpile & Execute
    print("Transpiling...")
    # For simulation of large circuits, we must ensure no coupling map is enforced
    # if the backend reports a default one (which Aer sometimes does based on system limits).
    if mode == 'simulation':
        # For simulation, use minimal transpilation to avoid coupling map restrictions
        # Large circuits (70+ qubits) may exceed simulator's default coupling map
        try:
            t_qc = transpile(qc, backend, optimization_level=0, coupling_map=None)
        except Exception as e:
            # If transpilation fails, try without any optimization
            print(f"Transpilation warning: {e}")
            print("Attempting direct execution without transpilation...")
            t_qc = qc  # Use circuit directly
    else:
        t_qc = transpile(qc, backend, optimization_level=1)
    
    print(f"Executing {shots} shots...")
    job_start = time.time()
    job = backend.run(t_qc, shots=shots)
    result = job.result()
    quantum_runtime = time.time() - job_start
    
    counts = result.get_counts()
    print("Execution complete.")
    
    # 4. Apply H2Q Mitigation
    print("Applying H2Q Thermodynamic Error Mitigation...")
    # Threshold selection: theta_on=0.8 (stable states), theta_off=0.2 (noise floor)
    # These values are empirically validated for quantum advantage benchmarks
    # and can be tuned based on circuit characteristics and hardware noise profiles
    mitigator = H2QMitigator(theta_on=0.8, theta_off=0.2)
    mitigated_probs = mitigator.apply_correction(counts)
    
    # 5. Calculate Observable (e.g., Global Z Expectation <Z...Z>)
    # For the proxy circuit (Hadamards + Rotations), the expected value depends on the structure.
    # We calculate the expectation value from the mitigated distribution.
    
    def calculate_expectation(probs):
        exp_val = 0.0
        for bitstring, prob in probs.items():
            # Parity: Even parity -> +1, Odd parity -> -1
            parity = bitstring.count('1') % 2
            val = 1 if parity == 0 else -1
            exp_val += val * prob
        return exp_val

    observable_val = calculate_expectation(mitigated_probs)
    error_margin, _ = mitigator.calculate_confidence_intervals(mitigated_probs)
    
    classical_runtime = time.time() - start_time - quantum_runtime
    
    # 6. Report Results
    results_data = {
        "observable_estimate": observable_val,
        "error_bound_low": observable_val - error_margin,
        "error_bound_high": observable_val + error_margin,
        "quantum_runtime_sec": quantum_runtime,
        "classical_runtime_sec": classical_runtime,
        "hardware": backend.name,
        "mode": mode,
        "qubits": num_qubits,
        "timestamp": datetime.now().isoformat()
    }
    
    # Save to file
    os.makedirs("results", exist_ok=True)
    with open("results/results.json", "w") as f:
        json.dump(results_data, f, indent=2)
        
    print("\n--- Results ---")
    print(json.dumps(results_data, indent=2))
    print(f"Results saved to results/results.json")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IBM Quantum Advantage Experiment Runner")
    parser.add_argument("--mode", choices=['simulation', 'hardware'], default='simulation', help="Execution mode")
    parser.add_argument("--shots", type=int, default=1024, help="Number of shots")
    parser.add_argument("--backend", type=str, help="Specific IBM Quantum backend name")
    parser.add_argument("--qubits", type=int, default=70, help="Number of qubits")
    
    args = parser.parse_args()
    run_experiment(mode=args.mode, shots=args.shots, backend_name=args.backend, num_qubits=args.qubits)
