# ⚡ Quick Start Guide

Get the Ultimate MCP System running in 5 minutes!

## 🚀 One-Command Install (Docker)

```bash
git clone https://github.com/W3JDev/ultimate-mcp-system.git
cd ultimate-mcp-system
cp .env.example .env
docker-compose up -d
```

**Done!** Access at:
- Master Orchestrator: http://localhost:7860
- N8N Automation: http://localhost:7862
- Agent Builder: http://localhost:7863
- Local Control: http://localhost:7864

## 🐍 Python Quick Start (Without Docker)

### 1. Install

```bash
# Clone and enter directory
git clone https://github.com/W3JDev/ultimate-mcp-system.git
cd ultimate-mcp-system

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: .\venv\Scripts\Activate.ps1  # Windows

# Install dependencies
pip install -r backend/requirements.txt
playwright install chromium
```

### 2. Configure (Optional)

```bash
cp .env.example .env
# Edit .env to add API keys (optional for testing)
```

### 3. Launch

```bash
python launch_all_servers.py
```

**Done!** All 4 servers are now running.

## 🎯 First Steps

### Test the Master Orchestrator

1. Open http://localhost:7860
2. You'll see the orchestrator UI
3. Try a test message: "Hello, show me system info"
4. The orchestrator routes your request to the appropriate MCP

### Explore Individual MCPs

**N8N Automation (Port 7862):**
- Create workflows from natural language
- Deploy to N8N instance
- Test workflow logic

**Agent Builder (Port 7863):**
- Build AI agents with multiple frameworks
- Manage agent configurations
- Test agent responses

**Local Control (Port 7864):**
- Execute system commands
- Manage processes
- Automate browser tasks
- Control keyboard/mouse

## 🔑 Adding API Keys (For Full Features)

Edit `.env` file:

```env
# Essential for AI features
ANTHROPIC_API_KEY=sk-ant-api03-YOUR_KEY_HERE
OPENAI_API_KEY=sk-YOUR_KEY_HERE

# Optional integrations
N8N_API_KEY=your_n8n_key
N8N_BASE_URL=http://localhost:5678
```

Restart servers after adding keys:
```bash
# Stop servers (Ctrl+C)
# Then restart
python launch_all_servers.py
```

## 📊 Verify Everything Works

### Check Server Status

```bash
# Quick check (Windows PowerShell)
Test-NetConnection localhost -Port 7860
Test-NetConnection localhost -Port 7862
Test-NetConnection localhost -Port 7863
Test-NetConnection localhost -Port 7864

# Quick check (Linux/Mac)
for port in 7860 7862 7863 7864; do
  curl -s http://localhost:$port && echo "✅ Port $port OK"
done
```

### View Logs

```bash
# Watch all logs
tail -f backend/logs/*.log

# Watch specific server
tail -f backend/logs/mcp_system.log
```

## 🎨 Basic Usage Examples

### Example 1: Create a Workflow

1. Open http://localhost:7862 (N8N Automation)
2. Go to "Workflow Builder" tab
3. Enter description: "Send email when GitHub issue is created"
4. Click "Generate Workflow"
5. View generated N8N workflow JSON

### Example 2: Build an Agent

1. Open http://localhost:7863 (Agent Builder)
2. Select a framework tab (e.g., "ADK Agent")
3. Enter agent details:
   - Name: "Research Assistant"
   - Description: "Helps with research tasks"
   - Model: "claude-3-sonnet"
4. Click "Create Agent"
5. Test agent in the interface

### Example 3: System Automation

1. Open http://localhost:7864 (Local Control)
2. Go to "System Commands" tab
3. Select "Get System Info"
4. Click "Execute"
5. View system information

### Example 4: Smart Routing

1. Open http://localhost:7860 (Master Orchestrator)
2. Enter: "Build me an agent that can search the web"
3. Orchestrator routes to Agent Builder MCP
4. View response with agent creation details

## 🔧 Common First-Time Issues

### Port Already in Use

```bash
# Find and kill process
lsof -i :7860  # Linux/Mac
netstat -ano | findstr :7860  # Windows
```

### Python 3.13 Issues

```bash
pip install audioop-lts
pip install 'huggingface_hub<1.0.0'
```

### Import Errors

```bash
# Ensure virtual environment is activated
which python  # Should show path in venv/

# Reinstall if needed
pip install -r backend/requirements.txt
```

### Browser Not Found (Playwright)

```bash
playwright install chromium
playwright install-deps chromium  # Linux
```

## 📚 Next Steps

Now that you're up and running:

1. **Read Documentation**
   - [Full Installation Guide](installation.md)
   - [Configuration Guide](configuration.md)
   - [User Guide](user-guide.md)

2. **Explore Architecture**
   - [System Architecture](../architecture/system-architecture.md)
   - [MCP Servers Overview](../architecture/mcp-servers.md)

3. **Try Examples**
   - [Basic Examples](../examples/basic-examples.md)
   - [Advanced Examples](../examples/advanced-examples.md)

4. **Deploy to Production**
   - [Deployment Guide](../../DEPLOYMENT.md)
   - [Docker Best Practices](../../DEPLOYMENT.md#docker)

## 🆘 Need Help?

- Check [Troubleshooting Guide](troubleshooting.md)
- Review [FAQ](faq.md)
- Open an [Issue](https://github.com/W3JDev/ultimate-mcp-system/issues)
- Join [Discussions](https://github.com/W3JDev/ultimate-mcp-system/discussions)

## 🎉 You're Ready!

You now have a fully functional multi-MCP orchestration system running locally. Start automating workflows, building agents, and controlling your system with AI!

**Happy Automating! 🚀**
