import streamlit as st
import requests
import pandas as pd
import plotly.graph_objs as go
from pycoingecko import CoinGeckoAPI
import time

class CryptoTracker:
    def __init__(self):
        self.cg = CoinGeckoAPI()
    
    def get_top_cryptocurrencies(self, limit=10):
        """Fetch top cryptocurrencies by market cap"""
        try:
            coins = self.cg.get_coins_markets(
                vs_currency='usd', 
                order='market_cap_desc', 
                per_page=limit, 
                page=1
            )
            return coins
        except Exception as e:
            st.error(f"Error fetching cryptocurrencies: {e}")
            return []
    
    def get_historical_price_data(self, coin_id, days=30):
        """Fetch historical price data for a cryptocurrency"""
        try:
            historical_data = self.cg.get_coin_market_chart_by_id(
                id=coin_id, 
                vs_currency='usd', 
                days=days
            )
            return historical_data['prices']
        except Exception as e:
            st.error(f"Error fetching historical data: {e}")
            return []
    
    def create_price_chart(self, historical_data, coin_name):
        """Create a price chart using Plotly"""
        df = pd.DataFrame(
            historical_data, 
            columns=['Date', 'Price']
        )
        df['Date'] = pd.to_datetime(df['Date'], unit='ms')
        
        fig = go.Figure(data=[go.Scatter(
            x=df['Date'], 
            y=df['Price'], 
            mode='lines', 
            name=f'{coin_name} Price'
        )])
        
        fig.update_layout(
            title=f'{coin_name} Price Over Last {len(df)} Days',
            xaxis_title='Date',
            yaxis_title='Price (USD)'
        )
        
        return fig

def main():
    st.title("🚀 Cryptocurrency Tracker")
    
    # Initialize crypto tracker
    tracker = CryptoTracker()
    
    # Fetch top cryptocurrencies
    top_cryptos = tracker.get_top_cryptocurrencies()
    
    # Sidebar for cryptocurrency selection
    st.sidebar.header("Cryptocurrency Insights")
    
    # Create a selectbox for cryptocurrencies
    crypto_names = [crypto['name'] for crypto in top_cryptos]
    selected_crypto_index = st.sidebar.selectbox(
        "Select a Cryptocurrency", 
        range(len(crypto_names)), 
        format_func=lambda x: crypto_names[x]
    )
    
    # Get selected cryptocurrency details
    selected_crypto = top_cryptos[selected_crypto_index]
    
    # Display cryptocurrency details
    col1, col2 = st.columns(2)
    
    with col1:
        st.image(selected_crypto['image'], width=200)
    
    with col2:
        st.metric("Current Price", f"${selected_crypto['current_price']:,.2f}")
        st.metric("Market Cap", f"${selected_crypto['market_cap']:,.0f}")
        st.metric("24h Change", f"{selected_crypto['price_change_percentage_24h']:.2f}%")
    
    # Tabs for different insights
    tab1, tab2, tab3 = st.tabs([
        "Price History", 
        "Market Performance", 
        "Advanced Metrics"
    ])
    
    with tab1:
        # Historical price chart
        historical_data = tracker.get_historical_price_data(
            selected_crypto['id'], 
            days=30
        )
        
        if historical_data:
            price_chart = tracker.create_price_chart(
                historical_data, 
                selected_crypto['name']
            )
            st.plotly_chart(price_chart)
    
    with tab2:
        # Market performance metrics
        st.subheader("Market Performance")
        
        performance_metrics = {
            "Market Cap Rank": selected_crypto['market_cap_rank'],
            "Total Volume": f"${selected_crypto['total_volume']:,.0f}",
            "Circulating Supply": f"{selected_crypto['circulating_supply']:,.0f}",
            "Total Supply": f"{selected_crypto.get('total_supply', 'N/A'):,.0f}"
        }
        
        for metric, value in performance_metrics.items():
            st.metric(metric, value)
    
    with tab3:
        # Advanced metrics and comparisons
        st.subheader("Advanced Metrics")
        
        # Compare with other top cryptocurrencies
        st.write("Top Cryptocurrencies Comparison")
        
        comparison_df = pd.DataFrame([
            {
                'Name': crypto['name'], 
                'Price': crypto['current_price'], 
                'Market Cap': crypto['market_cap'], 
                '24h Change (%)': crypto['price_change_percentage_24h']
            } for crypto in top_cryptos
        ])
        
        st.dataframe(comparison_df)

if __name__ == "__main__":
    main()
