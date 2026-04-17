"""Memory-driven priors for the Decision Layer.

Phase 3 implementation: builds hints from real UserProfile + MemoryManager.
Falls back to empty hints when memory is not yet initialized.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from loguru import logger


@dataclass
class MemoryHints:
    """Learned preferences / patterns fed into Decision Layer + Router.

    Fields are populated from :class:`core.memory.user_profile.UserProfile`
    and :class:`core.memory.manager.MemoryManager`.
    """

    prefer_arabic_quality: bool = False
    code_heavy: bool = False
    similar_failures: int = 0
    recent_success_strategy: str | None = None
    preferred_mode: str | None = None
    preferred_language: str | None = None
    technical_level: str | None = None
    total_interactions: int = 0
    extra: dict[str, object] = field(default_factory=dict)


def empty_hints() -> MemoryHints:
    """Return zero-value hints (no memory connected)."""
    return MemoryHints()


def build_hints_from_profile(profile: Any) -> MemoryHints:
    """Build MemoryHints from a :class:`core.memory.user_profile.UserProfile`.

    Accepts *any* object with the expected attributes to avoid circular imports.
    """
    try:
        lang = getattr(profile, "preferred_language", "ar")
        return MemoryHints(
            prefer_arabic_quality=lang.startswith("ar") if lang else False,
            code_heavy=getattr(profile, "is_code_heavy", False),
            similar_failures=getattr(profile, "recent_failures", 0),
            recent_success_strategy=None,
            preferred_mode=getattr(profile, "preferred_mode", None),
            preferred_language=lang,
            technical_level=getattr(profile, "technical_level", None),
            total_interactions=getattr(profile, "total_interactions", 0),
        )
    except Exception as exc:
        logger.warning("Failed to build hints from profile: {}", exc)
        return empty_hints()
