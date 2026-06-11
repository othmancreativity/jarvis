from __future__ import annotations

import logging
from typing import Any

from agents.base_agent import BaseAgent, AgentMessage

logger = logging.getLogger("jarvis.agents.coding")


class CodingAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(
            agent_id="coding",
            name="Coding Agent",
            description="Code generation and analysis",
        )
        self.register_capability("code_generation")
        self.register_capability("syntax_check")
        self.register_capability("code_review")

    async def handle_command(self, message: AgentMessage) -> None:
        payload = message.payload
        command = payload.get("command", "")

        if command in ("code", "generate code", "write code"):
            query = payload.get("query", "")
            await self.send_response(message.sender, {
                "status": "success",
                "responseText": f"I can help generate code for: {query}. Please specify the language and requirements.",
            }, message.correlation_id)
        else:
            await self.send_response(message.sender, {"status": "error", "error": f"Unknown command: {command}"}, message.correlation_id)
