import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.io as pio

class NVIDIAFinancialForecast:
    def __init__(self):
        # Q4 FY25 Financial Highlights from Investor Presentation
        self.q4_fy25_revenue = 39331  # in millions
        self.q4_fy25_gross_margin = 0.735  # 73.5%
        self.q4_fy25_net_income = 22091  # in millions
        
        # Segment Breakdown from Q4 FY25
        self.segments = {
            'Data Center': 35580,
            'Gaming': 2544,
            'Professional Visualization': 511,
            'Automotive': 570,
            'Software and AI Services': 126
        }
        
        # Growth and Diversification Assumptions
        self.growth_rates = {
            'Data Center': 0.93,  # High initial growth
            'Gaming': -0.11,  
            'Professional Visualization': 0.10,
            'Automotive': 0.06,
            'Software and AI Services': 0.10
        }
        
        # Diversification strategy
        self.diversification_factor = {
            'Data Center': [1.0, 0.85, 0.75],  # Gradual reduction
            'Gaming': [1.0, 1.2, 1.4],  # Gradual increase
            'Professional Visualization': [1.0, 1.15, 1.3],
            'Automotive': [1.0, 1.1, 1.2],
            'Software and AI Services': [1.0, 1.25, 1.5]
        }
        
    def generate_forecast(self):
        """
        Generate 3-year financial forecast with diversifying segment breakdown
        """
        forecasts = []
        
        # Forecast for FY26, FY27, FY28
        for year in range(1, 4):
            # Calculate segment revenues
            segment_revenues = {}
            total_revenue = 0
            
            for segment, current_revenue in self.segments.items():
                # Base growth calculation
                if segment in ['Automotive', 'Software and AI Services']:
                    # Use fixed growth rates for these segments
                    growth_rate = self.growth_rates.get(segment, 0.10)
                    base_revenue = current_revenue * (1 + growth_rate)
                else:
                    # More dynamic growth for other segments
                    base_revenue = current_revenue * (1 + self.long_term_growth_rate)
                
                # Apply diversification factor
                diversification_multiplier = self.diversification_factor[segment][year - 1]
                adjusted_revenue = base_revenue * diversification_multiplier
                
                segment_revenues[segment] = adjusted_revenue
                total_revenue += adjusted_revenue
            
            # Estimate gross margin with slight decline
            gross_margin = max(self.q4_fy25_gross_margin - (year * 0.02), 0.68)
            
            # Estimate net income margin
            net_income_margin = self.q4_fy25_net_income / self.q4_fy25_revenue
            net_income = total_revenue * net_income_margin
            
            # Create forecast entry
            forecast = {
                'Fiscal Year': f'FY{25 + year}',
                'Total Revenue': total_revenue,
                'Gross Margin %': gross_margin,
                'Net Income': net_income,
                'Segments': segment_revenues,
                'Segment Percentages': {
                    seg: (rev / total_revenue * 100) for seg, rev in segment_revenues.items()
                }
            }
            
            forecasts.append(forecast)
            
            # Update current year's segments for next iteration
            self.segments = segment_revenues
        
        return forecasts
    
    def create_visualization(self, forecasts):
        """
        Create an interactive HTML visualization of the forecast
        """
        # Prepare data for plotting
        fiscal_years = [f['Fiscal Year'] for f in forecasts]
        
        # Segment breakdown
        segment_data = {}
        for segment in ['Data Center', 'Gaming', 'Professional Visualization', 'Automotive', 'Software and AI Services']:
            segment_data[segment] = [f['Segments'][segment] for f in forecasts]
        
        # Create figure with segment stacked area chart
        fig = go.Figure()
        
        # Segment Stacked Area Chart
        for segment, revenues in segment_data.items():
            fig.add_trace(go.Scatter(
                x=fiscal_years,
                y=revenues,
                mode='lines',
                stackgroup='one',
                name=segment,
                line=dict(width=0.5)
            ))
        
        # Segment Percentage Annotations
        for segment in segment_data.keys():
            percentages = [f['Segment Percentages'][segment] for f in forecasts]
            fig.add_trace(go.Scatter(
                x=fiscal_years,
                y=percentages,
                mode='text',
                name=f'{segment} %',
                text=[f'{p:.1f}%' for p in percentages],
                textposition='top center',
                showlegend=False,
                hoverinfo='none'
            ))
        
        # Update layout
        fig.update_layout(
            title='NVIDIA Segment Revenue Forecast with Percentage (FY26-FY28)',
            xaxis_title='Fiscal Year',
            yaxis_title='Segment Revenue ($ Millions)',
            hovermode='x unified',
            legend_title='Segments',
            template='plotly_white',
            height=600
        )
        
        # Save to HTML
        html_path = 'nvidia_financial_forecast.html'
        pio.write_html(fig, file=html_path, auto_open=False)
        print(f"\nInteractive forecast visualization saved to {html_path}")
    
    def display_forecast(self, forecasts):
        """
        Display forecast in a detailed format
        """
        print("NVIDIA 3-Year Financial Forecast")
        print("=" * 50)
        
        for forecast in forecasts:
            print(f"\n{forecast['Fiscal Year']} Projection:")
            print(f"Total Revenue: ${forecast['Total Revenue']:,.0f} million")
            print(f"Gross Margin: {forecast['Gross Margin %']:.1%}")
            print(f"Net Income: ${forecast['Net Income']:,.0f} million")
            print("\nSegment Breakdown:")
            for segment, revenue in forecast['Segments'].items():
                percentage = forecast['Segment Percentages'][segment]
                print(f"  {segment}: ${revenue:,.0f} million ({percentage:.1f}%)")
    
    def export_forecast(self, forecasts):
        """
        Export forecast to CSV
        """
        # Prepare data for export
        export_data = []
        for forecast in forecasts:
            row = {
                'Fiscal Year': forecast['Fiscal Year'],
                'Total Revenue': forecast['Total Revenue'],
                'Gross Margin %': forecast['Gross Margin %'],
                'Net Income': forecast['Net Income']
            }
            # Add segment revenues and percentages
            for segment, revenue in forecast['Segments'].items():
                row[f'{segment} Revenue'] = revenue
                row[f'{segment} Percentage'] = forecast['Segment Percentages'][segment]
            
            export_data.append(row)
        
        df = pd.DataFrame(export_data)
        df.to_csv('nvidia_financial_forecast.csv', index=False)
        print("\nForecast exported to nvidia_financial_forecast.csv")

# Run the forecast
forecast_model = NVIDIAFinancialForecast()
forecast_results = forecast_model.generate_forecast()
forecast_model.display_forecast(forecast_results)
forecast_model.export_forecast(forecast_results)
forecast_model.create_visualization(forecast_results)