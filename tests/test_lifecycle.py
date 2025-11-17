"""
Unit tests for MCP Lifecycle Management
"""

import sys

import pytest

# Add backend to path
sys.path.insert(0, "/home/runner/work/ultimate-mcp-system/ultimate-mcp-system/backend")

from mcp_protocol.errors import InvalidParams, InvalidRequest
from mcp_protocol.lifecycle import LifecycleManager


class TestLifecycleManager:
    """Test lifecycle management"""

    def test_initialize_success(self):
        """Test successful initialization"""
        manager = LifecycleManager()

        params = {
            "protocolVersion": "2025-03-26",
            "capabilities": {"roots": {"listChanged": True}, "sampling": {}},
            "clientInfo": {"name": "test-client", "version": "1.0.0"},
        }

        result = manager.handle_initialize(params)

        assert result["protocolVersion"] == "2025-03-26"
        assert "capabilities" in result
        assert "serverInfo" in result
        assert result["serverInfo"]["name"] == "ultimate-mcp-hub"

    def test_initialize_missing_protocol_version(self):
        """Test initialization fails without protocol version"""
        manager = LifecycleManager()

        params = {"capabilities": {}, "clientInfo": {"name": "test"}}

        with pytest.raises(InvalidParams) as exc:
            manager.handle_initialize(params)

        error_dict = exc.value.to_dict()
        assert "protocolVersion" in str(error_dict)

    def test_initialize_missing_capabilities(self):
        """Test initialization fails without capabilities"""
        manager = LifecycleManager()

        params = {"protocolVersion": "2025-03-26", "clientInfo": {"name": "test"}}

        with pytest.raises(InvalidParams) as exc:
            manager.handle_initialize(params)

        error_dict = exc.value.to_dict()
        assert "capabilities" in str(error_dict)

    def test_initialize_missing_client_info(self):
        """Test initialization fails without client info"""
        manager = LifecycleManager()

        params = {"protocolVersion": "2025-03-26", "capabilities": {}}

        with pytest.raises(InvalidParams) as exc:
            manager.handle_initialize(params)

        error_dict = exc.value.to_dict()
        assert "clientInfo" in str(error_dict)

    def test_initialized_notification(self):
        """Test initialized notification handling"""
        manager = LifecycleManager()

        assert not manager.is_initialized()

        manager.handle_initialized()

        assert manager.is_initialized()

    def test_require_initialized_before_init(self):
        """Test require_initialized raises before initialization"""
        manager = LifecycleManager()

        with pytest.raises(InvalidRequest) as exc:
            manager.require_initialized()

        error_dict = exc.value.to_dict()
        assert "initialized" in str(error_dict).lower()

    def test_require_initialized_after_init(self):
        """Test require_initialized succeeds after initialization"""
        manager = LifecycleManager()

        params = {
            "protocolVersion": "2025-03-26",
            "capabilities": {},
            "clientInfo": {"name": "test"},
        }

        manager.handle_initialize(params)
        manager.handle_initialized()

        # Should not raise
        manager.require_initialized()

    def test_get_client_info(self):
        """Test retrieving client information"""
        manager = LifecycleManager()

        client_info = {"name": "test-client", "version": "2.0.0"}

        params = {
            "protocolVersion": "2025-03-26",
            "capabilities": {},
            "clientInfo": client_info,
        }

        manager.handle_initialize(params)

        retrieved = manager.get_client_info()
        assert retrieved == client_info

    def test_get_server_info(self):
        """Test retrieving server information"""
        manager = LifecycleManager()

        server_info = manager.get_server_info()

        assert "name" in server_info
        assert "version" in server_info
        assert "protocolVersion" in server_info
        assert server_info["name"] == "ultimate-mcp-hub"
