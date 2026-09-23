from pathlib import Path
import json


def _bullets(items):
    if not items:
        return "- None identified\n"

    return "".join(
        f"- {item}\n"
        for item in items
    )


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
    lines = []

    lines.append(
        "# AURA — AI Research & Decision Report\n"
    )

    lines.append(
        "## Research Question\n"
    )
    lines.append(
        f"{question.strip()}\n"
    )

    lines.append(
        "## Research Plan\n"
    )

    lines.append(
        f"**Goal:** {plan.get('goal', '')}\n"
    )

    lines.append(
        f"**Domain:** {plan.get('domain', '')}\n"
    )

    lines.append(
        "### Tasks\n"
    )

    for task in plan.get(
        "tasks",
        [],
    ):
        lines.append(
            f"- **{task.get('task_type')}** — "
            f"{task.get('purpose')}\n"
        )

    lines.append(
        "\n## Sources Discovered\n"
    )

    lines.append(
        f"- Papers: {len(papers)}\n"
    )
    lines.append(
        f"- Datasets: {len(datasets)}\n"
    )
    lines.append(
        f"- Code repositories: {len(repositories)}\n"
    )
    lines.append(
        f"- Unified evidence items: {len(evidence)}\n"
    )

    lines.append(
        "\n## Verified Claims\n"
    )

    for claim in verification.get(
        "claims",
        [],
    ):
        lines.append(
            f"### {claim.get('claim', 'Claim')}\n"
        )
        lines.append(
            f"- Confidence: {claim.get('confidence', '')}\n"
        )
        lines.append(
            f"- Reason: {claim.get('reason', '')}\n"
        )
        lines.append(
            "- Supporting evidence IDs: "
            f"{claim.get('supporting_evidence_ids', [])}\n"
        )

    lines.append(
        "\n## Key Findings\n"
    )

    lines.append(
        _bullets(
            analysis.get(
                "key_findings",
                []
            )
        )
    )

    lines.append(
        "\n## Method Comparison\n"
    )

    for method in analysis.get(
        "method_comparisons",
        [],
    ):
        lines.append(
            f"### {method.get('approach', 'Approach')}\n"
        )

        lines.append(
            "**Strengths**\n"
        )

        lines.append(
            _bullets(
                method.get(
                    "strengths",
                    []
                )
            )
        )

        lines.append(
            "**Limitations**\n"
        )

        lines.append(
            _bullets(
                method.get(
                    "limitations",
                    []
                )
            )
        )

    lines.append(
        "\n## Research Gaps\n"
    )

    lines.append(
        _bullets(
            analysis.get(
                "research_gaps",
                []
            )
        )
    )

    lines.append(
        "\n## Recommendation\n"
    )

    lines.append(
        f"{decision.get('recommended_direction', '')}\n"
    )

    lines.append(
        "\n### Why\n"
    )

    lines.append(
        _bullets(
            decision.get(
                "why",
                []
            )
        )
    )

    lines.append(
        "\n### Risks\n"
    )

    lines.append(
        _bullets(
            decision.get(
                "risks",
                []
            )
        )
    )

    lines.append(
        "\n### Confidence\n"
    )

    lines.append(
        f"{decision.get('confidence', '')}\n"
    )

    lines.append(
        "\n## Implementation Roadmap\n"
    )

    for phase in roadmap.get(
        "phases",
        [],
    ):

        lines.append(
            f"### Phase {phase.get('phase')} — "
            f"{phase.get('name')}\n"
        )

        lines.append(
            f"**Objective:** "
            f"{phase.get('objective', '')}\n"
        )

        lines.append(
            "\n**Tasks**\n"
        )

        lines.append(
            _bullets(
                phase.get(
                    "tasks",
                    []
                )
            )
        )

        lines.append(
            "\n**Deliverables**\n"
        )

        lines.append(
            _bullets(
                phase.get(
                    "deliverables",
                    []
                )
            )
        )

        lines.append(
            "\n**Evaluation**\n"
        )

        lines.append(
            _bullets(
                phase.get(
                    "evaluation",
                    []
                )
            )
        )

    lines.append(
        "\n## Major Risks\n"
    )

    lines.append(
        _bullets(
            roadmap.get(
                "major_risks",
                []
            )
        )
    )

    lines.append(
        "\n## Success Criteria\n"
    )

    lines.append(
        _bullets(
            roadmap.get(
                "success_criteria",
                []
            )
        )
    )

    lines.append(
        "\n## Evidence Sources\n"
    )

    for index, item in enumerate(
        evidence,
        start=1,
    ):

        title = item.get(
            "title",
            "Untitled source",
        )

        url = item.get(
            "url",
            "",
        )

        source_type = item.get(
            "source_type",
            "",
        )

        lines.append(
            f"{index}. [{source_type}] "
            f"{title}"
        )

        if url:
            lines.append(
                f" — {url}"
            )

        lines.append("\n")

    return "".join(lines)


def save_report(
    report_text: str,
    output_path: str,
):

    path = Path(output_path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        report_text,
        encoding="utf-8",
    )

    return str(path)
