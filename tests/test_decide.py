"""Automated Test Suite for MasteryFlow Pedagogical Decision Engine (decide.py).

Authored by: Ayon Mukherjee (Team Lead & Orchestrator)
Tests the 6 deterministic ordered rules, prerequisite recursive walks,
stagnation detection, retention decay reviews, and snapshot reproducibility (Test 8).
"""

import pytest
try:
    from backend.engine.contracts import (
        ActionType,
        ConceptMastery,
        CurriculumGraph,
        EngineConfig,
        Decision,
        CANONICAL_CONCEPTS,
    )
    from backend.engine.decide import (
        make_decision,
        reconstruct_decision_from_snapshot,
        check_stagnation,
        find_weakest_prerequisite,
        find_most_decayed_review,
    )
except ImportError:
    from masteryflow.engine.contracts import (
        ActionType,
        ConceptMastery,
        CurriculumGraph,
        EngineConfig,
        Decision,
        CANONICAL_CONCEPTS,
    )
    from masteryflow.engine.decide import (
        make_decision,
        reconstruct_decision_from_snapshot,
        check_stagnation,
        find_weakest_prerequisite,
        find_most_decayed_review,
    )


@pytest.fixture
def graph():
    """Returns the canonical 10-concept Fractions & Ratios DAG."""
    return CurriculumGraph(CANONICAL_CONCEPTS)


@pytest.fixture
def config():
    """Standard engine configuration matching hackathon requirements."""
    return EngineConfig(
        mastery_threshold=0.85,
        prereq_remediation_threshold=0.55,
        review_threshold=0.60,
        stagnation_delta=0.05,
        stagnation_cycles=3,
        inconsistency_cap_delta=0.25,
        config_version=1,
    )


@pytest.fixture
def fresh_mastery_map():
    """Initializes mastery dictionary for all 10 concepts at baseline."""
    return {
        cid: ConceptMastery(concept_id=cid, p_raw=0.10, p_eff=0.10)
        for cid in CANONICAL_CONCEPTS
    }


# ==================== RULE 1: TEACHER INTERVENTION TESTS ====================

def test_rule1_stagnation_triggers_teacher_intervention(graph, config, fresh_mastery_map):
    """Rule 1 fires when change in p < 0.05 across 3 consecutive attempts on the same concept."""
    # Student struggling on C2 with minimal gains
    c2 = fresh_mastery_map["C2"]
    c2.p_raw = 0.42
    c2.p_eff = 0.42
    c2.history_p = [0.39, 0.40, 0.41, 0.42]  # Gain is 0.42 - 0.39 = 0.03 (< 0.05) across 3 cycles
    c2.attempts_count = 5
    c2.errors_count = 3
    c2.hints_count = 4

    decision = make_decision(
        student_id="STU_001",
        current_concept_id="C2",
        mastery_map=fresh_mastery_map,
        graph=graph,
        config=config,
    )

    assert decision.action == ActionType.TEACHER_INTERVENTION
    assert decision.target_concept_id == "C2"
    assert "Rule 1" in decision.rule_triggered
    assert "stagnation" in decision.reason.lower() or "gain" in decision.reason.lower()
    assert decision.metadata.get("stagnation_detected") is True


def test_rule1_no_intervention_when_progress_is_sufficient(graph, config, fresh_mastery_map):
    """Rule 1 does not fire if gain across 3 cycles is >= 0.05."""
    c2 = fresh_mastery_map["C2"]
    c2.p_raw = 0.50
    c2.p_eff = 0.50
    c2.history_p = [0.35, 0.40, 0.45, 0.50]  # Gain is 0.15 (>= 0.05)
    fresh_mastery_map["C1"].p_eff = 0.85
    fresh_mastery_map["C1"].was_mastered = True

    decision = make_decision(
        student_id="STU_001",
        current_concept_id="C2",
        mastery_map=fresh_mastery_map,
        graph=graph,
        config=config,
    )

    assert decision.action != ActionType.TEACHER_INTERVENTION


# ==================== RULE 2: REMEDIATE PREREQUISITE TESTS ====================

def test_rule2_remediate_weakest_unmastered_prerequisite(graph, config, fresh_mastery_map):
    """Rule 2 triggers remediation when an upstream ancestor has p_eff < 0.55."""
    # Student practicing C7 (Equivalent ratios).
    # Prerequisites of C7 are C6 and C5. Transitive prereq is C2.
    # C2 has decayed/unmastered p_eff = 0.42 (< 0.55).
    fresh_mastery_map["C1"].p_eff = 0.85
    fresh_mastery_map["C1"].was_mastered = True

    fresh_mastery_map["C2"].p_eff = 0.42
    fresh_mastery_map["C2"].was_mastered = False  # Never mastered foundational gap

    fresh_mastery_map["C5"].p_eff = 0.60
    fresh_mastery_map["C6"].p_eff = 0.65
    fresh_mastery_map["C7"].p_eff = 0.48
    fresh_mastery_map["C7"].history_p = [0.30, 0.40, 0.48]

    decision = make_decision(
        student_id="STU_002",
        current_concept_id="C7",
        mastery_map=fresh_mastery_map,
        graph=graph,
        config=config,
    )

    assert decision.action == ActionType.REMEDIATE_PREREQUISITE
    assert decision.target_concept_id == "C2"
    assert "Rule 2" in decision.rule_triggered
    assert "C2" in decision.reason
    assert "42" in decision.reason or "0.42" in decision.reason


def test_rule2_selects_weakest_among_multiple_weak_prerequisites(graph, config, fresh_mastery_map):
    """When multiple upstream ancestors are below 0.55, remediate the weakest one first."""
    # Current C10. Prereqs are C8, C9.
    # Suppose C8 has p_eff=0.50, but C6 has p_eff=0.35
    fresh_mastery_map["C1"].p_eff = 0.85
    fresh_mastery_map["C2"].p_eff = 0.85
    fresh_mastery_map["C3"].p_eff = 0.85
    fresh_mastery_map["C4"].p_eff = 0.85
    fresh_mastery_map["C5"].p_eff = 0.85
    fresh_mastery_map["C6"].p_eff = 0.35  # Weakest ancestor
    fresh_mastery_map["C7"].p_eff = 0.52
    fresh_mastery_map["C8"].p_eff = 0.50
    fresh_mastery_map["C9"].p_eff = 0.85
    fresh_mastery_map["C10"].p_eff = 0.40
    fresh_mastery_map["C10"].history_p = [0.20, 0.30, 0.40]

    decision = make_decision(
        student_id="STU_003",
        current_concept_id="C10",
        mastery_map=fresh_mastery_map,
        graph=graph,
        config=config,
    )

    assert decision.action == ActionType.REMEDIATE_PREREQUISITE
    assert decision.target_concept_id == "C6"


# ==================== RULE 3: SPACED REVIEW TESTS ====================

def test_rule3_previously_mastered_concept_triggers_review(graph, config, fresh_mastery_map):
    """Rule 3 triggers Spaced Review for a previously mastered concept that decayed below 0.60."""
    # C1 was mastered in the past, but has decayed over time to 0.52 (< 0.60).
    fresh_mastery_map["C1"].p_eff = 0.52
    fresh_mastery_map["C1"].was_mastered = True  # Key difference: was once mastered

    # Current concept C3 is practicing fine
    fresh_mastery_map["C2"].p_eff = 0.70
    fresh_mastery_map["C3"].p_eff = 0.65
    fresh_mastery_map["C3"].history_p = [0.50, 0.58, 0.65]

    decision = make_decision(
        student_id="STU_004",
        current_concept_id="C3",
        mastery_map=fresh_mastery_map,
        graph=graph,
        config=config,
    )

    assert decision.action == ActionType.REVIEW
    assert decision.target_concept_id == "C1"
    assert "Rule 3" in decision.rule_triggered
    assert "review" in decision.reason.lower() or "retrieval" in decision.reason.lower()


def test_rule3_prioritizes_most_decayed_concept(graph, config, fresh_mastery_map):
    """When multiple mastered concepts have decayed, prioritize the one with lowest p_eff."""
    fresh_mastery_map["C1"].was_mastered = True
    fresh_mastery_map["C1"].p_eff = 0.58  # Decayed

    fresh_mastery_map["C2"].was_mastered = True
    fresh_mastery_map["C2"].p_eff = 0.45  # More severely decayed

    fresh_mastery_map["C3"].p_eff = 0.70
    fresh_mastery_map["C3"].history_p = [0.50, 0.60, 0.70]

    decision = make_decision(
        student_id="STU_005",
        current_concept_id="C3",
        mastery_map=fresh_mastery_map,
        graph=graph,
        config=config,
    )

    assert decision.action == ActionType.REVIEW
    assert decision.target_concept_id == "C2"


# ==================== RULE 4: PRACTICE TESTS ====================

def test_rule4_standard_practice_when_under_mastery_threshold(graph, config, fresh_mastery_map):
    """Rule 4 triggers standard practice within the Zone of Proximal Development."""
    fresh_mastery_map["C1"].p_eff = 0.90
    fresh_mastery_map["C1"].was_mastered = True

    fresh_mastery_map["C2"].p_eff = 0.72  # < 0.85
    fresh_mastery_map["C2"].history_p = [0.60, 0.66, 0.72]

    decision = make_decision(
        student_id="STU_006",
        current_concept_id="C2",
        mastery_map=fresh_mastery_map,
        graph=graph,
        config=config,
    )

    assert decision.action == ActionType.PRACTICE
    assert decision.target_concept_id == "C2"
    assert "Rule 4" in decision.rule_triggered


def test_rule4_fragile_concept_requires_practice(graph, config, fresh_mastery_map):
    """Rule 4 triggers Practice if the concept is flagged fragile due to prereq capping."""
    fresh_mastery_map["C1"].p_eff = 0.85
    fresh_mastery_map["C1"].was_mastered = True

    # C2 has p_eff=0.60. C4 scored high (p_raw=0.90) but is capped at 0.60 + 0.25 = 0.85 and marked fragile.
    fresh_mastery_map["C2"].p_eff = 0.60
    fresh_mastery_map["C4"].p_raw = 0.90
    fresh_mastery_map["C4"].p_eff = 0.85
    fresh_mastery_map["C4"].is_fragile = True
    fresh_mastery_map["C4"].history_p = [0.70, 0.78, 0.85]

    decision = make_decision(
        student_id="STU_007",
        current_concept_id="C4",
        mastery_map=fresh_mastery_map,
        graph=graph,
        config=config,
    )

    assert decision.action == ActionType.PRACTICE
    assert decision.target_concept_id == "C4"
    assert "fragile" in decision.reason.lower() or "prerequisite" in decision.reason.lower()


def test_rule4_practice_when_transfer_not_verified(graph, config, fresh_mastery_map):
    """Rule 4 continues practice if p_eff >= 0.85 but difficult transfer question hasn't been solved."""
    fresh_mastery_map["C1"].p_eff = 0.88
    fresh_mastery_map["C1"].was_mastered = False
    fresh_mastery_map["C1"].transfer_verified = False  # Easy streak only, no transfer proof
    fresh_mastery_map["C1"].history_p = [0.70, 0.80, 0.88]

    decision = make_decision(
        student_id="STU_008",
        current_concept_id="C1",
        mastery_map=fresh_mastery_map,
        graph=graph,
        config=config,
    )

    assert decision.action == ActionType.PRACTICE
    assert decision.target_concept_id == "C1"
    assert "transfer" in decision.reason.lower() or "provisional" in decision.reason.lower()


# ==================== RULE 5: ADVANCE TESTS ====================

def test_rule5_advance_to_next_unlocked_concept(graph, config, fresh_mastery_map):
    """Rule 5 advances student to the next topological concept when current is fully mastered."""
    fresh_mastery_map["C1"].p_eff = 0.92
    fresh_mastery_map["C1"].was_mastered = True
    fresh_mastery_map["C1"].transfer_verified = True
    fresh_mastery_map["C1"].history_p = [0.75, 0.84, 0.92]

    decision = make_decision(
        student_id="STU_009",
        current_concept_id="C1",
        mastery_map=fresh_mastery_map,
        graph=graph,
        config=config,
    )

    assert decision.action == ActionType.ADVANCE
    assert decision.target_concept_id == "C2"
    assert "Rule 5" in decision.rule_triggered
    assert "advance" in decision.reason.lower() or "unlocked" in decision.reason.lower()


# ==================== RULE 6: CHALLENGE TESTS ====================

def test_rule6_challenge_when_curriculum_fully_mastered(graph, config, fresh_mastery_map):
    """Rule 6 serves capstone challenge questions when all concepts are mastered."""
    for cid in fresh_mastery_map:
        fresh_mastery_map[cid].p_eff = 0.92
        fresh_mastery_map[cid].was_mastered = True
        fresh_mastery_map[cid].transfer_verified = True
        fresh_mastery_map[cid].history_p = [0.80, 0.86, 0.92]

    decision = make_decision(
        student_id="STU_010",
        current_concept_id="C10",
        mastery_map=fresh_mastery_map,
        graph=graph,
        config=config,
    )

    assert decision.action == ActionType.CHALLENGE
    assert decision.target_concept_id == "C10"
    assert "Rule 6" in decision.rule_triggered


def test_rule6_challenge_mode_teacher_override_flag(graph, config, fresh_mastery_map):
    """Rule 6 triggers if challenge_mode is explicitly enabled."""
    fresh_mastery_map["C1"].p_eff = 0.90
    fresh_mastery_map["C1"].was_mastered = True
    fresh_mastery_map["C1"].transfer_verified = True

    decision = make_decision(
        student_id="STU_011",
        current_concept_id="C1",
        mastery_map=fresh_mastery_map,
        graph=graph,
        config=config,
        challenge_mode=True,
    )

    assert decision.action == ActionType.CHALLENGE
    assert "challenge" in decision.reason.lower()


# ==================== TEST 6: TWIN HISTORIES DIVERGENCE (RUBRIC PROOF) ====================

def test_twin_histories_divergence(graph, config, fresh_mastery_map):
    """Test 6 from Hackathon Spec: Two students with identical current score on C3 diverge based on history.
    Student A has an unreviewed decayed prerequisite C1 -> triggers Spaced Review (C1).
    Student B has solid prerequisites -> triggers Practice (C3).
    """
    import copy

    # Student A: Current C3 p_eff=0.70, but previously mastered C1 decayed to 0.48
    student_a_map = copy.deepcopy(fresh_mastery_map)
    student_a_map["C1"].was_mastered = True
    student_a_map["C1"].p_eff = 0.48  # Decayed < 0.60
    student_a_map["C2"].p_eff = 0.80
    student_a_map["C2"].was_mastered = True
    student_a_map["C3"].p_eff = 0.70
    student_a_map["C3"].history_p = [0.55, 0.62, 0.70]

    # Student B: Same C3 p_eff=0.70, but C1 is intact (0.90)
    student_b_map = copy.deepcopy(fresh_mastery_map)
    student_b_map["C1"].was_mastered = True
    student_b_map["C1"].p_eff = 0.90
    student_b_map["C2"].p_eff = 0.80
    student_b_map["C2"].was_mastered = True
    student_b_map["C3"].p_eff = 0.70
    student_b_map["C3"].history_p = [0.55, 0.62, 0.70]

    decision_a = make_decision(
        student_id="STU_A",
        current_concept_id="C3",
        mastery_map=student_a_map,
        graph=graph,
        config=config,
    )

    decision_b = make_decision(
        student_id="STU_B",
        current_concept_id="C3",
        mastery_map=student_b_map,
        graph=graph,
        config=config,
    )

    # Identical current scores, divergent pedagogical paths
    assert decision_a.action == ActionType.REVIEW
    assert decision_a.target_concept_id == "C1"

    assert decision_b.action == ActionType.PRACTICE
    assert decision_b.target_concept_id == "C3"
    assert decision_a.action != decision_b.action


# ==================== TEST 8: DECISION REPRODUCIBILITY (RUBRIC PROOF) ====================

def test_decision_reproducibility_from_snapshot(graph, config, fresh_mastery_map):
    """Test 8 from Hackathon Spec: Recomputing from stored inputs_json produces exact same result."""
    fresh_mastery_map["C1"].p_eff = 0.88
    fresh_mastery_map["C1"].was_mastered = True
    fresh_mastery_map["C2"].p_eff = 0.42  # Weak prereq triggers Remediate
    fresh_mastery_map["C2"].was_mastered = False
    fresh_mastery_map["C7"].p_eff = 0.50
    fresh_mastery_map["C7"].history_p = [0.35, 0.42, 0.50]
    fresh_mastery_map["C7"].errors_count = 2
    fresh_mastery_map["C7"].hints_count = 2

    original_decision = make_decision(
        student_id="STU_042",
        current_concept_id="C7",
        mastery_map=fresh_mastery_map,
        graph=graph,
        config=config,
    )

    snapshot = original_decision.inputs_snapshot
    assert "p_eff" in snapshot
    assert "current_concept_id" in snapshot
    assert "config" in snapshot

    # Recompute strictly from the serialized snapshot dictionary
    reconstructed_decision = reconstruct_decision_from_snapshot(snapshot, graph)

    assert reconstructed_decision.action == original_decision.action
    assert reconstructed_decision.target_concept_id == original_decision.target_concept_id
    assert reconstructed_decision.rule_triggered == original_decision.rule_triggered
    assert reconstructed_decision.reason == original_decision.reason
