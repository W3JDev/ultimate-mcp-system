#!/bin/bash
# Stop all running MCP servers

set -e

echo "🛑 Ultimate MCP System - Stop Demo Script"
echo "========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"
PIDS_DIR="$PROJECT_ROOT/backend/pids"

echo "📂 Project root: $PROJECT_ROOT"
echo ""

# Function to stop server by PID file
stop_server() {
    local name=$1
    local pid_file=$2
    
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if kill -0 "$pid" 2>/dev/null; then
            echo -n "Stopping $name (PID: $pid)... "
            kill "$pid" 2>/dev/null || kill -9 "$pid" 2>/dev/null
            rm "$pid_file"
            echo -e "${GREEN}✅ Stopped${NC}"
        else
            echo -e "${YELLOW}⚠️ $name (PID: $pid) not running${NC}"
            rm "$pid_file"
        fi
    else
        echo -e "${YELLOW}⚠️ $name PID file not found${NC}"
    fi
}

# Stop all servers
echo "🛑 Stopping servers..."
echo ""

stop_server "Master Orchestrator" "$PIDS_DIR/master.pid"
stop_server "N8N Automation MCP" "$PIDS_DIR/n8n.pid"
stop_server "Agent Builder MCP" "$PIDS_DIR/agent_builder.pid"
stop_server "Local Control MCP" "$PIDS_DIR/local_control.pid"

# Also try to kill by port (fallback)
echo ""
echo "🔍 Checking for any remaining processes..."

PORTS=(7860 7862 7863 7864)
FOUND_ANY=false

for port in "${PORTS[@]}"; do
    pid=$(lsof -ti:$port 2>/dev/null || true)
    if [ ! -z "$pid" ]; then
        FOUND_ANY=true
        echo -n "Killing process on port $port (PID: $pid)... "
        kill -9 "$pid" 2>/dev/null || true
        echo -e "${GREEN}✅ Killed${NC}"
    fi
done

if [ "$FOUND_ANY" = false ]; then
    echo -e "${GREEN}✅ No remaining processes found${NC}"
fi

echo ""
echo "============================================"
echo -e "${GREEN}✅ All servers stopped${NC}"
echo "============================================"
echo ""
