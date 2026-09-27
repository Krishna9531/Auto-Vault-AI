# -*- coding: utf-8 -*-
"""
AUTOVAULT AI — Clean Home Page
"""
import streamlit as st
from pathlib import Path
import sys

# Ensure imports work
sys.path.insert(0, str(Path(__file__).parent.parent))

# Page config must be first
st.set_page_config(
    page_title="AUTOVAULT AI",
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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');

*, body, .stApp {
    font-family: 'Inter', system-ui, sans-serif;
}

/* Hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 4rem 4rem !important; max-width: 1400px !important; }

/* ── Minimalist Landing Section ── */
.landing-wrapper {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    min-height: 65vh;
    position: relative;
    z-index: 10;
}

.title {
    font-size: clamp(4rem, 8vw, 7rem);
    font-weight: 900;
    line-height: 0.95;
    letter-spacing: -0.04em;
    color: #1A1A1A;
    margin-bottom: 1.5rem;
}
.title span { color: #FF2800; }

.subtitle {
    font-size: clamp(1.2rem, 2vw, 1.5rem);
    font-weight: 400;
    color: #444;
    max-width: 700px;
    line-height: 1.6;
    margin-bottom: 3rem;
}

/* ── Clean Huge CTA Button ── */
.cta-button-container {
    width: 100%;
    max-width: 400px;
}
.cta-button-container .stButton > button {
    background: #1A1A1A !important;
    color: #FFFFFF !important;
    border: none !important;
    padding: 24px 40px !important;
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    border-radius: 8px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1) !important;
    width: 100% !important;
}
.cta-button-container .stButton > button:hover {
    background: #FF2800 !important;
    transform: translateY(-4px) !important;
    box-shadow: 0 15px 40px rgba(255,40,0,0.2) !important;
}
.cta-button-container .stButton > button:active {
    transform: translateY(0px) !important;
}

/* ── Abstract Background Graphic ── */
.bg-graphic {
    position: absolute;
    top: 5%;
    right: 5%;
    width: 50vw;
    height: 50vw;
    max-width: 700px;
    max-height: 700px;
    background: radial-gradient(circle, rgba(255,40,0,0.04) 0%, rgba(255,40,0,0) 70%);
    border-radius: 50%;
    z-index: 1;
    pointer-events: none;
}
.bg-grid {
    position: absolute;
    top: 15%;
    right: 10%;
    width: 400px;
    height: 400px;
    background-image: radial-gradient(#1A1A1A 2px, transparent 2px);
    background-size: 30px 30px;
    opacity: 0.04;
    z-index: 2;
    pointer-events: none;
}
</style>

<div class="bg-graphic"></div>
<div class="bg-grid"></div>

<div class="landing-wrapper">
    <div class="title">AUTO<span>VAULT</span></div>
    <div class="subtitle">
        The complete automotive intelligence platform.<br>
        Predict depreciation curves, forecast maintenance risks, and calculate true total cost of ownership before making your decision.
    </div>
</div>
""", unsafe_allow_html=True)

# The button needs to be in Streamlit python space to handle the routing
st.markdown("<div class='cta-button-container'>", unsafe_allow_html=True)
if st.button("GET STARTED →"):
    st.switch_page("pages/01_Vehicle_Input.py")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<div style="margin-top: 20px; font-size: 0.85rem; color: #888; font-weight: 500;">
    Select a vehicle to unlock all analysis modules.
</div>
""", unsafe_allow_html=True)
