from typing import List, Dict, Any
from app.llm import FAST_MODEL, generate_with_fallback, clean_json_response

ANALYSIS_PROMPT = """
You are the Analysis & Reasoning Agent of AURA.
Compare discovered approaches, identify strengths, limitations and research gaps,
distinguish strong conclusions from uncertain ones, and use only supplied evidence.
Return ONLY valid JSON.
"""


def analyze_research(user_question: str, evidence: List[Dict[str, Any]], verification: Dict[str, Any]) -> Dict[str, Any]:
    prompt = f"""
{ANALYSIS_PROMPT}

USER QUESTION:
{user_question}

EVIDENCE:
{evidence}

VERIFICATION:
{verification}

Return JSON:
{{
  "key_findings": [],
  "method_comparisons": [
    {{
      "approach": "approach name",
      "strengths": [],
      "limitations": [],
      "evidence_ids": []
    }}
  ],
  "research_gaps": [],
  "important_constraints": [],
  "uncertainties": [],
  "analysis_summary": "short synthesis"
}}
"""
    response = generate_with_fallback(prompt, preferred_model=FAST_MODEL)
    return clean_json_response(response.text)
