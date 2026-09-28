"""MasteryFlow Interactive DAG Concept Tree & Progress Visualizer (dag_visualizer.py).

Owner: Soham Choudhury (Frontend Co-Lead & Question Bank Lead)
Aesthetic: State-of-the-Art 2026 dark glass curriculum roadmap with layered prerequisite tiers,
progress meter bars, luminous status badges, animated flow connectors, and interactive node selection.
"""

from typing import Any, Dict, List, Optional
import streamlit as st


STATUS_CONFIG = {
    "mastered": {
        "label": "Mastered",
        "badge_color": "#10B981",
        "bg_gradient": "linear-gradient(135deg, rgba(16, 185, 129, 0.16) 0%, rgba(6, 78, 59, 0.25) 100%)",
        "border_color": "#10B981",
        "glow": "rgba(16, 185, 129, 0.25)",
        "icon": "✦"
    },
    "provisional": {
        "label": "Provisional",
        "badge_color": "#F59E0B",
        "bg_gradient": "linear-gradient(135deg, rgba(245, 158, 11, 0.16) 0%, rgba(120, 53, 15, 0.25) 100%)",
        "border_color": "#F59E0B",
        "glow": "rgba(245, 158, 11, 0.25)",
        "icon": "⏳"
    },
    "practicing": {
        "label": "Practicing",
        "badge_color": "#00F0FF",
        "bg_gradient": "linear-gradient(135deg, rgba(0, 240, 255, 0.15) 0%, rgba(14, 165, 233, 0.20) 100%)",
        "border_color": "#00F0FF",
        "glow": "rgba(0, 240, 255, 0.25)",
        "icon": "⚡"
    },
    "fragile": {
        "label": "Fragile Cap",
        "badge_color": "#F43F5E",
        "bg_gradient": "linear-gradient(135deg, rgba(244, 63, 94, 0.18) 0%, rgba(136, 19, 55, 0.30) 100%)",
        "border_color": "#F43F5E",
        "glow": "rgba(244, 63, 94, 0.30)",
        "icon": "⚠️"
    },
    "unseen": {
        "label": "Locked",
        "badge_color": "#64748B",
        "bg_gradient": "linear-gradient(135deg, rgba(30, 41, 59, 0.45) 0%, rgba(15, 23, 42, 0.65) 100%)",
        "border_color": "#334155",
        "glow": "rgba(0, 0, 0, 0)",
        "icon": "🔒"
    }
}


DAG_LAYERS = [
    {"tier": "Tier 1", "title": "Foundational Baseline", "concepts": ["C1"]},
    {"tier": "Tier 2", "title": "Core Equivalence Principle", "concepts": ["C2"]},
    {"tier": "Tier 3", "title": "Fraction Operations & Ratios", "concepts": ["C3", "C4", "C5", "C6"]},
    {"tier": "Tier 4", "title": "Rate & Percentage Dynamics", "concepts": ["C7", "C9"]},
    {"tier": "Tier 5", "title": "Algebraic Proportions", "concepts": ["C8"]},
    {"tier": "Tier 6", "title": "Capstone Real-World Synthesis", "concepts": ["C10"]},
]


def render_dag_visualizer(
    concepts_meta: Dict[str, Dict[str, Any]],
    mastery_map: Dict[str, Dict[str, Any]],
    active_concept_id: str,
    on_select_concept_cb=None
):
    """Renders the stylized 2026 dark-glass curriculum DAG roadmap with interactive nodes."""
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 16px; flex-wrap: wrap; gap: 12px;">
        <div>
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 1.25rem;">🗺️</span>
                <h3 style="font-family: 'Space Grotesk', sans-serif; color: #00F0FF; margin: 0; font-size: 1.35rem; font-weight: 800; letter-spacing: -0.5px;">
                    Curriculum Knowledge Graph (10-Node Topological DAG)
                </h3>
            </div>
            <p style="color: #94A3B8; font-size: 0.84rem; margin: 4px 0 0 0;">
                Bayesian Knowledge Tracing &middot; Prerequisite Invariant Ceilings &middot; Ebbinghaus Retention Decay
            </p>
        </div>
        <div style="display: flex; gap: 8px; flex-wrap: wrap; font-size: 0.72rem;">
            <span style="background: rgba(16, 185, 129, 0.15); color: #34D399; border: 1px solid rgba(16, 185, 129, 0.4); padding: 3px 8px; border-radius: 6px; font-weight: 700;">✦ Mastered (&ge;85%)</span>
            <span style="background: rgba(245, 158, 11, 0.15); color: #FBBF24; border: 1px solid rgba(245, 158, 11, 0.4); padding: 3px 8px; border-radius: 6px; font-weight: 700;">⏳ Provisional</span>
            <span style="background: rgba(0, 240, 255, 0.15); color: #00F0FF; border: 1px solid rgba(0, 240, 255, 0.4); padding: 3px 8px; border-radius: 6px; font-weight: 700;">⚡ Practicing</span>
            <span style="background: rgba(244, 63, 94, 0.15); color: #FB7185; border: 1px solid rgba(244, 63, 94, 0.4); padding: 3px 8px; border-radius: 6px; font-weight: 700;">⚠️ Fragile Cap</span>
            <span style="background: rgba(100, 116, 139, 0.15); color: #94A3B8; border: 1px solid rgba(100, 116, 139, 0.4); padding: 3px 8px; border-radius: 6px; font-weight: 700;">🔒 Locked</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    for layer_idx, layer in enumerate(DAG_LAYERS):
        # Downward connector line between tiers
        if layer_idx > 0:
            st.markdown("""
            <div style="display: flex; justify-content: center; align-items: center; gap: 8px; margin: 2px 0 8px 0;">
                <div style="height: 1px; width: 40px; background: rgba(56, 189, 248, 0.2);"></div>
                <span style="color: #38BDF8; font-size: 0.80rem; opacity: 0.6;">▼ Prerequisite Flow</span>
                <div style="height: 1px; width: 40px; background: rgba(56, 189, 248, 0.2);"></div>
            </div>
            """, unsafe_allow_html=True)

        # Tier Divider Label
        st.markdown(f"""
        <div style="
            display: flex;
            align-items: center;
            gap: 10px;
            margin: 12px 0 10px 0;
        ">
            <span style="
                font-family: 'Space Grotesk', sans-serif;
                font-size: 0.70rem;
                text-transform: uppercase;
                background: rgba(56, 189, 248, 0.15);
                color: #38BDF8;
                border: 1px solid rgba(56, 189, 248, 0.35);
                padding: 2px 8px;
                border-radius: 4px;
                font-weight: 800;
                letter-spacing: 1px;
            ">
                {layer['tier']}
            </span>
            <span style="
                font-family: 'Space Grotesk', sans-serif;
                font-size: 0.82rem;
                font-weight: 700;
                color: #E2E8F0;
                letter-spacing: 0.5px;
            ">
                {layer['title']}
            </span>
            <div style="flex-grow: 1; height: 1px; background: rgba(255, 255, 255, 0.06);"></div>
        </div>
        """, unsafe_allow_html=True)

        cols = st.columns(len(layer["concepts"]))
        for idx, cid in enumerate(layer["concepts"]):
            c_meta = concepts_meta.get(cid, {})
            m_state = mastery_map.get(cid, {})

            p_eff = float(m_state.get("p_eff", 0.30))
            is_fragile = bool(m_state.get("is_fragile", False))
            status_raw = str(m_state.get("status", "unseen"))
            stability = m_state.get("stability_days", 7.0)

            # Classify status
            if is_fragile:
                status_key = "fragile"
            elif status_raw in STATUS_CONFIG:
                status_key = status_raw
            else:
                status_key = "practicing" if p_eff > 0.35 else "unseen"

            cfg = STATUS_CONFIG[status_key]
            is_active = (cid == active_concept_id)

            active_glow = "box-shadow: 0 0 24px rgba(0, 240, 255, 0.4), inset 0 0 12px rgba(0, 240, 255, 0.2); border: 2px solid #00F0FF;" if is_active else f"border: 1px solid {cfg['border_color']}66; box-shadow: 0 10px 24px -6px rgba(0,0,0,0.5);"

            prereqs = c_meta.get("prerequisites", [])
            prereq_str = ", ".join(prereqs) if prereqs else "Root (Baseline)"

            pct_val = max(5, min(100, int(round(p_eff * 100))))
            meter_color = cfg["badge_color"]

            with cols[idx]:
                node_html = f"""
                <div style="
                    background: {cfg['bg_gradient']};
                    {active_glow}
                    border-radius: 14px;
                    padding: 14px 16px;
                    margin-bottom: 8px;
                    backdrop-filter: blur(16px);
                    transition: all 0.25s ease;
                ">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <span style="font-family: 'Space Grotesk', sans-serif; font-size: 1rem; font-weight: 800; color: #FFFFFF;">
                            {c_meta.get('icon', '🔹')} {cid}
                        </span>
                        <span style="
                            font-size: 0.65rem;
                            font-weight: 700;
                            text-transform: uppercase;
                            color: {cfg['badge_color']};
                            background: rgba(0,0,0,0.45);
                            padding: 2px 8px;
                            border-radius: 9999px;
                            border: 1px solid {cfg['badge_color']}44;
                            display: inline-flex;
                            align-items: center;
                            gap: 3px;
                        ">
                            {cfg['icon']} {cfg['label']}
                        </span>
                    </div>

                    <div style="font-size: 0.85rem; font-weight: 600; color: #F1F5F9; margin: 2px 0 10px 0; line-height: 1.25; min-height: 34px;">
                        {c_meta.get('name', cid)}
                    </div>

                    <!-- Progress Bar -->
                    <div style="background: rgba(0, 0, 0, 0.4); border-radius: 6px; height: 6px; overflow: hidden; margin-bottom: 8px; border: 1px solid rgba(255,255,255,0.06);">
                        <div style="width: {pct_val}%; height: 100%; background: {meter_color}; border-radius: 6px; transition: width 0.4s ease;"></div>
                    </div>

                    <div style="display: flex; justify-content: space-between; font-size: 0.74rem; color: #94A3B8;">
                        <span>p_eff: <strong style="color: #FFFFFF; font-family: monospace;">{pct_val}%</strong></span>
                        <span>Stability S: <strong style="color: #A78BFA; font-family: monospace;">{stability}d</strong></span>
                    </div>

                    <div style="font-size: 0.68rem; color: #64748B; margin-top: 6px; border-top: 1px solid rgba(255,255,255,0.06); padding-top: 4px;">
                        Prereqs: <span style="color: #CBD5E1;">{prereq_str}</span>
                    </div>
                </div>
                """
                st.markdown(node_html, unsafe_allow_html=True)
                btn_label = f"🎯 Current Focus ({cid})" if is_active else f"Switch Focus to {cid}"
                if st.button(btn_label, key=f"btn_target_{cid}", use_container_width=True):
                    if on_select_concept_cb:
                        on_select_concept_cb(cid)
