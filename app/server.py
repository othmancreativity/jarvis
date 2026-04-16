"""HTTP server entry (``python -m app.server``) — same as ``--interface web``."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.main import _run_web
from settings.loader import load_settings
from settings.logging import setup_logging


def main() -> None:
    settings = load_settings()
    setup_logging(level=settings.logging.level)
    _run_web(settings)


if __name__ == "__main__":
    main()
