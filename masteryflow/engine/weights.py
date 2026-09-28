"""
Multi-Signal Anti-Gaming Evidence Weight Telemetry (weights.py).
Author: Yash (ML Lead) & Soham Choudhury (Frontend Co-Lead)
Calculates deterministic multiplicative evidence weight w in [0.0, 1.0] across behavioral signals.
Supports both object-oriented TelemetrySignal and functional calling conventions.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, Tuple, Union


@dataclass
class TelemetrySignal:
    hints_used: int = 0
    attempt_no: int = 1
    retry_gap_seconds: float = 999.0
    prev_correct: bool = True
    time_ms: int = 10000
    min_time_ms: int = 3000
    confidence: str = 'medium'  # 'low', 'medium', 'high'
    correct: bool = True


@dataclass
class EvidenceWeightResult:
    weight: float
    is_rapid_guess: bool = False
    is_brute_force_retry: bool = False
    is_lucky_guess: bool = False
    is_misconception: bool = False
    penalty_breakdown: Dict[str, float] = field(default_factory=dict)

    def __iter__(self):
        yield self.weight
        yield self.is_misconception

    def __getitem__(self, idx: int):
        return (self.weight, self.is_misconception)[idx]


def compute_evidence_weight(
    telemetry_or_hints: Union[TelemetrySignal, int] = 0,
    attempt_no: int = 1,
    time_ms: Optional[int] = None,
    retry_gap_seconds: Optional[float] = None,
    prev_correct: Optional[bool] = None,
    confidence: Optional[str] = None,
    is_correct: bool = True,
    min_time_ms: int = 3000,
    **kwargs: Any
) -> EvidenceWeightResult:
    """
    Computes evidence weight w in [0.0, 1.0] and multi-signal behavioral flags.
    
    Accepts either:
    1. A single TelemetrySignal object: compute_evidence_weight(telemetry)
    2. Discrete keyword/positional parameters: compute_evidence_weight(hints_used=1, attempt_no=2, ...)
    """
    if isinstance(telemetry_or_hints, TelemetrySignal):
        t = telemetry_or_hints
        hints_used = t.hints_used
        attempt_no = t.attempt_no
        retry_gap_seconds = t.retry_gap_seconds
        prev_correct = t.prev_correct
        time_ms = t.time_ms
        min_time_ms = t.min_time_ms
        confidence = t.confidence
        is_correct = t.correct
    else:
        hints_used = int(telemetry_or_hints)

    w = 1.0
    penalties: Dict[str, float] = {}

    # Halves evidence for each hint consulted: w *= (0.5 ** hints_used)
    if hints_used > 0:
        hint_factor = 0.5 ** hints_used
        w *= hint_factor
        penalties['hints'] = round(hint_factor, 4)

    # Retries yield significantly diminished diagnostic value
    if attempt_no > 1:
        w *= 0.3
        penalties['retry_diminish'] = 0.3

    # Immediate brute-force retry receives ZERO evidence weight
    is_brute_force = False
    if retry_gap_seconds is not None and retry_gap_seconds < 5.0 and prev_correct is False:
        w = 0.0
        is_brute_force = True
        penalties['rapid_retry_zeroed'] = 0.0

    # Rapid click-through (<3s) discounted as mindless guess
    is_rapid = False
    if time_ms is not None and time_ms < min_time_ms:
        w *= 0.2
        is_rapid = True
        penalties['rapid_latency'] = 0.2

    conf_norm = (confidence or "medium").strip().lower()
    # Lucky guess discount: student was guessing but happened to be right
    is_lucky = False
    if is_correct and conf_norm == "low":
        w *= 0.7
        is_lucky = True
        penalties['lucky_guess'] = 0.7

    # Misconception signal: wrong answer with high confidence
    is_misconception = False
    if (not is_correct) and conf_norm == "high":
        w = min(1.0, w * 1.2)
        is_misconception = True
        penalties['misconception_boost'] = 1.2

    w = max(0.0, min(1.0, round(w, 4)))

    return EvidenceWeightResult(
        weight=w,
        is_rapid_guess=is_rapid,
        is_brute_force_retry=is_brute_force,
        is_lucky_guess=is_lucky,
        is_misconception=is_misconception,
        penalty_breakdown=penalties
    )

