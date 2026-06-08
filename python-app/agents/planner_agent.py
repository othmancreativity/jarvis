"""
JARVIS 4.5 — Planner Agent
===========================
Decomposes high-level tasks into executable steps.
Uses LLM for complex planning and rule-based fallback.
"""

import logging
from typing import Any
from agents.base_agent import BaseAgent
from agents.message_bus import AgentMessage

logger = logging.getLogger("jarvis.agents.planner")


class PlannerAgent(BaseAgent):
    """
    Planner Agent: Decomposes tasks into actionable steps.
    Capabilities: task decomposition, plan validation, step ordering
    """

    def __init__(self):
        super().__init__(
            agent_id="planner",
            name="Planner Agent",
            description="Task decomposition and planning",
        )
        self.register_capability("task_decomposition")
        self.register_capability("plan_validation")
        self.register_capability("step_ordering")
        self.register_capability("dependency_analysis")

    async def handle_command(self, message: AgentMessage) -> None:
        """Handle planning commands."""
        payload = message.payload
        command = payload.get("command", "")

        if command == "decompose":
            task = payload.get("task", "")
            plan = await self._decompose_task(task)
            await self.send_response(
                message.sender,
                {"plan": plan},
                message.correlation_id,
            )
        elif command == "validate":
            plan = payload.get("plan", [])
            valid, reason = self._validate_plan(plan)
            await self.send_response(
                message.sender,
                {"valid": valid, "reason": reason},
                message.correlation_id,
            )

    async def _decompose_task(self, task: str) -> list[dict]:
        """Decompose a task into steps."""
        # Rule-based decomposition for common patterns
        task_lower = task.lower()

        if "browser" in task_lower or "navigate" in task_lower or "open" in task_lower:
            return [
                {"step": 1, "tool": "browser.open", "description": "Open browser"},
                {"step": 2, "tool": "browser.navigate", "description": f"Navigate to URL from: {task}"},
                {"step": 3, "tool": "browser.get_page_info", "description": "Extract page information"},
            ]

        if "screenshot" in task_lower:
            return [
                {"step": 1, "tool": "screen.screenshot", "description": "Capture screenshot"},
                {"step": 2, "tool": "screen.ocr", "description": "Extract text from screenshot"},
            ]

        if "file" in task_lower and "search" in task_lower:
            return [
                {"step": 1, "tool": "file.search", "description": f"Search files: {task}"},
                {"step": 2, "tool": "file.get_info", "description": "Get file details"},
            ]

        # Default: return a generic plan
        return [
            {"step": 1, "tool": "system.info", "description": "Gather system context"},
            {"step": 2, "tool": "analyze", "description": f"Analyze task: {task}"},
            {"step": 3, "tool": "execute", "description": "Execute appropriate tools"},
        ]

    def _validate_plan(self, plan: list[dict]) -> tuple[bool, str]:
        """Validate a plan's correctness."""
        if not plan:
            return False, "Empty plan"

        for i, step in enumerate(plan):
            if "tool" not in step:
                return False, f"Step {i} missing tool"
            if "description" not in step:
                return False, f"Step {i} missing description"

        return True, "Plan is valid"
