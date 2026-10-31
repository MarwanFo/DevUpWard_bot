# PowerShell Development Launcher for DevUpward
Write-Host "🚀 Launching DevUpward Full Stack (FastAPI + Bot + React)..." -ForegroundColor Cyan

# Check if .env exists
if (-not (Test-Path .env)) {
    Write-Host "⚠️ .env not found. Copying .env.example to .env..." -ForegroundColor Yellow
    Copy-Item .env.example .env
}

# Start Backend in new process
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Write-Host '🐍 Starting Backend...'; & .\backend\venv\Scripts\Activate.ps1; python backend\app\main.py"

# Start Frontend in current process
Write-Host "⚛️ Starting Frontend Vite Dev Server..." -ForegroundColor Green
Set-Location frontend
npm run dev

