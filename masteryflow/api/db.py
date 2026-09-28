"""
SQLite Database Layer (9 Tables) & Safe Query Interface (db.py).
Owner: Shreyash Jha (Backend & Persistence Lead)
Implements all 9 relational tables, transactions, parameter sanitization, and audit trails.
"""

import json
import sqlite3
import time
from pathlib import Path
from typing import Any, Dict, List, Optional


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS students (
    student_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    created_at REAL NOT NULL,
    active_concept_id TEXT NOT NULL DEFAULT 'C1',
    streak INTEGER NOT NULL DEFAULT 0,
    best_streak INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS concepts (
    concept_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    category TEXT,
    order_index INTEGER,
    icon TEXT
);

CREATE TABLE IF NOT EXISTS prerequisites (
    prerequisite_id TEXT NOT NULL,
    concept_id TEXT NOT NULL,
    PRIMARY KEY (prerequisite_id, concept_id)
);

CREATE TABLE IF NOT EXISTS questions (
    question_id TEXT PRIMARY KEY,
    concept_id TEXT NOT NULL,
    type TEXT NOT NULL,
    difficulty REAL NOT NULL,
    is_transfer INTEGER NOT NULL DEFAULT 0,
    prompt TEXT NOT NULL,
    correct_answer TEXT NOT NULL,
    eval_expr TEXT,
    hints_json TEXT,
    explanation TEXT,
    FOREIGN KEY (concept_id) REFERENCES concepts (concept_id)
);

CREATE TABLE IF NOT EXISTS student_mastery (
    student_id TEXT NOT NULL,
    concept_id TEXT NOT NULL,
    p REAL NOT NULL DEFAULT 0.30,
    p_eff REAL NOT NULL DEFAULT 0.30,
    stability_days REAL NOT NULL DEFAULT 7.0,
    evidence_sum REAL NOT NULL DEFAULT 0.0,
    transfer_passed INTEGER NOT NULL DEFAULT 0,
    is_fragile INTEGER NOT NULL DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'unseen',
    updated_at REAL NOT NULL,
    PRIMARY KEY (student_id, concept_id),
    FOREIGN KEY (student_id) REFERENCES students (student_id),
    FOREIGN KEY (concept_id) REFERENCES concepts (concept_id)
);

CREATE TABLE IF NOT EXISTS attempts (
    attempt_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    concept_id TEXT NOT NULL,
    question_id TEXT NOT NULL,
    user_answer TEXT,
    is_correct INTEGER NOT NULL,
    confidence TEXT,
    time_ms INTEGER,
    hints_used INTEGER NOT NULL DEFAULT 0,
    retry_gap_seconds REAL,
    attempt_no INTEGER NOT NULL DEFAULT 1,
    evidence_weight REAL NOT NULL,
    timestamp REAL NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students (student_id)
);

CREATE TABLE IF NOT EXISTS decisions (
    decision_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    action TEXT NOT NULL,
    target_concept TEXT NOT NULL,
    reason TEXT NOT NULL,
    config_version INTEGER NOT NULL,
    inputs_json TEXT NOT NULL,
    timestamp REAL NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students (student_id)
);

CREATE TABLE IF NOT EXISTS overrides (
    override_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    target_concept TEXT NOT NULL,
    action TEXT NOT NULL,
    reason TEXT NOT NULL,
    teacher_name TEXT NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at REAL NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students (student_id)
);

CREATE TABLE IF NOT EXISTS audit_log (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL,
    student_id TEXT,
    actor TEXT NOT NULL,
    details_json TEXT NOT NULL,
    timestamp REAL NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_mastery_student ON student_mastery (student_id);
CREATE INDEX IF NOT EXISTS idx_attempts_student ON attempts (student_id);
CREATE INDEX IF NOT EXISTS idx_decisions_student ON decisions (student_id);
CREATE INDEX IF NOT EXISTS idx_overrides_student ON overrides (student_id, is_active);
"""


class Database:
    """Manages SQLite connection, schema migrations, and parameterized operations."""

    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self):
        with self.conn:
            self.conn.executescript(SCHEMA_SQL)

    def close(self):
        self.conn.close()

    def seed_curriculum(self, concepts_path: Optional[str] = None, questions_path: Optional[str] = None):
        """Seeds concepts, prerequisites, and questions safely from JSON files."""
        base_dir = Path(__file__).parent.parent / "data"
        c_path = concepts_path or str(base_dir / "concepts.json")
        q_path = questions_path or str(base_dir / "questions.json")

        if Path(c_path).exists():
            with open(c_path, "r", encoding="utf-8") as f:
                c_data = json.load(f).get("concepts", [])
            with self.conn:
                for c in c_data:
                    self.conn.execute(
                        """INSERT OR REPLACE INTO concepts (concept_id, name, description, category, order_index, icon)
                           VALUES (?, ?, ?, ?, ?, ?)""",
                        (c["id"], c["name"], c.get("description", ""), c.get("category", ""), c.get("order", 1), c.get("icon", "📚"))
                    )
                    for pr in c.get("prerequisites", []):
                        self.conn.execute(
                            "INSERT OR REPLACE INTO prerequisites (prerequisite_id, concept_id) VALUES (?, ?)",
                            (pr, c["id"])
                        )

        if Path(q_path).exists():
            with open(q_path, "r", encoding="utf-8") as f:
                q_data = json.load(f).get("questions", [])
            with self.conn:
                for q in q_data:
                    self.conn.execute(
                        """INSERT OR REPLACE INTO questions 
                           (question_id, concept_id, type, difficulty, is_transfer, prompt, correct_answer, eval_expr, hints_json, explanation)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (
                            q["id"], q["concept_id"], q["type"], q["difficulty"],
                            1 if q.get("is_transfer") else 0,
                            q["prompt"], q["correct_answer"], q.get("eval_expr", ""),
                            json.dumps(q.get("hints", [])), q.get("explanation", "")
                        )
                    )

    def ensure_student(self, student_id: str, name: str = "Learner") -> str:
        """Initializes student records and ensures all 10 concepts are mapped in student_mastery."""
        now = time.time()
        with self.conn:
            self.conn.execute(
                """INSERT OR IGNORE INTO students (student_id, name, created_at, active_concept_id, streak, best_streak)
                   VALUES (?, ?, ?, 'C1', 0, 0)""",
                (student_id, name, now)
            )
            cursor = self.conn.execute("SELECT concept_id FROM concepts")
            for row in cursor.fetchall():
                self.conn.execute(
                    """INSERT OR IGNORE INTO student_mastery 
                       (student_id, concept_id, p, p_eff, stability_days, evidence_sum, transfer_passed, is_fragile, status, updated_at)
                       VALUES (?, ?, 0.30, 0.30, 7.0, 0.0, 0, 0, 'unseen', ?)""",
                    (student_id, row["concept_id"], now)
                )
        return student_id

    def get_student(self, student_id: str) -> Optional[Dict[str, Any]]:
        cursor = self.conn.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def update_streak(self, student_id: str, is_correct: bool) -> int:
        stu = self.get_student(student_id)
        if not stu:
            return 0
        current_streak = stu.get("streak", 0)
        best = stu.get("best_streak", 0)
        if is_correct:
            new_streak = current_streak + 1
            new_best = max(best, new_streak)
        else:
            new_streak = 0
            new_best = best
        with self.conn:
            self.conn.execute(
                "UPDATE students SET streak = ?, best_streak = ? WHERE student_id = ?",
                (new_streak, new_best, student_id)
            )
        return new_streak

    def get_all_concepts(self) -> List[Dict[str, Any]]:
        cursor = self.conn.execute("SELECT * FROM concepts ORDER BY order_index ASC")
        return [dict(r) for r in cursor.fetchall()]

    def get_student_mastery_map(self, student_id: str) -> Dict[str, Dict[str, Any]]:
        cursor = self.conn.execute(
            """SELECT sm.*, c.name, c.icon, c.order_index 
               FROM student_mastery sm 
               JOIN concepts c ON sm.concept_id = c.concept_id 
               WHERE sm.student_id = ? 
               ORDER BY c.order_index ASC""",
            (student_id,)
        )
        return {r["concept_id"]: dict(r) for r in cursor.fetchall()}

    def update_student_mastery(
        self,
        student_id: str,
        concept_id: str,
        p: float,
        p_eff: float,
        stability_days: float,
        evidence_weight: float,
        is_transfer: bool = False,
        is_fragile: bool = False,
        status: Optional[str] = None
    ):
        now = time.time()
        with self.conn:
            # Fetch current evidence sum and transfer status
            cur = self.conn.execute(
                "SELECT evidence_sum, transfer_passed FROM student_mastery WHERE student_id = ? AND concept_id = ?",
                (student_id, concept_id)
            )
            row = cur.fetchone()
            cur_sum = row["evidence_sum"] if row else 0.0
            cur_transfer = bool(row["transfer_passed"]) if row else False

            new_sum = cur_sum + evidence_weight
            transfer_flag = 1 if (cur_transfer or (is_transfer and evidence_weight >= 0.5)) else 0

            # Determine official status
            if status:
                final_status = status
            elif p_eff >= 0.85 and transfer_flag == 1 and new_sum >= 3.0:
                final_status = "mastered"
            elif p_eff >= 0.85:
                final_status = "provisional"
            elif p_eff >= 0.40:
                final_status = "practicing"
            else:
                final_status = "practicing"

            self.conn.execute(
                """UPDATE student_mastery 
                   SET p = ?, p_eff = ?, stability_days = ?, evidence_sum = ?, transfer_passed = ?, is_fragile = ?, status = ?, updated_at = ?
                   WHERE student_id = ? AND concept_id = ?""",
                (p, p_eff, stability_days, new_sum, transfer_flag, 1 if is_fragile else 0, final_status, now, student_id, concept_id)
            )

    def record_attempt(
        self,
        student_id: str,
        concept_id: str,
        question_id: str,
        user_answer: str,
        is_correct: bool,
        confidence: str,
        time_ms: int,
        hints_used: int,
        retry_gap_seconds: Optional[float],
        attempt_no: int,
        evidence_weight: float
    ) -> int:
        now = time.time()
        with self.conn:
            cur = self.conn.execute(
                """INSERT INTO attempts 
                   (student_id, concept_id, question_id, user_answer, is_correct, confidence, time_ms, hints_used, retry_gap_seconds, attempt_no, evidence_weight, timestamp)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (student_id, concept_id, question_id, user_answer, 1 if is_correct else 0, confidence, time_ms, hints_used, retry_gap_seconds, attempt_no, evidence_weight, now)
            )
            return cur.lastrowid

    def record_override(
        self,
        student_id: str,
        target_concept: str,
        action: str,
        reason: str,
        teacher_name: str = "Instructor"
    ) -> int:
        now = time.time()
        with self.conn:
            self.conn.execute("UPDATE overrides SET is_active = 0 WHERE student_id = ?", (student_id,))
            cur = self.conn.execute(
                """INSERT INTO overrides (student_id, target_concept, action, reason, teacher_name, is_active, created_at)
                   VALUES (?, ?, ?, ?, ?, 1, ?)""",
                (student_id, target_concept, action, reason, teacher_name, now)
            )
            override_id = cur.lastrowid
            self.conn.execute(
                """INSERT INTO audit_log (event_type, student_id, actor, details_json, timestamp)
                   VALUES ('TEACHER_OVERRIDE', ?, ?, ?, ?)""",
                (student_id, teacher_name, json.dumps({"override_id": override_id, "target_concept": target_concept, "action": action, "reason": reason}), now)
            )
            return override_id

    def get_active_override(self, student_id: str) -> Optional[Dict[str, Any]]:
        cur = self.conn.execute(
            """SELECT override_id, target_concept, action, reason, teacher_name, created_at 
               FROM overrides WHERE student_id = ? AND is_active = 1 
               ORDER BY created_at DESC LIMIT 1""",
            (student_id,)
        )
        row = cur.fetchone()
        return dict(row) if row else None

    def log_decision(
        self,
        student_id: str,
        action: str,
        target_concept: str,
        reason: str,
        config_version: int,
        inputs_json: str
    ) -> int:
        now = time.time()
        with self.conn:
            cur = self.conn.execute(
                """INSERT INTO decisions (student_id, action, target_concept, reason, config_version, inputs_json, timestamp)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (student_id, action, target_concept, reason, config_version, inputs_json, now)
            )
            return cur.lastrowid

    def get_questions_for_concept(self, concept_id: str) -> List[Dict[str, Any]]:
        cur = self.conn.execute("SELECT * FROM questions WHERE concept_id = ?", (concept_id,))
        rows = [dict(r) for r in cur.fetchall()]
        for r in rows:
            r["id"] = r["question_id"]
            if r.get("hints_json"):
                try:
                    r["hints"] = json.loads(r["hints_json"])
                except Exception:
                    r["hints"] = []
    def get_audit_trail(self, student_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Queries audit log entries with parameterized filters."""
        if student_id:
            cur = self.conn.execute("SELECT * FROM audit_log WHERE student_id = ? ORDER BY timestamp DESC", (student_id,))
        else:
            cur = self.conn.execute("SELECT * FROM audit_log ORDER BY timestamp DESC")
        return [dict(r) for r in cur.fetchall()]


def init_db(db_path: str = "masteryflow.db") -> Database:
    """Initializes and seeds the database."""
    db = Database(db_path)
    db.seed_curriculum()
    return db
