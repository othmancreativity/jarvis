"""Posterior confidence estimates (post-generation)."""

from __future__ import annotations

import re

from core.runtime.decision.schema import DecisionOutput


def posterior_confidence(
    user_message: str,
    assistant_text: str,
    decision: DecisionOutput,
) -> float:
    """
    Lightweight heuristic: not a second LLM call (Phase 2).

    Uses length ratio, hedging phrases, and task fit.
    """
    text = assistant_text.strip()
    if not text:
        return 0.05

    prior = decision.confidence
    score = 0.55 * prior + 0.45 * min(1.0, len(text) / max(len(user_message), 80))

    hedges = (
        r"\b(maybe|perhaps|not sure|unclear|might|could be|لا أعلم|ربما|غير واضح)\b",
    )
    if any(re.search(h, text, re.I) for h in hedges):
        score -= 0.12

    if "?" in user_message and "?" not in text and len(user_message) < 400:
        score -= 0.08

    return max(0.05, min(0.99, score))


def confidence_band(
    value: float,
    *,
    high: float,
    medium: float,
) -> str:
    if value >= high:
        return "high"
    if value >= medium:
        return "medium"
    return "low"
