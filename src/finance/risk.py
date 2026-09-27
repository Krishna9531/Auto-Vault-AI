from typing import Dict, Any, List

class FinancialRiskEngine:
    """
    Evaluates the financial risks associated with purchasing and owning a vehicle.
    """
    
    def __init__(self):
        pass
        
    def score(self, tco_dict: Dict[str, Any], vehicle_dict: Dict[str, Any], user_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate comprehensive financial risk scores.
        
        Args:
            tco_dict: Output from TCOEngine
            vehicle_dict: Vehicle attributes
            user_params: User financial context (income, etc.)
            
        Returns:
            dict: Risk assessment
        """
        explanations: List[str] = []
        
        # 1. Ownership Burden Risk
        burden_pct = tco_dict.get('ownership_burden_pct', 0)
        if burden_pct > 40:
            financing_risk = 90.0
            explanations.append("CRITICAL: Vehicle costs consume >40% of monthly income.")
        elif burden_pct > 25:
            financing_risk = 70.0
            explanations.append("HIGH: Vehicle costs are a significant portion of income (>25%).")
        elif burden_pct > 15:
            financing_risk = 40.0
            explanations.append("MEDIUM: Comfortable, but noticeable impact on monthly budget.")
        else:
            financing_risk = 10.0
            explanations.append("LOW: Vehicle costs are well within safe budget limits.")
            
        # 2. Resale Risk
        purchase_price = tco_dict.get('purchase_price', 1)
        resale_value = tco_dict.get('expected_resale', 0)
        depreciation_pct = ((purchase_price - resale_value) / purchase_price) * 100
        
        if depreciation_pct > 65:
            resale_risk = 85.0
            explanations.append("HIGH: Asset depreciates very rapidly.")
        elif depreciation_pct > 50:
            resale_risk = 60.0
        else:
            resale_risk = 20.0
            explanations.append("LOW: Asset holds value well.")
            
        # 3. Running Cost Volatility (Fuel/Energy)
        fuel_type = vehicle_dict.get('fuel_type', 'petrol').lower()
        if fuel_type == 'ev':
            running_cost_risk = 20.0
            explanations.append("LOW: EV energy costs are relatively stable and low.")
        else:
            running_cost_risk = 65.0
            explanations.append("MEDIUM-HIGH: Exposure to volatile fossil fuel prices.")
            
        # 4. Maintenance Risk
        age = vehicle_dict.get('age_years', 0)
        luxury = vehicle_dict.get('is_luxury', False)
        
        maintenance_risk = min(100.0, (age * 10) + (30 if luxury else 0))
        if maintenance_risk > 70:
            explanations.append("HIGH: Maintenance costs likely to be high or unpredictable (age/luxury factor).")

        # Purchase Risk
        purchase_risk = min(100.0, (financing_risk * 0.7) + (resale_risk * 0.3))

        # Overall Risk (Weighted average)
        overall_risk = (
            (financing_risk * 0.4) +
            (resale_risk * 0.3) +
            (running_cost_risk * 0.15) +
            (maintenance_risk * 0.15)
        )
        
        if overall_risk > 75:
            risk_label = "HIGH RISK"
        elif overall_risk > 45:
            risk_label = "MODERATE RISK"
        else:
            risk_label = "LOW RISK"
            
        # Break Even Years (rough heuristic: when net TCO flattens out relatively)
        # Simplified calculation for display purposes
        break_even_years = max(2.5, min(7.0, (purchase_price / max(1, tco_dict.get('annual_cost', 100000))) * 0.8))

        return {
            'overall_risk': float(round(overall_risk, 2)),
            'purchase_risk': float(round(purchase_risk, 2)),
            'running_cost_risk': float(round(running_cost_risk, 2)),
            'maintenance_risk': float(round(maintenance_risk, 2)),
            'resale_risk': float(round(resale_risk, 2)),
            'financing_risk': float(round(financing_risk, 2)),
            'ownership_burden': float(round(burden_pct, 2)),
            'risk_label': risk_label,
            'risk_explanations': explanations,
            'break_even_years': float(round(break_even_years, 1))
        }
