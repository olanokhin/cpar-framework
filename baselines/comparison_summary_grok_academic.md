# CPAR vs Zero-Shot (academic): Grok Judge Results

**Judge model:** grok-4-1-fast (xAI Grok — web + X search enabled)  
**Date:** 2026-03-30  
**Baseline variant:** academic  
**Method:** Blind A/B with random position assignment

| Case | Factual | Balance | Structure | Practical | Overall |
|------|---------|---------|-----------|-----------|--------|
| context_windows | ✅ CPAR | ✅ CPAR | ⬜ Zero-shot (academic) | ⬜ Zero-shot (academic) | ⬜ Zero-shot (academic) |
| vibe_coding | ✅ CPAR | ⬜ Zero-shot (academic) | ⬜ Zero-shot (academic) | ✅ CPAR | ✅ CPAR |
| llm_alignment | ⬜ Zero-shot (academic) | ⬜ Zero-shot (academic) | ⬜ Zero-shot (academic) | ⬜ Zero-shot (academic) | ⬜ Zero-shot (academic) |

## Reasoning

**context_windows:** Document B excels in rigorous academic analysis, logical decomposition, and forward-looking practicality, making it the stronger peer-reviewed response despite A's recency edge in citations.

**vibe_coding:** Document A excels in timeliness, precision to the vibe coding claim with verified recent evidence, practical engineering insights (e.g., ownership paradox, risks like prompt rot), and balanced nuance despite B's superior formal structure and explicit pro/con balance.

**llm_alignment:** Document B excels as a rigorous, balanced academic evaluation of the claim, providing precise analysis, verifiable evidence, and practical forward-looking insights superior to Document A's advocacy piece.

