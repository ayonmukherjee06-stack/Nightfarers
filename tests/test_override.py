"""Test Suite for Teacher Persistent Override (Test 5 in Hackathon Rubric).

Authored by: Ayon Mukherjee (Team Lead & Orchestrator)
Tests persistent override storage, engine honoring human-in-the-loop decisions,
and complete audit log persistence.
"""

import pytest
import tempfile
import os
try:
    from backend.engine.contracts import ActionType, EngineConfig, CurriculumGraph, CANONICAL_CONCEPTS, ConceptMastery
    from backend.engine.override import OverrideManager
    from backend.engine.decide import make_decision
except ImportError:
    from masteryflow.engine.contracts import ActionType, EngineConfig, CurriculumGraph, CANONICAL_CONCEPTS, ConceptMastery
    from masteryflow.engine.override import OverrideManager
    from masteryflow.engine.decide import make_decision


@pytest.fixture
def temp_db():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.remove(path)


@pytest.fixture
def graph():
    return CurriculumGraph(CANONICAL_CONCEPTS)


@pytest.fixture
def config():
    return EngineConfig()


def test_test5_persistent_teacher_override(temp_db, graph, config):
    """Test 5 from Hackathon Rubric:
    Teacher overrides engine recommendation from Practice C3 to Remediate C1.
    Written to persistent SQLite overrides table; engine continues from new concept;
    audit history remains intact.
    """
    mgr = OverrideManager(db_path=temp_db)

    # Initial state: student practicing C3
    mastery_map = {cid: ConceptMastery(concept_id=cid, p_eff=0.70) for cid in CANONICAL_CONCEPTS}
    mastery_map["C1"].was_mastered = True
    mastery_map["C1"].p_eff = 0.90
    mastery_map["C2"].was_mastered = True
    mastery_map["C2"].p_eff = 0.85
    mastery_map["C3"].p_eff = 0.70

    # 1. Without override, engine would decide Practice C3
    d_before = make_decision("STU_100", "C3", mastery_map, graph, config)
    assert d_before.action == ActionType.PRACTICE
    assert d_before.target_concept_id == "C3"

    # 2. Teacher records persistent override to Remediate C1
    override_id = mgr.record_override(
        student_id="STU_100",
        action=ActionType.REMEDIATE_PREREQUISITE,
        target_concept_id="C1",
        reason="Teacher observed student struggling with basic denominator intuition during oral check.",
        teacher_id="TEACHER_SHUKLA",
    )
    assert override_id > 0

    # 3. Check active override
    active = mgr.get_active_override("STU_100")
    assert active is not None
    assert active["action"] == ActionType.REMEDIATE_PREREQUISITE.value
    assert active["target_concept_id"] == "C1"

    # 4. Engine now prioritizes human override
    d_after = make_decision(
        student_id="STU_100",
        current_concept_id="C3",
        mastery_map=mastery_map,
        graph=graph,
        config=config,
        active_override=active,
    )
    assert d_after.action == ActionType.REMEDIATE_PREREQUISITE
    assert d_after.target_concept_id == "C1"
    assert "Teacher Override" in d_after.rule_triggered
    assert "TEACHER_SHUKLA" in d_after.reason or "oral check" in d_after.reason

    # 5. Verify audit log persists
    logs = mgr.get_override_audit_log()
    assert len(logs) == 1
    assert logs[0]["student_id"] == "STU_100"
    assert logs[0]["target_concept_id"] == "C1"
    assert logs[0]["teacher_id"] == "TEACHER_SHUKLA"
