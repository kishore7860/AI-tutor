from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi. responses import HTMLResponse
from pydantic import BaseModel, Field
import os
from typing import List, Dict, Any, Optional
from dotenv import  load_dotenv
from .engine import generate_tutoring_response, create_quiz

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")
app = FastAPI(
    title="AI Tutor API",
    description="A simple API for generating responses from a GPT-4 model",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

class TutorRequest(BaseModel):
    subject: str = Field(..., description="Academic subject")
    level: str = Field(..., description="Level of difficulty(Beginner, Intermediate, Advanced)")
    question: str = Field(..., description="Question")
    learning_style: str = Field(..., description="Learning style")
    background: str = Field("Unknown", description="Background information")
    language: str = Field("English", description="Language")

class QuizRequest(BaseModel):
    subject: str = Field(..., description="Academic subject")
    level: str = Field(..., description="Level of difficulty(Beginner, Intermediate, Advanced)")
    num_questions: int = Field(5, description="Number of questions", ge=1, le=10)
    reveal_answer: Optional[bool] = Field(True, description="Whether to reveal the answer")

class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    correct_answer: str
    explanation: Optional[str] = None

class TutorResponse(BaseModel):
    response: str

class QuizResponse(BaseModel):
    quiz: List[Dict[str, Any]]
    formatted_quiz: Optional[str]=None

@app.post("/tutor", response_model=TutorResponse)
async def get_tutoring_response(data: TutorRequest):
    try:
        response_data = generate_tutoring_response(
            subject=data.subject,
            level=data.level,
            question=data.question,
            learning_style=data.learning_style,
            background=data.background,
            language=data.language
        )
        return response_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/quiz", response_model=QuizResponse)
async def generate_quiz_api(data: QuizRequest):
    try:
        quiz_data = create_quiz(
            subject=data.subject,
            level=data.level,
            num_questions=data.num_questions,
            reveal_answer=data.reveal_answer
        )
        if data.reveal_answer:
            return {
                "quiz": quiz_data["quiz_data"],
                "formatted_quiz": quiz_data.get("formatted_quiz")
            }
        else:
            return {
                "quiz": quiz_data["quiz"]  # 🔄 Not "quiz_data"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/quiz-html/{subject}/{level}/{num_questions}", response_class=HTMLResponse)
async def get_quiz_html(subject: str, level: str, num_questions: int=5):
    try:
        quiz_data = create_quiz_quiz(subject, level, num_questions, reveal_answer=True)
        return quiz_data["formatted_quiz"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    return {"status": "Healthy"}