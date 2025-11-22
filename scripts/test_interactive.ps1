# Interactive Testing Menu for Ultimate MCP System
# Run this to test each server interactively

function Show-Menu {
    Clear-Host
    Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host "     🧪 Ultimate MCP System - Interactive Testing      " -ForegroundColor Cyan
    Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  1. Test All Servers (Quick Health Check)" -ForegroundColor White
    Write-Host "  2. Test N8N MCP Server (Port 7862)" -ForegroundColor White
    Write-Host "  3. Test Agent Builder MCP Server (Port 7863)" -ForegroundColor White
    Write-Host "  4. Test Local Control MCP Server (Port 7864)" -ForegroundColor White
    Write-Host "  5. Test Claude Desktop Connection" -ForegroundColor White
    Write-Host "  6. Run E2E Integration Tests" -ForegroundColor White
    Write-Host "  7. Open All UIs in Browser" -ForegroundColor White
    Write-Host "  8. View Server Logs" -ForegroundColor White
    Write-Host "  9. Check Server Status" -ForegroundColor White
    Write-Host "  0. Exit" -ForegroundColor White
    Write-Host ""
    Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
}

function Test-AllServers {
    Write-Host "`n🧪 Running comprehensive server tests...`n" -ForegroundColor Cyan
    python test_all_servers.py
    Read-Host "`nPress Enter to continue"
}

function Test-N8NServer {
    Write-Host "`n🔄 Testing N8N MCP Server...`n" -ForegroundColor Cyan
    
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:7862" -TimeoutSec 5 -UseBasicParsing
        Write-Host "✅ N8N Server responding (Status: $($response.StatusCode))" -ForegroundColor Green
        Write-Host "`nOpening N8N UI in browser..." -ForegroundColor Yellow
        Start-Process "http://localhost:7862"
        Write-Host "`n📋 Test Checklist:" -ForegroundColor Yellow
        Write-Host "  □ Workflow Builder tab loads" -ForegroundColor White
        Write-Host "  □ Can generate workflow from description" -ForegroundColor White
        Write-Host "  □ Workflow Tester tab works" -ForegroundColor White
        Write-Host "  □ Deployer tab is accessible" -ForegroundColor White
    } catch {
        Write-Host "❌ N8N Server not responding" -ForegroundColor Red
        Write-Host "   Make sure the server is running: python backend/mcp_servers/n8n_automation/server.py" -ForegroundColor Yellow
    }
    
    Read-Host "`nPress Enter to continue"
}

function Test-AgentBuilderServer {
    Write-Host "`n🤖 Testing Agent Builder MCP Server...`n" -ForegroundColor Cyan
    
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:7863" -TimeoutSec 5 -UseBasicParsing
        Write-Host "✅ Agent Builder Server responding (Status: $($response.StatusCode))" -ForegroundColor Green
        Write-Host "`nOpening Agent Builder UI in browser..." -ForegroundColor Yellow
        Start-Process "http://localhost:7863"
        Write-Host "`n📋 Test Checklist:" -ForegroundColor Yellow
        Write-Host "  □ ADK tab - Create agent" -ForegroundColor White
        Write-Host "  □ A2A Protocol tab - Configure protocol" -ForegroundColor White
        Write-Host "  □ CrewAI tab - Create multi-agent team" -ForegroundColor White
        Write-Host "  □ Langbase tab - Create memory" -ForegroundColor White
        Write-Host "  □ AGUI tab - Create interface" -ForegroundColor White
    } catch {
        Write-Host "❌ Agent Builder Server not responding" -ForegroundColor Red
        Write-Host "   Make sure the server is running: python backend/mcp_servers/agent_builder/server.py" -ForegroundColor Yellow
    }
    
    Read-Host "`nPress Enter to continue"
}

function Test-LocalControlServer {
    Write-Host "`n💻 Testing Local Control MCP Server...`n" -ForegroundColor Cyan
    
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:7864" -TimeoutSec 5 -UseBasicParsing
        Write-Host "✅ Local Control Server responding (Status: $($response.StatusCode))" -ForegroundColor Green
        Write-Host "`nOpening Local Control UI in browser..." -ForegroundColor Yellow
        Start-Process "http://localhost:7864"
        Write-Host "`n📋 Test Checklist:" -ForegroundColor Yellow
        Write-Host "  □ System Commands tab - Run 'echo Hello'" -ForegroundColor White
        Write-Host "  □ Browser Automation tab - Scrape example.com" -ForegroundColor White
        Write-Host "  □ File Operations tab - Create test file" -ForegroundColor White
    } catch {
        Write-Host "❌ Local Control Server not responding" -ForegroundColor Red
        Write-Host "   Make sure the server is running: python backend/mcp_servers/local_control/server.py" -ForegroundColor Yellow
    }
    
    Read-Host "`nPress Enter to continue"
}

function Test-ClaudeDesktop {
    Write-Host "`n🔌 Testing Claude Desktop Connection...`n" -ForegroundColor Cyan
    
    # Check config exists
    $configPath = "$env:APPDATA\Claude\claude_desktop_config.json"
    if (Test-Path $configPath) {
        Write-Host "✅ MCP config found at: $configPath" -ForegroundColor Green
        
        # Check config content
        try {
            $config = Get-Content $configPath | ConvertFrom-Json
            $serverCount = ($config.mcpServers | Get-Member -MemberType NoteProperty).Count
            Write-Host "✅ $serverCount MCP servers configured" -ForegroundColor Green
        } catch {
            Write-Host "⚠️  Config file exists but couldn't parse JSON" -ForegroundColor Yellow
        }
    } else {
        Write-Host "❌ MCP config not found" -ForegroundColor Red
        Write-Host "   Run: Copy-Item 'claude_desktop_config.json' '$env:APPDATA\Claude\'" -ForegroundColor Yellow
    }
    
    Write-Host "`n📋 Manual Testing Steps:" -ForegroundColor Yellow
    Write-Host "  1. Restart Claude Desktop completely" -ForegroundColor White
    Write-Host "  2. Check for 3 MCP servers in Claude" -ForegroundColor White
    Write-Host "  3. Try command: 'What MCP servers are available?'" -ForegroundColor White
    Write-Host "  4. Try command: 'Get my system information'" -ForegroundColor White
    Write-Host "  5. Try command: 'Create a simple N8N workflow'" -ForegroundColor White
    
    Read-Host "`nPress Enter to continue"
}

function Run-E2ETests {
    Write-Host "`n🔗 Running E2E Integration Tests...`n" -ForegroundColor Cyan
    
    Write-Host "Checking if all servers are running..." -ForegroundColor Yellow
    $ports = @(7860, 7862, 7863, 7864)
    $allRunning = $true
    
    foreach ($port in $ports) {
        $test = Test-NetConnection -ComputerName localhost -Port $port -InformationLevel Quiet -WarningAction SilentlyContinue
        if ($test) {
            Write-Host "  ✅ Port $port is active" -ForegroundColor Green
        } else {
            Write-Host "  ❌ Port $port is not responding" -ForegroundColor Red
            $allRunning = $false
        }
    }
    
    if ($allRunning) {
        Write-Host "`nRunning pytest E2E tests..." -ForegroundColor Yellow
        python -m pytest tests/e2e/ -v
    } else {
        Write-Host "`n⚠️  Not all servers are running. Start them first:" -ForegroundColor Yellow
        Write-Host "   python launch_all_servers.py" -ForegroundColor White
    }
    
    Read-Host "`nPress Enter to continue"
}

function Open-AllUIs {
    Write-Host "`n🌐 Opening all server UIs in browser...`n" -ForegroundColor Cyan
    
    Start-Process "http://localhost:7860"  # Master Orchestrator
    Write-Host "  → Master Orchestrator: http://localhost:7860" -ForegroundColor Green
    Start-Sleep -Milliseconds 500
    
    Start-Process "http://localhost:7862"  # N8N
    Write-Host "  → N8N Automation: http://localhost:7862" -ForegroundColor Green
    Start-Sleep -Milliseconds 500
    
    Start-Process "http://localhost:7863"  # Agent Builder
    Write-Host "  → Agent Builder: http://localhost:7863" -ForegroundColor Green
    Start-Sleep -Milliseconds 500
    
    Start-Process "http://localhost:7864"  # Local Control
    Write-Host "  → Local Control: http://localhost:7864" -ForegroundColor Green
    
    Write-Host "`n✅ All UIs opened in browser tabs" -ForegroundColor Green
    
    Read-Host "`nPress Enter to continue"
}

function View-ServerLogs {
    Write-Host "`n📋 Server Logs (Last 20 lines)...`n" -ForegroundColor Cyan
    
    if (Test-Path "backend/logs") {
        Get-ChildItem "backend/logs" -Filter "*.log" | ForEach-Object {
            Write-Host "═══ $($_.Name) ═══" -ForegroundColor Yellow
            Get-Content $_.FullName | Select-Object -Last 20
            Write-Host ""
        }
    } else {
        Write-Host "❌ No log files found in backend/logs/" -ForegroundColor Red
    }
    
    Read-Host "`nPress Enter to continue"
}

function Check-ServerStatus {
    Write-Host "`n📊 Server Status Check...`n" -ForegroundColor Cyan
    
    $servers = @(
        @{Name="Master Orchestrator"; Port=7860},
        @{Name="N8N Automation"; Port=7862},
        @{Name="Agent Builder"; Port=7863},
        @{Name="Local Control"; Port=7864}
    )
    
    foreach ($server in $servers) {
        $test = Test-NetConnection -ComputerName localhost -Port $server.Port -InformationLevel Quiet -WarningAction SilentlyContinue
        if ($test) {
            Write-Host "  ✅ $($server.Name) (Port $($server.Port)): RUNNING" -ForegroundColor Green
        } else {
            Write-Host "  ❌ $($server.Name) (Port $($server.Port)): NOT RUNNING" -ForegroundColor Red
        }
    }
    
    Write-Host "`n💡 To start all servers:" -ForegroundColor Yellow
    Write-Host "   python launch_all_servers.py" -ForegroundColor White
    Write-Host "`n💡 Or use the start script:" -ForegroundColor Yellow
    Write-Host "   .\scripts\start_dev.ps1" -ForegroundColor White
    
    Read-Host "`nPress Enter to continue"
}

# Main loop
do {
    Show-Menu
    $choice = Read-Host "`nSelect an option (0-9)"
    
    switch ($choice) {
        "1" { Test-AllServers }
        "2" { Test-N8NServer }
        "3" { Test-AgentBuilderServer }
        "4" { Test-LocalControlServer }
        "5" { Test-ClaudeDesktop }
        "6" { Run-E2ETests }
        "7" { Open-AllUIs }
        "8" { View-ServerLogs }
        "9" { Check-ServerStatus }
        "0" { 
            Write-Host "`n👋 Exiting testing menu. Happy testing!`n" -ForegroundColor Green
            exit 
        }
        default { 
            Write-Host "`n❌ Invalid option. Please select 0-9." -ForegroundColor Red
            Start-Sleep -Seconds 2
        }
    }
} while ($true)
