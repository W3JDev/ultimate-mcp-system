# 📖 User Guide

Comprehensive guide to using the Ultimate MCP System.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Master Orchestrator](#master-orchestrator)
3. [N8N Automation MCP](#n8n-automation-mcp)
4. [Agent Builder MCP](#agent-builder-mcp)
5. [Local Control MCP](#local-control-mcp)
6. [Best Practices](#best-practices)
7. [Advanced Usage](#advanced-usage)

---

## Getting Started

### Understanding the System

The Ultimate MCP System consists of 4 specialized servers:

```
Master Orchestrator → Routes requests to appropriate MCP
         ↓
    ┌────┼────┬────┐
    │    │    │    │
  N8N  Agent Local Cloud
  MCP   MCP   MCP   MCP
```

**Workflow**:
1. You send a request to Master Orchestrator
2. It analyzes your intent (AI-powered or keyword-based)
3. Routes to the appropriate specialized MCP
4. Returns the response

### Access Points

- **Master Orchestrator**: http://localhost:7860
- **N8N Automation**: http://localhost:7862
- **Agent Builder**: http://localhost:7863
- **Local Control**: http://localhost:7864

---

## Master Orchestrator

### Purpose
Central hub that intelligently routes your requests to the right service.

### Features
- Natural language understanding
- Intelligent routing
- Context memory (remembers conversation)
- Multi-MCP coordination

### Usage

#### Basic Request
```
Input: "Create a workflow for email notifications"
Output: Routes to N8N MCP → Returns workflow
```

#### Follow-up with Context
```
Turn 1: "Create a workflow"
Turn 2: "Now add Slack notification"  # Remembers previous context
Turn 3: "Deploy it"  # Still knows what "it" refers to
```

#### Direct Routing
You can also request specific services:
- "Use N8N to create..."
- "Build an agent with..."
- "Run system command..."

### Tips
- Be specific in your requests
- Use natural language
- Context is maintained across turns
- Works without API keys (keyword fallback)

---

## N8N Automation MCP

### Purpose
Create, test, and deploy N8N workflows from natural language descriptions.

### Interface Tabs

#### 1. Workflow Builder
**Purpose**: Generate workflows from descriptions

**Usage**:
1. Enter description: "Send email when GitHub issue created"
2. Click "Generate Workflow"
3. Review generated JSON
4. Copy or deploy

**Example**:
```
Description: "When Stripe payment succeeds, send confirmation email and create invoice in QuickBooks"

Generated:
- Stripe webhook trigger
- Email node
- QuickBooks API node
- Conditional error handling
```

#### 2. Deploy
**Purpose**: Deploy workflows to N8N instance

**Requirements**:
- N8N instance running
- N8N API key configured

**Usage**:
1. Paste workflow JSON
2. Enter N8N credentials
3. Click "Deploy"
4. View deployment status

#### 3. Templates
**Purpose**: Pre-built workflow templates

**Available Templates**:
- Email notifications
- Slack/Discord integrations
- GitHub automation
- Database sync
- API polling
- And 50+ more

**Usage**:
1. Browse templates
2. Select template
3. Customize parameters
4. Deploy or generate variations

#### 4. Test
**Purpose**: Test workflow logic before deployment

**Usage**:
1. Paste workflow JSON
2. Provide test data
3. Click "Test"
4. View execution results

#### 5. History
**Purpose**: View previously generated workflows

**Features**:
- Search by name/description
- Re-use past workflows
- Export to file

#### 6. Settings
**Purpose**: Configure N8N connection

**Settings**:
- N8N Base URL
- API Key
- Timeout settings
- Default parameters

### Best Practices

#### Writing Good Descriptions
❌ "Create workflow"  
✅ "Create workflow that sends email to team@example.com when GitHub issue is labeled 'urgent'"

#### Include Details
- **Trigger**: What starts the workflow?
- **Actions**: What should happen?
- **Conditions**: Any if/then logic?
- **Error handling**: What if something fails?

#### Example Well-Formed Description
```
When a new user signs up on our website:
1. Add them to Mailchimp mailing list
2. If they selected "premium", create Stripe subscription
3. Send welcome email with appropriate template
4. Log to Airtable database
5. If any step fails, send alert to Slack #alerts channel
```

---

## Agent Builder MCP

### Purpose
Create and manage AI agents across multiple frameworks.

### Supported Frameworks

#### 1. ADK (AI Development Kit)
**Best for**: Production-ready agents

**Features**:
- Tool integration
- Memory management
- Multi-turn conversations
- Production deployment

**Usage**:
1. Go to "ADK Agent" tab
2. Fill in details:
   - Name: "Customer Support"
   - Description: "Handles customer inquiries"
   - Model: "claude-3-sonnet"
   - Tools: ["web_search", "database_query"]
3. Create agent

#### 2. CrewAI
**Best for**: Multi-agent teams

**Features**:
- Multiple specialized agents
- Task delegation
- Collaborative workflows
- Role-based agents

**Usage**:
1. Go to "CrewAI" tab
2. Define team members:
   - Researcher (gathers info)
   - Analyst (processes data)
   - Writer (creates content)
3. Set team goal
4. Create team

**Note**: Requires Python 3.10-3.12

#### 3. A2A (Agent-to-Agent)
**Best for**: Agent communication

**Features**:
- Inter-agent messaging
- Shared state
- Coordination protocols

#### 4. Langbase
**Best for**: RAG (Retrieval-Augmented Generation)

**Features**:
- Document indexing
- Semantic search
- Context-aware responses
- Memory persistence

**Usage**:
1. Go to "Langbase" tab
2. Upload documents or provide URLs
3. Configure RAG pipeline
4. Create agent

#### 5. AGUI
**Best for**: Agent GUIs

**Features**:
- Visual interfaces for agents
- User interaction flows
- Form handling

### Management Tab

**Features**:
- List all agents
- View agent details
- Edit configurations
- Delete agents
- Test agent responses

**Usage**:
```python
# List agents
agents = agent_builder.list_agents()

# Get specific agent
agent = agent_builder.get_agent("agent_123")

# Test agent
response = agent.test("What is quantum computing?")

# Update agent
agent.update(description="Updated description")

# Delete agent
agent.delete()
```

### Agent Configuration

#### Essential Fields
- **Name**: Unique identifier
- **Description**: What the agent does
- **Framework**: ADK, CrewAI, etc.
- **Model**: claude-3-sonnet, gpt-4, etc.

#### Optional Fields
- **Tools**: Available functions
- **Temperature**: Creativity (0-1)
- **Max Tokens**: Response length
- **System Prompt**: Behavior instructions
- **Memory**: Context retention

### Testing Agents

Before deploying, test your agent:
1. Go to Management tab
2. Select agent
3. Enter test input
4. Review response
5. Adjust configuration if needed

---

## Local Control MCP

### Purpose
Automate your local system with natural language commands.

### Interface Tabs

#### 1. System Commands
**Purpose**: Execute system commands safely

**Available Commands**:
- Get system info (CPU, RAM, disk)
- List running processes
- Network status
- Check disk space
- System uptime

**Usage**:
1. Select command from dropdown
2. Or enter custom command
3. Click "Execute"
4. View output

**Safety**: Commands are sandboxed for security

#### 2. Process Manager
**Purpose**: View and control running processes

**Features**:
- List all processes
- Filter by name/PID
- View CPU/memory usage
- Terminate processes (carefully!)

**Usage**:
```
List Processes → See all running processes
Filter by Name → Search for "python"
Select Process → View details
Terminate → Stop selected process
```

#### 3. File Operations
**Purpose**: Manage files and directories

**Operations**:
- **Read**: View file contents
- **Write**: Create/update files
- **Delete**: Remove files
- **List**: View directory contents
- **Move**: Relocate files
- **Copy**: Duplicate files

**Usage**:
1. Select operation
2. Enter path(s)
3. Execute
4. View result

**Example**:
```
Operation: Read
Path: /tmp/test.txt
Result: File contents displayed
```

#### 4. Input Control
**Purpose**: Automate keyboard and mouse

**Features**:
- Type text
- Press key combinations
- Move mouse
- Click coordinates
- Scroll

**Usage**:
```python
# Type text
input_control.type_text("Hello World")

# Press key
input_control.press_key("Enter")

# Mouse click
input_control.click(x=100, y=200)
```

**Warning**: Use carefully as it controls actual input devices

#### 5. Browser Automation
**Purpose**: Automate browser tasks with Playwright

**Features**:
- Navigate to URLs
- Take screenshots
- Fill forms
- Click elements
- Extract data
- Run JavaScript

**Usage**:
1. Enter URL
2. Click "Navigate"
3. Perform actions (click, type, etc.)
4. Take screenshot
5. View result

**Example**:
```
1. Navigate to https://example.com
2. Take Screenshot → View page
3. Fill Form → Enter data
4. Click Button → Submit
5. Extract Result → Get response text
```

#### 6. System Info
**Purpose**: Real-time system monitoring

**Displays**:
- CPU usage per core
- Memory usage (used/available)
- Disk usage per partition
- Network interfaces
- Python version
- OS information

**Updates**: Real-time (refreshes every few seconds)

### Safety Features

#### Command Whitelisting
Certain dangerous commands are blocked:
- `rm -rf /`
- `format C:`
- System file modifications

#### Sandboxing
Commands run in restricted environment:
- Limited file system access
- No sudo/admin by default
- Logged for audit

#### Confirmation
Destructive operations require confirmation:
- Process termination
- File deletion
- System modifications

---

## Best Practices

### 1. API Keys

**Store Securely**:
```bash
# .env file (not committed to git)
ANTHROPIC_API_KEY=sk-ant-api03-xxx
```

**Rotate Regularly**:
- Every 90 days for production
- Immediately if compromised

### 2. Workflow Design

**Start Simple**:
```
Bad: "Complex multi-step conditional workflow with error handling and retries"
Good: "Send email when webhook received" (then iterate)
```

**Test Before Deploy**:
1. Generate workflow
2. Test with sample data
3. Deploy to staging
4. Monitor for errors
5. Deploy to production

### 3. Agent Configuration

**Choose Right Framework**:
- Single task → ADK
- Team collaboration → CrewAI
- Document Q&A → Langbase
- Visual interface → AGUI

**Set Appropriate Temperature**:
- 0.0-0.3: Factual, consistent (support, data)
- 0.4-0.7: Balanced (general purpose)
- 0.8-1.0: Creative (writing, brainstorming)

### 4. System Automation

**Safety First**:
```bash
# Good: Safe, reversible
ls -la
cat file.txt
df -h

# Dangerous: Require confirmation
rm important_file.txt
kill <process>
```

**Log Everything**:
- All commands executed
- Results and errors
- Timestamp each action

### 5. Resource Management

**Monitor Usage**:
```bash
# Check system resources regularly
CPU: < 80% sustained
Memory: < 90% total
Disk: < 90% capacity
```

**Clean Up**:
- Delete old logs
- Remove unused agents
- Clear workflow history

### 6. Error Handling

**Graceful Degradation**:
- Works without API keys (limited)
- Fallback to templates
- Keyword-based routing backup

**Logging**:
```python
# All errors logged
logger.error(f"Failed to generate workflow: {e}")
```

---

## Advanced Usage

### Chaining Operations

**Example**: Create agent, then workflow, then deploy
```
1. Create agent for email analysis
2. Generate workflow using that agent
3. Deploy workflow to production
4. Monitor execution
```

### Custom Templates

Create your own workflow templates:
1. Generate workflow
2. Save to templates
3. Parameterize variables
4. Reuse across projects

### Batch Operations

Process multiple items:
```python
# Create multiple agents
for role in ["support", "sales", "research"]:
    agent_builder.create_agent(
        name=f"{role}_agent",
        description=f"Handles {role} tasks"
    )
```

### Integration with External Tools

Connect to your existing stack:
- **Slack**: Notifications
- **GitHub**: CI/CD triggers
- **Jira**: Task management
- **Airtable**: Data storage

### API Access

Use REST API for programmatic access:
```python
import requests

# Create workflow via API
response = requests.post(
    "http://localhost:7862/api/workflow/generate",
    json={"description": "Email workflow"}
)
workflow = response.json()
```

---

## Next Steps

- Try [Basic Examples](../examples/basic-examples.md)
- Explore [Advanced Examples](../examples/advanced-examples.md)
- Read [API Documentation](../api/rest-api.md)
- Check [Troubleshooting Guide](troubleshooting.md)

## Need Help?

- [FAQ](faq.md)
- [GitHub Issues](https://github.com/W3JDev/ultimate-mcp-system/issues)
- [Community Discussions](https://github.com/W3JDev/ultimate-mcp-system/discussions)
