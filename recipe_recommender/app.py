import streamlit as st
import requests
import random

class RecipeRecommender:
    def __init__(self):
        self.base_url = "https://www.themealdb.com/api/json/v1/1"
        self.categories = [
            "Beef", "Chicken", "Dessert", "Seafood", "Vegetarian"
        ]
        self.dietary_preferences = [
            "Vegetarian", "Vegan", "Gluten Free", "Low Carb"
        ]

    def get_recipes_by_category(self, category):
        """Fetch recipes by category from TheMealDB API"""
        url = f"{self.base_url}/filter.php?c={category}"
        response = requests.get(url)
        return response.json().get('meals', [])

    def get_recipe_details(self, meal_id):
        """Get detailed recipe information"""
        url = f"{self.base_url}/lookup.php?i={meal_id}"
        response = requests.get(url)
        return response.json().get('meals', [None])[0]

    def filter_recipes(self, recipes, dietary_preference=None):
        """Filter recipes based on dietary preferences"""
        if not dietary_preference or dietary_preference == "None":
            return recipes

        filtered_recipes = []
        for recipe in recipes:
            details = self.get_recipe_details(recipe['idMeal'])
            if details:
                # Basic filtering logic (can be expanded)
                if dietary_preference == "Vegetarian" and "Meat" not in details.get('strCategory', ''):
                    filtered_recipes.append(recipe)
                elif dietary_preference == "Vegan" and "Meat" not in details.get('strCategory', '') and "Dairy" not in details.get('strIngredient1', ''):
                    filtered_recipes.append(recipe)
                # Add more sophisticated filtering as needed

        return filtered_recipes

def main():
    st.title("🍽️ Recipe Recommender")
    
    recommender = RecipeRecommender()
    
    # Sidebar for filtering
    st.sidebar.header("Recipe Filters")
    selected_category = st.sidebar.selectbox("Select Cuisine", recommender.categories)
    dietary_preference = st.sidebar.selectbox("Dietary Preference", ["None"] + recommender.dietary_preferences)
    
    # Fetch and filter recipes
    recipes = recommender.get_recipes_by_category(selected_category)
    filtered_recipes = recommender.filter_recipes(recipes, dietary_preference)
    
    # Recommend 3 random recipes
    st.header(f"{selected_category} Recipes")
    
    if filtered_recipes:
        recommended_recipes = random.sample(filtered_recipes, min(3, len(filtered_recipes)))
        
        for recipe in recommended_recipes:
            recipe_details = recommender.get_recipe_details(recipe['idMeal'])
            
            with st.expander(recipe['strMeal']):
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.image(recipe['strMealThumb'], use_column_width=True)
                
                with col2:
                    st.subheader("Recipe Details")
                    st.write(f"**Category:** {recipe_details.get('strCategory', 'N/A')}")
                    st.write(f"**Area:** {recipe_details.get('strArea', 'N/A')}")
                    
                    # Ingredients
                    st.subheader("Ingredients")
                    ingredients = []
                    for i in range(1, 21):
                        ingredient = recipe_details.get(f'strIngredient{i}', '')
                        measure = recipe_details.get(f'strMeasure{i}', '')
                        if ingredient and ingredient.strip():
                            ingredients.append(f"{measure} {ingredient}")
                    
                    st.write("\n".join(ingredients))
                    
                    # Instructions
                    st.subheader("Instructions")
                    st.write(recipe_details.get('strInstructions', 'No instructions available'))
                    
                    # External Link
                    st.markdown(f"[View on TheMealDB]({recipe_details.get('strSource', '#')})")
    else:
        st.warning("No recipes found matching your preferences.")

if __name__ == "__main__":
    main()
