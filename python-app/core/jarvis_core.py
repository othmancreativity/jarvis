"""
JARVIS 4.5 — Central Orchestrator
===================================
The "brain" of JARVIS. Coordinates all agents, manages the agent runtime state
machine, handles the continuous agent loop, and integrates with the UI.

Responsibilities:
    - Receive intent from user (text, voice, command)
    - Classify intent and route to appropriate agent(s)
    - Manage the agent runtime lifecycle
    - Coordinate multi-step plans
    - Handle errors and recovery
    - Maintain session state
    - Report status to UI
"""

from __future__ import annotations

import asyncio
import logging
import time
import uuid
from typing import Optional, Callable, Any, Coroutine
from dataclasses import dataclass, field

from core.agent_runtime import AgentRuntime, AgentState, AgentEvent, RuntimeContext
from core.tool_registry import registry
from agents.planner_agent import PlannerAgent
from agents.execution_agent import ExecutionAgent
from agents.browser_agent import BrowserAgent
from agents.memory_agent import MemoryAgent
from agents.vision_agent import VisionAgent
from agents.coding_agent import CodingAgent
from agents.google_agent import GoogleAgent
from agents.security_agent import SecurityAgent
from agents.scheduler_agent import SchedulerAgent
from agents.message_bus import message_bus, AgentMessage, MessageType
from security.permissions import permission_engine
from memory.memory_system import memory

logger = logging.getLogger("jarvis.core")


@dataclass
class Session:
    """A user session."""
    id: str
    start_time: float = field(default_factory=time.time)
    last_activity: float = field(default_factory=time.time)
    context: list[dict] = field(default_factory=list)
    max_context: int = 20
    metadata: dict = field(default_factory=dict)

    def touch(self) -> None:
        self.last_activity = time.time()

    def add_context(self, role: str, content: str) -> None:
        """Add to context with automatic trimming."""
        self.context.append({"role": role, "content": content, "timestamp": time.time()})
        # Trim to max context size, keeping system messages
        if len(self.context) > self.max_context:
            # Keep first system message and most recent messages
            system_msgs = [c for c in self.context if c.get("role") == "system"]
            other_msgs = [c for c in self.context if c.get("role") != "system"]
            keep_system = system_msgs[:1]
            keep_other = other_msgs[-(self.max_context - len(keep_system)):]
            self.context = keep_system + keep_other
        self.touch()

    def is_expired(self, timeout: float = 300) -> bool:
        return (time.time() - self.last_activity) > timeout

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "start_time": self.start_time,
            "elapsed_seconds": time.time() - self.start_time,
            "context_length": len(self.context),
            "metadata": self.metadata,
        }


@dataclass
class IntentResult:
    """Result of intent classification."""
    intent: str
    confidence: float
    target_agent: str
    params: dict = field(default_factory=dict)


class JarvisCore:
    """
    Central orchestrator for JARVIS 4.5.
    Coordinates all subsystems into a unified assistant.
    """

    def __init__(self):
        self.runtime = AgentRuntime()
        self.session: Optional[Session] = None
        self.agents: dict[str, Any] = {}
        self._running = False
        self._shutdown_event = asyncio.Event()
        self._status_callbacks: list[Callable[[str, dict], None]] = []
        self._response_callbacks: list[Callable[[str], None]] = []
        self._planner = PlannerAgent()
        self._executor = ExecutionAgent()

    def on_status_update(self, callback: Callable[[str, dict], None]) -> None:
        """Register a callback for status updates."""
        self._status_callbacks.append(callback)

    def on_response(self, callback: Callable[[str], None]) -> None:
        """Register a callback for assistant responses."""
        self._response_callbacks.append(callback)

    def _notify_status(self, status: str, data: dict = None) -> None:
        """Notify all status listeners."""
        for cb in self._status_callbacks:
            try:
                cb(status, data or {})
            except Exception as e:
                logger.error(f"Status callback error: {e}")

    def _notify_response(self, text: str) -> None:
        """Notify all response listeners."""
        for cb in self._response_callbacks:
            try:
                cb(text)
            except Exception as e:
                logger.error(f"Response callback error: {e}")

    async def initialize(self) -> bool:
        """Initialize all subsystems."""
        logger.info("JARVIS 4.5 initializing...")
        self._notify_status("initializing", {"phase": "agents"})

        # Initialize all agents
        self.agents = {
            "planner": self._planner,
            "executor": self._executor,
            "browser": BrowserAgent(),
            "memory": MemoryAgent(),
            "vision": VisionAgent(),
            "coding": CodingAgent(),
            "google": GoogleAgent(),
            "security": SecurityAgent(),
            "scheduler": SchedulerAgent(),
        }

        for name, agent in self.agents.items():
            try:
                await agent.initialize()
                logger.info(f"Agent '{name}' initialized")
            except Exception as e:
                logger.error(f"Agent '{name}' init failed: {e}")

        # Initialize permission engine
        permission_engine.set_confirmation_callback(self._request_confirmation)

        # Register runtime state change handler
        self.runtime.on_state_change(self._on_state_change)

        # Load or create default session
        self.session = Session(id=str(uuid.uuid4())[:8])
        memory.record_episode(self.session.id, "session_start", "Session initialized", "ok")

        self._notify_status("ready", {"session_id": self.session.id})
        logger.info("JARVIS 4.5 initialized successfully")
        return True

    async def _on_state_change(self, from_state: AgentState, to_state: AgentState) -> None:
        """Handle runtime state changes."""
        self._notify_status("state_change", {
            "from": from_state.value,
            "to": to_state.value,
        })

        if to_state == AgentState.ERROR_RECOVERY:
            self._notify_response("I'm encountering an issue. Let me try to recover...")
        elif to_state == AgentState.EMERGENCY_STOP:
            self._notify_response("EMERGENCY STOP activated. All operations halted.")

    def _request_confirmation(self, request) -> Any:
        """Handle permission confirmation requests."""
        # This will be overridden by UI
        from security.permissions import PermissionResult, Decision
        return PermissionResult(
            decision=Decision.ALLOW,
            request_id=request.request_id,
            tool_name=request.tool_name,
            action=request.action,
            target=request.target,
            confirmed=True,
            reason="Auto-allowed (no UI configured)",
        )

    async def process_input(self, text: str, source: str = "local") -> str:
        """
        Process user input through the full pipeline.
        This is the main entry point for user interactions.
        """
        if not self.session:
            self.session = Session(id=str(uuid.uuid4())[:8])

        self.session.touch()
        self.session.add_context("user", text)

        # 1. Trigger understanding state
        await self.runtime.trigger(AgentEvent.USER_INPUT, {"text": text, "source": source})

        # 2. Classify intent
        intent = await self._classify_intent(text)
        logger.info(f"Intent classified: {intent.intent} -> {intent.target_agent} (conf={intent.confidence:.2f})")

        await self.runtime.trigger(AgentEvent.INTENT_CLASSIFIED, intent.to_dict())

        # 3. Route to appropriate handler
        response = await self._route_intent(intent, text)

        # 4. Record in memory
        self.session.add_context("assistant", response)
        memory.record_episode(self.session.id, f"intent:{intent.intent}", text, response)

        # 5. Update runtime
        await self.runtime.trigger(AgentEvent.EXECUTION_COMPLETE)

        self._notify_response(response)
        return response

    async def _classify_intent(self, text: str) -> IntentResult:
        """Classify user intent from text."""
        text_lower = text.lower()

        # Pattern-based intent classification
        patterns = {
            "browser": ["open chrome", "open browser", "navigate to", "go to ", "visit ", "search google"],
            "screenshot": ["screenshot", "capture screen", "take a picture"],
            "system_info": ["system info", "cpu usage", "memory usage", "disk space", "how much ram"],
            "file_search": ["find file", "search for file", "locate ", "where is"],
            "file_read": ["read file", "open file", "show file", "cat ", "contents of"],
            "file_write": ["write file", "create file", "save to", "new file"],
            "shell": ["run command", "execute ", "terminal", "shell"],
            "code": ["write code", "generate code", "python script", "javascript"],
            "youtube": ["youtube", "search video", "find video"],
            "gmail": ["email", "gmail", "check mail", "send email"],
            "calendar": ["calendar", "schedule", "appointment", "meeting"],
            "drive": ["drive", "google drive", "upload file", "download file"],
            "translate": ["translate", "in arabic", "in english", "in spanish"],
            "plan": ["plan", "create a plan", "schedule tasks", "roadmap"],
            "memory": ["remember", "what did i say", "recall", "what was"],
            "app": ["open app", "launch ", "start application", "close app"],
            "ocr": ["ocr", "extract text", "read screen"],
            "help": ["help", "what can you do", "capabilities", "commands"],
        }

        for intent_name, keywords in patterns.items():
            for kw in keywords:
                if kw in text_lower:
                    return IntentResult(
                        intent=intent_name,
                        confidence=0.8,
                        target_agent=self._agent_for_intent(intent_name),
                        params={"query": text},
                    )

        # Default: general chat
        return IntentResult(
            intent="general_chat",
            confidence=0.5,
            target_agent="general",
            params={"query": text},
        )

    def _agent_for_intent(self, intent: str) -> str:
        """Map intent to target agent."""
        mapping = {
            "browser": "browser",
            "screenshot": "vision",
            "system_info": "system",
            "file_search": "executor",
            "file_read": "executor",
            "file_write": "executor",
            "shell": "executor",
            "code": "coding",
            "youtube": "google",
            "gmail": "google",
            "calendar": "google",
            "drive": "google",
            "translate": "google",
            "plan": "planner",
            "memory": "memory",
            "app": "executor",
            "ocr": "vision",
            "help": "general",
            "general_chat": "general",
        }
        return mapping.get(intent, "general")

    async def _route_intent(self, intent: IntentResult, original_text: str) -> str:
        """Route the intent to the appropriate handler."""
        await self.runtime.trigger(AgentEvent.PLAN_CREATED, {"plan": [intent.intent]})

        # Handle general chat
        if intent.target_agent == "general":
            return await self._handle_general_chat(original_text)

        # Handle via specific agent
        agent = self.agents.get(intent.target_agent)
        if not agent:
            return f"I don't have a handler for '{intent.intent}' yet."

        try:
            # Send command to agent via message bus
            response = await message_bus.request(
                sender="core",
                recipient=intent.target_agent,
                payload={"command": intent.intent, **intent.params},
                timeout=60.0,
            )

            if response:
                payload = response.payload
                if payload.get("status") == "error":
                    return f"I encountered an error: {payload.get('error', 'Unknown error')}"
                return payload.get("responseText", str(payload))
            else:
                return f"The {intent.target_agent} agent didn't respond in time."

        except Exception as e:
            logger.error(f"Error routing intent {intent.intent}: {e}")
            return f"I had trouble handling your request: {str(e)}"

    async def _handle_general_chat(self, text: str) -> str:
        """Handle general chat via LLM."""
        from config import config

        if not config.groq_api_key:
            return (
                "I'm JARVIS 4.5, your AI Operating Assistant.\n\n"
                "I can help you with:\n"
                "- Browser automation (open Chrome, navigate, screenshots)\n"
                "- File operations (search, read, write)\n"
                "- System info (CPU, memory, processes)\n"
                "- Screen capture and OCR\n"
                "- Application control\n"
                "- Google services (YouTube, Gmail, Calendar, Drive)\n"
                "- Code generation and review\n"
                "- Task planning\n\n"
                "Set GROQ_API_KEY for AI-powered responses."
            )

        try:
            import requests

            messages = [
                {"role": "system", "content": (
                    "You are JARVIS 4.5, a highly capable personal AI Operating Assistant. "
                    "You help users operate their computer, organize work, and execute tasks. "
                    "You have access to: browser control, file operations, system monitoring, "
                    "screen capture, application management, and Google services. "
                    "Be concise, helpful, and precise."
                )},
            ]
            # Add recent context
            if self.session:
                for ctx in self.session.context[-10:]:
                    messages.append({"role": ctx["role"], "content": ctx["content"]})

            resp = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {config.groq_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": config.model,
                    "messages": messages,
                    "temperature": 0.3,
                    "max_tokens": 2000,
                },
                timeout=30,
            )
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]

        except Exception as e:
            logger.error(f"LLM error: {e}")
            return f"I'm having trouble connecting to the language model: {str(e)}"

    async def run_scheduler(self) -> None:
        """Background task to run the scheduler agent's task checker."""
        scheduler = self.agents.get("scheduler")
        if not scheduler:
            return

        while self._running:
            try:
                await scheduler._check_tasks()
                await asyncio.sleep(5)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Scheduler error: {e}")
                await asyncio.sleep(10)

    async def run(self) -> None:
        """Main run loop — starts runtime and background tasks."""
        self._running = True
        logger.info("JARVIS 4.5 core starting...")

        # Start scheduler background task
        scheduler_task = asyncio.create_task(self.run_scheduler())

        # Start agent runtime loop
        runtime_task = asyncio.create_task(self.runtime.start())

        # Wait for shutdown
        await self._shutdown_event.wait()

        # Cleanup
        scheduler_task.cancel()
        runtime_task.cancel()
        try:
            await asyncio.gather(scheduler_task, runtime_task, return_exceptions=True)
        except Exception:
            pass

        self._running = False
        logger.info("JARVIS 4.5 core stopped")

    async def stop(self) -> None:
        """Graceful shutdown."""
        logger.info("Shutdown requested")
        self._running = False
        await self.runtime.stop()
        self._shutdown_event.set()

    def emergency_stop(self) -> None:
        """Immediate emergency stop."""
        self.runtime.emergency_stop()
        self._notify_status("emergency_stop", {})

    def get_status(self) -> dict:
        """Get full system status."""
        return {
            "runtime": self.runtime.get_diagnostics(),
            "session": self.session.to_dict() if self.session else None,
            "agents": {name: agent.get_info() for name, agent in self.agents.items()},
            "tools_registered": registry.count,
            "memory": memory.get_stats(),
        }
