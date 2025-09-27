# 💎 Jewellery Shop Demand Forecasting System

**Predict daily buying quantity for a jewellery shop using past sales, inventory, and gold price data.**

---

## 🏆 Project Overview

This project provides a **data-driven decision support system** for jewellery shop owners. Currently, the owner manually decides how much gold/jewellery to purchase each day. This system automates that process by:

1. Forecasting future demand using historical sales data.
2. Considering current stock levels and gold price trends.
3. Providing daily actionable recommendations on purchase quantity.
4. Presenting results in an **interactive dashboard** for easy use.

---

## 📂 Repository Structure
jewellery_demand_forecasting/ │── data/ │   ├── raw/                  # Raw sales, stock & gold price data │   ├── processed/            # Cleaned & preprocessed datasets │── notebooks/ │   ├── 01_data_cleaning.ipynb │   ├── 02_eda.ipynb │   ├── 03_model_training.ipynb │── src/ │   ├── data_preprocessing.py # Cleaning & feature engineering │   ├── model.py              # Model training & prediction │   ├── utils.py              # Helper functions │── app/ │   ├── main.py               # FastAPI backend │   ├── streamlit_app.py      # Interactive dashboard │   ├── requirements.txt │   ├── config.yaml │── models/ │   ├── demand_forecast.pkl   # Trained model │── tests/ │   ├── test_preprocessing.py │   ├── test_model.py │── README.md │── .gitignore

---

## ⚡ Features

- **Demand Forecasting:** Predict next 7 days of jewellery sales using Prophet or ARIMA models.
- **Inventory Management:** Suggests daily purchase quantity based on current stock and forecast.
- **Gold Price Awareness:** Adjusts recommendation based on real-time gold price trends.
- **Festival & Seasonality Handling:** Automatically accounts for sales spikes during festivals.
- **Interactive Dashboard:** Streamlit-based GUI for non-technical users.
- **API Ready:** FastAPI backend for future integrations with mobile or web apps.

---

## 🛠 Technology Stack

- **Python** → Data processing & model development
- **Pandas & NumPy** → Data handling
- **Prophet / statsmodels (ARIMA)** → Time series forecasting
- **scikit-learn** → Helper metrics & ML utilities
- **Matplotlib / Plotly** → Visualization
- **Streamlit** → Interactive dashboard
- **FastAPI** → Backend API for predictions

---

## 🚀 Usage

### 1. Clone Repository
```bash
git clone https://github.com/rkpcode/jewellery_demand_forecasting.git
cd jewellery_demand_forecasting

## 🌐 Live Demo
[![Streamlit App](https://img.shields.io/badge/Streamlit-Live%20App-brightgreen?logo=streamlit)](https://lalchandgbrt.streamlit.app)