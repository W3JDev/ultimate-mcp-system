# 🛠️ Scripts Directory

**Purpose**: Automation scripts for testing, deployment, and demo management

---

## 📜 Available Scripts

### 1. `start_demo.sh` - Start Demo Environment
**Purpose**: Start all 4 MCP servers for demo/testing

**Usage**:
```bash
./scripts/start_demo.sh
```

**What it does**:
- ✅ Checks Python version and dependencies
- ✅ Activates virtual environment
- ✅ Creates necessary directories (logs, pids)
- ✅ Checks for port conflicts
- ✅ Starts all 4 servers in background
- ✅ Saves PIDs for later management
- ✅ Optionally runs server tests

**Servers Started**:
- Master Orchestrator (port 7860)
- N8N Automation MCP (port 7862)
- Agent Builder MCP (port 7863)
- Local Control MCP (port 7864)

**Requirements**:
- Python 3.11+ installed
- Virtual environment created (script creates if missing)
- Dependencies installed (script installs if missing)

---

### 2. `stop_demo.sh` - Stop All Servers
**Purpose**: Gracefully stop all running MCP servers

**Usage**:
```bash
./scripts/stop_demo.sh
```

**What it does**:
- ✅ Reads PIDs from saved files
- ✅ Sends SIGTERM to each process
- ✅ Falls back to SIGKILL if needed
- ✅ Cleans up PID files
- ✅ Checks ports for any remaining processes

**Safe to Run**:
- Won't error if servers not running
- Cleans up stale PID files
- Double-checks ports after stopping

---

### 3. `test_servers.sh` - Test Server Health
**Purpose**: Verify all servers are running and responding correctly

**Usage**:
```bash
./scripts/test_servers.sh
```

**What it does**:
- ✅ Tests port availability (7860-7864)
- ✅ Tests HTTP endpoints (/, /status, /docs)
- ✅ Tests API functionality (/process)
- ✅ Tests error handling
- ✅ Tests routing logic (N8N, Agent Builder)
- ✅ Generates test report with pass/fail stats

**Test Phases**:
1. **Phase 1**: Port Availability (netcat)
2. **Phase 2**: HTTP Endpoint Tests (curl)
3. **Phase 3**: API Functionality Tests
4. **Phase 4**: Response Validation Tests

**Output**:
```
🧪 Ultimate MCP System - Server Testing Script
==============================================

📡 Phase 1: Port Availability Tests
-----------------------------------
Testing Master Orchestrator (port 7860)... ✅ PASS
Testing N8N Automation MCP (port 7862)... ✅ PASS
...

📈 Test Results Summary
==============================================
Tests Run:    15
Tests Passed: 15
Tests Failed: 0

Success Rate: 100%

✅ System Health: EXCELLENT
```

**Exit Codes**:
- `0` - All tests passed (80%+ success rate)
- `1` - Tests failed (<60% success rate)

---

## 🚀 Quick Start Workflow

### First Time Setup
```bash
# 1. Clone repository (if not already done)
git clone https://github.com/W3JDev/ultimate-mcp-system.git
cd ultimate-mcp-system

# 2. Make scripts executable
chmod +x scripts/*.sh

# 3. Start demo environment
./scripts/start_demo.sh

# The script will:
# - Create virtual environment
# - Install dependencies
# - Start all servers
# - Optionally run tests
```

### Daily Development Workflow
```bash
# Start servers
./scripts/start_demo.sh

# Do your development/testing...

# Test servers are working
./scripts/test_servers.sh

# Stop servers when done
./scripts/stop_demo.sh
```

### Demo Day Workflow
```bash
# 30 minutes before demo
./scripts/start_demo.sh

# Verify everything works
./scripts/test_servers.sh

# Open all UIs in browser:
# http://localhost:7860
# http://localhost:7862
# http://localhost:7863
# http://localhost:7864

# Run your demo...

# After demo
./scripts/stop_demo.sh
```

---

## 🔧 Troubleshooting

### Issue: "Permission denied" when running scripts
**Solution**:
```bash
chmod +x scripts/*.sh
```

### Issue: "Python not found"
**Solution**:
```bash
# Install Python 3.11 or later
# Ubuntu/Debian
sudo apt-get install python3.11

# macOS
brew install python@3.11

# Windows
# Download from python.org
```

### Issue: "Port already in use"
**Solution**:
```bash
# Stop existing servers
./scripts/stop_demo.sh

# Or manually kill processes
lsof -ti:7860 | xargs kill -9
lsof -ti:7862 | xargs kill -9
lsof -ti:7863 | xargs kill -9
lsof -ti:7864 | xargs kill -9
```

### Issue: "Module not found" errors
**Solution**:
```bash
# Reinstall dependencies
source venv/bin/activate
pip install -r backend/requirements.txt

# For Python 3.13 compatibility
pip install audioop-lts 'huggingface_hub<1.0.0'
```

### Issue: "Servers won't start"
**Solution**:
```bash
# Check logs
tail -f backend/logs/master.log
tail -f backend/logs/n8n.log
tail -f backend/logs/agent_builder.log
tail -f backend/logs/local_control.log

# Common causes:
# 1. Missing dependencies - run pip install
# 2. Port conflicts - run stop_demo.sh first
# 3. Python version - use 3.11 or 3.12
```

### Issue: Tests fail with "Connection refused"
**Solution**:
```bash
# Servers may still be starting
# Wait 10-15 seconds after start_demo.sh
sleep 10
./scripts/test_servers.sh
```

---

## 📊 Script Output Files

### Logs Directory
```
backend/logs/
├── master.log            # Master Orchestrator logs
├── n8n.log              # N8N Automation MCP logs
├── agent_builder.log    # Agent Builder MCP logs
└── local_control.log    # Local Control MCP logs
```

### PIDs Directory
```
backend/pids/
├── master.pid           # Master Orchestrator PID
├── n8n.pid             # N8N Automation MCP PID
├── agent_builder.pid   # Agent Builder MCP PID
└── local_control.pid   # Local Control MCP PID
```

---

## 🎯 Advanced Usage

### Running Individual Servers
```bash
# Activate virtual environment
source venv/bin/activate

# Start only Master Orchestrator
python backend/main.py

# Start only N8N Automation MCP
python backend/mcp_servers/n8n_automation/server.py

# Start only Agent Builder MCP
python backend/mcp_servers/agent_builder/server.py

# Start only Local Control MCP
python backend/mcp_servers/local_control/server.py
```

### Testing Specific Endpoints
```bash
# Test Master Orchestrator status
curl http://localhost:7860/status

# Test Master Orchestrator process endpoint
curl -X POST http://localhost:7860/process \
  -H "Content-Type: application/json" \
  -d '{"message": "test"}'

# Test N8N UI accessibility
curl http://localhost:7862

# Test Agent Builder UI
curl http://localhost:7863

# Test Local Control UI
curl http://localhost:7864
```

### Viewing Real-Time Logs
```bash
# All logs at once (requires GNU parallel or similar)
tail -f backend/logs/*.log

# Individual logs
tail -f backend/logs/master.log
tail -f backend/logs/n8n.log
tail -f backend/logs/agent_builder.log
tail -f backend/logs/local_control.log

# With color highlighting (if ccze installed)
tail -f backend/logs/master.log | ccze -A
```

---

## 🔐 Environment Variables

Scripts respect `.env` file in project root:

```bash
# backend/.env
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
N8N_API_KEY=your_key_here
N8N_BASE_URL=http://localhost:5678/
```

**Note**: Scripts work without API keys (using fallback mode), but some AI features will be limited.

---

## 📝 Adding New Scripts

To add a new automation script:

1. Create script in `scripts/` directory
2. Add shebang: `#!/bin/bash`
3. Make executable: `chmod +x scripts/your_script.sh`
4. Document in this README
5. Follow existing script patterns for consistency

**Script Template**:
```bash
#!/bin/bash
# Your script description

set -e  # Exit on error

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo "🚀 Your Script Name"
echo "===================="
echo ""

# Your script logic here

echo -e "${GREEN}✅ Done!${NC}"
```

---

## 🤝 Contributing

When modifying scripts:
- Test on Linux, macOS, and Windows (WSL)
- Handle errors gracefully
- Provide helpful error messages
- Update this README
- Follow existing coding style

---

**Last Updated**: November 16, 2025  
**Maintainer**: W3JDev  
**License**: MIT
