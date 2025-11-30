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
from tools import AGENT_TOOLS, LOCAL_TOOLS, N8N_TOOLS, MCP_HUB_TOOLS, ToolRegistry

# Load environment variables
load_dotenv()

# Configure logging
logger.add("logs/mcp_system.log", rotation="1 day", retention="7 days")


def main():
    """Initialize and launch the Ultimate MCP System"""

    logger.info(f"🚀 Starting W3J MCP Hub")

    # Verify API keys
    required_keys = ["ANTHROPIC_API_KEY", "OPENAI_API_KEY"]
    missing_keys = [k for k in required_keys if not os.getenv(k)]

    if missing_keys:
        logger.warning(f"⚠️ Using test API keys for Phase 1 testing")

    # Initialize tool registry first
    logger.info("🔧 Initializing tool registry...")
    tool_registry = ToolRegistry()

    # Register all tools
    for tool in N8N_TOOLS:
        tool_registry.register(tool)
    for tool in AGENT_TOOLS:
        tool_registry.register(tool)
    for tool in LOCAL_TOOLS:
        tool_registry.register(tool)
    
    # Register MCP Hub meta-tools
    logger.info("🌟 Registering MCP Hub meta-tools...")
    for tool in MCP_HUB_TOOLS:
        tool_registry.register(tool)

    tool_count = len(tool_registry._tools)
    logger.info(f"✅ Registered {tool_count} tools (including {len(MCP_HUB_TOOLS)} MCP Hub meta-tools)")

    # Initialize components with registry
    logger.info("📦 Initializing components...")
    memory = MemoryManager()
    orchestrator = MCPOrchestrator(memory, tool_registry)

    # Create FastAPI app
    app = FastAPI(title="Ultimate MCP System", version="1.0.0")

    @app.get("/favicon.ico")
    async def favicon():
        """Serve favicon"""
        return {"status": "ok"}

    @app.get("/", response_class=HTMLResponse)
    async def root():
        """Serve interactive chat interface"""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>🤖 Ultimate MCP Orchestrator - Chat Interface</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }
                
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    padding: 20px;
                }
                
                .chat-container {
                    width: 100%;
                    max-width: 900px;
                    height: 90vh;
                    background: white;
                    border-radius: 20px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                    display: flex;
                    flex-direction: column;
                    overflow: hidden;
                }
                
                .chat-header {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 25px 30px;
                    border-bottom: 2px solid rgba(255,255,255,0.1);
                }
                
                .chat-header h1 {
                    font-size: 24px;
                    margin-bottom: 5px;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                }
                
                .status-badge {
                    background: rgba(76, 217, 100, 0.9);
                    padding: 4px 12px;
                    border-radius: 12px;
                    font-size: 12px;
                    font-weight: 600;
                }
                
                .chat-subtitle {
                    font-size: 14px;
                    opacity: 0.9;
                    margin-top: 5px;
                }
                
                .chat-messages {
                    flex: 1;
                    overflow-y: auto;
                    padding: 30px;
                    background: #f8f9fa;
                }
                
                .message {
                    display: flex;
                    margin-bottom: 20px;
                    animation: fadeIn 0.3s ease-in;
                }
                
                @keyframes fadeIn {
                    from { opacity: 0; transform: translateY(10px); }
                    to { opacity: 1; transform: translateY(0); }
                }
                
                .message.user {
                    justify-content: flex-end;
                }
                
                .message-content {
                    max-width: 70%;
                    padding: 15px 20px;
                    border-radius: 18px;
                    position: relative;
                }
                
                .message.assistant .message-content {
                    background: white;
                    border: 2px solid #e0e0e0;
                    border-radius: 18px 18px 18px 4px;
                }
                
                .message.user .message-content {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    border-radius: 18px 18px 4px 18px;
                }
                
                .message-avatar {
                    width: 36px;
                    height: 36px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 18px;
                    margin: 0 12px;
                    flex-shrink: 0;
                }
                
                .message.assistant .message-avatar {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                }
                
                .message.user .message-avatar {
                    background: #4a5568;
                }
                
                .chat-input-container {
                    padding: 20px 30px;
                    background: white;
                    border-top: 2px solid #e0e0e0;
                }
                
                .chat-input-wrapper {
                    display: flex;
                    gap: 10px;
                    align-items: center;
                }
                
                #userInput {
                    flex: 1;
                    padding: 15px 20px;
                    border: 2px solid #e0e0e0;
                    border-radius: 25px;
                    font-size: 15px;
                    outline: none;
                    transition: all 0.3s;
                }
                
                #userInput:focus {
                    border-color: #667eea;
                    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
                }
                
                #sendBtn {
                    padding: 15px 30px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    border: none;
                    border-radius: 25px;
                    font-size: 15px;
                    font-weight: 600;
                    cursor: pointer;
                    transition: all 0.3s;
                }
                
                #sendBtn:hover:not(:disabled) {
                    transform: translateY(-2px);
                    box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
                }
                
                #sendBtn:disabled {
                    opacity: 0.6;
                    cursor: not-allowed;
                }
                
                .quick-actions {
                    display: flex;
                    gap: 10px;
                    margin-top: 10px;
                    flex-wrap: wrap;
                }
                
                .quick-action-btn {
                    padding: 8px 16px;
                    background: #f0f0f0;
                    border: 1px solid #e0e0e0;
                    border-radius: 20px;
                    font-size: 13px;
                    cursor: pointer;
                    transition: all 0.2s;
                }
                
                .quick-action-btn:hover {
                    background: #667eea;
                    color: white;
                    border-color: #667eea;
                }
                
                .typing-indicator {
                    display: none;
                    align-items: center;
                    gap: 5px;
                    padding: 15px 20px;
                }
                
                .typing-indicator.active {
                    display: flex;
                }
                
                .typing-dot {
                    width: 8px;
                    height: 8px;
                    background: #999;
                    border-radius: 50%;
                    animation: typing 1.4s infinite;
                }
                
                .typing-dot:nth-child(2) { animation-delay: 0.2s; }
                .typing-dot:nth-child(3) { animation-delay: 0.4s; }
                
                @keyframes typing {
                    0%, 60%, 100% { transform: translateY(0); }
                    30% { transform: translateY(-10px); }
                }
                
                .welcome-message {
                    text-align: center;
                    padding: 40px 20px;
                    color: #666;
                }
                
                .welcome-message h2 {
                    margin-bottom: 10px;
                    color: #333;
                }
                
                .capabilities {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 15px;
                    margin-top: 20px;
                }
                
                .capability-card {
                    background: white;
                    padding: 15px;
                    border-radius: 10px;
                    border: 2px solid #e0e0e0;
                    text-align: left;
                }
                
                .capability-card h3 {
                    font-size: 16px;
                    margin-bottom: 5px;
                    color: #667eea;
                }
                
                .capability-card p {
                    font-size: 13px;
                    color: #666;
                }
            </style>
        </head>
        <body>
            <div class="chat-container">
                <div class="chat-header">
                    <h1>
                        🤖 Ultimate MCP Orchestrator
                        <span class="status-badge">● ONLINE</span>
                    </h1>
                    <div class="chat-subtitle">
                        AI-powered automation system • N8N + Agents + Local Control
                    </div>
                </div>
                
                <div class="chat-messages" id="chatMessages">
                    <div class="welcome-message">
                        <h2>👋 Welcome to Your MCP Orchestrator!</h2>
                        <p>I can help you automate workflows, create AI agents, and control your system.</p>
                        
                        <div class="capabilities">
                            <div class="capability-card">
                                <h3>🔄 Workflow Automation</h3>
                                <p>Create and deploy N8N workflows</p>
                            </div>
                            <div class="capability-card">
                                <h3>🤖 AI Agents</h3>
                                <p>Build agents with 5 frameworks</p>
                            </div>
                            <div class="capability-card">
                                <h3>💻 Local Control</h3>
                                <p>Manage files and system tasks</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="chat-input-container">
                    <div class="quick-actions">
                        <button class="quick-action-btn" onclick="sendQuick('What can you do?')">
                            💡 What can you do?
                        </button>
                        <button class="quick-action-btn" onclick="sendQuick('Create an AI agent')">
                            🤖 Create AI agent
                        </button>
                        <button class="quick-action-btn" onclick="sendQuick('List my files')">
                            📁 List files
                        </button>
                        <button class="quick-action-btn" onclick="sendQuick('Show system info')">
                            💻 System info
                        </button>
                    </div>
                    
                    <div class="chat-input-wrapper">
                        <input 
                            type="text" 
                            id="userInput" 
                            placeholder="Ask me anything... (e.g., 'Create a LinkedIn post' or 'Build a research agent')"
                            onkeypress="if(event.key==='Enter') sendMessage()"
                        />
                        <button id="sendBtn" onclick="sendMessage()">Send</button>
                    </div>
                </div>
            </div>
            
            <script>
                const chatMessages = document.getElementById('chatMessages');
                const userInput = document.getElementById('userInput');
                const sendBtn = document.getElementById('sendBtn');
                
                function addMessage(content, isUser = false) {
                    const messageDiv = document.createElement('div');
                    messageDiv.className = `message ${isUser ? 'user' : 'assistant'}`;
                    
                    const avatar = document.createElement('div');
                    avatar.className = 'message-avatar';
                    avatar.textContent = isUser ? '👤' : '🤖';
                    
                    const contentDiv = document.createElement('div');
                    contentDiv.className = 'message-content';
                    
                    // Render markdown-like formatting
                    const formattedContent = formatMarkdown(content);
                    contentDiv.innerHTML = formattedContent;
                    
                    if (isUser) {
                        messageDiv.appendChild(contentDiv);
                        messageDiv.appendChild(avatar);
                    } else {
                        messageDiv.appendChild(avatar);
                        messageDiv.appendChild(contentDiv);
                    }
                    
                    // Remove welcome message if exists
                    const welcome = chatMessages.querySelector('.welcome-message');
                    if (welcome) welcome.remove();
                    
                    chatMessages.appendChild(messageDiv);
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                }
                
                function showTyping() {
                    const typingDiv = document.createElement('div');
                    typingDiv.className = 'message assistant';
                    typingDiv.id = 'typingIndicator';
                    
                    const avatar = document.createElement('div');
                    avatar.className = 'message-avatar';
                    avatar.textContent = '🤖';
                    
                    const indicator = document.createElement('div');
                    indicator.className = 'typing-indicator active';
                    indicator.innerHTML = '<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>';
                    
                    typingDiv.appendChild(avatar);
                    typingDiv.appendChild(indicator);
                    chatMessages.appendChild(typingDiv);
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                }
                
                function hideTyping() {
                    const typing = document.getElementById('typingIndicator');
                    if (typing) typing.remove();
                }
                
                async function sendMessage() {
                    const message = userInput.value.trim();
                    if (!message) return;
                    
                    // Add user message
                    addMessage(message, true);
                    userInput.value = '';
                    sendBtn.disabled = true;
                    
                    // Show typing indicator
                    showTyping();
                    
                    try {
                        const response = await fetch('/process', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ message: message })
                        });
                        
                        const data = await response.json();
                        hideTyping();
                        
                        if (data.status === 'success') {
                            addMessage(data.response);
                        } else {
                            addMessage('❌ Error: ' + (data.error || 'Unknown error occurred'));
                        }
                    } catch (error) {
                        hideTyping();
                        addMessage('❌ Connection error. Please check if the server is running.');
                    }
                    
                    sendBtn.disabled = false;
                    userInput.focus();
                }
                
                function sendQuick(text) {
                    userInput.value = text;
                    sendMessage();
                }
                
                function formatMarkdown(text) {
                    // Convert markdown to HTML with styling
                    let html = text
                        // Bold **text**
                        .replace(/\\*\\*(.*?)\\*\\*/g, '<strong style="color:#667eea;">$1</strong>')
                        // Code blocks ```
                        .replace(/```(.*?)```/gs, '<pre style="background:#f5f5f5;padding:10px;border-radius:5px;margin:10px 0;"><code>$1</code></pre>')
                        // Inline code `text`
                        .replace(/`(.*?)`/g, '<code style="background:#f5f5f5;padding:2px 6px;border-radius:3px;font-family:monospace;">$1</code>')
                        // Links [text](url)
                        .replace(/\\[(.*?)\\]\\((.*?)\\)/g, '<a href="$2" target="_blank" style="color:#667eea;">$1</a>')
                        // Bullet lists - (with emojis)
                        .replace(/^[-\\*] (.*$)/gim, '<li style="margin:5px 0;">$1</li>')
                        // Numbered lists
                        .replace(/^\\d+\\. (.*$)/gim, '<li style="margin:5px 0;">$1</li>');
                    
                    // Wrap lists
                    html = html.replace(/(<li.*<\\/li>)/s, '<ul style="margin:10px 0;padding-left:20px;">$1</ul>');
                    
                    // Line breaks
                    html = html.replace(/\\n\\n/g, '<br><br>').replace(/\\n/g, '<br>');
                    
                    return html;
                }
                
                // Focus input on load
                userInput.focus();
            </script>
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
                "tools": "active",
            },
            "tools": {
                "total": len(tool_registry),
                "categories": tool_registry.get_categories(),
            },
        }

    @app.get("/tools/list")
    async def list_tools(category: str = None):
        """List all available MCP tools"""
        tools = tool_registry.list_tools(category=category)
        return {
            "status": "success",
            "total": len(tools),
            "category": category or "all",
            "tools": tools,
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
    print("🤖 W3J MCP HUB - Master Orchestrator Running")
    print("[WEB] Chat Interface: http://localhost:7860")
    print("[DOCS] API Docs: http://localhost:7860/docs")
    print("[CREATOR] @W3JDev | https://github.com/W3JDev")
    print("=" * 60 + "\n")

    return app


if __name__ == "__main__":
    import uvicorn

    app = main()
    # Use PORT from environment (Cloud Run compatibility)
    port = int(os.getenv("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)
