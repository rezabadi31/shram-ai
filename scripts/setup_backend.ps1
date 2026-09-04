# PowerShell script to set up Python virtual environment and install dependencies
$ErrorActionPreference = "Stop"

Write-Host "=== Setting up ShramAI Backend Environment ===" -ForegroundColor Cyan
cd backend
if (-Not (Test-Path ".venv")) {
    Write-Host "Creating Python virtual environment..."
    python -m venv .venv
}
Write-Host "Activating virtual environment..."
.\.venv\Scripts\Activate.ps1
Write-Host "Upgrading pip and installing requirements..."
pip install --upgrade pip
pip install -r requirements.txt
Write-Host "Backend environment ready!" -ForegroundColor Green
cd ..
