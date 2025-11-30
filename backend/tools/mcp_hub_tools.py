"""
MCP Hub Tools - Wraps the Ultimate MCP Hub server tools

Exposes the 11 meta-MCP tools via the orchestrator's tool registry
"""

import json
import subprocess
from pathlib import Path
from typing import Dict, Any

from loguru import logger

from .base import MCPTool, ToolSchema


class MCPHubTool(MCPTool):
    """Wrapper for MCP Hub server tools"""
    
    def __init__(self, tool_name: str, tool_schema: Dict):
        """
        Initialize MCP Hub tool wrapper
        
        Args:
            tool_name: Name of the tool
            tool_schema: Tool schema from mcp_hub_server
        """
        self.tool_name = tool_name
        self.mcp_schema = tool_schema
        
        # Convert MCP inputSchema properties to ToolParameter list
        input_schema = tool_schema.get("inputSchema", {})
        properties = input_schema.get("properties", {})
        required_fields = input_schema.get("required", [])
        
        from .base import ToolParameter
        
        parameters = []
        for param_name, param_info in properties.items():
            param = ToolParameter(
                name=param_name,
                type=param_info.get("type", "string"),
                description=param_info.get("description", ""),
                required=param_name in required_fields,
                enum=param_info.get("enum"),
                default=param_info.get("default"),
            )
            parameters.append(param)
        
        # Convert MCP schema to MCPTool schema
        schema = ToolSchema(
            name=tool_name,
            display_name=tool_name.replace("_", " ").title(),
            description=tool_schema.get("description", ""),
            category="mcp_hub",
            parameters=parameters,
            returns="Tool execution result from MCP Hub",
        )
        
        # Create handler function that calls mcp_hub_server
        def handler(**params):
            return self._call_mcp_hub(**params)
        
        super().__init__(schema, handler)
        logger.info(f"🔗 Wrapped MCP Hub tool: {tool_name}")
    
    def _call_mcp_hub(self, **params) -> Dict[str, Any]:
        """
        Call mcp_hub_server via JSON-RPC
        
        Args:
            **params: Tool parameters
        
        Returns:
            Tool execution result
        """
        try:
            # Build JSON-RPC request
            request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": self.tool_name,
                    "arguments": params
                }
            }
            
            # Get path to mcp_hub_server.py
            hub_server_path = Path(__file__).parent.parent.parent / "mcp_hub_server.py"
            
            # Call mcp_hub_server via subprocess
            logger.info(f"🚀 Calling MCP Hub tool: {self.tool_name}")
            logger.debug(f"Parameters: {params}")
            
            process = subprocess.Popen(
                ["python", str(hub_server_path)],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            
            # Send request and get response
            stdout, stderr = process.communicate(input=json.dumps(request) + "\n")
            
            if stderr:
                logger.warning(f"⚠️ MCP Hub stderr: {stderr}")
            
            # Parse response
            response = json.loads(stdout.strip())
            
            if "error" in response:
                error = response["error"]
                logger.error(f"❌ MCP Hub error: {error}")
                return {
                    "status": "error",
                    "error": error.get("message", "Unknown error"),
                    "code": error.get("code", -1),
                }
            
            result = response.get("result", {})
            logger.info(f"✅ MCP Hub tool executed: {self.tool_name}")
            
            return {
                "status": "success",
                "tool": self.tool_name,
                "result": result,
            }
            
        except Exception as e:
            logger.error(f"❌ Error executing MCP Hub tool {self.tool_name}: {e}")
            return {
                "status": "error",
                "error": str(e),
                "tool": self.tool_name,
            }


# Load MCP Hub tools by querying the server
def load_mcp_hub_tools():
    """
    Load all tools from mcp_hub_server
    
    Returns:
        List of MCPHubTool instances
    """
    try:
        logger.info("🔍 Loading MCP Hub tools...")
        
        # Get path to mcp_hub_server.py
        hub_server_path = Path(__file__).parent.parent.parent / "mcp_hub_server.py"
        
        # Query tools/list
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {}
        }
        
        process = subprocess.Popen(
            ["python", str(hub_server_path)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        
        stdout, stderr = process.communicate(input=json.dumps(request) + "\n")
        
        if stderr:
            logger.debug(f"MCP Hub init: {stderr}")
        
        # Parse response
        response = json.loads(stdout.strip())
        
        if "error" in response:
            logger.error(f"❌ Failed to load MCP Hub tools: {response['error']}")
            return []
        
        tools_list = response.get("result", {}).get("tools", [])
        logger.info(f"📦 Found {len(tools_list)} MCP Hub tools")
        
        # Create MCPHubTool wrappers
        mcp_hub_tools = []
        for tool_schema in tools_list:
            tool_name = tool_schema.get("name")
            if tool_name:
                tool = MCPHubTool(tool_name, tool_schema)
                mcp_hub_tools.append(tool)
        
        logger.info(f"✅ Loaded {len(mcp_hub_tools)} MCP Hub tools")
        return mcp_hub_tools
        
    except Exception as e:
        logger.error(f"❌ Error loading MCP Hub tools: {e}")
        return []


# Export all MCP Hub tools
MCP_HUB_TOOLS = load_mcp_hub_tools()

logger.info(f"🌟 MCP Hub Tools module loaded with {len(MCP_HUB_TOOLS)} tools")
