# Contributing Guidelines

Thank you for your interest in contributing to the Video Fraud Detection Agent project!

---

## Table of Contents

1. [Development Setup](#development-setup)
2. [Code Style Guide](#code-style-guide)
3. [Testing Requirements](#testing-requirements)
4. [Pull Request Process](#pull-request-process)
5. [Project Structure](#project-structure)

---

## Development Setup

### Prerequisites

- Python 3.10 or higher
- Ollama with a vision model (e.g., llava)
- Git

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd project9

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black ruff mypy pre-commit

# Set up pre-commit hooks
pre-commit install

# Copy environment template
cp .env.example .env
```

### Verify Setup

```bash
# Run tests
pytest tests/ -v

# Check code style
black --check src/ tests/
ruff check src/ tests/

# Run type checking
mypy src/
```

---

## Code Style Guide

### Formatting

We use **Black** for code formatting with default settings:

```bash
# Format code
black src/ tests/ scripts/

# Check formatting without changes
black --check src/ tests/ scripts/
```

### Linting

We use **Ruff** for linting:

```bash
# Run linter
ruff check src/ tests/ scripts/

# Auto-fix issues
ruff check --fix src/ tests/ scripts/
```

### Type Hints

All functions must include type hints:

```python
# Good
def analyze_frame(self, frame_path: str | Path) -> AnalysisResult:
    ...

# Bad
def analyze_frame(self, frame_path):
    ...
```

### Docstrings

Use NumPy-style docstrings for all public functions and classes:

```python
def analyze_video(self, video_path: str | Path, sample_frames: int = 5) -> AnalysisResult:
    """Analyze a video file for AI generation indicators.

    Parameters
    ----------
    video_path : str | Path
        Path to the video file
    sample_frames : int, optional
        Number of frames to sample (default: 5)

    Returns
    -------
    AnalysisResult
        Aggregated analysis result

    Raises
    ------
    FileNotFoundError
        If video file does not exist
    ValueError
        If video cannot be opened or has no frames
    """
```

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Functions | snake_case | `analyze_frame()` |
| Classes | PascalCase | `VideoFraudDetectionAgent` |
| Constants | UPPER_SNAKE | `SYSTEM_PROMPT` |
| Variables | snake_case | `frame_results` |
| Private | _prefix | `_temp_dir` |

### File Organization

- Maximum 150 lines per file
- Maximum 50 lines per function
- One class per file (with small helpers allowed)
- Group imports: stdlib, third-party, local

---

## Testing Requirements

### Test Structure

```
tests/
├── __init__.py
├── conftest.py          # Shared fixtures
├── test_agent.py        # Agent tests
├── test_models.py       # Model tests
├── test_parsing.py      # Parsing tests
└── test_video_utils.py  # Video utility tests
```

### Writing Tests

```python
import pytest
from src.agent import VideoFraudDetectionAgent

class TestVideoFraudDetectionAgent:
    """Tests for VideoFraudDetectionAgent."""

    def test_analyze_frame_file_not_found(self):
        """Test that FileNotFoundError is raised for missing files."""
        agent = VideoFraudDetectionAgent()
        with pytest.raises(FileNotFoundError):
            agent.analyze_frame("nonexistent.jpg")

    def test_analyze_frame_with_valid_image(self, mock_ollama, sample_image):
        """Test frame analysis with mocked LLM."""
        agent = VideoFraudDetectionAgent()
        result = agent.analyze_frame(sample_image)
        assert result.verdict in [Verdict.AI_GENERATED, Verdict.AUTHENTIC, Verdict.UNCERTAIN]
```

### Coverage Requirements

- Minimum coverage: 70%
- Run with: `pytest --cov=src --cov-fail-under=70`

### Test Categories

1. **Unit tests**: Test individual functions in isolation
2. **Integration tests**: Test component interactions
3. **Edge cases**: Test boundary conditions and error handling

---

## Pull Request Process

### Before Submitting

1. **Run all checks**:
   ```bash
   black --check src/ tests/
   ruff check src/ tests/
   mypy src/
   pytest tests/ -v --cov=src
   ```

2. **Update documentation** if adding features

3. **Add tests** for new functionality

### PR Template

```markdown
## Summary
Brief description of changes

## Changes
- Change 1
- Change 2

## Testing
- [ ] All tests pass
- [ ] Coverage maintained > 70%
- [ ] New tests added for new features

## Checklist
- [ ] Code formatted with black
- [ ] No ruff warnings
- [ ] Type hints added
- [ ] Docstrings updated
```

### Review Process

1. Submit PR against `main` branch
2. Automated checks must pass
3. At least one approval required
4. Squash and merge

---

## Project Structure

```
project9/
├── src/                    # Source code
│   ├── __init__.py        # Package exports
│   ├── agent.py           # Main agent class
│   ├── models.py          # Data models
│   ├── parsing.py         # Response parsing
│   ├── prompts.py         # Prompt templates
│   ├── providers.py       # LLM providers
│   ├── video_utils.py     # Video processing
│   └── main.py            # CLI entry point
├── tests/                  # Test files
├── docs/                   # Documentation
├── scripts/               # Utility scripts
├── results/               # Experiment outputs
├── videos/                # Test videos
├── notebooks/             # Analysis notebooks
├── .env.example           # Environment template
├── requirements.txt       # Dependencies
├── pyproject.toml         # Project config
└── README.md              # Main documentation
```

---

## Getting Help

- Open an issue for bugs or feature requests
- Check existing issues before creating new ones
- Provide minimal reproduction steps for bugs
