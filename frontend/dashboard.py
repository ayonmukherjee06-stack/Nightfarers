"""MasteryFlow Student Dashboard (dashboard.py).

Apitex Edition: Provides an executive learning overview for students inspired by the
Apitex Mobile Banking & Fintech UI template:
- Signature Cognitive Platinum Passport card widget
- Quick action capsules (Practice, Review, Agency)
- Quick learner avatar switcher ("Quick inspect learner profile")
- Clean porcelain white topic overview cards with smooth rounded progress meters
"""

from pathlib import Path
import streamlit as st
import json

BASE_DIR = Path(__file__).resolve().parent.parent
db_file = str(BASE_DIR / "masteryflow.db")
concepts_file = str(BASE_DIR / "data" / "concepts.json")

try:
    from backend.api.db import init_db
    from backend.engine.graph import load_concept_graph
except ImportError:
    try:
        from api.db import init_db
        from engine.graph import load_concept_graph
    except ImportError:
        from masteryflow.backend.api.db import init_db
        from masteryflow.backend.engine.graph import load_concept_graph

try:
    from frontend.components.universe_3d import render_3d_universe_widget
    from frontend.components.theme import (
        apply_theme,
        render_html,
        render_apitex_passport_card,
        render_apitex_quick_actions
    )
except ImportError:
    from masteryflow.ui.components.universe_3d import render_3d_universe_widget
    from masteryflow.ui.components.theme import (
        apply_theme,
        render_html,
        render_apitex_passport_card,
        render_apitex_quick_actions
    )


def get_status_color(status, is_fragile):
    if is_fragile:
        return "#E11D48"  # Soft rose
    elif status == "mastered":
        return "#059669"  # Soft emerald
    elif status == "practicing":
        return "#11141D"  # Deep obsidian
    elif status == "provisional":
        return "#D97706"  # Warm amber
    else:
        return "#78716C"  # Warm slate


def get_status_badge(status, is_fragile):
    color = get_status_color(status, is_fragile)
    label = "Prereq Gap" if is_fragile else status.capitalize()
    if label == "Unseen":
        label = "Upcoming"
    
    bg_color = "#FFE4E6" if is_fragile else (
        "#E8F7F0" if status == "mastered" else (
            "#F4EEE5" if status == "practicing" else (
                "#FEF3C7" if status == "provisional" else "#F5EFE6"
            )
        )
    )
    border_color = "#FECDD3" if is_fragile else (
        "#A7F3D0" if status == "mastered" else (
            "#E5DCD0" if status == "practicing" else (
                "#FDE68A" if status == "provisional" else "#E8E0D4"
            )
        )
    )
    return f"""<span style='background-color: {bg_color}; color: {color}; padding: 3px 10px; border-radius: 9999px; font-size: 0.70rem; border: 1px solid {border_color}; font-weight: 700;'>{label}</span>"""


def render_student_dashboard():
    apply_theme()

    local_db = init_db(db_file)
    cur_subject = st.session_state.get("active_subject", "Mathematics")
    try:
        from backend.engine.contracts import get_subject_curriculum_graph
        local_graph = get_subject_curriculum_graph(cur_subject)
    except Exception:
        try:
            from masteryflow.engine.contracts import get_subject_curriculum_graph
            local_graph = get_subject_curriculum_graph(cur_subject)
        except Exception:
            local_graph = load_concept_graph(concepts_file)

    if 'student_id' not in st.session_state:
        st.session_state.student_id = "STU_042"

    student_id = st.session_state.student_id

    student = local_db.get_student(student_id)
    if not student:
        st.error(f"Student {student_id} not found.")
        return

    student_name = student.get("name", "Student")
    mastery_map = local_db.get_student_mastery_map(student_id)
    concepts = local_db.get_all_concepts()

    if not concepts:
        st.warning("No concepts found in database.")
        return

    subject_concepts = [c for c in concepts if c.get("subject", "Mathematics") == cur_subject]
    if not subject_concepts:
        subject_concepts = [c for c in concepts if c.get("subject", "Mathematics") == "Mathematics"] or concepts

    total_p_eff = 0.0
    concepts_mastered = 0
    total_concepts = len(subject_concepts)

    for c in subject_concepts:
        cid = c['concept_id']
        c_map = mastery_map.get(cid, {})
        p_eff = c_map.get('p_eff', 0.0)
        total_p_eff += p_eff

        status = c_map.get('status', 'unseen')
        transfer = c_map.get('transfer_passed', False)
        if p_eff >= 0.85 and transfer:
            concepts_mastered += 1

    avg_p_eff = total_p_eff / total_concepts if total_concepts > 0 else 0.0

    # 1. Signature Apitex Hero Card (Cognitive Platinum Passport)
    render_apitex_passport_card(
        student_id=student_id,
        student_name=student_name,
        p_eff=avg_p_eff,
        certified_count=concepts_mastered,
        total_count=total_concepts,
        status=f"Active Learner &middot; {cur_subject}"
    )

    # 2. Apitex Quick Action Row (3 obsidian capsules)
    render_apitex_quick_actions(
        act1_label="Next Recommended Exercise",
        act2_label="Ebbinghaus Spaced Review",
        act3_label="Student Agency & Voice"
    )

    # 3. Quick Learner Switcher Avatars (Apitex "Quick transfer to" avatar row)
    st.markdown("""
    <div style="margin: 18px 0 8px 0;">
        <span style="font-size: 0.82rem; font-weight: 700; color: #78716C; text-transform: uppercase; letter-spacing: 0.5px;">
            Quick switch learner profile:
        </span>
    </div>
    """, unsafe_allow_html=True)

    avatars = [
        ("STU_001", "Priya Singh", "Top"),
        ("STU_042", "Diya Sharma", "Prereq Gap"),
        ("STU_002", "Aarav Patel", "Plateau"),
        ("STU_004", "Kabir Verma", "Decay 21d"),
        ("STU_005", "Ananya Roy", "Balanced"),
        ("STU_006", "Rohan Mehta", "Guesser")
    ]

    av_cols = st.columns(len(avatars))
    for idx, (s_id, s_name, role) in enumerate(avatars):
        is_active = (s_id == student_id)
        with av_cols[idx]:
            border_style = "2px solid #11141D" if is_active else "1px solid rgba(220, 210, 195, 0.9)"
            bg_style = "#11141D" if is_active else "#FFFFFF"
            text_color = "#FFFFFF" if is_active else "#11141D"
            if st.button(f"{s_name.split()[0]}", key=f"btn_av_{s_id}", use_container_width=True):
                st.session_state.student_id = s_id
                st.session_state.student_name = s_name
                st.rerun()

    st.markdown("<hr style='border: 0; border-top: 1px solid rgba(228, 221, 211, 0.9); margin: 18px 0 22px 0;'>", unsafe_allow_html=True)

    # 4. Apitex Metric Tiles
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div class="mf-glass-card" style="padding: 18px 22px; text-align: center; min-height: 110px;">
            <div style="color: #78716C; font-size: 0.74rem; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px; margin-bottom: 4px;">Cognitive Readiness</div>
            <div style="color: #11141D; font-size: 2.2rem; font-weight: 900; letter-spacing: -0.03em;">{avg_p_eff*100:.1f}%</div>
            <div style="color: #78716C; font-size: 0.72rem; margin-top: 2px;">Average across {total_concepts} concepts</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="mf-glass-card" style="padding: 18px 22px; text-align: center; min-height: 110px;">
            <div style="color: #78716C; font-size: 0.74rem; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px; margin-bottom: 4px;">Concepts Certified</div>
            <div style="color: #059669; font-size: 2.2rem; font-weight: 900; letter-spacing: -0.03em;">{concepts_mastered} <span style="font-size: 1.1rem; color: #78716C; font-weight: 700;">/ {total_concepts}</span></div>
            <div style="color: #78716C; font-size: 0.72rem; margin-top: 2px;">Deep transfer verified</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        streak = student.get('streak', 0)
        st.markdown(f"""
        <div class="mf-glass-card" style="padding: 18px 22px; text-align: center; min-height: 110px;">
            <div style="color: #78716C; font-size: 0.74rem; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px; margin-bottom: 4px;">Learning Streak</div>
            <div style="color: #D97706; font-size: 2.2rem; font-weight: 900; letter-spacing: -0.03em;">{streak} <span style="font-size: 1.1rem; color: #78716C; font-weight: 700;">days</span></div>
            <div style="color: #78716C; font-size: 0.72rem; margin-top: 2px;">Active practice consistency</div>
        </div>
        """, unsafe_allow_html=True)

    # Multi-Disciplinary Course Progress Overview
    render_html("""
    <div style="margin: 28px 0 14px 0;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
            <div>
                <h3 style="color: #11141D; margin: 0; font-size: 1.25rem; font-weight: 800; letter-spacing: -0.02em;">
                    Multi-Disciplinary Course Progress
                </h3>
                <p style="font-size: 0.80rem; color: #78716C; margin: 2px 0 0 0;">
                    Real-time adaptive cognitive mastery tracking across all 5 academic curricula
                </p>
            </div>
            <span style="font-size: 0.72rem; color: #047857; background: #E8F7F0; padding: 4px 12px; border-radius: 9999px; font-weight: 700; border: 1px solid #A7F3D0;">
                5 Active Disciplines
            </span>
        </div>
    </div>
    """)

    all_subjects_meta = [
        ("Mathematics", "📐", ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10"]),
        ("Computer Networks", "🌐", ["CN1", "CN2", "CN3", "CN4", "CN5", "CN6", "CN7", "CN8"]),
        ("Artificial Intelligence", "🤖", ["AI1", "AI2", "AI3", "AI4", "AI5", "AI6", "AI7", "AI8"]),
        ("Formal Languages & Automata", "⚙️", ["FLA1", "FLA2", "FLA3", "FLA4", "FLA5", "FLA6", "FLA7", "FLA8"]),
        ("Biochemistry", "🧬", ["BIO1", "BIO2", "BIO3", "BIO4", "BIO5", "BIO6", "BIO7", "BIO8"]),
    ]

    p_cols = st.columns(5)
    for idx, (s_name, s_icon, s_cids) in enumerate(all_subjects_meta):
        s_m = [mastery_map.get(cid, {}) for cid in s_cids]
        s_done = sum(1 for m in s_m if m.get("status") == "mastered" or float(m.get("p_eff", 0)) >= 0.85)
        s_tot = len(s_cids)
        s_avg_p = (sum(float(m.get("p_eff", 0.30)) for m in s_m) / s_tot) * 100 if s_tot else 0
        s_pct = int(round((s_done / s_tot) * 100))
        is_cur = (s_name == cur_subject)

        card_bg = "#FFFFFF"
        border_st = "2px solid #11141D" if is_cur else "1px solid rgba(228, 221, 211, 0.9)"
        shadow_st = "0 8px 24px -2px rgba(17, 20, 29, 0.12)" if is_cur else "0 4px 16px -2px rgba(60, 50, 30, 0.04)"

        with p_cols[idx]:
            st.markdown(f"""
            <div style="background: {card_bg}; border: {border_st}; border-radius: 18px; padding: 14px 14px 12px 14px; min-height: 155px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: {shadow_st}; margin-bottom: 10px;">
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <span style="font-size: 1.25rem;">{s_icon}</span>
                        <span style="font-size: 0.64rem; font-weight: 700; background: {'#11141D' if is_cur else '#F4EEE5'}; color: {'#FFFFFF' if is_cur else '#11141D'}; padding: 2px 7px; border-radius: 9999px;">
                            {'Active' if is_cur else f'{s_done}/{s_tot}'}
                        </span>
                    </div>
                    <div style="font-size: 0.82rem; font-weight: 800; color: #11141D; line-height: 1.25; margin-bottom: 4px;">
                        {s_name}
                    </div>
                    <div style="font-size: 0.70rem; color: #78716C;">
                        Readiness: <strong style="color: #059669;">{s_avg_p:.0f}%</strong>
                    </div>
                </div>
                <div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.68rem; color: #78716C; margin-bottom: 3px;">
                        <span>{s_done}/{s_tot} Mastered</span>
                        <span style="font-weight: 700; color: #11141D;">{s_pct}%</span>
                    </div>
                    <div style="background: #EDE6DA; border-radius: 999px; height: 5px; overflow: hidden; margin-bottom: 6px;">
                        <div style="width: {s_pct}%; height: 100%; background: #059669; border-radius: 999px;"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if not is_cur:
                if st.button(f"Switch to {s_name}", key=f"btn_switch_subj_{idx}", use_container_width=True):
                    st.session_state.active_subject = s_name
                    default_cids = {
                        "Mathematics": "C1",
                        "Computer Networks": "CN1",
                        "Artificial Intelligence": "AI1",
                        "Formal Languages & Automata": "FLA1",
                        "Biochemistry": "BIO1"
                    }
                    new_cid = default_cids.get(s_name, "C1")
                    with local_db.conn:
                        local_db.conn.execute("UPDATE students SET active_concept_id = ? WHERE student_id = ?", (new_cid, student_id))
                    st.rerun()

    # 5. 3D Curriculum Sphere Map
    concepts_meta = {}
    for c in subject_concepts:
        cid = c.get('concept_id') or c.get('id')
        c_dict = dict(c)
        c_dict["id"] = cid
        c_dict["concept_id"] = cid
        prereqs = []
        if hasattr(local_graph, "get_prerequisites"):
            try:
                prereqs = local_graph.get_prerequisites(cid)
            except Exception:
                prereqs = []
        if not prereqs and "prerequisites" in c:
            prereqs = c.get("prerequisites", [])
        c_dict["prerequisites"] = prereqs
        concepts_meta[cid] = c_dict

    for cid in concepts_meta:
        if cid not in mastery_map:
            mastery_map[cid] = {"concept_id": cid, "p_eff": 0.30, "status": "unseen", "stability_days": 7.0}

    render_html("""
    <div style="display: flex; align-items: center; justify-content: space-between; padding: 12px 20px; margin: 16px 0 16px 0; background: #FFFFFF; border: 1px solid rgba(228, 221, 211, 0.9); border-radius: 9999px; font-size: 0.82rem; color: #11141D; box-shadow: 0 4px 16px -2px rgba(60, 50, 30, 0.03);">
        <div>
            <strong style="color: #11141D;">▲ 3D Universe:</strong> Interactive curriculum sphere map. Drag to orbit, scroll to zoom.
        </div>
        <div>
            <span style="color: #78716C;">Click any node to inspect pedagogical status.</span>
        </div>
    </div>
    """)

    curr_active_cid = student.get('active_concept_id')
    if not curr_active_cid or curr_active_cid not in concepts_meta:
        curr_active_cid = list(concepts_meta.keys())[0] if concepts_meta else 'C1'

    render_3d_universe_widget(
        concepts_meta=concepts_meta,
        mastery_map=mastery_map,
        active_concept_id=curr_active_cid,
        height=520
    )

    # 6. Apitex Concept Mastery Grid
    render_html(f"""
    <div style="margin: 24px 0 14px 0;">
        <h3 style="color: #11141D; margin: 0; font-size: 1.25rem; font-weight: 800;">
            Topic Overview &middot; {cur_subject}
        </h3>
        <p style="font-size: 0.80rem; color: #78716C; margin-top: 2px;">
            Current readiness level and retention stability across all {len(subject_concepts)} concepts
        </p>
    </div>
    """)

    sorted_concepts = sorted(subject_concepts, key=lambda x: x.get('order_index', 99))

    grid_cols = st.columns(min(len(sorted_concepts), 5) if sorted_concepts else 1)
    for i, concept in enumerate(sorted_concepts):
        col = grid_cols[i % len(grid_cols)]

        cid = concept.get('concept_id')
        name = concept.get('name', cid)

        c_map = mastery_map.get(cid, {})
        p_eff = c_map.get('p_eff', 0.0)
        status = c_map.get('status', 'unseen')
        is_fragile = c_map.get('is_fragile', False)
        stability = c_map.get('stability_days', 0)

        badge_html = get_status_badge(status, is_fragile)
        progress_color = get_status_color(status, is_fragile)

        with col:
            st.markdown(f"""
            <div style="background: #FFFFFF; border: 1px solid rgba(228, 221, 211, 0.9); border-radius: 18px; padding: 14px 16px; min-height: 155px; display: flex; flex-direction: column; justify-content: space-between; margin-bottom: 12px; box-shadow: 0 4px 16px -2px rgba(60, 50, 30, 0.03);">
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 6px;">
                        <div>{badge_html}</div>
                    </div>
                    <div style="color: #11141D; font-weight: 700; font-size: 0.90rem; margin-bottom: 3px; line-height: 1.25;">
                        {name}
                    </div>
                    <div style="color: #78716C; font-size: 0.72rem; margin-bottom: 8px;">
                        Retention: {stability:.1f}d
                    </div>
                </div>
                <div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.72rem; color: #78716C; margin-bottom: 3px;">
                        <span>Readiness</span>
                        <span style="font-weight: 700; color: #11141D;">{p_eff*100:.0f}%</span>
                    </div>
                    <div style="width: 100%; background-color: #EDE6DA; border-radius: 999px; height: 6px; overflow: hidden;">
                        <div style="width: {min(100, int(p_eff*100))}%; background-color: {progress_color}; height: 100%; border-radius: 999px; transition: width 0.3s ease;"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # 7. Student Data Export Desk (CSV / Excel)
    render_html("""
    <div style="margin: 32px 0 14px 0; border-top: 1px solid rgba(228, 221, 211, 0.9); padding-top: 24px;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
            <div>
                <h3 style="color: #11141D; margin: 0; font-size: 1.25rem; font-weight: 800; letter-spacing: -0.02em;">
                    Export Personal Learning Records (CSV / Excel)
                </h3>
                <p style="font-size: 0.82rem; color: #78716C; margin: 3px 0 0 0;">
                    Download certified mathematical mastery transcripts and practice telemetry for spreadsheet analysis or school records.
                </p>
            </div>
            <div style="display: flex; gap: 6px;">
                <span style="background: #F4EEE5; color: #11141D; font-size: 0.70rem; font-weight: 700; padding: 4px 10px; border-radius: 9999px; border: 1px solid #E5DCD0;">UTF-8 BOM</span>
                <span style="background: #E8F7F0; color: #047857; font-size: 0.70rem; font-weight: 700; padding: 4px 10px; border-radius: 9999px; border: 1px solid #A7F3D0;">Excel Ready</span>
            </div>
        </div>
    </div>
    """)

    try:
        from frontend.components.export_service import export_student_mastery_csv, export_student_attempts_csv
    except ImportError:
        from masteryflow.ui.components.export_service import export_student_mastery_csv, export_student_attempts_csv

    csv_portfolio, file_portfolio = export_student_mastery_csv(student_id, db=local_db)
    csv_attempts, file_attempts = export_student_attempts_csv(student_id, db=local_db)

    exp_col1, exp_col2 = st.columns(2)

    with exp_col1:
        st.markdown("""
        <div style="background: #FFFFFF; border: 1px solid rgba(228, 221, 211, 0.9); border-radius: 16px; padding: 18px 20px; box-shadow: 0 4px 16px -2px rgba(60, 50, 30, 0.03); margin-bottom: 12px;">
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 8px;">
                <span style="font-size: 0.70rem; font-weight: 800; background: #11141D; color: #FFFFFF; padding: 2px 8px; border-radius: 6px;">PORTFOLIO</span>
                <span style="font-size: 0.70rem; color: #78716C; font-weight: 600;">10 Concepts</span>
            </div>
            <div style="font-size: 1.05rem; font-weight: 800; color: #11141D; margin-bottom: 4px;">
                Concept Mastery Transcript
            </div>
            <div style="font-size: 0.78rem; color: #78716C; line-height: 1.45; margin-bottom: 4px;">
                Complete record of Bayesian mastery beliefs, retention stability half-lives, transfer verification, and prerequisite flags.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.download_button(
            label=f"Download Portfolio ({file_portfolio})",
            data=csv_portfolio,
            file_name=file_portfolio,
            mime="text/csv",
            use_container_width=True,
            type="primary"
        )

    with exp_col2:
        st.markdown("""
        <div style="background: #FFFFFF; border: 1px solid rgba(228, 221, 211, 0.9); border-radius: 16px; padding: 18px 20px; box-shadow: 0 4px 16px -2px rgba(60, 50, 30, 0.03); margin-bottom: 12px;">
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 8px;">
                <span style="font-size: 0.70rem; font-weight: 800; background: #0E7490; color: #FFFFFF; padding: 2px 8px; border-radius: 6px;">TELEMETRY</span>
                <span style="font-size: 0.70rem; color: #78716C; font-weight: 600;">Full Practice Log</span>
            </div>
            <div style="font-size: 1.05rem; font-weight: 800; color: #11141D; margin-bottom: 4px;">
                Practice Attempts & Telemetry History
            </div>
            <div style="font-size: 0.78rem; color: #78716C; line-height: 1.45; margin-bottom: 4px;">
                Itemized question responses with millisecond latency, hint usage counts, evidence weights, and anti-gaming audit stamps.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.download_button(
            label=f"Download Attempts ({file_attempts})",
            data=csv_attempts,
            file_name=file_attempts,
            mime="text/csv",
            use_container_width=True
        )

    # Preview Expander
    with st.expander("Preview Export Data Before Downloading", expanded=False):
        tab_p1, tab_p2 = st.tabs(["Mastery Portfolio Preview", "Practice Attempts Preview"])
        with tab_p1:
            import io, csv as py_csv
            f_prev1 = io.StringIO(csv_portfolio.lstrip("\ufeff"))
            r_prev1 = list(py_csv.reader(f_prev1))
            data_rows1 = [r for r in r_prev1 if r and not r[0].startswith("#")]
            if len(data_rows1) > 1:
                import pandas as pd
                df1 = pd.DataFrame(data_rows1[1:], columns=data_rows1[0])
                st.dataframe(df1, use_container_width=True, hide_index=True)
            else:
                st.info("No mastery records available to preview.")
        with tab_p2:
            import io, csv as py_csv
            f_prev2 = io.StringIO(csv_attempts.lstrip("\ufeff"))
            r_prev2 = list(py_csv.reader(f_prev2))
            data_rows2 = [r for r in r_prev2 if r and not r[0].startswith("#")]
            if len(data_rows2) > 1:
                import pandas as pd
                df2 = pd.DataFrame(data_rows2[1:], columns=data_rows2[0])
                st.dataframe(df2, use_container_width=True, hide_index=True)
            else:
                st.info("No practice attempts recorded yet for this profile. Solve questions in the Learn portal to generate telemetry data.")


if __name__ == "__main__":
    render_student_dashboard()

