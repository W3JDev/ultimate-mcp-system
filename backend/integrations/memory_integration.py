"""
Memory MCP Integration
Provides knowledge graph and memory capabilities
"""

from typing import Any, Dict, List

from .base_integration import BaseMCPIntegration


class MemoryMCPIntegration(BaseMCPIntegration):
    """Integration with Memory MCP for knowledge graph"""

    def __init__(self):
        """Initialize Memory MCP integration"""
        # Memory MCP server command
        server_command = ["npx", "-y", "@modelcontextprotocol/server-memory"]
        super().__init__(server_command, "Memory MCP")

    def get_integration_name(self) -> str:
        """Get the integration name"""
        return "memory"

    def create_entities(self, entities: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create entities in knowledge graph

        Args:
            entities: List of entities to create

        Returns:
            Creation result
        """
        return self.call_tool("create_entities", {"entities": entities})

    def create_relations(self, relations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create relations between entities

        Args:
            relations: List of relations to create

        Returns:
            Creation result
        """
        return self.call_tool("create_relations", {"relations": relations})

    def search_nodes(self, query: str) -> Dict[str, Any]:
        """
        Search for nodes in knowledge graph

        Args:
            query: Search query

        Returns:
            Search results
        """
        return self.call_tool("search_nodes", {"query": query})

    def open_nodes(self, names: List[str]) -> Dict[str, Any]:
        """
        Open specific nodes by name

        Args:
            names: List of node names

        Returns:
            Node data
        """
        return self.call_tool("open_nodes", {"names": names})
