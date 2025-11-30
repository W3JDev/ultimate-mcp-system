"""
ADK Integration - AI Development Kit integration using Anthropic API
"""

import os
from typing import Any, Dict, Optional, List
from anthropic import Anthropic

from loguru import logger


class ADKIntegration:
    """ADK (AI Development Kit) integration for agent building with Anthropic API"""

    def __init__(self):
        """Initialize ADK integration with Anthropic API"""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        
        # Initialize Anthropic client
        if not api_key:
            logger.error("❌ ANTHROPIC_API_KEY not found in environment")
            logger.info("💡 Add ANTHROPIC_API_KEY to your .env file")
            self.client = None
        else:
            try:
                self.client = Anthropic(api_key=api_key)
                logger.success(f"✅ ADK initialized with Anthropic API")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Anthropic client: {e}")
                self.client = None
        
        # Store active agents with conversation history
        self.agents = {}
        logger.info("🔧 ADK integration initialized")

    def create_agent(
        self,
        name: str,
        description: str,
        capabilities: list,
        model: str = "claude-3-5-sonnet-20241022",
    ) -> Dict[str, Any]:
        """
        Create an ADK agent

        Args:
            name: Agent name
            description: Agent description
            capabilities: List of agent capabilities
            model: Claude model to use

        Returns:
            Agent configuration
        """
        logger.info(f"🤖 Creating ADK agent: {name}")

        agent_id = f"adk_{name.lower().replace(' ', '_')}"
        
        agent_config = {
            "framework": "ADK",
            "name": name,
            "description": description,
            "model": model,
            "capabilities": capabilities,
            "tools": self._get_tools_for_capabilities(capabilities),
            "system_prompt": self._generate_system_prompt(
                name, description, capabilities
            ),
            "temperature": 0.7,
            "max_tokens": 4096,
            "agent_id": agent_id,
            "conversation_history": [],  # Track conversation
        }
        
        # Store agent in active agents
        self.agents[agent_id] = agent_config
        
        logger.success(f"✅ ADK agent created: {agent_id}")

        return {
            "success": True,
            "agent": agent_config,
            "agent_id": agent_id,
            "message": f"ADK agent '{name}' created successfully with Vertex AI",
        }

    def _get_tools_for_capabilities(self, capabilities: list) -> list:
        """Map capabilities to ADK tools"""
        tool_mapping = {
            "web_search": ["search_web", "fetch_url"],
            "code_execution": ["execute_python", "run_shell"],
            "file_operations": ["read_file", "write_file", "list_directory"],
            "api_calls": ["make_http_request", "call_api"],
            "data_analysis": ["analyze_data", "plot_chart"],
        }

        tools = []
        for capability in capabilities:
            if capability in tool_mapping:
                tools.extend(tool_mapping[capability])

        return tools

    def _generate_system_prompt(
        self, name: str, description: str, capabilities: list
    ) -> str:
        """Generate system prompt for agent"""
        capabilities_text = ", ".join(capabilities)

        return f"""You are {name}, an AI agent built with ADK.

Description: {description}

Your capabilities include: {capabilities_text}

You are helpful, accurate, and follow user instructions precisely. Always explain your reasoning and provide clear, actionable responses."""

    def execute_agent(
        self, 
        agent_id: str, 
        user_message: str,
        conversation_history: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Execute agent with REAL Vertex AI Anthropic API call

        Args:
            agent_id: Agent ID
            user_message: User's message
            conversation_history: Optional conversation history

        Returns:
            Agent response with full details
        """
        if not self.client:
            return {
                "success": False,
                "error": "Vertex AI client not initialized. Run: gcloud auth application-default login"
            }
        
        if agent_id not in self.agents:
            return {
                "success": False,
                "error": f"Agent '{agent_id}' not found"
            }
        
        agent = self.agents[agent_id]
        logger.info(f"🤖 Executing agent: {agent['name']}")
        
        try:
            # Build conversation history
            messages = conversation_history or agent.get("conversation_history", [])
            messages.append({
                "role": "user",
                "content": user_message
            })
            
            # Call Anthropic API directly
            response = self.client.messages.create(
                model=agent["model"],
                max_tokens=agent["max_tokens"],
                temperature=agent["temperature"],
                system=agent["system_prompt"],
                messages=messages
            )
            
            # Extract response
            assistant_message = response.content[0].text
            
            # Update conversation history
            messages.append({
                "role": "assistant",
                "content": assistant_message
            })
            agent["conversation_history"] = messages[-10:]  # Keep last 10 messages
            
            logger.success(f"✅ Agent {agent['name']} responded successfully")
            
            return {
                "success": True,
                "agent_id": agent_id,
                "agent_name": agent["name"],
                "user_message": user_message,
                "response": assistant_message,
                "model": agent["model"],
                "conversation_length": len(messages),
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens,
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Agent execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "agent_id": agent_id,
            }
    
    def chat_with_agent(self, agent_id: str, user_message: str) -> str:
        """
        Simple chat interface - returns just the response text
        
        Args:
            agent_id: Agent ID
            user_message: User's message
            
        Returns:
            Agent's response text
        """
        result = self.execute_agent(agent_id, user_message)
        
        if result["success"]:
            return result["response"]
        else:
            return f"Error: {result.get('error', 'Unknown error')}"
    
    def list_agents(self) -> Dict[str, Any]:
        """
        List all created agents
        
        Returns:
            Dictionary of agent IDs and their configs
        """
        return {
            "success": True,
            "count": len(self.agents),
            "agents": {
                agent_id: {
                    "name": config["name"],
                    "description": config["description"],
                    "model": config["model"],
                    "capabilities": config["capabilities"],
                    "conversation_length": len(config.get("conversation_history", []))
                }
                for agent_id, config in self.agents.items()
            }
        }
    
    def reset_conversation(self, agent_id: str) -> Dict[str, Any]:
        """
        Reset agent's conversation history
        
        Args:
            agent_id: Agent ID
            
        Returns:
            Success status
        """
        if agent_id not in self.agents:
            return {"success": False, "error": f"Agent '{agent_id}' not found"}
        
        self.agents[agent_id]["conversation_history"] = []
        logger.info(f"🔄 Reset conversation for agent: {agent_id}")
        
        return {
            "success": True,
            "message": f"Conversation reset for agent '{agent_id}'"
        }
