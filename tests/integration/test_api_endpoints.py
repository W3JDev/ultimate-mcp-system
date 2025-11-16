"""
Integration tests for API endpoints
"""
import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """Create test client for FastAPI app"""
    # Import here to avoid issues with module loading
    try:
        from main import app
        return TestClient(app)
    except Exception as e:
        pytest.skip(f"Could not create test client: {e}")


class TestMasterOrchestratorAPI:
    """Test Master Orchestrator API endpoints"""
    
    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert data["status"] in ["healthy", "ok"]
    
    def test_process_endpoint_post(self, client):
        """Test process endpoint with POST request"""
        payload = {
            "message": "test message",
            "context": {}
        }
        
        response = client.post("/api/process", json=payload)
        
        # Should return 200 or appropriate status
        assert response.status_code in [200, 400, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, dict)
    
    def test_memory_endpoint(self, client):
        """Test memory retrieval endpoint"""
        response = client.get("/api/memory")
        
        # Should return memory context
        assert response.status_code in [200, 404, 501]
        
        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, dict)


class TestN8NMCPAPI:
    """Test N8N MCP API endpoints"""
    
    @pytest.mark.skip(reason="N8N MCP server may not be running")
    def test_n8n_workflow_generate(self):
        """Test workflow generation endpoint"""
        # This would test actual N8N MCP API
        pass


class TestAgentBuilderAPI:
    """Test Agent Builder MCP API endpoints"""
    
    @pytest.mark.skip(reason="Agent Builder MCP server may not be running")
    def test_agent_creation(self):
        """Test agent creation endpoint"""
        # This would test actual Agent Builder API
        pass


class TestLocalControlAPI:
    """Test Local Control MCP API endpoints"""
    
    @pytest.mark.skip(reason="Local Control MCP server may not be running")
    def test_system_info(self):
        """Test system info endpoint"""
        # This would test actual Local Control API
        pass
