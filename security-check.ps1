# Pre-Push Security Scan

Write-Host "`nSecurity Scan - Checking for exposed secrets...`n" -ForegroundColor Cyan

$found_issues = $false

# Check if .env is in .gitignore
Write-Host "[1/5] Checking .gitignore..." -ForegroundColor Yellow
if (Select-String -Path .gitignore -Pattern "^\.env$" -Quiet) {
    Write-Host "  [OK] .env is in .gitignore" -ForegroundColor Green
} else {
    Write-Host "  [FAIL] WARNING: .env not found in .gitignore!" -ForegroundColor Red
    $found_issues = $true
}

# Check if .env exists and is not tracked
Write-Host "`n[2/5] Checking if .env is tracked by git..." -ForegroundColor Yellow
$tracked_files = git ls-files
if ($tracked_files -like "*.env*" -or $tracked_files -like "*credentials.json*") {
    Write-Host "  [FAIL] WARNING: Sensitive files are tracked!" -ForegroundColor Red
    $found_issues = $true
    git ls-files | Select-String -Pattern "env|credential|key|secret"
} else {
    Write-Host "  [OK] No .env files tracked" -ForegroundColor Green
}

# Check staged files for secrets
Write-Host "`n[3/5] Checking staged files for API keys..." -ForegroundColor Yellow
$staged_diff = git diff --staged
if ($staged_diff -match "API_KEY|api_key|SECRET|secret|TOKEN|token|PASSWORD|password") {
    Write-Host "  [WARN] Potential secrets in staged files!" -ForegroundColor Red
    $found_issues = $true
    git diff --staged | Select-String -Pattern "API_KEY|SECRET|TOKEN|PASSWORD" | Select-Object -First 5
} else {
    Write-Host "  [OK] No obvious secrets in staged files" -ForegroundColor Green
}

# Check for hardcoded secrets in Python files
Write-Host "`n[4/5] Scanning Python files for hardcoded secrets..." -ForegroundColor Yellow
$secret_patterns = @("sk-ant-", "sk-proj-", "ghp_", "gho_", "Bearer ", "api_key\s*=\s*")
$found_secrets = Get-ChildItem -Recurse -Include *.py | Select-String -Pattern $secret_patterns | Where-Object { $_.Path -notlike "*\.venv*" -and $_.Path -notlike "*archived*" }

if ($found_secrets) {
    Write-Host "  [WARN] Potential hardcoded secrets found!" -ForegroundColor Red
    $found_issues = $true
    $found_secrets | ForEach-Object {
        Write-Host "  File: $($_.Path):$($_.LineNumber)" -ForegroundColor Yellow
    }
} else {
    Write-Host "  [OK] No hardcoded secrets detected" -ForegroundColor Green
}

# Check .env.example exists
Write-Host "`n[5/5] Checking for .env.example..." -ForegroundColor Yellow
if (Test-Path ".env.example") {
    Write-Host "  [OK] .env.example exists" -ForegroundColor Green
} else {
    Write-Host "  [INFO] .env.example not found (optional)" -ForegroundColor Yellow
}

# Final verdict
Write-Host "`n===================================================" -ForegroundColor Cyan
if ($found_issues) {
    Write-Host "[FAIL] Security scan complete with warnings!" -ForegroundColor Red
    Write-Host "       DO NOT PUSH until issues are resolved!" -ForegroundColor Yellow
    Write-Host "===================================================`n" -ForegroundColor Cyan
    exit 1
} else {
    Write-Host "[PASS] Security scan passed - Safe to push!" -ForegroundColor Green
    Write-Host "===================================================`n" -ForegroundColor Cyan
    exit 0
}
