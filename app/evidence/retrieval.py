"""
AURA Retrieval Layer

Real embedding-based RAG will be implemented
after the core research pipeline is stable.
"""


def retrieve_evidence(
    query: str,
    evidence_items: list,
    top_k: int = 5,
):
    """
    Temporary lightweight retrieval.

    This will later be replaced by
    semantic embedding retrieval.
    """

    query_words = set(
        query.lower().split()
    )

    scored = []

    for item in evidence_items:

        text = str(
            item
        ).lower()

        score = sum(
            word in text
            for word in query_words
        )

        scored.append(
            (score, item)
        )

    scored.sort(
        key=lambda x: x[0],
        reverse=True,
    )

    return [
        item
        for score, item
        in scored[:top_k]
        if score > 0
    ]
