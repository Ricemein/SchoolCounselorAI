# Usage Guide - College Admissions AI Counselor

## Table of Contents
1. [Quick Start](#quick-start)
2. [Command Line Interface](#command-line-interface)
3. [Python API](#python-api)
4. [Student Profile Format](#student-profile-format)
5. [Agent Types](#agent-types)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Installation

```bash
# Clone the repository
cd college-admissions-counselor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### First Run - Interactive Mode

```bash
python main.py --interactive
```

This will guide you through creating a student profile and getting recommendations.

### Using a Sample Student Profile

```bash
# Analyze sample student profile
python main.py --agent profile-analyzer --student data/students/sample_student.json

# Get university recommendations
python main.py --agent university-matcher --student data/students/sample_student.json

# Get comprehensive consultation
python main.py --agent comprehensive --student data/students/sample_student.json --output data/reports/report.json
```

---

## Command Line Interface

### Basic Commands

#### Profile Analysis
```bash
python main.py --agent profile-analyzer --student <path-to-student-json>
```
Analyzes student academic profile, extracurriculars, and overall competitiveness.

**Output includes:**
- Academic Index (0-100 score)
- CS profile strength assessment
- Extracurricular evaluation
- AI-generated detailed analysis
- Recommendations for improvement

#### University Matching
```bash
python main.py --agent university-matcher --student <path-to-student-json>
```
Provides university recommendations categorized as reach, target, and safety schools.

**Output includes:**
- List of reach schools (3-4)
- List of target schools (4-5)
- List of safety schools (2-3)
- Detailed reasoning for each recommendation

#### Comprehensive Consultation
```bash
python main.py --agent comprehensive --student <path-to-student-json>
```
Complete consultation covering all aspects of college admissions.

**Output includes:**
- Profile analysis
- University recommendations
- Personalized next steps
- Timeline guidance

### Saving Reports

Add `--output` flag to save results to a file:

```bash
python main.py --agent comprehensive --student data/students/jane_doe.json \
    --output data/reports/jane_doe_report.json
```

### Interactive Mode

```bash
python main.py --interactive
```

Guides you through:
1. Creating a student profile (basic info)
2. Choosing what analysis to run
3. Viewing results in a formatted display

---

## Python API

### Basic Usage

```python
from counselor_ai import CounselorAgent, StudentProfile
from counselor_ai.models.student import AcademicRecord

# Create student profile
academic_record = AcademicRecord(
    gpa=3.85,
    sat_total=1480,
    ap_courses=["AP CS A", "AP Calculus BC"],
    cs_courses=["AP CS A", "Data Structures"]
)

student = StudentProfile(
    name="John Doe",
    graduation_year=2025,
    academic_record=academic_record,
    cs_interests=["AI/ML", "Robotics"]
)

# Initialize agent
agent = CounselorAgent()

# Get analysis
analysis = agent.analyze_student_profile(student)
print(analysis["quick_summary"])

# Get university recommendations
recommendations = agent.get_university_recommendations(student)
print(recommendations["structured_recommendations"])
```

### Advanced Usage

#### Custom Preferences
```python
# University matching with preferences
recommendations = agent.get_university_recommendations(
    student=student,
    preferences={
        "regions": ["Northeast", "California"],
        "university_size": "medium to large",
        "research_focus": True,
        "financial_aid_needed": True
    }
)
```

#### Essay Feedback
```python
# Get essay feedback
essay_text = "Your essay content here..."

feedback = agent.analyze_essay(
    student=student,
    essay_content=essay_text,
    essay_type="personal_statement",
    prompt="Tell us about yourself"
)

print(f"Word count: {feedback['word_count']}")
print(f"Quick checks: {feedback['quick_checks']}")
# View AI feedback
print(feedback['ai_feedback'])
```

#### Application Timeline
```python
# Create timeline
timeline = agent.create_application_timeline(
    student=student,
    target_universities=["MIT", "Stanford", "CMU"],
    application_type="regular_decision"
)

# View key deadlines
for deadline in timeline['key_deadlines']:
    print(f"{deadline['deadline']}: {deadline['type']}")
```

#### Research Opportunities
```python
# Find research opportunities
opportunities = agent.get_research_opportunities(
    student=student,
    research_interests=["AI/ML", "Computer Vision"],
    target_universities=["MIT", "Stanford"]
)

# View summer programs
for program in opportunities['structured_opportunities']['summer_programs']:
    print(f"{program['name']}: {program['description']}")
```

---

## Student Profile Format

### JSON Structure

```json
{
  "student_id": "unique_id",
  "name": "Student Name",
  "email": "email@example.com",
  "graduation_year": 2025,
  
  "academic_record": {
    "gpa": 3.85,
    "gpa_weighted": 4.2,
    "class_rank": 15,
    "class_size": 400,
    "sat_total": 1480,
    "sat_math": 780,
    "sat_ebrw": 700,
    "act_composite": null,
    "ap_courses": ["AP CS A", "AP Calculus BC"],
    "ap_scores": {"AP CS A": 5},
    "cs_courses": ["AP CS A", "Data Structures"],
    "math_courses": ["AP Calculus BC"]
  },
  
  "cs_interests": ["AI/ML", "Robotics"],
  "career_goals": "Research in AI",
  
  "extracurriculars": [
    {
      "name": "Robotics Club",
      "category": "STEM",
      "role": "Captain",
      "years_participated": 3,
      "hours_per_week": 10,
      "achievements": ["Regional Winner"]
    }
  ],
  
  "research_experience": [
    {
      "title": "ML Project",
      "field": "Computer Science",
      "description": "Built CNN model",
      "duration_months": 6,
      "outcome": "Published paper"
    }
  ],
  
  "awards_honors": ["National Merit", "Science Fair Winner"],
  "first_generation": false,
  "financial_need": "medium"
}
```

### Required Fields
- `name` (string)
- `graduation_year` (integer)
- `academic_record.gpa` (float, 0-4.0)

### Optional But Recommended
- Test scores (SAT/ACT)
- CS courses and interests
- Extracurricular activities
- Research experience
- Awards and honors

---

## Agent Types

### 1. Profile Analyzer Agent
**Purpose:** Comprehensive evaluation of student profile

**Key Metrics:**
- Academic Index (0-100)
- CS Profile Strength (exceptional/strong/moderate/developing)
- Extracurricular Strength
- Research Experience Assessment

**Use When:**
- Initial student assessment
- Identifying strengths/weaknesses
- Planning profile improvements

### 2. University Matcher Agent
**Purpose:** Match students with appropriate universities

**Methodology:**
- Compares student stats to university admission data
- Considers academic fit, program strengths, preferences
- Categorizes as reach/target/safety

**Use When:**
- Building college list
- Evaluating school competitiveness
- Balancing application portfolio

### 3. Essay Coach Agent
**Purpose:** Provide feedback on college essays

**Features:**
- Content and structure analysis
- Voice and authenticity check
- Specific improvement suggestions
- Topic brainstorming

**Use When:**
- Drafting essays
- Revising and polishing
- Choosing essay topics

### 4. Timeline Manager Agent
**Purpose:** Create application timeline

**Includes:**
- Month-by-month breakdown
- Key deadlines (EA/ED/RD)
- Testing timeline
- Financial aid deadlines

**Use When:**
- Starting application process
- Planning junior/senior year
- Tracking progress

### 5. Research Advisor Agent
**Purpose:** Identify research opportunities

**Provides:**
- Summer programs (REU, MIT BWSI, etc.)
- Local opportunities
- Outreach strategies
- Preparation tips

**Use When:**
- Seeking research experience
- Strengthening STEM profile
- Planning summer activities

---

## Best Practices

### For Counselors

1. **Start with Profile Analysis**
   - Always run profile analysis first
   - Use insights to guide other recommendations
   - Update profile as student progresses

2. **Maintain Realistic Expectations**
   - Use reach/target/safety categories appropriately
   - Consider acceptance rates and competitiveness
   - Account for program-specific selectivity (CS)

3. **Regular Updates**
   - Update student profiles quarterly
   - Track progress on recommendations
   - Adjust college list as needed

4. **Holistic Approach**
   - Don't focus solely on test scores
   - Consider research, leadership, impact
   - Evaluate fit beyond rankings

### For Students

1. **Be Honest and Thorough**
   - Provide complete, accurate information
   - Include all relevant experiences
   - Update profile regularly

2. **Use AI as a Guide, Not Decision Maker**
   - Review AI recommendations critically
   - Discuss with counselors and family
   - Visit schools when possible

3. **Start Early**
   - Begin profile building in junior year
   - Allow time for test prep and retakes
   - Start essays over the summer

4. **Balance Your List**
   - Apply to mix of reach/target/safety
   - Consider financial fit
   - Have genuine backup options

---

## Troubleshooting

### API Key Issues

**Problem:** `OPENAI_API_KEY not found in environment variables`

**Solution:**
```bash
# Make sure .env file exists
cp .env.example .env

# Edit .env and add your API key
# OPENAI_API_KEY=your_actual_api_key_here

# Verify it's set
cat .env | grep OPENAI_API_KEY
```

### Import Errors

**Problem:** Missing modules or import errors

**Solution:**
```bash
# Ensure you're in the virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep openai
```

### JSON Format Errors

**Problem:** Error loading student profile

**Solution:**
- Validate JSON syntax (use jsonlint.com)
- Ensure required fields are present
- Check data types (GPA should be float, year should be int)
- Use sample_student.json as template

### Rate Limiting

**Problem:** OpenAI API rate limit errors

**Solution:**
- Wait a moment and retry
- Consider upgrading OpenAI plan
- Batch student analyses
- Use caching for repeated queries

---

## Additional Resources

- See `examples/api_usage_examples.py` for comprehensive code examples
- Check `data/students/sample_student.json` for profile template
- Review college websites for specific program requirements
- Consult official admission statistics for accuracy

---

## Support

For questions or issues:
1. Check this guide first
2. Review example code
3. Consult README.md
4. Open an issue on GitHub (if applicable)

Remember: This tool provides guidance, not guarantees. Always verify information and combine AI insights with human expertise!
