"""Pre-execution token/latency/gpu tier estimates (inputs to router scoring)."""

from __future__ import annotations

import re

from core.runtime.decision.schema import Complexity, CostEstimate, DecisionOutput, ThinkingMode


def _base_tokens_for_complexity(c: Complexity) -> int:
    return {"low": 512, "medium": 2048, "high": 8192}[c]


def _latency_for_mode(mode: ThinkingMode) -> str:
    if mode == "fast":
        return "low"
    if mode in ("deep", "planning", "research"):
        return "high"
    return "medium"


def _gpu_for_mode_and_complexity(mode: ThinkingMode, complexity: Complexity) -> str:
    if mode == "fast" and complexity == "low":
        return "low"
    if complexity == "high" or mode in ("deep", "research"):
        return "high"
    return "medium"


def build_cost_estimate(
    *,
    mode: ThinkingMode,
    complexity: Complexity,
    requires_tools: bool,
    requires_planning: bool,
    message: str,
) -> CostEstimate:
    """Heuristic cost estimate (scoring-based, tunable later)."""
    est = _base_tokens_for_complexity(complexity)
    est += min(len(message) // 4, 4000)
    if requires_tools:
        est += 1500
    if requires_planning:
        est += 2000
    est = min(est, 32000)

    return CostEstimate(
        tokens=est,
        latency=_latency_for_mode(mode),
        gpu_load=_gpu_for_mode_and_complexity(mode, complexity),
    )


def refine_decision_cost(decision: DecisionOutput, message: str) -> DecisionOutput:
    """Fill or refresh ``cost_estimate`` on an existing decision."""
    ce = build_cost_estimate(
        mode=decision.mode,
        complexity=decision.complexity,
        requires_tools=decision.requires_tools,
        requires_planning=decision.requires_planning,
        message=message,
    )
    return decision.model_copy(update={"cost_estimate": ce})

