"""Browser control module — open Chrome, navigate, capture screenshots."""

import asyncio
import base64
from pathlib import Path
from typing import Optional

# Lazy import playwright to avoid startup overhead
try:
    from playwright.async_api import async_playwright, Browser, Page
except ImportError:
    async_playwright = None
    Browser = None
    Page = None


class BrowserController:
    """Control Chrome browser via Playwright."""

    def __init__(self):
        self._browser: Optional[Browser] = None
        self._page: Optional[Page] = None
        self._playwright = None

    async def _ensure_browser(self):
        if self._browser is None:
            if async_playwright is None:
                raise ImportError("Install playwright: pip install playwright && playwright install chromium")
            self._playwright = await async_playwright().start()
            self._browser = await self._playwright.chromium.launch(headless=False)
            self._page = await self._browser.new_page()

    async def open(self, url: str = None) -> dict:
        """Open Chrome. Optionally navigate to URL."""
        await self._ensure_browser()
        if url:
            await self._page.goto(url, wait_until="domcontentloaded", timeout=30000)
        return {"status": "opened", "url": url, "title": await self._page.title() if self._page.url != "about:blank" else "New Tab"}

    async def navigate(self, url: str) -> dict:
        """Navigate to URL in existing browser."""
        await self._ensure_browser()
        await self._page.goto(url, wait_until="domcontentloaded", timeout=30000)
        title = await self._page.title()
        return {"status": "navigated", "url": url, "title": title}

    async def get_page_info(self) -> dict:
        """Get page title, URL, meta description."""
        if not self._page:
            return {"error": "Browser not open"}
        title = await self._page.title()
        url = self._page.url
        description = ""
        try:
            desc_elem = await self._page.query_selector('meta[name="description"]')
            if desc_elem:
                description = await desc_elem.get_attribute("content") or ""
        except Exception:
            pass
        return {"title": title, "url": url, "description": description}

    async def screenshot(self) -> dict:
        """Capture browser screenshot as base64 PNG."""
        if not self._page:
            return {"error": "Browser not open"}
        screenshot = await self._page.screenshot(type="png")
        b64 = base64.b64encode(screenshot).decode("utf-8")
        return {"status": "success", "base64": f"data:image/png;base64,{b64}", "format": "png"}

    async def close(self) -> dict:
        """Close browser."""
        if self._browser:
            await self._browser.close()
            self._browser = None
            self._page = None
        if self._playwright:
            await self._playwright.stop()
            self._playwright = None
        return {"status": "closed"}

    async def scroll(self, direction: str = "down", amount: int = 500) -> dict:
        """Scroll page."""
        if not self._page:
            return {"error": "Browser not open"}
        if direction == "down":
            await self._page.evaluate(f"window.scrollBy(0, {amount})")
        elif direction == "up":
            await self._page.evaluate(f"window.scrollBy(0, -{amount})")
        return {"status": "scrolled", "direction": direction, "amount": amount}
