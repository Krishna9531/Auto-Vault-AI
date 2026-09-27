import streamlit as st
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title='Simulator', page_icon='🚗', layout='wide')

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

st.markdown("<h1 style='font-weight: 900; text-transform: uppercase;'>07 SIMULATOR</h1>", unsafe_allow_html=True)
st.markdown("---")

col_sliders, col_results = st.columns([1, 2])

with col_sliders:
    st.markdown("### SCENARIO VARIABLES")
    
    if st.button("RESET TO BASE", use_container_width=True):
        st.session_state.sim_years = 5
        st.session_state.sim_km = v_data['annual_mileage']
        st.session_state.sim_fuel = 1.0
        st.session_state.sim_resale = 1.0
        st.rerun()

    years = st.slider("OWNERSHIP YEARS", 1, 15, st.session_state.get('sim_years', 5), key='sim_years')
    km = st.slider("ANNUAL KM", 1000, 100000, st.session_state.get('sim_km', v_data['annual_mileage']), key='sim_km')
    fuel = st.slider("FUEL PRICE MULTIPLIER", 0.5, 2.0, st.session_state.get('sim_fuel', 1.0), key='sim_fuel')
    resale = st.slider("RESALE OPTIMISM", 0.5, 1.5, st.session_state.get('sim_resale', 1.0), key='sim_resale')

with col_results:
    st.markdown("### SCENARIO COMPARISON")
    
    # Calculate dummy arrays based on sliders
    base_tco = [(i+1) * 1.5 for i in range(15)]
    sim_tco = [(i+1) * 1.5 * fuel * (km/10000) for i in range(15)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(range(1, years+1)), y=base_tco[:years], mode='lines', name='Base Scenario', line=dict(color='#1A1A1A', dash='dash')))
    fig.add_trace(go.Scatter(x=list(range(1, years+1)), y=sim_tco[:years], mode='lines+markers', name='Simulated Scenario', line=dict(color='#FF2800', width=3)))
    
    fig.update_layout(plot_bgcolor='#F5F5F0', paper_bgcolor='#F5F5F0', margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig, use_container_width=True)

st.write("---")
st.markdown("### SNAPSHOT RESULTS")
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("#### 3-YEAR TCO")
    st.markdown(f"**₹{sim_tco[2]:.2f}L**")
with c2:
    st.markdown("#### 5-YEAR TCO")
    st.markdown(f"**₹{sim_tco[4]:.2f}L**")
with c3:
    st.markdown("#### 7-YEAR TCO")
    st.markdown(f"**₹{sim_tco[6]:.2f}L**")

st.info("**WHAT-IF**: Increasing fuel costs by 20% would add approximately ₹50,000 to your total running costs over 5 years. Opting for a higher resale optimism assumes you keep the vehicle in pristine condition.")
