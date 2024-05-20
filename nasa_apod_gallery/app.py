import streamlit as st
import requests

st.title("NASA Astronomy Picture of the Day Gallery")

st.write("Browse NASA's Astronomy Picture of the Day (APOD) using the public API.")

API_URL = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&count=5"

if st.button("Show Random Pictures"):
    response = requests.get(API_URL)
    data = response.json()
    for item in data:
        st.subheader(item['title'])
        st.image(item['url'])
        st.write(item.get('explanation', ''))
