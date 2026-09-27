from typing import Dict, Any, List

class MaintenanceModel:
    """
    Predicts maintenance events, probabilities, and costs based on vehicle state.
    """
    
    # Simple simulated OEM schedules (interval_km, cost)
    SCHEDULES = {
        'petrol': {
            'oil_service': (10000, 3000),
            'brake_service': (30000, 8000),
            'tyre_replacement': (40000, 25000),
            'battery_service': (50000, 6000),
            'major_service': (40000, 15000),
            'ac_service': (20000, 4000)
        },
        'diesel': {
            'oil_service': (10000, 4500),
            'brake_service': (30000, 9000),
            'tyre_replacement': (40000, 28000),
            'battery_service': (50000, 7000),
            'major_service': (40000, 18000),
            'ac_service': (20000, 4000)
        },
        'ev': {
            'oil_service': (999999, 0), # N/A
            'brake_service': (60000, 6000), # Less wear due to regen
            'tyre_replacement': (35000, 30000), # EV tyres wear faster (torque/weight)
            'battery_service': (100000, 20000), # Coolant etc.
            'major_service': (50000, 8000),
            'ac_service': (20000, 5000)
        }
    }

    def __init__(self):
        pass
        
    def predict_events(self, vehicle_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict maintenance events and costs for the upcoming year.
        
        Args:
            vehicle_dict: Vehicle attributes
            
        Returns:
            dict: Maintenance predictions and risk assessment
        """
        mileage_km = vehicle_dict.get('mileage_km', 0)
        annual_km = vehicle_dict.get('annual_km', 12000)
        fuel_type = vehicle_dict.get('fuel_type', 'petrol').lower()
        age_years = vehicle_dict.get('age_years', 0)
        
        # Get baseline schedule for fuel type, fallback to petrol
        schedule = self.SCHEDULES.get(fuel_type, self.SCHEDULES['petrol'])
        
        target_km = mileage_km + annual_km
        
        event_probabilities = {}
        cost_breakdown = {}
        total_expected_cost = 0.0
        explanations: List[str] = []
        
        risk_score = 10.0 # Base risk
        
        for event, (interval, cost) in schedule.items():
            if interval > 100000 and cost == 0:
                event_probabilities[event] = 0.0
                continue
                
            # Calculate how close we are to the next interval
            # e.g. if mileage is 9000 and interval is 10000, probability is high
            km_since_last = mileage_km % interval
            km_to_next = interval - km_since_last
            
            if km_to_next <= annual_km:
                # Event is likely to happen this year
                prob = 1.0 - (km_to_next / max(annual_km, 1))
                # Boost probability as cars get older
                prob = min(0.99, prob * (1 + (age_years * 0.05)))
            else:
                # Unlikely to happen this year, but add residual risk
                prob = 0.1 * (annual_km / max(km_to_next, 1))
                
            event_probabilities[event] = float(round(prob, 3))
            
            # Expected cost = Cost * Probability
            expected_cost = cost * prob
            cost_breakdown[event] = float(round(expected_cost, 2))
            total_expected_cost += expected_cost
            
            if prob > 0.7:
                explanations.append(f"High likelihood of {event.replace('_', ' ')} (Interval: {interval}km).")
                risk_score += (prob * 10)
                
        # Age-based unexpected repair risk
        if age_years > 5:
            unexpected_risk_prob = min(0.5, (age_years - 5) * 0.1)
            unexpected_cost = 15000 * unexpected_risk_prob
            cost_breakdown['unexpected_repairs'] = float(round(unexpected_cost, 2))
            total_expected_cost += unexpected_cost
            risk_score += (unexpected_risk_prob * 20)
            explanations.append(f"Age-related repair risk factor included ({age_years} years old).")
            
        risk_score = min(100.0, risk_score)
        
        if risk_score > 70:
            risk_level = "HIGH"
        elif risk_score > 40:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
            
        next_service_interval = schedule.get('oil_service', (10000, 0))[0]
        if fuel_type == 'ev':
             next_service_interval = schedule.get('major_service', (20000, 0))[0]
             
        km_to_next_service = next_service_interval - (mileage_km % next_service_interval)
        next_service_km = mileage_km + km_to_next_service

        return {
            'annual_cost_estimate': float(round(total_expected_cost, 2)),
            'event_probabilities': event_probabilities,
            'risk_score': float(round(risk_score, 2)),
            'risk_level': risk_level,
            'next_service_km': float(next_service_km),
            'cost_breakdown': cost_breakdown,
            'explanation': explanations
        }
