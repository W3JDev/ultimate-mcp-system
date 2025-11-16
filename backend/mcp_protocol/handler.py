"""
MCP Protocol Request Handler
Routes and processes JSON-RPC requests
"""
import sys
from typing import Any, Dict

from loguru import logger

from .errors import (
    InternalError,
    InvalidParams,
    InvalidRequest,
    JSONRPCError,
    MethodNotFound,
)
from .lifecycle import LifecycleManager
from .registry import ToolRegistry
from .transport import StdioTransport


class MCPRequestHandler:
    """
    Handles MCP protocol requests
    
    Manages:
    - Request routing
    - Lifecycle methods
    - Tool operations
    - Error handling
    """
    
    def __init__(self, transport: StdioTransport, lifecycle: LifecycleManager, registry: ToolRegistry):
        self.transport = transport
        self.lifecycle = lifecycle
        self.registry = registry
        logger.info("🎯 Request handler initialized", file=sys.stderr)
    
    def handle_request(self, message: Dict[str, Any]):
        """
        Process a JSON-RPC request message
        
        Args:
            message: Validated JSON-RPC request
        """
        method = message["method"]
        params = message.get("params", {})
        request_id = message.get("id")  # None for notifications
        
        logger.info(f"🔍 Processing: {method}", file=sys.stderr)
        
        try:
            # Route to appropriate handler
            if method == "initialize":
                result = self.handle_initialize(params)
                if request_id is not None:
                    self.transport.send_response(request_id, result)
            
            elif method == "initialized":
                self.handle_initialized(params)
                # This is a notification, no response needed
            
            elif method == "tools/list":
                # Require initialized session
                self.lifecycle.require_initialized()
                result = self.handle_tools_list(params)
                if request_id is not None:
                    self.transport.send_response(request_id, result)
            
            elif method == "tools/call":
                # Require initialized session
                self.lifecycle.require_initialized()
                result = self.handle_tools_call(params)
                if request_id is not None:
                    self.transport.send_response(request_id, result)
            
            else:
                raise MethodNotFound(method)
        
        except JSONRPCError as e:
            # Known protocol errors
            logger.error(f"❌ Protocol error: {e.message}", file=sys.stderr)
            if request_id is not None:
                error = e.to_dict()
                self.transport.send_error(
                    request_id,
                    error["code"],
                    error["message"],
                    error.get("data")
                )
        
        except Exception as e:
            # Unexpected errors
            logger.error(f"❌ Internal error: {str(e)}", file=sys.stderr)
            if request_id is not None:
                self.transport.send_error(
                    request_id,
                    InternalError().code,
                    "Internal error",
                    str(e)
                )
    
    def handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle initialize request"""
        return self.lifecycle.handle_initialize(params)
    
    def handle_initialized(self, params: Any):
        """Handle initialized notification"""
        self.lifecycle.handle_initialized(params)
    
    def handle_tools_list(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle tools/list request
        
        Returns list of available tools
        """
        tools = self.registry.list_tools()
        return {"tools": tools}
    
    def handle_tools_call(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle tools/call request
        
        Executes a tool and returns result
        
        Args:
            params: Must contain 'name' and optionally 'arguments'
        """
        if "name" not in params:
            raise InvalidParams("Missing 'name' field")
        
        tool_name = params["name"]
        arguments = params.get("arguments", {})
        
        # Execute tool
        result = self.registry.call_tool(tool_name, arguments)
        
        # Return result in MCP format
        return {
            "content": [
                {
                    "type": "text",
                    "text": str(result)
                }
            ]
        }
