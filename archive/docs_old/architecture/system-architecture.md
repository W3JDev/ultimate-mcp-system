# 🏗️ System Architecture

Deep dive into the Ultimate MCP System architecture and design decisions.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interfaces                          │
│  (Web Browser, CLI, API Clients, Claude Desktop)           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│           Master Orchestrator (Port 7860)                   │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  • FastAPI HTTP Server                                │ │
│  │  • AI-Powered Intent Analysis (Anthropic Claude)      │ │
│  │  • Keyword-Based Fallback Routing                     │ │
│  │  • Context Memory Management                          │ │
│  │  • Request/Response Coordination                      │ │
│  └───────────────────────────────────────────────────────┘ │
└────────────┬────────────┬────────────┬────────────┬─────────┘
             │            │            │            │
    ┌────────▼──┐  ┌─────▼────┐  ┌───▼──────┐  ┌──▼──────────┐
    │  N8N MCP  │  │Agent MCP │  │Local MCP │  │ Cloud MCP   │
    │ Port 7862 │  │Port 7863 │  │Port 7864 │  │   (TBD)     │
    └───────────┘  └──────────┘  └──────────┘  └─────────────┘
         │              │              │
         ▼              ▼              ▼
┌─────────────┐  ┌──────────────┐  ┌──────────────┐
│N8N Instance │  │Agent Runtime │  │System Kernel │
│External API │  │Multi-Framework│  │ OS Commands  │
└─────────────┘  └──────────────┘  └──────────────┘
```

## Core Components

### 1. Master Orchestrator

**Purpose**: Central routing hub that directs user requests to appropriate MCP servers

**Technology Stack**:
- FastAPI (Web framework)
- Anthropic Claude API (AI-powered routing)
- Gradio (Web UI)
- Loguru (Logging)

**Key Responsibilities**:
- Receive and parse user requests
- Analyze intent using AI or keywords
- Route to appropriate MCP server
- Maintain conversation context
- Aggregate and return responses

**Files**:
- `backend/main.py` - FastAPI server and Gradio UI
- `backend/orchestrator.py` - Routing logic
- `backend/memory.py` - Context management

**Port**: 7860

**API Endpoints**:
- `POST /api/process` - Process user request
- `GET /api/memory` - Get conversation context
- `GET /health` - Health check

### 2. N8N Automation MCP

**Purpose**: AI-powered workflow creation and N8N deployment

**Technology Stack**:
- Gradio (6-tab UI)
- Anthropic Claude (Workflow generation)
- N8N API Client
- PyYAML (Config management)

**Key Responsibilities**:
- Generate N8N workflows from natural language
- Provide workflow templates
- Test workflow logic
- Deploy to N8N instance
- Manage workflow configurations

**Files**:
- `backend/mcp_servers/n8n_automation/server.py` - Main server
- `backend/mcp_servers/n8n_automation/workflow_builder.py` - Generation logic
- `backend/mcp_servers/n8n_automation/deployer.py` - N8N API client
- `backend/mcp_servers/n8n_automation/workflow_tester.py` - Testing logic

**Port**: 7862

**Tabs**:
1. Workflow Builder - Generate from description
2. Deploy - Deploy to N8N
3. Templates - Pre-built workflows
4. Test - Test workflow logic
5. History - Previous workflows
6. Settings - N8N configuration

### 3. Agent Builder MCP

**Purpose**: Multi-framework AI agent creation and management

**Technology Stack**:
- Gradio (6-tab UI)
- Multiple agent frameworks:
  - ADK (AI Development Kit)
  - CrewAI (Multi-agent teams)
  - A2A (Agent-to-Agent)
  - Langbase (RAG & memory)
  - AGUI (Agent GUIs)
- JSON storage

**Key Responsibilities**:
- Create agents across multiple frameworks
- Manage agent configurations
- Test agent responses
- Store and retrieve agents
- Handle framework-specific requirements

**Files**:
- `backend/mcp_servers/agent_builder/server.py` - Main server with UI
- `backend/mcp_servers/agent_builder/agents/` - Agent storage (JSON)

**Port**: 7863

**Tabs**:
1. ADK Agent - AI Development Kit agents
2. CrewAI - Multi-agent teams
3. A2A - Agent communication
4. Langbase - RAG agents
5. AGUI - GUI agents
6. Management - CRUD operations

### 4. Local Control MCP

**Purpose**: System automation and local PC control

**Technology Stack**:
- Gradio (6-tab UI)
- psutil (System information)
- pyautogui (Input control)
- Playwright (Browser automation)
- os, subprocess (System commands)

**Key Responsibilities**:
- Execute system commands
- Manage processes
- Control keyboard/mouse input
- Automate browser tasks
- File system operations
- Display system information

**Files**:
- `backend/mcp_servers/local_control/server.py` - Complete implementation

**Port**: 7864

**Tabs**:
1. System Commands - OS commands
2. Process Manager - Process control
3. File Operations - File system
4. Input Control - Keyboard/mouse
5. Browser Automation - Playwright
6. System Info - Monitoring

## Design Patterns

### 1. Microservices Architecture

Each MCP server is an independent service:
- Separate process and port
- Independent failure isolation
- Horizontal scaling capability
- Technology diversity

**Benefits**:
- Fault isolation
- Independent deployment
- Technology flexibility
- Clear boundaries

### 2. Hub-and-Spoke Pattern

Master Orchestrator (hub) coordinates MCP servers (spokes):

```
        N8N ◄─────┐
                   │
Agent Builder ◄────┤──── Master Orchestrator
                   │
Local Control ◄────┘
```

**Benefits**:
- Centralized routing
- Single entry point
- Simplified client interaction
- Context management

### 3. Graceful Degradation

System works without API keys through fallback logic:

```python
if anthropic_api_key:
    response = ai_powered_routing(request)
else:
    response = keyword_based_routing(request)
```

**Benefits**:
- Always operational
- Progressive enhancement
- Development without keys
- Cost control

### 4. UI-First Design

Every MCP has a Gradio interface:
- Visual interaction
- Testing without API calls
- Development debugging
- User-friendly

## Data Flow

### Request Processing Flow

```
1. User sends request
   ↓
2. Master Orchestrator receives
   ↓
3. Intent analysis (AI or keywords)
   ↓
4. Route to appropriate MCP
   ↓
5. MCP processes request
   ↓
6. MCP returns response
   ↓
7. Orchestrator aggregates
   ↓
8. Return to user
```

### Context Management Flow

```
1. User message received
   ↓
2. Memory Manager stores in context
   ↓
3. Context sent with routing decision
   ↓
4. MCP receives message + context
   ↓
5. MCP response stored in context
   ↓
6. Context available for next request
```

## Technology Decisions

### Why FastAPI?

- Modern Python web framework
- Automatic API documentation
- Type hints and validation
- High performance
- WebSocket support

### Why Gradio?

- Rapid UI development
- Python-native
- Auto-generated interfaces
- Built-in sharing capabilities
- Beautiful, responsive UIs

### Why Multiple Frameworks?

Agent Builder supports 5+ frameworks:
- **Market coverage**: Reach more users
- **Best tool for job**: Different frameworks excel at different tasks
- **Future-proofing**: Adapt to ecosystem changes
- **Learning**: Show patterns across frameworks

### Why Independent Servers?

- **Isolation**: Failure in one doesn't affect others
- **Scaling**: Scale busy servers independently
- **Development**: Work on one without affecting others
- **Deployment**: Deploy changes to specific servers

## Scalability Considerations

### Current Limitations

- Single-process per server
- In-memory context storage
- No load balancing
- No horizontal scaling

### Future Enhancements

**Horizontal Scaling**:
```
         ┌─ Orchestrator 1
Load     ├─ Orchestrator 2
Balancer ├─ Orchestrator 3
         └─ Orchestrator 4
```

**Shared State**:
- Redis for context storage
- PostgreSQL for persistent data
- Message queue (RabbitMQ/Redis)

**Service Mesh**:
- Kubernetes deployment
- Service discovery
- Health checks
- Auto-scaling

## Security Architecture

### Current State (Development)

- No authentication
- No authorization
- Local-only access
- Trust-based

### Production Requirements

**Authentication**:
- JWT tokens
- API keys per user
- OAuth 2.0 integration

**Authorization**:
- Role-based access control
- Per-MCP permissions
- Command whitelisting

**Network Security**:
- HTTPS/TLS only
- Rate limiting
- IP whitelisting
- WAF integration

**Secrets Management**:
- Vault integration
- Encrypted environment variables
- Key rotation

## Monitoring & Observability

### Logging Architecture

**Current**:
```
Each server → Local log file (backend/logs/)
```

**Production**:
```
Each server → Structured logs → Log aggregator (ELK/Splunk)
```

### Metrics (Proposed)

- Request count per MCP
- Response times
- Error rates
- API key usage
- Memory consumption
- CPU utilization

### Tracing (Proposed)

Distributed tracing with OpenTelemetry:
```
User Request → Orchestrator → MCP → External API
     │              │           │         │
     └──────────── Trace ID ────┴─────────┘
```

## Deployment Architecture

### Development

```
Local Machine
├── Python venv
├── 4 Python processes
└── SQLite (future)
```

### Docker Deployment

```
Docker Host
├── mcp-orchestrator container
├── mcp-n8n container
├── mcp-agent-builder container
├── mcp-local-control container
└── Shared volumes (logs, memory)
```

### Cloud Deployment

```
Cloud Run / AWS ECS
├── Orchestrator service
├── N8N MCP service
├── Agent Builder service
├── Local Control service
├── PostgreSQL (managed)
└── Redis (managed)
```

## Performance Characteristics

### Latency

- **Orchestrator routing**: <100ms (no AI), <2s (with AI)
- **Workflow generation**: 3-10s (AI-powered)
- **Agent creation**: 1-5s
- **System commands**: <1s

### Throughput

Current (single instance):
- 10-20 requests/second (orchestrator)
- 5-10 workflows/minute (generation)
- 20-50 agents/minute (creation)

Scalable to:
- 100+ requests/second (with load balancing)
- 50+ workflows/minute (parallel processing)
- 200+ agents/minute (distributed)

## Future Architecture Evolution

### Phase 1: True MCP Protocol

Replace HTTP/REST with MCP protocol:
- JSON-RPC 2.0
- stdio/SSE transport
- Standard tool registration
- Claude Desktop integration

### Phase 2: Event-Driven

Move to event-driven architecture:
- Message broker (RabbitMQ/Kafka)
- Async processing
- Event sourcing
- CQRS pattern

### Phase 3: Distributed

Full distributed system:
- Service mesh
- API gateway
- Circuit breakers
- Distributed tracing

## Related Documentation

- [MCP Servers Details](mcp-servers.md)
- [Orchestration Flow](orchestration-flow.md)
- [Deployment Guide](../../DEPLOYMENT.md)
- [API Reference](../api/rest-api.md)
