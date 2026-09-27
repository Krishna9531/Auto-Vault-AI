from typing import Dict, Any, List

class VehicleHealthModel:
    """
    Model to score the overall health and components of a vehicle.
    Uses rule-based scoring derived from empirical vehicle maintenance data.
    """
    
    def __init__(self):
        pass
        
    def score_vehicle(self, vehicle_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate a comprehensive health score for the vehicle.
        
        Args:
            vehicle_dict (dict): Vehicle attributes and history.
            
        Returns:
            dict: Health assessment with scores and qualitative factors.
        """
        base_score = 100.0
        positive_factors: List[str] = []
        negative_factors: List[str] = []
        
        age_years = vehicle_dict.get('age_years', 0)
        mileage_km = vehicle_dict.get('mileage_km', 0)
        service_history_complete = vehicle_dict.get('service_history_complete', False)
        accidents = vehicle_dict.get('accident_count', 0)
        fuel_type = vehicle_dict.get('fuel_type', 'petrol').lower()
        fast_charge_pct = vehicle_dict.get('fast_charge_pct', 0)
        climate = vehicle_dict.get('climate', 'moderate').lower()
        
        # 1. Age Penalty
        if age_years > 3:
            penalty = (age_years - 3) * 2
            base_score -= penalty
            if penalty > 5:
                negative_factors.append(f"Age-related wear ({age_years} years old)")
                
        # 2. Mileage Penalty
        if mileage_km > 60000:
            penalty = ((mileage_km - 60000) / 10000) * 1
            base_score -= penalty
            negative_factors.append("High mileage wear")
            
        # 3. Service History
        if service_history_complete:
            base_score += 5
            positive_factors.append("Comprehensive service history")
        else:
            base_score -= 8
            negative_factors.append("Incomplete service history")
            
        # 4. Accident Penalty
        if accidents > 0:
            base_score -= (10 * accidents)
            negative_factors.append(f"History of {accidents} accident(s)")
            
        # 5. Fuel Type Adjustments
        if fuel_type == 'ev':
            base_score += 3
            positive_factors.append("EV drivetrain (fewer moving parts)")
            
            if fast_charge_pct > 50:
                base_score -= 5
                negative_factors.append("High fast-charging ratio affects battery health")
                
        # 6. Climate
        if climate in ['hot', 'high_temp']:
            base_score -= 2
            negative_factors.append("Operated in high-temperature climate")
            
        # Sub-system estimations (simulated based on general correlations)
        mechanical_score = max(0, min(100, base_score + (5 if service_history_complete else -5) - (mileage_km/20000)))
        electrical_score = max(0, min(100, base_score - (age_years * 1.5)))
        usage_score = max(0, min(100, 100 - (mileage_km/15000) - (accidents * 15)))
        service_score = 100.0 if service_history_complete else 60.0
        
        overall_health = max(0.0, min(100.0, base_score))
        
        if overall_health >= 85:
            health_label = 'EXCELLENT'
        elif overall_health >= 70:
            health_label = 'GOOD'
        elif overall_health >= 50:
            health_label = 'FAIR'
        else:
            health_label = 'POOR'
            
        # Add basic positive factors if empty
        if not positive_factors and overall_health > 70:
            if age_years <= 3:
                positive_factors.append("Relatively new vehicle")
            if mileage_km < 30000:
                positive_factors.append("Low mileage")
                
        confidence = 0.9 if 'service_history_complete' in vehicle_dict else 0.6
            
        return {
            'overall_health': float(overall_health),
            'mechanical': float(mechanical_score),
            'electrical': float(electrical_score),
            'usage': float(usage_score),
            'service': float(service_score),
            'positive_factors': positive_factors,
            'negative_factors': negative_factors,
            'health_label': health_label,
            'confidence': confidence
        }
        
    def score_battery(self, battery_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess EV battery health specifically.
        
        Args:
            battery_dict: Dictionary containing battery specific metrics
        """
        age_years = battery_dict.get('age_years', 0)
        cycles = battery_dict.get('charge_cycles', age_years * 150)
        fast_charge_pct = battery_dict.get('fast_charge_pct', 20)
        chemistry = battery_dict.get('chemistry', 'NMC').upper()
        
        # Base degradation models
        if chemistry == 'LFP':
            degradation_rate = 0.015  # 1.5% per 100 cycles
            chemistry_factor = 1.1
        else: # NMC/NCA
            degradation_rate = 0.020  # 2.0% per 100 cycles
            chemistry_factor = 0.9
            
        # Fast charging impact
        if fast_charge_pct > 30:
            degradation_rate *= (1 + ((fast_charge_pct - 30) / 100))
            
        # Calculate State of Health (SOH)
        cycle_degradation = (cycles / 100) * degradation_rate * 100
        age_degradation = age_years * 1.5 # 1.5% per year calendar aging
        
        soh = max(0.0, 100.0 - cycle_degradation - age_degradation)
        
        # Remaining Useful Life (RUL) - assuming 70% is end of life for automotive
        usable_soh = max(0.0, soh - 70.0)
        yearly_drop = (100 - soh) / max(0.1, age_years)
        rul_years = usable_soh / max(0.5, yearly_drop)
        
        return {
            'soh': float(soh),
            'rul_years': float(rul_years),
            'degradation_rate_pct_year': float(yearly_drop),
            'chemistry_factor': float(chemistry_factor)
        }
