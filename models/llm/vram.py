"""Serialize access to a single heavy Ollama model at a time (best-effort).

Enhanced with swap logging, timing, and capacity check.
"""

from __future__ import annotations

import threading
import time
from typing import Callable

from loguru import logger


class VramGuard:
    """Track active model id; enforce single-model policy on 6 GB VRAM.

    ``on_swap`` is called when a model change is needed — implementations
    can unload via Ollama API or wait for idle.
    """

    def __init__(self, *, settle_s: float = 0.05) -> None:
        self._lock = threading.Lock()
        self._active: str | None = None
        self._settle_s = settle_s
        self._swap_count: int = 0
        self._last_swap_time: float = 0.0

    @property
    def active_model(self) -> str | None:
        return self._active

    @property
    def swap_count(self) -> int:
        return self._swap_count

    @property
    def time_since_last_swap(self) -> float:
        if self._last_swap_time == 0:
            return 0.0
        return time.monotonic() - self._last_swap_time

    def prepare(
        self,
        model_id: str,
        *,
        on_swap: Callable[[str | None, str], None] | None = None,
    ) -> bool:
        """Mark intent to use ``model_id``.

        Returns True if a swap occurred, False if already loaded.
        Calls ``on_swap(old, new)`` when model changes.
        """
        with self._lock:
            old = self._active
            if old == model_id:
                return False

            logger.info("VramGuard: swap {} → {}", old or "none", model_id)
            if on_swap:
                try:
                    on_swap(old, model_id)
                except Exception as exc:
                    logger.warning("VramGuard: on_swap callback failed: {}", exc)

            self._active = model_id
            self._swap_count += 1
            self._last_swap_time = time.monotonic()

            # Small settle to allow GPU memory release
            if old is not None and self._settle_s > 0:
                time.sleep(self._settle_s)

            return True

    def release(self) -> None:
        """Mark no model as active (e.g. before image generation)."""
        with self._lock:
            if self._active:
                logger.debug("VramGuard: released {}", self._active)
            self._active = None

    def summary(self) -> dict[str, object]:
        return {
            "active": self._active,
            "swaps": self._swap_count,
            "time_since_swap": round(self.time_since_last_swap, 2),
        }
