"""
Seed realistic multi-subject course progress for all students across all 5 disciplines.
Disciplines:
  1. Mathematics (C1-C10)
  2. Computer Networks (CN1-CN8)
  3. Artificial Intelligence (AI1-AI8)
  4. Formal Languages & Automata (FLA1-FLA8)
  5. Biochemistry (BIO1-BIO8)
"""
import sqlite3
import time
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "masteryflow.db"

def seed_multisubject_progress(db_path: str = None):
    target_path = db_path or str(DB_PATH)
    conn = sqlite3.connect(target_path)
    now = time.time()

    # Target students with profile streaks
    target_students = [
        ("STU_365", "Ayon Mukherjee", 7, 12),
        ("STU_001", "Priya Singh", 9, 14),
        ("STU_042", "Diya Sharma", 4, 6),
        ("STU_002", "Aarav Patel", 1, 3),
        ("STU_004", "Kabir Verma", 0, 8),
        ("STU_005", "Ananya Roy", 6, 7),
        ("STU_006", "Rohan Mehta", 0, 2),
        ("STU_007", "Ishaan Gupta", 1, 1),
        ("STU_008", "Meera Nair", 14, 16),
    ]

    with conn:
        # Ensure all existing and target students are present
        for sid, name, strk, best in target_students:
            conn.execute(
                "INSERT OR IGNORE INTO students (student_id, name, created_at, active_concept_id, streak, best_streak) VALUES (?, ?, ?, 'C1', ?, ?)",
                (sid, name, now, strk, best)
            )
            conn.execute(
                "UPDATE students SET streak = ?, best_streak = ? WHERE student_id = ?",
                (strk, best, sid)
            )

        # Get all concept IDs from concepts table
        cur = conn.execute("SELECT concept_id FROM concepts")
        all_cids = [r[0] for r in cur.fetchall()]

        # Query all student IDs in the database
        cur_stu = conn.execute("SELECT student_id FROM students")
        all_sids = [r[0] for r in cur_stu.fetchall()]

        # Ensure every student in DB has an entry for every concept
        for sid in all_sids:
            for cid in all_cids:
                conn.execute(
                    """INSERT OR IGNORE INTO student_mastery 
                       (student_id, concept_id, p, p_eff, stability_days, evidence_sum, transfer_passed, is_fragile, status, updated_at)
                       VALUES (?, ?, 0.30, 0.30, 7.0, 0.0, 0, 0, 'unseen', ?)""",
                    (sid, cid, now)
                )

    # 1. AYON MUKHERJEE (STU_365) - Advanced Consistent Student (~65-75% per subject)
    ayon_progress = {
        # Mathematics (6 Mastered, 2 Practicing, 1 Provisional, 1 Unseen)
        "C1": (0.96, 0.96, 14.0, 5.2, 1, 0, "mastered"),
        "C2": (0.94, 0.94, 12.0, 4.8, 1, 0, "mastered"),
        "C3": (0.90, 0.90, 11.0, 4.2, 1, 0, "mastered"),
        "C4": (0.92, 0.92, 10.0, 4.5, 1, 0, "mastered"),
        "C5": (0.88, 0.88, 9.0, 3.8, 1, 0, "mastered"),
        "C6": (0.90, 0.90, 9.5, 4.0, 1, 0, "mastered"),
        "C7": (0.72, 0.72, 7.0, 2.5, 0, 0, "practicing"),
        "C8": (0.50, 0.50, 7.0, 1.5, 0, 0, "practicing"),
        "C9": (0.35, 0.35, 7.0, 0.8, 0, 0, "provisional"),
        "C10": (0.20, 0.20, 7.0, 0.0, 0, 0, "unseen"),
        # Computer Networks (5 Mastered, 1 Practicing, 1 Provisional, 1 Unseen)
        "CN1": (0.96, 0.96, 14.0, 5.0, 1, 0, "mastered"),
        "CN2": (0.92, 0.92, 12.0, 4.6, 1, 0, "mastered"),
        "CN3": (0.89, 0.89, 11.0, 4.1, 1, 0, "mastered"),
        "CN4": (0.88, 0.88, 10.0, 3.9, 1, 0, "mastered"),
        "CN5": (0.87, 0.87, 9.0, 3.7, 1, 0, "mastered"),
        "CN6": (0.74, 0.74, 7.0, 2.4, 0, 0, "practicing"),
        "CN7": (0.45, 0.45, 7.0, 1.0, 0, 0, "provisional"),
        "CN8": (0.20, 0.20, 7.0, 0.0, 0, 0, "unseen"),
        # Artificial Intelligence (5 Mastered, 1 Practicing, 1 Provisional, 1 Unseen)
        "AI1": (0.97, 0.97, 15.0, 5.4, 1, 0, "mastered"),
        "AI2": (0.93, 0.93, 12.5, 4.7, 1, 0, "mastered"),
        "AI3": (0.91, 0.91, 11.0, 4.3, 1, 0, "mastered"),
        "AI4": (0.88, 0.88, 10.0, 4.0, 1, 0, "mastered"),
        "AI5": (0.86, 0.86, 9.0, 3.6, 1, 0, "mastered"),
        "AI6": (0.70, 0.70, 7.0, 2.2, 0, 0, "practicing"),
        "AI7": (0.45, 0.45, 7.0, 1.1, 0, 0, "provisional"),
        "AI8": (0.20, 0.20, 7.0, 0.0, 0, 0, "unseen"),
        # Formal Languages & Automata (5 Mastered, 1 Practicing, 1 Provisional, 1 Unseen)
        "FLA1": (0.95, 0.95, 14.0, 5.1, 1, 0, "mastered"),
        "FLA2": (0.92, 0.92, 12.0, 4.5, 1, 0, "mastered"),
        "FLA3": (0.89, 0.89, 10.5, 4.0, 1, 0, "mastered"),
        "FLA4": (0.86, 0.86, 9.0, 3.5, 1, 0, "mastered"),
        "FLA5": (0.85, 0.85, 8.5, 3.4, 1, 0, "mastered"),
        "FLA6": (0.68, 0.68, 7.0, 2.0, 0, 0, "practicing"),
        "FLA7": (0.42, 0.42, 7.0, 0.9, 0, 0, "provisional"),
        "FLA8": (0.20, 0.20, 7.0, 0.0, 0, 0, "unseen"),
        # Biochemistry (5 Mastered, 1 Practicing, 1 Provisional, 1 Unseen)
        "BIO1": (0.96, 0.96, 14.5, 5.2, 1, 0, "mastered"),
        "BIO2": (0.92, 0.92, 12.0, 4.6, 1, 0, "mastered"),
        "BIO3": (0.89, 0.89, 11.0, 4.1, 1, 0, "mastered"),
        "BIO4": (0.87, 0.87, 9.5, 3.8, 1, 0, "mastered"),
        "BIO5": (0.86, 0.86, 9.0, 3.6, 1, 0, "mastered"),
        "BIO6": (0.72, 0.72, 7.0, 2.3, 0, 0, "practicing"),
        "BIO7": (0.45, 0.45, 7.0, 1.0, 0, 0, "provisional"),
        "BIO8": (0.20, 0.20, 7.0, 0.0, 0, 0, "unseen"),
    }

    # 2. PRIYA SINGH (STU_001) - Top Performer (7 Mastered in Math, 6-7 Mastered in others)
    priya_progress = dict(ayon_progress)
    priya_progress.update({
        "C7": (0.90, 0.90, 11.0, 4.8, 1, 0, "mastered"),
        "C8": (0.75, 0.75, 8.0, 3.0, 0, 0, "practicing"),
        "CN6": (0.89, 0.89, 11.0, 4.2, 1, 0, "mastered"),
        "CN7": (0.72, 0.72, 8.0, 2.8, 0, 0, "practicing"),
        "AI6": (0.91, 0.91, 11.0, 4.4, 1, 0, "mastered"),
        "AI7": (0.70, 0.70, 8.0, 2.6, 0, 0, "practicing"),
        "FLA6": (0.88, 0.88, 10.0, 4.0, 1, 0, "mastered"),
        "FLA7": (0.70, 0.70, 8.0, 2.5, 0, 0, "practicing"),
        "BIO6": (0.90, 0.90, 11.0, 4.3, 1, 0, "mastered"),
        "BIO7": (0.72, 0.72, 8.0, 2.7, 0, 0, "practicing"),
    })

    # 3. MEERA NAIR (STU_008) - Capstone Advanced (8/10 Math, 7/8 in other subjects)
    meera_progress = dict(priya_progress)
    meera_progress.update({
        "C8": (0.92, 0.92, 12.0, 4.5, 1, 0, "mastered"),
        "C9": (0.78, 0.78, 8.0, 2.9, 0, 0, "practicing"),
        "CN7": (0.90, 0.90, 11.0, 4.1, 1, 0, "mastered"),
        "CN8": (0.65, 0.65, 7.0, 2.0, 0, 0, "practicing"),
        "AI7": (0.89, 0.89, 10.5, 4.0, 1, 0, "mastered"),
        "AI8": (0.68, 0.68, 7.0, 2.1, 0, 0, "practicing"),
        "FLA7": (0.88, 0.88, 10.0, 3.9, 1, 0, "mastered"),
        "FLA8": (0.66, 0.66, 7.0, 2.0, 0, 0, "practicing"),
        "BIO7": (0.91, 0.91, 11.0, 4.2, 1, 0, "mastered"),
        "BIO8": (0.67, 0.67, 7.0, 2.0, 0, 0, "practicing"),
    })

    # 4. ANANYA ROY (STU_005) - Mid-Level Achiever (4 Mastered per subject)
    ananya_progress = {
        "C1": (0.92, 0.92, 12.0, 4.2, 1, 0, "mastered"),
        "C2": (0.90, 0.90, 11.0, 4.0, 1, 0, "mastered"),
        "C3": (0.87, 0.87, 9.5, 3.6, 1, 0, "mastered"),
        "C4": (0.86, 0.86, 9.0, 3.5, 1, 0, "mastered"),
        "C5": (0.65, 0.65, 7.0, 2.0, 0, 0, "practicing"),
        "C6": (0.35, 0.35, 7.0, 0.8, 0, 0, "provisional"),
        "C7": (0.20, 0.20, 7.0, 0.0, 0, 0, "unseen"),
        "C8": (0.15, 0.15, 7.0, 0.0, 0, 0, "unseen"),
        "C9": (0.15, 0.15, 7.0, 0.0, 0, 0, "unseen"),
        "C10": (0.10, 0.10, 7.0, 0.0, 0, 0, "unseen"),

        "CN1": (0.91, 0.91, 11.0, 4.1, 1, 0, "mastered"),
        "CN2": (0.89, 0.89, 10.0, 3.9, 1, 0, "mastered"),
        "CN3": (0.87, 0.87, 9.0, 3.6, 1, 0, "mastered"),
        "CN4": (0.85, 0.85, 8.5, 3.4, 1, 0, "mastered"),
        "CN5": (0.62, 0.62, 7.0, 1.8, 0, 0, "practicing"),
        "CN6": (0.30, 0.30, 7.0, 0.5, 0, 0, "provisional"),
        "CN7": (0.15, 0.15, 7.0, 0.0, 0, 0, "unseen"),
        "CN8": (0.10, 0.10, 7.0, 0.0, 0, 0, "unseen"),

        "AI1": (0.93, 0.93, 12.0, 4.3, 1, 0, "mastered"),
        "AI2": (0.90, 0.90, 10.5, 4.0, 1, 0, "mastered"),
        "AI3": (0.88, 0.88, 9.5, 3.7, 1, 0, "mastered"),
        "AI4": (0.86, 0.86, 9.0, 3.5, 1, 0, "mastered"),
        "AI5": (0.64, 0.64, 7.0, 1.9, 0, 0, "practicing"),
        "AI6": (0.32, 0.32, 7.0, 0.6, 0, 0, "provisional"),
        "AI7": (0.15, 0.15, 7.0, 0.0, 0, 0, "unseen"),
        "AI8": (0.10, 0.10, 7.0, 0.0, 0, 0, "unseen"),

        "FLA1": (0.92, 0.92, 11.5, 4.2, 1, 0, "mastered"),
        "FLA2": (0.89, 0.89, 10.0, 3.9, 1, 0, "mastered"),
        "FLA3": (0.87, 0.87, 9.0, 3.6, 1, 0, "mastered"),
        "FLA4": (0.85, 0.85, 8.5, 3.4, 1, 0, "mastered"),
        "FLA5": (0.60, 0.60, 7.0, 1.7, 0, 0, "practicing"),
        "FLA6": (0.30, 0.30, 7.0, 0.5, 0, 0, "provisional"),
        "FLA7": (0.15, 0.15, 7.0, 0.0, 0, 0, "unseen"),
        "FLA8": (0.10, 0.10, 7.0, 0.0, 0, 0, "unseen"),

        "BIO1": (0.93, 0.93, 12.0, 4.3, 1, 0, "mastered"),
        "BIO2": (0.90, 0.90, 10.5, 4.0, 1, 0, "mastered"),
        "BIO3": (0.88, 0.88, 9.5, 3.7, 1, 0, "mastered"),
        "BIO4": (0.86, 0.86, 9.0, 3.5, 1, 0, "mastered"),
        "BIO5": (0.63, 0.63, 7.0, 1.8, 0, 0, "practicing"),
        "BIO6": (0.31, 0.31, 7.0, 0.5, 0, 0, "provisional"),
        "BIO7": (0.15, 0.15, 7.0, 0.0, 0, 0, "unseen"),
        "BIO8": (0.10, 0.10, 7.0, 0.0, 0, 0, "unseen"),
    }

    # 5. DIYA SHARMA (STU_042) - Prerequisite Gap
    diya_progress = {
        "C1": (0.88, 0.88, 10.0, 4.0, 1, 0, "mastered"),
        "C2": (0.35, 0.35, 5.0, 1.2, 0, 1, "fragile"),
        "C3": (0.45, 0.45, 6.0, 1.5, 0, 0, "practicing"),
        "C4": (0.25, 0.25, 7.0, 0.0, 0, 0, "unseen"),
        "C5": (0.20, 0.20, 7.0, 0.0, 0, 0, "unseen"),
        "C6": (0.20, 0.20, 7.0, 0.0, 0, 0, "unseen"),
        "C7": (0.40, 0.40, 5.0, 1.8, 0, 1, "fragile"),
        "C8": (0.15, 0.15, 7.0, 0.0, 0, 0, "unseen"),
        "C9": (0.15, 0.15, 7.0, 0.0, 0, 0, "unseen"),
        "C10": (0.10, 0.10, 7.0, 0.0, 0, 0, "unseen"),

        "CN1": (0.88, 0.88, 10.0, 4.0, 1, 0, "mastered"),
        "CN2": (0.34, 0.34, 4.5, 1.1, 0, 1, "fragile"),
        "CN3": (0.42, 0.42, 6.0, 1.3, 0, 0, "practicing"),
        "CN4": (0.20, 0.20, 7.0, 0.0, 0, 0, "unseen"),
        "CN5": (0.38, 0.38, 5.0, 1.4, 0, 1, "fragile"),
        "CN6": (0.15, 0.15, 7.0, 0.0, 0, 0, "unseen"),
        "CN7": (0.15, 0.15, 7.0, 0.0, 0, 0, "unseen"),
        "CN8": (0.10, 0.10, 7.0, 0.0, 0, 0, "unseen"),

        "AI1": (0.89, 0.89, 10.0, 4.1, 1, 0, "mastered"),
        "AI2": (0.33, 0.33, 4.5, 1.0, 0, 1, "fragile"),
        "AI3": (0.44, 0.44, 6.0, 1.4, 0, 0, "practicing"),
        "AI4": (0.20, 0.20, 7.0, 0.0, 0, 0, "unseen"),
        "AI5": (0.36, 0.36, 5.0, 1.2, 0, 1, "fragile"),
        "AI6": (0.15, 0.15, 7.0, 0.0, 0, 0, "unseen"),
        "AI7": (0.15, 0.15, 7.0, 0.0, 0, 0, "unseen"),
        "AI8": (0.10, 0.10, 7.0, 0.0, 0, 0, "unseen"),

        "FLA1": (0.88, 0.88, 10.0, 4.0, 1, 0, "mastered"),
        "FLA2": (0.35, 0.35, 5.0, 1.1, 0, 1, "fragile"),
        "FLA3": (0.40, 0.40, 6.0, 1.3, 0, 0, "practicing"),
        "FLA4": (0.20, 0.20, 7.0, 0.0, 0, 0, "unseen"),
        "FLA5": (0.20, 0.20, 7.0, 0.0, 0, 0, "unseen"),
        "FLA6": (0.15, 0.15, 7.0, 0.0, 0, 0, "unseen"),
        "FLA7": (0.15, 0.15, 7.0, 0.0, 0, 0, "unseen"),
        "FLA8": (0.10, 0.10, 7.0, 0.0, 0, 0, "unseen"),

        "BIO1": (0.89, 0.89, 10.0, 4.2, 1, 0, "mastered"),
        "BIO2": (0.32, 0.32, 4.5, 1.0, 0, 1, "fragile"),
        "BIO3": (0.42, 0.42, 6.0, 1.3, 0, 0, "practicing"),
        "BIO4": (0.20, 0.20, 7.0, 0.0, 0, 0, "unseen"),
        "BIO5": (0.20, 0.20, 7.0, 0.0, 0, 0, "unseen"),
        "BIO6": (0.15, 0.15, 7.0, 0.0, 0, 0, "unseen"),
        "BIO7": (0.15, 0.15, 7.0, 0.0, 0, 0, "unseen"),
        "BIO8": (0.10, 0.10, 7.0, 0.0, 0, 0, "unseen"),
    }

    # 6. AARAV PATEL (STU_002) - Stuck Plateau (Active on Tier 2 with low gains)
    aarav_progress = {
        "C1": (0.86, 0.86, 9.0, 3.5, 1, 0, "mastered"),
        "C2": (0.40, 0.40, 5.0, 2.8, 0, 0, "practicing"),
        "C3": (0.20, 0.20, 7.0, 0.0, 0, 0, "unseen"),
        "C4": (0.15, 0.15, 7.0, 0.0, 0, 0, "unseen"),
        "C5": (0.15, 0.15, 7.0, 0.0, 0, 0, "unseen"),
        "C6": (0.15, 0.15, 7.0, 0.0, 0, 0, "unseen"),
        "C7": (0.10, 0.10, 7.0, 0.0, 0, 0, "unseen"),
        "C8": (0.10, 0.10, 7.0, 0.0, 0, 0, "unseen"),
        "C9": (0.10, 0.10, 7.0, 0.0, 0, 0, "unseen"),
        "C10": (0.10, 0.10, 7.0, 0.0, 0, 0, "unseen"),

        "CN1": (0.85, 0.85, 8.5, 3.2, 1, 0, "mastered"),
        "CN2": (0.38, 0.38, 5.0, 2.5, 0, 0, "practicing"),
        "CN3": (0.20, 0.20, 7.0, 0.0, 0, 0, "unseen"),
        "CN4": (0.15, 0.15, 7.0, 0.0, 0, 0, "unseen"),
        "CN5": (0.15, 0.15, 7.0, 0.0, 0, 0, "unseen"),
        "CN6": (0.15, 0.15, 7.0, 0.0, 0, 0, "unseen"),
        "CN7": (0.10, 0.10, 7.0, 0.0, 0, 0, "unseen"),
        "CN8": (0.10, 0.10, 7.0, 0.0, 0, 0, "unseen"),

        "AI1": (0.86, 0.86, 9.0, 3.4, 1, 0, "mastered"),
        "AI2": (0.39, 0.39, 5.0, 2.6, 0, 0, "practicing"),
        "AI3": (0.20, 0.20, 7.0, 0.0, 0, 0, "unseen"),
        "AI4": (0.15, 0.15, 7.0, 0.0, 0, 0, "unseen"),
        "AI5": (0.15, 0.15, 7.0, 0.0, 0, 0, "unseen"),
        "AI6": (0.15, 0.15, 7.0, 0.0, 0, 0, "unseen"),
        "AI7": (0.10, 0.10, 7.0, 0.0, 0, 0, "unseen"),
        "AI8": (0.10, 0.10, 7.0, 0.0, 0, 0, "unseen"),

        "FLA1": (0.85, 0.85, 8.5, 3.2, 1, 0, "mastered"),
        "FLA2": (0.37, 0.37, 5.0, 2.4, 0, 0, "practicing"),
        "FLA3": (0.20, 0.20, 7.0, 0.0, 0, 0, "unseen"),
        "FLA4": (0.15, 0.15, 7.0, 0.0, 0, 0, "unseen"),
        "FLA5": (0.15, 0.15, 7.0, 0.0, 0, 0, "unseen"),
        "FLA6": (0.15, 0.15, 7.0, 0.0, 0, 0, "unseen"),
        "FLA7": (0.10, 0.10, 7.0, 0.0, 0, 0, "unseen"),
        "FLA8": (0.10, 0.10, 7.0, 0.0, 0, 0, "unseen"),

        "BIO1": (0.86, 0.86, 9.0, 3.3, 1, 0, "mastered"),
        "BIO2": (0.38, 0.38, 5.0, 2.5, 0, 0, "practicing"),
        "BIO3": (0.20, 0.20, 7.0, 0.0, 0, 0, "unseen"),
        "BIO4": (0.15, 0.15, 7.0, 0.0, 0, 0, "unseen"),
        "BIO5": (0.15, 0.15, 7.0, 0.0, 0, 0, "unseen"),
        "BIO6": (0.15, 0.15, 7.0, 0.0, 0, 0, "unseen"),
        "BIO7": (0.10, 0.10, 7.0, 0.0, 0, 0, "unseen"),
        "BIO8": (0.10, 0.10, 7.0, 0.0, 0, 0, "unseen"),
    }

    # 7. KABIR VERMA (STU_004) - Memory Decay (Decays upon simulated inactivity)
    kabir_progress = {
        "C1": (0.90, 0.90, 8.0, 3.8, 1, 0, "mastered"),
        "C2": (0.88, 0.88, 7.5, 3.4, 1, 0, "mastered"),
        "C3": (0.85, 0.85, 7.0, 3.0, 1, 0, "mastered"),
        "C4": (0.50, 0.50, 6.0, 1.5, 0, 0, "practicing"),
        "C5": (0.20, 0.20, 7.0, 0.0, 0, 0, "unseen"),
        "C6": (0.15, 0.15, 7.0, 0.0, 0, 0, "unseen"),
        "C7": (0.15, 0.15, 7.0, 0.0, 0, 0, "unseen"),
        "C8": (0.10, 0.10, 7.0, 0.0, 0, 0, "unseen"),
        "C9": (0.10, 0.10, 7.0, 0.0, 0, 0, "unseen"),
        "C10": (0.10, 0.10, 7.0, 0.0, 0, 0, "unseen"),

        "CN1": (0.89, 0.89, 8.0, 3.6, 1, 0, "mastered"),
        "CN2": (0.86, 0.86, 7.0, 3.1, 1, 0, "mastered"),
        "CN3": (0.48, 0.48, 6.0, 1.4, 0, 0, "practicing"),
        "CN4": (0.20, 0.20, 7.0, 0.0, 0, 0, "unseen"),
        "CN5": (0.15, 0.15, 7.0, 0.0, 0, 0, "unseen"),
        "CN6": (0.15, 0.15, 7.0, 0.0, 0, 0, "unseen"),
        "CN7": (0.10, 0.10, 7.0, 0.0, 0, 0, "unseen"),
        "CN8": (0.10, 0.10, 7.0, 0.0, 0, 0, "unseen"),

        "AI1": (0.91, 0.91, 8.0, 3.8, 1, 0, "mastered"),
        "AI2": (0.87, 0.87, 7.5, 3.2, 1, 0, "mastered"),
        "AI3": (0.46, 0.46, 6.0, 1.3, 0, 0, "practicing"),
        "AI4": (0.20, 0.20, 7.0, 0.0, 0, 0, "unseen"),
        "AI5": (0.15, 0.15, 7.0, 0.0, 0, 0, "unseen"),
        "AI6": (0.15, 0.15, 7.0, 0.0, 0, 0, "unseen"),
        "AI7": (0.10, 0.10, 7.0, 0.0, 0, 0, "unseen"),
        "AI8": (0.10, 0.10, 7.0, 0.0, 0, 0, "unseen"),

        "FLA1": (0.89, 0.89, 8.0, 3.5, 1, 0, "mastered"),
        "FLA2": (0.85, 0.85, 7.0, 3.0, 1, 0, "mastered"),
        "FLA3": (0.45, 0.45, 6.0, 1.2, 0, 0, "practicing"),
        "FLA4": (0.20, 0.20, 7.0, 0.0, 0, 0, "unseen"),
        "FLA5": (0.15, 0.15, 7.0, 0.0, 0, 0, "unseen"),
        "FLA6": (0.15, 0.15, 7.0, 0.0, 0, 0, "unseen"),
        "FLA7": (0.10, 0.10, 7.0, 0.0, 0, 0, "unseen"),
        "FLA8": (0.10, 0.10, 7.0, 0.0, 0, 0, "unseen"),

        "BIO1": (0.90, 0.90, 8.0, 3.7, 1, 0, "mastered"),
        "BIO2": (0.86, 0.86, 7.0, 3.1, 1, 0, "mastered"),
        "BIO3": (0.47, 0.47, 6.0, 1.4, 0, 0, "practicing"),
        "BIO4": (0.20, 0.20, 7.0, 0.0, 0, 0, "unseen"),
        "BIO5": (0.15, 0.15, 7.0, 0.0, 0, 0, "unseen"),
        "BIO6": (0.15, 0.15, 7.0, 0.0, 0, 0, "unseen"),
        "BIO7": (0.10, 0.10, 7.0, 0.0, 0, 0, "unseen"),
        "BIO8": (0.10, 0.10, 7.0, 0.0, 0, 0, "unseen"),
    }

    # 8. ROHAN MEHTA (STU_006) - Adversarial Guesser
    rohan_progress = {
        "C1": (0.45, 0.45, 4.0, 0.8, 0, 1, "practicing"),
        "CN1": (0.42, 0.42, 4.0, 0.7, 0, 1, "practicing"),
        "AI1": (0.44, 0.44, 4.0, 0.8, 0, 1, "practicing"),
        "FLA1": (0.40, 0.40, 4.0, 0.6, 0, 1, "practicing"),
        "BIO1": (0.43, 0.43, 4.0, 0.7, 0, 1, "practicing"),
    }

    # 9. ISHAAN GUPTA (STU_007) - Novice Cold-Start
    ishaan_progress = {
        "C1": (0.50, 0.50, 6.0, 1.2, 0, 0, "practicing"),
        "CN1": (0.48, 0.48, 6.0, 1.1, 0, 0, "practicing"),
        "AI1": (0.49, 0.49, 6.0, 1.1, 0, 0, "practicing"),
        "FLA1": (0.46, 0.46, 6.0, 1.0, 0, 0, "practicing"),
        "BIO1": (0.47, 0.47, 6.0, 1.0, 0, 0, "practicing"),
    }

    # Apply all updates
    updates = [
        ("STU_365", ayon_progress),
        ("STU_001", priya_progress),
        ("STU_008", meera_progress),
        ("STU_005", ananya_progress),
        ("STU_042", diya_progress),
        ("STU_002", aarav_progress),
        ("STU_004", kabir_progress),
        ("STU_006", rohan_progress),
        ("STU_007", ishaan_progress),
    ]

    with conn:
        for sid, pmap in updates:
            for cid, (p, peff, s, ev, trans, frag, stat) in pmap.items():
                conn.execute(
                    """UPDATE student_mastery 
                       SET p=?, p_eff=?, stability_days=?, evidence_sum=?, transfer_passed=?, is_fragile=?, status=?, updated_at=?
                       WHERE student_id=? AND concept_id=?""",
                    (p, peff, s, ev, trans, frag, stat, now, sid, cid)
                )

    conn.close()
    print("Successfully seeded multi-subject course progress across all 5 disciplines for all learner personas!")

if __name__ == "__main__":
    seed_multisubject_progress()
