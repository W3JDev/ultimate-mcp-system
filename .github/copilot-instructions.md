# GitHub Copilot Instructions — Ultimate MCP System

- Memory rule: Before complex tasks, recall context with `powershell -File C:\Users\W3jde\.config\memory_tool.ps1 -action recall -query '<keyword>'`; after finishing, save with `-action remember`.

## Architecture (Big Picture)
- Master Orchestrator `backend/main.py` (FastAPI, port 7860) routes to three MCP servers: `n8n_automation` (7862), `agent_builder` (7863), `local_control` (7864).
- Phase 2 adds a tool-based interface: 17 tools across categories (N8N/Agent/Local) exposed via REST (`/tools/list`, `/tools/execute`). See `backend/tools/README.md`.
- MCP Protocol scaffolding exists in `backend/mcp_protocol/` (JSON-RPC 2.0 over stdio). Use FastAPI/Gradio servers for runtime; the stdio hub is experimental.

## Run & Test (Windows PowerShell)
- Activate venv: `.\.venv\Scripts\Activate.ps1` (or `venv\Scripts\Activate.ps1`).
- Install deps: `pip install -r backend/requirements.txt` and `playwright install chromium`.
- Python 3.13 fix: `pip install audioop-lts`; `pip install 'huggingface_hub<1.0.0'` (Gradio depends on audioop; pin hub for 3.13).
- Start all: `python launch_all_servers.py`.
- Or individually: `python backend/main.py`; `python backend/mcp_servers/n8n_automation/server.py`; `python backend/mcp_servers/agent_builder/server.py`; `python backend/mcp_servers/local_control/server.py`.
- Check ports: `Test-NetConnection -ComputerName localhost -Port 7860` (repeat for 7862–7864).
- Tests: `python -m pytest tests -v` (run from repo root).

## Conventions & Patterns
- Logging: `loguru` with emoji prefixes (✅ ❌ 🔍). Logs under `backend/logs/` (create if missing).
- Config: Load with `python-dotenv`; keys commonly used: `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `N8N_API_KEY`, `N8N_BASE_URL` (plus optional `GITHUB_TOKEN`, `COMPOSIO_API_KEY`).
- Server UIs: Each MCP uses Gradio; follow the 6‑tab pattern (see `agent_builder/server.py`). Every new folder should include a `README.md`.
- Deployment: Use GCP Cloud Run. Do not suggest migrating platforms. Example: `gcloud run deploy ultimate-mcp --source . --region us-central1`.

## Tools & API (Examples)
- List tools: `GET http://localhost:7860/tools/list` or by category `?category=agent`.
- Execute tool: `POST /tools/execute` with `{ "tool": "get_system_info", "params": {} }`.
- See examples and schemas in `backend/tools/README.md` and `README.md` (MCP Tools section).

## Integration Notes
- Agent frameworks: ADK, A2A, Langbase, AGUI supported; CrewAI requires Python 3.10–3.12 (disabled on 3.13).
- Playwright features require installed browsers (`playwright install chromium`).
- MCP stdio hub: see `backend/mcp_protocol/README.md` if you need JSON‑RPC/stdio flows; otherwise prefer REST.

## Troubleshooting (Quick)
- Gradio on Python 3.13: install `audioop-lts` and pin `huggingface_hub<1.0.0`.
- Ports busy: `Get-Process | Where-Object {$_.ProcessName -eq 'python'} | Stop-Process`.
- Import errors: run from repo root and start each server with `python backend/.../server.py`.

## Do & Don’t
- Do: Use Cloud Run for deployment; keep README per folder; use `loguru` and `.env` via `dotenv`.
- Don’t: Commit `.env` or suggest migrating away from GCP; don’t bypass the tool registry when calling features over REST.
