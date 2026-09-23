from typing import List, Dict, Any

from app.llm import (
    FAST_MODEL,
    generate_with_fallback,
    clean_json_response,
)


ANALYSIS_PROMPT = """
You are the Analysis & Reasoning Agent of AURA.

You receive verified research evidence.

Your job is to:

1. Compare the discovered approaches.
2. Identify important strengths.
3. Identify limitations and research gaps.
4. Distinguish strong conclusions from uncertain ones.
5. Use only the supplied evidence and verification results.
6. Do not invent papers, datasets, results, or claims.

Return ONLY valid JSON.
"""


def analyze_research(
    user_question: str,
    evidence: List[Dict[str, Any]],
    verification: Dict[str, Any],
) -> Dict[str, Any]:

    prompt = f"""
{ANALYSIS_PROMPT}

USER QUESTION:
{user_question}

EVIDENCE:
{evidence}

VERIFICATION:
{verification}

Return JSON exactly in this structure:

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

    response = generate_with_fallback(
        prompt,
        preferred_model=FAST_MODEL,
    )

    return clean_json_response(
        response.text
    )
