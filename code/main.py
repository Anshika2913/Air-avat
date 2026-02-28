from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
import joblib
import numpy as np
import pandas as pd

from safety_engine import classify_health, generate_alert

app = FastAPI(title="AIR-AVAT Predictive Maintenance API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model and scaler
model = joblib.load("rf_model.pkl")
scaler = joblib.load("scaler.pkl")


@app.post("/predict")
def predict(sensor_input: dict):

    input_df = pd.DataFrame([sensor_input])
    input_scaled = scaler.transform(input_df)

    predicted_rul = model.predict(input_scaled)[0]

    health_status = classify_health(predicted_rul)
    alerts = generate_alert(predicted_rul, sensor_input)

    return {
        "Predicted_RUL": round(float(predicted_rul), 2),
        "Health_Status": health_status,
        "Alerts": alerts
    }