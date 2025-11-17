# Ultimate MCP System - GCP Cloud Run Deployment Script
# Deploys all services to Google Cloud Platform

param(
    [string]$ProjectId = "ultimate-mcp-system",
    [string]$Region = "us-central1",
    [switch]$SkipBuild,
    [switch]$Verbose
)

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "☁️  DEPLOYING ULTIMATE MCP SYSTEM TO GCP CLOUD RUN" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check if gcloud is installed
if (-not (Get-Command gcloud -ErrorAction SilentlyContinue)) {
    Write-Host "❌ gcloud CLI not found. Please install it first:" -ForegroundColor Red
    Write-Host "   https://cloud.google.com/sdk/docs/install" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

# Check if logged in
$account = gcloud auth list --filter=status:ACTIVE --format="value(account)" 2>$null
if (-not $account) {
    Write-Host "❌ Not logged into gcloud. Please run: gcloud auth login" -ForegroundColor Red
    Write-Host ""
    exit 1
}

Write-Host "✅ Logged in as: $account" -ForegroundColor Green
Write-Host "📦 Project ID: $ProjectId" -ForegroundColor Cyan
Write-Host "🌍 Region: $Region" -ForegroundColor Cyan
Write-Host ""

# Set project
Write-Host "🔧 Setting GCP project..." -ForegroundColor Yellow
gcloud config set project $ProjectId 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to set project. Please check project ID." -ForegroundColor Red
    exit 1
}
Write-Host "   ✅ Project set" -ForegroundColor Green
Write-Host ""

# Load environment variables
Write-Host "🔐 Loading environment variables..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Write-Host "❌ .env file not found!" -ForegroundColor Red
    exit 1
}

$envVars = @()
Get-Content ".env" | ForEach-Object {
    if ($_ -match '^([^=]+)=(.*)$') {
        $key = $Matches[1].Trim()
        $value = $Matches[2].Trim()
        # Remove quotes if present
        $value = $value -replace '^["'']|["'']$', ''
        $envVars += "$key=$value"
    }
}
Write-Host "   ✅ Loaded $($envVars.Count) environment variables" -ForegroundColor Green
Write-Host ""

# Build and deploy services
$services = @(
    @{
        Name = "ultimate-mcp-master"
        Port = 7860
        Source = "."
        Dockerfile = "Dockerfile"
        Memory = "2Gi"
        CPU = "2"
    },
    @{
        Name = "ultimate-mcp-n8n"
        Port = 7862
        Source = "."
        Dockerfile = "backend/Dockerfile"
        Memory = "1Gi"
        CPU = "1"
    },
    @{
        Name = "ultimate-mcp-agent"
        Port = 7863
        Source = "."
        Dockerfile = "backend/Dockerfile"
        Memory = "2Gi"
        CPU = "2"
    },
    @{
        Name = "ultimate-mcp-local"
        Port = 7864
        Source = "."
        Dockerfile = "backend/Dockerfile"
        Memory = "1Gi"
        CPU = "1"
    }
)

$deployedCount = 0
$failedCount = 0

foreach ($service in $services) {
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host "🚀 Deploying $($service.Name)..." -ForegroundColor Cyan
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host ""
    
    $envString = $envVars -join ","
    
    $deployArgs = @(
        "run", "deploy", $service.Name,
        "--source", $service.Source,
        "--region", $Region,
        "--platform", "managed",
        "--allow-unauthenticated",
        "--port", $service.Port,
        "--memory", $service.Memory,
        "--cpu", $service.CPU,
        "--set-env-vars", $envString,
        "--timeout", "300",
        "--concurrency", "80",
        "--min-instances", "0",
        "--max-instances", "10"
    )
    
    if ($Verbose) {
        $deployArgs += "--verbosity=debug"
    }
    
    Write-Host "Running: gcloud $($deployArgs -join ' ')" -ForegroundColor Gray
    Write-Host ""
    
    & gcloud @deployArgs
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ $($service.Name) deployed successfully!" -ForegroundColor Green
        $deployedCount++
        
        # Get service URL
        $url = gcloud run services describe $service.Name --region=$Region --format="value(status.url)" 2>$null
        if ($url) {
            Write-Host "   URL: $url" -ForegroundColor Cyan
        }
    } else {
        Write-Host ""
        Write-Host "❌ Failed to deploy $($service.Name)" -ForegroundColor Red
        $failedCount++
    }
    
    Write-Host ""
}

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "📊 DEPLOYMENT SUMMARY" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "✅ Deployed: $deployedCount" -ForegroundColor Green
Write-Host "❌ Failed: $failedCount" -ForegroundColor Red
Write-Host ""

if ($failedCount -eq 0) {
    Write-Host "🎉 ALL SERVICES DEPLOYED SUCCESSFULLY!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Test the deployed services" -ForegroundColor White
    Write-Host "2. Update DNS records if needed" -ForegroundColor White
    Write-Host "3. Monitor logs: gcloud logging tail" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host "⚠️  SOME DEPLOYMENTS FAILED" -ForegroundColor Yellow
    Write-Host "Check the logs above for details." -ForegroundColor Yellow
    Write-Host ""
    exit 1
}
