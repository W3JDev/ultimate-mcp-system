"""
Base MCP Integration Class
Provides common interface for connecting to external MCP servers
"""

import json
import subprocess
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from loguru import logger


class BaseMCPIntegration(ABC):
    """Base class for MCP integrations"""

    def __init__(self, server_command: List[str], server_name: str):
        """
        Initialize MCP integration

        Args:
            server_command: Command to start the MCP server (e.g., ['npx', '-y', '@modelcontextprotocol/server-github'])
            server_name: Human-readable name for logging
        """
        self.server_command = server_command
        self.server_name = server_name
        self.process: Optional[subprocess.Popen] = None
        self.tools: List[Dict[str, Any]] = []
        self.initialized = False

    def start(self) -> bool:
        """
        Start the MCP server subprocess

        Returns:
            True if started successfully, False otherwise
        """
        try:
            logger.info(f"🚀 Starting {self.server_name} MCP server...")
            self.process = subprocess.Popen(
                self.server_command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            # Send initialize request
            init_request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "ultimate-mcp-hub", "version": "1.0.0"},
                },
            }

            self._send_request(init_request)
            response = self._read_response()

            if response and "result" in response:
                logger.info(f"✅ {self.server_name} initialized successfully")

                # Send initialized notification
                initialized_notification = {
                    "jsonrpc": "2.0",
                    "method": "notifications/initialized",
                }
                self._send_request(initialized_notification)

                # Fetch available tools
                self._fetch_tools()
                self.initialized = True
                return True
            else:
                logger.error(f"❌ Failed to initialize {self.server_name}: {response}")
                return False

        except Exception as e:
            logger.error(f"❌ Error starting {self.server_name}: {e}")
            return False

    def stop(self):
        """Stop the MCP server subprocess"""
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
                logger.info(f"🛑 {self.server_name} stopped")
            except Exception as e:
                logger.warning(f"⚠️ Error stopping {self.server_name}: {e}")
                self.process.kill()

    def _send_request(self, request: Dict[str, Any]):
        """Send JSON-RPC request to MCP server"""
        if not self.process or not self.process.stdin:
            raise RuntimeError(f"{self.server_name} process not running")

        request_str = json.dumps(request) + "\n"
        self.process.stdin.write(request_str)
        self.process.stdin.flush()

    def _read_response(self) -> Optional[Dict[str, Any]]:
        """Read JSON-RPC response from MCP server"""
        if not self.process or not self.process.stdout:
            return None

        try:
            line = self.process.stdout.readline()
            if line:
                return json.loads(line.strip())
        except json.JSONDecodeError as e:
            logger.error(f"❌ JSON decode error from {self.server_name}: {e}")
        except Exception as e:
            logger.error(f"❌ Error reading from {self.server_name}: {e}")

        return None

    def _fetch_tools(self):
        """Fetch available tools from MCP server"""
        try:
            request = {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}

            self._send_request(request)
            response = self._read_response()

            if response and "result" in response:
                self.tools = response["result"].get("tools", [])
                logger.info(
                    f"📋 {self.server_name} has {len(self.tools)} tools available"
                )
            else:
                logger.warning(f"⚠️ No tools found for {self.server_name}")

        except Exception as e:
            logger.error(f"❌ Error fetching tools from {self.server_name}: {e}")

    def list_tools(self) -> List[Dict[str, Any]]:
        """
        Get list of available tools

        Returns:
            List of tool definitions
        """
        return self.tools

    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call a tool on the MCP server

        Args:
            tool_name: Name of the tool to call
            arguments: Tool arguments

        Returns:
            Tool execution result
        """
        try:
            request = {
                "jsonrpc": "2.0",
                "id": self._next_request_id(),
                "method": "tools/call",
                "params": {"name": tool_name, "arguments": arguments},
            }

            self._send_request(request)
            response = self._read_response()

            if response and "result" in response:
                logger.info(f"✅ Tool {tool_name} executed successfully")
                return response["result"]
            elif response and "error" in response:
                logger.error(f"❌ Tool {tool_name} error: {response['error']}")
                return {"error": response["error"]}
            else:
                return {"error": "No response from MCP server"}

        except Exception as e:
            logger.error(f"❌ Error calling tool {tool_name}: {e}")
            return {"error": str(e)}

    def _next_request_id(self) -> int:
        """Generate next request ID"""
        if not hasattr(self, "_request_id"):
            self._request_id = 2  # Start at 3 (1=initialize, 2=tools/list)
        self._request_id += 1
        return self._request_id

    @abstractmethod
    def get_integration_name(self) -> str:
        """Get the integration name"""
        pass

    def __enter__(self):
        """Context manager entry"""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop()
