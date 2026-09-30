"""MasteryFlow Fraction & Ratio Question Runner.

Apitex Edition: Clean, distraction-free mathematical problem player with progressive hints,
quick fraction input helpers, and confidence calibration in refined warm porcelain style.
"""

import time
from typing import Any, Callable, Dict, List, Optional
import streamlit as st
from .math_parser import evaluate_student_answer, parse_fraction_input

try:
    from frontend.components.theme import render_html
except ImportError:
    from .theme import render_html


def render_question_runner(
    question: Dict[str, Any],
    on_submit_attempt: Callable[[Dict[str, Any]], None],
    current_streak: int = 0
):
    """Renders the question player, confidence selector, progressive hints, and submission controls in Apitex Edition."""
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
    quick_input_key = f"input_{qid}"
    if quick_input_key not in st.session_state:
        st.session_state[quick_input_key] = ""

    type_color = "#059669" if qtype in ["EASY", "LOW"] else ("#0284C7" if qtype in ["MEDIUM", "MED"] else "#E11D48")
    type_bg = "#E8F7F0" if qtype in ["EASY", "LOW"] else ("#E0F2FE" if qtype in ["MEDIUM", "MED"] else "#FFE4E6")
    diff_bar_pct = int(min(100, max(15, diff * 100)))

    streak_badge = f"""
    <div style="
        background: #FEF3C7;
        color: #D97706;
        border: 1px solid #FDE68A;
        padding: 4px 12px;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.78rem;
        display: inline-flex;
        align-items: center;
        gap: 5px;
    ">
         {current_streak} streak
    </div>
    """ if current_streak > 0 else ""

    transfer_badge = f"""
    <span style="
        background: #EDE9FE;
        color: #7C3AED;
        border: 1px solid #DDD6FE;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 3px 10px;
        border-radius: 9999px;
    ">
        Mastery Check
    </span>
    """ if is_transfer else ""

    options = question.get("options") or []
    if options:
        format_bar = '<span style="font-weight: 600; color: #4B5563;">Question Type:</span> <span style="color: #11141D; font-weight: 700;">Multiple Choice</span> &middot; Select the best answer option.'
    else:
        format_bar = """
        <span style="font-weight: 600; color: #4B5563;">Accepted formats:</span>
        <code style="color: #11141D; background: #F4EEE5; border: 1px solid #E5DCD0; padding: 2px 7px; border-radius: 6px;">3/4</code>
        <code style="color: #11141D; background: #F4EEE5; border: 1px solid #E5DCD0; padding: 2px 7px; border-radius: 6px;">1 1/2</code>
        <code style="color: #11141D; background: #F4EEE5; border: 1px solid #E5DCD0; padding: 2px 7px; border-radius: 6px;">0.75</code>
        <code style="color: #11141D; background: #F4EEE5; border: 1px solid #E5DCD0; padding: 2px 7px; border-radius: 6px;">5</code>
        """

    # Apitex Question Header & Prompt Card
    render_html(f"""
    <div style="
        background: #FFFFFF;
        border: 1px solid rgba(228, 221, 211, 0.9);
        border-radius: 22px;
        padding: 24px 28px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px -4px rgba(60, 50, 30, 0.05), 0 2px 8px -1px rgba(60, 50, 30, 0.02);
    ">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; flex-wrap: wrap; gap: 8px;">
            <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
                <span style="
                    font-family: 'JetBrains Mono', monospace;
                    font-size: 0.80rem;
                    color: #11141D;
                    font-weight: 700;
                    background: #F4EEE5;
                    border: 1px solid #E5DCD0;
                    padding: 3px 8px;
                    border-radius: 6px;
                ">
                    {qid}
                </span>
                <span style="
                    background: {type_bg};
                    color: {type_color};
                    border: 1px solid {type_color}30;
                    font-size: 0.72rem;
                    font-weight: 700;
                    padding: 3px 10px;
                    border-radius: 9999px;
                    text-transform: uppercase;
                ">
                    {qtype}
                </span>
                {transfer_badge}
                <div style="display: inline-flex; align-items: center; gap: 6px; font-size: 0.74rem; color: #78716C;">
                    <span>Difficulty:</span>
                    <strong style="color: #11141D;">{diff:.2f}</strong>
                    <div style="width: 44px; height: 6px; background: #EDE6DA; border-radius: 999px; overflow: hidden; display: inline-block;">
                        <div style="width: {diff_bar_pct}%; height: 100%; background: {type_color}; border-radius: 999px;"></div>
                    </div>
                </div>
            </div>
            <div>
                {streak_badge}
            </div>
        </div>

        <div style="
            font-size: 1.25rem;
            font-weight: 700;
            color: #11141D;
            line-height: 1.6;
            letter-spacing: -0.015em;
            padding: 6px 0 12px 0;
        ">
            {prompt}
        </div>
        
        <div style="
            display: flex;
            gap: 8px;
            margin-top: 12px;
            padding-top: 12px;
            border-top: 1px solid rgba(228, 221, 211, 0.9);
            font-size: 0.74rem;
            color: #78716C;
            flex-wrap: wrap;
            align-items: center;
        ">
            {format_bar}
        </div>
    </div>
    """)

    # Interactive Progressive Hint Drawer
    num_hints_revealed = st.session_state[hint_key]
    with st.expander(f"Need a hint? ({num_hints_revealed}/{len(hints)} revealed)", expanded=(num_hints_revealed > 0)):
        render_html(
            "<div style='background: #FFFBEB; border: 1px solid #FDE68A; border-radius: 12px; padding: 10px 14px; margin-bottom: 10px;'>"
            "<p style='font-size: 0.82rem; color: #92400E; margin: 0; line-height: 1.4;'>"
            "Hints guide you step-by-step. Try applying each clue before requesting another."
            "</p></div>"
        )
        for h_idx in range(num_hints_revealed):
            st.info(f"Hint {h_idx + 1}: {hints[h_idx]}")

        if num_hints_revealed < len(hints):
            if st.button(f"Reveal Next Hint ({num_hints_revealed + 1}/{len(hints)})", key=f"btn_hint_{qid}"):
                st.session_state[hint_key] += 1
                st.rerun()


    # Clean Submission Form
    with st.form(key=f"form_question_{qid}"):
        if options:
            selected_mcq = st.radio(
                "Choose the correct option:",
                options=options,
                key=f"mcq_radio_{qid}",
                index=None
            )
            user_input = selected_mcq or ""
            col_blank, col_conf = st.columns([3, 2])
            with col_conf:
                confidence = st.selectbox(
                    "How confident are you?",
                    options=[
                        "High — I'm confident in this answer",
                        "Medium — Pretty sure, checking my work",
                        "Low — Making an educated guess"
                    ],
                    index=0,
                    key=f"conf_{qid}",
                    help="Helps the learning system tailor the pace of subsequent practice."
                )
        else:
            col_ans, col_conf = st.columns([3, 2])

            with col_ans:
                user_input = st.text_input(
                    "Your Answer:",
                    value=st.session_state.get(quick_input_key, ""),
                    placeholder="Type your answer (e.g. 3/4, 1 1/2, 0.5)...",
                    key=f"field_input_{qid}"
                )

            with col_conf:
                confidence = st.selectbox(
                    "How confident are you?",
                    options=[
                        "High — I'm confident in this answer",
                        "Medium — Pretty sure, checking my work",
                        "Low — Making an educated guess"
                    ],
                    index=0,
                    key=f"conf_{qid}",
                    help="Helps the learning system tailor the pace of subsequent practice."
                )

        submit_btn = st.form_submit_button("Submit Answer", use_container_width=True)

    if submit_btn:
        actual_input = user_input.strip() if isinstance(user_input, str) else str(user_input or "")
        if not actual_input:
            st.warning("Please select or enter your answer before submitting.")
            return

        now = time.time()
        start_time = st.session_state.get(start_time_key, now - 10.0)
        time_ms = int(max(500, (now - start_time) * 1000))

        last_sub_time = st.session_state.get(last_sub_key)
        retry_gap_sec = round(now - last_sub_time, 2) if last_sub_time else None
        st.session_state[last_sub_key] = now

        is_correct, parsed_val, err_msg = evaluate_student_answer(actual_input, correct_ans, options=options)

        if err_msg:
            st.error(f"Format Notice: {err_msg}")
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
