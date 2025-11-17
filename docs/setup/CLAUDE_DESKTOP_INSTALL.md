# Claude Desktop MCP Installation Instructions

## Quick Install (Windows)

### Step 1: Locate Claude Desktop Config Directory
The config file is located at:
```
%APPDATA%\Claude\claude_desktop_config.json
```

Full path typically:
```
C:\Users\W3jde\AppData\Roaming\Claude\claude_desktop_config.json
```

### Step 2: Backup Existing Config (if any)
```powershell
Copy-Item "$env:APPDATA\Claude\claude_desktop_config.json" "$env:APPDATA\Claude\claude_desktop_config.json.backup" -ErrorAction SilentlyContinue
```

### Step 3: Copy Our MCP Config
```powershell
# Create Claude config directory if it doesn't exist
New-Item -Path "$env:APPDATA\Claude" -ItemType Directory -Force

# Copy our config
Copy-Item "C:\Users\W3jde\PROJECTS\MCP\ultimate-mcp-system\claude_desktop_config.json" "$env:APPDATA\Claude\claude_desktop_config.json" -Force
```

### Step 4: Restart Claude Desktop
1. Quit Claude Desktop completely
2. Reopen Claude Desktop
3. Look for MCP servers in the connection status

---

## What Gets Installed

Your Claude Desktop will have access to 3 MCP servers:

### 1. **ultimate-mcp-n8n** (N8N Automation)
- Create workflows from natural language
- Test workflow execution
- Deploy workflows to N8N instance
- **Tools:**
  - `create_workflow` - Generate N8N workflow from description
  - `test_workflow` - Test workflow with sample data
  - `deploy_workflow` - Deploy workflow to N8N

### 2. **ultimate-mcp-agent-builder** (Agent Builder)
- Build agents across 5 frameworks (ADK, A2A, CrewAI, Langbase, AGUI)
- Multi-agent orchestration
- Agent-to-Agent communication
- **Tools:**
  - `create_adk_agent` - Create ADK agent
  - `create_crewai_team` - Build CrewAI multi-agent team
  - `create_a2a_agent` - Set up A2A communication agent
  - `create_langbase_agent` - Memory-enabled RAG agent
  - `create_agui_agent` - GUI interface agent

### 3. **ultimate-mcp-local-control** (Local Control)
- System automation and control
- Browser automation with Playwright
- Safe file operations
- **Tools:**
  - `get_system_info` - CPU, memory, disk stats
  - `run_safe_command` - Execute whitelisted commands
  - `list_processes` - View running processes
  - `start_browser` - Launch browser automation
  - `navigate` - Go to URL
  - `screenshot` - Capture screenshot
  - `read_file` - Read file contents
  - `write_file` - Write to file
  - `list_directory` - List directory contents

---

## Verification

### Check if MCP Servers Are Running
Open PowerShell and run:
```powershell
Test-NetConnection -ComputerName localhost -Port 7862 -InformationLevel Quiet  # N8N
Test-NetConnection -ComputerName localhost -Port 7863 -InformationLevel Quiet  # Agent Builder
Test-NetConnection -ComputerName localhost -Port 7864 -InformationLevel Quiet  # Local Control
```

All should return `True`.

### Test in Claude Desktop
After restarting Claude Desktop, ask:
```
"Can you list the available MCP servers?"
"Create a simple N8N workflow that sends an email"
"Get my system information"
```

---

## Troubleshooting

### MCP Servers Not Showing in Claude
1. Verify config file location: `$env:APPDATA\Claude\claude_desktop_config.json`
2. Check JSON syntax is valid
3. Ensure absolute paths in config are correct
4. Restart Claude Desktop completely (quit, not just minimize)

### MCP Tools Not Working
1. Check servers are running: `python launch_all_servers.py`
2. Verify ports 7862, 7863, 7864 are accessible
3. Check environment variables in config match your `.env` file

### Permission Errors
Run PowerShell as Administrator:
```powershell
Start-Process powershell -Verb RunAs
```

---

## Environment Variables

The config includes these environment variables:

**N8N Server:**
- `ANTHROPIC_API_KEY` - For Claude-powered workflow generation
- `OPENAI_API_KEY` - For OpenAI model support
- `N8N_API_KEY` - N8N instance API key
- `N8N_BASE_URL` - N8N instance URL (default: http://localhost:5678/)
- `GITHUB_TOKEN` - GitHub API access

**Agent Builder:**
- `ANTHROPIC_API_KEY` - For AI agent reasoning
- `OPENAI_API_KEY` - For alternative models

**Local Control:**
- `PLAYWRIGHT_BROWSERS_PATH` - Playwright browser binaries location

---

## Security Notes

⚠️ **IMPORTANT:** The config file contains API keys in plain text!

- Keep `claude_desktop_config.json` secure
- Do NOT commit it to Git
- Ensure `.gitignore` excludes this file
- Rotate API keys if config is exposed

---

## Next Steps

1. **Run Installation Script:** See Step 3 above
2. **Restart Claude Desktop**
3. **Test MCP Connection:** Ask Claude to list MCP servers
4. **Try Example Commands:** Create workflow, build agent, get system info
5. **Read Documentation:** Check `PROJECT_STATUS_HACKATHON.md` for full capabilities

---

## Manual Configuration Alternative

If you prefer to manually edit the config, open:
```
C:\Users\W3jde\AppData\Roaming\Claude\claude_desktop_config.json
```

And merge the contents of:
```
C:\Users\W3jde\PROJECTS\MCP\ultimate-mcp-system\claude_desktop_config.json
```

---

**Status:** ✅ Configuration file ready for installation  
**Last Updated:** November 17, 2025  
**Servers Required:** All 3 MCP servers must be running
