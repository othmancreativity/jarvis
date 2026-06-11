from __future__ import annotations

import asyncio
import time
import logging
from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Callable, Any

from jarvis.cancellation_token import CancellationTokenSource

logger = logging.getLogger("jarvis.runtime")


class AgentState(str, Enum):
    IDLE = "idle"
    LISTENING = "listening"
    UNDERSTANDING = "understanding"
    PLANNING = "planning"
    EXECUTING = "executing"
    WAITING = "waiting"
    MONITORING = "monitoring"
    LEARNING = "learning"
    ERROR_RECOVERY = "error_recovery"
    EMERGENCY_STOP = "emergency_stop"
    SHUTDOWN = "shutdown"


class AgentEvent(str, Enum):
    USER_INPUT = "user_input"
    INTENT_CLASSIFIED = "intent_classified"
    PLAN_CREATED = "plan_created"
    EXECUTION_STARTED = "execution_started"
    EXECUTION_COMPLETE = "execution_complete"
    EXECUTION_FAILED = "execution_failed"
    WAITING_FOR_USER = "waiting_for_user"
    USER_RESPONDED = "user_responded"
    ERROR_OCCURRED = "error_occurred"
    RECOVERY_SUCCESS = "recovery_success"
    RECOVERY_FAILED = "recovery_failed"
    EMERGENCY_TRIGGERED = "emergency_triggered"
    SHUTDOWN_REQUESTED = "shutdown_requested"
    TIMEOUT = "timeout"


TRANSITION_MATRIX: dict[AgentState, dict[AgentEvent, AgentState]] = {
    AgentState.IDLE: {
        AgentEvent.USER_INPUT: AgentState.UNDERSTANDING,
        AgentEvent.SHUTDOWN_REQUESTED: AgentState.SHUTDOWN,
    },
    AgentState.LISTENING: {
        AgentEvent.USER_INPUT: AgentState.UNDERSTANDING,
        AgentEvent.TIMEOUT: AgentState.IDLE,
        AgentEvent.SHUTDOWN_REQUESTED: AgentState.SHUTDOWN,
    },
    AgentState.UNDERSTANDING: {
        AgentEvent.INTENT_CLASSIFIED: AgentState.PLANNING,
        AgentEvent.ERROR_OCCURRED: AgentState.ERROR_RECOVERY,
        AgentEvent.TIMEOUT: AgentState.LISTENING,
    },
    AgentState.PLANNING: {
        AgentEvent.PLAN_CREATED: AgentState.EXECUTING,
        AgentEvent.ERROR_OCCURRED: AgentState.ERROR_RECOVERY,
        AgentEvent.TIMEOUT: AgentState.LISTENING,
    },
    AgentState.EXECUTING: {
        AgentEvent.EXECUTION_COMPLETE: AgentState.MONITORING,
        AgentEvent.EXECUTION_FAILED: AgentState.ERROR_RECOVERY,
        AgentEvent.WAITING_FOR_USER: AgentState.WAITING,
        AgentEvent.TIMEOUT: AgentState.ERROR_RECOVERY,
        AgentEvent.EMERGENCY_TRIGGERED: AgentState.EMERGENCY_STOP,
    },
    AgentState.WAITING: {
        AgentEvent.USER_RESPONDED: AgentState.EXECUTING,
        AgentEvent.TIMEOUT: AgentState.IDLE,
        AgentEvent.ERROR_OCCURRED: AgentState.ERROR_RECOVERY,
    },
    AgentState.MONITORING: {
        AgentEvent.USER_INPUT: AgentState.UNDERSTANDING,
        AgentEvent.TIMEOUT: AgentState.IDLE,
        AgentEvent.SHUTDOWN_REQUESTED: AgentState.SHUTDOWN,
    },
    AgentState.LEARNING: {
        AgentEvent.TIMEOUT: AgentState.IDLE,
    },
    AgentState.ERROR_RECOVERY: {
        AgentEvent.RECOVERY_SUCCESS: AgentState.PLANNING,
        AgentEvent.RECOVERY_FAILED: AgentState.IDLE,
        AgentEvent.TIMEOUT: AgentState.IDLE,
        AgentEvent.EMERGENCY_TRIGGERED: AgentState.EMERGENCY_STOP,
    },
    AgentState.EMERGENCY_STOP: {
        AgentEvent.SHUTDOWN_REQUESTED: AgentState.SHUTDOWN,
    },
    AgentState.SHUTDOWN: {},
}


@dataclass
class RuntimeContext:
    session_id: str = ""
    user_id: str = "default"
    source: str = "local"
    current_intent: str = ""
    intent_confidence: float = 0.0
    execution_plan: list[dict] = field(default_factory=list)
    current_step: int = 0
    max_steps: int = 20
    iteration_count: int = 0
    max_iterations: int = 50
    error_count: int = 0
    max_errors: int = 5
    start_time: float = field(default_factory=time.time)
    last_activity: float = field(default_factory=time.time)
    timeout_seconds: float = 300.0
    tool_results: list[dict] = field(default_factory=list)

    def is_timed_out(self) -> bool:
        return (time.time() - self.last_activity) > self.timeout_seconds

    def is_looping(self) -> bool:
        return self.iteration_count >= self.max_iterations

    def has_too_many_errors(self) -> bool:
        return self.error_count >= self.max_errors

    def touch(self) -> None:
        self.last_activity = time.time()


class AgentRuntime:
    def __init__(self) -> None:
        self.state = AgentState.IDLE
        self.previous_state: Optional[AgentState] = None
        self.context = RuntimeContext()
        self._transition_history: deque = deque(maxlen=100)
        self._state_change_callbacks: list[Callable[[AgentState, AgentState], None]] = []
        self._running = False
        self._cancel_source: CancellationTokenSource = CancellationTokenSource()

    @property
    def cancellation_token(self) -> CancellationTokenSource:
        return self._cancel_source

    def on_state_change(self, callback: Callable[[AgentState, AgentState], None]) -> None:
        self._state_change_callbacks.append(callback)

    def can_transition(self, event: AgentEvent) -> bool:
        transitions = TRANSITION_MATRIX.get(self.state, {})
        return event in transitions

    async def trigger(self, event: AgentEvent, data: Any = None) -> bool:
        if not self.can_transition(event):
            return False
        next_state = TRANSITION_MATRIX[self.state][event]

        if self.context.is_looping():
            logger.error("Loop detected: %s iterations", self.context.iteration_count)
            await self._force_state(AgentState.ERROR_RECOVERY)
            return False

        self._transition_history.append({
            "from": self.state.value,
            "to": next_state.value,
            "event": event.value,
            "timestamp": time.time(),
        })

        old = self.state
        self.state = next_state
        self.context.iteration_count += 1
        self.context.touch()

        for cb in self._state_change_callbacks:
            try:
                if asyncio.iscoroutinefunction(cb):
                    await cb(old, self.state)
                else:
                    cb(old, self.state)
            except Exception as e:
                logger.error("State change callback error: %s", e)

        return True

    async def _force_state(self, state: AgentState) -> None:
        old = self.state
        self.state = state
        for cb in self._state_change_callbacks:
            try:
                if asyncio.iscoroutinefunction(cb):
                    await cb(old, self.state)
                else:
                    cb(old, self.state)
            except Exception:
                pass

    def emergency_stop(self) -> None:
        logger.critical("EMERGENCY STOP ACTIVATED")
        self.state = AgentState.EMERGENCY_STOP
        self._running = False
        self._cancel_source.cancel()

    async def start(self) -> None:
        self._running = True
        logger.info("Agent runtime started")
        while self._running and self.state != AgentState.SHUTDOWN:
            try:
                if self.state == AgentState.ERROR_RECOVERY:
                    self.context.error_count += 1
                    if self.context.has_too_many_errors():
                        await self.trigger(AgentEvent.EMERGENCY_TRIGGERED)
                    else:
                        await asyncio.sleep(2)
                        await self.trigger(AgentEvent.RECOVERY_SUCCESS)
                elif self.state == AgentState.EMERGENCY_STOP:
                    await self._cancel_source.token.wait_for_cancellation()
                    break
                else:
                    await asyncio.sleep(0.5)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error("Runtime loop error: %s", e)
                self.context.error_count += 1
                if self.context.has_too_many_errors():
                    await self._force_state(AgentState.EMERGENCY_STOP)
                else:
                    await self._force_state(AgentState.ERROR_RECOVERY)
        self._running = False
        logger.info("Agent runtime stopped")

    async def stop(self) -> None:
        logger.info("Shutdown requested")
        self._running = False
        await self.trigger(AgentEvent.SHUTDOWN_REQUESTED)

    def get_diagnostics(self) -> dict:
        return {
            "state": self.state.value,
            "previous_state": self.previous_state.value if self.previous_state else None,
            "running": self._running,
            "context": {
                "iteration_count": self.context.iteration_count,
                "error_count": self.context.error_count,
                "current_step": self.context.current_step,
                "elapsed_seconds": time.time() - self.context.start_time,
            },
            "transition_count": len(self._transition_history),
        }
