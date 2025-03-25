import numpy as np
import pandas as pd

class NVIDIAValuationModel:
    def __init__(self):
        # Detailed Assumptions from Previous Analysis
        self.risk_free_rate = 0.0347  # 3.47% from US 10-year zero coupon bond
        self.market_risk_premium = 0.055  # 5.5% average market risk premium
        self.beta = 1.84  # Calculated from 2018-2023 stock price movements
        self.cost_of_debt = 0.024  # 2.4% weighted average interest expense
        self.tax_rate = 0.02  # 2% effective tax rate
        self.terminal_growth_rate = 0.035  # 3.5% average GDP growth
        
        # Current Financial Metrics
        self.current_revenue = 60.9  # Billion USD
        self.current_stock_price = 121  # Current trading price
        self.shares_outstanding = 2.46  # Billion shares
        self.net_cash = 11.0  # Billion USD

    def calculate_wacc(self):
        # WACC Calculation
        cost_of_equity = self.risk_free_rate + (self.beta * self.market_risk_premium)
        
        # current capital structure
        debt_weight = 0.13
        equity_weight = 0.87
        
        wacc = (cost_of_equity * equity_weight) + \
               (self.cost_of_debt * (1 - self.tax_rate) * debt_weight)
        
        return wacc

    def project_cash_flows(self, years=5):
        # Realistic growth projection with AI-driven momentum
        growth_rates = [
            0.70,  # Year 1 - Strong AI-driven growth
            0.60,  # Year 2 - Continued strong growth
            0.50,  # Year 3 - Moderate deceleration
            0.40,  # Year 4 - Continued moderation
            0.30,  # Year 5 - Stabilizing growth
        ]
        
        # Profit margin projection
        profit_margins = [
            0.70,  # Year 1 - Peak margins
            0.7,  # Year 2 - Slight compression
            0.7,  # Year 3 - More competitive environment
            0.7,  # Year 4 - Continued margin pressure
            0.7,  # Year 5 - Stabilized margins
        ]
        
        # Project revenues and cash flows
        revenues = [self.current_revenue]
        cash_flows = []
        
        for rate, margin in zip(growth_rates, profit_margins):
            next_revenue = revenues[-1] * (1 + rate)
            revenues.append(next_revenue)
            cash_flows.append(next_revenue * margin)
        
        return revenues[1:], cash_flows

    def calculate_dcf(self):
        # Calculate WACC
        wacc = self.calculate_wacc()
        
        # Project cash flows
        revenues, cash_flows = self.project_cash_flows()
        
        # Discount cash flows
        pv_cash_flows = [cf / ((1 + wacc) ** (t+1)) for t, cf in enumerate(cash_flows)]
        
        # Terminal value calculation
        final_cash_flow = cash_flows[-1]
        terminal_value = final_cash_flow * (1 + self.terminal_growth_rate) / (wacc - self.terminal_growth_rate)
        pv_terminal_value = terminal_value / ((1 + wacc) ** len(cash_flows))
        
        # Enterprise value
        enterprise_value = sum(pv_cash_flows) + pv_terminal_value
        
        # Equity value
        equity_value = enterprise_value + self.net_cash
        implied_per_share = equity_value / self.shares_outstanding
        
        return {
            'WACC': wacc,
            'Projected Revenues': revenues,
            'Projected Cash Flows': cash_flows,
            'PV Cash Flows': pv_cash_flows,
            'Terminal Value': terminal_value,
            'PV Terminal Value': pv_terminal_value,
            'Enterprise Value': enterprise_value,
            'Implied Per Share Value': implied_per_share,
            'Upside Potential': (implied_per_share / self.current_stock_price - 1) * 100
        }

    def sensitivity_analysis(self):
        # Create sensitivity matrix for WACC and Terminal Growth
        wacc_range = np.linspace(0.10, 0.15, 6)
        terminal_growth_range = np.linspace(0.03, 0.05, 6)
        
        sensitivity_matrix = np.zeros((len(wacc_range), len(terminal_growth_range)))
        
        for i, wacc in enumerate(wacc_range):
            for j, terminal_growth in enumerate(terminal_growth_range):
                # Temporarily modify WACC and terminal growth
                original_wacc = self.calculate_wacc()
                original_terminal_growth = self.terminal_growth_rate
                
                self.terminal_growth_rate = terminal_growth
                
                # Recalculate valuation
                dcf_results = self.calculate_dcf()
                
                # Store implied share value
                sensitivity_matrix[i, j] = dcf_results['Implied Per Share Value']
                
                # Restore original values
                self.terminal_growth_rate = original_terminal_growth
        
        return {
            'WACC Range': wacc_range,
            'Terminal Growth Range': terminal_growth_range,
            'Sensitivity Matrix': sensitivity_matrix
        }

# Run the valuation
model = NVIDIAValuationModel()
results = model.calculate_dcf()
sensitivity = model.sensitivity_analysis()

# Print Results
print("NVIDIA DCF Valuation:")
print(f"WACC: {results['WACC']:.4f}")
print(f"Projected Revenues: {[f'${x:.2f}B' for x in results['Projected Revenues']]}")
print(f"Projected Cash Flows: {[f'${x:.2f}B' for x in results['Projected Cash Flows']]}")
print(f"Implied Per Share Value: ${results['Implied Per Share Value']:.2f}")
print(f"Current Stock Price: $121")
print(f"Upside Potential: {results['Upside Potential']:.2f}%")

print("\nSensitivity Analysis:")
print("WACC Range:", [f"{x:.2%}" for x in sensitivity['WACC Range']])
print("Terminal Growth Range:", [f"{x:.2%}" for x in sensitivity['Terminal Growth Range']])
print("Sensitivity Matrix (Implied Share Values):")
print(sensitivity['Sensitivity Matrix'])