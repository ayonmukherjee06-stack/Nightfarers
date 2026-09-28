"""
Safe Fraction & Number Input Parser.
Owner: Soham Choudhury (Frontend Co-Lead & Question Bank Lead)
ZERO security flaws: strictly regex-based parsing, NO eval(), NO exec(), safe conversion to fractions.Fraction.
"""

import re
from fractions import Fraction
from typing import Optional, Tuple


def parse_fraction_input(raw_input: str) -> Tuple[Optional[Fraction], Optional[str]]:
    """
    Safely parses student input into a canonical fractions.Fraction.
    Supports:
      - Whole numbers: "5", "-2"
      - Simple fractions: "3/4", "-7/8", "6/8"
      - Mixed numbers: "1 1/2", "3 3/4"
      - Decimals: "0.75", "1.5", ".25"
      - Ratios: "3:4" (parsed as Fraction(3, 4))
    
    Returns:
      (Fraction object or None, error_message or None)
    
    Security Guarantee:
      Pure regex matching and integer arithmetic. Completely immune to code injection or eval exploitation.
    """
    if not raw_input or not isinstance(raw_input, str):
        return None, "Please enter an answer."

    cleaned = raw_input.strip()
    if len(cleaned) > 50:
        return None, "Input is too long (max 50 characters)."

    # 1. Check for ratio format: "3:4"
    ratio_match = re.match(r"^(\d+)\s*:\s*(\d+)$", cleaned)
    if ratio_match:
        n, d = int(ratio_match.group(1)), int(ratio_match.group(2))
        if d == 0:
            return None, "Denominator in ratio cannot be zero."
        return Fraction(n, d), None

    # 2. Check for mixed number format: "1 1/2" or "2 3/4"
    mixed_match = re.match(r"^(-?\d+)\s+(\d+)\s*/\s*(\d+)$", cleaned)
    if mixed_match:
        whole = int(mixed_match.group(1))
        n = int(mixed_match.group(2))
        d = int(mixed_match.group(3))
        if d == 0:
            return None, "Denominator cannot be zero."
        frac = Fraction(n, d)
        if whole < 0:
            return whole - frac, None
        return whole + frac, None

    # 3. Check for standard fraction: "3/4" or "-5/6"
    frac_match = re.match(r"^(-?\d+)\s*/\s*(\d+)$", cleaned)
    if frac_match:
        n = int(frac_match.group(1))
        d = int(frac_match.group(2))
        if d == 0:
            return None, "Denominator cannot be zero."
        return Fraction(n, d), None

    # 4. Check for integer: "5" or "-12"
    int_match = re.match(r"^(-?\d+)$", cleaned)
    if int_match:
        return Fraction(int(int_match.group(1)), 1), None

    # 5. Check for decimal: "0.75" or "1.5" or ".5"
    dec_match = re.match(r"^(-?\d*(?:\.\d+)?)$", cleaned)
    if dec_match and cleaned not in ("", "-", "."):
        try:
            # Fraction(str(float_val)) parses decimals exactly (e.g. Fraction('0.75') -> 3/4)
            return Fraction(cleaned), None
        except (ValueError, ZeroDivisionError):
            return None, "Invalid decimal format."

    return None, "Unrecognized format. Please enter a fraction (e.g. 3/4), integer (e.g. 5), or mixed number (e.g. 1 1/2)."


def evaluate_student_answer(student_raw: str, correct_raw: str) -> Tuple[bool, Optional[Fraction], Optional[str]]:
    """
    Evaluates whether the student's input matches the correct fraction answer.
    Handles semantic equivalence: e.g. "6/8" matches "3/4", "0.75" matches "3/4", "1 1/2" matches "3/2".
    """
    student_frac, err = parse_fraction_input(student_raw)
    if err or student_frac is None:
        return False, None, err

    correct_frac, _ = parse_fraction_input(correct_raw)
    if correct_frac is None:
        return False, student_frac, "System error evaluating answer key."

    is_correct = (student_frac == correct_frac)
    return is_correct, student_frac, None
