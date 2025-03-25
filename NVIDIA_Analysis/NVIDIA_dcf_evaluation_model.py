import pandas as pd
import numpy as np
from scipy import stats

class NVIDIAFinancialModel:
    def __init__(self):
        # Extract key financial metrics from Q4 FY24 and Q4 FY25 presentations
        self.historical_data = {
            'FY24': {
                'Revenue': 22103,
                'EBIT': 13615,
                'Effective Tax Rate': 0.17,
                'Depreciation and Amortization': 1134,  # Estimated from financial statements
                'Capital Expenditure': 282,
                'Free Cash Flow': 11499
            },
            'FY25': {
                'Revenue': 39331,
                'EBIT': 24034,
                'Effective Tax Rate': 0.17,
                'Depreciation and Amortization': 2000,  # Estimated increase
                'Capital Expenditure': 1100,
                'Free Cash Flow': 16628
            }
        }
        
    def calculate_growth_rates(self):
        """Calculate year-over-year growth rates for key metrics"""
        growth_rates = {}
        for metric in ['Revenue', 'EBIT', 'Free Cash Flow']:
            growth_rates[metric] = (self.historical_data['FY25'][metric] / 
                                    self.historical_data['FY24'][metric] - 1)
        return growth_rates
    
    def project_financials(self, years=2):
        """
        Project financial metrics for the next 2 years using historical growth rates
        Uses geometric mean of growth rates for more stable projection
        """
        projections = {}
        growth_rates = self.calculate_growth_rates()
        
        # Calculate geometric mean of growth rates
        geo_mean_growth = {k: (1 + v)**0.5 - 1 for k, v in growth_rates.items()}
        
        # Project financials
        for year in range(1, years + 1):
            projections[f'FY{25+year}'] = {
                metric: self.historical_data['FY25'][metric] * ((1 + geo_mean_growth[metric])**year)
                for metric in ['Revenue', 'EBIT', 'Free Cash Flow']
            }
            
            # Additional estimated metrics
            projections[f'FY{25+year}']['Effective Tax Rate'] = 0.17
            projections[f'FY{25+year}']['Depreciation and Amortization'] = (
                self.historical_data['FY25']['Depreciation and Amortization'] * 
                ((1 + geo_mean_growth['Revenue'])**year)
            )
            projections[f'FY{25+year}']['Capital Expenditure'] = (
                self.historical_data['FY25']['Capital Expenditure'] * 
                ((1 + geo_mean_growth['Revenue'])**year)
            )
        
        return projections
    
    def calculate_terminal_value(self, projected_free_cash_flow, perpetual_growth_rate=0.03):
        """
        Calculate terminal value using perpetual growth method
        Assumes a long-term growth rate of 3%
        """
        # Use the last projected year's free cash flow
        last_year = list(projected_free_cash_flow.keys())[-1]
        terminal_value = (projected_free_cash_flow[last_year]['Free Cash Flow'] * 
                          (1 + perpetual_growth_rate))
        return terminal_value
    
    def perform_dcf_analysis(self, discount_rate=0.10):
        """
        Perform Discounted Cash Flow (DCF) analysis
        """
        # Project financials
        projections = self.project_financials()
        
        # Calculate discounted free cash flows
        discounted_flows = {}
        for year, data in projections.items():
            discounted_flows[year] = data['Free Cash Flow'] / ((1 + discount_rate)**int(year[-2:]))
        
        # Calculate terminal value
        terminal_value = self.calculate_terminal_value(projections)
        discounted_terminal_value = terminal_value / ((1 + discount_rate)**(len(projections)))
        
        # Sum of discounted cash flows plus discounted terminal value
        total_dcf = sum(discounted_flows.values()) + discounted_terminal_value
        
        return {
            'Projected Financials': projections,
            'Discounted Cash Flows': discounted_flows,
            'Terminal Value': terminal_value,
            'Discounted Terminal Value': discounted_terminal_value,
            'Total Discounted Cash Flow': total_dcf
        }

# Run the analysis
nvidia_model = NVIDIAFinancialModel()

# Calculate and print growth rates
print("Growth Rates:")
growth_rates = nvidia_model.calculate_growth_rates()
for metric, rate in growth_rates.items():
    print(f"{metric}: {rate*100:.2f}%")

# Perform DCF Analysis
dcf_analysis = nvidia_model.perform_dcf_analysis()

print("\nProjected Financials:")
for year, financials in dcf_analysis['Projected Financials'].items():
    print(f"\n{year} Projection:")
    for metric, value in financials.items():
        print(f"{metric}: ${value:,.0f}")

print("\nDCF Analysis Results:")
for key, value in dcf_analysis.items():
    if key != 'Projected Financials':
        print(f"{key}: ${value:,.0f}")