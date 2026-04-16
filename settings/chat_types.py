"""Shared chat routing metadata for Web/CLI (avoid circular imports with orchestrator)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class RouteKind(str, Enum):
    """High-level routing label for debugging / UI."""

    STUB = "stub"
    LLM = "llm"
    FALLBACK = "fallback"


@dataclass(frozen=True)
class Decision:
    """Minimal decision object for Web UI / API responses."""

    kind: RouteKind
    model: str
    reason: str
