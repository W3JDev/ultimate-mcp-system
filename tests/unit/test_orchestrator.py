"""
Unit tests for Orchestrator
"""
import pytest
from orchestrator import MCPOrchestrator


class TestMCPOrchestrator:
    """Test MCP Orchestrator functionality"""
    
    def test_initialization(self):
        """Test orchestrator initialization"""
        orchestrator = MCPOrchestrator()
        assert orchestrator is not None
        assert hasattr(orchestrator, 'mcp_servers')
        assert hasattr(orchestrator, 'memory')
    
    def test_mcp_servers_configured(self):
        """Test that MCP servers are configured"""
        orchestrator = MCPOrchestrator()
        servers = orchestrator.mcp_servers
        
        assert 'n8n' in servers
        assert 'agent_builder' in servers
        assert 'local_control' in servers
        
        # Check server configuration
        assert 'url' in servers['n8n']
        assert 'keywords' in servers['n8n']
    
    def test_keyword_routing_n8n(self):
        """Test keyword-based routing to N8N"""
        orchestrator = MCPOrchestrator()
        
        # Test various N8N-related keywords
        test_messages = [
            "create a workflow",
            "n8n automation",
            "build workflow for emails"
        ]
        
        for message in test_messages:
            server = orchestrator._route_by_keywords(message)
            assert server == 'n8n', f"Failed to route '{message}' to n8n"
    
    def test_keyword_routing_agent_builder(self):
        """Test keyword-based routing to Agent Builder"""
        orchestrator = MCPOrchestrator()
        
        test_messages = [
            "create an agent",
            "build AI agent",
            "crewai setup"
        ]
        
        for message in test_messages:
            server = orchestrator._route_by_keywords(message)
            assert server == 'agent_builder', f"Failed to route '{message}' to agent_builder"
    
    def test_keyword_routing_local_control(self):
        """Test keyword-based routing to Local Control"""
        orchestrator = MCPOrchestrator()
        
        test_messages = [
            "system info",
            "execute command",
            "browser automation"
        ]
        
        for message in test_messages:
            server = orchestrator._route_by_keywords(message)
            assert server == 'local_control', f"Failed to route '{message}' to local_control"
    
    def test_default_routing(self):
        """Test default routing for unclear messages"""
        orchestrator = MCPOrchestrator()
        
        # Generic message that doesn't match any keywords
        server = orchestrator._route_by_keywords("hello world")
        assert server in ['n8n', 'agent_builder', 'local_control']
    
    def test_process_request_structure(self):
        """Test that process_request returns expected structure"""
        orchestrator = MCPOrchestrator()
        
        # This will use fallback logic without real API
        response = orchestrator.process("create a workflow")
        
        assert isinstance(response, dict)
        assert 'response' in response or 'error' in response
