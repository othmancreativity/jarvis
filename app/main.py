"""
Jarvis entry point: ``--interface`` CLI, Web, Telegram, GUI, or ``all``.
"""

from __future__ import annotations

import argparse
import sys
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from loguru import logger

from settings.loader import load_settings
from settings.logging import setup_logging


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="jarvis",
        description="Jarvis — local AI assistant (Phase 1 foundation)",
    )
    p.add_argument(
        "--interface",
        "-i",
        choices=("cli", "web", "telegram", "gui", "all"),
        default="cli",
        help="Which interface to launch",
    )
    p.add_argument(
        "--config",
        type=Path,
        default=None,
        metavar="PATH",
        help="Path to settings.yaml (default: config/settings.yaml)",
    )
    return p.parse_args()


def _run_web(settings: object) -> None:
    import uvicorn

    host = settings.interfaces.web.host
    port = settings.interfaces.web.port
    logger.info("Starting Web UI at http://{}:{}", host, port)
    uvicorn.run(
        "interfaces.web.app:app",
        host=host,
        port=port,
        log_level="info",
    )


def _run_all(settings: object) -> None:
    """Run FastAPI in a background thread and interactive CLI in the foreground."""
    import uvicorn

    host = settings.interfaces.web.host
    port = settings.interfaces.web.port

    def _serve() -> None:
        uvicorn.run(
            "interfaces.web.app:app",
            host=host,
            port=port,
            log_level="warning",
        )

    thread = threading.Thread(target=_serve, daemon=True, name="jarvis-web")
    thread.start()
    logger.info("Web UI starting in background: http://{}:{}", host, port)
    logger.info("Telegram & GUI: Phase 1 stubs only (see TASKS Phase 10)")
    from interfaces.telegram.runner import run_telegram_stub
    from interfaces.gui.runner import run_gui_stub

    run_telegram_stub(settings)
    run_gui_stub(settings)

    from interfaces.cli.runner import run_cli

    run_cli(settings)


def main() -> None:
    args = _parse_args()
    settings = load_settings(config_path=args.config) if args.config else load_settings()
    setup_logging(level=settings.logging.level)

    logger.info("{} | interface={}", settings.jarvis.name, args.interface)

    if args.interface == "cli":
        from interfaces.cli.runner import run_cli

        run_cli(settings)
    elif args.interface == "web":
        _run_web(settings)
    elif args.interface == "telegram":
        from interfaces.telegram.runner import run_telegram

        run_telegram(settings)
    elif args.interface == "gui":
        from interfaces.gui.runner import run_gui

        run_gui(settings)
    else:
        _run_all(settings)


if __name__ == "__main__":
    main()
