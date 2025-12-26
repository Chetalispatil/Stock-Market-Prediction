
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import get_stock_data
from lstm_model import train_and_predict
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pandas as pd
import os
import numpy as np

app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if not data or 'company' not in data:
        return jsonify({'error': 'Company name is required'}), 400

    company_name = data['company']  # Use consistently
    ticker = f"{company_name}.NS"  # NSE stock format

    # Fetch stock data
    df = get_stock_data(ticker)
    if df is None:
        return jsonify({'error': 'Stock data for the company could not be retrieved'}), 500

    df.columns = ['Date', 'Close']
    df['Date'] = pd.to_datetime(df['Date'])

    # Call LSTM model for predictions
    predictions = train_and_predict(company_name, df)
    predictions_list = predictions.tolist() if hasattr(predictions, 'tolist') else list(predictions)

    # Generate future dates
    start_date = datetime.today() + timedelta(days=1)
    dates = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(len(predictions_list))]
    predicted_with_dates = [{"date": date, "price": round(price, 2)} for date, price in zip(dates, predictions_list)]

    # Line Graph
    future_dates = [df['Date'].iloc[-1] + timedelta(days=i + 1) for i in range(30)]
    prediction_df = pd.DataFrame({'Date': future_dates, 'Predicted': predictions_list})

    plt.figure(figsize=(10, 5))
    plt.plot(prediction_df['Date'], prediction_df['Predicted'], label="Predicted Prices", color='green')
    plt.xticks(rotation=45)
    plt.title(f"{company_name} - 30-Day Stock Price Prediction")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    line_graph_path = f'static/graphs/{company_name}_line.png'
    plt.tight_layout()
    plt.savefig(line_graph_path)
    plt.close()

    # Weekly Averages Bar Graph
    past_data = df.tail(21).copy()
    past_data['Week'] = pd.to_datetime(past_data['Date']).dt.to_period('W')
    past_avg = past_data.groupby('Week')['Close'].mean().tolist()

    future_data = prediction_df.copy()
    future_data['Week'] = pd.to_datetime(future_data['Date']).dt.to_period('W')
    future_avg = future_data.groupby('Week')['Predicted'].mean().tolist()[:4]

    averages = past_avg + future_avg
    all_weeks = [f"Last Week {i+1}" for i in reversed(range(len(past_avg)))] + \
                [f"Next Week {i+1}" for i in range(len(future_avg))]

    plt.figure(figsize=(10, 5))
    plt.bar(all_weeks, averages, color='skyblue')
    plt.title(f"{company_name} - Weekly Average Prices")
    plt.xlabel("Week")
    plt.ylabel("Average Price")
    plt.xticks(rotation=15)
    bar_graph_path = f'static/graphs/{company_name}_bar.png'
    plt.tight_layout()
    plt.savefig(bar_graph_path)
    plt.close()

    # Generate Stock Analysis Report
    peak_price = max(predictions_list)
    low_price = min(predictions_list)
    trend = "Rising " if predictions_list[-1] > predictions_list[0] else "Falling "
    buy_day = predictions_list.index(low_price) + 1
    sell_day = predictions_list.index(peak_price) + 1
    avg_price = np.mean(predictions_list)
    price_std = np.std(predictions_list)
    confidence_range = f"₹{avg_price - price_std:.2f} - ₹{avg_price + price_std:.2f}"

    daily_changes = [predictions_list[i+1] - predictions_list[i] for i in range(len(predictions_list)-1)]
    positive_days = sum(1 for change in daily_changes if change > 0)
    negative_days = sum(1 for change in daily_changes if change < 0)
    steady_days = len(predictions_list) - 1 - positive_days - negative_days

    report_text = f"""
    🏢 Company: {company_name}

    1.  Executive Summary:
    -------------------------
    The model has forecasted the next 30 days of stock prices using LSTM-based time series modeling,
    leveraging historical data trends for future price prediction.

    2.  Key Insights:
    -------------------
      Predicted Peak Price: ₹{peak_price:.2f} (Day {sell_day})
      Predicted Low Price: ₹{low_price:.2f} (Day {buy_day})
      Average Predicted Price: ₹{avg_price:.2f}
      Confidence Interval (±1σ): {confidence_range}
      Trend: {trend}
      Volatility: {'High ' if price_std > 20 else 'Moderate ' if price_std > 10 else 'Low '}

    3.  Daily Change Summary:
    ----------------------------
      Days with Price Increase: {positive_days}
      Days with Price Decrease: {negative_days}
      Days with Minimal Change: {steady_days}

    4.  Actionable Recommendations:
    ----------------------------
       Buy Recommendation: Day {buy_day}
       Sell Recommendation: Day {sell_day}
       Hold: On all other days with minimal fluctuations

    📝 Note: This analysis is based on predictive modeling and may not account for sudden market events. Exercise due diligence.
    """
    return jsonify({
        "company": company_name,
        "lineGraph": line_graph_path,
        "barGraph": bar_graph_path,
        "predictions": predicted_with_dates,
        "report": report_text
    })

@app.route('/')
def index():
    return "✅ Backend is running"

if __name__ == '__main__':
    os.makedirs("static/graphs", exist_ok=True)
    app.run(debug=True)
