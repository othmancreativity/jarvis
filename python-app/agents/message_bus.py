from __future__ import annotations

import asyncio
import logging
import time
import uuid
from collections import defaultdict, deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Any, Callable

logger = logging.getLogger("jarvis.agents.bus")


class MessageType(str, Enum):
    COMMAND = "command"
    QUERY = "query"
    RESPONSE = "response"
    EVENT = "event"
    ERROR = "error"
    BROADCAST = "broadcast"
    HEARTBEAT = "heartbeat"


class MessagePriority(int, Enum):
    CRITICAL = 0
    HIGH = 1
    NORMAL = 2
    LOW = 3


@dataclass
class AgentMessage:
    id: str = ""
    sender: str = ""
    recipient: str = ""
    type: str = ""
    payload: dict = field(default_factory=dict)
    priority: int = 2
    timestamp: float = field(default_factory=time.time)
    correlation_id: str = ""
    ttl: int = 60

    def __post_init__(self) -> None:
        if not self.id:
            self.id = str(uuid.uuid4())[:8]

    def is_expired(self) -> bool:
        return (time.time() - self.timestamp) > self.ttl


class MessageBus:
    def __init__(self) -> None:
        self._subscribers: dict[str, list[Callable]] = defaultdict(list)
        self._pending_requests: dict[str, asyncio.Future] = {}
        self._history: deque[AgentMessage] = deque(maxlen=500)
        self._lock = asyncio.Lock()

    async def subscribe(self, agent_id: str, handler: Callable[[AgentMessage], Any]) -> None:
        async with self._lock:
            self._subscribers[agent_id].append(handler)

    async def unsubscribe(self, agent_id: str, handler: Callable) -> None:
        async with self._lock:
            if agent_id in self._subscribers:
                self._subscribers[agent_id] = [h for h in self._subscribers[agent_id] if h != handler]

    async def send(self, message: AgentMessage) -> bool:
        if message.is_expired():
            return False

        self._history.append(message)

        if message.type == MessageType.RESPONSE and message.correlation_id:
            future = self._pending_requests.pop(message.correlation_id, None)
            if future and not future.done():
                future.set_result(message)
                return True

        if message.recipient and message.recipient != "*":
            handlers = self._subscribers.get(message.recipient, [])
            for handler in handlers:
                try:
                    if asyncio.iscoroutinefunction(handler):
                        asyncio.create_task(handler(message))
                    else:
                        handler(message)
                except Exception as e:
                    logger.error("Message handler error: %s", e)
            return len(handlers) > 0

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
                            logger.error("Broadcast handler error: %s", e)
            return True

        return False

    async def request(self, sender: str, recipient: str, payload: dict,
                      timeout: float = 30.0) -> Optional[AgentMessage]:
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

    def get_stats(self) -> dict:
        return {
            "subscribers": len(self._subscribers),
            "subscriber_ids": list(self._subscribers.keys()),
            "pending_requests": len(self._pending_requests),
            "history_size": len(self._history),
        }


message_bus = MessageBus()
