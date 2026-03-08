"""
Research advisor agent
"""
from typing import Dict, Any, List, Optional
from counselor_ai.agents.base_agent import BaseAgent
from counselor_ai.models.student import StudentProfile
from counselor_ai.knowledge.prompts import (
    RESEARCH_ADVISOR_SYSTEM,
    RESEARCH_OPPORTUNITIES_PROMPT
)


class ResearchAdvisorAgent(BaseAgent):
    """Agent specialized in identifying research opportunities"""
    
    def find_opportunities(
        self,
        student: StudentProfile,
        research_interests: List[str],
        target_universities: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Find research opportunities for student
        
        Args:
            student: Student profile
            research_interests: List of research interests
            target_universities: Optional target universities
            
        Returns:
            Dictionary with research opportunities and guidance
        """
        # Format inputs
        profile_text = self._format_student_profile(student)
        interests_text = "\n".join([f"- {interest}" for interest in research_interests])
        universities_text = "\n".join([f"- {uni}" for uni in target_universities]) if target_universities else "To be determined"
        
        # Generate AI recommendations
        prompt = RESEARCH_OPPORTUNITIES_PROMPT.format(
            student_profile=profile_text,
            research_interests=interests_text,
            universities=universities_text
        )
        
        ai_recommendations = self.llm.generate_completion(
            prompt=prompt,
            system_prompt=RESEARCH_ADVISOR_SYSTEM,
            temperature=0.7,
            max_tokens=2500
        )
        
        # Generate structured opportunities
        structured_opportunities = self._generate_structured_opportunities(
            research_interests,
            student.graduation_year
        )
        
        # Strategy for approaching research
        outreach_strategy = self._generate_outreach_strategy(student)
        
        result = {
            "research_interests": research_interests,
            "ai_recommendations": ai_recommendations,
            "structured_opportunities": structured_opportunities,
            "outreach_strategy": outreach_strategy,
            "preparation_tips": self._get_preparation_tips(student)
        }
        
        return result
    
    def _generate_structured_opportunities(
        self,
        research_interests: List[str],
        graduation_year: int
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Generate structured list of research opportunities"""
        
        opportunities = {
            "summer_programs": [],
            "local_opportunities": [],
            "online_programs": [],
            "competitions": []
        }
        
        # Major REU programs (for rising seniors/college students)
        opportunities["summer_programs"] = [
            {
                "name": "NSF Research Experience for Undergraduates (REU)",
                "description": "Funded summer research at universities nationwide",
                "eligibility": "High school seniors and college students",
                "website": "nsf.gov/crssprgm/reu",
                "application_period": "December - February",
                "relevant_for": "All CS interests"
            },
            {
                "name": "MIT BWSI (Beaver Works Summer Institute)",
                "description": "Intensive summer STEM program",
                "eligibility": "Rising high school seniors",
                "application_period": "January - March",
                "relevant_for": "AI/ML, Robotics, Cybersecurity"
            },
            {
                "name": "Carnegie Mellon SAMS",
                "description": "Summer Academy for Math and Science",
                "eligibility": "Rising high school seniors",
                "application_period": "January - March",
                "relevant_for": "CS, Math, Engineering"
            },
            {
                "name": "Google Computer Science Summer Institute (CSSI)",
                "description": "3-week introduction to CS at Google",
                "eligibility": "High school seniors",
                "application_period": "February - March",
                "relevant_for": "General CS"
            }
        ]
        
        # Local opportunities
        opportunities["local_opportunities"] = [
            {
                "type": "University Research Labs",
                "description": "Contact local university CS departments",
                "action": "Email professors about volunteer/intern opportunities",
                "timing": "Start 2-3 months before desired start date"
            },
            {
                "type": "Company Internships",
                "description": "Local tech companies often have HS programs",
                "action": "Check company career pages for student programs",
                "timing": "Apply 3-4 months in advance"
            },
            {
                "type": "Science Fairs",
                "description": "Develop independent project for competition",
                "action": "Consider Intel ISEF, Regeneron STS, local fairs",
                "timing": "Start project 6-12 months before competition"
            }
        ]
        
        # Online opportunities
        opportunities["online_programs"] = [
            {
                "name": "MIT PRIMES",
                "description": "Year-long online research mentorship",
                "eligibility": "High school students",
                "application_period": "September - November",
                "format": "Online with MIT mentors"
            },
            {
                "name": "Polygence",
                "description": "1-on-1 research mentorship program",
                "eligibility": "High school students",
                "format": "Paid program, flexible timing",
                "outcome": "Research paper or project"
            },
            {
                "name": "Pioneer Academics",
                "description": "Online research program with university professors",
                "eligibility": "High school students",
                "format": "Online, 12-week program",
                "application_period": "Rolling admissions"
            }
        ]
        
        # Competitions and opportunities by interest
        if any("AI" in interest or "ML" in interest or "machine learning" in interest.lower() 
               for interest in research_interests):
            opportunities["competitions"].extend([
                {
                    "name": "Kaggle Competitions",
                    "description": "Data science and ML competitions",
                    "level": "Beginner to Advanced",
                    "benefit": "Real-world ML experience, portfolio building"
                },
                {
                    "name": "Congressional App Challenge",
                    "description": "Create an app addressing a problem",
                    "deadline": "October",
                    "benefit": "Recognition, portfolio piece"
                }
            ])
        
        if any("robotics" in interest.lower() for interest in research_interests):
            opportunities["competitions"].extend([
                {
                    "name": "FIRST Robotics Competition",
                    "description": "Team-based robotics competition",
                    "timing": "September - April",
                    "benefit": "Hands-on engineering, teamwork"
                }
            ])
        
        # General CS competitions
        opportunities["competitions"].extend([
            {
                "name": "USA Computing Olympiad (USACO)",
                "description": "Competitive programming",
                "format": "Online contests throughout the year",
                "benefit": "Algorithm skills, recognition"
            },
            {
                "name": "CyberPatriot",
                "description": "National cybersecurity competition",
                "timing": "October - March",
                "benefit": "Cybersecurity skills"
            }
        ])
        
        return opportunities
    
    def _generate_outreach_strategy(self, student: StudentProfile) -> Dict[str, Any]:
        """Generate strategy for reaching out to professors"""
        
        return {
            "when_to_reach_out": {
                "best_timing": "Early semester (September or January)",
                "avoid": "End of semester, summer (unless for summer research)",
                "lead_time": "2-3 months before desired start date"
            },
            "email_template": {
                "subject": "Undergraduate Research Opportunity - [Your Name]",
                "structure": [
                    "Brief introduction (name, school, year)",
                    "Specific interest in their research (cite a paper or project)",
                    "Your relevant experience and skills",
                    "What you hope to learn/contribute",
                    "Availability and commitment",
                    "Resume attached"
                ],
                "length": "3-4 short paragraphs",
                "tone": "Professional but enthusiastic"
            },
            "preparation": [
                "Read recent papers from the lab",
                "Understand the research area basics",
                "Prepare a 1-page resume highlighting relevant skills",
                "Have specific questions about their research",
                "Be ready to discuss your background"
            ],
            "follow_up": {
                "wait_time": "1-2 weeks before following up",
                "persistence": "Follow up once, then move on if no response",
                "backup_plan": "Contact 5-10 professors, expect 10-20% response rate"
            }
        }
    
    def _get_preparation_tips(self, student: StudentProfile) -> List[str]:
        """Get tips for preparing for research opportunities"""
        
        tips = []
        
        # Based on current CS background
        cs_strength = student.get_cs_profile_strength()
        
        if cs_strength in ["developing", "moderate"]:
            tips.extend([
                "Take online courses in your area of interest (Coursera, edX)",
                "Build personal projects to demonstrate skills",
                "Learn relevant programming languages (Python for ML, C++ for systems)",
                "Read introductory papers in your field of interest"
            ])
        
        # For all students
        tips.extend([
            "Create a GitHub profile showcasing your projects",
            "Prepare a research-focused resume",
            "Practice explaining your interests clearly and concisely",
            "Network at local tech meetups or university events",
            "Consider starting with a summer program before reaching out to professors"
        ])
        
        # If they have some experience
        if student.research_experience:
            tips.extend([
                "Prepare an abstract of your previous research",
                "Be ready to discuss what you learned and what you'd like to explore next",
                "Ask previous mentors for recommendations"
            ])
        
        return tips
