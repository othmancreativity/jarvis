from __future__ import annotations

import asyncio
import logging
from typing import Optional

from jarvis.browser_pool import pool as browser_pool

logger = logging.getLogger("jarvis.automation.browser")


class BrowserController:
    async def open(self, url: Optional[str] = None, headless: bool = False) -> dict:
        try:
            async with await browser_pool.acquire() as browser:
                page = browser.page
                if url:
                    if "://" not in url:
                        url = "https://" + url
                    await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                title = await page.title()
                return {"status": "opened", "url": page.url, "title": title}
        except Exception as e:
            logger.error("Browser open error: %s", e)
            return {"status": "error", "error": str(e)}

    async def navigate(self, url: str) -> dict:
        try:
            async with await browser_pool.acquire() as browser:
                page = browser.page
                if "://" not in url:
                    url = "https://" + url
                await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                title = await page.title()
                return {"status": "navigated", "url": page.url, "title": title}
        except Exception as e:
            logger.error("Navigation error: %s", e)
            return {"status": "error", "error": str(e)}

    async def close(self) -> dict:
        await browser_pool.close_all()
        return {"status": "closed"}

    async def screenshot(self, full_page: bool = False) -> dict:
        try:
            async with await browser_pool.acquire() as browser:
                page = browser.page
                import base64
                png_bytes = await page.screenshot(full_page=full_page, type="png")
                b64 = base64.b64encode(png_bytes).decode("utf-8")
                return {"status": "success", "base64": f"data:image/png;base64,{b64}"}
        except Exception as e:
            logger.error("Browser screenshot error: %s", e)
            return {"status": "error", "error": str(e)}

    async def new_tab(self, url: Optional[str] = None) -> dict:
        try:
            async with await browser_pool.acquire() as browser:
                page = await browser.context.new_page()
                if url:
                    await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                return {"status": "tab_created", "url": page.url}
        except Exception as e:
            return {"status": "error", "error": str(e)}
