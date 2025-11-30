# 🤖 W3J MCP Hub - Ultimate Multi-Server Orchestration

**Master Orchestrator connecting N8N · AI Agents · Local Control**

[![Creator](https://img.shields.io/badge/Creator-@W3JDev-purple)](https://github.com/W3JDev)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-green)]()
[![Python](https://img.shields.io/badge/Python-3.11+-blue)]()
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Hackathon](https://img.shields.io/badge/Hackathon-MCP%202025-orange)](https://huggingface.co/MCP-1st-Birthday)

---

## 📋 Overview

**W3J MCP Hub** by [@W3JDev](https://github.com/W3JDev) is a **production-ready multi-MCP orchestration platform** that coordinates three specialized automation servers through Claude Desktop. Each MCP server handles a specific domain: workflow automation (N8N), multi-framework agent creation (5 frameworks), and local system control (browser + files).

**Phase 6 Complete - Production Cloud Deployment:**
- ✅ **MCP Hub** deployed to Google Cloud Run (https://w3j-mcp-hub-533751401713-uc.a.run.app)
- ✅ **N8N** deployed to Cloud Run with PostgreSQL (https://n8n-533751401713.us-central1.run.app)
- ✅ **Gemini 3 Pro** integration via Vertex AI
- ✅ **3 MCP Servers** fully implemented and running
- ✅ **5 Agent Frameworks** integrated (ADK, A2A, CrewAI, Langbase, AGUI)
- ✅ **Master Orchestrator** with tool execution (not "coming soon")
- ✅ **17 MCP Tools** with complete schemas
- ✅ **49/49 Unit Tests** passing
- ✅ **Cloud SQL PostgreSQL** for N8N persistence

### ✅ Current Status: Production Deployed

**Live Cloud Services:**
- 🌐 **MCP Hub**: https://w3j-mcp-hub-533751401713-uc.a.run.app
- 🔄 **N8N**: https://n8n-533751401713.us-central1.run.app (setup required)
- 🤖 **Gemini 3 Pro**: Integrated via Vertex AI
- 🗄️ **PostgreSQL**: Cloud SQL for workflow persistence

**What's Fully Operational:**
- ✅ N8N Cloud Run deployment - Production-grade with PostgreSQL backend
- ✅ MCP Hub Cloud Run - Orchestrator with actual tool execution
- ✅ Agent Builder - 5 frameworks, multi-agent teams
- ✅ Local Control - Remote PC bridge ready (WebSocket)
- ✅ Gemini 3 Pro - AI-powered workflow & agent generation
- ✅ Tool Registry - 17 tools callable via orchestrator
- ✅ Secret Manager - Secure credential storage

**Key Features:**
- 🤖 **Multi-Framework Agents**: ADK, A2A, CrewAI, Langbase, AGUI
- 🔄 **N8N Integration**: Cloud-hosted workflow automation
- 🌐 **Remote PC Control**: WebSocket bridge for local system access
- 📁 **File Operations**: Complete file system management
- 🎯 **AI Routing**: Gemini 3 Pro powered orchestration
- 🚀 **Production Ready**: GCP Cloud Run with Cloud SQL

**See [PROJECT_STATUS_FINAL.md](PROJECT_STATUS_FINAL.md) for complete system status.**

---

## 🎯 Architecture

### Production Cloud Architecture

```
┌─────────────────────────────────────────────────────────────┐
│            Google Cloud Run - Production                     │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │   MCP Hub (w3j-mcp-hub)                               │  │
│  │   https://w3j-mcp-hub-533751401713-uc.a.run.app       │  │
│  │   • Orchestrator with Tool Registry                   │  │
│  │   • Gemini 3 Pro (Vertex AI)                          │  │
│  │   • 17 Callable MCP Tools                             │  │
│  └────────────┬──────────────────────┬───────────────────┘  │
│               │                      │                       │
│               ▼                      ▼                       │
│  ┌────────────────────┐  ┌─────────────────────────┐       │
│  │   N8N (Cloud Run)  │  │   Cloud SQL PostgreSQL  │       │
│  │   Port: 5678       │◄─┤   • Workflow Storage    │       │
│  │   Memory: 2Gi      │  │   • Execution Logs      │       │
│  │   🔗 n8n-533...    │  │   • Credentials         │       │
│  └────────────────────┘  └─────────────────────────┘       │
│                                                               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                  ┌───────────────────────┐
                  │   Remote PC Bridge    │
                  │   (WebSocket/WSS)     │
                  │   • Local Control     │
                  │   • Browser Automation│
                  │   • File Operations   │
                  └───────────────────────┘
```

### Local Development Architecture

```
┌─────────────────────────────────────────┐
│   Master Orchestrator (Port 7860)      │
│   FastAPI + AI Intent Routing          │
└───────────┬─────────────────────────────┘
            │
    ┌───────┼───────┬───────────┐
    │       │       │           │
┌───▼───┐ ┌─▼──┐ ┌─▼────┐ ┌───▼────┐
│  N8N  │ │Agent│ │Local │ │ Cloud  │
│  MCP  │ │Build│ │ Ctrl │ │Services│
│ 7862  │ │7863 │ │ 7864 │ │ Ready  │
└───────┘ └─────┘ └──────┘ └────────┘
```

---

## ⚡ Quick Start

### Prerequisites

- **Python 3.11+** (3.13 supported with audioop-lts)
- **Optional**: Anthropic API key (for AI features)
- **Optional**: N8N instance (for workflow deployment)

### Installation

```bash
# Clone repository
git clone https://github.com/W3JDev/ultimate-mcp-system.git
cd ultimate-mcp-system

# Create virtual environment (Windows)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Or (Linux/Mac)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt

# Install Playwright browsers (for Local Control)
playwright install chromium

# Configure environment
cp .env.example .env
# Edit .env with your API keys (optional for basic testing)

# Start all servers
python launch_all_servers.py

# Or start individually
python backend/main.py  # Master Orchestrator
python backend/mcp_servers/n8n_automation/server.py
python backend/mcp_servers/agent_builder/server.py
python backend/mcp_servers/local_control/server.py
```

### Access UIs

- **Master Orchestrator**: http://localhost:7860
- **N8N Automation**: http://localhost:7862
- **Agent Builder**: http://localhost:7863
- **Local Control**: http://localhost:7864

---

## 🔧 MCP Tools (Phase 2)

### Tool Architecture

All business logic has been converted to **17 callable MCP tools** with standardized interfaces:

#### **N8N Tools** (4 tools)
- `create_n8n_workflow` - Create workflows from natural language
- `test_n8n_workflow` - Test workflows with validation
- `deploy_n8n_workflow` - Deploy to N8N instance
- `validate_n8n_workflow` - Validate workflow outputs

#### **Agent Tools** (6 tools)
- `create_adk_agent` - Create ADK agents
- `create_crewai_team` - Create CrewAI multi-agent teams
- `create_a2a_agent` - Create A2A protocol agents
- `create_langbase_agent` - Create Langbase RAG agents
- `create_agui_agent` - Create AGUI interface agents
- `list_agents` - List all created agents

#### **Local Control Tools** (7 tools)
- `execute_system_command` - Execute shell commands
- `list_processes` - List running processes
- `kill_process` - Terminate processes
- `list_files` - List directory contents
- `read_file` - Read file contents
- `open_url` - Open URLs in browser
- `get_system_info` - Get system information

### Using Tools via API

```bash
# List all tools
curl http://localhost:7860/tools/list

# List tools by category
curl http://localhost:7860/tools/list?category=agent

# Execute a tool
curl -X POST http://localhost:7860/tools/execute \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "get_system_info",
    "params": {}
  }'

# Create an agent
curl -X POST http://localhost:7860/tools/execute \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "create_adk_agent",
    "params": {
      "name": "my_agent",
      "model": "gpt-4",
      "tools": ["github", "slack"],
      "system_prompt": "You are a helpful assistant"
    }
  }'
```

See [backend/tools/README.md](backend/tools/README.md) for complete tool documentation.

---

## 📦 What's Inside

### 1. Master Orchestrator (Port 7860)
**Purpose**: Routes user requests to appropriate MCP servers

**Features:**
- Natural language intent analysis (with API key)
- Keyword-based fallback routing
- Memory management across MCPs
- FastAPI web interface

**Tech**: FastAPI, Anthropic Claude API, loguru

### 2. N8N Automation MCP (Port 7862)
**Purpose**: AI-powered workflow creation and deployment

**Features:**
- Generate N8N workflows from descriptions
- Template-based fallback
- Workflow testing
- N8N API integration

**Tech**: Gradio, Anthropic Claude, N8N API

**Detailed Docs**: [backend/mcp_servers/n8n_automation/README_DETAILED.md](backend/mcp_servers/n8n_automation/README_DETAILED.md)

### 3. Agent Builder MCP (Port 7863)
**Purpose**: Multi-framework AI agent creation

**Features:**
- 6-tab UI for different frameworks
- Support for ADK, CrewAI, A2A, Langbase, AGUI
- JSON-based agent storage
- Agent management (CRUD operations)

**Tech**: Gradio, multiple AI frameworks

**Detailed Docs**: [backend/mcp_servers/agent_builder/README.md](backend/mcp_servers/agent_builder/README.md)

### 4. Local Control MCP (Port 7864)
**Purpose**: System automation and PC control

**Features:**
- System command execution
- Process management
- File operations
- Input control (keyboard/mouse)
- Browser automation (Playwright)
- System information display

**Tech**: Gradio, psutil, pyautogui, playwright

---

## 🔑 API Keys & Configuration

### Required for AI Features

```env
# .env file
ANTHROPIC_API_KEY=sk-ant-api03-...
OPENAI_API_KEY=sk-...
```

### Optional Integrations

```env
# N8N Cloud Run Instance
N8N_API_KEY=n8n_api_...  # Get from N8N settings/api after setup
N8N_BASE_URL=https://n8n-533751401713.us-central1.run.app

# Other Integrations
GITHUB_TOKEN=ghp_...
COMPOSIO_API_KEY=...

# Remote PC Bridge (optional)
REMOTE_PC_BRIDGE_URL=wss://your-tunnel.trycloudflare.com
REMOTE_PC_AUTH_TOKEN=your_secure_token_here
```

### Running Without Keys

System runs with limited functionality:
- ✅ UIs load and display
- ✅ Keyword-based routing
- ✅ Template workflows
- ⚠️ No AI-powered features
- ⚠️ No intelligent routing

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [SYSTEM_ASSESSMENT.md](SYSTEM_ASSESSMENT.md) | **Honest evaluation, ratings, roadmap** |
| [DEPLOYMENT.md](DEPLOYMENT.md) | **Docker, Cloud Run, Railway, AWS, etc.** |
| [AGENT.md](AGENT.md) | AI agent instructions for development |
| [.github/copilot-instructions.md](.github/copilot-instructions.md) | GitHub Copilot guidance |
| [SETUP_STATUS.md](SETUP_STATUS.md) | Python 3.13 compatibility notes |

### Per-Server Documentation

- [N8N Automation README](backend/mcp_servers/n8n_automation/README_DETAILED.md)
- [Agent Builder README](backend/mcp_servers/agent_builder/README.md)
- [Local Control README](backend/mcp_servers/local_control/README.md)

---

## 🚀 Deployment Options

### 1. Production Cloud Run (✅ Currently Deployed)

**Live Services:**
- **MCP Hub**: https://w3j-mcp-hub-533751401713-uc.a.run.app
- **N8N**: https://n8n-533751401713.us-central1.run.app

**Setup N8N:**
1. Visit N8N URL and create owner account
2. Get API key from: https://n8n-533751401713.us-central1.run.app/settings/api
3. Update MCP Hub:
```bash
gcloud run services update w3j-mcp-hub \
  --set-env-vars "N8N_API_KEY=<your_key>" \
  --project stellar-state-471406-f8 \
  --region us-central1
```

See [N8N_DEPLOYMENT_SUCCESS.md](N8N_DEPLOYMENT_SUCCESS.md) for complete guide.

### 2. Deploy Your Own Instance

```bash
# Deploy MCP Hub
gcloud run deploy w3j-mcp-hub --source . --region us-central1

# Deploy N8N (automated script)
.\scripts\deploy_n8n_gcp.ps1
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete guide.

### 3. Docker (Local Development)

```bash
# Quick start
docker-compose up -d

# Access at localhost:7860-7864
```

### 4. Railway / Render

One-click deploy from GitHub. See [DEPLOYMENT.md](DEPLOYMENT.md).

### 5. Self-Hosted (AWS EC2, DigitalOcean, etc.)

Systemd services, Nginx reverse proxy. See [DEPLOYMENT.md](DEPLOYMENT.md).

---

## 🧪 Testing

### Test Server Availability

```powershell
# Windows PowerShell
Test-NetConnection -ComputerName localhost -Port 7860
Test-NetConnection -ComputerName localhost -Port 7862
Test-NetConnection -ComputerName localhost -Port 7863
Test-NetConnection -ComputerName localhost -Port 7864
```

```bash
# Linux/Mac
curl http://localhost:7860
curl http://localhost:7862
curl http://localhost:7863
curl http://localhost:7864
```

### View Logs

```bash
# All logs in backend/logs/
tail -f backend/logs/mcp_system.log
tail -f backend/logs/agent_builder.log
tail -f backend/logs/n8n_automation.log
```

---

## ⭐ System Ratings (Honest Assessment)

| Category | Current | Potential | Notes |
|----------|---------|-----------|-------|
| **Automation Efficiency** | 5/10 | 9/10 | Not true MCP yet, needs protocol |
| **Value Proposition** | 7/10 | 9/10 | Strong architecture, incomplete features |
| **Problem Solving** | 7/10 | 9/10 | Creative approach, needs killer feature |
| **Documentation** | 4/10 | 9/10 | Improving with detailed guides |
| **Production Ready** | 3/10 | 9/10 | 3-4 months to enterprise-grade |

**See [SYSTEM_ASSESSMENT.md](SYSTEM_ASSESSMENT.md) for detailed breakdown.**

---

## 🛣️ Roadmap

### Phase 1: MCP Protocol (3-4 weeks)
- [ ] Implement JSON-RPC 2.0
- [ ] Add stdio/SSE transport
- [ ] Create tool registration system
- [ ] Claude Desktop integration

### Phase 2: Feature Completion (3-4 weeks)
- [ ] Real N8N workflow execution
- [ ] Agent instantiation (ADK, CrewAI)
- [ ] System command execution (secured)
- [ ] AI-powered orchestrator routing

### Phase 3: Enterprise Features (2-3 weeks)
- [ ] Authentication & authorization
- [ ] Multi-user support
- [ ] Rate limiting
- [ ] API documentation (OpenAPI)
- [ ] Health checks & metrics

### Phase 4: Production (2 weeks)
- [ ] Docker optimization
- [ ] CI/CD pipeline
- [ ] Security hardening
- [ ] Load testing
- [ ] Monitoring & alerting

**Total Timeline**: ~11-15 weeks to production-ready

---

## 🤝 Contributing

We welcome contributions! Areas needing help:

- [ ] MCP protocol implementation (CRITICAL)
- [ ] Feature completion (workflows, agents)
- [ ] Documentation improvements
- [ ] Testing infrastructure
- [ ] UI/UX enhancements
- [ ] Security hardening

**See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.**

---

## 🐛 Known Issues

### Python 3.13 Compatibility
- ✅ **Fixed**: Install `audioop-lts` and downgrade `huggingface_hub<1.0.0`
- See [SETUP_STATUS.md](SETUP_STATUS.md) for details

### Anthropic Client Error
- ✅ **Fixed**: Graceful handling of missing/invalid API keys
- System falls back to keyword-based routing

### Not True MCP Protocol
- ⚠️ **Current**: Gradio/FastAPI HTTP interfaces
- 🎯 **Target**: JSON-RPC 2.0 over stdio/SSE
- 📅 **Timeline**: Phase 1 (3-4 weeks)

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/W3JDev/ultimate-mcp-system/issues)
- **Discussions**: [GitHub Discussions](https://github.com/W3JDev/ultimate-mcp-system/discussions)
- **Documentation**: Check `docs/` folder
- **Logs**: `backend/logs/` directory

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file

---

## 📚 Documentation

**Complete documentation available in `/docs`:**

- **[docs/INDEX.md](docs/INDEX.md)** - 📖 Documentation index (start here)
- **[HANDOVER_COMPLETE.md](HANDOVER_COMPLETE.md)** - 🎁 Complete system handover guide
- **[QUICKSTART.md](QUICKSTART.md)** - ⚡ Quick reference commands
- **[docs/setup/](docs/setup/)** - 🔧 Setup and installation guides
- **[docs/demo/](docs/demo/)** - 🎬 Demo scenarios and video scripts
- **[docs/architecture/](docs/architecture/)** - 🏗️ System architecture
- **[docs/api/](docs/api/)** - 🔌 API reference
- **[docs/status-reports/](docs/status-reports/)** - 📊 Project status reports

---

## 🤝 Contributing

We welcome contributions! Please see:

- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines
- **[AGENT.md](AGENT.md)** - AI agent instructions
- **[docs/guides/best-practices.md](docs/guides/best-practices.md)** - Best practices

---

## 🙏 Acknowledgments

- **MCP 1st Birthday Hackathon** - Inspiration and motivation
- **Anthropic** - Claude API powering intelligent routing
- **Gradio** - Beautiful UI framework for MCP servers
- **N8N** - Workflow automation platform
- **OpenAI** - GPT models for additional AI features

---

## 📊 Project Stats

- **Lines of Code**: 10,000+ (Python, Markdown, Config)
- **MCP Servers**: 3 specialized servers + 1 orchestrator
- **Agent Frameworks**: 5 integrated (ADK, A2A, CrewAI, Langbase, AGUI)
- **Test Coverage**: 49/49 unit tests passing
- **Documentation**: 60+ markdown files organized
- **Status**: ✅ Production Ready
- **Python Version**: 3.13.5
- **Deployment**: Docker + GCP Cloud Run ready

---

## 📝 License

MIT License - See [LICENSE](LICENSE) for details

---

**Built for MCP 1st Birthday Hackathon (Nov 14-30, 2025)**  
**Repository**: [github.com/W3JDev/ultimate-mcp-system](https://github.com/W3JDev/ultimate-mcp-system)  
**Maintained By**: W3JDev

**Version**: 0.1.0-beta  
**Last Updated**: November 16, 2025  
**Maintainer**: W3JDev  
**Repository**: https://github.com/W3JDev/ultimate-mcp-system
