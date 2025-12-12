# Quantum Advantage Tracker Submission Text

## Observable Estimations Ticket - Result/Notes Field

Copy and paste this text into the "Result / Notes" box when submitting to the Quantum Advantage Tracker:

---

For operator_loschmidt_echo_70x1872, H²Q thermodynamic error mitigation on IBM Quantum reports ⟨O⟩ = 0.0004 ± 0.016 based on 10 hardware runs (6 runs at 1024 shots, 3 runs at 4096 shots, 1 run at 8192 shots) on backend ibm_fez. Total compute time: < 10 minutes (within IBM Quantum free access window). Job IDs: d4ps8frher1c73bakq70, d4ps8hnt3pms7396j020, d4ps8j7t3pms7396j040, d4ps8kk5fjns73cvoomg, d4ps8m3her1c73bakqdg, d4pthtsfitbs739gdd00, d4puf9ft3pms7396l61g, d4puo87t3pms7396lef0, d4puo9nt3pms7396leh0, d4puobkfitbs739geheg. Recomputable artifacts and run provenance are provided in HARDWARE_VALIDATION.md and the results/ directory.

**Interpretation and Caveats:** The reported observable value ⟨O⟩ = 0.0004 ± 0.016 is consistent with zero within uncertainty. Analysis of all 10 runs reveals uniform (maximally mixed) bitstring distributions across all shot counts (1024-8192), which may indicate: (1) the circuit operates in a high-noise regime where noise dominates signal, (2) insufficient shot counts to resolve structure above noise, or (3) the Loschmidt echo circuit naturally measures quantum coherence rather than state populations. This submission demonstrates H²Q thermodynamic error mitigation methodology on real hardware with rigorous statistical validation (10 independent runs, shot-weighted aggregation, 95% confidence intervals). However, the uniform distribution suggests this validates H²Q's conservative filtering approach (preserving all states when signal structure is unclear) more than it demonstrates quantum advantage over classical methods for this specific circuit instance. Future work with higher shot counts, different circuit types producing structured outputs (e.g., VQE), or baseline comparisons (ZNE, CDR) would strengthen quantum advantage claims.

---

**Values used:**
- `X` = 0.0004 (H²Q‑mitigated expectation value from comprehensive validation report)
- `δX` = 0.016 (95% confidence interval half-width combining statistical uncertainty and systematic bias bound)
- `N` = 10 (total independent hardware runs)
- `M` = 1024-8192 (mixed shot counts: 6 runs at 1024, 3 at 4096, 1 at 8192)
- `B` = ibm_fez (156-qubit backend)
- **Total Compute Time:** < 10 minutes (within IBM Quantum free access window)
- **Job IDs:** d4ps8frher1c73bakq70, d4ps8hnt3pms7396j020, d4ps8j7t3pms7396j040, d4ps8kk5fjns73cvoomg, d4ps8m3her1c73bakqdg, d4pthtsfitbs739gdd00, d4puf9ft3pms7396l61g, d4puo87t3pms7396lef0, d4puo9nt3pms7396leh0, d4puobkfitbs739geheg

**Source:** `results/comprehensive_validation_report.json` - All 10 runs aggregated with observable Z_52 Z_59 Z_72
