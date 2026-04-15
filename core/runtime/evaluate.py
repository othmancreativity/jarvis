"""Evaluate stage: quality + posterior + stop/escalate recommendation."""

from __future__ import annotations

from dataclasses import dataclass

from core.runtime.confidence import confidence_band, posterior_confidence
from core.runtime.decision.schema import DecisionOutput
from core.runtime.memory_hints import MemoryHints
from models.llm.profiles import RoutingConfig


@dataclass
class EvaluateResult:
    posterior_confidence: float
    quality_score: float
    should_finish: bool
    should_escalate: bool
    band: str


def evaluate_reply(
    *,
    user_message: str,
    assistant_text: str,
    decision: DecisionOutput,
    routing: RoutingConfig,
    escalation_depth: int,
    max_escalation_depth: int,
    memory_hints: MemoryHints | None = None,
) -> EvaluateResult:
    """After full reply buffered, decide finish vs escalate.

    ``memory_hints`` is reserved for Phase 3 priors (Phase 2 accepts but ignores).
    """
    _ = memory_hints
    post = posterior_confidence(user_message, assistant_text, decision)
    # Quality proxy: inverse of empty / error markers
    quality = min(1.0, len(assistant_text.strip()) / 300.0)
    quality = min(1.0, 0.5 + quality * 0.5)

    band = confidence_band(
        post,
        high=routing.confidence_high,
        medium=routing.confidence_medium,
    )

    can_escalate = escalation_depth < max_escalation_depth
    should_escalate = band == "low" and can_escalate
    # Finish if good enough, or if we cannot escalate further (caller may emit fallback)
    should_finish = band in ("high", "medium") or (band == "low" and not can_escalate)

    if escalation_depth >= max_escalation_depth:
        should_escalate = False
        should_finish = True

    return EvaluateResult(
        posterior_confidence=post,
        quality_score=quality,
        should_finish=should_finish,
        should_escalate=should_escalate,
        band=band,
    )
