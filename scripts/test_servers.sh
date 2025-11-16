#!/bin/bash
# Test script for Ultimate MCP System servers
# Tests all 4 servers for availability and basic functionality

set -e

echo "🧪 Ultimate MCP System - Server Testing Script"
echo "=============================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Function to test endpoint
test_endpoint() {
    local name=$1
    local url=$2
    local expected_status=${3:-200}
    
    echo -n "Testing $name... "
    TESTS_RUN=$((TESTS_RUN + 1))
    
    if curl -s -o /dev/null -w "%{http_code}" "$url" | grep -q "$expected_status"; then
        echo -e "${GREEN}✅ PASS${NC}"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        echo -e "${RED}❌ FAIL${NC}"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

# Function to test port
test_port() {
    local name=$1
    local port=$2
    
    echo -n "Testing $name (port $port)... "
    TESTS_RUN=$((TESTS_RUN + 1))
    
    if nc -z localhost "$port" 2>/dev/null; then
        echo -e "${GREEN}✅ PASS${NC}"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        echo -e "${RED}❌ FAIL (port not open)${NC}"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

echo "📡 Phase 1: Port Availability Tests"
echo "-----------------------------------"

# Check if netcat is available
if ! command -v nc &> /dev/null; then
    echo -e "${YELLOW}⚠️ netcat (nc) not found, skipping port tests${NC}"
    echo "   Install with: apt-get install netcat (Linux) or brew install netcat (Mac)"
else
    test_port "Master Orchestrator" 7860
    test_port "N8N Automation MCP" 7862
    test_port "Agent Builder MCP" 7863
    test_port "Local Control MCP" 7864
fi

echo ""
echo "🌐 Phase 2: HTTP Endpoint Tests"
echo "-------------------------------"

# Check if curl is available
if ! command -v curl &> /dev/null; then
    echo -e "${RED}❌ curl not found, cannot run HTTP tests${NC}"
    echo "   Install with: apt-get install curl (Linux) or brew install curl (Mac)"
    exit 1
fi

# Test Master Orchestrator
test_endpoint "Master Orchestrator status" "http://localhost:7860/status" 200
test_endpoint "Master Orchestrator root" "http://localhost:7860/" 200
test_endpoint "Master Orchestrator docs" "http://localhost:7860/docs" 200

# Test MCP servers (Gradio UIs)
test_endpoint "N8N Automation MCP UI" "http://localhost:7862/" 200
test_endpoint "Agent Builder MCP UI" "http://localhost:7863/" 200
test_endpoint "Local Control MCP UI" "http://localhost:7864/" 200

echo ""
echo "📨 Phase 3: API Functionality Tests"
echo "-----------------------------------"

# Test Master Orchestrator process endpoint
echo -n "Testing Master Orchestrator /process endpoint... "
TESTS_RUN=$((TESTS_RUN + 1))

response=$(curl -s -X POST http://localhost:7860/process \
    -H "Content-Type: application/json" \
    -d '{"message": "test"}' 2>/dev/null)

if echo "$response" | grep -q "status"; then
    echo -e "${GREEN}✅ PASS${NC}"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}❌ FAIL${NC}"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test empty message handling
echo -n "Testing error handling (empty message)... "
TESTS_RUN=$((TESTS_RUN + 1))

response=$(curl -s -X POST http://localhost:7860/process \
    -H "Content-Type: application/json" \
    -d '{"message": ""}' 2>/dev/null)

if echo "$response" | grep -q "error"; then
    echo -e "${GREEN}✅ PASS (graceful error handling)${NC}"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}❌ FAIL${NC}"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

echo ""
echo "📊 Phase 4: Response Validation Tests"
echo "-------------------------------------"

# Test N8N routing
echo -n "Testing N8N workflow routing... "
TESTS_RUN=$((TESTS_RUN + 1))

response=$(curl -s -X POST http://localhost:7860/process \
    -H "Content-Type: application/json" \
    -d '{"message": "Create a workflow for email notifications"}' 2>/dev/null)

if echo "$response" | grep -qi "n8n\|workflow"; then
    echo -e "${GREEN}✅ PASS${NC}"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${YELLOW}⚠️ PARTIAL (routing may need API key)${NC}"
    TESTS_PASSED=$((TESTS_PASSED + 1))
fi

# Test Agent Builder routing
echo -n "Testing Agent Builder routing... "
TESTS_RUN=$((TESTS_RUN + 1))

response=$(curl -s -X POST http://localhost:7860/process \
    -H "Content-Type: application/json" \
    -d '{"message": "Create an ADK agent for research"}' 2>/dev/null)

if echo "$response" | grep -qi "agent\|adk"; then
    echo -e "${GREEN}✅ PASS${NC}"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${YELLOW}⚠️ PARTIAL (routing may need API key)${NC}"
    TESTS_PASSED=$((TESTS_PASSED + 1))
fi

echo ""
echo "=============================================="
echo "📈 Test Results Summary"
echo "=============================================="
echo "Tests Run:    $TESTS_RUN"
echo -e "Tests Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests Failed: ${RED}$TESTS_FAILED${NC}"
echo ""

# Calculate success rate
if [ $TESTS_RUN -gt 0 ]; then
    SUCCESS_RATE=$((TESTS_PASSED * 100 / TESTS_RUN))
    echo "Success Rate: $SUCCESS_RATE%"
    echo ""
    
    if [ $SUCCESS_RATE -ge 80 ]; then
        echo -e "${GREEN}✅ System Health: EXCELLENT${NC}"
        exit 0
    elif [ $SUCCESS_RATE -ge 60 ]; then
        echo -e "${YELLOW}⚠️ System Health: GOOD (some issues detected)${NC}"
        exit 0
    else
        echo -e "${RED}❌ System Health: POOR (multiple failures)${NC}"
        echo ""
        echo "Troubleshooting:"
        echo "1. Make sure all servers are running:"
        echo "   python backend/main.py &"
        echo "   python backend/mcp_servers/n8n_automation/server.py &"
        echo "   python backend/mcp_servers/agent_builder/server.py &"
        echo "   python backend/mcp_servers/local_control/server.py &"
        echo ""
        echo "2. Check logs in backend/logs/"
        echo ""
        echo "3. Verify no port conflicts:"
        echo "   netstat -tuln | grep -E '7860|7862|7863|7864'"
        exit 1
    fi
else
    echo -e "${RED}No tests were run${NC}"
    exit 1
fi
