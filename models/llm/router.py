"""Score candidate models from DecisionOutput + capability profiles (no static task→model)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from loguru import logger

from core.runtime.decision.schema import CostEstimate, DecisionOutput
from models.llm.profiles import ModelProfile, ModelsConfig, tier_to_score
from models.llm.vram import VramGuard

if TYPE_CHECKING:
    from settings.app_settings import AppSettings


@dataclass
class RouterOverride:
    """User/UI can force a model id; caps still enforced elsewhere."""

    model_id: str | None = None


def _quality_need(decision: DecisionOutput) -> float:
    """Higher when we should spend capability budget."""
    m = {"low": 0.35, "medium": 0.65, "high": 0.95}[decision.complexity]
    conf_gap = 1.0 - decision.confidence
    return min(1.0, m * 0.6 + conf_gap * 0.4 + (0.15 if decision.requires_planning else 0))


def _cost_penalty(ce: CostEstimate) -> float:
    lat = {"low": 0.2, "medium": 0.5, "high": 0.85}[ce.latency]
    gpu = {"low": 0.2, "medium": 0.55, "high": 0.9}[ce.gpu_load]
    tok = min(1.0, ce.tokens / 16000)
    return (lat + gpu + tok) / 3


def _intent_fit(model_id: str, profile: ModelCapabilityView, decision: DecisionOutput) -> float:
    """How well does this model match intent + mode (soft scoring)."""
    ib = profile.code_bias
    ar = profile.arabic_quality
    rs = tier_to_score(profile.reasoning_tier)

    if decision.intent == "code":
        score = ib * 0.65 + rs * 0.35
    elif decision.intent == "research":
        score = rs * 0.55 + ib * 0.2 + ar * 0.25
    else:
        score = ar * 0.55 + rs * 0.45

    mode_boost = {
        "fast": 0.25 if profile.latency_tier == "fast" else 0.0,
        "normal": 0.1,
        "deep": 0.35 if profile.reasoning_tier in ("high", "very_high") else 0.0,
        "planning": 0.25 * rs,
        "research": 0.3 * rs,
    }.get(decision.mode, 0.0)

    return min(1.0, score * 0.85 + mode_boost)


@dataclass
class ModelCapabilityView:
    code_bias: float
    arabic_quality: float
    reasoning_tier: str
    latency_tier: str


def _profile_view(p: ModelProfile) -> ModelCapabilityView:
    c = p.capability
    return ModelCapabilityView(
        code_bias=c.code_bias,
        arabic_quality=c.arabic_quality,
        reasoning_tier=c.reasoning_tier,
        latency_tier=c.latency_tier,
    )


class ModelRouter:
    """Pick best Ollama model id for this turn."""

    def __init__(
        self,
        *,
        settings: AppSettings,
        models_cfg: ModelsConfig,
        vram: VramGuard | None = None,
    ) -> None:
        self._settings = settings
        self._cfg = models_cfg
        self._vram = vram or VramGuard()
        self._routing = models_cfg.routing

    def candidate_ids(
        self,
        decision: DecisionOutput,
        *,
        has_image: bool,
        override: RouterOverride | None = None,
    ) -> list[str]:
        """Ordered pool of model ids to score."""
        m = self._settings.models
        if override and override.model_id:
            return [override.model_id]

        # Vision forces vision model when pixels present
        if has_image:
            return [m.vision_llm, m.default_llm, m.deep_llm]

        ids = [m.default_llm, m.fast_llm, m.code_llm, m.deep_llm]
        # de-dup preserve order
        seen: set[str] = set()
        out: list[str] = []
        for x in ids:
            if x not in seen:
                seen.add(x)
                out.append(x)
        return out

    def select(
        self,
        decision: DecisionOutput,
        *,
        has_image: bool,
        override: RouterOverride | None = None,
    ) -> tuple[str, str]:
        """Return (model_id, reason_summary)."""
        if override and override.model_id:
            mid = override.model_id
            self._vram.prepare(mid)
            return mid, "user_override"

        # Multimodal: must use vision-capable weights (TASKS 2.2.3).
        if has_image:
            mid = self._settings.models.vision_llm
            if mid not in self._cfg.models:
                logger.warning("Vision model {} missing from models.yaml; falling back to scoring", mid)
            else:
                self._vram.prepare(mid)
                return mid, "vision_required"

        candidates = self.candidate_ids(decision, has_image=has_image, override=override)
        w = self._routing.weights
        qn = _quality_need(decision)
        cp = _cost_penalty(decision.cost_estimate)

        best_id: str | None = None
        best_score = -1e9
        for mid in candidates:
            prof = self._cfg.models.get(mid)
            if prof is None:
                logger.warning("No profile for model {}; skipping", mid)
                continue
            view = _profile_view(prof)
            fit = _intent_fit(mid, view, decision)
            complexity_fit = tier_to_score(view.reasoning_tier) * (
                0.4
                if decision.complexity == "low"
                else 0.65
                if decision.complexity == "medium"
                else 0.95
            )

            score = (
                w.get("fit_complexity", 1.0) * complexity_fit
                + w.get("fit_mode", 1.0) * fit
                + w.get("quality_need", 1.2) * qn
                - w.get("cost_penalty", 0.35) * cp
            )
            # Soft alignment bonuses (TASKS 2.2.3–2.2.5): code / fast / deep without a static map.
            m = self._settings.models
            if decision.intent == "code" and mid == m.code_llm:
                score += w.get("fit_mode", 1.0) * 0.55
            if decision.mode == "fast" and decision.complexity == "low" and mid == m.fast_llm:
                score += w.get("fit_mode", 1.0) * 0.5
            if decision.mode == "deep" and decision.complexity == "high" and mid == m.deep_llm:
                score += w.get("fit_complexity", 1.0) * 0.35

            if score > best_score:
                best_score = score
                best_id = mid

        if not best_id:
            best_id = self._settings.models.default_llm
            return best_id, "fallback_default"

        self._vram.prepare(best_id)
        return best_id, f"score={best_score:.3f}"
