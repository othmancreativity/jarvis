"""
Chat service facade: Phase 2 uses :class:`~core.brain.orchestrator.ChatOrchestrator`.
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Tuple

from settings.chat_types import Decision, RouteKind
from settings.loader import load_settings


class ChatService:
    """Streams replies via orchestrator (Ollama + decision + router)."""

    def __init__(self, *, settings: object | None = None) -> None:
        self._settings = settings

    def stream_reply(self, message: str) -> Tuple[Decision, Iterator[str]]:
        if self._settings is None:
            from settings.loader import load_settings as ls

            self._settings = ls()

        try:
            from core.brain.orchestrator import stream_reply_chunks

            return stream_reply_chunks(self._settings, message)  # type: ignore[arg-type]
        except Exception as e:
            # Fallback if Ollama unreachable / import error
            return self._fallback(message, str(e))

    def _fallback(self, message: str, err: str) -> Tuple[Decision, Iterator[str]]:
        decision = Decision(
            kind=RouteKind.FALLBACK,
            model="none",
            reason=f"orchestrator_error:{err[:200]}",
        )

        def chunks() -> Iterator[str]:
            yield (
                f"[Jarvis] Could not run the AI stack ({err[:120]}). "
                "Ensure Ollama is running and models are pulled. "
                f"Echo: {message.strip()[:500]}\n"
            )

        return decision, chunks()


def get_chat_service(settings: object | None = None) -> ChatService:
    """Return a chat service instance with resolved settings."""
    resolved = settings if settings is not None else load_settings()
    return ChatService(settings=resolved)
