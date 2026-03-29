"""
Smoke tests — validates that each provider's API key, model name, and web search
config are correct. Each test streams a short response and prints the first tokens.

Run: uv run python test_apis.py
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

PROMPT = "In one sentence, what happened in AI news today? (use web search)"

PASS = "\033[92m PASS\033[0m"
FAIL = "\033[91m FAIL\033[0m"


def test_grok():
    print("── Grok", end=" ", flush=True)
    try:
        from xai_sdk.sync.client import Client as XAIClient
        from xai_sdk.chat import user, system
        from xai_sdk.tools import web_search
        from cpar import MODEL_GROK

        client = XAIClient(api_key=os.getenv("XAI_API_KEY"))
        chat = client.chat.create(
            model=MODEL_GROK,
            messages=[system("You are a helpful assistant."), user(PROMPT)],
            tools=[web_search()],
        )
        tokens = []
        for _response, chunk in chat.stream():
            if chunk.content:
                tokens.append(chunk.content)
            if len("".join(tokens)) > 80:
                break
        preview = "".join(tokens)[:80]
        print(f"({MODEL_GROK}){PASS} — '{preview}...'")
        return True
    except Exception as e:
        print(f"{FAIL} — {e}")
        return False


def test_gemini():
    print("── Gemini", end=" ", flush=True)
    try:
        from google import genai as google_genai
        from google.genai import types as google_types
        from cpar import MODEL_GEMINI

        client = google_genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        chat = client.chats.create(
            model=MODEL_GEMINI,
            config=google_types.GenerateContentConfig(
                tools=[google_types.Tool(google_search=google_types.GoogleSearch())],
            ),
        )
        tokens = []
        for chunk in chat.send_message_stream(PROMPT):
            if chunk.text:
                tokens.append(chunk.text)
            if len("".join(tokens)) > 80:
                break
        preview = "".join(tokens)[:80]
        print(f"({MODEL_GEMINI}){PASS} — '{preview}...'")
        return True
    except Exception as e:
        print(f"{FAIL} — {e}")
        return False


def test_chatgpt():
    print("── ChatGPT", end=" ", flush=True)
    try:
        from openai import OpenAI
        from cpar import MODEL_CHATGPT

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        tokens = []
        with client.responses.stream(
            model=MODEL_CHATGPT,
            input=[{"role": "user", "content": PROMPT}],
            tools=[{"type": "web_search"}],
        ) as stream:
            for event in stream:
                if event.type == "response.output_text.delta":
                    tokens.append(event.delta)
                if len("".join(tokens)) > 80:
                    break
        preview = "".join(tokens)[:80]
        print(f"({MODEL_CHATGPT}){PASS} — '{preview}...'")
        return True
    except Exception as e:
        print(f"{FAIL} — {e}")
        return False


def test_claude():
    print("── Claude", end=" ", flush=True)
    try:
        import anthropic
        from cpar import MODEL_CLAUDE

        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        tokens = []
        with client.messages.stream(
            model=MODEL_CLAUDE,
            max_tokens=64,
            messages=[{"role": "user", "content": "Say 'Claude online' and nothing else."}],
        ) as stream:
            for text in stream.text_stream:
                tokens.append(text)
                if len("".join(tokens)) > 40:
                    break
        preview = "".join(tokens)[:80]
        print(f"({MODEL_CLAUDE}){PASS} — '{preview}...'")
        return True
    except Exception as e:
        print(f"{FAIL} — {e}")
        return False


def test_convergence_judge():
    print("── Convergence judge", end=" ", flush=True)
    try:
        from openai import OpenAI
        from cpar import MODEL_CHATGPT, CONVERGENCE_JUDGE_PROMPT

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        prompt = CONVERGENCE_JUDGE_PROMPT.format(
            n=3,
            reviews="### Grok\nLooks good.\n\n### Gemini\nMinor issues only.\n\n### ChatGPT\nReady to ship.",
        )
        response = client.chat.completions.create(
            model=MODEL_CHATGPT,
            max_completion_tokens=256,
            messages=[{"role": "user", "content": prompt}],
        )
        import json, re
        raw = response.choices[0].message.content.strip()
        raw_json = re.sub(r"^```json\s*|^```\s*|```$", "", raw, flags=re.MULTILINE).strip()
        data = json.loads(raw_json)
        assert "converged" in data and "reason" in data
        print(f"({MODEL_CHATGPT}){PASS} — converged={data['converged']} | {data['reason'][:60]}")
        return True
    except Exception as e:
        print(f"{FAIL} — {e}")
        return False


if __name__ == "__main__":
    print(f"\nCPAR API smoke tests\n{'─' * 40}")
    results = [
        test_grok(),
        test_gemini(),
        test_chatgpt(),
        test_claude(),
        test_convergence_judge(),
    ]
    print("─" * 40)
    passed = sum(results)
    total = len(results)
    status = "\033[92mAll passed\033[0m" if passed == total else f"\033[91m{total - passed} failed\033[0m"
    print(f"{status} ({passed}/{total})\n")
    sys.exit(0 if passed == total else 1)
