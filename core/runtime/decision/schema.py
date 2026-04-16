"""Structured decision output (prior confidence + cost estimate)."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


Intent = Literal["chat", "code", "research", "action"]
Complexity = Literal["low", "medium", "high"]
ThinkingMode = Literal["fast", "normal", "deep", "planning", "research"]
LatencyTier = Literal["low", "medium", "high"]
GpuLoadTier = Literal["low", "medium", "high"]


class CostEstimate(BaseModel):
    tokens: int = Field(ge=0, description="Rough budget for prompt+completion")
    latency: LatencyTier = "medium"
    gpu_load: GpuLoadTier = "medium"


class DecisionOutput(BaseModel):
    intent: Intent
    complexity: Complexity
    mode: ThinkingMode
    requires_tools: bool
    requires_planning: bool
    confidence: float = Field(ge=0.0, le=1.0, description="Prior confidence before main LLM call")
    cost_estimate: CostEstimate
    model_preference: Literal["auto"] = "auto"
