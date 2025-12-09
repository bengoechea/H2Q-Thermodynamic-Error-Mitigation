# Competitive Analysis: Quick Start Guide

## Current Location
You are in: `/Users/kenbengoetxea/container-projects/apps/claude_desktop/QEC-IBM-Quantum-Advantage`

## What You Can Run From Here (Root Directory)

### ✅ Option 1: Run from Root (No Switch Needed)

**Quick Comparison:**
```bash
python3 competitive_analysis/quick_compare.py
```
Shows immediate IBM 156Q comparison.

**Full Analysis:**
```bash
python3 competitive_analysis/competitive_analysis.py
```
Generates full report comparing against all competitors.

**Package Import (Python):**
```python
from competitive_analysis import CompetitiveAnalyzer
analyzer = CompetitiveAnalyzer()
analyzer.generate_report()
```

### ✅ Option 2: Switch to Package Directory

**When to switch:**
- You want to work inside the package directory
- You want to see generated files in the same location
- You're doing development on the package itself

**Switch command:**
```bash
cd competitive_analysis
```

**Then run:**
```bash
python3 quick_compare.py          # Quick comparison
python3 competitive_analysis.py   # Full analysis
```

## Quick Reference

| Task | Command (from root) | Command (from competitive_analysis/) |
|------|---------------------|-------------------------------------|
| Quick comparison | `python3 competitive_analysis/quick_compare.py` | `python3 quick_compare.py` |
| Full analysis | `python3 competitive_analysis/competitive_analysis.py` | `python3 competitive_analysis.py` |
| Package import | `from competitive_analysis import CompetitiveAnalyzer` | `from competitive_analysis import CompetitiveAnalyzer` |

## Generated Files Location

**From root directory:**
- Reports saved to: `competitive_analysis/competitive_analysis_report.txt`
- JSON saved to: `competitive_analysis/competitive_analysis_data.json`

**From competitive_analysis/ directory:**
- Reports saved to: `competitive_analysis_report.txt` (current directory)
- JSON saved to: `competitive_analysis_data.json` (current directory)

## Recommendation

**Stay in root directory** if you:
- Just want to run the analysis
- Want to keep generated files organized in the package directory
- Are using it as part of a larger workflow

**Switch to competitive_analysis/** if you:
- Are developing or modifying the package
- Want generated files in your current working directory
- Prefer shorter command paths

## Examples

### Example 1: Quick Check (Stay in Root)
```bash
# You're here: QEC-IBM-Quantum-Advantage/
python3 competitive_analysis/quick_compare.py
```

### Example 2: Full Analysis (Stay in Root)
```bash
# You're here: QEC-IBM-Quantum-Advantage/
python3 competitive_analysis/competitive_analysis.py
# Report saved to: competitive_analysis/competitive_analysis_report.txt
```

### Example 3: Work in Package (Switch)
```bash
# You're here: QEC-IBM-Quantum-Advantage/
cd competitive_analysis
# Now you're here: QEC-IBM-Quantum-Advantage/competitive_analysis/
python3 quick_compare.py
python3 competitive_analysis.py
# Reports saved to current directory
```

## Package Usage (Python Script)

```python
# From anywhere in the repo
from competitive_analysis import CompetitiveAnalyzer, SystemMetrics

# Create analyzer
analyzer = CompetitiveAnalyzer()

# Generate report (saves to current directory or specified path)
analyzer.generate_report("my_report.txt")

# Export JSON
analyzer.export_json("my_data.json")

# Custom competitor analysis
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
print(f"Effective Circuit Depth: {value_add.effective_circuit_depth:.2f}x")
```

## Summary

**You can run everything from the root directory** - no need to switch unless you prefer working inside the package directory. Both approaches work identically!

