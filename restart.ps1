# Truth in Listings - Restart Script
# This script restarts both frontend and backend servers

Write-Host "🔄 Restarting Truth in Listings..." -ForegroundColor Cyan
Write-Host ""

# Function to kill processes on a specific port
function Kill-ProcessOnPort {
    param($Port)
    $processes = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique
    if ($processes) {
        foreach ($proc in $processes) {
            Write-Host "Stopping process on port $Port (PID: $proc)..." -ForegroundColor Yellow
            Stop-Process -Id $proc -Force -ErrorAction SilentlyContinue
        }
    }
}

# Kill existing processes
Write-Host "Stopping existing servers..." -ForegroundColor Yellow
Kill-ProcessOnPort 8000  # Backend
Kill-ProcessOnPort 5173  # Frontend

Start-Sleep -Seconds 2

# Start Backend
Write-Host ""
Write-Host "🚀 Starting Backend Server..." -ForegroundColor Green
$backendPath = Join-Path $PSScriptRoot "backend"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backendPath'; .\venv\Scripts\activate; uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

Start-Sleep -Seconds 3

# Start Frontend
Write-Host "🚀 Starting Frontend Server..." -ForegroundColor Green
$frontendPath = Join-Path $PSScriptRoot "frontend"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$frontendPath'; npm run dev"

Start-Sleep -Seconds 2

Write-Host ""
Write-Host "✅ Servers are starting..." -ForegroundColor Green
Write-Host ""
Write-Host "📡 URLs:" -ForegroundColor Cyan
Write-Host "   Frontend: http://localhost:5173" -ForegroundColor White
Write-Host "   Backend:  http://localhost:8000" -ForegroundColor White
Write-Host "   API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
