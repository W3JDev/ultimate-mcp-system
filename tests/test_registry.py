"""
Unit tests for MCP Tool Registry
"""
import sys

import pytest

# Add backend to path
sys.path.insert(0, '/home/runner/work/ultimate-mcp-system/ultimate-mcp-system/backend')

from mcp_protocol.registry import ToolRegistry
from mcp_protocol.errors import ToolNotFound, ToolExecutionError


class TestToolRegistry:
    """Test tool registry functionality"""
    
    def test_register_tool(self):
        """Test registering a tool"""
        registry = ToolRegistry()
        
        def test_handler(args):
            return "test"
        
        registry.register_tool(
            name="test_tool",
            description="Test tool",
            handler=test_handler
        )
        
        assert registry.has_tool("test_tool")
    
    def test_list_tools(self):
        """Test listing registered tools"""
        registry = ToolRegistry()
        
        def handler1(args):
            return "1"
        
        def handler2(args):
            return "2"
        
        registry.register_tool("tool1", "First tool", handler1)
        registry.register_tool("tool2", "Second tool", handler2)
        
        tools = registry.list_tools()
        
        assert len(tools) == 2
        assert any(t["name"] == "tool1" for t in tools)
        assert any(t["name"] == "tool2" for t in tools)
        
        # Verify handler is not exposed
        for tool in tools:
            assert "handler" not in tool
    
    def test_has_tool(self):
        """Test checking tool existence"""
        registry = ToolRegistry()
        
        def test_handler(args):
            return "test"
        
        registry.register_tool("existing", "Exists", test_handler)
        
        assert registry.has_tool("existing")
        assert not registry.has_tool("nonexistent")
    
    def test_call_tool_success(self):
        """Test calling a tool successfully"""
        registry = ToolRegistry()
        
        def add_handler(args):
            return args["a"] + args["b"]
        
        registry.register_tool("add", "Add numbers", add_handler)
        
        result = registry.call_tool("add", {"a": 5, "b": 3})
        assert result == 8
    
    def test_call_tool_not_found(self):
        """Test calling non-existent tool"""
        registry = ToolRegistry()
        
        with pytest.raises(ToolNotFound) as exc:
            registry.call_tool("nonexistent", {})
        
        error_dict = exc.value.to_dict()
        assert "nonexistent" in str(error_dict)
    
    def test_call_tool_execution_error(self):
        """Test tool execution error handling"""
        registry = ToolRegistry()
        
        def failing_handler(args):
            raise ValueError("Tool failed")
        
        registry.register_tool("failing", "Fails", failing_handler)
        
        with pytest.raises(ToolExecutionError) as exc:
            registry.call_tool("failing", {})
        
        error_dict = exc.value.to_dict()
        assert "failing" in str(error_dict)
    
    def test_unregister_tool(self):
        """Test unregistering a tool"""
        registry = ToolRegistry()
        
        def test_handler(args):
            return "test"
        
        registry.register_tool("temp", "Temporary", test_handler)
        assert registry.has_tool("temp")
        
        registry.unregister_tool("temp")
        assert not registry.has_tool("temp")
    
    def test_clear_tools(self):
        """Test clearing all tools"""
        registry = ToolRegistry()
        
        def handler(args):
            return "test"
        
        registry.register_tool("tool1", "Tool 1", handler)
        registry.register_tool("tool2", "Tool 2", handler)
        
        assert len(registry.list_tools()) == 2
        
        registry.clear()
        assert len(registry.list_tools()) == 0
    
    def test_tool_with_schema(self):
        """Test registering tool with input schema"""
        registry = ToolRegistry()
        
        def handler(args):
            return args
        
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "number"}
            },
            "required": ["name"]
        }
        
        registry.register_tool("user", "User tool", handler, schema)
        
        tools = registry.list_tools()
        user_tool = next(t for t in tools if t["name"] == "user")
        
        assert user_tool["inputSchema"] == schema
