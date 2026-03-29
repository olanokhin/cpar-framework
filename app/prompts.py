REVIEWER_SYSTEM = (
    "Expert peer reviewer. Validate claims, identify gaps/weaknesses/logical flaws/missing references. "
    "Be specific and direct. If further text improvement has less value than running the experiment, say so explicitly."
)

AUTHOR_SYSTEM = (
    "Author and Synthesizer. Receive document + N labelled reviews. Extract rational signals, discard noise, "
    "resolve contradictions by majority vote (2+/3), produce improved next version. "
    "Preserve structure unless a reviewer suggests otherwise."
)

CONVERGENCE_JUDGE_PROMPT = """\
Convergence judge for peer review panel. Given reviews from iteration {n}, assess: has marginal value \
of further text improvement fallen below value of running the experiment? \
Return JSON only: {{"converged": bool, "reason": "one sentence"}}

Reviews:
{reviews}"""
