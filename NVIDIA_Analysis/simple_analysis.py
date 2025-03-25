import yfinance as yf
import numpy as np

# Define assumptions
growth_fy2026 = 0.70  # 70% growth for FY2026
growth_fy2027 = 0.60  # 45% growth for FY2027
growth_fy2028 = 0.50  # 25% growth for FY2028
fcf_margin = 0.35     # Assume Free Cash Flow is 35% of Revenue
wacc = 0.11           # Weighted Average Cost of Capital: 11%
terminal_growth = 0.06  # Terminal growth rate: 6%

# Fetch current data for NVIDIA using yfinance
ticker_symbol = "NVDA"
ticker = yf.Ticker(ticker_symbol)

# Try to get the latest annual revenue (FY revenue) from financials
try:
    financials = ticker.financials
    # Try common revenue labels
    if 'Total Revenue' in financials.index:
        latest_revenue = financials.loc['Total Revenue'].iloc[0]
    elif 'Revenue' in financials.index:
        latest_revenue = financials.loc['Revenue'].iloc[0]
    else:
        raise ValueError("Revenue field not found.")
    
    # Convert revenue from USD to billions
    revenue_fy2025 = latest_revenue / 1e9
except Exception as e:
    print("Could not fetch revenue from yfinance, using assumed value. Error:", e)
    revenue_fy2025 = 30.0  # assumed $30 billion for FY2025

# Try to fetch shares outstanding (if available)
try:
    shares_outstanding = ticker.info.get('sharesOutstanding', None)
    if shares_outstanding is None:
        raise ValueError("sharesOutstanding not available.")
    shares_outstanding = shares_outstanding / 1e9  # convert to billions
except Exception as e:
    print("Could not fetch shares outstanding, using assumed value. Error:", e)
    shares_outstanding = 2.5  # assumed 2.5 billion shares

# Calculate Net Debt = Total Debt - Cash (or Cash And Cash Equivalents)
try:
    bs = ticker.balance_sheet
    # Look for Total Debt in the balance sheet
    if 'Total Debt' in bs.index:
        total_debt = bs.loc['Total Debt'].iloc[0]
    else:
        raise ValueError("Total Debt not found.")
    
    # Try to find cash: check for 'Cash And Cash Equivalents' or 'Cash'
    if 'Cash And Cash Equivalents' in bs.index:
        cash = bs.loc['Cash And Cash Equivalents'].iloc[0]
    elif 'Cash' in bs.index:
        cash = bs.loc['Cash'].iloc[0]
    else:
        raise ValueError("Cash information not found.")
    
    net_debt = (total_debt - cash) / 1e9  # convert to billions
    # In case the calculation results in a negative value (net cash), we set net_debt to 0 for this model.
    if net_debt < 0:
        net_debt = 0.0
except Exception as e:
    print("Could not fetch net debt data, using assumed value. Error:", e)
    net_debt = 10.0  # assumed $10 billion net debt

# Forecast revenues for FY2026, FY2027, FY2028
revenue_fy2026 = revenue_fy2025 * (1 + growth_fy2026)
revenue_fy2027 = revenue_fy2026 * (1 + growth_fy2027)
revenue_fy2028 = revenue_fy2027 * (1 + growth_fy2028)

# Calculate Free Cash Flows (in billions)
fcf_fy2026 = revenue_fy2026 * fcf_margin
fcf_fy2027 = revenue_fy2027 * fcf_margin
fcf_fy2028 = revenue_fy2028 * fcf_margin

# Discount the FCFs to present value
pv_fcf_fy2026 = fcf_fy2026 / ((1 + wacc)**1)
pv_fcf_fy2027 = fcf_fy2027 / ((1 + wacc)**2)
pv_fcf_fy2028 = fcf_fy2028 / ((1 + wacc)**3)

# Calculate Terminal Value at end of FY2028 using the Gordon Growth Model
terminal_value = (fcf_fy2028 * (1 + terminal_growth)) / (wacc - terminal_growth)
pv_terminal_value = terminal_value / ((1 + wacc)**3)

# Calculate Total Enterprise Value (EV)
enterprise_value = pv_fcf_fy2026 + pv_fcf_fy2027 + pv_fcf_fy2028 + pv_terminal_value

# Adjust for net debt to get Equity Value
equity_value = enterprise_value - net_debt

# Compute the stock price per share (in USD)
stock_price = equity_value / shares_outstanding

# Print the results
print("DCF Model Stock Prediction for", ticker_symbol)
print("Assumed FY2025 Revenue: ${:.2f} billion".format(revenue_fy2025))
print("Projected Revenue:")
print(" FY2026: ${:.2f} billion".format(revenue_fy2026))
print(" FY2027: ${:.2f} billion".format(revenue_fy2027))
print(" FY2028: ${:.2f} billion".format(revenue_fy2028))
print("\nCalculated Free Cash Flows:")
print(" FY2026 FCF: ${:.2f} billion".format(fcf_fy2026))
print(" FY2027 FCF: ${:.2f} billion".format(fcf_fy2027))
print(" FY2028 FCF: ${:.2f} billion".format(fcf_fy2028))
print("\nPresent Value of FCFs:")
print(" FY2026: ${:.2f} billion".format(pv_fcf_fy2026))
print(" FY2027: ${:.2f} billion".format(pv_fcf_fy2027))
print(" FY2028: ${:.2f} billion".format(pv_fcf_fy2028))
print("Terminal Value (undiscounted): ${:.2f} billion".format(terminal_value))
print("PV of Terminal Value: ${:.2f} billion".format(pv_terminal_value))
print("\nEnterprise Value: ${:.2f} billion".format(enterprise_value))
print("Net Debt: ${:.2f} billion".format(net_debt))
print("Equity Value: ${:.2f} billion".format(equity_value))
print("Estimated Stock Price: ${:.2f}".format(stock_price))
