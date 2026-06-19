import streamlit as st
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# FastAPI backend URL
FASTAPI_URL = "http://127.0.0.1:8000"

# Streamlit UI Configuration
st.set_page_config(page_title="🌍 CO2 Emission Prediction", layout="wide")

# Sidebar for Navigation
st.sidebar.title("🚀 Navigation Panel")
page = st.sidebar.radio("📌 Choose a Section", ["🏭 Predict Emissions", "📈 CO2 Trends", "⚡ Optimize Regulations", "📊 Data Analysis"])

# Title and Introduction
st.title("🌍 CO2 Emission Prediction & Optimization")
st.markdown("### 🔬 Predict, Analyze, and Optimize CO2 Emissions Based on Economic and Energy Factors.")
st.markdown("---")

# 🎯 Prediction Page
if page == "🏭 Predict Emissions":
    st.header("🔮 Predict CO2 Emissions")
    st.write("🔢 Enter the economic and energy parameters to estimate CO2 emissions.")

    gdp = st.number_input("💰 GDP (USD)", min_value=0.0, format="%.2f")
    energy = st.number_input("⚡ Energy Consumption", min_value=0.0, format="%.2f")
    industry_output = st.number_input("🏭 Industry Output", min_value=0.0, format="%.2f")
    population = st.number_input("👥 Population", min_value=0.0, format="%.2f")
    regulations = st.slider("📜 Regulation Level", 0, 10, 5)

    if st.button("🚀 Predict CO2 Emissions"):
        data = {"gdp": gdp, "energy": energy, "industry_output": industry_output, "population": population, "regulations": regulations}
        response = requests.post(f"{FASTAPI_URL}/predict", json=data)
        if response.status_code == 200:
            st.success(f"🌱 Predicted CO2 Emissions: {response.json()['predicted_CO2_emissions']:.2f} metric tons per capita")
        else:
            st.error("❌ Error: Unable to get prediction.")

# 📈 Trends Page
elif page == "📈 CO2 Trends":
    st.header("📊 CO2 Emission Trends Over the Years")
    st.write("📅 See how CO2 emissions have changed over time.")

    if st.button("📉 Show Trends"):
        response = requests.get(f"{FASTAPI_URL}/trends")
        if response.status_code == 200:
            trends = pd.DataFrame(response.json())
            st.line_chart(trends.set_index("Year"))
        else:
            st.error("❌ Error fetching trends.")

# ⚡ Optimization Page
elif page == "⚡ Optimize Regulations":
    st.header("⚖️ Optimize CO2 Regulations")
    st.write("🛠️ Find the best regulation level for reducing CO2 emissions.")

    if st.button("🔍 Find Best Regulation Level"):
        response = requests.get(f"{FASTAPI_URL}/optimize")
        if response.status_code == 200:
            st.info(f"✅ Recommended Regulation Level: {response.json()['recommended_regulation_level']}")
        else:
            st.error("❌ Error optimizing regulations.")

# 📊 Data Analysis Page
elif page == "📊 Data Analysis":
    st.header("🔎 Exploratory Data Analysis")
    st.write("📌 Analyze correlations between economic and energy factors.")

    if st.button("📊 Show Heatmap"):
        df = pd.read_csv("world_bank_dataset_final.csv")
        numeric_columns = ['GDP (USD)', 'Population', 'Life Expectancy', 'Unemployment Rate (%)', 'CO2 Emissions (metric tons per capita)', 'Access to Electricity (%)']
        
        plt.figure(figsize=(10, 6))
        sns.heatmap(df[numeric_columns].corr(), annot=True, cmap="coolwarm")
        st.pyplot(plt)

st.markdown("---")
st.write("🎯 Built with **FastAPI** & **Streamlit** 🚀")

