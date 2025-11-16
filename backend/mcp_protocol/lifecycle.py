"""
MCP Lifecycle Management
Handles protocol initialization and capability negotiation
"""
import sys
from typing import Any, Dict

from loguru import logger

from .errors import InvalidParams, ProtocolVersionMismatch


class LifecycleManager:
    """
    Manages MCP protocol lifecycle
    - Initialize handshake
    - Capability negotiation
    - Session state
    """
    
    SUPPORTED_PROTOCOL_VERSION = "2025-03-26"
    
    def __init__(self):
        self.initialized = False
        self.client_info = None
        self.client_capabilities = {}
        self.protocol_version = None
        logger.info("🔄 Lifecycle manager initialized", file=sys.stderr)
    
    def handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle 'initialize' request
        
        Performs protocol handshake and capability negotiation
        
        Args:
            params: Initialize parameters from client
            
        Returns:
            Initialize result with server info and capabilities
            
        Raises:
            InvalidParams: If required parameters missing
            ProtocolVersionMismatch: If protocol version not supported
        """
        # Validate required parameters
        if "protocolVersion" not in params:
            raise InvalidParams({"message": "Missing 'protocolVersion'"})
        
        if "capabilities" not in params:
            raise InvalidParams({"message": "Missing 'capabilities'"})
        
        if "clientInfo" not in params:
            raise InvalidParams({"message": "Missing 'clientInfo'"})
        
        # Check protocol version
        requested_version = params["protocolVersion"]
        if requested_version != self.SUPPORTED_PROTOCOL_VERSION:
            logger.warning(
                f"⚠️ Protocol version mismatch: {requested_version} (requested) vs {self.SUPPORTED_PROTOCOL_VERSION} (supported)",
                file=sys.stderr
            )
            # For now, we'll accept it but log the warning
            # In strict mode, could raise ProtocolVersionMismatch
        
        # Store client info
        self.protocol_version = requested_version
        self.client_info = params["clientInfo"]
        self.client_capabilities = params["capabilities"]
        
        logger.info(f"🤝 Initialize from: {self.client_info.get('name', 'unknown')}", file=sys.stderr)
        logger.info(f"📋 Protocol version: {self.protocol_version}", file=sys.stderr)
        
        # Return server capabilities
        result = {
            "protocolVersion": self.SUPPORTED_PROTOCOL_VERSION,
            "capabilities": {
                "tools": {
                    "listChanged": True  # Server can notify when tool list changes
                },
                "logging": {}  # Server supports logging
            },
            "serverInfo": {
                "name": "ultimate-mcp-hub",
                "version": "1.0.0"
            }
        }
        
        logger.info("✅ Initialize handshake complete", file=sys.stderr)
        return result
    
    def handle_initialized(self, params: Any = None):
        """
        Handle 'initialized' notification from client
        
        This notification indicates client is ready to start using the protocol
        
        Args:
            params: Optional parameters (usually empty)
        """
        self.initialized = True
        logger.info("✅ Client confirmed initialization", file=sys.stderr)
        logger.info("🚀 MCP session active", file=sys.stderr)
    
    def is_initialized(self) -> bool:
        """Check if session is fully initialized"""
        return self.initialized
    
    def require_initialized(self):
        """
        Raise error if session not initialized
        
        Should be called before processing tools/list or tools/call
        """
        if not self.initialized:
            from .errors import InvalidRequest
            raise InvalidRequest("Session not initialized. Send 'initialize' first.")
    
    def get_client_info(self) -> Dict[str, Any]:
        """Get connected client information"""
        return self.client_info or {}
    
    def get_server_info(self) -> Dict[str, Any]:
        """Get server information"""
        return {
            "name": "ultimate-mcp-hub",
            "version": "1.0.0",
            "protocolVersion": self.SUPPORTED_PROTOCOL_VERSION
        }
