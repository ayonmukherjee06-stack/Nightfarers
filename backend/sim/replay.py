"""MasteryFlow Simulation Replay Runner.

Authored by: Ayon Mukherjee (Team Lead & Orchestrator)
Role: Replays the 4 distinct cognitive personas through the deterministic decision engine,
demonstrating gap remediation, Ebbinghaus review recovery, stagnation escalation, and DAG advancement.
"""

from __future__ import annotations
import json
import os
from typing import Dict, List, Any, Optional
import copy

try:
    from backend.engine.contracts import (
        CurriculumGraph,
        EngineConfig,
        ConceptMastery,
        ActionType,
        CANONICAL_CONCEPTS,
    )
    from backend.engine.decide import make_decision
except ImportError:
    from masteryflow.engine.contracts import (
        CurriculumGraph,
        EngineConfig,
        ConceptMastery,
        ActionType,
        CANONICAL_CONCEPTS,
    )
    from masteryflow.engine.decide import make_decision


DEFAULT_PERSONAS_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "data", "personas.json"
)


def load_personas(json_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """Loads scripted learner profiles from JSON file."""
    path = json_path or DEFAULT_PERSONAS_PATH
    if not os.path.exists(path):
        alt_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "personas.json")
        if os.path.exists(alt_path):
            path = alt_path
        else:
            raise FileNotFoundError(f"Personas file not found at: {path}")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    all_p = data.get("personas", [])
    sim_ids = {"STU_DIYA", "STU_ROHAN", "STU_AARAV", "STU_PRIYA"}
    canonical = [p for p in all_p if p.get("id") in sim_ids]
    if len(canonical) == 4:
        return canonical
    return all_p


def build_mastery_map_from_persona(persona: Dict[str, Any]) -> Dict[str, ConceptMastery]:
    """Constructs a complete mastery map for all 10 canonical concepts from persona definition."""
    mastery_map = {
        cid: ConceptMastery(concept_id=cid, p_raw=0.10, p_eff=0.10)
        for cid in CANONICAL_CONCEPTS
    }
    for cid, state in persona.get("initial_mastery", {}).items():
        if cid in mastery_map:
            m = mastery_map[cid]
            m.p_raw = state.get("p_raw", state.get("p_eff", 0.10))
            m.p_eff = state.get("p_eff", 0.10)
            m.was_mastered = state.get("was_mastered", False)
            m.is_fragile = state.get("is_fragile", False)
            m.transfer_verified = state.get("transfer_verified", False)
            m.attempts_count = state.get("attempts_count", 0)
            m.errors_count = state.get("errors_count", 0)
            m.hints_count = state.get("hints_count", 0)
            m.history_p = list(state.get("history_p", []))
    return mastery_map


def replay_persona(
    persona: Dict[str, Any],
    graph: Optional[CurriculumGraph] = None,
    config: Optional[EngineConfig] = None,
) -> Dict[str, Any]:
    """Executes a multi-step pedagogical simulation for a given persona."""
    if graph is None:
        graph = CurriculumGraph(CANONICAL_CONCEPTS)
    if config is None:
        config = EngineConfig()

    mastery_map = build_mastery_map_from_persona(persona)
    current_cid = persona["initial_concept"]

    # Step 1: Initial Recommendation
    decision_step1 = make_decision(
        student_id=persona["id"],
        current_concept_id=current_cid,
        mastery_map=mastery_map,
        graph=graph,
        config=config,
    )

    steps = [
        {
            "step": 1,
            "description": "Initial Evaluation",
            "active_concept": current_cid,
            "action": decision_step1.action.value,
            "target_concept": decision_step1.target_concept_id,
            "rule": decision_step1.rule_triggered,
            "reason": decision_step1.reason,
        }
    ]

    # Step 2: Adaptive Resolution Step
    # Simulate learner responding to the engine's recommendation
    mastery_after = copy.deepcopy(mastery_map)

    if decision_step1.action == ActionType.REMEDIATE_PREREQUISITE:
        # Student remediates the weak prerequisite and masters it
        target = decision_step1.target_concept_id
        mastery_after[target].p_eff = 0.88
        mastery_after[target].was_mastered = True
        mastery_after[target].transfer_verified = True
        # Re-evaluate from original concept
        decision_step2 = make_decision(
            student_id=persona["id"],
            current_concept_id=current_cid,
            mastery_map=mastery_after,
            graph=graph,
            config=config,
        )
        steps.append({
            "step": 2,
            "description": f"Post-Remediation on {target} (Healed to 88%)",
            "active_concept": current_cid,
            "action": decision_step2.action.value,
            "target_concept": decision_step2.target_concept_id,
            "rule": decision_step2.rule_triggered,
            "reason": decision_step2.reason,
        })

    elif decision_step1.action == ActionType.REVIEW:
        # Student reviews decayed concept and restores retention
        target = decision_step1.target_concept_id
        mastery_after[target].p_eff = 0.92
        # Now continue on current concept
        decision_step2 = make_decision(
            student_id=persona["id"],
            current_concept_id=current_cid,
            mastery_map=mastery_after,
            graph=graph,
            config=config,
        )
        steps.append({
            "step": 2,
            "description": f"Post-Review Recovery on {target} (Restored to 92%)",
            "active_concept": current_cid,
            "action": decision_step2.action.value,
            "target_concept": decision_step2.target_concept_id,
            "rule": decision_step2.rule_triggered,
            "reason": decision_step2.reason,
        })

    elif decision_step1.action == ActionType.ADVANCE:
        # Move forward into newly unlocked node
        next_cid = decision_step1.target_concept_id
        decision_step2 = make_decision(
            student_id=persona["id"],
            current_concept_id=next_cid,
            mastery_map=mastery_after,
            graph=graph,
            config=config,
        )
        steps.append({
            "step": 2,
            "description": f"Advanced into Unlocked Node {next_cid}",
            "active_concept": next_cid,
            "action": decision_step2.action.value,
            "target_concept": decision_step2.target_concept_id,
            "rule": decision_step2.rule_triggered,
            "reason": decision_step2.reason,
        })

    return {
        "persona_id": persona["id"],
        "name": persona["name"],
        "archetype": persona["archetype"],
        "expected_initial_action": persona.get("expected_initial_action"),
        "expected_target_concept": persona.get("expected_target_concept"),
        "steps": steps,
        "is_verified": (
            decision_step1.action.value == persona.get("expected_initial_action")
            and decision_step1.target_concept_id == persona.get("expected_target_concept")
        ),
    }


def run_all_replays(json_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """Runs simulation replay for all 4 profiles and prints formatted traces."""
    personas = load_personas(json_path)
    results = []
    print("=" * 80)
    print(" MASTERYFLOW MULTI-PERSONA COGNITIVE SIMULATION REPLAY")
    print(" Authored by: Ayon Mukherjee (Team Lead & Orchestrator)")
    print("=" * 80)

    for p in personas:
        res = replay_persona(p)
        results.append(res)
        status = "PASSED (100% VERIFIED)" if res["is_verified"] else "FAILED"
        print(f"\n[{res['persona_id']}] {res['name']} — {res['archetype']} => {status}")
        for s in res["steps"]:
            print(f"  Step {s['step']}: {s['description']}")
            print(f"    Action: {s['action']} -> Target: {s['target_concept']}")
            print(f"    Rule:   {s['rule']}")
            print(f"    Reason: {s['reason'][:90]}...")

    print("\n" + "=" * 80)
    return results


if __name__ == "__main__":
    run_all_replays()
