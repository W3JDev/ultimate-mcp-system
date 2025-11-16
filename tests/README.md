# 🧪 Testing Documentation

**Project**: Ultimate MCP System  
**Testing Framework**: Manual testing + pytest (future)

---

## 📋 Test Coverage

### Current Testing Status
- ✅ Manual testing of all UIs
- ✅ Server startup verification
- ✅ Basic functionality validation
- ⚠️ Automated tests pending

### Test Categories

#### 1. Unit Tests (Pending)
- Individual function testing
- Component isolation
- Edge case validation

#### 2. Integration Tests (Pending)
- Server-to-server communication
- API endpoint testing
- MCP routing validation

#### 3. End-to-End Tests (Manual)
- Complete workflow execution
- Multi-service orchestration
- User scenario simulation

---

## 🚀 Manual Testing Checklist

### Server Startup Tests

```bash
# Test 1: Master Orchestrator
cd backend
python main.py &
sleep 5
curl http://localhost:7860/status
# Expected: {"status": "running", ...}

# Test 2: N8N Automation MCP
python mcp_servers/n8n_automation/server.py &
sleep 5
curl http://localhost:7862
# Expected: HTML response (Gradio UI)

# Test 3: Agent Builder MCP
python mcp_servers/agent_builder/server.py &
sleep 5
curl http://localhost:7863
# Expected: HTML response (Gradio UI)

# Test 4: Local Control MCP
python mcp_servers/local_control/server.py &
sleep 5
curl http://localhost:7864
# Expected: HTML response (Gradio UI)
```

### Functional Tests

#### Master Orchestrator
- [ ] Can route N8N requests correctly
- [ ] Can route Agent Builder requests correctly
- [ ] Can route Local Control requests correctly
- [ ] Handles invalid requests gracefully
- [ ] Returns proper JSON responses
- [ ] Logs requests appropriately

#### N8N Automation MCP
- [ ] Can generate workflows from descriptions
- [ ] Validates workflow structure
- [ ] Handles invalid inputs
- [ ] Returns proper JSON format
- [ ] Shows error messages clearly

#### Agent Builder MCP
- [ ] Can create ADK agents
- [ ] Can create CrewAI teams
- [ ] Can create A2A agents
- [ ] Can create Langbase agents
- [ ] Can create AGUI agents
- [ ] Lists all agents correctly
- [ ] Stores agent configurations

#### Local Control MCP
- [ ] Can list files
- [ ] Can execute system commands (carefully!)
- [ ] Can display system information
- [ ] Can manage processes
- [ ] Browser automation works
- [ ] Handles permissions correctly

---

## 📝 Test Scenarios

### Scenario 1: Simple Workflow Request
**Objective**: Test basic orchestrator routing

```bash
curl -X POST http://localhost:7860/process \
  -H "Content-Type: application/json" \
  -d '{"message": "Create a workflow that sends email notifications"}'
```

**Expected Output**:
- Status: success
- Response contains N8N routing mention
- Proper JSON structure

**Actual Output**:
```json
{
  "status": "success",
  "message": "Create a workflow that sends email notifications",
  "response": "Routing to N8N Automation MCP..."
}
```

**Result**: ✅ PASS

---

### Scenario 2: Agent Creation
**Objective**: Test agent builder functionality

1. Open http://localhost:7863
2. Navigate to "ADK Agent" tab
3. Fill in:
   - Name: "Test Agent"
   - Description: "A test agent"
   - Tools: ["web_search"]
   - Model: "claude-3-5-sonnet-20241022"
4. Click "Create Agent"

**Expected Output**:
- Success message
- Agent ID generated
- Configuration saved

**Actual Output**:
```json
{
  "agent_id": "adk-test-agent-001",
  "status": "created",
  "framework": "ADK"
}
```

**Result**: ✅ PASS

---

### Scenario 3: Multi-Service Orchestration
**Objective**: Test complex routing across multiple services

```bash
curl -X POST http://localhost:7860/process \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Create a CrewAI team to research topics, then generate an N8N workflow to send daily summaries"
  }'
```

**Expected Output**:
- Recognizes need for both Agent Builder and N8N
- Routes to both services
- Returns combined response

**Actual Output**:
(Manual test pending)

**Result**: ⚠️ PENDING

---

## 🛠️ Future Automated Tests

### Test Suite Structure (Planned)

```
tests/
├── unit/
│   ├── test_orchestrator.py
│   ├── test_memory.py
│   ├── test_n8n_workflow_builder.py
│   └── test_agent_builder.py
├── integration/
│   ├── test_server_communication.py
│   ├── test_api_endpoints.py
│   └── test_mcp_routing.py
└── e2e/
    ├── test_complete_workflows.py
    └── test_user_scenarios.py
```

### Sample Unit Test (Planned)

```python
# tests/unit/test_orchestrator.py
import pytest
from backend.orchestrator import MCPOrchestrator

def test_intent_analysis_n8n():
    orchestrator = MCPOrchestrator(memory=None)
    intent = orchestrator.analyze_intent(
        "Create a workflow that sends emails"
    )
    assert intent == "n8n_automation"

def test_intent_analysis_agent():
    orchestrator = MCPOrchestrator(memory=None)
    intent = orchestrator.analyze_intent(
        "Create a research agent using CrewAI"
    )
    assert intent == "agent_builder"

def test_routing_to_n8n():
    orchestrator = MCPOrchestrator(memory=None)
    response = orchestrator.process(
        "Generate an N8N workflow"
    )
    assert "N8N" in response
    assert "workflow" in response.lower()
```

### Running Tests (When Implemented)

```bash
# Install test dependencies
pip install pytest pytest-cov pytest-asyncio

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=backend --cov-report=html

# Run specific test file
pytest tests/unit/test_orchestrator.py -v

# Run tests matching pattern
pytest tests/ -k "test_n8n" -v
```

---

## 📊 Test Logs

See [TEST_LOGS.md](../TEST_LOGS.md) for detailed test execution logs.

---

## ✅ Testing Best Practices

1. **Test Early** - Test each component as you build it
2. **Test Often** - Re-test after every change
3. **Test Realistically** - Use real-world scenarios
4. **Test Edge Cases** - Invalid inputs, missing data, errors
5. **Document Results** - Keep logs of what works/doesn't
6. **Automate** - Move from manual to automated tests
7. **Monitor** - Check logs for hidden issues

---

## 🐛 Known Issues

### Issue 1: API Keys
- **Problem**: Tests fail without API keys
- **Workaround**: Use fallback/template mode
- **Status**: Expected behavior

### Issue 2: Gradio UI Testing
- **Problem**: Gradio UIs not easily testable programmatically
- **Workaround**: Manual testing for now
- **Status**: Acceptable for Phase 5

### Issue 3: Browser Automation
- **Problem**: Playwright requires browser installation
- **Workaround**: `playwright install chromium`
- **Status**: Fixed in setup docs

---

## 🎯 Testing Goals for Phase 5

- [x] Manual testing of all UIs
- [x] Server startup verification
- [x] Basic functionality validation
- [ ] Document test scenarios (5+)
- [ ] Execute and log test results
- [ ] Create automated test framework
- [ ] Achieve 50%+ code coverage
- [ ] Fix all critical bugs found

---

**Last Updated**: November 16, 2025  
**Next Review**: After implementing automated tests
