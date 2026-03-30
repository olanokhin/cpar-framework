"""
Zero-shot baseline for CPAR comparison.
Runs two variants: academic (structured) and generic (minimal).
Usage: uv run --project app python eval/zero_shot.py
"""

import anthropic
import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).parent.parent
load_dotenv(ROOT / "app" / ".env")

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
    "generic": """\
Analyze the following claim and produce an improved version.

Claim: {claim}
""",
}

MODEL = "claude-sonnet-4-6"


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
    for variant, prompt in PROMPTS.items():
        for claim in CLAIMS:
            print(f"\n[{variant}] {claim[:70]}...")
            result = run_zero_shot(claim, prompt)
            fname = ROOT / "baselines" / f"zero_shot_{variant}_{slug(claim)}.md"
            with open(fname, "w") as f:
                f.write(f"# Zero-Shot Baseline — {variant}\n\n")
                f.write(f"**Model:** {MODEL}  \n")
                f.write(f"**Variant:** {variant}  \n")
                f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d')}  \n")
                f.write(f"**Input:** {claim}\n\n---\n\n")
                f.write(result)
            print(f"  → {fname.name} ({len(result)} chars)")


if __name__ == "__main__":
    main()