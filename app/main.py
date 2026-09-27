import streamlit as st
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

st.set_page_config(
    page_title='AUTOVAULT AI',
    page_icon='🚗',
    layout='wide',
    initial_sidebar_state='expanded'
)

def load_css():
    css_path = Path(__file__).parent / "styles" / "brutalist.css"
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        # Fallback minimal CSS if not present
        st.markdown("""
        <style>
        .stApp { background-color: #F5F5F0; }
        .stMarkdown { font-family: system-ui; }
        .stButton>button { border: 2px solid #1A1A1A !important; border-radius: 0 !important; font-weight: bold; }
        </style>
        """, unsafe_allow_html=True)

load_css()

# Initialize session state
if "vehicle_data" not in st.session_state:
    st.session_state.vehicle_data = None
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None

st.markdown("<h1 style='font-weight: 900; text-transform: uppercase; border-bottom: 4px solid #1A1A1A; padding-bottom: 10px;'>AUTOVAULT AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 1.2rem; font-weight: bold; margin-bottom: 2rem;'>COMPREHENSIVE RESIDUAL FORECASTING AND TOTAL COST OF OWNERSHIP ENGINE</p>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("<div style='background: white; border: 2px solid #1A1A1A; padding: 20px; height: 150px;'><h3 style='margin-top:0'>01 INPUT</h3><p>Configure your vehicle parameters and usage patterns.</p></div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div style='background: white; border: 2px solid #1A1A1A; padding: 20px; height: 150px;'><h3 style='margin-top:0'>02 HEALTH</h3><p>Analyze mechanical & electrical wear based on age & mileage.</p></div>", unsafe_allow_html=True)
with col3:
    st.markdown("<div style='background: white; border: 2px solid #1A1A1A; padding: 20px; height: 150px;'><h3 style='margin-top:0'>03 DEPRECIATION</h3><p>Forecast residual value over time.</p></div>", unsafe_allow_html=True)
with col4:
    st.markdown("<div style='background: white; border: 2px solid #1A1A1A; padding: 20px; height: 150px;'><h3 style='margin-top:0'>04 MAINTENANCE</h3><p>Predict service and unexpected repair costs.</p></div>", unsafe_allow_html=True)

st.write("")
col5, col6, col7, col8 = st.columns(4)

with col5:
    st.markdown("<div style='background: white; border: 2px solid #1A1A1A; padding: 20px; height: 150px;'><h3 style='margin-top:0'>05 TCO</h3><p>Calculate total cost of ownership including all factors.</p></div>", unsafe_allow_html=True)
with col6:
    st.markdown("<div style='background: white; border: 2px solid #1A1A1A; padding: 20px; height: 150px;'><h3 style='margin-top:0'>06 RISK</h3><p>Evaluate financial exposure and risk elements.</p></div>", unsafe_allow_html=True)
with col7:
    st.markdown("<div style='background: white; border: 2px solid #1A1A1A; padding: 20px; height: 150px;'><h3 style='margin-top:0'>07 SIMULATOR</h3><p>Play with variables to see future value scenarios.</p></div>", unsafe_allow_html=True)
with col8:
    st.markdown("<div style='background: white; border: 2px solid #1A1A1A; padding: 20px; height: 150px;'><h3 style='margin-top:0'>08 COMPARE</h3><p>Benchmark multiple vehicles side-by-side.</p></div>", unsafe_allow_html=True)

st.write("")
if st.button("PROCEED TO VEHICLE INPUT ➔", use_container_width=True):
    st.switch_page("pages/01_Vehicle_Input.py")
