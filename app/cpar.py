import json
import os
import re
from typing import Iterator

import anthropic
import google.generativeai as genai
from dotenv import load_dotenv
from openai import OpenAI

from prompts import AUTHOR_SYSTEM, CONVERGENCE_JUDGE_PROMPT, REVIEWER_SYSTEM

load_dotenv()

CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-6")
GROK_MODEL = os.getenv("GROK_MODEL", "grok-4")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-pro")
GPT_MODEL = os.getenv("GPT_MODEL", "gpt-5")

REVIEWERS = ["Grok", "Gemini", "ChatGPT"]


def doc_prompt(document: str, round_n: int) -> str:
    return f"Round {round_n}. Document under review:\n\n{document}"


def _stream_openai_compatible(client: OpenAI, model: str, history: list, user_msg: str) -> Iterator[str]:
    messages = [{"role": "system", "content": REVIEWER_SYSTEM}] + history + [
        {"role": "user", "content": user_msg}
    ]
    stream = client.chat.completions.create(model=model, messages=messages, stream=True)
    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


def stream_grok(history: list, user_msg: str) -> Iterator[str]:
    client = OpenAI(base_url="https://api.x.ai/v1", api_key=os.getenv("XAI_API_KEY"))
    yield from _stream_openai_compatible(client, GROK_MODEL, history, user_msg)


def stream_gpt(history: list, user_msg: str) -> Iterator[str]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    yield from _stream_openai_compatible(client, GPT_MODEL, history, user_msg)


def stream_gemini(history: list, user_msg: str) -> Iterator[str]:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel(GEMINI_MODEL, system_instruction=REVIEWER_SYSTEM)
    contents = [
        {"role": "model" if m["role"] == "assistant" else "user", "parts": [m["content"]]}
        for m in history
    ] + [{"role": "user", "parts": [user_msg]}]
    for chunk in model.generate_content(contents, stream=True):
        if chunk.text:
            yield chunk.text


REVIEWER_STREAMS = {"Grok": stream_grok, "Gemini": stream_gemini, "ChatGPT": stream_gpt}


def stream_author(document: str, reviews: dict, round_n: int) -> Iterator[str]:
    labelled = "\n\n".join(f"### Review by {name}\n{text}" for name, text in reviews.items())
    user_msg = f"Current document:\n\n{document}\n\n---\n\nReviews (round {round_n}):\n\n{labelled}"
    client = anthropic.Anthropic()
    with client.messages.stream(
        model=CLAUDE_MODEL,
        max_tokens=8192,
        system=AUTHOR_SYSTEM,
        messages=[{"role": "user", "content": user_msg}],
    ) as stream:
        yield from stream.text_stream


def check_convergence(reviews: dict, round_n: int) -> tuple[bool, str]:
    if round_n < 3:
        return False, "Convergence check starts from round 3."
    labelled = "\n\n".join(f"### {name}\n{text}" for name, text in reviews.items())
    client = anthropic.Anthropic()
    resp = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=300,
        messages=[
            {"role": "user", "content": CONVERGENCE_JUDGE_PROMPT.format(n=round_n, reviews=labelled)}
        ],
    )
    text = resp.content[0].text
    match = re.search(r"\{.*\}", text, re.DOTALL)
    try:
        data = json.loads(match.group(0)) if match else {}
        return bool(data.get("converged")), str(data.get("reason", ""))
    except json.JSONDecodeError:
        return False, "Could not parse judge response."
