"""Bridge runtime → LLM: decision, route, stream, evaluate, optional escalation.

Phase 3 integration:
- MemoryManager for context injection and interaction persistence
- ContextBuffer for multimodal input staging
- SystemPromptBuilder for identity-aware prompts (replaces static combined_system)
- UserProfile → MemoryHints for Decision Layer priors
- Post-turn memory save and profile update
"""

from __future__ import annotations

import time
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
from core.runtime.memory_hints import MemoryHints, build_hints_from_profile, empty_hints
from core.runtime.mode_controller import effective_profile
from core.runtime.runtime_manager import RuntimeManager
from core.runtime.state.session import SessionState
from settings.chat_types import Decision, RouteKind
from models.llm.engine import LLMEngine, LLMEngineError, stream_text_chunks
from models.llm.profiles import load_models_config
from models.llm.router import ModelRouter, RouterOverride

if TYPE_CHECKING:
    from core.context.buffer import ContextBuffer
    from core.identity.prompt_builder import SystemPromptBuilder
    from core.memory.manager import MemoryManager
    from core.memory.user_profile import UserProfile
    from settings.app_settings import AppSettings


class ChatOrchestrator:
    """Full turn runner with memory, context buffer, and identity integration."""

    def __init__(
        self,
        settings: "AppSettings",
        *,
        bus: EventBus | None = None,
        engine: LLMEngine | None = None,
        model_override: str | None = None,
        memory: "MemoryManager | None" = None,
        user_profile: "UserProfile | None" = None,
        context_buffer: "ContextBuffer | None" = None,
        prompt_builder: "SystemPromptBuilder | None" = None,
    ) -> None:
        self._settings = settings
        self._bus = bus or EventBus()
        self._engine = engine or LLMEngine()
        self._models_cfg = load_models_config()
        self._router = ModelRouter(settings=settings, models_cfg=self._models_cfg)
        self._limits: RunLimits = from_routing(self._models_cfg.routing)
        self._runtime = RuntimeManager(settings=settings, limits=self._limits)
        self._override = RouterOverride(model_id=model_override) if model_override else None

        # Phase 3 modules (lazy init if not provided)
        self._memory = memory
        self._user_profile = user_profile
        self._context_buffer = context_buffer
        self._prompt_builder = prompt_builder

    # -- Lazy Phase 3 init ---------------------------------------------------

    def _ensure_memory(self) -> "MemoryManager":
        if self._memory is None:
            from core.memory.manager import MemoryManager

            from settings.paths import PROJECT_ROOT

            paths = self._settings.resolved_paths(PROJECT_ROOT)
            self._memory = MemoryManager(
                db_path=str(paths["sqlite"]),
                chroma_dir=str(paths["chroma"]),
            )
        return self._memory

    def _ensure_profile(self) -> "UserProfile":
        if self._user_profile is None:
            from core.memory.user_profile import UserProfile

            self._user_profile = UserProfile()
        return self._user_profile

    def _ensure_buffer(self) -> "ContextBuffer":
        if self._context_buffer is None:
            from core.context.buffer import ContextBuffer

            self._context_buffer = ContextBuffer()
        return self._context_buffer

    def _ensure_prompt_builder(self) -> "SystemPromptBuilder":
        if self._prompt_builder is None:
            from core.identity.jarvis_profile import load_jarvis_identity
            from core.identity.model_awareness import ModelAwarenessLayer
            from core.identity.prompt_builder import SystemPromptBuilder
            from core.identity.user_profile import IdentityUserProfile

            identity = load_jarvis_identity()
            profile = self._ensure_profile()
            id_profile = IdentityUserProfile.from_memory_profile(profile)
            awareness = ModelAwarenessLayer(identity, id_profile)
            self._prompt_builder = SystemPromptBuilder(awareness)
        return self._prompt_builder

    # -- Build hints from real profile ---------------------------------------

    def _build_hints(self) -> MemoryHints:
        try:
            profile = self._ensure_profile()
            return build_hints_from_profile(profile)
        except Exception:
            return empty_hints()

    # -- Build system prompt via identity pipeline ---------------------------

    def _build_system_prompt(
        self,
        decision: DecisionOutput,
        user_message: str,
    ) -> str:
        """Build system prompt using the full identity pipeline."""
        try:
            builder = self._ensure_prompt_builder()
            memory = self._ensure_memory()
            buffer = self._ensure_buffer()

            # Memory context
            memory_snippet = memory.build_context_snippet(user_message, max_chars=1200)

            # Buffer context
            task_context = buffer.merged_summary() if not buffer.is_empty else ""

            lang = self._settings.jarvis.language[0] if self._settings.jarvis.language else "en"

            return builder.build(
                mode=decision.mode,
                language=lang,
                task_context=task_context,
                memory_snippet=memory_snippet,
            )
        except Exception as exc:
            # Fallback to simple prompt on any identity pipeline error
            logger.warning("Prompt builder fallback: {}", exc)
            from models.llm.prompts import combined_system

            lang = self._settings.jarvis.language[0] if self._settings.jarvis.language else "en"
            return combined_system(language=lang, mode=decision.mode)  # type: ignore[arg-type]

    # -- Main entry ----------------------------------------------------------

    def stream_tokens(
        self,
        user_message: str,
        *,
        has_image: bool = False,
    ) -> Iterator[str]:
        """Yield text chunks; may run second pass if evaluation escalates."""
        t0 = time.monotonic()
        state = SessionState()
        state.add_user(user_message)
        self._runtime.begin_turn(state)
        self._bus.emit("on_message", text=user_message)

        # Phase 3: build hints from real profile
        hints = self._build_hints()

        # Phase 3: check context buffer for image modality
        buffer = self._ensure_buffer()
        modality = buffer.modality_flags()
        if modality.get("has_image"):
            has_image = True

        decision = decide(user_message, has_image=has_image, memory_hints=hints)
        self._bus.emit("on_decision", decision=decision.model_dump())

        escalation_depth = 0
        path = dispatch_path(decision)
        logger.info("dispatch path={} ({})", path, describe_path(path))

        assistant_text = ""

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

            # Phase 3: identity-aware system prompt
            system = self._build_system_prompt(decision, user_message)

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

        # Phase 3: post-turn persistence
        self._post_turn(user_message, assistant_text, decision)

        elapsed = time.monotonic() - t0
        self._bus.emit("on_response", done=True, elapsed_s=round(elapsed, 2))
        logger.info("turn completed in {:.2f}s", elapsed)

    # -- Post-turn persistence -----------------------------------------------

    def _post_turn(
        self, user_message: str, assistant_text: str, decision: DecisionOutput
    ) -> None:
        """Save interaction to memory and update user profile."""
        try:
            memory = self._ensure_memory()
            memory.save_interaction("user", user_message)
            if assistant_text:
                memory.save_interaction("assistant", assistant_text)
        except Exception as exc:
            logger.warning("Memory save failed: {}", exc)

        try:
            profile = self._ensure_profile()
            profile.record_interaction(decision.intent, len(user_message))
        except Exception as exc:
            logger.warning("Profile update failed: {}", exc)

        # Clear context buffer after turn completes
        try:
            buffer = self._ensure_buffer()
            buffer.clear()
        except Exception:
            pass

    # -- Public helpers ------------------------------------------------------

    def build_decision(self, user_message: str, *, has_image: bool = False) -> DecisionOutput:
        hints = self._build_hints()
        return decide(user_message, has_image=has_image, memory_hints=hints)

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

    @property
    def context_buffer(self) -> "ContextBuffer":
        """Expose buffer for interfaces to enqueue inputs."""
        return self._ensure_buffer()

    @property
    def memory(self) -> "MemoryManager":
        """Expose memory for direct queries."""
        return self._ensure_memory()

    def _fallback_chunks(self, text: str) -> Iterator[str]:
        yield text
        if not text.endswith("\n"):
            yield "\n"


def stream_reply_chunks(
    settings: "AppSettings",
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
