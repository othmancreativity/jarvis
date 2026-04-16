"""System prompts and mode packs (Arabic / English / code / planning)."""

from __future__ import annotations

from typing import Literal

ThinkingMode = Literal["fast", "normal", "deep", "planning", "research"]


def jarvis_persona_ar() -> str:
    return (
        "أنت جارفيس، مساعد ذكاء اصطناعي محلي يتحدث العربية والإنجليزية. "
        "كن دقيقاً، مهذباً، وواضحاً. إذا لم تكن متأكداً فاعترف بذلك."
    )


def jarvis_persona_en() -> str:
    return (
        "You are Jarvis, a local AI assistant fluent in Arabic and English. "
        "Be precise, polite, and clear. Admit uncertainty when appropriate."
    )


def code_mode_system() -> str:
    return (
        "You are in CODE mode. Prefer concise code blocks, explain assumptions briefly, "
        "and mention edge cases. Use the user's language for explanations."
    )


def planning_mode_system() -> str:
    return (
        "You are in PLANNING mode. Break the task into ordered steps before executing. "
        "Keep steps short and actionable."
    )


def mode_pack(mode: ThinkingMode) -> str:
    """Composable fragments for decoding behavior (paired with model params in ModeController)."""
    packs: dict[ThinkingMode, str] = {
        "fast": "Respond briefly. One short paragraph unless a list is needed.",
        "normal": "balanced depth and length; no unnecessary verbosity.",
        "deep": "Think step by step. Show reasoning, then the final answer.",
        "planning": "First outline steps, then address each. Avoid skipping dependencies.",
        "research": "Cite need for tools/web when facts are missing; structure findings clearly.",
    }
    return packs.get(mode, packs["normal"])


def combined_system(
    *,
    language: str,
    mode: ThinkingMode,
    extra: str | None = None,
) -> str:
    """Merge persona + mode pack for the active locale."""
    if language.lower().startswith("ar"):
        base = jarvis_persona_ar()
    else:
        base = jarvis_persona_en()
    parts = [base, mode_pack(mode)]
    if extra:
        parts.append(extra)
    return "\n\n".join(parts)
