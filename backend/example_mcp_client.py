#!/usr/bin/env python3
"""
Example MCP Client
Demonstrates how to interact with the MCP Hub Server
"""

import json
import subprocess
import sys

from loguru import logger

logger.add("logs/example_client.log", rotation="1 day")


class MCPClient:
    """Simple MCP client for testing"""

    def __init__(self, server_command):
        """
        Initialize MCP client

        Args:
            server_command: Command to start MCP server
        """
        self.process = subprocess.Popen(
            server_command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        self.request_id = 0

    def send_request(self, method, params=None):
        """Send JSON-RPC request to server"""
        self.request_id += 1
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
            "params": params or {},
        }

        logger.info(f"📤 Sending: {method}")
        request_str = json.dumps(request) + "\n"
        self.process.stdin.write(request_str)
        self.process.stdin.flush()

        # Read response
        response_line = self.process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            logger.info(f"📥 Received: {response.get('result', response.get('error'))}")
            return response

        return None

    def close(self):
        """Close connection to server"""
        if self.process:
            self.process.terminate()
            self.process.wait(timeout=5)


def main():
    """Demonstrate MCP Hub usage"""
    print("🚀 MCP Hub Client Demo")
    print("=" * 60)

    # Start MCP Hub Server
    print("\n1. Starting MCP Hub Server...")
    client = MCPClient(["python", "mcp_hub_server.py"])

    try:
        # Initialize
        print("\n2. Initializing connection...")
        init_response = client.send_request(
            "initialize",
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "example-client", "version": "1.0.0"},
            },
        )

        if init_response and "result" in init_response:
            server_info = init_response["result"].get("serverInfo", {})
            print(
                f"   ✅ Connected to {server_info.get('name')} v{server_info.get('version')}"
            )

            # Send initialized notification
            client.send_request("notifications/initialized")

            # List available tools
            print("\n3. Fetching available tools...")
            tools_response = client.send_request("tools/list")

            if tools_response and "result" in tools_response:
                tools = tools_response["result"].get("tools", [])
                print(f"   ✅ Found {len(tools)} tools")

                # Show first 10 tools
                print("\n   Sample tools:")
                for i, tool in enumerate(tools[:10], 1):
                    print(
                        f"   {i}. {tool['name']}: {tool.get('description', 'No description')[:60]}..."
                    )

                # Test calling a custom tool
                print("\n4. Testing tool call...")
                call_response = client.send_request(
                    "tools/call",
                    {
                        "name": "custom_list_processes",
                        "arguments": {},
                    },
                )

                if call_response and "result" in call_response:
                    print("   ✅ Tool executed successfully")
                    result = call_response["result"]
                    print(f"   Result: {json.dumps(result, indent=2)[:200]}...")

        print("\n" + "=" * 60)
        print("✅ Demo completed successfully!")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()

    finally:
        print("\n5. Closing connection...")
        client.close()
        print("   ✅ Connection closed")


if __name__ == "__main__":
    main()
