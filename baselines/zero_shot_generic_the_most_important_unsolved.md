# Zero-Shot Baseline — generic

**Model:** claude-sonnet-4-6  
**Variant:** generic  
**Date:** 2026-03-30  
**Input:** The most important unsolved problem in LLM alignment is not values but epistemics — models that confidently don't know what they don't know

---

## Analysis of the Claim

### What the Claim Is Trying to Say

The author argues that **calibration and epistemic humility** — models being uncertain when they should be uncertain — matter more to alignment than getting values right.

---

### Problems With the Original Claim

**Logical/Structural Issues**
- "Confidently don't know what they don't know" is **self-contradictory as written** — it conflates *overconfidence* with *unknown unknowns*, which are related but distinct problems
- The framing as a binary (values *vs.* epistemics) is a **false dichotomy** — miscalibrated epistemics *are* a values problem if you consider honesty a value
- "Most important" is asserted without argumentation

**Conceptual Imprecision**
- Conflates several distinct problems:
  - **Calibration** (confidence ≠ accuracy)
  - **Unknown unknowns** (Rumsfeld problem)
  - **Sycophancy** (updating based on social pressure rather than evidence)
  - **Hallucination** (generating false information fluently)
- "Epistemics" is doing enormous undifferentiated work

**What's Actually Right About It**
- There is a genuine, underappreciated insight here: a model with *perfect values but broken epistemics* could cause serious harm through confident wrong beliefs
- Epistemic failures are arguably **harder to detect** than value failures, making them more dangerous
- Current alignment work *is* disproportionately focused on value specification

---

## Improved Version

> **A critically underaddressed problem in LLM alignment is epistemic miscalibration: models that express high confidence in claims they cannot reliably verify, fail to flag the boundaries of their competence, and resist updating when presented with contradicting evidence. Even a model with well-specified values will cause harm if it acts on false beliefs it holds with unwarranted certainty. Values tell a model what to optimize for; epistemics determine whether its model of the world is trustworthy enough to optimize toward anything at all. Alignment research that neglects calibration, honest uncertainty expression, and resistance to sycophancy may be solving the wrong layer of the problem.**

---

### What the Improved Version Does Differently

| Dimension | Original | Improved |
|---|---|---|
| Core concept | Vague ("epistemics") | Specific (calibration, uncertainty expression, sycophancy resistance) |
| Logical structure | Self-contradictory phrasing | Internally consistent |
| Values/epistemics relationship | False dichotomy | Layered dependency explained |
| Claim strength | Overclaims "most important" | Claims "critically underaddressed" — defensible |
| Mechanism | Implicit | Explicit: bad epistemics undermine good values |

---

### Remaining Open Questions the Claim Should Acknowledge

1. **Is this actually solvable separately from values?** — Epistemic honesty *is* a value
2. **Does the priority claim hold empirically?** — Value misalignment (e.g., deception, manipulation) may pose larger near-term risks
3. **Whose epistemics are the reference point?** — Calibrated relative to what ground truth?

The core insight is **valuable and underappreciated** — the execution needed significant tightening.