"""
Longitudinal Decay & Spaced Review (decay.py).
Owner: Yash (ML Model & Knowledge Tracing Lead)
Evaluates read-time Ebbinghaus exponential forgetting curve and manages spaced retrieval stability.
"""

import math
from dataclasses import dataclass


@dataclass
class DecayState:
    p_eff: float
    dt_days: float
    current_stability: float
    is_review_due: bool
    is_resilient_decay: bool

    def __float__(self) -> float:
        return float(self.p_eff)


def compute_effective_mastery(
    p: float,
    dt_days: float,
    stability_days: float = 7.0,
    floor: float = 0.25
) -> float:
    """
    Computes effective retention p_eff after dt_days of inactivity using Ebbinghaus decay.
    
    Psychometric Rationale:
    1. Knowledge decays asymptotically toward an asymptotic baseline floor (0.25) rather than zero.
    2. Stability S acts as memory half-life parameter, scaling retention duration across reviews.
    """
    if dt_days <= 0.0:
        return round(p, 4)

    s = max(0.1, stability_days)
    decay_factor = math.exp(-dt_days / s)
    p_eff = floor + (p - floor) * decay_factor
    p_eff = max(floor, min(p, p_eff))
    return round(p_eff, 4)


def compute_decayed_mastery(
    p: float,
    dt_days: float,
    stability: float = 7.0,
    floor: float = 0.25,
    was_mastered: bool = False,
    review_threshold: float = 0.60
) -> DecayState:
    """
    Computes effective mastery p_eff using Ebbinghaus exponential forgetting curve evaluated at read time.
    """
    if dt_days <= 0.0:
        p_eff = p
    else:
        decay_factor = math.exp(-max(0.0, dt_days) / max(0.1, stability))
        p_eff = floor + (p - floor) * decay_factor

    p_eff = max(0.0, min(1.0, round(p_eff, 4)))
    is_review_due = was_mastered and (p_eff < review_threshold)
    is_resilient = was_mastered and (dt_days >= 14.0)

    return DecayState(
        p_eff=p_eff,
        dt_days=dt_days,
        current_stability=stability,
        is_review_due=is_review_due,
        is_resilient_decay=is_resilient
    )


def update_stability(
    current_stability: float,
    is_correct: bool,
    is_review_attempt: bool = True,
    multiplier: float = 1.8
) -> float:
    """
    Expands memory stability parameter S when a spaced review is successfully passed.
    """
    if is_correct and is_review_attempt:
        return round(current_stability * multiplier, 2)
    elif not is_correct and is_review_attempt:
        # Long gap failure: resilience preservation (doesn't wipe out stability entirely)
        return round(max(3.0, current_stability * 0.75), 2)
    return round(current_stability, 2)


def update_review_stability(
    current_stability: float,
    is_correct: bool,
    expansion_factor: float = 1.8,
    contraction_factor: float = 0.6
) -> float:
    """
    Updates stability S based on review outcome: expands on retrieval success, contracts on failure.
    """
    if is_correct:
        new_s = current_stability * expansion_factor
    else:
        new_s = max(2.0, current_stability * contraction_factor)
    return round(new_s, 2)

