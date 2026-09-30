# -*- coding: utf-8 -*-
"""
01 Vehicle Input — AUTOVAULT AI
Clean single-flow form. No duplicate controls.
Built-in live visualizations: variant price chart, depreciation preview.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import datetime

def format_price(val_lakhs):
    if val_lakhs >= 100:
        return f"Rs.{val_lakhs/100:.2f}Cr"
    return f"Rs.{val_lakhs:.2f}L"


st.set_page_config(
    page_title="Vehicle Input | AUTOVAULT AI",
    page_icon="ðŸš—",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom navigation
try:
    from app.components.navigation import build_sidebar
    build_sidebar()
except Exception as e:
    pass


# ─€─€ Design System ─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;700&family=Inter:wght@400;600;700;900&display=swap');

* { box-sizing: border-box; }
html, body, .stApp { background: #F4F4EF !important; font-family: 'Inter', sans-serif; color: #1A1A1A; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2.5rem 3rem !important; max-width: 1300px !important; }

/* ─€─€ Typography ─€─€ */
h1 { font-size: 2.2rem; font-weight: 900; letter-spacing: -0.01em; color: #1A1A1A; margin: 0; }
h2 { font-size: 1.1rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: #1A1A1A; }
h3 { font-size: 0.85rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.15em; color: #888; }

/* ─€─€ Inputs ─€─€ */
label {
  font-size: 0.68rem !important;
  font-weight: 700 !important;
  letter-spacing: 0.2em !important;
  text-transform: uppercase !important;
  color: #888 !important;
}
.stSelectbox > div > div {
  border: 2px solid #1A1A1A !important;
  border-radius: 0 !important;
  background: white !important;
  font-weight: 600 !important;
  box-shadow: 3px 3px 0 #1A1A1A !important;
  transition: box-shadow 120ms ease, border-color 120ms ease !important;
}
.stSelectbox > div > div:hover {
  border-color: #FF2800 !important;
  box-shadow: 3px 3px 0 #FF2800 !important;
}
.stNumberInput > div > div > input,
.stTextInput > div > div > input {
  border: 2px solid #1A1A1A !important;
  border-radius: 0 !important;
  background: white !important;
  font-weight: 600 !important;
  box-shadow: 3px 3px 0 #1A1A1A !important;
}
.stNumberInput > div > div > input:focus {
  border-color: #FF2800 !important;
  box-shadow: 3px 3px 0 #FF2800 !important;
  outline: none !important;
}

/* ─€─€ Slider ─€─€ */
.stSlider [role="slider"] {
  background: #FF2800 !important;
  border: 2px solid #1A1A1A !important;
  width: 20px !important; height: 20px !important;
}

/* ─€─€ Radio (segment selector) ─€─€ */
.stRadio > div { display: flex !important; gap: 0 !important; }
.stRadio label {
  border: 2px solid #1A1A1A !important;
  border-right: none !important;
  padding: 10px 20px !important;
  background: white !important;
  font-size: 0.72rem !important;
  font-weight: 700 !important;
  letter-spacing: 0.12em !important;
  cursor: pointer;
  transition: all 120ms ease !important;
  color: #1A1A1A !important;
}
.stRadio label:last-child { border-right: 2px solid #1A1A1A !important; }
.stRadio label:hover { background: #1A1A1A !important; color: white !important; }
.stRadio label:has(input:checked) { background: #FF2800 !important; color: white !important; border-color: #FF2800 !important; }
.stRadio label span:first-child { display: none !important; }
.stRadio input { display: none !important; }

/* ─€─€ Buttons ─€─€ */
.stButton > button {
  border-radius: 0 !important;
  font-family: 'IBM Plex Mono', monospace !important;
  font-weight: 700 !important;
  letter-spacing: 0.15em !important;
  text-transform: uppercase !important;
  transition: all 120ms ease !important;
}
.stButton > button[kind="primary"] {
  background: #1A1A1A !important;
  color: white !important;
  border: 2px solid #1A1A1A !important;
  box-shadow: 4px 4px 0 #FF2800 !important;
  font-size: 1rem !important;
  padding: 14px 32px !important;
}
.stButton > button[kind="primary"]:hover {
  background: #FF2800 !important;
  border-color: #FF2800 !important;
  box-shadow: 4px 4px 0 #1A1A1A !important;
  transform: translate(-2px,-2px) !important;
}
.stButton > button[kind="primary"]:active { transform: translate(2px,2px) !important; box-shadow: none !important; }
.stButton > button[kind="secondary"] {
  background: white !important;
  color: #1A1A1A !important;
  border: 2px solid #1A1A1A !important;
  box-shadow: 2px 2px 0 #1A1A1A !important;
}
.stButton > button[kind="secondary"]:hover {
  background: #1A1A1A !important;
  color: white !important;
}

/* ─€─€ Section card ─€─€ */
.sec { background: white; border: 2px solid #1A1A1A; padding: 28px; margin-bottom: 20px; }
.sec-head {
  display: flex; align-items: center; gap: 12px;
  border-bottom: 2px solid #1A1A1A; padding-bottom: 14px; margin-bottom: 22px;
}
.sec-num {
  background: #1A1A1A; color: white;
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.75rem; font-weight: 700;
  padding: 4px 10px; letter-spacing: 0.1em;
}
.sec-num.red { background: #FF2800; }
.sec-title { font-size: 1rem; font-weight: 900; text-transform: uppercase; letter-spacing: 0.08em; }

/* ─€─€ Price display ─€─€ */
.price-hero {
  background: #1A1A1A; color: white;
  padding: 20px 28px; margin: 16px 0;
  display: flex; align-items: center; gap: 32px;
}
.price-hero .main {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 2.8rem; font-weight: 700; color: #FF2800; line-height: 1;
}
.price-hero .label {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.6rem; font-weight: 700;
  letter-spacing: 0.2em; text-transform: uppercase;
  color: rgba(255,255,255,0.4); margin-bottom: 2px;
}
.price-hero .sub { font-size: 0.85rem; font-weight: 600; color: rgba(255,255,255,0.7); }

/* ─€─€ EMI bar ─€─€ */
.emi-bar {
  display: grid; grid-template-columns: repeat(4,1fr);
  gap: 2px; background: #1A1A1A;
  border: 2px solid #1A1A1A; margin: 16px 0;
}
.emi-cell { background: white; padding: 16px 20px; }
.emi-cell:first-child { border-left: 4px solid #FF2800; }
.emi-key { font-family:'IBM Plex Mono',monospace; font-size:0.6rem; font-weight:700; letter-spacing:0.2em; text-transform:uppercase; color:#888; margin-bottom:4px; }
.emi-val { font-family:'IBM Plex Mono',monospace; font-size:1.3rem; font-weight:700; color:#1A1A1A; }
.emi-val.red { color:#FF2800; }

/* ─€─€ Summary review ─€─€ */
.review-grid {
  display: grid; grid-template-columns: 1fr 1fr; gap: 2px;
  background: #1A1A1A; border: 2px solid #1A1A1A;
}
.review-cell { background: #F4F4EF; padding: 16px 20px; }
.review-cell.dark { background: #1A1A1A; }
.rv-key { font-family:'IBM Plex Mono',monospace; font-size:0.58rem; font-weight:700; letter-spacing:0.2em; text-transform:uppercase; color:#888; margin-bottom:3px; }
.rv-key.light { color:rgba(255,255,255,0.4); }
.rv-val { font-size:1rem; font-weight:700; color:#1A1A1A; }
.rv-val.light { color:white; }
.rv-val.red { color:#FF2800; }

/* ─€─€ Info note ─€─€ */
.info-note { border-left: 3px solid #FF2800; padding: 8px 14px; background: rgba(255,40,0,0.05); font-size:0.8rem; color:#555; margin: 8px 0; }

/* ─€─€ Chart section ─€─€ */
.chart-label {
  font-family:'IBM Plex Mono',monospace; font-size:0.65rem;
  font-weight:700; letter-spacing:0.2em; text-transform:uppercase; color:#888;
  margin-bottom:8px;
}

/* Divider */
hr { border:none; border-top:2px solid #1A1A1A; margin:24px 0; }

/* Selection feedback */
::selection { background:#FF2800; color:white; }
::-webkit-scrollbar { width:5px; } ::-webkit-scrollbar-thumb { background:#ccc; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# VEHICLE DATA
# ═══════════════════════════════════════════════════════════════════════════════

from app.utils.vehicle_db import DB

SEGMENTS = {b: ("Volume" if b in ["Maruti Suzuki","Hyundai","Tata","Mahindra","Kia","Toyota","Honda","Volkswagen","Skoda","MG","Renault","Nissan","Citroen"]
               else "Luxury" if b in ["BMW","Mercedes-Benz","Audi","Volvo"]
               else "Ultra Luxury")
            for b in DB}

CITIES = ["Mumbai","Delhi","Bengaluru","Chennai","Hyderabad","Pune","Kolkata",
          "Ahmedabad","Jaipur","Surat","Lucknow","Chandigarh","Kochi",
          "Coimbatore","Nagpur","Indore","Bhopal","Visakhapatnam","Noida","Gurugram"]

# ─€─€ Plotly theme ─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€
THEME = dict(
    plot_bgcolor="#FFFFFF", paper_bgcolor="#F4F4EF",
    font=dict(family="IBM Plex Mono, monospace", color="#1A1A1A"),
    margin=dict(l=10,r=10,t=30,b=10),
)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE
# ═══════════════════════════════════════════════════════════════════════════════

# Header
col_h1, col_h2 = st.columns([3,1])
with col_h1:
    st.markdown("""
    <div style="font-family:'IBM Plex Mono',monospace;font-size:0.65rem;font-weight:700;
    letter-spacing:0.25em;color:#FF2800;margin-bottom:6px;">AUTOVAULT AI · 01</div>
    <h1>Configure Your Vehicle</h1>
    <p style="color:#888;margin-top:6px;font-size:0.9rem;">
    Select brand, model and variant — exact prices and live analysis load automatically.
    </p>
    """, unsafe_allow_html=True)
with col_h2:
    st.markdown("""
    <div style="background:#1A1A1A;color:white;padding:16px 20px;margin-top:16px;">
    <div style="font-family:'IBM Plex Mono',monospace;font-size:0.6rem;letter-spacing:0.2em;color:rgba(255,255,255,0.4);">WHAT HAPPENS NEXT</div>
    <div style="font-size:0.78rem;margin-top:6px;line-height:1.7;color:rgba(255,255,255,0.7);">
    Health · Depreciation<br/>Maintenance · TCO<br/>Risk · Simulator · Compare
    </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr/>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — VEHICLE
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="sec-head">
  <span class="sec-num red">01</span>
  <span class="sec-title">Vehicle Selection</span>
</div>
""", unsafe_allow_html=True)

# Single segment filter — radio, not tabs (avoids the duplicate brand bug)
segment = st.radio("FILTER BY SEGMENT", ["ALL", "Volume", "Luxury", "Ultra Luxury"],
                   horizontal=True)

filtered_brands = sorted([b for b, s in SEGMENTS.items() if segment == "ALL" or s == segment])

# Single, clean 3-column selector
sel1, sel2, sel3, sel4 = st.columns(4)

with sel1:
    brand = st.selectbox("BRAND", filtered_brands,
                         index=filtered_brands.index("Hyundai") if "Hyundai" in filtered_brands else 0)

bdata = DB.get(brand, {})

# Find all unique body types (segments) for this brand
all_body_types = list(set([data.get("seg", "Other") for m, data in bdata.items()]))
all_body_types.sort()

with sel2:
    body_type = st.selectbox("BODY TYPE", ["All"] + all_body_types)

if body_type == "All":
    models = list(bdata.keys())
else:
    models = [m for m, data in bdata.items() if data.get("seg") == body_type]
    
# Fallback if list is empty for some reason
if not models: models = list(bdata.keys())

with sel3:
    model = st.selectbox("MODEL", models)

mdata    = bdata.get(model, {})
variants = mdata.get("v", ["Standard"])
prices   = mdata.get("p", [10.0])
fuels    = mdata.get("f", ["Petrol"])
seg_name = mdata.get("seg", "")

with sel4:
    variant_opts = [f"{v}  —  {format_price(p)}" for v, p in zip(variants, prices)]
    v_sel = st.selectbox("VARIANT", variant_opts)
    vi       = variant_opts.index(v_sel)
    variant  = variants[vi]
    ex_price = prices[vi]

# Price hero
st.markdown(f"""
<div class="price-hero">
    <div>
        <div class="label">EX-SHOWROOM PRICE</div>
        <div class="main">{format_price(ex_price)}</div>
        <div class="sub">{brand} {model} · {variant} · {seg_name}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─€─€ VISUALIZATION 1: Variant price comparison bar ─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€
st.markdown("<div class='chart-label'>VARIANT PRICE COMPARISON</div>", unsafe_allow_html=True)
colors = ["#FF2800" if v == variant else "#1A1A1A" for v in variants]
fig_var = go.Figure(go.Bar(
    x=variants, y=prices,
    marker_color=colors,
    text=[format_price(p) for p in prices],
    textposition="outside",
    textfont=dict(family="IBM Plex Mono", size=11, color="#1A1A1A"),
    hovertemplate="<b>%{x}</b><br>%{text}<extra></extra>",
))
fig_var.update_layout(
    **THEME,
    height=220,
    xaxis=dict(showgrid=False, tickfont=dict(size=10)),
    yaxis=dict(gridcolor="#EAEAEA", title="Rs. Lakhs"),
    showlegend=False,
    bargap=0.3,
)
fig_var.add_annotation(text=f"SELECTED: {variant}",
    xref="paper", yref="paper", x=0, y=1.02, showarrow=False,
    font=dict(family="IBM Plex Mono", size=9, color="#FF2800"))
st.plotly_chart(fig_var, use_container_width=True)

st.markdown("<hr/>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — USAGE
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="sec-head">
  <span class="sec-num">02</span>
  <span class="sec-title">Usage & History</span>
</div>
""", unsafe_allow_html=True)

u1, u2, u3, u4 = st.columns(4)
with u1:
    mfg_year = st.selectbox("YEAR", list(range(2025,2014,-1)))
with u2:
    odometer = st.number_input("ODOMETER (KM)", 0, 500000, 12000, 500)
with u3:
    annual_km = st.slider("ANNUAL KM", 3000, 60000, 12000, 1000)
with u4:
    ownership = st.slider("KEEP FOR (YRS)", 1, 12, 5, 1)

u5, u6 = st.columns(2)
with u5:
    city = st.selectbox("CITY", CITIES)
with u6:
    income = st.number_input("MONTHLY INCOME Rs. (optional)", 0, 50_000_000, 0, 10000)

current_year = datetime.datetime.now().year
age = max(0, current_year - mfg_year)

# ─€─€ VISUALIZATION 2: 5-year depreciation preview ─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€
DEPR = {"Petrol":[0.15,0.12,0.10,0.09,0.08,0.07,0.07],
        "Diesel":[0.18,0.13,0.10,0.09,0.08,0.07,0.07],
        "EV":    [0.20,0.15,0.12,0.10,0.09,0.08,0.08],
        "Hybrid":[0.13,0.11,0.09,0.08,0.07,0.07,0.06],
        "CNG":   [0.16,0.12,0.10,0.09,0.08,0.07,0.07]}
fuel0  = fuels[0]
rates0 = DEPR.get(fuel0, DEPR["Petrol"])
dep_vals = [ex_price]
for y in range(ownership):
    dep_vals.append(round(dep_vals[-1] * (1 - rates0[min(y, len(rates0)-1)]), 2))

dep_years = list(range(ownership+1))

d1, d2 = st.columns([3,1])
with d1:
    st.markdown("<div class='chart-label'>ESTIMATED VALUE OVER OWNERSHIP PERIOD (Preview)</div>", unsafe_allow_html=True)
    fig_dep = go.Figure()
    fig_dep.add_trace(go.Scatter(
        x=dep_years, y=dep_vals,
        mode="lines+markers",
        fill="tozeroy",
        fillcolor="rgba(255,40,0,0.07)",
        line=dict(color="#FF2800", width=3),
        marker=dict(size=9, color="#1A1A1A", symbol="circle"),
        text=[format_price(v) for v in dep_vals],
        hovertemplate="Year %{x}: %{text}<extra></extra>",
    ))
    fig_dep.update_layout(
        **THEME, height=200,
        xaxis=dict(title="Ownership Year", tickmode="linear", gridcolor="#EAEAEA"),
        yaxis=dict(title="Est. Value (Rs.L)", gridcolor="#EAEAEA"),
    )
    st.plotly_chart(fig_dep, use_container_width=True)

with d2:
    total_depr = round((ex_price - dep_vals[-1]) / ex_price * 100, 1)
    st.markdown(f"""
    <div style="background:#1A1A1A;padding:20px;height:100%;display:flex;flex-direction:column;justify-content:center;gap:12px;margin-top:28px;">
        <div>
            <div style="font-family:'IBM Plex Mono',monospace;font-size:0.6rem;letter-spacing:0.2em;color:rgba(255,255,255,0.4);">PURCHASE</div>
            <div style="font-family:'IBM Plex Mono',monospace;font-size:1.2rem;font-weight:700;color:white;">{format_price(ex_price)}</div>
        </div>
        <div>
            <div style="font-family:'IBM Plex Mono',monospace;font-size:0.6rem;letter-spacing:0.2em;color:rgba(255,255,255,0.4);">EST. RESALE ({ownership}yr)</div>
            <div style="font-family:'IBM Plex Mono',monospace;font-size:1.2rem;font-weight:700;color:#FF2800;">{format_price(dep_vals[-1])}</div>
        </div>
        <div>
            <div style="font-family:'IBM Plex Mono',monospace;font-size:0.6rem;letter-spacing:0.2em;color:rgba(255,255,255,0.4);">TOTAL DEPRECIATION</div>
            <div style="font-family:'IBM Plex Mono',monospace;font-size:1.2rem;font-weight:700;color:#FF2800;">{total_depr}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr/>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — FUEL TYPE
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="sec-head">
  <span class="sec-num red">03</span>
  <span class="sec-title">Fuel Type</span>
</div>
""", unsafe_allow_html=True)

fuel_type = st.radio("SELECT FUEL", list(dict.fromkeys(fuels)), horizontal=True)

FUEL_DATA = {
    "Petrol": ("~Rs.106/L","17–22 km/L","High price volatility risk"),
    "Diesel": ("~Rs.94/L","18–25 km/L","Better highway range"),
    "CNG":    ("~Rs.80/kg","25–30 km/kg","Lowest running cost"),
    "EV":     ("~Rs.8/kWh","5–7 km/kWh","Zero emission, cheapest per km"),
    "Hybrid": ("~Rs.106/L","22–28 km/L","Best city efficiency, self-charging"),
}
fuel_note = FUEL_DATA.get(fuel_type, ("","",""))
st.markdown(f"""
<div class="info-note">
<strong>{fuel_type}</strong> &nbsp;·&nbsp; Price: {fuel_note[0]} &nbsp;·&nbsp;
Efficiency: {fuel_note[1]} &nbsp;·&nbsp; {fuel_note[2]}
</div>
""", unsafe_allow_html=True)

# ─€─€ VISUALIZATION 3: Fuel cost per 15000 km comparison ─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€─€
st.markdown("<div class='chart-label'>ANNUAL RUNNING COST COMPARISON (at 15,000 km/yr)</div>", unsafe_allow_html=True)
fuel_costs = {"Petrol":  (15000/19)*106/100000,
              "Diesel":  (15000/22)*94/100000,
              "CNG":     (15000/27)*80/100000,
              "EV":      (15000/6)*8/100000,
              "Hybrid":  (15000/25)*106/100000}
avail_fuels_all = list(fuel_costs.keys())
cost_vals = [round(fuel_costs[f], 2) for f in avail_fuels_all]
bar_colors = ["#FF2800" if f == fuel_type else "#D0D0C8" for f in avail_fuels_all]

fig_fuel = go.Figure(go.Bar(
    x=avail_fuels_all, y=cost_vals,
    marker_color=bar_colors,
    text=[f"{format_price(v)}/yr" for v in cost_vals],
    textposition="outside",
    textfont=dict(family="IBM Plex Mono", size=10),
    hovertemplate="<b>%{x}</b><br>%{text} per year<extra></extra>",
))
fig_fuel.update_layout(
    **THEME, height=200,
    xaxis=dict(showgrid=False),
    yaxis=dict(gridcolor="#EAEAEA", title="Rs. Lakhs/yr"),
    bargap=0.35,
)
st.plotly_chart(fig_fuel, use_container_width=True)

# EV section
battery_capacity, charging_freq, fast_charge_pct = None, "Daily", 0

if fuel_type == "EV":
    st.markdown("""
    <div style="border:2px dashed #FF2800;padding:16px 20px;background:rgba(255,40,0,0.03);margin-bottom:8px;">
    <strong style="font-family:'IBM Plex Mono',monospace;font-size:0.72rem;letter-spacing:0.15em;color:#FF2800;">
    BATTERY DETAILS — Required for health analysis
    </strong>
    </div>
    """, unsafe_allow_html=True)
    ev1, ev2, ev3 = st.columns(3)
    with ev1:
        battery_capacity = st.number_input("BATTERY CAPACITY (kWh)", 10.0, 200.0, 40.0, 0.5)
    with ev2:
        charging_freq = st.selectbox("CHARGING FREQUENCY", ["Daily","Every 2-3 Days","Weekly","Rarely"])
    with ev3:
        fast_charge_pct = st.slider("FAST CHARGING %", 0, 100, 20)
    if fast_charge_pct > 60:
        st.warning(f"High fast charging ({fast_charge_pct}%) reduces battery lifespan. Recommend <40% for longevity.")

st.markdown("<hr/>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — FINANCING
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="sec-head">
  <span class="sec-num">04</span>
  <span class="sec-title">Financing</span>
</div>
""", unsafe_allow_html=True)

fin1, fin2, fin3, fin4 = st.columns(4)
with fin1:
    on_road = st.number_input("ON-ROAD PRICE (Rs.L)",
                               1.0, 10000.0, round(ex_price * 1.10, 1), 0.10)
with fin2:
    down_pct = st.slider("DOWN PAYMENT %", 0, 100, 20, 5)
with fin3:
    loan_rate = st.slider("INTEREST RATE %", 6.0, 20.0, 9.0, 0.25)
with fin4:
    tenure = st.selectbox("TENURE", [12,24,36,48,60,72,84], index=4,
                           format_func=lambda x: f"{x} mo · {x//12}yr{'' if x//12==1 else 's'}")

# EMI
principal = on_road * (1 - down_pct/100) * 100000
down_amt  = on_road * down_pct / 100
if loan_rate > 0 and tenure > 0 and down_pct < 100:
    r   = loan_rate / (12*100)
    emi = principal * r * (1+r)**tenure / ((1+r)**tenure - 1)
    total_paid = emi * tenure
    interest   = total_paid - principal
else:
    emi = principal / tenure if tenure else 0
    interest = 0; total_paid = principal

st.markdown(f"""
<div class="emi-bar">
    <div class="emi-cell">
        <div class="emi-key">Monthly EMI</div>
        <div class="emi-val red">Rs.{emi:,.0f}</div>
    </div>
    <div class="emi-cell">
        <div class="emi-key">Down Payment</div>
        <div class="emi-val">{format_price(down_amt)}</div>
    </div>
    <div class="emi-cell">
        <div class="emi-key">Total Interest</div>
        <div class="emi-val">{format_price(interest/100000)}</div>
    </div>
    <div class="emi-cell">
        <div class="emi-key">Loan Amount</div>
        <div class="emi-val">{format_price(principal/100000)}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─€─€ VISUALIZATION 4: EMI amortization — principal vs interest split ─€─€─€─€─€─€─€─€─€─€─€
years_axis = list(range(1, tenure+1))
balance    = principal
p_list, i_list = [], []
r = loan_rate / (12*100)
for m in range(1, tenure+1):
    int_m  = balance * r
    prin_m = emi - int_m
    balance = max(0, balance - prin_m)
    p_list.append(round(prin_m, 0))
    i_list.append(round(int_m, 0))

fig_emi = go.Figure()
fig_emi.add_trace(go.Bar(x=years_axis, y=p_list, name="Principal",
    marker_color="#1A1A1A", hovertemplate="Month %{x}<br>Principal: Rs.%{y:,.0f}<extra></extra>"))
fig_emi.add_trace(go.Bar(x=years_axis, y=i_list, name="Interest",
    marker_color="#FF2800", hovertemplate="Month %{x}<br>Interest: Rs.%{y:,.0f}<extra></extra>"))
fig_emi.update_layout(
    **THEME, height=220, barmode="stack",
    xaxis=dict(title="Month", showgrid=False),
    yaxis=dict(title="Rs.", gridcolor="#EAEAEA"),
    legend=dict(orientation="h", y=-0.25, font=dict(family="IBM Plex Mono", size=10)),
)
st.markdown("<div class='chart-label'>EMI BREAKDOWN — PRINCIPAL VS INTEREST (MONTH BY MONTH)</div>", unsafe_allow_html=True)
st.plotly_chart(fig_emi, use_container_width=True)

if interest > principal * 0.35:
    st.warning(f"You'll pay {format_price(interest/100000)} in interest — consider a larger down payment or shorter tenure.")

st.markdown("<hr/>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# REVIEW & SUBMIT
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="sec-head">
  <span class="sec-num red">05</span>
  <span class="sec-title">Review & Launch Analysis</span>
</div>
""", unsafe_allow_html=True)

rc1, rc2 = st.columns(2)
with rc1:
    st.markdown(f"""
    <div style="background:white;border:2px solid #1A1A1A;padding:24px;">
        <div style="font-family:'IBM Plex Mono',monospace;font-size:0.6rem;letter-spacing:0.2em;color:#888;margin-bottom:8px;">VEHICLE</div>
        <div style="font-size:1.5rem;font-weight:900;text-transform:uppercase;line-height:1.1;margin-bottom:16px;">
            {brand}<br/><span style="color:#FF2800;">{model}</span>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
            <div><div style="font-size:0.6rem;font-weight:700;letter-spacing:0.15em;color:#888;text-transform:uppercase;">Variant</div><div style="font-weight:700;">{variant}</div></div>
            <div><div style="font-size:0.6rem;font-weight:700;letter-spacing:0.15em;color:#888;text-transform:uppercase;">Fuel</div><div style="font-weight:700;">{fuel_type}</div></div>
            <div><div style="font-size:0.6rem;font-weight:700;letter-spacing:0.15em;color:#888;text-transform:uppercase;">Year / Age</div><div style="font-weight:700;">{mfg_year} · {age}yr</div></div>
            <div><div style="font-size:0.6rem;font-weight:700;letter-spacing:0.15em;color:#888;text-transform:uppercase;">City</div><div style="font-weight:700;">{city}</div></div>
            <div><div style="font-size:0.6rem;font-weight:700;letter-spacing:0.15em;color:#888;text-transform:uppercase;">Odometer</div><div style="font-weight:700;">{odometer:,} km</div></div>
            <div><div style="font-size:0.6rem;font-weight:700;letter-spacing:0.15em;color:#888;text-transform:uppercase;">Annual KM</div><div style="font-weight:700;">{annual_km:,} km/yr</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
with rc2:
    st.markdown(f"""
    <div style="background:#1A1A1A;padding:24px;height:100%;">
        <div style="font-family:'IBM Plex Mono',monospace;font-size:0.6rem;letter-spacing:0.2em;color:rgba(255,255,255,0.4);margin-bottom:4px;">ON-ROAD PRICE</div>
        <div style="font-family:'IBM Plex Mono',monospace;font-size:2.6rem;font-weight:700;color:#FF2800;line-height:1;margin-bottom:20px;">{format_price(on_road)}</div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
            <div><div style="font-family:'IBM Plex Mono',monospace;font-size:0.58rem;letter-spacing:0.15em;color:rgba(255,255,255,0.4);">EMI</div><div style="font-family:'IBM Plex Mono',monospace;font-size:1.2rem;font-weight:700;color:white;">Rs.{emi:,.0f}/mo</div></div>
            <div><div style="font-family:'IBM Plex Mono',monospace;font-size:0.58rem;letter-spacing:0.15em;color:rgba(255,255,255,0.4);">DOWN</div><div style="font-family:'IBM Plex Mono',monospace;font-size:1.2rem;font-weight:700;color:white;">{format_price(down_amt)}</div></div>
            <div><div style="font-family:'IBM Plex Mono',monospace;font-size:0.58rem;letter-spacing:0.15em;color:rgba(255,255,255,0.4);">EST. RESALE</div><div style="font-family:'IBM Plex Mono',monospace;font-size:1.2rem;font-weight:700;color:#FF2800;">{format_price(dep_vals[-1])}</div></div>
            <div><div style="font-family:'IBM Plex Mono',monospace;font-size:0.58rem;letter-spacing:0.15em;color:rgba(255,255,255,0.4);">OWNERSHIP</div><div style="font-family:'IBM Plex Mono',monospace;font-size:1.2rem;font-weight:700;color:white;">{ownership} YRS</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br/>", unsafe_allow_html=True)

btn_col, note_col = st.columns([2,1])
with btn_col:
    go_btn = st.button(f"ANALYZE {brand.upper()} {model.upper()} — START", use_container_width=True, type="primary")
with note_col:
    st.markdown("""
    <div style="padding:12px 0;color:#888;font-size:0.78rem;line-height:1.8;">
    Proceeds to health, depreciation, maintenance,<br>TCO, risk, simulator, and comparison.
    </div>
    """, unsafe_allow_html=True)

if go_btn:
    st.session_state.vehicle_data = {
        "brand": brand, "model": model, "variant": variant,
        "fuel_type": fuel_type, "segment": seg_name,
        "purchase_price": on_road, "ex_showroom_price": ex_price,
        "mfg_year": mfg_year, "current_mileage": odometer,
        "annual_mileage": annual_km, "ownership_period": ownership,
        "city": city, "income": income,
        "battery_capacity": battery_capacity,
        "charging_freq": charging_freq,
        "fast_charge_pct": fast_charge_pct if fuel_type == "EV" else 0,
        "down_payment_pct": down_pct,
        "loan_rate": loan_rate,
        "tenure_months": tenure,
    }
    st.success(f"✅ {brand} {model} {variant} — analysis ready. Loading...")
    st.balloons()
    import time; time.sleep(0.6)
    st.switch_page("pages/02_Vehicle_Health.py")

