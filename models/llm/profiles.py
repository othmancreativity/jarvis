"""Load ``config/models.yaml`` capability profiles and routing weights."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

import yaml


@dataclass
class ModelCapability:
    """Per-model metadata used by the router (scoring, not hardcoded routes)."""

    reasoning_tier: str = "medium"
    arabic_quality: float = 0.8
    code_bias: float = 0.5
    latency_tier: str = "medium"
    vram_estimate_gb: float = 4.5
    vision_required: bool = False


@dataclass
class RoutingConfig:
    weights: dict[str, float] = field(
        default_factory=lambda: {
            "fit_complexity": 1.0,
            "fit_mode": 1.0,
            "cost_penalty": 0.35,
            "quality_need": 1.2,
            "memory_bias": 0.25,
        }
    )
    confidence_high: float = 0.75
    confidence_medium: float = 0.45
    max_iterations: int = 5
    max_escalation_depth: int = 2


@dataclass
class ModelProfile:
    """Single Ollama model id + generation defaults + capability."""

    model_id: str
    temperature: float
    top_p: float
    max_tokens: int
    capability: ModelCapability


@dataclass
class ModelsConfig:
    """Full parsed ``models.yaml``."""

    defaults: dict[str, Any]
    models: dict[str, ModelProfile]
    routing: RoutingConfig


def _parse_capability(raw: dict[str, Any]) -> ModelCapability:
    return ModelCapability(
        reasoning_tier=str(raw.get("reasoning_tier", "medium")),
        arabic_quality=float(raw.get("arabic_quality", 0.8)),
        code_bias=float(raw.get("code_bias", 0.5)),
        latency_tier=str(raw.get("latency_tier", "medium")),
        vram_estimate_gb=float(raw.get("vram_estimate_gb", 4.5)),
        vision_required=bool(raw.get("vision_required", False)),
    )


def load_models_config(path: Path | None = None) -> ModelsConfig:
    """Load YAML from ``config/models.yaml`` relative to project root."""
    from settings.paths import PROJECT_ROOT

    p = path or (PROJECT_ROOT / "config" / "models.yaml")
    with p.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not data:
        return ModelsConfig(defaults={}, models={}, routing=RoutingConfig())

    defaults = data.get("defaults") or {}
    raw_models = data.get("models") or {}
    models: dict[str, ModelProfile] = {}
    for mid, spec in raw_models.items():
        if not isinstance(spec, dict):
            continue
        cap_raw = spec.get("capability") or {}
        models[mid] = ModelProfile(
            model_id=mid,
            temperature=float(spec.get("temperature", defaults.get("temperature", 0.7))),
            top_p=float(spec.get("top_p", defaults.get("top_p", 0.9))),
            max_tokens=int(spec.get("max_tokens", defaults.get("max_tokens", 4096))),
            capability=_parse_capability(cap_raw if isinstance(cap_raw, dict) else {}),
        )

    rr = data.get("routing") or {}
    w = (rr.get("weights") or {}) if isinstance(rr, dict) else {}
    th = (rr.get("thresholds") or {}) if isinstance(rr, dict) else {}
    esc = (rr.get("escalation") or {}) if isinstance(rr, dict) else {}
    routing = RoutingConfig(
        weights={
            "fit_complexity": float(w.get("fit_complexity", 1.0)),
            "fit_mode": float(w.get("fit_mode", 1.0)),
            "cost_penalty": float(w.get("cost_penalty", 0.35)),
            "quality_need": float(w.get("quality_need", 1.2)),
            "memory_bias": float(w.get("memory_bias", 0.25)),
        },
        confidence_high=float(th.get("confidence_high", 0.75)),
        confidence_medium=float(th.get("confidence_medium", 0.45)),
        max_iterations=int(esc.get("max_iterations", 5)),
        max_escalation_depth=int(esc.get("max_escalation_depth", 2)),
    )

    return ModelsConfig(defaults=defaults, models=models, routing=routing)


def tier_to_score(tier: str) -> float:
    """Map reasoning_tier label to numeric score for fit."""
    m = {
        "low": 0.35,
        "medium": 0.55,
        "high": 0.75,
        "very_high": 0.95,
    }
    return m.get(tier.lower(), 0.5)


LatencyTier = Literal["low", "medium", "high"]
GpuLoadTier = Literal["low", "medium", "high"]
