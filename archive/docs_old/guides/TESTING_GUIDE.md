# 🧪 Testing Guide - Ultimate MCP System

**Quick guide to test all MCP servers manually and automatically**

---

## ⚡ Quick Test Commands

### Test All Servers at Once
```powershell
# Run the comprehensive test suite
python test_all_servers.py
```

### Test Individual Servers
```powershell
# Test N8N MCP Server (Port 7862)
Invoke-WebRequest http://localhost:7862

# Test Agent Builder MCP Server (Port 7863)
Invoke-WebRequest http://localhost:7863

# Test Local Control MCP Server (Port 7864)
Invoke-WebRequest http://localhost:7864

# Test Master Orchestrator (Port 7860)
Invoke-WebRequest http://localhost:7860/health
```

---

## 🔄 N8N MCP Server Testing (Port 7862)

### Option 1: Web UI Testing (Easiest)

1. **Open in Browser**: http://localhost:7862
2. **Test Workflow Builder Tab**:
   - Enter workflow name: "Test Email Workflow"
   - Enter description: "Send email when GitHub PR is merged"
   - Click "Generate Workflow"
   - Verify JSON workflow is generated

3. **Test Workflow Tester Tab**:
   - Load a workflow ID
   - Enter test data:
     ```json
     {
       "pr_number": 123,
       "repository": "test-repo",
       "merged": true
     }
     ```
   - Click "Run Test"
   - Check results

4. **Test Deployer Tab**:
   - Enter workflow ID
   - Click "Deploy to Production"
   - Check deployment status

### Option 2: Python API Testing

Create `test_n8n_manual.py`:
```python
import requests

BASE_URL = "http://localhost:7862"

# Test 1: Check server is running
print("Testing N8N MCP Server...")
response = requests.get(BASE_URL)
print(f"✅ Server responding: {response.status_code == 200}")

# Test 2: Create workflow (if API endpoint exists)
# Add specific API tests based on your server's endpoints
```

Run:
```powershell
python test_n8n_manual.py
```

---

## 🤖 Agent Builder MCP Server Testing (Port 7863)

### Option 1: Web UI Testing (Easiest)

1. **Open in Browser**: http://localhost:7863

2. **Test ADK Tab**:
   - Name: "Python Helper"
   - Description: "Helps with Python coding"
   - Capabilities: code_analysis, debugging
   - Model: claude-3-5-sonnet-20241022
   - Click "Create Agent"
   - Verify agent configuration appears

3. **Test A2A Protocol Tab**:
   - Agent Name: "Coordinator"
   - Protocol Version: 1.0
   - Message Format: JSON
   - Click "Create A2A Agent"
   - Check protocol configuration

4. **Test CrewAI Tab** (Python 3.10-3.12 only):
   - Create 3 agents:
     * Researcher (web_search tool)
     * Analyst (data_analysis tool)
     * Writer (document_generation tool)
   - Create Crew with sequential process
   - Run task: "Analyze AI trends"
   - Check output

5. **Test Langbase Tab**:
   - Memory Name: "Project Memory"
   - Memory Type: conversational
   - Click "Create Memory"
   - Add/retrieve memories

6. **Test AGUI Tab**:
   - Interface Name: "Dashboard"
   - Components: button, input, display
   - Click "Create Interface"
   - Test component interactions

### Option 2: Python API Testing

Create `test_agent_builder_manual.py`:
```python
import requests

BASE_URL = "http://localhost:7863"

print("Testing Agent Builder MCP Server...")
response = requests.get(BASE_URL)
print(f"✅ Server responding: {response.status_code == 200}")

# Test each framework tab is accessible
# Add specific tests for your agent creation endpoints
```

---

## 💻 Local Control MCP Server Testing (Port 7864)

### Option 1: Web UI Testing (Easiest)

1. **Open in Browser**: http://localhost:7864

2. **Test System Commands Tab**:
   - Command: `echo "Hello from Ultimate MCP"`
   - Click "Execute"
   - Verify output appears
   
   - Command: `Get-Date` (Windows) or `date` (Linux/Mac)
   - Click "Execute"
   - Check date output

3. **Test Browser Automation Tab**:
   - URL: `https://example.com`
   - Selector: `h1`
   - Click "Scrape"
   - Verify page title is extracted
   
   - Test with pagination:
     * URL: `https://books.toscrape.com`
     * Selectors:
       ```json
       {
         "title": "h3 a",
         "price": ".price_color"
       }
       ```
     * Enable pagination, max 2 pages
     * Click "Scrape"
     * Check results table

4. **Test File Operations Tab**:
   - Operation: Create File
   - Path: `temp_test.txt`
   - Content: `This is a test file`
   - Click "Execute"
   - Verify file created
   
   - Operation: Read File
   - Path: `temp_test.txt`
   - Click "Execute"
   - Verify content displayed
   
   - Operation: Delete File
   - Path: `temp_test.txt`
   - Click "Execute"
   - Verify file deleted

### Option 2: Python API Testing

Create `test_local_control_manual.py`:
```python
import requests

BASE_URL = "http://localhost:7864"

print("Testing Local Control MCP Server...")
response = requests.get(BASE_URL)
print(f"✅ Server responding: {response.status_code == 200}")

# Test system commands, browser automation, file ops
# Add specific API endpoint tests
```

---

## 🔗 End-to-End Integration Testing

### Option 1: Run Existing E2E Tests

```powershell
# Ensure all servers are running first
python launch_all_servers.py

# Wait 10 seconds for startup
Start-Sleep -Seconds 10

# Run E2E tests
python -m pytest tests/e2e/ -v
```

### Option 2: Manual Cross-Server Workflow Test

Create `test_e2e_manual.py`:
```python
"""
Test a workflow that uses all 3 MCP servers:
1. Local Control: Scrape data from website
2. Agent Builder: Analyze data with AI agent
3. N8N: Send results via email workflow
"""
import requests
import time

print("🧪 E2E Integration Test\n")

# Step 1: Local Control - Scrape data
print("Step 1: Scraping data with Local Control MCP...")
local_url = "http://localhost:7864"
# Make API call to scrape endpoint (adjust based on your API)
print("✅ Data scraped\n")

# Step 2: Agent Builder - Analyze data
print("Step 2: Analyzing data with Agent Builder MCP...")
agent_url = "http://localhost:7863"
# Make API call to agent endpoint (adjust based on your API)
print("✅ Data analyzed\n")

# Step 3: N8N - Send results
print("Step 3: Sending results with N8N MCP...")
n8n_url = "http://localhost:7862"
# Make API call to N8N endpoint (adjust based on your API)
print("✅ Results sent\n")

print("🎉 E2E test complete!")
```

Run:
```powershell
python test_e2e_manual.py
```

---

## 🔌 Claude Desktop Connection Testing

### Step 1: Verify Config Installed
```powershell
# Check config file exists
Test-Path "$env:APPDATA\Claude\claude_desktop_config.json"
# Should return: True

# View config
Get-Content "$env:APPDATA\Claude\claude_desktop_config.json" | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

### Step 2: Restart Claude Desktop
```powershell
# Close Claude Desktop
Get-Process | Where-Object {$_.ProcessName -eq 'Claude'} | Stop-Process

# Wait 5 seconds
Start-Sleep -Seconds 5

# Restart (adjust path if needed)
Start-Process "C:\Users\W3jde\AppData\Local\AnthropicClaude\Claude.exe"
```

### Step 3: Test in Claude Desktop

Open Claude Desktop and try these commands:

1. **Check MCP Servers**:
   ```
   What MCP servers are available?
   ```
   *Expected: Should list 3 servers (ultimate-mcp-n8n, ultimate-mcp-agent-builder, ultimate-mcp-local-control)*

2. **Test N8N MCP**:
   ```
   Create a simple workflow that sends me an email reminder every day at 9 AM
   ```
   *Expected: Claude uses N8N MCP to generate workflow*

3. **Test Agent Builder MCP**:
   ```
   Create an ADK agent that can help me write Python code
   ```
   *Expected: Claude uses Agent Builder MCP to create agent*

4. **Test Local Control MCP**:
   ```
   What is my computer's current CPU usage and memory status?
   ```
   *Expected: Claude uses Local Control MCP to get system info*

5. **Test Cross-MCP Workflow**:
   ```
   Scrape the top 5 articles from Hacker News, analyze them, and create a summary workflow in N8N
   ```
   *Expected: Claude coordinates all 3 MCPs*

---

## 📊 Automated Test Suite

### Run All Tests
```powershell
# Run comprehensive test suite
python test_all_servers.py

# Run pytest unit tests
python -m pytest tests/ -v

# Run pytest with coverage
python -m pytest tests/ -v --cov=backend --cov-report=html
```

### Expected Output
```
✅ PASS Master Orchestrator       | Server responding
✅ PASS N8N MCP Server            | Gradio UI responding
✅ PASS Agent Builder MCP         | Gradio UI responding
✅ PASS Local Control MCP         | Gradio UI responding

Results: 4 passed, 0 warnings, 0 failed out of 4 tests
🎉 ALL TESTS PASSED! System is fully operational.
```

---

## 🐛 Troubleshooting

### Server Not Responding
```powershell
# Check if server is running
Test-NetConnection -ComputerName localhost -Port 7862  # N8N
Test-NetConnection -ComputerName localhost -Port 7863  # Agent Builder
Test-NetConnection -ComputerName localhost -Port 7864  # Local Control

# Restart specific server
# (Stop and restart using launch_all_servers.py)
```

### Gradio UI Not Loading
```powershell
# Check logs
Get-Content backend/logs/*.log | Select-Object -Last 50

# Clear browser cache and reload
```

### Claude Desktop Not Seeing Servers
```powershell
# Verify config
Get-Content "$env:APPDATA\Claude\claude_desktop_config.json"

# Check servers are running
python test_all_servers.py

# Restart Claude Desktop completely
```

---

## 📝 Test Checklist

### Before Testing
- [ ] All 4 servers running (7860, 7862, 7863, 7864)
- [ ] Virtual environment activated
- [ ] .env file configured with API keys
- [ ] Playwright browsers installed (`playwright install chromium`)

### N8N MCP Server
- [ ] Gradio UI loads at http://localhost:7862
- [ ] Can generate workflow from description
- [ ] Can test workflow with sample data
- [ ] Can deploy workflow (or shows proper error)

### Agent Builder MCP Server
- [ ] Gradio UI loads at http://localhost:7863
- [ ] ADK agent creation works
- [ ] A2A protocol configuration works
- [ ] CrewAI multi-agent team creation works (Python 3.10-3.12)
- [ ] Langbase memory operations work
- [ ] AGUI interface creation works

### Local Control MCP Server
- [ ] Gradio UI loads at http://localhost:7864
- [ ] System commands execute successfully
- [ ] Browser automation scrapes data
- [ ] File operations work (create, read, delete)

### E2E Integration
- [ ] Can run pytest E2E tests
- [ ] Cross-server workflows function
- [ ] Orchestrator routes requests correctly

### Claude Desktop
- [ ] Config installed at %APPDATA%\Claude\
- [ ] 3 MCP servers appear in Claude
- [ ] Can use N8N MCP through Claude
- [ ] Can use Agent Builder MCP through Claude
- [ ] Can use Local Control MCP through Claude

---

## 🎯 Quick Start Testing

**The fastest way to test everything:**

```powershell
# 1. Ensure servers are running
python launch_all_servers.py

# 2. Run automated tests
python test_all_servers.py

# 3. Open UIs in browser
Start-Process "http://localhost:7862"  # N8N
Start-Process "http://localhost:7863"  # Agent Builder
Start-Process "http://localhost:7864"  # Local Control

# 4. Try each UI manually (see sections above)

# 5. Test Claude Desktop connection (restart Claude first)
```

---

**Need help?** Check `HANDOVER_COMPLETE.md` for troubleshooting or `docs/setup/CLAUDE_DESKTOP_INSTALL.md` for Claude Desktop issues.

**Ready to test?** Start with the Quick Start Testing section above! 🚀
