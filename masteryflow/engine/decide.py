"""MasteryFlow Pedagogical Decision Engine & 6 Ordered Decision Rules (decide.py).

Unified Engine authored jointly by: Ayon Mukherjee (Lead & Orchestrator) & Yash (ML Lead)
Integrated with Soham Choudhury (Student Portal) & Shreyash Jha (Backend REST API)

JUDGING INVARIANT:
- Pure algorithmic Python (Zero LLM calls, zero network I/O, zero random seed drift).
- Evaluates 6 ordered rules deterministically.
- Full support for both next_action() (BKT student runner) and make_decision() (teacher command deck & test suite).
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Tuple
import math
import copy

try:
    from .contracts import (
        ActionType,
        ConceptMastery,
        CurriculumGraph,
        EngineConfig,
        CANONICAL_CONCEPTS,
    )
except ImportError:
    from backend.engine.contracts import (
        ActionType,
        ConceptMastery,
        CurriculumGraph,
        EngineConfig,
        CANONICAL_CONCEPTS,
    )


@dataclass
class ConceptState:
    p: float = 0.30
    p_eff: float = 0.30
    stability_days: float = 7.0
    evidence_sum: float = 0.0
    transfer_passed: bool = False
    is_fragile: bool = False
    status: str = "unseen"  # unseen, practicing, provisional, mastered
    consecutive_stagnant_cycles: int = 0
    recent_errors: int = 0
    recent_hints: int = 0


@dataclass
class StudentState:
    student_id: str
    active_concept_id: str
    concepts: Dict[str, ConceptState] = field(default_factory=dict)
    active_override: Optional[Dict[str, Any]] = None
    last_attempt_time_days: float = 0.0
    challenge_mode: bool = False


@dataclass
class Decision:
    action: Any  # str or ActionType
    target_concept: str = ""
    reason: str = ""
    rule_triggered: str = ""
    config_version: int = 1
    inputs_snapshot: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    target_concept_id: str = ""
    target_concept_name: str = ""
    rule_number: int = 4
    rule_name: str = ""
    p_eff: float = 0.50
    evidence_sum: float = 0.0
    status: str = "practicing"
    is_fragile: bool = False
    inputs_json: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.target_concept_id and self.target_concept:
            self.target_concept_id = self.target_concept
        if not self.target_concept and self.target_concept_id:
            self.target_concept = self.target_concept_id
        if not self.target_concept_name:
            self.target_concept_name = self.target_concept
        if not self.rule_name and self.rule_triggered:
            self.rule_name = self.rule_triggered
        if not self.rule_triggered and self.rule_name:
            self.rule_triggered = self.rule_name
        if not self.rule_triggered:
            act_str = self.action.value if hasattr(self.action, "value") else str(self.action)
            self.rule_triggered = f"Rule: {act_str}"
        if not self.inputs_json and self.inputs_snapshot:
            self.inputs_json = self.inputs_snapshot
        if not self.inputs_snapshot and self.inputs_json:
            self.inputs_snapshot = self.inputs_json

    def to_dict(self) -> Dict[str, Any]:
        act_str = self.action.value if hasattr(self.action, "value") else str(self.action)
        return {
            "action": act_str,
            "target_concept": self.target_concept,
            "target_concept_id": self.target_concept_id,
            "target_concept_name": self.target_concept_name,
            "reason": self.reason,
            "rule_number": self.rule_number,
            "rule_name": self.rule_name,
            "rule_triggered": self.rule_triggered,
            "p_eff": self.p_eff,
            "evidence_sum": self.evidence_sum,
            "status": self.status,
            "is_fragile": self.is_fragile,
            "config_version": self.config_version,
            "inputs_snapshot": self.inputs_snapshot,
            "inputs_json": self.inputs_json,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Decision:
        act_raw = data.get("action", "Practice")
        try:
            act = ActionType(act_raw)
        except ValueError:
            act = act_raw
        return cls(
            action=act,
            target_concept=data.get("target_concept", data.get("target_concept_id", "")),
            target_concept_id=data.get("target_concept_id", data.get("target_concept", "")),
            target_concept_name=data.get("target_concept_name", ""),
            reason=data.get("reason", ""),
            rule_number=data.get("rule_number", 4),
            rule_name=data.get("rule_name", ""),
            rule_triggered=data.get("rule_triggered", ""),
            p_eff=data.get("p_eff", 0.50),
            evidence_sum=data.get("evidence_sum", 0.0),
            status=data.get("status", "practicing"),
            is_fragile=data.get("is_fragile", False),
            config_version=data.get("config_version", 1),
            inputs_snapshot=data.get("inputs_snapshot", data.get("inputs_json", {})),
            inputs_json=data.get("inputs_json", data.get("inputs_snapshot", {})),
            metadata=data.get("metadata", {}),
        )



# ==============================================================================
# SOHAM & YASH COMPATIBILITY: next_action()
# ==============================================================================

def next_action(
    state_or_student_id: Optional[Union[StudentState, str]] = None,
    graph: Optional[Any] = None,
    config: Optional[Dict[str, Any]] = None,
    student_id: Optional[str] = None
) -> Decision:
    """Computes deterministic pedagogical next action across the 6 ordered rules for student portal.
    Supports both next_action(student_state, graph) and next_action(student_id='STU_001').
    """
    target_id = student_id or (state_or_student_id if isinstance(state_or_student_id, str) else None)
    if target_id is not None:
        from .service import default_service
        return default_service.next_action(target_id)

    state = state_or_student_id
    cfg = config or {}
    thresholds = cfg.get("thresholds", {})
    mastery_th = thresholds.get("mastery", 0.85)
    review_th = thresholds.get("review", 0.60)
    prereq_th = thresholds.get("prerequisite", 0.55)
    capping_offset = thresholds.get("capping_offset", 0.25)
    config_version = cfg.get("config_version", 1)

    snapshot = {
        "student_id": state.student_id,
        "active_concept_id": state.active_concept_id,
        "concepts": {cid: asdict(cs) for cid, cs in state.concepts.items()},
        "active_override": state.active_override,

        "last_attempt_time_days": state.last_attempt_time_days,
        "challenge_mode": state.challenge_mode,
        "config_version": config_version,
    }

    # RULE 1: Teacher Intervention & Persistent Overrides
    if state.active_override:
        ov = state.active_override
        target = ov.get("target_concept", state.active_concept_id)
        action_name = ov.get("action", "Remediate")
        note = ov.get("reason", "Instructor intervention override active.")
        cname = graph.concepts_meta.get(target, {}).get("name", target) if hasattr(graph, "concepts_meta") else target
        reason = f"{action_name} {target} ({cname}): Instructor override active - '{note}'"
        return Decision(
            action=action_name,
            target_concept=target,
            reason=reason,
            rule_triggered="Rule 0: Persistent Teacher Override (Human Authority)",
            config_version=config_version,
            inputs_snapshot=snapshot,
        )

    active_cid = state.active_concept_id
    active_meta = graph.concepts_meta.get(active_cid, {}) if hasattr(graph, "concepts_meta") else {}
    active_name = active_meta.get("name", active_cid)
    active_cstate = state.concepts.get(active_cid, ConceptState())

    # Stuck learner escalation: Delta p < 0.05 across 3 consecutive cycles
    if active_cstate.consecutive_stagnant_cycles >= 3:
        reason = (
            f"Escalate to Teacher for {active_cid} ({active_name}): Student made <0.05 p gain across 3 "
            f"consecutive cycles with {active_cstate.recent_errors} errors and {active_cstate.recent_hints} hints. "
            f"Requires 1-on-1 human coaching."
        )
        return Decision(
            action="Escalate to Teacher",
            target_concept=active_cid,
            reason=reason,
            rule_triggered="Rule 1: Teacher Intervention (Stagnation)",
            config_version=config_version,
            inputs_snapshot=snapshot,
        )

    # RULE 2: Remediate Prerequisite
    prereqs = graph.get_prerequisites(active_cid) if hasattr(graph, "get_prerequisites") else []
    all_p_eff = {cid: cs.p_eff for cid, cs in state.concepts.items()}

    if hasattr(graph, "apply_prerequisite_capping"):
        capped_p, is_fragile, weakest_prereq, weakest_val = graph.apply_prerequisite_capping(
            active_cid, active_cstate.p_eff, all_p_eff, capping_offset=capping_offset
        )
        if is_fragile and weakest_prereq:
            weakest_meta = graph.concepts_meta.get(weakest_prereq, {}) if hasattr(graph, "concepts_meta") else {}
            weakest_name = weakest_meta.get("name", weakest_prereq)
            weakest_pct = int(round((weakest_val or 0.0) * 100))
            active_pct = int(round(active_cstate.p_eff * 100))
            cap_pct = int(round(capped_p * 100))
            reason = (
                f"Remediate {weakest_prereq} ({weakest_name}): prerequisite for {active_cid} ({active_name}) "
                f"has decayed to {weakest_pct}%, capping {active_cid} at {cap_pct}% (tagged fragile). "
                f"Prerequisite threshold is {int(prereq_th * 100)}%."
            )
            return Decision(
                action="Remediate",
                target_concept=weakest_prereq,
                reason=reason,
                rule_triggered="Rule 2: Remediate Prerequisite (Foundational Gap)",
                config_version=config_version,
                inputs_snapshot=snapshot,
            )

    for pr in prereqs:
        pr_val = all_p_eff.get(pr, 0.25)
        if pr_val < prereq_th:
            pr_meta = graph.concepts_meta.get(pr, {}) if hasattr(graph, "concepts_meta") else {}
            pr_name = pr_meta.get("name", pr)
            reason = (
                f"Remediate {pr} ({pr_name}): prerequisite for {active_cid} has decayed to "
                f"{int(round(pr_val * 100))}%, below prerequisite threshold {int(prereq_th * 100)}%."
            )
            return Decision(
                action="Remediate",
                target_concept=pr,
                reason=reason,
                rule_triggered="Rule 2: Remediate Prerequisite (Foundational Gap)",
                config_version=config_version,
                inputs_snapshot=snapshot,
            )

    # RULE 3: Longitudinal Spaced Review
    candidates_for_review = []
    for cid, cstate in state.concepts.items():
        if cstate.status == "mastered" and cstate.p_eff < review_th:
            candidates_for_review.append((cid, cstate))

    if candidates_for_review:
        candidates_for_review.sort(key=lambda item: item[1].p_eff)
        rev_cid, rev_state = candidates_for_review[0]
        rev_meta = graph.concepts_meta.get(rev_cid, {}) if hasattr(graph, "concepts_meta") else {}
        rev_name = rev_meta.get("name", rev_cid)
        rev_pct = int(round(rev_state.p_eff * 100))
        rev_th_pct = int(round(review_th * 100))
        reason = (
            f"Review {rev_cid} ({rev_name}): p_eff decayed to {rev_pct}% "
            f"after elapsed inactivity (review threshold {rev_th_pct}%)."
        )
        return Decision(
            action="Review",
            target_concept=rev_cid,
            reason=reason,
            rule_triggered="Rule 3: Spaced Review (Retention Decay)",
            config_version=config_version,
            inputs_snapshot=snapshot,
        )

    # RULE 4: Practice (Current Concept)
    active_pct = int(round(active_cstate.p_eff * 100))
    if active_cstate.p_eff < mastery_th:
        reason = (
            f"Practice {active_cid} ({active_name}): p_eff {active_pct}%, "
            f"needs 1 transfer answer with w >= 0.5."
        )
        return Decision(
            action="Practice",
            target_concept=active_cid,
            reason=reason,
            rule_triggered="Rule 4: Practice (ZPD Consolidation)",
            config_version=config_version,
            inputs_snapshot=snapshot,
        )

    if not active_cstate.transfer_passed or active_cstate.evidence_sum < 3.0:
        reason = (
            f"Practice {active_cid} ({active_name}): p_eff {active_pct}% is high, "
            f"but remains provisional until at least 1 transfer item is passed with w >= 0.5."
        )
        return Decision(
            action="Practice",
            target_concept=active_cid,
            reason=reason,
            rule_triggered="Rule 4: Practice (Transfer Problem Verification)",
            config_version=config_version,
            inputs_snapshot=snapshot,
        )

    # RULE 5: Advance to Next Unlocked Concept
    topo = graph.topological_order() if hasattr(graph, "topological_order") else list(state.concepts.keys())
    for cid in topo:
        if cid == active_cid:
            continue
        cstate = state.concepts.get(cid, ConceptState())
        if cstate.status != "mastered":
            candidate_prereqs = graph.get_prerequisites(cid) if hasattr(graph, "get_prerequisites") else []
            prereqs_met = all(all_p_eff.get(pr, 0.0) >= prereq_th for pr in candidate_prereqs)
            if prereqs_met:
                c_meta = graph.concepts_meta.get(cid, {}) if hasattr(graph, "concepts_meta") else {}
                c_name = c_meta.get("name", cid)
                reason = (
                    f"Advance to {cid} ({c_name}): {active_cid} mastered at {active_pct}% "
                    f"with transfer requirement verified; all prerequisites for {cid} satisfied."
                )
                return Decision(
                    action="Advance",
                    target_concept=cid,
                    reason=reason,
                    rule_triggered="Rule 5: Advance (Next Unlocked Concept)",
                    config_version=config_version,
                    inputs_snapshot=snapshot,
                )

    # RULE 6: Challenge / Consolidate
    last_cid = topo[-1] if topo else active_cid
    last_meta = graph.concepts_meta.get(last_cid, {}) if hasattr(graph, "concepts_meta") else {}
    last_name = last_meta.get("name", last_cid)
    reason = (
        f"Challenge {last_cid} ({last_name}): entire curriculum mastered; "
        f"offering high-difficulty synthesis transfer challenge problem."
    )
    return Decision(
        action="Challenge",
        target_concept=last_cid,
        reason=reason,
        rule_triggered="Rule 6: Challenge (Capstone & Acceleration)",
        config_version=config_version,
        inputs_snapshot=snapshot,
    )


# ==============================================================================
# AYON'S DETERMINISTIC ENGINE FUNCTIONS: make_decision()
# ==============================================================================

def check_stagnation(
    history_p: List[float],
    cycles: int = 3,
    delta_threshold: float = 0.05,
) -> Tuple[bool, float]:
    """Evaluates whether the learner is caught in an unproductive cognitive plateau."""
    if len(history_p) <= cycles:
        return False, 0.0

    p_now = history_p[-1]
    p_past = history_p[-(cycles + 1)]
    delta_p = p_now - p_past

    if delta_p < delta_threshold:
        return True, delta_p

    return False, delta_p


def find_weakest_prerequisite(
    concept_id: str,
    mastery_map: Dict[str, ConceptMastery],
    graph: CurriculumGraph,
    remediation_threshold: float = 0.55,
) -> Optional[Tuple[str, float]]:
    """Traverses all upstream ancestor concepts in the DAG to locate foundational gaps."""
    ancestors = graph.get_all_ancestors(concept_id) if hasattr(graph, "get_all_ancestors") else []
    if not ancestors:
        return None

    candidates: List[Tuple[str, float]] = []
    for anc_id in ancestors:
        m = mastery_map.get(anc_id)
        if m is not None:
            if (not m.was_mastered) and (m.p_eff < remediation_threshold):
                candidates.append((anc_id, m.p_eff))

    if not candidates:
        return None

    candidates.sort(key=lambda item: item[1])
    return candidates[0]


def find_most_decayed_review(
    mastery_map: Dict[str, ConceptMastery],
    graph: CurriculumGraph,
    review_threshold: float = 0.60,
) -> Optional[Tuple[str, float]]:
    """Identifies previously mastered concepts that have suffered Ebbinghaus memory decay."""
    candidates: List[Tuple[str, float]] = []
    for cid, m in mastery_map.items():
        if m.was_mastered and m.p_eff < review_threshold:
            candidates.append((cid, m.p_eff))

    if not candidates:
        return None

    candidates.sort(key=lambda item: item[1])
    return candidates[0]


def find_next_advance_target(
    current_concept_id: str,
    mastery_map: Dict[str, ConceptMastery],
    graph: CurriculumGraph,
    config: EngineConfig,
) -> Optional[str]:
    """Finds next eligible concept in topological order."""
    topo_order = graph.get_topological_order() if hasattr(graph, "get_topological_order") else list(mastery_map.keys())

    for cid in topo_order:
        m = mastery_map.get(cid)
        if m is None or (not m.was_mastered) or (m.p_eff < config.mastery_threshold):
            prereqs = graph.get_prerequisites(cid) if hasattr(graph, "get_prerequisites") else []
            all_prereqs_met = True
            for p in prereqs:
                p_m = mastery_map.get(p)
                if p_m is None or p_m.p_eff < config.prereq_remediation_threshold:
                    all_prereqs_met = False
                    break

            if all_prereqs_met and cid != current_concept_id:
                return cid

    return None


def serialize_inputs_snapshot(
    student_id: str,
    current_concept_id: str,
    mastery_map: Dict[str, ConceptMastery],
    config: EngineConfig,
    challenge_mode: bool = False,
    active_override: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Creates a deterministic, JSON-serializable snapshot of engine inputs for Test 8."""
    return {
        "student_id": student_id,
        "current_concept_id": current_concept_id,
        "challenge_mode": challenge_mode,
        "active_override": active_override,
        "config": config.to_dict(),
        "p_eff": {cid: round(m.p_eff, 4) for cid, m in mastery_map.items()},
        "mastery_state": {cid: m.to_dict() for cid, m in mastery_map.items()},
    }


def make_decision(
    student_id: str,
    current_concept_id: str,
    mastery_map: Dict[str, ConceptMastery],
    graph: CurriculumGraph,
    config: EngineConfig,
    challenge_mode: bool = False,
    active_override: Optional[Dict[str, Any]] = None,
) -> Decision:
    """Evaluates the 6 deterministic pedagogical rules in strict priority order for Teacher & Test Suites."""
    current_mastery = mastery_map.get(current_concept_id)
    if current_mastery is None:
        current_mastery = ConceptMastery(concept_id=current_concept_id)
        mastery_map[current_concept_id] = current_mastery

    inputs_snapshot = serialize_inputs_snapshot(
        student_id=student_id,
        current_concept_id=current_concept_id,
        mastery_map=mastery_map,
        config=config,
        challenge_mode=challenge_mode,
        active_override=active_override,
    )

    # RULE 0: Human-in-the-Loop Override
    if active_override is not None:
        action_raw = active_override.get("action", ActionType.REMEDIATE_PREREQUISITE)
        if isinstance(action_raw, str):
            try:
                act_enum = ActionType(action_raw)
            except ValueError:
                act_enum = action_raw
        else:
            act_enum = action_raw
        target_cid = active_override.get("target_concept_id", active_override.get("target_concept", current_concept_id))
        teacher_id = active_override.get("teacher_id", "TEACHER_1")
        custom_reason = active_override.get("reason", "Teacher applied direct pedagogical override.")

        title = graph.get_concept_title(target_cid) if hasattr(graph, "get_concept_title") else target_cid
        act_val = act_enum.value if hasattr(act_enum, "value") else str(act_enum)
        reason = (
            f"HUMAN TEACHER OVERRIDE ACTIVE (Authorized by {teacher_id}): "
            f"Direct override enforcing action {act_val} on {target_cid} "
            f"('{title}'). Rationale: {custom_reason}"
        )
        return Decision(
            action=act_enum,
            target_concept=target_cid,
            target_concept_id=target_cid,
            reason=reason,
            rule_triggered="Rule 0: Persistent Teacher Override (Human Authority)",
            inputs_snapshot=inputs_snapshot,
            metadata={"teacher_override": active_override},
        )

    # RULE 1: Teacher Intervention
    stagnant, delta_p = check_stagnation(
        history_p=current_mastery.history_p,
        cycles=config.stagnation_cycles,
        delta_threshold=config.stagnation_delta,
    )
    title_curr = graph.get_concept_title(current_concept_id) if hasattr(graph, "get_concept_title") else current_concept_id
    if stagnant:
        gain_pct = delta_p * 100.0
        reason = (
            f"Stagnation detected on Concept {current_concept_id} "
            f"('{title_curr}'): effective mastery increased by only "
            f"{gain_pct:.1f}% (< {config.stagnation_delta * 100:.1f}%) over the last "
            f"{config.stagnation_cycles} cycles. Automated remediation exhausted; "
            f"flagged for 1-on-1 human coaching."
        )
        return Decision(
            action=ActionType.TEACHER_INTERVENTION,
            target_concept=current_concept_id,
            target_concept_id=current_concept_id,
            reason=reason,
            rule_triggered="Rule 1: Teacher Intervention (Stagnation)",
            inputs_snapshot=inputs_snapshot,
            metadata={"delta_p": delta_p, "stagnation_detected": True},
        )

    # RULE 2: Remediate Prerequisite
    weakest_prereq = find_weakest_prerequisite(
        concept_id=current_concept_id,
        mastery_map=mastery_map,
        graph=graph,
        remediation_threshold=config.prereq_remediation_threshold,
    )
    if weakest_prereq is not None:
        prereq_id, prereq_p = weakest_prereq
        p_title = graph.get_concept_title(prereq_id) if hasattr(graph, "get_concept_title") else prereq_id
        reason = (
            f"You are practicing {current_concept_id} ('{title_curr}'), "
            f"but our structural knowledge map detected that your mastery of prerequisite {prereq_id} "
            f"('{p_title}') is currently {prereq_p * 100:.1f}% "
            f"(threshold: {config.prereq_remediation_threshold * 100:.1f}%). "
            f"In recent attempts on {current_concept_id}, you recorded {current_mastery.errors_count} errors "
            f"and used {current_mastery.hints_count} hints. Strengthening {prereq_id} first guarantees success!"
        )
        return Decision(
            action=ActionType.REMEDIATE_PREREQUISITE,
            target_concept=prereq_id,
            target_concept_id=prereq_id,
            reason=reason,
            rule_triggered="Rule 2: Remediate Prerequisite (Foundational Gap)",
            inputs_snapshot=inputs_snapshot,
            metadata={"weakest_prereq_id": prereq_id, "prereq_p_eff": prereq_p},
        )

    # RULE 3: Spaced Review
    most_decayed = find_most_decayed_review(
        mastery_map=mastery_map,
        graph=graph,
        review_threshold=config.review_threshold,
    )
    if most_decayed is not None:
        decay_cid, decay_p = most_decayed
        dec_title = graph.get_concept_title(decay_cid) if hasattr(graph, "get_concept_title") else decay_cid
        reason = (
            f"Previously mastered concept {decay_cid} ('{dec_title}') "
            f"has decayed over time to {decay_p * 100:.1f}% effective retention "
            f"(below review threshold of {config.review_threshold * 100:.1f}%). "
            f"Spaced retrieval review scheduled to arrest Ebbinghaus forgetting curve."
        )
        return Decision(
            action=ActionType.REVIEW,
            target_concept=decay_cid,
            target_concept_id=decay_cid,
            reason=reason,
            rule_triggered="Rule 3: Spaced Review (Retention Decay)",
            inputs_snapshot=inputs_snapshot,
            metadata={"decayed_concept_id": decay_cid, "decayed_p_eff": decay_p},
        )

    # RULE 4: Practice
    is_mastered_candidate = current_mastery.p_eff >= config.mastery_threshold

    if not is_mastered_candidate:
        reason = (
            f"Effective mastery of {current_concept_id} ('{title_curr}') "
            f"is {current_mastery.p_eff * 100:.1f}% (target: {config.mastery_threshold * 100:.1f}%). "
            f"Delivering targeted practice problems within your Zone of Proximal Development."
        )
        return Decision(
            action=ActionType.PRACTICE,
            target_concept=current_concept_id,
            target_concept_id=current_concept_id,
            reason=reason,
            rule_triggered="Rule 4: Practice (ZPD Consolidation)",
            inputs_snapshot=inputs_snapshot,
            metadata={"p_eff": current_mastery.p_eff},
        )

    if current_mastery.is_fragile:
        reason = (
            f"Concept {current_concept_id} mastery is capped at {current_mastery.p_eff * 100:.1f}% "
            f"and tagged as 'fragile' because a prerequisite has lower mastery. "
            f"Consolidation practice required to stabilize foundational consistency."
        )
        return Decision(
            action=ActionType.PRACTICE,
            target_concept=current_concept_id,
            target_concept_id=current_concept_id,
            reason=reason,
            rule_triggered="Rule 4: Practice (Fragile Mastery Stabilization)",
            inputs_snapshot=inputs_snapshot,
            metadata={"p_eff": current_mastery.p_eff, "is_fragile": True},
        )

    if not current_mastery.transfer_verified:
        reason = (
            f"Mastery belief for {current_concept_id} reached {current_mastery.p_eff * 100:.1f}%, "
            f"but remains 'provisional'. Higher-difficulty transfer verification problem required "
            f"to confirm robust mastery without guessing/slipping."
        )
        return Decision(
            action=ActionType.PRACTICE,
            target_concept=current_concept_id,
            target_concept_id=current_concept_id,
            reason=reason,
            rule_triggered="Rule 4: Practice (Transfer Problem Verification)",
            inputs_snapshot=inputs_snapshot,
            metadata={"p_eff": current_mastery.p_eff, "transfer_verified": False},
        )

    # RULE 5: Advance
    next_concept_id = find_next_advance_target(
        current_concept_id=current_concept_id,
        mastery_map=mastery_map,
        graph=graph,
        config=config,
    )
    if next_concept_id is not None and not challenge_mode:
        n_title = graph.get_concept_title(next_concept_id) if hasattr(graph, "get_concept_title") else next_concept_id
        reason = (
            f"Concept {current_concept_id} ('{title_curr}') "
            f"mastered at {current_mastery.p_eff * 100:.1f}% with verified transfer evidence. "
            f"Advancing to next unlocked concept {next_concept_id} "
            f"('{n_title}'). All prerequisites satisfied >= "
            f"{config.prereq_remediation_threshold * 100:.1f}%."
        )
        return Decision(
            action=ActionType.ADVANCE,
            target_concept=next_concept_id,
            target_concept_id=next_concept_id,
            reason=reason,
            rule_triggered="Rule 5: Advance (Next Unlocked Concept)",
            inputs_snapshot=inputs_snapshot,
            metadata={"advanced_from": current_concept_id, "advanced_to": next_concept_id},
        )

    # RULE 6: Challenge
    avg_mastery = sum(m.p_eff for m in mastery_map.values()) / max(len(mastery_map), 1)
    target_challenge = "C10" if "C10" in mastery_map else current_concept_id
    c_title = graph.get_concept_title(target_challenge) if hasattr(graph, "get_concept_title") else target_challenge
    reason = (
        f"Challenge mode active (Overall curriculum mastery {avg_mastery * 100:.1f}%). "
        f"Serving capstone multi-step transfer problems on {target_challenge} "
        f"('{c_title}') for high-performing learners."
    )
    return Decision(
        action=ActionType.CHALLENGE,
        target_concept=target_challenge,
        target_concept_id=target_challenge,
        reason=reason,
        rule_triggered="Rule 6: Challenge (Capstone & Acceleration)",
        inputs_snapshot=inputs_snapshot,
        metadata={"avg_curriculum_mastery": avg_mastery, "challenge_mode": challenge_mode},
    )


def reconstruct_decision_from_snapshot(
    snapshot: Dict[str, Any],
    graph: Optional[CurriculumGraph] = None,
) -> Decision:
    """Test 8 Proof: Reconstructs exact decision deterministically from stored inputs_json."""
    if graph is None:
        graph = CurriculumGraph(CANONICAL_CONCEPTS)

    student_id = snapshot["student_id"]
    current_concept_id = snapshot["current_concept_id"]
    challenge_mode = snapshot.get("challenge_mode", False)
    config = EngineConfig.from_dict(snapshot["config"])

    mastery_map: Dict[str, ConceptMastery] = {}
    for cid, state_dict in snapshot["mastery_state"].items():
        mastery_map[cid] = ConceptMastery.from_dict(state_dict)

    active_override = snapshot.get("active_override")

    return make_decision(
        student_id=student_id,
        current_concept_id=current_concept_id,
        mastery_map=mastery_map,
        graph=graph,
        config=config,
        challenge_mode=challenge_mode,
        active_override=active_override,
    )


class DecisionEngine:
    """
    6 Ordered Deterministic Pedagogical Rules matching Section 5 of the charter.
    Authored by Yash (ML Lead).
    """
    def __init__(
        self,
        dag: Any,
        bkt: Any,
        config_version: int = 1,
        stuck_cycles: int = 3,
        stuck_delta: float = 0.05,
        prereq_threshold: float = 0.55,
        review_threshold: float = 0.60,
        mastery_threshold: float = 0.85
    ):
        self.dag = dag
        self.bkt = bkt
        self.config_version = config_version
        self.stuck_cycles = stuck_cycles
        self.stuck_delta = stuck_delta
        self.prereq_threshold = prereq_threshold
        self.review_threshold = review_threshold
        self.mastery_threshold = mastery_threshold

    def get_concept_name(self, cid: str) -> str:
        if hasattr(self.dag, "concept_metadata"):
            meta = self.dag.concept_metadata.get(cid, {})
            return meta.get('name', cid)
        elif hasattr(self.dag, "get_concept_title"):
            return self.dag.get_concept_title(cid)
        return cid

    def next_action(self, learner_state: Any, active_concept_id: Optional[str] = None) -> Decision:
        cid = active_concept_id or getattr(learner_state, "active_concept_id", "C1") or "C1"
        current_cm = learner_state.get_or_create_concept(cid)

        capping_results = self.dag.apply_all_cappings(learner_state)
        current_p_eff = capping_results[cid]['p_eff_capped']
        current_status = capping_results[cid]['status']
        current_fragile = capping_results[cid]['is_fragile']

        inputs_snapshot = {
            'student_id': learner_state.student_id,
            'active_concept_id': cid,
            'virtual_clock': getattr(learner_state, "virtual_clock", 0.0),
            'consecutive_low_deltas': getattr(current_cm, "consecutive_low_deltas", 0),
            'p_eff_map': {c: capping_results[c]['p_eff_capped'] for c in capping_results},
            'status_map': {c: capping_results[c]['status'] for c in capping_results},
            'evidence_map': {c: learner_state.get_or_create_concept(c).evidence_sum for c in capping_results},
            'config_version': self.config_version
        }

        # Rule 1: Teacher Intervention
        if getattr(current_cm, "consecutive_low_deltas", 0) >= self.stuck_cycles:
            reason = (
                f"Teacher Intervention Required: Student made <{self.stuck_delta*100:.0f}% mastery gain "
                f"across {current_cm.consecutive_low_deltas} consecutive attempts on {cid} ({self.get_concept_name(cid)}). "
                f"Halting automated loop to alert instructor on the stuck learner escalation queue."
            )
            return Decision(
                action=ActionType.TEACHER_INTERVENTION,
                target_concept=cid,
                target_concept_id=cid,
                target_concept_name=self.get_concept_name(cid),
                reason=reason,
                rule_number=1,
                rule_name="Teacher Intervention",
                rule_triggered="Rule 1: Teacher Intervention (Stagnation)",
                p_eff=current_p_eff,
                evidence_sum=current_cm.evidence_sum,
                status=current_status,
                is_fragile=current_fragile,
                config_version=self.config_version,
                inputs_json=inputs_snapshot,
                inputs_snapshot=inputs_snapshot
            )

        # Rule 2: Remediate Prerequisite
        weakest_prereq = self.dag.find_weakest_prerequisite(
            cid, learner_state, prereq_threshold=self.prereq_threshold
        )
        if weakest_prereq is not None:
            w_cid, w_p = weakest_prereq
            w_name = self.get_concept_name(w_cid)
            reason = (
                f"Remediate Prerequisite -> {w_cid} ({w_name}): "
                f"You are practicing {cid} ({self.get_concept_name(cid)}), but prerequisite {w_cid} "
                f"is at {w_p*100:.1f}% (below {self.prereq_threshold*100:.0f}% threshold). "
                f"Healing foundational gap before advancing on {cid}."
            )
            w_cm = learner_state.get_or_create_concept(w_cid)
            return Decision(
                action=ActionType.REMEDIATE_PREREQUISITE,
                target_concept=w_cid,
                target_concept_id=w_cid,
                target_concept_name=w_name,
                reason=reason,
                rule_number=2,
                rule_name="Remediate Prerequisite",
                rule_triggered="Rule 2: Remediate Prerequisite (Weak Foundation)",
                p_eff=w_p,
                evidence_sum=w_cm.evidence_sum,
                status=capping_results[w_cid]['status'],
                is_fragile=capping_results[w_cid]['is_fragile'],
                config_version=self.config_version,
                inputs_json=inputs_snapshot,
                inputs_snapshot=inputs_snapshot
            )

        # Rule 3: Spaced Review
        decayed_candidates = []
        for c in self.dag.get_topological_order():
            cm_check = learner_state.get_or_create_concept(c)
            if getattr(cm_check, "is_mastered_certified", False) or getattr(cm_check, "was_mastered", False):
                decay_state = cm_check.get_effective_mastery(
                    getattr(learner_state, "virtual_clock", 0.0),
                    floor=getattr(self.bkt, "decay_floor", 0.25),
                    review_threshold=self.review_threshold
                )
                if decay_state.p_eff < self.review_threshold or getattr(cm_check, "needs_review", False):
                    decayed_candidates.append((c, decay_state.p_eff, decay_state.dt_days))

        if decayed_candidates:
            decayed_candidates.sort(key=lambda x: x[1])
            d_cid, d_p, d_days = decayed_candidates[0]
            d_name = self.get_concept_name(d_cid)
            reason = (
                f"Spaced Review -> {d_cid} ({d_name}): "
                f"Previously mastered concept decayed to p_eff {d_p*100:.1f}% after {d_days:.1f} days "
                f"via Ebbinghaus curve (below review threshold {self.review_threshold*100:.0f}%). "
                f"Triggering retrieval practice to reinforce retention."
            )
            d_cm = learner_state.get_or_create_concept(d_cid)
            return Decision(
                action=ActionType.SPACED_REVIEW if hasattr(ActionType, "SPACED_REVIEW") else ActionType.REVIEW,
                target_concept=d_cid,
                target_concept_id=d_cid,
                target_concept_name=d_name,
                reason=reason,
                rule_number=3,
                rule_name="Spaced Review",
                rule_triggered="Rule 3: Spaced Review (Ebbinghaus Decay)",
                p_eff=d_p,
                evidence_sum=d_cm.evidence_sum,
                status="review_due",
                is_fragile=capping_results[d_cid]['is_fragile'],
                config_version=self.config_version,
                inputs_json=inputs_snapshot,
                inputs_snapshot=inputs_snapshot
            )

        # Rule 4: Practice
        is_mastered = getattr(current_cm, "is_mastered_certified", False) or getattr(current_cm, "was_mastered", False)
        if (not is_mastered) or current_fragile:
            if current_fragile:
                reason = (
                    f"Practice {cid} ({self.get_concept_name(cid)}): "
                    f"Concept mastery is capped at {current_p_eff*100:.1f}% and marked 'fragile' "
                    f"due to weak prerequisite foundation. Additional practice required."
                )
            elif current_p_eff >= self.mastery_threshold and not getattr(current_cm, "has_transfer_success", False):
                reason = (
                    f"Practice {cid} ({self.get_concept_name(cid)}): "
                    f"p_eff is {current_p_eff*100:.1f}% >= 85%, but marked 'Provisional'. "
                    f"Needs 1 transfer answer (d >= 0.5, w >= 0.5) to certify mastery."
                )
            else:
                reason = (
                    f"Practice {cid} ({self.get_concept_name(cid)}): "
                    f"Current effective mastery is {current_p_eff*100:.1f}% (target: {self.mastery_threshold*100:.0f}%). "
                    f"Delivering deliberate practice in Zone of Proximal Development."
                )
            return Decision(
                action=ActionType.PRACTICE,
                target_concept=cid,
                target_concept_id=cid,
                target_concept_name=self.get_concept_name(cid),
                reason=reason,
                rule_number=4,
                rule_name="Practice",
                rule_triggered="Rule 4: Practice (Zone of Proximal Development)",
                p_eff=current_p_eff,
                evidence_sum=current_cm.evidence_sum,
                status=current_status,
                is_fragile=current_fragile,
                config_version=self.config_version,
                inputs_json=inputs_snapshot,
                inputs_snapshot=inputs_snapshot
            )

        # Rule 5: Advance
        topo = self.dag.get_topological_order()
        unlocked = self.dag.get_unlocked_concepts(learner_state, prereq_threshold=self.prereq_threshold)
        next_cid = None
        for cand in topo:
            cand_cm = learner_state.get_or_create_concept(cand)
            cand_m = getattr(cand_cm, "is_mastered_certified", False) or getattr(cand_cm, "was_mastered", False)
            if cand in unlocked and not cand_m:
                next_cid = cand
                break

        if next_cid is not None and next_cid != cid:
            n_name = self.get_concept_name(next_cid)
            n_cm = learner_state.get_or_create_concept(next_cid)
            reason = (
                f"Advance -> {next_cid} ({n_name}): "
                f"Successfully certified mastery on {cid} (p_eff {current_p_eff*100:.1f}%, transfer verified). "
                f"All prerequisites for {next_cid} met (>= {self.prereq_threshold*100:.0f}%). Advancing curriculum."
            )
            return Decision(
                action=ActionType.ADVANCE,
                target_concept=next_cid,
                target_concept_id=next_cid,
                target_concept_name=n_name,
                reason=reason,
                rule_number=5,
                rule_name="Advance",
                rule_triggered="Rule 5: Advance (Next Unlocked Concept)",
                p_eff=capping_results[next_cid]['p_eff_capped'],
                evidence_sum=n_cm.evidence_sum,
                status=capping_results[next_cid]['status'],
                is_fragile=capping_results[next_cid]['is_fragile'],
                config_version=self.config_version,
                inputs_json=inputs_snapshot,
                inputs_snapshot=inputs_snapshot
            )

        # Rule 6: Challenge
        capstone_cid = topo[-1]
        cap_name = self.get_concept_name(capstone_cid)
        cap_cm = learner_state.get_or_create_concept(capstone_cid)
        reason = (
            f"Challenge -> {capstone_cid} ({cap_name}): "
            f"All unlocked foundational concepts mastered. "
            f"Routing gifted learner to Capstone multi-step transfer challenge."
        )
        return Decision(
            action=ActionType.CHALLENGE,
            target_concept=capstone_cid,
            target_concept_id=capstone_cid,
            target_concept_name=cap_name,
            reason=reason,
            rule_number=6,
            rule_name="Challenge",
            rule_triggered="Rule 6: Challenge (Capstone Synthesis)",
            p_eff=capping_results[capstone_cid]['p_eff_capped'],
            evidence_sum=cap_cm.evidence_sum,
            status=capping_results[capstone_cid]['status'],
            is_fragile=capping_results[capstone_cid]['is_fragile'],
            config_version=self.config_version,
            inputs_json=inputs_snapshot,
            inputs_snapshot=inputs_snapshot
        )

    def decide_from_snapshot(self, inputs_json: Dict[str, Any], config_version: int = 1) -> Decision:
        student_id = inputs_json.get('student_id', 'STU_REPRO')
        from .mastery import LearnerState
        learner = LearnerState(student_id=student_id, virtual_clock=inputs_json.get('virtual_clock', 0.0))
        active_cid = inputs_json.get('active_concept_id', 'C1')
        learner.active_concept_id = active_cid

        p_eff_map = inputs_json.get('p_eff_map', {})
        status_map = inputs_json.get('status_map', {})
        evidence_map = inputs_json.get('evidence_map', {})

        for cid, p_val in p_eff_map.items():
            cm = learner.get_or_create_concept(cid, default_p=p_val)
            cm.p = p_val
            cm.evidence_sum = evidence_map.get(cid, 0.0)
            if status_map.get(cid) == 'mastered':
                cm.is_mastered_certified = True
                cm.has_transfer_success = True

        active_cm = learner.get_or_create_concept(active_cid)
        active_cm.consecutive_low_deltas = inputs_json.get('consecutive_low_deltas', 0)

        return self.next_action(learner, active_concept_id=active_cid)

