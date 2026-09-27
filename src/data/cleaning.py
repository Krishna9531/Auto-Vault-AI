import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple
from dataclasses import dataclass

@dataclass
class DataQualityReport:
    total_rows: int
    missing_values: Dict[str, int]
    duplicates_removed: int
    outliers_detected: int
    is_valid: bool

def standardize_vehicle_name(name: str) -> str:
    """
    Standardize brand/model names (e.g., lowercase, strip whitespace, handle aliases).
    """
    if not isinstance(name, str):
        return ""
    
    name = name.lower().strip()
    # Handle common aliases/typos
    aliases = {
        'vw': 'volkswagen',
        'chevy': 'chevrolet',
        'mercedes': 'mercedes-benz',
        'mb': 'mercedes-benz'
    }
    return aliases.get(name, name)

def clean_price_column(series: pd.Series) -> pd.Series:
    """
    Remove currency symbols, commas, and convert to numeric.
    """
    if series.dtype == 'object':
        series = series.astype(str).str.replace(r'[^\d.]', '', regex=True)
    return pd.to_numeric(series, errors='coerce')

def clean_mileage_column(series: pd.Series) -> pd.Series:
    """
    Extract numeric mileage from strings like '45,000 km'.
    """
    if series.dtype == 'object':
        series = series.astype(str).str.lower().str.replace('km', '').str.replace(',', '').str.strip()
    return pd.to_numeric(series, errors='coerce')

def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply imputation strategies for missing data.
    """
    df = df.copy()
    
    # Numeric columns: fill with median (robust to outliers)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if df[col].isnull().any():
            df[col].fillna(df[col].median(), inplace=True)
            
    # Categorical columns: fill with mode or 'Unknown'
    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    for col in cat_cols:
        if df[col].isnull().any():
            df[col].fillna('Unknown', inplace=True)
            
    return df

def detect_and_remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate rows, keeping the latest/first occurrence.
    """
    return df.drop_duplicates(keep='first')

def validate_data_integrity(df: pd.DataFrame) -> DataQualityReport:
    """
    Generate a quality report for the dataset.
    """
    total_rows = len(df)
    missing = df.isnull().sum().to_dict()
    duplicates = df.duplicated().sum()
    
    # Simple outlier detection (Z-score > 3 on price if it exists)
    outliers = 0
    if 'price' in df.columns and pd.api.types.is_numeric_dtype(df['price']):
        z_scores = np.abs((df['price'] - df['price'].mean()) / df['price'].std())
        outliers = (z_scores > 3).sum()
        
    is_valid = total_rows > 0 and sum(missing.values()) < (total_rows * df.shape[1] * 0.2) # <20% missing
    
    return DataQualityReport(
        total_rows=total_rows,
        missing_values={k: v for k, v in missing.items() if v > 0},
        duplicates_removed=duplicates,
        outliers_detected=outliers,
        is_valid=is_valid
    )

def normalize_fuel_type(fuel: str) -> str:
    """
    Normalize fuel type strings to standard categories.
    """
    if not isinstance(fuel, str):
        return 'unknown'
        
    fuel = fuel.lower().strip()
    
    if 'petrol' in fuel or 'gasoline' in fuel or 'gas' in fuel:
        return 'petrol'
    elif 'diesel' in fuel:
        return 'diesel'
    elif 'electric' in fuel or 'ev' in fuel:
        return 'ev'
    elif 'hybrid' in fuel or 'phev' in fuel or 'mhev' in fuel:
        return 'hybrid'
    elif 'cng' in fuel:
        return 'cng'
    else:
        return 'unknown'
