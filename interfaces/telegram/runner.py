"""Telegram interface — Phase 1 stub."""

from __future__ import annotations

from typing import TYPE_CHECKING

from loguru import logger

if TYPE_CHECKING:
    from settings.app_settings import AppSettings


def run_telegram_stub(settings: "AppSettings") -> None:
    logger.info(
        "Telegram stub: set TELEGRAM_BOT_TOKEN in .env — full bot in Phase 10 "
        "(enabled={})",
        settings.interfaces.telegram.enabled,
    )


def run_telegram(settings: "AppSettings") -> None:
    """Block until Phase 10 implements python-telegram-bot polling."""
    run_telegram_stub(settings)
    logger.warning(
        "Telegram interface not implemented yet (Phase 10). Exiting. "
        "Configure TELEGRAM_BOT_TOKEN and revisit TASKS.md."
    )


__all__ = ["run_telegram", "run_telegram_stub"]
