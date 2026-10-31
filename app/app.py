import html

import gradio as gr

from cpar import REVIEWER_STREAMS, REVIEWERS, doc_prompt, check_convergence, stream_author


def render_history(rounds: list) -> str:
    if not rounds:
        return ""
    blocks = []
    for r in rounds:
        body = "".join(
            f"<h4>{html.escape(name)}</h4><pre style='white-space:pre-wrap'>{html.escape(r['reviews'].get(name, ''))}</pre>"
            for name in REVIEWERS
        )
        body += f"<h4>Author synthesis</h4><pre style='white-space:pre-wrap'>{html.escape(r['synthesis'])}</pre>"
        body += f"<p><i>{html.escape(r['advisory'])}</i></p>"
        blocks.append(f"<details><summary><b>Round {r['n']}</b></summary>{body}</details>")
    return "".join(blocks)


def run_round(document: str, state: dict):
    if not state:
        if not document.strip():
            raise gr.Error("Paste a document or idea first.")
        state = {"doc": document, "histories": {n: [] for n in REVIEWERS}, "round": 1, "rounds": []}

    n = state["round"]
    doc = state["doc"]
    texts = {name: "" for name in REVIEWERS}
    synthesis, advisory = "", ""
    header = f"### Round {n}"

    def ui(buttons_enabled=False):
        return (
            header, texts["Grok"], texts["Gemini"], texts["ChatGPT"], synthesis, advisory,
            render_history(state["rounds"]), state,
            gr.update(interactive=False, visible=n == 1 and not buttons_enabled),
            gr.update(interactive=buttons_enabled, visible=True),
        )

    yield ui()

    reviews = {}
    user_msg = doc_prompt(doc, n)
    for name in REVIEWERS:
        try:
            for token in REVIEWER_STREAMS[name](state["histories"][name], user_msg):
                texts[name] += token
                yield ui()
        except Exception as e:
            texts[name] += f"\n[error: {e}]"
            yield ui()
            continue
        state["histories"][name] += [
            {"role": "user", "content": user_msg},
            {"role": "assistant", "content": texts[name]},
        ]
        reviews[name] = texts[name]

    if not reviews:
        advisory = "All reviewers failed. Check your API keys."
        yield ui(buttons_enabled=True)
        return

    try:
        for token in stream_author(doc, reviews, n):
            synthesis += token
            yield ui()
        converged, reason = check_convergence(reviews, n)
    except Exception as e:
        advisory = f"Author step failed: {e}"
        yield ui(buttons_enabled=True)
        return

    advisory = (
        f"Panel suggests stopping: {reason}" if converged else f"Panel recommends continuing: {reason}"
    )
    state["rounds"].append({"n": n, "reviews": reviews, "synthesis": synthesis, "advisory": advisory})
    state["doc"] = synthesis
    state["round"] = n + 1
    yield ui(buttons_enabled=True)


with gr.Blocks(title="CPAR") as demo:
    gr.Markdown("# CPAR — Cross-Provider Adversarial Review")
    document = gr.Textbox(lines=15, label="Your document or idea")
    state = gr.State({})
    start_btn = gr.Button("Start Round 1", variant="primary")

    header = gr.Markdown()
    with gr.Row():
        grok = gr.Textbox(label="Grok", lines=12, interactive=False)
        gemini = gr.Textbox(label="Gemini", lines=12, interactive=False)
        gpt = gr.Textbox(label="ChatGPT", lines=12, interactive=False)
    synthesis = gr.Textbox(label="Author Synthesis (Claude) — current document", lines=15, interactive=False)
    advisory = gr.Markdown()
    next_btn = gr.Button("Next Round", visible=False)
    gr.Markdown("## History")
    history = gr.HTML()

    outputs = [header, grok, gemini, gpt, synthesis, advisory, history, state, start_btn, next_btn]
    start_btn.click(run_round, [document, state], outputs)
    next_btn.click(run_round, [document, state], outputs)

if __name__ == "__main__":
    demo.launch()
