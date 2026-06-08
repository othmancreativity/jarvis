"""
JARVIS 4.5 — Execution Agent
=============================
Coordinates tool execution, manages dependencies between steps,
handles retries and error recovery for multi-step operations.
"""

import asyncio
import logging
import time
from typing import Any, Optional
from agents.base_agent import BaseAgent
from agents.message_bus import AgentMessage, MessageType, message_bus
from core.tool_registry import registry

logger = logging.getLogger("jarvis.agents.execution")


class ExecutionAgent(BaseAgent):
    """
    Execution Agent: Coordinates tool execution.
    Capabilities: step execution, dependency management, retry logic, parallel execution
    """

    def __init__(self):
        super().__init__(
            agent_id="executor",
            name="Execution Agent",
            description="Tool execution and coordination",
        )
        self.register_capability("tool_execution")
        self.register_capability("retry_management")
        self.register_capability("parallel_execution")
        self.register_capability("step_sequencing")
        self._active_executions: dict[str, Any] = {}

    async def handle_command(self, message: AgentMessage) -> None:
        """Handle execution commands."""
        payload = message.payload
        command = payload.get("command", "")

        if command == "execute_plan":
            plan = payload.get("plan", [])
            execution_id = payload.get("execution_id", "")
            results = await self._execute_plan(plan, execution_id)
            await self.send_response(
                message.sender,
                {"results": results, "execution_id": execution_id},
                message.correlation_id,
            )
        elif command == "execute_tool":
            tool_name = payload.get("tool", "")
            params = payload.get("params", {})
            result = await self._execute_tool(tool_name, params)
            await self.send_response(
                message.sender,
                result,
                message.correlation_id,
            )

    async def _execute_plan(self, plan: list[dict], execution_id: str) -> list[dict]:
        """Execute a multi-step plan sequentially."""
        results = []
        for step in plan:
            tool_name = step.get("tool", "")
            params = step.get("params", {})

            result = await self._execute_tool(tool_name, params)
            results.append({
                "step": step.get("step", 0),
                "tool": tool_name,
                "result": result,
                "status": result.get("status", "unknown"),
            })

            # Stop on critical errors
            if result.get("status") in ("blocked", "error"):
                if step.get("critical", False):
                    break

            await asyncio.sleep(0.1)

        return results

    async def _execute_tool(self, tool_name: str, params: dict) -> dict:
        """Execute a single tool with validation and retry."""
        tool = registry.get(tool_name)
        if not tool:
            return {"status": "error", "error": f"Unknown tool: {tool_name}"}

        # Validate input
        valid, errors = tool.validate_input(params)
        if not valid:
            return {"status": "error", "error": f"Validation failed: {errors}"}

        # Execute with retry
        for attempt in range(tool.max_retries + 1):
            try:
                if tool.handler:
                    result = await tool.handler(params)
                    return result if isinstance(result, dict) else {"status": "success", "data": result}
                else:
                    return {"status": "error", "error": f"No handler for tool: {tool_name}"}
            except Exception as e:
                if attempt < tool.max_retries:
                    wait = 2 ** attempt  # Exponential backoff
                    await asyncio.sleep(wait)
                    continue
                return {"status": "error", "error": str(e)}

        return {"status": "error", "error": "Max retries exceeded"}
