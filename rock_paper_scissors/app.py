import streamlit as st
import random

def play_game(user_choice):
    choices = ['Rock', 'Paper', 'Scissors']
    computer_choice = random.choice(choices)
    
    if user_choice == computer_choice:
        return 'Tie', computer_choice
    elif (
        (user_choice == 'Rock' and computer_choice == 'Scissors') or
        (user_choice == 'Paper' and computer_choice == 'Rock') or
        (user_choice == 'Scissors' and computer_choice == 'Paper')
    ):
        return 'Win', computer_choice
    else:
        return 'Lose', computer_choice

def main():
    st.title("🪨 Rock Paper Scissors Game")
    
    # Session state to track score
    if 'score' not in st.session_state:
        st.session_state.score = {'Win': 0, 'Lose': 0, 'Tie': 0}
    
    # Game interface
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### Your Choice")
        user_choice = st.radio("Pick one:", ['Rock', 'Paper', 'Scissors'])
    
    with col2:
        st.write("### Computer's Choice")
        if st.button("Play"):
            result, computer_choice = play_game(user_choice)
            st.write(f"Computer chose: {computer_choice}")
            
            if result == 'Win':
                st.success("You Win! 🎉")
            elif result == 'Lose':
                st.error("You Lose! 😢")
            else:
                st.warning("It's a Tie! 🤝")
            
            # Update score
            st.session_state.score[result] += 1
    
    # Score board
    st.write("## Score Board")
    col3, col4, col5 = st.columns(3)
    
    with col3:
        st.metric("Wins", st.session_state.score['Win'])
    with col4:
        st.metric("Losses", st.session_state.score['Lose'])
    with col5:
        st.metric("Ties", st.session_state.score['Tie'])
    
    # Reset button
    if st.button("Reset Score"):
        st.session_state.score = {'Win': 0, 'Lose': 0, 'Tie': 0}
        st.rerun()

if __name__ == "__main__":
    main()
