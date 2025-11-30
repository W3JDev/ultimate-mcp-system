# 🤖 W3J MCP Hub

**Multi-MCP Orchestration Platform for N8N · AI Agents · System Control**

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-14%20passing-brightgreen.svg)]()

> Production-ready orchestrator coordinating 3 MCP servers via unified FastAPI interface

---

## Quick Start

```powershell
git clone https://github.com/W3JDev/ultimate-mcp-system.git
cd ultimate-mcp-system
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt

python launch_all_servers.py

# Access: http://localhost:7860 (Orchestrator)
#         http://localhost:7862 (N8N Automation)
#         http://localhost:7863 (Agent Builder)
#         http://localhost:7864 (Local Control)
```

**Python 3.13**: See [QUICKSTART.md](QUICKSTART.md#python-313-fix) for compatibility fix

---

## What It Does

**Master Orchestrator** routes requests to 3 specialized MCP servers:

1. **N8N Automation** - AI workflow generation & deployment
2. **Agent Builder** - 5 frameworks (ADK, CrewAI, A2A, Langbase, AGUI)
3. **Local Control** - System automation, files, browser

**Routing**: Gemini 3 Pro intent analysis with keyword fallback

---

## Architecture

```
FastAPI (7860) → Tool Registry → Lazy-loaded servers
                                  ├─ N8N (7862)
                                  ├─ Agent (7863)
                                  └─ Local (7864)
```

**Stack**: FastAPI, Gradio, Claude API, Gemini 3 Pro, Loguru

---

## Docs

- **[QUICKSTART.md](QUICKSTART.md)** - Setup & troubleshooting
- **[PROJECT_STATUS.md](PROJECT_STATUS.md)** - Verified capabilities (code-backed)
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute
- **[.github/copilot-instructions.md](.github/copilot-instructions.md)** - Developer guide

---

## Testing

```powershell
python -m pytest tests/unit -v          # 14 unit tests
python -m pytest tests --cov=backend    # With coverage
```

---

## Requirements

- Python 3.11+ (3.13 supported)
- Windows PowerShell or equivalent
- Optional: Anthropic/OpenAI keys, N8N instance

---

## Current Status

✅ Core orchestrator operational  
✅ 3 MCP servers (Gradio UIs)  
✅ 17+ registered tools  
✅ 5 agent frameworks  
✅ Gemini 3 Pro routing  

⚠️ In-memory storage only  
⚠️ Single-user (no auth)  
⚠️ 14 tests (needs more)

**Full analysis**: [PROJECT_STATUS.md](PROJECT_STATUS.md)

---

## License

MIT © [@W3JDev](https://github.com/W3JDev) | Created for MCP 1st Birthday Hackathon 2025
