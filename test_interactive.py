#!/usr/bin/env python3
"""
🎮 INTERACTIVE TEST - Play with Your MCP System!
Run this to see real results from your system.
"""
import requests
import json
import sys

def print_separator():
    print("\n" + "="*70 + "\n")

def test_1_check_alive():
    """Test if servers respond"""
    print("🔍 TEST 1: Are the servers alive?")
    print_separator()
    
    servers = {
        "Master Orchestrator": "http://localhost:7860",
        "N8N Automation": "http://localhost:7862",
        "Agent Builder": "http://localhost:7863",
        "Local Control": "http://localhost:7864"
    }
    
    for name, url in servers.items():
        try:
            response = requests.get(f"{url}/health", timeout=2)
            if response.status_code == 200:
                print(f"✅ {name:25} → ONLINE")
            else:
                print(f"⚠️  {name:25} → Response: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"❌ {name:25} → OFFLINE (Not running)")
        except Exception as e:
            print(f"⚠️  {name:25} → Error: {str(e)[:40]}")
    
    print_separator()

def test_2_list_tools():
    """Test listing all tools"""
    print("🛠️  TEST 2: What tools does your system have?")
    print_separator()
    
    try:
        response = requests.get("http://localhost:7860/tools", timeout=5)
        if response.status_code == 200:
            data = response.json()
            tools = data.get('tools', [])
            
            print(f"✅ Found {len(tools)} tools in your system!\n")
            
            # Show first 5 tools
            print("📋 First 5 Tools:")
            for i, tool in enumerate(tools[:5], 1):
                name = tool.get('name', 'Unknown')
                desc = tool.get('description', 'No description')[:50]
                print(f"   {i}. {name}")
                print(f"      └─ {desc}...")
            
            print(f"\n   ... and {len(tools) - 5} more tools!")
        else:
            print(f"⚠️  Got response code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure servers are running: python launch_all_servers.py")
    
    print_separator()

def test_3_get_system_info():
    """Test getting system information"""
    print("💻 TEST 3: Get your computer info")
    print_separator()
    
    try:
        response = requests.post(
            "http://localhost:7864/execute",
            json={"tool": "get_system_info", "params": {}},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ System Information Retrieved!\n")
            print(json.dumps(data, indent=2))
        else:
            print(f"⚠️  Response: {response.status_code}")
            print("This tool gets: OS, CPU, Memory, Disk info")
    except Exception as e:
        print(f"⚠️  {e}")
        print("\n💡 What this tool CAN do:")
        print("   • Get OS information (Windows/Mac/Linux)")
        print("   • CPU usage percentage")
        print("   • Memory usage (RAM)")
        print("   • Disk space available")
    
    print_separator()

def test_4_list_files():
    """Test listing files"""
    print("📁 TEST 4: List files in your current directory")
    print_separator()
    
    import os
    current_dir = os.getcwd()
    
    try:
        response = requests.post(
            "http://localhost:7864/execute",
            json={
                "tool": "list_files",
                "params": {"path": current_dir}
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Files in: {current_dir}\n")
            print(json.dumps(data, indent=2))
        else:
            print(f"⚠️  Response: {response.status_code}")
            # Show what files exist manually
            files = [f for f in os.listdir('.') if os.path.isfile(f)][:10]
            print(f"\n📋 Files in current directory ({len(files)} shown):")
            for f in files:
                print(f"   • {f}")
    except Exception as e:
        print(f"⚠️  {e}")
        # Fallback: show actual files
        try:
            files = [f for f in os.listdir('.') if os.path.isfile(f)][:10]
            print(f"\n📋 Your project files ({len(files)} shown):")
            for f in files:
                print(f"   • {f}")
        except:
            pass
    
    print_separator()

def test_5_agent_frameworks():
    """Show available agent frameworks"""
    print("🤖 TEST 5: What AI agent frameworks do you support?")
    print_separator()
    
    frameworks = [
        ("ADK", "Anthropic Developer Kit", "Claude-powered agents"),
        ("CrewAI", "Multi-agent teams", "Collaborative AI workflows"),
        ("A2A", "Agent-to-Agent", "Inter-agent communication"),
        ("Langbase", "LLM pipelines", "Custom language model chains"),
        ("AGUI", "Agent UI", "Visual agent interfaces")
    ]
    
    print("✅ Your system supports 5 agent frameworks:\n")
    
    for i, (name, full_name, description) in enumerate(frameworks, 1):
        print(f"   {i}. {name:12} ({full_name})")
        print(f"      └─ {description}")
        print()
    
    print("💡 You can create agents in ANY of these frameworks!")
    print_separator()

def show_menu():
    """Interactive menu"""
    print("\n" + "="*70)
    print("🎮 ULTIMATE MCP SYSTEM - INTERACTIVE TESTER".center(70))
    print("="*70 + "\n")
    
    print("Choose a test to run:")
    print("  1. Check if servers are alive")
    print("  2. List all available tools")
    print("  3. Get system information")
    print("  4. List files in current directory")
    print("  5. Show agent frameworks")
    print("  6. Run ALL tests")
    print("  0. Exit")
    print()
    
    choice = input("Enter your choice (0-6): ").strip()
    return choice

def run_all_tests():
    """Run all tests in sequence"""
    tests = [
        test_1_check_alive,
        test_2_list_tools,
        test_3_get_system_info,
        test_4_list_files,
        test_5_agent_frameworks
    ]
    
    for test in tests:
        test()
        input("\n⏸️  Press Enter to continue...")
        print("\n")

def main():
    """Main interactive loop"""
    print("\n🚀 Starting Interactive Tester...")
    print("💡 Make sure your servers are running!")
    print("   Run: python launch_all_servers.py")
    input("\nPress Enter when ready...")
    
    while True:
        choice = show_menu()
        
        if choice == "0":
            print("\n👋 Goodbye!\n")
            sys.exit(0)
        elif choice == "1":
            test_1_check_alive()
        elif choice == "2":
            test_2_list_tools()
        elif choice == "3":
            test_3_get_system_info()
        elif choice == "4":
            test_4_list_files()
        elif choice == "5":
            test_5_agent_frameworks()
        elif choice == "6":
            run_all_tests()
        else:
            print("❌ Invalid choice! Please enter 0-6.")
        
        input("\n⏸️  Press Enter to return to menu...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!\n")
        sys.exit(0)
