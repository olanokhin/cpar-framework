# CPAR — Cross-Provider Adversarial Review Framework

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Status](https://img.shields.io/badge/Status-Working%20System%20%2B%20Case%20Studies-green.svg)]()
[![HF Space](https://img.shields.io/badge/Demo-HuggingFace%20Spaces-yellow.svg)]()

> *N independent AI reviewers from different providers conduct blind iterative peer review of a document until consensus convergence — composing their distinct capabilities through the document as shared medium.*

---

## The Problem

Any single AI reviewer has systematic blind spots: training bias, knowledge cutoff, default complimentary tone. A single model cannot reliably catch its own failure modes.

The solution is not a better model. It is **adversarial diversity across providers**.

CPAR composes models from different labs with different RLHF objectives, different training corpora, and different failure modes into a **cross-provider adversarial panel**. This mitigates herding bias — the tendency of models to converge on the same errors — by enforcing reviewer blindness and grounding every iteration in real-time web search.

---

## Panel Roles

| Role | Model | Observed Tendency | Observed Bias |
|---|---|---|---|
| **Author / Synthesizer** | Claude Sonnet | Long-context coherence, signal filtering | Conservative, low ideation |
| **Research Validator** | Grok | Real-time OSINT, web + X search per iteration | Seeks contradictions with reality |
| **Creative Architect** | Gemini | Elegant structural solutions | Prioritises composition over grounding |
| **Devil's Advocate** | ChatGPT | Adversarial skepticism | Default complimentary — skepticism carries high signal weight precisely because of this |

> Tendencies were **observed empirically** across iterations of case studies — not pre-assigned. They are versioned observations, not stable model properties. Verify against your panel configuration.

---

## Architectural Principles

**1. Blind Review**
Each reviewer maintains independent conversation history. Reviewers never see each other's reviews. This mitigates herding bias and authority effects.

**2. Web-Grounded Validation**
Every reviewer uses real-time web search on every iteration. Live literature review is a side effect — novelty claims are continuously checked against what already exists.

**3. Temporal Composition via Document**
Reviewers never communicate directly. Their distinct capabilities compose **through the document** across iterations. An idea introduced by one reviewer becomes a target for another in the next round — without either knowing. This is the core architectural insight: emergence through shared medium, not direct communication.

**4. Signal Voting**
```
Majority signal (2/3 same observation)  → apply with confidence
Minority signal (1/3 unique finding)    → do not ignore
                                          especially if source = Grok (OSINT)
```

**5. Opportunity Cost Stop Criterion**
```
STOP when reviewers independently conclude:
  "marginal value of further text improvement
   is less than value of running the experiment"

NOT → "text is perfect"
BUT → opportunity cost of polishing > cost of shipping
```

---

## Algorithm

```
INPUT: initial idea, sentence, or draft

PHASE 1 — DIVERGE
  Solution space expands aggressively.
  References, criteria, counterarguments accumulate.

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
  Suggestions become stylistic or tonal.

  Loop continues until STOP CRITERION is met.

OUTPUT: converged document + iteration log
```

Phase boundary is **emergent** — never explicitly set. Arises naturally from panel dynamics.

---

## Empirical Case Studies

Three case studies were run using the working implementation. Each started from a **single provocative sentence** — no prior research, no citations, no structure:

> *"Smaller context windows force better prompt engineering and produce higher quality outputs than large context windows"*

> *"Vibe coding is a valid software engineering methodology for production systems"*

> *"The most important unsolved problem in LLM alignment is not values but epistemics — models that confidently don't know what they don't know"*

All three runs converged in 3 rounds.

| Input (one sentence) | Domain | Rounds | Session Log | Final Synthesis |
|---|---|---|---|---|
| "Smaller context windows force better prompt engineering and produce higher quality outputs than large context windows" | Technical / CS | 3 | [log](cases/session_context_windows.md) | [synthesis](cases/synthesis_context_windows.md) |
| "Vibe coding is a valid software engineering methodology for production systems" | Contested / Engineering | 3 | [log](cases/session_vibe_coding.md) | [synthesis](cases/synthesis_vibe_coding.md) |
| "The most important unsolved problem in LLM alignment is not values but epistemics — models that confidently don't know what they don't know" | Philosophical / AI Safety | 3 | [log](cases/session_llm_alignment.md) | [synthesis](cases/synthesis_llm_alignment.md) |

**Key observation:** All three inputs were single sentences with zero citations. All three outputs contained verified citations sourced by Grok via real-time web search. Live literature review is an architectural side effect, not a separately invoked feature.

**Key observation:** All three inputs were single sentences with zero citations. All three outputs contained verified citations sourced by Grok via real-time web search. Live literature review is an architectural side effect, not a separately invoked feature.

---

## What CPAR Is and Is Not

**CPAR is:**
- A working cross-provider adversarial review system with a reference implementation
- A workflow architecture that applies blind peer review principles to document improvement
- Empirically observed to converge in 3 rounds on single-sentence inputs across three domains

**CPAR is not:**
- A validated framework with controlled benchmarks
- A replacement for expert human review
- A claim that composition always beats a stronger single model

The critical baseline comparison — CPAR vs. token-matched single-model self-refinement — has not been run. That is the next empirical step.

---

## Why It Matters

- **Research teams:** Turns a one-sentence idea into a cited, structured document ready for refinement
- **Automatic literature review:** Web-grounded reviewers continuously check novelty against live sources
- **Cross-lab diversity:** Each reviewer brings a different lab's training signal, failure modes, and tool access — blind to the others
- **Cost:** Working implementation runs on free tiers across all four providers

---

## Panel Configuration

| Parameter | Recommendation | Rationale |
|---|---|---|
| Panel size | N = 3 minimum, N = 5 robust | Odd number enables majority signal |
| Provider diversity | One per top-tier lab | Different RLHF, training data, blind spots |
| Model versions | Pin specific versions per run | Prevents cross-run variance from updates |
| Knowledge cutoff | Must be current | Stale models miss recent literature |
| Web search | Required for all reviewers | Grounds novelty claims in real literature |

**Models not used in current case studies:**
- Qwen — live search integration not confirmed in tested configuration
- DeepSeek — reasoning chain not auditable in English by Author in current workflow

---

## Repository Contents

| Artifact | Status |
|---|---|
| README / framework description | ✅ |
| Working Gradio implementation (`app/app.py`) | ✅ |
| BYOK support (Bring Your Own Keys) | ✅ |
| Parallel reviewers with retry logic | ✅ |
| Convergence judge (GPT as independent judge) | ✅ |
| Session export and iteration logs | ✅ |
| Case study logs (`cases/`) | ✅ |
| Benchmark comparison vs. single-model | ❌ |
| pip-installable library | ❌ |

---

## Next Steps

1. **Commit case study logs** — three runs are complete; logs go into `cases/`
2. **HuggingFace Spaces demo** — BYOK Gradio app, public
3. **Baseline comparison** — same input, single-model (Claude Sonnet solo) vs. CPAR; blind human eval
4. **arXiv technical report** — system description + three case studies + convergence analysis

---

## Citation

```bibtex
@misc{anokhin2026cpar,
  title  = {CPAR: Cross-Provider Adversarial Review Framework},
  author = {Anokhin, Alex},
  year   = {2026},
  note   = {Working system + case studies. github.com/olanokhin/cpar-framework}
}
```

---

**Author:** Alex Anokhin · [olanokhin@gmail.com](mailto:olanokhin@gmail.com)  
**Date:** March 2026