# Competitive Analysis: H2QEC + Control-Layer Augmentation

Quick tools to analyze the value-add of your 5-tuple hysteresis error correction with a patent-covered control-layer augmentation (implementation details withheld in the public repo) compared to competitors (IBM 156-qubit, Google, etc.).

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
- `competitive_analysis_report.txt` - Detailed text report (gitignored)
- `competitive_analysis_data.json` - Machine-readable data (gitignored)

## Installation

No external dependencies required. Uses Python 3.x standard library only:
- `json`
- `dataclasses`
- `datetime`
- `typing`

## Usage as Package

```python
from competitive_analysis import CompetitiveAnalyzer, SystemMetrics

# Create analyzer
analyzer = CompetitiveAnalyzer()

# Generate report
report = analyzer.generate_report("my_report.txt")

# Export JSON
analyzer.export_json("my_data.json")

# Custom competitor
competitor = SystemMetrics(
    name="Custom System",
    qubit_count=156,
    gate_fidelity_1q=0.9992,
    gate_fidelity_2q=0.992,
    coherence_t1=180.0,
    coherence_t2=120.0,
    logical_error_rate=0.035,
    false_positive_rate=0.015,
    error_correction_method="Custom method",
    parameter_source="Public source URL"
)

value_add = analyzer.calculate_value_add(competitor)
print(f"Value Score: {value_add.overall_value_score:.1f}/100")
```

## Key Metrics

See full documentation in parent directory: `../COMPETITIVE_ANALYSIS_README.md`

## Files

- `competitive_analysis.py` - Main analysis framework
- `quick_compare.py` - Fast comparison tool
- `__init__.py` - Package initialization

## Notes

- All generated files (`*_report.txt`, `*_data.json`) should be gitignored
- Parameter sources include public links for independent verification
- Analysis is hardware-agnostic and ready for cross-platform use

