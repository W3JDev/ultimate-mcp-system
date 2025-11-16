'''
Workflow Builder - Generate N8N workflows from natural language
'''
import os
import json
from typing import Dict, Any, List
from anthropic import Anthropic
from loguru import logger

class WorkflowBuilder:
    '''AI-powered N8N workflow builder'''

    def __init__(self):
        '''Initialize builder with Claude API'''
        api_key = os.getenv("ANTHROPIC_API_KEY")
        try:
            if api_key and api_key != "test-key":
                self.client = Anthropic(api_key=api_key)
            else:
                self.client = None
                logger.warning("⚠️  No valid Anthropic API key - workflow builder running in limited mode")
        except Exception as e:
            self.client = None
            logger.error(f"❌ Failed to initialize Anthropic client: {e}")
        self.templates = self._load_templates()
        logger.info("🏗️  Workflow builder initialized")

    def build_from_description(self, description: str) -> Dict[str, Any]:
        '''
        Build N8N workflow from natural language description

        Args:
            description: Natural language workflow description

        Returns:
            N8N workflow JSON
        '''
        logger.info(f"🏗️  Building workflow: {description}")

        # Fallback to template if no AI available
        if self.client is None:
            logger.warning("⚠️  Using template workflow (no AI client)")
            return self._create_template_workflow(description)

        # Use Claude to generate workflow
        system_prompt = self._get_system_prompt()

        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4000,
                messages=[{
                    "role": "user",
                    "content": f"Create an N8N workflow for: {description}"
                }],
                system=system_prompt
            )

            # Parse workflow JSON from response
            workflow_json = self._extract_json(response.content[0].text)

            # Validate basic structure
            workflow = self._validate_workflow(workflow_json)

            logger.info("✅ Workflow built successfully")
            return workflow

        except Exception as e:
            logger.error(f"Workflow build error: {e}")
            raise

    def _get_system_prompt(self) -> str:
        '''Get system prompt for workflow generation'''
        return '''You are an expert N8N workflow builder.

Generate N8N workflow JSON from natural language descriptions.

N8N Workflow Structure:
{
  "name": "Workflow Name",
  "nodes": [
    {
      "id": "trigger_node",
      "type": "n8n-nodes-base.webhook",
      "parameters": {...},
      "position": [250, 300]
    },
    {
      "id": "action_node",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {...},
      "position": [450, 300]
    }
  ],
  "connections": {
    "trigger_node": {
      "main": [[{"node": "action_node", "type": "main", "index": 0}]]
    }
  }
}

Common N8N Node Types:
- Triggers: webhook, schedule, emailTrigger
- Actions: httpRequest, gmail, slack, github
- Logic: if, switch, merge
- Data: set, function, code

Rules:
1. Return ONLY valid JSON
2. Include all required node parameters
3. Ensure proper connections between nodes
4. Use realistic node positioning
5. Include error handling where appropriate

Generate complete, working N8N workflows.'''

    def _extract_json(self, text: str) -> Dict:
        '''Extract JSON from Claude response'''
        # Remove markdown code blocks if present
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]

        return json.loads(text.strip())

    def _validate_workflow(self, workflow: Dict) -> Dict:
        '''Validate basic workflow structure'''
        required_fields = ["name", "nodes", "connections"]

        for field in required_fields:
            if field not in workflow:
                raise ValueError(f"Missing required field: {field}")

        if not workflow["nodes"]:
            raise ValueError("Workflow must have at least one node")

        return workflow

    def _load_templates(self) -> Dict[str, Dict]:
        '''Load pre-built workflow templates'''
        # Will expand with actual templates
        return {
            "github_to_slack": {},
            "email_to_sheet": {},
            "rss_to_twitter": {},
        }

    def _create_template_workflow(self, description: str) -> Dict[str, Any]:
        '''Create a basic template workflow when AI is unavailable'''
        return {
            "name": f"Workflow: {description[:50]}",
            "nodes": [
                {
                    "id": "trigger",
                    "type": "n8n-nodes-base.manualTrigger",
                    "parameters": {},
                    "position": [250, 300]
                }
            ],
            "connections": {},
            "settings": {
                "executionOrder": "v1"
            }
        }
