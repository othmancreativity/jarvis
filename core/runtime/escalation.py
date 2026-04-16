"""Escalation: deeper mode / stronger routing bias after low posterior."""

from __future__ import annotations

from core.runtime.decision.schema import DecisionOutput, ThinkingMode


def escalate_decision(prev: DecisionOutput) -> DecisionOutput:
    """Return a new decision with deeper mode / higher implied quality need."""
    mode_order: list[ThinkingMode] = ["fast", "normal", "deep", "planning", "research"]
    try:
        i = mode_order.index(prev.mode)
    except ValueError:
        i = 1
    new_mode = mode_order[min(i + 1, len(mode_order) - 1)]

    # Slightly increase implied complexity for router
    complexity = prev.complexity
    if complexity == "low":
        complexity = "medium"
    elif complexity == "medium":
        complexity = "high"

    return prev.model_copy(
        update={
            "mode": new_mode,
            "complexity": complexity,
            "confidence": max(0.1, prev.confidence - 0.05),
            "requires_planning": True if new_mode in ("planning", "research") else prev.requires_planning,
        }
    )


def with_backoff_delay(attempt: int, base_s: float = 0.5) -> float:
    return base_s * (2**attempt)
