# 🔌 N8N Automation MCP Server

**AI-Powered Workflow Automation Interface**

[![Status](https://img.shields.io/badge/Status-Beta-yellow)]()
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)]()
[![Port](https://img.shields.io/badge/Port-7862-green)]()

---

## 📋 Overview

The N8N Automation MCP provides AI-powered workflow creation, testing, and deployment for N8N. Build complex automation workflows using natural language descriptions.

### Key Features

- ✅ **Natural Language Workflows**: Describe workflows in plain English
- ✅ **AI-Generated JSON**: Claude generates N8N-compatible workflow JSON
- ✅ **Workflow Testing**: Simulate workflow execution before deployment
- ✅ **N8N Integration**: Deploy directly to N8N instance
- ✅ **Template Library**: Pre-built workflow templates
- ✅ **Fallback Mode**: Template-based workflows when AI unavailable

---

## 🚀 Quick Start

### Prerequisites

```bash
# Python 3.11+ required (Python 3.13 supported)
pip install audioop-lts gradio loguru anthropic requests
```

### Configuration

```env
# .env file
N8N_API_KEY=your_n8n_api_key
N8N_BASE_URL=http://localhost:5678
ANTHROPIC_API_KEY=sk-ant-...  # Optional for AI generation
```

### Run Server

```bash
cd backend/mcp_servers/n8n_automation
python server.py
```

Server starts on: **http://localhost:7862**

---

## 🎨 User Interface

### Tab 1: Workflow Builder
**Purpose**: Generate N8N workflows from natural language

**Inputs:**
- Workflow Description (natural language)

**Outputs:**
- Generated N8N workflow JSON
- Workflow preview
- Download workflow file

**Example:**
```
"Create a workflow that monitors GitHub issues, 
sends a Slack notification when a new issue is created, 
and adds the issue to a Google Sheet"
```

**Generated Output:**
```json
{
  "name": "GitHub to Slack & Sheets",
  "nodes": [
    {
      "id": "github_trigger",
      "type": "n8n-nodes-base.githubTrigger",
      "parameters": {...}
    },
    {
      "id": "slack_notify",
      "type": "n8n-nodes-base.slack",
      "parameters": {...}
    },
    {
      "id": "google_sheet",
      "type": "n8n-nodes-base.googleSheets",
      "parameters": {...}
    }
  ],
  "connections": {...}
}
```

### Tab 2: Workflow Tester
**Purpose**: Test workflows before deployment

**Inputs:**
- Workflow JSON
- Test Data (optional)

**Outputs:**
- Execution results
- Node-by-node output
- Error messages (if any)

### Tab 3: Deploy to N8N
**Purpose**: Deploy workflows to N8N instance

**Requirements:**
- N8N API Key configured
- N8N instance accessible

**Inputs:**
- Workflow JSON
- Workflow Name
- Target N8N URL

**Outputs:**
- Deployment status
- Workflow ID in N8N
- Activation link

---

## 🏗️ Architecture

```
N8NAutomationMCP
├── workflow_builder.py
│   ├── WorkflowBuilder.build_from_description()
│   ├── _get_system_prompt()
│   ├── _extract_json()
│   └── _create_template_workflow()
│
├── workflow_tester.py
│   ├── WorkflowTester.test_workflow()
│   ├── _simulate_execution()
│   └── _validate_nodes()
│
├── deployer.py
│   ├── N8NDeployer.deploy()
│   ├── _authenticate()
│   └── _activate_workflow()
│
└── server.py
    └── N8NAutomationMCP.process()
```

---

## 📡 API Endpoints

### Generate Workflow
```python
POST /workflow/generate
{
  "description": "Send email when form is submitted"
}

Response: {
  "workflow": {...},  # N8N JSON
  "status": "success"
}
```

### Test Workflow
```python
POST /workflow/test
{
  "workflow": {...},  # N8N JSON
  "test_data": {...}
}

Response: {
  "results": [...],
  "status": "success"
}
```

### Deploy Workflow
```python
POST /workflow/deploy
{
  "workflow": {...},
  "name": "MyWorkflow",
  "activate": true
}

Response: {
  "workflow_id": "abc123",
  "url": "http://n8n.local/workflow/abc123",
  "status": "deployed"
}
```

---

## 🔧 Configuration

### N8N Setup

**1. Enable N8N API:**
```bash
# In N8N settings
API Access: Enabled
Generate API Key: Copy key to .env
```

**2. Configure URL:**
```env
N8N_BASE_URL=http://localhost:5678  # Local
# OR
N8N_BASE_URL=https://your-n8n.cloud  # Cloud
```

**3. Test Connection:**
```bash
curl -H "X-N8N-API-KEY: your_key" \
  http://localhost:5678/api/v1/workflows
```

### AI Configuration

**With Anthropic API:**
```env
ANTHROPIC_API_KEY=sk-ant-api03-...
```
- ✅ AI-generated workflows
- ✅ Complex workflow logic
- ✅ Natural language understanding

**Without API Key:**
- ⚠️ Template-based workflows only
- ⚠️ Limited customization
- ✅ Basic workflow generation

---

## 📚 Workflow Templates

### 1. GitHub to Slack
```yaml
Trigger: GitHub webhook (new issue)
Action: Send Slack message
Nodes: 2
```

### 2. Email to Sheet
```yaml
Trigger: Email received
Transform: Extract data
Action: Add to Google Sheet
Nodes: 3
```

### 3. RSS to Twitter
```yaml
Trigger: RSS feed check (schedule)
Filter: New items only
Action: Post to Twitter
Nodes: 3
```

### 4. Form to CRM
```yaml
Trigger: Webhook (form submission)
Transform: Map fields
Action: Create CRM record
Nodes: 3
```

---

## 🧪 Testing Workflows

### Local Testing (Without N8N)
```python
from workflow_tester import WorkflowTester

tester = WorkflowTester()
results = tester.test_workflow(workflow_json, test_data)

print(results["execution_summary"])
print(results["node_outputs"])
```

### Integration Testing (With N8N)
```bash
# Deploy to test N8N instance
N8N_BASE_URL=http://test.n8n.local python deployer.py

# Execute workflow via API
curl -X POST http://test.n8n.local/api/v1/workflows/abc123/execute
```

---

## 🔒 Security

### API Key Management
```bash
# NEVER commit API keys
echo ".env" >> .gitignore

# Use environment variables
export N8N_API_KEY=your_key

# Or use secrets manager
aws secretsmanager get-secret-value --secret-id n8n-api-key
```

### N8N Permissions
- ✅ Use read-only API keys for testing
- ✅ Separate keys for dev/staging/prod
- ⚠️ Limit workflow execution permissions
- ⚠️ Validate all user inputs before deployment

---

## 🐛 Troubleshooting

### Issue: "No valid Anthropic API key"
**Symptom**: Workflows use templates instead of AI generation
**Solution**: Add `ANTHROPIC_API_KEY` to `.env` file

### Issue: "Failed to connect to N8N"
**Check:**
```bash
# Test N8N is running
curl http://localhost:5678

# Test API endpoint
curl -H "X-N8N-API-KEY: $N8N_API_KEY" \
  $N8N_BASE_URL/api/v1/workflows
```

### Issue: "Workflow deployment failed"
**Common Causes:**
- Invalid N8N_API_KEY
- N8N instance not accessible
- Workflow JSON invalid
- Missing node credentials in N8N

**Solution:**
```python
# Validate workflow before deploy
from workflow_tester import WorkflowTester
tester = WorkflowTester()
validation = tester.validate_workflow(workflow_json)
if validation["valid"]:
    deployer.deploy(workflow_json)
```

---

## 📊 Monitoring

### Workflow Logs
```bash
# MCP Server logs
tail -f backend/logs/n8n_automation.log

# N8N execution logs
# In N8N UI: Executions tab
```

### Health Check
```python
GET /health
Response: {
  "status": "healthy",
  "n8n_connected": true,
  "ai_available": true,
  "version": "0.1.0"
}
```

---

## 🛣️ Roadmap

### Current (v0.1 - Beta)
- [x] AI workflow generation
- [x] Template fallback
- [x] Basic workflow testing
- [x] N8N deployment API

### Next (v0.2)
- [ ] Visual workflow editor
- [ ] More templates (20+)
- [ ] Workflow versioning
- [ ] Schedule management
- [ ] Error handling improvements

### Future (v0.3+)
- [ ] Multi-tenant support
- [ ] Workflow marketplace
- [ ] Advanced testing (mocks, fixtures)
- [ ] Performance optimization
- [ ] Real-time execution monitoring
- [ ] Webhook management

---

## 📞 Support

- **Issues**: GitHub Issues
- **Documentation**: [Full docs](../../docs/)
- **N8N Docs**: https://docs.n8n.io
- **Logs**: `backend/logs/n8n_automation.log`

---

## 📄 License

MIT License - See [LICENSE](../../../LICENSE)

---

**Version**: 0.1.0-beta  
**Last Updated**: November 16, 2025  
**Maintainer**: W3JDev
