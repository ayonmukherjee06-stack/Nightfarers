"""MasteryFlow Project Documentation & Platform Guide (video_guide.py).

NOTE: The resource-consuming simulated demo video player has been removed completely
in favor of the comprehensive, text-based Project Guide & Architecture Manual.
This module now points to frontend.components.project_guide while maintaining
full backward compatibility for existing imports and test suites.
"""

from frontend.components.project_guide import (
    CHAPTERS,
    GUIDE_CHAPTERS,
    render_project_guide,
    render_video_guide,
)

__all__ = [
    "CHAPTERS",
    "GUIDE_CHAPTERS",
    "render_project_guide",
    "render_video_guide",
]
