"""MasteryFlow Engine Contracts & Protocols.

Authored by: Ayon Mukherjee (Team Lead & Orchestrator)
Role: Definitive Type Contracts and Data Protocols for Engine, UI, and Backend integration.
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Dict, List, Optional, Any, Set
import copy


class ActionType(str, Enum):
    """The 6 Deterministic Pedagogical Action Types in MasteryFlow."""
    TEACHER_INTERVENTION = "TEACHER_INTERVENTION"
    REMEDIATE_PREREQUISITE = "REMEDIATE_PREREQUISITE"
    REVIEW = "REVIEW"
    PRACTICE = "PRACTICE"
    ADVANCE = "ADVANCE"
    CHALLENGE = "CHALLENGE"


# The 10 Canonical Concepts for Fractions, Ratios, and Proportions (Domain 4: EduGenAI)
CANONICAL_CONCEPTS: Dict[str, Dict[str, Any]] = {
    "C1": {
        "title": "Fraction basics (part-whole, number line)",
        "prereqs": [],
        "description": "Baseline foundation: visual unit fractions, fractional values on a 0-to-1 number line.",
    },
    "C2": {
        "title": "Equivalent fractions and simplifying",
        "prereqs": ["C1"],
        "description": "Equivalence property via common divisors; reducing fractions to lowest terms.",
    },
    "C3": {
        "title": "Comparing and ordering fractions",
        "prereqs": ["C2"],
        "description": "Cross-multiplication and least common denominator comparison.",
    },
    "C4": {
        "title": "Adding and subtracting fractions",
        "prereqs": ["C2"],
        "description": "Addition and subtraction with like and unlike denominators.",
    },
    "C5": {
        "title": "Multiplying and dividing fractions",
        "prereqs": ["C2"],
        "description": "Area model multiplication and reciprocal division algorithms.",
    },
    "C6": {
        "title": "Ratio basics (part:part, part:whole)",
        "prereqs": ["C1", "C2"],
        "description": "Representing relational quantities as simplified colon ratios and fraction ratios.",
    },
    "C7": {
        "title": "Equivalent ratios and unit rate",
        "prereqs": ["C6", "C5"],
        "description": "Scaling ratios up/down and computing per-unit rates.",
    },
    "C8": {
        "title": "Proportion (solve a/b = c/d)",
        "prereqs": ["C7"],
        "description": "Algebraic cross-multiplication to solve missing variable proportions.",
    },
    "C9": {
        "title": "Percentages as ratios",
        "prereqs": ["C3", "C6"],
        "description": "Relating parts per hundred to simplified fractions and decimal equivalents.",
    },
    "C10": {
        "title": "Proportion word problems & scaling",
        "prereqs": ["C8", "C9"],
        "description": "Capstone multi-step real-world modeling: recipe scaling, map distances, rate problems.",
    },
}

try:
    from data.curricula import (
        NETWORKS_CONCEPTS,
        AI_CONCEPTS,
        FLA_CONCEPTS,
        BIOCHEM_CONCEPTS,
        SUBJECTS_CONCEPTS_MAP,
        SUBJECTS_REGISTRY
    )
except ImportError:
    NETWORKS_CONCEPTS = {}
    AI_CONCEPTS = {}
    FLA_CONCEPTS = {}
    BIOCHEM_CONCEPTS = {}
    SUBJECTS_CONCEPTS_MAP = {"Mathematics": CANONICAL_CONCEPTS}
    SUBJECTS_REGISTRY = {}


def get_subject_curriculum_graph(subject_name: str = "Mathematics") -> "CurriculumGraph":
    """Constructs a validated CurriculumGraph for any of the 5 subjects."""
    cmap = SUBJECTS_CONCEPTS_MAP.get(subject_name, CANONICAL_CONCEPTS)
    # Adapt to prereqs format expected by CurriculumGraph
    adapted = {}
    for cid, data in cmap.items():
        adapted[cid] = {
            "title": data.get("name") or data.get("title", cid),
            "prereqs": data.get("prerequisites") if "prerequisites" in data else data.get("prereqs", []),
            "description": data.get("description", "")
        }
    return CurriculumGraph(adapted)


class CurriculumGraph:
    """Directed Acyclic Graph (DAG) for Curriculum Concepts."""

    def __init__(self, concepts_dict: Optional[Dict[str, Dict[str, Any]]] = None):
        self._concepts = copy.deepcopy(concepts_dict or CANONICAL_CONCEPTS)
        self._validate_acyclic()

    def _validate_acyclic(self) -> None:
        """Ensures the curriculum graph contains no circular dependencies."""
        visited: Set[str] = set()
        rec_stack: Set[str] = set()

        def dfs(node: str) -> None:
            visited.add(node)
            rec_stack.add(node)
            for prereq in self._concepts.get(node, {}).get("prereqs", []):
                if prereq not in visited:
                    dfs(prereq)
                elif prereq in rec_stack:
                    raise ValueError(f"Cycle detected involving concept {prereq} and {node}")
            rec_stack.remove(node)

        for concept_id in self._concepts:
            if concept_id not in visited:
                dfs(concept_id)

    def __contains__(self, concept_id: str) -> bool:
        """Enables 'concept_id in graph' syntax."""
        return concept_id in self._concepts

    @property
    def graph(self) -> Dict[str, Dict[str, Any]]:
        """Compatibility property returning internal concept map for graph queries."""
        return self._concepts

    def get_prerequisites(self, concept_id: str) -> List[str]:
        """Returns immediate prerequisite concept IDs."""
        return list(self._concepts.get(concept_id, {}).get("prereqs", []))

    def get_all_ancestors(self, concept_id: str) -> List[str]:
        """Recursive traversal returning all upstream prerequisites in topological order."""
        ancestors: List[str] = []
        visited: Set[str] = set()

        def recurse(cid: str) -> None:
            for p in self.get_prerequisites(cid):
                if p not in visited:
                    visited.add(p)
                    recurse(p)
                    ancestors.append(p)

        recurse(concept_id)
        return ancestors

    def get_concept_title(self, concept_id: str) -> str:
        """Returns the human-readable concept title."""
        return self._concepts.get(concept_id, {}).get("title", f"Concept {concept_id}")

    def get_all_concepts(self) -> List[str]:
        """Returns all concept IDs in defined order."""
        return list(self._concepts.keys())

    def get_topological_order(self) -> List[str]:
        """Returns all concepts topologically sorted (prerequisites first)."""
        visited: Set[str] = set()
        order: List[str] = []

        def dfs(node: str) -> None:
            visited.add(node)
            for prereq in self.get_prerequisites(node):
                if prereq not in visited:
                    dfs(prereq)
            if node not in order:
                order.append(node)

        for cid in self._concepts:
            if cid not in visited:
                dfs(cid)
        return order

    def topological_order(self) -> List[str]:
        """Alias for get_topological_order() for cross-graph compatibility."""
        return self.get_topological_order()


@dataclass
class EngineConfig:
    """Deterministic thresholds governing MasteryFlow pedagogical decisions."""
    mastery_threshold: float = 0.85
    prereq_remediation_threshold: float = 0.55
    review_threshold: float = 0.60
    stagnation_delta: float = 0.05
    stagnation_cycles: int = 3
    inconsistency_cap_delta: float = 0.25
    config_version: int = 1

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> EngineConfig:
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class ConceptMastery:
    """Belief state for a single concept in student's cognitive model."""
    concept_id: str
    p_raw: float = 0.10
    p_eff: float = 0.10
    was_mastered: bool = False
    is_fragile: bool = False
    transfer_verified: bool = False
    history_p: List[float] = field(default_factory=list)
    attempts_count: int = 0
    errors_count: int = 0
    hints_count: int = 0
    last_attempt_timestamp: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ConceptMastery:
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class Decision:
    """Explainable pedagogical recommendation produced deterministically."""
    action: ActionType
    target_concept_id: str
    reason: str
    rule_triggered: str
    inputs_snapshot: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["action"] = self.action.value
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Decision:
        return cls(
            action=ActionType(data["action"]),
            target_concept_id=data["target_concept_id"],
            reason=data["reason"],
            rule_triggered=data["rule_triggered"],
            inputs_snapshot=data["inputs_snapshot"],
            metadata=data.get("metadata", {}),
        )
