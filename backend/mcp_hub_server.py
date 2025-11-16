#!/usr/bin/env python3
"""
MCP Hub Server - Main Entry Point
JSON-RPC 2.0 over stdio implementation

This server implements the Model Context Protocol (MCP) for tool communication.
It communicates via stdin/stdout using newline-delimited JSON-RPC 2.0 messages.
"""
import sys

from loguru import logger

from mcp_protocol import (
    LifecycleManager,
    MCPRequestHandler,
    StdioTransport,
    ToolRegistry,
)
from mcp_protocol.errors import InvalidRequest, JSONRPCError, ParseError


def setup_logging():
    """Configure logging to stderr only"""
    # Remove default handler
    logger.remove()
    
    # Add stderr handler with custom format
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
        level="INFO"
    )


def register_example_tools(registry: ToolRegistry):
    """
    Register example tools for demonstration
    
    In production, tools would be registered dynamically based on
    available MCP servers or capabilities.
    """
    
    def echo_tool(args):
        """Simple echo tool"""
        message = args.get("message", "")
        return f"Echo: {message}"
    
    def add_tool(args):
        """Simple addition tool"""
        a = args.get("a", 0)
        b = args.get("b", 0)
        return {"result": a + b}
    
    def get_time_tool(args):
        """Get current time"""
        import datetime
        return {"time": datetime.datetime.now().isoformat()}
    
    # Register tools
    registry.register_tool(
        name="echo",
        description="Echo back a message",
        handler=echo_tool,
        input_schema={
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "Message to echo"
                }
            },
            "required": ["message"]
        }
    )
    
    registry.register_tool(
        name="add",
        description="Add two numbers",
        handler=add_tool,
        input_schema={
            "type": "object",
            "properties": {
                "a": {
                    "type": "number",
                    "description": "First number"
                },
                "b": {
                    "type": "number",
                    "description": "Second number"
                }
            },
            "required": ["a", "b"]
        }
    )
    
    registry.register_tool(
        name="get_time",
        description="Get current timestamp",
        handler=get_time_tool,
        input_schema={
            "type": "object",
            "properties": {}
        }
    )


def main():
    """Main server loop"""
    setup_logging()
    
    logger.info("=" * 60)
    logger.info("🚀 MCP Hub Server Starting")
    logger.info("=" * 60)
    
    # Initialize components
    transport = StdioTransport()
    lifecycle = LifecycleManager()
    registry = ToolRegistry()
    handler = MCPRequestHandler(transport, lifecycle, registry)
    
    # Register example tools
    register_example_tools(registry)
    
    logger.info("✅ MCP Hub Server Ready")
    logger.info("📡 Listening on stdin for JSON-RPC 2.0 messages")
    logger.info("=" * 60)
    
    # Main message loop
    try:
        while True:
            try:
                # Read message from stdin
                message = transport.read_message()
                
                if message is None:
                    # stdin closed, exit gracefully
                    logger.info("📭 stdin closed, shutting down")
                    break
                
                # Validate JSON-RPC request
                try:
                    validated = transport.validate_request(message)
                    handler.handle_request(validated)
                    
                except InvalidRequest as e:
                    # Send error response for invalid requests
                    logger.error(f"❌ Invalid request: {e.message}")
                    request_id = message.get("id")
                    error = e.to_dict()
                    transport.send_error(
                        request_id,
                        error["code"],
                        error["message"],
                        error.get("data")
                    )
            
            except ParseError as e:
                # Can't extract request ID from invalid JSON
                logger.error(f"❌ Parse error: {e.message}")
                error = e.to_dict()
                transport.send_error(
                    None,
                    error["code"],
                    error["message"],
                    error.get("data")
                )
            
            except KeyboardInterrupt:
                logger.info("⚠️ Interrupted by user")
                break
            
            except Exception as e:
                logger.error(f"❌ Unexpected error: {str(e)}")
                # Try to send error response
                try:
                    transport.send_error(None, -32603, "Internal error", str(e))
                except:
                    pass
    
    finally:
        logger.info("=" * 60)
        logger.info("👋 MCP Hub Server Shutting Down")
        logger.info("=" * 60)


if __name__ == "__main__":
    main()
