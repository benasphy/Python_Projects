import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import numpy as np

class CarbonFootprintCalculator:
    def __init__(self):
        # Carbon emission factors (kg CO2 per unit)
        self.emission_factors = {
            'Electricity': {
                'Coal': 0.9,
                'Natural Gas': 0.4,
                'Renewable': 0.05
            },
            'Transportation': {
                'Car (Gasoline)': 0.2,  # per km
                'Car (Electric)': 0.05,  # per km
                'Public Transit': 0.1,   # per km
                'Bicycle/Walking': 0
            },
            'Diet': {
                'Meat-Heavy': 3.3,    # per meal
                'Balanced': 2.0,      # per meal
                'Vegetarian': 1.5,    # per meal
                'Vegan': 1.0          # per meal
            },
            'Waste': {
                'High Waste': 2.5,    # per week
                'Average Waste': 1.5, # per week
                'Low Waste': 0.5      # per week
            }
        }
    
    def calculate_carbon_footprint(self, inputs):
        """Calculate total carbon footprint based on user inputs"""
        total_emissions = 0
        breakdown = {}
        
        # Electricity calculation
        electricity_type = inputs.get('electricity_type', 'Coal')
        electricity_usage = inputs.get('electricity_usage', 0)
        electricity_emissions = electricity_usage * self.emission_factors['Electricity'][electricity_type]
        total_emissions += electricity_emissions
        breakdown['Electricity'] = electricity_emissions
        
        # Transportation calculation
        transport_type = inputs.get('transport_type', 'Car (Gasoline)')
        transport_distance = inputs.get('transport_distance', 0)
        transport_emissions = transport_distance * self.emission_factors['Transportation'][transport_type]
        total_emissions += transport_emissions
        breakdown['Transportation'] = transport_emissions
        
        # Diet calculation
        diet_type = inputs.get('diet_type', 'Meat-Heavy')
        meals_per_week = inputs.get('meals_per_week', 0)
        diet_emissions = meals_per_week * self.emission_factors['Diet'][diet_type]
        total_emissions += diet_emissions
        breakdown['Diet'] = diet_emissions
        
        # Waste calculation
        waste_level = inputs.get('waste_level', 'High Waste')
        waste_emissions = self.emission_factors['Waste'][waste_level]
        total_emissions += waste_emissions
        breakdown['Waste'] = waste_emissions
        
        return total_emissions, breakdown
    
    def get_carbon_reduction_tips(self, emissions):
        """Provide personalized carbon reduction tips"""
        tips = []
        
        if emissions < 10:
            tips.append("Great job! You have a low carbon footprint.")
        
        if emissions > 20:
            tips.append("Your carbon footprint is high. Consider these improvements:")
            tips.append("- Switch to renewable energy sources")
            tips.append("- Use public transit or electric vehicles")
            tips.append("- Reduce meat consumption")
            tips.append("- Minimize waste and recycle")
        
        return tips

def main():
    st.title("🌍 Personal Carbon Footprint Calculator")
    
    # Initialize calculator
    calculator = CarbonFootprintCalculator()
    
    # Input sections
    st.header("Carbon Footprint Assessment")
    
    # Electricity input
    st.subheader("Electricity")
    electricity_type = st.selectbox(
        "Electricity Source", 
        list(calculator.emission_factors['Electricity'].keys())
    )
    electricity_usage = st.number_input(
        "Monthly Electricity Usage (kWh)", 
        min_value=0, 
        value=200
    )
    
    # Transportation input
    st.subheader("Transportation")
    transport_type = st.selectbox(
        "Primary Transportation", 
        list(calculator.emission_factors['Transportation'].keys())
    )
    transport_distance = st.number_input(
        "Daily Travel Distance (km)", 
        min_value=0, 
        value=20
    )
    
    # Diet input
    st.subheader("Diet")
    diet_type = st.selectbox(
        "Diet Type", 
        list(calculator.emission_factors['Diet'].keys())
    )
    meals_per_week = st.number_input(
        "Meals per Week", 
        min_value=0, 
        value=14
    )
    
    # Waste input
    st.subheader("Waste")
    waste_level = st.selectbox(
        "Waste Management Level", 
        list(calculator.emission_factors['Waste'].keys())
    )
    
    # Calculate carbon footprint
    if st.button("Calculate Carbon Footprint"):
        # Prepare inputs
        inputs = {
            'electricity_type': electricity_type,
            'electricity_usage': electricity_usage,
            'transport_type': transport_type,
            'transport_distance': transport_distance,
            'diet_type': diet_type,
            'meals_per_week': meals_per_week,
            'waste_level': waste_level
        }
        
        # Calculate emissions
        total_emissions, breakdown = calculator.calculate_carbon_footprint(inputs)
        
        # Results section
        st.header("Carbon Footprint Results")
        
        # Total emissions
        st.metric("Total Monthly Carbon Emissions", f"{total_emissions:.2f} kg CO2")
        
        # Emissions breakdown visualization
        st.subheader("Emissions Breakdown")
        breakdown_df = pd.DataFrame.from_dict(
            breakdown, 
            orient='index', 
            columns=['Emissions']
        )
        
        # Pie chart of emissions
        fig_pie = px.pie(
            breakdown_df, 
            values='Emissions', 
            names=breakdown_df.index, 
            title='Carbon Emissions by Category'
        )
        st.plotly_chart(fig_pie)
        
        # Bar chart of emissions
        fig_bar = px.bar(
            breakdown_df, 
            title='Carbon Emissions Comparison'
        )
        st.plotly_chart(fig_bar)
        
        # Carbon reduction tips
        st.subheader("Carbon Reduction Tips")
        tips = calculator.get_carbon_reduction_tips(total_emissions)
        for tip in tips:
            st.write(f"- {tip}")

if __name__ == "__main__":
    main()
