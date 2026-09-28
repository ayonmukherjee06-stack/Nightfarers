"""MasteryFlow World-Class 2026 UI Theme & Design System (theme.py).

Authored by: Ayon Mukherjee (Team Lead & Orchestrator) & Soham Choudhury (Frontend Co-Lead)
Aesthetic: Raycast / Linear / Vercel Pro Glassmorphic Luxury Dark Mode.
Includes: Animated mesh glows, pulsing live telemetry dots, bento grid containers,
interactive quick-input chips, glowing circular gauges, and cybernetic typography.
"""

from __future__ import annotations
import streamlit as st


GLOBAL_THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

:root {
    --bg-primary: #04060C;
    --bg-surface: #090E20;
    --bg-card: rgba(12, 17, 34, 0.75);
    --bg-card-hover: rgba(18, 26, 52, 0.88);
    
    --accent-cyan: #00F0FF;
    --accent-cyan-glow: rgba(0, 240, 255, 0.4);
    --accent-blue: #38BDF8;
    --accent-indigo: #6366F1;
    --accent-purple: #8B5CF6;
    --accent-green: #10B981;
    --accent-amber: #F59E0B;
    --accent-rose: #F43F5E;
    
    --text-primary: #F8FAFC;
    --text-secondary: #94A3B8;
    --text-muted: #64748B;
    
    --border-subtle: rgba(255, 255, 255, 0.08);
    --border-accent: rgba(0, 240, 255, 0.35);
    --border-glow: rgba(0, 240, 255, 0.2);
}

/* Animations */
@keyframes pulseGlow {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.6; transform: scale(0.95); }
}

@keyframes borderGlowPulse {
    0%, 100% { border-color: rgba(0, 240, 255, 0.3); box-shadow: 0 0 15px rgba(0, 240, 255, 0.15); }
    50% { border-color: rgba(139, 92, 246, 0.4); box-shadow: 0 0 25px rgba(139, 92, 246, 0.25); }
}

@keyframes shimmerSweep {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}

/* Global Background Canvas with Layered Cosmic Spotlight */
.stApp {
    background-color: var(--bg-primary) !important;
    background-image: 
        radial-gradient(ellipse 90% 55% at 50% -12%, rgba(14, 165, 233, 0.16) 0%, transparent 60%),
        radial-gradient(circle at 8% 70%, rgba(139, 92, 246, 0.10) 0%, transparent 50%),
        radial-gradient(circle at 92% 80%, rgba(16, 185, 129, 0.08) 0%, transparent 50%),
        radial-gradient(circle at 50% 50%, rgba(3, 7, 18, 0.8) 0%, transparent 100%) !important;
    color: var(--text-primary) !important;
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    letter-spacing: -0.01em !important;
}

/* Hide Default Streamlit Clutter */
#MainMenu, header[data-testid="stHeader"], footer {
    visibility: visible;
}
header[data-testid="stHeader"] {
    background: transparent !important;
}

/* Typography Overrides */
h1, h2, h3, h4, .brand-font {
    font-family: 'Space Grotesk', 'Plus Jakarta Sans', sans-serif !important;
    letter-spacing: -0.025em !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
}

p, span, div {
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
}

code, kbd, samp, pre {
    font-family: 'JetBrains Mono', monospace !important;
}

/* Sidebar Ultra-Sleek Dark Theme */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #060914 0%, #03050A 100%) !important;
    border-right: 1px solid var(--border-subtle) !important;
    box-shadow: 4px 0 35px rgba(0, 0, 0, 0.5) !important;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: var(--text-secondary) !important;
}

/* Modern Segmented Navigation for Sidebar Radio */
[data-testid="stSidebar"] [data-testid="stRadio"] > div {
    gap: 8px !important;
    background: transparent !important;
    padding: 0 !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    background: rgba(12, 17, 34, 0.65) !important;
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
    border-radius: 12px !important;
    padding: 11px 14px !important;
    margin-bottom: 4px !important;
    transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1) !important;
    cursor: pointer !important;
    display: flex !important;
    align-items: center !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: rgba(20, 29, 56, 0.8) !important;
    border-color: rgba(0, 240, 255, 0.35) !important;
    transform: translateX(3px) !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label[data-checked="true"],
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
    background: linear-gradient(135deg, rgba(0, 240, 255, 0.16) 0%, rgba(56, 189, 248, 0.08) 100%) !important;
    border: 1px solid rgba(0, 240, 255, 0.5) !important;
    box-shadow: 0 0 18px rgba(0, 240, 255, 0.22), inset 0 1px 0 rgba(255, 255, 255, 0.12) !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label div[data-testid="stMarkdownContainer"] p {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    color: #FFFFFF !important;
    letter-spacing: -0.01em !important;
}

/* Tabs Styling - Modern Segmented Floating Bar */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px !important;
    background: rgba(9, 13, 26, 0.8) !important;
    padding: 6px !important;
    border-radius: 14px !important;
    border: 1px solid var(--border-subtle) !important;
    margin-bottom: 22px !important;
    box-shadow: 0 8px 24px -4px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.06) !important;
}

.stTabs [data-baseweb="tab"] {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.90rem !important;
    color: #94A3B8 !important;
    border-radius: 10px !important;
    padding: 8px 18px !important;
    border: none !important;
    background-color: transparent !important;
    transition: all 0.2s ease !important;
}

.stTabs [data-baseweb="tab"]:hover {
    color: #00F0FF !important;
    background-color: rgba(0, 240, 255, 0.08) !important;
}

.stTabs [aria-selected="true"] {
    color: #00F0FF !important;
    background: linear-gradient(135deg, rgba(0, 240, 255, 0.20), rgba(56, 189, 248, 0.10)) !important;
    border: 1px solid rgba(0, 240, 255, 0.45) !important;
    box-shadow: 0 0 18px rgba(0, 240, 255, 0.25), inset 0 1px 0 rgba(255, 255, 255, 0.15) !important;
}

/* Premium 2026 Glassmorphic Card Container */
.mf-glass-card {
    background: linear-gradient(135deg, rgba(12, 18, 36, 0.82) 0%, rgba(8, 12, 26, 0.92) 100%);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 18px;
    padding: 22px 26px;
    margin-bottom: 22px;
    backdrop-filter: blur(24px);
    box-shadow: 0 16px 40px -10px rgba(0, 0, 0, 0.65), inset 0 1px 0 0 rgba(255, 255, 255, 0.09);
    transition: all 0.28s cubic-bezier(0.16, 1, 0.3, 1);
}

.mf-glass-card:hover {
    border-color: rgba(0, 240, 255, 0.35);
    box-shadow: 0 20px 48px -8px rgba(0, 240, 255, 0.2), inset 0 1px 0 0 rgba(255, 255, 255, 0.16);
    transform: translateY(-2px);
}

/* Primary Action Buttons */
.stButton>button {
    background: linear-gradient(135deg, #00F0FF 0%, #38BDF8 60%, #3B82F6 100%) !important;
    color: #030611 !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 10px 24px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 800 !important;
    font-size: 0.92rem !important;
    letter-spacing: 0.4px !important;
    box-shadow: 0 6px 22px -3px rgba(0, 240, 255, 0.42), inset 0 1px 0 rgba(255, 255, 255, 0.4) !important;
    transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

.stButton>button:hover {
    background: linear-gradient(135deg, #38BDF8 0%, #60A5FA 100%) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(0, 240, 255, 0.65) !important;
    color: #000000 !important;
}

.stButton>button:active {
    transform: translateY(0) !important;
}

/* Secondary Button Styling */
button[kind="secondary"] {
    background: rgba(14, 20, 42, 0.8) !important;
    color: #F8FAFC !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 12px !important;
}

button[kind="secondary"]:hover {
    background: rgba(28, 38, 72, 0.9) !important;
    border-color: rgba(255, 255, 255, 0.22) !important;
}

/* Form Inputs, Textarea & Selectboxes */
.stTextInput>div>div>input, 
.stTextArea>div>div>textarea, 
.stSelectbox>div>div>div {
    background-color: rgba(9, 14, 28, 0.88) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 12px !important;
    font-size: 0.96rem !important;
    font-family: 'JetBrains Mono', monospace !important;
    transition: all 0.2s ease !important;
}

.stTextInput>div>div>input:focus, 
.stTextArea>div>div>textarea:focus, 
.stSelectbox>div>div>div:focus {
    border-color: var(--accent-cyan) !important;
    box-shadow: 0 0 0 2px rgba(0, 240, 255, 0.3) !important;
}

/* Metrics Cards Overhaul */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(12, 18, 36, 0.72) 0%, rgba(8, 12, 26, 0.85) 100%) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 16px !important;
    padding: 16px 20px !important;
    box-shadow: 0 12px 28px -6px rgba(0, 0, 0, 0.45) !important;
}

[data-testid="stMetricValue"] {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 800 !important;
    color: #00F0FF !important;
    font-size: 1.9rem !important;
    letter-spacing: -0.02em !important;
}

[data-testid="stMetricLabel"] {
    font-size: 0.72rem !important;
    text-transform: uppercase !important;
    letter-spacing: 1.2px !important;
    color: var(--text-secondary) !important;
    font-weight: 700 !important;
}

/* Expander Styling */
.streamlit-expanderHeader {
    background-color: rgba(12, 18, 36, 0.75) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 14px !important;
    color: #F1F5F9 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}

.streamlit-expanderHeader:hover {
    border-color: rgba(0, 240, 255, 0.35) !important;
}

/* Dataframe & Table Dark Overrides */
[data-testid="stDataFrame"] {
    border-radius: 14px !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    overflow: hidden !important;
    box-shadow: 0 14px 34px rgba(0, 0, 0, 0.5) !important;
}

/* Alerts / Callouts */
.stAlert {
    background-color: rgba(12, 18, 36, 0.88) !important;
    border-radius: 14px !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    backdrop-filter: blur(16px) !important;
}

/* Custom Scrollbar */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: #04060C;
}
::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.15);
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: rgba(0, 240, 255, 0.5);
}
</style>
"""


def apply_theme():
    """Injects the unified 2026 global theme CSS into Streamlit."""
    st.markdown(GLOBAL_THEME_CSS, unsafe_allow_html=True)


apply_custom_theme = apply_theme


def render_circular_gauge(percentage: int, label: str, color: str = "#00F0FF", size: int = 110) -> str:
    """Generates an ultra-crisp SVG circular gauge with glowing meter arc."""
    stroke_width = 8
    radius = (size - stroke_width * 2) // 2
    circumference = int(2 * 3.14159 * radius)
    clamped_pct = max(0, min(100, percentage))
    stroke_dashoffset = int(circumference - (clamped_pct / 100.0) * circumference)
    cx = size // 2
    cy = size // 2

    return f"""
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
        <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" style="transform: rotate(-90deg);">
            <!-- Background Ring -->
            <circle cx="{cx}" cy="{cy}" r="{radius}" fill="transparent" stroke="rgba(255, 255, 255, 0.08)" stroke-width="{stroke_width}" />
            <!-- Glowing Meter Arc -->
            <circle cx="{cx}" cy="{cy}" r="{radius}" fill="transparent" stroke="{color}" stroke-width="{stroke_width}"
                stroke-dasharray="{circumference}" stroke-dashoffset="{stroke_dashoffset}" stroke-linecap="round"
                style="filter: drop-shadow(0 0 8px {color}88); transition: stroke-dashoffset 0.6s ease;" />
        </svg>
        <div style="margin-top: -{size * 0.62}px; text-align: center; pointer-events: none;">
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.45rem; font-weight: 800; color: #FFFFFF; line-height: 1;">
                {clamped_pct}%
            </div>
            <div style="font-size: 0.65rem; color: #94A3B8; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px; margin-top: 4px;">
                {label}
            </div>
        </div>
        <div style="height: {size * 0.25}px;"></div>
    </div>
    """


def render_brand_header(title: str, subtitle: str, badge: str = "LIVE DETERMINISTIC PSYCHOMETRICS"):
    """Renders a consistent, high-end 2026 Linear-style hero header across all portal pages."""
    header_html = f"""
    <div style="
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 14px;
        padding: 14px 0 22px 0;
        margin-bottom: 22px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    ">
        <div>
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px;">
                <span style="
                    font-size: 1.85rem;
                    background: linear-gradient(135deg, #00F0FF 0%, #38BDF8 50%, #818CF8 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    font-family: 'Space Grotesk', sans-serif;
                    font-weight: 800;
                    letter-spacing: -0.8px;
                ">
                    MasteryFlow
                </span>
                <span style="
                    background: rgba(0, 240, 255, 0.12);
                    color: #00F0FF;
                    border: 1px solid rgba(0, 240, 255, 0.35);
                    font-size: 0.70rem;
                    font-weight: 700;
                    padding: 3px 10px;
                    border-radius: 9999px;
                    letter-spacing: 0.8px;
                    text-transform: uppercase;
                    box-shadow: 0 0 12px rgba(0, 240, 255, 0.15);
                ">
                    ● {badge}
                </span>
            </div>
            <div style="font-size: 0.92rem; color: #94A3B8; font-weight: 400; font-family: 'Plus Jakarta Sans', sans-serif;">
                {subtitle}
            </div>
        </div>
        <div style="text-align: right;">
            <span style="font-size: 0.74rem; color: #64748B; text-transform: uppercase; letter-spacing: 1px; font-weight: 700;">
                YUVA Megathon 2026 &middot; Domain 4: Intelligent Educational Systems
            </span>
            <div style="font-size: 0.82rem; color: #E2E8F0; font-weight: 600; margin-top: 3px;">
                Team Nightfarers &middot; Lead: Ayon Mukherjee
            </div>
        </div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)
