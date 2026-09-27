import streamlit as st
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title='Maintenance', page_icon='🚗', layout='wide')

def load_css():
    css_path = Path(__file__).parent.parent / "styles" / "brutalist.css"
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

if "vehicle_data" not in st.session_state or st.session_state.vehicle_data is None:
    st.warning("⚠️ VEHICLE DATA NOT FOUND. PLEASE COMPLETE INPUT FIRST.")
    st.stop()

v_data = st.session_state.vehicle_data

st.markdown("<h1 style='font-weight: 900; text-transform: uppercase;'>04 MAINTENANCE</h1>", unsafe_allow_html=True)
st.markdown("---")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown("<div style='background: white; border: 2px solid #1A1A1A; padding: 20px; text-align: center; height: 100%;'>", unsafe_allow_html=True)
    st.markdown("<h3>EST. ANNUAL COST</h3>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-size: 3rem; margin: 0; color: #1A1A1A; font-family: \"IBM Plex Mono\", monospace;'>₹15,400</h1>", unsafe_allow_html=True)
    st.markdown("<span style='background: #1A1A1A; color: white; padding: 2px 5px; font-size: 0.8rem; font-weight: bold;'>ESTIMATED</span>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div style='background: white; border: 2px solid #1A1A1A; padding: 20px; text-align: center; height: 100%;'>", unsafe_allow_html=True)
    st.markdown("<h3>NEXT SERVICE DUE</h3>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-size: 2.5rem; margin: 0; color: #1A1A1A; font-family: \"IBM Plex Mono\", monospace;'>20,000 KM</h1>", unsafe_allow_html=True)
    st.markdown("<p>or in 4 Months</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div style='background: white; border: 2px solid #1A1A1A; padding: 20px; text-align: center; height: 100%;'>", unsafe_allow_html=True)
    st.markdown("<h3>RISK SCORE</h3>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-size: 3rem; margin: 0; color: #FF2800; font-family: \"IBM Plex Mono\", monospace;'>LOW</h1>", unsafe_allow_html=True)
    st.markdown("<p>Predictive failure risk</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.write("---")
col4, col5 = st.columns(2)

with col4:
    st.markdown("### EVENT PROBABILITIES (YEAR 1-3)")
    fig = go.Figure(go.Bar(
        x=[0.15, 0.45, 0.85, 0.05],
        y=['Major Repair', 'Brake Pads', 'Oil Change', 'Battery Replace'],
        orientation='h',
        marker=dict(color='#1A1A1A')
    ))
    fig.update_layout(
        plot_bgcolor='#F5F5F0', paper_bgcolor='#F5F5F0', margin=dict(l=0, r=0, t=0, b=0), height=300
    )
    st.plotly_chart(fig, use_container_width=True)

with col5:
    st.markdown("### COST BREAKDOWN (5 YEARS)")
    st.markdown("**Scheduled Servicing**: ₹45,000")
    st.markdown("**Wear & Tear (Tires/Brakes)**: ₹30,000")
    st.markdown("**Unexpected Repairs**: ₹15,000")
    st.markdown("**TOTAL**: ₹90,000")

st.markdown("### RISK FACTORS")
st.markdown("- **Age-related component fatigue**: Minimal until year 5.")
st.markdown("- **Driving environment**: City driving increases brake wear.")
st.markdown("---")
st.markdown("### OEM SCHEDULE REFERENCE")
st.table([
    {"Interval": "10,000 km", "Action": "Oil & Filter Change, General Check"},
    {"Interval": "20,000 km", "Action": "AC Filter, Brake Inspection"},
    {"Interval": "40,000 km", "Action": "Coolant, Brake Fluid, Major Check"}
])
