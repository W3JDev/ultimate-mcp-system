# ================================================================================================
# N8N Google Cloud Run Deployment Script
# ================================================================================================
# This script deploys a production-grade N8N instance on Google Cloud Run with:
# - Cloud SQL PostgreSQL database for persistence
# - Secret Manager for credentials
# - Service Account with minimal permissions
# - 2Gi memory, no CPU throttling
# ================================================================================================

param(
    [string]$ProjectId = "stellar-state-471406-f8",
    [string]$Region = "us-central1",
    [string]$DbPassword = "n8n_secure_$(Get-Random -Minimum 1000 -Maximum 9999)",
    [switch]$SkipCleanup
)

Write-Host "🚀 N8N Google Cloud Run Deployment" -ForegroundColor Cyan
Write-Host "================================================================================================" -ForegroundColor Cyan
Write-Host "Project ID: $ProjectId" -ForegroundColor Yellow
Write-Host "Region: $Region" -ForegroundColor Yellow
Write-Host "Database Password: $DbPassword" -ForegroundColor Yellow
Write-Host "================================================================================================`n" -ForegroundColor Cyan

# Set environment variables
$env:PROJECT_ID = $ProjectId
$env:REGION = $Region

Write-Host "📋 Step 1: Setting GCP project and enabling APIs..." -ForegroundColor Green
gcloud config set project $ProjectId

Write-Host "`n🔌 Enabling required APIs (this may take 2-3 minutes)..." -ForegroundColor Yellow
gcloud services enable run.googleapis.com sqladmin.googleapis.com secretmanager.googleapis.com

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to enable APIs" -ForegroundColor Red
    exit 1
}

Write-Host "✅ APIs enabled successfully`n" -ForegroundColor Green

# ================================================================================================
# Step 2: Create Cloud SQL Instance
# ================================================================================================
Write-Host "📋 Step 2: Creating Cloud SQL PostgreSQL instance (this takes ~5 minutes)..." -ForegroundColor Green
Write-Host "Instance: n8n-db | Version: POSTGRES_15 | Tier: db-g1-small" -ForegroundColor Yellow

gcloud sql instances create n8n-db `
    --database-version=POSTGRES_15 `
    --tier=db-g1-small `
    --region=$Region `
    --edition=ENTERPRISE `
    --root-password=postgres

if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Cloud SQL instance may already exist or creation failed" -ForegroundColor Yellow
    Write-Host "Continuing with existing instance..." -ForegroundColor Yellow
} else {
    Write-Host "✅ Cloud SQL instance created successfully`n" -ForegroundColor Green
}

# ================================================================================================
# Step 3: Setup Database and Secrets
# ================================================================================================
Write-Host "📋 Step 3: Setting up N8N database and credentials..." -ForegroundColor Green

# Create database
Write-Host "Creating n8n database..." -ForegroundColor Yellow
gcloud sql databases create n8n --instance=n8n-db 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Database 'n8n' created" -ForegroundColor Green
} else {
    Write-Host "⚠️  Database 'n8n' may already exist" -ForegroundColor Yellow
}

# Create database user
Write-Host "Creating database user 'n8n-user'..." -ForegroundColor Yellow
gcloud sql users create n8n-user --instance=n8n-db --password="$DbPassword" 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Database user created" -ForegroundColor Green
} else {
    Write-Host "⚠️  Database user may already exist" -ForegroundColor Yellow
}

# Store database password in Secret Manager
Write-Host "Storing database password in Secret Manager..." -ForegroundColor Yellow
Write-Output $DbPassword | gcloud secrets create n8n-db-password --replication-policy="automatic" --data-file=- 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Secret 'n8n-db-password' created" -ForegroundColor Green
} else {
    Write-Host "⚠️  Secret may already exist, updating..." -ForegroundColor Yellow
    Write-Output $DbPassword | gcloud secrets versions add n8n-db-password --data-file=-
}

# Generate and store encryption key
Write-Host "Generating encryption key..." -ForegroundColor Yellow
$encryptionKey = -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 56 | ForEach-Object {[char]$_})
$encryptionKey | Out-File -FilePath "n8n-encryption-key.tmp" -NoNewline -Encoding ASCII

gcloud secrets create n8n-encryption-key --data-file=n8n-encryption-key.tmp --replication-policy="automatic" 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Encryption key created" -ForegroundColor Green
} else {
    Write-Host "⚠️  Encryption key may already exist, updating..." -ForegroundColor Yellow
    gcloud secrets versions add n8n-encryption-key --data-file=n8n-encryption-key.tmp
}

Remove-Item "n8n-encryption-key.tmp" -ErrorAction SilentlyContinue

Write-Host "✅ Database and secrets configured`n" -ForegroundColor Green

# ================================================================================================
# Step 4: Create Service Account
# ================================================================================================
Write-Host "📋 Step 4: Creating Service Account with required permissions..." -ForegroundColor Green

gcloud iam service-accounts create n8n-service-account --display-name="n8n Service Account" 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Service Account created" -ForegroundColor Green
} else {
    Write-Host "⚠️  Service Account may already exist" -ForegroundColor Yellow
}

$SA_NAME = "n8n-service-account@$ProjectId.iam.gserviceaccount.com"

# Grant Secret Manager access
Write-Host "Granting Secret Manager access..." -ForegroundColor Yellow
gcloud secrets add-iam-policy-binding n8n-db-password --member="serviceAccount:$SA_NAME" --role="roles/secretmanager.secretAccessor" 2>$null
gcloud secrets add-iam-policy-binding n8n-encryption-key --member="serviceAccount:$SA_NAME" --role="roles/secretmanager.secretAccessor" 2>$null

# Grant Cloud SQL client access
Write-Host "Granting Cloud SQL client access..." -ForegroundColor Yellow
gcloud projects add-iam-policy-binding $ProjectId --member="serviceAccount:$SA_NAME" --role="roles/cloudsql.client" 2>$null

Write-Host "✅ Service Account configured`n" -ForegroundColor Green

# ================================================================================================
# Step 5: Deploy N8N to Cloud Run
# ================================================================================================
Write-Host "📋 Step 5: Deploying N8N to Cloud Run (~2 minutes)..." -ForegroundColor Green
Write-Host "Image: n8nio/n8n:latest | Memory: 2Gi | Port: 5678" -ForegroundColor Yellow

gcloud run deploy n8n `
    --image=n8nio/n8n:latest `
    --command="/bin/sh" `
    --args="-c,sleep 5;n8n start" `
    --region=$Region `
    --allow-unauthenticated `
    --port=5678 `
    --memory=2Gi `
    --no-cpu-throttling `
    --set-env-vars="N8N_PORT=5678,N8N_PROTOCOL=https,DB_TYPE=postgresdb,DB_POSTGRESDB_DATABASE=n8n,DB_POSTGRESDB_USER=n8n-user,DB_POSTGRESDB_HOST=/cloudsql/$ProjectId`:$Region`:n8n-db,DB_POSTGRESDB_PORT=5432,DB_POSTGRESDB_SCHEMA=public,GENERIC_TIMEZONE=UTC,QUEUE_HEALTH_CHECK_ACTIVE=true" `
    --set-secrets="DB_POSTGRESDB_PASSWORD=n8n-db-password:latest,N8N_ENCRYPTION_KEY=n8n-encryption-key:latest" `
    --add-cloudsql-instances=$ProjectId`:$Region`:n8n-db `
    --service-account=$SA_NAME

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Deployment failed" -ForegroundColor Red
    exit 1
}

# ================================================================================================
# Step 6: Get Service URL
# ================================================================================================
Write-Host "`n📋 Step 6: Retrieving N8N Service URL..." -ForegroundColor Green

$n8nUrl = gcloud run services describe n8n --region=$Region --format="value(status.url)"

Write-Host "`n================================================================================================" -ForegroundColor Cyan
Write-Host "✅ N8N DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "================================================================================================" -ForegroundColor Cyan
Write-Host "🌐 N8N Service URL: $n8nUrl" -ForegroundColor Yellow
Write-Host "================================================================================================`n" -ForegroundColor Cyan

# ================================================================================================
# Step 7: Save configuration
# ================================================================================================
$configFile = "n8n_deployment_config.txt"
@"
N8N Deployment Configuration
=============================
Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

Service URL: $n8nUrl
Project ID: $ProjectId
Region: $Region
Database: n8n-db
Database User: n8n-user
Database Password: $DbPassword
Service Account: $SA_NAME

Next Steps:
1. Visit $n8nUrl to setup owner account
2. Update MCP Hub with N8N_BASE_URL: $n8nUrl
3. Create N8N API key and add to MCP Hub
"@ | Out-File -FilePath $configFile -Encoding UTF8

Write-Host "📄 Configuration saved to: $configFile" -ForegroundColor Green

# ================================================================================================
# Step 8: Update MCP Hub configuration
# ================================================================================================
Write-Host "`n📋 Step 7: Next steps for MCP Hub integration..." -ForegroundColor Green
Write-Host "Run this command to update MCP Hub with new N8N URL:" -ForegroundColor Yellow
Write-Host "`ngcloud run services update w3j-mcp-hub ``" -ForegroundColor Cyan
Write-Host "    --set-env-vars `"N8N_BASE_URL=$n8nUrl`" ``" -ForegroundColor Cyan
Write-Host "    --project $ProjectId ``" -ForegroundColor Cyan
Write-Host "    --region $Region`n" -ForegroundColor Cyan

Write-Host "After setting up N8N owner account, get API key from:" -ForegroundColor Yellow
Write-Host "$n8nUrl/settings/api" -ForegroundColor Cyan
Write-Host "`nThen update MCP Hub with N8N API key:" -ForegroundColor Yellow
Write-Host "gcloud run services update w3j-mcp-hub ``" -ForegroundColor Cyan
Write-Host "    --set-env-vars `"N8N_API_KEY=<your-api-key>`" ``" -ForegroundColor Cyan
Write-Host "    --project $ProjectId ``" -ForegroundColor Cyan
Write-Host "    --region $Region`n" -ForegroundColor Cyan

Write-Host "================================================================================================" -ForegroundColor Cyan
Write-Host "✅ Deployment script completed successfully!" -ForegroundColor Green
Write-Host "================================================================================================`n" -ForegroundColor Cyan
