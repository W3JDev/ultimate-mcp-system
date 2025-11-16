#!/usr/bin/env python3
'''
Start individual MCP server for testing
Usage: python start_server.py [master|n8n|agent|local]
'''
import sys
import subprocess

if len(sys.argv) < 2:
    print("Usage: python start_server.py [master|n8n|agent|local]")
    sys.exit(1)

server = sys.argv[1].lower()

servers = {
    'master': {
        'path': 'backend/main.py',
        'port': 7860,
        'name': 'Master Orchestrator'
    },
    'n8n': {
        'path': 'backend/mcp_servers/n8n_automation/server.py',
        'port': 7862,
        'name': 'N8N Automation'
    },
    'agent': {
        'path': 'backend/mcp_servers/agent_builder/server.py',
        'port': 7863,
        'name': 'Agent Builder'
    },
    'local': {
        'path': 'backend/mcp_servers/local_control/server.py',
        'port': 7864,
        'name': 'Local Control'
    }
}

if server not in servers:
    print(f"Unknown server: {server}")
    print(f"Available: {', '.join(servers.keys())}")
    sys.exit(1)

s = servers[server]
print(f"\n[STARTING] {s['name']} on port {s['port']}")
print(f"[PATH] {s['path']}\n")

subprocess.run([sys.executable, s['path']])
