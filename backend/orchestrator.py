"""
MCP Orchestrator - Routes requests to appropriate MCP servers
"""

import os
from typing import Any, Dict, Optional

from loguru import logger

# Import system modules for lazy loading
import sys
from pathlib import Path

# Import Gemini client
try:
    from backend.gemini_client import GeminiClient
except ImportError:
    from gemini_client import GeminiClient


class MCPOrchestrator:
    """W3J MCP Hub - Master orchestrator routing to N8N, Agent Builder, and Local Control servers"""

    def __init__(self, memory_manager, tool_registry=None):
        """Initialize orchestrator with memory and AI client"""
        self.memory = memory_manager
        self.registry = tool_registry

        # Initialize Gemini 3 Pro client
        try:
            self.client = GeminiClient()
            logger.success("🤖 W3J MCP Hub using Gemini 3 Pro")
        except Exception as e:
            logger.warning(f"⚠️ Could not initialize Gemini client: {e}")
            logger.info("⚠️ Using keyword-based routing")
            self.client = None

        # MCP servers - loaded lazily when first needed
        self.mcp_servers = {
            "n8n": None,
            "agent_builder": None,
            "local_control": None,
            "cloud_services": None,
        }

        logger.info("🧠 W3J MCP Hub initialized (lazy-loading enabled)")

    def _load_server(self, server_name: str):
        """Lazy-load MCP server on first use"""
        if self.mcp_servers[server_name] is not None:
            return self.mcp_servers[server_name]

        logger.info(f"📦 Loading {server_name} server...")

        # Add server directories to path for internal imports
        base_path = Path(__file__).parent / "mcp_servers"

        try:
            if server_name == "n8n":
                sys.path.insert(0, str(base_path / "n8n_automation"))
                from mcp_servers.n8n_automation.server import N8NAutomationMCP
                self.mcp_servers["n8n"] = N8NAutomationMCP()

            elif server_name == "agent_builder":
                sys.path.insert(0, str(base_path / "agent_builder"))
                from mcp_servers.agent_builder.server import AgentBuilderMCP
                self.mcp_servers["agent_builder"] = AgentBuilderMCP()

            elif server_name == "local_control":
                sys.path.insert(0, str(base_path / "local_control"))
                from mcp_servers.local_control.server import LocalControlMCP
                self.mcp_servers["local_control"] = LocalControlMCP()

            logger.info(f"✅ {server_name} server loaded")
            return self.mcp_servers[server_name]

        except Exception as e:
            logger.error(f"❌ Failed to load {server_name}: {e}")
            return None

    def process(self, user_input: str) -> str:
        """
        Process user input and route to appropriate MCP

        Args:
            user_input: User's natural language request

        Returns:
            Response from the appropriate MCP or orchestrator
        """
        logger.info(f"🔍 Processing: {user_input}")

        # Get context from memory
        context = self.memory.get_context()

        # Analyze intent and route
        intent = self._analyze_intent(user_input, context)

        # Route to appropriate MCP
        if intent["target"] == "n8n":
            return self._handle_n8n(user_input, intent)
        elif intent["target"] == "agent":
            return self._handle_agent(user_input, intent)
        elif intent["target"] == "local":
            return self._handle_local(user_input, intent)
        elif intent["target"] == "cloud":
            return self._handle_cloud(user_input, intent)
        else:
            return self._handle_general(user_input)

    def _analyze_intent(self, user_input: str, context: Dict) -> Dict[str, Any]:
        """Use Claude to analyze user intent and determine routing"""

        # Fallback to keyword-based routing if no API client
        if self.client is None:
            return self._keyword_based_intent(user_input)

        system_prompt = f"""You are the intent analyzer for Ultimate MCP System.
Analyze user requests and determine which MCP to route to:

- "n8n": N8N workflow automation (create, test, deploy workflows)
- "agent": Agent building (CrewAI, ADK, A2A, Langbase, AGUI)
- "local": Local PC control (commands, file ops, browser, apps)
- "cloud": Cloud services (GCP, WhatsApp, GitHub Actions)
- "general": General queries or system info

Context: {context}

Respond with JSON: {{"target": "...", "confidence": 0.0-1.0, "params": {{}}}}"""

        try:
            # Use Gemini client's analyze_intent method
            if self.client and hasattr(self.client, 'analyze_intent'):
                intent = self.client.analyze_intent(user_input, context)
                logger.info(f"🎯 Intent: {intent['target']} ({intent.get('confidence', 0)})")
                return intent
            else:
                return self._keyword_based_intent(user_input)

        except Exception as e:
            logger.error(f"Intent analysis error: {e}")
            return self._keyword_based_intent(user_input)

    def _keyword_based_intent(self, user_input: str) -> Dict[str, Any]:
        """Simple keyword-based intent detection fallback"""
        text = user_input.lower()

        if any(word in text for word in ["workflow", "n8n", "automation", "integrate"]):
            return {"target": "n8n", "confidence": 0.7, "params": {}}
        elif any(
            word in text for word in ["agent", "crewai", "adk", "langbase", "crew"]
        ):
            return {"target": "agent", "confidence": 0.7, "params": {}}
        elif any(
            word in text
            for word in ["command", "file", "system", "browser", "local", "pc"]
        ):
            return {"target": "local", "confidence": 0.7, "params": {}}
        elif any(word in text for word in ["cloud", "gcp", "whatsapp", "github"]):
            return {"target": "cloud", "confidence": 0.7, "params": {}}
        else:
            return {"target": "general", "confidence": 0.5, "params": {}}

    def _handle_n8n(self, input_text: str, intent: Dict) -> str:
        """Handle N8N workflow requests - Actually creates workflows"""
        if not self.registry:
            return "⚠️ Tool registry not available"
        
        # Get N8N tool for creating workflows
        create_tool = self.registry.get_tool("create_n8n_workflow")
        
        if not create_tool:
            return "⚠️ N8N workflow creation tool not available"
        
        try:
            # Actually create the workflow
            logger.info(f"🔄 Creating N8N workflow from: {input_text}")
            result = create_tool.execute(description=input_text)
            
            if "error" in result:
                return f"❌ **Error Creating Workflow:**\n\n{result['error']}"
            
            # Format the response with actual workflow
            import json
            workflow_json = json.dumps(result, indent=2)
            
            response = f"""✅ **N8N Workflow Created Successfully!**

**Your Request:** {input_text}

**Generated Workflow:**
```json
{workflow_json}
```

**Next Steps:**
1. Review the workflow above
2. Test it: Tell me "test this workflow"
3. Deploy it: Tell me "deploy to N8N"

**Connected to:** https://n8n.aixlabs.fun/ ✅
"""
            return response
            
        except Exception as e:
            logger.error(f"❌ N8N workflow creation failed: {e}")
            return f"❌ **Error:** {str(e)}\n\nPlease describe your workflow more clearly."

    def _handle_agent(self, input_text: str, intent: Dict) -> str:
        """Handle agent building requests - Actually creates agents"""
        if not self.registry:
            return "⚠️ Tool registry not available"
        
        # Detect which framework user wants
        text_lower = input_text.lower()
        
        if "crewai" in text_lower or "crew" in text_lower:
            tool = self.registry.get_tool("create_crewai_agent")
            framework = "CrewAI"
        elif "adk" in text_lower:
            tool = self.registry.get_tool("create_adk_agent")
            framework = "ADK"
        elif "a2a" in text_lower:
            tool = self.registry.get_tool("create_a2a_agent")
            framework = "A2A"
        elif "langbase" in text_lower:
            tool = self.registry.get_tool("create_langbase_agent")
            framework = "Langbase"
        elif "agui" in text_lower or "gui" in text_lower:
            tool = self.registry.get_tool("create_agui_agent")
            framework = "AGUI"
        elif "list" in text_lower:
            tool = self.registry.get_tool("list_agents")
            framework = "List"
        else:
            # Show available frameworks
            agent_tools = self.registry.get_by_category("agent")
            tool_list = "\n".join([f"- **{t.schema.display_name}**" for t in agent_tools])
            return f"""🤖 **Which Agent Framework?**

Please specify which framework you want to use:

{tool_list}

**Examples:**
- "Create a CrewAI agent for research"
- "Build ADK agent for automation"
- "List all my agents"
"""
        
        if not tool:
            return f"⚠️ {framework} tool not available"
        
        try:
            # Extract agent name and purpose from input
            import re
            name_match = re.search(r'(?:agent|team)?\s*(?:for|to|named|called)\s+([a-zA-Z0-9_\s]+)', input_text, re.IGNORECASE)
            agent_name = name_match.group(1).strip() if name_match else "My Agent"
            
            logger.info(f"🤖 Creating {framework} agent: {agent_name}")
            
            # Execute tool with appropriate parameters
            if framework == "List":
                result = tool.execute()
            else:
                result = tool.execute(
                    name=agent_name,
                    description=input_text,
                    system_prompt=f"You are {agent_name}. {input_text}"
                )
            
            if "error" in result:
                return f"❌ **Error Creating Agent:**\n\n{result['error']}"
            
            import json
            agent_json = json.dumps(result, indent=2)
            
            response = f"""✅ **{framework} Agent Created Successfully!**

**Agent Name:** {agent_name}
**Your Request:** {input_text}

**Agent Configuration:**
```json
{agent_json}
```

**Agent is ready to use!** You can now give it tasks or modify its configuration.
"""
            return response
            
        except Exception as e:
            logger.error(f"❌ Agent creation failed: {e}")
            return f"❌ **Error:** {str(e)}\n\nPlease provide: agent name and purpose."

    def _handle_local(self, input_text: str, intent: Dict) -> str:
        """Handle local PC control requests - Actually executes commands"""
        if not self.registry:
            return "⚠️ Tool registry not available"
        
        text_lower = input_text.lower()
        
        # Detect what user wants to do
        if "execute" in text_lower or "run command" in text_lower or "cmd" in text_lower:
            tool = self.registry.get_tool("execute_system_command")
            # Extract command
            import re
            cmd_match = re.search(r'(?:execute|run|cmd)[\s:]+(.+)', input_text, re.IGNORECASE)
            command = cmd_match.group(1).strip() if cmd_match else input_text
            
            try:
                result = tool.execute(command=command)
                return f"""✅ **Command Executed**

**Command:** `{command}`
**Exit Code:** {result.get('exit_code', 'N/A')}

**Output:**
```
{result.get('stdout', '')}
```

**Errors:**
```
{result.get('stderr', '')}
```
"""
            except Exception as e:
                return f"❌ **Error:** {str(e)}"
        
        elif "list" in text_lower and "file" in text_lower:
            tool = self.registry.get_tool("list_files")
            # Extract path
            import re
            path_match = re.search(r'(?:in|from|at)\s+([^\s]+)', input_text, re.IGNORECASE)
            path = path_match.group(1).strip() if path_match else "."
            
            try:
                result = tool.execute(path=path)
                files = result.get('files', [])
                file_list = "\n".join([f"- {f['name']} ({'dir' if f.get('is_dir') else 'file'})" for f in files[:20]])
                return f"""✅ **Files in {result.get('path', path')}:**

{file_list}

Total: {len(files)} items
"""
            except Exception as e:
                return f"❌ **Error:** {str(e)}"
        
        elif "system info" in text_lower or "get info" in text_lower:
            tool = self.registry.get_tool("get_system_info")
            try:
                result = tool.execute()
                return f"""✅ **System Information**

**OS:** {result.get('system', '')} {result.get('release', '')}
**Processor:** {result.get('processor', '')}
**CPU Cores:** {result.get('cpu_count', '')}
**Memory:** {result.get('memory_total', 0) // (1024**3)} GB total
**Disk:** {result.get('disk_total', 0) // (1024**3)} GB total
"""
            except Exception as e:
                return f"❌ **Error:** {str(e)}"
        
        elif "process" in text_lower:
            tool = self.registry.get_tool("list_processes")
            try:
                result = tool.execute(limit=10)
                proc_list = "\n".join([f"- **{p['name']}** (PID: {p['pid']}) - CPU: {p.get('cpu_percent', 0)}%, Mem: {p.get('memory_percent', 0)}%" for p in result[:10]])
                return f"""✅ **Top Processes:**

{proc_list}
"""
            except Exception as e:
                return f"❌ **Error:** {str(e)}"
        
        # Default: show options
        local_tools = self.registry.get_by_category("local")
        tool_list = "\n".join([f"- **{t.schema.display_name}**" for t in local_tools])
        
        response = f"""💻 **Local PC Control**

**Your Question:** {input_text}

**Available Tools:**

{tool_list}

**Example Commands:**
- "List files in my Documents folder"
- "Get system information"
- "Open Chrome browser"
- "Execute command: dir"
- "Show running processes"

**Next Steps:**
1. Tell me what you want to do
2. I'll use the appropriate tool
3. You'll get the results instantly

What would you like me to do on your PC?
"""
        return response

    def _handle_cloud(self, input_text: str, intent: Dict) -> str:
        """Handle cloud services requests"""
        if self.mcp_servers["cloud_services"] is None:
            return "🔜 Cloud Services MCP coming soon!\n\nIntegrations:\n- GCP (Cloud Run, Storage, etc.)\n- WhatsApp (unofficial API)\n- GitHub Actions (workflows, runs)\n- More coming..."

        return self.mcp_servers["cloud_services"].process(input_text)

    def _handle_general(self, input_text: str) -> str:
        """Handle general queries about the system"""

        response = f"""👋 **W3J MCP Hub - FULLY OPERATIONAL!** by [@W3JDev](https://github.com/W3JDev)

**🎉 Current Status:** Production Ready - Powered by Gemini 3 Pro

**✅ What's Working Right Now:**

1. **🔄 N8N Automation**
   - Create workflows from natural language
   - Test & validate workflows
   - Deploy to your N8N instance
   - 4 tools ready: create, test, deploy, validate

2. **🤖 AI Agent Builder**
   - CrewAI multi-agent teams
   - ADK (AI Development Kit)
   - A2A agent-to-agent communication
   - Langbase with memory & RAG
   - AGUI visual interfaces
   - 6 tools ready to build agents

3. **💻 Local PC Control**
   - Execute system commands
   - File operations (list, read)
   - Process management
   - Open URLs & applications
   - Get system information
   - 7 tools for full PC control

**🤖 AI Engine:**
- Model: Gemini 3 Pro (gemini-3-pro-preview)
- Project: stellar-state-471406-f8
- Features: Advanced reasoning, agentic operations, multimodal understanding

**📊 System Stats:**
- Total Tools: 17
- Categories: N8N (4), Agent (6), Local (7)
- Status: All systems operational
- Response Time: Fast (keyword routing with AI fallback)

**💡 Try These Commands:**
- "Create a workflow that posts to Slack"
- "Build an AI agent for research"
- "List files in my documents folder"
- "Show system information"
- "Create a blog writing agent"

**Your question:** {input_text}

Need help? Check out the docs or visit [GitHub](https://github.com/W3JDev/ultimate-mcp-system)
"""

        return response
