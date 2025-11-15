# 🔧 Backend - Ultimate MCP System

**Core MCP servers and orchestration logic**

## Structure

```
backend/
├── main.py              ← Entry point
├── orchestrator.py      ← Routes requests to MCPs
├── memory.py           ← State management
├── mcp_servers/        ← Individual MCP implementations
├── utils/              ← Helper functions
└── requirements.txt    ← Dependencies
```

## Run Locally

```bash
cd backend
python main.py
```

Access at: http://localhost:7860

## Deploy to GCP

```bash
gcloud run deploy ultimate-mcp-system --source . --region us-central1
```

See [AGENT.md](../AGENT.md) for complete setup instructions.
