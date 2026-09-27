# -*- coding: utf-8 -*-
"""
01 Vehicle Input — AUTOVAULT AI
UX Principles Applied: Affordances · Signifiers · Visual Hierarchy ·
8px Grid · Typography Scale · Color Theory · Shadows · Micro/Macro Interactions
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st

st.set_page_config(
    page_title="Vehicle Input | AUTOVAULT AI",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Load global design system ─────────────────────────────────────────────────
css_path = Path(__file__).parent.parent / "styles" / "brutalist.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

# ── Additional page-specific micro-interaction styles ─────────────────────────
st.markdown("""
<style>
/* Animated selected state for brand card */
.brand-selected {
  border-color: var(--c-red) !important;
  box-shadow: var(--shadow-red) !important;
  transform: translate(-2px,-2px);
}

/* Sticky bottom bar */
.sticky-cta {
  position: fixed;
  bottom: 0; left: 0; right: 0;
  background: var(--c-ink);
  border-top: 3px solid var(--c-red);
  padding: 14px 48px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  z-index: 999;
  gap: 24px;
}
.sticky-vehicle-name {
  font-family: var(--font-mono);
  font-size: var(--text-sm);
  font-weight: 700;
  color: rgba(255,255,255,0.6);
  letter-spacing: 0.1em;
  text-transform: uppercase;
}
.sticky-price {
  font-family: var(--font-mono);
  font-size: var(--text-lg);
  font-weight: 700;
  color: var(--c-red);
}
/* Spacer for sticky bar */
.sticky-spacer { height: 80px; }

/* Completion ring */
.completion-ring {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: 700;
  letter-spacing: 0.15em;
  color: var(--c-text-muted);
}

/* Number chip */
.n-chip {
  background: var(--c-ink);
  color: white;
  width: 28px; height: 28px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: 700;
  flex-shrink: 0;
}
.n-chip.done { background: var(--c-red); }

/* Fuel type visual buttons */
.fuel-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 8px;
  margin: 12px 0;
}
.fuel-btn {
  background: white;
  border: 2px solid var(--c-border);
  padding: 14px 8px;
  text-align: center;
  cursor: pointer;
  transition: all 120ms var(--ease);
  box-shadow: 2px 2px 0 var(--c-border);
}
.fuel-btn:hover {
  background: var(--c-ink);
  color: white;
  transform: translate(-1px,-1px);
  box-shadow: 3px 3px 0 var(--c-red);
}
.fuel-btn.sel {
  background: var(--c-ink);
  color: white;
  border-color: var(--c-red);
  box-shadow: 3px 3px 0 var(--c-red);
}
.fuel-icon { font-size: 1.5rem; display: block; margin-bottom: 4px; }
.fuel-label {
  font-family: var(--font-mono);
  font-size: 0.6rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════════════════════

VEHICLE_DB = {
    "Maruti Suzuki": {
        "Alto K10":     {"v": ["STD","LXI","VXI","ZXI","ZXI+"],                        "p": [3.99,4.26,4.79,5.45,5.83],          "f": ["Petrol","CNG"],          "seg": "Hatchback"},
        "Swift":        {"v": ["LXI","VXI","ZXI","ZXI+"],                               "p": [6.49,7.49,8.49,9.64],               "f": ["Petrol","CNG"],          "seg": "Hatchback"},
        "Baleno":       {"v": ["Sigma","Delta","Zeta","Alpha"],                          "p": [6.61,7.45,8.45,9.88],               "f": ["Petrol","CNG"],          "seg": "Hatchback"},
        "Dzire":        {"v": ["LXI","VXI","ZXI","ZXI+"],                               "p": [6.79,7.81,8.85,9.93],               "f": ["Petrol","CNG"],          "seg": "Sedan"},
        "Fronx":        {"v": ["Sigma","Delta","Delta+","Zeta","Alpha"],                 "p": [7.51,8.97,10.04,11.41,13.06],       "f": ["Petrol","CNG"],          "seg": "Coupe SUV"},
        "Brezza":       {"v": ["LXI","VXI","ZXI","ZXI+","ZXI+ Dual Tone"],              "p": [8.34,10.49,12.52,14.14,14.58],      "f": ["Petrol","CNG"],          "seg": "SUV"},
        "Ertiga":       {"v": ["LXI","VXI","ZXI","ZXI+"],                               "p": [8.69,10.44,12.09,13.08],            "f": ["Petrol","CNG"],          "seg": "MPV"},
        "Grand Vitara": {"v": ["Sigma","Delta","Zeta","Alpha","Alpha+ Hybrid"],          "p": [10.70,13.45,16.45,18.99,19.99],     "f": ["Petrol","Hybrid"],       "seg": "SUV"},
        "Jimny":        {"v": ["Zeta","Alpha"],                                          "p": [12.74,15.05],                       "f": ["Petrol"],                "seg": "Off-Road SUV"},
    },
    "Hyundai": {
        "i20":          {"v": ["Era","Magna","Sportz","Asta","Asta (O)"],                 "p": [7.04,8.27,9.84,11.12,12.10],        "f": ["Petrol","Diesel","CNG"], "seg": "Hatchback"},
        "Venue":        {"v": ["E","S","S+","SX","SX+","SX(O)"],                        "p": [7.94,9.53,10.47,12.08,13.12,13.57], "f": ["Petrol","Diesel","CNG"], "seg": "SUV"},
        "Creta":        {"v": ["E","EX","S","S+","SX","SX(O)"],                         "p": [11.00,12.50,14.25,16.50,18.75,20.15],"f": ["Petrol","Diesel","CNG"],"seg": "SUV"},
        "Creta Electric":{"v":["Executive","Smart","Smart+","Prime","Prime+","Excellence"],"p":[17.99,18.99,19.89,21.40,22.60,23.50],"f":["EV"],                   "seg": "Electric SUV"},
        "Alcazar":      {"v": ["Prestige","Prestige(O)","Platinum","Signature","Signature(O)"],"p":[14.99,16.77,18.18,20.17,21.45],"f": ["Petrol","Diesel"],       "seg": "3-Row SUV"},
        "Tucson":       {"v": ["Platinum","Signature 2WD","Signature AWD"],             "p": [26.93,32.25,34.59],                 "f": ["Petrol","Diesel"],       "seg": "Premium SUV"},
        "Ioniq 5":      {"v": ["RWD Standard","RWD Long Range","AWD Long Range"],       "p": [44.95,46.95,60.45],                 "f": ["EV"],                    "seg": "Electric SUV"},
    },
    "Tata": {
        "Tiago":        {"v": ["XE","XM","XM+","XT","XZ","XZ+"],                        "p": [5.60,6.20,6.75,7.25,8.10,8.45],     "f": ["Petrol","CNG"],          "seg": "Hatchback"},
        "Punch":        {"v": ["Pure","Adventure","Accomplished","Creative"],            "p": [6.13,7.49,8.49,10.20],              "f": ["Petrol","CNG"],          "seg": "Micro SUV"},
        "Tiago EV":     {"v": ["XT","XZ","XZ+","XZ+ Tech LR"],                          "p": [8.69,9.99,11.49,12.04],             "f": ["EV"],                    "seg": "Electric Hatchback"},
        "Punch EV":     {"v": ["Smart","Smart+","Adventure","Empowered","Empowered+"],  "p": [10.99,11.99,13.49,14.49,15.49],     "f": ["EV"],                    "seg": "Electric Micro SUV"},
        "Nexon":        {"v": ["Smart","Smart+","Pure","Creative","Fearless","Fearless+"],"p":[8.10,9.30,10.49,12.99,14.29,15.50],"f": ["Petrol","Diesel","CNG"], "seg": "SUV"},
        "Nexon EV":     {"v": ["Smart","Smart+","Creative","Fearless","Fearless+"],     "p": [12.49,13.99,15.49,17.49,19.00],     "f": ["EV"],                    "seg": "Electric SUV"},
        "Curvv":        {"v": ["Smart","Smart+","Accomplished","Creative","Accomplished+ S"],"p":[10.00,11.19,12.99,15.49,19.00], "f": ["Petrol","Diesel"],       "seg": "Coupe SUV"},
        "Curvv EV":     {"v": ["Creative","Fearless","Fearless+"],                      "p": [17.49,19.99,21.99],                 "f": ["EV"],                    "seg": "Electric Coupe SUV"},
        "Harrier":      {"v": ["Smart","Smart+","Pure","Creative","Fearless","Fearless+"],"p":[14.99,16.49,17.99,20.99,23.49,26.44],"f":["Petrol","Diesel"],      "seg": "Premium SUV"},
        "Safari":       {"v": ["Smart+","Pure+","Creative","Fearless","Fearless+","Gold"],"p":[16.19,18.49,21.49,24.49,26.49,27.34],"f":["Petrol","Diesel"],      "seg": "3-Row SUV"},
    },
    "Mahindra": {
        "XUV 3XO":      {"v": ["MX1","MX2","MX2 Pro","MX3","MX3 Pro","AX5 L","AX7 L"],"p": [7.99,9.48,10.34,11.54,12.49,14.98,15.49],"f":["Petrol","Diesel"],  "seg": "SUV"},
        "Thar ROXX":    {"v": ["MX1","MX3","AX3 L","AX5 L","AX7 L","AX7 AWD L"],      "p": [12.99,15.49,16.99,18.79,20.49,22.49],   "f": ["Petrol","Diesel"],   "seg": "Off-Road SUV"},
        "Scorpio N":    {"v": ["Z2","Z4","Z6","Z8","Z8 L","Z8 AWD"],                   "p": [13.85,15.50,18.29,21.99,23.49,24.54],   "f": ["Petrol","Diesel"],   "seg": "SUV"},
        "XUV700":       {"v": ["MX","AX3","AX5","AX7","AX7 AWD"],                      "p": [13.99,17.99,20.99,24.99,26.70],          "f": ["Petrol","Diesel"],   "seg": "Premium SUV"},
        "BE 6":         {"v": ["Pack One","Pack Two","Pack Three"],                     "p": [18.90,23.90,26.90],                      "f": ["EV"],                "seg": "Electric Coupe SUV"},
        "XEV 9e":       {"v": ["Pack One","Pack Two","Pack Three"],                     "p": [21.90,26.90,30.50],                      "f": ["EV"],                "seg": "Electric SUV"},
    },
    "Kia": {
        "Sonet":        {"v": ["HTE","HTK","HTK+","HTX","HTX+","GTX+"],                 "p": [7.99,9.89,11.75,13.19,15.09,15.89],  "f": ["Petrol","Diesel","CNG"],"seg": "SUV"},
        "Seltos":       {"v": ["HTK","HTK+","HTX","HTX+","GTX","GTX+","X-Line"],        "p": [10.90,13.45,15.45,17.29,18.89,20.65,21.45],"f":["Petrol","Diesel","CNG"],"seg":"SUV"},
        "Carens":       {"v": ["Premium","Premium+","Luxury","Luxury+","X-Line"],       "p": [10.45,12.59,14.67,17.49,18.20],      "f": ["Petrol","Diesel","CNG"],"seg": "MPV"},
        "EV6":          {"v": ["RWD Standard","RWD Long Range","GT-Line AWD"],          "p": [60.97,63.97,65.97],                  "f": ["EV"],                   "seg": "Electric GT"},
    },
    "Toyota": {
        "Glanza":       {"v": ["E","S","G","V"],                                        "p": [6.73,7.59,8.47,10.03],    "f": ["Petrol","CNG"],   "seg": "Hatchback"},
        "Hyryder":      {"v": ["E","S","G","V Hybrid","V Hybrid AWD"],                  "p": [10.73,12.62,14.64,17.99,19.44],"f":["Petrol","Hybrid"],"seg": "SUV"},
        "Innova Hycross":{"v":["G","V","VX","ZX","ZX(O)"],                              "p": [19.77,23.00,26.50,30.05,30.60],"f":["Petrol","Hybrid"],"seg": "Premium MPV"},
        "Fortuner":     {"v": ["4x2 MT","4x2 AT","Legender 4x2","Legender 4x4"],       "p": [33.43,37.99,44.43,50.31], "f": ["Petrol","Diesel"],"seg": "Premium SUV"},
        "Camry Hybrid": {"v": ["Hybrid"],                                               "p": [48.08],                   "f": ["Hybrid"],         "seg": "Executive Sedan"},
    },
    "Honda": {
        "Amaze":        {"v": ["S MT","S CVT","V MT","V CVT","VX CVT"],                "p": [7.21,8.04,9.03,9.88,11.08],  "f": ["Petrol","Diesel","CNG"],"seg": "Sedan"},
        "Elevate":      {"v": ["V MT","V CVT","SV CVT","ZX CVT","ZX MT"],              "p": [11.69,13.77,15.15,15.96,16.19],"f":["Petrol"],           "seg": "SUV"},
        "City":         {"v": ["V MT","V CVT","ZX MT","ZX CVT"],                       "p": [11.73,13.55,15.09,15.97],   "f": ["Petrol"],            "seg": "Sedan"},
        "City e:HEV":   {"v": ["ZX Hybrid"],                                           "p": [19.59],                     "f": ["Hybrid"],            "seg": "Hybrid Sedan"},
    },
    "Volkswagen": {
        "Taigun":       {"v": ["Comfortline","Highline","Topline","GT Plus Sport"],     "p": [11.69,14.53,17.17,20.43],   "f": ["Petrol"],  "seg": "SUV"},
        "Virtus":       {"v": ["Comfortline","Highline","Topline","GT Plus"],           "p": [11.56,14.12,16.78,19.41],   "f": ["Petrol"],  "seg": "Sedan"},
        "Tiguan":       {"v": ["Elegance","R-Line"],                                   "p": [35.17,48.97],               "f": ["Petrol"],  "seg": "Premium SUV"},
    },
    "Skoda": {
        "Kushaq":       {"v": ["Active","Ambition","Style","Monte Carlo"],              "p": [11.09,14.39,17.49,19.49],   "f": ["Petrol"],  "seg": "SUV"},
        "Slavia":       {"v": ["Active","Ambition","Style","Monte Carlo"],              "p": [10.69,14.19,17.09,18.49],   "f": ["Petrol"],  "seg": "Sedan"},
        "Kodiaq":       {"v": ["Style 4x2","Sportline 4x2"],                           "p": [46.89,48.89],               "f": ["Petrol"],  "seg": "Premium SUV"},
        "Superb":       {"v": ["Laurin & Klement"],                                    "p": [54.49],                     "f": ["Petrol"],  "seg": "Premium Sedan"},
    },
    "MG": {
        "Hector":       {"v": ["Style","Super","Smart Pro","Select Pro","Savvy Pro"],   "p": [13.99,16.30,18.20,20.50,21.99],"f":["Petrol","CNG","Diesel"],"seg":"SUV"},
        "Windsor EV":   {"v": ["Excite","Essence","Exclusive"],                        "p": [13.50,14.50,15.50],          "f": ["EV"],  "seg": "Electric SUV"},
        "ZS EV":        {"v": ["Excite Pro","Essence Pro"],                            "p": [18.98,25.88],                "f": ["EV"],  "seg": "Electric SUV"},
        "Gloster":      {"v": ["Super 2WD","Sharp 2WD","Savvy 2WD","Savvy AWD"],       "p": [37.80,40.50,44.00,45.00],    "f": ["Diesel"],"seg": "Premium SUV"},
    },
    "Jeep": {
        "Compass":      {"v": ["Sport","Longitude","Longitude+","Trailhawk","Model S 4x4"],"p":[20.49,22.99,25.49,28.29,30.39],"f":["Petrol","Diesel"],"seg":"Premium SUV"},
        "Meridian":     {"v": ["Longitude 2WD","Limited 4WD","Overland 4WD"],          "p": [29.90,33.50,37.00],  "f": ["Diesel"],  "seg": "Premium 3-Row SUV"},
        "Wrangler":     {"v": ["Unlimited Sport","Unlimited Sahara","Unlimited Rubicon"],"p":[56.95,62.45,67.65],"f": ["Petrol"],   "seg": "Off-Road Icon"},
    },
    "BMW": {
        "3 Series":      {"v": ["320i Sport","330i M Sport","M340i"],                  "p": [46.90,57.90,72.90],   "f": ["Petrol"],         "seg": "Luxury Sedan"},
        "5 Series":      {"v": ["520i Luxury","530i M Sport","M550i xDrive"],          "p": [67.90,72.90,1.05*100],"f": ["Petrol"],         "seg": "Executive Sedan"},
        "7 Series":      {"v": ["740i Luxury","740Ld Luxury","760i xDrive"],           "p": [1.72*100,1.95*100,2.53*100],"f":["Petrol","Diesel"],"seg": "Ultra Luxury Sedan"},
        "X1":            {"v": ["sDrive18i xLine","sDrive18i M Sport"],                "p": [46.50,56.90],         "f": ["Petrol"],         "seg": "Luxury SUV"},
        "X3":            {"v": ["xDrive20i Luxury","xDrive20d Luxury","xDrive30i M Sport"],"p":[69.90,73.90,90.90],"f":["Petrol","Diesel"],"seg": "Luxury SUV"},
        "X5":            {"v": ["xDrive40i M Sport","xDrive40d M Sport"],              "p": [93.90,98.90],         "f": ["Petrol","Diesel"],"seg": "Luxury SUV"},
        "iX":            {"v": ["iX xDrive40","iX xDrive50 Sport"],                   "p": [1.21*100,1.40*100],   "f": ["EV"],             "seg": "Electric Luxury SUV"},
        "M3 Competition":{"v": ["Competition Sedan"],                                  "p": [1.47*100],            "f": ["Petrol"],         "seg": "Performance Sedan"},
    },
    "Mercedes-Benz": {
        "A-Class":       {"v": ["A 200 Progressive","A 220 4MATIC AMG"],               "p": [45.50,53.00],         "f": ["Petrol"],  "seg": "Luxury Hatchback"},
        "C-Class":       {"v": ["C 200 Progressive","C 220d Progressive","C 300d AMG"],"p": [57.00,62.00,68.00],  "f": ["Petrol","Diesel"],"seg": "Luxury Sedan"},
        "E-Class":       {"v": ["E 200","E 220d","E 350d 4MATIC AMG"],                 "p": [78.50,84.50,95.00],  "f": ["Petrol","Diesel"],"seg": "Executive Sedan"},
        "S-Class":       {"v": ["S 450d Exclusive","S 500 Exclusive","Maybach S 680"],"p": [1.69*100,2.20*100,3.50*100],"f":["Petrol","Diesel"],"seg":"Ultra Luxury Sedan"},
        "GLA":           {"v": ["GLA 200 Progressive","GLA 220d 4MATIC AMG"],         "p": [49.90,56.50],         "f": ["Petrol","Diesel"],"seg": "Luxury SUV"},
        "GLC":           {"v": ["GLC 220d 4MATIC","GLC 300d 4MATIC AMG"],             "p": [68.00,80.00],         "f": ["Diesel"],  "seg": "Luxury SUV"},
        "GLE":           {"v": ["GLE 300d 4MATIC","GLE 450 4MATIC","AMG GLE 53"],     "p": [97.00,1.10*100,1.50*100],"f":["Petrol","Diesel"],"seg":"Luxury SUV"},
        "EQS":           {"v": ["EQS 450+","AMG EQS 53 4MATIC+"],                     "p": [1.55*100,2.45*100],   "f": ["EV"],      "seg": "Electric Luxury Sedan"},
    },
    "Audi": {
        "A4":            {"v": ["35 TFSI Premium","45 TFSI Technology"],               "p": [47.34,54.65],         "f": ["Petrol"],  "seg": "Luxury Sedan"},
        "A6":            {"v": ["45 TFSI Technology","55 TFSI Technology"],            "p": [63.99,73.99],         "f": ["Petrol"],  "seg": "Executive Sedan"},
        "A8 L":          {"v": ["55 TFSI","60 TFSI quattro"],                          "p": [1.39*100,1.60*100],   "f": ["Petrol"],  "seg": "Ultra Luxury Sedan"},
        "Q3":            {"v": ["35 TFSI Premium","40 TFSI Technology"],               "p": [44.89,52.89],         "f": ["Petrol"],  "seg": "Luxury SUV"},
        "Q5":            {"v": ["45 TFSI Technology","55 TFSI quattro"],               "p": [67.97,84.15],         "f": ["Petrol"],  "seg": "Luxury SUV"},
        "Q7":            {"v": ["45 TFSI Technology","55 TFSI quattro"],               "p": [91.83,1.05*100],      "f": ["Petrol"],  "seg": "Luxury SUV"},
        "e-tron":        {"v": ["50 quattro Technology","55 quattro Technology"],      "p": [1.14*100,1.20*100],   "f": ["EV"],      "seg": "Electric Luxury SUV"},
    },
    "Porsche": {
        "Macan":         {"v": ["Base","S","GTS","Turbo"],                             "p": [89.42,1.04*100,1.14*100,1.38*100],"f":["Petrol"],"seg":"Luxury SUV"},
        "Cayenne":       {"v": ["Base","S","GTS","Turbo","Turbo GT"],                  "p": [1.29*100,1.47*100,1.93*100,2.31*100,2.98*100],"f":["Petrol"],"seg":"Luxury SUV"},
        "Panamera":      {"v": ["4 E-Hybrid","4S","GTS","Turbo S E-Hybrid"],           "p": [1.99*100,2.21*100,2.62*100,3.38*100],"f":["Hybrid","Petrol"],"seg":"Luxury Sedan"},
        "911":           {"v": ["Carrera","Carrera S","Targa 4","GT3","Turbo S"],      "p": [2.21*100,2.64*100,2.95*100,3.79*100,4.39*100],"f":["Petrol"],"seg":"Sports Car"},
        "Taycan":        {"v": ["RWD","4S","GTS","Turbo","Turbo S"],                   "p": [1.87*100,2.09*100,2.30*100,2.74*100,3.14*100],"f":["EV"],"seg":"Electric Luxury Sedan"},
    },
    "Land Rover": {
        "Defender":      {"v": ["90 S","110 S","110 HSE","110 X","130 HSE"],           "p": [1.07*100,1.19*100,1.50*100,1.98*100,2.35*100],"f":["Diesel","Petrol"],"seg":"Luxury Off-Road"},
        "Discovery":     {"v": ["S","HSE","HSE Luxury"],                               "p": [98.30,1.15*100,1.45*100],"f":["Diesel"],"seg": "Luxury SUV"},
        "Range Rover Sport":{"v":["Dynamic SE","HSE Dynamic","Autobiography"],         "p": [1.63*100,1.93*100,2.19*100],"f":["Petrol","Diesel"],"seg":"Luxury SUV"},
        "Range Rover":   {"v": ["SE LWB","HSE LWB","Autobiography LWB","SV LWB"],     "p": [2.39*100,2.90*100,3.65*100,4.65*100],"f":["Petrol","Diesel"],"seg":"Ultra Luxury SUV"},
    },
    "Volvo": {
        "XC40":          {"v": ["B4 Plus Dark","B4 Plus","B4 Ultimate"],               "p": [57.90,62.90,67.90],   "f": ["Petrol"],  "seg": "Luxury SUV"},
        "XC60":          {"v": ["B5 Plus Dark","B5 Plus","B6 Ultimate"],               "p": [68.90,73.90,83.90],   "f": ["Petrol"],  "seg": "Luxury SUV"},
        "XC90":          {"v": ["B6 Plus Dark","B6 Plus 7S","Ultimate 7S"],            "p": [1.03*100,1.07*100,1.15*100],"f":["Petrol"],"seg":"Luxury 3-Row SUV"},
        "EX40":          {"v": ["Single Motor","Twin Motor"],                          "p": [55.90,63.90],         "f": ["EV"],      "seg": "Electric Luxury SUV"},
    },
    "BYD": {
        "Atto 3":        {"v": ["Standard","Extended Range"],                          "p": [33.99,37.99],         "f": ["EV"],  "seg": "Electric SUV"},
        "Seal":          {"v": ["Excellence RWD","Performance AWD"],                   "p": [41.00,53.00],         "f": ["EV"],  "seg": "Electric Sedan"},
        "eMAX 7":        {"v": ["7-Seater"],                                           "p": [26.90],               "f": ["EV"],  "seg": "Electric MPV"},
    },
    "Renault": {
        "Kiger":         {"v": ["RXE","RXL","RXT","RXT(O)","RXZ","RXZ Turbo"],        "p": [5.99,7.49,8.55,9.55,10.50,11.23],"f":["Petrol"],"seg": "SUV"},
        "Triber":        {"v": ["RXE","RXL","RXT","RXZ","RXZ AMT"],                   "p": [6.00,6.99,7.82,8.65,8.97],"f":["Petrol","CNG"],"seg": "MPV"},
    },
    "Nissan": {
        "Magnite":       {"v": ["XE","XL","XV","XV Premium","XV Premium(O)","Turbo XV Premium(O)"],"p":[5.99,7.09,8.69,9.99,10.99,11.39],"f":["Petrol"],"seg":"SUV"},
    },
    "Citroen": {
        "C3":            {"v": ["Live","Feel","Feel+","Shine"],                        "p": [6.16,7.59,8.42,9.19],  "f": ["Petrol"],  "seg": "Hatchback"},
        "C3 Aircross":   {"v": ["Feel","Feel+ MT","Feel+ AT","Shine AT"],              "p": [9.99,11.68,13.32,14.49],"f":["Petrol"],  "seg": "SUV"},
        "eC3":           {"v": ["Feel","Shine"],                                       "p": [11.50,12.90],          "f": ["EV"],      "seg": "Electric Hatchback"},
    },
}

CITIES = [
    "Mumbai","Delhi","Bengaluru","Chennai","Hyderabad",
    "Pune","Kolkata","Ahmedabad","Jaipur","Surat",
    "Lucknow","Chandigarh","Kochi","Coimbatore","Nagpur",
    "Indore","Bhopal","Visakhapatnam","Noida","Gurugram"
]

BRAND_TIER = {
    "Maruti Suzuki":"Volume","Hyundai":"Volume","Tata":"Volume","Mahindra":"Volume",
    "Kia":"Volume","Toyota":"Volume","Honda":"Volume","Volkswagen":"Volume",
    "Skoda":"Volume","MG":"Volume","Renault":"Volume","Nissan":"Volume","Citroen":"Volume",
    "Jeep":"Upper","BYD":"Upper",
    "BMW":"Luxury","Mercedes-Benz":"Luxury","Audi":"Luxury","Volvo":"Luxury",
    "Porsche":"Ultra Luxury","Land Rover":"Ultra Luxury",
}

FUEL_ICONS = {"Petrol":"⛽","Diesel":"🛢️","CNG":"🌿","EV":"⚡","Hybrid":"🔋"}

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE LAYOUT
# ═══════════════════════════════════════════════════════════════════════════════

# ── Breadcrumb ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="av-breadcrumb">
    <span>AUTOVAULT AI</span>
    <span class="sep">/</span>
    <span class="active">01 · VEHICLE INPUT</span>
</div>
""", unsafe_allow_html=True)

# ── Page header ───────────────────────────────────────────────────────────────
col_head, col_tip = st.columns([3, 1])
with col_head:
    st.markdown("""
    <h1>Configure Vehicle</h1>
    <p style="color:var(--c-text-muted);font-size:0.9rem;margin-top:4px;">
    Fill in each section below. Your analysis updates live as you select.
    All prices are 2025 ex-showroom (India).
    </p>
    """, unsafe_allow_html=True)
with col_tip:
    st.info("💡 **Tip:** Select a variant — the exact price fills automatically. Override with your on-road quote in the Finance section.")

st.markdown("<hr/>", unsafe_allow_html=True)

# ── Step indicator ────────────────────────────────────────────────────────────
st.markdown("""
<div class="step-bar">
    <div class="step-item active">
        <span class="step-num">1</span> VEHICLE SELECTION
    </div>
    <div class="step-item">
        <span class="step-num">2</span> USAGE & HISTORY
    </div>
    <div class="step-item">
        <span class="step-num">3</span> FUEL TYPE
    </div>
    <div class="step-item">
        <span class="step-num">4</span> FINANCING
    </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — VEHICLE SELECTION
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="av-panel-head" style="margin-bottom:16px;">
    <div class="av-panel-icon red">🚗</div>
    <div>
        <div class="av-panel-title">STEP 01</div>
        <div class="av-panel-subtitle">Vehicle Selection</div>
    </div>
</div>
""", unsafe_allow_html=True)

all_brands = sorted(VEHICLE_DB.keys())

# Brand tier tabs for navigation
t1, t2, t3, t4 = st.tabs(["⚡ VOLUME  (₹4L–₹25L)", "🔥 UPPER  (₹20L–₹70L)", "💎 LUXURY  (₹45L–₹1.2Cr)", "👑 ULTRA LUXURY  (₹90L+)"])

with t1:
    vb = [b for b,s in BRAND_TIER.items() if s=="Volume"]
    _bv = st.selectbox("BRAND", vb, key="tab_vol")
with t2:
    ub = [b for b,s in BRAND_TIER.items() if s=="Upper"]
    _bu = st.selectbox("BRAND", ub, key="tab_up")
with t3:
    lb = [b for b,s in BRAND_TIER.items() if s=="Luxury"]
    _bl = st.selectbox("BRAND", lb, key="tab_lux")
with t4:
    ulb = [b for b,s in BRAND_TIER.items() if s=="Ultra Luxury"]
    _bul = st.selectbox("BRAND", ulb, key="tab_ultra")

st.markdown("<hr style='margin:8px 0 20px 0;'/>", unsafe_allow_html=True)

# Master brand picker + model + variant
c1, c2, c3 = st.columns([1, 1, 1])

with c1:
    st.markdown("**BRAND** &nbsp;<span class='av-hint'>?</span>", unsafe_allow_html=True)
    brand = st.selectbox("Brand", all_brands, index=all_brands.index("Hyundai"),
                         label_visibility="collapsed", help="Select manufacturer")

brand_data = VEHICLE_DB.get(brand, {})
models = list(brand_data.keys())

with c2:
    st.markdown("**MODEL** &nbsp;<span class='av-hint'>?</span>", unsafe_allow_html=True)
    model = st.selectbox("Model", models, label_visibility="collapsed",
                         help="Model selection updates available variants and prices")

mdata    = brand_data.get(model, {})
variants = mdata.get("v", ["Standard"])
prices   = mdata.get("p", [10.0])
seg      = mdata.get("seg", "")
fuels    = mdata.get("f", ["Petrol"])

with c3:
    st.markdown("**VARIANT &amp; PRICE** &nbsp;<span class='av-hint' title='Price is 2025 ex-showroom. Your on-road price will be higher by ~8–12%.'>?</span>", unsafe_allow_html=True)
    variant_opts = [f"{v}  ·  ₹{p:.2f}L" for v, p in zip(variants, prices)]
    variant_sel  = st.selectbox("Variant", variant_opts, label_visibility="collapsed",
                                 help="Price shown is ex-showroom (2025). Override with actual on-road in Finance section.")
    vi           = variant_opts.index(variant_sel)
    variant      = variants[vi]
    auto_price   = prices[vi]

# Price banner
tier = BRAND_TIER.get(brand, "Volume")
tier_colors = {"Volume":"#1A1A1A","Upper":"#5B4FCF","Luxury":"#B8860B","Ultra Luxury":"#8B0000"}
tier_color  = tier_colors.get(tier,"#1A1A1A")

st.markdown(f"""
<div class="av-price-display">
    <div>
        <div style="font-family:var(--font-mono);font-size:0.65rem;font-weight:700;letter-spacing:0.2em;color:rgba(255,255,255,0.5);margin-bottom:4px;">EX-SHOWROOM PRICE</div>
        <div class="av-price-main">₹<span class="av-price-red">{auto_price:.2f}</span>L</div>
    </div>
    <div style="border-left:1px solid rgba(255,255,255,0.2);padding-left:24px;display:flex;flex-direction:column;gap:8px;">
        <span class="av-tag av-tag-white">{seg}</span>
        <span class="av-tag av-tag-outline">{brand.upper()}</span>
    </div>
    <div style="margin-left:auto;text-align:right;">
        <div style="font-family:var(--font-mono);font-size:0.65rem;font-weight:700;letter-spacing:0.2em;color:rgba(255,255,255,0.4);margin-bottom:4px;">TIER</div>
        <div style="font-family:var(--font-mono);font-size:0.85rem;font-weight:700;color:{tier_color};background:white;padding:4px 12px;">{tier.upper()}</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br/>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — USAGE & HISTORY
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="av-panel-head" style="margin-bottom:16px;">
    <div class="av-panel-icon">📊</div>
    <div>
        <div class="av-panel-title">STEP 02</div>
        <div class="av-panel-subtitle">Usage &amp; History</div>
    </div>
</div>
""", unsafe_allow_html=True)

u1, u2, u3, u4 = st.columns(4)

with u1:
    mfg_year = st.selectbox("MANUFACTURING YEAR",
                             list(range(2025, 2014, -1)),
                             help="Year the vehicle was manufactured (not registration year)")
with u2:
    current_mileage = st.number_input("CURRENT ODOMETER (KM)",
                                       min_value=0, max_value=500000, value=12000, step=500,
                                       help="Total kilometres on odometer right now")
with u3:
    annual_mileage = st.slider("ANNUAL MILEAGE (KM/YR)",
                                3000, 60000, 12000, 1000,
                                help="How many km you typically drive per year")
with u4:
    ownership_period = st.slider("PLANNED OWNERSHIP (YEARS)",
                                  1, 12, 5, 1,
                                  help="How many years you plan to keep this vehicle")

import datetime
current_year = datetime.datetime.now().year
age = max(0, current_year - mfg_year)

# Usage insight callout
intensity = annual_mileage / 12000
usage_label = "LOW" if intensity < 0.75 else "MODERATE" if intensity < 1.5 else "HIGH"
usage_color = "#006400" if intensity < 0.75 else "#E07000" if intensity < 1.5 else "#FF2800"

u5, u6 = st.columns(2)
with u5:
    city = st.selectbox("PRIMARY USAGE CITY", CITIES,
                        help="Affects thermal stress, road quality penalty, and depreciation assumptions")
    st.markdown(f"<div class='field-help'>🏙️ Selected: <strong>{city}</strong> — affects maintenance risk and climate adjustment</div>", unsafe_allow_html=True)

with u6:
    income = st.number_input("MONTHLY INCOME ₹ (OPTIONAL)",
                              min_value=0, max_value=50_000_000, value=0, step=10000,
                              help="Used only to calculate ownership burden % — leave 0 to skip")
    st.markdown("<div class='field-help'>🔒 Used only for ownership burden calculation. Not stored or shared.</div>", unsafe_allow_html=True)

# Usage summary chips
st.markdown(f"""
<div style="display:flex;gap:8px;flex-wrap:wrap;margin:12px 0;">
    <span class="seg-pill active">Age: {age} {'yr' if age==1 else 'yrs'}</span>
    <span class="seg-pill active">{mileage if (mileage:=current_mileage) else 0:,} km on clock</span>
    <span class="seg-pill active" style="border-color:{usage_color};color:{usage_color};">Usage: {usage_label} ({annual_mileage:,} km/yr)</span>
    <span class="seg-pill active">{ownership_period}yr ownership</span>
    <span class="seg-pill active">{city}</span>
</div>
""", unsafe_allow_html=True)

st.markdown("<br/>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — FUEL TYPE
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="av-panel-head" style="margin-bottom:16px;">
    <div class="av-panel-icon red">⛽</div>
    <div>
        <div class="av-panel-title">STEP 03</div>
        <div class="av-panel-subtitle">Fuel Type</div>
    </div>
</div>
""", unsafe_allow_html=True)

available_fuels = list(dict.fromkeys(fuels))
fuel_type = st.radio(
    "FUEL TYPE",
    available_fuels,
    horizontal=True,
    help="Only fuel types available for this model are shown"
)

# Fuel cost insight
FUEL_COST_NOTE = {
    "Petrol":  "~₹106/L · ~17–22 km/L · High fuel price volatility",
    "Diesel":  "~₹94/L  · ~18–25 km/L · Better highway efficiency",
    "CNG":     "~₹80/kg  · ~25–30 km/kg · Lowest running cost",
    "EV":      "~₹8/kWh · ~5–7 km/kWh · Zero emission, lowest per-km cost",
    "Hybrid":  "~₹106/L · ~22–28 km/L · Self-charging, best city efficiency",
}
st.markdown(f"<div class='field-help'>{FUEL_ICONS.get(fuel_type,'⛽')} {FUEL_COST_NOTE.get(fuel_type,'')}</div>", unsafe_allow_html=True)

# EV specifics
battery_capacity, charging_freq, fast_charge_pct = None, None, 0

if fuel_type == "EV":
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:rgba(255,40,0,0.05);border:1.5px dashed #FF2800;padding:16px 20px;margin-bottom:12px;">
        <span style="font-family:var(--font-mono);font-size:0.7rem;font-weight:700;letter-spacing:0.2em;color:#FF2800;">
        ⚡ EV BATTERY PARAMETERS — Required for accurate health and degradation analysis
        </span>
    </div>
    """, unsafe_allow_html=True)
    ev1, ev2, ev3 = st.columns(3)
    with ev1:
        battery_capacity = st.number_input("BATTERY CAPACITY (kWh)",
                                            10.0, 200.0, 40.0, 0.5,
                                            help="Total usable battery capacity from manufacturer spec sheet")
    with ev2:
        charging_freq = st.selectbox("CHARGING FREQUENCY",
                                      ["Daily", "Every 2–3 Days", "Weekly", "Rarely"],
                                      help="How often you charge the vehicle")
    with ev3:
        fast_charge_pct = st.slider("DC FAST CHARGING %", 0, 100, 20,
                                     help="% of sessions using DC fast chargers (>50kW). High % degrades battery faster.")
        if fast_charge_pct > 60:
            st.warning(f"⚠️ {fast_charge_pct}% fast charging accelerates battery degradation.")

st.markdown("<br/>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — FINANCING
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="av-panel-head" style="margin-bottom:16px;">
    <div class="av-panel-icon">💰</div>
    <div>
        <div class="av-panel-title">STEP 04</div>
        <div class="av-panel-subtitle">Financing Details</div>
    </div>
</div>
""", unsafe_allow_html=True)

f1, f2, f3, f4 = st.columns(4)
with f1:
    on_road = st.number_input(
        "ON-ROAD PRICE (₹L)",
        min_value=1.0, max_value=600.0,
        value=round(auto_price * 1.10, 1), step=0.10,
        help="Ex-showroom + RTO + Insurance + Accessories. Typically ex-showroom × 1.08–1.12"
    )
    diff = round((on_road / auto_price - 1) * 100, 1)
    if diff > 0:
        st.markdown(f"<div class='field-help'>+{diff}% over ex-showroom · Auto-filled at 10%</div>", unsafe_allow_html=True)

with f2:
    down_pct = st.slider("DOWN PAYMENT %", 0, 100, 20, 5,
                          help="Percentage of on-road price you pay upfront")
with f3:
    loan_rate = st.slider("INTEREST RATE %", 6.0, 20.0, 9.0, 0.25,
                           help="Annual interest rate from your bank/NBFC. Typically 8.5–12% for new cars")
with f4:
    tenure = st.selectbox("LOAN TENURE",
                           [12, 24, 36, 48, 60, 72, 84],
                           index=4,
                           format_func=lambda x: f"{x} months ({x//12} yr{'' if x//12==1 else 's'})",
                           help="Longer tenure = lower EMI but higher total interest paid")

# Live EMI computation
principal = on_road * (1 - down_pct / 100) * 100000
down_amt  = on_road * down_pct / 100
if loan_rate > 0 and tenure > 0 and down_pct < 100:
    r   = loan_rate / (12 * 100)
    emi = principal * r * (1 + r)**tenure / ((1 + r)**tenure - 1)
    total_paid = emi * tenure
    interest   = total_paid - principal
else:
    emi = principal / tenure if tenure > 0 else 0
    interest = 0
    total_paid = principal

st.markdown(f"""
<div class="av-emi-bar">
    <div class="av-emi-cell">
        <div class="av-emi-label">Monthly EMI</div>
        <div class="av-emi-value red">₹{emi:,.0f}</div>
    </div>
    <div class="av-emi-cell">
        <div class="av-emi-label">Down Payment</div>
        <div class="av-emi-value">₹{down_amt:.2f}L</div>
    </div>
    <div class="av-emi-cell">
        <div class="av-emi-label">Total Interest</div>
        <div class="av-emi-value">₹{interest/100000:.2f}L</div>
    </div>
    <div class="av-emi-cell">
        <div class="av-emi-label">Loan Amount</div>
        <div class="av-emi-value">₹{principal/100000:.2f}L</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Interest warning
interest_pct = (interest / principal * 100) if principal > 0 else 0
if interest_pct > 40:
    st.warning(f"⚠️ You'll pay **₹{interest/100000:.2f}L in interest** — {interest_pct:.0f}% extra over {tenure//12} years. Consider a shorter tenure or larger down payment.")

st.markdown("<br/><br/>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# REVIEW & SUBMIT
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("<hr/>", unsafe_allow_html=True)
st.markdown("<h2>REVIEW YOUR CONFIGURATION</h2>", unsafe_allow_html=True)

# Summary 2-col layout
rs1, rs2 = st.columns(2)

with rs1:
    st.markdown(f"""
    <div style="background:white;border:2px solid #1A1A1A;padding:24px;">
        <div style="font-family:var(--font-mono);font-size:0.65rem;font-weight:700;letter-spacing:0.2em;color:var(--c-text-muted);margin-bottom:4px;">VEHICLE</div>
        <div style="font-size:1.4rem;font-weight:900;text-transform:uppercase;margin-bottom:16px;line-height:1.2;">
            {brand}<br/><span style="color:#FF2800;">{model}</span>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
            <div><div style="font-family:var(--font-mono);font-size:0.6rem;letter-spacing:0.2em;color:#888;text-transform:uppercase;">Variant</div><div style="font-weight:700;font-size:0.85rem;">{variant}</div></div>
            <div><div style="font-family:var(--font-mono);font-size:0.6rem;letter-spacing:0.2em;color:#888;text-transform:uppercase;">Fuel</div><div style="font-weight:700;font-size:0.85rem;">{FUEL_ICONS.get(fuel_type,'')} {fuel_type}</div></div>
            <div><div style="font-family:var(--font-mono);font-size:0.6rem;letter-spacing:0.2em;color:#888;text-transform:uppercase;">Year</div><div style="font-weight:700;font-size:0.85rem;">{mfg_year} · Age {age}yr</div></div>
            <div><div style="font-family:var(--font-mono);font-size:0.6rem;letter-spacing:0.2em;color:#888;text-transform:uppercase;">City</div><div style="font-weight:700;font-size:0.85rem;">{city}</div></div>
            <div><div style="font-family:var(--font-mono);font-size:0.6rem;letter-spacing:0.2em;color:#888;text-transform:uppercase;">Odometer</div><div style="font-weight:700;font-size:0.85rem;">{current_mileage:,} km</div></div>
            <div><div style="font-family:var(--font-mono);font-size:0.6rem;letter-spacing:0.2em;color:#888;text-transform:uppercase;">Annual KM</div><div style="font-weight:700;font-size:0.85rem;">{annual_mileage:,} km</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with rs2:
    st.markdown(f"""
    <div style="background:#1A1A1A;padding:24px;border:2px solid #1A1A1A;">
        <div style="font-family:var(--font-mono);font-size:0.65rem;font-weight:700;letter-spacing:0.2em;color:rgba(255,255,255,0.4);margin-bottom:4px;">FINANCIAL SNAPSHOT</div>
        <div style="font-family:var(--font-mono);font-size:2.5rem;font-weight:700;color:#FF2800;line-height:1;">₹{on_road:.1f}L</div>
        <div style="font-family:var(--font-mono);font-size:0.7rem;color:rgba(255,255,255,0.4);margin-bottom:20px;letter-spacing:0.1em;">ON-ROAD PRICE</div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
            <div><div style="font-family:var(--font-mono);font-size:0.6rem;letter-spacing:0.15em;color:rgba(255,255,255,0.4);">MONTHLY EMI</div><div style="font-family:var(--font-mono);font-size:1.1rem;font-weight:700;color:white;">₹{emi:,.0f}</div></div>
            <div><div style="font-family:var(--font-mono);font-size:0.6rem;letter-spacing:0.15em;color:rgba(255,255,255,0.4);">DOWN PAYMENT</div><div style="font-family:var(--font-mono);font-size:1.1rem;font-weight:700;color:white;">₹{down_amt:.1f}L</div></div>
            <div><div style="font-family:var(--font-mono);font-size:0.6rem;letter-spacing:0.15em;color:rgba(255,255,255,0.4);">TOTAL INTEREST</div><div style="font-family:var(--font-mono);font-size:1.1rem;font-weight:700;color:#FF2800;">₹{interest/100000:.2f}L</div></div>
            <div><div style="font-family:var(--font-mono);font-size:0.6rem;letter-spacing:0.15em;color:rgba(255,255,255,0.4);">OWNERSHIP</div><div style="font-family:var(--font-mono);font-size:1.1rem;font-weight:700;color:white;">{ownership_period} yrs</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br/>", unsafe_allow_html=True)

# ── ANALYZE CTA ───────────────────────────────────────────────────────────────
col_btn, col_note = st.columns([2, 1])

with col_btn:
    analyze = st.button(f"  ANALYZE {brand.upper()} {model.upper()}  →",
                         use_container_width=True, type="primary")

with col_note:
    st.markdown("""
    <div style="font-family:var(--font-mono);font-size:0.68rem;color:var(--c-text-muted);line-height:1.7;padding:8px 0;">
    ↳ Proceeds to 8-module analysis<br/>
    ↳ Health · Depreciation · Maintenance<br/>
    ↳ TCO · Risk · Simulator · Compare
    </div>
    """, unsafe_allow_html=True)

if analyze:
    st.session_state.vehicle_data = {
        "brand": brand, "model": model, "variant": variant,
        "fuel_type": fuel_type, "segment": seg,
        "purchase_price": on_road, "ex_showroom_price": auto_price,
        "mfg_year": mfg_year, "current_mileage": current_mileage,
        "annual_mileage": annual_mileage, "ownership_period": ownership_period,
        "city": city, "income": income,
        "battery_capacity": battery_capacity,
        "charging_freq": charging_freq,
        "fast_charge_pct": fast_charge_pct if fuel_type == "EV" else 0,
        "down_payment_pct": down_pct,
        "loan_rate": loan_rate,
        "tenure_months": tenure,
    }
    st.success(f"✅ **{brand} {model} · {variant}** configured. Launching analysis...")
    st.balloons()
    import time
    time.sleep(0.8)
    st.switch_page("pages/02_Vehicle_Health.py")

# Bottom spacer
st.markdown("<div class='sticky-spacer'></div>", unsafe_allow_html=True)

# ── Sticky bottom summary bar ─────────────────────────────────────────────────
st.markdown(f"""
<div class="sticky-cta">
    <div>
        <div class="sticky-vehicle-name">{brand} · {model} · {variant}</div>
        <div style="font-family:var(--font-mono);font-size:0.65rem;color:rgba(255,255,255,0.3);letter-spacing:0.15em;">
            {mfg_year} · {fuel_type} · {city} · {annual_mileage:,} km/yr
        </div>
    </div>
    <div style="display:flex;align-items:center;gap:32px;">
        <div>
            <div style="font-family:var(--font-mono);font-size:0.6rem;color:rgba(255,255,255,0.4);letter-spacing:0.15em;">ON-ROAD</div>
            <div class="sticky-price">₹{on_road:.1f}L</div>
        </div>
        <div>
            <div style="font-family:var(--font-mono);font-size:0.6rem;color:rgba(255,255,255,0.4);letter-spacing:0.15em;">MONTHLY EMI</div>
            <div style="font-family:var(--font-mono);font-size:1.2rem;font-weight:700;color:white;">₹{emi:,.0f}</div>
        </div>
        <div>
            <div style="font-family:var(--font-mono);font-size:0.6rem;color:rgba(255,255,255,0.4);letter-spacing:0.15em;">OWNERSHIP</div>
            <div style="font-family:var(--font-mono);font-size:1.2rem;font-weight:700;color:white;">{ownership_period} YRS</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
