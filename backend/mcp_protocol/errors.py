"""
MCP Protocol Error Codes and Exceptions
Implements JSON-RPC 2.0 standard error codes
"""


class JSONRPCError(Exception):
    """Base class for JSON-RPC errors"""

    def __init__(self, code: int, message: str, data=None):
        self.code = code
        self.message = message
        self.data = data
        super().__init__(message)

    def to_dict(self):
        """Convert error to JSON-RPC error object"""
        error = {"code": self.code, "message": self.message}
        if self.data is not None:
            error["data"] = self.data
        return error


# JSON-RPC 2.0 Standard Error Codes
class ParseError(JSONRPCError):
    """Invalid JSON was received by the server"""

    def __init__(self, data=None):
        super().__init__(-32700, "Parse error", data)


class InvalidRequest(JSONRPCError):
    """The JSON sent is not a valid Request object"""

    def __init__(self, data=None):
        super().__init__(-32600, "Invalid Request", data)


class MethodNotFound(JSONRPCError):
    """The method does not exist / is not available"""

    def __init__(self, method: str):
        super().__init__(-32601, "Method not found", {"method": method})


class InvalidParams(JSONRPCError):
    """Invalid method parameter(s)"""

    def __init__(self, data=None):
        super().__init__(-32602, "Invalid params", data)


class InternalError(JSONRPCError):
    """Internal JSON-RPC error"""

    def __init__(self, data=None):
        super().__init__(-32603, "Internal error", data)


# MCP-specific error codes (application level, -32000 to -32099 reserved)
class ToolNotFound(JSONRPCError):
    """Requested tool does not exist"""

    def __init__(self, tool_name: str):
        super().__init__(-32000, "Tool not found", {"tool": tool_name})


class ToolExecutionError(JSONRPCError):
    """Error executing tool"""

    def __init__(self, tool_name: str, error: str):
        super().__init__(
            -32001, "Tool execution error", {"tool": tool_name, "error": error}
        )


class ProtocolVersionMismatch(JSONRPCError):
    """Protocol version not supported"""

    def __init__(self, requested: str, supported: str):
        super().__init__(
            -32002,
            "Protocol version mismatch",
            {"requested": requested, "supported": supported},
        )
