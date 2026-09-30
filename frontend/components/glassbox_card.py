"""MasteryFlow Transparent Recommendation Card (glassbox_card.py).

Apitex Edition: Displays personalized learning recommendations and the pedagogical rationale
with warm porcelain white cards, deep obsidian badges, and refined low-saturation accents.
"""

from typing import Any, Dict, Optional, Union
import streamlit as st


ACTION_THEMES = {
    "Practice": {
        "badge_color": "#11141D",
        "bg_badge": "#F4EEE5",
        "border": "#E5DCD0",
        "icon": "",
        "rule_name": "Active Skill Practice & Consolidation",
        "action_title": "Targeted Practice"
    },
    "PRACTICE": {
        "badge_color": "#11141D",
        "bg_badge": "#F4EEE5",
        "border": "#E5DCD0",
        "icon": "",
        "rule_name": "Active Skill Practice & Consolidation",
        "action_title": "Targeted Practice"
    },
    "Remediate": {
        "badge_color": "#E11D48",
        "bg_badge": "#FFE4E6",
        "border": "#FECDD3",
        "icon": "",
        "rule_name": "Foundational Prerequisite Support",
        "action_title": "Prerequisite Review"
    },
    "REMEDIATE_PREREQUISITE": {
        "badge_color": "#E11D48",
        "bg_badge": "#FFE4E6",
        "border": "#FECDD3",
        "icon": "",
        "rule_name": "Foundational Prerequisite Support",
        "action_title": "Prerequisite Review"
    },
    "Review": {
        "badge_color": "#7C3AED",
        "bg_badge": "#EDE9FE",
        "border": "#DDD6FE",
        "icon": "",
        "rule_name": "Spaced Retention Check",
        "action_title": "Spaced Review"
    },
    "REVIEW": {
        "badge_color": "#7C3AED",
        "bg_badge": "#EDE9FE",
        "border": "#DDD6FE",
        "icon": "",
        "rule_name": "Spaced Retention Check",
        "action_title": "Spaced Review"
    },
    "Advance": {
        "badge_color": "#059669",
        "bg_badge": "#E8F7F0",
        "border": "#A7F3D0",
        "icon": "",
        "rule_name": "Next Curriculum Concept Progression",
        "action_title": "Advance to Next Topic"
    },
    "ADVANCE": {
        "badge_color": "#059669",
        "bg_badge": "#E8F7F0",
        "border": "#A7F3D0",
        "icon": "",
        "rule_name": "Next Curriculum Concept Progression",
        "action_title": "Advance to Next Topic"
    },
    "Challenge": {
        "badge_color": "#D97706",
        "bg_badge": "#FEF3C7",
        "border": "#FDE68A",
        "icon": "",
        "rule_name": "Capstone Synthesis & Deep Application",
        "action_title": "Challenge Problem"
    },
    "CHALLENGE": {
        "badge_color": "#D97706",
        "bg_badge": "#FEF3C7",
        "border": "#FDE68A",
        "icon": "",
        "rule_name": "Capstone Synthesis & Deep Application",
        "action_title": "Challenge Problem"
    },
    "Escalate to Teacher": {
        "badge_color": "#E11D48",
        "bg_badge": "#FFE4E6",
        "border": "#FECDD3",
        "icon": "",
        "rule_name": "Teacher Consultation Queue",
        "action_title": "Teacher Guidance"
    },
    "TEACHER_INTERVENTION": {
        "badge_color": "#E11D48",
        "bg_badge": "#FFE4E6",
        "border": "#FECDD3",
        "icon": "",
        "rule_name": "Teacher Consultation Queue",
        "action_title": "Teacher Guidance"
    },
}


def render_glassbox_card(
    decision: Any,
    concept_meta: Optional[Dict[str, Any]] = None,
    concept_state: Optional[Dict[str, Any]] = None,
    graph: Optional[Any] = None,
    student_name: str = "Student",
) -> None:
    """Renders the transparent learning path recommendation card in Apitex Edition design."""
    if hasattr(decision, "action"):
        act_val = decision.action.value if hasattr(decision.action, "value") else str(decision.action)
    elif isinstance(decision, dict):
        act_val = decision.get("action", "Practice")
    else:
        act_val = str(decision)

    if hasattr(decision, "target_concept_id") and decision.target_concept_id:
        target_cid = decision.target_concept_id
    elif hasattr(decision, "target_concept") and decision.target_concept:
        target_cid = decision.target_concept
    elif isinstance(decision, dict):
        target_cid = decision.get("target_concept", decision.get("target_concept_id", "C1"))
    else:
        target_cid = "C1"

    if hasattr(decision, "reason"):
        reason = decision.reason
    elif isinstance(decision, dict):
        reason = decision.get("reason", "Continuing focused practice on active concept.")
    else:
        reason = "Continuing focused practice on active concept."

    if hasattr(decision, "rule_triggered") and decision.rule_triggered:
        rule_name = decision.rule_triggered
    else:
        theme_default = ACTION_THEMES.get(act_val, ACTION_THEMES["Practice"])
        rule_name = theme_default["rule_name"]

    theme = ACTION_THEMES.get(act_val, ACTION_THEMES["Practice"])

    if concept_meta and isinstance(concept_meta, dict):
        cname = concept_meta.get("name", concept_meta.get("title", target_cid))
        cicon = concept_meta.get("icon", "")
    elif graph and hasattr(graph, "get_concept_title"):
        cname = graph.get_concept_title(target_cid)
        cicon = ""
    elif graph and hasattr(graph, "concepts_meta"):
        meta = graph.concepts_meta.get(target_cid, {})
        cname = meta.get("name", target_cid)
        cicon = meta.get("icon", "")
    else:
        cname = f"Concept {target_cid}"
        cicon = ""

    cstate = concept_state or {}
    p_eff = cstate.get("p_eff", getattr(decision, "metadata", {}).get("p_eff", 0.50))
    is_fragile = cstate.get("is_fragile", getattr(decision, "metadata", {}).get("is_fragile", False))
    status = cstate.get("status", "practicing")

    fragile_html = """
    <span style="
        background: #FFE4E6;
        color: #E11D48;
        border: 1px solid #FECDD3;
        padding: 3px 12px;
        border-radius: 9999px;
        font-size: 0.72rem;
        font-weight: 700;
        display: inline-flex;
        align-items: center;
        gap: 4px;
    ">
        Prerequisite gap detected
    </span>
    """ if is_fragile else ""

    provisional_html = """
    <span style="
        background: #FEF3C7;
        color: #D97706;
        border: 1px solid #FDE68A;
        padding: 3px 12px;
        border-radius: 9999px;
        font-size: 0.72rem;
        font-weight: 700;
        display: inline-flex;
        align-items: center;
        gap: 4px;
    ">
        Transfer check pending
    </span>
    """ if (float(p_eff) >= 0.85 and status == "provisional") else ""

    card_html = f"""
    <div style="
        background: #FFFFFF;
        border: 1px solid rgba(228, 221, 211, 0.9);
        border-left: 5px solid {theme['badge_color']};
        border-radius: 22px;
        padding: 22px 26px;
        margin-bottom: 22px;
        box-shadow: 0 10px 30px -4px rgba(60, 50, 30, 0.05), 0 2px 8px -1px rgba(60, 50, 30, 0.02);
    ">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px;">
            <div>
                <div style="display: flex; align-items: center; gap: 6px;">
                    <span style="
                        font-size: 0.72rem;
                        font-weight: 700;
                        letter-spacing: 0.6px;
                        text-transform: uppercase;
                        color: #78716C;
                    ">
                        Recommended Next Step &middot; {student_name}
                    </span>
                </div>
                <div style="display: flex; align-items: center; flex-wrap: wrap; gap: 10px; margin-top: 6px;">
                    <h2 style="margin: 0; font-size: 1.35rem; color: #11141D; font-weight: 800; letter-spacing: -0.02em;">
                        {target_cid}: {cname}
                    </h2>
                    {fragile_html}
                    {provisional_html}
                </div>
            </div>
            
            <div style="
                background: {theme['bg_badge']};
                border: 1px solid {theme['border']};
                color: {theme['badge_color']};
                font-size: 0.84rem;
                font-weight: 700;
                padding: 6px 16px;
                border-radius: 9999px;
                display: flex;
                align-items: center;
                gap: 6px;
                box-shadow: 0 2px 8px -2px rgba(60, 50, 30, 0.04);
            ">
                <span>{theme['action_title']}</span>
            </div>
        </div>

        <!-- Apitex Decision Rationale Box -->
        <div style="
            background: #FBF8F2;
            border: 1px solid #EAE2D5;
            border-radius: 14px;
            padding: 14px 18px;
            margin: 16px 0;
            box-shadow: inset 0 1px 3px rgba(60, 50, 30, 0.02);
        ">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 5px;">
                <span style="font-size: 0.72rem; color: #78716C; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 700;">
                    Pedagogical Rationale
                </span>
                <span style="font-size: 0.70rem; color: #11141D; font-weight: 700; letter-spacing: 0.3px;">
                    Deterministic Rule Execution
                </span>
            </div>
            <p style="margin: 0; font-size: 0.94rem; line-height: 1.55; color: #11141D;">
                {reason}
            </p>
        </div>

        <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-top: 12px; font-size: 0.76rem;">
            <span style="background: #F4EEE5; padding: 5px 12px; border-radius: 9999px; border: 1px solid #E5DCD0; color: #4B5563;">
                Topic: <strong style="color: #11141D;">{target_cid}</strong>
            </span>
            <span style="background: #F4EEE5; padding: 5px 12px; border-radius: 9999px; border: 1px solid #E5DCD0; color: #4B5563;">
                Current Readiness: <strong style="color: #11141D;">{int(round(float(p_eff) * 100))}%</strong>
            </span>
            <span style="background: #11141D; padding: 5px 14px; border-radius: 9999px; color: #FFFFFF; font-weight: 600;">
                Rule: {rule_name}
            </span>
        </div>
    </div>
    """
    clean_card = "\n".join(l.strip() for l in card_html.splitlines() if l.strip())
    st.markdown(clean_card, unsafe_allow_html=True)
