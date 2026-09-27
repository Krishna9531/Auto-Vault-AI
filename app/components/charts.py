"""Plotly charts with brutalist styling."""

import plotly.graph_objects as go
import plotly.express as px

def apply_brutalist_theme(fig):
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='monospace', color='black', size=12),
        title_font=dict(family='system-ui, sans-serif', size=16, color='black'),
        margin=dict(l=40, r=40, t=60, b=40),
        xaxis=dict(
            showgrid=True, gridcolor='black', gridwidth=1,
            zeroline=True, zerolinecolor='black', zerolinewidth=2,
            showline=True, linecolor='black', linewidth=2
        ),
        yaxis=dict(
            showgrid=True, gridcolor='black', gridwidth=1,
            zeroline=True, zerolinecolor='black', zerolinewidth=2,
            showline=True, linecolor='black', linewidth=2
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=14,
            font_family="monospace"
        )
    )
    return fig

def depreciation_curve(years: list, values: list, title: str) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years, y=values,
        mode='lines+markers',
        line=dict(color='#FF2800', width=4),
        marker=dict(size=10, color='black', symbol='square', line=dict(color='black', width=2))
    ))
    fig.update_layout(title=title.upper())
    return apply_brutalist_theme(fig)

def tco_waterfall(components: dict, title: str) -> go.Figure:
    fig = go.Figure(go.Waterfall(
        name="TCO", orientation="v",
        measure=["relative"] * len(components) + ["total"],
        x=list(components.keys()) + ["Total"],
        textposition="outside",
        text=[f"₹{v:,.0f}" for v in components.values()] + [f"₹{sum(components.values()):,.0f}"],
        y=list(components.values()) + [sum(components.values())],
        connector={"line": {"color": "black", "width": 2}},
        decreasing={"marker": {"color": "#000", "line": {"color": "black", "width": 2}}},
        increasing={"marker": {"color": "#FF2800", "line": {"color": "black", "width": 2}}},
        totals={"marker": {"color": "white", "line": {"color": "black", "width": 3}}}
    ))
    fig.update_layout(title=title.upper(), showlegend=False)
    return apply_brutalist_theme(fig)

def maintenance_probability_bar(items: dict) -> go.Figure:
    fig = go.Figure(go.Bar(
        x=list(items.values()),
        y=list(items.keys()),
        orientation='h',
        marker=dict(
            color='#000',
            line=dict(color='black', width=2)
        )
    ))
    fig.update_layout(title="MAINTENANCE PROBABILITIES", xaxis_title="Probability (%)")
    return apply_brutalist_theme(fig)

def risk_radar(dimensions: dict) -> go.Figure:
    fig = go.Figure(go.Scatterpolar(
        r=list(dimensions.values()),
        theta=list(dimensions.keys()),
        fill='toself',
        fillcolor='rgba(255, 40, 0, 0.3)',
        line=dict(color='#FF2800', width=3)
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], color='black', gridcolor='black'),
            angularaxis=dict(color='black', gridcolor='black')
        ),
        showlegend=False,
        title="RISK DIMENSIONS"
    )
    return apply_brutalist_theme(fig)

def scenario_comparison_bar(scenarios: dict) -> go.Figure:
    fig = go.Figure(go.Bar(
        x=list(scenarios.keys()),
        y=list(scenarios.values()),
        marker=dict(color=['#000', '#FF2800', '#FFF'], line=dict(color='black', width=3))
    ))
    fig.update_layout(title="SCENARIO COMPARISON")
    return apply_brutalist_theme(fig)

def battery_degradation_curve(soh_values: list, cycles: list) -> go.Figure:
    fig = go.Figure(go.Scatter(
        x=cycles, y=soh_values,
        mode='lines',
        line=dict(color='black', width=3, dash='dash')
    ))
    fig.update_layout(title="BATTERY DEGRADATION", xaxis_title="Cycles", yaxis_title="SOH (%)")
    return apply_brutalist_theme(fig)

def fuel_cost_projection(years: list, costs: list, scenarios: dict) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years, y=costs,
        mode='lines+markers',
        line=dict(color='#000', width=3),
        name='Base'
    ))
    for name, data in scenarios.items():
        fig.add_trace(go.Scatter(
            x=years, y=data,
            mode='lines',
            line=dict(width=2, dash='dot'),
            name=name
        ))
    fig.update_layout(title="FUEL COST PROJECTION")
    return apply_brutalist_theme(fig)
