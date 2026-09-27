"""Brutalist metric cards and UI components."""

import streamlit as st

def metric_card(label: str, value: str, subtext: str = "", color: str = "#000", border_color: str = "#000"):
    st.markdown(f"""
        <div style="
            border: 2px solid {border_color};
            padding: 1.5rem;
            background: #FFF;
            margin-bottom: 1rem;
            box-shadow: 4px 4px 0px {border_color};
        ">
            <div style="font-size: 0.8rem; font-weight: bold; text-transform: uppercase; letter-spacing: 0.1em; color: {color};">{label}</div>
            <div style="font-size: 2.5rem; font-weight: 800; margin: 0.5rem 0; font-family: monospace; color: {color};">{value}</div>
            <div style="font-size: 0.8rem; color: #333; text-transform: uppercase;">{subtext}</div>
        </div>
    """, unsafe_allow_html=True)

def score_card(label: str, score: float, max_score: int = 100, description: str = ""):
    color = "#FF2800" if score < max_score * 0.5 else "#000"
    st.markdown(f"""
        <div style="border: 2px solid #000; padding: 1.5rem; background: #FFF; margin-bottom: 1rem;">
            <div style="font-size: 0.9rem; font-weight: bold; text-transform: uppercase;">{label}</div>
            <div style="font-size: 3rem; font-weight: 800; font-family: monospace; color: {color};">
                {score:.0f}<span style="font-size: 1.5rem; color: #000;">/{max_score}</span>
            </div>
            <div style="font-size: 0.8rem; margin-top: 0.5rem;">{description}</div>
        </div>
    """, unsafe_allow_html=True)

def risk_badge(level: str):
    bg_color = "#FF2800" if level.upper() == "HIGH" else "#000"
    st.markdown(f"""
        <span style="background: {bg_color}; color: #FFF; padding: 0.3rem 0.6rem; 
        font-weight: bold; font-size: 0.8rem; text-transform: uppercase; border: 2px solid #000;">
            {level} RISK
        </span>
    """, unsafe_allow_html=True)

def health_gauge(score: float, label: str):
    width = min(max(score, 0), 100)
    st.markdown(f"""
        <div style="border: 2px solid #000; padding: 1rem; background: #FFF; margin-bottom: 1rem;">
            <div style="font-size: 0.8rem; font-weight: bold; text-transform: uppercase; margin-bottom: 0.5rem;">{label}</div>
            <div style="height: 20px; border: 2px solid #000; width: 100%; position: relative;">
                <div style="height: 100%; width: {width}%; background: #000;"></div>
            </div>
            <div style="text-align: right; font-family: monospace; font-weight: bold; margin-top: 0.2rem;">{score:.0f}%</div>
        </div>
    """, unsafe_allow_html=True)

def comparison_row(metric: str, val_a: str, val_b: str, better: str = 'lower'):
    st.markdown(f"""
        <div style="display: flex; justify-content: space-between; border-bottom: 2px solid #000; padding: 0.5rem 0;">
            <div style="font-weight: bold; text-transform: uppercase;">{metric}</div>
            <div style="display: flex; gap: 2rem; font-family: monospace; font-weight: bold;">
                <div>{val_a}</div>
                <div>{val_b}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def section_header(title: str, subtitle: str = ''):
    st.markdown(f"""
        <div style="margin: 2rem 0 1rem 0; border-bottom: 4px solid #000; padding-bottom: 0.5rem;">
            <h2 style="font-size: 1.8rem; font-weight: 900; text-transform: uppercase; margin: 0; color: #000;">{title}</h2>
            {f'<div style="font-size: 1rem; color: #333; font-weight: bold;">{subtitle}</div>' if subtitle else ''}
        </div>
    """, unsafe_allow_html=True)

def data_confidence_bar(confidence: float, label: str):
    st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 1rem; margin-top: 0.5rem;">
            <div style="font-size: 0.7rem; font-weight: bold; text-transform: uppercase;">{label}</div>
            <div style="flex-grow: 1; height: 10px; border: 1px solid #000; background: repeating-linear-gradient(45deg, #000, #000 5px, #fff 5px, #fff 10px);">
                <div style="height: 100%; width: {confidence}%; background: #000;"></div>
            </div>
            <div style="font-size: 0.7rem; font-family: monospace; font-weight: bold;">{confidence:.0f}%</div>
        </div>
    """, unsafe_allow_html=True)

def verified_badge():
    st.markdown("""<span style="border: 2px solid #000; padding: 0.1rem 0.4rem; font-weight: 900; font-size: 0.7rem; background: #000; color: #FFF;">VERIFIED</span>""", unsafe_allow_html=True)

def estimated_badge():
    st.markdown("""<span style="border: 2px dashed #000; padding: 0.1rem 0.4rem; font-weight: 900; font-size: 0.7rem; color: #000;">ESTIMATED</span>""", unsafe_allow_html=True)

def assumption_badge():
    st.markdown("""<span style="border: 2px solid #FF2800; padding: 0.1rem 0.4rem; font-weight: 900; font-size: 0.7rem; color: #FF2800;">USER ASSUMPTION</span>""", unsafe_allow_html=True)

def info_callout(text: str):
    st.markdown(f"""
        <div style="border-left: 4px solid #FF2800; padding: 1rem; background: #FFF; font-weight: bold; margin-bottom: 1rem; border-top: 1px solid #000; border-right: 1px solid #000; border-bottom: 1px solid #000;">
            {text}
        </div>
    """, unsafe_allow_html=True)
