"""Validation utilities and data structures."""

from pydantic import BaseModel, Field, validator
import pandas as pd
import numpy as np
from dataclasses import dataclass

class VehicleInput(BaseModel):
    brand: str
    model: str
    variant: str = "Standard"
    fuel_type: str
    year: int = Field(ge=1990, le=2026)
    mileage_km: float = Field(ge=0)
    purchase_price: float = Field(ge=10_000)
    city: str = "Delhi"
    
    @validator('year')
    def validate_year_range(cls, v):
        if v > 2026 or v < 1990:
            raise ValueError('Year must be between 1990 and 2026')
        return v

def validate_mileage(km: float) -> bool:
    """Validates mileage is reasonable."""
    return 0 <= km <= 1_000_000

def validate_price(price: float) -> bool:
    """Validates price is reasonable."""
    return price > 10_000

def validate_year(year: int) -> bool:
    """Validates year is within bounds."""
    return 1990 <= year <= 2026

def detect_outliers(df: pd.DataFrame, column: str) -> pd.Series:
    """Detects outliers using IQR."""
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return (df[column] < lower_bound) | (df[column] > upper_bound)

def sanitize_input(data: dict) -> dict:
    """Sanitizes input data."""
    sanitized = {}
    for k, v in data.items():
        if isinstance(v, str):
            sanitized[k] = v.strip()
        else:
            sanitized[k] = v
    return sanitized

@dataclass
class DataQualityReport:
    total_records: int
    missing_values: int
    outliers_detected: int
    clean_records: int
    is_valid: bool
