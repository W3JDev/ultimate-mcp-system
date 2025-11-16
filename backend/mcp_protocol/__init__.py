"""
MCP Protocol Implementation
JSON-RPC 2.0 over stdio transport

This package implements the Model Context Protocol (MCP) for tool communication.
"""

from .errors import (
    InternalError,
    InvalidParams,
    InvalidRequest,
    JSONRPCError,
    MethodNotFound,
    ParseError,
    ProtocolVersionMismatch,
    ToolExecutionError,
    ToolNotFound,
)
from .handler import MCPRequestHandler
from .lifecycle import LifecycleManager
from .registry import ToolRegistry
from .transport import StdioTransport

__all__ = [
    # Transport
    "StdioTransport",
    # Lifecycle
    "LifecycleManager",
    # Registry
    "ToolRegistry",
    # Handler
    "MCPRequestHandler",
    # Errors
    "JSONRPCError",
    "ParseError",
    "InvalidRequest",
    "MethodNotFound",
    "InvalidParams",
    "InternalError",
    "ToolNotFound",
    "ToolExecutionError",
    "ProtocolVersionMismatch",
]

__version__ = "1.0.0"
