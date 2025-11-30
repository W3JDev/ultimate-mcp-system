# 📦 Installation Guide

Complete guide to installing and setting up the Ultimate MCP System.

## Prerequisites

### System Requirements

- **Operating System**: Linux, macOS, or Windows 10+
- **Python**: 3.11 or higher (3.13 supported with additional steps)
- **RAM**: Minimum 4GB, recommended 8GB+
- **Disk Space**: 2GB for installation and dependencies
- **Network**: Internet connection for package downloads

### Optional Requirements

- **Docker**: For containerized deployment (recommended for production)
- **Anthropic API Key**: For AI-powered features
- **OpenAI API Key**: Alternative AI provider
- **N8N Instance**: For workflow automation features

## Installation Methods

### Method 1: Quick Install (Recommended for Testing)

```bash
# Clone the repository
git clone https://github.com/W3JDev/ultimate-mcp-system.git
cd ultimate-mcp-system

# Create and activate virtual environment
python -m venv venv

# On Windows
.\venv\Scripts\Activate.ps1

# On Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt

# Install Playwright browsers
playwright install chromium

# Configure environment
cp .env.example .env
# Edit .env with your API keys (optional for basic testing)

# Start all servers
python launch_all_servers.py
```

### Method 2: Docker Installation (Recommended for Production)

```bash
# Clone the repository
git clone https://github.com/W3JDev/ultimate-mcp-system.git
cd ultimate-mcp-system

# Copy environment file
cp .env.example .env
# Edit .env with your API keys

# Start with Docker Compose
docker-compose up -d

# Verify all services are running
docker-compose ps

# View logs
docker-compose logs -f
```

### Method 3: Manual Installation

#### Step 1: Clone Repository

```bash
git clone https://github.com/W3JDev/ultimate-mcp-system.git
cd ultimate-mcp-system
```

#### Step 2: Set Up Python Environment

**For Python 3.11 or 3.12:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\Activate.ps1  # Windows
```

**For Python 3.13 (Additional Steps):**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\Activate.ps1  # Windows

# Install Python 3.13 compatibility packages
pip install audioop-lts
pip install 'huggingface_hub<1.0.0'
```

#### Step 3: Install Dependencies

```bash
pip install -r backend/requirements.txt
```

#### Step 4: Install Playwright Browsers

```bash
playwright install chromium
playwright install-deps chromium  # Linux only
```

#### Step 5: Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit with your preferred editor
nano .env  # or vim, code, etc.
```

**Required API Keys (for full functionality):**
```env
ANTHROPIC_API_KEY=sk-ant-api03-...
OPENAI_API_KEY=sk-...
```

**Optional API Keys:**
```env
N8N_API_KEY=your_n8n_key
N8N_BASE_URL=http://localhost:5678
GITHUB_TOKEN=ghp_...
COMPOSIO_API_KEY=...
```

#### Step 6: Create Required Directories

```bash
mkdir -p backend/logs
mkdir -p backend/memory
mkdir -p backend/mcp_servers/agent_builder/agents
```

#### Step 7: Verify Installation

```bash
# Test Python imports
python -c "import gradio, fastapi, anthropic; print('✅ All imports successful')"

# Check Python version
python --version

# Verify Playwright installation
playwright --version
```

## Starting the System

### Start All Servers at Once

```bash
python launch_all_servers.py
```

This launches all 4 MCP servers:
- Master Orchestrator: http://localhost:7860
- N8N Automation: http://localhost:7862
- Agent Builder: http://localhost:7863
- Local Control: http://localhost:7864

### Start Individual Servers

```bash
# Master Orchestrator (Port 7860)
python backend/main.py

# N8N Automation MCP (Port 7862)
python backend/mcp_servers/n8n_automation/server.py

# Agent Builder MCP (Port 7863)
python backend/mcp_servers/agent_builder/server.py

# Local Control MCP (Port 7864)
python backend/mcp_servers/local_control/server.py
```

### Run in Background (Linux/Mac)

```bash
# Using nohup
nohup python launch_all_servers.py > logs/system.log 2>&1 &

# Using screen
screen -dmS mcp-system python launch_all_servers.py

# Using tmux
tmux new-session -d -s mcp-system 'python launch_all_servers.py'
```

### Run as Windows Service

```powershell
# Using NSSM (Non-Sucking Service Manager)
nssm install UltimateMCP "C:\Path\To\Python\python.exe"
nssm set UltimateMCP AppDirectory "C:\Path\To\ultimate-mcp-system"
nssm set UltimateMCP AppParameters "launch_all_servers.py"
nssm start UltimateMCP
```

## Verification

### Check Server Status

**PowerShell (Windows):**
```powershell
Test-NetConnection -ComputerName localhost -Port 7860
Test-NetConnection -ComputerName localhost -Port 7862
Test-NetConnection -ComputerName localhost -Port 7863
Test-NetConnection -ComputerName localhost -Port 7864
```

**Bash (Linux/Mac):**
```bash
curl http://localhost:7860/health || echo "Port 7860 not responding"
curl http://localhost:7862 || echo "Port 7862 not responding"
curl http://localhost:7863 || echo "Port 7863 not responding"
curl http://localhost:7864 || echo "Port 7864 not responding"
```

### View Logs

```bash
# All logs are in backend/logs/
tail -f backend/logs/mcp_system.log
tail -f backend/logs/agent_builder.log
tail -f backend/logs/n8n_automation.log
```

### Test Basic Functionality

1. Open http://localhost:7860 in your browser
2. You should see the Master Orchestrator UI
3. Try sending a test message (works without API keys)
4. Check individual server UIs at ports 7862-7864

## Troubleshooting

### Port Already in Use

```bash
# Find process using port (Linux/Mac)
lsof -i :7860

# Find process using port (Windows)
netstat -ano | findstr :7860

# Kill process
kill <PID>  # Linux/Mac
taskkill /PID <PID> /F  # Windows
```

### Gradio Won't Start (Python 3.13)

```bash
pip install audioop-lts
pip install 'huggingface_hub<1.0.0'
```

### Missing Playwright Browsers

```bash
playwright install chromium
playwright install-deps chromium
```

### Import Errors

```bash
# Reinstall dependencies
pip install --force-reinstall -r backend/requirements.txt

# Check Python version
python --version

# Verify virtual environment is activated
which python  # Linux/Mac
where python  # Windows
```

### Permission Errors (Linux/Mac)

```bash
# Fix directory permissions
chmod -R 755 backend/
chmod -R 777 backend/logs/
```

## Next Steps

- Read the [Quick Start Guide](quickstart.md)
- Configure [API Keys](configuration.md)
- Check out [Usage Examples](../examples/basic-examples.md)
- Review [Architecture Documentation](../architecture/system-architecture.md)

## Additional Resources

- [System Requirements Details](system-requirements.md)
- [Development Setup](development.md)
- [Deployment Guide](../../DEPLOYMENT.md)
- [Troubleshooting Guide](troubleshooting.md)
