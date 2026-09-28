"""
Diagnostic Engine & Cold Start Graph Propagation (coldstart.py).
Owner: Yash (ML Model & Knowledge Tracing Lead)
Shannon Entropy item selection and 0.3*w graph propagation across the DAG.
Pure Python, Zero External Network Calls.
"""

import math
from typing import Dict, List, Optional, Tuple, Any
from .graph import PrerequisiteGraph, ConceptDAG
from .mastery import BKTModel, LearnerState, ConceptMastery, AttemptResult, update_bkt
from .weights import TelemetrySignal, compute_evidence_weight


class DiagnosticEngine:
    """Manages diagnostic sequence, Shannon entropy item selection, and graph-based cold-start propagation."""

    def __init__(
        self,
        graph: Optional[Any] = None,
        diagnostic_concepts: Optional[List[str]] = None,
        dag: Optional[Any] = None,
        bkt: Optional[BKTModel] = None
    ):
        self.dag = dag or graph
        self.graph = graph or dag
        self.bkt = bkt or BKTModel()
        self.diagnostic_concepts = diagnostic_concepts or ["C1", "C2", "C3", "C4", "C6", "C7"]
        self.default_diagnostic_concepts = self.diagnostic_concepts

    @staticmethod
    def calculate_shannon_entropy(p: float) -> float:
        """
        // INFORMATION-GAIN ITEM SELECTION
        # FORMULA: Shannon entropy of Bernoulli knowledge state
        # RATIONALE: Maximizes diagnostic information gain by selecting concept closest to p=0.5
        """
        p_clamped = max(0.001, min(0.999, p))
        return -(p_clamped * math.log2(p_clamped) + (1.0 - p_clamped) * math.log2(1.0 - p_clamped))

    def select_next_uncertain_concept(
        self,
        learner_state: LearnerState,
        candidate_concepts: Optional[List[str]] = None
    ) -> str:
        """Selects candidate concept with highest epistemic uncertainty (closest to p=0.5)."""
        candidates = candidate_concepts or (
            self.dag.get_topological_order() if (self.dag and hasattr(self.dag, 'get_topological_order'))
            else self.diagnostic_concepts
        )
        max_entropy = -1.0
        best_concept = candidates[0]

        for cid in candidates:
            cm = learner_state.get_or_create_concept(cid)
            entropy = self.calculate_shannon_entropy(cm.p)
            if entropy > max_entropy:
                max_entropy = entropy
                best_concept = cid

        return best_concept

    def pick_next_diagnostic_concept(
        self,
        assessed_concepts: List[str],
        current_mastery: Dict[str, float]
    ) -> Optional[str]:
        """Picks unassessed diagnostic concept with highest uncertainty (closest to p=0.5)."""
        unassessed = [c for c in self.diagnostic_concepts if c not in assessed_concepts]
        if not unassessed:
            return None
        return min(unassessed, key=lambda c: abs(current_mastery.get(c, 0.30) - 0.50))

    def process_diagnostic_attempt(
        self,
        learner_state: LearnerState,
        concept_id: str,
        correct: bool,
        difficulty: float,
        telemetry: Optional[TelemetrySignal] = None,
        propagation_factor: float = 0.3
    ) -> Dict[str, Any]:
        """
        Processes diagnostic answer and propagates 0.3*w evidence across graph neighbors (Test 7).
        """
        if telemetry is None:
            telemetry = TelemetrySignal(hints_used=0, attempt_no=1, time_ms=10000, confidence='medium', correct=correct)

        cm = learner_state.get_or_create_concept(concept_id)
        result = self.bkt.update_mastery(
            concept=cm,
            correct=correct,
            difficulty=difficulty,
            is_transfer=False,
            telemetry=telemetry,
            current_timestamp=getattr(learner_state, 'virtual_clock', 0.0)
        )
        w = result.evidence_weight

        propagated_updates = {}
        target_val = 0.80 if correct else 0.20

        # Upstream prerequisites propagation
        prereqs = []
        if self.dag:
            if hasattr(self.dag, 'get_direct_prerequisites'):
                prereqs = self.dag.get_direct_prerequisites(concept_id)
            elif hasattr(self.dag, 'get_prerequisites'):
                prereqs = self.dag.get_prerequisites(concept_id)

        for prereq_id in prereqs:
            pcm = learner_state.get_or_create_concept(prereq_id)
            delta = propagation_factor * w * (target_val - pcm.p)
            pcm.p = max(0.01, min(0.99, round(pcm.p + delta, 4)))
            pcm.evidence_sum = round(pcm.evidence_sum + (0.3 * w), 4)
            propagated_updates[prereq_id] = pcm.p

        # Downstream children propagation
        children = []
        if self.dag:
            if hasattr(self.dag, 'get_direct_children'):
                children = self.dag.get_direct_children(concept_id)
            elif hasattr(self.dag, 'get_dependents'):
                children = self.dag.get_dependents(concept_id)

        for child_id in children:
            ccm = learner_state.get_or_create_concept(child_id)
            delta = (propagation_factor * 0.5) * w * (target_val - ccm.p)
            ccm.p = max(0.01, min(0.99, round(ccm.p + delta, 4)))
            ccm.evidence_sum = round(ccm.evidence_sum + (0.15 * w), 4)
            propagated_updates[child_id] = ccm.p

        if self.dag and hasattr(self.dag, 'apply_all_cappings'):
            self.dag.apply_all_cappings(learner_state)

        return {
            'target_concept': concept_id,
            'primary_result': result,
            'propagated_updates': propagated_updates,
            'evidence_weight': w
        }

    def propagate_diagnostic_evidence(
        self,
        target_concept: str,
        is_correct: bool,
        w: float,
        mastery_state: Dict[str, float],
        propagation_attenuation: float = 0.30
    ) -> Dict[str, float]:
        """
        Updates target concept via BKT and propagates attenuated evidence (0.3*w) across prerequisite edges.
        """
        updated_state = dict(mastery_state)

        # 1. Update target concept directly
        p_target = updated_state.get(target_concept, 0.30)
        p_target_new, _ = update_bkt(p_target, is_correct=is_correct, difficulty=0.5, w=w)
        updated_state[target_concept] = p_target_new

        # 2. Propagate to direct prerequisites
        prereqs = []
        if self.dag:
            if hasattr(self.dag, 'get_direct_prerequisites'):
                prereqs = self.dag.get_direct_prerequisites(target_concept)
            elif hasattr(self.dag, 'get_prerequisites'):
                prereqs = self.dag.get_prerequisites(target_concept)

        for pr in prereqs:
            p_pr = updated_state.get(pr, 0.30)
            p_pr_new, _ = update_bkt(
                p_pr,
                is_correct=is_correct,
                difficulty=0.4,
                w=round(w * propagation_attenuation, 4)
            )
            updated_state[pr] = p_pr_new

        # 3. Propagate to direct dependents
        dependents = []
        if self.dag:
            if hasattr(self.dag, 'get_direct_children'):
                dependents = self.dag.get_direct_children(target_concept)
            elif hasattr(self.dag, 'get_dependents'):
                dependents = self.dag.get_dependents(target_concept)

        for dep in dependents:
            p_dep = updated_state.get(dep, 0.30)
            p_dep_new, _ = update_bkt(
                p_dep,
                is_correct=is_correct,
                difficulty=0.6,
                w=round(w * propagation_attenuation, 4)
            )
            updated_state[dep] = p_dep_new

        return updated_state

    def initialize_learner_vector(
        self,
        student_id: str,
        diagnostic_answers: List[Dict[str, Any]]
    ) -> LearnerState:
        """Calibrates initial cognitive vector for a new student given a sequence of diagnostic answers."""
        learner = LearnerState(student_id=student_id)
        for ans in diagnostic_answers:
            cid = ans.get('concept_id', 'C1')
            correct = ans.get('correct', True)
            diff = ans.get('difficulty', 0.2)
            telemetry = TelemetrySignal(
                hints_used=ans.get('hints_used', 0),
                time_ms=ans.get('time_ms', 10000),
                confidence=ans.get('confidence', 'medium'),
                correct=correct
            )
            self.process_diagnostic_attempt(
                learner_state=learner,
                concept_id=cid,
                correct=correct,
                difficulty=diff,
                telemetry=telemetry
            )
        return learner
