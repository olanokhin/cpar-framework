"""
Probe tool: dumps raw usage/response structure from each provider after a web-search call.
Usage: uv run --project app python eval/probe_usage.py
"""
import sys
import os
import pprint
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).parent.parent
load_dotenv(ROOT / "app" / ".env")
sys.path.insert(0, str(ROOT / "app"))

QUERY = "What is the current version of Python?"


# ── Grok ──────────────────────────────────────────────────────────────────────
def probe_grok():
    print("\n" + "=" * 60)
    print("GROK")
    print("=" * 60)
    from xai_sdk.sync.client import Client as XAIClient
    from xai_sdk.chat import user as xai_user, system as xai_system
    from xai_sdk.tools import web_search as xai_web_search, x_search as xai_x_search
    from cpar import MODEL_GROK

    client = XAIClient(api_key=os.getenv("XAI_API_KEY"))
    chat = client.chat.create(
        model=MODEL_GROK,
        messages=[xai_system("Answer briefly."), xai_user(QUERY)],
        tools=[xai_web_search(), xai_x_search()],
    )
    last_resp = None
    for _response, chunk in chat.stream():
        last_resp = _response

    print("last_resp type:", type(last_resp))
    print("last_resp dir:", [a for a in dir(last_resp) if not a.startswith("_")])
    u = getattr(last_resp, "usage", None)
    print("usage:", u)
    if u:
        print("usage type:", type(u))
        print("usage dir:", [a for a in dir(u) if not a.startswith("_")])
        print("usage vars:", vars(u) if hasattr(u, "__dict__") else "no __dict__")
        pprint.pprint({a: getattr(u, a) for a in dir(u) if not a.startswith("_") and not callable(getattr(u, a))})


# ── Gemini ────────────────────────────────────────────────────────────────────
def probe_gemini():
    print("\n" + "=" * 60)
    print("GEMINI")
    print("=" * 60)
    from google import genai as google_genai
    from google.genai import types as google_types
    from cpar import MODEL_GEMINI

    client = google_genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    chat = client.chats.create(
        model=MODEL_GEMINI,
        config=google_types.GenerateContentConfig(
            system_instruction="Answer briefly.",
            tools=[google_types.Tool(google_search=google_types.GoogleSearch())],
        ),
    )
    last_chunk = None
    for chunk in chat.send_message_stream(QUERY):
        last_chunk = chunk

    print("last_chunk type:", type(last_chunk))
    print("last_chunk dir:", [a for a in dir(last_chunk) if not a.startswith("_")])

    m = getattr(last_chunk, "usage_metadata", None)
    print("\nusage_metadata:", m)
    if m:
        print("usage_metadata type:", type(m))
        pprint.pprint({a: getattr(m, a) for a in dir(m) if not a.startswith("_") and not callable(getattr(m, a))})

    gm = getattr(last_chunk, "grounding_metadata", None)
    print("\ngrounding_metadata:", gm)
    if gm:
        print("grounding_metadata type:", type(gm))
        pprint.pprint({a: getattr(gm, a) for a in dir(gm) if not a.startswith("_") and not callable(getattr(gm, a))})

    # Also check candidates
    cands = getattr(last_chunk, "candidates", None)
    if cands:
        for i, c in enumerate(cands):
            gm2 = getattr(c, "grounding_metadata", None)
            print(f"\ncandidates[{i}].grounding_metadata:", gm2)
            if gm2:
                pprint.pprint({a: getattr(gm2, a) for a in dir(gm2) if not a.startswith("_") and not callable(getattr(gm2, a))})


# ── ChatGPT ───────────────────────────────────────────────────────────────────
def probe_chatgpt():
    print("\n" + "=" * 60)
    print("CHATGPT")
    print("=" * 60)
    from openai import OpenAI
    from cpar import MODEL_CHATGPT

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    all_events = []
    with client.responses.stream(
        model=MODEL_CHATGPT,
        instructions="Answer briefly.",
        input=[{"role": "user", "content": QUERY}],
        tools=[{"type": "web_search"}],
    ) as stream:
        for event in stream:
            all_events.append(event.type)

        final = stream.get_final_response()

    print("Event types seen:", sorted(set(all_events)))
    print("\nfinal type:", type(final))
    print("final dir:", [a for a in dir(final) if not a.startswith("_")])

    u = getattr(final, "usage", None)
    print("\nusage:", u)
    if u:
        print("usage type:", type(u))
        pprint.pprint({a: getattr(u, a) for a in dir(u) if not a.startswith("_") and not callable(getattr(u, a))})

    # Inspect output items for search calls
    output = getattr(final, "output", None)
    if output:
        print(f"\noutput items ({len(output)}):")
        for item in output:
            item_type = getattr(item, "type", "?")
            print(f"  type={item_type}", end="")
            if item_type in ("web_search_call", "tool_call"):
                print(f"  → {vars(item) if hasattr(item, '__dict__') else item}", end="")
            print()


def probe_claude():
    print("\n" + "=" * 60)
    print("CLAUDE (ANTHROPIC) — no tools")
    print("=" * 60)
    import anthropic
    from cpar import MODEL_CLAUDE

    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    with client.messages.stream(
        model=MODEL_CLAUDE,
        max_tokens=256,
        system="Answer briefly.",
        messages=[{"role": "user", "content": QUERY}],
    ) as stream:
        for _ in stream.text_stream:
            pass
        msg = stream.get_final_message()

    print("msg.usage:", msg.usage)
    pprint.pprint({a: getattr(msg.usage, a) for a in dir(msg.usage) if not a.startswith("_") and not callable(getattr(msg.usage, a))})
    print("stop_reason:", msg.stop_reason)


def probe_claude_web_search():
    print("\n" + "=" * 60)
    print("CLAUDE (ANTHROPIC) — web_search_20250305")
    print("=" * 60)
    import anthropic
    from cpar import MODEL_CLAUDE

    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    response = client.beta.messages.create(
        model=MODEL_CLAUDE,
        max_tokens=1024,
        system="Answer briefly.",
        messages=[{"role": "user", "content": QUERY}],
        tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 5}],
        betas=["web-search-2025-03-05"],
    )

    print("usage:", response.usage)
    pprint.pprint({a: getattr(response.usage, a) for a in dir(response.usage) if not a.startswith("_") and not callable(getattr(response.usage, a))})
    print("\nstop_reason:", response.stop_reason)
    print("\ncontent block types:", [getattr(b, "type", "?") for b in response.content])


if __name__ == "__main__":
    probe_claude_web_search()
