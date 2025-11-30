"""
Agent Runtime - Execute agents in isolated environments with real tool access
"""

import asyncio
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional
import os

from loguru import logger


class AgentRuntime:
    """Runtime environment for executing agents with real tool access"""

    def __init__(self):
        """Initialize agent runtime"""
        self.active_sessions = {}
        self.execution_history = []
        logger.info("🚀 Agent Runtime initialized")

    async def execute_agent_code(
        self,
        agent_id: str,
        code: str,
        environment: Dict[str, str] = None,
        timeout: int = 30
    ) -> Dict[str, Any]:
        """
        Execute agent-generated code in isolated environment
        
        Args:
            agent_id: Agent identifier
            code: Python code to execute
            environment: Environment variables
            timeout: Execution timeout in seconds
            
        Returns:
            Execution results with stdout, stderr, exit code
        """
        logger.info(f"🔧 Executing code for agent: {agent_id}")
        
        # Create temporary file for code
        with tempfile.NamedTemporaryFile(
            mode='w', 
            suffix='.py', 
            delete=False,
            encoding='utf-8'
        ) as f:
            f.write(code)
            temp_file = f.name
        
        try:
            # Build environment
            exec_env = os.environ.copy()
            if environment:
                exec_env.update(environment)
            
            # Execute code in subprocess
            result = subprocess.run(
                ['python', temp_file],
                capture_output=True,
                text=True,
                timeout=timeout,
                env=exec_env
            )
            
            execution_result = {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "exit_code": result.returncode,
                "agent_id": agent_id,
            }
            
            # Log execution
            self.execution_history.append({
                "agent_id": agent_id,
                "timestamp": str(asyncio.get_event_loop().time()),
                "result": execution_result
            })
            
            logger.success(f"✅ Code executed for {agent_id}")
            return execution_result
            
        except subprocess.TimeoutExpired:
            logger.error(f"❌ Execution timeout for {agent_id}")
            return {
                "success": False,
                "error": f"Execution timeout after {timeout}s",
                "agent_id": agent_id
            }
        except Exception as e:
            logger.error(f"❌ Execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "agent_id": agent_id
            }
        finally:
            # Cleanup temp file
            try:
                Path(temp_file).unlink()
            except Exception:
                pass

    async def deploy_agent_to_n8n(
        self,
        agent_config: Dict[str, Any],
        n8n_api_url: str,
        n8n_api_key: str
    ) -> Dict[str, Any]:
        """
        Deploy agent as N8N workflow
        
        Args:
            agent_config: Agent configuration
            n8n_api_url: N8N API URL
            n8n_api_key: N8N API key
            
        Returns:
            Deployment result with workflow ID
        """
        logger.info(f"🚀 Deploying agent to N8N: {agent_config['name']}")
        
        try:
            import aiohttp
            
            # Build N8N workflow from agent
            workflow = self._build_n8n_workflow(agent_config)
            
            # Deploy to N8N
            async with aiohttp.ClientSession() as session:
                headers = {
                    "X-N8N-API-KEY": n8n_api_key,
                    "Content-Type": "application/json"
                }
                
                async with session.post(
                    f"{n8n_api_url}/workflows",
                    json=workflow,
                    headers=headers
                ) as response:
                    if response.status in [200, 201]:
                        result = await response.json()
                        logger.success(f"✅ Agent deployed to N8N: {result.get('id')}")
                        return {
                            "success": True,
                            "workflow_id": result.get('id'),
                            "workflow_url": result.get('url'),
                            "agent_id": agent_config['agent_id']
                        }
                    else:
                        error_text = await response.text()
                        logger.error(f"❌ N8N deployment failed: {error_text}")
                        return {
                            "success": False,
                            "error": error_text,
                            "status_code": response.status
                        }
        except Exception as e:
            logger.error(f"❌ Deployment error: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def _build_n8n_workflow(self, agent_config: Dict[str, Any]) -> Dict[str, Any]:
        """Build N8N workflow JSON from agent config"""
        return {
            "name": f"Agent: {agent_config['name']}",
            "nodes": [
                {
                    "parameters": {
                        "httpMethod": "POST",
                        "path": f"agent/{agent_config['agent_id']}",
                        "responseMode": "responseNode"
                    },
                    "name": "Webhook",
                    "type": "n8n-nodes-base.webhook",
                    "typeVersion": 1,
                    "position": [250, 300]
                },
                {
                    "parameters": {
                        "modelId": agent_config.get('model', 'gemini-2.0-flash-exp'),
                        "prompt": agent_config.get('system_prompt', ''),
                        "options": {
                            "temperature": agent_config.get('temperature', 0.7),
                            "maxTokens": agent_config.get('max_tokens', 4096)
                        }
                    },
                    "name": "AI Agent",
                    "type": "n8n-nodes-base.ai",
                    "typeVersion": 1,
                    "position": [450, 300]
                },
                {
                    "parameters": {
                        "respondWith": "={{$json.response}}"
                    },
                    "name": "Respond",
                    "type": "n8n-nodes-base.respondToWebhook",
                    "typeVersion": 1,
                    "position": [650, 300]
                }
            ],
            "connections": {
                "Webhook": {"main": [[{"node": "AI Agent", "type": "main", "index": 0}]]},
                "AI Agent": {"main": [[{"node": "Respond", "type": "main", "index": 0}]]}
            },
            "active": True,
            "settings": {
                "executionOrder": "v1"
            }
        }

    async def test_agent_deployment(
        self,
        workflow_id: str,
        test_input: str,
        n8n_api_url: str,
        n8n_api_key: str
    ) -> Dict[str, Any]:
        """
        Test deployed agent by triggering workflow
        
        Args:
            workflow_id: N8N workflow ID
            test_input: Test message
            n8n_api_url: N8N API URL
            n8n_api_key: N8N API key
            
        Returns:
            Test execution results
        """
        logger.info(f"🧪 Testing workflow: {workflow_id}")
        
        try:
            import aiohttp
            
            async with aiohttp.ClientSession() as session:
                headers = {
                    "X-N8N-API-KEY": n8n_api_key,
                    "Content-Type": "application/json"
                }
                
                # Trigger workflow
                async with session.post(
                    f"{n8n_api_url}/workflows/{workflow_id}/execute",
                    json={"data": {"message": test_input}},
                    headers=headers
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        logger.success(f"✅ Test passed for workflow {workflow_id}")
                        return {
                            "success": True,
                            "execution_id": result.get('id'),
                            "output": result.get('data'),
                            "workflow_id": workflow_id
                        }
                    else:
                        error = await response.text()
                        logger.error(f"❌ Test failed: {error}")
                        return {
                            "success": False,
                            "error": error,
                            "status_code": response.status
                        }
        except Exception as e:
            logger.error(f"❌ Test error: {e}")
            return {
                "success": False,
                "error": str(e)
            }
