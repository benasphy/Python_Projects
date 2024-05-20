import streamlit as st
import random

import streamlit as st

QUESTIONS = [
    {
        "question": "What is the capital of France?",
        "options": ["London", "Berlin", "Paris", "Madrid"],
        "correct": "Paris"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Venus", "Mars", "Jupiter", "Saturn"],
        "correct": "Mars"
    },
    {
        "question": "What is 7 × 8?",
        "options": ["54", "56", "62", "64"],
        "correct": "56"
    }
]

def main():
    st.title("🎲 Fun Quiz Game")

    if "score" not in st.session_state:
        st.session_state.score = 0
    if "current_question" not in st.session_state:
        st.session_state.current_question = 0
    if "answered" not in st.session_state:
        st.session_state.answered = False
    if "last_answer_correct" not in st.session_state:
        st.session_state.last_answer_correct = None

    if st.session_state.current_question < len(QUESTIONS):
        q = QUESTIONS[st.session_state.current_question]
        st.write(f"### Question {st.session_state.current_question + 1}")
        st.write(q["question"])
        user_answer = st.radio("Choose your answer:", q["options"], key=f"radio_{st.session_state.current_question}")

        if st.button("Submit Answer") and not st.session_state.answered:
            st.session_state.answered = True
            if user_answer == q["correct"]:
                st.session_state.score += 1
                st.session_state.last_answer_correct = True
            else:
                st.session_state.last_answer_correct = False
            st.rerun()

        if st.session_state.answered:
            if st.session_state.last_answer_correct:
                st.success("Correct! 🎉")
            else:
                st.error(f"Wrong! The correct answer is {q['correct']}. 😢")
            if st.button("Next Question"):
                st.session_state.current_question += 1
                st.session_state.answered = False
                st.session_state.last_answer_correct = None
                st.rerun()
    else:
        st.title("Quiz Completed!")
        st.write(f"## Your Final Score: {st.session_state.score}/{len(QUESTIONS)}")
        if st.button("Play Again"):
            st.session_state.score = 0
            st.session_state.current_question = 0
            st.session_state.answered = False
            st.session_state.last_answer_correct = None
            st.rerun()

if __name__ == "__main__":
    main()
