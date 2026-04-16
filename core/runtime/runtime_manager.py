"""Owns a single turn: iterations, timeouts, hooks to router VRAM policy."""

from __future__ import annotations

import time
from typing import TYPE_CHECKING, Callable

from core.runtime.limits import RunLimits
from core.runtime.state.session import SessionState
from loguru import logger

if TYPE_CHECKING:
    from settings.app_settings import AppSettings


class RuntimeManager:
    """Start/end run; enforce ``RunLimits`` for inner loops."""

    def __init__(
        self,
        *,
        settings: AppSettings,
        limits: RunLimits,
        on_step: Callable[[str, object], None] | None = None,
    ) -> None:
        self._settings = settings
        self._limits = limits
        self._on_step = on_step

    @property
    def limits(self) -> RunLimits:
        return self._limits

    def begin_turn(self, state: SessionState) -> None:
        state.run.step_index = 0
        logger.debug("begin_turn snapshot={}", state.snapshot())

    def can_continue(self, state: SessionState) -> bool:
        return state.run.step_index < self._limits.max_iterations

    def record_step(self, state: SessionState, label: str, payload: object = None) -> None:
        state.run.step_index += 1
        if self._on_step:
            self._on_step(label, payload)
        logger.trace("step {} {}", label, state.run.step_index)

    def with_step_timeout(self, fn: Callable[[], None], timeout_s: float | None = None) -> None:
        """Phase 2: synchronous placeholder; Phase 12 can wrap async with ``wait_for``."""
        t = timeout_s or self._limits.step_timeout_s
        start = time.monotonic()
        fn()
        if time.monotonic() - start > t:
            logger.warning("Step exceeded soft timeout {:.1f}s", t)
