@echo off
title JARVIS Launch System
setlocal enabledelayedexpansion

:: ─── JARVIS Zero-Touch Bootloader ──────────────────────────────────────────
:: This script starts n8n, waits for it to be ready, and launches the
:: JARVIS Desktop GUI client. Handles cleanup on exit.
:: ────────────────────────────────────────────────────────────────────────────

:: ── Configuration ──────────────────────────────────────────────────────────
set "N8N_PORT=5678"
set "N8N_START_TIMEOUT=30"
set "PYTHON=python"
set "SCRIPT_DIR=%~dp0"
set "JARVIS_SCRIPT=%SCRIPT_DIR%jarvis_client.py"

:: ── Banner ─────────────────────────────────────────────────────────────────
cls
echo.
echo     ╔══════════════════════════════════════════╗
echo     ║          JARVIS Launch System             ║
echo     ║       Neural Interface Bootloader v1.0    ║
echo     ╚══════════════════════════════════════════╝
echo.

:: ── Dependency Check ───────────────────────────────────────────────────────
echo [CHECK] Verifying dependencies...

where "%PYTHON%" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found in PATH. Please install Python 3.10+.
    pause
    exit /b 1
)
echo [OK] Python found.

where n8n >nul 2>&1
if errorlevel 1 (
    echo [WARN] n8n not found in PATH globally.
    echo [INFO] Checking for n8n in common locations...

    :: Common n8n installation paths
    set "N8N_FOUND="
    for %%p in (
        "%APPDATA%\npm\n8n"
        "%LOCALAPPDATA%\npm\n8n"
        "%ProgramFiles%\nodejs\n8n"
        "C:\Users\%USERNAME%\AppData\Roaming\npm\n8n"
    ) do (
        if exist "%%p" (
            set "N8N_PATH=%%p"
            set "N8N_FOUND=1"
        )
    )

    if not defined N8N_FOUND (
        echo [INFO] n8n not found. The system will try to start it via 'npx n8n'.
        echo [INFO] Alternatively, start n8n manually before running this script.
        set "N8N_CMD=npx n8n"
    ) else (
        echo [OK] n8n found at !N8N_PATH!
        set "N8N_CMD=!N8N_PATH!"
    )
) else (
    set "N8N_CMD=n8n"
)

:: Check Python packages
echo [CHECK] Verifying Python packages...
"%PYTHON%" -c "import customtkinter, sounddevice, faster_whisper, edge_tts, aiohttp, av, numpy" 2>nul
if errorlevel 1 (
    echo [INFO] Installing required Python packages...
    pip install customtkinter sounddevice faster-whisper edge-tts aiohttp av numpy
    if errorlevel 1 (
        echo [ERROR] Failed to install Python dependencies.
        pause
        exit /b 1
    )
)
echo [OK] Python packages verified.

:: ── Start n8n ──────────────────────────────────────────────────────────────
echo.
echo [N8N] Starting n8n automation engine...

:: Kill any existing n8n process on our port
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :%N8N_PORT% ^| findstr LISTENING 2^>nul') do (
    echo [N8N] Port %N8N_PORT% is in use by PID %%a. Attempting graceful restart...
    taskkill /PID %%a /F 2>nul
    timeout /t 2 /nobreak >nul
)

:: Start n8n in a minimized window
start "n8n-server" /MIN cmd /c "!N8N_CMD! start 2>&1"

echo [N8N] Waiting for n8n to become available on port %N8N_PORT%...
set "WAIT_COUNT=0"
:N8N_WAIT
timeout /t 1 /nobreak >nul
set /a WAIT_COUNT+=1

netstat -ano | findstr ":%N8N_PORT% " | findstr LISTENING >nul 2>&1
if errorlevel 1 (
    if !WAIT_COUNT! geq %N8N_START_TIMEOUT% (
        echo [WARN] n8n did not start within %N8N_START_TIMEOUT% seconds.
        echo [WARN] Continuing anyway - JARVIS will show n8n as OFFLINE.
        goto :N8N_CHECK_DONE
    )
    goto :N8N_WAIT
)
echo [OK] n8n is running on port %N8N_PORT%.
:N8N_CHECK_DONE

:: ── Launch JARVIS GUI ──────────────────────────────────────────────────────
echo.
echo [JARVIS] Launching Desktop Client...
echo.

:: Set environment variables for the Python client
set "N8N_WEBHOOK_URL=http://localhost:%N8N_PORT%/webhook/jarvis"

:: Launch the Python GUI
start "JARVIS" /B "%PYTHON%" "%JARVIS_SCRIPT%"

:: Store the PID of the Python process
set "JARVIS_PID=%ERRORLEVEL%"

echo [JARVIS] Client launched. Close the GUI window to shut down.
echo [JARVIS] To manually stop, press Ctrl+C in this window.
echo.

:: ── Wait for JARVIS to close ──────────────────────────────────────────────
:: Monitor the Python process; when it exits, clean up n8n
:MONITOR_LOOP
timeout /t 3 /nobreak >nul

:: Check if python is still running our script
tasklist /FI "IMAGENAME eq python.exe" 2>nul | findstr /I python >nul 2>&1
if errorlevel 1 (
    echo.
    echo [JARVIS] Client process ended.
    goto :CLEANUP
)

:: Also check if the window was closed by checking the process
:: Using a simpler approach: just wait for user to press a key
:: Actually, let's do a cleaner approach - check for the Python window
goto :MONITOR_LOOP

:MANUAL_STOP
echo.
echo [JARVIS] Shutdown requested.

:CLEANUP
echo [JARVIS] Cleaning up...
:: Ask if user wants to stop n8n
echo [N8N] Do you want to stop the n8n server? (Y/N)
echo [N8N] Default: N (keep running for future use)
choice /C YN /N /T 5 /D N >nul
if errorlevel 2 goto :SKIP_N8N_STOP

:: Stop n8n
echo [N8N] Stopping n8n...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :%N8N_PORT% ^| findstr LISTENING 2^>nul') do (
    taskkill /PID %%a /F 2>nul
)
echo [OK] n8n stopped.

:SKIP_N8N_STOP
echo.
echo [JARVIS] System shutdown complete.
echo.
timeout /t 2 /nobreak >nul
exit /b 0
