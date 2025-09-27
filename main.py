from fastapi import FastAPI
import pickle
import pandas as pd

app = FastAPI()

# Load trained model
with open("models/demand_forecast.pkl", "rb") as f:
    model = pickle.load(f)

@app.get("/")
def home():
    return {"message": "Jewellery Demand Forecasting API is running!"}

@app.post("/predict")
def predict(data: dict):
    df = pd.DataFrame([data])
    prediction = model.predict(df)[0]
    return {"predicted_demand": round(prediction, 2)}
