import subprocess
import sys
import importlib.util
import os
from pathlib import Path

print("🔍 CORE ISSUE DIAGNOSIS - ULTIMATE MCP SYSTEM")
print("=" * 60)

# 1. Check Python Environment
print("\n1️⃣ PYTHON ENVIRONMENT:")
print(f"   Python Version: {sys.version}")
print(f"   Working Directory: {os.getcwd()}")

# 2. Check Critical Dependencies
print("\n2️⃣ CRITICAL DEPENDENCIES:")
critical_deps = ['gradio', 'anthropic', 'fastapi', 'uvicorn', 'loguru', 'audioop']
for dep in critical_deps:
    try:
        if dep == 'audioop':
            import audioop
            print(f"   ✅ {dep}: Available")
        else:
            spec = importlib.util.find_spec(dep)
            if spec:
                module = importlib.import_module(dep)
                version = getattr(module, '__version__', 'unknown')
                print(f"   ✅ {dep}: {version}")
            else:
                print(f"   ❌ {dep}: Not found")
    except Exception as e:
        print(f"   ❌ {dep}: {str(e)}")

# 3. Test MCP Component Imports
print("\n3️⃣ MCP COMPONENT IMPORTS:")
components = [
    'backend.orchestrator',
    'backend.mcp_servers.n8n_automation.server',
    'backend.mcp_servers.agent_builder.server', 
    'backend.mcp_servers.local_control.server'
]

for comp in components:
    try:
        importlib.import_module(comp)
        print(f"   ✅ {comp}")
    except Exception as e:
        print(f"   ❌ {comp}: {str(e)}")

# 4. Check Environment Variables
print("\n4️⃣ ENVIRONMENT VARIABLES:")
critical_env = ['ANTHROPIC_API_KEY', 'OPENAI_API_KEY', 'N8N_API_KEY']
for env in critical_env:
    value = os.getenv(env)
    if value:
        print(f"   ✅ {env}: Set (length: {len(value)})")
    else:
        print(f"   ❌ {env}: Missing")

# 5. Test Port Availability
print("\n5️⃣ PORT AVAILABILITY:")
import socket
ports = [7860, 7862, 7863, 7864]
for port in ports:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex(('localhost', port))
    if result == 0:
        print(f"   ⚠️  Port {port}: In use")
    else:
        print(f"   ✅ Port {port}: Available")
    sock.close()

# 6. Test Basic Orchestrator Functionality
print("\n6️⃣ ORCHESTRATOR TEST:")
try:
    sys.path.append('backend')
    from orchestrator import Orchestrator
    
    # Initialize orchestrator without starting servers
    orchestrator = Orchestrator()
    print("   ✅ Orchestrator class imports")
    
    # Test tool registry
    if hasattr(orchestrator, 'tool_registry'):
        print(f"   ✅ Tool registry available")
    else:
        print("   ❌ Tool registry missing")
        
except Exception as e:
    print(f"   ❌ Orchestrator error: {str(e)}")

# 7. Check Log Directory
print("\n7️⃣ LOG SYSTEM:")
log_dir = Path("backend/logs")
if log_dir.exists():
    log_files = list(log_dir.glob("*.log"))
    print(f"   ✅ Log directory exists with {len(log_files)} files")
    for log_file in log_files[:3]:  # Show first 3
        size = log_file.stat().st_size
        print(f"   📄 {log_file.name}: {size} bytes")
else:
    print("   ❌ Log directory missing")

print("\n" + "=" * 60)
print("📊 DIAGNOSIS COMPLETE")