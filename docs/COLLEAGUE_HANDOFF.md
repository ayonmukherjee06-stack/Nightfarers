# MasteryFlow: Machine Learning Engine Hand-Off & Integration Guide

**From:** Yash (ML Model & Knowledge Tracing Lead)  
**To:** Shreyash Jha (FastAPI & SQLite Persistence Lead), Soham Choudhury (Simulation & Test Lead), Ayon Mukherjee (Lead)  
**Package:** `masteryflow.engine`

---

## 1. Quick Import & Available Methods

Your colleagues can directly import and call the ML engine functions with zero setup:

```python
from masteryflow.engine import (
    record_attempt,
    next_action,
    get_student_state,
    apply_teacher_override,
    advance_student_time,
    get_cohort_heatmap,
    get_stuck_learners
)
```

---

## 2. Direct FastAPI Endpoint Implementations

Here is the exact drop-in implementation for Shreyash's `masteryflow/api/routes.py`:

### 1. `POST /api/attempt` (Record Student Attempt)
```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from masteryflow.engine import record_attempt

router = APIRouter()

class AttemptRequest(BaseModel):
    student_id: str
    concept_id: str
    is_correct: bool
    difficulty: float = 0.3
    is_transfer: bool = False
    hints_used: int = 0
    attempt_no: int = 1
    retry_gap_seconds: float = 999.0
    time_ms: int = 10000
    confidence: str = 'medium'

@router.post("/api/attempt")
def submit_attempt(payload: AttemptRequest):
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
```

### 2. `GET /api/next-action/{student_id}` (Get Next Decision)
```python
from masteryflow.engine import next_action

@router.get("/api/next-action/{student_id}")
def get_next_action(student_id: str):
    decision = next_action(student_id)
    return {
        "action": decision.action.value,
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
        "inputs_json": decision.inputs_json  # Save to SQLite decisions table for Test 8!
    }
```

### 3. `POST /api/teacher/override` (Persistent Teacher Override)
```python
from masteryflow.engine import apply_teacher_override

class OverrideRequest(BaseModel):
    student_id: str
    override_concept: str
    override_action: str
    teacher_name: str
    reason: str

@router.post("/api/teacher/override")
def teacher_override(payload: OverrideRequest):
    dec = apply_teacher_override(
        student_id=payload.student_id,
        override_concept=payload.override_concept,
        override_action=payload.override_action,
        teacher_name=payload.teacher_name,
        reason=payload.reason
    )
    return {"status": "persisted", "next_decision": dec.to_dict()}
```

### 4. `GET /api/teacher/heatmap` (Cohort Heatmap Matrix)
```python
from typing import List
from fastapi import Query
from masteryflow.engine import get_cohort_heatmap

@router.get("/api/teacher/heatmap")
def cohort_heatmap(student_ids: List[str] = Query(...)):
    return get_cohort_heatmap(student_ids)
```

### 5. `GET /api/teacher/stuck-learners` (Stuck-Learner Escalation Queue)
```python
from masteryflow.engine import get_stuck_learners

@router.get("/api/teacher/stuck-learners")
def stuck_learners_queue():
    return {"stuck_learners": get_stuck_learners()}
```

---

## 3. Test Verification Proofs for Soham

All 10 tests are green and ready:
```bash
python -m pytest tests/ -v
```
- Tests 1 to 4: BKT math, anti-gaming telemetry, DAG capping, Ebbinghaus decay
- Test 5: Teacher override persistence
- Tests 6 to 8: Twin divergence, cold-start propagation, decision reproducibility (0.000% variance)
- Test 9: 50 fraction questions exactness via `fractions.Fraction`
- Test 10: Colleague API service contract
