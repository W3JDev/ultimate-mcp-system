"""
Test N8N connection from orchestrator
"""
import os
import requests
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

def test_n8n_rest_api():
    """Test N8N REST API connection"""
    n8n_url = os.getenv("N8N_API_URL", "https://n8n-533751401713.us-central1.run.app/api/v1")
    n8n_key = os.getenv("N8N_API_KEY")
    
    logger.info(f"🔍 Testing N8N REST API: {n8n_url}")
    
    try:
        headers = {
            "X-N8N-API-KEY": n8n_key,
            "Accept": "application/json"
        }
        
        # Test 1: List workflows
        response = requests.get(
            f"{n8n_url}/workflows",
            headers=headers,
            timeout=10
        )
        
        logger.info(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            workflows = data.get("data", [])
            logger.success(f"✅ N8N REST API connected! Found {len(workflows)} workflows")
            return True
        else:
            logger.error(f"❌ Failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Connection failed: {e}")
        return False

def test_n8n_mcp_client():
    """Test N8N MCP client"""
    logger.info("🔍 Testing N8N MCP Client...")
    
    try:
        from backend.integrations.n8n_mcp_client import test_n8n_mcp_connection
        
        result = test_n8n_mcp_connection()
        if result:
            logger.success("✅ N8N MCP client works!")
            return True
        else:
            logger.error("❌ N8N MCP client failed")
            return False
            
    except Exception as e:
        logger.error(f"❌ MCP client test failed: {e}")
        return False

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("🧪 N8N Connection Validation")
    logger.info("=" * 60)
    
    rest_ok = test_n8n_rest_api()
    print()
    mcp_ok = test_n8n_mcp_client()
    
    print("\n" + "=" * 60)
    if rest_ok and mcp_ok:
        logger.success("🎉 All N8N connections validated!")
    else:
        logger.warning("⚠️ Some connections failed - see errors above")
    print("=" * 60)
