#!/usr/bin/env python3
"""
College Admissions AI Counselor - Main Entry Point
"""
import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich import print as rprint

from counselor_ai import CounselorAgent, StudentProfile
from counselor_ai.models.student import AcademicRecord


console = Console()


def load_student_profile(file_path: str) -> StudentProfile:
    """Load student profile from JSON file"""
    with open(file_path, 'r') as f:
        data = json.load(f)
    return StudentProfile(**data)


def save_report(content: dict, output_file: str):
    """Save report to file"""
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(content, f, indent=2, default=str)
    
    console.print(f"[green]✓ Report saved to {output_file}[/green]")


def run_profile_analysis(agent: CounselorAgent, student: StudentProfile, output: Optional[str] = None):
    """Run profile analysis"""
    console.print("\n[bold cyan]Analyzing Student Profile...[/bold cyan]\n")
    
    result = agent.analyze_student_profile(student)
    
    # Display quick summary
    console.print(Panel(result["quick_summary"], title="Quick Summary", border_style="green"))
    
    # Display metrics
    console.print("\n[bold]Objective Metrics:[/bold]")
    metrics = result["objective_metrics"]
    console.print(f"  Academic Index: {metrics['academic_index']}/100")
    console.print(f"  GPA: {metrics['gpa']}/4.0")
    console.print(f"  SAT: {metrics['test_scores']['sat'] or 'N/A'}")
    console.print(f"  Extracurricular Strength: {metrics['extracurricular_strength']}")
    console.print(f"  CS Profile Strength: {metrics['cs_profile_strength']}")
    console.print(f"  Research Experience: {'Yes' if metrics['has_research_experience'] else 'No'}")
    
    # Display AI analysis
    console.print("\n[bold]AI Analysis:[/bold]\n")
    console.print(Markdown(result["ai_analysis"]))
    
    if output:
        save_report(result, output)


def run_university_matching(agent: CounselorAgent, student: StudentProfile, output: Optional[str] = None):
    """Run university matching"""
    console.print("\n[bold cyan]Finding University Matches...[/bold cyan]\n")
    
    result = agent.get_university_recommendations(student)
    
    # Display structured recommendations
    structured = result["structured_recommendations"]
    
    console.print("[bold red]Reach Schools:[/bold red]")
    for school in structured["reach"]:
        console.print(f"  • {school}")
    
    console.print("\n[bold yellow]Target Schools:[/bold yellow]")
    for school in structured["target"]:
        console.print(f"  • {school}")
    
    console.print("\n[bold green]Safety Schools:[/bold green]")
    for school in structured["safety"]:
        console.print(f"  • {school}")
    
    # Display AI recommendations
    console.print("\n[bold]Detailed AI Recommendations:[/bold]\n")
    console.print(Markdown(result["ai_recommendations"]))
    
    if output:
        save_report(result, output)


def run_comprehensive_consultation(agent: CounselorAgent, student: StudentProfile, output: Optional[str] = None):
    """Run comprehensive consultation"""
    console.print("\n[bold cyan]Running Comprehensive Consultation...[/bold cyan]\n")
    
    result = agent.comprehensive_consultation(student)
    
    # Display profile analysis
    console.print("[bold]1. Profile Analysis[/bold]")
    console.print(Panel(result["profile_analysis"]["quick_summary"], border_style="blue"))
    
    # Display university recommendations
    console.print("\n[bold]2. University Recommendations[/bold]")
    structured = result["university_recommendations"]["structured_recommendations"]
    console.print(f"  Reach: {', '.join(structured['reach'][:3])}")
    console.print(f"  Target: {', '.join(structured['target'][:3])}")
    console.print(f"  Safety: {', '.join(structured['safety'][:2])}")
    
    # Display next steps
    console.print("\n[bold]3. Recommended Next Steps[/bold]")
    for i, step in enumerate(result["recommended_next_steps"], 1):
        console.print(f"  {i}. {step}")
    
    if output:
        save_report(result, output)


def interactive_mode():
    """Interactive mode for counselor"""
    console.print("\n[bold cyan]College Admissions AI Counselor - Interactive Mode[/bold cyan]\n")
    
    # Quick student profile creation
    console.print("[bold]Create Student Profile[/bold]\n")
    
    name = console.input("Student name: ")
    graduation_year = int(console.input("Graduation year: "))
    gpa = float(console.input("GPA (0-4.0): "))
    
    sat_input = console.input("SAT score (or press Enter to skip): ")
    sat_score = int(sat_input) if sat_input else None
    
    cs_interests = console.input("CS interests (comma-separated): ").split(",")
    cs_interests = [i.strip() for i in cs_interests if i.strip()]
    
    # Create student profile
    academic_record = AcademicRecord(
        gpa=gpa,
        sat_total=sat_score,
        ap_courses=[],
        cs_courses=[]
    )
    
    student = StudentProfile(
        name=name,
        graduation_year=graduation_year,
        academic_record=academic_record,
        cs_interests=cs_interests
    )
    
    # Initialize agent
    console.print("\n[dim]Initializing AI counselor...[/dim]")
    agent = CounselorAgent()
    
    # Main menu
    while True:
        console.print("\n[bold]What would you like to do?[/bold]")
        console.print("1. Analyze student profile")
        console.print("2. Get university recommendations")
        console.print("3. Get comprehensive consultation")
        console.print("4. Exit")
        
        choice = console.input("\nEnter choice (1-4): ")
        
        if choice == "1":
            run_profile_analysis(agent, student)
        elif choice == "2":
            run_university_matching(agent, student)
        elif choice == "3":
            run_comprehensive_consultation(agent, student)
        elif choice == "4":
            console.print("\n[green]Thank you for using College Admissions AI Counselor![/green]")
            break
        else:
            console.print("[red]Invalid choice. Please try again.[/red]")


def main():
    parser = argparse.ArgumentParser(
        description="College Admissions AI Counselor for CS/Engineering Programs"
    )
    
    parser.add_argument(
        "--agent",
        choices=["profile-analyzer", "university-matcher", "comprehensive"],
        help="Specific agent to run"
    )
    
    parser.add_argument(
        "--student",
        type=str,
        help="Path to student profile JSON file"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        help="Output file for report"
    )
    
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive mode"
    )
    
    args = parser.parse_args()
    
    # Interactive mode
    if args.interactive:
        interactive_mode()
        return
    
    # Check for required arguments
    if not args.agent or not args.student:
        console.print("[yellow]Starting in interactive mode (use --help for other options)[/yellow]")
        interactive_mode()
        return
    
    # Load student profile
    try:
        student = load_student_profile(args.student)
    except FileNotFoundError:
        console.print(f"[red]Error: Student file not found: {args.student}[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error loading student profile: {e}[/red]")
        sys.exit(1)
    
    # Initialize agent
    console.print("[dim]Initializing AI counselor...[/dim]")
    agent = CounselorAgent()
    
    # Run specified agent
    if args.agent == "profile-analyzer":
        run_profile_analysis(agent, student, args.output)
    elif args.agent == "university-matcher":
        run_university_matching(agent, student, args.output)
    elif args.agent == "comprehensive":
        run_comprehensive_consultation(agent, student, args.output)


if __name__ == "__main__":
    main()
