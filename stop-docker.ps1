# 🛑 Stop Docker Containers

Write-Host "`n🛑 Stopping Agent Builder MCP...`n" -ForegroundColor Yellow

Set-Location backend/mcp_servers/agent_builder

docker-compose down

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ Container stopped successfully`n" -ForegroundColor Green
} else {
    Write-Host "`n❌ Error stopping container`n" -ForegroundColor Red
}

Set-Location ../../..
