# -*- coding: utf-8 -*-
"""
06 Financial Risk - AUTOVAULT AI
Computes financial exposure scores, break-even year, and risk radar from vehicle inputs.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
import plotly.graph_objects as go
import datetime

st.set_page_config(page_title="Financial Risk | AUTOVAULT AI", page_icon="🚗", layout="wide")

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
.big-num { font-family: 'IBM Plex Mono', monospace; font-size: 3rem; font-weight: 700; color: #1A1A1A; line-height: 1.1; }
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

# ── Risk Engine ───────────────────────────────────────────────────────────────
price      = v.get("purchase_price", 10.0)
fuel       = v.get("fuel_type", "Petrol")
annual_km  = v.get("annual_mileage", 12000)
ownership  = v.get("ownership_period", 5)
loan_pct   = (100 - v.get("down_payment_pct", 20)) / 100
rate       = v.get("loan_rate", 9.0)
tenure     = v.get("tenure_months", 60)
income     = v.get("income", 0)
age        = datetime.datetime.now().year - v.get("mfg_year", datetime.datetime.now().year)

# Purchase Risk: how much of the vehicle is financed
purchase_risk = round(min(90, loan_pct * 70 + (rate / 20) * 20))

# Running Cost Risk: fuel volatility + annual km
FUEL_VOLATILE = {"Petrol": 55, "Diesel": 50, "EV": 20, "Hybrid": 35, "CNG": 45}
running_risk  = round(min(90, FUEL_VOLATILE.get(fuel, 50) + min(20, annual_km / 2000)))

# Maintenance Risk
BASE = {"Petrol": 40, "Diesel": 45, "EV": 20, "Hybrid": 30, "CNG": 40}
maint_risk = round(min(90, BASE.get(fuel, 40) + age * 4 + min(15, annual_km / 3000)))

# Resale Risk: EV/Diesel depreciates faster
RESALE_BASE = {"Petrol": 35, "Diesel": 45, "EV": 50, "Hybrid": 30, "CNG": 40}
resale_risk  = round(min(90, RESALE_BASE.get(fuel, 35) + ownership * 2))

# Financing Risk
if tenure == 0:
    financing_risk = 0
else:
    financing_risk = round(min(90, (rate / 15) * 40 + (tenure / 84) * 30 + loan_pct * 20))

# Overall weighted risk
overall_risk = round(
    purchase_risk * 0.15 +
    running_risk  * 0.25 +
    maint_risk    * 0.20 +
    resale_risk   * 0.25 +
    financing_risk* 0.15
)

risk_label = "LOW" if overall_risk < 30 else "MEDIUM" if overall_risk < 60 else "HIGH"
risk_color = "#006400" if overall_risk < 30 else "#FF8C00" if overall_risk < 60 else "#FF2800"

# Break-even year: when total running cost = resale value recovered
# Simplified: year when cumulative cost stops growing faster than depreciation
DEPR = {"Petrol": [0.15,0.12,0.10,0.09,0.08], "Diesel": [0.18,0.13,0.10,0.09,0.08],
        "EV": [0.20,0.15,0.12,0.10,0.09], "Hybrid": [0.13,0.11,0.09,0.08,0.07],
        "CNG": [0.16,0.12,0.10,0.09,0.08]}
rates = DEPR.get(fuel, DEPR["Petrol"])

ENERGY = {"Petrol": (106, 17), "Diesel": (94, 18), "EV": (8, 0), "Hybrid": (106, 27), "CNG": (80, 25)}
ep, eff = ENERGY.get(fuel, (106, 17))
annual_energy = (annual_km / eff * ep / 100000) if fuel != "EV" else (annual_km / 6 * 8 / 100000)
BASE_M = {"Petrol": 0.14, "Diesel": 0.16, "EV": 0.07, "Hybrid": 0.11, "CNG": 0.15}
annual_running = annual_energy + BASE_M.get(fuel, 0.14)

val = price
cumulative_cost = 0
break_even = ownership
for y in range(1, 11):
    val *= (1 - rates[min(y-1, len(rates)-1)])
    cumulative_cost += annual_running
    if cumulative_cost >= (price - val) * 0.5:
        break_even = y
        break

# Risk explanations
insights = []
if financing_risk > 50:
    insights.append(f"**Financing Risk**: High loan-to-value ratio ({int(loan_pct*100)}%) increases financial exposure.")
if running_risk > 50:
    insights.append(f"**Running Cost Risk**: {fuel} fuel price volatility adds uncertainty to long-term costs.")
if resale_risk > 50:
    insights.append(f"**Resale Risk**: {fuel} vehicles face higher depreciation in current market conditions.")
if maint_risk > 50:
    insights.append(f"**Maintenance Risk**: Age and mileage profile suggests elevated repair probability.")
if overall_risk < 35:
    insights.append("**Overall**: Vehicle presents a low financial risk profile for the given ownership period.")

# ── UI ────────────────────────────────────────────────────────────────────────
st.markdown("<h1>06 — FINANCIAL RISK</h1>", unsafe_allow_html=True)
st.caption("Model-based financial exposure score — not a guarantee of future costs.")
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown(f"""<div class="card">
        <p style="font-weight:700;letter-spacing:0.1em;margin:0;">OVERALL RISK SCORE</p>
        <p class="big-num" style="font-size:4rem;color:{risk_color};">{overall_risk}<span style="font-size:1.5rem;">/100</span></p>
        <p style="font-weight:900;letter-spacing:0.15em;color:{risk_color};">{risk_label} RISK</p>
        <span class="badge-est">ESTIMATED</span>
    </div>""", unsafe_allow_html=True)

    st.markdown("### RISK DIMENSIONS")
    dims = {
        "Purchase Risk":    purchase_risk,
        "Running Cost":     running_risk,
        "Maintenance":      maint_risk,
        "Resale Risk":      resale_risk,
        "Financing Risk":   financing_risk,
    }
    for dim, score in dims.items():
        color = "#FF2800" if score > 60 else "#FF8C00" if score > 35 else "#006400"
        st.markdown(f"**{dim}**: <span style='color:{color};font-family:IBM Plex Mono,monospace;font-weight:700;'>{score}</span>", unsafe_allow_html=True)
        st.progress(score / 100)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("### BREAK-EVEN YEAR")
    st.markdown(f"<p class='big-num' style='color:#FF2800;'>YEAR {break_even}</p>", unsafe_allow_html=True)
    st.caption("Estimated year where cumulative running cost equals 50% of depreciation recovered.")

with col2:
    # Radar chart
    dim_values = list(dims.values())
    dim_labels = list(dims.keys())
    fig = go.Figure(data=go.Scatterpolar(
        r=dim_values + [dim_values[0]],
        theta=dim_labels + [dim_labels[0]],
        fill='toself',
        fillcolor='rgba(255, 40, 0, 0.15)',
        line=dict(color='#FF2800', width=2),
        name='Risk Profile'
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=10)),
            angularaxis=dict(tickfont=dict(size=11, family='Inter'))
        ),
        showlegend=False,
        plot_bgcolor='#F5F5F0', paper_bgcolor='#F5F5F0',
        margin=dict(l=40, r=40, t=40, b=40), height=380
    )
    st.plotly_chart(fig, use_container_width=True)

    # Year-by-year cumulative cost vs resale
    st.markdown("### CUMULATIVE COST vs. VEHICLE VALUE")
    cum_costs, vehicle_vals = [0], [price]
    val = price
    cum = 0
    for y in range(1, ownership + 1):
        val *= (1 - rates[min(y-1, len(rates)-1)])
        cum += annual_running
        cum_costs.append(round(cum, 2))
        vehicle_vals.append(round(val, 2))

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=list(range(ownership + 1)), y=vehicle_vals, mode='lines+markers',
        name='Vehicle Value', line=dict(color='#1A1A1A', width=3),
        marker=dict(size=8)
    ))
    fig2.add_trace(go.Scatter(
        x=list(range(ownership + 1)), y=cum_costs, mode='lines+markers',
        name='Cumulative Running Cost', line=dict(color='#FF2800', width=3, dash='dash'),
        marker=dict(size=8, symbol='diamond')
    ))
    fig2.update_layout(
        plot_bgcolor='#F5F5F0', paper_bgcolor='#F5F5F0',
        xaxis=dict(title='Year', gridcolor='#E0E0E0', tickmode='linear'),
        yaxis=dict(title='Rs. Lakhs', gridcolor='#E0E0E0'),
        legend=dict(orientation='h', y=-0.2),
        margin=dict(l=10, r=10, t=10, b=40), height=300
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown("### RISK INSIGHTS")
for insight in insights:
    st.markdown(f"- {insight}")

st.caption("Risk scores are model-based financial exposure estimates. They do not constitute financial advice. Actual costs depend on market conditions, maintenance decisions, and usage.")
