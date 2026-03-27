# CPAR — Cross-Provider Adversarial Review Framework

## One-liner

> *N independent AI reviewers with distinct cognitive profiles, biases, and real-time internet access conduct blind iterative peer review of a document until consensus convergence.*

---

## Roles

| Role | Model | Observed Superpower | Observed Bias |
|------|-------|-------------------|---------------|
| **Author / Synthesizer** | Claude Sonnet | Long-context coherence, signal filtering | Conservative, low ideation |
| **Research Validator** | Grok | Real-time OSINT, hundreds of sources per iteration | Seeks contradictions with reality |
| **Creative Architect** | Gemini | Elegant structural solutions | Prioritises composition over grounding |
| **Devil's Advocate** | ChatGPT | Adversarial skepticism | Engagement-optimised, default complimentary |

> Roles and superpowers were **observed empirically** across iterations — not pre-assigned.

---

## Model Selection Rationale

| Model | Inclusion Criterion |
|-------|-------------------|
| Claude Sonnet | BullshitBench #1 (91% detection, 3% hallucination) → optimal synthesis node |
| Grok | Unique real-time OSINT depth unavailable in other providers |
| Gemini | Creative restructuring, Google Research training signal |
| ChatGPT | Top-1 lab representation; skepticism carries high signal weight precisely because default mode is complimentary |
| Qwen | **Excluded** — knowledge cutoff stuck at end 2024 |
| DeepSeek | **Excluded** — non-English reasoning chain, not auditable by Author |

---

## Architectural Principles

### 1. Blind Review
- Each reviewer maintains independent chat with full document iteration history
- Reviewers **never** see each other's reviews
- Eliminates herding effect and authority bias

### 2. Web-Grounded Validation
- Every reviewer uses built-in web search on every iteration
- Grounds suggestions in real literature
- Produces automatic live literature review as side effect

### 3. Author Isolation
- Author receives all reviews simultaneously
- Each review is **labelled by reviewer name**
- Author knows the source of each suggestion

### 4. Signal Voting
```
Majority signal (2/3 same observation)  → strong, apply with confidence
Minority signal (1/3 unique finding)    → do not ignore
                                          especially if source = Grok (OSINT)
```

---

## Algorithm

```
INPUT: initial idea or draft

PHASE 1 — DIVERGE
  Characteristic: solution space expands aggressively
                  tables, criteria, references grow rapidly
  Signal to watch: volume of new insights per iteration

  Loop:
    Step 1: Author generates / updates document
    Step 2: All reviewers receive document IN PARALLEL
            + instruction: validate via web search,
              find gaps vs existing literature
    Step 3: Author receives 3 labelled reviews
            + instruction: extract rational signals,
              apply, produce next version

PHASE 2 — CONVERGE
  Characteristic: new findings overlap with existing ones
                  reviewers begin defending current structure
                  suggestions become stylistic / tonal

  Same loop continues until STOP CRITERION is met

STOP CRITERION:
  ∀ reviewers independently conclude:
  "marginal value of further text improvement
   is less than value of running the experiment"

  NOT → "text is perfect"
  BUT → opportunity cost of polishing > cost of shipping

OUTPUT: fixed document + iteration log
```

> Phase boundary is **emergent** — never explicitly set.
> Arises naturally from panel dynamics, typically around iteration 5-7.

---

## Emergent Cross-Reviewer Synergy

The critical property of CPAR is **not** parallelism.
It is temporal composition through the document as shared medium.

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

Reviewers never communicate directly.
Superpowers compose **through the document** across iterations — not within a single cycle.

> Synergy is only visible at the iteration sequence level.

---

## Novelty Preservation Mechanism

Web-grounded reviewers continuously check:
*"does this already exist?"*

Document drifts not toward "beautiful text"
but toward **maximum defensible novelty gap**.

Web search also enables reviewers to say:
*"three similar papers were desk-rejected without empirical results — prioritise experiment over polish."*

CPAR functions as **research advisor**, not just text reviewer.

---

## Panel Configuration

| Parameter | Recommendation | Rationale |
|-----------|---------------|-----------|
| Panel size | N = 3 minimum, N = 5 robust | Odd number enables majority signal |
| Provider diversity | One per top-tier lab | Different RLHF, training data, blind spots |
| Knowledge cutoff | Must be current | Stale models miss recent literature |
| Reasoning transparency | Must be auditable | Non-English chains not usable by Author |
| Web search | Required for all reviewers | Grounds novelty claims in real literature |

---

## Empirical Result

```
Case study:    cs.NE paper — Dynamic Recursive MoE
Iterations:    14
Panel:         Sonnet (Author) + Grok + Gemini + ChatGPT
Tier:          Free on all four providers
Phase 1:       ~iterations 1–5, rapid expansion
Phase 2:       ~iterations 6–14, convergence
Stop signal:   all reviewers independently concluded
               "run the experiment, text is sufficient"
```
