---
title: CPAR — Cross-Provider Adversarial Review
emoji: 🔬
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 6.10.0
app_file: app.py
pinned: false
license: apache-2.0
short_description: Blind iterative peer review by a cross-provider AI panel
---

# CPAR — Cross-Provider Adversarial Review Framework

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Status](https://img.shields.io/badge/Status-Working%20System%20%2B%20Benchmarks-green.svg)]()
[![HF Space](https://img.shields.io/badge/🤗%20Demo-HuggingFace%20Spaces-yellow.svg)](https://huggingface.co/spaces/olanokhin/cpar-framework)

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
| **Author / Synthesizer** | Claude Sonnet 4.6 | Long-context coherence, signal filtering | Conservative, low ideation |
| **Research Validator** | Grok 4.1 Fast | Real-time OSINT, web + X search per iteration | Seeks contradictions with reality |
| **Creative Architect** | Gemini 3 Flash Preview | Elegant structural solutions | Prioritises composition over grounding |
| **Devil's Advocate** | GPT-5.4 Mini | Adversarial skepticism | Default complimentary — skepticism carries high signal weight precisely because of this |

> Tendencies were **observed empirically** across iterations of case studies — not pre-assigned. They are versioned observations, not stable model properties.

**On the choice of Claude as Author:** Claude's role as synthesizer is informed in part by empirical evidence of its above-average tendency to identify and reject low-quality signals rather than incorporate them uncritically. The [Bullshit Benchmark](https://github.com/petergpt/bullshit-benchmark) — a benchmark testing whether models push back on nonsensical prompts instead of confidently answering them — shows Claude exhibits stronger resistance to accepting poor-quality input than most frontier models. This property is desirable in an Author that must filter N reviewer signals, discard noise, and resolve contradictions by majority vote rather than synthesize everything it receives.

**On reviewer role labels:** The role names (Research Validator, Creative Architect, Devil's Advocate) are *descriptive*, not prescriptive. All three reviewers receive an identical system prompt — no persona, no role instruction, no behavioral directive. The observed behavioral differences (Grok's citation density, Gemini's structural suggestions, GPT's adversarial stance) are emergent properties of provider-level differences in RLHF objectives, training corpora, and default generation behavior — not prompt engineering artifacts. This is verifiable in the session logs: identical input, identical instruction, three structurally distinct outputs per round.

Reproducibility note: model strings are pinned per run (see `app/cpar.py`). Output diversity is a function of provider-level weight differences — not prompt variation. Pattern-level reproducibility (Grok as citation validator, Gemini as structural architect) holds across runs on the same model versions. Whether these behavioral signatures persist across major version updates is an open empirical question and a known limitation of the current design.

> **Experiment snapshot — 2026-04-01.** Model versions, observed behavioral tendencies, and pricing are specific to this date and the exact model versions listed above. Role labels reflect emergent behavior observed in these versions — they may not hold across major model updates. Pricing verified against official provider documentation on the same date.

---

## Architectural Principles

**1. Blind Review**
Each reviewer maintains independent conversation history. Reviewers never see each other's reviews. Mitigates herding bias and authority effects.

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

| Input (one sentence) | Domain | Rounds | Session Log | Final Synthesis | Zero-shot |
|---|---|---|---|---|---|
| Context windows claim | Technical / CS | 3 | [log](cases/session_context_windows.md) | [synthesis](cases/synthesis_context_windows.md) | [baseline](baselines/zero_shot_author_web_smaller_context_windows_force.md) |
| Vibe coding claim | Contested / Engineering | 3 | [log](cases/session_vibe_coding.md) | [synthesis](cases/synthesis_vibe_coding.md) | [baseline](baselines/zero_shot_author_web_vibe_coding_is_a.md) |
| LLM alignment claim | Philosophical / AI Safety | 3 | [log](cases/session_llm_alignment.md) | [synthesis](cases/synthesis_llm_alignment.md) | [baseline](baselines/zero_shot_author_web_the_most_important_unsolved.md) |

**Observation:** All three inputs had zero citations. All three outputs contained verified citations sourced by reviewers via real-time web search. Live literature review is an architectural side effect, not a separately invoked feature.

---

## Baseline Comparison

To evaluate whether CPAR adds value beyond single-model generation, we ran a blind A/B comparison against a zero-shot baseline using the **same model, same system prompt, and same web search access** as CPAR's Author — isolating the adversarial review architecture as the sole variable.

**Experimental design:**
- **CPAR:** Claude Sonnet 4.6 (Author) + 3-reviewer panel (Grok, Gemini, GPT) × 3 rounds, all with web search
- **Zero-shot:** Claude Sonnet 4.6, same Author system prompt, same web search, single pass
- **Judge:** GLM-5 (Z.ai, via Together.ai) — architecturally independent from all panel members: different lab, different training corpus, different RLHF pipeline, different inference hardware (Huawei Ascend). No web search access.
- **Blinding:** Document position randomized per case. CPAR occupied position A in 1/3 cases and position B in 2/3 cases.

### Results

| Case | Factual | Balance | Structure | Practical | Overall | CPAR position |
|------|---------|---------|-----------|-----------|---------|--------------|
| context_windows | ✅ CPAR | ✅ CPAR | ✅ CPAR | ✅ CPAR | ✅ CPAR | B |
| vibe_coding | ✅ CPAR | ✅ CPAR | ✅ CPAR | ✅ CPAR | ✅ CPAR | B |
| llm_alignment | ✅ CPAR | ✅ CPAR | ✅ CPAR | ✅ CPAR | ✅ CPAR | A |

**CPAR wins 3/3 overall, 15/15 criteria, across both document positions.**

Full verdict logs with per-criterion quotes: [`baselines/`](baselines/)

- [verdict_context_windows.json](baselines/verdict_context_windows.json)
- [verdict_vibe_coding.json](baselines/verdict_vibe_coding.json)
- [verdict_llm_alignment.json](baselines/verdict_llm_alignment.json)
- [comparison_summary.md](baselines/comparison_summary.md)

### Cost Analysis

| Case | CPAR total | Zero-shot | Ratio |
|---|---|---|---|
| context_windows | $0.7156 | $0.4034 | 1.77× |
| vibe_coding | $0.8507 | $0.4188 | 2.03× |
| llm_alignment | $0.9860 | $0.4344 | 2.27× |
| **Average** | **$0.85** | **$0.42** | **2.02×** |

CPAR costs approximately **2× more** than an equivalent zero-shot call. This premium covers three rounds of parallel cross-provider review with independent web-grounded validation per round.

*Pricing snapshot: 2026-04-01. Models: Claude Sonnet 4.6 ($3/$15 per MTok), Grok 4.1 Fast ($0.20/$0.50 + $5/1k search calls), Gemini 3 Flash Preview ($0.50/$3 + $14/1k search queries), GPT-5.4 Mini ($0.75/$4.50). Gemini search billed at rack rate; Google provides 5,000 free grounding queries/month shared across Gemini 3.*

### Interpretation

The Author prompt is the primary control variable in CPAR. The architecture separates content generation (reviewers) from output synthesis (Author prompt) — applying the same prompt to both zero-shot and CPAR isolates adversarial diversity as the causal factor.

The judge's per-criterion quotes reveal the mechanism: CPAR outputs showed higher quantitative precision, more rigorous epistemic hedging, and more actionable research agendas — properties that emerge from iterative cross-provider challenge rather than from any single model's capabilities.

---

## What CPAR Is and Is Not

**CPAR is:**
- A working cross-provider adversarial review system with a reference implementation
- A workflow architecture that applies blind peer review principles to document improvement
- Empirically shown to outperform zero-shot with equivalent prompting and web search access across three domains and all evaluated criteria

**CPAR is not:**
- A validated framework with controlled benchmarks at scale
- A replacement for expert human review
- A claim that composition always beats a stronger single model

The token-matched single-model self-refinement comparison has not been run. That is the next empirical step.

---

## Panel Configuration

| Parameter | Recommendation | Rationale |
|---|---|---|
| Panel size | N = 3 minimum, N = 5 robust | Odd number enables majority signal |
| Provider diversity | One per top-tier lab | Different RLHF, training data, blind spots |
| Model versions | Pin specific versions per run | Prevents cross-run variance from updates |
| Knowledge cutoff | Must be current | Stale models miss recent literature |
| Web search | Required for all reviewers | Grounds novelty claims in real literature |
| Judge | Must be external to panel | Eliminates evaluator-panel affiliation as confound |

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
| Per-round cost tracking (tokens + search calls + USD) | ✅ |
| Convergence judge — GPT-5.4 Mini (internal, no zero-shot access) | ✅ |
| Evaluation judge — GLM-5 via Together.ai (external, blind A/B) | ✅ |
| Session export with full cost breakdown | ✅ |
| Case study logs and syntheses (`cases/`) | ✅ |
| Zero-shot baselines (`baselines/`) | ✅ |
| Baseline comparison scripts (`eval/`) | ✅ |
| Baseline verdict logs (`baselines/`) | ✅ |
| Token-matched self-refinement comparison | ❌ |
| pip-installable library | ❌ |

---

## Next Steps

1. ~~**HuggingFace Spaces demo**~~ ✅ [Live demo](https://huggingface.co/spaces/olanokhin/cpar-framework)
2. **Token-matched baseline** — CPAR vs. N×T single-model self-refinement steps
3. **arXiv technical report** — system description + case studies + benchmark results

---

## Citation

```bibtex
@misc{anokhin2026cpar,
  title  = {CPAR: Cross-Provider Adversarial Review Framework},
  author = {Anokhin, Alex},
  year   = {2026},
  note   = {Working system + benchmarks. arXiv preprint in preparation. github.com/olanokhin/cpar-framework}
}
```

---

**Author:** Alex Anokhin · [olanokhin@gmail.com](mailto:olanokhin@gmail.com)  
**Date:** April 2026
