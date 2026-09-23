from typing import List, Dict, Any
from app.llm import FAST_MODEL, generate_with_fallback, clean_json_response
from app.tools.github import fetch_github_readme

CODE_RELEVANCE_PROMPT = """
You are the Code Research Agent of AURA.
Evaluate whether a GitHub repository is useful for the user's scientific or technical goal.
Use only supplied repository metadata and README. Evaluate relevance, implementation value,
technical stack, strengths, limitations, and reusability. Do not invent information.
Return ONLY valid JSON.
"""


def evaluate_code_relevance(user_question: str, repository: Dict[str, Any]) -> Dict[str, Any]:
    readme = fetch_github_readme(repository.get("full_name", ""))
    prompt = f"""
{CODE_RELEVANCE_PROMPT}

USER QUESTION: {user_question}
NAME: {repository.get('full_name')}
DESCRIPTION: {repository.get('description')}
URL: {repository.get('url')}
STARS: {repository.get('stars')}
FORKS: {repository.get('forks')}
LANGUAGE: {repository.get('language')}
TOPICS: {repository.get('topics')}
UPDATED AT: {repository.get('updated_at')}
README: {readme}

Return JSON:
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
    response = generate_with_fallback(prompt, preferred_model=FAST_MODEL)
    return clean_json_response(response.text)


def evaluate_repositories(user_question: str, repositories: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    results = []
    for repository in repositories:
        evaluation = evaluate_code_relevance(user_question, repository)
        results.append({"repository": repository, "evaluation": evaluation})
    return results
