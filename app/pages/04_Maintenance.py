# -*- coding: utf-8 -*-
"""
04 Maintenance - AUTOVAULT AI
Predicts maintenance events, annual cost, and risk score from vehicle inputs.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
import plotly.graph_objects as go
import datetime

st.set_page_config(page_title="Maintenance | AUTOVAULT AI", page_icon="🚗", layout="wide")

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

# ── Maintenance Engine ────────────────────────────────────────────────────────
current_year = datetime.datetime.now().year
age = current_year - v.get("mfg_year", current_year)
mileage = v.get("current_mileage", 0)
annual_km = v.get("annual_mileage", 12000)
fuel = v.get("fuel_type", "Petrol")
ownership = v.get("ownership_period", 5)

# Base annual costs by fuel type (INR)
BASE_ANNUAL = {"Petrol": 14000, "Diesel": 16000, "EV": 7000, "Hybrid": 11000, "CNG": 15000}
base_cost = BASE_ANNUAL.get(fuel, 14000)

# Age multiplier
age_mult = 1.0 + max(0, (age - 2) * 0.12)
# Mileage multiplier
km_mult  = 1.0 + max(0, (annual_km - 12000) / 12000) * 0.20

annual_cost = round(base_cost * age_mult * km_mult)
total_5y    = round(annual_cost * ownership * (1 + 0.05 * (ownership / 2)))  # costs rise with age

# Next service (every 10k km for ICE, 15k for EV)
svc_interval = 15000 if fuel == "EV" else 10000
next_service  = (mileage // svc_interval + 1) * svc_interval
km_to_service = next_service - mileage
months_to_svc = round(km_to_service / (annual_km / 12)) if annual_km > 0 else 12

# Risk score
risk_score = min(95, int(
    (age * 6) +
    (mileage / 10000) * 2 +
    (annual_km / 5000) * 3 +
    (0 if fuel == "EV" else 5)
))
risk_label = "LOW" if risk_score < 30 else "MEDIUM" if risk_score < 60 else "HIGH"
risk_color = "#006400" if risk_score < 30 else "#FF8C00" if risk_score < 60 else "#FF2800"

# Event probabilities (0-1)
events = {
    "Oil / Filter Change":    0.95 if fuel != "EV" else 0.0,
    "Brake Service":          min(0.95, 0.20 + age * 0.08 + annual_km / 100000),
    "Tyre Replacement":       min(0.90, 0.10 + annual_km / 50000 + age * 0.05),
    "AC Service":             min(0.80, 0.15 + age * 0.10),
    "Battery Service":        0.30 if fuel == "EV" and age > 3 else 0.05,
    "Major Service (40k km)": min(0.75, mileage / 80000),
}

# Cost breakdown
sched_cost  = round(annual_cost * 0.55 * ownership)
wear_cost   = round(annual_cost * 0.30 * ownership)
repair_cost = round(annual_cost * 0.15 * ownership)

# Risk explanations
explanations = []
if age > 4:
    explanations.append(f"Vehicle is {age} years old — component fatigue increases after year 4")
if annual_km > 18000:
    explanations.append(f"High annual usage ({annual_km:,} km) accelerates brake and tyre wear")
if mileage > 70000:
    explanations.append(f"Odometer at {mileage:,} km — approaching major service milestones")
if fuel == "EV" and age > 3:
    explanations.append("EV battery health check recommended after year 3")
if not explanations:
    explanations.append("Vehicle within normal maintenance risk parameters")

# ── UI ────────────────────────────────────────────────────────────────────────
st.markdown("<h1>04 — MAINTENANCE</h1>", unsafe_allow_html=True)
st.markdown(f"**{v.get('brand','')} {v.get('model','')} &nbsp;|&nbsp; {fuel} &nbsp;|&nbsp; Age: {age} yrs &nbsp;|&nbsp; {mileage:,} km**")
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"""<div class="card">
        <p style="font-weight:700;letter-spacing:0.1em;margin:0;">EST. ANNUAL COST</p>
        <p class="big-num">Rs.{annual_cost:,}</p>
        <span class="badge-est">ESTIMATED</span>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""<div class="card">
        <p style="font-weight:700;letter-spacing:0.1em;margin:0;">NEXT SERVICE DUE</p>
        <p class="big-num">{next_service:,} <span style="font-size:1.2rem;">km</span></p>
        <p style="margin:4px 0;font-size:0.9rem;">~{months_to_svc} months away ({km_to_service:,} km remaining)</p>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""<div class="card">
        <p style="font-weight:700;letter-spacing:0.1em;margin:0;">RISK SCORE</p>
        <p class="big-num" style="color:{risk_color};">{risk_score}<span style="font-size:1.5rem;">/100</span></p>
        <p style="font-weight:900;color:{risk_color};letter-spacing:0.15em;">{risk_label}</p>
    </div>""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
col4, col5 = st.columns(2)

with col4:
    st.markdown("### EVENT PROBABILITIES")
    # Filter out zero-prob events
    active = {k: v for k, v in events.items() if v > 0.01}
    fig = go.Figure(go.Bar(
        x=list(active.values()),
        y=list(active.keys()),
        orientation='h',
        marker=dict(color=['#FF2800' if v > 0.7 else '#1A1A1A' for v in active.values()]),
        text=[f"{int(p*100)}%" for p in active.values()],
        textposition='outside'
    ))
    fig.update_layout(
        plot_bgcolor='#F5F5F0', paper_bgcolor='#F5F5F0',
        xaxis=dict(range=[0, 1.1], title='Probability', gridcolor='#E0E0E0'),
        margin=dict(l=10, r=10, t=10, b=10), height=320
    )
    st.plotly_chart(fig, use_container_width=True)

with col5:
    st.markdown(f"### COST BREAKDOWN ({ownership}-YEAR TOTAL)")
    st.markdown(f"**Scheduled Servicing**: Rs.{sched_cost:,}")
    st.progress(sched_cost / total_5y)
    st.markdown(f"**Wear & Tear (Tyres/Brakes)**: Rs.{wear_cost:,}")
    st.progress(wear_cost / total_5y)
    st.markdown(f"**Unexpected Repairs**: Rs.{repair_cost:,}")
    st.progress(repair_cost / total_5y)
    st.markdown("---")
    st.markdown(f"**TOTAL ESTIMATED**: Rs.{total_5y:,}")

    st.markdown("### RISK FACTORS")
    for e in explanations:
        st.markdown(f"- {e}")

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown("### OEM SERVICE SCHEDULE REFERENCE")
if fuel == "EV":
    schedule = [
        {"Interval": "15,000 km", "Action": "Tyre rotation, brake inspection, cabin filter"},
        {"Interval": "30,000 km", "Action": "Coolant check, brake fluid, battery diagnostic"},
        {"Interval": "45,000 km", "Action": "Full system check, suspension inspection"},
    ]
else:
    schedule = [
        {"Interval": "10,000 km", "Action": "Engine oil & filter, general inspection"},
        {"Interval": "20,000 km", "Action": "AC filter, brake pads, tyre check"},
        {"Interval": "40,000 km", "Action": "Coolant, brake fluid, spark plugs, major check"},
        {"Interval": "80,000 km", "Action": "Timing belt/chain, transmission fluid, full overhaul"},
    ]
st.table(schedule)
st.caption("Maintenance costs are estimates based on OEM schedules, vehicle age, mileage, and fuel type. Actual costs vary by brand, city, and service provider.")
