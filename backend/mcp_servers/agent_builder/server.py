#!/usr/bin/env python3
"""
Agent Builder MCP Server
Multi-framework AI agent creation (ADK, CrewAI, A2A, Langbase, AGUI)
+ Composio integration for 100+ tools
Port: 7863
"""
import json
import os
import sys
import time
from pathlib import Path

import gradio as gr
from a2a_protocol import A2AProtocol
from adk_integration import ADKIntegration
from agui_interface import AGUIInterface
from crewai_wrapper import CrewAIWrapper
from dotenv import load_dotenv
from langbase_connector import LangbaseConnector
from loguru import logger

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

# Try importing Composio, fallback if not available
try:
    from integrations.composio_integration import ComposioIntegration
    COMPOSIO_AVAILABLE = True
except ImportError as e:
    logger.warning(f"⚠️ Could not import Composio: {e}")
    ComposioIntegration = None
    COMPOSIO_AVAILABLE = False

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
        
        # Initialize Composio integration
        if COMPOSIO_AVAILABLE and ComposioIntegration:
            try:
                self.composio = ComposioIntegration()
                logger.success("✅ Composio integration loaded")
            except Exception as e:
                logger.warning(f"⚠️ Composio not available: {e}")
                self.composio = None
        else:
            logger.warning("⚠️ Composio integration not available")
            self.composio = None
        
        # Initialize Agent Runtime for execution & deployment
        try:
            from agent_runtime import AgentRuntime
            self.runtime = AgentRuntime()
            logger.success("✅ Agent Runtime initialized")
        except Exception as e:
            logger.warning(f"⚠️ Agent Runtime not available: {e}")
            self.runtime = None
        
        # Initialize Database for persistence
        try:
            from agent_database import AgentDatabase
            self.db = AgentDatabase()
            logger.success("✅ Agent Database initialized")
            
            # Load existing agents from database
            saved_agents = self.db.list_agents()
            for agent_data in saved_agents:
                self.agents[agent_data["agent_id"]] = agent_data["config"]
            logger.info(f"📦 Loaded {len(saved_agents)} agents from database")
        except Exception as e:
            logger.warning(f"⚠️ Database not available: {e}")
            self.db = None

        logger.info("🤖 Agent Builder MCP initialized with all frameworks")

    # === ADK Agent ===
    def create_adk_agent(self, name, tools, model, system_prompt):
        """Create an ADK agent with Vertex AI"""
        try:
            capabilities = [c.strip() for c in tools.split(",")] if tools else []

            result = self.adk.create_agent(
                name=name,
                description=system_prompt or f"ADK agent: {name}",
                model=model,
                capabilities=capabilities,
            )

            if result.get("success"):
                agent_config = result["agent"]
                self.agents[agent_config["agent_id"]] = agent_config
                
                # Save to database
                if self.db:
                    self.db.save_agent(agent_config)
                
                logger.info(f"✅ Created ADK agent: {agent_config['agent_id']}")
                return json.dumps(agent_config, indent=2)
            else:
                return f"Error: {result.get('error', 'Unknown error')}"

        except Exception as e:
            logger.error(f"❌ ADK agent creation failed: {e}")
            return f"Error: {str(e)}"
    
    def execute_adk_agent(self, agent_id, user_message):
        """Execute ADK agent with REAL Vertex AI call"""
        try:
            if not agent_id or not user_message:
                return "Error: Please provide both agent ID and message"
            
            result = self.adk.execute_agent(agent_id, user_message)
            
            if result.get("success"):
                response = f"✅ Agent: {result['agent_name']}\n\n"
                response += f"Response:\n{result['response']}\n\n"
                response += f"Model: {result['model']}\n"
                response += f"Tokens: {result['usage']['input_tokens']} in, {result['usage']['output_tokens']} out\n"
                response += f"Conversation length: {result['conversation_length']} messages"
                return response
            else:
                return f"❌ Error: {result.get('error', 'Unknown error')}"
        
        except Exception as e:
            logger.error(f"❌ Agent execution failed: {e}")
            return f"Error: {str(e)}"
    
    def list_adk_agents(self):
        """List all ADK agents"""
        try:
            result = self.adk.list_agents()
            if result.get("success"):
                return result["agents"]
            else:
                return {"error": "Failed to list agents"}
        except Exception as e:
            logger.error(f"❌ Failed to list agents: {e}")
            return {"error": str(e)}

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
    
    # === Agent Testing & Deployment ===
    def test_agent_execution(self, agent_id: str, test_message: str):
        """Test agent execution with real API call"""
        try:
            if not agent_id or not test_message:
                return {"error": "Please provide agent ID and test message"}
            
            # Execute agent
            start_time = time.time()
            result = self.adk.execute_agent(agent_id, test_message)
            execution_time_ms = int((time.time() - start_time) * 1000)
            
            # Log to database
            if self.db and result.get("success"):
                self.db.log_execution(
                    agent_id,
                    test_message,
                    result.get("response", ""),
                    True,
                    execution_time_ms
                )
            
            return result
        except Exception as e:
            logger.error(f"❌ Test execution failed: {e}")
            return {"error": str(e)}
    
    def deploy_agent_to_n8n(self, agent_id: str, n8n_url: str, n8n_key: str):
        """Deploy agent as N8N workflow"""
        try:
            if not agent_id:
                return {"error": "Please provide agent ID"}
            
            if agent_id not in self.agents:
                return {"error": f"Agent '{agent_id}' not found"}
            
            if not self.runtime:
                return {"error": "Agent Runtime not initialized"}
            
            agent_config = self.agents[agent_id]
            
            # Get N8N credentials
            final_n8n_url = n8n_url or os.getenv("N8N_API_URL", "")
            final_n8n_key = n8n_key or os.getenv("N8N_API_KEY", "")
            
            if not final_n8n_url or not final_n8n_key:
                return {"error": "N8N API URL and Key required"}
            
            # Deploy to N8N (async operation)
            import asyncio
            result = asyncio.run(
                self.runtime.deploy_agent_to_n8n(
                    agent_config,
                    final_n8n_url,
                    final_n8n_key
                )
            )
            
            return result
        except Exception as e:
            logger.error(f"❌ Deployment failed: {e}")
            return {"error": str(e)}
    
    def run_orchestrator_integration(self, agent_id: str, command: str):
        """Run orchestrator to build, test, and deploy agent"""
        try:
            if not agent_id or not command:
                return "Error: Please provide agent ID and command"
            
            # Load orchestrator
            sys.path.insert(0, str(Path(__file__).parent.parent.parent))
            from orchestrator import MCPOrchestrator
            from memory import MemoryManager
            
            # Initialize orchestrator
            memory = MemoryManager()
            orchestrator = MCPOrchestrator(memory)
            
            # Add agent context to memory
            if agent_id in self.agents:
                agent_info = self.agents[agent_id]
                memory.add_message(
                    "system",
                    f"Agent {agent_id} configuration: {json.dumps(agent_info)}"
                )
            
            # Build full orchestrator command
            full_command = f"""
Agent ID: {agent_id}
Task: {command}

Available actions:
1. Test the agent with a sample message
2. Deploy the agent to N8N as a workflow
3. Verify deployment and get webhook URL
4. Run end-to-end test

Execute this complete workflow and report results.
"""
            
            # Execute through orchestrator
            result = orchestrator.process(full_command)
            
            return f"✅ Orchestrator Response:\n\n{result}"
            
        except Exception as e:
            logger.error(f"❌ Orchestrator integration failed: {e}")
            return f"Error: {str(e)}"
    
    # === Composio Integration ===
    def get_composio_status(self):
        """Get Composio integration status"""
        if not self.composio:
            return json.dumps({"error": "Composio not initialized"}, indent=2)
        
        try:
            status = self.composio.get_integration_status()
            return json.dumps(status, indent=2)
        except Exception as e:
            logger.error(f"❌ Composio status check failed: {e}")
            return json.dumps({"error": str(e)}, indent=2)
    
    def list_composio_apps(self):
        """List available Composio apps"""
        if not self.composio:
            return json.dumps({"error": "Composio not initialized"}, indent=2)
        
        try:
            apps = self.composio.list_available_apps()
            return json.dumps(apps, indent=2)
        except Exception as e:
            logger.error(f"❌ Failed to list apps: {e}")
            return json.dumps({"error": str(e)}, indent=2)
    
    def search_composio_tools(self, query):
        """Search Composio tools by keyword"""
        if not self.composio:
            return json.dumps({"error": "Composio not initialized"}, indent=2)
        
        if not query:
            return json.dumps({"error": "Please provide a search query"}, indent=2)
        
        try:
            results = self.composio.search_tools(query)
            return json.dumps(results, indent=2)
        except Exception as e:
            logger.error(f"❌ Search failed: {e}")
            return json.dumps({"error": str(e)}, indent=2)
    
    def list_composio_app_actions(self, app_key):
        """List actions for a specific Composio app"""
        if not self.composio:
            return json.dumps({"error": "Composio not initialized"}, indent=2)
        
        if not app_key:
            return json.dumps({"error": "Please provide an app key"}, indent=2)
        
        try:
            actions = self.composio.list_app_actions(app_key)
            return json.dumps(actions, indent=2)
        except Exception as e:
            logger.error(f"❌ Failed to list actions: {e}")
            return json.dumps({"error": str(e)}, indent=2)
    
    def execute_composio_action(self, app_key, action_key, parameters_json):
        """Execute a Composio action"""
        if not self.composio:
            return json.dumps({"error": "Composio not initialized"}, indent=2)
        
        if not all([app_key, action_key, parameters_json]):
            return json.dumps({"error": "Please provide app_key, action_key, and parameters"}, indent=2)
        
        try:
            # Parse parameters JSON
            parameters = json.loads(parameters_json)
            
            result = self.composio.execute_action(
                app_key=app_key,
                action_key=action_key,
                parameters=parameters
            )
            return json.dumps(result, indent=2)
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON in parameters"}, indent=2)
        except Exception as e:
            logger.error(f"❌ Action execution failed: {e}")
            return json.dumps({"error": str(e)}, indent=2)
    
    def connect_composio_account(self, app_key):
        """Generate OAuth URL to connect an account"""
        if not self.composio:
            return json.dumps({"error": "Composio not initialized"}, indent=2)
        
        if not app_key:
            return json.dumps({"error": "Please provide an app key"}, indent=2)
        
        try:
            result = self.composio.connect_account(app_key)
            return json.dumps(result, indent=2)
        except Exception as e:
            logger.error(f"❌ Connection failed: {e}")
            return json.dumps({"error": str(e)}, indent=2)

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

    with gr.Blocks(title="Agent Builder MCP") as demo:
        gr.Markdown(
            """
        # 🤖 Agent Builder MCP
        **Multi-framework AI agent creation platform**
        
        Supports: ADK, CrewAI, A2A Protocol, Langbase, AGUI
        """
        )

        with gr.Tab("🔧 ADK Agent (Vertex AI)"):
            gr.Markdown("### Create & Execute AI Development Kit (ADK) Agent with Vertex AI Anthropic")
            
            with gr.Row():
                with gr.Column():
                    gr.Markdown("#### Create Agent")
                    adk_name = gr.Textbox(label="Agent Name", placeholder="my_assistant")
                    adk_tools = gr.Textbox(
                        label="Capabilities (comma-separated)", 
                        placeholder="web_search,code_execution,file_operations"
                    )
                    adk_model = gr.Dropdown(
                        choices=[
                            "claude-3-5-sonnet-20241022",
                            "claude-3-opus-20240229",
                            "claude-3-sonnet-20240229",
                            "claude-3-haiku-20240307"
                        ],
                        label="Claude Model (Vertex AI)",
                        value="claude-3-5-sonnet-20241022",
                    )
                    adk_prompt = gr.Textbox(
                        label="System Prompt",
                        placeholder="You are a helpful assistant that...",
                        lines=3,
                    )
                    adk_btn = gr.Button("Create ADK Agent", variant="primary")
                    adk_output = gr.Code(label="Agent Configuration", language="json")
                    
                with gr.Column():
                    gr.Markdown("#### Execute Agent")
                    adk_agent_id = gr.Textbox(
                        label="Agent ID", 
                        placeholder="adk_my_assistant"
                    )
                    adk_message = gr.Textbox(
                        label="Your Message",
                        placeholder="Write a Python function to calculate fibonacci...",
                        lines=3
                    )
                    adk_exec_btn = gr.Button("Execute Agent", variant="primary")
                    adk_response = gr.Textbox(
                        label="Agent Response",
                        lines=10,
                        interactive=False
                    )
                    adk_list_btn = gr.Button("List All Agents")
                    adk_agents_list = gr.JSON(label="Active Agents")

            adk_btn.click(
                mcp.create_adk_agent,
                inputs=[adk_name, adk_tools, adk_model, adk_prompt],
                outputs=adk_output,
            )
            
            adk_exec_btn.click(
                mcp.execute_adk_agent,
                inputs=[adk_agent_id, adk_message],
                outputs=adk_response
            )
            
            adk_list_btn.click(
                mcp.list_adk_agents,
                outputs=adk_agents_list
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

        with gr.Tab("🔌 Composio Tools"):
            gr.Markdown("""
            ### Composio Integration - Connect 100+ Tools
            **Productivity**: Gmail, Slack, Notion, Trello, Asana  
            **Dev Tools**: GitHub, GitLab, Jira, Linear  
            **Data**: Google Sheets, Airtable, PostgreSQL  
            **More**: Calendar, Drive, Dropbox, Zapier, etc.
            """)
            
            with gr.Row():
                with gr.Column():
                    gr.Markdown("#### Status & Discovery")
                    composio_status_btn = gr.Button("Check Status", variant="secondary")
                    composio_status = gr.JSON(label="Integration Status")
                    
                    composio_search = gr.Textbox(
                        label="Search Tools",
                        placeholder="email, calendar, slack, github..."
                    )
                    composio_search_btn = gr.Button("Search", variant="primary")
                    composio_search_results = gr.JSON(label="Search Results")
                    
                    composio_list_apps_btn = gr.Button("List All Apps")
                    composio_apps = gr.JSON(label="Available Apps (top 50)")
                
                with gr.Column():
                    gr.Markdown("#### App Actions & Execution")
                    composio_app_key = gr.Textbox(
                        label="App Key",
                        placeholder="gmail, slack, github..."
                    )
                    composio_actions_btn = gr.Button("Get Actions")
                    composio_actions = gr.JSON(label="Available Actions")
                    
                    gr.Markdown("##### Execute Action")
                    composio_action_key = gr.Textbox(
                        label="Action Key",
                        placeholder="GMAIL_SEND_EMAIL, SLACK_POST_MESSAGE..."
                    )
                    composio_parameters = gr.Code(
                        label="Parameters (JSON)",
                        value='{\n  "to": "user@example.com",\n  "subject": "Hello",\n  "body": "Test"\n}',
                        language="json",
                        lines=5
                    )
                    composio_exec_btn = gr.Button("Execute Action", variant="primary")
                    composio_exec_result = gr.JSON(label="Execution Result")
                    
                    gr.Markdown("##### Connect Account")
                    composio_connect_app = gr.Textbox(
                        label="App to Connect",
                        placeholder="gmail, slack, github..."
                    )
                    composio_connect_btn = gr.Button("Generate Auth URL")
                    composio_connect_result = gr.JSON(label="Connection Info")
            
            # Wire up Composio events
            composio_status_btn.click(
                mcp.get_composio_status,
                outputs=composio_status
            )
            
            composio_search_btn.click(
                mcp.search_composio_tools,
                inputs=composio_search,
                outputs=composio_search_results
            )
            
            composio_list_apps_btn.click(
                mcp.list_composio_apps,
                outputs=composio_apps
            )
            
            composio_actions_btn.click(
                mcp.list_composio_app_actions,
                inputs=composio_app_key,
                outputs=composio_actions
            )
            
            composio_exec_btn.click(
                mcp.execute_composio_action,
                inputs=[composio_app_key, composio_action_key, composio_parameters],
                outputs=composio_exec_result
            )
            
            composio_connect_btn.click(
                mcp.connect_composio_account,
                inputs=composio_connect_app,
                outputs=composio_connect_result
            )

        with gr.Tab("🧪 Test & Deploy"):
            gr.Markdown("""
            ### Agent Testing & Deployment
            - **Test Execution**: Run agent code in isolated environment
            - **Deploy to N8N**: Convert agent to live workflow
            - **Orchestrator Integration**: Connect agent to master orchestrator
            """)
            
            with gr.Row():
                with gr.Column():
                    gr.Markdown("#### 1. Test Agent Execution")
                    test_agent_id = gr.Textbox(
                        label="Agent ID",
                        placeholder="adk_my_agent"
                    )
                    test_message = gr.Textbox(
                        label="Test Message",
                        placeholder="Hello, can you help me with...",
                        lines=3
                    )
                    test_btn = gr.Button("🧪 Test Agent", variant="primary")
                    test_output = gr.JSON(label="Execution Result")
                
                with gr.Column():
                    gr.Markdown("#### 2. Deploy to N8N")
                    deploy_agent_id = gr.Textbox(
                        label="Agent ID",
                        placeholder="adk_my_agent"
                    )
                    n8n_url = gr.Textbox(
                        label="N8N API URL",
                        value=os.getenv("N8N_API_URL", "")
                    )
                    n8n_key = gr.Textbox(
                        label="N8N API Key",
                        value=os.getenv("N8N_API_KEY", ""),
                        type="password"
                    )
                    deploy_btn = gr.Button("🚀 Deploy to N8N", variant="primary")
                    deploy_output = gr.JSON(label="Deployment Result")
            
            with gr.Row():
                with gr.Column():
                    gr.Markdown("#### 3. Orchestrator Integration")
                    orchestrator_agent_id = gr.Textbox(
                        label="Agent ID",
                        placeholder="adk_my_agent"
                    )
                    orchestrator_command = gr.Textbox(
                        label="Orchestrator Command",
                        placeholder="Build and test the agent, then create N8N workflow",
                        lines=3
                    )
                    orchestrator_btn = gr.Button("🎯 Run Orchestrator", variant="primary")
                    orchestrator_output = gr.Textbox(
                        label="Orchestrator Response",
                        lines=15
                    )
            
            # Event handlers
            test_btn.click(
                mcp.test_agent_execution,
                inputs=[test_agent_id, test_message],
                outputs=test_output
            )
            
            deploy_btn.click(
                mcp.deploy_agent_to_n8n,
                inputs=[deploy_agent_id, n8n_url, n8n_key],
                outputs=deploy_output
            )
            
            orchestrator_btn.click(
                mcp.run_orchestrator_integration,
                inputs=[orchestrator_agent_id, orchestrator_command],
                outputs=orchestrator_output
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
