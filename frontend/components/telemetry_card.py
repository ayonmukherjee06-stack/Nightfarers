"""MasteryFlow Instant Telemetry & Multi-Signal Evidence Breakdown Card (telemetry_card.py).

Owner: Soham Choudhury (Frontend Co-Lead & Question Bank Lead)
Visualizes evidence weight w attenuation, BKT state shifts, and anti-gaming detections in real time
using modern 2026 Linear/Raycast dark glass aesthetics and telemetry HUD metrics.
"""

from typing import Any, Dict
import streamlit as st


def render_telemetry_breakdown(attempt_result: Dict[str, Any], question: Dict[str, Any]):
    """Renders the step-by-step telemetry and psychometric mathematics for judges and students."""
    is_correct = attempt_result.get("is_correct", False)
    w = attempt_result.get("evidence_weight", 1.0)
    is_misconception = attempt_result.get("is_misconception", False)
    new_p = attempt_result.get("new_p", 0.5)
    p_eff = attempt_result.get("p_eff", 0.5)
    time_ms = attempt_result.get("time_ms", 5000)
    hints_used = attempt_result.get("hints_used", 0)
    retry_gap = attempt_result.get("retry_gap_seconds")
    explanation = question.get("explanation", "")
    correct_answer = question.get("correct_answer", "")

    status_color = "#10B981" if is_correct else "#F43F5E"
    status_label = "CORRECT ANSWER" if is_correct else "INCORRECT ATTEMPT"
    status_icon = "✦" if is_correct else "✕"
    glow_color = "rgba(16, 185, 129, 0.15)" if is_correct else "rgba(244, 63, 94, 0.15)"

    # Anti-gaming tags
    tags = []
    if retry_gap is not None and retry_gap < 5.0 and not is_correct:
        tags.append("""
        <span style="background: rgba(244, 63, 94, 0.2); color: #FB7185; border: 1px solid rgba(244, 63, 94, 0.45); padding: 3px 10px; border-radius: 9999px; font-size: 0.72rem; font-weight: 700; letter-spacing: 0.5px;">
            ⚡ RAPID RETRY CLAMP (w = 0.0)
        </span>
        """)
    if time_ms < 3000:
        tags.append("""
        <span style="background: rgba(245, 158, 11, 0.2); color: #FBBF24; border: 1px solid rgba(245, 158, 11, 0.45); padding: 3px 10px; border-radius: 9999px; font-size: 0.72rem; font-weight: 700; letter-spacing: 0.5px;">
            ⏱️ SPEED ATTENUATION (0.2×)
        </span>
        """)
    if hints_used > 0:
        tags.append(f"""
        <span style="background: rgba(56, 189, 248, 0.2); color: #38BDF8; border: 1px solid rgba(56, 189, 248, 0.45); padding: 3px 10px; border-radius: 9999px; font-size: 0.72rem; font-weight: 700; letter-spacing: 0.5px;">
            💡 {hints_used} HINTS ACCESSED (0.5^{hints_used}×)
        </span>
        """)
    if is_misconception:
        tags.append("""
        <span style="background: rgba(225, 29, 72, 0.25); color: #FDA4AF; border: 1px solid rgba(225, 29, 72, 0.5); padding: 3px 10px; border-radius: 9999px; font-size: 0.72rem; font-weight: 700; letter-spacing: 0.5px;">
            🧠 MISCONCEPTION FLAGGED (1.2×)
        </span>
        """)

    tag_html = " ".join(tags)

    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(14, 20, 40, 0.90) 0%, rgba(8, 12, 26, 0.96) 100%);
        border: 1px solid {status_color}55;
        box-shadow: 0 16px 40px -10px rgba(0, 0, 0, 0.65), 0 0 24px -6px {glow_color}, inset 0 1px 0 rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 22px 26px;
        margin-top: 14px;
        margin-bottom: 22px;
        backdrop-filter: blur(20px);
        font-family: 'Plus Jakarta Sans', sans-serif;
    ">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="
                    width: 32px;
                    height: 32px;
                    border-radius: 50%;
                    background: {status_color}22;
                    border: 1px solid {status_color};
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: {status_color};
                    font-weight: 800;
                    font-size: 1.1rem;
                ">
                    {status_icon}
                </div>
                <div>
                    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.15rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.02em;">
                        {status_label}
                    </div>
                    <div style="font-size: 0.72rem; color: #94A3B8;">
                        Deterministic Multi-Signal Telemetry Recorded
                    </div>
                </div>
            </div>
            <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                {tag_html}
            </div>
        </div>

        <div style="
            margin: 16px 0;
            font-size: 0.92rem;
            color: #E2E8F0;
            line-height: 1.6;
            background: rgba(6, 10, 22, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-left: 4px solid {status_color};
            padding: 14px 18px;
            border-radius: 10px;
        ">
            <div style="margin-bottom: 6px;">
                <strong style="color: #38BDF8; font-family: 'Space Grotesk', sans-serif;">Correct Reference Answer:</strong> 
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 1.02rem; color: #FFFFFF; background: rgba(255,255,255,0.06); padding: 2px 8px; border-radius: 4px; font-weight: 700; margin-left: 6px;">
                    {correct_answer}
                </span>
            </div>
            <div>
                <strong style="color: #A78BFA; font-family: 'Space Grotesk', sans-serif;">Pedagogical Derivation:</strong> 
                <span style="color: #CBD5E1;">{explanation}</span>
            </div>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 12px; margin-top: 16px; border-top: 1px solid rgba(255, 255, 255, 0.06); padding-top: 16px;">
            <div style="background: rgba(13, 19, 38, 0.7); padding: 12px 14px; border-radius: 12px; border: 1px solid rgba(0, 240, 255, 0.2);">
                <div style="font-size: 0.68rem; color: #94A3B8; text-transform: uppercase; font-weight: 700; letter-spacing: 1px; font-family: 'Space Grotesk', sans-serif;">Evidence Weight w</div>
                <div style="font-size: 1.35rem; font-weight: 800; color: #00F0FF; font-family: 'JetBrains Mono', monospace; margin-top: 2px;">{w:.2f}</div>
            </div>
            <div style="background: rgba(13, 19, 38, 0.7); padding: 12px 14px; border-radius: 12px; border: 1px solid rgba(16, 185, 129, 0.2);">
                <div style="font-size: 0.68rem; color: #94A3B8; text-transform: uppercase; font-weight: 700; letter-spacing: 1px; font-family: 'Space Grotesk', sans-serif;">Updated Latent p</div>
                <div style="font-size: 1.35rem; font-weight: 800; color: #10B981; font-family: 'JetBrains Mono', monospace; margin-top: 2px;">{int(round(new_p * 100))}%</div>
            </div>
            <div style="background: rgba(13, 19, 38, 0.7); padding: 12px 14px; border-radius: 12px; border: 1px solid rgba(168, 85, 247, 0.2);">
                <div style="font-size: 0.68rem; color: #94A3B8; text-transform: uppercase; font-weight: 700; letter-spacing: 1px; font-family: 'Space Grotesk', sans-serif;">Effective Retention p_eff</div>
                <div style="font-size: 1.35rem; font-weight: 800; color: #A855F7; font-family: 'JetBrains Mono', monospace; margin-top: 2px;">{int(round(p_eff * 100))}%</div>
            </div>
            <div style="background: rgba(13, 19, 38, 0.7); padding: 12px 14px; border-radius: 12px; border: 1px solid rgba(245, 158, 11, 0.2);">
                <div style="font-size: 0.68rem; color: #94A3B8; text-transform: uppercase; font-weight: 700; letter-spacing: 1px; font-family: 'Space Grotesk', sans-serif;">Response Latency</div>
                <div style="font-size: 1.35rem; font-weight: 800; color: #F59E0B; font-family: 'JetBrains Mono', monospace; margin-top: 2px;">{round(time_ms/1000, 2)}s</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


render_telemetry_card = render_telemetry_breakdown
