import yfinance as yf 
import pandas as pd
from datetime import datetime, timedelta

# Function to fetch stock data
def get_stock_data(ticker, period="60d"):
    try:
        # Fetch stock data using yfinance
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        if hist.empty:
            print(f"No data returned for {ticker}")
            return None  # Handle empty response
        return hist['Close'].reset_index()
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return None

# Function to split data into weekly averages
def split_weeks(df):
    try:
        # Ensure the Date column is in datetime format
        df['Week'] = df['Date'].dt.isocalendar().week
        
        # Debugging output to check week splitting
        print(f"Data with Week column added:")
        print(df.head())  # Print the first few rows to verify
        
        # Return the mean of the last 7 weeks (3 past + 4 future)
        return df.groupby('Week')['Close'].mean().tail(7)  # Last 7 weeks
    
    except Exception as e:
        print(f"Error splitting data by weeks: {e}")
        return None

# Test the function independently (to be run separately from Flask)
if __name__ == "__main__":
    # Test with a company (ticker symbol)
    company = "TCS.NS"  # For Indian market, TCS's symbol is TCS.NS (adjust accordingly)
    df = get_stock_data(company)
    
    # If data is valid, print it
    if df is not None:
        print(df)
    else:
        print(f"No data found for {company}")
