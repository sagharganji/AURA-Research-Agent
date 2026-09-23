---
title: AURA Research Agent
emoji: 🔎
colorFrom: purple
colorTo: blue
sdk: gradio
sdk_version: 6.0.0
app_file: app.py
pinned: false
---

# AURA — AI Research & Decision Agent

AURA is a multi-stage scientific research and decision-support prototype that turns a technical question into source discovery, evidence verification, analysis, a recommendation, and an implementation roadmap.

## MVP pipeline

`Question → Planner → Papers/Datasets/Code → Evidence Store → Verification → Analysis → Decision → Roadmap → Report`

## Included

- OpenAlex paper discovery with rate-limit handling
- DataCite dataset discovery with fallback queries
- GitHub repository discovery with graceful rate-limit handling
- Gemini model fallback/retry logic
- Unified evidence store
- Claim verification
- Analysis, decision, and roadmap agents
- Markdown report export
- Polished Gradio UI with a reliable Demo Snapshot mode
- Original prototype/clean notebooks in `notebooks/`

## Run locally

1. Create a virtual environment.
2. Install dependencies: `pip install -r requirements.txt`
3. Set `GEMINI_API_KEY` (and optionally `OPENALEX_EMAIL`, `GITHUB_TOKEN`).
4. Run: `python -m app.ui`

## Hugging Face Spaces

Create a Gradio Space, upload this project, then add `GEMINI_API_KEY` under **Settings → Variables and secrets**. The `README.md` metadata and root `app.py` are already prepared for Spaces.

## Important

The **Demo Snapshot** is intentionally labeled and uses prebuilt sample content so the UI can be demonstrated even when external APIs are rate-limited. Use **Run Live Research** for real external-source execution.
