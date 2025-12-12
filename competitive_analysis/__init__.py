"""
Competitive Analysis: H2QEC + Control-Layer Augmentation vs. State-of-the-Art

Analyzes value-add of 5-tuple hysteresis error correction with a control-layer augmentation
compared to competitors (IBM 156-qubit, Google, etc.) on fidelity and coherence metrics.

Task Class: Surface-code style QEC for sampling, variational algorithms (VQE),
and expectation-value estimation workloads.

Benchmark Framework: Aligned with IBM Quantum Optimization Benchmarking Library (QOBLIB)
evaluation methodology for practical quantum advantage assessment.
"""

from .competitive_analysis import CompetitiveAnalyzer, SystemMetrics, ValueAddMetrics

__all__ = ['CompetitiveAnalyzer', 'SystemMetrics', 'ValueAddMetrics']
__version__ = '1.0.0'

