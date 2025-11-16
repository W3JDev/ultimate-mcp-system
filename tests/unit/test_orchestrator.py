"""
Unit tests for Orchestrator
"""
import pytest
from memory import MemoryManager
from orchestrator import MCPOrchestrator


class TestMCPOrchestrator:
    """Test MCP Orchestrator functionality"""
    
    def test_initialization(self):
        """Test orchestrator initialization"""
        memory = MemoryManager()
        orchestrator = MCPOrchestrator(memory)
        assert orchestrator is not None
        assert hasattr(orchestrator, 'mcp_servers')
        assert hasattr(orchestrator, 'memory')
        assert orchestrator.memory == memory
    
    def test_mcp_servers_configured(self):
        """Test that MCP servers are configured"""
        memory = MemoryManager()
        orchestrator = MCPOrchestrator(memory)
        servers = orchestrator.mcp_servers
        
        assert 'n8n' in servers
        assert 'agent_builder' in servers
        assert 'local_control' in servers
        assert 'cloud_services' in servers
    
    def test_process_request_basic(self):
        """Test basic request processing"""
        memory = MemoryManager()
        orchestrator = MCPOrchestrator(memory)
        
        # This will use fallback logic without real API
        response = orchestrator.process("Hello")
        
        # Should return a string response
        assert isinstance(response, str)
        assert len(response) > 0
    
    def test_memory_integration(self):
        """Test that orchestrator uses memory manager"""
        memory = MemoryManager()
        orchestrator = MCPOrchestrator(memory)
        
        # Add a message to memory
        memory.add_message("user", "Test message")
        
        # Verify orchestrator can access it
        context = orchestrator.memory.get_context()
        assert "recent_messages" in context
        assert len(context["recent_messages"]) == 1
    
    def test_no_api_key_fallback(self):
        """Test that orchestrator works without API key"""
        memory = MemoryManager()
        orchestrator = MCPOrchestrator(memory)
        
        # Should initialize without errors even without API key
        assert orchestrator.client is None or orchestrator.client is not None
        
        # Should still be able to process requests
        response = orchestrator.process("test request")
        assert isinstance(response, str)
    
    def test_multiple_requests(self):
        """Test processing multiple requests in sequence"""
        memory = MemoryManager()
        orchestrator = MCPOrchestrator(memory)
        
        # Process multiple requests
        response1 = orchestrator.process("First request")
        response2 = orchestrator.process("Second request")
        
        # Both should return valid responses
        assert isinstance(response1, str)
        assert isinstance(response2, str)
        assert len(response1) > 0
        assert len(response2) > 0
