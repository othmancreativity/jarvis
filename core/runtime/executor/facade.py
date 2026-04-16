"""Tool execution façade — validates name; Phase 5 registers implementations."""

from __future__ import annotations

from typing import Any

from loguru import logger


class ToolExecutionError(RuntimeError):
    pass


class ToolExecutor:
    """``execute(name, args)`` with policy hooks (sandbox in Phase 5)."""

    def __init__(self, *, allow_all: bool = False) -> None:
        self._allow_all = allow_all

    def execute(self, name: str, args: dict[str, Any]) -> dict[str, Any]:
        """No tools registered yet — return structured 'not implemented' observation."""
        logger.info("tool request (stub): {} {}", name, args)
        return {
            "ok": False,
            "error": "no_tool_registered",
            "tool": name,
            "detail": "Phase 5 implements skills registry execution",
        }
