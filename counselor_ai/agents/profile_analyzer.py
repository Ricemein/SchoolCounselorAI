"""
Profile analyzer agent
"""
from typing import Dict, Any
from counselor_ai.agents.base_agent import BaseAgent
from counselor_ai.models.student import StudentProfile
from counselor_ai.knowledge.prompts import (
    PROFILE_ANALYZER_SYSTEM,
    PROFILE_ANALYSIS_PROMPT
)


class ProfileAnalyzerAgent(BaseAgent):
    """Agent specialized in analyzing student profiles"""
    
    def analyze(self, student: StudentProfile) -> Dict[str, Any]:
        """
        Comprehensive analysis of student profile
        
        Args:
            student: Student profile to analyze
            
        Returns:
            Dictionary with detailed analysis
        """
        # Format student profile
        profile_text = self._format_student_profile(student)
        
        # Generate AI analysis
        prompt = PROFILE_ANALYSIS_PROMPT.format(student_profile=profile_text)
        ai_analysis = self.llm.generate_completion(
            prompt=prompt,
            system_prompt=PROFILE_ANALYZER_SYSTEM,
            temperature=0.7
        )
        
        # Calculate objective metrics
        academic_index = student.calculate_academic_index()
        ec_strength = student.get_extracurricular_strength()
        cs_strength = student.get_cs_profile_strength()
        
        # Structure the response
        result = {
            "student_name": student.name,
            "objective_metrics": {
                "academic_index": round(academic_index, 2),
                "gpa": student.academic_record.gpa,
                "test_scores": {
                    "sat": student.academic_record.sat_total,
                    "act": student.academic_record.act_composite
                },
                "extracurricular_strength": ec_strength,
                "cs_profile_strength": cs_strength,
                "has_research_experience": student.has_research_experience()
            },
            "ai_analysis": ai_analysis,
            "quick_summary": self._generate_quick_summary(student, academic_index, ec_strength, cs_strength)
        }
        
        return result
    
    def _generate_quick_summary(
        self,
        student: StudentProfile,
        academic_index: float,
        ec_strength: str,
        cs_strength: str
    ) -> str:
        """Generate a quick summary of the profile"""
        
        # Academic level
        if academic_index >= 90:
            academic_level = "exceptional"
        elif academic_index >= 80:
            academic_level = "very strong"
        elif academic_index >= 70:
            academic_level = "strong"
        else:
            academic_level = "competitive"
        
        summary = f"{student.name} presents a {academic_level} academic profile "
        summary += f"with {ec_strength} extracurricular involvement and "
        summary += f"{cs_strength} CS preparation. "
        
        # Add context
        if student.has_research_experience():
            summary += "Research experience adds significant strength. "
        
        if student.first_generation:
            summary += "First-generation status provides additional context. "
        
        # Competitive level
        if academic_index >= 85 and cs_strength in ["strong", "exceptional"]:
            summary += "Competitive for top-tier CS programs with balanced list."
        elif academic_index >= 75:
            summary += "Competitive for strong CS programs; reach schools possible with strong essays."
        else:
            summary += "Should focus on programs matching profile with some reaches."
        
        return summary
