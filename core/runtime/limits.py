"""Per-turn limits from routing config + hardware."""

from __future__ import annotations

from dataclasses import dataclass

from models.llm.profiles import RoutingConfig


@dataclass
class RunLimits:
    max_iterations: int
    max_escalation_depth: int
    step_timeout_s: float = 120.0


def from_routing(r: RoutingConfig) -> RunLimits:
    return RunLimits(
        max_iterations=r.max_iterations,
        max_escalation_depth=r.max_escalation_depth,
    )
