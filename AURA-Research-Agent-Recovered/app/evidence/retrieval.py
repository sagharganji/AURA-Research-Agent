"""Lightweight retrieval placeholder for the MVP.

A true embedding/vector-store RAG layer is a planned extension.
"""


def retrieve_evidence(query: str, evidence_items: list, top_k: int = 5):
    query_words = set(query.lower().split())
    scored = []
    for item in evidence_items:
        text = str(item).lower()
        score = sum(word in text for word in query_words)
        scored.append((score, item))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [item for score, item in scored[:top_k] if score > 0]
