import streamlit as st

st.set_page_config(
    page_title = "Trading App",
    page_icon = "chart_with_downwards_trend:",
    layout = "wide"
)

st.header("Trading Guide App")

st.header("We provide the greatest for you to collect all information prier to investing in stocks.")

#st.image("a.png")

st.markdown("## We provide the following services:")

st.markdown("### :one: Stock Information")
st.write("Through this page, you can see all the information about stock.")

st.markdown("### :two: Stock Prediction")
st.write("You can explore predicted closing prices for the next 30 days based on historical stock data and advanced forecasting modls.Use this tool to gain valuable indights into market trends and make informed investment decisions.")

st.markdown("### :three: CAPM Return")
st.write("Discover how the Capital Asset Pricing Model(CAPM) calculates the expected return of different asset based on its risk and market performace. ")

st.markdown("### :four: CAPM Beta")
st.write("Calculates Beta and Expected Return for individual Stocks.")
