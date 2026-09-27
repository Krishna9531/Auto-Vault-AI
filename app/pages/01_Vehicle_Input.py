# -*- coding: utf-8 -*-
"""
01 Vehicle Input - AUTOVAULT AI
Complete vehicle input form with real Indian car brands, models, variants, and prices.
"""
import streamlit as st
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

st.set_page_config(page_title="Vehicle Input | AUTOVAULT AI", page_icon="🚗", layout="wide",
                   initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;700&family=Inter:wght@300;400;700;900&display=swap');

*, body, .stApp { background-color: #F5F5F0 !important; font-family: 'Inter', system-ui, sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem !important; max-width: 1400px; }

h1, h2, h3 { text-transform: uppercase; letter-spacing: 0.08em; font-weight: 900; color: #1A1A1A; }

/* Section panels */
.section-panel {
    background: white;
    border: 2px solid #1A1A1A;
    padding: 28px 28px 20px 28px;
    margin-bottom: 20px;
}
.section-label {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #FF2800;
    font-family: 'IBM Plex Mono', monospace;
    margin-bottom: 4px;
}
.section-title {
    font-size: 1.2rem;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #1A1A1A;
    border-bottom: 2px solid #1A1A1A;
    padding-bottom: 10px;
    margin-bottom: 20px;
}

/* Price badge */
.price-badge {
    display: inline-block;
    background: #1A1A1A;
    color: white;
    padding: 6px 14px;
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 700;
    font-size: 0.85rem;
    letter-spacing: 0.08em;
    margin: 8px 0 4px 0;
}
.price-badge-red {
    display: inline-block;
    background: #FF2800;
    color: white;
    padding: 6px 14px;
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 700;
    font-size: 0.85rem;
}
.segment-tag {
    display: inline-block;
    border: 1.5px solid #1A1A1A;
    padding: 2px 8px;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-left: 8px;
    vertical-align: middle;
}

/* Streamlit widget overrides */
.stSelectbox > div > div, .stTextInput > div > div > input,
.stNumberInput > div > div > input {
    border: 2px solid #1A1A1A !important;
    border-radius: 0 !important;
    background: white !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
}
.stSelectbox > div > div:focus-within, .stTextInput > div > div > input:focus {
    border-color: #FF2800 !important;
    box-shadow: none !important;
}
.stSlider > div > div > div { background: #1A1A1A !important; }
.stSlider [data-testid="stThumbValue"] { color: #FF2800 !important; }

/* Radio buttons */
.stRadio > div { gap: 8px !important; }
.stRadio label {
    border: 2px solid #1A1A1A !important;
    padding: 6px 14px !important;
    font-weight: 700 !important;
    font-size: 0.82rem !important;
    cursor: pointer;
    background: white !important;
}
.stRadio [data-testid="stMarkdownContainer"] p { font-size: 0.82rem; font-weight: 700; }

/* Analyze button */
.stButton > button[kind="primary"] {
    background: #1A1A1A !important;
    color: white !important;
    border: none !important;
    border-radius: 0 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-weight: 700 !important;
    font-size: 1.05rem !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    padding: 1rem !important;
    transition: background 0.15s !important;
}
.stButton > button[kind="primary"]:hover { background: #FF2800 !important; }
.stButton > button[kind="secondary"] {
    background: white !important;
    color: #1A1A1A !important;
    border: 2px solid #1A1A1A !important;
    border-radius: 0 !important;
    font-weight: 700 !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] { gap: 0; border-bottom: 2px solid #1A1A1A !important; }
.stTabs [data-baseweb="tab"] {
    border: 2px solid #1A1A1A !important;
    border-bottom: none !important;
    border-radius: 0 !important;
    font-weight: 700 !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    padding: 8px 18px !important;
    background: white !important;
    margin-right: 4px;
}
.stTabs [aria-selected="true"] { background: #1A1A1A !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# REAL VEHICLE DATABASE
# ═══════════════════════════════════════════════════════════════════════════════

VEHICLE_DB = {
    # ── MARUTI SUZUKI ──────────────────────────────────────────────────────────
    "Maruti Suzuki": {
        "Alto K10":     {"variants": ["STD", "LXI", "VXI", "ZXI", "ZXI+"], "prices": [3.99, 4.26, 4.79, 5.45, 5.83], "fuel": ["Petrol", "CNG"], "segment": "Hatchback"},
        "Swift":        {"variants": ["LXI", "VXI", "ZXI", "ZXI+"], "prices": [6.49, 7.49, 8.49, 9.64], "fuel": ["Petrol", "CNG"], "segment": "Hatchback"},
        "Baleno":       {"variants": ["Sigma", "Delta", "Zeta", "Alpha"], "prices": [6.61, 7.45, 8.45, 9.88], "fuel": ["Petrol", "CNG"], "segment": "Hatchback"},
        "Dzire":        {"variants": ["LXI", "VXI", "ZXI", "ZXI+"], "prices": [6.79, 7.81, 8.85, 9.93], "fuel": ["Petrol", "CNG"], "segment": "Sedan"},
        "Ertiga":       {"variants": ["LXI", "VXI", "ZXI", "ZXI+"], "prices": [8.69, 10.44, 12.09, 13.08], "fuel": ["Petrol", "CNG"], "segment": "MPV"},
        "Brezza":       {"variants": ["LXI", "VXI", "ZXI", "ZXI+", "ZXI+ Dual Tone"], "prices": [8.34, 10.49, 12.52, 14.14, 14.58], "fuel": ["Petrol", "CNG"], "segment": "SUV"},
        "Grand Vitara": {"variants": ["Sigma", "Delta", "Zeta", "Alpha", "Alpha+ Hybrid"], "prices": [10.70, 13.45, 16.45, 18.99, 19.99], "fuel": ["Petrol", "Hybrid"], "segment": "SUV"},
        "Jimny":        {"variants": ["Zeta", "Alpha"], "prices": [12.74, 15.05], "fuel": ["Petrol"], "segment": "Off-Road SUV"},
        "Fronx":        {"variants": ["Sigma", "Delta", "Delta+", "Zeta", "Alpha"], "prices": [7.51, 8.97, 10.04, 11.41, 13.06], "fuel": ["Petrol", "CNG"], "segment": "SUV"},
    },

    # ── HYUNDAI ────────────────────────────────────────────────────────────────
    "Hyundai": {
        "i20":          {"variants": ["Era", "Magna", "Sportz", "Asta", "Asta (O)"], "prices": [7.04, 8.27, 9.84, 11.12, 12.10], "fuel": ["Petrol", "Diesel", "CNG"], "segment": "Hatchback"},
        "Venue":        {"variants": ["E", "S", "S+", "SX", "SX+", "SX(O)"], "prices": [7.94, 9.53, 10.47, 12.08, 13.12, 13.57], "fuel": ["Petrol", "Diesel", "CNG"], "segment": "SUV"},
        "Creta":        {"variants": ["E", "EX", "S", "S+", "SX", "SX(O)"], "prices": [11.00, 12.50, 14.25, 16.50, 18.75, 20.15], "fuel": ["Petrol", "Diesel", "CNG"], "segment": "SUV"},
        "Creta Electric":{"variants": ["Executive", "Smart", "Smart+", "Prime", "Prime+", "Excellence"], "prices": [17.99, 18.99, 19.89, 21.40, 22.60, 23.50], "fuel": ["EV"], "segment": "Electric SUV"},
        "Alcazar":      {"variants": ["Prestige", "Prestige(O)", "Platinum", "Signature", "Signature(O)"], "prices": [14.99, 16.77, 18.18, 20.17, 21.45], "fuel": ["Petrol", "Diesel"], "segment": "3-Row SUV"},
        "Tucson":       {"variants": ["Platinum", "Signature 2WD", "Signature AWD"], "prices": [26.93, 32.25, 34.59], "fuel": ["Petrol", "Diesel"], "segment": "Premium SUV"},
        "Ioniq 5":      {"variants": ["RWD Standard", "RWD Long Range", "AWD Long Range"], "prices": [44.95, 46.95, 60.45], "fuel": ["EV"], "segment": "Electric SUV"},
    },

    # ── TATA ──────────────────────────────────────────────────────────────────
    "Tata": {
        "Tiago":        {"variants": ["XE", "XM", "XM+", "XT", "XZ", "XZ+"], "prices": [5.60, 6.20, 6.75, 7.25, 8.10, 8.45], "fuel": ["Petrol", "CNG"], "segment": "Hatchback"},
        "Tigor":        {"variants": ["XE", "XM", "XT", "XZ", "XZ+"], "prices": [6.30, 7.05, 7.80, 8.70, 9.50], "fuel": ["Petrol", "CNG"], "segment": "Sedan"},
        "Punch":        {"variants": ["Pure", "Adventure", "Accomplished", "Creative"], "prices": [6.13, 7.49, 8.49, 10.20], "fuel": ["Petrol", "CNG"], "segment": "Micro SUV"},
        "Punch EV":     {"variants": ["Smart", "Smart+", "Adventure", "Empowered", "Empowered+"], "prices": [10.99, 11.99, 13.49, 14.49, 15.49], "fuel": ["EV"], "segment": "Electric Micro SUV"},
        "Tiago EV":     {"variants": ["XT", "XZ", "XZ+", "XZ+ Tech LR"], "prices": [8.69, 9.99, 11.49, 12.04], "fuel": ["EV"], "segment": "Electric Hatchback"},
        "Nexon":        {"variants": ["Smart", "Smart+", "Pure", "Creative", "Fearless", "Fearless+"], "prices": [8.10, 9.30, 10.49, 12.99, 14.29, 15.50], "fuel": ["Petrol", "Diesel", "CNG"], "segment": "SUV"},
        "Nexon EV":     {"variants": ["Smart", "Smart+", "Creative", "Fearless", "Fearless+"], "prices": [12.49, 13.99, 15.49, 17.49, 19.00], "fuel": ["EV"], "segment": "Electric SUV"},
        "Curvv":        {"variants": ["Smart", "Smart+", "Accomplished", "Creative", "Accomplished+ S"], "prices": [10.00, 11.19, 12.99, 15.49, 19.00], "fuel": ["Petrol", "Diesel"], "segment": "Coupe SUV"},
        "Curvv EV":     {"variants": ["Creative", "Fearless", "Fearless+"], "prices": [17.49, 19.99, 21.99], "fuel": ["EV"], "segment": "Electric Coupe SUV"},
        "Harrier":      {"variants": ["Smart", "Smart+", "Pure", "Creative", "Fearless", "Fearless+"], "prices": [14.99, 16.49, 17.99, 20.99, 23.49, 26.44], "fuel": ["Petrol", "Diesel"], "segment": "Premium SUV"},
        "Safari":       {"variants": ["Smart+", "Pure+", "Creative", "Fearless", "Fearless+", "Gold"], "prices": [16.19, 18.49, 21.49, 24.49, 26.49, 27.34], "fuel": ["Petrol", "Diesel"], "segment": "3-Row SUV"},
    },

    # ── MAHINDRA ──────────────────────────────────────────────────────────────
    "Mahindra": {
        "XUV 3XO":      {"variants": ["MX1", "MX2", "MX2 Pro", "MX3", "MX3 Pro", "AX5 L", "AX7 L"], "prices": [7.99, 9.48, 10.34, 11.54, 12.49, 14.98, 15.49], "fuel": ["Petrol", "Diesel"], "segment": "SUV"},
        "Bolero":       {"variants": ["B4", "B6", "B6 Opt", "B8", "B9"], "prices": [9.80, 10.18, 10.54, 10.72, 10.98], "fuel": ["Diesel"], "segment": "SUV"},
        "Thar":         {"variants": ["AX Std", "AX (O)", "LX Petrol", "LX Diesel"], "prices": [10.99, 13.99, 15.49, 16.49], "fuel": ["Petrol", "Diesel"], "segment": "Off-Road SUV"},
        "Thar ROXX":    {"variants": ["MX1", "MX3", "AX3 L", "AX5 L", "AX7 L", "AX7 AWD L"], "prices": [12.99, 15.49, 16.99, 18.79, 20.49, 22.49], "fuel": ["Petrol", "Diesel"], "segment": "Off-Road SUV"},
        "Scorpio N":    {"variants": ["Z2", "Z4", "Z6", "Z8", "Z8 L", "Z8 AWD"], "prices": [13.85, 15.50, 18.29, 21.99, 23.49, 24.54], "fuel": ["Petrol", "Diesel"], "segment": "SUV"},
        "XUV700":       {"variants": ["MX", "AX3", "AX5", "AX7", "AX7 AWD"], "prices": [13.99, 17.99, 20.99, 24.99, 26.70], "fuel": ["Petrol", "Diesel"], "segment": "Premium SUV"},
        "BE 6":         {"variants": ["Pack One", "Pack Two", "Pack Three"], "prices": [18.90, 23.90, 26.90], "fuel": ["EV"], "segment": "Electric Coupe SUV"},
        "XEV 9e":       {"variants": ["Pack One", "Pack Two", "Pack Three"], "prices": [21.90, 26.90, 30.50], "fuel": ["EV"], "segment": "Electric SUV"},
    },

    # ── KIA ───────────────────────────────────────────────────────────────────
    "Kia": {
        "Sonet":        {"variants": ["HTE", "HTK", "HTK+", "HTX", "HTX+", "GTX+"], "prices": [7.99, 9.89, 11.75, 13.19, 15.09, 15.89], "fuel": ["Petrol", "Diesel", "CNG"], "segment": "SUV"},
        "Seltos":       {"variants": ["HTK", "HTK+", "HTX", "HTX+", "GTX", "GTX+", "X-Line"], "prices": [10.90, 13.45, 15.45, 17.29, 18.89, 20.65, 21.45], "fuel": ["Petrol", "Diesel", "CNG"], "segment": "SUV"},
        "Carens":       {"variants": ["Premium", "Premium+", "Luxury", "Luxury+", "X-Line"], "prices": [10.45, 12.59, 14.67, 17.49, 18.20], "fuel": ["Petrol", "Diesel", "CNG"], "segment": "MPV"},
        "EV6":          {"variants": ["RWD Standard", "RWD Long Range", "GT-Line AWD"], "prices": [60.97, 63.97, 65.97], "fuel": ["EV"], "segment": "Electric Sedan SUV"},
        "EV9":          {"variants": ["GT-Line", "GT-Line AWD"], "prices": [1.29 * 100, 1.39 * 100], "fuel": ["EV"], "segment": "Electric 3-Row SUV"},
    },

    # ── TOYOTA ────────────────────────────────────────────────────────────────
    "Toyota": {
        "Glanza":       {"variants": ["E", "S", "G", "V"], "prices": [6.73, 7.59, 8.47, 10.03], "fuel": ["Petrol", "CNG"], "segment": "Hatchback"},
        "Urban Cruiser Hyryder": {"variants": ["E", "S", "G", "V Hybrid", "V Hybrid AWD"], "prices": [10.73, 12.62, 14.64, 17.99, 19.44], "fuel": ["Petrol", "Hybrid"], "segment": "SUV"},
        "Innova Hycross":{"variants": ["G", "V", "VX", "ZX", "ZX(O)"], "prices": [19.77, 23.00, 26.50, 30.05, 30.60], "fuel": ["Petrol", "Hybrid"], "segment": "Premium MPV"},
        "Fortuner":     {"variants": ["4x2 MT", "4x2 AT", "Legender 4x2", "Legender 4x4"], "prices": [33.43, 37.99, 44.43, 50.31], "fuel": ["Petrol", "Diesel"], "segment": "Premium SUV"},
        "Camry Hybrid": {"variants": ["Hybrid"], "prices": [48.08], "fuel": ["Hybrid"], "segment": "Premium Sedan"},
        "Land Cruiser": {"variants": ["LC300 GX-R"], "prices": [235.00], "fuel": ["Diesel"], "segment": "Luxury SUV"},
    },

    # ── HONDA ─────────────────────────────────────────────────────────────────
    "Honda": {
        "Amaze":        {"variants": ["S MT", "S CVT", "V MT", "V CVT", "VX MT", "VX CVT"], "prices": [7.21, 8.04, 9.03, 9.88, 10.07, 11.08], "fuel": ["Petrol", "Diesel", "CNG"], "segment": "Sedan"},
        "Elevate":      {"variants": ["V MT", "V CVT", "SV MT", "SV CVT", "ZX CVT", "ZX MT"], "prices": [11.69, 13.77, 14.05, 15.15, 15.96, 16.19], "fuel": ["Petrol"], "segment": "SUV"},
        "City":         {"variants": ["V MT", "V CVT", "ZX MT", "ZX CVT"], "prices": [11.73, 13.55, 15.09, 15.97], "fuel": ["Petrol"], "segment": "Sedan"},
        "City e:HEV":   {"variants": ["ZX Hybrid"], "prices": [19.59], "fuel": ["Hybrid"], "segment": "Hybrid Sedan"},
    },

    # ── VOLKSWAGEN ────────────────────────────────────────────────────────────
    "Volkswagen": {
        "Taigun":       {"variants": ["Comfortline", "Highline", "Topline", "GT Plus Sport"], "prices": [11.69, 14.53, 17.17, 20.43], "fuel": ["Petrol"], "segment": "SUV"},
        "Virtus":       {"variants": ["Comfortline", "Highline", "Topline", "GT Plus"], "prices": [11.56, 14.12, 16.78, 19.41], "fuel": ["Petrol"], "segment": "Sedan"},
        "Tiguan":       {"variants": ["Elegance", "R-Line"], "prices": [35.17, 48.97], "fuel": ["Petrol"], "segment": "Premium SUV"},
    },

    # ── SKODA ─────────────────────────────────────────────────────────────────
    "Skoda": {
        "Kushaq":       {"variants": ["Active", "Ambition", "Style", "Monte Carlo"], "prices": [11.09, 14.39, 17.49, 19.49], "fuel": ["Petrol"], "segment": "SUV"},
        "Slavia":       {"variants": ["Active", "Ambition", "Style", "Monte Carlo"], "prices": [10.69, 14.19, 17.09, 18.49], "fuel": ["Petrol"], "segment": "Sedan"},
        "Kodiaq":       {"variants": ["Style 4x2", "Sportline 4x2"], "prices": [46.89, 48.89], "fuel": ["Petrol"], "segment": "Premium SUV"},
        "Superb":       {"variants": ["Laurin & Klement"], "prices": [54.49], "fuel": ["Petrol"], "segment": "Premium Sedan"},
    },

    # ── MG ────────────────────────────────────────────────────────────────────
    "MG": {
        "Hector":       {"variants": ["Style", "Super", "Smart Pro", "Select Pro", "Savvy Pro"], "prices": [13.99, 16.30, 18.20, 20.50, 21.99], "fuel": ["Petrol", "CNG", "Diesel"], "segment": "SUV"},
        "Windsor EV":   {"variants": ["Excite", "Essence", "Exclusive"], "prices": [13.50, 14.50, 15.50], "fuel": ["EV"], "segment": "Electric SUV"},
        "ZS EV":        {"variants": ["Excite Pro", "Essence Pro"], "prices": [18.98, 25.88], "fuel": ["EV"], "segment": "Electric SUV"},
        "Gloster":      {"variants": ["Super 2WD", "Sharp 2WD", "Savvy 2WD", "Savvy AWD"], "prices": [37.80, 40.50, 44.00, 45.00], "fuel": ["Diesel"], "segment": "Premium SUV"},
    },

    # ── JEEP ──────────────────────────────────────────────────────────────────
    "Jeep": {
        "Compass":      {"variants": ["Sport", "Longitude", "Longitude+", "Trailhawk", "Model S 4x4"], "prices": [20.49, 22.99, 25.49, 28.29, 30.39], "fuel": ["Petrol", "Diesel"], "segment": "Premium SUV"},
        "Meridian":     {"variants": ["Longitude 2WD", "Limited 4WD", "Overland 4WD"], "prices": [29.90, 33.50, 37.00], "fuel": ["Diesel"], "segment": "Premium 3-Row SUV"},
        "Wrangler":     {"variants": ["Unlimited Sport", "Unlimited Sahara", "Unlimited Rubicon"], "prices": [56.95, 62.45, 67.65], "fuel": ["Petrol"], "segment": "Off-Road SUV"},
    },

    # ── BMW ───────────────────────────────────────────────────────────────────
    "BMW": {
        "3 Series":     {"variants": ["320i Sport", "330i M Sport", "M340i"], "prices": [46.90, 57.90, 72.90], "fuel": ["Petrol"], "segment": "Luxury Sedan"},
        "5 Series":     {"variants": ["520i Luxury", "530i M Sport", "540i M Sport"], "prices": [67.90, 72.90, 81.90], "fuel": ["Petrol"], "segment": "Luxury Sedan"},
        "7 Series":     {"variants": ["740i Luxury", "740Ld Luxury", "760i xDrive"], "prices": [1.72 * 100, 1.95 * 100, 2.53 * 100], "fuel": ["Petrol", "Diesel"], "segment": "Ultra Luxury Sedan"},
        "X1":           {"variants": ["sDrive18i xLine", "sDrive18i M Sport"], "prices": [46.50, 56.90], "fuel": ["Petrol"], "segment": "Luxury SUV"},
        "X3":           {"variants": ["xDrive20i Luxury", "xDrive20d Luxury", "xDrive30i M Sport"], "prices": [69.90, 73.90, 90.90], "fuel": ["Petrol", "Diesel"], "segment": "Luxury SUV"},
        "X5":           {"variants": ["xDrive40i M Sport", "xDrive40d M Sport"], "prices": [93.90, 98.90], "fuel": ["Petrol", "Diesel"], "segment": "Luxury SUV"},
        "iX":           {"variants": ["iX xDrive40", "iX xDrive50 Sport"], "prices": [1.21 * 100, 1.40 * 100], "fuel": ["EV"], "segment": "Electric Luxury SUV"},
        "M3 Competition":{"variants": ["Competition Sedan"], "prices": [1.47 * 100], "fuel": ["Petrol"], "segment": "Performance Sedan"},
    },

    # ── MERCEDES-BENZ ─────────────────────────────────────────────────────────
    "Mercedes-Benz": {
        "A-Class":      {"variants": ["A 200 Progressive", "A 220 4MATIC AMG"], "prices": [45.50, 53.00], "fuel": ["Petrol"], "segment": "Luxury Hatchback"},
        "C-Class":      {"variants": ["C 200 Progressive", "C 220d Progressive", "C 300d AMG"], "prices": [57.00, 62.00, 68.00], "fuel": ["Petrol", "Diesel"], "segment": "Luxury Sedan"},
        "E-Class":      {"variants": ["E 200", "E 220d", "E 350d 4MATIC AMG"], "prices": [78.50, 84.50, 95.00], "fuel": ["Petrol", "Diesel"], "segment": "Luxury Sedan"},
        "S-Class":      {"variants": ["S 450d Exclusive", "S 500 Exclusive", "Maybach S 680"], "prices": [1.69 * 100, 2.20 * 100, 3.50 * 100], "fuel": ["Petrol", "Diesel"], "segment": "Ultra Luxury Sedan"},
        "GLA":          {"variants": ["GLA 200 Progressive", "GLA 220d 4MATIC AMG"], "prices": [49.90, 56.50], "fuel": ["Petrol", "Diesel"], "segment": "Luxury SUV"},
        "GLC":          {"variants": ["GLC 220d 4MATIC", "GLC 300d 4MATIC AMG"], "prices": [68.00, 80.00], "fuel": ["Diesel"], "segment": "Luxury SUV"},
        "GLE":          {"variants": ["GLE 300d 4MATIC", "GLE 450 4MATIC", "AMG GLE 53"], "prices": [97.00, 1.10 * 100, 1.50 * 100], "fuel": ["Petrol", "Diesel"], "segment": "Luxury SUV"},
        "EQS":          {"variants": ["EQS 450+", "AMG EQS 53 4MATIC+"], "prices": [1.55 * 100, 2.45 * 100], "fuel": ["EV"], "segment": "Electric Luxury Sedan"},
    },

    # ── AUDI ──────────────────────────────────────────────────────────────────
    "Audi": {
        "A4":           {"variants": ["35 TFSI Premium", "45 TFSI Technology"], "prices": [47.34, 54.65], "fuel": ["Petrol"], "segment": "Luxury Sedan"},
        "A6":           {"variants": ["45 TFSI Technology", "55 TFSI Technology"], "prices": [63.99, 73.99], "fuel": ["Petrol"], "segment": "Luxury Sedan"},
        "A8 L":         {"variants": ["55 TFSI", "60 TFSI quattro"], "prices": [1.39 * 100, 1.60 * 100], "fuel": ["Petrol"], "segment": "Ultra Luxury Sedan"},
        "Q3":           {"variants": ["35 TFSI Premium", "40 TFSI Technology"], "prices": [44.89, 52.89], "fuel": ["Petrol"], "segment": "Luxury SUV"},
        "Q5":           {"variants": ["45 TFSI Technology", "55 TFSI quattro"], "prices": [67.97, 84.15], "fuel": ["Petrol"], "segment": "Luxury SUV"},
        "Q7":           {"variants": ["45 TFSI Technology", "55 TFSI quattro"], "prices": [91.83, 1.05 * 100], "fuel": ["Petrol"], "segment": "Luxury SUV"},
        "e-tron":       {"variants": ["50 quattro Technology", "55 quattro Technology"], "prices": [1.14 * 100, 1.20 * 100], "fuel": ["EV"], "segment": "Electric Luxury SUV"},
    },

    # ── PORSCHE ───────────────────────────────────────────────────────────────
    "Porsche": {
        "Macan":        {"variants": ["Base", "S", "GTS", "Turbo"], "prices": [89.42, 1.04 * 100, 1.14 * 100, 1.38 * 100], "fuel": ["Petrol"], "segment": "Luxury SUV"},
        "Cayenne":      {"variants": ["Base", "S", "GTS", "Turbo", "Turbo GT"], "prices": [1.29 * 100, 1.47 * 100, 1.93 * 100, 2.31 * 100, 2.98 * 100], "fuel": ["Petrol"], "segment": "Luxury SUV"},
        "Panamera":     {"variants": ["4 E-Hybrid", "4S", "GTS", "Turbo S E-Hybrid"], "prices": [1.99 * 100, 2.21 * 100, 2.62 * 100, 3.38 * 100], "fuel": ["Hybrid", "Petrol"], "segment": "Luxury Sedan"},
        "911":          {"variants": ["Carrera", "Carrera S", "Targa 4", "GT3", "Turbo S"], "prices": [2.21 * 100, 2.64 * 100, 2.95 * 100, 3.79 * 100, 4.39 * 100], "fuel": ["Petrol"], "segment": "Sports Car"},
        "Taycan":       {"variants": ["RWD", "4S", "GTS", "Turbo", "Turbo S"], "prices": [1.87 * 100, 2.09 * 100, 2.30 * 100, 2.74 * 100, 3.14 * 100], "fuel": ["EV"], "segment": "Electric Luxury Sedan"},
    },

    # ── LAND ROVER ────────────────────────────────────────────────────────────
    "Land Rover": {
        "Defender":     {"variants": ["90 S", "110 S", "110 HSE", "110 X", "130 HSE"], "prices": [1.07 * 100, 1.19 * 100, 1.50 * 100, 1.98 * 100, 2.35 * 100], "fuel": ["Diesel", "Petrol"], "segment": "Luxury Off-Road"},
        "Discovery":    {"variants": ["S", "HSE", "HSE Luxury"], "prices": [98.30, 1.15 * 100, 1.45 * 100], "fuel": ["Diesel"], "segment": "Luxury SUV"},
        "Range Rover Sport": {"variants": ["Dynamic SE", "HSE Dynamic", "Autobiography"], "prices": [1.63 * 100, 1.93 * 100, 2.19 * 100], "fuel": ["Petrol", "Diesel"], "segment": "Luxury SUV"},
        "Range Rover":  {"variants": ["SE LWB", "HSE LWB", "Autobiography LWB", "SV LWB"], "prices": [2.39 * 100, 2.90 * 100, 3.65 * 100, 4.65 * 100], "fuel": ["Petrol", "Diesel"], "segment": "Ultra Luxury SUV"},
    },

    # ── VOLVO ─────────────────────────────────────────────────────────────────
    "Volvo": {
        "XC40":         {"variants": ["B4 Plus Dark", "B4 Plus", "B4 Ultimate"], "prices": [57.90, 62.90, 67.90], "fuel": ["Petrol"], "segment": "Luxury SUV"},
        "XC60":         {"variants": ["B5 Plus Dark", "B5 Plus", "B6 Ultimate"], "prices": [68.90, 73.90, 83.90], "fuel": ["Petrol"], "segment": "Luxury SUV"},
        "XC90":         {"variants": ["B6 Plus Dark", "B6 Plus 7S", "Ultimate 7S"], "prices": [1.03 * 100, 1.07 * 100, 1.15 * 100], "fuel": ["Petrol"], "segment": "Luxury 3-Row SUV"},
        "EX40":         {"variants": ["Single Motor", "Twin Motor"], "prices": [55.90, 63.90], "fuel": ["EV"], "segment": "Electric Luxury SUV"},
    },

    # ── BYD ───────────────────────────────────────────────────────────────────
    "BYD": {
        "Atto 3":       {"variants": ["Standard", "Extended Range"], "prices": [33.99, 37.99], "fuel": ["EV"], "segment": "Electric SUV"},
        "Seal":         {"variants": ["Excellence RWD", "Performance AWD"], "prices": [41.00, 53.00], "fuel": ["EV"], "segment": "Electric Sedan"},
        "eMAX 7":       {"variants": ["7-Seater"], "prices": [26.90], "fuel": ["EV"], "segment": "Electric MPV"},
    },

    # ── RENAULT ───────────────────────────────────────────────────────────────
    "Renault": {
        "Kiger":        {"variants": ["RXE", "RXL", "RXT", "RXT(O)", "RXZ", "RXZ Turbo"], "prices": [5.99, 7.49, 8.55, 9.55, 10.50, 11.23], "fuel": ["Petrol"], "segment": "SUV"},
        "Triber":       {"variants": ["RXE", "RXL", "RXT", "RXZ", "RXZ AMT"], "prices": [6.00, 6.99, 7.82, 8.65, 8.97], "fuel": ["Petrol", "CNG"], "segment": "MPV"},
    },

    # ── NISSAN ────────────────────────────────────────────────────────────────
    "Nissan": {
        "Magnite":      {"variants": ["XE", "XL", "XV", "XV Premium", "XV Premium(O)", "Turbo XV Premium(O)"], "prices": [5.99, 7.09, 8.69, 9.99, 10.99, 11.39], "fuel": ["Petrol"], "segment": "SUV"},
    },

    # ── CITROEN ───────────────────────────────────────────────────────────────
    "Citroen": {
        "C3":           {"variants": ["Live", "Feel", "Feel+", "Shine"], "prices": [6.16, 7.59, 8.42, 9.19], "fuel": ["Petrol"], "segment": "Hatchback"},
        "C3 Aircross":  {"variants": ["Feel", "Feel+ MT", "Feel+ AT", "Shine AT"], "prices": [9.99, 11.68, 13.32, 14.49], "fuel": ["Petrol"], "segment": "SUV"},
        "eC3":          {"variants": ["Feel", "Shine"], "prices": [11.50, 12.90], "fuel": ["EV"], "segment": "Electric Hatchback"},
    },
}

# 20 Best Indian Cities
CITIES = [
    "Mumbai", "Delhi", "Bengaluru", "Chennai", "Hyderabad",
    "Pune", "Kolkata", "Ahmedabad", "Jaipur", "Surat",
    "Lucknow", "Chandigarh", "Kochi", "Coimbatore", "Nagpur",
    "Indore", "Bhopal", "Visakhapatnam", "Noida", "Gurugram"
]

BRAND_SEGMENTS = {
    "Maruti Suzuki": "Volume",  "Hyundai": "Volume",    "Tata": "Volume",
    "Mahindra": "Volume",       "Kia": "Volume",         "Toyota": "Volume",
    "Honda": "Volume",          "Volkswagen": "Volume",  "Skoda": "Volume",
    "MG": "Volume",             "Jeep": "Upper",         "Renault": "Volume",
    "Nissan": "Volume",         "Citroen": "Volume",     "BYD": "Upper",
    "BMW": "Luxury",            "Mercedes-Benz": "Luxury", "Audi": "Luxury",
    "Porsche": "Ultra Luxury",  "Land Rover": "Ultra Luxury", "Volvo": "Luxury",
}

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE UI
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div style="margin-bottom:6px;">
    <span style="font-size:0.68rem;font-weight:700;letter-spacing:0.25em;text-transform:uppercase;
    color:#FF2800;font-family:'IBM Plex Mono',monospace;">01 — Vehicle Intelligence</span>
</div>
<h1 style="font-size:2.4rem;font-weight:900;letter-spacing:0.05em;margin-bottom:0;line-height:1;">
    CONFIGURE VEHICLE
</h1>
<hr style="border:none;border-top:3px solid #1A1A1A;margin:14px 0 24px 0;"/>
""", unsafe_allow_html=True)

# ── TABS for brand category ────────────────────────────────────────────────────
tab_vol, tab_upper, tab_lux, tab_ultra = st.tabs(["VOLUME BRANDS", "UPPER SEGMENT", "LUXURY", "ULTRA LUXURY"])

with tab_vol:
    vol_brands = [b for b, s in BRAND_SEGMENTS.items() if s == "Volume"]
    brand_sel_vol = st.selectbox("SELECT BRAND", vol_brands, key="vol_brand")
    selected_brand = brand_sel_vol

with tab_upper:
    upper_brands = [b for b, s in BRAND_SEGMENTS.items() if s == "Upper"]
    brand_sel_up = st.selectbox("SELECT BRAND", upper_brands, key="up_brand")
    selected_brand = brand_sel_up

with tab_lux:
    lux_brands = [b for b, s in BRAND_SEGMENTS.items() if s == "Luxury"]
    brand_sel_lux = st.selectbox("SELECT BRAND", lux_brands, key="lux_brand")
    selected_brand = brand_sel_lux

with tab_ultra:
    ultra_brands = [b for b, s in BRAND_SEGMENTS.items() if s == "Ultra Luxury"]
    brand_sel_ultra = st.selectbox("SELECT BRAND", ultra_brands, key="ultra_brand")
    selected_brand = brand_sel_ultra

# Determine active brand from widget values
active_tab_index = 0  # We'll use session state trick below
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Volume"

# Determine brand from all selectboxes (last changed wins via key priority)
# Use a combined selector approach
all_brands = sorted(VEHICLE_DB.keys())
st.markdown('<div class="section-panel">', unsafe_allow_html=True)
st.markdown('<div class="section-title">VEHICLE SELECTION</div>', unsafe_allow_html=True)

col_b, col_m, col_v = st.columns(3)

with col_b:
    brand = st.selectbox("BRAND", all_brands, index=all_brands.index("Hyundai"))

brand_data = VEHICLE_DB.get(brand, {})
models = list(brand_data.keys())

with col_m:
    model = st.selectbox("MODEL", models)

model_data = brand_data.get(model, {})
variants = model_data.get("variants", ["Standard"])
prices   = model_data.get("prices", [10.0])
seg      = model_data.get("segment", "")
fuels    = model_data.get("fuel", ["Petrol"])

with col_v:
    variant_options = [f"{v}  ·  ₹{p:.2f}L" for v, p in zip(variants, prices)]
    variant_sel = st.selectbox("VARIANT + PRICE", variant_options)
    variant_idx = variant_options.index(variant_sel)
    variant = variants[variant_idx]
    auto_price = prices[variant_idx]

# Price display
price_color = "#FF2800" if auto_price > 80 else "#1A1A1A"
st.markdown(f"""
<div style="display:flex;align-items:center;gap:16px;margin:12px 0;">
    <div style="background:#1A1A1A;color:white;padding:10px 20px;font-family:'IBM Plex Mono',monospace;font-weight:700;font-size:1.4rem;">
        ₹{auto_price:.2f}L
    </div>
    <div style="border:1.5px solid #1A1A1A;padding:4px 10px;font-size:0.7rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;">{seg}</div>
    <div style="border:1.5px solid #FF2800;color:#FF2800;padding:4px 10px;font-size:0.7rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;">{brand}</div>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── USAGE & HISTORY ──────────────────────────────────────────────────────────
st.markdown('<div class="section-panel">', unsafe_allow_html=True)
st.markdown('<div class="section-title">USAGE & HISTORY</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    mfg_year = st.selectbox("MANUFACTURING YEAR", list(range(2025, 2014, -1)))
with col2:
    current_mileage = st.number_input("CURRENT ODOMETER (KM)", min_value=0, max_value=500000,
                                       value=15000, step=500, help="Total km driven till date")
with col3:
    annual_mileage = st.slider("ANNUAL MILEAGE (KM/YR)", 3000, 60000, 12000, 1000)
with col4:
    ownership_period = st.slider("PLANNED OWNERSHIP (YRS)", 1, 12, 5, 1)

col5, col6 = st.columns(2)
with col5:
    city = st.selectbox("PRIMARY USAGE CITY", CITIES)
with col6:
    income = st.number_input("MONTHLY INCOME ₹ (OPTIONAL — for burden calc)",
                              min_value=0, max_value=50000000, value=0, step=10000,
                              help="Used only to calculate ownership burden percentage")

st.markdown('</div>', unsafe_allow_html=True)

# ── FUEL TYPE & EV SPECIFICS ─────────────────────────────────────────────────
st.markdown('<div class="section-panel">', unsafe_allow_html=True)
st.markdown('<div class="section-title">FUEL TYPE</div>', unsafe_allow_html=True)

available_fuels = fuels + (["Petrol"] if "Petrol" not in fuels else [])
available_fuels = list(dict.fromkeys(fuels))  # Deduplicate preserving order
fuel_type = st.radio("SELECT FUEL TYPE", available_fuels, horizontal=True)

if fuel_type == "EV":
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**EV BATTERY DETAILS**")
    ev1, ev2, ev3 = st.columns(3)
    with ev1:
        battery_capacity = st.number_input("BATTERY CAPACITY (kWh)", 10.0, 200.0, 40.0, 0.5)
    with ev2:
        charging_freq = st.selectbox("CHARGING FREQUENCY", ["Daily", "Every 2-3 Days", "Weekly", "Rarely"])
    with ev3:
        fast_charge_pct = st.slider("FAST CHARGING %", 0, 100, 20,
                                     help="% of charging sessions that use DC fast chargers")
    battery_capacity = battery_capacity
else:
    battery_capacity, charging_freq, fast_charge_pct = None, None, 0

st.markdown('</div>', unsafe_allow_html=True)

# ── FINANCING ────────────────────────────────────────────────────────────────
st.markdown('<div class="section-panel">', unsafe_allow_html=True)
st.markdown('<div class="section-title">FINANCING</div>', unsafe_allow_html=True)

fin1, fin2, fin3, fin4 = st.columns(4)
with fin1:
    purchase_price_override = st.number_input("FINAL ON-ROAD PRICE (₹L)",
                                               min_value=1.0, max_value=600.0,
                                               value=round(auto_price * 1.10, 2), step=0.10,
                                               help="Ex-showroom × ~1.10 for on-road (RTO + insurance)")
with fin2:
    down_payment_pct = st.slider("DOWN PAYMENT %", 0, 100, 20, 5)
with fin3:
    loan_rate = st.slider("LOAN INTEREST RATE %", 6.0, 20.0, 9.0, 0.25)
with fin4:
    tenure_months = st.selectbox("LOAN TENURE", [12, 24, 36, 48, 60, 72, 84], index=4,
                                  format_func=lambda x: f"{x} months ({x//12} yr{'' if x//12==1 else 's'})")

# Live EMI preview
if loan_rate > 0 and tenure_months > 0 and down_payment_pct < 100:
    principal = purchase_price_override * (1 - down_payment_pct/100) * 100000
    r = loan_rate / (12 * 100)
    emi = principal * r * (1 + r)**tenure_months / ((1 + r)**tenure_months - 1)
    total_interest = emi * tenure_months - principal
    st.markdown(f"""
    <div style="display:flex;gap:24px;margin-top:12px;padding:14px 18px;background:#1A1A1A;color:white;">
        <div>
            <div style="font-size:0.65rem;letter-spacing:0.2em;opacity:0.7;">MONTHLY EMI</div>
            <div style="font-family:'IBM Plex Mono',monospace;font-size:1.4rem;font-weight:700;color:#FF2800;">
                ₹{emi:,.0f}
            </div>
        </div>
        <div>
            <div style="font-size:0.65rem;letter-spacing:0.2em;opacity:0.7;">LOAN AMOUNT</div>
            <div style="font-family:'IBM Plex Mono',monospace;font-size:1.4rem;font-weight:700;">
                ₹{principal/100000:.2f}L
            </div>
        </div>
        <div>
            <div style="font-size:0.65rem;letter-spacing:0.2em;opacity:0.7;">TOTAL INTEREST</div>
            <div style="font-family:'IBM Plex Mono',monospace;font-size:1.4rem;font-weight:700;">
                ₹{total_interest/100000:.2f}L
            </div>
        </div>
        <div>
            <div style="font-size:0.65rem;letter-spacing:0.2em;opacity:0.7;">DOWN PAYMENT</div>
            <div style="font-family:'IBM Plex Mono',monospace;font-size:1.4rem;font-weight:700;">
                ₹{purchase_price_override * down_payment_pct/100:.2f}L
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── ANALYZE BUTTON ────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)

if st.button("ANALYZE VEHICLE  →", use_container_width=True, type="primary"):
    if model == "" or brand == "":
        st.error("Please select a brand and model.")
    else:
        st.session_state.vehicle_data = {
            "brand": brand,
            "model": model,
            "variant": variant,
            "fuel_type": fuel_type,
            "segment": seg,
            "purchase_price": purchase_price_override,
            "ex_showroom_price": auto_price,
            "mfg_year": mfg_year,
            "current_mileage": current_mileage,
            "annual_mileage": annual_mileage,
            "ownership_period": ownership_period,
            "city": city,
            "income": income,
            "battery_capacity": battery_capacity,
            "charging_freq": charging_freq,
            "fast_charge_pct": fast_charge_pct if fuel_type == "EV" else 0,
            "down_payment_pct": down_payment_pct,
            "loan_rate": loan_rate,
            "tenure_months": tenure_months,
        }
        st.success(f"✓ {brand} {model} {variant} configured. Proceeding to Health Analysis...")
        st.balloons()
        st.switch_page("pages/02_Vehicle_Health.py")
