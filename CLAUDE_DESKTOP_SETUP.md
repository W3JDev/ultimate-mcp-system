# Claude Desktop Integration Guide

This guide shows how to connect the Ultimate MCP Hub to Claude Desktop.

## Prerequisites

1. **Claude Desktop** installed
2. **Python 3.11+** with dependencies installed
3. **Ultimate MCP System** cloned and set up

## Configuration

### Step 1: Locate Claude Desktop Config

**macOS/Linux**:
```bash
~/.config/Claude/claude_desktop_config.json
```

**Windows**:
```
%APPDATA%\Claude\claude_desktop_config.json
```

### Step 2: Add MCP Hub Server

Edit `claude_desktop_config.json` and add the Ultimate MCP Hub:

```json
{
  "mcpServers": {
    "ultimate-mcp-hub": {
      "command": "python",
      "args": [
        "/absolute/path/to/ultimate-mcp-system/backend/mcp_hub_server.py"
      ],
      "env": {
        "GITHUB_TOKEN": "your_github_token_here"
      }
    }
  }
}
```

**Important**: Replace `/absolute/path/to/ultimate-mcp-system` with the actual path on your system.

### Step 3: Optional Environment Variables

Add any of these environment variables as needed:

```json
{
  "mcpServers": {
    "ultimate-mcp-hub": {
      "command": "python",
      "args": ["/path/to/backend/mcp_hub_server.py"],
      "env": {
        "GITHUB_TOKEN": "ghp_...",
        "ANTHROPIC_API_KEY": "sk-ant-...",
        "OPENAI_API_KEY": "sk-...",
        "N8N_API_KEY": "...",
        "N8N_BASE_URL": "https://n8n.example.com"
      }
    }
  }
}
```

### Step 4: Restart Claude Desktop

Completely quit and restart Claude Desktop for changes to take effect.

## Verification

### Check Connection Status

1. Open Claude Desktop
2. Click the **🔌** (MCP) icon in the bottom right
3. You should see "ultimate-mcp-hub" listed as connected
4. Check the available tools count (should be 500+)

### Test Basic Tool

Ask Claude:

```
Can you list the available MCP tools?
```

Claude should show tools from:
- **Rube MCP**: `rube_RUBE_SEARCH_TOOLS`, etc.
- **Memory MCP**: `memory_create_entities`, etc.
- **GitHub MCP**: `github_create_issue`, etc.
- **Playwright MCP**: `playwright_navigate`, etc.
- **Custom Tools**: `custom_create_n8n_workflow`, etc.

### Test Tool Execution

Try a simple tool:

```
Use the custom_list_processes tool to show running processes
```

## Troubleshooting

### MCP Hub Not Appearing

**Check logs**:
```bash
tail -f backend/logs/mcp_hub.log
```

**Common issues**:
1. Incorrect path in config
2. Python not in PATH
3. Dependencies not installed

**Solution**:
```bash
# Verify Python path
which python  # macOS/Linux
where python  # Windows

# Verify dependencies
pip list | grep -E "(loguru|dotenv)"

# Test hub manually
cd backend
python mcp_hub_server.py
# Type: {"jsonrpc":"2.0","id":1,"method":"ping"}
# Should return: {"jsonrpc":"2.0","id":1,"result":{}}
```

### No Tools Showing Up

**Check integration logs**:
```bash
tail -f backend/logs/mcp_hub.log | grep "integration"
```

**Common issues**:
1. External MCP servers not installed
2. npm/npx not in PATH
3. Missing environment variables

**Solution**:
```bash
# Install external MCPs (optional)
npx -y @modelcontextprotocol/server-github
npx -y @modelcontextprotocol/server-memory
npx -y @playwright/mcp-server

# Verify npm/npx
which npx  # Should show path
```

### Tools Execute But Return Errors

**Check specific integration**:

1. **GitHub MCP**: Verify `GITHUB_TOKEN` is set and valid
2. **Rube MCP**: Check Rube server is installed
3. **Custom tools**: These are placeholders - integration pending

**Debug**:
```bash
# Enable verbose logging
export LOG_LEVEL=DEBUG

# Check Claude Desktop logs (macOS)
tail -f ~/Library/Logs/Claude/mcp*.log

# Check Claude Desktop logs (Windows)
# %APPDATA%\Claude\logs\mcp*.log
```

## Advanced Configuration

### Running Hub on Different Port

The hub uses stdio (stdin/stdout) by default, but you can modify for HTTP:

```python
# In mcp_hub_server.py, add at end:
if __name__ == "__main__":
    import uvicorn
    # ... create FastAPI wrapper ...
    uvicorn.run(app, host="0.0.0.0", port=7865)
```

Then configure Claude Desktop:

```json
{
  "mcpServers": {
    "ultimate-mcp-hub": {
      "url": "http://localhost:7865"
    }
  }
}
```

### Selective Integration Loading

Modify `mcp_hub_server.py` to only load specific integrations:

```python
# In MCPHubServer.start_integrations()
integrations_config = [
    ("github", GitHubMCPIntegration),  # Only GitHub
    # ("rube", RubeMCPIntegration),    # Commented out
]
```

## Usage Examples

### Example 1: GitHub Issue Creation

```
Create a GitHub issue in W3JDev/ultimate-mcp-system with title "Feature request: Add X" and body "Please add feature X"
```

### Example 2: Knowledge Graph

```
Use the memory MCP to create an entity for "Claude" as an AI assistant, then create a relation showing it was developed by Anthropic
```

### Example 3: Browser Automation

```
Use Playwright to navigate to https://example.com and take a screenshot
```

### Example 4: Custom Workflow

```
Use the custom_create_n8n_workflow tool to create a workflow that monitors GitHub issues and sends Slack notifications
```

## Performance Notes

- **First request**: May be slow (2-5 seconds) as integrations initialize
- **Subsequent requests**: Should be fast (<1 second)
- **Tool listing**: Cached after first call
- **Memory usage**: ~50-100MB per integration

## Security Considerations

1. **API Keys**: Stored in config file - ensure proper file permissions
2. **Subprocess Execution**: Hub spawns external MCP servers - review their security
3. **Local File Access**: Some tools can access local files - use with caution
4. **Network Access**: Integrations can make external API calls

## Support

- **Issues**: https://github.com/W3JDev/ultimate-mcp-system/issues
- **Documentation**: See `PHASE3_IMPLEMENTATION.md`
- **Logs**: Check `backend/logs/mcp_hub.log`

---

**Happy MCP Hubbing!** 🚀
