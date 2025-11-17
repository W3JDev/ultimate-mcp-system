"""
System Commands - Execute local system operations safely
"""

import os
import platform
import subprocess
from typing import Any, Dict, Optional

import psutil
from loguru import logger


class SystemCommands:
    """Safe local system command execution"""

    def __init__(self):
        """Initialize system commands with safety checks"""
        self.os_type = platform.system()
        self.allowed_commands = self._get_allowed_commands()
        logger.info(f"💻 System commands initialized ({self.os_type})")

    def get_system_info(self) -> Dict[str, Any]:
        """
        Get comprehensive system information

        Returns:
            System details dictionary
        """
        return {
            "os": {
                "system": platform.system(),
                "release": platform.release(),
                "version": platform.version(),
                "machine": platform.machine(),
                "processor": platform.processor(),
            },
            "cpu": {
                "physical_cores": psutil.cpu_count(logical=False),
                "logical_cores": psutil.cpu_count(logical=True),
                "usage_percent": psutil.cpu_percent(interval=1),
            },
            "memory": {
                "total": psutil.virtual_memory().total,
                "available": psutil.virtual_memory().available,
                "used": psutil.virtual_memory().used,
                "percent": psutil.virtual_memory().percent,
            },
            "disk": {
                "total": psutil.disk_usage("/").total,
                "used": psutil.disk_usage("/").used,
                "free": psutil.disk_usage("/").free,
                "percent": psutil.disk_usage("/").percent,
            },
        }

    def run_safe_command(
        self, command: str, args: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Execute a safe system command

        Args:
            command: Command to execute
            args: Optional command arguments

        Returns:
            Command execution result
        """
        logger.info(f"🔧 Executing command: {command}")

        # Security check
        if not self._is_command_allowed(command):
            raise PermissionError(f"Command not allowed: {command}")

        try:
            full_command = [command] + (args or [])

            result = subprocess.run(
                full_command,
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
            }

        except subprocess.TimeoutExpired:
            logger.error(f"Command timeout: {command}")
            return {
                "success": False,
                "error": "Command execution timeout (30s)",
            }
        except Exception as e:
            logger.error(f"Command error: {e}")
            return {"success": False, "error": str(e)}

    def list_processes(self, limit: int = 10) -> list:
        """
        List running processes

        Args:
            limit: Maximum number of processes to return

        Returns:
            List of process info dictionaries
        """
        processes = []
        for proc in psutil.process_iter(
            ["pid", "name", "cpu_percent", "memory_percent"]
        ):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        # Sort by CPU usage
        processes.sort(key=lambda x: x.get("cpu_percent", 0), reverse=True)
        return processes[:limit]

    def kill_process(self, pid: int) -> Dict[str, Any]:
        """
        Safely terminate a process

        Args:
            pid: Process ID to terminate

        Returns:
            Operation result
        """
        try:
            process = psutil.Process(pid)
            process_name = process.name()

            # Safety check - don't kill critical processes
            critical_processes = ["System", "csrss.exe", "wininit.exe", "services.exe"]
            if process_name in critical_processes:
                raise PermissionError(f"Cannot kill critical process: {process_name}")

            process.terminate()
            logger.info(f"✅ Terminated process {pid} ({process_name})")

            return {
                "success": True,
                "message": f"Process {process_name} (PID: {pid}) terminated",
            }

        except psutil.NoSuchProcess:
            return {"success": False, "error": f"Process {pid} not found"}
        except psutil.AccessDenied:
            return {
                "success": False,
                "error": f"Access denied to kill process {pid}",
            }
        except Exception as e:
            logger.error(f"Kill process error: {e}")
            return {"success": False, "error": str(e)}

    def _is_command_allowed(self, command: str) -> bool:
        """Check if command is in allowed list"""
        return command in self.allowed_commands

    def _get_allowed_commands(self) -> set:
        """Get OS-specific allowed commands"""
        common_commands = {
            "echo",
            "date",
            "hostname",
            "whoami",
            "pwd",
            "ls",
            "dir",
            "ping",
            "curl",
            "wget",
        }

        os_specific = {
            "Windows": {"ipconfig", "tasklist", "systeminfo"},
            "Linux": {"ifconfig", "ps", "uname", "df", "top"},
            "Darwin": {"ifconfig", "ps", "uname", "df", "top"},  # macOS
        }

        return common_commands | os_specific.get(self.os_type, set())
