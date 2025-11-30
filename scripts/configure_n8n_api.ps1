# ✅ N8N API Key Configuration Script
# Run this to configure MCP Hub with N8N credentials

Write-Host "🔧 Configuring MCP Hub with N8N API Key..." -ForegroundColor Cyan

$N8N_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4NjRiMmI3Ny03ZmQ0LTQyNDAtOThiMi0xMDgyMjdhNzU0ZTEiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY0NDIzNTg1fQ.ZN3w3hwHQJDsYMiVIacuh6Ogc9PvNkOKevBYhYchABM"
$N8N_BASE_URL = "https://n8n-533751401713.us-central1.run.app"

Write-Host "`nUpdating MCP Hub Cloud Run service..." -ForegroundColor Yellow

gcloud run services update w3j-mcp-hub `
    --set-env-vars "N8N_API_KEY=$N8N_API_KEY,N8N_BASE_URL=$N8N_BASE_URL" `
    --project stellar-state-471406-f8 `
    --region us-central1

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ MCP Hub configured successfully!" -ForegroundColor Green
    Write-Host "`n📋 Configuration:" -ForegroundColor Cyan
    Write-Host "  N8N URL: $N8N_BASE_URL" -ForegroundColor White
    Write-Host "  API Key: ${N8N_API_KEY.Substring(0, 50)}..." -ForegroundColor White
    Write-Host "`n🎯 Next Steps:" -ForegroundColor Cyan
    Write-Host "  1. Visit: https://w3j-mcp-hub-533751401713-uc.a.run.app" -ForegroundColor White
    Write-Host "  2. Test: 'Create a workflow that sends Slack message'" -ForegroundColor White
    Write-Host "  3. Verify actual workflow creation (not 'coming soon')" -ForegroundColor White
} else {
    Write-Host "`n❌ Configuration failed!" -ForegroundColor Red
    Write-Host "Check the error above and try again." -ForegroundColor Yellow
}
