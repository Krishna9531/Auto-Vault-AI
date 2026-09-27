# -*- coding: utf-8 -*-
"""
AUTOVAULT AI — Sidebar Navigation Component
"""
import streamlit as st

def build_sidebar():
    """Renders a custom, beautifully styled sidebar across all pages."""
    st.markdown("""
    <style>
    /* 1. Hide default Streamlit sidebar page links */
    [data-testid="stSidebarNav"] { display: none !important; }
    
    /* 2. Style the sidebar container */
    [data-testid="stSidebar"] {
        background-color: #1A1A1A !important;
        border-right: 3px solid #FF2800 !important;
    }
    
    /* 3. Text colors in sidebar */
    [data-testid="stSidebar"] * {
        color: #F4F4EF !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* 4. Custom Page Links */
    .stPageLink a {
        padding: 12px 16px !important;
        border: 2px solid transparent !important;
        transition: all 150ms ease !important;
        border-radius: 0 !important;
    }
    .stPageLink a:hover {
        border-color: #FF2800 !important;
        background: rgba(255, 40, 0, 0.1) !important;
        transform: translateX(4px);
    }
    .stPageLink a p {
        font-weight: 700 !important;
        font-size: 0.85rem !important;
        letter-spacing: 0.05em !important;
        text-transform: uppercase !important;
    }
    
    /* 5. Title */
    .nav-brand {
        font-family: 'IBM Plex Mono', monospace !important;
        font-weight: 900 !important;
        font-size: 1.6rem !important;
        letter-spacing: 0.1em !important;
        color: #FF2800 !important;
        margin-bottom: 24px !important;
        text-transform: uppercase !important;
    }
    .nav-brand span { color: white !important; }
    
    hr.nav-div {
        border: none !important;
        border-top: 1px dashed rgba(255,255,255,0.2) !important;
        margin: 16px 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown('<div class="nav-brand">AUTO<span>VAULT</span></div>', unsafe_allow_html=True)
        
        # Core Navigation
        st.page_link("Home.py", label="Home / Overview", icon="🏠")
        
        st.markdown("<hr class='nav-div'>", unsafe_allow_html=True)
        
        st.page_link("pages/01_Vehicle_Input.py", label="Vehicle Input", icon="🚗")
        st.page_link("pages/02_Vehicle_Health.py", label="Health Analysis", icon="🩺")
        st.page_link("pages/03_Depreciation.py", label="Depreciation", icon="📉")
        st.page_link("pages/04_Maintenance.py", label="Maintenance", icon="🔧")
        st.page_link("pages/05_TCO.py", label="Total Cost (TCO)", icon="💰")
        st.page_link("pages/06_Financial_Risk.py", label="Financial Risk", icon="⚠️")
        st.page_link("pages/07_Simulator.py", label="Simulator", icon="🕹️")
        st.page_link("pages/08_Compare.py", label="Compare", icon="⚖️")
        
        # Display active vehicle config if set
        if "vehicle_data" in st.session_state and st.session_state.vehicle_data:
            v = st.session_state.vehicle_data
            st.markdown(f"""
            <div style="margin-top: 40px; background: #0A0A0A; padding: 20px; border: 2px solid #333;">
                <div style="font-family:'IBM Plex Mono', monospace; font-size:0.65rem; color:#888; letter-spacing:0.2em; margin-bottom: 8px;">ACTIVE VEHICLE</div>
                <div style="font-weight:900; font-size:1.1rem; line-height:1.2; text-transform:uppercase;">{v.get('brand')} <br/> <span style="color:#FF2800;">{v.get('model')}</span></div>
                <div style="font-size:0.75rem; color:#aaa; font-weight:700; margin-top:6px;">{v.get('variant')}</div>
            </div>
            """, unsafe_allow_html=True)
