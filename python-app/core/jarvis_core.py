from __future__ import annotations

import asyncio
import json
import logging
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional, Callable, Any

from core.agent_runtime import AgentRuntime, AgentState, AgentEvent
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
from jarvis.cancellation_token import CancellationTokenSource
from jarvis.local_llm import local_llm, LocalLLM
from jarvis.browser_pool import pool as browser_pool
from jarvis.cross_platform_paths import paths

logger = logging.getLogger("jarvis.core")


@dataclass
class Session:
    id: str
    start_time: float = field(default_factory=time.time)
    last_activity: float = field(default_factory=time.time)
    context: list[dict] = field(default_factory=list)
    max_context: int = 20
    metadata: dict = field(default_factory=dict)
    message_count: int = 0

    def touch(self) -> None:
        self.last_activity = time.time()

    def add_context(self, role: str, content: str) -> None:
        self.context.append({"role": role, "content": content, "timestamp": time.time()})
        self.message_count += 1
        if len(self.context) > self.max_context:
            system_msgs = [c for c in self.context if c.get("role") == "system"]
            other_msgs = [c for c in self.context if c.get("role") != "system"]
            keep_system = system_msgs[:1]
            keep_other = other_msgs[-(self.max_context - len(keep_system)):]
            self.context = keep_system + keep_other
        self.touch()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "start_time": self.start_time,
            "last_activity": self.last_activity,
            "context": self.context[-10:],
            "message_count": self.message_count,
            "metadata": self.metadata,
        }


@dataclass
class IntentResult:
    intent: str
    confidence: float
    target_agent: str
    params: dict = field(default_factory=dict)


class JarvisCore:
    def __init__(self) -> None:
        self.runtime: AgentRuntime = AgentRuntime()
        self.session: Optional[Session] = None
        self.agents: dict[str, Any] = {}
        self._running = False
        self._cancel_source: CancellationTokenSource = CancellationTokenSource()
        self._status_callbacks: list[Callable[[str, dict], None]] = []
        self._response_callbacks: list[Callable[[str], None]] = []
        self._planner = PlannerAgent()
        self._executor = ExecutionAgent()

    def on_status_update(self, callback: Callable[[str, dict], None]) -> None:
        self._status_callbacks.append(callback)

    def on_response(self, callback: Callable[[str], None]) -> None:
        self._response_callbacks.append(callback)

    def _notify_status(self, status: str, data: dict = None) -> None:
        for cb in self._status_callbacks:
            try:
                cb(status, data or {})
            except Exception as e:
                logger.error("Status callback error: %s", e)

    def _notify_response(self, text: str) -> None:
        for cb in self._response_callbacks:
            try:
                cb(text)
            except Exception as e:
                logger.error("Response callback error: %s", e)

    async def initialize(self) -> bool:
        logger.info("JARVIS 4.6 initializing...")
        self._notify_status("initializing", {"phase": "agents"})

        await local_llm.check_availability()
        logger.info("Local LLM available: %s", local_llm.is_available)

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
                logger.info("Agent '%s' initialized", name)
            except Exception as e:
                logger.error("Agent '%s' init failed: %s", name, e)

        self.runtime.on_state_change(self._on_state_change)
        self.session = Session(id=str(uuid.uuid4())[:8])
        self._load_checkpoint()
        self._notify_status("ready", {"session_id": self.session.id})
        logger.info("JARVIS 4.6 initialized successfully")
        return True

    async def _on_state_change(self, from_state: AgentState, to_state: AgentState) -> None:
        self._notify_status("state_change", {"from": from_state.value, "to": to_state.value})
        if to_state == AgentState.ERROR_RECOVERY:
            self._notify_response("I encountered an issue. Let me recover...")
        elif to_state == AgentState.EMERGENCY_STOP:
            self._notify_response("EMERGENCY STOP activated. All operations halted.")

    def _load_checkpoint(self) -> None:
        checkpoint_dir = paths.checkpoint_dir
        checkpoints = sorted(checkpoint_dir.glob("checkpoint_*.json"))
        if checkpoints:
            try:
                data = json.loads(checkpoints[-1].read_text(encoding="utf-8"))
                if self.session:
                    self.session.metadata = data.get("metadata", {})
                    self.session.message_count = data.get("message_count", 0)
                    ctx = data.get("context", [])
                    if ctx:
                        self.session.context = ctx
                    logger.info("Loaded checkpoint from %s", checkpoints[-1].name)
            except Exception as e:
                logger.error("Failed to load checkpoint: %s", e)

    def _save_checkpoint(self) -> None:
        if not self.session:
            return
        checkpoint_dir = paths.checkpoint_dir
        checkpoint_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = checkpoint_dir / f"checkpoint_{timestamp}.json"
        try:
            path.write_text(
                json.dumps(self.session.to_dict(), indent=2, default=str),
                encoding="utf-8",
            )
            checkpoints = sorted(checkpoint_dir.glob("checkpoint_*.json"))
            while len(checkpoints) > 10:
                checkpoints[0].unlink()
                checkpoints = checkpoints[1:]
        except Exception as e:
            logger.error("Failed to save checkpoint: %s", e)

    async def process_input(self, text: str, source: str = "local") -> str:
        if not self.session:
            self.session = Session(id=str(uuid.uuid4())[:8])

        self.session.touch()
        self.session.add_context("user", text)

        if self.session.message_count > 0 and self.session.message_count % 5 == 0:
            self._save_checkpoint()

        await self.runtime.trigger(AgentEvent.USER_INPUT, {"text": text, "source": source})

        intent = await self._classify_intent(text)
        logger.info("Intent classified: %s -> %s (conf=%.2f)", intent.intent, intent.target_agent, intent.confidence)

        await self.runtime.trigger(AgentEvent.INTENT_CLASSIFIED, intent.__dict__)

        response = await self._route_intent(intent, text)

        self.session.add_context("assistant", response)

        await self.runtime.trigger(AgentEvent.EXECUTION_COMPLETE)

        self._notify_response(response)
        return response

    async def _classify_intent(self, text: str) -> IntentResult:
        text_lower = text.lower()
        patterns = {
            "browser": ["open chrome", "open browser", "navigate to", "go to ", "visit ", "search google", "browser"],
            "screenshot": ["screenshot", "capture screen", "take a picture"],
            "system_info": ["system info", "cpu usage", "memory usage", "disk space", "how much ram", "system information"],
            "file_search": ["find file", "search for file", "locate ", "where is"],
            "file_read": ["read file", "open file", "show file", "cat ", "contents of"],
            "file_write": ["write file", "create file", "save to", "new file"],
            "shell": ["run command", "execute ", "terminal", "shell", "command"],
            "code": ["write code", "generate code", "python script", "javascript", "code"],
            "youtube": ["youtube", "search video", "find video"],
            "gmail": ["email", "gmail", "check mail", "send email"],
            "calendar": ["calendar", "schedule", "appointment", "meeting"],
            "translate": ["translate", "in arabic", "in english", "in spanish"],
            "plan": ["plan", "create a plan", "schedule tasks", "roadmap", "plan"],
            "memory": ["remember", "what did i say", "recall", "what was", "do you remember"],
            "app": ["open app", "launch ", "start application", "close app"],
            "ocr": ["ocr", "extract text", "read screen"],
            "help": ["help", "what can you do", "capabilities", "commands", "menu"],
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
        return IntentResult(
            intent="general_chat",
            confidence=0.5,
            target_agent="general",
            params={"query": text},
        )

    def _agent_for_intent(self, intent: str) -> str:
        mapping = {
            "browser": "browser", "screenshot": "vision", "system_info": "system",
            "file_search": "executor", "file_read": "executor", "file_write": "executor",
            "shell": "executor", "code": "coding", "youtube": "google", "gmail": "google",
            "calendar": "google", "translate": "google", "plan": "planner", "memory": "memory",
            "app": "executor", "ocr": "vision", "help": "general", "general_chat": "general",
        }
        return mapping.get(intent, "general")

    async def _route_intent(self, intent: IntentResult, original_text: str) -> str:
        await self.runtime.trigger(AgentEvent.PLAN_CREATED, {"plan": [intent.intent]})

        if intent.target_agent == "general":
            return await self._handle_general_chat(original_text)

        agent = self.agents.get(intent.target_agent)
        if not agent:
            return f"I don't have a handler for '{intent.intent}' yet."

        try:
            response = await message_bus.request(
                sender="core",
                recipient=intent.target_agent,
                payload={"command": intent.intent, **intent.params},
                timeout=60.0,
            )
            if response:
                payload = response.payload
                if payload.get("status") == "error":
                    return f"Error: {payload.get('error', 'Unknown error')}"
                return payload.get("responseText", str(payload))
            return f"The {intent.target_agent} agent didn't respond in time."
        except asyncio.CancelledError:
            return "Operation was cancelled."
        except Exception as e:
            logger.error("Error routing intent %s: %s", intent.intent, e)
            return f"Error handling your request: {e}"

    async def _handle_general_chat(self, text: str) -> str:
        try:
            import requests
            from config import config

            messages = [
                {"role": "system", "content": (
                    "You are JARVIS 4.6, a highly capable personal AI Operating Assistant. "
                    "You help users operate their computer, organize work, and execute tasks. "
                    "Be concise, helpful, and precise."
                )},
            ]
            if self.session:
                for ctx in self.session.context[-10:]:
                    messages.append({"role": ctx["role"], "content": ctx["content"]})

            if config.groq_api_key:
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

            if local_llm.is_available:
                result = await local_llm.generate(messages)
                if result:
                    return result

            return (
                "I'm JARVIS 4.6, your AI Operating Assistant.\n\n"
                "I can help with:\n"
                "- Browser automation (open, navigate, screenshot)\n"
                "- File operations (search, read, write)\n"
                "- System info (CPU, memory, processes)\n"
                "- Screen capture and OCR\n"
                "- Application control\n"
                "- Code generation\n"
                "- Task planning\n"
                "- Google services (YouTube, Gmail, Calendar)\n\n"
                "Set GROQ_API_KEY or install Ollama for AI-powered responses."
            )
        except requests.exceptions.ConnectionError:
            if local_llm.is_available:
                result = await local_llm.generate(messages)
                if result:
                    return result
            return "I'm offline and cannot connect to the AI model."
        except Exception as e:
            logger.error("LLM error: %s", e)
            if local_llm.is_available:
                result = await local_llm.generate(messages)
                if result:
                    return result
            return f"Error connecting to the language model: {e}"

    async def run_scheduler(self) -> None:
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
                logger.error("Scheduler error: %s", e)
                await asyncio.sleep(10)

    async def run(self) -> None:
        self._running = True
        logger.info("JARVIS 4.6 core starting...")
        scheduler_task = asyncio.create_task(self.run_scheduler())
        runtime_task = asyncio.create_task(self.runtime.start())

        try:
            await asyncio.gather(
                scheduler_task,
                runtime_task,
                return_exceptions=True,
            )
        except asyncio.CancelledError:
            pass

        self._running = False
        logger.info("JARVIS 4.6 core stopped")

    async def stop(self) -> None:
        logger.info("Shutdown requested")
        self._save_checkpoint()
        self._running = False
        await self.runtime.stop()
        await browser_pool.close_all()

    def emergency_stop(self) -> None:
        logger.critical("Emergency stop triggered")
        self.runtime.emergency_stop()
        self._cancel_source.cancel()
        self._notify_status("emergency_stop", {})

    def get_status(self) -> dict:
        return {
            "runtime": self.runtime.get_diagnostics(),
            "session": self.session.to_dict() if self.session else None,
            "agents": {name: agent.get_info() for name, agent in self.agents.items()},
            "browser_pool": browser_pool.stats,
            "local_llm_available": local_llm.is_available,
        }
