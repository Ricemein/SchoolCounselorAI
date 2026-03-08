"""
University matcher agent
"""
from typing import Dict, Any, List, Optional
from counselor_ai.agents.base_agent import BaseAgent
from counselor_ai.models.student import StudentProfile
from counselor_ai.knowledge.prompts import (
    UNIVERSITY_MATCHER_SYSTEM,
    UNIVERSITY_MATCH_PROMPT
)


class UniversityMatcherAgent(BaseAgent):
    """Agent specialized in matching students with universities"""
    
    def match_universities(
        self,
        student: StudentProfile,
        preferences: Optional[Dict[str, Any]] = None
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Match student with appropriate universities
        
        Args:
            student: Student profile
            preferences: Optional preferences dict
            
        Returns:
            Dictionary with reach, target, and safety recommendations
        """
        # Format student profile
        profile_text = self._format_student_profile(student)
        
        # Format preferences
        if preferences:
            pref_text = "\n".join([f"- {k}: {v}" for k, v in preferences.items()])
        else:
            pref_text = "No specific preferences provided"
            # Use student's stated preferences if available
            if student.geographic_preference:
                pref_text += f"\n- Geographic preference: {', '.join(student.geographic_preference)}"
            if student.preferred_university_size:
                pref_text += f"\n- University size: {student.preferred_university_size}"
            if student.preferred_location:
                pref_text += f"\n- Location type: {student.preferred_location}"
        
        # Generate AI recommendations
        prompt = UNIVERSITY_MATCH_PROMPT.format(
            student_profile=profile_text,
            preferences=pref_text
        )
        
        ai_recommendations = self.llm.generate_completion(
            prompt=prompt,
            system_prompt=UNIVERSITY_MATCHER_SYSTEM,
            temperature=0.7,
            max_tokens=3000
        )
        
        # Also provide structured recommendations
        structured_recs = self._generate_structured_recommendations(student)
        
        result = {
            "ai_recommendations": ai_recommendations,
            "structured_recommendations": structured_recs,
            "match_criteria": {
                "academic_index": student.calculate_academic_index(),
                "gpa": student.academic_record.gpa,
                "test_score": student.academic_record.sat_total or student.academic_record.act_composite,
                "cs_strength": student.get_cs_profile_strength()
            }
        }
        
        return result
    
    def _generate_structured_recommendations(self, student: StudentProfile) -> Dict[str, List[str]]:
        """Generate structured university recommendations based on profile"""
        
        academic_index = student.calculate_academic_index()
        gpa = student.academic_record.gpa
        sat = student.academic_record.sat_total
        
        reach_schools = []
        target_schools = []
        safety_schools = []
        
        # Top tier (most selective)
        if academic_index >= 90 and gpa >= 3.85:
            reach_schools.extend([
                "MIT",
                "Stanford University",
                "Carnegie Mellon University",
                "UC Berkeley"
            ])
            target_schools.extend([
                "University of Illinois Urbana-Champaign",
                "Georgia Institute of Technology",
                "University of Michigan",
                "University of Washington"
            ])
        
        # Very strong profile
        elif academic_index >= 80 and gpa >= 3.7:
            reach_schools.extend([
                "Carnegie Mellon University",
                "UC Berkeley",
                "University of Michigan",
                "Georgia Institute of Technology"
            ])
            target_schools.extend([
                "University of Illinois Urbana-Champaign",
                "University of Washington",
                "UT Austin",
                "University of Wisconsin-Madison",
                "University of Maryland"
            ])
            safety_schools.extend([
                "Purdue University",
                "Ohio State University"
            ])
        
        # Strong profile
        elif academic_index >= 70 and gpa >= 3.5:
            reach_schools.extend([
                "University of Illinois Urbana-Champaign",
                "University of Washington",
                "Georgia Institute of Technology"
            ])
            target_schools.extend([
                "University of Wisconsin-Madison",
                "University of Maryland",
                "Purdue University",
                "Penn State University",
                "University of Massachusetts Amherst"
            ])
            safety_schools.extend([
                "Ohio State University",
                "Rutgers University",
                "Virginia Tech"
            ])
        
        # Competitive profile
        else:
            reach_schools.extend([
                "University of Wisconsin-Madison",
                "Purdue University",
                "University of Maryland"
            ])
            target_schools.extend([
                "Penn State University",
                "Ohio State University",
                "Rutgers University",
                "Virginia Tech",
                "University of Massachusetts Amherst"
            ])
            safety_schools.extend([
                "Arizona State University",
                "University of Central Florida",
                "Iowa State University"
            ])
        
        return {
            "reach": reach_schools[:4],
            "target": target_schools[:5],
            "safety": safety_schools[:3]
        }
