"""Posterior confidence estimates (post-generation).

Enhanced with code detection, completeness heuristics, language alignment,
and answer quality signals.
"""

from __future__ import annotations

import re

from core.runtime.decision.schema import DecisionOutput


def posterior_confidence(
    user_message: str,
    assistant_text: str,
    decision: DecisionOutput,
) -> float:
    """
    Lightweight heuristic posterior confidence — no second LLM call.

    Combines:
    - Prior confidence from Decision Layer
    - Length ratio (response adequacy)
    - Hedging phrase detection (AR + EN)
    - Question-answer alignment
    - Code block presence when code is expected
    - Completeness signals (truncation, trailing ellipsis)
    """
    text = assistant_text.strip()
    if not text:
        return 0.05

    prior = decision.confidence
    msg_len = max(len(user_message), 80)

    # Base: weighted blend of prior + length adequacy
    length_ratio = min(1.0, len(text) / msg_len)
    score = 0.50 * prior + 0.30 * length_ratio

    # --- Penalty: hedging phrases (AR + EN) ---
    hedges = (
        r"\b(maybe|perhaps|not sure|unclear|might|could be|i think|i'm not certain)\b",
        r"\b(لا أعلم|ربما|غير واضح|قد يكون|لست متأكد|يمكن أن)\b",
    )
    hedge_count = sum(1 for h in hedges if re.search(h, text, re.I))
    score -= 0.08 * min(hedge_count, 3)

    # --- Penalty: unanswered questions ---
    if "?" in user_message and "?" not in text and len(user_message) < 400:
        score -= 0.06

    # --- Bonus: code block when code intent ---
    if decision.intent == "code":
        if "```" in text or re.search(r"^(def |class |import |const |function )", text, re.M):
            score += 0.10
        else:
            score -= 0.10  # Expected code but didn't get any

    # --- Penalty: truncation signals ---
    if text.endswith("...") or text.endswith("…"):
        score -= 0.08
    if len(text) < 20 and decision.complexity != "low":
        score -= 0.12

    # --- Bonus: structured response for complex tasks ---
    if decision.complexity in ("medium", "high"):
        if any(marker in text for marker in ("\n- ", "\n* ", "\n1.", "\n##")):
            score += 0.05

    # --- Bonus: sufficient length for deep mode ---
    if decision.mode in ("deep", "planning", "research") and len(text) > 300:
        score += 0.05

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
