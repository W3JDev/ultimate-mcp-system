# ⚙️ Configuration Guide

Complete guide to configuring the Ultimate MCP System.

## Environment Variables

All configuration is done through environment variables in the `.env` file.

### Creating Configuration File

```bash
# Copy example file
cp .env.example .env

# Edit with your preferred editor
nano .env  # or vim, code, etc.
```

## Required Configuration

### API Keys (Essential for AI Features)

#### Anthropic API Key

**Purpose**: Powers AI-based workflow generation, agent creation, and intelligent routing

**Get Your Key**: https://console.anthropic.com/

```env
ANTHROPIC_API_KEY=sk-ant-api03-YOUR_KEY_HERE
```

**Used By**:
- Master Orchestrator (intent analysis)
- N8N Automation MCP (workflow generation)
- Agent Builder MCP (agent creation)

#### OpenAI API Key

**Purpose**: Alternative AI provider for agent frameworks

**Get Your Key**: https://platform.openai.com/api-keys

```env
OPENAI_API_KEY=sk-YOUR_KEY_HERE
```

**Used By**:
- Agent Builder MCP (CrewAI, Langchain)
- Alternative to Anthropic for some features

## Optional Configuration

### N8N Integration

For deploying workflows to a real N8N instance:

```env
N8N_API_KEY=your_n8n_api_key
N8N_BASE_URL=http://localhost:5678
```

**Get N8N API Key**:
1. Open N8N instance settings
2. Go to "API" section
3. Generate new API key

### GitHub Integration

For agent builder GitHub operations:

```env
GITHUB_TOKEN=ghp_YOUR_GITHUB_PAT
```

**Get GitHub Token**:
1. Go to https://github.com/settings/tokens
2. Generate new token (classic)
3. Select scopes: `repo`, `workflow`

### Composio Integration

For advanced agent integrations:

```env
COMPOSIO_API_KEY=your_composio_key
```

**Get Composio Key**: https://app.composio.dev/

## Server Configuration

### Port Configuration

By default, servers use these ports:
- Master Orchestrator: 7860
- N8N Automation: 7862
- Agent Builder: 7863
- Local Control: 7864

**Change Ports** (Advanced):

Edit the server files:
```python
# In backend/main.py (Master Orchestrator)
demo.launch(server_port=7860)  # Change this

# In backend/mcp_servers/*/server.py
demo.launch(server_port=7862)  # Change this
```

### Logging Configuration

Logs are stored in `backend/logs/` by default.

**Configure Log Levels**:

Edit server files to adjust loguru settings:
```python
from loguru import logger

# Change rotation and retention
logger.add(
    "logs/server.log",
    rotation="1 day",    # Rotate daily
    retention="7 days",  # Keep for 7 days
    level="INFO"         # Change to DEBUG for more detail
)
```

### Server Sharing (External Access)

**Enable Public Sharing** (Development Only):

Edit server launch commands:
```python
demo.launch(
    server_port=7860,
    share=True  # Creates public Gradio link
)
```

**⚠️ Security Warning**: Only use `share=True` for development/testing!

## Running Without API Keys

The system supports graceful degradation without API keys:

### What Works Without Keys
- ✅ All Gradio UIs load and display
- ✅ Basic routing via keyword matching
- ✅ Template-based workflows
- ✅ System information display
- ✅ File operations UI
- ✅ Manual agent configuration

### What Requires API Keys
- ❌ AI-powered intent analysis
- ❌ Natural language workflow generation
- ❌ AI-based agent creation
- ❌ Intelligent multi-MCP orchestration

### Fallback Behavior

When API keys are missing:
```
🔍 Request: "Create a workflow"
↓
Master Orchestrator checks for API key
↓
No key found → Falls back to keyword matching
↓
Routes based on keywords: "workflow" → N8N MCP
↓
N8N MCP provides template instead of AI generation
```

## Docker Configuration

### Using Environment File with Docker

```bash
# docker-compose reads .env automatically
docker-compose up -d

# Or specify environment file
docker-compose --env-file .env.production up -d
```

### Docker Environment Variables

```yaml
# docker-compose.yml
services:
  orchestrator:
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
```

### Docker Secrets (Production)

```bash
# Create Docker secrets
echo "sk-ant-api03-..." | docker secret create anthropic_key -

# Use in docker-compose.yml
services:
  orchestrator:
    secrets:
      - anthropic_key
```

## Security Best Practices

### 1. Never Commit API Keys

```bash
# Ensure .env is in .gitignore
echo ".env" >> .gitignore

# Check what's being committed
git status
git diff
```

### 2. Use Different Keys for Different Environments

```env
# .env.development
ANTHROPIC_API_KEY=sk-ant-test-key

# .env.production
ANTHROPIC_API_KEY=sk-ant-prod-key
```

### 3. Rotate Keys Regularly

- Rotate Anthropic keys every 90 days
- Rotate GitHub tokens every 180 days
- Use key management service for production

### 4. Limit Key Permissions

- Use read-only keys when possible
- Limit scope of GitHub tokens
- Use separate keys per service

## Advanced Configuration

### Memory Configuration

**Configure context memory** (in `backend/memory.py`):

```python
class MemoryManager:
    def __init__(self, max_context_length=10):
        self.max_context_length = max_context_length  # Change this
```

### Orchestrator Routing

**Configure keyword routing** (in `backend/orchestrator.py`):

```python
mcp_servers = {
    "n8n": {
        "url": "http://localhost:7862",
        "keywords": ["workflow", "n8n", "automation"],  # Add keywords
    }
}
```

### Performance Tuning

**Gradio Queue Configuration**:

```python
demo.launch(
    server_port=7860,
    max_threads=40,  # Increase for more concurrent users
)
```

**Memory Limits**:

```python
# Limit context history
memory_manager = MemoryManager(max_context_length=5)
```

## Environment-Specific Configurations

### Development

```env
# .env.development
ANTHROPIC_API_KEY=sk-ant-dev-key
DEBUG=true
LOG_LEVEL=DEBUG
```

### Staging

```env
# .env.staging
ANTHROPIC_API_KEY=sk-ant-staging-key
DEBUG=false
LOG_LEVEL=INFO
```

### Production

```env
# .env.production
ANTHROPIC_API_KEY=sk-ant-prod-key
DEBUG=false
LOG_LEVEL=WARNING
SENTRY_DSN=https://your-sentry-dsn
```

## Configuration Validation

### Check Configuration

```bash
# Test environment loading
python -c "
from dotenv import load_dotenv
import os
load_dotenv()
print('✅ ANTHROPIC_API_KEY:', 'Set' if os.getenv('ANTHROPIC_API_KEY') else '❌ Missing')
print('✅ OPENAI_API_KEY:', 'Set' if os.getenv('OPENAI_API_KEY') else '❌ Missing')
"
```

### Verify API Keys Work

```bash
# Test Anthropic API
python -c "
from anthropic import Anthropic
import os
from dotenv import load_dotenv
load_dotenv()
client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
print('✅ Anthropic API key is valid')
"
```

## Troubleshooting Configuration

### API Key Not Loading

```bash
# Check file exists
ls -la .env

# Verify format (no spaces around =)
cat .env | grep API_KEY

# Check for hidden characters
cat -A .env
```

### Wrong Key Format

```bash
# Anthropic keys start with: sk-ant-api03-
# OpenAI keys start with: sk-
# GitHub tokens start with: ghp_ or gh_
```

### Environment Not Loading in Docker

```bash
# Check docker-compose.yml has env_file
docker-compose config

# Verify environment in container
docker exec mcp-orchestrator env | grep API_KEY
```

## Next Steps

- [Installation Guide](installation.md)
- [User Guide](user-guide.md)
- [Troubleshooting Guide](troubleshooting.md)
- [API Documentation](../api/rest-api.md)

## Additional Resources

- [Anthropic API Documentation](https://docs.anthropic.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [N8N API Documentation](https://docs.n8n.io/api/)
- [Environment Variables Best Practices](https://12factor.net/config)
