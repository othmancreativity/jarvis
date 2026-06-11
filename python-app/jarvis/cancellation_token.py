from __future__ import annotations

import asyncio
from typing import Optional


class CancellationToken:
    """Propagates notification that operations should be cancelled.

    Modeled after C# System.Threading.CancellationToken.
    Thread-safe; designed for use with asyncio.
    """

    def __init__(self, source: CancellationTokenSource) -> None:
        self._source: CancellationTokenSource = source

    @property
    def is_cancellation_requested(self) -> bool:
        return self._source._cancelled

    def throw_if_cancellation_requested(self) -> None:
        if self.is_cancellation_requested:
            raise asyncio.CancelledError("Operation was cancelled")

    def __bool__(self) -> bool:
        return self.is_cancellation_requested

    def __await__(self):
        return self._source._event.wait().__await__()


class CancellationTokenSource:
    """Signals to a CancellationToken that it should be cancelled.

    Modeled after C# System.Threading.CancellationTokenSource.
    Supports linked tokens for hierarchical cancellation.
    """

    def __init__(self) -> None:
        self._cancelled: bool = False
        self._event: asyncio.Event = asyncio.Event()
        self._linked_sources: list[CancellationTokenSource] = []
        self._registered_callbacks: list[callable] = []

    @property
    def token(self) -> CancellationToken:
        return CancellationToken(self)

    @property
    def is_cancellation_requested(self) -> bool:
        return self._cancelled

    def cancel(self) -> None:
        if self._cancelled:
            return
        self._cancelled = True
        self._event.set()
        for cb in self._registered_callbacks:
            try:
                cb()
            except Exception:
                pass
        for src in self._linked_sources:
            src.cancel()

    def cancel_after(self, delay: float) -> asyncio.Task:
        async def _timer() -> None:
            await asyncio.sleep(delay)
            self.cancel()
        return asyncio.create_task(_timer())

    def register(self, callback: callable) -> None:
        self._registered_callbacks.append(callback)

    def link(self, other: CancellationTokenSource) -> None:
        self._linked_sources.append(other)
        other.register(self.cancel)
        if other.is_cancellation_requested:
            self.cancel()

    @staticmethod
    def create_linked(*sources: CancellationTokenSource) -> CancellationTokenSource:
        combined = CancellationTokenSource()
        for src in sources:
            combined.link(src)
        return combined

    def reset(self) -> None:
        self._cancelled = False
        self._event.clear()
        self._registered_callbacks.clear()
        self._linked_sources.clear()

    async def wait_for_cancellation(self) -> None:
        await self._event.wait()

    def __enter__(self) -> CancellationTokenSource:
        return self

    def __exit__(self, *args) -> None:
        self.cancel()
