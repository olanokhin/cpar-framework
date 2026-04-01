import atexit
import glob
import os
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed

import anthropic
import gradio as gr

from cpar import (
    stream_grok,
    stream_gemini,
    stream_chatgpt,
    stream_author,
    check_convergence,
    make_histories,
    append_to_history,
    compute_cost,
    MODEL_GROK,
    MODEL_GEMINI,
    MODEL_CHATGPT,
    MODEL_CLAUDE,
)

_ENV_KEYS = {
    "anthropic": os.getenv("ANTHROPIC_API_KEY", ""),
    "xai":       os.getenv("XAI_API_KEY", ""),
    "google":    os.getenv("GOOGLE_API_KEY", ""),
    "openai":    os.getenv("OPENAI_API_KEY", ""),
}
_SHOW_BYOK = not all(_ENV_KEYS.values())


def _cleanup_tmp():
    for f in glob.glob("/tmp/synthesis_round*.md") + glob.glob("/tmp/cpar_session_*.md"):
        try:
            os.unlink(f)
        except OSError:
            pass

atexit.register(_cleanup_tmp)

LABEL_GROK    = "Grok — Research Validator"
LABEL_GEMINI  = "Gemini — Creative Architect"
LABEL_CHATGPT = "ChatGPT — Devil's Advocate"


def render_history(completed_rounds: list) -> str:
    if not completed_rounds:
        return ""
    parts = []
    for r in completed_rounds:
        n = r["round"]
        round_cost = sum(r.get(k, {}).get("cost", 0.0) for k in ("grok_usage", "gemini_usage", "chatgpt_usage", "author_usage"))
        cost_label = f" — ${round_cost:.4f}" if round_cost else ""
        parts.append(
            f"<details><summary><strong>Round {n}</strong>{cost_label}</summary>"
            f"<h4>{LABEL_GROK}</h4><pre>{_esc(r['grok'])}</pre>"
            f"<h4>{LABEL_GEMINI}</h4><pre>{_esc(r['gemini'])}</pre>"
            f"<h4>{LABEL_CHATGPT}</h4><pre>{_esc(r['chatgpt'])}</pre>"
            f"<h4>Author Synthesis</h4><pre>{_esc(r['synthesis'])}</pre>"
            f"</details>"
        )
    return "\n".join(parts)


def _esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _cost_table(r: dict) -> str:
    rows = [
        ("Grok",    r.get("grok_usage",    {})),
        ("Gemini",  r.get("gemini_usage",  {})),
        ("ChatGPT", r.get("chatgpt_usage", {})),
        ("Author",  r.get("author_usage",  {})),
    ]
    lines = [
        "## Cost\n",
        "| Reviewer | Input tok | Output tok | Search calls | Cost ($) |",
        "|----------|-----------|------------|--------------|----------|",
    ]
    round_total = 0.0
    for name, u in rows:
        inp  = u.get("input_tokens", 0)
        out  = u.get("output_tokens", 0)
        srch = u.get("search_calls", 0) if name != "Author" else "—"
        cost = u.get("cost", 0.0)
        round_total += cost
        lines.append(f"| {name} | {inp:,} | {out:,} | {srch} | ${cost:.4f} |")
    lines.append(f"| **Round total** | | | | **${round_total:.4f}** |")
    return "\n".join(lines)


def export_session(completed_rounds: list) -> str:
    lines = []
    grand_total = 0.0
    for r in completed_rounds:
        lines.append(f"# Round {r['round']}\n")
        lines.append(f"## Grok\n{r['grok']}\n")
        lines.append(f"## Gemini\n{r['gemini']}\n")
        lines.append(f"## ChatGPT\n{r['chatgpt']}\n")
        lines.append(f"## Synthesis\n{r['synthesis']}\n")
        lines.append(_cost_table(r))
        round_cost = sum(r.get(k, {}).get("cost", 0.0) for k in ("grok_usage", "gemini_usage", "chatgpt_usage", "author_usage"))
        grand_total += round_cost
        lines.append("\n---\n")
    lines.append(f"# Total Run Cost\n\n**${grand_total:.4f}** across {len(completed_rounds)} round(s)\n")
    return "\n".join(lines)


def _with_cost(model: str, usage: dict) -> dict:
    if not usage:
        return {"input_tokens": 0, "output_tokens": 0, "search_calls": 0, "cost": 0.0}
    return {**usage, "cost": compute_cost(
        model,
        usage.get("input_tokens", 0),
        usage.get("output_tokens", 0),
        usage.get("search_calls", 0),
    )}


def _log(round_n: int, msg: str) -> None:
    import time
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] Round {round_n} | {msg}", flush=True)


def run_round(doc_input, state_doc, state_histories, state_author_history, state_round, state_completed_rounds,
              key_anthropic, key_xai, key_google, key_openai):
    def _key(ui_val, env_val):
        return (ui_val or "").strip() or env_val

    eff_anthropic = _key(key_anthropic, _ENV_KEYS["anthropic"])
    eff_xai       = _key(key_xai,       _ENV_KEYS["xai"])
    eff_google    = _key(key_google,    _ENV_KEYS["google"])
    eff_openai    = _key(key_openai,    _ENV_KEYS["openai"])

    missing = [name for name, val in [
        ("Anthropic (Claude)", eff_anthropic),
        ("xAI (Grok)", eff_xai),
        ("Google (Gemini)", eff_google),
        ("OpenAI (ChatGPT + Judge)", eff_openai),
    ] if not val]

    document = doc_input if state_round == 1 else state_doc
    round_n = state_round

    _log(round_n, "Starting round")

    # all_outputs order:
    # round_header, grok_acc, grok_out, gemini_acc, gemini_out, chatgpt_acc, chatgpt_out,
    # synthesis_acc, synthesis_out, advisory_out, download_btn,
    # history_html, state_doc, state_histories, state_author_history,
    # state_round, state_completed_rounds, run_btn

    # Initial: collapse all accordions with spinner labels, clear text
    yield (
        gr.update(value=f"## Round {round_n}", visible=True),   # round_header
        gr.update(label=f"⏳ {LABEL_GROK}", open=False),         # grok_acc
        gr.update(value=""),                                      # grok_out
        gr.update(label=f"⏳ {LABEL_GEMINI}", open=False),        # gemini_acc
        gr.update(value=""),                                      # gemini_out
        gr.update(label=f"⏳ {LABEL_CHATGPT}", open=False),       # chatgpt_acc
        gr.update(value=""),                                      # chatgpt_out
        gr.update(label="Author Synthesis", open=True),           # synthesis_acc
        gr.update(value=""),                                      # synthesis_out
        gr.update(value="", visible=False),                       # advisory_out
        gr.update(visible=False),                                 # download_btn
        render_history(state_completed_rounds),                   # history_html
        state_doc,
        state_histories,
        state_author_history,
        state_round,
        state_completed_rounds,
        gr.update(interactive=False),                             # run_btn
    )

    if missing:
        yield (
            gr.update(visible=False),
            gr.update(), gr.update(),
            gr.update(), gr.update(),
            gr.update(), gr.update(),
            gr.update(), gr.update(),
            gr.update(value=f"⚠️ Missing API keys: {', '.join(missing)}. Enter them in the API Keys section above.", visible=True),
            gr.update(visible=False),
            render_history(state_completed_rounds),
            state_doc,
            state_histories,
            state_author_history,
            state_round,
            state_completed_rounds,
            gr.update(interactive=True),
        )
        return

    # --- Parallel reviewers — checkmark appears as each one finishes ---
    results = {"grok": None, "gemini": None, "chatgpt": None}

    def _acc(key, label):
        v = results[key]
        if v is None:
            icon = "⏳"
        elif v.startswith(f"[{key} reviewer offline"):
            icon = "❌"
        else:
            icon = "✅"
        return gr.update(label=f"{icon} {label}", open=False)

    def _txt(key):
        return gr.update(value=results[key] if results[key] is not None else "")

    _log(round_n, "Dispatching 3 reviewers in parallel")
    import time as _time

    with ThreadPoolExecutor(max_workers=3) as ex:
        def _run(key, fn):
            t0 = _time.monotonic()
            _log(round_n, f"{key} → request sent")
            last_exc = None
            for attempt in range(1, 4):
                try:
                    result = "".join(fn())
                    _log(round_n, f"{key} → done ({_time.monotonic() - t0:.1f}s, {len(result)} chars)")
                    return result
                except Exception as e:
                    last_exc = e
                    wait = 2 ** attempt
                    _log(round_n, f"{key} → attempt {attempt} failed: {e}; retrying in {wait}s")
                    if attempt < 3:
                        _time.sleep(wait)
            _log(round_n, f"{key} → all retries exhausted: {last_exc}")
            return f"[{key} reviewer offline — skipped this round]"

        grok_usage, gemini_usage, chatgpt_usage = {}, {}, {}
        future_map = {
            ex.submit(_run, "grok",    lambda: stream_grok(document, state_histories["grok"], eff_xai, usage_out=grok_usage)): "grok",
            ex.submit(_run, "gemini",  lambda: stream_gemini(document, state_histories["gemini"], eff_google, usage_out=gemini_usage)): "gemini",
            ex.submit(_run, "chatgpt", lambda: stream_chatgpt(document, state_histories["chatgpt"], eff_openai, usage_out=chatgpt_usage)): "chatgpt",
        }
        for future in as_completed(future_map):
            key = future_map[future]
            results[key] = future.result()
            yield (
                gr.update(),
                _acc("grok", LABEL_GROK),    _txt("grok"),
                _acc("gemini", LABEL_GEMINI), _txt("gemini"),
                _acc("chatgpt", LABEL_CHATGPT), _txt("chatgpt"),
                gr.update(),  # synthesis_acc
                gr.update(),  # synthesis_out
                gr.update(),  # advisory_out
                gr.update(),  # download_btn
                gr.update(),  # history_html
                state_doc,
                state_histories,
                state_author_history,
                state_round,
                state_completed_rounds,
                gr.update(),
            )

    grok_text, gemini_text, chatgpt_text = results["grok"], results["gemini"], results["chatgpt"]

    offline = {k for k in ("grok", "gemini", "chatgpt") if results[k].startswith(f"[{k} reviewer offline")}

    if len(offline) >= 2:
        _log(round_n, f"Round aborted — {offline} offline")
        def _label(key, label):
            return gr.update(label=f"{'❌' if key in offline else '✅'} {label}")
        yield (
            gr.update(value=f"## Round {round_n}", visible=True),
            _label("grok", LABEL_GROK),      gr.update(value=grok_text),
            _label("gemini", LABEL_GEMINI),   gr.update(value=gemini_text),
            _label("chatgpt", LABEL_CHATGPT), gr.update(value=chatgpt_text),
            gr.update(label="Author Synthesis", open=True),
            gr.update(value=""),
            gr.update(value=f"⚠️ Round {round_n} aborted — {len(offline)}/3 reviewers offline. Check API keys and retry.", visible=True),
            gr.update(visible=False),
            render_history(state_completed_rounds),
            state_doc,
            state_histories,
            state_author_history,
            state_round,
            state_completed_rounds,
            gr.update(interactive=True),
        )
        return

    for key in ("grok", "gemini", "chatgpt"):
        if key not in offline:
            append_to_history(state_histories, key, document, results[key])

    _log(round_n, "All reviews collected — starting author synthesis")
    yield (
        gr.update(),
        gr.update(), gr.update(),
        gr.update(), gr.update(),
        gr.update(), gr.update(),
        gr.update(label="⏳ Author Synthesis", open=True),
        gr.update(value="Synthesizing..."),
        gr.update(),
        gr.update(),
        gr.update(),
        state_doc,
        state_histories,
        state_author_history,
        state_round,
        state_completed_rounds,
        gr.update(),
    )

    # --- Author synthesis (streaming) ---
    _log(round_n, "Author synthesis → streaming started")
    reviews = {"Grok": grok_text, "Gemini": gemini_text, "ChatGPT": chatgpt_text}
    synthesis_text = ""
    author_usage = {}
    _t_synth = _time.monotonic()
    try:
        for token in stream_author(document, reviews, state_author_history, eff_anthropic, usage_out=author_usage):
            synthesis_text += token
            yield (
                gr.update(),
                gr.update(), gr.update(),
                gr.update(), gr.update(),
                gr.update(), gr.update(),
                gr.update(),  # synthesis_acc
                gr.update(value=synthesis_text),
                gr.update(),
                gr.update(),
                gr.update(),
                state_doc,
                state_histories,
                state_author_history,
                state_round,
                state_completed_rounds,
                gr.update(),
            )
    except anthropic.BadRequestError as e:
        msg = str(e)
        notice = "⚠️ Anthropic API error: credit balance too low — please top up your Anthropic account." \
            if "credit balance" in msg else f"⚠️ Anthropic (Author) API error: {msg}"
        _log(round_n, f"Author synthesis → Anthropic error: {msg}")
        yield (
            gr.update(value=f"## Round {round_n}", visible=True),
            gr.update(), gr.update(),
            gr.update(), gr.update(),
            gr.update(), gr.update(),
            gr.update(label="❌ Author Synthesis", open=True),
            gr.update(value=synthesis_text or ""),
            gr.update(value=notice, visible=True),
            gr.update(visible=False),
            gr.update(),
            state_doc,
            state_histories,
            state_author_history,
            state_round,
            state_completed_rounds,
            gr.update(interactive=True),
        )
        return

    _log(round_n, f"Author synthesis → done ({_time.monotonic() - _t_synth:.1f}s, {len(synthesis_text)} chars)")

    # Update author history
    review_text = "\n\n".join(f"### {name}\n{text}" for name, text in reviews.items())
    user_msg = f"## Document\n{document}\n\n## Reviews\n{review_text}"
    state_author_history = state_author_history + [
        {"role": "user", "content": user_msg},
        {"role": "assistant", "content": synthesis_text},
    ]

    # --- Convergence check ---
    _log(round_n, "Convergence check → sending to judge")
    converged, reason = check_convergence(reviews, round_n, eff_openai)
    _log(round_n, f"Convergence check → converged={converged} | {reason}")
    if converged:
        advisory_md = f"## Convergence reached\n{reason}"
    else:
        advisory_md = f"*Round {round_n} complete — {reason}*"

    # --- Update state ---
    new_round = {
        "round": round_n,
        "grok": grok_text,         "grok_usage":    _with_cost(MODEL_GROK,    grok_usage),
        "gemini": gemini_text,     "gemini_usage":  _with_cost(MODEL_GEMINI,  gemini_usage),
        "chatgpt": chatgpt_text,   "chatgpt_usage": _with_cost(MODEL_CHATGPT, chatgpt_usage),
        "synthesis": synthesis_text, "author_usage": _with_cost(MODEL_CLAUDE, author_usage),
    }
    updated_completed = state_completed_rounds + [new_round]
    new_round_n = round_n + 1

    _log(round_n, f"Round complete — next is Round {new_round_n}")

    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", prefix=f"synthesis_round{round_n}_", delete=False
    )
    tmp.write(synthesis_text)
    tmp.close()

    yield (
        gr.update(value=f"## Round {round_n}", visible=True),
        gr.update(label=f"{'❌' if 'grok' in offline else '✅'} {LABEL_GROK}"),
        gr.update(value=grok_text),
        gr.update(label=f"{'❌' if 'gemini' in offline else '✅'} {LABEL_GEMINI}"),
        gr.update(value=gemini_text),
        gr.update(label=f"{'❌' if 'chatgpt' in offline else '✅'} {LABEL_CHATGPT}"),
        gr.update(value=chatgpt_text),
        gr.update(label="✅ Author Synthesis", open=True),
        gr.update(value=synthesis_text),
        gr.update(value=advisory_md, visible=True),
        gr.update(value=tmp.name, visible=True),
        render_history(updated_completed),
        synthesis_text,
        state_histories,
        state_author_history,
        new_round_n,
        updated_completed,
        gr.update(value=f"Run Round {new_round_n}", interactive=True),
    )


def make_export_file(completed_rounds):
    content = export_session(completed_rounds)
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".md", prefix="cpar_session_", delete=False)
    tmp.write(content)
    tmp.close()
    return tmp.name


with gr.Blocks(title="CPAR — Cross-Provider Adversarial Review") as demo:
    gr.Markdown("# CPAR — Cross-Provider Adversarial Review")
    gr.Markdown("""\
> **CPAR** runs a panel of 4 AI reviewers (Grok, Gemini, ChatGPT, Claude) \
on your document in parallel — each from a different provider, each with \
real-time web search, none seeing the others' reviews. Claude synthesizes \
the signals each round until the panel converges.
>
> Paste any claim, idea, or draft. Press **Start Round 1**. \
Run 2–4 rounds. Export the full session log when done.
""")

    state_doc             = gr.State("")
    state_histories       = gr.State(make_histories())
    state_author_history  = gr.State([])
    state_round           = gr.State(1)
    state_completed_rounds = gr.State([])

    with gr.Accordion("API Keys", open=_SHOW_BYOK):
        gr.Markdown("Enter API keys to use. Leave blank to use server-configured keys (if available).")
        with gr.Row():
            key_anthropic = gr.Textbox(label="Anthropic API Key (Claude)", type="password", placeholder="sk-ant-...")
            key_xai       = gr.Textbox(label="xAI API Key (Grok)",          type="password", placeholder="xai-...")
        with gr.Row():
            key_google = gr.Textbox(label="Google API Key (Gemini)", type="password", placeholder="AIza...")
            key_openai = gr.Textbox(label="OpenAI API Key (ChatGPT + Judge)", type="password", placeholder="sk-proj-...")

    doc_input = gr.Textbox(
        lines=15, label="Your document or idea",
        placeholder=(
            "Example: \"Smaller context windows force better prompt engineering "
            "and produce higher quality outputs than large context windows\"\n\n"
            "Paste any claim, idea, draft, or document."
        ),
    )

    with gr.Row():
        run_btn   = gr.Button("Start Round 1", variant="primary")
        reset_btn = gr.Button("🔄 New session", variant="stop")

    round_header = gr.Markdown(visible=False)

    with gr.Accordion(LABEL_GROK, open=False) as grok_acc:
        grok_out = gr.Markdown()

    with gr.Accordion(LABEL_GEMINI, open=False) as gemini_acc:
        gemini_out = gr.Markdown()

    with gr.Accordion(LABEL_CHATGPT, open=False) as chatgpt_acc:
        chatgpt_out = gr.Markdown()

    with gr.Accordion("Author Synthesis", open=True) as synthesis_acc:
        synthesis_out = gr.Markdown()
    advisory_out  = gr.Markdown(visible=False)

    with gr.Row():
        download_btn = gr.DownloadButton(label="Download synthesis", visible=False, variant="secondary")
        export_btn   = gr.DownloadButton(label="⬇️ Export full session", variant="secondary")

    history_html = gr.HTML()

    all_outputs = [
        round_header,
        grok_acc,    grok_out,
        gemini_acc,  gemini_out,
        chatgpt_acc, chatgpt_out,
        synthesis_acc, synthesis_out,
        advisory_out,
        download_btn,
        history_html,
        state_doc,
        state_histories,
        state_author_history,
        state_round,
        state_completed_rounds,
        run_btn,
    ]

    all_inputs = [
        doc_input,
        state_doc,
        state_histories,
        state_author_history,
        state_round,
        state_completed_rounds,
        key_anthropic,
        key_xai,
        key_google,
        key_openai,
    ]

    def reset_session():
        return (
            "",                  # doc_input
            "",                  # state_doc
            make_histories(),    # state_histories
            [],                  # state_author_history
            1,                   # state_round
            [],                  # state_completed_rounds
            gr.update(visible=False),                              # round_header
            gr.update(label=LABEL_GROK, open=False),              # grok_acc
            gr.update(value=""),                                   # grok_out
            gr.update(label=LABEL_GEMINI, open=False),            # gemini_acc
            gr.update(value=""),                                   # gemini_out
            gr.update(label=LABEL_CHATGPT, open=False),           # chatgpt_acc
            gr.update(value=""),                                   # chatgpt_out
            gr.update(label="Author Synthesis", open=True),       # synthesis_acc
            gr.update(value=""),                                   # synthesis_out
            gr.update(value="", visible=False),                   # advisory_out
            gr.update(visible=False),                             # download_btn
            "",                                                    # history_html
            gr.update(value="Start Round 1", interactive=True),  # run_btn
        )

    reset_btn.click(
        fn=reset_session,
        outputs=[
            doc_input,
            state_doc, state_histories, state_author_history, state_round, state_completed_rounds,
            round_header,
            grok_acc, grok_out,
            gemini_acc, gemini_out,
            chatgpt_acc, chatgpt_out,
            synthesis_acc, synthesis_out,
            advisory_out,
            download_btn,
            history_html,
            run_btn,
        ],
    )

    run_btn.click(fn=run_round, inputs=all_inputs, outputs=all_outputs)
    export_btn.click(fn=make_export_file, inputs=[state_completed_rounds], outputs=[export_btn])

    gr.Markdown("""\
---
Built by [Alex Anokhin](https://olanokhin.com) · \
[GitHub](https://github.com/olanokhin/cpar-framework) · \
[LinkedIn](https://linkedin.com/in/olanokhin) · \
arXiv preprint in preparation
""")


if __name__ == "__main__":
    demo.launch()
