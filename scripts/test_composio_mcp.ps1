# 🧪 Composio MCP Connection Test Script

Write-Host "🔌 Testing Composio MCP Connection..." -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Configuration
$apiKey = "ak_VnzNckpdAt9k0xMhVtzd"
$mcpUrl = "https://backend.composio.dev/v3/mcp/be4a071b-1b59-413b-9483-56a9a3cd2bb4/mcp?user_id=pg-test-3259f522-976a-4bcb-b8fb-feabf399a58e"

# Headers
$headers = @{
    "x-api-key" = $apiKey
    "Content-Type" = "application/json"
}

Write-Host "📍 MCP Endpoint: $mcpUrl" -ForegroundColor Gray
Write-Host "🔑 API Key: ak_VnzN...d" -ForegroundColor Gray
Write-Host ""

# Test 1: List Available Tools (MCP JSON-RPC Request)
Write-Host "Test 1: Listing Available Tools..." -ForegroundColor Yellow

$listToolsRequest = @{
    jsonrpc = "2.0"
    method = "tools/list"
    id = 1
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri $mcpUrl -Headers $headers -Method POST -Body $listToolsRequest
    
    if ($response.result) {
        Write-Host "✅ Connection Successful!" -ForegroundColor Green
        Write-Host ""
        Write-Host "📦 Available Tools:" -ForegroundColor Cyan
        
        $tools = $response.result.tools
        if ($tools) {
            $toolCount = $tools.Count
            Write-Host "Total Tools: $toolCount" -ForegroundColor White
            Write-Host ""
            
            # Show first 20 tools
            $tools | Select-Object -First 20 | ForEach-Object {
                Write-Host "  ✓ $($_.name)" -ForegroundColor Green
                if ($_.description) {
                    Write-Host "    $($_.description)" -ForegroundColor Gray
                }
            }
            
            if ($toolCount -gt 20) {
                Write-Host ""
                Write-Host "  ... and $($toolCount - 20) more tools" -ForegroundColor Gray
            }
        }
    } else {
        Write-Host "⚠️  Unexpected response format" -ForegroundColor Yellow
        Write-Host "Response: $($response | ConvertTo-Json)" -ForegroundColor Gray
    }
} catch {
    Write-Host "❌ Connection Failed" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    
    if ($_.ErrorDetails.Message) {
        Write-Host "Details: $($_.ErrorDetails.Message)" -ForegroundColor Red
    }
}

Write-Host ""

# Test 2: Check for Specific Tools
Write-Host "Test 2: Checking for Key Tools..." -ForegroundColor Yellow

$keyTools = @("GMAIL_SEND_EMAIL", "LINKEDIN_CREATE_POST", "TWITTER_CREATE_TWEET", "REDDIT_SUBMIT_POST")

try {
    $response = Invoke-RestMethod -Uri $mcpUrl -Headers $headers -Method POST -Body $listToolsRequest
    
    if ($response.result.tools) {
        $availableToolNames = $response.result.tools | ForEach-Object { $_.name }
        
        foreach ($tool in $keyTools) {
            if ($availableToolNames -contains $tool) {
                Write-Host "  ✅ $tool - Available" -ForegroundColor Green
            } else {
                Write-Host "  ❌ $tool - Not Found" -ForegroundColor Red
            }
        }
    }
} catch {
    Write-Host "❌ Could not check tools" -ForegroundColor Red
}

Write-Host ""

# Test 3: Get Server Info
Write-Host "Test 3: Getting Server Information..." -ForegroundColor Yellow

$infoRequest = @{
    jsonrpc = "2.0"
    method = "initialize"
    params = @{
        protocolVersion = "2024-11-05"
        capabilities = @{}
        clientInfo = @{
            name = "n8n-mcp-test"
            version = "1.0.0"
        }
    }
    id = 2
} | ConvertTo-Json -Depth 10

try {
    $response = Invoke-RestMethod -Uri $mcpUrl -Headers $headers -Method POST -Body $infoRequest
    
    if ($response.result) {
        Write-Host "✅ Server Info Retrieved" -ForegroundColor Green
        
        if ($response.result.serverInfo) {
            Write-Host "  Server Name: $($response.result.serverInfo.name)" -ForegroundColor Gray
            Write-Host "  Version: $($response.result.serverInfo.version)" -ForegroundColor Gray
        }
        
        if ($response.result.capabilities) {
            Write-Host "  Capabilities: Tools, Resources" -ForegroundColor Gray
        }
    }
} catch {
    Write-Host "⚠️  Server info not available (this is OK)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "📊 Test Summary" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Next Steps:" -ForegroundColor White
Write-Host "1. Install MCP Client node in n8n UI" -ForegroundColor Gray
Write-Host "2. Create HTTP Streamable credentials with:" -ForegroundColor Gray
Write-Host "   URL: $mcpUrl" -ForegroundColor Yellow
Write-Host "   Header: x-api-key:$apiKey" -ForegroundColor Yellow
Write-Host "3. Test 'List Tools' operation in n8n" -ForegroundColor Gray
Write-Host "4. Start using Gmail, LinkedIn, Twitter, Reddit tools!" -ForegroundColor Gray
Write-Host ""

Write-Host "📚 Full Guide: COMPOSIO_MCP_SETUP.md" -ForegroundColor Cyan
Write-Host ""
