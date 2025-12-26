### Stock Price Prediction Using LSTM

A full-stack web application that predicts next 30 days stock prices for NIFTY 50 companies using a Long Short-Term Memory (LSTM) deep learning model. The system provides visual analysis, statistical insights, and downloadable PDF reports to support informed investment decisions.

 ## Features

 1. 30-day stock price prediction using LSTM

 2. Select from NIFTY 50 companies

 3. Line graph for future price trends

 4. Weekly average bar chart

 5. Auto-generated stock analysis report

 6. Download report as PDF

 7. Responsive and user-friendly UI

## Tech Stack
Frontend
React.js
HTML5, CSS3
Axios
jsPDF, html2canvas

Backend
Python (Flask)
TensorFlow / Keras
Pandas, NumPy
yFinance
Matplotlib


## Project Architecture
Stock-Price-Prediction/
│
├── backend/
│   ├── app.py
│   ├── lstm_model.py
│   ├── utils.py
│   └── static/graphs/
│
├── frontend/
│   ├── App.js
│   ├── App.css
│   └── package.json
│
└── README.md

## How It Works

User selects a company from NIFTY 50

Frontend sends request to Flask backend

Backend fetches historical stock data

LSTM model predicts next 30 days prices

Graphs and insights are generated

Results are displayed on UI

User can download the report as PDF


## Machine Learning Model

Model: Long Short-Term Memory (LSTM)

Input: Last 30 days closing prices

Output: Next 30 days predicted prices

Scaling: MinMaxScaler

Framework: TensorFlow / Keras

## Installation & Setup
1️ Backend Setup
pip install flask flask-cors tensorflow keras pandas numpy yfinance matplotlib
python app.py


Backend runs at:

http://localhost:5000

2️ Frontend Setup
npm install
npm start


## Sample Outputs

Line graph showing predicted daily prices

Bar chart showing weekly averages

Text-based analytical report

Downloadable PDF report


## Future Enhancements

News-based sentiment analysis

Improved prediction accuracy

Cloud deployment

Support for global stock markets

User authentication & dashboards


## Disclaimer

This project is for educational purposes only.
Stock market predictions are uncertain and should not be used as financial advice.

## Author

Chetali Patil
B.Tech Computer Science
