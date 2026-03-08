"""
Essay coach agent
"""
from typing import Dict, Any, Optional, List
from counselor_ai.agents.base_agent import BaseAgent
from counselor_ai.models.student import StudentProfile
from counselor_ai.knowledge.prompts import (
    ESSAY_COACH_SYSTEM,
    ESSAY_FEEDBACK_PROMPT
)


class EssayCoachAgent(BaseAgent):
    """Agent specialized in providing essay feedback and guidance"""
    
    def analyze_essay(
        self,
        student: StudentProfile,
        essay_content: str,
        essay_type: str = "personal_statement",
        prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze and provide feedback on student essay
        
        Args:
            student: Student profile for context
            essay_content: The essay text
            essay_type: Type of essay
            prompt: Optional essay prompt
            
        Returns:
            Dictionary with detailed feedback
        """
        # Format student summary
        student_summary = f"""
{student.name}, Class of {student.graduation_year}
GPA: {student.academic_record.gpa}
Interests: {', '.join(student.cs_interests) if student.cs_interests else 'Not specified'}
Key Activities: {', '.join([ec.name for ec in student.extracurriculars[:3]]) if student.extracurriculars else 'Not specified'}
"""
        
        # Default prompts for common essay types
        default_prompts = {
            "personal_statement": "Some students have a background, identity, interest, or talent that is so meaningful they believe their application would be incomplete without it. If this sounds like you, then please share your story.",
            "why_cs": "Why are you interested in studying Computer Science?",
            "why_school": "Why do you want to attend this university?",
            "challenge": "The lessons we take from obstacles we encounter can be fundamental to later success. Recount a time when you faced a challenge, setback, or failure. How did it affect you, and what did you learn from the experience?"
        }
        
        essay_prompt = prompt or default_prompts.get(essay_type, "No specific prompt provided")
        
        # Generate AI feedback
        feedback_prompt = ESSAY_FEEDBACK_PROMPT.format(
            essay_type=essay_type,
            prompt=essay_prompt,
            essay_content=essay_content,
            student_summary=student_summary
        )
        
        ai_feedback = self.llm.generate_completion(
            prompt=feedback_prompt,
            system_prompt=ESSAY_COACH_SYSTEM,
            temperature=0.7,
            max_tokens=2500
        )
        
        # Basic essay analysis
        word_count = len(essay_content.split())
        
        result = {
            "essay_type": essay_type,
            "word_count": word_count,
            "recommended_length": self._get_recommended_length(essay_type),
            "ai_feedback": ai_feedback,
            "quick_checks": self._perform_quick_checks(essay_content, essay_type)
        }
        
        return result
    
    def _get_recommended_length(self, essay_type: str) -> str:
        """Get recommended word count for essay type"""
        ranges = {
            "personal_statement": "550-650 words (Common App: 650 max)",
            "supplemental": "200-300 words (varies by school)",
            "why_cs": "300-500 words",
            "why_school": "200-400 words",
            "activity": "150 words",
            "short_answer": "50-150 words"
        }
        return ranges.get(essay_type, "Check specific requirements")
    
    def _perform_quick_checks(self, essay_content: str, essay_type: str) -> Dict[str, Any]:
        """Perform quick automated checks on essay"""
        word_count = len(essay_content.split())
        
        checks = {
            "word_count_appropriate": True,
            "has_specific_examples": "specific" in essay_content.lower() or any(
                indicator in essay_content.lower() 
                for indicator in ["for example", "for instance", "specifically", "when i"]
            ),
            "avoids_cliches": not any(
                cliche in essay_content.lower()
                for cliche in [
                    "passion for", "since i was a child", "always been passionate",
                    "make a difference", "give back", "think outside the box"
                ]
            ),
            "uses_active_voice": True,  # Simplified check
            "shows_not_tells": any(
                word in essay_content.lower()
                for word in ["i created", "i built", "i developed", "i discovered", "i learned"]
            )
        }
        
        # Check word count for personal statement
        if essay_type == "personal_statement":
            checks["word_count_appropriate"] = 500 <= word_count <= 650
        elif essay_type == "supplemental":
            checks["word_count_appropriate"] = 150 <= word_count <= 350
        
        return checks
    
    def suggest_essay_topics(self, student: StudentProfile) -> List[str]:
        """Suggest potential essay topics based on student profile"""
        topics = []
        
        # Research-based topics
        if student.research_experience:
            topics.append(
                f"Your research experience in {student.research_experience[0].field} and what it taught you"
            )
        
        # Extracurricular-based topics
        if student.extracurriculars:
            for ec in student.extracurriculars:
                if ec.role and ec.achievements:
                    topics.append(
                        f"Your leadership in {ec.name} and specific challenges overcome"
                    )
        
        # CS interest topics
        if student.cs_interests:
            topics.append(
                f"Your journey discovering your interest in {student.cs_interests[0]}"
            )
        
        # Personal context
        if student.first_generation:
            topics.append(
                "Your perspective as a first-generation college student and what drives you"
            )
        
        # Project-based
        topics.extend([
            "A specific CS project that challenged you and what you learned",
            "A time you failed at something technical and how you persevered",
            "How you balance technical interests with other aspects of your life"
        ])
        
        return topics[:8]  # Return top 8 suggestions
