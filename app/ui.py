
from pathlib import Path
import html
import gradio as gr

from app.main import run_aura


APP_NAME = "AURA — AI Research & Decision Agent"


# =========================================================
# Generic helpers
# =========================================================

def esc(value):
    if value is None:
        return ""
    return html.escape(str(value))


def safe(value, fallback="—"):
    if value is None:
        return fallback

    text = str(value).strip()

    return text if text else fallback


def write_text_file(path_str: str, content: str):
    path = Path(path_str)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return str(path)


# =========================================================
# Demo snapshot
# =========================================================

def build_demo_result(question: str):
    q = question.strip() if question and question.strip() else (
        "I want to build a solar flare prediction system using machine learning. "
        "Find relevant papers, datasets and code, compare the approaches, "
        "identify limitations, verify the evidence, recommend a direction, "
        "and create an implementation roadmap."
    )

    report = f"""# AURA — Demo Report

## Research Question
{q}

## Executive Summary
AURA analyzed research papers, datasets, and open-source implementation signals
related to solar flare prediction. The overall recommendation is to begin with
a benchmark-oriented supervised learning pipeline built around historical active
region features and magnetogram-derived inputs, then gradually move toward
hybrid deep learning approaches once dataset quality and evaluation rigor are stable.

## Verified Claims
- Historical active region magnetic features remain a strong baseline for solar flare prediction.
- Data quality, class imbalance, and inconsistent evaluation protocols remain major limitations.
- Operationally useful systems require calibration, robustness checks, and temporal validation.
- Combining structured features with image-based signals may improve modeling flexibility.

## Recommendation
Start with a reliable baseline benchmark system before scaling to a more complex hybrid model.

## Roadmap
1. Dataset curation and benchmark definition
2. Baseline modeling and evaluation
3. Hybrid model expansion and deployment readiness
"""

    return {
        "research_question": q,
        "papers": [
            {
                "paper": {
                    "title": "Solar Flare Prediction Using SDO/HMI Vector Magnetic Field Data With a Machine-Learning Algorithm",
                    "year": 2015,
                    "citation_count": 398,
                    "url": "https://doi.org/10.1088/0004-637X/804/1/28",
                },
                "evaluation": {
                    "relevance_score": 0.96,
                    "reason": "Directly addresses solar flare prediction with machine learning and magnetogram-based features."
                }
            },
            {
                "paper": {
                    "title": "Solar Flare Prediction Using Advanced Feature Extraction, Machine Learning, and Feature Selection",
                    "year": 2011,
                    "citation_count": 194,
                    "url": "https://ui.adsabs.harvard.edu/",
                },
                "evaluation": {
                    "relevance_score": 0.91,
                    "reason": "Useful baseline reference for feature engineering and classical ML methods."
                }
            },
        ],
        "datasets": [
            {
                "dataset": {
                    "title": "SDO/HMI Active Region Patch Data",
                    "publication_year": 2016,
                    "publisher": "NASA / JSOC",
                    "url": "https://jsoc.stanford.edu/",
                },
                "evaluation": {
                    "relevance_score": 0.95,
                    "reason": "High-value magnetogram source suitable for feature extraction and model development."
                }
            },
            {
                "dataset": {
                    "title": "GOES X-ray Flare Event Catalog",
                    "publication_year": 2014,
                    "publisher": "NOAA",
                    "url": "https://www.ngdc.noaa.gov/stp/solar/solarflares.html",
                },
                "evaluation": {
                    "relevance_score": 0.88,
                    "reason": "Important reference target source for flare labeling and temporal event matching."
                }
            },
        ],
        "repositories": [
            {
                "repository": {
                    "full_name": "example/solar-flare-prediction",
                    "language": "Python",
                    "stars": 241,
                    "url": "https://github.com/example/solar-flare-prediction",
                    "description": "A research prototype for solar flare prediction using classical ML baselines."
                },
                "evaluation": {
                    "relevance_score": 0.84,
                    "reason": "Reasonably reusable as a baseline implementation reference."
                }
            },
            {
                "repository": {
                    "full_name": "example/flare-deep-learning",
                    "language": "Python",
                    "stars": 173,
                    "url": "https://github.com/example/flare-deep-learning",
                    "description": "Deep learning experiments for solar activity forecasting."
                },
                "evaluation": {
                    "relevance_score": 0.80,
                    "reason": "Useful for architecture ideas, but would need validation before production use."
                }
            },
        ],
        "evidence": [
            {"source_type": "paper", "title": "Paper 1"},
            {"source_type": "paper", "title": "Paper 2"},
            {"source_type": "dataset", "title": "Dataset 1"},
            {"source_type": "dataset", "title": "Dataset 2"},
            {"source_type": "repository", "title": "Repo 1"},
            {"source_type": "repository", "title": "Repo 2"},
        ],
        "verification": {
            "claims": [
                {
                    "claim": "Feature-based machine learning remains a strong benchmark for solar flare prediction.",
                    "confidence": "high",
                    "reason": "Multiple evidence items support its practicality and frequent use in prior work.",
                    "supporting_evidence_ids": [1, 2, 3]
                },
                {
                    "claim": "Class imbalance is a central challenge in flare forecasting.",
                    "confidence": "high",
                    "reason": "This issue repeatedly appears as a limitation in the evidence base.",
                    "supporting_evidence_ids": [1, 2, 4]
                },
                {
                    "claim": "Hybrid pipelines combining structured features and imaging signals are promising.",
                    "confidence": "medium",
                    "reason": "Evidence supports this direction, but consistency and benchmark rigor still matter.",
                    "supporting_evidence_ids": [1, 5, 6]
                },
                {
                    "claim": "A benchmark-first engineering strategy is more realistic than immediately building a complex end-to-end system.",
                    "confidence": "high",
                    "reason": "The evidence favors reliable baselines and careful evaluation before scaling complexity.",
                    "supporting_evidence_ids": [1, 2, 3, 4]
                },
            ]
        },
        "analysis": {
            "analysis_summary": "The evidence suggests that an initial benchmark-driven pipeline should precede more advanced hybrid deep learning systems.",
            "key_findings": [
                "Magnetogram-derived feature pipelines remain a strong baseline.",
                "Reliable label alignment and temporal validation are essential.",
                "Dataset preparation quality may matter more than model complexity in early stages.",
                "Operational usefulness depends on calibration and false-alarm management."
            ],
            "method_comparisons": [
                {
                    "approach": "Feature-based ML baselines",
                    "strengths": [
                        "More interpretable",
                        "Faster to build and benchmark",
                        "Easier to debug"
                    ],
                    "limitations": [
                        "May underuse image-level spatial information",
                        "Performance ceiling may be lower than advanced hybrid methods"
                    ]
                },
                {
                    "approach": "Deep learning / hybrid approaches",
                    "strengths": [
                        "Can capture richer spatial patterns",
                        "Potentially stronger performance with good data"
                    ],
                    "limitations": [
                        "Higher complexity",
                        "More compute-intensive",
                        "Needs stronger data discipline and evaluation rigor"
                    ]
                }
            ],
            "research_gaps": [
                "Lack of standardized evaluation across papers",
                "Need for reproducible benchmark pipelines",
                "Need for better operational robustness analysis"
            ],
            "uncertainties": [
                "Generalization across solar cycles",
                "Robustness under deployment constraints"
            ]
        },
        "decision": {
            "recommended_direction": "Build a benchmark-first supervised learning pipeline using curated active-region magnetic features and flare labels, then expand toward a hybrid feature + imaging system.",
            "confidence": "high",
            "why": [
                "This is the most practical path for an MVP.",
                "It balances scientific value, engineering feasibility, and evaluation quality.",
                "It creates a defensible baseline before investing in more expensive models."
            ],
            "alternatives": [
                {
                    "option": "Go directly to deep learning on magnetograms",
                    "when_to_use": "If a high-quality image pipeline and sufficient compute are already available."
                }
            ],
            "risks": [
                "Noisy labels or weak temporal splits can invalidate comparisons.",
                "Operational performance may differ from offline benchmark performance."
            ]
        },
        "roadmap": {
            "phases": [
                {
                    "phase": 1,
                    "name": "Data & Benchmark Setup",
                    "objective": "Prepare datasets, labels, and evaluation design.",
                    "tasks": [
                        "Collect magnetogram and flare event sources",
                        "Define prediction targets and time windows",
                        "Create train/validation/test temporal splits"
                    ],
                    "deliverables": [
                        "Curated benchmark dataset",
                        "Evaluation protocol",
                        "Data dictionary"
                    ],
                    "evaluation": [
                        "Data completeness checks",
                        "Label quality checks"
                    ]
                },
                {
                    "phase": 2,
                    "name": "Baseline Modeling",
                    "objective": "Build reliable feature-based ML baselines.",
                    "tasks": [
                        "Engineer active-region features",
                        "Train baseline classifiers",
                        "Evaluate precision, recall, and calibration"
                    ],
                    "deliverables": [
                        "Baseline model suite",
                        "Benchmark report"
                    ],
                    "evaluation": [
                        "Cross-time validation",
                        "Class imbalance handling review"
                    ]
                },
                {
                    "phase": 3,
                    "name": "Hybrid Expansion",
                    "objective": "Explore higher-capacity hybrid approaches.",
                    "tasks": [
                        "Add image-driven model components",
                        "Compare hybrid models to baselines",
                        "Prepare deployment-oriented inference design"
                    ],
                    "deliverables": [
                        "Hybrid model experiments",
                        "Comparison report",
                        "Deployment concept"
                    ],
                    "evaluation": [
                        "Performance delta vs baseline",
                        "Latency / compute feasibility"
                    ]
                }
            ]
        },
        "report": report,
    }


# =========================================================
# Render helpers
# =========================================================

def render_status(message, kind="info"):
    kind_class = {
        "info": "status-info",
        "success": "status-success",
        "error": "status-error",
        "demo": "status-demo",
    }.get(kind, "status-info")

    return f"""
<div class="status-card {kind_class}">
    <div class="status-label">STATUS</div>
    <div class="status-text">{esc(message)}</div>
</div>
"""


def render_pipeline(state="idle"):
    states = {
        "idle": [
            ("Plan", "pending"),
            ("Discover", "pending"),
            ("Verify", "pending"),
            ("Analyze", "pending"),
            ("Decide", "pending"),
            ("Roadmap", "pending"),
        ],
        "live": [
            ("Plan", "done"),
            ("Discover", "done"),
            ("Verify", "done"),
            ("Analyze", "done"),
            ("Decide", "done"),
            ("Roadmap", "done"),
        ],
        "demo": [
            ("Plan", "done"),
            ("Discover", "done"),
            ("Verify", "done"),
            ("Analyze", "done"),
            ("Decide", "done"),
            ("Roadmap", "done"),
        ],
        "error": [
            ("Plan", "done"),
            ("Discover", "warn"),
            ("Verify", "warn"),
            ("Analyze", "warn"),
            ("Decide", "warn"),
            ("Roadmap", "warn"),
        ],
    }

    items = states.get(state, states["idle"])

    blocks = []

    for label, status in items:
        status_label = {
            "pending": "Pending",
            "done": "Done",
            "warn": "Needs attention"
        }[status]

        blocks.append(
            f"""
<div class="stage-card">
    <div class="stage-dot {status}"></div>
    <div class="stage-content">
        <div class="stage-title">{label}</div>
        <div class="stage-sub">{status_label}</div>
    </div>
</div>
"""
        )

    return f"""
<div class="panel-card">
    <div class="panel-header">
        <div class="panel-kicker">PIPELINE</div>
        <div class="panel-title">Research Execution Flow</div>
    </div>
    <div class="stage-list">
        {''.join(blocks)}
    </div>
</div>
"""


def render_metrics(result, mode_label="LIVE RUN"):
    papers = len(result.get("papers", []))
    datasets = len(result.get("datasets", []))
    repos = len(result.get("repositories", []))
    evidence = len(result.get("evidence", []))
    claims = len(result.get("verification", {}).get("claims", []))
    phases = len(result.get("roadmap", {}).get("phases", []))

    recommendation = result.get("decision", {}).get(
        "recommended_direction",
        "No recommendation generated."
    )

    confidence = result.get("decision", {}).get(
        "confidence",
        "—"
    )

    return f"""
<div class="overview-wrap">

    <div class="hero-insight">
        <div class="hero-kicker">{esc(mode_label)}</div>
        <div class="hero-title">Decision Brief</div>
        <div class="hero-summary">{esc(recommendation)}</div>
        <div class="hero-confidence">
            Confidence: <strong>{esc(confidence)}</strong>
        </div>
    </div>

    <div class="metrics-grid">
        <div class="metric-card">
            <div class="metric-value">{papers}</div>
            <div class="metric-label">Papers</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{datasets}</div>
            <div class="metric-label">Datasets</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{repos}</div>
            <div class="metric-label">Repositories</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{evidence}</div>
            <div class="metric-label">Evidence</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{claims}</div>
            <div class="metric-label">Claims</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{phases}</div>
            <div class="metric-label">Roadmap Phases</div>
        </div>
    </div>

</div>
"""


def render_empty_block(title, subtitle):
    return f"""
<div class="empty-card">
    <div class="empty-title">{esc(title)}</div>
    <div class="empty-sub">{esc(subtitle)}</div>
</div>
"""


def render_sources(items, source_key):
    if not items:
        return render_empty_block(
            "No sources available",
            "Run the pipeline or load the demo snapshot to populate this section."
        )

    blocks = []

    for i, item in enumerate(items, start=1):
        source = item.get(source_key, {})
        evaluation = item.get("evaluation", {})

        if source_key == "paper":
            title = source.get("title")
            meta = f"{source.get('year', '—')} · {source.get('citation_count', 0)} citations"
            url = source.get("url")
        elif source_key == "dataset":
            title = source.get("title")
            meta = f"{source.get('publication_year', '—')} · {source.get('publisher', 'Dataset source')}"
            url = source.get("url")
        else:
            title = source.get("full_name")
            meta = f"{source.get('language', 'Unknown language')} · ★ {source.get('stars', 0)}"
            url = source.get("url")

        score = evaluation.get("relevance_score", "—")
        reason = evaluation.get("reason", "No explanation available.")

        link_html = ""
        if url:
            link_html = f'<a href="{esc(url)}" target="_blank">Open ↗</a>'

        blocks.append(
            f"""
<div class="source-card">
    <div class="source-index">{i:02}</div>
    <div class="source-main">
        <div class="source-title">{esc(title)}</div>
        <div class="source-meta">{esc(meta)}</div>
        <div class="source-reason">{esc(reason)}</div>
        <div class="source-bottom">
            <span class="badge badge-score">Relevance {esc(score)}</span>
            {link_html}
        </div>
    </div>
</div>
"""
        )

    return "".join(blocks)


def render_claims(verification):
    claims = verification.get("claims", [])

    if not claims:
        return render_empty_block(
            "No verified claims",
            "This panel will show evidence-backed findings after the run completes."
        )

    html_blocks = []

    for claim in claims:
        confidence = str(claim.get("confidence", "unknown")).lower()
        reason = claim.get("reason", "")
        claim_text = claim.get("claim", "")
        evidence_ids = claim.get("supporting_evidence_ids", [])

        html_blocks.append(
            f"""
<div class="claim-card">
    <div class="claim-top">
        <span class="badge badge-{esc(confidence)}">{esc(confidence.upper())}</span>
        <span class="claim-evidence">Evidence {esc(evidence_ids)}</span>
    </div>
    <div class="claim-title">{esc(claim_text)}</div>
    <div class="claim-reason">{esc(reason)}</div>
</div>
"""
        )

    return "".join(html_blocks)


def render_analysis_md(analysis):
    if not analysis:
        return "# Analysis\n\nNo analysis available yet."

    text = "# Analysis\n\n"

    summary = analysis.get("analysis_summary", "")
    if summary:
        text += f"{summary}\n\n"

    findings = analysis.get("key_findings", [])
    if findings:
        text += "## Key Findings\n"
        for x in findings:
            text += f"- {x}\n"
        text += "\n"

    comparisons = analysis.get("method_comparisons", [])
    if comparisons:
        text += "## Method Comparison\n"
        for item in comparisons:
            text += f"### {item.get('approach', 'Approach')}\n"
            strengths = item.get("strengths", [])
            limitations = item.get("limitations", [])

            if strengths:
                text += "**Strengths**\n"
                for x in strengths:
                    text += f"- {x}\n"

            if limitations:
                text += "\n**Limitations**\n"
                for x in limitations:
                    text += f"- {x}\n"

            text += "\n"

    gaps = analysis.get("research_gaps", [])
    if gaps:
        text += "## Research Gaps\n"
        for x in gaps:
            text += f"- {x}\n"
        text += "\n"

    uncertainties = analysis.get("uncertainties", [])
    if uncertainties:
        text += "## Uncertainties\n"
        for x in uncertainties:
            text += f"- {x}\n"

    return text


def render_decision_md(decision):
    if not decision:
        return "# Decision\n\nNo decision available yet."

    text = "# Decision\n\n"
    text += f"{decision.get('recommended_direction', '')}\n\n"
    text += f"**Confidence:** {decision.get('confidence', '—')}\n\n"

    why = decision.get("why", [])
    if why:
        text += "## Why this direction\n"
        for x in why:
            text += f"- {x}\n"
        text += "\n"

    alternatives = decision.get("alternatives", [])
    if alternatives:
        text += "## Alternatives\n"
        for alt in alternatives:
            text += f"- **{alt.get('option', 'Alternative')}** — {alt.get('when_to_use', '')}\n"
        text += "\n"

    risks = decision.get("risks", [])
    if risks:
        text += "## Risks\n"
        for x in risks:
            text += f"- {x}\n"

    return text


def render_roadmap_md(roadmap):
    if not roadmap:
        return "# Roadmap\n\nNo roadmap available yet."

    phases = roadmap.get("phases", [])
    if not phases:
        return "# Roadmap\n\nNo roadmap phases were generated."

    text = "# Implementation Roadmap\n\n"

    for phase in phases:
        text += f"## Phase {phase.get('phase')} — {phase.get('name', '')}\n\n"
        text += f"**Objective:** {phase.get('objective', '')}\n\n"

        tasks = phase.get("tasks", [])
        if tasks:
            text += "**Tasks**\n"
            for x in tasks:
                text += f"- {x}\n"
            text += "\n"

        deliverables = phase.get("deliverables", [])
        if deliverables:
            text += "**Deliverables**\n"
            for x in deliverables:
                text += f"- {x}\n"
            text += "\n"

        evaluation = phase.get("evaluation", [])
        if evaluation:
            text += "**Evaluation**\n"
            for x in evaluation:
                text += f"- {x}\n"
            text += "\n"

        text += "---\n\n"

    return text


def build_presentable_output(result, mode="live"):
    mode_label = "LIVE RESEARCH RUN" if mode == "live" else "DEMO SNAPSHOT"
    overview = render_metrics(result, mode_label=mode_label)
    papers = render_sources(result.get("papers", []), "paper")
    datasets = render_sources(result.get("datasets", []), "dataset")
    repositories = render_sources(result.get("repositories", []), "repository")
    claims = render_claims(result.get("verification", {}))
    analysis = render_analysis_md(result.get("analysis", {}))
    decision = render_decision_md(result.get("decision", {}))
    roadmap = render_roadmap_md(result.get("roadmap", {}))
    report = result.get("report", "# Report\n\nNo report available.")

    report_name = "outputs/AURA_demo_report.md" if mode == "demo" else "outputs/AURA_final_report.md"
    report_file = write_text_file(report_name, report)

    return overview, papers, datasets, repositories, claims, analysis, decision, roadmap, report, report_file


def empty_workspace():
    return (
        render_status("Ready. Enter a research question or load the demo snapshot.", "info"),
        render_pipeline("idle"),
        render_empty_block("AURA Workspace", "Run live research or load the demo snapshot to view the workspace."),
        render_empty_block("Papers", "No paper results yet."),
        render_empty_block("Datasets", "No dataset results yet."),
        render_empty_block("Code", "No repository results yet."),
        render_empty_block("Verified Evidence", "No verified claims yet."),
        "# Analysis\n\nNo analysis available yet.",
        "# Decision\n\nNo decision available yet.",
        "# Roadmap\n\nNo roadmap available yet.",
        "# Full Report\n\nNo report available yet.",
        None,
    )


# =========================================================
# Actions
# =========================================================

def run_live(question, progress=gr.Progress()):
    if not question or not question.strip():
        raise gr.Error("First enter a research question.")

    try:
        progress(0.08, desc="Launching AURA pipeline...")

        result = run_aura(
            question.strip(),
            max_papers=3,
            max_datasets=3,
            max_repositories=2,
            save_output=True,
        )

        progress(0.92, desc="Rendering workspace...")

        overview, papers, datasets, repositories, claims, analysis, decision, roadmap, report, report_file = build_presentable_output(
            result,
            mode="live"
        )

        progress(1.0, desc="Done")

        status = render_status(
            "Live research completed successfully.",
            "success"
        )

        pipeline = render_pipeline("live")

        return (
            status,
            pipeline,
            overview,
            papers,
            datasets,
            repositories,
            claims,
            analysis,
            decision,
            roadmap,
            report,
            report_file,
        )

    except Exception as e:
        status = render_status(
            f"Live research failed. You can still click 'Load Demo Snapshot' for a polished demo view. Error: {str(e)}",
            "error"
        )

        pipeline = render_pipeline("error")

        return (
            status,
            pipeline,
            render_empty_block("Run failed", "The live pipeline encountered an error. Use the demo snapshot to showcase the UI reliably."),
            render_empty_block("Papers", "No paper results available."),
            render_empty_block("Datasets", "No dataset results available."),
            render_empty_block("Code", "No repository results available."),
            render_empty_block("Verified Evidence", "No verified claims available."),
            "# Analysis\n\nLive execution failed.",
            "# Decision\n\nLive execution failed.",
            "# Roadmap\n\nLive execution failed.",
            "# Full Report\n\nLive execution failed.",
            None,
        )


def load_demo(question):
    result = build_demo_result(question)

    overview, papers, datasets, repositories, claims, analysis, decision, roadmap, report, report_file = build_presentable_output(
        result,
        mode="demo"
    )

    status = render_status(
        "Demo snapshot loaded. This is ideal for recording a polished walkthrough.",
        "demo"
    )

    pipeline = render_pipeline("demo")

    return (
        status,
        pipeline,
        overview,
        papers,
        datasets,
        repositories,
        claims,
        analysis,
        decision,
        roadmap,
        report,
        report_file,
    )


def clear_all():
    return ("",) + empty_workspace()


# =========================================================
# Design
# =========================================================

CSS = """
:root{
    --bg:#06101f;
    --panel:#0c1729;
    --panel-2:#101c31;
    --text:#eef3fb;
    --muted:#8ea0bb;
    --border:rgba(148,163,184,.16);
    --accent:#7c3aed;
    --accent2:#2563eb;
    --green:#10b981;
    --yellow:#f59e0b;
    --red:#ef4444;
    --cyan:#22d3ee;
}

html, body, .gradio-container{
    background:
        radial-gradient(circle at 15% 0%, rgba(124,58,237,.18), transparent 30%),
        radial-gradient(circle at 85% 10%, rgba(37,99,235,.12), transparent 28%),
        linear-gradient(180deg, #06101f 0%, #040b17 100%) !important;
    color: var(--text) !important;
    font-family: Inter, ui-sans-serif, system-ui, sans-serif !important;
}

.gradio-container{
    max-width: 1450px !important;
    margin: auto !important;
}

.aura-shell{
    padding-top: 18px;
    padding-bottom: 30px;
}

.hero-card{
    border:1px solid var(--border);
    background: linear-gradient(145deg, rgba(12,23,41,.95), rgba(8,15,28,.92));
    border-radius: 30px;
    padding: 42px;
    margin-bottom: 20px;
    box-shadow: 0 18px 55px rgba(0,0,0,.28);
}

.hero-kicker{
    color:#a78bfa;
    letter-spacing:.22em;
    font-size:12px;
    font-weight:800;
}

.hero-main{
    margin-top:14px;
    font-size:56px;
    line-height:1.02;
    letter-spacing:-.05em;
    font-weight:800;
    color:#f8fafc;
    max-width:760px;
}

.hero-sub{
    margin-top:16px;
    max-width:820px;
    line-height:1.7;
    font-size:17px;
    color:#9eb0c7;
}

.hero-flow{
    margin-top:26px;
    color:#73839c;
    letter-spacing:.02em;
    font-size:13px;
}

.panel-card{
    border:1px solid var(--border);
    background: rgba(12,23,41,.78);
    border-radius: 24px;
    padding: 22px;
    height: 100%;
}

.panel-header{
    margin-bottom: 16px;
}

.panel-kicker{
    color:#60a5fa;
    letter-spacing:.18em;
    font-size:11px;
    font-weight:800;
}

.panel-title{
    margin-top:7px;
    font-size:20px;
    font-weight:700;
    color:#f1f5f9;
}

.input-wrap{
    border:1px solid var(--border) !important;
    background: rgba(12,23,41,.78) !important;
    border-radius: 24px !important;
    padding: 18px !important;
}

#question-box textarea{
    background: rgba(255,255,255,.02) !important;
    font-size: 16px !important;
    line-height: 1.7 !important;
}

#live-btn{
    background: linear-gradient(100deg, #7c3aed, #2563eb) !important;
    border: none !important;
    border-radius: 16px !important;
    min-height: 54px;
    font-weight: 800 !important;
}

#demo-btn{
    background: rgba(255,255,255,.03) !important;
    border: 1px solid rgba(148,163,184,.22) !important;
    color: #e2e8f0 !important;
    border-radius: 16px !important;
    min-height: 54px;
    font-weight: 700 !important;
}

#clear-btn{
    border-radius: 16px !important;
    min-height: 54px;
}

.status-card{
    border:1px solid var(--border);
    border-radius: 18px;
    padding: 16px 18px;
    margin-top: 16px;
    margin-bottom: 18px;
}

.status-label{
    font-size:11px;
    letter-spacing:.18em;
    font-weight:800;
    margin-bottom:8px;
}

.status-text{
    font-size:14px;
    line-height:1.6;
}

.status-info{background: rgba(12,23,41,.68);}
.status-info .status-label{color:#60a5fa;}

.status-success{background: rgba(16,185,129,.08); border-color: rgba(16,185,129,.24);}
.status-success .status-label{color:#6ee7b7;}

.status-error{background: rgba(239,68,68,.08); border-color: rgba(239,68,68,.22);}
.status-error .status-label{color:#fca5a5;}

.status-demo{background: rgba(124,58,237,.10); border-color: rgba(124,58,237,.26);}
.status-demo .status-label{color:#c4b5fd;}

.stage-list{
    display:grid;
    gap:10px;
}

.stage-card{
    display:flex;
    align-items:center;
    gap:12px;
    border:1px solid rgba(148,163,184,.10);
    background: rgba(255,255,255,.02);
    border-radius: 16px;
    padding: 12px 14px;
}

.stage-dot{
    width:10px;
    height:10px;
    border-radius:999px;
}

.stage-dot.pending{background:#475569;}
.stage-dot.done{background:#10b981;}
.stage-dot.warn{background:#f59e0b;}

.stage-title{
    font-weight:700;
    color:#edf2fb;
    font-size:14px;
}

.stage-sub{
    color:#8294ad;
    font-size:12px;
    margin-top:2px;
}

.overview-wrap{
    display:grid;
    grid-template-columns: 1.25fr 1fr;
    gap:16px;
    align-items:stretch;
}

.hero-insight{
    border:1px solid rgba(124,58,237,.22);
    background: linear-gradient(145deg, rgba(124,58,237,.10), rgba(37,99,235,.07));
    border-radius: 22px;
    padding: 24px;
}

.hero-title{
    margin-top:8px;
    font-size:28px;
    font-weight:800;
    color:#f8fafc;
}

.hero-summary{
    margin-top:12px;
    color:#dde7f7;
    font-size:15px;
    line-height:1.72;
}

.hero-confidence{
    margin-top:14px;
    color:#9fb0c6;
    font-size:13px;
}

.metrics-grid{
    display:grid;
    grid-template-columns: repeat(3, minmax(120px,1fr));
    gap:12px;
}

.metric-card{
    border:1px solid var(--border);
    background: rgba(12,23,41,.70);
    border-radius: 18px;
    padding: 18px;
    min-height: 100px;
}

.metric-value{
    font-size:30px;
    font-weight:800;
    color:#f8fafc;
}

.metric-label{
    margin-top:6px;
    color:#8ea0bb;
    font-size:13px;
}

.source-card,
.claim-card,
.empty-card{
    border:1px solid var(--border);
    background: rgba(12,23,41,.72);
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 12px;
}

.source-card{
    display:flex;
    gap:16px;
}

.source-index{
    width:36px;
    color:#64748b;
    font-family: ui-monospace, monospace;
    font-size:12px;
}

.source-main{
    flex:1;
}

.source-title,
.claim-title,
.empty-title{
    color:#f1f5f9;
    font-weight:780;
    line-height:1.45;
}

.source-meta{
    color:#7f92ad;
    margin-top:6px;
    font-size:12px;
}

.source-reason,
.claim-reason,
.empty-sub{
    color:#9caec6;
    margin-top:12px;
    line-height:1.65;
    font-size:13px;
}

.source-bottom{
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-top:14px;
}

.source-bottom a{
    color:#c4b5fd !important;
    font-size:12px;
    text-decoration:none;
}

.badge{
    display:inline-flex;
    align-items:center;
    border-radius:999px;
    padding:5px 10px;
    font-size:11px;
    font-weight:800;
}

.badge-score{
    background: rgba(34,211,238,.09);
    color:#67e8f9;
}

.badge-high{
    background: rgba(16,185,129,.10);
    color:#6ee7b7;
}

.badge-medium{
    background: rgba(245,158,11,.10);
    color:#fde68a;
}

.badge-low{
    background: rgba(239,68,68,.10);
    color:#fca5a5;
}

.claim-top{
    display:flex;
    justify-content:space-between;
    align-items:center;
    gap:12px;
    margin-bottom:12px;
}

.claim-evidence{
    color:#8294ad;
    font-size:12px;
}

.empty-card{
    text-align:center;
    padding:28px;
}

.markdown,
.prose,
.prose *{
    color:#e6edf8 !important;
}

footer{
    display:none !important;
}
"""

HEADER = """
<div class="aura-shell">
    <div class="hero-card">
        <div class="hero-kicker">AURA / RESEARCH INTELLIGENCE</div>
        <div class="hero-main">From questions to evidence-backed decisions.</div>
        <div class="hero-sub">
            A multi-agent scientific research workspace that plans, discovers
            sources, verifies evidence, compares approaches, and turns research
            into an actionable implementation roadmap.
        </div>
        <div class="hero-flow">
            PLAN → DISCOVER → VERIFY → ANALYZE → DECIDE → BUILD
        </div>
    </div>
</div>
"""


# =========================================================
# App
# =========================================================

with gr.Blocks(title=APP_NAME) as demo:
    gr.HTML(f"<style>{CSS}</style>")
    gr.HTML(HEADER)

    with gr.Row():
        with gr.Column(scale=7):
            with gr.Group(elem_classes=["input-wrap"]):
                question = gr.Textbox(
                    label="RESEARCH QUESTION",
                    placeholder=(
                        "Example: I want to build a solar flare prediction system. "
                        "Find relevant papers, datasets and methods, compare approaches, "
                        "identify limitations, and propose an implementation roadmap."
                    ),
                    lines=5,
                    elem_id="question-box",
                )

                with gr.Row():
                    live_btn = gr.Button(
                        "Run Live Research →",
                        elem_id="live-btn",
                    )
                    demo_btn = gr.Button(
                        "Load Demo Snapshot",
                        elem_id="demo-btn",
                    )
                    clear_btn = gr.Button(
                        "Reset",
                        elem_id="clear-btn",
                    )

        with gr.Column(scale=5):
            pipeline = gr.HTML(render_pipeline("idle"))

    status = gr.HTML(
        render_status(
            "Ready. Use Live Research for a real run, or Demo Snapshot for a polished presentation.",
            "info"
        )
    )

    with gr.Tabs():
        with gr.Tab("Overview"):
            overview = gr.HTML(
                render_empty_block(
                    "AURA Workspace",
                    "Run live research or load the demo snapshot."
                )
            )

        with gr.Tab("Papers"):
            papers = gr.HTML(
                render_empty_block(
                    "Papers",
                    "No paper results yet."
                )
            )

        with gr.Tab("Datasets"):
            datasets = gr.HTML(
                render_empty_block(
                    "Datasets",
                    "No dataset results yet."
                )
            )

        with gr.Tab("Code"):
            repositories = gr.HTML(
                render_empty_block(
                    "Code",
                    "No repository results yet."
                )
            )

        with gr.Tab("Verified Claims"):
            claims = gr.HTML(
                render_empty_block(
                    "Verified Claims",
                    "No verified claims yet."
                )
            )

        with gr.Tab("Analysis"):
            analysis = gr.Markdown("# Analysis\n\nNo analysis available yet.")

        with gr.Tab("Decision"):
            decision = gr.Markdown("# Decision\n\nNo decision available yet.")

        with gr.Tab("Roadmap"):
            roadmap = gr.Markdown("# Roadmap\n\nNo roadmap available yet.")

        with gr.Tab("Full Report"):
            report = gr.Markdown("# Full Report\n\nNo report available yet.")

    report_file = gr.File(
        label="Download Report",
        interactive=False
    )

    gr.Markdown(
        """
---
**AURA — AI Research & Decision Agent**  
Research discovery · Evidence verification · Decision intelligence
"""
    )

    live_btn.click(
        fn=run_live,
        inputs=[question],
        outputs=[
            status,
            pipeline,
            overview,
            papers,
            datasets,
            repositories,
            claims,
            analysis,
            decision,
            roadmap,
            report,
            report_file,
        ],
    )

    demo_btn.click(
        fn=load_demo,
        inputs=[question],
        outputs=[
            status,
            pipeline,
            overview,
            papers,
            datasets,
            repositories,
            claims,
            analysis,
            decision,
            roadmap,
            report,
            report_file,
        ],
    )

    clear_btn.click(
        fn=clear_all,
        inputs=[],
        outputs=[
            question,
            status,
            pipeline,
            overview,
            papers,
            datasets,
            repositories,
            claims,
            analysis,
            decision,
            roadmap,
            report_file,
        ],
    )


if __name__ == "__main__":
    demo.queue()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
        show_error=True,
    )
