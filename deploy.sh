#!/bin/bash
# Jarvis — Oracle Cloud VPS deployment helper
# Run from inside the project folder (where package.json and paths.json live).

set -e

echo "========================================"
echo "  Jarvis — Deployment Script"
echo "========================================"

# 1. System updates
echo "[1/7] Updating system..."
sudo apt-get update && sudo apt-get upgrade -y

# 2. Install Node.js 20
echo "[2/7] Installing Node.js 20..."
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
echo "Node.js $(node -v) installed"

# 3. Install build tools for native modules (better-sqlite3)
echo "[3/7] Installing build tools..."
sudo apt-get install -y python3 make g++ git

# 4. Install PM2
echo "[4/7] Installing PM2..."
sudo npm install -g pm2

# 5. Verify project root
echo "[5/7] Verifying project..."
if [ ! -f "package.json" ] || [ ! -f "paths.json" ]; then
  echo "Run this script from the Jarvis project root (where package.json and paths.json are)."
  echo "Example: cd ~/jarvis && bash deploy.sh"
  exit 1
fi

# 6. Install dependencies and build
echo "[6/7] Installing dependencies and building..."
npm ci
npm run build

# 7. Start with PM2
echo "[7/7] Starting Jarvis..."
pm2 delete jarvis 2>/dev/null || true
pm2 start ecosystem.config.cjs
pm2 save

# Setup PM2 to start on boot
sudo env PATH=$PATH:/usr/bin pm2 startup systemd -u $USER --hp $HOME
pm2 save

echo ""
echo "========================================"
echo "  Jarvis is deployed and running!"
echo "========================================"
echo ""
echo "Useful commands:"
echo "  pm2 status          — Check if running"
echo "  pm2 logs jarvis   — View logs"
echo "  pm2 restart jarvis — Restart"
echo "  pm2 stop jarvis   — Stop"
echo ""
echo "Don't forget: .env, tokens/*.json, paths.json / more_paths.json"
echo "========================================"
