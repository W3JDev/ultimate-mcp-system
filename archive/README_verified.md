# 🤖 W3J MCP Hub - Multi-MCP Orchestration Platform

**Master Orchestrator connecting N8N Workflows · AI Agent Builder · Local System Control**

[![Creator](https://img.shields.io/badge/Creator-@W3JDev-purple)](https://github.com/W3JDev)
[![Python](https://img.shields.io/badge/Python-3.11+-blue)]()
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-14%20passing-brightgreen)]()

> **Verified Status**: See [PROJECT_STATUS.md](PROJECT_STATUS.md) for complete codebase analysis  
> **Quick Start**: See [QUICKSTART.md](QUICKSTART.md) for 5-minute setup  
> **AI Instructions**: See [.github/copilot-instructions.md](.github/copilot-instructions.md) for development guide

---

## 📋 What Is This?

**W3J MCP Hub** is a production-ready orchestration platform that coordinates three specialized MCP (Model Context Protocol) servers through a unified FastAPI interface. Each server handles a specific automation domain:

1. **N8N Automation MCP** (Port 7862) - AI-powered workflow generation and deployment
2. **Agent Builder MCP** (Port 7863) - Multi-framework AI agent creation (5 frameworks)
3. **Local Control MCP** (Port 7864) - System automation, file operations, browser control

The Master Orchestrator (Port 7860) routes requests using **Gemini 3 Pro** intent analysis and provides a chat interface for natural language interactions.

---

## ✅ Verified Capabilities (Code-Backed)

### 🏗 Core Architecture

```
Master Orchestrator (backend/main.py, FastAPI, port 7860)
    ├─ Gemini 3 Pro intent routing (Vertex AI)
    ├─ Tool Registry (17+ registered tools)
    ├─ Memory Manager (conversation context)
    └─ Lazy-loading MCP servers
         ├─ N8N Automation MCP (port 7862)
         ├─ Agent Builder MCP (port 7863)
         └─ Local Control MCP (port 7864)
```

**Launch Pattern**:
- ✅ `python launch_all_servers.py` - Spawns all 4 processes
- ✅ PID tracking in `backend/pids/`
- ✅ Graceful shutdown on Ctrl+C
- ✅ 3-second cold start (lazy loading)

### 🔧 N8N Automation MCP

**What It Does**: Creates N8N workflows from natural language descriptions

**Verified Components**:
- ✅ `workflow_builder.py` - AI generation via Claude 3.5 Haiku
- ✅ `deployer.py` - N8N REST API integration
- ✅ `templates/` - Pre-built workflow templates
- ✅ Gradio UI with 3 tabs (Create, Test, Deploy)

**Example Usage**:
```python
from backend.mcp_servers.n8n_automation.server import N8NAutomationMCP

mcp = N8NAutomationMCP()
workflow = mcp.create_workflow("When GitHub PR merged, send Slack message")
result = mcp.deploy_workflow(workflow)
```

**Requirements**: External N8N instance with API key

### 🤖 Agent Builder MCP

**What It Does**: Creates AI agents across 5 different frameworks

**Verified Frameworks**:
1. ✅ **ADK** (`adk_integration.py`) - Anthropic Agent Development Kit
2. ✅ **CrewAI** (`crewai_wrapper.py`) - Multi-agent teams (Python 3.10-3.12 only)
3. ✅ **A2A Protocol** (`a2a_protocol.py`) - Agent-to-agent communication
4. ✅ **Langbase** (`langbase_connector.py`) - RAG-powered agents
5. ✅ **AGUI** (`agui_interface.py`) - GUI interaction agents

**Example Usage**:
```python
from backend.mcp_servers.agent_builder.server import AgentBuilderMCP

mcp = AgentBuilderMCP()
agent = mcp.create_adk_agent(
    name="Research Assistant",
    tools="web_search,code_execution",
    model="claude-3-5-sonnet-20241022",
    system_prompt="Expert at finding and synthesizing information"
)
```

**Agent Storage**: In-memory `self.agents` dictionary (no persistence)

### 🖥 Local Control MCP

**What It Does**: System automation, file operations, browser control

**Verified Capabilities**:
- ✅ Execute shell commands with timeout
- ✅ Process management (list, kill)
- ✅ File operations (list, read, create)
- ✅ Browser automation (via Playwright)
- ✅ System information retrieval
- ✅ Gradio UI with 6 tabs

**Example Usage**:
```python
from backend.mcp_servers.local_control.server import LocalControlMCP

mcp = LocalControlMCP()
mcp.execute_command("dir", timeout=10)
mcp.list_files("C:/Projects")
mcp.open_url("https://example.com")
```

### 🛠 Tool System (17+ Tools)

**Architecture**:
```python
# backend/tools/base.py
class MCPTool:
    schema: ToolSchema  # Parameters, returns, examples
    handler: Callable   # Implementation function
    
    def execute(**kwargs) → Dict[str, Any]
```

**Tool Categories**:
- **N8N Tools** (4): create_workflow, test_workflow, deploy_workflow, validate_workflow
- **Agent Tools** (6): create_adk_agent, create_crewai_team, create_a2a_agent, etc.
- **Local Tools** (7): execute_command, list_processes, kill_process, list_files, etc.

**Registration** (`backend/main.py`):
```python
tool_registry = ToolRegistry()
for tool in N8N_TOOLS + AGENT_TOOLS + LOCAL_TOOLS:
    tool_registry.register(tool)
```

### 🔗 External MCP Integrations

**Client Wrappers Ready** (`backend/integrations/`):
- ✅ **GitHub** - Repository operations, issues, PRs
- ✅ **Playwright** - Browser automation
- ✅ **Memory** - Persistent memory storage
- ✅ **N8N MCP Client** - External n8n-mcp package
- ✅ **Rube** - Remote MCP access

**Pattern**:
```python
class BaseMCPIntegration:
    def start() → bool              # Launch subprocess
    def call_tool(name, params)     # Execute via JSON-RPC
    def stop()                      # Terminate
```

### 🤖 AI Integration (Gemini 3 Pro)

**Usage**: Intent routing in orchestrator

```python
# backend/gemini_client.py
client = GeminiClient()
intent = client.analyze_intent(user_input, context)
# Returns: {"target": "n8n"|"agent_builder"|"local_control", "confidence": 0-1}
```

**Fallback**: Keyword-based routing when Gemini unavailable

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** (3.13 supported with [workarounds](QUICKSTART.md#python-313-fix))
- **Windows PowerShell** (or adapt for Linux/Mac)
- **Optional**: Anthropic API key, N8N instance

### Installation

```powershell
# Clone repository
git clone https://github.com/W3JDev/ultimate-mcp-system.git
cd ultimate-mcp-system

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r backend/requirements.txt

# Python 3.13 fix (if needed)
pip install audioop-lts 'huggingface_hub==0.26.0' 'urllib3<2.4.0' --force-reinstall

# Optional: Install Playwright
playwright install chromium

# Configure environment (optional for testing)
cp .env.example .env
# Edit .env with your API keys
```

### Launch

```powershell
# Start all 4 servers
python launch_all_servers.py

# Access UIs:
# Master Orchestrator → http://localhost:7860
# N8N Automation     → http://localhost:7862
# Agent Builder      → http://localhost:7863
# Local Control      → http://localhost:7864
```

**Stop**: Press Ctrl+C in terminal

### Testing

```powershell
# Run all tests
python -m pytest tests/unit -v

# With coverage
python -m pytest tests --cov=backend
```

---

## 📚 Documentation

- **[PROJECT_STATUS.md](PROJECT_STATUS.md)** - Complete verified status (what actually works)
- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute setup guide with troubleshooting
- **[.github/copilot-instructions.md](.github/copilot-instructions.md)** - Comprehensive dev guide for AI assistants
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines
- **[backend/tools/README.md](backend/tools/README.md)** - Tool system architecture
- **[backend/mcp_protocol/README.md](backend/mcp_protocol/README.md)** - MCP protocol implementation

### Architecture Deep-Dive

See `.github/copilot-instructions.md` for:
- Three-layer orchestration design
- Tool architecture (base classes, registry, execution)
- Lazy loading rationale
- Gradio multi-tab UI pattern
- Testing patterns and fixtures
- Troubleshooting common issues

---

## 🔧 Development

### Adding a New Tool

```python
# 1. Define in backend/tools/local_tools.py
def my_tool_handler(param: str) -> Dict[str, Any]:
    return {"success": True, "result": param.upper()}

my_tool = MCPTool(
    schema=ToolSchema(
        name="my_tool",
        display_name="My Tool",
        description="Uppercases a string",
        category="local",
        parameters=[ToolParameter(name="param", type="string", description="Input")],
        returns="Uppercased string"
    ),
    handler=my_tool_handler
)

# 2. Add to LOCAL_TOOLS list
LOCAL_TOOLS = [..., my_tool]

# 3. Register in backend/main.py (auto-imports from list)
```

### Adding a New MCP Server

```python
# 1. Create backend/mcp_servers/my_server/server.py
class MyServerMCP:
    def __init__(self):
        self.data = {}
    
    def create_ui(self):
        # Gradio interface
        pass

# 2. Register in backend/orchestrator.py:_load_server()
elif server_name == "my_server":
    from mcp_servers.my_server.server import MyServerMCP
    self.mcp_servers["my_server"] = MyServerMCP()

# 3. Add to launch_all_servers.py servers list
```

---

## 🧪 Testing

**Current Status**: 14 unit tests, all passing

```powershell
# Unit tests (fast)
python -m pytest tests/unit -v

# Integration tests (requires servers)
python launch_all_servers.py       # Terminal 1
python -m pytest tests/integration -v  # Terminal 2

# Specific test
python -m pytest tests/unit/test_memory.py::TestMemoryManager::test_initialization -v
```

**Test Markers** (from `pytest.ini`):
- `@pytest.mark.unit` - Fast, no external dependencies
- `@pytest.mark.integration` - Requires servers running
- `@pytest.mark.requires_api_key` - Needs API keys
- `@pytest.mark.requires_servers` - Needs all 4 servers

---

## 🏛 Architecture Decisions

### Why Lazy Loading?
- **Problem**: Loading all 3 MCP servers on startup = 15+ seconds
- **Solution**: Import servers only when first request arrives
- **Trade-off**: First request slower, but orchestrator starts in <3 seconds

### Why Hybrid Protocol (REST + JSON-RPC)?
- **REST**: Chat UI, web API, inter-server communication
- **JSON-RPC over stdio**: Claude Desktop MCP protocol requirement
- **Implementation**: `backend/mcp_protocol/` for stdio, `backend/main.py` for REST

### Why No Database?
- **Current**: In-memory storage (agents, context)
- **Rationale**: Prototype phase, quick iteration
- **Future**: SQLite/PostgreSQL when multi-user needed

---

## 🚨 Known Limitations

### Current Version (v1.0)

- ⚠️ **No Persistence** - All data in-memory (agents lost on restart)
- ⚠️ **Single User** - No authentication or multi-tenancy
- ⚠️ **Gemini Required** - Falls back to keyword routing without Vertex AI access
- ⚠️ **External N8N** - Requires separate N8N instance for deployments
- ⚠️ **Python 3.13** - CrewAI incompatible (use 3.10-3.12 for CrewAI)
- ⚠️ **Test Coverage** - Only 14 tests (need 100+ for production)

### Production Considerations

- Add database (SQLite/PostgreSQL)
- Implement authentication
- Add rate limiting
- Implement error recovery/retry logic
- Add monitoring/observability
- Security audit (input sanitization, API key management)

---

## 📊 Project Stats

- **Python Files**: ~50
- **MCP Servers**: 3 (N8N, Agent Builder, Local Control)
- **Agent Frameworks**: 5 (ADK, CrewAI, A2A, Langbase, AGUI)
- **External Integrations**: 5 (GitHub, Playwright, Memory, N8N Client, Rube)
- **Tools**: 17+ registered
- **Tests**: 14 unit tests
- **Lines of Code**: ~3,000+ (backend only)

---

## 📖 Learn More

- **Model Context Protocol**: https://modelcontextprotocol.io/
- **Claude Desktop MCP**: https://docs.anthropic.com/claude/docs/mcp
- **N8N Automation**: https://n8n.io/
- **Gemini 3 Pro**: https://ai.google.dev/gemini-api/docs/models/gemini-v3

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Quick Contribution Workflow**:
1. Fork the repository
2. Create feature branch (`git checkout -b feature/my-feature`)
3. Make changes with tests
4. Run `python -m pytest tests/unit -v`
5. Commit (`git commit -m 'Add feature'`)
6. Push (`git push origin feature/my-feature`)
7. Open Pull Request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file

---

## 👨‍💻 Author

**[@W3JDev](https://github.com/W3JDev)**

Created for the MCP 1st Birthday Hackathon 2025 · [Submission Archive](archive/hackathon/)

---

## 🔗 Related Projects

- **n8n-mcp** - N8N MCP server package (external)
- **Anthropic MCP** - Official MCP servers by Anthropic
- **MCP Servers Gallery** - Community MCP servers

---

**Last Updated**: November 30, 2025  
**Status**: Verified by direct codebase analysis  
**See**: [PROJECT_STATUS.md](PROJECT_STATUS.md) for detailed verification results
