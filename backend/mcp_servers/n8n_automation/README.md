# 🔄 N8N Automation MCP

**Build, test, validate & deploy N8N workflows via natural language**

## What This Does

This MCP server lets AI create complete N8N workflows from descriptions:
- **Workflow Builder**: Generate N8N workflow JSON from text
- **Workflow Tester**: Run tests with validation
- **Output Validator**: Verify output formats
- **Deployer**: Deploy to N8N instance

## Example Usage

```python
from n8n_automation import N8NAutomationMCP

mcp = N8NAutomationMCP()

# Create workflow from description
workflow = mcp.create_workflow(
    "When a GitHub PR is merged, send WhatsApp to team and update Notion"
)

# Test workflow
test_result = mcp.test_workflow(workflow, test_data={...})

# Validate outputs
validation = mcp.validate_outputs(test_result)

# Deploy
deployment = mcp.deploy_workflow(workflow)
```

## Files

- `server.py` - Main MCP server (Gradio interface)
- `workflow_builder.py` - AI-powered workflow generator
- `workflow_tester.py` - Test runner with validation
- `deployer.py` - N8N deployment manager
- `templates/` - Pre-built workflow templates

## Setup

```bash
# N8N API credentials in .env
N8N_API_KEY=your_key
N8N_BASE_URL=http://localhost:5678/
```

## Integration

Called by Master Orchestrator when user requests workflow automation.
