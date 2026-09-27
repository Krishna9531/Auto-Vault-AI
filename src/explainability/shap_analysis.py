"""
SHAP-based explainability for AUTOVAULT AI.
=============================================
Provides feature importance extraction and human-readable "why" explanations
for each prediction domain (depreciation, maintenance risk, health).

Design philosophy:
  - No hard SHAP library dependency at module import time.  The functions
    that actually need `shap` import it lazily so that the rest of the app
    can still run if the optional library is not installed.
  - All public functions accept plain Python / NumPy / sklearn objects and
    return plain Python dicts/lists — nothing framework-specific.
  - Human-readable reason strings are written for a non-technical end-user
    (used-car buyer / fleet manager), not a data scientist.
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Thresholds and copy used by the explanation generators
# ---------------------------------------------------------------------------

# Depreciation reason thresholds ─ keyed on feature name
_DEPR_THRESHOLDS: dict[str, dict[str, Any]] = {
    "age_years":        {"warn": 5,    "critical": 8},
    "annual_km":        {"warn": 18_000, "critical": 25_000},
    "accident_penalty": {"warn": 0.05, "critical": 0.15},
    "service_score":    {"good": 0.75, "poor": 0.50},
    "popularity_score": {"good": 0.80, "poor": 0.65},
    "climate_factor":   {"warn": 1.05},
    "is_luxury":        {},   # handled by flag value
    "is_ev":            {},   # handled by flag value
}

# Maintenance risk copy — score bands
_RISK_BANDS: list[tuple[float, str, str]] = [
    (0.25, "Low",      "🟢"),
    (0.50, "Moderate", "🟡"),
    (0.75, "High",     "🟠"),
    (1.01, "Critical", "🔴"),
]


# ===========================================================================
# Core utility
# ===========================================================================

def get_feature_importance(
    model: Any,
    feature_names: list[str],
    top_n: int = 10,
) -> dict[str, float]:
    """Extract feature importance from a fitted sklearn-compatible or XGBoost model.

    Supports any estimator that exposes ``feature_importances_`` (RandomForest,
    GradientBoosting, XGBoost, LightGBM, etc.).  For models without that
    attribute (e.g. linear regressors with ``coef_``), the absolute coefficient
    values are used as a proxy.  As a last resort, uniform importance is
    returned so that downstream callers never crash.

    Parameters
    ----------
    model:
        A fitted sklearn-compatible estimator.
    feature_names:
        Ordered list of feature names matching the columns the model was
        trained on.
    top_n:
        Maximum number of features to return, sorted by descending importance.

    Returns
    -------
    dict[str, float]
        Mapping of ``{feature_name: importance_score}`` for the top ``top_n``
        features.  Scores are raw (not re-normalised to sum to 1).
    """
    if hasattr(model, "feature_importances_"):
        # Tree-based models: Gini / gain importance
        importances: np.ndarray = np.asarray(model.feature_importances_, dtype=float)
    elif hasattr(model, "coef_"):
        # Linear models: use absolute coefficient magnitude
        coef = np.asarray(model.coef_, dtype=float)
        importances = np.abs(coef.ravel())
        # Pad or trim to match feature_names length
        if importances.size < len(feature_names):
            importances = np.pad(importances, (0, len(feature_names) - importances.size))
        else:
            importances = importances[: len(feature_names)]
    else:
        # Unknown model type — return uniform importance as a neutral fallback
        importances = np.ones(len(feature_names), dtype=float) / len(feature_names)

    # Guard against length mismatch (e.g. pipeline with feature selection)
    n = min(len(feature_names), len(importances))
    pairs = sorted(
        zip(feature_names[:n], importances[:n].tolist()),
        key=lambda x: x[1],
        reverse=True,
    )
    return {name: float(imp) for name, imp in pairs[:top_n]}


# ===========================================================================
# Depreciation explainability
# ===========================================================================

def explain_depreciation(
    feature_importance: dict[str, float],
    vehicle: dict[str, Any],
) -> list[str]:
    """Generate human-readable reasons that drive a vehicle's depreciation score.

    The reasons are ordered by the magnitude of the feature's importance in
    the model, so the most impactful factor is always listed first.

    Parameters
    ----------
    feature_importance:
        Output of :func:`get_feature_importance` — ``{feature: score}``.
    vehicle:
        Raw vehicle input dict (same schema as used in feature engineering).

    Returns
    -------
    list[str]
        Up to 5 plain-English reason strings suitable for display in a UI.
        Each string starts with an emoji indicator for quick scanning.
    """
    import datetime

    current_year: int = datetime.date.today().year
    age: float        = max(current_year - int(vehicle.get("manufacture_year", current_year - 3)), 0.5)
    total_km: int     = int(vehicle.get("total_km", 0))
    annual_km: float  = total_km / age
    fuel: str         = vehicle.get("fuel_type", "petrol").lower()
    city: str         = vehicle.get("city", "Delhi")
    acc: int          = int(vehicle.get("num_accidents", 0))
    major_acc: bool   = bool(vehicle.get("major_accident", False))
    num_svc: int      = int(vehicle.get("num_services", 0))
    auth_svc: bool    = bool(vehicle.get("authorised_service", False))

    # Build a {feature: reason_string} map; only include if condition met
    candidate_reasons: dict[str, str] = {}

    # Age
    if age >= _DEPR_THRESHOLDS["age_years"]["critical"]:
        candidate_reasons["age_years"] = (
            f"⏳ Vehicle is {age:.0f} years old — significant age-related depreciation applies."
        )
    elif age >= _DEPR_THRESHOLDS["age_years"]["warn"]:
        candidate_reasons["age_years"] = (
            f"⏳ At {age:.0f} years, the vehicle is entering its steeper depreciation curve."
        )

    # Annual mileage
    if annual_km >= _DEPR_THRESHOLDS["annual_km"]["critical"]:
        candidate_reasons["annual_km"] = (
            f"🛣️ Very high annual usage ({annual_km:,.0f} km/year) accelerates wear and lowers resale value."
        )
    elif annual_km >= _DEPR_THRESHOLDS["annual_km"]["warn"]:
        candidate_reasons["annual_km"] = (
            f"🛣️ Above-average annual mileage ({annual_km:,.0f} km/year) reduces residual value."
        )

    # Accident history
    if major_acc:
        candidate_reasons["accident_penalty"] = (
            "💥 Major structural accident on record — significant resale value penalty applied."
        )
    elif acc > 0:
        candidate_reasons["accident_penalty"] = (
            f"⚠️ {acc} accident(s) recorded — buyers typically discount by 5–10 % per incident."
        )

    # Service history
    expected_services = age * 2.0
    if num_svc < expected_services * 0.5:
        candidate_reasons["service_score"] = (
            "🔧 Sparse service history detected — well-documented vehicles command a premium."
        )
    elif not auth_svc:
        candidate_reasons["service_score"] = (
            "🔧 Non-authorised service history — OEM dealer records add resale confidence."
        )

    # Climate penalty
    from src.features.engineering import get_climate_factor
    cf = get_climate_factor(city)
    if cf >= 1.10:
        candidate_reasons["climate_factor"] = (
            f"🌡️ Registered in {city} — combined heat & humidity cause above-average degradation."
        )
    elif cf > 1.0:
        candidate_reasons["climate_factor"] = (
            f"☀️ Registered in {city} — harsh climate conditions modestly reduce resale value."
        )

    # EV-specific (rapid tech evolution = faster residual decline)
    if fuel == "electric":
        candidate_reasons["is_ev"] = (
            "⚡ EVs face faster residual value erosion due to rapid battery tech improvement cycles."
        )

    # Luxury (high absolute depreciation but sometimes better % retention)
    if vehicle.get("ex_showroom_price_lakh", 0) >= 30:
        candidate_reasons["is_luxury"] = (
            "💎 Luxury vehicles carry high absolute depreciation in the first 3 years."
        )

    # Sort candidates by feature importance (most important first)
    sorted_reasons = sorted(
        candidate_reasons.items(),
        key=lambda kv: feature_importance.get(kv[0], 0.0),
        reverse=True,
    )

    # If no specific concerns, return a positive message
    if not sorted_reasons:
        return [
            "✅ Vehicle profile is well-maintained with no major depreciation red flags.",
            "📈 Good service history and moderate mileage support a healthy residual value.",
        ]

    return [reason for _, reason in sorted_reasons[:5]]


# ===========================================================================
# Maintenance risk explainability
# ===========================================================================

def explain_maintenance_risk(vehicle: dict[str, Any], risk_score: float) -> list[str]:
    """Generate plain-English maintenance risk explanation for a given risk score.

    Parameters
    ----------
    vehicle:
        Raw vehicle input dict.
    risk_score:
        Normalised risk score in [0, 1] produced by the maintenance model.
        0 = no risk, 1 = immediate intervention required.

    Returns
    -------
    list[str]
        2–5 explanation strings suitable for display in a Streamlit info box.
    """
    import datetime
    current_year: int = datetime.date.today().year

    total_km: int    = int(vehicle.get("total_km", 0))
    last_svc_km: int = int(vehicle.get("last_service_km", 0))
    km_gap: int      = max(total_km - last_svc_km, 0)

    mfg_year: int    = int(vehicle.get("manufacture_year", current_year - 3))
    age: float       = max(current_year - mfg_year, 0.5)
    annual_km: float = total_km / age
    fuel: str        = vehicle.get("fuel_type", "petrol").lower()
    num_acc: int     = int(vehicle.get("num_accidents", 0))

    # --- Risk band label ---
    band_label = "Low"
    band_emoji = "🟢"
    for threshold, label, emoji in _RISK_BANDS:
        if risk_score < threshold:
            band_label = label
            band_emoji = emoji
            break

    reasons: list[str] = [
        f"{band_emoji} Overall maintenance risk: **{band_label}** "
        f"(score: {risk_score:.2f} / 1.00)"
    ]

    # Service gap
    if km_gap > 10_000:
        reasons.append(
            f"🔴 Service overdue by {km_gap - 7_500:,} km — immediate service recommended."
        )
    elif km_gap > 7_500:
        reasons.append(
            f"🟠 Last service was {km_gap:,} km ago — schedule a service soon."
        )
    elif km_gap > 5_000:
        reasons.append(
            f"🟡 {km_gap:,} km since last service — approaching standard service interval."
        )

    # High annual usage
    if annual_km > 25_000:
        reasons.append(
            f"🛣️ Very high annual usage ({annual_km:,.0f} km/year) — consider bi-annual servicing."
        )
    elif annual_km > 18_000:
        reasons.append(
            f"🛣️ Above-average mileage ({annual_km:,.0f} km/year) increases wear rate."
        )

    # Age-related wear
    if age >= 8:
        reasons.append(
            f"⏳ Vehicle is {age:.0f} years old — ageing components (belts, seals, suspension) "
            "warrant a comprehensive inspection."
        )
    elif age >= 5:
        reasons.append(
            f"⏳ At {age:.0f} years, proactive replacement of wear items (brake pads, filters) "
            "is advisable."
        )

    # Accident-related structural concern
    if vehicle.get("major_accident", False):
        reasons.append(
            "💥 Major accident history — structural and hidden electrical damage should be "
            "inspected by a certified technician."
        )
    elif num_acc > 1:
        reasons.append(
            f"⚠️ {num_acc} accidents recorded — cumulative chassis stress may accelerate "
            "suspension and alignment wear."
        )

    # EV battery maintenance note
    if fuel == "electric":
        battery_pct = float(vehicle.get("battery_health_pct", 100.0))
        if battery_pct < 80:
            reasons.append(
                f"⚡ Battery health at {battery_pct:.0f}% — below 80% threshold; "
                "battery reconditioning or replacement may be needed."
            )
        else:
            reasons.append(
                f"⚡ Battery health: {battery_pct:.0f}% — within acceptable range."
            )

    return reasons[:6]  # cap at 6 items for UI clarity


# ===========================================================================
# SHAP display formatter
# ===========================================================================

def format_shap_for_display(shap_dict: dict[str, float]) -> list[dict[str, Any]]:
    """Format a feature-importance / SHAP-value dict for a Plotly bar chart.

    Converts raw importance/SHAP values into a list of records that can be
    fed directly into a ``px.bar`` call or a ``st.dataframe`` table.

    Parameters
    ----------
    shap_dict:
        Mapping of ``{feature_name: shap_value}`` where positive values
        increase the prediction and negative values decrease it.
        (If using plain feature importances rather than SHAP, all values
        will be non-negative and ``direction`` will always be ``"positive"``.)

    Returns
    -------
    list[dict]
        Each dict has three keys:

        =================== ==============================================
        ``feature``         Human-readable feature label (str)
        ``impact``          Absolute SHAP/importance value (float)
        ``direction``       ``"positive"`` or ``"negative"`` (str)
        =================== ==============================================

        Records are sorted by ``impact`` descending.

    Examples
    --------
    >>> fmt = format_shap_for_display({"age_years": 0.35, "log_mileage": -0.12})
    >>> fmt[0]
    {'feature': 'Age (years)', 'impact': 0.35, 'direction': 'positive'}
    """
    # Human-readable label mapping for known AUTOVAULT features
    _LABEL_MAP: dict[str, str] = {
        "age_years":            "Age (years)",
        "log_mileage":          "Mileage (log)",
        "annual_km":            "Annual KM",
        "age_sq":               "Age² (non-linear)",
        "mileage_per_year":     "Mileage / Year",
        "brand_tier_encoded":   "Brand Tier",
        "fuel_encoded":         "Fuel Type",
        "is_ev":                "Is Electric",
        "is_hybrid":            "Is Hybrid",
        "is_luxury":            "Is Luxury",
        "price_segment":        "Price Segment",
        "service_score":        "Service Quality",
        "accident_penalty":     "Accident History",
        "popularity_score":     "Resale Popularity",
        "climate_factor":       "Climate Harshness",
        "fuel_type_encoded":    "Fuel Type",
        "brand_tier":           "Brand Tier",
        "last_service_km_gap":  "KM Since Last Service",
        "service_overdue_flag": "Service Overdue",
        "high_intensity_flag":  "High Usage Intensity",
        "km":                   "Total Odometer (KM)",
        "usage_intensity":      "Usage Intensity",
        "tyre_score":           "Tyre Condition",
        "battery_health":       "Battery Health",
    }

    records: list[dict[str, Any]] = []
    for feature, value in shap_dict.items():
        label = _LABEL_MAP.get(feature, feature.replace("_", " ").title())
        records.append(
            {
                "feature":   label,
                "impact":    abs(float(value)),
                "direction": "positive" if float(value) >= 0 else "negative",
            }
        )

    # Sort by descending absolute impact
    records.sort(key=lambda r: r["impact"], reverse=True)
    return records
