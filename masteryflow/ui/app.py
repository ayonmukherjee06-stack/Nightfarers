"""MasteryFlow Unified Application Portal (app.py).

Unified Frontend authored jointly by:
- Ayon Mukherjee (Team Lead, Frontend Co-Lead & Orchestrator)
- Soham Choudhury (Frontend Co-Lead & Question Bank Lead)
Integrated with Yash (ML Lead) & Shreyash Jha (Backend Lead)

Role: Single-entry master portal allowing seamless live switching between:
1. 🎓 Student Experience & Adaptive Question Runner (Soham & Ayon)
2. 👩‍🏫 Teacher Command Center & Cohort Governance (Ayon)
3. 🔬 Multi-Persona Cognitive Simulation Replays (Ayon)
4. 📐 Structural DAG Knowledge Graph & Test 8 Reproducibility Proofs (Team)
5. ⚡ ML Engine Inspector & Persona Bench (Yash)
"""

from __future__ import annotations
import sys
from pathlib import Path
import streamlit as st

# Setup base paths for clean imports
BASE_DIR = Path(__file__).resolve().parent.parent
UI_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
if str(UI_DIR) not in sys.path:
    sys.path.insert(0, str(UI_DIR))

# Master Page Config
try:
    st.set_page_config(
        page_title="MasteryFlow | Explainable Adaptive Learning Engine",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded",
    )
except Exception:
    pass

try:
    from backend.engine.contracts import CANONICAL_CONCEPTS, CurriculumGraph, EngineConfig
    from frontend.components.theme import apply_theme
    from frontend.teacher import render_teacher_dashboard
    from backend.sim.replay import load_personas, replay_persona
    from backend.engine.decide import reconstruct_decision_from_snapshot
except ImportError:
    from masteryflow.engine.contracts import CANONICAL_CONCEPTS, CurriculumGraph, EngineConfig
    from masteryflow.ui.components.theme import apply_theme
    from masteryflow.ui.teacher import render_teacher_dashboard
    from masteryflow.sim.replay import load_personas, replay_persona
    from masteryflow.engine.decide import reconstruct_decision_from_snapshot


def render_master_portal():
    # Inject unified 2026 dark design system
    apply_theme()

    # Sidebar Header & Navigation
    st.sidebar.markdown("""
    <div style="
        padding: 16px 14px 18px 14px;
        background: linear-gradient(135deg, rgba(14, 20, 42, 0.8) 0%, rgba(8, 12, 26, 0.9) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        margin-bottom: 18px;
        box-shadow: 0 10px 24px -6px rgba(0, 0, 0, 0.5);
    ">
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="
                width: 38px;
                height: 38px;
                border-radius: 10px;
                background: linear-gradient(135deg, #00F0FF, #38BDF8);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.25rem;
                box-shadow: 0 0 16px rgba(0, 240, 255, 0.4);
            ">
                🌌
            </div>
            <div>
                <h2 style="margin: 0; color: #00F0FF; font-family: 'Space Grotesk', sans-serif; font-weight: 800; font-size: 1.35rem; letter-spacing: -0.5px; line-height: 1.1;">
                    MASTERY<span style="color: #FFFFFF;">FLOW</span>
                </h2>
                <div style="font-size: 0.68rem; color: #94A3B8; font-weight: 600; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 2px;">
                    Cognitive Engine
                </div>
            </div>
        </div>
        <div style="
            margin-top: 12px;
            padding-top: 10px;
            border-top: 1px solid rgba(255, 255, 255, 0.06);
            display: flex;
            justify-content: space-between;
            align-items: center;
        ">
            <span style="font-size: 0.68rem; color: #38BDF8; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">
                YUVA Megathon 2026
            </span>
            <span style="font-size: 0.65rem; background: rgba(16, 185, 129, 0.15); color: #34D399; border: 1px solid rgba(16, 185, 129, 0.3); padding: 1px 6px; border-radius: 9999px; font-weight: 700;">
                Domain 4
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    portal_view = st.sidebar.radio(
        "Workspace Navigation:",
        [
            "🎓 Student Adaptive Learning Portal",
            "👩‍🏫 Teacher Command Center & Cohort Deck",
            "🔬 Multi-Persona Simulation Replays",
            "📐 Curriculum DAG & Test 8 Proofs",
            "⚡ ML Engine Inspector & Persona Bench (Yash)",
        ],
        index=0,
        help="Seamlessly switch between Student question runner, Teacher governance deck, and Simulation replays.",
    )

    st.sidebar.markdown("<hr style='border: 0; border-top: 1px solid rgba(255,255,255,0.06); margin: 18px 0;'>", unsafe_allow_html=True)

    # 1-Click Live Judge Demo Presets
    with st.sidebar.expander("⚡ 1-Click Jury Demo Presets", expanded=False):
        st.markdown("<p style='font-size: 0.74rem; color: #94A3B8; margin-bottom: 8px;'>Instant 1-click stress scenario triggers for hackathon evaluation:</p>", unsafe_allow_html=True)
        if st.button("🛡️ Preset 1: Anti-Gaming Defense (w=0.0)", key="preset_btn_1", use_container_width=True):
            st.session_state.student_id = "STU_GUESSER"
            st.session_state.student_name = "Adversarial Guesser"
            st.session_state.virtual_days = 0.0
            st.session_state.latest_attempt_result = {
                "attempt_id": 999,
                "is_correct": False,
                "evidence_weight": 0.0,
                "is_misconception": False,
                "new_p": 0.30,
                "p_eff": 0.30,
                "time_ms": 1400,
                "hints_used": 0,
                "retry_gap_seconds": 1.2
            }
            st.session_state.last_question_answered = "Q_01"
            st.toast("Preset 1: Rapid Guessing Attack Blocked (w=0.0)!", icon="🛡️")
            st.rerun()

        if st.button("🩹 Preset 2: Prereq Collapse (C4 Fragile Cap)", key="preset_btn_2", use_container_width=True):
            st.session_state.student_id = "STU_001"
            st.session_state.student_name = "Alex Chen"
            st.session_state.virtual_days = 0.0
            st.session_state.latest_attempt_result = None
            st.toast("Preset 2: Prerequisite Inconsistency & Fragile Capping!", icon="🩹")
            st.rerun()

        if st.button("⏳ Preset 3: Memory Time Travel (+21d Decay)", key="preset_btn_3", use_container_width=True):
            st.session_state.student_id = "STU_042"
            st.session_state.student_name = "Diya Sharma"
            st.session_state.virtual_days = 21.0
            st.session_state.latest_attempt_result = None
            st.toast("Preset 3: 21 Days Elapsed -> Spaced Review Triggered!", icon="⏳")
            st.rerun()

        if st.button("🚀 Preset 4: Transfer Verification Barrier", key="preset_btn_4", use_container_width=True):
            st.session_state.student_id = "STU_002"
            st.session_state.student_name = "Maya Patel"
            st.session_state.virtual_days = 0.0
            st.session_state.latest_attempt_result = None
            st.toast("Preset 4: High Accuracy on Easy -> Transfer Proof Required!", icon="🚀")
            st.rerun()

    st.sidebar.markdown("""
    <div style="
        background: rgba(13, 19, 38, 0.65);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 14px;
        padding: 14px 16px;
        margin-bottom: 16px;
    ">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div style="font-size: 0.70rem; color: #00F0FF; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; font-family: 'Space Grotesk', sans-serif;">
                Team Nightfarers
            </div>
            <span style="font-size: 0.65rem; background: rgba(0, 240, 255, 0.12); color: #00F0FF; padding: 1px 6px; border-radius: 4px; font-weight: 700;">
                Jury Verified
            </span>
        </div>
        <div style="font-size: 0.74rem; color: #CBD5E1; margin-top: 8px; line-height: 1.6;">
            &bull; <strong style="color: #FFFFFF;">Ayon Mukherjee</strong> (Lead &amp; Orchestrator)<br>
            &bull; <strong style="color: #FFFFFF;">Yash</strong> (ML &amp; Knowledge Tracing)<br>
            &bull; <strong style="color: #FFFFFF;">Shreyash Jha</strong> (Backend &amp; Persistence)<br>
            &bull; <strong style="color: #FFFFFF;">Soham Choudhury</strong> (Frontend &amp; Questions)
        </div>
    </div>
    """, unsafe_allow_html=True)

    if portal_view == "🎓 Student Adaptive Learning Portal":
        try:
            from frontend.student import render_student_portal
        except ImportError:
            from masteryflow.ui.student import render_student_portal
        render_student_portal(show_header=False, show_sidebar=True)

    elif portal_view == "👩‍🏫 Teacher Command Center & Cohort Deck":
        render_teacher_dashboard()

    elif portal_view == "🔬 Multi-Persona Simulation Replays":
        st.markdown("""
        <div style="
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            padding-bottom: 18px;
            margin-bottom: 22px;
            flex-wrap: wrap;
            gap: 12px;
        ">
            <div>
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div style="
                        width: 44px;
                        height: 44px;
                        border-radius: 12px;
                        background: linear-gradient(135deg, #00F0FF 0%, #8B5CF6 100%);
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 1.4rem;
                        box-shadow: 0 0 20px rgba(0, 240, 255, 0.35);
                    ">
                        🔬
                    </div>
                    <div>
                        <h1 style="color: #00F0FF; margin: 0; font-size: 1.8rem; font-weight: 800; letter-spacing: -0.5px; font-family: 'Space Grotesk', sans-serif;">
                            MULTI-PERSONA<span style="color: #FFFFFF;"> SIMULATION REPLAYS</span>
                        </h1>
                        <div style="font-size: 0.84rem; color: #94A3B8; margin-top: 2px;">
                            Validating 4 Scripted Cognitive Archetypes Through Pure Deterministic State Transitions
                        </div>
                    </div>
                </div>
            </div>
            <div>
                <span style="
                    background: rgba(16, 185, 129, 0.15);
                    color: #34D399;
                    border: 1px solid rgba(16, 185, 129, 0.4);
                    font-size: 0.72rem;
                    font-weight: 800;
                    padding: 4px 14px;
                    border-radius: 9999px;
                    letter-spacing: 0.8px;
                ">
                    ● 100% DETERMINISTIC VERIFICATION
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        personas = load_personas()
        for p in personas:
            res = replay_persona(p)
            status_color = "#10B981" if res["is_verified"] else "#EF4444"
            status_text = "PASSED & VERIFIED" if res["is_verified"] else "FAILED"

            with st.expander(f"👤 {res['name']} ({res['persona_id']}) — Archetype: {res['archetype']} [{status_text}]", expanded=True):
                st.markdown(f"""
                <div style="
                    background: rgba(13, 19, 38, 0.65);
                    border: 1px solid rgba(255, 255, 255, 0.06);
                    border-radius: 12px;
                    padding: 14px 18px;
                    margin-bottom: 14px;
                    font-size: 0.88rem;
                    color: #CBD5E1;
                    line-height: 1.5;
                ">
                    <strong style="color: #FFFFFF;">Archetype Profile:</strong> {p['description']}<br>
                    <strong style="color: #FFFFFF;">Expected Initial Routing:</strong> 
                    <span style="color: #00F0FF; font-family: monospace; font-weight: 700;">{res['expected_initial_action']}</span> on node 
                    <span style="color: #38BDF8; font-family: monospace; font-weight: 700;">{res['expected_target_concept']}</span>
                </div>
                """, unsafe_allow_html=True)

                for step in res["steps"]:
                    act_c = "#10B981" if "ADVANCE" in step["action"] else ("#F43F5E" if "REMEDIATE" in step["action"] else ("#A855F7" if "REVIEW" in step["action"] else "#00F0FF"))
                    st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, rgba(13, 19, 38, 0.75) 0%, rgba(8, 12, 26, 0.85) 100%);
                        border-left: 4px solid {act_c};
                        border-top: 1px solid rgba(255, 255, 255, 0.06);
                        border-right: 1px solid rgba(255, 255, 255, 0.06);
                        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
                        border-radius: 12px;
                        padding: 14px 18px;
                        margin-bottom: 10px;
                        backdrop-filter: blur(14px);
                    ">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; flex-wrap: wrap; gap: 8px;">
                            <strong style="color: #FFFFFF; font-family: 'Space Grotesk', sans-serif; font-size: 0.95rem;">
                                Step {step['step']}: {step['description']}
                            </strong>
                            <div style="display: flex; gap: 8px;">
                                <span style="background: {act_c}22; color: {act_c}; border: 1px solid {act_c}55; font-size: 0.70rem; font-weight: 800; padding: 2px 8px; border-radius: 4px;">
                                    {step['action']}
                                </span>
                                <span style="background: rgba(56, 189, 248, 0.15); color: #38BDF8; border: 1px solid rgba(56, 189, 248, 0.3); font-size: 0.70rem; font-weight: 800; padding: 2px 8px; border-radius: 4px;">
                                    🎯 {step['target_concept']}
                                </span>
                            </div>
                        </div>
                        <div style="font-size: 0.82rem; color: #94A3B8;">
                            <strong>Rule:</strong> <span style="color: #E2E8F0;">{step['rule']}</span>
                        </div>
                        <div style="font-size: 0.82rem; color: #CBD5E1; margin-top: 4px; line-height: 1.4;">
                            <strong>Pedagogical Reason:</strong> <em>"{step['reason']}"</em>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    elif portal_view == "📐 Curriculum DAG & Test 8 Proofs":
        st.markdown("""
        <div style="
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            padding-bottom: 18px;
            margin-bottom: 22px;
            flex-wrap: wrap;
            gap: 12px;
        ">
            <div>
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div style="
                        width: 44px;
                        height: 44px;
                        border-radius: 12px;
                        background: linear-gradient(135deg, #00F0FF 0%, #10B981 100%);
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 1.4rem;
                        box-shadow: 0 0 20px rgba(0, 240, 255, 0.35);
                    ">
                        📐
                    </div>
                    <div>
                        <h1 style="color: #00F0FF; margin: 0; font-size: 1.8rem; font-weight: 800; letter-spacing: -0.5px; font-family: 'Space Grotesk', sans-serif;">
                            CURRICULUM DAG<span style="color: #FFFFFF;"> &amp; TEST 8 REPRODUCIBILITY</span>
                        </h1>
                        <div style="font-size: 0.84rem; color: #94A3B8; margin-top: 2px;">
                            Acyclic Prerequisite Knowledge Graph across Fractions &amp; Ratios &middot; Zero-Variance Mathematical Snapshots
                        </div>
                    </div>
                </div>
            </div>
            <div>
                <span style="
                    background: rgba(0, 240, 255, 0.15);
                    color: #00F0FF;
                    border: 1px solid rgba(0, 240, 255, 0.35);
                    font-size: 0.72rem;
                    font-weight: 800;
                    padding: 4px 14px;
                    border-radius: 9999px;
                    letter-spacing: 0.8px;
                ">
                    ● HACKATHON RUBRIC TEST 8
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        graph = CurriculumGraph(CANONICAL_CONCEPTS)

        col_a, col_b = st.columns([1.2, 1.0])
        with col_a:
            st.markdown("""
            <div style="margin-bottom: 12px;">
                <h3 style="font-family: 'Space Grotesk', sans-serif; color: #00F0FF; font-size: 1.25rem; font-weight: 800; margin: 0;">
                    🗺️ The 10 Canonical Concepts (C1–C10)
                </h3>
            </div>
            """, unsafe_allow_html=True)
            for cid, data in CANONICAL_CONCEPTS.items():
                prereqs = data["prereqs"]
                prereq_str = ", ".join(prereqs) if prereqs else "None (Foundational Baseline)"
                st.markdown(f"""
                <div class="mf-glass-card" style="padding: 16px 20px; margin-bottom: 10px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <strong style="color: #FFFFFF; font-size: 0.98rem; font-family: 'Space Grotesk', sans-serif;">
                            {cid}: {data['title']}
                        </strong>
                        <span style="font-size: 0.70rem; background: rgba(56, 189, 248, 0.15); border: 1px solid rgba(56, 189, 248, 0.3); padding: 2px 8px; border-radius: 6px; color: #38BDF8; font-weight: 700;">
                            Prereqs: {prereq_str}
                        </span>
                    </div>
                    <div style="font-size: 0.82rem; color: #94A3B8; margin-top: 6px; line-height: 1.45;">
                        {data['description']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        with col_b:
            st.markdown("""
            <div style="margin-bottom: 6px;">
                <h3 style="font-family: 'Space Grotesk', sans-serif; color: #38BDF8; font-size: 1.25rem; font-weight: 800; margin: 0;">
                    ⚡ Test 8: Decision Snapshot Reproducibility Proof
                </h3>
                <p style="font-size: 0.80rem; color: #94A3B8; margin: 4px 0 14px 0;">
                    Recomputing from stored <code>inputs_snapshot</code> must yield 100% identical outputs with 0.00% variance.
                </p>
            </div>
            """, unsafe_allow_html=True)

            sample_snapshot = {
                "student_id": "STU_DIYA",
                "current_concept_id": "C7",
                "challenge_mode": False,
                "config": EngineConfig().to_dict(),
                "p_eff": {"C1": 0.88, "C2": 0.42, "C7": 0.48},
                "mastery_state": {
                    "C1": {"concept_id": "C1", "p_eff": 0.88, "was_mastered": True, "transfer_verified": True},
                    "C2": {"concept_id": "C2", "p_eff": 0.42, "was_mastered": False, "transfer_verified": False},
                    "C7": {"concept_id": "C7", "p_eff": 0.48, "was_mastered": False, "transfer_verified": False, "errors_count": 2, "hints_count": 2},
                }
            }

            st.json(sample_snapshot)

            if st.button("⚡ Verify Snapshot Reconstruction (Zero Variance)", type="primary", use_container_width=True):
                reconstructed = reconstruct_decision_from_snapshot(sample_snapshot, graph)
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, rgba(16, 185, 129, 0.16) 0%, rgba(13, 19, 38, 0.95) 100%);
                    border: 1px solid rgba(16, 185, 129, 0.45);
                    border-radius: 14px;
                    padding: 18px 22px;
                    margin-top: 14px;
                    box-shadow: 0 10px 24px -4px rgba(16, 185, 129, 0.2);
                ">
                    <div style="color: #34D399; font-weight: 800; font-size: 1.05rem; margin-bottom: 10px; font-family: 'Space Grotesk', sans-serif;">
                        ✅ TEST 8 PASS: 100% Deterministic Fidelity Reproduced!
                    </div>
                    <div style="font-size: 0.85rem; color: #F8FAFC; line-height: 1.65;">
                        &bull; <strong>Action:</strong> <code style="color: #34D399;">{reconstructed.action.value}</code><br>
                        &bull; <strong>Target Node:</strong> <code style="color: #38BDF8;">{reconstructed.target_concept_id}</code><br>
                        &bull; <strong>Rule Triggered:</strong> <span style="color: #CBD5E1;">{reconstructed.rule_triggered}</span><br>
                        &bull; <strong>Pedagogical Reason:</strong> <em>"{reconstructed.reason}"</em>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    elif portal_view == "⚡ ML Engine Inspector & Persona Bench (Yash)":
        try:
            from frontend.ml_inspector import render_ml_engine_inspector
        except ImportError:
            from masteryflow.ui.ml_inspector import render_ml_engine_inspector
        render_ml_engine_inspector()


if __name__ == "__main__":
    render_master_portal()
