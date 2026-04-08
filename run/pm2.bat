@echo off
title Jarvis — PM2
cd /d "%~dp0.."
echo Building Jarvis...
call npm run build
echo Starting with PM2...
pm2 start ecosystem.config.cjs
pm2 save
echo Jarvis is running in the background. You can close this window.
pause
