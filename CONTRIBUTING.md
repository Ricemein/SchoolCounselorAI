# Contributing to College Admissions AI Counselor

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Ways to Contribute

1. **Report Bugs** - Found a bug? Open an issue with details
2. **Suggest Features** - Have ideas for improvements? We'd love to hear them
3. **Improve Documentation** - Help make the docs clearer and more comprehensive
4. **Add University Data** - Expand the university knowledge base
5. **Code Contributions** - Fix bugs or implement new features

## Getting Started

### Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/yourusername/college-admissions-counselor.git
cd college-admissions-counselor

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-asyncio black flake8 mypy

# Set up pre-commit hooks (optional)
pip install pre-commit
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=counselor_ai

# Run specific test file
pytest tests/test_counselor_ai.py -v
```

### Code Style

We follow PEP 8 style guidelines with some modifications:

```bash
# Format code with black
black counselor_ai/ tests/

# Check style with flake8
flake8 counselor_ai/ tests/

# Type checking with mypy
mypy counselor_ai/
```

**Style Guidelines:**
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use type hints for function signatures
- Write docstrings for all public functions/classes
- Follow existing naming conventions

## Contributing Code

### Branch Naming

- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring

### Commit Messages

Follow conventional commits format:

```
<type>: <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat: add essay topic suggestion feature

fix: correct GPA calculation for weighted scores

docs: update usage guide with new examples
```

### Pull Request Process

1. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**
   - Write clear, concise code
   - Add tests for new features
   - Update documentation as needed
   - Ensure all tests pass

3. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat: add your feature"
   ```

4. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Open a Pull Request**
   - Provide a clear description of changes
   - Reference any related issues
   - Ensure CI checks pass
   - Wait for review

### Pull Request Checklist

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] Commit messages follow convention
- [ ] No breaking changes (or documented if necessary)

## Adding New Features

### Adding a New Agent

To add a new specialized agent:

1. Create new file in `counselor_ai/agents/`
   ```python
   # counselor_ai/agents/your_agent.py
   from counselor_ai.agents.base_agent import BaseAgent
   
   class YourAgent(BaseAgent):
       def your_method(self, ...):
           # Implementation
           pass
   ```

2. Add prompts to `counselor_ai/knowledge/prompts.py`
   ```python
   YOUR_AGENT_SYSTEM = """System prompt for your agent"""
   YOUR_AGENT_PROMPT = """Template for your agent"""
   ```

3. Integrate with CounselorAgent in `base_agent.py`

4. Add tests in `tests/`

5. Update documentation

### Adding University Data

To add universities to the knowledge base:

1. Edit `counselor_ai/knowledge/universities.json`
2. Follow the existing format:
   ```json
   {
     "name": "University Name",
     "location": "City, State",
     "admission_stats": { ... },
     // ... other fields
   }
   ```
3. Ensure data accuracy (cite sources in PR)
4. Test with university matcher agent

### Adding New Models

To add new data models:

1. Create in `counselor_ai/models/`
2. Use Pydantic for data validation
3. Add appropriate validation
4. Write comprehensive tests
5. Update documentation

## Testing Guidelines

### Writing Tests

- Test all public methods
- Use fixtures for common setup
- Test edge cases and error conditions
- Mock external API calls
- Aim for >80% code coverage

### Test Organization

```
tests/
├── test_models.py          # Model tests
├── test_agents.py          # Agent tests
├── test_integration.py     # Integration tests
└── fixtures/               # Test fixtures
```

## Documentation Guidelines

### Docstring Format

Use Google-style docstrings:

```python
def function_name(param1: str, param2: int) -> bool:
    """
    Brief description of function.
    
    More detailed description if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    
    Raises:
        ValueError: When condition occurs
    
    Example:
        >>> function_name("test", 5)
        True
    """
    pass
```

### Updating Documentation

When adding features:
1. Update README.md (if major feature)
2. Update USAGE_GUIDE.md with examples
3. Add to CHANGELOG.md
4. Update docstrings

## Code Review Process

### What Reviewers Look For

- **Correctness**: Does the code do what it's supposed to?
- **Tests**: Are there adequate tests?
- **Style**: Does it follow style guidelines?
- **Documentation**: Is it well-documented?
- **Performance**: Are there any performance concerns?
- **Security**: Are there any security issues?

### Responding to Reviews

- Be open to feedback
- Ask questions if unclear
- Make requested changes or discuss alternatives
- Update PR based on feedback

## Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Assume good intentions

### Getting Help

- Check existing documentation
- Search existing issues
- Ask questions in discussions
- Be specific about problems

## Release Process

(For maintainers)

1. Update version in `counselor_ai/__init__.py`
2. Update CHANGELOG.md
3. Create release tag
4. Build and test distribution
5. Publish release

## Feature Requests

### Submitting Feature Requests

When suggesting features:
1. Check if it already exists
2. Describe the use case
3. Explain why it's valuable
4. Consider implementation complexity
5. Be open to discussion

### Feature Priority

Features are prioritized based on:
- Value to users (counselors and students)
- Alignment with project goals
- Implementation complexity
- Community interest

## Questions?

- Open a discussion for general questions
- Open an issue for bug reports
- Check documentation first

## Thank You!

Every contribution helps make this tool better for students and counselors. Thank you for your time and effort!

---

## Quick Reference

### Common Commands

```bash
# Run tests
pytest tests/ -v

# Format code
black counselor_ai/ tests/

# Check style
flake8 counselor_ai/

# Type check
mypy counselor_ai/

# Run example
python main.py --interactive

# Run with sample data
python main.py --agent comprehensive --student data/students/sample_student.json
```

### File Structure

```
counselor_ai/
├── agents/          # AI agent implementations
├── models/          # Data models
├── knowledge/       # Knowledge bases and prompts
└── utils/           # Utility functions
```

### Need Help?

- 📖 Read the [Usage Guide](docs/USAGE_GUIDE.md)
- 🚀 Check the [Quick Start](docs/QUICKSTART.md)
- 💬 Open a discussion
- 🐛 Report bugs via issues
