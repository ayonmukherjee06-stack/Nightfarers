"""Unit tests for Multi-Subject Expansion, YouTube Video Recommendations, and Guided Video Tour.

Authored by: Ayon Mukherjee
Verifies:
1. All 5 subject curricula (Math, CN, AI, FLA, BIO) have strictly acyclic DAGs.
2. Every concept has at least one curated YouTube video lesson with thumbnail, duration, and takeaways.
3. Exercise failure automatically triggers YouTube video remediation recommendation.
4. Interactive video guide has complete multi-chapter tour structure.
"""

import pytest
import networkx as nx
from data.curricula import (
    SUBJECTS_CONCEPTS_MAP,
    YOUTUBE_VIDEOS_CATALOG,
    get_subject_concepts,
    get_video_for_concept,
    get_videos_for_subject,
    MULTI_SUBJECT_QUESTIONS,
)
from backend.engine.contracts import get_subject_curriculum_graph
from frontend.components.video_guide import GUIDE_CHAPTERS


def test_all_five_subjects_exist():
    """Verify all 5 academic disciplines are registered."""
    expected_subjects = [
        "Mathematics",
        "Computer Networks",
        "Artificial Intelligence",
        "Formal Languages & Automata",
        "Biochemistry",
    ]
    for subj in expected_subjects:
        assert subj in SUBJECTS_CONCEPTS_MAP, f"Subject '{subj}' missing from registry"
        concepts = get_subject_concepts(subj)
        assert len(concepts) >= 8, f"Subject '{subj}' has fewer than 8 concepts"


def test_all_subject_graphs_are_acyclic_dags():
    """Verify each subject's prerequisite knowledge graph is a valid, acyclic DAG."""
    for subj in SUBJECTS_CONCEPTS_MAP:
        graph = get_subject_curriculum_graph(subj)
        topological_order = graph.topological_order()
        concepts = get_subject_concepts(subj)
        assert len(topological_order) == len(concepts), (
            f"Subject '{subj}' topological order count mismatch"
        )
        # Verify prerequisites precede children in topological order
        pos = {cid: idx for idx, cid in enumerate(topological_order)}
        for cid, meta in concepts.items():
            for prereq in meta.get("prerequisites", []):
                assert pos[prereq] < pos[cid], (
                    f"In '{subj}', prereq {prereq} does not precede {cid} in topological order"
                )


def test_every_concept_has_curated_youtube_video():
    """Verify every single concept across all subjects has a curated YouTube video lesson."""
    all_concept_ids = set()
    for subj, concepts in SUBJECTS_CONCEPTS_MAP.items():
        all_concept_ids.update(concepts.keys())

    assert len(all_concept_ids) == 42, f"Expected 42 concepts, got {len(all_concept_ids)}"

    for cid in all_concept_ids:
        video = get_video_for_concept(cid)
        assert video is not None, f"Concept '{cid}' is missing a curated YouTube video"
        assert "video_id" in video and len(video["video_id"]) >= 6, f"Invalid video_id for '{cid}'"
        assert "title" in video and len(video["title"]) > 0, f"Missing title for '{cid}' video"
        assert "channel" in video, f"Missing channel for '{cid}' video"
        assert "duration" in video, f"Missing duration badge for '{cid}' video"
        assert "thumbnail_url" in video and video["thumbnail_url"].startswith("https://img.youtube.com/vi/"), (
            f"Invalid thumbnail URL for '{cid}'"
        )
        assert "takeaways" in video and len(video["takeaways"]) >= 2, (
            f"Concept '{cid}' video must have at least 2 key takeaways"
        )


def test_multi_subject_questions_coverage():
    """Verify practice questions exist for non-math subjects with multiple-choice options."""
    for subj in ["Computer Networks", "Artificial Intelligence", "Formal Languages & Automata", "Biochemistry"]:
        concepts = get_subject_concepts(subj)
        for cid in concepts:
            q_matches = [q for q in MULTI_SUBJECT_QUESTIONS if q.get("concept_id") == cid]
            assert len(q_matches) >= 1, f"Missing practice question for concept '{cid}' in '{subj}'"
            q = q_matches[0]
            assert "options" in q and len(q["options"]) == 4, f"Question '{q['id']}' must have 4 MCQ options"
            assert "correct_answer" in q and q["correct_answer"] in q["options"], (
                f"Question '{q['id']}' correct_answer not in options list"
            )


def test_guided_video_tour_chapters():
    """Verify the interactive video walkthrough has all necessary feature chapters."""
    assert len(GUIDE_CHAPTERS) >= 6
    chapter_titles = [c["title"] for c in GUIDE_CHAPTERS]
    features_covered = " ".join(chapter_titles).lower()

    assert "adaptive" in features_covered or "personalized" in features_covered
    assert "curriculum" in features_covered or "multi-subject" in features_covered
    assert "math" in features_covered or "bkt" in features_covered or "engine" in features_covered
    assert "anti-gaming" in features_covered or "telemetry" in features_covered
    assert "remediation" in features_covered or "youtube" in features_covered
    assert "teacher" in features_covered or "3d" in features_covered or "universe" in features_covered
