"""MasteryFlow Dedicated Teacher Command Center (teacher.py).

Role: Institutional-grade management deck for educators:
- Cohort Mastery Heatmap (Students x Concepts)
- Systemic Curricular Bottleneck Alerts
- Stuck-Learner Escalation Queue
- Direct Learning Path Override Console
- Chronological SQLite Audit Log
- Simulated Inactivity Retention Decay Controls
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
    from frontend.components.theme import apply_theme, render_html
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
    from masteryflow.ui.components.theme import apply_theme, render_html


def get_default_teacher_cohort(subject_name: str = "Mathematics"):
    """Builds realistic cohort dataset with diverse student profiles for the selected subject."""
    try:
        from backend.engine.contracts import CANONICAL_CONCEPTS
        from data.curricula import get_subject_concepts
        cur_concepts = get_subject_concepts(subject_name)
        concept_cids = list(cur_concepts.keys()) if cur_concepts else list(CANONICAL_CONCEPTS.keys())
    except Exception:
        concept_cids = list(CANONICAL_CONCEPTS.keys())

    cohort = {}
    base_map = lambda: {cid: ConceptMastery(concept_id=cid, p_raw=0.10, p_eff=0.10) for cid in concept_cids}

    # Fetch from SQLite database if available
    try:
        import sqlite3
        conn = sqlite3.connect("masteryflow.db")
        cur = conn.cursor()
        target_sids = ["STU_001", "STU_002", "STU_042", "STU_004", "STU_005", "STU_008"]
        q_marks = ",".join("?" for _ in target_sids)
        cur.execute(f"SELECT student_id, name FROM students WHERE student_id IN ({q_marks})", target_sids)
        stu_rows = cur.fetchall()

        for sid, sname in stu_rows:
            cohort[sid] = {"name": sname, "mastery": base_map()}
            c_marks = ",".join("?" for _ in concept_cids)
            cur.execute(f"SELECT concept_id, p, p_eff, status FROM student_mastery WHERE student_id = ? AND concept_id IN ({c_marks})", [sid] + concept_cids)
            for cid, p_raw, p_eff, status in cur.fetchall():
                if cid in cohort[sid]["mastery"]:
                    cohort[sid]["mastery"][cid].p_raw = float(p_raw)
                    cohort[sid]["mastery"][cid].p_eff = float(p_eff)
                    cohort[sid]["mastery"][cid].was_mastered = (status == "mastered" or float(p_eff) >= 0.85)
        conn.close()
        if cohort and len(cohort) >= 3:
            return cohort
    except Exception:
        pass

    # 1. Priya Singh (High Performer)
    cohort["STU_001"] = {"name": "Priya Singh", "mastery": base_map()}
    if "C1" in cohort["STU_001"]["mastery"]:
        cohort["STU_001"]["mastery"]["C1"].p_eff = 0.95
        cohort["STU_001"]["mastery"]["C1"].was_mastered = True
    if "C2" in cohort["STU_001"]["mastery"]:
        cohort["STU_001"]["mastery"]["C2"].p_eff = 0.92
        cohort["STU_001"]["mastery"]["C2"].was_mastered = True
    if "C3" in cohort["STU_001"]["mastery"]:
        cohort["STU_001"]["mastery"]["C3"].p_eff = 0.88
        cohort["STU_001"]["mastery"]["C3"].was_mastered = True

    # 2. Aarav Patel (Stuck Learner - Plateau on C2)
    cohort["STU_002"] = {"name": "Aarav Patel", "mastery": base_map()}
    if "C1" in cohort["STU_002"]["mastery"]:
        cohort["STU_002"]["mastery"]["C1"].p_eff = 0.85
        cohort["STU_002"]["mastery"]["C1"].was_mastered = True
    if "C2" in cohort["STU_002"]["mastery"]:
        cohort["STU_002"]["mastery"]["C2"].p_eff = 0.40
        cohort["STU_002"]["mastery"]["C2"].history_p = [0.38, 0.39, 0.39, 0.40]
        cohort["STU_002"]["mastery"]["C2"].attempts_count = 6
        cohort["STU_002"]["mastery"]["C2"].errors_count = 4

    # 3. Diya Sharma (Foundational Gap on C2, Active on C7)
    cohort["STU_003"] = {"name": "Diya Sharma", "mastery": base_map()}
    if "C1" in cohort["STU_003"]["mastery"]:
        cohort["STU_003"]["mastery"]["C1"].p_eff = 0.88
        cohort["STU_003"]["mastery"]["C1"].was_mastered = True
    if "C2" in cohort["STU_003"]["mastery"]:
        cohort["STU_003"]["mastery"]["C2"].p_eff = 0.42

    # 4. Kabir Khan (Weak on C2)
    cohort["STU_004"] = {"name": "Kabir Khan", "mastery": base_map()}
    if "C1" in cohort["STU_004"]["mastery"]:
        cohort["STU_004"]["mastery"]["C1"].p_eff = 0.78
    if "C2" in cohort["STU_004"]["mastery"]:
        cohort["STU_004"]["mastery"]["C2"].p_eff = 0.38

    # 5. Rohan Verma (Decayed on C1)
    cohort["STU_005"] = {"name": "Rohan Verma", "mastery": base_map()}
    if "C1" in cohort["STU_005"]["mastery"]:
        cohort["STU_005"]["mastery"]["C1"].p_eff = 0.48
        cohort["STU_005"]["mastery"]["C1"].was_mastered = True
    if "C2" in cohort["STU_005"]["mastery"]:
        cohort["STU_005"]["mastery"]["C2"].p_eff = 0.82
        cohort["STU_005"]["mastery"]["C2"].was_mastered = True

    # 6. Ananya Sen (Solid on C1 & C2)
    cohort["STU_006"] = {"name": "Ananya Sen", "mastery": base_map()}
    if "C1" in cohort["STU_006"]["mastery"]:
        cohort["STU_006"]["mastery"]["C1"].p_eff = 0.90
        cohort["STU_006"]["mastery"]["C1"].was_mastered = True
    if "C2" in cohort["STU_006"]["mastery"]:
        cohort["STU_006"]["mastery"]["C2"].p_eff = 0.86
        cohort["STU_006"]["mastery"]["C2"].was_mastered = True

    return cohort


def render_teacher_dashboard():
    """Main rendering routine for the Teacher Command Center in clean light design."""
    try:
        st.set_page_config(page_title="MasteryFlow — Teacher Dashboard", page_icon=None, layout="wide")
    except Exception:
        pass

    apply_theme()

    cur_subject = st.session_state.get("active_subject", "Mathematics")

    # Teacher Hero Header
    render_html(f"""
    <div style="
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid rgba(228, 221, 211, 0.9);
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
                    background: #11141D;
                    color: #FFFFFF;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 1.15rem;
                    font-weight: 800;
                    box-shadow: 0 4px 14px rgba(17, 20, 29, 0.18);
                ">TC</div>
                <div>
                    <h1 style="color: #11141D; margin: 0; font-size: 1.6rem; font-weight: 800; letter-spacing: -0.02em;">
                        Teacher Command Center
                    </h1>
                    <div style="font-size: 0.84rem; color: #78716C; margin-top: 2px;">
                        Cohort Mastery &middot; Curricular Bottleneck Alerts &middot; Human-in-the-Loop Override
                    </div>
                </div>
            </div>
        </div>
        <div style="text-align: right;">
            <span style="
                background: #E8F7F0;
                color: #047857;
                border: 1px solid rgba(5, 150, 105, 0.35);
                font-size: 0.72rem;
                font-weight: 700;
                padding: 5px 14px;
                border-radius: 9999px;
            ">
                ● Educator Portal Active
            </span>
            <div style="font-size: 0.76rem; color: #78716C; margin-top: 3px;">
                Teacher: TEACHER_SHUKLA &middot; {cur_subject}
            </div>
        </div>
    </div>
    """)

    try:
        from backend.engine.contracts import get_subject_curriculum_graph
        graph = get_subject_curriculum_graph(cur_subject)
    except Exception:
        graph = CurriculumGraph(CANONICAL_CONCEPTS)

    override_mgr = OverrideManager("masteryflow.db")
    cohort = get_default_teacher_cohort(cur_subject)

    # Time Travel Clock Slider in Teacher Deck
    with st.expander("Cohort Retention Simulator (Simulate Inactivity Decay Across Cohort)", expanded=False):
        render_html(
            "<p style='font-size: 0.84rem; color: #78716C; margin-bottom: 8px;'>"
            "Advance the simulated clock by N days to observe how forgetting curves impact student mastery across the cohort:"
            "</p>"
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

    # Direct Teacher Override Console
    render_html("""
    <div style="margin-top: 26px; margin-bottom: 12px;">
        <div style="display: flex; align-items: center; gap: 8px;">
            <h3 style="color: #11141D; margin: 0; font-size: 1.25rem; font-weight: 800;">
                Teacher Learning Path Override
            </h3>
        </div>
        <p style="font-size: 0.84rem; color: #78716C; margin: 3px 0 0 0;">
            Manually assign a topic or action for any student. Overrides take precedence over automated recommendations.
        </p>
    </div>
    """)

    cur_subject = st.session_state.get("active_subject", "Mathematics")
    try:
        from data.curricula import get_subject_concepts
        subj_concepts_dict = get_subject_concepts(cur_subject)
        available_concepts = list(subj_concepts_dict.keys()) if subj_concepts_dict else list(CANONICAL_CONCEPTS.keys())
    except Exception:
        available_concepts = list(CANONICAL_CONCEPTS.keys())

    with st.container(border=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            stu_choice = st.selectbox("Select Student to Override:", list(cohort.keys()), format_func=lambda k: f"{cohort[k]['name']} ({k})")
        with c2:
            act_choice = st.selectbox("Assign Pedagogical Action:", [a.value for a in ActionType])
        with c3:
            target_choice = st.selectbox("Target Concept Node:", available_concepts, index=0)

        reason_input = st.text_input("Pedagogical Rationale for Audit Log:", "Identified foundational misconception in classroom check; assigned targeted practice.")

        btn_col1, btn_col2 = st.columns([1, 1])
        with btn_col1:
            if st.button("Apply & Record Override", type="primary", use_container_width=True):
                rec_id = override_mgr.record_override(
                    student_id=stu_choice,
                    action=act_choice,
                    target_concept_id=target_choice,
                    reason=reason_input,
                    teacher_id="TEACHER_SHUKLA",
                )
                st.success(f"Override Recorded (ID: {rec_id}) for {cohort[stu_choice]['name']}: {act_choice} on {target_choice}.")
                st.rerun()

        with btn_col2:
            if st.button("Clear Active Override", use_container_width=True):
                active = override_mgr.get_active_override(stu_choice)
                if active:
                    override_mgr.deactivate_override(active["id"])
                    st.info(f"Cleared override for {cohort[stu_choice]['name']}.")
                    st.rerun()
                else:
                    st.warning("No active override found for this student.")

    # Override History Table
    render_html("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin: 24px 0 10px 0;">
        <h4 style="color: #11141D; margin: 0; font-size: 1.05rem; font-weight: 800;">
            Teacher Override History
        </h4>
        <span style="font-size: 0.74rem; color: #78716C;">
            Recorded in SQLite
        </span>
    </div>
    """)
    logs = override_mgr.get_override_audit_log()
    if logs:
        st.dataframe(logs, use_container_width=True)
    else:
        st.info("No teacher overrides recorded yet.")

    # =========================================================================
    # Student & Cohort Data Export Desk (CSV / Excel)
    # =========================================================================
    render_html("""
    <div style="margin: 34px 0 14px 0; border-top: 1px solid rgba(228, 221, 211, 0.9); padding-top: 24px;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
            <div>
                <h3 style="color: #11141D; margin: 0; font-size: 1.25rem; font-weight: 800; letter-spacing: -0.02em;">
                    Student &amp; Cohort Data Export Desk (CSV / Excel)
                </h3>
                <p style="font-size: 0.82rem; color: #78716C; margin: 3px 0 0 0;">
                    Generate and download official CSV and Excel-compatible transcripts, cohort mastery matrices, and anti-gaming telemetry logs.
                </p>
            </div>
            <div style="display: flex; gap: 6px;">
                <span style="background: #F4EEE5; color: #11141D; font-size: 0.70rem; font-weight: 700; padding: 4px 10px; border-radius: 9999px; border: 1px solid #E5DCD0;">UTF-8 BOM</span>
                <span style="background: #E8F7F0; color: #047857; font-size: 0.70rem; font-weight: 700; padding: 4px 10px; border-radius: 9999px; border: 1px solid #A7F3D0;">Excel Compatible</span>
                <span style="background: #EFF6FF; color: #1D4ED8; font-size: 0.70rem; font-weight: 700; padding: 4px 10px; border-radius: 9999px; border: 1px solid #BFDBFE;">RFC 4180</span>
            </div>
        </div>
    </div>
    """)

    try:
        from frontend.components.export_service import (
            export_cohort_matrix_csv,
            export_classroom_attempts_csv,
            export_student_roster_summary_csv,
            export_teacher_overrides_csv,
        )
    except ImportError:
        from masteryflow.ui.components.export_service import (
            export_cohort_matrix_csv,
            export_classroom_attempts_csv,
            export_student_roster_summary_csv,
            export_teacher_overrides_csv,
        )

    # Generate the export datasets
    csv_matrix, fn_matrix = export_cohort_matrix_csv(cohort_dict=cohort)
    csv_roster, fn_roster = export_student_roster_summary_csv(cohort_dict=cohort)
    csv_attempts, fn_attempts = export_classroom_attempts_csv()
    csv_overrides, fn_overrides = export_teacher_overrides_csv()

    # 4 Export Cards
    c_exp1, c_exp2 = st.columns(2)
    with c_exp1:
        st.markdown("""
        <div style="background: #FFFFFF; border: 1px solid rgba(228, 221, 211, 0.9); border-radius: 16px; padding: 18px 20px; box-shadow: 0 4px 16px -2px rgba(60, 50, 30, 0.03); margin-bottom: 12px;">
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 8px;">
                <span style="font-size: 0.70rem; font-weight: 800; background: #11141D; color: #FFFFFF; padding: 2px 8px; border-radius: 6px;">COHORT MATRIX</span>
                <span style="font-size: 0.70rem; color: #78716C; font-weight: 600;">Students x 10 Concepts</span>
            </div>
            <div style="font-size: 1.05rem; font-weight: 800; color: #11141D; margin-bottom: 4px;">
                Cohort Mastery Matrix
            </div>
            <div style="font-size: 0.78rem; color: #78716C; line-height: 1.45; margin-bottom: 4px;">
                Complete grid mapping every student against all 10 concepts with effective retention, status, certified counts, and fragile prerequisite gaps.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.download_button(
            label=f"Download Cohort Matrix ({fn_matrix})",
            data=csv_matrix,
            file_name=fn_matrix,
            mime="text/csv",
            use_container_width=True,
            type="primary"
        )

    with c_exp2:
        st.markdown("""
        <div style="background: #FFFFFF; border: 1px solid rgba(228, 221, 211, 0.9); border-radius: 16px; padding: 18px 20px; box-shadow: 0 4px 16px -2px rgba(60, 50, 30, 0.03); margin-bottom: 12px;">
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 8px;">
                <span style="font-size: 0.70rem; font-weight: 800; background: #0E7490; color: #FFFFFF; padding: 2px 8px; border-radius: 6px;">ROSTER SUMMARY</span>
                <span style="font-size: 0.70rem; color: #78716C; font-weight: 600;">Executive Overview</span>
            </div>
            <div style="font-size: 1.05rem; font-weight: 800; color: #11141D; margin-bottom: 4px;">
                Student Performance &amp; Risk Roster
            </div>
            <div style="font-size: 0.78rem; color: #78716C; line-height: 1.45; margin-bottom: 4px;">
                Classroom roster summarizing cognitive readiness averages, certification counts, fragile bottleneck counts, and practice streaks.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.download_button(
            label=f"Download Student Roster ({fn_roster})",
            data=csv_roster,
            file_name=fn_roster,
            mime="text/csv",
            use_container_width=True
        )

    c_exp3, c_exp4 = st.columns(2)
    with c_exp3:
        st.markdown("""
        <div style="background: #FFFFFF; border: 1px solid rgba(228, 221, 211, 0.9); border-radius: 16px; padding: 18px 20px; box-shadow: 0 4px 16px -2px rgba(60, 50, 30, 0.03); margin-bottom: 12px;">
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 8px;">
                <span style="font-size: 0.70rem; font-weight: 800; background: #047857; color: #FFFFFF; padding: 2px 8px; border-radius: 6px;">TELEMETRY</span>
                <span style="font-size: 0.70rem; color: #78716C; font-weight: 600;">Classroom Audit</span>
            </div>
            <div style="font-size: 1.05rem; font-weight: 800; color: #11141D; margin-bottom: 4px;">
                Practice Telemetry &amp; Anti-Gaming Log
            </div>
            <div style="font-size: 0.78rem; color: #78716C; line-height: 1.45; margin-bottom: 4px;">
                Granular attempt history across all learners with millisecond latencies, hint deductions, Bayesian evidence weights, and anti-gaming clamp flags.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.download_button(
            label=f"Download Telemetry Log ({fn_attempts})",
            data=csv_attempts,
            file_name=fn_attempts,
            mime="text/csv",
            use_container_width=True
        )

    with c_exp4:
        st.markdown("""
        <div style="background: #FFFFFF; border: 1px solid rgba(228, 221, 211, 0.9); border-radius: 16px; padding: 18px 20px; box-shadow: 0 4px 16px -2px rgba(60, 50, 30, 0.03); margin-bottom: 12px;">
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 8px;">
                <span style="font-size: 0.70rem; font-weight: 800; background: #6D28D9; color: #FFFFFF; padding: 2px 8px; border-radius: 6px;">GOVERNANCE</span>
                <span style="font-size: 0.70rem; color: #78716C; font-weight: 600;">SQLite Audit Log</span>
            </div>
            <div style="font-size: 1.05rem; font-weight: 800; color: #11141D; margin-bottom: 4px;">
                Teacher Override Audit Trail
            </div>
            <div style="font-size: 0.78rem; color: #78716C; line-height: 1.45; margin-bottom: 4px;">
                Official compliance record of all instructor learning path overrides, assigned actions, timestamps, and pedagogical rationales.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.download_button(
            label=f"Download Override Audit Log ({fn_overrides})",
            data=csv_overrides,
            file_name=fn_overrides,
            mime="text/csv",
            use_container_width=True
        )

    # Interactive Previews for Teachers
    with st.expander("Preview Export Datasets Before Downloading", expanded=False):
        import io, csv as py_csv
        import pandas as pd
        t_prev1, t_prev2, t_prev3, t_prev4 = st.tabs([
            "Cohort Matrix Preview",
            "Student Roster Preview",
            "Telemetry Log Preview",
            "Override Audit Preview"
        ])
        with t_prev1:
            f1 = io.StringIO(csv_matrix.lstrip("\ufeff"))
            rows1 = [r for r in py_csv.reader(f1) if r and not r[0].startswith("#")]
            if len(rows1) > 1:
                st.dataframe(pd.DataFrame(rows1[1:], columns=rows1[0]), use_container_width=True, hide_index=True)
            else:
                st.info("No cohort matrix data available to preview.")
        with t_prev2:
            f2 = io.StringIO(csv_roster.lstrip("\ufeff"))
            rows2 = [r for r in py_csv.reader(f2) if r and not r[0].startswith("#")]
            if len(rows2) > 1:
                st.dataframe(pd.DataFrame(rows2[1:], columns=rows2[0]), use_container_width=True, hide_index=True)
            else:
                st.info("No roster data available to preview.")
        with t_prev3:
            f3 = io.StringIO(csv_attempts.lstrip("\ufeff"))
            rows3 = [r for r in py_csv.reader(f3) if r and not r[0].startswith("#")]
            if len(rows3) > 1:
                st.dataframe(pd.DataFrame(rows3[1:], columns=rows3[0]), use_container_width=True, hide_index=True)
            else:
                st.info("No telemetry attempts available to preview.")
        with t_prev4:
            f4 = io.StringIO(csv_overrides.lstrip("\ufeff"))
            rows4 = [r for r in py_csv.reader(f4) if r and not r[0].startswith("#")]
            if len(rows4) > 1:
                st.dataframe(pd.DataFrame(rows4[1:], columns=rows4[0]), use_container_width=True, hide_index=True)
            else:
                st.info("No overrides recorded yet.")

    # Reset Data Utility
    st.markdown("<hr style='border: 0; border-top: 1px solid rgba(148, 163, 184, 0.16); margin: 22px 0 14px 0;'>", unsafe_allow_html=True)
    c_rst1, c_rst2 = st.columns([3, 1])

    with c_rst1:
        st.caption("Reset and re-seed the cohort database with standard student profiles and practice histories.")
    with c_rst2:
        if st.button("Re-Seed Cohort Data", use_container_width=True):
            try:
                from backend.api.seed_data import seed_database
            except ImportError:
                from masteryflow.api.seed_data import seed_database
            seed_database("masteryflow.db")
            st.success("Database refreshed with cohort profiles!")
            st.rerun()


if __name__ == "__main__":
    render_teacher_dashboard()
