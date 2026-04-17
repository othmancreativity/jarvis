"""Evaluate stage: quality + posterior + stop/escalate recommendation.

Enhanced with richer quality scoring, intent-specific checks, and
memory hint integration for learned patterns.
"""

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
    reason: str = ""


def _quality_score(
    user_message: str,
    assistant_text: str,
    decision: DecisionOutput,
) -> float:
    """Multi-signal quality estimate (0.0–1.0)."""
    text = assistant_text.strip()
    if not text:
        return 0.05

    score = 0.5  # baseline

    # Length adequacy
    length_ratio = min(1.0, len(text) / max(len(user_message), 60))
    score += 0.15 * length_ratio

    # Error markers
    error_phrases = (
        "i cannot", "i can't", "i'm unable", "error:", "exception:",
        "لا أستطيع", "غير قادر", "عذراً",
    )
    if any(ep in text.lower() for ep in error_phrases):
        score -= 0.15

    # Intent alignment
    if decision.intent == "code":
        has_code = "```" in text or ("def " in text) or ("class " in text)
        score += 0.15 if has_code else -0.10

    if decision.intent == "research":
        has_sources = any(w in text.lower() for w in ("http", "source", "according", "study"))
        score += 0.10 if has_sources else -0.05

    # Structured for complex
    if decision.complexity in ("medium", "high"):
        structured = any(m in text for m in ("\n- ", "\n* ", "\n1.", "\n## "))
        score += 0.08 if structured else 0.0

    # Over-brevity penalty for non-fast modes
    if decision.mode != "fast" and len(text) < 50:
        score -= 0.15

    return max(0.05, min(1.0, score))


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

    Uses memory_hints to adjust thresholds (e.g. raise bar if
    similar past failures indicate the model typically struggles).
    """
    post = posterior_confidence(user_message, assistant_text, decision)
    quality = _quality_score(user_message, assistant_text, decision)

    # Adjust thresholds from memory hints
    high_threshold = routing.confidence_high
    medium_threshold = routing.confidence_medium

    if memory_hints and memory_hints.similar_failures > 1:
        # Raise the bar when we know this kind of task has failed before
        high_threshold = min(0.95, high_threshold + 0.05 * memory_hints.similar_failures)

    band = confidence_band(
        post,
        high=high_threshold,
        medium=medium_threshold,
    )

    can_escalate = escalation_depth < max_escalation_depth
    should_escalate = band == "low" and can_escalate

    # Finish conditions
    should_finish = band in ("high", "medium") or (band == "low" and not can_escalate)

    if escalation_depth >= max_escalation_depth:
        should_escalate = False
        should_finish = True

    # Determine reason for debugging
    reason = f"band={band} post={post:.3f} quality={quality:.3f}"
    if should_escalate:
        reason += " → escalate"
    elif should_finish:
        reason += " → finish"

    return EvaluateResult(
        posterior_confidence=post,
        quality_score=quality,
        should_finish=should_finish,
        should_escalate=should_escalate,
        band=band,
        reason=reason,
    )
