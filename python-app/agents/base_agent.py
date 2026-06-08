"""
JARVIS 4.5 — Base Agent Class
==============================
Abstract base for all specialized agents.
Provides: lifecycle management, message handling, health monitoring.
"""

from __future__ import annotations

import asyncio
import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, Any
from enum import Enum

from agents.message_bus import AgentMessage, MessageType, message_bus

logger = logging.getLogger("jarvis.agents.base")


class AgentStatus(str, Enum):
    """Agent lifecycle states."""
    INITIALIZING = "initializing"
    READY = "ready"
    BUSY = "busy"
    ERROR = "error"
    DEGRADED = "degraded"
    STOPPED = "stopped"


@dataclass
class AgentHealth:
    """Agent health metrics."""
    status: str = "initializing"
    last_heartbeat: float = 0.0
    messages_processed: int = 0
    errors_count: int = 0
    avg_response_ms: float = 0.0
    uptime_seconds: float = 0.0


class BaseAgent(ABC):
    """
    Base class for all JARVIS agents.
    Handles message routing, health tracking, and lifecycle.
    """

    def __init__(self, agent_id: str, name: str, description: str = ""):
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
        """List of capabilities this agent provides."""
        return self._capabilities

    def register_capability(self, capability: str) -> None:
        """Register a capability."""
        if capability not in self._capabilities:
            self._capabilities.append(capability)

    async def initialize(self) -> bool:
        """Initialize the agent. Override for custom init."""
        try:
            self.status = AgentStatus.READY
            self.health.status = self.status.value
            self.health.last_heartbeat = time.time()
            await message_bus.subscribe(self.agent_id, self._handle_message)
            logger.info(f"Agent {self.name} ({self.agent_id}) initialized")
            return True
        except Exception as e:
            self.status = AgentStatus.ERROR
            self.health.status = self.status.value
            logger.error(f"Agent {self.name} initialization failed: {e}")
            return False

    async def start(self) -> None:
        """Start the agent's background task."""
        self._running = True
        self._task = asyncio.create_task(self._run_loop())
        logger.info(f"Agent {self.name} started")

    async def stop(self) -> None:
        """Stop the agent gracefully."""
        self._running = False
        self.status = AgentStatus.STOPPED
        self.health.status = self.status.value
        if self._task and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info(f"Agent {self.name} stopped")

    async def _run_loop(self) -> None:
        """Background health monitoring loop."""
        while self._running:
            try:
                self.health.uptime_seconds = time.time() - self._start_time
                self.health.last_heartbeat = time.time()

                # Calculate average response time
                if self._response_times:
                    self.health.avg_response_ms = sum(self._response_times[-50:]) / len(self._response_times[-50:])

                await asyncio.sleep(30)  # Heartbeat every 30s
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Agent {self.name} loop error: {e}")
                self.health.errors_count += 1

    async def _handle_message(self, message: AgentMessage) -> None:
        """Handle incoming messages."""
        start = time.time()
        self._message_count += 1
        self.health.messages_processed = self._message_count

        try:
            if message.type == MessageType.COMMAND:
                await self.handle_command(message)
            elif message.type == MessageType.QUERY:
                await self.handle_query(message)
            elif message.type == MessageType.EVENT:
                await self.handle_event(message)
            elif message.type == MessageType.HEARTBEAT:
                await self.handle_heartbeat(message)
            else:
                logger.debug(f"Unhandled message type: {message.type}")
        except Exception as e:
            logger.error(f"Error handling message in {self.name}: {e}")
            self.health.errors_count += 1

        elapsed = (time.time() - start) * 1000
        self._response_times.append(elapsed)

    @abstractmethod
    async def handle_command(self, message: AgentMessage) -> None:
        """Handle command messages. Must be implemented by subclasses."""
        pass

    async def handle_query(self, message: AgentMessage) -> None:
        """Handle query messages. Override if needed."""
        pass

    async def handle_event(self, message: AgentMessage) -> None:
        """Handle event messages. Override if needed."""
        pass

    async def handle_heartbeat(self, message: AgentMessage) -> None:
        """Handle heartbeat messages. Override if needed."""
        pass

    async def send_response(self, to: str, payload: dict,
                            correlation_id: str = "") -> None:
        """Send a response message."""
        response = AgentMessage(
            sender=self.agent_id,
            recipient=to,
            type=MessageType.RESPONSE,
            payload=payload,
            correlation_id=correlation_id,
        )
        await message_bus.send(response)

    def get_info(self) -> dict:
        """Get agent information."""
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
