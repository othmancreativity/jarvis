from __future__ import annotations

import json
import logging
from typing import Any

from agents.base_agent import BasePlanningAgent, AgentMessage
from agents.message_bus import MessageType

logger = logging.getLogger("jarvis.agents.planner")


class PlannerAgent(BasePlanningAgent):
    def __init__(self) -> None:
        super().__init__(
            agent_id="planner",
            name="Planner Agent",
            description="Task decomposition and planning",
        )
        self.register_capability("task_decomposition")
        self.register_capability("plan_validation")
        self.register_capability("step_ordering")
        self.register_capability("failure_learning")

    async def handle_command(self, message: AgentMessage) -> None:
        payload = message.payload
        command = payload.get("command", "")

        if command == "decompose" or command == "plan":
            task = payload.get("task", payload.get("query", ""))
            plan = await self._decompose_task(task)
            await self.send_response(message.sender, {"plan": plan, "status": "success"}, message.correlation_id)
        elif command == "validate":
            plan = payload.get("plan", [])
            valid, reason = self._validate_plan(plan)
            await self.send_response(message.sender, {"valid": valid, "reason": reason}, message.correlation_id)
        else:
            await self.send_response(message.sender, {"status": "error", "error": f"Unknown command: {command}"}, message.correlation_id)

    async def _decompose_task(self, task: str) -> list[dict]:
        task_lower = task.lower()

        if "browser" in task_lower or "navigate" in task_lower or "open" in task_lower:
            return [
                {"step": 1, "tool": "browser.open", "description": "Open browser", "params": {"url": task}},
                {"step": 2, "tool": "browser.navigate", "description": f"Navigate: {task}"},
            ]
        if "screenshot" in task_lower:
            return [
                {"step": 1, "tool": "screen.screenshot", "description": "Capture screenshot"},
                {"step": 2, "tool": "screen.ocr", "description": "Extract text from screenshot"},
            ]
        if "file" in task_lower and "search" in task_lower:
            return [
                {"step": 1, "tool": "file.search", "description": f"Search: {task}"},
            ]
        if "file" in task_lower and "read" in task_lower:
            return [
                {"step": 1, "tool": "file.read", "description": f"Read file: {task}"},
            ]
        if "system" in task_lower or ("info" in task_lower and "system" in task_lower):
            return [
                {"step": 1, "tool": "system.info", "description": "Get system information"},
            ]
        if "code" in task_lower or "write" in task_lower or "generate" in task_lower:
            return [
                {"step": 1, "tool": "coding.analyze", "description": f"Analyze: {task}"},
                {"step": 2, "tool": "coding.generate", "description": "Generate code"},
            ]

        return [
            {"step": 1, "tool": "system.info", "description": "Gather system context"},
            {"step": 2, "tool": "analyze", "description": f"Analyze task: {task}"},
            {"step": 3, "tool": "execute", "description": "Execute appropriate tools"},
        ]

    def _validate_plan(self, plan: list[dict]) -> tuple[bool, str]:
        if not plan:
            return False, "Empty plan"
        for i, step in enumerate(plan):
            if "tool" not in step:
                return False, f"Step {i} missing tool"
            if "description" not in step:
                return False, f"Step {i} missing description"
        return True, "Plan is valid"
