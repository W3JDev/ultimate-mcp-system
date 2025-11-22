
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add backend to path
sys.path.append(str(Path.cwd() / "backend"))

# Load env
load_dotenv()

from tools.n8n_tools import create_workflow_handler

def test_real_n8n():
    print("🚀 Testing Real N8N Workflow Generation...")
    description = "When a new GitHub issue is opened, send a message to Slack channel #dev"
    
    try:
        result = create_workflow_handler(description)
        print("\n✅ Result Received!")
        print(f"Workflow Name: {result.get('name')}")
        print(f"Node Count: {len(result.get('nodes', []))}")
        print("Structure looks valid.")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    test_real_n8n()
