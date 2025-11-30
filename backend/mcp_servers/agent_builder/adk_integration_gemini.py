"""
ADK Integration - Using Gemini 3 Pro instead of Claude
"""

import os
from typing import Any, Dict, Optional, List
from google import genai
from google.genai import types

from loguru import logger


class ADKIntegration:
    """ADK (AI Development Kit) integration for agent building with Gemini 3 Pro"""

    def __init__(self):
        """Initialize ADK integration with Gemini 3 Pro via Vertex AI"""
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "stellar-state-471406-f8")
        self.location = os.getenv("GOOGLE_CLOUD_LOCATION", "global")
        self.model_id = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")
        
        # Initialize Gemini client
        try:
            self.client = genai.Client(
                vertexai=True,
                project=self.project_id,
                location=self.location
            )
            logger.success(f"✅ ADK initialized with Gemini 3 Pro (Project: {self.project_id})")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Gemini client: {e}")
            logger.info("💡 Run: gcloud auth application-default login --project=stellar-state-471406-f8")
            self.client = None
        
        # Store active agents with conversation history
        self.agents = {}
        logger.info("🔧 ADK integration initialized")

    def create_agent(
        self,
        name: str,
        description: str,
        capabilities: list,
        model: str = "gemini-2.0-flash-exp",
    ) -> Dict[str, Any]:
        """
        Create an ADK agent

        Args:
            name: Agent name
            description: Agent description
            capabilities: List of agent capabilities
            model: Gemini model to use

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
            "message": f"ADK agent '{name}' created successfully with Gemini 3 Pro",
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

        return f"""You are {name}, an AI agent.

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
        Execute agent with REAL Gemini 3 Pro API call

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
                "error": "Gemini client not initialized. Run: gcloud auth application-default login"
            }
        
        if agent_id not in self.agents:
            return {
                "success": False,
                "error": f"Agent '{agent_id}' not found"
            }
        
        agent = self.agents[agent_id]
        logger.info(f"🤖 Executing agent: {agent['name']}")
        
        try:
            # Build full prompt with system instructions
            full_prompt = f"{agent['system_prompt']}\n\nUser: {user_message}\n\nAssistant:"
            
            # Call Gemini API
            response = self.client.models.generate_content(
                model=agent["model"],
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    temperature=agent["temperature"],
                    max_output_tokens=agent["max_tokens"],
                )
            )
            
            # Extract response
            assistant_message = response.text
            
            # Update conversation history
            history = agent.get("conversation_history", [])
            history.append({"role": "user", "content": user_message})
            history.append({"role": "assistant", "content": assistant_message})
            agent["conversation_history"] = history[-10:]  # Keep last 10 messages
            
            logger.success(f"✅ Agent {agent['name']} responded successfully")
            
            return {
                "success": True,
                "agent_id": agent_id,
                "agent_name": agent["name"],
                "user_message": user_message,
                "response": assistant_message,
                "model": agent["model"],
                "conversation_length": len(history),
                "usage": {
                    "model": agent["model"],
                    "prompt_length": len(full_prompt),
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
