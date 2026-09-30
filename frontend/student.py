"""MasteryFlow: Student Glass-Box Adaptive Learning Portal.

Aesthetic: Modern 2026 Linear/Raycast Dark Glassmorphism, Live Telemetry HUD, Interactive 3D WebGL & DAG Roadmap.
Security: Zero eval/exec, parameterized queries, strict fraction regex parsing, and fault-tolerant backend connectivity.
"""

import json
import os
import random
import time
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List, Optional
import requests
import streamlit as st

# Add base paths to sys.path for clean, robust imports
import sys
BASE_DIR = Path(__file__).resolve().parent.parent
UI_DIR = Path(__file__).resolve().parent
BACKEND_DIR = BASE_DIR / "backend"
for p in [str(BASE_DIR), str(UI_DIR), str(BACKEND_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

# Import local components
try:
    from frontend.components.theme import (
        apply_theme,
        render_brand_header,
        render_circular_gauge,
        render_judge_demo_ribbon,
        render_apitex_passport_card,
        render_apitex_quick_actions
    )
    from frontend.components.math_parser import evaluate_student_answer, parse_fraction_input
    from frontend.components.glassbox_card import render_glassbox_card
    from frontend.components.dag_visualizer import render_dag_visualizer
    from frontend.components.universe_3d import render_3d_universe_widget
    from frontend.components.question_runner import render_question_runner
    from frontend.components.telemetry_card import render_telemetry_breakdown
    from frontend.components.agency_modal import render_agency_modal
    from frontend.components.video_recommender import (
        render_failure_remediation_card,
        render_concept_video_recommendation,
        render_subject_video_library
    )
except ModuleNotFoundError:
    try:
        from components.theme import apply_theme, render_brand_header, render_circular_gauge, render_judge_demo_ribbon
        from components.math_parser import evaluate_student_answer, parse_fraction_input
        from components.glassbox_card import render_glassbox_card
        from components.dag_visualizer import render_dag_visualizer
        from components.universe_3d import render_3d_universe_widget
        from components.question_runner import render_question_runner
        from components.telemetry_card import render_telemetry_breakdown
        from components.agency_modal import render_agency_modal
        from components.video_recommender import (
            render_failure_remediation_card,
            render_concept_video_recommendation,
            render_subject_video_library
        )
    except ModuleNotFoundError:
        from masteryflow.ui.components.theme import apply_theme, render_brand_header, render_circular_gauge, render_judge_demo_ribbon
        from masteryflow.ui.components.math_parser import evaluate_student_answer, parse_fraction_input
        from masteryflow.ui.components.glassbox_card import render_glassbox_card
        from masteryflow.ui.components.dag_visualizer import render_dag_visualizer
        from masteryflow.ui.components.universe_3d import render_3d_universe_widget
        from masteryflow.ui.components.question_runner import render_question_runner
        from masteryflow.ui.components.telemetry_card import render_telemetry_breakdown
        from masteryflow.ui.components.agency_modal import render_agency_modal
        from masteryflow.ui.components.video_recommender import (
            render_failure_remediation_card,
            render_concept_video_recommendation,
            render_subject_video_library
        )

try:
    from backend.engine.graph import load_concept_graph, PrerequisiteGraph
    from backend.engine.mastery import update_bkt, compute_uncertainty
    from backend.engine.weights import compute_evidence_weight
    from backend.engine.decay import compute_effective_mastery, update_stability
    from backend.engine.decide import next_action, StudentState, ConceptState
    from backend.engine.coldstart import DiagnosticEngine
    from backend.api.db import init_db, Database
except ImportError:
    try:
        from engine.graph import load_concept_graph, PrerequisiteGraph
        from engine.mastery import update_bkt, compute_uncertainty
        from engine.weights import compute_evidence_weight
        from engine.decay import compute_effective_mastery, update_stability
        from engine.decide import next_action, StudentState, ConceptState
        from engine.coldstart import DiagnosticEngine
        from api.db import init_db, Database
    except ImportError:
        from masteryflow.engine.graph import load_concept_graph, PrerequisiteGraph
        from masteryflow.engine.mastery import update_bkt, compute_uncertainty
        from masteryflow.engine.weights import compute_evidence_weight
        from masteryflow.engine.decay import compute_effective_mastery, update_stability
        from masteryflow.engine.decide import next_action, StudentState, ConceptState
        from masteryflow.engine.coldstart import DiagnosticEngine
        from masteryflow.api.db import init_db, Database

def clean_html(html_str: str) -> str:
    """Strips leading whitespace from every line and eliminates empty lines,
    preventing Streamlit's CommonMark parser from misinterpreting indented HTML as code blocks."""
    if not html_str:
        return ""
    return "\n".join(line.strip() for line in html_str.splitlines() if line.strip())


def render_html(html_str: str) -> None:
    """Safely renders HTML via st.markdown with zero risk of CommonMark code block conversion."""
    st.markdown(clean_html(html_str), unsafe_allow_html=True)


# Page Configuration (Safe if embedded)
try:
    st.set_page_config(
        page_title="MasteryFlow | Adaptive Cognitive Learning",
        page_icon=None,
        layout="wide",
        initial_sidebar_state="expanded"
    )
except Exception:
    pass

# Apply unified 2026 dark glass design system
apply_theme()

# ==============================================================================
# STATE & BACKEND CONNECTIVITY ENGINE
# ==============================================================================
FASTAPI_URL = os.getenv("MASTERYFLOW_API_URL", "http://localhost:8000")

@st.cache_resource
def get_embedded_engine():
    """Initializes local pure-Python engine & SQLite DB for zero-latency standalone execution."""
    db_file = str(BASE_DIR / "masteryflow.db")
    db = init_db(db_file)
    graph = load_concept_graph(str(BASE_DIR / "data" / "concepts.json"))
    return db, graph

def check_backend_online() -> bool:
    try:
        r = requests.get(f"{FASTAPI_URL}/", timeout=0.8)
        return r.status_code == 200
    except Exception:
        return False

# Initialize resources
local_db, local_graph = get_embedded_engine()
is_backend_live = check_backend_online()

def init_student_session_state() -> None:
    """Guarantees student session state keys exist across fresh browser sessions and reruns."""
    try:
        uid = st.session_state.get("user_id")
        if uid and ("student_id" not in st.session_state or not st.session_state.student_id):
            st.session_state.student_id = uid
        if "student_id" not in st.session_state or not st.session_state.student_id:
            st.session_state.student_id = "STU_042"
        # Synchronize student name from DB
        try:
            stu_r = local_db.get_student(st.session_state.student_id)
            if stu_r and stu_r.get("name"):
                st.session_state.student_name = stu_r["name"]
        except Exception:
            pass
        if st.session_state.get("student_name") == "Ayoni" or st.session_state.student_id == "STU_365":
            st.session_state.student_name = "Ayon Mukherjee"
        elif "student_name" not in st.session_state or not st.session_state.student_name:
            st.session_state.student_name = "Diya Sharma" if st.session_state.student_id == "STU_042" else "Learner"
        if "active_subject" not in st.session_state:
            st.session_state.active_subject = "Mathematics"
        if "virtual_days" not in st.session_state:
            st.session_state.virtual_days = 0.0
        if "latest_attempt_result" not in st.session_state:
            st.session_state.latest_attempt_result = None
        if "last_question_answered" not in st.session_state:
            st.session_state.last_question_answered = None
        if "active_tab" not in st.session_state:
            st.session_state.active_tab = 0
    except Exception:
        pass

# Safe initial trigger for module import
init_student_session_state()
try:
    local_db.ensure_student(st.session_state.student_id, st.session_state.student_name)
except Exception:
    pass

def get_current_subject_graph():
    """Builds a validated PrerequisiteGraph for the student's active subject."""
    cur_subj = st.session_state.get("active_subject", "Mathematics")
    try:
        from data.curricula import get_subject_concepts
        concepts = get_subject_concepts(cur_subj)
        c_list = []
        for cid, data in concepts.items():
            c_list.append({
                "id": cid,
                "name": data.get("name") or data.get("title", cid),
                "prerequisites": data.get("prerequisites", []),
                "category": data.get("category", ""),
                "order": data.get("order", 1),
                "icon": data.get("icon", "")
            })
        return PrerequisiteGraph(c_list)
    except Exception:
        return local_graph

# ==============================================================================
# DATA RETRIEVAL HELPERS
# ==============================================================================
def fetch_student_mastery() -> Dict[str, Any]:
    init_student_session_state()
    return local_db.get_student_mastery_map(st.session_state.student_id)

def fetch_next_decision() -> Dict[str, Any]:
    init_student_session_state()
    subj_graph = get_current_subject_graph()
    top_order = subj_graph.topological_order()
    default_root = top_order[0] if top_order else "C1"

    stu = local_db.get_student(st.session_state.student_id)
    active_cid = stu.get("active_concept_id", default_root) if stu else default_root
    if active_cid not in top_order:
        active_cid = default_root

    m_map = local_db.get_student_mastery_map(st.session_state.student_id)

    cstates = {}
    for cid in top_order:
        row = m_map.get(cid, {"p": 0.30, "stability_days": 7.0, "evidence_sum": 0.0, "transfer_passed": 0, "is_fragile": 0, "status": "unseen"})
        decayed_p_eff = compute_effective_mastery(
            p=row["p"],
            dt_days=st.session_state.virtual_days,
            stability_days=row["stability_days"]
        )
        cstates[cid] = ConceptState(
            p=row["p"],
            p_eff=decayed_p_eff,
            stability_days=row["stability_days"],
            evidence_sum=row["evidence_sum"],
            transfer_passed=bool(row["transfer_passed"]),
            is_fragile=bool(row["is_fragile"]),
            status=row["status"]
        )

    override = local_db.get_active_override(st.session_state.student_id)
    s_state = StudentState(
        student_id=st.session_state.student_id,
        active_concept_id=active_cid,
        concepts=cstates,
        active_override=override,
        last_attempt_time_days=st.session_state.virtual_days
    )
    decision = next_action(s_state, subj_graph)
    return decision.to_dict()

def fetch_questions_for_concept(concept_id: str) -> List[Dict[str, Any]]:
    return local_db.get_questions_for_concept(concept_id)

# ==============================================================================
# SUBMISSION HANDLER
# ==============================================================================
def handle_student_attempt(attempt_payload: Dict[str, Any]):
    init_student_session_state()
    student_id = st.session_state.student_id
    cid = attempt_payload["concept_id"]
    qid = attempt_payload["question_id"]
    is_corr = attempt_payload["is_correct"]
    diff = attempt_payload["difficulty"]
    is_trans = attempt_payload["is_transfer"]
    conf = attempt_payload["confidence"]
    t_ms = attempt_payload["time_ms"]
    hints = attempt_payload["hints_used"]
    gap = attempt_payload["retry_gap_seconds"]
    attempt_no = attempt_payload["attempt_no"]
    ans = attempt_payload["user_answer"]

    # 1. Compute anti-gaming weight w
    w, is_misconception = compute_evidence_weight(
        hints_used=hints,
        attempt_no=attempt_no,
        time_ms=t_ms,
        retry_gap_seconds=gap,
        prev_correct=None,
        confidence=conf,
        is_correct=is_corr
    )

    # 2. Fetch current mastery
    mastery_map = local_db.get_student_mastery_map(student_id)
    cur = mastery_map.get(cid, {"p": 0.30, "stability_days": 7.0})
    cur_p = cur["p"]
    cur_s = cur["stability_days"]

    # 3. BKT update
    new_p, uncertainty = update_bkt(p=cur_p, is_correct=is_corr, difficulty=diff, w=w)

    # 4. Stability update
    new_s = update_stability(cur_s, is_correct=is_corr)

    # 5. Decay calculation
    p_eff = compute_effective_mastery(new_p, dt_days=st.session_state.virtual_days, stability_days=new_s)

    # 6. Invariant capping using subject graph
    subj_graph = get_current_subject_graph()
    all_p_eff = {k: v["p_eff"] for k, v in mastery_map.items()}
    all_p_eff[cid] = p_eff
    capped_p, is_fragile, _, _ = subj_graph.apply_prerequisite_capping(cid, p_eff, all_p_eff)

    # 7. Update DB state
    local_db.update_streak(student_id, is_corr)
    local_db.update_student_mastery(
        student_id=student_id,
        concept_id=cid,
        p=new_p,
        p_eff=capped_p,
        stability_days=new_s,
        evidence_weight=w,
        is_transfer=is_trans,
        is_fragile=is_fragile
    )
    attempt_id = local_db.record_attempt(
        student_id=student_id,
        concept_id=cid,
        question_id=qid,
        user_answer=ans,
        is_correct=is_corr,
        confidence=conf,
        time_ms=t_ms,
        hints_used=hints,
        retry_gap_seconds=gap,
        attempt_no=attempt_no,
        evidence_weight=w
    )

    # Store telemetry result in session
    res = {
        "attempt_id": attempt_id,
        "is_correct": is_corr,
        "evidence_weight": w,
        "is_misconception": is_misconception,
        "new_p": new_p,
        "p_eff": capped_p,
        "time_ms": t_ms,
        "hints_used": hints,
        "retry_gap_seconds": gap,
    }
    st.session_state.latest_attempt_result = res
    st.session_state.last_question_answered = qid
    st.rerun()

# ==============================================================================
# MAIN RENDER ENTRY POINT
# ==============================================================================
def render_student_portal(show_header: bool = False, show_sidebar: bool = True):
    """Renders the comprehensive Student Adaptive Learning Portal."""
    init_student_session_state()
    local_db.ensure_student(st.session_state.student_id, st.session_state.student_name)

    stu_record = local_db.get_student(st.session_state.student_id)
    streak = stu_record.get("streak", 0) if stu_record else 0
    best_streak = stu_record.get("best_streak", 0) if stu_record else 0

    # Evaluation & Demo Scenarios
    with st.expander("Evaluation Scenarios & Quick Presets", expanded=False):
        c_p1, c_p2, c_p3, c_p4 = st.columns(4)
        with c_p1:
            if st.button("Anti-Gaming Defense", key="st_p1", use_container_width=True):
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
                st.toast("Anti-gaming scenario loaded.", )
                st.rerun()
        with c_p2:
            if st.button("Prerequisite Gap", key="st_p2", use_container_width=True):
                st.session_state.student_id = "STU_001"
                st.session_state.student_name = "Alex Chen"
                st.session_state.virtual_days = 0.0
                st.session_state.latest_attempt_result = None
                st.toast("Prerequisite ceiling scenario loaded.", )
                st.rerun()
        with c_p3:
            if st.button("+21d Memory Decay", key="st_p3", use_container_width=True):
                st.session_state.student_id = "STU_042"
                st.session_state.student_name = "Diya Sharma"
                st.session_state.virtual_days = 21.0
                st.session_state.latest_attempt_result = None
                st.toast("21-day decay scenario loaded.", )
                st.rerun()
        with c_p4:
            if st.button("Mastery Check Gate", key="st_p4", use_container_width=True):
                st.session_state.student_id = "STU_002"
                st.session_state.student_name = "Maya Patel"
                st.session_state.virtual_days = 0.0
                st.session_state.latest_attempt_result = None
                st.toast("Mastery check scenario loaded.", )
                st.rerun()

    # Fetch student state early
    mastery_map = fetch_student_mastery()
    total_concepts = len(mastery_map) if mastery_map else 10
    certified_count = sum(1 for v in mastery_map.values() if v.get("status") == "mastered" or v.get("p_eff", 0) >= 0.85)
    avg_p_eff = (sum(float(v.get("p_eff", 0.3)) for v in mastery_map.values()) / max(1, len(mastery_map))) if mastery_map else 0.50

    # 1. TOP STUDENT STATUS HEADER - Apitex Cognitive Platinum Card & Action Row
    if show_header:
        render_apitex_passport_card(
            student_id=st.session_state.student_id,
            student_name=st.session_state.student_name,
            p_eff=avg_p_eff,
            certified_count=certified_count,
            total_count=total_concepts,
            status=f"Active &middot; Streak {streak}d"
        )
        render_apitex_quick_actions(
            act1_label="Targeted Skill Practice",
            act2_label="Retention Spaced Review",
            act3_label="Student Voice / Agency"
        )


    # 2. SIDEBAR CONTROLS
    if show_sidebar:
        with st.sidebar:
            render_html("""
            <div style="margin-bottom: 8px;">
                <span style="font-size: 0.74rem; color: #64748B; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">
                    Learner Profile
                </span>
            </div>
            """)

            student_profiles_map = {
                "STU_001": ("Priya Singh", "Top Performer — Active: C8 | C1-C7 Mastered"),
                "STU_042": ("Diya Sharma", "Prereq Gap — Active: C7 | C2 Fragile Gap"),
                "STU_002": ("Aarav Patel", "Stuck Plateau — Active: C2 | C1 Mastered"),
                "STU_004": ("Kabir Verma", "Memory Decay — Active: C1 | 21d Gap"),
                "STU_005": ("Ananya Roy", "Mid-Level Achiever — Active: C5 | C1-C4 Mastered"),
                "STU_008": ("Meera Nair", "Capstone Advanced — Active: C9 | C1-C8 Mastered"),
                "STU_006": ("Rohan Mehta", "Adversarial Guesser — Active: C1"),
                "STU_007": ("Ishaan Gupta", "Novice Cold-Start — Active: C1"),
                "STU_365": ("Ayon Mukherjee", "Registered Learner — Active: C1"),
            }

            if st.session_state.student_id in student_profiles_map:
                stu_options = list(student_profiles_map.keys())
                curr_pos = stu_options.index(st.session_state.student_id)

                chosen_pid = st.selectbox(
                    "Active Student:",
                    options=stu_options,
                    index=curr_pos,
                    format_func=lambda k: f"{student_profiles_map[k][0]} ({k})"
                )

                if chosen_pid != st.session_state.student_id:
                    st.session_state.student_id = chosen_pid
                    st.session_state.student_name = student_profiles_map[chosen_pid][0]
                    st.session_state.latest_attempt_result = None
                    st.session_state.virtual_days = 21.0 if chosen_pid == "STU_004" else 0.0
                    st.rerun()
            else:
                st.write(f"Logged in as: {st.session_state.student_name} ({st.session_state.student_id})")

            local_db.ensure_student(st.session_state.student_id, st.session_state.student_name)

            render_html("<hr style='border: 0; border-top: 1px solid #E2E8F0; margin: 16px 0;'>")

            render_html("""
            <div style="margin-bottom: 6px;">
                <span style="font-size: 0.74rem; color: #64748B; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">
                    Knowledge Retention Simulator
                </span>
            </div>
            <p style="font-size: 0.78rem; color: #64748B; line-height: 1.4; margin-bottom: 8px;">
                Test how days of inactivity affect memory retention and trigger review recommendations.
            </p>
            """)

            v_days = st.slider("Simulate Days Inactive:", min_value=0, max_value=30, value=int(st.session_state.virtual_days), step=1)
            if v_days != st.session_state.virtual_days:
                st.session_state.virtual_days = float(v_days)
                st.rerun()

            render_html("<hr style='border: 0; border-top: 1px solid #E2E8F0; margin: 16px 0;'>")

            render_html("""
            <div style="margin-bottom: 6px;">
                <span style="font-size: 0.74rem; color: #64748B; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">
                    Export My Learning Data
                </span>
            </div>
            <p style="font-size: 0.78rem; color: #64748B; line-height: 1.4; margin-bottom: 8px;">
                Download your certified mastery record as an Excel-compatible CSV file.
            </p>
            """)
            try:
                from frontend.components.export_service import export_student_mastery_csv
            except ImportError:
                from masteryflow.ui.components.export_service import export_student_mastery_csv

            csv_dl, fn_dl = export_student_mastery_csv(st.session_state.student_id, db=local_db)
            st.download_button(
                label="Download My Mastery (CSV)",
                data=csv_dl,
                file_name=fn_dl,
                mime="text/csv",
                use_container_width=True
            )

            render_html("<hr style='border: 0; border-top: 1px solid #E2E8F0; margin: 16px 0;'>")

            if st.button("Reset Progress (Start Fresh)", use_container_width=True):
                local_db.ensure_student(st.session_state.student_id, st.session_state.student_name)
                cur_m_map = local_db.get_student_mastery_map(st.session_state.student_id)
                for cid in cur_m_map.keys():
                    local_db.update_student_mastery(
                        st.session_state.student_id, cid, p=0.30, p_eff=0.30, stability_days=7.0, evidence_weight=0.0, status="unseen"
                    )
                st.session_state.latest_attempt_result = None
                st.session_state.virtual_days = 0.0
                st.success("Learner progress reset across all curricula.")
                st.rerun()


    # Fetch state & decision
    cur_subject = st.session_state.get("active_subject", "Mathematics")
    subj_graph = get_current_subject_graph()
    try:
        from data.curricula import get_subject_concepts
        cur_concepts_dict = get_subject_concepts(cur_subject)
    except Exception:
        cur_concepts_dict = {}

    mastery_map = fetch_student_mastery()
    next_decision = fetch_next_decision()

    concepts_meta = {}
    for cid, data in cur_concepts_dict.items():
        c_dict = dict(data)
        c_dict["id"] = cid
        c_dict["concept_id"] = cid
        c_dict["prerequisites"] = subj_graph.get_prerequisites(cid)
        concepts_meta[cid] = c_dict

    target_cid = next_decision.get("target_concept")
    if not target_cid or target_cid not in concepts_meta:
        top_cids = list(concepts_meta.keys())
        target_cid = top_cids[0] if top_cids else "C1"

    target_meta = concepts_meta.get(target_cid, {"name": target_cid, "icon": ""})
    target_cstate = mastery_map.get(target_cid, {})

    p_eff_val = max(5, min(100, int(round(float(target_cstate.get("p_eff", 0.30)) * 100))))
    stability_val = target_cstate.get("stability_days", 7.0)
    is_fragile = target_cstate.get("is_fragile", False)
    status_label = target_cstate.get("status", "practicing").capitalize()
    gauge_html = render_circular_gauge(p_eff_val, "Mastery", color="#E11D48" if is_fragile else "#11141D", size=84)

    # 3-Column Clean HUD in Apitex Style
    col_hud1, col_hud2, col_hud3 = st.columns([1.1, 1.0, 1.0])
    with col_hud1:
        render_html(f"""
        <div class="mf-glass-card" style="padding: 18px 22px; margin-bottom: 18px; display: flex; align-items: center; justify-content: space-between; min-height: 110px;">
            <div>
                <span style="font-size: 0.70rem; color: #78716C; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px;">
                    Current Focus
                </span>
                <div style="font-size: 1.35rem; font-weight: 800; color: #11141D; margin-top: 2px;">
                    {target_cid}
                </div>
                <div style="font-size: 0.82rem; color: #78716C; margin-top: 1px;">
                    {target_meta.get('name', target_cid)}
                </div>
            </div>
            <div>
                {gauge_html}
            </div>
        </div>
        """)

    with col_hud2:
        render_html(f"""
        <div class="mf-glass-card" style="padding: 18px 22px; margin-bottom: 18px; min-height: 110px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 0.70rem; color: #78716C; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px;">
                    Retention Stability
                </span>
                <span style="font-size: 0.68rem; color: #7C3AED; background: #EDE9FE; border: 1px solid #DDD6FE; padding: 3px 10px; border-radius: 9999px; font-weight: 700;">
                    Spaced Practice
                </span>
            </div>
            <div style="font-size: 1.5rem; font-weight: 800; color: #11141D; margin-top: 3px;">
                {stability_val:.1f} Days
            </div>
            <div style="font-size: 0.74rem; color: #78716C; margin-top: 3px;">
                Estimated retention interval before review
            </div>
            <div style="background: #EDE6DA; border-radius: 999px; height: 6px; overflow: hidden; margin-top: 8px;">
                <div style="width: {min(100, int((stability_val/30.0)*100))}%; height: 100%; background: #7C3AED; border-radius: 999px;"></div>
            </div>
        </div>
        """)

    with col_hud3:
        render_html(f"""
        <div class="mf-glass-card" style="padding: 18px 22px; margin-bottom: 18px; min-height: 110px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 0.70rem; color: #78716C; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px;">
                    Learning Rhythm
                </span>
                <span style="font-size: 0.68rem; color: #059669; background: #E8F7F0; border: 1px solid #A7F3D0; padding: 3px 10px; border-radius: 9999px; font-weight: 700;">
                    Active
                </span>
            </div>
            <div style="font-size: 1.5rem; font-weight: 800; color: #11141D; margin-top: 3px;">
                {str(streak) + ' in a row' if streak > 0 else 'Steady Progress'}
            </div>
            <div style="font-size: 0.74rem; color: #78716C; margin-top: 3px;">
                Status: <strong style="color: #11141D;">{status_label}</strong> &middot; Adaptive Path
            </div>
            <div style="background: #EDE6DA; border-radius: 999px; height: 6px; overflow: hidden; margin-top: 8px;">
                <div style="width: 100%; height: 100%; background: #059669; border-radius: 999px;"></div>
            </div>
        </div>
        """)

    # Active Subject Course Progress Strip
    subj_order = subj_graph.topological_order()
    m_done = sum(1 for cid in subj_order if mastery_map.get(cid, {}).get("status") == "mastered" or float(mastery_map.get(cid, {}).get("p_eff", 0)) >= 0.85)
    subj_total = len(subj_order) or 1
    subj_pct = int(round((m_done / subj_total) * 100))
    avg_subj_peff = int(round((sum(float(mastery_map.get(cid, {}).get("p_eff", 0.30)) for cid in subj_order) / subj_total) * 100))
    subj_icons = {
        "Mathematics": "",
        "Computer Networks": "",
        "Artificial Intelligence": "",
        "Formal Languages & Automata": "",
        "Biochemistry": ""
    }
    s_abbr = cur_subject[:3].upper() if cur_subject else "CRS"

    render_html(f"""
    <div class="mf-glass-card" style="padding: 14px 20px; margin-bottom: 18px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="width: 38px; height: 38px; border-radius: 12px; background: #11141D; display: flex; align-items: center; justify-content: center; font-size: 0.82rem; font-weight: 800; color: #FFFFFF; letter-spacing: 0.5px; box-shadow: 0 4px 12px rgba(17, 20, 29, 0.20);">
                {s_abbr}
            </div>
            <div>
                <div style="font-size: 0.94rem; font-weight: 800; color: #11141D;">
                    {cur_subject} Course Progress &middot; <span style="color: #059669;">{subj_pct}% Completed</span>
                </div>
                <div style="font-size: 0.74rem; color: #78716C; margin-top: 1px;">
                    {m_done} of {subj_total} Concepts Certified &middot; Cognitive Readiness: <strong style="color: #11141D;">{avg_subj_peff}%</strong>
                </div>
            </div>
        </div>
        <div style="min-width: 220px; flex-grow: 1; max-width: 360px;">
            <div style="display: flex; justify-content: space-between; font-size: 0.70rem; color: #78716C; margin-bottom: 3px;">
                <span>Curriculum Mastery</span>
                <span style="font-weight: 700; color: #11141D;">{m_done}/{subj_total} Topics</span>
            </div>
            <div style="background: #EDE6DA; border-radius: 999px; height: 7px; overflow: hidden;">
                <div style="width: {subj_pct}%; height: 100%; background: #059669; border-radius: 9999px; transition: width 0.4s ease;"></div>
            </div>
        </div>
    </div>
    """)

    # 3. TABS WORKSPACE
    tabs = st.tabs([
        "Practice & Exercises",
        "Curriculum Roadmap",
        "Video Lessons",
        "Project Guide",
        "Diagnostic Assessment",
        "Progress & Analytics"
    ])

    # TAB 1: PRACTICE & EXERCISES
    with tabs[0]:
        render_glassbox_card(next_decision, target_meta, target_cstate, student_name=st.session_state.student_name)

        render_agency_modal(
            student_id=st.session_state.student_id,
            current_concept_id=target_cid,
            student_name=st.session_state.student_name
        )

        if st.session_state.latest_attempt_result and st.session_state.last_question_answered:
            q_records = local_db.get_questions_for_concept(target_cid)
            matching_q = next((q for q in q_records if q["id"] == st.session_state.last_question_answered), None)
            if matching_q:
                render_telemetry_breakdown(st.session_state.latest_attempt_result, matching_q)
                
                # Immediate Conceptual Guidance Card & Video Remediation on Exercise Failure
                if not st.session_state.latest_attempt_result.get("is_correct"):
                    render_html(f"""
                    <div style="background: #FFF1F2; border: 1px solid #FECDD3; border-radius: 14px; padding: 14px 18px; margin-bottom: 12px;">
                        <div style="color: #9F1239; font-weight: 800; font-size: 0.95rem; margin-bottom: 4px;">
                            Concept Remediation &amp; Guidance: {target_cid}
                        </div>
                        <div style="font-size: 0.82rem; color: #881337; line-height: 1.5;">
                            {target_meta.get('description', 'Review the foundational principles of this topic. Take your time before re-attempting.')}
                        </div>
                    </div>
                    """)
                    render_failure_remediation_card(target_cid, target_meta.get('title') or target_meta.get('name', target_cid))

                if st.button("Continue to Next Exercise", key="btn_continue_next", use_container_width=True):
                    st.session_state.latest_attempt_result = None
                    st.rerun()

        questions_list = fetch_questions_for_concept(target_cid)
        if not questions_list:
            st.warning(f"No exercises currently found for topic {target_cid}.")
        else:
            with st.expander("Concept Guide & Pedagogical Walkthrough", expanded=False):
                render_html(f"""
                <div style="background: #FFFFFF; border: 1px solid #E5DCD0; border-radius: 14px; padding: 16px 20px; margin-bottom: 8px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <strong style="color: #11141D; font-size: 0.95rem;">
                            {target_cid}: {target_meta.get('title') or target_meta.get('name', target_cid)}
                        </strong>
                        <span style="background: #F4EEE5; color: #11141D; font-size: 0.72rem; font-weight: 700; padding: 2px 8px; border-radius: 9999px;">
                            Readiness: {int(target_cstate.get('p_eff', 0.3) * 100)}%
                        </span>
                    </div>
                    <p style="color: #475569; font-size: 0.85rem; line-height: 1.5; margin: 0 0 10px 0;">
                        {target_meta.get('description', 'Master this core foundational concept through calibrated practice in your Zone of Proximal Development (ZPD).')}
                    </p>
                    <div style="font-size: 0.78rem; color: #64748B;">
                        <strong>Prerequisites:</strong> {', '.join(target_meta.get('prerequisites', [])) or 'None (Root Topic)'} &middot; 
                        <strong>Certification:</strong> Answer calibrated items (d &ge; 0.5) to certify mastery.
                    </div>
                </div>
                """)
                render_concept_video_recommendation(target_cid, target_meta.get('title') or target_meta.get('name', target_cid))

            transfer_ready = (target_cstate.get("p_eff", 0.3) >= 0.70 and not target_cstate.get("transfer_passed"))
            if transfer_ready:
                selected_q = next((q for q in questions_list if q.get("is_transfer")), questions_list[0])
            else:
                candidates = [q for q in questions_list if not q.get("is_transfer")]
                selected_q = candidates[0] if candidates else questions_list[0]

            render_question_runner(
                question=selected_q,
                on_submit_attempt=handle_student_attempt,
                current_streak=streak
            )

    # TAB 2: CURRICULUM ROADMAP
    with tabs[1]:
        def on_select_node(clicked_cid):
            with local_db.conn:
                local_db.conn.execute(
                    "UPDATE students SET active_concept_id = ? WHERE student_id = ?",
                    (clicked_cid, st.session_state.student_id)
                )
            st.toast(f"Active focus switched to {clicked_cid}.")
            st.rerun()

        col_v1, col_v2 = st.columns([2, 1])
        with col_v1:
            view_mode = st.radio(
                "Visualizer Mode:",
                ["Visual Learning Map", "3D Knowledge Universe"],
                horizontal=True,
                label_visibility="collapsed"
            )
        with col_v2:
            quick_switch_cid = st.selectbox(
                "Focus on Topic:",
                options=list(concepts_meta.keys()),
                index=list(concepts_meta.keys()).index(target_cid) if target_cid in concepts_meta else 0,
                format_func=lambda cid: f"{cid}: {concepts_meta.get(cid, {}).get('title', cid)}",
                label_visibility="collapsed"
            )
            if quick_switch_cid != target_cid:
                if st.button(f"Focus on {quick_switch_cid}", use_container_width=True):
                    on_select_node(quick_switch_cid)

        if view_mode == "3D Knowledge Universe":
            render_html("""
            <div style="display: flex; align-items: center; justify-content: space-between; padding: 11px 18px; margin-bottom: 14px; background: rgba(56, 189, 248, 0.08); border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 9999px; font-size: 0.82rem; color: #CBD5E1; backdrop-filter: blur(12px);">
                <div>
                    <strong style="color: #38BDF8;">3D Controls:</strong> Drag to orbit 360° &middot; Scroll to zoom &middot; Right-click to pan.
                </div>
                <div>
                    <span style="color: #94A3B8;">Click any sphere to inspect concept details.</span>
                </div>
            </div>
            """)
            render_3d_universe_widget(
                concepts_meta=concepts_meta,
                mastery_map=mastery_map,
                active_concept_id=target_cid,
                height=650
            )
        else:
            render_dag_visualizer(
                concepts_meta=concepts_meta,
                mastery_map=mastery_map,
                active_concept_id=target_cid,
                on_select_concept_cb=on_select_node
            )

    # TAB 3: VIDEO LESSONS HUB
    with tabs[2]:
        render_subject_video_library(cur_subject, target_cid)

    # TAB 4: PROJECT GUIDE & FEATURE MANUAL (README)
    with tabs[3]:
        from frontend.components.project_guide import render_project_guide
        render_project_guide()

    # TAB 5: DIAGNOSTIC ASSESSMENT
    with tabs[4]:
        render_html(f"""
        <div class="mf-glass-card" style="padding: 18px 22px; margin-bottom: 18px;">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div>
                        <h3 style="color: #F8FAFC; margin: 0; font-size: 1.25rem; font-weight: 800;">
                            {cur_subject} Diagnostic Assessment
                        </h3>
                        <p style="font-size: 0.82rem; color: #94A3B8; margin: 2px 0 0 0;">
                            Quickly calibrate your mastery across key milestone concepts to personalize your learning path.
                        </p>
                    </div>
                </div>
                <span style="background: rgba(56, 189, 248, 0.12); color: #38BDF8; border: 1px solid rgba(56, 189, 248, 0.35); padding: 3px 10px; border-radius: 9999px; font-size: 0.70rem; font-weight: 700;">
                    Milestone Diagnostic
                </span>
            </div>
        </div>
        """)

        subj_order = subj_graph.topological_order()
        subj_diag_cids = subj_order[:min(len(subj_order), 6)] if subj_order else ["C1"]
        diag_engine = DiagnosticEngine(subj_graph, diagnostic_concepts=subj_diag_cids)
        diag_cids = diag_engine.diagnostic_concepts

        done_count = sum(1 for c in diag_cids if mastery_map.get(c, {}).get("status") in ["practicing", "mastered", "provisional"])
        st.progress(done_count / max(1, len(diag_cids)), text=f"Diagnostic Progress: {done_count}/{len(diag_cids)} Milestone Concepts Checked")

        st.markdown("<p style='font-size: 0.78rem; color: #94A3B8; margin: 14px 0 10px 0; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;'>Key Milestone Concepts:</p>", unsafe_allow_html=True)
        diag_cols = st.columns(min(len(diag_cids), 3))
        for d_idx, dcid in enumerate(diag_cids):
            cm = concepts_meta.get(dcid, {})
            ms = mastery_map.get(dcid, {})
            p_val = int(round(float(ms.get("p_eff", 0.30)) * 100))
            with diag_cols[d_idx % len(diag_cols)]:
                render_html(f"""
                <div style="padding: 14px 16px; margin-bottom: 12px; border: 1px solid rgba(148, 163, 184, 0.16); background: rgba(17, 24, 39, 0.75); backdrop-filter: blur(14px); border-radius: 12px; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35);">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <strong style="color: #F8FAFC; font-size: 0.95rem;">
                            {dcid}
                        </strong>
                        <span style="font-size: 0.68rem; color: #38BDF8; background: rgba(56, 189, 248, 0.12); border: 1px solid rgba(56, 189, 248, 0.35); padding: 2px 7px; border-radius: 9999px; font-weight: 700;">
                            Mastery: {p_val}%
                        </span>
                    </div>
                    <div style="font-size: 0.82rem; color: #CBD5E1; margin: 4px 0 6px 0; font-weight: 600;">
                        {cm.get('name', dcid)}
                    </div>
                    <div style="font-size: 0.72rem; color: #94A3B8;">
                        Prerequisites: {', '.join(cm.get('prerequisites', [])) or 'None (Baseline)'}
                    </div>
                </div>
                """)
                if st.button(f"Practice {dcid}", key=f"btn_diag_test_{dcid}", use_container_width=True):
                    with local_db.conn:
                        local_db.conn.execute("UPDATE students SET active_concept_id = ? WHERE student_id = ?", (dcid, st.session_state.student_id))
                    st.toast(f"Switched focus to {dcid}.")
                    st.rerun()

    # TAB 6: PROGRESS & ANALYTICS
    with tabs[5]:
        # 1. Multi-Disciplinary Course Progress Comparison Matrix
        all_subjects_meta = [
            ("Mathematics", "", ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10"]),
            ("Computer Networks", "", ["CN1", "CN2", "CN3", "CN4", "CN5", "CN6", "CN7", "CN8"]),
            ("Artificial Intelligence", "", ["AI1", "AI2", "AI3", "AI4", "AI5", "AI6", "AI7", "AI8"]),
            ("Formal Languages & Automata", "", ["FLA1", "FLA2", "FLA3", "FLA4", "FLA5", "FLA6", "FLA7", "FLA8"]),
            ("Biochemistry", "", ["BIO1", "BIO2", "BIO3", "BIO4", "BIO5", "BIO6", "BIO7", "BIO8"]),
        ]

        render_html("""
        <div class="mf-glass-card" style="padding: 18px 22px; margin-bottom: 18px;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
                <div>
                    <h3 style="color: #11141D; margin: 0; font-size: 1.22rem; font-weight: 800; letter-spacing: -0.02em;">
                        Cross-Disciplinary Course Progress Overview
                    </h3>
                    <p style="font-size: 0.80rem; color: #78716C; margin: 2px 0 0 0;">
                        Real-time cognitive mastery, certified concepts, and completion velocity across all 5 disciplines
                    </p>
                </div>
                <span style="font-size: 0.72rem; color: #047857; background: #E8F7F0; padding: 4px 12px; border-radius: 9999px; font-weight: 700; border: 1px solid #A7F3D0;">
                    5 Active Curricula
                </span>
            </div>
        </div>
        """)

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
                    if st.button(f"Switch to {s_icon}", key=f"btn_tab6_switch_subj_{idx}", use_container_width=True):
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
                            local_db.conn.execute("UPDATE students SET active_concept_id = ? WHERE student_id = ?", (new_cid, st.session_state.student_id))
                        st.rerun()

        render_html("<hr style='border: 0; border-top: 1px solid #E2E8F0; margin: 20px 0 16px 0;'>")

        # 2. Detailed Concept Breakdown for Active Subject
        subj_order = subj_graph.topological_order()
        start_cid = subj_order[0] if subj_order else ""
        end_cid = subj_order[-1] if subj_order else ""
        render_html(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; flex-wrap: wrap; gap: 10px;">
            <div>
                <h3 style="color: #11141D; margin: 0; font-size: 1.25rem; font-weight: 800;">
                    {cur_subject} &middot; Detailed Concept Mastery Breakdown
                </h3>
                <div style="font-size: 0.80rem; color: #78716C; margin-top: 2px;">
                    Topological concept progression and cognitive metrics across the {cur_subject} curriculum
                </div>
            </div>
            <span style="font-size: 0.72rem; color: #11141D; background: #F4EEE5; padding: 4px 12px; border-radius: 9999px; border: 1px solid #E5DCD0; font-weight: 700;">
                Topological Order ({start_cid} &rarr; {end_cid})
            </span>
        </div>
        """)

        # Clean Mathematical Proof Formulas in Apitex Porcelain Card
        st.markdown(r"""
        <div class="mf-glass-card" style="padding: 16px 20px; margin-bottom: 16px;">
            <div style="font-size: 0.72rem; color: #78716C; font-weight: 700; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 8px;">
                Core Principles of the Adaptive Decision Engine
            </div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 10px; font-size: 0.82rem; color: #11141D;">
                <div style="background: #F4EEE5; padding: 10px 14px; border-radius: 10px; border: 1px solid #E8E0D4;">
                    <strong style="color: #11141D;">Bayesian Knowledge Tracing:</strong><br>
                    $$P(L_t \mid \text{obs}) = \frac{P(L_{t-1}) \cdot P(\text{obs} \mid L_{t-1})}{P(\text{obs})}$$
                </div>
                <div style="background: #F4EEE5; padding: 10px 14px; border-radius: 10px; border: 1px solid #E8E0D4;">
                    <strong style="color: #11141D;">Memory Retention Decay:</strong><br>
                    $$p_{\text{eff}} = \text{floor} + (p - \text{floor}) \cdot e^{-\Delta t / S}$$
                </div>
                <div style="background: #F4EEE5; padding: 10px 14px; border-radius: 10px; border: 1px solid #E8E0D4;">
                    <strong style="color: #059669;">Response Quality Factor:</strong><br>
                    $$w = w_{\text{speed}} \cdot w_{\text{hints}} \cdot w_{\text{conf}} \cdot w_{\text{retry}}$$
                </div>
                <div style="background: #F4EEE5; padding: 10px 14px; border-radius: 10px; border: 1px solid #E8E0D4;">
                    <strong style="color: #E11D48;">Prerequisite Verification:</strong><br>
                    $$p_{\text{capped}} = \min(p_{\text{eff}}, \min_{u \in \text{parents}}(p_u) + 0.25)$$
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        matrix_rows = []
        for cid in subj_order:
            cm = concepts_meta.get(cid, {})
            ms = mastery_map.get(cid, {})
            p = ms.get("p", 0.30)
            p_eff = ms.get("p_eff", 0.30)
            s = ms.get("stability_days", 7.0)
            ev = ms.get("evidence_sum", 0.0)
            tp = "Yes" if ms.get("transfer_passed") else "Pending"
            fr = "Gap" if ms.get("is_fragile") else "Solid"
            st_label = ms.get("status", "unseen").capitalize()

            matrix_rows.append({
                "Topic ID": cid,
                "Topic Name": cm.get("name", cid),
                "Status": st_label,
                "Mastery": f"{round(p * 100, 1)}%",
                "Effective Retention": f"{round(p_eff * 100, 1)}%",
                "Stability": f"{s:.1f} days",
                "Evidence Weight": round(ev, 2),
                "Transfer Verified": tp,
                "Prerequisite Health": fr
            })

        st.dataframe(matrix_rows, use_container_width=True)

        render_html("""
        <div class="mf-glass-card" style="padding: 18px 22px; margin-top: 18px;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                <h4 style="color: #11141D; margin: 0; font-size: 1.05rem; font-weight: 800;">
                    How MasteryFlow Personalizes Your Journey
                </h4>
            </div>
            <ul style="font-size: 0.86rem; color: #4B5563; margin: 0; padding-left: 20px; line-height: 1.65;">
                <li><strong style="color: #11141D;">Skill Tracing:</strong> Evaluates your answers, timing, and hints to determine accurate latent mastery for each concept.</li>
                <li><strong style="color: #11141D;">Prerequisite Verification:</strong> Automatically checks foundational building blocks before unlocking complex topics.</li>
                <li><strong style="color: #11141D;">Spaced Practice:</strong> Schedules timely reviews of previously mastered topics to prevent memory forgetting over time.</li>
                <li><strong style="color: #11141D;">Fair Evaluation:</strong> Differentiates between thoughtful solutions and rapid guesses to keep practice meaningful.</li>
            </ul>
        </div>
        """)


if __name__ == "__main__":
    render_student_portal(show_header=True, show_sidebar=True)
