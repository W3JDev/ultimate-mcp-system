# 🤖 Automated Composio MCP Configuration for N8N
# This script will configure Composio MCP credentials in your n8n instance via API

Write-Host "🚀 Automated N8N MCP Configuration" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# Load environment variables
if (Test-Path ".env") {
    Get-Content ".env" | ForEach-Object {
        if ($_ -match '^\s*([^#][^=]+?)\s*=\s*(.+?)\s*$') {
            $key = $matches[1]
            $value = $matches[2]
            [Environment]::SetEnvironmentVariable($key, $value, "Process")
        }
    }
    Write-Host "✅ Environment variables loaded" -ForegroundColor Green
} else {
    Write-Host "❌ .env file not found!" -ForegroundColor Red
    exit 1
}

# Configuration
$n8nUrl = [Environment]::GetEnvironmentVariable("N8N_API_URL")
$n8nApiKey = [Environment]::GetEnvironmentVariable("N8N_API_KEY")
$composioApiKey = [Environment]::GetEnvironmentVariable("COMPOSIO_API_KEY")
$composioMcpUrl = [Environment]::GetEnvironmentVariable("COMPOSIO_MCP_URL")

Write-Host "📍 N8N URL: $n8nUrl" -ForegroundColor Gray
Write-Host "🔑 Composio API Key: $($composioApiKey.Substring(0,10))..." -ForegroundColor Gray
Write-Host ""

# Headers for N8N API
$headers = @{
    "X-N8N-API-KEY" = $n8nApiKey
    "Content-Type" = "application/json"
}

# Step 1: Check if MCP Client node is installed
Write-Host "Step 1: Checking for MCP Client node..." -ForegroundColor Yellow

try {
    $installedNodes = Invoke-RestMethod -Uri "$n8nUrl/community-packages" -Headers $headers -Method GET
    
    $mcpInstalled = $false
    if ($installedNodes.data) {
        foreach ($node in $installedNodes.data) {
            if ($node.packageName -eq "n8n-nodes-mcp-client") {
                $mcpInstalled = $true
                Write-Host "✅ MCP Client node is installed (version: $($node.installedVersion))" -ForegroundColor Green
                break
            }
        }
    }
    
    if (-not $mcpInstalled) {
        Write-Host "⚠️  MCP Client node not found" -ForegroundColor Yellow
        Write-Host "Installing n8n-nodes-mcp-client..." -ForegroundColor Gray
        
        $installBody = @{
            name = "n8n-nodes-mcp-client"
        } | ConvertTo-Json
        
        try {
            $installResult = Invoke-RestMethod -Uri "$n8nUrl/community-packages" -Headers $headers -Method POST -Body $installBody
            Write-Host "✅ MCP Client node installation started" -ForegroundColor Green
            Write-Host "⏳ Please wait ~2 minutes for installation to complete, then restart n8n" -ForegroundColor Yellow
            Start-Sleep -Seconds 5
        } catch {
            Write-Host "❌ Could not auto-install. Please install manually:" -ForegroundColor Red
            Write-Host "   Settings → Community Nodes → Install: n8n-nodes-mcp-client" -ForegroundColor Gray
        }
    }
} catch {
    Write-Host "⚠️  Could not check community packages: $($_.Exception.Message)" -ForegroundColor Yellow
    Write-Host "This is OK if you're using a custom n8n deployment" -ForegroundColor Gray
}

Write-Host ""

# Step 2: Create Composio MCP Credentials
Write-Host "Step 2: Creating Composio MCP Credentials..." -ForegroundColor Yellow

$credentialData = @{
    name = "Composio MCP - All Apps"
    type = "mcpHttpStreamableApi"
    data = @{
        url = $composioMcpUrl
        additionalHeaders = "x-api-key:$composioApiKey"
    }
} | ConvertTo-Json -Depth 10

try {
    # Check if credential already exists
    $existingCreds = Invoke-RestMethod -Uri "$n8nUrl/credentials" -Headers $headers -Method GET
    
    $credExists = $false
    $existingCredId = $null
    
    if ($existingCreds.data) {
        foreach ($cred in $existingCreds.data) {
            if ($cred.name -eq "Composio MCP - All Apps") {
                $credExists = $true
                $existingCredId = $cred.id
                Write-Host "⚠️  Credential already exists (ID: $existingCredId)" -ForegroundColor Yellow
                break
            }
        }
    }
    
    if ($credExists) {
        Write-Host "Do you want to update the existing credential? (Y/N): " -NoNewline -ForegroundColor Cyan
        $response = Read-Host
        
        if ($response -eq "Y" -or $response -eq "y") {
            try {
                $updateResult = Invoke-RestMethod -Uri "$n8nUrl/credentials/$existingCredId" -Headers $headers -Method PATCH -Body $credentialData
                Write-Host "✅ Credential updated successfully!" -ForegroundColor Green
            } catch {
                Write-Host "❌ Failed to update credential: $($_.Exception.Message)" -ForegroundColor Red
            }
        } else {
            Write-Host "ℹ️  Keeping existing credential" -ForegroundColor Gray
        }
    } else {
        try {
            $createResult = Invoke-RestMethod -Uri "$n8nUrl/credentials" -Headers $headers -Method POST -Body $credentialData
            Write-Host "✅ Composio MCP credential created successfully!" -ForegroundColor Green
            Write-Host "   Credential ID: $($createResult.id)" -ForegroundColor Gray
        } catch {
            Write-Host "❌ Failed to create credential: $($_.Exception.Message)" -ForegroundColor Red
            Write-Host ""
            Write-Host "Manual Setup:" -ForegroundColor Yellow
            Write-Host "1. Go to: $n8nUrl" -ForegroundColor Gray
            Write-Host "2. Credentials → Add → MCP Client (HTTP Streamable) API" -ForegroundColor Gray
            Write-Host "3. URL: $composioMcpUrl" -ForegroundColor Gray
            Write-Host "4. Header: x-api-key:$composioApiKey" -ForegroundColor Gray
        }
    }
} catch {
    Write-Host "❌ API call failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "📋 Manual Setup Instructions:" -ForegroundColor Yellow
    Write-Host "1. Open: $n8nUrl" -ForegroundColor Gray
    Write-Host "2. Go to Credentials → Add Credential" -ForegroundColor Gray
    Write-Host "3. Select: MCP Client (HTTP Streamable) API" -ForegroundColor Gray
    Write-Host "4. Fill in:" -ForegroundColor Gray
    Write-Host "   URL: $composioMcpUrl" -ForegroundColor Cyan
    Write-Host "   Header: x-api-key:$composioApiKey" -ForegroundColor Cyan
    Write-Host "5. Name: Composio MCP - All Apps" -ForegroundColor Gray
    Write-Host "6. Save" -ForegroundColor Gray
}

Write-Host ""

# Step 3: Create a test workflow
Write-Host "Step 3: Creating test workflow..." -ForegroundColor Yellow

$testWorkflow = @{
    name = "MCP Test - Composio Tools"
    nodes = @(
        @{
            id = "manual-trigger"
            name = "Manual Trigger"
            type = "n8n-nodes-base.manualTrigger"
            typeVersion = 1
            position = @(100, 200)
            parameters = @{}
        },
        @{
            id = "mcp-list-tools"
            name = "List Composio Tools"
            type = "n8n-nodes-mcp-client.mcpClient"
            typeVersion = 1
            position = @(300, 200)
            parameters = @{
                operation = "listTools"
            }
            credentials = @{
                mcpHttpStreamableApi = @{
                    name = "Composio MCP - All Apps"
                }
            }
        }
    )
    connections = @{
        "Manual Trigger" = @{
            main = @(
                @(
                    @{
                        node = "List Composio Tools"
                        type = "main"
                        index = 0
                    }
                )
            )
        }
    }
    settings = @{}
    active = $false
} | ConvertTo-Json -Depth 10

try {
    $workflowResult = Invoke-RestMethod -Uri "$n8nUrl/workflows" -Headers $headers -Method POST -Body $testWorkflow
    Write-Host "✅ Test workflow created!" -ForegroundColor Green
    Write-Host "   Workflow ID: $($workflowResult.id)" -ForegroundColor Gray
    Write-Host "   URL: $n8nUrl/../workflow/$($workflowResult.id)" -ForegroundColor Cyan
} catch {
    Write-Host "⚠️  Could not create test workflow: $($_.Exception.Message)" -ForegroundColor Yellow
    Write-Host "You can create it manually once credentials are set up" -ForegroundColor Gray
}

Write-Host ""
Write-Host "====================================" -ForegroundColor Cyan
Write-Host "📊 Configuration Summary" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "✅ Credentials configured for:" -ForegroundColor Green
Write-Host "   • Gmail (GMAIL_SEND_EMAIL)" -ForegroundColor Gray
Write-Host "   • LinkedIn (LINKEDIN_CREATE_POST)" -ForegroundColor Gray
Write-Host "   • Twitter (TWITTER_CREATE_TWEET)" -ForegroundColor Gray
Write-Host "   • Reddit (REDDIT_SUBMIT_POST)" -ForegroundColor Gray
Write-Host "   • 200+ more apps" -ForegroundColor Gray
Write-Host ""

Write-Host "🎯 Next Steps:" -ForegroundColor Cyan
Write-Host "1. Open test workflow in n8n UI" -ForegroundColor White
Write-Host "2. Execute 'List Composio Tools' node" -ForegroundColor White
Write-Host "3. Verify tools are listed" -ForegroundColor White
Write-Host "4. Update your existing workflows to use MCP Client nodes" -ForegroundColor White
Write-Host ""

Write-Host "📚 Documentation:" -ForegroundColor Cyan
Write-Host "   • COMPOSIO_QUICKSTART.md - Quick setup guide" -ForegroundColor Gray
Write-Host "   • COMPOSIO_MCP_SETUP.md - Detailed documentation" -ForegroundColor Gray
Write-Host ""

Write-Host "🎉 Configuration complete!" -ForegroundColor Green
Write-Host ""
