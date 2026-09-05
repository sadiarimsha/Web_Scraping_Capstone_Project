import streamlit as st
import sqlite3
import pandas as pd     
import numpy as np     
import plotly.express as px 

try:
    with  sqlite3.connect('db/weather.db') as conn:
        print("Database created and connected successfully.")
        cursor = conn.cursor()

        sql_statement = """
        SELECT * FROM weather_clean
        """

        df = pd.read_sql_query(sql_statement, conn)
        print(df)

except sqlite3.Error as e:
    print(f"An error occurred: {e}")

st.title("Weather Dashboard")
st.write("This dashboard shows weather data scraped from timeanddate.com for a few cities. Use the dropdowns below to compare metrics and explore individual city details.")

# Visualization 1: Grouped Bar Chart for Temperature vs Feels Like

st.header("Feels Like vs. Temperature")
fig_grouped = px.bar( df, x = "Title", y =["Temperature", "Feels Like"], barmode = "group", title= "Actual Temperature vs. Feels Like Temperature by City", labels={"Title": "City", "value": "Temperature (°F)", "variable": "Metric"})
st.plotly_chart(fig_grouped)

# Visualization 2: Bar chart with Temperatures of different cities

st.header("Comparing different weather metrics")
choice = st.selectbox("Pick a metric to compare:", ["Temperature","Feels Like"])
fig = px.bar( df, x="Title", y=choice, color="Description", title = f"{choice} by City", labels={"Title": "City", choice: f"{choice} (°F)"},)
st.plotly_chart(fig)

# Visualization 3:
st.header(" City-wise weather details")
pick_a_city = st.selectbox("Pick a city:", df["Title"])
city_choice = df[df["Title"] == pick_a_city]
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Temperature", f"{city_choice['Temperature'].values[0]}°F")

with col2:
    st.metric("Feels Like", f"{city_choice['Feels Like'].values[0]}°F")

with col3:
    st.write(city_choice['Description'].values[0])

