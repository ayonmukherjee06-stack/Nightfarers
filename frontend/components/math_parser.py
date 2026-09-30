"""
Safe Fraction & Number Input Parser.
ZERO security flaws: strictly regex-based parsing, NO eval(), NO exec(), safe conversion to fractions.Fraction.
"""

import re
from fractions import Fraction
from typing import Optional, Tuple, List, Any


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


def evaluate_student_answer(
    student_raw: str,
    correct_raw: str,
    options: Optional[List[str]] = None
) -> Tuple[bool, Any, Optional[str]]:
    """
    Evaluates student answer against the key across mathematical fractions,
    multiple-choice options, and conceptual text inputs.
    
    1. If both parse as fractions, evaluates mathematical equivalence (e.g. 6/8 == 3/4).
    2. If options are present, checks letter match (A, B, C, D) or option text match.
    3. Fallback checks normalized string equality.
    """
    if not student_raw or not isinstance(student_raw, str):
        return False, None, "Please enter an answer."

    s_clean = student_raw.strip()
    c_clean = str(correct_raw).strip()

    # 1. First attempt: mathematical fraction equivalence
    student_frac, s_err = parse_fraction_input(s_clean)
    correct_frac, c_err = parse_fraction_input(c_clean)

    if student_frac is not None and correct_frac is not None:
        is_correct = (student_frac == correct_frac)
        return is_correct, student_frac, None

    # 2. Second attempt: multiple choice matching (e.g., 'A' or 'B' or 'A) Option Text')
    s_norm = s_clean.lower()
    c_norm = c_clean.lower()

    # Extract single letter if user just typed 'A', 'B', 'C', 'D'
    s_letter = s_norm[:1] if len(s_norm) <= 2 and s_norm[:1] in "abcd" else None
    c_letter = c_norm[:1] if len(c_norm) >= 2 and c_norm[1] in ") ." and c_norm[:1] in "abcd" else None

    if s_letter and c_letter and s_letter == c_letter:
        return True, s_clean, None

    if s_norm == c_norm:
        return True, s_clean, None

    # If student chose option text without prefix (e.g. "Data Link Layer" vs "B) Data Link Layer")
    if c_letter and c_norm.startswith(f"{c_letter})"):
        c_body = c_norm[2:].strip()
        if s_norm == c_body or (len(s_norm) > 4 and s_norm in c_body) or (len(c_body) > 4 and c_body in s_norm):
            return True, s_clean, None

    # If math was expected and fraction parser failed
    if correct_frac is not None and s_err:
        return False, None, s_err

    # Mismatch
    return False, s_clean, None
