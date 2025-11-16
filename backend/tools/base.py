"""
Base classes for MCP Tools
Defines the interface that all MCP tools must implement
"""

from typing import Any, Callable, Dict, List, Optional
from pydantic import BaseModel, Field
from loguru import logger


class ToolParameter(BaseModel):
    """Schema for a tool parameter"""

    name: str = Field(..., description="Parameter name")
    type: str = Field(..., description="Parameter type (string, number, boolean, object, array)")
    description: str = Field(..., description="What this parameter does")
    required: bool = Field(default=True, description="Whether this parameter is required")
    default: Optional[Any] = Field(default=None, description="Default value if not required")
    enum: Optional[List[Any]] = Field(default=None, description="Allowed values (for enums)")


class ToolSchema(BaseModel):
    """Schema definition for an MCP tool"""

    name: str = Field(..., description="Tool identifier (lowercase_with_underscores)")
    display_name: str = Field(..., description="Human-readable tool name")
    description: str = Field(..., description="What this tool does")
    category: str = Field(..., description="Tool category (n8n, agent, local, cloud)")
    parameters: List[ToolParameter] = Field(default_factory=list, description="Tool parameters")
    returns: str = Field(..., description="Description of what the tool returns")
    examples: List[str] = Field(default_factory=list, description="Example usage strings")


class MCPTool:
    """
    Base class for all MCP tools
    
    Each tool represents a specific capability (e.g., create_workflow, list_files)
    Tools can be called directly or via natural language through the orchestrator
    """

    def __init__(self, schema: ToolSchema, handler: Callable):
        """
        Initialize an MCP tool
        
        Args:
            schema: Tool schema defining interface
            handler: Function that implements the tool logic
        """
        self.schema = schema
        self.handler = handler
        logger.debug(f"🔧 Initialized tool: {schema.name}")

    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the tool with given parameters
        
        Args:
            **kwargs: Tool parameters
            
        Returns:
            Result dictionary with 'success', 'data', and optionally 'error'
        """
        try:
            logger.info(f"⚙️ Executing tool: {self.schema.name}")
            result = self.handler(**kwargs)
            
            return {
                "success": True,
                "tool": self.schema.name,
                "data": result
            }
        except Exception as e:
            logger.error(f"❌ Tool {self.schema.name} failed: {e}")
            return {
                "success": False,
                "tool": self.schema.name,
                "error": str(e)
            }

    def get_schema(self) -> Dict[str, Any]:
        """Get tool schema as dictionary"""
        return self.schema.model_dump()

    def __repr__(self):
        return f"MCPTool({self.schema.name})"
