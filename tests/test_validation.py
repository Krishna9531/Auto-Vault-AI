"""
tests/test_validation.py
========================
Pytest test suite for the input validation utility functions.

Validates the three core guard functions used across all Streamlit
form inputs to prevent bad data from reaching ML models or finance
engines:

  - validate_mileage  — rejects ≤ 0, unrealistically high values
  - validate_price    — rejects ≤ 0, verifies realistic price bands
  - validate_year     — rejects future years and pre-automobile era years

Run with:
    pytest tests/test_validation.py -v
"""

import sys
import datetime
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import pytest
from app.utils.validation import validate_mileage, validate_price, validate_year

# ---------------------------------------------------------------------------
# Current year helper (used in dynamic year tests)
# ---------------------------------------------------------------------------
_CURRENT_YEAR = datetime.datetime.now().year


# ===========================================================================
# validate_mileage
# ===========================================================================

class TestValidateMileage:
    """Tests for validate_mileage(km_per_year)."""

    def test_negative_mileage_invalid(self):
        """Negative mileage is physically impossible — must be rejected."""
        assert validate_mileage(-100) is False

    def test_zero_mileage_invalid(self):
        """Zero annual km makes no sense for a vehicle in use — must be rejected."""
        assert validate_mileage(0) is False

    def test_valid_typical_mileage(self):
        """Typical Indian annual mileage of 15,000 km must be accepted."""
        assert validate_mileage(15_000) is True

    def test_valid_low_mileage(self):
        """Very low but positive mileage (e.g., vintage/weekend car) must be valid."""
        assert validate_mileage(500) is True

    def test_valid_high_mileage(self):
        """Commercial-use high mileage (60,000 km/yr) should be accepted."""
        assert validate_mileage(60_000) is True

    def test_unrealistically_high_mileage_invalid(self):
        """
        No passenger car covers 500,000 km in a single year —
        this is a data entry error and must be rejected.
        """
        assert validate_mileage(500_000) is False

    def test_float_mileage_valid(self):
        """Non-integer km values (e.g., from unit conversions) must be accepted."""
        assert validate_mileage(12_345.67) is True

    def test_string_mileage_invalid(self):
        """Non-numeric input must be rejected gracefully without raising."""
        assert validate_mileage("fifteen thousand") is False

    def test_none_mileage_invalid(self):
        """None must be treated as invalid input."""
        assert validate_mileage(None) is False


# ===========================================================================
# validate_price
# ===========================================================================

class TestValidatePrice:
    """Tests for validate_price(price_in_rupees)."""

    def test_zero_price_invalid(self):
        """A car that costs ₹0 is not a real transaction — must be rejected."""
        assert validate_price(0) is False

    def test_negative_price_invalid(self):
        """Negative prices are impossible — must be rejected."""
        assert validate_price(-50_000) is False

    def test_valid_price(self):
        """A standard hatchback price of ₹15,00,000 must be valid."""
        assert validate_price(1_500_000) is True

    def test_valid_minimum_realistic_price(self):
        """Entry-level used car price (e.g., ₹1 lakh = ₹1,00,000) must be valid."""
        assert validate_price(100_000) is True

    def test_valid_luxury_price(self):
        """High-end luxury car price (₹2 crore) must also be accepted."""
        assert validate_price(20_000_000) is True

    def test_absurdly_high_price_invalid(self):
        """
        A price of ₹100 crore (₹1,000,000,000) is beyond any car sold in
        India — treat as a data entry error.
        """
        assert validate_price(1_000_000_000) is False

    def test_string_price_invalid(self):
        """Non-numeric price string must be rejected gracefully."""
        assert validate_price("fifteen lakh") is False

    def test_none_price_invalid(self):
        """None input must be treated as invalid."""
        assert validate_price(None) is False

    def test_float_price_valid(self):
        """Prices with paise (e.g., ₹8,45,999.50) must be accepted."""
        assert validate_price(845_999.50) is True


# ===========================================================================
# validate_year
# ===========================================================================

class TestValidateYear:
    """Tests for validate_year(year)."""

    def test_future_year_invalid(self):
        """
        A registration year two years in the future is a data entry error —
        you cannot buy a car that hasn't been manufactured yet.
        """
        future_year = _CURRENT_YEAR + 2
        assert validate_year(future_year) is False

    def test_next_year_invalid(self):
        """Next calendar year should also be treated as future/invalid."""
        assert validate_year(_CURRENT_YEAR + 1) is False

    def test_current_year_valid(self):
        """A car registered this year is a perfectly valid new purchase."""
        assert validate_year(_CURRENT_YEAR) is True

    def test_recent_year_valid(self):
        """A 2022-registered vehicle is a typical used-car input — must pass."""
        assert validate_year(2022) is True

    def test_valid_inputs_decade_ago(self):
        """A vehicle from 10 years ago is a valid used-car candidate."""
        assert validate_year(_CURRENT_YEAR - 10) is True

    def test_pre_automobile_era_invalid(self):
        """Year 1885 is before the first automobile — must be rejected."""
        assert validate_year(1885) is False

    def test_very_old_year_invalid(self):
        """Year 1800 is obviously invalid for any motor vehicle."""
        assert validate_year(1800) is False

    def test_reasonable_classic_car_year_valid(self):
        """A 1980s classic/vintage car is rare but could be listed — accept if ≥ 1900."""
        assert validate_year(1985) is True

    def test_string_year_invalid(self):
        """String years (e.g., from a mis-typed form) must be rejected."""
        assert validate_year("2022") is False

    def test_float_year_invalid(self):
        """Float years are ambiguous and must be rejected."""
        assert validate_year(2022.5) is False

    def test_none_year_invalid(self):
        """None must be treated as invalid."""
        assert validate_year(None) is False
