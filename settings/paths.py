"""Project root and filesystem helpers."""

from __future__ import annotations

from pathlib import Path

# Repository root (parent of this package directory)
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent


def config_dir() -> Path:
    return PROJECT_ROOT / "config"


def data_dir() -> Path:
    return PROJECT_ROOT / "data"


def logs_dir() -> Path:
    return PROJECT_ROOT / "logs"
