# GitHub Copilot Instructions — Ultimate MCP System

- Memory rule: Before complex tasks, recall context with `powershell -File C:\Users\W3jde\.config\memory_tool.ps1 -action recall -query '<keyword>'`; after finishing, save with `-action remember`.

## 🏗 Architecture & Patterns
- **Master Orchestrator**: `backend/main.py` (FastAPI, port 7860) routes to 3 sub-servers: `n8n` (7862), `agent` (7863), `local` (7864).
- **Tool Registry**: Tools are defined in `backend/tools/` using `MCPTool`. **Register new tools in `backend/tools/registry.py`**.
- **Protocol**: Hybrid. REST API (FastAPI) for orchestration; MCP Protocol (JSON-RPC) scaffolding in `backend/mcp_protocol/`.
- **UI**: Gradio interfaces for each server. Follow the "6-tab pattern" (see `agent_builder/server.py`).

## 🛠 Critical Workflows (Windows PowerShell)
- **Start All**: `python launch_all_servers.py` (Starts Orchestrator + 3 Sub-servers).
- **Start Individual**: `python backend/main.py` (Orchestrator only).
- **Test**: `python -m pytest tests -v` (Run from root).
- **Check Ports**: `Test-NetConnection -ComputerName localhost -Port 7860` (repeat for 7862–7864).

## 📝 Coding Conventions
- **Logging**: Use `loguru` with emojis (✅ Success, ⚠️ Warning, ❌ Error, 📦 Init). Logs to `backend/logs/`.
- **Config**: Load secrets via `dotenv`. NEVER commit `.env`.
- **Python**: 3.11+. For 3.13+, install `audioop-lts` and pin `huggingface_hub<1.0.0`.
- **Deployment**: GCP Cloud Run ONLY. Use `gcloud run deploy`.

## 🔌 Integration Points
- **Tools**: `backend/tools/` - Add new tools here. See `backend/tools/README.md`.
- **Agents**: `backend/mcp_servers/agent_builder/` - Supports ADK, A2A, Langbase, AGUI. **CrewAI requires Python 3.10–3.12**.
- **N8N**: `backend/mcp_servers/n8n_automation/` - Workflow automation logic.

## 🐛 Troubleshooting
- **Ports Busy**: `Get-Process | Where-Object {$_.ProcessName -eq 'python'} | Stop-Process`
- **Import Errors**: Always run from repo root.
