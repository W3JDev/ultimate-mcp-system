#!/usr/bin/env python3
"""
Ultimate MCP System - Main Entry Point (FastAPI Version)
Master Orchestrator that routes requests to appropriate MCP servers
"""
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from loguru import logger
from memory import MemoryManager
from orchestrator import MCPOrchestrator
from tools import ToolRegistry, N8N_TOOLS, AGENT_TOOLS, LOCAL_TOOLS

# Load environment variables
load_dotenv()

# Configure logging
logger.add("logs/mcp_system.log", rotation="1 day", retention="7 days")


def main():
    """Initialize and launch the Ultimate MCP System"""

    logger.info("🚀 Starting Ultimate MCP System")

    # Verify API keys
    required_keys = ["ANTHROPIC_API_KEY", "OPENAI_API_KEY"]
    missing_keys = [k for k in required_keys if not os.getenv(k)]

    if missing_keys:
        logger.warning(f"⚠️ Using test API keys for Phase 1 testing")

    # Initialize components
    logger.info("📦 Initializing components...")
    memory = MemoryManager()
    orchestrator = MCPOrchestrator(memory)
    
    # Initialize tool registry
    logger.info("🔧 Initializing tool registry...")
    tool_registry = ToolRegistry()
    
    # Register all tools
    for tool in N8N_TOOLS:
        tool_registry.register(tool)
    for tool in AGENT_TOOLS:
        tool_registry.register(tool)
    for tool in LOCAL_TOOLS:
        tool_registry.register(tool)
    
    logger.info(f"✅ Registered {len(tool_registry)} tools")

    # Create FastAPI app
    app = FastAPI(title="Ultimate MCP System", version="1.0.0")

    @app.get("/", response_class=HTMLResponse)
    async def root():
        """Serve welcome page"""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>🤖 Ultimate MCP System</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 50px; }
                .container { max-width: 800px; margin: 0 auto; }
                h1 { color: #333; }
                .status { background: #f0f0f0; padding: 20px; border-radius: 5px; }
                .feature { margin: 10px 0; }
                code { background: #f5f5f5; padding: 2px 5px; border-radius: 3px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🤖 Ultimate MCP System - Phase 1</h1>
                <p><strong>All-in-one MCP Orchestrator: N8N + Agents + Local Control</strong></p>
                
                <div class="status">
                    <h2>✅ System Status</h2>
                    <p><strong>Status:</strong> Running</p>
                    <p><strong>Version:</strong> 1.0.0</p>
                    
                    <h3>Available Endpoints:</h3>
                    <ul>
                        <li><code>GET /</code> - This welcome page</li>
                        <li><code>POST /process</code> - Send a request to the orchestrator</li>
                        <li><code>GET /status</code> - System status</li>
                        <li><code>GET /tools/list</code> - List all available MCP tools</li>
                        <li><code>POST /tools/execute</code> - Execute a specific tool</li>
                        <li><code>GET /docs</code> - Interactive API documentation</li>
                    </ul>
                    
                    <h3>Phase 1 Components:</h3>
                    <ul>
                        <li>✅ Master Orchestrator - AI-powered intent routing</li>
                        <li>✅ Memory Manager - Context management</li>
                        <li>✅ Logging System - Real-time logs</li>
                        <li>✅ FastAPI Server - REST API</li>
                    </ul>
                    
                    <h3>Phase 2 Complete - MCP Tools:</h3>
                    <ul>
                        <li>✅ N8N Automation Tools (4 tools)</li>
                        <li>✅ Agent Builder Tools (6 tools)</li>
                        <li>✅ Local Control Tools (7 tools)</li>
                        <li>🔜 Cloud Services MCP</li>
                    </ul>
                </div>
                
                <p style="margin-top: 30px; color: #666;">
                    📚 <a href="https://github.com/W3JDev/ultimate-mcp-system">GitHub</a> | 
                    📖 <a href="/docs">API Docs</a>
                </p>
            </div>
        </body>
        </html>
        """

    @app.get("/status")
    async def status():
        """Get system status"""
        return {
            "status": "running",
            "version": "1.0.0",
            "components": {
                "orchestrator": "active",
                "memory": "active",
                "api": "active",
                "tools": "active"
            },
            "tools": {
                "total": len(tool_registry),
                "categories": tool_registry.get_categories()
            }
        }

    @app.get("/tools/list")
    async def list_tools(category: str = None):
        """List all available MCP tools"""
        tools = tool_registry.list_tools(category=category)
        return {
            "status": "success",
            "total": len(tools),
            "category": category or "all",
            "tools": tools
        }

    @app.post("/tools/execute")
    async def execute_tool(request: dict):
        """Execute a specific tool by name"""
        tool_name = request.get("tool")
        params = request.get("params", {})

        if not tool_name:
            return {"error": "No tool name provided"}

        logger.info(f"🔧 Executing tool: {tool_name}")

        result = tool_registry.execute_tool(tool_name, **params)
        return result

    @app.post("/process")
    async def process(request: dict):
        """Process a user request through the orchestrator"""
        message = request.get("message", "")

        if not message:
            return {"error": "No message provided"}

        logger.info(f"📨 User: {message}")

        try:
            response = orchestrator.process(message)
            logger.info(f"💬 Assistant: {response[:100]}...")

            return {"status": "success", "message": message, "response": response}
        except Exception as e:
            logger.error(f"❌ Error: {str(e)}")
            return {"status": "error", "message": message, "error": str(e)}

    # Launch
    logger.info("✅ All systems ready")
    print("\n" + "=" * 60)
    print("[OK] Ultimate MCP System Running")
    print("[WEB] Access at: http://localhost:7860")
    print("[DOCS] API Docs: http://localhost:7860/docs")
    print("[GIT] Docs: https://github.com/W3JDev/ultimate-mcp-system")
    print("=" * 60 + "\n")

    return app


if __name__ == "__main__":
    import uvicorn

    app = main()
    uvicorn.run(app, host="0.0.0.0", port=7860)
