"""
tests/test_tco.py
=================
Pytest test suite for the TCO (Total Cost of Ownership) engine.

Tests cover:
  - EMI calculation correctness
  - Fuel cost positivity
  - Net TCO sanity (costs exceed resale recovery)
  - EV electricity cost vs petrol cost comparison

Run with:
    pytest tests/test_tco.py -v
"""

import sys
from pathlib import Path

# Ensure project root is importable regardless of invocation directory
sys.path.append(str(Path(__file__).parent.parent))

import pytest
from src.finance.tco import TCOEngine

# ---------------------------------------------------------------------------
# Module-level fixture — engine is stateless so a single instance is fine
# ---------------------------------------------------------------------------
engine = TCOEngine()


# ---------------------------------------------------------------------------
# EMI Tests
# ---------------------------------------------------------------------------

def test_emi_calculation():
    """
    Basic sanity: EMI result must contain expected keys and positive values.
    Uses a ₹10 lakh loan at 8.5% p.a. for 60 months — a typical Indian car loan.
    """
    result = engine.calculate_emi(principal=1_000_000, rate=8.5, tenure_months=60)

    assert 'monthly_emi' in result, "Result must expose 'monthly_emi' key"
    assert 'total_interest' in result, "Result must expose 'total_interest' key"

    assert result['monthly_emi'] > 0, "Monthly EMI must be positive"
    assert result['total_interest'] > 0, "Interest on a non-zero loan must be positive"


def test_emi_zero_rate():
    """
    Edge case: at 0% interest the total repayment should equal principal.
    Avoids division-by-zero in some EMI formula implementations.
    """
    result = engine.calculate_emi(principal=600_000, rate=0.0, tenure_months=60)
    assert result['monthly_emi'] == pytest.approx(600_000 / 60, rel=1e-3)


def test_emi_single_month():
    """
    Degenerate tenure of 1 month — EMI should be (principal + one month interest).
    """
    result = engine.calculate_emi(principal=500_000, rate=12.0, tenure_months=1)
    assert result['monthly_emi'] > 500_000, "Single-month EMI must exceed principal"


# ---------------------------------------------------------------------------
# Fuel Cost Tests
# ---------------------------------------------------------------------------

def test_fuel_cost_positive():
    """
    Fuel cost for 15,000 km/year at 18 kmpl and ₹105/litre over 5 years
    must be a strictly positive number.
    """
    cost = engine.calculate_fuel_cost(15_000, 18.0, 105.0, 5)
    assert cost > 0, "Fuel cost must be positive"


def test_fuel_cost_proportional_to_distance():
    """
    Doubling annual km should (approximately) double the total fuel cost
    because price and efficiency are held constant.
    """
    base = engine.calculate_fuel_cost(10_000, 18.0, 100.0, 5)
    double = engine.calculate_fuel_cost(20_000, 18.0, 100.0, 5)
    assert double == pytest.approx(base * 2, rel=1e-6)


def test_fuel_cost_higher_with_lower_mileage():
    """
    A car with worse mileage should always cost more to run over the same period.
    """
    efficient = engine.calculate_fuel_cost(15_000, 25.0, 105.0, 5)
    guzzler   = engine.calculate_fuel_cost(15_000, 12.0, 105.0, 5)
    assert guzzler > efficient


# ---------------------------------------------------------------------------
# Net TCO Tests
# ---------------------------------------------------------------------------

def test_tco_net_positive():
    """
    Net TCO (total spend minus resale value) must be positive — you always
    spend more than you recover on a depreciating asset.
    """
    vehicle = {
        'purchase_price_lakh': 18.5,
        'fuel_type':           'Petrol',
        'claimed_mileage_kmpl': 17.0,
    }
    params = {
        'annual_km':         15_000,
        'ownership_years':   5,
        'fuel_price':        105.0,
        'loan_rate':         8.5,
        'down_payment_pct':  20,
        'tenure_months':     60,
        'resale_value_lakh': 8.7,
    }
    result = engine.calculate(vehicle, params)
    assert result['net_tco'] > 0, "Net TCO must always be positive"


def test_tco_result_has_required_keys():
    """
    The full TCO result dict must expose all cost component keys
    that the UI and downstream analytics depend on.
    """
    vehicle = {
        'purchase_price_lakh': 12.0,
        'fuel_type':           'Petrol',
        'claimed_mileage_kmpl': 20.0,
    }
    params = {
        'annual_km':         12_000,
        'ownership_years':   3,
        'fuel_price':        100.0,
        'loan_rate':         9.0,
        'down_payment_pct':  25,
        'tenure_months':     36,
        'resale_value_lakh': 7.0,
    }
    result = engine.calculate(vehicle, params)

    required_keys = {'net_tco', 'total_fuel_cost', 'total_emi_paid', 'resale_value_lakh'}
    for key in required_keys:
        assert key in result, f"TCO result missing required key: '{key}'"


def test_longer_ownership_increases_tco():
    """
    Holding a car longer means more fuel, more maintenance, more EMI payments —
    net TCO should grow with ownership duration.
    """
    vehicle = {
        'purchase_price_lakh': 15.0,
        'fuel_type':           'Petrol',
        'claimed_mileage_kmpl': 18.0,
    }
    base_params = {
        'annual_km':         12_000,
        'fuel_price':        102.0,
        'loan_rate':         8.0,
        'down_payment_pct':  20,
        'tenure_months':     60,
        'resale_value_lakh': 9.0,
    }

    short_params = {**base_params, 'ownership_years': 3}
    long_params  = {**base_params, 'ownership_years': 7}

    short = engine.calculate(vehicle, short_params)
    long  = engine.calculate(vehicle, long_params)

    assert long['net_tco'] > short['net_tco'], \
        "TCO must be higher for longer ownership periods"


# ---------------------------------------------------------------------------
# EV vs Petrol Tests
# ---------------------------------------------------------------------------

def test_electricity_cheaper_than_petrol():
    """
    EV running costs should be significantly cheaper per km than petrol.

    Assumptions:
      - Petrol: 15,000 km/yr, 18 kmpl, ₹105/litre → ~₹8.75/km
      - EV    : 15,000 km/yr,  6 km/kWh, ₹8/kWh  → ~₹1.33/km
    """
    petrol_cost = engine.calculate_fuel_cost(15_000, 18.0, 105.0, 5)
    ev_cost     = engine.calculate_electricity_cost(15_000, 6.0, 8.0, 5)
    assert ev_cost < petrol_cost, "EV running cost must be lower than petrol over same period"


def test_electricity_cost_positive():
    """
    Electricity cost must be strictly positive (no free charging scenario).
    """
    ev_cost = engine.calculate_electricity_cost(12_000, 5.5, 7.5, 3)
    assert ev_cost > 0


def test_electricity_cost_scales_with_tariff():
    """
    Higher electricity tariff should result in higher total EV running cost.
    """
    cheap = engine.calculate_electricity_cost(15_000, 6.0, 6.0, 5)
    expensive = engine.calculate_electricity_cost(15_000, 6.0, 12.0, 5)
    assert expensive == pytest.approx(cheap * 2, rel=1e-6)
