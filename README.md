# gold_demand_forecasting
jewellery_demand_forecasting/
│── data/
│   ├── raw/                  # Raw sales, stock & gold price data
│   ├── processed/            # Cleaned & preprocessed datasets
│── notebooks/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_model_training.ipynb
│── src/
│   ├── __init__.py
│   ├── data_preprocessing.py # Cleaning, feature engineering
│   ├── model.py              # Training & prediction code
│   ├── utils.py              # Helper functions (plotting, metrics)
│── app/
│   ├── main.py               # FastAPI/Streamlit entrypoint
│   ├── requirements.txt
│   ├── config.yaml           # Config file (model path, data path, API keys)
│── models/
│   ├── demand_forecast.pkl   # Trained ML model
│── tests/
│   ├── test_preprocessing.py
│   ├── test_model.py
│── README.md
│── .gitignore
