from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
import os
from dotenv import load_dotenv

# Import our AI modules
from career_recommendation.recommendation_engine import CareerRecommendationEngine
from skill_analysis.skill_analyzer import SkillAnalyzer
from chatbot.career_chatbot import CareerChatbot
from personality_analysis.personality_analyzer import app as personality_app

load_dotenv()

app = FastAPI(title="Career Advisor AI Services", version="1.0.0")

# Initialize AI engines
recommendation_engine = CareerRecommendationEngine()
skill_analyzer = SkillAnalyzer()
career_chatbot = CareerChatbot()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class UserProfile(BaseModel):
    interests: List[str]
    skills: List[str]
    experience_level: str
    education: str
    preferred_industries: List[str]

class CareerRecommendation(BaseModel):
    job_title: str
    match_percentage: float
    description: str
    required_skills: List[str]
    salary_range: str
    growth_prospects: str
    remote_friendly: bool = True
    industries: List[str] = []

class SkillGap(BaseModel):
    skill: str
    current_level: int
    required_level: int
    importance: str
    learning_resources: List[str]
    estimated_learning_time: int = 8
    market_demand: int = 5
    difficulty: int = 5

class ChatMessage(BaseModel):
    message: str
    user_context: Optional[Dict] = None

class PersonalityResponse(BaseModel):
    responses: Dict[int, str]

@app.get("/")
async def root():
    return {"message": "Career Advisor AI Services API - Enhanced with ML"}

@app.post("/career-recommendations")
async def get_career_recommendations(profile: UserProfile) -> List[CareerRecommendation]:
    try:
        # Convert Pydantic model to dict
        profile_dict = profile.dict()
        
        # Get recommendations from AI engine
        recommendations = recommendation_engine.get_recommendations(profile_dict, top_n=5)
        
        # Convert to Pydantic models
        result = []
        for rec in recommendations:
            result.append(CareerRecommendation(
                job_title=rec["job_title"],
                match_percentage=rec["match_percentage"],
                description=rec["description"],
                required_skills=rec["required_skills"],
                salary_range=rec["salary_range"],
                growth_prospects=rec["growth_prospects"],
                remote_friendly=rec.get("remote_friendly", True),
                industries=rec.get("industries", [])
            ))
        
        return result
    except Exception as e:
        # Fallback to mock data if AI engine fails
        return [
            CareerRecommendation(
                job_title="Data Scientist",
                match_percentage=92.5,
                description="Analyze complex data to help organizations make informed decisions",
                required_skills=["Python", "Machine Learning", "Statistics", "SQL"],
                salary_range="$80,000 - $150,000",
                growth_prospects="High demand, 22% growth expected"
            )
        ]

@app.post("/skill-gap-analysis")
async def analyze_skill_gaps(profile: UserProfile) -> List[SkillGap]:
    try:
        # Convert Pydantic model to dict
        profile_dict = profile.dict()
        
        # Get skill gap analysis from AI engine
        gaps = skill_analyzer.analyze_skill_gaps(profile_dict)
        
        # Convert to Pydantic models
        result = []
        for gap in gaps:
            result.append(SkillGap(
                skill=gap["skill"],
                current_level=gap["current_level"],
                required_level=gap["required_level"],
                importance=gap["importance"],
                learning_resources=gap["learning_resources"],
                estimated_learning_time=gap.get("estimated_learning_time", 8),
                market_demand=gap.get("market_demand", 5),
                difficulty=gap.get("difficulty", 5)
            ))
        
        return result
    except Exception as e:
        # Fallback to mock data
        return [
            SkillGap(
                skill="Machine Learning",
                current_level=3,
                required_level=7,
                importance="High",
                learning_resources=["Coursera ML Course", "Kaggle Learn", "Fast.ai"]
            )
        ]

@app.post("/chat")
async def chat_with_advisor(message: ChatMessage) -> Dict[str, str]:
    try:
        # Get response from AI chatbot
        response = career_chatbot.process_message(
            message.message, 
            message.user_context
        )
        return {"response": response}
    except Exception as e:
        # Fallback response
        return {"response": "I'm here to help with your career questions! Ask me about career paths, skills, or job market trends."}

@app.get("/job-forecasting")
async def get_job_forecasting(category: str = "all") -> List[Dict[str, Any]]:
    # Enhanced job forecasting data with category information
    all_forecasts = [
        {
            "job_title": "AI/ML Engineer",
            "growth_rate": 35,
            "demand_level": "Very High",
            "avg_salary": "$120,000",
            "key_skills": ["Python", "TensorFlow", "Deep Learning", "MLOps"],
            "trend": "Rapidly Growing",
            "category": "technology"
        },
        {
            "job_title": "Cybersecurity Specialist",
            "growth_rate": 28,
            "demand_level": "High",
            "avg_salary": "$95,000",
            "key_skills": ["Network Security", "Ethical Hacking", "Risk Assessment", "Compliance"],
            "trend": "Consistently Growing",
            "category": "technology"
        },
        {
            "job_title": "Data Analyst",
            "growth_rate": 23,
            "demand_level": "High",
            "avg_salary": "$75,000",
            "key_skills": ["SQL", "Excel", "Tableau", "Python", "Statistics"],
            "trend": "Steady Growth",
            "category": "technology"
        },
        {
            "job_title": "Cloud Solutions Architect",
            "growth_rate": 30,
            "demand_level": "Very High",
            "avg_salary": "$130,000",
            "key_skills": ["AWS", "Azure", "System Design", "DevOps"],
            "trend": "Rapidly Growing",
            "category": "technology"
        },
        {
            "job_title": "Product Manager",
            "growth_rate": 19,
            "demand_level": "High",
            "avg_salary": "$110,000",
            "key_skills": ["Product Strategy", "Analytics", "Agile", "Leadership"],
            "trend": "Steady Growth",
            "category": "technology"
        },
        {
            "job_title": "Nurse Practitioner",
            "growth_rate": 45,
            "demand_level": "Very High",
            "avg_salary": "$85,000",
            "key_skills": ["Patient Care", "Medical Knowledge", "Communication", "Critical Thinking"],
            "trend": "Rapidly Growing",
            "category": "healthcare"
        },
        {
            "job_title": "Physical Therapist",
            "growth_rate": 32,
            "demand_level": "High",
            "avg_salary": "$78,000",
            "key_skills": ["Rehabilitation", "Anatomy", "Patient Assessment", "Treatment Planning"],
            "trend": "Rapidly Growing",
            "category": "healthcare"
        },
        {
            "job_title": "Financial Analyst",
            "growth_rate": 15,
            "demand_level": "Medium",
            "avg_salary": "$72,000",
            "key_skills": ["Financial Modeling", "Excel", "Data Analysis", "Risk Assessment"],
            "trend": "Steady Growth",
            "category": "finance"
        },
        {
            "job_title": "Investment Advisor",
            "growth_rate": 18,
            "demand_level": "High",
            "avg_salary": "$95,000",
            "key_skills": ["Portfolio Management", "Client Relations", "Market Analysis", "Compliance"],
            "trend": "Steady Growth",
            "category": "finance"
        },
        {
            "job_title": "Special Education Teacher",
            "growth_rate": 22,
            "demand_level": "High",
            "avg_salary": "$58,000",
            "key_skills": ["Special Needs Education", "IEP Development", "Patience", "Communication"],
            "trend": "Consistently Growing",
            "category": "education"
        }
    ]
    
    # Filter by category
    if category == "all":
        return all_forecasts
    else:
        return [forecast for forecast in all_forecasts if forecast["category"] == category]

@app.get("/skill-learning-path/{skill_name}")
async def get_skill_learning_path(skill_name: str, current_level: int = 1, target_level: int = 8):
    try:
        learning_path = skill_analyzer.get_skill_learning_path(skill_name, current_level, target_level)
        return learning_path
    except Exception as e:
        return {"error": "Could not generate learning path"}

@app.get("/chatbot/conversation-summary")
async def get_conversation_summary():
    try:
        summary = career_chatbot.get_conversation_summary()
        return summary
    except Exception as e:
        return {"error": "Could not get conversation summary"}

@app.post("/chatbot/reset")
async def reset_chatbot():
    try:
        career_chatbot.reset_conversation()
        return {"message": "Conversation reset successfully"}
    except Exception as e:
        return {"error": "Could not reset conversation"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)