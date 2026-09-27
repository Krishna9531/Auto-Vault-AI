"""
EMI and Financing Calculator for AUTOVAULT AI.
Follows standard reducing-balance EMI formula.
"""
import math

def calculate_emi(principal: float, annual_rate_pct: float, tenure_months: int) -> dict:
    """Calculate EMI using standard reducing balance formula.
    Args:
        principal: Loan amount in INR
        annual_rate_pct: Annual interest rate (e.g., 8.5 for 8.5%)
        tenure_months: Loan tenure in months
    Returns:
        dict with monthly_emi, total_payment, total_interest, effective_cost
    """
    if annual_rate_pct == 0:
        emi = principal / tenure_months
        return {'monthly_emi': emi, 'total_payment': principal, 'total_interest': 0, 'effective_cost': principal}
    r = annual_rate_pct / (12 * 100)
    emi = principal * r * (1 + r) ** tenure_months / ((1 + r) ** tenure_months - 1)
    total = emi * tenure_months
    return {
        'monthly_emi': round(emi, 2),
        'total_payment': round(total, 2),
        'total_interest': round(total - principal, 2),
        'effective_cost': round(total, 2),
        'loan_amount': principal,
        'annual_rate_pct': annual_rate_pct,
        'tenure_months': tenure_months
    }

def amortization_schedule(principal: float, annual_rate_pct: float, tenure_months: int) -> list[dict]:
    """Generate full amortization schedule month by month."""
    r = annual_rate_pct / (12 * 100)
    emi_dict = calculate_emi(principal, annual_rate_pct, tenure_months)
    emi = emi_dict['monthly_emi']
    balance = principal
    schedule = []
    for month in range(1, tenure_months + 1):
        interest = balance * r
        principal_payment = emi - interest
        balance -= principal_payment
        schedule.append({
            'month': month,
            'emi': round(emi, 2),
            'principal': round(principal_payment, 2),
            'interest': round(interest, 2),
            'balance': round(max(0, balance), 2)
        })
    return schedule

def loan_eligibility(annual_income: float, existing_emi: float = 0, rate: float = 8.5, tenure_months: int = 60) -> dict:
    """Estimate maximum eligible loan based on FOIR (Fixed Obligation to Income Ratio)."""
    # Standard FOIR: 40-50% of monthly income
    monthly_income = annual_income / 12
    max_foir = 0.45
    max_emi_capacity = monthly_income * max_foir - existing_emi
    if max_emi_capacity <= 0:
        return {'eligible_loan': 0, 'max_emi': 0, 'message': 'Existing obligations exceed FOIR limit'}
    r = rate / (12 * 100)
    max_loan = max_emi_capacity * ((1 + r) ** tenure_months - 1) / (r * (1 + r) ** tenure_months)
    return {
        'eligible_loan': round(max_loan, 2),
        'max_emi': round(max_emi_capacity, 2),
        'foir_used': round((existing_emi / monthly_income) * 100, 1),
        'message': f'Eligible for loan up to ₹{round(max_loan/100000, 2)}L'
    }
