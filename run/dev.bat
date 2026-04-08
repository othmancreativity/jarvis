@echo off
title Jarvis — Dev
cd /d "%~dp0.."
echo Starting Jarvis (dev, Telegram)...
npx tsx src/index.ts
