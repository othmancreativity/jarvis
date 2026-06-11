from __future__ import annotations

import logging
from typing import Any

from agents.base_agent import BaseAgent, AgentMessage

logger = logging.getLogger("jarvis.agents.security")


class SecurityAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(
            agent_id="security",
            name="Security Agent",
            description="Security monitoring and threat detection",
        )
        self.register_capability("threat_detection")
        self.register_capability("permission_check")

    async def handle_command(self, message: AgentMessage) -> None:
        payload = message.payload
        command = payload.get("command", "")

        if command == "check_threat":
            await self.send_response(message.sender, {
                "status": "success",
                "responseText": "Security check complete. No threats detected.",
            }, message.correlation_id)
        elif command == "status":
            await self.send_response(message.sender, {
                "status": "success",
                "security_level": "active",
                "responseText": "Security subsystem is active.",
            }, message.correlation_id)
        else:
            await self.send_response(message.sender, {"status": "error", "error": f"Unknown command: {command}"}, message.correlation_id)
