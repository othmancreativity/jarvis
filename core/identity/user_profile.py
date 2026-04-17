"""Identity-aware user profile for the prompt builder.

Complements :mod:`core.memory.user_profile` (adaptive counters) with
a structured view that the System Prompt Builder consumes.  Both modules
share the same JSON backing store to avoid duplicate data.
"""

from __future__ import annotations

from typing import Any

from loguru import logger


class IdentityUserProfile:
    """Read-only view of user profile data for prompt injection.

    This wraps :class:`core.memory.user_profile.UserProfile` and exposes
    the subset of data that identity/prompt layers need.
    """

    def __init__(self, profile_data: dict[str, Any] | None = None) -> None:
        self._data = profile_data or {}

    @classmethod
    def from_memory_profile(cls, profile: Any) -> "IdentityUserProfile":
        """Create from a :class:`core.memory.user_profile.UserProfile` instance."""
        return cls(profile.to_dict() if hasattr(profile, "to_dict") else {})

    # -- Accessors -----------------------------------------------------------

    @property
    def display_name(self) -> str:
        return self._data.get("display_name", "User")

    @property
    def language(self) -> str:
        return self._data.get("preferred_language", "ar")

    @property
    def style(self) -> str:
        return self._data.get("response_style", "balanced")

    @property
    def formality(self) -> str:
        return self._data.get("formality", "casual")

    @property
    def technical_level(self) -> str:
        return self._data.get("technical_level", "intermediate")

    # -- Prompt fragment -----------------------------------------------------

    def prompt_fragment(self) -> str:
        """Compact user context block for system prompts."""
        parts = [
            f"User: {self.display_name}",
            f"Language preference: {self.language}",
            f"Response style: {self.style} / {self.formality}",
            f"Technical level: {self.technical_level}",
        ]
        return "User profile:\n" + "\n".join(f"  {p}" for p in parts)

    def to_dict(self) -> dict[str, Any]:
        return {
            "display_name": self.display_name,
            "language": self.language,
            "style": self.style,
            "formality": self.formality,
            "technical_level": self.technical_level,
        }
