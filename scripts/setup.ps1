$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

Write-Host "[AIRIS] Checking Python..." -ForegroundColor Cyan
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Write-Error "Python was not found in PATH. Please install Python 3.11+ and try again."
    exit 1
}

Write-Host "[AIRIS] Creating virtual environment..." -ForegroundColor Cyan
if (-not (Test-Path ".venv")) {
    python -m venv .venv
}

Write-Host "[AIRIS] Activating virtual environment..." -ForegroundColor Cyan
. ".\.venv\Scripts\Activate.ps1"

Write-Host "[AIRIS] Upgrading pip..." -ForegroundColor Cyan
python -m pip install --upgrade pip

Write-Host "[AIRIS] Installing requirements..." -ForegroundColor Cyan
pip install -r requirements.txt

Write-Host "[AIRIS] Creating folders..." -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path "data/input", "data/snapshots", "data/database", "models" | Out-Null

Write-Host "[AIRIS] Verifying core imports..." -ForegroundColor Cyan
$imports = @("cv2", "numpy", "torch", "ultralytics", "pytest")
$failed = @()
foreach ($name in $imports) {
    try {
        python -c "import $name; print('$name OK')"
    }
    catch {
        $failed += $name
    }
}

if ($failed.Count -gt 0) {
    Write-Error "[AIRIS] Failed imports: $($failed -join ', ')"
    exit 1
}

Write-Host "[AIRIS] Setup completed successfully." -ForegroundColor Green
