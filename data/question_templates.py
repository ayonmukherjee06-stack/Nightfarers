"""
Question Templates & Dynamic Parameterized Problem Generators.
Owner: Soham Choudhury (Question Bank, Anti-Gaming & Simulation Lead)
Generates randomized fraction problems with mathematically exact answers verified via Python's fractions.Fraction.
"""

import math
import random
from fractions import Fraction
from typing import Any, Dict, Optional


def generate_c1_basics(rng: Optional[random.Random] = None) -> Dict[str, Any]:
    """Generates a dynamic C1 (Fraction Basics & Visual Part-Whole) problem."""
    r = rng or random.Random()
    total_parts = r.randint(4, 12)
    shaded_parts = r.randint(1, total_parts - 1)
    ans = Fraction(shaded_parts, total_parts)
    return {
        "concept_id": "C1",
        "type": "easy",
        "difficulty": round(0.15 + 0.15 * (shaded_parts / total_parts), 2),
        "is_transfer": False,
        "prompt": f"A geometric strip is partitioned into {total_parts} equal cells. {shaded_parts} cells are filled with blue light. What fraction of the strip is illuminated in simplest form?",
        "correct_answer": str(ans),
        "fraction_value": ans,
        "parameters": {"total": total_parts, "shaded": shaded_parts},
        "hints": [
            f"The denominator represents the total number of cells: {total_parts}.",
            f"The numerator represents illuminated cells: {shaded_parts}.",
            f"Write as {shaded_parts}/{total_parts} and simplify to lowest terms."
        ],
        "explanation": f"{shaded_parts} parts out of {total_parts} = {shaded_parts}/{total_parts} = {ans}."
    }


def generate_c2_equivalent(rng: Optional[random.Random] = None) -> Dict[str, Any]:
    """Generates a dynamic C2 (Equivalent Fractions & Simplification) problem."""
    r = rng or random.Random()
    base_num = r.choice([1, 2, 3, 5])
    base_den = r.choice([2, 3, 4, 5, 6, 7])
    while math.gcd(base_num, base_den) != 1 or base_num >= base_den:
        base_den = r.randint(base_num + 1, 9)
    scale = r.randint(2, 6)
    scaled_num = base_num * scale
    scaled_den = base_den * scale
    ans = Fraction(scaled_num, scaled_den)
    return {
        "concept_id": "C2",
        "type": "medium",
        "difficulty": round(0.35 + 0.05 * scale, 2),
        "is_transfer": False,
        "prompt": f"Simplify the fraction {scaled_num}/{scaled_den} to its lowest terms.",
        "correct_answer": str(ans),
        "fraction_value": ans,
        "parameters": {"num": scaled_num, "den": scaled_den, "scale": scale},
        "hints": [
            f"Find the greatest common divisor of {scaled_num} and {scaled_den}.",
            f"Both numbers are divisible by {scale}.",
            f"Divide numerator and denominator by {scale}."
        ],
        "explanation": f"{scaled_num}/{scaled_den} ÷ {scale}/{scale} = {ans}."
    }


def generate_c3_comparing(rng: Optional[random.Random] = None) -> Dict[str, Any]:
    """Generates a dynamic C3 (Comparing & Ordering Fractions) problem."""
    r = rng or random.Random()
    d1 = r.choice([3, 4, 5, 6])
    d2 = r.choice([7, 8, 9, 10])
    n1 = r.randint(1, d1 - 1)
    n2 = r.randint(1, d2 - 1)
    f1 = Fraction(n1, d1)
    f2 = Fraction(n2, d2)
    while f1 == f2:
        n2 = r.randint(1, d2 - 1)
        f2 = Fraction(n2, d2)
    diff = abs(f1 - f2)
    larger = max(f1, f2)
    smaller = min(f1, f2)
    return {
        "concept_id": "C3",
        "type": "medium",
        "difficulty": 0.55,
        "is_transfer": False,
        "prompt": f"Compute the positive difference between {f1} and {f2} (larger minus smaller) in simplest form.",
        "correct_answer": str(diff),
        "fraction_value": diff,
        "parameters": {"f1": str(f1), "f2": str(f2), "larger": str(larger), "smaller": str(smaller)},
        "hints": [
            f"Find a common denominator for {d1} and {d2}.",
            f"Convert to common denominator: larger is {larger}, smaller is {smaller}.",
            f"Subtract {larger} - {smaller}."
        ],
        "explanation": f"{larger} - {smaller} = {diff}."
    }


def generate_c4_addition(rng: Optional[random.Random] = None) -> Dict[str, Any]:
    """Generates a dynamic C4 (Adding and Subtracting Fractions) problem."""
    r = rng or random.Random()
    d1 = r.choice([2, 3, 4, 5, 6])
    d2 = r.choice([3, 4, 5, 6, 8])
    n1 = r.randint(1, d1 - 1)
    n2 = r.randint(1, d2 - 1)
    f1 = Fraction(n1, d1)
    f2 = Fraction(n2, d2)
    ans = f1 + f2
    return {
        "concept_id": "C4",
        "type": "medium" if d1 != d2 else "easy",
        "difficulty": 0.48 if d1 != d2 else 0.22,
        "is_transfer": False,
        "prompt": f"Compute the sum of {f1} + {f2}. Express the answer in simplest form.",
        "correct_answer": str(ans),
        "fraction_value": ans,
        "parameters": {"f1": str(f1), "f2": str(f2)},
        "hints": [
            f"Find the least common denominator of {f1.denominator} and {f2.denominator}.",
            "Scale the fractions to the common denominator.",
            "Add the numerators together and simplify."
        ],
        "explanation": f"{f1} + {f2} = {ans}."
    }


def generate_c5_multiplication(rng: Optional[random.Random] = None) -> Dict[str, Any]:
    """Generates a dynamic C5 (Multiplying and Dividing Fractions) problem."""
    r = rng or random.Random()
    n1, d1 = r.randint(1, 5), r.randint(2, 7)
    n2, d2 = r.randint(1, 5), r.randint(2, 7)
    f1 = Fraction(n1, d1)
    f2 = Fraction(n2, d2)
    ans = f1 * f2
    return {
        "concept_id": "C5",
        "type": "medium",
        "difficulty": 0.50,
        "is_transfer": False,
        "prompt": f"Multiply the fractions: {f1} × {f2}. Express the product in simplest form.",
        "correct_answer": str(ans),
        "fraction_value": ans,
        "parameters": {"f1": str(f1), "f2": str(f2)},
        "hints": [
            f"Multiply the numerators: {f1.numerator} × {f2.numerator}.",
            f"Multiply the denominators: {f1.denominator} × {f2.denominator}.",
            "Simplify to lowest terms."
        ],
        "explanation": f"{f1} × {f2} = {ans}."
    }


def generate_c6_ratio_basics(rng: Optional[random.Random] = None) -> Dict[str, Any]:
    """Generates a dynamic C6 (Ratio Basics: Part:Part, Part:Whole) problem."""
    r = rng or random.Random()
    part_a = r.randint(2, 7)
    part_b = r.randint(2, 7)
    while part_a == part_b:
        part_b = r.randint(2, 7)
    total = part_a + part_b
    ans = Fraction(part_a, total)
    return {
        "concept_id": "C6",
        "type": "easy",
        "difficulty": 0.25,
        "is_transfer": False,
        "prompt": f"A chemical solution has a ratio of compound Alpha to compound Beta of {part_a}:{part_b}. What fraction of the total solution is compound Alpha? Express in simplest form.",
        "correct_answer": str(ans),
        "fraction_value": ans,
        "parameters": {"part_a": part_a, "part_b": part_b, "total": total},
        "hints": [
            f"Find total ratio parts: {part_a} + {part_b} = {total}.",
            f"Compound Alpha is {part_a} out of {total} parts.",
            f"Write as {part_a}/{total} and simplify."
        ],
        "explanation": f"Alpha represents {part_a} out of {total} parts: {part_a}/{total} = {ans}."
    }


def generate_c7_unit_rate(rng: Optional[random.Random] = None) -> Dict[str, Any]:
    """Generates a dynamic C7 (Equivalent Ratios and Unit Rate) problem."""
    r = rng or random.Random()
    unit = r.randint(4, 15)
    hours = r.randint(2, 6)
    total_km = unit * hours
    ans = Fraction(total_km, hours)
    return {
        "concept_id": "C7",
        "type": "easy",
        "difficulty": 0.22,
        "is_transfer": False,
        "prompt": f"A solar rover travels {total_km} kilometers across terrain in {hours} hours. What is its unit speed in kilometers per hour?",
        "correct_answer": str(ans),
        "fraction_value": ans,
        "parameters": {"total_km": total_km, "hours": hours, "unit": unit},
        "hints": [
            f"Unit rate = total distance ÷ total time: {total_km} ÷ {hours}."
        ],
        "explanation": f"{total_km} ÷ {hours} = {ans} km/h."
    }


def generate_c8_proportion(rng: Optional[random.Random] = None) -> Dict[str, Any]:
    """Generates a dynamic C8 (Proportion: solve a/b = c/d) problem."""
    r = rng or random.Random()
    a = r.randint(2, 6)
    b = r.randint(3, 8)
    multiplier = r.randint(2, 5)
    c = a * multiplier
    ans = Fraction(b * c, a)  # d = b * multiplier
    return {
        "concept_id": "C8",
        "type": "medium",
        "difficulty": 0.50,
        "is_transfer": False,
        "prompt": f"Solve for unknown variable d in the proportion: {a}/{b} = {c}/d. Enter the value of d.",
        "correct_answer": str(ans),
        "fraction_value": ans,
        "parameters": {"a": a, "b": b, "c": c, "d": str(ans)},
        "hints": [
            f"Notice that the numerator {a} was multiplied by {multiplier} to get {c}.",
            f"Multiply the denominator {b} by the same scale factor {multiplier}.",
            f"Or cross-multiply: d = ({b} × {c}) ÷ {a}."
        ],
        "explanation": f"d = ({b} × {c}) / {a} = {ans}."
    }


GENERATOR_REGISTRY = {
    "C1": generate_c1_basics,
    "C2": generate_c2_equivalent,
    "C3": generate_c3_comparing,
    "C4": generate_c4_addition,
    "C5": generate_c5_multiplication,
    "C6": generate_c6_ratio_basics,
    "C7": generate_c7_unit_rate,
    "C8": generate_c8_proportion,
}


def generate_question(concept_id: str, rng: Optional[random.Random] = None) -> Dict[str, Any]:
    """Generates a randomized question for any supported concept with exact fractions.Fraction evaluation."""
    if concept_id not in GENERATOR_REGISTRY:
        raise ValueError(f"Concept {concept_id} does not have a registered template generator.")
    return GENERATOR_REGISTRY[concept_id](rng)
