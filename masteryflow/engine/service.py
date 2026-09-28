"""
MasteryFlow Machine Learning Service & Integration Layer
Official Hand-off Interface for Backend (FastAPI), Persistence (SQLite),
and Frontend (Streamlit). Provides production-ready helper functions.
"""
import os
import json
import time
from typing import Dict, List, Optional, Any, Tuple

from .mastery import BKTModel, LearnerState, ConceptMastery, AttemptResult
from .weights import TelemetrySignal, compute_evidence_weight
from .decay import compute_decayed_mastery, update_review_stability
from .graph import ConceptDAG
from .coldstart import DiagnosticEngine
from .decide import DecisionEngine, Decision, ActionType


class MLService:
    """
    Singleton ML Service managing psychometric models and student cognitive states.
    Designed for clean integration with FastAPI routes and SQLite databases.
    """
    def __init__(
        self,
        concepts_json_path: Optional[str] = None,
        config_yaml_path: Optional[str] = None
    ):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
        c_path = concepts_json_path or os.path.join(base_dir, "concepts.json")
        
        self.dag = ConceptDAG(c_path if os.path.exists(c_path) else None)
        self.bkt = BKTModel(
            learning_transition_rate=0.15,
            mastery_threshold=0.85,
            min_evidence_sum=3.0,
            decay_floor=0.25,
            review_threshold=0.60
        )
        self.decision_engine = DecisionEngine(
            dag=self.dag,
            bkt=self.bkt,
            config_version=1,
            stuck_cycles=3,
            stuck_delta=0.05,
            prereq_threshold=0.55,
            review_threshold=0.60,
            mastery_threshold=0.85
        )
        self.diagnostic_engine = DiagnosticEngine(dag=self.dag, bkt=self.bkt)

        # In-memory session registry (backed by persistence layer)
        self.learners: Dict[str, LearnerState] = {}
        self.overrides_log: List[Dict[str, Any]] = []

    def get_or_create_learner(self, student_id: str) -> LearnerState:
        if student_id not in self.learners:
            self.learners[student_id] = LearnerState(student_id=student_id)
        return self.learners[student_id]

    def record_attempt(
        self,
        student_id: str,
        concept_id: str,
        is_correct: bool,
        difficulty: float = 0.3,
        is_transfer: bool = False,
        hints_used: int = 0,
        attempt_no: int = 1,
        retry_gap_seconds: float = 999.0,
        time_ms: int = 10000,
        confidence: str = 'medium'
    ) -> AttemptResult:
        """
        Processes a student assessment attempt through the full BKT and anti-gaming pipeline.
        Returns serialized AttemptResult for REST API responses.
        """
        learner = self.get_or_create_learner(student_id)
        cm = learner.get_or_create_concept(concept_id)

        telemetry = TelemetrySignal(
            hints_used=hints_used,
            attempt_no=attempt_no,
            retry_gap_seconds=retry_gap_seconds,
            prev_correct=(attempt_no == 1 or is_correct),
            time_ms=time_ms,
            min_time_ms=3000,
            confidence=confidence,
            correct=is_correct
        )

        result = self.bkt.update_mastery(
            concept=cm,
            correct=is_correct,
            difficulty=difficulty,
            is_transfer=is_transfer,
            telemetry=telemetry,
            current_timestamp=learner.virtual_clock
        )

        # Update active concept
        learner.active_concept_id = concept_id

        # Re-evaluate DAG capping
        self.dag.apply_all_cappings(learner)

        return result

    def next_action(self, student_id: str, active_concept_id: Optional[str] = None) -> Decision:
        """
        Computes the next optimal pedagogical action matching 6 deterministic rules.
        """
        learner = self.get_or_create_learner(student_id)
        target_cid = active_concept_id or learner.active_concept_id or 'C1'
        return self.decision_engine.next_action(learner, active_concept_id=target_cid)

    def get_student_state(self, student_id: str) -> Dict[str, Any]:
        """
        Returns full cognitive profile for a student including all 10 concepts,
        effective masteries, statuses, fragility flags, and uncertainty metrics.
        """
        learner = self.get_or_create_learner(student_id)
        cappings = self.dag.apply_all_cappings(learner)

        concepts_out = {}
        for cid in self.dag.get_topological_order():
            cm = learner.get_or_create_concept(cid)
            meta = self.dag.concept_metadata.get(cid, {})
            c_info = cappings.get(cid, {'p_eff_capped': cm.p, 'status': 'practicing', 'is_fragile': False})
            unc = cm.compute_uncertainty()

            concepts_out[cid] = {
                'id': cid,
                'name': meta.get('name', cid),
                'short_name': meta.get('short_name', cid),
                'raw_p': cm.p,
                'p_eff': c_info['p_eff_capped'],
                'evidence_sum': cm.evidence_sum,
                'status': c_info['status'],
                'is_fragile': c_info['is_fragile'],
                'is_mastered': cm.is_mastered_certified,
                'has_transfer': cm.has_transfer_success,
                'uncertainty': unc
            }

        return {
            'student_id': student_id,
            'active_concept_id': learner.active_concept_id,
            'virtual_clock': learner.virtual_clock,
            'concepts': concepts_out
        }

    def apply_teacher_override(
        self,
        student_id: str,
        override_concept: str,
        override_action: str,
        teacher_name: str,
        reason: str
    ) -> Decision:
        """
        Persists a teacher override and resets student target concept.
        Enforces Teacher Sovereignty: human instructor has ultimate routing authority.
        """
        learner = self.get_or_create_learner(student_id)
        learner.active_concept_id = override_concept

        override_record = {
            'student_id': student_id,
            'override_concept': override_concept,
            'override_action': override_action,
            'teacher_name': teacher_name,
            'reason': reason,
            'timestamp': time.time()
        }
        self.overrides_log.append(override_record)

        cm = learner.get_or_create_concept(override_concept)
        cappings = self.dag.apply_all_cappings(learner)
        c_info = cappings.get(override_concept, {'p_eff_capped': cm.p, 'status': 'practicing', 'is_fragile': False})

        # Return explicit override decision
        act_enum = ActionType.PRACTICE
        if 'remediat' in override_action.lower():
            act_enum = ActionType.REMEDIATE_PREREQUISITE
        elif 'review' in override_action.lower():
            act_enum = ActionType.SPACED_REVIEW
        elif 'advance' in override_action.lower():
            act_enum = ActionType.ADVANCE
        elif 'challenge' in override_action.lower():
            act_enum = ActionType.CHALLENGE

        return Decision(
            action=act_enum,
            target_concept=override_concept,
            target_concept_name=self.dag.concept_metadata.get(override_concept, {}).get('name', override_concept),
            reason=f"Teacher Override by {teacher_name}: {reason}",
            rule_number=0,
            rule_name="Teacher Override",
            p_eff=c_info['p_eff_capped'],
            evidence_sum=cm.evidence_sum,
            status=c_info['status'],
            is_fragile=c_info['is_fragile'],
            config_version=self.decision_engine.config_version,
            inputs_json={'teacher_override': override_record}
        )

    def advance_student_time(self, student_id: str, days: float) -> Dict[str, Any]:
        """
        Advances the virtual clock for a learner to trigger Ebbinghaus decay.
        """
        learner = self.get_or_create_learner(student_id)
        learner.advance_virtual_clock_days(days)
        return self.get_student_state(student_id)

    def get_cohort_heatmap(self, student_ids: List[str]) -> Dict[str, Dict[str, float]]:
        """
        Returns student x concept mastery matrix for Shreyash's Teacher Heatmap.
        """
        heatmap = {}
        for sid in student_ids:
            learner = self.get_or_create_learner(sid)
            cappings = self.dag.apply_all_cappings(learner)
            heatmap[sid] = {
                cid: cappings[cid]['p_eff_capped'] for cid in self.dag.get_topological_order()
            }
        return heatmap

    def get_stuck_learners(self) -> List[Dict[str, Any]]:
        """
        Scans all active learners and returns students failing to gain >= 0.05 across 3 cycles.
        """
        stuck = []
        for sid, learner in self.learners.items():
            cid = learner.active_concept_id or 'C1'
            cm = learner.get_or_create_concept(cid)
            if cm.consecutive_low_deltas >= self.decision_engine.stuck_cycles:
                stuck.append({
                    'student_id': sid,
                    'stuck_concept': cid,
                    'concept_name': self.dag.concept_metadata.get(cid, {}).get('name', cid),
                    'consecutive_cycles': cm.consecutive_low_deltas,
                    'current_p': cm.p
                })
        return stuck


# Global Service Instance for direct module import
default_service = MLService()

# Module-level convenience functions
def record_attempt(*args, **kwargs):
    return default_service.record_attempt(*args, **kwargs)

def next_action(*args, **kwargs):
    return default_service.next_action(*args, **kwargs)

def get_student_state(*args, **kwargs):
    return default_service.get_student_state(*args, **kwargs)

def apply_teacher_override(*args, **kwargs):
    return default_service.apply_teacher_override(*args, **kwargs)

def advance_student_time(*args, **kwargs):
    return default_service.advance_student_time(*args, **kwargs)

def get_cohort_heatmap(*args, **kwargs):
    return default_service.get_cohort_heatmap(*args, **kwargs)

def get_stuck_learners(*args, **kwargs):
    return default_service.get_stuck_learners(*args, **kwargs)
