import yfinance as yf
import pandas as pd
import numpy as np 
import streamlit as st
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
from datetime import datetime, timedelta


@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_data(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period="1y")
    return data


# def get_data(ticker):
#     import yfinance as yf
#     stock = yf.Ticker(ticker)
#     data = stock.history(period="1y")

#     if data is None or data.empty:
#         raise ValueError(f"Error: No data found for ticker {ticker}")

#     return data



# def get_data(ticker):
#     stock_data = yf.download(ticker, start='2024-01-01')
    
#     for attempt in range(5):  # Retry up to 5 times
#         try:
#             return stock_data.info
#         except yf.YFRateLimitError:
#             wait_time = (attempt + 1) * 5  # Exponential backoff (5s, 10s, 15s...)
#             print(f"Rate limit hit. Retrying in {wait_time} seconds...")
#             time.sleep(wait_time)

#     return None


def stationary_check(clode_price):
    adf_test = adfuller(clode_price)
    p_value = round(adf_test[1],3)
    return p_value


def get_rolling_mean(close_price):
    if not isinstance(close_price, pd.Series):
        raise TypeError("close_price must be a Pandas Series!")

    rolling_price = close_price.rolling(window=7).mean().dropna()
    return rolling_price


def get_differencing_order(close_price):
    p_value = stationary_check(close_price)
    d = 0
    while True:
        if p_value > 0.05:
            d = d + 1
            close_price = close_price.diff().dropna()
            p_value = stationary_check(close_price)
        else:
            break
    return d


def fit_model(data,differencing_order):
    model = ARIMA(data, order=(30, differencing_order, 30))
    model_fit = model.fit()

    forcast_steps = 30
    forcast = model_fit.get_forcast(steps=forcast_steps)

    predictions = forecast.predicted_mean
    return predictions


def evaluate_model(original_price, differencing_order):
    train_data, test_data = original_price[:-30], original_price[-30:]
    predictions = fit_model(train_data, differencing_order)
    rmse = np.sqrt(mean_squared_error(test_data, predictions))

    return round(rmse, 2)


def get_scalling(close_price):
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(np.array(close_price).reshape(-1,1))

    return scaled_data, scaler


def get_forcast(original_price, differencing_order):
    predictions = fit_model(original_price, differencing_order)
    start_date = datetime.now().strftime('%Y-%m-%d')
    end_date = (datetime.now() + timedelta(days=29)).strftime('%Y-%m-%d')
    forcast_index = pd.date_range(start=start_date, end=end_date, freq='D')
    forcast_df = pd.DataFrame(predictions, index=forcast_index, columns=['Close'])

    return forcast_df


def inverse_scaling(scaler, scaled_data):
    close_price = scaler.inverse_transform(np.array(scaled_data).reshape(-1,1))
    
    return close_price
