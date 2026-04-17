"""Short-term memory: in-session conversation history with token-aware trimming.

Backends:
* **In-memory** (always available) — default.
* **Redis** (optional persistence) — auto-reconnect; fallback to in-memory on failure.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Sequence

from loguru import logger

# ---------------------------------------------------------------------------
# Approximate token budget
# ---------------------------------------------------------------------------

_CHARS_PER_TOKEN = 4  # rough average for mixed AR/EN content


def _estimate_tokens(text: str) -> int:
    """Character-based token estimate (no tokeniser dependency)."""
    return max(1, len(text) // _CHARS_PER_TOKEN)


# ---------------------------------------------------------------------------
# Message container
# ---------------------------------------------------------------------------

@dataclass
class Message:
    role: str  # "user" | "assistant" | "system"
    content: str
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, str]:
        return {"role": self.role, "content": self.content}

    def token_count(self) -> int:
        return _estimate_tokens(self.content)


# ---------------------------------------------------------------------------
# Short-term memory
# ---------------------------------------------------------------------------

class ShortTermMemory:
    """Rolling conversation buffer with an approximate token budget.

    Parameters
    ----------
    max_messages : int
        Hard cap on the number of messages retained (newest kept).
    max_tokens : int
        Approximate token budget; oldest messages trimmed to fit.
    redis_url : str | None
        ``redis://host:port/db`` — if *None* or unreachable, falls back to
        in-memory-only mode.
    session_id : str
        Key prefix so multiple sessions can share one Redis instance.
    """

    def __init__(
        self,
        *,
        max_messages: int = 50,
        max_tokens: int = 6000,
        redis_url: str | None = None,
        session_id: str = "default",
    ) -> None:
        self._max_messages = max_messages
        self._max_tokens = max_tokens
        self._session_id = session_id
        self._messages: list[Message] = []
        self._redis: Any | None = None

        if redis_url:
            self._try_connect_redis(redis_url)

    # -- Redis helpers -------------------------------------------------------

    def _try_connect_redis(self, url: str) -> None:
        try:
            import redis as _redis

            self._redis = _redis.from_url(url, decode_responses=True, socket_timeout=2)
            self._redis.ping()
            logger.info("ShortTermMemory: Redis connected ({})", url)
            self._load_from_redis()
        except Exception as exc:
            logger.warning("ShortTermMemory: Redis unavailable ({}); using in-memory only", exc)
            self._redis = None

    def _redis_key(self) -> str:
        return f"jarvis:stm:{self._session_id}"

    def _sync_to_redis(self) -> None:
        if self._redis is None:
            return
        try:
            import json

            data = json.dumps(
                [{"role": m.role, "content": m.content, "ts": m.timestamp} for m in self._messages],
                ensure_ascii=False,
            )
            self._redis.set(self._redis_key(), data, ex=86400)  # 24 h TTL
        except Exception as exc:
            logger.warning("ShortTermMemory: Redis sync failed ({})", exc)

    def _load_from_redis(self) -> None:
        if self._redis is None:
            return
        try:
            import json

            raw = self._redis.get(self._redis_key())
            if raw:
                items = json.loads(raw)
                self._messages = [
                    Message(role=i["role"], content=i["content"], timestamp=i.get("ts", 0))
                    for i in items
                ]
                logger.debug("ShortTermMemory: loaded {} messages from Redis", len(self._messages))
        except Exception as exc:
            logger.warning("ShortTermMemory: Redis load failed ({})", exc)

    # -- Public API ----------------------------------------------------------

    def add(self, role: str, content: str) -> None:
        """Append a message and trim to budget."""
        self._messages.append(Message(role=role, content=content))
        self._trim()
        self._sync_to_redis()

    def get_messages(self, n: int | None = None) -> list[dict[str, str]]:
        """Return the last *n* messages (or all) as dicts for the LLM."""
        msgs = self._messages[-n:] if n else self._messages
        return [m.to_dict() for m in msgs]

    def get_all(self) -> list[Message]:
        return list(self._messages)

    def clear(self) -> None:
        self._messages.clear()
        if self._redis:
            try:
                self._redis.delete(self._redis_key())
            except Exception:
                pass

    @property
    def total_tokens(self) -> int:
        return sum(m.token_count() for m in self._messages)

    @property
    def count(self) -> int:
        return len(self._messages)

    # -- Trimming ------------------------------------------------------------

    def _trim(self) -> None:
        # Hard message cap
        while len(self._messages) > self._max_messages:
            self._messages.pop(0)

        # Token budget
        while self.total_tokens > self._max_tokens and len(self._messages) > 1:
            self._messages.pop(0)
