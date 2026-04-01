import json
from typing import Iterator
from dotenv import load_dotenv
import os

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
XAI_API_KEY = os.getenv("XAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

from openai import OpenAI
import anthropic
from google import genai as google_genai
from google.genai import types as google_types
from xai_sdk.sync.client import Client as XAIClient
from xai_sdk.chat import user as xai_user, system as xai_system, assistant as xai_assistant
from xai_sdk.tools import web_search as xai_web_search, x_search as xai_x_search

from prompts import REVIEWER_SYSTEM, AUTHOR_SYSTEM, REVIEW_PREFIX, CONVERGENCE_JUDGE_PROMPT

# Model configuration — update here to switch versions
MODEL_GROK = "grok-4-1-fast"
MODEL_GEMINI = "gemini-3-flash-preview"
MODEL_CHATGPT = "gpt-5.4-mini"
MODEL_CLAUDE = "claude-sonnet-4-6"

# Pricing per 1M tokens (input/output) and per 1k search calls.
# VERIFY against provider sites before each run.
PRICING_DATE = "2026-04-01"
PRICING = {
    MODEL_CLAUDE:  {"input": 3.00,  "output": 15.00, "search": 10.0},
    MODEL_GROK:    {"input": 0.20,  "output": 6.00, "search": 0.50},
    MODEL_GEMINI:  {"input": 0.50, "output": 3.00,  "search": 14.0},
    MODEL_CHATGPT: {"input": 0.75,  "output": 4.50,  "search": 10.0},
}


def compute_cost(model: str, input_tokens: int, output_tokens: int, search_calls: int = 0) -> float:
    p = PRICING.get(model, {"input": 0.0, "output": 0.0, "search": 0.0})
    return (
        (input_tokens * p["input"] + output_tokens * p["output"]) / 1_000_000
        + search_calls * p["search"] / 1_000
    )


def stream_grok(document: str, history: list[dict], api_key: str | None = None, usage_out: dict | None = None) -> Iterator[str]:
    client = XAIClient(api_key=api_key or XAI_API_KEY)
    messages = [xai_system(REVIEWER_SYSTEM)]
    for msg in history:
        if msg["role"] == "user":
            messages.append(xai_user(msg["content"]))
        else:
            messages.append(xai_assistant(msg["content"]))
    messages.append(xai_user(document))
    chat = client.chat.create(
        model=MODEL_GROK,
        messages=messages,
        tools=[xai_web_search(), xai_x_search()],
    )
    last_resp = None
    for _response, chunk in chat.stream():
        if chunk.content:
            yield chunk.content
        last_resp = _response
    if usage_out is not None and last_resp is not None:
        u = getattr(last_resp, "usage", None)
        if u:
            usage_out["input_tokens"]  = getattr(u, "prompt_tokens", 0)
            usage_out["output_tokens"] = getattr(u, "completion_tokens", 0)
            usage_out["search_calls"]  = len(getattr(u, "server_side_tools_used", []))


def stream_gemini(document: str, history: list[dict], api_key: str | None = None, usage_out: dict | None = None) -> Iterator[str]:
    client = google_genai.Client(api_key=api_key or GOOGLE_API_KEY)
    gemini_history = []
    for msg in history:
        role = "model" if msg["role"] == "assistant" else "user"
        gemini_history.append(google_types.Content(role=role, parts=[google_types.Part(text=msg["content"])]))
    chat = client.chats.create(
        model=MODEL_GEMINI,
        config=google_types.GenerateContentConfig(
            system_instruction=REVIEWER_SYSTEM,
            tools=[google_types.Tool(google_search=google_types.GoogleSearch())],
        ),
        history=gemini_history,
    )
    last_chunk = None
    for chunk in chat.send_message_stream(document):
        yield chunk.text or ""
        last_chunk = chunk
    if usage_out is not None and last_chunk is not None:
        m = getattr(last_chunk, "usage_metadata", None)
        if m:
            usage_out["input_tokens"]  = getattr(m, "prompt_token_count", 0)
            usage_out["output_tokens"] = getattr(m, "candidates_token_count", 0)
        # Search queries are on candidates[0].grounding_metadata.web_search_queries
        search_calls = 0
        for cand in (getattr(last_chunk, "candidates", None) or []):
            gm = getattr(cand, "grounding_metadata", None)
            if gm:
                search_calls = len(getattr(gm, "web_search_queries", None) or [])
                break
        usage_out["search_calls"] = search_calls


def stream_chatgpt(document: str, history: list[dict], api_key: str | None = None, usage_out: dict | None = None) -> Iterator[str]:
    client = OpenAI(api_key=api_key or OPENAI_API_KEY)
    search_calls = 0
    with client.responses.stream(
        model=MODEL_CHATGPT,
        instructions=REVIEWER_SYSTEM,
        input=history + [{"role": "user", "content": document}],
        tools=[{"type": "web_search"}],
    ) as stream:
        for event in stream:
            if event.type == "response.output_text.delta":
                yield event.delta
            elif event.type == "response.web_search_call.completed":
                search_calls += 1
        if usage_out is not None:
            final = stream.get_final_response()
            u = getattr(final, "usage", None)
            if u:
                usage_out["input_tokens"]  = getattr(u, "input_tokens", 0)
                usage_out["output_tokens"] = getattr(u, "output_tokens", 0)
                usage_out["search_calls"]  = search_calls


def stream_author(document: str, reviews: dict, history: list[dict], api_key: str | None = None, usage_out: dict | None = None) -> Iterator[str]:
    review_text = "\n\n".join(f"### {name}\n{text}" for name, text in reviews.items())
    user_message = f"{REVIEW_PREFIX}\n\n## Document\n{document}\n\n## Reviews\n{review_text}"
    client = anthropic.Anthropic(api_key=api_key or ANTHROPIC_API_KEY)
    messages = history + [{"role": "user", "content": user_message}]
    with client.messages.stream(
        model=MODEL_CLAUDE,
        max_tokens=8192,
        system=AUTHOR_SYSTEM,
        messages=messages,
    ) as stream:
        for text in stream.text_stream:
            yield text
        if usage_out is not None:
            msg = stream.get_final_message()
            usage_out["input_tokens"]  = msg.usage.input_tokens
            usage_out["output_tokens"] = msg.usage.output_tokens


def check_convergence(reviews: dict, iteration: int, api_key: str | None = None) -> tuple[bool, str]:
    if iteration < 3:
        return False, "Too early to converge."
    review_text = "\n\n".join(f"### {name}\n{text}" for name, text in reviews.items())
    prompt = CONVERGENCE_JUDGE_PROMPT.format(n=iteration, reviews=review_text)
    # Use GPT as independent judge — avoids Claude judging its own synthesis
    client = OpenAI(api_key=api_key or OPENAI_API_KEY)
    response = client.chat.completions.create(
        model=MODEL_CHATGPT,
        max_completion_tokens=256,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = response.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()
    try:
        data = json.loads(raw)
        return bool(data["converged"]), str(data["reason"])
    except Exception:
        return False, "Could not parse convergence judgment."


def make_histories() -> dict:
    return {"grok": [], "gemini": [], "chatgpt": []}


def append_to_history(histories: dict, reviewer_key: str, document: str, response: str) -> None:
    histories[reviewer_key].append({"role": "user", "content": document})
    histories[reviewer_key].append({"role": "assistant", "content": response})
