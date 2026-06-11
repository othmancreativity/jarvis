# JARVIS 4.6 Internal API Documentation

## Architecture Overview

JARVIS 4.6 is a multi-agent AI assistant built on:

- **JarvisCore** (`core/jarvis_core.py`): Central orchestrator, async event loop, session management
- **AgentRuntime** (`core/agent_runtime.py`): State machine with 11 states and transition matrix
- **MessageBus** (`agents/message_bus.py`): Inter-agent pub/sub communication
- **BaseAgent/BasePlanningAgent** (`agents/base_agent.py`): Abstract agent lifecycle
- **9 Specialized Agents**: Planner, Execution, Browser, Memory, Vision, Coding, Google, Security, Scheduler
- **Automation Layer** (`automation/`): Browser, Apps, Files, Shell, Screen, System info
- **Memory System** (`memory/`): Working (LRU), Episodic (SQLite), Semantic (SQLite + vector), Procedural
- **Security Subsystem** (`security/`): Permission engine, RSA audit signing, input validation
- **Utility modules** (`jarvis/`): Cancellation tokens, browser pool, local LLM, backup, sleep, plugins, updater

## Core Classes

### `JarvisCore`

Main entry point for all interactions.

```python
core = JarvisCore()
await core.initialize()
response = await core.process_input("open browser")
await core.stop()
```

**Methods:**
- `initialize() -> bool` — Initialize all agents, load checkpoint, check local LLM
- `process_input(text, source) -> str` — Classify intent, route to agent, return response
- `emergency_stop()` — Cancel all tasks via CancellationTokenSource
- `get_status() -> dict` — Runtime diagnostics, agent health, browser pool stats
- `run() / stop()` — Start/stop the main event loop

### `Session`

User session with checkpointing.

```python
session = Session(id="abc123")
session.add_context("user", "hello")
session.to_dict()  # Serializable for checkpoint save
```

Checkpoints saved every 5 messages to `~/.jarvis/data/checkpoints/` (last 10 kept).

### `AgentRuntime`

State machine with valid transition matrix.

States: `IDLE -> UNDERSTANDING -> PLANNING -> EXECUTING -> MONITORING -> IDLE`

**Methods:**
- `trigger(event, data) -> bool` — Attempt state transition
- `emergency_stop()` — Force EMERGENCY_STOP state, cancel all

### `BaseAgent`

Abstract agent class with message subscription, health tracking, heartbeat.

```python
class MyAgent(BaseAgent):
    async def handle_command(self, message: AgentMessage):
        await self.send_response(sender, {payload}, correlation_id)
```

### `BasePlanningAgent(BaseAgent)`

Extends BaseAgent with `_execute_plan()` and `_execute_tool()` for multi-step execution.

## Message Bus

Agents communicate via `message_bus` singleton:

```python
from agents.message_bus import message_bus, AgentMessage, MessageType

# Subscribe
await message_bus.subscribe("agent_id", handler_func)

# Request-response
response = await message_bus.request(sender, recipient, payload, timeout=30.0)

# Send
await message_bus.send(AgentMessage(sender="a", recipient="b", type=MessageType.COMMAND, payload={}))
```

## Memory System

### `memory` (singleton)

```python
from memory.memory_system import memory

memory.working_set("key", value, ttl_seconds=300)
value = memory.working_get("key")
memory.learn_fact("PREFERENCE", "theme", "dark")
facts = memory.recall_fact(category="PREFERENCE")
memory.record_episode("session1", "action", "content", "ok")
```

### `SemanticMemory`

Vector-based semantic search using sentence-transformers + FAISS.

```python
from agents.memory_agent import SemanticMemory

sm = SemanticMemory()
await sm.initialize()
sm.add_memory("text to remember", {"metadata": "value"})
results = sm.search("query", top_k=3)
```

## Browser Pool

```python
from jarvis.browser_pool import pool

async with await pool.acquire() as browser:
    page = browser.page
    await page.goto("https://example.com")
```

## Cancellation Token

```python
from jarvis.cancellation_token import CancellationTokenSource

cts = CancellationTokenSource()
token = cts.token
# ... in another task ...
cts.cancel()
# ... check ...
token.throw_if_cancellation_requested()
```

## Security

### Permission Levels

- `SAFE` — Always allowed
- `CONFIRM_REQUIRED` — Ask user or deny
- `UNSAFE` — Denied by default unless whitelisted

### Permission Engine

```python
from security.permissions import permission_engine, PermissionRequest, PermissionLevel

req = PermissionRequest(request_id="r1", tool_name="file.delete", action="delete", target="/tmp/x", risk_level="high", permission_level="confirm_required")
result = permission_engine.check_permission(req)
```

### Audit Logger (RSA-signed)

```python
from security.audit import audit_logger, AuditEventType

audit_logger.log(AuditEventType.COMMAND, "shell.execute", target="ls -la")
```

## Automation Modules

### ShellController

```python
from automation.shell import ShellController

ctrl = ShellController()
result = await ctrl.execute("ls -la", timeout=30)
```

Returns `{"status", "returncode", "stdout", "stderr", "duration_ms"}`.

### BrowserController

```python
from automation.browser import BrowserController

ctrl = BrowserController()
await ctrl.open("https://example.com")
```

### AppController / FileController / ScreenController / SystemInfoController

Similar pattern — create instance, call `async` methods, get dict results.

## Plugin System

```python
from jarvis.plugin_manager import plugin_manager, plugin_tool, plugin_task

@plugin_tool
def my_tool(param: str) -> dict:
    return {"status": "success"}
```

Place in `plugins/` directory. Auto-discovered on startup.

## Backup Manager

```python
from jarvis.backup_manager import backup_manager

backup_manager.create_backup()  # -> Path
backup_manager.restore_backup(Path("backup.zip"))
backup_manager.list_backups()   # -> list[dict]
```

## Sleep Manager

```python
from jarvis.sleep_manager import sleep_manager

sleep_manager.register_sleep(lambda: print("going to sleep"))
sleep_manager.register_wake(lambda: print("waking up"))
sleep_manager.start()
```

## CLI Usage

```bash
python cli.py send "open browser"
python cli.py status
python cli.py backup create
python cli.py config get model
python cli.py update
```

## Testing

```bash
cd python-app
pytest tests/ -v --cov=jarvis --cov=core --cov=agents --cov=security
```
