"""
MasteryFlow FastAPI REST API Endpoints
Designed for production backend integration, SQLite persistence, and UI consumption.
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

try:
    from backend.engine import (
        record_attempt,
        next_action,
        get_student_state,
        apply_teacher_override,
        advance_student_time,
        get_cohort_heatmap,
        get_stuck_learners,
    )
except ImportError:
    from masteryflow.engine import (
        record_attempt,
        next_action,
        get_student_state,
        apply_teacher_override,
        advance_student_time,
        get_cohort_heatmap,
        get_stuck_learners,
    )

router = APIRouter(prefix="/api", tags=["MasteryFlow Engine"])


class AttemptRequest(BaseModel):
    student_id: str
    concept_id: str
    is_correct: bool
    difficulty: float = Field(0.3, ge=0.0, le=1.0)
    is_transfer: bool = False
    hints_used: int = 0
    attempt_no: int = 1
    retry_gap_seconds: Optional[float] = 999.0
    time_ms: int = 10000
    confidence: str = 'medium'


class OverrideRequest(BaseModel):
    student_id: str
    override_concept: str
    override_action: str
    teacher_name: str
    reason: str


class AdvanceTimeRequest(BaseModel):
    student_id: str
    days: float = Field(..., gt=0.0)


@router.post("/attempt")
def submit_attempt(payload: AttemptRequest):
    """Record an interactive student attempt and compute Bayesian Knowledge Tracing posterior."""
    result = record_attempt(
        student_id=payload.student_id,
        concept_id=payload.concept_id,
        is_correct=payload.is_correct,
        difficulty=payload.difficulty,
        is_transfer=payload.is_transfer,
        hints_used=payload.hints_used,
        attempt_no=payload.attempt_no,
        retry_gap_seconds=payload.retry_gap_seconds,
        time_ms=payload.time_ms,
        confidence=payload.confidence
    )
    return {
        "status": "success",
        "concept_id": result.concept_id,
        "is_correct": result.is_correct,
        "prior_p": result.prior_p,
        "posterior_p": result.posterior_p,
        "new_p": result.new_p,
        "evidence_weight": result.evidence_weight,
        "evidence_sum": result.evidence_sum,
        "cognitive_status": result.status,
        "is_misconception": result.is_misconception,
        "uncertainty_se": result.uncertainty_se
    }


@router.get("/next-action/{student_id}")
def get_next_action(student_id: str):
    """Evaluate 6 deterministic pedagogical rules and yield next learning decision from SQLite database."""
    from backend.api.db import Database
    from backend.engine.graph import load_concept_graph
    from backend.engine.decide import next_action as compute_next_action, StudentState, ConceptState
    from backend.engine.decay import compute_effective_mastery
    from pathlib import Path

    db_path = str(Path(__file__).parent.parent.parent / "masteryflow.db")
    db = Database(db_path)
    graph = load_concept_graph(str(Path(__file__).parent.parent.parent / "data" / "concepts.json"))

    stu = db.get_student(student_id)
    active_cid = stu.get("active_concept_id", "C1") if stu else "C1"
    m_map = db.get_student_mastery_map(student_id)

    cstates = {}
    for cid, row in m_map.items():
        decayed_p_eff = compute_effective_mastery(
            p=row["p"],
            dt_days=0.0,
            stability_days=row["stability_days"]
        )
        cstates[cid] = ConceptState(
            p=row["p"],
            p_eff=decayed_p_eff,
            stability_days=row["stability_days"],
            evidence_sum=row["evidence_sum"],
            transfer_passed=bool(row["transfer_passed"]),
            is_fragile=bool(row["is_fragile"]),
            status=row["status"]
        )

    override = db.get_active_override(student_id)
    s_state = StudentState(
        student_id=student_id,
        active_concept_id=active_cid,
        concepts=cstates,
        active_override=override,
        last_attempt_time_days=0.0
    )
    decision = compute_next_action(s_state, graph)
    return decision.to_dict()


@router.get("/state/{student_id}")
def get_state(student_id: str):
    """Retrieve full cognitive vector, virtual clock, and concept records for a learner."""
    return get_student_state(student_id=student_id)


@router.get("/student/{student_id}/mastery")
def get_student_mastery_endpoint(student_id: str):
    """Retrieve per-concept cognitive mastery dictionary from SQLite DB."""
    from backend.api.db import Database
    from pathlib import Path
    db_path = str(Path(__file__).parent.parent.parent / "masteryflow.db")
    db = Database(db_path)
    m_map = db.get_student_mastery_map(student_id)
    return {"status": "success", "student_id": student_id, "mastery": m_map}


@router.post("/teacher/override")
def teacher_override(payload: OverrideRequest):
    """Apply an immutable human-in-the-loop teacher override to guide the learning path."""
    dec = apply_teacher_override(
        student_id=payload.student_id,
        override_concept=payload.override_concept,
        override_action=payload.override_action,
        teacher_name=payload.teacher_name,
        reason=payload.reason
    )
    return {"status": "persisted", "next_decision": dec.to_dict()}


@router.post("/time-travel")
def advance_time(payload: AdvanceTimeRequest):
    """Advance longitudinal virtual clock to evaluate Ebbinghaus memory decay."""
    state = advance_student_time(student_id=payload.student_id, days=payload.days)
    return {"status": "advanced", "student_state": state}


@router.get("/teacher/heatmap")
def cohort_heatmap(student_ids: List[str] = Query(...)):
    """Compute 2D cohort mastery heatmap matrix across all C1-C10 curriculum nodes."""
    return get_cohort_heatmap(student_ids)


@router.get("/teacher/stuck-learners")
def stuck_learners_queue():
    """List all learners flagged for immediate teacher intervention (Delta p < 0.05 over 3 cycles)."""
    return {"stuck_learners": get_stuck_learners()}
