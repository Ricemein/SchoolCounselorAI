# College Admissions AI Counselor

An intelligent AI agent system designed to help school counselors guide students through the college admissions process for Computer Science and Engineering programs at top research universities.

## Features

- **Personalized Student Profiling**: Analyze student academic records, test scores, extracurriculars, and interests
- **University Matching**: AI-powered recommendations for CS/Engineering programs based on student profile
- **Application Timeline Management**: Track deadlines, requirements, and milestones
- **Essay Guidance**: AI-assisted feedback on college essays and personal statements
- **Interview Preparation**: Mock interview questions and tips specific to CS/Engineering programs
- **Financial Aid Analysis**: Scholarship opportunities and financial planning
- **Holistic Evaluation**: Consider research interests, career goals, and university culture fit

## Architecture

The application uses an **agentic AI architecture** with specialized agents:
- **Profile Analyzer Agent**: Evaluates student credentials and strengths
- **University Matcher Agent**: Recommends suitable programs and schools
- **Timeline Manager Agent**: Tracks application deadlines and requirements
- **Essay Coach Agent**: Provides writing guidance and feedback
- **Research Advisor Agent**: Matches students with research opportunities

## Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env and add your API keys
```

## Configuration

Add your API keys to `.env`:
```
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key  # Optional
```

## Usage

### Command Line Interface

```bash
# Start the counselor assistant
python main.py

# Run specific agent
python main.py --agent profile-analyzer --student data/students/john_doe.json

# Generate university recommendations
python main.py --agent university-matcher --student data/students/john_doe.json

# Interactive mode
python main.py --interactive
```

### Python API

```python
from counselor_ai import CounselorAgent, StudentProfile

# Initialize the agent
agent = CounselorAgent()

# Create student profile
student = StudentProfile(
    name="Jane Smith",
    gpa=3.9,
    sat_score=1520,
    interests=["AI/ML", "Robotics"],
    extracurriculars=["Robotics Club Captain", "Math Olympiad"]
)

# Get recommendations
recommendations = agent.get_university_recommendations(student)

# Get application timeline
timeline = agent.create_application_timeline(student, target_universities=recommendations[:5])

# Get essay feedback
essay_feedback = agent.analyze_essay(student, essay_text, essay_type="personal_statement")
```

## Project Structure

```
.
├── main.py                     # Entry point
├── counselor_ai/
│   ├── __init__.py
│   ├── agents/                 # AI agent implementations
│   │   ├── __init__.py
│   │   ├── base_agent.py
│   │   ├── profile_analyzer.py
│   │   ├── university_matcher.py
│   │   ├── timeline_manager.py
│   │   ├── essay_coach.py
│   │   └── research_advisor.py
│   ├── models/                 # Data models
│   │   ├── __init__.py
│   │   ├── student.py
│   │   └── university.py
│   ├── knowledge/              # Knowledge bases
│   │   ├── universities.json
│   │   ├── programs.json
│   │   └── prompts.py
│   └── utils/                  # Utilities
│       ├── __init__.py
│       └── llm_client.py
├── data/                       # Sample data
│   ├── students/
│   └── reports/
├── tests/
└── requirements.txt
```

## Example Use Cases

### 1. Evaluate Student Profile
```python
analysis = agent.analyze_student_profile(student)
# Returns: strengths, weaknesses, recommendations for improvement
```

### 2. Match Universities
```python
matches = agent.match_universities(student, category="reach")
# Returns: list of reach, target, and safety schools
```

### 3. Application Timeline
```python
timeline = agent.generate_timeline(student, deadline_type="early_action")
# Returns: detailed timeline with tasks and deadlines
```

## Data Privacy

- All student data is processed locally
- No data is shared without explicit consent
- Compliant with FERPA guidelines
- API calls to LLM providers are encrypted

## Contributing

Contributions are welcome! Please read CONTRIBUTING.md for guidelines.

## License

MIT License - see LICENSE file for details

## Support

For questions or issues, please open a GitHub issue or contact the maintainers.
