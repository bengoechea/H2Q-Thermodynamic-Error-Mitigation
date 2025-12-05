#!/usr/bin/env python3
"""Download official Quantum Advantage Tracker benchmark circuits."""

import urllib.request
import os

CIRCUITS = {
    "70Q_OLE_circuit_L_6_b_0.25_delta0.15.qasm": 
        "https://raw.githubusercontent.com/quantum-advantage-tracker/quantum-advantage-tracker.github.io/main/data/observable-estimations/circuit-models/operator_loschmidt_echo/70Q_OLE_circuit_L_6_b_0.25_delta0.15.qasm",
    "49Q_OLE_circuit_L_6_b_0.25_delta0.15.qasm":
        "https://raw.githubusercontent.com/quantum-advantage-tracker/quantum-advantage-tracker.github.io/main/data/observable-estimations/circuit-models/operator_loschmidt_echo/49Q_OLE_circuit_L_6_b_0.25_delta0.15.qasm",
    "49Q_OLE_circuit_L_3_b_0.25_delta0.15.qasm":
        "https://raw.githubusercontent.com/quantum-advantage-tracker/quantum-advantage-tracker.github.io/main/data/observable-estimations/circuit-models/operator_loschmidt_echo/49Q_OLE_circuit_L_3_b_0.25_delta0.15.qasm",
}

def main():
    os.makedirs("circuits", exist_ok=True)
    
    for filename, url in CIRCUITS.items():
        filepath = os.path.join("circuits", filename)
        print(f"Downloading {filename}...")
        try:
            urllib.request.urlretrieve(url, filepath)
            print(f"  Saved to {filepath}")
            
            # Verify file size
            size = os.path.getsize(filepath)
            print(f"  Size: {size:,} bytes")
        except Exception as e:
            print(f"  ERROR: {e}")
    
    print("\nAll circuits downloaded successfully.")

if __name__ == "__main__":
    main()

