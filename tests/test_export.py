"""Unit tests for the MasteryFlow Data Export Service (tests/test_export.py).

Verifies:
1. Student Mastery Portfolio CSV structure and completeness.
2. Student Practice Attempts & Telemetry CSV structure.
3. Cohort Mastery Matrix CSV structure (Excel compatibility).
4. Full Classroom Attempts CSV structure.
5. Student Roster Summary CSV structure.
6. Teacher Override Audit Log CSV structure.
7. RFC 4180 parsing validity with Python standard csv reader.
8. Zero emojis across all exported CSV texts.
9. Presence of UTF-8 BOM (\\ufeff) for seamless Microsoft Excel import.
"""

import csv
import io
import re
import pytest
from frontend.components.export_service import (
    export_student_mastery_csv,
    export_student_attempts_csv,
    export_cohort_matrix_csv,
    export_classroom_attempts_csv,
    export_student_roster_summary_csv,
    export_teacher_overrides_csv,
)
from backend.api.db import init_db


@pytest.fixture
def db():
    return init_db("masteryflow.db")


def test_export_student_mastery_csv(db):
    csv_str, filename = export_student_mastery_csv("STU_042", db=db)
    
    assert filename.startswith("MasteryFlow_Portfolio_")
    assert filename.endswith(".csv")
    assert csv_str.startswith("\ufeff")  # Excel BOM check
    
    # Check no emojis
    emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]', flags=re.UNICODE)
    assert not emoji_pattern.findall(csv_str)
    
    # Parse with csv reader
    f = io.StringIO(csv_str.lstrip("\ufeff"))
    reader = csv.reader(f)
    rows = [r for r in reader if r and not r[0].startswith("#")]
    
    assert len(rows) >= 11  # 1 header + 10 concepts
    header = rows[0]
    assert "Concept Code" in header
    assert "Effective Retention P_eff" in header
    assert "Pedagogical Status" in header


def test_export_student_attempts_csv(db):
    csv_str, filename = export_student_attempts_csv("STU_042", db=db)
    
    assert filename.startswith("MasteryFlow_Attempts_")
    assert filename.endswith(".csv")
    assert csv_str.startswith("\ufeff")
    
    emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]', flags=re.UNICODE)
    assert not emoji_pattern.findall(csv_str)
    
    f = io.StringIO(csv_str.lstrip("\ufeff"))
    reader = csv.reader(f)
    rows = [r for r in reader if r and not r[0].startswith("#")]
    assert len(rows) >= 1
    assert "Attempt ID" in rows[0]
    assert "Bayesian Evidence Weight" in rows[0]


def test_export_cohort_matrix_csv(db):
    csv_str, filename = export_cohort_matrix_csv(cohort_dict=None, db=db)
    
    assert filename == "MasteryFlow_Cohort_Mastery_Matrix.csv"
    assert csv_str.startswith("\ufeff")
    
    emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]', flags=re.UNICODE)
    assert not emoji_pattern.findall(csv_str)
    
    f = io.StringIO(csv_str.lstrip("\ufeff"))
    reader = csv.reader(f)
    rows = [r for r in reader if r and not r[0].startswith("#")]
    
    assert len(rows) >= 2  # Header + at least 1 student
    header = rows[0]
    assert "Student ID" in header
    assert "Student Name" in header
    assert "C1 Effective Mastery" in header
    assert "Cohort Average Mastery" in header


def test_export_classroom_attempts_csv(db):
    csv_str, filename = export_classroom_attempts_csv(db=db)
    
    assert filename == "MasteryFlow_Classroom_Attempts_Telemetry.csv"
    assert csv_str.startswith("\ufeff")
    
    emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]', flags=re.UNICODE)
    assert not emoji_pattern.findall(csv_str)
    
    f = io.StringIO(csv_str.lstrip("\ufeff"))
    reader = csv.reader(f)
    rows = [r for r in reader if r and not r[0].startswith("#")]
    assert "Student ID" in rows[0]
    assert "Latency (seconds)" in rows[0]


def test_export_student_roster_summary_csv(db):
    csv_str, filename = export_student_roster_summary_csv(cohort_dict=None, db=db)
    
    assert filename == "MasteryFlow_Student_Roster_Summary.csv"
    assert csv_str.startswith("\ufeff")
    
    emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]', flags=re.UNICODE)
    assert not emoji_pattern.findall(csv_str)
    
    f = io.StringIO(csv_str.lstrip("\ufeff"))
    reader = csv.reader(f)
    rows = [r for r in reader if r and not r[0].startswith("#")]
    assert len(rows) >= 2
    header = rows[0]
    assert "Cognitive Readiness Average" in header
    assert "Mastered Concepts (Certified)" in header
    assert "Current Academic Status" in header


def test_export_teacher_overrides_csv(db):
    csv_str, filename = export_teacher_overrides_csv(db=db)
    
    assert filename == "MasteryFlow_Teacher_Override_Audit_Log.csv"
    assert csv_str.startswith("\ufeff")
    
    emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]', flags=re.UNICODE)
    assert not emoji_pattern.findall(csv_str)
    
    f = io.StringIO(csv_str.lstrip("\ufeff"))
    reader = csv.reader(f)
    rows = [r for r in reader if r and not r[0].startswith("#")]
    assert "Override ID" in rows[0]
    assert "Teacher Name" in rows[0]
