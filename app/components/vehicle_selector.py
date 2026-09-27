"""Vehicle selector component."""

import streamlit as st
from app.utils.constants import BRAND_LIST, MODEL_DATA, FUEL_TYPES

def render_vehicle_selector() -> dict:
    st.markdown("""<div style="border: 3px solid #000; padding: 1.5rem; background: #FFF; margin-bottom: 2rem;">
        <h3 style="margin-top:0; text-transform:uppercase;">Vehicle Specifications</h3>""", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        brand = st.selectbox("BRAND", BRAND_LIST)
        models = MODEL_DATA.get(brand, ["Standard"])
        model = st.selectbox("MODEL", models)
        year = st.number_input("MANUFACTURE YEAR", min_value=1990, max_value=2026, value=2021)
    
    with col2:
        fuel = st.selectbox("FUEL TYPE", FUEL_TYPES)
        variant = st.text_input("VARIANT (Optional)", value="Standard")
        mileage = st.number_input("CURRENT MILEAGE (KM)", min_value=0, value=30000, step=1000)
        
    price = st.number_input("PURCHASE PRICE (₹)", min_value=10000, value=500000, step=10000)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    return {
        "brand": brand,
        "model": model,
        "variant": variant,
        "fuel_type": fuel,
        "year": year,
        "mileage_km": mileage,
        "purchase_price": price
    }
