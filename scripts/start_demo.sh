#!/bin/bash
# Start all MCP servers for demo purposes
# This script starts all 4 servers in the background

set -e

echo "🚀 Ultimate MCP System - Demo Startup Script"
echo "============================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

echo "📂 Project root: $PROJECT_ROOT"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found${NC}"
    echo "Please install Python 3.11 or later"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1-2)
echo "🐍 Python version: $PYTHON_VERSION"

if [[ "$PYTHON_VERSION" == "3.13" ]]; then
    echo -e "${YELLOW}⚠️ Python 3.13 detected${NC}"
    echo "   Note: Requires audioop-lts package for Gradio"
    echo "   Install with: pip install audioop-lts"
fi

# Check if virtual environment exists
if [ ! -d "$PROJECT_ROOT/venv" ]; then
    echo -e "${YELLOW}⚠️ Virtual environment not found${NC}"
    echo "   Creating virtual environment..."
    python3 -m venv "$PROJECT_ROOT/venv"
    echo -e "${GREEN}✅ Virtual environment created${NC}"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source "$PROJECT_ROOT/venv/bin/activate" 2>/dev/null || source "$PROJECT_ROOT/venv/Scripts/activate" 2>/dev/null || {
    echo -e "${RED}❌ Failed to activate virtual environment${NC}"
    exit 1
}

# Check if dependencies are installed
if ! python -c "import gradio" 2>/dev/null; then
    echo -e "${YELLOW}⚠️ Dependencies not installed${NC}"
    echo "   Installing from requirements.txt..."
    pip install -r "$PROJECT_ROOT/backend/requirements.txt"
    echo -e "${GREEN}✅ Dependencies installed${NC}"
fi

# Create logs directory if it doesn't exist
mkdir -p "$PROJECT_ROOT/backend/logs"

# Create PIDs directory if it doesn't exist
mkdir -p "$PROJECT_ROOT/backend/pids"

# Function to check if port is in use
check_port() {
    local port=$1
    if nc -z localhost "$port" 2>/dev/null; then
        return 0  # Port is in use
    else
        return 1  # Port is free
    fi
}

# Function to kill process on port
kill_port() {
    local port=$1
    local pid=$(lsof -ti:$port 2>/dev/null)
    if [ ! -z "$pid" ]; then
        echo "   Killing process $pid on port $port"
        kill -9 $pid 2>/dev/null || true
        sleep 1
    fi
}

echo ""
echo "🔍 Checking for existing servers..."

# Check and clean up ports
PORTS=(7860 7862 7863 7864)
for port in "${PORTS[@]}"; do
    if check_port $port; then
        echo -e "${YELLOW}⚠️ Port $port is already in use${NC}"
        read -p "   Kill existing process? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            kill_port $port
        else
            echo "   Skipping port $port"
        fi
    fi
done

echo ""
echo "🚀 Starting servers..."
echo ""

cd "$PROJECT_ROOT/backend"

# Start Master Orchestrator
echo -n "Starting Master Orchestrator (port 7860)... "
python main.py > logs/master.log 2>&1 &
MASTER_PID=$!
echo $MASTER_PID > pids/master.pid
sleep 2
if kill -0 $MASTER_PID 2>/dev/null; then
    echo -e "${GREEN}✅ Started (PID: $MASTER_PID)${NC}"
else
    echo -e "${RED}❌ Failed to start${NC}"
    echo "Check logs/master.log for details"
fi

# Start N8N Automation MCP
echo -n "Starting N8N Automation MCP (port 7862)... "
python mcp_servers/n8n_automation/server.py > logs/n8n.log 2>&1 &
N8N_PID=$!
echo $N8N_PID > pids/n8n.pid
sleep 2
if kill -0 $N8N_PID 2>/dev/null; then
    echo -e "${GREEN}✅ Started (PID: $N8N_PID)${NC}"
else
    echo -e "${RED}❌ Failed to start${NC}"
    echo "Check logs/n8n.log for details"
fi

# Start Agent Builder MCP
echo -n "Starting Agent Builder MCP (port 7863)... "
python mcp_servers/agent_builder/server.py > logs/agent_builder.log 2>&1 &
AGENT_PID=$!
echo $AGENT_PID > pids/agent_builder.pid
sleep 2
if kill -0 $AGENT_PID 2>/dev/null; then
    echo -e "${GREEN}✅ Started (PID: $AGENT_PID)${NC}"
else
    echo -e "${RED}❌ Failed to start${NC}"
    echo "Check logs/agent_builder.log for details"
fi

# Start Local Control MCP
echo -n "Starting Local Control MCP (port 7864)... "
python mcp_servers/local_control/server.py > logs/local_control.log 2>&1 &
LOCAL_PID=$!
echo $LOCAL_PID > pids/local_control.pid
sleep 2
if kill -0 $LOCAL_PID 2>/dev/null; then
    echo -e "${GREEN}✅ Started (PID: $LOCAL_PID)${NC}"
else
    echo -e "${RED}❌ Failed to start${NC}"
    echo "Check logs/local_control.log for details"
fi

echo ""
echo "⏳ Waiting for servers to fully initialize (10 seconds)..."
sleep 8

echo ""
echo "============================================"
echo "✅ All servers started!"
echo "============================================"
echo ""
echo "📡 Access the UIs at:"
echo "  • Master Orchestrator:  http://localhost:7860"
echo "  • N8N Automation MCP:   http://localhost:7862"
echo "  • Agent Builder MCP:    http://localhost:7863"
echo "  • Local Control MCP:    http://localhost:7864"
echo ""
echo "📋 Process IDs saved in backend/pids/"
echo "📝 Logs available in backend/logs/"
echo ""
echo "🛑 To stop all servers, run:"
echo "   ./scripts/stop_demo.sh"
echo ""
echo "🧪 To test servers, run:"
echo "   ./scripts/test_servers.sh"
echo ""

# Optional: Run tests
read -p "Run server tests now? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    "$SCRIPT_DIR/test_servers.sh"
fi

echo ""
echo -e "${GREEN}🎉 Demo environment ready!${NC}"
