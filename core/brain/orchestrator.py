"""Bridge runtime → LLM: decision, route, stream, evaluate, optional escalation."""

from __future__ import annotations

from collections.abc import Iterator
from typing import TYPE_CHECKING, Any

from loguru import logger

from core.brain.dispatcher import dispatch_path, describe_path
from core.events.event_bus import EventBus
from core.runtime.decision import decide, refine_decision_cost
from core.runtime.decision.schema import DecisionOutput
from core.runtime.escalation import escalate_decision
from core.runtime.evaluate import evaluate_reply
from core.runtime.limits import RunLimits, from_routing
from core.runtime.memory_hints import empty_hints
from core.runtime.mode_controller import effective_profile
from core.runtime.runtime_manager import RuntimeManager
from core.runtime.state.session import SessionState
from settings.chat_types import Decision, RouteKind
from models.llm.engine import LLMEngine, LLMEngineError, stream_text_chunks
from models.llm.prompts import ThinkingMode, combined_system
from models.llm.profiles import load_models_config
from models.llm.router import ModelRouter, RouterOverride

if TYPE_CHECKING:
    from settings.app_settings import AppSettings


class ChatOrchestrator:
    """Phase 2 turn runner (streaming)."""

    def __init__(
        self,
        settings: AppSettings,
        *,
        bus: EventBus | None = None,
        engine: LLMEngine | None = None,
        model_override: str | None = None,
    ) -> None:
        self._settings = settings
        self._bus = bus or EventBus()
        self._engine = engine or LLMEngine()
        self._models_cfg = load_models_config()
        self._router = ModelRouter(settings=settings, models_cfg=self._models_cfg)
        self._limits: RunLimits = from_routing(self._models_cfg.routing)
        self._runtime = RuntimeManager(settings=settings, limits=self._limits)
        self._override = RouterOverride(model_id=model_override) if model_override else None

    def stream_tokens(self, user_message: str, *, has_image: bool = False) -> Iterator[str]:
        """Yield text chunks; may run second pass if evaluation escalates."""
        state = SessionState()
        state.add_user(user_message)
        self._runtime.begin_turn(state)
        self._bus.emit("on_message", text=user_message)

        hints = empty_hints()
        decision = decide(user_message, has_image=has_image, memory_hints=hints)
        self._bus.emit("on_decision", decision=decision.model_dump())

        escalation_depth = 0
        path = dispatch_path(decision)
        logger.info("dispatch path={} ({})", path, describe_path(path))

        while True:
            if not self._runtime.can_continue(state):
                yield from self._fallback_chunks("Reached iteration limit; try a shorter question.")
                break

            model_id, route_reason = self._router.select(
                decision,
                has_image=has_image,
                override=self._override,
            )
            profile = self._models_cfg.models.get(model_id)
            if profile is None:
                yield from self._fallback_chunks(f"No model profile for {model_id}")
                break

            eff = effective_profile(profile, decision.mode)
            lang = self._settings.jarvis.language[0] if self._settings.jarvis.language else "en"
            system = combined_system(language=lang, mode=decision.mode)  # type: ignore[arg-type]

            messages: list[dict[str, str]] = [
                {"role": "system", "content": system},
                *state.messages,
            ]

            self._runtime.record_step(state, "think", {"model": model_id})

            try:
                stream = self._engine.chat(
                    messages,
                    model_id,
                    profile=eff,
                    stream=True,
                )
            except LLMEngineError as e:
                logger.exception("LLM failure")
                self._bus.emit("on_error", error=str(e))
                yield from self._fallback_chunks(f"[Jarvis] Model error: {e}")
                break

            parts: list[str] = []
            for chunk in stream_text_chunks(stream):  # type: ignore[arg-type]
                parts.append(chunk)
                yield chunk

            assistant_text = "".join(parts)
            state.add_assistant(assistant_text)

            ev = evaluate_reply(
                user_message=user_message,
                assistant_text=assistant_text,
                decision=decision,
                routing=self._models_cfg.routing,
                escalation_depth=escalation_depth,
                max_escalation_depth=self._limits.max_escalation_depth,
                memory_hints=hints,
            )
            self._bus.emit(
                "on_evaluate",
                posterior=ev.posterior_confidence,
                band=ev.band,
                should_escalate=ev.should_escalate,
            )

            if ev.should_finish or not ev.should_escalate:
                break

            decision = escalate_decision(decision)
            decision = refine_decision_cost(decision, user_message)
            escalation_depth += 1
            state.run.escalation_depth = escalation_depth
            self._bus.emit("on_escalation", depth=escalation_depth, decision=decision.model_dump())
            # Drop last assistant message for re-generation
            if state.messages and state.messages[-1]["role"] == "assistant":
                state.messages.pop()

        self._bus.emit("on_response", done=True)

    def build_decision(self, user_message: str, *, has_image: bool = False) -> DecisionOutput:
        return decide(user_message, has_image=has_image, memory_hints=empty_hints())

    def last_route(self, user_message: str) -> tuple[Decision, DecisionOutput]:
        """Non-streaming meta for Web: first-pass model selection."""
        d_out = self.build_decision(user_message)
        mid, reason = self._router.select(d_out, has_image=False, override=self._override)
        d = Decision(
            kind=RouteKind.LLM,
            model=mid,
            reason=reason,
        )
        return d, d_out

    def _fallback_chunks(self, text: str) -> Iterator[str]:
        yield text
        if not text.endswith("\n"):
            yield "\n"


def stream_reply_chunks(
    settings: AppSettings,
    message: str,
    *,
    model_override: str | None = None,
) -> tuple[Decision, Iterator[str]]:
    """Adapter for :class:`core.bootstrap.ChatService`."""
    orch = ChatOrchestrator(settings, model_override=model_override)
    dec, _ = orch.last_route(message)

    def gen() -> Iterator[str]:
        yield from orch.stream_tokens(message)

    return dec, gen()
