$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

$venvCandidates = @(
    "$projectRoot\.venv\Scripts\python.exe",
    "$projectRoot\.venv-1\Scripts\python.exe"
)

$pythonExe = $null
foreach ($candidate in $venvCandidates) {
    if (Test-Path $candidate) {
        $pythonExe = $candidate
        break
    }
}

if (-not $pythonExe) {
    Write-Error "No Python virtual environment was found in the project root. Run scripts/setup.ps1 first."
    exit 1
}

Write-Host "[AIRIS] Starting backend API..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "Set-Location '$projectRoot'; & '$pythonExe' -m uvicorn src.api.app:app --host 127.0.0.1 --port 8000"
)

Write-Host "[AIRIS] Starting frontend dev server..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "Set-Location '$projectRoot\web'; npm run dev -- --host airis.local --port 5173"
)

Write-Host "[AIRIS] Web dashboard is starting..." -ForegroundColor Green
Write-Host "Backend: http://127.0.0.1:8000/api/health" -ForegroundColor Green
Write-Host "Frontend: http://airis.local:5173" -ForegroundColor Green
