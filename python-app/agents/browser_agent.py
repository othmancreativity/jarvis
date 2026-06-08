"""
JARVIS 4.5 — Browser Agent
===========================
Handles web automation tasks via the BrowserController.
Provides high-level web operations: search, extract, navigate.
"""

import logging
from typing import Any
from agents.base_agent import BaseAgent
from agents.message_bus import AgentMessage

logger = logging.getLogger("jarvis.agents.browser")


class BrowserAgent(BaseAgent):
    """
    Browser Agent: High-level web automation.
    Capabilities: web_search, page_extraction, form_interaction, data_scraping
    """

    def __init__(self):
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
        """Handle browser commands."""
        payload = message.payload
        command = payload.get("command", "")

        if command == "navigate":
            url = payload.get("url", "")
            await self.send_response(
                message.sender,
                {"status": "queued", "action": "browser.navigate", "url": url},
                message.correlation_id,
            )
        elif command == "screenshot":
            await self.send_response(
                message.sender,
                {"status": "queued", "action": "browser.screenshot"},
                message.correlation_id,
            )
        elif command == "extract":
            selector = payload.get("selector", "")
            await self.send_response(
                message.sender,
                {"status": "queued", "action": "extract", "selector": selector},
                message.correlation_id,
            )
