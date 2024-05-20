import streamlit as st
import pandas as pd
import plotly.express as px

st.title("IMDB Movie Explorer")

@st.cache_data
def load_movies():
    url = "https://raw.githubusercontent.com/fivethirtyeight/data/master/fandango/fandango_score_comparison.csv"
    df = pd.read_csv(url)
    return df

st.write("Explore and analyze movie ratings from various platforms.")

df = load_movies()

st.sidebar.header("Movie Rating Comparison")
rating_columns = ['RottenTomatoes', 'Metacritic', 'IMDB', 'Fandango']
selected_ratings = st.sidebar.multiselect("Select Rating Platforms", rating_columns, default=['IMDB', 'RottenTomatoes'])

if selected_ratings:
    fig = px.scatter(df, x=selected_ratings[0], y=selected_ratings[1], 
                     hover_data=['FILM'], 
                     title=f"{selected_ratings[0]} vs {selected_ratings[1]} Ratings")
    st.plotly_chart(fig)

st.dataframe(df[['FILM'] + selected_ratings])
