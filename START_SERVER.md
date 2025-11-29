# 🚀 W3J MCP Hub - Quick Start Commands

## Windows PowerShell

### 1. Navigate to Project
```powershell
cd C:\Users\W3jde\PROJECTS\MCP\ultimate-mcp-system
```

### 2. Activate Virtual Environment
```powershell
.venv\Scripts\Activate.ps1
```

### 3. Start the Server
```powershell
python backend/main.py
```

## Expected Output
```
✅ Gemini 3 Pro client initialized (Project: stellar-state-471406-f8)
🤖 W3J MCP Hub using Gemini 3 Pro
✅ Registered 17 tools
============================================================
🤖 W3J MCP HUB - Master Orchestrator Running
[WEB] Chat Interface: http://localhost:7860
[DOCS] API Docs: http://localhost:7860/docs
[CREATOR] @W3JDev | https://github.com/W3JDev
============================================================
INFO:     Uvicorn running on http://0.0.0.0:7860 (Press CTRL+C to quit)
```

## Test the API

### Open in Browser
```
http://localhost:7860
```

### Test with PowerShell
```powershell
Invoke-RestMethod -Uri "http://localhost:7860/process" -Method POST -ContentType "application/json" -Body '{"message":"What can you do?"}'
```

### Test with curl
```powershell
curl -X POST http://localhost:7860/process -H "Content-Type: application/json" -d '{\"message\":\"Create an AI agent\"}'
```

---

**Created by @W3JDev** | Powered by Gemini 3 Pro 🚀
