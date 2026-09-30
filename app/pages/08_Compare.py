import streamlit as st
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from app.utils.vehicle_db import DB

st.set_page_config(page_title='Compare', page_icon='🚗', layout='wide')

# Custom navigation
try:
    from app.components.navigation import build_sidebar
    build_sidebar()
except Exception as e:
    pass

def load_css():
    css_path = Path(__file__).parent.parent / "styles" / "brutalist.css"
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

st.markdown("<h1 style='font-weight: 900; text-transform: uppercase;'>08 COMPARE</h1>", unsafe_allow_html=True)
st.markdown("---")

if 'compare_list' not in st.session_state:
    st.session_state.compare_list = []

# Top controls
c1, c2 = st.columns([3, 1])
with c1:
    st.markdown("### ADD VEHICLE TO COMPARISON")
    sel1, sel2, sel3, sel4 = st.columns(4)
    brands = list(DB.keys())
    with sel1:
        brand = st.selectbox("Brand", brands, key="cmp_brand")
    with sel2:
        models = list(DB[brand].keys())
        model = st.selectbox("Model", models, key="cmp_model")
    
    mdata = DB[brand][model]
    variants = mdata.get("v", ["Base"])
    prices = mdata.get("p", [0.0])
    fuels = mdata.get("f", ["Petrol"])
    
    with sel3:
        variant = st.selectbox("Variant", variants, key="cmp_var")
        v_idx = variants.index(variant)
        price = prices[v_idx]
        # Fuel logic: sometimes fuel list is shorter than variants list
        fuel = fuels[v_idx] if v_idx < len(fuels) else fuels[0]
        
    with sel4:
        st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)
        if st.button("ADD TO COMPARE", use_container_width=True):
            st.session_state.compare_list.append({
                "Brand": brand,
                "Model": model,
                "Variant": variant,
                "Price": price,
                "Fuel": fuel
            })
            st.rerun()

with c2:
    st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)
    if st.button("CLEAR ALL", use_container_width=True, type="primary"):
        st.session_state.compare_list = []
        st.rerun()

st.write("---")

if len(st.session_state.compare_list) > 0:
    st.markdown("### COMPARISON MATRIX")
    
    data = []
    col_names = []
    
    for i, v in enumerate(st.session_state.compare_list):
        # Create unique column name
        col_name = f"{v['Brand']} {v['Model']} ({i+1})"
        col_names.append(col_name)
        
        data.append({
            "Vehicle": col_name,
            "Variant": v['Variant'],
            "Fuel Type": v['Fuel'],
            "Purchase Price (L)": round(v['Price'], 2),
            "Estimated 5Y TCO (L)": round(v['Price'] * 1.45, 2),
            "Est. Resale Value (L)": round(v['Price'] * (0.6 if v['Fuel'] != 'EV' else 0.45), 2),
            "Maintenance (L/yr)": round(v['Price'] * 0.015, 2),
            "Risk Score": "Low" if v['Fuel'] != 'EV' else "Medium"
        })
    
    df = pd.DataFrame(data).set_index("Vehicle").T
    # df columns are guaranteed unique because of (i+1)
    
    def highlight_min_max(s):
        # Don't highlight categorical rows
        if s.name in ['Variant', 'Fuel Type', 'Risk Score']:
            return [''] * len(s)
            
        try:
            s_num = pd.to_numeric(s)
            is_max = s_num == s_num.max()
            is_min = s_num == s_num.min()
            
            # For prices/costs, lower is better (green), higher is worse (red).
            # For resale value, higher is better (green), lower is worse (red).
            if s.name == 'Est. Resale Value (L)':
                return ['background-color: #d4edda; color: black' if m else 'background-color: #f8d7da; color: black' if v else '' for v, m in zip(is_min, is_max)]
            else:
                return ['background-color: #d4edda; color: black' if v else 'background-color: #f8d7da; color: black' if m else '' for v, m in zip(is_min, is_max)]
        except:
            return [''] * len(s)
            
    st.dataframe(df.style.apply(highlight_min_max, axis=1), use_container_width=True)
    
    st.markdown("### SUMMARY")
    st.info("**Models differ primarily in their long-term running costs and depreciation curves. Green indicates the best value in that category, red indicates the worst.**")
