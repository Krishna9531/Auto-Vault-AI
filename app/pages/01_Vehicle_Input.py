import streamlit as st
from pathlib import Path

st.set_page_config(page_title='Vehicle Input', page_icon='🚗', layout='wide')

def load_css():
    css_path = Path(__file__).parent.parent / "styles" / "brutalist.css"
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

st.markdown("<h1 style='font-weight: 900; text-transform: uppercase;'>01 VEHICLE INPUT</h1>", unsafe_allow_html=True)
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### BASIC DETAILS")
    brands = ["Maruti Suzuki", "Hyundai", "Tata", "Mahindra", "Kia", "Toyota", "Honda", "Renault", "Skoda", "Volkswagen", "MG", "Nissan", "Jeep", "Citroen", "Ford", "Chevrolet", "Fiat", "Datsun", "Audi", "BMW", "Mercedes-Benz"]
    brand = st.selectbox("BRAND", brands)
    model = st.selectbox("MODEL", [f"{brand} Model A", f"{brand} Model B", f"{brand} Model C"])
    variant = st.text_input("VARIANT", "Top Spec")
    fuel_type = st.radio("FUEL TYPE", ["Petrol", "Diesel", "CNG", "EV"])
    purchase_price = st.slider("PURCHASE PRICE (₹ LAKHS)", 1.0, 80.0, 10.0, 0.1)
    mfg_year = st.selectbox("MANUFACTURING YEAR", list(range(2025, 2014, -1)))

with col2:
    st.markdown("### USAGE & FINANCING")
    current_mileage = st.number_input("CURRENT MILEAGE (KM)", 0, 500000, 15000)
    annual_mileage = st.slider("EXPECTED ANNUAL MILEAGE (KM)", 5000, 50000, 12000, 1000)
    ownership_period = st.slider("PLANNED OWNERSHIP PERIOD (YEARS)", 1, 10, 5, 1)
    city = st.selectbox("PRIMARY USAGE CITY", ["Delhi", "Mumbai", "Bangalore", "Chennai", "Hyderabad", "Pune", "Kolkata"])
    income = st.number_input("MONTHLY INCOME (₹, OPTIONAL FOR BURDEN CALC)", 0, 10000000, 100000, step=10000)

if fuel_type == "EV":
    st.markdown("### EV SPECIFICS")
    col_ev1, col_ev2, col_ev3 = st.columns(3)
    with col_ev1:
        battery_capacity = st.number_input("BATTERY CAPACITY (kWh)", 10.0, 150.0, 40.0)
    with col_ev2:
        charging_freq = st.selectbox("CHARGING FREQUENCY", ["Daily", "Every 2-3 Days", "Weekly", "Rarely"])
    with col_ev3:
        fast_charge_pct = st.slider("FAST CHARGING (%)", 0, 100, 20)
else:
    battery_capacity, charging_freq, fast_charge_pct = None, None, None

st.markdown("### FINANCING")
col_fin1, col_fin2, col_fin3 = st.columns(3)
with col_fin1:
    down_payment_pct = st.slider("DOWN PAYMENT (%)", 0, 100, 20)
with col_fin2:
    loan_rate = st.slider("LOAN RATE (%)", 5.0, 20.0, 9.0, 0.1)
with col_fin3:
    tenure_months = st.selectbox("LOAN TENURE (MONTHS)", [12, 24, 36, 48, 60, 72, 84], index=4)

if st.button("ANALYZE VEHICLE", use_container_width=True, type="primary"):
    st.session_state.vehicle_data = {
        "brand": brand,
        "model": model,
        "variant": variant,
        "fuel_type": fuel_type,
        "purchase_price": purchase_price,
        "mfg_year": mfg_year,
        "current_mileage": current_mileage,
        "annual_mileage": annual_mileage,
        "ownership_period": ownership_period,
        "city": city,
        "income": income,
        "battery_capacity": battery_capacity,
        "charging_freq": charging_freq,
        "fast_charge_pct": fast_charge_pct,
        "down_payment_pct": down_payment_pct,
        "loan_rate": loan_rate,
        "tenure_months": tenure_months
    }
    st.success("DATA SAVED. PROCEED TO HEALTH ANALYSIS.")
    st.switch_page("pages/02_Vehicle_Health.py")
