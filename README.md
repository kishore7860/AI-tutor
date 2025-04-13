# 🧠 AI Tutor & Quiz Generator

An intelligent tutoring system built with **FastAPI** (backend) and **Streamlit** (frontend), powered by **OpenAI via LangChain**. This app allows users to:
- Ask academic questions and receive AI-generated answers
- Generate quizzes with explanations based on a selected subject, level, and learning style

---

## 🛠️ Project Structure

. ├── backend/ │ ├── main.py # FastAPI server │ └── engine.py # LLM logic for tutoring and quiz ├── frontend/ │ └── app.py # Streamlit frontend interface ├── .env # Contains OPENAI_API_KEY ├── requirements.txt # All project dependencies


---

## 🚀 Features

✅ AI-powered tutoring answers (via OpenAI)\
✅ Quiz generation with multiple-choice questions & explanations\
✅ Supports different learning styles and languages\
✅ Frontend built in Streamlit with tabbed layout\
✅ Backend served via FastAPI API with JSON responses

---

## 📦 Installation

### 1. Clone the repository


git clone https://github.com/your-username/ai-tutor.git
cd ai-tutor
### 2. Create a virtual environment and activate it

python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
### 3. Install dependencies

pip install -r requirements.txt
### 4. Set your OpenAI API key
Create a .env file in the root and add:

OPENAI_API_KEY=your_openai_api_key_here
# 🧪 How to Run the Project
### 1. Start the FastAPI backend

cd backend
uvicorn main:app --reload
By default, it will run at: http://127.0.0.1:8000

You can check the docs here:

Swagger UI: http://127.0.0.1:8000/docs

Redoc: http://127.0.0.1:8000/redoc

### 2. In a new terminal, run the Streamlit frontend

cd frontend
streamlit run app.py
This will open the UI in your browser: http://localhost:8501

✅ Example Usage
Select a subject like "Math", level "Beginner", and ask a question like:

Explain Newton's second law in simple terms.
Or go to the "Take a Quiz" tab and generate 5 random questions on "Science".

# ⚙️ Tech Stack
Frontend: Streamlit

Backend: FastAPI

AI Engine: LangChain + OpenAI

Environment Management: Python Dotenv

# 📄 Requirements
Here are some key dependencies:

- fastapi==0.104.1
- uvicorn==0.23.2
- streamlit==1.28.0
- langchain==0.0.335
- openai==1.2.4
- python-dotenv==1.0.0

Make sure to update your requirements.txt if you're adding new libraries.