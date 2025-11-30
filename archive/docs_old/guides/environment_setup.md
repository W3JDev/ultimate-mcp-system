# Environment Setup Guide

This guide walks you through setting up the development environment for the Ultimate MCP System.

## 🔧 Prerequisites

- **Python**: 3.13+ (required for latest features and sponsor API compatibility)
- **Git**: For version control
- **PowerShell**: For Windows development (recommended)
- **VS Code**: Recommended IDE with Python and MCP extensions

## 📁 Project Structure

```
ultimate-mcp-system/
├── .venv/                    # Python virtual environment (STANDARD)
├── venv/                     # Legacy environment (to be deprecated)
├── docs/                     # Documentation hub
├── backend/                  # Core MCP servers and orchestrator
├── .env                      # Environment variables (create from .env.template)
├── .env.template             # Environment variables template
└── requirements.txt          # Python dependencies
```

## 🚀 Quick Setup

### 1. Clone and Navigate
```powershell
git clone <repository-url>
cd ultimate-mcp-system
```

### 2. Create Python Environment
```powershell
# Create virtual environment (use .venv for consistency)
python -m venv .venv

# Activate environment
.\.venv\Scripts\Activate.ps1

# Verify activation (should show .venv in prompt)
where python
```

### 3. Install Dependencies
```powershell
# Core dependencies
pip install -r backend/requirements.txt

# Critical Python 3.13 compatibility fix
pip install audioop-lts
pip install 'huggingface_hub<1.0.0'

# Browser automation (if needed)
playwright install chromium
```

### 4. Configure Environment
```powershell
# Copy environment template
Copy-Item .env.template .env

# Edit .env file with your API keys
notepad .env  # or your preferred editor
```

### 5. Verify Setup
```powershell
# Test core imports
python -c "import gradio; import loguru; import anthropic; print('✅ Core dependencies working')"

# Check MCP protocol tools
python -c "from backend.orchestrator import MCPOrchestrator; print('✅ MCP orchestrator imports')"
```

## 🔑 Environment Variables

### Required for Basic Functionality
- `ANTHROPIC_API_KEY` - Primary AI model (Claude)
- `OPENAI_API_KEY` - Alternative AI model and embeddings

### Sponsor API Keys (Optional but Recommended)
- `ELEVENLABS_API_KEY` - Text-to-speech
- `HUGGINGFACE_API_TOKEN` - Model hosting
- `MODAL_TOKEN_ID` + `MODAL_TOKEN_SECRET` - GPU compute
- `NEBIUS_API_KEY` - Cloud AI platform
- `SAMBANOVA_API_KEY` - Fast AI inference
- `BLAXEL_API_KEY` - Video processing

### Workflow Automation
- `N8N_API_KEY` + `N8N_BASE_URL` - Workflow automation

See `.env.template` for the complete list with examples.

## 🏗️ Development Workflow

### Starting MCP Servers
```powershell
# Activate environment
.\.venv\Scripts\Activate.ps1

# Start master orchestrator
python backend/main.py

# Or start individual MCP servers
python backend/mcp_servers/n8n_automation/server.py
python backend/mcp_servers/agent_builder/server.py
python backend/mcp_servers/local_control/server.py
```

### Running Tests
```powershell
# Unit tests
pytest backend/tests/

# Integration tests
pytest backend/tests/integration/

# Code quality checks
flake8 backend/ --exclude=venv --max-line-length=100
```

### Monitoring Logs
```powershell
# View real-time logs
Get-Content backend/logs/mcp_system.log -Wait

# Check specific component logs
Get-Content backend/logs/agent_builder.log -Wait
```

## 🐳 Docker Development (Alternative)

If you prefer containerized development:

```powershell
# Build development image
docker-compose up --build

# Run specific services
docker-compose up orchestrator
docker-compose up n8n-mcp
```

## 🔧 IDE Configuration

### VS Code Setup
1. Install extensions:
   - Python
   - MCP Protocol Support
   - Pylance
   - Python Docstring Generator

2. Configure workspace settings (`.vscode/settings.json`):
```json
{
    "python.pythonPath": "./.venv/Scripts/python.exe",
    "python.linting.flake8Enabled": true,
    "python.linting.enabled": true,
    "python.formatting.provider": "black"
}
```

### Environment Variables in IDE
1. Create `.vscode/launch.json` for debugging
2. Reference `.env` file in debug configurations
3. Use VS Code's built-in environment variable support

## 🚨 Common Issues

### Python 3.13 Compatibility
**Problem**: Gradio fails to import with "No module named 'audioop'" error
**Solution**: 
```powershell
pip install audioop-lts
pip install 'huggingface_hub<1.0.0'
```

### Virtual Environment Conflicts
**Problem**: Multiple Python environments causing conflicts
**Solution**: Always use `.venv` and ensure it's activated:
```powershell
# Check which Python you're using
where python
# Should show: C:\path\to\project\.venv\Scripts\python.exe
```

### Port Conflicts
**Problem**: "Port already in use" errors
**Solution**: 
```powershell
# Find processes using ports
Get-NetTCPConnection -LocalPort 7860,7862,7863,7864
# Stop Python processes
Get-Process python | Stop-Process
```

### API Key Issues
**Problem**: Authentication errors with sponsor APIs
**Solution**:
1. Verify `.env` file is in project root
2. Check API key format and validity
3. Restart server after changing environment variables

## 📊 Performance Tuning

### Memory Management
- Use `del` statements for large objects
- Monitor memory usage during development
- Consider Redis for caching in production

### API Rate Limiting
- Implement exponential backoff for API calls
- Use connection pooling for database operations
- Monitor API usage quotas

## 🔒 Security Best Practices

### Development
- Never commit `.env` files
- Use `.env.template` for documentation
- Rotate API keys regularly

### Production
- Use secret management systems
- Enable HTTPS for all endpoints
- Implement proper CORS policies
- Use environment-specific configurations

## 📞 Getting Help

### Documentation
- Check component-specific `AGENT.md` files
- Review API documentation in `/docs/api/`
- Read architecture overviews in `/docs/architecture/`

### Debugging
- Enable debug logging: `LOG_LEVEL=DEBUG` in `.env`
- Use VS Code debugger with breakpoints
- Check server logs in `backend/logs/`

### Community
- GitHub Issues for bug reports
- GitHub Discussions for questions
- Component maintainers listed in individual `AGENT.md` files

---

*Last updated: November 16, 2025*