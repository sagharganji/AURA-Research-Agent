# AURA Atlas — AI Research & Decision Agent

**From complex research questions to structured, evidence-aware decisions.**

AURA is a Python multi-agent research prototype with a browser-based research workspace. It decomposes technical questions into research tasks, searches scholarly literature, datasets and open-source code, organizes evidence, analyzes approaches, and drafts implementation roadmaps.

> **Project status:** Research prototype. The published static interface can show a **clearly labeled saved example** without a running backend. New questions require the FastAPI service, external research APIs, and valid Gemini credentials. Outputs should be independently checked before use.

## Try the interface

- **Static demo:** Deploy `AURA_demo_UI/` to Vercel (instructions below).
- **Local preview:** From the repository root, run `python -m http.server 5500 -d AURA_demo_UI`, then open <http://localhost:5500>.
- **Recorded sample:** Select **Open recorded example** to explore a saved solar-flare research report. It is not generated anew for the text you enter.

The Atlas interface includes a persistent left sidebar, research templates, a visual agent map, an evidence index, summary/roadmap/full-report tabs, accessible desktop/mobile navigation, and Markdown export.

## Architecture

```text
Browser / AURA Atlas (Vercel)
  ├─ Sample mode → saved Markdown report (no API costs)
  └─ Live mode   → POST /research
                    │
                FastAPI (Google Cloud Run)
                    │
                AURA orchestrator
                    ├─ Planning
                    ├─ Paper discovery (OpenAlex)
                    ├─ Dataset discovery (DataCite)
                    ├─ Code discovery (GitHub)
                    ├─ Evidence verification and comparison
                    └─ Decision support and roadmap
                         │
                      Gemini API
```

## Run locally

**Prerequisites:** Python 3.11+, Git, a browser. A Gemini API key is needed **only** for live research.

```bash
git clone https://github.com/sagharganji/AURA-Research-Agent.git
cd AURA-Research-Agent
python -m venv .venv
```

Activate the environment (Windows PowerShell: `./.venv/Scripts/Activate.ps1`; macOS/Linux: `source .venv/bin/activate`) and install:

```bash
python -m pip install -r requirements.txt
```

**Preview the frontend (no secrets):**

```bash
python -m http.server 5500 -d AURA_demo_UI
```

Open <http://localhost:5500>. If already inside `AURA_demo_UI`, omit `-d AURA_demo_UI` to avoid 404 errors.

**Run live research:** Copy `.env.example` to `.env`, add `GEMINI_API_KEY` locally and **never commit it**. Environment variables must be loaded into the server process; for example, in PowerShell:

```powershell
$env:GEMINI_API_KEY = Read-Host "Gemini key"
python -m uvicorn app.api:app --host 127.0.0.1 --port 8080
```

In `AURA_demo_UI/config.js`, temporarily set `window.AURA_BACKEND_URL = "http://127.0.0.1:8080";`. Open the frontend through `localhost:5500` and test a research question. **Never add an API key to config.js or any browser file.**

Check the backend at `http://127.0.0.1:8080/health`, or view its API schema at `/docs`. For tests, install `pytest httpx` and run `python -m pytest tests/test_api.py -q`.

## Deploy once, share the link

**Frontend → Vercel:** Import this repository, set Root Directory to `AURA_demo_UI`, Framework Preset to **Other**, and leave the build command empty (static HTML/CSS/JS). Click Deploy. Share the **Vercel link**, not `localhost`, on LinkedIn; no terminal needs to remain open.

**Backend → Google Cloud Run (optional):** See [DEPLOY.md](DEPLOY.md). Cloud Run requires an eligible Google Cloud account with billing enabled. Configure `GEMINI_API_KEY` as a Secret Manager secret and `ALLOWED_ORIGINS` as your exact Vercel origin. After deployment, copy only the Cloud Run HTTPS URL into `AURA_demo_UI/config.js`, commit and redeploy Vercel.

**Costs and availability:** Cloud Run and Gemini can incur charges; free quotas are not a guarantee of zero cost. Some countries and accounts are restricted. The saved-example frontend is usable without these services. The current in-memory rate limit is a courtesy cap, not secure production abuse protection—add authorization and stricter server-side quotas before publicly exposing paid live inference.

## Repository layout

```text
AURA_demo_UI/        Responsive static website and recorded example
app/api.py           FastAPI health and research endpoints
app/main.py          Multi-agent orchestration
app/agents/          Planner, discovery, verification, analysis and roadmap
app/tools/           OpenAlex, DataCite and GitHub integrations
app/evidence/        Evidence organization
app/report.py        Markdown report assembly
Dockerfile           Cloud Run backend image
requirements.txt     Local development dependencies
requirements.backend.txt  Lean production backend dependencies
tests/               Offline API contract and smoke tests
```

## Example research question

> Design an evidence-backed AI pipeline for solar flare prediction using multimodal satellite observations, public benchmark datasets, calibrated uncertainty estimates, reproducible baselines, and a realistic roadmap for deployment.

## Limitations & next steps

- The interface displays a saved report until a live API URL is configured; it does **not** fabricate live progress, fresh citations or validation scores.
- Source relevance, source credibility and generated conclusions require human review.
- The HTTP endpoint returns a completed result rather than real-time per-agent telemetry.
- Planned: persistent run history, streaming agent progress, stronger evaluation and citation verification, user authentication, and safer public rate limits.

## Author

**Saghar Ganji** · [GitHub](https://github.com/sagharganji)

AURA is an evolving AI research and decision-support prototype, not a finished autonomous scientific validation system.
