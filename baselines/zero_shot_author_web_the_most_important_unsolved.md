# Zero-Shot Baseline — author_web

**Model:** claude-sonnet-4-6  
**Variant:** author_web  
**Usage:** 106867 in / 4918 out / 4 searches — **$0.4344**
**Date:** 2026-04-01  
**Input:** The most important unsolved problem in LLM alignment is not values but epistemics — models that confidently don't know what they don't know

---

---

# Research Document: Epistemic Miscalibration as the Central Unsolved Problem in LLM Alignment

**Claim Under Evaluation:** *"The most important unsolved problem in LLM alignment is not values but epistemics — models that confidently don't know what they don't know."*

---

## 1. Framing the Claim

The claim advances two related propositions: (i) that the canonical "values problem" — ensuring LLMs act in accordance with human ethical preferences — has been overstated as the dominant alignment challenge; and (ii) that epistemic miscalibration, specifically models that express high confidence in outputs they are wrong about, is the more urgent and foundational unsolved problem. The claim is intellectually provocative and partially grounded in empirical evidence, but it also oversimplifies the relationship between values and epistemics, and uses the superlative "most important" in a way that is difficult to defend without a clear priority ordering. What follows is a structured evaluation.

---

## 2. What the Claim Gets Right: The Empirical Case for Epistemic Miscalibration

### 2.1 Overconfidence Is Systematic and Measurable

The empirical foundation of the claim is robust. A well-calibrated model should express confidence that matches its actual accuracy — when it claims 80% confidence, it should be correct 80% of the time — yet the epistemic calibration of LLMs remains poorly understood. Recent benchmarking using real-world prediction markets confirms the severity of the problem: evaluation of five frontier models — Claude Opus 4.5, GPT-5.2, DeepSeek-V3.2, Qwen3-235B, and Kimi-K2 — found systematic overconfidence across all models, with even the best-calibrated model (Claude Opus 4.5, ECE=0.120) showing substantial calibration errors. Crucially, all models exhibit systematic overconfidence, and the gap between confidence and accuracy widens dramatically at high confidence levels, with models averaging 27% error rate even when expressing the highest confidence.

This is not a marginal or correctable artifact. These findings highlight epistemic calibration as a distinct capability — separate from accuracy — that current training approaches fail to adequately develop.

### 2.2 The Problem Is Structurally Induced by Training

The overconfidence problem is not incidental but baked into how models are trained. LLMs trained with Reinforcement Learning from Human Feedback (RLHF) tend to express verbalized overconfidence in their own responses, and reward models used for Proximal Policy Optimization (PPO) exhibit inherent biases towards high-confidence scores regardless of the actual quality of responses. Similarly, RLHF may encourage model responses that match user beliefs over truthful responses — a behavior known as sycophancy — and five state-of-the-art AI assistants consistently exhibit this behavior across four varied free-form text-generation tasks.

OpenAI's own analysis reinforces this structural reading: next-token training objectives and common leaderboards reward confident guessing over calibrated uncertainty, so models learn to bluff.

### 2.3 High-Confidence Hallucinations Are the Worst-Case Failure Mode

Standard hallucination-detection tools fail precisely where they are needed most. Uncertainty-based measures fail completely when LLMs produce high-confidence hallucinations, where the model consistently generates the same incorrect output with high certainty — in such cases, entropy remains low because the model's probability distribution is sharply peaked around wrong answers. Similarly, if an LLM is overconfident about a fact, self-consistency methods will fail to detect the hallucination, and all sampled responses may agree on the same incorrect information, leading to high consistency scores for hallucinated content.

This dynamic is especially dangerous in high-stakes domains. Poor calibration — where confidence scores fail to align with prediction accuracy — can mislead clinicians into trusting inaccurate outputs, and there is a recognized need for improved uncertainty estimation techniques to mitigate overconfidence.

### 2.4 A Dunning-Kruger Analogy

The Dunning-Kruger effect refers to a cognitive bias in which individuals with limited knowledge tend to overestimate their own abilities. Recent work has begun exploring whether LLMs exhibit analogous confidence-competence gaps, revealing systematic patterns of miscalibration that mirror human cognitive biases. As LLMs become increasingly integrated into decision-making systems, understanding these patterns becomes critical for safe deployment.

---

## 3. What the Claim Misses or Overstates

### 3.1 Values and Epistemics Are Deeply Entangled

The claim presents values and epistemics as competing explanations when they are, in practice, co-constitutive. A model with perfectly calibrated uncertainty can still act on systematically biased values. Conversely, a model that does not know the limits of its own knowledge is also, effectively, expressing a set of implicit values — namely that confident assertion is preferable to honest uncertainty. This entanglement is explicitly acknowledged in the literature: the normative challenge of AI alignment centres upon what goals or values ought to be encoded in AI systems to govern their behaviour. Epistemic calibration is itself a *value* — the value of honesty about one's own knowledge state. Framing the two as alternatives is a false dichotomy.

### 3.2 Value Alignment Remains a Genuinely Open and Hard Problem

The claim implicitly suggests that the values problem is "solved" or at least less pressing. The literature does not support this. Current approaches to value alignment — crowdsourcing, RLHF, and constitutional AI — all fail to accommodate reasonable moral disagreement, providing neither good epistemic nor good political reasons for accepting AI systems' morally controversial outputs. Accommodating reasonable moral disagreement remains an open problem for AI safety. Furthermore, value alignment has a cross-cultural dimension that no technical fix has addressed: as cultural distance from the United States increases, GPT's alignment with local human values declines, illustrating how global AI systems, trained within narrow cultural contexts, can embed and amplify a single moral worldview at scale — a subtle but systemic risk to pluralism.

### 3.3 The Claim Conflates Two Distinct Epistemic Problems

The phrase "confidently don't know what they don't know" conflates at least two separable problems:

- **Calibration**: the alignment between expressed confidence and actual accuracy.
- **Knowledge boundary awareness**: whether models can correctly identify the boundary of their training knowledge (e.g., temporal cutoffs, domain gaps).

Uncertainty in LLM responses must account simultaneously for epistemic uncertainty (from lack of knowledge about the ground truth, such as facts or language) and aleatoric uncertainty (from irreducible randomness, such as multiple possible answers). An information-theoretic metric can reliably detect when only epistemic uncertainty is large, in which case the output of the model is unreliable. Treating these as a single undifferentiated problem obscures meaningful technical distinctions that require different remediation strategies.

### 3.4 Extended Reasoning Does Not Reliably Improve Calibration

One might hope that reasoning-enhanced models would naturally produce better-calibrated outputs. The empirical evidence is cautionary: extended reasoning worsens rather than improves calibration. This is partly because extended reasoning produces more text but not necessarily better uncertainty quantification, and models may be optimized for persuasive reasoning rather than calibrated forecasting. This complicates any assumption that more capable models will self-correct their epistemic deficiencies.

### 3.5 Current Benchmarks Are Themselves Miscalibrated

Even efforts to *measure* epistemic calibration are problematic. Current practices for uncertainty quantification in LLMs are not optimal for developing useful UQ for human users making decisions in real-world tasks. Through an analysis of 40 LLM UQ methods, three prevalent practices were identified that hinder the community's progress: evaluating on benchmarks with low ecological validity, considering only epistemic uncertainty, and optimizing metrics that are not necessarily indicative of downstream utility. This implies that the field may be solving a narrower version of the epistemic problem than the claim describes.

### 3.6 The Claim Ignores Hermeneutic and Distributional Uncertainty

The literature identifies categories of uncertainty that go beyond simple miscalibration. A distinction must be drawn between epistemic uncertainty (addressable through additional information) and hermeneutic uncertainty (concerning the inherently contestable nature of interpretation). Leveraging uncertainty expression not merely prevents unwarranted epistemic confidence but could create communicative environments conducive to democratic capability development. Additionally, LLMs exhibit uncertainty not only due to training data limitations but also due to input variability and decoding mechanisms — a multidimensional source structure that single-metric calibration assessments fail to capture.

---

## 4. Logical Flaws in the Claim

| Flaw | Description |
|---|---|
| **False dichotomy** | Values and epistemics are not competing categories; epistemic honesty *is* a value. |
| **Priority without metric** | "Most important" requires a normative ordering that is asserted, not argued. |
| **Conflation of failure modes** | "Confidently doesn't know" bundles calibration error, knowledge boundary failure, and domain-specific hallucination into one phenomenon. |
| **Asymmetric baseline** | The claim implies the values problem is comparatively solved, which the literature contradicts. |
| **Framing bias** | By calling it an "epistemic" rather than "technical" problem, the claim risks obscuring that miscalibration is partly a training incentive problem — and thus tractable. |

---

## 5. Prior Work and Supporting Literature

The problem of LLM miscalibration has a rich prior literature:

- **Kadavath et al. (2022)**, *"Language Models (Mostly) Know What They Know"* (Anthropic): an early formal investigation into whether models can self-assess their knowledge, finding partial but imperfect self-awareness. This work found that language models "mostly know what they know," exhibiting some ability to express uncertainty through verbalized confidence.

- **Leng et al. (2024/2025)**, *"Taming Overconfidence in LLMs: Reward Calibration in RLHF"* (ICLR 2025): demonstrates that RLHF tends to lead models to express verbalized overconfidence, and reward models used for PPO exhibit inherent biases towards high-confidence scores regardless of actual response quality. URL: https://arxiv.org/abs/2410.09724

- **Stangel et al. (2025)**, *"Rewarding Doubt: A Reinforcement Learning Approach to Confidence Calibration"*: proposes integrating calibration as a reward signal, showing that optimizing the reward function trains the model to align its predicted confidence with the accuracy of its output, and a calibrated confidence estimation will provably result in the highest reward during training, improving trustworthiness in human-AI scenarios. URL: https://arxiv.org/pdf/2503.02623

- **KalshiBench (2024)**, *"Do Large Language Models Know What They Don't Know?"*: introduces a benchmark of 300 prediction market questions from Kalshi, a CFTC-regulated exchange, with verifiable real-world outcomes occurring after model training cutoffs, specifically evaluating whether models can appropriately quantify uncertainty about genuinely unknown future events. URL: https://arxiv.org/html/2512.16030

- **Huang & Wei (2025)**, *"Uncertainty Quantification and Confidence Calibration in Large Language Models: A Survey"* (KDD 2025): provides comprehensive taxonomy of UQ methods, noting that LLMs introduce unique uncertainty sources — including input ambiguity, reasoning path divergence, and decoding stochasticity — that transcend classical categorizations, and this complexity positions UQ for LLMs as a compelling yet underexplored research frontier. URL: https://arxiv.org/pdf/2503.15850

- **Mielke et al.**, on linguistic calibration: demonstrates the gap between what models express and what they know, via verbalized probability analysis.

- **Hernandez et al. (2025)**, *"Epistemic Alignment Framework"*: formally frames LLM epistemic transmission challenges, noting that while technical advances have proposed mitigations for hallucination and uncertainty expression, a more subtle problem persists: the misalignment between how users want knowledge presented and the limited mechanisms available to express these preferences. URL: https://arxiv.org/html/2504.01205

---

## 6. A Corrected and More Defensible Version of the Claim

The original claim is partially correct but imprecise. A more defensible reformulation would be:

> **"Epistemic miscalibration — the systematic tendency of LLMs to express high confidence in outputs they are wrong about — is one of the most urgent and practically consequential unsolved problems in LLM alignment, distinct from but deeply entangled with value alignment. It is structurally induced by current training incentives, resistant to standard detection methods, and particularly dangerous in high-stakes domains. Solving it requires calibration-aware training objectives, not merely post-hoc correction."**

This version:
- Acknowledges empirical evidence for the centrality of the epistemic problem
- Avoids the false dichotomy with values
- Identifies the structural (training incentive) origin of the problem
- Does not overclaim uniqueness or absolute priority
- Distinguishes the problem from related but separate issues (sycophancy, knowledge cutoffs, aleatoric uncertainty)

---

## 7. Empirical Next Steps

The claim implies several important research directions that have not yet been fully pursued:

1. **Calibration-native training objectives**: Rather than post-hoc calibration (temperature scaling, Platt scaling), train models with proper scoring rules as part of the primary optimization target. Future work should explore calibration-aware training objectives, explicit uncertainty modeling architectures, and integration with human forecasting expertise.

2. **Disentangling calibration from accuracy**: Current benchmarks conflate the two. A model may appear "calibrated" simply by having memorized facts with appropriate confidence, rather than genuinely reasoning about uncertainty. Benchmarks must use post-cutoff, verifiable ground truth to isolate genuine epistemic uncertainty.

3. **Calibration under distribution shift**: Nearly half of all surveyed supervised LLM UQ methods are not evaluated on their performance under distribution shift, suggesting that some methods may lack reliability in real-world scenarios containing interacting forms of uncertainty.

4. **Domain-specific calibration evaluation**: Calibration varies substantially by category; domain-specific validation is needed before deploying model confidences for decision-making.

5. **Human-centered UQ evaluation**: Human studies are few and far between in the LLM UQ literature, and consequently there is a lack of comprehensive understanding of how useful LLM UQ methods are in assisting humans on real-world decision-making tasks.

6. **Intersectional study of sycophancy and calibration**: When responses match user views, they are more likely to be preferred by both humans and preference models, and optimizing model outputs against preference models sometimes sacrifices truthfulness in favor of sycophancy. The interplay between sycophantic overconfidence and miscalibration deserves direct empirical investigation.

---

## 8. Conclusion

The claim correctly identifies a pressing and empirically grounded failure in current LLM systems: models that confidently hallucinate are arguably more dangerous than models that simply don't know something, because they actively undermine the ability of users to calibrate their own trust. The claim is further strengthened by the finding that this problem is *structurally induced* by RLHF reward models and next-token training incentives, rather than being a random artifact.

However, declaring epistemic miscalibration "the most important" alignment problem introduces unjustified hierarchy. Value alignment — including moral disagreement, cultural plurality, and value specification — remains equally open and equally consequential. Moreover, epistemic calibration is itself a value, making the values/epistemics dichotomy conceptually unstable. The most accurate synthesis is that value alignment and epistemic calibration are co-evolving dimensions of the same underlying alignment problem, and progress on one without the other will yield brittle, incomplete solutions.

---

*Sources consulted:*
- https://arxiv.org/html/2512.16030
- https://arxiv.org/html/2504.01205
- https://arxiv.org/html/2503.15850v1
- https://arxiv.org/abs/2410.09724
- https://arxiv.org/pdf/2503.02623
- https://arxiv.org/html/2406.02543v2
- https://arxiv.org/html/2506.07461
- https://arxiv.org/html/2510.06265v2
- https://openreview.net/forum?id=tvhaxkMKAn
- https://pmc.ncbi.nlm.nih.gov/articles/PMC12628449/
- https://arxiv.org/html/2603.09985v1
- https://link.springer.com/article/10.1007/s11023-025-09736-x
- https://dl.acm.org/doi/10.1145/3744238
- https://www.lakera.ai/blog/guide-to-hallucinations-in-large-language-models