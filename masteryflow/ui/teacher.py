"""MasteryFlow Dedicated Teacher Command Center (teacher.py).

Authored by: Ayon Mukherjee (Team Lead & Orchestrator)
Role: Institutional-grade management deck for educators:
- Cohort Mastery Heatmap (Students x Concepts)
- Systemic Curricular Bottleneck Alerts
- Stuck-Learner Escalation Queue
- 1-Click Persistent Human Override Console
- Chronological SQLite Audit Log
- Live Time Travel Ebbinghaus Decay Simulator
"""

from __future__ import annotations
import streamlit as st
import copy

try:
    from backend.engine.contracts import (
        CurriculumGraph,
        EngineConfig,
        ConceptMastery,
        ActionType,
        CANONICAL_CONCEPTS,
    )
    from backend.engine.override import OverrideManager
    from frontend.components.heatmap import (
        render_cohort_heatmap,
        compute_cohort_metrics,
        detect_group_bottlenecks,
        get_stuck_learners,
    )
    from frontend.components.time_travel import render_time_travel_slider, apply_time_travel_decay
    from frontend.components.theme import apply_theme
except ImportError:
    from masteryflow.engine.contracts import (
        CurriculumGraph,
        EngineConfig,
        ConceptMastery,
        ActionType,
        CANONICAL_CONCEPTS,
    )
    from masteryflow.engine.override import OverrideManager
    from masteryflow.ui.components.heatmap import (
        render_cohort_heatmap,
        compute_cohort_metrics,
        detect_group_bottlenecks,
        get_stuck_learners,
    )
    from masteryflow.ui.components.time_travel import render_time_travel_slider, apply_time_travel_decay
    from masteryflow.ui.components.theme import apply_theme


def get_default_teacher_cohort():
    """Builds realistic cohort dataset with 6 diverse student profiles."""
    cohort = {}
    base_map = lambda: {cid: ConceptMastery(concept_id=cid, p_raw=0.10, p_eff=0.10) for cid in CANONICAL_CONCEPTS}

    # 1. Priya Singh (High Performer)
    cohort["STU_001"] = {"name": "Priya Singh", "mastery": base_map()}
    cohort["STU_001"]["mastery"]["C1"].p_eff = 0.95
    cohort["STU_001"]["mastery"]["C1"].was_mastered = True
    cohort["STU_001"]["mastery"]["C2"].p_eff = 0.92
    cohort["STU_001"]["mastery"]["C2"].was_mastered = True
    cohort["STU_001"]["mastery"]["C3"].p_eff = 0.88
    cohort["STU_001"]["mastery"]["C3"].was_mastered = True

    # 2. Aarav Patel (Stuck Learner - Plateau on C2)
    cohort["STU_002"] = {"name": "Aarav Patel", "mastery": base_map()}
    cohort["STU_002"]["mastery"]["C1"].p_eff = 0.85
    cohort["STU_002"]["mastery"]["C1"].was_mastered = True
    cohort["STU_002"]["mastery"]["C2"].p_eff = 0.40
    cohort["STU_002"]["mastery"]["C2"].history_p = [0.38, 0.39, 0.39, 0.40]
    cohort["STU_002"]["mastery"]["C2"].attempts_count = 6
    cohort["STU_002"]["mastery"]["C2"].errors_count = 4

    # 3. Diya Sharma (Foundational Gap on C2, Active on C7)
    cohort["STU_003"] = {"name": "Diya Sharma", "mastery": base_map()}
    cohort["STU_003"]["mastery"]["C1"].p_eff = 0.88
    cohort["STU_003"]["mastery"]["C1"].was_mastered = True
    cohort["STU_003"]["mastery"]["C2"].p_eff = 0.42
    cohort["STU_003"]["mastery"]["C5"].p_eff = 0.65
    cohort["STU_003"]["mastery"]["C6"].p_eff = 0.60
    cohort["STU_003"]["mastery"]["C7"].p_eff = 0.48
    cohort["STU_003"]["mastery"]["C7"].errors_count = 2

    # 4. Kabir Khan (Weak on C2)
    cohort["STU_004"] = {"name": "Kabir Khan", "mastery": base_map()}
    cohort["STU_004"]["mastery"]["C1"].p_eff = 0.78
    cohort["STU_004"]["mastery"]["C2"].p_eff = 0.38

    # 5. Rohan Verma (Decayed on C1)
    cohort["STU_005"] = {"name": "Rohan Verma", "mastery": base_map()}
    cohort["STU_005"]["mastery"]["C1"].p_eff = 0.48
    cohort["STU_005"]["mastery"]["C1"].was_mastered = True
    cohort["STU_005"]["mastery"]["C2"].p_eff = 0.82
    cohort["STU_005"]["mastery"]["C2"].was_mastered = True

    # 6. Ananya Sen (Solid on C1 & C2)
    cohort["STU_006"] = {"name": "Ananya Sen", "mastery": base_map()}
    cohort["STU_006"]["mastery"]["C1"].p_eff = 0.90
    cohort["STU_006"]["mastery"]["C1"].was_mastered = True
    cohort["STU_006"]["mastery"]["C2"].p_eff = 0.86
    cohort["STU_006"]["mastery"]["C2"].was_mastered = True

    return cohort


def render_teacher_dashboard():
    """Main rendering routine for the Teacher Command Center with executive glassmorphic styling."""
    try:
        st.set_page_config(page_title="MasteryFlow — Teacher Command Center", page_icon="👩‍🏫", layout="wide")
    except Exception:
        pass

    apply_theme()

    # Teacher Hero Header (2026 Executive Linear Style)
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
                    background: linear-gradient(135deg, #00F0FF 0%, #3B82F6 100%);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 1.4rem;
                    box-shadow: 0 0 20px rgba(0, 240, 255, 0.35);
                ">
                    👩‍🏫
                </div>
                <div>
                    <h1 style="color: #00F0FF; margin: 0; font-size: 1.8rem; font-weight: 800; letter-spacing: -0.5px; font-family: 'Space Grotesk', sans-serif;">
                        TEACHER<span style="color: #FFFFFF;"> COMMAND CENTER</span>
                    </h1>
                    <div style="font-size: 0.84rem; color: #94A3B8; margin-top: 2px;">
                        Institutional Cohort Diagnostics &middot; Systemic Bottlenecks &middot; Human-in-the-Loop Governance
                    </div>
                </div>
            </div>
        </div>
        <div style="text-align: right;">
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
                ● GOVERNANCE DECK ACTIVE
            </span>
            <div style="font-size: 0.74rem; color: #64748B; margin-top: 4px; font-family: monospace;">
                Teacher: TEACHER_SHUKLA &middot; Grade 6 Fractions
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    graph = CurriculumGraph(CANONICAL_CONCEPTS)
    override_mgr = OverrideManager("masteryflow.db")
    cohort = get_default_teacher_cohort()

    # Time Travel Clock Slider in Teacher Deck
    with st.expander("⏳ Longitudinal Time Travel Simulation (Simulate Ebbinghaus Forgetting Curves Across Cohort)", expanded=False):
        st.markdown(
            "<p style='font-size: 0.85rem; color: #94A3B8; margin-bottom: 10px;'>"
            "Advance the cohort clock by N days to simulate forgetting curves across all students simultaneously:"
            "</p>",
            unsafe_allow_html=True
        )
        elapsed_days = render_time_travel_slider(default_days=0)
        if elapsed_days > 0:
            for stu_id in cohort:
                for cid in cohort[stu_id]["mastery"]:
                    m = cohort[stu_id]["mastery"][cid]
                    if m.was_mastered:
                        m.p_eff = apply_time_travel_decay(m.p_eff, elapsed_days)

    # Render Cohort Heatmap, Systemic Bottlenecks & Stuck Queue
    render_cohort_heatmap(cohort, graph=graph)

    # 1-Click Persistent Override Console
    st.markdown("""
    <div style="margin-top: 26px; margin-bottom: 14px;">
        <div style="display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 1.25rem;">🛠️</span>
            <h3 style="font-family: 'Space Grotesk', sans-serif; color: #00F0FF; margin: 0; font-size: 1.35rem; font-weight: 800;">
                1-Click Persistent Teacher Override Console
            </h3>
        </div>
        <p style="font-size: 0.84rem; color: #94A3B8; margin: 4px 0 0 0;">
            Intervene directly in student learning paths. Decisions are written immediately to SQLite and supersede automatic engine recommendations.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="mf-glass-card" style="padding: 22px 26px; margin-bottom: 20px;">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            stu_choice = st.selectbox("Select Student to Override:", list(cohort.keys()), format_func=lambda k: f"{cohort[k]['name']} ({k})")
        with c2:
            act_choice = st.selectbox("Assign Pedagogical Action:", [a.value for a in ActionType])
        with c3:
            target_choice = st.selectbox("Target Concept Node:", list(CANONICAL_CONCEPTS.keys()), index=0)

        reason_input = st.text_input("Mandatory Pedagogical Rationale for Audit Log:", "Identified foundational misconception in oral exam; assigned foundational remediation.")

        btn_col1, btn_col2 = st.columns([1, 1])
        with btn_col1:
            if st.button("💾 Apply & Record Override in SQLite", type="primary", use_container_width=True):
                rec_id = override_mgr.record_override(
                    student_id=stu_choice,
                    action=act_choice,
                    target_concept_id=target_choice,
                    reason=reason_input,
                    teacher_id="TEACHER_SHUKLA",
                )
                st.success(f"✅ Override Recorded (Audit ID: {rec_id}) for {cohort[stu_choice]['name']}. Set to {act_choice} on {target_choice}.")
                st.rerun()

        with btn_col2:
            if st.button("🔄 Deactivate Active Override for Student", use_container_width=True):
                active = override_mgr.get_active_override(stu_choice)
                if active:
                    override_mgr.deactivate_override(active["id"])
                    st.info(f"Deactivated active override for {cohort[stu_choice]['name']}.")
                    st.rerun()
                else:
                    st.warning("No active override found for this student.")
        st.markdown('</div>', unsafe_allow_html=True)

    # Immutable SQLite Audit Log Table
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin: 24px 0 10px 0;">
        <h4 style="font-family: 'Space Grotesk', sans-serif; color: #38BDF8; margin: 0; font-size: 1.15rem; font-weight: 800;">
            📋 SQLite Audit Log: Chronological Human Governance Trail
        </h4>
        <span style="font-size: 0.72rem; color: #64748B; font-family: monospace;">
            TABLE: teacher_overrides
        </span>
    </div>
    """, unsafe_allow_html=True)
    logs = override_mgr.get_override_audit_log()
    if logs:
        st.dataframe(logs, use_container_width=True)
    else:
        st.info("No teacher overrides recorded yet in SQLite.")

    # 1-Click Database Reset for Live Judges
    st.markdown("<hr style='border: 0; border-top: 1px solid rgba(255,255,255,0.06); margin: 24px 0 16px 0;'>", unsafe_allow_html=True)
    c_rst1, c_rst2 = st.columns([3, 1])
    with c_rst1:
        st.caption("⚡ **Live Presentation Utility:** Reset and re-seed the SQLite database with 8 authentic cognitive archetypes and interaction histories.")
    with c_rst2:
        if st.button("🔄 Re-Seed SQLite DB", use_container_width=True):
            try:
                from backend.api.seed_data import seed_database
            except ImportError:
                from masteryflow.api.seed_data import seed_database
            seed_database("masteryflow.db")
            st.success("✅ Database refreshed with full 8-persona cohort!")
            st.rerun()


if __name__ == "__main__":
    render_teacher_dashboard()
