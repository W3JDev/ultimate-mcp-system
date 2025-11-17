"""
Agent Builder MCP Tools
Tools for creating agents across multiple frameworks (ADK, CrewAI, A2A, Langbase, AGUI)
"""

import json
from typing import Any, Dict, List

from loguru import logger

from .base import MCPTool, ToolParameter, ToolSchema

# Simple agent storage (in production, would use database)
_agent_store: Dict[str, Dict] = {}


# === Tool: Create ADK Agent ===
def create_adk_agent_handler(
    name: str, model: str, tools: List[str] = None, system_prompt: str = ""
) -> Dict[str, Any]:
    """
    Create an AI Development Kit (ADK) agent

    Args:
        name: Agent name
        model: LLM model to use
        tools: List of tools for the agent
        system_prompt: System prompt for the agent

    Returns:
        Agent configuration
    """
    agent_id = f"adk_{name}_{len(_agent_store)}"

    agent_config = {
        "id": agent_id,
        "type": "ADK",
        "name": name,
        "model": model,
        "tools": tools or [],
        "system_prompt": system_prompt,
        "created_at": "2025-11-16",
    }

    _agent_store[agent_id] = agent_config
    logger.info(f"✅ Created ADK agent: {agent_id}")

    return agent_config


create_adk_agent_tool = MCPTool(
    schema=ToolSchema(
        name="create_adk_agent",
        display_name="Create ADK Agent",
        description="Create an AI Development Kit (ADK) agent with specific tools and model",
        category="agent",
        parameters=[
            ToolParameter(
                name="name", type="string", description="Agent name", required=True
            ),
            ToolParameter(
                name="model",
                type="string",
                description="LLM model (gpt-4, gpt-3.5-turbo, claude-3-opus, claude-3-sonnet)",
                required=True,
                enum=["gpt-4", "gpt-3.5-turbo", "claude-3-opus", "claude-3-sonnet"],
            ),
            ToolParameter(
                name="tools",
                type="array",
                description="List of tool names for the agent",
                required=False,
                default=[],
            ),
            ToolParameter(
                name="system_prompt",
                type="string",
                description="System prompt defining agent behavior",
                required=False,
                default="",
            ),
        ],
        returns="Agent configuration with ID and settings",
        examples=[
            "Create ADK agent named 'coding_assistant' with GPT-4 and GitHub/Slack tools",
            "Build ADK agent for customer support using Claude",
        ],
    ),
    handler=create_adk_agent_handler,
)


# === Tool: Create CrewAI Team ===
def create_crewai_team_handler(
    team_name: str, agents: List[Dict], tasks: List[Dict]
) -> Dict[str, Any]:
    """
    Create a CrewAI multi-agent team

    Args:
        team_name: Name of the team
        agents: List of agent definitions
        tasks: List of task definitions

    Returns:
        Team configuration
    """
    team_id = f"crew_{team_name}_{len(_agent_store)}"

    team_config = {
        "id": team_id,
        "type": "CrewAI",
        "team_name": team_name,
        "agents": agents,
        "tasks": tasks,
        "created_at": "2025-11-16",
    }

    _agent_store[team_id] = team_config
    logger.info(f"✅ Created CrewAI team: {team_id}")

    return team_config


create_crewai_team_tool = MCPTool(
    schema=ToolSchema(
        name="create_crewai_team",
        display_name="Create CrewAI Team",
        description="Create a multi-agent team using CrewAI framework",
        category="agent",
        parameters=[
            ToolParameter(
                name="team_name",
                type="string",
                description="Name of the agent team",
                required=True,
            ),
            ToolParameter(
                name="agents",
                type="array",
                description="Array of agent definitions with roles and goals",
                required=True,
            ),
            ToolParameter(
                name="tasks",
                type="array",
                description="Array of task definitions for the team",
                required=True,
            ),
        ],
        returns="Team configuration with agents and tasks",
        examples=[
            "Create development team with developer, reviewer, and tester agents",
            "Build research team with researcher, analyst, and writer roles",
        ],
    ),
    handler=create_crewai_team_handler,
)


# === Tool: Create A2A Agent ===
def create_a2a_agent_handler(
    agent_name: str, protocol_version: str, endpoints: List[str] = None
) -> Dict[str, Any]:
    """
    Create an Agent-to-Agent (A2A) protocol agent

    Args:
        agent_name: Agent name
        protocol_version: A2A protocol version
        endpoints: List of agent endpoints to communicate with

    Returns:
        Agent configuration
    """
    agent_id = f"a2a_{agent_name}_{len(_agent_store)}"

    agent_config = {
        "id": agent_id,
        "type": "A2A",
        "name": agent_name,
        "protocol_version": protocol_version,
        "endpoints": endpoints or [],
        "created_at": "2025-11-16",
    }

    _agent_store[agent_id] = agent_config
    logger.info(f"✅ Created A2A agent: {agent_id}")

    return agent_config


create_a2a_agent_tool = MCPTool(
    schema=ToolSchema(
        name="create_a2a_agent",
        display_name="Create A2A Agent",
        description="Create an Agent-to-Agent communication protocol agent",
        category="agent",
        parameters=[
            ToolParameter(
                name="agent_name",
                type="string",
                description="Agent name",
                required=True,
            ),
            ToolParameter(
                name="protocol_version",
                type="string",
                description="A2A protocol version",
                required=True,
                enum=["v1", "v2", "v3"],
            ),
            ToolParameter(
                name="endpoints",
                type="array",
                description="List of agent endpoint URLs to communicate with",
                required=False,
                default=[],
            ),
        ],
        returns="Agent configuration with protocol settings",
        examples=[
            "Create A2A integration agent to coordinate multiple services",
            "Build inter-agent communication bridge",
        ],
    ),
    handler=create_a2a_agent_handler,
)


# === Tool: Create Langbase Agent ===
def create_langbase_agent_handler(
    agent_name: str, memory_type: str, documents: List[str] = None
) -> Dict[str, Any]:
    """
    Create a Langbase memory-enabled agent with RAG

    Args:
        agent_name: Agent name
        memory_type: Vector database type
        documents: List of document paths

    Returns:
        Agent configuration
    """
    agent_id = f"langbase_{agent_name}_{len(_agent_store)}"

    agent_config = {
        "id": agent_id,
        "type": "Langbase",
        "name": agent_name,
        "memory_type": memory_type,
        "documents": documents or [],
        "created_at": "2025-11-16",
    }

    _agent_store[agent_id] = agent_config
    logger.info(f"✅ Created Langbase agent: {agent_id}")

    return agent_config


create_langbase_agent_tool = MCPTool(
    schema=ToolSchema(
        name="create_langbase_agent",
        display_name="Create Langbase Agent",
        description="Create a Langbase memory-enabled agent with RAG capabilities",
        category="agent",
        parameters=[
            ToolParameter(
                name="agent_name",
                type="string",
                description="Agent name",
                required=True,
            ),
            ToolParameter(
                name="memory_type",
                type="string",
                description="Vector database type for memory",
                required=True,
                enum=["chromadb", "pinecone", "weaviate", "qdrant"],
            ),
            ToolParameter(
                name="documents",
                type="array",
                description="List of document paths to index",
                required=False,
                default=[],
            ),
        ],
        returns="Agent configuration with memory settings",
        examples=[
            "Create knowledge bot with ChromaDB memory and company docs",
            "Build RAG agent with Pinecone for customer support",
        ],
    ),
    handler=create_langbase_agent_handler,
)


# === Tool: Create AGUI Agent ===
def create_agui_agent_handler(
    agent_name: str, ui_components: List[str], theme: str = "soft"
) -> Dict[str, Any]:
    """
    Create an AGUI visual interface agent

    Args:
        agent_name: Agent name
        ui_components: List of UI components
        theme: UI theme

    Returns:
        Agent configuration
    """
    agent_id = f"agui_{agent_name}_{len(_agent_store)}"

    agent_config = {
        "id": agent_id,
        "type": "AGUI",
        "name": agent_name,
        "ui_components": ui_components,
        "theme": theme,
        "created_at": "2025-11-16",
    }

    _agent_store[agent_id] = agent_config
    logger.info(f"✅ Created AGUI agent: {agent_id}")

    return agent_config


create_agui_agent_tool = MCPTool(
    schema=ToolSchema(
        name="create_agui_agent",
        display_name="Create AGUI Agent",
        description="Create an AGUI visual interface agent with custom components",
        category="agent",
        parameters=[
            ToolParameter(
                name="agent_name",
                type="string",
                description="Agent name",
                required=True,
            ),
            ToolParameter(
                name="ui_components",
                type="array",
                description="List of UI component types",
                required=True,
            ),
            ToolParameter(
                name="theme",
                type="string",
                description="UI theme",
                required=False,
                default="soft",
                enum=["light", "dark", "soft", "monochrome"],
            ),
        ],
        returns="Agent configuration with UI settings",
        examples=[
            "Create dashboard agent with chat, graph, and table components",
            "Build data visualization agent with custom UI",
        ],
    ),
    handler=create_agui_agent_handler,
)


# === Tool: List Agents ===
def list_agents_handler(agent_type: str = None) -> List[Dict[str, Any]]:
    """
    List all created agents

    Args:
        agent_type: Optional filter by agent type

    Returns:
        List of agent configurations
    """
    if agent_type:
        agents = [
            agent for agent in _agent_store.values() if agent.get("type") == agent_type
        ]
    else:
        agents = list(_agent_store.values())

    logger.info(f"📋 Listed {len(agents)} agents")
    return agents


list_agents_tool = MCPTool(
    schema=ToolSchema(
        name="list_agents",
        display_name="List Agents",
        description="List all created agents or filter by type",
        category="agent",
        parameters=[
            ToolParameter(
                name="agent_type",
                type="string",
                description="Filter by agent type",
                required=False,
                enum=["ADK", "CrewAI", "A2A", "Langbase", "AGUI"],
            )
        ],
        returns="List of agent configurations",
        examples=["List all agents", "Show all CrewAI teams", "List ADK agents"],
    ),
    handler=list_agents_handler,
)


# Export all agent tools
AGENT_TOOLS = [
    create_adk_agent_tool,
    create_crewai_team_tool,
    create_a2a_agent_tool,
    create_langbase_agent_tool,
    create_agui_agent_tool,
    list_agents_tool,
]
