import pandas as pd
import os
from typing import Dict, Any, Optional

def load_vehicle_master(path: str) -> pd.DataFrame:
    """
    Load the master list of vehicle specifications.
    """
    if not os.path.exists(path):
        # Return empty dataframe with expected schema if file doesn't exist
        return pd.DataFrame(columns=[
            'vehicle_id', 'brand', 'model', 'variant', 'fuel_type', 
            'body_type', 'transmission', 'original_price', 'launch_year'
        ])
    return pd.read_csv(path)

def load_fuel_prices(path: str) -> pd.DataFrame:
    """
    Load historical and current fuel/electricity prices.
    """
    if not os.path.exists(path):
        return pd.DataFrame(columns=['date', 'state', 'petrol_price', 'diesel_price', 'cng_price', 'ev_rate'])
    return pd.read_csv(path)

def load_used_listings(path: str) -> pd.DataFrame:
    """
    Load market data for used vehicles.
    """
    if not os.path.exists(path):
        return pd.DataFrame(columns=[
            'listing_id', 'vehicle_id', 'year', 'mileage_km', 
            'price', 'condition_score', 'location'
        ])
    return pd.read_csv(path)

def get_vehicle_by_id(df: pd.DataFrame, vehicle_id: str) -> Dict[str, Any]:
    """
    Extract a single vehicle's complete profile as a dictionary.
    """
    if 'vehicle_id' not in df.columns:
        return {}
        
    result = df[df['vehicle_id'] == vehicle_id]
    if result.empty:
        return {}
        
    return result.iloc[0].to_dict()

def search_vehicles(df: pd.DataFrame, brand: Optional[str] = None, 
                   model: Optional[str] = None, fuel_type: Optional[str] = None) -> pd.DataFrame:
    """
    Filter vehicle dataframe based on search criteria.
    """
    mask = pd.Series(True, index=df.index)
    
    if brand:
        if 'brand' in df.columns:
            mask = mask & (df['brand'].str.lower() == brand.lower())
            
    if model:
        if 'model' in df.columns:
            mask = mask & (df['model'].str.lower().str.contains(model.lower(), na=False))
            
    if fuel_type:
        if 'fuel_type' in df.columns:
            mask = mask & (df['fuel_type'].str.lower() == fuel_type.lower())
            
    return df[mask]
