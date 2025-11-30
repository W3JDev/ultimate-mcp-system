# 🔧 MCP Servers Details

In-depth documentation for each MCP server in the Ultimate MCP System.

## Overview

The system consists of 4 independent MCP servers, each specialized for a specific domain:

| Server | Port | Purpose | Status |
|--------|------|---------|--------|
| Master Orchestrator | 7860 | Request routing & coordination | ✅ Active |
| N8N Automation MCP | 7862 | Workflow creation & deployment | ✅ Active |
| Agent Builder MCP | 7863 | Multi-framework agent creation | ✅ Active |
| Local Control MCP | 7864 | System automation & control | ✅ Active |

---

## Master Orchestrator

### Technical Details

**File**: `backend/main.py`, `backend/orchestrator.py`  
**Port**: 7860  
**Framework**: FastAPI + Gradio  
**Dependencies**: Anthropic API, loguru

### Architecture

```python
FastAPI App
    ├── /api/process (POST) - Main request handler
    ├── /api/memory (GET) - Context retrieval
    ├── /health (GET) - Health check
    └── Gradio UI - Web interface

Orchestrator Class
    ├── AI-Powered Routing (Anthropic Claude)
    ├── Keyword-Based Fallback
    ├── Memory Manager Integration
    └── MCP Server Registry
```

### Routing Logic

#### AI-Powered Routing (with API key)
```python
def route_request(self, message: str) -> str:
    # 1. Analyze message with Claude
    analysis = self.ai_client.analyze(message)
    
    # 2. Determine intent
    intent = analysis.get('intent')
    
    # 3. Route to appropriate MCP
    if intent == 'workflow':
        return 'n8n'
    elif intent == 'agent':
        return 'agent_builder'
    elif intent == 'system':
        return 'local_control'
```

#### Keyword Fallback (without API key)
```python
def route_by_keywords(self, message: str) -> str:
    keywords = {
        'n8n': ['workflow', 'automation', 'n8n', 'deploy'],
        'agent_builder': ['agent', 'AI', 'crewai', 'adk'],
        'local_control': ['system', 'command', 'browser', 'file']
    }
    
    # Match keywords to server
    for server, words in keywords.items():
        if any(word in message.lower() for word in words):
            return server
    
    return 'n8n'  # Default
```

### Memory Management

**File**: `backend/memory.py`

```python
class MemoryManager:
    def __init__(self, max_context_length=10):
        self.context = []
        self.max_context_length = max_context_length
    
    def add_message(self, role: str, content: str):
        """Add message to context with timestamp"""
        self.context.append({
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        })
        
        # Keep only last N messages
        if len(self.context) > self.max_context_length:
            self.context = self.context[-self.max_context_length:]
    
    def get_context(self) -> List[Dict]:
        """Retrieve conversation context"""
        return self.context
```

### Configuration

**MCP Server Registry**:
```python
mcp_servers = {
    'n8n': {
        'url': 'http://localhost:7862',
        'keywords': ['workflow', 'n8n', 'automation'],
        'description': 'Workflow automation'
    },
    'agent_builder': {
        'url': 'http://localhost:7863',
        'keywords': ['agent', 'AI', 'crewai'],
        'description': 'Agent creation'
    },
    'local_control': {
        'url': 'http://localhost:7864',
        'keywords': ['system', 'command', 'browser'],
        'description': 'System control'
    }
}
```

---

## N8N Automation MCP

### Technical Details

**File**: `backend/mcp_servers/n8n_automation/server.py`  
**Port**: 7862  
**Framework**: Gradio (6-tab UI)  
**Dependencies**: Anthropic API, N8N API, PyYAML

### Components

#### 1. Workflow Builder
**File**: `workflow_builder.py`

```python
class WorkflowBuilder:
    def generate(self, description: str) -> Dict:
        """Generate N8N workflow from description"""
        
        # AI-powered generation
        if self.has_api_key:
            return self._generate_with_ai(description)
        
        # Template fallback
        return self._generate_from_template(description)
    
    def _generate_with_ai(self, desc: str) -> Dict:
        """Use Claude to generate workflow"""
        prompt = f"""
        Create N8N workflow for: {desc}
        
        Return JSON with:
        - nodes (trigger, actions, conditions)
        - connections between nodes
        - error handling
        """
        response = self.client.messages.create(...)
        return json.loads(response.content[0].text)
```

#### 2. Deployer
**File**: `deployer.py`

```python
class N8NDeployer:
    def deploy(self, workflow: Dict, n8n_url: str, api_key: str):
        """Deploy workflow to N8N instance"""
        
        response = requests.post(
            f"{n8n_url}/api/v1/workflows",
            headers={"X-N8N-API-KEY": api_key},
            json=workflow
        )
        
        if response.status_code == 201:
            return response.json()['id']
        else:
            raise DeploymentError(response.text)
```

#### 3. Workflow Tester
**File**: `workflow_tester.py`

```python
class WorkflowTester:
    def test(self, workflow: Dict, test_data: Dict) -> Dict:
        """Test workflow logic without deployment"""
        
        # Simulate execution
        results = []
        for node in workflow['nodes']:
            result = self._execute_node(node, test_data)
            results.append(result)
        
        return {
            'success': all(r['success'] for r in results),
            'results': results
        }
```

### Workflow Templates

**50+ Pre-built Templates**:
- Email notifications
- Slack/Discord bots
- GitHub automation
- Database synchronization
- API polling
- Webhook handling
- Data transformation
- Error notifications

**Template Structure**:
```json
{
    "name": "Email Notification",
    "description": "Send email on event",
    "nodes": [
        {
            "name": "Webhook",
            "type": "n8n-nodes-base.webhook",
            "parameters": {...}
        },
        {
            "name": "Email",
            "type": "n8n-nodes-base.emailSend",
            "parameters": {...}
        }
    ],
    "connections": {...}
}
```

---

## Agent Builder MCP

### Technical Details

**File**: `backend/mcp_servers/agent_builder/server.py`  
**Port**: 7863  
**Framework**: Gradio (6-tab UI)  
**Storage**: JSON files in `agents/` directory

### Framework Integrations

#### 1. ADK (AI Development Kit)
```python
class ADKAgentBuilder:
    def create_agent(self, config: Dict) -> Agent:
        """Create ADK agent"""
        return Agent(
            name=config['name'],
            model=config['model'],
            tools=config['tools'],
            instructions=config['instructions']
        )
```

#### 2. CrewAI
```python
class CrewAIBuilder:
    def create_crew(self, config: Dict) -> Crew:
        """Create multi-agent crew"""
        agents = [
            Agent(role=role, goal=goal)
            for role, goal in config['agents'].items()
        ]
        
        return Crew(
            agents=agents,
            tasks=config['tasks'],
            process=Process.sequential
        )
```

#### 3. Langbase (RAG)
```python
class LangbaseBuilder:
    def create_rag_agent(self, config: Dict) -> Agent:
        """Create RAG-enabled agent"""
        
        # Create vector store
        vectorstore = Chroma.from_documents(
            documents=config['documents'],
            embedding=OpenAIEmbeddings()
        )
        
        # Create retriever
        retriever = vectorstore.as_retriever()
        
        # Create agent with RAG
        return create_agent(
            llm=config['llm'],
            tools=[retriever],
            memory=ConversationBufferMemory()
        )
```

### Agent Storage

**Format**: JSON files
**Location**: `backend/mcp_servers/agent_builder/agents/`

**Structure**:
```json
{
    "id": "agent_123",
    "name": "Research Assistant",
    "framework": "adk",
    "config": {
        "model": "claude-3-sonnet",
        "tools": ["web_search", "document_reader"],
        "temperature": 0.7,
        "max_tokens": 2000
    },
    "created_at": "2025-11-16T12:00:00Z",
    "updated_at": "2025-11-16T12:00:00Z"
}
```

### CRUD Operations

```python
class AgentManager:
    def create(self, config: Dict) -> str:
        """Create new agent"""
        agent_id = generate_id()
        agent_data = {
            'id': agent_id,
            'created_at': now(),
            **config
        }
        save_to_file(agent_id, agent_data)
        return agent_id
    
    def read(self, agent_id: str) -> Dict:
        """Get agent by ID"""
        return load_from_file(agent_id)
    
    def update(self, agent_id: str, updates: Dict):
        """Update agent configuration"""
        agent = self.read(agent_id)
        agent.update(updates)
        agent['updated_at'] = now()
        save_to_file(agent_id, agent)
    
    def delete(self, agent_id: str):
        """Delete agent"""
        remove_file(agent_id)
    
    def list(self) -> List[Dict]:
        """List all agents"""
        return [load_from_file(f) for f in list_files()]
```

---

## Local Control MCP

### Technical Details

**File**: `backend/mcp_servers/local_control/server.py`  
**Port**: 7864  
**Framework**: Gradio (6-tab UI)  
**Dependencies**: psutil, pyautogui, playwright, os

### Capabilities

#### 1. System Commands
```python
class SystemCommands:
    SAFE_COMMANDS = {
        'system_info': self._get_system_info,
        'list_processes': self._list_processes,
        'disk_usage': self._disk_usage,
        'network_info': self._network_info
    }
    
    def execute(self, command: str) -> str:
        """Execute safe system command"""
        if command in self.SAFE_COMMANDS:
            return self.SAFE_COMMANDS[command]()
        else:
            return self._execute_sandboxed(command)
```

#### 2. Process Management
```python
class ProcessManager:
    def list_processes(self) -> List[Dict]:
        """List all running processes"""
        return [
            {
                'pid': p.pid,
                'name': p.name(),
                'cpu_percent': p.cpu_percent(),
                'memory_percent': p.memory_percent()
            }
            for p in psutil.process_iter()
        ]
    
    def terminate(self, pid: int):
        """Terminate process by PID"""
        process = psutil.Process(pid)
        process.terminate()
```

#### 3. Browser Automation
```python
class BrowserAutomation:
    def __init__(self):
        self.browser = playwright.chromium.launch()
        self.page = self.browser.new_page()
    
    def navigate(self, url: str):
        """Navigate to URL"""
        self.page.goto(url)
    
    def screenshot(self) -> bytes:
        """Take screenshot"""
        return self.page.screenshot()
    
    def click(self, selector: str):
        """Click element"""
        self.page.click(selector)
    
    def type(self, selector: str, text: str):
        """Type text into element"""
        self.page.fill(selector, text)
```

#### 4. File Operations
```python
class FileOperations:
    def read(self, path: str) -> str:
        """Read file contents"""
        with open(path, 'r') as f:
            return f.read()
    
    def write(self, path: str, content: str):
        """Write file contents"""
        with open(path, 'w') as f:
            f.write(content)
    
    def list_directory(self, path: str) -> List[str]:
        """List directory contents"""
        return os.listdir(path)
```

### Security

#### Command Whitelisting
```python
BLOCKED_COMMANDS = [
    'rm -rf /',
    'format',
    'dd if=',
    'chmod 777',
    # ... dangerous commands
]

def is_safe_command(command: str) -> bool:
    """Check if command is safe to execute"""
    return not any(
        blocked in command.lower()
        for blocked in BLOCKED_COMMANDS
    )
```

#### Sandboxing
```python
def execute_sandboxed(command: str) -> str:
    """Execute command in sandboxed environment"""
    
    # Limit execution time
    timeout = 30  # seconds
    
    # Restrict file access
    allowed_paths = ['/tmp', '/home/user']
    
    # Run with limited permissions
    result = subprocess.run(
        command,
        shell=True,
        timeout=timeout,
        capture_output=True,
        cwd=allowed_paths[0]
    )
    
    return result.stdout.decode()
```

---

## Adding New MCP Servers

### Template Structure

```python
# backend/mcp_servers/new_mcp/server.py

import gradio as gr
from loguru import logger

class NewMCP:
    def __init__(self):
        self.logger = logger
        self.logger.add("../../logs/new_mcp.log")
    
    def process(self, user_input: str) -> str:
        """Main processing method"""
        # Your logic here
        return response

def create_ui() -> gr.Blocks:
    """Create Gradio interface"""
    
    with gr.Blocks() as demo:
        gr.Markdown("# New MCP Server")
        
        with gr.Tab("Main"):
            input_box = gr.Textbox(label="Input")
            output_box = gr.Textbox(label="Output")
            btn = gr.Button("Process")
            
            btn.click(
                fn=mcp.process,
                inputs=input_box,
                outputs=output_box
            )
    
    return demo

if __name__ == "__main__":
    mcp = NewMCP()
    demo = create_ui()
    demo.launch(server_port=7865)
```

### Registration

Add to `backend/orchestrator.py`:
```python
mcp_servers = {
    # ... existing servers
    'new_mcp': {
        'url': 'http://localhost:7865',
        'keywords': ['new', 'custom'],
        'description': 'New MCP functionality'
    }
}
```

---

## Related Documentation

- [System Architecture](system-architecture.md)
- [API Reference](../api/rest-api.md)
- [User Guide](../guides/user-guide.md)
- [Development Guide](../guides/development.md)
