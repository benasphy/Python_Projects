import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from sqlalchemy import create_engine, Column, Integer, Float, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

# SQLAlchemy setup
Base = declarative_base()
engine = create_engine('sqlite:///health_tracker.db')
Session = sessionmaker(bind=engine)

class HealthEntry(Base):
    """SQLAlchemy model for health tracking"""
    __tablename__ = 'health_entries'
    
    id = Column(Integer, primary_key=True)
    date = Column(Date, default=datetime.now().date)
    weight = Column(Float)
    calories = Column(Integer)
    steps = Column(Integer)
    workout_type = Column(String)
    workout_duration = Column(Integer)

# Create tables
Base.metadata.create_all(engine)

class HealthFitnessTracker:
    def __init__(self):
        self.session = Session()
    
    def add_health_entry(self, weight, calories, steps, workout_type, workout_duration):
        """Add a new health and fitness entry"""
        entry = HealthEntry(
            date=datetime.now().date(),
            weight=weight,
            calories=calories,
            steps=steps,
            workout_type=workout_type,
            workout_duration=workout_duration
        )
        self.session.add(entry)
        self.session.commit()
    
    def get_health_entries(self, days=30):
        """Retrieve health entries for the last specified number of days"""
        start_date = datetime.now().date() - timedelta(days=days)
        entries = self.session.query(HealthEntry).filter(
            HealthEntry.date >= start_date
        ).order_by(HealthEntry.date).all()
        
        return entries
    
    def analyze_health_data(self, entries):
        """Analyze health and fitness data"""
        if not entries:
            return None
        
        # Convert entries to DataFrame
        data = [{
            'Date': entry.date,
            'Weight': entry.weight,
            'Calories': entry.calories,
            'Steps': entry.steps,
            'Workout Type': entry.workout_type,
            'Workout Duration': entry.workout_duration
        } for entry in entries]
        
        df = pd.DataFrame(data)
        return df

def main():
    st.title("🏋️ Personal Health & Fitness Tracker")
    
    # Initialize tracker
    tracker = HealthFitnessTracker()
    
    # Tabs for different functionalities
    tab1, tab2, tab3 = st.tabs([
        "Log Health Data", 
        "Health Insights", 
        "Progress Tracking"
    ])
    
    with tab1:
        st.header("Daily Health Log")
        
        # Input columns
        col1, col2 = st.columns(2)
        
        with col1:
            weight = st.number_input("Weight (kg)", min_value=0.0, step=0.1)
            calories = st.number_input("Calories Consumed", min_value=0)
        
        with col2:
            steps = st.number_input("Daily Steps", min_value=0)
            workout_type = st.selectbox(
                "Workout Type", 
                ["Cardio", "Strength Training", "Yoga", "Running", "Other"]
            )
        
        workout_duration = st.number_input("Workout Duration (minutes)", min_value=0)
        
        # Log health data
        if st.button("Log Health Data"):
            tracker.add_health_entry(
                weight, calories, steps, 
                workout_type, workout_duration
            )
            st.success("Health data logged successfully!")
    
    with tab2:
        st.header("Health Insights")
        
        # Retrieve health entries
        entries = tracker.get_health_entries()
        
        if entries:
            # Analyze health data
            health_df = tracker.analyze_health_data(entries)
            
            # Weight tracking
            st.subheader("Weight Tracking")
            fig_weight = px.line(
                health_df, 
                x='Date', 
                y='Weight', 
                title='Weight Progress'
            )
            st.plotly_chart(fig_weight)
            
            # Workout analysis
            st.subheader("Workout Analysis")
            workout_counts = health_df['Workout Type'].value_counts()
            fig_workout = px.pie(
                values=workout_counts.values, 
                names=workout_counts.index, 
                title='Workout Type Distribution'
            )
            st.plotly_chart(fig_workout)
            
            # Daily steps
            st.subheader("Daily Steps")
            fig_steps = px.bar(
                health_df, 
                x='Date', 
                y='Steps', 
                title='Daily Step Count'
            )
            st.plotly_chart(fig_steps)
        else:
            st.warning("No health data available. Start logging your health data!")
    
    with tab3:
        st.header("Progress Tracking")
        
        # Retrieve health entries
        entries = tracker.get_health_entries(days=90)
        
        if entries:
            health_df = tracker.analyze_health_data(entries)
            
            # Goal setting and tracking
            st.subheader("Health Goals")
            
            # Weight goal
            current_weight = health_df['Weight'].iloc[-1]
            goal_weight = st.number_input(
                "Goal Weight (kg)", 
                min_value=0.0, 
                value=current_weight
            )
            
            # Progress calculation
            weight_progress = (current_weight - goal_weight) / (current_weight + 0.001) * 100
            
            # Progress bar
            st.metric("Weight Progress", f"{abs(weight_progress):.2f}%")
            st.progress(abs(weight_progress) / 100)
            
            # Recommendations
            st.subheader("Personalized Recommendations")
            if weight_progress > 0:
                st.write("🔥 You're making great progress towards your weight goal!")
            else:
                st.write("💪 Keep working towards your fitness goals!")
        else:
            st.warning("Not enough data for progress tracking.")

if __name__ == "__main__":
    main()
