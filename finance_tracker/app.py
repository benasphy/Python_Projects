import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

# SQLAlchemy Setup
Base = declarative_base()
engine = create_engine('sqlite:///finance_tracker.db')
Session = sessionmaker(bind=engine)

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    category = Column(String)
    amount = Column(Float)
    description = Column(String)

Base.metadata.create_all(engine)

def add_transaction(date, category, amount, description):
    session = Session()
    transaction = Transaction(
        date=date, 
        category=category, 
        amount=amount, 
        description=description
    )
    session.add(transaction)
    session.commit()
    session.close()

def get_transactions():
    session = Session()
    transactions = session.query(Transaction).all()
    session.close()
    return pd.DataFrame([
        {
            'Date': t.date, 
            'Category': t.category, 
            'Amount': t.amount, 
            'Description': t.description
        } for t in transactions
    ])

def main():
    st.title("💰 Personal Finance Tracker")
    
    # Sidebar for adding transactions
    st.sidebar.header("Add New Transaction")
    transaction_date = st.sidebar.date_input("Date", datetime.date.today())
    categories = ["Income", "Food", "Transport", "Entertainment", "Bills", "Shopping", "Other"]
    category = st.sidebar.selectbox("Category", categories)
    amount = st.sidebar.number_input("Amount ($)", min_value=0.0, step=0.01)
    description = st.sidebar.text_input("Description")
    
    if st.sidebar.button("Add Transaction"):
        add_transaction(transaction_date, category, amount, description)
        st.sidebar.success("Transaction added successfully!")
    
    # Main area for displaying transactions and insights
    tab1, tab2, tab3 = st.tabs(["Transactions", "Spending Analysis", "Monthly Overview"])
    
    with tab1:
        st.header("Transaction History")
        df = get_transactions()
        if not df.empty:
            st.dataframe(df)
            
            # Total balance calculation
            total_income = df[df['Category'] == 'Income']['Amount'].sum()
            total_expenses = df[df['Category'] != 'Income']['Amount'].sum()
            st.metric("Total Balance", f"${total_income - total_expenses:.2f}")
        else:
            st.write("No transactions yet.")
    
    with tab2:
        st.header("Spending by Category")
        if not df.empty:
            expense_df = df[df['Category'] != 'Income']
            category_spending = expense_df.groupby('Category')['Amount'].sum().reset_index()
            
            # Pie chart of spending
            fig = px.pie(
                category_spending, 
                values='Amount', 
                names='Category', 
                title='Spending Distribution'
            )
            st.plotly_chart(fig)
    
    with tab3:
        st.header("Monthly Spending Trend")
        if not df.empty:
            df['Month'] = pd.to_datetime(df['Date']).dt.to_period('M')
            monthly_spending = df.groupby(['Month', 'Category'])['Amount'].sum().unstack()
            
            # Line chart of monthly trends
            fig = go.Figure()
            for category in monthly_spending.columns:
                if category != 'Income':
                    fig.add_trace(go.Scatter(
                        x=monthly_spending.index.astype(str), 
                        y=monthly_spending[category], 
                        mode='lines+markers', 
                        name=category
                    ))
            fig.update_layout(title='Monthly Spending Trends')
            st.plotly_chart(fig)

if __name__ == "__main__":
    main()
