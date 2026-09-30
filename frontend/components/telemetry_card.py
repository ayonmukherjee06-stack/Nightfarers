"""MasteryFlow Response Feedback & Mastery Update Card (telemetry_card.py).

Apitex Edition: Provides clear, encouraging feedback after an exercise attempt, explaining
the solution and showing how the response influenced mastery metrics in warm porcelain style.
"""

from typing import Any, Dict
import streamlit as st


def render_telemetry_breakdown(attempt_result: Dict[str, Any], question: Dict[str, Any]):
    """Renders the attempt feedback and mastery update details in Apitex warm porcelain design."""
    is_correct = attempt_result.get("is_correct", False)
    w = float(attempt_result.get("evidence_weight", 1.0))
    is_misconception = attempt_result.get("is_misconception", False)
    new_p = float(attempt_result.get("new_p", 0.5))
    p_eff = float(attempt_result.get("p_eff", 0.5))
    time_ms = int(attempt_result.get("time_ms", 5000))
    hints_used = int(attempt_result.get("hints_used", 0))
    retry_gap = attempt_result.get("retry_gap_seconds")
    explanation = question.get("explanation", "")
    correct_answer = question.get("correct_answer", "")

    status_color = "#059669" if is_correct else "#E11D48"
    status_bg = "#E8F7F0" if is_correct else "#FFE4E6"
    status_label = "Correct! Well done" if is_correct else "Not quite — let's review the solution"
    status_icon = "OK" if is_correct else "!"

    # Context tags
    tags = []
    if retry_gap is not None and retry_gap < 5.0 and not is_correct:
        tags.append("""
        <span style="background: #FFE4E6; color: #E11D48; border: 1px solid #FECDD3; padding: 3px 12px; border-radius: 9999px; font-size: 0.72rem; font-weight: 700;">
            Quick retry
        </span>
        """)
    if time_ms < 3000:
        tags.append("""
        <span style="background: #FEF3C7; color: #D97706; border: 1px solid #FDE68A; padding: 3px 12px; border-radius: 9999px; font-size: 0.72rem; font-weight: 700;">
            Rapid response
        </span>
        """)
    if hints_used > 0:
        tags.append(f"""
        <span style="background: #E0F2FE; color: #0284C7; border: 1px solid #BAE6FD; padding: 3px 12px; border-radius: 9999px; font-size: 0.72rem; font-weight: 700;">
            {hints_used} hint{'s' if hints_used > 1 else ''} used
        </span>
        """)
    if is_misconception:
        tags.append("""
        <span style="background: #FFE4E6; color: #E11D48; border: 1px solid #FECDD3; padding: 3px 12px; border-radius: 9999px; font-size: 0.72rem; font-weight: 700;">
            Common misconception addressed
        </span>
        """)

    tag_html = " ".join(tags)

    card_html = f"""
    <div style="
        background: #FFFFFF;
        border: 1px solid rgba(228, 221, 211, 0.9);
        border-left: 5px solid {status_color};
        border-radius: 22px;
        padding: 22px 26px;
        margin-top: 18px;
        margin-bottom: 22px;
        box-shadow: 0 10px 30px -4px rgba(60, 50, 30, 0.05), 0 2px 8px -1px rgba(60, 50, 30, 0.02);
    ">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="
                    width: 36px;
                    height: 36px;
                    border-radius: 50%;
                    background: {status_bg};
                    border: 1.5px solid {status_color};
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: {status_color};
                    font-weight: 800;
                    font-size: 0.85rem;
                ">
                    {status_icon}
                </div>
                <div>
                    <div style="font-size: 1.15rem; font-weight: 800; color: #11141D; letter-spacing: -0.015em;">
                        {status_label}
                    </div>
                    <div style="font-size: 0.75rem; color: #78716C; margin-top: 2px;">
                        Mastery status updated in your profile
                    </div>
                </div>
            </div>
            <div style="display: flex; gap: 6px; flex-wrap: wrap;">
                {tag_html}
            </div>
        </div>

        <div style="
            margin: 16px 0;
            font-size: 0.92rem;
            color: #11141D;
            line-height: 1.6;
            background: #FBF8F2;
            border: 1px solid #EAE2D5;
            padding: 14px 18px;
            border-radius: 14px;
        ">
            <div style="margin-bottom: 6px; display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
                <span style="color: #11141D; font-size: 0.84rem; font-weight: 700;">
                    Correct Answer:
                </span> 
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.95rem; color: #11141D; background: #EDE6DA; border: 1px solid #DCD3C5; padding: 2px 8px; border-radius: 6px; font-weight: 700;">
                    {correct_answer}
                </span>
            </div>
            <div>
                <span style="color: #4B5563;">{explanation}</span>
            </div>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 10px; margin-top: 14px; border-top: 1px solid rgba(228, 221, 211, 0.9); padding-top: 14px;">
            <div style="background: #F4EEE5; padding: 12px 14px; border-radius: 14px; border: 1px solid #E5DCD0;">
                <div style="font-size: 0.70rem; color: #78716C; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px;">Response Fidelity</div>
                <div style="font-size: 1.3rem; font-weight: 800; color: #11141D; margin-top: 2px;">{w:.2f}</div>
                <div style="font-size: 0.65rem; color: #78716C;">Evidence weight</div>
            </div>
            <div style="background: #F4EEE5; padding: 12px 14px; border-radius: 14px; border: 1px solid #E5DCD0;">
                <div style="font-size: 0.70rem; color: #78716C; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px;">Topic Mastery</div>
                <div style="font-size: 1.3rem; font-weight: 800; color: #059669; margin-top: 2px;">{int(round(new_p * 100))}%</div>
                <div style="font-size: 0.65rem; color: #78716C;">Updated confidence</div>
            </div>
            <div style="background: #F4EEE5; padding: 12px 14px; border-radius: 14px; border: 1px solid #E5DCD0;">
                <div style="font-size: 0.70rem; color: #78716C; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px;">Retention Level</div>
                <div style="font-size: 1.3rem; font-weight: 800; color: #7C3AED; margin-top: 2px;">{int(round(p_eff * 100))}%</div>
                <div style="font-size: 0.65rem; color: #78716C;">Long-term retention</div>
            </div>
            <div style="background: #F4EEE5; padding: 12px 14px; border-radius: 14px; border: 1px solid #E5DCD0;">
                <div style="font-size: 0.70rem; color: #78716C; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px;">Response Time</div>
                <div style="font-size: 1.3rem; font-weight: 800; color: #D97706; margin-top: 2px;">{time_ms / 1000.0:.1f}s</div>
                <div style="font-size: 0.65rem; color: #78716C;">Interaction latency</div>
            </div>
        </div>
    </div>
    """
    clean_html_str = "\n".join(l.strip() for l in card_html.splitlines() if l.strip())
    st.markdown(clean_html_str, unsafe_allow_html=True)


# Backward compatibility alias
render_telemetry_card = render_telemetry_breakdown

