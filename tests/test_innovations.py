"""Test Suite for Phase 5 Technical Innovation Features.

Authored by: Ayon Mukherjee (Team Lead & Orchestrator)
Tests Innovation (b) Information-Gain Item Selection and
Innovation (c) Student Agency Request Logging.
"""

import pytest
import tempfile
import os
try:
    from backend.engine.contracts import ActionType, CANONICAL_CONCEPTS, ConceptMastery
    from backend.engine.information_gain import compute_entropy, compute_expected_information_gain, rank_items_by_information_gain
    from frontend.components.agency_modal import StudentAgencyManager
except ImportError:
    from masteryflow.engine.contracts import ActionType, CANONICAL_CONCEPTS, ConceptMastery
    from masteryflow.engine.information_gain import compute_entropy, compute_expected_information_gain, rank_items_by_information_gain
    from masteryflow.ui.components.agency_modal import StudentAgencyManager


@pytest.fixture
def temp_db():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    yield path
    if os.path.exists(path):
        try:
            os.remove(path)
        except OSError:
            pass


# ==================== INNOVATION (B): INFORMATION GAIN TESTS ====================

def test_entropy_calculation():
    """Entropy is maximum (1.0 bit) at p=0.5 and minimum (0.0 bit) at p=0.0 or 1.0."""
    assert round(compute_entropy(0.50), 3) == 1.000
    assert compute_entropy(0.0) == 0.0
    assert compute_entropy(1.0) == 0.0
    assert compute_entropy(0.85) < compute_entropy(0.50)


def test_information_gain_ranking():
    """Items with difficulty d closest to current mastery p provide maximum expected information gain."""
    student_p = 0.50  # Maximum uncertainty
    # Item 1: matched difficulty (d=0.50)
    # Item 2: too easy (d=0.10)
    # Item 3: too hard (d=0.95)
    items = [
        {"id": "Q1", "difficulty": 0.50, "concept_id": "C2"},
        {"id": "Q2", "difficulty": 0.10, "concept_id": "C2"},
        {"id": "Q3", "difficulty": 0.95, "concept_id": "C2"},
    ]

    ranked = rank_items_by_information_gain(student_p=student_p, candidate_items=items)
    assert len(ranked) == 3
    # Top item must be Q1 (matched difficulty yields highest info gain)
    assert ranked[0]["id"] == "Q1"
    assert ranked[0]["expected_ig"] > ranked[1]["expected_ig"]


# ==================== INNOVATION (C): STUDENT AGENCY TESTS ====================

def test_student_agency_request_logging(temp_db):
    """Verifies student agency requests ('Request Different Action') persist to SQLite audit trail."""
    mgr = StudentAgencyManager(db_path=temp_db)

    req_id = mgr.submit_agency_request(
        student_id="STU_DIYA",
        requested_action=ActionType.PRACTICE,
        requested_concept_id="C1",
        reason="I feel more confident practicing C1 before tackling C2 operations.",
    )
    assert req_id > 0

    requests = mgr.get_student_agency_requests("STU_DIYA")
    assert len(requests) == 1
    assert requests[0]["student_id"] == "STU_DIYA"
    assert requests[0]["requested_action"] == ActionType.PRACTICE.value
    assert requests[0]["requested_concept_id"] == "C1"
    assert "confident" in requests[0]["reason"]
