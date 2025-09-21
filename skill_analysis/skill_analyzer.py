import pandas as pd
import numpy as np
from typing import List, Dict, Any
import json

class SkillAnalyzer:
    def __init__(self):
        self.skill_database = self._load_skill_database()
        self.learning_resources = self._load_learning_resources()
    
    def _load_skill_database(self) -> Dict:
        """Load comprehensive skill database with market demand and difficulty"""
        return {
            "Python": {
                "category": "Programming",
                "difficulty": 6,
                "market_demand": 9,
                "avg_learning_time_weeks": 12,
                "related_skills": ["Data Science", "Machine Learning", "Web Development"],
                "job_roles": ["Data Scientist", "Software Engineer", "Backend Developer"]
            },
            "Machine Learning": {
                "category": "AI/Data Science",
                "difficulty": 8,
                "market_demand": 10,
                "avg_learning_time_weeks": 16,
                "related_skills": ["Python", "Statistics", "Data Analysis"],
                "job_roles": ["Data Scientist", "ML Engineer", "AI Researcher"]
            },
            "JavaScript": {
                "category": "Programming",
                "difficulty": 5,
                "market_demand": 9,
                "avg_learning_time_weeks": 10,
                "related_skills": ["HTML", "CSS", "React", "Node.js"],
                "job_roles": ["Frontend Developer", "Full Stack Developer", "Web Developer"]
            },
            "Project Management": {
                "category": "Management",
                "difficulty": 6,
                "market_demand": 8,
                "avg_learning_time_weeks": 8,
                "related_skills": ["Leadership", "Communication", "Agile"],
                "job_roles": ["Project Manager", "Product Manager", "Scrum Master"]
            },
            "Data Analysis": {
                "category": "Analytics",
                "difficulty": 6,
                "market_demand": 9,
                "avg_learning_time_weeks": 10,
                "related_skills": ["SQL", "Excel", "Statistics", "Visualization"],
                "job_roles": ["Data Analyst", "Business Analyst", "Research Analyst"]
            },
            "Cloud Computing": {
                "category": "Infrastructure",
                "difficulty": 7,
                "market_demand": 9,
                "avg_learning_time_weeks": 14,
                "related_skills": ["AWS", "Azure", "DevOps", "Networking"],
                "job_roles": ["Cloud Engineer", "DevOps Engineer", "Solutions Architect"]
            },
            "Communication": {
                "category": "Soft Skills",
                "difficulty": 4,
                "market_demand": 10,
                "avg_learning_time_weeks": 6,
                "related_skills": ["Leadership", "Presentation", "Writing"],
                "job_roles": ["Manager", "Consultant", "Sales Representative"]
            },
            "Cybersecurity": {
                "category": "Security",
                "difficulty": 8,
                "market_demand": 10,
                "avg_learning_time_weeks": 18,
                "related_skills": ["Networking", "Risk Assessment", "Compliance"],
                "job_roles": ["Security Analyst", "Security Engineer", "CISO"]
            }
        }
    
    def _load_learning_resources(self) -> Dict:
        """Load learning resources for different skills"""
        return {
            "Python": [
                "Python.org Official Tutorial",
                "Codecademy Python Course",
                "Real Python",
                "Python Crash Course Book",
                "Automate the Boring Stuff"
            ],
            "Machine Learning": [
                "Coursera ML Course (Andrew Ng)",
                "Fast.ai Practical Deep Learning",
                "Kaggle Learn",
                "Scikit-learn Documentation",
                "Hands-On Machine Learning Book"
            ],
            "JavaScript": [
                "MDN Web Docs",
                "freeCodeCamp",
                "JavaScript.info",
                "Eloquent JavaScript Book",
                "You Don't Know JS Series"
            ],
            "Project Management": [
                "PMI Certification Courses",
                "Coursera Project Management",
                "Agile Alliance Resources",
                "Scrum.org Training",
                "LinkedIn Learning PM Courses"
            ],
            "Data Analysis": [
                "Kaggle Learn Data Analysis",
                "Coursera Data Analysis Specialization",
                "Excel Training Resources",
                "Tableau Public Training",
                "Google Analytics Academy"
            ],
            "Cloud Computing": [
                "AWS Training and Certification",
                "Microsoft Azure Learning",
                "Google Cloud Training",
                "Cloud Guru Courses",
                "Linux Academy"
            ],
            "Communication": [
                "Toastmasters International",
                "Coursera Communication Courses",
                "Dale Carnegie Training",
                "TED Talks on Communication",
                "Harvard Business Review Articles"
            ],
            "Cybersecurity": [
                "Cybrary Free Courses",
                "SANS Training",
                "CompTIA Security+ Certification",
                "Offensive Security Training",
                "NIST Cybersecurity Framework"
            ]
        }
    
    def analyze_skill_gaps(self, user_profile: Dict, target_roles: List[str] = None) -> List[Dict]:
        """Analyze skill gaps for user profile"""
        user_skills = {skill.lower(): self._estimate_user_level(skill, user_profile) 
                      for skill in user_profile.get('skills', [])}
        
        if not target_roles:
            # Use recommended roles based on user interests
            target_roles = self._get_target_roles_from_interests(user_profile)
        
        skill_gaps = []
        analyzed_skills = set()
        
        for role in target_roles:
            required_skills = self._get_required_skills_for_role(role)
            
            for skill_name, required_level in required_skills.items():
                if skill_name.lower() in analyzed_skills:
                    continue
                
                current_level = user_skills.get(skill_name.lower(), 0)
                
                if current_level < required_level:
                    gap_info = self._create_skill_gap_info(
                        skill_name, current_level, required_level, user_profile
                    )
                    skill_gaps.append(gap_info)
                    analyzed_skills.add(skill_name.lower())
        
        # Sort by importance and gap size
        skill_gaps.sort(key=lambda x: (x['importance_score'], x['gap_size']), reverse=True)
        return skill_gaps[:10]  # Return top 10 gaps
    
    def _estimate_user_level(self, skill: str, user_profile: Dict) -> int:
        """Estimate user's current skill level (1-10 scale)"""
        experience_level = user_profile.get('experience_level', 'entry')
        
        # Base level based on experience
        base_levels = {
            'entry': 3,
            'mid': 5,
            'senior': 7,
            'executive': 8
        }
        
        base_level = base_levels.get(experience_level, 3)
        
        # Adjust based on education
        education = user_profile.get('education', '')
        if 'phd' in education.lower():
            base_level += 1
        elif 'master' in education.lower():
            base_level += 0.5
        
        return min(int(base_level), 10)
    
    def _get_target_roles_from_interests(self, user_profile: Dict) -> List[str]:
        """Get target roles based on user interests"""
        interests = [interest.lower() for interest in user_profile.get('interests', [])]
        
        role_mapping = {
            'technology': ['Software Engineer', 'Data Scientist'],
            'data': ['Data Scientist', 'Data Analyst'],
            'management': ['Project Manager', 'Product Manager'],
            'design': ['UX Designer', 'Product Designer'],
            'security': ['Cybersecurity Analyst', 'Security Engineer']
        }
        
        target_roles = []
        for interest in interests:
            for key, roles in role_mapping.items():
                if key in interest:
                    target_roles.extend(roles)
        
        return list(set(target_roles)) if target_roles else ['Software Engineer', 'Data Analyst']
    
    def _get_required_skills_for_role(self, role: str) -> Dict[str, int]:
        """Get required skills and their levels for a specific role"""
        role_requirements = {
            'Data Scientist': {
                'Python': 8, 'Machine Learning': 8, 'Statistics': 7,
                'Data Analysis': 8, 'Communication': 6
            },
            'Software Engineer': {
                'Programming': 8, 'JavaScript': 7, 'Python': 6,
                'Problem Solving': 8, 'Communication': 6
            },
            'Project Manager': {
                'Project Management': 9, 'Communication': 9, 'Leadership': 8,
                'Agile': 7, 'Risk Management': 6
            },
            'Data Analyst': {
                'Data Analysis': 8, 'SQL': 7, 'Excel': 7,
                'Statistics': 6, 'Communication': 7
            },
            'Cybersecurity Analyst': {
                'Cybersecurity': 8, 'Network Security': 7, 'Risk Assessment': 7,
                'Incident Response': 6, 'Compliance': 6
            }
        }
        
        return role_requirements.get(role, {})
    
    def _create_skill_gap_info(self, skill_name: str, current_level: int, 
                              required_level: int, user_profile: Dict) -> Dict:
        """Create detailed skill gap information"""
        skill_info = self.skill_database.get(skill_name, {})
        gap_size = required_level - current_level
        
        # Calculate importance score
        market_demand = skill_info.get('market_demand', 5)
        difficulty = skill_info.get('difficulty', 5)
        importance_score = (market_demand * 0.7 + (10 - difficulty) * 0.3) * gap_size
        
        # Determine priority level
        if importance_score >= 7:
            priority = 'High'
        elif importance_score >= 4:
            priority = 'Medium'
        else:
            priority = 'Low'
        
        return {
            'skill': skill_name,
            'current_level': current_level,
            'required_level': required_level,
            'gap_size': gap_size,
            'importance': priority,
            'importance_score': importance_score,
            'learning_resources': self.learning_resources.get(skill_name, []),
            'estimated_learning_time': skill_info.get('avg_learning_time_weeks', 8),
            'market_demand': market_demand,
            'difficulty': difficulty,
            'category': skill_info.get('category', 'General')
        }
    
    def get_skill_learning_path(self, skill_name: str, current_level: int, target_level: int) -> Dict:
        """Generate a learning path for a specific skill"""
        skill_info = self.skill_database.get(skill_name, {})
        gap = target_level - current_level
        
        # Calculate timeline
        weeks_per_level = skill_info.get('avg_learning_time_weeks', 8) / 10
        estimated_weeks = gap * weeks_per_level
        
        # Create milestones
        milestones = []
        for level in range(current_level + 1, target_level + 1):
            milestone = {
                'level': level,
                'description': f'Reach level {level} in {skill_name}',
                'estimated_weeks': weeks_per_level,
                'resources': self.learning_resources.get(skill_name, [])[:3]
            }
            milestones.append(milestone)
        
        return {
            'skill': skill_name,
            'current_level': current_level,
            'target_level': target_level,
            'estimated_total_weeks': int(estimated_weeks),
            'difficulty': skill_info.get('difficulty', 5),
            'milestones': milestones,
            'related_skills': skill_info.get('related_skills', []),
            'career_impact': skill_info.get('job_roles', [])
        }