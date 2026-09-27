import pandas as pd
import numpy as np
import xgboost as xgb
import os
import joblib
import json
from typing import Tuple, Dict, Any, Optional
import warnings

warnings.filterwarnings('ignore')

class DepreciationModel:
    """
    ML Model to predict vehicle residual value and depreciation curves.
    Uses XGBoost under the hood, with a robust rule-based fallback if the model is not found.
    """
    
    def __init__(self, model_path: str = 'models/depreciation/'):
        """
        Initialize the DepreciationModel.
        
        Args:
            model_path (str): Path to the directory containing model artifacts.
        """
        self.model_path = model_path
        self.model_file = os.path.join(model_path, 'xgb_depreciation_model.json')
        self.encoder_file = os.path.join(model_path, 'brand_encoder.pkl')
        self.model = None
        self.brand_encoder = None
        
        self._load_model()
        
    def _load_model(self) -> None:
        """Load the model and encoders if they exist."""
        try:
            if os.path.exists(self.model_file):
                self.model = xgb.XGBRegressor()
                self.model.load_model(self.model_file)
            if os.path.exists(self.encoder_file):
                self.brand_encoder = joblib.load(self.encoder_file)
        except Exception as e:
            print(f"Warning: Could not load model artifacts. Falling back to rules. Error: {e}")
            self.model = None
            
    def _build_features(self, vehicle_dict: Dict[str, Any]) -> pd.DataFrame:
        """
        Engineer features for the prediction model from raw input.
        
        Args:
            vehicle_dict (dict): Raw vehicle attributes.
            
        Returns:
            pd.DataFrame: Feature dataframe for model ingestion.
        """
        # Extract basic features
        age_years = vehicle_dict.get('age_years', 0)
        mileage_km = vehicle_dict.get('mileage_km', 0)
        annual_km = mileage_km / age_years if age_years > 0 else mileage_km
        
        brand = vehicle_dict.get('brand', 'Unknown').lower()
        if self.brand_encoder:
            brand_encoded = self.brand_encoder.transform([brand])[0]
        else:
            # Simple hash encoding if no encoder available
            brand_encoded = hash(brand) % 100
            
        fuel_type = vehicle_dict.get('fuel_type', 'petrol').lower()
        fuel_type_encoded = 1 if fuel_type == 'diesel' else (2 if fuel_type == 'ev' else (3 if fuel_type == 'hybrid' else 0))
        
        is_luxury = 1 if vehicle_dict.get('is_luxury', False) else 0
        is_electric = 1 if fuel_type == 'ev' else 0
        is_hybrid = 1 if fuel_type == 'hybrid' else 0
        
        warranty_remaining = max(0, vehicle_dict.get('warranty_years', 3) - age_years)
        service_score = vehicle_dict.get('service_score', 80.0)
        
        # Engineered features
        log_mileage = np.log1p(mileage_km)
        age_squared = age_years ** 2
        mileage_per_year = annual_km
        
        # Price segment based on original price
        orig_price = vehicle_dict.get('original_price', 1000000)
        if orig_price < 500000:
            price_segment = 0
        elif orig_price < 1500000:
            price_segment = 1
        elif orig_price < 3000000:
            price_segment = 2
        else:
            price_segment = 3
            
        features = {
            'age_years': age_years,
            'mileage_km': mileage_km,
            'annual_km': annual_km,
            'brand_encoded': brand_encoded,
            'fuel_type_encoded': fuel_type_encoded,
            'is_luxury': is_luxury,
            'is_electric': is_electric,
            'is_hybrid': is_hybrid,
            'warranty_remaining': warranty_remaining,
            'service_score': service_score,
            'log_mileage': log_mileage,
            'age_squared': age_squared,
            'mileage_per_year': mileage_per_year,
            'price_segment': price_segment
        }
        
        return pd.DataFrame([features])

    def train(self, df: pd.DataFrame) -> None:
        """
        Train the XGBoost Regressor model.
        
        Args:
            df (pd.DataFrame): Training data containing features and 'current_value' target.
        """
        if 'current_value' not in df.columns:
            raise ValueError("Training data must contain 'current_value' column.")
            
        X = df.drop(columns=['current_value'])
        y = df['current_value']
        
        self.model = xgb.XGBRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=6,
            min_child_weight=1,
            subsample=0.8,
            colsample_bytree=0.8,
            objective='reg:squarederror',
            random_state=42
        )
        
        self.model.fit(X, y)
        
        os.makedirs(self.model_path, exist_ok=True)
        self.model.save_model(self.model_file)

    def _rule_based_depreciation(self, vehicle_dict: Dict[str, Any], year_offset: int = 0) -> float:
        """Apply rule-based depreciation if model is unavailable."""
        orig_price = vehicle_dict.get('original_price', 1000000)
        age = vehicle_dict.get('age_years', 0) + year_offset
        fuel_type = vehicle_dict.get('fuel_type', 'petrol').lower()
        
        if fuel_type == 'ev':
            rates = [0.20, 0.15, 0.12, 0.10, 0.09]
            default_rate = 0.08
        elif fuel_type == 'hybrid':
            rates = [0.13, 0.11, 0.09, 0.08, 0.07]
            default_rate = 0.06
        else: # ICE
            rates = [0.15, 0.12, 0.10, 0.09, 0.08]
            default_rate = 0.07
            
        current_val = orig_price
        for i in range(int(age)):
            rate = rates[i] if i < len(rates) else default_rate
            current_val *= (1 - rate)
            
        # Adjust for high mileage
        annual_km = vehicle_dict.get('mileage_km', 0) / max(1, vehicle_dict.get('age_years', 1))
        if annual_km > 15000:
            current_val *= 0.95
            
        return float(current_val)

    def predict(self, vehicle_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict vehicle residual value and generate insights.
        
        Args:
            vehicle_dict (dict): Vehicle attributes.
            
        Returns:
            dict: Prediction results including values, depreciation, and confidence.
        """
        orig_price = vehicle_dict.get('original_price', 0)
        
        if self.model is not None:
            features = self._build_features(vehicle_dict)
            current_value = float(self.model.predict(features)[0])
            
            # Feature importance
            importance_scores = self.model.feature_importances_
            feature_names = features.columns
            feature_importance = dict(zip(feature_names, [float(x) for x in importance_scores]))
            
            # Predict future years
            yearly_values = {}
            for year in range(6):
                future_dict = vehicle_dict.copy()
                future_dict['age_years'] = vehicle_dict.get('age_years', 0) + year
                future_dict['mileage_km'] = vehicle_dict.get('mileage_km', 0) + (vehicle_dict.get('annual_km_estimate', 10000) * year)
                future_features = self._build_features(future_dict)
                yearly_values[year] = float(self.model.predict(future_features)[0])
                
            data_confidence = 0.85
        else:
            current_value = self._rule_based_depreciation(vehicle_dict)
            yearly_values = {
                year: self._rule_based_depreciation(vehicle_dict, year_offset=year)
                for year in range(6)
            }
            feature_importance = {}
            data_confidence = 0.60  # Lower confidence for rules

        # Ensure values don't exceed original price
        current_value = min(current_value, orig_price)
        for y in yearly_values:
            yearly_values[y] = min(yearly_values[y], orig_price)

        depreciation_pct = ((orig_price - current_value) / orig_price) * 100 if orig_price > 0 else 0
        
        # Confidence interval (wider for older cars)
        age = vehicle_dict.get('age_years', 0)
        margin = 0.05 + (0.01 * age)
        confidence_range = (current_value * (1 - margin), current_value * (1 + margin))

        return {
            'current_value': current_value,
            'yearly_values': yearly_values,
            'depreciation_pct': depreciation_pct,
            'confidence_range': confidence_range,
            'feature_importance': feature_importance,
            'data_confidence': data_confidence
        }

    def predict_resale(self, vehicle_dict: Dict[str, Any], years: int) -> float:
        """
        Predict the resale value after a specific number of years.
        """
        future_dict = vehicle_dict.copy()
        future_dict['age_years'] = vehicle_dict.get('age_years', 0) + years
        future_dict['mileage_km'] = vehicle_dict.get('mileage_km', 0) + (vehicle_dict.get('annual_km_estimate', 10000) * years)
        
        if self.model is not None:
            features = self._build_features(future_dict)
            return float(self.model.predict(features)[0])
        else:
            return self._rule_based_depreciation(future_dict)

    def get_shap_explanation(self, vehicle_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a simulated SHAP-like explanation of factors affecting price.
        """
        # In a real scenario, we would use the shap library here:
        # explainer = shap.TreeExplainer(self.model)
        # shap_values = explainer.shap_values(self._build_features(vehicle_dict))
        
        # Simulated explanation based on rules
        age = vehicle_dict.get('age_years', 0)
        mileage = vehicle_dict.get('mileage_km', 0)
        fuel = vehicle_dict.get('fuel_type', 'petrol').lower()
        
        impacts = {
            'age': -50000 * age,
            'mileage': -1000 * (mileage / 10000),
            'brand_reputation': 20000 if vehicle_dict.get('brand', '').lower() in ['toyota', 'honda'] else 0,
            'fuel_type_demand': 30000 if fuel == 'ev' else (-10000 if fuel == 'diesel' else 0),
            'service_history': 15000 if vehicle_dict.get('service_score', 0) > 80 else -15000
        }
        
        return impacts
