"""
Student profile and academic record models
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import date


class AcademicRecord(BaseModel):
    """Student's academic performance data"""
    gpa: float = Field(..., ge=0.0, le=4.0, description="GPA on 4.0 scale")
    gpa_weighted: Optional[float] = Field(None, ge=0.0, le=5.0, description="Weighted GPA")
    class_rank: Optional[int] = Field(None, description="Class rank")
    class_size: Optional[int] = Field(None, description="Total students in class")
    
    # Standardized test scores
    sat_total: Optional[int] = Field(None, ge=400, le=1600, description="SAT total score")
    sat_math: Optional[int] = Field(None, ge=200, le=800, description="SAT Math")
    sat_ebrw: Optional[int] = Field(None, ge=200, le=800, description="SAT EBRW")
    
    act_composite: Optional[int] = Field(None, ge=1, le=36, description="ACT composite")
    
    # AP/IB courses
    ap_courses: List[str] = Field(default_factory=list, description="AP courses taken")
    ap_scores: Dict[str, int] = Field(default_factory=dict, description="AP exam scores")
    ib_diploma: bool = Field(default=False, description="Pursuing IB Diploma")
    
    # Relevant coursework
    cs_courses: List[str] = Field(default_factory=list, description="Computer Science courses")
    math_courses: List[str] = Field(default_factory=list, description="Math courses")
    engineering_courses: List[str] = Field(default_factory=list, description="Engineering courses")


class Extracurricular(BaseModel):
    """Single extracurricular activity"""
    name: str = Field(..., description="Activity name")
    category: str = Field(..., description="Category (e.g., STEM, Leadership, Arts)")
    role: Optional[str] = Field(None, description="Role or position")
    years_participated: int = Field(..., description="Years of participation")
    hours_per_week: Optional[int] = Field(None, description="Time commitment")
    achievements: List[str] = Field(default_factory=list, description="Notable achievements")
    description: Optional[str] = Field(None, description="Activity description")


class ResearchExperience(BaseModel):
    """Research or project experience"""
    title: str = Field(..., description="Project/research title")
    field: str = Field(..., description="Field of study")
    description: str = Field(..., description="Project description")
    duration_months: int = Field(..., description="Duration in months")
    mentor: Optional[str] = Field(None, description="Mentor or supervisor")
    outcome: Optional[str] = Field(None, description="Publications, awards, presentations")


class StudentProfile(BaseModel):
    """Complete student profile for college counseling"""
    
    # Basic Information
    student_id: Optional[str] = Field(None, description="Unique student identifier")
    name: str = Field(..., description="Student name")
    email: Optional[str] = Field(None, description="Contact email")
    graduation_year: int = Field(..., description="Expected high school graduation year")
    
    # Academic Record
    academic_record: AcademicRecord = Field(..., description="Academic performance data")
    
    # Interests and Goals
    cs_interests: List[str] = Field(
        default_factory=list,
        description="CS/Engineering interests (e.g., AI/ML, Robotics, Systems, Theory)"
    )
    career_goals: Optional[str] = Field(None, description="Long-term career aspirations")
    research_interests: Optional[str] = Field(None, description="Specific research interests")
    
    # Extracurriculars and Experience
    extracurriculars: List[Extracurricular] = Field(
        default_factory=list,
        description="Extracurricular activities"
    )
    research_experience: List[ResearchExperience] = Field(
        default_factory=list,
        description="Research and project experience"
    )
    
    # Additional Factors
    work_experience: List[str] = Field(default_factory=list, description="Work experience")
    awards_honors: List[str] = Field(default_factory=list, description="Awards and honors")
    leadership_positions: List[str] = Field(default_factory=list, description="Leadership roles")
    
    # Personal Context
    first_generation: bool = Field(default=False, description="First-generation college student")
    underrepresented_minority: bool = Field(default=False, description="URM status")
    geographic_preference: Optional[List[str]] = Field(None, description="Preferred regions/states")
    financial_need: Optional[str] = Field(None, description="Financial aid needs (high/medium/low)")
    
    # Application Strategy
    target_deadline: Optional[str] = Field(None, description="Target application deadline type")
    preferred_university_size: Optional[str] = Field(None, description="small/medium/large")
    preferred_location: Optional[str] = Field(None, description="urban/suburban/rural")
    
    # Notes
    counselor_notes: Optional[str] = Field(None, description="Counselor's private notes")
    student_essay_topics: List[str] = Field(default_factory=list, description="Essay topic ideas")
    
    def calculate_academic_index(self) -> float:
        """Calculate a simple academic strength index (0-100)"""
        score = 0.0
        
        # GPA component (40 points)
        score += (self.academic_record.gpa / 4.0) * 40
        
        # Test scores (30 points)
        if self.academic_record.sat_total:
            score += (self.academic_record.sat_total / 1600) * 30
        elif self.academic_record.act_composite:
            score += (self.academic_record.act_composite / 36) * 30
        
        # AP/IB courses (15 points)
        ap_count = len(self.academic_record.ap_courses)
        score += min(ap_count * 2, 15)
        
        # Class rank (15 points)
        if self.academic_record.class_rank and self.academic_record.class_size:
            percentile = 1 - (self.academic_record.class_rank / self.academic_record.class_size)
            score += percentile * 15
        
        return min(score, 100.0)
    
    def get_extracurricular_strength(self) -> str:
        """Assess extracurricular profile strength"""
        if not self.extracurriculars:
            return "needs_improvement"
        
        # Calculate based on number, duration, and leadership
        total_activities = len(self.extracurriculars)
        leadership_count = sum(1 for ec in self.extracurriculars 
                             if ec.role and any(term in ec.role.lower() 
                                              for term in ['president', 'captain', 'founder', 'leader']))
        
        avg_years = sum(ec.years_participated for ec in self.extracurriculars) / total_activities if total_activities > 0 else 0
        
        if total_activities >= 5 and leadership_count >= 2 and avg_years >= 2:
            return "exceptional"
        elif total_activities >= 3 and (leadership_count >= 1 or avg_years >= 2):
            return "strong"
        elif total_activities >= 2:
            return "moderate"
        else:
            return "needs_improvement"
    
    def has_research_experience(self) -> bool:
        """Check if student has meaningful research experience"""
        return len(self.research_experience) > 0
    
    def get_cs_profile_strength(self) -> str:
        """Assess CS-specific profile strength"""
        cs_indicators = 0
        
        # CS coursework
        if len(self.academic_record.cs_courses) >= 2:
            cs_indicators += 2
        elif len(self.academic_record.cs_courses) >= 1:
            cs_indicators += 1
        
        # CS-related AP exams
        cs_aps = [ap for ap in self.academic_record.ap_courses 
                 if 'Computer Science' in ap]
        if cs_aps:
            cs_indicators += 1
        
        # CS-related extracurriculars
        cs_ecs = [ec for ec in self.extracurriculars 
                 if any(term in ec.name.lower() or term in ec.category.lower()
                       for term in ['computer', 'programming', 'robotics', 'coding', 'software'])]
        if len(cs_ecs) >= 2:
            cs_indicators += 2
        elif len(cs_ecs) >= 1:
            cs_indicators += 1
        
        # Research experience in CS
        cs_research = [r for r in self.research_experience 
                      if any(term in r.field.lower() 
                            for term in ['computer', 'cs', 'ai', 'ml', 'software'])]
        if cs_research:
            cs_indicators += 2
        
        if cs_indicators >= 6:
            return "exceptional"
        elif cs_indicators >= 4:
            return "strong"
        elif cs_indicators >= 2:
            return "moderate"
        else:
            return "developing"
    
    def to_summary(self) -> str:
        """Generate a human-readable summary of the profile"""
        return f"""
Student Profile Summary: {self.name}
{'=' * 50}
Graduation Year: {self.graduation_year}
GPA: {self.academic_record.gpa} / 4.0
Academic Index: {self.calculate_academic_index():.1f}/100

Test Scores:
- SAT: {self.academic_record.sat_total or 'N/A'}
- ACT: {self.academic_record.act_composite or 'N/A'}

CS Interests: {', '.join(self.cs_interests) if self.cs_interests else 'N/A'}
Research Experience: {len(self.research_experience)} project(s)
Extracurricular Strength: {self.get_extracurricular_strength()}
CS Profile Strength: {self.get_cs_profile_strength()}
"""
