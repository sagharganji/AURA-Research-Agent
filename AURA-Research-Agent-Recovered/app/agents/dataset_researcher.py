from typing import List, Dict, Any
from app.llm import FAST_MODEL, generate_with_fallback, clean_json_response

DATASET_RELEVANCE_PROMPT = """
You are the Dataset Research Agent of AURA.
Evaluate whether a dataset is relevant to the user's scientific or technical research goal.
Use only supplied dataset metadata. Evaluate relevance, likely use, useful characteristics, and limitations.
Do not invent missing information. Return ONLY valid JSON.
"""


def evaluate_dataset_relevance(user_question: str, dataset: Dict[str, Any]) -> Dict[str, Any]:
    prompt = f"""
{DATASET_RELEVANCE_PROMPT}

USER QUESTION: {user_question}
TITLE: {dataset.get('title')}
DOI: {dataset.get('doi')}
PUBLISHER: {dataset.get('publisher')}
PUBLICATION YEAR: {dataset.get('publication_year')}
CREATORS: {dataset.get('creators')}
URL: {dataset.get('url')}
DESCRIPTION: {dataset.get('description')}

Return JSON:
{{
    "relevant": true,
    "relevance_score": 0.0,
    "reason": "short explanation",
    "possible_uses": [],
    "strengths": [],
    "limitations": []
}}
"""
    response = generate_with_fallback(prompt, preferred_model=FAST_MODEL)
    return clean_json_response(response.text)


def evaluate_datasets(user_question: str, datasets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [
        {"dataset": dataset, "evaluation": evaluate_dataset_relevance(user_question, dataset)}
        for dataset in datasets
    ]
