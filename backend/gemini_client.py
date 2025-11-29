"""
Gemini 3 Pro Client Wrapper for W3J MCP Hub
Uses Google Gen AI SDK with OAuth2 credentials
"""

import os
import json
from typing import Optional, Dict, Any
from pathlib import Path

from google import genai
from google.genai import types
from loguru import logger


class GeminiClient:
    """W3J MCP Hub - Gemini 3 Pro Client"""

    def __init__(self):
        """Initialize Gemini client with Google Cloud credentials"""
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "stellar-state-471406-f8")
        self.location = os.getenv("GOOGLE_CLOUD_LOCATION", "global")
        self.model_id = os.getenv("GEMINI_MODEL", "gemini-3-pro-preview")
        
        # Try to initialize client
        self.client = None
        self._initialize_client()

    def _initialize_client(self):
        """Initialize Google Gen AI client with Vertex AI"""
        try:
            # Use application default credentials (from gcloud auth)
            # Don't use credentials.json - it's OAuth2 client credentials, not service account
            
            # Initialize client with Vertex AI
            self.client = genai.Client(
                vertexai=True,
                project=self.project_id,
                location=self.location
            )
            
            logger.success(f"✅ Gemini 3 Pro client initialized (Project: {self.project_id})")
            
        except Exception as e:
            logger.warning(f"⚠️ Could not initialize Gemini client: {e}")
            logger.info("💡 Run: gcloud auth application-default login --project=stellar-state-471406-f8")
            self.client = None

    def generate_text(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        temperature: float = 1.0,
        max_tokens: int = 8000,
        thinking_level: str = "low",
    ) -> str:
        """
        Generate text using Gemini 3 Pro
        
        Args:
            prompt: User prompt
            system_instruction: System instructions
            temperature: Temperature (default 1.0 recommended for Gemini 3)
            max_tokens: Max output tokens
            thinking_level: "low" for fast responses, "high" for complex reasoning
            
        Returns:
            Generated text
        """
        if not self.client:
            return "❌ Gemini client not initialized. Please configure Google Cloud credentials."
        
        try:
            # Map thinking level
            thinking_map = {
                "low": types.ThinkingLevel.LOW,
                "high": types.ThinkingLevel.HIGH,
            }
            
            # Build config
            config = types.GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
                thinking_config=types.ThinkingConfig(
                    thinking_level=thinking_map.get(thinking_level, types.ThinkingLevel.LOW)
                ),
            )
            
            # Add system instruction if provided
            if system_instruction:
                config.system_instruction = system_instruction
            
            # Generate content
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=config,
            )
            
            return response.text
            
        except Exception as e:
            logger.error(f"❌ Gemini generation failed: {e}")
            return f"Error generating response: {str(e)}"

    def analyze_intent(self, user_input: str, context: str = "") -> Dict[str, Any]:
        """
        Analyze user intent using Gemini 3 Pro
        
        Args:
            user_input: User's input
            context: Additional context
            
        Returns:
            Intent analysis dict with target, confidence, parameters
        """
        if not self.client:
            # Fallback to keyword matching
            return self._keyword_intent(user_input)
        
        system_instruction = """You are an intelligent router for W3J MCP Hub.
Analyze the user's request and determine which service should handle it:

- "n8n": Workflow automation, integrations, scheduling, webhooks
- "agent": AI agents, LLM tasks, code generation, reasoning
- "local": File operations, system control, terminal commands
- "orchestrator": General chat, unclear requests

Return JSON: {"target": "service_name", "confidence": 0.0-1.0, "reasoning": "why"}"""

        prompt = f"""User request: {user_input}

Context: {context if context else "None"}

Analyze and return JSON only."""

        try:
            response = self.generate_text(
                prompt=prompt,
                system_instruction=system_instruction,
                thinking_level="low",  # Fast routing
            )
            
            # Parse JSON response
            import json
            result = json.loads(response.strip())
            return result
            
        except Exception as e:
            logger.warning(f"⚠️ Intent analysis failed, using keywords: {e}")
            return self._keyword_intent(user_input)

    def _keyword_intent(self, user_input: str) -> Dict[str, Any]:
        """Fallback keyword-based intent detection"""
        user_lower = user_input.lower()
        
        # N8N keywords
        n8n_keywords = ["workflow", "automation", "integrate", "schedule", "webhook", "n8n"]
        if any(k in user_lower for k in n8n_keywords):
            return {"target": "n8n", "confidence": 0.7, "reasoning": "Keyword match"}
        
        # Agent keywords
        agent_keywords = ["agent", "ai", "generate", "code", "analyze", "reason"]
        if any(k in user_lower for k in agent_keywords):
            return {"target": "agent", "confidence": 0.7, "reasoning": "Keyword match"}
        
        # Local keywords
        local_keywords = ["file", "folder", "system", "terminal", "command", "local"]
        if any(k in user_lower for k in local_keywords):
            return {"target": "local", "confidence": 0.7, "reasoning": "Keyword match"}
        
        # Default to orchestrator
        return {"target": "orchestrator", "confidence": 0.5, "reasoning": "Default routing"}
