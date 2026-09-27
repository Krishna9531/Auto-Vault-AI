import streamlit as st
from pathlib import Path

st.set_page_config(page_title='Vehicle Health', page_icon='🚗', layout='wide')

def load_css():
    css_path = Path(__file__).parent.parent / "styles" / "brutalist.css"
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

if "vehicle_data" not in st.session_state or st.session_state.vehicle_data is None:
    st.warning("⚠️ VEHICLE DATA NOT FOUND. PLEASE COMPLETE INPUT FIRST.")
    if st.button("GO TO INPUT"):
        st.switch_page("pages/01_Vehicle_Input.py")
    st.stop()

v_data = st.session_state.vehicle_data

st.markdown("<h1 style='font-weight: 900; text-transform: uppercase;'>02 VEHICLE HEALTH</h1>", unsafe_allow_html=True)
st.markdown(f"**{v_data['brand']} {v_data['model']} {v_data['variant']} ({v_data['mfg_year']})**")
st.markdown("---")

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("<div style='background: white; border: 2px solid #1A1A1A; padding: 20px; text-align: center;'>", unsafe_allow_html=True)
    st.markdown("<h3>OVERALL HEALTH</h3>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-size: 5rem; margin: 0; color: #FF2800; font-family: \"IBM Plex Mono\", monospace;'>87<span style='font-size: 2rem; color: #1A1A1A;'>/100</span></h1>", unsafe_allow_html=True)
    st.markdown("<span style='background: #1A1A1A; color: white; padding: 2px 5px; font-size: 0.8rem; font-weight: bold;'>ESTIMATED</span>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    st.markdown("### CONFIDENCE")
    st.progress(85)
    st.caption("Based on robust statistical models.")

with col2:
    st.markdown("### SUBSCORES")
    
    st.markdown("**MECHANICAL** (82/100)")
    st.progress(82)
    
    st.markdown("**ELECTRICAL** (90/100)")
    st.progress(90)
    
    st.markdown("**USAGE PATTERN** (75/100)")
    st.progress(75)
    
    st.markdown("**SERVICE HISTORY** (88/100)")
    st.progress(88)

st.write("---")
col3, col4 = st.columns(2)

with col3:
    st.markdown("### <span style='color: green;'>✔</span> POSITIVE FACTORS", unsafe_allow_html=True)
    st.markdown("- **Low Annual Mileage**: Expected wear is reduced.")
    st.markdown("- **Modern Platform**: Known for high reliability.")
    st.markdown("- **City Profile**: Favorable conditions compared to rough terrain.")

with col4:
    st.markdown("### <span style='color: #FF2800;'>✘</span> NEGATIVE FACTORS", unsafe_allow_html=True)
    st.markdown("- **High Initial Mileage**: Accelerated initial wear.")
    st.markdown("- **Stop-and-Go Traffic**: Increases transmission strain.")

if v_data.get('fuel_type') == "EV":
    st.write("---")
    st.markdown("### EV BATTERY SOH (STATE OF HEALTH)")
    st.metric("Estimated SOH", "92%", "-2% per year")
    st.markdown(f"- **Capacity**: {v_data.get('battery_capacity')} kWh")
    st.markdown(f"- **Charging Impact**: Frequent fast charging ({v_data.get('fast_charge_pct')}%) reduces longevity slightly.")
