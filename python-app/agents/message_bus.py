"""
JARVIS 4.5 — Agent Message Bus
===============================
Standardized inter-agent communication protocol.
All agents send and receive messages through this bus.
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
import uuid
from enum import Enum
from dataclasses import dataclass, field, asdict
from typing import Optional, Any, Callable
from collections import defaultdict, deque

logger = logging.getLogger("jarvis.agents.bus")


class MessageType(str, Enum):
    """Types of inter-agent messages."""
    COMMAND = "command"
    QUERY = "query"
    RESPONSE = "response"
    EVENT = "event"
    ERROR = "error"
    BROADCAST = "broadcast"
    HEARTBEAT = "heartbeat"
    STATUS = "status"


class MessagePriority(int, Enum):
    """Message priority levels."""
    CRITICAL = 0
    HIGH = 1
    NORMAL = 2
    LOW = 3


@dataclass
class AgentMessage:
    """Standard message format for inter-agent communication."""
    id: str = ""
    sender: str = ""          # Agent ID
    recipient: str = ""       # Agent ID or "*" for broadcast
    type: str = ""
    payload: dict = field(default_factory=dict)
    priority: int = 2         # NORMAL
    timestamp: float = field(default_factory=time.time)
    correlation_id: str = ""  # Links requests to responses
    ttl: int = 60             # Time to live in seconds

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())[:8]

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "sender": self.sender,
            "recipient": self.recipient,
            "type": self.type,
            "payload": self.payload,
            "priority": self.priority,
            "timestamp": self.timestamp,
            "correlation_id": self.correlation_id,
            "ttl": self.ttl,
        }

    @classmethod
    def from_dict(cls, data: dict) -> AgentMessage:
        return cls(
            id=data.get("id", ""),
            sender=data.get("sender", ""),
            recipient=data.get("recipient", ""),
            type=data.get("type", ""),
            payload=data.get("payload", {}),
            priority=data.get("priority", 2),
            timestamp=data.get("timestamp", time.time()),
            correlation_id=data.get("correlation_id", ""),
            ttl=data.get("ttl", 60),
        )

    def is_expired(self) -> bool:
        return (time.time() - self.timestamp) > self.ttl


class MessageBus:
    """
    Central message bus for inter-agent communication.
    Supports: direct messaging, broadcasting, request-response patterns.
    """

    def __init__(self):
        self._subscribers: dict[str, list[Callable]] = defaultdict(list)
        self._queues: dict[str, asyncio.Queue] = {}
        self._pending_requests: dict[str, asyncio.Future] = {}
        self._history: deque[AgentMessage] = deque(maxlen=500)
        self._lock = asyncio.Lock()

    async def subscribe(self, agent_id: str, handler: Callable[[AgentMessage], Any]) -> None:
        """Subscribe an agent to receive messages."""
        async with self._lock:
            self._subscribers[agent_id].append(handler)
            if agent_id not in self._queues:
                self._queues[agent_id] = asyncio.Queue(maxsize=1000)

    async def unsubscribe(self, agent_id: str, handler: Callable) -> None:
        """Unsubscribe an agent."""
        async with self._lock:
            if agent_id in self._subscribers:
                self._subscribers[agent_id] = [h for h in self._subscribers[agent_id] if h != handler]

    async def send(self, message: AgentMessage) -> bool:
        """
        Send a message to a specific agent or broadcast.
        Returns True if delivered.
        """
        if message.is_expired():
            return False

        self._history.append(message)

        # Handle response to pending request
        if message.type == MessageType.RESPONSE and message.correlation_id:
            future = self._pending_requests.pop(message.correlation_id, None)
            if future and not future.done():
                future.set_result(message)
                return True

        # Direct message
        if message.recipient and message.recipient != "*":
            handlers = self._subscribers.get(message.recipient, [])
            for handler in handlers:
                try:
                    if asyncio.iscoroutinefunction(handler):
                        asyncio.create_task(handler(message))
                    else:
                        handler(message)
                except Exception as e:
                    logger.error(f"Message handler error: {e}")
            return len(handlers) > 0

        # Broadcast
        if message.recipient == "*":
            for agent_id, handlers in self._subscribers.items():
                if agent_id != message.sender:
                    for handler in handlers:
                        try:
                            if asyncio.iscoroutinefunction(handler):
                                asyncio.create_task(handler(message))
                            else:
                                handler(message)
                        except Exception as e:
                            logger.error(f"Broadcast handler error: {e}")
            return True

        return False

    async def request(self, sender: str, recipient: str, payload: dict,
                      timeout: float = 30.0) -> Optional[AgentMessage]:
        """
        Send a request and wait for response.
        Returns the response message or None on timeout.
        """
        correlation_id = str(uuid.uuid4())[:8]
        future = asyncio.get_event_loop().create_future()
        self._pending_requests[correlation_id] = future

        message = AgentMessage(
            sender=sender,
            recipient=recipient,
            type=MessageType.COMMAND,
            payload=payload,
            priority=MessagePriority.NORMAL,
            correlation_id=correlation_id,
        )

        await self.send(message)

        try:
            return await asyncio.wait_for(future, timeout=timeout)
        except asyncio.TimeoutError:
            self._pending_requests.pop(correlation_id, None)
            return None

    def get_history(self, sender: Optional[str] = None,
                    recipient: Optional[str] = None,
                    limit: int = 50) -> list[AgentMessage]:
        """Get message history with optional filtering."""
        messages = list(self._history)
        if sender:
            messages = [m for m in messages if m.sender == sender]
        if recipient:
            messages = [m for m in messages if m.recipient == recipient]
        return messages[-limit:]

    def get_stats(self) -> dict:
        """Get bus statistics."""
        return {
            "subscribers": len(self._subscribers),
            "subscriber_ids": list(self._subscribers.keys()),
            "pending_requests": len(self._pending_requests),
            "history_size": len(self._history),
        }


# Singleton instance
message_bus = MessageBus()
