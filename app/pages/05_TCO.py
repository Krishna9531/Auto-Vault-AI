import streamlit as st
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title='TCO', page_icon='🚗', layout='wide')

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

st.markdown("<h1 style='font-weight: 900; text-transform: uppercase;'>05 TOTAL COST OF OWNERSHIP</h1>", unsafe_allow_html=True)

period = st.radio("SELECT PERIOD", [3, 5, 7], index=1, horizontal=True)

st.markdown("---")

col1, col2, col3 = st.columns(3)

# Dummy TCO calculations
depreciation_cost = v_data['purchase_price'] * 0.40 * (period/5)
maintenance_cost = 0.90 * (period/5)
fuel_cost = 4.0 * (period/5)
insurance_cost = 1.5 * (period/5)
net_tco = depreciation_cost + maintenance_cost + fuel_cost + insurance_cost

with col1:
    st.markdown("<div style='background: white; border: 2px solid #1A1A1A; padding: 20px; text-align: center;'>", unsafe_allow_html=True)
    st.markdown(f"<h3>{period}-YEAR NET TCO</h3>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='font-size: 3rem; margin: 0; color: #1A1A1A; font-family: \"IBM Plex Mono\", monospace;'>₹{net_tco:.2f}L</h1>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div style='background: white; border: 2px solid #1A1A1A; padding: 20px; text-align: center;'>", unsafe_allow_html=True)
    st.markdown("<h3>ANNUAL COST</h3>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='font-size: 3rem; margin: 0; color: #1A1A1A; font-family: \"IBM Plex Mono\", monospace;'>₹{(net_tco*100000/period):,.0f}</h1>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div style='background: white; border: 2px solid #1A1A1A; padding: 20px; text-align: center;'>", unsafe_allow_html=True)
    st.markdown("<h3>MONTHLY COST</h3>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='font-size: 3rem; margin: 0; color: #1A1A1A; font-family: \"IBM Plex Mono\", monospace;'>₹{(net_tco*100000/(period*12)):,.0f}</h1>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.write("---")
col4, col5 = st.columns(2)

with col4:
    st.markdown("### TCO BREAKDOWN")
    fig = go.Figure(go.Waterfall(
        name="20", orientation="v",
        measure=["relative", "relative", "relative", "relative", "total"],
        x=["Depreciation", "Fuel/Energy", "Maintenance", "Insurance/Tax", "Total"],
        textposition="outside",
        y=[depreciation_cost, fuel_cost, maintenance_cost, insurance_cost, net_tco],
        connector={"line":{"color":"#1A1A1A"}},
        increasing={"marker":{"color":"#FF2800"}},
        totals={"marker":{"color":"#1A1A1A"}}
    ))
    fig.update_layout(plot_bgcolor='#F5F5F0', paper_bgcolor='#F5F5F0')
    st.plotly_chart(fig, use_container_width=True)

with col5:
    st.markdown("### YEAR-WISE BREAKDOWN")
    st.table([
        {"Year": 1, "Depreciation": f"₹{(depreciation_cost*0.4):.2f}L", "Running Costs": f"₹{((fuel_cost+maintenance_cost+insurance_cost)/period):.2f}L"},
        {"Year": 2, "Depreciation": f"₹{(depreciation_cost*0.25):.2f}L", "Running Costs": f"₹{((fuel_cost+maintenance_cost+insurance_cost)/period):.2f}L"},
        {"Year": 3, "Depreciation": f"₹{(depreciation_cost*0.15):.2f}L", "Running Costs": f"₹{((fuel_cost+maintenance_cost+insurance_cost)/period):.2f}L"}
    ])

    if v_data.get('income', 0) > 0:
        annual_income = v_data['income'] * 12
        annual_tco = (net_tco * 100000) / period
        burden = (annual_tco / annual_income) * 100
        st.markdown(f"**OWNERSHIP BURDEN**: {burden:.1f}% of annual income.")
        if burden > 20:
            st.warning("High burden! Recommended burden is under 20%.")
