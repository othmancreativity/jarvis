"""Unified memory interface: coordinates short-term, long-term, and database layers.

All backends are lazily initialised — only connect when first needed.
"""

from __future__ import annotations

from typing import Any

from loguru import logger


class MemoryManager:
    """Single entry point for all memory operations.

    Parameters
    ----------
    db_path : str
        SQLite database file path.
    chroma_dir : str
        ChromaDB persistence directory.
    redis_url : str | None
        Redis connection URL for short-term persistence (optional).
    max_short_messages : int
        Max messages kept in short-term buffer.
    max_short_tokens : int
        Approximate token budget for short-term buffer.
    """

    def __init__(
        self,
        *,
        db_path: str = "data/jarvis.db",
        chroma_dir: str = "data/chroma",
        redis_url: str | None = None,
        max_short_messages: int = 50,
        max_short_tokens: int = 6000,
        session_id: str = "default",
    ) -> None:
        self._db_path = db_path
        self._chroma_dir = chroma_dir
        self._redis_url = redis_url
        self._max_short_messages = max_short_messages
        self._max_short_tokens = max_short_tokens
        self._session_id = session_id

        # Lazy singletons
        self._short: Any | None = None
        self._long: Any | None = None
        self._db: Any | None = None

    # -- Lazy accessors ------------------------------------------------------

    @property
    def short_term(self) -> Any:
        if self._short is None:
            from core.memory.short_term import ShortTermMemory

            self._short = ShortTermMemory(
                max_messages=self._max_short_messages,
                max_tokens=self._max_short_tokens,
                redis_url=self._redis_url,
                session_id=self._session_id,
            )
        return self._short

    @property
    def long_term(self) -> Any:
        if self._long is None:
            from core.memory.long_term import LongTermMemory

            self._long = LongTermMemory(persist_dir=self._chroma_dir)
        return self._long

    @property
    def database(self) -> Any:
        if self._db is None:
            from core.memory.database import Database

            self._db = Database(db_path=self._db_path)
        return self._db

    # -- Interaction (read/write) --------------------------------------------

    def save_interaction(self, role: str, content: str) -> None:
        """Save a message to both short-term and database."""
        self.short_term.add(role, content)
        self.database.save_message(role, content, session_id=self._session_id)

    def get_context(self, n_messages: int = 20) -> list[dict[str, str]]:
        """Return the last *n* messages from short-term memory for LLM context."""
        return self.short_term.get_messages(n_messages)

    # -- Semantic memory -----------------------------------------------------

    def remember(self, text: str, *, metadata: dict[str, Any] | None = None) -> str:
        """Store a fact in long-term semantic memory."""
        return self.long_term.remember(text, metadata=metadata)

    def recall(self, query: str, n: int = 5) -> list[dict[str, Any]]:
        """Semantic similarity search across long-term memory."""
        return self.long_term.recall(query, n=n)

    # -- Unified search ------------------------------------------------------

    def search(self, query: str, *, n_semantic: int = 5, n_facts: int = 5) -> dict[str, Any]:
        """Search all memory layers and return combined results."""
        semantic = self.recall(query, n=n_semantic)
        facts = self.database.search_facts(query, limit=n_facts)
        return {
            "semantic": semantic,
            "facts": facts,
        }

    # -- Context building for LLM -------------------------------------------

    def build_context_snippet(self, query: str, max_chars: int = 1500) -> str:
        """Build a compact memory snippet for injection into LLM system prompt.

        Combines recent conversation + relevant semantic memories.
        """
        parts: list[str] = []

        # Recent conversation summary
        recent = self.get_context(5)
        if recent:
            conv_lines = [f"  {m['role']}: {m['content'][:120]}" for m in recent[-3:]]
            parts.append("Recent conversation:\n" + "\n".join(conv_lines))

        # Semantic recall
        try:
            recalls = self.recall(query, n=3)
            if recalls:
                mem_lines = [f"  - {r['text'][:150]}" for r in recalls if r.get("text")]
                if mem_lines:
                    parts.append("Relevant memories:\n" + "\n".join(mem_lines))
        except Exception:
            pass  # ChromaDB might not be ready

        snippet = "\n\n".join(parts)
        return snippet[:max_chars] if len(snippet) > max_chars else snippet

    # -- Lifecycle -----------------------------------------------------------

    def clear_session(self) -> None:
        """Clear short-term memory for the current session."""
        self.short_term.clear()

    def clear_all(self) -> None:
        """Clear all memory layers."""
        self.short_term.clear()
        try:
            self.long_term.clear()
        except Exception:
            pass
        self.database.clear_all()
        logger.info("MemoryManager: all memory cleared")

    def close(self) -> None:
        """Release resources."""
        if self._db is not None:
            self.database.close()
