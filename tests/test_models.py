"""
tests/test_models.py
====================
Pytest test suite for VehicleHealthModel and MaintenanceModel.

Tests cover:
  - Health score bounded in [0, 100]
  - Accident history reduces health score
  - Older / higher-mileage vehicles score lower
  - Maintenance risk score bounded in [0, 100]
  - Annual cost estimate is a positive non-zero value
  - Incomplete service history increases maintenance risk

Run with:
    pytest tests/test_models.py -v
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import pytest
from src.models.health_model import VehicleHealthModel
from src.models.maintenance_model import MaintenanceModel

# ---------------------------------------------------------------------------
# Module-level model instances (stateless after initialisation)
# ---------------------------------------------------------------------------
health_model = VehicleHealthModel()
maint_model  = MaintenanceModel()


# ---------------------------------------------------------------------------
# Helper builders
# ---------------------------------------------------------------------------

def _healthy_vehicle(**overrides):
    """Return a default well-maintained petrol vehicle dict."""
    base = {
        'age_years':                3,
        'mileage_km':               35_000,
        'annual_km':                12_000,
        'fuel_type':                'Petrol',
        'service_history_complete': True,
        'accident_history':         False,
        'city':                     'Mumbai',
    }
    return {**base, **overrides}


def _maintenance_vehicle(**overrides):
    """Return a default vehicle dict for maintenance prediction."""
    base = {
        'brand':                    'Tata',
        'model':                    'Nexon',
        'fuel_type':                'Petrol',
        'age_years':                4,
        'mileage_km':               55_000,
        'annual_km':                14_000,
        'service_history_complete': True,
    }
    return {**base, **overrides}


# ---------------------------------------------------------------------------
# VehicleHealthModel — Bounds Tests
# ---------------------------------------------------------------------------

def test_health_score_in_range():
    """
    Overall health score must lie in [0, 100] for a typical vehicle.
    This is the primary contract that the UI progress bar depends on.
    """
    result = health_model.score_vehicle(_healthy_vehicle())
    score  = result['overall_health']

    assert 0 <= score <= 100, \
        f"overall_health={score} is outside the valid [0, 100] range"


def test_health_score_returns_dict():
    """
    score_vehicle() must return a dict with at least the 'overall_health'
    key so callers can access it by name without positional fragility.
    """
    result = health_model.score_vehicle(_healthy_vehicle())
    assert isinstance(result, dict),       "score_vehicle() must return a dict"
    assert 'overall_health' in result,     "Result must contain 'overall_health'"


def test_health_score_perfect_vehicle():
    """
    A brand-new, never-crashed vehicle with complete service records should
    score highly (≥ 85 out of 100).
    """
    new_vehicle = _healthy_vehicle(age_years=0, mileage_km=0)
    result      = health_model.score_vehicle(new_vehicle)
    assert result['overall_health'] >= 85, \
        "A brand-new vehicle should score ≥ 85 health"


def test_health_score_clamps_at_zero():
    """
    Even the worst vehicle configuration must not produce a negative score.
    """
    beaten_up = _healthy_vehicle(
        age_years=15,
        mileage_km=250_000,
        accident_history=True,
        service_history_complete=False,
    )
    result = health_model.score_vehicle(beaten_up)
    assert result['overall_health'] >= 0, "Health score must never go negative"


# ---------------------------------------------------------------------------
# VehicleHealthModel — Directional / Monotonicity Tests
# ---------------------------------------------------------------------------

def test_accident_reduces_health():
    """
    A vehicle with accident history must score lower than an otherwise
    identical vehicle with a clean record.
    """
    base     = _healthy_vehicle()
    accident = _healthy_vehicle(accident_history=True)

    base_score     = health_model.score_vehicle(base)['overall_health']
    accident_score = health_model.score_vehicle(accident)['overall_health']

    assert base_score > accident_score, \
        "Accident history must reduce the overall health score"


def test_older_vehicle_scores_lower():
    """
    Ageing degrades vehicle health — a 8-year-old car should score lower
    than an otherwise identical 1-year-old car.
    """
    young = _healthy_vehicle(age_years=1, mileage_km=12_000)
    old   = _healthy_vehicle(age_years=8, mileage_km=96_000)

    assert health_model.score_vehicle(old)['overall_health'] < \
           health_model.score_vehicle(young)['overall_health'], \
        "Older vehicle must have a lower health score"


def test_incomplete_service_reduces_health():
    """
    Missing service records indicate uncertain mechanical condition —
    this must be reflected as a lower health score.
    """
    serviced   = _healthy_vehicle(service_history_complete=True)
    unserviced = _healthy_vehicle(service_history_complete=False)

    assert health_model.score_vehicle(unserviced)['overall_health'] < \
           health_model.score_vehicle(serviced)['overall_health'], \
        "Incomplete service history must lower health score"


def test_high_mileage_reduces_health():
    """
    Higher mileage indicates more wear — health score should decrease
    as odometer reading increases, all else equal.
    """
    low  = _healthy_vehicle(mileage_km=10_000)
    high = _healthy_vehicle(mileage_km=120_000)

    assert health_model.score_vehicle(high)['overall_health'] < \
           health_model.score_vehicle(low)['overall_health'], \
        "High mileage must reduce health score vs low mileage"


# ---------------------------------------------------------------------------
# MaintenanceModel — Bounds Tests
# ---------------------------------------------------------------------------

def test_maintenance_risk_score_in_range():
    """
    Risk score must lie in [0, 100]. This is the fundamental output contract
    for the risk gauge displayed in the UI.
    """
    result = maint_model.predict_events(_maintenance_vehicle())
    score  = result['risk_score']

    assert 0 <= score <= 100, \
        f"risk_score={score} is outside the valid [0, 100] range"


def test_maintenance_annual_cost_positive():
    """
    Annual maintenance cost estimate must be a positive, non-zero value.
    Even the best-maintained car has oil changes, tyre rotations, etc.
    """
    result = maint_model.predict_events(_maintenance_vehicle())
    assert result['annual_cost_estimate'] > 0, \
        "Annual maintenance cost estimate must be positive"


def test_maintenance_result_has_required_keys():
    """
    The result dict must contain 'risk_score' and 'annual_cost_estimate'
    at minimum — both are rendered in the UI.
    """
    result = maint_model.predict_events(_maintenance_vehicle())
    assert 'risk_score' in result,          "Missing key: 'risk_score'"
    assert 'annual_cost_estimate' in result, "Missing key: 'annual_cost_estimate'"


# ---------------------------------------------------------------------------
# MaintenanceModel — Directional / Monotonicity Tests
# ---------------------------------------------------------------------------

def test_incomplete_service_increases_risk():
    """
    Unknown maintenance history means higher uncertainty and risk —
    the model must penalise vehicles with incomplete service records.
    """
    serviced   = _maintenance_vehicle(service_history_complete=True)
    unserviced = _maintenance_vehicle(service_history_complete=False)

    risk_serviced   = maint_model.predict_events(serviced)['risk_score']
    risk_unserviced = maint_model.predict_events(unserviced)['risk_score']

    assert risk_unserviced > risk_serviced, \
        "Incomplete service history must increase maintenance risk score"


def test_older_vehicle_higher_risk():
    """
    Older vehicles with more wear should have a higher maintenance risk score.
    """
    new_vehicle = _maintenance_vehicle(age_years=1, mileage_km=12_000)
    old_vehicle = _maintenance_vehicle(age_years=9, mileage_km=110_000)

    new_risk = maint_model.predict_events(new_vehicle)['risk_score']
    old_risk = maint_model.predict_events(old_vehicle)['risk_score']

    assert old_risk > new_risk, \
        "Older high-mileage vehicle must have a higher maintenance risk score"


def test_ev_maintenance_lower_than_petrol():
    """
    EVs have fewer moving parts (no engine, gearbox, exhaust) so their
    annual maintenance cost estimate should be lower than a petrol equivalent.
    """
    petrol = _maintenance_vehicle(fuel_type='Petrol')
    ev     = _maintenance_vehicle(fuel_type='Electric')

    petrol_cost = maint_model.predict_events(petrol)['annual_cost_estimate']
    ev_cost     = maint_model.predict_events(ev)['annual_cost_estimate']

    assert ev_cost < petrol_cost, \
        "EV annual maintenance cost must be lower than petrol equivalent"
