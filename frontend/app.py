import streamlit as st
import requests
import uuid 
import random
from streamlit.components.v1 import html
# Page configuration
st.set_page_config(page_title="AI Tutor",layout="wide")
st.title("AI Tutor & Quiz app")
with st.sidebar:
    st.header("Learning preferences")
    subject = st.selectbox("Subject", ["Math", "Science", "History", "English", "Geography", "Computer Science"])
    level = st.selectbox("Level", ["Beginner", "Intermediate", "Advanced"])
    learning_style = st.selectbox("Learning Style", ["Visual", "Text-Based", "Hands-On"])
    language = st.selectbox("Language", ["English", "French", "Spanish", "German", "Chinese"])
    background = st.selectbox("Background Knowledge", ["Begginer", "Intermediate", "Advanced"])
     
API_ENDPOINT = "http://127.0.0.1:8000"

tab1, tab2 = st.tabs(["Ask a Question", "Take a Quiz"])

with tab1:
    st.header("Ask a Question")
    question = st.text_area("what do you want to learn today?", "Explain Newtons Second law in simple terms.")
    if st.button("Get Answer"):
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
    col1, col2 = st.columns([2,1])
    with col1:
        num_questions = st.slider("Number of Questions", min_value=1, max_value=10, value=5)
    with col2:
        quiz_button = st.button("Generate Quiz", use_container_width=True)
    if quiz_button:
        with st.spinner("Generating quiz..."):
            try:
                response = requests.post(
                    f"{API_ENDPOINT}/quiz",
                    json={
                        "subject": subject,
                        "level": level,
                        "num_questions": num_questions,
                        "reveal_answer": True
                    }).json()
                st.success("Here's your quiz:")
                if 'formatted_quiz' in response and response["formatted_quiz"]:
                    html(response["formatted_quiz"],height=num_questions*300)
                else:
                    quiz_items = response.get("quiz") or response.get("quiz_data")
                    if not quiz_items:
                        st.error("Quiz data not found in API response.")
                    else:
                        for i, q in enumerate(response["quiz_data"]):
                            with st.expander(f"Question {i+1}: {q[question]}", expanded=True):
                                session_id = str(uuid.uuid4())
                                selected =  st.radio(
                                    "Select an option",
                                    q["options"],
                                    key=f"q_{session_id}"
                                )
                                if st.button("Submit", key=f"submit_{session_id}"):
                                    if selected == q["correct_answer"]:
                                        st.success(f"Correct! {q.get('explanation','')}")
                                    else:
                                        st.error("Incorrect!")
                                        st.write(f"Correct answer: {q['correct_answer']}")
                                        if "explanation" in q:
                                            st.info(f"Explanation: {q['explanation']}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error: {e}")
                st.info("Please check your internet connection and try again.")