"""
Integration tests for MCP tools
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools import ToolRegistry, N8N_TOOLS, AGENT_TOOLS, LOCAL_TOOLS


def test_tool_imports():
    """Test that all tool modules can be imported"""
    assert len(N8N_TOOLS) == 4, f"Expected 4 N8N tools, got {len(N8N_TOOLS)}"
    assert len(AGENT_TOOLS) == 6, f"Expected 6 Agent tools, got {len(AGENT_TOOLS)}"
    assert len(LOCAL_TOOLS) == 7, f"Expected 7 Local tools, got {len(LOCAL_TOOLS)}"
    print("✅ Tool imports test passed")


def test_tool_registry_registration():
    """Test tool registration in registry"""
    registry = ToolRegistry()
    
    # Register all tools
    for tool in N8N_TOOLS + AGENT_TOOLS + LOCAL_TOOLS:
        registry.register(tool)
    
    assert len(registry) == 17, f"Expected 17 tools, got {len(registry)}"
    
    # Check categories
    categories = registry.get_categories()
    assert categories["n8n"] == 4, f"Expected 4 N8N tools, got {categories['n8n']}"
    assert categories["agent"] == 6, f"Expected 6 Agent tools, got {categories['agent']}"
    assert categories["local"] == 7, f"Expected 7 Local tools, got {categories['local']}"
    
    print("✅ Tool registry registration test passed")


def test_tool_listing():
    """Test listing tools by category"""
    registry = ToolRegistry()
    
    for tool in N8N_TOOLS + AGENT_TOOLS + LOCAL_TOOLS:
        registry.register(tool)
    
    # List all tools
    all_tools = registry.list_tools()
    assert len(all_tools) == 17, f"Expected 17 tools, got {len(all_tools)}"
    
    # List by category
    n8n_tools = registry.list_tools(category="n8n")
    assert len(n8n_tools) == 4, f"Expected 4 N8N tools, got {len(n8n_tools)}"
    
    agent_tools = registry.list_tools(category="agent")
    assert len(agent_tools) == 6, f"Expected 6 Agent tools, got {len(agent_tools)}"
    
    local_tools = registry.list_tools(category="local")
    assert len(local_tools) == 7, f"Expected 7 Local tools, got {len(local_tools)}"
    
    print("✅ Tool listing test passed")


def test_tool_search():
    """Test searching for tools"""
    registry = ToolRegistry()
    
    for tool in N8N_TOOLS + AGENT_TOOLS + LOCAL_TOOLS:
        registry.register(tool)
    
    # Search for "file" tools
    file_tools = registry.search_tools("file")
    assert len(file_tools) >= 2, f"Expected at least 2 file-related tools, got {len(file_tools)}"
    
    # Search for "agent" tools
    agent_tools = registry.search_tools("agent")
    assert len(agent_tools) >= 5, f"Expected at least 5 agent-related tools, got {len(agent_tools)}"
    
    print("✅ Tool search test passed")


def test_tool_execution_system_info():
    """Test executing get_system_info tool"""
    registry = ToolRegistry()
    
    for tool in LOCAL_TOOLS:
        registry.register(tool)
    
    result = registry.execute_tool("get_system_info")
    
    assert result["success"] is True, "Tool execution should succeed"
    assert "data" in result, "Result should contain data"
    assert "os" in result["data"], "Result should contain OS info"
    assert "cpu" in result["data"], "Result should contain CPU info"
    assert "memory" in result["data"], "Result should contain memory info"
    
    print("✅ Tool execution (system_info) test passed")


def test_tool_execution_create_agent():
    """Test executing create_adk_agent tool"""
    registry = ToolRegistry()
    
    for tool in AGENT_TOOLS:
        registry.register(tool)
    
    result = registry.execute_tool(
        "create_adk_agent",
        name="test_agent",
        model="gpt-4",
        tools=["github", "slack"],
        system_prompt="Test agent"
    )
    
    assert result["success"] is True, "Tool execution should succeed"
    assert "data" in result, "Result should contain data"
    assert result["data"]["type"] == "ADK", "Agent should be ADK type"
    assert result["data"]["name"] == "test_agent", "Agent name should match"
    
    print("✅ Tool execution (create_agent) test passed")


def test_tool_schema_structure():
    """Test that all tools have proper schema structure"""
    registry = ToolRegistry()
    
    for tool in N8N_TOOLS + AGENT_TOOLS + LOCAL_TOOLS:
        registry.register(tool)
    
    all_tools = registry.list_tools()
    
    for tool_schema in all_tools:
        # Check required fields
        assert "name" in tool_schema, "Tool must have name"
        assert "display_name" in tool_schema, "Tool must have display_name"
        assert "description" in tool_schema, "Tool must have description"
        assert "category" in tool_schema, "Tool must have category"
        assert "parameters" in tool_schema, "Tool must have parameters"
        assert "returns" in tool_schema, "Tool must have returns"
        assert "examples" in tool_schema, "Tool must have examples"
        
        # Check parameter structure
        for param in tool_schema["parameters"]:
            assert "name" in param, "Parameter must have name"
            assert "type" in param, "Parameter must have type"
            assert "description" in param, "Parameter must have description"
            assert "required" in param, "Parameter must have required field"
    
    print("✅ Tool schema structure test passed")


def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("Running MCP Tools Integration Tests")
    print("=" * 60 + "\n")
    
    try:
        test_tool_imports()
        test_tool_registry_registration()
        test_tool_listing()
        test_tool_search()
        test_tool_execution_system_info()
        test_tool_execution_create_agent()
        test_tool_schema_structure()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED")
        print("=" * 60 + "\n")
        return True
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}\n")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
