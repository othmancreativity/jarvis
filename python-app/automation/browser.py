"""
JARVIS 4.5 — Browser Automation Module
=======================================
Full browser control via Playwright:
    - Open/close browser
    - Tab management (new, close, list, switch)
    - Navigation with wait strategies
    - Screenshot (viewport, full page, element)
    - Page info extraction
    - Scroll control
    - File download
    - Cookie management
    - Session persistence
"""

from __future__ import annotations

import asyncio
import base64
import json
import logging
import tempfile
from pathlib import Path
from typing import Optional, Any
from dataclasses import dataclass, field

logger = logging.getLogger("jarvis.automation.browser")

try:
    from playwright.async_api import async_playwright, Browser, BrowserContext, Page, Download
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False
    async_playwright = None
    Browser = None
    BrowserContext = None
    Page = None
    Download = None


@dataclass
class TabInfo:
    """Information about a browser tab."""
    index: int
    title: str
    url: str
    active: bool = False


class BrowserController:
    """
    Full-featured browser controller via Playwright.
    Manages browser lifecycle, tabs, navigation, screenshots, and downloads.
    """

    def __init__(self):
        self._playwright = None
        self._browser: Optional[Browser] = None
        self._context: Optional[BrowserContext] = None
        self._pages: list[Page] = []
        self._current_page_index: int = 0
        self._downloads_dir = Path.home() / ".jarvis" / "downloads"
        self._downloads_dir.mkdir(parents=True, exist_ok=True)
        self._session_file = Path.home() / ".jarvis" / "browser_session.json"

    async def _ensure_browser(self, headless: bool = False) -> None:
        """Ensure browser is open."""
        if self._browser is not None and not self._browser.is_connected():
            await self.close()
            self._browser = None

        if self._browser is None:
            if not HAS_PLAYWRIGHT:
                raise ImportError(
                    "Playwright not installed. Run: pip install playwright && playwright install chromium"
                )
            self._playwright = await async_playwright().start()
            self._browser = await self._playwright.chromium.launch(
                headless=headless,
                args=["--no-sandbox", "--disable-blink-features=AutomationControlled"]
            )
            self._context = await self._browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.0",
                accept_downloads=True,
            )
            # Set up download handler
            self._context.on("download", self._handle_download)
            page = await self._context.new_page()
            self._pages = [page]
            self._current_page_index = 0

    def _handle_download(self, download: Download) -> None:
        """Handle file downloads."""
        try:
            path = self._downloads_dir / download.suggested_filename
            asyncio.create_task(download.save_as(str(path)))
            logger.info(f"Download saved: {path}")
        except Exception as e:
            logger.error(f"Download error: {e}")

    def _current_page(self) -> Page:
        """Get the current active page."""
        if not self._pages:
            raise RuntimeError("No pages open")
        if self._current_page_index >= len(self._pages):
            self._current_page_index = 0
        return self._pages[self._current_page_index]

    # ── Core Browser Operations ────────────────────────────────────────

    async def open(self, url: Optional[str] = None, headless: bool = False) -> dict:
        """Open Chrome. Optionally navigate to URL."""
        try:
            await self._ensure_browser(headless=headless)
            page = self._current_page()
            if url:
                await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                await asyncio.sleep(0.5)  # Allow JS to settle
            title = await page.title()
            return {
                "status": "opened",
                "url": page.url,
                "title": title,
                "tabs": len(self._pages),
            }
        except Exception as e:
            logger.error(f"Browser open error: {e}")
            return {"status": "error", "error": str(e)}

    async def navigate(self, url: str, wait_until: str = "domcontentloaded") -> dict:
        """Navigate to URL in existing browser."""
        try:
            await self._ensure_browser()
            page = self._current_page()
            await page.goto(url, wait_until=wait_until, timeout=30000)
            await asyncio.sleep(0.5)
            title = await page.title()
            return {"status": "navigated", "url": page.url, "title": title}
        except Exception as e:
            logger.error(f"Navigation error: {e}")
            return {"status": "error", "error": str(e)}

    async def close(self) -> dict:
        """Close browser and all resources."""
        try:
            if self._context:
                await self._context.close()
                self._context = None
            if self._browser:
                await self._browser.close()
                self._browser = None
            if self._playwright:
                await self._playwright.stop()
                self._playwright = None
            self._pages = []
            self._current_page_index = 0
            return {"status": "closed"}
        except Exception as e:
            logger.error(f"Browser close error: {e}")
            return {"status": "error", "error": str(e)}

    # ── Tab Management ─────────────────────────────────────────────────

    async def new_tab(self, url: Optional[str] = None) -> dict:
        """Open a new browser tab."""
        try:
            await self._ensure_browser()
            page = await self._context.new_page()
            self._pages.append(page)
            self._current_page_index = len(self._pages) - 1
            if url:
                await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            return {
                "status": "tab_opened",
                "tab_index": self._current_page_index,
                "url": page.url,
                "tabs": len(self._pages),
            }
        except Exception as e:
            logger.error(f"New tab error: {e}")
            return {"status": "error", "error": str(e)}

    async def close_tab(self, index: int = -1) -> dict:
        """Close a tab by index (-1 for current)."""
        try:
            if not self._pages:
                return {"status": "error", "error": "No tabs open"}

            idx = self._current_page_index if index == -1 else index
            if idx < 0 or idx >= len(self._pages):
                return {"status": "error", "error": f"Invalid tab index: {idx}"}

            page = self._pages[idx]
            await page.close()
            self._pages.pop(idx)

            if self._current_page_index >= len(self._pages):
                self._current_page_index = max(0, len(self._pages) - 1)

            return {"status": "tab_closed", "tab_index": idx, "tabs": len(self._pages)}
        except Exception as e:
            logger.error(f"Close tab error: {e}")
            return {"status": "error", "error": str(e)}

    async def list_tabs(self) -> dict:
        """List all open tabs."""
        try:
            await self._ensure_browser()
            tabs = []
            for i, page in enumerate(self._pages):
                try:
                    title = await page.title()
                    tabs.append(TabInfo(
                        index=i,
                        title=title,
                        url=page.url,
                        active=(i == self._current_page_index),
                    ).__dict__)
                except Exception:
                    tabs.append(TabInfo(index=i, title="<unavailable>", url=page.url).__dict__)
            return {"status": "success", "tabs": tabs, "count": len(tabs)}
        except Exception as e:
            logger.error(f"List tabs error: {e}")
            return {"status": "error", "error": str(e)}

    async def switch_tab(self, index: int) -> dict:
        """Switch to a different tab by index."""
        try:
            if index < 0 or index >= len(self._pages):
                return {"status": "error", "error": f"Invalid tab index: {index}"}
            self._current_page_index = index
            page = self._current_page()
            return {"status": "switched", "tab_index": index, "url": page.url, "title": await page.title()}
        except Exception as e:
            logger.error(f"Switch tab error: {e}")
            return {"status": "error", "error": str(e)}

    # ── Page Information ───────────────────────────────────────────────

    async def get_page_info(self) -> dict:
        """Get page title, URL, meta description."""
        try:
            if not self._pages:
                return {"error": "Browser not open"}
            page = self._current_page()
            title = await page.title()
            url = page.url
            description = ""
            try:
                desc_elem = await page.query_selector('meta[name="description"]')
                if desc_elem:
                    description = await desc_elem.get_attribute("content") or ""
            except Exception:
                pass
            return {"title": title, "url": url, "description": description}
        except Exception as e:
            return {"error": str(e)}

    # ── Screenshot ─────────────────────────────────────────────────────

    async def screenshot(self, full_page: bool = False) -> dict:
        """Capture browser screenshot as base64 PNG."""
        try:
            await self._ensure_browser()
            page = self._current_page()
            screenshot = await page.screenshot(full_page=full_page, type="png")
            b64 = base64.b64encode(screenshot).decode("utf-8")
            return {
                "status": "success",
                "base64": f"data:image/png;base64,{b64}",
                "format": "png",
                "full_page": full_page,
            }
        except Exception as e:
            logger.error(f"Screenshot error: {e}")
            return {"status": "error", "error": str(e)}

    # ── Scroll ─────────────────────────────────────────────────────────

    async def scroll(self, direction: str = "down", amount: int = 500) -> dict:
        """Scroll page."""
        try:
            if not self._pages:
                return {"error": "Browser not open"}
            page = self._current_page()
            directions = {
                "down": (0, amount),
                "up": (0, -amount),
                "left": (-amount, 0),
                "right": (amount, 0),
            }
            dx, dy = directions.get(direction, (0, amount))
            await page.evaluate(f"window.scrollBy({dx}, {dy})")
            return {"status": "scrolled", "direction": direction, "amount": amount}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    # ── Download ───────────────────────────────────────────────────────

    async def download(self, url: str, filename: Optional[str] = None) -> dict:
        """Download a file via the browser."""
        try:
            await self._ensure_browser()
            page = self._current_page()

            if not filename:
                filename = Path(url).name or "download"

            dest = self._downloads_dir / filename

            # Use page download
            async with page.expect_download(timeout=60000) as download_info:
                await page.evaluate(f"window.location.href = '{url}'")
            download = await download_info.value
            await download.save_as(str(dest))

            return {
                "status": "success",
                "path": str(dest),
                "size": dest.stat().st_size if dest.exists() else 0,
                "filename": filename,
            }
        except Exception as e:
            logger.error(f"Download error: {e}")
            return {"status": "error", "error": str(e)}

    # ── Cookie Management ──────────────────────────────────────────────

    async def get_cookies(self) -> dict:
        """Get all cookies from the current context."""
        try:
            if not self._context:
                return {"cookies": []}
            cookies = await self._context.cookies()
            return {"status": "success", "cookies": cookies}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def save_session(self) -> dict:
        """Save browser session (cookies + storage) to disk."""
        try:
            if not self._context:
                return {"status": "error", "error": "No active context"}
            storage = await self._context.storage_state()
            with open(self._session_file, "w") as f:
                json.dump(storage, f)
            return {"status": "saved", "path": str(self._session_file)}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def load_session(self) -> dict:
        """Restore browser session from disk."""
        try:
            if not self._session_file.exists():
                return {"status": "error", "error": "No saved session found"}
            with open(self._session_file, "r") as f:
                storage = json.load(f)
            if self._context:
                await self._context.close()
            self._context = await self._browser.new_context(storage_state=storage)
            page = await self._context.new_page()
            self._pages = [page]
            self._current_page_index = 0
            return {"status": "loaded", "path": str(self._session_file)}
        except Exception as e:
            return {"status": "error", "error": str(e)}
