"""Shared planning behavior for planner and execution agents."""

from __future__ import annotations

import logging
from typing import Any

from agents.base_agent import BaseAgent
from memory.memory_system import memory

logger = logging.getLogger("jarvis.agents.planning")


class BasePlanningAgent(BaseAgent):
    """Base class for agents that create, validate, or execute plans."""

    def _validate_plan(self, plan: list[dict[str, Any]]) -> tuple[bool, str]:
        """Validate a plan's structure.

        Args:
            plan (list[dict[str, Any]]): Plan steps.

        Returns:
            tuple[bool, str]: Valid flag and diagnostic reason.
        """

        if not plan:
            return False, "Empty plan"
        for index, step in enumerate(plan):
            if "tool" not in step:
                return False, f"Step {index} missing tool"
            if "description" not in step:
                return False, f"Step {index} missing description"
        return True, "Plan is valid"

    def _record_failed_plan(self, name: str, plan: list[dict[str, Any]], reason: str) -> None:
        """Store failed plan details in procedural memory.

        Args:
            name (str): Procedure name.
            plan (list[dict[str, Any]]): Failed plan steps.
            reason (str): Failure reason.
        """

        try:
            existing = memory.recall_procedure(name)
            if not existing:
                memory.learn_procedure(name, f"Failed plan: {reason}", plan, source=self.agent_id)
            memory.record_procedure_failure(name)
        except Exception:
            logger.exception("Failed to record procedural failure")
