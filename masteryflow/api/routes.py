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
    """Evaluate 6 deterministic pedagogical rules and yield next learning decision."""
    decision = next_action(student_id=student_id)
    action_val = decision.action.value if hasattr(decision.action, 'value') else str(decision.action)
    return {
        "action": action_val,
        "target_concept": decision.target_concept,
        "target_concept_name": decision.target_concept_name,
        "reason": decision.reason,
        "rule_number": decision.rule_number,
        "rule_name": decision.rule_name,
        "p_eff": decision.p_eff,
        "evidence_sum": decision.evidence_sum,
        "status": decision.status,
        "is_fragile": decision.is_fragile,
        "config_version": decision.config_version,
        "inputs_json": decision.inputs_json
    }


@router.get("/state/{student_id}")
def get_state(student_id: str):
    """Retrieve full cognitive vector, virtual clock, and concept records for a learner."""
    return get_student_state(student_id=student_id)


@router.get("/student/{student_id}/mastery")
def get_student_mastery_endpoint(student_id: str):
    """Retrieve per-concept cognitive mastery dictionary for student UI."""
    state = get_student_state(student_id=student_id)
    return {"status": "success", "student_id": student_id, "mastery": state.get("concepts", {})}


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
