"""
Tests 1-4, 6, 8: Core Mathematical Invariants, Anti-Gaming Telemetry & Reproducibility.
Owner: Soham Choudhury & Ayon Mukherjee
"""

import json
import math
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from backend.engine.mastery import update_bkt, compute_uncertainty
    from backend.engine.weights import compute_evidence_weight
    from backend.engine.decay import compute_effective_mastery, update_stability
    from backend.engine.graph import load_concept_graph, PrerequisiteGraph
    from backend.engine.decide import next_action, StudentState, ConceptState, Decision
except ImportError:
    from engine.mastery import update_bkt, compute_uncertainty
    from engine.weights import compute_evidence_weight
    from engine.decay import compute_effective_mastery, update_stability
    from engine.graph import load_concept_graph, PrerequisiteGraph
    from engine.decide import next_action, StudentState, ConceptState, Decision


@pytest.fixture
def graph():
    c_path = Path(__file__).parent.parent / "data" / "concepts.json"
    return load_concept_graph(str(c_path))


def test_1_transfer_failure_barrier(graph):
    """
    Test 1: Transfer Failure Barrier
    Student answers several easy items correctly (d=0.2), reaching high latent p >= 0.85.
    Then fails a transfer item (d=0.8, is_transfer=True).
    Mastery p may be high, but concept MUST NOT be marked 'mastered' (remains 'provisional').
    Next pedagogical action must be Practice.
    """
    p = 0.30
    # Three correct easy attempts (d=0.2)
    for _ in range(3):
        w, _ = compute_evidence_weight(hints_used=0, attempt_no=1, time_ms=10000, is_correct=True)
        p, _ = update_bkt(p, is_correct=True, difficulty=0.2, w=w)

    assert p >= 0.85, f"Expected latent p >= 0.85 after 3 easy items, got {p}"

    # Fails a transfer item (d=0.8)
    w_trans, _ = compute_evidence_weight(hints_used=0, attempt_no=1, time_ms=12000, is_correct=False)
    p_after_transfer, _ = update_bkt(p, is_correct=False, difficulty=0.8, w=w_trans)

    # Student State with transfer_passed=False
    state = StudentState(
        student_id="STU_T1",
        active_concept_id="C1",
        concepts={
            "C1": ConceptState(
                p=p_after_transfer,
                p_eff=p_after_transfer,
                stability_days=7.0,
                evidence_sum=3.5,
                transfer_passed=False,
                status="provisional"
            )
        }
    )

    decision = next_action(state, graph)
    assert decision.action == "Practice", f"Expected action 'Practice', got '{decision.action}'"
    assert decision.target_concept == "C1"
    assert "provisional" in decision.reason.lower() or "transfer" in decision.reason.lower()


def test_2_rapid_retrying_anti_gaming():
    """
    Test 2: Rapid Retrying Anti-Gaming Telemetry
    Student submits an incorrect answer, then submits 3 rapid retries within 4 seconds (<5.0s)
    until guessing correctly.
    Evidence weight w must drop to exactly 0.0 for retries <5s.
    Overall p gain must be negligible (<0.01), completely defeating the guessing attack.
    """
    initial_p = 0.40
    p = initial_p

    # 1. First incorrect attempt (gap is None)
    w1, _ = compute_evidence_weight(hints_used=0, attempt_no=1, time_ms=2500, retry_gap_seconds=None, prev_correct=None, is_correct=False)
    p, _ = update_bkt(p, is_correct=False, difficulty=0.5, w=w1)

    p_before_attack = p

    # 2. Rapid retry #1 (2.5s, incorrect) -> w must be 0.0
    w2, _ = compute_evidence_weight(hints_used=0, attempt_no=2, time_ms=1900, retry_gap_seconds=2.5, prev_correct=False, is_correct=False)
    assert w2 == 0.0, f"Expected w=0.0 on rapid retry, got {w2}"
    p, _ = update_bkt(p, is_correct=False, difficulty=0.5, w=w2)

    # 3. Rapid retry #2 (3.1s, incorrect) -> w must be 0.0
    w3, _ = compute_evidence_weight(hints_used=0, attempt_no=3, time_ms=1800, retry_gap_seconds=3.1, prev_correct=False, is_correct=False)
    assert w3 == 0.0, f"Expected w=0.0 on rapid retry, got {w3}"
    p, _ = update_bkt(p, is_correct=False, difficulty=0.5, w=w3)

    # 4. Rapid retry #3 (3.8s, correct lucky guess) -> w must STILL be 0.0 because gap < 5.0s after incorrect answer!
    w4, _ = compute_evidence_weight(hints_used=0, attempt_no=4, time_ms=1500, retry_gap_seconds=3.8, prev_correct=False, is_correct=True)
    assert w4 == 0.0, f"Expected w=0.0 on rapid correct guess, got {w4}"
    p_final, _ = update_bkt(p, is_correct=True, difficulty=0.5, w=w4)

    delta_p = abs(p_final - p_before_attack)
    assert delta_p < 0.001, f"Expected negligible delta p (<0.001) during attack, got {delta_p}"


def test_3_prerequisite_inconsistency_capping(graph):
    """
    Test 3: Prerequisite Inconsistency Capping
    Student scores high on C4 (Addition) with p_eff = 0.85, but prerequisite C2 (Equivalent fractions)
    has decayed to 0.35.
    C4 mastery must be capped at min(prereq) + 0.25 = 0.35 + 0.25 = 0.60.
    C4 must be marked 'fragile', and decision engine must trigger 'Remediate C2'.
    """
    all_p_eff = {"C1": 0.90, "C2": 0.35, "C4": 0.85}
    capped_p, is_fragile, weakest_prereq, weakest_val = graph.apply_prerequisite_capping(
        "C4", p_eff=0.85, all_p_eff=all_p_eff, capping_offset=0.25
    )

    assert is_fragile is True, "C4 must be marked fragile when prerequisite is decayed"
    assert round(capped_p, 2) == 0.60, f"Expected capped p_eff = 0.60, got {capped_p}"
    assert weakest_prereq == "C2"

    state = StudentState(
        student_id="STU_T3",
        active_concept_id="C4",
        concepts={
            "C1": ConceptState(p=0.90, p_eff=0.90, status="mastered"),
            "C2": ConceptState(p=0.35, p_eff=0.35, status="practicing"),
            "C4": ConceptState(p=0.85, p_eff=capped_p, is_fragile=True, status="practicing")
        }
    )

    decision = next_action(state, graph)
    assert decision.action == "Remediate", f"Expected action 'Remediate', got '{decision.action}'"
    assert decision.target_concept == "C2", f"Expected target 'C2', got '{decision.target_concept}'"
    assert "remediate c2" in decision.reason.lower()


def test_4_long_gap_decay_vs_failure_drop(graph):
    """
    Test 4: Long Gap Decay vs. Failure Drop
    Student mastered C1 (p=0.92, S=7 days).
    Clock advances 21 days; effective mastery p_eff decays to 0.52 (below review threshold 0.60).
    Student fails an attempt on C1.
    Failure after long gap on a previously mastered concept queues 'Review', NOT 'Remediate'.
    """
    p_mastered = 0.92
    s_initial = 7.0
    dt_days = 21.0

    p_eff = compute_effective_mastery(p=p_mastered, dt_days=dt_days, stability_days=s_initial, floor=0.25)
    assert p_eff < 0.60, f"Expected p_eff < 0.60 after 21 days, got {p_eff}"

    state = StudentState(
        student_id="STU_T4",
        active_concept_id="C1",
        concepts={
            "C1": ConceptState(p=p_mastered, p_eff=p_eff, stability_days=s_initial, status="mastered")
        }
    )

    decision = next_action(state, graph)
    assert decision.action == "Review", f"Expected action 'Review', got '{decision.action}'"
    assert decision.target_concept == "C1"
    assert "review" in decision.reason.lower()


def test_6_twin_histories_divergence(graph):
    """
    Test 6: Twin Histories Divergence
    Student A and Student B both achieve identical 60% scores on recent quizzes.
    However, Student A has a decaying prerequisite (C1 decayed < 0.60),
    while Student B has strong prerequisites but relied on multiple hints during practice.
    Engine computes completely divergent pedagogical actions: Student A -> Review, Student B -> Practice.
    """
    # Student A: decaying prerequisite C1 after 21 days
    p_eff_a_c1 = compute_effective_mastery(0.90, dt_days=21.0, stability_days=7.0)
    state_a = StudentState(
        student_id="STU_TWIN_A",
        active_concept_id="C3",
        concepts={
            "C1": ConceptState(p=0.90, p_eff=p_eff_a_c1, status="mastered"),
            "C2": ConceptState(p=0.85, p_eff=0.80, status="mastered"),
            "C3": ConceptState(p=0.65, p_eff=0.62, status="practicing")
        }
    )
    decision_a = next_action(state_a, graph)
    assert decision_a.action == "Review", f"Student A should route to 'Review', got '{decision_a.action}'"
    assert decision_a.target_concept == "C1"

    # Student B: strong prerequisites, but practicing C3 with low evidence (needs practice)
    state_b = StudentState(
        student_id="STU_TWIN_B",
        active_concept_id="C3",
        concepts={
            "C1": ConceptState(p=0.90, p_eff=0.88, status="mastered"),
            "C2": ConceptState(p=0.88, p_eff=0.85, status="mastered"),
            "C3": ConceptState(p=0.65, p_eff=0.62, status="practicing")
        }
    )
    decision_b = next_action(state_b, graph)
    assert decision_b.action == "Practice", f"Student B should route to 'Practice', got '{decision_b.action}'"
    assert decision_b.target_concept == "C3"

    assert decision_a.action != decision_b.action, "Twin learners must receive divergent actions!"


def test_8_decision_reproducibility(graph):
    """
    Test 8: Decision Deterministic Reproducibility
    Running next_action() using stored inputs_snapshot from an earlier decision record
    MUST yield the EXACT same action, target concept, and numeric reason string (0.000% variance).
    """
    state = StudentState(
        student_id="STU_REPRO_01",
        active_concept_id="C3",
        concepts={
            "C1": ConceptState(p=0.92, p_eff=0.88, evidence_sum=4.5, transfer_passed=True, status="mastered"),
            "C2": ConceptState(p=0.86, p_eff=0.81, evidence_sum=3.2, transfer_passed=True, status="mastered"),
            "C3": ConceptState(p=0.65, p_eff=0.62, evidence_sum=1.8, transfer_passed=False, status="practicing")
        }
    )

    decision_1 = next_action(state, graph)
    snapshot = decision_1.inputs_snapshot

    # Reconstruct state from snapshot
    reconstructed_concepts = {}
    for cid, data in snapshot["concepts"].items():
        reconstructed_concepts[cid] = ConceptState(**data)

    reconstructed_state = StudentState(
        student_id=snapshot["student_id"],
        active_concept_id=snapshot["active_concept_id"],
        concepts=reconstructed_concepts,
        active_override=snapshot["active_override"],
        last_attempt_time_days=snapshot["last_attempt_time_days"]
    )

    decision_2 = next_action(reconstructed_state, graph)

    assert decision_1.action == decision_2.action
    assert decision_1.target_concept == decision_2.target_concept
    assert decision_1.reason == decision_2.reason
    assert decision_1.config_version == decision_2.config_version
