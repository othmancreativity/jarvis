"""Lightweight pub/sub for runtime events (sync + optional async)."""

from __future__ import annotations

import asyncio
from collections import defaultdict
from collections.abc import Awaitable, Callable
from typing import Any


Handler = Callable[..., Any]
AsyncHandler = Callable[..., Awaitable[Any]]


class EventBus:
    """Subscribe callables by event name; emit sync or async."""

    def __init__(self) -> None:
        self._sync: dict[str, list[Handler]] = defaultdict(list)
        self._async: dict[str, list[AsyncHandler]] = defaultdict(list)

    def subscribe(self, event: str, fn: Handler) -> None:
        self._sync[event].append(fn)

    def subscribe_async(self, event: str, fn: AsyncHandler) -> None:
        self._async[event].append(fn)

    def emit(self, event: str, **payload: Any) -> None:
        for fn in self._sync[event]:
            try:
                fn(**payload)
            except Exception:
                # Never break caller on observer failure
                pass

    async def emit_async(self, event: str, **payload: Any) -> None:
        self.emit(event, **payload)
        for fn in self._async[event]:
            await fn(**payload)
