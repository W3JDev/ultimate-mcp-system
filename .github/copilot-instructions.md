# GitHub Copilot Instructions - Ultimate MCP System
{
    "text": "- Rule - Use Your Memory: Before starting any complex task, first use your memory tool to recall any relevant context. Run `powershell -File C:\\Users\\W3jde\\.config\\memory_tool.ps1 -action recall -query 'your_best_guess_for_a_keyword'`. Also, at the end of a task, reflect on what you learned and save it to memory by running the 'remember' action."
},
## Architecture Overview

This is a **multi-MCP orchestrator** system with 4 independent servers coordinated by a master orchestrator:

1. **Master Orchestrator** (`backend/main.py`) - Port 7860 - FastAPI routing hub
2. **N8N Automation MCP** (`backend/mcp_servers/n8n_automation/`) - Port 7862 - Workflow automation
3. **Agent Builder MCP** (`backend/mcp_servers/agent_builder/`) - Port 7863 - Multi-framework agent creation
4. **Local Control MCP** (`backend/mcp_servers/local_control/`) - Port 7864 - System automation

**Key Pattern**: Each MCP server is a standalone Gradio/FastAPI app. The orchestrator routes natural language requests to the appropriate MCP based on intent analysis.

## Critical Python 3.13 Compatibility Fix

**Always include these dependencies together:**
```bash
pip install audioop-lts  # Required for Gradio with Python 3.13
pip install 'huggingface_hub<1.0.0'  # Gradio 4.44.1 compatibility
```

**Why**: Python 3.13 removed `audioop` module. Gradio depends on it. Solution: `audioop-lts` + downgraded huggingface_hub.

## Development Workflow

### Starting Servers Locally
```bash
# Activate venv (Windows)
.\venv\Scripts\Activate.ps1

# Individual server
python backend/main.py  # Master on 7860
python backend/mcp_servers/agent_builder/server.py  # Agent Builder on 7863

# All servers (after fixing Python 3.13 issues)
python launch_all_servers.py
```

### Testing Servers
```powershell
Test-NetConnection -ComputerName localhost -Port 7860  # Check Master
Test-NetConnection -ComputerName localhost -Port 7863  # Check Agent Builder
```

## Project-Specific Conventions

### MCP Server Structure
Every MCP server follows this pattern:
```python
class SomeNameMCP:
    def __init__(self):
        self.logger = logger  # loguru logging
        # Initialize components
    
    def process(self, user_input: str) -> str:
        '''Handle natural language from orchestrator'''
        # Intent parsing and execution
        return response
    
    def create_ui() -> gr.Blocks:
        '''Gradio interface with multiple tabs'''
        # 6-tab pattern for complex MCPs
        return demo

if __name__ == "__main__":
    demo = create_ui()
    demo.launch(server_port=PORT)
```

### Logging Pattern
```python
from loguru import logger
logger.add("../../logs/service_name.log", rotation="1 day", retention="7 days")
logger.info(f"✅ Action completed")  # Use emoji prefixes for visual scanning
logger.error(f"❌ Error: {e}")
```

### Environment Variables
Always load via `python-dotenv`:
```python
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")
```

Check `.env.example` for required keys. Current keys: `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `N8N_API_KEY`, `N8N_BASE_URL`.

## Agent Frameworks Integration

The Agent Builder MCP supports 5 frameworks - each has a dedicated tab:
- **ADK** (AI Development Kit) - Agent building
- **CrewAI** - Multi-agent teams (requires Python 3.10-3.12, commented out for 3.13)
- **A2A** (Agent-to-Agent) - Inter-agent communication
- **Langbase** - RAG & memory
- **AGUI** - Agent GUI interfaces

**Pattern**: Store agent configs in `self.agents` dict with JSON serialization.

## Testing & Debugging

### Check Server Logs
```bash
# Logs are in backend/logs/
tail -f backend/logs/mcp_system.log
tail -f backend/logs/agent_builder.log
```

### Common Issues

**Gradio won't start with Python 3.13:**
```bash
pip install audioop-lts
pip install 'huggingface_hub<1.0.0'
```

**Port already in use:**
```powershell
Get-Process | Where-Object {$_.ProcessName -eq "python"} | Stop-Process
```

**Import errors from MCP servers:**
- Check you're running from project root: `python backend/mcp_servers/*/server.py`
- Relative imports assume execution from root

## File Organization Rules

- **AGENT.md**: Comprehensive AI agent instructions (READ FIRST)
- **SETUP_STATUS.md**: Real-time development status
- **CURRENT_STATUS.md**: Phase/milestone tracking
- Each MCP folder has its own README.md explaining purpose

**When adding new MCP servers:**
1. Create `backend/mcp_servers/new_mcp/server.py`
2. Follow 6-tab Gradio pattern (see agent_builder/server.py)
3. Add to orchestrator.py's `mcp_servers` dict
4. Update SETUP_STATUS.md

## Deployment Context

**GCP Cloud Run** is the existing infrastructure (NEVER suggest migration):
```bash
gcloud run deploy ultimate-mcp --source . --region us-central1
```

## Quick Reference Commands

```bash
# Install dependencies
pip install -r backend/requirements.txt
playwright install chromium  # For browser automation

# Create logs directory
mkdir -p backend/logs

# Run orchestrator
python backend/main.py

# Check all running servers
Get-Process python | Select-Object Id,ProcessName,StartTime
```

## When Making Changes

1. **Before editing**: Check SETUP_STATUS.md for latest known issues
2. **After editing**: Update relevant README.md if architecture changes
3. **New features**: Add to appropriate MCP server, not orchestrator (separation of concerns)
4. **Dependencies**: Add to requirements.txt with version pinning
5. **Python 3.13**: Always test Gradio imports work with audioop-lts

## Code Style

- Use type hints: `def process(self, input: str) -> Dict[str, Any]:`
- Docstrings for all public methods (Google style)
- Emoji prefixes in logs for quick scanning (✅ ❌ 🔍 📝 🚀)
- Keep MCP servers independent - no cross-imports between MCPs
- Use loguru, not built-in logging
