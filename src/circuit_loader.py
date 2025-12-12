import numpy as np
import os
from pathlib import Path
from qiskit import QuantumCircuit
try:
    from qiskit.qasm3 import loads as load_qasm3
    HAS_QASM3 = True
except ImportError:
    HAS_QASM3 = False
try:
    from qiskit.qasm2 import load as load_qasm2
    HAS_QASM2 = True
except ImportError:
    HAS_QASM2 = False

# Circuit file mapping
CIRCUIT_FILES = {
    "70Q": "70Q_OLE_circuit_L_6_b_0.25_delta0.15.qasm",
    "49Q_L6": "49Q_OLE_circuit_L_6_b_0.25_delta0.15.qasm",
    "49Q_L3": "49Q_OLE_circuit_L_3_b_0.25_delta0.15.qasm",
    # Falsification benchmarks with strong simulator ground truth
    "REP3": "H2QEC_REPETITION_CODE_3q.qasm",
    "REP5": "H2QEC_REPETITION_CODE_5q.qasm",
}

def load_benchmark_circuit(circuit_key="70Q", circuits_dir="circuits", num_qubits=None, depth=None):
    """
    Loads the official 'operator_loschmidt_echo' benchmark circuit from Quantum Advantage Tracker.
    
    Args:
        circuit_key (str): Circuit identifier - "70Q", "49Q_L6", or "49Q_L3" (default: "70Q")
        circuits_dir (str): Directory containing circuit files (default: "circuits")
        num_qubits (int): Deprecated - use circuit_key instead
        depth (int): Deprecated - use circuit_key instead
        
    Returns:
        QuantumCircuit: The loaded benchmark circuit.
    """
    # Map legacy parameters to circuit_key
    if num_qubits is not None:
        if num_qubits == 70:
            circuit_key = "70Q"
        elif num_qubits == 49:
            circuit_key = "49Q_L6"  # Default to L6 for 49 qubits
        else:
            # Fall back to proxy for other sizes
            return _load_proxy_circuit(num_qubits, depth)
    
    # Try to load actual circuit file
    filename = CIRCUIT_FILES.get(circuit_key)
    if filename:
        filepath = Path(circuits_dir) / filename
        if filepath.exists():
            print(f"Loading actual benchmark circuit: {filename}")
            try:
                # Read file content
                with open(filepath, 'r') as f:
                    qasm_content = f.read()
                
                # Try QASM 3.0 first (newer format)
                if HAS_QASM3:
                    try:
                        circuit = load_qasm3(qasm_content)
                        print(f"  Qubits: {circuit.num_qubits}")
                        print(f"  Depth: {circuit.depth()}")
                        print(f"  Gates: {len(circuit.data)}")
                        return circuit
                    except:
                        pass
                
                # Fall back to QASM 2.0
                if HAS_QASM2:
                    try:
                        circuit = load_qasm2(str(filepath))
                        print(f"  Qubits: {circuit.num_qubits}")
                        print(f"  Depth: {circuit.depth()}")
                        print(f"  Gates: {len(circuit.data)}")
                        return circuit
                    except:
                        pass
                
                raise Exception("Could not parse QASM file (tried both 2.0 and 3.0)")
            except Exception as e:
                print(f"  Warning: Failed to load circuit file: {e}")
                print(f"  Falling back to proxy circuit...")
        else:
            print(f"Warning: Circuit file not found: {filepath}")
            print(f"  Run 'python download_circuits.py' to download circuits")
            print(f"  Falling back to proxy circuit...")
    
    # Fallback to proxy circuit
    if num_qubits is None:
        num_qubits = 70 if circuit_key == "70Q" else 49
    return _load_proxy_circuit(num_qubits, depth)

def _load_proxy_circuit(num_qubits=70, depth=1872):
    """
    Generate a proxy circuit for testing when actual circuit file is not available.
    
    Args:
        num_qubits (int): Number of qubits (default 70).
        depth (int): Depth of the circuit (default 1872).
        
    Returns:
        QuantumCircuit: The constructed proxy circuit.
    """
    qc = QuantumCircuit(num_qubits)
    
    # Add a layer of Hadamards to create superposition
    qc.h(range(num_qubits))
    
    # Simplified pattern to mimic benchmark structure
    for i in range(0, num_qubits - 1, 2):
        qc.cx(i, i+1)
        
    for i in range(num_qubits):
        qc.rz(np.pi/4, i)
        qc.rx(np.pi/4, i)
        
    # Add a final measurement layer
    qc.measure_all()
    
    qc.name = f"operator_loschmidt_echo_{num_qubits}x{depth}_proxy"
    return qc

if __name__ == "__main__":
    qc = load_benchmark_circuit()
    print(f"Generated circuit: {qc.name}")
    print(f"Width: {qc.num_qubits}")
    # print(f"Depth: {qc.depth()}") # Might be small in this proxy
