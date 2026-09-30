"""MasteryFlow Interactive Curriculum Graph & Progress Map (dag_visualizer.py).

Renders the 10-concept prerequisite knowledge graph with clear learning tiers,
mastery progress meters, and interactive focus selection in clean light design.
"""

from typing import Any, Dict, List, Optional
import streamlit as st

try:
    from frontend.components.theme import render_html
except ImportError:
    from .theme import render_html


STATUS_CONFIG = {
    "mastered": {
        "label": "Mastered",
        "badge_color": "#059669",
        "bg": "#E8F7F0",
        "border_color": "rgba(5, 150, 105, 0.35)",
        "icon": ""
    },
    "provisional": {
        "label": "Verifying",
        "badge_color": "#D97706",
        "bg": "#FEF3C7",
        "border_color": "rgba(217, 119, 6, 0.35)",
        "icon": ""
    },
    "practicing": {
        "label": "In Progress",
        "badge_color": "#0284C7",
        "bg": "#E0F2FE",
        "border_color": "rgba(2, 132, 199, 0.35)",
        "icon": ""
    },
    "fragile": {
        "label": "Prereq Gap",
        "badge_color": "#E11D48",
        "bg": "#FFE4E6",
        "border_color": "rgba(225, 29, 72, 0.35)",
        "icon": ""
    },
    "unseen": {
        "label": "Upcoming",
        "badge_color": "#78716C",
        "bg": "#F5EFE6",
        "border_color": "rgba(120, 113, 108, 0.25)",
        "icon": ""
    }
}


SUBJECTS_DAG_LAYERS: Dict[str, List[Dict[str, Any]]] = {
    "Mathematics": [
        {"tier": "Tier 1", "title": "Foundational Baseline", "concepts": ["C1"]},
        {"tier": "Tier 2", "title": "Core Equivalence Principle", "concepts": ["C2"]},
        {"tier": "Tier 3", "title": "Fraction Operations & Ratios", "concepts": ["C3", "C4", "C5", "C6"]},
        {"tier": "Tier 4", "title": "Rate & Percentage Dynamics", "concepts": ["C7", "C9"]},
        {"tier": "Tier 5", "title": "Algebraic Proportions", "concepts": ["C8"]},
        {"tier": "Tier 6", "title": "Capstone Real-World Applications", "concepts": ["C10"]},
    ],
    "Computer Networks": [
        {"tier": "Tier 1", "title": "Architectural Reference Models", "concepts": ["CN1"]},
        {"tier": "Tier 2", "title": "Data Link & Error Detection", "concepts": ["CN2"]},
        {"tier": "Tier 3", "title": "Core Protocols & Addressing", "concepts": ["CN3", "CN5"]},
        {"tier": "Tier 4", "title": "Routing Protocols & Congestion", "concepts": ["CN4", "CN6"]},
        {"tier": "Tier 5", "title": "Application Layer & Web Systems", "concepts": ["CN7"]},
        {"tier": "Tier 6", "title": "Network Security & Cryptography", "concepts": ["CN8"]},
    ],
    "Artificial Intelligence": [
        {"tier": "Tier 1", "title": "State-Space & Heuristic Search", "concepts": ["AI1"]},
        {"tier": "Tier 2", "title": "Game Trees & Statistical Learning", "concepts": ["AI2", "AI3"]},
        {"tier": "Tier 3", "title": "Artificial Neurons & Activations", "concepts": ["AI4"]},
        {"tier": "Tier 4", "title": "Deep Neural Nets & Optimization", "concepts": ["AI5"]},
        {"tier": "Tier 5", "title": "Computer Vision & Transformers", "concepts": ["AI6", "AI7"]},
        {"tier": "Tier 6", "title": "Reinforcement Learning & Bellman", "concepts": ["AI8"]},
    ],
    "Formal Languages & Automata": [
        {"tier": "Tier 1", "title": "Alphabets & Regular Expressions", "concepts": ["FLA1"]},
        {"tier": "Tier 2", "title": "Deterministic & NFA Automata", "concepts": ["FLA2", "FLA3"]},
        {"tier": "Tier 3", "title": "Non-Regularity & Context-Free", "concepts": ["FLA4", "FLA5"]},
        {"tier": "Tier 4", "title": "Pushdown Automata & Stack Memory", "concepts": ["FLA6"]},
        {"tier": "Tier 5", "title": "Turing Computability", "concepts": ["FLA7"]},
        {"tier": "Tier 6", "title": "Decidability & Complexity Classes", "concepts": ["FLA8"]},
    ],
    "Biochemistry": [
        {"tier": "Tier 1", "title": "Aqueous & Buffer Foundations", "concepts": ["BIO1"]},
        {"tier": "Tier 2", "title": "Protein Hierarchies & Kinetics", "concepts": ["BIO2", "BIO3"]},
        {"tier": "Tier 3", "title": "Membrane Dynamics & Lipids", "concepts": ["BIO4"]},
        {"tier": "Tier 4", "title": "Central Metabolic Catabolism", "concepts": ["BIO5", "BIO6"]},
        {"tier": "Tier 5", "title": "Oxidative Bioenergetics", "concepts": ["BIO7"]},
        {"tier": "Tier 6", "title": "Molecular Genetics & DNA", "concepts": ["BIO8"]},
    ],
}


def render_dag_visualizer(
    concepts_meta: Dict[str, Dict[str, Any]],
    mastery_map: Dict[str, Dict[str, Any]],
    active_concept_id: str,
    on_select_concept_cb=None
):
    """Renders the curriculum roadmap with interactive concept nodes in Apitex porcelain design."""
    total_count = len(concepts_meta) if concepts_meta else 10
    matched_mastery = [mastery_map.get(cid, {}) for cid in concepts_meta]
    mastered_count = sum(1 for m in matched_mastery if m.get("status") == "mastered" or float(m.get("p_eff", 0)) >= 0.85)
    fragile_count = sum(1 for m in matched_mastery if m.get("is_fragile"))
    practicing_count = max(0, total_count - mastered_count)

    # Detect current subject from concepts_meta
    sample_cid = list(concepts_meta.keys())[0] if concepts_meta else "C1"
    if sample_cid.startswith("CN"):
        cur_subject = "Computer Networks"
    elif sample_cid.startswith("AI"):
        cur_subject = "Artificial Intelligence"
    elif sample_cid.startswith("FLA"):
        cur_subject = "Formal Languages & Automata"
    elif sample_cid.startswith("BIO"):
        cur_subject = "Biochemistry"
    else:
        cur_subject = st.session_state.get("active_subject", "Mathematics")

    subject_layers = SUBJECTS_DAG_LAYERS.get(cur_subject)
    if not subject_layers:
        # Fallback dynamic tier builder
        cats = {}
        for cid, meta in concepts_meta.items():
            cat = meta.get("category", "General")
            cats.setdefault(cat, []).append(cid)
        subject_layers = [
            {"tier": f"Tier {i+1}", "title": cat_name, "concepts": cids}
            for i, (cat_name, cids) in enumerate(cats.items())
        ]

    render_html(f"""
    <div style="
        background: #FFFFFF;
        border: 1px solid rgba(228, 221, 211, 0.9);
        border-radius: 22px;
        padding: 22px 26px;
        margin-bottom: 22px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 12px;
        box-shadow: 0 10px 30px -4px rgba(60, 50, 30, 0.05);
    ">
        <div>
            <div style="display: flex; align-items: center; gap: 8px;">
                <h3 style="color: #11141D; margin: 0; font-size: 1.25rem; font-weight: 800; letter-spacing: -0.02em;">
                    {cur_subject} Curriculum Learning Roadmap
                </h3>
            </div>
            <p style="color: #78716C; font-size: 0.84rem; margin: 4px 0 0 0;">
                {total_count} sequential concepts mapped by prerequisite dependencies
            </p>
        </div>

        <div style="display: flex; gap: 8px; flex-wrap: wrap; font-size: 0.74rem;">
            <span style="background: #E8F7F0; color: #047857; border: 1px solid rgba(5, 150, 105, 0.35); padding: 5px 14px; border-radius: 9999px; font-weight: 700;">
                {mastered_count}/{total_count} Mastered
            </span>
            <span style="background: #E0F2FE; color: #0369A1; border: 1px solid rgba(2, 132, 199, 0.35); padding: 5px 14px; border-radius: 9999px; font-weight: 700;">
                {practicing_count} In Progress
            </span>
            {f'<span style="background: #FFE4E6; color: #BE123C; border: 1px solid rgba(225, 29, 72, 0.35); padding: 5px 14px; border-radius: 9999px; font-weight: 700;">{fragile_count} Prereq Gap</span>' if fragile_count > 0 else ''}
        </div>
    </div>
    """)

    for layer_idx, layer in enumerate(subject_layers):
        # Subtle downward connector
        if layer_idx > 0:
            render_html("""
            <div style="display: flex; justify-content: center; align-items: center; gap: 10px; margin: 8px 0 12px 0;">
                <div style="height: 1px; width: 44px; background: rgba(228, 221, 211, 0.9);"></div>
                <span style="color: #A8A29E; font-size: 0.76rem; font-weight: 700;">
                    ↓
                </span>
                <div style="height: 1px; width: 44px; background: rgba(228, 221, 211, 0.9);"></div>
            </div>
            """)

        # Tier Divider Label
        render_html(f"""
        <div style="
            display: flex;
            align-items: center;
            gap: 12px;
            margin: 12px 0 10px 0;
        ">
            <span style="
                font-size: 0.70rem;
                text-transform: uppercase;
                background: #11141D;
                color: #FFFFFF;
                border: 1px solid #11141D;
                padding: 4px 12px;
                border-radius: 9999px;
                font-weight: 800;
                letter-spacing: 0.5px;
            ">
                {layer['tier']}
            </span>
            <span style="
                font-size: 0.88rem;
                font-weight: 800;
                color: #11141D;
            ">
                {layer['title']}
            </span>
            <div style="flex-grow: 1; height: 1px; background: rgba(228, 221, 211, 0.8);"></div>
        </div>
        """)

        cols = st.columns(len(layer["concepts"]))
        for idx, cid in enumerate(layer["concepts"]):
            c_meta = concepts_meta.get(cid, {})
            m_state = mastery_map.get(cid, {})

            p_eff = float(m_state.get("p_eff", 0.30))
            is_fragile = bool(m_state.get("is_fragile", False))
            status_raw = str(m_state.get("status", "unseen"))
            stability = m_state.get("stability_days", 7.0)

            if is_fragile:
                status_key = "fragile"
            elif status_raw in STATUS_CONFIG:
                status_key = status_raw
            else:
                status_key = "practicing" if p_eff > 0.35 else "unseen"

            cfg = STATUS_CONFIG[status_key]
            is_active = (cid == active_concept_id)

            card_border = (
                "border: 2px solid #11141D; background: #FFFFFF; box-shadow: 0 10px 28px -4px rgba(17, 20, 29, 0.12);"
                if is_active
                else "border: 1px solid rgba(228, 221, 211, 0.9); background: #FFFFFF; box-shadow: 0 4px 16px -2px rgba(60, 50, 30, 0.04);"
            )

            prereqs = c_meta.get("prerequisites", [])
            prereq_str = ", ".join(prereqs) if prereqs else "None (Foundational)"

            pct_val = max(5, min(100, int(round(p_eff * 100))))
            meter_color = cfg["badge_color"]

            with cols[idx]:
                node_html = f"""
                <div style="
                    {card_border}
                    border-radius: 18px;
                    padding: 16px 18px;
                    margin-bottom: 8px;
                    transition: all 0.2s ease;
                ">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                        <span style="font-size: 0.98rem; font-weight: 800; color: #11141D;">
                            {cid}
                        </span>
                        <span style="
                            font-size: 0.65rem;
                            font-weight: 700;
                            color: {cfg['badge_color']};
                            background: {cfg['bg']};
                            padding: 3px 9px;
                            border-radius: 9999px;
                            border: 1px solid {cfg['border_color']};
                            display: inline-flex;
                            align-items: center;
                            gap: 4px;
                        ">
                            {cfg['icon']} {cfg['label']}
                        </span>
                    </div>

                    <div style="font-size: 0.86rem; font-weight: 700; color: #11141D; margin: 4px 0 12px 0; line-height: 1.35; min-height: 36px;">
                        {c_meta.get('name', cid)}
                    </div>

                    <!-- Progress Bar -->
                    <div style="background: rgba(228, 221, 211, 0.6); border-radius: 999px; height: 6px; overflow: hidden; margin-bottom: 10px;">
                        <div style="width: {pct_val}%; height: 100%; background: {meter_color}; border-radius: 999px; transition: width 0.4s ease;"></div>
                    </div>

                    <div style="display: flex; justify-content: space-between; font-size: 0.74rem; color: #78716C;">
                        <span>Mastery: <strong style="color: #11141D;">{pct_val}%</strong></span>
                        <span>Retention: <strong style="color: #11141D;">{stability:.1f}d</strong></span>
                    </div>

                    <div style="font-size: 0.70rem; color: #78716C; margin-top: 8px; border-top: 1px solid rgba(228, 221, 211, 0.7); padding-top: 6px;">
                        Prereqs: <span style="color: #11141D; font-weight: 600;">{prereq_str}</span>
                    </div>
                </div>
                """
                render_html(node_html)
                btn_label = f"Current Topic ({cid})" if is_active else f"Switch to {cid}"
                if st.button(btn_label, key=f"btn_target_{cid}", use_container_width=True):
                    if on_select_concept_cb:
                        on_select_concept_cb(cid)
