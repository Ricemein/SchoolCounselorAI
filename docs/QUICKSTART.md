# Quick Start Guide

Get up and running with the College Admissions AI Counselor in 5 minutes!

## Step 1: Installation (2 minutes)

```bash
# Navigate to project directory
cd college-admissions-counselor

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Configuration (1 minute)

```bash
# Copy environment template
cp .env.example .env

# Edit .env file and add your OpenAI API key
# Open .env in any text editor and set:
# OPENAI_API_KEY=sk-your-actual-key-here
```

**Don't have an OpenAI API key?**
1. Go to https://platform.openai.com/
2. Sign up or log in
3. Navigate to API keys section
4. Create a new API key
5. Copy and paste into .env file

## Step 3: Try the Interactive Mode (2 minutes)

```bash
python main.py --interactive
```

Follow the prompts to:
1. Enter student information (name, GPA, test scores, interests)
2. Choose an analysis type
3. View results!

## Step 4: Try with Sample Data

```bash
# Analyze the sample student profile
python main.py --agent profile-analyzer --student data/students/sample_student.json

# Get university recommendations
python main.py --agent university-matcher --student data/students/sample_student.json

# Get comprehensive consultation
python main.py --agent comprehensive --student data/students/sample_student.json
```

## Example Output

When you run the profile analyzer, you'll see:

```
Analyzing Student Profile...

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Quick Summary                                      ┃
┃                                                    ┃
┃ Alex Chen presents a very strong academic         ┃
┃ profile with strong extracurricular involvement   ┃
┃ and strong CS preparation. Research experience    ┃
┃ adds significant strength. Competitive for top-   ┃
┃ tier CS programs with balanced list.              ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

Objective Metrics:
  Academic Index: 88.5/100
  GPA: 3.85/4.0
  SAT: 1480
  Extracurricular Strength: strong
  CS Profile Strength: strong
  Research Experience: Yes
```

## Next Steps

### Create Your Own Student Profile

1. Copy the sample student file:
   ```bash
   cp data/students/sample_student.json data/students/your_student.json
   ```

2. Edit `your_student.json` with actual student data

3. Run analysis:
   ```bash
   python main.py --agent comprehensive --student data/students/your_student.json
   ```

### Use the Python API

Create a Python script:

```python
from counselor_ai import CounselorAgent, StudentProfile
from counselor_ai.models.student import AcademicRecord

# Create student profile
academic_record = AcademicRecord(
    gpa=3.8,
    sat_total=1450,
    ap_courses=["AP Computer Science A"],
    cs_courses=["AP CS A", "Data Structures"]
)

student = StudentProfile(
    name="Your Student",
    graduation_year=2025,
    academic_record=academic_record,
    cs_interests=["Artificial Intelligence", "Robotics"]
)

# Get AI counseling
agent = CounselorAgent()
analysis = agent.analyze_student_profile(student)

print(analysis["quick_summary"])
```

### Explore More Features

Check out the comprehensive examples:
```bash
python examples/api_usage_examples.py
```

Or read the full [Usage Guide](USAGE_GUIDE.md).

## Common Issues

### "Module not found" error
Make sure you activated the virtual environment:
```bash
source venv/bin/activate
```

### "API key not found" error
Make sure you created the .env file and added your key:
```bash
cp .env.example .env
# Then edit .env and add your key
```

### JSON format error
Use the sample student file as a template. Make sure:
- All quotes are double quotes (not single)
- No trailing commas
- Numbers are not in quotes (unless specified)

## Tips

1. **Start with interactive mode** - easiest way to get started
2. **Use sample_student.json as template** - copy and modify it
3. **Check the examples folder** - lots of code examples
4. **Read the full docs** - comprehensive guide in docs/USAGE_GUIDE.md

## Need Help?

- Check the [Usage Guide](USAGE_GUIDE.md) for detailed documentation
- Look at `examples/api_usage_examples.py` for code examples
- Review the sample student file for JSON format reference

---

## Ready to Go!

You're all set! The counselor AI can help with:
- ✅ Student profile analysis
- ✅ University recommendations (reach/target/safety)
- ✅ Essay feedback and topic ideas
- ✅ Application timeline planning
- ✅ Research opportunity identification

Happy counseling! 🎓
