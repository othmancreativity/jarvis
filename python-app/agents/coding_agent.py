"""
JARVIS 4.5 — Coding Agent
==========================
Handles code generation, analysis, and execution assistance.
Provides: code_generation, code_review, syntax_check, documentation
"""

import logging
from typing import Any
from agents.base_agent import BaseAgent
from agents.message_bus import AgentMessage

logger = logging.getLogger("jarvis.agents.coding")


class CodingAgent(BaseAgent):
    """
    Coding Agent: Code generation and analysis.
    Capabilities: code_generation, code_review, syntax_check, refactoring
    """

    def __init__(self):
        super().__init__(
            agent_id="coding",
            name="Coding Agent",
            description="Code generation and analysis",
        )
        self.register_capability("code_generation")
        self.register_capability("code_review")
        self.register_capability("syntax_check")
        self.register_capability("refactoring")
        self.register_capability("documentation")
        self._supported_languages = ["python", "javascript", "typescript", "bash", "sql", "json", "yaml"]

    async def handle_command(self, message: AgentMessage) -> None:
        """Handle coding commands."""
        payload = message.payload
        command = payload.get("command", "")

        if command == "generate":
            language = payload.get("language", "python")
            description = payload.get("description", "")
            await self.send_response(
                message.sender,
                {
                    "status": "queued",
                    "action": "code_generate",
                    "language": language,
                    "description": description,
                },
                message.correlation_id,
            )
        elif command == "review":
            code = payload.get("code", "")
            language = payload.get("language", "python")
            await self.send_response(
                message.sender,
                {"status": "queued", "action": "code_review", "language": language, "code_length": len(code)},
                message.correlation_id,
            )
        elif command == "check_syntax":
            code = payload.get("code", "")
            language = payload.get("language", "python")
            # Basic syntax check for Python
            if language == "python":
                import ast
                try:
                    ast.parse(code)
                    await self.send_response(message.sender, {"status": "success", "valid": True}, message.correlation_id)
                except SyntaxError as e:
                    await self.send_response(
                        message.sender,
                        {"status": "success", "valid": False, "error": str(e), "line": e.lineno},
                        message.correlation_id,
                    )
            else:
                await self.send_response(message.sender, {"status": "error", "error": f"Syntax check not supported for {language}"}, message.correlation_id)
