# -*- coding: utf-8 -*-
"""
05 TCO - AUTOVAULT AI
Computes full Total Cost of Ownership using EMI, fuel, maintenance, insurance, and resale.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
import plotly.graph_objects as go
import datetime

st.set_page_config(page_title="TCO | AUTOVAULT AI", page_icon="🚗", layout="wide")

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
.card { background: white; border: 2px solid #1A1A1A; padding: 24px; margin-bottom: 16px; text-align:center; }
.big-num { font-family: 'IBM Plex Mono', monospace; font-size: 2.8rem; font-weight: 700; color: #1A1A1A; line-height: 1.1; }
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

# ── TCO Engine ────────────────────────────────────────────────────────────────
def compute_tco(v, period):
    price    = v.get("purchase_price", 10.0)   # lakhs
    fuel     = v.get("fuel_type", "Petrol")
    annual_km= v.get("annual_mileage", 12000)
    loan_pct = (100 - v.get("down_payment_pct", 20)) / 100
    rate     = v.get("loan_rate", 9.0)
    tenure   = v.get("tenure_months", 60)
    income   = v.get("income", 0)

    principal = price * loan_pct * 100000  # INR

    # EMI (reducing balance)
    if rate > 0 and tenure > 0:
        r = rate / (12 * 100)
        emi = principal * r * (1 + r)**tenure / ((1 + r)**tenure - 1)
        total_loan_paid = emi * tenure
        interest = total_loan_paid - principal
    else:
        emi = principal / tenure if tenure > 0 else 0
        interest = 0

    financing_cost = round(interest / 100000, 2)  # lakhs

    # Fuel / Energy
    if fuel == "EV":
        # avg 6 km/kWh, Rs.8/unit
        energy_cost_yr = (annual_km / 6) * 8 / 100000
    elif fuel == "Diesel":
        energy_cost_yr = (annual_km / 18) * 94 / 100000
    elif fuel == "CNG":
        energy_cost_yr = (annual_km / 25) * 80 / 100000
    else:  # Petrol
        energy_cost_yr = (annual_km / 17) * 106 / 100000
    fuel_total = round(energy_cost_yr * period, 2)

    # Maintenance
    BASE = {"Petrol": 14000, "Diesel": 16000, "EV": 7000, "Hybrid": 11000, "CNG": 15000}
    ann_maint = BASE.get(fuel, 14000)
    maint_total = round(ann_maint * period * (1 + 0.04 * period) / 100000, 2)

    # Insurance (approx 2.5% of current value Y1, reducing)
    ins_total = round(price * 0.025 * period * 0.85, 2)

    # Tyres (~Rs.25,000 per set, 1 set per 40k km)
    sets = max(1, int(annual_km * period / 40000))
    tyres_total = round(sets * 25000 / 100000, 2)

    # Depreciation / Resale
    DEPR = {"Petrol": [0.15,0.12,0.10,0.09,0.08,0.07,0.07],
            "Diesel": [0.18,0.13,0.10,0.09,0.08,0.07,0.07],
            "EV":     [0.20,0.15,0.12,0.10,0.09,0.08,0.08],
            "Hybrid": [0.13,0.11,0.09,0.08,0.07,0.07,0.06],
            "CNG":    [0.16,0.12,0.10,0.09,0.08,0.07,0.07]}
    rates = DEPR.get(fuel, DEPR["Petrol"])
    val = price
    for y in range(period):
        val *= (1 - rates[min(y, len(rates)-1)])
    resale = round(val, 2)

    net_tco = round(price + fuel_total + maint_total + ins_total + tyres_total + financing_cost - resale, 2)
    annual   = round(net_tco / period, 2)
    monthly  = round(net_tco / (period * 12), 2)

    burden = 0
    if income > 0:
        ann_income_l = income * 12 / 100000
        burden = round(annual / ann_income_l * 100, 1)

    components = {
        "Purchase Price": price,
        "Fuel / Energy": fuel_total,
        "Maintenance": maint_total,
        "Insurance": ins_total,
        "Tyres": tyres_total,
        "Financing (Interest)": financing_cost,
        "Resale Value": -resale,
    }

    return {
        "price": price, "fuel_total": fuel_total, "maint_total": maint_total,
        "ins_total": ins_total, "tyres_total": tyres_total, "financing_cost": financing_cost,
        "resale": resale, "net_tco": net_tco, "annual": annual, "monthly": monthly,
        "burden": burden, "components": components, "emi_monthly": round(emi / 1000, 1)
    }

# ── UI ────────────────────────────────────────────────────────────────────────
st.markdown("<h1>05 — TOTAL COST OF OWNERSHIP</h1>", unsafe_allow_html=True)
st.markdown(f"**{v.get('brand','')} {v.get('model','')} &nbsp;|&nbsp; {v.get('fuel_type','')}**")
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

period = st.radio("SELECT OWNERSHIP PERIOD", [3, 5, 7, 10], index=1, horizontal=True)

tco = compute_tco(v, period)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""<div class="card">
        <p style="font-weight:700;letter-spacing:0.1em;margin:0;">{period}-YEAR NET TCO</p>
        <p class="big-num" style="color:#FF2800;">Rs.{tco['net_tco']:.1f}L</p>
        <span class="badge-est">ESTIMATED</span>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""<div class="card">
        <p style="font-weight:700;letter-spacing:0.1em;margin:0;">ANNUAL COST</p>
        <p class="big-num">Rs.{tco['annual']:.2f}L</p>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""<div class="card">
        <p style="font-weight:700;letter-spacing:0.1em;margin:0;">MONTHLY COST</p>
        <p class="big-num">Rs.{tco['monthly']:.2f}L</p>
    </div>""", unsafe_allow_html=True)
with c4:
    st.markdown(f"""<div class="card">
        <p style="font-weight:700;letter-spacing:0.1em;margin:0;">MONTHLY EMI</p>
        <p class="big-num">Rs.{tco['emi_monthly']:.1f}K</p>
    </div>""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
col4, col5 = st.columns(2)

with col4:
    st.markdown("### TCO WATERFALL")
    comps = tco["components"]
    measures = ["relative"] * (len(comps) - 1) + ["relative"]
    measures.append("total")
    labels  = list(comps.keys()) + ["NET TCO"]
    amounts = list(comps.values()) + [tco["net_tco"]]
    measures = ["relative"] * len(comps) + ["total"]

    fig = go.Figure(go.Waterfall(
        orientation="v",
        measure=measures,
        x=labels,
        y=amounts,
        text=[f"Rs.{abs(a):.2f}L" for a in amounts],
        textposition="outside",
        connector={"line": {"color": "#1A1A1A", "width": 1}},
        increasing={"marker": {"color": "#FF2800"}},
        decreasing={"marker": {"color": "#006400"}},
        totals={"marker": {"color": "#1A1A1A"}},
    ))
    fig.update_layout(
        plot_bgcolor='#F5F5F0', paper_bgcolor='#F5F5F0',
        xaxis=dict(tickangle=-30),
        yaxis=dict(title="Rs. Lakhs", gridcolor='#E0E0E0'),
        margin=dict(l=10, r=10, t=10, b=60), height=380
    )
    st.plotly_chart(fig, use_container_width=True)

with col5:
    st.markdown("### COST BREAKDOWN")
    for label, val in tco["components"].items():
        prefix = "-" if val < 0 else "+"
        color = "#006400" if val < 0 else "#1A1A1A"
        st.markdown(f"<span style='color:{color};font-weight:700;'>{prefix} {label}:</span> **Rs.{abs(val):.2f}L**", unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Year-wise breakdown table
    st.markdown("### YEAR-WISE SNAPSHOT")
    rows = []
    DEPR = {"Petrol": [0.15,0.12,0.10,0.09,0.08,0.07,0.07],
            "Diesel": [0.18,0.13,0.10,0.09,0.08,0.07,0.07],
            "EV": [0.20,0.15,0.12,0.10,0.09,0.08,0.08],
            "Hybrid": [0.13,0.11,0.09,0.08,0.07,0.07,0.06],
            "CNG":    [0.16,0.12,0.10,0.09,0.08,0.07,0.07]}
    rates = DEPR.get(v.get("fuel_type","Petrol"), DEPR["Petrol"])
    val = v.get("purchase_price", 10.0)
    for y in range(1, period + 1):
        val *= (1 - rates[min(y-1, len(rates)-1)])
        rows.append({
            "Year": y,
            "Running Cost (L)": f"Rs.{(tco['fuel_total']+tco['maint_total']+tco['ins_total'])/period:.2f}",
            "Vehicle Value (L)": f"Rs.{val:.2f}"
        })
    st.table(rows)

    if tco["burden"] > 0:
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        bcolor = "#FF2800" if tco["burden"] > 25 else "#FF8C00" if tco["burden"] > 15 else "#006400"
        st.markdown(f"### OWNERSHIP BURDEN")
        st.markdown(f"<span style='font-family:IBM Plex Mono,monospace;font-size:2rem;font-weight:700;color:{bcolor};'>{tco['burden']}%</span> of annual income", unsafe_allow_html=True)
        if tco["burden"] > 25:
            st.warning("High burden — recommended threshold is under 20% of annual income.")
        elif tco["burden"] > 15:
            st.info("Moderate burden — within acceptable range for most households.")
        else:
            st.success("Comfortable burden — well within recommended limits.")

st.caption("TCO uses rule-based calculations. Fuel prices: Petrol Rs.106/L, Diesel Rs.94/L, Electricity Rs.8/kWh, CNG Rs.80/kg. Adjust inputs for precision.")
