from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List
import uvicorn

app = FastAPI()

class PersonalityResult(BaseModel):
    dominant_color: str
    scores: Dict[str, int]
    career_suggestions: List[str]
    strengths: List[str]
    weaknesses: List[str]

QUESTIONS = [
    "In a group project, you usually:",
    "When faced with a problem, you:",
    "Others would describe you as:",
    "What stresses you the most?",
    "At a party, you're the one who:",
    "What motivates you the most?",
    "How do you handle decisions?",
    "When working with others, you prefer:",
    "Your biggest strength is:",
    "Your biggest weakness could be:"
]

CAREER_MAP = {
    "RED": ["Management", "Entrepreneurship", "Sales Leadership", "Project Management"],
    "YELLOW": ["Marketing", "Public Relations", "Training", "Sales", "HR"],
    "GREEN": ["Customer Service", "Healthcare", "Social Work", "Teaching"],
    "BLUE": ["Data Analysis", "Engineering", "Research", "Quality Assurance"]
}

@app.get("/questions")
def get_questions():
    return {"questions": QUESTIONS}

@app.post("/analyze", response_model=PersonalityResult)
def analyze_personality(responses: Dict[int, str]):
    scores = {"RED": 0, "YELLOW": 0, "GREEN": 0, "BLUE": 0}
    
    for answer in responses.values():
        if answer.upper() == "A":
            scores["RED"] += 1
        elif answer.upper() == "B":
            scores["YELLOW"] += 1
        elif answer.upper() == "C":
            scores["GREEN"] += 1
        elif answer.upper() == "D":
            scores["BLUE"] += 1
    
    dominant = max(scores, key=scores.get)
    
    return PersonalityResult(
        dominant_color=dominant,
        scores=scores,
        career_suggestions=CAREER_MAP[dominant],
        strengths=get_strengths(dominant),
        weaknesses=get_weaknesses(dominant)
    )

def get_strengths(color: str) -> List[str]:
    strengths_map = {
        "RED": ["Leadership", "Decision-making", "Results-oriented"],
        "YELLOW": ["Communication", "Creativity", "Optimism"],
        "GREEN": ["Teamwork", "Patience", "Reliability"],
        "BLUE": ["Analysis", "Precision", "Planning"]
    }
    return strengths_map.get(color, [])

def get_weaknesses(color: str) -> List[str]:
    weaknesses_map = {
        "RED": ["Impatience", "Dominating"],
        "YELLOW": ["Disorganized", "Unrealistic"],
        "GREEN": ["Avoids conflict", "Resistant to change"],
        "BLUE": ["Overthinking", "Critical"]
    }
    return weaknesses_map.get(color, [])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)