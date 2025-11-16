"""
MCP Orchestrator - Routes requests to appropriate MCP servers
"""

import os
from typing import Any, Dict, Optional

from anthropic import Anthropic
from loguru import logger


class MCPOrchestrator:
    """Master orchestrator that routes user requests to appropriate MCP servers"""

    def __init__(self, memory_manager):
        """Initialize orchestrator with memory and AI client"""
        self.memory = memory_manager

        # Initialize Anthropic client if API key exists
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if api_key and api_key != "test-key":
            try:
                self.client = Anthropic(api_key=api_key)
            except Exception as e:
                logger.warning(f"⚠️ Could not initialize Anthropic client: {e}")
                self.client = None
        else:
            logger.info("⚠️ Using keyword-based routing (no Anthropic API key)")
            self.client = None

        # Available MCP servers (will be expanded)
        self.mcp_servers = {
            "n8n": None,  # Will import when ready
            "agent_builder": None,
            "local_control": None,
            "cloud_services": None,
        }

        logger.info("🧠 Orchestrator initialized")

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
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=500,
                messages=[{"role": "user", "content": user_input}],
                system=system_prompt,
            )

            # Parse response
            import json

            intent = json.loads(response.content[0].text)
            logger.info(f"🎯 Intent: {intent['target']} ({intent['confidence']})")
            return intent

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
        """Handle N8N workflow requests"""
        if self.mcp_servers["n8n"] is None:
            return "🔜 N8N MCP is being built! Coming in Phase 2.\n\nIt will let you:\n- Create workflows from natural language\n- Test workflows with validation\n- Deploy to your N8N instance\n- Monitor workflow execution"

        # Will call actual N8N MCP
        return self.mcp_servers["n8n"].process(input_text)

    def _handle_agent(self, input_text: str, intent: Dict) -> str:
        """Handle agent building requests"""
        if self.mcp_servers["agent_builder"] is None:
            return "🔜 Agent Builder MCP coming soon!\n\nSupported frameworks:\n- CrewAI (multi-agent teams)\n- ADK (AI Development Kit)\n- A2A (agent-to-agent communication)\n- Langbase (memory & RAG)\n- AGUI (visual interfaces)"

        return self.mcp_servers["agent_builder"].process(input_text)

    def _handle_local(self, input_text: str, intent: Dict) -> str:
        """Handle local PC control requests"""
        if self.mcp_servers["local_control"] is None:
            return "🔜 Local Control MCP coming soon!\n\nCapabilities:\n- Execute system commands\n- Control applications (VS Code, browsers)\n- File operations\n- Browser automation with your auth\n- Keyboard/mouse control"

        return self.mcp_servers["local_control"].process(input_text)

    def _handle_cloud(self, input_text: str, intent: Dict) -> str:
        """Handle cloud services requests"""
        if self.mcp_servers["cloud_services"] is None:
            return "🔜 Cloud Services MCP coming soon!\n\nIntegrations:\n- GCP (Cloud Run, Storage, etc.)\n- WhatsApp (unofficial API)\n- GitHub Actions (workflows, runs)\n- More coming..."

        return self.mcp_servers["cloud_services"].process(input_text)

    def _handle_general(self, input_text: str) -> str:
        """Handle general queries about the system"""

        response = f"""👋 **Ultimate MCP System Active!**

**Current Status:** Phase 1 - Foundation Complete

**Available Soon:**
1. 🔄 **N8N Automation** - Build & deploy workflows
2. 🤖 **Agent Builder** - Create AI agent teams
3. 💻 **Local PC Control** - Full system access
4. ☁️ **Cloud Services** - GCP, WhatsApp, GitHub

**Try asking:**
- "What can you do?"
- "Show me system status"
- "Explain N8N integration"

**Your question:** {input_text}

Right now I'm in foundation phase. The actual MCP servers are being built in Phase 2!
Check CURRENT_STATUS.md for latest progress.
"""

        return response
