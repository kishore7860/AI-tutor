from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
import os
from dotenv import load_dotenv
import json
import re
import logging

#configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

#load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def get_llm():
    try:
        llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.5,
            openai_api_key=OPENAI_API_KEY
        )
        logger.info("LLM initialized successfully")
        return llm
    except Exception as e:
        logger.error(f"Error initializing LLM: {e}")
        raise e
    
def generate_tutoring_response(subject, level, question, learning_style, background, language):
    try:
        llm = get_llm()
        
        # Construct the prompt with all the context
        prompt = _create_prompt(subject, level, question, learning_style, background, language)
        logger.info(f"Generating the tutoring response for subject {subject}, level {level}")
        response = llm.invoke(prompt)

        # Extract and validate response content
        if hasattr(response, 'content') and response.content:
            formatted_response = _format_tutoring_response(str(response.content), learning_style)
            return {"response": formatted_response}
        else:
            logger.error("Empty or invalid response from LLM")
            raise ValueError("Empty or invalid response from LLM")
    except Exception as e:
        logger.error(f"Error generating tutoring response: {str(e)}")
        raise Exception(f"Error generating tutoring response: {str(e)}")

    
def _format_tutoring_response(response, learning_style):
    if learning_style == "visual":
        return response + "\n\n*Note: The response includes a visual representation of the answer."
    elif learning_style == "Hands-on":
        return response + "\n\n*Note: The response includes a hands-on activity to help the student understand the answer."
    else:
        return response

def _create_prompt(subject, level, question, learning_style, background, language):
    prompt = f"""You are an expert tutor in {subject} for {level} level students.
    The student's learning style is: {learning_style}
    Their background knowledge: {background}
    Preferred language: {language}
    
    Please provide a clear and helpful response to this question:
    {question}

    Please structure your response in a way that:
    1. Addresses the question directly
    2. Provides step-by-step explanations
    3. Includes relevant examples
    4. Uses appropriate difficulty level for the student
    """
    return prompt

def _create_quiz_prompt(subject, level, num_questions):
    return f"""
You are an expert tutor in {subject} for {level}-level students.

Please create a quiz containing {num_questions} multiple-choice questions. 
Each question should be appropriate for the {level} level of difficulty.

Format your response **strictly** as a JSON array. 
Each question should follow this structure:

[
  {{
    "question": "Your question text here",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct_answer": "The correct answer text",
    "explanation": "Brief explanation of why this is the correct answer"
  }},
  ...
]

❗ Do not include any text before or after the JSON block.
Ensure the JSON is syntactically valid and well-structured.
"""

def _create_fallback_quiz(subject, num_questions):
    logger.warning(f"Using fallback quiz for subject {subject} with {num_questions} questions")
    return [
        {
            "question": f"Sample {subject} question {i+1}",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct_answer": "Option A",
            "explanation": "This is a fallback explanation for the question."
        }
        for i in range(num_questions)
    ]

def _validate_quiz_data(quiz_data):
    if not isinstance(quiz_data, list):
        raise ValueError("Quiz data must be a list")
    if not all(isinstance(question, dict) for question in quiz_data):
        raise ValueError("Quiz data must be a list of dictionaries")
    if not all(key in question for question in quiz_data for key in ["question", "options", "correct_answer", "explanation"]):
        raise ValueError("Quiz data must contain 'question', 'options', 'correct_answer', and 'explanation' keys")
    for question in quiz_data:
        if not isinstance(question["question"], str):
            raise ValueError("Question must be a string")
        if not isinstance(question["options"], list):
            raise ValueError("Options must be a list")
        if not isinstance(question["correct_answer"], str):
            raise ValueError("Correct answer must be a string")
        if not isinstance(question["explanation"], str):
            raise ValueError("Explanation must be a string")
    
def _parse_quiz_response(response_content,subject,num_questions):
    try:
        json_match=re.search(r'```json\s*(\[[\s\S]&?\])\s*```', response_content)
        if json_match:
            quiz_json=json_match.group(1)
        else:
            json_match=re.search(r'\[\s*\{.*\}\s*\]', response_content, re.DOTALL)
            if json_match:
                quiz_json=json_match.group(0)
            else:
                quiz_json=response_content
        quiz_data=json.loads(quiz_json)
        _validate_quiz_data(quiz_data)
        if len(quiz_data) > num_questions:
            quiz_data=quiz_data[:num_questions]
        for question in quiz_data:
            if "explanation" not in question:
                question["explanation"]=f"The correct answer is {question['correct_answer']}"
        return quiz_data
    except (json.JSONDecodeError, TypeError, ValueError) as e:
        logger.error(f"Error parsing quiz response: {e}")
        return _create_fallback_quiz(subject, num_questions)

def create_quiz(subject, level, num_questions=5, reveal_answer=True):
    try:
        llm=get_llm()
        prompt=_create_quiz_prompt(subject, level, num_questions)
        logger.info(f"Generating quiz for {subject} at level {level} with {num_questions} questions")
        response = llm.invoke(prompt)
        quiz_data=_parse_quiz_response(response.content, subject, num_questions)
        if reveal_answer:
            formatted_quiz=_format_quiz_with_reveal(quiz_data)
            return {
                "quiz_data":quiz_data,
                "formatted_quiz":formatted_quiz
            }
        else:
            return {"quiz": quiz_data}
    except Exception as e:
        logger.error(f"Error creating quiz: {e}")
        raise Exception(f"Error creating quiz: {e}")
    
def _format_quiz_with_reveal(quiz_data):
    html = ""
    for i, question in enumerate(quiz_data, 1):
        html += f"<h4>Q{i}. {question['question']}</h4><ul>"
        option_letters = ["A", "B", "C", "D"]
        correct_index = question["options"].index(question["correct_answer"]) if question["correct_answer"] in question["options"] else 0
        for j, option in enumerate(question["options"]):
            is_correct = j == correct_index
            if is_correct:
                html += f"<li><b>{option_letters[j]}. {option} ✅</b></li>"
            else:
                html += f"<li>{option_letters[j]}. {option}</li>"
        html += f"</ul><p><i>Explanation: {question['explanation']}</i></p><hr>"
    return html
def export_quiz_to_html(quiz_data,file_path="quiz.html"):
    try:
        with open(file_path,"w",encoding="utf-8") as file:
            file.write(_format_quiz_with_reveal(quiz_data))
        logger.info(f"Quiz exported to {file_path}")
        return True
    except Exception as e:
        logger.error(f"Error exporting quiz to HTML: {e}")
        raise Exception(f"Error exporting quiz to HTML: {e}")
        return False

