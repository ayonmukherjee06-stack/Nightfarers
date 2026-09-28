"""MasteryFlow Phase 1 CLI Replay Verification.

Authored by: Ayon Mukherjee (Team Lead & Orchestrator)
Role: Demonstrates deterministic decision engine outputs across real educational scenarios
with zero network calls, zero hardcoding, and complete Glass-Box transparency.
"""

from __future__ import annotations
import copy
try:
    from backend.engine.contracts import (
        CurriculumGraph,
        EngineConfig,
        ConceptMastery,
        CANONICAL_CONCEPTS,
    )
    from backend.engine.decide import (
        make_decision,
        reconstruct_decision_from_snapshot,
    )
except ImportError:
    from masteryflow.engine.contracts import (
        CurriculumGraph,
        EngineConfig,
        ConceptMastery,
        CANONICAL_CONCEPTS,
    )
    from masteryflow.engine.decide import (
        make_decision,
        reconstruct_decision_from_snapshot,
    )


def run_phase1_cli_replay() -> None:
    print("=" * 80)
    print(" MASTERYFLOW DETERMINISTIC DECISION ENGINE (PHASE 1 CLI REPLAY)")
    print(" Authored by: Ayon Mukherjee (Team Lead & Orchestrator)")
    print("=" * 80)

    graph = CurriculumGraph(CANONICAL_CONCEPTS)
    config = EngineConfig()

    def get_base_mastery():
        return {
            cid: ConceptMastery(concept_id=cid, p_raw=0.10, p_eff=0.10)
            for cid in CANONICAL_CONCEPTS
        }

    # Scenario 1: Foundational Prerequisite Gap (Rule 2)
    print("\n--- SCENARIO 1: FOUNDATIONAL PREREQUISITE REMEDIATION (RULE 2) ---")
    m1 = get_base_mastery()
    m1["C1"].p_eff = 0.85
    m1["C1"].was_mastered = True
    m1["C2"].p_eff = 0.42  # Unmastered weak prereq
    m1["C2"].was_mastered = False
    m1["C5"].p_eff = 0.65
    m1["C6"].p_eff = 0.60
    m1["C7"].p_eff = 0.48
    m1["C7"].history_p = [0.35, 0.42, 0.48]
    m1["C7"].errors_count = 2
    m1["C7"].hints_count = 2

    d1 = make_decision("STU_DIYA", "C7", m1, graph, config)
    print(f"Student: STU_DIYA | Current Concept: C7 (p_eff = {m1['C7'].p_eff:.1%})")
    print(f"Triggered Rule: {d1.rule_triggered}")
    print(f"Engine Decision: ACTION = {d1.action.value} -> TARGET = {d1.target_concept_id}")
    print(f"Glass-Box Reason:\n  \"{d1.reason}\"")

    # Scenario 2: Memory Retention Decay (Rule 3)
    print("\n--- SCENARIO 2: EBBINGHAUS RETENTION DECAY (RULE 3) ---")
    m2 = get_base_mastery()
    m2["C1"].was_mastered = True
    m2["C1"].p_eff = 0.48  # Decayed over time below 0.60
    m2["C2"].was_mastered = True
    m2["C2"].p_eff = 0.80
    m2["C3"].p_eff = 0.70
    m2["C3"].history_p = [0.55, 0.62, 0.70]

    d2 = make_decision("STU_ROHAN", "C3", m2, graph, config)
    print(f"Student: STU_ROHAN | Current Concept: C3 (p_eff = {m2['C3'].p_eff:.1%})")
    print(f"Triggered Rule: {d2.rule_triggered}")
    print(f"Engine Decision: ACTION = {d2.action.value} -> TARGET = {d2.target_concept_id}")
    print(f"Glass-Box Reason:\n  \"{d2.reason}\"")

    # Scenario 3: Cognitive Plateau Stagnation (Rule 1)
    print("\n--- SCENARIO 3: COGNITIVE PLATEAU STAGNATION (RULE 1) ---")
    m3 = get_base_mastery()
    m3["C2"].p_eff = 0.42
    m3["C2"].history_p = [0.39, 0.40, 0.41, 0.42]  # Gain is 0.03 (< 0.05) over 3 cycles

    d3 = make_decision("STU_AARAV", "C2", m3, graph, config)
    print(f"Student: STU_AARAV | Current Concept: C2 (p_eff = {m3['C2'].p_eff:.1%})")
    print(f"Triggered Rule: {d3.rule_triggered}")
    print(f"Engine Decision: ACTION = {d3.action.value} -> TARGET = {d3.target_concept_id}")
    print(f"Glass-Box Reason:\n  \"{d3.reason}\"")

    # Scenario 4: Mastery & Unlocked Advancement (Rule 5)
    print("\n--- SCENARIO 4: VERIFIED MASTERY & ADVANCE (RULE 5) ---")
    m4 = get_base_mastery()
    m4["C1"].p_eff = 0.92
    m4["C1"].was_mastered = True
    m4["C1"].transfer_verified = True
    m4["C1"].history_p = [0.70, 0.82, 0.92]

    d4 = make_decision("STU_PRIYA", "C1", m4, graph, config)
    print(f"Student: STU_PRIYA | Current Concept: C1 (p_eff = {m4['C1'].p_eff:.1%})")
    print(f"Triggered Rule: {d4.rule_triggered}")
    print(f"Engine Decision: ACTION = {d4.action.value} -> TARGET = {d4.target_concept_id}")
    print(f"Glass-Box Reason:\n  \"{d4.reason}\"")

    # Scenario 5: Reproducibility Check (Test 8 Proof)
    print("\n--- SCENARIO 5: TEST 8 REPRODUCIBILITY RECONSTRUCTION ---")
    snapshot = d1.inputs_snapshot
    reconstructed = reconstruct_decision_from_snapshot(snapshot, graph)
    matches = (
        reconstructed.action == d1.action
        and reconstructed.target_concept_id == d1.target_concept_id
        and reconstructed.reason == d1.reason
    )
    print(f"Reconstructed Decision: ACTION = {reconstructed.action.value} -> TARGET = {reconstructed.target_concept_id}")
    print(f"Deterministic Match with Original Decision: {'PASS (100% IDENTICAL)' if matches else 'FAIL'}")
    print("=" * 80)


if __name__ == "__main__":
    run_phase1_cli_replay()
