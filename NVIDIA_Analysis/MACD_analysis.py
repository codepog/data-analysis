import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

def calculate_macd(data, fast_period=12, slow_period=26, signal_period=9):
    """
    Calculate the Moving Average Convergence Divergence (MACD)
    """
    exp1 = data['Close'].ewm(span=fast_period, adjust=False).mean()
    exp2 = data['Close'].ewm(span=slow_period, adjust=False).mean()
    macd_line = exp1 - exp2
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
    macd_histogram = macd_line - signal_line
    
    data['MACD_Line'] = macd_line
    data['Signal_Line'] = signal_line
    data['MACD_Histogram'] = macd_histogram
    return data

def plot_macd_analysis(ticker='NVDA', period='1y'):
    """
    Fetch stock data and create an interactive MACD analysis chart
    """
    # Fetch stock data directly from yfinance
    stock = yf.Ticker(ticker)
    stock_data = stock.history(period=period)
    
    # Calculate MACD
    stock_data = calculate_macd(stock_data)
    
    # Create figure with subplots
    fig = make_subplots(
        rows=2, 
        cols=1, 
        shared_xaxes=True, 
        vertical_spacing=0.02, 
        row_heights=[0.7, 0.3],
        subplot_titles=(f'{ticker} Stock Price', 'MACD Indicators')
    )
    
    # Stock price candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=stock_data.index,
            open=stock_data['Open'],
            high=stock_data['High'],
            low=stock_data['Low'],
            close=stock_data['Close'],
            name='Stock Price'
        ),
        row=1, col=1
    )
    
    # MACD Lines
    fig.add_trace(
        go.Scatter(
            x=stock_data.index,
            y=stock_data['MACD_Line'],
            mode='lines',
            name='MACD Line',
            line=dict(color='blue', width=1.5)
        ),
        row=2, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=stock_data.index,
            y=stock_data['Signal_Line'],
            mode='lines',
            name='Signal Line',
            line=dict(color='red', width=1.5)
        ),
        row=2, col=1
    )
    
    # MACD Histogram
    fig.add_trace(
        go.Bar(
            x=stock_data.index,
            y=stock_data['MACD_Histogram'],
            name='MACD Histogram',
            marker_color=stock_data['MACD_Histogram'].apply(lambda x: 'green' if x > 0 else 'red')
        ),
        row=2, col=1
    )
    
    # Zero line for MACD
    fig.add_hline(y=0, line_color='black', line_width=1, line_dash='dash', row=2, col=1)
    
    # Update layout for better readability
    fig.update_layout(
        title=f'{ticker} Stock Price and MACD Analysis',
        xaxis_rangeslider_visible=False,
        height=800,
        width=1200,
        showlegend=True,
        xaxis2_rangeslider_visible=False
    )
    
    # Adjust y-axis titles
    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="MACD Value", row=2, col=1)
    
    # Save the interactive HTML
    fig.write_html(f"{ticker}_macd_analysis.html")
    
    # MACD Signal Analysis
    last_macd = stock_data['MACD_Line'].iloc[-1]
    last_signal = stock_data['Signal_Line'].iloc[-1]
    last_histogram = stock_data['MACD_Histogram'].iloc[-1]
    
    print("\nMACD Analysis Signals:")
    print(f"MACD Line: {last_macd:.4f}")
    print(f"Signal Line: {last_signal:.4f}")
    print(f"MACD Histogram: {last_histogram:.4f}")
    
    if last_macd > last_signal and last_histogram > 0:
        print("\nBullish Signal: MACD is above Signal Line and Histogram is positive")
    elif last_macd < last_signal and last_histogram < 0:
        print("\nBearish Signal: MACD is below Signal Line and Histogram is negative")
    else:
        print("\nNeutral Signal: Mixed MACD indicators")

# Run the analysis
plot_macd_analysis()