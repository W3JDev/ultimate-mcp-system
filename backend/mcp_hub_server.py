#!/usr/bin/env python3
"""
MCP Hub Server - Aggregates Multiple MCP Servers
Implements JSON-RPC 2.0 over stdio protocol
Combines tools from Rube, Memory, GitHub, Playwright and custom servers
"""

import json
import os
import sys
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from integrations import (
    GitHubMCPIntegration,
    MemoryMCPIntegration,
    PlaywrightMCPIntegration,
    RubeMCPIntegration,
)
from loguru import logger

# Load environment variables
load_dotenv()

# Configure logging to file only (not stdout, which is used for JSON-RPC)
logger.remove()
logger.add("logs/mcp_hub.log", rotation="1 day", retention="7 days")


class MCPHubServer:
    """MCP Hub Server that aggregates multiple MCP servers"""

    def __init__(self):
        """Initialize MCP Hub Server"""
        self.integrations: Dict[str, Any] = {}
        self.server_info = {
            "name": "ultimate-mcp-hub",
            "version": "1.0.0",
            "protocolVersion": "2024-11-05",
        }
        self.capabilities = {
            "tools": {},
            "resources": {},
            "prompts": {},
        }
        self.initialized = False

        logger.info("🚀 MCP Hub Server initializing...")

    def start_integrations(self):
        """Start all MCP integrations"""
        logger.info("📡 Starting MCP integrations...")

        # Initialize integrations (will fail gracefully if not available)
        integrations_config = [
            ("rube", RubeMCPIntegration),
            ("memory", MemoryMCPIntegration),
            ("github", GitHubMCPIntegration),
            ("playwright", PlaywrightMCPIntegration),
        ]

        for name, integration_class in integrations_config:
            try:
                integration = integration_class()
                if integration.start():
                    self.integrations[name] = integration
                    logger.info(f"✅ {name} integration started")
                else:
                    logger.warning(f"⚠️ {name} integration failed to start")
            except Exception as e:
                logger.warning(f"⚠️ Could not start {name} integration: {e}")

        logger.info(
            f"📋 {len(self.integrations)} integrations active: {list(self.integrations.keys())}"
        )

    def stop_integrations(self):
        """Stop all MCP integrations"""
        logger.info("🛑 Stopping MCP integrations...")
        for name, integration in self.integrations.items():
            try:
                integration.stop()
                logger.info(f"✅ {name} integration stopped")
            except Exception as e:
                logger.error(f"❌ Error stopping {name}: {e}")

    def handle_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Handle JSON-RPC request

        Args:
            request: JSON-RPC request

        Returns:
            JSON-RPC response or None for notifications
        """
        method = request.get("method")
        request_id = request.get("id")
        params = request.get("params", {})

        logger.info(f"📥 Request: {method} (id={request_id})")

        try:
            # Handle methods
            if method == "initialize":
                result = self._handle_initialize(params)
            elif method == "notifications/initialized":
                self._handle_initialized()
                return None  # Notifications don't return responses
            elif method == "tools/list":
                result = self._handle_tools_list(params)
            elif method == "tools/call":
                result = self._handle_tools_call(params)
            elif method == "ping":
                result = {}
            else:
                raise ValueError(f"Unknown method: {method}")

            # Return success response
            if request_id is not None:
                return {"jsonrpc": "2.0", "id": request_id, "result": result}

        except Exception as e:
            logger.error(f"❌ Error handling {method}: {e}")
            if request_id is not None:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -32603, "message": str(e)},
                }

        return None

    def _handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle initialize request"""
        logger.info("🔧 Initializing MCP Hub Server...")

        client_info = params.get("clientInfo", {})
        logger.info(
            f"📱 Client: {client_info.get('name', 'unknown')} v{client_info.get('version', 'unknown')}"
        )

        # Start integrations
        self.start_integrations()

        return {
            "protocolVersion": self.server_info["protocolVersion"],
            "capabilities": self.capabilities,
            "serverInfo": {
                "name": self.server_info["name"],
                "version": self.server_info["version"],
            },
        }

    def _handle_initialized(self):
        """Handle initialized notification"""
        self.initialized = True
        logger.info("✅ MCP Hub Server initialized successfully")

    def _handle_tools_list(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle tools/list request
        Aggregates tools from all connected MCP servers
        """
        logger.info("📋 Listing all available tools...")

        all_tools = []

        # Collect tools from each integration
        for name, integration in self.integrations.items():
            try:
                tools = integration.list_tools()
                # Prefix tool names with integration name to avoid conflicts
                for tool in tools:
                    tool_copy = tool.copy()
                    tool_copy["name"] = f"{name}_{tool['name']}"
                    tool_copy["description"] = (
                        f"[{name.upper()}] {tool.get('description', '')}"
                    )
                    all_tools.append(tool_copy)

                logger.info(f"  ✅ {name}: {len(tools)} tools")
            except Exception as e:
                logger.error(f"  ❌ Error getting tools from {name}: {e}")

        # Add custom tools from this system (N8N, Agent Builder, Local Control)
        custom_tools = self._get_custom_tools()
        all_tools.extend(custom_tools)
        logger.info(f"  ✅ custom: {len(custom_tools)} tools")

        logger.info(f"📊 Total tools available: {len(all_tools)}")

        return {"tools": all_tools}

    def _handle_tools_call(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle tools/call request
        Routes to appropriate MCP server or custom handler
        """
        tool_name = params.get("name", "")
        arguments = params.get("arguments", {})

        logger.info(f"🔧 Calling tool: {tool_name}")

        # Determine which integration to route to based on tool name prefix
        if "_" in tool_name:
            integration_name, actual_tool_name = tool_name.split("_", 1)

            if integration_name in self.integrations:
                # Route to external MCP integration
                integration = self.integrations[integration_name]
                result = integration.call_tool(actual_tool_name, arguments)
                return result
            elif integration_name == "custom":
                # Route to custom tools
                return self._call_custom_tool(actual_tool_name, arguments)

        # Tool not found
        raise ValueError(f"Tool not found: {tool_name}")

    def _get_custom_tools(self) -> List[Dict[str, Any]]:
        """Get custom tools from this system (N8N, Agent Builder, Local Control)"""
        return [
            {
                "name": "custom_create_n8n_workflow",
                "description": "[CUSTOM] Create an N8N workflow from natural language description",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "description": {
                            "type": "string",
                            "description": "Natural language description of the workflow",
                        },
                        "trigger": {
                            "type": "string",
                            "description": "Workflow trigger type (webhook, schedule, manual)",
                        },
                    },
                    "required": ["description"],
                },
            },
            {
                "name": "custom_create_adk_agent",
                "description": "[CUSTOM] Create an ADK agent with specified tools and model",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Agent name"},
                        "tools": {
                            "type": "array",
                            "description": "List of tools the agent can use",
                        },
                        "model": {
                            "type": "string",
                            "description": "AI model to use (gpt-4, claude-3, etc.)",
                        },
                    },
                    "required": ["name"],
                },
            },
            {
                "name": "custom_execute_system_command",
                "description": "[CUSTOM] Execute a system command on the local PC",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "command": {
                            "type": "string",
                            "description": "Command to execute",
                        }
                    },
                    "required": ["command"],
                },
            },
            {
                "name": "custom_list_processes",
                "description": "[CUSTOM] List running processes on the local PC",
                "inputSchema": {"type": "object", "properties": {}},
            },
            {
                "name": "custom_file_operation",
                "description": "[CUSTOM] Perform file operations (list, read, write)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "operation": {
                            "type": "string",
                            "enum": ["list", "read", "write"],
                            "description": "Operation to perform",
                        },
                        "path": {
                            "type": "string",
                            "description": "File or directory path",
                        },
                        "content": {
                            "type": "string",
                            "description": "Content to write (for write operation)",
                        },
                    },
                    "required": ["operation", "path"],
                },
            },
        ]

    def _call_custom_tool(
        self, tool_name: str, arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Call a custom tool from this system"""
        # Import custom server modules
        try:
            if tool_name.startswith("create_n8n"):
                return self._handle_n8n_tool(tool_name, arguments)
            elif tool_name.startswith("create_adk") or tool_name.startswith(
                "create_crewai"
            ):
                return self._handle_agent_tool(tool_name, arguments)
            elif (
                tool_name.startswith("execute_system")
                or tool_name.startswith("list_processes")
                or tool_name.startswith("file_operation")
            ):
                return self._handle_local_tool(tool_name, arguments)
            else:
                raise ValueError(f"Unknown custom tool: {tool_name}")
        except Exception as e:
            logger.error(f"❌ Error calling custom tool {tool_name}: {e}")
            return {"error": str(e)}

    def _handle_n8n_tool(
        self, tool_name: str, arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle N8N workflow tools"""
        # Placeholder - would integrate with actual N8N MCP server
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"N8N tool {tool_name} called with args: {arguments}\n(Integration pending)",
                }
            ]
        }

    def _handle_agent_tool(
        self, tool_name: str, arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle agent builder tools"""
        # Placeholder - would integrate with actual Agent Builder MCP server
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Agent tool {tool_name} called with args: {arguments}\n(Integration pending)",
                }
            ]
        }

    def _handle_local_tool(
        self, tool_name: str, arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle local control tools"""
        # Placeholder - would integrate with actual Local Control MCP server
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Local tool {tool_name} called with args: {arguments}\n(Integration pending)",
                }
            ]
        }

    def run(self):
        """Run the MCP server (stdio transport)"""
        logger.info("🚀 MCP Hub Server starting...")

        try:
            # Read from stdin, write to stdout
            for line in sys.stdin:
                try:
                    request = json.loads(line.strip())
                    response = self.handle_request(request)

                    if response:
                        # Write response to stdout
                        sys.stdout.write(json.dumps(response) + "\n")
                        sys.stdout.flush()

                except json.JSONDecodeError as e:
                    logger.error(f"❌ Invalid JSON: {e}")
                    error_response = {
                        "jsonrpc": "2.0",
                        "id": None,
                        "error": {"code": -32700, "message": "Parse error"},
                    }
                    sys.stdout.write(json.dumps(error_response) + "\n")
                    sys.stdout.flush()

        except KeyboardInterrupt:
            logger.info("⚠️ Shutting down...")
        finally:
            self.stop_integrations()

        logger.info("✅ MCP Hub Server stopped")


def main():
    """Main entry point"""
    server = MCPHubServer()
    server.run()


if __name__ == "__main__":
    main()
