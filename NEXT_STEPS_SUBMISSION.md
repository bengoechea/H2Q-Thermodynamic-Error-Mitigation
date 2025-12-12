# Next Steps: IBM Quantum Advantage Tracker Submission

**Date:** December 10, 2025  
**Status:** ✅ Ready to Submit  
**Pathway:** Observable Estimations

---

## 🎯 Quick Summary

You have **TWO submission options**:

1. **Observable Estimations** (Ready Now) - Submit your Loschmidt echo results
2. **Classically Verifiable Problems** (Optional) - Submit circuit models via PR

**Recommended:** Start with **Option 1** (Observable Estimations) since you have complete results.

---

## 📋 OPTION 1: Observable Estimations Submission (RECOMMENDED)

### Step 1: Navigate to Submission Page

1. Go to: https://quantum-advantage-tracker.github.io/trackers/observable-estimations
2. Click **"Open submission ticket"** link
3. This will take you to the GitHub issue form

### Step 2: Fill Out GitHub Issue Form

**Required Fields:**

#### **Authors:**
```
Kenneth A Mendoza
```

#### **Institutions:**
```
Independent Research
```

#### **Method Proof:**

**Patent Reference:**
- US Provisional Application 63/927,371 (filed November 29, 2025)
- US Provisional Application 63/933,465 (filed December 8, 2025)
- Patent details: https://kenmendoza.com/patents

**Implementation Repository:**
- https://github.com/bengoechea/H2Q-Thermodynamic-Error-Mitigation

**Method Explanation:**
H²Q thermodynamic error mitigation treating syndromes as thermal fluctuations with domain-calibrated hysteresis-based filtering. H²Q applies dual-threshold hysteresis gates with dwell-time enforcement to achieve 79.7% false positive reduction in quantum error correction.

**Key Features:**
- Domain-calibrated asymmetry ratio (κ\_QEC) for measurement-disturbance-dominated regimes
- Dwell-time enforcement: τ (configurable; measured in rounds/cycles)
- Asymmetric thresholds: θ\_up = κ·θ\_base, θ\_down = θ\_base/κ

**Validation Results:**
- False Positive Reduction: 79.7% (validated on `ibm_fez`, `ibm_torino`)
- Statistical Significance: Cohen's d = 10.59, p < 0.0001
- Hardware Validated: IBM `ibm_fez` (156-qubit), `ibm_torino` (133-qubit Heron r2)

#### **Circuit Selection:**

Select from dropdown (if available):
- `operator_loschmidt_echo_70x1872`

OR manually specify:
- Circuit: `operator_loschmidt_echo_70x1872`
- Observable: Z_52 Z_59 Z_72

#### **Result / Notes Field:**

**Copy this entire text from:** `QUANTUM_ADVANTAGE_TRACKER_SUBMISSION_TEXT.md`

```
For operator_loschmidt_echo_70x1872, H²Q thermodynamic error mitigation on IBM Quantum reports ⟨O⟩ = 0.0004 ± 0.016 based on 10 hardware runs (6 runs at 1024 shots, 3 runs at 4096 shots, 1 run at 8192 shots) on backend ibm_fez. Total compute time: < 10 minutes (within IBM Quantum free access window). Job IDs: d4ps8frher1c73bakq70, d4ps8hnt3pms7396j020, d4ps8j7t3pms7396j040, d4ps8kk5fjns73cvoomg, d4ps8m3her1c73bakqdg, d4pthtsfitbs739gdd00, d4puf9ft3pms7396l61g, d4puo87t3pms7396lef0, d4puo9nt3pms7396leh0, d4puobkfitbs739geheg. Recomputable artifacts and run provenance are provided in HARDWARE_VALIDATION.md and the results/ directory.

**Interpretation and Caveats:** The reported observable value ⟨O⟩ = 0.0004 ± 0.016 is consistent with zero within uncertainty. Analysis of all 10 runs reveals uniform (maximally mixed) bitstring distributions across all shot counts (1024-8192), which may indicate: (1) the circuit operates in a high-noise regime where noise dominates signal, (2) insufficient shot counts to resolve structure above noise, or (3) the Loschmidt echo circuit naturally measures quantum coherence rather than state populations. This submission demonstrates H²Q thermodynamic error mitigation methodology on real hardware with rigorous statistical validation (10 independent runs, shot-weighted aggregation, 95% confidence intervals). However, the uniform distribution suggests this validates H²Q's conservative filtering approach (preserving all states when signal structure is unclear) more than it demonstrates quantum advantage over classical methods for this specific circuit instance. Future work with higher shot counts, different circuit types producing structured outputs (e.g., VQE), or baseline comparisons (ZNE, CDR) would strengthen quantum advantage claims.
```

### Step 3: Submit the Issue

1. Review all fields
2. Click **"Submit new issue"**
3. **Do NOT assign labels** - maintainers will handle that

### Step 4: Track Your Submission

Monitor status at: https://quantum-advantage-tracker.github.io/trackers/observable-estimations

**Status Tags:**
- **Backlog** - Awaiting review
- **In review** - Reviewer assigned
- **Incomplete** - Missing details (respond if this happens)
- **Verified** - ✅ Approved and added to tracker
- **Closed** - Technical issues (rare)

---

## 📋 OPTION 2: Classically Verifiable Problems (Optional)

If you want to also submit your circuit models:

### Step 1: Fork and Clone Tracker Repository

```bash
# Fork the repository on GitHub first, then:
git clone https://github.com/YOUR_USERNAME/quantum-advantage-tracker.git
cd quantum-advantage-tracker
```

### Step 2: Create Branch

```bash
git checkout -b add-h2qec-circuits
```

### Step 3: Copy Circuit Files

Use the circuit files in this repository under `circuits/` and follow the Quantum Advantage Tracker repository’s contribution instructions. Avoid hardcoding local absolute paths in public documentation.

### Step 4: Update circuit-models.json

Edit `data/classically-verifiable-problems/circuit-models.json` and add:

```json
{
  "h2qec": {
    "instances": [
      {
        "id": "h2qec_surface_code_5x5",
        "path": "H2QEC_SURFACE_CODE_5x5.qasm",
        "qubits": 49,
        "gates": 163
      },
      {
        "id": "h2qec_repetition_3q",
        "path": "H2QEC_REPETITION_CODE_3q.qasm",
        "qubits": 4,
        "gates": 13
      },
      {
        "id": "h2qec_repetition_5q",
        "path": "H2QEC_REPETITION_CODE_5q.qasm",
        "qubits": 6,
        "gates": 23
      }
    ]
  }
}
```

### Step 5: Commit and Push

```bash
git add data/classically-verifiable-problems/circuit-models/h2qec/
git add data/classically-verifiable-problems/circuit-models.json
git commit -m "Add H²QEC circuit models

- Surface Code 5×5 (49 qubits, 163 gates)
- Repetition Code 3q (4 qubits, 13 gates)
- Repetition Code 5q (6 qubits, 23 gates)
- 79.7% false positive reduction validated on IBM hardware
- Patent: US App 63/927,371"
git push origin add-h2qec-circuits
```

### Step 6: Create Pull Request

1. Go to your fork on GitHub
2. Click "New Pull Request"
3. Use PR description from: `circuits/SUBMISSION_FILES/PR_DESCRIPTION.md`

---

## ✅ Pre-Submission Checklist

### For Observable Estimations:
- [x] All Job IDs documented (10 runs)
- [x] Statistical model documented
- [x] Error bars calculated (95% CI)
- [x] Repository is public and ready
- [x] Submission text prepared
- [x] Caveats included (Feynman principles)
- [ ] **Submit GitHub issue** ← **NEXT STEP**

### For Classically Verifiable Problems (Optional):
- [x] Circuit files ready (.qasm)
- [x] README prepared
- [x] JSON entry prepared
- [x] PR description ready
- [ ] Fork tracker repository
- [ ] Create PR

---

## 📝 Key Files Reference

**For Observable Estimations:**
- Submission text: `QUANTUM_ADVANTAGE_TRACKER_SUBMISSION_TEXT.md`
- Issue template: `circuits/SUBMISSION_FILES/GITHUB_ISSUE_TEMPLATE.md`

**For Classically Verifiable Problems:**
- Complete guide: `circuits/SUBMISSION_FILES/COMPLETE_SUBMISSION_GUIDE.md`
- Git commands: `circuits/SUBMISSION_FILES/git-commands.sh`
- PR description: `circuits/SUBMISSION_FILES/PR_DESCRIPTION.md`

---

## 🚀 IMMEDIATE ACTION

**Right Now:**
1. Go to: https://quantum-advantage-tracker.github.io/trackers/observable-estimations
2. Click "Open submission ticket"
3. Fill out the form using text from `QUANTUM_ADVANTAGE_TRACKER_SUBMISSION_TEXT.md`
4. Submit!

**Estimated Time:** 10-15 minutes

---

## 📞 After Submission

1. **Monitor the issue** - Check for reviewer questions
2. **Respond promptly** - If marked "Incomplete", provide requested details
3. **Celebrate** - You've submitted to the IBM Quantum Advantage Tracker! 🎉

---

**Status:** ✅ **READY TO SUBMIT NOW**

All materials prepared. Just need to fill out the GitHub issue form!
