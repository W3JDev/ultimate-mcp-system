"""
Unit tests for MCP Transport Layer
"""

import io
import sys

import pytest

# Add backend to path
sys.path.insert(0, "/home/runner/work/ultimate-mcp-system/ultimate-mcp-system/backend")

from mcp_protocol.errors import InvalidRequest, ParseError
from mcp_protocol.transport import StdioTransport


class TestStdioTransport:
    """Test stdio transport functionality"""

    def test_validate_valid_request(self):
        """Test validation of valid JSON-RPC request"""
        transport = StdioTransport()

        message = {"jsonrpc": "2.0", "id": 1, "method": "test", "params": {}}

        validated = transport.validate_request(message)
        assert validated == message

    def test_validate_valid_notification(self):
        """Test validation of valid notification (no id)"""
        transport = StdioTransport()

        message = {"jsonrpc": "2.0", "method": "test", "params": {}}

        validated = transport.validate_request(message)
        assert validated == message

    def test_validate_missing_jsonrpc(self):
        """Test validation fails without jsonrpc field"""
        transport = StdioTransport()

        message = {"id": 1, "method": "test"}

        with pytest.raises(InvalidRequest) as exc:
            transport.validate_request(message)
        error_dict = exc.value.to_dict()
        assert "jsonrpc" in str(error_dict)

    def test_validate_wrong_jsonrpc_version(self):
        """Test validation fails with wrong JSON-RPC version"""
        transport = StdioTransport()

        message = {"jsonrpc": "1.0", "id": 1, "method": "test"}

        with pytest.raises(InvalidRequest) as exc:
            transport.validate_request(message)
        error_dict = exc.value.to_dict()
        assert "jsonrpc" in str(error_dict)

    def test_validate_missing_method(self):
        """Test validation fails without method field"""
        transport = StdioTransport()

        message = {"jsonrpc": "2.0", "id": 1}

        with pytest.raises(InvalidRequest) as exc:
            transport.validate_request(message)
        error_dict = exc.value.to_dict()
        assert "method" in str(error_dict)

    def test_validate_invalid_method_type(self):
        """Test validation fails with non-string method"""
        transport = StdioTransport()

        message = {"jsonrpc": "2.0", "id": 1, "method": 123}

        with pytest.raises(InvalidRequest) as exc:
            transport.validate_request(message)
        error_dict = exc.value.to_dict()
        assert "method" in str(error_dict)

    def test_validate_invalid_params_type(self):
        """Test validation fails with invalid params type"""
        transport = StdioTransport()

        message = {"jsonrpc": "2.0", "id": 1, "method": "test", "params": "invalid"}

        with pytest.raises(InvalidRequest) as exc:
            transport.validate_request(message)
        error_dict = exc.value.to_dict()
        assert "params" in str(error_dict)

    def test_send_response(self, capsys):
        """Test sending a JSON-RPC response"""
        transport = StdioTransport()

        transport.send_response(1, {"status": "ok"})

        captured = capsys.readouterr()
        import json

        response = json.loads(captured.out.strip())

        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 1
        assert response["result"] == {"status": "ok"}

    def test_send_error(self, capsys):
        """Test sending a JSON-RPC error"""
        transport = StdioTransport()

        transport.send_error(1, -32600, "Invalid Request", {"detail": "test"})

        captured = capsys.readouterr()
        import json

        response = json.loads(captured.out.strip())

        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 1
        assert response["error"]["code"] == -32600
        assert response["error"]["message"] == "Invalid Request"
        assert response["error"]["data"]["detail"] == "test"

    def test_send_notification(self, capsys):
        """Test sending a JSON-RPC notification"""
        transport = StdioTransport()

        transport.send_notification("test_event", {"data": "value"})

        captured = capsys.readouterr()
        import json

        notification = json.loads(captured.out.strip())

        assert notification["jsonrpc"] == "2.0"
        assert notification["method"] == "test_event"
        assert notification["params"] == {"data": "value"}
        assert "id" not in notification
