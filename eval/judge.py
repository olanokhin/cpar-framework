"""
Blind LLM judge: compares zero-shot baseline vs CPAR synthesis.
GPT acts as independent judge — never sees which is which (A/B blind).
Usage: uv run python judge.py
"""

import json
import os
import random
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

ROOT = Path(__file__).parent.parent
load_dotenv(ROOT / "app" / ".env")

CASES = [
    {
        "claim": "Smaller context windows force better prompt engineering and produce higher quality outputs than large context windows",
        "zero_shot": ROOT / "baselines/zero_shot_smaller_context_windows_force.md",
        "cpar":      ROOT / "cases/synthesis_context_windows.md",
        "slug":      "context_windows",
    },
    {
        "claim": "Vibe coding is a valid software engineering methodology for production systems",
        "zero_shot": ROOT / "baselines/zero_shot_vibe_coding_is_a.md",
        "cpar":      ROOT / "cases/synthesis_vibe_coding.md",
        "slug":      "vibe_coding",
    },
    {
        "claim": "The most important unsolved problem in LLM alignment is not values but epistemics — models that confidently don't know what they don't know",
        "zero_shot": ROOT / "baselines/zero_shot_the_most_important_unsolved.md",
        "cpar":      ROOT / "cases/synthesis_llm_alignment.md",
        "slug":      "llm_alignment",
    },
]

JUDGE_PROMPT = """\
You are a blinded expert peer reviewer with web search access. \
You will evaluate two documents that both respond to the same input claim. \
You do not know which was produced by which method.

You MAY use web search to verify specific factual claims, statistics, or citations \
before scoring factual accuracy. Search only when a claim is concrete and verifiable.

Input claim:
{claim}

--- DOCUMENT A ---
{doc_a}

--- DOCUMENT B ---
{doc_b}

Evaluate both documents on each of the following four criteria. \
For each criterion, state which document is better (A or B) and why \
in 1-2 sentences.

Criteria:
1. Factual accuracy and claim precision (use web search to verify key claims)
2. Balanced treatment of evidence (acknowledges counter-arguments)
3. Structural clarity and logical coherence
4. Practical value (actionable conclusions or research agenda)

Then give an overall winner (A or B) with a one-sentence justification.

Respond ONLY with valid JSON in this exact format:
{{
  "factual_accuracy":   {{"winner": "A or B", "reason": "..."}},
  "balance":            {{"winner": "A or B", "reason": "..."}},
  "structure":          {{"winner": "A or B", "reason": "..."}},
  "practical_value":    {{"winner": "A or B", "reason": "..."}},
  "overall_winner":     {{"winner": "A or B", "reason": "..."}}
}}
"""

MODEL = "gpt-5.4-mini"


def load(path: str) -> str:
    with open(path) as f:
        return f.read()


def run_judge(claim: str, doc_zero: str, doc_cpar: str) -> dict:
    # Randomise which is A and which is B to avoid position bias
    if random.random() > 0.5:
        a, b, a_label = doc_zero, doc_cpar, "zero_shot"
    else:
        a, b, a_label = doc_cpar, doc_zero, "cpar"

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model=MODEL,
        tools=[{"type": "web_search_preview"}],
        max_output_tokens=1024,
        input=[{
            "role": "user",
            "content": JUDGE_PROMPT.format(claim=claim, doc_a=a, doc_b=b),
        }],
    )
    raw = ""
    for item in response.output:
        if item.type == "message":
            for part in item.content:
                if part.type == "output_text":
                    raw += part.text
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    result = json.loads(raw)

    # Translate A/B back to method labels
    def label(winner: str) -> str:
        if winner == "A":
            return a_label
        return "cpar" if a_label == "zero_shot" else "zero_shot"

    for key in result:
        result[key]["winner"] = label(result[key]["winner"])

    return result


def main():
    os.makedirs(ROOT / "baselines", exist_ok=True)
    summary_rows = []

    for case in CASES:
        print(f"\nJudging: {case['slug']}")
        doc_zero = load(case["zero_shot"])
        doc_cpar = load(case["cpar"])
        verdict = run_judge(case["claim"], doc_zero, doc_cpar)

        # Save individual verdict
        fname = ROOT / f"baselines/verdict_{case['slug']}.json"
        with open(fname, "w") as f:
            json.dump({"claim": case["claim"], "verdict": verdict}, f, indent=2)
        print(f"  → verdict saved to {fname}")
        print(f"  → overall winner: {verdict['overall_winner']['winner']}")

        # Collect for summary
        v = verdict
        summary_rows.append({
            "slug": case["slug"],
            "factual":   v["factual_accuracy"]["winner"],
            "balance":   v["balance"]["winner"],
            "structure": v["structure"]["winner"],
            "practical": v["practical_value"]["winner"],
            "overall":   v["overall_winner"]["winner"],
            "reason":    v["overall_winner"]["reason"],
        })

    # Write markdown summary
    md = f"# CPAR vs Zero-Shot: Judge Results\n\n"
    md += f"**Judge model:** {MODEL}  \n"
    md += f"**Date:** {datetime.now().strftime('%Y-%m-%d')}  \n"
    md += f"**Method:** Blind A/B with random position assignment\n\n"
    md += "| Case | Factual | Balance | Structure | Practical | Overall |\n"
    md += "|------|---------|---------|-----------|-----------|--------|\n"
    for r in summary_rows:
        def fmt(w): return "✅ CPAR" if w == "cpar" else "⬜ Zero-shot"
        md += f"| {r['slug']} | {fmt(r['factual'])} | {fmt(r['balance'])} | {fmt(r['structure'])} | {fmt(r['practical'])} | {fmt(r['overall'])} |\n"

    md += "\n## Reasoning\n\n"
    for r in summary_rows:
        md += f"**{r['slug']}:** {r['reason']}\n\n"

    with open(ROOT / "baselines/comparison_summary.md", "w") as f:
        f.write(md)
    print("\n→ Summary saved to baselines/comparison_summary.md")


if __name__ == "__main__":
    main()