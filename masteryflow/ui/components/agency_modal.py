"""MasteryFlow Innovation Feature (c): Student Agency Component & Audit Trail.

Authored by: Ayon Mukherjee (Team Lead & Orchestrator)
Role: Empowers learners with self-regulated learning agency by allowing them to
request alternative pedagogical paths ('Request Different Action') with mandatory self-reflection,
logged immutably to SQLite.
"""

from __future__ import annotations
import sqlite3
from typing import Dict, List, Optional, Any
import streamlit as st

try:
    from backend.engine.contracts import ActionType, CANONICAL_CONCEPTS
except ImportError:
    from masteryflow.engine.contracts import ActionType, CANONICAL_CONCEPTS


class StudentAgencyManager:
    """Manages student self-regulated agency requests in SQLite."""

    def __init__(self, db_path: str = "masteryflow.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS student_agency_requests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id TEXT NOT NULL,
                    requested_action TEXT NOT NULL,
                    requested_concept_id TEXT NOT NULL,
                    reason TEXT NOT NULL,
                    status TEXT DEFAULT 'LOGGED_AND_CONSIDERED',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def submit_agency_request(
        self,
        student_id: str,
        requested_action: Any,
        requested_concept_id: str,
        reason: str,
    ) -> int:
        act_val = requested_action.value if hasattr(requested_action, "value") else str(requested_action)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO student_agency_requests (student_id, requested_action, requested_concept_id, reason)
                VALUES (?, ?, ?, ?)
            """, (student_id, act_val, requested_concept_id, reason))
            conn.commit()
            return cursor.lastrowid

    def get_student_agency_requests(self, student_id: Optional[str] = None) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            if student_id:
                cursor.execute("""
                    SELECT id, student_id, requested_action, requested_concept_id, reason, status, created_at
                    FROM student_agency_requests
                    WHERE student_id = ?
                    ORDER BY id DESC
                """, (student_id,))
            else:
                cursor.execute("""
                    SELECT id, student_id, requested_action, requested_concept_id, reason, status, created_at
                    FROM student_agency_requests
                    ORDER BY id DESC
                """)
            return [dict(r) for r in cursor.fetchall()]


def render_agency_modal(student_id: str, current_concept_id: str, student_name: str = "Student") -> None:
    """Renders the self-regulated learning agency interface in Streamlit with modern 2026 dark styling."""
    agency_mgr = StudentAgencyManager("masteryflow.db")

    with st.expander("🙋 Student Agency: Prefer a Different Next Step? (Click to Request Alternative Path)", expanded=False):
        st.markdown(f"""
        <div style="
            background: rgba(14, 20, 42, 0.6);
            border: 1px solid rgba(0, 240, 255, 0.2);
            border-radius: 12px;
            padding: 12px 16px;
            margin-bottom: 14px;
            font-size: 0.86rem;
            color: #E2E8F0;
            line-height: 1.5;
        ">
            <strong style="color: #00F0FF;">Self-Regulated Metacognition:</strong> You are in full control of your learning pace, <strong>{student_name}</strong>.
            If you wish to revisit an earlier prerequisite or jump ahead to an advanced synthesis challenge, submit your reflection below.
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            req_action = st.selectbox(
                "Preferred Pedagogical Action:",
                [ActionType.PRACTICE.value, ActionType.REVIEW.value, ActionType.CHALLENGE.value],
                key=f"agency_act_{student_id}",
            )
        with c2:
            req_concept = st.selectbox(
                "Target Curriculum Concept:",
                list(CANONICAL_CONCEPTS.keys()),
                index=0,
                key=f"agency_cid_{student_id}",
            )

        req_reason = st.text_area(
            "Pedagogical Reason / Metacognitive Reflection:",
            "I want to do 2 more practice questions on foundational fractions before continuing.",
            key=f"agency_reason_{student_id}",
        )

        if st.button("📤 Submit Self-Regulated Agency Request", key=f"btn_agency_{student_id}", type="primary"):
            req_id = agency_mgr.submit_agency_request(
                student_id=student_id,
                requested_action=req_action,
                requested_concept_id=req_concept,
                reason=req_reason,
            )
            st.success(f"✅ Agency Request #{req_id} logged immutably! Your teacher dashboard and psychometric engine have received your learning preference.")
            st.rerun()

        # Show previous requests
        my_reqs = agency_mgr.get_student_agency_requests(student_id)
        if my_reqs:
            st.markdown("""
            <div style="margin-top: 14px; font-size: 0.80rem; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.8px;">
                📝 Recent Agency Audit Trail:
            </div>
            """, unsafe_allow_html=True)
            for r in my_reqs[:3]:
                st.markdown(f"""
                <div style="
                    background: rgba(10, 15, 30, 0.7);
                    border: 1px solid rgba(255, 255, 255, 0.06);
                    border-radius: 8px;
                    padding: 8px 12px;
                    margin-top: 6px;
                    font-size: 0.78rem;
                    color: #CBD5E1;
                ">
                    <strong style="color: #38BDF8;">{r['requested_action']}</strong> on 
                    <strong style="color: #A855F7;">{r['requested_concept_id']}</strong> 
                    <span style="color: #64748B;">({r['created_at']})</span>: 
                    <em>&ldquo;{r['reason']}&rdquo;</em>
                </div>
                """, unsafe_allow_html=True)


# Backward compatibility alias
render_agency_drawer = render_agency_modal
