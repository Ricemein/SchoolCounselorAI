#!/usr/bin/env python3
"""
Example: Using Local LLM Models (No API Key Required)

This example shows how to use local models like TinyLlama
instead of OpenAI API, removing the need for API keys.
"""

from counselor_ai import CounselorAgent, StudentProfile
from counselor_ai.models.student import AcademicRecord
import os

# Force use of local model
os.environ['USE_LOCAL_MODEL'] = 'true'
os.environ['LOCAL_MODEL'] = 'TinyLlama/TinyLlama-1.1B-Chat-v1.0'

print("=" * 60)
print("Local LLM Example - No API Key Required!")
print("=" * 60)

# Create student profile
academic_record = AcademicRecord(
    gpa=3.7,
    sat_total=1400,
    ap_courses=["AP Computer Science A", "AP Calculus AB"],
    cs_courses=["AP CS A", "Intro to Programming"]
)

student = StudentProfile(
    name="Alex Smith",
    graduation_year=2025,
    academic_record=academic_record,
    cs_interests=["Software Engineering", "Web Development"]
)

print(f"\nStudent: {student.name}")
print(f"GPA: {student.academic_record.gpa}")
print(f"SAT: {student.academic_record.sat_total}")
print(f"Interests: {', '.join(student.cs_interests)}")

print("\n" + "=" * 60)
print("Initializing Local Model (this may take a few minutes)...")
print("=" * 60)

# Initialize agent with local model
agent = CounselorAgent()

print("\n" + "=" * 60)
print("Analyzing Student Profile...")
print("=" * 60)

# Get basic metrics (no LLM needed)
academic_index = student.calculate_academic_index()
cs_strength = student.get_cs_profile_strength()

print(f"\nAcademic Index: {academic_index:.1f}/100")
print(f"CS Profile Strength: {cs_strength}")

# Get AI-powered analysis (uses local model)
print("\nGenerating AI Analysis (using local TinyLlama model)...")
try:
    analysis = agent.analyze_student_profile(student)
    print("\n" + "=" * 60)
    print("Profile Analysis Complete!")
    print("=" * 60)
    print(f"\n{analysis['quick_summary']}")
    
except Exception as e:
    print(f"\nError during analysis: {e}")
    print("\nNote: Local models may require significant memory.")
    print("If you encounter errors, try:")
    print("  1. Using a smaller model")
    print("  2. Closing other applications")
    print("  3. Using OpenAI API instead (set USE_LOCAL_MODEL=false)")

print("\n" + "=" * 60)
print("Example Complete!")
print("=" * 60)

print("\nBenefits of Local Models:")
print("  ✓ No API key required")
print("  ✓ No usage costs")
print("  ✓ Complete privacy (data stays local)")
print("  ✓ Works offline")

print("\nTrade-offs:")
print("  ✗ Requires more RAM/disk space")
print("  ✗ Slower on CPU (faster with GPU)")
print("  ✗ May produce less accurate results than GPT-4")

print("\nSupported Models:")
print("  • TinyLlama/TinyLlama-1.1B-Chat-v1.0 (default, ~2GB)")
print("  • microsoft/phi-2 (~5GB)")
print("  • meta-llama/Llama-2-7b-chat-hf (~13GB)")
print("  • Any HuggingFace chat model")

print("\nTo switch models, edit .env:")
print("  LOCAL_MODEL=microsoft/phi-2")
