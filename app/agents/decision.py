from typing import Dict, Any

from app.llm import (
    FAST_MODEL,
    generate_with_fallback,
    clean_json_response,
)


DECISION_PROMPT = """
You are the Decision Agent of AURA.

Based on verified evidence and analysis,
produce a practical research or engineering recommendation.

The recommendation must:

1. Be grounded in the supplied evidence.
2. Explain why the recommended direction is appropriate.
3. Mention relevant alternatives.
4. Explain risks and trade-offs.
5. Avoid unsupported certainty.
6. Never invent evidence.

Return ONLY valid JSON.
"""


def create_decision(
    user_question: str,
    verification: Dict[str, Any],
    analysis: Dict[str, Any],
) -> Dict[str, Any]:

    prompt = f"""
{DECISION_PROMPT}

USER QUESTION:
{user_question}

VERIFICATION:
{verification}

ANALYSIS:
{analysis}

Return JSON exactly in this structure:

{{
  "recommended_direction": "main recommendation",
  "why": [],
  "alternatives": [
    {{
      "option": "alternative",
      "when_to_use": "condition"
    }}
  ],
  "risks": [],
  "tradeoffs": [],
  "confidence": "low|medium|high",
  "decision_summary": "short summary"
}}
"""

    response = generate_with_fallback(
        prompt,
        preferred_model=FAST_MODEL,
    )

    return clean_json_response(
        response.text
    )
