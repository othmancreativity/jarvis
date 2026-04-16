"""Phase 2.13 — Escalation deepens mode and complexity."""

from __future__ import annotations

from core.runtime.decision.schema import CostEstimate, DecisionOutput
from core.runtime.escalation import escalate_decision


def test_escalate_decision_deepens_mode() -> None:
    d = DecisionOutput(
        intent="chat",
        complexity="low",
        mode="fast",
        requires_tools=False,
        requires_planning=False,
        confidence=0.8,
        cost_estimate=CostEstimate(tokens=512, latency="low", gpu_load="low"),
    )
    n = escalate_decision(d)
    assert n.mode == "normal"
    assert n.complexity == "medium"
    assert n.confidence < d.confidence
