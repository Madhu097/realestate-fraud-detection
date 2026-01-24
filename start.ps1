# Truth in Listings - Quick Start Script
# This script helps you start both backend and frontend servers

Write-Host "================================" -ForegroundColor Cyan
Write-Host "  Truth in Listings - Startup  " -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Function to check if a command exists
function Test-Command($command) {
    try {
        if (Get-Command $command -ErrorAction Stop) {
            return $true
        }
    }
    catch {
        return $false
    }
}

# Check Python
Write-Host "Checking Python..." -ForegroundColor Yellow
if (Test-Command python) {
    $pythonVersion = python --version
    Write-Host "✅ $pythonVersion found" -ForegroundColor Green
} else {
    Write-Host "❌ Python not found. Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Check Node.js
Write-Host "Checking Node.js..." -ForegroundColor Yellow
if (Test-Command node) {
    $nodeVersion = node --version
    Write-Host "✅ Node.js $nodeVersion found" -ForegroundColor Green
} else {
    Write-Host "⚠️  Node.js not found. Install it to run the frontend." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "  Choose an option:             " -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host "1. Start Backend Only" -ForegroundColor White
Write-Host "2. Start Frontend Only" -ForegroundColor White
Write-Host "3. Start Both (Recommended)" -ForegroundColor White
Write-Host "4. Run Backend Tests" -ForegroundColor White
Write-Host "5. Exit" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Enter your choice (1-5)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "Starting Backend Server..." -ForegroundColor Green
        Write-Host "Navigate to: http://localhost:8000" -ForegroundColor Cyan
        Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
        Write-Host ""
        Set-Location backend
        .\venv\Scripts\activate
        uvicorn app.main:app --reload
    }
    "2" {
        Write-Host ""
        Write-Host "Starting Frontend Server..." -ForegroundColor Green
        Write-Host "Make sure you've initialized the frontend first!" -ForegroundColor Yellow
        Write-Host ""
        Set-Location frontend
        if (Test-Path "package.json") {
            npm run dev
        } else {
            Write-Host "❌ Frontend not initialized yet!" -ForegroundColor Red
            Write-Host "Run: cd frontend && npm create vite@latest . -- --template react" -ForegroundColor Yellow
        }
    }
    "3" {
        Write-Host ""
        Write-Host "Starting Both Servers..." -ForegroundColor Green
        Write-Host "Backend: http://localhost:8000" -ForegroundColor Cyan
        Write-Host "Frontend: http://localhost:5173" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Opening Backend in new window..." -ForegroundColor Yellow
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\backend'; .\venv\Scripts\activate; uvicorn app.main:app --reload"
        
        Start-Sleep -Seconds 2
        
        if (Test-Path "frontend\package.json") {
            Write-Host "Opening Frontend in new window..." -ForegroundColor Yellow
            Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\frontend'; npm run dev"
        } else {
            Write-Host "⚠️  Frontend not initialized. Skipping..." -ForegroundColor Yellow
        }
    }
    "4" {
        Write-Host ""
        Write-Host "Running Backend Tests..." -ForegroundColor Green
        Write-Host ""
        Set-Location backend
        .\venv\Scripts\activate
        python test_api.py
        Write-Host ""
        Write-Host "Tests completed!" -ForegroundColor Green
        Read-Host "Press Enter to exit"
    }
    "5" {
        Write-Host "Goodbye! 👋" -ForegroundColor Cyan
        exit 0
    }
    default {
        Write-Host "Invalid choice. Exiting..." -ForegroundColor Red
        exit 1
    }
}
