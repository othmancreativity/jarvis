from __future__ import annotations

import logging
from typing import Any

from agents.base_agent import BaseAgent, AgentMessage
from jarvis.browser_pool import pool as browser_pool

logger = logging.getLogger("jarvis.agents.browser")


class BrowserAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(
            agent_id="browser",
            name="Browser Agent",
            description="Web automation and data extraction",
        )
        self.register_capability("web_navigation")
        self.register_capability("page_extraction")
        self.register_capability("web_search")
        self.register_capability("screenshot_capture")

    async def handle_command(self, message: AgentMessage) -> None:
        payload = message.payload
        command = payload.get("command", "")

        if command in ("navigate", "open browser", "browser"):
            url = payload.get("url", payload.get("query", "about:blank"))
            try:
                async with await browser_pool.acquire() as browser:
                    page = browser.page
                    if url and url != "about:blank" and "://" not in url:
                        url = "https://" + url
                    if url and url != "about:blank":
                        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                    title = await page.title()
                    await self.send_response(message.sender, {
                        "status": "success",
                        "responseText": f"Opened browser at {page.url}. Page title: {title}",
                        "url": page.url,
                        "title": title,
                    }, message.correlation_id)
            except Exception as e:
                logger.error("Browser navigate error: %s", e)
                await self.send_response(message.sender, {"status": "error", "error": str(e)}, message.correlation_id)
        elif command == "screenshot":
            try:
                async with await browser_pool.acquire() as browser:
                    page = browser.page
                    b64 = (await page.screenshot(full_page=False, type="png")).hex()
                    await self.send_response(message.sender, {
                        "status": "success",
                        "responseText": "Screenshot captured",
                        "screenshot": b64,
                    }, message.correlation_id)
            except Exception as e:
                logger.error("Browser screenshot error: %s", e)
                await self.send_response(message.sender, {"status": "error", "error": str(e)}, message.correlation_id)
        elif command == "search google":
            query = payload.get("query", payload.get("query", ""))
            try:
                async with await browser_pool.acquire() as browser:
                    page = browser.page
                    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                    await page.goto(search_url, wait_until="domcontentloaded", timeout=30000)
                    title = await page.title()
                    await self.send_response(message.sender, {
                        "status": "success",
                        "responseText": f"Searched Google for '{query}'. Results at {page.url}",
                        "url": page.url,
                        "title": title,
                    }, message.correlation_id)
            except Exception as e:
                await self.send_response(message.sender, {"status": "error", "error": str(e)}, message.correlation_id)
        else:
            await self.send_response(message.sender, {"status": "error", "error": f"Unknown command: {command}"}, message.correlation_id)
