"""
Remote PC Bridge - Connects Cloud Run to Remote PC via WebSocket
Allows Cloud Run to execute local commands on remote PC through Rust Desktop
"""

import asyncio
import json
import os
from typing import Any, Dict

import websockets
from loguru import logger


class RemotePCBridge:
    """Bridge between Cloud Run and Remote PC"""

    def __init__(self, bridge_url: str = None, auth_token: str = None):
        """
        Initialize bridge

        Args:
            bridge_url: WebSocket URL of remote PC agent
            auth_token: Authentication token
        """
        self.bridge_url = bridge_url or os.getenv(
            "REMOTE_PC_BRIDGE_URL", "ws://localhost:8765"
        )
        self.auth_token = auth_token or os.getenv("REMOTE_PC_AUTH_TOKEN")
        self.websocket = None
        logger.info(f"🌉 Remote PC Bridge initialized: {self.bridge_url}")

    async def connect(self):
        """Connect to remote PC via WebSocket"""
        try:
            self.websocket = await websockets.connect(
                self.bridge_url,
                extra_headers={"Authorization": f"Bearer {self.auth_token}"},
            )
            logger.info("✅ Connected to remote PC")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to connect to remote PC: {e}")
            return False

    async def execute_command(self, command: str, timeout: int = 30) -> Dict[str, Any]:
        """
        Execute command on remote PC

        Args:
            command: Command to execute
            timeout: Timeout in seconds

        Returns:
            Command result
        """
        if not self.websocket:
            await self.connect()

        if not self.websocket:
            return {"error": "Not connected to remote PC"}

        try:
            # Send command
            request = {"type": "execute", "command": command, "timeout": timeout}

            await self.websocket.send(json.dumps(request))
            logger.info(f"📤 Sent command to remote PC: {command}")

            # Wait for response
            response = await asyncio.wait_for(
                self.websocket.recv(), timeout=timeout + 5
            )

            result = json.loads(response)
            logger.info(f"📥 Received response from remote PC")

            return result

        except asyncio.TimeoutError:
            return {"error": f"Command timed out after {timeout}s"}
        except Exception as e:
            logger.error(f"❌ Command execution failed: {e}")
            return {"error": str(e)}

    async def list_files(self, path: str) -> Dict[str, Any]:
        """List files on remote PC"""
        return await self.execute_command(f"list_files:{path}")

    async def get_system_info(self) -> Dict[str, Any]:
        """Get remote PC system information"""
        return await self.execute_command("system_info")

    async def close(self):
        """Close connection"""
        if self.websocket:
            await self.websocket.close()
            logger.info("🔌 Disconnected from remote PC")


# Synchronous wrapper for FastAPI
class RemotePCClient:
    """Synchronous client for Remote PC operations"""

    def __init__(self):
        self.bridge = RemotePCBridge()

    def execute_command(self, command: str, timeout: int = 30) -> Dict[str, Any]:
        """Execute command (sync)"""
        return asyncio.run(self.bridge.execute_command(command, timeout))

    def list_files(self, path: str) -> Dict[str, Any]:
        """List files (sync)"""
        return asyncio.run(self.bridge.list_files(path))

    def get_system_info(self) -> Dict[str, Any]:
        """Get system info (sync)"""
        return asyncio.run(self.bridge.get_system_info())


if __name__ == "__main__":
    # Test connection
    import sys

    async def test():
        bridge = RemotePCBridge()
        connected = await bridge.connect()

        if connected:
            print("✅ Connected successfully")

            # Test command
            result = await bridge.execute_command("echo Hello from remote PC!")
            print(f"Result: {result}")

            await bridge.close()
        else:
            print("❌ Connection failed")
            sys.exit(1)

    asyncio.run(test())
