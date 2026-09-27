# -*- coding: utf-8 -*-
"""
03 Depreciation - AUTOVAULT AI
Computes year-by-year value using fuel-type depreciation curves + mileage adjustments.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Depreciation | AUTOVAULT AI", page_icon="🚗", layout="wide")

# Custom navigation
try:
    from app.components.navigation import build_sidebar
    build_sidebar()
except Exception as e:
    pass


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;700&family=Inter:wght@400;700;900&display=swap');
body, .stApp { background-color: #F5F5F0; font-family: 'Inter', system-ui, sans-serif; }
h1,h2,h3 { text-transform: uppercase; letter-spacing: 0.08em; font-weight: 900; }
.card { background: white; border: 2px solid #1A1A1A; padding: 24px; margin-bottom: 16px; }
.big-num { font-family: 'IBM Plex Mono', monospace; font-size: 3.5rem; font-weight: 700; color: #1A1A1A; line-height: 1; }
.badge-est { background:#1A1A1A; color:white; padding:2px 8px; font-size:0.7rem; font-weight:700; letter-spacing:0.1em; }
.divider { border-top: 3px solid #1A1A1A; margin: 20px 0; }
</style>
""", unsafe_allow_html=True)

if "vehicle_data" not in st.session_state or st.session_state.vehicle_data is None:
    st.error("NO VEHICLE DATA FOUND. PLEASE COMPLETE THE INPUT FORM FIRST.")
    if st.button("GO TO INPUT"):
        st.switch_page("pages/01_Vehicle_Input.py")
    st.stop()

v = st.session_state.vehicle_data

# ── Depreciation Engine ───────────────────────────────────────────────────────
DEPR_RATES = {
    "Petrol":  [0.15, 0.12, 0.10, 0.09, 0.08, 0.07, 0.07],
    "Diesel":  [0.18, 0.13, 0.10, 0.09, 0.08, 0.07, 0.07],
    "EV":      [0.20, 0.15, 0.12, 0.10, 0.09, 0.08, 0.08],
    "Hybrid":  [0.13, 0.11, 0.09, 0.08, 0.07, 0.07, 0.06],
    "CNG":     [0.16, 0.12, 0.10, 0.09, 0.08, 0.07, 0.07],
}
AVG_KM = {"Petrol": 12000, "Diesel": 15000, "EV": 12000, "Hybrid": 13000, "CNG": 14000}

price = v.get("purchase_price", 10.0)
fuel  = v.get("fuel_type", "Petrol")
annual_km = v.get("annual_mileage", 12000)
ownership = v.get("ownership_period", 5)
brand = v.get("brand", "")

rates = DEPR_RATES.get(fuel, DEPR_RATES["Petrol"])
avg   = AVG_KM.get(fuel, 12000)
excess_10k = max(0, (annual_km - avg) / 10000)
mileage_adj = excess_10k * 0.005  # 0.5% extra per 10k above avg

# Build yearly value table
values = [price]
for y in range(1, ownership + 1):
    r = rates[min(y - 1, len(rates) - 1)]
    total_rate = min(r + mileage_adj, 0.35)
    values.append(round(values[-1] * (1 - total_rate), 2))

years = list(range(ownership + 1))
resale = values[-1]
total_depr_pct = round((price - resale) / price * 100, 1)

# Confidence band (+/- 8%)
upper = [round(v * 1.08, 2) for v in values]
lower = [round(v * 0.92, 2) for v in values]

# SHAP-style factor importance (rule-based)
factors = {
    "Fuel Type Demand":   0.90 if fuel in ["Petrol", "Hybrid"] else 0.65,
    "Brand Reliability":  0.85 if brand in ["Maruti Suzuki", "Hyundai", "Toyota"] else 0.70,
    "Annual Mileage":     max(0.2, 1 - (annual_km / 50000)),
    "Market Segment":     0.75,
    "Ownership Period":   max(0.2, 1 - (ownership / 12)),
}

# ── UI ────────────────────────────────────────────────────────────────────────
st.markdown("<h1>03 — DEPRECIATION</h1>", unsafe_allow_html=True)
st.markdown(f"**{v.get('brand','')} {v.get('model','')} &nbsp;|&nbsp; {fuel} &nbsp;|&nbsp; {annual_km:,} km/yr planned**")
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown(f"""
    <div class="card" style="text-align:center;">
        <p style="font-weight:700;letter-spacing:0.1em;margin:0;">PURCHASE PRICE</p>
        <p class="big-num">Rs.{price:.1f}L</p>
        <span style="background:#FF2800;color:white;padding:2px 8px;font-size:0.7rem;font-weight:700;">VERIFIED</span>
    </div>
    <div class="card" style="text-align:center;">
        <p style="font-weight:700;letter-spacing:0.1em;margin:0;">EXPECTED RESALE ({ownership}Y)</p>
        <p class="big-num" style="color:#FF2800;">Rs.{resale:.1f}L</p>
        <p style="margin:4px 0;font-size:0.85rem;">Range: Rs.{lower[-1]:.1f}L &ndash; Rs.{upper[-1]:.1f}L</p>
        <span class="badge-est">ESTIMATED</span>
    </div>
    <div class="card" style="text-align:center;">
        <p style="font-weight:700;letter-spacing:0.1em;margin:0;">TOTAL DEPRECIATION</p>
        <p class="big-num" style="color:#FF2800;">{total_depr_pct}%</p>
        <span class="badge-est">ESTIMATED</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### YEAR-BY-YEAR")
    rows = []
    for i, val in enumerate(values):
        pct = round((price - val) / price * 100, 1) if i > 0 else 0
        rows.append({"Year": i, "Value (L)": f"Rs.{val:.2f}", "Depr.": f"-{pct}%" if i > 0 else "—"})
    st.table(rows)

with col2:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years, y=upper, fill=None, mode='lines',
        line=dict(color='rgba(200,200,200,0.3)', width=0), showlegend=False
    ))
    fig.add_trace(go.Scatter(
        x=years, y=lower, fill='tonexty', mode='lines',
        line=dict(color='rgba(200,200,200,0.3)', width=0),
        fillcolor='rgba(200,200,200,0.3)', name='Confidence Range'
    ))
    fig.add_trace(go.Scatter(
        x=years, y=values, mode='lines+markers',
        line=dict(color='#FF2800', width=4),
        marker=dict(size=10, color='#1A1A1A', symbol='circle'),
        name='Expected Value',
        text=[f"Rs.{v:.2f}L" for v in values],
        hovertemplate='Year %{x}<br>Value: %{text}<extra></extra>'
    ))
    fig.update_layout(
        plot_bgcolor='#F5F5F0', paper_bgcolor='#F5F5F0',
        xaxis=dict(title='Ownership Year', gridcolor='#E0E0E0', tickmode='linear'),
        yaxis=dict(title='Value (Rs. Lakhs)', gridcolor='#E0E0E0'),
        legend=dict(orientation='h', y=-0.2),
        margin=dict(l=10, r=10, t=10, b=10), height=360
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### KEY DEPRECIATION FACTORS")
    for factor, impact in sorted(factors.items(), key=lambda x: x[1], reverse=True):
        pct_int = int(impact * 100)
        st.markdown(f"**{factor}**")
        st.progress(pct_int / 100, text=f"{pct_int}% influence")

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Segment comparison
seg_avg_depr = {"Petrol": 52, "Diesel": 55, "EV": 58, "Hybrid": 48, "CNG": 53}
seg_avg = seg_avg_depr.get(fuel, 52)
diff = round(seg_avg - total_depr_pct, 1)
direction = "retains more" if diff > 0 else "depreciates faster than"
st.info(f"**SEGMENT COMPARISON**: This vehicle {direction} the segment average by {abs(diff)}% over {ownership} years. Segment average depreciation: {seg_avg}%.")
st.caption("Depreciation estimates use rule-based curves by fuel type + mileage adjustment. Actual resale depends on market conditions, demand, and vehicle condition.")
