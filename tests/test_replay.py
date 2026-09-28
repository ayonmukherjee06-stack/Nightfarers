"""Test Suite for Simulation Replay Runner and Cold Start Divergence (Test 7).

Authored by: Ayon Mukherjee (Team Lead & Orchestrator)
Tests multi-step simulation replay across all 4 student archetypes and
proves Test 7 Cold Start cognitive vector divergence.
"""

import pytest
try:
    from backend.engine.contracts import CurriculumGraph, EngineConfig, CANONICAL_CONCEPTS, ConceptMastery, ActionType
    from backend.sim.replay import load_personas, replay_persona
    from backend.engine.decide import make_decision
except ImportError:
    from masteryflow.engine.contracts import CurriculumGraph, EngineConfig, CANONICAL_CONCEPTS, ConceptMastery, ActionType
    from masteryflow.sim.replay import load_personas, replay_persona
    from masteryflow.engine.decide import make_decision


@pytest.fixture
def graph():
    return CurriculumGraph(CANONICAL_CONCEPTS)


@pytest.fixture
def config():
    return EngineConfig()


def test_all_4_personas_replay_verified():
    """Verifies that all 4 scripted persona profiles (Diya, Rohan, Aarav, Priya)
    execute through the real engine and achieve 100% expected action verification."""
    personas = load_personas()
    assert len(personas) == 4

    for p in personas:
        result = replay_persona(p)
        assert result["is_verified"] is True, f"Persona {p['name']} failed verification"
        assert len(result["steps"]) >= 1


def test_test7_cold_start_divergence(graph, config):
    """Test 7 from Hackathon Rubric:
    Students X and Y take a diagnostic test with opposite response patterns.
    Student X masters foundational C1, C2, but misses C7.
    Student Y misses C1, C2, but attempts C7.
    Produces distinct starting vectors and divergent starting action/targets.
    """
    # Student X: Strong foundation
    map_x = {cid: ConceptMastery(concept_id=cid, p_eff=0.10) for cid in CANONICAL_CONCEPTS}
    map_x["C1"].p_eff = 0.90
    map_x["C1"].was_mastered = True
    map_x["C1"].transfer_verified = True
    map_x["C2"].p_eff = 0.88
    map_x["C2"].was_mastered = True
    map_x["C2"].transfer_verified = True

    # Student Y: Weak foundation, attempted C7
    map_y = {cid: ConceptMastery(concept_id=cid, p_eff=0.10) for cid in CANONICAL_CONCEPTS}
    map_y["C1"].p_eff = 0.40
    map_y["C2"].p_eff = 0.35  # Weakest foundational ancestor
    map_y["C5"].p_eff = 0.60
    map_y["C6"].p_eff = 0.60
    map_y["C7"].p_eff = 0.45

    # Decision for Student X starting after C2
    decision_x = make_decision(
        student_id="STU_DIAG_X",
        current_concept_id="C2",
        mastery_map=map_x,
        graph=graph,
        config=config,
    )

    # Decision for Student Y starting on C7
    decision_y = make_decision(
        student_id="STU_DIAG_Y",
        current_concept_id="C7",
        mastery_map=map_y,
        graph=graph,
        config=config,
    )

    # Student X advances forward into C3
    assert decision_x.action == ActionType.ADVANCE
    assert decision_x.target_concept_id in ["C3", "C4", "C5", "C6"]

    # Student Y gets routed back to heal foundational C2
    assert decision_y.action == ActionType.REMEDIATE_PREREQUISITE
    assert decision_y.target_concept_id in ["C1", "C2"]

    # Guaranteed divergent cognitive trajectories
    assert decision_x.action != decision_y.action
    assert decision_x.target_concept_id != decision_y.target_concept_id
