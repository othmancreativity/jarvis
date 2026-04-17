"""Mutable conversation + run state for one user/session."""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from typing import Any


def _new_session_id() -> str:
    return uuid.uuid4().hex[:12]


@dataclass
class RunState:
    """Single turn loop state."""

    step_index: int = 0
    escalation_depth: int = 0
    last_model: str | None = None
    last_decision_snapshot: dict[str, Any] | None = None
    start_time: float = field(default_factory=time.monotonic)

    @property
    def elapsed_s(self) -> float:
        return time.monotonic() - self.start_time


@dataclass
class SessionState:
    """Conversation history + run metadata with session tracking."""

    session_id: str = field(default_factory=_new_session_id)
    messages: list[dict[str, str]] = field(default_factory=list)
    run: RunState = field(default_factory=RunState)
    created_at: float = field(default_factory=time.time)
    _turn_count: int = field(default=0, init=False, repr=False)

    def add_user(self, content: str) -> None:
        self.messages.append({
            "role": "user",
            "content": content,
        })
        self._turn_count += 1

    def add_assistant(self, content: str) -> None:
        self.messages.append({
            "role": "assistant",
            "content": content,
        })

    def add_system(self, content: str) -> None:
        self.messages.append({
            "role": "system",
            "content": content,
        })

    @property
    def turn_count(self) -> int:
        return self._turn_count

    @property
    def last_user_message(self) -> str | None:
        for msg in reversed(self.messages):
            if msg["role"] == "user":
                return msg["content"]
        return None

    @property
    def last_assistant_message(self) -> str | None:
        for msg in reversed(self.messages):
            if msg["role"] == "assistant":
                return msg["content"]
        return None

    @property
    def message_count(self) -> int:
        return len(self.messages)

    def snapshot(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "message_count": len(self.messages),
            "turn_count": self._turn_count,
            "escalation_depth": self.run.escalation_depth,
            "step_index": self.run.step_index,
            "elapsed_s": round(self.run.elapsed_s, 2),
        }

    def trim_to(self, max_messages: int) -> None:
        """Keep only the last *max_messages* messages."""
        if len(self.messages) > max_messages:
            self.messages = self.messages[-max_messages:]

    def reset_run(self) -> None:
        """Reset run state for a new turn within the same session."""
        self.run = RunState()
