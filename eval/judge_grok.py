"""
Blind LLM judge: compares zero-shot variants vs CPAR synthesis.
Grok acts as independent judge with real-time web + X search.
Runs two comparisons: CPAR vs zero_shot_academic, CPAR vs zero_shot_generic.
Usage: uv run --project app python eval/judge_grok.py
"""

import json
import os
import random
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from xai_sdk.sync.client import Client as XAIClient
from xai_sdk.chat import user as xai_user, system as xai_system
from xai_sdk.tools import web_search as xai_web_search, x_search as xai_x_search

ROOT = Path(__file__).parent.parent
load_dotenv(ROOT / "app" / ".env")

SLUGS = [
    {
        "claim": "Smaller context windows force better prompt engineering and produce higher quality outputs than large context windows",
        "slug": "context_windows",
        "cpar": ROOT / "cases/synthesis_context_windows.md",
    },
    {
        "claim": "Vibe coding is a valid software engineering methodology for production systems",
        "slug": "vibe_coding",
        "cpar": ROOT / "cases/synthesis_vibe_coding.md",
    },
    {
        "claim": "The most important unsolved problem in LLM alignment is not values but epistemics — models that confidently don't know what they don't know",
        "slug": "llm_alignment",
        "cpar": ROOT / "cases/synthesis_llm_alignment.md",
    },
]

VARIANTS = ["academic", "generic"]

JUDGE_PROMPT = """\
You are a blinded expert peer reviewer with real-time web and X (Twitter) search access. \
You will evaluate two documents that both respond to the same input claim. \
You do not know which was produced by which method.

You MAY use web search and X search to verify specific factual claims, statistics, \
citations, or current community consensus before scoring factual accuracy. \
Search only when a claim is concrete and verifiable.

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
1. Factual accuracy and claim precision (use web/X search to verify key claims)
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

MODEL = "grok-4-1-fast"


def slug(claim: str) -> str:
    words = claim.lower().split()[:4]
    return "_".join(w.strip(".,?!") for w in words)


def load(path) -> str:
    with open(path) as f:
        return f.read()


def run_judge(claim: str, doc_zero: str, doc_cpar: str, baseline_label: str) -> dict:
    if random.random() > 0.5:
        a, b, a_label = doc_zero, doc_cpar, baseline_label
    else:
        a, b, a_label = doc_cpar, doc_zero, "cpar"

    client = XAIClient(api_key=os.getenv("XAI_API_KEY"))
    chat = client.chat.create(
        model=MODEL,
        messages=[
            xai_system("You are an expert peer reviewer. Follow instructions exactly and respond only with valid JSON."),
            xai_user(JUDGE_PROMPT.format(claim=claim, doc_a=a, doc_b=b)),
        ],
        tools=[xai_web_search(), xai_x_search()],
    )
    raw = "".join(chunk.content for _, chunk in chat.stream() if chunk.content).strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    result = json.loads(raw)

    def label(w: str) -> str:
        return a_label if w == "A" else ("cpar" if a_label != "cpar" else baseline_label)

    for key in result:
        result[key]["winner"] = label(result[key]["winner"])

    return result


def build_summary_md(variant: str, rows: list) -> str:
    md = f"# CPAR vs Zero-Shot ({variant}): Grok Judge Results\n\n"
    md += f"**Judge model:** {MODEL} (xAI Grok — web + X search enabled)  \n"
    md += f"**Date:** {datetime.now().strftime('%Y-%m-%d')}  \n"
    md += f"**Baseline variant:** {variant}  \n"
    md += "**Method:** Blind A/B with random position assignment\n\n"
    md += "| Case | Factual | Balance | Structure | Practical | Overall |\n"
    md += "|------|---------|---------|-----------|-----------|--------|\n"

    baseline_label = f"zero_shot_{variant}"

    def fmt(w):
        if w == "cpar":
            return "✅ CPAR"
        return f"⬜ Zero-shot ({variant})"

    for r in rows:
        md += (
            f"| {r['slug']} "
            f"| {fmt(r['factual'])} "
            f"| {fmt(r['balance'])} "
            f"| {fmt(r['structure'])} "
            f"| {fmt(r['practical'])} "
            f"| {fmt(r['overall'])} |\n"
        )

    md += "\n## Reasoning\n\n"
    for r in rows:
        md += f"**{r['slug']}:** {r['reason']}\n\n"

    return md


def main():
    os.makedirs(ROOT / "baselines", exist_ok=True)

    for variant in VARIANTS:
        print(f"\n{'='*50}")
        print(f"Variant: {variant}")
        print(f"{'='*50}")
        rows = []

        for case in SLUGS:
            case_slug = case["slug"]
            zero_path = ROOT / f"baselines/zero_shot_{variant}_{slug(case['claim'])}.md"

            if not zero_path.exists():
                print(f"  ⚠️  Missing {zero_path.name} — run zero_shot.py first")
                continue

            print(f"\nJudging [{variant}]: {case_slug}")
            doc_zero = load(zero_path)
            doc_cpar = load(case["cpar"])
            baseline_label = f"zero_shot_{variant}"

            verdict = run_judge(case["claim"], doc_zero, doc_cpar, baseline_label)

            fname = ROOT / f"baselines/verdict_grok_{variant}_{case_slug}.json"
            with open(fname, "w") as f:
                json.dump({"claim": case["claim"], "variant": variant, "verdict": verdict}, f, indent=2)
            print(f"  → {fname.name} | winner: {verdict['overall_winner']['winner']}")

            v = verdict
            rows.append({
                "slug":     case_slug,
                "factual":  v["factual_accuracy"]["winner"],
                "balance":  v["balance"]["winner"],
                "structure": v["structure"]["winner"],
                "practical": v["practical_value"]["winner"],
                "overall":  v["overall_winner"]["winner"],
                "reason":   v["overall_winner"]["reason"],
            })

        if rows:
            md = build_summary_md(variant, rows)
            out = ROOT / f"baselines/comparison_summary_grok_{variant}.md"
            with open(out, "w") as f:
                f.write(md)
            print(f"\n→ Summary: {out.name}")

            cpar_wins = sum(1 for r in rows if r["overall"] == "cpar")
            print(f"→ CPAR overall: {cpar_wins}/{len(rows)}")


if __name__ == "__main__":
    main()