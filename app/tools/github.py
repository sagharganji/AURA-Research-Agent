import os
from typing import List, Dict, Any

import requests


GITHUB_SEARCH_API = (
    "https://api.github.com/search/repositories"
)


def build_github_fallback_queries(
    query: str,
) -> List[str]:

    cleaned = (
        query
        .replace("github", "")
        .replace("repository", "")
        .replace("repositories", "")
        .strip()
    )

    words = cleaned.split()

    queries = [
        query,
        cleaned,
    ]

    if len(words) > 5:
        queries.append(
            " ".join(words[:5])
        )

    if "solar" in cleaned.lower():
        queries.extend([
            "solar flare prediction",
            "solar flare machine learning",
            "SDO HMI solar flare",
        ])

    return list(
        dict.fromkeys(
            q.strip()
            for q in queries
            if q.strip()
        )
    )


def _search_github_once(
    query: str,
    max_results: int = 5,
) -> List[Dict[str, Any]]:

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "AURA-Research-Agent",
    }

    github_token = os.getenv(
        "GITHUB_TOKEN"
    )

    if github_token:
        headers["Authorization"] = (
            f"Bearer {github_token}"
        )

    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": max_results,
    }

    response = requests.get(
        GITHUB_SEARCH_API,
        headers=headers,
        params=params,
        timeout=30,
    )

    if response.status_code == 403:
        print(
            "⚠️ GitHub rate limit reached. "
            "Continuing without repository results."
        )
        return []

    response.raise_for_status()

    return response.json().get(
        "items",
        [],
    )


def search_github_repositories(
    query: str,
    max_results: int = 5,
) -> List[Dict[str, Any]]:

    queries = build_github_fallback_queries(
        query
    )

    for candidate_query in queries:

        print(
            f"GitHub query: {candidate_query}"
        )

        results = _search_github_once(
            candidate_query,
            max_results=max_results,
        )

        if results:
            return results

    return []


def normalize_github_repositories(
    repositories: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:

    normalized = []

    for repo in repositories:

        owner = (
            repo.get("owner")
            or {}
        )

        normalized.append({
            "id": repo.get("id"),
            "name": repo.get("name"),
            "full_name": repo.get(
                "full_name"
            ),
            "description": repo.get(
                "description"
            ),
            "url": repo.get(
                "html_url"
            ),
            "api_url": repo.get("url"),
            "owner": owner.get("login"),
            "stars": repo.get(
                "stargazers_count",
                0,
            ),
            "forks": repo.get(
                "forks_count",
                0,
            ),
            "language": repo.get(
                "language"
            ),
            "topics": repo.get(
                "topics",
                [],
            ),
            "default_branch": repo.get(
                "default_branch"
            ),
            "updated_at": repo.get(
                "updated_at"
            ),
        })

    return normalized


def fetch_github_readme(
    full_name: str,
) -> str:

    if not full_name:
        return ""

    headers = {
        "Accept": "application/vnd.github.raw+json",
        "User-Agent": "AURA-Research-Agent",
    }

    github_token = os.getenv(
        "GITHUB_TOKEN"
    )

    if github_token:
        headers["Authorization"] = (
            f"Bearer {github_token}"
        )

    url = (
        f"https://api.github.com/repos/"
        f"{full_name}/readme"
    )

    response = requests.get(
        url,
        headers=headers,
        timeout=30,
    )

    if response.status_code == 404:
        return ""

    response.raise_for_status()

    return response.text[:12000]
