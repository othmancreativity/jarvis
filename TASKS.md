# 🗂️ JARVIS — Task Board (Production Blueprint)

> **Every task contains:** DESCRIPTION · INPUT · OUTPUT · FILES · IMPLEMENTATION · SUCCESS CRITERIA
>
> **Rule:** Do not start a phase until the previous phase's end state is verified.
> **Rule:** Phase 0 is mandatory first. No exceptions.

---

## 📊 Progress Tracker

| Phase | Name | Tasks | Done | End State |
|-------|------|-------|------|-----------|
| 0 | First Working System | 5 | 0 | "open chrome" executes |
| 1 | Foundation | 8 | 0 | `main.py --interface cli` boots |
| 2 | Runtime Loop | 8 | 0 | Full turn: input → LLM → output |
| 3 | Decision System | 5 | 0 | Intent classified; model selected |
| 4 | Tool System | 5 | 0 | Any skill callable via LLM |
| 5 | System Control Skills | 8 | 0 | OS fully controllable |
| 6 | Browser & Web Skills | 6 | 0 | Browser automation + sessions |
| 7 | Google APIs | 7 | 0 | Calendar/Gmail/Drive work |
| 8 | Context + Memory | 6 | 0 | Facts persist across sessions |
| 9 | Agents | 5 | 0 | Multi-step goals execute |
| 10 | Safety + Capabilities | 4 | 0 | Dangerous ops blocked/confirmed |
| 11 | Logging + Feedback | 4 | 0 | Decisions logged; weights update |
| 12 | CLI Interface | 5 | 0 | Rich terminal chat works |
| 13 | Web UI | 12 | 0 | Premium glassmorphism chat |
| 14 | Voice Pipeline | 5 | 0 | "Hey Jarvis" → spoken answer |
| 15 | Vision + Image Gen | 4 | 0 | Image understood + generated |
| 16 | Telegram + GUI | 4 | 0 | Bot + desktop app working |
| 17 | QA + Security | 7 | 0 | Tests pass; credentials safe |

---

## 🚀 Phase 0 — First Working System

> **End state:** User types "open chrome" → Chrome opens. This proves the full pipe works.
> **Time estimate:** 2-4 hours.

---

### TASK 0.1 — Minimal Ollama chat call

**DESCRIPTION:** Prove Ollama is connected and responding.

**INPUT:** String "hello"
**OUTPUT:** String response printed to terminal

**FILES:**
- CREATE: `src/models/llm/engine.py`

**IMPLEMENTATION:**
```python
# src/models/llm/engine.py
import ollama

def chat(message: str, model: str = "qwen3:8b", system: str = "") -> str:
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": message})
    
    response = ollama.chat(model=model, messages=messages)
    return response["message"]["content"]

def stream_chat(message: str, model: str = "qwen3:8b", system: str = ""):
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": message})
    
    stream = ollama.chat(model=model, messages=messages, stream=True)
    for chunk in stream:
        token = chunk["message"]["content"]
        if token:
            yield token

if __name__ == "__main__":
    print(chat("hello"))
```

**SUCCESS CRITERIA:**
- `python src/models/llm/engine.py` prints a coherent English or Arabic response
- No exception raised
- Response takes < 30 seconds

---

### TASK 0.2 — Intent classifier (JSON output)

**DESCRIPTION:** Given a user message, classify it and return structured JSON.

**INPUT:** String "open chrome"
**OUTPUT:** `{"intent": "tool_use", "tool": "open_app", "args": {"name": "chrome"}}`

**FILES:**
- CREATE: `src/core/decision/classifier.py`

**IMPLEMENTATION:**
```python
# src/core/decision/classifier.py
import json
from src.models.llm.engine import chat

SYSTEM = """You are a command classifier. Return ONLY valid JSON, nothing else.

Schema:
{
  "intent": "chat|code|tool_use|search|vision|research",
  "complexity": "low|medium|high",
  "mode": "fast|normal|deep|planning|research",
  "model": "gemma3:4b|qwen3:8b|qwen2.5-coder:7b|llava:7b",
  "requires_tools": true|false,
  "requires_planning": true|false,
  "tool_name": "tool_name_or_null",
  "tool_args": {}
}

Rules:
- Short, simple → fast, gemma3:4b
- Code → qwen2.5-coder:7b
- Multi-step goals → planning, qwen3:8b
- App/file/browser operations → tool_use
- Questions/conversation → chat

Examples:
"open chrome" → {"intent":"tool_use","complexity":"low","mode":"fast","model":"gemma3:4b","requires_tools":true,"requires_planning":false,"tool_name":"open_app","tool_args":{"name":"chrome"}}
"what is AI?" → {"intent":"chat","complexity":"low","mode":"fast","model":"gemma3:4b","requires_tools":false,"requires_planning":false,"tool_name":null,"tool_args":{}}
"افتح Chrome" → {"intent":"tool_use","complexity":"low","mode":"fast","model":"gemma3:4b","requires_tools":true,"requires_planning":false,"tool_name":"open_app","tool_args":{"name":"chrome"}}
"""

def classify(message: str) -> dict:
    raw = chat(message, model="gemma3:4b", system=SYSTEM)
    # Strip any markdown code blocks if present
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())
```

**SUCCESS CRITERIA:**
- `classify("open chrome")` returns dict with `intent="tool_use"` and `tool_name="open_app"`
- `classify("what is AI?")` returns dict with `intent="chat"`
- `classify("افتح Chrome")` returns same as "open chrome"
- No JSONDecodeError on any of the above

---

### TASK 0.3 — App launcher tool

**DESCRIPTION:** Open an application by name on Windows/Linux/macOS.

**INPUT:** `{"name": "chrome"}`
**OUTPUT:** App opens. Returns `{"success": True, "pid": 4521}`

**FILES:**
- CREATE: `src/skills/system/apps.py`

**IMPLEMENTATION:**
```python
# src/skills/system/apps.py
import subprocess, shutil, platform, os
from pathlib import Path

PLATFORM = platform.system().lower()

def open_app(name: str) -> dict:
    """Open an application by name. Searches PATH, then platform-specific locations."""
    
    # 1. Try PATH directly
    exe = shutil.which(name) or shutil.which(f"{name}.exe")
    if exe:
        proc = subprocess.Popen([exe])
        return {"success": True, "pid": proc.pid, "path": exe}
    
    if PLATFORM == "windows":
        return _open_windows(name)
    elif PLATFORM == "linux":
        return _open_linux(name)
    elif PLATFORM == "darwin":
        return _open_macos(name)
    
    return {"success": False, "error": f"App '{name}' not found"}

def _open_windows(name: str) -> dict:
    search_dirs = [
        os.environ.get("PROGRAMFILES", "C:/Program Files"),
        os.environ.get("PROGRAMFILES(X86)", "C:/Program Files (x86)"),
        os.environ.get("LOCALAPPDATA", ""),
        os.environ.get("APPDATA", ""),
    ]
    for d in search_dirs:
        if not d or not Path(d).exists():
            continue
        for exe_path in Path(d).rglob(f"*{name}*.exe"):
            try:
                proc = subprocess.Popen([str(exe_path)])
                return {"success": True, "pid": proc.pid, "path": str(exe_path)}
            except (PermissionError, OSError):
                continue
    return {"success": False, "error": f"App '{name}' not found on Windows"}

def _open_linux(name: str) -> dict:
    proc = subprocess.Popen([name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return {"success": True, "pid": proc.pid}

def _open_macos(name: str) -> dict:
    result = subprocess.run(["open", "-a", name], capture_output=True)
    if result.returncode == 0:
        return {"success": True}
    return {"success": False, "error": result.stderr.decode()}

def close_app(name: str) -> dict:
    """Close an application by name."""
    if PLATFORM == "windows":
        result = subprocess.run(["taskkill", "/IM", f"{name}.exe", "/F"], capture_output=True)
        return {"success": result.returncode == 0}
    else:
        result = subprocess.run(["pkill", "-f", name], capture_output=True)
        return {"success": result.returncode == 0}
```

**SUCCESS CRITERIA:**
- `open_app("notepad")` on Windows → Notepad opens + success=True returned
- `open_app("gedit")` on Linux → gedit opens (or appropriate editor)
- `open_app("nonexistent_xyz")` → returns `{"success": False, "error": "..."}`
- `close_app("notepad")` → Notepad closes

---

### TASK 0.4 — Wire: classifier → tool → output

**DESCRIPTION:** Connect the three pieces into one runnable script.

**INPUT:** String from `input()` in terminal
**OUTPUT:** App opens + confirmation printed, OR conversational answer

**FILES:**
- CREATE: `app/jarvis_slice.py`

**IMPLEMENTATION:**
```python
# app/jarvis_slice.py — Phase 0 proof of concept
import json
from src.models.llm.engine import chat
from src.core.decision.classifier import classify
from src.skills.system.apps import open_app, close_app

TOOL_MAP = {
    "open_app": open_app,
    "close_app": close_app,
}

def run(user_input: str):
    print(f"\nClassifying: '{user_input}'")
    
    try:
        decision = classify(user_input)
        print(f"Decision: {json.dumps(decision, ensure_ascii=False, indent=2)}")
    except (json.JSONDecodeError, Exception) as e:
        print(f"Classification failed: {e}. Defaulting to chat.")
        decision = {"intent": "chat", "requires_tools": False}
    
    if decision.get("requires_tools") and decision.get("tool_name") in TOOL_MAP:
        tool_fn = TOOL_MAP[decision["tool_name"]]
        result = tool_fn(**decision.get("tool_args", {}))
        print(f"\n✓ Tool result: {result}")
    else:
        response = chat(user_input)
        print(f"\nJarvis: {response}")

if __name__ == "__main__":
    print("Jarvis Phase 0 — type 'quit' to exit\n")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "quit":
            break
        if user_input:
            run(user_input)
```

**SUCCESS CRITERIA:**
- `python app/jarvis_slice.py`
- Type "open notepad" → Notepad opens + confirmation printed
- Type "what is machine learning?" → conversational answer printed
- Type "quit" → exits cleanly

---

### TASK 0.5 — Arabic input test

**DESCRIPTION:** Verify Arabic commands work identically to English.

**INPUT:** Arabic commands typed at prompt
**OUTPUT:** Same behavior as English equivalents

**FILES:** No new files — test against existing code

**TEST CASES:**
```
"افتح Notepad"          → Notepad opens
"ما هو الذكاء الاصطناعي؟"  → Arabic answer printed
"أغلق Notepad"           → Notepad closes
```

**SUCCESS CRITERIA:**
- All three Arabic commands produce correct behavior
- If classifier fails on Arabic: add 3 more Arabic examples to SYSTEM prompt in Task 0.2 and retry

---

## 🏗️ Phase 1 — Foundation

> **End state:** `python app/main.py --interface cli` boots, loads config, starts logging, shows "Jarvis ready."

---

### TASK 1.1 — Configuration system

**DESCRIPTION:** Load all settings from YAML + .env into a typed Python object.

**INPUT:** `config/settings.yaml` + `.env`
**OUTPUT:** `get_settings()` returns `AppSettings` Pydantic object

**FILES:**
- CREATE: `config/settings.example.yaml`
- CREATE: `config/settings.yaml` (copy from example)
- CREATE: `src/core/config.py`

**IMPLEMENTATION:**

`config/settings.example.yaml`:
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
  model_idle_timeout_s: 300

interfaces:
  web_host: "127.0.0.1"
  web_port: 8080
  telegram_polling_timeout: 30

paths:
  data: "data"
  logs: "logs"
  chroma: "data/chroma"
  sqlite: "data/jarvis.db"
  sessions: "data/sessions"
  downloads: "data/downloads"
  screenshots: "data/screenshots"
  generated: "data/generated"

hotkeys:
  open_cli: "ctrl+alt+j"
  start_voice: "ctrl+alt+s"

runtime:
  max_iterations: 5
  max_escalation_depth: 2
  turn_timeout_s: 120
  tool_timeout_s: 30
```

`src/core/config.py`:
```python
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from pathlib import Path
import yaml
from functools import lru_cache

class JarvisConfig(BaseModel):
    name: str = "Jarvis"
    language: list[str] = ["ar", "en"]
    wake_word: str = "hey_jarvis"

class ModelsConfig(BaseModel):
    default: str = "qwen3:8b"
    fast: str = "gemma3:4b"
    code: str = "qwen2.5-coder:7b"
    vision: str = "llava:7b"

class HardwareConfig(BaseModel):
    gpu_vram_limit_gb: float = 5.5
    max_concurrent_models: int = 1
    model_idle_timeout_s: int = 300

class InterfacesConfig(BaseModel):
    web_host: str = "127.0.0.1"
    web_port: int = 8080
    telegram_polling_timeout: int = 30

class PathsConfig(BaseModel):
    data: str = "data"
    logs: str = "logs"
    chroma: str = "data/chroma"
    sqlite: str = "data/jarvis.db"
    sessions: str = "data/sessions"
    downloads: str = "data/downloads"
    screenshots: str = "data/screenshots"
    generated: str = "data/generated"

class HotkeysConfig(BaseModel):
    open_cli: str = "ctrl+alt+j"
    start_voice: str = "ctrl+alt+s"

class RuntimeConfig(BaseModel):
    max_iterations: int = 5
    max_escalation_depth: int = 2
    turn_timeout_s: int = 120
    tool_timeout_s: int = 30

class AppSettings(BaseModel):
    jarvis: JarvisConfig = JarvisConfig()
    models: ModelsConfig = ModelsConfig()
    hardware: HardwareConfig = HardwareConfig()
    interfaces: InterfacesConfig = InterfacesConfig()
    paths: PathsConfig = PathsConfig()
    hotkeys: HotkeysConfig = HotkeysConfig()
    runtime: RuntimeConfig = RuntimeConfig()

@lru_cache(maxsize=1)
def get_settings() -> AppSettings:
    config_path = Path("config/settings.yaml")
    if config_path.exists():
        with open(config_path, encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return AppSettings(**data)
    return AppSettings()

def create_directories():
    """Create all required data directories."""
    cfg = get_settings()
    for path_str in [cfg.paths.data, cfg.paths.logs, cfg.paths.chroma,
                     cfg.paths.sessions, cfg.paths.downloads,
                     cfg.paths.screenshots, cfg.paths.generated]:
        Path(path_str).mkdir(parents=True, exist_ok=True)
```

**SUCCESS CRITERIA:**
- `from src.core.config import get_settings; s = get_settings()`
- `s.jarvis.name == "Jarvis"` → True
- `s.models.default == "qwen3:8b"` → True
- `s.runtime.max_iterations == 5` → True

---

### TASK 1.2 — Logging setup

**DESCRIPTION:** Structured logging to file + terminal with rotation.

**INPUT:** Call `setup_logging()` at app startup
**OUTPUT:** Logs in terminal AND `logs/jarvis.log`

**FILES:**
- CREATE: `src/core/logging_setup.py`

**IMPLEMENTATION:**
```python
from loguru import logger
from pathlib import Path
import sys

def setup_logging(level: str = "INFO", debug: bool = False):
    Path("logs").mkdir(exist_ok=True)
    
    # Remove default stderr handler
    logger.remove()
    
    # Terminal: colored, concise
    logger.add(
        sys.stderr,
        level=level,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>",
        colorize=True,
    )
    
    # File: structured, rotating
    logger.add(
        "logs/jarvis.log",
        level=level,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
        rotation="10 MB",
        retention="7 days",
        encoding="utf-8",
    )
    
    if debug:
        logger.add(
            "logs/debug.log",
            level="DEBUG",
            format="{time} | {level} | {function}:{line} | {message}",
            rotation="100 MB",
            retention="1 day",
            encoding="utf-8",
        )
    
    logger.info("Logging initialized level={}", level)
```

**SUCCESS CRITERIA:**
- `setup_logging()` creates `logs/jarvis.log`
- `logger.info("test")` writes to both terminal and file
- File has timestamps, level, message

---

### TASK 1.3 — Package skeleton

**DESCRIPTION:** Create all package directories with `__init__.py`.

**INPUT:** Nothing
**OUTPUT:** All directories exist; `import src.core.decision` works

**FILES:** Create all following files (empty `__init__.py`):
```
src/__init__.py
src/core/__init__.py
src/core/context/__init__.py
src/core/decision/__init__.py
src/core/runtime/__init__.py
src/core/agents/__init__.py
src/core/memory/__init__.py
src/core/tools/__init__.py
src/core/identity/__init__.py
src/models/__init__.py
src/models/llm/__init__.py
src/models/vision/__init__.py
src/models/speech/__init__.py
src/models/diffusion/__init__.py
src/skills/__init__.py
src/skills/system/__init__.py
src/skills/files/__init__.py
src/skills/browser/__init__.py
src/skills/search/__init__.py
src/skills/social/__init__.py
src/skills/api/__init__.py
src/skills/pdf/__init__.py
src/skills/office/__init__.py
src/skills/screen/__init__.py
src/skills/notify/__init__.py
src/skills/coder/__init__.py
src/skills/media/__init__.py
src/skills/network/__init__.py
src/interfaces/__init__.py
src/interfaces/cli/__init__.py
src/interfaces/web/__init__.py
src/interfaces/voice/__init__.py
src/interfaces/telegram/__init__.py
src/interfaces/gui/__init__.py
```

**SUCCESS CRITERIA:**
- `python -c "import src.core.decision"` → no ModuleNotFoundError
- `python -c "import src.skills.system"` → no ModuleNotFoundError

---

### TASK 1.4 — Model capability profiles

**DESCRIPTION:** Load model metadata from YAML; used by Decision for routing.

**INPUT:** `config/models.yaml`
**OUTPUT:** `get_model_profile("qwen3:8b")` returns capability dict

**FILES:**
- CREATE: `config/models.yaml`
- CREATE: `src/models/profiles.py`

**`config/models.yaml`:**
```yaml
qwen3:8b:
  temperature: 0.6
  top_p: 0.9
  max_tokens: 8192
  vram_gb: 5.0
  arabic_quality: 0.95
  reasoning: "high"
  code_bias: 0.50
  vision: false
  latency: "medium"

gemma3:4b:
  temperature: 0.7
  top_p: 0.9
  max_tokens: 2048
  vram_gb: 3.0
  arabic_quality: 0.85
  reasoning: "low"
  code_bias: 0.35
  vision: false
  latency: "fast"

qwen2.5-coder:7b:
  temperature: 0.3
  top_p: 0.95
  max_tokens: 8192
  vram_gb: 4.7
  arabic_quality: 0.75
  reasoning: "medium"
  code_bias: 0.95
  vision: false
  latency: "fast"

llava:7b:
  temperature: 0.4
  top_p: 0.9
  max_tokens: 2048
  vram_gb: 4.5
  arabic_quality: 0.70
  reasoning: "medium"
  code_bias: 0.20
  vision: true
  latency: "medium"
```

**`src/models/profiles.py`:**
```python
from pathlib import Path
from functools import lru_cache
import yaml

@lru_cache(maxsize=1)
def _load_all() -> dict:
    path = Path("config/models.yaml")
    with open(path) as f:
        return yaml.safe_load(f)

def get_model_profile(model: str) -> dict:
    return _load_all().get(model, {})

def all_models() -> list[str]:
    return list(_load_all().keys())
```

**SUCCESS CRITERIA:**
- `get_model_profile("qwen3:8b")["vram_gb"] == 5.0` → True
- `get_model_profile("llava:7b")["vision"] == True` → True

---

### TASK 1.5 — LLM engine with VRAM guard

**DESCRIPTION:** Expand engine.py with model tracking and VRAM-safe swaps.

**INPUT:** Call `swap_to("qwen3:8b")` then `swap_to("gemma3:4b")`
**OUTPUT:** Models swap without OOM

**FILES:**
- MODIFY: `src/models/llm/engine.py`

**IMPLEMENTATION (additions to engine.py):**
```python
import requests
from loguru import logger

_active_model: str | None = None

def get_active_model() -> str | None:
    return _active_model

def unload_current_model():
    global _active_model
    if _active_model:
        try:
            # Ollama: set keep_alive=0 to unload
            requests.post("http://localhost:11434/api/generate",
                          json={"model": _active_model, "keep_alive": 0},
                          timeout=10)
            logger.info("model.unloaded model={}", _active_model)
            _active_model = None
        except Exception as e:
            logger.warning("model.unload_failed model={} error={}", _active_model, e)

def swap_to(new_model: str):
    global _active_model
    if _active_model == new_model:
        return  # already loaded
    if _active_model:
        unload_current_model()
    logger.info("model.loading model={}", new_model)
    _active_model = new_model
    # First chat call will actually load the model
```

**SUCCESS CRITERIA:**
- `swap_to("gemma3:4b")` then `swap_to("qwen3:8b")` → no OOM error
- `get_active_model()` returns correct model after swap

---

### TASK 1.6 — Identity: system prompt builder

**DESCRIPTION:** Build the system prompt injected into every LLM call.

**INPUT:** `task_context: str`, `mode: str`, `tools: list`
**OUTPUT:** Complete system prompt string

**FILES:**
- CREATE: `config/jarvis_identity.yaml`
- CREATE: `src/core/identity/builder.py`

**`config/jarvis_identity.yaml`:**
```yaml
name: "Jarvis"
role: "personal AI assistant system"
component_notice: "You are a component of Jarvis. You are not the underlying model (qwen, gemma, llava). You are Jarvis. Behave consistently regardless of which model is active."
safety_rules:
  - "Never expose credentials, API keys, passwords, or raw file paths in responses"
  - "Always confirm before: deleting files, sending emails, sending messages, killing processes, running code"
  - "Admit uncertainty rather than fabricate information"
  - "All data stays local — never suggest sending data to external services unless the user explicitly requests it"
language_behavior:
  arabic:
    greeting: "أهلاً وسهلاً"
    affirmation: "بالتأكيد"
    style: "Use natural Arabic expressions, warm and direct tone"
  english:
    greeting: "Hello"
    affirmation: "Sure"
    style: "Direct, concise, and professional tone"
```

**`src/core/identity/builder.py`:**
```python
from pathlib import Path
from functools import lru_cache
import yaml
from src.core.memory.user_profile import load_profile

MODE_FRAGMENTS = {
    "fast":     "Answer concisely. One to three sentences maximum. No preamble.",
    "normal":   "Provide a complete, well-structured answer.",
    "deep":     "Think step by step. Show your reasoning. Self-critique before finalizing.",
    "planning": "Decompose the goal into numbered steps before executing any of them.",
    "research": "Use multiple sources. Cite each factual claim. Summarize at the end.",
}

@lru_cache(maxsize=1)
def _load_identity() -> dict:
    path = Path("config/jarvis_identity.yaml")
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)

def build_system_prompt(task_context: str = "", mode: str = "normal",
                         tools: list = [], previous_model: str | None = None,
                         current_model: str | None = None) -> str:
    identity = _load_identity()
    profile = load_profile()
    
    lang = profile.get("language", "ar")
    lang_behavior = identity["language_behavior"].get(lang, {})
    
    parts = [
        f"You are {identity['name']}, {identity['role']}.",
        identity["component_notice"],
        "",
        "Safety rules:",
        *[f"- {rule}" for rule in identity["safety_rules"]],
        "",
        f"User profile: name={profile.get('name','User')} | language={lang} | style={profile.get('style','balanced')} | level={profile.get('technical_level','intermediate')}",
        f"Language style: {lang_behavior.get('style', '')}",
        "",
        f"Mode: {mode} — {MODE_FRAGMENTS.get(mode, '')}",
    ]
    
    if task_context:
        parts.append(f"\nTask context: {task_context}")
    
    if tools:
        tool_descriptions = "\n".join(f"- {t['function']['name']}: {t['function']['description']}" for t in tools)
        parts.append(f"\nAvailable tools:\n{tool_descriptions}")
        parts.append("\nWhen you need to use a tool, output ONLY this JSON (no other text):\n{\"type\":\"tool_call\",\"tool\":\"tool_name\",\"args\":{...}}")
    
    if previous_model and current_model and previous_model != current_model:
        parts.append(f"\n[Context: switched from {previous_model} to {current_model} — maintain conversation continuity]")
    
    return "\n".join(parts)
```

**SUCCESS CRITERIA:**
- `build_system_prompt("open chrome", "fast")` returns non-empty string
- String contains "Jarvis", safety rules, and mode instructions
- Changing mode changes the mode section of the output

---

### TASK 1.7 — `.env` + environment variables

**DESCRIPTION:** Document and load all required environment variables.

**INPUT:** `.env` file
**OUTPUT:** Variables accessible via `os.environ`

**FILES:**
- CREATE: `.env.example`
- CREATE: `.env` (from example)

**`.env.example`:**
```bash
# Telegram Bot
TELEGRAM_BOT_TOKEN=

# Google APIs (get from Google Cloud Console)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

# YouTube Data API v3
YOUTUBE_API_KEY=

# Session encryption key (generate with: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
SESSION_ENCRYPTION_KEY=

# Debug mode (1 = enable debug logging and debug.log)
JARVIS_DEBUG=0

# Ollama host (default: http://localhost:11434)
OLLAMA_HOST=http://localhost:11434
```

**SUCCESS CRITERIA:**
- `cp .env.example .env` works
- `from dotenv import load_dotenv; load_dotenv(); import os; os.environ.get("JARVIS_DEBUG")` returns "0"

---

### TASK 1.8 — main.py entry point

**DESCRIPTION:** The single entry point for starting Jarvis with any interface.

**INPUT:** `--interface cli` (or web, voice, telegram, gui, all)
**OUTPUT:** "Jarvis ready." + interface starts

**FILES:**
- CREATE: `app/main.py`

**IMPLEMENTATION:**
```python
#!/usr/bin/env python3
# app/main.py
import argparse
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

from src.core.config import get_settings, create_directories
from src.core.logging_setup import setup_logging
from loguru import logger
import os

def main():
    parser = argparse.ArgumentParser(prog="jarvis", description="Jarvis AI Assistant")
    parser.add_argument("--interface", choices=["cli","web","voice","telegram","gui","all"],
                        default="cli", help="Which interface to start")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()
    
    # Setup
    debug = args.debug or os.environ.get("JARVIS_DEBUG", "0") == "1"
    setup_logging(level="DEBUG" if debug else "INFO", debug=debug)
    cfg = get_settings()
    create_directories()
    
    logger.info("Jarvis starting interface={} version=1.0.0", args.interface)
    
    # Launch interface
    if args.interface == "cli":
        from src.interfaces.cli.interface import run_cli
        run_cli(cfg)
    elif args.interface == "web":
        from src.interfaces.web.app import run_web
        run_web(cfg)
    elif args.interface == "voice":
        from src.interfaces.voice.pipeline import run_voice_pipeline
        run_voice_pipeline(cfg)
    elif args.interface == "telegram":
        from src.interfaces.telegram.bot import run_bot
        run_bot(cfg)
    elif args.interface == "gui":
        from src.interfaces.gui.main_window import run_gui
        run_gui(cfg)
    elif args.interface == "all":
        import threading
        threads = [
            threading.Thread(target=lambda: __import__('src.interfaces.cli.interface', fromlist=['run_cli']).run_cli(cfg), daemon=True),
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Jarvis stopped by user")
```

**SUCCESS CRITERIA:**
- `python app/main.py --interface cli` prints "Jarvis ready." (once CLI is implemented in Phase 12)
- `python app/main.py --help` shows usage
- Ctrl+C exits cleanly

---

## 🔄 Phase 2 — Runtime Loop

> **End state:** Full turn: text input → Context assembled → Decision made → LLM called → response streamed. No tools yet.

---

### TASK 2.1 — ContextBundle + assembler

**DESCRIPTION:** Create the data structure for one turn's input.

**INPUT:** `user_message: str`, `session_id: str`
**OUTPUT:** `ContextBundle` with message + empty slots for memory (filled Phase 8)

**FILES:**
- CREATE: `src/core/context/bundle.py`
- CREATE: `src/core/context/assembler.py`

**`src/core/context/bundle.py`:**
```python
from pydantic import BaseModel, Field
from typing import Any
import time

class Attachment(BaseModel):
    type: str        # "image" | "file" | "audio"
    path: str
    mime_type: str = ""
    size_bytes: int = 0

class Message(BaseModel):
    role: str        # "user" | "assistant"
    content: str
    timestamp: float = Field(default_factory=time.time)

class UserProfile(BaseModel):
    name: str = "User"
    language: str = "ar"
    style: str = "balanced"
    tone: str = "casual"
    technical_level: str = "intermediate"
    timezone: str = "UTC"

class ToolResult(BaseModel):
    tool: str
    success: bool
    data: dict = {}
    error: str = ""
    duration_ms: float = 0

class ContextBundle(BaseModel):
    user_message: str
    session_id: str
    attachments: list[Attachment] = []
    tool_results: list[ToolResult] = []
    memory_snippets: list[str] = []
    recent_history: list[Message] = []
    user_profile: UserProfile = UserProfile()
    turn_number: int = 1
    started_at: float = Field(default_factory=time.time)
```

**`src/core/context/assembler.py`:**
```python
from src.core.context.bundle import ContextBundle, UserProfile
from src.core.memory.user_profile import load_profile

_turn_counters: dict[str, int] = {}

def assemble_context(user_message: str, session_id: str,
                     attachments: list = []) -> ContextBundle:
    _turn_counters[session_id] = _turn_counters.get(session_id, 0) + 1
    
    profile_data = load_profile()
    user_profile = UserProfile(**profile_data)
    
    # Memory injection added in Phase 8
    # For now: empty snippets and history
    
    return ContextBundle(
        user_message=user_message,
        session_id=session_id,
        attachments=attachments,
        user_profile=user_profile,
        turn_number=_turn_counters[session_id],
    )
```

**SUCCESS CRITERIA:**
- `assemble_context("hello", "s1")` returns `ContextBundle`
- `bundle.user_message == "hello"` → True
- `bundle.turn_number` increments on repeated calls with same session_id

---

### TASK 2.2 — DecisionOutput + Decision module

**DESCRIPTION:** Formal Decision layer that outputs a typed routing decision.

**INPUT:** `ContextBundle`
**OUTPUT:** `DecisionOutput` with model, mode, intent

**FILES:**
- CREATE: `src/core/decision/decision.py`
- MODIFY: `src/core/decision/classifier.py` (use DecisionOutput)

**`src/core/decision/decision.py`:**
```python
from pydantic import BaseModel
from src.core.context.bundle import ContextBundle

class DecisionOutput(BaseModel):
    intent: str            # chat|code|tool_use|search|vision|research|voice
    complexity: str        # low|medium|high
    mode: str              # fast|normal|deep|planning|research
    model: str             # exact ollama tag
    requires_tools: bool
    requires_planning: bool
    tool_name: str | None = None
    tool_args: dict = {}
    confidence: float = 0.8

# Fast-path rules (no LLM call needed)
def _fast_path(context: ContextBundle) -> DecisionOutput | None:
    msg = context.user_message
    
    # Image attached → vision
    if any(a.type == "image" for a in context.attachments):
        return DecisionOutput(intent="vision", complexity="medium", mode="normal",
                               model="llava:7b", requires_tools=False, requires_planning=False)
    
    # Very short message → fast chat
    if len(msg) < 20 and not any(kw in msg.lower() for kw in ["open","close","send","search","find","create","delete","run"]):
        return DecisionOutput(intent="chat", complexity="low", mode="fast",
                               model="gemma3:4b", requires_tools=False, requires_planning=False)
    
    return None  # no fast path; use classifier

def decide(context: ContextBundle) -> DecisionOutput:
    from src.core.decision.classifier import classify
    import json
    
    fast = _fast_path(context)
    if fast:
        return fast
    
    try:
        raw = classify(context.user_message)
        return DecisionOutput(**raw)
    except Exception:
        # Fallback: safe default
        return DecisionOutput(intent="chat", complexity="medium", mode="normal",
                               model="qwen3:8b", requires_tools=False, requires_planning=False,
                               confidence=0.5)
```

**SUCCESS CRITERIA:**
- `decide(assemble_context("hello", "s1"))` → `intent="chat"`, `model="gemma3:4b"`
- `decide(assemble_context("write Python code to sort a list", "s1"))` → `model="qwen2.5-coder:7b"`
- `decide(assemble_context("افتح Chrome", "s1"))` → `intent="tool_use"`, `tool_name="open_app"`
- Short message uses fast path (no LLM call): verify by checking no Ollama call was made

---

### TASK 2.3 — Executor (runtime core)

**DESCRIPTION:** Run one complete turn: assemble → decide → think → evaluate.

**INPUT:** `user_input: str`, `session_id: str`
**OUTPUT:** Generator yielding response tokens

**FILES:**
- CREATE: `src/core/runtime/executor.py`

**IMPLEMENTATION:**
```python
from src.core.context.assembler import assemble_context
from src.core.decision.decision import decide, DecisionOutput
from src.core.identity.builder import build_system_prompt
from src.models.llm.engine import stream_chat, swap_to, get_active_model
from src.core.context.bundle import ContextBundle
from loguru import logger
import time

def execute_turn(user_input: str, session_id: str, attachments: list = []):
    """Generator: yields response tokens."""
    started = time.time()
    
    context = assemble_context(user_input, session_id, attachments)
    decision = decide(context)
    
    logger.info("decision intent={} model={} mode={} tools={} planning={}",
                decision.intent, decision.model, decision.mode,
                decision.requires_tools, decision.requires_planning)
    
    prev_model = get_active_model()
    swap_to(decision.model)
    
    system = build_system_prompt(
        task_context=user_input,
        mode=decision.mode,
        previous_model=prev_model,
        current_model=decision.model,
    )
    
    if decision.requires_tools:
        # Tool execution added in Phase 4
        yield "[tool execution not yet implemented — use Phase 4]"
        return
    
    messages = [
        {"role": "system", "content": system},
        # History injection added in Phase 8
        {"role": "user", "content": user_input},
    ]
    
    for token in stream_chat(user_input, model=decision.model, system=system):
        yield token
    
    logger.info("turn.done session={} ms={:.0f}", session_id, (time.time()-started)*1000)
```

**SUCCESS CRITERIA:**
- `list(execute_turn("what is AI?", "s1"))` returns list of tokens that form a coherent answer
- Arabic input returns Arabic answer
- Logging shows `decision intent=...` line in output

---

### TASK 2.4 — Evaluator

**DESCRIPTION:** Score the response and decide if retry is needed.

**INPUT:** `response: str`, `decision: DecisionOutput`
**OUTPUT:** `EvalResult(quality: float, should_retry: bool, reason: str)`

**FILES:**
- CREATE: `src/core/runtime/evaluator.py`

**IMPLEMENTATION:**
```python
from pydantic import BaseModel
from src.core.decision.decision import DecisionOutput

class EvalResult(BaseModel):
    quality: float
    should_retry: bool
    reason: str

def evaluate(response: str, decision: DecisionOutput) -> EvalResult:
    # Empty response
    if not response or not response.strip():
        return EvalResult(quality=0.0, should_retry=True, reason="empty response")
    
    # Too short for complex task
    if decision.complexity == "high" and len(response.strip()) < 80:
        return EvalResult(quality=0.3, should_retry=True, reason="too short for complex task")
    
    # Tool call required but LLM gave plain text (or vice versa)
    if decision.requires_tools and '{"type":"tool_call"' not in response and len(response) < 50:
        return EvalResult(quality=0.4, should_retry=True, reason="expected tool call but got short text")
    
    # Error indicators in response
    error_phrases = ["i cannot", "i don't know how", "unable to", "I'm not able"]
    if any(p.lower() in response.lower() for p in error_phrases) and decision.complexity == "low":
        return EvalResult(quality=0.5, should_retry=True, reason="model expressed inability on simple task")
    
    return EvalResult(quality=0.85, should_retry=False, reason="acceptable")
```

**SUCCESS CRITERIA:**
- `evaluate("", decision)` → `should_retry=True`
- `evaluate("Paris is the capital of France.", decision_with_low_complexity)` → `should_retry=False`
- `evaluate("I cannot help with that.", decision_with_low_complexity)` → `should_retry=True`

---

### TASK 2.5 — Runtime loop (full turn with retry)

**DESCRIPTION:** Full turn execution with escalation logic.

**INPUT:** `user_input: str`, `session_id: str`
**OUTPUT:** Final response string

**FILES:**
- CREATE: `src/core/runtime/loop.py`

**IMPLEMENTATION:**
```python
from src.core.context.assembler import assemble_context
from src.core.decision.decision import decide, DecisionOutput
from src.core.runtime.executor import execute_turn
from src.core.runtime.evaluator import evaluate
from src.core.config import get_settings
from loguru import logger

ESCALATION = [
    ("fast",    "gemma3:4b"),
    ("normal",  "qwen3:8b"),
    ("deep",    "qwen3:8b"),
]

def run_turn(user_input: str, session_id: str, attachments: list = []) -> str:
    cfg = get_settings()
    max_iter = cfg.runtime.max_iterations
    
    context = assemble_context(user_input, session_id, attachments)
    decision = decide(context)
    
    escalation_level = 0
    
    for iteration in range(max_iter):
        logger.info("turn.iter iter={} model={} mode={}", iteration+1, decision.model, decision.mode)
        
        tokens = []
        for token in execute_turn(user_input, session_id, attachments):
            tokens.append(token)
        response = "".join(tokens)
        
        eval_result = evaluate(response, decision)
        
        if not eval_result.should_retry:
            logger.info("turn.eval quality={:.2f} retry=False", eval_result.quality)
            return response
        
        # Escalate
        escalation_level += 1
        if escalation_level >= len(ESCALATION):
            logger.warning("turn.maxescalation — returning best available")
            return response
        
        new_mode, new_model = ESCALATION[escalation_level]
        logger.info("turn.escalate mode={} model={} reason={}", new_mode, new_model, eval_result.reason)
        decision.mode = new_mode
        decision.model = new_model
    
    return response  # return whatever we have after max iterations

def run_turn_streaming(user_input: str, session_id: str, attachments: list = []):
    """Version that yields tokens for streaming interfaces."""
    cfg = get_settings()
    context = assemble_context(user_input, session_id, attachments)
    decision = decide(context)
    
    tokens = []
    for token in execute_turn(user_input, session_id, attachments):
        tokens.append(token)
        yield token
    
    response = "".join(tokens)
    eval_result = evaluate(response, decision)
    
    if eval_result.should_retry and decision.mode != "deep":
        yield "\n\n[Retrying with deeper analysis...]\n\n"
        decision.mode = "deep"
        decision.model = "qwen3:8b"
        for token in execute_turn(user_input, session_id, attachments):
            yield token
```

**SUCCESS CRITERIA:**
- `run_turn("what is AI?", "s1")` returns non-empty string
- Empty response from model triggers retry (test by mocking LLM to return empty)
- After max escalations, returns best available response

---

### TASK 2.6 — EventBus

**DESCRIPTION:** Lightweight pub/sub for system-wide event notifications.

**INPUT:** `bus.emit("turn.end", {"response": "..."})`
**OUTPUT:** All subscribers for "turn.end" receive the data

**FILES:**
- CREATE: `src/core/events.py`

**IMPLEMENTATION:**
```python
from collections import defaultdict
from typing import Callable, Any
from loguru import logger

class EventBus:
    def __init__(self):
        self._handlers: dict[str, list[Callable]] = defaultdict(list)
    
    def subscribe(self, event: str, handler: Callable):
        self._handlers[event].append(handler)
        logger.debug("event.subscribe event={} handler={}", event, handler.__name__)
    
    def unsubscribe(self, event: str, handler: Callable):
        self._handlers[event] = [h for h in self._handlers[event] if h != handler]
    
    def emit(self, event: str, data: dict = {}):
        for handler in self._handlers[event]:
            try:
                handler(data)
            except Exception as e:
                logger.error("event.handler_error event={} handler={} error={}", event, handler.__name__, e)

# Global singleton
bus = EventBus()

# Standard events:
# turn.start   {session_id, user_input}
# turn.end     {session_id, response, quality}
# decision     {intent, model, mode, tool_name}
# tool.start   {tool_name, args_hash}
# tool.end     {tool_name, success, duration_ms}
# eval.retry   {reason, escalation_level}
# model.swap   {from_model, to_model}
# error        {type, message, session_id}
```

**SUCCESS CRITERIA:**
- Subscribe handler to "turn.end"
- Call `run_turn()` (which emits "turn.end" internally)
- Verify handler was called with response data

---

### TASK 2.7 — Structured turn logging

**DESCRIPTION:** Log all turn events in a structured, queryable format.

**INPUT:** Turn execution
**OUTPUT:** Structured log lines in `logs/jarvis.log`

**FILES:**
- MODIFY: `src/core/runtime/loop.py` (add log calls)
- MODIFY: `src/core/runtime/executor.py` (add log calls)

Add these log calls in `run_turn()`:
```python
logger.info("turn.start session={} input_len={} turn={}", session_id, len(user_input), context.turn_number)
# ... after decision:
logger.info("decision intent={} model={} mode={} tools={}", decision.intent, decision.model, decision.mode, decision.requires_tools)
# ... after eval:
logger.info("turn.end session={} quality={:.2f} retry={} ms={:.0f}", session_id, eval_result.quality, eval_result.should_retry, elapsed_ms)
```

**SUCCESS CRITERIA:**
- After 3 turns, `logs/jarvis.log` contains 9+ structured lines
- Each line has session_id, timestamp, and relevant fields
- Grepping `"decision"` shows all routing decisions

---

### TASK 2.8 — User profile module

**DESCRIPTION:** Persistent user preferences stored in JSON.

**INPUT:** `{"language": "ar", "style": "concise"}`
**OUTPUT:** Saved to `data/user_profile.json`; loadable on restart

**FILES:**
- CREATE: `src/core/memory/user_profile.py`

**IMPLEMENTATION:**
```python
from pathlib import Path
import json

PROFILE_PATH = Path("data/user_profile.json")

DEFAULT_PROFILE = {
    "name": "User",
    "language": "ar",
    "style": "balanced",      # concise | balanced | detailed
    "tone": "casual",          # formal | casual | warm
    "technical_level": "intermediate",
    "timezone": "UTC",
    "preferred_model": None,
    "preferred_mode": None,
}

def load_profile() -> dict:
    if PROFILE_PATH.exists():
        return {**DEFAULT_PROFILE, **json.loads(PROFILE_PATH.read_text(encoding="utf-8"))}
    return DEFAULT_PROFILE.copy()

def save_profile(updates: dict):
    current = load_profile()
    current.update(updates)
    PROFILE_PATH.parent.mkdir(exist_ok=True)
    PROFILE_PATH.write_text(json.dumps(current, ensure_ascii=False, indent=2), encoding="utf-8")

def get_profile_value(key: str, default=None):
    return load_profile().get(key, default)
```

**SUCCESS CRITERIA:**
- `save_profile({"language": "en"})` → file written
- Restart Python → `load_profile()["language"] == "en"` → True
- `load_profile()` returns DEFAULT_PROFILE if no file exists

---

## 🎯 Phase 3 — Decision System

> **End state:** All intent types correctly classified with correct model selected.

---

### TASK 3.1 — Robust JSON classifier

**DESCRIPTION:** Handle malformed JSON from classifier; add retry logic.

**INPUT:** Any user message including edge cases
**OUTPUT:** Always returns valid `DecisionOutput`

**FILES:**
- MODIFY: `src/core/decision/classifier.py`

**IMPLEMENTATION:**
```python
import json, re
from src.models.llm.engine import chat
from loguru import logger

SYSTEM = """..."""  # (full system prompt from Task 0.2)

def _extract_json(text: str) -> str:
    """Extract JSON from response that may contain markdown or other text."""
    text = text.strip()
    # Remove markdown code blocks
    text = re.sub(r'```(?:json)?', '', text).strip('`').strip()
    # Find first { to last }
    start = text.find('{')
    end = text.rfind('}')
    if start != -1 and end != -1:
        return text[start:end+1]
    return text

def classify(message: str, max_retries: int = 2) -> dict:
    for attempt in range(max_retries + 1):
        try:
            raw = chat(message, model="gemma3:4b", system=SYSTEM)
            clean = _extract_json(raw)
            result = json.loads(clean)
            # Validate required fields
            required = ["intent", "complexity", "mode", "model", "requires_tools", "requires_planning"]
            for field in required:
                if field not in result:
                    raise ValueError(f"Missing field: {field}")
            logger.debug("classifier.success attempt={} intent={}", attempt+1, result["intent"])
            return result
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            logger.warning("classifier.parse_error attempt={} error={}", attempt+1, e)
            if attempt == max_retries:
                # Safe fallback
                return {"intent": "chat", "complexity": "medium", "mode": "normal",
                        "model": "qwen3:8b", "requires_tools": False, "requires_planning": False,
                        "tool_name": None, "tool_args": {}}
```

**SUCCESS CRITERIA:**
- `classify("open chrome")` → correct JSON with `intent="tool_use"`
- `classify("")` → returns fallback dict without crashing
- If gemma3:4b returns malformed JSON, retry fires and succeeds or returns fallback

---

### TASK 3.2 — Decision routing tests

**DESCRIPTION:** Verify all intent types route to the correct model.

**INPUT:** Various test messages
**OUTPUT:** All route to expected model/mode

**FILES:**
- CREATE: `tests/test_decision.py`

**TEST CASES:**
```python
def test_routing():
    cases = [
        ("hello", "chat", "gemma3:4b", "fast"),
        ("write Python code to sort a list", "code", "qwen2.5-coder:7b", "normal"),
        ("research the history of AI and write a report", "research", "qwen3:8b", "research"),
        ("افتح Chrome", "tool_use", "gemma3:4b", "fast"),
        ("ما هو الذكاء الاصطناعي؟", "chat", "gemma3:4b", "fast"),
    ]
    for message, expected_intent, expected_model, expected_mode in cases:
        result = decide(assemble_context(message, "test_session"))
        assert result.intent == expected_intent, f"'{message}': expected {expected_intent}, got {result.intent}"
        assert result.model == expected_model, f"'{message}': expected {expected_model}, got {result.model}"
```

**SUCCESS CRITERIA:**
- `pytest tests/test_decision.py -v` → all cases pass

---

### TASK 3.3 — VRAM guard integration

**DESCRIPTION:** Ensure model swaps don't cause OOM on 6GB GPU.

**INPUT:** Sequence of requests requiring different models
**OUTPUT:** Models swap cleanly; no OOM error

**FILES:**
- CREATE: `src/models/llm/vram_guard.py`

**IMPLEMENTATION:**
```python
from src.models.profiles import get_model_profile
from src.core.config import get_settings
from loguru import logger

def can_load_model(model: str) -> bool:
    """Check if model fits in available VRAM."""
    cfg = get_settings()
    profile = get_model_profile(model)
    needed = profile.get("vram_gb", 5.0)
    limit = cfg.hardware.gpu_vram_limit_gb
    can_load = needed <= limit
    if not can_load:
        logger.warning("vram.insufficient model={} needed={}GB limit={}GB", model, needed, limit)
    return can_load

def get_smallest_available_model() -> str:
    """Return the model with lowest VRAM requirement that's available."""
    models = ["gemma3:4b", "qwen2.5-coder:7b", "llava:7b", "qwen3:8b"]
    return min(models, key=lambda m: get_model_profile(m).get("vram_gb", 99))
```

**SUCCESS CRITERIA:**
- `can_load_model("qwen3:8b")` → True on 6GB GPU
- Sequential calls to different models work without memory errors

---

### TASK 3.4 — Mode escalation chain

**DESCRIPTION:** Define and implement the escalation path when evaluation fails.

**INPUT:** Current mode + model
**OUTPUT:** Next mode + model to try

**FILES:**
- CREATE: `src/core/runtime/escalation.py`

**IMPLEMENTATION:**
```python
from dataclasses import dataclass

@dataclass
class EscalationLevel:
    mode: str
    model: str
    description: str

ESCALATION_CHAIN = [
    EscalationLevel("fast",    "gemma3:4b",         "Quick answer attempt"),
    EscalationLevel("normal",  "qwen3:8b",           "Standard response"),
    EscalationLevel("deep",    "qwen3:8b",           "Deep chain-of-thought"),
]

def get_next_escalation(current_mode: str, current_model: str) -> EscalationLevel | None:
    for i, level in enumerate(ESCALATION_CHAIN):
        if level.mode == current_mode and level.model == current_model:
            if i + 1 < len(ESCALATION_CHAIN):
                return ESCALATION_CHAIN[i + 1]
            return None  # already at max
    # If not found in chain, start from beginning
    return ESCALATION_CHAIN[0]
```

**SUCCESS CRITERIA:**
- `get_next_escalation("fast", "gemma3:4b")` → `EscalationLevel(mode="normal", model="qwen3:8b")`
- `get_next_escalation("deep", "qwen3:8b")` → `None` (already at max)

---

### TASK 3.5 — Decision integration tests

**DESCRIPTION:** End-to-end: message → decision → model called → response returned.

**INPUT:** Various messages
**OUTPUT:** Correct model used; response coherent

**FILES:**
- CREATE: `tests/test_runtime_integration.py`

**TEST CASES:**
```python
def test_full_turn_arabic():
    response = run_turn("ما هو الذكاء الاصطناعي؟", "test_session_ar")
    assert len(response) > 10
    # Arabic characters present in response
    assert any('\u0600' <= c <= '\u06FF' for c in response)

def test_full_turn_code():
    response = run_turn("write a Python function to check if a number is prime", "test_session_code")
    assert "def " in response or "function" in response.lower()
```

**SUCCESS CRITERIA:**
- Both tests pass
- No exceptions raised

---

## 🛠️ Phase 4 — Tool System

> **End state:** LLM can call any registered skill. Tool calls parsed, validated, executed, and result fed back to LLM.

---

### TASK 4.1 — BaseTool + ToolResult

**DESCRIPTION:** Abstract base class for all tools.

**INPUT:** Python class extending BaseTool
**OUTPUT:** Tool discoverable and executable

**FILES:**
- CREATE: `src/core/tools/base.py`

**IMPLEMENTATION:**
```python
from abc import ABC, abstractmethod
from pydantic import BaseModel
from pathlib import Path
import yaml, platform

class ToolResult(BaseModel):
    tool: str = ""
    success: bool
    data: dict = {}
    error: str = ""
    duration_ms: float = 0

class BaseTool(ABC):
    name: str = ""
    description: str = ""
    category: str = ""
    requires_confirmation: bool = False
    platform: list[str] = ["windows", "linux", "darwin"]  # supported platforms
    
    @abstractmethod
    def execute(self, **kwargs) -> ToolResult: ...
    
    def is_available(self) -> bool:
        current = platform.system().lower()
        return current in self.platform
    
    @classmethod
    def get_schema(cls) -> dict:
        schema_path = Path(f"config/schemas/{cls.category}/{cls.name}.schema.json")
        if schema_path.exists():
            import json
            return json.loads(schema_path.read_text())
        return {}
    
    def to_ollama_format(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.get_schema().get("properties", {}),
            }
        }
```

**SUCCESS CRITERIA:**
- `class TestTool(BaseTool): name="test"; execute(**kwargs): return ToolResult(success=True)` works
- `isinstance(TestTool(), BaseTool)` → True

---

### TASK 4.2 — Tool registry with auto-discovery

**DESCRIPTION:** Automatically find and register all BaseTool subclasses.

**INPUT:** `src/skills/` directory
**OUTPUT:** All tools registered; accessible by name

**FILES:**
- CREATE: `src/core/tools/registry.py`

**IMPLEMENTATION:**
```python
import importlib, pkgutil, inspect, platform
from src.core.tools.base import BaseTool, ToolResult
from loguru import logger

class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, BaseTool] = {}
        self._discovered = False
    
    def discover(self):
        if self._discovered:
            return
        
        import src.skills as skills_pkg
        for finder, modname, ispkg in pkgutil.walk_packages(
            skills_pkg.__path__, prefix="src.skills.", onerror=lambda x: None
        ):
            try:
                module = importlib.import_module(modname)
                for attr_name in dir(module):
                    cls = getattr(module, attr_name)
                    if (isinstance(cls, type) and issubclass(cls, BaseTool) 
                        and cls is not BaseTool and cls.name):
                        tool = cls()
                        if tool.is_available():
                            self._tools[tool.name] = tool
                            logger.debug("tool.registered name={}", tool.name)
            except Exception as e:
                logger.warning("tool.discovery_error module={} error={}", modname, e)
        
        self._discovered = True
        logger.info("tool.registry_ready count={}", len(self._tools))
    
    def get(self, name: str) -> BaseTool | None:
        self.discover()
        return self._tools.get(name)
    
    def all_names(self) -> list[str]:
        self.discover()
        return list(self._tools.keys())
    
    def all_available(self) -> list[BaseTool]:
        self.discover()
        return list(self._tools.values())
    
    def to_ollama_format(self) -> list[dict]:
        return [t.to_ollama_format() for t in self.all_available()]
    
    def get_schema(self, name: str) -> dict:
        tool = self.get(name)
        return tool.get_schema() if tool else {}

# Singleton
registry = ToolRegistry()
```

**SUCCESS CRITERIA:**
- `registry.discover()` finds `AppLauncherTool` from Phase 0/5
- `registry.get("open_app")` returns tool instance
- `registry.all_names()` lists all discovered tools

---

### TASK 4.3 — Safety classifier

**DESCRIPTION:** Classify tool operations as safe/risky/critical before execution.

**INPUT:** `tool_name: str`, `args: dict`
**OUTPUT:** `SafetyResult` with level and allowed flag

**FILES:**
- CREATE: `src/core/tools/safety.py`

**IMPLEMENTATION:**
```python
from pydantic import BaseModel
from loguru import logger

SAFE = "safe"
RISKY = "risky"
CRITICAL = "critical"

RISKY_TOOLS = {
    "open_app", "run_shell", "send_email", "send_message",
    "execute_python", "send_whatsapp",
}
CRITICAL_TOOLS = {
    "delete_file", "kill_process", "format_disk",
    "registry_write", "clear_memory",
}
BLOCKED_SHELL_PATTERNS = [
    "rm -rf", "format c:", "del /s /q", ":(){:|:&};:",
    "shutdown", "reboot", "mkfs", "dd if=",
]

class SafetyResult(BaseModel):
    level: str          # safe|risky|critical
    allowed: bool | None  # True=go, False=block, None=ask_user
    reason: str

def classify_safety(tool_name: str, args: dict) -> SafetyResult:
    # Check critical tools first
    if tool_name in CRITICAL_TOOLS:
        logger.warning("safety.critical tool={}", tool_name)
        return SafetyResult(level=CRITICAL, allowed=False,
                            reason=f"Tool '{tool_name}' requires explicit user authorization — not allowed via LLM")
    
    # Check shell command blocklist
    args_str = " ".join(str(v) for v in args.values()).lower()
    for pattern in BLOCKED_SHELL_PATTERNS:
        if pattern in args_str:
            logger.warning("safety.blocked_pattern tool={} pattern={}", tool_name, pattern)
            return SafetyResult(level=CRITICAL, allowed=False, reason=f"Blocked pattern: {pattern}")
    
    # Risky: allow but require user confirmation
    if tool_name in RISKY_TOOLS:
        return SafetyResult(level=RISKY, allowed=None, reason="Requires user confirmation")
    
    return SafetyResult(level=SAFE, allowed=True, reason="")
```

**SUCCESS CRITERIA:**
- `classify_safety("delete_file", {})` → `level=CRITICAL, allowed=False`
- `classify_safety("send_email", {})` → `level=RISKY, allowed=None`
- `classify_safety("web_search", {})` → `level=SAFE, allowed=True`
- `classify_safety("run_shell", {"command": "rm -rf /"})` → `level=CRITICAL, allowed=False`

---

### TASK 4.4 — Tool executor + validator

**DESCRIPTION:** Validate args against schema, then execute tool.

**INPUT:** `tool_name: str`, `args: dict`
**OUTPUT:** `ToolResult`

**FILES:**
- CREATE: `src/core/tools/executor.py`

**IMPLEMENTATION:**
```python
import time, json
from src.core.tools.registry import registry
from src.core.tools.safety import classify_safety, RISKY, CRITICAL
from src.core.tools.base import ToolResult
from loguru import logger

def _ask_confirmation(tool_name: str, args: dict) -> bool:
    try:
        args_str = json.dumps(args, ensure_ascii=False)
        answer = input(f"\n⚠️  Jarvis wants to: {tool_name}({args_str})\nConfirm? [y/N]: ").strip().lower()
        return answer == "y"
    except (EOFError, KeyboardInterrupt):
        return False

def _validate_args(args: dict, schema: dict) -> str | None:
    """Returns error message or None if valid."""
    required = schema.get("required", [])
    for field in required:
        if field not in args:
            return f"Missing required field: {field}"
    props = schema.get("properties", {})
    for field, value in args.items():
        if field in props:
            expected_type = props[field].get("type")
            if expected_type == "string" and not isinstance(value, str):
                return f"Field '{field}' must be a string"
            if expected_type == "integer" and not isinstance(value, int):
                return f"Field '{field}' must be an integer"
    return None

def execute_tool(tool_name: str, args: dict) -> ToolResult:
    start = time.time()
    logger.info("tool.start name={} args_len={}", tool_name, len(args))
    
    # Find tool
    tool = registry.get(tool_name)
    if not tool:
        return ToolResult(tool=tool_name, success=False, error=f"Tool '{tool_name}' not found in registry")
    
    # Safety check
    safety = classify_safety(tool_name, args)
    if safety.allowed == False:
        return ToolResult(tool=tool_name, success=False, error=f"Blocked: {safety.reason}")
    if safety.allowed is None:  # RISKY — ask user
        if not _ask_confirmation(tool_name, args):
            return ToolResult(tool=tool_name, success=False, error="User declined execution")
    
    # Schema validation
    schema = registry.get_schema(tool_name)
    if schema:
        error = _validate_args(args, schema)
        if error:
            return ToolResult(tool=tool_name, success=False, error=f"Validation error: {error}")
    
    # Execute
    try:
        result = tool.execute(**args)
        result.tool = tool_name
        result.duration_ms = (time.time() - start) * 1000
        logger.info("tool.done name={} success={} ms={:.0f}", tool_name, result.success, result.duration_ms)
        return result
    except Exception as e:
        duration_ms = (time.time() - start) * 1000
        logger.error("tool.error name={} error={} ms={:.0f}", tool_name, e, duration_ms)
        return ToolResult(tool=tool_name, success=False, error=str(e), duration_ms=duration_ms)
```

**SUCCESS CRITERIA:**
- `execute_tool("open_app", {"name": "notepad"})` → opens Notepad, returns `success=True`
- `execute_tool("nonexistent_tool", {})` → returns `success=False, error="not found"`
- Dangerous shell pattern → blocked before execution

---

### TASK 4.5 — Wire tools into runtime loop

**DESCRIPTION:** When LLM outputs a tool call JSON, parse it, execute, and feed result back.

**INPUT:** LLM response containing tool call JSON
**OUTPUT:** Tool executes; result injected as next observation; LLM generates final answer

**FILES:**
- MODIFY: `src/core/runtime/executor.py`

**IMPLEMENTATION:**
```python
import json, re

TOOL_CALL_PATTERN = r'\{[^{}]*"type"\s*:\s*"tool_call"[^{}]*\}'

def _parse_tool_call(text: str) -> dict | None:
    """Extract tool call JSON from LLM response."""
    match = re.search(TOOL_CALL_PATTERN, text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    return None

# In execute_turn(), replace the "tool not implemented" placeholder:
def execute_turn(user_input: str, session_id: str, attachments: list = []):
    context = assemble_context(user_input, session_id, attachments)
    decision = decide(context)
    
    prev_model = get_active_model()
    swap_to(decision.model)
    
    system = build_system_prompt(
        task_context=user_input,
        mode=decision.mode,
        tools=registry.to_ollama_format() if decision.requires_tools else [],
        previous_model=prev_model,
        current_model=decision.model,
    )
    
    messages = [{"role": "system", "content": system},
                {"role": "user", "content": user_input}]
    
    # Add tool results from previous iterations
    for tr in context.tool_results:
        result_msg = f"Tool '{tr.tool}' result: {json.dumps(tr.data if tr.success else {'error': tr.error})}"
        messages.append({"role": "system", "content": result_msg})
    
    # Stream response
    tokens = []
    for token in stream_chat(user_input, model=decision.model, system=system):
        tokens.append(token)
    
    response = "".join(tokens)
    
    # Check for tool call
    tool_call = _parse_tool_call(response)
    if tool_call:
        from src.core.tools.executor import execute_tool
        from src.core.context.bundle import ToolResult as ContextToolResult
        
        result = execute_tool(tool_call["tool"], tool_call.get("args", {}))
        context.tool_results.append(ContextToolResult(**result.dict()))
        
        # Re-enter with tool result in context
        follow_up = f"Tool result: {json.dumps({'success': result.success, 'data': result.data, 'error': result.error})}\nNow provide the final answer to the user."
        for token in stream_chat(follow_up, model=decision.model, system=system):
            yield token
    else:
        for token in tokens:
            yield token
```

**SUCCESS CRITERIA:**
- "open notepad" → tool call parsed → Notepad opens → LLM says "Opened Notepad" → Notepad is visible
- Multi-turn: web search → LLM uses result to answer question

---

## 🖥️ Phase 5 — System Control Skills

> **End state:** All OS-level operations work on Windows/Linux/macOS.

---

### TASK 5.1 — Complete app launcher (with BaseTool)

**DESCRIPTION:** Refactor Phase 0 app launcher as a proper BaseTool subclass.

**INPUT:** `{"name": "chrome"}`
**OUTPUT:** App opens. ToolResult returned.

**FILES:**
- MODIFY: `src/skills/system/apps.py`

**IMPLEMENTATION:** Wrap existing functions in `AppLauncherTool(BaseTool)`:
```python
class AppLauncherTool(BaseTool):
    name = "open_app"
    description = "Open an application by name"
    category = "system"
    requires_confirmation = False
    
    def execute(self, name: str) -> ToolResult:
        result = open_app(name)
        return ToolResult(success=result["success"], data=result,
                          error=result.get("error", ""))

class AppCloseTool(BaseTool):
    name = "close_app"
    description = "Close an application by name"
    category = "system"
    requires_confirmation = True
    
    def execute(self, name: str) -> ToolResult:
        result = close_app(name)
        return ToolResult(success=result["success"], data=result,
                          error=result.get("error", ""))
```

**SUCCESS CRITERIA:**
- `registry.discover()` finds `open_app` and `close_app`
- `execute_tool("open_app", {"name": "notepad"})` → success + Notepad opens
- `execute_tool("close_app", {"name": "notepad"})` → prompts for confirmation; after "y", closes

---

### TASK 5.2 — System info + process control

**FILES:** `src/skills/system/sysinfo.py`

**Tools to implement:**

`system_info` — Get CPU%, RAM, disk, GPU VRAM:
```python
import psutil, platform
try:
    import pynvml
    pynvml.nvmlInit()
    HAS_GPU = True
except:
    HAS_GPU = False

class SystemInfoTool(BaseTool):
    name = "system_info"
    description = "Get CPU, RAM, disk, and GPU usage statistics"
    category = "system"
    
    def execute(self) -> ToolResult:
        data = {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "ram_used_gb": psutil.virtual_memory().used / 1e9,
            "ram_total_gb": psutil.virtual_memory().total / 1e9,
            "disk_free_gb": psutil.disk_usage('/').free / 1e9,
        }
        if HAS_GPU:
            handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            mem = pynvml.nvmlDeviceGetMemoryInfo(handle)
            data["gpu_vram_used_gb"] = mem.used / 1e9
            data["gpu_vram_total_gb"] = mem.total / 1e9
        return ToolResult(success=True, data=data)
```

`list_processes` — Running processes:
`kill_process(name_or_pid)` — requires_confirmation=True
`get_network_info()` — IP addresses, adapter names

**SUCCESS CRITERIA:**
- `system_info()` returns valid numeric CPU/RAM values
- `list_processes()` returns list with at least 5 entries
- `kill_process("notepad.exe")` prompts, kills after confirm

---

### TASK 5.3 — Clipboard manager

**FILES:** `src/skills/system/clipboard.py`

```python
import pyperclip, platform

class ReadClipboardTool(BaseTool):
    name = "read_clipboard"
    description = "Read the current clipboard content"
    category = "system"
    
    def execute(self) -> ToolResult:
        try:
            text = pyperclip.paste()
            return ToolResult(success=True, data={"content": text, "type": "text"})
        except Exception as e:
            return ToolResult(success=False, error=str(e))

class WriteClipboardTool(BaseTool):
    name = "write_clipboard"
    description = "Write text to the clipboard"
    category = "system"
    
    def execute(self, text: str) -> ToolResult:
        pyperclip.copy(text)
        return ToolResult(success=True, data={"written": text[:50] + "..." if len(text) > 50 else text})
```

**SUCCESS CRITERIA:**
- Copy text in Notepad. Call `read_clipboard()` → returns that text.
- Call `write_clipboard("hello from Jarvis")` → paste anywhere → "hello from Jarvis" appears.

---

### TASK 5.4 — Windows notifications (cross-platform)

**FILES:** `src/skills/notify/toasts.py`

```python
import platform

class SendNotificationTool(BaseTool):
    name = "send_notification"
    description = "Send a system notification/toast message"
    category = "notify"
    
    def execute(self, title: str, message: str, type: str = "info") -> ToolResult:
        sys = platform.system().lower()
        try:
            if sys == "windows":
                from winotify import Notification
                toast = Notification(app_id="Jarvis", title=title, msg=message)
                toast.show()
            elif sys == "linux":
                import subprocess
                subprocess.run(["notify-send", f"[{type.upper()}] {title}", message])
            elif sys == "darwin":
                import subprocess
                subprocess.run(["osascript", "-e",
                    f'display notification "{message}" with title "Jarvis: {title}"'])
            return ToolResult(success=True, data={"title": title, "type": type})
        except Exception as e:
            # Fallback: print to console
            print(f"\n🔔 [{type.upper()}] {title}: {message}")
            return ToolResult(success=True, data={"title": title, "fallback": "console"})
```

**SUCCESS CRITERIA:**
- `send_notification("Test", "Hello from Jarvis", "info")` → notification appears (or console output on unsupported system)
- Works on Windows (winotify), Linux (notify-send), macOS (osascript)

---

### TASK 5.5 — Screen capture + OCR

**FILES:** `src/skills/screen/capture.py`

```python
import mss, pytesseract, time
from pathlib import Path
from PIL import Image

class ScreenshotTool(BaseTool):
    name = "take_screenshot"
    description = "Take a screenshot of the full screen or a region"
    category = "screen"
    
    def execute(self, region: dict | None = None) -> ToolResult:
        Path("data/screenshots").mkdir(parents=True, exist_ok=True)
        filename = f"data/screenshots/screenshot_{int(time.time())}.png"
        
        with mss.mss() as sct:
            if region:
                monitor = {"left": region["x"], "top": region["y"],
                           "width": region["w"], "height": region["h"]}
            else:
                monitor = sct.monitors[1]  # full screen
            
            sct.shot(mon=sct.monitors.index(monitor) if not region else -1, output=filename)
            # Use grab for region
            if region:
                img = sct.grab(monitor)
                mss.tools.to_png(img.rgb, img.size, output=filename)
        
        return ToolResult(success=True, data={"path": filename})

class OCRTool(BaseTool):
    name = "read_screen_text"
    description = "Take a screenshot and extract text from it using OCR"
    category = "screen"
    
    def execute(self) -> ToolResult:
        screenshot_result = ScreenshotTool().execute()
        if not screenshot_result.success:
            return screenshot_result
        
        path = screenshot_result.data["path"]
        text = pytesseract.image_to_string(Image.open(path), lang="ara+eng")
        return ToolResult(success=True, data={"text": text.strip(), "screenshot": path})
```

**SUCCESS CRITERIA:**
- `take_screenshot()` → PNG file created in `data/screenshots/`
- `read_screen_text()` on a screen with visible text → text extracted with > 70% accuracy

---

### TASK 5.6 — File operations

**FILES:** `src/skills/files/file_ops.py`

Implement all file operations as BaseTool subclasses:
- `ReadFileTool` (name="read_file") — read text file → content
- `WriteFileTool` (name="write_file") — write content to file (confirm if overwrite)
- `ListDirectoryTool` (name="list_directory") — list files with metadata
- `SearchFilesTool` (name="search_files") — glob by name + optional grep by content
- `MoveFileTool` (name="move_file", requires_confirmation=True) — move file
- `CopyFileTool` (name="copy_file") — copy file
- `DeleteFileTool` (name="delete_file", requires_confirmation=True) — send to recycle bin via `send2trash`

Path safety for all write/delete operations:
```python
ALLOWED_ROOTS = [
    Path.home(),
    Path("data"),
    Path("logs"),
]

def _is_path_safe(path: Path) -> bool:
    path = path.resolve()
    return any(path.is_relative_to(root.resolve()) for root in ALLOWED_ROOTS)
```

**SUCCESS CRITERIA:**
- Read a known file → correct content returned
- Write to `data/test.txt` → file created
- Delete file → file in Recycle Bin (not permanently deleted)
- Delete file outside allowed roots → blocked with error

---

### TASK 5.7 — Code executor

**FILES:** `src/skills/coder/executor.py`

```python
import subprocess, tempfile, time, re
from pathlib import Path

BLOCKED_PATTERNS = [
    r"os\.remove\s*\(",
    r"shutil\.rmtree\s*\(",
    r"subprocess\.run\s*\(",
    r"os\.system\s*\(",
    r"sys\.exit\s*\(",
    r"__import__\s*\(",
]
BLOCKED_SHELL = ["rm -rf", "format", "del /s", "shutdown", "reboot", "mkfs"]

class RunPythonTool(BaseTool):
    name = "execute_python"
    description = "Execute Python code and return stdout/stderr"
    category = "coder"
    requires_confirmation = True
    
    def execute(self, code: str, timeout: int = 30) -> ToolResult:
        for pattern in BLOCKED_PATTERNS:
            if re.search(pattern, code):
                return ToolResult(success=False, error=f"Blocked: pattern '{pattern}' not allowed")
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write(code)
            fname = f.name
        
        start = time.time()
        try:
            result = subprocess.run(
                ["python", fname], capture_output=True, text=True,
                timeout=timeout, encoding='utf-8'
            )
            return ToolResult(success=result.returncode == 0, data={
                "stdout": result.stdout, "stderr": result.stderr,
                "returncode": result.returncode,
                "duration_ms": (time.time() - start) * 1000,
            })
        except subprocess.TimeoutExpired:
            return ToolResult(success=False, error=f"Timeout after {timeout}s")
        finally:
            Path(fname).unlink(missing_ok=True)
```

**SUCCESS CRITERIA:**
- `execute_python("print(2+2)")` → stdout="4\n", success=True
- `execute_python("import os; os.remove('/')") ` → blocked, success=False
- `execute_python("import time; time.sleep(999)")` → timeout error after configured seconds

---

### TASK 5.8 — Web search

**FILES:** `src/skills/search/web_search.py`

```python
import httpx, re
from bs4 import BeautifulSoup
from functools import lru_cache
import time

_cache: dict[str, tuple[list, float]] = {}
CACHE_TTL = 300  # 5 minutes

class WebSearchTool(BaseTool):
    name = "web_search"
    description = "Search the web using DuckDuckGo and return results"
    category = "search"
    
    def execute(self, query: str, max_results: int = 5) -> ToolResult:
        # Check cache
        if query in _cache:
            results, cached_at = _cache[query]
            if time.time() - cached_at < CACHE_TTL:
                return ToolResult(success=True, data={"results": results, "cached": True})
        
        try:
            headers = {"User-Agent": "Mozilla/5.0 (compatible; Jarvis/1.0)"}
            url = f"https://html.duckduckgo.com/html/?q={httpx.URL(query=query)}"
            
            with httpx.Client(timeout=10, headers=headers, follow_redirects=True) as client:
                resp = client.get(url)
            
            soup = BeautifulSoup(resp.text, "html.parser")
            results = []
            for r in soup.select(".result__body")[:max_results]:
                title_el = r.select_one(".result__title")
                url_el = r.select_one(".result__url")
                snippet_el = r.select_one(".result__snippet")
                if title_el and url_el:
                    results.append({
                        "title": title_el.get_text(strip=True),
                        "url": url_el.get_text(strip=True),
                        "snippet": snippet_el.get_text(strip=True) if snippet_el else "",
                    })
            
            _cache[query] = (results, time.time())
            return ToolResult(success=True, data={"results": results})
        except Exception as e:
            return ToolResult(success=False, error=str(e))
```

**SUCCESS CRITERIA:**
- `web_search("Python tutorial")` → 5 results with valid titles and URLs
- Same query within 5 minutes → returns cached=True, no HTTP request made
- Network failure → returns success=False with error message

---

## 🌐 Phase 6 — Browser & Web Skills

> **End state:** Playwright browser with persistent sessions, downloads, WhatsApp automation.

---

### TASK 6.1 — Playwright browser singleton

**FILES:** `src/skills/browser/browser.py`

Single browser instance (not recreated per call). Session manager integrated.

```python
from playwright.sync_api import sync_playwright, Browser, Page
import atexit

_playwright = None
_browser: Browser | None = None
_page: Page | None = None

def get_browser() -> Browser:
    global _playwright, _browser
    if not _browser:
        _playwright = sync_playwright().__enter__()
        _browser = _playwright.chromium.launch(headless=False)
        atexit.register(cleanup)
    return _browser

def get_page(domain: str | None = None) -> Page:
    global _page
    browser = get_browser()
    if not _page:
        context = _load_session(browser, domain) if domain else browser.new_context()
        _page = context.new_page()
    return _page

def cleanup():
    global _playwright, _browser, _page
    try:
        if _page: _page.close()
        if _browser: _browser.close()
        if _playwright: _playwright.__exit__(None, None, None)
    except: pass
```

Implement tools:
- `NavigateTool` (name="browser_navigate") — go to URL
- `ClickTool` (name="browser_click") — click by selector/text
- `FillTool` (name="browser_fill") — fill input
- `GetTextTool` (name="browser_get_text") — get page text as Markdown
- `BrowserScreenshotTool` (name="browser_screenshot") — page screenshot

**SUCCESS CRITERIA:**
- `browser_navigate({"url": "https://example.com"})` → page title "Example Domain"
- `browser_fill` fills a known input field
- Browser stays open between tool calls (singleton)

---

### TASK 6.2 — Session persistence

**FILES:** `src/skills/browser/session.py`

```python
from pathlib import Path
import json
from cryptography.fernet import Fernet
import os

def _get_fernet() -> Fernet | None:
    key = os.environ.get("SESSION_ENCRYPTION_KEY")
    if key:
        return Fernet(key.encode())
    return None

def save_session(domain: str):
    page = get_page()
    state = page.context.storage_state()
    path = Path(f"data/sessions/{domain}.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    
    data = json.dumps(state)
    fernet = _get_fernet()
    if fernet:
        data = fernet.encrypt(data.encode()).decode()
    
    path.write_text(data, encoding="utf-8")

def load_session(domain: str) -> dict | None:
    path = Path(f"data/sessions/{domain}.json")
    if not path.exists():
        return None
    
    data = path.read_text(encoding="utf-8")
    fernet = _get_fernet()
    if fernet:
        try:
            data = fernet.decrypt(data.encode()).decode()
        except Exception:
            return None
    
    return json.loads(data)
```

**SUCCESS CRITERIA:**
- Log into a test website → `save_session("example.com")` → file created
- Kill Python process → restart → load session → navigate to site → still logged in

---

### TASK 6.3 — File download + upload

**FILES:** `src/skills/browser/transfer.py`

Downloads: intercept `page.on("download")` → save to `data/downloads/`
Uploads: `page.set_input_files(selector, file_path)`

**SUCCESS CRITERIA:**
- Download PDF from public URL → file in `data/downloads/`
- Upload local file to file input → confirmed via DOM state change

---

### TASK 6.4 — Auth wall handler

**FILES:** `src/skills/browser/auth_handler.py`

Detect login/captcha page → send notification → wait for user → save session on resume.

**SUCCESS CRITERIA:**
- Navigate to login-required page → notification appears → user logs in → Enter pressed → session saved → automation continues

---

### TASK 6.5 — WhatsApp Web automation

**FILES:** `src/skills/social/whatsapp.py`

Flow: load session → if expired: show QR → wait → save session → find contact → send message

**SUCCESS CRITERIA:**
- "Send Ahmed: Meeting at 3pm" → message appears in WhatsApp Web chat for Ahmed contact

---

### TASK 6.6 — Media player control

**FILES:** `src/skills/media/player.py`

System media keys for play/pause/next/prev. Volume control via pycaw (Windows), amixer (Linux), osascript (macOS).

**SUCCESS CRITERIA:**
- `set_volume(50)` → system volume at 50%
- `play_pause()` → current media player toggles

---

## 🔌 Phase 7 — Google APIs

> **End state:** One OAuth flow → Calendar, Gmail, Drive, Contacts, YouTube all functional.

---

### TASK 7.1 — Unified Google OAuth

**FILES:** `src/skills/api/google_auth.py`

Combined scopes in one consent. Token at `data/google_token.json`. Auto-refresh.

**SUCCESS CRITERIA:**
- First run → browser opens → user consents → token saved
- Second run → no browser → token loaded from file → all APIs accessible

---

### TASK 7.2 — Google Calendar (full CRUD)

**FILES:** `src/skills/api/calendar.py`

Tools: `calendar_list`, `calendar_create`, `calendar_update`, `calendar_delete`, `calendar_search`

**SUCCESS CRITERIA:**
- Create test event → list → found → delete → list → gone

---

### TASK 7.3 — Gmail (send/read/search/reply)

**FILES:** `src/skills/api/gmail.py`

Tools: `gmail_list`, `gmail_search`, `gmail_send` (confirmation), `gmail_reply` (confirmation), `gmail_mark`, `gmail_move`

**SUCCESS CRITERIA:**
- Send email to self → appears in inbox → search finds it → mark read → unread count decreases

---

### TASK 7.4 — Google Drive

**FILES:** `src/skills/api/drive.py`

Tools: `drive_list`, `drive_search`, `drive_upload`, `drive_download`, `drive_share`, `drive_create_folder`

**SUCCESS CRITERIA:**
- Upload `data/test.txt` → appears in Drive → download back → content matches

---

### TASK 7.5 — Google Contacts

**FILES:** `src/skills/api/contacts.py`

Tools: `contacts_list`, `contacts_search`, `contacts_get`, `contacts_create`
Integration: `resolve_name(name)` → email address (for Gmail "send to Ahmed" flow)

**SUCCESS CRITERIA:**
- Search known contact by name → email returned
- "Send email to [contact name]" → uses Contacts to resolve email → Gmail sends

---

### TASK 7.6 — YouTube

**FILES:** `src/skills/api/youtube.py`

Tools: `youtube_search`, `youtube_get_info`, `youtube_open`

**SUCCESS CRITERIA:**
- `youtube_search("machine learning")` → 5 results with valid YouTube URLs
- `youtube_open(video_id)` → browser opens that URL

---

### TASK 7.7 — PDF + Office readers/writers

**FILES:** `src/skills/pdf/reader.py`, `src/skills/office/reader.py`

PDF: `pdf_read_text`, `pdf_extract_tables`, `pdf_summarize` (LLM-assisted)
Office: `docx_read`, `xlsx_read`, `pptx_read`, `docx_write`, `xlsx_write`

**SUCCESS CRITERIA:**
- Extract text from a 5-page PDF → non-empty string returned
- Read a .docx file → text content returned
- Create a simple .docx with title + paragraph → file saved

---

## 💾 Phase 8 — Context + Memory

> **End state:** Facts from session 1 recalled in session 2. Memory injected into every turn.

---

### TASK 8.1 — Short-term memory (Redis + fallback)

**FILES:** `src/core/memory/short_term.py`

```python
import redis, json
from loguru import logger

_redis: redis.Redis | None = None
_fallback: dict[str, list] = {}

def _get_redis() -> redis.Redis | None:
    global _redis
    if _redis is None:
        try:
            _redis = redis.Redis(host="localhost", port=6379, decode_responses=True)
            _redis.ping()
        except Exception:
            logger.warning("memory.redis_unavailable — using in-memory fallback")
            _redis = False  # type: ignore
    return _redis if _redis else None

def save_message(session_id: str, role: str, content: str):
    message = {"role": role, "content": content}
    r = _get_redis()
    if r:
        r.rpush(f"history:{session_id}", json.dumps(message))
        r.expire(f"history:{session_id}", 86400)  # 24h TTL
        # Trim to last 50 messages
        r.ltrim(f"history:{session_id}", -50, -1)
    else:
        if session_id not in _fallback:
            _fallback[session_id] = []
        _fallback[session_id].append(message)
        _fallback[session_id] = _fallback[session_id][-50:]

def get_history(session_id: str, n: int = 10) -> list[dict]:
    r = _get_redis()
    if r:
        raw = r.lrange(f"history:{session_id}", -n, -1)
        return [json.loads(m) for m in raw]
    return _fallback.get(session_id, [])[-n:]
```

**SUCCESS CRITERIA:**
- Save 3 messages → get_history → returns 3 in order
- With Redis: restart Python → history still present
- Without Redis: in-memory fallback works (no crash)

---

### TASK 8.2 — Long-term semantic memory

**FILES:** `src/core/memory/long_term.py`

ChromaDB with sentence-transformers embeddings. `remember(text, metadata)` + `recall(query, n=5)`.

**SUCCESS CRITERIA:**
- `remember("User prefers concise Arabic summaries")`
- Restart Python
- `recall("user preferences")` → returns that text in top results

---

### TASK 8.3 — SQLite store

**FILES:** `src/core/memory/database.py`

Tables: conversations, feedback, tasks, routing_weights. Auto-create on init.

**SUCCESS CRITERIA:**
- Insert row in each table → restart → rows present

---

### TASK 8.4 — Memory injection into Context

**FILES:** MODIFY `src/core/context/assembler.py`

```python
from src.core.memory.short_term import get_history
from src.core.memory.long_term import recall

def assemble_context(user_message: str, session_id: str, attachments: list = []) -> ContextBundle:
    profile_data = load_profile()
    user_profile = UserProfile(**profile_data)
    
    # Inject history
    history_raw = get_history(session_id, n=10)
    recent_history = [Message(role=m["role"], content=m["content"]) for m in history_raw]
    
    # Inject semantic memories
    memory_snippets = recall(user_message, n=3)
    
    return ContextBundle(
        user_message=user_message,
        session_id=session_id,
        attachments=attachments,
        user_profile=user_profile,
        recent_history=recent_history,
        memory_snippets=memory_snippets,
        turn_number=_turn_counters.get(session_id, 0) + 1,
    )
```

**SUCCESS CRITERIA:**
- Tell Jarvis "my name is Ahmed" in turn 1
- Turn 2: "what is my name?" → "Ahmed" returned without explicit context

---

### TASK 8.5 — Auto-save after turns

**FILES:** MODIFY `src/core/runtime/loop.py`

After every `run_turn()`:
```python
from src.core.memory.short_term import save_message
from src.core.memory.long_term import remember
from src.core.memory.database import insert_conversation

save_message(session_id, "user", user_input)
save_message(session_id, "assistant", response)
insert_conversation(session_id, "user", user_input)
insert_conversation(session_id, "assistant", response)

if eval_result.quality > 0.8:
    remember(f"[{decision.intent}] User asked: '{user_input[:100]}' — response was well-received",
             metadata={"session": session_id, "model": decision.model, "type": "outcome"})
```

**SUCCESS CRITERIA:**
- 5 turns → 10 rows in SQLite conversations table
- Good responses saved to ChromaDB long-term memory

---

### TASK 8.6 — Feedback system + weight updates

**FILES:** `src/core/memory/feedback.py`, `src/core/decision/weight_updater.py`

Collect: `/thumbsup` = score 1.0, `/thumbsdown` = score 0.0. Implicit: user follows up = +0.1, rephrases = -0.3.

Update routing weights every 20 turns using exponential moving average.

**SUCCESS CRITERIA:**
- 20 turns with poor gemma3:4b performance on code → weight for (code, gemma3:4b) decreases

---

## 🤖 Phase 9 — Agents

> **End state:** Multi-step tasks like "research X, summarize, save to Drive" execute autonomously.

---

### TASK 9.1 — Thinker agent (CoT + self-critique)

**FILES:** `src/core/agents/thinker.py`

```python
from src.models.llm.engine import chat

THINK_SYSTEM = """Think step by step.
First: write your reasoning process.
Then: write your answer.
Then: critique your answer — what could be wrong or missing?
Finally: write your improved final answer after [FINAL ANSWER]:"""

def think(question: str, model: str = "qwen3:8b") -> str:
    response = chat(question, model=model, system=THINK_SYSTEM)
    # Extract final answer
    if "[FINAL ANSWER]:" in response:
        return response.split("[FINAL ANSWER]:")[-1].strip()
    return response
```

**SUCCESS CRITERIA:**
- `think("What are trade-offs between RAG and fine-tuning?")` → more detailed answer than direct `chat()` call
- Response contains reasoning steps before final answer

---

### TASK 9.2 — Planner agent (step decomposition)

**FILES:** `src/core/agents/planner.py`

LLM with planning mode produces JSON step list. Each step has: `id, description, tool, args, depends_on`.

**SUCCESS CRITERIA:**
- `plan("research AI news and email summary to ahmed@test.com", ["web_search", "send_email"])` → returns 2-3 ordered steps

---

### TASK 9.3 — Step executor (sequential with output passing)

**FILES:** `src/core/agents/step_executor.py`

Execute steps in order. Pass `step[N].result` as input to `step[N+1].args` where `depends_on` specifies it.

**SUCCESS CRITERIA:**
- 3-step plan: search → summarize → save to file. After execution, file exists with search content.

---

### TASK 9.4 — Researcher agent

**FILES:** `src/core/agents/researcher.py`

Generate 3 search queries → search each → fetch top result page content → summarize → combine into report.

**SUCCESS CRITERIA:**
- `research("local AI models 2025")` → Markdown report with content from 3+ distinct sources

---

### TASK 9.5 — Computer use agent

**FILES:** `src/core/agents/computer_use.py`

Loop: screenshot → OCR/LLaVA → LLM decides next action → pyautogui executes → repeat. Max 10 iterations. All actions require confirmation.

**SUCCESS CRITERIA:**
- Goal "open Notepad and type hello" → Notepad opens → "hello" typed → success message returned

---

## 🔒 Phase 10 — Safety + Capabilities

> **End state:** Dangerous operations blocked or confirmed. Tool capabilities match platform.

---

### TASK 10.1 — Complete safety system

**FILES:** MODIFY `src/core/tools/safety.py`

Add:
- Platform-specific dangerous commands
- File path traversal check
- Email/message rate limiting (max 10 per session)
- Confirmation timeout (30s, then auto-decline)

**SUCCESS CRITERIA:**
- All items in safety checklist from README pass
- Rate limit test: 11th email in session → blocked

---

### TASK 10.2 — Capability registry

**FILES:** MODIFY `config/skills.yaml`, `src/core/tools/registry.py`

Add `enabled` flag to each tool in skills.yaml. Platform filter: tools not available on current OS show as unavailable.

**SUCCESS CRITERIA:**
- `registry.all_available()` on Linux → no Windows-only tools
- `send_email` with `enabled: false` in skills.yaml → not in available tools

---

### TASK 10.3 — JSON Schema validation (all tools)

**FILES:** `config/schemas/` — create schema file for every tool

Create schemas for all tools from Phases 5-7. Validator uses schema before execution.

**SUCCESS CRITERIA:**
- `execute_tool("send_email", {"to": "not-an-email", "subject": "test", "body": "hi"})` → validation error returned (no email sent)

---

### TASK 10.4 — Error handling + retry + fallback

**FILES:** MODIFY `src/core/runtime/loop.py`, `src/core/runtime/executor.py`

Error classes: model_error, tool_error, validation_error, safety_blocked, timeout, vram_oom.
Each class has defined retry strategy.

**SUCCESS CRITERIA:**
- Mock Ollama returning empty → retry fires with next model
- Mock tool raising exception → ToolResult(success=False) returned, loop continues

---

## 📊 Phase 11 — Logging + Feedback

> **End state:** All decisions logged. Feedback collected. Routing weights update.

---

### TASK 11.1 — Complete structured logging

**FILES:** MODIFY all runtime files

Every event has structured key=value pairs. Log file is grep-friendly.

Events logged: `turn.start`, `decision`, `tool.start`, `tool.done`, `tool.error`, `eval`, `turn.end`, `model.swap`, `memory.save`, `escalation`

**SUCCESS CRITERIA:**
- After 5 turns: `grep "decision" logs/jarvis.log` shows 5 lines with intent/model/mode

---

### TASK 11.2 — Feedback collection

**FILES:** `src/core/memory/feedback.py`

**SUCCESS CRITERIA:**
- 5 turns → 5 feedback rows in SQLite
- `/thumbsup` → score 1.0 in feedback table

---

### TASK 11.3 — Routing weight updates

**FILES:** `src/core/decision/weight_updater.py`

**SUCCESS CRITERIA:**
- After simulating poor performance on code tasks → weight for (code, gemma3:4b) decreases numerically (verify in SQLite)

---

### TASK 11.4 — Observability dashboard data

**FILES:** `src/core/monitoring.py`

`get_stats()` → dict with: total_turns, avg_quality, most_used_model, tool_success_rates

This feeds the Web UI dashboard in Phase 13.

**SUCCESS CRITERIA:**
- `get_stats()` returns valid dict after 3 turns

---

## 💻 Phase 12 — CLI Interface

> **End state:** Rich terminal chat with streaming, Arabic RTL, slash commands, hotkeys.

---

### TASK 12.1 — Rich streaming chat loop

**FILES:** `src/interfaces/cli/interface.py`

```python
from rich.console import Console
from rich.live import Live
from rich.text import Text
from rich.panel import Panel
from src.core.runtime.loop import run_turn_streaming

console = Console()

def _is_rtl(text: str) -> bool:
    arabic_count = sum(1 for c in text if '\u0600' <= c <= '\u06FF')
    return arabic_count / max(len(text), 1) > 0.3

def run_cli(cfg):
    from src.core.config import create_directories
    create_directories()
    
    session_id = f"cli_{int(time.time())}"
    console.print(Panel("[bold green]Jarvis ready[/bold green] | /help for commands | Ctrl+C to exit"))
    
    while True:
        try:
            user_input = console.input("[bold blue]You:[/bold blue] ").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[yellow]Jarvis stopped.[/yellow]")
            break
        
        if not user_input:
            continue
        
        if user_input.startswith("/"):
            from src.interfaces.cli.commands import handle_command
            handle_command(user_input, session_id, cfg)
            continue
        
        response_parts = []
        with Live(Text("⏳ Thinking..."), refresh_per_second=10, console=console) as live:
            for token in run_turn_streaming(user_input, session_id):
                response_parts.append(token)
                response = "".join(response_parts)
                justify = "right" if _is_rtl(response) else "left"
                live.update(Text(f"Jarvis: {response}", justify=justify))
        
        # Save to history
        from src.core.memory.short_term import save_message
        save_message(session_id, "user", user_input)
        save_message(session_id, "assistant", "".join(response_parts))
```

**SUCCESS CRITERIA:**
- Arabic message → response with RTL alignment
- Streaming shows tokens appearing progressively
- Ctrl+C exits cleanly

---

### TASK 12.2 — Slash commands

**FILES:** `src/interfaces/cli/commands.py`

All 9 commands from README implemented:
`/clear`, `/model`, `/mode`, `/memory`, `/tools`, `/status`, `/profile`, `/config`, `/help`

**SUCCESS CRITERIA:**
- All 9 commands execute without error
- `/model qwen3:8b` changes model for session
- `/clear` clears history with confirmation prompt

---

### TASK 12.3 — Global hotkeys + tray

**FILES:** `src/interfaces/cli/hotkeys.py`, `src/interfaces/cli/tray.py`

Ctrl+Alt+J → bring CLI to focus. Ctrl+Alt+S → start voice input.
System tray (pystray): Open CLI / Open Web / Quit.

**SUCCESS CRITERIA:**
- Ctrl+Alt+J from another window → CLI window comes to focus
- Tray icon visible in system notification area

---

### TASK 12.4 — Input history

**FILES:** MODIFY `src/interfaces/cli/interface.py`

Arrow up/down → previous inputs. Persistence in `data/cli_history.txt`.

**SUCCESS CRITERIA:**
- Type 3 messages. Up arrow 3 times. All 3 recalled in reverse order. Survives restart.

---

### TASK 12.5 — Status bar

**FILES:** MODIFY `src/interfaces/cli/interface.py`

One-line status after each response: `[qwen3:8b] [deep] [turn: 5] [session: abc]`

**SUCCESS CRITERIA:**
- Status bar updates after every turn with correct model, mode, turn count

---

## 🌐 Phase 13 — Web UI

> **End state:** Premium glassmorphism chat browser interface with all features.

---

### TASK 13.1 — FastAPI app + WebSocket

**FILES:** `src/interfaces/web/app.py`, `src/interfaces/web/ws.py`, `app/server.py`

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI(title="Jarvis Web UI")
app.mount("/static", StaticFiles(directory="src/interfaces/web/static"), name="static")
templates = Jinja2Templates(directory="src/interfaces/web/templates")

@app.get("/", response_class=HTMLResponse)
async def index(request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(ws: WebSocket, session_id: str):
    await ws.accept()
    try:
        while True:
            data = await ws.receive_json()
            message = data.get("message", "")
            mode = data.get("mode", "normal")
            
            from src.core.runtime.loop import run_turn_streaming
            async for token in async_wrap_generator(run_turn_streaming(message, session_id)):
                await ws.send_json({"type": "token", "data": token})
            await ws.send_json({"type": "done"})
    except WebSocketDisconnect:
        pass
```

**SUCCESS CRITERIA:**
- Navigate to localhost:8080 → page loads
- Send message → streamed response appears in browser

---

### TASK 13.2 — HTML structure

**FILES:** `src/interfaces/web/templates/index.html`

Structure:
```html
<body>
  <div id="sidebar">
    <div id="search-bar">...</div>
    <div id="conversation-list">...</div>
    <div id="settings-btn">...</div>
  </div>
  <div id="main">
    <div id="header">
      <button id="sidebar-toggle">☰</button>
      <div id="model-indicator">qwen3:8b | normal</div>
    </div>
    <div id="messages">...</div>
    <div id="input-bar">
      <button id="attach-btn">+</button>
      <div id="mode-selector">⚡ 🧠 ⚛ 📋 🔭</div>
      <textarea id="message-input" placeholder="Message Jarvis..."></textarea>
      <button id="send-btn">↑</button>
    </div>
  </div>
  <div id="settings-panel" class="hidden">...</div>
</body>
```

**SUCCESS CRITERIA:**
- All structural elements present in DOM
- No JavaScript errors in browser console on load

---

### TASK 13.3 — CSS: Glassmorphism design system

**FILES:** `src/interfaces/web/static/style.css`

Complete CSS implementation:

```css
/* Color tokens */
:root {
  --bg-primary: #0a0a1a;
  --bg-secondary: #12122a;
  --glass-bg: rgba(255, 255, 255, 0.05);
  --glass-border: rgba(255, 255, 255, 0.08);
  --glass-blur: 16px;
  --accent-blue: #3b82f6;
  --accent-teal: #06b6d4;
  --accent-violet: #8b5cf6;
  --accent-gradient: linear-gradient(135deg, #3b82f6, #06b6d4, #8b5cf6);
  --text-primary: #f1f5f9;
  --text-secondary: #94a3b8;
  --text-muted: #64748b;
  --success: #22c55e;
  --error: #ef4444;
  --warning: #f59e0b;
  --shadow-glow: 0 0 20px rgba(59, 130, 246, 0.15);
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-xl: 24px;
  --font-sans: 'Inter', system-ui, sans-serif;
  --font-arabic: 'IBM Plex Arabic', 'Noto Sans Arabic', sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
}

/* Light theme */
[data-theme="light"] {
  --bg-primary: #f8fafc;
  --bg-secondary: #f1f5f9;
  --glass-bg: rgba(255, 255, 255, 0.7);
  --glass-border: rgba(0, 0, 0, 0.08);
  --text-primary: #0f172a;
  --text-secondary: #475569;
}

/* Base */
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: var(--bg-primary);
  color: var(--text-primary);
  font-family: var(--font-sans);
  height: 100vh;
  display: flex;
  overflow: hidden;
}

/* Glassmorphism panel */
.glass {
  background: var(--glass-bg);
  backdrop-filter: blur(var(--glass-blur));
  -webkit-backdrop-filter: blur(var(--glass-blur));
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-md);
}

/* Sidebar */
#sidebar {
  width: 280px;
  min-width: 280px;
  height: 100vh;
  background: var(--bg-secondary);
  border-right: 1px solid var(--glass-border);
  display: flex;
  flex-direction: column;
  padding: 16px;
  transition: transform 0.3s ease;
}
#sidebar.collapsed {
  transform: translateX(-280px);
  position: absolute;
}

/* Conversation list */
.conversation-item {
  padding: 10px 12px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: background 0.15s;
}
.conversation-item:hover { background: var(--glass-bg); }
.conversation-item.active {
  background: var(--glass-bg);
  border-left: 3px solid var(--accent-blue);
}
.conv-title { font-size: 14px; color: var(--text-primary); font-weight: 500; }
.conv-preview { font-size: 12px; color: var(--text-muted); margin-top: 2px; }
.conv-date { font-size: 11px; color: var(--text-muted); }

/* Date group headers */
.date-group-label {
  font-size: 11px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding: 8px 12px 4px;
}

/* Main chat area */
#main {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
}

/* Header */
#header {
  display: flex;
  align-items: center;
  padding: 12px 20px;
  border-bottom: 1px solid var(--glass-border);
  gap: 12px;
}
#model-indicator {
  font-size: 13px;
  color: var(--text-secondary);
  background: var(--glass-bg);
  padding: 4px 12px;
  border-radius: 99px;
  border: 1px solid var(--glass-border);
}

/* Messages */
#messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* Message bubbles */
.message { display: flex; gap: 12px; max-width: 80%; }
.message.user { align-self: flex-end; flex-direction: row-reverse; }
.message.assistant { align-self: flex-start; }
.message-content {
  padding: 12px 16px;
  border-radius: var(--radius-md);
  font-size: 15px;
  line-height: 1.6;
}
.message.user .message-content {
  background: var(--accent-gradient);
  background: linear-gradient(135deg, var(--accent-blue), var(--accent-teal));
  color: white;
  border-radius: var(--radius-md) var(--radius-md) 4px var(--radius-md);
}
.message.assistant .message-content {
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  border-radius: 4px var(--radius-md) var(--radius-md) var(--radius-md);
}
.message.rtl { direction: rtl; }
.message.rtl .message-content { text-align: right; font-family: var(--font-arabic); }

/* Typing indicator */
.typing-indicator { display: flex; gap: 4px; align-items: center; padding: 12px 16px; }
.typing-dot {
  width: 8px; height: 8px;
  background: var(--accent-blue);
  border-radius: 50%;
  animation: typing-pulse 1.4s infinite;
}
.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes typing-pulse {
  0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
  30% { transform: translateY(-6px); opacity: 1; }
}

/* Message animations */
.message { animation: message-in 0.3s cubic-bezier(0.34, 1.56, 0.64, 1); }
@keyframes message-in {
  from { opacity: 0; transform: translateY(8px) scale(0.97); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}

/* Code blocks */
pre {
  background: #1e1e2e;
  border-radius: var(--radius-sm);
  padding: 16px;
  overflow-x: auto;
  position: relative;
  margin: 8px 0;
}
pre .copy-btn {
  position: absolute;
  top: 8px; right: 8px;
  font-size: 12px;
  padding: 4px 8px;
  border-radius: 4px;
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  cursor: pointer;
  color: var(--text-secondary);
}
code { font-family: var(--font-mono); font-size: 14px; }

/* Input bar */
#input-bar {
  padding: 16px 20px;
  border-top: 1px solid var(--glass-border);
  display: flex;
  align-items: flex-end;
  gap: 8px;
}
#message-input {
  flex: 1;
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-md);
  padding: 12px 16px;
  color: var(--text-primary);
  font-size: 15px;
  font-family: var(--font-sans);
  resize: none;
  min-height: 44px;
  max-height: 200px;
  transition: border-color 0.2s, box-shadow 0.2s;
  overflow-y: auto;
}
#message-input:focus {
  outline: none;
  border-color: var(--accent-blue);
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
}
#message-input::placeholder { color: var(--text-muted); }

/* Mode selector */
#mode-selector {
  display: flex;
  gap: 4px;
  align-items: center;
}
.mode-btn {
  width: 32px; height: 32px;
  border-radius: 8px;
  border: 1px solid var(--glass-border);
  background: transparent;
  cursor: pointer;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s;
  color: var(--text-secondary);
}
.mode-btn:hover { background: var(--glass-bg); }
.mode-btn.active {
  background: rgba(59, 130, 246, 0.2);
  border-color: var(--accent-blue);
  color: var(--accent-blue);
}

/* Send / Mic button */
#send-btn {
  width: 40px; height: 40px;
  border-radius: 50%;
  background: var(--accent-gradient);
  background: linear-gradient(135deg, var(--accent-blue), var(--accent-teal));
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  color: white;
  transition: transform 0.15s, box-shadow 0.15s;
  flex-shrink: 0;
}
#send-btn:hover { transform: scale(1.08); box-shadow: var(--shadow-glow); }
#send-btn:active { transform: scale(0.95); }

/* Attachment preview */
#attachment-strip {
  display: flex; gap: 8px; flex-wrap: wrap;
  padding: 8px 20px 0;
}
.attachment-card {
  display: flex; align-items: center; gap: 6px;
  padding: 6px 10px;
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-sm);
  font-size: 13px;
}
.attachment-remove { cursor: pointer; color: var(--error); font-size: 16px; }

/* Toast notifications */
#toast-container {
  position: fixed;
  top: 20px; right: 20px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.toast {
  padding: 12px 16px;
  border-radius: var(--radius-sm);
  font-size: 14px;
  animation: toast-in 0.3s ease;
  max-width: 300px;
}
.toast.success { background: rgba(34, 197, 94, 0.15); border: 1px solid var(--success); color: var(--success); }
.toast.error { background: rgba(239, 68, 68, 0.15); border: 1px solid var(--error); color: var(--error); }
.toast.info { background: rgba(59, 130, 246, 0.15); border: 1px solid var(--accent-blue); color: var(--accent-blue); }
.toast.warning { background: rgba(245, 158, 11, 0.15); border: 1px solid var(--warning); color: var(--warning); }
@keyframes toast-in {
  from { opacity: 0; transform: translateX(20px); }
  to { opacity: 1; transform: translateX(0); }
}

/* Settings panel */
#settings-panel {
  position: absolute; right: 0; top: 0;
  width: 320px; height: 100vh;
  background: var(--bg-secondary);
  border-left: 1px solid var(--glass-border);
  padding: 20px;
  overflow-y: auto;
  transform: translateX(100%);
  transition: transform 0.3s ease;
  z-index: 100;
}
#settings-panel.open { transform: translateX(0); }

/* Responsive */
@media (max-width: 768px) {
  #sidebar { position: absolute; z-index: 50; width: 100%; }
  .message { max-width: 95%; }
}

/* Dashboard */
#dashboard {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 12px;
  padding: 12px 20px;
  border-bottom: 1px solid var(--glass-border);
}
.stat-card {
  padding: 10px 14px;
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-sm);
}
.stat-label { font-size: 11px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; }
.stat-value { font-size: 18px; font-weight: 600; color: var(--text-primary); margin-top: 2px; }
.vram-bar {
  height: 4px;
  background: var(--glass-border);
  border-radius: 99px;
  margin-top: 4px;
  overflow: hidden;
}
.vram-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--success), var(--accent-blue));
  border-radius: 99px;
  transition: width 0.5s ease;
}
```

**SUCCESS CRITERIA:**
- CSS loads without errors
- Dark theme renders correctly
- Mode buttons visually distinct when active
- Message bubbles styled correctly (user: gradient, assistant: glass)

---

### TASK 13.4 — JavaScript: chat.js

**FILES:** `src/interfaces/web/static/chat.js`

Complete JavaScript including:
- WebSocket connection + reconnect logic
- Token streaming: append tokens as they arrive, show cursor
- RTL detection: if >30% Arabic chars → `direction: rtl`
- Markdown rendering (marked.js from CDN)
- Syntax highlighting (highlight.js)
- Mode selector: update active mode; send mode with message
- Send/Mic button morph: empty → mic icon; typing → send arrow
- Attachment system: "+" menu, drag-and-drop, paste image, preview strip
- Conversation sidebar: group by date, rename inline, delete with confirm
- Settings panel: theme toggle, font size, default mode, enter key behavior
- Toast notification system: 4 types, auto-dismiss 4s
- Dashboard: poll `/api/status` every 3s, update VRAM bar, active tool
- Feedback buttons: 👍/👎 per message → POST to `/api/feedback`

```javascript
// Minimal skeleton — expand each section fully:
const ws_url = `ws://${location.host}/ws/${generateSessionId()}`;
let ws, currentMode = 'normal', activeSessionId = null;

function connect() {
  ws = new WebSocket(ws_url);
  ws.onopen = () => showToast('Connected', 'success');
  ws.onclose = () => { showToast('Reconnecting...', 'warning'); setTimeout(connect, 2000); };
  ws.onerror = (e) => showToast('Connection error', 'error');
  ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    if (msg.type === 'token') appendToken(msg.data);
    if (msg.type === 'done') finalizeMessage();
  };
}

function sendMessage() {
  const text = document.getElementById('message-input').value.trim();
  if (!text || !ws || ws.readyState !== WebSocket.OPEN) return;
  
  addUserMessage(text);
  showTypingIndicator();
  
  ws.send(JSON.stringify({ message: text, mode: currentMode }));
  document.getElementById('message-input').value = '';
  autoResizeTextarea();
}

function addUserMessage(text) {
  const isRTL = detectRTL(text);
  const div = createMessageEl('user', text, isRTL);
  document.getElementById('messages').appendChild(div);
  scrollToBottom();
}

function detectRTL(text) {
  const arabicCount = (text.match(/[\u0600-\u06FF]/g) || []).length;
  return arabicCount / Math.max(text.length, 1) > 0.3;
}

// ... (full implementation of all features listed above)
```

**SUCCESS CRITERIA:**
- Streaming messages appear token-by-token with cursor
- Arabic messages render RTL
- Mode selector updates active mode
- Drag-and-drop file attaches successfully
- Toast notification appears and auto-dismisses

---

### TASK 13.5 — REST API routes

**FILES:** `src/interfaces/web/routes.py`

Implement all 11 endpoints from README Section 9 (Tool System → REST API Routes).

**SUCCESS CRITERIA:**
- All endpoints return correct HTTP 200/400/404 status codes
- Conversation CRUD works end-to-end
- `/api/status` returns VRAM, model, and system health data

---

### TASK 13.6 — Settings panel implementation

**FILES:** MODIFY `src/interfaces/web/static/chat.js`

Settings panel sections:
1. **Appearance:** theme (dark/light/system), accent color, font size (sm/md/lg/xl), message density, blur intensity (for accessibility), animations toggle, bubble style
2. **Behavior:** default mode, default language, response style, auto-scroll, sound notifications, enter key (send/newline), show model indicator, show confidence scores
3. **Model:** active model selector, temperature slider, max tokens slider, model override toggle
4. **Data & Privacy:** export conversations (JSON), export conversations (Markdown), clear all conversations, clear memory, reset profile
5. **About:** version, build date, Ollama status, model list

All settings persisted to `localStorage`. Changes apply immediately without page reload.

**SUCCESS CRITERIA:**
- Toggle dark/light → changes immediately
- Font size slider → text size changes live
- Temperature slider → visible value updates; sent with next message
- Export conversations → downloads JSON file

---

### TASK 13.7 — Conversation management (sidebar)

**FILES:** MODIFY `src/interfaces/web/static/chat.js`

- New conversation: generates new session_id; clears message area
- Load conversation: fetches messages from `/api/conversations/:id`; renders all
- Rename: inline contenteditable → Enter to save → PUT `/api/conversations/:id`
- Delete: confirm dialog → DELETE `/api/conversations/:id` → remove from list
- Pin: toggle pin → re-sort list (pinned first)
- Archive: move to "Archived" section at bottom
- Search: Ctrl+K → focus search input → filter by title (instant) → by content (debounced API call)
- Date groups: "Today", "Yesterday", "Previous 7 days", "Previous 30 days", "Older"

**SUCCESS CRITERIA:**
- Create 5 conversations → rename 2 → pin 1 → delete 1 → archive 1
- Pinned conversation stays at top after page reload (localStorage)
- Search "AI" → only conversations with "AI" in title shown

---

### TASK 13.8 — File upload integration

**FILES:** `src/interfaces/web/routes.py` (add upload endpoint), MODIFY `chat.js`

Upload flow:
1. User clicks "+" → selects file OR drags onto chat OR pastes image (Ctrl+V)
2. File uploaded to POST `/api/upload` → server saves to `data/temp/` → returns `{id, name, type, size}`
3. Attachment card shown in preview strip with: icon, name, size, × button
4. When message sent: include `attachments: [{id, type}]` in WebSocket message
5. Server resolves attachment IDs to file paths; passes to context assembler

**SUCCESS CRITERIA:**
- Upload image → preview card appears above input bar
- Send message with image → LLaVA describes image in response
- Upload PDF → send "summarize this" → summary returned

---

### TASK 13.9 — Markdown + code rendering

**FILES:** `src/interfaces/web/static/chat.js`

Use `marked.js` (CDN) for Markdown parsing. Use `highlight.js` (CDN) for syntax highlighting.

Code blocks: add "Copy" button (top-right). Click → copy code → show "Copied!" for 2s.

KaTeX (CDN): render `$...$` and `$$...$$` math expressions.

**SUCCESS CRITERIA:**
- Response with `**bold**`, `- list item`, `` `code` `` renders correctly
- Code block with Python → syntax colored + Copy button works
- Math expression `$E=mc^2$` renders as formatted equation

---

### TASK 13.10 — Connection status + error states

**FILES:** MODIFY `src/interfaces/web/static/chat.js`

States:
- **Connected:** green dot in header
- **Reconnecting:** yellow dot + "Reconnecting..." text
- **Offline:** red dot + "No connection" + message input disabled
- **Error:** error toast + retry button on message

Reconnection: exponential backoff (1s, 2s, 4s, 8s, max 30s).

**SUCCESS CRITERIA:**
- Stop server → yellow dot → "Reconnecting..." shown
- Restart server → green dot restored → chat continues
- Message sent while offline → "Failed to send" toast

---

### TASK 13.11 — Dashboard panel

**FILES:** MODIFY template + chat.js

Dashboard shown above message area (collapsible). Updated every 3 seconds via `/api/status`.

Cards: VRAM % (with bar), Active Model, Active Tool, CPU%, RAM%.

**SUCCESS CRITERIA:**
- Dashboard visible above chat
- VRAM bar fills proportionally to actual GPU usage
- While a tool runs, "Active Tool" shows tool name

---

### TASK 13.12 — Feedback + message actions

**FILES:** MODIFY `chat.js`, add feedback endpoint to routes

Per-message actions (visible on hover):
- 👍 / 👎 (feedback)
- 📋 Copy full message
- 🔄 Regenerate (resend same user message)
- ✏️ Edit user message (only for user messages)

**SUCCESS CRITERIA:**
- Click 👍 → POST feedback → green highlight on button
- Click 📋 → full message text copied to clipboard
- Click 🔄 → same request sent again → new response replaces old

---

## 🎙️ Phase 14 — Voice Pipeline

> **End state:** "Hey Jarvis" → speak command → hear spoken response.

---

### TASK 14.1 — Whisper STT

**FILES:** `src/models/speech/stt.py`

Load `whisper.load_model("medium")`. Record with sounddevice. Auto-detect Arabic/English.

**SUCCESS CRITERIA:**
- 5 seconds Arabic speech → correct Arabic text
- 5 seconds English speech → correct English text

---

### TASK 14.2 — Piper TTS

**FILES:** `src/models/speech/tts.py`

Load Arabic + English Piper voices. Auto-select based on text language. `speak(text, lang)` plays audio via sounddevice.

**SUCCESS CRITERIA:**
- `speak("مرحباً", "ar")` → natural Arabic audio plays
- `speak("Hello", "en")` → natural English audio plays

---

### TASK 14.3 — Wake word detection

**FILES:** `src/interfaces/voice/wake_word.py`

openWakeWord `hey_jarvis` model. Score > 0.5 threshold. Fire EventBus event.

**SUCCESS CRITERIA:**
- "Hey Jarvis" → detection within 1 second
- Random speech → no false triggers in 60-second test

---

### TASK 14.4 — Voice Activity Detection

**FILES:** `src/interfaces/voice/vad.py`

webrtcvad at aggressiveness=2. Stop recording after 1 second of continuous silence.

**SUCCESS CRITERIA:**
- Speak 3 seconds + 1 second silence → recording stops automatically at correct point

---

### TASK 14.5 — Full voice pipeline

**FILES:** `src/interfaces/voice/pipeline.py`

```python
def run_voice_pipeline(cfg):
    print("Voice pipeline ready. Say 'Hey Jarvis' to activate.")
    session_id = f"voice_{int(time.time())}"
    
    while True:
        wait_for_wake_word()     # blocks until detected
        play_activation_chime()  # audio feedback
        
        audio = record_with_vad()
        text = transcribe(audio)
        print(f"Heard: {text}")
        
        response = run_turn(text, session_id)
        
        lang = "ar" if is_arabic(response) else "en"
        speak(response, lang)
```

**SUCCESS CRITERIA:**
- "Hey Jarvis, what's the capital of Egypt?" → spoken answer within 15 seconds
- Arabic question → Arabic spoken answer
- English question → English spoken answer

---

## 👁️ Phase 15 — Vision + Image Generation

> **End state:** Images understood and described. Images generated from text prompts.

---

### TASK 15.1 — LLaVA image understanding

**FILES:** `src/models/vision/llava.py`

```python
import base64, ollama
from src.models.llm.engine import swap_to, get_active_model

def describe_image(image_path: str, question: str = "Describe this image in detail") -> str:
    prev_model = get_active_model()
    swap_to("llava:7b")
    
    with open(image_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    
    response = ollama.chat(
        model="llava:7b",
        messages=[{"role": "user", "content": question, "images": [b64]}]
    )
    return response["message"]["content"]
```

**SUCCESS CRITERIA:**
- Upload code screenshot → LLaVA identifies programming language and explains code
- Upload Arabic text image → text read correctly
- Image understanding works after text LLM has been active (VRAM swap)

---

### TASK 15.2 — Stable Diffusion image generation

**FILES:** `src/models/diffusion/sd.py`

```python
from diffusers import StableDiffusionPipeline
import torch
from pathlib import Path
import time

def generate_image(prompt: str, steps: int = 20, width: int = 512, height: int = 512) -> str:
    from src.models.llm.engine import swap_to, unload_current_model
    
    # Translate Arabic prompt to English (SD trained on English)
    if _is_arabic(prompt):
        from src.models.llm.engine import chat
        unload_current_model()  # free VRAM for translation
        prompt_en = chat(f"Translate to English for image generation. Output ONLY the translated prompt: {prompt}")
        prompt = prompt_en.strip()
    else:
        unload_current_model()
    
    pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16
    ).to("cuda")
    
    image = pipe(prompt, num_inference_steps=steps, width=width, height=height).images[0]
    
    Path("data/generated").mkdir(parents=True, exist_ok=True)
    output_path = f"data/generated/image_{int(time.time())}.png"
    image.save(output_path)
    
    del pipe
    torch.cuda.empty_cache()
    
    return output_path

def _is_arabic(text: str) -> bool:
    return sum(1 for c in text if '\u0600' <= c <= '\u06FF') / max(len(text), 1) > 0.3
```

**SUCCESS CRITERIA:**
- `generate_image("a sunset over the Nile river, digital art")` → PNG file created
- Arabic prompt `"جبل مغطى بالثلج"` → translated → image generated
- VRAM released after generation (verified by pynvml)

---

### TASK 15.3 — Vision integration into runtime

**FILES:** MODIFY `src/core/context/assembler.py`, `src/core/runtime/executor.py`

When image in attachments: call `describe_image(path)` → description added to `memory_snippets` before LLM call.

**SUCCESS CRITERIA:**
- Upload image of a chart → ask "what trend does this show?" → correct answer based on image

---

### TASK 15.4 — Screen description tool

**FILES:** `src/skills/screen/describe.py`

```python
class DescribeScreenTool(BaseTool):
    name = "describe_screen"
    description = "Take a screenshot and describe what's visible on the screen"
    category = "screen"
    
    def execute(self, question: str = "What is on this screen?") -> ToolResult:
        from src.skills.screen.capture import ScreenshotTool
        screenshot_result = ScreenshotTool().execute()
        if not screenshot_result.success:
            return screenshot_result
        
        from src.models.vision.llava import describe_image
        description = describe_image(screenshot_result.data["path"], question)
        return ToolResult(success=True, data={
            "description": description,
            "screenshot": screenshot_result.data["path"]
        })
```

**SUCCESS CRITERIA:**
- "What's on my screen?" → accurate description of visible windows and content

---

## 📱 Phase 16 — Telegram + GUI

> **End state:** Telegram bot works. PyQt6 desktop app with tray icon.

---

### TASK 16.1 — Telegram bot (full implementation)

**FILES:** `src/interfaces/telegram/bot.py`, `src/interfaces/telegram/handlers.py`, `src/interfaces/telegram/commands.py`

Handlers: text → run_turn, photo → vision, voice → STT + run_turn, document → reader + summary.
Commands: /start, /clear, /model, /mode, /image, /search.

**SUCCESS CRITERIA:**
- Arabic voice note → transcription + Arabic answer returned
- Photo upload → image described in Arabic

---

### TASK 16.2 — PyQt6 desktop app

**FILES:** `src/interfaces/gui/main_window.py`, `src/interfaces/gui/settings_dialog.py`

Chat area + input + send/mic buttons + model dropdown + mode toolbar. Arabic RTL rendering.

**SUCCESS CRITERIA:**
- Launch GUI → type Arabic → RTL correct
- Send/Mic button visible and functional

---

### TASK 16.3 — System tray + auto-start

**FILES:** `src/interfaces/gui/tray.py`, `src/interfaces/gui/autostart.py`

pystray tray icon. Menu: Open GUI / Open Web / Settings / Quit. Wake word in background.
Auto-start: Windows registry / Linux .desktop / macOS LaunchAgents.

**SUCCESS CRITERIA:**
- App in tray → Say "Hey Jarvis" → GUI window appears
- Enable auto-start → reboot → Jarvis starts automatically

---

### TASK 16.4 — Task decomposition engine

**FILES:** `src/core/agents/decomposer.py`, `src/core/agents/graph_executor.py`

DAG-based execution. Parallel frontier with asyncio.gather(). Selective retry (failed nodes only). Checkpoint resume.

**SUCCESS CRITERIA:**
- "Book meeting with Ahmed and email agenda" → Calendar + Gmail tools used in correct order
- Force-fail one node → only that node retries on `resume(run_id)`

---

## ✅ Phase 17 — QA + Security

> **End state:** Tests pass. No credentials in logs. Performance benchmarks met.

---

### TASK 17.1 — Complete test suite

**FILES:** `tests/` directory

Create test files:
- `test_models.py` — Ollama engine, VRAM guard, model swap
- `test_decision.py` — all intent types routed correctly
- `test_memory.py` — short/long term, cross-session, Redis fallback
- `test_tools.py` — registry discovery, safety gate, executor, schema validation
- `test_runtime.py` — full turn, retry, escalation, evaluator
- `test_skills.py` — app open/close, file ops, clipboard, notification, screenshot, code exec
- `test_browser.py` — navigation, session save/load, download
- `test_apis.py` — Google OAuth, Calendar CRUD, Gmail send/receive, Contacts resolve
- `test_agents.py` — planner step decomposition, thinker improvement, researcher multi-source
- `test_voice.py` — STT accuracy, TTS synthesis, wake word detection
- `test_vision.py` — LLaVA description, SD generation

**SUCCESS CRITERIA:**
- `pytest tests/ --cov=src` → 0 failures, ≥ 70% coverage

---

### TASK 17.2 — Security hardening audit

**FILES:** Multiple (review and fix)

Checklist:
- [ ] `delete_file` uses `send2trash` (never `os.remove` on user files)
- [ ] `run_shell` checks blocklist BEFORE subprocess.run
- [ ] `send_email` always shows confirmation prompt
- [ ] `google_token.json` not logged anywhere (grep logs/ for token patterns)
- [ ] `data/sessions/*.json` encrypted with Fernet when SESSION_ENCRYPTION_KEY set
- [ ] All tool args validated against JSON Schema before execution
- [ ] File paths restricted to ALLOWED_ROOTS (no path traversal)
- [ ] Error messages sanitized: no stack traces exposed to LLM
- [ ] `.env` in `.gitignore`; `.env.example` has no real values

**SUCCESS CRITERIA:**
- Every item above manually verified and checked off

---

### TASK 17.3 — Performance benchmarks

**FILES:** `scripts/benchmark.py`

```python
import time

benchmarks = {
    "cold_start": (10.0, "seconds from python app/main.py to first response"),
    "simple_chat_gemma": (5.0, "seconds for gemma3:4b response"),
    "file_read_tool": (1.0, "seconds for read_file tool"),
    "vram_peak_chat": (5.5, "GB VRAM during normal chat"),
    "voice_round_trip": (15.0, "seconds wake word to spoken answer"),
    "web_ui_first_message": (3.0, "seconds from send to first token"),
}
```

**SUCCESS CRITERIA:**
- All 6 metrics within targets
- Report generated as `data/benchmark_results.json`

---

### TASK 17.4 — Windows 11 clean install test

**FILES:** `scripts/install.ps1` (finalize + test)

Test on fresh Windows 11 machine (VM acceptable):
1. Run `install.ps1`
2. `python app/main.py --interface cli`
3. Text chat (Arabic + English)
4. File operations, app launch, notification, clipboard
5. Web UI at localhost:8080
6. Voice pipeline
7. Telegram (if configured)

**SUCCESS CRITERIA:**
- All steps complete without manual intervention beyond entering API keys

---

### TASK 17.5 — Linux test

**FILES:** `scripts/install.sh` (finalize + test)

Test on Ubuntu 22.04 or 24.04:
- Core chat, tools, browser, APIs
- Note any Windows-only features that correctly report as unavailable

**SUCCESS CRITERIA:**
- All platform-independent features work
- Windows-only tools return `is_available()=False` gracefully

---

### TASK 17.6 — Credential audit + CI setup

**FILES:** `scripts/credential_audit.py`, `.github/workflows/ci.yml`, `.pre-commit-config.yaml`

Credential audit: scan `logs/` for API key patterns. Should return 0 matches.

CI workflow:
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
      - run: mypy src/ --ignore-missing-imports
      - run: pytest tests/ --cov=src -x --tb=short
      - run: python scripts/credential_audit.py
```

**SUCCESS CRITERIA:**
- Credential audit: 0 matches
- CI passes on clean push
- Pre-commit hooks prevent bad commits locally

---

## 📌 Implementation Reference

### Layer Responsibilities (hard rules)

| Layer | File Location | Only Does | Never Does |
|-------|--------------|-----------|-----------|
| Interface | `src/interfaces/` | Receive input, display output | Classify, route, store |
| Context | `src/core/context/` | Bundle this turn's inputs | Store across turns |
| Decision | `src/core/decision/` | Classify intent, select model | Think, generate, execute |
| Runtime | `src/core/runtime/` | Drive the loop | Implement intelligence |
| Agents | `src/core/agents/` | Multi-step reasoning | Route requests, execute tools directly |
| Tools (mgmt) | `src/core/tools/` | Registry, validate, execute bridge | Implement tool logic |
| Skills (impl) | `src/skills/` | One specific action | Decisions, routing, storage |
| Models | `src/models/` | Wrap AI model I/O | Decisions, memory, tools |
| Memory | `src/core/memory/` | Persist data | Participate in routing |
| Identity | `src/core/identity/` | Build system prompts | Make routing decisions |

### Model Selection (quick reference)

```python
# In order of priority:
if has_image(context): return "llava:7b"
if intent == "code": return "qwen2.5-coder:7b"
if complexity == "low" or mode == "fast": return "gemma3:4b"
return "qwen3:8b"  # default
```

### Arabic Detection

```python
def is_arabic(text: str) -> bool:
    count = sum(1 for c in text if '\u0600' <= c <= '\u06FF')
    return count / max(len(text), 1) > 0.3
```

### Tool Call JSON (LLM must output this exact format)

```json
{"type": "tool_call", "tool": "tool_name", "args": {"param": "value"}}
```

### Tool Result JSON (returned to LLM after execution)

```json
{"type": "tool_result", "tool": "tool_name", "success": true, "data": {}, "error": null, "duration_ms": 312}
```

### VRAM Swap Rule

```python
# Before loading any model:
current = get_active_model()
if current != new_model:
    unload_current_model()   # wait for VRAM to free
    swap_to(new_model)       # then load new
# Never load two models simultaneously
```

### Path Convention (all relative to project root)

```
data/                  ← all runtime data (gitignored)
data/chroma/           ← ChromaDB vector store
data/sessions/         ← browser sessions (encrypted, gitignored)
data/google_token.json ← OAuth token (gitignored)
data/downloads/        ← files downloaded by browser tool
data/screenshots/      ← screenshots
data/generated/        ← SD-generated images
data/cli_history.txt   ← CLI input history
data/user_profile.json ← user preferences
data/jarvis.db         ← SQLite database
logs/                  ← log files (gitignored)
config/                ← all YAML config (NOT gitignored)
config/schemas/        ← JSON Schemas for tools
```

### Cross-Platform Command Map

| Action | Windows | Linux | macOS |
|--------|---------|-------|-------|
| Kill process | `taskkill /IM name.exe /F` | `pkill name` | `kill -9 $(pgrep name)` |
| Open app | `ShellExecute(name)` | `subprocess([name])` | `open -a name` |
| Notifications | `winotify` | `notify-send` | `osascript` |
| Volume | `pycaw` | `pactl/amixer` | `osascript` |
| Auto-start | Registry Run key | `~/.config/autostart/` | `~/Library/LaunchAgents/` |

---

*Version 1.0.0-alpha — Complete Production Blueprint*
*Build Phase 0 first. Verify end state before proceeding. No phase skipping.*
