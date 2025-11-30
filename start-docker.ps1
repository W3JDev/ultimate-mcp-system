# 🚀 Quick Start - Agent Builder Docker

Write-Host "`n🐳 Starting Agent Builder MCP in Docker...`n" -ForegroundColor Cyan

# Check if .env exists
if (-not (Test-Path ".env")) {
    Write-Host "❌ ERROR: .env file not found!" -ForegroundColor Red
    Write-Host "📝 Copy .env.example to .env and fill in your API keys`n" -ForegroundColor Yellow
    exit 1
}

# Check if Docker is running
try {
    docker ps | Out-Null
} catch {
    Write-Host "❌ ERROR: Docker is not running!" -ForegroundColor Red
    Write-Host "🐳 Please start Docker Desktop and try again`n" -ForegroundColor Yellow
    exit 1
}

# Navigate to agent builder directory
Set-Location backend/mcp_servers/agent_builder

Write-Host "📦 Building Docker image..." -ForegroundColor Yellow
docker-compose build

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Build successful!`n" -ForegroundColor Green
    
    Write-Host "🚀 Starting container in detached mode..." -ForegroundColor Yellow
    docker-compose up -d
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✅ Agent Builder MCP is running!`n" -ForegroundColor Green
        Write-Host "============================================" -ForegroundColor Cyan
        Write-Host "🌐 Web UI:  http://localhost:7863" -ForegroundColor White
        Write-Host "📊 Logs:    docker-compose logs -f" -ForegroundColor White
        Write-Host "🛑 Stop:    docker-compose down" -ForegroundColor White
        Write-Host "🔄 Restart: docker-compose restart" -ForegroundColor White
        Write-Host "============================================`n" -ForegroundColor Cyan
        
        # Wait a moment for container to start
        Start-Sleep -Seconds 3
        
        # Show logs
        Write-Host "📋 Container logs (Ctrl+C to exit):`n" -ForegroundColor Yellow
        docker-compose logs -f
    } else {
        Write-Host "`n❌ Failed to start container`n" -ForegroundColor Red
        docker-compose logs
        exit 1
    }
} else {
    Write-Host "`n❌ Build failed!`n" -ForegroundColor Red
    exit 1
}
