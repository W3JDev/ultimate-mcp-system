"""
Quick test script for real ADK agents with Anthropic API
"""
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

sys.path.insert(0, "backend/mcp_servers/agent_builder")

from adk_integration import ADKIntegration
from loguru import logger

# Test ADK agent
print("="*60)
print("Testing Real ADK Agent with Anthropic API")
print("="*60)

adk = ADKIntegration()

# Create an agent
print("\n1. Creating agent...")
result = adk.create_agent(
    name="Test Assistant",
    description="A helpful coding assistant",
    capabilities=["code_execution", "web_search"],
    model="gemini-2.0-flash-exp"
)

if result["success"]:
    agent_id = result["agent_id"]
    print(f"✅ Agent created: {agent_id}")
    print(f"   Model: {result['agent']['model']}")
    print(f"   Capabilities: {result['agent']['capabilities']}")
    
    # Execute the agent
    print("\n2. Executing agent...")
    exec_result = adk.execute_agent(
        agent_id=agent_id,
        user_message="Write a Python function to calculate fibonacci sequence. Keep it simple."
    )
    
    if exec_result["success"]:
        print(f"✅ Agent responded!")
        print(f"\n{'='*60}")
        print(f"Response:\n")
        print(exec_result["response"])
        print(f"\n{'='*60}")
        print(f"Model: {exec_result['usage']['model']}")
        print(f"Prompt length: {exec_result['usage']['prompt_length']} chars")
    else:
        print(f"❌ Execution failed: {exec_result['error']}")
else:
    print(f"❌ Agent creation failed: {result.get('error', 'Unknown error')}")
