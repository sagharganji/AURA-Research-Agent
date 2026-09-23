from typing import List, Dict, Any

from app.llm import (
    FAST_MODEL,
    generate_with_fallback,
    clean_json_response,
)

from app.tools.github import (
    fetch_github_readme,
)


CODE_RELEVANCE_PROMPT = """
You are the Code Research Agent of AURA.

Your job is to evaluate whether a GitHub repository
is useful for the user's scientific or technical goal.

Use only the supplied repository metadata and README.

Evaluate:

- relevance to the user's research goal
- likely implementation value
- technical stack
- strengths
- limitations
- whether the repository appears reusable

Do not invent information.

Return ONLY valid JSON.
"""


def evaluate_code_relevance(
    user_question: str,
    repository: Dict[str, Any],
) -> Dict[str, Any]:

    readme = fetch_github_readme(
        repository.get("full_name", "")
    )

    prompt = f"""
{CODE_RELEVANCE_PROMPT}

USER QUESTION:
{user_question}

REPOSITORY:

Name:
{repository.get("full_name")}

Description:
{repository.get("description")}

URL:
{repository.get("url")}

Stars:
{repository.get("stars")}

Forks:
{repository.get("forks")}

Language:
{repository.get("language")}

Topics:
{repository.get("topics")}

Updated at:
{repository.get("updated_at")}

README:
{readme}

Return JSON using exactly this structure:

{{
    "relevant": true,
    "relevance_score": 0.0,
    "reason": "short explanation",
    "technical_stack": [],
    "possible_uses": [],
    "strengths": [],
    "limitations": [],
    "reusable": true
}}
"""

    response = generate_with_fallback(
        prompt,
        preferred_model=FAST_MODEL,
    )

    return clean_json_response(
        response.text
    )


def evaluate_repositories(
    user_question: str,
    repositories: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:

    results = []

    for repository in repositories:

        evaluation = evaluate_code_relevance(
            user_question,
            repository,
        )

        results.append({
            "repository": repository,
            "evaluation": evaluation,
        })

    return results
