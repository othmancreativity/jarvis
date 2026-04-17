# Jarvis — Windows install script (PowerShell)
# Run: powershell -ExecutionPolicy Bypass -File scripts\install.ps1

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ROOT = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $ROOT

Write-Host "=== Jarvis — Windows Install (Phase 1) ===" -ForegroundColor Cyan

# --- Ollama ---
if (Get-Command ollama -ErrorAction SilentlyContinue) {
    Write-Host "[OK] Ollama found" -ForegroundColor Green
} else {
    Write-Host "[INSTALL] Installing Ollama via winget..." -ForegroundColor Yellow
    winget install Ollama.Ollama --accept-source-agreements --accept-package-agreements
}

# --- Python venv ---
$VENV = if ($env:VENV) { $env:VENV } else { Join-Path $ROOT ".venv" }

if (-Not (Test-Path $VENV)) {
    Write-Host "[SETUP] Creating Python virtual environment at $VENV" -ForegroundColor Yellow
    python -m venv $VENV
}

$activateScript = Join-Path $VENV "Scripts\Activate.ps1"
if (Test-Path $activateScript) {
    & $activateScript
} else {
    Write-Host "[WARN] Could not activate venv; proceeding with system Python" -ForegroundColor Red
}

Write-Host "[PIP] Upgrading pip..."
python -m pip install --upgrade pip

Write-Host "[PIP] Installing requirements..."
python -m pip install -r (Join-Path $ROOT "requirements.txt")

# --- Playwright ---
if (Get-Command playwright -ErrorAction SilentlyContinue) {
    Write-Host "[PLAYWRIGHT] Installing Chromium browser..."
    playwright install chromium
} else {
    Write-Host "[INFO] Playwright CLI not on PATH; run: pip install playwright && playwright install chromium" -ForegroundColor Yellow
}

# --- Ollama model pulls ---
if (Get-Command ollama -ErrorAction SilentlyContinue) {
    Write-Host "[OLLAMA] Pulling models..." -ForegroundColor Yellow
    $models = @("qwen2.5:7b", "qwen2.5-coder:7b", "gemma3:4b", "qwen3:8b", "llava:7b")
    foreach ($model in $models) {
        Write-Host "  Pulling $model..."
        ollama pull $model 2>$null
    }
} else {
    Write-Host "[SKIP] Ollama not found. Install from https://ollama.com then re-run model pulls." -ForegroundColor Yellow
}

# --- Data directories ---
$dataDir = Join-Path $ROOT "data"
$logsDir = Join-Path $ROOT "logs"
if (-Not (Test-Path $dataDir)) { New-Item -ItemType Directory -Path $dataDir | Out-Null }
if (-Not (Test-Path $logsDir)) { New-Item -ItemType Directory -Path $logsDir | Out-Null }

Write-Host ""
Write-Host "=== Done ===" -ForegroundColor Green
Write-Host "Activate venv:  $activateScript"
Write-Host "Run CLI:        python app\main.py --interface cli"
Write-Host "Run Web:        python app\main.py --interface web"
