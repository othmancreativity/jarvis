"""Map coarse intent → future tool/agent path (Phase 5 wires handlers)."""

from __future__ import annotations

from typing import Literal

from core.runtime.decision.schema import DecisionOutput

HandlerPath = Literal["llm_only", "tools", "planner_agent", "thinker_agent"]


def dispatch_path(decision: DecisionOutput) -> HandlerPath:
    """Return where this turn should be processed (policy stub)."""
    if decision.requires_planning and decision.complexity == "high":
        return "planner_agent"
    if decision.requires_tools:
        return "tools"
    return "llm_only"


def describe_path(path: HandlerPath) -> str:
    return {
        "llm_only": "direct_llm",
        "tools": "tool_loop_pending_phase5",
        "planner_agent": "planner_pending_phase6",
        "thinker_agent": "thinker_pending_phase6",
    }[path]
