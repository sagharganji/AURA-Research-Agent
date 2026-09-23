import os

from app.agents.planner import create_research_plan
from app.tools.openalex import search_openalex, normalize_openalex_papers
from app.agents.paper_researcher import evaluate_papers
from app.tools.datacite import search_datacite_datasets, normalize_datacite_datasets, deduplicate_datasets_by_title
from app.agents.dataset_researcher import evaluate_datasets
from app.tools.github import search_github_repositories, normalize_github_repositories
from app.agents.code_researcher import evaluate_repositories
from app.evidence.store import build_unified_evidence
from app.agents.verifier import verify_evidence
from app.agents.analyst import analyze_research
from app.agents.decision import create_decision
from app.agents.roadmap import create_roadmap
from app.report import build_final_report, save_report


def run_aura(
    question: str,
    max_papers: int = 5,
    max_datasets: int = 5,
    max_repositories: int = 3,
    save_output: bool = False,
):
    print("\n[1/12] Creating research plan...")
    plan = create_research_plan(question)

    paper_tasks = [task for task in plan.tasks if task.task_type == "paper_search"]
    dataset_tasks = [task for task in plan.tasks if task.task_type == "dataset_search"]
    code_tasks = [task for task in plan.tasks if task.task_type == "code_search"]

    paper_query = paper_tasks[0].query if paper_tasks else question
    dataset_query = dataset_tasks[0].query if dataset_tasks else question
    code_query = code_tasks[0].query if code_tasks else question

    print("\n[2/12] Searching papers...")
    raw_papers = search_openalex(
        query=paper_query,
        max_results=max_papers,
        email=os.getenv("OPENALEX_EMAIL"),
    )
    papers = normalize_openalex_papers(raw_papers)
    print(f"Found {len(papers)} papers.")

    print("\n[3/12] Evaluating papers...")
    evaluated_papers = evaluate_papers(question, papers)

    print("\n[4/12] Searching datasets...")
    raw_datasets = search_datacite_datasets(query=dataset_query, max_results=max_datasets)
    datasets = deduplicate_datasets_by_title(normalize_datacite_datasets(raw_datasets))
    print(f"Found {len(datasets)} datasets.")

    print("\n[5/12] Evaluating datasets...")
    evaluated_datasets = evaluate_datasets(question, datasets)

    print("\n[6/12] Searching GitHub...")
    raw_repositories = search_github_repositories(query=code_query, max_results=max_repositories)
    repositories = normalize_github_repositories(raw_repositories)
    print(f"Found {len(repositories)} repositories.")

    print("\n[7/12] Evaluating code...")
    evaluated_repositories = evaluate_repositories(question, repositories)

    print("\n[8/12] Building evidence store...")
    evidence = build_unified_evidence(evaluated_papers, evaluated_datasets, evaluated_repositories)
    print(f"Evidence items: {len(evidence)}")

    print("\n[9/12] Verifying evidence...")
    verification = verify_evidence(question, evidence)

    print("\n[10/12] Analyzing evidence...")
    analysis = analyze_research(question, evidence, verification)

    print("\n[11/12] Making decision...")
    decision = create_decision(question, verification, analysis)

    print("\n[12/12] Building roadmap...")
    roadmap = create_roadmap(question, analysis, decision)

    report = build_final_report(
        question=question,
        plan=plan.model_dump(),
        papers=evaluated_papers,
        datasets=evaluated_datasets,
        repositories=evaluated_repositories,
        evidence=evidence,
        verification=verification,
        analysis=analysis,
        decision=decision,
        roadmap=roadmap,
    )

    result = {
        "research_question": question,
        "research_plan": plan.model_dump(),
        "papers": evaluated_papers,
        "datasets": evaluated_datasets,
        "repositories": evaluated_repositories,
        "evidence": evidence,
        "verification": verification,
        "analysis": analysis,
        "decision": decision,
        "roadmap": roadmap,
        "report": report,
    }

    if save_output:
        output_path = "outputs/AURA_final_report.md"
        save_report(report, output_path)
        print(f"\n✅ Report saved to {output_path}")

    return result
