"""
Pytest configuration and fixtures
"""
import os
import sys
import pytest
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

# Set test environment variables
os.environ["TESTING"] = "1"
os.environ["ANTHROPIC_API_KEY"] = "test-key-anthropic"
os.environ["OPENAI_API_KEY"] = "test-key-openai"


@pytest.fixture
def test_env():
    """Provide test environment variables"""
    return {
        "ANTHROPIC_API_KEY": "test-key-anthropic",
        "OPENAI_API_KEY": "test-key-openai",
        "N8N_API_KEY": "test-key-n8n",
        "N8N_BASE_URL": "http://localhost:5678"
    }


@pytest.fixture
def mock_anthropic_client(monkeypatch):
    """Mock Anthropic client for testing"""
    class MockMessage:
        def __init__(self, content):
            self.content = [type('obj', (object,), {'text': content})]
    
    class MockMessages:
        def create(self, **kwargs):
            return MockMessage("Mocked AI response for testing")
    
    class MockAnthropic:
        def __init__(self, *args, **kwargs):
            self.messages = MockMessages()
    
    import anthropic
    monkeypatch.setattr(anthropic, "Anthropic", MockAnthropic)
    return MockAnthropic


@pytest.fixture
def temp_logs_dir(tmp_path):
    """Create temporary logs directory"""
    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()
    return logs_dir


@pytest.fixture
def temp_memory_dir(tmp_path):
    """Create temporary memory directory"""
    memory_dir = tmp_path / "memory"
    memory_dir.mkdir()
    return memory_dir


@pytest.fixture
def temp_agents_dir(tmp_path):
    """Create temporary agents directory"""
    agents_dir = tmp_path / "agents"
    agents_dir.mkdir()
    return agents_dir
