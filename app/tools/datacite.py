from typing import List, Dict, Any

import requests


DATACITE_API = "https://api.datacite.org/dois"


def _search_datacite_once(
    query: str,
    max_results: int = 10,
) -> List[Dict[str, Any]]:

    params = {
        "query": query,
        "resource-type-id": "dataset",
        "page[size]": max_results,
    }

    response = requests.get(
        DATACITE_API,
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    return response.json().get(
        "data",
        [],
    )


def build_dataset_fallback_queries(
    query: str,
) -> List[str]:

    cleaned = (
        query
        .replace("dataset", "")
        .replace("datasets", "")
        .strip()
    )

    words = cleaned.split()

    queries = [
        query,
        cleaned,
    ]

    if len(words) > 4:
        queries.append(
            " ".join(words[:4])
        )

    if "solar" in cleaned.lower():
        queries.extend([
            "solar flare",
            "solar magnetic field",
            "SDO HMI",
        ])

    # Remove duplicates
    return list(
        dict.fromkeys(
            q.strip()
            for q in queries
            if q.strip()
        )
    )


def search_datacite_datasets(
    query: str,
    max_results: int = 10,
) -> List[Dict[str, Any]]:

    queries = build_dataset_fallback_queries(
        query
    )

    for candidate_query in queries:

        print(
            f"DataCite query: {candidate_query}"
        )

        results = _search_datacite_once(
            candidate_query,
            max_results=max_results,
        )

        if results:
            return results

    return []


def normalize_datacite_datasets(
    items: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:

    datasets = []

    for item in items:

        attributes = item.get(
            "attributes",
            {},
        )

        titles = attributes.get(
            "titles",
            [],
        )

        title = (
            titles[0].get("title")
            if titles
            else None
        )

        creators = []

        for creator in attributes.get(
            "creators",
            [],
        ):
            name = creator.get("name")

            if name:
                creators.append(name)

        descriptions = attributes.get(
            "descriptions",
            [],
        )

        description = ""

        if descriptions:
            description = descriptions[0].get(
                "description",
                "",
            )

        datasets.append({
            "id": item.get("id"),
            "doi": attributes.get("doi"),
            "title": title,
            "publisher": attributes.get(
                "publisher"
            ),
            "publication_year": attributes.get(
                "publicationYear"
            ),
            "creators": creators,
            "url": attributes.get("url"),
            "description": description,
        })

    return datasets


def deduplicate_datasets_by_title(
    datasets: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:

    seen = set()
    unique = []

    for dataset in datasets:

        title = (
            dataset.get("title")
            or ""
        ).strip().lower()

        if not title:
            continue

        if title in seen:
            continue

        seen.add(title)
        unique.append(dataset)

    return unique
