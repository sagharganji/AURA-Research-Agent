from typing import Dict, Any

from app.llm import (
    FAST_MODEL,
    generate_with_fallback,
    clean_json_response,
)


ROADMAP_PROMPT = """
You are the Implementation Planning Agent of AURA.

Create a realistic implementation roadmap based on
the verified evidence, analysis, and final recommendation.

The roadmap must be practical and ordered.

Include:

- phases
- objectives
- concrete tasks
- suggested tools/resources
- deliverables
- evaluation criteria
- major risks

Do not invent evidence.

Return ONLY valid JSON.
"""


def create_roadmap(
    user_question: str,
    analysis: Dict[str, Any],
    decision: Dict[str, Any],
) -> Dict[str, Any]:

    prompt = f"""
{ROADMAP_PROMPT}

USER QUESTION:
{user_question}

ANALYSIS:
{analysis}

DECISION:
{decision}

Return JSON exactly in this structure:

{{
  "phases": [
    {{
      "phase": 1,
      "name": "phase name",
      "objective": "objective",
      "tasks": [],
      "tools_resources": [],
      "deliverables": [],
      "evaluation": []
    }}
  ],
  "major_risks": [],
  "success_criteria": [],
  "roadmap_summary": "short summary"
}}
"""

    response = generate_with_fallback(
        prompt,
        preferred_model=FAST_MODEL,
    )

    return clean_json_response(
        response.text
    )
