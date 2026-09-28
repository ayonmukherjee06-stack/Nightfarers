"""
Test 5: Persistent Teacher Override & SQLite Persistence Engine.
Owner: Shreyash Jha & Soham Choudhury
Verifies instructor override authority, state preservation, and audit logging.
"""

import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from backend.api.db import Database
    from backend.engine.graph import load_concept_graph
    from backend.engine.decide import next_action, StudentState, ConceptState
except ImportError:
    from api.db import Database
    from engine.graph import load_concept_graph
    from engine.decide import next_action, StudentState, ConceptState


def test_5_persistent_teacher_override():
    """
    Test 5: Persistent Teacher Override
    Teacher overrides engine recommendation from 'Practice C3' to 'Remediate C1' with reason.
    Written to overrides table; next_action continues from new concept; student history intact.
    """
    db = Database(":memory:")
    c_path = Path(__file__).parent.parent / "data" / "concepts.json"
    q_path = Path(__file__).parent.parent / "data" / "questions.json"
    db.seed_curriculum(str(c_path), str(q_path))

    student_id = "STU_TEST_05"
    db.ensure_student(student_id, "Test Learner")
    graph = load_concept_graph(str(c_path))

    # Initial state would recommend Practice C3
    state = StudentState(
        student_id=student_id,
        active_concept_id="C3",
        concepts={
            "C1": ConceptState(p=0.90, p_eff=0.88, status="mastered"),
            "C2": ConceptState(p=0.85, p_eff=0.80, status="mastered"),
            "C3": ConceptState(p=0.60, p_eff=0.60, status="practicing")
        }
    )
    initial_decision = next_action(state, graph)
    assert initial_decision.action == "Practice"
    assert initial_decision.target_concept == "C3"

    # Teacher submits override: Remediate C1
    override_reason = "Teacher observed student struggling with basic denominator visualization."
    override_id = db.record_override(
        student_id=student_id,
        target_concept="C1",
        action="Remediate",
        reason=override_reason,
        teacher_name="Mr. Sharma"
    )

    # Verify override is persisted and active in DB
    active_override = db.get_active_override(student_id)
    assert active_override is not None
    assert active_override["target_concept"] == "C1"
    assert active_override["action"] == "Remediate"
    assert active_override["reason"] == override_reason

    # Attach active override to state
    state.active_override = active_override
    overridden_decision = next_action(state, graph)

    # Verify engine strictly obeys teacher override
    assert overridden_decision.action == "Remediate"
    assert overridden_decision.target_concept == "C1"
    assert override_reason in overridden_decision.reason

    # Verify audit log captures event
    audit = db.get_audit_trail(student_id)
    assert len(audit) >= 1
    assert audit[0]["actor"] == "Mr. Sharma"
    assert audit[0]["event_type"] == "TEACHER_OVERRIDE"
