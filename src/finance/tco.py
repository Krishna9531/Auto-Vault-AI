from typing import Dict, Any

class TCOEngine:
    """
    Total Cost of Ownership Engine.
    Calculates the complete financial picture of owning a vehicle over a period.
    """
    
    def __init__(self):
        pass

    def calculate_emi(self, principal: float, rate_annual_pct: float, tenure_months: int) -> Dict[str, float]:
        """Calculate EMI and total interest."""
        if tenure_months == 0 or principal <= 0:
             return {'emi': 0.0, 'total_interest': 0.0, 'total_payment': principal}
             
        r = (rate_annual_pct / 12) / 100
        n = tenure_months
        
        if r == 0:
            emi = principal / n
            total_interest = 0
        else:
            emi = principal * r * ((1+r)**n) / (((1+r)**n) - 1)
            total_payment = emi * n
            total_interest = total_payment - principal
            
        return {
            'emi': float(emi),
            'total_interest': float(total_interest),
            'total_payment': float(principal + total_interest)
        }

    def calculate_fuel_cost(self, annual_km: float, mileage_kmpl: float, price_per_l: float, years: int) -> float:
        """Calculate ICE fuel cost over years, factoring in 3% annual inflation."""
        if mileage_kmpl <= 0:
            return 0.0
            
        total_cost = 0.0
        current_price = price_per_l
        
        for _ in range(years):
            annual_liters = annual_km / mileage_kmpl
            total_cost += annual_liters * current_price
            current_price *= 1.03 # 3% inflation
            
        return float(total_cost)

    def calculate_electricity_cost(self, annual_km: float, efficiency_km_kwh: float, rate_per_kwh: float, years: int) -> float:
        """Calculate EV charging cost over years, factoring in 2% annual inflation."""
        if efficiency_km_kwh <= 0:
            return 0.0
            
        total_cost = 0.0
        current_rate = rate_per_kwh
        
        for _ in range(years):
            annual_kwh = annual_km / efficiency_km_kwh
            total_cost += annual_kwh * current_rate
            current_rate *= 1.02 # 2% inflation
            
        return float(total_cost)

    def calculate_insurance(self, vehicle_value: float, years: int, vehicle_type: str = 'ice') -> float:
        """Estimate insurance costs over ownership period."""
        # Simple heuristic: ~3% of IDV for comprehensive, decreasing as value drops
        total_insurance = 0.0
        current_value = vehicle_value
        base_rate = 0.035 if vehicle_type == 'ev' else 0.03 # EV insurance often slightly higher
        
        for _ in range(years):
            total_insurance += current_value * base_rate
            current_value *= 0.90 # 10% depreciation of IDV per year
            
        return float(total_insurance)

    def calculate_tco(self, years: int, purchase_price: float, fuel_costs: float, 
                     maintenance_costs: float, insurance_costs: float, 
                     resale_value: float, emi_interest_total: float) -> Dict[str, float]:
        """Aggregate all costs to find Net TCO."""
        
        total_outflow = purchase_price + fuel_costs + maintenance_costs + insurance_costs + emi_interest_total
        net_tco = total_outflow - resale_value
        
        annual_cost = net_tco / max(1, years)
        monthly_cost = annual_cost / 12
        
        return {
            'purchase_price': float(purchase_price),
            'total_fuel_energy': float(fuel_costs),
            'total_maintenance': float(maintenance_costs),
            'total_insurance': float(insurance_costs),
            'total_financing': float(emi_interest_total),
            'expected_resale': float(resale_value),
            'total_outflow': float(total_outflow),
            'net_tco': float(net_tco),
            'annual_cost': float(annual_cost),
            'monthly_cost': float(monthly_cost)
        }

    def calculate(self, vehicle_dict: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate the full TCO breakdown.
        
        Args:
            vehicle_dict: Vehicle details
            params: User parameters (loan details, usage, etc.)
        """
        years = params.get('ownership_years', 5)
        annual_km = params.get('annual_km', 12000)
        purchase_price = vehicle_dict.get('price', 1000000)
        fuel_type = vehicle_dict.get('fuel_type', 'petrol').lower()
        
        # Financing
        down_payment = params.get('down_payment', purchase_price * 0.2)
        loan_amount = purchase_price - down_payment
        loan_rate = params.get('loan_rate_pct', 9.0)
        loan_tenure = params.get('loan_tenure_months', 60)
        
        fin_details = self.calculate_emi(loan_amount, loan_rate, loan_tenure)
        financing_cost = fin_details['total_interest']
        
        # Energy/Fuel
        if fuel_type == 'ev':
            efficiency = vehicle_dict.get('efficiency_km_kwh', 6.5)
            rate = params.get('electricity_rate', 8.0)
            energy_cost = self.calculate_electricity_cost(annual_km, efficiency, rate, years)
        else:
            efficiency = vehicle_dict.get('mileage_kmpl', 15.0)
            rate = params.get('fuel_price', 100.0)
            energy_cost = self.calculate_fuel_cost(annual_km, efficiency, rate, years)
            
        # Maintenance (simplified for engine, usually calls MaintenanceModel)
        annual_maint = params.get('annual_maintenance_est', 15000)
        total_maintenance = annual_maint * years
        
        # Insurance
        total_insurance = self.calculate_insurance(purchase_price, years, fuel_type)
        
        # Tyres
        tyre_cost = 25000 * ( (annual_km * years) // 40000 )
        total_maintenance += tyre_cost # Add to general maintenance bucket for simplicity in TCO args
        
        # Resale (usually calls DepreciationModel)
        resale_value = params.get('expected_resale', purchase_price * 0.4)
        
        # Calculate final TCO
        tco_results = self.calculate_tco(
            years=years,
            purchase_price=purchase_price,
            fuel_costs=energy_cost,
            maintenance_costs=total_maintenance,
            insurance_costs=total_insurance,
            resale_value=resale_value,
            emi_interest_total=financing_cost
        )
        
        tco_results['total_tyres'] = float(tyre_cost)
        
        # Affordability / Burden
        income_lakh = params.get('income_lakh', 12.0)
        monthly_income = (income_lakh * 100000) / 12
        if monthly_income > 0:
            # Burden = (EMI + Monthly Running Costs) / Monthly Income
            monthly_running = (energy_cost + total_maintenance + total_insurance) / (years * 12)
            monthly_obligation = fin_details['emi'] + monthly_running
            tco_results['ownership_burden_pct'] = float((monthly_obligation / monthly_income) * 100)
        else:
            tco_results['ownership_burden_pct'] = 0.0
            
        # Data for Waterfall chart
        tco_results['waterfall_data'] = {
            'Purchase Price': purchase_price,
            'Financing Interest': financing_cost,
            'Fuel/Energy': energy_cost,
            'Maintenance & Tyres': total_maintenance,
            'Insurance': total_insurance,
            'Resale Value': -resale_value
        }
        
        return tco_results
