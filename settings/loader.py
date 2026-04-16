"""Load ``config/settings.yaml`` + optional ``.env`` and validate with Pydantic."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

from settings.app_settings import AppSettings
from settings.paths import PROJECT_ROOT, config_dir


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"Config file not found: {path}")
    with path.open(encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    if raw is None:
        return {}
    if not isinstance(raw, dict):
        raise ValueError(f"Config root must be a mapping: {path}")
    return raw


def load_settings(
    *,
    config_path: Path | None = None,
    env_path: Path | None = None,
) -> AppSettings:
    """
    Load settings from ``config/settings.yaml`` (or ``config_path``).

    Loads ``.env`` from project root when present (does not override existing OS env).
    """
    load_dotenv(dotenv_path=env_path or (PROJECT_ROOT / ".env"), override=False)

    path = config_path or (config_dir() / "settings.yaml")
    data = _load_yaml(path)
    settings = AppSettings.model_validate(data)

    if port := os.getenv("JARVIS_WEB_PORT"):
        settings.interfaces.web.port = int(port)
    if host := os.getenv("JARVIS_WEB_HOST"):
        settings.interfaces.web.host = host
    if level := os.getenv("JARVIS_LOG_LEVEL"):
        settings.logging.level = level

    return settings
