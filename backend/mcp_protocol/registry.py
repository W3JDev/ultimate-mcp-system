"""
MCP Tool Registry
Manages registration and execution of tools
"""
import sys
from typing import Any, Callable, Dict, List, Optional

from loguru import logger

from .errors import ToolExecutionError, ToolNotFound


class ToolRegistry:
    """Registry for managing MCP tools"""
    
    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}
        logger.info("🔧 Tool registry initialized", file=sys.stderr)
    
    def register_tool(
        self,
        name: str,
        description: str,
        handler: Callable,
        input_schema: Optional[Dict[str, Any]] = None
    ):
        """
        Register a new tool
        
        Args:
            name: Tool identifier
            description: Human-readable description
            handler: Function to execute when tool is called
            input_schema: JSON schema for tool inputs (optional)
        """
        self.tools[name] = {
            "name": name,
            "description": description,
            "handler": handler,
            "inputSchema": input_schema or {
                "type": "object",
                "properties": {}
            }
        }
        logger.info(f"✅ Registered tool: {name}", file=sys.stderr)
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """
        List all registered tools
        
        Returns:
            List of tool metadata (without handlers)
        """
        return [
            {
                "name": tool["name"],
                "description": tool["description"],
                "inputSchema": tool["inputSchema"]
            }
            for tool in self.tools.values()
        ]
    
    def has_tool(self, name: str) -> bool:
        """Check if tool exists"""
        return name in self.tools
    
    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool with given arguments
        
        Args:
            name: Tool name
            arguments: Tool input parameters
            
        Returns:
            Tool execution result
            
        Raises:
            ToolNotFound: If tool doesn't exist
            ToolExecutionError: If tool execution fails
        """
        if not self.has_tool(name):
            raise ToolNotFound(name)
        
        tool = self.tools[name]
        handler = tool["handler"]
        
        try:
            logger.info(f"🔧 Executing tool: {name}", file=sys.stderr)
            result = handler(arguments)
            logger.info(f"✅ Tool {name} completed", file=sys.stderr)
            return result
        except Exception as e:
            logger.error(f"❌ Tool {name} failed: {str(e)}", file=sys.stderr)
            raise ToolExecutionError(name, str(e))
    
    def unregister_tool(self, name: str):
        """Remove a tool from registry"""
        if name in self.tools:
            del self.tools[name]
            logger.info(f"🗑️ Unregistered tool: {name}", file=sys.stderr)
    
    def clear(self):
        """Remove all tools"""
        self.tools.clear()
        logger.info("🗑️ Cleared all tools", file=sys.stderr)
