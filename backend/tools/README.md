# MCP Tools

This directory contains the MCP tool implementations that convert business logic into callable tools with standardized interfaces.

## Architecture

### Base Classes (`base.py`)

- **`ToolParameter`**: Defines a tool parameter with type, description, and validation
- **`ToolSchema`**: Complete schema for a tool including name, description, parameters, returns, and examples
- **`MCPTool`**: Base class for all tools that wraps handler functions with schema and execution logic

### Tool Registry (`registry.py`)

The `ToolRegistry` class provides:
- Tool registration and discovery
- Category-based organization
- Tool search functionality
- Centralized tool execution

### Tool Categories

#### N8N Tools (`n8n_tools.py`) - 4 tools
Workflow automation tools:
- `create_n8n_workflow` - Create workflows from natural language
- `test_n8n_workflow` - Test workflows with validation
- `deploy_n8n_workflow` - Deploy to N8N instance
- `validate_n8n_workflow` - Validate workflow outputs

#### Agent Tools (`agent_tools.py`) - 6 tools
Multi-framework agent creation:
- `create_adk_agent` - Create ADK agents
- `create_crewai_team` - Create CrewAI multi-agent teams
- `create_a2a_agent` - Create A2A protocol agents
- `create_langbase_agent` - Create Langbase RAG agents
- `create_agui_agent` - Create AGUI interface agents
- `list_agents` - List all created agents

#### Local Control Tools (`local_tools.py`) - 7 tools
System automation:
- `execute_system_command` - Execute shell commands
- `list_processes` - List running processes
- `kill_process` - Terminate processes
- `list_files` - List directory contents
- `read_file` - Read file contents
- `open_url` - Open URLs in browser
- `get_system_info` - Get system information

## Usage

### Importing Tools

```python
from tools import ToolRegistry, N8N_TOOLS, AGENT_TOOLS, LOCAL_TOOLS

# Create registry
registry = ToolRegistry()

# Register tools
for tool in N8N_TOOLS + AGENT_TOOLS + LOCAL_TOOLS:
    registry.register(tool)
```

### Listing Tools

```python
# List all tools
all_tools = registry.list_tools()

# List by category
n8n_tools = registry.list_tools(category="n8n")
agent_tools = registry.list_tools(category="agent")
local_tools = registry.list_tools(category="local")
```

### Executing Tools

```python
# Execute a tool
result = registry.execute_tool("get_system_info")

# Execute with parameters
result = registry.execute_tool(
    "create_adk_agent",
    name="my_agent",
    model="gpt-4",
    tools=["github", "slack"],
    system_prompt="You are a helpful assistant"
)

# Check result
if result["success"]:
    data = result["data"]
    print(f"Success: {data}")
else:
    error = result["error"]
    print(f"Error: {error}")
```

### Searching Tools

```python
# Search for tools by keyword
file_tools = registry.search_tools("file")
agent_tools = registry.search_tools("agent")
```

## API Endpoints

The tools are exposed via FastAPI endpoints:

### `GET /tools/list`
List all available tools or filter by category.

Query parameters:
- `category` (optional): Filter by category (n8n, agent, local, cloud)

Example:
```bash
curl http://localhost:7860/tools/list?category=agent
```

### `POST /tools/execute`
Execute a specific tool.

Request body:
```json
{
  "tool": "create_adk_agent",
  "params": {
    "name": "my_agent",
    "model": "gpt-4",
    "tools": ["github", "slack"],
    "system_prompt": "You are a helpful assistant"
  }
}
```

Example:
```bash
curl -X POST http://localhost:7860/tools/execute \
  -H "Content-Type: application/json" \
  -d '{"tool": "get_system_info", "params": {}}'
```

## Tool Schema Structure

Each tool has a complete schema:

```python
{
    "name": "tool_name",                    # Unique identifier
    "display_name": "Tool Name",            # Human-readable name
    "description": "What this tool does",   # Detailed description
    "category": "local",                    # Category (n8n, agent, local, cloud)
    "parameters": [                         # Array of parameters
        {
            "name": "param_name",
            "type": "string",
            "description": "Parameter description",
            "required": true,
            "default": null,
            "enum": null
        }
    ],
    "returns": "Description of return value",
    "examples": [                           # Usage examples
        "Example 1",
        "Example 2"
    ]
}
```

## Testing

Run integration tests:
```bash
cd backend
python tests/test_tools.py
```

Tests cover:
- Tool imports
- Registry registration
- Tool listing and filtering
- Tool search
- Tool execution
- Schema validation

## Adding New Tools

1. Create a handler function:
```python
def my_tool_handler(param1: str, param2: int) -> Dict[str, Any]:
    """Handler logic"""
    # Your implementation
    return {"result": "data"}
```

2. Create a tool schema:
```python
my_tool = MCPTool(
    schema=ToolSchema(
        name="my_tool",
        display_name="My Tool",
        description="What my tool does",
        category="local",
        parameters=[
            ToolParameter(
                name="param1",
                type="string",
                description="First parameter",
                required=True
            ),
            ToolParameter(
                name="param2",
                type="number",
                description="Second parameter",
                required=False,
                default=0
            )
        ],
        returns="Description of return value",
        examples=["Example usage"]
    ),
    handler=my_tool_handler
)
```

3. Add to tool list and export:
```python
MY_TOOLS = [my_tool]
```

4. Register in main.py:
```python
from tools import MY_TOOLS

for tool in MY_TOOLS:
    tool_registry.register(tool)
```

## Statistics

- **Total Tools**: 17
- **N8N Tools**: 4
- **Agent Tools**: 6
- **Local Tools**: 7
- **Cloud Tools**: 0 (planned)

## Next Steps

- [ ] Add cloud service tools (GCP, WhatsApp, GitHub Actions)
- [ ] Add tool versioning
- [ ] Add tool deprecation handling
- [ ] Add tool rate limiting
- [ ] Add tool authentication
- [ ] Add tool documentation generation
