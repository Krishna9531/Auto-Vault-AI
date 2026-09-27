import streamlit as st
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title='Financial Risk', page_icon='🚗', layout='wide')

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

st.markdown("<h1 style='font-weight: 900; text-transform: uppercase;'>06 FINANCIAL RISK</h1>", unsafe_allow_html=True)
st.caption("Model-based financial exposure score")
st.markdown("---")

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("<div style='background: white; border: 2px solid #1A1A1A; padding: 20px; text-align: center;'>", unsafe_allow_html=True)
    st.markdown("<h3>OVERALL RISK SCORE</h3>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-size: 5rem; margin: 0; color: #1A1A1A; font-family: \"IBM Plex Mono\", monospace;'>4.2<span style='font-size: 2rem;'>/10</span></h1>", unsafe_allow_html=True)
    st.markdown("<p>MODERATE RISK</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.write("")
    st.markdown("### BREAK-EVEN YEAR")
    st.markdown("<h2 style='font-size: 2rem; margin: 0; color: #FF2800; font-family: \"IBM Plex Mono\", monospace;'>YEAR 3</h2>", unsafe_allow_html=True)
    st.write("The point where asset value exceeds outstanding loan balance.")

with col2:
    st.markdown("### RISK DIMENSIONS")
    fig = go.Figure(data=go.Scatterpolar(
      r=[4, 3, 6, 2, 5],
      theta=['Depreciation', 'Maintenance', 'Fuel Cost', 'Insurance', 'Market Demand'],
      fill='toself',
      fillcolor='rgba(26, 26, 26, 0.5)',
      line=dict(color='#1A1A1A')
    ))
    fig.update_layout(
      polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
      showlegend=False,
      plot_bgcolor='#F5F5F0', paper_bgcolor='#F5F5F0', margin=dict(l=20, r=20, t=20, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)

st.write("---")
st.markdown("### RISK INSIGHTS")
st.markdown("- **Depreciation Risk**: Moderate. Segment holds value steadily but new launches may disrupt.")
st.markdown("- **Maintenance Risk**: Low. Well-documented service network and parts availability.")
st.markdown("- **Energy Risk**: High. Subject to fuel price volatility over the next 5 years.")
