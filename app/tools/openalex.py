import time
from typing import List, Dict, Any

import requests


OPENALEX_BASE_URL = "https://api.openalex.org/works"


def reconstruct_abstract(
    inverted_index
) -> str:

    if not inverted_index:
        return ""

    positions = []

    for word, indexes in inverted_index.items():
        for index in indexes:
            positions.append(
                (index, word)
            )

    positions.sort(
        key=lambda item: item[0]
    )

    return " ".join(
        word
        for _, word in positions
    )


def search_openalex(
    query: str,
    max_results: int = 10,
    email: str | None = None,
    max_retries: int = 3,
) -> List[Dict[str, Any]]:

    params = {
        "search": query,
        "per-page": max_results,
    }

    if email:
        params["mailto"] = email

    headers = {
        "User-Agent": (
            f"AURA-Research-Agent/1.0 "
            f"({email or 'research-agent'})"
        )
    }

    for attempt in range(
        max_retries
    ):

        response = requests.get(
            OPENALEX_BASE_URL,
            params=params,
            headers=headers,
            timeout=30,
        )

        if response.status_code == 200:
            return response.json().get(
                "results",
                [],
            )

        if response.status_code == 429:

            wait_time = 5 * (
                attempt + 1
            )

            print(
                "OpenAlex rate limit reached. "
                f"Waiting {wait_time} seconds..."
            )

            time.sleep(
                wait_time
            )

            continue

        response.raise_for_status()

    print(
        "⚠️ OpenAlex unavailable after retries. "
        "Continuing without paper results."
    )

    return []


def normalize_openalex_papers(
    works: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:

    papers = []

    for work in works:

        authors = []

        for authorship in work.get(
            "authorships",
            [],
        ):
            author = authorship.get(
                "author",
                {},
            )

            name = author.get(
                "display_name"
            )

            if name:
                authors.append(
                    name
                )

        primary_location = (
            work.get(
                "primary_location"
            )
            or {}
        )

        papers.append({
            "id": work.get("id"),
            "title": work.get("title"),
            "year": work.get(
                "publication_year"
            ),
            "doi": work.get("doi"),
            "url": primary_location.get(
                "landing_page_url"
            ),
            "authors": authors,
            "citation_count": work.get(
                "cited_by_count",
                0,
            ),
            "abstract": reconstruct_abstract(
                work.get(
                    "abstract_inverted_index"
                )
            ),
        })

    return papers
