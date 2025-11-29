"""
Local PC Agent - Runs on remote PC and accepts commands via WebSocket
Works with Rust Desktop or any remote connection

Usage:
    python backend/local_agent.py --port 8765 --token YOUR_SECRET_TOKEN
"""

import argparse
import asyncio
import json
import os
import platform
import subprocess
from pathlib import Path
from typing import Any, Dict

import psutil
import websockets
from loguru import logger


class LocalPCAgent:
    """Agent that runs on local PC and executes commands"""

    def __init__(self, auth_token: str):
        """
        Initialize agent

        Args:
            auth_token: Authentication token for security
        """
        self.auth_token = auth_token
        logger.info("🖥️ Local PC Agent initialized")

    async def handle_client(self, websocket, path):
        """Handle incoming WebSocket connection"""
        # Authenticate
        try:
            auth_header = websocket.request_headers.get("Authorization")
            if not auth_header or auth_header != f"Bearer {self.auth_token}":
                logger.warning("⚠️ Unauthorized connection attempt")
                await websocket.close(1008, "Unauthorized")
                return

            logger.info("✅ Client authenticated")

            async for message in websocket:
                try:
                    request = json.loads(message)
                    command_type = request.get("type")

                    if command_type == "execute":
                        result = await self.execute_command(
                            request.get("command"), request.get("timeout", 30)
                        )
                    elif command_type == "list_files":
                        result = await self.list_files(request.get("path", "."))
                    elif command_type == "system_info":
                        result = await self.get_system_info()
                    else:
                        result = {"error": f"Unknown command type: {command_type}"}

                    await websocket.send(json.dumps(result))

                except json.JSONDecodeError:
                    await websocket.send(
                        json.dumps({"error": "Invalid JSON request"})
                    )
                except Exception as e:
                    logger.error(f"❌ Error handling request: {e}")
                    await websocket.send(json.dumps({"error": str(e)}))

        except Exception as e:
            logger.error(f"❌ Connection error: {e}")

    async def execute_command(self, command: str, timeout: int = 30) -> Dict[str, Any]:
        """Execute shell command"""
        try:
            logger.info(f"📟 Executing: {command}")

            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await asyncio.wait_for(
                process.communicate(), timeout=timeout
            )

            return {
                "success": True,
                "exit_code": process.returncode,
                "stdout": stdout.decode("utf-8", errors="ignore"),
                "stderr": stderr.decode("utf-8", errors="ignore"),
            }

        except asyncio.TimeoutError:
            return {"success": False, "error": f"Command timed out after {timeout}s"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def list_files(self, path: str) -> Dict[str, Any]:
        """List files in directory"""
        try:
            target_path = Path(path).expanduser().resolve()

            if not target_path.exists():
                return {"success": False, "error": "Path does not exist"}

            files = []
            for item in target_path.iterdir():
                files.append(
                    {
                        "name": item.name,
                        "path": str(item),
                        "is_dir": item.is_dir(),
                        "size": item.stat().st_size if item.is_file() else 0,
                    }
                )

            return {"success": True, "path": str(target_path), "files": files}

        except Exception as e:
            return {"success": False, "error": str(e)}

    async def get_system_info(self) -> Dict[str, Any]:
        """Get system information"""
        try:
            return {
                "success": True,
                "system": platform.system(),
                "release": platform.release(),
                "version": platform.version(),
                "machine": platform.machine(),
                "processor": platform.processor(),
                "cpu_count": psutil.cpu_count(),
                "memory_total": psutil.virtual_memory().total,
                "memory_available": psutil.virtual_memory().available,
                "disk_usage": {
                    "total": psutil.disk_usage("/").total,
                    "used": psutil.disk_usage("/").used,
                    "free": psutil.disk_usage("/").free,
                },
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def start(self, host: str = "0.0.0.0", port: int = 8765):
        """Start WebSocket server"""
        logger.info(f"🚀 Starting Local PC Agent on {host}:{port}")
        async with websockets.serve(self.handle_client, host, port):
            logger.info("✅ Agent ready to accept connections")
            await asyncio.Future()  # Run forever


def main():
    parser = argparse.ArgumentParser(description="Local PC Agent for Remote Control")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8765, help="Port to listen on")
    parser.add_argument(
        "--token", required=True, help="Authentication token (keep secret!)"
    )

    args = parser.parse_args()

    agent = LocalPCAgent(auth_token=args.token)

    try:
        asyncio.run(agent.start(args.host, args.port))
    except KeyboardInterrupt:
        logger.info("👋 Agent stopped by user")


if __name__ == "__main__":
    main()
