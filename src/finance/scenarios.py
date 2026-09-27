import pandas as pd
from typing import Dict, Any, List
from src.finance.tco import TCOEngine

class ScenarioEngine:
    """
    Simulates different financial and usage scenarios for vehicles.
    """
    def __init__(self):
        self.tco_engine = TCOEngine()

    def run_scenario(self, vehicle_dict: Dict[str, Any], scenario_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run a single TCO scenario.
        """
        # Scenario parameters override defaults
        params = {
            'ownership_years': scenario_params.get('ownership_years', 5),
            'annual_km': scenario_params.get('annual_km', 12000),
            'down_payment': scenario_params.get('down_payment', vehicle_dict.get('price', 1000000) * 0.2),
            'loan_rate_pct': scenario_params.get('loan_rate_pct', 9.0),
            'loan_tenure_months': scenario_params.get('loan_tenure_months', 60),
            'income_lakh': scenario_params.get('income_lakh', 12.0)
        }
        
        # Apply fuel price multiplier
        fuel_multiplier = scenario_params.get('fuel_price_multiplier', 1.0)
        fuel_type = vehicle_dict.get('fuel_type', 'petrol').lower()
        if fuel_type == 'ev':
            params['electricity_rate'] = scenario_params.get('base_electricity_rate', 8.0) * fuel_multiplier
        else:
            params['fuel_price'] = scenario_params.get('base_fuel_price', 100.0) * fuel_multiplier

        # Apply resale optimism
        resale_optimism = scenario_params.get('resale_optimism', 0.0) # -0.15 to +0.15
        base_resale = scenario_params.get('base_resale_value', vehicle_dict.get('price', 1000000) * 0.4)
        params['expected_resale'] = base_resale * (1.0 + resale_optimism)
        
        # Set base maintenance
        params['annual_maintenance_est'] = scenario_params.get('base_annual_maintenance', 15000)

        return self.tco_engine.calculate(vehicle_dict, params)

    def compare_scenarios(self, base_vehicle: Dict[str, Any], scenarios: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Compare multiple scenarios side-by-side.
        """
        results = []
        for i, scenario in enumerate(scenarios):
            name = scenario.pop('scenario_name', f'Scenario {i+1}')
            res = self.run_scenario(base_vehicle, scenario)
            
            results.append({
                'Scenario': name,
                'Net TCO': res['net_tco'],
                'Monthly Cost': res['monthly_cost'],
                'Resale Value': res['expected_resale'],
                'Fuel Cost': res['total_fuel_energy'],
                'Burden %': res['ownership_burden_pct']
            })
            
        return pd.DataFrame(results)

    def what_if_analysis(self, vehicle_dict: Dict[str, Any], what_if: Dict[str, Any]) -> str:
        """
        Provide text explanation for a specific what-if change.
        """
        base_params = {
            'ownership_years': 5,
            'annual_km': 12000,
            'base_resale_value': vehicle_dict.get('price', 1000000) * 0.4
        }
        
        base_res = self.run_scenario(vehicle_dict, base_params)
        
        test_params = base_params.copy()
        test_params.update(what_if)
        test_res = self.run_scenario(vehicle_dict, test_params)
        
        diff_tco = test_res['net_tco'] - base_res['net_tco']
        diff_monthly = test_res['monthly_cost'] - base_res['monthly_cost']
        
        if diff_tco > 0:
            direction = "increase"
            monthly_dir = "costing you an extra"
        else:
            direction = "decrease"
            monthly_dir = "saving you"
            
        return f"This scenario would {direction} your Total Cost of Ownership by ₹{abs(diff_tco):,.0f} over {test_params['ownership_years']} years, {monthly_dir} ₹{abs(diff_monthly):,.0f} per month compared to the baseline."
