# Infra-Chat Startup Script
# This script starts both backend and frontend

Write-Host "🚀 Starting Infra-Chat Application" -ForegroundColor Cyan
Write-Host "=" * 60
Write-Host ""

# Check if processes are already running
$backendRunning = Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue
$frontendRunning = Get-NetTCPConnection -LocalPort 5173 -ErrorAction SilentlyContinue

if ($backendRunning) {
    Write-Host "⚠️  Backend is already running on port 5000" -ForegroundColor Yellow
    Write-Host "   If you want to restart, press Ctrl+C in the backend terminal" -ForegroundColor Gray
    Write-Host ""
}

if ($frontendRunning) {
    Write-Host "⚠️  Frontend is already running on port 5173" -ForegroundColor Yellow
    Write-Host "   If you want to restart, press Ctrl+C in the frontend terminal" -ForegroundColor Gray
    Write-Host ""
}

# Instructions
Write-Host "📋 To start your application, you need 2 terminals:" -ForegroundColor White
Write-Host ""

Write-Host "Terminal 1 - Backend:" -ForegroundColor Yellow
Write-Host "  cd d:\Infra-Chat\backend" -ForegroundColor Gray
Write-Host "  python app_minimal.py" -ForegroundColor Green
Write-Host ""

Write-Host "Terminal 2 - Frontend:" -ForegroundColor Yellow
Write-Host "  cd d:\Infra-Chat\frontend" -ForegroundColor Gray
Write-Host "  npm run dev" -ForegroundColor Green
Write-Host ""

Write-Host "=" * 60
Write-Host ""

# Offer to start backend in this terminal
$response = Read-Host "Would you like to start the BACKEND in this terminal? (Y/N)"

if ($response -eq "Y" -or $response -eq "y") {
    Write-Host ""
    Write-Host "✅ Starting backend..." -ForegroundColor Green
    Write-Host "   (Open a NEW terminal for frontend)" -ForegroundColor Yellow
    Write-Host ""
    
    Set-Location "d:\Infra-Chat\backend"
    
    # Check if virtual environment exists and activate it
    if (Test-Path "venv\Scripts\Activate.ps1") {
        Write-Host "Activating virtual environment..." -ForegroundColor Gray
        & venv\Scripts\Activate.ps1
    }
    
    # Start the backend
    python app_minimal.py
} else {
    Write-Host ""
    Write-Host "💡 Quick Start Commands:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "# Terminal 1 (Backend)" -ForegroundColor Yellow
    Write-Host 'cd d:\Infra-Chat\backend; python app_minimal.py' -ForegroundColor Green
    Write-Host ""
    Write-Host "# Terminal 2 (Frontend)" -ForegroundColor Yellow
    Write-Host 'cd d:\Infra-Chat\frontend; npm run dev' -ForegroundColor Green
    Write-Host ""
    Write-Host "# Then visit: http://localhost:5173" -ForegroundColor Cyan
    Write-Host ""
}
