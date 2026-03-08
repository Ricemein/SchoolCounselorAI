"""
Base agent implementation for college counseling
"""
from typing import List, Dict, Any, Optional
from counselor_ai.models.student import StudentProfile
from counselor_ai.models.university import University
from counselor_ai.utils.llm_client import LLMClient
from counselor_ai.knowledge.prompts import *


class BaseAgent:
    """Base class for all counselor AI agents"""
    
    def __init__(self, llm_client: Optional[LLMClient] = None):
        """
        Initialize base agent
        
        Args:
            llm_client: LLM client instance (creates new one if not provided)
        """
        self.llm = llm_client or LLMClient()
    
    def _format_student_profile(self, student: StudentProfile) -> str:
        """Format student profile for LLM consumption"""
        profile_text = f"""
Student: {student.name}
Graduation Year: {student.graduation_year}

ACADEMIC RECORD:
- GPA: {student.academic_record.gpa} / 4.0"""
        
        if student.academic_record.gpa_weighted:
            profile_text += f" (Weighted: {student.academic_record.gpa_weighted})"
        
        if student.academic_record.class_rank and student.academic_record.class_size:
            percentile = (1 - (student.academic_record.class_rank / student.academic_record.class_size)) * 100
            profile_text += f"\n- Class Rank: {student.academic_record.class_rank} / {student.academic_record.class_size} (Top {percentile:.1f}%)"
        
        # Test scores
        if student.academic_record.sat_total:
            profile_text += f"\n- SAT: {student.academic_record.sat_total}"
            if student.academic_record.sat_math:
                profile_text += f" (Math: {student.academic_record.sat_math}, EBRW: {student.academic_record.sat_ebrw})"
        
        if student.academic_record.act_composite:
            profile_text += f"\n- ACT: {student.academic_record.act_composite}"
        
        # Coursework
        if student.academic_record.cs_courses:
            profile_text += f"\n- CS Courses: {', '.join(student.academic_record.cs_courses)}"
        
        if student.academic_record.math_courses:
            profile_text += f"\n- Math Courses: {', '.join(student.academic_record.math_courses)}"
        
        if student.academic_record.ap_courses:
            profile_text += f"\n- AP Courses: {', '.join(student.academic_record.ap_courses)}"
            if student.academic_record.ap_scores:
                scores_str = ', '.join([f"{course}: {score}" for course, score in student.academic_record.ap_scores.items()])
                profile_text += f"\n- AP Scores: {scores_str}"
        
        # Interests
        if student.cs_interests:
            profile_text += f"\n\nCS/ENGINEERING INTERESTS:\n{', '.join(student.cs_interests)}"
        
        if student.career_goals:
            profile_text += f"\n\nCAREER GOALS:\n{student.career_goals}"
        
        # Research Experience
        if student.research_experience:
            profile_text += f"\n\nRESEARCH EXPERIENCE:"
            for i, research in enumerate(student.research_experience, 1):
                profile_text += f"\n{i}. {research.title}"
                profile_text += f"\n   Field: {research.field}"
                profile_text += f"\n   Duration: {research.duration_months} months"
                profile_text += f"\n   Description: {research.description}"
                if research.outcome:
                    profile_text += f"\n   Outcome: {research.outcome}"
        
        # Extracurriculars
        if student.extracurriculars:
            profile_text += f"\n\nEXTRACURRICULAR ACTIVITIES:"
            for i, ec in enumerate(student.extracurriculars, 1):
                profile_text += f"\n{i}. {ec.name}"
                if ec.role:
                    profile_text += f" - {ec.role}"
                profile_text += f"\n   Years: {ec.years_participated}"
                if ec.hours_per_week:
                    profile_text += f", Hours/week: {ec.hours_per_week}"
                if ec.achievements:
                    profile_text += f"\n   Achievements: {', '.join(ec.achievements)}"
        
        # Awards and Honors
        if student.awards_honors:
            profile_text += f"\n\nAWARDS & HONORS:\n{', '.join(student.awards_honors)}"
        
        # Context
        if student.first_generation:
            profile_text += f"\n\nFirst-generation college student"
        
        if student.financial_need:
            profile_text += f"\nFinancial need: {student.financial_need}"
        
        return profile_text


class CounselorAgent:
    """
    Main counselor agent that coordinates specialized agents
    """
    
    def __init__(self, llm_client: Optional[LLMClient] = None):
        """
        Initialize the counselor agent with all specialized agents
        
        Args:
            llm_client: Optional LLM client to share across agents
        """
        self.llm = llm_client or LLMClient()
        
        # Import specialized agents here to avoid circular imports
        from counselor_ai.agents.profile_analyzer import ProfileAnalyzerAgent
        from counselor_ai.agents.university_matcher import UniversityMatcherAgent
        from counselor_ai.agents.essay_coach import EssayCoachAgent
        from counselor_ai.agents.timeline_manager import TimelineManagerAgent
        from counselor_ai.agents.research_advisor import ResearchAdvisorAgent
        
        # Initialize specialized agents
        self.profile_analyzer = ProfileAnalyzerAgent(self.llm)
        self.university_matcher = UniversityMatcherAgent(self.llm)
        self.essay_coach = EssayCoachAgent(self.llm)
        self.timeline_manager = TimelineManagerAgent(self.llm)
        self.research_advisor = ResearchAdvisorAgent(self.llm)
    
    def analyze_student_profile(self, student: StudentProfile) -> Dict[str, Any]:
        """
        Comprehensive analysis of student profile
        
        Args:
            student: Student profile to analyze
            
        Returns:
            Dictionary with analysis results
        """
        return self.profile_analyzer.analyze(student)
    
    def get_university_recommendations(
        self,
        student: StudentProfile,
        preferences: Optional[Dict[str, Any]] = None
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get university recommendations for student
        
        Args:
            student: Student profile
            preferences: Optional preferences (region, size, etc.)
            
        Returns:
            Dictionary with reach, target, and safety school recommendations
        """
        return self.university_matcher.match_universities(student, preferences)
    
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
            essay_type: Type of essay (personal_statement, supplemental, etc.)
            prompt: The essay prompt
            
        Returns:
            Dictionary with feedback and suggestions
        """
        return self.essay_coach.analyze_essay(student, essay_content, essay_type, prompt)
    
    def create_application_timeline(
        self,
        student: StudentProfile,
        target_universities: List[str],
        application_type: str = "regular_decision"
    ) -> Dict[str, Any]:
        """
        Create application timeline for student
        
        Args:
            student: Student profile
            target_universities: List of university names
            application_type: Type of application (early_action, early_decision, regular_decision)
            
        Returns:
            Dictionary with timeline and milestones
        """
        return self.timeline_manager.create_timeline(student, target_universities, application_type)
    
    def get_research_opportunities(
        self,
        student: StudentProfile,
        research_interests: List[str],
        target_universities: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Identify research opportunities for student
        
        Args:
            student: Student profile
            research_interests: Specific research interests
            target_universities: Optional list of target universities
            
        Returns:
            Dictionary with research opportunities and strategies
        """
        return self.research_advisor.find_opportunities(student, research_interests, target_universities)
    
    def comprehensive_consultation(self, student: StudentProfile) -> Dict[str, Any]:
        """
        Complete consultation covering all aspects
        
        Args:
            student: Student profile
            
        Returns:
            Dictionary with comprehensive guidance
        """
        results = {
            "profile_analysis": self.analyze_student_profile(student),
            "university_recommendations": self.get_university_recommendations(student),
            "recommended_next_steps": []
        }
        
        # Add personalized next steps based on analysis
        profile_strength = student.get_cs_profile_strength()
        
        if profile_strength in ["developing", "moderate"]:
            results["recommended_next_steps"].append(
                "Consider additional CS coursework or projects to strengthen your profile"
            )
        
        if not student.research_experience:
            results["recommended_next_steps"].append(
                "Explore research opportunities to enhance your application"
            )
        
        if student.academic_record.sat_total and student.academic_record.sat_total < 1450:
            results["recommended_next_steps"].append(
                "Consider retaking standardized tests or focusing on test-optional schools"
            )
        
        return results
