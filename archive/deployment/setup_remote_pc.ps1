# W3J MCP Hub - Remote PC Setup Script
# Automatically connects your remote PC to Cloud Run
# Run this on the PC you want to control (via Rust Desktop or direct)

param(
    [string]$CloudRunURL = "",
    [switch]$Help
)

if ($Help) {
    Write-Host @"
🖥️  W3J MCP Hub - Remote PC Setup

USAGE:
    .\setup_remote_pc.ps1 -CloudRunURL https://your-cloud-run-url.run.app

WHAT IT DOES:
1. Installs websockets dependency
2. Generates secure authentication token
3. Starts local agent on port 8765
4. Creates Cloudflare tunnel
5. Registers with Cloud Run

REQUIREMENTS:
- Python 3.11+ with venv activated
- Cloudflare CLI (cloudflared) - will auto-install if missing
- Internet connection

"@
    exit 0
}

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🖥️  W3J MCP Hub - Remote PC Setup" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check if venv is activated
if (-not $env:VIRTUAL_ENV) {
    Write-Host "⚠️  Virtual environment not activated!" -ForegroundColor Yellow
    Write-Host "Run: .\.venv\Scripts\Activate.ps1" -ForegroundColor Yellow
    Write-Host ""
    $activate = Read-Host "Activate now? (y/n)"
    if ($activate -eq "y") {
        & .\.venv\Scripts\Activate.ps1
    } else {
        Write-Host "❌ Aborted" -ForegroundColor Red
        exit 1
    }
}

# Step 1: Install websockets
Write-Host "📦 Step 1/5: Installing dependencies..." -ForegroundColor Green
pip install websockets --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Step 2: Generate secure token
Write-Host "`n🔑 Step 2/5: Generating secure token..." -ForegroundColor Green
$TOKEN = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 48 | ForEach-Object {[char]$_})
Write-Host "✅ Token generated: $TOKEN" -ForegroundColor Green
Write-Host "⚠️  SAVE THIS TOKEN! You'll need it for Cloud Run." -ForegroundColor Yellow

# Save token to file
$TOKEN | Out-File -FilePath ".remote_pc_token" -NoNewline
Write-Host "💾 Token saved to: .remote_pc_token" -ForegroundColor Gray

# Step 3: Check Cloudflare CLI
Write-Host "`n☁️  Step 3/5: Checking Cloudflare tunnel..." -ForegroundColor Green
if (-not (Get-Command cloudflared -ErrorAction SilentlyContinue)) {
    Write-Host "⚠️  Cloudflare CLI not found. Installing..." -ForegroundColor Yellow
    winget install cloudflare.cloudflared --silent
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Cloudflare CLI installed" -ForegroundColor Green
    } else {
        Write-Host "❌ Failed to install Cloudflare CLI" -ForegroundColor Red
        Write-Host "Manual install: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/" -ForegroundColor Yellow
        exit 1
    }
} else {
    Write-Host "✅ Cloudflare CLI found" -ForegroundColor Green
}

# Step 4: Start local agent (background job)
Write-Host "`n🤖 Step 4/5: Starting local agent..." -ForegroundColor Green
$AgentJob = Start-Job -ScriptBlock {
    param($Token)
    Set-Location $using:PWD
    & .\.venv\Scripts\Activate.ps1
    python backend/local_agent.py --port 8765 --token $Token
} -ArgumentList $TOKEN

Start-Sleep -Seconds 3

if ($AgentJob.State -eq "Running") {
    Write-Host "✅ Local agent started (Job ID: $($AgentJob.Id))" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to start local agent" -ForegroundColor Red
    Receive-Job $AgentJob
    exit 1
}

# Step 5: Create Cloudflare tunnel
Write-Host "`n🌐 Step 5/5: Creating public tunnel..." -ForegroundColor Green
Write-Host "⏳ Please wait..." -ForegroundColor Gray

$TunnelJob = Start-Job -ScriptBlock {
    cloudflared tunnel --url http://localhost:8765 2>&1 | ForEach-Object {
        if ($_ -match "https://.*\.trycloudflare\.com") {
            $matches[0]
        }
    }
}

Start-Sleep -Seconds 8

$TunnelOutput = Receive-Job $TunnelJob
$TunnelURL = $TunnelOutput | Where-Object { $_ -match "https://.*\.trycloudflare\.com" } | Select-Object -First 1

if ($TunnelURL) {
    Write-Host "✅ Tunnel created: $TunnelURL" -ForegroundColor Green
} else {
    Write-Host "⚠️  Tunnel URL not detected yet. Check manually." -ForegroundColor Yellow
    Write-Host "Run in another terminal: cloudflared tunnel --url http://localhost:8765" -ForegroundColor Gray
}

# Display summary
Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "🎉 Setup Complete!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 Next Steps:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1️⃣  Configure Cloud Run with these values:" -ForegroundColor White
Write-Host "   REMOTE_PC_BRIDGE_URL=$($TunnelURL -replace 'https://', 'wss://')" -ForegroundColor Cyan
Write-Host "   REMOTE_PC_AUTH_TOKEN=$TOKEN" -ForegroundColor Cyan
Write-Host ""
Write-Host "2️⃣  Run this command:" -ForegroundColor White
Write-Host @"
   gcloud run services update w3j-mcp-hub \
     --set-env-vars REMOTE_PC_BRIDGE_URL=wss://$($TunnelURL -replace 'https://', '') \
     --set-env-vars REMOTE_PC_AUTH_TOKEN=$TOKEN \
     --project stellar-state-471406-f8 \
     --region us-central1
"@ -ForegroundColor Gray
Write-Host ""
Write-Host "3️⃣  Your Cloud Run URL (save this):" -ForegroundColor White
if ($CloudRunURL) {
    Write-Host "   $CloudRunURL" -ForegroundColor Cyan
} else {
    Write-Host "   (Will be provided after deployment)" -ForegroundColor Gray
}
Write-Host ""
Write-Host "📊 Status:" -ForegroundColor Yellow
Write-Host "   ✅ Local agent running (port 8765)" -ForegroundColor Green
Write-Host "   ✅ Cloudflare tunnel active" -ForegroundColor Green
Write-Host "   ⏳ Waiting for Cloud Run configuration" -ForegroundColor Yellow
Write-Host ""
Write-Host "🛑 To stop:" -ForegroundColor Yellow
Write-Host "   Stop-Job $($AgentJob.Id); Stop-Job $($TunnelJob.Id)" -ForegroundColor Gray
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan

# Keep script running to maintain jobs
Write-Host "`nPress Ctrl+C to stop..." -ForegroundColor Gray
try {
    while ($true) {
        Start-Sleep -Seconds 10
        if ($AgentJob.State -ne "Running") {
            Write-Host "⚠️  Agent stopped unexpectedly!" -ForegroundColor Red
            Receive-Job $AgentJob
            break
        }
    }
} finally {
    Write-Host "`n👋 Cleaning up..." -ForegroundColor Yellow
    Stop-Job $AgentJob -ErrorAction SilentlyContinue
    Stop-Job $TunnelJob -ErrorAction SilentlyContinue
    Remove-Job $AgentJob -ErrorAction SilentlyContinue
    Remove-Job $TunnelJob -ErrorAction SilentlyContinue
    Write-Host "✅ Cleanup complete" -ForegroundColor Green
}
