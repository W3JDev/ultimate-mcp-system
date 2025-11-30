# GitHub Copilot Instructions — Ultimate MCP System

**W3J MCP Hub**: Production-ready multi-MCP orchestration platform coordinating N8N workflows, multi-framework AI agents, and local system control via Claude Desktop integration.

## 🏗 Architecture Fundamentals

### Three-Layer Design
```
Master Orchestrator (backend/main.py, FastAPI, port 7860)
    ├─ N8N Automation MCP (port 7862) - workflow generation & deployment
    ├─ Agent Builder MCP (port 7863) - 5 agent frameworks (ADK, CrewAI, A2A, Langbase, AGUI)
    └─ Local Control MCP (port 7864) - system automation & browser control
```

**Launch pattern**: `python launch_all_servers.py` spawns all 4 servers with PIDs tracked in `backend/pids/`. Each sub-server is a self-contained Gradio app.

**Lazy loading**: Orchestrator imports sub-servers only when needed (`orchestrator.py:_load_server()`). Adds server directories to `sys.path` dynamically to handle relative imports.

### Tool Architecture
- **Base class**: `backend/tools/base.py` defines `MCPTool(schema, handler)` - all tools inherit this
- **Schema**: `ToolSchema` with Pydantic models for parameters, returns, examples  
- **Registry**: `backend/tools/registry.py` centralizes registration, discovery, execution by category (n8n/agent/local/cloud)
- **Categories**: 17 tools across 4 files: `n8n_tools.py` (4), `agent_tools.py` (6), `local_tools.py` (7), plus meta-tools
- **Registration pattern**: In `backend/main.py`, import tool lists (`N8N_TOOLS`, etc.) and call `tool_registry.register(tool)` for each

**Adding new tools**: 
1. Define in appropriate `backend/tools/*_tools.py` using `MCPTool` + `ToolSchema`
2. Add to category list (e.g., `AGENT_TOOLS = [...]`)
3. Import and register in `backend/main.py` init sequence

### Protocol Implementation
- **MCP Protocol**: JSON-RPC 2.0 over stdio in `backend/mcp_protocol/` (transport, lifecycle, handler)
- **REST API**: FastAPI serves chat interface at root + `/api/*` endpoints
- **Integration**: Both protocols coexist - Orchestrator uses REST, MCP protocol is for Claude Desktop stdio channels

## 🛠 Critical Developer Workflows

### Starting Services (Windows PowerShell)
```powershell
# All servers at once (recommended for development)
python launch_all_servers.py    # Spawns 4 processes, Ctrl+C stops all

# Individual server testing
python backend/main.py                                        # Port 7860 (orchestrator)
python backend/mcp_servers/n8n_automation/server.py          # Port 7862
python backend/mcp_servers/agent_builder/server.py           # Port 7863  
python backend/mcp_servers/local_control/server.py           # Port 7864
```

**Port conflicts**: `Get-Process | Where-Object {$_.ProcessName -eq 'python'} | Stop-Process -Force`

### Testing
```powershell
# Always run from repo root (import path requirements)
python -m pytest tests -v                     # All tests (49 pass, 20 skip)
python -m pytest tests/unit -v                # Unit only
python -m pytest tests/integration -v         # Integration (needs servers)
python -m pytest tests --cov=backend          # With coverage
```

**Test markers**: `@pytest.mark.unit`, `@pytest.mark.requires_servers`, `@pytest.mark.requires_api_key` (see `pytest.ini`)

**Fixtures**: `tests/conftest.py` provides mocked Anthropic client, test env vars (`TESTING=1`), and fixture helpers

### Deployment (GCP Cloud Run Only)
```powershell
# Main orchestrator
gcloud run deploy w3j-mcp-hub --source . --region us-central1 --project stellar-state-471406-f8

# N8N with Cloud SQL
gcloud run deploy n8n-533751401713 --set-env-vars DATABASE_TYPE=postgresdb,...

# Environment variables managed via Secret Manager (N8N_API_KEY, etc.)
```

**Production URLs**:
- MCP Hub: `https://w3j-mcp-hub-533751401713-uc.a.run.app`
- N8N: `https://n8n-533751401713.us-central1.run.app`

## 📝 Code Conventions

### Logging with Loguru + Emojis
```python
from loguru import logger

logger.info("📦 Loading component...")       # Initialization
logger.success("✅ Operation completed")      # Success
logger.warning("⚠️ Using fallback method")   # Warnings  
logger.error("❌ Failed to connect")          # Errors
```
- **Log files**: `backend/logs/*.log` (rotation: 1 day, retention: 7 days)
- **Diagnostic output**: MCP protocol uses stderr for logs (stdout reserved for JSON-RPC)

### Configuration & Secrets
```python
from dotenv import load_dotenv
import os

load_dotenv()  # Loads from .env (NEVER commit this file)
api_key = os.getenv("ANTHROPIC_API_KEY")
```
**Production**: Use `os.environ` directly - Cloud Run injects env vars from Secret Manager

### Python Version Gotchas
- **3.11+** recommended, **3.13** supported with workarounds:
  ```powershell
  pip install audioop-lts 'huggingface_hub==0.26.0' 'urllib3<2.4.0' --force-reinstall
  ```
- **CrewAI**: Requires Python 3.10-3.12 (NOT 3.13) - document this in agent builder docs

### UI Pattern: Gradio Multi-Tab Layout
All sub-servers follow the "multi-tab Gradio pattern" (see `agent_builder/server.py` lines 270-410):
```python
with gr.Blocks(theme=gr.themes.Soft(), title="Server Name") as demo:
    gr.Markdown("# Header")
    
    with gr.Tab("🔧 Tab 1"):
        # Components for feature 1
    
    with gr.Tab("👥 Tab 2"):
        # Components for feature 2
    
    # ... more tabs
    
demo.launch(server_port=7863, share=False)
```

**Agent Builder**: 6 tabs (ADK Agent, CrewAI Team, A2A Protocol, Langbase RAG, AGUI Interface, List Agents)
**N8N Automation**: 3 tabs (Create Workflow, Test Workflow, Deploy)
**Local Control**: 6 tabs (System Commands, App Control, File Operations, Input Control, Browser Automation, System Info)

## 🔌 Integration Points

### Gemini 3 Pro (Vertex AI)
- **Client**: `backend/gemini_client.py` wraps `google-genai` SDK
- **Model**: `gemini-3-pro-preview` via Vertex AI endpoint
- **Usage**: Intent analysis in `orchestrator.py:_analyze_intent()` - falls back to keyword matching if unavailable
- **Project**: `stellar-state-471406-f8` (must have Vertex AI API enabled)

### N8N Integration
- **API**: `backend/mcp_servers/n8n_automation/deployer.py` uses N8N REST API
- **Workflow generation**: `workflow_builder.py` creates JSON from natural language
- **Env vars**: `N8N_API_URL`, `N8N_API_KEY` (from settings page)
- **Templates**: `backend/mcp_servers/n8n_automation/templates/*.json` for common patterns

### Agent Frameworks (5 supported)
Located in `backend/mcp_servers/agent_builder/`:
- **ADK**: `adk_integration.py` - Anthropic's Agent Development Kit
- **CrewAI**: `crewai_wrapper.py` - Multi-agent teams (Python 3.10-3.12 only)
- **A2A Protocol**: `a2a_protocol.py` - Agent-to-agent communication
- **Langbase**: `langbase_connector.py` - RAG-powered agents
- **AGUI**: `agui_interface.py` - GUI interaction agents

**Agent storage**: Stored in `self.agents` dict in `server.py:AgentBuilderMCP.__init__()`

### Remote PC Bridge (WebSocket)
- **Bridge**: `backend/remote_bridge.py` connects Cloud Run to local PC via WSS
- **Local agent**: `backend/local_agent.py` runs on PC (port 8765)
- **Setup script**: `setup_remote_pc.ps1` automates Cloudflare tunnel creation
- **Env vars**: `REMOTE_PC_BRIDGE_URL` (wss://...), `REMOTE_PC_AUTH_TOKEN`

## 🐛 Troubleshooting Patterns

### Import Errors
**Always run from repo root** - scripts use relative imports expecting `backend/` in path:
```powershell
cd C:\Users\W3jde\PROJECTS\MCP\ultimate-mcp-system
python backend/main.py  # NOT: cd backend && python main.py
```

### Server Won't Start
1. Check port availability: `Test-NetConnection -ComputerName localhost -Port 7860`
2. Kill zombie processes: `Get-Process | Where-Object {$_.ProcessName -eq 'python'} | Stop-Process`
3. Check logs: `backend/logs/*.log` for stack traces
4. Verify venv: `.\.venv\Scripts\Activate.ps1` before running

### MCP Protocol Issues
- **Claude Desktop**: Config at `C:\Users\W3jde\AppData\Roaming\Code\User\mcp.json`
- **Server list**: MCP Hub server is `n8n-mcp` entry with stdio transport
- **Debugging**: Check stderr output (protocol logs) vs stdout (JSON-RPC messages)

## 🎨 User-Facing Design Patterns

### Chat Interface (FastAPI HTML)
The main orchestrator serves an interactive chat UI at root `/`:
```python
# backend/main.py lines 68-300+
@app.get("/", response_class=HTMLResponse)
async def root():
    return """<!DOCTYPE html>..."""  # Embedded gradient chat UI
```
- **Styling**: Purple gradient background (`#667eea` to `#764ba2`)
- **Real-time chat**: Message bubbles, auto-scroll, typing indicators
- **API endpoint**: `POST /api/chat` for message submission

### Gradio Multi-Tab Pattern (Sub-servers)
Each MCP server follows consistent tab organization:
```python
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# Server Title")
    with gr.Tab("🔧 Feature 1"): ...
    with gr.Tab("👥 Feature 2"): ...
```

**Tab counts by server**:
- **N8N** (3 tabs): Create → Test → Deploy
- **Agent Builder** (6 tabs): ADK → CrewAI → A2A → Langbase → AGUI → List
- **Local Control** (6 tabs): Commands → Apps → Files → Input → Browser → Info

### Error Handling UI
```python
try:
    result = operation()
    return f"✅ Success: {result}"
except Exception as e:
    logger.error(f"❌ {operation_name} failed: {e}")
    return f"❌ Error: {str(e)}"  # User-friendly error message
```

## 🏛 Architectural Decisions

### Why Lazy Loading?
**Problem**: Loading all 3 MCP servers on startup increased cold start to 15+ seconds.  
**Solution**: `orchestrator.py:_load_server()` imports only when first request arrives for that MCP.  
**Trade-off**: First request to each MCP is slower, but orchestrator starts in <3 seconds.

### Why Hybrid Protocol (REST + JSON-RPC)?
**REST**: Chat UI, web API, internal communication between orchestrator and sub-servers.  
**JSON-RPC over stdio**: Claude Desktop integration - MCP protocol requirement for tool discovery.  
**Implementation**: `backend/mcp_protocol/` handles stdio, `backend/main.py` FastAPI handles REST.

### Why No Database?
**Current**: In-memory storage in `self.agents` dicts and `MemoryManager` context lists.  
**Rationale**: Prototype/demo phase - persistence added via Cloud SQL for N8N only.  
**Future**: Add SQLite/PostgreSQL when multi-user sessions needed.

### Agent Framework Abstractions
All 5 frameworks wrapped with consistent interface:
```python
# Each integration has create_agent() → returns {"success": bool, "agent": dict}
adk_integration.py:create_agent(name, description, capabilities, model)
crewai_wrapper.py:create_agent(role, goal, backstory, tools)
a2a_protocol.py:create_agent(...)
langbase_connector.py:create_agent(...)
agui_interface.py:create_agent(...)
```

**Stored centrally**: `AgentBuilderMCP.agents[agent_id] = config`

## 📖 Development Guides

### Adding a New MCP Server
1. **Create directory**: `backend/mcp_servers/your_server/`
2. **Implement class**:
   ```python
   class YourServerMCP:
       def __init__(self): ...
       def create_ui(self): # Gradio interface
   ```
3. **Register in orchestrator**: `backend/orchestrator.py:_load_server()` add case
4. **Add to launcher**: `launch_all_servers.py` servers list
5. **Document**: Update `backend/mcp_servers/README.md`

### Adding a New Tool
1. **Define handler**: `backend/tools/*_tools.py`
   ```python
   def my_tool_handler(param1: str, param2: int) -> Dict[str, Any]:
       # Implementation
       return {"success": True, "data": result}
   ```
2. **Create schema**:
   ```python
   my_tool = MCPTool(
       schema=ToolSchema(
           name="my_tool",
           display_name="My Tool",
           description="What it does",
           category="local",  # n8n/agent/local/cloud
           parameters=[...],
           returns="Description of return value",
           examples=["Example usage 1", "Example 2"]
       ),
       handler=my_tool_handler
   )
   ```
3. **Register**: Add to `LOCAL_TOOLS` list in same file
4. **Import**: `backend/main.py` imports and registers via registry

### Testing Workflow
```powershell
# Unit tests (fast, no servers needed)
.\.venv\Scripts\python.exe -m pytest tests/unit -v

# Integration tests (requires servers running)
python launch_all_servers.py  # Terminal 1
.\.venv\Scripts\python.exe -m pytest tests/integration -v  # Terminal 2

# Test specific module
.\.venv\Scripts\python.exe -m pytest tests/unit/test_memory.py -v

# Coverage report
.\.venv\Scripts\python.exe -m pytest tests --cov=backend --cov-report=html
# View: open htmlcov/index.html
```

### Debugging MCP Protocol
**Stdio logging**: All protocol logs go to stderr (stdout reserved for JSON-RPC).  
**Check Claude Desktop logs**: `%APPDATA%\Code\User\globalStorage\...logs`  
**Validate messages**:
```python
# backend/mcp_protocol/transport.py validates JSON-RPC 2.0 format
{
    "jsonrpc": "2.0",
    "id": 1,  # Required for requests
    "method": "tools/list",  # Or tools/call, initialize
    "params": {...}
}
```

### Environment Setup per Service
```bash
# Local development
.env file with:
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
N8N_API_KEY=...
N8N_API_URL=http://localhost:5678/api/v1

# Cloud Run (via Secret Manager)
GOOGLE_CLOUD_PROJECT=stellar-state-471406-f8
GEMINI_MODEL=gemini-3-pro-preview
N8N_API_URL=https://n8n-533751401713.us-central1.run.app/api/v1
N8N_API_KEY=<from-secret>
```

## 📚 Key Files Reference

- **`launch_all_servers.py`**: Multi-server startup, PID tracking, shutdown handler
- **`backend/main.py`**: FastAPI app, tool registration, orchestrator init, chat UI
- **`backend/orchestrator.py`**: Intent routing (Gemini 3 Pro), lazy server loading
- **`backend/gemini_client.py`**: Vertex AI wrapper for intent analysis
- **`backend/tools/base.py`**: `MCPTool`, `ToolSchema`, parameter validation
- **`backend/tools/registry.py`**: Tool discovery, categorization, execution
- **`backend/mcp_protocol/handler.py`**: JSON-RPC request routing for Claude Desktop
- **`backend/mcp_servers/*/server.py`**: Each MCP's Gradio interface + business logic
- **`backend/integrations/*_integration.py`**: External MCP client wrappers (GitHub, Playwright, etc.)
- **`QUICKSTART.md`**: Python 3.13 fix, launch instructions, testing commands
- **`DEPLOYMENT_COMPLETE.md`**: GCP Cloud Run deployment, remote PC setup
