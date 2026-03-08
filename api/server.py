"""
FastAPI server for College Admissions AI Counselor
Provides REST API endpoints for the web application
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from counselor_ai import CounselorAgent
from counselor_ai.models.student import StudentProfile, AcademicRecord, Extracurricular
from counselor_ai.models.university import University

app = FastAPI(
    title="College Admissions AI Counselor API",
    description="AI-powered college counseling for CS/Engineering programs",
    version="1.0.0"
)

# CORS configuration for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the counselor agent
counselor = None

def get_counselor():
    """Get or create counselor agent instance"""
    global counselor
    if counselor is None:
        counselor = CounselorAgent()
    return counselor


# Request/Response Models
class AcademicRecordRequest(BaseModel):
    gpa: float = Field(..., ge=0.0, le=4.0, description="GPA on 4.0 scale")
    sat_total: Optional[int] = Field(None, ge=400, le=1600, description="SAT total score")
    sat_math: Optional[int] = Field(None, ge=200, le=800, description="SAT Math")
    sat_verbal: Optional[int] = Field(None, ge=200, le=800, description="SAT Verbal")
    act_composite: Optional[int] = Field(None, ge=1, le=36, description="ACT composite")
    ap_courses: List[str] = Field(default_factory=list, description="List of AP courses")
    honors_courses: List[str] = Field(default_factory=list, description="List of honors courses")

class ExtracurricularRequest(BaseModel):
    name: str
    category: str
    years_involved: int
    leadership_role: Optional[str] = None
    description: Optional[str] = None
    hours_per_week: Optional[int] = None

class StudentProfileRequest(BaseModel):
    name: str
    email: Optional[str] = None
    graduation_year: int
    academic_record: AcademicRecordRequest
    cs_interests: List[str] = Field(default_factory=list)
    extracurriculars: List[ExtracurricularRequest] = Field(default_factory=list)
    target_programs: List[str] = Field(default_factory=list)

class EssayRequest(BaseModel):
    essay_text: str = Field(..., min_length=50, description="Essay text to analyze")
    essay_prompt: Optional[str] = Field(None, description="Essay prompt/question")

class UniversitySearchRequest(BaseModel):
    student_profile: StudentProfileRequest
    preferences: Optional[Dict[str, Any]] = Field(default_factory=dict)

# Health Check
@app.get("/")
async def root():
    """API health check"""
    return {
        "status": "healthy",
        "service": "College Admissions AI Counselor",
        "version": "1.0.0"
    }

@app.get("/api/health")
async def health_check():
    """Detailed health check"""
    try:
        agent = get_counselor()
        return {
            "status": "healthy",
            "llm_status": "configured",
            "agents": ["profile_analyzer", "university_matcher", "essay_coach", "timeline_manager", "research_advisor"]
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }


# Student Profile Analysis
@app.post("/api/analyze-profile")
async def analyze_profile(student_request: StudentProfileRequest):
    """
    Analyze a student's profile and provide comprehensive counseling insights
    """
    try:
        agent = get_counselor()
        
        # Convert request to StudentProfile
        academic_record = AcademicRecord(**student_request.academic_record.dict())
        extracurriculars = [
            Extracurricular(**ec.dict()) 
            for ec in student_request.extracurriculars
        ]
        
        student = StudentProfile(
            name=student_request.name,
            email=student_request.email,
            graduation_year=student_request.graduation_year,
            academic_record=academic_record,
            cs_interests=student_request.cs_interests,
            extracurriculars=extracurriculars,
            target_programs=student_request.target_programs
        )
        
        # Get analysis
        analysis = agent.analyze_student_profile(student)
        
        return {
            "success": True,
            "student_name": student.name,
            "analysis": analysis
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# University Matching
@app.post("/api/match-universities")
async def match_universities(request: UniversitySearchRequest):
    """
    Find and rank universities that match the student's profile
    """
    try:
        agent = get_counselor()
        
        # Convert request to StudentProfile
        academic_record = AcademicRecord(**request.student_profile.academic_record.dict())
        extracurriculars = [
            Extracurricular(**ec.dict()) 
            for ec in request.student_profile.extracurriculars
        ]
        
        student = StudentProfile(
            name=request.student_profile.name,
            email=request.student_profile.email,
            graduation_year=request.student_profile.graduation_year,
            academic_record=academic_record,
            cs_interests=request.student_profile.cs_interests,
            extracurriculars=extracurriculars,
            target_programs=request.student_profile.target_programs
        )
        
        # Get university matches
        matches = agent.match_universities(student, request.preferences)
        
        return {
            "success": True,
            "student_name": student.name,
            "matches": matches
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Essay Analysis
@app.post("/api/analyze-essay")
async def analyze_essay(essay_request: EssayRequest):
    """
    Analyze an essay and provide feedback
    """
    try:
        agent = get_counselor()
        
        feedback = agent.analyze_essay(
            essay_request.essay_text,
            essay_request.essay_prompt
        )
        
        return {
            "success": True,
            "feedback": feedback
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Essay Topic Suggestions
@app.post("/api/suggest-essay-topics")
async def suggest_essay_topics(student_request: StudentProfileRequest):
    """
    Suggest essay topics based on student profile
    """
    try:
        agent = get_counselor()
        
        # Convert request to StudentProfile
        academic_record = AcademicRecord(**student_request.academic_record.dict())
        extracurriculars = [
            Extracurricular(**ec.dict()) 
            for ec in student_request.extracurriculars
        ]
        
        student = StudentProfile(
            name=student_request.name,
            email=student_request.email,
            graduation_year=student_request.graduation_year,
            academic_record=academic_record,
            cs_interests=student_request.cs_interests,
            extracurriculars=extracurriculars,
            target_programs=student_request.target_programs
        )
        
        suggestions = agent.suggest_essay_topics(student)
        
        return {
            "success": True,
            "student_name": student.name,
            "suggestions": suggestions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Application Timeline
@app.post("/api/generate-timeline")
async def generate_timeline(student_request: StudentProfileRequest):
    """
    Generate a personalized application timeline
    """
    try:
        agent = get_counselor()
        
        # Convert request to StudentProfile
        academic_record = AcademicRecord(**student_request.academic_record.dict())
        extracurriculars = [
            Extracurricular(**ec.dict()) 
            for ec in student_request.extracurriculars
        ]
        
        student = StudentProfile(
            name=student_request.name,
            email=student_request.email,
            graduation_year=student_request.graduation_year,
            academic_record=academic_record,
            cs_interests=student_request.cs_interests,
            extracurriculars=extracurriculars,
            target_programs=student_request.target_programs
        )
        
        timeline = agent.create_application_timeline(student)
        
        return {
            "success": True,
            "student_name": student.name,
            "timeline": timeline
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Research Opportunities
@app.post("/api/find-research-opportunities")
async def find_research_opportunities(student_request: StudentProfileRequest):
    """
    Find research opportunities matching student interests
    """
    try:
        agent = get_counselor()
        
        # Convert request to StudentProfile
        academic_record = AcademicRecord(**student_request.academic_record.dict())
        extracurriculars = [
            Extracurricular(**ec.dict()) 
            for ec in student_request.extracurriculars
        ]
        
        student = StudentProfile(
            name=student_request.name,
            email=student_request.email,
            graduation_year=student_request.graduation_year,
            academic_record=academic_record,
            cs_interests=student_request.cs_interests,
            extracurriculars=extracurriculars,
            target_programs=student_request.target_programs
        )
        
        opportunities = agent.find_research_opportunities(student)
        
        return {
            "success": True,
            "student_name": student.name,
            "opportunities": opportunities
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get Available Universities
@app.get("/api/universities")
async def get_universities():
    """
    Get list of all universities in the knowledge base
    """
    try:
        from counselor_ai.knowledge.universities import get_all_universities
        universities = get_all_universities()
        return {
            "success": True,
            "count": len(universities),
            "universities": [u.dict() for u in universities]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
