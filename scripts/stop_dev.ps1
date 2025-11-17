# Ultimate MCP System - Stop Development Servers
# Stops all running MCP servers

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🛑 STOPPING ULTIMATE MCP SYSTEM SERVERS" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Find Python processes running our servers
Write-Host "🔍 Finding server processes..." -ForegroundColor Yellow

$serverPorts = @{
    7860 = "Master Orchestrator"
    7862 = "N8N Automation"
    7863 = "Agent Builder"
    7864 = "Local Control"
}

$stoppedCount = 0

foreach ($port in $serverPorts.Keys) {
    $connections = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
    
    if ($connections) {
        foreach ($conn in $connections) {
            $process = Get-Process -Id $conn.OwningProcess -ErrorAction SilentlyContinue
            
            if ($process -and $process.ProcessName -eq "python") {
                Write-Host "   Stopping $($serverPorts[$port]) (Port $port, PID $($process.Id))..." -ForegroundColor Yellow
                Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue
                $stoppedCount++
                Write-Host "   ✅ Stopped" -ForegroundColor Green
            }
        }
    } else {
        Write-Host "   ℹ️  No server running on port $port" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan

if ($stoppedCount -gt 0) {
    Write-Host "✅ STOPPED $stoppedCount SERVER(S)" -ForegroundColor Green
} else {
    Write-Host "ℹ️  NO SERVERS WERE RUNNING" -ForegroundColor Yellow
}

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Clean up PID files
Write-Host "🧹 Cleaning up PID files..." -ForegroundColor Yellow
if (Test-Path "backend\pids") {
    Remove-Item "backend\pids\*.pid" -Force -ErrorAction SilentlyContinue
    Write-Host "   ✅ PID files cleaned" -ForegroundColor Green
}

Write-Host ""
Write-Host "To restart servers: .\scripts\start_dev.ps1" -ForegroundColor Cyan
Write-Host ""
