import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Any
import json

class CareerRecommendationEngine:
    def __init__(self):
        self.job_database = self._load_job_database()
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self._prepare_job_vectors()
    
    def _load_job_database(self) -> List[Dict]:
        """Load job database with comprehensive job information"""
        return [
            {
                "job_title": "Data Scientist",
                "description": "Analyze complex data to help organizations make informed decisions using statistical methods and machine learning",
                "required_skills": ["Python", "Machine Learning", "Statistics", "SQL", "Data Visualization", "R"],
                "preferred_skills": ["Deep Learning", "Big Data", "Cloud Computing", "Tableau"],
                "industries": ["Technology", "Finance", "Healthcare", "Consulting"],
                "experience_levels": ["mid", "senior"],
                "education_requirements": ["bachelor", "master", "phd"],
                "salary_range": "$80,000 - $150,000",
                "growth_prospects": "High demand, 22% growth expected",
                "remote_friendly": True
            },
            {
                "job_title": "Software Engineer",
                "description": "Design, develop, and maintain software applications and systems",
                "required_skills": ["Programming", "Problem Solving", "System Design", "Git"],
                "preferred_skills": ["JavaScript", "Python", "Java", "React", "Node.js"],
                "industries": ["Technology", "Finance", "Healthcare", "Media"],
                "experience_levels": ["entry", "mid", "senior"],
                "education_requirements": ["bachelor", "master"],
                "salary_range": "$70,000 - $140,000",
                "growth_prospects": "Excellent, 13% growth expected",
                "remote_friendly": True
            },
            {
                "job_title": "Product Manager",
                "description": "Lead product development from conception to launch, working with cross-functional teams",
                "required_skills": ["Product Strategy", "Project Management", "Communication", "Analytics"],
                "preferred_skills": ["Agile", "User Research", "Data Analysis", "Leadership"],
                "industries": ["Technology", "Retail", "Finance", "Healthcare"],
                "experience_levels": ["mid", "senior"],
                "education_requirements": ["bachelor", "master"],
                "salary_range": "$90,000 - $160,000",
                "growth_prospects": "Strong demand, 15% growth expected",
                "remote_friendly": True
            },
            {
                "job_title": "UX Designer",
                "description": "Create user-centered designs for digital products and services",
                "required_skills": ["Design Thinking", "Prototyping", "User Research", "Wireframing"],
                "preferred_skills": ["Figma", "Adobe Creative Suite", "HTML/CSS", "Psychology"],
                "industries": ["Technology", "Media", "Retail", "Healthcare"],
                "experience_levels": ["entry", "mid", "senior"],
                "education_requirements": ["bachelor", "master"],
                "salary_range": "$65,000 - $120,000",
                "growth_prospects": "Growing field, 18% growth expected",
                "remote_friendly": True
            },
            {
                "job_title": "Cybersecurity Analyst",
                "description": "Protect organizations from cyber threats and security breaches",
                "required_skills": ["Network Security", "Risk Assessment", "Incident Response", "Security Tools"],
                "preferred_skills": ["Ethical Hacking", "Compliance", "Forensics", "Cloud Security"],
                "industries": ["Technology", "Finance", "Government", "Healthcare"],
                "experience_levels": ["entry", "mid", "senior"],
                "education_requirements": ["bachelor", "master"],
                "salary_range": "$75,000 - $130,000",
                "growth_prospects": "Very high demand, 28% growth expected",
                "remote_friendly": False
            },
            {
                "job_title": "Digital Marketing Manager",
                "description": "Develop and execute digital marketing strategies across multiple channels",
                "required_skills": ["Digital Marketing", "Analytics", "Content Strategy", "SEO/SEM"],
                "preferred_skills": ["Social Media", "Email Marketing", "Google Analytics", "A/B Testing"],
                "industries": ["Marketing", "Retail", "Technology", "Media"],
                "experience_levels": ["mid", "senior"],
                "education_requirements": ["bachelor", "master"],
                "salary_range": "$60,000 - $110,000",
                "growth_prospects": "Steady growth, 12% growth expected",
                "remote_friendly": True
            }
        ]
    
    def _prepare_job_vectors(self):
        """Prepare TF-IDF vectors for job matching"""
        job_texts = []
        for job in self.job_database:
            text = f"{job['description']} {' '.join(job['required_skills'])} {' '.join(job['preferred_skills'])}"
            job_texts.append(text)
        
        self.job_vectors = self.vectorizer.fit_transform(job_texts)
    
    def calculate_match_score(self, user_profile: Dict, job: Dict) -> float:
        """Calculate comprehensive match score between user and job"""
        score = 0.0
        
        # Skills matching (40% weight)
        user_skills = set([skill.lower() for skill in user_profile.get('skills', [])])
        required_skills = set([skill.lower() for skill in job['required_skills']])
        preferred_skills = set([skill.lower() for skill in job['preferred_skills']])
        
        required_match = len(user_skills.intersection(required_skills)) / len(required_skills) if required_skills else 0
        preferred_match = len(user_skills.intersection(preferred_skills)) / len(preferred_skills) if preferred_skills else 0
        
        skills_score = (required_match * 0.7 + preferred_match * 0.3) * 0.4
        score += skills_score
        
        # Experience level matching (20% weight)
        user_exp = user_profile.get('experience_level', '').lower()
        if user_exp in job['experience_levels']:
            score += 0.2
        
        # Education matching (15% weight)
        user_edu = user_profile.get('education', '').lower()
        if user_edu in job['education_requirements']:
            score += 0.15
        
        # Industry preference matching (15% weight)
        user_industries = set([ind.lower() for ind in user_profile.get('preferred_industries', [])])
        job_industries = set([ind.lower() for ind in job['industries']])
        
        if user_industries.intersection(job_industries):
            score += 0.15
        
        # Interest alignment using text similarity (10% weight)
        user_text = ' '.join(user_profile.get('interests', []))
        if user_text:
            user_vector = self.vectorizer.transform([user_text])
            job_index = next(i for i, j in enumerate(self.job_database) if j['job_title'] == job['job_title'])
            similarity = cosine_similarity(user_vector, self.job_vectors[job_index:job_index+1])[0][0]
            score += similarity * 0.1
        
        return min(score * 100, 100)  # Convert to percentage and cap at 100
    
    def get_recommendations(self, user_profile: Dict, top_n: int = 5) -> List[Dict]:
        """Get top N career recommendations for user"""
        recommendations = []
        
        for job in self.job_database:
            match_score = self.calculate_match_score(user_profile, job)
            
            recommendation = {
                "job_title": job["job_title"],
                "match_percentage": round(match_score, 1),
                "description": job["description"],
                "required_skills": job["required_skills"],
                "salary_range": job["salary_range"],
                "growth_prospects": job["growth_prospects"],
                "remote_friendly": job["remote_friendly"],
                "industries": job["industries"]
            }
            recommendations.append(recommendation)
        
        # Sort by match percentage and return top N
        recommendations.sort(key=lambda x: x['match_percentage'], reverse=True)
        return recommendations[:top_n]
    
    def get_skill_recommendations(self, user_profile: Dict, target_job: str) -> List[str]:
        """Get skill recommendations for a specific target job"""
        target_job_data = next((job for job in self.job_database if job['job_title'] == target_job), None)
        
        if not target_job_data:
            return []
        
        user_skills = set([skill.lower() for skill in user_profile.get('skills', [])])
        required_skills = set([skill.lower() for skill in target_job_data['required_skills']])
        preferred_skills = set([skill.lower() for skill in target_job_data['preferred_skills']])
        
        missing_required = required_skills - user_skills
        missing_preferred = preferred_skills - user_skills
        
        recommendations = list(missing_required) + list(missing_preferred)
        return recommendations[:10]  # Return top 10 skill recommendations