"""
Feature Engineering for AUTOVAULT AI
======================================
Transforms raw vehicle input dictionaries into ML-ready pandas DataFrames.

Each public `engineer_*_features()` function targets a specific model domain
(depreciation, maintenance, health) and returns a single-row DataFrame whose
columns exactly match the feature names the corresponding trained model expects.

Design notes:
  - All encodings are deterministic (no fitted encoders needed at inference).
  - Climate / brand / fuel factors are derived from lookup tables defined here.
  - Intermediate helpers are intentionally small and unit-testable.
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Brand tier mapping
# Tiers drive depreciation rates, maintenance cost multipliers, and resale
# demand. Brands not found in any tier fall back to 'volume'.
# ---------------------------------------------------------------------------
BRAND_TIERS: dict[str, list[str]] = {
    "premium": ["Volkswagen", "Skoda", "Hyundai", "Kia", "Toyota", "Honda"],
    "volume":  ["Maruti Suzuki", "Tata", "Mahindra"],
    "luxury":  ["BMW", "Mercedes-Benz", "Audi"],
    "new_ev":  ["MG", "BYD"],
}

# Numeric encoding for brand tiers (used in tree-based models as ordinal proxy)
_BRAND_TIER_ORDINAL: dict[str, int] = {
    "volume":  0,
    "premium": 1,
    "new_ev":  2,
    "luxury":  3,
}

# ---------------------------------------------------------------------------
# City climate classification
# High-temperature and/or high-humidity cities accelerate rubber/seal
# degradation, battery stress, and corrosion — modelled as a penalty factor.
# ---------------------------------------------------------------------------
HIGH_TEMP_CITIES: list[str] = [
    "Chennai", "Hyderabad", "Ahmedabad", "Jaipur", "Nagpur", "Pune",
]
HUMID_CITIES: list[str] = [
    "Mumbai", "Kolkata", "Chennai", "Kochi",
]

# ---------------------------------------------------------------------------
# Fuel type ordinal encoding
# Used in tree models; the numbers carry no linear relationship — they just
# let the model split on fuel type cleanly.
# ---------------------------------------------------------------------------
_FUEL_ORDINAL: dict[str, int] = {
    "petrol":   0,
    "diesel":   1,
    "cng":      2,
    "hybrid":   3,
    "electric": 4,
}

# ---------------------------------------------------------------------------
# Popularity / demand index for 20 well-known Indian vehicle models
# Scale: 0.0 (very low resale demand) → 1.0 (highest demand)
# Sourced from historical used-car platform listing velocity data (proxy).
# ---------------------------------------------------------------------------
_POPULARITY_SCORES: dict[str, float] = {
    # Maruti Suzuki
    "Swift":          0.92,
    "Baleno":         0.88,
    "WagonR":         0.85,
    "Dzire":          0.87,
    # Hyundai
    "i20":            0.86,
    "Creta":          0.90,
    "Venue":          0.82,
    # Tata
    "Nexon":          0.83,
    "Punch":          0.80,
    "Tiago":          0.76,
    # Mahindra
    "Scorpio":        0.81,
    "XUV700":         0.79,
    # Honda
    "City":           0.84,
    "Amaze":          0.75,
    # Toyota
    "Innova Crysta":  0.88,
    "Fortuner":       0.85,
    # Volkswagen
    "Polo":           0.72,
    "Taigun":         0.74,
    # EV-specific
    "Nexon EV":       0.78,
    "ZS EV":          0.70,
}
_DEFAULT_POPULARITY: float = 0.65  # fallback for unlisted models

# ---------------------------------------------------------------------------
# Vehicle type annual-km thresholds (km/year)
# Used to normalise usage intensity relative to expected usage per segment.
# ---------------------------------------------------------------------------
_EXPECTED_ANNUAL_KM: dict[str, int] = {
    "hatchback": 12_000,
    "sedan":     14_000,
    "suv":       15_000,
    "muv":       18_000,
    "ev":        10_000,  # EV owners tend to drive more in city, shorter trips
    "truck":     40_000,
    "commercial":50_000,
}
_DEFAULT_EXPECTED_KM: int = 14_000

# ---------------------------------------------------------------------------
# Price segment boundaries (ex-showroom, INR lakhs)
# ---------------------------------------------------------------------------
_PRICE_SEGMENTS: list[tuple[float, str]] = [
    (5.0,   "budget"),
    (10.0,  "economy"),
    (18.0,  "mid"),
    (30.0,  "upper_mid"),
    (60.0,  "premium"),
    (float("inf"), "luxury"),
]
_PRICE_SEGMENT_ORDINAL: dict[str, int] = {
    "budget":    0,
    "economy":   1,
    "mid":       2,
    "upper_mid": 3,
    "premium":   4,
    "luxury":    5,
}


# ===========================================================================
# Helper / primitive functions
# ===========================================================================

def get_brand_tier(brand: str) -> str:
    """Return the AUTOVAULT brand tier for a given manufacturer name.

    Parameters
    ----------
    brand:
        Manufacturer name exactly as stored in the vehicle record
        (e.g. ``"Maruti Suzuki"``, ``"BMW"``).

    Returns
    -------
    str
        One of ``"volume"``, ``"premium"``, ``"luxury"``, ``"new_ev"``.
        Defaults to ``"volume"`` if the brand is not found in any tier.

    Examples
    --------
    >>> get_brand_tier("Toyota")
    'premium'
    >>> get_brand_tier("Unknown Brand")
    'volume'
    """
    brand_clean = brand.strip()
    for tier, brands in BRAND_TIERS.items():
        if brand_clean in brands:
            return tier
    return "volume"


def get_climate_factor(city: str) -> float:
    """Return a climate harshness multiplier for the given city.

    The factor represents how much faster environmental conditions accelerate
    vehicle degradation relative to a neutral (temperate, low-humidity) city.

    Parameters
    ----------
    city:
        City name from the vehicle registration / owner record.

    Returns
    -------
    float
        ``1.0`` — neutral / mild climate.
        ``1.05`` — high temperature only.
        ``1.05`` — high humidity only.
        ``1.10`` — both high temperature *and* high humidity (compounding).

    Notes
    -----
    The penalty is intentionally modest because vehicles sold through
    authorised dealers in harsh-climate cities already factor in
    regional service schedules. This factor is used as a soft correction.
    """
    city_clean = city.strip()
    is_hot   = city_clean in HIGH_TEMP_CITIES
    is_humid = city_clean in HUMID_CITIES

    if is_hot and is_humid:
        return 1.10  # compounding stress (e.g. Chennai)
    if is_hot:
        return 1.05  # dry heat (e.g. Jaipur, Ahmedabad)
    if is_humid:
        return 1.05  # humid but not extreme heat (e.g. Kochi)
    return 1.00      # neutral (e.g. Bengaluru, Delhi, Chandigarh)


def calculate_usage_intensity(annual_km: int, vehicle_type: str) -> float:
    """Compute a normalised usage intensity score on the [0, 1] scale.

    Compares the vehicle's actual annual kilometres to the segment-expected
    annual kilometres. Values > 1.0 are clipped to 1.0 to keep the feature
    bounded.

    Parameters
    ----------
    annual_km:
        Kilometres driven per year (total_km / age_years).
    vehicle_type:
        Vehicle segment identifier — one of the keys in
        ``_EXPECTED_ANNUAL_KM`` (case-insensitive).

    Returns
    -------
    float
        0.0 → barely used / very low mileage.
        0.5 → exactly at segment average usage.
        1.0 → extremely heavy usage (≥ 2× segment average).

    Examples
    --------
    >>> calculate_usage_intensity(15_000, "hatchback")
    0.625
    >>> calculate_usage_intensity(30_000, "hatchback")
    1.0
    """
    vtype = vehicle_type.lower().strip()
    expected = _EXPECTED_ANNUAL_KM.get(vtype, _DEFAULT_EXPECTED_KM)

    # Intensity as ratio capped at 2× expected (maps linearly to 0-1)
    ratio = annual_km / (2.0 * expected)
    return float(np.clip(ratio, 0.0, 1.0))


def _get_price_segment(ex_showroom_lakh: float) -> str:
    """Map an ex-showroom price to a named segment string."""
    for threshold, segment in _PRICE_SEGMENTS:
        if ex_showroom_lakh < threshold:
            return segment
    return "luxury"


def _service_score(vehicle: dict[str, Any]) -> float:
    """Compute a normalised [0, 1] service history quality score.

    Higher scores indicate better-maintained vehicles (more service records,
    manufacturer-authorised servicing, OBD data present).

    Parameters
    ----------
    vehicle:
        Raw vehicle input dict. Relevant keys:
        ``num_services``  — number of logged service events (int, default 0).
        ``authorised_service`` — bool, True if serviced at OEM dealer.
        ``has_obd_data``  — bool, True if OBD-II telematics are available.
    """
    age_years: float = max(vehicle.get("age_years", 1.0), 1.0)
    num_services: int = int(vehicle.get("num_services", 0))

    # Expected services: roughly every 6 months
    expected_services = age_years * 2.0
    service_ratio = min(num_services / max(expected_services, 1.0), 1.5)

    # Bonuses for authorised service and telematics data availability
    auth_bonus = 0.15 if vehicle.get("authorised_service", False) else 0.0
    obd_bonus  = 0.10 if vehicle.get("has_obd_data", False) else 0.0

    raw_score = (service_ratio / 1.5) * 0.75 + auth_bonus + obd_bonus
    return float(np.clip(raw_score, 0.0, 1.0))


def _accident_penalty(vehicle: dict[str, Any]) -> float:
    """Compute a depreciation penalty factor for accident history.

    Returns
    -------
    float
        0.0 — no accident history.
        0.05–0.10 — minor incidents.
        0.15–0.25 — major structural damage.
    """
    num_accidents: int = int(vehicle.get("num_accidents", 0))
    major_accident: bool = bool(vehicle.get("major_accident", False))

    if num_accidents == 0:
        return 0.0
    # Each minor accident adds 5% penalty, major adds a flat 15% on top
    minor_penalty = min(num_accidents * 0.05, 0.15)
    major_penalty = 0.15 if major_accident else 0.0
    return float(np.clip(minor_penalty + major_penalty, 0.0, 0.30))


# ===========================================================================
# Core feature engineering functions
# ===========================================================================

def engineer_depreciation_features(vehicle: dict[str, Any]) -> pd.DataFrame:
    """Build a single-row DataFrame of features for the depreciation model.

    Parameters
    ----------
    vehicle:
        Raw vehicle input dictionary. Expected keys (all with sensible
        defaults if absent):

        =================== =========================================================
        Key                 Description
        =================== =========================================================
        ``brand``           Manufacturer name (str)
        ``model``           Model name (str)
        ``manufacture_year``Year of manufacture (int)
        ``total_km``        Odometer reading in km (int)
        ``fuel_type``       One of petrol/diesel/cng/hybrid/electric (str)
        ``ex_showroom_price_lakh`` Original ex-showroom price in INR lakhs (float)
        ``city``            Registration city (str)
        ``num_accidents``   Number of logged accidents (int, default 0)
        ``major_accident``  True if any accident was structural (bool, default False)
        ``num_services``    Number of service records (int, default 0)
        ``authorised_service`` True if serviced at OEM dealer (bool, default False)
        ``has_obd_data``    True if telematics data is available (bool, default False)
        =================== =========================================================

    Returns
    -------
    pd.DataFrame
        Single-row DataFrame with the following columns:

        - ``age_years``         — Vehicle age in decimal years
        - ``log_mileage``       — Natural log of (total_km + 1)
        - ``annual_km``         — Estimated kilometres driven per year
        - ``age_sq``            — age_years² (captures non-linear depreciation curve)
        - ``mileage_per_year``  — alias of annual_km (explicit model feature)
        - ``brand_tier_encoded``— Ordinal brand tier (0=volume … 3=luxury)
        - ``fuel_encoded``      — Ordinal fuel type (0=petrol … 4=electric)
        - ``is_ev``             — Binary flag: 1 if electric
        - ``is_hybrid``         — Binary flag: 1 if hybrid
        - ``is_luxury``         — Binary flag: 1 if luxury tier
        - ``price_segment``     — Ordinal price segment (0=budget … 5=luxury)
        - ``service_score``     — Service quality score [0, 1]
        - ``accident_penalty``  — Depreciation penalty from accidents [0, 0.30]
        - ``popularity_score``  — Resale demand index [0, 1]
        - ``climate_factor``    — Climate harshness multiplier [1.0, 1.10]
    """
    import datetime
    current_year: int = datetime.date.today().year

    brand: str      = vehicle.get("brand", "Maruti Suzuki")
    model_name: str = vehicle.get("model", "")
    mfg_year: int   = int(vehicle.get("manufacture_year", current_year - 3))
    total_km: int   = int(vehicle.get("total_km", 30_000))
    fuel_type: str  = vehicle.get("fuel_type", "petrol").lower().strip()
    price_lakh: float = float(vehicle.get("ex_showroom_price_lakh", 10.0))
    city: str       = vehicle.get("city", "Delhi")

    # --- Derived time / mileage features ---
    age_years: float = max(current_year - mfg_year, 0.5)  # floor at 6 months
    log_mileage: float = math.log1p(total_km)              # log(km + 1), stable at 0
    annual_km: float = total_km / age_years
    age_sq: float = age_years ** 2

    # --- Brand / tier encoding ---
    tier: str = get_brand_tier(brand)
    brand_tier_encoded: int = _BRAND_TIER_ORDINAL.get(tier, 0)

    # --- Fuel encoding + binary flags ---
    fuel_encoded: int = _FUEL_ORDINAL.get(fuel_type, 0)
    is_ev: int      = 1 if fuel_type == "electric" else 0
    is_hybrid: int  = 1 if fuel_type == "hybrid" else 0
    is_luxury: int  = 1 if tier == "luxury" else 0

    # --- Price segment ---
    segment_str: str = _get_price_segment(price_lakh)
    price_segment: int = _PRICE_SEGMENT_ORDINAL.get(segment_str, 1)

    # --- Service quality & accident history ---
    svc_score: float   = _service_score(vehicle)
    acc_penalty: float = _accident_penalty(vehicle)

    # --- Popularity / resale demand ---
    popularity: float = _POPULARITY_SCORES.get(model_name, _DEFAULT_POPULARITY)

    # --- Climate harshness ---
    climate: float = get_climate_factor(city)

    row: dict[str, Any] = {
        "age_years":          age_years,
        "log_mileage":        log_mileage,
        "annual_km":          annual_km,
        "age_sq":             age_sq,
        "mileage_per_year":   annual_km,        # explicit alias expected by model
        "brand_tier_encoded": brand_tier_encoded,
        "fuel_encoded":       fuel_encoded,
        "is_ev":              is_ev,
        "is_hybrid":          is_hybrid,
        "is_luxury":          is_luxury,
        "price_segment":      price_segment,
        "service_score":      svc_score,
        "accident_penalty":   acc_penalty,
        "popularity_score":   popularity,
        "climate_factor":     climate,
    }
    return pd.DataFrame([row])


def engineer_maintenance_features(vehicle: dict[str, Any]) -> pd.DataFrame:
    """Build a single-row DataFrame of features for the maintenance risk model.

    Parameters
    ----------
    vehicle:
        Raw vehicle input dictionary. Expected keys:

        ======================== ===================================================
        Key                      Description
        ======================== ===================================================
        ``brand``                Manufacturer name (str)
        ``manufacture_year``     Year of manufacture (int)
        ``total_km``             Odometer reading in km (int)
        ``fuel_type``            petrol/diesel/cng/hybrid/electric (str)
        ``last_service_km``      Odometer at last service event (int, default 0)
        ``vehicle_type``         hatchback/sedan/suv/muv/ev/truck (str)
        ======================== ===================================================

    Returns
    -------
    pd.DataFrame
        Single-row DataFrame with:

        - ``age_years``            — Vehicle age in decimal years
        - ``km``                   — Total odometer reading
        - ``annual_km``            — Estimated km/year
        - ``fuel_type_encoded``    — Ordinal fuel type (0=petrol … 4=electric)
        - ``brand_tier``           — Ordinal brand tier (0=volume … 3=luxury)
        - ``last_service_km_gap``  — km driven since last service event
        - ``service_overdue_flag`` — 1 if gap > 7 500 km (typical OEM interval)
        - ``high_intensity_flag``  — 1 if usage intensity > 0.65
    """
    import datetime
    current_year: int = datetime.date.today().year

    brand: str        = vehicle.get("brand", "Maruti Suzuki")
    mfg_year: int     = int(vehicle.get("manufacture_year", current_year - 3))
    total_km: int     = int(vehicle.get("total_km", 30_000))
    fuel_type: str    = vehicle.get("fuel_type", "petrol").lower().strip()
    last_svc_km: int  = int(vehicle.get("last_service_km", 0))
    vtype: str        = vehicle.get("vehicle_type", "sedan").lower().strip()

    age_years: float  = max(current_year - mfg_year, 0.5)
    annual_km: float  = total_km / age_years

    fuel_encoded: int = _FUEL_ORDINAL.get(fuel_type, 0)
    tier: str         = get_brand_tier(brand)
    brand_tier: int   = _BRAND_TIER_ORDINAL.get(tier, 0)

    # km gap since last service — main predictor of near-term maintenance need
    last_service_km_gap: int = max(total_km - last_svc_km, 0)

    # OEM service intervals are typically 7 500–10 000 km; flag at 7 500 km
    service_overdue_flag: int = 1 if last_service_km_gap > 7_500 else 0

    # High-intensity flag: vehicles driven harder than 65 % of max expected
    usage_intensity: float   = calculate_usage_intensity(int(annual_km), vtype)
    high_intensity_flag: int = 1 if usage_intensity > 0.65 else 0

    row: dict[str, Any] = {
        "age_years":            age_years,
        "km":                   total_km,
        "annual_km":            annual_km,
        "fuel_type_encoded":    fuel_encoded,
        "brand_tier":           brand_tier,
        "last_service_km_gap":  last_service_km_gap,
        "service_overdue_flag": service_overdue_flag,
        "high_intensity_flag":  high_intensity_flag,
    }
    return pd.DataFrame([row])


def engineer_health_features(vehicle: dict[str, Any]) -> pd.DataFrame:
    """Build a single-row DataFrame of features for the vehicle health model.

    Combines mechanical, historical, and environmental signals into a
    feature vector that the health score regressor can ingest directly.

    Parameters
    ----------
    vehicle:
        Raw vehicle input dictionary. Expected keys:

        ========================= ==================================================
        Key                       Description
        ========================= ==================================================
        ``brand``                 Manufacturer name (str)
        ``manufacture_year``      Year of manufacture (int)
        ``total_km``              Odometer reading in km (int)
        ``fuel_type``             petrol/diesel/cng/hybrid/electric (str)
        ``vehicle_type``          hatchback/sedan/suv/muv/ev/truck (str)
        ``city``                  Registration city (str)
        ``num_accidents``         Number of logged accidents (int, default 0)
        ``major_accident``        True if any accident was structural (bool)
        ``num_services``          Number of service records (int, default 0)
        ``authorised_service``    True if serviced at OEM dealer (bool)
        ``has_obd_data``          True if telematics available (bool)
        ``last_service_km``       Odometer at last service (int, default 0)
        ``tyre_condition``        Subjective tyre rating 0–10 (float, default 7.0)
        ``battery_health_pct``    Battery SoH % for EVs/hybrids (float, default 100)
        ========================= ==================================================

    Returns
    -------
    pd.DataFrame
        Single-row DataFrame with:

        - ``age_years``           — Vehicle age in decimal years
        - ``log_mileage``         — log(total_km + 1)
        - ``annual_km``           — km/year estimate
        - ``usage_intensity``     — Normalised usage intensity [0, 1]
        - ``brand_tier_encoded``  — Ordinal brand tier
        - ``fuel_encoded``        — Ordinal fuel type
        - ``is_ev``               — 1 if electric
        - ``service_score``       — Service quality score [0, 1]
        - ``accident_penalty``    — Accident history penalty [0, 0.30]
        - ``climate_factor``      — Climate harshness multiplier
        - ``service_overdue_flag``— 1 if km since last service > 7 500
        - ``high_intensity_flag`` — 1 if usage intensity > 0.65
        - ``tyre_score``          — Normalised tyre condition [0, 1]
        - ``battery_health``      — Battery SoH fraction [0, 1]
    """
    import datetime
    current_year: int = datetime.date.today().year

    brand: str         = vehicle.get("brand", "Maruti Suzuki")
    mfg_year: int      = int(vehicle.get("manufacture_year", current_year - 3))
    total_km: int      = int(vehicle.get("total_km", 30_000))
    fuel_type: str     = vehicle.get("fuel_type", "petrol").lower().strip()
    vtype: str         = vehicle.get("vehicle_type", "sedan").lower().strip()
    city: str          = vehicle.get("city", "Delhi")
    last_svc_km: int   = int(vehicle.get("last_service_km", 0))
    tyre_raw: float    = float(vehicle.get("tyre_condition", 7.0))      # 0–10 scale
    battery_raw: float = float(vehicle.get("battery_health_pct", 100.0))  # 0–100 %

    age_years: float  = max(current_year - mfg_year, 0.5)
    log_mileage: float = math.log1p(total_km)
    annual_km: float   = total_km / age_years

    usage_intensity: float = calculate_usage_intensity(int(annual_km), vtype)

    tier: str            = get_brand_tier(brand)
    brand_tier_encoded: int = _BRAND_TIER_ORDINAL.get(tier, 0)
    fuel_encoded: int    = _FUEL_ORDINAL.get(fuel_type, 0)
    is_ev: int           = 1 if fuel_type == "electric" else 0

    svc_score: float     = _service_score(vehicle)
    acc_penalty: float   = _accident_penalty(vehicle)
    climate: float       = get_climate_factor(city)

    last_svc_gap: int    = max(total_km - last_svc_km, 0)
    svc_overdue: int     = 1 if last_svc_gap > 7_500 else 0
    high_intensity: int  = 1 if usage_intensity > 0.65 else 0

    # Normalise tyre condition from 0–10 scale to 0–1
    tyre_score: float    = float(np.clip(tyre_raw / 10.0, 0.0, 1.0))

    # Normalise battery health from 0–100 % to 0–1 fraction
    battery_health: float = float(np.clip(battery_raw / 100.0, 0.0, 1.0))

    row: dict[str, Any] = {
        "age_years":            age_years,
        "log_mileage":          log_mileage,
        "annual_km":            annual_km,
        "usage_intensity":      usage_intensity,
        "brand_tier_encoded":   brand_tier_encoded,
        "fuel_encoded":         fuel_encoded,
        "is_ev":                is_ev,
        "service_score":        svc_score,
        "accident_penalty":     acc_penalty,
        "climate_factor":       climate,
        "service_overdue_flag": svc_overdue,
        "high_intensity_flag":  high_intensity,
        "tyre_score":           tyre_score,
        "battery_health":       battery_health,
    }
    return pd.DataFrame([row])
