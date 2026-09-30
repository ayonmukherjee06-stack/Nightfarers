"""MasteryFlow YouTube Video Recommendation Engine & Video Player UI (video_recommender.py).

Provides YouTube video recommendations when learners struggle with a question or concept,
renders realistic video thumbnail cards with duration badges and play overlays, and embeds
interactive video playback directly inside the Streamlit portal.
"""

from typing import Any, Dict, List, Optional
import streamlit as st

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
_DATA_DIR = _ROOT / "data"
if str(_DATA_DIR) not in sys.path:
    sys.path.insert(0, str(_DATA_DIR))

try:
    from data.curricula import (
        YOUTUBE_VIDEOS_CATALOG,
        get_video_for_concept,
        get_videos_for_subject,
        SUBJECTS_REGISTRY,
        get_subject_concepts,
    )
except ImportError:
    try:
        from masteryflow.data.curricula import (
            YOUTUBE_VIDEOS_CATALOG,
            get_video_for_concept,
            get_videos_for_subject,
            SUBJECTS_REGISTRY,
            get_subject_concepts,
        )
    except ImportError:
        from curricula import (
            YOUTUBE_VIDEOS_CATALOG,
            get_video_for_concept,
            get_videos_for_subject,
            SUBJECTS_REGISTRY,
            get_subject_concepts,
        )

try:
    from data.curricula import get_topic_brief_explanation
except (ImportError, AttributeError):
    try:
        from masteryflow.data.curricula import get_topic_brief_explanation
    except (ImportError, AttributeError):
        try:
            from curricula import get_topic_brief_explanation
        except (ImportError, AttributeError):
            def get_topic_brief_explanation(concept_id: str):
                return None

try:
    from frontend.components.theme import render_html, clean_html
except ImportError:
    try:
        from masteryflow.ui.components.theme import render_html, clean_html
    except ImportError:
        from theme import render_html, clean_html


def render_youtube_thumbnail_card(
    video: Dict[str, Any],
    is_recommended: bool = True,
    reason: str = "",
    allow_embed: bool = True,
    unique_key: str = "yt_card"
):
    """
    Renders an authentic, sleek YouTube video card featuring thumbnail, duration pill,
    channel badge, and direct embedded player toggle.
    """
    vid_id = video.get("video_id", "3xUQkQO8vQY")
    title = video.get("title", "Concept Video Lesson")
    channel = video.get("channel", "Educational Channel")
    duration = video.get("duration", "10:00")
    thumb_url = video.get("thumbnail_url") or f"https://img.youtube.com/vi/{vid_id}/hqdefault.jpg"
    watch_url = video.get("url") or f"https://www.youtube.com/watch?v={vid_id}"
    cid = video.get("concept_id", "")
    description = video.get("description", "")
    takeaways = video.get("takeaways", [])

    badge_html = """
    <div style="
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #FEF2F2;
        color: #DC2626;
        border: 1px solid #FECACA;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.74rem;
        font-weight: 800;
        letter-spacing: 0.02em;
        text-transform: uppercase;
        margin-bottom: 8px;
    ">
        <span>▶</span> Recommended Video Lesson
    </div>
    """ if is_recommended else ""

    reason_html = f"""
    <div style="
        font-size: 0.82rem;
        color: #7F1D1D;
        background: #FFF1F2;
        border-left: 3px solid #E11D48;
        padding: 8px 12px;
        border-radius: 8px;
        margin-bottom: 12px;
        line-height: 1.45;
    ">
        <strong>Why this video?</strong> {reason}
    </div>
    """ if reason else ""

    render_html(f"""
    <div style="
        background: #FFFFFF;
        border: 1px solid rgba(228, 221, 211, 0.95);
        border-radius: 20px;
        padding: 20px;
        margin-top: 14px;
        margin-bottom: 16px;
        box-shadow: 0 8px 24px -4px rgba(60, 50, 30, 0.06);
    ">
        {badge_html}
        {reason_html}

        <div style="display: flex; gap: 18px; flex-wrap: wrap; align-items: flex-start;">
            <!-- Thumbnail preview with duration badge and play overlay -->
            <div style="
                position: relative;
                width: 280px;
                min-width: 240px;
                aspect-ratio: 16 / 9;
                border-radius: 14px;
                overflow: hidden;
                box-shadow: 0 4px 14px rgba(0, 0, 0, 0.12);
                background: #11141D;
            ">
                <img src="{thumb_url}" alt="{title}" style="
                    width: 100%;
                    height: 100%;
                    object-fit: cover;
                    display: block;
                "/>
                <!-- Play button overlay -->
                <div style="
                    position: absolute;
                    inset: 0;
                    background: rgba(0, 0, 0, 0.28);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                ">
                    <div style="
                        width: 46px;
                        height: 46px;
                        border-radius: 50%;
                        background: #DC2626;
                        color: #FFFFFF;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 1.25rem;
                        box-shadow: 0 4px 12px rgba(220, 38, 38, 0.5);
                    ">▶</div>
                </div>
                <!-- Duration pill in bottom right -->
                <div style="
                    position: absolute;
                    bottom: 8px;
                    right: 8px;
                    background: rgba(17, 20, 29, 0.88);
                    color: #FFFFFF;
                    font-family: 'JetBrains Mono', monospace;
                    font-size: 0.72rem;
                    font-weight: 700;
                    padding: 2px 7px;
                    border-radius: 6px;
                ">
                    {duration}
                </div>
            </div>

            <!-- Video Metadata & Description -->
            <div style="flex: 1; min-width: 260px;">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                    <span style="
                        font-size: 0.70rem;
                        font-weight: 800;
                        background: #F4EEE5;
                        color: #11141D;
                        border: 1px solid #E5DCD0;
                        padding: 2px 8px;
                        border-radius: 6px;
                    ">{cid}</span>
                    <span style="font-size: 0.78rem; font-weight: 700; color: #4B5563;">
                        {channel}
                    </span>
                </div>
                <h4 style="
                    color: #11141D;
                    margin: 0 0 8px 0;
                    font-size: 1.08rem;
                    font-weight: 800;
                    line-height: 1.35;
                ">
                    {title}
                </h4>
                <p style="font-size: 0.82rem; color: #64748B; line-height: 1.5; margin: 0 0 10px 0;">
                    {description}
                </p>
                <div style="font-size: 0.75rem; color: #4B5563;">
                    <strong>Key Concepts Covered:</strong>
                    <ul style="margin: 4px 0 0 16px; padding: 0;">
                        {"".join(f'<li style="margin-bottom: 2px;">{t}</li>' for t in takeaways[:3])}
                    </ul>
                </div>
            </div>
        </div>
    </div>
    """)

    if allow_embed:
        embed_state_key = f"embed_open_{unique_key}_{vid_id}"
        if embed_state_key not in st.session_state:
            st.session_state[embed_state_key] = False

        c_play, c_yt = st.columns([2, 1])
        with c_play:
            btn_label = "Hide Video Player" if st.session_state[embed_state_key] else "Watch Lesson Here (Embedded)"
            if st.button(btn_label, key=f"btn_toggle_{unique_key}_{vid_id}", use_container_width=True):
                st.session_state[embed_state_key] = not st.session_state[embed_state_key]
                st.rerun()

        with c_yt:
            st.markdown(
                f'<a href="{watch_url}" target="_blank" style="'
                'display: flex; align-items: center; justify-content: center; gap: 6px; '
                'background: #F4EEE5; color: #11141D; text-decoration: none; '
                'border: 1px solid #E5DCD0; padding: 7px 14px; border-radius: 10px; '
                'font-size: 0.80rem; font-weight: 700; height: 38px;'
                '">Open in YouTube &rarr;</a>',
                unsafe_allow_html=True
            )

        if st.session_state[embed_state_key]:
            st.markdown("---")
            st.video(watch_url)


def render_topic_brief_card(concept_id: str):
    """
    Renders a comprehensive, pedagogical Topic Brief Explanation card.
    Used as an immediate reading guide and as an automatic fallback
    when a video lesson is not loaded or for learners who prefer text.
    """
    info = get_topic_brief_explanation(concept_id)
    if not info:
        return

    cid = info.get("concept_id", concept_id)
    title = info.get("title", f"Topic {cid}")
    summary = info.get("summary", "")
    core_principles = info.get("core_principles", [])
    key_formula = info.get("key_formula", "")
    example = info.get("example", "")
    common_pitfall = info.get("common_pitfall", "")

    principles_html = "".join(f"<li style='margin-bottom: 6px; line-height: 1.45;'>{p}</li>" for p in core_principles)

    render_html(f"""
    <div style="
        background: #FFFFFF;
        border: 1px solid rgba(228, 221, 211, 0.95);
        border-radius: 18px;
        padding: 20px;
        margin-top: 10px;
        margin-bottom: 16px;
        box-shadow: 0 4px 16px -2px rgba(60, 50, 30, 0.05);
    ">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; flex-wrap: wrap; gap: 8px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="
                    font-size: 0.72rem;
                    font-weight: 800;
                    background: #11141D;
                    color: #FFFFFF;
                    padding: 3px 8px;
                    border-radius: 6px;
                ">{cid}</span>
                <h4 style="margin: 0; color: #11141D; font-size: 1.05rem; font-weight: 800;">
                    {title}
                </h4>
            </div>
            <span style="
                font-size: 0.68rem;
                background: #F4EEE5;
                color: #78716C;
                border: 1px solid #E5DCD0;
                padding: 2px 8px;
                border-radius: 9999px;
                font-weight: 700;
            ">
                Topic Brief Study Guide
            </span>
        </div>

        <div style="
            font-size: 0.85rem;
            color: #334155;
            line-height: 1.55;
            background: #F8FAFC;
            border-left: 3px solid #0284C7;
            padding: 10px 14px;
            border-radius: 8px;
            margin-bottom: 14px;
        ">
            <strong>Core Concept:</strong> {summary}
        </div>

        <div style="margin-bottom: 14px;">
            <div style="font-size: 0.76rem; font-weight: 800; color: #64748B; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px;">
                Essential Mechanics &amp; Theoretical Principles
            </div>
            <ul style="font-size: 0.82rem; color: #1E293B; margin: 0; padding-left: 18px;">
                {principles_html}
            </ul>
        </div>

        <div style="
            background: #FAF5FF;
            border: 1px solid #E9D5FF;
            border-radius: 10px;
            padding: 10px 14px;
            margin-bottom: 12px;
            font-size: 0.82rem;
            color: #6B21A8;
        ">
            <strong>Key Formula / Algorithmic Rule:</strong><br>
            <code style="font-family: 'JetBrains Mono', monospace; font-size: 0.80rem; color: #581C87;">{key_formula}</code>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 10px; margin-top: 10px;">
            <div style="
                background: #F0FDF4;
                border: 1px solid #BBF7D0;
                border-radius: 10px;
                padding: 10px 14px;
                font-size: 0.80rem;
                color: #166534;
            ">
                <strong>Concrete Example:</strong><br>
                {example}
            </div>

            <div style="
                background: #FFF1F2;
                border: 1px solid #FECDD3;
                border-radius: 10px;
                padding: 10px 14px;
                font-size: 0.80rem;
                color: #9F1239;
            ">
                <strong>Common Student Pitfall:</strong><br>
                {common_pitfall}
            </div>
        </div>
    </div>
    """)


def render_failure_remediation_card(concept_id: str, concept_name: str = ""):
    """
    Renders an automatic video remediation card when a student misses an exercise.
    If video is unavailable, seamlessly falls back to the rich Topic Brief Explanation.
    """
    video = get_video_for_concept(concept_id)
    if not video:
        render_topic_brief_card(concept_id)
        return

    c_name = concept_name or video.get("title", concept_id)
    reason_text = (
        f"You missed a question on {concept_id}: {c_name}. "
        "Reviewing this focused visual lesson before your next attempt will reinforce the core intuition."
    )

    render_youtube_thumbnail_card(
        video=video,
        is_recommended=True,
        reason=reason_text,
        allow_embed=True,
        unique_key=f"fail_remed_{concept_id}"
    )
    with st.expander(f"Read {concept_id} Topic Brief Explanation & Study Notes", expanded=False):
        render_topic_brief_card(concept_id)


def render_concept_video_recommendation(concept_id: str, concept_name: str = "", reason: str = ""):
    """Renders a concept video recommendation with attached brief explanation."""
    video = get_video_for_concept(concept_id)
    if not video:
        render_topic_brief_card(concept_id)
        return
    c_name = concept_name or video.get("title", concept_id)
    render_youtube_thumbnail_card(
        video=video,
        is_recommended=True,
        reason=reason or f"Visual explanation & core intuitions for {c_name}",
        allow_embed=True,
        unique_key=f"concept_rec_{concept_id}"
    )
    with st.expander(f"Read {concept_id} Topic Brief Explanation & Study Notes", expanded=False):
        render_topic_brief_card(concept_id)


def render_subject_video_library(subject_name: str = "Mathematics", active_concept_id: Optional[str] = None):
    """
    Renders a comprehensive, filterable Video Lesson Library for all concepts in a subject.
    """
    concepts = get_subject_concepts(subject_name)
    videos = get_videos_for_subject(subject_name)

    render_html(f"""
    <div style="
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 12px;
        margin-bottom: 16px;
        border-bottom: 1px solid rgba(228, 221, 211, 0.9);
        flex-wrap: wrap;
        gap: 8px;
    ">
        <div>
            <h2 style="color: #11141D; margin: 0; font-size: 1.35rem; font-weight: 800; letter-spacing: -0.02em;">
                {subject_name} Video Lessons Hub
            </h2>
            <div style="font-size: 0.80rem; color: #78716C; margin-top: 2px;">
                Curated visual lessons covering every concept in the {subject_name} knowledge graph.
            </div>
        </div>
        <div>
            <span style="
                background: #E8F7F0;
                color: #047857;
                border: 1px solid #A7F3D0;
                font-size: 0.72rem;
                font-weight: 700;
                padding: 4px 12px;
                border-radius: 9999px;
            ">
                {len(videos)} Curated Lessons
            </span>
        </div>
    </div>
    """)

    # Filter chips
    filter_opts = ["All Concepts"] + [f"{cid}: {data.get('short_name') or data.get('name')}" for cid, data in concepts.items()]
    selected_filter = st.selectbox("Filter by Concept Topic:", filter_opts, index=0, label_visibility="collapsed")

    filtered_videos = videos
    if selected_filter != "All Concepts":
        sel_cid = selected_filter.split(":")[0].strip()
        filtered_videos = [v for v in videos if v.get("concept_id") == sel_cid]

    if not filtered_videos:
        st.info("No video lessons match your current selection.")
        return

    # Render video cards in grid
    for idx, vid in enumerate(filtered_videos):
        cid = vid.get("concept_id")
        is_highlight = (cid == active_concept_id)
        render_youtube_thumbnail_card(
            video=vid,
            is_recommended=is_highlight,
            reason="Currently active learning concept" if is_highlight else "",
            allow_embed=True,
            unique_key=f"lib_{cid}_{idx}"
        )
