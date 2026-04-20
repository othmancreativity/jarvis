# 🗂️ JARVIS — Task Board
> Every task has: INPUT, OUTPUT, FILES, SUCCESS CRITERIA.
> Build in phase order. Each phase has a runnable end state.
> **Start with Phase 0. Do not move to Phase 1 until Phase 0 passes.**

---

## 📊 Progress

| Phase | Name | Tasks | Done |
|-------|------|-------|------|
| 0 | Vertical Slice | 5 | 0 |
| 1 | Foundation | 7 | 0 |
| 2 | Runtime Loop | 8 | 0 |
| 3 | Memory | 6 | 0 |
| 4 | CLI Interface | 5 | 0 |
| 5 | Tool System | 5 | 0 |
| 6 | System Control Skills | 7 | 0 |
| 7 | Browser & Web Skills | 6 | 0 |
| 8 | Google APIs | 6 | 0 |
| 9 | Agents | 5 | 0 |
| 10 | Task Decomposition | 5 | 0 |
| 11 | Feedback Loop | 4 | 0 |
| 12 | Web UI | 7 | 0 |
| 13 | Voice Pipeline | 5 | 0 |
| 14 | Vision & Image Gen | 4 | 0 |
| 15 | Telegram + GUI | 4 | 0 |
| 16 | QA + Security | 6 | 0 |
| 17 | Personality | 3 | 0 |

---

## 🚀 Phase 0 — Vertical Slice
> **End state:** User types "open chrome" → Chrome opens. Nothing else required.
> This phase proves the full pipe works before building anything else.

---

### TASK 0.1 — Minimal Ollama chat call

**INPUT:** String "hello"
**OUTPUT:** String response from qwen3:8b printed to terminal
**FILES:** `src/models/llm/engine.py` (create)

```python
import ollama

def chat(message: str, model: str = "qwen3:8b") -> str:
    response = ollama.chat(model=model, messages=[{"role": "user", "content": message}])
    return response["message"]["content"]

if __name__ == "__main__":
    print(chat("hello"))
```

**SUCCESS:** `python src/models/llm/engine.py` prints a coherent response. No errors.

---

### TASK 0.2 — Minimal intent classifier

**INPUT:** String "open chrome"
**OUTPUT:** `{"intent": "tool_use", "tool": "open_app", "args": {"name": "chrome"}}`
**FILES:** `src/core/decision/classifier.py` (create)

Use `gemma3:4b` with a system prompt that forces JSON output:

```python
SYSTEM = """You are a command classifier.
Given a user message, return ONLY valid JSON:
{"intent": "chat|tool_use|code|search", "tool": "tool_name_or_null", "args": {}}

Examples:
"open chrome" -> {"intent": "tool_use", "tool": "open_app", "args": {"name": "chrome"}}
"what is AI?" -> {"intent": "chat", "tool": null, "args": {}}
"افتح Chrome" -> {"intent": "tool_use", "tool": "open_app", "args": {"name": "chrome"}}
"""

def classify(message: str) -> dict:
    import json
    raw = chat(message, model="gemma3:4b", system=SYSTEM)
    return json.loads(raw)
```

**SUCCESS:** Both `classify("open chrome")` and `classify("افتح Chrome")` return `{"intent": "tool_use", "tool": "open_app", "args": {"name": "chrome"}}`.

---

### TASK 0.3 — Minimal app launcher

**INPUT:** `{"name": "chrome"}`
**OUTPUT:** Chrome opens. `{"success": True, "pid": 1234}`
**FILES:** `src/skills/system/apps.py` (create)

```python
import subprocess, shutil, os
from pathlib import Path

def open_app(name: str) -> dict:
    # 1. Try PATH
    path = shutil.which(name)
    if path:
        proc = subprocess.Popen([path])
        return {"success": True, "pid": proc.pid}

    # 2. Search Windows program directories
    search_dirs = [
        os.environ.get("PROGRAMFILES", "C:/Program Files"),
        os.environ.get("PROGRAMFILES(X86)", "C:/Program Files (x86)"),
        os.environ.get("LOCALAPPDATA", ""),
    ]
    for d in search_dirs:
        if not d:
            continue
        for root, _, files in os.walk(d):
            for f in files:
                if name.lower() in f.lower() and f.endswith(".exe"):
                    proc = subprocess.Popen([os.path.join(root, f)])
                    return {"success": True, "pid": proc.pid}

    return {"success": False, "error": f"App '{name}' not found"}
```

**SUCCESS:** `open_app("chrome")` opens Chrome. `open_app("notepad")` opens Notepad.

---

### TASK 0.4 — Wire: classifier → tool → output

**INPUT:** String from `input()` in terminal
**OUTPUT:** App opens + confirmation printed
**FILES:** `app/jarvis_slice.py` (create, temporary)

```python
import json
from src.models.llm.engine import chat
from src.skills.system.apps import open_app
from src.core.decision.classifier import classify

def run(user_input: str):
    decision = classify(user_input)

    if decision["intent"] == "tool_use" and decision["tool"] == "open_app":
        result = open_app(decision["args"]["name"])
        print(f"✓ {result}")
    else:
        print(f"Jarvis: {chat(user_input)}")

if __name__ == "__main__":
    run(input("You: "))
```

**SUCCESS:** Type "open notepad" → Notepad opens + confirmation printed.

---

### TASK 0.5 — Arabic input test

**INPUT:** "افتح Chrome" typed at prompt
**OUTPUT:** Chrome opens (same as 0.4)
**FILES:** No new files — test existing code

**SUCCESS:** Arabic command produces same result as English. If not, add Arabic examples to classifier system prompt until it does.

---

## 🏗️ Phase 1 — Foundation
> **End state:** `python app/main.py --interface cli` starts without crashing. Config loads. Logging works. All `__init__.py` files exist.

---

### TASK 1.1 — Config system

**INPUT:** `config/settings.yaml` file
**OUTPUT:** `AppSettings` Python object importable anywhere
**FILES:** `config/settings.example.yaml` (create), `config/settings.yaml` (create), `src/core/config.py` (create)

Minimum `settings.example.yaml`:
```yaml
jarvis:
  name: "Jarvis"
  language: ["ar", "en"]
  wake_word: "hey_jarvis"

models:
  default: "qwen3:8b"
  fast: "gemma3:4b"
  code: "qwen2.5-coder:7b"
  vision: "llava:7b"

hardware:
  gpu_vram_limit_gb: 5.5
  max_concurrent_models: 1

interfaces:
  web_port: 8080
  web_host: "127.0.0.1"

paths:
  data: "data"
  logs: "logs"

hotkeys:
  open_cli: "ctrl+alt+j"
  start_voice: "ctrl+alt+s"
```

`src/core/config.py`: Pydantic model that loads from YAML via `get_settings()` singleton.

**SUCCESS:** `from src.core.config import get_settings; assert get_settings().jarvis.name == "Jarvis"` passes.

---

### TASK 1.2 — Logging setup

**INPUT:** Call to `setup_logging()` at startup
**OUTPUT:** Logs appear in terminal AND `logs/jarvis.log` with daily rotation
**FILES:** `src/core/logging_setup.py` (create)

```python
from loguru import logger
from pathlib import Path

def setup_logging(level: str = "INFO"):
    Path("logs").mkdir(exist_ok=True)
    logger.add("logs/jarvis.log", rotation="10 MB", retention="7 days", level=level,
               format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")
```

**SUCCESS:** `setup_logging()` then `logger.info("test")` writes to both terminal and `logs/jarvis.log`.

---

### TASK 1.3 — Package skeleton

**INPUT:** Nothing
**OUTPUT:** All `src/` subdirectories exist with `__init__.py`
**FILES:** Create all directories + `__init__.py` files

Required directories:
```
src/core/context/   src/core/decision/   src/core/runtime/
src/core/agents/    src/core/memory/     src/core/tools/
src/core/identity/  src/models/llm/      src/models/vision/
src/models/speech/  src/models/diffusion/
src/skills/files/   src/skills/system/   src/skills/browser/
src/skills/search/  src/skills/social/   src/skills/api/
src/skills/pdf/     src/skills/office/   src/skills/screen/
src/skills/notify/  src/skills/coder/
src/interfaces/cli/ src/interfaces/web/  src/interfaces/voice/
src/interfaces/telegram/ src/interfaces/gui/
```

**SUCCESS:** `python -c "from src.core.decision import classifier"` raises ImportError only for missing module content, not for missing package.

---

### TASK 1.4 — Model capability profiles

**INPUT:** `config/models.yaml` with 4 model entries
**OUTPUT:** `get_model_profile("qwen3:8b")` returns dict with all capability fields
**FILES:** `config/models.yaml` (create), `src/models/profiles.py` (create)

```yaml
# config/models.yaml
qwen3:8b:
  temperature: 0.6
  max_tokens: 8192
  vram_gb: 5.0
  arabic_quality: 0.95
  code_bias: 0.5
  reasoning: "high"
  latency: "medium"

gemma3:4b:
  temperature: 0.6
  max_tokens: 2048
  vram_gb: 3.0
  arabic_quality: 0.85
  code_bias: 0.35
  reasoning: "low"
  latency: "fast"

qwen2.5-coder:7b:
  temperature: 0.3
  max_tokens: 8192
  vram_gb: 4.7
  arabic_quality: 0.75
  code_bias: 0.95
  reasoning: "medium"
  latency: "fast"

llava:7b:
  temperature: 0.4
  max_tokens: 2048
  vram_gb: 4.5
  vision: true
  latency: "medium"
```

**SUCCESS:** `get_model_profile("qwen3:8b")["vram_gb"] == 5.0` passes.

---

### TASK 1.5 — LLM engine with VRAM guard

**INPUT:** model name + messages
**OUTPUT:** Response text; VRAM guard prevents loading two heavy models
**FILES:** `src/models/llm/engine.py` (expand from Phase 0)

Add:
- `get_active_model() → str | None`
- `unload_current_model()` — call Ollama API to stop model
- `swap_to(model: str)` — unload current if different, load new

**SUCCESS:** `swap_to("gemma3:4b")` then `swap_to("qwen3:8b")` does not crash. Active model tracker is accurate after each swap.

---

### TASK 1.6 — Identity: system prompt builder

**INPUT:** `config/jarvis_identity.yaml` + user profile dict
**OUTPUT:** System prompt string ready to prepend to any LLM call
**FILES:** `config/jarvis_identity.yaml` (create), `src/core/identity/builder.py` (create)

```yaml
# config/jarvis_identity.yaml
name: "Jarvis"
role: "Personal AI assistant"
safety_rules:
  - "Never expose credentials, API keys, or file system secrets"
  - "Admit uncertainty rather than fabricate information"
  - "Confirm before destructive actions"
```

```python
def build_system_prompt(task_context: str = "", mode: str = "normal") -> str:
    identity = load_jarvis_identity()
    user = load_user_profile()
    return f"""You are {identity.name}, {identity.role}.
Rules: {'; '.join(identity.safety_rules)}
User: {user.name} | Language: {user.language} | Style: {user.style}
Task: {task_context}
Mode: {mode}
You are a component of the Jarvis system. Respond as Jarvis, not as the underlying model."""
```

**SUCCESS:** `build_system_prompt("open chrome", "fast")` returns a non-empty string. Changing `mode` changes the output string.

---

### TASK 1.7 — main.py entry point

**INPUT:** `--interface cli` argument
**OUTPUT:** "Jarvis ready." printed; waits for input; clean exit on Ctrl+C
**FILES:** `app/main.py` (create)

```python
import argparse
from src.core.config import get_settings
from src.core.logging_setup import setup_logging

def main():
    parser = argparse.ArgumentParser(prog="jarvis")
    parser.add_argument("--interface", choices=["cli","web","voice","telegram","gui","all"],
                        default="cli")
    args = parser.parse_args()
    setup_logging()
    cfg = get_settings()

    if args.interface == "cli":
        from src.interfaces.cli.interface import run_cli
        run_cli(cfg)
    elif args.interface == "web":
        from src.interfaces.web.app import run_web
        run_web(cfg)
    # ... other interfaces

if __name__ == "__main__":
    main()
```

**SUCCESS:** `python app/main.py --interface cli` prints "Jarvis ready." and accepts input. Ctrl+C exits cleanly with no traceback.

---

## 🔄 Phase 2 — Runtime Loop
> **End state:** Text input → Decision → correct LLM → text output. No tools yet. Just the core loop.

---

### TASK 2.1 — Context assembler

**INPUT:** `user_message: str`, `session_id: str`
**OUTPUT:** `ContextBundle` Pydantic model
**FILES:** `src/core/context/assembler.py` (create)

```python
class ContextBundle(BaseModel):
    user_message: str
    session_id: str
    attachments: list = []      # images, files — populated in Phase 14
    tool_results: list = []     # from previous tool calls
    memory_snippets: list = []  # injected in Phase 3
    turn_number: int = 1
```

**SUCCESS:** `assemble_context("hello", "s1")` returns `ContextBundle` with correct fields.

---

### TASK 2.2 — Decision layer

**INPUT:** `ContextBundle`
**OUTPUT:** `DecisionOutput` Pydantic model
**FILES:** `src/core/decision/decision.py` (create)

```python
class DecisionOutput(BaseModel):
    intent: str          # "chat" | "tool_use" | "code" | "search" | "vision"
    complexity: str      # "low" | "medium" | "high"
    mode: str            # "fast" | "normal" | "deep" | "planning"
    model: str           # exact ollama model tag
    requires_tools: bool
    requires_planning: bool
    tool_name: str | None = None
    tool_args: dict = {}

def decide(context: ContextBundle) -> DecisionOutput:
    # Use gemma3:4b for classification (fast, cheap)
    # For simple short messages: skip LLM call, default to chat/fast/gemma3
    # For complex or tool-needing: call classifier
    ...
```

**SUCCESS:**
- `decide(ctx("what time is it?"))` → `intent="chat"`, `model="gemma3:4b"`
- `decide(ctx("write a Python web scraper"))` → `intent="code"`, `model="qwen2.5-coder:7b"`
- `decide(ctx("افتح Chrome"))` → `intent="tool_use"`, `tool_name="open_app"`

---

### TASK 2.3 — Runtime executor

**INPUT:** `ContextBundle` + `DecisionOutput`
**OUTPUT:** `Generator[str]` — streams response tokens
**FILES:** `src/core/runtime/executor.py` (create)

```python
def execute(context: ContextBundle, decision: DecisionOutput) -> Generator[str, None, None]:
    system = build_system_prompt(context.user_message, decision.mode)

    if decision.requires_tools:
        # Tool execution added in Phase 5
        yield "[tool execution not yet implemented]"
        return

    for token in stream_chat(decision.model, system, context.user_message):
        yield token
```

**SUCCESS:** `list(execute(ctx, dec))` returns a list of string tokens that concatenate to a coherent answer.

---

### TASK 2.4 — Evaluator

**INPUT:** `response: str`, `context: ContextBundle`
**OUTPUT:** `EvalResult(quality: float, should_retry: bool, reason: str)`
**FILES:** `src/core/runtime/evaluator.py` (create)

Heuristic-based (no extra LLM call at this stage):
- Empty response → `quality=0.0, retry=True`
- Response < 10 chars on `complexity="high"` → `quality=0.3, retry=True`
- Otherwise → `quality=0.8, retry=False`

**SUCCESS:** `evaluate("", ctx)` → `should_retry=True`. `evaluate("Paris is the capital of France.", ctx)` → `should_retry=False`.

---

### TASK 2.5 — Safety gate

**INPUT:** `tool_name: str`, `args: dict`
**OUTPUT:** `SafetyResult(level: str, allowed: bool | None, reason: str)`
**FILES:** `src/core/tools/safety.py` (create)

```python
SAFE = "safe"
RISKY = "risky"      # requires user confirmation
CRITICAL = "critical" # blocked

RISKY_TOOLS = {"open_app", "run_shell", "send_email", "execute_code"}
CRITICAL_TOOLS = {"delete_file", "kill_process", "format_disk"}
BLOCKED_PATTERNS = ["rm -rf", "format c:", "del /s /q", ":(){:|:&};:"]

def classify_safety(tool_name: str, args: dict) -> SafetyResult:
    if tool_name in CRITICAL_TOOLS:
        return SafetyResult(level=CRITICAL, allowed=False, reason="Requires explicit authorization")
    args_str = str(args).lower()
    for p in BLOCKED_PATTERNS:
        if p in args_str:
            return SafetyResult(level=CRITICAL, allowed=False, reason=f"Blocked pattern: {p}")
    if tool_name in RISKY_TOOLS:
        return SafetyResult(level=RISKY, allowed=None, reason="Confirm before executing")
    return SafetyResult(level=SAFE, allowed=True, reason="")
```

**SUCCESS:** `classify_safety("delete_file", {})` → `allowed=False`. `classify_safety("web_search", {})` → `allowed=True`.

---

### TASK 2.6 — Full turn loop

**INPUT:** `user_input: str` from terminal
**OUTPUT:** Streamed answer printed; retry fires if quality low
**FILES:** `src/core/runtime/loop.py` (create)

```python
def run_turn(user_input: str, session_id: str) -> str:
    context = assemble_context(user_input, session_id)
    decision = decide(context)

    response_tokens = []
    for token in execute(context, decision):
        print(token, end="", flush=True)
        response_tokens.append(token)
    print()
    response = "".join(response_tokens)

    eval_result = evaluate(response, context)
    if eval_result.should_retry and decision.complexity != "low":
        # One retry with deeper model
        decision.model = "qwen3:8b"
        decision.mode = "deep"
        response_tokens = []
        for token in execute(context, decision):
            print(token, end="", flush=True)
            response_tokens.append(token)
        print()
        response = "".join(response_tokens)

    return response
```

**SUCCESS:**
- `run_turn("ما هو الذكاء الاصطناعي؟", "s1")` prints coherent Arabic answer.
- `run_turn("write a Python function to reverse a string", "s1")` uses `qwen2.5-coder:7b` (check logs).
- Empty response triggers retry (verify by logging model used on retry).

---

### TASK 2.7 — EventBus

**INPUT:** Event name + data dict
**OUTPUT:** All subscribers for that event receive the data
**FILES:** `src/core/events.py` (create)

```python
from collections import defaultdict
from typing import Callable

class EventBus:
    def __init__(self):
        self._handlers: dict[str, list[Callable]] = defaultdict(list)

    def subscribe(self, event: str, handler: Callable):
        self._handlers[event].append(handler)

    def emit(self, event: str, data: dict = {}):
        for h in self._handlers[event]:
            h(data)

bus = EventBus()  # singleton, import from here
```

Emit these events in `run_turn()`: `turn.start`, `decision.made`, `turn.end`, `eval.retry`.

**SUCCESS:** Subscribe to `turn.end`, call `run_turn()`, verify handler fires with `{"response": "..."}`.

---

### TASK 2.8 — Structured logging for runtime

**INPUT:** Runtime events
**OUTPUT:** Structured log entries in `logs/jarvis.log`
**FILES:** `src/core/runtime/loop.py` (modify)

Add to `run_turn()`:
```python
logger.info("turn.start session={} input_len={}", session_id, len(user_input))
logger.info("decision intent={} model={} mode={}", decision.intent, decision.model, decision.mode)
logger.info("turn.end response_len={} quality={}", len(response), eval_result.quality)
```

**SUCCESS:** After 3 turns, `logs/jarvis.log` has 9 entries (3 per turn) with correct field values.

---

## 💾 Phase 3 — Memory
> **End state:** Facts from session 1 recalled in session 2. User profile persists across restarts.

---

### TASK 3.1 — Short-term memory

**INPUT:** `role: str`, `content: str`, `session_id: str`
**OUTPUT:** Message saved; `get_history(session_id)` returns ordered list
**FILES:** `src/core/memory/short_term.py` (create)

In-memory dict + optional Redis backend. Max 50 messages per session. Token-aware trimming: drop oldest when limit exceeded.

**SUCCESS:** Save 3 messages, call `get_history()`, receive all 3 in order. Restart with Redis enabled → history still present.

---

### TASK 3.2 — Long-term semantic memory

**INPUT:** `text: str`, `metadata: dict`
**OUTPUT:** Stored in ChromaDB; `recall("AI news")` returns relevant snippets
**FILES:** `src/core/memory/long_term.py` (create)

```python
import chromadb
from uuid import uuid4

client = chromadb.PersistentClient(path="data/chroma")
col = client.get_or_create_collection("jarvis_memory")

def remember(text: str, metadata: dict = {}):
    col.add(documents=[text], metadatas=[metadata], ids=[uuid4().hex])

def recall(query: str, n: int = 5) -> list[str]:
    results = col.query(query_texts=[query], n_results=n)
    return results["documents"][0] if results["documents"] else []
```

**SUCCESS:** `remember("User prefers concise Arabic answers")`. Restart Python. `recall("user preferences")` returns that text in top-5.

---

### TASK 3.3 — SQLite store

**INPUT:** SQL operations via wrapper
**OUTPUT:** Data persists; queryable across restarts
**FILES:** `src/core/memory/database.py` (create)

Tables:
- `conversations(id, session_id, role, content, timestamp)`
- `facts(id, text, source, created_at)`
- `feedback(id, session_id, model, score, timestamp)`
- `tasks(id, run_id, title, status, result, created_at)`

**SUCCESS:** Insert 1 row in each table. Restart. Query all 4 tables — rows present.

---

### TASK 3.4 — User profile

**INPUT:** Key-value preferences
**OUTPUT:** Saved to `data/user_profile.json`; loadable at startup
**FILES:** `src/core/memory/user_profile.py` (create)

```python
DEFAULT_PROFILE = {
    "name": "User",
    "language": "ar",
    "style": "balanced",          # concise | balanced | detailed
    "tone": "casual",             # formal | casual | warm
    "technical_level": "intermediate",
}

def load_profile() -> dict:
    path = Path("data/user_profile.json")
    if path.exists():
        return json.loads(path.read_text())
    return DEFAULT_PROFILE

def save_profile(updates: dict):
    profile = load_profile()
    profile.update(updates)
    Path("data/user_profile.json").write_text(json.dumps(profile, indent=2))
```

**SUCCESS:** `save_profile({"language": "en"})`. Restart. `load_profile()["language"] == "en"`.

---

### TASK 3.5 — Inject memory into Context

**INPUT:** `user_message + session_id`
**OUTPUT:** `ContextBundle` with `memory_snippets` populated
**FILES:** `src/core/context/assembler.py` (modify)

Modify `assemble_context()`:
1. `get_history(session_id)` → last 10 messages → add to bundle
2. `recall(user_message, n=3)` → top semantic matches → add to bundle
3. `load_profile()` → attach to bundle

**SUCCESS:** Tell Jarvis "my name is Ahmed" in turn 1. Turn 2: "what's my name?" → returns "Ahmed" without explicit context passing.

---

### TASK 3.6 — Auto-save after every turn

**INPUT:** Completed turn
**OUTPUT:** User message + response saved to short-term + SQLite
**FILES:** `src/core/runtime/loop.py` (modify)

End of `run_turn()`:
```python
save_interaction(session_id, "user", user_input)
save_interaction(session_id, "assistant", response)
```

**SUCCESS:** Run 5 turns. SQLite `conversations` table has 10 rows.

---

## 💻 Phase 4 — CLI Interface
> **End state:** `python app/main.py --interface cli` shows Rich chat UI. Arabic RTL. Slash commands work.

---

### TASK 4.1 — Rich chat loop

**INPUT:** User types in terminal
**OUTPUT:** Formatted streaming chat display
**FILES:** `src/interfaces/cli/interface.py` (create)

Use `rich.console` and `rich.live` for streaming display. Detect Arabic text (>30% Arabic chars) and align right.

**SUCCESS:** Chat works. Arabic input renders RTL. English input renders LTR. Ctrl+C exits cleanly.

---

### TASK 4.2 — Slash commands

**INPUT:** Commands starting with `/`
**OUTPUT:** Command executes; result displayed
**FILES:** `src/interfaces/cli/commands.py` (create)

| Command | Action | Confirmation? |
|---------|--------|--------------|
| `/clear` | Clear session history | Yes |
| `/model qwen3:8b` | Switch model for session | No |
| `/mode deep` | Switch thinking mode | No |
| `/memory` | Print last 5 memories | No |
| `/tools` | List all tools with status | No |
| `/status` | Model, mode, session stats | No |
| `/help` | All commands with descriptions | No |

**SUCCESS:** All 7 commands execute without error.

---

### TASK 4.3 — Global hotkeys

**INPUT:** Ctrl+Alt+J pressed anywhere on system
**OUTPUT:** CLI window brought to focus
**FILES:** `src/interfaces/cli/hotkeys.py` (create)

```python
import keyboard

def register_hotkeys():
    keyboard.add_hotkey("ctrl+alt+j", bring_cli_to_focus)
    keyboard.add_hotkey("ctrl+alt+s", trigger_voice_input)
```

Run in background thread at startup.

**SUCCESS:** CLI running. Press Ctrl+Alt+J from another window. CLI comes to focus.

---

### TASK 4.4 — Input history

**INPUT:** Arrow up/down keys
**OUTPUT:** Previous inputs recalled
**FILES:** `src/interfaces/cli/interface.py` (modify)

Store inputs in `data/cli_history.txt`. Use `prompt_toolkit` or readline history.

**SUCCESS:** Type 3 messages. Press up 3 times. All 3 recalled in reverse order. History survives restart.

---

### TASK 4.5 — Status bar

**INPUT:** Current state after each turn
**OUTPUT:** One-line bar: `[model: qwen3:8b] [mode: normal] [turn: 5]`
**FILES:** `src/interfaces/cli/interface.py` (modify)

**SUCCESS:** Status bar updates after every turn with correct model, mode, and turn count.

---

## 🛠️ Phase 5 — Tool System
> **End state:** Any skill in `src/skills/` is auto-discovered, validated, and callable by the LLM.

---

### TASK 5.1 — BaseTool contract

**INPUT:** Python class extending BaseTool
**OUTPUT:** Tool discoverable and executable by registry
**FILES:** `src/core/tools/base.py` (create)

```python
from abc import ABC, abstractmethod
from pydantic import BaseModel

class ToolResult(BaseModel):
    success: bool
    data: dict = {}
    error: str = ""
    duration_ms: float = 0

class BaseTool(ABC):
    name: str
    description: str
    category: str
    requires_confirmation: bool = False

    @abstractmethod
    def execute(self, **kwargs) -> ToolResult: ...

    def is_available(self) -> bool:
        return True

    @classmethod
    def to_ollama_tool(cls) -> dict:
        return {
            "type": "function",
            "function": {
                "name": cls.name,
                "description": cls.description,
                "parameters": cls.get_schema()
            }
        }
```

**SUCCESS:** Create dummy `class TestTool(BaseTool)` with `execute()`. `isinstance(TestTool(), BaseTool)` is True.

---

### TASK 5.2 — Tool registry with auto-discovery

**INPUT:** `src/skills/` directory
**OUTPUT:** All available tools registered; exportable as Ollama tool list
**FILES:** `src/core/tools/registry.py` (create)

```python
import importlib, pkgutil, inspect
from src.core.tools.base import BaseTool

class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, BaseTool] = {}

    def discover(self):
        import src.skills as skills_pkg
        for _, modname, _ in pkgutil.walk_packages(skills_pkg.__path__, prefix="src.skills."):
            module = importlib.import_module(modname)
            for _, cls in inspect.getmembers(module, inspect.isclass):
                if issubclass(cls, BaseTool) and cls is not BaseTool:
                    tool = cls()
                    if tool.is_available():
                        self._tools[tool.name] = tool

    def get(self, name: str) -> BaseTool | None:
        return self._tools.get(name)

    def all_names(self) -> list[str]:
        return list(self._tools.keys())

    def to_ollama_format(self) -> list[dict]:
        return [t.to_ollama_tool() for t in self._tools.values()]

registry = ToolRegistry()
```

**SUCCESS:** `registry.discover()` finds `open_app` tool from Phase 0. `registry.get("open_app")` is not None.

---

### TASK 5.3 — Validator + executor bridge

**INPUT:** `tool_name: str`, `args: dict` (raw from LLM)
**OUTPUT:** `ToolResult`
**FILES:** `src/core/tools/executor.py` (create)

```python
def execute_tool(tool_name: str, args: dict) -> ToolResult:
    tool = registry.get(tool_name)
    if not tool:
        return ToolResult(success=False, error=f"Tool '{tool_name}' not found")

    safety = classify_safety(tool_name, args)
    if not safety.allowed:
        return ToolResult(success=False, error=f"Blocked: {safety.reason}")
    if safety.level == RISKY:
        answer = input(f"⚠️ Confirm: execute {tool_name} with {args}? [y/N] ")
        if answer.lower() != "y":
            return ToolResult(success=False, error="User declined")

    start = time.time()
    try:
        result = tool.execute(**args)
        result.duration_ms = (time.time() - start) * 1000
        logger.info("tool.done name={} success={} ms={:.0f}", tool_name, result.success, result.duration_ms)
        return result
    except Exception as e:
        logger.error("tool.error name={} error={}", tool_name, e)
        return ToolResult(success=False, error=str(e))
```

**SUCCESS:** `execute_tool("open_app", {"name": "notepad"})` opens Notepad and returns `success=True`. `execute_tool("fake", {})` returns `success=False`.

---

### TASK 5.4 — Wire tools into runtime loop

**INPUT:** `DecisionOutput` with `requires_tools=True`
**OUTPUT:** Tool runs; result fed back to LLM for final answer
**FILES:** `src/core/runtime/executor.py` (modify)

```python
if decision.requires_tools:
    tool_result = execute_tool(decision.tool_name, decision.tool_args)
    follow_up = f"Tool '{decision.tool_name}' result: {tool_result.data}\nNow answer the user's original question."
    for token in stream_chat(decision.model, system, follow_up):
        yield token
```

**SUCCESS:** "open notepad" → tool executes → LLM says "I've opened Notepad" → Notepad is open.

---

### TASK 5.5 — JSON Schema files for all tools

**INPUT:** Tool parameter definitions
**OUTPUT:** One JSON Schema file per tool in `config/schemas/`
**FILES:** `config/schemas/{category}/{tool_name}.schema.json` (one per tool)

Example `config/schemas/system/open_app.schema.json`:
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "open_app",
  "type": "object",
  "properties": {
    "name": {"type": "string", "description": "App name or executable"}
  },
  "required": ["name"]
}
```

Create schema files for all tools listed in Phases 6–8 before implementing those tools.

**SUCCESS:** Every tool in Phase 6–8 has a corresponding schema file. Executor validates args against schema before calling `execute()`.

---

## 🖥️ Phase 6 — System Control Skills
> **End state:** Jarvis opens/closes apps, manages files, reads clipboard, sends notifications, takes screenshots, and runs code.

---

### TASK 6.1 — App launcher (full Windows implementation)

**INPUT:** `{"name": "chrome"}`
**OUTPUT:** App opens. `ToolResult(success=True, data={"pid": 1234})`
**FILES:** `src/skills/system/apps.py` (expand from Phase 0)

Full search order:
1. `shutil.which(name)` — PATH
2. `%PROGRAMFILES%`, `%PROGRAMFILES(X86)%`, `%LOCALAPPDATA%` — walk for `name*.exe`
3. Start Menu `.lnk` shortcuts via `win32com.client`

Also implement:
- `close_app(name)` → `taskkill /IM {name}.exe /F` — needs confirmation
- `list_running()` → psutil list (name, PID, CPU%, RAM%)
- `bring_to_front(name)` → `SetForegroundWindow` via win32api

Register as `BaseTool` subclass so registry discovers it.

**SUCCESS:** "افتح Notepad" → Notepad opens. "أغلق Notepad" → Notepad closes.

---

### TASK 6.2 — File operations

**INPUT:** `{"operation": "read", "path": "C:/Users/test.txt"}`
**OUTPUT:** `ToolResult(data={"content": "..."})`
**FILES:** `src/skills/files/file_ops.py` (create)

Operations: `read`, `write`, `list`, `search`, `move`, `copy`, `delete`.
- `delete` → `send2trash` (recycle bin, NOT permanent) + `requires_confirmation=True`
- Path safety: reject paths outside user home and configured allowed roots
- Windows path normalization throughout

**SUCCESS:** Read/write/list/search all work. Delete sends to recycle bin (verifiable in Windows Recycle Bin UI).

---

### TASK 6.3 — System info + process control

**INPUT:** `{"metric": "all"}` or `{"action": "kill", "name": "notepad.exe"}`
**OUTPUT:** `ToolResult` with stats or kill confirmation
**FILES:** `src/skills/system/sysinfo.py` (create)

Use `psutil` for CPU/RAM/disk. Use `pynvml` for GPU VRAM. `kill_process` has `requires_confirmation=True`.

**SUCCESS:** `get_system_info()` returns valid numeric values. `kill_process` prompts, then kills target process.

---

### TASK 6.4 — Clipboard

**INPUT:** `{}` (read) or `{"text": "hello"}` (write)
**OUTPUT:** `ToolResult(data={"content": "clipboard text"})` or write confirmation
**FILES:** `src/skills/system/clipboard.py` (create)

Use `pyperclip` for text. Use `win32clipboard` for image detection. Image → save to `data/temp/clipboard_image.png` → return path.

**SUCCESS:** Copy text in any app → `read_clipboard()` returns that text. Write "test" via tool → paste in Notepad → "test" appears.

---

### TASK 6.5 — Windows notifications

**INPUT:** `{"title": "Done", "message": "Task complete", "type": "success"}`
**OUTPUT:** Windows Toast appears. `ToolResult(success=True)`
**FILES:** `src/skills/notify/toasts.py` (create)

Use `winotify`. Fallback to console print if unavailable.

**SUCCESS:** Notification appears in Windows notification center within 2 seconds of tool call.

---

### TASK 6.6 — Screen capture + OCR

**INPUT:** `{}` (full screen) or `{"region": {"x":0,"y":0,"w":800,"h":600}}`
**OUTPUT:** `ToolResult(data={"path": "data/screenshots/...", "text": "extracted text"})`
**FILES:** `src/skills/screen/capture.py` (create)

Use `mss` for capture. Use `pytesseract` for OCR (no LLM needed). Save PNG to `data/screenshots/`.

**SUCCESS:** Screenshot of window with visible text → OCR returns that text with >80% accuracy on clear fonts.

---

### TASK 6.7 — Code executor

**INPUT:** `{"language": "python", "code": "print(2+2)"}`
**OUTPUT:** `ToolResult(data={"stdout": "4\n", "stderr": "", "returncode": 0})`
**FILES:** `src/skills/coder/executor.py` (create)

Run in subprocess with 30s timeout. Block dangerous patterns (`os.remove`, `shutil.rmtree`, `sys.exit`). `requires_confirmation=True`.

**SUCCESS:** `execute_code("python", "print(2+2)")` → stdout="4\n". Dangerous pattern → blocked error returned (no execution).

---

## 🌐 Phase 7 — Browser & Web Skills
> **End state:** Jarvis navigates sites, stays logged in between restarts, downloads files, sends WhatsApp messages.

---

### TASK 7.1 — Web search

**INPUT:** `{"query": "latest AI news", "max_results": 5}`
**OUTPUT:** `ToolResult(data={"results": [{"title":..., "url":..., "snippet":...}]})`
**FILES:** `src/skills/search/web_search.py` (create)

DuckDuckGo HTML search (no API key). Parse with BeautifulSoup. TTL cache: 5 minutes for identical queries.

**SUCCESS:** Search "Python tutorial" → 5 results with valid URLs and non-empty snippets.

---

### TASK 7.2 — Browser core

**INPUT:** `{"action": "navigate", "url": "https://google.com"}`
**OUTPUT:** `ToolResult(data={"title": "Google", "url": "..."})`
**FILES:** `src/skills/browser/browser.py` (create)

Single Playwright Chromium instance (singleton). Actions: `navigate`, `click`, `fill`, `get_text`, `screenshot`, `scroll`.

**SUCCESS:** Navigate to google.com → title "Google". Fill search bar → submit → page changes.

---

### TASK 7.3 — Session persistence

**INPUT:** `domain: str`
**OUTPUT:** Session saved to `data/sessions/{domain}.json`; reloaded on next open
**FILES:** `src/skills/browser/session.py` (create)

```python
async def save_session(page, domain: str):
    state = await page.context.storage_state()
    Path(f"data/sessions/{domain}.json").write_text(json.dumps(state))

async def load_session(browser, domain: str):
    path = Path(f"data/sessions/{domain}.json")
    if path.exists():
        return await browser.new_context(storage_state=str(path))
    return await browser.new_context()
```

**SUCCESS:** Log into site → save session → kill Jarvis → restart → navigate to same site → already logged in.

---

### TASK 7.4 — File download + upload

**INPUT:** Download: `{"url": "..."}` | Upload: `{"selector": "#file-input", "path": "local.pdf"}`
**OUTPUT:** `ToolResult` with download path or upload confirmation
**FILES:** `src/skills/browser/transfer.py` (create)

Download: intercept `page.on("download")`, save to `data/downloads/`.
Upload: `page.set_input_files(selector, path)`.

**SUCCESS:** Download a public PDF → file in `data/downloads/`. Upload local file → confirmed via DOM element.

---

### TASK 7.5 — WhatsApp Web

**INPUT:** `{"action": "send", "contact": "Ahmed", "message": "Hello from Jarvis"}`
**OUTPUT:** `ToolResult(success=True)` + message visible in WhatsApp Web
**FILES:** `src/skills/social/whatsapp.py` (create)

Flow:
1. Open WhatsApp Web using saved session
2. If not logged in: screenshot QR → display in terminal → wait 30s → save session
3. Find contact via search box → type message → send

**SUCCESS:** Natural language "Send Ahmed: Meeting at 3pm" → message appears in WhatsApp chat.

---

### TASK 7.6 — Auth wall handler

**INPUT:** Currently open browser page
**OUTPUT:** Pause automation; notify user; resume on signal
**FILES:** `src/skills/browser/auth_handler.py` (create)

```python
AUTH_KEYWORDS = ["login", "sign in", "تسجيل الدخول", "captcha", "verify"]

def check_for_auth_wall(page) -> bool:
    title = page.title().lower()
    return any(kw in title or kw in page.url.lower() for kw in AUTH_KEYWORDS)

def handle_auth_wall(page):
    send_notification("Jarvis", "Login required — complete login and press Enter", "warning")
    input("Press Enter after completing login...")
    save_session(page, extract_domain(page.url))
```

**SUCCESS:** Navigate to login-required page → notification appears → user logs in → Enter → automation resumes.

---

## 🔌 Phase 8 — Google APIs
> **End state:** One OAuth consent → Calendar, Gmail, Drive, Contacts all work via natural language.

---

### TASK 8.1 — Unified Google OAuth

**INPUT:** `credentials.json` from Google Cloud Console
**OUTPUT:** `data/google_token.json` saved; all Google APIs accessible
**FILES:** `src/skills/api/google_auth.py` (create)

Combined scopes: Calendar + Gmail + Drive + Contacts + YouTube in one consent flow. Auto-refresh expired tokens. Token stored in `data/google_token.json` (gitignored).

**SUCCESS:** First run → browser opens for consent → token saved. Second run → no browser → uses saved token.

---

### TASK 8.2 — Google Calendar

**INPUT:** `{"action": "create", "title": "Meeting", "datetime": "2025-01-15T10:00:00"}`
**OUTPUT:** `ToolResult(data={"event_id": "...", "link": "..."})`
**FILES:** `src/skills/api/calendar.py` (create)

Operations: `list` (next N days), `create`, `update`, `delete`, `search`.

**SUCCESS:** Create test event → list → found. Delete → list again → gone.

---

### TASK 8.3 — Gmail

**INPUT:** `{"action": "send", "to": "test@example.com", "subject": "Test", "body": "Hello"}`
**OUTPUT:** `ToolResult(success=True, data={"message_id": "..."})`
**FILES:** `src/skills/api/gmail.py` (create)

Operations: `list` (last N), `search`, `send`, `reply`, `mark_read`, `move_to_label`.
`send` and `reply` have `requires_confirmation=True`.

**SUCCESS:** Send email to self → appears in inbox. Search for it → found. Mark as read → unread badge decreases.

---

### TASK 8.4 — Google Drive

**INPUT:** `{"action": "upload", "local_path": "data/report.pdf"}`
**OUTPUT:** `ToolResult(data={"file_id": "...", "web_link": "..."})`
**FILES:** `src/skills/api/drive.py` (create)

Operations: `list`, `search`, `upload`, `download`, `share`, `create_folder`.

**SUCCESS:** Upload local file → appears in Drive. Download it back → content matches original.

---

### TASK 8.5 — Google Contacts

**INPUT:** `{"action": "search", "query": "Ahmed"}`
**OUTPUT:** `ToolResult(data={"contacts": [{"name": "...", "email": "..."}]})`
**FILES:** `src/skills/api/contacts.py` (create)

Operations: `list`, `search`, `get`, `create`, `update`.

Integration: "Send email to Ahmed" → resolve via Contacts → pass email to Gmail tool.

**SUCCESS:** Search known contact name → email returned. "Send Ahmed an email" → email sent to correct address.

---

### TASK 8.6 — YouTube + Office/PDF readers

**INPUT:** `{"action": "search", "query": "machine learning tutorial"}`
**OUTPUT:** `ToolResult(data={"videos": [{"title":..., "url":..., "duration":...}]})`
**FILES:** `src/skills/api/youtube.py`, `src/skills/pdf/reader.py`, `src/skills/office/reader.py` (create)

YouTube: search + get_info + open_in_browser.
PDF: text extraction (`pdfplumber`), table extraction, LLM summarization for long docs.
Office: read `.docx`, `.xlsx`, `.pptx`; write simple `.docx` and `.xlsx`.

**SUCCESS:** YouTube search returns valid URLs. PDF text extraction works on a 10-page PDF. Office reader extracts text from a .docx file.

---

## 🤖 Phase 9 — Agents
> **End state:** "Research AI news, summarize it, save to file" executes without step-by-step guidance.

---

### TASK 9.1 — Planner agent

**INPUT:** `goal: str`, `available_tools: list`
**OUTPUT:** `list[Step]` — ordered plan with tool assignments
**FILES:** `src/core/agents/planner.py` (create)

```python
class Step(BaseModel):
    step_id: str
    description: str
    tool: str | None      # None = LLM-only step
    args: dict = {}
    depends_on: list[str] = []

def plan(goal: str, tools: list[str]) -> list[Step]:
    # Use qwen3:8b in planning mode
    # System prompt lists available tools + asks for JSON step list
    ...
```

**SUCCESS:** `plan("research AI news and save to file", ["web_search", "write_file"])` returns 2+ steps in dependency order.

---

### TASK 9.2 — Step executor

**INPUT:** `list[Step]` from planner
**OUTPUT:** All steps executed; outputs passed between dependent steps
**FILES:** `src/core/agents/step_executor.py` (create)

```python
def execute_plan(steps: list[Step]) -> dict:
    results = {}
    for step in topological_sort(steps):
        resolved_args = inject_prior_results(step.args, results)
        if step.tool:
            result = execute_tool(step.tool, resolved_args)
        else:
            result = llm_only_step(step.description, resolved_args)
        results[step.step_id] = result
    return results
```

**SUCCESS:** 3-step plan (search → summarize → save) executes all steps. File created with search content.

---

### TASK 9.3 — Thinker (chain-of-thought + self-critique)

**INPUT:** `question: str`
**OUTPUT:** Higher-quality answer than direct LLM call
**FILES:** `src/core/agents/thinker.py` (create)

1. Generate initial answer (qwen3:8b, deep mode)
2. Ask: "Rate this answer 1-10. What's missing?" → if < 7: regenerate with gaps
3. Return final answer

**SUCCESS:** Complex question like "What are trade-offs between RAG and fine-tuning?" → thinker answer is more complete than direct LLM call (measurable by length and coverage).

---

### TASK 9.4 — Researcher agent

**INPUT:** `topic: str`
**OUTPUT:** Markdown research report with multiple sources
**FILES:** `src/core/agents/researcher.py` (create)

```python
def research(topic: str) -> str:
    queries = generate_queries(topic)         # 3 search queries via LLM
    results = [web_search(q) for q in queries]
    pages = [fetch_page_content(r[0]["url"]) for r in results]
    return summarize_multi_source(pages, topic)
```

**SUCCESS:** `research("local AI 2025")` returns markdown with content from 3+ different sources.

---

### TASK 9.5 — Computer use agent

**INPUT:** `goal: str`
**OUTPUT:** Goal accomplished or failure message
**FILES:** `src/core/agents/computer_use.py` (create)

Loop (max 10 iterations):
1. Take screenshot
2. Describe via LLaVA (if available) or OCR
3. Ask LLM: "Given this screen, what's the next action for [goal]?"
4. Execute action via pyautogui
5. Check if goal achieved

All actions require confirmation. Max iterations enforced.

**SUCCESS:** Goal "open Notepad and type hello" → Notepad opens → "hello" typed → success.

---

## 🧩 Phase 10 — Task Decomposition
> **End state:** Complex multi-step goals with parallel subtasks execute correctly. Only failed steps retry.

---

### TASK 10.1 — DAG schema + decomposer

**INPUT:** `goal: str`
**OUTPUT:** `TaskGraph` with subtasks and dependencies
**FILES:** `src/core/agents/decomposer.py` (create)

```python
class Subtask(BaseModel):
    id: str
    title: str
    tool: str | None
    args: dict = {}
    depends_on: list[str] = []
    status: str = "pending"
    result: dict | None = None

class TaskGraph(BaseModel):
    goal: str
    run_id: str
    subtasks: list[Subtask]
```

**SUCCESS:** `decompose("Email all contacts in my spreadsheet")` returns graph: read_spreadsheet → (parallel: send_email × N) → notify_done.

---

### TASK 10.2 — Parallel graph executor

**INPUT:** `TaskGraph`
**OUTPUT:** All subtasks executed; parallel frontier runs concurrently
**FILES:** `src/core/agents/graph_executor.py` (create)

Use `asyncio.gather()` for parallel frontier. Topological sort for ordering.

**SUCCESS:** 3 independent tasks run in parallel (verify via timestamps in logs showing concurrent execution).

---

### TASK 10.3 — Selective retry

**INPUT:** `TaskGraph` with one failed subtask
**OUTPUT:** Only failed subtask re-executes; successful ones untouched
**FILES:** `src/core/agents/graph_executor.py` (modify)

**SUCCESS:** Force-fail one task. Call retry. Logs show only that task re-ran.

---

### TASK 10.4 — Resume from checkpoint

**INPUT:** `run_id: str` of interrupted execution
**OUTPUT:** Execution resumes from last successful step
**FILES:** `src/core/memory/database.py` (add `task_graphs` table)

Save graph state to SQLite after each subtask. On resume: load graph, skip `status="done"` tasks.

**SUCCESS:** Start 5-step task. Kill process after step 3. Restart with `run_id`. Steps 1-3 skipped. Steps 4-5 execute.

---

### TASK 10.5 — End-to-end scenario test

**INPUT:** "Book a meeting with Ahmed at 3pm tomorrow and email him the agenda"
**OUTPUT:** Calendar event created + email sent to Ahmed's address (from Contacts)
**FILES:** No new files — integration test

**SUCCESS:** Command executes using Planner → Contacts → Calendar + Gmail tools in correct order.

---

## 🔁 Phase 11 — Feedback Loop
> **End state:** After 10 sessions, routing weights shift based on what worked.

---

### TASK 11.1 — Feedback signal collection

**INPUT:** Turn outcome (response, eval result, user follow-up behavior)
**OUTPUT:** Score (0-1) saved to `feedback` table
**FILES:** `src/core/memory/feedback.py` (create)

Signals:
- `eval.quality > 0.8` → score += 0.1 (positive)
- User sends follow-up immediately → score += 0.1
- User rephrases same question → score -= 0.3 (negative)
- `/thumbsup` command → score = 1.0
- `/thumbsdown` command → score = 0.0

**SUCCESS:** 5 turns → 5 rows in feedback table with scores.

---

### TASK 11.2 — Routing weight updater

**INPUT:** Feedback table entries (computed every 20 turns)
**OUTPUT:** Updated weights in `data/routing_weights.json`
**FILES:** `src/core/decision/weight_updater.py` (create)

Exponential moving average: `new = old × 0.9 + avg_score × 0.1`. Max delta: ±0.15 per update.

**SUCCESS:** Simulate 20 turns of poor `gemma3:4b` performance on code tasks → weight for `(code, gemma3:4b)` decreases numerically.

---

### TASK 11.3 — Privacy controls

**INPUT:** `/feedback off` or `/clear feedback` CLI command
**OUTPUT:** Collection stops / all data deleted
**FILES:** `src/interfaces/cli/commands.py` (modify)

**SUCCESS:** `/feedback off` → no new feedback rows. `/clear feedback` → table is empty.

---

### TASK 11.4 — Memory writes from good outcomes

**INPUT:** Turn with quality > 0.8
**OUTPUT:** "What worked" summary saved to long-term memory
**FILES:** `src/core/runtime/loop.py` (modify)

When quality high: `long_term.remember(f"For '{intent}', '{model}' in '{mode}' mode works well", metadata={"type": "routing_hint"})`.

**SUCCESS:** After 3 high-quality code turns, `recall("code tasks")` returns routing hint.

---

## 🌐 Phase 12 — Web UI
> **End state:** Premium glassmorphism browser chat. Streaming. File upload. Arabic RTL. Sidebar with history.

---

### TASK 12.1 — FastAPI app + WebSocket

**INPUT:** Browser connects to http://localhost:8080
**OUTPUT:** Chat page served; WebSocket connects; messages stream
**FILES:** `src/interfaces/web/app.py` (create), `src/interfaces/web/ws.py` (create), `app/server.py` (create)

```python
@app.websocket("/ws/{session_id}")
async def ws_endpoint(ws: WebSocket, session_id: str):
    await ws.accept()
    while True:
        data = await ws.receive_json()
        async for token in run_turn_streaming(data["message"], session_id):
            await ws.send_json({"type": "token", "data": token})
        await ws.send_json({"type": "done"})
```

**SUCCESS:** Open localhost:8080 → page loads → type message → streamed response appears.

---

### TASK 12.2 — HTML/CSS/JS chat interface

**INPUT:** Browser request
**OUTPUT:** Glassmorphism chat UI
**FILES:** `src/interfaces/web/templates/index.html`, `src/interfaces/web/static/style.css`, `src/interfaces/web/static/chat.js` (create)

Design:
- Background: `#0a0a1a`
- Panels: `backdrop-filter: blur(16px); background: rgba(255,255,255,0.05)`
- Accent: `#3b82f6` → `#06b6d4` gradient
- Font: Inter + IBM Plex Arabic
- Auto RTL: Arabic messages → `direction: rtl; text-align: right`
- Streaming cursor animation
- Code blocks: Highlight.js syntax highlighting
- Markdown rendering

**SUCCESS:** Arabic messages render RTL. Streaming shows cursor. Code blocks have syntax colors.

---

### TASK 12.3 — Input bar: attachments + mode selector + send/mic

**INPUT:** User interaction with input controls
**OUTPUT:** Message sent with mode and attachments
**FILES:** `src/interfaces/web/static/chat.js` (expand)

- "+" button → upload file / image / paste clipboard
- Mode row: ⚡ fast / 🧠 normal / ⚛ deep / 📋 planning / 🔭 research
- Empty → mic icon; typing → send arrow (smooth morph)
- Drag-and-drop on chat area
- Ctrl+V image paste

**SUCCESS:** All input mechanisms work. Selected mode is sent with message and changes routing.

---

### TASK 12.4 — Sidebar: conversations + search + settings

**INPUT:** User interaction with sidebar
**OUTPUT:** History shown, search works, settings persist
**FILES:** `src/interfaces/web/static/chat.js` (expand)

- Conversation list grouped by date
- New Chat, rename, delete (confirm), pin, archive
- Ctrl+K → search by title (instant) or content (server-side)
- Settings: theme, font size, mode, language, enter key behavior

**SUCCESS:** 5 conversations created. Search finds them. Settings persist after page reload.

---

### TASK 12.5 — REST API endpoints

**INPUT:** HTTP requests from browser JS
**OUTPUT:** JSON responses
**FILES:** `src/interfaces/web/routes.py` (create)

| Endpoint | Method | Action |
|----------|--------|--------|
| `/api/conversations` | GET | Paginated list |
| `/api/conversations/:id` | GET/PUT/DELETE | CRUD |
| `/api/memory` | DELETE | Clear session |
| `/api/upload` | POST | File → buffer id |
| `/api/settings` | GET/PUT | User prefs |
| `/api/status` | GET | VRAM, model, health |

**SUCCESS:** All endpoints return correct HTTP status. CRUD complete round-trip.

---

### TASK 12.6 — Dashboard panel

**INPUT:** `/api/status` polled every 3 seconds
**OUTPUT:** Live VRAM bar, active tool, system stats
**FILES:** `src/interfaces/web/templates/index.html` (add section)

Cards: GPU VRAM %, Active Model, Active Tool, CPU%, RAM.

**SUCCESS:** Dashboard updates live. While a tool runs, "Active Tool" shows its name.

---

### TASK 12.7 — Feedback + toast notifications

**INPUT:** Thumbs up/down per message; system events
**OUTPUT:** Feedback recorded in DB; toast notification shown
**FILES:** `src/interfaces/web/static/chat.js` (expand)

Toast types: success (green), error (red), info (blue), warning (orange). Auto-dismiss 4s.

**SUCCESS:** Click thumbs up → feedback row in DB → green toast appears.

---

## 🎙️ Phase 13 — Voice Pipeline
> **End state:** "Hey Jarvis" → speak command → hear spoken answer.

---

### TASK 13.1 — Whisper STT

**INPUT:** Audio from microphone (numpy array)
**OUTPUT:** `{"text": "open chrome", "language": "ar"}`
**FILES:** `src/models/speech/stt.py` (create)

Load `whisper.load_model("medium")`. Record with `sounddevice`. Transcribe with auto-language detection.

**SUCCESS:** 5 seconds of Arabic → correct Arabic transcription. 5 seconds of English → correct English.

---

### TASK 13.2 — Piper TTS

**INPUT:** `text: str`, `language: str`
**OUTPUT:** Audio played through speakers
**FILES:** `src/models/speech/tts.py` (create)

Load `ar_JO-kareem-medium.onnx` for Arabic. English voice for English. Auto-select based on language.

**SUCCESS:** `speak("مرحباً", "ar")` produces natural Arabic audio. `speak("Hello", "en")` produces English audio.

---

### TASK 13.3 — Wake word detection

**INPUT:** Continuous mic stream
**OUTPUT:** Event when "Hey Jarvis" detected
**FILES:** `src/interfaces/voice/wake_word.py` (create)

openWakeWord model at score > 0.5 threshold. Runs on 1280-frame chunks.

**SUCCESS:** Say "Hey Jarvis" → fires within 1 second. Random speech → no false triggers.

---

### TASK 13.4 — Voice Activity Detection

**INPUT:** Mic stream post-wake-word
**OUTPUT:** Audio segment that ends when user stops speaking
**FILES:** `src/interfaces/voice/vad.py` (create)

Use `webrtcvad` at aggressiveness=2. Stop after 1 second of continuous silence.

**SUCCESS:** Speak 3 seconds, pause 1 second → recording stops precisely.

---

### TASK 13.5 — Full voice pipeline

**INPUT:** "Hey Jarvis" spoken
**OUTPUT:** Spoken response from Jarvis
**FILES:** `src/interfaces/voice/pipeline.py` (create)

```python
def run_voice_pipeline():
    while True:
        wait_for_wake_word()
        play_chime()
        audio = record_with_vad()
        text = transcribe(audio)
        response = run_turn(text, session_id="voice")
        speak(response, detect_language(text))
```

**SUCCESS:** "Hey Jarvis, what's the capital of Egypt?" → spoken answer "القاهرة" (or "Cairo") within 15 seconds.

---

## 👁️ Phase 14 — Vision & Image Generation
> **End state:** Upload image → Arabic description. Ask for image → generated and shown.

---

### TASK 14.1 — LLaVA image understanding

**INPUT:** `image_path: str`, `question: str`
**OUTPUT:** Text description in user's language
**FILES:** `src/models/vision/llava.py` (create)

```python
def describe_image(image_path: str, question: str = "Describe this image in detail") -> str:
    with open(image_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode()
    response = ollama.chat(model="llava:7b",
                           messages=[{"role": "user", "content": question, "images": [image_b64]}])
    return response["message"]["content"]
```

VRAM guard: unload text model before loading LLaVA.

**SUCCESS:** Upload code screenshot → LLaVA describes the code. Upload Arabic text image → text read correctly.

---

### TASK 14.2 — Stable Diffusion image generation

**INPUT:** `prompt: str` (any language)
**OUTPUT:** Image saved to `data/generated/`; path returned
**FILES:** `src/models/diffusion/sd.py` (create)

Translate Arabic prompt to English first (via LLM). Use SD 1.5 with float16. Unload after generation to free VRAM.

**SUCCESS:** "Generate an image of a mountain at sunset" → image saved → displayable.

---

### TASK 14.3 — Vision integration into runtime

**INPUT:** `ContextBundle` with image attachment
**OUTPUT:** LLaVA description injected into context; LLM answers about image
**FILES:** `src/core/context/assembler.py` (modify)

When images in bundle: call `describe_image()` per image → add to `memory_snippets`.

**SUCCESS:** Upload chart image in Web UI → ask "what does this show?" → correct answer based on image content.

---

### TASK 14.4 — Screen description tool

**INPUT:** `{"action": "describe_screen"}`
**OUTPUT:** Natural language description of current screen
**FILES:** `src/skills/screen/describe.py` (create)

```python
def describe_screen() -> ToolResult:
    path = take_screenshot()
    description = describe_image(path, "What is on this screen?")
    return ToolResult(success=True, data={"description": description, "screenshot": path})
```

**SUCCESS:** "What's on my screen?" → accurate description of visible content.

---

## 📱 Phase 15 — Telegram + GUI
> **End state:** Full Jarvis via Telegram. PyQt6 desktop app with tray icon.

---

### TASK 15.1 — Telegram bot

**INPUT:** Text, photo, voice note, or document sent to bot
**OUTPUT:** Jarvis responds correctly to each type
**FILES:** `src/interfaces/telegram/bot.py` (create)

- Text → `run_turn()` → reply
- Photo → `describe_image()` → reply
- Voice → `transcribe()` → `run_turn()` → reply
- Document → `read_pdf()` or `read_office()` → summary reply
- Commands: `/clear`, `/model`, `/mode`, `/image [prompt]`, `/search [query]`

**SUCCESS:** Send Arabic voice note → transcription + answer returned as text.

---

### TASK 15.2 — PyQt6 desktop app

**INPUT:** User interaction with desktop window
**OUTPUT:** Chat works; Arabic RTL correct; voice button works
**FILES:** `src/interfaces/gui/main_window.py` (create)

Scrollable chat area + expanding input box + send/mic buttons + model dropdown + mode toolbar.

**SUCCESS:** Launch GUI → type Arabic → RTL correct. Voice button activates STT.

---

### TASK 15.3 — System tray daemon

**INPUT:** App minimized or `--background` flag
**OUTPUT:** Tray icon visible; wake word active in background
**FILES:** `src/interfaces/gui/tray.py` (create)

`pystray` menu: Open GUI / Open Web UI / Settings / Quit. Wake word thread runs in background.

**SUCCESS:** App in tray. Say "Hey Jarvis" → GUI window appears.

---

### TASK 15.4 — Auto-start on Windows login

**INPUT:** User toggles "Start with Windows" in settings
**OUTPUT:** Registry key added/removed
**FILES:** `src/interfaces/gui/autostart.py` (create)

Write/delete `HKCU\Software\Microsoft\Windows\CurrentVersion\Run\Jarvis` registry key.

**SUCCESS:** Enable → reboot Windows → Jarvis tray icon appears automatically.

---

## 🔒 Phase 16 — QA + Security
> **End state:** All tests pass. VRAM stays under limit. No credentials in logs.

---

### TASK 16.1 — Test suite

**INPUT:** `pytest tests/` command
**OUTPUT:** All tests pass; coverage ≥ 70%
**FILES:** `tests/test_models.py`, `test_decision.py`, `test_memory.py`, `test_tools.py`, `test_runtime.py`, `test_skills.py`, `test_browser.py`, `test_apis.py`, `test_agents.py` (create)

Each test file covers the corresponding phase. Tests are real (not mocked where possible).

**SUCCESS:** `pytest tests/ --cov=src` reports 0 failures, ≥70% coverage.

---

### TASK 16.2 — Security hardening

**INPUT:** Code review of all skills
**OUTPUT:** Security checklist complete
**FILES:** Multiple files (audit and fix)

Checklist:
- [ ] `delete_file` uses `send2trash` (never `os.remove` directly on user files)
- [ ] `run_shell` checks blocklist before execution
- [ ] `send_email` always requires confirmation
- [ ] `google_token.json` never appears in any log line
- [ ] Browser sessions encrypted at rest (Fernet key from `.env`)
- [ ] All tool args validated against JSON Schema before execution
- [ ] Path traversal: file paths checked against allowed roots
- [ ] Error messages sanitized before returning to LLM (no stack traces)

**SUCCESS:** Manual audit of all 8 items passes.

---

### TASK 16.3 — Performance benchmarks

**INPUT:** `python scripts/benchmark.py`
**OUTPUT:** All metrics within targets
**FILES:** `scripts/benchmark.py` (create)

| Metric | Target |
|--------|--------|
| Cold start to first response | < 10 seconds |
| Simple chat (gemma3:4b) | < 5 seconds |
| File read tool | < 1 second |
| VRAM peak during chat | < 5.5 GB |
| Voice round-trip | < 15 seconds |
| Web UI first message | < 3 seconds |

**SUCCESS:** All 6 metrics pass.

---

### TASK 16.4 — Windows 11 clean install test

**INPUT:** Clean Windows 11 machine (or VM)
**OUTPUT:** Full install + all features work
**FILES:** `scripts/install.ps1` (finalize)

Test sequence:
1. `install.ps1` on clean machine
2. `python app/main.py --interface cli`
3. Text chat, file ops, app launch, notification, clipboard
4. Web UI, Telegram, voice

**SUCCESS:** All steps complete on a machine that never had Jarvis before.

---

### TASK 16.5 — Credential audit

**INPUT:** All log files
**OUTPUT:** Zero credentials visible in logs
**FILES:** `scripts/credential_audit.py` (create)

Scan `logs/` for patterns: API keys, OAuth tokens, email addresses in unexpected positions.

**SUCCESS:** Script finds zero matches.

---

### TASK 16.6 — CI setup

**INPUT:** Git push
**OUTPUT:** Lint + type check + tests run automatically
**FILES:** `.github/workflows/ci.yml` (create)

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: "3.11"}
      - run: pip install -r requirements.txt
      - run: ruff check src/
      - run: pytest tests/ --cov=src -x
```

**SUCCESS:** Push triggers CI. All checks pass.

---

## 🎭 Phase 17 — Personality
> **End state:** Tone and style adapt to user preferences. Arabic feels Arabic, not translated.

---

### TASK 17.1 — Personality fragments in system prompt

**INPUT:** User profile (style, tone)
**OUTPUT:** Personality fragment injected before every LLM call
**FILES:** `src/core/identity/personality.py` (create)

```python
FRAGMENTS = {
    "concise": "Keep answers brief. Use bullet points. No preamble.",
    "detailed": "Provide thorough explanations with examples.",
    "formal": "Use formal language. Avoid contractions.",
    "casual": "Be conversational and friendly.",
    "arabic_native": "Use natural Arabic expressions. Avoid literal translations from English.",
}

def get_personality_fragment(profile: dict) -> str:
    parts = []
    parts.append(FRAGMENTS.get(profile.get("style", "balanced"), ""))
    parts.append(FRAGMENTS.get(profile.get("tone", "casual"), ""))
    if profile.get("language") == "ar":
        parts.append(FRAGMENTS["arabic_native"])
    return " ".join(p for p in parts if p)
```

**SUCCESS:** `style=concise` → responses measurably shorter. `language=ar` → responses use native Arabic expressions.

---

### TASK 17.2 — Adaptive drift from feedback

**INPUT:** Feedback table entries
**OUTPUT:** User profile style/tone updated based on patterns
**FILES:** `src/core/identity/personality.py` (expand)

Every 10 turns: check which styles got positive feedback. Nudge profile by one step (concise → balanced → detailed). Max 1 step per update.

**SUCCESS:** 20 turns of positive feedback on short answers → profile drifts to `style=concise`.

---

### TASK 17.3 — Arabic/English native feel test

**INPUT:** Same question in Arabic + in English
**OUTPUT:** Each response feels native in its language
**FILES:** `config/jarvis_identity.yaml` (add language behavior section)

Add to identity:
```yaml
language_behavior:
  arabic:
    greeting: "أهلاً وسهلاً"
    affirmation: "بالتأكيد"
    note: "Use natural Arabic expressions, warm tone"
  english:
    greeting: "Hello"
    affirmation: "Sure"
    note: "Direct and concise tone"
```

**SUCCESS:** Arabic input → response includes natural Arabic phrases (not "بالتأكيد" translated from "Sure"). English input → direct sentences without filler.

---

## 📌 Quick Reference

### Layer Responsibilities (no overlap)

| Layer | Files | Does | Does NOT |
|-------|-------|------|----------|
| `src/models/` | engine.py, llava.py, stt.py | Wrap AI models, return text/audio/images | Decide, read memory, know tools |
| `src/core/context/` | assembler.py | Collect this turn's inputs | Store across turns |
| `src/core/decision/` | decision.py, classifier.py | Classify intent, select model | Think, plan, execute |
| `src/core/runtime/` | loop.py, executor.py, evaluator.py | Drive the Think→Act→Evaluate cycle | Implement intelligence |
| `src/core/agents/` | planner.py, thinker.py, researcher.py | Multi-step reasoning, planning | Route requests, execute tools directly |
| `src/core/tools/` | registry.py, executor.py, safety.py | Discover, validate, run tools | Implement tool logic |
| `src/core/memory/` | short_term.py, long_term.py, database.py | Store and retrieve data | Participate in routing |
| `src/core/identity/` | builder.py, personality.py | Build system prompts | Make decisions |
| `src/skills/` | (one file per tool) | Do one specific thing in the world | Anything else |
| `src/interfaces/` | cli/, web/, voice/, telegram/, gui/ | Receive input, display output | Contain logic |

### Model Selection Rules

```
complexity=low OR mode=fast          → gemma3:4b
intent=code OR code_bias signal      → qwen2.5-coder:7b
image in context                     → llava:7b
everything else                      → qwen3:8b
```

### Arabic Detection

```python
def is_arabic(text: str) -> bool:
    arabic = sum(1 for c in text if '\u0600' <= c <= '\u06FF')
    return arabic / max(len(text), 1) > 0.3
```

### VRAM Rule

```
Before loading any model:
  1. Check current model via get_active_model()
  2. If different model needed: call unload_current_model()
  3. Verify freed: wait for Ollama to confirm
  4. Load new model
  Never load two heavy models simultaneously.
```

---

*Version 0.4.0-alpha — Tasks with INPUT/OUTPUT/FILES/SUCCESS_CRITERIA*
*Phase 0 first. Each phase has a working end state before you move on.*
