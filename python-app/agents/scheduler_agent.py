"""
JARVIS 4.5 — Scheduler Agent
=============================
Manages scheduled tasks, reminders, and recurring operations.
Provides: schedule_task, cancel_task, list_tasks, recurring_jobs
"""

import asyncio
import logging
import time
from typing import Any, Optional
from dataclasses import dataclass, field
from agents.base_agent import BaseAgent
from agents.message_bus import AgentMessage

logger = logging.getLogger("jarvis.agents.scheduler")


@dataclass
class ScheduledTask:
    """A scheduled task."""
    id: str
    name: str
    trigger_time: float
    action: str
    params: dict = field(default_factory=dict)
    recurring: bool = False
    interval_seconds: float = 0
    executed: bool = False


class SchedulerAgent(BaseAgent):
    """
    Scheduler Agent: Task scheduling and reminders.
    Capabilities: schedule_task, cancel_task, list_tasks, recurring_jobs
    """

    def __init__(self):
        super().__init__(
            agent_id="scheduler",
            name="Scheduler Agent",
            description="Task scheduling and reminders",
        )
        self.register_capability("schedule_task")
        self.register_capability("cancel_task")
        self.register_capability("list_tasks")
        self.register_capability("recurring_jobs")
        self._tasks: dict[str, ScheduledTask] = {}
        self._task_counter = 0

    async def handle_command(self, message: AgentMessage) -> None:
        """Handle scheduler commands."""
        payload = message.payload
        command = payload.get("command", "")

        if command == "schedule":
            name = payload.get("name", "")
            delay = payload.get("delay_seconds", 0)
            action = payload.get("action", "")
            params = payload.get("params", {})
            recurring = payload.get("recurring", False)
            interval = payload.get("interval_seconds", 0)

            self._task_counter += 1
            task_id = f"task_{self._task_counter}_{int(time.time())}"
            task = ScheduledTask(
                id=task_id,
                name=name,
                trigger_time=time.time() + delay,
                action=action,
                params=params,
                recurring=recurring,
                interval_seconds=interval,
            )
            self._tasks[task_id] = task
            await self.send_response(message.sender, {"status": "scheduled", "task_id": task_id}, message.correlation_id)

        elif command == "cancel":
            task_id = payload.get("task_id", "")
            if task_id in self._tasks:
                del self._tasks[task_id]
                await self.send_response(message.sender, {"status": "cancelled"}, message.correlation_id)
            else:
                await self.send_response(message.sender, {"status": "error", "error": "Task not found"}, message.correlation_id)

        elif command == "list":
            tasks = [
                {
                    "id": t.id,
                    "name": t.name,
                    "trigger_time": t.trigger_time,
                    "action": t.action,
                    "recurring": t.recurring,
                }
                for t in self._tasks.values()
                if not t.executed
            ]
            await self.send_response(message.sender, {"status": "success", "tasks": tasks}, message.correlation_id)

    async def _check_tasks(self) -> None:
        """Check for tasks that need execution."""
        now = time.time()
        for task in list(self._tasks.values()):
            if not task.executed and task.trigger_time <= now:
                task.executed = True
                logger.info(f"Executing scheduled task: {task.name}")
                # Here you would dispatch to the appropriate agent
                if task.recurring:
                    task.trigger_time = now + task.interval_seconds
                    task.executed = False
