# -*- coding: utf-8 -*-
"""
AUTOVAULT AI — Landing Page
"""
import streamlit as st
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(
    page_title="AUTOVAULT AI",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;700&family=Inter:wght@300;400;700;900&display=swap');

*, body, .stApp {
    background-color: #F5F5F0 !important;
    font-family: 'Inter', system-ui, sans-serif;
}

/* Hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 2rem 3rem !important; max-width: 1400px; }

/* Hero */
.hero-title {
    font-size: clamp(3rem, 7vw, 6rem);
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
    margin: 1.5rem 0;
}

/* Module cards */
.module-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin: 2rem 0;
}
.module-card {
    background: #FFFFFF;
    border: 2px solid #1A1A1A;
    padding: 24px 20px;
    position: relative;
    overflow: hidden;
    transition: background 0.15s;
    min-height: 160px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.module-card:hover { background: #1A1A1A; }
.module-card:hover .mc-num, .module-card:hover .mc-title, .module-card:hover .mc-desc { color: #F5F5F0 !important; }
.module-card:hover .mc-accent { background: #FF2800; }

.mc-num {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.2em;
    color: #FF2800;
    margin-bottom: 8px;
}
.mc-title {
    font-size: 1.1rem;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #1A1A1A;
    line-height: 1.2;
    margin: 0 0 10px 0;
}
.mc-desc {
    font-size: 0.82rem;
    color: #555;
    line-height: 1.5;
    flex-grow: 1;
}
.mc-accent {
    width: 32px;
    height: 3px;
    background: #1A1A1A;
    margin-top: 14px;
}

/* Stats bar */
.stats-bar {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    border: 2px solid #1A1A1A;
    background: #1A1A1A;
    gap: 2px;
    margin: 2rem 0;
}
.stat-cell {
    background: #F5F5F0;
    padding: 20px 24px;
    text-align: center;
}
.stat-num {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    color: #FF2800;
    line-height: 1;
}
.stat-label {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #1A1A1A;
    margin-top: 4px;
}

/* CTA Button */
.stButton > button {
    background: #1A1A1A !important;
    color: #F5F5F0 !important;
    border: none !important;
    border-radius: 0 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    padding: 1rem 2rem !important;
    width: 100% !important;
    transition: background 0.15s !important;
}
.stButton > button:hover {
    background: #FF2800 !important;
    color: white !important;
}

/* Tag line */
.tagline-box {
    border-left: 4px solid #FF2800;
    padding: 12px 20px;
    background: white;
    border-top: 2px solid #1A1A1A;
    border-right: 2px solid #1A1A1A;
    border-bottom: 2px solid #1A1A1A;
    margin-bottom: 2rem;
}
</style>
""", unsafe_allow_html=True)

# Session state init
for key in ["vehicle_data", "analysis_results"]:
    if key not in st.session_state:
        st.session_state[key] = None

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<h1 class="hero-title">AUTO<span class="hero-red">VAULT</span> AI</h1>
<p class="hero-sub">Automotive Risk · Value · Ownership Intelligence</p>
<hr class="hero-divider"/>
""", unsafe_allow_html=True)

# ── Tagline ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="tagline-box">
    <span style="font-weight:700;font-size:0.95rem;">
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

# ── Module grid ───────────────────────────────────────────────────────────────
modules = [
    ("01", "VEHICLE\nINPUT",    "Configure brand, model, variant, usage patterns, and financing details."),
    ("02", "HEALTH\nANALYSIS", "Estimate mechanical & electrical health from age, mileage, and fuel type."),
    ("03", "DEPRECIATION",      "Forecast year-by-year residual value with confidence intervals and SHAP factors."),
    ("04", "MAINTENANCE",       "Predict service event probabilities and 5-year maintenance cost exposure."),
    ("05", "TCO ENGINE",        "Compute total ownership cost — EMI, fuel, insurance, tyres, and resale."),
    ("06", "FINANCIAL\nRISK",   "Score purchase, running, resale, and financing risk across 5 dimensions."),
    ("07", "WHAT-IF\nSIMULATOR","Live scenario modeling — change mileage, fuel price, ownership period."),
    ("08", "COMPARE",           "Benchmark multiple vehicles side-by-side on TCO, resale, and risk."),
]

cols_a = st.columns(4)
cols_b = st.columns(4)

for i, (num, title, desc) in enumerate(modules):
    col = cols_a[i] if i < 4 else cols_b[i - 4]
    with col:
        st.markdown(f"""
        <div class="module-card">
            <div>
                <div class="mc-num">{num}</div>
                <div class="mc-title">{title.replace(chr(10), ' ')}</div>
                <div class="mc-desc">{desc}</div>
            </div>
            <div class="mc-accent"></div>
        </div>
        """, unsafe_allow_html=True)

# ── CTA ───────────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
if st.button("BEGIN ANALYSIS  →", use_container_width=True):
    st.switch_page("pages/01_Vehicle_Input.py")

# ── Footer note ───────────────────────────────────────────────────────────────
st.markdown("""
<p style="font-size:0.72rem;color:#888;text-align:center;margin-top:1.5rem;font-family:'IBM Plex Mono',monospace;">
AUTOVAULT AI · All values are model-based estimates · Not financial advice · India Market · 2025–26
</p>
""", unsafe_allow_html=True)
