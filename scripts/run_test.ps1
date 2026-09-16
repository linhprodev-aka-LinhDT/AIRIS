$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

if (-not (Test-Path ".venv")) {
    Write-Error "Virtual environment not found. Run scripts/setup.ps1 first."
    exit 1
}

. ".\.venv\Scripts\Activate.ps1"
pytest -q
