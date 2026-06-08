"""
JARVIS 4.5 — Memory Agent
==========================
Manages all memory operations: working, episodic, semantic, procedural.
Acts as interface between agents and the memory system.
"""

import logging
from typing import Any
from agents.base_agent import BaseAgent
from agents.message_bus import AgentMessage
from memory.memory_system import memory

logger = logging.getLogger("jarvis.agents.memory")


class MemoryAgent(BaseAgent):
    """
    Memory Agent: Memory management and retrieval.
    Capabilities: fact_storage, episode_recording, procedure_learning,
                  context_management, preference_tracking
    """

    def __init__(self):
        super().__init__(
            agent_id="memory",
            name="Memory Agent",
            description="Memory management and retrieval",
        )
        self.register_capability("fact_storage")
        self.register_capability("episode_recording")
        self.register_capability("procedure_learning")
        self.register_capability("context_management")
        self.register_capability("preference_tracking")
        self.register_capability("profile_management")

    async def handle_command(self, message: AgentMessage) -> None:
        """Handle memory commands."""
        payload = message.payload
        command = payload.get("command", "")

        try:
            if command == "learn_fact":
                category = payload.get("category", "KNOWLEDGE")
                key = payload.get("key", "")
                value = payload.get("value", "")
                mid = memory.learn_fact(category, key, value)
                await self.send_response(message.sender, {"status": "success", "memory_id": mid}, message.correlation_id)

            elif command == "recall_fact":
                category = payload.get("category")
                key = payload.get("key")
                facts = memory.recall_fact(category, key)
                await self.send_response(
                    message.sender,
                    {"status": "success", "facts": [{"category": f.category, "key": f.key, "value": f.value} for f in facts]},
                    message.correlation_id,
                )

            elif command == "record_episode":
                session_id = payload.get("session_id", "")
                action = payload.get("action", "")
                content = payload.get("content", "")
                result = payload.get("result", "")
                eid = memory.record_episode(session_id, action, content, result)
                await self.send_response(message.sender, {"status": "success", "episode_id": eid}, message.correlation_id)

            elif command == "update_preference":
                key = payload.get("key", "")
                value = payload.get("value", "")
                mid = memory.update_preference(key, value)
                await self.send_response(message.sender, {"status": "success", "memory_id": mid}, message.correlation_id)

            elif command == "get_profile":
                profile = memory.get_user_profile()
                prefs = memory.get_preferences()
                await self.send_response(
                    message.sender,
                    {"status": "success", "profile": profile, "preferences": prefs},
                    message.correlation_id,
                )

            elif command == "working_set":
                key = payload.get("key", "")
                value = payload.get("value", "")
                ttl = payload.get("ttl", 300)
                memory.working_set(key, value, ttl)
                await self.send_response(message.sender, {"status": "success"}, message.correlation_id)

            elif command == "working_get":
                key = payload.get("key", "")
                value = memory.working_get(key)
                await self.send_response(message.sender, {"status": "success", "value": value}, message.correlation_id)

            elif command == "cleanup":
                stats = memory.cleanup()
                await self.send_response(message.sender, {"status": "success", "cleanup": stats}, message.correlation_id)

            else:
                await self.send_response(message.sender, {"status": "error", "error": f"Unknown command: {command}"}, message.correlation_id)

        except Exception as e:
            logger.error(f"Memory agent error: {e}")
            await self.send_response(message.sender, {"status": "error", "error": str(e)}, message.correlation_id)
