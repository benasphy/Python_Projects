import streamlit as st
from textblob import TextBlob

st.title("Sentiment Analyzer (Manual Text Input)")

st.write("Enter any text (tweet, review, message, etc.) below and analyze its sentiment.")

text = st.text_area("Paste your text here:")

if st.button("Analyze Sentiment"):
    if text.strip():
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        if polarity > 0.1:
            label = "Positive"
        elif polarity < -0.1:
            label = "Negative"
        else:
            label = "Neutral"
        st.markdown(f"**Sentiment:** {label}")
        st.markdown(f"**Polarity:** {polarity:.2f}")
        st.markdown(f"**Subjectivity:** {subjectivity:.2f}")
    else:
        st.warning("Please enter some text to analyze.")
                



