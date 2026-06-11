"""
JARVIS 4.5 — Configuration Management
======================================
Unified config loading from: .env file, YAML config, environment variables.
Priority: env vars > .env file > config.yaml > defaults
"""

from __future__ import annotations

import os
import logging
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

logger = logging.getLogger("jarvis.config")

# ── Default Configuration ────────────────────────────────────────────────

DEFAULTS = {
    "bridge_port": 8765,
    "bridge_host": "0.0.0.0",
    "rate_limit_per_minute": 30,
    "log_level": "INFO",
    "jarvis_lang": "en",
    "jarvis_model": "llama-3.3-70b-versatile",
    "wake_word_enabled": False,
    "wake_word_model": "porcupine",
    "session_timeout": 300,
    "max_chat_context": 20,
    "max_iterations": 50,
    "max_errors": 5,
    "auto_save_session": True,
    "theme": "dark",
    "confirm_dangerous_actions": True,
    "emergency_stop_auto_threshold": 5,
}


@dataclass
class JarvisConfig:
    """Central configuration for JARVIS 4.5."""

    # API Keys
    groq_api_key: str = ""
    google_api_key: str = ""
    google_access_token: str = ""
    telegram_bot_token: str = ""
    owner_user_id: str = ""

    # Bridge
    bridge_secret: str = "change-me-in-production"
    bridge_port: int = 8765
    bridge_host: str = "0.0.0.0"

    # Model
    model: str = "llama-3.3-70b-versatile"

    # Rate limiting
    rate_limit_per_minute: int = 30

    # UI
    language: str = "en"
    theme: str = "dark"

    # Wake word
    wake_word_enabled: bool = False
    wake_word_model: str = "porcupine"

    # Runtime
    session_timeout: int = 300
    max_chat_context: int = 20
    max_iterations: int = 50
    max_errors: int = 5
    auto_save_session: bool = True
    confirm_dangerous_actions: bool = True
    emergency_stop_auto_threshold: int = 5

    # Paths
    log_dir: Path = field(default_factory=lambda: Path.home() / ".jarvis" / "logs")
    data_dir: Path = field(default_factory=lambda: Path.home() / ".jarvis" / "data")
    capture_dir: Path = field(default_factory=lambda: Path.home() / ".jarvis" / "captures")

    # Logging
    log_level: str = "INFO"

    def __post_init__(self):
        """Ensure directories exist."""
        for d in [self.log_dir, self.data_dir, self.capture_dir]:
            d.mkdir(parents=True, exist_ok=True)

    @classmethod
    def load(cls) -> "JarvisConfig":
        """
        Load configuration from all sources.
        Priority: env vars > .env file > config.yaml > defaults
        """
        # 1. Try to load .env file
        env_path = Path(__file__).parent.parent / ".env"
        if env_path.exists():
            try:
                from dotenv import load_dotenv
                load_dotenv(env_path)
            except ImportError:
                logger.debug("python-dotenv not installed, skipping .env file")

        # 2. Try to load config.yaml
        config = cls._load_yaml()

        # 3. Environment variables override everything
        config.groq_api_key = os.environ.get("GROQ_API_KEY", config.groq_api_key)
        config.google_api_key = os.environ.get("GOOGLE_API_KEY", config.google_api_key)
        config.google_access_token = os.environ.get("GOOGLE_ACCESS_TOKEN", config.google_access_token)
        config.telegram_bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", config.telegram_bot_token)
        config.owner_user_id = os.environ.get("OWNER_USER_ID", config.owner_user_id)
        config.bridge_secret = os.environ.get("JARVIS_BRIDGE_SECRET", config.bridge_secret)
        config.bridge_port = int(os.environ.get("BRIDGE_PORT", config.bridge_port))
        config.bridge_host = os.environ.get("BRIDGE_HOST", config.bridge_host)
        config.model = os.environ.get("JARVIS_MODEL", config.model)
        config.rate_limit_per_minute = int(os.environ.get("RATE_LIMIT_PER_MINUTE", config.rate_limit_per_minute))
        config.language = os.environ.get("JARVIS_LANG", config.language)
        config.wake_word_enabled = os.environ.get("WAKE_WORD_ENABLED", str(config.wake_word_enabled)).lower() == "true"
        config.log_level = os.environ.get("LOG_LEVEL", config.log_level)

        return config

    @classmethod
    def _load_yaml(cls) -> "JarvisConfig":
        """Load from config.yaml if it exists."""
        config_path = Path.home() / ".jarvis" / "config.yaml"
        if not config_path.exists():
            return cls()

        try:
            import yaml
            with open(config_path, "r") as f:
                data = yaml.safe_load(f) or {}
            return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
        except ImportError:
            logger.debug("PyYAML not installed, skipping config.yaml")
            return cls()
        except Exception as e:
            logger.warning(f"Failed to load config.yaml: {e}")
            return cls()

    def save_yaml(self) -> None:
        """Save current config to config.yaml."""
        config_path = Path.home() / ".jarvis" / "config.yaml"
        try:
            import yaml
            data = {
                k: str(v) if isinstance(v, Path) else v
                for k, v in self.__dict__.items()
            }
            with open(config_path, "w") as f:
                yaml.dump(data, f, default_flow_style=False)
        except ImportError:
            pass
        except Exception as e:
            logger.warning(f"Failed to save config.yaml: {e}")


# Global config instance
config = JarvisConfig.load()
