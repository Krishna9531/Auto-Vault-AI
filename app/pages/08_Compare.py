import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title='Compare', page_icon='🚗', layout='wide')

# Custom navigation
try:
    from app.components.navigation import build_sidebar
    build_sidebar()

if "vehicle_data" not in st.session_state or not st.session_state.vehicle_data:
    st.markdown("<div style='text-align:center; padding: 60px 20px;'><h2 style='color:#FF2800; font-weight:900;'>VEHICLE REQUIRED</h2><p style='color:#555; font-size:1.1rem; margin-bottom: 30px;'>Please configure a vehicle first to view this analysis module.</p></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("← GO TO VEHICLE INPUT", use_container_width=True, type="primary"):
            st.switch_page("pages/01_Vehicle_Input.py")
    st.stop()

except Exception as e:
    pass


def load_css():
    css_path = Path(__file__).parent.parent / "styles" / "brutalist.css"
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

st.markdown("<h1 style='font-weight: 900; text-transform: uppercase;'>08 COMPARE</h1>", unsafe_allow_html=True)
st.markdown("---")

col1, col2, col3 = st.columns(3)

if 'compare_list' not in st.session_state:
    st.session_state.compare_list = []

def add_vehicle(col_idx):
    with st.expander(f"Add Vehicle {col_idx+1}", expanded=True):
        brand = st.selectbox(f"Brand {col_idx+1}", ["Hyundai", "Tata", "Maruti"])
        price = st.number_input(f"Price (Lakhs) {col_idx+1}", 5.0, 50.0, 10.0)
        fuel = st.selectbox(f"Fuel {col_idx+1}", ["Petrol", "Diesel", "EV"])
        if st.button(f"ADD V{col_idx+1}"):
            st.session_state.compare_list.append({"Brand": brand, "Price": price, "Fuel": fuel})
            st.rerun()

with col1:
    if len(st.session_state.compare_list) < 1: add_vehicle(0)
    else: st.markdown(f"### {st.session_state.compare_list[0]['Brand']} ({st.session_state.compare_list[0]['Fuel']})")

with col2:
    if len(st.session_state.compare_list) < 2: add_vehicle(1)
    else: st.markdown(f"### {st.session_state.compare_list[1]['Brand']} ({st.session_state.compare_list[1]['Fuel']})")

with col3:
    if len(st.session_state.compare_list) < 3: add_vehicle(2)
    else: st.markdown(f"### {st.session_state.compare_list[2]['Brand']} ({st.session_state.compare_list[2]['Fuel']})")

st.write("---")

if len(st.session_state.compare_list) > 0:
    st.markdown("### COMPARISON MATRIX")
    
    # Generate dummy data for comparison
    data = []
    for v in st.session_state.compare_list:
        data.append({
            "Vehicle": f"{v['Brand']} {v['Fuel']}",
            "Purchase Price (L)": v['Price'],
            "5Y TCO (L)": v['Price'] * 1.5,
            "Resale Value (L)": v['Price'] * 0.4,
            "Maintenance (L)": 0.5,
            "Energy Cost (L)": 2.0 if v['Fuel'] != 'EV' else 0.5,
            "Risk Score": "Low" if v['Fuel'] != 'EV' else "Medium"
        })
    
    df = pd.DataFrame(data).set_index("Vehicle").T
    
    # Apply simple highlighting styling using pandas Styler
    def highlight_min_max(s):
        if s.dtype == 'object': return [''] * len(s)
        is_max = s == s.max()
        is_min = s == s.min()
        return ['background-color: #d4edda; color: black' if v else 'background-color: #f8d7da; color: black' if m else '' for v, m in zip(is_min, is_max)]
    
    st.dataframe(df.style.apply(highlight_min_max, axis=1), use_container_width=True)
    
    st.markdown("### SUMMARY")
    st.info("**Models differ primarily in their long-term running costs and depreciation curves.**")
    
    if st.button("CLEAR COMPARISON"):
        st.session_state.compare_list = []
        st.rerun()
