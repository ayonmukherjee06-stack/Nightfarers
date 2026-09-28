"""
FastAPI Route Unit Tests.
Owner: Shreyash Jha (Backend & Persistence Lead)
Verifies that all API endpoint handlers execute flawlessly and produce valid contract responses.
"""

try:
    from backend.api.routes import (
        submit_attempt,
        get_next_action,
        get_state,
        teacher_override,
        advance_time,
        cohort_heatmap,
        stuck_learners_queue,
        AttemptRequest,
        OverrideRequest,
        AdvanceTimeRequest,
    )
except ImportError:
    from masteryflow.api.routes import (
        submit_attempt,
        get_next_action,
        get_state,
        teacher_override,
        advance_time,
        cohort_heatmap,
        stuck_learners_queue,
        AttemptRequest,
        OverrideRequest,
        AdvanceTimeRequest,
    )


def test_api_submit_attempt():
    payload = AttemptRequest(
        student_id="STU_API_TEST",
        concept_id="C1",
        is_correct=True,
        difficulty=0.3,
        is_transfer=False,
        hints_used=0,
        time_ms=8500,
        confidence="high"
    )
    res = submit_attempt(payload)
    assert res["status"] == "success"
    assert res["concept_id"] == "C1"
    assert res["is_correct"] is True
    assert res["new_p"] > res["prior_p"]


def test_api_next_action():
    dec = get_next_action(student_id="STU_API_TEST")
    assert dec["action"].upper() in ["PRACTICE", "ADVANCE", "REVIEW", "REMEDIATE"]
    assert dec["target_concept"] in ["C1", "C2"]
    assert dec["rule_number"] in [1, 2, 3, 4, 5, 6]


def test_api_teacher_override():
    payload = OverrideRequest(
        student_id="STU_API_TEST",
        override_concept="C3",
        override_action="Practice",
        teacher_name="Mr. Sharma",
        reason="Targeted geometry preparation"
    )
    res = teacher_override(payload)
    assert res["status"] == "persisted"
    assert res["next_decision"]["target_concept"] == "C3"


def test_api_advance_time():
    payload = AdvanceTimeRequest(student_id="STU_API_TEST", days=14.0)
    res = advance_time(payload)
    assert res["status"] == "advanced"
    assert res["student_state"]["virtual_clock"] == 14.0 * 86400.0


def test_api_teacher_heatmap_and_stuck_queue():
    matrix = cohort_heatmap(student_ids=["STU_API_TEST"])
    assert "STU_API_TEST" in matrix
    assert len(matrix["STU_API_TEST"]) == 10

    stuck = stuck_learners_queue()
    assert "stuck_learners" in stuck
    assert isinstance(stuck["stuck_learners"], list)
