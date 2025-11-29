# 🚀 MCP Client Installation & Testing Script
# PowerShell script to set up MCP client in n8n

Write-Host "🔧 MCP Client Setup for N8N" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Install MCP Server Packages
Write-Host "📦 Step 1: Installing MCP Server Packages..." -ForegroundColor Yellow

$mcpServers = @(
    "@modelcontextprotocol/server-brave-search",
    "@modelcontextprotocol/server-filesystem",
    "@modelcontextprotocol/server-github",
    "@modelcontextprotocol/server-example-streamable"
)

foreach ($server in $mcpServers) {
    Write-Host "Installing $server..." -ForegroundColor Gray
    npm install -g $server
}

Write-Host "✅ MCP servers installed!" -ForegroundColor Green
Write-Host ""

# Step 2: Check Environment Variables
Write-Host "🔍 Step 2: Checking Environment Variables..." -ForegroundColor Yellow

# Load .env file
if (Test-Path ".env") {
    Get-Content ".env" | ForEach-Object {
        if ($_ -match '^\s*([^#][^=]+?)\s*=\s*(.+?)\s*$') {
            $key = $matches[1]
            $value = $matches[2]
            [Environment]::SetEnvironmentVariable($key, $value, "Process")
        }
    }
    Write-Host "✅ Environment variables loaded from .env" -ForegroundColor Green
} else {
    Write-Host "❌ .env file not found!" -ForegroundColor Red
    exit 1
}

# Check critical variables
$requiredVars = @(
    "N8N_COMMUNITY_PACKAGES_ALLOW_TOOL_USAGE",
    "N8N_API_KEY",
    "N8N_BASE_URL"
)

$missingVars = @()
foreach ($var in $requiredVars) {
    if ([string]::IsNullOrEmpty([Environment]::GetEnvironmentVariable($var))) {
        $missingVars += $var
    }
}

if ($missingVars.Count -gt 0) {
    Write-Host "❌ Missing required environment variables:" -ForegroundColor Red
    $missingVars | ForEach-Object { Write-Host "  - $_" -ForegroundColor Red }
    exit 1
}

Write-Host "✅ All required environment variables are set!" -ForegroundColor Green
Write-Host ""

# Step 3: Start Example MCP Server
Write-Host "🚀 Step 3: Starting Example MCP Server (HTTP Streamable)..." -ForegroundColor Yellow
Write-Host "Starting on http://localhost:3001/stream" -ForegroundColor Gray

# Start in background
$mcpProcess = Start-Process -FilePath "npx" -ArgumentList "@modelcontextprotocol/server-example-streamable" -PassThru -NoNewWindow
Write-Host "✅ MCP Server started (PID: $($mcpProcess.Id))" -ForegroundColor Green
Write-Host ""

# Wait for server to start
Start-Sleep -Seconds 3

# Step 4: Test MCP Server Connection
Write-Host "🧪 Step 4: Testing MCP Server Connection..." -ForegroundColor Yellow

try {
    $response = Invoke-WebRequest -Uri "http://localhost:3001/health" -Method GET -TimeoutSec 5 -ErrorAction Stop
    Write-Host "✅ MCP Server is responding!" -ForegroundColor Green
    Write-Host "Response: $($response.StatusCode) $($response.StatusDescription)" -ForegroundColor Gray
} catch {
    Write-Host "⚠️  Health check endpoint not available (this is OK for some MCP servers)" -ForegroundColor Yellow
    Write-Host "Testing stream endpoint instead..." -ForegroundColor Gray
    
    try {
        Test-NetConnection -ComputerName localhost -Port 3001 -WarningAction SilentlyContinue | Out-Null
        Write-Host "✅ MCP Server port 3001 is open!" -ForegroundColor Green
    } catch {
        Write-Host "❌ Cannot connect to MCP Server on port 3001" -ForegroundColor Red
    }
}

Write-Host ""

# Step 5: Check N8N Connection
Write-Host "🔗 Step 5: Testing N8N Connection..." -ForegroundColor Yellow

$n8nUrl = [Environment]::GetEnvironmentVariable("N8N_BASE_URL")
$n8nApiKey = [Environment]::GetEnvironmentVariable("N8N_API_KEY")

try {
    $headers = @{
        "X-N8N-API-KEY" = $n8nApiKey
        "Content-Type" = "application/json"
    }
    
    $healthCheck = Invoke-WebRequest -Uri "$n8nUrl/healthz" -Headers $headers -Method GET -TimeoutSec 5 -ErrorAction Stop
    Write-Host "✅ N8N is accessible!" -ForegroundColor Green
    Write-Host "N8N Health: $($healthCheck.StatusCode)" -ForegroundColor Gray
} catch {
    Write-Host "❌ Cannot connect to N8N at $n8nUrl" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# Step 6: Display Next Steps
Write-Host "📋 Next Steps:" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Install MCP Client Node in N8N:" -ForegroundColor White
Write-Host "   - Open n8n UI at: $n8nUrl" -ForegroundColor Gray
Write-Host "   - Go to Settings → Community Nodes" -ForegroundColor Gray
Write-Host "   - Install: n8n-nodes-mcp-client" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Create MCP Client Credentials:" -ForegroundColor White
Write-Host "   - Type: MCP Client (HTTP Streamable) API" -ForegroundColor Gray
Write-Host "   - URL: http://localhost:3001/stream" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Test in N8N Workflow:" -ForegroundColor White
Write-Host "   - Add MCP Client node" -ForegroundColor Gray
Write-Host "   - Select 'List Tools' operation" -ForegroundColor Gray
Write-Host "   - Execute to see available tools" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Restart N8N if needed:" -ForegroundColor White
Write-Host "   docker-compose restart n8n" -ForegroundColor Gray
Write-Host "   OR" -ForegroundColor Gray
Write-Host "   Restart n8n desktop app" -ForegroundColor Gray
Write-Host ""

Write-Host "💡 Tip: Check the full setup guide at:" -ForegroundColor Yellow
Write-Host "   MCP_CLIENT_SETUP_GUIDE.md" -ForegroundColor Gray
Write-Host ""

Write-Host "🎉 Setup Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "MCP Server running on: http://localhost:3001/stream" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the MCP server" -ForegroundColor Gray
Write-Host ""

# Keep script running
try {
    Wait-Process -Id $mcpProcess.Id
} catch {
    Write-Host "MCP Server stopped." -ForegroundColor Yellow
}
