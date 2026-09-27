"""Formatting utilities for the AUTOVAULT AI project."""

def format_lakhs(amount_inr: float) -> str:
    """Returns '₹18.5L' format."""
    return f"₹{amount_inr / 100_000:.1f}L"

def format_currency(amount_inr: float) -> str:
    """Returns formatted currency."""
    return f"₹{amount_inr:,.0f}"

def format_percentage(value: float, decimals=1) -> str:
    """Returns formatted percentage."""
    return f"{value:.{decimals}f}%"

def format_score(score: float, max_score=100) -> str:
    """Returns formatted score."""
    return f"{score:.0f}/{max_score}"

def format_km(km: float) -> str:
    """Returns formatted km, e.g., '31,240 km'."""
    return f"{km:,.0f} km"

def risk_label(score: float) -> tuple[str, str]:
    """Returns (label, color) based on risk score."""
    if score <= 30:
        return ("LOW", "#000000")
    elif score <= 70:
        return ("MEDIUM", "#000000")
    return ("HIGH", "#FF2800")

def health_label(score: float) -> tuple[str, str]:
    """Returns (label, color) based on health score."""
    if score >= 90:
        return ("Excellent", "#000000")
    elif score >= 75:
        return ("Good", "#000000")
    elif score >= 60:
        return ("Fair", "#000000")
    return ("Poor", "#FF2800")

def years_label(years: float) -> str:
    """Returns formatted years."""
    if years == 1:
        return "1 Year"
    return f"{years:.1f} Years".replace(".0", "")

def format_inr_crore(amount: float) -> str:
    """Returns amount in crores."""
    return f"₹{amount / 10_000_000:.2f}Cr"

def depreciation_color(pct: float) -> str:
    """Returns a color based on depreciation percentage."""
    if pct > 50:
        return "#FF2800"
    return "#000000"
