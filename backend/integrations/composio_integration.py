"""
Composio Integration - Connect 100+ productivity tools to AI agents
Provides email, calendar, Slack, GitHub, and more via unified API

NOTE: Using REST API approach due to Python 3.14 compatibility issues with SDK
"""

import os
import subprocess
import json
from typing import Dict, Any, List, Optional
from loguru import logger

# Use REST API instead of SDK for Python 3.14 compatibility
COMPOSIO_AVAILABLE = True  # Using CLI/REST approach


class ComposioIntegration:
    """Wrapper for Composio MCP integration using REST API"""
    
    BASE_URL = "https://backend.composio.dev/api/v1"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Composio client
        
        Args:
            api_key: Composio API key (defaults to COMPOSIO_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("COMPOSIO_API_KEY")
        if not self.api_key:
            logger.warning("⚠️ COMPOSIO_API_KEY not set - get it from https://app.composio.dev")
            self.client = None
        else:
            self.client = True  # Flag to indicate API key is set
            logger.success("✅ Composio client initialized")
    
    def _make_request(self, endpoint: str, method: str = "GET", data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make REST API request to Composio"""
        import requests
        
        if not self.api_key:
            return {"error": "API key not configured"}
        
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        
        url = f"{self.BASE_URL}/{endpoint}"
        
        try:
            if method == "GET":
                response = requests.get(url, headers=headers)
            elif method == "POST":
                response = requests.post(url, headers=headers, json=data)
            else:
                return {"error": f"Unsupported method: {method}"}
            
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"❌ API request failed: {e}")
            return {"error": str(e)}
    
    def list_available_apps(self) -> List[Dict[str, Any]]:
        """
        List all available Composio apps (Gmail, Slack, GitHub, etc.)
        
        Returns:
            List of app metadata dicts with {name, key, description, tags}
        """
        if not self.client:
            return []
        
        try:
            response = self._make_request("apps")
            
            if "error" in response:
                logger.error(f"❌ API error: {response['error']}")
                return []
            
            apps = response.get("items", [])
            
            result = []
            for app in apps[:50]:  # Limit to first 50 for display
                result.append({
                    "name": app.get('name', 'Unknown'),
                    "key": app.get('key', 'unknown'),
                    "description": app.get('description', 'No description'),
                    "tags": app.get('tags', [])
                })
            
            logger.info(f"📦 Found {len(result)} Composio apps")
            return result
            
        except Exception as e:
            logger.error(f"❌ Failed to list apps: {e}")
            return []
    
    def list_app_actions(self, app_key: str) -> List[Dict[str, Any]]:
        """
        List all actions for a specific app
        
        Args:
            app_key: App identifier (e.g., 'gmail', 'slack', 'github')
        
        Returns:
            List of action metadata dicts
        """
        if not self.client:
            return []
        
        try:
            response = self._make_request(f"actions?appKey={app_key}")
            
            if "error" in response:
                logger.error(f"❌ API error: {response['error']}")
                return []
            
            actions = response.get("items", [])
            
            result = []
            for action in actions[:20]:  # Limit to first 20
                result.append({
                    "name": action.get('name', 'Unknown'),
                    "key": action.get('key', 'unknown'),
                    "description": action.get('description', 'No description'),
                    "parameters": action.get('parameters', {})
                })
            
            logger.info(f"🔧 Found {len(result)} actions for {app_key}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Failed to list actions for {app_key}: {e}")
            return []
    
    def execute_action(
        self,
        app_key: str,
        action_key: str,
        parameters: Dict[str, Any],
        entity_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute a Composio action
        
        Args:
            app_key: App identifier (e.g., 'gmail')
            action_key: Action to execute (e.g., 'GMAIL_SEND_EMAIL')
            parameters: Action parameters as dict
            entity_id: Optional entity ID for user-specific actions
        
        Returns:
            Action execution result
        """
        if not self.client:
            return {"success": False, "error": "Composio client not initialized"}
        
        try:
            logger.info(f"🚀 Executing {app_key}.{action_key}")
            
            # Execute action via REST API
            payload = {
                "actionName": action_key,
                "input": parameters
            }
            if entity_id:
                payload["entityId"] = entity_id
            
            response = self._make_request("actions/execute", method="POST", data=payload)
            
            if "error" in response:
                logger.error(f"❌ Action failed: {response['error']}")
                return {
                    "success": False,
                    "error": response['error'],
                    "action": action_key
                }
            
            logger.success(f"✅ Action completed: {action_key}")
            return {
                "success": True,
                "data": response,
                "action": action_key
            }
            
        except Exception as e:
            logger.error(f"❌ Action execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "action": action_key
            }
    
    def get_connected_accounts(self) -> List[Dict[str, Any]]:
        """
        Get list of user's connected accounts
        
        Returns:
            List of connected account metadata
        """
        if not self.client:
            return []
        
        try:
            response = self._make_request("connectedAccounts")
            
            if "error" in response:
                logger.error(f"❌ API error: {response['error']}")
                return []
            
            accounts = response.get("items", [])
            
            result = []
            for account in accounts:
                result.append({
                    "id": account.get('id', 'unknown'),
                    "appName": account.get('appName', 'Unknown'),
                    "status": account.get('status', 'unknown')
                })
            
            logger.info(f"👤 Found {len(result)} connected accounts")
            return result
            
        except Exception as e:
            logger.error(f"❌ Failed to get connected accounts: {e}")
            return []
    
    def connect_account(self, app_key: str, entity_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Initiate OAuth flow to connect an account
        
        Args:
            app_key: App to connect (e.g., 'gmail')
            entity_id: Optional entity ID
        
        Returns:
            Connection URL and metadata
        """
        if not self.client:
            return {"success": False, "error": "Composio client not initialized"}
        
        try:
            payload = {"app": app_key}
            if entity_id:
                payload["entityId"] = entity_id
            
            response = self._make_request("connectedAccounts", method="POST", data=payload)
            
            if "error" in response:
                logger.error(f"❌ Connection failed: {response['error']}")
                return {
                    "success": False,
                    "error": response['error']
                }
            
            auth_url = response.get('redirectUrl') or response.get('authUrl', '')
            
            logger.info(f"🔗 Generated connection URL for {app_key}")
            return {
                "success": True,
                "auth_url": auth_url,
                "app": app_key,
                "message": f"Visit the URL to connect {app_key}"
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to generate connection: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def search_tools(self, query: str) -> List[Dict[str, Any]]:
        """
        Search Composio tools by keyword
        
        Args:
            query: Search query (e.g., 'email', 'calendar', 'slack')
        
        Returns:
            List of matching apps and actions
        """
        if not self.client:
            return []
        
        try:
            # Search apps
            apps = self.list_available_apps()
            matching_apps = [
                app for app in apps 
                if query.lower() in app['name'].lower() or 
                   query.lower() in app['description'].lower()
            ]
            
            logger.info(f"🔍 Found {len(matching_apps)} apps matching '{query}'")
            return matching_apps
            
        except Exception as e:
            logger.error(f"❌ Search failed: {e}")
            return []
    
    def get_integration_status(self) -> Dict[str, Any]:
        """
        Get status of Composio integration
        
        Returns:
            Status metadata including available apps, connected accounts, health
        """
        if not self.client:
            return {
                "available": False,
                "error": "API key not configured",
                "apps": 0,
                "connected_accounts": 0
            }
        
        try:
            apps = self.list_available_apps()
            accounts = self.get_connected_accounts()
            
            return {
                "available": True,
                "api_key_set": bool(self.api_key),
                "apps_available": len(apps),
                "connected_accounts": len(accounts),
                "top_apps": [app['name'] for app in apps[:10]],
                "message": f"✅ Composio ready with {len(apps)} apps"
            }
            
        except Exception as e:
            logger.error(f"❌ Status check failed: {e}")
            return {
                "available": False,
                "error": str(e),
                "apps": 0,
                "connected_accounts": 0
            }


# Convenience function for quick initialization
def get_composio_client(api_key: Optional[str] = None) -> ComposioIntegration:
    """Get initialized Composio client"""
    return ComposioIntegration(api_key=api_key)


if __name__ == "__main__":
    # Test the integration
    print("🧪 Testing Composio Integration...")
    
    client = get_composio_client()
    status = client.get_integration_status()
    
    print(f"\n📊 Status: {status}")
    
    if status['available']:
        print(f"\n✅ Composio is ready!")
        print(f"📦 {status['apps_available']} apps available")
        print(f"👤 {status['connected_accounts']} accounts connected")
        
        # Show top apps
        apps = client.list_available_apps()
        if apps:
            print("\n🔝 Top 10 Apps:")
            for app in apps[:10]:
                print(f"  - {app['name']}: {app['description'][:60]}...")
    else:
        print(f"\n⚠️ Composio not configured: {status.get('error', 'Unknown error')}")
        print("💡 Get your API key from: https://app.composio.dev")
