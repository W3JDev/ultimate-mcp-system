"""
Playwright MCP Integration
Provides browser automation capabilities
"""

from typing import Any, Dict, Optional

from .base_integration import BaseMCPIntegration


class PlaywrightMCPIntegration(BaseMCPIntegration):
    """Integration with Playwright MCP for browser automation"""

    def __init__(self):
        """Initialize Playwright MCP integration"""
        # Playwright MCP server command
        server_command = ["npx", "-y", "@playwright/mcp-server"]
        super().__init__(server_command, "Playwright MCP")

    def get_integration_name(self) -> str:
        """Get the integration name"""
        return "playwright"

    def navigate(self, url: str) -> Dict[str, Any]:
        """
        Navigate to a URL

        Args:
            url: URL to navigate to

        Returns:
            Navigation result
        """
        return self.call_tool("playwright_navigate", {"url": url})

    def screenshot(self, selector: Optional[str] = None) -> Dict[str, Any]:
        """
        Take a screenshot

        Args:
            selector: Optional CSS selector to screenshot specific element

        Returns:
            Screenshot data
        """
        params = {}
        if selector:
            params["selector"] = selector
        return self.call_tool("playwright_screenshot", params)

    def click(self, selector: str) -> Dict[str, Any]:
        """
        Click an element

        Args:
            selector: CSS selector of element to click

        Returns:
            Click result
        """
        return self.call_tool("playwright_click", {"selector": selector})

    def fill(self, selector: str, value: str) -> Dict[str, Any]:
        """
        Fill a form field

        Args:
            selector: CSS selector of input field
            value: Value to fill

        Returns:
            Fill result
        """
        return self.call_tool("playwright_fill", {"selector": selector, "value": value})

    def evaluate(self, expression: str) -> Dict[str, Any]:
        """
        Evaluate JavaScript in page context

        Args:
            expression: JavaScript expression to evaluate

        Returns:
            Evaluation result
        """
        return self.call_tool("playwright_evaluate", {"expression": expression})
