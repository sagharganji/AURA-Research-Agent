"""FastAPI adapter for the AURA research orchestration prototype.

The included limits are best-effort in-memory courtesy limits, not a secure
production protection mechanism. Restrict access before exposing paid inference.
"""
import logging
import os
import threading
import time
from collections import defaultdict, deque

from fastapi import FastAPI, HTTPException, Request
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

logger = logging.getLogger(__name__)
app = FastAPI(title="AURA Research API", version="0.1.0")
origins = [value.strip().rstrip("/") for value in os.getenv(
    "ALLOWED_ORIGINS", "http://localhost:5500,http://127.0.0.1:5500"
).split(",") if value.strip()]
app.add_middleware(
    CORSMiddleware, allow_origins=origins,
    allow_methods=["GET", "POST"], allow_headers=["Content-Type"],
)

DAY = 86400
MAX_GLOBAL_DAILY = int(os.getenv("AURA_DAILY_LIMIT", "15"))
MAX_IP_DAILY = int(os.getenv("AURA_PER_IP_DAILY_LIMIT", "2"))
_lock = threading.Lock()
_recent_all = deque()
_recent_by_ip = defaultdict(deque)


class ResearchRequest(BaseModel):
    question: str = Field(min_length=12, max_length=1200)

    @field_validator("question")
    @classmethod
    def check_question(cls, value):
        value = value.strip()
        if len(value) < 12:
            raise ValueError("Enter a meaningful research question.")
        return value


@app.get("/health")
def health():
    return {
        "status": "ok",
        "gemini_configured": bool(os.getenv("GEMINI_API_KEY")),
    }


def execute_research(question):
    # Import lazily so /health works even when the Gemini key is absent.
    from app.main import run_aura

    return run_aura(
        question,
        max_papers=2, max_datasets=2, max_repositories=1,
        save_output=False,
    )


def _take_slot(ip):
    now = time.monotonic()
    with _lock:
        while _recent_all and now - _recent_all[0] >= DAY:
            _recent_all.popleft()
        seen = _recent_by_ip[ip]
        while seen and now - seen[0] >= DAY:
            seen.popleft()
        if len(_recent_all) >= MAX_GLOBAL_DAILY or len(seen) >= MAX_IP_DAILY:
            return False
        _recent_all.append(now)
        seen.append(now)
        return True


@app.post("/research")
async def research(payload: ResearchRequest, request: Request):
    if not os.getenv("GEMINI_API_KEY"):
        raise HTTPException(
            status_code=503,
            detail="Gemini API key is not configured on the server.",
        )
    client_ip = request.client.host if request.client else "unknown"
    if not _take_slot(client_ip):
        raise HTTPException(
            status_code=429,
            detail="Demo usage limit reached. Please try again later.",
        )
    started = time.monotonic()
    try:
        result = await run_in_threadpool(execute_research, payload.question)
        return {
            "mode": "live",
            "question": payload.question,
            "counts": {
                "papers": len(result["papers"]),
                "datasets": len(result["datasets"]),
                "repositories": len(result["repositories"]),
                "evidence": len(result["evidence"]),
            },
            "report": result["report"],
            "elapsed_seconds": round(time.monotonic() - started, 1),
        }
    except Exception:
        logger.exception("Research pipeline failed")
        raise HTTPException(
            status_code=502,
            detail="The research pipeline failed. Check backend logs.",
        )
