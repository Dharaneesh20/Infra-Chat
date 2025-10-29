# Test Script for Infra-Chat
# This script verifies your installation and tests the API

Write-Host "🧪 Infra-Chat Test Suite" -ForegroundColor Cyan
Write-Host "=" * 60
Write-Host ""

# Test 1: Check if backend is running
Write-Host "Test 1: Backend Health Check" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:5000/api/health" -ErrorAction Stop
    if ($response.status -eq "healthy") {
        Write-Host "✅ Backend is running and healthy" -ForegroundColor Green
        Write-Host "   Status: $($response.status)" -ForegroundColor Gray
        Write-Host "   Message: $($response.message)" -ForegroundColor Gray
    } else {
        Write-Host "⚠️  Backend responded but status is: $($response.status)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Backend is not running on port 5000" -ForegroundColor Red
    Write-Host "   Start it with: python app_minimal.py" -ForegroundColor Gray
}
Write-Host ""

# Test 2: Check if frontend is accessible
Write-Host "Test 2: Frontend Availability" -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5173" -TimeoutSec 2 -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Frontend is accessible" -ForegroundColor Green
        Write-Host "   URL: http://localhost:5173" -ForegroundColor Gray
    }
} catch {
    Write-Host "⚠️  Frontend is not running on port 5173" -ForegroundColor Yellow
    Write-Host "   Start it with: npm run dev (in frontend directory)" -ForegroundColor Gray
}
Write-Host ""

# Test 3: Test chat endpoint
Write-Host "Test 3: Chat API Functionality" -ForegroundColor Yellow
try {
    $body = @{
        message = "How do I deploy to AWS?"
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "http://localhost:5000/api/chat" `
        -Method POST `
        -ContentType "application/json" `
        -Body $body `
        -ErrorAction Stop
    
    if ($response.response) {
        Write-Host "✅ Chat API is working" -ForegroundColor Green
        Write-Host "   Response length: $($response.response.Length) characters" -ForegroundColor Gray
        Write-Host "   Mode: $($response.mode)" -ForegroundColor Gray
        Write-Host "   Sample: $($response.response.Substring(0, [Math]::Min(80, $response.response.Length)))..." -ForegroundColor Gray
    }
} catch {
    Write-Host "❌ Chat API test failed" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Gray
}
Write-Host ""

# Test 4: Check documentation index
Write-Host "Test 4: Documentation Index" -ForegroundColor Yellow
$indexPath = "d:\Infra-Chat\backend\docs_index.json"
if (Test-Path $indexPath) {
    $index = Get-Content $indexPath | ConvertFrom-Json
    Write-Host "✅ Documentation index exists" -ForegroundColor Green
    Write-Host "   Documents indexed: $($index.metadata.total_docs)" -ForegroundColor Gray
    Write-Host "   Index mode: $($index.metadata.mode)" -ForegroundColor Gray
} else {
    Write-Host "⚠️  Documentation index not found" -ForegroundColor Yellow
    Write-Host "   Run: python ingest_minimal.py" -ForegroundColor Gray
}
Write-Host ""

# Test 5: Check git repository
Write-Host "Test 5: Git Repository" -ForegroundColor Yellow
Push-Location "d:\Infra-Chat"
try {
    $commits = git log --oneline -5 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Git repository is initialized" -ForegroundColor Green
        Write-Host "   Recent commits:" -ForegroundColor Gray
        $commits | ForEach-Object { Write-Host "   $_" -ForegroundColor Gray }
    }
} catch {
    Write-Host "⚠️  Git repository check failed" -ForegroundColor Yellow
}
Pop-Location
Write-Host ""

# Test 6: Check environment configuration
Write-Host "Test 6: Environment Configuration" -ForegroundColor Yellow
$envPath = "d:\Infra-Chat\backend\.env"
if (Test-Path $envPath) {
    $envContent = Get-Content $envPath
    $hasGoogleKey = $envContent | Where-Object { $_ -match "GOOGLE_API_KEY=.+" }
    
    if ($hasGoogleKey) {
        Write-Host "✅ .env file exists with API key configured" -ForegroundColor Green
    } else {
        Write-Host "⚠️  .env file exists but GOOGLE_API_KEY might be empty" -ForegroundColor Yellow
        Write-Host "   Add your key from: https://makersuite.google.com/app/apikey" -ForegroundColor Gray
    }
} else {
    Write-Host "⚠️  .env file not found" -ForegroundColor Yellow
    Write-Host "   Copy from: .env.example" -ForegroundColor Gray
}
Write-Host ""

# Summary
Write-Host "=" * 60
Write-Host "🎯 Test Summary" -ForegroundColor Cyan
Write-Host ""
Write-Host "Ready to demo: Check that backend and frontend tests passed" -ForegroundColor White
Write-Host ""
Write-Host "To start your application:" -ForegroundColor White
Write-Host "  1. Backend:  cd d:\Infra-Chat\backend && python app_minimal.py" -ForegroundColor Gray
Write-Host "  2. Frontend: cd d:\Infra-Chat\frontend && npm run dev" -ForegroundColor Gray
Write-Host "  3. Visit:    http://localhost:5173" -ForegroundColor Gray
Write-Host ""
Write-Host "=" * 60
