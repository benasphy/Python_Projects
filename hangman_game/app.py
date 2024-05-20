import streamlit as st
import random

class HangmanGame:
    def __init__(self):
        self.words = ['python', 'programming', 'computer', 'game', 'streamlit']
        self.reset_game()

    def reset_game(self):
        self.word = random.choice(self.words)
        self.guessed_letters = set()
        self.attempts_left = 6
        self.game_over = False
        self.win = False

    def display_word(self):
        display = ''
        for letter in self.word:
            if letter in self.guessed_letters:
                display += letter
            else:
                display += '_'
        return display

    def make_guess(self, guess):
        if guess in self.guessed_letters:
            return "You already guessed that letter!"
        
        self.guessed_letters.add(guess)
        
        if guess not in self.word:
            self.attempts_left -= 1
            if self.attempts_left == 0:
                self.game_over = True
                return f"Game Over! The word was {self.word}."
        
        if set(self.word) <= self.guessed_letters:
            self.game_over = True
            self.win = True
            return "Congratulations! You won!"
        
        return "Keep guessing!"

def main():
    st.title("🎲 Hangman Game")
    
    # Initialize game in session state
    if 'game' not in st.session_state:
        st.session_state.game = HangmanGame()
    
    game = st.session_state.game
    
    # Display current word state
    st.write(f"### Word: {game.display_word()}")
    st.write(f"### Attempts Left: {game.attempts_left}")
    
    # Input for letter guess
    guess = st.text_input("Guess a letter:", max_chars=1).lower()
    
    if st.button("Guess"):
        if guess:
            result = game.make_guess(guess)
            st.write(result)
    
    # Game over conditions
    if game.game_over:
        if game.win:
            st.balloons()
            st.success("You Won! 🎉")
        else:
            st.error(f"Game Over! The word was {game.word}. 😢")
        
        if st.button("Play Again"):
            st.session_state.game = HangmanGame()
            st.rerun()

if __name__ == "__main__":
    main()
