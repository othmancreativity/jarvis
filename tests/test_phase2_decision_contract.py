"""Phase 2.17.5 / 2.11 — DecisionOutput schema and bounds."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from core.runtime.decision.schema import CostEstimate, DecisionOutput


def test_decision_output_valid() -> None:
    d = DecisionOutput(
        intent="chat",
        complexity="low",
        mode="fast",
        requires_tools=False,
        requires_planning=False,
        confidence=0.5,
        cost_estimate=CostEstimate(tokens=1024, latency="low", gpu_load="low"),
    )
    assert d.model_preference == "auto"


def test_confidence_bounds() -> None:
    with pytest.raises(ValidationError):
        DecisionOutput(
            intent="chat",
            complexity="low",
            mode="normal",
            requires_tools=False,
            requires_planning=False,
            confidence=1.5,
            cost_estimate=CostEstimate(tokens=0),
        )


def test_cost_estimate_tokens_non_negative() -> None:
    with pytest.raises(ValidationError):
        CostEstimate(tokens=-1)
