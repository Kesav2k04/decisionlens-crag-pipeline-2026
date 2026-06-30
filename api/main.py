# api/main.py
# FastAPI service that exposes the DecisionLens engine over HTTP.
# It is a thin wrapper: it imports run() from pipeline/agent.py and returns the
# same structured response the Streamlit app uses. No retrieval or generation
# logic is duplicated or changed here — this is purely a transport layer so a
# React/Three.js frontend can reach the identical Granite/Docling/CRAG pipeline.

import json
import os
import sys
import time
from pathlib import Path

import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parent.parent
for _p in (str(ROOT / "pipeline"), str(ROOT)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# Importing the agent loads the retriever once at startup (embedding + BM25 cache).
from agent import (  # noqa: E402
    run,
    GRANITE_MODEL,
    OLLAMA_URL,
    GOOD_THRESHOLD,
    POOR_THRESHOLD,
)

RESULTS_PATH = ROOT / "evaluation" / "results.json"
QUICK_ASKS = [
    "What makes a handball deliberate?",
    "When can VAR overturn an on-field decision?",
    "Explain the offside rule in simple terms",
    "What earns a straight red card?",
]
LANGUAGES = ["English", "Spanish", "Portuguese", "French"]
MAX_QUESTION_CHARS = 2000

app = FastAPI(
    title="DecisionLens API",
    version="1.0.0",
    description=(
        "Explains VAR and referee decisions from the official IFAB Laws of the Game "
        "and VAR Protocol, with citations, an evidence-sufficiency score, and honest "
        "abstention. Wraps the local IBM Granite + Docling + CRAG pipeline."
    ),
)

# CORS: "*" in dev; set ALLOWED_ORIGINS=https://your-app.vercel.app for production.
_cors_raw = os.environ.get("ALLOWED_ORIGINS", "*").strip()
_cors_origins = ["*"] if _cors_raw in ("", "*") else [o.strip() for o in _cors_raw.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


class ExplainRequest(BaseModel):
    question: str = Field(..., description="A football rule or VAR decision question.")
    mode: str = Field("fan", description="Explanation register: 'fan' or 'analyst'.")
    language: str = Field("English", description="Response language (see /api/config).")
    use_match_context: bool = Field(
        False, description="Prepend the Context Forge mock match metadata to the prompt."
    )


def _ollama_base() -> str:
    # OLLAMA_URL is .../api/generate — strip back to the host root.
    return OLLAMA_URL.rsplit("/api/", 1)[0]


@app.get("/api/health")
def health() -> dict:
    """Liveness + whether the local Granite/embedding backend is reachable."""
    ollama_ok = False
    models: list = []
    try:
        r = requests.get(f"{_ollama_base()}/api/tags", timeout=4)
        if r.status_code == 200:
            ollama_ok = True
            models = [m.get("name") for m in r.json().get("models", [])]
    except Exception:
        ollama_ok = False
    return {
        "status": "ok",
        "ollama_reachable": ollama_ok,
        "granite_model": GRANITE_MODEL,
        "granite_loaded": GRANITE_MODEL in models,
        "models": models,
    }


@app.get("/api/config")
def config() -> dict:
    """Static config the frontend needs: registers, languages, CRAG thresholds, examples."""
    return {
        "modes": ["fan", "analyst"],
        "languages": LANGUAGES,
        "quick_asks": QUICK_ASKS,
        "crag": {"good_threshold": GOOD_THRESHOLD, "poor_threshold": POOR_THRESHOLD},
        "decision_types": [
            "handball", "offside", "penalty", "red_card", "var_reviewability", "unknown",
        ],
        "max_question_chars": MAX_QUESTION_CHARS,
    }


@app.get("/api/metrics")
def metrics() -> dict:
    """The canonical evaluation summary (evaluation/results.json), for the UI's metrics view."""
    try:
        data = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
        return data.get("summary", {})
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="results.json not found; run evaluation/evaluate.py")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"could not read results.json: {type(exc).__name__}")


@app.post("/api/explain")
def explain(req: ExplainRequest) -> dict:
    """Run one question through the full DecisionLens pipeline and return the structured verdict."""
    question = (req.question or "").strip()
    if not question:
        raise HTTPException(status_code=422, detail="question must not be empty")
    if len(question) > MAX_QUESTION_CHARS:
        raise HTTPException(
            status_code=413,
            detail=f"question exceeds {MAX_QUESTION_CHARS} characters",
        )
    mode = req.mode if req.mode in ("fan", "analyst") else "fan"
    started = time.perf_counter()
    try:
        result = run(
            question,
            mode=mode,
            language=req.language or "English",
            use_match_context=bool(req.use_match_context),
        )
    except requests.exceptions.RequestException:
        raise HTTPException(
            status_code=503,
            detail="rule engine unreachable — is Ollama running with granite3.1-dense:8b?",
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"engine error: {type(exc).__name__}")
    result["api_latency_seconds"] = round(time.perf_counter() - started, 2)
    return result


@app.get("/")
def root() -> dict:
    return {"service": "DecisionLens API", "docs": "/docs", "health": "/api/health"}
