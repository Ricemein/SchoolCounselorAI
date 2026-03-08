"""
Timeline manager agent
"""
from typing import Dict, Any, List
from datetime import datetime, timedelta
from counselor_ai.agents.base_agent import BaseAgent
from counselor_ai.models.student import StudentProfile
from counselor_ai.knowledge.prompts import (
    TIMELINE_MANAGER_SYSTEM,
    TIMELINE_GENERATION_PROMPT
)


class TimelineManagerAgent(BaseAgent):
    """Agent specialized in creating application timelines"""
    
    def create_timeline(
        self,
        student: StudentProfile,
        target_universities: List[str],
        application_type: str = "regular_decision"
    ) -> Dict[str, Any]:
        """
        Create detailed application timeline
        
        Args:
            student: Student profile
            target_universities: List of target university names
            application_type: Type of application deadline
            
        Returns:
            Dictionary with timeline and milestones
        """
        # Format inputs
        profile_text = self._format_student_profile(student)
        universities_text = "\n".join([f"- {uni}" for uni in target_universities])
        current_date = datetime.now().strftime("%B %d, %Y")
        
        # Generate AI timeline
        prompt = TIMELINE_GENERATION_PROMPT.format(
            student_profile=profile_text,
            universities=universities_text,
            application_type=application_type,
            current_date=current_date
        )
        
        ai_timeline = self.llm.generate_completion(
            prompt=prompt,
            system_prompt=TIMELINE_MANAGER_SYSTEM,
            temperature=0.5,
            max_tokens=2500
        )
        
        # Generate structured timeline
        structured_timeline = self._generate_structured_timeline(
            student.graduation_year,
            application_type
        )
        
        # Key deadlines
        deadlines = self._get_key_deadlines(application_type, student.graduation_year)
        
        result = {
            "application_type": application_type,
            "target_universities": target_universities,
            "ai_timeline": ai_timeline,
            "structured_timeline": structured_timeline,
            "key_deadlines": deadlines,
            "current_phase": self._determine_current_phase(student.graduation_year, application_type)
        }
        
        return result
    
    def _generate_structured_timeline(
        self,
        graduation_year: int,
        application_type: str
    ) -> Dict[str, List[Dict[str, str]]]:
        """Generate structured month-by-month timeline"""
        
        senior_year = graduation_year - 1
        junior_year = graduation_year - 2
        
        timeline = {}
        
        # Junior Year Spring (if relevant)
        if datetime.now().year <= junior_year:
            timeline[f"Spring {junior_year} (Junior Year)"] = [
                {"task": "Take SAT/ACT (if needed)", "priority": "high"},
                {"task": "Visit colleges (if possible)", "priority": "medium"},
                {"task": "Identify potential recommenders", "priority": "medium"},
                {"task": "Work on summer activities/internships", "priority": "high"},
                {"task": "Begin brainstorming essay topics", "priority": "low"}
            ]
        
        # Summer before Senior Year
        timeline[f"Summer {senior_year}"] = [
            {"task": "Draft personal statement", "priority": "high"},
            {"task": "Finalize college list", "priority": "high"},
            {"task": "Create Common App account", "priority": "high"},
            {"task": "Request recommendations (by August)", "priority": "high"},
            {"task": "Retake SAT/ACT if needed", "priority": "medium"},
            {"task": "Visit top choice schools", "priority": "medium"}
        ]
        
        # Fall Senior Year
        timeline[f"September {senior_year}"] = [
            {"task": "Complete activities list on Common App", "priority": "high"},
            {"task": "Revise personal statement (multiple drafts)", "priority": "high"},
            {"task": "Research scholarship opportunities", "priority": "medium"},
            {"task": "Confirm recommenders have submitted", "priority": "high"}
        ]
        
        timeline[f"October {senior_year}"] = [
            {"task": "Finalize personal statement", "priority": "high"},
            {"task": "Start supplemental essays", "priority": "high"},
            {"task": "Complete UC applications (if applicable) - Due Oct 31", "priority": "high"},
            {"task": "Submit Early Action/Decision apps - Due Nov 1", "priority": "high" if application_type in ["early_action", "early_decision"] else "medium"}
        ]
        
        timeline[f"November {senior_year}"] = [
            {"task": "Complete all supplemental essays", "priority": "high"},
            {"task": "Proofread all application materials", "priority": "high"},
            {"task": "Complete CSS Profile/FAFSA prep", "priority": "high"},
            {"task": "Submit remaining Early Action apps", "priority": "medium"}
        ]
        
        timeline[f"December {senior_year}"] = [
            {"task": "Complete Regular Decision applications", "priority": "high"},
            {"task": "Submit FAFSA (opens Oct 1)", "priority": "high"},
            {"task": "Submit CSS Profile if required", "priority": "high"},
            {"task": "Maintain strong grades!", "priority": "high"}
        ]
        
        timeline[f"January {graduation_year}"] = [
            {"task": "Submit any remaining Regular Decision apps - Due Jan 1-15", "priority": "high"},
            {"task": "Send mid-year grade reports", "priority": "high"},
            {"task": "Apply for additional scholarships", "priority": "medium"},
            {"task": "Prepare for interviews if offered", "priority": "medium"}
        ]
        
        # Spring Senior Year
        timeline[f"February-March {graduation_year}"] = [
            {"task": "Complete interviews", "priority": "high"},
            {"task": "Continue scholarship applications", "priority": "medium"},
            {"task": "Maintain grades and activities", "priority": "high"},
            {"task": "Wait for decisions (check portals regularly)", "priority": "medium"}
        ]
        
        timeline[f"April {graduation_year}"] = [
            {"task": "Review acceptance letters and financial aid packages", "priority": "high"},
            {"task": "Visit admitted student days", "priority": "high"},
            {"task": "Compare offers and make decision", "priority": "high"},
            {"task": "Submit deposit by May 1", "priority": "high"}
        ]
        
        return timeline
    
    def _get_key_deadlines(self, application_type: str, graduation_year: int) -> List[Dict[str, str]]:
        """Get key application deadlines"""
        senior_year = graduation_year - 1
        
        deadlines = []
        
        if application_type in ["early_action", "early_decision"]:
            deadlines.extend([
                {
                    "deadline": f"November 1, {senior_year}",
                    "type": "Early Action/Early Decision",
                    "description": "Most EA/ED deadlines"
                },
                {
                    "deadline": f"December 15, {senior_year}",
                    "type": "EA/ED Decisions",
                    "description": "Typical notification date"
                }
            ])
        
        deadlines.extend([
            {
                "deadline": f"October 31, {senior_year}",
                "type": "UC Applications",
                "description": "All UC schools"
            },
            {
                "deadline": f"January 1, {graduation_year}",
                "type": "Regular Decision",
                "description": "Most RD deadlines"
            },
            {
                "deadline": f"January 15, {graduation_year}",
                "type": "Late Regular Decision",
                "description": "Some schools have Jan 15 deadlines"
            },
            {
                "deadline": f"March 15-April 1, {graduation_year}",
                "type": "Decision Notifications",
                "description": "Most decisions released"
            },
            {
                "deadline": f"May 1, {graduation_year}",
                "type": "Enrollment Deposit",
                "description": "National Decision Day"
            }
        ])
        
        # Financial Aid deadlines
        deadlines.extend([
            {
                "deadline": f"October 1, {senior_year}",
                "type": "FAFSA Opens",
                "description": "File as early as possible"
            },
            {
                "deadline": f"November 1, {senior_year}",
                "type": "CSS Profile Priority",
                "description": "For early applicants"
            }
        ])
        
        return deadlines
    
    def _determine_current_phase(self, graduation_year: int, application_type: str) -> str:
        """Determine what phase the student is currently in"""
        current_date = datetime.now()
        current_month = current_date.month
        current_year = current_date.year
        senior_year = graduation_year - 1
        
        if current_year < senior_year - 1:
            return "early_preparation"
        elif current_year == senior_year - 1 and current_month >= 6:
            return "summer_before_senior"
        elif current_year == senior_year and current_month <= 10:
            return "early_application_season"
        elif current_year == senior_year and current_month <= 12:
            return "peak_application_season"
        elif current_year == graduation_year and current_month <= 4:
            return "waiting_for_decisions"
        elif current_year == graduation_year and current_month <= 6:
            return "final_decision_making"
        else:
            return "application_complete"
