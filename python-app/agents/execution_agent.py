from __future__ import annotations

import asyncio
import logging
from typing import Any, Optional

from agents.base_agent import BasePlanningAgent, AgentMessage
from agents.message_bus import message_bus
from core.tool_registry import registry

logger = logging.getLogger("jarvis.agents.execution")


class ExecutionAgent(BasePlanningAgent):
    def __init__(self) -> None:
        super().__init__(
            agent_id="executor",
            name="Execution Agent",
            description="Tool execution and coordination",
        )
        self.register_capability("tool_execution")
        self.register_capability("retry_management")
        self.register_capability("step_sequencing")
        self._active_executions: dict[str, Any] = {}

    async def handle_command(self, message: AgentMessage) -> None:
        payload = message.payload
        command = payload.get("command", "")

        if command == "execute_plan":
            plan = payload.get("plan", [])
            execution_id = payload.get("execution_id", "")
            results = await self._execute_plan(plan, execution_id)
            await self.send_response(message.sender, {"results": results, "execution_id": execution_id}, message.correlation_id)
        elif command == "execute_tool":
            tool_name = payload.get("tool", "")
            params = payload.get("params", {})
            result = await self._execute_tool(tool_name, params)
            await self.send_response(message.sender, result, message.correlation_id)
        elif command.startswith("file_") or command.startswith("shell"):
            tool_name = f"{'file' if command.startswith('file') else 'shell'}.{command.split('_', 1)[1] if '_' in command else command}"
            params = {"path": payload.get("query", ""), "content": payload.get("content", "")}
            result = await self._execute_tool(tool_name, params)
            await self.send_response(message.sender, {
                "status": result.get("status", "success"),
                "responseText": result.get("stdout") or result.get("content") or str(result),
            }, message.correlation_id)
        else:
            await self.send_response(message.sender, {"status": "error", "error": f"Unknown command: {command}"}, message.correlation_id)
