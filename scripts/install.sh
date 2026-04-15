#!/bin/bash
echo "=== Installing Jarvis ==="
# System deps
sudo apt update && sudo apt install -y python3-pip python3-venv \
    portaudio19-dev ffmpeg redis-server

# Python env
python3 -m venv jarvis_env
source jarvis_env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Playwright
playwright install chromium

# Ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen3:8b &
ollama pull llama3.1:8b &
wait

# Start Redis
sudo systemctl enable redis-server
sudo systemctl start redis-server

echo "=== Jarvis installation complete! ==="
echo "Run: python main.py"