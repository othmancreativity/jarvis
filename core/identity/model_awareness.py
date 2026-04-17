"""Model awareness layer: ensures every LLM call receives consistent identity context.

Injects Jarvis identity + user profile + system context into every model
invocation so that no model acts as a standalone product.
"""

from __future__ import annotations

from typing import Any

from loguru import logger

from core.identity.jarvis_profile import JarvisIdentity
from core.identity.user_profile import IdentityUserProfile


class ModelAwarenessLayer:
    """Wraps identity injection for every model call.

    The same framing is applied across fast/deep/coder/vision routes;
    only the task and mode sections differ.
    """

    def __init__(
        self,
        identity: JarvisIdentity,
        user_profile: IdentityUserProfile | None = None,
    ) -> None:
        self._identity = identity
        self._user = user_profile or IdentityUserProfile()

    @property
    def identity(self) -> JarvisIdentity:
        return self._identity

    @property
    def user_profile(self) -> IdentityUserProfile:
        return self._user

    def set_user_profile(self, profile: IdentityUserProfile) -> None:
        self._user = profile

    def identity_context(self) -> str:
        """Full identity + user context string for system prompt injection."""
        parts: list[str] = []

        # 1. Jarvis identity
        parts.append(self._identity.identity_block())

        # 2. Safety rules
        safety = self._identity.safety_block()
        if safety:
            parts.append(safety)

        # 3. Model framing
        framing = self._identity.framing_block()
        if framing:
            parts.append(framing)

        # 4. User profile
        parts.append(self._user.prompt_fragment())

        return "\n\n".join(parts)

    def system_context_summary(self) -> str:
        """Short system context (runtime phase, tool availability) — no secrets."""
        return (
            "System context: runtime active, tools available on demand, "
            "memory system online, adaptive routing enabled."
        )
