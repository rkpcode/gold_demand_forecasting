import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
import requests  # For API call

# Title
st.title("💎 Jewellery Shop Demand & Purchase Recommendation")

# Sidebar inputs
st.sidebar.header("Today's Inputs")
current_stock = st.sidebar.number_input("Current Stock (grams)", min_value=0, value=2000)
today_price = st.sidebar.number_input("Today's Gold Price (₹/g)", min_value=4000, value=5800)

# Function to fetch live gold price from free API
@st.cache_data(ttl=3600)  # Cache for 1 hour to avoid too many calls
def fetch_gold_price():
    try:
        # GoldAPI.io free endpoint (USD per ounce)
        url = "https://www.goldapi.io/api/XAU/USD"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            price_usd_per_oz = data['price']  # USD per ounce
            # Convert to INR per gram (approx: 1 oz = 31.1035g, USD-INR rate ~83.5, adjust as needed)
            usd_inr_rate = 83.5  # You can fetch this from another free API like exchangerate-api.com
            price_inr_per_gram = (price_usd_per_oz * usd_inr_rate) / 31.1035
            return round(price_inr_per_gram, 2)
        else:
            st.warning("API call failed, using fallback price.")
            return 5800  # Fallback
    except Exception as e:
        st.warning(f"Error fetching price: {e}. Using fallback.")
        return 5800

# Fetch latest gold price
latest_gold_price = fetch_gold_price()
st.sidebar.metric("Live Gold Price (₹/g)", latest_gold_price)

# Upload option for real sales data
uploaded_file = st.sidebar.file_uploader("Upload Sales Data CSV", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, parse_dates=["Date"])
    # Fill or overwrite GoldPrice column with latest price (for simplicity; adjust for historical if needed)
    if "GoldPrice" in df.columns:
        df["GoldPrice"] = latest_gold_price  # Or append historical logic
    else:
        df["GoldPrice"] = latest_gold_price
else:
    st.warning("⚠️ No file uploaded. Using dummy dataset.")
    # Generate dummy DataFrame with API price
    dates = pd.date_range(start="2023-01-01", periods=10)
    df = pd.DataFrame({
        "Date": dates,
        "SalesQty": [100, 120, 150, 130, 140, 160, 180, 170, 190, 200],
        "GoldPrice": latest_gold_price  # Use API price
    })

# Show data preview
st.subheader("📊 Data Preview")
st.dataframe(df.tail(10))

# Placeholder for best_pred
if 'best_pred' not in locals() or len(best_pred) == 0:
    best_pred = [150] * 5  # Dummy forecast

# Forecast plot
st.subheader("📈 Sales Forecast vs Actual")
if "Date" in df.columns and "SalesQty" in df.columns:
    plt.figure(figsize=(10, 5))
    plt.plot(df["Date"], df["SalesQty"], label="Actual Sales")
    plt.plot(df["Date"][-len(best_pred):], best_pred, label="Forecast", color="red")
    plt.legend()
    st.pyplot(plt)
else:
    st.write("Missing 'Date' or 'SalesQty' columns.")

# Gold Price Trend (now with API-updated data)
st.subheader("💰 Gold Price Trend")
if "Date" in df.columns and "GoldPrice" in df.columns:
    plt.figure(figsize=(10, 5))
    plt.plot(df["Date"], df["GoldPrice"], label="Gold Price")
    plt.plot(df["Date"], df["GoldPrice"].rolling(7).mean(), label="7-day Avg", linestyle="dashed")
    plt.legend()
    st.pyplot(plt)
else:
    st.write("Missing 'Date' or 'GoldPrice' columns.")

# Placeholder decision_engine
def decision_engine(df, best_pred, today_date):
    if len(best_pred) > 0 and best_pred[-1] > df["SalesQty"].mean():
        return {"Recommendation": "Buy Gold", "BuyQty": 50}
    return {"Recommendation": "Hold Stock", "BuyQty": 0}

# Recommendation Engine
if "Date" in df.columns:
    today = df["Date"].iloc[-1]
else:
    today = pd.to_datetime("2023-01-10")
result = decision_engine(df, best_pred, today_date=today)

# Show recommendation
st.subheader("📌 Today's Recommendation")
st.markdown(f"### {result['Recommendation']}")
st.metric("Buy Quantity (grams)", result["BuyQty"])