# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **concept/whitepaper repository** — no implementation code exists. The sole deliverable is `README.md`, which documents the CPAR (Cross-Provider Adversarial Review Framework): a methodology for using N independent AI models with distinct cognitive profiles to conduct blind iterative peer review of documents until consensus convergence.

There are no build, test, or lint commands.

## Core Concepts

**The framework has two phases:**
- **DIVERGE** (iterations 1–5 typically): Parallel blind reviews expand the solution space aggressively; Author synthesizes signals into the next document version
- **CONVERGE** (iterations 6–14 typically): Reviewers begin defending current structure; loop continues until all reviewers independently conclude opportunity cost of polishing > shipping

**Key architectural principles:**
- **Blind review**: Each reviewer has independent history; reviewers never see each other's feedback — eliminates herding/authority bias
- **Temporal composition**: Models compose superpowers *through the document across iterations*, not by communicating directly with each other
- **Signal voting**: Majority signal (2+/3) → apply confidently; minority signal (1/3) → do not ignore, especially from Grok (OSINT)
- **Web grounding**: All reviewers use real-time web search each iteration, producing a live literature review as a side effect

**Empirically observed panel (4-model):**
- Claude Sonnet — Author/Synthesizer (long-context coherence, conservative)
- Grok — Research Validator (real-time OSINT, seeks contradictions with reality)
- Gemini — Creative Architect (elegant structural solutions, composition over grounding)
- ChatGPT — Devil's Advocate (adversarial skepticism; skepticism carries extra weight because of its default complimentary tone)

**Stop criterion:** All reviewers independently conclude "marginal value of further improvement < value of running the experiment" — not "text is perfect."

## What Belongs Here

This repo is for the concept specification only. If adding content, it should be:
- Refinements to the framework description in `README.md`
- Case studies following the same empirical format as the RCI example
- Panel configuration guidance based on observed model behavior
