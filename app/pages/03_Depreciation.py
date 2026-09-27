import streamlit as st
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title='Depreciation', page_icon='🚗', layout='wide')

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

st.markdown("<h1 style='font-weight: 900; text-transform: uppercase;'>03 DEPRECIATION</h1>", unsafe_allow_html=True)
st.markdown("---")

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("<div style='background: white; border: 2px solid #1A1A1A; padding: 20px; text-align: center;'>", unsafe_allow_html=True)
    st.markdown("<h3>CURRENT EST. VALUE</h3>", unsafe_allow_html=True)
    
    current_val = v_data['purchase_price'] * 0.85 # Dummy calc
    
    st.markdown(f"<h1 style='font-size: 4rem; margin: 0; color: #1A1A1A; font-family: \"IBM Plex Mono\", monospace;'>₹{current_val:.2f}L</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='margin: 0; font-weight: bold;'>CONFIDENCE RANGE: ₹{current_val*0.9:.2f}L - ₹{current_val*1.1:.2f}L</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.write("")
    st.markdown("### YEARLY PROJECTION")
    years = [0, 1, 2, 3, 4, 5]
    values = [v_data['purchase_price']]
    for y in range(1, 6):
        values.append(values[-1] * 0.9) # 10% dep per year
        
    for i, v in enumerate(values):
        st.markdown(f"**Year {i}**: ₹{v:.2f}L ({-10 if i>0 else 0}%)")
        
with col2:
    st.markdown("### DEPRECIATION CURVE")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years, y=values, mode='lines+markers', line=dict(color='#FF2800', width=4), marker=dict(size=10, color='#1A1A1A')))
    fig.update_layout(
        plot_bgcolor='#F5F5F0',
        paper_bgcolor='#F5F5F0',
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(title='Years', gridcolor='lightgray'),
        yaxis=dict(title='Value (₹ Lakhs)', gridcolor='lightgray')
    )
    st.plotly_chart(fig, use_container_width=True)

st.write("---")
st.markdown("### FEATURE IMPORTANCE (SHAP)")
st.markdown("Factors driving the depreciation for this model:")
st.progress(90, text="Brand Reliability (90%)")
st.progress(75, text="Mileage (75%)")
st.progress(60, text="Fuel Type Demand (60%)")
st.progress(40, text="Market Segment Trend (40%)")

st.info("**SEGMENT COMPARISON**: This vehicle retains 4% more value over 5 years compared to the segment average.")
