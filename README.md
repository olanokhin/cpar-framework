# CPAR — Cross-Provider Adversarial Review Framework

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Status](https://img.shields.io/badge/Status-Concept%20%2B%20Case%20Study-blue.svg)]()

> *N independent AI reviewers with distinct cognitive profiles, biases, and real-time internet access conduct blind iterative peer review of a document until consensus convergence.*

---

## The Problem with Single-Model Review

Any single AI reviewer has blind spots: training bias, knowledge cutoff, default complimentary tone. The solution is not a better model — it is **adversarial diversity**.

CPAR composes multiple models with different RLHF signals, different training data, and different failure modes into a single review panel. Superpowers emerge from composition, not from any individual model.

---

## Panel Roles

| Role | Model | Observed Superpower | Observed Bias |
|---|---|---|---|
| **Author / Synthesizer** | Claude Sonnet | Long-context coherence, signal filtering | Conservative, low ideation |
| **Research Validator** | Grok | Real-time OSINT, hundreds of sources per iteration | Seeks contradictions with reality |
| **Creative Architect** | Gemini | Elegant structural solutions | Prioritises composition over grounding |
| **Devil's Advocate** | ChatGPT | Adversarial skepticism | Default complimentary — skepticism carries high signal weight precisely because of this |

> Roles and superpowers were **observed empirically** across iterations — not pre-assigned.

---

## Architectural Principles

**1. Blind Review**
Each reviewer maintains independent history. Reviewers never see each other's reviews. Eliminates herding effect and authority bias.

**2. Web-Grounded Validation**
Every reviewer uses real-time web search on every iteration. Produces automatic live literature review as a side effect.

**3. Signal Voting**
```
Majority signal (2/3 same observation)  → apply with confidence
Minority signal (1/3 unique finding)    → do not ignore
                                          especially if source = Grok (OSINT)
```

---

## Algorithm

```
INPUT: initial idea or draft

PHASE 1 — DIVERGE
  Solution space expands aggressively.
  Tables, criteria, references grow rapidly.

  Loop:
    Author generates / updates document
    → All reviewers receive document IN PARALLEL
      + instruction: validate via web search,
        find gaps vs existing literature
    → Author receives N labelled reviews
      + instruction: extract rational signals,
        apply, produce next version

PHASE 2 — CONVERGE
  New findings overlap with existing ones.
  Reviewers begin defending current structure.
  Suggestions become stylistic / tonal.

  Same loop continues until STOP CRITERION:

    ∀ reviewers independently conclude:
    "marginal value of further text improvement
     is less than value of running the experiment"

    NOT → "text is perfect"
    BUT → opportunity cost of polishing > cost of shipping

OUTPUT: fixed document + iteration log
```

Phase boundary is **emergent** — never explicitly set. Arises naturally from panel dynamics, typically around iteration 5–7.

---

## The Critical Property: Temporal Composition

CPAR's power is not parallelism. It is **temporal composition through the document as shared medium**.

```
Gemini alone:            generates elegant idea
                         does NOT know it already exists
                         → false novelty risk

Grok alone:              finds competitors in literature
                         has NO elegant idea to defend
                         → literature survey without contribution

Gemini + Grok via doc:   elegant idea →
                         competitor found →
                         precise gap formulation →
                         defended novelty that existed
                         in neither model alone
```

Reviewers never communicate directly. Superpowers compose **through the document** across iterations — not within a single cycle.

---

## Why It Matters in Production

- **Research teams:** Automates the adversarial review process that normally requires senior researchers from multiple disciplines
- **Cost:** Free tier on all four providers — zero marginal cost per iteration
- **Speed:** 14-iteration review cycle completed in hours, not weeks
- **Output:** Not just a better document — a document with a **defensible novelty gap** verified against live literature

---

## Empirical Case Study

```
Document:    RCI — Recursive Convergent Inference (cs.NE)
Iterations:  14
Panel:       Claude Sonnet + Grok + Gemini + ChatGPT
Tier:        Free on all four providers

Phase 1:     iterations 1–5   rapid expansion
Phase 2:     iterations 6–14  convergence

Stop signal: all reviewers independently concluded
             "run the experiment, text is sufficient"
```

---

## Panel Configuration

| Parameter | Recommendation | Rationale |
|---|---|---|
| Panel size | N = 3 minimum, N = 5 robust | Odd number enables majority signal |
| Provider diversity | One per top-tier lab | Different RLHF, training data, blind spots |
| Knowledge cutoff | Must be current | Stale models miss recent literature |
| Web search | Required for all reviewers | Grounds novelty claims in real literature |

**Excluded models:**
- Qwen — knowledge cutoff stuck at end 2024
- DeepSeek — non-English reasoning chain, not auditable by Author

---

## Citation

```bibtex
@misc{anokhin2026cpar,
  title  = {CPAR: Cross-Provider Adversarial Review Framework},
  author = {Anokhin, Alex},
  year   = {2026},
  note   = {Concept. github.com/olanokhin/cpar-framework}
}
```

---

**Author:** Alex Anokhin · [olanokhin@gmail.com](mailto:olanokhin@gmail.com)  
**Date:** March 2026
