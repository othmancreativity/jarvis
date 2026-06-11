from __future__ import annotations

import logging
from typing import Any

from agents.base_agent import BaseAgent, AgentMessage
from automation.screen import ScreenController

logger = logging.getLogger("jarvis.agents.vision")


class VisionAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(
            agent_id="vision",
            name="Vision Agent",
            description="Screen capture and OCR",
        )
        self.register_capability("screenshot")
        self.register_capability("ocr")
        self.register_capability("screen_analysis")
        self._screen = ScreenController()

    async def handle_command(self, message: AgentMessage) -> None:
        payload = message.payload
        command = payload.get("command", "")

        if command in ("screenshot", "capture screen", "take a picture"):
            result = await self._screen.screenshot()
            if result.get("status") == "success":
                await self.send_response(message.sender, {
                    "status": "success",
                    "responseText": "Screenshot captured successfully.",
                    "path": result.get("path"),
                }, message.correlation_id)
            else:
                await self.send_response(message.sender, {"status": "error", "error": result.get("error")}, message.correlation_id)
        elif command in ("ocr", "extract text", "read screen"):
            result = await self._screen.ocr()
            if result.get("status") == "success":
                text = result.get("text", "")
                await self.send_response(message.sender, {
                    "status": "success",
                    "responseText": f"Extracted text:\n{text}",
                }, message.correlation_id)
            else:
                await self.send_response(message.sender, {"status": "error", "error": result.get("error")}, message.correlation_id)
        else:
            await self.send_response(message.sender, {"status": "error", "error": f"Unknown command: {command}"}, message.correlation_id)
