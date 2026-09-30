"""
MasteryFlow FastAPI REST Application Server (server.py).
Owner: Shreyash Jha (Backend & Persistence Lead)
Mounts all REST routes, CORS middleware, OpenAPI Swagger documentation (/docs),
and database lifecycle handlers.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

try:
    from backend.api.routes import router
    from backend.api.db import Database
except ImportError:
    from masteryflow.api.routes import router
    from masteryflow.api.db import Database

app = FastAPI(
    title="MasteryFlow Engine REST API",
    description=(
        "Production REST service for MasteryFlow: Explainable Adaptive Learning & Intervention Engine. "
        "Exposes BKT attempt ingestion, deterministic next-action evaluation, persistent teacher overrides, "
        "cohort heatmaps, and stuck-learner escalation queues."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Enable CORS for local Streamlit, web dashboards, and mobile clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include engine router
app.include_router(router)


@app.on_event("startup")
def startup_db_check():
    """Ensure database schema and curriculum tables are initialized."""
    db = Database("masteryflow.db")
    db.seed_curriculum()
    db.close()


@app.get("/", tags=["Health & Status"])
def root_status():
    """Root health check and engine metadata."""
    return {
        "status": "online",
        "service": "MasteryFlow Engine REST API",
        "version": "1.0.0",
        "domain": "Domain 04: Intelligent Educational Systems",
        "competition": "YUVA Megathon 2026",
        "docs_url": "/docs",
        "psychometric_invariants": {
            "pure_python_engine": True,
            "zero_llm_decision_loop": True,
            "deterministic_reproducibility": "100.0%"
        }
    }
