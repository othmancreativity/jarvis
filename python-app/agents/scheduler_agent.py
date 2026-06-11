from __future__ import annotations

import asyncio
import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Optional
from dataclasses import dataclass, field

from agents.base_agent import BaseAgent, AgentMessage
from jarvis.cross_platform_paths import paths

logger = logging.getLogger("jarvis.agents.scheduler")


@dataclass
class ScheduledTask:
    id: str
    name: str
    command: str
    interval_seconds: int
    last_run: float = 0.0
    next_run: float = 0.0
    enabled: bool = True
    run_count: int = 0


class SchedulerAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(
            agent_id="scheduler",
            name="Scheduler Agent",
            description="Task scheduling and reminders",
        )
        self.register_capability("task_scheduling")
        self.register_capability("reminders")
        self._tasks: dict[str, ScheduledTask] = {}
        self._tasks_file: Path = paths.data_dir / "scheduled_tasks.json"
        self._load_tasks()

    def _load_tasks(self) -> None:
        if self._tasks_file.exists():
            try:
                data = json.loads(self._tasks_file.read_text(encoding="utf-8"))
                for t in data:
                    task = ScheduledTask(**t)
                    self._tasks[task.id] = task
            except Exception as e:
                logger.error("Failed to load scheduled tasks: %s", e)

    def _save_tasks(self) -> None:
        self._tasks_file.parent.mkdir(parents=True, exist_ok=True)
        data = [t.__dict__ for t in self._tasks.values()]
        self._tasks_file.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")

    async def handle_command(self, message: AgentMessage) -> None:
        payload = message.payload
        command = payload.get("command", "")

        if command == "list":
            tasks = [{"id": t.id, "name": t.name, "interval": t.interval_seconds,
                      "next_run": t.next_run, "enabled": t.enabled, "run_count": t.run_count}
                     for t in self._tasks.values()]
            await self.send_response(message.sender, {"status": "success", "tasks": tasks}, message.correlation_id)
        elif command == "add":
            name = payload.get("name", "")
            cmd = payload.get("command", payload.get("cmd", ""))
            interval = payload.get("interval_seconds", 300)
            import uuid
            task = ScheduledTask(
                id=str(uuid.uuid4())[:8],
                name=name,
                command=cmd,
                interval_seconds=interval,
                next_run=time.time() + interval,
            )
            self._tasks[task.id] = task
            self._save_tasks()
            await self.send_response(message.sender, {"status": "success", "task_id": task.id}, message.correlation_id)
        else:
            await self.send_response(message.sender, {"status": "error", "error": f"Unknown command: {command}"}, message.correlation_id)

    async def _check_tasks(self) -> None:
        now = time.time()
        for task in list(self._tasks.values()):
            if task.enabled and now >= task.next_run:
                logger.info("Running scheduled task: %s", task.name)
                task.last_run = now
                task.next_run = now + task.interval_seconds
                task.run_count += 1
                self._save_tasks()
