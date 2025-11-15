# 🦖 Agent Builder MCP Server

## Purpose
Universal AI agent builder that supports multiple frameworks in a single interface. Create, configure, and deploy agents using ADK, CrewAI, A2A, Langbase, or AGUI without learning each framework's API.

## What's Inside This Folder

```
agent_builder/
├── __init__.py          # Package initialization
├── README.md           # This file - explains everything
├── server.py           # Main MCP server with Gradio UI
├── adk_integration.py  # AI Development Kit wrapper
├── crewai_integration.py # CrewAI multi-agent system
├── a2a_protocol.py     # Agent-to-Agent communication
├── langbase_integration.py # Memory & RAG system
└── agui_integration.py # Agent GUI generator
```

## Features

### 🛐️ Supported Frameworks

1. **ADK (AI Development Kit)**
   - Create agents with rich toolkits
   - Custom reasoning engines
   - Production-ready deployment

2. **CrewAI** 
   - Multi-agent crews with roles
   - Task assignment & delegation
   - Collaborative problem-solving

3. **A2A (Agent-to-Agent)**
   - Inter-agent communication
   - Message passing protocols
   - Agent swarm coordination

4. **Langbase**
   - Long-term memory
   - RAG (Retrieval Augmented Generation)
   - Knowledge base integration

5. **AGUI (Agent GUI)**
   - Auto-generate interfaces
   - Chat-based interaction
   - Visual agent control

## Dependencies

See `backend/requirements.txt`:
```
langchain>=0.1.0
crewai>=0.1.0
a