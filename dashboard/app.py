import streamlit as st
import duckdb
import pandas as pd

st.set_page_config(page_title="SkyLogix Weather Dashboard", layout="wide")

st.title("🌦️ SkyLogix Real-Time Weather Dashboard")

# Connect to DuckDB
con = duckdb.connect("../duckdb/weather.duckdb")

query = """
SELECT
    city,
    country,
    temperature,
    humidity,
    weather,
    updatedAt
FROM weather_readings
ORDER BY updatedAt DESC
"""

df = con.execute(query).df()

# KPIs
col1, col2, col3 = st.columns(3)

col1.metric("Cities Monitored", df["city"].nunique())
col2.metric("Avg Temperature (°C)", round(df["temperature"].mean(), 1))
col3.metric("Avg Humidity (%)", round(df["humidity"].mean(), 1))

st.divider()

# Table
st.subheader("Latest Weather Readings")
st.dataframe(df, use_container_width=True)

st.divider()

# Charts
st.subheader("Temperature by City")
st.bar_chart(df.groupby("city")["temperature"].mean())
