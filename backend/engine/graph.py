"""
NetworkX DAG Prerequisite Knowledge Graph & Inconsistency Capping (graph.py).
Owner: Yash & Ayon Mukherjee
Enforces Directed Acyclic Graph invariants across C1-C10 and prerequisite ceiling capping.
"""

import os
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
import networkx as nx


class PrerequisiteGraph:
    """Directed Acyclic Graph (DAG) modeling curriculum dependencies and prerequisite ceilings."""

    def __init__(self, concepts_data: Optional[List[Dict]] = None):
        self.graph = nx.DiGraph()
        self.concepts_meta: Dict[str, Dict] = {}

        if concepts_data:
            self._build_graph(concepts_data)

    def _build_graph(self, concepts_data: List[Dict]):
        """Populates the DiGraph and performs acyclic validation."""
        for item in concepts_data:
            cid = item["id"]
            self.graph.add_node(cid, **item)
            self.concepts_meta[cid] = item

        for item in concepts_data:
            cid = item["id"]
            for prereq in item.get("prerequisites", []):
                # Edge from prerequisite -> child concept
                self.graph.add_edge(prereq, cid)

        # Invariant: NetworkX DAG validates acyclic graph at system boot
        if not nx.is_directed_acyclic_graph(self.graph):
            cycle = nx.find_cycle(self.graph, orientation="original")
            raise ValueError(f"CRITICAL: Prerequisite cycle detected in curriculum graph: {cycle}")

    def get_prerequisites(self, concept_id: str) -> List[str]:
        """Returns direct prerequisites of a concept."""
        if concept_id not in self.graph:
            return []
        return list(self.graph.predecessors(concept_id))

    def get_all_ancestors(self, concept_id: str) -> Set[str]:
        """Returns all transitive prerequisite ancestors."""
        if concept_id not in self.graph:
            return set()
        return nx.ancestors(self.graph, concept_id)

    def get_dependents(self, concept_id: str) -> List[str]:
        """Returns immediate downstream concepts dependent on concept_id."""
        if concept_id not in self.graph:
            return []
        return list(self.graph.successors(concept_id))

    def topological_order(self) -> List[str]:
        """Returns topological ordering of all concepts."""
        return list(nx.topological_sort(self.graph))

    def apply_prerequisite_capping(
        self,
        concept_id: str,
        p_eff: float,
        all_p_eff: Dict[str, float],
        capping_offset: float = 0.25
    ) -> Tuple[float, bool, Optional[str], Optional[float]]:
        """
        Enforces prerequisite ceiling invariant:
        min_prereq_p = min([p_eff[p] for p in direct_prerequisites(C)]) if direct_prerequisites(C) else 1.0
        p_eff_capped = min(p_eff[C], min_prereq_p + 0.25)
        if p_eff_capped < p_eff[C]:
            is_fragile = True
        
        Returns:
            (p_eff_capped, is_fragile, weakest_prereq_id, weakest_prereq_p)
        """
        prereqs = self.get_prerequisites(concept_id)
        if not prereqs:
            return p_eff, False, None, None

        weakest_id = None
        min_prereq_val = 1.0

        for pr in prereqs:
            pr_val = all_p_eff.get(pr, 0.25)
            if pr_val < min_prereq_val:
                min_prereq_val = pr_val
                weakest_id = pr

        ceiling = round(min_prereq_val + capping_offset, 4)
        if p_eff > ceiling:
            # Ceiling binds: mark as fragile and cap effective mastery
            return ceiling, True, weakest_id, min_prereq_val

        return p_eff, False, weakest_id, min_prereq_val


class ConceptDAG:
    """
    Curriculum Knowledge Graph for C1-C10 with NetworkX Directed Acyclic Graph validation.
    """
    def __init__(self, concepts_json_path: Optional[str] = None):
        self.graph = nx.DiGraph()
        self.concept_metadata: Dict[str, Dict] = {}

        if concepts_json_path and os.path.exists(concepts_json_path):
            self._load_from_json(concepts_json_path)
        else:
            self._load_default_curriculum()

        # System boot invariant: validate acyclic structure
        self.validate_acyclic()

    def _load_from_json(self, path: str) -> None:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for c in data.get('concepts', []):
            cid = c['id']
            self.concept_metadata[cid] = c
            self.graph.add_node(cid, **c)
            for prereq in c.get('prerequisites', []):
                self.graph.add_edge(prereq, cid)

    def _load_default_curriculum(self) -> None:
        """Official 10-node curriculum from Section 3.4."""
        default_concepts = [
            {"id": "C1", "name": "Fraction basics (part-whole, number line)", "prerequisites": [], "default_p": 0.25},
            {"id": "C2", "name": "Equivalent fractions and simplifying", "prerequisites": ["C1"], "default_p": 0.20},
            {"id": "C3", "name": "Comparing and ordering fractions", "prerequisites": ["C2"], "default_p": 0.20},
            {"id": "C4", "name": "Adding and subtracting fractions", "prerequisites": ["C2"], "default_p": 0.15},
            {"id": "C5", "name": "Multiplying and dividing fractions", "prerequisites": ["C2"], "default_p": 0.15},
            {"id": "C6", "name": "Ratio basics (part:part, part:whole)", "prerequisites": ["C1", "C2"], "default_p": 0.15},
            {"id": "C7", "name": "Equivalent ratios and unit rate", "prerequisites": ["C6", "C5"], "default_p": 0.10},
            {"id": "C8", "name": "Proportion (solve a/b = c/d)", "prerequisites": ["C7"], "default_p": 0.10},
            {"id": "C9", "name": "Percentages as ratios", "prerequisites": ["C3", "C6"], "default_p": 0.10},
            {"id": "C10", "name": "Proportion word problems & scaling", "prerequisites": ["C8", "C9"], "default_p": 0.05}
        ]
        for c in default_concepts:
            cid = c['id']
            self.concept_metadata[cid] = c
            self.graph.add_node(cid, **c)
            for prereq in c['prerequisites']:
                self.graph.add_edge(prereq, cid)

    def validate_acyclic(self) -> None:
        if not nx.is_directed_acyclic_graph(self.graph):
            cycles = list(nx.simple_cycles(self.graph))
            raise ValueError(f"Cyclic dependency detected in curriculum graph: {cycles}")

    def get_direct_prerequisites(self, concept_id: str) -> List[str]:
        if concept_id in self.graph:
            return list(self.graph.predecessors(concept_id))
        return []

    def get_prerequisites(self, concept_id: str) -> List[str]:
        return self.get_direct_prerequisites(concept_id)

    def get_all_ancestor_prerequisites(self, concept_id: str) -> Set[str]:
        if concept_id in self.graph:
            return nx.ancestors(self.graph, concept_id)
        return set()

    def get_all_ancestors(self, concept_id: str) -> Set[str]:
        return self.get_all_ancestor_prerequisites(concept_id)

    def get_direct_children(self, concept_id: str) -> List[str]:
        if concept_id in self.graph:
            return list(self.graph.successors(concept_id))
        return []

    def get_dependents(self, concept_id: str) -> List[str]:
        return self.get_direct_children(concept_id)

    def get_topological_order(self) -> List[str]:
        return list(nx.topological_sort(self.graph))

    def topological_order(self) -> List[str]:
        return self.get_topological_order()

    def evaluate_prerequisite_capping(
        self,
        concept_id: str,
        learner_state: Any,
        ceiling_margin: float = 0.25
    ) -> Tuple[float, bool]:
        concept = learner_state.get_or_create_concept(concept_id)
        decay = concept.get_effective_mastery(learner_state.virtual_clock)
        raw_p_eff = decay.p_eff

        prereqs = self.get_direct_prerequisites(concept_id)
        if not prereqs:
            concept.is_fragile = False
            return raw_p_eff, False

        prereq_p_effs = []
        for pid in prereqs:
            p_cm = learner_state.get_or_create_concept(pid)
            p_decay = p_cm.get_effective_mastery(learner_state.virtual_clock)
            prereq_p_effs.append(p_decay.p_eff)

        min_prereq_p = min(prereq_p_effs)
        p_eff_capped = min(raw_p_eff, round(min_prereq_p + ceiling_margin, 4))
        is_fragile = p_eff_capped < raw_p_eff
        concept.is_fragile = is_fragile
        return p_eff_capped, is_fragile

    def apply_all_cappings(self, learner_state: Any) -> Dict[str, Dict]:
        results = {}
        for cid in self.get_topological_order():
            p_capped, is_fragile = self.evaluate_prerequisite_capping(cid, learner_state)
            cm = learner_state.get_or_create_concept(cid)
            status = cm.determine_status(p_capped)
            results[cid] = {
                'raw_p': cm.p,
                'p_eff_capped': p_capped,
                'is_fragile': is_fragile,
                'status': status
            }
        return results

    def find_weakest_prerequisite(
        self,
        concept_id: str,
        learner_state: Any,
        prereq_threshold: float = 0.55
    ) -> Optional[Tuple[str, float]]:
        ancestors = self.get_all_ancestor_prerequisites(concept_id)
        if not ancestors:
            return None

        weakest_id = None
        min_p = 1.0
        for aid in ancestors:
            acm = learner_state.get_or_create_concept(aid)
            decay = acm.get_effective_mastery(learner_state.virtual_clock)
            if decay.p_eff < prereq_threshold and decay.p_eff < min_p:
                min_p = decay.p_eff
                weakest_id = aid

        if weakest_id is not None:
            return weakest_id, min_p
        return None

    def get_unlocked_concepts(
        self,
        learner_state: Any,
        prereq_threshold: float = 0.55
    ) -> List[str]:
        unlocked = []
        for cid in self.get_topological_order():
            prereqs = self.get_direct_prerequisites(cid)
            if not prereqs:
                unlocked.append(cid)
                continue
            all_prereqs_met = True
            for pid in prereqs:
                pcm = learner_state.get_or_create_concept(pid)
                p_eff = pcm.get_effective_mastery(learner_state.virtual_clock).p_eff
                if p_eff < prereq_threshold:
                    all_prereqs_met = False
                    break
            if all_prereqs_met:
                unlocked.append(cid)
        return unlocked


def load_concept_graph(concepts_json_path: Optional[str] = None) -> PrerequisiteGraph:
    """Loads concept graph from JSON file path."""
    if concepts_json_path is None:
        concepts_json_path = str(Path(__file__).parent.parent / "data" / "concepts.json")
    with open(concepts_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return PrerequisiteGraph(data.get("concepts", []))

