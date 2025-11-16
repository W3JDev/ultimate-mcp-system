"""
Local Control MCP Tools
Tools for system automation (commands, processes, files, input, browser)
"""

import os
import platform
import subprocess
from pathlib import Path
from typing import Any, Dict, List
import psutil
from loguru import logger
from .base import MCPTool, ToolSchema, ToolParameter


# === Tool: Execute System Command ===
def execute_command_handler(command: str, timeout: int = 30) -> Dict[str, Any]:
    """
    Execute a system command
    
    Args:
        command: Command to execute
        timeout: Command timeout in seconds
        
    Returns:
        Command output and exit code
    """
    try:
        if not command.strip():
            return {"error": "Empty command"}
        
        logger.info(f"📟 Executing: {command}")
        
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=timeout
        )
        
        return {
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "command": command
        }
    except subprocess.TimeoutExpired:
        return {"error": f"Command timed out after {timeout}s"}
    except Exception as e:
        return {"error": str(e)}


execute_command_tool = MCPTool(
    schema=ToolSchema(
        name="execute_system_command",
        display_name="Execute System Command",
        description="Execute a shell command on the local system",
        category="local",
        parameters=[
            ToolParameter(
                name="command",
                type="string",
                description="Shell command to execute",
                required=True
            ),
            ToolParameter(
                name="timeout",
                type="number",
                description="Command timeout in seconds",
                required=False,
                default=30
            )
        ],
        returns="Command output with exit code, stdout, and stderr",
        examples=[
            "Execute: git status",
            "Run: python --version",
            "List files: ls -la"
        ]
    ),
    handler=execute_command_handler
)


# === Tool: List Processes ===
def list_processes_handler(limit: int = 20, sort_by: str = "memory") -> List[Dict[str, Any]]:
    """
    List running processes
    
    Args:
        limit: Maximum number of processes to return
        sort_by: Sort by 'memory', 'cpu', or 'name'
        
    Returns:
        List of process information
    """
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append({
                    "pid": proc.info['pid'],
                    "name": proc.info['name'],
                    "cpu_percent": round(proc.info['cpu_percent'], 1),
                    "memory_percent": round(proc.info['memory_percent'], 1)
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Sort processes
        if sort_by == "cpu":
            processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
        elif sort_by == "name":
            processes.sort(key=lambda x: x['name'])
        else:  # memory
            processes.sort(key=lambda x: x['memory_percent'], reverse=True)
        
        return processes[:limit]
    except Exception as e:
        return [{"error": str(e)}]


list_processes_tool = MCPTool(
    schema=ToolSchema(
        name="list_processes",
        display_name="List Processes",
        description="List running system processes with CPU and memory usage",
        category="local",
        parameters=[
            ToolParameter(
                name="limit",
                type="number",
                description="Maximum number of processes to return",
                required=False,
                default=20
            ),
            ToolParameter(
                name="sort_by",
                type="string",
                description="Sort by field",
                required=False,
                default="memory",
                enum=["memory", "cpu", "name"]
            )
        ],
        returns="List of process information with PID, name, CPU%, and memory%",
        examples=[
            "List top 20 processes by memory usage",
            "Show processes sorted by CPU usage"
        ]
    ),
    handler=list_processes_handler
)


# === Tool: Kill Process ===
def kill_process_handler(pid: int) -> Dict[str, Any]:
    """
    Kill a process by PID
    
    Args:
        pid: Process ID to kill
        
    Returns:
        Result of kill operation
    """
    try:
        proc = psutil.Process(pid)
        proc_name = proc.name()
        
        proc.terminate()
        proc.wait(timeout=5)
        
        logger.info(f"✅ Killed process {pid} ({proc_name})")
        return {
            "success": True,
            "pid": pid,
            "name": proc_name,
            "message": f"Process {pid} ({proc_name}) terminated"
        }
    except psutil.NoSuchProcess:
        return {"error": f"Process {pid} not found"}
    except psutil.AccessDenied:
        return {"error": f"Access denied (requires elevated privileges)"}
    except Exception as e:
        return {"error": str(e)}


kill_process_tool = MCPTool(
    schema=ToolSchema(
        name="kill_process",
        display_name="Kill Process",
        description="Terminate a running process by PID",
        category="local",
        parameters=[
            ToolParameter(
                name="pid",
                type="number",
                description="Process ID to terminate",
                required=True
            )
        ],
        returns="Result of termination with success status",
        examples=[
            "Kill process 12345",
            "Terminate unresponsive application"
        ]
    ),
    handler=kill_process_handler
)


# === Tool: List Files ===
def list_files_handler(directory: str, show_hidden: bool = False) -> Dict[str, Any]:
    """
    List files in a directory
    
    Args:
        directory: Directory path to list
        show_hidden: Include hidden files
        
    Returns:
        Directory contents
    """
    try:
        path = Path(directory).expanduser().resolve()
        
        if not path.exists():
            return {"error": f"Directory not found: {directory}"}
        
        if not path.is_dir():
            return {"error": f"Not a directory: {directory}"}
        
        files = []
        for item in path.iterdir():
            if not show_hidden and item.name.startswith('.'):
                continue
            
            try:
                stat = item.stat()
                files.append({
                    "name": item.name,
                    "type": "directory" if item.is_dir() else "file",
                    "size": stat.st_size if item.is_file() else None,
                    "modified": stat.st_mtime
                })
            except Exception:
                pass
        
        return {
            "directory": str(path),
            "count": len(files),
            "files": sorted(files, key=lambda x: (x['type'] != 'directory', x['name']))
        }
    except Exception as e:
        return {"error": str(e)}


list_files_tool = MCPTool(
    schema=ToolSchema(
        name="list_files",
        display_name="List Files",
        description="List files and directories in a given path",
        category="local",
        parameters=[
            ToolParameter(
                name="directory",
                type="string",
                description="Directory path to list",
                required=True
            ),
            ToolParameter(
                name="show_hidden",
                type="boolean",
                description="Include hidden files (starting with .)",
                required=False,
                default=False
            )
        ],
        returns="Directory contents with file/directory information",
        examples=[
            "List files in home directory",
            "Show contents of /tmp including hidden files"
        ]
    ),
    handler=list_files_handler
)


# === Tool: Read File ===
def read_file_handler(filepath: str, max_size: int = 1000000) -> Dict[str, Any]:
    """
    Read file contents
    
    Args:
        filepath: Path to file
        max_size: Maximum file size in bytes
        
    Returns:
        File contents
    """
    try:
        path = Path(filepath).expanduser().resolve()
        
        if not path.exists():
            return {"error": f"File not found: {filepath}"}
        
        if not path.is_file():
            return {"error": f"Not a file: {filepath}"}
        
        size = path.stat().st_size
        if size > max_size:
            return {"error": f"File too large ({size} bytes, max {max_size})"}
        
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        return {
            "filepath": str(path),
            "size": size,
            "content": content
        }
    except Exception as e:
        return {"error": str(e)}


read_file_tool = MCPTool(
    schema=ToolSchema(
        name="read_file",
        display_name="Read File",
        description="Read the contents of a text file",
        category="local",
        parameters=[
            ToolParameter(
                name="filepath",
                type="string",
                description="Path to file to read",
                required=True
            ),
            ToolParameter(
                name="max_size",
                type="number",
                description="Maximum file size in bytes",
                required=False,
                default=1000000
            )
        ],
        returns="File contents with metadata",
        examples=[
            "Read config.json",
            "Show contents of README.md"
        ]
    ),
    handler=read_file_handler
)


# === Tool: Open URL ===
def open_url_handler(url: str) -> Dict[str, Any]:
    """
    Open URL in default browser
    
    Args:
        url: URL to open
        
    Returns:
        Result of operation
    """
    try:
        import webbrowser
        webbrowser.open(url)
        return {
            "success": True,
            "url": url,
            "message": f"Opened {url} in default browser"
        }
    except Exception as e:
        return {"error": str(e)}


open_url_tool = MCPTool(
    schema=ToolSchema(
        name="open_url",
        display_name="Open URL",
        description="Open a URL in the default web browser",
        category="local",
        parameters=[
            ToolParameter(
                name="url",
                type="string",
                description="URL to open",
                required=True
            )
        ],
        returns="Confirmation of URL opening",
        examples=[
            "Open https://github.com",
            "Launch documentation website"
        ]
    ),
    handler=open_url_handler
)


# === Tool: Get System Info ===
def get_system_info_handler() -> Dict[str, Any]:
    """
    Get system information
    
    Returns:
        System information including OS, CPU, memory, disk
    """
    try:
        cpu_count = psutil.cpu_count()
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            "os": {
                "system": platform.system(),
                "release": platform.release(),
                "machine": platform.machine(),
                "processor": platform.processor() or "N/A"
            },
            "cpu": {
                "cores": cpu_count,
                "usage_percent": cpu_percent
            },
            "memory": {
                "total_gb": round(memory.total / (1024**3), 2),
                "available_gb": round(memory.available / (1024**3), 2),
                "used_percent": memory.percent
            },
            "disk": {
                "total_gb": round(disk.total / (1024**3), 2),
                "free_gb": round(disk.free / (1024**3), 2),
                "used_percent": disk.percent
            }
        }
    except Exception as e:
        return {"error": str(e)}


get_system_info_tool = MCPTool(
    schema=ToolSchema(
        name="get_system_info",
        display_name="Get System Info",
        description="Get detailed system information (OS, CPU, memory, disk)",
        category="local",
        parameters=[],
        returns="System information with OS, CPU, memory, and disk metrics",
        examples=[
            "Show system information",
            "Get current resource usage"
        ]
    ),
    handler=get_system_info_handler
)


# Export all local control tools
LOCAL_TOOLS = [
    execute_command_tool,
    list_processes_tool,
    kill_process_tool,
    list_files_tool,
    read_file_tool,
    open_url_tool,
    get_system_info_tool
]
