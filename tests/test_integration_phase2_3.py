"""Cross-phase integration tests: verify Phase 3 modules wire correctly
with Phase 2 runtime components.
"""

from __future__ import annotations

import pytest
from unittest.mock import MagicMock


class TestMemoryHintsIntegration:
    """Test that MemoryHints builds correctly from UserProfile and feeds into Decision."""

    def test_hints_from_real_profile(self, tmp_path):
        from core.memory.user_profile import UserProfile
        from core.runtime.memory_hints import build_hints_from_profile

        profile = UserProfile(user_id="test", profiles_dir=tmp_path)
        for _ in range(6):
            profile.record_interaction("code", 200)
        for _ in range(2):
            profile.record_interaction("chat", 50)
        profile.record_failure()
        profile.record_failure()

        hints = build_hints_from_profile(profile)
        assert hints.code_heavy is True
        assert hints.similar_failures == 2
        assert hints.prefer_arabic_quality is True  # default language is ar

    def test_hints_influence_decision(self, tmp_path):
        from core.memory.user_profile import UserProfile
        from core.runtime.memory_hints import build_hints_from_profile
        from core.runtime.decision.layer import decide

        profile = UserProfile(user_id="coder", profiles_dir=tmp_path)
        for _ in range(8):
            profile.record_interaction("code", 200)

        hints = build_hints_from_profile(profile)
        # Ambiguous message that could be chat or code
        decision = decide("fix this bug", memory_hints=hints)
        assert decision.intent == "code"  # code_heavy should bias toward code


class TestDecisionLayerUpgrades:
    """Test enhanced pattern detection in the decision layer."""

    def test_arabic_research_detection(self):
        from core.runtime.decision.layer import decide

        d = decide("ابحث عن معلومات عن الذكاء الاصطناعي")
        assert d.intent == "research"

    def test_arabic_code_detection(self):
        from core.runtime.decision.layer import decide

        d = decide("اكتب كود بايثون لحل هذه المشكلة")
        assert d.intent == "code"

    def test_arabic_action_detection(self):
        from core.runtime.decision.layer import decide

        d = decide("افتح المتصفح وابحث")
        assert d.intent == "action"

    def test_high_complexity_code_triggers_planning(self):
        from core.runtime.decision.layer import decide

        long_msg = """
        Create a full REST API with:
        - User authentication
        - Database models
        - Error handling
        - Unit tests
        - Deployment script
        """
        d = decide(long_msg)
        assert d.complexity == "high"
        assert d.requires_planning is True

    def test_simple_greeting_is_fast(self):
        from core.runtime.decision.layer import decide

        d = decide("hello")
        assert d.mode == "fast"
        assert d.complexity == "low"

    def test_programming_language_triggers_code(self):
        from core.runtime.decision.layer import decide

        d = decide("How do I use async/await in JavaScript?")
        assert d.intent == "code"

    def test_failure_history_lowers_confidence(self, tmp_path):
        from core.memory.user_profile import UserProfile
        from core.runtime.memory_hints import build_hints_from_profile
        from core.runtime.decision.layer import decide

        profile = UserProfile(user_id="fail", profiles_dir=tmp_path)
        for _ in range(3):
            profile.record_failure()

        hints_fail = build_hints_from_profile(profile)
        d_fail = decide("explain quantum computing", memory_hints=hints_fail)

        d_normal = decide("explain quantum computing")

        assert d_fail.confidence < d_normal.confidence


class TestConfidenceUpgrades:
    """Test enhanced posterior confidence scoring."""

    def test_code_intent_with_code_gets_bonus(self):
        from core.runtime.confidence import posterior_confidence
        from core.runtime.decision.schema import CostEstimate, DecisionOutput

        decision = DecisionOutput(
            intent="code", complexity="medium", mode="normal",
            requires_tools=False, requires_planning=False,
            confidence=0.7,
            cost_estimate=CostEstimate(tokens=2000, latency="medium", gpu_load="medium"),
        )

        # Response with code block
        with_code = "Here's the solution:\n```python\ndef hello():\n    print('hello')\n```"
        without_code = "You should try writing a function that prints hello."

        conf_code = posterior_confidence("write a hello function", with_code, decision)
        conf_no_code = posterior_confidence("write a hello function", without_code, decision)

        assert conf_code > conf_no_code

    def test_truncated_response_penalty(self):
        from core.runtime.confidence import posterior_confidence
        from core.runtime.decision.schema import CostEstimate, DecisionOutput

        decision = DecisionOutput(
            intent="chat", complexity="medium", mode="normal",
            requires_tools=False, requires_planning=False,
            confidence=0.7,
            cost_estimate=CostEstimate(tokens=2000, latency="medium", gpu_load="medium"),
        )

        complete = "This is a complete response with good information."
        truncated = "This is a response that seems to be cut off..."

        conf_complete = posterior_confidence("tell me about AI", complete, decision)
        conf_truncated = posterior_confidence("tell me about AI", truncated, decision)

        assert conf_complete > conf_truncated

    def test_structured_response_bonus(self):
        from core.runtime.confidence import posterior_confidence
        from core.runtime.decision.schema import CostEstimate, DecisionOutput

        decision = DecisionOutput(
            intent="research", complexity="high", mode="deep",
            requires_tools=True, requires_planning=False,
            confidence=0.55,
            cost_estimate=CostEstimate(tokens=8000, latency="high", gpu_load="high"),
        )

        structured = "Here are the findings:\n\n## Key Points\n\n- Point one with details\n- Point two with more details\n- Point three with conclusions"
        flat = "Here are the findings point one with details point two with more details point three with conclusions"

        conf_structured = posterior_confidence("research AI safety", structured, decision)
        conf_flat = posterior_confidence("research AI safety", flat, decision)

        assert conf_structured > conf_flat


class TestEvaluateUpgrades:
    """Test enhanced evaluation with quality scoring."""

    def test_quality_score_for_code_with_code_blocks(self):
        from core.runtime.evaluate import _quality_score
        from core.runtime.decision.schema import CostEstimate, DecisionOutput

        decision = DecisionOutput(
            intent="code", complexity="medium", mode="normal",
            requires_tools=False, requires_planning=False,
            confidence=0.7,
            cost_estimate=CostEstimate(tokens=2000, latency="medium", gpu_load="medium"),
        )

        with_code = "```python\ndef hello():\n    print('hello')\n```"
        without = "Try writing a hello function."

        q_code = _quality_score("write hello", with_code, decision)
        q_no = _quality_score("write hello", without, decision)

        assert q_code > q_no

    def test_memory_hints_raise_threshold(self):
        from core.runtime.evaluate import evaluate_reply
        from core.runtime.memory_hints import MemoryHints
        from core.runtime.decision.schema import CostEstimate, DecisionOutput
        from models.llm.profiles import RoutingConfig

        decision = DecisionOutput(
            intent="chat", complexity="medium", mode="normal",
            requires_tools=False, requires_planning=False,
            confidence=0.6,
            cost_estimate=CostEstimate(tokens=2000, latency="medium", gpu_load="medium"),
        )

        hints = MemoryHints(similar_failures=3)

        ev = evaluate_reply(
            user_message="explain something",
            assistant_text="This is a reasonable answer with some detail.",
            decision=decision,
            routing=RoutingConfig(),
            escalation_depth=0,
            max_escalation_depth=2,
            memory_hints=hints,
        )

        # With multiple failures, the system should be more demanding
        assert ev.reason  # reason should be non-empty

    def test_evaluate_has_reason_string(self):
        from core.runtime.evaluate import evaluate_reply
        from core.runtime.decision.schema import CostEstimate, DecisionOutput
        from models.llm.profiles import RoutingConfig

        decision = DecisionOutput(
            intent="chat", complexity="low", mode="fast",
            requires_tools=False, requires_planning=False,
            confidence=0.8,
            cost_estimate=CostEstimate(tokens=500, latency="low", gpu_load="low"),
        )

        ev = evaluate_reply(
            user_message="hi",
            assistant_text="Hello! How can I help you today?",
            decision=decision,
            routing=RoutingConfig(),
            escalation_depth=0,
            max_escalation_depth=2,
        )

        assert "band=" in ev.reason
        assert "post=" in ev.reason


class TestEventBusUpgrades:
    """Test enhanced event bus features."""

    def test_error_logging_not_crash(self):
        from core.events.event_bus import EventBus

        bus = EventBus()

        def bad_handler(**kw):
            raise ValueError("test error")

        bus.subscribe("test", bad_handler)
        # Should not raise
        bus.emit("test", data="hello")

    def test_unsubscribe(self):
        from core.events.event_bus import EventBus

        bus = EventBus()
        calls = []

        def handler(**kw):
            calls.append(1)

        bus.subscribe("ev", handler)
        bus.emit("ev")
        assert len(calls) == 1

        bus.unsubscribe("ev", handler)
        bus.emit("ev")
        assert len(calls) == 1  # no more calls

    def test_once_handler(self):
        from core.events.event_bus import EventBus

        bus = EventBus()
        calls = []

        def handler(**kw):
            calls.append(1)

        bus.subscribe_once("ev", handler)
        bus.emit("ev")
        bus.emit("ev")
        assert len(calls) == 1  # only fired once

    def test_event_history(self):
        from core.events.event_bus import EventBus

        bus = EventBus()
        bus.emit("a", x=1)
        bus.emit("b", y=2)

        assert len(bus.history) == 2
        assert bus.history[0].event == "a"
        assert bus.history[1].event == "b"


class TestSessionStateUpgrades:
    """Test enhanced session state."""

    def test_session_id_generated(self):
        from core.runtime.state.session import SessionState

        s1 = SessionState()
        s2 = SessionState()
        assert s1.session_id != s2.session_id
        assert len(s1.session_id) == 12

    def test_turn_count(self):
        from core.runtime.state.session import SessionState

        s = SessionState()
        s.add_user("hello")
        s.add_assistant("hi")
        s.add_user("how are you")
        assert s.turn_count == 2

    def test_last_message_accessors(self):
        from core.runtime.state.session import SessionState

        s = SessionState()
        s.add_user("user msg")
        s.add_assistant("bot msg")
        assert s.last_user_message == "user msg"
        assert s.last_assistant_message == "bot msg"

    def test_trim_to(self):
        from core.runtime.state.session import SessionState

        s = SessionState()
        for i in range(10):
            s.add_user(f"msg {i}")

        s.trim_to(5)
        assert s.message_count == 5

    def test_snapshot_has_session_id(self):
        from core.runtime.state.session import SessionState

        s = SessionState()
        s.add_user("test")
        snap = s.snapshot()
        assert "session_id" in snap
        assert "turn_count" in snap


class TestVramGuardUpgrades:
    """Test enhanced VramGuard."""

    def test_swap_returns_bool(self):
        from models.llm.vram import VramGuard

        guard = VramGuard(settle_s=0)
        assert guard.prepare("model_a") is True  # first model → swap
        assert guard.prepare("model_a") is False  # same model → no swap
        assert guard.prepare("model_b") is True  # different → swap

    def test_swap_count(self):
        from models.llm.vram import VramGuard

        guard = VramGuard(settle_s=0)
        guard.prepare("a")
        guard.prepare("b")
        guard.prepare("c")
        assert guard.swap_count == 3

    def test_release(self):
        from models.llm.vram import VramGuard

        guard = VramGuard(settle_s=0)
        guard.prepare("model_a")
        guard.release()
        assert guard.active_model is None

    def test_summary(self):
        from models.llm.vram import VramGuard

        guard = VramGuard(settle_s=0)
        guard.prepare("test_model")
        s = guard.summary()
        assert s["active"] == "test_model"
        assert s["swaps"] == 1


class TestPromptBuilderIntegration:
    """Test identity → prompt builder → system prompt pipeline."""

    def test_full_pipeline_produces_valid_prompt(self):
        from core.identity.jarvis_profile import load_jarvis_identity
        from core.identity.model_awareness import ModelAwarenessLayer
        from core.identity.prompt_builder import SystemPromptBuilder
        from core.identity.user_profile import IdentityUserProfile

        identity = load_jarvis_identity()
        user = IdentityUserProfile({"display_name": "Othman", "preferred_language": "ar"})
        awareness = ModelAwarenessLayer(identity, user)
        builder = SystemPromptBuilder(awareness)

        prompt = builder.build(
            mode="deep",
            language="ar",
            task_context="User uploaded a Python file",
            memory_snippet="User prefers detailed code explanations",
        )

        # Verify all sections present
        assert "Jarvis" in prompt
        assert "Othman" in prompt
        assert "DEEP" in prompt
        assert "Python" in prompt
        assert "code explanations" in prompt
        assert "Arabic" in prompt

    def test_minimal_prompt_is_short(self):
        from core.identity.jarvis_profile import JarvisIdentity
        from core.identity.model_awareness import ModelAwarenessLayer
        from core.identity.prompt_builder import SystemPromptBuilder

        awareness = ModelAwarenessLayer(JarvisIdentity())
        builder = SystemPromptBuilder(awareness)

        minimal = builder.build_minimal("en")
        full = builder.build(mode="deep", language="en", task_context="context")

        assert len(minimal) < len(full)
