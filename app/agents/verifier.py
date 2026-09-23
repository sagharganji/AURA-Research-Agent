from typing import List, Dict, Any
from app.llm import FAST_MODEL, generate_with_fallback, clean_json_response

VERIFICATION_PROMPT = """
You are the Verification Agent of AURA.
Inspect research evidence and assess the reliability of important claims.
Identify claims, supporting evidence, possible contradictions, and evidence quality.
Never invent support that is not present. Return ONLY valid JSON.
"""


def verify_evidence(user_question: str, evidence: List[Dict[str, Any]]) -> Dict[str, Any]:
    compact_evidence = []
    for index, item in enumerate(evidence):
        compact_evidence.append({
            "evidence_id": index + 1,
            "source_type": item.get("source_type"),
            "title": item.get("title"),
            "url": item.get("url"),
            "content": item.get("content"),
            "key_results": item.get("key_results", []),
            "limitations": item.get("limitations", []),
            "possible_uses": item.get("possible_uses", []),
        })

    prompt = f"""
{VERIFICATION_PROMPT}

USER QUESTION:
{user_question}

EVIDENCE:
{compact_evidence}

Return JSON:
{{
  "claims": [
    {{
      "claim": "important claim",
      "supporting_evidence_ids": [1, 2],
      "contradicting_evidence_ids": [],
      "confidence": "high",
      "reason": "short explanation"
    }}
  ],
  "contradictions": [
    {{
      "description": "contradiction summary",
      "evidence_ids": [1, 3]
    }}
  ],
  "overall_assessment": "short assessment of evidence quality"
}}
"""
    response = generate_with_fallback(prompt, preferred_model=FAST_MODEL)
    return clean_json_response(response.text)
