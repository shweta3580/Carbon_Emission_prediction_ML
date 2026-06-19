# Importing necessary libraries
from fastapi import FastAPI
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
import joblib
import nest_asyncio
import uvicorn
import subprocess

# Apply nest_asyncio (useful for notebooks)
nest_asyncio.apply()

app = FastAPI()

# Load the dataset
df = pd.read_csv("world_bank_dataset_final.csv")  # Ensure this file exists in your directory

# Data Cleaning and Preprocessing
df.dropna(inplace=True)

numeric_columns = ['GDP (USD)', 'Population', 'Life Expectancy', 'Unemployment Rate (%)',
                   'CO2 Emissions (metric tons per capita)', 'Access to Electricity (%)']

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df.fillna(df.mean(numeric_only=True), inplace=True)

# Scale the data
scaler = MinMaxScaler()
scaled_features = scaler.fit_transform(df[numeric_columns])
scaled_df = pd.DataFrame(scaled_features, columns=numeric_columns)
scaled_df['Country'] = df['Country'].values
scaled_df['Year'] = df['Year'].values
df = scaled_df.copy()

# K-Means Clustering
kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
df['Cluster'] = kmeans.fit_predict(df[numeric_columns])

# Predictive Modeling with Random Forest
X = df[['Year', 'Population', 'Unemployment Rate (%)', 'CO2 Emissions (metric tons per capita)', 'Access to Electricity (%)', 'Cluster']]
y = df['Life Expectancy']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

y_pred = rf_model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f"\nRandom Forest RMSE: {rmse}")

# API Endpoints
@app.post("/predict")
def predict_emissions(data: dict):
    model = joblib.load("carbon_model.pkl")
    scaler = joblib.load("scaler.pkl")
    input_data = np.array([[data['gdp'], data['energy'], data['industry_output'], data['population'], data['regulations']]])
    input_scaled = scaler.transform(input_data)
    prediction = model.predict(input_scaled)[0]
    return {"predicted_CO2_emissions": prediction}

@app.get("/trends")
def get_trends():
    trends = df.groupby("Year")["CO2 Emissions (metric tons per capita)"].mean().reset_index()
    return trends.to_dict(orient="records")

@app.get("/optimize")
def optimize_regulations():
    optimal_action = np.argmax(Q_table.mean(axis=0))
    return {"recommended_regulation_level": optimal_action}

# Run FastAPI server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# 🔹 NGROK INTEGRATION
NGROK_AUTH_TOKEN = "2vAcLURM8JyMhbuHm3St9UJRwdf_3J4xi2hP3a3MEAnbnu7cT"  # Replace with your actual ngrok token

if NGROK_AUTH_TOKEN:
    subprocess.run(["ngrok", "authtoken", NGROK_AUTH_TOKEN], check=True)
    subprocess.run(["ngrok", "http", "8000"], check=True)
else:
    print("Error: NGROK_AUTH_TOKEN is not set!")
