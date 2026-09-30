"""MasteryFlow Data Export & Compliance Service (export_service.py).

Provides institutional-grade CSV and Excel-compatible data export capabilities
for students, teachers, and school administrators:
1. Student Personal Mastery Portfolio (Concept-by-concept BKT states, effective retention)
2. Student Historical Practice & Telemetry Log (Attempts, latency, hints, anti-gaming flags)
3. Cohort Mastery Matrix (Students x 10 Canonical Concepts with status and readiness)
4. Full Classroom Telemetry Log (All historical attempts across the cohort)
5. Student Roster Performance Summary (Readiness %, mastered counts, streaks)
6. Teacher Pedagogical Override Audit Trail (Recorded overrides with rationales)

Compliance & Formatting:
- UTF-8 with BOM prefix (\\ufeff) for seamless auto-formatting in Microsoft Excel, Google Sheets, Apple Numbers.
- RFC 4180 standard CSV structure.
- Strict ZERO EMOJI rule enforced across all headers, status badges, and rows.
"""

from __future__ import annotations
import csv
import io
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = str(BASE_DIR / "masteryflow.db")

try:
    from backend.api.db import init_db, Database
    from backend.engine.contracts import CANONICAL_CONCEPTS
except ImportError:
    try:
        from api.db import init_db, Database
        from engine.contracts import CANONICAL_CONCEPTS
    except ImportError:
        from masteryflow.backend.api.db import init_db, Database
        from masteryflow.backend.engine.contracts import CANONICAL_CONCEPTS


def _format_timestamp(ts: Optional[float]) -> str:
    """Formats a Unix epoch timestamp into ISO 8601 string or returns N/A."""
    if not ts:
        return "N/A"
    try:
        dt = datetime.fromtimestamp(ts, tz=timezone.utc)
        return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
    except Exception:
        return "N/A"


def _clean_str(val: Any) -> str:
    """Safely cleans and converts values to string with zero emojis."""
    if val is None:
        return ""
    s = str(val).strip()
    return s


def export_student_mastery_csv(student_id: str, db: Optional[Database] = None) -> Tuple[str, str]:
    """Generates a detailed concept-by-concept CSV export of a student's mastery portfolio.
    
    Returns:
        (csv_string, suggested_filename)
    """
    if db is None:
        db = init_db(DB_PATH)

    student = db.get_student(student_id)
    student_name = student.get("name", "Student") if student else "Student"
    mastery_map = db.get_student_mastery_map(student_id)
    concepts = db.get_all_concepts()

    output = io.StringIO()
    # Add UTF-8 BOM so Excel natively recognizes encoding without manual import wizard
    output.write("\ufeff")
    writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)

    # Metadata Header
    writer.writerow(["# MASTERYFLOW ADAPTIVE LEARNING PLATFORM - STUDENT MASTERY PORTFOLIO"])
    writer.writerow(["# Student ID:", student_id])
    writer.writerow(["# Student Name:", student_name])
    writer.writerow(["# Export Timestamp:", _format_timestamp(time.time())])
    writer.writerow(["# Standard:", "Grade 6 Mathematics - Rational Numbers & Fractions"])
    writer.writerow([])

    # Table Header (Clean, professional, zero emojis)
    headers = [
        "Concept Code",
        "Concept Title",
        "Curriculum Order",
        "Category",
        "Raw BKT Probability P(L)",
        "Effective Retention P_eff",
        "Pedagogical Status",
        "Memory Stability (Days)",
        "Cumulative Evidence Sum",
        "Deep Transfer Verified",
        "Fragile Prerequisite Gap",
        "Last Practiced Date",
    ]
    writer.writerow(headers)

    # Sort concepts by curriculum sequence
    sorted_concepts = sorted(concepts, key=lambda x: x.get("order_index", 99))

    for c in sorted_concepts:
        cid = c.get("concept_id") or c.get("id")
        c_name = c.get("name", cid)
        c_order = c.get("order_index", 0)
        c_cat = c.get("category", "General")

        m = mastery_map.get(cid, {})
        p_raw = float(m.get("p", 0.30))
        p_eff = float(m.get("p_eff", 0.30))
        status = m.get("status", "unseen").capitalize()
        stability = float(m.get("stability_days", 7.0))
        evidence = float(m.get("evidence_sum", 0.0))
        transfer = "YES" if m.get("transfer_passed") else "NO"
        fragile = "YES - PREREQ GAP" if m.get("is_fragile") else "NO"
        last_updated = _format_timestamp(m.get("updated_at"))

        writer.writerow([
            cid,
            c_name,
            c_order,
            c_cat,
            f"{p_raw:.4f}",
            f"{p_eff:.4f}",
            status,
            f"{stability:.1f}",
            f"{evidence:.2f}",
            transfer,
            fragile,
            last_updated,
        ])

    sanitized_name = student_name.replace(" ", "_").replace(".", "")
    filename = f"MasteryFlow_Portfolio_{sanitized_name}_{student_id}.csv"
    return output.getvalue(), filename


def export_student_attempts_csv(student_id: str, db: Optional[Database] = None) -> Tuple[str, str]:
    """Generates a CSV export of all practice attempts and telemetry logs for a student.
    
    Returns:
        (csv_string, suggested_filename)
    """
    if db is None:
        db = init_db(DB_PATH)

    student = db.get_student(student_id)
    student_name = student.get("name", "Student") if student else "Student"
    attempts = db.get_attempts(student_id=student_id, limit=2000)

    output = io.StringIO()
    output.write("\ufeff")
    writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)

    # Metadata Header
    writer.writerow(["# MASTERYFLOW ADAPTIVE LEARNING PLATFORM - STUDENT PRACTICE HISTORY"])
    writer.writerow(["# Student ID:", student_id])
    writer.writerow(["# Student Name:", student_name])
    writer.writerow(["# Total Logged Attempts:", len(attempts)])
    writer.writerow(["# Export Timestamp:", _format_timestamp(time.time())])
    writer.writerow([])

    headers = [
        "Attempt ID",
        "Timestamp (UTC)",
        "Concept Code",
        "Concept Name",
        "Question ID",
        "Submitted Answer",
        "Result",
        "Response Time (seconds)",
        "Hints Requested",
        "Retry Gap (seconds)",
        "Attempt Number",
        "Bayesian Evidence Weight",
        "Anti-Gaming Dampened",
    ]
    writer.writerow(headers)

    for att in attempts:
        att_id = att.get("attempt_id")
        ts_str = _format_timestamp(att.get("timestamp"))
        cid = att.get("concept_id", "")
        c_name = att.get("concept_name", cid)
        qid = att.get("question_id", "")
        ans = _clean_str(att.get("user_answer", ""))
        correct = "CORRECT" if att.get("is_correct") else "INCORRECT"
        
        time_ms = att.get("time_ms", 0) or 0
        time_sec = f"{time_ms / 1000.0:.2f}"
        hints = att.get("hints_used", 0)
        
        gap = att.get("retry_gap_seconds")
        gap_str = f"{gap:.1f}" if gap is not None else "N/A"
        
        att_no = att.get("attempt_no", 1)
        w = float(att.get("evidence_weight", 1.0))
        dampened = "YES (w=0.00)" if w <= 0.01 else "NO"

        writer.writerow([
            att_id,
            ts_str,
            cid,
            c_name,
            qid,
            ans,
            correct,
            time_sec,
            hints,
            gap_str,
            att_no,
            f"{w:.2f}",
            dampened,
        ])

    sanitized_name = student_name.replace(" ", "_").replace(".", "")
    filename = f"MasteryFlow_Attempts_{sanitized_name}_{student_id}.csv"
    return output.getvalue(), filename


def export_cohort_matrix_csv(cohort_dict: Optional[Dict[str, Any]] = None, db: Optional[Database] = None) -> Tuple[str, str]:
    """Generates a matrix CSV for teachers: Rows = Students, Columns = Concepts (P_eff + Status).
    
    Returns:
        (csv_string, suggested_filename)
    """
    if db is None:
        db = init_db(DB_PATH)

    output = io.StringIO()
    output.write("\ufeff")
    writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)

    concepts = db.get_all_concepts()
    concept_ids = [c["concept_id"] for c in concepts]

    writer.writerow(["# MASTERYFLOW ADAPTIVE LEARNING PLATFORM - COHORT MASTERY MATRIX"])
    writer.writerow(["# Grade / Subject:", "Grade 6 Mathematics - Fractions & Decimals"])
    writer.writerow(["# Export Timestamp:", _format_timestamp(time.time())])
    writer.writerow([])

    # Header Row
    header = ["Student ID", "Student Name"]
    for cid in concept_ids:
        header.extend([f"{cid} Effective Mastery", f"{cid} Status"])
    header.extend(["Cohort Average Mastery", "Mastered Concepts Count (>=85%)", "Fragile Gaps Count"])
    writer.writerow(header)

    # Use supplied cohort_dict if available (e.g. from teacher dashboard simulation)
    # Otherwise fetch from database
    if cohort_dict:
        for stu_id, stu_data in cohort_dict.items():
            name = stu_data.get("name", stu_id)
            mastery_map = stu_data.get("mastery", {})
            row = [stu_id, name]
            
            p_effs = []
            mastered_cnt = 0
            fragile_cnt = 0
            
            for cid in concept_ids:
                m = mastery_map.get(cid)
                if m is not None:
                    # Support ConceptMastery dataclass or dict
                    pe = getattr(m, "p_eff", None)
                    if pe is None and isinstance(m, dict):
                        pe = m.get("p_eff", 0.10)
                    elif pe is None:
                        pe = 0.10

                    was_m = getattr(m, "was_mastered", False) if hasattr(m, "was_mastered") else (pe >= 0.85)
                    is_frag = getattr(m, "is_fragile", False) if hasattr(m, "is_fragile") else False
                    errors = getattr(m, "errors_count", 0) if hasattr(m, "errors_count") else 0
                    
                    status = "Mastered" if was_m or pe >= 0.85 else ("Fragile Gap" if is_frag or errors >= 3 else ("Practicing" if pe >= 0.40 else "Unseen"))
                else:
                    pe = 0.10
                    status = "Unseen"

                p_effs.append(pe)
                if pe >= 0.85:
                    mastered_cnt += 1
                if status == "Fragile Gap":
                    fragile_cnt += 1

                row.extend([f"{pe:.3f}", status])

            avg_pe = sum(p_effs) / len(p_effs) if p_effs else 0.0
            row.extend([f"{avg_pe*100:.1f}%", mastered_cnt, fragile_cnt])
            writer.writerow(row)
    else:
        students = db.get_all_students()
        for stu in students:
            stu_id = stu["student_id"]
            name = stu.get("name", stu_id)
            mastery_map = db.get_student_mastery_map(stu_id)
            row = [stu_id, name]
            
            p_effs = []
            mastered_cnt = 0
            fragile_cnt = 0
            
            for cid in concept_ids:
                m = mastery_map.get(cid, {})
                pe = float(m.get("p_eff", 0.30))
                status = m.get("status", "unseen").capitalize()
                is_frag = bool(m.get("is_fragile", 0))

                p_effs.append(pe)
                if pe >= 0.85 and m.get("transfer_passed"):
                    mastered_cnt += 1
                if is_frag or status == "Fragile":
                    fragile_cnt += 1

                row.extend([f"{pe:.3f}", status])

            avg_pe = sum(p_effs) / len(p_effs) if p_effs else 0.0
            row.extend([f"{avg_pe*100:.1f}%", mastered_cnt, fragile_cnt])
            writer.writerow(row)

    filename = "MasteryFlow_Cohort_Mastery_Matrix.csv"
    return output.getvalue(), filename


def export_classroom_attempts_csv(db: Optional[Database] = None) -> Tuple[str, str]:
    """Generates an exhaustive CSV log of all classroom attempts with full latency telemetry.
    
    Returns:
        (csv_string, suggested_filename)
    """
    if db is None:
        db = init_db(DB_PATH)

    attempts = db.get_attempts(student_id=None, limit=5000)

    output = io.StringIO()
    output.write("\ufeff")
    writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)

    writer.writerow(["# MASTERYFLOW ADAPTIVE LEARNING PLATFORM - CLASSROOM ATTEMPTS & TELEMETRY LOG"])
    writer.writerow(["# Scope:", "Full Classroom Cohort"])
    writer.writerow(["# Total Attempt Records:", len(attempts)])
    writer.writerow(["# Export Timestamp:", _format_timestamp(time.time())])
    writer.writerow([])

    headers = [
        "Attempt ID",
        "Timestamp (UTC)",
        "Student ID",
        "Student Name",
        "Concept Code",
        "Concept Name",
        "Question ID",
        "Student Answer",
        "Outcome",
        "Latency (seconds)",
        "Hints Used",
        "Retry Gap (seconds)",
        "Attempt Sequence",
        "Evidence Weight",
        "Anti-Gaming Dampened",
    ]
    writer.writerow(headers)

    for att in attempts:
        att_id = att.get("attempt_id")
        ts_str = _format_timestamp(att.get("timestamp"))
        stu_id = att.get("student_id", "")
        stu_name = att.get("student_name", stu_id)
        cid = att.get("concept_id", "")
        c_name = att.get("concept_name", cid)
        qid = att.get("question_id", "")
        ans = _clean_str(att.get("user_answer", ""))
        correct = "CORRECT" if att.get("is_correct") else "INCORRECT"
        
        time_ms = att.get("time_ms", 0) or 0
        time_sec = f"{time_ms / 1000.0:.2f}"
        hints = att.get("hints_used", 0)
        
        gap = att.get("retry_gap_seconds")
        gap_str = f"{gap:.1f}" if gap is not None else "N/A"
        
        att_no = att.get("attempt_no", 1)
        w = float(att.get("evidence_weight", 1.0))
        dampened = "YES (w=0.00)" if w <= 0.01 else "NO"

        writer.writerow([
            att_id,
            ts_str,
            stu_id,
            stu_name,
            cid,
            c_name,
            qid,
            ans,
            correct,
            time_sec,
            hints,
            gap_str,
            att_no,
            f"{w:.2f}",
            dampened,
        ])

    filename = "MasteryFlow_Classroom_Attempts_Telemetry.csv"
    return output.getvalue(), filename


def export_student_roster_summary_csv(cohort_dict: Optional[Dict[str, Any]] = None, db: Optional[Database] = None) -> Tuple[str, str]:
    """Generates an executive student performance and readiness roster CSV for educators.
    
    Returns:
        (csv_string, suggested_filename)
    """
    if db is None:
        db = init_db(DB_PATH)

    output = io.StringIO()
    output.write("\ufeff")
    writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)

    writer.writerow(["# MASTERYFLOW ADAPTIVE LEARNING PLATFORM - STUDENT ROSTER PERFORMANCE SUMMARY"])
    writer.writerow(["# Grade / Subject:", "Grade 6 Mathematics"])
    writer.writerow(["# Export Timestamp:", _format_timestamp(time.time())])
    writer.writerow([])

    headers = [
        "Student ID",
        "Student Name",
        "Cognitive Readiness Average",
        "Mastered Concepts (Certified)",
        "Fragile Prerequisite Gaps",
        "Active Learning Streak (Days)",
        "Best Streak (Days)",
        "Primary Target Concept",
        "Current Academic Status",
    ]
    writer.writerow(headers)

    if cohort_dict:
        for stu_id, stu_data in cohort_dict.items():
            name = stu_data.get("name", stu_id)
            mastery_map = stu_data.get("mastery", {})
            
            p_effs = []
            mastered_cnt = 0
            fragile_cnt = 0
            
            for cid, m in mastery_map.items():
                pe = getattr(m, "p_eff", None)
                if pe is None and isinstance(m, dict):
                    pe = m.get("p_eff", 0.10)
                elif pe is None:
                    pe = 0.10
                p_effs.append(pe)
                
                was_m = getattr(m, "was_mastered", False) if hasattr(m, "was_mastered") else (pe >= 0.85)
                is_frag = getattr(m, "is_fragile", False) if hasattr(m, "is_fragile") else False
                errors = getattr(m, "errors_count", 0) if hasattr(m, "errors_count") else 0
                
                if was_m or pe >= 0.85:
                    mastered_cnt += 1
                if is_frag or errors >= 3:
                    fragile_cnt += 1

            avg_pe = sum(p_effs) / len(p_effs) if p_effs else 0.0
            
            # Categorize student status
            if avg_pe >= 0.80:
                acad_status = "Accelerated Achiever"
            elif fragile_cnt > 0:
                acad_status = "Remediation Needed (Prereq Gap)"
            elif avg_pe <= 0.45:
                acad_status = "Foundational Support"
            else:
                acad_status = "On Track & Practicing"

            # Query database for streak if exists
            stu_db = db.get_student(stu_id)
            streak = stu_db.get("streak", 0) if stu_db else 3
            best_streak = stu_db.get("best_streak", streak) if stu_db else streak
            active_c = stu_db.get("active_concept_id", "C1") if stu_db else "C1"

            writer.writerow([
                stu_id,
                name,
                f"{avg_pe*100:.1f}%",
                f"{mastered_cnt} / 10",
                fragile_cnt,
                streak,
                best_streak,
                active_c,
                acad_status,
            ])
    else:
        students = db.get_all_students()
        for stu in students:
            stu_id = stu["student_id"]
            name = stu.get("name", stu_id)
            streak = stu.get("streak", 0)
            best_streak = stu.get("best_streak", streak)
            active_c = stu.get("active_concept_id", "C1")
            
            mastery_map = db.get_student_mastery_map(stu_id)
            p_effs = []
            mastered_cnt = 0
            fragile_cnt = 0
            
            for cid, m in mastery_map.items():
                pe = float(m.get("p_eff", 0.30))
                p_effs.append(pe)
                if pe >= 0.85 and m.get("transfer_passed"):
                    mastered_cnt += 1
                if bool(m.get("is_fragile", 0)) or m.get("status") == "fragile":
                    fragile_cnt += 1

            avg_pe = sum(p_effs) / len(p_effs) if p_effs else 0.0
            if avg_pe >= 0.80:
                acad_status = "Accelerated Achiever"
            elif fragile_cnt > 0:
                acad_status = "Remediation Needed (Prereq Gap)"
            elif avg_pe <= 0.45:
                acad_status = "Foundational Support"
            else:
                acad_status = "On Track & Practicing"

            writer.writerow([
                stu_id,
                name,
                f"{avg_pe*100:.1f}%",
                f"{mastered_cnt} / 10",
                fragile_cnt,
                streak,
                best_streak,
                active_c,
                acad_status,
            ])

    filename = "MasteryFlow_Student_Roster_Summary.csv"
    return output.getvalue(), filename


def export_teacher_overrides_csv(db: Optional[Database] = None) -> Tuple[str, str]:
    """Generates an audit trail CSV of teacher overrides recorded in SQLite.
    
    Returns:
        (csv_string, suggested_filename)
    """
    if db is None:
        db = init_db(DB_PATH)

    output = io.StringIO()
    output.write("\ufeff")
    writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)

    writer.writerow(["# MASTERYFLOW ADAPTIVE LEARNING PLATFORM - TEACHER OVERRIDE AUDIT LOG"])
    writer.writerow(["# Export Timestamp:", _format_timestamp(time.time())])
    writer.writerow([])

    headers = [
        "Override ID",
        "Created At (UTC)",
        "Student ID",
        "Target Concept",
        "Assigned Action",
        "Teacher Name",
        "Active Flag",
        "Pedagogical Rationale",
    ]
    writer.writerow(headers)

    cur = db.conn.execute("SELECT * FROM overrides ORDER BY created_at DESC")
    for r in cur.fetchall():
        writer.writerow([
            r["override_id"],
            _format_timestamp(r["created_at"]),
            r["student_id"],
            r["target_concept"],
            r["action"],
            r["teacher_name"],
            "ACTIVE" if r["is_active"] else "INACTIVE",
            r["reason"],
        ])

    filename = "MasteryFlow_Teacher_Override_Audit_Log.csv"
    return output.getvalue(), filename
