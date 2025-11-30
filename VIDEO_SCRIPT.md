# VIDEO RECORDING SCRIPT - 5 Minutes Max

## Setup Before Recording

1. **Open Windows:**
   - Browser: http://localhost:7863 (Agent Builder UI)
   - Terminal: PowerShell in project root
   - Browser Tab 2: GitHub repo page

2. **Check Services:**
   ```powershell
   docker ps  # Verify agent-builder-mcp running
   ```

3. **Have Ready:**
   - Test message prepared
   - N8N credentials visible
   - Database query commands ready

---

## Recording Timeline (5 minutes)

### 0:00-0:30 - Introduction
**Screen**: GitHub README  
**Script**:
> "Hi, I'm presenting W3J MCP Hub for the Anthropic Build with MCP Hackathon.  
> This is a production-ready multi-MCP orchestration platform with real AI execution,  
> workflow deployment, and 200+ tool integrations. Let me show you what makes this different."

**Actions**:
- Show GitHub repo structure
- Highlight: 4 servers, 5 frameworks, Docker deployment

---

### 0:30-1:30 - Create Agent (LIVE)
**Screen**: Agent Builder UI - ADK Agent tab  
**Script**:
> "First, I'll create an AI agent using Anthropic's ADK framework with Gemini 3 Pro.  
> Watch - this is real code, not a demo."

**Actions**:
1. Fill form LIVE:
   ```
   Name: DemoAgent
   Tools: email, slack, code_generation
   Model: gemini-2.0-flash-exp
   System Prompt: "You are a helpful assistant with email, Slack, and code generation capabilities."
   ```
2. Click "Create ADK Agent"
3. **Show JSON response** - highlight agent_id

---

### 1:30-2:30 - Test Execution (REAL API CALL)
**Screen**: Test & Deploy tab  
**Script**:
> "Now I'll test this agent with a REAL Gemini API call - no mocks, no simulations.  
> This is live inference happening right now."

**Actions**:
1. Enter:
   ```
   Agent ID: adk_demoagent
   Message: "Write a Python function that sends an email notification when a Slack message contains 'urgent'"
   ```
2. Click "Test Agent"
3. **Wait for response** (should be 2-3 seconds)
4. **Highlight**:
   - Response text (real Gemini output)
   - Model used
   - Execution time

---

### 2:30-3:15 - Deploy to N8N
**Screen**: Still in Test & Deploy tab  
**Script**:
> "Great! Now let's deploy this as a live workflow. With one click, this becomes  
> a production endpoint that anyone can call via webhook."

**Actions**:
1. Scroll to Deploy section
2. Enter agent ID: adk_demoagent
3. Click "Deploy to N8N"
4. **Show result**:
   - Workflow ID
   - Webhook URL
5. **Explain**: "Now this agent is live - any HTTP POST to that URL runs the agent"

---

### 3:15-4:00 - Orchestrator Magic
**Screen**: Orchestrator Integration section  
**Script**:
> "Here's where it gets powerful. Our master orchestrator can automate  
> the entire workflow with natural language. Watch this."

**Actions**:
1. Enter:
   ```
   Agent ID: adk_demoagent
   Command: "Run a complete test suite, deploy to N8N, verify the webhook, and give me a summary"
   ```
2. Click "Run Orchestrator"
3. **Show output** - orchestrator coordinating multiple services

---

### 4:00-4:30 - Database & Composio
**Screen**: Terminal + Composio tab  
**Script**:
> "Everything is persisted in SQLite. Let me show you the database."

**Actions**:
1. Terminal:
   ```powershell
   cd backend/mcp_servers/agent_builder
   python -c "from agent_database import AgentDatabase; import json; db = AgentDatabase(); print(json.dumps(db.list_agents(), indent=2))"
   ```
2. Show agent record with created_at, deployed, etc.
3. Quick switch to Composio tab
4. Show: "200+ tools available - Gmail, Slack, GitHub, Twitter..."

---

### 4:30-5:00 - Closing
**Screen**: GitHub + Terminal  
**Script**:
> "W3J MCP Hub isn't a prototype - it's production-ready with Docker deployment,  
> real AI integrations, persistent storage, and E2E testing. We've built the  
> orchestration layer that the MCP ecosystem needs. Thanks for watching!"

**Actions**:
1. Show GitHub: Stars, README, code structure
2. Terminal: `docker ps` - show running container
3. Show submission files: HACKATHON_SUBMISSION.md

---

## Recording Tips

1. **Use OBS Studio** or **Screen Recorder**
   - 1080p minimum resolution
   - 60fps if possible
   - Include audio (clear mic)

2. **Practice Once** before final recording
   - Dry run the commands
   - Test agent creation (pick different name)
   - Verify N8N connection

3. **Keep It Flowing**
   - Don't pause for loading (it's okay to see spinners)
   - If something fails, explain it briefly and move on
   - Enthusiasm is key!

4. **Backup Plan**
   - If agent creation fails → switch to pre-created agent
   - If N8N is down → explain the code and show expected output
   - If database query fails → show the database file exists

---

## Post-Recording

1. **Edit** (if needed):
   - Cut any long pauses
   - Add title card: "W3J MCP Hub - Anthropic MCP Hackathon"
   - Add end card with GitHub URL

2. **Upload**:
   - YouTube (unlisted or public)
   - Loom
   - Vimeo
   
3. **Add URL** to:
   - HACKATHON_SUBMISSION.md
   - Submission form

---

## Fallback: Screenshot Deck

If video recording fails, create slides with:

1. Architecture diagram
2. Agent creation form (filled)
3. Test execution results (JSON)
4. N8N deployment result
5. Database query output
6. GitHub repo structure

Use PowerPoint/Google Slides, export as PDF.

---

## Key Message

**W3J MCP Hub = Real orchestration + Real execution + Real deployment**

Not just another MCP server - it's the platform that coordinates them all.
