import os
import matplotlib.pyplot as plt
import numpy as np
from dotenv import load_dotenv
from qiskit_ibm_runtime import QiskitRuntimeService

# Load Env (Token)
load_dotenv()

JOB_ID = "d4qa8as5fjns73d06teg"

def plot_death_watch():
    print(f">>> RETRIEVING JOB {JOB_ID} FROM IBM QUANTUM...")
    
    # 1. Connect
    try:
        service = QiskitRuntimeService(channel="ibm_quantum_platform")
    except:
        service = QiskitRuntimeService()
        
    # 2. Retrieve Job
    job = service.job(JOB_ID)
    print(f"   [+] Job Status: {job.status()}")
    
    result = job.result()
    # SamplerV2 Access Pattern
    try:
        counts = result[0].data.meas.get_counts()
    except:
        try:
             # Fallback for some versions
             counts = result[0].data.meas
        except:
             print("   [!] Could not parse counts directly. Using mock data for safety if fails.")
             return

    print(f"   [+] Counts Retrieved: {len(counts)} unique strings")

    # 3. Analyze Hamming Weights
    # For a GHZ state |00...0> + |11...1>, valid states are HW=0 and HW=N.
    # Noise creates a distribution between them.
    
    hamming_weights = []
    
    for bitstring, count in counts.items():
        # Qiskit bitstrings are often "00101". Calculate number of '1's
        hw = bitstring.count('1')
        # Add to list 'count' times
        hamming_weights.extend([hw] * count)
        
    hamming_weights = np.array(hamming_weights)
    num_qubits = len(list(counts.keys())[0])
    
    print(f"   [+] Analyzed {len(hamming_weights)} shots. Max HW: {max(hamming_weights)}")

    # 4. Plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Histogram (Twin Peaks)
    ax1.hist(hamming_weights, bins=range(num_qubits+2), color='#6f42c1', alpha=0.7, rwidth=0.8)
    ax1.set_title(f"Thermodynamic Coherence (N={num_qubits} Qubits)")
    ax1.set_xlabel("Hamming Weight (Energy Level)")
    ax1.set_ylabel("Count")
    ax1.axvline(x=0, color='r', linestyle='--', label='|0...0> Ground')
    ax1.axvline(x=num_qubits, color='r', linestyle='--', label='|1...1> Excited')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # CDF (Sigmoid)
    # Sort data
    sorted_hw = np.sort(hamming_weights)
    y_vals = np.arange(len(sorted_hw)) / float(len(sorted_hw) - 1)
    
    ax2.plot(sorted_hw, y_vals, color='#d63384', linewidth=3)
    ax2.set_title("The Death-Watch Sigmoid (Hysteresis Signature)")
    ax2.set_xlabel("Hamming Weight")
    ax2.set_ylabel("Cumulative Probability")
    ax2.grid(True, alpha=0.3)
    
    # Annotate the Sigmoid
    ax2.text(num_qubits*0.2, 0.8, "Bit-Flip Noise\n(Thermal)", fontsize=10, bbox=dict(facecolor='white', alpha=0.8))
    ax2.text(num_qubits*0.8, 0.2, "Bit-Flip Noise\n(Thermal)", fontsize=10, bbox=dict(facecolor='white', alpha=0.8))
    ax2.text(num_qubits*0.5, 0.5, "Coherent\nTransition", ha='center', fontsize=10, fontweight='bold', rotation=45)

    timestamp = "final_26s"
    filename = f"death_watch_sigmoid_{timestamp}.png"
    plt.savefig(filename, dpi=300)
    print(f"   [+] Plot Saved: {os.path.abspath(filename)}")

if __name__ == "__main__":
    plot_death_watch()
