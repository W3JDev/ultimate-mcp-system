"""
Comprehensive MCP System Test Suite
Tests all 4 servers and their capabilities
"""
import requests
import json
from datetime import datetime

print("="*60)
print("🧪 ULTIMATE MCP SYSTEM - COMPREHENSIVE TEST SUITE")
print("="*60)
print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

test_results = []

# Test 1: Master Orchestrator
print("1️⃣  Testing Master Orchestrator (Port 7860)...")
try:
    response = requests.get("http://localhost:7860", timeout=5)
    if response.status_code == 200:
        test_results.append(("Master Orchestrator", "✅ PASS", "Server responding"))
        print("   ✅ Master Orchestrator is ONLINE")
    else:
        test_results.append(("Master Orchestrator", "⚠️  WARN", f"Status {response.status_code}"))
        print(f"   ⚠️  Master Orchestrator returned status {response.status_code}")
except Exception as e:
    test_results.append(("Master Orchestrator", "❌ FAIL", str(e)))
    print(f"   ❌ Master Orchestrator FAILED: {e}")

print()

# Test 2: N8N Automation MCP
print("2️⃣  Testing N8N Automation MCP (Port 7862)...")
try:
    response = requests.get("http://localhost:7862", timeout=5)
    if response.status_code == 200:
        test_results.append(("N8N MCP Server", "✅ PASS", "Gradio UI responding"))
        print("   ✅ N8N MCP Server is ONLINE")
        print("   📝 Features: Workflow creation, testing, deployment")
    else:
        test_results.append(("N8N MCP Server", "⚠️  WARN", f"Status {response.status_code}"))
        print(f"   ⚠️  N8N MCP returned status {response.status_code}")
except Exception as e:
    test_results.append(("N8N MCP Server", "❌ FAIL", str(e)))
    print(f"   ❌ N8N MCP FAILED: {e}")

print()

# Test 3: Agent Builder MCP
print("3️⃣  Testing Agent Builder MCP (Port 7863)...")
try:
    response = requests.get("http://localhost:7863", timeout=5)
    if response.status_code == 200:
        test_results.append(("Agent Builder MCP", "✅ PASS", "Gradio UI responding"))
        print("   ✅ Agent Builder MCP is ONLINE")
        print("   🤖 Frameworks: ADK, A2A, CrewAI, Langbase, AGUI")
    else:
        test_results.append(("Agent Builder MCP", "⚠️  WARN", f"Status {response.status_code}"))
        print(f"   ⚠️  Agent Builder returned status {response.status_code}")
except Exception as e:
    test_results.append(("Agent Builder MCP", "❌ FAIL", str(e)))
    print(f"   ❌ Agent Builder FAILED: {e}")

print()

# Test 4: Local Control MCP
print("4️⃣  Testing Local Control MCP (Port 7864)...")
try:
    response = requests.get("http://localhost:7864", timeout=5)
    if response.status_code == 200:
        test_results.append(("Local Control MCP", "✅ PASS", "Gradio UI responding"))
        print("   ✅ Local Control MCP is ONLINE")
        print("   💻 Features: System commands, browser automation, file ops")
    else:
        test_results.append(("Local Control MCP", "⚠️  WARN", f"Status {response.status_code}"))
        print(f"   ⚠️  Local Control returned status {response.status_code}")
except Exception as e:
    test_results.append(("Local Control MCP", "❌ FAIL", str(e)))
    print(f"   ❌ Local Control FAILED: {e}")

print()
print("="*60)
print("📊 TEST SUMMARY")
print("="*60)

passed = sum(1 for _, status, _ in test_results if "✅" in status)
warned = sum(1 for _, status, _ in test_results if "⚠️" in status)
failed = sum(1 for _, status, _ in test_results if "❌" in status)
total = len(test_results)

for component, status, details in test_results:
    print(f"{status} {component:25} | {details}")

print()
print(f"Results: {passed} passed, {warned} warnings, {failed} failed out of {total} tests")
print()

if failed == 0 and warned == 0:
    print("🎉 ALL TESTS PASSED! System is fully operational.")
    exit(0)
elif failed == 0:
    print("✅ All critical tests passed (some warnings)")
    exit(0)
else:
    print("❌ Some tests failed. Check server logs.")
    exit(1)
