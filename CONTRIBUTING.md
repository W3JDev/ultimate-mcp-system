# 🤝 Contributing to Ultimate MCP System

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Areas Needing Help](#areas-needing-help)

---

## 🤝 Code of Conduct

### Our Pledge

We pledge to make participation in this project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

**Positive behavior includes:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Unacceptable behavior includes:**
- Trolling, insulting/derogatory comments, personal or political attacks
- Public or private harassment
- Publishing others' private information without permission
- Other conduct which could reasonably be considered inappropriate

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+ (3.13 supported)
- Git
- Basic understanding of FastAPI, Gradio, or AI APIs
- Familiarity with async Python (for advanced contributions)

### First Steps

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/ultimate-mcp-system.git
   cd ultimate-mcp-system
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/W3JDev/ultimate-mcp-system.git
   ```
4. **Create a branch** for your work:
   ```bash
   git checkout -b feature/your-feature-name
   ```

---

## 💻 Development Setup

### 1. Create Virtual Environment

```bash
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
# Production dependencies
pip install -r backend/requirements.txt

# Development dependencies
pip install -r backend/requirements-dev.txt  # If exists

# Or install dev tools manually
pip install pytest pytest-asyncio black flake8 mypy
```

### 3. Install Playwright (for Local Control MCP)

```bash
playwright install chromium
```

### 4. Configure Environment

```bash
cp .env.example .env
# Add test API keys if needed
```

### 5. Run Tests

```bash
pytest tests/
```

### 6. Start Development Server

```bash
# Start individual MCP
python backend/mcp_servers/agent_builder/server.py

# Or all servers
python launch_all_servers.py
```

---

## 📁 Project Structure

```
ultimate-mcp-system/
├── backend/
│   ├── main.py                 # Master Orchestrator
│   ├── orchestrator.py         # Routing logic
│   ├── memory.py               # Memory management
│   ├── requirements.txt        # Dependencies
│   ├── logs/                   # Log files (created at runtime)
│   └── mcp_servers/
│       ├── n8n_automation/     # N8N Automation MCP
│       ├── agent_builder/      # Agent Builder MCP
│       ├── local_control/      # Local Control MCP
│       └── cloud_services/     # Cloud Services MCP (TBD)
├── tests/                      # Test suite
├── docs/                       # Documentation
├── .github/                    # GitHub config, workflows
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Multi-container setup
├── README.md                   # Main documentation
├── SYSTEM_ASSESSMENT.md        # Honest evaluation
├── DEPLOYMENT.md               # Deployment guides
├── CONTRIBUTING.md             # This file
└── LICENSE                     # MIT License
```

### Key Files to Know

| File | Purpose |
|------|---------|
| `backend/main.py` | FastAPI master orchestrator entry point |
| `backend/orchestrator.py` | Intent analysis and MCP routing |
| `backend/mcp_servers/*/server.py` | Individual MCP server implementations |
| `.github/copilot-instructions.md` | AI agent development guidelines |
| `SYSTEM_ASSESSMENT.md` | Project status and roadmap |

---

## 📏 Coding Standards

### Python Style Guide

Follow **PEP 8** with these specifics:

```python
# Use type hints
def process_request(user_input: str) -> Dict[str, Any]:
    pass

# Docstrings (Google style)
def create_agent(name: str, description: str) -> Agent:
    '''
    Create a new AI agent with given parameters.
    
    Args:
        name: Agent name (3-50 characters)
        description: Natural language agent description
    
    Returns:
        Agent object with unique ID
    
    Raises:
        ValueError: If name is invalid
    '''
    pass

# Use loguru for logging
from loguru import logger
logger.info("✅ Agent created successfully")
logger.error("❌ Failed to create agent: {error}")

# Emoji prefixes for log scanning
# ✅ Success  ❌ Error  ⚠️ Warning  🔍 Debug  📝 Info  🚀 Start
```

### Code Formatting

```bash
# Format code with Black
black backend/

# Check linting
flake8 backend/

# Type checking
mypy backend/
```

### Naming Conventions

- **Classes**: `PascalCase` (e.g., `AgentBuilderMCP`)
- **Functions/Variables**: `snake_case` (e.g., `create_workflow()`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `DEFAULT_PORT`)
- **Private methods**: `_leading_underscore()` (e.g., `_validate_input()`)

### File Organization

```python
# Order of sections in .py files:
# 1. Module docstring
# 2. Imports (stdlib, third-party, local)
# 3. Constants
# 4. Classes
# 5. Functions
# 6. if __name__ == "__main__"

'''
Module description here
'''
import os
import sys
from typing import Dict, Any

from gradio import gr
from loguru import logger

from .utils import helper_function

DEFAULT_PORT = 7860

class MyMCP:
    pass

def main():
    pass

if __name__ == "__main__":
    main()
```

---

## 🧪 Testing

### Running Tests

```bash
# All tests
pytest tests/

# Specific test file
pytest tests/test_orchestrator.py

# With coverage
pytest --cov=backend tests/

# Verbose output
pytest -v tests/
```

### Writing Tests

```python
# tests/test_agent_builder.py
import pytest
from backend.mcp_servers.agent_builder.server import AgentBuilderMCP

@pytest.fixture
def mcp():
    return AgentBuilderMCP()

def test_create_agent(mcp):
    '''Test agent creation with valid inputs'''
    result = mcp.create_adk_agent(
        name="TestAgent",
        description="Test description"
    )
    assert result["status"] == "success"
    assert "agent_id" in result

def test_create_agent_invalid_name(mcp):
    '''Test agent creation with invalid name'''
    with pytest.raises(ValueError):
        mcp.create_adk_agent(
            name="",  # Invalid empty name
            description="Test"
        )
```

### Test Guidelines

- Write tests for all new features
- Aim for 80%+ code coverage
- Test edge cases and error conditions
- Use meaningful test names
- Keep tests isolated (no shared state)

---

## 🔄 Pull Request Process

### Before Submitting

1. **Update from upstream**:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run tests**:
   ```bash
   pytest tests/
   ```

3. **Format code**:
   ```bash
   black backend/
   flake8 backend/
   ```

4. **Update documentation** if needed

5. **Commit with clear messages**:
   ```bash
   git commit -m "feat: Add workflow template library"
   git commit -m "fix: Handle missing API keys gracefully"
   git commit -m "docs: Update installation instructions"
   ```

### Commit Message Format

Use conventional commits:

```
type(scope): short description

Longer description if needed

Fixes #123
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style (formatting, no logic change)
- `refactor`: Code restructuring
- `test`: Adding/updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(agent-builder): Add CrewAI team creation
fix(orchestrator): Handle None client gracefully
docs(readme): Update deployment instructions
test(n8n): Add workflow validation tests
```

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings

## Related Issues
Fixes #123
```

### Review Process

1. Automated checks (tests, linting) must pass
2. At least one maintainer review required
3. Address review comments
4. Maintainer will merge once approved

---

## 🎯 Areas Needing Help

### Critical (High Priority)

- [ ] **MCP Protocol Implementation**
  - JSON-RPC 2.0 handler
  - stdio/SSE transport layer
  - Tool registration system
  - Claude Desktop integration

- [ ] **Feature Completion**
  - N8N workflow execution
  - Agent instantiation (ADK, CrewAI)
  - System command security layer

### High Priority

- [ ] **Testing Infrastructure**
  - Unit tests for all MCPs
  - Integration tests
  - End-to-end tests
  - CI/CD pipeline

- [ ] **Security**
  - Input validation
  - API key management
  - Rate limiting
  - Authentication system

### Medium Priority

- [ ] **Documentation**
  - API documentation (OpenAPI)
  - Video tutorials
  - Example workflows
  - Troubleshooting guides

- [ ] **UI/UX**
  - Visual workflow builder
  - Dark mode support
  - Mobile responsiveness
  - Accessibility improvements

### Nice to Have

- [ ] **Additional Features**
  - Workflow marketplace
  - Agent templates
  - Multi-language support
  - Monitoring dashboard

---

## 💡 Contribution Ideas

### For Beginners

- Fix typos in documentation
- Improve code comments
- Add type hints
- Write unit tests for existing functions
- Update README with missing information

### For Intermediate

- Implement error handling improvements
- Add new workflow templates
- Create agent framework integrations
- Improve UI components
- Add logging enhancements

### For Advanced

- Implement MCP protocol
- Design authentication system
- Build monitoring infrastructure
- Optimize performance
- Create CI/CD pipeline

---

## 📞 Getting Help

- **Questions**: Open a GitHub Discussion
- **Bugs**: Open a GitHub Issue
- **Feature Requests**: Open a GitHub Issue with `enhancement` label
- **Security Issues**: Email maintainer directly (see SECURITY.md)

---

## 🏆 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Given credit in relevant documentation

Top contributors may be invited to become maintainers.

---

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to Ultimate MCP System! 🚀**

**Questions?** Open a discussion or reach out to maintainers.
