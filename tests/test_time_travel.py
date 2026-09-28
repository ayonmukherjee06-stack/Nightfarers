"""Test Suite for Virtual Clock Time Travel & Ebbinghaus Decay Trigger.

Authored by: Ayon Mukherjee (Team Lead & Orchestrator)
Tests that advancing the virtual clock by N days applies exponential Ebbinghaus decay,
causing effective retention p_eff to drop below the 0.60 threshold and trigger Spaced Review (Rule 3).
"""

import pytest
try:
    from backend.engine.contracts import CurriculumGraph, EngineConfig, CANONICAL_CONCEPTS, ConceptMastery, ActionType
    from frontend.components.time_travel import apply_time_travel_decay
    from backend.engine.decide import make_decision
except ImportError:
    from masteryflow.engine.contracts import CurriculumGraph, EngineConfig, CANONICAL_CONCEPTS, ConceptMastery, ActionType
    from masteryflow.ui.components.time_travel import apply_time_travel_decay
    from masteryflow.engine.decide import make_decision


@pytest.fixture
def graph():
    return CurriculumGraph(CANONICAL_CONCEPTS)


@pytest.fixture
def config():
    return EngineConfig()


def test_time_travel_zero_days_preserves_mastery():
    """Advancing by 0 days leaves mastery belief unchanged."""
    m = ConceptMastery(concept_id="C1", p_raw=0.92, p_eff=0.92, was_mastered=True)
    decayed_p = apply_time_travel_decay(p_eff=m.p_eff, days=0, decay_rate=0.035)
    assert decayed_p == 0.92


def test_time_travel_21_days_triggers_ebbinghaus_review(graph, config):
    """Advancing by 21 days drops p_eff from 0.90 to < 0.60, triggering Rule 3 Spaced Review."""
    # Initial state: student mastered C1 (0.90), currently practicing C3 (0.75)
    mastery_map = {cid: ConceptMastery(concept_id=cid, p_eff=0.10) for cid in CANONICAL_CONCEPTS}
    mastery_map["C1"].p_eff = 0.90
    mastery_map["C1"].was_mastered = True
    mastery_map["C2"].p_eff = 0.85
    mastery_map["C2"].was_mastered = True
    mastery_map["C3"].p_eff = 0.75

    # Without time travel, decision is Practice C3
    d_before = make_decision("STU_TIME_1", "C3", mastery_map, graph, config)
    assert d_before.action == ActionType.PRACTICE
    assert d_before.target_concept_id == "C3"

    # Advance clock by 21 days
    decayed_c1_p = apply_time_travel_decay(p_eff=mastery_map["C1"].p_eff, days=21, decay_rate=0.035)
    assert decayed_c1_p < config.review_threshold  # < 0.60
    mastery_map["C1"].p_eff = decayed_c1_p

    # Engine re-evaluates: Rule 3 (Spaced Review) activates on C1
    d_after = make_decision("STU_TIME_1", "C3", mastery_map, graph, config)
    assert d_after.action == ActionType.REVIEW
    assert d_after.target_concept_id == "C1"
    assert "Rule 3" in d_after.rule_triggered
