import streamlit as st
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from datetime import datetime, timedelta

# Database Setup
Base = declarative_base()
engine = sa.create_engine('sqlite:///expense_tracker.db')
Session = sessionmaker(bind=engine)

class Expense(Base):
    __tablename__ = 'expenses'
    id = sa.Column(sa.Integer, primary_key=True)
    date = sa.Column(sa.Date)
    category = sa.Column(sa.String)
    amount = sa.Column(sa.Float)
    description = sa.Column(sa.String)

Base.metadata.create_all(engine)

class ExpenseTracker:
    @staticmethod
    def add_expense(date, category, amount, description):
        session = Session()
        expense = Expense(
            date=date, 
            category=category, 
            amount=amount, 
            description=description
        )
        session.add(expense)
        session.commit()
        session.close()

    @staticmethod
    def get_expenses(start_date=None, end_date=None):
        session = Session()
        query = session.query(Expense)
        
        if start_date and end_date:
            query = query.filter(
                Expense.date.between(start_date, end_date)
            )
        
        expenses = query.all()
        session.close()
        
        return pd.DataFrame([
            {
                'Date': e.date, 
                'Category': e.category, 
                'Amount': e.amount, 
                'Description': e.description
            } for e in expenses])

def main():
    st.title("💰 Expense Tracker")
    
    # Sidebar for adding expenses
    st.sidebar.header("Add New Expense")
    expense_date = st.sidebar.date_input("Date", datetime.today())
    categories = [
        "Food", "Transport", "Housing", "Utilities", 
        "Entertainment", "Shopping", "Healthcare", "Other"
    ]
    category = st.sidebar.selectbox("Category", categories)
    amount = st.sidebar.number_input("Amount ($)", min_value=0.0, step=0.01)
    description = st.sidebar.text_input("Description")
    
    if st.sidebar.button("Add Expense"):
        ExpenseTracker.add_expense(expense_date, category, amount, description)
        st.sidebar.success("Expense added successfully!")
    
    # Main area with tabs
    tab1, tab2, tab3 = st.tabs(["Expense List", "Spending Analysis", "Budget Tracking"])
    
    with tab1:
        st.header("Expense History")
        
        # Date range filter
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", datetime.today() - timedelta(days=30))
        with col2:
            end_date = st.date_input("End Date", datetime.today())
        
        # Fetch and display expenses
        expenses_df = ExpenseTracker.get_expenses(start_date, end_date)
        # Normalize column names to Title Case and strip whitespace
        expenses_df.columns = [col.strip().title() for col in expenses_df.columns]
        
        if not expenses_df.empty:
            st.dataframe(expenses_df)
            
            # Total expenses
            total_expenses = expenses_df['Amount'].sum()
            st.metric("Total Expenses", f"${total_expenses:.2f}")
    
    with tab2:
        st.header("Spending Analysis")
        
        if not expenses_df.empty:
            if 'Category' not in expenses_df.columns:
                st.error("No 'Category' column found in your data. Please check your CSV or data source.")
                st.write("Available columns:", expenses_df.columns.tolist())
            else:
                # Category-wise spending
                category_spending = expenses_df.groupby('Category')['Amount'].sum().reset_index()
                # Pie chart of spending by category
                fig1 = px.pie(
                    category_spending, 
                    values='Amount', 
                    names='Category', 
                    title='Spending by Category'
                )
                st.plotly_chart(fig1)
                # Line chart of expenses over time
                expenses_df['Date'] = pd.to_datetime(expenses_df['Date'])
                daily_expenses = expenses_df.groupby(expenses_df['Date'].dt.date)['Amount'].sum().reset_index()
                fig2 = go.Figure(data=go.Scatter(
                    x=daily_expenses['Date'], 
                    y=daily_expenses['Amount'], 
                    mode='lines+markers'
                ))
                fig2.update_layout(title='Daily Expenses', xaxis_title='Date', yaxis_title='Amount')
                st.plotly_chart(fig2)
    
    with tab3:
        st.header("Budget Tracking")
        
        # Budget setting
        budget_categories = {
            "Food": 300,
            "Transport": 200,
            "Housing": 1000,
            "Utilities": 150,
            "Entertainment": 100,
            "Shopping": 200,
            "Healthcare": 100,
            "Other": 150
        }
        
        if 'Category' not in expenses_df.columns:
            st.error("No 'Category' column found in your data. Budget tracking cannot proceed.")
            st.write("Available columns:", expenses_df.columns.tolist())
        else:
            for category, budget in budget_categories.items():
                category_total = expenses_df[expenses_df['Category'] == category]['Amount'].sum()
                remaining = budget - category_total
                st.subheader(f"{category} Budget")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Budget", f"${budget}")
                with col2:
                    st.metric("Spent", f"${category_total:.2f}")
                with col3:
                    st.metric("Remaining", f"${remaining:.2f}", 
                              delta=f"{(category_total/budget)*100:.1f}%" if budget > 0 else "N/A")
                # Progress bar
                st.progress(min(category_total/budget, 1.0))

if __name__ == "__main__":
    main()
