from typing import List, Dict, Any

from app.llm import (
    FAST_MODEL,
    generate_with_fallback,
    clean_json_response,
)


PAPER_RELEVANCE_PROMPT = """
You are the Paper Research Agent of AURA.

Evaluate whether a scientific paper is relevant
to the user's research question.

Use only information supported by the supplied
paper metadata and abstract.

Analyze:

- relevance
- methods
- datasets
- important findings
- limitations

Do not invent missing information.

Return ONLY valid JSON.
"""


def evaluate_paper_relevance(
    user_question: str,
    paper: Dict[str, Any],
) -> Dict[str, Any]:

    prompt = f"""
{PAPER_RELEVANCE_PROMPT}

USER QUESTION:
{user_question}

PAPER TITLE:
{paper.get("title")}

YEAR:
{paper.get("year")}

AUTHORS:
{paper.get("authors")}

DOI:
{paper.get("doi")}

URL:
{paper.get("url")}

ABSTRACT:
{paper.get("abstract")}

Return:

{{
    "relevant": true,
    "relevance_score": 0.0,
    "reason": "short explanation",
    "methods": [],
    "datasets": [],
    "key_results": [],
    "limitations": []
}}
"""

    response = generate_with_fallback(
        prompt,
        preferred_model=FAST_MODEL,
    )

    return clean_json_response(
        response.text
    )


def evaluate_papers(
    user_question: str,
    papers: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:

    results = []

    for paper in papers:

        evaluation = (
            evaluate_paper_relevance(
                user_question,
                paper,
            )
        )

        results.append({
            "paper": paper,
            "evaluation": evaluation,
        })

    return results
