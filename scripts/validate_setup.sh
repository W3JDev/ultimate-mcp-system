#!/bin/bash
# Validate that the Ultimate MCP System is properly set up for demo/submission
# This script checks all prerequisites without starting servers

set -e

echo "🔍 Ultimate MCP System - Setup Validation"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

CHECKS_PASSED=0
CHECKS_FAILED=0
WARNINGS=0

# Function to check and report
check_requirement() {
    local name=$1
    local check_command=$2
    local install_hint=$3
    
    echo -n "Checking $name... "
    
    if eval "$check_command" &>/dev/null; then
        echo -e "${GREEN}✅ OK${NC}"
        CHECKS_PASSED=$((CHECKS_PASSED + 1))
        return 0
    else
        echo -e "${RED}❌ MISSING${NC}"
        if [ ! -z "$install_hint" ]; then
            echo "   Install with: $install_hint"
        fi
        CHECKS_FAILED=$((CHECKS_FAILED + 1))
        return 1
    fi
}

# Function to check optional requirement
check_optional() {
    local name=$1
    local check_command=$2
    local install_hint=$3
    
    echo -n "Checking $name (optional)... "
    
    if eval "$check_command" &>/dev/null; then
        echo -e "${GREEN}✅ OK${NC}"
        CHECKS_PASSED=$((CHECKS_PASSED + 1))
        return 0
    else
        echo -e "${YELLOW}⚠️ Not installed${NC}"
        if [ ! -z "$install_hint" ]; then
            echo "   Install with: $install_hint"
        fi
        WARNINGS=$((WARNINGS + 1))
        return 1
    fi
}

echo "📦 Phase 1: System Requirements"
echo "-------------------------------"

# Check Python
check_requirement "Python 3" "command -v python3" "apt-get install python3 or brew install python3"

if command -v python3 &>/dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo "   Version: $PYTHON_VERSION"
    
    MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
    
    if [ "$MAJOR" -ge 3 ] && [ "$MINOR" -ge 11 ]; then
        echo -e "   ${GREEN}✅ Version is compatible (3.11+)${NC}"
    else
        echo -e "   ${RED}❌ Version too old (need 3.11+)${NC}"
        CHECKS_FAILED=$((CHECKS_FAILED + 1))
    fi
fi

# Check pip
check_requirement "pip" "command -v pip" "python3 -m ensurepip"

# Check curl (for tests)
check_requirement "curl" "command -v curl" "apt-get install curl or brew install curl"

# Check netcat (for port tests)
check_optional "netcat" "command -v nc" "apt-get install netcat or brew install netcat"

# Check git
check_requirement "git" "command -v git" "apt-get install git or brew install git"

echo ""
echo "📁 Phase 2: Project Structure"
echo "-----------------------------"

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

cd "$PROJECT_ROOT"

# Check project files
check_requirement "backend directory" "test -d backend" "Something is wrong with project structure"
check_requirement "main.py" "test -f backend/main.py" "Missing main entry point"
check_requirement "requirements.txt" "test -f backend/requirements.txt" "Missing dependencies file"

# Check MCP servers
check_requirement "N8N MCP server" "test -f backend/mcp_servers/n8n_automation/server.py" "Missing N8N server"
check_requirement "Agent Builder MCP" "test -f backend/mcp_servers/agent_builder/server.py" "Missing Agent Builder"
check_requirement "Local Control MCP" "test -f backend/mcp_servers/local_control/server.py" "Missing Local Control"

# Check documentation
check_requirement "README.md" "test -f README.md" "Missing project README"
check_requirement "SUBMISSION_CHECKLIST.md" "test -f SUBMISSION_CHECKLIST.md" "Missing submission checklist"
check_requirement "DEMO_SCENARIOS.md" "test -f DEMO_SCENARIOS.md" "Missing demo scenarios"

echo ""
echo "🐍 Phase 3: Python Environment"
echo "------------------------------"

# Check for virtual environment
if [ -d "venv" ]; then
    echo -e "Virtual environment... ${GREEN}✅ Found${NC}"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
else
    echo -e "Virtual environment... ${YELLOW}⚠️ Not found${NC}"
    echo "   Create with: python3 -m venv venv"
    WARNINGS=$((WARNINGS + 1))
fi

# Try to activate and check packages
if [ -d "venv" ]; then
    # Activate venv
    source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null || true
    
    # Check key dependencies
    check_requirement "gradio package" "python3 -c 'import gradio'" "pip install gradio"
    check_requirement "fastapi package" "python3 -c 'import fastapi'" "pip install fastapi"
    check_requirement "anthropic package" "python3 -c 'import anthropic'" "pip install anthropic"
    check_optional "playwright package" "python3 -c 'import playwright'" "pip install playwright"
    
    # Check for Python 3.13 compatibility
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1-2)
    if [ "$PYTHON_VERSION" = "3.13" ]; then
        echo -n "Checking audioop-lts (Python 3.13 fix)... "
        if python3 -c "import audioop_lts" 2>/dev/null; then
            echo -e "${GREEN}✅ Installed${NC}"
            CHECKS_PASSED=$((CHECKS_PASSED + 1))
        else
            echo -e "${YELLOW}⚠️ Missing${NC}"
            echo "   Install with: pip install audioop-lts"
            WARNINGS=$((WARNINGS + 1))
        fi
    fi
fi

echo ""
echo "🔐 Phase 4: Configuration"
echo "------------------------"

# Check for .env file
if [ -f "backend/.env" ] || [ -f ".env" ]; then
    echo -e ".env file... ${GREEN}✅ Found${NC}"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
    
    # Check for API keys (optional)
    if [ -f "backend/.env" ]; then
        ENV_FILE="backend/.env"
    else
        ENV_FILE=".env"
    fi
    
    if grep -q "ANTHROPIC_API_KEY=sk-" "$ENV_FILE" 2>/dev/null; then
        echo -e "Anthropic API key... ${GREEN}✅ Configured${NC}"
    else
        echo -e "Anthropic API key... ${YELLOW}⚠️ Not configured (optional)${NC}"
        echo "   System will work in fallback mode"
    fi
    
    if grep -q "OPENAI_API_KEY=sk-" "$ENV_FILE" 2>/dev/null; then
        echo -e "OpenAI API key... ${GREEN}✅ Configured${NC}"
    else
        echo -e "OpenAI API key... ${YELLOW}⚠️ Not configured (optional)${NC}"
    fi
else
    echo -e ".env file... ${YELLOW}⚠️ Not found${NC}"
    echo "   Copy from: cp .env.example backend/.env"
    echo "   System will work in fallback mode"
    WARNINGS=$((WARNINGS + 1))
fi

# Check .env.example exists
check_requirement ".env.example" "test -f .env.example" "Missing environment template"

echo ""
echo "📝 Phase 5: Required Directories"
echo "--------------------------------"

# Check/create logs directory
if [ -d "backend/logs" ]; then
    echo -e "logs directory... ${GREEN}✅ Exists${NC}"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
else
    echo -e "logs directory... ${YELLOW}⚠️ Creating${NC}"
    mkdir -p backend/logs
    echo -e "   ${GREEN}✅ Created${NC}"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
fi

# Check/create pids directory
if [ -d "backend/pids" ]; then
    echo -e "pids directory... ${GREEN}✅ Exists${NC}"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
else
    echo -e "pids directory... ${YELLOW}⚠️ Creating${NC}"
    mkdir -p backend/pids
    echo -e "   ${GREEN}✅ Created${NC}"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
fi

echo ""
echo "🛠️ Phase 6: Scripts"
echo "------------------"

# Check scripts are executable
for script in start_demo.sh stop_demo.sh test_servers.sh; do
    if [ -f "scripts/$script" ]; then
        if [ -x "scripts/$script" ]; then
            echo -e "$script... ${GREEN}✅ Executable${NC}"
            CHECKS_PASSED=$((CHECKS_PASSED + 1))
        else
            echo -e "$script... ${YELLOW}⚠️ Not executable, fixing${NC}"
            chmod +x "scripts/$script"
            echo -e "   ${GREEN}✅ Fixed${NC}"
            CHECKS_PASSED=$((CHECKS_PASSED + 1))
        fi
    else
        echo -e "$script... ${RED}❌ Missing${NC}"
        CHECKS_FAILED=$((CHECKS_FAILED + 1))
    fi
done

echo ""
echo "=========================================="
echo "📊 Validation Summary"
echo "=========================================="
echo ""
echo "Checks Passed: ${GREEN}$CHECKS_PASSED${NC}"
echo "Checks Failed: ${RED}$CHECKS_FAILED${NC}"
echo "Warnings:      ${YELLOW}$WARNINGS${NC}"
echo ""

# Calculate readiness
TOTAL_CHECKS=$((CHECKS_PASSED + CHECKS_FAILED))
if [ $TOTAL_CHECKS -gt 0 ]; then
    SUCCESS_RATE=$((CHECKS_PASSED * 100 / TOTAL_CHECKS))
    echo "Success Rate: $SUCCESS_RATE%"
    echo ""
    
    if [ $CHECKS_FAILED -eq 0 ]; then
        echo -e "${GREEN}✅ READY FOR DEMO!${NC}"
        echo ""
        echo "Next steps:"
        echo "  1. Start servers: ./scripts/start_demo.sh"
        echo "  2. Test servers: ./scripts/test_servers.sh"
        echo "  3. Open UIs in browser"
        echo "  4. Follow DEMO_SCENARIOS.md"
        exit 0
    elif [ $SUCCESS_RATE -ge 80 ]; then
        echo -e "${YELLOW}⚠️ MOSTLY READY${NC}"
        echo ""
        echo "Fix critical issues before demo:"
        echo "  • Review failed checks above"
        echo "  • Install missing requirements"
        echo "  • Warnings are optional but recommended"
        exit 0
    else
        echo -e "${RED}❌ NOT READY${NC}"
        echo ""
        echo "Critical issues must be fixed:"
        echo "  • Review all failed checks above"
        echo "  • Install missing requirements"
        echo "  • Run this script again after fixes"
        exit 1
    fi
fi
