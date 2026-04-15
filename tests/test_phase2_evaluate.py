"""Phase 2.18 / 2.20 — Evaluate finish vs escalate."""

from __future__ import annotations

from core.runtime.evaluate import evaluate_reply
from core.runtime.decision.schema import CostEstimate, DecisionOutput
from models.llm.profiles import RoutingConfig


def _routing() -> RoutingConfig:
    return RoutingConfig(confidence_high=0.75, confidence_medium=0.45, max_escalation_depth=2)


def _decision(conf: float = 0.8) -> DecisionOutput:
    return DecisionOutput(
        intent="chat",
        complexity="low",
        mode="fast",
        requires_tools=False,
        requires_planning=False,
        confidence=conf,
        cost_estimate=CostEstimate(tokens=512, latency="low", gpu_load="low"),
    )


def test_evaluate_high_band_finishes() -> None:
    r = _routing()
    ev = evaluate_reply(
        user_message="What is 2+2?",
        assistant_text="The answer is 4. " * 20,
        decision=_decision(),
        routing=r,
        escalation_depth=0,
        max_escalation_depth=2,
    )
    assert ev.band in ("high", "medium")
    assert ev.should_finish is True
    assert ev.should_escalate is False


def test_evaluate_low_band_escalates_when_allowed() -> None:
    r = _routing()
    ev = evaluate_reply(
        user_message="Explain quantum gravity in detail.",
        assistant_text="",
        decision=_decision(),
        routing=r,
        escalation_depth=0,
        max_escalation_depth=2,
    )
    assert ev.band == "low"
    assert ev.should_escalate is True
    assert ev.should_finish is False


def test_evaluate_respects_max_escalation_depth() -> None:
    r = _routing()
    ev = evaluate_reply(
        user_message="x",
        assistant_text="",
        decision=_decision(),
        routing=r,
        escalation_depth=2,
        max_escalation_depth=2,
    )
    assert ev.should_escalate is False
    assert ev.should_finish is True
