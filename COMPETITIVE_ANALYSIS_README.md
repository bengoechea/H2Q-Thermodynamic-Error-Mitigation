# Competitive Analysis: H2QEC + Control-Layer Augmentation

Quick tools to analyze the value-add of your 5-tuple hysteresis error correction with a patent-pending control-layer augmentation compared to competitors (IBM 156-qubit, Google, etc.).

**Task Class:** Surface-code style QEC for sampling, variational algorithms (VQE), and expectation-value estimation workloads.

**Benchmark Framework:** Aligned with IBM Quantum Optimization Benchmarking Library (QOBLIB) evaluation methodology.

**Hardware Agnostic:** Model- and hardware-agnostic control logic applicable to superconducting and trapped-ion systems.

## Quick Start

### Fast Comparison (IBM 156Q)
```bash
python3 quick_compare.py
```

Shows immediate comparison against IBM 156-qubit system for:
- X gate fidelity
- T2 coherence
- Logical error rates
- False positive rates

### Full Analysis
```bash
python3 competitive_analysis.py
```

Generates comprehensive report comparing against:
- IBM 156Q Standard
- IBM 156Q Advanced
- Google Willow
- IonQ Trapped Ion

Outputs:
- `competitive_analysis_report.txt` - Detailed text report
- `competitive_analysis_data.json` - Machine-readable data

## Key Metrics Analyzed

### 1. **X Gate Fidelity (1Q)**
- Measures single-qubit gate performance
- H2QEC + control augmentation: 0.9995 (vs IBM 0.9990)
- **Improvement: +0.05%** (control-layer timing augmentation; details withheld in public repo)
- **Source:** internal hardware timing experiment (job IDs available upon request)

### 2. **T2 Coherence**
- Quantum memory lifetime
- H2QEC + control augmentation: 150 μs (vs IBM 100 μs)
- **Improvement: +50%** (combined effect)
- **Source:** internal hardware timing experiment (details withheld in public repo)

### 3. **False Positive Reduction**
- Syndrome detection accuracy
- H2QEC: 0.45% (vs IBM 2.23%)
- **Reduction: 79.8%** (hysteresis filtering)
- **Source:** H2QEC validation (ibm_fez, job d4lutmiv0j9c73e5nvt0)

### 4. **Logical Error Rate**
- Overall system reliability
- H2QEC: 2.37% (vs IBM 4.0%)
- **Reduction: 40.8%** (5-tuple + Alpha)
- **Source:** H2QEC validation (ibm_fez, job d4lutmiv0j9c73e5nvt0)

### 5. **Effective Circuit Depth** (Utility-Scale Metric)
- How many times deeper circuits can run at same error budget
- H2QEC: ~1.33x deeper vs IBM standard
- **Meaning:** Enables progress toward utility-scale, fault-tolerant advantage

## Value-Add Summary

### vs IBM 156-Qubit Standard:
- **79.8%** fewer false positives
- **40.8%** lower logical errors
- **50%** longer T2 coherence
- **+0.05%** better X gate fidelity
- **+63.6 effective qubits** (from error reduction)
- **~1.33x effective circuit depth** (can run deeper circuits at same error budget)

### Key Differentiators:
1. **5-Tuple Hysteresis**: Prevents measurement-induced oscillations
2. **Control-Layer Augmentation**: Physics-informed timing family (details withheld in public repo)
3. **Dual-Layer Suppression**: Physical control + hysteresis logic = stability stack
4. **Hardware-Agnostic**: Applicable to superconducting, trapped-ion, and other platforms
5. **QOBLIB-Aligned**: Metrics align with IBM's benchmarking framework for practical advantage

## Parameter Sources & Citations

All competitor metrics include inline citations with public links for independent verification:

- **IBM 156Q Standard**: [IBM Quantum roadmap 2025](https://www.ibm.com/quantum/roadmap), typical Eagle/Heron processor specs
- **IBM 156Q Advanced**: [IBM Quantum roadmap 2025](https://www.ibm.com/quantum/roadmap) improvements, temporal averaging methods
- **Google Willow**: Google Willow spec sheet (Dec 2024), [Nature publication (2024)](https://www.nature.com/articles/s41586-023-07107-9) - "Suppressing quantum errors by scaling a surface code logical qubit"
- **IonQ**: [IonQ Aria system specs](https://ionq.com/systems/aria), IonQ public specifications 2024-2025

H2QEC metrics sourced from hardware validation:
- `Validation/H2QEC_Hardware_Validation_Summary.md`
- `H2-Supremacy/COMPUTE_STORIES.md`
- Job IDs: available upon request

## Custom Analysis

To analyze against custom competitor metrics:

```python
from competitive_analysis import CompetitiveAnalyzer, SystemMetrics

# Define custom competitor
competitor = SystemMetrics(
    name="Custom System",
    qubit_count=156,
    gate_fidelity_1q=0.9992,
    gate_fidelity_2q=0.992,
    coherence_t1=180.0,
    coherence_t2=120.0,
    logical_error_rate=0.035,
    false_positive_rate=0.015,
    error_correction_method="Custom method"
)

# Analyze
analyzer = CompetitiveAnalyzer()
value_add = analyzer.calculate_value_add(competitor)
print(f"Value Score: {value_add.overall_value_score:.1f}/100")
```

## Understanding the Metrics

### Overall Value Score (0-100)
Weighted composite of:
- **30%** Fidelity improvements (1Q + 2Q)
- **20%** Coherence improvements (T1 + T2)
- **30%** Logical error reduction
- **20%** False positive reduction

### Effective Qubit Gain
Calculated as: `(error_reduction / 100) × competitor_qubit_count`
- Lower error rate = more usable qubits
- Example: 40.8% error reduction on 156 qubits = +63.6 effective qubits

### Compute Time Savings
From reduced:
- False positive corrections (30% weight)
- Logical error retries (20% weight)

## Files

- `competitive_analysis.py` - Full analysis framework
- `quick_compare.py` - Fast IBM 156Q comparison
- `competitive_analysis_report.txt` - Generated detailed report
- `competitive_analysis_data.json` - JSON export for further analysis

## QOBLIB Alignment

This analysis aligns with IBM's Quantum Optimization Benchmarking Library (QOBLIB) framework:

- **Benchmark Problems**: Surface-code style QEC for sampling, VQE, and expectation-value estimation
- **Evaluation Metrics**: Logical error rate and runtime vs. default settings
- **Practical Advantage**: Assesses progress toward utility-scale, fault-tolerant quantum computing
- **Task Classes**: Explicitly labeled for sampling, variational algorithms, and expectation-value estimation

### QOBLIB Metric Mapping

**Note:** This analysis uses **QOBLIB-style metrics** for QEC workloads rather than direct QOBLIB problem instances. The metrics map to QOBLIB's expected reporting fields as follows:

| QOBLIB Field | H2QEC Metric | Mapping |
|--------------|--------------|---------|
| **Solution Quality** | Logical Error Rate | Lower logical error rate = higher solution quality. H2QEC achieves 2.37% vs 4.0% baseline (40.8% improvement) |
| **Wall-Clock Time** | Compute Time Savings | Reduced false positives and errors translate to 32% compute time savings (fewer correction cycles and retries) |
| **Resource Counts** | Effective Qubit Gain | Error reduction enables +63.6 effective qubits (more usable qubits from same physical hardware) |

**QEC-Specific Extensions:**
- **False Positive Rate**: Maps to solution quality (fewer unnecessary corrections = better quality)
- **Effective Circuit Depth**: Maps to resource efficiency (deeper circuits at same error budget)
- **Coherence Times**: Maps to resource utilization (longer coherence = more computation time available)

This framework can be extended to use direct QOBLIB problem instances when evaluating specific optimization problems (e.g., MaxCut, portfolio optimization) with H2QEC error correction applied.

## Hardware-Agnostic Design

H2QEC + control-layer augmentation is **model- and hardware-agnostic** control logic that can sit on top of:

- **Superconducting systems**: IBM (Eagle/Heron), Google (Willow)
- **Trapped-ion systems**: IonQ, Quantinuum
- **Any quantum platform**: Requires error correction

This cross-cutting approach aligns with how roadmaps discuss error-correction improvements that work across platforms.

## Utility-Scale Metrics

The analysis translates improvements into IBM's preferred language:

- **Effective Circuit Depth**: How many times deeper circuits can run at same error budget
- **Effective Qubit Count**: Additional usable qubits from error reduction
- **Fault-Tolerant Advantage**: Progress toward utility-scale quantum computing
- **Practical Quantum Advantage**: Assessment for defined problem sets (QOBLIB framework)

## Notes

- Baseline metrics from hardware validation on `ibm_fez` and `ibm_torino`
- H2QEC false positive reduction: 79.7% (validated)
- Additional timing/control-layer experiment results: available upon request
- All metrics based on real hardware results
- All parameter sources cited inline in code comments
- Analysis framework ready for integration with QOBLIB benchmark problems

