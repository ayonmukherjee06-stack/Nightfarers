"""
Test 7: Cold Start Divergence via Diagnostic Propagation.
Owner: Yash & Soham Choudhury
Verifies distinct cognitive vector synthesis and divergent initial pedagogical recommendations.
"""

import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from backend.engine.graph import load_concept_graph
    from backend.engine.coldstart import DiagnosticEngine
    from backend.engine.decide import next_action, StudentState, ConceptState
except ImportError:
    from engine.graph import load_concept_graph
    from engine.coldstart import DiagnosticEngine
    from engine.decide import next_action, StudentState, ConceptState


def test_7_cold_start_divergence():
    """
    Test 7: Cold Start Divergence
    Student X and Student Y take the 6-question diagnostic with opposite accuracy patterns:
    - Student X performs well on fractions (C1, C2, C4) but fails ratio concepts (C6, C7, C10).
    - Student Y fails fractions (C1, C2, C4) but succeeds on applied problems.
    Distinct initial cognitive vectors generated via 0.3*w graph propagation; starting actions differ completely.
    """
    c_path = Path(__file__).parent.parent / "data" / "concepts.json"
    graph = load_concept_graph(str(c_path))
    engine = DiagnosticEngine(graph)

    # Initial uniform baseline
    baseline_x = {cid: 0.30 for cid in graph.topological_order()}
    baseline_y = {cid: 0.30 for cid in graph.topological_order()}

    # Student X answers C1, C2, C4 correctly; fails C6, C7, C10
    state_x = dict(baseline_x)
    for c in ["C1", "C2", "C4"]:
        state_x = engine.propagate_diagnostic_evidence(c, is_correct=True, w=1.0, mastery_state=state_x)
    for c in ["C6", "C7", "C10"]:
        state_x = engine.propagate_diagnostic_evidence(c, is_correct=False, w=1.0, mastery_state=state_x)

    # Student Y answers opposite: fails C1, C2, C4; succeeds on C6, C7, C10
    state_y = dict(baseline_y)
    for c in ["C1", "C2", "C4"]:
        state_y = engine.propagate_diagnostic_evidence(c, is_correct=False, w=1.0, mastery_state=state_y)
    for c in ["C6", "C7", "C10"]:
        state_y = engine.propagate_diagnostic_evidence(c, is_correct=True, w=1.0, mastery_state=state_y)

    # Cognitive vectors must be distinct
    assert state_x["C1"] > state_y["C1"], "Student X must have higher C1 mastery than Student Y"
    assert state_x["C7"] < state_y["C7"], "Student Y must have higher C7 mastery than Student X"

    # Evaluate next action for Student X
    stu_x_concepts = {
        cid: ConceptState(p=val, p_eff=val, status="practicing") for cid, val in state_x.items()
    }
    stu_x_state = StudentState(student_id="STU_X", active_concept_id="C6", concepts=stu_x_concepts)
    decision_x = next_action(stu_x_state, graph)

    # Evaluate next action for Student Y
    stu_y_concepts = {
        cid: ConceptState(p=val, p_eff=val, status="practicing") for cid, val in state_y.items()
    }
    stu_y_state = StudentState(student_id="STU_Y", active_concept_id="C1", concepts=stu_y_concepts)
    decision_y = next_action(stu_y_state, graph)

    assert (decision_x.action != decision_y.action) or (decision_x.target_concept != decision_y.target_concept), (
        "Diagnostic outcomes must yield divergent starting recommendations!"
    )
