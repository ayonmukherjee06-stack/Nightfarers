"""
Test 9: Question Bank Programmatic Exactness Verification.
Owner: Soham Choudhury (Frontend Co-Lead & Question Bank Lead)
Guarantees 100% of stored answers match Python's fractions.Fraction with zero hallucination.
"""

import json
import sys
from fractions import Fraction
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from data.question_templates import GENERATOR_REGISTRY, generate_question


def test_question_bank_exactness():
    """
    Test 9: Question Bank Exactness
    Iterates through all 50 questions in questions.json, evaluates their mathematical expressions,
    and proves stored answers equal computed fractions with 100% exactness.
    """
    q_path = Path(__file__).parent.parent / "data" / "questions.json"
    assert q_path.exists(), f"Questions file missing at {q_path}"

    with open(q_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    questions = data.get("questions", [])
    assert len(questions) == 50, f"Expected exactly 50 questions, found {len(questions)}"

    # Check that every concept C1-C10 has exactly 5 questions
    concept_counts = {}
    for q in questions:
        cid = q["concept_id"]
        concept_counts[cid] = concept_counts.get(cid, 0) + 1

        # Check required fields
        assert "prompt" in q and len(q["prompt"]) > 5
        assert "hints" in q and len(q["hints"]) >= 2
        assert "explanation" in q and len(q["explanation"]) > 5
        assert "difficulty" in q and 0.0 <= q["difficulty"] <= 1.0

        # Programmatic Fraction Verification
        stored_ans = q["correct_answer"]
        eval_expr = q.get("eval_expr")
        assert eval_expr, f"Question {q['id']} is missing eval_expr for programmatic verification"

        # Evaluate ground-truth fraction mathematically
        computed_fraction = eval(eval_expr, {"Fraction": Fraction, "max": max, "min": min})
        assert str(computed_fraction) == stored_ans, (
            f"Math mismatch in question {q['id']}! "
            f"Stored '{stored_ans}' does not equal computed '{computed_fraction}'"
        )

    for i in range(1, 11):
        cid = f"C{i}"
        assert concept_counts.get(cid) == 5, f"Concept {cid} must have exactly 5 questions"


def test_parameterized_generators():
    """
    Verifies that parameterized dynamic question generators produce valid fractions and correct answers.
    """
    for cid in GENERATOR_REGISTRY:
        q = generate_question(cid)
        assert q["concept_id"] == cid
        assert "prompt" in q
        assert "correct_answer" in q
        assert isinstance(q["fraction_value"], Fraction)
        assert str(q["fraction_value"]) == q["correct_answer"]
