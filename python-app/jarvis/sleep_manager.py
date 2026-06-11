from __future__ import annotations

import asyncio
import logging
import time
from typing import Optional, Callable

from jarvis.cancellation_token import CancellationTokenSource

logger = logging.getLogger("jarvis.sleep_manager")


class SleepManager:
    """Idle monitoring for JARVIS.

    After N minutes without user input:
      - Flushes working memory to disk
      - Closes WebSocket / bridge connections
      - Stops the agent runtime loop
      - Reduces polling frequency
      - Enters low-CPU sleep mode

    Wakes on any user input and restores all subsystems.
    """

    def __init__(self, idle_timeout_minutes: int = 10) -> None:
        self._timeout: float = idle_timeout_minutes * 60.0
        self._last_activity: float = time.time()
        self._sleeping: bool = False
        self._wake_callbacks: list[Callable] = []
        self._sleep_callbacks: list[Callable] = []
        self._token_source: CancellationTokenSource = CancellationTokenSource()
        self._task: Optional[asyncio.Task] = None

    @property
    def is_sleeping(self) -> bool:
        return self._sleeping

    @property
    def idle_seconds(self) -> float:
        return time.time() - self._last_activity

    def register_wake(self, callback: Callable) -> None:
        self._wake_callbacks.append(callback)

    def register_sleep(self, callback: Callable) -> None:
        self._sleep_callbacks.append(callback)

    def notify_activity(self) -> None:
        self._last_activity = time.time()
        if self._sleeping:
            self._wake()

    def _wake(self) -> None:
        logger.info("Waking from sleep mode")
        self._sleeping = False
        self._token_source.reset()
        for cb in self._wake_callbacks:
            try:
                cb()
            except Exception as e:
                logger.error("Wake callback error: %s", e)

    async def _enter_sleep(self) -> None:
        logger.info("Entering sleep mode (idle for %ss)", self._timeout)
        self._sleeping = True
        for cb in self._sleep_callbacks:
            try:
                if asyncio.iscoroutinefunction(cb):
                    await cb()
                else:
                    cb()
            except Exception as e:
                logger.error("Sleep callback error: %s", e)

    async def run(self) -> None:
        while True:
            try:
                if not self._sleeping and self.idle_seconds >= self._timeout:
                    await self._enter_sleep()
                await asyncio.sleep(5)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error("Sleep monitor error: %s", e)

    def start(self) -> None:
        if self._task is None or self._task.done():
            self._task = asyncio.create_task(self.run())

    async def stop(self) -> None:
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        self._wake()


sleep_manager = SleepManager()
