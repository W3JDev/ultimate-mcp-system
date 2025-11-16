"""
Rube MCP Integration
Provides access to 500+ app integrations via Rube MCP
"""

from typing import List

from .base_integration import BaseMCPIntegration


class RubeMCPIntegration(BaseMCPIntegration):
    """Integration with Rube MCP for 500+ app integrations"""

    def __init__(self):
        """Initialize Rube MCP integration"""
        # Rube MCP server command - adjust based on actual installation
        server_command = ["npx", "-y", "@rube/mcp-server"]
        super().__init__(server_command, "Rube MCP")

    def get_integration_name(self) -> str:
        """Get the integration name"""
        return "rube"

    def search_apps(self, query: str) -> List[str]:
        """
        Search available apps in Rube

        Args:
            query: Search query

        Returns:
            List of matching app names
        """
        # Use Rube's search tool if available
        result = self.call_tool("RUBE_SEARCH_TOOLS", {"query": query})

        if "error" not in result:
            return result.get("apps", [])
        return []

    def get_app_actions(self, app_name: str) -> List[str]:
        """
        Get available actions for an app

        Args:
            app_name: Name of the app

        Returns:
            List of action names
        """
        # Use Rube's action listing if available
        result = self.call_tool("RUBE_LIST_ACTIONS", {"app": app_name})

        if "error" not in result:
            return result.get("actions", [])
        return []
