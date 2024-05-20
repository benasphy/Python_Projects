import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
import random

class StockMarketSimulator:
    def __init__(self, initial_balance=10000):
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.portfolio = {}
        self.transaction_history = []

    def get_stock_data(self, ticker, period='1mo'):
        """Fetch stock data from Yahoo Finance"""
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(period=period)
            return data
        except Exception as e:
            st.error(f"Error fetching stock data: {e}")
            return None

    def buy_stock(self, ticker, amount):
        """Simulate buying stocks"""
        stock_data = self.get_stock_data(ticker)
        if stock_data is not None and not stock_data.empty:
            current_price = stock_data['Close'].iloc[-1]
            shares = amount / current_price
            
            if amount <= self.balance:
                self.balance -= amount
                self.portfolio[ticker] = self.portfolio.get(ticker, 0) + shares
                
                # Record transaction
                self.transaction_history.append({
                    'type': 'Buy',
                    'ticker': ticker,
                    'shares': shares,
                    'price': current_price,
                    'total_cost': amount
                })
                
                return True
            else:
                st.warning("Insufficient balance")
                return False

    def sell_stock(self, ticker, shares):
        """Simulate selling stocks"""
        stock_data = self.get_stock_data(ticker)
        if stock_data is not None and not stock_data.empty:
            current_price = stock_data['Close'].iloc[-1]
            
            if ticker in self.portfolio and self.portfolio[ticker] >= shares:
                sale_amount = shares * current_price
                self.balance += sale_amount
                self.portfolio[ticker] -= shares
                
                # Remove ticker if no shares left
                if self.portfolio[ticker] == 0:
                    del self.portfolio[ticker]
                
                # Record transaction
                self.transaction_history.append({
                    'type': 'Sell',
                    'ticker': ticker,
                    'shares': shares,
                    'price': current_price,
                    'total_sale': sale_amount
                })
                
                return True
            else:
                st.warning("Insufficient shares")
                return False

    def calculate_portfolio_value(self):
        """Calculate current portfolio value"""
        total_value = self.balance
        for ticker, shares in self.portfolio.items():
            stock_data = self.get_stock_data(ticker)
            if stock_data is not None and not stock_data.empty:
                current_price = stock_data['Close'].iloc[-1]
                total_value += shares * current_price
        return total_value

def main():
    st.title("📈 Stock Market Simulator")
    
    # Initialize simulator
    if 'simulator' not in st.session_state:
        st.session_state.simulator = StockMarketSimulator()
    
    simulator = st.session_state.simulator
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["Trading", "Portfolio", "Performance"])
    
    with tab1:
        st.header("Stock Trading")
        
        # Stock selection
        ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, GOOGL)", value="AAPL")
        
        # Fetch and display stock data
        stock_data = simulator.get_stock_data(ticker)
        
        if stock_data is not None and not stock_data.empty:
            # Stock price chart
            fig = go.Figure(data=[go.Candlestick(
                x=stock_data.index,
                open=stock_data['Open'],
                high=stock_data['High'],
                low=stock_data['Low'],
                close=stock_data['Close']
            )])
            fig.update_layout(title=f'{ticker} Stock Price')
            st.plotly_chart(fig)
            
            # Current price
            current_price = stock_data['Close'].iloc[-1]
            st.write(f"Current Price: ${current_price:.2f}")
            
            # Trading actions
            col1, col2 = st.columns(2)
            
            with col1:
                buy_amount = st.number_input("Buy Amount ($)", min_value=0.0, step=10.0)
                if st.button("Buy"):
                    if simulator.buy_stock(ticker, buy_amount):
                        st.success(f"Bought ${buy_amount} of {ticker}")
            
            with col2:
                sell_shares = st.number_input("Sell Shares", min_value=0.0, step=0.1)
                if st.button("Sell"):
                    if simulator.sell_stock(ticker, sell_shares):
                        st.success(f"Sold {sell_shares} shares of {ticker}")
    
    with tab2:
        st.header("Portfolio")
        
        # Current balance
        st.metric("Cash Balance", f"${simulator.balance:.2f}")
        
        # Portfolio holdings
        st.subheader("Current Holdings")
        for ticker, shares in simulator.portfolio.items():
            stock_data = simulator.get_stock_data(ticker)
            if stock_data is not None and not stock_data.empty:
                current_price = stock_data['Close'].iloc[-1]
                total_value = shares * current_price
                
                st.write(f"{ticker}: {shares:.2f} shares (${total_value:.2f})")
        
        # Total portfolio value
        portfolio_value = simulator.calculate_portfolio_value()
        st.metric("Total Portfolio Value", f"${portfolio_value:.2f}")
        st.metric("Total Gain/Loss", f"${portfolio_value - simulator.initial_balance:.2f}")
    
    with tab3:
        st.header("Transaction History")
        
        # Display transaction history
        transaction_df = pd.DataFrame(simulator.transaction_history)
        if not transaction_df.empty:
            st.dataframe(transaction_df)
        else:
            st.write("No transactions yet")

if __name__ == "__main__":
    main()
