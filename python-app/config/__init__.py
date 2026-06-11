from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from jarvis.cross_platform_paths import paths

logger = logging.getLogger("jarvis.config")


@dataclass
class JarvisConfig:
    groq_api_key: str = ""
    google_api_key: str = ""
    google_access_token: str = ""
    telegram_bot_token: str = ""
    bridge_secret: str = "change-me-in-production"
    bridge_port: int = 8765
    bridge_host: str = "0.0.0.0"
    model: str = "llama-3.3-70b-versatile"
    language: str = "en"
    log_level: str = "INFO"
    session_timeout: int = 300
    max_chat_context: int = 20
    max_iterations: int = 50
    max_errors: int = 5
    confirm_dangerous_actions: bool = True
    log_dir: Path = field(default_factory=lambda: paths.log_dir)
    data_dir: Path = field(default_factory=lambda: paths.data_dir)
    capture_dir: Path = field(default_factory=lambda: paths.data_dir / "captures")

    def __post_init__(self) -> None:
        for d in [self.log_dir, self.data_dir, self.capture_dir]:
            d.mkdir(parents=True, exist_ok=True)

    @classmethod
    def load(cls) -> "JarvisConfig":
        env_path = Path(__file__).parent.parent / ".env"
        if env_path.exists():
            try:
                from dotenv import load_dotenv
                load_dotenv(env_path)
            except ImportError:
                pass

        config = cls()

        config.groq_api_key = os.environ.get("GROQ_API_KEY", config.groq_api_key)
        config.google_api_key = os.environ.get("GOOGLE_API_KEY", config.google_api_key)
        config.bridge_secret = os.environ.get("JARVIS_BRIDGE_SECRET", config.bridge_secret)
        config.bridge_port = int(os.environ.get("BRIDGE_PORT", config.bridge_port))
        config.language = os.environ.get("JARVIS_LANG", config.language)
        config.model = os.environ.get("JARVIS_MODEL", config.model)
        config.log_level = os.environ.get("LOG_LEVEL", config.log_level)

        return config


config = JarvisConfig.load()
