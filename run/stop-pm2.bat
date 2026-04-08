@echo off
title Jarvis — Stop PM2
cd /d "%~dp0.."
echo Stopping PM2 app "jarvis" (if running)...
pm2 stop jarvis 2>nul
if %ERRORLEVEL% equ 0 (
  echo OK — jarvis stopped. You can run dev.bat or npm run dev now.
) else (
  echo No running PM2 app named jarvis, or PM2 not installed.
)
pause
