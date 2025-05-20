import streamlit as st
import pandas as pd
import os

def main():
    st.title("🌍 World Happiness Visualizer")
    st.write("""
        Explore global happiness data with interactive visualizations.
        Upload a CSV file containing World Happiness data, or use a sample dataset.
    """)

    # Sample data option
    if st.button("Load Sample Data"):
        sample_data = {
            'Country': ['Finland', 'Denmark', 'Switzerland', 'Iceland', 'Netherlands'],
            'Score': [7.8, 7.6, 7.5, 7.5, 7.4],
            'GDP per Capita': [1.34, 1.38, 1.45, 1.38, 1.40],
            'Social Support': [1.59, 1.57, 1.52, 1.56, 1.52],
            'Healthy Life Expectancy': [0.96, 0.97, 1.05, 0.98, 0.99]
        }
        df = pd.DataFrame(sample_data)
        st.session_state['whv_df'] = df

    uploaded_file = st.file_uploader("Upload your World Happiness CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.session_state['whv_df'] = df

    df = st.session_state.get('whv_df', None)
    if df is not None:
        st.subheader("Data Preview")
        st.dataframe(df)

        st.subheader("Happiness Score by Country")
        st.bar_chart(df.set_index('Country')['Score'])

        if 'GDP per Capita' in df.columns:
            st.subheader("GDP per Capita vs. Happiness Score")
            st.scatter_chart(df, x='GDP per Capita', y='Score', color='Country')

        if 'Healthy Life Expectancy' in df.columns:
            st.subheader("Healthy Life Expectancy vs. Happiness Score")
            st.scatter_chart(df, x='Healthy Life Expectancy', y='Score', color='Country')
    else:
        st.info("Please upload a CSV file or load the sample data to begin.")

if __name__ == "__main__":
    main()
