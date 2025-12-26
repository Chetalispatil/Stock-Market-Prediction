import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Input, LSTM, Dense
import os

# Caches for models and scalers
model_cache = {}
scaler_cache = {}

def prepare_data(data):
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(data[['Close']])
    
    X, y = [], []
    for i in range(30, len(scaled)):
        X.append(scaled[i-30:i])
        y.append(scaled[i])
    
    X, y = np.array(X), np.array(y)
    X = X.reshape((X.shape[0], X.shape[1], 1))
    return X, y, scaler

def build_model(input_shape):
    model = Sequential()
    model.add(Input(shape=(10, 1)))  # instead of passing input_shape in LSTM
    model.add(LSTM(50))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    return model

def train_model_for_company(company_name, data):
    if company_name in model_cache:
        return model_cache[company_name], scaler_cache[company_name]

    X, y, scaler = prepare_data(data)
    model = build_model((X.shape[1], 1))
    model.fit(X, y, epochs=5, batch_size=32, verbose=0)

    model_cache[company_name] = model
    scaler_cache[company_name] = scaler

    return model, scaler

def predict_next_30_days(company_name, data):
    model, scaler = train_model_for_company(company_name, data)

    scaled = scaler.transform(data[['Close']])
    last_30 = scaled[-30:]

    preds = []
    current_input = last_30

    for _ in range(30):
        pred = model.predict(current_input.reshape(1, 30, 1), verbose=0)
        preds.append(pred[0][0])
        current_input = np.append(current_input[1:], pred).reshape(30, 1)

    preds_rescaled = scaler.inverse_transform(np.array(preds).reshape(-1, 1))
    return preds_rescaled.flatten().tolist()

def train_and_predict(company_name, data):
    return predict_next_30_days(company_name, data)
