# -*- coding: utf-8 -*-
"""
07 Simulator - AUTOVAULT AI
What-if scenario simulator — live recalculation of TCO on slider changes.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Simulator | AUTOVAULT AI", page_icon="🚗", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;700&family=Inter:wght@400;700;900&display=swap');
body, .stApp { background-color: #F5F5F0; font-family: 'Inter', system-ui, sans-serif; }
h1,h2,h3 { text-transform: uppercase; letter-spacing: 0.08em; font-weight: 900; }
.card { background: white; border: 2px solid #1A1A1A; padding: 20px; margin-bottom: 12px; text-align:center; }
.big-num { font-family: 'IBM Plex Mono', monospace; font-size: 2.4rem; font-weight: 700; color: #1A1A1A; line-height: 1.1; }
.divider { border-top: 3px solid #1A1A1A; margin: 20px 0; }
.badge-sim { background:#FF2800; color:white; padding:2px 8px; font-size:0.7rem; font-weight:700; letter-spacing:0.1em; }
</style>
""", unsafe_allow_html=True)

if "vehicle_data" not in st.session_state or st.session_state.vehicle_data is None:
    st.error("NO VEHICLE DATA FOUND. PLEASE COMPLETE THE INPUT FORM FIRST.")
    if st.button("GO TO INPUT"):
        st.switch_page("pages/01_Vehicle_Input.py")
    st.stop()

v = st.session_state.vehicle_data

# ── Simulation Engine ─────────────────────────────────────────────────────────
def simulate(v, years, annual_km, fuel_mult, resale_opt):
    price = v.get("purchase_price", 10.0)
    fuel  = v.get("fuel_type", "Petrol")

    DEPR = {"Petrol": [0.15,0.12,0.10,0.09,0.08,0.07,0.07],
            "Diesel": [0.18,0.13,0.10,0.09,0.08,0.07,0.07],
            "EV":     [0.20,0.15,0.12,0.10,0.09,0.08,0.08],
            "Hybrid": [0.13,0.11,0.09,0.08,0.07,0.07,0.06],
            "CNG":    [0.16,0.12,0.10,0.09,0.08,0.07,0.07]}
    rates = DEPR.get(fuel, DEPR["Petrol"])

    BASE_M = {"Petrol": 0.14, "Diesel": 0.16, "EV": 0.07, "Hybrid": 0.11, "CNG": 0.15}
    base_annual_maint = BASE_M.get(fuel, 0.14)

    # Fuel cost per year
    if fuel == "EV":
        fuel_yr = (annual_km / 6) * 8 * fuel_mult / 100000
    elif fuel == "Diesel":
        fuel_yr = (annual_km / 18) * 94 * fuel_mult / 100000
    elif fuel == "CNG":
        fuel_yr = (annual_km / 25) * 80 * fuel_mult / 100000
    else:
        fuel_yr = (annual_km / 17) * 106 * fuel_mult / 100000

    # Maintenance scales with km
    km_factor = annual_km / 12000
    maint_yr  = base_annual_maint * km_factor

    # Insurance
    ins_yr = price * 0.025 * 0.85

    # Depreciation
    val = price
    for y in range(years):
        val *= (1 - rates[min(y, len(rates)-1)])
    resale = round(val * resale_opt, 2)

    total_fuel  = round(fuel_yr * years, 2)
    total_maint = round(maint_yr * years * (1 + 0.04 * years/2), 2)
    total_ins   = round(ins_yr * years, 2)
    net_tco     = round(price + total_fuel + total_maint + total_ins - resale, 2)

    # Year-by-year cumulative TCO
    val_curve, cum_tco = [price], [0]
    val2 = price
    cum = 0
    for y in range(1, years + 1):
        val2 *= (1 - rates[min(y-1, len(rates)-1)])
        cum  += fuel_yr + maint_yr + ins_yr
        val_curve.append(round(val2, 2))
        cum_tco.append(round(cum, 2))

    return {
        "net_tco": net_tco, "fuel": total_fuel, "maint": total_maint,
        "ins": total_ins, "resale": resale, "val_curve": val_curve,
        "cum_tco": cum_tco, "annual": round(net_tco / years, 2)
    }

# ── Base values from vehicle input ────────────────────────────────────────────
base_years = v.get("ownership_period", 5)
base_km    = v.get("annual_mileage", 12000)
fuel       = v.get("fuel_type", "Petrol")

# ── UI ────────────────────────────────────────────────────────────────────────
st.markdown("<h1>07 — WHAT-IF SIMULATOR</h1>", unsafe_allow_html=True)
st.markdown(f"**{v.get('brand','')} {v.get('model','')} &nbsp;|&nbsp; {fuel}** &nbsp; — &nbsp; Adjust sliders to see live TCO impact")
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

col_sliders, col_results = st.columns([1, 2])

with col_sliders:
    st.markdown("### SCENARIO VARIABLES")

    if st.button("RESET TO BASE", use_container_width=True):
        for k in ["sim_years","sim_km","sim_fuel","sim_resale"]:
            if k in st.session_state:
                del st.session_state[k]
        st.rerun()

    years   = st.slider("OWNERSHIP YEARS", 1, 15, st.session_state.get("sim_years", base_years), key="sim_years")
    km      = st.slider("ANNUAL KM", 3000, 60000, st.session_state.get("sim_km", base_km), step=1000, key="sim_km")
    f_mult  = st.slider("FUEL PRICE MULTIPLIER", 0.7, 2.0, st.session_state.get("sim_fuel", 1.0), step=0.05, key="sim_fuel",
                        help="1.0 = current price. 1.2 = 20% higher, etc.")
    r_opt   = st.slider("RESALE OPTIMISM", 0.7, 1.3, st.session_state.get("sim_resale", 1.0), step=0.05, key="sim_resale",
                        help="1.0 = base estimate. 1.2 = 20% better resale, 0.8 = 20% worse.")

    # Labels
    fuel_label   = f"+{int((f_mult-1)*100)}%" if f_mult >= 1 else f"{int((f_mult-1)*100)}%"
    resale_label = "Optimistic" if r_opt > 1.05 else "Conservative" if r_opt < 0.95 else "Base"
    st.markdown(f"""
    <div style="background:white;border:2px solid #1A1A1A;padding:16px;margin-top:12px;">
        <p style="margin:0;font-size:0.85rem;"><b>Fuel adjustment:</b> {fuel_label}</p>
        <p style="margin:0;font-size:0.85rem;"><b>Annual distance:</b> {km:,} km/yr</p>
        <p style="margin:0;font-size:0.85rem;"><b>Resale scenario:</b> {resale_label}</p>
        <p style="margin:0;font-size:0.85rem;"><b>Ownership:</b> {years} years</p>
    </div>
    """, unsafe_allow_html=True)

# Compute base and simulated scenarios
base = simulate(v, years, base_km, 1.0, 1.0)
sim  = simulate(v, years, km, f_mult, r_opt)

with col_results:
    # Headline comparison
    delta = round(sim["net_tco"] - base["net_tco"], 2)
    delta_color = "#FF2800" if delta > 0 else "#006400"
    delta_sign  = "+" if delta > 0 else ""

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class="card">
            <p style="font-weight:700;letter-spacing:0.1em;margin:0;">BASE TCO ({years}Y)</p>
            <p class="big-num">Rs.{base['net_tco']:.1f}L</p>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="card">
            <p style="font-weight:700;letter-spacing:0.1em;margin:0;">SIMULATED TCO</p>
            <p class="big-num" style="color:#FF2800;">Rs.{sim['net_tco']:.1f}L</p>
            <span class="badge-sim">SCENARIO</span>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="card">
            <p style="font-weight:700;letter-spacing:0.1em;margin:0;">DIFFERENCE</p>
            <p class="big-num" style="color:{delta_color};">{delta_sign}Rs.{abs(delta):.1f}L</p>
        </div>""", unsafe_allow_html=True)

    # Chart — cumulative TCO over years
    yrs_axis = list(range(years + 1))
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=yrs_axis, y=base["cum_tco"], mode='lines', name='Base Running Cost',
        line=dict(color='#1A1A1A', width=2, dash='dash')
    ))
    fig.add_trace(go.Scatter(
        x=yrs_axis, y=sim["cum_tco"], mode='lines+markers', name='Simulated Running Cost',
        line=dict(color='#FF2800', width=3), marker=dict(size=7, color='#FF2800')
    ))
    fig.add_trace(go.Scatter(
        x=yrs_axis, y=base["val_curve"], mode='lines', name='Vehicle Value',
        line=dict(color='#888', width=2, dash='dot')
    ))
    fig.update_layout(
        plot_bgcolor='#F5F5F0', paper_bgcolor='#F5F5F0',
        xaxis=dict(title='Year', gridcolor='#E0E0E0', tickmode='linear'),
        yaxis=dict(title='Rs. Lakhs', gridcolor='#E0E0E0'),
        legend=dict(orientation='h', y=-0.25),
        margin=dict(l=10, r=10, t=10, b=50), height=340
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown("### 3 / 5 / 7 YEAR COMPARISON")
cs1, cs2, cs3 = st.columns(3)

for col, yr in zip([cs1, cs2, cs3], [3, 5, 7]):
    s = simulate(v, yr, km, f_mult, r_opt)
    with col:
        st.markdown(f"""<div class="card">
            <p style="font-weight:900;letter-spacing:0.1em;margin:0 0 10px 0;">{yr}-YEAR</p>
            <p style="margin:2px 0;font-size:0.85rem;"><b>Net TCO:</b> Rs.{s['net_tco']:.1f}L</p>
            <p style="margin:2px 0;font-size:0.85rem;"><b>Fuel/Energy:</b> Rs.{s['fuel']:.2f}L</p>
            <p style="margin:2px 0;font-size:0.85rem;"><b>Maintenance:</b> Rs.{s['maint']:.2f}L</p>
            <p style="margin:2px 0;font-size:0.85rem;"><b>Insurance:</b> Rs.{s['ins']:.2f}L</p>
            <p style="margin:2px 0;font-size:0.85rem;"><b>Expected Resale:</b> Rs.{s['resale']:.1f}L</p>
            <p style="margin:6px 0 0 0;font-size:0.85rem;"><b>Annual Cost:</b> Rs.{s['annual']:.2f}L</p>
        </div>""", unsafe_allow_html=True)

# What-if text
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown("### WHAT-IF SUMMARY")
lines = []
if abs(f_mult - 1.0) > 0.05:
    impact = round((sim["fuel"] - base["fuel"]) * 100000)
    lines.append(f"A **{fuel_label}** fuel price change adds **Rs.{abs(impact):,}** to your {years}-year energy cost.")
if km != base_km:
    diff = km - base_km
    lines.append(f"Driving **{abs(diff):,} km {'more' if diff>0 else 'less'} per year** changes your TCO by **Rs.{abs(delta):.1f}L** over {years} years.")
if abs(r_opt - 1.0) > 0.05:
    lines.append(f"A **{resale_label.lower()}** resale market changes your final resale value to **Rs.{sim['resale']:.1f}L**.")
if not lines:
    lines.append("Adjust the sliders above to see how different scenarios affect your total cost of ownership.")

for line in lines:
    st.markdown(f"- {line}")

st.caption("Simulator uses rule-based calculations. Results are illustrative estimates, not financial guarantees.")
