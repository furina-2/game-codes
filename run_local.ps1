$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "=== Game Codes - Local Dev ===" -ForegroundColor Cyan
Write-Host "[1/1] Starting server..." -ForegroundColor Green
python run.py
