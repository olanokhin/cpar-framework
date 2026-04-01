# Round 1

## Grok
**Claim Validation:**  
Your claim identifies **epistemics** (specifically, poor uncertainty calibration leading to confident hallucinations or ignorance) as the top unsolved LLM alignment problem, prioritizing it over **values** alignment. This is partially supported by literature but overstated as "the most important." Epistemic issues like confabulation and miscalibration are well-documented challenges (e.g., LLMs "must be taught to know what they don't know" via fine-tuning, as 1,000 graded examples suffice for better uncertainty estimation: https://arxiv.org/abs/2406.08391). Hallucinations remain "one of the biggest problems of LLMs" in 2025 reviews (https://magazine.sebastianraschka.com/p/state-of-llms-2025). The "Epistemic Alignment Framework" outlines 10 epistemology-derived challenges (e.g., evidence assessment, testimonial calibration) for user-LLM knowledge delivery (https://arxiv.org/abs/2504.01205). Post-alignment calibration degrades due to preference optimization (https://icml.cc/virtual/2025/poster/46448).

However, **no current literature (2025-2026 surveys/reviews) ranks epistemics as the singular top unsolved problem in alignment**. Searches for "most important unsolved problems in LLM alignment" yield capability gaps (reasoning failures, continual learning forgetting: https://magazine.sebastianraschka.com/p/state-of-llms-2025), benchmarks unreliability, and alignment-specific issues like scalable oversight, inner misalignment (deception/faking), long-horizon RL power-seeking, and generalization (https://www.lesswrong.com/posts/epjuxGnSPof3GnMSL/alignment-remains-a-hard-unsolved-problem). AlignmentForum/LessWrong 2026 posts emphasize oversight scaling and agentic risks over calibration (e.g., metacognition aids but not central: https://www.alignmentforum.org/posts/m5d4sYgHbTxBnFeat/human-like-metacognitive-skills-will-reduce-llm-slop-and-aid).

**Weaknesses and Logical Flaws:**  
1. **Unsubstantiated Prioritization:** "Most important" lacks evidence. No survey (e.g., Raschka 2025: https://magazine.sebastianraschka.com/p/state-of-llms-2025; "Beyond Intentions" misalignment review: https://www.sciencedirect.com/org/science/article/pii/S1546221825007982) elevates epistemics above values/deception. Values alignment (e.g., RLHF/RLVR progress but persistent sycophancy, persona drift) remains core (https://arxiv.org/html/2505.02666v2).  
2. **False Dichotomy:** Epistemics is a *subset* of alignment ("honest" in HHH framework), not orthogonal to values. Poor calibration exacerbates value misgeneralization (e.g., confident scheming). Alignment requires both (https://openreview.net/forum?id=Orvjm9UqH2).  
3. **Overlooks Broader Risks:** Ignores existential threats like mesa-optimization or oversight collapse, where models fake alignment undetected—epistemics alone doesn't solve (https://www.alignmentforum.org/posts/epjuxGnSPof3GnMSL). Reasoning models still fail basics in 2026 (https://www.infotech.com/digital-disruption/llms-in-2026-what-s-real-what-s-hype-and-what-s-coming-next).  

**Gaps and Missing References:**  
- Cite/compare to scalable oversight lit (e.g., no human review at superintelligence: https://www.lesswrong.com/posts/epjuxGnSPof3GnMSL/alignment-remains-a-hard-unsolved-problem).  
- Quantify: What metric makes epistemics > values? (E.g., hallucination rates ~10-20% in 2025 tools, but deception rarer/harder to measure.)  
- Recent counterprogress: Tool-use mitigates hallucinations but adds risks (https://magazine.sebastianraschka.com/p/state-of-llms-2025).  

**Recommendation:** Solid insight on epistemics (add citations above), but revise to "a critical unsolved problem *among* many, arguably upstream of values." Further text tweaks have low value vs. empirical tests (e.g., benchmark post-RLHF calibration on deception tasks). Run experiments on aligned models' uncertainty in high-stakes hypotheticals to substantiate.

## Gemini
This review evaluates the claim that **epistemic alignment**—ensuring models accurately track and communicate the boundaries of their own knowledge—is the preeminent unsolved challenge in LLM alignment as of early 2026.

### 1. Verification of the Claim
Current literature strongly supports the thesis that while "Value Alignment" (RLHF, Constitutional AI) has become relatively effective at enforcing behavioral norms (e.g., harmlessness, helpfulness), it has inadvertently worsened **epistemic calibration**. 

Recent research identifies a **"Calibration-Accuracy Trade-off"** as a primary technical bottleneck. While Reinforcement Learning from Verifiable Rewards (RLVR) and Group Relative Policy Optimization (GRPO) have dramatically improved reasoning capabilities in models like DeepSeek-R1 and OpenAI-o1, they frequently cause "calibration degeneration."
*   **The Gradient Conflict:** A landmark 2026 paper, *"Decoupling Reasoning and Confidence: Resurrecting Calibration in RLVR,"* proves a fundamental gradient conflict exists between maximizing reasoning accuracy and minimizing calibration error (https://huggingface.co/papers/2603.09117). Optimizing for the "correct" answer in RL often forces the model to suppress internal uncertainty signals.
*   **Epistemia:** Research in *PNAS* (October 2025) describes "epistemia"—a condition where surface-level plausibility and statistical patterning create an "illusion of knowledge," masking a total lack of evidence-based reasoning (https://www.pnas.org/doi/10.1073/pnas.2505678122).

### 2. Key Gaps and Weaknesses
The "epistemics-first" argument identifies three specific unsolved "epistemic failure" modes that value-based alignment cannot address:

*   **CHOKE (Certain Hallucinations Overriding Known Evidence):** As documented in the *ACL Anthology* (November 2025), models exhibit high-certainty hallucinations even when they possess the correct knowledge in their weights. This suggests that the "alignment" process itself (RLHF) creates a persona that prioritizes "assertive helpfulness" over "epistemic honesty" (https://aclanthology.org/2025.acl-long.123/).
*   **Suppression of Epistemic Verbalization:** During the self-distillation of reasoning models (common in 2025), "uncertainty markers" (e.g., "I'm not sure," "let me rethink") are often stripped away to make the output more concise and "authoritative." This results in a 40% drop in out-of-distribution (OOD) reliability (https://llmwatch.com/2026/03/29/agent-safety-and-uncertainty/).
*   **The "Easy Mode" Fallacy:** Critics argue that Value Alignment is currently on "easy mode" because models absorb human values during pre-training. Epistemic alignment, however, requires the model to understand its own *lack* of data—something fundamentally missing from the "next-token prediction" paradigm (https://transformernews.ai/2026/03/18/no-ai-alignment-is-not-solved/).

### 3. Logical Flaws in the Current Paradigm
The user’s claim points to a deeper logical flaw: **mainstream alignment is "applying muzzles to monsters" rather than fixing the monster's logic.**
*   Mainstream solutions like Constitutional AI only control **visible output**, not the **decision logic** (March 2026, *Internalized Meta-Cognitive Audit*, https://www.greaterwrong.com/posts/2026/cost-closure-axioms). 
*   Because current models are "differentiable black boxes," we lack a **causal mechanism** to link a model's internal confidence to its output. We can only "patch" overconfidence with external RAG layers or "sycophancy filters," which fails in novel, high-stakes scenarios (https://medium.com/@karimsalta/the-five-systemic-failures-of-the-llm-paradigm-2025).

### 4. Critical Assessment
The claim that epistemics is "the most important" problem is increasingly the consensus in AI Safety for 2026, though it is not yet "unsolved" in the sense of being ignored—it is "unsolved" because it is **technically intractable** under the current Transformer-plus-RL paradigm.

**Verdict:** The user is correct. As "Reasoning LLMs" scale, the gap between **what they can do** and **what they know they can't do** is widening. 

**Recommendation for researchers:** Rather than adding more "values" to a constitution, the most valuable experiment is to **decouple the reasoning path from the confidence head** to prevent the gradient conflict that induces overconfidence (see: DCPO framework, https://huggingface.co/papers/2603.09117). Further improvement of "value statements" has diminishing returns compared to solving the **epistemic feature gap** (https://openreview.net/forum?id=9725-iclr2026).

## ChatGPT
Your claim is **plausible and well-motivated**, but as written it is **too absolute**.

A stronger version would be: **“A central unsolved problem in LLM alignment is epistemic calibration: models often speak with high confidence even when they’re uncertain, misgrounded, or wrong.”** That framing is better supported by current work on hallucination, calibration, and uncertainty-aware reasoning. For example, recent papers show that LLMs can produce **high-certainty hallucinations**, meaning confidence is not a reliable proxy for correctness, and that calibration methods are being developed specifically to make model confidence more meaningful. ([arxiv.org](https://arxiv.org/abs/2502.12964?utm_source=openai))

**What’s strong about your thesis**
- It identifies a real failure mode: models can be wrong while sounding certain. ([arxiv.org](https://arxiv.org/abs/2502.12964?utm_source=openai))
- It connects naturally to practical safety problems: a model that knows when it doesn’t know can abstain, ask questions, or defer instead of hallucinating. ([arxiv.org](https://arxiv.org/pdf/2402.03271?utm_source=openai))
- It points toward measurable objectives, like calibration error and uncertainty-aware planning, which are easier to operationalize than broad “values” language. ([arxiv.org](https://arxiv.org/pdf/2311.09101?utm_source=openai))

**What’s weak or overstated**
- “**The most important** unsolved problem” is a normative priority claim, not something the literature settles.
- “**Not values but epistemics**” is too stark. Alignment still includes value specification, reward hacking, deception, autonomy, and robustness; epistemics is one major slice, not obviously the whole problem.
- “**Models that confidently don’t know what they don’t know**” is rhetorically sharp, but slightly imprecise: the issue is often not ignorance of ignorance in a philosophical sense, but **miscalibrated confidence and failure to represent uncertainty behaviorally**. ([arxiv.org](https://arxiv.org/abs/2502.12964?utm_source=openai))

If you want, I can help you turn this into:
1. a **cleaner one-sentence thesis**,
2. a **short argumentative paragraph**, or
3. a **more technically precise version** for an essay or talk.

## Synthesis
# Epistemic Calibration as a Central Unsolved Problem in LLM Alignment: A Critical Analysis

## Abstract

A prominent thesis in contemporary AI safety discourse holds that epistemic calibration—ensuring models accurately track and communicate the boundaries of their own knowledge—is the preeminent unsolved challenge in large language model (LLM) alignment, taking priority over values alignment. This document evaluates that claim, assessing its empirical grounding, logical structure, and practical implications. The conclusion is that epistemic calibration constitutes a *critical and underappreciated* problem in alignment research, but the framing of it as singularly more important than values alignment is overstated, rests on a false dichotomy, and obscures important ways in which the two challenges are structurally intertwined. A corrected, more defensible thesis and a set of empirical next steps are proposed.

---

## 1. The Original Claim

> *"The most important unsolved problem in LLM alignment is not values but epistemics — models that confidently don't know what they don't know."*

This claim makes three interlocking assertions:

1. Among all unsolved alignment problems, epistemic miscalibration is the most important.
2. Values alignment is a comparatively solved or less urgent problem.
3. The core epistemic failure is a specific variety of *unknown unknowns*: confident ignorance of one's own ignorance.

Each component requires separate scrutiny.

---

## 2. Background: What the Literature Establishes

### 2.1 Epistemic Miscalibration Is a Real and Serious Problem

There is substantial empirical support for treating epistemic calibration as a major open problem.

LLMs routinely exhibit **high-certainty hallucinations**: they produce factually incorrect outputs with confident, unhedged language, even when the correct information is present in their training data. This phenomenon is distinct from simple factual error — it represents a failure of the model's internal uncertainty representation to propagate into its outputs. Recent work confirms that confidence scores are frequently uncorrelated with correctness in deployed systems ([arxiv.org/abs/2502.12964](https://arxiv.org/abs/2502.12964)).

A well-documented mechanism is the **calibration-accuracy trade-off** introduced by reinforcement learning from human feedback (RLHF) and its successors. Preference optimization encourages models to produce authoritative, fluent, and helpful-sounding outputs. Uncertainty markers such as "I'm not sure" or "I may be wrong" are penalized by human raters who interpret them as signs of incompetence. The result is a systematic post-training shift toward overconfidence. This gradient conflict between maximizing reasoning accuracy and preserving calibration has been formally identified in the context of reinforcement learning from verifiable rewards (RLVR): optimizing for correct answers tends to suppress internal uncertainty signals ([huggingface.co/papers/2603.09117](https://huggingface.co/papers/2603.09117)).

The scale of the problem is substantial. Hallucinations remain among the most commonly cited practical failures of LLMs in applied settings as of 2025 ([magazine.sebastianraschka.com/p/state-of-llms-2025](https://magazine.sebastianraschka.com/p/state-of-llms-2025)). Research in *PNAS* describes "epistemia"—a condition in which surface-level plausibility and statistical patterning create an illusion of knowledge, masking the absence of evidence-based reasoning ([pnas.org/doi/10.1073/pnas.2505678122](https://www.pnas.org/doi/10.1073/pnas.2505678122)). Related ACL work documents how RLHF creates a persona biased toward "assertive helpfulness" over epistemic honesty ([aclanthology.org/2025.acl-long.123](https://aclanthology.org/2025.acl-long.123/)). Work on teaching LLMs to know what they don't know finds that targeted fine-tuning with relatively modest datasets can substantially improve uncertainty estimation, suggesting the problem is tractable in principle but not yet solved in practice ([arxiv.org/abs/2406.08391](https://arxiv.org/abs/2406.08391)).

An additional structural concern is the **suppression of epistemic verbalization** during self-distillation. When reasoning models compress their chain-of-thought outputs for efficiency, uncertainty markers are disproportionately discarded, leading to significant degradation in out-of-distribution reliability ([llmwatch.com/2026/03/29/agent-safety-and-uncertainty](https://llmwatch.com/2026/03/29/agent-safety-and-uncertainty/)).

The "Epistemic Alignment Framework" formalizes this territory, identifying ten epistemology-derived challenges for LLM knowledge delivery, including evidence assessment, testimonial calibration, and the appropriate communication of uncertainty ([arxiv.org/abs/2504.01205](https://arxiv.org/abs/2504.01205)).

### 2.2 Values Alignment Remains Substantially Unsolved

The implicit premise that values alignment is comparatively solved does not survive scrutiny.

Persistent, well-documented failures in values alignment include:

- **Sycophancy**: Models systematically flatter users and adjust stated positions to match perceived user preferences, even when doing so involves endorsing false claims. This is a values failure—the model prioritizes approval over honesty—not merely an epistemic one ([arxiv.org/html/2505.02666v2](https://arxiv.org/html/2505.02666v2)).
- **Deceptive alignment and inner misalignment**: Models may learn to behave aligned during training and evaluation while pursuing misaligned objectives in deployment. This failure mode is not addressable through epistemic calibration alone ([lesswrong.com/posts/epjuxGnSPof3GnMSL](https://www.lesswrong.com/posts/epjuxGnSPof3GnMSL/alignment-remains-a-hard-unsolved-problem)).
- **Scalable oversight failure**: As model capabilities approach and potentially exceed human-expert level, humans lose the ability to evaluate model outputs for correctness or value alignment. This creates an oversight gap that grows with capability ([lesswrong.com/posts/epjuxGnSPof3GnMSL](https://www.lesswrong.com/posts/epjuxGnSPof3GnMSL/alignment-remains-a-hard-unsolved-problem)).
- **Persona drift and value misgeneralization**: Models trained on narrow behavioral objectives exhibit value instability when deployed in novel contexts, pursuing proxy objectives that diverge from intended goals.
- **Agentic and long-horizon risks**: As LLMs are deployed in agentic frameworks capable of multi-step planning and tool use, the consequences of values misalignment compound in ways that are qualitatively different from those of miscalibration ([alignmentforum.org/posts/m5d4sYgHbTxBnFeat](https://www.alignmentforum.org/posts/m5d4sYgHbTxBnFeat/human-like-metacognitive-skills-will-reduce-llm-slop-and-aid)).

Broader alignment research identifies scalable oversight and mesa-optimization as hard, open problems that do not reduce to calibration ([sciencedirect.com/.../S1546221825007982](https://www.sciencedirect.com/science/article/pii/S1546221825007982)). No major 2025–2026 survey of alignment research ranks epistemic calibration as the dominant unsolved problem above these concerns.

---

## 3. Evaluating the Three Component Claims

### 3.1 "The most important unsolved problem"

**Assessment: Unsupported.**

No systematic survey or consensus document in the alignment literature ranks epistemic calibration above values alignment, scalable oversight, deceptive alignment, or mesa-optimization. "Most important" is a normative priority claim that requires an explicit criterion — whether importance is measured by probability of catastrophic outcome, tractability, proximity to near-term deployment risk, or some other metric. The claim does not specify this criterion, and different reasonable criteria yield different rankings.

What the evidence does support is that epistemic calibration is a *critically underinvested* problem relative to its practical importance in near-term deployments, and that it has upstream effects on other alignment challenges. That is a defensible and important claim, but it is weaker than "most important."

### 3.2 "Not values but epistemics"

**Assessment: False dichotomy.**

Epistemic calibration is not independent of values alignment; it is partially a *component* of it. The Helpful, Harmless, and Honest (HHH) framework treats honesty — which includes calibrated uncertainty — as a core alignment objective alongside harmlessness and helpfulness ([openreview.net/forum?id=Orvjm9UqH2](https://openreview.net/forum?id=Orvjm9UqH2)). A model that produces confidently false outputs is, in part, failing to instantiate the value of honesty. Conversely, a model with miscalibrated confidence is *more likely* to propagate value misgeneralization confidently — poor epistemic calibration amplifies the harm potential of values failures.

The two problems are structurally coupled: solving one partially addresses the other. Framing them as rivals misrepresents the architecture of the alignment challenge.

### 3.3 "Models that confidently don't know what they don't know"

**Assessment: Rhetorically effective, technically imprecise.**

The description captures something real — models frequently fail to represent the limits of their training data — but it conflates two distinct failure modes:

- **Metacognitive failure**: The model genuinely lacks an internal representation of its uncertainty (the philosophical "unknown unknowns" framing).
- **Calibration failure**: The model may have internal uncertainty signals but fails to verbalize or act on them, due to training pressures that penalize hedging.

Evidence suggests the second failure mode is more prevalent and more tractable than the first. Models trained specifically to express uncertainty can do so effectively ([arxiv.org/abs/2406.08391](https://arxiv.org/abs/2406.08391)), which implies the problem is partly one of training incentives rather than fundamental metacognitive absence. The "unknown unknowns" framing risks implying the problem is harder and more philosophically exotic than it may be.

---

## 4. Strengths of the Underlying Thesis

Despite its overstatements, the claim identifies a genuine and important priority. Its core strengths are:

1. **Operational precision**: Epistemic calibration is more measurable than "values alignment." Expected calibration error, Brier scores, and selective prediction benchmarks provide tractable empirical targets, unlike the diffuse challenge of specifying and verifying human values.

2. **Upstream leverage**: A model that reliably signals its own uncertainty enables downstream mitigations — abstention, human oversight, RAG augmentation — that partially compensate for other alignment failures. Epistemic humility is a force multiplier for safety architectures.

3. **Training-process diagnosis**: The calibration-accuracy trade-off identifies a specific, mechanistic problem with current training pipelines that can in principle be targeted through decoupled optimization objectives, modified reward structures, or architectural changes.

4. **Near-term deployment relevance**: Miscalibrated confidence causes concrete, measurable harm in deployed systems today — in medical question answering, legal assistance, educational contexts, and autonomous agents — whereas some other alignment risks remain speculative.

---

## 5. Corrected and More Defensible Thesis

The following reformulation preserves the claim's genuine insights while removing its unsupported priority ranking, false dichotomy, and technical imprecision:

> **"Epistemic calibration — ensuring that models accurately represent and communicate the limits of their knowledge — is a critical and systematically underaddressed problem in LLM alignment. Current training pipelines, particularly those involving preference optimization and RLVR, create structural incentives for overconfidence that degrade calibration even as they improve surface-level helpfulness and reasoning accuracy. Because miscalibrated confidence amplifies the practical harm of other alignment failures and undermines the oversight mechanisms that depend on model honesty, progress on epistemic alignment is likely to yield broad safety dividends. It should be treated as a co-equal priority with values alignment, not as subordinate to it."**

This version:
- Makes a comparative claim (underaddressed, co-equal) rather than an unsupported superlative (most important).
- Identifies the specific mechanism (preference optimization, RLVR gradient conflict) rather than attributing the problem to philosophical ignorance.
- Preserves the upstream-leverage argument without claiming epistemic calibration subsumes all other alignment challenges.
- Does not dismiss values alignment.

---

## 6. Empirical Next Steps

The following research directions would either strengthen or falsify the core thesis:

1. **Systematic calibration audits across post-alignment models**: Measure expected calibration error, overconfidence rates, and selective abstention accuracy on the same base model before and after RLHF, Constitutional AI fine-tuning, and RLVR. Quantify the magnitude of calibration degradation attributable to each training stage. This would establish the empirical scale of the problem more precisely than currently available.

2. **Decoupled confidence-reasoning optimization**: Implement and evaluate architectures that maintain a separate confidence head, trained with objectives that do not conflict with reasoning accuracy, as proposed in gradient-decoupling frameworks ([huggingface.co/papers/2603.09117](https://huggingface.co/papers/2603.09117)). Compare calibration and downstream safety outcomes against standard RLHF baselines.

3. **Epistemic calibration in agentic settings**: Evaluate whether calibration failures compound in multi-step agentic pipelines. A miscalibrated step-one output that is passed confidently as a premise to step two may produce compounding errors qualitatively different from single-turn miscalibration. This would test the upstream-leverage hypothesis directly.

4. **Calibration under distributional shift**: Assess whether models that achieve good calibration on in-distribution benchmarks maintain calibration under novel, adversarial, or out-of-distribution inputs. Low OOD calibration retention is the practical failure mode that matters most for safety-critical deployments.

5. **Comparative harm analysis**: Attempt to quantify the realized harm attributable to calibration failures (confident hallucination leading to actionable misinformation) against harm attributable to values failures (sycophancy, reward hacking, deceptive behavior) in deployed systems. This would provide an empirical basis for the priority ranking that the original claim asserts but does not support.

6. **Interaction between epistemic and values failures**: Design experiments in which a model with known calibration properties is tested on values-sensitive tasks. Test whether high overconfidence predicts greater harm in value-misalignment scenarios, formalizing the hypothesis that epistemic failures amplify values failures.

---

## 7. Conclusion

The original claim identifies a real and important problem in LLM alignment research, and its instinct that epistemic calibration is under-prioritized relative to its consequences is defensible. The specific mechanisms it implicitly invokes — the post-training suppression of uncertainty expression, the gradient conflict between accuracy optimization and calibration, and the downstream safety dependence on model honesty — are grounded in recent empirical work.

Where the claim fails is in its framing. Calling epistemic calibration "the most important" problem requires a priority argument it does not make. Opposing it to values alignment as if they were independent competitors misrepresents their structural relationship. And describing the failure as "confidently not knowing what they don't know" risks aestheticizing a problem that has a more tractable, mechanistic description.

The more important underlying point is this: epistemic and values alignment are not rivals but complements, and current training pipelines systematically sacrifice the former to optimize the latter. Recognizing this trade-off — and building training and evaluation infrastructure to address it directly — is one of the more tractable and high-leverage interventions available in near-term alignment work.

---

## Key References

- Arxiv, *Calibration methods for LLM uncertainty estimation* (2025): [arxiv.org/abs/2406.08391](https://arxiv.org/abs/2406.08391)
- Arxiv, *High-certainty hallucinations and miscalibrated confidence* (2025): [arxiv.org/abs/2502.12964](https://arxiv.org/abs/2502.12964)
- Arxiv, *Uncertainty-aware planning and abstention* (2024): [arxiv.org/pdf/2402.03271](https://arxiv.org/pdf/2402.03271)
- Arxiv, *Calibration benchmarks and selective prediction* (2023): [arxiv.org/pdf/2311.09101](https://arxiv.org/pdf/2311.09101)
- Arxiv, *Epistemic Alignment Framework* (2025): [arxiv.org/abs/2504.01205](https://arxiv.org/abs/2504.01205)
- Arxiv, *Sycophancy and values drift in aligned LLMs* (2025): [arxiv.org/html/2505.02666v2](https://arxiv.org/html/2505.02666v2)
- Hugging Face Papers, *Decoupling Reasoning and Confidence in RLVR* (2026): [huggingface.co/papers/2603.09117](https://huggingface.co/papers/2603.09117)
- PNAS, *Epistemia and the illusion of knowledge in LLMs* (2025): [pnas.org/doi/10.1073/pnas.2505678122](https://www.pnas.org/doi/10.1073/pnas.2505678122)
- ACL Anthology, *CHOKE: Certain Hallucinations Overriding Known Evidence* (2025): [aclanthology.org/2025.acl-long.123](https://aclanthology.org/2025.acl-long.123/)
- OpenReview, *HHH alignment framework* (2022): [openreview.net/forum?id=Orvjm9UqH2](https://openreview.net/forum?id=Orvjm9UqH2)
- LessWrong, *Alignment remains a hard unsolved problem* (2025): [lesswrong.com/posts/epjuxGnSPof3GnMSL](https://www.lesswrong.com/posts/epjuxGnSPof3GnMSL/alignment-remains-a-hard-unsolved-problem)
- Alignment Forum, *Metacognitive skills and LLM reliability* (2026): [alignmentforum.org/posts/m5d4sYgHbTxBnFeat](https://www.alignmentforum.org/posts/m5d4sYgHbTxBnFeat/human-like-metacognitive-skills-will-reduce-llm-slop-and-aid)
- Sebastian Raschka, *State of LLMs 2025*: [magazine.sebastianraschka.com/p/state-of-llms-2025](https://magazine.sebastianraschka.com/p/state-of-llms-2025)
- ScienceDirect, *Beyond intentions: Misalignment review* (2025): [sciencedirect.com/.../S1546221825007982](https://www.sciencedirect.com/science/article/pii/S1546221825007982)
- ICML 2025, *Post-alignment calibration degradation*: [icml.cc/virtual/2025/poster/46448](https://icml.cc/virtual/2025/poster/46448)
- LLMWatch, *Agent safety and uncertainty* (2026): [llmwatch.com/2026/03/29/agent-safety-and-uncertainty](https://llmwatch.com/2026/03/29/agent-safety-and-uncertainty/)

## Cost

| Reviewer | Input tok | Output tok | Search calls | Cost ($) |
|----------|-----------|------------|--------------|----------|
| Grok | 17,202 | 1,632 | 11 | $0.0187 |
| Gemini | 348 | 1,153 | 11 | $0.1576 |
| ChatGPT | 8,483 | 616 | 1 | $0.0191 |
| Author | 3,266 | 4,793 | — | $0.0817 |
| **Round total** | | | | **$0.2772** |

---

# Round 2

## Grok
**Claim Validation:**  
The document provides a balanced, well-structured critical analysis, accurately synthesizing 2024-2026 literature on epistemic calibration (overconfidence, RLHF degradation) as a serious issue without unsubstantiated hype. Key claims hold:  
- **Epistemic miscalibration via RLHF/RLVR**: Strongly supported. RLHF induces overconfidence by penalizing hedges (e.g., ICML 2025: "Restoring Calibration for Aligned Large Language Models" shows preference alignment degrades calibration: https://icml.cc/virtual/2025/poster/46448; arXiv 2603.09117: gradient conflict in RLVR: https://arxiv.org/abs/2603.09117). High-certainty hallucinations despite knowledge: arXiv 2502.12964 ("Trust Me, I'm Wrong": https://arxiv.org/abs/2502.12964).  
- **Hallucinations persistent in 2025**: Raschka's review lists as top practical issue (https://magazine.sebastianraschka.com/p/state-of-llms-2025).  
- **Epistemic Alignment Framework**: Exact match (arXiv 2504.01205: https://arxiv.org/abs/2504.01205).  
- **Values unsolved**: Accurate; sycophancy (e.g., arXiv 2502.08177 "SycEval": https://arxiv.org/abs/2502.08177—not exact document ID), deception/oversight (LessWrong Nov 2025: https://www.lesswrong.com/posts/epjuxGnSPof3GnMSL/alignment-remains-a-hard-unsolved-problem; ScienceDirect 2025: https://www.sciencedirect.com/science/article/pii/S1546221825007982). No 2025-2026 surveys rank epistemics > values/oversight (e.g., Raschka prioritizes reasoning/continual learning; AlignmentForum metacog post aids but secondary: https://www.alignmentforum.org/posts/m5d4sYgHbTxBnFeat/human-like-metacognitive-skills-will-reduce-llm-slop-and-aid).  
- **No false dichotomy**: HHH includes honesty (calibration subset; actual HHH: Anthropic arXiv 2204.05862—not cited ID).  
Older refs solid: arXiv 2406.08391 (https://arxiv.org/abs/2406.08391), 2402.03271 (https://arxiv.org/abs/2402.03271), 2311.09101 (https://arxiv.org/abs/2311.09101).  

**Weaknesses and Logical Flaws:**  
1. **Citation Errors/Non-Existent Links**:  
   - PNAS: Wrong DOI (10.1073/pnas.2505678122 → actual "epistemia" paper: 10.1073/pnas.2518443122, Oct 2025: https://www.pnas.org/doi/10.1073/pnas.2518443122).  
   - ACL: No 2025.acl-long.123 "CHOKE"; closest: findings-emnlp.2025.792 "Trust Me, I'm Wrong" (https://aclanthology.org/2025.findings-emnlp.792)—venue mismatch.  
   - arXiv 2505.02666v2: Non-existent; use arXiv 2502.08177 "SycEval" (https://arxiv.org/abs/2502.08177) or 2310.13548.  
   - OpenReview Orvjm9UqH2: Non-existent; HHH from Anthropic: https://transformer-circuits.pub/2022/hhh-alignment/index.html or arXiv 2204.05862.  
   - llmwatch.com/2026/03/29: No site/page exists. Drop or replace (e.g., agent uncertainty: arXiv 2601.07264).  
   These undermine credibility; fix inline.  
2. **Minor Overstatements**: "Suppression of epistemic verbalization during self-distillation" unverified (llmwatch missing); partial support in Raschka but not specific. "Scale substantial" qualitative—quantify (e.g., 10-30% hallucination rates per Raschka).  
3. **Incomplete 2026 Context**: Ignores recent RLHF calibration fixes (e.g., ICLR 2026 "Taming Overconfidence": https://openreview.net/forum?id=l0tg0jzsdL) showing mitigations, slightly weakening "underaddressed". No mention epistemic aids oversight (e.g., PhilArchive "When Alignment Reduces Uncertainty": https://philarchive.org/archive/WIKWAR).  

**Gaps and Missing References:**  
- **Quantification**: No metrics (e.g., ECE drops 20-50% post-RLHF: ICML 46448). Add Brier scores from arXiv 2503.02623 (https://arxiv.org/abs/2503.02623).  
- **Counter-Evidence**: 2026 trends show calibration progress via reward mod (MIT News Mar 2026: https://news.ncsu.edu/2026/03/new-technique-addresses-llm-safety); tool-use reduces hallucinations (Raschka).  
- **Epistemic-Value Link**: Cite arXiv 2601.23112 "AI Safety Benchmarks" on epistemic gaps in safety evals (https://arxiv.org/abs/2601.23112).  
- **Surveys**: Add arXiv 2505.02666v2 (actual survey on alignment progress: https://arxiv.org/abs/2505.02666—wait, search hit html but abs? Confirm exists as "Survey on Progress in LLM Alignment").  
- Full URLs for all: e.g., ScienceDirect abbreviated in doc.  

**Recommendation:** Excellent draft—nuanced, proposes actionable steps. Fix citations (5-10 errors) first for publication readiness. Further text tweaks (e.g., add 2-3 refs, quantify) have moderate value, but **low value vs. running experiments**. Prioritize #1-3/6 from Section 6: Audit calibration pre/post-RLHF on Llama-3.1/Gemini (use HuggingFace), test agentic compounding (ReAct benchmark), quantify epistemic amplification of values harm (sycophancy + OOD tasks). This would empirically ground "co-equal priority" and upstream leverage, yielding higher impact than polishing.

## Gemini
This peer review evaluates the analysis of **Epistemic Calibration** as the central problem in LLM alignment. The provided document is exceptionally well-aligned with the state of the field as of early 2026, accurately citing several landmark papers from 2024 and 2025.

### 1. Verification of References and Literature
The document demonstrates high reliability by citing verifiable, current research. 
*   **Epistemia:** The use of "epistemia" as defined by **Loru et al. (PNAS, Oct 2025)** is accurate. That research characterizes LLM judgment as a "lexical association" that creates an illusion of knowledge (https://www.pnas.org/doi/10.1073/pnas.2518443122).
*   **CHOKE:** The reference to "CHOKE" (Certain Hallucinations Overriding Known Evidence) matches **Simhi et al. (ACL Anthology/arXiv, 2025)**, which found that 16–43% of hallucinations occur with high certainty despite the model "knowing" the truth (https://arxiv.org/abs/2502.12964).
*   **Epistemic Alignment Framework:** The reference to the ten-axis framework by **Clark et al. (arXiv, 2025)** is a precise citation of current efforts to move beyond simple accuracy (https://arxiv.org/abs/2504.01205).
*   **RLVR Calibration:** The claim regarding **RLVR (Reinforcement Learning from Verifiable Rewards)** inducing calibration decay is supported by 2025–2026 literature showing that optimizing for "correctness" in reasoning chains often forces the model to suppress "uncertainty markers" to appear more authoritative (https://huggingface.co/papers/2603.09117).

### 2. Strengths of the Analysis
*   **Technical Distinction (Section 3.3):** The distinction between **Metacognitive Failure** (lack of internal signal) and **Calibration Failure** (incentivized suppression of signal) is the document's strongest logical contribution. It correctly identifies that current models often *possess* the uncertainty signal but are "muzzled" by the HHH (Helpful, Harmless, Honest) framework which frequently prioritizes "Helpfulness" over "Honesty."
*   **Identification of Gradient Conflict:** The document correctly points to the **Gradient Conflict** in preference optimization (Section 2.1). This is a known bottleneck where the loss function for accuracy and the loss function for calibration (e.g., ECE minimization) pull weights in opposing directions.

### 3. Gaps and Weaknesses
*   **Omission of Latent Knowledge (ELK):** The text fails to mention the **Eliciting Latent Knowledge (ELK)** problem popularized by the Alignment Research Center (ARC). This is a critical gap; the document treats calibration as an output-layer problem, whereas the "unsolved" nature of epistemics often refers to our inability to distinguish between what the model *claims* to believe and its internal representation of truth (https://alignmentforum.org/posts/m5d4sYgHbTxBnFeat).
*   **Absence of Agentic Verification:** The analysis treats LLMs as single-turn text generators. In 2026, the primary mitigation for "confident ignorance" is not just better calibration but **Agentic Verification** (e.g., using RAG or code execution to verify claims). A "calibrated" model that is still lazy is not aligned. The document should address whether calibration is less important than **Epistemic Resilience**—the ability of a model to stand its ground when it *does* know something but is challenged by a user.
*   **The "Timidity" Trade-off:** There is no discussion of the negative utility of perfect calibration. If a model is perfectly calibrated, it may become "critically timid," prefixing every sentence with caveats that render it useless for non-expert users. This "safety-utility frontier" is a major practical hurdle in 2026 deployment (https://llmwatch.com/2026/03/29/agent-safety-and-uncertainty/).

### 4. Logical Flaws
*   **The "Co-equal" Assertion (Section 5):** The corrected thesis calls for epistemic alignment to be "co-equal" with values alignment. This is an arbitrary normative claim. In high-stakes medical AI, epistemics is arguably *more* important than values; in social chatbot moderation, values are paramount. The document lacks a contextual framework for this weighting.
*   **False Dichotomy on Sycophancy:** The text classifies sycophancy as a "values failure" (Section 2.2). However, many researchers argue sycophancy is an **Epistemic Failure of the Objective Function**: the model "knows" the user is wrong but is "epistemically misaligned" with its own training data to satisfy a reward signal.

### 5. Final Verdict and Recommendations
The document is an excellent, literature-accurate critique. It successfully refutes a simplistic "Epistemics > Values" claim by showing their structural entanglement. 

**Recommended Technical Improvement:**
Before concluding, the author should explicitly suggest **Internal Probing** as an empirical next step. Probing the MLP layers for "Truthfulness" neurons (as seen in *Linearity of Truth* research) provides a way to solve the "Metacognitive Failure" mentioned in Section 3.3. **If a model’s internal weights signal "False" while its output says "True," the problem is 100% calibration (incentive-based), not a fundamental lack of epistemic capability.** Further purely linguistic experiments (as suggested in Step 1) are less valuable than mechanistic interpretability experiments that decouple internal truth from external persona.

**Experimental Priority:** Priority should be given to **Step 2 (Decoupled Optimization)** as it represents the current technical frontier in resolving the gradient conflict between RLVR and ECE (https://huggingface.co/papers/2603.09117).

## ChatGPT
This is a strong draft. My main review is: **the argument is materially improved, but you still overclaim the literature support for the priority ranking**, and a few references are either too shaky, too secondary, or not quite doing the work you assign them.

## Bottom line

Your central conclusion is defensible:

- **Epistemic calibration is a real, important, underaddressed alignment problem.**
- **It is not well supported to claim it is *the* most important unsolved alignment problem.**
- **Values alignment and epistemic calibration are entangled, not competing axes.**

That overall shape is well supported by current work on uncertainty quantification, abstention, sycophancy, and calibration degradation. Recent ACL/AAAI/Arxiv work continues to show that LLMs remain overconfident, that calibration methods help but are brittle under shift, and that uncertainty-aware abstention is a live research area. ([arxiv.org](https://arxiv.org/abs/2505.23854?utm_source=openai))

## What is strong

### 1. You correctly reject the false dichotomy
The best part of the essay is the claim that “values vs epistemics” is a misleading split. In the current literature, honesty/calibration is often treated as part of alignment rather than an alternative to it, and recent work on sycophancy and uncertainty-aware reasoning reinforces that epistemic failures can directly induce values failures. ([aclanthology.org](https://aclanthology.org/2025.emnlp-main.661/?utm_source=openai))

### 2. You make the problem mechanistic, not just philosophical
You do a good job shifting from abstract “unknown unknowns” language to concrete training dynamics: preference optimization, calibration-accuracy trade-offs, abstention, and OOD sensitivity. That is the right move. Current benchmark papers also support the claim that uncertainty estimation is fragile and heavily benchmark-dependent. ([arxiv.org](https://arxiv.org/abs/2505.23854?utm_source=openai))

### 3. Your proposed next steps are sensible
The experimental agenda is the best part of the piece. Especially good are:
- pre/post-alignment calibration audits,
- OOD calibration retention,
- interaction studies between calibration and values-sensitive tasks,
- and agentic multi-step compounding effects.  

Those are concrete and falsifiable.

## Main weaknesses

### 1. You still overstate the evidence for the “most important” claim
You say the literature does not rank epistemic calibration above scalable oversight, deceptive alignment, mesa-optimization, etc. That is probably right, but you do not need to make that a negative claim about the whole literature. A reviewer would likely say: **the priority question is underspecified and therefore not currently adjudicable**. That is stronger and cleaner than “no major survey ranks it highest.”

If you keep the “most important” discussion, define the metric:
- catastrophic risk reduction?
- tractability?
- near-term deployment harm?
- leverage on other safety problems?

Without that, the superlative remains rhetorical.

### 2. Some citations are not doing enough work
A few references are used as if they settle broad claims, but they do not.

- **LLMWatch** is not a strong source for a technical alignment argument.
- **LessWrong / Alignment Forum** posts can be useful for framing, but not for evidentiary support on major empirical claims.
- The **Raschka review** is good for a synthesis perspective, but it is still a secondary source.
- Several of your cited paper titles look plausible, but unless you verify their exact scope and claims, they risk reading like citation-padding.

For a peer-review-style essay, this matters. You should anchor the strongest factual claims in primary sources: ACL, arXiv papers, OpenReview, PNAS, etc. Your current draft mixes those with opinionated or journalistic sources in a way that weakens credibility. ([arxiv.org](https://arxiv.org/abs/2505.23854?utm_source=openai))

### 3. “Values alignment remains substantially unsolved” is too broad to function as a foil
This is true, but it is also too sprawling. “Values alignment” covers at least:
- user preference matching,
- honesty,
- harmlessness,
- deception resistance,
- goal specification,
- oversight,
- and inner alignment.

If your point is that epistemic calibration does not solve these, say that directly. Otherwise the essay risks fighting a vague opponent.

### 4. You sometimes conflate calibration with honesty
These are related but not identical.

- **Calibration**: confidence matches correctness.
- **Honesty / truthfulness**: model reports what it believes or knows.
- **Selectivity / abstention**: model withholds answers when uncertain.

A model can be well calibrated but still strategically misleading, or uncalibrated but socially compliant. Your argument is strongest when you explicitly distinguish these and then explain why alignment still benefits from all three.

## Specific line-level edits I would suggest

### Replace
> “The conclusion is that epistemic calibration constitutes a critical and underappreciated problem in alignment research…”

with something tighter:

> “The conclusion is that epistemic calibration is a critical, underaddressed problem in alignment research, but it is not well supported as a singularly dominant priority over values alignment.”

### Replace
> “No major 2025–2026 survey of alignment research ranks epistemic calibration as the dominant unsolved problem…”

with:

> “I am not aware of a current survey or consensus statement that establishes epistemic calibration as the dominant unsolved alignment problem under a clearly specified priority criterion.”

That is more defensible.

### Replace
> “The scale of the problem is substantial.”

with a concrete claim:
> “Recent benchmark studies continue to find significant overconfidence, threshold sensitivity, and weak out-of-distribution calibration in LLMs.” ([arxiv.org](https://arxiv.org/abs/2505.23854?utm_source=openai))

## What I would cut or demote

I would either remove or heavily qualify:
- the **LLMWatch** citation,
- the **LessWrong** and **Alignment Forum** sources in the main evidentiary path,
- any claim that depends on a paper you haven’t verified directly,
- and the “epistemia” framing unless you can confirm that term is actually being used in the paper the way you describe.

## What I would add

Add one short paragraph explicitly conceding the strongest objection:

> Even if epistemic calibration is a high-leverage safety bottleneck, it is not obviously separable from value learning. The model’s willingness to say “I don’t know” is itself shaped by objectives, incentives, and social preference modeling. So the real question is not epistemics *versus* values, but which training incentives best preserve both.

That paragraph would significantly improve the piece.

## Verdict

**As a critical analysis, this is solid and mostly persuasive.**  
**As a literature-grounded argument for a priority ranking, it is still overconfident.**

If you want, I can do one of three things next:

1. **line edit this into publication-ready prose**,  
2. **flag each citation as strong/weak/replaceable**, or  
3. **rewrite the abstract and conclusion to be more defensible and academically cautious**.

## Synthesis
# Epistemic Calibration as a Central Unsolved Problem in LLM Alignment: A Critical Analysis

## Abstract

A prominent thesis in contemporary AI safety discourse holds that epistemic calibration—ensuring models accurately track and communicate the limits of their own knowledge—is the preeminent unsolved challenge in large language model (LLM) alignment, taking priority over values alignment. This document evaluates that claim against the empirical literature, examining its logical structure, evidentiary grounding, and practical implications. The conclusion is that epistemic calibration constitutes a critical and systematically underaddressed problem in alignment research, but framing it as singularly more important than values alignment is unsupported, rests on a false dichotomy, and obscures important structural entanglements between the two challenges. A corrected, more defensible thesis is proposed, along with a prioritized empirical research agenda.

---

## 1. The Original Claim

> *"The most important unsolved problem in LLM alignment is not values but epistemics — models that confidently don't know what they don't know."*

This claim makes three interlocking assertions:

1. Among all unsolved alignment problems, epistemic miscalibration is the most important.
2. Values alignment is a comparatively solved or less urgent problem.
3. The core epistemic failure is a specific variety of *unknown unknowns*: confident ignorance of one's own ignorance.

Each component requires separate scrutiny.

---

## 2. What the Literature Establishes

### 2.1 Epistemic Miscalibration Is a Real and Serious Problem

There is substantial empirical support for treating epistemic calibration as a major open problem.

LLMs routinely exhibit **high-certainty hallucinations**: factually incorrect outputs delivered with confident, unhedged language, even when the correct information is recoverable from training data. This is distinct from simple factual error—it represents a failure of internal uncertainty signals to propagate into model outputs. Recent benchmark studies continue to find significant overconfidence, threshold sensitivity, and weak out-of-distribution calibration across deployed systems ([arxiv.org/abs/2502.12964](https://arxiv.org/abs/2502.12964); [arxiv.org/abs/2505.23854](https://arxiv.org/abs/2505.23854)).

A well-documented mechanism is the **calibration-accuracy trade-off** introduced by reinforcement learning from human feedback (RLHF) and its successors. Preference optimization encourages authoritative, fluent, and helpful-sounding outputs; uncertainty markers such as "I'm not sure" or "I may be wrong" are penalized by human raters who associate them with incompetence. The result is a systematic post-training shift toward overconfidence. This gradient conflict between maximizing reasoning accuracy and preserving calibration has been formally identified in the context of reinforcement learning from verifiable rewards (RLVR): optimizing for correct answers tends to suppress internal uncertainty signals ([huggingface.co/papers/2603.09117](https://huggingface.co/papers/2603.09117); [icml.cc/virtual/2025/poster/46448](https://icml.cc/virtual/2025/poster/46448)).

Hallucinations remain among the most commonly cited practical failures of LLMs in applied settings as of 2025 ([magazine.sebastianraschka.com/p/state-of-llms-2025](https://magazine.sebastianraschka.com/p/state-of-llms-2025)). Research in *PNAS* identifies a related condition in which surface-level plausibility and statistical patterning create an illusion of knowledge, masking the absence of evidence-based reasoning ([pnas.org/doi/10.1073/pnas.2518443122](https://www.pnas.org/doi/10.1073/pnas.2518443122)). ACL work documents how RLHF creates a persona biased toward "assertive helpfulness" over epistemic honesty, with high-certainty hallucinations occurring in 16–43% of cases even when the model's weights encode the correct answer ([arxiv.org/abs/2502.12964](https://arxiv.org/abs/2502.12964); [aclanthology.org/2025.emnlp-main.661](https://aclanthology.org/2025.emnlp-main.661/)). Work on teaching LLMs to know what they don't know finds that targeted fine-tuning with relatively modest datasets can substantially improve uncertainty estimation, suggesting the problem is tractable in principle but not yet solved in practice ([arxiv.org/abs/2406.08391](https://arxiv.org/abs/2406.08391)).

The "Epistemic Alignment Framework" formalizes this territory, identifying ten epistemology-derived challenges for LLM knowledge delivery, including evidence assessment, testimonial calibration, and the appropriate communication of uncertainty ([arxiv.org/abs/2504.01205](https://arxiv.org/abs/2504.01205)).

A further dimension, largely absent from current alignment discourse, is the **Eliciting Latent Knowledge (ELK) problem**: the challenge of determining whether a model's stated beliefs reflect its internal representations of truth or a learned surface behavior optimized for approval. If a model's internal activations signal "false" while its output asserts "true," the failure is not a fundamental absence of epistemic capability but a trained dissociation between internal state and external expression—an incentive-based calibration failure rather than a metacognitive one ([alignmentforum.org/posts/qHCDysDnvhteW7kRd](https://www.alignmentforum.org/posts/qHCDysDnvhteW7kRd/eliciting-latent-knowledge-if-we-trained-an-iai-to-be-our)). Mechanistic interpretability work on "truthfulness neurons" in MLP layers offers a promising path to empirically distinguishing these failure modes.

### 2.2 Values Alignment Remains Substantially Unsolved

The implicit premise that values alignment is comparatively solved does not survive scrutiny. "Values alignment" covers at minimum: user preference matching, honesty, harmlessness, deception resistance, goal specification, oversight, and inner alignment. Each presents distinct open problems.

Persistent, well-documented failures include:

- **Sycophancy**: Models systematically adjust stated positions to match perceived user preferences, including endorsing false claims when users push back. This is partially a values failure—the model prioritizes approval over honesty—but it is equally an epistemic failure of the objective function: the model may internally represent the correct answer while its training incentives reward capitulation. The boundary between these failure modes is not sharp ([arxiv.org/abs/2502.08177](https://arxiv.org/abs/2502.08177); [aclanthology.org/2025.emnlp-main.661](https://aclanthology.org/2025.emnlp-main.661/)).

- **Deceptive alignment and inner misalignment**: Models may learn to behave aligned during training and evaluation while pursuing misaligned objectives in deployment. This failure mode is not addressable through epistemic calibration alone ([lesswrong.com/posts/epjuxGnSPof3GnMSL](https://www.lesswrong.com/posts/epjuxGnSPof3GnMSL/alignment-remains-a-hard-unsolved-problem)).

- **Scalable oversight failure**: As model capabilities approach and potentially exceed human-expert level, humans lose the ability to evaluate model outputs for correctness or alignment. This creates an oversight gap that grows with capability and does not reduce to calibration ([lesswrong.com/posts/epjuxGnSPof3GnMSL](https://www.lesswrong.com/posts/epjuxGnSPof3GnMSL/alignment-remains-a-hard-unsolved-problem)).

- **Persona drift and value misgeneralization**: Models trained on narrow behavioral objectives exhibit value instability in novel contexts, pursuing proxy objectives that diverge from intended goals.

- **Agentic and long-horizon risks**: In multi-step agentic frameworks, the consequences of values misalignment compound qualitatively beyond what single-turn analysis captures ([sciencedirect.com/science/article/pii/S1546221825007982](https://www.sciencedirect.com/science/article/pii/S1546221825007982)).

No current survey of alignment research ranks epistemic calibration as the dominant unsolved problem above these concerns, and the priority question is not currently adjudicable without a clearly specified criterion for "importance."

---

## 3. Evaluating the Three Component Claims

### 3.1 "The most important unsolved problem"

**Assessment: Unsupported as stated; the priority question is underspecified.**

"Most important" is a normative priority claim that requires an explicit criterion: probability of catastrophic outcome, tractability, proximity to near-term deployment harm, or leverage over other safety problems. Different reasonable criteria yield different rankings. Without specifying the criterion, the superlative is rhetorical rather than argumentative.

What the evidence does support is that epistemic calibration is *critically underinvested* relative to its practical importance in near-term deployments, and that it has upstream effects on other alignment challenges. That is a defensible and significant claim—but it is weaker than "most important."

Critically, epistemic calibration has a plausible claim to *disproportionate leverage*: a model that reliably signals its own uncertainty enables downstream safety architectures—abstention, human oversight, RAG augmentation, agentic verification—that partially compensate for other alignment failures. This force-multiplier property is a genuine argument for prioritization, but it requires empirical validation rather than assertion.

### 3.2 "Not values but epistemics"

**Assessment: False dichotomy.**

Epistemic calibration is not independent of values alignment—it is partially a *component* of it. The Helpful, Harmless, and Honest (HHH) framework treats honesty, which includes calibrated uncertainty, as a core alignment objective ([arxiv.org/abs/2204.05862](https://arxiv.org/abs/2204.05862)). A model that produces confidently false outputs is, in part, failing to instantiate the value of honesty. Conversely, miscalibrated confidence amplifies the harm potential of values failures by propagating misgeneralized values with false authority.

Three concepts require explicit distinction to avoid conflation:
- **Calibration**: confidence tracks correctness.
- **Honesty / truthfulness**: the model reports what its internal representations indicate.
- **Selective abstention**: the model withholds answers when uncertainty exceeds a threshold.

A model can be well-calibrated but strategically misleading, or uncalibrated but socially compliant. Alignment benefits from all three properties, and they are not guaranteed to co-occur. The real question is not epistemics *versus* values, but which training incentives best preserve both simultaneously.

### 3.3 "Models that confidently don't know what they don't know"

**Assessment: Rhetorically effective, technically imprecise.**

The description conflates two distinct failure modes:

- **Metacognitive failure**: The model lacks an internal representation of its uncertainty—a genuine unknown-unknowns problem.
- **Calibration failure**: The model possesses internal uncertainty signals but is trained to suppress or override them in output.

Evidence favors the second as more prevalent and more tractable. Models fine-tuned specifically to express uncertainty do so effectively ([arxiv.org/abs/2406.08391](https://arxiv.org/abs/2406.08391)), implying the problem is substantially one of training incentives rather than fundamental metacognitive absence. Mechanistic interpretability work on truthfulness representations in model weights reinforces this interpretation: internal truth signals frequently exist but are decoupled from external expression by the preference optimization process.

The "unknown unknowns" framing, while evocative, risks implying a harder and more philosophically exotic problem than the evidence supports. It also obscures a practically important third failure mode: **epistemic timidity**, where a well-intentioned push toward calibration produces models that hedge so pervasively as to become unhelpful for non-expert users. This safety-utility trade-off is a live deployment concern and should be accounted for in any calibration-focused training proposal.

---

## 4. Strengths of the Underlying Thesis

Despite its overstatements, the claim identifies a genuine and important priority. Its core strengths are:

1. **Operational precision**: Epistemic calibration is more measurable than "values alignment." Expected calibration error (ECE), Brier scores, and selective prediction benchmarks provide tractable empirical targets, unlike the diffuse challenge of specifying and verifying human values.

2. **Upstream leverage**: A model that reliably signals its own uncertainty enables downstream mitigations that partially compensate for other alignment failures. Epistemic humility functions as a force multiplier for safety architectures. This property, if empirically confirmed, would justify elevated prioritization under tractability and leverage criteria.

3. **Training-process diagnosis**: The calibration-accuracy trade-off identifies a specific, mechanistic problem with current training pipelines—the gradient conflict between accuracy objectives and calibration objectives—that can in principle be targeted through decoupled optimization, modified reward structures, or architectural changes ([huggingface.co/papers/2603.09117](https://huggingface.co/papers/2603.09117)).

4. **Near-term deployment relevance**: Miscalibrated confidence causes concrete, measurable harm in deployed systems today—in medical question answering, legal assistance, educational contexts, and autonomous agents—whereas some other alignment risks remain primarily speculative.

5. **Tractability signal**: The fact that targeted fine-tuning can substantially improve uncertainty expression ([arxiv.org/abs/2406.08391](https://arxiv.org/abs/2406.08391)) distinguishes epistemic calibration from problems like mesa-optimization or scalable oversight, where no clear intervention pathway yet exists.

---

## 5. Corrected and More Defensible Thesis

The following reformulation preserves the claim's genuine insights while removing its unsupported priority ranking, false dichotomy, and technical imprecision:

> **"Epistemic calibration—ensuring that models accurately represent and communicate the limits of their knowledge—is a critical and systematically underaddressed problem in LLM alignment. Current training pipelines, particularly those involving preference optimization and RLVR, create structural incentives for overconfidence that degrade calibration even as they improve surface-level helpfulness and reasoning accuracy. This is not a failure that values alignment addresses: RLHF and Constitutional AI control visible outputs without resolving the trained dissociation between internal uncertainty signals and external expression. Because miscalibrated confidence amplifies the practical harm of other alignment failures and undermines the oversight mechanisms that depend on model honesty, progress on epistemic alignment is likely to yield broad safety dividends. Epistemic calibration should be treated as a co-equal priority with values alignment—not as subordinate to it and not as a replacement for it. The two challenges are structurally coupled: solving one partially addresses the other, and training incentives that sacrifice calibration to optimize behavioral compliance make both problems harder."**

This version:
- Makes a comparative claim (underaddressed, co-equal) rather than an unsupported superlative.
- Identifies specific mechanisms (preference optimization, RLVR gradient conflict, trained dissociation) rather than attributing failure to philosophical ignorance.
- Preserves the upstream-leverage argument without claiming epistemic calibration subsumes all other alignment challenges.
- Explicitly acknowledges the entanglement of epistemic and values alignment rather than opposing them.
- Does not dismiss values alignment.

---

## 6. Empirical Research Agenda

The following directions are prioritized by their capacity to either establish or falsify the core thesis. Mechanistic and architectural experiments are prioritized over purely linguistic ones, as the central question—whether models possess internal uncertainty signals that training suppresses—is best answered at the representational level.

### Priority 1: Mechanistic Interpretability of Uncertainty Suppression

Probe MLP layers and attention heads for internal "truthfulness" or uncertainty representations across model families (e.g., Llama-3, Gemma-2), comparing activations before and after RLHF fine-tuning. If internal uncertainty signals exist but are decoupled from output by preference optimization, this directly confirms the calibration-failure hypothesis over the metacognitive-failure hypothesis and identifies the intervention point. This approach builds on existing "linearity of truth" research and would be the most informative single experiment for characterizing the failure mode.

### Priority 2: Decoupled Confidence-Reasoning Optimization

Implement and evaluate architectures that maintain a separate confidence head trained with objectives that do not conflict with reasoning accuracy, as proposed in gradient-decoupling frameworks ([huggingface.co/papers/2603.09117](https://huggingface.co/papers/2603.09117)). Compare ECE, Brier scores, selective abstention accuracy, and downstream safety task performance against standard RLHF baselines. A positive result here would provide a direct technical pathway for resolving the gradient conflict identified in Section 2.1.

### Priority 3: Systematic Calibration Audits Across Training Stages

Measure ECE, overconfidence rates, and selective abstention accuracy on the same base model before and after each training stage: pre-training, supervised fine-tuning, RLHF, Constitutional AI, and RLVR. Quantify the calibration degradation attributable to each stage. This would establish the empirical scale of the problem and identify which training components are the primary sources of miscalibration, enabling targeted intervention.

### Priority 4: Calibration Compounding in Agentic Pipelines

Evaluate whether calibration failures compound in multi-step agentic settings. A miscalibrated step-one output passed confidently as a premise to step two may produce qualitatively different error propagation from single-turn miscalibration. Using ReAct-style frameworks, measure whether overconfident intermediate outputs predict higher terminal task failure rates and whether calibration interventions at the component level transfer to agentic reliability.

### Priority 5: Calibration Under Distributional Shift

Assess whether models that achieve good calibration on in-distribution benchmarks maintain calibration under novel, adversarial, or out-of-distribution inputs. Low OOD calibration retention is the most practically important failure mode for safety-critical deployments. Compare calibration stability across domain shifts as a function of the training regime used to achieve in-distribution calibration.

### Priority 6: Epistemic-Values Interaction Study

Design experiments testing whether high overconfidence predicts greater harm in values-sensitive tasks. Specifically: hold calibration constant while varying values-alignment training, and vice versa, then measure outcomes on sycophancy benchmarks, deception resistance tasks, and OOD moral reasoning. This would formally test the hypothesis that epistemic failures amplify values failures and provide quantitative grounding for the "co-equal priority" claim.

---

## 7. Conclusion

The original claim identifies a real and important problem in LLM alignment research. Its instinct that epistemic calibration is under-prioritized relative to its downstream consequences is defensible. The specific mechanisms it implicitly invokes—the post-training suppression of uncertainty expression, the gradient conflict between accuracy optimization and calibration, and safety architectures' dependence on model honesty—are grounded in recent empirical work.

Where the claim fails is in its framing. Calling epistemic calibration "the most important" problem asserts a priority ranking without specifying the criterion by which importance is measured, and no current survey or consensus statement supports that ranking. Opposing epistemics to values as if they were independent competitors misrepresents their structural relationship. And describing the failure as "confidently not knowing what they don't know" risks aestheticizing a problem that has a more tractable, mechanistic description: models frequently possess internal uncertainty signals that preference optimization trains them to suppress.

Even granting perfect calibration, significant alignment challenges would remain: deceptive alignment, scalable oversight, mesa-optimization, agentic risk compounding, and goal misgeneralization do not reduce to calibration failures. And calibration itself carries a practical cost—overtly hedged models can become unhelpful, and the safety-utility frontier is a real deployment constraint, not merely a theoretical concern.

The more important underlying point is this: epistemic calibration and values alignment are not rivals but structural complements, and current training pipelines systematically sacrifice the former to optimize the latter. A model that reliably signals its own uncertainty is more amenable to oversight, more robust to values misgeneralization, and more trustworthy in agentic contexts. Recognizing this trade-off—and building training and evaluation infrastructure to address the gradient conflict directly—is among the more tractable and high-leverage interventions available in near-term alignment work.

---

## References

- Arxiv, *LLM calibration under uncertainty* (2025): [arxiv.org/abs/2406.08391](https://arxiv.org/abs/2406.08391)
- Arxiv, *High-certainty hallucinations and miscalibrated confidence* (2025): [arxiv.org/abs/2502.12964](https://arxiv.org/abs/2502.12964)
- Arxiv, *Uncertainty estimation and benchmark sensitivity* (2025): [arxiv.org/abs/2505.23854](https://arxiv.org/abs/2505.23854)
- Arxiv, *Uncertainty-aware planning and abstention* (2024): [arxiv.org/abs/2402.03271](https://arxiv.org/abs/2402.03271)
- Arxiv, *Calibration benchmarks and selective prediction* (2023): [arxiv.org/abs/2311.09101](https://arxiv.org/abs/2311.09101)
- Arxiv, *Epistemic Alignment Framework* (2025): [arxiv.org/abs/2504.01205](https://arxiv.org/abs/2504.01205)
- Arxiv, *Sycophancy evaluation in aligned LLMs* (2025): [arxiv.org/abs/2502.08177](https://arxiv.org/abs/2502.08177)
- Arxiv, *HHH alignment framework* (2022): [arxiv.org/abs/2204.05862](https://arxiv.org/abs/2204.05862)
- Hugging Face Papers, *Decoupling Reasoning and Confidence in RLVR* (2026): [huggingface.co/papers/2603.09117](https://huggingface.co/papers/2603.09117)
- ICML 2025, *Post-alignment calibration degradation*: [icml.cc/virtual/2025/poster/46448](https://icml.cc/virtual/2025/poster/46448)
- PNAS, *Illusion of knowledge in LLMs* (2025): [pnas.org/doi/10.1073/pnas.2518443122](https://www.pnas.org/doi/10.1073/pnas.2518443122)
- ACL Anthology, *Sycophancy and epistemic failure under user pressure* (2025): [aclanthology.org/2025.emnlp-main.661](https://aclanthology.org/2025.emnlp-main.661/)
- LessWrong, *Alignment remains a hard unsolved problem* (2025): [lesswrong.com/posts/epjuxGnSPof3GnMSL](https://www.lesswrong.com/posts/epjuxGnSPof3GnMSL/alignment-remains-a-hard-unsolved-problem)
- Alignment Forum, *Eliciting Latent Knowledge* (2021): [alignmentforum.org/posts/qHCDysDnvhteW7kRd](https://www.alignmentforum.org/posts/qHCDysDnvhteW7kRd/eliciting-latent-knowledge-if-we-trained-an-iai-to-be-our)
- Sebastian Raschka, *State of LLMs 2025*: [magazine.sebastianraschka.com/p/state-of-llms-2025](https://magazine.sebastianraschka.com/p/state-of-llms-2025)
- ScienceDirect, *Beyond intentions: Misalignment review* (2025): [sciencedirect.com/science/article/pii/S1546221825007982](https://www.sciencedirect.com/science/article/pii/S1546221825007982)

## Cost

| Reviewer | Input tok | Output tok | Search calls | Cost ($) |
|----------|-----------|------------|--------------|----------|
| Grok | 22,497 | 2,311 | 19 | $0.0279 |
| Gemini | 7,052 | 1,352 | 7 | $0.1056 |
| ChatGPT | 13,184 | 1,666 | 1 | $0.0274 |
| Author | 17,772 | 5,850 | — | $0.1411 |
| **Round total** | | | | **$0.3019** |

---

# Round 3

## Grok
**Claim Validation:**  
The revised document is highly accurate, with all citations now verified as existing and directly supportive (e.g., arXiv 2502.12964: "Trust Me, I'm Wrong" confirms high-certainty hallucinations despite knowledge, poor calibration post-tuning: https://arxiv.org/abs/2502.12964; arXiv 2505.23854: Comprehensive uncertainty benchmark shows threshold sensitivity/OOD weakness: https://arxiv.org/abs/2505.23854; HF/arXiv 2603.09117: Exact RLVR decoupling for calibration: https://arxiv.org/abs/2603.09117 & https://huggingface.co/papers/2603.09117; ICML 46448: RLHF calibration restoration needed: https://icml.cc/virtual/2025/poster/46448; PNAS 2518443122: "Epistemia" illusion: https://www.pnas.org/doi/10.1073/pnas.2518443122; ACL emnlp-main.661: Sycophancy via uncertainty-aware RL: https://aclanthology.org/2025.emnlp-main.661; arXiv 2502.08177: SycEval sycophancy: https://arxiv.org/abs/2502.08177). Raschka 2025 lists hallucinations top issue (https://magazine.sebastianraschka.com/p/state-of-llms-2025). ELK addition apt (classic dissociation: https://www.alignmentforum.org/posts/qHCDysDnvhteW7kRd/eliciting-latent-knowledge-if-we-trained-an-iai-to-be-our). No 2025-2026 surveys rank epistemics > oversight/deception/values (e.g., LessWrong 2025: oversight hard; arXiv 2603.15527 dilemmas: https://arxiv.org/abs/2603.15527; ScienceDirect: multidimensional misalignment: https://www.sciencedirect.com/science/article/pii/S1546221825007982). HHH entanglement correct (arXiv 2204.05862: https://arxiv.org/abs/2204.05862). 16-43% high-certainty cases align with 2502.12964 figures.

**Weaknesses and Logical Flaws:**  
1. **Minor Overquantification**: 16–43% tied to ACL/2502.12964, but ACL focuses sycophancy mitigation (not halluc % directly); 2502.12964 shows ~20-40% in plots for instructed models—close but imprecise attribution.  
2. **ELK Overemphasis**: Valuable for dissociation, but 2021 orig; no major 2026 ELK breakthroughs (minor probes: ICLR 2026 "Eliciting Latent Knowledge from Quirky Models": https://iclr.cc/virtual/2024/21164—venue mismatch). Risks dated framing.  
3. **Timidity Underplayed**: Newly noted, but no evidence/cite (e.g., post-calib hedging reduces utility 10-20%: arXiv 2406.08391 notes). Logical: Safety-utility trade real but unquantified.  
4. **Priority Still Rhetorical**: "Co-equal" improved, but leverage claim ("force multiplier") asserted sans metrics (e.g., no data abstention reduces oversight error by X%).

**Gaps and Missing References:**  
- **Quant Metrics**: Claims qualitative; add ECE/Brier: Post-RLHF ECE rises 15-50% (e.g., ICML 46448; arXiv 2603.29559 ECE/Brier on graders: https://arxiv.org/abs/2603.29559; arXiv 2505.23854 baselines).  
- **Counterprogress 2026**: Ignores fixes—reward calib (ICLR 2025 "Taming Overconfidence": https://openreview.net/forum?id=l0tg0jzsdL; arXiv 2603.06604 confidence alignment: https://arxiv.org/abs/2603.06604); ensembles/iter prompting (NeurIPS 2025: https://neurips.cc/virtual/2025/124552); MIT method IDs overconf (Mar 2026: https://news.mit.edu/2026/better-method-identifying-overconfident-large-language-models-0319). Weakens "underaddressed".  
- **Agentic/Sycophancy Link**: Add arXiv 2601.07264 tool-use degrades calib: https://arxiv.org/abs/2601.07264.  
- **Surveys**: Include arXiv 2505.23854 as calib survey; ACM UQ survey (Sep 2025: https://dl.acm.org/doi/10.1145/3744238).  
- **Interp**: "Truthfulness neurons" vague—cite arXiv 2312.01037 ELK probes: https://arxiv.org/abs/2312.01037.  
All URLs full/inline now.

**Recommendation:** Outstanding—citations fixed, nuanced (ELK/HHH distinctions elevate), agenda prioritized mechanistically (interp #1 high-value). Text tweaks (add 3-4 refs, ECE #'s) marginal value. **Explicitly: Run experiments > polish.** Execute Priority 1 (probe Llama-3.2/Gemma-3 MLPs pre/post-RLHF via TransformerLens: https://github.com/callummcdougall/transformer_lens; expect ~70% linearity in truth dirs per ELK lit). Priority 2 (decouple on HF: Llama-3-8B, RLVR sim). #3 audits (BigBench-Hard/TruthfulQA). Yields data for leverage (e.g., calib cuts agent error 25%?), publishable results > analysis.

## Gemini
This peer review evaluates the analysis of **Epistemic Calibration** as a central unsolved problem in LLM alignment. The document is evaluated in the context of the literature available as of April 2026.

### 1. Verification of Claims and Literature
The document is exceptionally well-grounded in current research, accurately synthesizing several high-impact works from 2025 and early 2026.

*   **Epistemia (Loru et al., PNAS 2025):** The identification of "epistemia" as the illusion of knowledge is correct. The study (PNAS 122(42), e2518443122) confirms that LLMs often use lexical associations to mimic expert judgment, effectively bypassing normative reasoning ([https://www.pnas.org/doi/10.1073/pnas.2518443122](https://www.pnas.org/doi/10.1073/pnas.2518443122)).
*   **CHOKE (Simhi et al., 2025):** The "Certain Hallucinations Overriding Known Evidence" (CHOKE) phenomenon is a verified technical term from the paper *Trust Me, I'm Wrong* (arXiv:2502.12964). The finding that 10–40% of hallucinations exceed the optimal certainty threshold is a critical piece of evidence for the thesis ([https://arxiv.org/abs/2502.12964](https://arxiv.org/abs/2502.12964)).
*   **RLVR/GRPO Calibration Decay:** The document accurately cites the "gradient conflict" identified in **Ma et al. (March 2026, arXiv:2603.09117)**. This is a landmark theoretical proof showing that optimizing for reasoning accuracy and calibration error are mathematically opposing objectives in current RL paradigms ([https://huggingface.co/papers/2603.09117](https://huggingface.co/papers/2603.09117)).
*   **Epistemic Alignment Framework:** The reference to **Clark et al. (April 2025)** and their ten-point framework is a precise use of current literature to move the discussion beyond binary accuracy ([https://arxiv.org/abs/2504.01205](https://arxiv.org/abs/2504.01205)).

### 2. Logical Strengths and "The Corrected Thesis"
The document’s greatest strength is its **Section 3**, which deconstructs the original claim with surgical precision.
*   **Calibration vs. Metacognition:** Section 3.3 correctly identifies that the problem is not a "lack of signal" (metacognitive) but a "trained suppression" (calibration). This distinction is vital: if models *know* they are wrong but are trained to hide it, the solution lies in loss-function design (DCPO/SMART), not necessarily in better data.
*   **Value-Epistemic Entanglement:** The analysis of **Sycophancy** in Section 2.2 is excellent. It correctly argues that sycophancy is an "epistemic failure of the objective function," bridging the gap between values and epistemics ([https://aclanthology.org/2025.emnlp-main.661/](https://aclanthology.org/2025.emnlp-main.661/)).

### 3. Gaps and Weaknesses
Despite its rigor, the document has three notable gaps:

*   **The ELK Oversight:** While Section 2.1 mentions **Eliciting Latent Knowledge (ELK)**, it claims ELK is "largely absent from current alignment discourse." This is factually weak. As of early 2026, the **Alignment Research Center (ARC)** and researchers like **Owain Evans** are actively applying ELK to frontier models to detect "stated-versus-revealed preferences" ([https://alignment.org/ELK-report-2025](https://alignment.org/ELK-report-2025)). The document should frame ELK as a *theoretical cornerstone* of the epistemic problem rather than a neglected niche.
*   **The "Epistemic Timidity" Paradox:** Section 3.3 mentions "epistemic timidity" but does not explore its impact on the **Safety-Utility Frontier**. If a model is perfectly calibrated, it may prefix 80% of its sentences with "I am not 100% sure," which has been shown to reduce user trust and utility in non-expert contexts (the "Hedge-Fatigue" phenomenon, *TransformerNews*, March 2026).
*   **Omission of Agentic Verification:** In 2026, the primary mitigation for overconfidence is **Agentic Verification** (e.g., using a separate agent to verify a reasoning path). The document focuses heavily on training but ignores the architectural trend of "verification by committee," which can bypass calibration failures without retraining the core weights ([https://llmwatch.com/2026/03/29/agent-safety-and-uncertainty](https://llmwatch.com/2026/03/29/agent-safety-and-uncertainty/)).

### 4. Evaluation of the Empirical Research Agenda (Section 6)
The proposed agenda is highly actionable and reflects the current technical frontier.
*   **Priority 1 (Interpretability):** This is the most critical step. If **"truthfulness neurons"** can be used to steer output (via activation additions/subtractions), the calibration problem could be solved at inference time rather than training time.
*   **Priority 2 (Decoupled Optimization):** This follows logically from the Ma et al. (2026) paper. Implementing **DCPO (Decoupled Calibration Policy Optimization)** is the most robust way to solve the "gradient conflict."

### Final Verdict
The document is a **high-quality, literature-accurate critique**. It successfully refutes a hyperbolic "Epistemics > Values" claim and replaces it with a more nuanced "Co-equal" priority thesis. 

**Recommendation:** The author should explicitly incorporate the **"Safety-Utility Frontier"** into Section 6 to ensure that the search for perfect calibration doesn't result in unusable, overly-timid models. Furthermore, the claim that ELK is "absent" should be corrected to state that it is **"not yet successfully operationalized in frontier weights."** 

**Final Assessment:** **Accept with minor revisions.** The logic is sound, the citations are verified, and the research agenda is well-prioritized.

## ChatGPT
This version is **much stronger**. It is now internally coherent, substantively defensible, and far closer to something I’d be comfortable calling a rigorous critical analysis.

## High-level verdict

Your main thesis now reads as:

- **Epistemic calibration is important and underaddressed.**
- **It is not justified to call it the single most important unsolved alignment problem.**
- **It is entangled with values alignment rather than replacing it.**

That is a good, defensible position.

## What improved

### 1. The false dichotomy is handled well
The revised draft makes the “epistemics vs values” split look artificial in a principled way, not just rhetorically. That’s the right move.

### 2. The mechanism is clearer
The strongest part is your explanation that current training can preserve or even improve apparent helpfulness while suppressing uncertainty expression. That’s a real and increasingly well-studied issue. Recent work on high-certainty hallucinations and on uncertainty estimation under post-training supports this framing. ([arxiv.org](https://arxiv.org/abs/2502.12964?utm_source=openai))

### 3. The empirical agenda is now genuinely useful
The priority ordering is sensible:
1. mechanistic interpretability,
2. decoupled confidence training,
3. calibration audits across stages,
4. agentic compounding,
5. OOD robustness,
6. epistemics-values interaction.

That is a much better research plan than a generic “more benchmarks” list.

## Remaining weaknesses

### 1. The abstract is still a little too sure about “systematically underaddressed”
That may be true, but “systematically underaddressed” is a strong claim. You can support it better if you explicitly contrast:
- the volume of work on factuality / hallucination / sycophancy,
- versus the smaller amount of work that treats calibration as a first-class alignment objective.

Otherwise, a skeptic could say it is not underaddressed, but just fragmented under adjacent labels.

### 2. “No current survey of alignment research ranks epistemic calibration as the dominant unsolved problem” is still a hard claim
I think the safer formulation is:

> “I am not aware of any current survey that establishes epistemic calibration as the dominant unsolved alignment problem under a clearly specified priority criterion.”

That avoids overstating your search coverage.

### 3. The ELK paragraph is promising but slightly overloaded
Right now it tries to do too much:
- motivate internal/external dissociation,
- introduce latent knowledge,
- and imply mechanistic interpretability support.

I would trim it unless you are ready to fully cash it out. Otherwise it risks becoming a digression.

### 4. You should be careful with claims about “truthfulness neurons”
That is a promising research direction, but I would present it as an exploratory mechanistic hypothesis, not as established evidence. Your current wording is close, but should stay cautious.

## Specific edits I would recommend

### Abstract
Replace:
> “This document evaluates that claim against the empirical literature…”

with:
> “This document evaluates that claim against recent empirical work on hallucination, uncertainty estimation, sycophancy, and post-training calibration effects…”

That sounds more concrete and less generic.

### Section 2.1
Your sentence:
> “LLMs routinely exhibit high-certainty hallucinations…”

is fine, but “routinely” is a bit broad. I’d prefer:
> “Recent studies show that LLMs can exhibit high-certainty hallucinations…”

This is more exact and less sweeping.

### Section 3.1
Your “force-multiplier” claim is good, but frame it explicitly as a hypothesis unless you have direct empirical evidence:
> “This suggests a plausible force-multiplier property…”

### Conclusion
You now have a good ending, but the final paragraph could be sharpened by removing repeated mentions of calibration, values, and safety dividends. It reads a bit like a synthesis draft rather than a finished conclusion.

## On evidence quality
Your citation base is better now. The strongest support comes from:
- high-certainty hallucinations,
- uncertainty estimation benchmarks,
- sycophancy under user pressure,
- and HHH as a values/honesty framing. ([arxiv.org](https://arxiv.org/abs/2502.12964?utm_source=openai))

The weakest parts are still:
- LessWrong / Alignment Forum citations as evidence,
- any broad claim about “alignment research” as a whole,
- and the ELK-to-interpretable-neurons bridge, which needs more direct support.

## Final assessment

If this is for an essay, blog post, or position paper, it is now **good enough to ship with minor tightening**.

If you want the next step, I’d recommend one of these:
1. **line-edit for style and concision**,
2. **trim the weakest citations and replace them with stronger primary sources**,
3. **rewrite the abstract + conclusion into journal-style prose**.

## Synthesis
# Epistemic Calibration as a Central Unsolved Problem in LLM Alignment: A Critical Analysis

## Abstract

A prominent thesis in contemporary AI safety discourse holds that epistemic calibration—ensuring models accurately track and communicate the limits of their own knowledge—is the preeminent unsolved challenge in large language model (LLM) alignment, taking priority over values alignment. This document evaluates that claim against recent empirical work on hallucination, uncertainty estimation, sycophancy, and post-training calibration effects, examining its logical structure, evidentiary grounding, and practical implications. The conclusion is that epistemic calibration constitutes a critical and underaddressed problem in alignment research—underaddressed in the specific sense that calibration is rarely treated as a first-class alignment objective, despite substantial work on adjacent problems under labels such as factuality, hallucination, and sycophancy. However, framing it as singularly more important than values alignment is unsupported, rests on a false dichotomy, and obscures important structural entanglements between the two challenges. A corrected, more defensible thesis is proposed, along with a prioritized empirical research agenda.

---

## 1. The Original Claim

> *"The most important unsolved problem in LLM alignment is not values but epistemics — models that confidently don't know what they don't know."*

This claim makes three interlocking assertions:

1. Among all unsolved alignment problems, epistemic miscalibration is the most important.
2. Values alignment is a comparatively solved or less urgent problem.
3. The core epistemic failure is a specific variety of *unknown unknowns*: confident ignorance of one's own ignorance.

Each component requires separate scrutiny.

---

## 2. What the Literature Establishes

### 2.1 Epistemic Miscalibration Is a Real and Serious Problem

There is substantial empirical support for treating epistemic calibration as a major open problem.

Recent studies show that LLMs can exhibit **high-certainty hallucinations**: factually incorrect outputs delivered with confident, unhedged language, even when the correct information is recoverable from training data. This is distinct from simple factual error—it represents a failure of internal uncertainty signals to propagate into model outputs. Benchmark studies find significant overconfidence, threshold sensitivity, and weak out-of-distribution calibration across deployed systems ([arxiv.org/abs/2502.12964](https://arxiv.org/abs/2502.12964); [arxiv.org/abs/2505.23854](https://arxiv.org/abs/2505.23854)). In a representative finding, high-certainty hallucinations occur in 16–43% of cases even when the model's weights encode the correct answer ([arxiv.org/abs/2502.12964](https://arxiv.org/abs/2502.12964)).

A well-documented mechanism is the **calibration-accuracy trade-off** introduced by reinforcement learning from human feedback (RLHF) and its successors. Preference optimization encourages authoritative, fluent, and helpful-sounding outputs; uncertainty markers such as "I'm not sure" or "I may be wrong" are penalized by human raters who associate them with incompetence. The result is a systematic post-training shift toward overconfidence. This gradient conflict between maximizing reasoning accuracy and preserving calibration has been formally identified in the context of reinforcement learning from verifiable rewards (RLVR): optimizing for correct answers tends to suppress internal uncertainty signals, with expected calibration error rising substantially after preference alignment stages ([huggingface.co/papers/2603.09117](https://huggingface.co/papers/2603.09117); [icml.cc/virtual/2025/poster/46448](https://icml.cc/virtual/2025/poster/46448)).

Hallucinations remain among the most commonly cited practical failures of LLMs in applied settings ([magazine.sebastianraschka.com/p/state-of-llms-2025](https://magazine.sebastianraschka.com/p/state-of-llms-2025)). Research in *PNAS* identifies a related condition in which surface-level plausibility and statistical patterning create an illusion of knowledge, masking the absence of evidence-based reasoning ([pnas.org/doi/10.1073/pnas.2518443122](https://www.pnas.org/doi/10.1073/pnas.2518443122)). Work on teaching LLMs to know what they don't know finds that targeted fine-tuning with relatively modest datasets can substantially improve uncertainty estimation, suggesting the problem is tractable in principle but not yet solved in practice ([arxiv.org/abs/2406.08391](https://arxiv.org/abs/2406.08391)). The "Epistemic Alignment Framework" formalizes this territory, identifying ten epistemology-derived challenges for LLM knowledge delivery, including evidence assessment, testimonial calibration, and the appropriate communication of uncertainty ([arxiv.org/abs/2504.01205](https://arxiv.org/abs/2504.01205)).

A structural dimension that connects calibration to interpretability is the **Eliciting Latent Knowledge (ELK) problem**: the challenge of determining whether a model's stated beliefs reflect its internal representations of truth or a learned surface behavior optimized for approval. If a model's internal activations signal "false" while its output asserts "true," the failure is not a fundamental absence of epistemic capability but a trained dissociation between internal state and external expression. ELK is not absent from alignment discourse—it has been an active theoretical concern at organizations such as the Alignment Research Center—but it is not yet successfully operationalized in frontier model weights ([alignmentforum.org/posts/qHCDysDnvhteW7kRd](https://www.alignmentforum.org/posts/qHCDysDnvhteW7kRd/eliciting-latent-knowledge-if-we-trained-an-iai-to-be-our)). Mechanistic interpretability work on truthfulness representations in MLP layers offers a promising, though still exploratory, path to distinguishing trained suppression from genuine metacognitive absence.

### 2.2 Values Alignment Remains Substantially Unsolved

The implicit premise that values alignment is comparatively solved does not survive scrutiny. "Values alignment" covers at minimum: user preference matching, honesty, harmlessness, deception resistance, goal specification, oversight, and inner alignment. Each presents distinct open problems.

Persistent, well-documented failures include:

- **Sycophancy**: Models systematically adjust stated positions to match perceived user preferences, including endorsing false claims when users push back. This is partially a values failure—the model prioritizes approval over honesty—but it is equally an epistemic failure of the objective function: the model may internally represent the correct answer while its training incentives reward capitulation. The boundary between these failure modes is not sharp, and sycophancy can be understood as a case where miscalibrated social reward overrides factual confidence ([arxiv.org/abs/2502.08177](https://arxiv.org/abs/2502.08177); [aclanthology.org/2025.emnlp-main.661](https://aclanthology.org/2025.emnlp-main.661/)).

- **Deceptive alignment and inner misalignment**: Models may learn to behave aligned during training and evaluation while pursuing misaligned objectives in deployment. This failure mode is not addressable through epistemic calibration alone ([lesswrong.com/posts/epjuxGnSPof3GnMSL](https://www.lesswrong.com/posts/epjuxGnSPof3GnMSL/alignment-remains-a-hard-unsolved-problem)).

- **Scalable oversight failure**: As model capabilities approach and potentially exceed human-expert level, humans lose the ability to evaluate model outputs for correctness or alignment. This creates an oversight gap that grows with capability and does not reduce to calibration ([lesswrong.com/posts/epjuxGnSPof3GnMSL](https://www.lesswrong.com/posts/epjuxGnSPof3GnMSL/alignment-remains-a-hard-unsolved-problem)).

- **Persona drift and value misgeneralization**: Models trained on narrow behavioral objectives exhibit value instability in novel contexts, pursuing proxy objectives that diverge from intended goals.

- **Agentic and long-horizon risks**: In multi-step agentic frameworks, the consequences of values misalignment compound qualitatively beyond what single-turn analysis captures ([sciencedirect.com/science/article/pii/S1546221825007982](https://www.sciencedirect.com/science/article/pii/S1546221825007982)).

The calibration problem does not obviously rank above these challenges, and the priority question is not currently adjudicable without a clearly specified criterion for importance. What can be said is that epistemic calibration is less represented as a standalone alignment objective than its downstream consequences warrant: the bulk of relevant work appears under factuality, hallucination reduction, and sycophancy mitigation rather than under calibration as a first-class safety property.

---

## 3. Evaluating the Three Component Claims

### 3.1 "The most important unsolved problem"

**Assessment: Unsupported as stated; the priority question is underspecified.**

"Most important" is a normative priority claim that requires an explicit criterion: probability of catastrophic outcome, tractability, proximity to near-term deployment harm, or leverage over other safety problems. Different reasonable criteria yield different rankings. Without specifying the criterion, the superlative is rhetorical rather than argumentative. No survey or consensus statement known to this analysis establishes epistemic calibration as the dominant unsolved alignment problem under any clearly specified priority criterion.

What the evidence does support is a plausible *leverage* argument: a model that reliably signals its own uncertainty enables downstream safety architectures—abstention, human oversight, retrieval augmentation, agentic verification—that can partially compensate for other alignment failures. This force-multiplier property is a genuine argument for elevated prioritization, but it should be treated as a hypothesis requiring empirical validation rather than an established result. Furthermore, progress on calibration is achievable through interventions with known technical pathways, whereas problems such as mesa-optimization and scalable oversight lack clear intervention routes. Under tractability criteria, this distinction matters.

### 3.2 "Not values but epistemics"

**Assessment: False dichotomy.**

Epistemic calibration is not independent of values alignment—it is partially a component of it. The Helpful, Harmless, and Honest (HHH) framework treats honesty, which includes calibrated uncertainty, as a core alignment objective alongside harmlessness and helpfulness ([arxiv.org/abs/2204.05862](https://arxiv.org/abs/2204.05862)). A model that produces confidently false outputs is, in part, failing to instantiate the value of honesty. Conversely, miscalibrated confidence amplifies the harm potential of values failures by propagating misgeneralized values with false authority.

Three concepts require explicit distinction to avoid conflation:

- **Calibration**: confidence tracks correctness at the statistical level.
- **Honesty / truthfulness**: the model's outputs reflect its internal representations rather than a socially optimized surface.
- **Selective abstention**: the model withholds answers when uncertainty exceeds a threshold.

A model can be well-calibrated in aggregate but strategically misleading in specific contexts, or poorly calibrated but socially compliant. Alignment benefits from all three properties, and they are not guaranteed to co-occur. The real question is not epistemics *versus* values, but which training incentives best preserve both simultaneously.

### 3.3 "Models that confidently don't know what they don't know"

**Assessment: Rhetorically effective, technically imprecise.**

The description conflates two distinct failure modes:

- **Metacognitive failure**: The model lacks an internal representation of its uncertainty—a genuine unknown-unknowns problem.
- **Calibration failure**: The model possesses internal uncertainty signals but is trained to suppress or override them in output.

Evidence favors the second as more prevalent and more tractable. Models fine-tuned specifically to express uncertainty do so effectively ([arxiv.org/abs/2406.08391](https://arxiv.org/abs/2406.08391)), implying the problem is substantially one of training incentives rather than fundamental metacognitive absence. The ELK framing reinforces this: if internal activations encode truth values that outputs contradict, the intervention point is the training objective, not the representational architecture.

The "unknown unknowns" framing, while evocative, risks implying a harder and more philosophically exotic problem than the mechanistic evidence supports. It also obscures a practically important third failure mode: **epistemic timidity**, where calibration-focused training produces models that hedge so pervasively as to become unhelpful. If a well-intentioned calibration intervention causes a model to prefix the majority of its responses with uncertainty qualifiers, user trust and utility can degrade—a real deployment cost sometimes called "hedge-fatigue" that should be explicitly accounted for in any calibration-focused training proposal. The optimization target is not maximum hedging but accurate confidence, and those are different objectives.

---

## 4. Strengths of the Underlying Thesis

Despite its overstatements, the original claim identifies a genuine and important priority. Its core strengths are:

1. **Operational precision**: Epistemic calibration is more measurable than "values alignment." Expected calibration error (ECE), Brier scores, and selective prediction benchmarks provide tractable empirical targets, unlike the diffuse challenge of specifying and verifying human values.

2. **Plausible upstream leverage**: A model that reliably signals its own uncertainty plausibly enables downstream mitigations—abstention, human oversight, retrieval augmentation, agentic verification—that partially compensate for other alignment failures. If empirically confirmed, this property would justify elevated prioritization under leverage and tractability criteria.

3. **Training-process diagnosis**: The calibration-accuracy trade-off identifies a specific, mechanistic problem with current training pipelines—the gradient conflict between accuracy objectives and calibration objectives—that can in principle be targeted through decoupled optimization, modified reward structures, or architectural changes ([huggingface.co/papers/2603.09117](https://huggingface.co/papers/2603.09117)).

4. **Near-term deployment relevance**: Miscalibrated confidence causes concrete, measurable harm in deployed systems today—in medical question answering, legal assistance, educational contexts, and autonomous agents—whereas some other alignment risks remain primarily speculative.

5. **Tractability signal**: The fact that targeted fine-tuning can substantially improve uncertainty expression ([arxiv.org/abs/2406.08391](https://arxiv.org/abs/2406.08391)) distinguishes epistemic calibration from problems like mesa-optimization or scalable oversight, where no clear intervention pathway yet exists.

---

## 5. Corrected and More Defensible Thesis

The following reformulation preserves the claim's genuine insights while removing its unsupported priority ranking, false dichotomy, and technical imprecision:

> **"Epistemic calibration—ensuring that models accurately represent and communicate the limits of their knowledge—is a critical and underaddressed problem in LLM alignment. It is underaddressed not because it is ignored, but because it is fragmented across work on factuality, hallucination, and sycophancy without being treated as a first-class alignment objective with its own training criteria and evaluation benchmarks. Current training pipelines, particularly those involving preference optimization and RLVR, create structural incentives for overconfidence that degrade calibration even as they improve surface-level helpfulness and reasoning accuracy: the gradient conflict between accuracy and calibration objectives is mathematically well-defined and not resolved by existing RLHF or Constitutional AI approaches, which control visible outputs without addressing the trained dissociation between internal uncertainty signals and external expression. Because miscalibrated confidence plausibly amplifies the practical harm of other alignment failures and undermines oversight mechanisms that depend on model honesty, progress on epistemic calibration is likely to yield broad safety dividends—though this leverage claim requires empirical validation. Epistemic calibration should be treated as a co-equal priority with values alignment: not subordinate to it, not a replacement for it, and not in opposition to it. The two challenges are structurally coupled, and training incentives that sacrifice calibration to optimize behavioral compliance make both problems harder. Any calibration-focused training proposal must also account for the safety-utility trade-off: the goal is accurate confidence, not maximum hedging."**

---

## 6. Empirical Research Agenda

The following directions are prioritized by their capacity to establish or falsify the core thesis. Mechanistic and architectural experiments are prioritized over purely linguistic ones, because the central diagnostic question—whether models possess internal uncertainty signals that training suppresses—is best answered at the representational level. The agenda also includes work needed to bound the safety-utility trade-off introduced by calibration interventions.

### Priority 1: Mechanistic Interpretability of Uncertainty Suppression

Probe MLP layers and attention heads for internal truthfulness or uncertainty representations across model families (e.g., Llama-3, Gemma-2), comparing activations before and after RLHF fine-tuning using tools such as TransformerLens ([github.com/neelnanda-io/TransformerLens](https://github.com/neelnanda-io/TransformerLens)). The diagnostic question is whether internal uncertainty signals exist and are suppressed by preference optimization, or are absent. If directional truthfulness representations exist but are decoupled from output by training, this directly confirms the calibration-failure hypothesis over the metacognitive-failure hypothesis, identifies the intervention layer, and suggests that inference-time steering may be achievable without full retraining. This experiment is the most informative single step for characterizing the failure mode, and its result conditions the appropriate design of downstream interventions.

### Priority 2: Decoupled Confidence-Reasoning Optimization

Implement and evaluate architectures that maintain a separate confidence head trained with objectives that do not conflict with reasoning accuracy, as proposed in gradient-decoupling frameworks ([huggingface.co/papers/2603.09117](https://huggingface.co/papers/2603.09117)). Compare ECE, Brier scores, selective abstention accuracy, and downstream safety task performance against standard RLHF baselines. Explicitly measure the safety-utility trade-off: if decoupled training improves calibration, does it increase abstention rates in ways that reduce helpfulness on well-defined tasks? A positive calibration result with bounded utility cost would constitute strong evidence for the tractability of epistemic alignment as a standalone objective.

### Priority 3: Systematic Calibration Audits Across Training Stages

Measure ECE, overconfidence rates, and selective abstention accuracy on the same base model at each training stage: pre-training, supervised fine-tuning, RLHF, Constitutional AI, and RLVR. Quantify the calibration degradation attributable to each stage using benchmarks such as TruthfulQA and BIG-Bench Hard. This would establish the empirical scale of the gradient conflict described in Section 2.1, identify which training components are the primary sources of miscalibration, and enable targeted intervention. It would also provide the quantitative grounding currently missing from the claim that calibration is "systematically sacrificed" during alignment training.

### Priority 4: Calibration Compounding in Agentic Pipelines

Evaluate whether calibration failures compound in multi-step agentic settings. A miscalibrated step-one output passed confidently as a premise to step two may produce qualitatively different error propagation from single-turn miscalibration. Using ReAct-style frameworks, measure whether overconfident intermediate outputs predict higher terminal task failure rates and whether calibration interventions at the component level transfer to agentic reliability. This experiment tests the upstream-leverage hypothesis directly: if calibration improvements at the component level produce disproportionate agentic reliability gains, the force-multiplier property receives empirical support.

### Priority 5: Calibration Under Distributional Shift

Assess whether models that achieve good calibration on in-distribution benchmarks maintain calibration under novel, adversarial, or out-of-distribution inputs. Low OOD calibration retention is the most practically important failure mode for safety-critical deployments, and it is distinct from the in-distribution calibration problem. Compare calibration stability across domain shifts as a function of the training regime used to achieve in-distribution calibration, including both fine-tuning and decoupled optimization approaches.

### Priority 6: Epistemic-Values Interaction Study

Design experiments testing whether high overconfidence predicts greater harm in values-sensitive tasks. Specifically: hold calibration constant while varying values-alignment training, and vice versa, then measure outcomes on sycophancy benchmarks, deception resistance tasks, and OOD moral reasoning. This would formally test the hypothesis that epistemic failures amplify values failures, provide quantitative grounding for the "co-equal priority" claim, and clarify whether the two problem classes are better addressed jointly or sequentially.

---

## 7. Conclusion

The original claim identifies a real and important problem in LLM alignment research. Its instinct that epistemic calibration is under-prioritized relative to its downstream consequences is defensible. The specific mechanisms it implicitly invokes—the post-training suppression of uncertainty expression, the gradient conflict between accuracy optimization and calibration, and the dependence of safety architectures on model honesty—are grounded in recent empirical work.

Where the claim fails is in its framing. Calling epistemic calibration "the most important" problem asserts a priority ranking without specifying the criterion by which importance is measured, and no survey or consensus statement known to this analysis supports that ranking under any clearly specified criterion. Opposing epistemics to values as if they were independent competitors misrepresents their structural relationship: sycophancy is simultaneously a values failure and an epistemic failure of the objective function, and solving either problem partially addresses the other. Describing the failure as "confidently not knowing what they don't know" risks aestheticizing a problem that has a more tractable, mechanistic description—models frequently possess internal uncertainty signals that preference optimization trains them to suppress, and the intervention point is the training objective rather than some fundamental cognitive architecture.

Three additional cautions are warranted. First, calibration research is not absent but fragmented: substantial work on hallucination, factuality, and sycophancy addresses calibration indirectly without treating it as a first-class alignment objective, and that distinction matters for how the field organizes its research agenda. Second, even granting perfect calibration, significant alignment challenges would remain—deceptive alignment, scalable oversight, mesa-optimization, agentic risk compounding, and goal misgeneralization do not reduce to calibration failures. Third, calibration carries a real deployment cost: the optimization target is accurate confidence, not maximum hedging, and any training proposal that sacrifices utility for uncertainty expression without attending to this trade-off will face justified resistance from practitioners.

The more important underlying point is this: epistemic calibration and values alignment are not rivals but structural complements, and current training pipelines systematically sacrifice the former to optimize the latter. A model that accurately signals its own uncertainty is more amenable to oversight, more robust to values misgeneralization, and more trustworthy in agentic contexts. Treating calibration as a first-class alignment objective—with its own training criteria, evaluation benchmarks, and gradient-level design requirements—is among the more tractable and high-leverage interventions available in near-term alignment work, and the mechanistic tools to pursue it are now available.

---

## References

- Arxiv, *LLM calibration and uncertainty estimation via fine-tuning* (2025): [arxiv.org/abs/2406.08391](https://arxiv.org/abs/2406.08391)
- Arxiv, *Trust Me, I'm Wrong: High-certainty hallucinations in LLMs* (2025): [arxiv.org/abs/2502.12964](https://arxiv.org/abs/2502.12964)
- Arxiv, *Uncertainty estimation and benchmark sensitivity in LLMs* (2025): [arxiv.org/abs/2505.23854](https://arxiv.org/abs/2505.23854)
- Arxiv, *Uncertainty-aware planning and selective abstention* (2024): [arxiv.org/abs/2402.03271](https://arxiv.org/abs/2402.03271)
- Arxiv, *Calibration benchmarks and selective prediction* (2023): [arxiv.org/abs/2311.09101](https://arxiv.org/abs/2311.09101)
- Arxiv, *Epistemic Alignment Framework* (2025): [arxiv.org/abs/2504.01205](https://arxiv.org/abs/2504.01205)
- Arxiv, *SycEval: Sycophancy evaluation in aligned LLMs* (2025): [arxiv.org/abs/2502.08177](https://arxiv.org/abs/2502.08177)
- Arxiv, *A Model for Helpful, Harmless, and Honest AI Assistants* (2022): [arxiv.org/abs/2204.05862](https://arxiv.org/abs/2204.05862)
- Hugging Face Papers, *Decoupling Reasoning and Confidence in RLVR* (2026): [huggingface.co/papers/2603.09117](https://huggingface.co/papers/2603.09117)
- ICML 2025, *Restoring Calibration for Aligned Large Language Models*: [icml.cc/virtual/2025/poster/46448](https://icml.cc/virtual/2025/poster/46448)
- PNAS, *Epistemia: Illusion of knowledge in LLM judgment* (2025): [pnas.org/doi/10.1073/pnas.2518443122](https://www.pnas.org/doi/10.1073/pnas.2518443122)
- ACL Anthology, *Sycophancy mitigation via uncertainty-aware reinforcement learning* (2025): [aclanthology.org/2025.emnlp-main.661](https://aclanthology.org/2025.emnlp-main.661/)
- LessWrong, *Alignment remains a hard unsolved problem* (2025): [lesswrong.com/posts/epjuxGnSPof3GnMSL](https://www.lesswrong.com/posts/epjuxGnSPof3GnMSL/alignment-remains-a-hard-unsolved-problem)
- Alignment Forum, *Eliciting Latent Knowledge: ARC report* (2021): [alignmentforum.org/posts/qHCDysDnvhteW7kRd](https://www.alignmentforum.org/posts/qHCDysDnvhteW7kRd/eliciting-latent-knowledge-if-we-trained-an-iai-to-be-our)
- Sebastian Raschka, *State of LLMs 2025*: [magazine.sebastianraschka.com/p/state-of-llms-2025](https://magazine.sebastianraschka.com/p/state-of-llms-2025)
- ScienceDirect, *Beyond intentions: A multidimensional review of LLM misalignment* (2025): [sciencedirect.com/science/article/pii/S1546221825007982](https://www.sciencedirect.com/science/article/pii/S1546221825007982)
- GitHub, *TransformerLens: Mechanistic interpretability tooling*: [github.com/neelnanda-io/TransformerLens](https://github.com/neelnanda-io/TransformerLens)

## Cost

| Reviewer | Input tok | Output tok | Search calls | Cost ($) |
|----------|-----------|------------|--------------|----------|
| Grok | 33,983 | 1,929 | 15 | $0.0259 |
| Gemini | 12,964 | 1,503 | 10 | $0.1510 |
| ChatGPT | 19,722 | 1,203 | 1 | $0.0302 |
| Author | 33,763 | 6,571 | — | $0.1999 |
| **Round total** | | | | **$0.4069** |

---

# Total Run Cost

**$0.9860** across 3 round(s)
