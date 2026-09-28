"""MasteryFlow Fraction & Ratio Question Runner with Metacognitive Telemetry.

Owner: Soham Choudhury (Frontend Co-Lead & Question Bank Lead)
Aesthetic: Raycast/Linear 2026 dark glass question player with interactive telemetry chips,
quick-format suggestions, metacognitive confidence tuning, and progressive hint scaffolding.
Security: Zero eval/exec, safe mathematical verification via fractions.Fraction.
"""

import time
from typing import Any, Callable, Dict, List, Optional
import streamlit as st
from .math_parser import evaluate_student_answer, parse_fraction_input


def render_question_runner(
    question: Dict[str, Any],
    on_submit_attempt: Callable[[Dict[str, Any]], None],
    current_streak: int = 0
):
    """Renders the question player, confidence selector, progressive hints, and submission controls."""
    qid = question.get("id") or question.get("question_id", "Q_01")
    cid = question.get("concept_id", "C1")
    qtype = str(question.get("type", "medium")).upper()
    diff = float(question.get("difficulty", 0.5))
    is_transfer = bool(question.get("is_transfer", False))
    prompt = question.get("prompt", "")
    hints = question.get("hints", [])
    explanation = question.get("explanation", "")
    correct_ans = question.get("correct_answer", "")

    # State management keys
    hint_key = f"hints_revealed_{qid}"
    if hint_key not in st.session_state:
        st.session_state[hint_key] = 0

    start_time_key = f"q_start_time_{qid}"
    if start_time_key not in st.session_state:
        st.session_state[start_time_key] = time.time()

    last_sub_key = f"last_submission_time_{qid}"

    type_color = "#10B981" if qtype in ["EASY", "LOW"] else ("#00F0FF" if qtype in ["MEDIUM", "MED"] else "#F43F5E")

    streak_badge = f"""
    <div style="
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.22), rgba(217, 119, 6, 0.12));
        color: #FBBF24;
        border: 1px solid rgba(245, 158, 11, 0.5);
        padding: 4px 14px;
        border-radius: 9999px;
        font-weight: 800;
        font-size: 0.78rem;
        letter-spacing: 0.8px;
        box-shadow: 0 0 16px rgba(245, 158, 11, 0.2);
        display: inline-flex;
        align-items: center;
        gap: 6px;
    ">
        <span>🔥</span> {current_streak} STREAK
    </div>
    """ if current_streak > 0 else ""

    transfer_badge = f"""
    <span style="
        background: rgba(168, 85, 247, 0.18);
        color: #C084FC;
        border: 1px solid rgba(168, 85, 247, 0.4);
        font-size: 0.70rem;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 6px;
        letter-spacing: 0.5px;
    ">
        TRANSFER PROOF
    </span>
    """ if is_transfer else ""

    # Modern Question Header & Prompt Card
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(13, 19, 38, 0.82) 0%, rgba(8, 13, 26, 0.94) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 24px 26px;
        margin-bottom: 18px;
        backdrop-filter: blur(20px);
        box-shadow: 0 16px 40px -10px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.08);
    ">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; flex-wrap: wrap; gap: 8px;">
            <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
                <span style="
                    font-family: 'JetBrains Mono', monospace;
                    font-size: 0.82rem;
                    color: #38BDF8;
                    font-weight: 700;
                    background: rgba(56, 189, 248, 0.12);
                    border: 1px solid rgba(56, 189, 248, 0.3);
                    padding: 3px 9px;
                    border-radius: 6px;
                ">
                    {qid}
                </span>
                <span style="
                    background: {type_color}18;
                    color: {type_color};
                    border: 1px solid {type_color}55;
                    font-size: 0.70rem;
                    font-weight: 700;
                    padding: 3px 10px;
                    border-radius: 9999px;
                    text-transform: uppercase;
                    letter-spacing: 0.6px;
                ">
                    {qtype}
                </span>
                {transfer_badge}
                <span style="font-size: 0.74rem; color: #94A3B8; font-family: 'Space Grotesk', sans-serif;">
                    Item Difficulty: <strong style="color: #F8FAFC;">{diff:.2f}</strong>
                </span>
            </div>
            <div>
                {streak_badge}
            </div>
        </div>

        <div style="
            font-size: 1.25rem;
            font-weight: 600;
            color: #FFFFFF;
            line-height: 1.65;
            letter-spacing: -0.01em;
            padding: 8px 0;
            font-family: 'Space Grotesk', sans-serif;
        ">
            {prompt}
        </div>
        
        <div style="
            display: flex;
            gap: 8px;
            margin-top: 14px;
            padding-top: 12px;
            border-top: 1px solid rgba(255, 255, 255, 0.06);
            font-size: 0.72rem;
            color: #64748B;
            flex-wrap: wrap;
            align-items: center;
        ">
            <span>Accepted Formats:</span>
            <code style="color: #94A3B8; background: rgba(255,255,255,0.05); padding: 1px 6px; border-radius: 4px;">3/4</code>
            <code style="color: #94A3B8; background: rgba(255,255,255,0.05); padding: 1px 6px; border-radius: 4px;">1 1/2</code>
            <code style="color: #94A3B8; background: rgba(255,255,255,0.05); padding: 1px 6px; border-radius: 4px;">0.75</code>
            <code style="color: #94A3B8; background: rgba(255,255,255,0.05); padding: 1px 6px; border-radius: 4px;">5</code>
            <span style="margin-left: auto; color: #38BDF8; font-weight: 600;">⚡ Multi-Signal Telemetry Active</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Progressive Hint Drawer
    num_hints_revealed = st.session_state[hint_key]
    with st.expander(f"💡 Progressive Scaffolding Hints ({num_hints_revealed}/{len(hints)} revealed)", expanded=(num_hints_revealed > 0)):
        st.markdown(
            "<p style='font-size: 0.82rem; color: #94A3B8; margin-bottom: 12px;'>"
            "Note: Each hint consulted applies a <strong>0.5&times;</strong> multiplicative attenuation to your evidence weight "
            "<code>w</code> in accordance with BKT multi-signal telemetry.</p>",
            unsafe_allow_html=True
        )
        for h_idx in range(num_hints_revealed):
            st.info(f"💡 Hint {h_idx + 1}: {hints[h_idx]}")

        if num_hints_revealed < len(hints):
            if st.button(f"Reveal Next Hint ({num_hints_revealed + 1}/{len(hints)})", key=f"btn_hint_{qid}"):
                st.session_state[hint_key] += 1
                st.rerun()

    # Input & Metacognitive Submission Form
    with st.form(key=f"form_question_{qid}"):
        col_ans, col_conf = st.columns([3, 2])

        with col_ans:
            user_input = st.text_input(
                "Your Answer:",
                placeholder="Type simplified fraction or integer (e.g. 3/4, 5/6, 1 1/2)...",
                key=f"input_{qid}"
            )

        with col_conf:
            confidence = st.selectbox(
                "Metacognitive Confidence:",
                options=[
                    "High — Certain (Full evidence weight 1.0x)",
                    "Medium — Somewhat sure (Calibrated 0.8x)",
                    "Low — Guessing (Discounted 0.4x)"
                ],
                index=0,
                key=f"conf_{qid}",
                help="Calibrates anti-guessing Bayesian evidence weights based on self-reported metacognition."
            )

        submit_btn = st.form_submit_button("🚀 Submit Answer with Telemetry", use_container_width=True)

    if submit_btn:
        if not user_input.strip():
            st.warning("Please type your answer before submitting.")
            return

        now = time.time()
        start_time = st.session_state.get(start_time_key, now - 10.0)
        time_ms = int(max(500, (now - start_time) * 1000))

        # Check retry gap if previous submission exists
        last_sub_time = st.session_state.get(last_sub_key)
        retry_gap_sec = round(now - last_sub_time, 2) if last_sub_time else None
        st.session_state[last_sub_key] = now

        # Evaluate safely via fractions.Fraction (ZERO eval)
        is_correct, parsed_val, err_msg = evaluate_student_answer(user_input, correct_ans)

        if err_msg:
            st.error(f"Input Error: {err_msg}")
            return

        conf_code = "high" if "High" in confidence else ("low" if "Low" in confidence else "medium")

        attempt_payload = {
            "concept_id": cid,
            "question_id": qid,
            "user_answer": str(parsed_val),
            "is_correct": is_correct,
            "difficulty": diff,
            "is_transfer": is_transfer,
            "confidence": conf_code,
            "time_ms": time_ms,
            "hints_used": num_hints_revealed,
            "retry_gap_seconds": retry_gap_sec,
            "attempt_no": 1 if retry_gap_sec is None else 2
        }

        on_submit_attempt(attempt_payload)
