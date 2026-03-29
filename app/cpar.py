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

from prompts import REVIEWER_SYSTEM, AUTHOR_SYSTEM, CONVERGENCE_JUDGE_PROMPT

# Model configuration — update here to switch versions
MODEL_GROK = "grok-4-1-fast"
MODEL_GEMINI = "gemini-3-flash-preview"
MODEL_CHATGPT = "gpt-5.4-mini"
MODEL_CLAUDE = "claude-sonnet-4-6"


def stream_grok(document: str, history: list[dict], api_key: str | None = None) -> Iterator[str]:
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
    for _response, chunk in chat.stream():
        if chunk.content:
            yield chunk.content


def stream_gemini(document: str, history: list[dict], api_key: str | None = None) -> Iterator[str]:
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
    for chunk in chat.send_message_stream(document):
        yield chunk.text or ""


def stream_chatgpt(document: str, history: list[dict], api_key: str | None = None) -> Iterator[str]:
    client = OpenAI(api_key=api_key or OPENAI_API_KEY)
    with client.responses.stream(
        model=MODEL_CHATGPT,
        instructions=REVIEWER_SYSTEM,
        input=history + [{"role": "user", "content": document}],
        tools=[{"type": "web_search"}],
    ) as stream:
        for event in stream:
            if event.type == "response.output_text.delta":
                yield event.delta


def stream_author(document: str, reviews: dict, history: list[dict], api_key: str | None = None) -> Iterator[str]:
    review_text = "\n\n".join(f"### {name}\n{text}" for name, text in reviews.items())
    user_message = f"## Document\n{document}\n\n## Reviews\n{review_text}"
    client = anthropic.Anthropic(api_key=api_key or ANTHROPIC_API_KEY)
    messages = history + [{"role": "user", "content": user_message}]
    with client.messages.stream(
        model=MODEL_CLAUDE,
        max_tokens=4096,
        system=AUTHOR_SYSTEM,
        messages=messages,
    ) as stream:
        for text in stream.text_stream:
            yield text


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
