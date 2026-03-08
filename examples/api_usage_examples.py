#!/usr/bin/env python3
"""
Example usage of the College Admissions AI Counselor API

This script demonstrates how to use the counselor AI programmatically
for integration into other systems or custom workflows.
"""

from counselor_ai import CounselorAgent, StudentProfile
from counselor_ai.models.student import AcademicRecord, Extracurricular, ResearchExperience
import json


def example_1_create_and_analyze_profile():
    """Example 1: Create a student profile and get analysis"""
    
    print("=" * 60)
    print("Example 1: Creating and Analyzing Student Profile")
    print("=" * 60)
    
    # Create academic record
    academic_record = AcademicRecord(
        gpa=3.9,
        gpa_weighted=4.3,
        sat_total=1520,
        sat_math=790,
        sat_ebrw=730,
        ap_courses=[
            "AP Computer Science A",
            "AP Calculus BC",
            "AP Physics C"
        ],
        ap_scores={
            "AP Computer Science A": 5,
            "AP Calculus BC": 5
        },
        cs_courses=["AP CS A", "Data Structures", "Algorithms"]
    )
    
    # Create extracurricular activities
    robotics = Extracurricular(
        name="FIRST Robotics",
        category="STEM",
        role="Programming Lead",
        years_participated=3,
        hours_per_week=12,
        achievements=["Regional Champions", "State Qualifier"]
    )
    
    cs_club = Extracurricular(
        name="Computer Science Club",
        category="STEM",
        role="President",
        years_participated=2,
        hours_per_week=4,
        achievements=["Founded club", "Organized school hackathon"]
    )
    
    # Create research experience
    research = ResearchExperience(
        title="Machine Learning for Medical Image Analysis",
        field="Computer Science - AI/ML",
        description="Developed CNN model for detecting anomalies in X-ray images",
        duration_months=8,
        mentor="Dr. Jane Smith, University CS Department",
        outcome="Published in undergraduate research journal, presented at conference"
    )
    
    # Create complete student profile
    student = StudentProfile(
        name="Jane Doe",
        graduation_year=2025,
        academic_record=academic_record,
        cs_interests=["Artificial Intelligence", "Machine Learning", "Healthcare Technology"],
        career_goals="Pursuing PhD in AI with focus on healthcare applications",
        extracurriculars=[robotics, cs_club],
        research_experience=[research],
        awards_honors=[
            "National Merit Finalist",
            "USACO Gold Division",
            "Science Fair Regional Winner"
        ],
        first_generation=True
    )
    
    # Initialize the counselor agent
    agent = CounselorAgent()
    
    # Get profile analysis
    analysis = agent.analyze_student_profile(student)
    
    print(f"\nStudent: {student.name}")
    print(f"Academic Index: {analysis['objective_metrics']['academic_index']:.1f}/100")
    print(f"CS Profile Strength: {analysis['objective_metrics']['cs_profile_strength']}")
    print(f"\nQuick Summary:\n{analysis['quick_summary']}")
    
    return student, agent


def example_2_get_university_recommendations(student, agent):
    """Example 2: Get university recommendations"""
    
    print("\n" + "=" * 60)
    print("Example 2: Getting University Recommendations")
    print("=" * 60)
    
    # Get recommendations
    recommendations = agent.get_university_recommendations(
        student,
        preferences={
            "regions": ["Northeast", "West Coast"],
            "size_preference": "medium to large",
            "research_focus": True
        }
    )
    
    structured = recommendations["structured_recommendations"]
    
    print("\nREACH SCHOOLS:")
    for school in structured["reach"]:
        print(f"  • {school}")
    
    print("\nTARGET SCHOOLS:")
    for school in structured["target"]:
        print(f"  • {school}")
    
    print("\nSAFETY SCHOOLS:")
    for school in structured["safety"]:
        print(f"  • {school}")
    
    return structured


def example_3_application_timeline(student, agent):
    """Example 3: Create application timeline"""
    
    print("\n" + "=" * 60)
    print("Example 3: Creating Application Timeline")
    print("=" * 60)
    
    target_universities = [
        "MIT",
        "Stanford",
        "Carnegie Mellon",
        "UC Berkeley",
        "Georgia Tech"
    ]
    
    timeline = agent.create_application_timeline(
        student=student,
        target_universities=target_universities,
        application_type="regular_decision"
    )
    
    print(f"\nCurrent Phase: {timeline['current_phase']}")
    print("\nKey Deadlines:")
    for deadline in timeline['key_deadlines'][:5]:
        print(f"  • {deadline['deadline']}: {deadline['type']}")
    
    return timeline


def example_4_essay_feedback(student, agent):
    """Example 4: Get essay feedback"""
    
    print("\n" + "=" * 60)
    print("Example 4: Getting Essay Feedback")
    print("=" * 60)
    
    # Sample essay (shortened for example)
    sample_essay = """
    As I watched the robot I'd spent months programming crash into the wall for 
    the fifteenth time, I realized that failure isn't the opposite of success—it's 
    part of the process. My journey with FIRST Robotics taught me that the most 
    valuable lessons come not from perfect code, but from debugging the broken parts.
    
    What started as a simple interest in programming grew into a passion for AI and 
    machine learning when I began my research project on medical image analysis...
    """
    
    feedback = agent.analyze_essay(
        student=student,
        essay_content=sample_essay,
        essay_type="personal_statement"
    )
    
    print(f"\nWord Count: {feedback['word_count']}")
    print(f"Recommended Length: {feedback['recommended_length']}")
    
    quick_checks = feedback['quick_checks']
    print("\nQuick Checks:")
    print(f"  • Uses specific examples: {quick_checks['has_specific_examples']}")
    print(f"  • Avoids clichés: {quick_checks['avoids_cliches']}")
    print(f"  • Shows rather than tells: {quick_checks['shows_not_tells']}")
    
    return feedback


def example_5_research_opportunities(student, agent):
    """Example 5: Find research opportunities"""
    
    print("\n" + "=" * 60)
    print("Example 5: Finding Research Opportunities")
    print("=" * 60)
    
    opportunities = agent.get_research_opportunities(
        student=student,
        research_interests=["AI/ML", "Computer Vision", "Healthcare AI"],
        target_universities=["MIT", "Stanford", "CMU"]
    )
    
    print("\nSummer Programs (first 3):")
    for program in opportunities['structured_opportunities']['summer_programs'][:3]:
        print(f"  • {program['name']}")
        print(f"    {program['description']}")
    
    print("\nPreparation Tips:")
    for tip in opportunities['preparation_tips'][:3]:
        print(f"  • {tip}")
    
    return opportunities


def example_6_save_to_file():
    """Example 6: Save results to file"""
    
    print("\n" + "=" * 60)
    print("Example 6: Saving Results to File")
    print("=" * 60)
    
    # Create simple profile
    academic_record = AcademicRecord(
        gpa=3.7,
        sat_total=1400,
        ap_courses=["AP CS A"],
        cs_courses=["AP CS A"]
    )
    
    student = StudentProfile(
        name="John Smith",
        graduation_year=2025,
        academic_record=academic_record,
        cs_interests=["Software Engineering"]
    )
    
    agent = CounselorAgent()
    
    # Get comprehensive consultation
    result = agent.comprehensive_consultation(student)
    
    # Save to file
    output_file = "data/reports/john_smith_consultation.json"
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2, default=str)
    
    print(f"\n✓ Saved comprehensive consultation to {output_file}")


def main():
    """Run all examples"""
    
    print("\n" + "=" * 60)
    print("College Admissions AI Counselor - API Examples")
    print("=" * 60)
    
    # Run examples
    student, agent = example_1_create_and_analyze_profile()
    
    example_2_get_university_recommendations(student, agent)
    
    example_3_application_timeline(student, agent)
    
    example_4_essay_feedback(student, agent)
    
    example_5_research_opportunities(student, agent)
    
    example_6_save_to_file()
    
    print("\n" + "=" * 60)
    print("All examples completed successfully!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
