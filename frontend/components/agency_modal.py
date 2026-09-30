"""MasteryFlow Student Agency Component (agency_modal.py).

Empowers learners with self-regulated learning choices, allowing them to request
alternative practice topics with brief self-reflection in clean light design.
"""

from __future__ import annotations
import sqlite3
from typing import Dict, List, Optional, Any
import streamlit as st

try:
    from backend.engine.contracts import ActionType, CANONICAL_CONCEPTS
except ImportError:
    from masteryflow.engine.contracts import ActionType, CANONICAL_CONCEPTS

try:
    from frontend.components.theme import render_html
except ImportError:
    from .theme import render_html


def _connect_db(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path, timeout=30.0)
    try:
        conn.execute("PRAGMA busy_timeout = 30000;")
    except Exception:
        pass
    return conn


class StudentAgencyManager:
    """Manages student self-regulated agency requests in SQLite."""

    def __init__(self, db_path: str = "masteryflow.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        with _connect_db(self.db_path) as conn:
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
        with _connect_db(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO student_agency_requests (student_id, requested_action, requested_concept_id, reason)
                VALUES (?, ?, ?, ?)
            """, (student_id, act_val, requested_concept_id, reason))
            conn.commit()
            return cursor.lastrowid

    def get_student_agency_requests(self, student_id: Optional[str] = None) -> List[Dict[str, Any]]:
        with _connect_db(self.db_path) as conn:
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
    """Renders the self-regulated learning choice drawer in clean light design."""
    agency_mgr = StudentAgencyManager("masteryflow.db")

    with st.expander("Want to explore an alternate topic? Choose your learning path", expanded=False):
        render_html(f"""
        <div style="
            background: rgba(15, 23, 42, 0.82);
            border: 1px solid rgba(148, 163, 184, 0.16);
            border-radius: 12px;
            padding: 14px 18px;
            margin-bottom: 14px;
            font-size: 0.88rem;
            color: #E2E8F0;
            line-height: 1.55;
            box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.3);
        ">
            You can guide your own learning pace, <strong style="color: #38BDF8;">{student_name}</strong>. If you feel like reviewing an earlier topic or trying a challenge, let us know below.
        </div>
        """)

        c1, c2 = st.columns(2)
        with c1:
            req_action = st.selectbox(
                "Preferred Activity:",
                [ActionType.PRACTICE.value, ActionType.REVIEW.value, ActionType.CHALLENGE.value],
                key=f"agency_act_{student_id}",
            )
        with c2:
            req_concept = st.selectbox(
                "Target Concept:",
                list(CANONICAL_CONCEPTS.keys()),
                index=0,
                key=f"agency_cid_{student_id}",
            )

        req_reason = st.text_area(
            "Your reflection / reason:",
            "I want to practice more on this concept before moving ahead.",
            key=f"agency_reason_{student_id}",
        )

        if st.button("Submit Learning Path Request", key=f"btn_agency_{student_id}", type="primary"):
            req_id = agency_mgr.submit_agency_request(
                student_id=student_id,
                requested_action=req_action,
                requested_concept_id=req_concept,
                reason=req_reason,
            )
            st.success(f"Request #{req_id} logged. Your preference has been shared with your teacher.")
            st.rerun()

        my_reqs = agency_mgr.get_student_agency_requests(student_id)
        if my_reqs:
            render_html("""
            <div style="margin-top: 14px; font-size: 0.78rem; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.5px;">
                Previous Requests:
            </div>
            """)
            for r in my_reqs[:3]:
                render_html(f"""
                <div style="
                    background: rgba(17, 24, 39, 0.75);
                    backdrop-filter: blur(14px);
                    border: 1px solid rgba(148, 163, 184, 0.16);
                    border-radius: 10px;
                    padding: 10px 14px;
                    margin-top: 6px;
                    font-size: 0.80rem;
                    color: #CBD5E1;
                    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25);
                ">
                    <strong style="color: #38BDF8;">{r['requested_action']}</strong> on 
                    <strong style="color: #A78BFA;">{r['requested_concept_id']}</strong> 
                    <span style="color: #94A3B8;">({r['created_at']})</span>: 
                    <em>&ldquo;{r['reason']}&rdquo;</em>
                </div>
                """)


render_agency_drawer = render_agency_modal
