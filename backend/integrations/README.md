# MCP Integrations

This directory contains integration modules for connecting to external MCP servers.

## Overview

The Ultimate MCP System aggregates multiple MCP servers into a single hub, providing unified access to 500+ tools from various sources.

## Available Integrations

### 1. Rube MCP Integration (`rube_integration.py`)
**Purpose**: Access to 500+ app integrations via Rube MCP

**Features**:
- Search available apps
- Get app-specific actions
- Execute app integrations

**Installation**:
```bash
npx -y @rube/mcp-server
```

**Example Usage**:
```python
from integrations import RubeMCPIntegration

with RubeMCPIntegration() as rube:
    apps = rube.search_apps("messaging")
    actions = rube.get_app_actions("slack")
```

### 2. Memory MCP Integration (`memory_integration.py`)
**Purpose**: Knowledge graph and memory capabilities

**Features**:
- Create entities in knowledge graph
- Create relations between entities
- Search nodes
- Open specific nodes

**Installation**:
```bash
npx -y @modelcontextprotocol/server-memory
```

**Example Usage**:
```python
from integrations import MemoryMCPIntegration

with MemoryMCPIntegration() as memory:
    memory.create_entities([
        {"name": "John", "type": "person"},
        {"name": "Acme Corp", "type": "company"}
    ])
    memory.create_relations([
        {"from": "John", "to": "Acme Corp", "type": "works_at"}
    ])
```

### 3. GitHub MCP Integration (`github_integration.py`)
**Purpose**: GitHub repository operations

**Features**:
- Create repositories
- Create issues and pull requests
- Search repositories
- Get file contents
- Manage repository operations

**Installation**:
```bash
npx -y @modelcontextprotocol/server-github
```

**Environment Variables**:
- `GITHUB_TOKEN`: GitHub personal access token

**Example Usage**:
```python
from integrations import GitHubMCPIntegration

with GitHubMCPIntegration(github_token="your_token") as github:
    github.create_issue(
        "user/repo",
        title="Bug found",
        body="Description",
        labels=["bug"]
    )
```

### 4. Playwright MCP Integration (`playwright_integration.py`)
**Purpose**: Browser automation capabilities

**Features**:
- Navigate to URLs
- Take screenshots
- Click elements
- Fill forms
- Evaluate JavaScript

**Installation**:
```bash
npx -y @playwright/mcp-server
playwright install chromium
```

**Example Usage**:
```python
from integrations import PlaywrightMCPIntegration

with PlaywrightMCPIntegration() as browser:
    browser.navigate("https://example.com")
    browser.fill("#search", "query")
    browser.click("#submit")
    browser.screenshot()
```

## Base Integration Class

All integrations inherit from `BaseMCPIntegration` which provides:

- **Subprocess management**: Start/stop MCP server processes
- **JSON-RPC protocol**: Handle initialize, tools/list, tools/call
- **Error handling**: Graceful fallbacks when servers unavailable
- **Context manager**: Automatic cleanup with `with` statement

## Architecture

```
MCPHubServer (mcp_hub_server.py)
    ├─ RubeMCPIntegration
    │   └─ Rube MCP Server (subprocess)
    ├─ MemoryMCPIntegration
    │   └─ Memory MCP Server (subprocess)
    ├─ GitHubMCPIntegration
    │   └─ GitHub MCP Server (subprocess)
    └─ PlaywrightMCPIntegration
        └─ Playwright MCP Server (subprocess)
```

## Tool Naming Convention

Tools from external MCPs are prefixed with the integration name to avoid conflicts:

- `rube_RUBE_SEARCH_TOOLS`
- `memory_create_entities`
- `github_create_issue`
- `playwright_navigate`

Custom tools from this system are prefixed with `custom_`:

- `custom_create_n8n_workflow`
- `custom_create_adk_agent`
- `custom_execute_system_command`

## Error Handling

All integrations handle errors gracefully:

1. **Startup failures**: If an MCP server fails to start, the hub continues with available integrations
2. **Tool call errors**: Errors are logged and returned in the response
3. **Network issues**: Timeout and retry logic built-in

## Testing

Run integration tests:

```bash
cd backend
python -m pytest tests/test_integrations.py -v
```

Or with unittest:

```bash
cd backend
python -m unittest tests.test_integrations
```

## Configuration

Integrations can be configured via environment variables:

```bash
# GitHub token for GitHub MCP
export GITHUB_TOKEN=your_token_here

# Additional configuration as needed
```

## Development

### Adding a New Integration

1. Create `new_mcp_integration.py`:
```python
from .base_integration import BaseMCPIntegration

class NewMCPIntegration(BaseMCPIntegration):
    def __init__(self):
        server_command = ["npx", "-y", "@vendor/mcp-server"]
        super().__init__(server_command, "New MCP")
    
    def get_integration_name(self) -> str:
        return "new"
```

2. Add to `__init__.py`:
```python
from .new_mcp_integration import NewMCPIntegration

__all__ = [..., "NewMCPIntegration"]
```

3. Register in `mcp_hub_server.py`:
```python
integrations_config = [
    ...
    ("new", NewMCPIntegration),
]
```

## Troubleshooting

### Integration won't start
- Check that the MCP server is installed: `npx -y @vendor/mcp-server`
- Check logs: `tail -f logs/mcp_hub.log`
- Verify environment variables are set

### Tools not appearing
- Ensure integration started successfully (check logs)
- Verify MCP server responds to `tools/list`
- Check tool name prefixing is correct

### Tool calls failing
- Check argument format matches tool's `inputSchema`
- Verify MCP server is still running
- Check for error messages in logs

## References

- [MCP Protocol Specification](https://modelcontextprotocol.io/docs)
- [MCP SDK Documentation](https://github.com/modelcontextprotocol)
- [Ultimate MCP System Documentation](../../README.md)
