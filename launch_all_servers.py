#!/usr/bin/env python3
'''
Launch all MCP servers simultaneously
'''
import subprocess
import time
import os
import sys

# Change to project root
os.chdir(r'C:\Users\W3jde\PROJECTS\MCP\ultimate-mcp-system')

print("="*60)
print("🚀 LAUNCHING ALL MCP SERVERS")
print("="*60)

servers = [
    {
        'name': 'Master Orchestrator',
        'port': 7860,
        'path': 'backend/main.py',
        'desc': 'Main orchestration server (FastAPI)'
    },
    {
        'name': 'N8N Automation',
        'port': 7862,
        'path': 'backend/mcp_servers/n8n_automation/server.py',
        'desc': 'Workflow automation'
    },
    {
        'name': 'Agent Builder',
        'port': 7863,
        'path': 'backend/mcp_servers/agent_builder/server.py',
        'desc': 'Multi-framework agent creation'
    },
    {
        'name': 'Local Control',
        'port': 7864,
        'path': 'backend/mcp_servers/local_control/server.py',
        'desc': 'System automation & control'
    }
]

processes = []

for server in servers:
    print(f"\n[STARTING] {server['name']} on port {server['port']}...")
    print(f"[PATH] {server['path']}")
    
    try:
        # Use activated venv python
        proc = subprocess.Popen(
            [r'venv\Scripts\python.exe', server['path']],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        processes.append({
            'proc': proc,
            'server': server
        })
        print(f"[OK] {server['name']} starting (PID: {proc.pid})")
        time.sleep(2)  # Give it time to start
    except Exception as e:
        print(f"[ERROR] Failed to start {server['name']}: {e}")

print("\n" + "="*60)
print("✅ ALL SERVERS LAUNCHED!")
print("="*60)
print("\nAccess the servers:")
for server in servers:
    print(f"  {server['name']:25} → http://localhost:{server['port']}")
    print(f"  {' '*25}   {server['desc']}")

print("\n" + "="*60)
print("Press Ctrl+C to stop all servers")
print("="*60)

try:
    # Monitor all processes
    while True:
        time.sleep(1)
        for p in processes:
            if p['proc'].poll() is not None:
                print(f"\n[WARN] {p['server']['name']} stopped!")
                # Read any error output
                output = p['proc'].stdout.read()
                if output:
                    print(f"[OUTPUT] {output}")
except KeyboardInterrupt:
    print("\n\n[SHUTDOWN] Stopping all servers...")
    for p in processes:
        p['proc'].terminate()
        print(f"[OK] Stopped {p['server']['name']}")
    print("[DONE] All servers stopped")
