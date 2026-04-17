"""Heuristic intent classifier + complexity / prior confidence (no fixed task→model map).

Enhanced with wider pattern coverage, Arabic intent detection,
and memory-driven bias integration.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from core.runtime.decision.cost_estimator import build_cost_estimate
from core.runtime.decision.schema import Complexity, DecisionOutput, Intent, ThinkingMode

if TYPE_CHECKING:
    from core.runtime.memory_hints import MemoryHints


# --- Pattern sets -----------------------------------------------------------

_CODE_PATTERNS = (
    r"\b(def|class|import|fn |const |let |var |public |async |yield |return )\b",
    r"[{};]\s*\n",
    r"```",
    r"\b(function|interface|struct|enum|module|package)\b",
    r"\b(python|javascript|typescript|rust|java|c\+\+|golang|sql)\b",
    r"\b(اكتب كود|برمج|اعمل سكربت|كود)\b",
)
_RESEARCH_PATTERNS = (
    r"\b(search|research|source|cite|paper|study|survey|investigate|compare)\b",
    r"\b(بحث|مصادر|ابحث|دراسة|مقارنة|معلومات عن)\b",
    r"\b(what is|who is|how does|explain|describe|tell me about)\b",
    r"\b(ما هو|من هو|كيف يعمل|اشرح|وضح|أخبرني عن)\b",
)
_ACTION_PATTERNS = (
    r"\b(open|run|execute|create file|delete|install|click|launch|start|stop|close)\b",
    r"\b(افتح|شغل|نفذ|أنشئ|احذف|ثبت|أغلق)\b",
)
_PLANNING_KEYWORDS = (
    r"\b(first|then|step|after that|next|plan|breakdown|decompose)\b",
    r"\b(أولاً|ثم|خطوة|بعد ذلك|خطط|قسم)\b",
)


def _guess_intent(text: str) -> Intent:
    """Classify intent from text patterns — order matters (most specific first)."""
    if any(re.search(p, text, re.I) for p in _CODE_PATTERNS):
        return "code"
    if any(re.search(p, text, re.I) for p in _ACTION_PATTERNS):
        return "action"
    if any(re.search(p, text, re.I) for p in _RESEARCH_PATTERNS):
        return "research"
    return "chat"


def _guess_complexity(text: str) -> Complexity:
    n = len(text)
    q = text.count("?")
    newlines = text.count("\n")

    # Short, direct messages
    if n < 150 and q <= 1 and newlines <= 1:
        return "low"

    # Long, multi-part, structured
    if n > 1500 or q >= 3 or newlines >= 5 or "\n\n" in text:
        return "high"

    return "medium"


def _prior_confidence(text: str, complexity: Complexity, intent: Intent) -> float:
    """Higher when task looks clear; lower when ambiguous or long."""
    base = 0.72

    # Complexity adjustments
    if complexity == "high":
        base -= 0.12
    elif complexity == "low":
        base += 0.08

    # Ambiguity signals
    if "?" in text and text.count("or ") >= 2:
        base -= 0.10
    if text.count("?") >= 3:
        base -= 0.06

    # Intent confidence adjustments
    if intent == "code":
        base += 0.04  # Code tasks are usually well-defined
    if intent == "research":
        base -= 0.05  # Research often needs multiple passes

    return max(0.05, min(0.98, base))


def _default_mode(intent: Intent, complexity: Complexity) -> ThinkingMode:
    if complexity == "low" and intent == "chat":
        return "fast"
    if intent == "research":
        return "research"
    if intent == "code" and complexity == "high":
        return "planning"
    if complexity == "high":
        return "deep"
    return "normal"


def _needs_tools(intent: Intent, text: str) -> bool:
    t = text.lower()
    if intent in ("research", "action"):
        return True
    if any(kw in t for kw in ("http", "url", "website", "browse", "download")):
        return True
    if any(kw in t for kw in ("file", "directory", "folder", "ملف", "مجلد")):
        return True
    return False


def _needs_planning(text: str, complexity: Complexity, intent: Intent) -> bool:
    if complexity == "high" and "\n" in text.strip():
        return True
    if intent == "code" and complexity == "high":
        return True
    return bool(re.search("|".join(_PLANNING_KEYWORDS), text, re.I))


def decide(
    user_message: str,
    *,
    has_image: bool = False,
    memory_hints: "MemoryHints | None" = None,
) -> DecisionOutput:
    """
    Produce :class:`DecisionOutput` using lightweight heuristics.

    ``memory_hints`` biases intent, mode, and confidence from learned patterns.
    """
    text = user_message.strip()
    intent = _guess_intent(text)
    complexity = _guess_complexity(text)

    # Phase 3: memory-driven bias
    if memory_hints:
        # Code-heavy user gets code bias on ambiguous intents
        if memory_hints.code_heavy and intent == "chat":
            # Check if message has any code-adjacent words
            if re.search(r"\b(fix|bug|error|write|build|make|create)\b", text, re.I):
                intent = "code"

        # Arabic quality preference → don't downgrade complexity
        if memory_hints.prefer_arabic_quality:
            complexity = complexity if complexity == "high" else "medium"

        # Override mode from learned preference (if set and we're in normal)
        if memory_hints.preferred_mode and memory_hints.preferred_mode != "normal":
            pass  # Don't override — let heuristics decide, but consider for edge cases

    if has_image:
        intent = "action" if intent == "chat" else intent

    mode = _default_mode(intent, complexity)
    requires_tools = _needs_tools(intent, text)
    requires_planning = _needs_planning(text, complexity, intent)
    prior = _prior_confidence(text, complexity, intent)

    # Phase 3: failure history depresses confidence
    if memory_hints and memory_hints.similar_failures > 0:
        prior = max(0.1, prior - 0.08 * memory_hints.similar_failures)

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
