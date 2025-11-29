# 🧪 MCP Client Test Commands
# Quick commands to test your MCP setup

Write-Host "🧪 MCP Client Test Suite" -ForegroundColor Cyan
Write-Host "=========================" -ForegroundColor Cyan
Write-Host ""

# Test 1: Check MCP Server is Running
Write-Host "Test 1: Check MCP Server Connection" -ForegroundColor Yellow
Test-NetConnection -ComputerName localhost -Port 3001 -InformationLevel Quiet
if ($?) {
    Write-Host "✅ MCP Server is running on port 3001" -ForegroundColor Green
} else {
    Write-Host "❌ MCP Server is not running" -ForegroundColor Red
    Write-Host "Start with: npx @modelcontextprotocol/server-example-streamable" -ForegroundColor Gray
}
Write-Host ""

# Test 2: Check N8N Connection
Write-Host "Test 2: Check N8N API Connection" -ForegroundColor Yellow
try {
    # Load .env
    Get-Content ".env" | ForEach-Object {
        if ($_ -match '^\s*([^#][^=]+?)\s*=\s*(.+?)\s*$') {
            $key = $matches[1]
            $value = $matches[2]
            [Environment]::SetEnvironmentVariable($key, $value, "Process")
        }
    }

    $n8nUrl = [Environment]::GetEnvironmentVariable("N8N_API_URL")
    $n8nApiKey = [Environment]::GetEnvironmentVariable("N8N_API_KEY")
    
    $headers = @{
        "X-N8N-API-KEY" = $n8nApiKey
    }
    
    $response = Invoke-RestMethod -Uri "$n8nUrl/workflows" -Headers $headers -Method GET
    Write-Host "✅ N8N API is accessible" -ForegroundColor Green
    Write-Host "Found $($response.data.Count) workflows" -ForegroundColor Gray
} catch {
    Write-Host "❌ Cannot connect to N8N API" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test 3: Check Environment Variables
Write-Host "Test 3: Verify Environment Variables" -ForegroundColor Yellow
$envVars = @(
    "N8N_COMMUNITY_PACKAGES_ALLOW_TOOL_USAGE",
    "N8N_API_KEY",
    "N8N_BASE_URL",
    "MCP_OPENAI_API_KEY",
    "MCP_ANTHROPIC_API_KEY",
    "MCP_GITHUB_TOKEN"
)

$allSet = $true
foreach ($var in $envVars) {
    $value = [Environment]::GetEnvironmentVariable($var)
    if ([string]::IsNullOrEmpty($value)) {
        Write-Host "  ❌ $var - NOT SET" -ForegroundColor Red
        $allSet = $false
    } else {
        $maskedValue = $value.Substring(0, [Math]::Min(10, $value.Length)) + "..."
        Write-Host "  ✅ $var - $maskedValue" -ForegroundColor Green
    }
}

if ($allSet) {
    Write-Host "✅ All environment variables are configured" -ForegroundColor Green
} else {
    Write-Host "⚠️  Some environment variables are missing" -ForegroundColor Yellow
}
Write-Host ""

# Test 4: List Available MCP Servers
Write-Host "Test 4: Check Installed MCP Servers" -ForegroundColor Yellow
$mcpServers = @(
    "@modelcontextprotocol/server-brave-search",
    "@modelcontextprotocol/server-filesystem",
    "@modelcontextprotocol/server-github",
    "@modelcontextprotocol/server-example-streamable"
)

foreach ($server in $mcpServers) {
    try {
        $installed = npm list -g $server 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✅ $server" -ForegroundColor Green
        } else {
            Write-Host "  ❌ $server - NOT INSTALLED" -ForegroundColor Red
            Write-Host "     Install with: npm install -g $server" -ForegroundColor Gray
        }
    } catch {
        Write-Host "  ⚠️  $server - UNKNOWN" -ForegroundColor Yellow
    }
}
Write-Host ""

# Test 5: Test MCP Tools
Write-Host "Test 5: Test MCP Client in N8N (Manual Step)" -ForegroundColor Yellow
Write-Host "To test MCP Client in N8N:" -ForegroundColor White
Write-Host "1. Open n8n UI" -ForegroundColor Gray
Write-Host "2. Create new workflow" -ForegroundColor Gray
Write-Host "3. Add 'MCP Client' node" -ForegroundColor Gray
Write-Host "4. Configure credentials (HTTP Streamable)" -ForegroundColor Gray
Write-Host "5. Select 'List Tools' operation" -ForegroundColor Gray
Write-Host "6. Execute and verify tools are listed" -ForegroundColor Gray
Write-Host ""

# Summary
Write-Host "📊 Test Summary" -ForegroundColor Cyan
Write-Host "===============" -ForegroundColor Cyan
Write-Host "Next steps:" -ForegroundColor White
Write-Host "1. If MCP server is not running, start it:" -ForegroundColor Gray
Write-Host "   npx @modelcontextprotocol/server-example-streamable" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Install missing MCP servers globally" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Configure MCP Client credentials in n8n UI" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Test workflows with MCP Client node" -ForegroundColor Gray
Write-Host ""

Write-Host "✅ Testing complete!" -ForegroundColor Green
