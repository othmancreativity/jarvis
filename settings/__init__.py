"""
Application settings: YAML + env loading, paths, logging, and chat route metadata.

YAML files live under ``config/``; this package is Python-only (no nested ``jarvis/`` name).
"""

from __future__ import annotations

from settings.app_settings import (
    AppSettings,
    CliInterface,
    GuiInterface,
    HardwareBlock,
    InterfacesBlock,
    JarvisBlock,
    LoggingBlock,
    ModelsBlock,
    PathsBlock,
    TelegramInterface,
    WebInterface,
)
from settings.chat_types import Decision, RouteKind
from settings.loader import load_settings
from settings.logging import configure_logging, setup_logging
from settings.paths import PROJECT_ROOT, config_dir, data_dir, logs_dir

__all__ = [
    "AppSettings",
    "CliInterface",
    "Decision",
    "GuiInterface",
    "HardwareBlock",
    "InterfacesBlock",
    "JarvisBlock",
    "LoggingBlock",
    "ModelsBlock",
    "PathsBlock",
    "PROJECT_ROOT",
    "RouteKind",
    "TelegramInterface",
    "WebInterface",
    "configure_logging",
    "config_dir",
    "data_dir",
    "load_settings",
    "logs_dir",
    "setup_logging",
]
