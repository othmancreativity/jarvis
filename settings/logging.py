"""Loguru setup (single place for all entry points)."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from loguru import logger

from settings.paths import logs_dir


def setup_logging(
    *,
    level: str = "INFO",
    log_file: Path | None = None,
    rotation: str = "10 MB",
) -> None:
    """Configure Loguru: console + optional rotating file under ``logs/``."""
    logger.remove()
    logger.add(
        sys.stderr,
        level=level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    )
    path = log_file or (logs_dir() / "jarvis.log")
    path.parent.mkdir(parents=True, exist_ok=True)
    logger.add(
        path,
        level=level,
        rotation=rotation,
        retention="7 days",
        encoding="utf-8",
    )


def configure_logging(**kwargs: Any) -> None:
    """Alias used by some modules; forwards to :func:`setup_logging`."""
    setup_logging(**kwargs)
