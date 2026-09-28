"""
Test Contract for Colleagues (FastAPI Backend, SQLite, and Sim Lead Integration)
Verifies that all export functions in masteryflow.engine operate flawlessly.
"""
try:
    from backend.engine import (
        record_attempt,
        next_action,
        get_student_state,
        apply_teacher_override,
        advance_student_time,
        get_cohort_heatmap,
        get_stuck_learners,
        ActionType
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
        ActionType
    )


def test_colleague_api_contract():
    student_id = "STU_INTEGRATION_TEST"

    # 1. record_attempt()
    res = record_attempt(
        student_id=student_id,
        concept_id="C1",
        is_correct=True,
        difficulty=0.2,
        is_transfer=False,
        hints_used=0,
        time_ms=7500,
        confidence="high"
    )
    assert res.concept_id == "C1"
    assert res.is_correct is True
    assert res.new_p > res.prior_p

    # 2. next_action()
    dec = next_action(student_id=student_id)
    assert dec.action in [ActionType.PRACTICE, ActionType.ADVANCE]
    assert dec.target_concept in ["C1", "C2"]

    # 3. get_student_state()
    state = get_student_state(student_id=student_id)
    assert state['student_id'] == student_id
    assert "C1" in state['concepts']
    assert "C10" in state['concepts']

    # 4. apply_teacher_override()
    override_dec = apply_teacher_override(
        student_id=student_id,
        override_concept="C3",
        override_action="Practice",
        teacher_name="Mr. Sharma",
        reason="Targeted geometry preparation"
    )
    assert override_dec.target_concept == "C3"

    # 5. advance_student_time()
    advanced_state = advance_student_time(student_id=student_id, days=14.0)
    assert advanced_state['virtual_clock'] == 14.0 * 86400.0

    # 6. get_cohort_heatmap()
    matrix = get_cohort_heatmap([student_id])
    assert student_id in matrix
    assert len(matrix[student_id]) == 10

    # 7. get_stuck_learners()
    stuck_list = get_stuck_learners()
    assert isinstance(stuck_list, list)
