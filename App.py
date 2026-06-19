import streamlit as st
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# FastAPI backend URL
FASTAPI_URL = "http://127.0.0.1:8000"

st.title("CO2 Emission Prediction & Optimization")
st.write("This app predicts CO2 emissions based on economic and energy factors.")

# User Input for Prediction
gdp = st.number_input("GDP (USD)", min_value=0.0, format="%.2f")
energy = st.number_input("Energy Consumption", min_value=0.0, format="%.2f")
industry_output = st.number_input("Industry Output", min_value=0.0, format="%.2f")
population = st.number_input("Population", min_value=0.0, format="%.2f")
regulations = st.slider("Regulation Level", 0, 10, 5)

if st.button("Predict CO2 Emissions"):
    data = {"gdp": gdp, "energy": energy, "industry_output": industry_output, "population": population, "regulations": regulations}
    response = requests.post(f"{FASTAPI_URL}/predict", json=data)
    if response.status_code == 200:
        st.success(f"Predicted CO2 Emissions: {response.json()['predicted_CO2_emissions']:.2f} metric tons per capita")
    else:
        st.error("Error: Unable to get prediction.")

# Display Trends from API
if st.button("Show CO2 Trends"):
    response = requests.get(f"{FASTAPI_URL}/trends")
    if response.status_code == 200:
        trends = pd.DataFrame(response.json())
        st.line_chart(trends.set_index("Year"))
    else:
        st.error("Error fetching trends.")

# Show Optimization Recommendation
if st.button("Optimize Regulations"):
    response = requests.get(f"{FASTAPI_URL}/optimize")
    if response.status_code == 200:
        st.info(f"Recommended Regulation Level: {response.json()['recommended_regulation_level']}")
    else:
        st.error("Error optimizing regulations.")

# Load EDA Visualizations
st.write("### Exploratory Data Analysis")
if st.button("Show Heatmap"):
    df = pd.read_csv("/content/world_bank_dataset.csv")
    numeric_columns = ['GDP (USD)', 'Population', 'Life Expectancy', 'Unemployment Rate (%)', 'CO2 Emissions (metric tons per capita)', 'Access to Electricity (%)']
    plt.figure(figsize=(10, 6))
    sns.heatmap(df[numeric_columns].corr(), annot=True, cmap="coolwarm")
    st.pyplot(plt)

st.write("Built with **FastAPI** and **Streamlit** 🚀")

