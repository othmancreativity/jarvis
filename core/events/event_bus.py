"""Lightweight pub/sub for runtime events (sync + optional async).

Supports listener error logging, unsubscribe, event history,
and one-shot listeners.
"""

from __future__ import annotations

import asyncio
import time
from collections import defaultdict
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from typing import Any

from loguru import logger

Handler = Callable[..., Any]
AsyncHandler = Callable[..., Awaitable[Any]]


@dataclass
class EventRecord:
    """Lightweight log entry for emitted events."""

    event: str
    timestamp: float = field(default_factory=time.time)
    payload_keys: tuple[str, ...] = ()


class EventBus:
    """Subscribe callables by event name; emit sync or async.

    Features:
    - Error-safe: handler exceptions are logged, never propagated to caller
    - Unsubscribe support
    - One-shot listeners (auto-remove after first call)
    - Event history (bounded, for debugging)
    """

    def __init__(self, *, history_limit: int = 100) -> None:
        self._sync: dict[str, list[Handler]] = defaultdict(list)
        self._async: dict[str, list[AsyncHandler]] = defaultdict(list)
        self._once: dict[str, list[Handler]] = defaultdict(list)
        self._history: list[EventRecord] = []
        self._history_limit = history_limit

    def subscribe(self, event: str, fn: Handler) -> None:
        """Register a synchronous handler for *event*."""
        self._sync[event].append(fn)

    def subscribe_once(self, event: str, fn: Handler) -> None:
        """Register a handler that fires only once then auto-removes."""
        self._once[event].append(fn)

    def subscribe_async(self, event: str, fn: AsyncHandler) -> None:
        """Register an async handler for *event*."""
        self._async[event].append(fn)

    def unsubscribe(self, event: str, fn: Handler) -> bool:
        """Remove *fn* from *event* listeners. Returns True if found."""
        handlers = self._sync.get(event, [])
        try:
            handlers.remove(fn)
            return True
        except ValueError:
            return False

    def emit(self, event: str, **payload: Any) -> None:
        """Fire all sync handlers for *event*. Exceptions are logged, not raised."""
        self._record(event, payload)

        for fn in self._sync.get(event, []):
            try:
                fn(**payload)
            except Exception as exc:
                logger.warning("EventBus: handler {} for '{}' raised: {}", fn.__name__, event, exc)

        # One-shot handlers
        once = self._once.pop(event, [])
        for fn in once:
            try:
                fn(**payload)
            except Exception as exc:
                logger.warning("EventBus: once-handler {} for '{}' raised: {}", fn.__name__, event, exc)

    async def emit_async(self, event: str, **payload: Any) -> None:
        """Fire sync handlers first, then async handlers."""
        self.emit(event, **payload)
        for fn in self._async.get(event, []):
            try:
                await fn(**payload)
            except Exception as exc:
                logger.warning("EventBus: async handler {} for '{}' raised: {}", fn.__name__, event, exc)

    def _record(self, event: str, payload: dict[str, Any]) -> None:
        """Append to bounded event history."""
        self._history.append(EventRecord(event=event, payload_keys=tuple(payload.keys())))
        if len(self._history) > self._history_limit:
            self._history = self._history[-self._history_limit:]

    @property
    def history(self) -> list[EventRecord]:
        """Recent event history (for debugging and testing)."""
        return list(self._history)

    def clear(self) -> None:
        """Remove all handlers and history."""
        self._sync.clear()
        self._async.clear()
        self._once.clear()
        self._history.clear()
