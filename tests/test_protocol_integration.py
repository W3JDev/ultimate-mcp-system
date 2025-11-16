"""
Integration tests for MCP Protocol
Tests the full request/response cycle
"""
import io
import json
import sys

import pytest

# Add backend to path
sys.path.insert(0, '/home/runner/work/ultimate-mcp-system/ultimate-mcp-system/backend')

from mcp_protocol import (
    LifecycleManager,
    MCPRequestHandler,
    StdioTransport,
    ToolRegistry,
)


class TestProtocolIntegration:
    """Test full protocol integration"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.transport = StdioTransport()
        self.lifecycle = LifecycleManager()
        self.registry = ToolRegistry()
        self.handler = MCPRequestHandler(self.transport, self.lifecycle, self.registry)
        
        # Register a test tool
        def echo_handler(args):
            return args.get("message", "")
        
        self.registry.register_tool(
            "echo",
            "Echo a message",
            echo_handler,
            {
                "type": "object",
                "properties": {
                    "message": {"type": "string"}
                }
            }
        )
    
    def test_initialize_flow(self, capsys):
        """Test complete initialize flow"""
        # Send initialize request
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-03-26",
                "capabilities": {},
                "clientInfo": {"name": "test"}
            }
        }
        
        self.handler.handle_request(request)
        
        captured = capsys.readouterr()
        response = json.loads(captured.out.strip())
        
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 1
        assert "result" in response
        assert response["result"]["serverInfo"]["name"] == "ultimate-mcp-hub"
    
    def test_initialized_notification(self):
        """Test initialized notification"""
        # Initialize first
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-03-26",
                "capabilities": {},
                "clientInfo": {"name": "test"}
            }
        }
        self.handler.handle_request(init_request)
        
        # Send initialized notification
        notification = {
            "jsonrpc": "2.0",
            "method": "initialized"
        }
        
        self.handler.handle_request(notification)
        
        assert self.lifecycle.is_initialized()
    
    def test_tools_list(self, capsys):
        """Test tools/list after initialization"""
        # Initialize
        self._initialize()
        
        # Clear previous output
        capsys.readouterr()
        
        # Request tools list
        request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        
        self.handler.handle_request(request)
        
        captured = capsys.readouterr()
        response = json.loads(captured.out.strip())
        
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 2
        assert "result" in response
        assert "tools" in response["result"]
        
        tools = response["result"]["tools"]
        assert len(tools) == 1
        assert tools[0]["name"] == "echo"
    
    def test_tools_call(self, capsys):
        """Test tools/call after initialization"""
        # Initialize
        self._initialize()
        
        # Clear previous output
        capsys.readouterr()
        
        # Call tool
        request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "echo",
                "arguments": {"message": "Hello, World!"}
            }
        }
        
        self.handler.handle_request(request)
        
        captured = capsys.readouterr()
        response = json.loads(captured.out.strip())
        
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 3
        assert "result" in response
        assert "content" in response["result"]
    
    def test_tools_list_before_initialized(self, capsys):
        """Test tools/list fails before initialization"""
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {}
        }
        
        self.handler.handle_request(request)
        
        captured = capsys.readouterr()
        response = json.loads(captured.out.strip())
        
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 1
        assert "error" in response
        assert "initialized" in str(response["error"]).lower()
    
    def test_method_not_found(self, capsys):
        """Test unknown method handling"""
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "unknown/method",
            "params": {}
        }
        
        self.handler.handle_request(request)
        
        captured = capsys.readouterr()
        response = json.loads(captured.out.strip())
        
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 1
        assert "error" in response
        assert response["error"]["code"] == -32601
    
    def test_tool_not_found(self, capsys):
        """Test calling non-existent tool"""
        # Initialize
        self._initialize()
        
        # Clear previous output
        capsys.readouterr()
        
        # Call non-existent tool
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "nonexistent",
                "arguments": {}
            }
        }
        
        self.handler.handle_request(request)
        
        captured = capsys.readouterr()
        response = json.loads(captured.out.strip())
        
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 1
        assert "error" in response
        assert "nonexistent" in str(response["error"])
    
    def _initialize(self):
        """Helper to initialize the session"""
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-03-26",
                "capabilities": {},
                "clientInfo": {"name": "test"}
            }
        }
        self.handler.handle_request(init_request)
        
        notification = {
            "jsonrpc": "2.0",
            "method": "initialized"
        }
        self.handler.handle_request(notification)
