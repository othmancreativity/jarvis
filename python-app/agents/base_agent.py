from __future__ import annotations

import asyncio
import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Any

from agents.message_bus import AgentMessage, MessageType, message_bus

logger = logging.getLogger("jarvis.agents.base")


class AgentStatus(str, Enum):
    INITIALIZING = "initializing"
    READY = "ready"
    BUSY = "busy"
    ERROR = "error"
    DEGRADED = "degraded"
    STOPPED = "stopped"


@dataclass
class AgentHealth:
    status: str = "initializing"
    last_heartbeat: float = 0.0
    messages_processed: int = 0
    errors_count: int = 0
    avg_response_ms: float = 0.0
    uptime_seconds: float = 0.0


class BaseAgent(ABC):
    def __init__(self, agent_id: str, name: str, description: str = "") -> None:
        self.agent_id = agent_id
        self.name = name
        self.description = description
        self.status = AgentStatus.INITIALIZING
        self.health = AgentHealth()
        self._start_time = time.time()
        self._running = False
        self._task: Optional[asyncio.Task] = None
        self._message_count = 0
        self._response_times: list[float] = []
        self._capabilities: list[str] = []

    @property
    def capabilities(self) -> list[str]:
        return self._capabilities

    def register_capability(self, capability: str) -> None:
        if capability not in self._capabilities:
            self._capabilities.append(capability)

    async def initialize(self) -> bool:
        try:
            self.status = AgentStatus.READY
            self.health.status = self.status.value
            self.health.last_heartbeat = time.time()
            await message_bus.subscribe(self.agent_id, self._handle_message)
            logger.info("Agent %s (%s) initialized", self.name, self.agent_id)
            return True
        except Exception as e:
            self.status = AgentStatus.ERROR
            self.health.status = self.status.value
            logger.error("Agent %s initialization failed: %s", self.name, e)
            return False

    async def start(self) -> None:
        self._running = True
        self._task = asyncio.create_task(self._run_loop())
        logger.info("Agent %s started", self.name)

    async def stop(self) -> None:
        self._running = False
        self.status = AgentStatus.STOPPED
        self.health.status = self.status.value
        if self._task and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("Agent %s stopped", self.name)

    async def _run_loop(self) -> None:
        while self._running:
            try:
                self.health.uptime_seconds = time.time() - self._start_time
                self.health.last_heartbeat = time.time()
                if self._response_times:
                    self.health.avg_response_ms = sum(self._response_times[-50:]) / len(self._response_times[-50:])
                await asyncio.sleep(30)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error("Agent %s loop error: %s", self.name, e)
                self.health.errors_count += 1

    async def _handle_message(self, message: AgentMessage) -> None:
        start = time.time()
        self._message_count += 1
        self.health.messages_processed = self._message_count

        try:
            if message.type == MessageType.COMMAND:
                await self.handle_command(message)
        except Exception as e:
            logger.error("Error handling message in %s: %s", self.name, e)
            self.health.errors_count += 1

        elapsed = (time.time() - start) * 1000
        self._response_times.append(elapsed)

    @abstractmethod
    async def handle_command(self, message: AgentMessage) -> None:
        pass

    async def send_response(self, to: str, payload: dict,
                            correlation_id: str = "") -> None:
        response = AgentMessage(
            sender=self.agent_id,
            recipient=to,
            type=MessageType.RESPONSE,
            payload=payload,
            correlation_id=correlation_id,
        )
        await message_bus.send(response)

    def get_info(self) -> dict:
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "description": self.description,
            "status": self.status.value,
            "capabilities": self._capabilities,
            "health": {
                "status": self.health.status,
                "messages_processed": self.health.messages_processed,
                "errors": self.health.errors_count,
                "avg_response_ms": round(self.health.avg_response_ms, 1),
                "uptime_seconds": round(self.health.uptime_seconds, 0),
            },
        }


class BasePlanningAgent(BaseAgent):
    def __init__(self, agent_id: str, name: str, description: str = "") -> None:
        super().__init__(agent_id, name, description)
        self._plan_history: list[dict] = []

    async def _execute_plan(self, plan: list[dict], execution_id: str = "") -> list[dict]:
        results = []
        for step in plan:
            try:
                tool_name = step.get("tool", "")
                params = step.get("params", {})
                result = await self._execute_tool(tool_name, params)
                results.append({
                    "step": step.get("step", 0),
                    "tool": tool_name,
                    "result": result,
                    "status": result.get("status", "unknown"),
                })
                if result.get("status") in ("blocked", "error") and step.get("critical", False):
                    break
                await asyncio.sleep(0.1)
            except Exception as e:
                results.append({
                    "step": step.get("step", 0),
                    "tool": step.get("tool", ""),
                    "result": {"status": "error", "error": str(e)},
                    "status": "error",
                })
        return results

    async def _execute_tool(self, tool_name: str, params: dict) -> dict:
        from core.tool_registry import registry
        tool = registry.get(tool_name)
        if not tool:
            return {"status": "error", "error": f"Unknown tool: {tool_name}"}
        if not tool.handler:
            return {"status": "success", "note": f"Tool {tool_name} has no handler registered"}

        for attempt in range(tool.max_retries + 1):
            try:
                result = await tool.handler(params)
                return result if isinstance(result, dict) else {"status": "success", "data": result}
            except Exception as e:
                if attempt < tool.max_retries:
                    await asyncio.sleep(2 ** attempt)
                    continue
                return {"status": "error", "error": str(e)}
        return {"status": "error", "error": "Max retries exceeded"}

    def _record_plan(self, plan: dict, success: bool) -> None:
        self._plan_history.append({"plan": plan, "success": success, "timestamp": time.time()})
        if len(self._plan_history) > 50:
            self._plan_history.pop(0)
