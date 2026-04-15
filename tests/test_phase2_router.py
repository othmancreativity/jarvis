"""Phase 2.2 — Router scoring favors coder / fast / deep signals."""

from __future__ import annotations

from settings.loader import load_settings
from core.runtime.decision.schema import CostEstimate, DecisionOutput
from models.llm.profiles import load_models_config
from models.llm.router import ModelRouter, RouterOverride


def _base_decision(**kwargs: object) -> DecisionOutput:
    data = {
        "intent": "chat",
        "complexity": "medium",
        "mode": "normal",
        "requires_tools": False,
        "requires_planning": False,
        "confidence": 0.7,
        "cost_estimate": CostEstimate(tokens=2048, latency="medium", gpu_load="medium"),
    }
    data.update(kwargs)
    return DecisionOutput(**data)  # type: ignore[arg-type]


def test_router_code_intent_prefers_code_model() -> None:
    settings = load_settings()
    cfg = load_models_config()
    router = ModelRouter(settings=settings, models_cfg=cfg)
    d = _base_decision(intent="code", complexity="high", mode="normal")
    mid, reason = router.select(d, has_image=False)
    assert mid == settings.models.code_llm
    assert "score=" in reason


def test_router_fast_mode_low_complexity_prefers_fast_llm() -> None:
    settings = load_settings()
    cfg = load_models_config()
    router = ModelRouter(settings=settings, models_cfg=cfg)
    d = _base_decision(intent="chat", complexity="low", mode="fast")
    mid, _ = router.select(d, has_image=False)
    assert mid == settings.models.fast_llm


def test_router_deep_mode_prefers_deep_llm() -> None:
    settings = load_settings()
    cfg = load_models_config()
    router = ModelRouter(settings=settings, models_cfg=cfg)
    d = _base_decision(intent="chat", complexity="high", mode="deep")
    mid, _ = router.select(d, has_image=False)
    assert mid == settings.models.deep_llm


def test_router_vision_uses_vision_llm() -> None:
    settings = load_settings()
    cfg = load_models_config()
    router = ModelRouter(settings=settings, models_cfg=cfg)
    d = _base_decision()
    mid, _ = router.select(d, has_image=True)
    assert mid == settings.models.vision_llm


def test_router_override() -> None:
    settings = load_settings()
    cfg = load_models_config()
    router = ModelRouter(settings=settings, models_cfg=cfg)
    d = _base_decision()
    mid, reason = router.select(
        d,
        has_image=False,
        override=RouterOverride(model_id="gemma3:4b"),
    )
    assert mid == "gemma3:4b"
    assert reason == "user_override"
