"""Optional memory-driven priors (Phase 3 will populate this)."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class MemoryHints:
    """Stub for learned preferences / patterns (Phase 2.21)."""

    prefer_arabic_quality: bool = False
    code_heavy: bool = False
    similar_failures: int = 0
    recent_success_strategy: str | None = None
    extra: dict[str, object] = field(default_factory=dict)


def empty_hints() -> MemoryHints:
    return MemoryHints()
