"""MasteryFlow Glass-Box 'Why This Next?' Explainability Card (glassbox_card.py).

Jointly authored by: Soham Choudhury (Frontend Co-Lead) & Ayon Mukherjee (Lead & Orchestrator)
Role: Dual-perspective transparent explainability card displaying deterministic decision reasoning
with Linear / Raycast 2026 dark glass aesthetic, live mathematical telemetry, and prerequisite dependency badges.
"""

from typing import Any, Dict, Optional, Union
import streamlit as st


ACTION_THEMES = {
    "Practice": {
        "badge_color": "#00F0FF",
        "bg_glow": "rgba(0, 240, 255, 0.12)",
        "gradient": "linear-gradient(135deg, rgba(0, 240, 255, 0.16) 0%, rgba(14, 165, 233, 0.08) 100%)",
        "icon": "🎯",
        "rule_name": "Rule 4: Active Concept Mastery & Transfer Validation",
        "action_title": "Targeted Skill Reinforcement"
    },
    "PRACTICE": {
        "badge_color": "#00F0FF",
        "bg_glow": "rgba(0, 240, 255, 0.12)",
        "gradient": "linear-gradient(135deg, rgba(0, 240, 255, 0.16) 0%, rgba(14, 165, 233, 0.08) 100%)",
        "icon": "🎯",
        "rule_name": "Rule 4: Active Concept Mastery & Transfer Validation",
        "action_title": "Targeted Skill Reinforcement"
    },
    "Remediate": {
        "badge_color": "#F43F5E",
        "bg_glow": "rgba(244, 63, 94, 0.15)",
        "gradient": "linear-gradient(135deg, rgba(244, 63, 94, 0.18) 0%, rgba(225, 29, 72, 0.08) 100%)",
        "icon": "🩹",
        "rule_name": "Rule 2: Prerequisite Inconsistency & Ceiling Capping",
        "action_title": "Foundational Prerequisite Repair"
    },
    "REMEDIATE_PREREQUISITE": {
        "badge_color": "#F43F5E",
        "bg_glow": "rgba(244, 63, 94, 0.15)",
        "gradient": "linear-gradient(135deg, rgba(244, 63, 94, 0.18) 0%, rgba(225, 29, 72, 0.08) 100%)",
        "icon": "🩹",
        "rule_name": "Rule 2: Prerequisite Inconsistency & Ceiling Capping",
        "action_title": "Foundational Prerequisite Repair"
    },
    "Review": {
        "badge_color": "#A855F7",
        "bg_glow": "rgba(168, 85, 247, 0.15)",
        "gradient": "linear-gradient(135deg, rgba(168, 85, 247, 0.18) 0%, rgba(147, 51, 234, 0.08) 100%)",
        "icon": "⏳",
        "rule_name": "Rule 3: Longitudinal Ebbinghaus Spaced Review",
        "action_title": "Spaced Retention Calibration"
    },
    "REVIEW": {
        "badge_color": "#A855F7",
        "bg_glow": "rgba(168, 85, 247, 0.15)",
        "gradient": "linear-gradient(135deg, rgba(168, 85, 247, 0.18) 0%, rgba(147, 51, 234, 0.08) 100%)",
        "icon": "⏳",
        "rule_name": "Rule 3: Longitudinal Ebbinghaus Spaced Review",
        "action_title": "Spaced Retention Calibration"
    },
    "Advance": {
        "badge_color": "#10B981",
        "bg_glow": "rgba(16, 185, 129, 0.15)",
        "gradient": "linear-gradient(135deg, rgba(16, 185, 129, 0.18) 0%, rgba(5, 150, 105, 0.08) 100%)",
        "icon": "🚀",
        "rule_name": "Rule 5: Topological DAG Progress to Unlocked Concept",
        "action_title": "Curriculum Frontier Advancement"
    },
    "ADVANCE": {
        "badge_color": "#10B981",
        "bg_glow": "rgba(16, 185, 129, 0.15)",
        "gradient": "linear-gradient(135deg, rgba(16, 185, 129, 0.18) 0%, rgba(5, 150, 105, 0.08) 100%)",
        "icon": "🚀",
        "rule_name": "Rule 5: Topological DAG Progress to Unlocked Concept",
        "action_title": "Curriculum Frontier Advancement"
    },
    "Challenge": {
        "badge_color": "#F59E0B",
        "bg_glow": "rgba(245, 158, 11, 0.15)",
        "gradient": "linear-gradient(135deg, rgba(245, 158, 11, 0.18) 0%, rgba(217, 119, 6, 0.08) 100%)",
        "icon": "🏆",
        "rule_name": "Rule 6: Capstone Synthesis & Acceleration",
        "action_title": "Synthesis & Advanced Mastery Challenge"
    },
    "CHALLENGE": {
        "badge_color": "#F59E0B",
        "bg_glow": "rgba(245, 158, 11, 0.15)",
        "gradient": "linear-gradient(135deg, rgba(245, 158, 11, 0.18) 0%, rgba(217, 119, 6, 0.08) 100%)",
        "icon": "🏆",
        "rule_name": "Rule 6: Capstone Synthesis & Acceleration",
        "action_title": "Synthesis & Advanced Mastery Challenge"
    },
    "Escalate to Teacher": {
        "badge_color": "#EF4444",
        "bg_glow": "rgba(239, 68, 68, 0.2)",
        "gradient": "linear-gradient(135deg, rgba(239, 68, 68, 0.22) 0%, rgba(185, 28, 28, 0.08) 100%)",
        "icon": "🚨",
        "rule_name": "Rule 1: Teacher Escalation & 1-on-1 Coaching Queue",
        "action_title": "Human-in-the-Loop Teacher Escalation"
    },
    "TEACHER_INTERVENTION": {
        "badge_color": "#EF4444",
        "bg_glow": "rgba(239, 68, 68, 0.2)",
        "gradient": "linear-gradient(135deg, rgba(239, 68, 68, 0.22) 0%, rgba(185, 28, 28, 0.08) 100%)",
        "icon": "🚨",
        "rule_name": "Rule 1: Teacher Escalation & 1-on-1 Coaching Queue",
        "action_title": "Human-in-the-Loop Teacher Escalation"
    },
}


def render_glassbox_card(
    decision: Any,
    concept_meta: Optional[Dict[str, Any]] = None,
    concept_state: Optional[Dict[str, Any]] = None,
    graph: Optional[Any] = None,
    student_name: str = "Student",
) -> None:
    """Renders the Glass-Box explainability card supporting both student and teacher call styles."""
    # Extract action string
    if hasattr(decision, "action"):
        act_val = decision.action.value if hasattr(decision.action, "value") else str(decision.action)
    elif isinstance(decision, dict):
        act_val = decision.get("action", "Practice")
    else:
        act_val = str(decision)

    # Extract target concept
    if hasattr(decision, "target_concept_id") and decision.target_concept_id:
        target_cid = decision.target_concept_id
    elif hasattr(decision, "target_concept") and decision.target_concept:
        target_cid = decision.target_concept
    elif isinstance(decision, dict):
        target_cid = decision.get("target_concept", decision.get("target_concept_id", "C1"))
    else:
        target_cid = "C1"

    # Extract reason
    if hasattr(decision, "reason"):
        reason = decision.reason
    elif isinstance(decision, dict):
        reason = decision.get("reason", "Engaging standard practice on active concept.")
    else:
        reason = "Engaging standard practice."

    # Extract rule triggered
    if hasattr(decision, "rule_triggered") and decision.rule_triggered:
        rule_name = decision.rule_triggered
    else:
        theme_default = ACTION_THEMES.get(act_val, ACTION_THEMES["Practice"])
        rule_name = theme_default["rule_name"]

    theme = ACTION_THEMES.get(act_val, ACTION_THEMES["Practice"])

    # Resolve concept title and icon
    if concept_meta and isinstance(concept_meta, dict):
        cname = concept_meta.get("name", concept_meta.get("title", target_cid))
        cicon = concept_meta.get("icon", "📚")
    elif graph and hasattr(graph, "get_concept_title"):
        cname = graph.get_concept_title(target_cid)
        cicon = "📚"
    elif graph and hasattr(graph, "concepts_meta"):
        meta = graph.concepts_meta.get(target_cid, {})
        cname = meta.get("name", target_cid)
        cicon = meta.get("icon", "📚")
    else:
        cname = f"Concept {target_cid}"
        cicon = "📚"

    # Telemetry metrics
    cstate = concept_state or {}
    p_eff = cstate.get("p_eff", getattr(decision, "metadata", {}).get("p_eff", 0.50))
    is_fragile = cstate.get("is_fragile", getattr(decision, "metadata", {}).get("is_fragile", False))
    status = cstate.get("status", "practicing")

    fragile_html = """
    <span style="
        background: rgba(244, 63, 94, 0.18);
        color: #FB7185;
        border: 1px solid rgba(244, 63, 94, 0.45);
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 0.70rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        margin-left: 10px;
        display: inline-flex;
        align-items: center;
        gap: 4px;
    ">
        ⚠️ PREREQ CAP BINDING (FRAGILE)
    </span>
    """ if is_fragile else ""

    provisional_html = """
    <span style="
        background: rgba(245, 158, 11, 0.18);
        color: #FBBF24;
        border: 1px solid rgba(245, 158, 11, 0.45);
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 0.70rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        margin-left: 10px;
        display: inline-flex;
        align-items: center;
        gap: 4px;
    ">
        ⏳ PROVISIONAL (TRANSFER PENDING)
    </span>
    """ if (p_eff >= 0.85 and status == "provisional") else ""

    card_html = f"""
    <div style="
        background: linear-gradient(135deg, rgba(14, 20, 40, 0.85) 0%, rgba(8, 13, 26, 0.95) 100%);
        border: 1px solid {theme['badge_color']}44;
        box-shadow: 0 16px 40px -10px rgba(0, 0, 0, 0.65), inset 0 1px 0 rgba(255, 255, 255, 0.08), 0 0 24px -6px {theme['bg_glow']};
        border-radius: 18px;
        padding: 22px 26px;
        margin-bottom: 22px;
        backdrop-filter: blur(20px);
        font-family: 'Plus Jakarta Sans', sans-serif;
    ">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px;">
            <div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="
                        font-size: 0.70rem;
                        font-weight: 800;
                        letter-spacing: 1.5px;
                        text-transform: uppercase;
                        color: {theme['badge_color']};
                        font-family: 'Space Grotesk', sans-serif;
                    ">
                        {theme['icon']} ADAPTIVE ROUTING DECISION &middot; {student_name.upper()}
                    </span>
                </div>
                <div style="display: flex; align-items: center; flex-wrap: wrap; gap: 8px; margin-top: 6px;">
                    <h2 style="margin: 0; font-size: 1.5rem; color: #FFFFFF; font-weight: 800; font-family: 'Space Grotesk', sans-serif; letter-spacing: -0.5px;">
                        {cicon} {target_cid}: {cname}
                    </h2>
                    {fragile_html}
                    {provisional_html}
                </div>
            </div>
            
            <div style="
                background: {theme['gradient']};
                border: 1px solid {theme['badge_color']}66;
                color: {theme['badge_color']};
                font-family: 'Space Grotesk', sans-serif;
                font-size: 0.82rem;
                font-weight: 800;
                padding: 6px 16px;
                border-radius: 9999px;
                text-transform: uppercase;
                letter-spacing: 0.8px;
                box-shadow: 0 0 16px {theme['bg_glow']};
                display: flex;
                align-items: center;
                gap: 6px;
            ">
                <span>●</span> {act_val}
            </div>
        </div>

        <div style="
            background: rgba(6, 10, 22, 0.7);
            border-left: 4px solid {theme['badge_color']};
            border-radius: 0 12px 12px 0;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            border-right: 1px solid rgba(255, 255, 255, 0.05);
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            padding: 14px 18px;
            margin: 16px 0 14px 0;
        ">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px;">
                <span style="font-size: 0.70rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 1.2px; font-weight: 700; font-family: 'Space Grotesk', sans-serif;">
                    WHY THIS NEXT? (DETERMINISTIC COGNITIVE RATIONALE)
                </span>
                <span style="font-size: 0.70rem; color: #64748B; font-family: monospace;">
                    ZERO-HALLUCINATION PROOF
                </span>
            </div>
            <p style="margin: 0; font-size: 0.95rem; line-height: 1.55; color: #F1F5F9; font-weight: 450;">
                {reason}
            </p>
        </div>

        <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-top: 12px; font-size: 0.76rem;">
            <span style="background: rgba(15, 23, 42, 0.8); padding: 5px 12px; border-radius: 8px; border: 1px solid rgba(255, 255, 255, 0.08); color: #CBD5E1;">
                ⚖️ <strong style="color: #F8FAFC;">Engine Rule:</strong> {rule_name}
            </span>
            <span style="background: rgba(15, 23, 42, 0.8); padding: 5px 12px; border-radius: 8px; border: 1px solid rgba(255, 255, 255, 0.08); color: #CBD5E1;">
                🎯 <strong style="color: #F8FAFC;">Target Node:</strong> {target_cid}
            </span>
            <span style="background: rgba(15, 23, 42, 0.8); padding: 5px 12px; border-radius: 8px; border: 1px solid rgba(255, 255, 255, 0.08); color: #CBD5E1;">
                📊 <strong style="color: #F8FAFC;">Effective p_eff:</strong> {int(round(float(p_eff) * 100))}%
            </span>
            <span style="background: rgba(16, 185, 129, 0.12); padding: 5px 12px; border-radius: 8px; border: 1px solid rgba(16, 185, 129, 0.3); color: #34D399; font-weight: 600;">
                🔒 Pure Deterministic Invariant
            </span>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
