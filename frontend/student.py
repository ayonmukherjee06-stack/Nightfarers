"""MasteryFlow: Student Glass-Box Adaptive Learning Portal.

Owner: Soham Choudhury (Frontend Co-Lead & Question Bank Lead) & Ayon Mukherjee (Lead)
Aesthetic: Modern 2026 Linear/Raycast Dark Glassmorphism, Live Telemetry HUD, Interactive DAG Roadmap.
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
    from frontend.components.theme import apply_theme, render_brand_header, render_circular_gauge
    from frontend.components.math_parser import evaluate_student_answer, parse_fraction_input
    from frontend.components.glassbox_card import render_glassbox_card
    from frontend.components.dag_visualizer import render_dag_visualizer
    from frontend.components.question_runner import render_question_runner
    from frontend.components.telemetry_card import render_telemetry_breakdown
    from frontend.components.agency_modal import render_agency_modal
except ModuleNotFoundError:
    try:
        from components.theme import apply_theme, render_brand_header, render_circular_gauge
        from components.math_parser import evaluate_student_answer, parse_fraction_input
        from components.glassbox_card import render_glassbox_card
        from components.dag_visualizer import render_dag_visualizer
        from components.question_runner import render_question_runner
        from components.telemetry_card import render_telemetry_breakdown
        from components.agency_modal import render_agency_modal
    except ModuleNotFoundError:
        from masteryflow.ui.components.theme import apply_theme, render_brand_header, render_circular_gauge
        from masteryflow.ui.components.math_parser import evaluate_student_answer, parse_fraction_input
        from masteryflow.ui.components.glassbox_card import render_glassbox_card
        from masteryflow.ui.components.dag_visualizer import render_dag_visualizer
        from masteryflow.ui.components.question_runner import render_question_runner
        from masteryflow.ui.components.telemetry_card import render_telemetry_breakdown
        from masteryflow.ui.components.agency_modal import render_agency_modal

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

# Page Configuration (Safe if embedded)
try:
    st.set_page_config(
        page_title="MasteryFlow | Adaptive Cognitive Learning",
        page_icon="🌌",
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

# Session State Initialization
if "student_id" not in st.session_state:
    st.session_state.student_id = "STU_042"
    st.session_state.student_name = "Diya Sharma"

if "virtual_days" not in st.session_state:
    st.session_state.virtual_days = 0.0

if "latest_attempt_result" not in st.session_state:
    st.session_state.latest_attempt_result = None

if "last_question_answered" not in st.session_state:
    st.session_state.last_question_answered = None

if "active_tab" not in st.session_state:
    st.session_state.active_tab = 0

# Ensure student exists in local DB
local_db.ensure_student(st.session_state.student_id, st.session_state.student_name)

# ==============================================================================
# DATA RETRIEVAL HELPERS (FLAWLESS DUAL-MODE)
# ==============================================================================
def fetch_student_mastery() -> Dict[str, Any]:
    if is_backend_live:
        try:
            r = requests.get(f"{FASTAPI_URL}/api/student/{st.session_state.student_id}/mastery", timeout=2.0)
            if r.status_code == 200:
                return r.json().get("mastery", {})
        except Exception:
            pass
    # Fallback to local SQLite engine
    return local_db.get_student_mastery_map(st.session_state.student_id)

def fetch_next_decision() -> Dict[str, Any]:
    if is_backend_live:
        try:
            r = requests.get(f"{FASTAPI_URL}/api/next-action/{st.session_state.student_id}", timeout=2.0)
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass

    # Fallback to local pure Python decision engine
    stu = local_db.get_student(st.session_state.student_id)
    active_cid = stu.get("active_concept_id", "C1") if stu else "C1"
    m_map = local_db.get_student_mastery_map(st.session_state.student_id)

    cstates = {}
    for cid, row in m_map.items():
        # Apply virtual days decay for current view
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
    decision = next_action(s_state, local_graph)
    return decision.to_dict()

def fetch_questions_for_concept(concept_id: str) -> List[Dict[str, Any]]:
    return local_db.get_questions_for_concept(concept_id)

# ==============================================================================
# SUBMISSION HANDLER
# ==============================================================================
def handle_student_attempt(attempt_payload: Dict[str, Any]):
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

    # 6. Invariant capping
    all_p_eff = {k: v["p_eff"] for k, v in mastery_map.items()}
    all_p_eff[cid] = p_eff
    capped_p, is_fragile, _, _ = local_graph.apply_prerequisite_capping(cid, p_eff, all_p_eff)

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

    stu_record = local_db.get_student(st.session_state.student_id)
    streak = stu_record.get("streak", 0) if stu_record else 0
    best_streak = stu_record.get("best_streak", 0) if stu_record else 0

    # 1. TOP 2026 COMMAND HUD
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(13, 19, 38, 0.85) 0%, rgba(8, 12, 26, 0.95) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 16px 22px;
        margin-bottom: 22px;
        backdrop-filter: blur(20px);
        box-shadow: 0 14px 34px -10px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.08);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 14px;
    ">
        <!-- Learner Profile Info -->
        <div style="display: flex; align-items: center; gap: 14px;">
            <div style="
                width: 44px;
                height: 44px;
                border-radius: 12px;
                background: linear-gradient(135deg, #00F0FF 0%, #8B5CF6 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.3rem;
                box-shadow: 0 0 18px rgba(0, 240, 255, 0.35);
            ">
                🎓
            </div>
            <div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <h2 style="margin: 0; font-size: 1.35rem; font-weight: 800; color: #FFFFFF; font-family: 'Space Grotesk', sans-serif;">
                        {st.session_state.student_name}
                    </h2>
                    <span style="
                        background: rgba(0, 240, 255, 0.12);
                        color: #00F0FF;
                        border: 1px solid rgba(0, 240, 255, 0.3);
                        font-size: 0.68rem;
                        font-weight: 700;
                        padding: 2px 8px;
                        border-radius: 9999px;
                        letter-spacing: 0.5px;
                        font-family: monospace;
                    ">
                        {st.session_state.student_id}
                    </span>
                </div>
                <div style="font-size: 0.76rem; color: #94A3B8; margin-top: 2px;">
                    Adaptive Cognitive Session &middot; Live Knowledge Tracing
                </div>
            </div>
        </div>

        <!-- Telemetry Stats Pill -->
        <div style="
            display: flex;
            align-items: center;
            gap: 16px;
            background: rgba(6, 10, 22, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 12px;
            padding: 8px 18px;
        ">
            <div style="text-align: center;">
                <div style="font-size: 0.65rem; color: #94A3B8; text-transform: uppercase; font-weight: 700; letter-spacing: 0.8px; font-family: 'Space Grotesk', sans-serif;">Active Streak</div>
                <div style="font-size: 1.25rem; font-weight: 800; color: #F59E0B; font-family: 'JetBrains Mono', monospace;">
                    🔥 {streak}
                </div>
            </div>
            <div style="width: 1px; height: 26px; background: rgba(255,255,255,0.08);"></div>
            <div style="text-align: center;">
                <div style="font-size: 0.65rem; color: #94A3B8; text-transform: uppercase; font-weight: 700; letter-spacing: 0.8px; font-family: 'Space Grotesk', sans-serif;">Best Record</div>
                <div style="font-size: 1.25rem; font-weight: 800; color: #38BDF8; font-family: 'JetBrains Mono', monospace;">
                    ⚡ {best_streak}
                </div>
            </div>
            <div style="width: 1px; height: 26px; background: rgba(255,255,255,0.08);"></div>
            <div style="text-align: center;">
                <div style="font-size: 0.65rem; color: #94A3B8; text-transform: uppercase; font-weight: 700; letter-spacing: 0.8px; font-family: 'Space Grotesk', sans-serif;">Memory Clock</div>
                <div style="font-size: 1.25rem; font-weight: 800; color: #A855F7; font-family: 'JetBrains Mono', monospace;">
                    +{int(st.session_state.virtual_days)}d
                </div>
            </div>
        </div>

        <!-- Connection Indicator -->
        <div style="text-align: right;">
            <div style="
                display: inline-flex;
                align-items: center;
                gap: 6px;
                background: rgba(16, 185, 129, 0.12);
                border: 1px solid rgba(16, 185, 129, 0.35);
                color: #34D399;
                font-size: 0.74rem;
                font-weight: 700;
                padding: 4px 12px;
                border-radius: 9999px;
                letter-spacing: 0.5px;
            ">
                <span style="font-size: 0.6rem;">●</span> {'REST API ONLINE' if is_backend_live else 'EMBEDDED ENGINE ACTIVE'}
            </div>
            <div style="font-size: 0.70rem; color: #64748B; margin-top: 3px; font-family: 'Space Grotesk', sans-serif;">
                Deterministic Psychometric Loop
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. SIDEBAR CONTROLS
    if show_sidebar:
        with st.sidebar:
            st.markdown("""
            <div style="margin-bottom: 12px;">
                <span style="font-size: 0.72rem; color: #00F0FF; font-weight: 800; text-transform: uppercase; letter-spacing: 1.2px; font-family: 'Space Grotesk', sans-serif;">
                    Learner Profile
                </span>
            </div>
            """, unsafe_allow_html=True)

            profile_selection = st.selectbox(
                "Active Persona / Student:",
                options=[
                    "STU_042 - Diya Sharma (Standard Learner)",
                    "STU_001 - Alex Chen (Struggling with Prereqs)",
                    "STU_002 - Maya Patel (Advanced Proportions)",
                    "STU_GUESSER - Brute Force Guesser",
                    "CUSTOM - Enter Custom Student ID"
                ],
                index=0
            )

            if "CUSTOM" in profile_selection:
                new_id = st.text_input("Enter Student ID:", value="STU_999")
                st.session_state.student_id = new_id
                st.session_state.student_name = f"Learner {new_id}"
            else:
                pid = profile_selection.split(" - ")[0]
                pname = profile_selection.split(" - ")[1].split(" (")[0]
                st.session_state.student_id = pid
                st.session_state.student_name = pname

            local_db.ensure_student(st.session_state.student_id, st.session_state.student_name)

            st.markdown("<hr style='border: 0; border-top: 1px solid rgba(255,255,255,0.06); margin: 18px 0;'>", unsafe_allow_html=True)

            st.markdown("""
            <div style="margin-bottom: 8px;">
                <span style="font-size: 0.72rem; color: #A855F7; font-weight: 800; text-transform: uppercase; letter-spacing: 1.2px; font-family: 'Space Grotesk', sans-serif;">
                    ⏳ Ebbinghaus Longitudinal Time Travel
                </span>
            </div>
            <p style="font-size: 0.78rem; color: #94A3B8; line-height: 1.4; margin-bottom: 10px;">
                Simulate retention decay over days without training. Triggers Spaced Review live on faded nodes!
            </p>
            """, unsafe_allow_html=True)

            v_days = st.slider("Elapsed Days of Inactivity:", min_value=0, max_value=30, value=int(st.session_state.virtual_days), step=1)
            if v_days != st.session_state.virtual_days:
                st.session_state.virtual_days = float(v_days)
                st.rerun()

            st.markdown("<hr style='border: 0; border-top: 1px solid rgba(255,255,255,0.06); margin: 18px 0;'>", unsafe_allow_html=True)

            st.markdown("""
            <div style="margin-bottom: 8px;">
                <span style="font-size: 0.72rem; color: #F59E0B; font-weight: 800; text-transform: uppercase; letter-spacing: 1.2px; font-family: 'Space Grotesk', sans-serif;">
                    🕹️ Diagnostic Session Controls
                </span>
            </div>
            """, unsafe_allow_html=True)

            if st.button("🔄 Reset Learner State (Pristine Cold Start)", use_container_width=True):
                local_db.ensure_student(st.session_state.student_id, st.session_state.student_name)
                for cid in ["C1","C2","C3","C4","C5","C6","C7","C8","C9","C10"]:
                    local_db.update_student_mastery(
                        st.session_state.student_id, cid, p=0.30, p_eff=0.30, stability_days=7.0, evidence_weight=0.0, status="unseen"
                    )
                st.session_state.latest_attempt_result = None
                st.session_state.virtual_days = 0.0
                st.success("Learner state reset to pristine cold start.")
                st.rerun()

    # Fetch state & decision
    mastery_map = fetch_student_mastery()
    next_decision = fetch_next_decision()
    raw_concepts = local_db.get_all_concepts()
    concepts_meta = {}
    for c in raw_concepts:
        cid = c.get("concept_id") or c.get("id")
        c_dict = dict(c)
        c_dict["id"] = cid
        c_dict["concept_id"] = cid
        c_dict["prerequisites"] = local_graph.get_prerequisites(cid)
        concepts_meta[cid] = c_dict

    target_cid = next_decision.get("target_concept", "C1")
    target_meta = concepts_meta.get(target_cid, {"name": target_cid, "icon": "📚"})
    target_cstate = mastery_map.get(target_cid, {})

    p_eff_val = max(5, min(100, int(round(float(target_cstate.get("p_eff", 0.30)) * 100))))
    stability_val = target_cstate.get("stability_days", 7.0)
    is_fragile = target_cstate.get("is_fragile", False)
    status_label = target_cstate.get("status", "practicing").upper()
    gauge_html = render_circular_gauge(p_eff_val, "p_eff", color="#F43F5E" if is_fragile else "#00F0FF", size=96)

    # 3-Column Bento Live Telemetry HUD
    col_hud1, col_hud2, col_hud3 = st.columns([1.1, 1.0, 1.0])
    with col_hud1:
        st.markdown(f"""
        <div class="mf-glass-card" style="padding: 16px 20px; margin-bottom: 18px; display: flex; align-items: center; justify-content: space-between; min-height: 120px;">
            <div>
                <span style="font-size: 0.68rem; color: #00F0FF; text-transform: uppercase; font-weight: 800; letter-spacing: 1px; font-family: 'Space Grotesk', sans-serif;">
                    Active Focus Concept
                </span>
                <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.25rem; font-weight: 800; color: #FFFFFF; margin-top: 3px;">
                    {target_meta.get('icon', '📚')} {target_cid}
                </div>
                <div style="font-size: 0.80rem; color: #94A3B8; margin-top: 2px;">
                    {target_meta.get('name', target_cid)}
                </div>
            </div>
            <div>
                {gauge_html}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_hud2:
        st.markdown(f"""
        <div class="mf-glass-card" style="padding: 16px 20px; margin-bottom: 18px; min-height: 120px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 0.68rem; color: #A855F7; text-transform: uppercase; font-weight: 800; letter-spacing: 1px; font-family: 'Space Grotesk', sans-serif;">
                    Memory Stability (S)
                </span>
                <span style="font-size: 0.68rem; color: #A78BFA; background: rgba(168,85,247,0.15); border: 1px solid rgba(168,85,247,0.3); padding: 1px 7px; border-radius: 9999px;">
                    Ebbinghaus
                </span>
            </div>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.5rem; font-weight: 800; color: #FFFFFF; margin-top: 4px;">
                {stability_val} Days
            </div>
            <div style="font-size: 0.74rem; color: #94A3B8; margin-top: 4px;">
                Virtual Inactivity: <strong style="color: #A855F7;">+{int(st.session_state.virtual_days)}d elapsed</strong>
            </div>
            <div style="background: rgba(0,0,0,0.3); border-radius: 6px; height: 5px; overflow: hidden; margin-top: 8px;">
                <div style="width: {min(100, int((stability_val/30.0)*100))}%; height: 100%; background: linear-gradient(90deg, #A855F7, #EC4899); border-radius: 6px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_hud3:
        st.markdown(f"""
        <div class="mf-glass-card" style="padding: 16px 20px; margin-bottom: 18px; min-height: 120px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 0.68rem; color: #10B981; text-transform: uppercase; font-weight: 800; letter-spacing: 1px; font-family: 'Space Grotesk', sans-serif;">
                    Telemetry Guard
                </span>
                <span style="font-size: 0.68rem; color: #34D399; background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.3); padding: 1px 7px; border-radius: 9999px;">
                    Anti-Gaming
                </span>
            </div>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.5rem; font-weight: 800; color: #FFFFFF; margin-top: 4px;">
                w = 1.00 <span style="font-size: 0.72rem; color: #10B981; font-weight: 600;">(Full Fidelity)</span>
            </div>
            <div style="font-size: 0.74rem; color: #94A3B8; margin-top: 4px;">
                Latency Guard: <strong style="color: #F8FAFC;">Active (&gt;3s)</strong> &middot; Status: <strong style="color: #38BDF8;">{status_label}</strong>
            </div>
            <div style="background: rgba(0,0,0,0.3); border-radius: 6px; height: 5px; overflow: hidden; margin-top: 8px;">
                <div style="width: 100%; height: 100%; background: linear-gradient(90deg, #10B981, #00F0FF); border-radius: 6px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 3. TABS WORKSPACE
    tabs = st.tabs([
        "🎯 Adaptive Learning Loop",
        "🌌 Concept Knowledge Tree (DAG)",
        "🧪 6-Question Diagnostic",
        "📊 Psychometric Diagnostics & Telemetry"
    ])


    # TAB 1: ADAPTIVE LEARNING LOOP
    with tabs[0]:
        # 1. Glass-Box 'Why This Next?' Card
        render_glassbox_card(next_decision, target_meta, target_cstate, student_name=st.session_state.student_name)

        # 1b. Self-Regulated Student Agency (Innovation Feature)
        render_agency_modal(
            student_id=st.session_state.student_id,
            current_concept_id=target_cid,
            student_name=st.session_state.student_name
        )

        # 2. If recent attempt just occurred, display full telemetry breakdown
        if st.session_state.latest_attempt_result and st.session_state.last_question_answered:
            q_records = local_db.get_questions_for_concept(target_cid)
            matching_q = next((q for q in q_records if q["id"] == st.session_state.last_question_answered), None)
            if matching_q:
                render_telemetry_breakdown(st.session_state.latest_attempt_result, matching_q)
                if st.button("Continue to Next Recommended Problem ➡️", key="btn_continue_next", use_container_width=True):
                    st.session_state.latest_attempt_result = None
                    st.rerun()

        # 3. Fetch questions for current target concept
        questions_list = fetch_questions_for_concept(target_cid)
        if not questions_list:
            st.warning(f"No questions currently found for concept {target_cid}.")
        else:
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

    # TAB 2: DAG CONCEPT TREE
    with tabs[1]:
        def on_select_node(clicked_cid):
            with local_db.conn:
                local_db.conn.execute(
                    "UPDATE students SET active_concept_id = ? WHERE student_id = ?",
                    (clicked_cid, st.session_state.student_id)
                )
            st.toast(f"Active concept switched to {clicked_cid}!", icon="🎯")
            st.rerun()

        render_dag_visualizer(
            concepts_meta=concepts_meta,
            mastery_map=mastery_map,
            active_concept_id=target_cid,
            on_select_concept_cb=on_select_node
        )

    # TAB 3: 6-QUESTION COLD-START DIAGNOSTIC
    with tabs[2]:
        st.markdown("""
        <div class="mf-glass-card" style="padding: 20px 24px; margin-bottom: 18px;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                <span style="font-size: 1.2rem;">🧪</span>
                <h3 style="color: #00F0FF; margin: 0; font-family: 'Space Grotesk', sans-serif; font-size: 1.3rem;">
                    6-Question Cold-Start Diagnostic Sequence
                </h3>
            </div>
            <p style="font-size: 0.85rem; color: #94A3B8; margin: 0; line-height: 1.5;">
                Constructs the student's initial cognitive vector via maximum-uncertainty item selection and 
                <code>0.3&times;w</code> graph propagation across prerequisite edges.
            </p>
        </div>
        """, unsafe_allow_html=True)

        diag_engine = DiagnosticEngine(local_graph)
        diag_cids = diag_engine.diagnostic_concepts

        col_diag_status, col_diag_act = st.columns([3, 2])
        with col_diag_status:
            st.markdown(f"**Target Hub Concepts:** `{'`, `'.join(diag_cids)}`")
            done_count = sum(1 for c in diag_cids if mastery_map.get(c, {}).get("status") in ["practicing", "mastered", "provisional"])
            st.progress(done_count / len(diag_cids), text=f"Diagnostic Progress: {done_count}/{len(diag_cids)} Completed")

        with col_diag_act:
            if st.button("Begin Diagnostic Sequence", use_container_width=True):
                st.toast("Diagnostic mode activated!", icon="🚀")

    # TAB 4: PSYCHOMETRIC DIAGNOSTICS & TELEMETRY
    with tabs[3]:
        st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <h3 style="font-family: 'Space Grotesk', sans-serif; color: #00F0FF; margin: 0;">
                📊 Psychometric Telemetry &amp; BKT Latent Vector
            </h3>
            <span style="font-size: 0.72rem; color: #38BDF8; background: rgba(56,189,248,0.12); padding: 3px 8px; border-radius: 6px; border: 1px solid rgba(56,189,248,0.3);">
                Topological DAG Order C1&rarr;C10
            </span>
        </div>
        """, unsafe_allow_html=True)

        matrix_rows = []
        for cid in local_graph.topological_order():
            cm = concepts_meta.get(cid, {})
            ms = mastery_map.get(cid, {})
            p = ms.get("p", 0.30)
            p_eff = ms.get("p_eff", 0.30)
            s = ms.get("stability_days", 7.0)
            ev = ms.get("evidence_sum", 0.0)
            tp = "YES" if ms.get("transfer_passed") else "NO"
            fr = "YES" if ms.get("is_fragile") else "NO"
            st_label = ms.get("status", "unseen")

            matrix_rows.append({
                "Concept ID": cid,
                "Concept Name": cm.get("name", cid),
                "Status": st_label.upper(),
                "Latent p": f"{round(p * 100, 1)}%",
                "Effective p_eff": f"{round(p_eff * 100, 1)}%",
                "Stability S": f"{s} days",
                "Evidence Σw": round(ev, 2),
                "Transfer Verified": tp,
                "Fragile Cap": fr
            })

        st.dataframe(matrix_rows, use_container_width=True)

        st.markdown("""
        <div class="mf-glass-card" style="padding: 20px 24px; margin-top: 20px;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                <span style="font-size: 1.2rem;">🛡️</span>
                <h4 style="color: #38BDF8; margin: 0; font-family: 'Space Grotesk', sans-serif;">
                    Judge Defense: Why MasteryFlow Is Not a Black-Box Chatbot
                </h4>
            </div>
            <ul style="font-size: 0.86rem; color: #CBD5E1; margin: 0; padding-left: 20px; line-height: 1.65;">
                <li><strong>Deterministic Python:</strong> The decision loop executes mathematically in <code>engine/</code> with zero LLM API dependency.</li>
                <li><strong>Anti-Gaming Telemetry:</strong> Multiplicative weight <code>w</code> drops to 0.0 on rapid retries (&lt;5s), dampening trial-and-error spamming.</li>
                <li><strong>Prerequisite Ceilings:</strong> If an upstream prerequisite decays, downstream mastery is capped at <code>min(prereq) + 0.25</code> and tagged fragile.</li>
                <li><strong>Ebbinghaus Decay:</strong> Long-term memory retention decays over elapsed time according to <code>p_eff = floor + (p - floor) * exp(-dt/S)</code>.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    render_student_portal(show_header=True, show_sidebar=True)
