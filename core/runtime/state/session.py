"""Mutable conversation + run state for one user/session."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class RunState:
    """Single turn loop state."""

    step_index: int = 0
    escalation_depth: int = 0
    last_model: str | None = None
    last_decision_snapshot: dict[str, Any] | None = None


@dataclass
class SessionState:
    """Conversation history + run metadata."""

    messages: list[dict[str, str]] = field(default_factory=list)
    run: RunState = field(default_factory=RunState)

    def add_user(self, content: str) -> None:
        self.messages.append({"role": "user", "content": content})

    def add_assistant(self, content: str) -> None:
        self.messages.append({"role": "assistant", "content": content})

    def snapshot(self) -> dict[str, Any]:
        return {
            "message_count": len(self.messages),
            "escalation_depth": self.run.escalation_depth,
            "step_index": self.run.step_index,
        }
