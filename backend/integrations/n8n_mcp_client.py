"""
N8N MCP Server Client
Client for interacting with N8N's built-in MCP server
"""

import os
import requests
from typing import Any, Dict, List, Optional
from loguru import logger


class N8NMCPClient:
    """Client for N8N's built-in MCP server"""
    
    def __init__(
        self,
        base_url: Optional[str] = None,
        access_token: Optional[str] = None
    ):
        """
        Initialize N8N MCP client
        
        Args:
            base_url: N8N MCP server URL (default: from env)
            access_token: N8N MCP access token (default: from env)
        """
        self.base_url = base_url or os.getenv("N8N_MCP_SERVER_URL", "https://n8n-533751401713.us-central1.run.app/mcp-server/http")
        self.access_token = access_token or os.getenv("N8N_MCP_ACCESS_TOKEN")
        
        self.headers = {
            "Content-Type": "application/json",
        }
        
        # N8N MCP uses X-N8N-Token header for authentication
        if self.access_token:
            self.headers["X-N8N-Token"] = self.access_token
        
        logger.info(f"🔗 N8N MCP Client initialized: {self.base_url}")
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """
        List available N8N MCP tools/workflows
        
        Returns:
            List of available tools
        """
        try:
            # N8N MCP uses JSON-RPC 2.0 protocol
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/list",
                "params": {}
            }
            
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            
            data = response.json()
            tools = data.get("result", {}).get("tools", [])
            logger.info(f"✅ Listed {len(tools)} N8N MCP tools")
            return tools
            
        except Exception as e:
            logger.error(f"❌ Failed to list N8N MCP tools: {e}")
            return []
    
    def execute_workflow(
        self,
        workflow_id: str,
        input_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute a workflow via N8N MCP
        
        Args:
            workflow_id: Workflow ID to execute
            input_data: Input data for workflow
            
        Returns:
            Execution result
        """
        try:
            # N8N MCP uses JSON-RPC 2.0 protocol
            payload = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": f"workflow_{workflow_id}",
                    "arguments": input_data or {}
                }
            }
            
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            
            data = response.json()
            result = data.get("result", {})
            logger.info(f"✅ Executed workflow {workflow_id}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Failed to execute workflow {workflow_id}: {e}")
            return {"error": str(e)}
    
    def get_workflow_schema(self, workflow_id: str) -> Dict[str, Any]:
        """
        Get workflow input/output schema
        
        Args:
            workflow_id: Workflow ID
            
        Returns:
            Workflow schema
        """
        try:
            # N8N MCP uses JSON-RPC 2.0 protocol
            payload = {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/get",
                "params": {
                    "name": f"workflow_{workflow_id}"
                }
            }
            
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            
            data = response.json()
            schema = data.get("result", {})
            logger.info(f"✅ Got schema for workflow {workflow_id}")
            return schema
            
        except Exception as e:
            logger.error(f"❌ Failed to get workflow schema: {e}")
            return {}
    
    def list_available_workflows(self) -> List[Dict[str, Any]]:
        """
        List workflows available via MCP
        
        Returns:
            List of workflows with MCP access enabled
        """
        tools = self.list_tools()
        workflows = []
        
        for tool in tools:
            if tool.get("name", "").startswith("workflow_"):
                workflows.append({
                    "id": tool["name"].replace("workflow_", ""),
                    "name": tool.get("description", "Unnamed Workflow"),
                    "schema": tool.get("inputSchema", {})
                })
        
        logger.info(f"📋 Found {len(workflows)} MCP-enabled workflows")
        return workflows
    
    def test_connection(self) -> bool:
        """
        Test connection to N8N MCP server
        
        Returns:
            True if connection successful
        """
        try:
            tools = self.list_tools()
            logger.info(f"✅ N8N MCP server connection successful ({len(tools)} tools)")
            return True
        except Exception as e:
            logger.error(f"❌ N8N MCP server connection failed: {e}")
            return False


# Convenience function for quick testing
def test_n8n_mcp_connection():
    """Test N8N MCP server connection"""
    client = N8NMCPClient()
    
    print("\n🔍 Testing N8N MCP Server Connection...\n")
    
    # Test connection
    if client.test_connection():
        print("✅ Connection successful!")
        
        # List workflows
        workflows = client.list_available_workflows()
        print(f"\n📋 Available Workflows ({len(workflows)}):")
        for wf in workflows:
            print(f"  • {wf['id']}: {wf['name']}")
        
        return True
    else:
        print("❌ Connection failed!")
        return False


if __name__ == "__main__":
    test_n8n_mcp_connection()
