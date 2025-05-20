import streamlit as st
import importlib.util
import os
from pathlib import Path

# Define project categories
CATEGORIES = {
    "Financial Tools": [
        "expense_tracker",
        "finance_tracker"
    ],
    "Games": [
        "tic_tac_toe",
        "rock_paper_scissors",
        "hangman_game"
    ],
    "Data Analysis": [
        "stock_market_simulator",
        "world_happiness_visualizer"
    ],
    "Utilities": [
        "password_generator",
        "url_shortener",
        "task_manager"
    ],
    "AI & NLP": [
        "sentiment_analyzer",
        "translation_app"
    ]
}

def load_project(project_name):
    """Load and run the selected project"""
    import sys
    try:
        # Remove 'app' from sys.modules to avoid caching issues
        if 'app' in sys.modules:
            del sys.modules['app']
        # Import the project module
        module_path = os.path.join(os.getcwd(), project_name, "app.py")
        spec = importlib.util.spec_from_file_location("app", module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # For hangman game, we need to create an instance
        if project_name == "hangman_game":
            game = module.HangmanGame()
            module.main()
        else:
            # Run the project's main function
            if hasattr(module, "main"):
                module.main()
            elif hasattr(module, "run"):
                module.run()
            else:
                st.error(f"Project {project_name} doesn't have a main/run function")
    except Exception as e:
        st.error(f"Error loading {project_name}: {str(e)}")
        st.error(f"Error details: {str(e)}")
        st.error(f"Project path: {module_path}")

def get_project_description(project):
    """Get a description for each project"""
    descriptions = {
        "expense_tracker": "Track and manage your daily expenses with ease.",
        "finance_tracker": "Monitor your investments and financial goals.",
        "tic_tac_toe": "Play the classic Tic Tac Toe game.",
        "rock_paper_scissors": "Challenge the computer in Rock Paper Scissors.",
        "hangman_game": "Guess words in this fun word guessing game.",
        "stock_market_simulator": "Simulate stock market investments and trading strategies.",
        "world_happiness_visualizer": "Explore global happiness data with interactive visualizations.",
        "password_generator": "Generate secure passwords with customizable options.",
        "url_shortener": "Create and manage shortened URLs.",
        "task_manager": "Organize and track your tasks efficiently.",
        "sentiment_analyzer": "Analyze text sentiment with machine learning.",
        "translation_app": "Translate text between multiple languages."
    }
    return descriptions.get(project, "No description available")

def main():
    st.set_page_config(
        page_title="Python Projects Dashboard",
        page_icon="💻",
        layout="wide"
    )
    
    st.title("💻 Python Projects Dashboard")
    
    # Create sidebar with categories
    st.sidebar.title("Projects")
    category = st.sidebar.selectbox(
        "Select a category:",
        list(CATEGORIES.keys())
    )
    
    # Get projects in selected category
    projects = CATEGORIES[category]
    
    # Create radio buttons for projects
    project = st.sidebar.radio(
        "Select a project:",
        projects
    )
    
    # Display project description
    st.sidebar.markdown(f"""
    ### {project.replace('_', ' ').title()}
    {get_project_description(project)}
    """)
    
    # Load and display selected project
    if project:
        load_project(project)

if __name__ == "__main__":
    main()
