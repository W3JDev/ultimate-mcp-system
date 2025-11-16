"""
Integration Tests for MCP Hub Server
Tests connection to external MCP servers
"""

import json
import unittest
from unittest.mock import MagicMock, patch

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from integrations import (
    GitHubMCPIntegration,
    MemoryMCPIntegration,
    PlaywrightMCPIntegration,
    RubeMCPIntegration,
)


class TestBaseMCPIntegration(unittest.TestCase):
    """Test base MCP integration functionality"""

    def test_integration_initialization(self):
        """Test that integrations can be initialized"""
        # Test Rube integration
        rube = RubeMCPIntegration()
        self.assertEqual(rube.get_integration_name(), "rube")
        self.assertEqual(rube.server_name, "Rube MCP")

        # Test Memory integration
        memory = MemoryMCPIntegration()
        self.assertEqual(memory.get_integration_name(), "memory")
        self.assertEqual(memory.server_name, "Memory MCP")

        # Test GitHub integration
        github = GitHubMCPIntegration()
        self.assertEqual(github.get_integration_name(), "github")
        self.assertEqual(github.server_name, "GitHub MCP")

        # Test Playwright integration
        playwright = PlaywrightMCPIntegration()
        self.assertEqual(playwright.get_integration_name(), "playwright")
        self.assertEqual(playwright.server_name, "Playwright MCP")


class TestRubeMCPIntegration(unittest.TestCase):
    """Test Rube MCP integration"""

    def setUp(self):
        """Set up test fixtures"""
        self.integration = RubeMCPIntegration()

    @patch.object(RubeMCPIntegration, "call_tool")
    def test_search_apps(self, mock_call_tool):
        """Test searching for apps"""
        mock_call_tool.return_value = {"apps": ["slack", "github", "gmail"]}

        result = self.integration.search_apps("messaging")

        self.assertEqual(len(result), 3)
        self.assertIn("slack", result)
        mock_call_tool.assert_called_once_with("RUBE_SEARCH_TOOLS", {"query": "messaging"})

    @patch.object(RubeMCPIntegration, "call_tool")
    def test_get_app_actions(self, mock_call_tool):
        """Test getting app actions"""
        mock_call_tool.return_value = {"actions": ["send_message", "get_channels"]}

        result = self.integration.get_app_actions("slack")

        self.assertEqual(len(result), 2)
        self.assertIn("send_message", result)
        mock_call_tool.assert_called_once_with("RUBE_LIST_ACTIONS", {"app": "slack"})


class TestMemoryMCPIntegration(unittest.TestCase):
    """Test Memory MCP integration"""

    def setUp(self):
        """Set up test fixtures"""
        self.integration = MemoryMCPIntegration()

    @patch.object(MemoryMCPIntegration, "call_tool")
    def test_create_entities(self, mock_call_tool):
        """Test creating entities"""
        mock_call_tool.return_value = {"created": 2}

        entities = [
            {"name": "John", "type": "person"},
            {"name": "Acme Corp", "type": "company"},
        ]

        result = self.integration.create_entities(entities)

        self.assertEqual(result["created"], 2)
        mock_call_tool.assert_called_once_with("create_entities", {"entities": entities})

    @patch.object(MemoryMCPIntegration, "call_tool")
    def test_search_nodes(self, mock_call_tool):
        """Test searching nodes"""
        mock_call_tool.return_value = {"nodes": [{"name": "John", "type": "person"}]}

        result = self.integration.search_nodes("John")

        self.assertIn("nodes", result)
        mock_call_tool.assert_called_once_with("search_nodes", {"query": "John"})


class TestGitHubMCPIntegration(unittest.TestCase):
    """Test GitHub MCP integration"""

    def setUp(self):
        """Set up test fixtures"""
        self.integration = GitHubMCPIntegration()

    @patch.object(GitHubMCPIntegration, "call_tool")
    def test_create_repository(self, mock_call_tool):
        """Test creating a repository"""
        mock_call_tool.return_value = {"url": "https://github.com/user/repo"}

        result = self.integration.create_repository(
            "test-repo", description="Test repository", private=False
        )

        self.assertIn("url", result)
        mock_call_tool.assert_called_once()

    @patch.object(GitHubMCPIntegration, "call_tool")
    def test_create_issue(self, mock_call_tool):
        """Test creating an issue"""
        mock_call_tool.return_value = {"number": 1, "url": "https://github.com/user/repo/issues/1"}

        result = self.integration.create_issue(
            "user/repo", title="Bug found", body="Description", labels=["bug"]
        )

        self.assertIn("number", result)
        mock_call_tool.assert_called_once()


class TestPlaywrightMCPIntegration(unittest.TestCase):
    """Test Playwright MCP integration"""

    def setUp(self):
        """Set up test fixtures"""
        self.integration = PlaywrightMCPIntegration()

    @patch.object(PlaywrightMCPIntegration, "call_tool")
    def test_navigate(self, mock_call_tool):
        """Test navigation"""
        mock_call_tool.return_value = {"success": True}

        result = self.integration.navigate("https://example.com")

        self.assertTrue(result["success"])
        mock_call_tool.assert_called_once_with("playwright_navigate", {"url": "https://example.com"})

    @patch.object(PlaywrightMCPIntegration, "call_tool")
    def test_click(self, mock_call_tool):
        """Test clicking an element"""
        mock_call_tool.return_value = {"success": True}

        result = self.integration.click("#button")

        self.assertTrue(result["success"])
        mock_call_tool.assert_called_once_with("playwright_click", {"selector": "#button"})


class TestMCPHubServer(unittest.TestCase):
    """Test MCP Hub Server"""

    def setUp(self):
        """Set up test fixtures"""
        # Import here to avoid issues if module has initialization code
        from mcp_hub_server import MCPHubServer

        self.server = MCPHubServer()

    def test_server_initialization(self):
        """Test server initializes correctly"""
        self.assertEqual(self.server.server_info["name"], "ultimate-mcp-hub")
        self.assertEqual(self.server.server_info["version"], "1.0.0")
        self.assertFalse(self.server.initialized)

    def test_handle_initialize(self):
        """Test initialize request handling"""
        params = {
            "protocolVersion": "2024-11-05",
            "clientInfo": {"name": "test-client", "version": "1.0.0"},
        }

        result = self.server._handle_initialize(params)

        self.assertIn("protocolVersion", result)
        self.assertIn("capabilities", result)
        self.assertIn("serverInfo", result)

    def test_handle_tools_list(self):
        """Test tools/list request handling"""
        result = self.server._handle_tools_list({})

        self.assertIn("tools", result)
        self.assertIsInstance(result["tools"], list)
        # Should have at least custom tools
        self.assertGreater(len(result["tools"]), 0)

    def test_custom_tools_defined(self):
        """Test that custom tools are properly defined"""
        tools = self.server._get_custom_tools()

        self.assertGreater(len(tools), 0)

        # Check that each tool has required fields
        for tool in tools:
            self.assertIn("name", tool)
            self.assertIn("description", tool)
            self.assertIn("inputSchema", tool)


if __name__ == "__main__":
    unittest.main()
