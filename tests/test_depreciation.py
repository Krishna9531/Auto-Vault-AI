"""
tests/test_depreciation.py
==========================
Pytest test suite for the DepreciationModel.

Tests cover:
  - Output schema validation
  - EV vs petrol first-year depreciation comparison
  - Resale value < purchase price invariant
  - Accident & high-mileage penalty effects
  - Monotonically decreasing yearly value curve

Run with:
    pytest tests/test_depreciation.py -v
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import pytest
from src.models.depreciation_model import DepreciationModel

# ---------------------------------------------------------------------------
# Shared model instance (model is read-only / stateless after init)
# ---------------------------------------------------------------------------
model = DepreciationModel()


# ---------------------------------------------------------------------------
# Helper builders
# ---------------------------------------------------------------------------

def _petrol_vehicle(**overrides):
    """Return a base petrol vehicle dict with optional field overrides."""
    base = {
        'brand':                    'Hyundai',
        'model':                    'Creta',
        'fuel_type':                'Petrol',
        'purchase_price_lakh':      15.0,
        'age_years':                2,
        'mileage_km':               25_000,
        'annual_km':                12_000,
        'service_history_complete': True,
        'accident_history':         False,
    }
    return {**base, **overrides}


def _ev_vehicle(**overrides):
    """Return a base EV vehicle dict with optional field overrides."""
    base = {
        'brand':                    'Tata',
        'model':                    'Nexon EV',
        'fuel_type':                'Electric',
        'purchase_price_lakh':      17.5,
        'age_years':                2,
        'mileage_km':               30_000,
        'annual_km':                15_000,
        'service_history_complete': True,
        'accident_history':         False,
    }
    return {**base, **overrides}


# ---------------------------------------------------------------------------
# Schema / Output Structure Tests
# ---------------------------------------------------------------------------

def test_depreciation_returns_dict():
    """
    Model must return a dict with the three mandatory keys that all
    downstream consumers (UI, TCO, reports) depend on.
    """
    result = model.predict(_petrol_vehicle())

    assert isinstance(result, dict), "predict() must return a dict"
    assert 'current_value' in result,       "Missing key: 'current_value'"
    assert 'yearly_values' in result,       "Missing key: 'yearly_values'"
    assert 'depreciation_pct' in result,    "Missing key: 'depreciation_pct'"

    assert result['depreciation_pct'] > 0, "Depreciation % must be positive for a used vehicle"


def test_yearly_values_is_sequence():
    """
    yearly_values should be a list/sequence with at least one future year
    so the UI can plot the depreciation curve.
    """
    result = model.predict(_petrol_vehicle())
    yv = result['yearly_values']

    assert hasattr(yv, '__len__'), "yearly_values must be a sequence"
    assert len(yv) > 0,           "yearly_values must not be empty"


def test_depreciation_pct_in_valid_range():
    """
    Depreciation percentage must be between 0 and 100 for any realistic
    vehicle configuration — a >100% figure would mean negative value.
    """
    result = model.predict(_petrol_vehicle())
    assert 0 < result['depreciation_pct'] < 100


# ---------------------------------------------------------------------------
# EV vs Petrol Depreciation Tests
# ---------------------------------------------------------------------------

def test_ev_depreciates_faster_year1():
    """
    EVs currently depreciate faster than equivalent petrol cars in year 1
    due to rapid battery tech evolution and lower used-market demand.

    Both vehicles are brand new (age_years=0) so we compare the value
    remaining after one year of ownership.
    """
    petrol = _petrol_vehicle(age_years=0, mileage_km=0)
    ev     = {**petrol, 'fuel_type': 'Electric'}

    petrol_result = model.predict(petrol)
    ev_result     = model.predict(ev)

    # yearly_values[1] is value at end of year 1
    assert ev_result['yearly_values'][1] < petrol_result['yearly_values'][1], \
        "EV must have a lower residual value than petrol after year 1"


def test_ev_total_depreciation_pct_greater_than_petrol():
    """
    Over a 5-year hold, an EV's cumulative depreciation % should exceed
    that of a comparable petrol vehicle.
    """
    petrol_result = model.predict(_petrol_vehicle(age_years=5, mileage_km=60_000))
    ev_result     = model.predict(_ev_vehicle(age_years=5, mileage_km=60_000))

    assert ev_result['depreciation_pct'] >= petrol_result['depreciation_pct'], \
        "EV depreciation % should be >= petrol over 5 years"


# ---------------------------------------------------------------------------
# Resale Value Invariants
# ---------------------------------------------------------------------------

def test_resale_less_than_purchase():
    """
    Current value must always be strictly less than the original purchase
    price — cars are depreciating assets, not appreciating ones.
    """
    result = model.predict(_ev_vehicle())
    assert result['current_value'] < _ev_vehicle()['purchase_price_lakh'], \
        "Resale value must be less than purchase price"


def test_new_vehicle_value_close_to_purchase():
    """
    A brand-new vehicle (0 km, 0 years) should have a current value
    within 15% of its purchase price (first-year showroom depreciation allowed).
    """
    vehicle = _petrol_vehicle(age_years=0, mileage_km=0)
    result  = model.predict(vehicle)
    ratio   = result['current_value'] / vehicle['purchase_price_lakh']
    assert ratio >= 0.85, \
        f"New vehicle should retain ≥85% of value immediately; got {ratio:.2%}"


# ---------------------------------------------------------------------------
# Penalty / Modifier Tests
# ---------------------------------------------------------------------------

def test_accident_reduces_value():
    """
    A vehicle with accident history should have a lower residual value
    than an identical vehicle with a clean history.
    """
    clean    = _petrol_vehicle()
    damaged  = _petrol_vehicle(accident_history=True)

    clean_val   = model.predict(clean)['current_value']
    damaged_val = model.predict(damaged)['current_value']

    assert damaged_val < clean_val, \
        "Accident history must reduce current resale value"


def test_incomplete_service_reduces_value():
    """
    Missing service records lower buyer confidence and should reduce
    the predicted resale value.
    """
    serviced   = _petrol_vehicle(service_history_complete=True)
    unserviced = _petrol_vehicle(service_history_complete=False)

    assert model.predict(unserviced)['current_value'] < \
           model.predict(serviced)['current_value'], \
        "Incomplete service history must reduce resale value"


def test_high_mileage_reduces_value():
    """
    Higher odometer readings should yield a lower current residual value.
    """
    low_km  = _petrol_vehicle(mileage_km=10_000)
    high_km = _petrol_vehicle(mileage_km=80_000)

    assert model.predict(high_km)['current_value'] < \
           model.predict(low_km)['current_value'], \
        "Higher mileage must reduce resale value"


# ---------------------------------------------------------------------------
# Curve Shape Tests
# ---------------------------------------------------------------------------

def test_yearly_values_monotonically_decreasing():
    """
    Depreciation curves should be monotonically non-increasing — a car's
    value should never increase as it ages in the model.
    """
    result = model.predict(_petrol_vehicle(age_years=0, mileage_km=0))
    yv = list(result['yearly_values'].values()) \
        if isinstance(result['yearly_values'], dict) \
        else list(result['yearly_values'])

    for i in range(1, len(yv)):
        assert yv[i] <= yv[i - 1], \
            f"Yearly value increased from year {i - 1} to year {i}: {yv[i-1]} → {yv[i]}"
