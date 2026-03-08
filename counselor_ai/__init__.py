"""
College Admissions AI Counselor Package
"""

__version__ = "1.0.0"

from counselor_ai.models.student import StudentProfile, AcademicRecord
from counselor_ai.models.university import University, Program
from counselor_ai.agents.base_agent import CounselorAgent

__all__ = [
    "StudentProfile",
    "AcademicRecord",
    "University",
    "Program",
    "CounselorAgent",
]
