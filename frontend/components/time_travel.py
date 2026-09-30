"""MasteryFlow Virtual Clock Time Travel Component.

Role: Simulates passage of time (1 to 30 days) to demonstrate exponential Ebbinghaus
memory forgetting and live triggering of Rule 3 (Spaced Retrieval Review).

JUDGING INVARIANT:
- Ebbinghaus exponential decay formula with floor retention asymptote.
"""

from __future__ import annotations
import math
from typing import Dict, Any, Tuple
import streamlit as st


def apply_time_travel_decay(
    p_eff: float,
    days: int,
    decay_rate: float = 0.035,
    retention_floor: float = 0.20,
) -> float:
    """Computes decayed effective mastery belief after N days of inactivity.

    Formula:
        p(t) = p_floor + (p_0 - p_floor) * exp(-lambda * t)
    Parameters:
        p_0: Initial mastery belief before elapsed time
        t: Days of inactivity
        lambda: Concept-specific memory decay rate (default 0.035/day)
        p_floor: Minimum asymptotic retention floor (0.20 = 20%)
    Rationale:
        Human memory follows an exponential decay curve. Without retrieval practice,
        a concept mastered at 90% drops below the 60% review threshold after ~15-21 days.
    """
    if days <= 0:
        return p_eff

    decayed = retention_floor + (p_eff - retention_floor) * math.exp(-decay_rate * days)
    return round(max(min(decayed, 1.0), retention_floor), 4)


def render_time_travel_slider(default_days: int = 0) -> int:
    """Renders the interactive virtual clock slider in Streamlit."""
    st.markdown("#### Virtual Clock Controller (Live Ebbinghaus Time Travel)")
    st.caption("Advance time by N days to simulate realistic human memory forgetting and observe Rule 3 (Spaced Review) activate live.")

    days = st.slider(
        "Advance Virtual Clock (Days):",
        min_value=0,
        max_value=30,
        value=default_days,
        step=1,
        help="Simulates elapsed days without student practicing foundational concepts.",
    )

    if days > 0:
        pct_decay_preview = math.exp(-0.035 * days) * 100.0
        st.info(f"Clock advanced by **{days} days**. Theoretical memory retention factor: **{pct_decay_preview:.1f}%** of peak strength.")
    else:
        st.success("Clock is at Current Time (Day 0: No Memory Decay).")

    return days
