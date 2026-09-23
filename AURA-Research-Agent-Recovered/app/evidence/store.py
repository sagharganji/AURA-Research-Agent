from typing import List, Dict, Any


class EvidenceStore:
    def __init__(self):
        self.items: List[Dict[str, Any]] = []

    def add(self, item: Dict[str, Any]):
        self.items.append(item)

    def add_many(self, items: List[Dict[str, Any]]):
        self.items.extend(items)

    def all(self) -> List[Dict[str, Any]]:
        return self.items

    def by_source_type(self, source_type: str) -> List[Dict[str, Any]]:
        return [item for item in self.items if item.get("source_type") == source_type]

    def clear(self):
        self.items = []


def build_unified_evidence(papers, datasets, repositories):
    evidence = []

    for item in papers:
        paper = item.get("paper", {})
        evaluation = item.get("evaluation", {})
        evidence.append({
            "source_type": "paper",
            "source_id": paper.get("id"),
            "title": paper.get("title"),
            "url": paper.get("url"),
            "doi": paper.get("doi"),
            "content": paper.get("abstract"),
            "relevance_score": evaluation.get("relevance_score"),
            "methods": evaluation.get("methods", []),
            "datasets": evaluation.get("datasets", []),
            "key_results": evaluation.get("key_results", []),
            "limitations": evaluation.get("limitations", []),
        })

    for item in datasets:
        dataset = item.get("dataset", {})
        evaluation = item.get("evaluation", {})
        evidence.append({
            "source_type": "dataset",
            "source_id": dataset.get("id"),
            "title": dataset.get("title"),
            "url": dataset.get("url"),
            "doi": dataset.get("doi"),
            "content": dataset.get("description"),
            "relevance_score": evaluation.get("relevance_score"),
            "possible_uses": evaluation.get("possible_uses", []),
            "strengths": evaluation.get("strengths", []),
            "limitations": evaluation.get("limitations", []),
        })

    for item in repositories:
        repository = item.get("repository", {})
        evaluation = item.get("evaluation", {})
        evidence.append({
            "source_type": "repository",
            "source_id": repository.get("id"),
            "title": repository.get("full_name"),
            "url": repository.get("url"),
            "content": repository.get("description"),
            "relevance_score": evaluation.get("relevance_score"),
            "technical_stack": evaluation.get("technical_stack", []),
            "possible_uses": evaluation.get("possible_uses", []),
            "strengths": evaluation.get("strengths", []),
            "limitations": evaluation.get("limitations", []),
            "reusable": evaluation.get("reusable"),
        })

    return evidence
