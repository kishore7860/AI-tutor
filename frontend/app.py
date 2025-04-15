import streamlit as st
import requests

# Page Config
st.set_page_config(page_title="AI Tutor", layout="wide")
st.title("🧠 AI Tutoring Assistant")

# 🌈 Custom CSS
def load_custom_css():
    st.markdown("""
        <style>
        html, body, [class*="css"] {
            font-family: 'Segoe UI', sans-serif;
            background-color: #f4f6f8;
        }

        .stApp {
            padding-top: 2rem;
        }

        .stTextArea textarea {
            background-color: #fff !important;
            color: #333 !important;
            border-radius: 8px;
            border: 1.5px solid #ced6e0;
            padding: 1rem;
            font-size: 16px;
        }

        .stSelectbox div[data-baseweb="select"] {
            background-color: #fff;
            border-radius: 5px;
            padding: 4px;
        }

        .stButton>button {
            background-color: #0984e3;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 0.6em 1.2em;
            font-weight: bold;
            font-size: 16px;
        }

        .stButton>button:hover {
            background-color: #74b9ff;
            color: #000;
        }

        h1, h2, h3 {
            color: #2d3436;
        }

        .quiz-box {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 0 8px rgba(0,0,0,0.05);
        }

        .sidebar .sidebar-content {
            background-color: #dfe6e9;
        }

        .custom-footer {
            text-align: center;
            margin-top: 2rem;
            color: #636e72;
            font-size: 15px;
        }
        </style>
    """, unsafe_allow_html=True)

load_custom_css()

# Sidebar 🎛️
with st.sidebar:
    st.header("🎯 Learning Preferences")
    subject = st.selectbox("Subject", ["Math", "Science", "History", "English", "Geography", "Computer Science"])
    level = st.selectbox("Level", ["Beginner", "Intermediate", "Advanced"])
    learning_style = st.selectbox("Learning Style", ["Visual", "Text-Based", "Hands-On"])
    language = st.selectbox("Language", ["English", "French", "Spanish", "German", "Chinese"])
    background = st.selectbox("Background Knowledge", ["Beginner", "Intermediate", "Advanced"])
    st.markdown("""
    <hr>
    <h4>ℹ️ How it Works</h4>
    <ul>
        <li>Select your topic</li>
        <li>Ask a question or take a quiz</li>
        <li>Learn interactively!</li>
    </ul>
    """, unsafe_allow_html=True)

API_ENDPOINT = "http://127.0.0.1:8000"

tab1, tab2 = st.tabs(["💬 Ask a Question", "📝 Take a Quiz"])

# 👉 Ask a Question
with tab1:
    st.subheader("Ask the Tutor")
    question = st.text_area("📖 What would you like to learn?", "Explain Newton's Second law in simple terms.")

    if st.button("🚀 Get Answer"):
        with st.spinner("Getting answer..."):
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

                if "response" in response:
                    st.success("✅ Here’s your explanation:")
                    st.markdown(response["response"], unsafe_allow_html=True)
                else:
                    st.error("⚠️ Response format issue. Debug below.")
                    st.json(response)

            except Exception as e:
                st.error(f"❌ Error occurred: {e}")

# 🧪 Take a Quiz
with tab2:
    st.subheader("Your Personalized Quiz")
    num_questions = st.slider("Number of Questions", 1, 10, 5)

    if "quiz_data" not in st.session_state:
        st.session_state.quiz_data = []
        st.session_state.user_answers = {}
        st.session_state.submitted = False

    if st.button("🎲 Generate Quiz"):
        with st.spinner("Creating your quiz..."):
            try:
                response = requests.post(
                    f"{API_ENDPOINT}/quiz",
                    json={
                        "subject": subject,
                        "level": level,
                        "num_questions": num_questions,
                        "reveal_answer": False
                    }
                ).json()
                if 'quiz' in response:
                    st.session_state.quiz_data = response["quiz"]
                    st.session_state.user_answers = {}
                    st.session_state.submitted = False
                    st.success("✅ Quiz Ready! Please submit after answering.")
                else:
                    st.error("⚠️ Quiz format error.")
                    st.json(response)
            except Exception as e:
                st.error(f"❌ Error: {e}")

    if st.session_state.quiz_data:
        st.markdown('<div class="quiz-box">', unsafe_allow_html=True)
        for i, q in enumerate(st.session_state.quiz_data):
            st.markdown(f"**Q{i+1}: {q['question']}**")
            st.session_state.user_answers[f"q{i}"] = st.radio(
                "Choose one:",
                q["options"],
                key=f"answer_q{i}"
            )
            st.markdown("---")

        if st.button("📩 Submit Quiz"):
            st.session_state.submitted = True

        if st.session_state.submitted:
            st.subheader("Results 📊")
            correct = 0
            for i, q in enumerate(st.session_state.quiz_data):
                user_ans = st.session_state.user_answers.get(f"q{i}")
                if user_ans == q["correct_answer"]:
                    st.success(f"Q{i+1}: Correct!")
                    correct += 1
                else:
                    st.error(f"Q{i+1}: Incorrect. Correct Answer: {q['correct_answer']}")
                    st.caption(f"Explanation: {q.get('explanation', 'No explanation')}")

            st.markdown(f"### 🏁 Score: **{correct} / {len(st.session_state.quiz_data)}**")
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown('<div class="custom-footer">Made with ❤️ by <b>Kishore Reddy</b> | <a href="https://github.com/kishore7860/AI-tutor" target="_blank">GitHub</a></div>', unsafe_allow_html=True)