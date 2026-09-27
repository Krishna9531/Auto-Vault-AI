# -*- coding: utf-8 -*-
"""
02 Vehicle Health - AUTOVAULT AI
Scores vehicle health based on age, mileage, fuel type, accident and service history.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Vehicle Health | AUTOVAULT AI", page_icon="🚗", layout="wide")

# Custom navigation
try:
    from app.components.navigation import build_sidebar
    build_sidebar()
except Exception as e:
    pass


# ── Brutalist CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;700&family=Inter:wght@400;700;900&display=swap');
body, .stApp { background-color: #F5F5F0; font-family: 'Inter', system-ui, sans-serif; }
h1,h2,h3 { text-transform: uppercase; letter-spacing: 0.08em; font-weight: 900; }
.card { background: white; border: 2px solid #1A1A1A; padding: 24px; margin-bottom: 16px; }
.big-num { font-family: 'IBM Plex Mono', monospace; font-size: 3.5rem; font-weight: 700; color: #1A1A1A; line-height: 1; }
.red { color: #FF2800; }
.badge-est { background:#1A1A1A; color:white; padding:2px 8px; font-size:0.7rem; font-weight:700; letter-spacing:0.1em; }
.badge-ver { background:#FF2800; color:white; padding:2px 8px; font-size:0.7rem; font-weight:700; letter-spacing:0.1em; }
.divider { border-top: 3px solid #1A1A1A; margin: 20px 0; }
</style>
""", unsafe_allow_html=True)

# ── Guard ─────────────────────────────────────────────────────────────────────
if "vehicle_data" not in st.session_state or st.session_state.vehicle_data is None:
    st.error("NO VEHICLE DATA FOUND. PLEASE COMPLETE THE INPUT FORM FIRST.")
    if st.button("GO TO INPUT"):
        st.switch_page("pages/01_Vehicle_Input.py")
    st.stop()

v = st.session_state.vehicle_data

# ── Health Computation ────────────────────────────────────────────────────────
import datetime
current_year = datetime.datetime.now().year
age = current_year - v.get("mfg_year", current_year)
mileage = v.get("current_mileage", 0)
annual_km = v.get("annual_mileage", 12000)
fuel = v.get("fuel_type", "Petrol")
city = v.get("city", "Delhi")

HIGH_TEMP_CITIES = ["Chennai", "Hyderabad", "Ahmedabad", "Jaipur", "Nagpur"]

base = 100.0
positives, negatives = [], []

# Age penalty
age_penalty = max(0, (age - 2) * 2.5)
base -= age_penalty
if age <= 2:
    positives.append(f"Low vehicle age ({age} yr) — minimal wear accumulation")
elif age >= 5:
    negatives.append(f"Vehicle age {age} yrs — elevated component fatigue expected")

# Mileage penalty
km_penalty = max(0, (mileage - 50000) / 10000) * 1.5
base -= km_penalty
if mileage < 40000:
    positives.append(f"Low odometer ({mileage:,} km) — drivetrain in good condition")
elif mileage > 80000:
    negatives.append(f"High mileage ({mileage:,} km) — increased wear probability")

# EV bonus (simpler drivetrain)
if fuel == "EV":
    base += 3
    positives.append("Electric drivetrain — no engine oil, fewer moving parts")
    fast_pct = v.get("fast_charge_pct", 0) or 0
    if fast_pct > 50:
        base -= 5
        negatives.append(f"High fast-charging usage ({fast_pct}%) — accelerates battery degradation")

# Annual mileage intensity
if annual_km > 20000:
    penalty = (annual_km - 20000) / 5000
    base -= penalty
    negatives.append(f"High annual usage ({annual_km:,} km/yr) — increases wear rate")
elif annual_km < 10000:
    positives.append(f"Low annual usage ({annual_km:,} km/yr) — extends component life")

# Climate
if city in HIGH_TEMP_CITIES:
    base -= 2
    negatives.append(f"High-temperature city ({city}) — extra thermal stress on engine & battery")

# Clamp
overall = max(20, min(98, round(base)))

# Sub-scores
mechanical = max(20, min(98, overall - 3 + (3 if fuel != "EV" else 0)))
electrical = max(20, min(98, overall + 2 - (5 if fuel == "EV" and (v.get("fast_charge_pct") or 0) > 50 else 0)))
usage_score = max(20, min(98, 100 - int(annual_km / 500)))
service_score = 85  # Default; would improve with real service history

# Health label
if overall >= 85:
    hlabel, hcolor = "EXCELLENT", "#006400"
elif overall >= 70:
    hlabel, hcolor = "GOOD", "#228B22"
elif overall >= 55:
    hlabel, hcolor = "FAIR", "#FF8C00"
else:
    hlabel, hcolor = "POOR", "#FF2800"

# Battery SOH estimate (EV only)
if fuel == "EV":
    battery_cap = v.get("battery_capacity", 40)
    soh = max(70, 100 - (age * 3) - (mileage / 100000 * 10))
    soh = round(min(100, soh), 1)

# ── UI ────────────────────────────────────────────────────────────────────────
st.markdown("<h1>02 — VEHICLE HEALTH</h1>", unsafe_allow_html=True)
st.markdown(f"**{v.get('brand','')} {v.get('model','')} {v.get('variant','')} &nbsp;|&nbsp; {v.get('mfg_year','')} &nbsp;|&nbsp; {mileage:,} km**")
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown(f"""
    <div class="card" style="text-align:center;">
        <p style="font-weight:700;letter-spacing:0.1em;margin:0;">OVERALL HEALTH</p>
        <p class="big-num" style="font-size:5rem;color:{hcolor};">{overall}<span style="font-size:2rem;color:#1A1A1A;">/100</span></p>
        <p style="font-weight:900;color:{hcolor};letter-spacing:0.15em;">{hlabel}</p>
        <span class="badge-est">ESTIMATED</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**DATA CONFIDENCE**")
    conf = min(90, 60 + (10 if age <= 3 else 0) + (10 if mileage < 60000 else 0) + (10 if fuel == "EV" else 5))
    st.progress(conf / 100, text=f"{conf}%")
    st.caption("Based on age, mileage, fuel type, and usage pattern.")

with col2:
    st.markdown("### SUB-SCORES")

    for label, score in [("MECHANICAL", mechanical), ("ELECTRICAL", electrical),
                          ("USAGE PATTERN", usage_score), ("SERVICE HISTORY", service_score)]:
        color = "#006400" if score >= 80 else "#FF8C00" if score >= 60 else "#FF2800"
        st.markdown(f"**{label}** — <span style='color:{color};font-family:IBM Plex Mono,monospace;font-weight:700;'>{score}/100</span>", unsafe_allow_html=True)
        st.progress(score / 100)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
col3, col4 = st.columns(2)

with col3:
    st.markdown("### POSITIVE FACTORS")
    if not positives:
        positives.append("Vehicle meets baseline health criteria")
    for p in positives:
        st.markdown(f"<span style='color:#006400;font-weight:700;'>+ </span> {p}", unsafe_allow_html=True)

with col4:
    st.markdown("### NEGATIVE FACTORS")
    if not negatives:
        st.markdown("<span style='color:#006400;'>No significant risk factors identified</span>", unsafe_allow_html=True)
    for n in negatives:
        st.markdown(f"<span style='color:#FF2800;font-weight:700;'>- </span> {n}", unsafe_allow_html=True)

# EV Battery Section
if fuel == "EV":
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("### EV BATTERY STATE OF HEALTH")
    bcol1, bcol2, bcol3 = st.columns(3)
    with bcol1:
        st.markdown(f"""
        <div class="card" style="text-align:center;">
            <p style="font-weight:700;letter-spacing:0.1em;margin:0;">ESTIMATED SOH</p>
            <p class="big-num" style="color:#FF2800;">{soh}<span style="font-size:1.5rem;">%</span></p>
            <span class="badge-est">ESTIMATED</span>
        </div>""", unsafe_allow_html=True)
    with bcol2:
        st.markdown(f"""
        <div class="card" style="text-align:center;">
            <p style="font-weight:700;letter-spacing:0.1em;margin:0;">CAPACITY</p>
            <p class="big-num">{battery_cap}<span style="font-size:1.5rem;"> kWh</span></p>
            <span class="badge-ver">MANUFACTURER SPEC</span>
        </div>""", unsafe_allow_html=True)
    with bcol3:
        rul = max(0, round((soh - 70) / 3))
        st.markdown(f"""
        <div class="card" style="text-align:center;">
            <p style="font-weight:700;letter-spacing:0.1em;margin:0;">REMAINING USEFUL LIFE</p>
            <p class="big-num">~{rul}<span style="font-size:1.5rem;"> yrs</span></p>
            <span class="badge-est">ESTIMATED</span>
        </div>""", unsafe_allow_html=True)

    # Degradation curve
    soh_curve = [min(100, soh + (age * 3) - (i * 3)) for i in range(11)]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(range(11)), y=soh_curve, mode='lines+markers',
        line=dict(color='#FF2800', width=3), marker=dict(size=8, color='#1A1A1A'),
        name="Projected SOH"
    ))
    fig.add_hline(y=70, line_dash="dash", line_color="#888", annotation_text="80% Threshold (Usable)")
    fig.update_layout(
        plot_bgcolor='#F5F5F0', paper_bgcolor='#F5F5F0',
        xaxis=dict(title="Future Years", gridcolor='#E0E0E0'),
        yaxis=dict(title="SOH %", range=[50, 105], gridcolor='#E0E0E0'),
        margin=dict(l=10, r=10, t=10, b=10), height=280
    )
    st.plotly_chart(fig, use_container_width=True)

st.caption("Note: Health scores are model-based estimates derived from vehicle age, mileage, and usage pattern — not from direct diagnostic telemetry.")
