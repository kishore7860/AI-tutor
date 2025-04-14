import streamlit as st
import requests
import uuid 
import random
from streamlit.components.v1 import html
# Page configuration
st.set_page_config(page_title="AI Tutor",layout="wide")
st.title("👨‍🏫 AI Tutoring Assistant")
def load_custom_css():
    st.markdown("""
        <style>
        /* Set base styles for the app */
        .main {
            background-color: #f9f9f9;
            font-family: 'Segoe UI', sans-serif;
        }

        /* Style buttons */
        .stButton > button {
            background-color: #00b894;
            color: white;
            border-radius: 8px;
            padding: 0.5em 1em;
            font-size: 16px;
            font-weight: bold;
            transition: 0.3s;
        }

        .stButton > button:hover {
            background-color: #019875;
            cursor: pointer;
        }

        /* Text input and text area styling */
        .stTextInput input, .stTextArea textarea {
            border: 2px solid #00cec9;
            border-radius: 5px;
            padding: 0.3em;
        }

        /* Header colors */
        h1, h2, h3 {
            color: #0984e3;
        }

        /* Tabs spacing */
        .stTabs {
            margin-top: 1em;
        }
        </style>
    """, unsafe_allow_html=True)

load_custom_css()
with st.sidebar:
    st.header("Learning preferences")
    subject = st.selectbox("Subject", ["Math", "Science", "History", "English", "Geography", "Computer Science"])
    level = st.selectbox("Level", ["Beginner", "Intermediate", "Advanced"])
    learning_style = st.selectbox("Learning Style", ["Visual", "Text-Based", "Hands-On"])
    language = st.selectbox("Language", ["English", "French", "Spanish", "German", "Chinese"])
    background = st.selectbox("Background Knowledge", ["Beginner", "Intermediate", "Advanced"])
st.sidebar.markdown("""
###  How it Works
- Select a subject and level
- Ask a question or take a quiz
- Learn step-by-step with instant feedback
""")
API_ENDPOINT = "http://127.0.0.1:8000"

tab1, tab2 = st.tabs(["Ask a Question", "Take a Quiz"])
with tab1:
    st.header("Ask a Question")
    question = st.text_area("what do you want to learn today?", "Explain Newtons Second law in simple terms.")
    if st.button("💡 Get Answer"):
        with st.spinner("Generating answer..."):
            try:
                response = requests.post(
                    f"{API_ENDPOINT}/tutor",
                    json={
                        "subject": subject,
                        "level": level,
                        "learning_style": learning_style,
                        "background": background,
                        "language": language,
                        "question": question
                    }).json()
                st.success("Here's your explaination:")
                if "response" in response:
                    st.markdown(response["response"], unsafe_allow_html=True)
                else:
                    st.error("The key 'response' was not found in the API response.")
                    st.write("Full API response:", response)
            except requests.exceptions.RequestException as e:
                st.error(f"Error: {e}")
                st.info("Please check your internet connection and try again.")
with tab2:
    st.header("Take a Quiz")

    num_questions = st.slider("Number of Questions", min_value=1, max_value=10, value=5)

    if "quiz_data" not in st.session_state:
        st.session_state.quiz_data = []
        st.session_state.user_answers = {}
        st.session_state.submitted = False

    if st.button("Generate Quiz"):
        with st.spinner("Generating quiz..."):
            try:
                response = requests.post(
                    f"{API_ENDPOINT}/quiz",
                    json={
                        "subject": subject,
                        "level": level,
                        "num_questions": num_questions,
                        "reveal_answer": False  # ⛔ No answer reveal upfront
                    }
                ).json()

                if 'quiz' in response:
                    st.session_state.quiz_data = response["quiz"]
                    st.session_state.user_answers = {}
                    st.session_state.submitted = False
                    st.success("Quiz is ready! Select your answers and click 'Submit Quiz'.")
                else:
                    st.error("Quiz data not found in API response.")
                    st.write("Full response:", response)
            except Exception as e:
                st.error(f"Error generating quiz: {e}")

    if st.session_state.quiz_data:
        st.subheader("Your Quiz")

        for i, q in enumerate(st.session_state.quiz_data):
            st.markdown(f"**Q{i+1}. {q['question']}**")
            st.session_state.user_answers[f"q{i}"] = st.radio(
                label="Choose one:",
                options=q["options"],
                key=f"answer_q{i}",
                index=0
            )
            st.markdown("---")
        st.markdown("""
            <div style="background-color:#dfe6e9; padding: 10px; border-radius: 10px;">
            <b>Quiz Instructions:</b> Select the correct option and click submit!                </div>
        """, unsafe_allow_html=True)

        if st.button("Submit Quiz"):
            st.session_state.submitted = True

        if st.session_state.submitted:
            st.subheader("Quiz Results 📝")
            correct = 0
            for i, q in enumerate(st.session_state.quiz_data):
                user_ans = st.session_state.user_answers.get(f"q{i}")
                correct_ans = q["correct_answer"]
                explanation = q.get("explanation", "")

                if user_ans == correct_ans:
                    st.success(f"✅ Q{i+1}: Correct!")
                    correct += 1
                else:
                    st.error(f"❌ Q{i+1}: Incorrect.")
                    st.info(f"Correct Answer: **{correct_ans}**")
                    if explanation:
                        st.caption(f"Explanation: {explanation}")

            st.markdown(f"### 🎯 Your Score: **{correct} / {len(st.session_state.quiz_data)}**")
st.markdown("---")
st.markdown("Made with ❤️ by Kishore Reddy | [GitHub](https://github.com/kishore7860/AI-tutor)", unsafe_allow_html=True)