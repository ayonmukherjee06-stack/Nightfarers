"""MasteryFlow Apitex Edition Design System (theme.py).

Aesthetic: Inspired by the Apitex Mobile Banking & Fintech Design System:
- Warm luxury champagne / alabaster canvas (#FBF9F5) with subtle ambient warmth
- Crisp porcelain white surfaces (#FFFFFF) with generous rounded corners (22px-26px)
- Signature deep obsidian / carbon capsule buttons (#11141D) with high-contrast white text
- Luxury "Cognitive Platinum Passport" widget with metallic champagne-gold mesh
- High-end segmented pill tabs, rounded metric bars, and low-saturation pastel jewel badges
- Ultra-crisp typography (deep charcoal #11141D headings, warm taupe-gray #6B7280 metadata)
"""

from __future__ import annotations
import streamlit as st


GLOBAL_THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

:root {
    --bg-base: #FBF9F5;
    --bg-surface: #FFFFFF;
    --bg-surface-cream: #F5EFE6;
    --bg-card: #FFFFFF;
    --bg-card-hover: #FFFFFF;
    
    --primary: #11141D;
    --primary-hover: #1F2432;
    --primary-subtle: #F4EEE5;
    --primary-border: #E8E0D4;
    
    /* Apitex Signature Accents */
    --accent-gold: #D4AF37;
    --accent-champagne: #F5E8D4;
    --accent-obsidian: #11141D;
    --accent-emerald: #059669;
    --accent-amber: #D97706;
    --accent-rose: #E11D48;
    --accent-sky: #0284C7;
    
    --text-primary: #11141D;
    --text-secondary: #4B5563;
    --text-muted: #78716C;
    
    --border-subtle: rgba(228, 221, 211, 0.9);
    --border-strong: #DCD4C7;
    
    --radius-sm: 10px;
    --radius-md: 16px;
    --radius-lg: 22px;
    --radius-xl: 28px;
    --radius-full: 9999px;
    
    --shadow-sm: 0 2px 6px -1px rgba(60, 50, 30, 0.03);
    --shadow-md: 0 10px 30px -4px rgba(60, 50, 30, 0.05), 0 2px 8px -1px rgba(60, 50, 30, 0.02);
    --shadow-lg: 0 18px 40px -6px rgba(60, 50, 30, 0.08), 0 4px 12px -2px rgba(60, 50, 30, 0.03);
}

/* Apitex Warm Canvas */
.stApp {
    background-color: #FBF9F5 !important;
    background-image: 
        radial-gradient(circle at 12% 10%, rgba(246, 238, 227, 0.7) 0%, transparent 45%),
        radial-gradient(circle at 88% 18%, rgba(250, 243, 233, 0.8) 0%, transparent 50%),
        radial-gradient(circle at 50% 95%, rgba(243, 234, 221, 0.5) 0%, transparent 60%) !important;
    background-attachment: fixed !important;
    color: var(--text-primary) !important;
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    letter-spacing: -0.01em !important;
}

/* Layout container spacing */
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 2.5rem !important;
    max-width: 1360px !important;
}

/* Streamlit Header Cleanup */
#MainMenu, header[data-testid="stHeader"] {
    background: transparent !important;
}
header[data-testid="stHeader"] {
    height: 2.2rem !important;
}

/* Typography Hierarchy - Deep Obsidian Headings */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    letter-spacing: -0.025em !important;
    color: #11141D !important;
    font-weight: 800 !important;
}

p, span, div {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    color: inherit;
}

code, kbd, samp, pre {
    font-family: 'JetBrains Mono', monospace !important;
}

code {
    background: #F4EEE5 !important;
    color: #11141D !important;
    border: 1px solid #E5DCD0 !important;
    padding: 2px 7px !important;
    border-radius: 6px !important;
    font-size: 0.88em !important;
}

/* Sidebar - Apitex Warm Cream Minimalist Panel */
[data-testid="stSidebar"] {
    background: #F5EFE6 !important;
    border-right: 1px solid var(--border-subtle) !important;
    box-shadow: 2px 0 16px rgba(60, 50, 30, 0.03) !important;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: var(--text-secondary) !important;
}

/* Apitex Sidebar Navigation Cards */
[data-testid="stSidebar"] [data-testid="stRadio"] > div {
    gap: 8px !important;
    background: transparent !important;
    padding: 0 !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    background: #FFFFFF !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 14px !important;
    padding: 11px 16px !important;
    margin-bottom: 2px !important;
    transition: all 0.18s cubic-bezier(0.16, 1, 0.3, 1) !important;
    cursor: pointer !important;
    display: flex !important;
    align-items: center !important;
    box-shadow: 0 2px 8px -2px rgba(60, 50, 30, 0.04) !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    border-color: #11141D !important;
    transform: translateX(2px) !important;
    box-shadow: 0 4px 12px -2px rgba(60, 50, 30, 0.08) !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label[data-checked="true"],
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
    background: #11141D !important;
    border-color: #11141D !important;
    box-shadow: 0 6px 18px -3px rgba(17, 20, 29, 0.25) !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label[data-checked="true"] *,
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) *,
[data-testid="stSidebar"] [data-testid="stRadio"] label[data-checked="true"] p,
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) p,
[data-testid="stSidebar"] [data-testid="stRadio"] label[data-checked="true"] div[data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) div[data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] [data-testid="stRadio"] label[data-checked="true"] span,
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) span {
    color: #FFFFFF !important;
    font-weight: 700 !important;
    fill: #FFFFFF !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:active,
[data-testid="stSidebar"] [data-testid="stRadio"] label:active *,
[data-testid="stSidebar"] [data-testid="stRadio"] label:active div[data-testid="stMarkdownContainer"] p {
    background: #11141D !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:not([data-checked="true"]):not(:has(input:checked)) div[data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] [data-testid="stRadio"] label:not([data-checked="true"]):not(:has(input:checked)) p,
[data-testid="stSidebar"] [data-testid="stRadio"] label:not([data-checked="true"]):not(:has(input:checked)) span {
    font-weight: 600 !important;
    font-size: 0.90rem !important;
    color: #11141D !important;
}

/* Apitex Segmented Capsule Tabs (Income/Expenses style) */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px !important;
    background: #EDE6DA !important;
    padding: 5px !important;
    border-radius: 9999px !important;
    border: 1px solid rgba(220, 210, 195, 0.8) !important;
    margin-bottom: 22px !important;
    box-shadow: inset 0 2px 4px rgba(60, 50, 30, 0.04) !important;
}

.stTabs [data-baseweb="tab"] {
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    color: #78716C !important;
    border-radius: 9999px !important;
    padding: 8px 22px !important;
    border: none !important;
    background-color: transparent !important;
    transition: all 0.18s ease !important;
}

.stTabs [data-baseweb="tab"]:hover {
    color: #11141D !important;
}

.stTabs [aria-selected="true"] {
    color: #FFFFFF !important;
    background: #11141D !important;
    border: none !important;
    box-shadow: 0 4px 14px -2px rgba(17, 20, 29, 0.25) !important;
}

/* Apitex Porcelain Card Container */
.mf-glass-card {
    background: #FFFFFF !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 22px !important;
    padding: 22px 26px !important;
    margin-bottom: 20px !important;
    box-shadow: 0 10px 30px -4px rgba(60, 50, 30, 0.05), 0 2px 8px -1px rgba(60, 50, 30, 0.02) !important;
    transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1) !important;
    position: relative;
}

.mf-glass-card:hover {
    border-color: #D8CEBE !important;
    box-shadow: 0 14px 38px -4px rgba(60, 50, 30, 0.08), 0 3px 10px -1px rgba(60, 50, 30, 0.03) !important;
    transform: translateY(-1px) !important;
}

.mf-glass-card-accent {
    background: #FFFFFF !important;
    border: 1px solid var(--border-subtle) !important;
    border-left: 5px solid #11141D !important;
    border-radius: 22px !important;
    padding: 22px 26px !important;
    margin-bottom: 20px !important;
    box-shadow: 0 10px 30px -4px rgba(60, 50, 30, 0.05) !important;
}

/* Apitex Obsidian Capsule Buttons */
.stButton>button {
    background: #11141D !important;
    color: #FFFFFF !important;
    border: 1px solid #11141D !important;
    border-radius: 9999px !important;
    padding: 10px 24px !important;
    font-weight: 700 !important;
    font-size: 0.90rem !important;
    letter-spacing: -0.01em !important;
    box-shadow: 0 6px 18px -3px rgba(17, 20, 29, 0.25) !important;
    transition: all 0.18s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

.stButton>button * {
    color: inherit !important;
}

.stButton>button:hover {
    background: #252A37 !important;
    border-color: #252A37 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 24px -4px rgba(17, 20, 29, 0.35) !important;
    color: #FFFFFF !important;
}

.stButton>button:hover * {
    color: #FFFFFF !important;
}

.stButton>button:active,
.stButton>button:focus,
.stButton>button:focus:not(:focus-visible) {
    background: #11141D !important;
    border-color: #11141D !important;
    color: #FFFFFF !important;
    transform: translateY(0) !important;
    box-shadow: 0 4px 12px -2px rgba(17, 20, 29, 0.30) !important;
}

.stButton>button:active *,
.stButton>button:focus *,
.stButton>button:focus:not(:focus-visible) * {
    color: #FFFFFF !important;
}

/* Secondary Button */
button[kind="secondary"] {
    background: #F5EFE6 !important;
    color: #11141D !important;
    border: 1px solid #E5DCD0 !important;
    border-radius: 9999px !important;
    box-shadow: 0 2px 6px rgba(60, 50, 30, 0.03) !important;
}

button[kind="secondary"]:hover {
    background: #EDE5DA !important;
    border-color: #11141D !important;
    color: #11141D !important;
}

/* Inputs, Textareas, Selectboxes */
.stTextInput>div>div>input, 
.stTextArea>div>div>textarea, 
.stSelectbox>div>div>div {
    background-color: #FFFFFF !important;
    color: #11141D !important;
    border: 1px solid rgba(220, 210, 195, 0.95) !important;
    border-radius: 12px !important;
    font-size: 0.92rem !important;
    box-shadow: inset 0 2px 4px rgba(60, 50, 30, 0.02) !important;
    transition: border-color 0.18s ease, box-shadow 0.18s ease !important;
}

.stTextInput>div>div>input:focus, 
.stTextArea>div>div>textarea:focus, 
.stSelectbox>div>div>div:focus {
    border-color: #11141D !important;
    box-shadow: 0 0 0 3px rgba(17, 20, 29, 0.08) !important;
}

/* Metric Tiles - Clean Porcelain Cards */
[data-testid="stMetric"] {
    background: #FFFFFF !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 20px !important;
    padding: 16px 20px !important;
    box-shadow: 0 6px 20px -3px rgba(60, 50, 30, 0.04) !important;
    transition: all 0.18s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

[data-testid="stMetric"]:hover {
    border-color: #11141D !important;
    box-shadow: 0 10px 26px -4px rgba(60, 50, 30, 0.07) !important;
    transform: translateY(-1px) !important;
}

[data-testid="stMetricValue"] {
    font-weight: 800 !important;
    color: #11141D !important;
    font-size: 1.85rem !important;
    letter-spacing: -0.03em !important;
}

[data-testid="stMetricLabel"] {
    font-size: 0.74rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.6px !important;
    color: #78716C !important;
    font-weight: 700 !important;
}

/* Expanders */
.streamlit-expanderHeader {
    background-color: #FFFFFF !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 14px !important;
    color: #11141D !important;
    font-weight: 700 !important;
    box-shadow: 0 2px 8px -2px rgba(60, 50, 30, 0.03) !important;
}

.streamlit-expanderHeader:hover {
    border-color: #11141D !important;
}

/* Dataframe & Tables */
[data-testid="stDataFrame"] {
    background: #FFFFFF !important;
    border-radius: 16px !important;
    border: 1px solid var(--border-subtle) !important;
    overflow: hidden !important;
    box-shadow: 0 4px 14px -2px rgba(60, 50, 30, 0.03) !important;
}

/* Alerts / Callouts */
.stAlert {
    background-color: #FFFFFF !important;
    border-radius: 16px !important;
    border: 1px solid var(--border-subtle) !important;
    color: #11141D !important;
    box-shadow: 0 6px 18px -3px rgba(60, 50, 30, 0.04) !important;
}

/* Apitex Custom Scrollbar */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: #FBF9F5;
}
::-webkit-scrollbar-thumb {
    background: #D8CEBE;
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: #B8AC9A;
}
</style>
"""


def apply_theme():
    """Injects the Apitex Edition global theme CSS into Streamlit."""
    st.markdown(GLOBAL_THEME_CSS, unsafe_allow_html=True)


apply_custom_theme = apply_theme


def clean_html(html_str: str) -> str:
    """Strips leading whitespace and empty lines to prevent CommonMark from treating HTML as code blocks."""
    if not html_str:
        return ""
    return "\n".join(line.strip() for line in html_str.splitlines() if line.strip())


def render_html(html_str: str) -> None:
    """Safely renders HTML via st.markdown with zero risk of CommonMark code block conversion."""
    st.markdown(clean_html(html_str), unsafe_allow_html=True)


def render_circular_gauge(percentage: int, label: str, color: str = "#11141D", size: int = 90) -> str:
    """Generates an Apitex-style SVG circular gauge with warm champagne track and deep obsidian arc."""
    stroke_width = 7
    radius = (size - stroke_width * 2) // 2
    circumference = int(2 * 3.14159 * radius)
    clamped_pct = max(0, min(100, percentage))
    stroke_dashoffset = int(circumference - (clamped_pct / 100.0) * circumference)
    cx = size // 2
    cy = size // 2

    raw_html = f"""
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; position: relative;">
        <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" style="transform: rotate(-90deg);">
            <!-- Background Track -->
            <circle cx="{cx}" cy="{cy}" r="{radius}" fill="transparent" stroke="#EFE6DA" stroke-width="{stroke_width}" />
            <!-- Active Meter Arc -->
            <circle cx="{cx}" cy="{cy}" r="{radius}" fill="transparent" stroke="{color}" stroke-width="{stroke_width}"
                stroke-dasharray="{circumference}" stroke-dashoffset="{stroke_dashoffset}" stroke-linecap="round"
                style="transition: stroke-dashoffset 0.6s cubic-bezier(0.16, 1, 0.3, 1);" />
        </svg>
        <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; pointer-events: none;">
            <div style="font-size: 1.20rem; font-weight: 800; color: #11141D; line-height: 1; letter-spacing: -0.5px;">
                {clamped_pct}%
            </div>
            <div style="font-size: 0.62rem; color: #78716C; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px; margin-top: 3px;">
                {label}
            </div>
        </div>
    </div>
    """
    return clean_html(raw_html)


def render_brand_header(title: str, subtitle: str, badge: str = "Adaptive Learning System"):
    """Renders the Apitex-style minimalist luxury brand header."""
    header_html = f"""
    <div style="
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 12px;
        padding: 6px 0 18px 0;
        margin-bottom: 20px;
        border-bottom: 1px solid rgba(228, 221, 211, 0.9);
    ">
        <div style="display: flex; align-items: center; gap: 14px;">
            <div style="
                width: 44px;
                height: 44px;
                border-radius: 14px;
                background: #11141D;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #FFFFFF;
                font-weight: 900;
                font-size: 1.2rem;
                box-shadow: 0 6px 16px -2px rgba(17, 20, 29, 0.25);
            ">▲</div>
            <div>
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 2px;">
                    <span style="
                        font-size: 1.7rem;
                        color: #11141D;
                        font-weight: 800;
                        letter-spacing: -0.03em;
                    ">
                        Mastery<span style="color: #78716C; font-weight: 600;">Flow</span>
                    </span>
                    <span style="
                        background: #F4EEE5;
                        color: #11141D;
                        border: 1px solid #E5DCD0;
                        font-size: 0.70rem;
                        font-weight: 700;
                        padding: 3px 12px;
                        border-radius: 9999px;
                        letter-spacing: 0.4px;
                    ">
                        {badge}
                    </span>
                </div>
                <div style="font-size: 0.86rem; color: #78716C; font-weight: 500;">
                    {subtitle}
                </div>
            </div>
        </div>
        <div style="text-align: right;">
            <span style="font-size: 0.72rem; color: #78716C; letter-spacing: 0.5px; font-weight: 600; text-transform: uppercase;">
                YUVA Megathon 2026 &middot; Intelligent Educational Systems
            </span>
            <div style="font-size: 0.82rem; color: #11141D; font-weight: 700; margin-top: 2px;">
                Apitex Edition &middot; Adaptive Math Platform
            </div>
        </div>
    </div>
    """
    render_html(header_html)


def render_judge_demo_ribbon():
    """Renders the Apitex-style evaluation and presentation ribbon."""
    render_html("""
    <div style="
        background: #FFFFFF;
        border: 1px solid rgba(228, 221, 211, 0.9);
        border-top: 4px solid #11141D;
        border-radius: 20px;
        padding: 14px 20px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 12px;
        box-shadow: 0 8px 24px -3px rgba(60, 50, 30, 0.04);
    ">
        <div style="display: flex; align-items: center; gap: 10px;">
            <div>
                <span style="font-size: 0.88rem; font-weight: 800; color: #11141D;">
                    Official Jury Evaluation &amp; Presentation Mode
                </span>
                <span style="font-size: 0.78rem; color: #78716C; margin-left: 8px;">
                    Deterministic 6-rule decision loop &middot; Bayesian Knowledge Tracing &middot; Zero LLM Invariants
                </span>
            </div>
        </div>

        <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
            <span style="font-size: 0.72rem; color: #059669; background: #E8F7F0; border: 1px solid #A7F3D0; padding: 4px 12px; border-radius: 9999px; font-weight: 700;">
                100% Deterministic Engine
            </span>
            <span style="font-size: 0.72rem; color: #0284C7; background: #E0F2FE; border: 1px solid #BAE6FD; padding: 4px 12px; border-radius: 9999px; font-weight: 700;">
                10-Node Curriculum DAG
            </span>
            <span style="font-size: 0.72rem; color: #7C3AED; background: #EDE9FE; border: 1px solid #DDD6FE; padding: 4px 12px; border-radius: 9999px; font-weight: 700;">
                Ebbinghaus Spaced Review
            </span>
        </div>
    </div>
    """)


def render_apitex_passport_card(
    student_id: str,
    student_name: str,
    p_eff: float,
    certified_count: int,
    total_count: int = 10,
    status: str = "Active Learner"
) -> None:
    """Renders the signature Apitex Luxury Platinum Card widget for student status."""
    pct = int(p_eff * 100)
    card_html = f"""
    <div style="
        background: linear-gradient(135deg, #FDF7EE 0%, #F5E8D4 45%, #EED9BD 100%);
        border: 1px solid rgba(214, 185, 140, 0.45);
        border-radius: 24px;
        padding: 24px 28px;
        margin-bottom: 20px;
        box-shadow: 0 14px 34px -4px rgba(180, 140, 90, 0.16), 0 3px 10px -1px rgba(60, 50, 30, 0.04);
        position: relative;
        overflow: hidden;
    ">
        <!-- Subtle radial mesh decoration -->
        <div style="
            position: absolute;
            top: -40px;
            right: -40px;
            width: 160px;
            height: 160px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(255, 255, 255, 0.5) 0%, transparent 70%);
            pointer-events: none;
        "></div>

        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px;">
            <div>
                <div style="font-size: 0.72rem; font-weight: 800; color: #8A7255; text-transform: uppercase; letter-spacing: 1.2px;">
                    COGNITIVE PASSPORT &middot; PLATINUM
                </div>
                <div style="font-size: 1.15rem; font-weight: 800; color: #11141D; margin-top: 2px;">
                    {student_name}
                </div>
                <div style="font-size: 0.76rem; color: #8A7255; font-family: monospace;">
                    {student_id} &bull;&bull;&bull;&bull; 2026
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
                <div style="
                    width: 34px;
                    height: 26px;
                    border-radius: 6px;
                    background: linear-gradient(135deg, #D4AF37 0%, #AA820A 100%);
                    border: 1px solid rgba(255, 255, 255, 0.4);
                    box-shadow: inset 0 1px 2px rgba(255, 255, 255, 0.3);
                "></div>
            </div>
        </div>

        <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-top: 14px;">
            <div>
                <div style="font-size: 0.70rem; color: #8A7255; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px;">
                    EFFECTIVE COGNITIVE READINESS
                </div>
                <div style="font-size: 2.1rem; font-weight: 900; color: #11141D; line-height: 1.1; letter-spacing: -0.03em;">
                    {pct}% <span style="font-size: 0.95rem; font-weight: 700; color: #8A7255;">p_eff</span>
                </div>
            </div>

            <div style="text-align: right;">
                <span style="
                    background: #11141D;
                    color: #FFFFFF;
                    font-size: 0.72rem;
                    font-weight: 700;
                    padding: 5px 14px;
                    border-radius: 9999px;
                    letter-spacing: 0.4px;
                    display: inline-block;
                    box-shadow: 0 4px 12px rgba(17, 20, 29, 0.2);
                ">
                    {certified_count}/{total_count} CERTIFIED
                </span>
                <div style="font-size: 0.72rem; color: #8A7255; margin-top: 4px; font-weight: 600;">
                    Status: {status}
                </div>
            </div>
        </div>
    </div>
    """
    render_html(card_html)


def render_apitex_quick_actions(
    act1_label: str = "Practice Next Action",
    act2_label: str = "Spaced Review",
    act3_label: str = "Student Agency",
) -> None:
    """Renders the signature Apitex 3-capsule quick actions row."""
    html_row = f"""
    <div style="
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
        margin-bottom: 20px;
    ">
        <div style="
            background: #11141D;
            color: #FFFFFF;
            border-radius: 16px;
            padding: 14px 16px;
            text-align: center;
            font-size: 0.85rem;
            font-weight: 700;
            box-shadow: 0 6px 18px -3px rgba(17, 20, 29, 0.25);
            cursor: pointer;
        ">
            {act1_label}
        </div>
        <div style="
            background: #11141D;
            color: #FFFFFF;
            border-radius: 16px;
            padding: 14px 16px;
            text-align: center;
            font-size: 0.85rem;
            font-weight: 700;
            box-shadow: 0 6px 18px -3px rgba(17, 20, 29, 0.25);
            cursor: pointer;
        ">
            {act2_label}
        </div>
        <div style="
            background: #11141D;
            color: #FFFFFF;
            border-radius: 16px;
            padding: 14px 16px;
            text-align: center;
            font-size: 0.85rem;
            font-weight: 700;
            box-shadow: 0 6px 18px -3px rgba(17, 20, 29, 0.25);
            cursor: pointer;
        ">
            {act3_label}
        </div>
    </div>
    """
    render_html(html_row)
