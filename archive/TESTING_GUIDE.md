# 🧪 Testing Guide - W3J MCP Hub

## Quick Start

```powershell
# Run all tests
python -m pytest tests -v

# Run with coverage
python -m pytest tests --cov=backend --cov-report=html

# View coverage report
start htmlcov/index.html
```

## Test Structure

```
tests/
├── unit/                    # Fast, isolated tests
│   ├── test_memory.py      # Memory management
│   ├── test_tools.py       # Tool registry
│   └── test_gemini.py      # Gemini client
├── integration/             # Tests requiring running services
│   ├── test_orchestrator.py
│   ├── test_agents.py
│   └── test_composio.py
└── e2e/                     # End-to-end workflow tests
    ├── test_agent_workflow.py
    └── test_n8n_integration.py
```

## Running Tests by Category

### Unit Tests (Fast - No servers needed)
```powershell
# All unit tests
python -m pytest tests/unit -v

# Specific test file
python -m pytest tests/unit/test_memory.py -v

# Specific test function
python -m pytest tests/unit/test_memory.py::test_add_message -v

# With detailed output
python -m pytest tests/unit -v -s
```

### Integration Tests (Requires running servers)
```powershell
# Start servers first
docker-compose up -d

# Run integration tests
python -m pytest tests/integration -v

# Stop servers after
docker-compose down
```

### End-to-End Tests (Full workflows)
```powershell
# Requires all services + API keys
python -m pytest tests/e2e -v --slow
```

## Test Markers

Tests are marked for easy filtering:

```powershell
# Only unit tests
python -m pytest -m unit -v

# Skip slow tests
python -m pytest -m "not slow" -v

# Only tests requiring servers
python -m pytest -m requires_servers -v

# Only tests requiring API keys
python -m pytest -m requires_api_key -v

# Skip integration and e2e
python -m pytest -m "not integration and not e2e" -v
```

## Writing New Tests

### Unit Test Template

```python
# tests/unit/test_your_feature.py
import pytest

def test_your_function():
    """Test description"""
    # Arrange
    input_data = "test"
    
    # Act
    result = your_function(input_data)
    
    # Assert
    assert result == expected_output

@pytest.mark.unit
def test_with_marker():
    """Tests marked as unit run faster"""
    assert True
```

### Integration Test Template

```python
# tests/integration/test_your_integration.py
import pytest

@pytest.mark.integration
@pytest.mark.requires_servers
def test_agent_execution():
    """Test requiring running services"""
    from backend.mcp_servers.agent_builder.server import AgentBuilderMCP
    
    mcp = AgentBuilderMCP()
    result = mcp.create_adk_agent("test", "tools", "gemini-2.0-flash-exp", "test")
    
    assert '"success": true' in result.lower() or "agent_id" in result
```

### Mocking External APIs

```python
# tests/unit/test_with_mocks.py
import pytest
from unittest.mock import Mock, patch

@pytest.mark.unit
def test_api_call_mocked():
    """Test external API without making real requests"""
    
    with patch('requests.get') as mock_get:
        # Setup mock
        mock_get.return_value.json.return_value = {"status": "success"}
        
        # Test your code
        result = your_api_function()
        
        # Verify
        assert result["status"] == "success"
        mock_get.assert_called_once()
```

## Fixtures (Shared Test Data)

Located in `tests/conftest.py`:

```python
@pytest.fixture
def mock_agent():
    """Provides a mock agent for testing"""
    return {
        "agent_id": "test_agent",
        "name": "Test Agent",
        "model": "gemini-2.0-flash-exp"
    }

# Use in tests
def test_with_fixture(mock_agent):
    assert mock_agent["name"] == "Test Agent"
```

## Coverage Reports

### Generate Coverage
```powershell
# HTML report (recommended)
python -m pytest tests --cov=backend --cov-report=html
start htmlcov/index.html

# Terminal report
python -m pytest tests --cov=backend --cov-report=term

# Missing lines report
python -m pytest tests --cov=backend --cov-report=term-missing

# XML report (for CI/CD)
python -m pytest tests --cov=backend --cov-report=xml
```

### Coverage Goals
- **Overall**: 70%+ (current: 75%)
- **Critical paths**: 90%+ (orchestrator, agents)
- **UI code**: 50%+ (Gradio interfaces)

## Continuous Testing

### Watch Mode (Auto-run on file changes)
```powershell
# Install pytest-watch
pip install pytest-watch

# Run in watch mode
ptw tests/unit -- -v
```

### Pre-commit Testing
Add to `.git/hooks/pre-commit`:
```bash
#!/bin/bash
python -m pytest tests/unit -v
if [ $? -ne 0 ]; then
    echo "Tests failed! Commit aborted."
    exit 1
fi
```

Make executable (Linux/Mac):
```bash
chmod +x .git/hooks/pre-commit
```

## Testing Composio Integration

```python
# tests/integration/test_composio.py
import pytest
import os

@pytest.mark.integration
@pytest.mark.requires_api_key
def test_composio_status():
    """Test Composio API connectivity"""
    from backend.integrations.composio_integration import ComposioIntegration
    
    # Skip if no API key
    if not os.getenv("COMPOSIO_API_KEY"):
        pytest.skip("COMPOSIO_API_KEY not set")
    
    client = ComposioIntegration()
    status = client.get_integration_status()
    
    assert status["available"] == True
    assert status["apps_available"] > 0
```

## Testing ADK Agents

```python
# tests/integration/test_agents.py
import pytest
import os

@pytest.mark.integration
@pytest.mark.requires_api_key
def test_adk_agent_execution():
    """Test real agent execution with Gemini"""
    from backend.mcp_servers.agent_builder.adk_integration import ADKIntegration
    
    if not os.getenv("GEMINI_API_KEY"):
        pytest.skip("GEMINI_API_KEY not set")
    
    adk = ADKIntegration()
    
    # Create agent
    result = adk.create_agent(
        name="test_agent",
        description="Test agent",
        model="gemini-2.0-flash-exp",
        capabilities=["code_generation"]
    )
    
    assert result["success"] == True
    agent_id = result["agent"]["agent_id"]
    
    # Execute agent
    exec_result = adk.execute_agent(agent_id, "Say hello")
    
    assert exec_result["success"] == True
    assert len(exec_result["response"]) > 0
```

## Debugging Tests

### Run with Python Debugger
```powershell
# Drop into debugger on failure
python -m pytest tests/unit/test_memory.py --pdb

# Drop into debugger at start
python -m pytest tests/unit/test_memory.py --trace
```

### Verbose Output
```powershell
# Show print statements
python -m pytest tests -v -s

# Show local variables on failure
python -m pytest tests -v -l

# Show full diff on assertion failures
python -m pytest tests -v --tb=long
```

### Run Specific Test
```powershell
# By name pattern
python -m pytest tests -v -k "test_create"

# By file
python -m pytest tests/unit/test_memory.py

# By function
python -m pytest tests/unit/test_memory.py::test_add_message
```

## CI/CD Integration

### GitHub Actions Workflow
```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install -r backend/requirements.txt pytest pytest-cov
      
      - name: Run tests
        run: python -m pytest tests/unit -v --cov=backend
      
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

## Performance Testing

```python
# tests/performance/test_speed.py
import pytest
import time

@pytest.mark.slow
def test_agent_response_time():
    """Agent should respond within 5 seconds"""
    from backend.mcp_servers.agent_builder.adk_integration import ADKIntegration
    
    adk = ADKIntegration()
    
    start = time.time()
    result = adk.execute_agent("test_id", "Quick test")
    duration = time.time() - start
    
    assert duration < 5.0, f"Agent took {duration}s (> 5s limit)"
```

## Best Practices

1. **Test names** should describe behavior: `test_agent_creates_successfully`
2. **Arrange-Act-Assert** pattern for clarity
3. **One assertion per test** when possible
4. **Mock external APIs** in unit tests
5. **Use fixtures** for common setup
6. **Mark tests appropriately** (`@pytest.mark.unit`, etc.)
7. **Keep tests fast** - unit tests < 1s, integration < 10s
8. **Clean up** after tests (delete test agents, files, etc.)
9. **Document** complex test scenarios
10. **Maintain 70%+ coverage** on new code

## Common Issues

### Import Errors
```powershell
# Run from project root
cd C:\Users\W3jde\PROJECTS\MCP\ultimate-mcp-system
python -m pytest tests -v
```

### Missing Dependencies
```powershell
pip install pytest pytest-cov pytest-mock
```

### Test Discovery Issues
```powershell
# See what tests pytest finds
python -m pytest --collect-only

# Ensure test files start with test_
# Ensure test functions start with test_
```

## Next Steps

1. ✅ Run existing unit tests
2. 🔄 Add integration tests for Composio
3. 📝 Write tests for new features
4. 🎯 Achieve 80%+ coverage
5. 🤖 Set up CI/CD pipeline
