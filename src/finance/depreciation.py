"""
Rule-based depreciation curves for AUTOVAULT AI.
Used as fallback when ML model is not trained, and for financial calculations.
"""
from typing import Union

# Depreciation rate tables by fuel type (year 1, 2, 3, 4, 5)
DEPRECIATION_RATES = {
    'Petrol': [0.15, 0.12, 0.10, 0.09, 0.08],
    'Diesel': [0.18, 0.13, 0.10, 0.09, 0.08],
    'Electric': [0.20, 0.15, 0.12, 0.10, 0.09],
    'Hybrid': [0.13, 0.11, 0.09, 0.08, 0.07],
    'CNG': [0.16, 0.12, 0.10, 0.09, 0.08],
}

# Mileage adjustment: extra depreciation per 10k km above average
MILEAGE_PENALTY_PER_10K = 0.005  # 0.5% additional per 10k km above average annual

# Average annual mileage benchmarks by vehicle type
AVERAGE_ANNUAL_KM = {'Petrol': 12000, 'Diesel': 15000, 'Electric': 12000, 'Hybrid': 13000, 'CNG': 14000}

def get_yearly_values(purchase_price: float, fuel_type: str, annual_km: int = 12000, years: int = 5) -> dict:
    """Calculate expected vehicle value year by year.
    Returns dict: {0: purchase_price, 1: val_yr1, ..., years: val_yrN}
    """
    rates = DEPRECIATION_RATES.get(fuel_type, DEPRECIATION_RATES['Petrol'])
    avg_km = AVERAGE_ANNUAL_KM.get(fuel_type, 12000)
    excess_km_per_10k = max(0, (annual_km - avg_km) / 10000)
    
    values = {0: round(purchase_price, 2)}
    current_value = purchase_price
    
    for year in range(1, years + 1):
        base_rate = rates[min(year - 1, len(rates) - 1)]
        mileage_adj = excess_km_per_10k * MILEAGE_PENALTY_PER_10K
        total_rate = min(base_rate + mileage_adj, 0.35)  # cap at 35% per year
        current_value = current_value * (1 - total_rate)
        values[year] = round(current_value, 2)
    
    return values

def get_depreciation_pct(purchase_price: float, resale_value: float) -> float:
    """Calculate total depreciation percentage."""
    if purchase_price <= 0:
        return 0.0
    return round((purchase_price - resale_value) / purchase_price * 100, 1)

def get_residual_value(purchase_price: float, fuel_type: str, years: int, annual_km: int = 12000) -> float:
    """Get expected residual value after N years."""
    values = get_yearly_values(purchase_price, fuel_type, annual_km, years)
    return values.get(years, purchase_price * 0.4)
