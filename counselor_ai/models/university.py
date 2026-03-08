"""
University and program models
"""
from typing import List, Optional, Dict
from pydantic import BaseModel, Field


class AdmissionStatistics(BaseModel):
    """Admission statistics for a university"""
    acceptance_rate: float = Field(..., ge=0.0, le=1.0, description="Overall acceptance rate")
    cs_acceptance_rate: Optional[float] = Field(None, description="CS program acceptance rate")
    
    avg_gpa: float = Field(..., description="Average admitted student GPA")
    gpa_25th: float = Field(..., description="25th percentile GPA")
    gpa_75th: float = Field(..., description="75th percentile GPA")
    
    sat_avg: Optional[int] = Field(None, description="Average SAT score")
    sat_25th: Optional[int] = Field(None, description="25th percentile SAT")
    sat_75th: Optional[int] = Field(None, description="75th percentile SAT")
    
    act_avg: Optional[int] = Field(None, description="Average ACT score")
    act_25th: Optional[int] = Field(None, description="25th percentile ACT")
    act_75th: Optional[int] = Field(None, description="75th percentile ACT")


class Program(BaseModel):
    """CS/Engineering program details"""
    name: str = Field(..., description="Program name")
    degree_types: List[str] = Field(..., description="BS, BA, BS/MS, etc.")
    specializations: List[str] = Field(default_factory=list, description="Available specializations")
    
    # Program characteristics
    research_opportunities: bool = Field(default=True, description="Undergraduate research available")
    coop_internship: bool = Field(default=False, description="Co-op or internship program")
    study_abroad: bool = Field(default=False, description="Study abroad options")
    
    # Faculty and resources
    notable_faculty: List[str] = Field(default_factory=list, description="Notable faculty members")
    research_areas: List[str] = Field(default_factory=list, description="Key research areas")
    labs_centers: List[str] = Field(default_factory=list, description="Research labs and centers")
    
    # Rankings
    us_news_ranking: Optional[int] = Field(None, description="US News CS ranking")
    qs_ranking: Optional[int] = Field(None, description="QS World ranking")


class University(BaseModel):
    """University information"""
    
    # Basic Information
    name: str = Field(..., description="University name")
    location: str = Field(..., description="City, State")
    region: str = Field(..., description="Geographic region")
    
    # Institution Type
    institution_type: str = Field(..., description="public/private")
    size: str = Field(..., description="small/medium/large")
    setting: str = Field(..., description="urban/suburban/rural")
    
    # Programs
    cs_program: Program = Field(..., description="Computer Science program details")
    has_engineering_school: bool = Field(default=True, description="Has engineering school")
    engineering_programs: List[str] = Field(default_factory=list, description="Engineering majors")
    
    # Admissions
    admission_stats: AdmissionStatistics = Field(..., description="Admission statistics")
    application_deadlines: Dict[str, str] = Field(
        default_factory=dict,
        description="Deadlines (early_action, early_decision, regular)"
    )
    
    # Financial
    tuition_in_state: Optional[int] = Field(None, description="In-state tuition")
    tuition_out_state: Optional[int] = Field(None, description="Out-of-state tuition")
    financial_aid_available: bool = Field(default=True, description="Financial aid available")
    merit_scholarships: bool = Field(default=False, description="Merit scholarships available")
    meets_full_need: bool = Field(default=False, description="Meets 100% demonstrated need")
    
    # Student Life
    total_undergrad: int = Field(..., description="Total undergraduate enrollment")
    student_faculty_ratio: str = Field(..., description="Student to faculty ratio")
    
    # Additional Info
    notable_alumni: List[str] = Field(default_factory=list, description="Notable alumni in tech")
    career_outcomes: Dict[str, any] = Field(default_factory=dict, description="Career statistics")
    
    # Requirements
    requires_sat_act: bool = Field(default=False, description="Test-optional status")
    common_app: bool = Field(default=True, description="Uses Common Application")
    coalition_app: bool = Field(default=False, description="Uses Coalition Application")
    supplemental_essays: int = Field(default=0, description="Number of supplemental essays")
    
    # Special Notes
    special_programs: List[str] = Field(default_factory=list, description="Special programs or distinctions")
    website: Optional[str] = Field(None, description="University website")
    
    def calculate_match_score(self, student_gpa: float, student_test_score: Optional[int], 
                             score_type: str = "sat") -> Dict[str, any]:
        """
        Calculate how well the student matches with this university
        Returns match type and probability estimate
        """
        stats = self.admission_stats
        
        # GPA comparison
        gpa_score = 0
        if student_gpa >= stats.gpa_75th:
            gpa_score = 3  # Above 75th percentile
        elif student_gpa >= stats.avg_gpa:
            gpa_score = 2  # Above average
        elif student_gpa >= stats.gpa_25th:
            gpa_score = 1  # Within range
        else:
            gpa_score = 0  # Below range
        
        # Test score comparison
        test_score = 1  # Default neutral if no test scores
        if student_test_score:
            if score_type == "sat":
                if stats.sat_75th and student_test_score >= stats.sat_75th:
                    test_score = 3
                elif stats.sat_avg and student_test_score >= stats.sat_avg:
                    test_score = 2
                elif stats.sat_25th and student_test_score >= stats.sat_25th:
                    test_score = 1
                else:
                    test_score = 0
            elif score_type == "act":
                if stats.act_75th and student_test_score >= stats.act_75th:
                    test_score = 3
                elif stats.act_avg and student_test_score >= stats.act_avg:
                    test_score = 2
                elif stats.act_25th and student_test_score >= stats.act_25th:
                    test_score = 1
                else:
                    test_score = 0
        
        # Combined score
        combined_score = (gpa_score + test_score) / 6.0  # Normalize to 0-1
        
        # Determine match category
        if combined_score >= 0.75:
            match_type = "target"
            probability = "40-60%"
        elif combined_score >= 0.5:
            match_type = "target"
            probability = "30-50%"
        elif combined_score >= 0.33:
            match_type = "reach"
            probability = "10-30%"
        else:
            match_type = "high_reach"
            probability = "<10%"
        
        # Adjust for highly selective schools
        if stats.acceptance_rate < 0.15:
            if match_type == "target":
                match_type = "reach"
            elif match_type == "reach":
                match_type = "high_reach"
        
        # Check if it could be a safety
        if combined_score >= 0.85 and stats.acceptance_rate > 0.40:
            match_type = "safety"
            probability = ">70%"
        
        return {
            "university": self.name,
            "match_type": match_type,
            "probability_range": probability,
            "acceptance_rate": stats.acceptance_rate,
            "gpa_comparison": "strong" if gpa_score >= 2 else "competitive" if gpa_score == 1 else "below_range",
            "test_comparison": "strong" if test_score >= 2 else "competitive" if test_score == 1 else "below_range"
        }
    
    def get_program_strengths(self) -> List[str]:
        """Return list of program strengths"""
        strengths = []
        
        if self.cs_program.us_news_ranking and self.cs_program.us_news_ranking <= 20:
            strengths.append("Top 20 CS Program")
        
        if len(self.cs_program.research_areas) >= 5:
            strengths.append("Comprehensive Research Areas")
        
        if self.cs_program.coop_internship:
            strengths.append("Co-op/Internship Program")
        
        if self.meets_full_need:
            strengths.append("Meets 100% Financial Need")
        
        if len(self.cs_program.specializations) >= 4:
            strengths.append("Diverse Specializations")
        
        return strengths
