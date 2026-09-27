# -*- coding: utf-8 -*-
"""
AUTOVAULT AI — Clean Sidebar Navigation
"""
import streamlit as st

def build_sidebar():
    """Renders a clean, minimalist sidebar navigation."""
    st.markdown("""
    <style>
    /* 1. Hide default Streamlit sidebar page links */
    [data-testid="stSidebarNav"] { display: none !important; }
    
    /* 2. Style the sidebar container minimally */
    [data-testid="stSidebar"] {
        border-right: 1px solid #EAEAEA !important;
        background-color: #F8F9FA !important;
    }
    
    /* 3. Custom Page Links - Clean and Simple */
    .stPageLink a {
        padding: 10px 14px !important;
        border-radius: 4px !important;
        transition: all 150ms ease !important;
        color: #1A1A1A !important;
        text-decoration: none !important;
    }
    .stPageLink a:hover {
        background-color: #E9ECEF !important;
        transform: translateX(2px);
    }
    .stPageLink a p {
        font-family: 'Inter', system-ui, sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        color: #1A1A1A !important;
    }
    
    /* 4. Title */
    .nav-brand {
        font-family: 'Inter', system-ui, sans-serif !important;
        font-weight: 900 !important;
        font-size: 1.5rem !important;
        letter-spacing: -0.03em !important;
        color: #1A1A1A !important;
        margin-bottom: 24px !important;
    }
    .nav-brand span { color: #FF2800 !important; }
    
    hr.nav-div {
        border: none !important;
        border-top: 1px solid #DEE2E6 !important;
        margin: 16px 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown('<div class="nav-brand">AUTO<span>VAULT</span></div>', unsafe_allow_html=True)
        
        # Clean Navigation without emojis
        st.page_link("Home.py", label="Home")
        
        st.markdown("<hr class='nav-div'>", unsafe_allow_html=True)
        
        st.page_link("pages/01_Vehicle_Input.py", label="01 / Vehicle Input")
        st.page_link("pages/02_Vehicle_Health.py", label="02 / Health Analysis")
        st.page_link("pages/03_Depreciation.py", label="03 / Depreciation")
        st.page_link("pages/04_Maintenance.py", label="04 / Maintenance")
        st.page_link("pages/05_TCO.py", label="05 / Total Cost")
        st.page_link("pages/06_Financial_Risk.py", label="06 / Financial Risk")
        st.page_link("pages/07_Simulator.py", label="07 / Simulator")
        st.page_link("pages/08_Compare.py", label="08 / Compare")
        
        # Display active vehicle config if set
        if "vehicle_data" in st.session_state and st.session_state.vehicle_data:
            v = st.session_state.vehicle_data
            st.markdown(f"""
            <div style="margin-top: 40px; background: #FFFFFF; padding: 16px; border: 1px solid #DEE2E6; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
                <div style="font-family:'Inter', sans-serif; font-size:0.65rem; color:#888; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; margin-bottom:4px;">Active Vehicle</div>
                <div style="font-weight:900; font-size:1.1rem; line-height:1.2; color:#1A1A1A;">{v.get('brand')} <br/><span style="color:#FF2800;">{v.get('model')}</span></div>
                <div style="font-size:0.8rem; color:#555; font-weight:500; margin-top:4px;">{v.get('variant')}</div>
            </div>
            """, unsafe_allow_html=True)
