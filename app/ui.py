from pathlib import Path
import html
import gradio as gr

from app.main import run_aura

APP_NAME = "AURA — AI Research & Decision Agent"


def esc(value):
    return html.escape(str(value)) if value is not None else ""


def write_text_file(path_str: str, content: str):
    path = Path(path_str)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return str(path)


def build_demo_result(question: str):
    q = question.strip() if question and question.strip() else (
        "I want to build a solar flare prediction system using machine learning. "
        "Find relevant papers, datasets and code, compare approaches, identify limitations, "
        "verify the evidence, recommend a direction, and create an implementation roadmap."
    )
    report = f"""# AURA — Demo Report\n\n## Research Question\n{q}\n\n## Executive Summary\nAURA analyzed research papers, datasets, and implementation signals related to solar flare prediction.\n\n## Recommendation\nStart with a benchmark-first supervised learning pipeline, then expand toward a hybrid feature + imaging system.\n"""
    return {
        "research_question": q,
        "papers": [
            {"paper": {"title": "Solar Flare Prediction Using SDO/HMI Vector Magnetic Field Data With a Machine-Learning Algorithm", "year": 2015, "citation_count": 398, "url": "https://doi.org/10.1088/0004-637X/804/1/28"}, "evaluation": {"relevance_score": 0.96, "reason": "Directly addresses solar flare prediction with ML and magnetogram features."}},
            {"paper": {"title": "Solar Flare Prediction Using Advanced Feature Extraction, Machine Learning, and Feature Selection", "year": 2011, "citation_count": 194, "url": "https://ui.adsabs.harvard.edu/"}, "evaluation": {"relevance_score": 0.91, "reason": "Useful baseline reference for feature engineering and classical ML."}},
        ],
        "datasets": [
            {"dataset": {"title": "SDO/HMI Active Region Patch Data", "publication_year": 2016, "publisher": "NASA / JSOC", "url": "https://jsoc.stanford.edu/"}, "evaluation": {"relevance_score": 0.95, "reason": "High-value magnetogram source suitable for feature extraction."}},
            {"dataset": {"title": "GOES X-ray Flare Event Catalog", "publication_year": 2014, "publisher": "NOAA", "url": "https://www.ngdc.noaa.gov/stp/solar/solarflares.html"}, "evaluation": {"relevance_score": 0.88, "reason": "Useful target source for flare labels and event matching."}},
        ],
        "repositories": [],
        "evidence": [{"source_type": "paper"}, {"source_type": "paper"}, {"source_type": "dataset"}, {"source_type": "dataset"}],
        "verification": {"claims": [
            {"claim": "Feature-based ML remains a strong benchmark for solar flare prediction.", "confidence": "high", "reason": "Multiple evidence items support its practical use.", "supporting_evidence_ids": [1,2,3]},
            {"claim": "Class imbalance is a central challenge in flare forecasting.", "confidence": "high", "reason": "This issue repeatedly appears as a limitation.", "supporting_evidence_ids": [1,2,4]},
            {"claim": "Hybrid pipelines combining structured features and imaging signals are promising.", "confidence": "medium", "reason": "Evidence supports this direction, but benchmark rigor matters.", "supporting_evidence_ids": [1,3,4]},
        ]},
        "analysis": {"analysis_summary": "The evidence favors a benchmark-driven baseline before scaling to more complex hybrid systems.", "key_findings": ["Magnetogram-derived features remain a strong baseline.", "Temporal validation and label quality are essential.", "Operational usefulness depends on calibration and false-alarm management."], "method_comparisons": [{"approach": "Feature-based ML", "strengths": ["Interpretable", "Fast to benchmark"], "limitations": ["May underuse image-level spatial information"]}, {"approach": "Deep learning / hybrid", "strengths": ["Can capture richer spatial patterns"], "limitations": ["Higher complexity and compute"]}], "research_gaps": ["Need for reproducible benchmark pipelines"], "uncertainties": ["Generalization across solar cycles"]},
        "decision": {"recommended_direction": "Build a benchmark-first supervised learning pipeline using curated active-region magnetic features and flare labels, then expand toward a hybrid feature + imaging system.", "confidence": "high", "why": ["Practical for an MVP", "Balances scientific value and engineering feasibility"], "alternatives": [{"option": "Direct deep learning on magnetograms", "when_to_use": "When high-quality image data and compute are already available"}], "risks": ["Weak temporal splits can invalidate comparisons"]},
        "roadmap": {"phases": [
            {"phase": 1, "name": "Data & Benchmark Setup", "objective": "Prepare datasets, labels, and evaluation design.", "tasks": ["Collect sources", "Define targets", "Create temporal splits"], "deliverables": ["Curated dataset", "Evaluation protocol"], "evaluation": ["Data completeness", "Label quality"]},
            {"phase": 2, "name": "Baseline Modeling", "objective": "Build reliable ML baselines.", "tasks": ["Engineer features", "Train classifiers", "Evaluate calibration"], "deliverables": ["Baseline suite", "Benchmark report"], "evaluation": ["Cross-time validation"]},
            {"phase": 3, "name": "Hybrid Expansion", "objective": "Explore higher-capacity hybrid approaches.", "tasks": ["Add image model components", "Compare with baselines"], "deliverables": ["Hybrid experiments", "Comparison report"], "evaluation": ["Performance delta", "Compute feasibility"]},
        ]},
        "report": report,
    }


def render_status(message, kind="info"):
    return f'<div class="status-card status-{kind}"><div class="status-label">STATUS</div><div class="status-text">{esc(message)}</div></div>'


def render_pipeline(state="idle"):
    done = state in ("live", "demo")
    labels = ["Plan", "Discover", "Verify", "Analyze", "Decide", "Roadmap"]
    blocks = []
    for label in labels:
        status = "done" if done else ("warn" if state == "error" else "pending")
        sub = "Done" if status == "done" else ("Needs attention" if status == "warn" else "Pending")
        blocks.append(f'<div class="stage-card"><div class="stage-dot {status}"></div><div><div class="stage-title">{label}</div><div class="stage-sub">{sub}</div></div></div>')
    return '<div class="panel-card"><div class="panel-kicker">PIPELINE</div><div class="panel-title">Research Execution Flow</div><div class="stage-list">' + ''.join(blocks) + '</div></div>'


def render_empty_block(title, subtitle):
    return f'<div class="empty-card"><div class="empty-title">{esc(title)}</div><div class="empty-sub">{esc(subtitle)}</div></div>'


def render_metrics(result, mode_label="LIVE RUN"):
    papers = len(result.get("papers", [])); datasets = len(result.get("datasets", [])); repos = len(result.get("repositories", [])); evidence = len(result.get("evidence", [])); claims = len(result.get("verification", {}).get("claims", [])); phases = len(result.get("roadmap", {}).get("phases", []))
    recommendation = result.get("decision", {}).get("recommended_direction", "No recommendation generated.")
    confidence = result.get("decision", {}).get("confidence", "—")
    cards = ''.join(f'<div class="metric-card"><div class="metric-value">{v}</div><div class="metric-label">{l}</div></div>' for v,l in [(papers,"Papers"),(datasets,"Datasets"),(repos,"Repositories"),(evidence,"Evidence"),(claims,"Claims"),(phases,"Roadmap Phases")])
    return f'<div class="overview-wrap"><div class="hero-insight"><div class="hero-kicker">{esc(mode_label)}</div><div class="hero-title">Decision Brief</div><div class="hero-summary">{esc(recommendation)}</div><div class="hero-confidence">Confidence: <strong>{esc(confidence)}</strong></div></div><div class="metrics-grid">{cards}</div></div>'


def render_sources(items, source_key):
    if not items:
        return render_empty_block("No sources available", "No results from this provider during this run.")
    blocks = []
    for i,item in enumerate(items,1):
        source = item.get(source_key, {}); evaluation = item.get("evaluation", {})
        if source_key == "paper": title=source.get("title"); meta=f"{source.get('year','—')} · {source.get('citation_count',0)} citations"; url=source.get("url")
        elif source_key == "dataset": title=source.get("title"); meta=f"{source.get('publication_year','—')} · {source.get('publisher','Dataset source')}"; url=source.get("url")
        else: title=source.get("full_name"); meta=f"{source.get('language','Unknown')} · ★ {source.get('stars',0)}"; url=source.get("url")
        link = f'<a href="{esc(url)}" target="_blank">Open ↗</a>' if url else ""
        blocks.append(f'<div class="source-card"><div class="source-index">{i:02}</div><div class="source-main"><div class="source-title">{esc(title)}</div><div class="source-meta">{esc(meta)}</div><div class="source-reason">{esc(evaluation.get("reason",""))}</div><div class="source-bottom"><span class="badge badge-score">Relevance {esc(evaluation.get("relevance_score","—"))}</span>{link}</div></div></div>')
    return ''.join(blocks)


def render_claims(verification):
    claims = verification.get("claims", [])
    if not claims:
        return render_empty_block("No verified claims", "Verified findings will appear here.")
    return ''.join(f'<div class="claim-card"><div class="claim-top"><span class="badge badge-{esc(str(c.get("confidence","unknown")).lower())}">{esc(str(c.get("confidence","unknown")).upper())}</span><span class="claim-evidence">Evidence {esc(c.get("supporting_evidence_ids", []))}</span></div><div class="claim-title">{esc(c.get("claim"))}</div><div class="claim-reason">{esc(c.get("reason"))}</div></div>' for c in claims)


def render_analysis_md(analysis):
    text = "# Analysis\n\n" + analysis.get("analysis_summary", "") + "\n\n"
    if analysis.get("key_findings"):
        text += "## Key Findings\n" + ''.join(f'- {x}\n' for x in analysis["key_findings"]) + "\n"
    for item in analysis.get("method_comparisons", []):
        text += f'## {item.get("approach","Approach")}\n**Strengths**\n' + ''.join(f'- {x}\n' for x in item.get("strengths", [])) + '\n**Limitations**\n' + ''.join(f'- {x}\n' for x in item.get("limitations", [])) + '\n'
    if analysis.get("research_gaps"):
        text += "## Research Gaps\n" + ''.join(f'- {x}\n' for x in analysis["research_gaps"])
    return text


def render_decision_md(decision):
    text = "# Decision\n\n" + decision.get("recommended_direction", "") + f'\n\n**Confidence:** {decision.get("confidence","—")}\n\n'
    if decision.get("why"):
        text += "## Why\n" + ''.join(f'- {x}\n' for x in decision["why"]) + '\n'
    if decision.get("risks"):
        text += "## Risks\n" + ''.join(f'- {x}\n' for x in decision["risks"])
    return text


def render_roadmap_md(roadmap):
    text = "# Implementation Roadmap\n\n"
    for p in roadmap.get("phases", []):
        text += f'## Phase {p.get("phase")} — {p.get("name","")}\n\n**Objective:** {p.get("objective","")}\n\n**Tasks**\n' + ''.join(f'- {x}\n' for x in p.get("tasks", [])) + '\n**Deliverables**\n' + ''.join(f'- {x}\n' for x in p.get("deliverables", [])) + '\n---\n\n'
    return text


def build_presentable_output(result, mode="live"):
    report = result.get("report", "# Report\n\nNo report available.")
    path = write_text_file("outputs/AURA_demo_report.md" if mode == "demo" else "outputs/AURA_final_report.md", report)
    return (
        render_metrics(result, "DEMO SNAPSHOT" if mode == "demo" else "LIVE RESEARCH RUN"),
        render_sources(result.get("papers", []), "paper"),
        render_sources(result.get("datasets", []), "dataset"),
        render_sources(result.get("repositories", []), "repository"),
        render_claims(result.get("verification", {})),
        render_analysis_md(result.get("analysis", {})),
        render_decision_md(result.get("decision", {})),
        render_roadmap_md(result.get("roadmap", {})),
        report,
        path,
    )


def run_live(question, progress=gr.Progress()):
    if not question or not question.strip():
        raise gr.Error("First enter a research question.")
    try:
        progress(0.08, desc="Launching AURA pipeline...")
        result = run_aura(question.strip(), max_papers=3, max_datasets=3, max_repositories=2, save_output=True)
        progress(0.9, desc="Rendering workspace...")
        output = build_presentable_output(result, mode="live")
        return (render_status("Live research completed successfully.", "success"), render_pipeline("live"), *output)
    except Exception as e:
        return (
            render_status(f"Live research failed. Load Demo Snapshot for a reliable showcase. Error: {e}", "error"),
            render_pipeline("error"),
            render_empty_block("Run failed", "The live pipeline encountered an external-service error."),
            render_empty_block("Papers", "No results available."),
            render_empty_block("Datasets", "No results available."),
            render_empty_block("Code", "No results available."),
            render_empty_block("Verified Claims", "No results available."),
            "# Analysis\n\nLive execution failed.",
            "# Decision\n\nLive execution failed.",
            "# Roadmap\n\nLive execution failed.",
            "# Full Report\n\nLive execution failed.",
            None,
        )


def load_demo(question):
    result = build_demo_result(question)
    output = build_presentable_output(result, mode="demo")
    return (render_status("Demo snapshot loaded — ready for a polished walkthrough.", "demo"), render_pipeline("demo"), *output)


def reset_workspace():
    return (
        "",
        render_status("Ready. Run live research or load the demo snapshot.", "info"),
        render_pipeline("idle"),
        render_empty_block("AURA Workspace", "Run live research or load the demo snapshot."),
        render_empty_block("Papers", "No paper results yet."),
        render_empty_block("Datasets", "No dataset results yet."),
        render_empty_block("Code", "No repository results yet."),
        render_empty_block("Verified Claims", "No verified claims yet."),
        "# Analysis\n\nNo analysis available yet.",
        "# Decision\n\nNo decision available yet.",
        "# Roadmap\n\nNo roadmap available yet.",
        "# Full Report\n\nNo report available yet.",
        None,
    )


CSS = """
:root{--bg:#06101f;--panel:#0c1729;--text:#eef3fb;--muted:#8ea0bb;--border:rgba(148,163,184,.16);--accent:#7c3aed;--accent2:#2563eb}
html,body,.gradio-container{background:radial-gradient(circle at 15% 0%,rgba(124,58,237,.18),transparent 30%),radial-gradient(circle at 85% 10%,rgba(37,99,235,.12),transparent 28%),linear-gradient(180deg,#06101f 0%,#040b17 100%)!important;color:var(--text)!important;font-family:Inter,ui-sans-serif,system-ui,sans-serif!important}
.gradio-container{max-width:1450px!important;margin:auto!important}
.hero-card,.panel-card,.input-wrap,.metric-card,.source-card,.claim-card,.empty-card,.hero-insight{border:1px solid var(--border);background:rgba(12,23,41,.78);border-radius:24px;box-shadow:0 18px 55px rgba(0,0,0,.18)}
.hero-card{padding:42px;margin:18px 0 20px;background:linear-gradient(145deg,rgba(12,23,41,.95),rgba(8,15,28,.92))}
.hero-kicker,.panel-kicker{color:#a78bfa;letter-spacing:.2em;font-size:11px;font-weight:800}.hero-main{margin-top:14px;font-size:54px;line-height:1.03;letter-spacing:-.05em;font-weight:800;color:#f8fafc;max-width:800px}.hero-sub{margin-top:16px;max-width:860px;line-height:1.7;font-size:17px;color:#9eb0c7}.hero-flow{margin-top:25px;color:#73839c;font-size:13px}.panel-card{padding:22px;height:100%}.panel-title{margin:7px 0 16px;font-size:20px;font-weight:700}.input-wrap{padding:18px!important}.stage-list{display:grid;gap:10px}.stage-card{display:flex;gap:12px;align-items:center;border:1px solid rgba(148,163,184,.1);border-radius:16px;padding:12px 14px}.stage-dot{width:10px;height:10px;border-radius:999px}.stage-dot.pending{background:#475569}.stage-dot.done{background:#10b981}.stage-dot.warn{background:#f59e0b}.stage-title,.source-title,.claim-title,.empty-title{font-weight:750;color:#f1f5f9}.stage-sub,.source-meta,.source-reason,.claim-reason,.empty-sub{color:#91a3bb;font-size:12px}.status-card{border:1px solid var(--border);border-radius:18px;padding:16px 18px;margin:16px 0}.status-label{font-size:11px;letter-spacing:.18em;font-weight:800;margin-bottom:8px}.status-success{background:rgba(16,185,129,.08)}.status-error{background:rgba(239,68,68,.08)}.status-demo{background:rgba(124,58,237,.10)}.overview-wrap{display:grid;grid-template-columns:1.2fr 1fr;gap:16px}.hero-insight{padding:24px;background:linear-gradient(145deg,rgba(124,58,237,.10),rgba(37,99,235,.07))}.hero-title{font-size:28px;font-weight:800}.hero-summary{margin-top:12px;line-height:1.72}.hero-confidence{margin-top:14px;color:#9fb0c6}.metrics-grid{display:grid;grid-template-columns:repeat(3,minmax(110px,1fr));gap:12px}.metric-card{padding:18px}.metric-value{font-size:30px;font-weight:800}.metric-label{color:#8ea0bb;font-size:13px}.source-card{display:flex;gap:16px;padding:18px;margin-bottom:12px}.source-index{width:36px;color:#64748b;font-family:monospace}.source-main{flex:1}.source-meta{margin-top:6px}.source-reason,.claim-reason{margin-top:12px;line-height:1.6}.source-bottom,.claim-top{display:flex;justify-content:space-between;align-items:center;margin-top:14px}.badge{display:inline-flex;border-radius:999px;padding:5px 10px;font-size:11px;font-weight:800}.badge-score{background:rgba(34,211,238,.09);color:#67e8f9}.badge-high{background:rgba(16,185,129,.1);color:#6ee7b7}.badge-medium{background:rgba(245,158,11,.1);color:#fde68a}.badge-low{background:rgba(239,68,68,.1);color:#fca5a5}.claim-card,.empty-card{padding:18px;margin-bottom:12px}.empty-card{text-align:center;padding:28px}#live-btn{background:linear-gradient(100deg,#7c3aed,#2563eb)!important;border:none!important;border-radius:16px!important;min-height:54px;font-weight:800!important}#demo-btn,#clear-btn{border-radius:16px!important;min-height:54px}footer{display:none!important}
"""

HEADER = """
<div class="hero-card"><div class="hero-kicker">AURA / RESEARCH INTELLIGENCE</div><div class="hero-main">From questions to evidence-backed decisions.</div><div class="hero-sub">A multi-agent scientific research workspace that discovers sources, verifies evidence, compares approaches, and turns research into an actionable roadmap.</div><div class="hero-flow">PLAN → DISCOVER → VERIFY → ANALYZE → DECIDE → BUILD</div></div>
"""

with gr.Blocks(title=APP_NAME) as demo:
    gr.HTML(f"<style>{CSS}</style>")
    gr.HTML(HEADER)
    with gr.Row():
        with gr.Column(scale=7):
            with gr.Group(elem_classes=["input-wrap"]):
                question = gr.Textbox(label="RESEARCH QUESTION", placeholder="I want to build a solar flare prediction system...", lines=5)
                with gr.Row():
                    live_btn = gr.Button("Run Live Research →", elem_id="live-btn")
                    demo_btn = gr.Button("Load Demo Snapshot", elem_id="demo-btn")
                    clear_btn = gr.Button("Reset", elem_id="clear-btn")
        with gr.Column(scale=5):
            pipeline = gr.HTML(render_pipeline("idle"))

    status = gr.HTML(render_status("Ready. Run live research or load the demo snapshot.", "info"))

    with gr.Tabs():
        with gr.Tab("Overview"): overview = gr.HTML(render_empty_block("AURA Workspace", "Run live research or load the demo snapshot."))
        with gr.Tab("Papers"): papers = gr.HTML(render_empty_block("Papers", "No paper results yet."))
        with gr.Tab("Datasets"): datasets = gr.HTML(render_empty_block("Datasets", "No dataset results yet."))
        with gr.Tab("Code"): repositories = gr.HTML(render_empty_block("Code", "No repository results yet."))
        with gr.Tab("Verified Claims"): claims = gr.HTML(render_empty_block("Verified Claims", "No verified claims yet."))
        with gr.Tab("Analysis"): analysis = gr.Markdown("# Analysis\n\nNo analysis available yet.")
        with gr.Tab("Decision"): decision = gr.Markdown("# Decision\n\nNo decision available yet.")
        with gr.Tab("Roadmap"): roadmap = gr.Markdown("# Roadmap\n\nNo roadmap available yet.")
        with gr.Tab("Full Report"): report = gr.Markdown("# Full Report\n\nNo report available yet.")

    report_file = gr.File(label="Download Report", interactive=False)

    outputs = [status,pipeline,overview,papers,datasets,repositories,claims,analysis,decision,roadmap,report,report_file]
    live_btn.click(fn=run_live, inputs=[question], outputs=outputs)
    demo_btn.click(fn=load_demo, inputs=[question], outputs=outputs)
    clear_btn.click(fn=reset_workspace, inputs=[], outputs=[question,*outputs])

if __name__ == "__main__":
    demo.queue()
    demo.launch(server_name="0.0.0.0", server_port=7860, share=True, show_error=True)
