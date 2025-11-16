# 🔧 Troubleshooting Guide

Common issues and solutions for the Ultimate MCP System.

## Installation Issues

### Python Version Errors

**Problem**: `ImportError: No module named 'audioop'` on Python 3.13

**Solution**:
```bash
pip install audioop-lts
pip install 'huggingface_hub<1.0.0'
```

**Explanation**: Python 3.13 removed the `audioop` module. Gradio depends on it, so we need the compatibility package.

---

**Problem**: `ModuleNotFoundError: No module named 'gradio'`

**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\Activate.ps1  # Windows

# Reinstall dependencies
pip install -r backend/requirements.txt
```

---

### Port Already in Use

**Problem**: `OSError: [Errno 48] Address already in use`

**Solution (Linux/Mac)**:
```bash
# Find process using port
lsof -i :7860

# Kill process
kill -9 <PID>

# Or kill all Python processes (caution!)
pkill -9 python
```

**Solution (Windows)**:
```powershell
# Find process using port
netstat -ano | findstr :7860

# Kill process
taskkill /PID <PID> /F

# Or stop all Python processes
Get-Process python | Stop-Process -Force
```

---

### Playwright Browser Not Found

**Problem**: `Error: Executable doesn't exist at /path/to/chromium`

**Solution**:
```bash
# Install Playwright browsers
playwright install chromium

# Linux: Install system dependencies
playwright install-deps chromium

# If still fails, try reinstalling Playwright
pip uninstall playwright
pip install playwright
playwright install chromium
```

---

## Runtime Issues

### API Key Errors

**Problem**: `AuthenticationError: Invalid API key`

**Solution**:
```bash
# Check .env file exists
ls -la .env

# Verify key format
# Anthropic: sk-ant-api03-...
# OpenAI: sk-...

# Test key validity
python -c "
from anthropic import Anthropic
import os
from dotenv import load_dotenv
load_dotenv()
client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
print('✅ API key is valid')
"
```

**Note**: System works without API keys but with limited functionality.

---

**Problem**: `API key not found in environment`

**Solution**:
```bash
# Copy example file
cp .env.example .env

# Edit with your keys
nano .env

# Restart servers
python launch_all_servers.py
```

---

### Server Connection Issues

**Problem**: Server not responding at `http://localhost:7860`

**Check 1**: Is server running?
```bash
# Check running Python processes
ps aux | grep python

# Or on Windows
tasklist | findstr python
```

**Check 2**: Can you reach the port?
```bash
# Linux/Mac
curl http://localhost:7860

# Windows PowerShell
Test-NetConnection localhost -Port 7860
```

**Check 3**: View logs
```bash
tail -f backend/logs/mcp_system.log
```

**Solution**: Restart server
```bash
# Stop (Ctrl+C if running in foreground)
# Or kill process as shown above

# Start
python backend/main.py
```

---

### Memory/Context Issues

**Problem**: Orchestrator forgets previous conversation

**Solution**:
```python
# Check memory manager is working
python -c "
from backend.memory import MemoryManager
memory = MemoryManager()
memory.add_message('user', 'test')
print(memory.get_context())
"
```

**Workaround**: Restart server to clear memory and start fresh.

---

### Workflow Generation Fails

**Problem**: N8N workflow generation returns error or empty

**Check 1**: API key is set
```bash
grep ANTHROPIC_API_KEY .env
```

**Check 2**: Description is clear
❌ "Create workflow"  
✅ "Create workflow that sends email when GitHub issue is created"

**Check 3**: View N8N MCP logs
```bash
tail -f backend/logs/n8n_automation.log
```

**Fallback**: Use templates
- Go to "Templates" tab in N8N MCP
- Select pre-built template
- Customize for your needs

---

### Agent Creation Issues

**Problem**: Agent creation fails with framework error

**Check 1**: Python version
```bash
python --version
# CrewAI requires Python 3.10-3.12
# Other frameworks support 3.11+
```

**Check 2**: Framework dependencies installed
```bash
pip list | grep -i crewai
pip list | grep -i langchain
```

**Solution**: Install missing dependencies
```bash
pip install crewai  # Python 3.10-3.12 only
pip install langchain langchain-openai langchain-anthropic
```

---

## Docker Issues

### Docker Compose Fails to Start

**Problem**: `ERROR: Service 'orchestrator' failed to build`

**Solution**:
```bash
# View detailed error
docker-compose build --no-cache

# Check Docker is running
docker ps

# Check disk space
df -h

# Prune old images
docker system prune -a
```

---

**Problem**: Container exits immediately

**Solution**:
```bash
# View logs
docker-compose logs orchestrator

# Check if .env file exists
ls -la .env

# Start with explicit .env
docker-compose --env-file .env up
```

---

### Port Conflicts in Docker

**Problem**: `Error: Port 7860 is already allocated`

**Solution**:
```bash
# Stop all containers
docker-compose down

# Or change ports in docker-compose.yml
# Change "7860:7860" to "8860:7860"
```

---

## Performance Issues

### Slow Response Times

**Problem**: Requests take >10 seconds

**Check 1**: API provider status
- Check Anthropic status: https://status.anthropic.com/
- Check OpenAI status: https://status.openai.com/

**Check 2**: System resources
```bash
# Check CPU and memory
top  # Linux/Mac
# Windows: Task Manager

# Check disk I/O
iostat  # Linux
```

**Solution 1**: Reduce context length
```python
# In backend/memory.py
memory = MemoryManager(max_context_length=3)  # Reduce from 10
```

**Solution 2**: Use keyword routing
```python
# Works without API calls
# Set empty API key to force keyword routing
```

---

### High Memory Usage

**Problem**: Python process using >2GB RAM

**Solution**:
```bash
# Restart servers regularly
# Add cron job to restart daily

# Limit context history
# Edit memory.py to reduce max_context_length

# Monitor with
ps aux | grep python | awk '{print $6/1024 " MB"}'
```

---

## Network Issues

### Cannot Connect to N8N Instance

**Problem**: `Connection refused` to N8N at port 5678

**Solution**:
```bash
# Check N8N is running
curl http://localhost:5678

# Start N8N with Docker
docker run -d --name n8n -p 5678:5678 n8nio/n8n

# Or with docker-compose (included in project)
docker-compose up n8n
```

---

### CORS Errors in Browser

**Problem**: `CORS policy: No 'Access-Control-Allow-Origin' header`

**Solution**: Use Gradio's built-in sharing or configure CORS in FastAPI:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Development Issues

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'orchestrator'`

**Solution**:
```bash
# Run from project root
cd /path/to/ultimate-mcp-system
python backend/main.py

# Or add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/path/to/ultimate-mcp-system/backend"
```

---

### Code Changes Not Taking Effect

**Problem**: Changes to Python files don't reflect in running server

**Solution**:
```bash
# Stop server (Ctrl+C)
# Restart server
python backend/main.py

# For development, use auto-reload
uvicorn backend.main:app --reload
```

---

## Testing Issues

### Tests Failing

**Problem**: `pytest` fails with import errors

**Solution**:
```bash
# Install test dependencies
pip install pytest pytest-cov pytest-asyncio httpx

# Run from project root
cd /path/to/ultimate-mcp-system
pytest tests/ -v
```

---

**Problem**: E2E tests fail with "Connection refused"

**Solution**:
```bash
# E2E tests require all servers running
python launch_all_servers.py

# Then run E2E tests
pytest tests/e2e/ -v

# Or skip E2E tests
pytest tests/ -v -m "not e2e"
```

---

## Logging & Debugging

### Enable Debug Logging

**Method 1**: Environment variable
```bash
export LOG_LEVEL=DEBUG
python backend/main.py
```

**Method 2**: Edit server files
```python
from loguru import logger

logger.add(
    "logs/debug.log",
    level="DEBUG",  # Change from INFO
    rotation="1 day"
)
```

---

### View All Logs

```bash
# All logs in one view
tail -f backend/logs/*.log

# Specific server
tail -f backend/logs/mcp_system.log
tail -f backend/logs/agent_builder.log
tail -f backend/logs/n8n_automation.log

# With grep filtering
tail -f backend/logs/*.log | grep ERROR
```

---

### Clear Logs

```bash
# Delete old logs
rm backend/logs/*.log

# Or truncate
truncate -s 0 backend/logs/*.log

# Restart servers to recreate
```

---

## Database/Storage Issues

### Agent Storage Corruption

**Problem**: Agent Builder can't load saved agents

**Solution**:
```bash
# Check agents directory
ls -la backend/mcp_servers/agent_builder/agents/

# Validate JSON files
for file in backend/mcp_servers/agent_builder/agents/*.json; do
    python -m json.tool "$file" > /dev/null || echo "Invalid: $file"
done

# Backup and reset if needed
cp -r backend/mcp_servers/agent_builder/agents backup/
rm backend/mcp_servers/agent_builder/agents/*.json
```

---

## Security Issues

### Running as Root (Linux)

**Problem**: Should not run as root user

**Solution**:
```bash
# Create non-root user
useradd -m mcp-user
chown -R mcp-user:mcp-user /path/to/ultimate-mcp-system

# Run as that user
su - mcp-user
cd /path/to/ultimate-mcp-system
python launch_all_servers.py
```

---

### Exposed Secrets in Logs

**Problem**: API keys appearing in logs

**Solution**:
```python
# In logging code, mask secrets
import re

def mask_secrets(text):
    # Mask API keys
    text = re.sub(r'sk-ant-api03-[\w-]+', 'sk-ant-***', text)
    text = re.sub(r'sk-[\w]+', 'sk-***', text)
    return text

logger.info(mask_secrets(message))
```

---

## Getting More Help

### Check Documentation
1. [Installation Guide](installation.md)
2. [Configuration Guide](configuration.md)
3. [API Documentation](../api/rest-api.md)
4. [Architecture Guide](../architecture/system-architecture.md)

### Search Existing Issues
- [GitHub Issues](https://github.com/W3JDev/ultimate-mcp-system/issues)
- Use search to find similar problems

### Create New Issue
If your problem isn't listed:
1. Check if it's a known issue
2. Gather information:
   - Python version
   - Operating system
   - Error messages
   - Logs
3. Create detailed issue with reproduction steps

### Join Community
- [GitHub Discussions](https://github.com/W3JDev/ultimate-mcp-system/discussions)
- Ask questions
- Share solutions

---

## Quick Reference

### Most Common Issues

1. **Port in use** → Kill process or change port
2. **Import error** → Check virtual environment activated
3. **API key error** → Check .env file, restart server
4. **Playwright error** → Run `playwright install chromium`
5. **Python 3.13** → Install `audioop-lts`

### Health Check Commands

```bash
# Check servers
curl http://localhost:7860 || echo "Orchestrator down"
curl http://localhost:7862 || echo "N8N MCP down"
curl http://localhost:7863 || echo "Agent Builder down"
curl http://localhost:7864 || echo "Local Control down"

# Check logs for errors
grep -i error backend/logs/*.log

# Check Python processes
ps aux | grep python

# Check ports
lsof -i :7860,:7862,:7863,:7864
```

### Emergency Reset

```bash
# Stop everything
pkill -9 python  # Linux/Mac
Get-Process python | Stop-Process -Force  # Windows

# Clear logs
rm backend/logs/*.log

# Clear memory/state
rm -rf backend/memory/*
rm -rf backend/mcp_servers/agent_builder/agents/*

# Restart fresh
python launch_all_servers.py
```
