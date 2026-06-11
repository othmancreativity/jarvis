from __future__ import annotations

import asyncio
import logging
from typing import Optional
from dataclasses import dataclass, field

from playwright.async_api import async_playwright, Browser, BrowserContext, Page

logger = logging.getLogger("jarvis.browser_pool")


@dataclass
class PooledBrowser:
    """A browser instance managed by the pool."""
    browser: Browser
    context: BrowserContext
    in_use: bool = False
    page: Optional[Page] = None


class BrowserPool:
    """Async pool of Playwright browser instances.

    Reuses up to `max_size` concurrent browser instances to avoid
    the overhead of launching a new Chromium process for every command.

    Usage::
        async with pool.acquire() as browser:
            page = await browser.context.new_page()
            await page.goto("https://example.com")
    """

    def __init__(self, max_size: int = 5, headless: bool = False) -> None:
        self._max_size: int = max_size
        self._headless: bool = headless
        self._pool: list[PooledBrowser] = []
        self._queue: asyncio.Queue = asyncio.Queue()
        self._lock: asyncio.Lock = asyncio.Lock()
        self._closed: bool = False
        self._playwright = None

    async def _create_browser(self) -> PooledBrowser:
        pw = await async_playwright().start()
        browser = await pw.chromium.launch(
            headless=self._headless,
            args=[
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
            ]
        )
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            accept_downloads=True,
        )
        page = await context.new_page()
        pb = PooledBrowser(browser=browser, context=context, in_use=False, page=page)
        self._playwright = pw
        logger.info("Created new browser instance (pool: %s/%s)", len(self._pool), self._max_size)
        return pb

    async def acquire(self) -> "BrowserPool":
        pb = await self._acquire_internal()
        return _BrowserLease(pb, self)

    async def _acquire_internal(self) -> PooledBrowser:
        while True:
            async with self._lock:
                for pb in self._pool:
                    if not pb.in_use:
                        pb.in_use = True
                        return pb
                if len(self._pool) < self._max_size:
                    pb = await self._create_browser()
                    pb.in_use = True
                    self._pool.append(pb)
                    return pb
            await asyncio.sleep(0.1)

    async def release(self, pb: PooledBrowser) -> None:
        async with self._lock:
            pb.in_use = False

    async def close_all(self) -> None:
        async with self._lock:
            self._closed = True
            for pb in self._pool:
                try:
                    await pb.context.close()
                    await pb.browser.close()
                except Exception:
                    pass
            self._pool.clear()
            if self._playwright:
                await self._playwright.stop()

    @property
    def stats(self) -> dict:
        total = len(self._pool)
        in_use = sum(1 for pb in self._pool if pb.in_use)
        return {"total": total, "in_use": in_use, "idle": total - in_use, "max_size": self._max_size}


class _BrowserLease:
    """Context manager returned by BrowserPool.acquire()."""

    def __init__(self, pb: PooledBrowser, pool: BrowserPool) -> None:
        self._pb = pb
        self._pool = pool

    @property
    def browser(self) -> Browser:
        return self._pb.browser

    @property
    def context(self) -> BrowserContext:
        return self._pb.context

    @property
    def page(self) -> Page:
        return self._pb.page

    async def __aenter__(self) -> "PooledBrowser":
        return self._pb

    async def __aexit__(self, *args) -> None:
        await self._pool.release(self._pb)


pool = BrowserPool()
