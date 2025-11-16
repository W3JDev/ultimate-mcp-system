# 🔌 REST API Documentation

Complete REST API reference for the Ultimate MCP System.

## Base URLs

- **Master Orchestrator**: `http://localhost:7860`
- **N8N Automation MCP**: `http://localhost:7862`
- **Agent Builder MCP**: `http://localhost:7863`
- **Local Control MCP**: `http://localhost:7864`

## Authentication

Currently, the system does not require authentication for local development. For production deployments, implement authentication at the reverse proxy level (Nginx, Traefik, etc.).

## Master Orchestrator API

### Health Check

```http
GET /health
```

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-16T12:00:00Z",
  "version": "0.1.0-beta"
}
```

### Process Request

```http
POST /api/process
Content-Type: application/json
```

**Request Body**:
```json
{
  "message": "Create a workflow for email notifications",
  "context": {}
}
```

**Response**:
```json
{
  "response": "Routing to N8N Automation MCP...",
  "server": "n8n",
  "timestamp": "2025-11-16T12:00:00Z"
}
```

### Get Memory Context

```http
GET /api/memory
```

**Response**:
```json
{
  "context": [
    {
      "role": "user",
      "content": "Create a workflow",
      "timestamp": "2025-11-16T12:00:00Z"
    },
    {
      "role": "assistant",
      "content": "Workflow created successfully",
      "timestamp": "2025-11-16T12:00:01Z"
    }
  ]
}
```

## N8N Automation MCP API

### Generate Workflow

```http
POST /api/workflow/generate
Content-Type: application/json
```

**Request Body**:
```json
{
  "description": "Send email when GitHub issue is created",
  "requirements": {
    "trigger": "github_webhook",
    "actions": ["send_email"],
    "conditions": []
  }
}
```

**Response**:
```json
{
  "workflow": {
    "name": "GitHub Issue Email Notification",
    "nodes": [...],
    "connections": {...}
  },
  "status": "generated",
  "timestamp": "2025-11-16T12:00:00Z"
}
```

### Deploy Workflow

```http
POST /api/workflow/deploy
Content-Type: application/json
```

**Request Body**:
```json
{
  "workflow": {...},
  "n8n_url": "http://localhost:5678",
  "api_key": "your_n8n_api_key"
}
```

**Response**:
```json
{
  "status": "deployed",
  "workflow_id": "abc123",
  "url": "http://localhost:5678/workflow/abc123"
}
```

### Test Workflow

```http
POST /api/workflow/test
Content-Type: application/json
```

**Request Body**:
```json
{
  "workflow": {...},
  "test_data": {
    "trigger_payload": {...}
  }
}
```

**Response**:
```json
{
  "status": "success",
  "results": [...],
  "execution_time_ms": 123
}
```

## Agent Builder MCP API

### Create Agent

```http
POST /api/agent/create
Content-Type: application/json
```

**Request Body**:
```json
{
  "name": "Research Assistant",
  "description": "Helps with research tasks",
  "framework": "adk",
  "config": {
    "model": "claude-3-sonnet",
    "tools": ["web_search", "document_reader"],
    "temperature": 0.7
  }
}
```

**Response**:
```json
{
  "agent_id": "agent_123",
  "name": "Research Assistant",
  "status": "created",
  "timestamp": "2025-11-16T12:00:00Z"
}
```

### List Agents

```http
GET /api/agents
```

**Response**:
```json
{
  "agents": [
    {
      "id": "agent_123",
      "name": "Research Assistant",
      "framework": "adk",
      "created_at": "2025-11-16T12:00:00Z"
    }
  ]
}
```

### Get Agent Details

```http
GET /api/agent/{agent_id}
```

**Response**:
```json
{
  "id": "agent_123",
  "name": "Research Assistant",
  "description": "Helps with research tasks",
  "framework": "adk",
  "config": {...},
  "created_at": "2025-11-16T12:00:00Z"
}
```

### Update Agent

```http
PUT /api/agent/{agent_id}
Content-Type: application/json
```

**Request Body**:
```json
{
  "description": "Updated description",
  "config": {...}
}
```

**Response**:
```json
{
  "status": "updated",
  "agent_id": "agent_123",
  "timestamp": "2025-11-16T12:00:00Z"
}
```

### Delete Agent

```http
DELETE /api/agent/{agent_id}
```

**Response**:
```json
{
  "status": "deleted",
  "agent_id": "agent_123"
}
```

### Test Agent

```http
POST /api/agent/{agent_id}/test
Content-Type: application/json
```

**Request Body**:
```json
{
  "input": "What is quantum computing?"
}
```

**Response**:
```json
{
  "output": "Quantum computing is...",
  "execution_time_ms": 234,
  "tokens_used": 150
}
```

## Local Control MCP API

### Execute System Command

```http
POST /api/system/command
Content-Type: application/json
```

**Request Body**:
```json
{
  "command": "get_system_info"
}
```

**Response**:
```json
{
  "result": {
    "cpu_percent": 45.2,
    "memory_percent": 62.1,
    "disk_percent": 78.5,
    "platform": "Linux"
  },
  "status": "success"
}
```

### List Processes

```http
GET /api/system/processes
```

**Response**:
```json
{
  "processes": [
    {
      "pid": 1234,
      "name": "python",
      "cpu_percent": 5.2,
      "memory_percent": 2.1
    }
  ]
}
```

### Control Process

```http
POST /api/system/process/{pid}/action
Content-Type: application/json
```

**Request Body**:
```json
{
  "action": "terminate"
}
```

**Response**:
```json
{
  "status": "terminated",
  "pid": 1234
}
```

### Execute Browser Action

```http
POST /api/browser/action
Content-Type: application/json
```

**Request Body**:
```json
{
  "action": "navigate",
  "url": "https://example.com"
}
```

**Response**:
```json
{
  "status": "success",
  "screenshot": "base64_encoded_image"
}
```

### File Operations

```http
POST /api/file/operation
Content-Type: application/json
```

**Request Body**:
```json
{
  "operation": "read",
  "path": "/path/to/file.txt"
}
```

**Response**:
```json
{
  "content": "file contents...",
  "size_bytes": 1024,
  "modified": "2025-11-16T12:00:00Z"
}
```

## Error Responses

### Standard Error Format

All errors follow this format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {...}
  },
  "timestamp": "2025-11-16T12:00:00Z"
}
```

### Common Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `INVALID_REQUEST` | 400 | Malformed request body |
| `UNAUTHORIZED` | 401 | Missing or invalid API key |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `NOT_FOUND` | 404 | Resource not found |
| `RATE_LIMIT` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Server error |
| `SERVICE_UNAVAILABLE` | 503 | MCP server not responding |

### Example Error Response

```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Missing required field: 'description'",
    "details": {
      "field": "description",
      "required": true
    }
  },
  "timestamp": "2025-11-16T12:00:00Z"
}
```

## Rate Limiting

Currently not implemented. Recommended for production:

- **Rate Limit**: 100 requests per minute per IP
- **Burst**: 20 requests
- **Headers**:
  - `X-RateLimit-Limit`: Maximum requests
  - `X-RateLimit-Remaining`: Remaining requests
  - `X-RateLimit-Reset`: Reset timestamp

## Webhooks

Future feature - webhook support for:
- Workflow completion notifications
- Agent execution results
- System event alerts

## WebSocket API

Future feature - real-time communication:
- Live log streaming
- Real-time agent responses
- System monitoring updates

## Code Examples

### Python

```python
import requests

# Master Orchestrator
response = requests.post(
    "http://localhost:7860/api/process",
    json={
        "message": "Create a workflow",
        "context": {}
    }
)
print(response.json())

# Agent Builder
response = requests.post(
    "http://localhost:7863/api/agent/create",
    json={
        "name": "Test Agent",
        "framework": "adk",
        "config": {"model": "claude-3-sonnet"}
    }
)
print(response.json())
```

### JavaScript

```javascript
// Master Orchestrator
fetch('http://localhost:7860/api/process', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    message: 'Create a workflow',
    context: {}
  })
})
.then(res => res.json())
.then(data => console.log(data));

// Agent Builder
fetch('http://localhost:7863/api/agent/create', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    name: 'Test Agent',
    framework: 'adk',
    config: {model: 'claude-3-sonnet'}
  })
})
.then(res => res.json())
.then(data => console.log(data));
```

### cURL

```bash
# Master Orchestrator
curl -X POST http://localhost:7860/api/process \
  -H "Content-Type: application/json" \
  -d '{"message": "Create a workflow", "context": {}}'

# Agent Builder
curl -X POST http://localhost:7863/api/agent/create \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Agent", "framework": "adk", "config": {"model": "claude-3-sonnet"}}'
```

## OpenAPI Specification

Full OpenAPI 3.0 specification available at:
- Master: `http://localhost:7860/openapi.json`
- N8N MCP: `http://localhost:7862/openapi.json`
- Agent MCP: `http://localhost:7863/openapi.json`
- Local MCP: `http://localhost:7864/openapi.json`

## Next Steps

- [Python API Reference](python-api.md)
- [MCP Protocol Documentation](mcp-protocol.md)
- [Integration Examples](../examples/integration-examples.md)
- [API Security Best Practices](../guides/security.md)
