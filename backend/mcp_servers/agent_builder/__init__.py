"""
Agent Builder MCP Server
=======================

Multi-framework AI agent builder supporting:
- ADK (AI Development Kit)
- CrewAI (Multi-agent orchestration)
- A2A (Agent-to-Agent protocol)
- Langbase (Memory & RAG)
- AGUI (Agent GUI interface)
"""

from .server import AgentBuilderMCP

__all__ = ['AgentBuilderMCP']
__version__ = '1.0.0'
