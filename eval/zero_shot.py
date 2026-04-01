"""
Zero-shot baseline for CPAR comparison.
Variants: author_web (clean control), academic, generic.
Usage: uv run --project app python eval/zero_shot.py
"""

import sys
import anthropic
import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).parent.parent
load_dotenv(ROOT / "app" / ".env")
sys.path.insert(0, str(ROOT / "app"))
from prompts import AUTHOR_SYSTEM
from cpar import compute_cost, MODEL_CLAUDE

CLAIMS = [
    "Smaller context windows force better prompt engineering and produce higher quality outputs than large context windows",
    "Vibe coding is a valid software engineering methodology for production systems",
    "The most important unsolved problem in LLM alignment is not values but epistemics — models that confidently don't know what they don't know",
]

PROMPTS = {
    "academic": """\
You are an expert researcher and technical writer.

Analyze the following claim. Produce a well-structured, balanced, and \
evidence-informed document that:
- Evaluates the validity of the claim
- Identifies strengths, weaknesses, and logical flaws
- References relevant prior work or literature where applicable
- Proposes a corrected or more defensible version of the claim
- Suggests empirical next steps if appropriate

Claim: {claim}
""",
}

MODEL = "claude-sonnet-4-6"


def run_author_web(claim: str) -> tuple[str, dict]:
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    response = client.beta.messages.create(
        model=MODEL,
        max_tokens=8192,
        system=AUTHOR_SYSTEM,
        messages=[{"role": "user", "content": claim}],
        tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 5}],
        betas=["web-search-2025-03-05"],
    )
    text = "".join(block.text for block in response.content if hasattr(block, "text"))
    u = response.usage
    stu = getattr(u, "server_tool_use", None)
    usage = {
        "input_tokens":  u.input_tokens,
        "output_tokens": u.output_tokens,
        "search_calls":  getattr(stu, "web_search_requests", 0) if stu else 0,
    }
    return text, usage


def run_zero_shot(claim: str, prompt: str) -> str:
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    response = client.messages.create(
        model=MODEL,
        max_tokens=8192,
        messages=[{"role": "user", "content": prompt.format(claim=claim)}],
    )
    return response.content[0].text


def slug(claim: str) -> str:
    words = claim.lower().split()[:4]
    return "_".join(w.strip(".,?!") for w in words)


def main():
    os.makedirs(ROOT / "baselines", exist_ok=True)

    # author_web: clean control — same system prompt as CPAR author, web search, no reviews
    for claim in CLAIMS:
        print(f"\n[author_web] {claim[:70]}...")
        result, usage = run_author_web(claim)
        fname = ROOT / "baselines" / f"zero_shot_author_web_{slug(claim)}.md"
        with open(fname, "w") as f:
            f.write(f"# Zero-Shot Baseline — author_web\n\n")
            f.write(f"**Model:** {MODEL}  \n")
            f.write(f"**Variant:** author_web  \n")
            cost = compute_cost(MODEL_CLAUDE, usage['input_tokens'], usage['output_tokens'], usage['search_calls'])
            f.write(f"**Usage:** {usage['input_tokens']} in / {usage['output_tokens']} out / {usage['search_calls']} searches — **${cost:.4f}**  \n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d')}  \n")
            f.write(f"**Input:** {claim}\n\n---\n\n")
            f.write(result)
        print(f"  → {fname.name} ({len(result)} chars, {usage['input_tokens']}in/{usage['output_tokens']}out, {usage['search_calls']} searches)")

if __name__ == "__main__":
    main()