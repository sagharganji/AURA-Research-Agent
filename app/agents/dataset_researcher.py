from typing import List, Dict, Any

from app.llm import (
    FAST_MODEL,
    generate_with_fallback,
    clean_json_response,
)


DATASET_RELEVANCE_PROMPT = """
You are the Dataset Research Agent of AURA.

Your job is to evaluate whether a dataset is relevant
to the user's scientific or technical research goal.

Use only the supplied dataset metadata.

Evaluate:

- relevance to the user's problem
- likely use in model development or evaluation
- useful characteristics
- possible limitations

Do not invent missing information.

Return ONLY valid JSON.
"""


def evaluate_dataset_relevance(
    user_question: str,
    dataset: Dict[str, Any],
) -> Dict[str, Any]:

    prompt = f"""
{DATASET_RELEVANCE_PROMPT}

USER QUESTION:
{user_question}

DATASET:

Title:
{dataset.get("title")}

DOI:
{dataset.get("doi")}

Publisher:
{dataset.get("publisher")}

Publication year:
{dataset.get("publication_year")}

Creators:
{dataset.get("creators")}

URL:
{dataset.get("url")}

Description:
{dataset.get("description")}

Return JSON using exactly this structure:

{{
    "relevant": true,
    "relevance_score": 0.0,
    "reason": "short explanation",
    "possible_uses": [],
    "strengths": [],
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


def evaluate_datasets(
    user_question: str,
    datasets: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:

    results = []

    for dataset in datasets:

        evaluation = (
            evaluate_dataset_relevance(
                user_question,
                dataset,
            )
        )

        results.append({
            "dataset": dataset,
            "evaluation": evaluation,
        })

    return results
