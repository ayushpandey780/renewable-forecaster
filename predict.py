import pandas as pd
import xgboost as xgb
import os
from datetime import datetime

print("\n=== AI Renewable Energy Forecaster ===")

# 1. Load the trained model
model_path = os.path.join('models', 'solar_forecaster.json')
model = xgb.XGBRegressor()
model.load_model(model_path)
print("[System] XGBoost Model loaded successfully.")

# 2. Load the latest scraped weather data
data_path = os.path.join('data', 'raw', 'ranchi_weather_log.csv')
try:
    # Get the very last row of the CSV
    latest_data = pd.read_csv(data_path).tail(1).iloc[0]
    timestamp = pd.to_datetime(latest_data['timestamp'])
    
    print(f"\n--- Latest Live Weather (Ranchi) ---")
    print(f"Time: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Humidity: {latest_data['humidity_percent']}%")
    print(f"Wind Speed: {latest_data['wind_speed_kmh']} km/h")
except Exception as e:
    print(f"Error loading live data: {e}")
    exit()

# 3. Handle Missing Features (Interactive input)
print("\n[System] Model requires Temperature and Cloud Cover.")
try:
    temp = float(input("Enter current temperature in °C (e.g., 28): "))
    clouds = float(input("Enter estimated cloud cover % (0=clear, 100=overcast): "))
except ValueError:
    print("Invalid input. Please enter numbers only.")
    exit()

# 4. Prepare the exact feature array the model expects
input_data = pd.DataFrame([{
    'temperature_c': temp,
    'humidity_percent': latest_data['humidity_percent'],
    'wind_speed_kmh': latest_data['wind_speed_kmh'],
    'cloud_cover_percent': clouds,
    'hour': timestamp.hour,
    'month': timestamp.month,
    'day_of_year': timestamp.dayofyear
}])

# 5. Make the Prediction
prediction = model.predict(input_data)[0]

# Ensure the prediction doesn't output negative numbers due to model noise
final_kw = max(0, prediction)

print("\n========================================")
print(f"☀️ PREDICTED SOLAR OUTPUT: {final_kw:.2f} kW")
print("========================================")

if final_kw == 0:
    print("Note: Output is 0 because it is nighttime or cloud cover is too extreme.")
