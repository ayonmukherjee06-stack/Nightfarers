"""MasteryFlow Interactive Live Demo Application.

Role: Real-time interactive UI demonstrating the deterministic 6-rule decision engine,
Glass-Box explainability, teacher cohort heatmap, curriculum bottleneck alerts, and live Test 8 reproducibility.
"""

from __future__ import annotations
import streamlit as st
import json
import copy

try:
    from backend.engine.contracts import (
        CurriculumGraph,
        EngineConfig,
        ConceptMastery,
        ActionType,
        CANONICAL_CONCEPTS,
    )
    from backend.engine.decide import (
        make_decision,
        reconstruct_decision_from_snapshot,
    )
    from backend.engine.override import OverrideManager
    from backend.engine.information_gain import compute_expected_information_gain, rank_items_by_information_gain
    from frontend.components.glassbox_card import render_glassbox_card
    from frontend.components.heatmap import render_cohort_heatmap, compute_cohort_metrics, detect_group_bottlenecks
    from frontend.components.time_travel import render_time_travel_slider, apply_time_travel_decay
    from frontend.components.agency_modal import render_agency_modal, StudentAgencyManager
    from frontend.components.theme import apply_theme, render_html, clean_html
except ImportError:
    from masteryflow.engine.contracts import (
        CurriculumGraph,
        EngineConfig,
        ConceptMastery,
        ActionType,
        CANONICAL_CONCEPTS,
    )
    from masteryflow.engine.decide import (
        make_decision,
        reconstruct_decision_from_snapshot,
    )
    from masteryflow.engine.override import OverrideManager
    from masteryflow.engine.information_gain import compute_expected_information_gain, rank_items_by_information_gain
    from masteryflow.ui.components.glassbox_card import render_glassbox_card
    from masteryflow.ui.components.heatmap import render_cohort_heatmap, compute_cohort_metrics, detect_group_bottlenecks
    from masteryflow.ui.components.time_travel import render_time_travel_slider, apply_time_travel_decay
    from masteryflow.ui.components.agency_modal import render_agency_modal, StudentAgencyManager
    from masteryflow.ui.components.theme import apply_theme, render_html, clean_html


st.set_page_config(
    page_title="MasteryFlow Engine — Live Interactive Demo",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_theme()

# Custom Header Styling
render_html("""
<div class="mf-glass-card" style="padding: 20px 24px; margin-bottom: 22px;">
    <div style="font-size: 26px; font-weight: 800; color: #F8FAFC; margin-bottom: 4px; letter-spacing: -0.02em;">
        MasteryFlow: <span style="color: #38BDF8;">Explainable Adaptive Learning Engine</span>
    </div>
    <div style="font-size: 13px; color: #94A3B8;">
        <strong style="color: #CBD5E1;">YUVA Megathon 2026</strong> | Domain 4: Intelligent Educational Systems | 
        <strong style="color: #38BDF8;">Autonomous Pedagogical Decision Engine</strong>
    </div>
</div>
""")

# Initialize Curriculum Graph & Config
graph = CurriculumGraph(CANONICAL_CONCEPTS)
config = EngineConfig()

def create_base_mastery_map():
    return {
        cid: ConceptMastery(concept_id=cid, p_raw=0.10, p_eff=0.10)
        for cid in CANONICAL_CONCEPTS
    }

# Build realistic 6-student cohort dataset
def get_live_cohort():
    cohort = {}
    
    # 1. Priya Singh (High Performer)
    cohort["STU_001"] = {
        "name": "Priya Singh",
        "mastery": create_base_mastery_map()
    }
    cohort["STU_001"]["mastery"]["C1"].p_eff = 0.95
    cohort["STU_001"]["mastery"]["C1"].was_mastered = True
    cohort["STU_001"]["mastery"]["C1"].transfer_verified = True
    cohort["STU_001"]["mastery"]["C2"].p_eff = 0.92
    cohort["STU_001"]["mastery"]["C2"].was_mastered = True
    cohort["STU_001"]["mastery"]["C3"].p_eff = 0.88
    cohort["STU_001"]["mastery"]["C3"].was_mastered = True

    # 2. Aarav Patel (Stuck Learner - Cognitive Plateau on C2)
    cohort["STU_002"] = {
        "name": "Aarav Patel",
        "mastery": create_base_mastery_map()
    }
    cohort["STU_002"]["mastery"]["C1"].p_eff = 0.85
    cohort["STU_002"]["mastery"]["C1"].was_mastered = True
    cohort["STU_002"]["mastery"]["C2"].p_eff = 0.40
    cohort["STU_002"]["mastery"]["C2"].history_p = [0.38, 0.39, 0.39, 0.40]
    cohort["STU_002"]["mastery"]["C2"].attempts_count = 6
    cohort["STU_002"]["mastery"]["C2"].errors_count = 4

    # 3. Diya Sharma (Foundational Gap: C7 active, C2 weak)
    cohort["STU_003"] = {
        "name": "Diya Sharma",
        "mastery": create_base_mastery_map()
    }
    cohort["STU_003"]["mastery"]["C1"].p_eff = 0.88
    cohort["STU_003"]["mastery"]["C1"].was_mastered = True
    cohort["STU_003"]["mastery"]["C2"].p_eff = 0.42
    cohort["STU_003"]["mastery"]["C5"].p_eff = 0.65
    cohort["STU_003"]["mastery"]["C6"].p_eff = 0.60
    cohort["STU_003"]["mastery"]["C7"].p_eff = 0.48
    cohort["STU_003"]["mastery"]["C7"].errors_count = 2
    cohort["STU_003"]["mastery"]["C7"].hints_count = 2

    # 4. Kabir Khan (Also weak on C2)
    cohort["STU_004"] = {
        "name": "Kabir Khan",
        "mastery": create_base_mastery_map()
    }
    cohort["STU_004"]["mastery"]["C1"].p_eff = 0.78
    cohort["STU_004"]["mastery"]["C2"].p_eff = 0.38
    cohort["STU_004"]["mastery"]["C3"].p_eff = 0.30

    # 5. Rohan Verma (Memory Decay on C1)
    cohort["STU_005"] = {
        "name": "Rohan Verma",
        "mastery": create_base_mastery_map()
    }
    cohort["STU_005"]["mastery"]["C1"].p_eff = 0.48
    cohort["STU_005"]["mastery"]["C1"].was_mastered = True
    cohort["STU_005"]["mastery"]["C2"].p_eff = 0.82
    cohort["STU_005"]["mastery"]["C2"].was_mastered = True
    cohort["STU_005"]["mastery"]["C3"].p_eff = 0.70

    # 6. Ananya Sen (Solid on C1 & C2)
    cohort["STU_006"] = {
        "name": "Ananya Sen",
        "mastery": create_base_mastery_map()
    }
    cohort["STU_006"]["mastery"]["C1"].p_eff = 0.90
    cohort["STU_006"]["mastery"]["C1"].was_mastered = True
    cohort["STU_006"]["mastery"]["C2"].p_eff = 0.86
    cohort["STU_006"]["mastery"]["C2"].was_mastered = True
    cohort["STU_006"]["mastery"]["C4"].p_eff = 0.65

    return cohort

live_cohort = get_live_cohort()

# Primary Navigation Tabs
tab_student, tab_teacher, tab_architecture = st.tabs([
    "Student Experience & Glass-Box Explainability",
    "Teacher Command Center & Cohort Heatmap",
    "DAG Knowledge Graph & Test 8 Proofs",
])

# ==================== TAB 1: STUDENT VIEW ====================
with tab_student:
    st.sidebar.header("Student Simulator")
    persona_choice = st.sidebar.selectbox(
        "Select Active Learner:",
        [
            "Diya Sharma (Foundational Gap -> Remediate C2)",
            "Rohan Verma (Memory Decay -> Spaced Review C1)",
            "Aarav Patel (Cognitive Plateau -> Teacher Alert)",
            "Priya Singh (High Performer -> Advance to C2)",
            "Custom Interactive Sandbox",
        ],
        index=0,
    )

    # Configure student based on selection
    if "Diya" in persona_choice:
        student_id = "STU_003"
        student_name = "Diya Sharma"
        current_concept = "C7"
        student_mastery = copy.deepcopy(live_cohort[student_id]["mastery"])
        challenge_mode = False
    elif "Rohan" in persona_choice:
        student_id = "STU_005"
        student_name = "Rohan Verma"
        current_concept = "C3"
        student_mastery = copy.deepcopy(live_cohort[student_id]["mastery"])
        challenge_mode = False
    elif "Aarav" in persona_choice:
        student_id = "STU_002"
        student_name = "Aarav Patel"
        current_concept = "C2"
        student_mastery = copy.deepcopy(live_cohort[student_id]["mastery"])
        challenge_mode = False
    elif "Priya" in persona_choice:
        student_id = "STU_001"
        student_name = "Priya Singh"
        current_concept = "C1"
        student_mastery = copy.deepcopy(live_cohort[student_id]["mastery"])
        challenge_mode = False
    else:
        student_id = "STU_CUSTOM"
        student_name = "Custom Student"
        current_concept = st.sidebar.selectbox("Active Concept:", list(CANONICAL_CONCEPTS.keys()), index=1)
        challenge_mode = st.sidebar.checkbox("Challenge Mode", value=False)
        student_mastery = create_base_mastery_map()
        st.sidebar.markdown("---")
        st.sidebar.subheader("Adjust Concept Masteries (p_eff)")
        for cid in CANONICAL_CONCEPTS:
            val = st.sidebar.slider(f"{cid} Mastery", 0.0, 1.0, 0.50, 0.05)
            student_mastery[cid].p_eff = val
            if val >= 0.85:
                student_mastery[cid].was_mastered = True
                student_mastery[cid].transfer_verified = True

    # Check active teacher overrides
    override_mgr = OverrideManager("masteryflow.db")
    active_override = override_mgr.get_active_override(student_id)

    # Execute Engine Decision Live
    decision = make_decision(
        student_id=student_id,
        current_concept_id=current_concept,
        mastery_map=student_mastery,
        graph=graph,
        config=config,
        challenge_mode=challenge_mode,
        active_override=active_override,
    )

    if active_override:
        st.warning(
            f"**ACTIVE HUMAN OVERRIDE IN EFFECT:** Teacher `{active_override['teacher_id']}` has overridden "
            f"automated recommendations to enforce **{active_override['action']}** on **{active_override['target_concept_id']}**."
        )

    col1, col2 = st.columns([1.3, 1.0])
    with col1:
        st.subheader("Real-Time Engine Recommendation")
        render_glassbox_card(decision, graph=graph, student_name=student_name)

        st.markdown("### Active Concept Telemetry")
        m_curr = student_mastery[current_concept]
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Effective Mastery", f"{m_curr.p_eff * 100:.1f}%")
        c2.metric("Recent Errors", m_curr.errors_count)
        c3.metric("Hints Used", m_curr.hints_count)
        c4.metric("Transfer Status", "VERIFIED" if m_curr.transfer_verified else "PROVISIONAL")

        # Innovation (c): Student Agency Modal
        render_agency_modal(student_id=student_id, current_concept_id=current_concept, student_name=student_name)

        # Innovation (b): Information Gain Item Selection Preview
        st.markdown("---")
        st.subheader("Innovation (b): Information-Gain Adaptive Item Selection")
        st.caption("Bayesian Active Learning: selects questions that maximize expected Fisher information reduction.")
        sample_questions = [
            {"id": "Q1", "difficulty": 0.30, "prompt": f"Introductory check on {current_concept}"},
            {"id": "Q2", "difficulty": round(m_curr.p_eff, 2), "prompt": f"ZPD-matched diagnostic on {current_concept}"},
            {"id": "Q3", "difficulty": 0.85, "prompt": f"Advanced transfer challenge on {current_concept}"},
        ]
        ranked_qs = rank_items_by_information_gain(student_p=m_curr.p_eff, candidate_items=sample_questions)
        top_q = ranked_qs[0]
        st.success(
            f"**Optimal Question Selected:** `{top_q['id']}` (Difficulty: `{top_q['difficulty']:.2f}`, "
            f"Expected Information Gain: **{top_q['expected_ig']:.4f} bits**)\n\n"
            f"*Prompt:* \"{top_q['prompt']}\""
        )

    with col2:
        st.subheader("Individual Mastery Tree")
        for cid, meta in CANONICAL_CONCEPTS.items():
            m = student_mastery[cid]
            status_color = "#10B981" if m.was_mastered else ("#F59E0B" if m.p_eff >= 0.55 else "#EF4444")
            status_text = "Mastered" if m.was_mastered else ("In Progress" if m.p_eff >= 0.55 else "Gap (<55%)")

            render_html(
                f'<div class="mf-glass-card" style="border: 1px solid rgba(148, 163, 184, 0.16); border-radius: 8px; padding: 8px 12px; margin-bottom: 6px;">'
                f'<div style="display: flex; justify-content: space-between; align-items: center;">'
                f'<span style="font-weight: 600; font-size: 12px; color: #F8FAFC;"><strong style="color: #38BDF8;">{cid}</strong>: {meta["title"]}</span>'
                f'<span style="font-size: 11px; font-weight: 700; color: {status_color};">{status_text} ({m.p_eff*100:.0f}%)</span>'
                f'</div></div>'
            )
            st.progress(float(m.p_eff))

# ==================== TAB 2: TEACHER COMMAND CENTER ====================
with tab_teacher:
    st.subheader("Institutional Teacher Command Center")
    st.markdown("Live cohort monitoring, systemic bottleneck alerts, and stuck-learner escalation queue.")

    # Time Travel Expander in Teacher Deck
    with st.expander("Live Time Travel Controls (Ebbinghaus Retention Decay Simulator)", expanded=False):
        elapsed_days = render_time_travel_slider(default_days=0)
        if elapsed_days > 0:
            for s_id in live_cohort:
                for c_id in live_cohort[s_id]["mastery"]:
                    m_obj = live_cohort[s_id]["mastery"][c_id]
                    if m_obj.was_mastered:
                        m_obj.p_eff = apply_time_travel_decay(m_obj.p_eff, elapsed_days)

    render_cohort_heatmap(live_cohort, graph=graph)

    st.markdown("---")
    st.subheader("1-Click Human-in-the-Loop Override Console")
    st.caption("Teachers maintain final authority. Overrides are written to the audit log.")
    
    over_col1, over_col2, over_col3 = st.columns(3)
    with over_col1:
        override_stu = st.selectbox("Select Student to Override:", list(live_cohort.keys()), format_func=lambda k: f"{live_cohort[k]['name']} ({k})")
    with over_col2:
        override_action = st.selectbox("Action Override:", [a.value for a in ActionType])
    with over_col3:
        override_concept = st.selectbox("Target Concept Override:", list(CANONICAL_CONCEPTS.keys()), index=1)

    override_reason = st.text_input("Mandatory Pedagogical Reason for Audit Trail:", "Teacher observed foundational misconception during oral questioning.")
    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
        if st.button("Apply & Record Teacher Override", type="primary"):
            rec_id = override_mgr.record_override(
                student_id=override_stu,
                action=override_action,
                target_concept_id=override_concept,
                reason=override_reason,
                teacher_id="TEACHER_SHUKLA",
            )
            st.success(f"Override Recorded in SQLite Audit Trail (ID: {rec_id}): Set {live_cohort[override_stu]['name']} to {override_action} on {override_concept}.")
            st.rerun()

    with col_btn2:
        if st.button("Clear Active Override for Selected Student"):
            active = override_mgr.get_active_override(override_stu)
            if active:
                override_mgr.deactivate_override(active["id"])
                st.info(f"Cleared active override for {live_cohort[override_stu]['name']}.")
                st.rerun()

    st.markdown("### SQLite Audit Log: Chronological Human Overrides")
    audit_logs = override_mgr.get_override_audit_log()
    if audit_logs:
        st.dataframe(audit_logs, use_container_width=True)
    else:
        st.info("No teacher overrides recorded yet. Click 'Apply & Record Teacher Override' above to create the first persistent audit entry.")

    # Innovation (c) Table in Teacher Command Center
    st.markdown("### Student Agency Inbox: Self-Regulated Learning Requests")
    agency_mgr = StudentAgencyManager("masteryflow.db")
    agency_reqs = agency_mgr.get_student_agency_requests()
    if agency_reqs:
        st.dataframe(agency_reqs, use_container_width=True)
    else:
        st.caption("No student agency requests logged yet. Students can submit requests from Tab 1.")

# ==================== TAB 3: ARCHITECTURE & PROOFS ====================
with tab_architecture:
    st.subheader("Test 8: Decision Snapshot & Reproducibility Proof")
    st.caption("Recomputing next_action() from stored inputs_json must produce 100% identical outputs with zero variance.")

    if st.button("Run Test 8 Verification Live", type="primary"):
        reconstructed = reconstruct_decision_from_snapshot(decision.inputs_snapshot, graph)
        is_exact = (
            reconstructed.action == decision.action
            and reconstructed.target_concept_id == decision.target_concept_id
            and reconstructed.reason == decision.reason
        )
        if is_exact:
            st.success("**TEST 8 PASS:** Decision reconstructed with 100% deterministic fidelity from stored snapshot JSON!")
        else:
            st.error("Test 8 Failed: Inconsistency detected.")

    st.markdown("### Stored Inputs JSON Snapshot")
    st.json(decision.inputs_snapshot)

    st.markdown("---")
    st.subheader("The 10-Concept Fractions & Ratios DAG")
    for cid, data in CANONICAL_CONCEPTS.items():
        prereqs = data["prereqs"]
        prereq_str = ", ".join(prereqs) if prereqs else "None (Foundational Baseline)"
        st.markdown(f"**{cid} — {data['title']}** | Prereqs: `{prereq_str}`\n\n> {data['description']}")
