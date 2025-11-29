"""
Tool Registry - Manages all registered MCP tools
"""

from typing import Dict, List, Optional

from loguru import logger

from .base import MCPTool, ToolSchema


class ToolRegistry:
    """
    Central registry for all MCP tools

    Provides tool discovery, registration, and execution
    """

    def __init__(self):
        """Initialize empty tool registry"""
        self._tools: Dict[str, MCPTool] = {}
        self._categories: Dict[str, List[str]] = {
            "n8n": [],
            "agent": [],
            "local": [],
            "cloud": [],
        }
        logger.info("📚 Tool Registry initialized")

    def register(self, tool: MCPTool) -> None:
        """
        Register a new tool

        Args:
            tool: MCPTool instance to register
        """
        tool_name = tool.schema.name
        category = tool.schema.category

        if tool_name in self._tools:
            logger.warning(f"⚠️ Tool {tool_name} already registered, overwriting")

        self._tools[tool_name] = tool

        if category in self._categories and tool_name not in self._categories[category]:
            self._categories[category].append(tool_name)

        logger.info(f"✅ Registered tool: {tool_name} (category: {category})")

    def get_tool(self, name: str) -> Optional[MCPTool]:
        """
        Get a tool by name

        Args:
            name: Tool name

        Returns:
            MCPTool instance or None if not found
        """
        return self._tools.get(name)

    def get_by_category(self, category: str) -> List[MCPTool]:
        """
        Get all tools in a specific category

        Args:
            category: Category name (n8n, agent, local, cloud)

        Returns:
            List of MCPTool instances in that category
        """
        tool_names = self._categories.get(category, [])
        return [self._tools[name] for name in tool_names if name in self._tools]

    def list_tools(self, category: Optional[str] = None) -> List[Dict]:
        """
        List all tools or tools in a specific category

        Args:
            category: Optional category filter

        Returns:
            List of tool schemas
        """
        if category:
            tool_names = self._categories.get(category, [])
            tools = [self._tools[name] for name in tool_names if name in self._tools]
        else:
            tools = list(self._tools.values())

        return [tool.get_schema() for tool in tools]

    def execute_tool(self, tool_name: str, **kwargs) -> Dict:
        """
        Execute a tool by name

        Args:
            tool_name: Tool name
            **kwargs: Tool parameters

        Returns:
            Execution result
        """
        tool = self.get_tool(tool_name)

        if not tool:
            return {"success": False, "error": f"Tool '{tool_name}' not found"}

        return tool.execute(**kwargs)

    def get_categories(self) -> Dict[str, int]:
        """
        Get tool categories with counts

        Returns:
            Dictionary of category: count
        """
        return {category: len(tools) for category, tools in self._categories.items()}

    def search_tools(self, query: str) -> List[Dict]:
        """
        Search tools by name or description

        Args:
            query: Search query

        Returns:
            List of matching tool schemas
        """
        query = query.lower()
        matching_tools = []

        for tool in self._tools.values():
            schema = tool.schema
            if (
                query in schema.name.lower()
                or query in schema.display_name.lower()
                or query in schema.description.lower()
            ):
                matching_tools.append(tool.get_schema())

        return matching_tools

    def __len__(self):
        """Return number of registered tools"""
        return len(self._tools)

    def __repr__(self):
        return f"ToolRegistry({len(self._tools)} tools)"
