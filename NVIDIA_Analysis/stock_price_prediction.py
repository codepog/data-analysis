import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import tensorflow as tf
from textblob import TextBlob
import tweepy

class NvidiaStockPredictor:
    def __init__(self, ticker='NVDA'):
        """
        Initialize the stock prediction model with NVIDIA stock data
        and market sentiment analysis capabilities
        """
        self.ticker = ticker
        self.model = None
        self.scaler = MinMaxScaler()
        
    def fetch_stock_data(self, start_date='2020-01-01', end_date=None):
        """
        Fetch historical stock data from Yahoo Finance
        """
        if end_date is None:
            end_date = pd.Timestamp.now().strftime('%Y-%m-%d')
        
        # Fetch stock data
        stock_data = yf.download(self.ticker, start=start_date, end=end_date)
        
        # Calculate additional technical indicators
        stock_data['MA50'] = stock_data['Close'].rolling(window=50).mean()
        stock_data['MA200'] = stock_data['Close'].rolling(window=200).mean()
        stock_data['RSI'] = self._calculate_rsi(stock_data['Close'])
        
        return stock_data
    
    def _calculate_rsi(self, prices, periods=14):
        """
        Calculate Relative Strength Index (RSI)
        """
        delta = prices.diff()
        
        # Make two series: one for lower closes and one for higher closes
        up = delta.clip(lower=0)
        down = -1 * delta.clip(upper=0)
        
        # Use exponential moving average
        ma_up = up.ewm(com=periods-1, adjust=True, min_periods=periods).mean()
        ma_down = down.ewm(com=periods-1, adjust=True, min_periods=periods).mean()
        
        rsi = ma_up / ma_down
        return 100.0 - (100.0 / (1.0 + rsi))
    
    def analyze_market_sentiment(self, api_key, api_secret, access_token, access_token_secret):
        """
        Analyze Twitter sentiment about NVIDIA
        Note: This is a mock implementation due to API complexities
        """
        # Authentication would normally happen here
        # This is a simplified sentiment analysis simulation
        sentiments = [
            "NVIDIA's AI chip dominance continues",
            "Strong growth in data center segment",
            "Potential challenges in semiconductor supply chain"
        ]
        
        sentiment_scores = []
        for tweet in sentiments:
            blob = TextBlob(tweet)
            sentiment_scores.append(blob.sentiment.polarity)
        
        return np.mean(sentiment_scores)
    
    def prepare_data(self, stock_data):
        """
        Prepare data for machine learning model
        """
        # Select features
        features = ['Close', 'Volume', 'MA50', 'MA200', 'RSI']
        X = stock_data[features].dropna()
        
        # Target is next day's closing price
        y = X['Close'].shift(-1)
        X = X.iloc[:-1]
        y = y.iloc[:-1]
        
        # Normalize features
        X_scaled = self.scaler.fit_transform(X)
        
        return X_scaled, y
    
    def train_model(self, X, y):
        """
        Train a hybrid machine learning model
        Using Random Forest and Neural Network ensemble
        """
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Random Forest Model
        rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
        rf_model.fit(X_train, y_train)
        
        # Neural Network Model
        nn_model = tf.keras.Sequential([
            tf.keras.layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(1)
        ])
        nn_model.compile(optimizer='adam', loss='mse')
        nn_model.fit(X_train, y_train, epochs=50, verbose=0)
        
        # Ensemble predictions
        def ensemble_predict(X):
            rf_pred = rf_model.predict(X)
            nn_pred = nn_model.predict(X).flatten()
            return (rf_pred + nn_pred) / 2
        
        self.model = ensemble_predict
        
        # Evaluate model
        predictions = self.model(X_test)
        mse = np.mean((predictions - y_test)**2)
        print(f"Model Mean Squared Error: {mse}")
        
        return self.model
    
    def predict_future_price(self, latest_data, months_ahead=12):
        """
        Predict stock price for future months
        """
        if self.model is None:
            raise ValueError("Model must be trained first")
        
        # Simulate future price prediction with some randomness
        last_close = latest_data['Close'].iloc[-1]
        
        # Incorporate market sentiment
        # This is a mock sentiment score - in real implementation, 
        # you'd use actual Twitter/news sentiment analysis
        sentiment_score = 0.2  # Positive sentiment
        
        # Basic projection with sentiment adjustment
        projected_prices = [last_close]
        for _ in range(months_ahead):
            # Simple projection with some randomness and sentiment influence
            next_price = projected_prices[-1] * (1 + np.random.normal(0.005, 0.02) + sentiment_score)
            projected_prices.append(next_price)
        
        return projected_prices[1:]
    
    def generate_report(self, predictions):
        """
        Generate a simple prediction report
        """
        report = f"""NVIDIA Stock Price Projection Report
------------------------------
Current Price: ${predictions[0]:.2f}
Projected Prices (Next 12 Months):
"""
        for month, price in enumerate(predictions, 1):
            report += f"Month {month}: ${price:.2f}\n"
        
        return report

def main():
    # Initialize predictor
    predictor = NvidiaStockPredictor()
    
    # Fetch stock data
    stock_data = predictor.fetch_stock_data()
    
    # Prepare data
    X, y = predictor.prepare_data(stock_data)
    
    # Train model
    predictor.train_model(X, y)
    
    # Predict future prices
    predictions = predictor.predict_future_price(stock_data)
    
    # Generate and print report
    print(predictor.generate_report(predictions))

if __name__ == "__main__":
    main()