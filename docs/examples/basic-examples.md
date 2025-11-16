# 📝 Basic Usage Examples

Simple examples to get started with the Ultimate MCP System.

## Example 1: Create a Simple Workflow

### Goal
Create a workflow that sends an email notification when a new GitHub issue is created.

### Steps

1. **Open N8N Automation MCP**
   ```
   http://localhost:7862
   ```

2. **Navigate to "Workflow Builder" tab**

3. **Enter Description**
   ```
   Send email notification when GitHub issue is created
   ```

4. **Click "Generate Workflow"**

5. **Review Generated Workflow**
   ```json
   {
     "name": "GitHub Issue Email Notification",
     "nodes": [
       {
         "type": "github_webhook",
         "parameters": {
           "events": ["issues.opened"]
         }
       },
       {
         "type": "email",
         "parameters": {
           "to": "team@example.com",
           "subject": "New GitHub Issue: {{$json.issue.title}}"
         }
       }
     ]
   }
   ```

6. **Deploy to N8N** (optional, requires N8N instance)

### Result
Complete N8N workflow ready to use or deploy.

---

## Example 2: Build a Research Agent

### Goal
Create an AI agent that can perform web research.

### Steps

1. **Open Agent Builder MCP**
   ```
   http://localhost:7863
   ```

2. **Navigate to "ADK Agent" tab**

3. **Fill in Agent Details**
   - **Name**: `Research Assistant`
   - **Description**: `Helps with research tasks and information gathering`
   - **Model**: `claude-3-sonnet`
   - **Tools**: `web_search, document_reader`
   - **Temperature**: `0.7`

4. **Click "Create Agent"**

5. **Test Agent**
   - Go to "Management" tab
   - Select your agent
   - Enter test query: "What is quantum computing?"
   - View response

### Result
Configured AI agent ready for research tasks.

---

## Example 3: Get System Information

### Goal
Display current system information (CPU, memory, disk usage).

### Steps

1. **Open Local Control MCP**
   ```
   http://localhost:7864
   ```

2. **Navigate to "System Info" tab**

3. **View Information**
   - CPU usage percentage
   - Memory usage (used/total)
   - Disk usage per partition
   - Platform information
   - Python version

### Result
Real-time system information displayed.

---

## Example 4: Use Master Orchestrator

### Goal
Let the orchestrator route your request automatically.

### Steps

1. **Open Master Orchestrator**
   ```
   http://localhost:7860
   ```

2. **Enter Natural Language Request**
   ```
   Create a workflow that posts to Slack when someone stars my GitHub repo
   ```

3. **Orchestrator Routes to N8N MCP**
   - Analyzes intent: "workflow creation"
   - Routes to N8N Automation MCP
   - Returns workflow generation result

4. **Try Different Requests**
   ```
   Build me an AI agent for customer support
   → Routes to Agent Builder
   
   Show me system resource usage
   → Routes to Local Control
   ```

### Result
Intelligent routing to appropriate MCP based on your request.

---

## Example 5: Execute System Command

### Goal
Execute a safe system command.

### Steps

1. **Open Local Control MCP**
   ```
   http://localhost:7864
   ```

2. **Navigate to "System Commands" tab**

3. **Select Command**
   - Choose "Get System Info" from dropdown
   - Or enter custom command: `ls -la` (Linux/Mac) or `dir` (Windows)

4. **Click "Execute"**

5. **View Output**
   ```
   CPU: 45.2%
   Memory: 62.1%
   Disk: 78.5%
   Platform: Linux
   ```

### Result
Command executed and output displayed safely.

---

## Example 6: Browser Automation

### Goal
Navigate to a website and take a screenshot.

### Steps

1. **Open Local Control MCP**
   ```
   http://localhost:7864
   ```

2. **Navigate to "Browser Automation" tab**

3. **Enter URL**
   ```
   https://example.com
   ```

4. **Click "Navigate"**

5. **Take Screenshot**
   - Click "Take Screenshot" button
   - Screenshot appears below

### Result
Automated browser navigation with screenshot.

---

## Example 7: Create Multiple Agents

### Goal
Create agents for different tasks using different frameworks.

### Steps

1. **Open Agent Builder MCP**

2. **Create Customer Support Agent (ADK)**
   - Name: `Support Bot`
   - Framework: ADK
   - Model: `claude-3-sonnet`
   - Description: `Handles customer inquiries`

3. **Create Research Team (CrewAI)**
   - Name: `Research Team`
   - Framework: CrewAI
   - Agents: `Researcher, Analyst, Writer`
   - Description: `Collaborative research team`

4. **Create RAG Agent (Langbase)**
   - Name: `Document Assistant`
   - Framework: Langbase
   - Tools: `document_search, rag_pipeline`
   - Description: `Answers questions from documents`

### Result
Multiple agents created across different frameworks.

---

## Example 8: Workflow with Conditions

### Goal
Create a workflow with conditional logic.

### Steps

1. **Open N8N Automation MCP**

2. **Enter Description**
   ```
   When GitHub issue is created:
   - If labeled "urgent", send email to team@example.com
   - If labeled "bug", create Jira ticket
   - Otherwise, post to Slack #general
   ```

3. **Generate Workflow**

4. **Review Conditional Logic**
   ```json
   {
     "nodes": [
       {"type": "github_webhook"},
       {"type": "switch", "conditions": [...]},
       {"type": "email", "when": "urgent"},
       {"type": "jira", "when": "bug"},
       {"type": "slack", "when": "default"}
     ]
   }
   ```

### Result
Workflow with conditional branching logic.

---

## Example 9: File Operations

### Goal
Create, read, and manage files.

### Steps

1. **Open Local Control MCP**

2. **Navigate to "File Operations" tab**

3. **Create File**
   - Path: `/tmp/test.txt`
   - Content: `Hello from MCP System`
   - Click "Create File"

4. **Read File**
   - Path: `/tmp/test.txt`
   - Click "Read File"
   - View content

5. **List Directory**
   - Path: `/tmp/`
   - Click "List Directory"
   - See file listing

### Result
File created, read, and listed successfully.

---

## Example 10: Multi-Turn Conversation

### Goal
Have a conversation with context retention.

### Steps

1. **Open Master Orchestrator**

2. **Turn 1**
   ```
   User: Create a workflow for email notifications
   System: [Generates workflow]
   ```

3. **Turn 2** (Context remembered)
   ```
   User: Now add a Slack notification too
   System: [Updates workflow with Slack node]
   ```

4. **Turn 3** (Context still maintained)
   ```
   User: Deploy this to my N8N instance
   System: [Deploys workflow]
   ```

### Result
Multi-turn conversation with context memory.

---

## Tips for Success

### 1. Be Specific
❌ "Create workflow"  
✅ "Create workflow that sends email when GitHub issue is created"

### 2. Use Keywords
Include relevant keywords for better routing:
- Workflow: "workflow", "automation", "n8n"
- Agent: "agent", "AI", "crewai", "adk"
- System: "system", "command", "browser", "file"

### 3. Test Before Deploy
Always test workflows and agents before production use:
- Use "Test" tabs in each MCP
- Verify output is correct
- Check error handling

### 4. Start Simple
Begin with simple examples, then combine:
- Single workflow → Conditional workflow → Multi-step workflow
- Single agent → Multi-agent team
- One command → Command chains

### 5. Use Templates
Start with templates when available:
- N8N MCP has 50+ templates
- Agent Builder has framework examples
- Modify templates for your needs

## Next Steps

- Try [Advanced Examples](advanced-examples.md)
- Read [Integration Examples](integration-examples.md)
- Check [API Documentation](../api/rest-api.md)
- Review [Best Practices](../guides/best-practices.md)

## Common Issues

### "API key not found"
- Set `ANTHROPIC_API_KEY` in `.env` file
- System works without keys but with limited features

### "Server not responding"
- Check server is running: `curl http://localhost:7860`
- View logs: `tail -f backend/logs/*.log`
- Restart servers: `python launch_all_servers.py`

### "Workflow deployment failed"
- Verify N8N instance is running
- Check N8N API key is correct
- Ensure N8N_BASE_URL is set

### "Agent creation failed"
- Check Python version (3.11+ required)
- Install framework dependencies
- Verify API keys are set

## Get Help

- [Troubleshooting Guide](../guides/troubleshooting.md)
- [GitHub Issues](https://github.com/W3JDev/ultimate-mcp-system/issues)
- [Community Discussions](https://github.com/W3JDev/ultimate-mcp-system/discussions)
