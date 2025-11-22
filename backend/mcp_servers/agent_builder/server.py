#!/usr/bin/env python3
"""
Agent Builder MCP Server
Multi-framework AI agent creation (ADK, CrewAI, A2A, Langbase, AGUI)
Port: 7863
"""
import json
import os

import gradio as gr
from a2a_protocol import A2AProtocol
from adk_integration import ADKIntegration
from agui_interface import AGUIInterface
from crewai_wrapper import CrewAIWrapper
from dotenv import load_dotenv
from langbase_connector import LangbaseConnector
from loguru import logger

# Load environment variables
load_dotenv()

# Configure logging
logger.add("../../logs/agent_builder.log", rotation="1 day", retention="7 days")


class AgentBuilderMCP:
    """Agent Builder MCP - Create agents across multiple frameworks"""

    def __init__(self):
        self.agents = {}  # Store created agents

        # Initialize framework integrations
        self.adk = ADKIntegration()
        self.a2a = A2AProtocol()
        self.crewai = CrewAIWrapper()
        self.langbase = LangbaseConnector()
        self.agui = AGUIInterface()

        logger.info("🤖 Agent Builder MCP initialized with all frameworks")

    # === ADK Agent ===
    def create_adk_agent(self, name, tools, model, system_prompt):
        """Create an ADK agent"""
        try:
            capabilities = tools.split(",") if tools else []

            result = self.adk.create_agent(
                name=name,
                description=system_prompt or f"ADK agent: {name}",
                model=model,
                capabilities=capabilities,
            )

            if result.get("success"):
                agent_config = result["agent"]
                self.agents[agent_config["agent_id"]] = agent_config
                logger.info(f"✅ Created ADK agent: {agent_config['agent_id']}")
                return json.dumps(agent_config, indent=2)
            else:
                return f"Error: {result.get('error', 'Unknown error')}"

        except Exception as e:
            logger.error(f"❌ ADK agent creation failed: {e}")
            return f"Error: {str(e)}"

    # === CrewAI Team ===
    def create_crewai_team(self, team_name, agents_json, tasks_json):
        """Create a CrewAI agent team"""
        try:
            # Parse JSON inputs
            agents_list = json.loads(agents_json) if agents_json else []
            tasks_list = json.loads(tasks_json) if tasks_json else []

            # Build agents
            agents = []
            for agent_data in agents_list:
                agent_result = self.crewai.create_agent(
                    role=agent_data.get("role", "agent"),
                    goal=agent_data.get("goal", ""),
                    backstory=agent_data.get("backstory", "AI agent"),
                    tools=agent_data.get("tools", []),
                )
                if agent_result.get("success"):
                    agents.append(agent_result["agent"])

            # Build tasks
            tasks = []
            for task_data in tasks_list:
                task_result = self.crewai.create_task(
                    description=task_data.get("description", ""),
                    expected_output=task_data.get("expected_output", ""),
                    agent_role=task_data.get("agent", ""),
                )
                if task_result.get("success"):
                    tasks.append(task_result["task"])

            # Create crew
            result = self.crewai.create_crew(
                name=team_name, agents=agents, tasks=tasks, process="sequential"
            )

            if result.get("success"):
                crew_config = result["crew"]
                crew_id = crew_config["crew_id"]
                self.agents[crew_id] = crew_config
                logger.info(f"✅ Created CrewAI team: {crew_id}")
                return json.dumps(crew_config, indent=2)
            else:
                return f"Error: {result.get('error', 'Unknown error')}"

        except Exception as e:
            logger.error(f"❌ CrewAI team creation failed: {e}")
            return f"Error: {str(e)}"

    # === A2A Protocol ===
    def create_a2a_agent(self, agent_name, protocol_version, endpoints):
        """Create an Agent-to-Agent protocol agent"""
        try:
            capabilities = ["messaging", "coordination"]
            endpoint_list = endpoints.split(",") if endpoints else []
            agent_id = f"a2a_{agent_name}"

            agent_config = {
                "name": agent_name,
                "capabilities": capabilities,
                "endpoint": (
                    endpoint_list[0] if endpoint_list else "http://localhost:8000"
                ),
                "protocol_version": protocol_version,
            }

            result = self.a2a.register_agent(
                agent_id=agent_id, agent_config=agent_config
            )

            if result.get("success"):
                registered_agent = result["agent"]
                self.agents[agent_id] = registered_agent
                logger.info(f"✅ Created A2A agent: {agent_id}")
                return json.dumps(registered_agent, indent=2)
            else:
                return f"Error: {result.get('error', 'Unknown error')}"

        except Exception as e:
            logger.error(f"❌ A2A agent creation failed: {e}")
            return f"Error: {str(e)}"

    # === Langbase RAG ===
    def create_langbase_agent(self, agent_name, memory_type, documents):
        """Create a Langbase memory-enabled agent"""
        try:
            # Create memory store
            store_name = agent_name
            store_result = self.langbase.create_memory_store(
                name=store_name, embedding_model="text-embedding-ada-002"
            )

            if not store_result.get("success"):
                return f"Error: {store_result.get('error', 'Unknown error')}"

            # Add documents to memory
            doc_list = documents.split(",") if documents else []
            for doc in doc_list:
                self.langbase.add_memory(
                    store_name=store_name,
                    content=f"Document: {doc}",
                    metadata={"source": doc},
                )

            agent_config = {
                "agent_id": f"langbase_{agent_name}",
                "name": agent_name,
                "memory_store": store_name,
                "memory_type": memory_type,
                "documents": doc_list,
                "type": "Langbase",
            }

            self.agents[agent_config["agent_id"]] = agent_config
            logger.info(f"✅ Created Langbase agent: {agent_config['agent_id']}")

            return json.dumps(agent_config, indent=2)

        except Exception as e:
            logger.error(f"❌ Langbase agent creation failed: {e}")
            return f"Error: {str(e)}"

    # === AGUI Interface ===
    def create_agui_agent(self, agent_name, ui_components, theme):
        """Create an AGUI visual interface agent"""
        try:
            agent_id = f"agui_{agent_name}"

            # Determine layout from components
            components = ui_components.split(",") if ui_components else []
            layout = "chat" if "chat" in components else "dashboard"

            result = self.agui.create_interface(
                name=agent_name, agent_id=agent_id, layout=layout, theme=theme
            )

            if result.get("success"):
                interface_config = result["interface"]
                agent_config = {
                    "agent_id": agent_id,
                    "name": agent_name,
                    "type": "AGUI",
                    "interface": interface_config,
                    "components": components,
                }

                self.agents[agent_id] = agent_config
                logger.info(f"✅ Created AGUI agent: {agent_id}")
                return json.dumps(agent_config, indent=2)
            else:
                return f"Error: {result.get('error', 'Unknown error')}"

        except Exception as e:
            logger.error(f"❌ AGUI agent creation failed: {e}")
            return f"Error: {str(e)}"

    # === List Agents ===
    def list_agents(self):
        """List all created agents"""
        if not self.agents:
            return "No agents created yet."

        return json.dumps(list(self.agents.values()), indent=2)

    def process(self, user_input: str) -> str:
        """
        Process natural language request (called by Orchestrator)
        """
        try:
            text = user_input.lower()

            if "list" in text and "agent" in text:
                return self.list_agents()

            elif "create" in text and "adk" in text:
                name = "new_agent"
                if "named " in text:
                    name = text.split("named ")[1].split()[0]
                return self.create_adk_agent(name, "github,search", "gpt-4", f"You are {name}")

            elif "create" in text and ("crew" in text or "team" in text):
                name = "dev_team"
                if "named " in text:
                    name = text.split("named ")[1].split()[0]
                return self.create_crewai_team(name, '[]', '[]')

            elif "create" in text and "a2a" in text:
                return self.create_a2a_agent("connector_bot", "v2", "http://localhost:8000")

            elif "create" in text and "langbase" in text:
                return self.create_langbase_agent("memory_bot", "chromadb", "readme.md")

            else:
                return "Available commands: List agents, Create ADK agent, Create CrewAI team, Create A2A agent, Create Langbase agent"

        except Exception as e:
            return f"Error: {str(e)}"


def create_ui():
    """Create the Gradio UI"""

    mcp = AgentBuilderMCP()

    with gr.Blocks(theme=gr.themes.Soft(), title="Agent Builder MCP") as demo:
        gr.Markdown(
            """
        # 🤖 Agent Builder MCP
        **Multi-framework AI agent creation platform**
        
        Supports: ADK, CrewAI, A2A Protocol, Langbase, AGUI
        """
        )

        with gr.Tab("🔧 ADK Agent"):
            gr.Markdown("### Create AI Development Kit (ADK) Agent")
            adk_name = gr.Textbox(label="Agent Name", placeholder="my_assistant")
            adk_tools = gr.Textbox(
                label="Tools (comma-separated)", placeholder="github,slack,gmail"
            )
            adk_model = gr.Dropdown(
                choices=["gpt-4", "gpt-3.5-turbo", "claude-3-opus", "claude-3-sonnet"],
                label="Model",
                value="gpt-4",
            )
            adk_prompt = gr.Textbox(
                label="System Prompt",
                placeholder="You are a helpful coding assistant...",
                lines=3,
            )
            adk_btn = gr.Button("Create ADK Agent", variant="primary")
            adk_output = gr.Code(label="Agent Configuration", language="json")

            adk_btn.click(
                mcp.create_adk_agent,
                inputs=[adk_name, adk_tools, adk_model, adk_prompt],
                outputs=adk_output,
            )

        with gr.Tab("👥 CrewAI Team"):
            gr.Markdown("### Create Multi-Agent CrewAI Team")
            crew_name = gr.Textbox(label="Team Name", placeholder="dev_team")
            crew_agents = gr.Code(
                label="Agents JSON",
                value='[{"role":"developer","goal":"Write code"},{"role":"reviewer","goal":"Review code"}]',
                language="json",
                lines=5,
            )
            crew_tasks = gr.Code(
                label="Tasks JSON",
                value='[{"description":"Implement feature","agent":"developer"},{"description":"Review PR","agent":"reviewer"}]',
                language="json",
                lines=5,
            )
            crew_btn = gr.Button("Create CrewAI Team", variant="primary")
            crew_output = gr.Code(label="Team Configuration", language="json")

            crew_btn.click(
                mcp.create_crewai_team,
                inputs=[crew_name, crew_agents, crew_tasks],
                outputs=crew_output,
            )

        with gr.Tab("🔗 A2A Protocol"):
            gr.Markdown("### Create Agent-to-Agent Communication Agent")
            a2a_name = gr.Textbox(label="Agent Name", placeholder="integration_agent")
            a2a_version = gr.Dropdown(
                choices=["v1", "v2", "v3"], label="Protocol Version", value="v2"
            )
            a2a_endpoints = gr.Textbox(
                label="Endpoints (comma-separated)",
                placeholder="http://agent1:8000,http://agent2:8001",
            )
            a2a_btn = gr.Button("Create A2A Agent", variant="primary")
            a2a_output = gr.Code(label="Agent Configuration", language="json")

            a2a_btn.click(
                mcp.create_a2a_agent,
                inputs=[a2a_name, a2a_version, a2a_endpoints],
                outputs=a2a_output,
            )

        with gr.Tab("🧠 Langbase RAG"):
            gr.Markdown("### Create Langbase Memory Agent")
            lang_name = gr.Textbox(label="Agent Name", placeholder="knowledge_bot")
            lang_memory = gr.Dropdown(
                choices=["chromadb", "pinecone", "weaviate", "qdrant"],
                label="Memory Type",
                value="chromadb",
            )
            lang_docs = gr.Textbox(
                label="Documents (comma-separated)",
                placeholder="docs.pdf,knowledge.txt,data.csv",
            )
            lang_btn = gr.Button("Create Langbase Agent", variant="primary")
            lang_output = gr.Code(label="Agent Configuration", language="json")

            lang_btn.click(
                mcp.create_langbase_agent,
                inputs=[lang_name, lang_memory, lang_docs],
                outputs=lang_output,
            )

        with gr.Tab("🎨 AGUI Interface"):
            gr.Markdown("### Create AGUI Visual Agent")
            agui_name = gr.Textbox(label="Agent Name", placeholder="dashboard_agent")
            agui_components = gr.Textbox(
                label="UI Components (comma-separated)",
                placeholder="chat,graph,table,upload",
            )
            agui_theme = gr.Dropdown(
                choices=["light", "dark", "soft", "monochrome"],
                label="Theme",
                value="soft",
            )
            agui_btn = gr.Button("Create AGUI Agent", variant="primary")
            agui_output = gr.Code(label="Agent Configuration", language="json")

            agui_btn.click(
                mcp.create_agui_agent,
                inputs=[agui_name, agui_components, agui_theme],
                outputs=agui_output,
            )

        with gr.Tab("📋 List Agents"):
            gr.Markdown("### All Created Agents")
            list_btn = gr.Button("Refresh List", variant="secondary")
            list_output = gr.Code(label="Agents", language="json", lines=20)

            list_btn.click(mcp.list_agents, inputs=[], outputs=list_output)

    return demo


def main():
    """Launch the Agent Builder MCP server"""
    logger.info("🚀 Starting Agent Builder MCP...")

    demo = create_ui()

    logger.info("✅ Agent Builder MCP ready")
    print("\n" + "=" * 60)
    print("[OK] Agent Builder MCP Running")
    print("[WEB] Access at: http://localhost:7863")
    print("[MCP] Type: Agent Builder (Multi-framework)")
    print("=" * 60 + "\n")

    demo.launch(server_name="0.0.0.0", server_port=7863, share=False)


if __name__ == "__main__":
    main()
