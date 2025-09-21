import re
import json
from typing import Dict, List, Any
import random

class CareerChatbot:
    def __init__(self):
        self.conversation_history = []
        self.user_context = {}
        self.response_templates = self._load_response_templates()
        self.career_knowledge = self._load_career_knowledge()
    
    def _load_response_templates(self) -> Dict:
        """Load response templates for different types of queries"""
        return {
            "career_change": [
                "Career transitions can be exciting opportunities for growth! Here are some key steps to consider:",
                "Changing careers is a significant decision. Let me help you think through this:",
                "Many successful professionals have made career pivots. Here's how to approach it strategically:"
            ],
            "salary_negotiation": [
                "Salary negotiation is an important skill. Here are some proven strategies:",
                "When it comes to salary discussions, preparation is key:",
                "Let's talk about effective salary negotiation techniques:"
            ],
            "skill_development": [
                "Continuous learning is crucial in today's job market. Here's my advice:",
                "Developing new skills can significantly boost your career prospects:",
                "Let me share some strategies for effective skill development:"
            ],
            "job_search": [
                "Job searching can be challenging, but with the right approach, you can succeed:",
                "Here are some modern job search strategies that work:",
                "Let me help you optimize your job search process:"
            ],
            "interview_prep": [
                "Interview preparation is crucial for success. Here's how to excel:",
                "Great interviews require preparation and practice. Let me guide you:",
                "Here are proven strategies to ace your next interview:"
            ],
            "networking": [
                "Networking is one of the most powerful career tools. Here's how to do it effectively:",
                "Building professional relationships can transform your career:",
                "Let me share some networking strategies that actually work:"
            ],
            "work_life_balance": [
                "Work-life balance is essential for long-term career success:",
                "Maintaining balance while advancing your career is definitely possible:",
                "Here are strategies to achieve better work-life integration:"
            ]
        }
    
    def _load_career_knowledge(self) -> Dict:
        """Load career-related knowledge base"""
        return {
            "career_change_steps": [
                "1. Assess your transferable skills and identify what you enjoy most",
                "2. Research target industries and roles thoroughly",
                "3. Network with professionals in your target field",
                "4. Consider taking courses or certifications to bridge skill gaps",
                "5. Start with informational interviews to learn more",
                "6. Update your resume to highlight relevant experience",
                "7. Consider transitional roles that bridge your current and target careers"
            ],
            "salary_negotiation_tips": [
                "Research market rates for your role and location using sites like Glassdoor",
                "Document your achievements and quantify your impact",
                "Practice your negotiation conversation beforehand",
                "Consider the entire compensation package, not just base salary",
                "Time your negotiation appropriately (after job offer, during reviews)",
                "Be prepared to justify your request with concrete examples",
                "Remain professional and collaborative throughout the process"
            ],
            "skill_development_strategies": [
                "Identify skills that are in high demand in your field",
                "Use online platforms like Coursera, Udemy, or LinkedIn Learning",
                "Practice new skills through personal projects or volunteering",
                "Seek mentorship from experts in areas you want to develop",
                "Join professional communities and attend industry events",
                "Set specific, measurable learning goals with deadlines",
                "Apply new skills immediately in your current role when possible"
            ],
            "job_search_best_practices": [
                "Optimize your LinkedIn profile with relevant keywords",
                "Tailor your resume for each application",
                "Use multiple job search channels (company websites, recruiters, networking)",
                "Follow up professionally after applications and interviews",
                "Prepare for common interview questions and practice your responses",
                "Research companies thoroughly before applying",
                "Maintain a positive attitude and stay persistent"
            ],
            "interview_preparation": [
                "Research the company, role, and interviewer beforehand",
                "Prepare specific examples using the STAR method (Situation, Task, Action, Result)",
                "Practice common behavioral and technical questions",
                "Prepare thoughtful questions to ask the interviewer",
                "Plan your outfit and route to the interview location",
                "Bring multiple copies of your resume and a notepad",
                "Follow up with a thank-you email within 24 hours"
            ],
            "networking_strategies": [
                "Attend industry events, conferences, and meetups regularly",
                "Engage meaningfully on professional social media platforms",
                "Offer help and value to others before asking for favors",
                "Maintain relationships through regular, genuine communication",
                "Join professional associations in your field",
                "Participate in online communities and forums",
                "Consider informational interviews to expand your network"
            ]
        }
    
    def process_message(self, message: str, user_context: Dict = None) -> str:
        """Process user message and generate appropriate response"""
        if user_context:
            self.user_context.update(user_context)
        
        # Add to conversation history
        self.conversation_history.append({"role": "user", "message": message})
        
        # Analyze message intent
        intent = self._analyze_intent(message)
        
        # Generate response based on intent
        response = self._generate_response(intent, message)
        
        # Add response to history
        self.conversation_history.append({"role": "assistant", "message": response})
        
        return response
    
    def _analyze_intent(self, message: str) -> str:
        """Analyze user message to determine intent"""
        message_lower = message.lower()
        
        # Define intent patterns
        intent_patterns = {
            "career_change": [
                "career change", "switch career", "change job", "new career",
                "different field", "career transition", "pivot"
            ],
            "salary_negotiation": [
                "salary", "negotiate", "pay raise", "compensation", "money",
                "wage", "income", "raise"
            ],
            "skill_development": [
                "learn", "skill", "course", "training", "education",
                "improve", "develop", "certification"
            ],
            "job_search": [
                "job search", "find job", "looking for", "apply", "hiring",
                "employment", "job hunting", "opportunities"
            ],
            "interview_prep": [
                "interview", "preparation", "questions", "interview tips",
                "job interview", "behavioral questions"
            ],
            "networking": [
                "network", "connections", "professional relationships",
                "meet people", "industry contacts", "linkedin"
            ],
            "work_life_balance": [
                "work life balance", "stress", "burnout", "time management",
                "balance", "wellness", "mental health"
            ]
        }
        
        # Check for pattern matches
        for intent, patterns in intent_patterns.items():
            for pattern in patterns:
                if pattern in message_lower:
                    return intent
        
        return "general"
    
    def _generate_response(self, intent: str, message: str) -> str:
        """Generate response based on intent and message"""
        if intent == "general":
            return self._generate_general_response(message)
        
        # Get appropriate template and knowledge
        templates = self.response_templates.get(intent, ["I'd be happy to help with that!"])
        knowledge_key = f"{intent}_steps" if f"{intent}_steps" in self.career_knowledge else f"{intent.replace('_', '_')}_tips"
        
        if knowledge_key not in self.career_knowledge:
            knowledge_key = list(self.career_knowledge.keys())[0]
        
        knowledge_items = self.career_knowledge.get(knowledge_key, [])
        
        # Select random template
        template = random.choice(templates)
        
        # Build response
        response = f"{template}\n\n"
        
        # Add relevant knowledge points
        if knowledge_items:
            for i, item in enumerate(knowledge_items[:5], 1):  # Limit to 5 items
                response += f"{item}\n"
            
            response += f"\nWould you like me to elaborate on any of these points or help you with something specific related to {intent.replace('_', ' ')}?"
        
        # Add personalized touch if user context available
        if self.user_context:
            response += self._add_personalized_advice(intent)
        
        return response
    
    def _generate_general_response(self, message: str) -> str:
        """Generate response for general queries"""
        general_responses = [
            "I'm here to help with your career questions! I can assist with career planning, job search strategies, skill development, salary negotiation, and more. What specific area would you like to explore?",
            "That's an interesting question! I specialize in career guidance and can help with topics like career transitions, interview preparation, networking, and professional development. How can I assist you today?",
            "I'd be happy to help you with your career-related concerns. I have expertise in areas like job searching, skill building, career planning, and workplace success strategies. What would you like to know more about?"
        ]
        
        return random.choice(general_responses)
    
    def _add_personalized_advice(self, intent: str) -> str:
        """Add personalized advice based on user context"""
        if not self.user_context:
            return ""
        
        experience_level = self.user_context.get('experience_level', '')
        skills = self.user_context.get('skills', [])
        interests = self.user_context.get('interests', [])
        
        personalized_advice = "\n\n💡 Personalized tip: "
        
        if intent == "career_change" and experience_level:
            if experience_level == "entry":
                personalized_advice += "As someone early in your career, you have great flexibility to explore different paths. Focus on building transferable skills."
            elif experience_level in ["mid", "senior"]:
                personalized_advice += "With your experience level, you can leverage your existing expertise while transitioning. Consider roles that value your background."
        
        elif intent == "skill_development" and skills:
            personalized_advice += f"Based on your current skills in {', '.join(skills[:3])}, I'd recommend focusing on complementary skills that enhance your expertise."
        
        elif intent == "job_search" and interests:
            personalized_advice += f"Given your interests in {', '.join(interests[:2])}, consider targeting companies and roles in these areas for better job satisfaction."
        
        else:
            return ""
        
        return personalized_advice
    
    def get_conversation_summary(self) -> Dict:
        """Get summary of conversation for analytics"""
        intents_discussed = []
        for entry in self.conversation_history:
            if entry["role"] == "user":
                intent = self._analyze_intent(entry["message"])
                if intent not in intents_discussed:
                    intents_discussed.append(intent)
        
        return {
            "total_messages": len(self.conversation_history),
            "intents_discussed": intents_discussed,
            "user_context": self.user_context,
            "conversation_length": len([msg for msg in self.conversation_history if msg["role"] == "user"])
        }
    
    def reset_conversation(self):
        """Reset conversation history and context"""
        self.conversation_history = []
        self.user_context = {}