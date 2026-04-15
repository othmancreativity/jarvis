"""Heuristic intent classifier + complexity / prior confidence (no fixed task→model map)."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from core.runtime.decision.cost_estimator import build_cost_estimate
from core.runtime.decision.schema import Complexity, DecisionOutput, Intent, ThinkingMode

if TYPE_CHECKING:
    from core.runtime.memory_hints import MemoryHints


_CODE_PATTERNS = (
    r"\b(def|class|import|fn |const |let |var |public |async )\b",
    r"[{};]\s*\n",
    r"```",
)
_RESEARCH_PATTERNS = (
    r"\b(search|research|source|cite|paper|study|survey)\b",
    r"بحث|مصادر|مصادر",
)
_ACTION_PATTERNS = (
    r"\b(open|run|execute|create file|delete|install|click)\b",
)


def _guess_intent(text: str) -> Intent:
    t = text.lower()
    if any(re.search(p, text, re.I) for p in _CODE_PATTERNS):
        return "code"
    if any(re.search(p, text, re.I) for p in _RESEARCH_PATTERNS):
        return "research"
    if any(re.search(p, t) for p in _ACTION_PATTERNS):
        return "action"
    return "chat"


def _guess_complexity(text: str) -> Complexity:
    n = len(text)
    q = text.count("?")
    if n < 200 and q <= 1:
        return "low"
    if n > 2000 or q >= 3 or "\n\n" in text:
        return "high"
    return "medium"


def _prior_confidence(text: str, complexity: Complexity) -> float:
    """Higher when task looks clear; lower when ambiguous or long."""
    base = 0.72
    if complexity == "high":
        base -= 0.12
    if complexity == "low":
        base += 0.08
    if "?" in text and text.count("or ") >= 2:
        base -= 0.1
    return max(0.05, min(0.98, base))


def _default_mode(intent: Intent, complexity: Complexity) -> ThinkingMode:
    if complexity == "low" and intent == "chat":
        return "fast"
    if intent == "research":
        return "research"
    if complexity == "high":
        return "deep"
    return "normal"


def _needs_tools(intent: Intent, text: str) -> bool:
    t = text.lower()
    if intent == "research":
        return True
    if "http" in t or "url" in t.lower():
        return True
    return False


def _needs_planning(text: str, complexity: Complexity) -> bool:
    if complexity == "high" and "\n" in text.strip():
        return True
    return bool(re.search(r"\b(first|then|step|after that)\b", text.lower()))


def decide(
    user_message: str,
    *,
    has_image: bool = False,
    memory_hints: MemoryHints | None = None,
) -> DecisionOutput:
    """
    Produce :class:`DecisionOutput` using lightweight heuristics.

    ``memory_hints`` can bias toward code / Arabic (Phase 2 stub; Phase 3 full).
    """
    text = user_message.strip()
    intent = _guess_intent(text)
    complexity = _guess_complexity(text)

    if memory_hints:
        if memory_hints.code_heavy:
            intent = "code"
        if memory_hints.prefer_arabic_quality:
            complexity = complexity if complexity == "high" else "medium"

    if has_image:
        intent = "action" if intent == "chat" else intent

    mode = _default_mode(intent, complexity)
    requires_tools = _needs_tools(intent, text)
    requires_planning = _needs_planning(text, complexity)
    prior = _prior_confidence(text, complexity)

    if memory_hints and memory_hints.similar_failures > 0:
        prior = max(0.1, prior - 0.1 * memory_hints.similar_failures)

    ce = build_cost_estimate(
        mode=mode,
        complexity=complexity,
        requires_tools=requires_tools,
        requires_planning=requires_planning,
        message=text,
    )

    return DecisionOutput(
        intent=intent,
        complexity=complexity,
        mode=mode,
        requires_tools=requires_tools,
        requires_planning=requires_planning,
        confidence=prior,
        cost_estimate=ce,
    )
