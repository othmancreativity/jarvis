"""Map thinking mode → decode overrides (same model, different behavior)."""

from __future__ import annotations

from dataclasses import dataclass

from core.runtime.decision.schema import ThinkingMode
from models.llm.profiles import ModelProfile


@dataclass
class DecodeOverrides:
    temperature: float
    top_p: float
    max_tokens: int


def effective_profile(base: ModelProfile, mode: ThinkingMode) -> ModelProfile:
    """Return a shallowly adjusted profile for generation."""
    t, p, m = base.temperature, base.top_p, base.max_tokens
    if mode == "fast":
        t = min(0.9, t + 0.05)
        m = min(m, 1024)
    elif mode == "deep":
        t = max(0.3, t - 0.05)
        m = max(m, 4096)
    elif mode in ("planning", "research"):
        m = max(m, 4096)
    return ModelProfile(
        model_id=base.model_id,
        temperature=t,
        top_p=p,
        max_tokens=m,
        capability=base.capability,
    )
