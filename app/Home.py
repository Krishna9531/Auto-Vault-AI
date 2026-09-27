# -*- coding: utf-8 -*-
"""
AUTOVAULT AI — Home Page
"""
import streamlit as st
from pathlib import Path
import sys

# Ensure imports work
sys.path.insert(0, str(Path(__file__).parent.parent))

# Page config must be first
st.set_page_config(
    page_title="AUTOVAULT AI",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom sidebar
try:
    from app.components.navigation import build_sidebar
    build_sidebar()
except Exception as e:
    pass

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;700&family=Inter:wght@300;400;700;900&display=swap');

*, body, .stApp {
    background-color: #F5F5F0 !important;
    font-family: 'Inter', system-ui, sans-serif;
    color: #1A1A1A;
}

/* Hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2.5rem 3rem !important; max-width: 1400px !important; }

/* Hero */
.hero-title {
    font-size: clamp(3rem, 7vw, 5.5rem);
    font-weight: 900;
    letter-spacing: -0.02em;
    text-transform: uppercase;
    color: #1A1A1A;
    line-height: 0.95;
    margin: 0;
}
.hero-red { color: #FF2800; }
.hero-sub {
    font-size: 1rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #555;
    margin-top: 1rem;
    font-family: 'IBM Plex Mono', monospace;
}
.hero-divider {
    border: none;
    border-top: 4px solid #1A1A1A;
    margin: 1.5rem 0 2.5rem 0;
}

/* Tag line */
.tagline-box {
    border-left: 4px solid #FF2800;
    padding: 16px 24px;
    background: white;
    border-top: 2px solid #1A1A1A;
    border-right: 2px solid #1A1A1A;
    border-bottom: 2px solid #1A1A1A;
    margin-bottom: 2rem;
    box-shadow: 4px 4px 0 #1A1A1A;
}

/* Stats bar */
.stats-bar {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    border: 2px solid #1A1A1A;
    background: #1A1A1A;
    gap: 2px;
    margin: 2.5rem 0;
    box-shadow: 4px 4px 0 #FF2800;
}
.stat-cell {
    background: #F5F5F0;
    padding: 24px;
    text-align: center;
}
.stat-num {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 2.4rem;
    font-weight: 700;
    color: #FF2800;
    line-height: 1;
}
.stat-label {
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #1A1A1A;
    margin-top: 8px;
}

/* ── NATIVE STREAMLIT CARDS OVERRIDE ── */
[data-testid="stVerticalBlockBorderWrapper"] {
    border: 2px solid #1A1A1A !important;
    border-radius: 0 !important;
    background: #FFFFFF !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease !important;
    height: 100% !important;
}
[data-testid="stVerticalBlockBorderWrapper"]:hover {
    transform: translateY(-4px) !important;
    box-shadow: 6px 8px 0px #FF2800 !important;
}

/* ── NATIVE BUTTONS INSIDE CARDS ── */
[data-testid="stVerticalBlockBorderWrapper"] .stButton > button {
    background: #1A1A1A !important;
    color: white !important;
    border: 2px solid #1A1A1A !important;
    border-radius: 0 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    width: 100% !important;
    padding: 12px !important;
    transition: all 0.15s ease !important;
    margin-top: 10px !important;
}
[data-testid="stVerticalBlockBorderWrapper"] .stButton > button:hover {
    background: #FF2800 !important;
    border-color: #FF2800 !important;
    color: white !important;
}
[data-testid="stVerticalBlockBorderWrapper"] .stButton > button:active {
    transform: translateY(2px) !important;
}
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<h1 class="hero-title">AUTO<span class="hero-red">VAULT</span> AI</h1>
<p class="hero-sub">Automotive Risk · Value · Ownership Intelligence</p>
<hr class="hero-divider"/>
""", unsafe_allow_html=True)

# ── Tagline ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="tagline-box">
    <span style="font-weight:700;font-size:1.1rem;color:#1A1A1A;">
    Enter any vehicle. Get its complete financial future —
    depreciation curve, 5-year cost, resale value, maintenance risk, and what-if scenarios.
    </span>
</div>
""", unsafe_allow_html=True)

# ── Stats bar ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="stats-bar">
    <div class="stat-cell">
        <div class="stat-num">50+</div>
        <div class="stat-label">Vehicle Models</div>
    </div>
    <div class="stat-cell">
        <div class="stat-num">8</div>
        <div class="stat-label">Intelligence Modules</div>
    </div>
    <div class="stat-cell">
        <div class="stat-num">20</div>
        <div class="stat-label">Indian Cities</div>
    </div>
    <div class="stat-cell">
        <div class="stat-num">100%</div>
        <div class="stat-label">India-Specific Data</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br><h3 style='font-size:1.2rem;font-weight:900;letter-spacing:0.1em;text-transform:uppercase;'>INTELLIGENCE MODULES</h3>", unsafe_allow_html=True)

# ── Interactive Native Cards ──────────────────────────────────────────────────
modules = [
    ("01", "VEHICLE INPUT", "Configure brand, model, variant, usage patterns, and financing details.", "pages/01_Vehicle_Input.py"),
    ("02", "HEALTH ANALYSIS", "Estimate mechanical & electrical health from age, mileage, and fuel type.", "pages/02_Vehicle_Health.py"),
    ("03", "DEPRECIATION", "Forecast year-by-year residual value with confidence intervals.", "pages/03_Depreciation.py"),
    ("04", "MAINTENANCE", "Predict service event probabilities and 5-year maintenance exposure.", "pages/04_Maintenance.py"),
    ("05", "TCO ENGINE", "Compute total ownership cost — EMI, fuel, insurance, tyres, and resale.", "pages/05_TCO.py"),
    ("06", "FINANCIAL RISK", "Score purchase, running, resale, and financing risk across 5 dimensions.", "pages/06_Financial_Risk.py"),
    ("07", "SIMULATOR", "Live scenario modeling — change mileage, fuel price, ownership period.", "pages/07_Simulator.py"),
    ("08", "COMPARE", "Benchmark multiple vehicles side-by-side on TCO, resale, and risk.", "pages/08_Compare.py"),
]

# Row 1
c1, c2, c3, c4 = st.columns(4)
row1_cols = [c1, c2, c3, c4]

for i in range(4):
    num, title, desc, path = modules[i]
    with row1_cols[i]:
        with st.container(border=True):
            st.markdown(f"<div style='color:#FF2800;font-family:monospace;font-weight:700;font-size:0.8rem;letter-spacing:0.2em;margin-bottom:8px;'>{num}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:1.05rem;font-weight:900;line-height:1.2;text-transform:uppercase;margin-bottom:12px;'>{title}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:0.85rem;color:#555;margin-bottom:20px;line-height:1.5;'>{desc}</div>", unsafe_allow_html=True)
            if st.button("OPEN MODULE →", key=f"btn_{num}"):
                st.switch_page(path)

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# Row 2
c5, c6, c7, c8 = st.columns(4)
row2_cols = [c5, c6, c7, c8]

for i in range(4, 8):
    num, title, desc, path = modules[i]
    with row2_cols[i-4]:
        with st.container(border=True):
            st.markdown(f"<div style='color:#FF2800;font-family:monospace;font-weight:700;font-size:0.8rem;letter-spacing:0.2em;margin-bottom:8px;'>{num}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:1.05rem;font-weight:900;line-height:1.2;text-transform:uppercase;margin-bottom:12px;'>{title}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:0.85rem;color:#555;margin-bottom:20px;line-height:1.5;'>{desc}</div>", unsafe_allow_html=True)
            if st.button("OPEN MODULE →", key=f"btn_{num}"):
                st.switch_page(path)

# ── Footer note ───────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:4rem;padding-top:2rem;border-top:2px dashed #D0D0C8;">
    <p style="font-size:0.75rem;color:#888;font-family:'IBM Plex Mono',monospace;letter-spacing:0.1em;text-transform:uppercase;">
    AUTOVAULT AI · All values are model-based estimates · Not financial advice · India Market
    </p>
</div>
""", unsafe_allow_html=True)
