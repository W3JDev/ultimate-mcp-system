#!/usr/bin/env python3
'''
Ultimate MCP System - Main Entry Point
Master Orchestrator that routes requests to appropriate MCP servers
'''
import os
import gradio as gr
from dotenv import load_dotenv
from loguru import logger
from orchestrator import MCPOrchestrator
from memory import MemoryManager

# Load environment variables
load_dotenv()

# Configure logging
logger.add("logs/mcp_system.log", rotation="1 day", retention="7 days")

def main():
    '''Initialize and launch the Ultimate MCP System'''

    logger.info("🚀 Starting Ultimate MCP System")

    # Verify API keys
    required_keys = ["ANTHROPIC_API_KEY", "OPENAI_API_KEY"]
    missing_keys = [k for k in required_keys if not os.getenv(k)]

    if missing_keys:
        logger.error(f"❌ Missing API keys: {', '.join(missing_keys)}")
        print(f"\n⚠️  Missing required API keys: {', '.join(missing_keys)}")
        print("Please add them to backend/.env file")
        return

    # Initialize components
    logger.info("📦 Initializing components...")
    memory = MemoryManager()
    orchestrator = MCPOrchestrator(memory)

    # Create Gradio interface
    with gr.Blocks(theme=gr.themes.Soft(), title="Ultimate MCP System") as demo:
        gr.Markdown('''
        # 🤖 Ultimate MCP System
        **All-in-one MCP Orchestrator: N8N + Agents + Local Control**
        ''')

        with gr.Tab("💬 Chat"):
            chatbot = gr.Chatbot(height=600, label="MCP Assistant")
            msg = gr.Textbox(
                placeholder="Ask me to automate workflows, create agents, or control your PC...",
                show_label=False,
                container=False
            )
            clear = gr.Button("Clear")

            def respond(message, chat_history):
                '''Process user message through orchestrator'''
                logger.info(f"📨 User: {message}")

                # Route through orchestrator
                response = orchestrator.process(message)

                logger.info(f"📤 Assistant: {response[:100]}...")
                chat_history.append((message, response))
                return "", chat_history

            msg.submit(respond, [msg, chatbot], [msg, chatbot])
            clear.click(lambda: None, None, chatbot, queue=False)

            gr.Examples(
                examples=[
                    "Create an N8N workflow that monitors GitHub PRs",
                    "Build a CrewAI agent team for code review",
                    "Open VS Code and run my tests",
                    "Deploy my app to GCP Cloud Run",
                ],
                inputs=msg
            )

        with gr.Tab("📊 Status"):
            gr.Markdown('''
            ## System Status

            ### Available MCPs:
            - ✅ Master Orchestrator
            - 🔜 N8N Automation MCP
            - 🔜 Agent Builder MCP
            - 🔜 Local Control MCP
            - 🔜 Cloud Services MCP

            ### Memory:
            - Short-term: Active
            - Long-term: ChromaDB (ready)
            ''')

    # Launch
    logger.info("✅ All systems ready")
    print("\n" + "="*60)
    print("✅ Ultimate MCP System Running")
    print("🌐 Access at: http://localhost:7860")
    print("📚 Docs: https://github.com/W3JDev/ultimate-mcp-system")
    print("="*60 + "\n")

    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        mcp_server=True  # Enable MCP server mode
    )

if __name__ == "__main__":
    main()
