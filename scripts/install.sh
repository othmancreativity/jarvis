#!/usr/bin/env bash
# Full dev install (Linux / WSL). Adjust for your distro.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "=== Jarvis — install (Phase 1) ==="

if command -v apt-get >/dev/null 2>&1; then
  sudo apt-get update
  sudo apt-get install -y python3-pip python3-venv python3-dev \
    portaudio19-dev ffmpeg redis-server build-essential \
    || true
else
  echo "Skipping apt packages (non-Debian). Install: python3, pip, portaudio, ffmpeg, redis manually."
fi

VENV="${VENV:-$ROOT/.venv}"
python3 -m venv "$VENV"
# shellcheck source=/dev/null
source "$VENV/bin/activate"

pip install --upgrade pip
pip install -r "$ROOT/requirements.txt"

if command -v playwright >/dev/null 2>&1; then
  playwright install chromium
else
  echo "Playwright CLI not on PATH; run: pip install playwright && playwright install chromium"
fi

if command -v ollama >/dev/null 2>&1; then
  echo "Pulling Ollama models (README)…"
  ollama pull qwen2.5:7b || true
  ollama pull qwen2.5-coder:7b || true
  ollama pull gemma3:4b || true
  ollama pull qwen3:8b || true
  ollama pull llava:7b || true
else
  echo "Ollama not found. Install from https://ollama.com then re-run model pulls."
fi

echo "Optional: Whisper / Piper / openWakeWord assets — see TASKS Phase 1.7.5–1.7.7"

if command -v systemctl >/dev/null 2>&1; then
  sudo systemctl enable redis-server 2>/dev/null || true
  sudo systemctl start redis-server 2>/dev/null || true
fi

echo "=== Done. Activate venv: source $VENV/bin/activate ==="
echo "Run CLI: python -m app.main --interface cli"
echo "Run Web: python -m app.main --interface web"
