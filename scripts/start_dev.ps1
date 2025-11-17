# Ultimate MCP System - Local Development Startup Script
# Starts all 4 servers for local development

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🚀 STARTING ULTIMATE MCP SYSTEM - DEV MODE" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Change to project directory
Set-Location "C:\Users\W3jde\PROJECTS\MCP\ultimate-mcp-system"

# Activate virtual environment
Write-Host "📦 Activating virtual environment..." -ForegroundColor Yellow
& ".\.venv\Scripts\Activate.ps1"

# Check if servers are already running
Write-Host "🔍 Checking for existing servers..." -ForegroundColor Yellow
$ports = @(7860, 7862, 7863, 7864)
$running = @()

foreach ($port in $ports) {
    $test = Test-NetConnection -ComputerName localhost -Port $port -InformationLevel Quiet -WarningAction SilentlyContinue
    if ($test) {
        $running += $port
        Write-Host "   ⚠️  Port $port already in use" -ForegroundColor Yellow
    }
}

if ($running.Count -gt 0) {
    Write-Host ""
    Write-Host "❌ Some servers are already running on ports: $($running -join ', ')" -ForegroundColor Red
    Write-Host "Please stop them first or use launch_all_servers.py instead." -ForegroundColor Red
    Write-Host ""
    exit 1
}

Write-Host "   ✅ All ports available" -ForegroundColor Green
Write-Host ""

# Start servers in background
Write-Host "🚀 Starting servers..." -ForegroundColor Yellow
Write-Host ""

Write-Host "Starting Master Orchestrator (Port 7860)..." -ForegroundColor Cyan
Start-Process -FilePath ".\.venv\Scripts\python.exe" -ArgumentList "backend\main.py" -WindowStyle Hidden
Start-Sleep -Seconds 2

Write-Host "Starting N8N Automation MCP (Port 7862)..." -ForegroundColor Cyan
Start-Process -FilePath ".\.venv\Scripts\python.exe" -ArgumentList "backend\mcp_servers\n8n_automation\server.py" -WindowStyle Hidden
Start-Sleep -Seconds 2

Write-Host "Starting Agent Builder MCP (Port 7863)..." -ForegroundColor Cyan
Start-Process -FilePath ".\.venv\Scripts\python.exe" -ArgumentList "backend\mcp_servers\agent_builder\server.py" -WindowStyle Hidden
Start-Sleep -Seconds 2

Write-Host "Starting Local Control MCP (Port 7864)..." -ForegroundColor Cyan
Start-Process -FilePath ".\.venv\Scripts\python.exe" -ArgumentList "backend\mcp_servers\local_control\server.py" -WindowStyle Hidden
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "⏳ Waiting for servers to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Verify all servers are up
Write-Host ""
Write-Host "🔍 Verifying server status..." -ForegroundColor Yellow

$allUp = $true
foreach ($port in $ports) {
    $test = Test-NetConnection -ComputerName localhost -Port $port -InformationLevel Quiet -WarningAction SilentlyContinue
    if ($test) {
        Write-Host "   ✅ Port $port is ACTIVE" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Port $port is DOWN" -ForegroundColor Red
        $allUp = $false
    }
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan

if ($allUp) {
    Write-Host "✅ ALL SERVERS LAUNCHED SUCCESSFULLY!" -ForegroundColor Green
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Access the servers:" -ForegroundColor Yellow
    Write-Host "  Master Orchestrator       → http://localhost:7860" -ForegroundColor White
    Write-Host "  N8N Automation            → http://localhost:7862" -ForegroundColor White
    Write-Host "  Agent Builder             → http://localhost:7863" -ForegroundColor White
    Write-Host "  Local Control             → http://localhost:7864" -ForegroundColor White
    Write-Host ""
    Write-Host "To stop servers: .\scripts\stop_dev.ps1" -ForegroundColor Yellow
    Write-Host "To test system:  python test_all_servers.py" -ForegroundColor Yellow
    Write-Host ""
} else {
    Write-Host "❌ SOME SERVERS FAILED TO START" -ForegroundColor Red
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Check logs in backend/logs/ for details" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}
