# PowerShell script to run ShramAI backend and frontend
Write-Host "Starting ShramAI Development Services..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; if (Test-Path .venv) { .\.venv\Scripts\Activate.ps1 }; uvicorn app.main:app --reload --port 8000"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"
Write-Host "Backend launching at http://127.0.0.1:8000" -ForegroundColor Green
Write-Host "Frontend launching at http://localhost:5173" -ForegroundColor Green
