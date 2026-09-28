"""
Bayesian Knowledge Tracing (BKT) Engine (mastery.py).
Authors: Yash (ML Model & Knowledge Tracing Lead) & Soham Choudhury
Implements Corbett-Anderson BKT augmented with item response difficulty scaling,
multi-signal anti-gaming dampening, and object-oriented BKTModel / LearnerState architecture.
"""

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any, Union

from .weights import compute_evidence_weight, TelemetrySignal, EvidenceWeightResult
from .decay import compute_decayed_mastery, update_review_stability, DecayState


@dataclass
class AttemptResult:
    concept_id: str
    is_correct: bool
    difficulty: float
    is_transfer: bool
    evidence_weight: float
    prior_p: float
    posterior_p: float
    new_p: float
    evidence_sum: float
    status: str  # 'mastered', 'provisional', 'practicing', 'fragile', 'review_due'
    uncertainty_se: float
    is_misconception: bool
    telemetry_details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ConceptMastery:
    concept_id: str
    p: float = 0.20
    stability_days: float = 7.0
    last_practiced_timestamp: float = 0.0
    evidence_sum: float = 0.0
    attempts_count: int = 0
    correct_count: int = 0
    has_transfer_success: bool = False
    is_mastered_certified: bool = False
    is_fragile: bool = False
    needs_review: bool = False
    consecutive_low_deltas: int = 0
    history: List[Dict[str, Any]] = field(default_factory=list)

    @property
    def was_mastered(self) -> bool:
        return self.is_mastered_certified

    @was_mastered.setter
    def was_mastered(self, val: bool) -> None:
        self.is_mastered_certified = val

    @property
    def transfer_verified(self) -> bool:
        return self.has_transfer_success

    @transfer_verified.setter
    def transfer_verified(self, val: bool) -> None:
        self.has_transfer_success = val

    @property
    def errors_count(self) -> int:
        return max(0, self.attempts_count - self.correct_count)

    def get_effective_mastery(
        self,
        current_timestamp: float,
        floor: float = 0.25,
        review_threshold: float = 0.60
    ) -> DecayState:
        """Evaluates read-time Ebbinghaus decay."""
        if current_timestamp <= self.last_practiced_timestamp:
            dt_days = 0.0
        else:
            dt_days = (current_timestamp - self.last_practiced_timestamp) / 86400.0

        state = compute_decayed_mastery(
            p=self.p,
            dt_days=dt_days,
            stability=self.stability_days,
            floor=floor,
            was_mastered=self.is_mastered_certified,
            review_threshold=review_threshold
        )
        if self.needs_review:
            state.is_review_due = True
        return state

    def compute_uncertainty(self) -> Dict[str, Any]:
        """
        Quantifies epistemic uncertainty via BKT variance and standard error.
        sigma = sqrt(p * (1 - p))
        SE = sigma / sqrt(1 + evidence_sum)
        """
        p_val = max(0.001, min(0.999, self.p))
        sigma = math.sqrt(p_val * (1.0 - p_val))
        se = sigma / math.sqrt(1.0 + self.evidence_sum)
        ci_lower = max(0.0, round(self.p - 1.96 * se, 3))
        ci_upper = min(1.0, round(self.p + 1.96 * se, 3))

        level = 'low' if se <= 0.08 else ('medium' if se <= 0.15 else 'high')

        return {
            'variance': round(sigma ** 2, 4),
            'standard_error': round(se, 4),
            'confidence_interval': [ci_lower, ci_upper],
            'uncertainty_level': level
        }

    def determine_status(self, p_eff: float) -> str:
        """
        Evaluates mastery status:
        1. Latent Mastery: p_eff >= 0.85
        2. Evidence Threshold: evidence_sum >= 3.0
        3. Transfer Verification: has_transfer_success == True
        """
        if self.is_fragile:
            return 'fragile'

        if self.is_mastered_certified and (self.needs_review or p_eff < 0.60):
            return 'review_due'

        if p_eff >= 0.85:
            if self.has_transfer_success and self.evidence_sum >= 3.0:
                self.is_mastered_certified = True
                self.needs_review = False
                return 'mastered'
            else:
                return 'provisional'

        return 'practicing'


class BKTModel:
    """
    Bayesian Knowledge Tracing with Item Difficulty Scaling.
    """
    def __init__(
        self,
        learning_transition_rate: float = 0.15,
        mastery_threshold: float = 0.85,
        min_evidence_sum: float = 3.0,
        decay_floor: float = 0.25,
        review_threshold: float = 0.60,
        slip_base: float = 0.10,
        slip_slope: float = 0.05,
        guess_base: float = 0.30,
        guess_slope: float = 0.15
    ):
        self.T = learning_transition_rate
        self.mastery_threshold = mastery_threshold
        self.min_evidence_sum = min_evidence_sum
        self.decay_floor = decay_floor
        self.review_threshold = review_threshold
        self.slip_base = slip_base
        self.slip_slope = slip_slope
        self.guess_base = guess_base
        self.guess_slope = guess_slope

    def calculate_slip_and_guess(self, difficulty: float) -> Tuple[float, float]:
        d = max(0.0, min(1.0, difficulty))
        s = self.slip_base + self.slip_slope * d
        g = self.guess_base - self.guess_slope * d
        return round(s, 4), round(g, 4)

    def update_mastery(
        self,
        concept: ConceptMastery,
        correct: bool,
        difficulty: float,
        is_transfer: bool,
        telemetry: TelemetrySignal,
        current_timestamp: float,
        is_review: bool = False
    ) -> AttemptResult:
        s, g = self.calculate_slip_and_guess(difficulty)
        evidence_res = compute_evidence_weight(telemetry)
        w = evidence_res.weight
        prior_p = concept.p

        decay_state = concept.get_effective_mastery(current_timestamp, floor=self.decay_floor, review_threshold=self.review_threshold)
        is_decayed_master = concept.is_mastered_certified and (decay_state.p_eff < self.review_threshold or decay_state.dt_days >= 14.0)

        # Posterior update
        if correct:
            post = (prior_p * (1.0 - s)) / ((prior_p * (1.0 - s)) + ((1.0 - prior_p) * g))
        else:
            post = (prior_p * s) / ((prior_p * s) + ((1.0 - prior_p) * (1.0 - g)))
            if is_decayed_master:
                post = prior_p - 0.5 * (prior_p - post)

        # Learning transition
        post = post + (1.0 - post) * self.T

        # Evidence-weighted adjustment
        new_p = prior_p + w * (post - prior_p)
        new_p = max(0.01, min(0.99, round(new_p, 4)))

        # Update low delta counter
        delta_p = abs(new_p - prior_p)
        if delta_p < 0.05:
            concept.consecutive_low_deltas += 1
        else:
            concept.consecutive_low_deltas = 0

        concept.p = new_p
        concept.evidence_sum = round(concept.evidence_sum + w, 4)
        concept.attempts_count += 1
        if correct:
            concept.correct_count += 1

        if correct and (is_transfer or difficulty >= 0.5) and (w >= 0.5):
            concept.has_transfer_success = True

        if is_decayed_master or is_review or concept.needs_review:
            if correct:
                concept.needs_review = False
                concept.stability_days = update_review_stability(concept.stability_days, is_correct=True)
            else:
                concept.needs_review = True
                concept.stability_days = update_review_stability(concept.stability_days, is_correct=False)

        concept.last_practiced_timestamp = current_timestamp

        updated_decay = concept.get_effective_mastery(current_timestamp, floor=self.decay_floor, review_threshold=self.review_threshold)
        status = concept.determine_status(updated_decay.p_eff)
        uncertainty_info = concept.compute_uncertainty()

        attempt_record = {
            'timestamp': current_timestamp,
            'correct': correct,
            'difficulty': difficulty,
            'is_transfer': is_transfer,
            'evidence_weight': w,
            'prior_p': prior_p,
            'new_p': new_p,
            'status': status,
            'telemetry': evidence_res.__dict__
        }
        concept.history.append(attempt_record)

        return AttemptResult(
            concept_id=concept.concept_id,
            is_correct=correct,
            difficulty=difficulty,
            is_transfer=is_transfer,
            evidence_weight=w,
            prior_p=prior_p,
            posterior_p=round(post, 4),
            new_p=new_p,
            evidence_sum=concept.evidence_sum,
            status=status,
            uncertainty_se=uncertainty_info['standard_error'],
            is_misconception=evidence_res.is_misconception,
            telemetry_details=attempt_record['telemetry']
        )


@dataclass
class LearnerState:
    student_id: str
    concepts: Dict[str, ConceptMastery] = field(default_factory=dict)
    active_concept_id: str = 'C1'
    virtual_clock: float = 0.0

    def get_or_create_concept(self, concept_id: str, default_p: float = 0.20) -> ConceptMastery:
        if concept_id not in self.concepts:
            self.concepts[concept_id] = ConceptMastery(
                concept_id=concept_id,
                p=default_p,
                last_practiced_timestamp=self.virtual_clock
            )
        return self.concepts[concept_id]

    def advance_virtual_clock_days(self, days: float) -> None:
        self.virtual_clock += max(0.0, days) * 86400.0


def update_bkt(
    p: float,
    is_correct: bool,
    difficulty: float = 0.5,
    w: float = 1.0,
    T: float = 0.15,
    slip_base: float = 0.10,
    slip_slope: float = 0.05,
    guess_base: float = 0.30,
    guess_slope: float = 0.15
) -> Tuple[float, float]:
    """
    Updates knowledge state p in [0.0, 1.0] using BKT with difficulty scaling and evidence dampening.
    """
    d = max(0.0, min(1.0, difficulty))
    s = slip_base + slip_slope * d
    g = guess_base - guess_slope * d

    s = max(0.01, min(0.49, s))
    g = max(0.01, min(0.49, g))

    if is_correct:
        numerator = p * (1.0 - s)
        denominator = numerator + (1.0 - p) * g
    else:
        numerator = p * s
        denominator = numerator + (1.0 - p) * (1.0 - g)

    posterior = numerator / denominator if denominator > 0 else p
    post_transition = posterior + (1.0 - posterior) * T
    p_new = p + w * (post_transition - p)
    p_new = max(0.0, min(1.0, p_new))
    uncertainty = p_new * (1.0 - p_new)

    return round(p_new, 4), round(uncertainty, 4)


def compute_uncertainty(p: Union[float, ConceptMastery], total_attempts: int = 1) -> float:
    """Computes Bernoulli variance sigma^2 = p * (1 - p) as an uncertainty index."""
    if isinstance(p, ConceptMastery):
        return p.compute_uncertainty()['standard_error']
    return round(float(p) * (1.0 - float(p)), 4)

