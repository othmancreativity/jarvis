"""
JARVIS 4.5 — Agent Runtime State Machine
=========================================
Robust runtime for the AI agent with:
    - 11 defined states with valid transition matrix
    - Recovery logic for each state
    - Loop prevention with max iteration counters
    - Timeout handling for long-running operations
    - Graceful shutdown sequence
"""

from __future__ import annotations

import asyncio
import time
import logging
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Optional, Callable, Any, Coroutine
from collections import deque

logger = logging.getLogger("jarvis.runtime")


class AgentState(str, Enum):
    """Agent runtime states."""
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
    """Events that trigger state transitions."""
    USER_INPUT = "user_input"
    INTENT_CLASSIFIED = "intent_classified"
    PLAN_CREATED = "plan_created"
    EXECUTION_STARTED = "execution_started"
    EXECUTION_COMPLETE = "execution_complete"
    EXECUTION_FAILED = "execution_failed"
    TOOL_RESULT = "tool_result"
    WAITING_FOR_USER = "waiting_for_user"
    USER_RESPONDED = "user_responded"
    ERROR_OCCURRED = "error_occurred"
    RECOVERY_SUCCESS = "recovery_success"
    RECOVERY_FAILED = "recovery_failed"
    EMERGENCY_TRIGGERED = "emergency_triggered"
    SHUTDOWN_REQUESTED = "shutdown_requested"
    TIMEOUT = "timeout"
    HEARTBEAT = "heartbeat"


# Valid state transitions: current_state -> {event: next_state}
TRANSITION_MATRIX: dict[AgentState, dict[AgentEvent, AgentState]] = {
    AgentState.IDLE: {
        AgentEvent.USER_INPUT: AgentState.UNDERSTANDING,
        AgentEvent.SHUTDOWN_REQUESTED: AgentState.SHUTDOWN,
        AgentEvent.HEARTBEAT: AgentState.IDLE,
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
        AgentEvent.TOOL_RESULT: AgentState.EXECUTING,
        AgentEvent.WAITING_FOR_USER: AgentState.WAITING,
        AgentEvent.TIMEOUT: AgentState.ERROR_RECOVERY,
    },
    AgentState.WAITING: {
        AgentEvent.USER_RESPONDED: AgentState.EXECUTING,
        AgentEvent.TIMEOUT: AgentState.IDLE,
        AgentEvent.ERROR_OCCURRED: AgentState.ERROR_RECOVERY,
    },
    AgentState.MONITORING: {
        AgentEvent.USER_INPUT: AgentState.UNDERSTANDING,
        AgentEvent.HEARTBEAT: AgentState.MONITORING,
        AgentEvent.TIMEOUT: AgentState.IDLE,
        AgentEvent.SHUTDOWN_REQUESTED: AgentState.SHUTDOWN,
    },
    AgentState.LEARNING: {
        AgentEvent.HEARTBEAT: AgentState.IDLE,
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
        AgentEvent.USER_INPUT: AgentState.EMERGENCY_STOP,  # Stay in emergency
    },
    AgentState.SHUTDOWN: {
        # Terminal state — no transitions out
    },
}


@dataclass
class RuntimeContext:
    """Context maintained across the agent loop."""
    session_id: str = ""
    user_id: str = "default"
    source: str = "local"
    current_intent: str = ""
    intent_confidence: float = 0.0
    execution_plan: list[dict] = field(default_factory=list)
    current_step: int = 0
    max_steps: int = 20  # Loop prevention
    iteration_count: int = 0
    max_iterations: int = 50  # Hard loop limit
    error_count: int = 0
    max_errors: int = 5
    start_time: float = field(default_factory=time.time)
    last_activity: float = field(default_factory=time.time)
    timeout_seconds: float = 300.0  # 5 min session timeout
    metadata: dict = field(default_factory=dict)
    tool_results: list[dict] = field(default_factory=list)
    pending_confirmations: list[str] = field(default_factory=list)

    def is_timed_out(self) -> bool:
        return (time.time() - self.last_activity) > self.timeout_seconds

    def is_looping(self) -> bool:
        return self.iteration_count >= self.max_iterations

    def has_too_many_errors(self) -> bool:
        return self.error_count >= self.max_errors

    def touch(self) -> None:
        self.last_activity = time.time()


@dataclass
class StateTransition:
    """Record of a state transition."""
    from_state: AgentState
    to_state: AgentState
    event: AgentEvent
    timestamp: float
    context: Optional[str] = None


class AgentRuntime:
    """
    Agent runtime state machine with recovery logic.
    Implements the full agent loop: Observe -> Understand -> Plan -> Execute -> Verify -> Continue
    """

    def __init__(self):
        self.state = AgentState.IDLE
        self.previous_state: Optional[AgentState] = None
        self.context = RuntimeContext()
        self._transition_history: deque[StateTransition] = deque(maxlen=100)
        self._event_queue: asyncio.Queue = asyncio.Queue()
        self._handlers: dict[AgentEvent, list[Callable]] = {}
        self._state_handlers: dict[AgentState, list[Callable]] = {}
        self._running = False
        self._shutdown_event = asyncio.Event()
        self._state_change_callbacks: list[Callable[[AgentState, AgentState], None]] = []

    def on_state_change(self, callback: Callable[[AgentState, AgentState], None]) -> None:
        """Register a callback for state changes."""
        self._state_change_callbacks.append(callback)

    def on_event(self, event: AgentEvent, handler: Callable) -> None:
        """Register an event handler."""
        self._handlers.setdefault(event, []).append(handler)

    def on_enter_state(self, state: AgentState, handler: Callable) -> None:
        """Register a handler for entering a state."""
        self._state_handlers.setdefault(state, []).append(handler)

    def can_transition(self, event: AgentEvent) -> bool:
        """Check if a transition is valid from the current state."""
        transitions = TRANSITION_MATRIX.get(self.state, {})
        return event in transitions

    async def trigger(self, event: AgentEvent, data: Any = None) -> bool:
        """
        Trigger a state transition.
        Returns True if the transition was successful.
        """
        if not self.can_transition(event):
            logger.warning(f"Invalid transition: {self.state.value} -> {event.value}")
            return False

        next_state = TRANSITION_MATRIX[self.state][event]

        # Loop prevention
        if self.context.is_looping():
            logger.error(f"Loop detected: {self.context.iteration_count} iterations")
            await self._enter_state(AgentState.ERROR_RECOVERY, "loop_prevention")
            return False

        # Execute transition
        transition = StateTransition(
            from_state=self.state,
            to_state=next_state,
            event=event,
            timestamp=time.time(),
            context=str(data)[:200] if data else None,
        )
        self._transition_history.append(transition)

        self.previous_state = self.state
        self.state = next_state
        self.context.iteration_count += 1
        self.context.touch()

        # Notify callbacks
        for callback in self._state_change_callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(self.previous_state, self.state)
                else:
                    callback(self.previous_state, self.state)
            except Exception as e:
                logger.error(f"State change callback error: {e}")

        # Run event handlers
        for handler in self._handlers.get(event, []):
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(data)
                else:
                    handler(data)
            except Exception as e:
                logger.error(f"Event handler error for {event.value}: {e}")

        # Run state enter handlers
        for handler in self._state_handlers.get(next_state, []):
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(data)
                else:
                    handler(data)
            except Exception as e:
                logger.error(f"State enter handler error for {next_state.value}: {e}")

        logger.debug(f"Transition: {self.previous_state.value} --[{event.value}]--> {next_state.value}")
        return True

    async def _enter_state(self, state: AgentState, reason: str = "") -> None:
        """Force entry into a state (for error recovery)."""
        self.previous_state = self.state
        self.state = state
        for callback in self._state_change_callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(self.previous_state, self.state)
                else:
                    callback(self.previous_state, self.state)
            except Exception:
                pass

    async def run_agent_loop(self) -> None:
        """
        Main agent loop: Observe -> Understand -> Plan -> Execute -> Verify -> Continue
        """
        self._running = True
        logger.info("Agent runtime loop started")

        while self._running and self.state != AgentState.SHUTDOWN:
            try:
                # Check session timeout
                if self.context.is_timed_out() and self.state not in (
                    AgentState.IDLE, AgentState.SHUTDOWN, AgentState.EMERGENCY_STOP
                ):
                    logger.info("Session timed out, returning to idle")
                    await self.trigger(AgentEvent.TIMEOUT)
                    continue

                # State-specific behavior
                if self.state == AgentState.IDLE:
                    await asyncio.sleep(0.5)
                    # Check for queued inputs
                    if not self._event_queue.empty():
                        event = self._event_queue.get_nowait()
                        await self.trigger(event)

                elif self.state == AgentState.LISTENING:
                    await asyncio.sleep(0.5)

                elif self.state == AgentState.UNDERSTANDING:
                    # Processing user input — handled by event
                    await asyncio.sleep(0.1)

                elif self.state == AgentState.PLANNING:
                    # Creating execution plan — handled by event
                    await asyncio.sleep(0.1)

                elif self.state == AgentState.EXECUTING:
                    # Executing tools — handled by event
                    await asyncio.sleep(0.1)

                elif self.state == AgentState.WAITING:
                    # Waiting for user response
                    await asyncio.sleep(1)

                elif self.state == AgentState.MONITORING:
                    # Monitoring completed work
                    await asyncio.sleep(1)
                    # Auto-return to idle after monitoring period
                    if time.time() - self.context.last_activity > 10:
                        await self.trigger(AgentEvent.TIMEOUT)

                elif self.state == AgentState.ERROR_RECOVERY:
                    # Recovery logic
                    self.context.error_count += 1
                    if self.context.has_too_many_errors():
                        logger.error("Too many errors, shutting down")
                        await self.trigger(AgentEvent.EMERGENCY_TRIGGERED)
                    else:
                        await asyncio.sleep(2)
                        await self.trigger(AgentEvent.RECOVERY_SUCCESS)

                elif self.state == AgentState.EMERGENCY_STOP:
                    # Emergency stop — wait for shutdown
                    await self._shutdown_event.wait()

                elif self.state == AgentState.SHUTDOWN:
                    break

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Runtime loop error: {e}")
                self.context.error_count += 1
                if self.context.has_too_many_errors():
                    await self._enter_state(AgentState.EMERGENCY_STOP)
                else:
                    await self._enter_state(AgentState.ERROR_RECOVERY)

        logger.info("Agent runtime loop ended")
        self._running = False

    async def start(self) -> None:
        """Start the runtime."""
        self._running = True
        self._shutdown_event.clear()
        await self.run_agent_loop()

    async def stop(self) -> None:
        """Graceful shutdown."""
        logger.info("Shutdown requested")
        self._running = False
        await self.trigger(AgentEvent.SHUTDOWN_REQUESTED)
        self._shutdown_event.set()

    def emergency_stop(self) -> None:
        """Immediate emergency stop."""
        logger.critical("EMERGENCY STOP ACTIVATED")
        self.state = AgentState.EMERGENCY_STOP
        self._running = False
        self._shutdown_event.set()

    def queue_event(self, event: AgentEvent) -> None:
        """Queue an event for processing."""
        try:
            self._event_queue.put_nowait(event)
        except asyncio.QueueFull:
            logger.warning("Event queue full, dropping event")

    def get_transition_history(self) -> list[StateTransition]:
        """Get recent state transitions."""
        return list(self._transition_history)

    def get_diagnostics(self) -> dict:
        """Get runtime diagnostics."""
        return {
            "state": self.state.value,
            "previous_state": self.previous_state.value if self.previous_state else None,
            "running": self._running,
            "context": {
                "session_id": self.context.session_id,
                "iteration_count": self.context.iteration_count,
                "error_count": self.context.error_count,
                "current_step": self.context.current_step,
                "elapsed_seconds": time.time() - self.context.start_time,
            },
            "transition_count": len(self._transition_history),
            "queue_size": self._event_queue.qsize(),
        }
