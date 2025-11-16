# MCP Protocol Implementation

This directory contains the implementation of the Model Context Protocol (MCP) using JSON-RPC 2.0 over stdio transport.

## Architecture

The MCP protocol implementation follows a modular design:

```
mcp_protocol/
├── __init__.py          # Package exports
├── errors.py            # JSON-RPC error definitions
├── transport.py         # Stdio transport layer
├── lifecycle.py         # Protocol lifecycle management
├── registry.py          # Tool registration and execution
└── handler.py           # Request routing and processing
```

## Components

### Transport Layer (`transport.py`)

Implements JSON-RPC 2.0 communication over stdio:
- **Input**: Newline-delimited JSON on stdin
- **Output**: Newline-delimited JSON on stdout
- **Logging**: All diagnostic output to stderr

Key features:
- Message validation (JSON-RPC 2.0 compliance)
- Request/response/notification handling
- Error response formatting

### Lifecycle Management (`lifecycle.py`)

Manages protocol initialization and session state:
- `initialize` - Protocol handshake with capability negotiation
- `initialized` - Session confirmation notification
- Session state tracking

### Tool Registry (`registry.py`)

Dynamic tool registration and execution:
- Register tools with name, description, and handler
- JSON schema validation for tool inputs
- Tool execution with error handling
- List registered tools

### Request Handler (`handler.py`)

Routes JSON-RPC requests to appropriate handlers:
- Method routing (initialize, tools/list, tools/call)
- Error handling and response formatting
- Session state validation

### Error Handling (`errors.py`)

JSON-RPC 2.0 compliant error codes:
- Standard errors (-32700 to -32603)
- Application errors (-32000 to -32099)
- Custom MCP errors (tool not found, execution errors)

## Usage

### Starting the Server

```bash
cd backend
python mcp_hub_server.py
```

The server will:
1. Initialize all components
2. Register example tools (echo, add, get_time)
3. Listen on stdin for JSON-RPC messages
4. Log to stderr
5. Send responses to stdout

### Example Communication

**Initialize:**
```json
// Request
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"test","version":"1.0.0"}}}

// Response
{"jsonrpc":"2.0","id":1,"result":{"protocolVersion":"2025-03-26","capabilities":{"tools":{"listChanged":true},"logging":{}},"serverInfo":{"name":"ultimate-mcp-hub","version":"1.0.0"}}}
```

**Initialized Notification:**
```json
{"jsonrpc":"2.0","method":"initialized"}
```

**List Tools:**
```json
// Request
{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}

// Response
{"jsonrpc":"2.0","id":2,"result":{"tools":[{"name":"echo","description":"Echo back a message","inputSchema":{...}}]}}
```

**Call Tool:**
```json
// Request
{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"add","arguments":{"a":5,"b":3}}}

// Response
{"jsonrpc":"2.0","id":3,"result":{"content":[{"type":"text","text":"{'result': 8}"}]}}
```

## Supported Methods

| Method | Type | Description |
|--------|------|-------------|
| `initialize` | Request | Protocol handshake and capability negotiation |
| `initialized` | Notification | Client confirms initialization complete |
| `tools/list` | Request | List all available tools |
| `tools/call` | Request | Execute a tool with arguments |

## Extending the Server

### Registering Custom Tools

```python
from mcp_protocol import ToolRegistry

registry = ToolRegistry()

def my_tool_handler(args):
    # Process arguments
    result = args.get("param1") + args.get("param2")
    return result

registry.register_tool(
    name="my_tool",
    description="Description of what the tool does",
    handler=my_tool_handler,
    input_schema={
        "type": "object",
        "properties": {
            "param1": {"type": "string"},
            "param2": {"type": "string"}
        },
        "required": ["param1"]
    }
)
```

### Error Handling

All errors follow JSON-RPC 2.0 specification:

```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "error": {
        "code": -32601,
        "message": "Method not found",
        "data": {"method": "unknown_method"}
    }
}
```

## Testing

Run the test suite:

```bash
cd /home/runner/work/ultimate-mcp-system/ultimate-mcp-system
python -m pytest tests/ -v
```

Tests cover:
- Transport layer (JSON-RPC parsing and validation)
- Lifecycle management (initialization flow)
- Tool registry (registration, listing, execution)
- Integration (full request/response cycle)

## Protocol Compliance

This implementation follows:
- **JSON-RPC 2.0** specification
- **MCP Protocol** version 2025-03-26
- **Stdio transport** as specified in MCP docs

## References

- [MCP Specification](https://modelcontextprotocol.io/specification/)
- [JSON-RPC 2.0 Spec](https://www.jsonrpc.org/specification)
- [MCP Protocol Mechanics](https://pradeepl.com/blog/model-context-protocol/)
