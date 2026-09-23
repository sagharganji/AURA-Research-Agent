from pathlib import Path


def _bullets(items):
    if not items:
        return "- None identified\n"
    return "".join(f"- {item}\n" for item in items)


def build_final_report(
    question,
    plan,
    papers,
    datasets,
    repositories,
    evidence,
    verification,
    analysis,
    decision,
    roadmap,
):
    lines = ["# AURA — AI Research & Decision Report\n"]
    lines += ["## Research Question\n", f"{question.strip()}\n"]
    lines += ["## Research Plan\n", f"**Goal:** {plan.get('goal', '')}\n", f"**Domain:** {plan.get('domain', '')}\n", "### Tasks\n"]
    for task in plan.get("tasks", []):
        lines.append(f"- **{task.get('task_type')}** — {task.get('purpose')}\n")

    lines += [
        "\n## Sources Discovered\n",
        f"- Papers: {len(papers)}\n",
        f"- Datasets: {len(datasets)}\n",
        f"- Code repositories: {len(repositories)}\n",
        f"- Unified evidence items: {len(evidence)}\n",
        "\n## Verified Claims\n",
    ]

    for claim in verification.get("claims", []):
        lines += [
            f"### {claim.get('claim', 'Claim')}\n",
            f"- Confidence: {claim.get('confidence', '')}\n",
            f"- Reason: {claim.get('reason', '')}\n",
            f"- Supporting evidence IDs: {claim.get('supporting_evidence_ids', [])}\n",
        ]

    lines += ["\n## Key Findings\n", _bullets(analysis.get("key_findings", [])), "\n## Method Comparison\n"]
    for method in analysis.get("method_comparisons", []):
        lines += [
            f"### {method.get('approach', 'Approach')}\n",
            "**Strengths**\n",
            _bullets(method.get("strengths", [])),
            "**Limitations**\n",
            _bullets(method.get("limitations", [])),
        ]

    lines += [
        "\n## Research Gaps\n",
        _bullets(analysis.get("research_gaps", [])),
        "\n## Recommendation\n",
        f"{decision.get('recommended_direction', '')}\n",
        "\n### Why\n",
        _bullets(decision.get("why", [])),
        "\n### Risks\n",
        _bullets(decision.get("risks", [])),
        "\n### Confidence\n",
        f"{decision.get('confidence', '')}\n",
        "\n## Implementation Roadmap\n",
    ]

    for phase in roadmap.get("phases", []):
        lines += [
            f"### Phase {phase.get('phase')} — {phase.get('name')}\n",
            f"**Objective:** {phase.get('objective', '')}\n",
            "\n**Tasks**\n",
            _bullets(phase.get("tasks", [])),
            "\n**Deliverables**\n",
            _bullets(phase.get("deliverables", [])),
            "\n**Evaluation**\n",
            _bullets(phase.get("evaluation", [])),
        ]

    lines += [
        "\n## Major Risks\n",
        _bullets(roadmap.get("major_risks", [])),
        "\n## Success Criteria\n",
        _bullets(roadmap.get("success_criteria", [])),
        "\n## Evidence Sources\n",
    ]

    for index, item in enumerate(evidence, start=1):
        title = item.get("title", "Untitled source")
        url = item.get("url", "")
        source_type = item.get("source_type", "")
        lines.append(f"{index}. [{source_type}] {title}")
        if url:
            lines.append(f" — {url}")
        lines.append("\n")

    return "".join(lines)


def save_report(report_text: str, output_path: str):
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(report_text, encoding="utf-8")
    return str(path)
