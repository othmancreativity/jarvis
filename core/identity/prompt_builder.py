"""System Prompt Builder: dynamic generator that combines identity, user profile,
task context, memory snippets, and mode fragments into a single system prompt.

Every model call passes through this builder via :meth:`build`.
"""

from __future__ import annotations

from typing import Any

from loguru import logger

from core.identity.jarvis_profile import JarvisIdentity
from core.identity.model_awareness import ModelAwarenessLayer
from core.identity.user_profile import IdentityUserProfile


class SystemPromptBuilder:
    """Assemble a deterministic system prompt for any model call.

    Ordering (stable):
    1. Identity block (who Jarvis is)
    2. Safety rules
    3. Model framing (component, tools, memory)
    4. User profile
    5. Task context (buffer summary, memory snippets)
    6. Mode fragment (fast / normal / deep / planning / research)

    Parameters
    ----------
    awareness : ModelAwarenessLayer
        Provides identity + user context.
    """

    def __init__(self, awareness: ModelAwarenessLayer) -> None:
        self._awareness = awareness

    def build(
        self,
        *,
        mode: str = "normal",
        language: str = "ar",
        task_context: str = "",
        memory_snippet: str = "",
        extra: str = "",
    ) -> str:
        """Build the full system prompt string.

        Parameters
        ----------
        mode : str
            Thinking mode (fast, normal, deep, planning, research).
        language : str
            Preferred response language (ar, en).
        task_context : str
            Buffer summary + attachments context from Observe.
        memory_snippet : str
            Relevant memories injected by MemoryManager.
        extra : str
            Additional instructions (e.g. tool-specific).
        """
        sections: list[str] = []

        # 1. Identity + safety + framing + user profile
        sections.append(self._awareness.identity_context())

        # 2. System context (runtime status)
        sections.append(self._awareness.system_context_summary())

        # 3. Memory context
        if memory_snippet:
            sections.append(memory_snippet)

        # 4. Task context (buffer)
        if task_context:
            sections.append(f"Current task context:\n{task_context}")

        # 5. Language directive
        if language.startswith("ar"):
            sections.append(
                "Respond in Arabic by default unless the user writes in English "
                "or explicitly requests English."
            )
        else:
            sections.append("Respond in English by default.")

        # 6. Mode fragment
        mode_text = self._mode_fragment(mode)
        if mode_text:
            sections.append(f"Current mode: {mode.upper()}\n{mode_text}")

        # 7. Extra
        if extra:
            sections.append(extra)

        return "\n\n".join(sections)

    @staticmethod
    def _mode_fragment(mode: str) -> str:
        fragments = {
            "fast": "Respond briefly. One short paragraph unless a list is needed.",
            "normal": "Balanced depth and length; no unnecessary verbosity.",
            "deep": "Think step by step. Show reasoning, then the final answer.",
            "planning": "First outline steps, then address each. Avoid skipping dependencies.",
            "research": "Cite need for tools/web when facts are missing; structure findings clearly.",
        }
        return fragments.get(mode, fragments["normal"])

    def build_minimal(self, language: str = "ar") -> str:
        """Minimal prompt for lightweight / classification calls."""
        return self.build(mode="fast", language=language)
