import streamlit as st
from textblob import TextBlob
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Initialize session state
if 'sentiment_history' not in st.session_state:
    st.session_state.sentiment_history = []

def analyze_sentiment(text):
    """Analyze text sentiment and return detailed analysis"""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    
    # Determine sentiment category
    if polarity > 0.1:
        sentiment = "Positive"
        color = "green"
    elif polarity < -0.1:
        sentiment = "Negative"
        color = "red"
    else:
        sentiment = "Neutral"
        color = "blue"
    
    # Get word-by-word analysis
    word_analysis = []
    for word in blob.words:
        word_blob = TextBlob(word)
        word_polarity = word_blob.sentiment.polarity
        word_subjectivity = word_blob.sentiment.subjectivity
        word_analysis.append({
            'word': word,
            'polarity': word_polarity,
            'subjectivity': word_subjectivity
        })
    
    return {
        'sentiment': sentiment,
        'polarity': polarity,
        'subjectivity': subjectivity,
        'color': color,
        'word_analysis': word_analysis
    }

def plot_sentiment_history():
    """Plot sentiment history if available"""
    if st.session_state.sentiment_history:
        df = pd.DataFrame(st.session_state.sentiment_history)
        
        # Plot polarity over time
        st.header("Sentiment History")
        fig, ax = plt.subplots(figsize=(10, 4))
        sns.lineplot(x=range(len(df)), y='polarity', data=df, ax=ax)
        ax.set_xlabel('Analysis Number')
        ax.set_ylabel('Polarity')
        ax.set_title('Sentiment Polarity Over Time')
        st.pyplot(fig)

def main():
    st.title("📊 Sentiment Analyzer")
    st.write("""
        Analyze the sentiment of any text using TextBlob. 
        This tool helps you understand the emotional tone behind words.
    """)

    # Text input section
    st.header("Enter Text to Analyze")
    text_input = st.text_area("Type or paste text here:", height=150)

    if st.button("Analyze Sentiment") and text_input:
        # Analyze sentiment
        result = analyze_sentiment(text_input)
        
        # Store in history
        st.session_state.sentiment_history.append({
            'polarity': result['polarity'],
            'subjectivity': result['subjectivity'],
            'text': text_input[:50] + '...' if len(text_input) > 50 else text_input,
            'timestamp': pd.Timestamp.now()
        })
        
        # Display results
        st.header("Sentiment Analysis Results")
        
        # Display sentiment with color
        st.markdown(f"<h3 style='color:{result['color']}'>Sentiment: {result['sentiment']}</h3>", unsafe_allow_html=True)
        
        # Display polarity and subjectivity
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Polarity", f"{result['polarity']:.2f}")
            st.write("""
                -1.00 to -0.10: Strongly Negative
                -0.10 to -0.05: Slightly Negative
                -0.05 to 0.05: Neutral
                0.05 to 0.10: Slightly Positive
                0.10 to 1.00: Strongly Positive
            """)
        with col2:
            st.metric("Subjectivity", f"{result['subjectivity']:.2f}")
            st.write("""
                0.00 to 0.33: Objective
                0.33 to 0.66: Somewhat Subjective
                0.66 to 1.00: Highly Subjective
            """)

        # Display word-by-word analysis
        st.header("Word-by-Word Analysis")
        word_df = pd.DataFrame(result['word_analysis'])
        st.dataframe(word_df)
        
        # Plot word polarities
        fig, ax = plt.subplots(figsize=(10, 4))
        sns.barplot(x='word', y='polarity', data=word_df, ax=ax)
        ax.set_title('Word Polarity Distribution')
        plt.xticks(rotation=45)
        st.pyplot(fig)

    # Display sentiment history
    plot_sentiment_history()

if __name__ == "__main__":
    main()
