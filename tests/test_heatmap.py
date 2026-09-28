"""Test Suite for Teacher Cohort Heatmap & Bottleneck Detection.

Authored by: Ayon Mukherjee (Team Lead & Orchestrator)
Tests cohort matrix generation, group-level bottleneck identification,
and stuck-learner queue detection according to pedagogical specifications.
"""

import pytest
try:
    from backend.engine.contracts import (
        CurriculumGraph,
        ConceptMastery,
        CANONICAL_CONCEPTS,
    )
    from frontend.components.heatmap import (
        compute_cohort_metrics,
        detect_group_bottlenecks,
        get_stuck_learners,
    )
except ImportError:
    from masteryflow.engine.contracts import (
        CurriculumGraph,
        ConceptMastery,
        CANONICAL_CONCEPTS,
    )
    from masteryflow.ui.components.heatmap import (
        compute_cohort_metrics,
        detect_group_bottlenecks,
        get_stuck_learners,
    )


@pytest.fixture
def graph():
    return CurriculumGraph(CANONICAL_CONCEPTS)


@pytest.fixture
def sample_cohort():
    """Generates a sample cohort of 6 students with varied cognitive profiles."""
    cohort = {}

    # Student 1: Advanced (mastered C1, C2, C3, C4)
    cohort["STU_001"] = {
        "name": "Priya Singh",
        "mastery": {
            cid: ConceptMastery(concept_id=cid, p_raw=0.90, p_eff=0.90, was_mastered=True, transfer_verified=True)
            for cid in ["C1", "C2", "C3", "C4"]
        },
    }
    # Add remaining concepts baseline for STU_001
    for cid in ["C5", "C6", "C7", "C8", "C9", "C10"]:
        cohort["STU_001"]["mastery"][cid] = ConceptMastery(concept_id=cid, p_raw=0.20, p_eff=0.20)

    # Student 2: Struggling on C2 (Equivalent fractions)
    cohort["STU_002"] = {
        "name": "Aarav Patel",
        "mastery": {
            cid: ConceptMastery(concept_id=cid, p_raw=0.10, p_eff=0.10)
            for cid in CANONICAL_CONCEPTS
        },
    }
    cohort["STU_002"]["mastery"]["C1"].p_eff = 0.85
    cohort["STU_002"]["mastery"]["C1"].was_mastered = True
    cohort["STU_002"]["mastery"]["C2"].p_eff = 0.40  # Gap
    cohort["STU_002"]["mastery"]["C2"].history_p = [0.38, 0.39, 0.39, 0.40]  # Stagnant across 3 cycles: gain is 0.02 (< 0.05)

    # Student 3: Also struggling on C2
    cohort["STU_003"] = {
        "name": "Diya Sharma",
        "mastery": {
            cid: ConceptMastery(concept_id=cid, p_raw=0.10, p_eff=0.10)
            for cid in CANONICAL_CONCEPTS
        },
    }
    cohort["STU_003"]["mastery"]["C1"].p_eff = 0.88
    cohort["STU_003"]["mastery"]["C1"].was_mastered = True
    cohort["STU_003"]["mastery"]["C2"].p_eff = 0.42  # Gap
    cohort["STU_003"]["mastery"]["C7"].p_eff = 0.48

    # Student 4: Also struggling on C2
    cohort["STU_004"] = {
        "name": "Kabir Khan",
        "mastery": {
            cid: ConceptMastery(concept_id=cid, p_raw=0.10, p_eff=0.10)
            for cid in CANONICAL_CONCEPTS
        },
    }
    cohort["STU_004"]["mastery"]["C1"].p_eff = 0.80
    cohort["STU_004"]["mastery"]["C2"].p_eff = 0.38  # Gap

    # Student 5: Decayed on C1
    cohort["STU_005"] = {
        "name": "Rohan Verma",
        "mastery": {
            cid: ConceptMastery(concept_id=cid, p_raw=0.10, p_eff=0.10)
            for cid in CANONICAL_CONCEPTS
        },
    }
    cohort["STU_005"]["mastery"]["C1"].p_eff = 0.48
    cohort["STU_005"]["mastery"]["C1"].was_mastered = True  # Decayed
    cohort["STU_005"]["mastery"]["C2"].p_eff = 0.82

    # Student 6: On track
    cohort["STU_006"] = {
        "name": "Ananya Sen",
        "mastery": {
            cid: ConceptMastery(concept_id=cid, p_raw=0.10, p_eff=0.10)
            for cid in CANONICAL_CONCEPTS
        },
    }
    cohort["STU_006"]["mastery"]["C1"].p_eff = 0.90
    cohort["STU_006"]["mastery"]["C2"].p_eff = 0.85
    cohort["STU_006"]["mastery"]["C2"].was_mastered = True

    return cohort


def test_cohort_metrics_computation(sample_cohort):
    """Verifies calculation of mean mastery and status counts per concept."""
    metrics = compute_cohort_metrics(sample_cohort)
    
    assert "C1" in metrics
    assert "C2" in metrics
    assert 0.0 <= metrics["C1"]["mean_p"] <= 1.0
    assert metrics["C1"]["mastered_count"] >= 3


def test_group_bottleneck_detection(sample_cohort, graph):
    """Verifies that C2 is correctly flagged as a cohort bottleneck since 3 of 6 students have p < 0.55."""
    bottlenecks = detect_group_bottlenecks(sample_cohort, graph, gap_threshold=0.55, cohort_pct_threshold=0.30)
    
    # 3 out of 6 students (50%) have C2 < 0.55
    assert len(bottlenecks) >= 1
    c2_bottleneck = next((b for b in bottlenecks if b["concept_id"] == "C2"), None)
    assert c2_bottleneck is not None
    assert c2_bottleneck["struggling_count"] == 3
    assert c2_bottleneck["struggling_pct"] == 50.0
    assert "downstream_affected" in c2_bottleneck
    # Downstream of C2 includes C3, C4, C5, etc.
    assert len(c2_bottleneck["downstream_affected"]) > 0


def test_stuck_learners_queue(sample_cohort):
    """Verifies that Aarav Patel (STU_002) is flagged in the stuck-learner queue due to stagnation."""
    stuck_list = get_stuck_learners(sample_cohort)
    
    assert len(stuck_list) >= 1
    aarav_entry = next((s for s in stuck_list if s["student_id"] == "STU_002"), None)
    assert aarav_entry is not None
    assert aarav_entry["concept_id"] == "C2"
    assert aarav_entry["delta_p"] < 0.05
