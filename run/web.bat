@echo off
title Jarvis — Web
cd /d "%~dp0.."
echo Building Jarvis...
call npm run build
echo Starting Web + Telegram...
start http://localhost:3000
node dist/index.js --web
