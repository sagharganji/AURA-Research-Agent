"""Offline API contract checks: no credentials or outbound requests needed."""
from fastapi.testclient import TestClient

from app import api

client = TestClient(api.app)


def test_health_without_key(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    result = client.get("/health")
    assert result.status_code == 200
    assert result.json() == {"status": "ok", "gemini_configured": False}


def test_missing_api_key_blocks_research(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    result = client.post("/research", json={"question": "Investigate solar flare prediction"})
    assert result.status_code == 503


def test_short_question_rejected():
    assert client.post("/research", json={"question": "hi"}).status_code == 422


def test_mocked_success_contract(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "fake-test-key")
    monkeypatch.setattr(api, "execute_research", lambda question: {
        "papers": [{}], "datasets": [], "repositories": [],
        "evidence": [{}], "report": "# Example research output",
    })
    api._recent_all.clear()
    api._recent_by_ip.clear()
    result = client.post("/research", json={"question": "Investigate solar flare prediction"})
    assert result.status_code == 200
    data = result.json()
    assert data["mode"] == "live"
    assert data["counts"] == {"papers": 1, "datasets": 0, "repositories": 0, "evidence": 1}
    assert data["report"] == "# Example research output"


def test_usage_limit_with_mocked_runner(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "fake-test-key")
    monkeypatch.setattr(api, "execute_research", lambda question: {
        "papers": [], "datasets": [], "repositories": [], "evidence": [], "report": "ok",
    })
    api._recent_all.clear()
    api._recent_by_ip.clear()
    for _ in range(api.MAX_IP_DAILY):
        assert client.post("/research", json={"question": "Investigate solar flare prediction"}).status_code == 200
    assert client.post("/research", json={"question": "Investigate solar flare prediction"}).status_code == 429
