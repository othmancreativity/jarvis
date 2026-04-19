# 🗂️ JARVIS — Task Board

> **Every task has:** INPUT · OUTPUT · FILES · SUCCESS CRITERIA  
> **Rule:** Don't start Phase N until Phase N-1 is verified complete.

---

## Progress

| Phase | Description | Status |
|---|---|---|
| 1 | Minimal Working System | ⬜ |
| 2 | Runtime Loop (full) | ⬜ |
| 3 | Decision + Model Router | ⬜ |
| 4 | Tool System | ⬜ |
| 5 | Context Buffer | ⬜ |
| 6 | Memory | ⬜ |
| 7 | Agents | ⬜ |
| 8 | Skills (System + Browser + Search) | ⬜ |
| 9 | Safety | ⬜ |
| 10 | Google APIs | ⬜ |
| 11 | CLI Interface | ⬜ |
| 12 | Web UI | ⬜ |
| 13 | Voice Pipeline | ⬜ |
| 14 | Telegram + GUI | ⬜ |
| 15 | Logging + Observability | ⬜ |
| 16 | Optimization + QA | ⬜ |

---

## ⚡ Phase 1 — Minimal Working System

> **Goal:** `python app/main.py --interface cli` → user types text → gets real LLM response.  
> No tools. No memory. No agents. This is the foundation everything else plugs into.

---

### TASK 1.1 — Project skeleton

**INPUT:** Empty repository  
**OUTPUT:** All directories exist with `__init__.py`. Project importable.

**FILES TO CREATE:**
```
app/__init__.py
app/main.py               ← entry point (see 1.6)
src/__init__.py
src/core/__init__.py
src/core/runtime/__init__.py
src/core/orchestrator/__init__.py
src/core/agents/__init__.py
src/core/tools/__init__.py
src/core/memory/__init__.py
src/core/context/__init__.py
src/core/identity/__init__.py
src/core/safety/__init__.py
src/models/__init__.py
src/models/base/__init__.py
src/models/llm/__init__.py
src/models/vision/__init__.py
src/models/speech/__init__.py
src/models/diffusion/__init__.py
src/skills/__init__.py
src/skills/system/__init__.py
src/skills/browser/__init__.py
src/skills/search/__init__.py
src/skills/coder/__init__.py
src/skills/screen/__init__.py
src/skills/api/__init__.py
src/skills/office/__init__.py
src/interfaces/__init__.py
src/interfaces/cli/__init__.py
src/interfaces/web/__init__.py
src/interfaces/telegram/__init__.py
src/interfaces/gui/__init__.py
src/interfaces/voice/__init__.py
data/.gitkeep
logs/.gitkeep
```

**SUCCESS CRITERIA:**
- [ ] `python -c "import src.core.runtime"` runs without error (with `PYTHONPATH=src`)
- [ ] All directories exist on disk

---

### TASK 1.2 — Config files

**INPUT:** Nothing  
**OUTPUT:** Three YAML config files that load without error

**FILES TO CREATE:**

`config/settings.yaml`:
```yaml
jarvis:
  name: "Jarvis"
  language: ["ar", "en"]
  wake_word: "hey_jarvis"

runtime:
  max_iterations: 5
  max_escalation_depth: 2
  tool_timeout_s: 30
  step_timeout_s: 60

models:
  default: "qwen3:8b"
  fast:    "gemma3:4b"
  code:    "qwen2.5-coder:7b"
  vision:  "llava:7b"

hardware:
  gpu_vram_limit_gb: 5.5
  max_concurrent_models: 1

interfaces:
  web:
    host: "127.0.0.1"
    port: 8080

paths:
  data:        "data/"
  logs:        "logs/"
  sessions:    "data/sessions/"
  downloads:   "data/downloads/"
  screenshots: "data/screenshots/"
  chroma_db:   "data/chroma/"
  sqlite_db:   "data/jarvis.db"

hotkeys:
  open_cli:    "ctrl+alt+j"
  start_voice: "ctrl+alt+s"
```

`config/models.yaml`:
```yaml
routing:
  hard_rules:
    vision: "llava:7b"
    code:   "qwen2.5-coder:7b"
  mode_preferences:
    fast:     "gemma3:4b"
    normal:   "qwen3:8b"
    deep:     "qwen3:8b"
    planning: "qwen3:8b"
    research: "qwen3:8b"

models:
  qwen3:8b:
    ollama_tag: "qwen3:8b"
    vram_gb: 5.0
    temperature: 0.7
    top_p: 0.9
    max_tokens: 8192
  gemma3:4b:
    ollama_tag: "gemma3:4b"
    vram_gb: 3.0
    temperature: 0.7
    top_p: 0.9
    max_tokens: 4096
  qwen2.5-coder:7b:
    ollama_tag: "qwen2.5-coder:7b"
    vram_gb: 4.7
    temperature: 0.2
    top_p: 0.95
    max_tokens: 8192
  llava:7b:
    ollama_tag: "llava:7b"
    vram_gb: 4.5
    temperature: 0.7
    top_p: 0.9
    max_tokens: 4096
```

`config/identity.yaml`:
```yaml
name: "Jarvis"
version: "0.4.0"
role: "Personal AI assistant running fully locally on your machine"
default_language: "ar"
tone: "Professional, concise, and helpful"
always_confirm_destructive: true
```

**SUCCESS CRITERIA:**
- [ ] `import yaml; yaml.safe_load(open("config/settings.yaml"))` works without error
- [ ] All three files valid YAML
- [ ] No required key is missing

---

### TASK 1.3 — Settings loader

**INPUT:** `config/settings.yaml` + `.env`  
**OUTPUT:** Single importable `settings` object

**FILES TO CREATE:** `src/settings.py`

```python
from pydantic_settings import BaseSettings
from pydantic import BaseModel
import yaml

class RuntimeConfig(BaseModel):
    max_iterations: int = 5
    max_escalation_depth: int = 2
    tool_timeout_s: int = 30

class ModelsConfig(BaseModel):
    default: str = "qwen3:8b"
    fast: str = "gemma3:4b"
    code: str = "qwen2.5-coder:7b"
    vision: str = "llava:7b"

class JarvisSettings(BaseModel):
    runtime: RuntimeConfig
    models: ModelsConfig
    # ... other sections

def load_settings(path: str = "config/settings.yaml") -> JarvisSettings:
    raw = yaml.safe_load(open(path))
    return JarvisSettings(**raw)

settings = load_settings()
```

**SUCCESS CRITERIA:**
- [ ] `from settings import settings; print(settings.jarvis.name)` prints `"Jarvis"`
- [ ] Missing YAML key raises `ValidationError` with clear message
- [ ] `python -c "from settings import settings"` exits with code 0

---

### TASK 1.4 — Logger

**INPUT:** `config/settings.yaml` (log path)  
**OUTPUT:** `logger` object usable everywhere

**FILES TO CREATE:** `src/logger.py`

```python
from loguru import logger
import sys

logger.remove()
logger.add(sys.stdout, level="INFO", colorize=True,
           format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | {message}")
logger.add("logs/jarvis.log", level="DEBUG", rotation="1 day",
           retention="7 days", serialize=True)  # JSON format
```

**SUCCESS CRITERIA:**
- [ ] `from logger import logger; logger.info("test")` writes to both console and `logs/jarvis.log`
- [ ] Log file is valid JSON Lines (one JSON object per line)
- [ ] Each entry has: `timestamp`, `level`, `message`, `module`

---

### TASK 1.5 — LLM engine (Ollama client)

**INPUT:** `messages: list[dict]`, `model: str`  
**OUTPUT:** Streamed text tokens

**FILES TO CREATE:** `src/models/llm/engine.py`

```python
import httpx
from typing import Generator

class OllamaEngine:
    BASE_URL = "http://localhost:11434"

    def chat(self, messages: list[dict], model: str,
             system: str = "", stream: bool = True) -> Generator[str, None, None]:
        payload = {"model": model, "messages": messages, "stream": stream}
        if system:
            payload["messages"] = [{"role": "system", "content": system}] + messages

        with httpx.stream("POST", f"{self.BASE_URL}/api/chat", json=payload, timeout=120) as r:
            for line in r.iter_lines():
                chunk = json.loads(line)
                if text := chunk.get("message", {}).get("content", ""):
                    yield text
                if chunk.get("done"):
                    break

    def is_available(self) -> bool:
        try:
            httpx.get(f"{self.BASE_URL}/api/tags", timeout=3)
            return True
        except Exception:
            return False

    def list_models(self) -> list[str]:
        r = httpx.get(f"{self.BASE_URL}/api/tags", timeout=5)
        return [m["name"] for m in r.json().get("models", [])]
```

**SUCCESS CRITERIA:**
- [ ] `engine.is_available()` returns `True` when Ollama is running
- [ ] `list(engine.chat([{"role":"user","content":"Hi"}], "gemma3:4b"))` returns list of strings
- [ ] Arabic input `"مرحبا"` produces Arabic output tokens
- [ ] Connection refused → raises `httpx.ConnectError` (not silent failure)

---

### TASK 1.6 — Minimal runtime loop (stub)

**INPUT:** `user_input: str`, `session_id: str`  
**OUTPUT:** Streamed LLM response

**FILES TO CREATE:** `src/core/runtime/loop.py`

This is the Phase 1 stub — no decision layer, no memory, no tools:

```python
from models.llm.engine import OllamaEngine

class RuntimeLoop:
    def __init__(self):
        self.llm = OllamaEngine()

    def run(self, user_input: str, session_id: str = "default") -> Generator[str, None, None]:
        if not self.llm.is_available():
            yield "خطأ: Ollama غير متاح. تأكد من تشغيله."
            return

        messages = [{"role": "user", "content": user_input}]
        system = "أنت Jarvis، مساعد ذكاء اصطناعي محلي. أجب بإيجاز ووضوح."

        yield from self.llm.chat(messages, model="qwen3:8b", system=system)
```

**SUCCESS CRITERIA:**
- [ ] `list(loop.run("Hello"))` returns non-empty list of strings
- [ ] `list(loop.run("مرحبا"))` returns Arabic text
- [ ] `loop.run("")` yields a polite fallback message (not crash)
- [ ] Ollama offline → yields error message (not traceback)

---

### TASK 1.7 — CLI interface (minimal)

**INPUT:** User text from terminal  
**OUTPUT:** Streaming response in terminal

**FILES TO CREATE:** `src/interfaces/cli/interface.py`

```python
from rich.console import Console
from rich.live import Live
from rich.text import Text
from core.runtime.loop import RuntimeLoop

class CLIInterface:
    def __init__(self):
        self.console = Console()
        self.loop = RuntimeLoop()

    def start(self):
        self.console.print("[bold green]Jarvis ready. Press Ctrl+C to exit.[/]")
        while True:
            try:
                user_input = input("\nYou: ").strip()
                if not user_input:
                    continue
                self.console.print("[bold blue]Jarvis:[/] ", end="")
                for token in self.loop.run(user_input):
                    print(token, end="", flush=True)
                print()  # newline after response
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Goodbye.[/]")
                break
```

**FILES TO MODIFY:** `app/main.py`

```python
import argparse
from logger import logger
from settings import settings

def main():
    parser = argparse.ArgumentParser(description="Jarvis AI Assistant")
    parser.add_argument("--interface", choices=["cli","web","telegram","gui","voice","all"],
                        default="cli")
    args = parser.parse_args()

    logger.info(f"Starting Jarvis — interface: {args.interface}")

    if args.interface == "cli":
        from interfaces.cli.interface import CLIInterface
        CLIInterface().start()
    else:
        logger.warning(f"Interface '{args.interface}' not yet implemented.")

if __name__ == "__main__":
    main()
```

**SUCCESS CRITERIA:**
- [ ] `python app/main.py --interface cli` shows prompt
- [ ] Typing "Hello" → real streamed LLM response appears token by token
- [ ] Typing in Arabic → Arabic response
- [ ] `Ctrl+C` exits cleanly — no traceback
- [ ] `python app/main.py --help` shows usage

---

### TASK 1.8 — .env.example + requirements.txt

**FILES TO CREATE:** `.env.example`
```env
TELEGRAM_BOT_TOKEN=
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
YOUTUBE_API_KEY=
REDIS_URL=redis://localhost:6379
JARVIS_ENV=development
```

**FILES TO MODIFY:** `requirements.txt`

```
# Core
httpx>=0.27
pydantic>=2.0
pydantic-settings>=2.0
pyyaml>=6.0
python-dotenv>=1.0
loguru>=0.7

# LLM + ML
ollama>=0.2
sentence-transformers>=2.7
chromadb>=0.5
torch>=2.2
openai-whisper>=20231117
diffusers>=0.27
accelerate>=0.30
Pillow>=10.0

# Memory
redis>=5.0
aiosqlite>=0.20

# Browser + automation
playwright>=1.44
psutil>=5.9
pyperclip>=1.9

# Interfaces
fastapi>=0.111
uvicorn[standard]>=0.30
jinja2>=3.1
websockets>=12.0
rich>=13.7
python-telegram-bot>=21.0
PyQt6>=6.7

# Audio
pyaudio>=0.2
sounddevice>=0.4
webrtcvad>=2.0
openwakeword>=0.6

# Google APIs
google-auth>=2.29
google-auth-oauthlib>=1.2
google-api-python-client>=2.131

# Windows-specific
pywin32>=306; sys_platform == "win32"
pycaw>=20240210; sys_platform == "win32"
winotify>=1.1; sys_platform == "win32"
keyboard>=0.13; sys_platform == "win32"
pynput>=1.7
mss>=9.0
pytesseract>=0.3
pystray>=0.19

# Office documents
pypdf>=4.0
pdfplumber>=0.11
python-docx>=1.1
openpyxl>=3.1
python-pptx>=0.6

# Dev
pytest>=8.0
pytest-asyncio>=0.23
```

**SUCCESS CRITERIA:**
- [ ] `pip install -r requirements.txt` completes in clean venv
- [ ] No version conflicts

---

### ✅ Phase 1 Acceptance Test

Run this sequence. All steps must pass:

```bash
python app/main.py --interface cli
# Type: Hello
# Expect: English greeting response (streamed)

# Type: مرحبا
# Expect: Arabic response (streamed)

# Type: (empty — just press Enter)
# Expect: No crash

# Press Ctrl+C
# Expect: "Goodbye." — clean exit, no traceback
```

---

## 🔄 Phase 2 — Runtime Loop (Full)

> **Goal:** Full Observe → Decide → Think → Act → Evaluate loop with escalation.  
> **Depends on:** Phase 1 complete.

---

### TASK 2.1 — TurnState

**INPUT:** `session_id: str`  
**OUTPUT:** Mutable state object tracking the current turn

**FILES TO CREATE:** `src/core/runtime/state.py`

```python
from dataclasses import dataclass, field
from typing import Any

@dataclass
class ToolTrace:
    tool: str
    success: bool
    result: Any
    error: str | None
    duration_ms: int

@dataclass
class TurnState:
    session_id: str
    iteration: int = 0
    mode: str = "normal"
    messages: list[dict] = field(default_factory=list)
    tool_traces: list[ToolTrace] = field(default_factory=list)
    observations: list[str] = field(default_factory=list)

    def add_tool_result(self, result: ToolTrace):
        self.tool_traces.append(result)
        self.observations.append(f"Tool {result.tool}: {'OK' if result.success else result.error}")

    def to_dict(self) -> dict:
        return {
            "session_id": self.session_id,
            "iteration": self.iteration,
            "mode": self.mode,
            "tool_traces": len(self.tool_traces),
        }
```

**SUCCESS CRITERIA:**
- [ ] `TurnState("abc")` creates with defaults
- [ ] `add_tool_result()` appends to both `tool_traces` and `observations`
- [ ] `to_dict()` returns JSON-serializable dict

---

### TASK 2.2 — EvalResult + Evaluator

**INPUT:** Candidate answer (str) + `TurnState`  
**OUTPUT:** `EvalResult(recommendation="finish"|"escalate", score=float, reason=str)`

**FILES TO CREATE:** `src/core/runtime/evaluate.py`

```python
@dataclass
class EvalResult:
    recommendation: str  # "finish" | "escalate"
    score: float         # 0.0 to 1.0
    reason: str = ""

class Evaluator:
    def evaluate(self, answer: str, state: TurnState) -> EvalResult:
        if not answer.strip():
            return EvalResult("escalate", 0.0, "empty answer")

        if any(not t.success for t in state.tool_traces):
            return EvalResult("escalate", 0.3, "tool failed")

        if len(answer.split()) < 3:
            return EvalResult("escalate", 0.4, "answer too short")

        return EvalResult("finish", 0.85)
```

**SUCCESS CRITERIA:**
- [ ] Empty string → `recommendation == "escalate"`, `score == 0.0`
- [ ] Failed tool in state → `recommendation == "escalate"`
- [ ] Normal answer → `recommendation == "finish"`, `score >= 0.7`

---

### TASK 2.3 — Upgrade RuntimeLoop to full loop

**INPUT:** `TurnState`, `Evaluator` (from 2.2)  
**OUTPUT:** Full observe→decide→think→act→evaluate loop

**FILES TO MODIFY:** `src/core/runtime/loop.py`

Upgrade from Phase 1 stub to the full implementation shown in README Section 4.

Key changes:
- Add `TurnState` per turn
- Add `Evaluator` call after think
- Add escalation (mode upgrade + retry)
- Add max_iterations guard with fallback message
- Add `observe()` method that collects state.observations
- Add `_next_mode()` for escalation chain

**SUCCESS CRITERIA:**
- [ ] Empty answer from LLM → loop escalates to next mode
- [ ] After 5 iterations → yields fallback message
- [ ] Successful answer → yields response and returns (no extra iterations)
- [ ] `state.iteration` increments each loop cycle

---

## 🧭 Phase 3 — Decision Layer + Model Router

> **Goal:** Every input is classified before acting on it. Model selection is config-driven.  
> **Depends on:** Phase 2 complete.

---

### TASK 3.1 — DecisionOutput schema

**INPUT:** Nothing  
**OUTPUT:** Pydantic dataclass for decision output

**FILES TO CREATE:** `src/core/runtime/decision.py` (part 1)

```python
from dataclasses import dataclass
from typing import Literal

@dataclass
class DecisionOutput:
    intent: Literal["chat", "code", "action", "research", "vision"]
    complexity: Literal["low", "medium", "high"]
    mode: Literal["fast", "normal", "deep", "planning", "research"]
    requires_tools: bool
    requires_planning: bool
    prior_confidence: float  # 0.0–1.0
    model_preference: str = "auto"
```

**SUCCESS CRITERIA:**
- [ ] `DecisionOutput("chat","low","normal",False,False,0.8)` creates without error
- [ ] All fields accessible as attributes

---

### TASK 3.2 — DecisionLayer classifier

**INPUT:** `observation: str`  
**OUTPUT:** `DecisionOutput`

**FILES TO MODIFY:** `src/core/runtime/decision.py` (part 2, same file)

Implement keyword-based classifier exactly as shown in README Section 5.

Rules:
- Arabic + English keywords for each intent
- Complexity from word count + multi-step markers
- Mode derived from complexity + intent
- No LLM call inside this function

**SUCCESS CRITERIA:**
- [ ] `decide("open chrome")` → `intent="action"`, `requires_tools=True`
- [ ] `decide("what is Python?")` → `intent="chat"`, `requires_tools=False`
- [ ] `decide("write a function to sort a list")` → `intent="code"`
- [ ] `decide("search for news then summarize and save")` → `requires_planning=True`, `mode="planning"`
- [ ] All outputs are valid `DecisionOutput` instances

---

### TASK 3.3 — ModelRouter

**INPUT:** `DecisionOutput`  
**OUTPUT:** Model name string (e.g., `"qwen3:8b"`)

**FILES TO CREATE:** `src/models/llm/router.py`

Implement exactly as shown in README Section 6. Load rules from `config/models.yaml`, not hardcoded.

```python
class ModelRouter:
    def __init__(self, config_path: str = "config/models.yaml"):
        raw = yaml.safe_load(open(config_path))
        self.hard_rules = raw["routing"]["hard_rules"]
        self.mode_prefs = raw["routing"]["mode_preferences"]
        self.model_tags = {k: v["ollama_tag"] for k, v in raw["models"].items()}

    def select(self, decision: DecisionOutput) -> str:
        if decision.intent in self.hard_rules:
            key = self.hard_rules[decision.intent]
            return self.model_tags.get(key, key)
        key = self.mode_prefs.get(decision.mode, "qwen3:8b")
        return self.model_tags.get(key, key)
```

**SUCCESS CRITERIA:**
- [ ] `router.select(DecisionOutput(intent="vision",...))` returns `"llava:7b"`
- [ ] `router.select(DecisionOutput(intent="code",...))` returns `"qwen2.5-coder:7b"`
- [ ] `router.select(DecisionOutput(mode="fast",intent="chat",...))` returns `"gemma3:4b"`
- [ ] Model names come from config file, not Python constants

---

### TASK 3.4 — Wire Decision + Router into RuntimeLoop

**INPUT:** `DecisionLayer`, `ModelRouter`  
**OUTPUT:** Loop uses decision output to select model before LLM call

**FILES TO MODIFY:** `src/core/runtime/loop.py`

In `run()`, between observe and think:
```python
decision = self.decision.decide(observation)
model = self.router.select(decision)
state.mode = decision.mode
```

**SUCCESS CRITERIA:**
- [ ] "Open Chrome" → `gemma3:4b` selected (fast mode, action)
- [ ] "Explain quantum computing in detail" → `qwen3:8b` selected (deep/normal)
- [ ] `state.mode` correctly set from decision before LLM call

---

## 🔧 Phase 4 — Tool System

> **Goal:** The LLM can call tools. Tools are discovered automatically. Results feed back into the loop.  
> **Depends on:** Phase 3 complete.

---

### TASK 4.1 — BaseTool + ToolResult

**INPUT:** Nothing  
**OUTPUT:** Abstract base class for all skills

**FILES TO CREATE:** `src/skills/base.py`

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any
import time

@dataclass
class ToolResult:
    tool: str
    success: bool
    result: Any
    error: str | None = None
    duration_ms: int = 0

    def to_dict(self) -> dict:
        return {"tool": self.tool, "success": self.success,
                "result": str(self.result), "error": self.error,
                "duration_ms": self.duration_ms}

class BaseTool(ABC):
    name: str = ""
    description: str = ""
    category: str = ""
    requires_confirmation: bool = False

    @property
    @abstractmethod
    def input_schema(self) -> dict: ...

    @abstractmethod
    def execute(self, params: dict) -> ToolResult: ...

    def is_available(self) -> bool:
        return True

    def _run(self, params: dict) -> ToolResult:
        start = time.monotonic()
        try:
            result = self.execute(params)
            result.duration_ms = int((time.monotonic() - start) * 1000)
            return result
        except Exception as e:
            return ToolResult(self.name, False, None, str(e),
                              int((time.monotonic() - start) * 1000))
```

**SUCCESS CRITERIA:**
- [ ] Subclassing without `execute()` raises `TypeError`
- [ ] `ToolResult(...)` serializes to dict
- [ ] `_run()` catches exceptions and returns `ToolResult(success=False)`

---

### TASK 4.2 — Tool Registry

**INPUT:** `src/skills/` directory  
**OUTPUT:** Dict of all registered tools, exportable for LLM

**FILES TO CREATE:** `src/core/tools/registry.py`

```python
import importlib, inspect, pkgutil
from skills.base import BaseTool

class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, BaseTool] = {}

    def discover(self, package: str = "skills"):
        for finder, name, _ in pkgutil.walk_packages(
            importlib.import_module(package).__path__, prefix=package + "."
        ):
            try:
                mod = importlib.import_module(name)
                for _, cls in inspect.getmembers(mod, inspect.isclass):
                    if issubclass(cls, BaseTool) and cls is not BaseTool:
                        tool = cls()
                        if tool.name:
                            self.register(tool)
            except Exception:
                pass  # skip broken modules

    def register(self, tool: BaseTool):
        if tool.name in self._tools:
            raise ValueError(f"Duplicate tool name: {tool.name}")
        self._tools[tool.name] = tool

    def get(self, name: str) -> BaseTool | None:
        return self._tools.get(name)

    def list_enabled(self) -> list[BaseTool]:
        return [t for t in self._tools.values() if t.is_available()]

    def export_for_llm(self) -> list[dict]:
        return [
            {"type": "function", "function": {
                "name": t.name,
                "description": t.description,
                "parameters": t.input_schema,
            }}
            for t in self.list_enabled()
        ]
```

**SUCCESS CRITERIA:**
- [ ] `registry.discover()` finds `AppLauncherTool` after it's created in Phase 8
- [ ] `registry.export_for_llm()` returns valid Ollama tool format
- [ ] Duplicate name raises `ValueError`
- [ ] Unavailable tool excluded from `export_for_llm()`

---

### TASK 4.3 — Tool Validator

**INPUT:** Tool name (str) + params (dict)  
**OUTPUT:** `(is_valid: bool, errors: list[str])`

**FILES TO CREATE:** `src/core/tools/validator.py`

```python
import jsonschema

class ToolValidator:
    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    def validate(self, tool_name: str, params: dict) -> tuple[bool, list[str]]:
        tool = self.registry.get(tool_name)
        if not tool:
            return False, [f"Tool '{tool_name}' not found"]
        try:
            jsonschema.validate(params, tool.input_schema)
            return True, []
        except jsonschema.ValidationError as e:
            return False, [e.message]
```

**SUCCESS CRITERIA:**
- [ ] Valid params → `(True, [])`
- [ ] Missing required field → `(False, ["'app_name' is a required property"])`
- [ ] Unknown tool → `(False, ["Tool 'xyz' not found"])`

---

### TASK 4.4 — Tool Executor

**INPUT:** Tool name + params  
**OUTPUT:** `ToolResult`

**FILES TO CREATE:** `src/core/tools/executor.py`

```python
import concurrent.futures
from core.tools.registry import ToolRegistry
from core.tools.validator import ToolValidator
from logger import logger

class ToolExecutor:
    def __init__(self, registry: ToolRegistry, timeout: int = 30):
        self.registry = registry
        self.validator = ToolValidator(registry)
        self.timeout = timeout

    def execute(self, tool_name: str, params: dict) -> ToolResult:
        # 1. Validate
        valid, errors = self.validator.validate(tool_name, params)
        if not valid:
            return ToolResult(tool_name, False, None, f"validation: {errors[0]}")

        # 2. Get tool
        tool = self.registry.get(tool_name)

        # 3. Execute with timeout
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            future = pool.submit(tool._run, params)
            try:
                result = future.result(timeout=self.timeout)
            except concurrent.futures.TimeoutError:
                return ToolResult(tool_name, False, None, f"timeout after {self.timeout}s")

        # 4. Log
        logger.debug(f"Tool {tool_name}: success={result.success} duration={result.duration_ms}ms")
        return result
```

**SUCCESS CRITERIA:**
- [ ] Valid call → `ToolResult(success=True)`
- [ ] Invalid params → `ToolResult(success=False, error="validation: ...")`
- [ ] Tool takes > 30s → `ToolResult(success=False, error="timeout after 30s")`
- [ ] Every execution logged to console/file

---

### TASK 4.5 — Wire tool execution into RuntimeLoop Act step

**INPUT:** LLM output that may contain a `tool_call` block  
**OUTPUT:** Tool result injected as next observation

**FILES TO MODIFY:** `src/core/runtime/loop.py`

Add after `think()`:
```python
if llm_output.has_tool_call:
    result = self.executor.execute(
        llm_output.tool_call["name"],
        llm_output.tool_call["args"]
    )
    state.add_tool_result(result)
    continue  # back to observe() with tool result in state
```

Also add `parse_tool_call()` helper to extract JSON tool call from LLM text.

**SUCCESS CRITERIA:**
- [ ] LLM emitting `{"tool_call": {"name": "app_launcher", "args": {...}}}` triggers executor
- [ ] Tool result appears in next `observe()` output
- [ ] Failed tool → `state.tool_traces` has `success=False` → evaluator escalates

---

## 📥 Phase 5 — Context Buffer

> **Goal:** Stage multiple inputs (text + files + images) before the loop runs.  
> **Depends on:** Phase 4 complete.

---

### TASK 5.1 — Context Buffer

**INPUT:** Text string, file path, image path, or audio path  
**OUTPUT:** Staged snapshot readable by runtime

**FILES TO CREATE:** `src/core/context/buffer.py`

```python
import uuid, time, threading
from dataclasses import dataclass, field
from typing import Literal

@dataclass
class InputItem:
    id: str
    type: Literal["text", "file", "image", "audio"]
    content: str          # text OR file path
    mime_type: str = ""
    source: str = "cli"
    timestamp: float = field(default_factory=time.time)

class ContextBuffer:
    def __init__(self, ttl_seconds: int = 300):
        self._items: dict[str, InputItem] = {}
        self._ttl = ttl_seconds
        self._lock = threading.Lock()

    def add(self, item: InputItem) -> str:
        item.id = str(uuid.uuid4())
        with self._lock:
            self._evict_stale()
            self._items[item.id] = item
        return item.id

    def snapshot(self) -> list[InputItem]:
        with self._lock:
            self._evict_stale()
            return list(self._items.values())

    def clear(self):
        with self._lock:
            self._items.clear()

    def _evict_stale(self):
        now = time.time()
        stale = [k for k, v in self._items.items() if now - v.timestamp > self._ttl]
        for k in stale:
            del self._items[k]
```

**SUCCESS CRITERIA:**
- [ ] `buffer.add(item)` returns UUID string
- [ ] `buffer.snapshot()` returns all staged items
- [ ] `buffer.clear()` empties buffer
- [ ] Items older than TTL are auto-evicted
- [ ] Thread-safe (two simultaneous adds don't corrupt state)

---

## 💾 Phase 6 — Memory

> **Goal:** Jarvis remembers conversations. A fact from session 1 is recalled in session 2.  
> **Depends on:** Phase 5 complete.

---

### TASK 6.1 — Short-term memory (Redis + fallback)

**INPUT:** `role: str`, `content: str`, `session_id: str`  
**OUTPUT:** Stored + retrievable conversation history

**FILES TO CREATE:** `src/core/memory/short_term.py`

```python
class ShortTermMemory:
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        try:
            import redis
            self._redis = redis.from_url(redis_url, decode_responses=True)
            self._redis.ping()
            self._backend = "redis"
        except Exception:
            self._redis = None
            self._backend = "memory"
            self._store: dict[str, list] = {}

    def save(self, role: str, content: str, session_id: str):
        msg = json.dumps({"role": role, "content": content, "ts": time.time()})
        if self._backend == "redis":
            self._redis.rpush(f"history:{session_id}", msg)
            self._redis.ltrim(f"history:{session_id}", -50, -1)  # keep last 50
        else:
            self._store.setdefault(session_id, []).append(json.loads(msg))

    def get_history(self, session_id: str, n: int = 20) -> list[dict]:
        if self._backend == "redis":
            raw = self._redis.lrange(f"history:{session_id}", -n, -1)
            return [json.loads(r) for r in raw]
        return self._store.get(session_id, [])[-n:]
```

**SUCCESS CRITERIA:**
- [ ] `save("user", "Hello", "s1")` stores message
- [ ] `get_history("s1")` returns messages in order
- [ ] Redis offline → automatic fallback to in-memory (no crash, no error shown to user)
- [ ] Max 50 messages kept per session

---

### TASK 6.2 — Long-term memory (ChromaDB)

**INPUT:** Fact string + optional metadata  
**OUTPUT:** Semantically searchable memory

**FILES TO CREATE:** `src/core/memory/long_term.py`

```python
import chromadb
from sentence_transformers import SentenceTransformer

class LongTermMemory:
    def __init__(self, db_path: str = "data/chroma/"):
        self._client = chromadb.PersistentClient(path=db_path)
        self._collection = self._client.get_or_create_collection("jarvis_memory")
        self._embed = SentenceTransformer("all-MiniLM-L6-v2")

    def remember(self, text: str, metadata: dict = {}):
        embedding = self._embed.encode(text).tolist()
        self._collection.add(
            documents=[text],
            embeddings=[embedding],
            metadatas=[metadata],
            ids=[str(uuid.uuid4())]
        )

    def recall(self, query: str, n: int = 5) -> list[str]:
        embedding = self._embed.encode(query).tolist()
        results = self._collection.query(query_embeddings=[embedding], n_results=n)
        return results["documents"][0] if results["documents"] else []
```

**SUCCESS CRITERIA:**
- [ ] `remember("User's name is Ahmed")` stores fact
- [ ] `recall("what is the user's name?")` returns that fact as top result
- [ ] Facts persist across Python process restarts (ChromaDB persistent)

---

### TASK 6.3 — SQLite database

**INPUT:** Operations on conversations/facts/tasks/feedback tables  
**OUTPUT:** Persistent structured storage

**FILES TO CREATE:** `src/core/memory/database.py`

Schema:
```sql
CREATE TABLE IF NOT EXISTS conversations (
    id TEXT PRIMARY KEY, session_id TEXT, role TEXT,
    content TEXT, timestamp REAL, model TEXT
);
CREATE TABLE IF NOT EXISTS facts (
    id TEXT PRIMARY KEY, content TEXT, source TEXT,
    category TEXT, created_at REAL
);
CREATE TABLE IF NOT EXISTS tasks (
    id TEXT PRIMARY KEY, title TEXT, status TEXT,
    created_at REAL, updated_at REAL, run_id TEXT
);
CREATE TABLE IF NOT EXISTS feedback (
    id TEXT PRIMARY KEY, turn_id TEXT, model TEXT,
    mode TEXT, score REAL, timestamp REAL
);
```

**SUCCESS CRITERIA:**
- [ ] Schema auto-created on import (no manual migration needed)
- [ ] CRUD for all 4 tables works
- [ ] All queries parameterized (no f-string SQL)
- [ ] Data survives process restart

---

### TASK 6.4 — Memory Manager (unified interface)

**INPUT:** Query or save request  
**OUTPUT:** Results from the right backend

**FILES TO CREATE:** `src/core/memory/manager.py`

```python
class MemoryManager:
    def __init__(self):
        self.short = ShortTermMemory()
        self.long = LongTermMemory()
        self.db = Database()

    def save_turn(self, role: str, content: str, session_id: str):
        self.short.save(role, content, session_id)
        self.db.insert_conversation(role, content, session_id)

    def get_context(self, session_id: str, n: int = 10) -> list[dict]:
        return self.short.get_history(session_id, n)

    def search(self, query: str, n: int = 5) -> list[str]:
        return self.long.recall(query, n)

    def remember(self, text: str, metadata: dict = {}):
        self.long.remember(text, metadata)
```

**SUCCESS CRITERIA:**
- [ ] `save_turn()` writes to both short-term and SQLite
- [ ] `get_context()` returns formatted message list
- [ ] `search()` returns relevant strings

---

### TASK 6.5 — User Profile

**INPUT:** `user_id: str`  
**OUTPUT:** Loaded or default user profile

**FILES TO CREATE:** `src/core/identity/user_profile.py`

```python
@dataclass
class UserProfile:
    user_id: str
    display_name: str = ""
    language: str = "auto"           # ar | en | auto
    response_style: str = "balanced" # concise | balanced | detailed
    technical_level: str = "auto"

    @classmethod
    def load(cls, user_id: str) -> "UserProfile":
        path = Path(f"data/profiles/{user_id}.json")
        if path.exists():
            return cls(**json.loads(path.read_text()))
        return cls(user_id=user_id)

    @classmethod
    def default(cls) -> "UserProfile":
        return cls(user_id="default")

    def save(self):
        path = Path(f"data/profiles/{self.user_id}.json")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(asdict(self)))
```

**SUCCESS CRITERIA:**
- [ ] `UserProfile.load("nonexistent")` returns default profile (no crash)
- [ ] Saved profile loaded correctly on next call
- [ ] `UserProfile.default()` never raises

---

### TASK 6.6 — Prompt Builder

**INPUT:** `mode: str`, `profile: UserProfile`, optional `tools: list`, `task_context: str`  
**OUTPUT:** Complete system prompt string

**FILES TO CREATE:** `src/core/identity/prompt_builder.py`

```python
MODE_PACKS = {
    "fast":     "أجب مباشرةً وبإيجاز. بدون مقدمات.",
    "normal":   "أعطِ إجابة واضحة وكاملة.",
    "deep":     "فكّر خطوة بخطوة. تحقق من صحة إجابتك.",
    "planning": "قسّم المهمة إلى خطوات مرقّمة قبل البدء.",
    "research": "اجمع المعلومات من زوايا متعددة. أشر إلى المصادر.",
}

JARVIS_IDENTITY = open("config/identity.yaml").read()  # cached on module load
SAFETY_BLOCK = "لا تنفذ أوامر تضر بالنظام أو تكشف بيانات حساسة. اطلب تأكيداً قبل العمليات الخطرة."

class PromptBuilder:
    def build(self, mode: str, profile: UserProfile,
              tools: list[str] = [], task_context: str = "") -> str:
        parts = [
            f"أنت {JARVIS_IDENTITY}",   # identity
            SAFETY_BLOCK,               # safety
        ]

        if profile.language == "ar":
            parts.append("أجب دائماً باللغة العربية.")
        if profile.response_style == "concise":
            parts.append("اجعل إجاباتك موجزة.")

        parts.append(MODE_PACKS.get(mode, MODE_PACKS["normal"]))

        if tools:
            parts.append(f"الأدوات المتاحة: {', '.join(tools)}")
        if task_context:
            parts.append(f"السياق: {task_context}")

        return "\n\n".join(parts)
```

**SUCCESS CRITERIA:**
- [ ] Output always starts with Jarvis identity
- [ ] Arabic profile → Arabic instruction in prompt
- [ ] `mode="fast"` → short mode fragment in prompt
- [ ] Tools list non-empty → tools section included
- [ ] Deterministic: same inputs → same output every call

---

## 🤖 Phase 7 — Agents

> **Goal:** Multi-step reasoning and planning without user guidance.  
> **Depends on:** Phase 4 (tools) + Phase 6 (memory) complete.

---

### TASK 7.1 — Planner agent

**INPUT:** `goal: str` (complex multi-step task)  
**OUTPUT:** Ordered list of `Step` objects

**FILES TO CREATE:** `src/core/agents/planner.py`

```python
@dataclass
class Step:
    id: str
    title: str
    tool: str | None          # tool name or None for LLM-only step
    inputs: dict
    depends_on: list[str]     # step IDs
    result: Any = None
    done: bool = False

class Planner:
    def decompose(self, goal: str, context: str = "") -> list[Step]:
        # Ask LLM (planning mode) to break goal into steps
        # Parse numbered list response into Step objects
        ...

    def execute(self, steps: list[Step], executor: ToolExecutor,
                llm: OllamaEngine) -> Generator[str, None, None]:
        # Execute steps in dependency order
        # Yield progress updates
        ...
```

**SUCCESS CRITERIA:**
- [ ] "Search X and save to file" → 2 steps: [search, save]
- [ ] Step 2 runs only after Step 1 completes
- [ ] Step 1 result passed as input to Step 2

---

### TASK 7.2 — Thinker agent

**INPUT:** Complex question + context  
**OUTPUT:** `{answer: str, reasoning: list[str], confidence: float}`

**FILES TO CREATE:** `src/core/agents/thinker.py`

```python
class Thinker:
    def reason(self, question: str, context: str, llm: OllamaEngine) -> dict:
        # Use qwen3:8b in deep mode
        # Chain-of-thought: break into sub-questions first
        # Self-verify: ask "is this answer complete?"
        ...
```

**SUCCESS CRITERIA:**
- [ ] Multi-part question → answer includes reasoning steps
- [ ] `confidence` field between 0.0 and 1.0
- [ ] Uses `qwen3:8b` only (no hardcoded model name in code)

---

### TASK 7.3 — Researcher agent

**INPUT:** Research topic  
**OUTPUT:** `{summary: str, key_points: list[str], sources: list[str]}`

**FILES TO CREATE:** `src/core/agents/researcher.py`

Requirements:
- Run 3–5 distinct web search queries
- Summarize top results per query
- Requires `web_search` skill (Phase 8)

**SUCCESS CRITERIA:**
- [ ] Returns at least 3 key points
- [ ] `sources` contains real URLs
- [ ] Works even if one query returns no results

---

### TASK 7.4 — Wire Orchestrator

**INPUT:** `DecisionOutput`  
**OUTPUT:** Correct handler called (Planner | Researcher | ToolExecutor | direct LLM)

**FILES TO CREATE:**
- `src/core/orchestrator/dispatcher.py`
- `src/core/orchestrator/agent_selector.py`

```python
class Dispatcher:
    def route(self, decision: DecisionOutput, state: TurnState) -> str:
        if decision.requires_planning:
            return "planner"
        if decision.intent == "research":
            return "researcher"
        if decision.requires_tools:
            return "tool_executor"
        return "direct_llm"
```

**SUCCESS CRITERIA:**
- [ ] `requires_planning=True` → Planner
- [ ] `intent="research"` and `requires_planning=False` → Researcher
- [ ] `requires_tools=True, requires_planning=False` → ToolExecutor
- [ ] `intent="chat"` → direct LLM

---

## 🛠️ Phase 8 — Skills

> **Goal:** Concrete tool implementations: open apps, search web, read clipboard, run code.  
> **Depends on:** Phase 4 (tool system) complete.

---

### TASK 8.1 — AppLauncherTool

**INPUT:** `{"app_name": str}`  
**OUTPUT:** `ToolResult(success=True, result="Chrome launched (PID XXXX)")`

**FILES TO CREATE:** `src/skills/system/app_launcher.py`
**FILES TO CREATE:** `config/schemas/system/app_launcher.schema.json`

Schema:
```json
{"type": "object", "required": ["app_name"],
 "properties": {"app_name": {"type": "string", "minLength": 1}}}
```

Search order: PATH → Start Menu shortcuts → Program Files → AppData

**SUCCESS CRITERIA:**
- [ ] `execute({"app_name": "notepad"})` → Notepad opens
- [ ] `execute({"app_name": "chrome"})` → Chrome opens (if installed)
- [ ] Unknown app → `ToolResult(success=False, error="App 'xyz' not found")`
- [ ] Tool registered in registry after `registry.discover()`

---

### TASK 8.2 — FileOpsTool

**INPUT:** `{"operation": "list|read|write|delete", "path": str, "content?": str}`  
**OUTPUT:** `ToolResult` with file content or confirmation

**FILES TO CREATE:** `src/skills/system/file_ops.py`

Requirements:
- `delete` → moves to Recycle Bin (not permanent)
- `write` → creates parent directories if needed
- Path must be under allowed roots (configurable)
- `requires_confirmation = True` for delete

**SUCCESS CRITERIA:**
- [ ] `read("README.md")` → returns file content
- [ ] `write("data/test.txt", "hello")` → file created
- [ ] `delete(...)` → `requires_confirmation=True` in class definition
- [ ] Path outside allowed dirs → `ToolResult(success=False, error="access denied")`

---

### TASK 8.3 — WebSearchTool

**INPUT:** `{"query": str, "max_results": int (default 5)}`  
**OUTPUT:** `ToolResult(result=[{title, snippet, url}])`

**FILES TO CREATE:** `src/skills/search/web_search.py`

Requirements:
- DuckDuckGo HTML (no API key)
- TTL cache: same query within 5 min → cached result
- Optional full page extraction via `trafilatura`

**SUCCESS CRITERIA:**
- [ ] `execute({"query": "Python 3.13"})` returns ≥ 3 results
- [ ] Each result has `title`, `snippet`, `url`
- [ ] Works with no API key configured
- [ ] Second identical query within 5 min → returns cached (no network call)

---

### TASK 8.4 — ClipboardTool

**INPUT:** `{"operation": "read|write", "content?": str}`  
**OUTPUT:** Clipboard content or write confirmation

**FILES TO CREATE:** `src/skills/system/clipboard.py`

**SUCCESS CRITERIA:**
- [ ] `read` → returns current clipboard text
- [ ] `write` → sets clipboard text
- [ ] Image on clipboard → `"[IMAGE saved to data/clipboard.png]"`

---

### TASK 8.5 — CodeExecutorTool

**INPUT:** `{"language": "python|shell", "code": str}`  
**OUTPUT:** `{stdout, stderr, returncode, duration_ms}`

**FILES TO CREATE:** `src/skills/coder/code_executor.py`

Requirements:
- Subprocess isolation
- 30s timeout (configurable)
- Shell blocklist: `rm -rf /`, `format`, `del /s`, `shutdown`
- `requires_confirmation = True` for shell

**SUCCESS CRITERIA:**
- [ ] `python print("hi")` → `stdout="hi\n"`, `returncode=0`
- [ ] Timeout → `ToolResult(success=False, error="timeout after 30s")`
- [ ] Blocked pattern → `ToolResult(success=False, error="blocked: dangerous pattern detected")`

---

### TASK 8.6 — BrowserTool + SessionManager

**INPUT:** `{"action": "navigate|click|fill|extract|screenshot", ...params}`  
**OUTPUT:** `ToolResult` with page content or confirmation

**FILES TO CREATE:**
- `src/skills/browser/browser.py`
- `src/skills/browser/session_manager.py`

Session manager saves Playwright storage state per domain. Reloaded on next run.

**SUCCESS CRITERIA:**
- [ ] `navigate("https://example.com")` → returns page title
- [ ] Login to test site → save session → restart Python → session reloaded (no re-login)
- [ ] `extract()` returns page Markdown content

---

## 🛡️ Phase 9 — Safety

> **Goal:** Dangerous operations require explicit user confirmation.  
> **Depends on:** Phase 8 complete.

---

### TASK 9.1 — Safety classifier

**INPUT:** Tool name + params  
**OUTPUT:** `"safe" | "risky" | "critical"`

**FILES TO CREATE:** `src/core/safety/classifier.py`

```python
SAFETY_RULES = {
    "safe":     ["app_launcher", "web_search", "system_info", "screenshot", "clipboard.read"],
    "risky":    ["file_ops.write", "file_ops.move", "clipboard.write", "code_executor.python"],
    "critical": ["file_ops.delete", "gmail.send", "code_executor.shell", "calendar.delete"],
}

class SafetyClassifier:
    def classify(self, tool_name: str, params: dict) -> str:
        for level, tools in reversed(list(SAFETY_RULES.items())):
            if any(tool_name.startswith(t) for t in tools):
                return level
        return "risky"  # unknown tools default to risky
```

**SUCCESS CRITERIA:**
- [ ] `classify("app_launcher", ...)` → `"safe"`
- [ ] `classify("file_ops.delete", ...)` → `"critical"`
- [ ] `classify("gmail.send", ...)` → `"critical"`
- [ ] Unknown tool → `"risky"` (not silent approval)

---

### TASK 9.2 — Confirmation gate

**INPUT:** Safety class + tool name  
**OUTPUT:** User approves or denies

**FILES TO CREATE:** `src/core/safety/confirmation.py`

```python
class ConfirmationGate:
    def request(self, tool_name: str, params: dict, safety: str) -> bool:
        if safety == "safe":
            return True
        if safety == "risky":
            return True  # auto-approve risky but log

        # CRITICAL: must ask user
        summary = f"{tool_name}({json.dumps(params, ensure_ascii=False)[:80]})"
        answer = input(f"\n⚠️  Critical action: {summary}\nProceed? [y/N] ").strip().lower()
        return answer == "y"
```

**SUCCESS CRITERIA:**
- [ ] `SAFE` → returns `True` immediately
- [ ] `CRITICAL` → prints confirmation prompt → `"y"` returns `True`, anything else `False`
- [ ] Denied action → `ToolResult(success=False, error="user denied")` from executor

---

## 🌐 Phase 10 — Google APIs

> **Depends on:** Phase 8 (browser for OAuth redirect) + Phase 4 (tool system).

---

### TASK 10.1 — Google OAuth manager

**FILES TO CREATE:** `src/skills/api/google_auth.py`

Single OAuth2 flow granting Calendar + Gmail + Drive + Contacts + YouTube. Token saved to `data/google_token.json`. Auto-refresh on expiry.

**SUCCESS CRITERIA:**
- [ ] OAuth flow completes, token saved
- [ ] Second run: token loaded, no re-auth
- [ ] Expired token: auto-refreshed silently

---

### TASK 10.2 — Calendar, Gmail, Drive tools

**FILES TO CREATE:**
- `src/skills/api/calendar.py`
- `src/skills/api/gmail.py`
- `src/skills/api/drive.py`

**SUCCESS CRITERIA:**
- [ ] Calendar: create → list → delete test event
- [ ] Gmail: send to self → search → read
- [ ] Drive: upload → list → download → verify content
- [ ] All three use same OAuth token

---

## 💻 Phase 11 — CLI Interface (Full)

> **Depends on:** Phases 1–9 complete.

---

### TASK 11.1 — Full CLI with Rich + slash commands

**FILES TO MODIFY:** `src/interfaces/cli/interface.py`
**FILES TO CREATE:** `src/interfaces/cli/commands.py`

Commands: `/clear`, `/model`, `/mode`, `/memory`, `/tools`, `/status`, `/help`

**SUCCESS CRITERIA:**
- [ ] Arabic text displays right-aligned
- [ ] Response streams token-by-token
- [ ] All slash commands respond correctly
- [ ] Status bar shows model + mode

---

## Phases 12–16 (after Phase 11)

| Phase | Builds | Key SUCCESS |
|---|---|---|
| 12 | Web UI (FastAPI + WebSocket + HTML) | Browser chat with streaming Arabic RTL |
| 13 | Voice pipeline (Whisper + Piper + wake word) | Full cycle < 15s |
| 14 | Telegram bot + PyQt6 GUI | Voice note → transcription → reply |
| 15 | Logging + Observability | JSON logs for decisions, tools, models |
| 16 | Optimization + QA | VRAM < 5.5 GB, cold start < 10s, all e2e tests pass |

---

## 🧪 Vertical Slice Acceptance Tests

These two tests must pass after Phase 8. They exercise the full stack.

### Test A: "Say Hello" (no tools)
```python
loop = RuntimeLoop()  # with Decision + Router wired
response = "".join(loop.run("Hello", session_id="test"))
assert len(response) > 0
assert "error" not in response.lower()
```

### Test B: "Open Notepad" (tool execution)
```python
# 1. Jarvis receives "open notepad"
# 2. Decision: intent=action, requires_tools=True
# 3. LLM emits tool_call: app_launcher(app_name="notepad")
# 4. Executor runs app_launcher
# 5. Notepad process appears in process list
# 6. Response: "Notepad is now open."

import psutil
response = "".join(loop.run("open notepad", session_id="test"))
notepad_running = any("notepad" in p.name().lower() for p in psutil.process_iter())
assert notepad_running
```

Both tests must pass before moving to Phase 9.
