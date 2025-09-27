import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title
st.title("💎 Jewellery Shop Demand & Purchase Recommendation")

# Sidebar inputs (owner can update stock & gold price manually if needed)
st.sidebar.header("Today's Inputs")
current_stock = st.sidebar.number_input("Current Stock (grams)", min_value=0, value=2000)
today_price = st.sidebar.number_input("Today's Gold Price (₹/g)", min_value=4000, value=5800)

# Upload option for real sales data
uploaded_file = st.sidebar.file_uploader("Upload Sales Data CSV", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, parse_dates=["Date"])
else:
    st.warning("⚠️ No file uploaded. Using dummy dataset.")
    # fallback (Phase 1 dummy df)
    df = df  # assuming Phase 1 dataframe is loaded

# Show data preview
st.subheader("📊 Data Preview")
st.dataframe(df.tail(10))

# Forecast plot (assuming best_pred is available from Phase 2)
st.subheader("📈 Sales Forecast vs Actual")
plt.figure(figsize=(10,5))
plt.plot(df["Date"], df["SalesQty"], label="Actual Sales")
plt.plot(df["Date"][-len(best_pred):], best_pred, label="Forecast", color="red")
plt.legend()
st.pyplot(plt)

# Gold Price Trend
st.subheader("💰 Gold Price Trend")
plt.figure(figsize=(10,5))
plt.plot(df["Date"], df["GoldPrice"], label="Gold Price")
plt.plot(df["Date"], df["GoldPrice"].rolling(7).mean(), label="7-day Avg", linestyle="dashed")
plt.legend()
st.pyplot(plt)

# Recommendation Engine (Phase 3 function)
today = df["Date"].iloc[-1]  # last date as today
result = decision_engine(df, best_pred, today_date=today)

# Show recommendation
st.subheader("📌 Today's Recommendation")
st.markdown(f"### {result['Recommendation']}")
st.metric("Buy Quantity (grams)", result["BuyQty"])
st.text(f"Reason: {result['Reason']}")
