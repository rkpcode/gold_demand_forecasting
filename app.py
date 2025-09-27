import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
import numpy as np
from datetime import datetime

# Title
st.title("💎 Jewellery Shop Demand & Purchase Recommendation")

# Sidebar inputs
st.sidebar.header("Today's Inputs")
current_stock = st.sidebar.number_input("Current Stock (grams)", min_value=0, value=2000)
manual_gold_price = st.sidebar.number_input("Manual Gold Price (₹/g) - Use if API fails", min_value=4000, value=11488)
api_key = st.sidebar.text_input("API Key for GoldPriceZ (optional for custom API)")

# Function to fetch live gold price
@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_gold_price():
    try:
        if api_key:
            url = "https://goldpricez.com/api/rates/currency/inr/measure/gram"
            headers = {"X-API-KEY": api_key}
            response = requests.get(url, headers=headers)
        else:
            url = "https://api.api-ninjas.com/v1/goldprice?country=india"
            response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            if 'gram_in_inr' in data:
                price_inr_per_gram = data['gram_in_inr']
            elif isinstance(data, list) and 'price_per_gram' in data[0]:
                price_inr_per_gram = data[0]['price_per_gram']
            else:
                raise ValueError("Unexpected response format")
            return round(price_inr_per_gram, 2)
        else:
            st.warning(f"API call failed with status {response.status_code}. Using manual price.")
            return manual_gold_price
    except Exception as e:
        st.error(f"Error fetching price: {e}. Using manual price.")
        return manual_gold_price

# Fetch latest gold price
latest_gold_price = fetch_gold_price()
st.sidebar.metric("Live Gold Price (₹/g)", latest_gold_price)

# Upload option for real sales data
uploaded_file = st.sidebar.file_uploader("Upload Sales Data CSV", type="csv", key="sales_data_uploader")
if uploaded_file is not None:
    try:
        st.write("Processing uploaded file...")
        file_content = uploaded_file.read()
        if not file_content:
            st.error("Uploaded file is empty.")
            df = None
        else:
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file, parse_dates=["Date"], dayfirst=True)
            if df.empty:
                st.warning("Uploaded CSV is empty after reading.")
                df = None
            else:
                st.success("File uploaded successfully!")
    except ValueError as ve:
        st.error(f"Date parsing error: {ve}. Please ensure 'Date' column is in a valid format (e.g., DD/MM/YYYY or YYYY-MM-DD). Using dummy data.")
        df = None
    except Exception as e:
        st.error(f"Error loading CSV: {e}. Using dummy dataset. Check file format or permissions.")
        df = None
else:
    st.warning("⚠️ No file uploaded. Using dummy dataset.")
    df = None

# If df is None or empty, use dummy with seasonal pattern
if df is None or df.empty:
    dates = pd.date_range(start="2023-01-01", periods=24, freq='M')
    base_sales = np.array([100, 120, 150, 130, 140, 160, 180, 170, 190, 200, 220, 250] * 2)  # 24 elements
    seasonal_factor = np.tile(np.sin(np.linspace(0, 2 * np.pi, 12)) * 50 + 150, 2)  # Repeat 12-month pattern twice
    sales_qty = base_sales + seasonal_factor.astype(int)  # Ensure integer conversion after addition
    df = pd.DataFrame({
        "Date": dates,
        "SalesQty": sales_qty,
        "GoldPrice": latest_gold_price
    })

# Ensure Date is datetime and sort, set index
if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"], errors='coerce', dayfirst=True)
    df = df.sort_values("Date").dropna(subset=["Date"])
    df.set_index("Date", inplace=True)

# Add or update GoldPrice column
if "GoldPrice" not in df.columns:
    df["GoldPrice"] = latest_gold_price
else:
    df["GoldPrice"].fillna(latest_gold_price, inplace=True)

# Show data preview
st.subheader("📊 Data Preview")
st.dataframe(df.tail(10))

# Simple Moving Average Forecast
st.subheader("🧠 Forecasting Model")
if "SalesQty" in df.columns and len(df) >= 3:  # Need at least 3 points for moving average
    try:
        window = min(3, len(df))  # Use 3-period or all available data
        moving_avg = df["SalesQty"].rolling(window=window, min_periods=1).mean()
        forecast_steps = 5
        last_avg = moving_avg.iloc[-1]
        best_pred = np.full(forecast_steps, last_avg)
        forecast_index = pd.date_range(start=df.index[-1] + pd.Timedelta(days=1), periods=forecast_steps, freq='D')
        st.success("Simple moving average forecast generated.")
    except Exception as e:
        st.error(f"Error in calculating moving average: {e}. Using dummy forecast.")
        best_pred = np.array([df["SalesQty"].mean()] * 5)
        forecast_index = pd.date_range(start=df.index[-1] + pd.Timedelta(days=1), periods=5, freq='D')
else:
    st.warning("Not enough data for forecasting. Using dummy.")
    best_pred = np.array([150] * 5)
    forecast_index = pd.date_range(start=df.index[-1] + pd.Timedelta(days=1), periods=5, freq='D')

# Forecast plot
st.subheader("📈 Sales Forecast vs Actual")
if "SalesQty" in df.columns:
    try:
        plt.figure(figsize=(10, 5))
        plt.plot(df.index, df["SalesQty"], label="Actual Sales")
        plt.plot(forecast_index, best_pred, label="Forecast", color="red")
        plt.legend()
        st.pyplot(plt)
    except Exception as e:
        st.error(f"Error in plotting forecast: {e}")
else:
    st.write("Missing 'SalesQty' column.")

# Gold Price Trend
st.subheader("💰 Gold Price Trend")
if "GoldPrice" in df.columns:
    try:
        plt.figure(figsize=(10, 5))
        plt.plot(df.index, df["GoldPrice"], label="Gold Price")
        window = min(7, len(df))
        if window > 1:
            plt.plot(df.index, df["GoldPrice"].rolling(window).mean(), label=f"{window}-day Avg", linestyle="dashed")
        else:
            st.info("Not enough data for rolling average.")
        plt.legend()
        st.pyplot(plt)
    except Exception as e:
        st.error(f"Error in plotting gold trend: {e}")
else:
    st.write("Missing 'GoldPrice' column.")

# Decision Engine with seasonal insight
def decision_engine(df, best_pred, today_date, current_stock, latest_gold_price):
    try:
        future_demand = sum(best_pred)
        today_month = today_date.month
        seasonal_boost = 1.0
        festive_months = [10, 11, 12]  # Oct, Nov, Dec (Diwali, wedding season)
        if today_month in festive_months:
            seasonal_boost = 1.3
        
        adjusted_demand = future_demand * seasonal_boost
        is_price_low = latest_gold_price < df["GoldPrice"].mean()
        buy_qty = max(0, adjusted_demand - current_stock)
        if is_price_low:
            buy_qty *= 1.2
        
        buy_qty = round(buy_qty)
        recommendation = f"Buy Gold (Price is {'low' if is_price_low else 'normal'}, Seasonal Boost: {'Yes' if today_month in festive_months else 'No'})" if buy_qty > 0 else "Hold Stock (Sufficient inventory)"
        return {"Recommendation": recommendation, "BuyQty": buy_qty}
    except Exception as e:
        st.error(f"Error in decision engine: {e}")
        return {"Recommendation": "Error", "BuyQty": 0}

# Recommendation Engine
try:
    today = pd.to_datetime("today") if df.empty else df.index[-1]
    result = decision_engine(df, best_pred, today_date=today, current_stock=current_stock, latest_gold_price=latest_gold_price)
except Exception as e:
    st.error(f"Error getting today date: {e}")
    result = {"Recommendation": "Error", "BuyQty": 0}

# Show recommendation
st.subheader("📌 Today's Recommendation")
st.markdown(f"### {result['Recommendation']}")
st.metric("Buy Quantity (grams)", result["BuyQty"])