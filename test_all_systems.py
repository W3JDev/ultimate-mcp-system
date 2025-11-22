#!/usr/bin/env python3
"""
Complete MCP System Test - REAL WORLD VALIDATION
Tests all 3 MCP components with actual API calls
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add backend to path
sys.path.append(str(Path.cwd() / "backend"))
load_dotenv()

print("🚀 ULTIMATE MCP SYSTEM - REAL WORLD TEST")
print("=" * 50)

def test_1_n8n_workflow():
    """Test N8N workflow generation with Claude API"""
    print("\n1️⃣ Testing N8N Workflow Generation...")
    try:
        from tools.n8n_tools import create_workflow_handler
        
        description = "When a new GitHub issue is opened, send a message to Slack channel #dev"
        result = create_workflow_handler(description)
        
        if "error" in result:
            print(f"❌ N8N Error: {result['error']}")
            return False
        
        print("✅ N8N Workflow Generated!")
        print(f"   - Name: {result.get('name', 'Unknown')}")
        print(f"   - Nodes: {len(result.get('nodes', []))}")
        return True
    except Exception as e:
        print(f"❌ N8N Exception: {e}")
        return False

def test_2_agent_creation():
    """Test Agent creation"""
    print("\n2️⃣ Testing Agent Builder...")
    try:
        from tools.agent_tools import create_adk_agent_handler
        
        result = create_adk_agent_handler(
            name="TestAgent",
            model="gpt-4",
            tools=["github", "slack"],
            system_prompt="You are a helpful assistant"
        )
        
        print("✅ Agent Created!")
        print(f"   - ID: {result['id']}")
        print(f"   - Type: {result['type']}")
        print(f"   - Model: {result['model']}")
        return True
    except Exception as e:
        print(f"❌ Agent Exception: {e}")
        return False

def test_3_local_control():
    """Test Local System Control"""
    print("\n3️⃣ Testing Local Control...")
    try:
        from tools.local_tools import get_system_info_handler, list_processes_handler
        
        # Test system info
        sys_info = get_system_info_handler()
        print("✅ System Info Retrieved!")
        print(f"   - OS: {sys_info['os']['system']}")
        print(f"   - CPU Cores: {sys_info['cpu']['cores']}")
        
        # Test process listing
        processes = list_processes_handler(limit=3)
        print("✅ Process List Retrieved!")
        print(f"   - Found {len(processes)} processes")
        
        return True
    except Exception as e:
        print(f"❌ Local Control Exception: {e}")
        return False

def test_4_orchestrator():
    """Test Master Orchestrator"""
    print("\n4️⃣ Testing Master Orchestrator...")
    try:
        from memory import MemoryManager
        from orchestrator import MCPOrchestrator
        
        memory = MemoryManager()
        orchestrator = MCPOrchestrator(memory)
        
        # Test basic processing
        response = orchestrator.process("What's my system information?")
        
        print("✅ Orchestrator Working!")
        print(f"   - Response length: {len(response)} chars")
        return True
    except Exception as e:
        print(f"❌ Orchestrator Exception: {e}")
        return False

def main():
    """Run all tests"""
    tests = [
        test_1_n8n_workflow,
        test_2_agent_creation, 
        test_3_local_control,
        test_4_orchestrator
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    # Final Summary
    print("\n" + "=" * 50)
    print("📊 FINAL RESULTS")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total-passed}/{total}")
    
    if passed == total:
        print("\n🎉 ALL SYSTEMS OPERATIONAL!")
        print("✅ Ready for hackathon submission!")
    else:
        print("\n⚠️  Some components need attention")
        print("🔧 Check errors above for fixes needed")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)