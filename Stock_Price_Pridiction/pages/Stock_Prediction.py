import streamlit as st
from pages.utils.model_train import get_data, stationary_check, get_rolling_mean, get_differencing_order, fit_model, evaluate_model, get_scalling, get_forcast
import pandas as pd
from pages.utils.plotly_figure import plotly_table, Moving_average_forcast

st.set_page_config(
    page_title="Stock Prediction",
    page_icon="chart_with_downwards_trend",
    layout="wide",
)

st.title("Stock Prediction")

col1, col2, clo3 = st.columns(3)

with col1:
    ticker = st.text_input("Stock Ticker", "TSLA")

rmse = 0

st.subheader('Predicting Next 20 days Close Price for: '+ticker)

close_price = get_data(ticker)
rolling_price = get_rolling_mean(close_price)

differencing_order = get_differencing_order(rolling_price)
scaled_data, scaler = get_scalling(rolling_price)
rmse = evaluate_model(scaled_data, differencing_order)

st.write("**Model RMSE Score:**", rmse)

forcast = get_forcast(scaled_data, differencing_order)

forcast['Close'] = inverse_scaling(scaler, forcast['Close'])
st.write("##### Forecast Data (Next 30 days)")

fig_tail = plotly_table(forecast.sort_index(ascending=True).round(3))
fig_tail.update_layout(height = 220)
st.plotly_chart(fig_tail, use_container_width=True, config={"displayModeBar": False})

forcast = pd.concat([rolling_price, forcast])

st.plotly_chart(Moving_average_forcast(forcast.iloc[150:]), use_container_width=True)