"""Desktop GUI — Phase 1 stub."""

from __future__ import annotations

from typing import TYPE_CHECKING

from loguru import logger

if TYPE_CHECKING:
    from settings.app_settings import AppSettings


def run_gui_stub(settings: "AppSettings") -> None:
    logger.info(
        "GUI stub: toolkit={} — full window in Phase 10",
        settings.interfaces.gui.toolkit,
    )


def run_gui(settings: "AppSettings") -> None:
    run_gui_stub(settings)
    logger.warning("GUI interface not implemented yet (Phase 10). Exiting.")


__all__ = ["run_gui", "run_gui_stub"]
