"""
MCP JSON-RPC 2.0 Transport Layer
Handles stdio communication with proper message formatting
"""
import json
import sys
from typing import Any, Dict, Optional

from loguru import logger

from .errors import InvalidRequest, ParseError


class StdioTransport:
    """
    JSON-RPC 2.0 transport over stdin/stdout
    
    Messages are newline-delimited JSON objects
    - Reads from stdin
    - Writes to stdout
    - Logs to stderr
    """
    
    def __init__(self):
        logger.info("📡 Stdio transport initialized", file=sys.stderr)
        # Ensure stdin/stdout are in line-buffered mode
        try:
            sys.stdin.reconfigure(line_buffering=True)
            sys.stdout.reconfigure(line_buffering=True)
        except AttributeError:
            # In test environment, stdin/stdout may not have reconfigure
            pass
    
    def read_message(self) -> Optional[Dict[str, Any]]:
        """
        Read a JSON-RPC message from stdin
        
        Returns:
            Parsed message dict, or None if stdin closed
            
        Raises:
            ParseError: If JSON is invalid
        """
        try:
            line = sys.stdin.readline()
            
            if not line:
                # EOF reached
                logger.info("📭 stdin closed", file=sys.stderr)
                return None
            
            line = line.strip()
            if not line:
                # Empty line, skip
                return self.read_message()
            
            logger.opt(raw=False).debug("📨 Received: {msg}", msg=line, file=sys.stderr)
            
            try:
                message = json.loads(line)
                return message
            except json.JSONDecodeError as e:
                logger.error(f"❌ JSON parse error: {e}", file=sys.stderr)
                raise ParseError(str(e))
                
        except Exception as e:
            logger.error(f"❌ Transport read error: {e}", file=sys.stderr)
            raise
    
    def write_message(self, message: Dict[str, Any]):
        """
        Write a JSON-RPC message to stdout
        
        Args:
            message: Message dict to send (must be JSON-serializable)
        """
        try:
            json_str = json.dumps(message, separators=(',', ':'))
            # Log with repr to avoid JSON brace issues with loguru
            logger.opt(raw=False).debug("📤 Sending: {msg}", msg=json_str, file=sys.stderr)
            
            # Write as single line with newline delimiter
            sys.stdout.write(json_str + '\n')
            sys.stdout.flush()
            
        except Exception as e:
            logger.error(f"❌ Transport write error: {e}", file=sys.stderr)
            raise
    
    def send_response(self, request_id: Any, result: Any):
        """
        Send a successful JSON-RPC response
        
        Args:
            request_id: ID from the original request
            result: Result data to return
        """
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": result
        }
        self.write_message(response)
    
    def send_error(self, request_id: Any, error_code: int, error_message: str, error_data: Any = None):
        """
        Send a JSON-RPC error response
        
        Args:
            request_id: ID from the original request (may be None)
            error_code: JSON-RPC error code
            error_message: Error description
            error_data: Additional error information (optional)
        """
        error = {
            "code": error_code,
            "message": error_message
        }
        if error_data is not None:
            error["data"] = error_data
        
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": error
        }
        self.write_message(response)
    
    def send_notification(self, method: str, params: Any = None):
        """
        Send a JSON-RPC notification (no response expected)
        
        Args:
            method: Notification method name
            params: Notification parameters (optional)
        """
        notification = {
            "jsonrpc": "2.0",
            "method": method
        }
        if params is not None:
            notification["params"] = params
        
        self.write_message(notification)
    
    def validate_request(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate that a message is a proper JSON-RPC 2.0 request
        
        Args:
            message: Received message
            
        Returns:
            Validated message
            
        Raises:
            InvalidRequest: If message is not valid
        """
        # Must have jsonrpc field
        if message.get("jsonrpc") != "2.0":
            raise InvalidRequest("Missing or invalid 'jsonrpc' field")
        
        # Must have method field (string)
        if "method" not in message:
            raise InvalidRequest("Missing 'method' field")
        
        if not isinstance(message["method"], str):
            raise InvalidRequest("'method' must be a string")
        
        # If it has an id, it's a request; otherwise it's a notification
        # Both are valid
        
        # Params field is optional but must be object or array if present
        if "params" in message:
            params = message["params"]
            if not isinstance(params, (dict, list)):
                raise InvalidRequest("'params' must be an object or array")
        
        return message
