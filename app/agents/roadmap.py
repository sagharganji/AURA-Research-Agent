from typing import Dict, Any
from app.llm import FAST_MODEL, generate_with_fallback, clean_json_response

ROADMAP_PROMPT = """
You are the Implementation Planning Agent of AURA.
Create a realistic ordered implementation roadmap based on verified evidence, analysis, and recommendation.
Include phases, objectives, tasks, resources, deliverables, evaluation criteria, and risks.
Return ONLY valid JSON.
"""


def create_roadmap(user_question: str, analysis: Dict[str, Any], decision: Dict[str, Any]) -> Dict[str, Any]:
    prompt = f"""
{ROADMAP_PROMPT}

USER QUESTION:
{user_question}

ANALYSIS:
{analysis}

DECISION:
{decision}

Return JSON:
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
    response = generate_with_fallback(prompt, preferred_model=FAST_MODEL)
    return clean_json_response(response.text)
