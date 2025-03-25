import numpy as np
import pandas as pd

class NVIDIADiscountedCashFlowModel:
    def __init__(self):
        # Financial assumptions based on recent NVIDIA financial reports
        # These are example estimates and should be updated with latest financial data
        self.current_revenue = 60.92  # Revenue in billions for FY2024 (based on recent projections)
        self.free_cash_flow_margin = 0.35  # Estimated FCF margin
        self.cost_of_capital = 0.10  # Estimated WACC (Weighted Average Cost of Capital)
        self.long_term_growth_rate = 0.03  # Long-term sustainable growth rate
    
    def calculate_free_cash_flow(self, revenue):
        """
        Estimate Free Cash Flow based on revenue and FCF margin
        """
        return revenue * self.free_cash_flow_margin
    
    def project_revenues(self):
        """
        Project revenues for next 5 years with growth assumptions
        """
        revenues = [
            self.current_revenue,  # FY2024
            self.current_revenue * 1.25,  # FY2025 (25% growth)
            self.current_revenue * 1.25 * 1.20,  # FY2026 (20% growth)
            self.current_revenue * 1.25 * 1.20 * 1.15,  # FY2027 (15% growth)
            self.current_revenue * 1.25 * 1.20 * 1.15 * 1.10  # FY2028 (10% growth)
        ]
        return revenues
    
    def calculate_terminal_value(self, final_year_cash_flow):
        """
        Calculate terminal value using Gordon Growth Model
        """
        terminal_value = final_year_cash_flow * (1 + self.long_term_growth_rate) / \
                         (self.cost_of_capital - self.long_term_growth_rate)
        return terminal_value
    
    def discount_cash_flows(self, cash_flows):
        """
        Discount projected cash flows
        """
        discounted_cash_flows = [
            cf / ((1 + self.cost_of_capital) ** (year + 1)) 
            for year, cf in enumerate(cash_flows)
        ]
        return discounted_cash_flows
    
    def run_dcf_valuation(self):
        """
        Run complete DCF valuation
        """
        # Project revenues
        projected_revenues = self.project_revenues()
        
        # Calculate Free Cash Flows
        free_cash_flows = [
            self.calculate_free_cash_flow(revenue) for revenue in projected_revenues
        ]
        
        # Calculate Terminal Value
        terminal_value = self.calculate_terminal_value(free_cash_flows[-1])
        
        # Add Terminal Value to Cash Flows
        total_cash_flows = free_cash_flows + [terminal_value]
        
        # Discount Cash Flows
        discounted_cash_flows = self.discount_cash_flows(total_cash_flows)
        
        # Create results DataFrame
        results_df = pd.DataFrame({
            'Year': ['FY2024', 'FY2025', 'FY2026', 'FY2027', 'FY2028', 'Terminal Value'],
            'Revenue (Billions)': projected_revenues + ['-'],
            'Free Cash Flow (Billions)': free_cash_flows + [terminal_value],
            'Discounted Cash Flow (Billions)': discounted_cash_flows
        })
        
        # Calculate Enterprise Value
        enterprise_value = sum(discounted_cash_flows)
        
        return results_df, enterprise_value

# Run the valuation
dcf_model = NVIDIADiscountedCashFlowModel()
results, enterprise_value = dcf_model.run_dcf_valuation()

print("NVIDIA Discounted Cash Flow Valuation")
print(results)
print(f"\nEnterprise Value: ${enterprise_value:.2f} Billion")