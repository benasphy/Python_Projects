import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Global Earthquake Dashboard")

@st.cache_data
def load_earthquakes():
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv"
    df = pd.read_csv(url)
    return df

st.write("Visualize and analyze recent global earthquake data.")

df = load_earthquakes()

st.sidebar.header("Earthquake Filters")
magnitude_range = st.sidebar.slider("Magnitude Range", 0.0, 10.0, (4.0, 8.0))

filtered_df = df[(df['mag'] >= magnitude_range[0]) & (df['mag'] <= magnitude_range[1])]

st.subheader(f"Earthquakes between {magnitude_range[0]} and {magnitude_range[1]} magnitude")
fig = px.scatter_geo(filtered_df, 
                     lat='latitude', 
                     lon='longitude', 
                     color='mag',
                     size='mag',
                     hover_name='place',
                     title='Global Earthquake Locations')
st.plotly_chart(fig)

st.dataframe(filtered_df[['time', 'place', 'mag', 'depth']])
