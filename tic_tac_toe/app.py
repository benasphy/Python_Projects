import streamlit as st
import random

class TicTacToe:
    def __init__(self):
        self.board = ['' for _ in range(9)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None

    def make_move(self, position):
        if self.board[position] == '' and not self.game_over:
            self.board[position] = self.current_player
            self.check_winner()
            self.current_player = 'O' if self.current_player == 'X' else 'X'

    def computer_move(self):
        empty_positions = [i for i, spot in enumerate(self.board) if spot == '']
        if empty_positions:
            position = random.choice(empty_positions)
            self.make_move(position)

    def check_winner(self):
        # Winning combinations
        win_combos = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]

        for combo in win_combos:
            if (self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]]) and self.board[combo[0]] != '':
                self.game_over = True
                self.winner = self.board[combo[0]]
                return

        if '' not in self.board:
            self.game_over = True

def main():
    st.title("🎲 Tic Tac Toe")
    
    # Initialize game in session state
    if 'tic_tac_toe' not in st.session_state:
        st.session_state.tic_tac_toe = TicTacToe()
    
    game = st.session_state.tic_tac_toe
    
    # Display board
    board_display = [':white_large_square:' if spot == '' else spot for spot in game.board]
    
    # Create board layout
    cols = st.columns(3)
    for i in range(3):
        for j in range(3):
            with cols[j]:
                if st.button(board_display[i*3 + j], key=f'btn_{i*3 + j}'):
                    if game.board[i*3 + j] == '':
                        game.make_move(i*3 + j)
                        if not game.game_over:
                            game.computer_move()
    
    # Game status
    if game.game_over:
        if game.winner:
            st.success(f"Player {game.winner} wins! 🎉")
        else:
            st.warning("It's a draw! 🤝")
        
        if st.button("Play Again"):
            st.session_state.game = TicTacToe()
            st.rerun()

if __name__ == "__main__":
    main()
