"""Owns a single turn: iterations, timeouts, hooks to router VRAM policy.

Enhanced with timing metrics, step history, and diagnostic exports.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Callable

from core.runtime.limits import RunLimits
from core.runtime.state.session import SessionState
from loguru import logger

if TYPE_CHECKING:
    from settings.app_settings import AppSettings


@dataclass
class StepRecord:
    """Log entry for a single runtime step."""

    label: str
    step_index: int
    timestamp: float = field(default_factory=time.monotonic)
    payload: Any = None
    elapsed_s: float = 0.0


class RuntimeManager:
    """Start/end run; enforce ``RunLimits`` for inner loops.

    Tracks per-step timing and maintains a step history
    for diagnostics and observability.
    """

    def __init__(
        self,
        *,
        settings: "AppSettings",
        limits: RunLimits,
        on_step: Callable[[str, object], None] | None = None,
    ) -> None:
        self._settings = settings
        self._limits = limits
        self._on_step = on_step
        self._step_history: list[StepRecord] = []
        self._turn_start: float = 0.0

    @property
    def limits(self) -> RunLimits:
        return self._limits

    @property
    def step_history(self) -> list[StepRecord]:
        return list(self._step_history)

    @property
    def turn_elapsed_s(self) -> float:
        if self._turn_start == 0:
            return 0.0
        return time.monotonic() - self._turn_start

    def begin_turn(self, state: SessionState) -> None:
        """Initialize a new turn — reset counters and start timing."""
        state.run.step_index = 0
        self._step_history.clear()
        self._turn_start = time.monotonic()
        logger.debug("begin_turn session={} snapshot={}", state.session_id, state.snapshot())

    def can_continue(self, state: SessionState) -> bool:
        """Check whether more iterations are allowed."""
        if state.run.step_index >= self._limits.max_iterations:
            logger.warning("RuntimeManager: hit max_iterations={}", self._limits.max_iterations)
            return False

        # Global turn timeout
        if self.turn_elapsed_s > self._limits.step_timeout_s * self._limits.max_iterations:
            logger.warning("RuntimeManager: global turn timeout exceeded ({:.1f}s)", self.turn_elapsed_s)
            return False

        return True

    def record_step(self, state: SessionState, label: str, payload: object = None) -> None:
        """Record a runtime step with timing."""
        state.run.step_index += 1
        record = StepRecord(
            label=label,
            step_index=state.run.step_index,
            payload=payload,
        )
        self._step_history.append(record)

        if self._on_step:
            self._on_step(label, payload)

        logger.trace("step {} {} (turn elapsed: {:.2f}s)", label, state.run.step_index, self.turn_elapsed_s)

    def with_step_timeout(self, fn: Callable[[], None], timeout_s: float | None = None) -> bool:
        """Run *fn* with a soft timeout check. Returns True if within limits."""
        t = timeout_s or self._limits.step_timeout_s
        start = time.monotonic()
        fn()
        elapsed = time.monotonic() - start

        if elapsed > t:
            logger.warning("Step exceeded soft timeout {:.1f}s (actual: {:.1f}s)", t, elapsed)
            return False
        return True

    def diagnostics(self) -> dict[str, Any]:
        """Export diagnostic summary for debugging."""
        return {
            "total_steps": len(self._step_history),
            "turn_elapsed_s": round(self.turn_elapsed_s, 2),
            "steps": [
                {"label": s.label, "index": s.step_index}
                for s in self._step_history
            ],
        }
