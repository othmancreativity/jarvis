# 📋 JARVIS — Execution Plan

> **spec_version:** `v3.0` | **project_version:** `3.0.0` | **structure_version:** `1`

---

## 📑 Table of Contents

### Changelog & Status

- [Project Status](#-project-status)
- [Canonical Directory Structure](#-canonical-directory-structure-v30)
- [Status Legend](#-status-legend)
- [Phase Progress Summary](#-phase-progress-summary)

### Phases

- [Phase 0](#-phase-0--first-working-system-vertical-slice-contract-first) — First Working System
- [Phase 1](#-phase-1--foundation--observability) — Foundation + Observability
- [Phase 2](#-phase-2--execution-contract) — Execution Contract
- [Phase 3](#-phase-3--model-manager--vram) — Model Manager + VRAM
- [Phase 4](#-phase-4--runtime-state-machine) — Runtime State Machine
- [Phase 5](#-phase-5--decision-system) — Decision System
- [Phase 6](#-phase-6--sandbox--safety) — Sandbox + Safety
- [Phase 7](#-phase-7--memory-engine) — Memory Engine
- [Phase 8](#-phase-8--capability-system) — Capability System
- [Phase 9](#-phase-9--system-control-capabilities) — System Control Capabilities
- [Phase 10](#-phase-10--prompt-builder) — Prompt Builder
- [Phase 11](#-phase-11--execution-hardening) — Execution Hardening
- [Phase 12](#-phase-12--cli-interface) — CLI Interface
- [Phase 13](#-phase-13--web-automation--browser) — Web Automation & Browser
- [Phase 14](#-phase-14--google-apis) — Google APIs
- [Phase 14.5](#-phase-145--telegram-integration) — Telegram Integration
- [Phase 15](#-phase-15--web-ui) — Web UI
- [Phase 16](#-phase-16--voice-pipeline) — Voice Pipeline
- [Phase 17](#-phase-17--vision--image) — Vision + Image
- [Phase 18](#-phase-18--qa--production) — QA + Production

### Summary

- [Summary](#-summary)

---

## Project Status

```yaml
project:
  name: JARVIS
  version: "3.0.0"
  spec_version: "v3.0"
  structure_version: "1"
  last_updated: "2026-05-02"
  current_phase: 1
  overall_progress_percent: 6.5
  risk_level: "medium"
  hardware_profile:
    gpu: "RTX 3050 6GB VRAM"
    ram: "16 GB"
    cpu: "Intel Core i5 12th Gen"
  current_blocker: "none"
```

---

### Phase Progress

| Phase | Title                                 |  P  | Status | Progress    | Tasks | Blocker    | Next Action |
| :---: | :------------------------------------ | :-: | :----- | :---------- | :---- | :--------- | :---------- |
|   0   | First Working System (Vertical Slice) | P0  | done   | ░░░░░░░░ 0% | 0/5   | —          | —           |
|   1   | Foundation + Observability            | P0  | ▒ todo | ░░░░░░░░ 0% | 0/13  | Phase 0    | TASK 1.0    |
|   2   | Execution Contract                    | P0  | ▒ todo | ░░░░░░░░ 0% | 0/10  | Phase 1    | TASK 2.0    |
|   3   | Model Manager + VRAM                  | P0  | ▒ todo | ░░░░░░░░ 0% | 0/5   | Phase 2    | TASK 3.1    |
|   4   | Runtime State Machine                 | P0  | ▒ todo | ░░░░░░░░ 0% | 0/8   | Phase 3    | TASK 4.1    |
|   5   | Decision System                       | P1  | ▒ todo | ░░░░░░░░ 0% | 0/7   | Phase 4    | TASK 5.1    |
|   6   | Sandbox + Safety                      | P0  | ▒ todo | ░░░░░░░░ 0% | 0/7   | Phase 5    | TASK 6.1    |
|   7   | Memory Engine                         | P1  | ▒ todo | ░░░░░░░░ 0% | 0/6   | Phase 6    | TASK 7.1    |
|   8   | Capability System                     | P1  | ▒ todo | ░░░░░░░░ 0% | 0/6   | Phase 7    | TASK 8.1    |
|   9   | System Control Capabilities           | P1  | ▒ todo | ░░░░░░░░ 0% | 0/8   | Phase 8    | TASK 9.1    |
|  10   | Prompt Builder                        | P1  | ▒ todo | ░░░░░░░░ 0% | 0/5   | Phase 9    | TASK 10.1   |
|  11   | Execution Hardening                   | P0  | ▒ todo | ░░░░░░░░ 0% | 0/6   | Phase 10   | TASK 11.1   |
|  12   | CLI Interface                         | P2  | ▒ todo | ░░░░░░░░ 0% | 0/3   | Phase 11   | TASK 12.1   |
|  13   | Web Automation & Browser              | P2  | ▒ todo | ░░░░░░░░ 0% | 0/3   | Phase 12   | TASK 13.1   |
|  14   | Google APIs                           | P2  | ▒ todo | ░░░░░░░░ 0% | 0/4   | Phase 13   | TASK 14.1   |
| 14.5  | Telegram Integration                  | P2  | ▒ todo | ░░░░░░░░ 0% | 0/3   | Phase 14   | TASK 14.5.1 |
|  15   | Web UI                                | P2  | ▒ todo | ░░░░░░░░ 0% | 0/3   | Phase 14.5 | TASK 15.1   |
|  16   | Voice Pipeline                        | P3  | ▒ todo | ░░░░░░░░ 0% | 0/4   | Phase 15   | TASK 16.1   |
|  17   | Vision + Image                        | P3  | ▒ todo | ░░░░░░░░ 0% | 0/2   | Phase 16   | TASK 17.1   |
|  18   | QA + Production                       | P0  | ▒ todo | ░░░░░░░░ 0% | 0/6   | Phase 17   | TASK 18.1   |

---

## ✅ Phase 0 — First Working System (Vertical Slice, Contract-First)

```yaml
phase_id: 0
title: "First Working System (Vertical Slice)"
priority: "P0"
status: "done"
progress_percent: 100
total_tasks: 5
validation_status: "passed — contracts implemented, vertical slice working"
last_updated: "2026-05-02"
```

> Phase 0 rebuild complete. All v3.0 contract requirements met:
>
> - ✅ DecisionOutput with score_breakdown and candidate_list
> - ✅ LLMOutput contract implemented
> - ✅ ToolResult contract implemented
> - ✅ InputPacket and FinalResponse contracts
> - ✅ CapabilityExecutor replaces direct open_app() calls
> - ✅ Observe → Decide → Think → Act → Evaluate flow enforced in RuntimeLoop
> - ✅ Vertical slice demo working (app/jarvis_slice.py)
> - ✅ 17 contract tests passing

---

## 🔧 Phase 1 — Foundation + Observability

```yaml
phase_id: 1
title: "Foundation + Observability"
priority: "P0"
status: "not_started"
total_tasks: 13
blocker: "Phase 0 complete"
next_action: "TASK 1.0"
```

### Objective

Establish project packaging, configuration, logging, observability, and shared infrastructure that all subsequent phases depend on. Every task in this phase is a hard prerequisite for Phases 2+.

---

### TASK 1.0 — Project Scaffolding

Location:

- `pyproject.toml`
- `requirements.txt`
- All `__init__.py` stubs
- `app/__init__.py`
- `tests/__init__.py`

Purpose:

- Create installable Python package, declare all dependencies, and establish directory skeleton.

Steps:

1. Create `pyproject.toml` with `[project]` table: name=`jarvis`, version=`3.0.0`, requires-python=`>=3.10`.
2. Declare dependencies in `pyproject.toml` `[project.dependencies]`:
   ```
   ollama>=0.2.0
   pydantic>=2.0.0
   pyyaml>=6.0
   loguru>=0.7.0
   python-dotenv>=1.0.0
   psutil>=5.9.0
   pyperclip>=1.8.0
   pillow>=10.0.0
   colorama>=0.4.6
   fastapi>=0.110.0
   uvicorn>=0.27.0
   websockets>=12.0
   httpx>=0.27.0
   playwright>=1.42.0
   requests>=2.31.0
   beautifulsoup4>=4.12.0
   speechrecognition>=3.10.0
   google-auth>=2.28.0
   google-api-python-client>=2.120.0
   python-telegram-bot>=21.0
   pytest>=8.0.0
   pytest-asyncio>=0.23.0
   ```
3. Declare optional dependencies: `[project.optional-dependencies]` sections for `vision`, `voice`.
4. Add `[tool.pytest.ini_options]` with `testpaths = ["tests"]`, `asyncio_mode = "auto"`.
5. Create `requirements.txt` as pinned export of above (for environments without pip editable install).
6. Create every directory listed in the canonical structure above with a `.gitkeep` placeholder if empty.
7. Create `app/__init__.py` (empty, marks `app/` as package).
8. Create `tests/__init__.py` (empty).
9. Install package in development mode: `pip install -e ".[vision,voice]"`.
10. Verify all top-level imports resolve: `python -c "import src"`.

Success case:

- `pip install -e .` exits 0.
- `python -c "import src; import app"` succeeds.
- All directories exist per canonical structure.

Failure case:

- Missing system dependency (e.g., tesseract) → document in README `Requirements` section, do NOT fail silently.

Validation:

```bash
pip install -e .
python -c "import src; import app; print('packages OK')"
find . -name "__init__.py" | sort
```

Artifacts: `pyproject.toml`, `requirements.txt`, all `__init__.py` files, full directory tree

---

### TASK 1.1 — Settings YAML and Pydantic Loader

Location:

- `config/settings.example.yaml`
- `config/settings.yaml`
- `src/core/config.py`

Purpose:

- Create validated configuration system. `settings.yaml` is the live file; `settings.example.yaml` is the committed template.

Steps:

1. Create `config/settings.example.yaml` with the following top-level keys and defaults:
   ```yaml
   models:
     default: "gemma3:4b"
     timeout_s: 60
     fallback_chain: ["qwen2.5:7b", "gemma3:4b"]
   paths:
     allowed_roots: ["~/Documents", "~/Downloads", "~/Desktop"]
     memory_db: "data/memory.db"
     audit_db: "data/audit.db"
     logs_dir: "logs/"
   execution:
     mode: "BALANCED"           # SAFE | BALANCED | UNRESTRICTED
     max_iterations: 5
     max_tool_calls: 3
     max_tool_depth: 3
     max_decision_retries: 3
     max_model_retries: 2
     global_retry_budget: 8
     tool_timeout_s: 30
     model_timeout_s: 120
     step_timeout_s: 60
      total_turn_timeout_s: 300
      safety:
        blocked_apps: ["format", "mkfs", "fdisk", "dd", "diskpart"]
      blocked_paths: ["/etc", "/sys", "/proc", "/boot", "C:\\Windows\\System32", "C:\\Windows\\SysWOW64"]
      blocked_commands:
        # Unix destructive
        - "rm -rf"
        - "rm -r"
        - "shred"
        - "wipe"
        - "dd"
        - "mkfs"
        - "fdisk"
        - "parted"
        - "mkswap"
        # Windows destructive (cmd + powershell)
        - "format"
        - "diskpart"
        - "bcdedit"
        - "reg delete"
        - "Remove-Item -Recurse -Force"
        - "Clear-Disk"
        - "Format-Volume"
        - "Disable-NetAdapter"
      allowed_commands: []
   observability:
     log_level: "INFO"
     metrics_enabled: true
     trace_enabled: true
     replay_enabled: true
     log_rotation_mb: 100
     log_rotation_count: 5
   ```
2. Copy `settings.example.yaml` → `config/settings.yaml` (gitignored; user customizes this).
3. Add `config/settings.yaml` to `.gitignore`.
4. Create `src/core/config.py`.
5. Define nested Pydantic `BaseModel` hierarchy matching every YAML key above.
6. Define top-level `Settings` model.
7. Implement `load_config(path: str = "config/settings.yaml") -> Settings`.
8. Inside `load_config`: open YAML → parse → construct Settings → validate (Pydantic raises `ValidationError` on invalid values).
9. Environment variable override with strict precedence: CLI > ENV > .env > YAML.
   - Load order: (1) YAML defaults, (2) `.env` via `load_dotenv(override=False)`,
     (3) shell ENV via `SettingsConfigDict(env_prefix='JARVIS_', env_nested_delimiter='__')`,
     (4) CLI args passed to `load_config(cli_overrides={...})` which take final precedence.
   - `override=False` ensures `.env` does NOT overwrite existing shell env vars.
   - CLI args always win — passed as explicit dict to `load_config()`.
10. Expand `~` in all path fields using `Path.expanduser()` after loading.
11. `load_config` is a module-level singleton: call once at boot, subsequent calls return cached instance.

Success case:

- `load_config()` returns `Settings` with `models.default == "gemma3:4b"`.
- `JARVIS_EXECUTION__MODE=SAFE python -c "from src.core.config import load_config; s=load_config(); assert s.execution.mode=='SAFE'"` passes.

Failure case:

- `settings.yaml` missing → `FileNotFoundError` with message `"config/settings.yaml not found. Copy settings.example.yaml to settings.yaml and configure."`.
- Invalid `execution.mode` value → Pydantic `ValidationError` with field name and allowed values.

Edge cases:

- `allowed_roots` containing `~` → expanded at load time.
- `log_level: DEBUG` → accepted without error.

Validation:

```bash
python -c "
from src.core.config import load_config
s = load_config('config/settings.yaml')
assert s.models.default is not None
assert s.execution.mode in ('SAFE', 'BALANCED', 'UNRESTRICTED')
assert len(s.execution.fallback_chain) >= 1
print(f'Config OK: mode={s.execution.mode}, default_model={s.models.default}')
"
```

Artifacts: `config/settings.example.yaml`, `config/settings.yaml`, `src/core/config.py`

---

### TASK 1.2 — Structured Logging Setup

Location:

- `src/core/logging_setup.py`

Purpose:

- Implement structured logging with mandatory fields for all log events. Used by every other module via `from loguru import logger`.

Steps:

1. Create `src/core/logging_setup.py`.
2. Define `setup_logging(level: str, logs_dir: str) -> None`.
3. Remove Loguru's default handler: `logger.remove()`.
4. Add console sink: `logger.add(sys.stderr, level=level, format="{time:ISO8601} | {level:<8} | {message}")`.
5. Add structured file sink with rotation:
   ```python
   logger.add(
       f"{logs_dir}/jarvis_{{time}}.log",
       level=level,
       rotation="100 MB",
       retention=5,
       serialize=True,   # JSON output
   )
   ```
6. Define a `log_event(event: str, phase: str, session_id: str = "", turn_id: int = 0, trace_id: str = "", data: dict = None) -> None` helper that calls `logger.bind(event=event, session_id=session_id, turn_id=turn_id, phase=phase, trace_id=trace_id, data=data or {}).info(event)`.
7. Create `logs/` directory if it does not exist.
8. Call `setup_logging` exactly once from `app/main.py` boot sequence. Subsequent modules call `from loguru import logger` directly.
9. `setup_logging` is idempotent (safe to call multiple times).

Success case:

- JSON log file contains keys: `text`, `record.level.name`, `record.extra.event`, `record.extra.session_id`, `record.extra.turn_id`, `record.extra.phase`, `record.extra.trace_id`, `record.extra.data`.

Failure case:

- `logs/` not writable → falls back to stderr only, logs a warning.

Validation:

```bash
python -c "
import json, tempfile, os
from src.core.logging_setup import setup_logging, log_event
with tempfile.TemporaryDirectory() as d:
    setup_logging('DEBUG', d)
    log_event('test_event', phase='test', session_id='s1', turn_id=1, trace_id='t1', data={'k': 'v'})
    log_files = [f for f in os.listdir(d) if f.endswith('.log')]
    assert len(log_files) > 0, 'No log file created'
    line = open(os.path.join(d, log_files[0])).readline()
    parsed = json.loads(line)
    assert parsed['record']['extra']['event'] == 'test_event'
    print('Logging OK')
"
```

Artifact: `src/core/logging_setup.py`

---

### TASK 1.3 — Package `__init__.py` Public API

Location:

- `src/__init__.py`
- All sub-package `__init__.py` files

Purpose:

- Define public imports so that internal refactoring does not break callers of the public API.

Steps:

1. `src/__init__.py`: `__version__ = "3.0.0"`.
2. `src/core/__init__.py`: export `load_config`, `setup_logging`.
3. `src/capabilities/__init__.py`: export `BaseCapability`, `CapabilityRegistry`, `CapabilityExecutor`, `ToolResult`.
4. `src/memory/__init__.py`: export `MemoryDB`, `ContextRetriever`.
5. `src/models/__init__.py`: export `ModelManager`, `VRAMMonitor`.
6. `src/interfaces/__init__.py`: empty (interfaces are not imported, they are started).
7. `src/services/__init__.py`: empty.
8. All leaf package `__init__.py` files: empty unless there is a clear public export.

Success case:

- `from src import __version__` returns "3.0.0".
- `from src.core import load_config` resolves.

Validation:

```bash
python -c "
from src import __version__
assert __version__ == '3.0.0'
from src.core import load_config
print('Public API OK')
"
```

---

### TASK 1.4 — Model Capability Profiles

Location:

- `src/models/profiles.py`

Purpose:

- Define static model profiles consumed by the Decision scorer (Phase 5). Must be the single source of truth for model metadata.

Steps:

1. Create `src/models/profiles.py`.
2. Define `ModelProfile` as a frozen `dataclass`:
   ```python
   @dataclass(frozen=True)
   class ModelProfile:
       name: str
       vram_required_mb: int
       capabilities: list[str]       # ["reasoning", "code", "vision", "multilingual"]
       latency_tier: str             # "fast" | "medium" | "slow"
       reasoning_tier: str           # "low" | "medium" | "high"
       context_window_tokens: int
       supports_arabic: bool
   ```
3. Define `PROFILES: dict[str, ModelProfile]` with entries for:
   - `gemma3:4b`: vram=3200, capabilities=["reasoning","multilingual"], latency="fast", reasoning="medium", ctx=8192, arabic=True
   - `qwen3:8b`: vram=5000, capabilities=["reasoning","multilingual"], latency="medium", reasoning="high", ctx=32768, arabic=True
   - `qwen2.5-coder:7b`: vram=4800, capabilities=["code","reasoning"], latency="medium", reasoning="medium", ctx=16384, arabic=False
   - `llava:7b`: vram=4500, capabilities=["vision","reasoning"], latency="slow", reasoning="medium", ctx=4096, arabic=False
   - `qwen2.5:7b`: vram=4600, capabilities=["reasoning","multilingual"], latency="medium", reasoning="high", ctx=32768, arabic=True
4. Implement `get_profile(model_name: str) -> ModelProfile | None`.
5. Implement `list_profiles() -> list[ModelProfile]`.
6. Profiles are sourced from code here; `config/models.yaml` (TASK 1.5) provides scoring weights only — no duplication of profile data.

Success case:

- `get_profile("gemma3:4b").vram_required_mb == 3200`.
- `get_profile("unknown")` returns None.

Validation:

```bash
python -c "
from src.models.profiles import get_profile, list_profiles
p = get_profile('gemma3:4b')
assert p.vram_required_mb == 3200
assert p.latency_tier == 'fast'
assert get_profile('nonexistent') is None
print(f'{len(list_profiles())} profiles loaded')
"
```

Artifact: `src/models/profiles.py`

---

### TASK 1.5 — Model Scoring Weights YAML

Location:

- `config/models.yaml`

Purpose:

- Define scoring weights and fallback chain used by the Decision scorer. Separates tunable weights from model metadata.

Steps:

1. Create `config/models.yaml`:
   ```yaml
   weights:
     fit_complexity: 0.30 # model reasoning_tier vs input complexity
     fit_mode: 0.20 # latency_tier vs requested mode
     cost_penalty: 0.20 # vram_required_mb (lower = higher score)
     quality_need: 0.20 # reasoning_tier absolute quality
     memory_bias: 0.10 # recency of successful use
   variability_margin: 0.05 # ±0.05 for tie-break randomization (off by default)
   fallback:
     tier_1: "qwen2.5:7b"
     tier_2: "gemma3:4b"
   ```
2. Add a comment header: `# Scoring weights must sum to 1.0. Validated at config load time.`
3. In `src/core/config.py` TASK 1.1, add `models_config_path: str = "config/models.yaml"` and load + validate that weights sum to 1.0 (within floating-point tolerance of 0.001).

Success case:

- YAML loads, weights sum to 1.0.
- `fit_complexity + fit_mode + cost_penalty + quality_need + memory_bias == 1.0`.

Failure case:

- Weights sum ≠ 1.0 → `ValidationError` at config load.

Validation:

```bash
python -c "
import yaml
m = yaml.safe_load(open('config/models.yaml'))
w = m['weights']
total = sum(w.values())
assert abs(total - 1.0) < 0.001, f'Weights sum to {total}'
assert m['fallback']['tier_1'] and m['fallback']['tier_2']
print('models.yaml OK')
"
```

Artifact: `config/models.yaml`

---

### TASK 1.6 — Environment Variables

Location:

- `.env.example`
- `.env`

Purpose:

- Declare all secret variables. Secrets never go in YAML files.

Steps:

1. Create `.env.example`:

   ```
   # Telegram
   TELEGRAM_BOT_TOKEN=your_token_here

   # Google OAuth
   GOOGLE_CLIENT_ID=your_client_id
   GOOGLE_CLIENT_SECRET=your_client_secret
   GOOGLE_REDIRECT_URI=http://localhost:8080

   # Ollama (override if non-default)
   OLLAMA_BASE_URL=http://localhost:11434

   # Safety override (use with caution)
   JARVIS_EXECUTION__MODE=BALANCED
   ```

2. Copy `.env.example` → `.env` and add `.env` to `.gitignore`.
3. In `src/core/config.py` `load_config()`: call `load_dotenv(override=False)` before constructing `Settings` so YAML values are not silently overwritten by stale `.env` entries. Use `override=False` — explicit `JARVIS_*` env vars win, `.env` does not override shell env.
4. Document each variable's purpose inline.

Validation:

```bash
python -c "
from dotenv import load_dotenv
import os
load_dotenv('.env.example')
print('dotenv OK:', os.environ.get('OLLAMA_BASE_URL', 'not set'))
"
```

---

### TASK 1.7 — User Profile

Location:

- `src/memory/user_profile.py`

Purpose:

- Persistent user profile. Used by `InputPacket` (TASK 2.1) — must exist before Phase 2.

Steps:

1. Create `src/memory/user_profile.py`.
2. Define `UserProfile` dataclass:
   ```python
   @dataclass
   class UserProfile:
       user_id: str
       name: str = "User"
       language: str = "en"           # "en" | "ar"
       execution_mode: str = "BALANCED"
       preferences: dict = field(default_factory=dict)
       created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
       updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
   ```
3. Define `PROFILE_STORE_PATH = Path("data/profiles/")`.
4. Implement `load_profile(user_id: str) -> UserProfile`:
   - Look for `data/profiles/{user_id}.json`.
   - If missing → return `UserProfile(user_id=user_id)` (default).
   - If JSON parse fails → log warning, return default.
5. Implement `save_profile(profile: UserProfile) -> None`:
   - Create `data/profiles/` if absent.
   - Write `profile.__dict__` as JSON.
   - Update `updated_at` before writing.
6. Implement `update_mode(user_id: str, mode: str) -> UserProfile`: load → mutate → save → return.

Success case:

- `save_profile(p)` → `load_profile(p.user_id)` returns same data.
- `load_profile("nonexistent")` returns default profile without error.

Failure case:

- Corrupted JSON → returns default, logs `WARNING: corrupted profile for {user_id}, using defaults`.

Validation:

```bash
python -c "
from src.memory.user_profile import load_profile, save_profile, UserProfile
p = UserProfile(user_id='test_u1', name='Test', language='ar')
save_profile(p)
loaded = load_profile('test_u1')
assert loaded.language == 'ar'
assert loaded.name == 'Test'
print('UserProfile OK')
"
```

Artifact: `src/memory/user_profile.py`

---

### TASK 1.8 — Capabilities Manifest YAML

Location:

- `config/capabilities.yaml`

Purpose:

- Registry source-of-truth for all capabilities. The `CapabilityRegistry` (Phase 8) loads from this file.

Steps:

1. Create `config/capabilities.yaml`:

   ```yaml
   capabilities:
     - name: open_app
       domain: system
       risk_level: medium
       description: "Launch an application by name"
       module_path: "src.capabilities.system.apps.AppLauncher"
       input_schema:
         name: { type: string, required: true }
       platforms: [windows, linux, macos]

     - name: system_info
       domain: system
       risk_level: low
       description: "Return system hardware and OS information"
       module_path: "src.capabilities.system.sysinfo.SystemInfoCapability"
       input_schema:
         info_type:
           {
             type: string,
             required: false,
             default: all,
             enum: [all, cpu, ram, gpu, os],
           }
       platforms: [windows, linux, macos]

     - name: clipboard
       domain: system
       risk_level: low
       description: "Read or write system clipboard"
       module_path: "src.capabilities.system.clipboard.ClipboardCapability"
       input_schema:
         action: { type: string, required: true, enum: [read, write] }
         content: { type: string, required: false }
       platforms: [windows, linux, macos]

     - name: notify
       domain: notify
       risk_level: low
       description: "Send desktop notification"
       module_path: "src.capabilities.notify.toasts.NotificationCapability"
       input_schema:
         title: { type: string, required: true }
         message: { type: string, required: true }
         duration: { type: integer, required: false, default: 5 }
       platforms: [windows, linux, macos]

     - name: screenshot
       domain: screen
       risk_level: low
       description: "Capture screen, optionally with OCR"
       module_path: "src.capabilities.screen.capture.ScreenshotCapability"
       input_schema:
         ocr: { type: boolean, required: false, default: false }
         region: { type: object, required: false }
       platforms: [windows, linux, macos]

     - name: file_ops
       domain: files
       risk_level: medium
       description: "Read, write, list, delete, move, copy files"
       module_path: "src.capabilities.files.file_ops.FileOpsCapability"
       input_schema:
         action:
           {
             type: string,
             required: true,
             enum: [read, write, list, delete, move, copy],
           }
         path: { type: string, required: true }
         content: { type: string, required: false }
         destination: { type: string, required: false }
       platforms: [windows, linux, macos]

     - name: code_exec
       domain: coder
       risk_level: high
       description: "Execute code in sandboxed subprocess"
       module_path: "src.capabilities.coder.executor.CodeExecutorCapability"
       input_schema:
         language:
           { type: string, required: true, enum: [python, javascript, bash] }
         code: { type: string, required: true }
       platforms: [windows, linux, macos]

     - name: web_search
       domain: search
       risk_level: low
       description: "Web search and result extraction"
       module_path: "src.capabilities.search.web_search.WebSearchCapability"
       input_schema:
         query: { type: string, required: true }
         count: { type: integer, required: false, default: 5 }
       platforms: [windows, linux, macos]

     - name: browser
       domain: web
       risk_level: medium
       description: "Browser automation via Playwright"
       module_path: "src.capabilities.web.browser.BrowserCapability"
       input_schema:
         action:
           {
             type: string,
             required: true,
             enum: [navigate, click, type, screenshot, extract_text],
           }
         url: { type: string, required: false }
         selector: { type: string, required: false }
         text: { type: string, required: false }
       platforms: [windows, linux, macos]

     - name: stt
       domain: voice
       risk_level: low
       description: "Speech-to-text transcription"
       module_path: "src.capabilities.voice.stt.STTCapability"
       input_schema:
         audio_path: { type: string, required: false }
       platforms: [windows, linux, macos]

     - name: tts
       domain: voice
       risk_level: low
       description: "Text-to-speech synthesis"
       module_path: "src.capabilities.voice.tts.TTSCapability"
       input_schema:
         text: { type: string, required: true }
         voice: { type: string, required: false }
       platforms: [windows, linux, macos]

     - name: vision_analyze
       domain: vision
       risk_level: low
       description: "Analyze image using vision model"
       module_path: "src.capabilities.vision.vision.VisionCapability"
       input_schema:
         image_path: { type: string, required: true }
         prompt:
           { type: string, required: false, default: "describe this image" }
       platforms: [windows, linux, macos]

     - name: image_gen
       domain: vision
       risk_level: low
       description: "Generate image from text prompt"
       module_path: "src.capabilities.vision.image_gen.ImageGenCapability"
       input_schema:
         prompt: { type: string, required: true }
         size: { type: string, required: false, default: "512x512" }
       platforms: [windows, linux, macos]
   ```

2. Validate on load: each entry has `name`, `risk_level` in `[low, medium, high]`, `module_path`, `input_schema`.

Validation:

```bash
python -c "
import yaml
caps = yaml.safe_load(open('config/capabilities.yaml'))['capabilities']
assert all('risk_level' in c for c in caps)
assert all(c['risk_level'] in ('low','medium','high') for c in caps)
print(f'{len(caps)} capabilities defined')
"
```

Artifact: `config/capabilities.yaml`

---

### TASK 1.9 — Observability: Metrics Collector

Location:

- `src/core/observability/metrics.py`

Purpose:

- Thread-safe metrics collection for latency, error rate, model usage.

Steps:

1. Create `src/core/observability/metrics.py`.
2. Define `MetricsCollector` as a thread-safe singleton using a `threading.Lock`.
3. Internal state:
   ```python
   latency: dict[str, list[float]]   # phase → [ms values]
   errors: dict[str, dict[str, int]] # phase → {error_type → count}
   model_usage: dict[str, dict]      # model → {calls, successes, failures}
   turn_count: int
   ```
4. Implement `record_latency(phase: str, ms: float) -> None`.
5. Implement `record_error(phase: str, error_type: str) -> None`.
6. Implement `record_model_usage(model_name: str, success: bool) -> None`.
7. Implement `increment_turn() -> int` → increments and returns `turn_count`.
8. Implement `get_summary() -> dict`:
   ```python
   {
     "latency": {"decision": {"p50": ..., "p95": ..., "count": ...}, ...},
     "errors": {"model": {"timeout": 3}, ...},
     "model_usage": {"gemma3:4b": {"calls": 10, "success_rate": 0.9}},
     "turn_count": 42
   }
   ```
9. Implement `reset() -> None` (for tests).
10. Use `statistics.quantiles` for p50/p95 with `n=100`.

Success case:

- `record_latency("decision", 50)` then `get_summary()["latency"]["decision"]["p50"] > 0`.

Validation:

```bash
python -c "
from src.core.observability.metrics import MetricsCollector
mc = MetricsCollector()
mc.record_latency('decision', 50)
mc.record_latency('decision', 100)
mc.record_error('model', 'timeout')
mc.record_model_usage('gemma3:4b', True)
s = mc.get_summary()
assert 'decision' in s['latency']
assert s['errors']['model']['timeout'] == 1
assert s['model_usage']['gemma3:4b']['calls'] == 1
print(s)
"
```

Artifact: `src/core/observability/metrics.py`

---

### TASK 1.10 — `app/main.py` Entry Point

Location:

- `app/main.py`

Purpose:

- Canonical application entry point. Boot sequence with argument parsing and graceful shutdown.

Steps:

1. Create `app/main.py`.
2. Define `boot_sequence() -> None`:
   a. Load config via `load_config()`.
   b. Call `setup_logging(level=config.observability.log_level, logs_dir=config.paths.logs_dir)`.
   c. Initialize `MetricsCollector` singleton.
   d. Verify Ollama reachable: `GET http://localhost:11434/api/tags` → if 404/connection error, print WARNING and continue (core LLM will fail gracefully at call time).
   e. Ensure `data/` directories exist: `data/profiles/`, `data/memory.db` parent.
   f. Print `"JARVIS ready"` to stdout.
3. Define `main() -> None`:
   a. `argparse` arguments: `--interface {cli,web}` (default: cli), `--debug` (flag), `--trace` (flag), `--mode {SAFE,BALANCED,UNRESTRICTED}`.
   b. If `--debug`: set log level to DEBUG.
   c. If `--trace`: enable per-turn trace replay logging.
   d. If `--mode`: override `config.execution.mode` before starting interface.
   e. Call `boot_sequence()`.
   f. Dispatch to `CLIChat().start()` or `WebApp().start()` based on `--interface`.
4. Register `signal.SIGINT` and `signal.SIGTERM` handlers → set a `_shutdown` flag → interfaces check this flag in their loop → clean exit without traceback.
5. Wrap `main()` in `try/except KeyboardInterrupt: sys.exit(0)`.

Success case:

- `python app/main.py --interface cli` prints `JARVIS ready` and enters CLI loop.
- Ctrl+C exits with code 0, no traceback.
- `python app/main.py --mode SAFE` overrides mode.

Failure case:

- `config/settings.yaml` missing → prints `ERROR: config/settings.yaml not found. Copy settings.example.yaml.` and exits with code 1 (no crash).
- Ollama unreachable → prints `WARNING: Ollama not reachable at localhost:11434. LLM features will fail.` and continues.

Validation:

```bash
python app/main.py --interface cli
# Manually verify: "JARVIS ready" appears, Ctrl+C exits cleanly
python app/main.py --help
# Verify all arguments shown
```

Artifact: `app/main.py`

---

### TASK 1.11 — EventBus

Location:

- `src/core/observability/event_bus.py`

Purpose:

- In-process publish/subscribe bus for decoupled cross-layer event notification. Required by TASK 4.2 (state transitions) and TASK 4.7 (observability hooks). Must not be used for control flow — events are notifications only.

Steps:

1. Create `src/core/observability/event_bus.py`.
2. Define `EventBus` as a thread-safe singleton:

   ```python
   class EventBus:
       _instance = None
       _lock = threading.Lock()

       def __new__(cls):
           with cls._lock:
               if cls._instance is None:
                   cls._instance = super().__new__(cls)
                   cls._instance._subscribers = {}
                   cls._instance._event_lock = threading.Lock()
           return cls._instance
   ```

3. Implement `subscribe(event_type: str, callback: Callable) -> None`:
   - Adds callback to `_subscribers[event_type]` list.
   - `callback` signature: `callback(event: dict) -> None`.
4. Implement `publish(event_type: str, data: dict) -> None`:
   - Retrieves subscriber list for `event_type`.
   - Calls each callback with `{"type": event_type, "data": data, "timestamp": datetime.utcnow().isoformat()}`.
   - Exceptions in callbacks are caught and logged — they must NEVER propagate to publisher.
5. Implement `unsubscribe(event_type: str, callback: Callable) -> None`.
6. Implement `clear(event_type: str | None = None) -> None` (for tests).
7. Define event type constants as module-level strings:
   ```python
   EVT_STATE_TRANSITION = "runtime.state"
   EVT_MODEL_SWAP = "models.swap"
   EVT_TOOL_EXECUTED = "capabilities.executed"
   EVT_TURN_COMPLETE = "runtime.turn_complete"
   EVT_SAFETY_BLOCK = "safety.blocked"
   EVT_DEGRADATION = "runtime.degraded"
   ```

Success case:

- `subscribe` → `publish` → callback called with correct data.
- Callback exception does NOT raise to publisher.
- Two subscribers on same event both receive event.

Failure case:

- `publish` with no subscribers → no-op, no error.

Validation:

```bash
python -c "
from src.core.observability.event_bus import EventBus, EVT_STATE_TRANSITION
bus = EventBus()
received = []
bus.subscribe(EVT_STATE_TRANSITION, lambda e: received.append(e))
bus.publish(EVT_STATE_TRANSITION, {'from': 'IDLE', 'to': 'DECIDING'})
assert len(received) == 1
assert received[0]['data']['to'] == 'DECIDING'
# Test exception isolation
bus.subscribe(EVT_STATE_TRANSITION, lambda e: 1/0)  # bad callback
bus.publish(EVT_STATE_TRANSITION, {'from': 'DECIDING', 'to': 'EXECUTING_MODEL'})
assert len(received) == 2  # publisher not blocked
print('EventBus OK')
"
```

Artifact: `src/core/observability/event_bus.py`

---

### TASK 1.12 — Custom Exceptions

Location:

- `src/core/exceptions.py`

Purpose:

- Centralized exception hierarchy. All custom errors inherit from `JarvisError`. Prevents catching wrong exceptions.

Steps:

1. Create `src/core/exceptions.py`.
2. Define hierarchy:

   ```python
   class JarvisError(Exception):
       """Base for all Jarvis exceptions."""

   # Runtime
   class InvalidTransitionError(JarvisError):
       """State machine received an invalid transition."""

   class RetryBudgetExhaustedError(JarvisError):
       """Global retry budget consumed."""

   class TurnTimeoutError(JarvisError):
       """Total turn time limit exceeded."""

   # Models
   class ModelCallError(JarvisError):
       """LLM or model call failed."""

   class ModelUnavailableError(ModelCallError):
       """Requested model is not loaded or not available."""

   class VRAMInsufficientError(ModelCallError):
       """VRAM insufficient to load requested model."""

   # Capabilities
   class CapabilityNotFoundError(JarvisError):
       """Capability name not in registry."""

   class CapabilityValidationError(JarvisError):
       """Capability args failed schema validation."""

   class CapabilityTimeoutError(JarvisError):
       """Capability execution timed out."""

   # Safety
   class PermissionDeniedError(JarvisError):
       """Action blocked by safety or mode enforcer."""

   class PathTraversalError(PermissionDeniedError):
       """File path outside allowed roots."""

   # Decision
   class ParseError(JarvisError):
       """Failed to parse LLM output to expected structure."""

   class ClassifierError(JarvisError):
       """Classifier could not produce a valid decision."""
   ```

3. Each exception accepts an optional `detail: str` kwarg stored as `self.detail`.

Success case:

- All exceptions importable.
- `isinstance(VRAMInsufficientError(), JarvisError)` is True.
- `isinstance(VRAMInsufficientError(), ModelCallError)` is True.

Validation:

```bash
python -c "
from src.core.exceptions import (
    JarvisError, InvalidTransitionError, ModelCallError, VRAMInsufficientError,
    CapabilityNotFoundError, PermissionDeniedError, ParseError
)
assert issubclass(VRAMInsufficientError, ModelCallError)
assert issubclass(ModelCallError, JarvisError)
assert issubclass(PermissionDeniedError, JarvisError)
print('Exceptions OK')
"
```

Artifact: `src/core/exceptions.py`

---

### TASK 1.13 — `tests/conftest.py` Shared Fixtures

Location:

- `tests/conftest.py`

Purpose:

- Shared pytest fixtures to eliminate duplication across 10+ test files.

Steps:

1. Create `tests/conftest.py`.
2. Define fixtures:

   ```python
   @pytest.fixture
   def default_profile():
       return UserProfile(user_id="test_user", language="en")

   @pytest.fixture
   def default_packet(default_profile):
       return InputPacket(
           user_message="hello",
           session_id="test_session",
           user_profile=default_profile
       )

   @pytest.fixture(autouse=True)
   def reset_metrics():
       """Reset MetricsCollector singleton between tests."""
       yield
       MetricsCollector().reset()

   @pytest.fixture(autouse=True)
   def clear_event_bus():
       """Clear all EventBus subscriptions between tests."""
       yield
       EventBus().clear()

   @pytest.fixture
   def tmp_db(tmp_path):
       """Provide isolated temp SQLite path for memory tests."""
       return str(tmp_path / "test_memory.db")

   @pytest.fixture
   def mock_ollama(monkeypatch):
       """Monkeypatch OllamaEngine.chat to return deterministic response."""
       from src.models.llm.engine import OllamaEngine
       monkeypatch.setattr(OllamaEngine, "chat", lambda *a, **kw: "mocked response")
       return "mocked response"
   ```

3. Import guard: fixtures that import Phase 2+ objects use lazy imports inside the fixture body to avoid circular import at collection time.

Validation:

```bash
pytest tests/ --collect-only 2>&1 | grep "conftest"
# Should show conftest.py collected with no import errors
```

Artifact: `tests/conftest.py`

---

### Definition of Done — Phase 1

- `python app/main.py --interface cli` prints `JARVIS ready`, Ctrl+C exits cleanly.
- `pytest tests/` collects without errors (even if no tests yet).
- `config/settings.yaml` loads with all fields validated.
- EventBus, exceptions, profiles, logging all importable.

### Human Checkpoint

Manually: run `app/main.py`, check `logs/` directory has a JSON log file, verify Ollama warning appears if Ollama is not running.

---

## 📝 Phase 2 — Execution Contract

```yaml
phase_id: 2
title: "Execution Contract"
priority: "P0"
status: "not_started"
total_tasks: 10
blocker: "Phase 1 complete"
next_action: "TASK 2.0"
```

### Objective

Define strict data contracts binding all components. Every contract validates on instantiation and rejects invalid data. These are load-bearing types — all phases depend on them.

---

### TASK 2.0 — Capability Validator Stub

Location:

- `src/capabilities/validator.py`

Purpose:

- Create stub for `SchemaValidator` referenced in TASK 6.6 ("expand TASK 2.x"). Must exist before Phase 6.

Steps:

1. Create `src/capabilities/validator.py`.
2. Define `ValidationResult` dataclass (also used as contract — see TASK 2.9):
   ```python
   @dataclass
   class ValidationResult:
       valid: bool
       errors: list[str] = field(default_factory=list)
   ```
3. Define `SchemaValidator` stub class:
   ```python
   class SchemaValidator:
       def validate(self, capability_name: str, args: dict) -> ValidationResult:
           """Stub: always returns valid. Full implementation in Phase 6 TASK 6.6."""
           return ValidationResult(valid=True)
   ```
4. Phase 6 TASK 6.6 expands this class with real schema loading and validation. The stub ensures Phase 8 `CapabilityExecutor` can import `SchemaValidator` without waiting for Phase 6.

Validation:

```bash
python -c "
from src.capabilities.validator import SchemaValidator, ValidationResult
sv = SchemaValidator()
r = sv.validate('open_app', {'name': 'notepad'})
assert r.valid
print('Validator stub OK')
"
```

Artifact: `src/capabilities/validator.py`

---

### TASK 2.1 — Define `InputPacket`

Location:

- `src/core/context/bundle.py`

Purpose:

- Canonical input container passed through the entire runtime loop.

Steps:

1. Create `src/core/context/bundle.py`.
2. Define `InputPacket` using Pydantic `BaseModel` (not dataclass — enables `.model_validate()`, `.model_dump()`):

   ```python
   class InputPacket(BaseModel):
       user_message: str
       session_id: str
       attachments: list[dict] = []
       memory_snippets: list[dict] = []
       recent_history: list[dict] = []
       user_profile: UserProfile
       tool_results: list[dict] = []
       turn_number: int = 0
       trace_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
       timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

       model_config = ConfigDict(arbitrary_types_allowed=True)

       @field_validator('user_message')
       @classmethod
       def message_not_empty(cls, v):
           if not v or not v.strip():
               raise ValueError("user_message cannot be empty or whitespace")
           return v.strip()

       @field_validator('session_id')
       @classmethod
       def session_id_not_empty(cls, v):
           if not v:
               raise ValueError("session_id cannot be empty")
           return v
   ```

3. Import `UserProfile` from `src.memory.user_profile`.
4. `trace_id` auto-generated as UUIDv4 if not supplied.
5. `user_message` is stripped of leading/trailing whitespace.

Success case:

- Valid `InputPacket` instantiates without error.
- `user_message=""` raises `ValidationError`.
- `session_id=""` raises `ValidationError`.

Validation:

```bash
python -c "
from src.core.context.bundle import InputPacket
from src.memory.user_profile import UserProfile
import pytest
p = InputPacket(user_message='hello', session_id='s1', user_profile=UserProfile(user_id='u1'))
assert p.user_message == 'hello'
assert p.trace_id  # auto-generated
try:
    InputPacket(user_message='', session_id='s1', user_profile=UserProfile(user_id='u1'))
    assert False, 'Should have raised'
except Exception:
    pass
print('InputPacket OK')
"
```

Artifact: `src/core/context/bundle.py`

---

### TASK 2.2 — Define `DecisionOutput`

Location:

- `src/core/decision/output.py`

Purpose:

- Structured output of the decision system. **Separated from `decision.py`** (which contains the `decide()` function) to avoid circular imports.

Steps:

1. Create `src/core/decision/output.py` (NOT `decision.py` — that file is for the `decide()` function in Phase 5).
2. Define enums:

   ```python
   class Intent(str, Enum):
       chat = "chat"
       tool_use = "tool_use"
       planning = "planning"
       search = "search"

   class Complexity(str, Enum):
       low = "low"
       medium = "medium"
       high = "high"

   class ExecutionMode(str, Enum):
       fast = "fast"
       normal = "normal"
       deep = "deep"
       planning = "planning"
       research = "research"

   class RiskLevel(str, Enum):
       low = "low"
       medium = "medium"
       high = "high"

   class DecisionSource(str, Enum):
       fast_path = "fast_path"
       model = "model"
   ```

3. Define `DecisionOutput` as Pydantic `BaseModel`:

   ```python
   class DecisionOutput(BaseModel):
       intent: Intent
       complexity: Complexity
       mode: ExecutionMode
       model: str
       requires_tools: bool
       requires_planning: bool = False
       tool_name: str | None = None
       tool_args: dict = {}
       confidence: float = Field(ge=0.0, le=1.0)
       risk_level: RiskLevel
       decision_source: DecisionSource
       score_breakdown: dict = {}
       candidate_list: list[dict] = []

       @model_validator(mode='after')
       def validate_tool_consistency(self):
           if self.requires_tools and self.tool_name is None:
               raise ValueError("tool_name required when requires_tools=True")
           if not self.requires_tools and self.tool_name is not None:
               raise ValueError("tool_name must be None when requires_tools=False")
           if self.decision_source == DecisionSource.model:
               if not self.score_breakdown:
                   raise ValueError("score_breakdown required for model-path decisions")
               if not self.candidate_list:
                   raise ValueError("candidate_list required for model-path decisions")
           return self
   ```

Success case:

- Valid `DecisionOutput` instantiates.
- `confidence=1.5` raises `ValidationError`.
- `requires_tools=True, tool_name=None` raises `ValidationError`.
- `decision_source=model, score_breakdown={}` raises `ValidationError`.

Validation:

```bash
python -c "
from src.core.decision.output import DecisionOutput, Intent, Complexity, ExecutionMode, RiskLevel, DecisionSource
d = DecisionOutput(
    intent=Intent.chat, complexity=Complexity.low, mode=ExecutionMode.fast,
    model='gemma3:4b', requires_tools=False, confidence=0.9,
    risk_level=RiskLevel.low, decision_source=DecisionSource.fast_path
)
assert d.intent == Intent.chat
try:
    DecisionOutput(
        intent=Intent.tool_use, complexity=Complexity.low, mode=ExecutionMode.fast,
        model='gemma3:4b', requires_tools=True, tool_name=None, confidence=0.9,
        risk_level=RiskLevel.low, decision_source=DecisionSource.fast_path
    )
    assert False
except Exception:
    pass
print('DecisionOutput OK')
"
```

Artifact: `src/core/decision/output.py`

---

### TASK 2.3 — Define `LLMOutput`

Location:

- `src/core/runtime/llm_output.py`

Steps:

1. Create `src/core/runtime/llm_output.py`.
2. Define `LLMOutputType` enum: `answer`, `tool_call`.
3. Define `LLMOutput` as Pydantic `BaseModel`:

   ```python
   class LLMOutput(BaseModel):
       type: LLMOutputType
       content: str | None = None
       tool: str | None = None
       args: dict = {}
       raw: str = ""          # original LLM text before parsing, for debugging

       @model_validator(mode='after')
       def validate_type_fields(self):
           if self.type == LLMOutputType.answer and not self.content:
               raise ValueError("content required when type=answer")
           if self.type == LLMOutputType.tool_call and not self.tool:
               raise ValueError("tool required when type=tool_call")
           return self
   ```

Validation:

```bash
python -c "
from src.core.runtime.llm_output import LLMOutput, LLMOutputType
a = LLMOutput(type=LLMOutputType.answer, content='hi')
t = LLMOutput(type=LLMOutputType.tool_call, tool='open_app', args={'name': 'notepad'})
assert a.content == 'hi'
assert t.tool == 'open_app'
try:
    LLMOutput(type=LLMOutputType.answer)
    assert False
except Exception:
    pass
print('LLMOutput OK')
"
```

Artifact: `src/core/runtime/llm_output.py`

---

### TASK 2.4 — Define `ToolResult`

Location:

- `src/capabilities/result.py`

Steps:

1. Create `src/capabilities/result.py`.
2. Define `ToolResult` as Pydantic `BaseModel`:
   ```python
   class ToolResult(BaseModel):
       tool: str
       success: bool
       data: dict = {}
       error: str = ""
       duration_ms: float = 0.0
       dry_run: bool = False
       risk_level: str = "low"      # propagated from capability for audit
       turn_id: int = 0
   ```
3. Add class method `ToolResult.failure(tool, error, duration_ms=0.0)` for ergonomic error construction.

Validation:

```bash
python -c "
from src.capabilities.result import ToolResult
r = ToolResult(tool='open_app', success=True, data={'pid': 1234})
assert r.success
f = ToolResult.failure('open_app', 'not found')
assert not f.success and f.error == 'not found'
print('ToolResult OK')
"
```

Artifact: `src/capabilities/result.py`

---

### TASK 2.5 — Define `FinalResponse`

Location:

- `src/core/runtime/final_response.py`

Steps:

1. Create `src/core/runtime/final_response.py`.
2. Define `FinalResponse` as Pydantic `BaseModel`:
   ```python
   class FinalResponse(BaseModel):
       text: str
       session_id: str
       model: str
       mode: str
       quality: float = Field(ge=0.0, le=1.0)
       decision_source: DecisionSource
       degraded: bool = False
       turn_id: int
       tool_results: list[ToolResult] = []
       duration_ms: float = 0.0
       trace_id: str = ""
   ```

Validation:

```bash
python -c "
from src.core.runtime.final_response import FinalResponse
from src.core.decision.output import DecisionSource
r = FinalResponse(text='hi', session_id='s1', model='gemma3:4b', mode='fast',
                  quality=0.9, decision_source=DecisionSource.fast_path, turn_id=1)
assert r.text == 'hi'
try:
    FinalResponse(text='hi', session_id='s1', model='m', mode='f',
                  quality=1.5, decision_source=DecisionSource.fast_path, turn_id=1)
    assert False
except Exception:
    pass
print('FinalResponse OK')
"
```

Artifact: `src/core/runtime/final_response.py`

---

### TASK 2.6 — Define `ModelScore`

Location:

- `src/core/decision/model_score.py`

Steps:

1. Create `src/core/decision/model_score.py`.
2. Define `ModelScore` as Pydantic `BaseModel`:

   ```python
   class ModelScore(BaseModel):
       model: str
       score: float = Field(ge=0.0, le=1.0)
       factor_scores: dict[str, float]    # keys must match config/models.yaml weights keys
       vram_available_mb: int = 0
       is_available: bool = True

       @field_validator('factor_scores')
       @classmethod
       def validate_factor_keys(cls, v):
           required = {'fit_complexity', 'fit_mode', 'cost_penalty', 'quality_need', 'memory_bias'}
           if not required.issubset(v.keys()):
               missing = required - v.keys()
               raise ValueError(f"factor_scores missing keys: {missing}")
           return v
   ```

Validation:

```bash
python -c "
from src.core.decision.model_score import ModelScore
ms = ModelScore(
    model='gemma3:4b', score=0.85,
    factor_scores={'fit_complexity':0.9,'fit_mode':0.8,'cost_penalty':0.7,'quality_need':0.8,'memory_bias':0.9}
)
assert 0.0 <= ms.score <= 1.0
print('ModelScore OK')
"
```

Artifact: `src/core/decision/model_score.py`

---

### TASK 2.7 — Define `EvaluationResult`

Location:

- `src/core/runtime/evaluation_result.py`

Purpose:

- Return type of `Evaluator.evaluate()` (TASK 4.6). Defined here so it is available to all runtime modules.

Steps:

1. Create `src/core/runtime/evaluation_result.py`.
2. Define `EvaluationResult` as Pydantic `BaseModel`:
   ```python
   class EvaluationResult(BaseModel):
       should_retry: bool
       quality_score: float = Field(ge=0.0, le=1.0)
       issues: list[str] = []          # e.g., ["truncated", "off_topic"]
       retry_reason: str = ""
   ```

Validation:

```bash
python -c "
from src.core.runtime.evaluation_result import EvaluationResult
r = EvaluationResult(should_retry=False, quality_score=0.9)
assert not r.should_retry
print('EvaluationResult OK')
"
```

Artifact: `src/core/runtime/evaluation_result.py`

---

### TASK 2.8 — Define `ValidationResult`

Location:

- Already created in `src/capabilities/validator.py` (TASK 2.0).

Steps:

1. Verify `ValidationResult` in `src/capabilities/validator.py` has:

   ```python
   @dataclass
   class ValidationResult:
       valid: bool
       errors: list[str] = field(default_factory=list)

       def first_error(self) -> str | None:
           return self.errors[0] if self.errors else None
   ```

2. Add `first_error()` convenience method if not already present.

Validation:

```bash
python -c "
from src.capabilities.validator import ValidationResult
r = ValidationResult(valid=False, errors=['name is required'])
assert r.first_error() == 'name is required'
print('ValidationResult OK')
"
```

---

### TASK 2.9 — Contract Tests

Location:

- `tests/test_contracts.py`

Steps:

1. Create `tests/test_contracts.py`.
2. Tests (using `pytest.raises` for all failure cases):
   - `InputPacket` valid instantiation with all defaults
   - `InputPacket` rejects `user_message=""`
   - `InputPacket` rejects `user_message="   "` (whitespace-only)
   - `InputPacket` rejects `session_id=""`
   - `InputPacket` trace_id auto-generated as UUID
   - `DecisionOutput` valid chat instantiation
   - `DecisionOutput` rejects `confidence=1.5`
   - `DecisionOutput` rejects `requires_tools=True, tool_name=None`
   - `DecisionOutput` rejects `decision_source=model` with empty `score_breakdown`
   - `LLMOutput` valid answer type
   - `LLMOutput` valid tool_call type
   - `LLMOutput` rejects `type=answer` with no content
   - `LLMOutput` rejects `type=tool_call` with no tool
   - `ToolResult` valid instantiation + `ToolResult.failure()` convenience
   - `FinalResponse` valid instantiation
   - `FinalResponse` rejects `quality=1.5`
   - `ModelScore` valid instantiation
   - `ModelScore` rejects `factor_scores` missing required key
   - `EvaluationResult` valid instantiation
   - `ValidationResult` `first_error()` returns None when no errors

Validation:

```bash
pytest tests/test_contracts.py -v
# Expected: 20 passed
```

Artifact: `tests/test_contracts.py`

---

### Definition of Done — Phase 2

`pytest tests/test_contracts.py -v` passes all 20 contract tests.

---

## 🤖 Phase 3 — Model Manager + VRAM

```yaml
phase_id: 3
priority: "P0"
total_tasks: 5
blocker: "Phase 2 complete"
```

### Objective

VRAM monitoring, model lifecycle management with Ollama's actual API, and concurrency control.

---

### TASK 3.1 — VRAM Monitor

Location:

- `src/models/vram_monitor.py`

Steps:

1. Create `src/models/vram_monitor.py`.
2. Define `VRAMMonitor` class.
3. Primary implementation: use `pynvml`:
   ```python
   import pynvml
   pynvml.nvmlInit()
   handle = pynvml.nvmlDeviceGetHandleByIndex(0)  # GPU 0
   info = pynvml.nvmlDeviceGetMemoryInfo(handle)
   available_mb = info.free // (1024 * 1024)
   total_mb = info.total // (1024 * 1024)
   ```
4. Fallback (pynvml unavailable or no NVIDIA GPU):
   - `get_total_vram_mb()` → returns `6144` (RTX 3050 6GB heuristic).
   - `get_available_vram_mb()` → returns `4096` (conservative assumption).
   - Log `WARNING: pynvml unavailable, using heuristic VRAM values`.
5. Implement `get_available_vram_mb() -> int`.
6. Implement `get_total_vram_mb() -> int`.
7. Implement `is_model_loadable(required_vram_mb: int) -> bool` → `get_available_vram_mb() >= required_vram_mb + 512` (512MB safety margin).
8. Cache readings for 5 seconds to avoid hammering NVML.
9. Implement `force_refresh() -> None` to bypass cache.

Success case:

- `get_available_vram_mb()` returns positive integer.
- `is_model_loadable(8000)` returns False on 6GB card.

Validation:

```bash
python -c "
from src.models.vram_monitor import VRAMMonitor
vm = VRAMMonitor()
avail = vm.get_available_vram_mb()
total = vm.get_total_vram_mb()
assert avail > 0
assert total > 0
assert total >= avail
loadable = vm.is_model_loadable(3200)
print(f'VRAM: {avail}/{total} MB, gemma3:4b loadable: {loadable}')
"
```

Artifact: `src/models/vram_monitor.py`

---

### TASK 3.2 — Model Lifecycle Manager

Location:

- `src/models/manager.py`

Purpose:

- Load, unload, and swap models via Ollama's API. Serializes all operations with a `threading.Lock`. Enforces one-model-at-a-time.

Steps:

1. Create `src/models/manager.py`.
2. Define `ModelManager` class.
3. Internal state: `_current_model: str | None`, `_lock: threading.Lock`, `_busy: bool`.
4. Implement `load_model(model_name: str) -> None`:
   - Acquire lock.
   - If `_current_model == model_name`: release, return (no-op).
   - If `_current_model != None`: call `unload_model(_current_model)` first.
   - Check VRAM: `VRAMMonitor().is_model_loadable(profile.vram_required_mb)`.
   - If insufficient: release lock, raise `VRAMInsufficientError`.
   - Send Ollama warm-up call: `POST /api/generate {"model": model_name, "keep_alive": "10m", "prompt": ""}`.
   - Set `_current_model = model_name`.
   - Release lock.
5. Implement `unload_model(model_name: str) -> None`:
   - Send: `POST /api/generate {"model": model_name, "keep_alive": 0, "prompt": ""}`.
   - This is Ollama's official unload mechanism (`keep_alive: 0`).
   - Set `_current_model = None`.
6. Implement `swap_model(to_model: str) -> None` → calls `unload_model(current)` then `load_model(to_model)` within a single lock acquisition.
7. Implement `get_current_model() -> str | None`.
8. Implement `is_model_loaded(model_name: str) -> bool`.
9. Implement `is_busy() -> bool`.
10. Lock timeout: if lock not acquired within 120 seconds → raise `TimeoutError("ModelManager lock timeout")`.

Success case:

- `load_model("gemma3:4b")` → `get_current_model() == "gemma3:4b"`.
- `unload_model("gemma3:4b")` → `get_current_model() is None`.
- Second `load_model("gemma3:4b")` call when already loaded → no-op.

Failure case:

- VRAM insufficient → `VRAMInsufficientError` raised, no model loaded.
- Ollama not running → `ModelCallError` with connection detail.

Validation:

```bash
python -c "
from src.models.manager import ModelManager
mm = ModelManager()
# Only run if Ollama is available
import requests
try:
    requests.get('http://localhost:11434/api/tags', timeout=2)
    mm.load_model('gemma3:4b')
    assert mm.get_current_model() == 'gemma3:4b'
    mm.unload_model('gemma3:4b')
    assert mm.get_current_model() is None
    print('ModelManager OK')
except Exception as e:
    print(f'Skipped (Ollama unavailable): {e}')
"
```

Artifact: `src/models/manager.py`

---

### TASK 3.3 — Concurrency Control (expand TASK 3.2)

Location:

- `src/models/manager.py`

Purpose:

- Ensure concurrent model calls serialize correctly.

Steps:

1. All `ModelManager` methods already wrapped in `threading.Lock` from TASK 3.2.
2. Add `_call_count: int = 0` and `_queue_depth: int = 0` for observability.
3. In `load_model` and `unload_model`, publish `EVT_MODEL_SWAP` to `EventBus` after operation.
4. Add concurrency test:
   ```python
   # Two threads both try to load simultaneously — second should wait
   import threading
   results = []
   def load_and_record():
       mm = ModelManager()
       mm.load_model('gemma3:4b')
       results.append(mm.get_current_model())
   t1 = threading.Thread(target=load_and_record)
   t2 = threading.Thread(target=load_and_record)
   t1.start(); t2.start(); t1.join(); t2.join()
   assert all(r == 'gemma3:4b' for r in results)
   ```
5. No new artifact — changes are in `src/models/manager.py`.

---

### TASK 3.4 — Model Availability Registry

Location:

- `src/models/availability.py`

Steps:

1. Create `src/models/availability.py`.
2. Define `ModelAvailability` class.
3. Implement `refresh() -> None`:
   - Call `GET http://localhost:11434/api/tags` → parse `models` array from response.
   - Extract `name` from each entry.
   - Cross-reference with `PROFILES` from `src.models.profiles`.
   - Cross-reference with `VRAMMonitor().is_model_loadable(profile.vram_required_mb)`.
   - Store as `_available: list[str]`.
4. Implement `get_available_models() -> list[str]`.
5. Implement `is_available(model_name: str) -> bool`.
6. Cache for 30 seconds; `refresh()` forces immediate re-check.
7. If Ollama unreachable: return empty list, log WARNING.

Success case:

- After `ollama pull gemma3:4b`, `is_available("gemma3:4b")` returns True.
- `is_available("nonexistent:latest")` returns False.

Validation:

```bash
python -c "
from src.models.availability import ModelAvailability
ma = ModelAvailability()
ma.refresh()
available = ma.get_available_models()
print(f'Available models: {available}')
"
```

Artifact: `src/models/availability.py`

---

### TASK 3.5 — LLM Engine with Model Manager Integration

Location:

- `src/models/llm/engine.py` (expand Phase 0 TASK 0.1)

Steps:

1. Expand `src/models/llm/engine.py`.
2. `OllamaEngine` gains a `ModelManager` instance.
3. Implement `chat_with_model(model_name: str, messages: list[dict], system: str = "") -> str`:
   - Call `ModelManager().load_model(model_name)` (no-op if already loaded).
   - Construct Ollama `messages` array: `[{"role": "system", "content": system}, *messages]` if system provided.
   - POST to `http://localhost:11434/api/chat` with `{"model": model_name, "messages": [...], "stream": False}`.
   - Apply timeout from config `models.timeout_s`.
   - On `requests.Timeout` → raise `ModelCallError("model timeout")`.
   - On `requests.ConnectionError` → raise `ModelCallError("Ollama not reachable")`.
   - On non-200 response → raise `ModelCallError(f"Ollama error: {status_code}")`.
   - Return `response.json()["message"]["content"]`.
4. Retain original `chat(message, model)` method for Phase 0 backward compatibility during Phase 0 → Phase 9 migration window. Mark as deprecated with `warnings.warn`.
5. `chat_with_model` records latency to `MetricsCollector`.

Validation:

```bash
python -c "
from src.models.llm.engine import OllamaEngine
e = OllamaEngine()
try:
    r = e.chat_with_model('gemma3:4b', [{'role':'user','content':'say hello'}])
    assert len(r) > 0
    print(r[:80])
except Exception as ex:
    print(f'Skipped (Ollama unavailable): {ex}')
"
```

---

### Definition of Done — Phase 3

VRAM monitor returns valid readings. ModelManager loads, unloads, swaps. Concurrency is serialized. Availability registry returns correct list.

---

## ⚙️ Phase 4 — Runtime State Machine

```yaml
phase_id: 4
priority: "P0"
total_tasks: 8
blocker: "Phase 3 complete"
```

### Objective

The state machine is the single source of truth for all execution flow. No component may bypass it.

---

### TASK 4.1 — `RuntimeState` Enum and Transition Map

Location:

- `src/core/runtime/state.py`

Steps:

1. Create `src/core/runtime/state.py`.
2. Define `RuntimeState(str, Enum)`:
   ```python
   IDLE = "IDLE"
   DECIDING = "DECIDING"
   EXECUTING_MODEL = "EXECUTING_MODEL"
   EXECUTING_TOOL = "EXECUTING_TOOL"
   WAITING_CONFIRMATION = "WAITING_CONFIRMATION"
   EVALUATING = "EVALUATING"
   ERROR = "ERROR"
   COMPLETED = "COMPLETED"
   ```
3. Define `ALLOWED_TRANSITIONS: dict[RuntimeState, frozenset[RuntimeState]]`:
   ```python
   ALLOWED_TRANSITIONS = {
       IDLE:                   frozenset({DECIDING}),
       DECIDING:               frozenset({EXECUTING_MODEL, EXECUTING_TOOL, ERROR}),
       EXECUTING_MODEL:        frozenset({EVALUATING, EXECUTING_TOOL, ERROR}),
       EXECUTING_TOOL:         frozenset({WAITING_CONFIRMATION, EVALUATING, ERROR}),
       WAITING_CONFIRMATION:   frozenset({EXECUTING_TOOL, ERROR, IDLE}),
       EVALUATING:             frozenset({COMPLETED, DECIDING, ERROR}),
       ERROR:                  frozenset({IDLE}),
       COMPLETED:              frozenset({IDLE}),
   }
   ```
4. Implement `can_transition(from_state: RuntimeState, to_state: RuntimeState) -> bool`.

Validation:

```bash
python -c "
from src.core.runtime.state import RuntimeState, can_transition
assert can_transition(RuntimeState.IDLE, RuntimeState.DECIDING)
assert can_transition(RuntimeState.ERROR, RuntimeState.IDLE)
assert not can_transition(RuntimeState.IDLE, RuntimeState.EXECUTING_TOOL)
assert not can_transition(RuntimeState.COMPLETED, RuntimeState.EXECUTING_MODEL)
print('State transitions OK')
"
```

Artifact: `src/core/runtime/state.py`

---

### TASK 4.2 — State Manager

Location:

- `src/core/runtime/state_manager.py`

Steps:

1. Create `src/core/runtime/state_manager.py`.
2. Define `StateManager` class.
3. Internal state: `_state: RuntimeState = IDLE`, `_history: list[tuple[RuntimeState, RuntimeState, str]]`, `_lock: threading.Lock`.
4. Property `current_state -> RuntimeState`.
5. Implement `transition_to(new_state: RuntimeState, reason: str = "") -> None`:
   - Acquire lock.
   - Check `can_transition(self._state, new_state)`.
   - If invalid: release lock, raise `InvalidTransitionError(f"{self._state} → {new_state} not allowed")`.
   - Append `(self._state, new_state, datetime.utcnow().isoformat())` to history.
   - Set `self._state = new_state`.
   - Log transition via `log_event`.
   - Publish `EVT_STATE_TRANSITION` to `EventBus` with `{"from": old_state, "to": new_state, "reason": reason}`.
   - Release lock.
6. Implement `force_state(state: RuntimeState) -> None` (bypasses validation — for error recovery only):
   - Log WARNING with "FORCED STATE TRANSITION" prefix.
   - Sets state directly.
7. Implement `get_history() -> list[tuple]`.
8. Implement `reset() -> None` → `force_state(IDLE)`, clears history.

Validation:

```bash
python -c "
from src.core.runtime.state_manager import StateManager
from src.core.runtime.state import RuntimeState
from src.core.exceptions import InvalidTransitionError
sm = StateManager()
assert sm.current_state == RuntimeState.IDLE
sm.transition_to(RuntimeState.DECIDING, reason='test')
assert sm.current_state == RuntimeState.DECIDING
try:
    sm.transition_to(RuntimeState.IDLE)  # invalid: DECIDING → IDLE not allowed
    assert False
except InvalidTransitionError:
    pass
assert sm.current_state == RuntimeState.DECIDING  # unchanged
print('StateManager OK')
"
```

Artifact: `src/core/runtime/state_manager.py`

---

### TASK 4.3 — Hard Limits

Location:

- `src/core/runtime/limits.py`

Purpose:

- Single authoritative source for all numeric execution limits. Values loaded from config.

Steps:

1. Create `src/core/runtime/limits.py`.
2. Define `Limits` class:
   ```python
   class Limits:
       def __init__(self, config=None):
           cfg = config or load_config().execution
           self.max_iterations: int = cfg.max_iterations          # 5
           self.max_tool_calls: int = cfg.max_tool_calls          # 3
           self.max_tool_depth: int = cfg.max_tool_depth          # 3
           self.max_decision_retries: int = cfg.max_decision_retries  # 3
           self.max_model_retries: int = cfg.max_model_retries    # 2
           self.global_retry_budget: int = cfg.global_retry_budget # 8
           self.tool_timeout_s: int = cfg.tool_timeout_s          # 30
           self.model_timeout_s: int = cfg.model_timeout_s        # 120
           self.step_timeout_s: int = cfg.step_timeout_s          # 60
           self.total_turn_timeout_s: int = cfg.total_turn_timeout_s  # 300
   ```
3. Implement `check_limit(limit_name: str, current_value: int) -> bool`:
   - Returns `True` if `current_value < getattr(self, limit_name)` (still within limit).
   - Returns `False` if `current_value >= getattr(self, limit_name)` (limit reached or exceeded).
   - Raises `AttributeError` if `limit_name` not found — this is a programming error.
   - **Semantics: `check_limit("max_iterations", 4)` returns True (4 < 5 → OK to continue). `check_limit("max_iterations", 5)` returns False (5 >= 5 → stop).**

Success case:

- `check_limit("max_iterations", 4)` → True.
- `check_limit("max_iterations", 5)` → False.
- `check_limit("max_iterations", 6)` → False.

Validation:

```bash
python -c "
from src.core.runtime.limits import Limits
l = Limits()
assert l.check_limit('max_iterations', 4) == True
assert l.check_limit('max_iterations', 5) == False
assert l.check_limit('max_iterations', 6) == False
assert l.check_limit('max_tool_calls', 0) == True
assert l.check_limit('max_tool_calls', 3) == False
print('Limits OK')
"
```

Artifact: `src/core/runtime/limits.py`

---

### TASK 4.4 — Context Assembler

Location:

- `src/core/context/assembler.py`

Steps:

1. Create `src/core/context/assembler.py`.
2. Define `ContextAssembler` class with `MemoryDB` and `UserProfile` dependencies injected (or constructed internally with defaults).
3. Implement `assemble(user_input: str, session_id: str, turn_number: int = 0) -> InputPacket`:
   a. Load user profile: `load_profile("default")`.
   b. Fetch recent history: `MemoryDB().retrieve_recent(session_id, limit=5)` — empty list on cold start.
   c. Return `InputPacket(user_message=user_input, session_id=session_id, user_profile=profile, recent_history=history, turn_number=turn_number)`.
4. Cold start is not an error — `memory_snippets=[]` and `recent_history=[]` are valid.

Validation:

```bash
python -c "
from src.core.context.assembler import ContextAssembler
a = ContextAssembler()
p = a.assemble('hello', 's1', turn_number=0)
assert p.user_message == 'hello'
assert p.session_id == 's1'
assert isinstance(p.recent_history, list)
print('ContextAssembler OK')
"
```

Artifact: `src/core/context/assembler.py`

---

### TASK 4.5 — Executor

Location:

- `src/core/runtime/executor.py`

Steps:

1. Create `src/core/runtime/executor.py`.
2. Define `Executor` class.
3. Implement `execute(decision: DecisionOutput, input_packet: InputPacket) -> LLMOutput`:
   a. Build prompt via `PromptBuilder` (stubbed to return basic system string until Phase 10).
   b. Construct `messages` from `input_packet.recent_history` + current user message.
   c. Call `OllamaEngine().chat_with_model(decision.model, messages, system=prompt)`.
   d. Attempt JSON parse of response to detect tool call: look for `{"tool": ..., "args": ...}` structure.
   e. If parseable as tool call → return `LLMOutput(type=tool_call, tool=..., args=..., raw=raw_text)`.
   f. Else → return `LLMOutput(type=answer, content=raw_text, raw=raw_text)`.
   g. On `ModelCallError` → re-raise (caller handles via fallback).
   h. On JSON parse failure → return `LLMOutput(type=answer, content=raw_text)` (no retry here — let evaluator decide).
4. Record latency to `MetricsCollector`.

Artifact: `src/core/runtime/executor.py`

---

### TASK 4.6 — Evaluator

Location:

- `src/core/runtime/evaluator.py`

Steps:

1. Create `src/core/runtime/evaluator.py`.
2. Define `Evaluator` class.
3. Implement `should_evaluate(output: LLMOutput, decision: DecisionOutput) -> bool`:
   - Returns True only when: output.content length > 500 chars, OR decision.complexity == "high", OR decision.degraded.
   - Short/simple responses skip evaluation (performance optimization).
4. Implement `evaluate(output: LLMOutput, decision: DecisionOutput, input_packet: InputPacket) -> EvaluationResult`:
   - **Completeness**: check if content ends abruptly (no period/conclusion) → truncation signal.
   - **Relevance**: check if any key term from `input_packet.user_message` appears in output content (simple overlap heuristic).
   - **Coherence**: response length > 10 chars and is not an error message.
   - Compute `quality_score` as weighted average: completeness _ 0.4 + relevance _ 0.4 + coherence \* 0.2.
   - `should_retry = quality_score < 0.4`.
   - Return `EvaluationResult`.
5. This is a heuristic evaluator — no LLM call. LLM-based evaluation is a Phase 18 enhancement if needed.

Artifact: `src/core/runtime/evaluator.py`

---

### TASK 4.7 — Runtime Loop

Location:

- `src/core/runtime/loop.py`

Steps:

1. Create `src/core/runtime/loop.py`.
2. Define `run_turn(user_input: str, session_id: str, mode_override: str | None = None) -> FinalResponse`.
3. Create `StateManager`, `Limits`, `ContextAssembler`, `Executor`, `Evaluator` instances (or inject from DI container — use module-level singletons for now).
4. Track: `iteration_count = 0`, `tool_call_count = 0`, `turn_start_time = time.time()`.
5. Loop body — state transitions strictly via `StateManager.transition_to()`:
   ```
   IDLE → DECIDING
     assemble context via ContextAssembler
     call decide(input_packet) → DecisionOutput (stub until Phase 5)
   DECIDING → EXECUTING_MODEL (if intent=chat or decision_source=model needed)
     call Executor.execute(decision, input_packet) → LLMOutput
   EXECUTING_MODEL → EVALUATING
     if Evaluator.should_evaluate(): evaluate → EvaluationResult
     if should_retry and check_limit(iterations): EVALUATING → DECIDING
     else: EVALUATING → COMPLETED
   DECIDING → EXECUTING_TOOL (if intent=tool_use)
     [stub until Phase 8: return mock ToolResult]
   EXECUTING_TOOL → EVALUATING
   COMPLETED → IDLE (after building FinalResponse)
   ```
6. Enforce after each iteration: `iteration_count += 1; if not limits.check_limit("max_iterations", iteration_count): break`.
7. Enforce total turn timeout: `if time.time() - turn_start_time > limits.total_turn_timeout_s: raise TurnTimeoutError`.
8. On any `JarvisError`: `StateManager.transition_to(ERROR)` → `StateManager.transition_to(IDLE)` → return degraded FinalResponse.
9. After completing, publish `EVT_TURN_COMPLETE` to EventBus.
10. **Decision stub (Phase 0/4 bridge):** until Phase 5 is complete, the `decide()` function is a stub that always returns a chat DecisionOutput using `gemma3:4b`.

Validation:

```bash
python -c "
from src.core.runtime.loop import run_turn
r = run_turn('hello', 'test_session')
assert r.text is not None
assert r.session_id == 'test_session'
print(r.text[:100])
"
```

Artifact: `src/core/runtime/loop.py`

---

### TASK 4.8 — State Machine Tests

Location:

- `tests/test_state_machine.py`

Tests:

1. `IDLE → DECIDING` allowed.
2. `IDLE → EXECUTING_TOOL` raises `InvalidTransitionError`.
3. `ERROR → IDLE` allowed.
4. `COMPLETED → IDLE` allowed.
5. `COMPLETED → DECIDING` raises `InvalidTransitionError`.
6. `force_state()` bypasses validation.
7. `StateManager.reset()` returns to IDLE.
8. History records all transitions.
9. Limits: `check_limit("max_iterations", 4)` → True; `check_limit("max_iterations", 5)` → False.
10. `run_turn` returns `FinalResponse` with non-empty text.
11. `run_turn` on Ollama unavailable → returns degraded FinalResponse (no crash).
12. EventBus receives `EVT_STATE_TRANSITION` events.

Validation:

```bash
pytest tests/test_state_machine.py -v
```

Artifact: `tests/test_state_machine.py`

---

### Definition of Done — Phase 4

`run_turn("hello", "test")` returns `FinalResponse`. All transitions enforced. All limits checked. `pytest tests/test_state_machine.py -v` passes.

---

## 🧠 Phase 5 — Decision System

```yaml
phase_id: 5
priority: "P1"
total_tasks: 7
blocker: "Phase 4 complete"
```

### Objective

Replace Phase 4's decision stub with the full decision system: fast path, LLM classification, dynamic scoring, and risk assessment.

---

### TASK 5.1 — Classifier with Robust JSON Parsing

Location:

- `src/core/decision/classifier.py` (expand Phase 0 TASK 0.2)

Steps:

1. Expand `src/core/decision/classifier.py`.
2. Define `extract_json(text: str) -> dict | None`:
   - Strip markdown fences: `re.sub(r'```json|```', '', text)`.
   - Try `json.loads(stripped)`.
   - On `JSONDecodeError`: try to find first `{` and last `}` and parse that substring.
   - On second failure: return None.
3. Define `repair_json(text: str) -> str | None`:
   - Fix trailing commas: `re.sub(r',\s*}', '}', text)`.
   - Fix single quotes: `text.replace("'", '"')`.
   - Try parse again. Return repaired string or None.
4. Update `classify(message: str) -> DecisionOutput`:
   - Build JSON-forcing system prompt: `"Respond ONLY with a JSON object. Keys: intent (chat|tool_use|planning|search), complexity (low|medium|high), tool_name (string or null), tool_args (object). No other text."`.
   - Call `OllamaEngine().chat_with_model("gemma3:4b", messages, system=prompt)`.
   - Try `extract_json(response)` → if None, try `repair_json` → retry once (exponential backoff: sleep 1s).
   - After 2 failures: return `_safe_fallback_decision()`.
   - Parse result into `DecisionOutput` via `output.py` enums.
5. `_safe_fallback_decision() -> DecisionOutput` → always returns chat intent, `gemma3:4b`, confidence=0.5, `decision_source=fast_path`.

Validation:

```bash
python -c "
from src.core.decision.classifier import extract_json, Classifier
assert extract_json('\`\`\`json\n{\"intent\":\"chat\"}\n\`\`\`')['intent'] == 'chat'
assert extract_json('garbage text') is None
print('extract_json OK')
"
```

Artifact: `src/core/decision/classifier.py`

---

### TASK 5.2 — Fast-Path Rules

Location:

- `src/core/decision/fast_path.py`

Steps:

1. Create `src/core/decision/fast_path.py`.
2. Define `FastPath` class with a `_rules: list[tuple[Pattern, Callable → DecisionOutput]]` list.
3. Rule format: `(compiled_regex, factory_function)`.
4. Rules (English + Arabic, case-insensitive, compiled at class instantiation):
   ```
   Pattern: r"^(open|launch|start|run)\s+(.+)"  → intent=tool_use, tool_name=open_app, args={"name": group(2)}
   Pattern: r"^(افتح|شغّل|ابدأ)\s+(.+)"         → intent=tool_use, tool_name=open_app, args={"name": group(2)}
   Pattern: r"^(what is|what's|who is|define|explain)\s+(.+)" → intent=chat
   Pattern: r"^(ما هو|من هو|اشرح)\s+(.+)"        → intent=chat
   Pattern: r"^(search for|find|look up)\s+(.+)" → intent=search, tool_name=web_search, args={"query": group(2)}
   Pattern: r"^(ابحث عن|ابحث)\s+(.+)"            → intent=search, tool_name=web_search, args={"query": group(2)}
   Pattern: r"^(take a screenshot|screenshot)"   → intent=tool_use, tool_name=screenshot
   ```
5. Implement `check(message: str) -> DecisionOutput | None`:
   - Strip and lowercase for matching.
   - Return first match. Return None if no match.
   - All fast-path `DecisionOutput` have: `decision_source=fast_path`, `score_breakdown={}`, `candidate_list=[]`, `model=load_config().models.default`, `complexity=low`, `mode=fast`, `confidence=0.95`.
6. Fast-path decisions do NOT require `score_breakdown` or `candidate_list` because `decision_source=fast_path` (enforced by DecisionOutput validator in TASK 2.2).

Validation:

```bash
python -c "
from src.core.decision.fast_path import FastPath
fp = FastPath()
r = fp.check('open notepad')
assert r is not None and r.tool_name == 'open_app' and r.tool_args['name'] == 'notepad'
r_ar = fp.check('افتح المفكرة')
assert r_ar is not None and r_ar.tool_name == 'open_app'
assert fp.check('random gibberish abc') is None
print('FastPath OK')
"
```

Artifact: `src/core/decision/fast_path.py`

---

### TASK 5.3 — Dynamic Model Scorer

Location:

- `src/core/decision/scorer.py`

Purpose:

- Mathematically defined scoring. Factor names **must match** `config/models.yaml` weights keys exactly.

Steps:

1. Create `src/core/decision/scorer.py`.
2. Define `ModelScorer` class.
3. Load weights from `config/models.yaml` at instantiation.
4. Define normalization helpers:
   ```python
   REASONING_TIER_SCORES = {"low": 0.3, "medium": 0.7, "high": 1.0}
   LATENCY_TIER_SCORES = {"fast": 1.0, "medium": 0.6, "slow": 0.3}
   COMPLEXITY_NEEDED = {"low": 0.3, "medium": 0.6, "high": 1.0}
   MODE_LATENCY_NEEDED = {"fast": 1.0, "normal": 0.6, "deep": 0.3, "planning": 0.4, "research": 0.3}
   ```
5. Implement `score(model_name: str, complexity: str, mode: str, vram_available_mb: int, memory_bias: float = 0.5) -> ModelScore`:

   ```python
   profile = get_profile(model_name)
   if profile is None or not is_available(model_name):
       return ModelScore(model=model_name, score=0.0, factor_scores={...all zeros}, is_available=False)

   # fit_complexity: how well reasoning_tier matches complexity need
   fit_complexity = 1.0 - abs(REASONING_TIER_SCORES[profile.reasoning_tier] - COMPLEXITY_NEEDED[complexity])

   # fit_mode: how well latency_tier matches mode's latency requirement
   fit_mode = 1.0 - abs(LATENCY_TIER_SCORES[profile.latency_tier] - MODE_LATENCY_NEEDED[mode])

   # cost_penalty: lower VRAM = higher score (normalized to 6144 MB max)
   cost_penalty = 1.0 - (profile.vram_required_mb / 6144.0)

   # quality_need: absolute reasoning quality
   quality_need = REASONING_TIER_SCORES[profile.reasoning_tier]

   # memory_bias: passed in from historical success rate (0.0–1.0)
   # memory_bias = memory_bias  (already normalized)

   factor_scores = {
       "fit_complexity": round(fit_complexity, 4),
       "fit_mode": round(fit_mode, 4),
       "cost_penalty": round(cost_penalty, 4),
       "quality_need": round(quality_need, 4),
       "memory_bias": round(memory_bias, 4),
   }
   weighted_score = sum(weights[k] * factor_scores[k] for k in weights)
   return ModelScore(model=model_name, score=round(weighted_score, 4), factor_scores=factor_scores, vram_available_mb=vram_available_mb)
   ```

6. Implement `rank_models(complexity: str, mode: str, vram_available_mb: int) -> list[ModelScore]`:
   - Score all available models.
   - Sort by score descending.
   - Tie-break order: lower cost_penalty → lower vram → then alphabetical (deterministic).
   - Return sorted list.

Validation:

```bash
python -c "
from src.core.decision.scorer import ModelScorer
ms = ModelScorer()
result = ms.score('gemma3:4b', 'low', 'fast', 6000)
assert result.score > 0
required_keys = {'fit_complexity','fit_mode','cost_penalty','quality_need','memory_bias'}
assert required_keys == set(result.factor_scores.keys())
print(f'gemma3:4b score: {result.score}, factors: {result.factor_scores}')
"
```

Artifact: `src/core/decision/scorer.py`

---

### TASK 5.4 — Risk Assessment

Location:

- `src/core/decision/risk.py`

Steps:

1. Create `src/core/decision/risk.py`.
2. Define `RiskAssessor` class.
3. Define risk maps:
   ```python
   TOOL_RISK = {
       "open_app": "medium", "system_info": "low", "clipboard": "low",
       "notify": "low", "screenshot": "low", "file_ops": "medium",
       "code_exec": "high", "web_search": "low", "browser": "medium",
       "stt": "low", "tts": "low", "vision_analyze": "low", "image_gen": "low",
   }
   ACTION_RISK_OVERRIDE = {
       # file_ops action-level overrides
       "delete": "high", "write": "medium", "move": "medium",
       "read": "low", "list": "low", "copy": "medium",
   }
   ```
4. Implement `assess(decision: DecisionOutput) -> RiskLevel`:
   - If no tool: return `RiskLevel.low`.
   - Look up `TOOL_RISK.get(decision.tool_name, "high")` (unknown capability = high).
   - If tool is `file_ops` and `decision.tool_args.get("action")` in `ACTION_RISK_OVERRIDE`: use override.
   - Check `decision.tool_args` for dangerous patterns: path contains `..` → high, path starts with blocked root → high.
   - Return highest of computed levels.
5. Return `RiskLevel` enum value.

Validation:

```bash
python -c "
from src.core.decision.risk import RiskAssessor
from src.core.decision.output import DecisionOutput, Intent, Complexity, ExecutionMode, RiskLevel, DecisionSource
ra = RiskAssessor()
d = DecisionOutput(intent=Intent.tool_use, complexity=Complexity.low, mode=ExecutionMode.fast,
    model='gemma3:4b', requires_tools=True, tool_name='web_search',
    tool_args={'query':'python'}, confidence=0.9,
    risk_level=RiskLevel.low, decision_source=DecisionSource.fast_path)
assert ra.assess(d) == RiskLevel.low
print('RiskAssessor OK')
"
```

Artifact: `src/core/decision/risk.py`

---

### TASK 5.5 — Unified `decide()` Function

Location:

- `src/core/decision/decision.py`

Purpose:

- The public entry point for the decision system. Previously a stub in TASK 4.7 — this replaces it.

Steps:

1. Create `src/core/decision/decision.py`.
2. Import: `FastPath`, `Classifier`, `ModelScorer`, `RiskAssessor`, `ModelAvailability`, `VRAMMonitor`, `DecisionOutput`.
3. Define `decide(input_packet: InputPacket) -> DecisionOutput`:
   a. Step 1: `fast_result = FastPath().check(input_packet.user_message)` → if not None, assess risk, set `risk_level`, return.
   b. Step 2: `classification = Classifier().classify(input_packet.user_message)` → produces partial DecisionOutput.
   c. Step 3: `vram = VRAMMonitor().get_available_vram_mb()`.
   d. Step 4: `candidates = ModelScorer().rank_models(classification.complexity, classification.mode, vram)` — filter to `is_available=True`.
   e. Step 5: select `best = candidates[0]` (highest score). If candidates empty → use fallback from config.
   f. Step 6: `risk = RiskAssessor().assess(classification_with_model)`.
   g. Step 7: construct and return `DecisionOutput` with `model=best.model`, `score_breakdown=best.factor_scores`, `candidate_list=[c.model_dump() for c in candidates[:3]]`, `decision_source=model`.
4. Validate returned `DecisionOutput` before returning. If validation fails → return `_safe_default(input_packet)`.
5. Replace the stub `decide()` referenced in TASK 4.7's loop.

Validation:

```bash
python -c "
from src.core.decision.decision import decide
from src.core.context.bundle import InputPacket
from src.memory.user_profile import UserProfile
p = InputPacket(user_message='open notepad', session_id='s1', user_profile=UserProfile(user_id='default'))
d = decide(p)
assert d.intent is not None
print(f'Intent: {d.intent}, Source: {d.decision_source}, Model: {d.model}')
"
```

Artifact: `src/core/decision/decision.py`

---

### TASK 5.6 — Escalation Chain

Location:

- `src/core/runtime/escalation.py`

Steps:

1. Create `src/core/runtime/escalation.py`.
2. Define `EscalationChain` class.
3. Implement `retry(input_packet: InputPacket, attempt: int) -> DecisionOutput`:
   - attempt 1: call `decide(input_packet)` with standard weights.
   - attempt 2: adjust `fit_complexity` weight by +0.05, reduce `cost_penalty` by 0.05 (within config's `variability_margin`). Reconstruct scorer with adjusted weights and re-decide.
   - attempt 3: call `decide(input_packet)` with fallback tier_1 model forced.
   - attempt >= 4: return `_safe_fallback(input_packet)` using tier_2 model.
4. Log each attempt with attempt number and reason.

Artifact: `src/core/runtime/escalation.py`

---

### TASK 5.7 — Decision Tests

Location:

- `tests/test_decision.py`

Tests:

1. Fast path matches `"open notepad"` → `intent=tool_use, tool_name=open_app`.
2. Fast path matches `"افتح المفكرة"` → `intent=tool_use, tool_name=open_app`.
3. Fast path returns None for `"tell me a joke"`.
4. `extract_json` handles markdown fences.
5. `extract_json` handles malformed JSON (trailing comma).
6. `extract_json` returns None for pure garbage.
7. `ModelScorer.score` returns all 5 required factor keys.
8. `ModelScorer.rank_models` returns highest score first.
9. `RiskAssessor` returns `high` for `code_exec`.
10. `RiskAssessor` returns `low` for `web_search`.
11. `decide()` returns `decision_source=fast_path` for `"open notepad"`.
12. `decide()` returns `score_breakdown` and `candidate_list` for model-path.
13. `decide()` returns safe default when classifier fails.
14. Escalation: attempt 3 forces fallback tier_1 model.

Validation:

```bash
pytest tests/test_decision.py -v
```

Artifact: `tests/test_decision.py`

---

### Definition of Done — Phase 5

Fast path operational. Dynamic scoring uses all 5 factors with correct keys. All tests pass.

---

## 🛡️ Phase 6 — Sandbox + Safety

```yaml
phase_id: 6
priority: "P0"
total_tasks: 7
blocker: "Phase 5 complete"
```

---

### TASK 6.1 — Execution Sandbox

Location:

- `src/core/sandbox/sandbox.py`

Steps:

1. Create `src/core/sandbox/sandbox.py`.
2. Define `Sandbox` class.
3. Implement `execute(capability: BaseCapability, args: dict, timeout_s: int) -> ToolResult`:
   - Call `capability.execute(args)` in a `concurrent.futures.ThreadPoolExecutor` with `timeout` parameter.
   - On `TimeoutError`: return `ToolResult.failure(capability.name, f"timeout after {timeout_s}s")`.
   - On any `Exception`: return `ToolResult.failure(capability.name, str(e))`.
   - Record duration: `time.time()` before/after → set on `ToolResult.duration_ms`.
4. Implement `dry_run(capability: BaseCapability, args: dict) -> ToolResult`:
   - Call `capability.dry_run(args)`.
   - Returns what would happen without side effects.
   - `ToolResult.dry_run = True`.
5. **Resource limits**: capabilities run as Python objects in the executor thread, not subprocesses. Resource limits are enforced by:
   - Timeout (thread-level via Future).
   - Memory limit (optional): check `psutil.Process().memory_info().rss` after execution; if > threshold → log WARNING.
   - CPU is implicitly bounded by the GIL and timeout.
6. Track `_rollback_log: list[str]` — capabilities that support rollback append a rollback descriptor.

Artifact: `src/core/sandbox/sandbox.py`

---

### TASK 6.2 — Safety Classifier

Location:

- `src/core/safety/classifier.py`

Steps:

1. Create `src/core/safety/classifier.py`.
2. Define `SafetyClassifier` class.
3. Load `blocked_paths` and `allowed_roots` from config.
4. Implement `classify(capability_name: str, args: dict) -> RiskLevel`:
   - Look up base risk from `config/capabilities.yaml` via capability name.
   - Path check: if any arg value contains `..` (traversal) → return `high`.
   - Path check: if any arg value starts with a blocked path → return `high`.
   - Command check (for `code_exec`): code containing `import os`, `subprocess`, `__import__`, `exec`, `eval` → return `high`.
   - Unknown capability → return `high`.
   - Return looked-up risk level otherwise.
5. Use structured schema checks — **no string pattern matching on capability intent**. Path/arg values are checked, not the user's original message.

Validation:

```bash
python -c "
from src.core.safety.classifier import SafetyClassifier
from src.core.decision.output import RiskLevel
sc = SafetyClassifier()
assert sc.classify('web_search', {'query': 'python'}) == RiskLevel.low
assert sc.classify('file_ops', {'action': 'read', 'path': '/etc/passwd'}) == RiskLevel.high
assert sc.classify('file_ops', {'action': 'read', 'path': '../../../etc/shadow'}) == RiskLevel.high
print('SafetyClassifier OK')
"
```

Artifact: `src/core/safety/classifier.py`

---

### TASK 6.3 — Mode Enforcer

Location:

- `src/core/safety/mode_enforcer.py`

Steps:

1. Create `src/core/safety/mode_enforcer.py`.
2. Define `Permission(str, Enum)`: `allow`, `confirm`, `block`.
3. Define `ModeEnforcer` class.
4. Implement `check_permission(capability_name: str, risk_level: RiskLevel, mode: str) -> Permission`:
   ```
   SAFE:           all → confirm
   BALANCED:       low → allow
                   medium → confirm
                   high → block (phrase "I understand the risk" in args unlocks to confirm)
   UNRESTRICTED:   all → allow (schema/path validation still applies independently)
   ```
5. The override phrase for BALANCED high-risk is checked against a special `_override_phrase` field in args if present.
6. Publish `EVT_SAFETY_BLOCK` to EventBus when `block` is returned.

Validation:

```bash
python -c "
from src.core.safety.mode_enforcer import ModeEnforcer, Permission
from src.core.decision.output import RiskLevel
me = ModeEnforcer()
assert me.check_permission('open_app', RiskLevel.low, 'BALANCED') == Permission.allow
assert me.check_permission('open_app', RiskLevel.medium, 'BALANCED') == Permission.confirm
assert me.check_permission('code_exec', RiskLevel.high, 'BALANCED') == Permission.block
assert me.check_permission('code_exec', RiskLevel.high, 'SAFE') == Permission.confirm
assert me.check_permission('code_exec', RiskLevel.high, 'UNRESTRICTED') == Permission.allow
print('ModeEnforcer OK')
"
```

Artifact: `src/core/safety/mode_enforcer.py`

---

### TASK 6.4 — Permission Layer (Three-Gate System)

Location:

- `src/core/safety/permission.py`

Steps:

1. Create `src/core/safety/permission.py`.
2. Define `GateResult(str, Enum)`: `pass_`, `fail`.
3. Define `PermissionLayer` class.
4. Implement `check(tool_name: str, args: dict, decision: DecisionOutput, mode: str) -> tuple[Permission, str]`:
   - **Gate 1 — Decision Consistency**: `tool_name == decision.tool_name` → pass. Mismatch → fail, reason="tool mismatch with decision".
   - **Gate 2 — Argument Safety**: run `SafetyClassifier().classify(tool_name, args)` → get risk. Run `ModeEnforcer().check_permission(tool_name, risk, mode)` → get permission.
   - **Gate 3 — Schema Validity**: run `SchemaValidator().validate(tool_name, args)` → if not valid → fail, reason=errors.
   - Any gate fail → return `(block, reason)`.
   - All gates pass → return `(permission_from_gate2, "")`.
5. Log each gate result to AuditLogger.

Artifact: `src/core/safety/permission.py`

---

### TASK 6.5 — Audit Logger

Location:

- `src/core/safety/audit.py`

Steps:

1. Create `src/core/safety/audit.py`.
2. Define `AuditLogger` class with SQLite backend at `config.paths.audit_db`.
3. Schema:
   ```sql
   CREATE TABLE IF NOT EXISTS audit_log (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       timestamp TEXT NOT NULL,
       session_id TEXT NOT NULL,
       turn_id INTEGER,
       tool_name TEXT,
       args TEXT,         -- JSON string
       gate1 TEXT,
       gate2 TEXT,
       gate3 TEXT,
       final_decision TEXT,
       reason TEXT
   )
   ```
4. Implement `log_action(tool_name, args, gate_results: dict, decision: str, session_id, turn_id, reason="") -> None`.
5. Implement `get_audit_log(session_id: str, limit: int = 50) -> list[dict]`.
6. Thread-safe writes via SQLite WAL mode.

Validation:

```bash
python -c "
from src.core.safety.audit import AuditLogger
al = AuditLogger()
al.log_action('open_app', {'name':'notepad'}, {'gate1':'pass','gate2':'allow','gate3':'pass'}, 'allow', 's1', 1)
log = al.get_audit_log('s1', 10)
assert len(log) >= 1
assert log[-1]['tool_name'] == 'open_app'
print('AuditLogger OK')
"
```

Artifact: `src/core/safety/audit.py`

---

### TASK 6.6 — Schema Validator (Full Implementation)

Location:

- `src/capabilities/validator.py` (expand TASK 2.0 stub)

Steps:

1. Expand `src/capabilities/validator.py`.
2. Load `config/capabilities.yaml` at class instantiation.
3. Build lookup: `{capability_name: input_schema_dict}`.
4. Implement `validate(capability_name: str, args: dict) -> ValidationResult`:
   - If capability not in manifest → return `ValidationResult(valid=False, errors=["unknown capability"])`.
   - For each field in `input_schema`:
     - If `required=True` and key absent from args → append `"field '{name}' is required"`.
     - If `type=string` and value not str → append `"field '{name}' must be string"`.
     - If `enum` defined and value not in enum → append `"field '{name}' must be one of {enum}"`.
   - Return `ValidationResult(valid=len(errors)==0, errors=errors)`.

Validation:

```bash
python -c "
from src.capabilities.validator import SchemaValidator
sv = SchemaValidator()
r = sv.validate('open_app', {'name': 'notepad'})
assert r.valid
r2 = sv.validate('open_app', {})
assert not r2.valid and 'name' in r2.errors[0]
print('SchemaValidator OK')
"
```

---

### TASK 6.7 — Safety Tests

Location:

- `tests/test_safety.py`

Tests:

1. SAFE mode confirms all risk levels.
2. BALANCED low → allow.
3. BALANCED medium → confirm.
4. BALANCED high → block.
5. UNRESTRICTED high → allow.
6. Path traversal `..` classified as high.
7. Blocked path `/etc/passwd` classified as high.
8. Three gates: gate 1 fail (tool mismatch) → block.
9. Three gates: gate 3 fail (missing required arg) → block.
10. Audit log records entry after each check.
11. Schema validator rejects missing required field.
12. Schema validator rejects invalid enum value.

Validation:

```bash
pytest tests/test_safety.py -v
```

Artifact: `tests/test_safety.py`

---

### Definition of Done — Phase 6

Three-gate permission system enforced. Sandbox runs with timeout. Schema validation rejects invalid args. Audit log records all actions. All tests pass.

---

## 🧩 Phase 7 — Memory Engine

```yaml
phase_id: 7
priority: "P1"
total_tasks: 6
blocker: "Phase 6 complete"
```

---

### TASK 7.1 — Memory Database

Location:

- `src/memory/database.py`

Steps:

1. Create `src/memory/database.py`.
2. Define `MemoryDB` class with SQLite at `config.paths.memory_db`.
3. Schema:

   ```sql
   CREATE TABLE IF NOT EXISTS turns (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       session_id TEXT NOT NULL,
       turn_number INTEGER,
       user_message TEXT,
       assistant_response TEXT,
       model TEXT,
       timestamp TEXT,
       trace_id TEXT
   );

   CREATE TABLE IF NOT EXISTS memory_snippets (
       id TEXT PRIMARY KEY,
       session_id TEXT,
       content TEXT,
       keywords TEXT,     -- comma-separated
       created_at TEXT,
       expires_at TEXT,
       interaction_count INTEGER DEFAULT 0,
       relevance_score REAL DEFAULT 1.0
   );

   CREATE INDEX IF NOT EXISTS idx_turns_session ON turns(session_id);
   CREATE INDEX IF NOT EXISTS idx_snippets_session ON memory_snippets(session_id);
   ```

4. Use WAL journal mode for concurrent reads.
5. Implement `store(session_id: str, turn_data: dict) -> None`.
6. Implement `retrieve_recent(session_id: str, limit: int = 5) -> list[dict]` — newest first.
7. Implement `search_snippets(keywords: list[str]) -> list[dict]`.
8. Implement `store_snippet(snippet: dict) -> None`.
9. Implement `get_connection() -> sqlite3.Connection` with connection pooling (thread-local).
10. Handle corrupted DB: `sqlite3.DatabaseError` on open → rename corrupted file, create fresh DB, log WARNING.
11. Implement `get_schema_version() -> int` and `set_schema_version(v: int)` using `PRAGMA user_version` for future migration support.

Validation:

```bash
python -c "
import tempfile, os
from src.memory.database import MemoryDB
with tempfile.TemporaryDirectory() as d:
    db = MemoryDB(db_path=os.path.join(d, 'test.db'))
    db.store('s1', {'user_message': 'hello', 'assistant_response': 'hi', 'model': 'gemma3:4b', 'turn_number': 1})
    recent = db.retrieve_recent('s1', 5)
    assert len(recent) == 1
    assert recent[0]['user_message'] == 'hello'
    print('MemoryDB OK')
"
```

Artifact: `src/memory/database.py`

---

### TASK 7.2 — Memory Scorer

Location:

- `src/memory/scorer.py`

Steps:

1. Create `src/memory/scorer.py`.
2. Define `MemoryScorer` class.
3. Implement `score(snippet: dict, query: str) -> float`:

   ```python
   keywords = set(snippet.get('keywords', '').lower().split(','))
   query_words = set(query.lower().split())
   overlap = len(keywords & query_words) / max(len(query_words), 1)

   age_hours = (datetime.utcnow() - datetime.fromisoformat(snippet['created_at'])).seconds / 3600
   recency = max(0.0, 1.0 - (age_hours / 168.0))  # linear decay over 7 days

   interactions = min(snippet.get('interaction_count', 0) / 10.0, 1.0)  # cap at 10

   score = 0.5 * overlap + 0.3 * recency + 0.2 * interactions
   return round(score, 4)
   ```

4. Scores are always in [0.0, 1.0].

Validation:

```bash
python -c "
from datetime import datetime
from src.memory.scorer import MemoryScorer
ms = MemoryScorer()
snippet = {'keywords': 'python,code,programming', 'created_at': datetime.utcnow().isoformat(), 'interaction_count': 3}
score = ms.score(snippet, 'python programming')
assert 0.0 <= score <= 1.0
print(f'Score: {score}')
"
```

Artifact: `src/memory/scorer.py`

---

### TASK 7.3 — TTL and Decay Manager

Location:

- `src/memory/ttl.py`

Steps:

1. Create `src/memory/ttl.py`.
2. Define `TTLManager` class with `MemoryDB` dependency.
3. Define constants: `SHORT_TERM_TTL_HOURS = 24`, `LONG_TERM_TTL_DAYS = 30`.
4. Implement `set_ttl(snippet_id: str, ttl_hours: int) -> None` — updates `expires_at` in DB.
5. Implement `get_expired_ids() -> list[str]` — SELECT where `expires_at < now`.
6. Implement `apply_decay(decay_factor: float = 0.95) -> None` — UPDATE `relevance_score = relevance_score * decay_factor` where age > 24 hours.
7. Implement `cleanup() -> int` — DELETE expired entries, return count deleted.
8. `cleanup()` is called by a background thread launched at startup (every 1 hour).

Artifact: `src/memory/ttl.py`

---

### TASK 7.4 — Keyword Indexer

Location:

- `src/memory/indexer.py`

Steps:

1. Create `src/memory/indexer.py`.
2. Define `KeywordIndexer` class backed by SQLite table `keyword_index`:
   ```sql
   CREATE TABLE IF NOT EXISTS keyword_index (
       keyword TEXT NOT NULL,
       snippet_id TEXT NOT NULL,
       PRIMARY KEY (keyword, snippet_id)
   );
   ```
3. Implement `index(snippet_id: str, keywords: list[str]) -> None`.
4. Implement `lookup(keyword: str) -> list[str]` — returns snippet_ids.
5. Implement `remove(snippet_id: str) -> None` — for cleanup when snippet expires.
6. Implement `rebuild_index() -> None` — drop + recreate from snippets table. Not called on every write — called by `cleanup()` daily.

Validation:

```bash
python -c "
import tempfile, os
from src.memory.indexer import KeywordIndexer
with tempfile.TemporaryDirectory() as d:
    ki = KeywordIndexer(db_path=os.path.join(d, 'idx.db'))
    ki.index('snip_001', ['python', 'code'])
    results = ki.lookup('python')
    assert 'snip_001' in results
    print('KeywordIndexer OK')
"
```

Artifact: `src/memory/indexer.py`

---

### TASK 7.5 — Context Retriever

Location:

- `src/memory/retriever.py`

Steps:

1. Create `src/memory/retriever.py`.
2. Define `ContextRetriever` class.
3. Implement `get_context(session_id: str, query: str, limit: int = 5) -> list[dict]`:
   a. Fetch recent turns: `MemoryDB().retrieve_recent(session_id, limit=limit)`.
   b. Extract keywords from query: simple split + stop-word removal.
   c. Look up snippets via `KeywordIndexer().lookup(keyword)` for each keyword.
   d. Deduplicate snippet_ids.
   e. Fetch each snippet from DB.
   f. Score each via `MemoryScorer().score(snippet, query)`.
   g. Sort by score descending.
   h. Return top `limit` snippets.
4. Cold start (no DB entries) → return `[]`, no error.
5. Update `interaction_count` for any retrieved snippet.

Artifact: `src/memory/retriever.py`

---

### TASK 7.6 — Memory Tests

Location:

- `tests/test_memory.py`

Tests:

1. `MemoryDB.store` persists turn.
2. `MemoryDB.retrieve_recent` returns correct count, newest first.
3. Cold start returns empty list.
4. `MemoryScorer` scores relevant snippet > irrelevant snippet.
5. `MemoryScorer` score always in [0.0, 1.0].
6. `KeywordIndexer.index` → `lookup` returns correct IDs.
7. `TTLManager.get_expired_ids` returns expired entries.
8. `TTLManager.cleanup` removes expired, returns count.
9. `ContextRetriever.get_context` returns sorted results.
10. `ContextRetriever` cold start returns empty list.

Validation:

```bash
pytest tests/test_memory.py -v
```

Artifact: `tests/test_memory.py`

---

### Definition of Done — Phase 7

Memory stores, retrieves, scores, and expires. ContextRetriever returns relevant snippets. All tests pass.

---

## ⚡ Phase 8 — Capability System

```yaml
phase_id: 8
priority: "P1"
total_tasks: 6
blocker: "Phase 7 complete"
```

---

### TASK 8.1 — `BaseCapability` Abstract Class

Location:

- `src/capabilities/base.py` ✅ **IMPLEMENTED**

Status: **Completed in Phase 0**

- `BaseCapability(ABC)` defined with `execute()`, `validate_args()`, `dry_run()` methods
- `CapabilityResult` dataclass defined for returning execution results
- Concrete implementation: `AppLauncher` in `src/capabilities/system/apps.py`

Artifact: `src/capabilities/base.py`, `src/capabilities/system/apps.py`

---

### TASK 8.2 — Capability Registry

Location:

- `src/capabilities/registry.py`

Steps:

1. Create `src/capabilities/registry.py`.
2. Define `CapabilityRegistry` as a singleton.
3. Implement `register(capability: BaseCapability) -> None`:
   - Reject if `capability.name` already registered → raise `ValueError`.
4. Implement `get(name: str) -> BaseCapability | None`.
5. Implement `list_all() -> list[str]`.
6. Implement `load_from_manifest(manifest_path: str = "config/capabilities.yaml") -> None`:
   - For each entry in manifest: import `module_path`, instantiate, call `register()`.
   - Log failures with WARNING (missing module does not crash registry).

Artifact: `src/capabilities/registry.py`

---

### TASK 8.3 — Capability Executor

Location:

- `src/capabilities/executor.py` ✅ **IMPLEMENTED**

Status: **Completed in Phase 0**

- `CapabilityExecutor` class defined with `execute()` and `dry_run()` methods
- Returns `ToolResult` contracts
- Integrates with `BaseCapability` and `ToolResult`
- Note: Gates 3-6 (PermissionLayer, Sandbox, EventBus) to be added in Phase 6-7

Artifact: `src/capabilities/executor.py`

---

### TASK 8.4 — Capability Validation Tests

Location:

- `tests/test_capabilities.py`

Tests:

1. `BaseCapability` subclass missing `execute` → `TypeError`.
2. Registry `register` + `get` round trip.
3. Registry rejects duplicate name.
4. Registry `get` unknown name → None.
5. `CapabilityExecutor` rejects unknown capability (gate 1).
6. `CapabilityExecutor` rejects bad args (gate 2).
7. `CapabilityExecutor` respects BALANCED block for high-risk (gate 3).
8. `CapabilityExecutor` dry_run returns result with `dry_run=True`.

Validation:

```bash
pytest tests/test_capabilities.py -v
```

Artifact: `tests/test_capabilities.py`

---

### TASK 8.5 — Sandbox Tests

Location:

- `tests/test_sandbox.py`

Tests:

1. Sandbox enforces timeout (mock slow capability).
2. Sandbox catches and wraps capability exceptions as `ToolResult.failure`.
3. Dry-run returns result without calling `execute`.
4. Duration recorded in `ToolResult.duration_ms`.

Validation:

```bash
pytest tests/test_sandbox.py -v
```

Artifact: `tests/test_sandbox.py`

---

### TASK 8.6 — Observability Tests

Location:

- `tests/test_observability.py`

Tests:

1. `MetricsCollector` records latency and returns in summary.
2. `MetricsCollector.reset()` clears state.
3. `EventBus` delivers events to all subscribers.
4. `EventBus` isolates callback exceptions from publisher.
5. `EVT_TOOL_EXECUTED` published after capability execution.
6. `EVT_STATE_TRANSITION` published on state change.

Validation:

```bash
pytest tests/test_observability.py -v
```

Artifact: `tests/test_observability.py`

---

### Definition of Done — Phase 8

Full capability pipeline operational. All gates enforced. EventBus integrated. All tests pass.

---

## 🖥️ Phase 9 — System Control Capabilities

```yaml
phase_id: 9
priority: "P1"
total_tasks: 8
blocker: "Phase 8 complete"
```

### BREAKING CHANGE NOTICE

Phase 0 `AppLauncher.open_app(name)` interface is replaced by `AppLauncher.execute({"name": name})` here. After TASK 9.1, update `app/jarvis_slice.py` to use the new interface.

---

### TASK 9.1 — App Launcher Capability (Full)

Location:

- `src/capabilities/system/apps.py` (replace Phase 0 stub)

Steps:

1. **Replace** the Phase 0 `AppLauncher` entirely. The new class inherits `BaseCapability`.
2. Class attributes: `name = "open_app"`, `domain = "system"`, `description = "Launch application by name"`.
3. Implement `validate(args) -> ValidationResult`:
   - Check `"name"` key present and non-empty.
   - Check name not in `config.safety.blocked_apps` list.
4. Implement `get_risk_level() -> RiskLevel`: return `RiskLevel.medium`.
5. Implement `execute(args: dict) -> ToolResult`:
   - `name = args["name"]`
   - **Windows**: search PATH → `%APPDATA%\Microsoft\Windows\Start Menu` → `C:\Program Files` → `C:\Program Files (x86)`. Use `subprocess.Popen(executable)`.
   - **Linux**: search PATH via `shutil.which(name)` → `/usr/share/applications/*.desktop` parsing.
   - **macOS**: search PATH → `/Applications/{name}.app` → `open -a {name}`.
   - Case-insensitive match.
   - On success: return `ToolResult(tool="open_app", success=True, data={"pid": process.pid, "name": name})`.
   - On not found: return `ToolResult.failure("open_app", f"Application not found: {name}")`.
6. Implement `dry_run(args) -> ToolResult`: return `ToolResult(tool="open_app", success=True, data={"would_launch": args.get("name")}, dry_run=True)`.
7. Update `app/jarvis_slice.py` to call `AppLauncher().execute({"name": app_name})` instead of `open_app(app_name)`.

Artifact: `src/capabilities/system/apps.py`

---

### TASK 9.2 — System Info Capability

Location:

- `src/capabilities/system/sysinfo.py`

Steps:

1. Create `src/capabilities/system/sysinfo.py`. Inherit `BaseCapability`. `name = "system_info"`.
2. `execute(args)`:
   - `info_type = args.get("info_type", "all")`
   - CPU: `psutil.cpu_percent(interval=1)`, `psutil.cpu_freq()`, `platform.processor()`.
   - RAM: `psutil.virtual_memory().total/used/percent`.
   - GPU: `VRAMMonitor().get_available_vram_mb()` and `get_total_vram_mb()`.
   - OS: `platform.system()`, `platform.release()`, `platform.version()`.
   - Return `ToolResult(success=True, data={"cpu": ..., "ram": ..., "gpu": ..., "os": ...})`.
3. `get_risk_level()` → `RiskLevel.low`.

Artifact: `src/capabilities/system/sysinfo.py`

---

### TASK 9.3 — Clipboard Capability

Location:

- `src/capabilities/system/clipboard.py`

Steps:

1. Create. Inherit `BaseCapability`. `name = "clipboard"`.
2. `execute(args)`:
   - `action = args["action"]`
   - `read`: `content = pyperclip.paste()` → return `ToolResult(success=True, data={"content": content})`.
   - `write`: `pyperclip.copy(args["content"])` → return `ToolResult(success=True, data={})`.
3. `get_risk_level()` → `RiskLevel.low`.

Artifact: `src/capabilities/system/clipboard.py`

---

### TASK 9.4 — Notifications Capability

Location:

- `src/capabilities/notify/toasts.py`

Steps:

1. Create. Inherit `BaseCapability`. `name = "notify"`.
2. `execute(args)`:
   - Use `plyer.notification.notify(title=..., message=..., timeout=args.get("duration",5))`.
   - Fallback (plyer unavailable): log notification to console with `[NOTIFY]` prefix.
3. `get_risk_level()` → `RiskLevel.low`.

Artifact: `src/capabilities/notify/toasts.py`

---

### TASK 9.5 — Screenshot Capability

Location:

- `src/capabilities/screen/capture.py`

Steps:

1. Create. Inherit `BaseCapability`. `name = "screenshot"`.
2. `execute(args)`:
   - Use `PIL.ImageGrab.grab()` (or `mss` for multi-monitor).
   - Save to `data/screenshots/{timestamp}.png`.
   - If `args.get("ocr")`: run `pytesseract.image_to_string(img)`, return text in `data.ocr_text`.
   - Return `ToolResult(success=True, data={"path": str(save_path), "ocr_text": ...})`.
3. `get_risk_level()` → `RiskLevel.low`.

Artifact: `src/capabilities/screen/capture.py`

---

### TASK 9.6 — File Operations Capability

Location:

- `src/capabilities/files/file_ops.py`

Steps:

1. Create. Inherit `BaseCapability`. `name = "file_ops"`.
2. `validate(args)`:
   - Check `action` in allowed enum.
   - Check `path` is within an `allowed_root` from config (use `Path.resolve()` to prevent traversal).
3. `execute(args)`:
   - `list`: `Path(path).iterdir()` → return file names, sizes, types.
   - `read`: `Path(path).read_text(encoding="utf-8")` → return content.
   - `write`: `Path(path).write_text(args["content"])`.
   - `delete`: `Path(path).unlink()`.
   - `move`: `shutil.move(src, dst)`.
   - `copy`: `shutil.copy2(src, dst)`.
   - All operations return `ToolResult`.
4. `get_risk_level()` → dynamically: delete/write/move → `medium`; read/list → `low`.

Artifact: `src/capabilities/files/file_ops.py`

---

### TASK 9.7 — Code Executor Capability

Location:

- `src/capabilities/coder/executor.py`

Steps:

1. Create `src/capabilities/coder/executor.py`. Inherit `BaseCapability`. `name = "code_exec"`.
2. `validate(args)`:
   - Check `language` in `["python", "javascript", "bash"]`.
   - Check `code` not empty.
   - Check code does not contain `__import__('os').system`, raw `import subprocess` (baseline check — not exhaustive).
3. `execute(args)`:
   - Write code to `tempfile.NamedTemporaryFile`.
   - `python`: `subprocess.run(["python", tmpfile], capture_output=True, timeout=30, cwd=tempdir)`.
   - `javascript`: `subprocess.run(["node", tmpfile], capture_output=True, timeout=30, cwd=tempdir)`.
   - `bash`: `subprocess.run(["bash", tmpfile], capture_output=True, timeout=30, cwd=tempdir)`.
   - Return `ToolResult(success=returncode==0, data={"stdout": stdout, "stderr": stderr, "returncode": returncode})`.
4. `get_risk_level()` → `RiskLevel.high`.

Artifact: `src/capabilities/coder/executor.py`

---

### TASK 9.8 — Web Search Capability

Location:

- `src/capabilities/search/web_search.py`

Steps:

1. Create. Inherit `BaseCapability`. `name = "web_search"`.
2. `execute(args)`:
   - Use DuckDuckGo HTML endpoint: `GET https://html.duckduckgo.com/html/?q={query}`.
   - Parse with BeautifulSoup: extract `.result__title`, `.result__url`, `.result__snippet`.
   - Return top `args.get("count", 5)` results as list of `{"title": ..., "url": ..., "snippet": ...}`.
   - On network error: return `ToolResult.failure("web_search", "network unavailable")`.
3. `get_risk_level()` → `RiskLevel.low`.
4. Set `User-Agent` header to avoid bot blocks.

Artifact: `src/capabilities/search/web_search.py`

---

### Definition of Done — Phase 9

All 8 capabilities implemented, inherit `BaseCapability`, return `ToolResult`. `dry_run` implemented. `app/jarvis_slice.py` updated to new `execute()` interface.

---

## 💬 Phase 10 — Prompt Builder

```yaml
phase_id: 10
priority: "P1"
total_tasks: 5
blocker: "Phase 9 complete"
```

---

### TASK 10.1 — Jarvis Identity YAML

Location:

- `config/jarvis_identity.yaml`

Steps:

1. Create `config/jarvis_identity.yaml`:
   ```yaml
   name: JARVIS
    version: "3.0"
   role: "Local-first AI assistant for desktop control and automation"
   languages: [en, ar]
   personality:
     tone: "professional, direct, no filler phrases"
     verbosity: "concise"
     confirmation_style: "explicit"
   capabilities_summary: "system control, file operations, web automation, voice, vision, integrations"
   constraints:
     - "Never invent capabilities you do not have"
     - "Always report failures explicitly"
     - "Do not hallucinate file paths or application names"
     - "Respect execution mode restrictions"
   local_first: true
   cloud_fallback: false
   ```

Validation:

```bash
python -c "import yaml; i=yaml.safe_load(open('config/jarvis_identity.yaml')); assert i['name']=='JARVIS'; print('Identity OK')"
```

Artifact: `config/jarvis_identity.yaml`

---

### TASK 10.2 — Mode Fragments YAML

Location:

- `config/mode_fragments.yaml`

Steps:

1. Create `config/mode_fragments.yaml` with exactly 5 fragments (fast, normal, deep, planning, research):
   ```yaml
   fragments:
     fast:
       system_addition: "Respond concisely. Prioritize speed. Omit unnecessary explanation."
       output_format: "plain text, 1-3 sentences max"
       behavior: "no chain-of-thought, direct answer"
     normal:
       system_addition: "Balance detail with clarity. Explain your reasoning briefly."
       output_format: "plain text, structured if helpful"
       behavior: "standard response depth"
     deep:
       system_addition: "Provide thorough analysis. Explore edge cases. Be comprehensive."
       output_format: "structured prose with sections if needed"
       behavior: "full chain-of-thought"
     planning:
       system_addition: "Break the task into steps. Enumerate each action. Verify feasibility."
       output_format: "numbered steps"
       behavior: "planning-focused, tool calls encouraged"
     research:
       system_addition: "Gather and synthesize information. Cite sources when possible."
       output_format: "structured report"
       behavior: "search-first, citation-aware"
   ```

Validation:

```bash
python -c "import yaml; f=yaml.safe_load(open('config/mode_fragments.yaml')); assert len(f['fragments'])==5; print('Fragments OK')"
```

Artifact: `config/mode_fragments.yaml`

---

### TASK 10.3 — System Prompt Builder

Location:

- `src/core/context/builder.py`

Steps:

1. Create `src/core/context/builder.py`.
2. Define `PromptBuilder` class. Load identity and fragments at instantiation.
3. Implement `build(decision: DecisionOutput, input_packet: InputPacket) -> str`:
   a. Load identity YAML.
   b. Identity block: `f"You are {identity['name']}, {identity['role']}. Constraints: {'; '.join(identity['constraints'])}."`.
   c. Mode fragment: load `fragments[decision.mode.value]` → append `system_addition`.
   d. Context block: if `input_packet.memory_snippets` non-empty → `"Relevant context:\n" + snippets`.
   e. History block: last 3 turns formatted as `"User: ...\nJARVIS: ..."`.
   f. Language hint: if `input_packet.user_profile.language == "ar"` → append `"Respond in Arabic."`.
   g. Return concatenated prompt string.
4. `build()` is called by `Executor.execute()` before every LLM call.
5. Replace the stub `system` string in `Executor.execute()` with `PromptBuilder().build(decision, input_packet)`.

Artifact: `src/core/context/builder.py`

---

### TASK 10.4 — Wire `PromptBuilder` into `Executor`

Location:

- `src/core/runtime/executor.py` (expand TASK 4.5)

Steps:

1. Import `PromptBuilder` from `src.core.context.builder`.
2. Add `self._prompt_builder = PromptBuilder()` to `Executor.__init__`.
3. In `execute()`: `system_prompt = self._prompt_builder.build(decision, input_packet)` before LLM call.
4. Pass `system_prompt` to `OllamaEngine().chat_with_model()`.

---

### TASK 10.5 — Identity Enforcement Tests

Location:

- `tests/test_identity_enforcement.py`

Tests:

1. `PromptBuilder.build()` output contains identity name "JARVIS".
2. Prompt contains mode fragment for `fast` mode.
3. Prompt contains mode fragment for `deep` mode.
4. Arabic profile → prompt contains "Respond in Arabic".
5. Memory snippets non-empty → prompt contains context block.
6. History → prompt contains prior turns.
7. All 5 modes produce non-empty prompts.

Validation:

```bash
pytest tests/test_identity_enforcement.py -v
```

Artifact: `tests/test_identity_enforcement.py`

---

### Definition of Done — Phase 10

Prompt builder produces identity-aware, mode-specific prompts. All LLM calls include JARVIS identity. All tests pass.

---

## 🔩 Phase 11 — Execution Hardening

```yaml
phase_id: 11
priority: "P0"
total_tasks: 6
blocker: "Phase 10 complete"
```

---

### TASK 11.1 — Timeout Handler

Location:

- `src/core/runtime/timeout.py`

Steps:

1. Create `src/core/runtime/timeout.py`.
2. Define `TimeoutHandler` class with `Limits` dependency.
3. Implement `check(phase: str, start_time: float) -> None`:
   - Computes elapsed: `time.time() - start_time`.
   - Maps phase → limit: `{"tool": limits.tool_timeout_s, "step": limits.step_timeout_s, "model": limits.model_timeout_s, "turn": limits.total_turn_timeout_s}`.
   - If elapsed >= threshold: log EVT_DEGRADATION, raise `TurnTimeoutError(f"{phase} timeout after {elapsed:.1f}s")`.
4. Implement as context manager:
   ```python
   @contextmanager
   def phase_timeout(self, phase: str):
       start = time.time()
       try:
           yield
       finally:
           self.check(phase, start)
   ```

Artifact: `src/core/runtime/timeout.py`

---

### TASK 11.2 — Graceful Degradation

Location:

- `src/core/runtime/degradation.py`

Steps:

1. Create `src/core/runtime/degradation.py`.
2. Define `DegradationHandler` class.
3. Implement `handle_model_failure(model: str, error: Exception) -> str | None`:
   - Log error.
   - Publish `EVT_DEGRADATION` to EventBus.
   - Return next fallback model from config `fallback_chain`, cycling through tier_1 → tier_2.
   - If all fallbacks exhausted → return None.
4. Implement `handle_tool_failure(tool: str, error: Exception) -> None`:
   - Log warning — do NOT crash.
   - Publish `EVT_SAFETY_BLOCK` if it was a permission failure.
5. Implement `generate_error_response(error_type: str, detail: str = "") -> str`:
   - `"model_unavailable"` → `"I'm unable to process that right now — model unavailable. Please try again."`.
   - `"timeout"` → `"That took too long. Please try a simpler request."`.
   - `"permission_denied"` → `"That action requires elevated permission or approval."`.
   - `"budget_exhausted"` → `"I've reached my retry limit for this request."`.
6. Track `_degraded: bool` state. `is_degraded() -> bool`.

Artifact: `src/core/runtime/degradation.py`

---

### TASK 11.3 — Tiered Fallback System

Location:

- `src/core/runtime/fallback.py`

Steps:

1. Create `src/core/runtime/fallback.py`.
2. Define `FallbackSystem` class.
3. Load `fallback.tier_1` and `fallback.tier_2` from `config/models.yaml`.
4. Implement `attempt(input_packet: InputPacket, tier: int, decision: DecisionOutput) -> FinalResponse`:
   - Tier 1: force `decision.model = config.fallback.tier_1`. Call `Executor().execute(decision, input_packet)`. Return FinalResponse.
   - Tier 2: force `decision.model = config.fallback.tier_2`. Call `Executor().execute()`. Return FinalResponse.
   - Both: set `FinalResponse.degraded = True`.
5. Called by `DegradationHandler` when primary model fails.
6. Tier 1 is always attempted before Tier 2 — enforced by caller in `run_turn()`.

Artifact: `src/core/runtime/fallback.py`

---

### TASK 11.4 — Retry Manager

Location:

- `src/core/runtime/retry.py`

Steps:

1. Create `src/core/runtime/retry.py`.
2. Define `RetryManager` class (per-turn instance, not singleton).
3. `_budget: int = limits.global_retry_budget` (8 default).
4. Implement `consume(n: int = 1) -> int`:
   - Decrement `_budget` by n.
   - Log remaining budget.
   - Return remaining.
5. Implement `can_retry() -> bool` → `self._budget > 0`.
6. Implement `reset() -> None` → `self._budget = limits.global_retry_budget`.
7. `RetryManager` is instantiated fresh per `run_turn()` call.
8. `run_turn()` passes `retry_manager` to all sub-calls that need to retry. Each retry consumes budget.

Validation:

```bash
python -c "
from src.core.runtime.retry import RetryManager
rm = RetryManager()
for _ in range(8):
    rm.consume()
assert not rm.can_retry()
rm.reset()
assert rm.can_retry()
print('RetryManager OK')
"
```

Artifact: `src/core/runtime/retry.py`

---

### TASK 11.5 — Decision Validation Enforcer

Location:

- `src/core/runtime/validate_decision.py`

Steps:

1. Create `src/core/runtime/validate_decision.py`.
2. Define `DecisionEnforcer` class.
3. Implement `validate(decision: DecisionOutput) -> bool`:
   - If `decision_source == model`:
     - `score_breakdown` must be non-empty dict → False if not.
     - `candidate_list` must be non-empty list → False if not.
   - `model` must be in `ModelAvailability().get_available_models()` → False if not (log WARNING).
   - `confidence` must be `>= 0.3` → if lower, log WARNING but do NOT reject (low confidence is valid data).
   - Return True if all checks pass.
4. If `validate()` returns False: caller (`run_turn()`) uses `_safe_default()` from decision module. Do NOT retry — invalid decision is replaced immediately.

Artifact: `src/core/runtime/validate_decision.py`

---

### TASK 11.6 — Integration Tests

Location:

- `tests/test_integration.py`

Tests:

1. `run_turn("hello", "s1")` → FinalResponse with non-empty text.
2. `run_turn("open notepad", "s1")` → fast path, tool_use decision.
3. Mock slow model → timeout fires → degraded FinalResponse (no crash).
4. Mock model failure → fallback chain activates (tier_1 tried first).
5. Retry budget: mock all models fail → budget exhausted → FinalResponse with error text.
6. Safety: `run_turn("delete /etc/passwd", "s1")` → ToolResult failure (permission denied).
7. Memory: two turns → second turn has `recent_history` from first.
8. State machine: all transitions logged to EventBus.
9. Mode SAFE: every tool requires confirmation (mock confirmation signal).
10. `run_turn` never raises an uncaught exception regardless of failures.

Validation:

```bash
pytest tests/test_integration.py -v
```

Artifact: `tests/test_integration.py`

---

### Definition of Done — Phase 11

Runtime handles all failure modes. Fallback chain works. Budget enforced. `run_turn` never crashes. All integration tests pass.

---

## 💻 Phase 12 — CLI Interface

```yaml
phase_id: 12
priority: "P2"
total_tasks: 3
blocker: "Phase 11 complete"
```

---

### TASK 12.1 — CLI Chat Loop

Location:

- `src/interfaces/cli/chat.py`

Steps:

1. Create `src/interfaces/cli/chat.py`.
2. Define `CLIChat` class.
3. Implement `start() -> None`:
   - Print banner: `"JARVIS v3.0 — type /help for commands"`.
   - Loop: `input("You: ")` → strip → if empty continue → if starts with `/` → dispatch to `CommandHandler` → else call `run_turn(message, session_id)` → print `FinalResponse`.
4. `session_id` = UUIDv4 generated at `start()` time, persisted for session duration.
5. Wire `signal.SIGINT` → graceful exit: print `"\nGoodbye."`, `sys.exit(0)`.
6. Check `_shutdown` flag from `app/main.py` signal handler in loop condition.
7. Print thinking indicator during `run_turn()`: `print("Thinking...", end="\r")`.

Artifact: `src/interfaces/cli/chat.py`

---

### TASK 12.2 — CLI Command Handlers

Location:

- `src/interfaces/cli/commands.py`

Steps:

1. Create `src/interfaces/cli/commands.py`.
2. Define `CommandHandler` class.
3. Commands:
   - `/help` → print all commands.
   - `/mode SAFE|BALANCED|UNRESTRICTED` → call `update_mode(user_id, mode)`, print confirmation.
   - `/replay [turn_id]` → fetch from AuditLogger or StateManager history, print.
   - `/debug` → toggle debug logging level.
   - `/status` → print: current model, mode, VRAM available, session_id, turn count.
   - `/quit` → `sys.exit(0)`.
4. Invalid mode value → print error and current mode.
5. All commands start with `/` and are case-insensitive.

Artifact: `src/interfaces/cli/commands.py`

---

### TASK 12.3 — CLI Formatting

Location:

- `src/interfaces/cli/formatting.py`

Steps:

1. Create `src/interfaces/cli/formatting.py`.
2. Define `CLIFormatter` class.
3. Implement `format_response(response: FinalResponse) -> str`:
   - Use colorama: `Fore.CYAN` for JARVIS prefix, `Fore.WHITE` for text, `Style.RESET_ALL`.
   - If `response.degraded`: prefix `[DEGRADED]` in `Fore.YELLOW`.
   - If `response.tool_results`: print each tool result summary.
4. Implement `format_tool_result(result: ToolResult) -> str`:
   - Success: `Fore.GREEN + f"✓ {result.tool}: {result.data}"`.
   - Failure: `Fore.RED + f"✗ {result.tool}: {result.error}"`.
5. Arabic RTL: print Arabic content preceded by Unicode RLM mark `\u200f`.

Artifact: `src/interfaces/cli/formatting.py`

---

### Definition of Done — Phase 12

Full CLI chat loop operational. All commands functional. Formatting readable. Arabic displays correctly.

---

## 🌐 Phase 13 — Web Automation & Browser

```yaml
phase_id: 13
priority: "P2"
total_tasks: 3
blocker: "Phase 12 complete"
```

**NOTE:** Directory is `src/capabilities/web/` (not `web_automation/`) per canonical structure.

---

### TASK 13.1 — Browser Capability

Location:

- `src/capabilities/web/browser.py`

Steps:

1. Create `src/capabilities/web/browser.py`. Inherit `BaseCapability`. `name = "browser"`.
2. `execute(args)` dispatches on `action`:
   - `navigate`: `page.goto(url, timeout=30000)` → return `{"url": page.url, "title": page.title()}`.
   - `click`: `page.click(selector)`.
   - `type`: `page.fill(selector, text)`.
   - `screenshot`: `page.screenshot(path=save_path)` → return path.
   - `extract_text`: `page.inner_text(selector or "body")` → return text.
3. Manage Playwright lifecycle:
   ```python
   from playwright.sync_api import sync_playwright
   self._playwright = sync_playwright().start()
   self._browser = self._playwright.chromium.launch(headless=False)
   ```
4. Browser launched once per `BrowserCapability` instance lifetime. `__del__` closes it.
5. `get_risk_level()` → `RiskLevel.medium`.
6. Resource note: browser adds ~500MB RAM. Log memory usage on launch.

Artifact: `src/capabilities/web/browser.py`

---

### TASK 13.2 — Web Session Manager

Location:

- `src/capabilities/web/session.py`

Steps:

1. Create `src/capabilities/web/session.py`.
2. Define `WebSessionManager` class.
3. `create_session(browser) -> BrowserContext` — creates Playwright context with isolated cookies/storage.
4. `close_session(context_id) -> None`.
5. `get_session(context_id) -> BrowserContext | None`.
6. `list_sessions() -> list[str]`.
7. Session IDs are UUIDs. Sessions are stored in `_sessions: dict[str, BrowserContext]`.

Artifact: `src/capabilities/web/session.py`

---

### TASK 13.3 — Web Automation Tests

Location:

- `tests/test_web_automation.py`

Tests (use `pytest-playwright` or mock Playwright):

1. Navigate to URL returns page title.
2. Screenshot returns valid file path.
3. Extract text returns non-empty string.
4. Session create/close lifecycle.
5. Timeout on unresponsive page returns `ToolResult.failure`.

Validation:

```bash
pytest tests/test_web_automation.py -v
```

Artifact: `tests/test_web_automation.py`

---

### Definition of Done — Phase 13

Browser automation operational with Playwright. Sessions managed. All tests pass.

---

## 📅 Phase 14 — Google APIs

```yaml
phase_id: 14
priority: "P2"
total_tasks: 4
blocker: "Phase 13 complete"
```

---

### TASK 14.1 — Google Auth Service

Location:

- `src/services/google/auth.py`

Steps:

1. Create `src/services/google/auth.py`.
2. Define `GoogleAuth` class.
3. Implement `authenticate(credentials_path: str = "data/google_credentials.json") -> Credentials`:
   - If `data/google_token.json` exists: load and refresh.
   - Else: run OAuth2 flow via `google_auth_oauthlib.flow.InstalledAppFlow` with scopes: Calendar, Gmail, Drive.
   - Save token to `data/google_token.json`.
4. Implement `get_credentials() -> Credentials` (returns cached or refreshed).
5. Scopes: `["https://www.googleapis.com/auth/calendar", "https://mail.google.com/", "https://www.googleapis.com/auth/drive"]`.
6. If credentials absent: raise `PermissionDeniedError("Google credentials not configured. Run auth flow.")`.

Artifact: `src/services/google/auth.py`

---

### TASK 14.2 — Google Calendar Service

Location:

- `src/services/google/calendar.py`

Steps:

1. Create `src/services/google/calendar.py`.
2. Define `GoogleCalendar` class.
3. Build service: `build("calendar", "v3", credentials=GoogleAuth().get_credentials())`.
4. `list_events(start: str, end: str) -> list[dict]` — ISO8601 strings.
5. `create_event(summary, start, end, description="") -> dict`.
6. `delete_event(event_id: str) -> None`.
7. All methods handle `HttpError` → raise `JarvisError` with user-friendly message.

Artifact: `src/services/google/calendar.py`

---

### TASK 14.3 — Gmail Service

Location:

- `src/services/google/gmail.py`

Steps:

1. Create `src/services/google/gmail.py`.
2. Define `GmailService` class.
3. `list_messages(query: str = "", max_results: int = 10) -> list[dict]`.
4. `get_message(message_id: str) -> dict` — includes subject, sender, body snippet.
5. `send_message(to: str, subject: str, body: str) -> None` — uses MIMEText + base64url encoding.

Artifact: `src/services/google/gmail.py`

---

### TASK 14.4 — Google Drive Service

Location:

- `src/services/google/drive.py`

Steps:

1. Create `src/services/google/drive.py`.
2. Define `GoogleDrive` class.
3. `list_files(query: str = "", max_results: int = 20) -> list[dict]`.
4. `download_file(file_id: str, destination: str) -> str` — returns path.
5. `upload_file(name: str, content: bytes, mime_type: str) -> str` — returns file_id.

Artifact: `src/services/google/drive.py`

---

### Definition of Done — Phase 14

Google services authenticate and return data. All three services functional with error handling.

---

## 📨 Phase 14.5 — Telegram Integration

```yaml
phase_id: 14.5
title: "Telegram Integration"
priority: "P2"
status: "not_started"
total_tasks: 3
blocker: "Phase 14 complete"
next_action: "TASK 14.5.1"
note: "In STRUCTURE.md and README but was absent from v2.0 tasks. Added in v2.1."
```

### Objective

Implement Telegram bot as an alternate interface to the JARVIS runtime. Users send messages via Telegram and receive responses. Bot acts as a thin interface — all decisions and execution flow through the same `run_turn()` pipeline.

---

### TASK 14.5.1 — Telegram Bot Service

Location:

- `src/services/telegram/bot.py`

Purpose:

- Define the Telegram bot connection and message routing.

Steps:

1. Create `src/services/telegram/bot.py`.
2. Define `TelegramBot` class.
3. Use `python-telegram-bot` library (async, v21+).
4. Implement `start(token: str) -> None`:
   - Build `Application` via `ApplicationBuilder().token(token).build()`.
   - Register handlers: `MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)`.
   - Register command handlers: `/start`, `/mode`, `/status`, `/quit`.
   - Call `application.run_polling()`.
5. Implement `async handle_message(update, context)`:
   - Extract `user_message = update.message.text`.
   - Extract `session_id = str(update.effective_chat.id)`.
   - Call `run_turn(user_message, session_id)` (sync → use `asyncio.to_thread`).
   - Send response: `await update.message.reply_text(response.text)`.
6. Implement `async send_message(chat_id: str, text: str) -> None` — for proactive notifications.
7. Token loaded from `os.environ["TELEGRAM_BOT_TOKEN"]`. If absent: log ERROR and skip bot start.

Success case:

- Bot starts, receives message, calls `run_turn()`, replies with response.

Failure case:

- Invalid token → `InvalidToken` exception caught, log ERROR, bot does not start.
- Ollama unavailable → degraded FinalResponse sent back to user.

Validation:

```bash
python -c "
from src.services.telegram.bot import TelegramBot
# Instantiation without token should not crash
try:
    bot = TelegramBot()
    print('TelegramBot instantiates OK')
except Exception as e:
    print(f'Expected if no token: {e}')
"
```

Artifact: `src/services/telegram/bot.py`

---

### TASK 14.5.2 — Telegram Command Handlers

Location:

- `src/services/telegram/commands.py`

Steps:

1. Create `src/services/telegram/commands.py`.
2. Define `async handle_start(update, context)` → reply with welcome message and available commands.
3. Define `async handle_mode(update, context)`:
   - Parse `context.args[0]` as mode.
   - Call `update_mode(session_id, mode)`.
   - Reply with confirmation.
4. Define `async handle_status(update, context)`:
   - Fetch: current model, mode, VRAM.
   - Reply with status summary.
5. Define `async handle_quit(update, context)` → reply "Goodbye" only (bot keeps running for other users).
6. Commands are registered in `TelegramBot.start()`.

Artifact: `src/services/telegram/commands.py`

---

### TASK 14.5.3 — Telegram Interface Tests

Location:

- `tests/test_telegram.py`

Steps:

1. Create `tests/test_telegram.py`.
2. Mock `python-telegram-bot` Application for unit tests.
3. Test: `handle_message` calls `run_turn` with correct args.
4. Test: response text is sent back to chat.
5. Test: `/mode SAFE` updates mode and replies.
6. Test: missing `TELEGRAM_BOT_TOKEN` → bot does not start, no crash.
7. Test: `run_turn` failure → user receives degraded response, not raw exception.

Validation:

```bash
pytest tests/test_telegram.py -v
```

Artifact: `tests/test_telegram.py`

---

### Definition of Done — Phase 14.5

Telegram bot receives messages, routes through `run_turn()`, replies. Mode command works. Missing token handled gracefully. All tests pass.

---

## 🌍 Phase 15 — Web UI

```yaml
phase_id: 15
priority: "P2"
total_tasks: 3
blocker: "Phase 14.5 complete"
```

**NOTE:** Directory is `src/interfaces/web_ui/` (underscore, not space).

---

### TASK 15.1 — Web UI Backend

Location:

- `src/interfaces/web_ui/app.py`

Steps:

1. Create `src/interfaces/web_ui/app.py`.
2. Define FastAPI `app`.
3. `POST /chat`: accepts `{"message": str, "session_id": str}` → calls `run_turn()` → returns `FinalResponse.model_dump()`.
4. `GET /history/{session_id}`: calls `MemoryDB().retrieve_recent(session_id, 20)` → returns list.
5. `GET /status`: returns `{"model": ..., "mode": ..., "vram_mb": ..., "degraded": ...}`.
6. `POST /mode`: accepts `{"mode": str}` → updates mode.
7. WebSocket `/ws/{session_id}`: accepts messages, streams `run_turn()` progress events via `EVT_STATE_TRANSITION` EventBus subscription, sends `FinalResponse` when complete.
8. Mount `src/interfaces/web_ui/static/` as `StaticFiles`.
9. Define `WebApp.start(host="0.0.0.0", port=8000)` → `uvicorn.run(app, ...)`.

Artifact: `src/interfaces/web_ui/app.py`

---

### TASK 15.2 — Web UI Frontend

Location:

- `src/interfaces/web_ui/static/index.html`

Steps:

1. Create `src/interfaces/web_ui/static/index.html`.
2. Single-file HTML/CSS/JS — no build step, no framework dependency.
3. Features:
   - Chat message display: user messages right-aligned, JARVIS left-aligned.
   - Input box + Send button.
   - WebSocket client: connect to `/ws/{uuid_session}` on load.
   - Mode toggle: dropdown SAFE/BALANCED/UNRESTRICTED → POST `/mode`.
   - Status bar: shows current model, VRAM, mode.
   - Arabic input: `dir="auto"` on input field for RTL support.
   - Loading indicator during response.
4. No external CDN dependencies — self-contained.

Artifact: `src/interfaces/web_ui/static/index.html`

---

### TASK 15.3 — Web UI Tests

Location:

- `tests/test_web_ui.py`

Tests (use `httpx.AsyncClient` with `ASGITransport`):

1. `POST /chat` returns `FinalResponse` JSON.
2. `GET /history/{session_id}` returns list.
3. `GET /status` returns model/mode/vram.
4. `POST /mode` with `SAFE` updates mode.
5. WebSocket connects and receives state events.

Validation:

```bash
pytest tests/test_web_ui.py -v
```

Artifact: `tests/test_web_ui.py`

---

### Definition of Done — Phase 15

Web UI functional. Chat, history, status, mode toggle all working. WebSocket streams state events. All tests pass.

---

## 🎙️ Phase 16 — Voice Pipeline

```yaml
phase_id: 16
priority: "P3"
total_tasks: 4
blocker: "Phase 15 complete"
```

---

### TASK 16.1 — STT Capability (Whisper)

Location:

- `src/capabilities/voice/stt.py`

Steps:

1. Create. Inherit `BaseCapability`. `name = "stt"`.
2. Use `openai-whisper` package (local, not API): `whisper.load_model("base")` — `base` model fits in ~1GB VRAM.
3. `execute(args)`:
   - `audio_path = args.get("audio_path")` — if None, record from microphone via `speech_recognition`.
   - Transcribe: `result = model.transcribe(audio_path)`.
   - Return `ToolResult(success=True, data={"text": result["text"], "language": result["language"]})`.
4. Model loaded lazily at first call to avoid VRAM use when unused.
5. `get_risk_level()` → `RiskLevel.low`.

Artifact: `src/capabilities/voice/stt.py`

---

### TASK 16.2 — TTS Capability (Piper)

Location:

- `src/capabilities/voice/tts.py`

Steps:

1. Create. Inherit `BaseCapability`. `name = "tts"`.
2. Use `piper-tts` — runs entirely CPU-side, no VRAM.
3. `execute(args)`:
   - `text = args["text"]`, `voice = args.get("voice", "en_US-lessac-medium")`.
   - Run: `piper --model {voice} --output_file {output_path} <<< "{text}"` via subprocess.
   - For Arabic: `voice = "ar_JO-kareem-medium"`.
   - Return `ToolResult(success=True, data={"audio_path": str(output_path)})`.
4. Play audio: `subprocess.Popen(["aplay" or "afplay" or "start", output_path])`.

Artifact: `src/capabilities/voice/tts.py`

---

### TASK 16.3 — Wake Word Detection

Location:

- `src/capabilities/voice/wake_word.py`

Steps:

1. Create. Define `WakeWordDetector` class (not a `BaseCapability` — it is a listener, not an action).
2. Use `speech_recognition.Recognizer` with `Microphone` source.
3. Implement `listen_for_wake_word(wake_word: str = "jarvis", callback: Callable) -> None`:
   - Runs in a background thread.
   - Continuous microphone listen loop.
   - On detecting text containing `wake_word` (case-insensitive): call `callback()`.
4. Implement `stop() -> None` → sets stop flag.
5. Integrates with `CLIChat` and `WebApp` for voice-activated input mode.

Artifact: `src/capabilities/voice/wake_word.py`

---

### TASK 16.4 — Voice Pipeline Tests

Location:

- `tests/test_voice.py`

Tests (mock audio files and mic input):

1. STT transcribes WAV file to text.
2. STT returns language field.
3. TTS generates audio file.
4. Wake word detection fires callback on match.
5. Wake word detection does not fire on non-match.

Validation:

```bash
pytest tests/test_voice.py -v
```

Artifact: `tests/test_voice.py`

---

### Definition of Done — Phase 16

STT transcribes. TTS synthesizes. Wake word triggers activation. All tests pass.

---

## 👁️ Phase 17 — Vision + Image

```yaml
phase_id: 17
priority: "P3"
total_tasks: 2
blocker: "Phase 16 complete"
```

---

### TASK 17.1 — Vision Capability (llava:7b)

Location:

- `src/capabilities/vision/vision.py`

Steps:

1. Create. Inherit `BaseCapability`. `name = "vision_analyze"`.
2. VRAM requirement: llava:7b = 4500MB. Check before loading.
3. `execute(args)`:
   - `image_path = args["image_path"]`
   - `prompt = args.get("prompt", "describe this image")`
   - Encode image: `base64.b64encode(Path(image_path).read_bytes()).decode()`.
   - POST to Ollama: `{"model": "llava:7b", "messages": [{"role": "user", "content": prompt, "images": [b64_image]}]}`.
   - Return `ToolResult(success=True, data={"description": response_text})`.
4. If VRAM insufficient: `ToolResult.failure("vision_analyze", "VRAM insufficient for llava:7b (requires 4500MB)")`.

Artifact: `src/capabilities/vision/vision.py`

---

### TASK 17.2 — Image Generation Capability

Location:

- `src/capabilities/vision/image_gen.py`

Steps:

1. Create. Inherit `BaseCapability`. `name = "image_gen"`.
2. Use `diffusers` library with `StableDiffusionPipeline`.
3. Model: `runwayml/stable-diffusion-v1-5` (requires ~2GB VRAM) or float32 CPU fallback.
4. `execute(args)`:
   - `prompt = args["prompt"]`, `size = args.get("size", "512x512")`.
   - Parse `size` → `width, height`.
   - Generate: `pipeline(prompt=prompt, width=width, height=height).images[0]`.
   - Save to `data/images/{uuid}.png`.
   - Return `ToolResult(success=True, data={"image_path": str(save_path)})`.
5. On VRAM insufficient: fall back to CPU (float32 pipeline).

Artifact: `src/capabilities/vision/image_gen.py`

---

### Definition of Done — Phase 17

Vision analyzes images. Image generation produces output. VRAM constraints handled with CPU fallback.

---

## 🚀 Phase 18 — QA + Production

```yaml
phase_id: 18
priority: "P0"
total_tasks: 6
blocker: "Phase 17 complete"
```

---

### TASK 18.1 — Performance Tests

Location:

- `tests/test_performance.py`

Steps:

1. Create `tests/test_performance.py`.
2. Fast-path latency test:
   ```python
   start = time.perf_counter()
   d = FastPath().check("open notepad")
   elapsed_ms = (time.perf_counter() - start) * 1000
   assert elapsed_ms < 100, f"Fast path took {elapsed_ms:.1f}ms > 100ms target"
   ```
3. Simple query latency: `run_turn("what is 2+2", "s1")` → assert elapsed < 5000ms.
4. VRAM check: after loading `gemma3:4b`, `VRAMMonitor().get_available_vram_mb() >= 512` (safety headroom).
5. MetricsCollector summary after 10 turns: `p95 < 5000ms` for decision phase.
6. Web UI concurrent: 3 simultaneous `POST /chat` requests all return within 30s.

Validation:

```bash
pytest tests/test_performance.py -v
```

Artifact: `tests/test_performance.py`

---

### TASK 18.2 — Arabic Language Tests

Location:

- `tests/test_arabic.py`

Tests:

1. Fast path: `"افتح المفكرة"` → `intent=tool_use, tool_name=open_app`.
2. Fast path: `"ابحث عن الذكاء الاصطناعي"` → `intent=search`.
3. Classifier: Arabic input does not cause encoding error.
4. `PromptBuilder` with `language=ar` → prompt contains "Respond in Arabic".
5. Arabic text in InputPacket passes validation.
6. CLI formatter: Arabic response preceded by RLM mark.
7. STT: Arabic audio transcribes to Arabic text.

Validation:

```bash
pytest tests/test_arabic.py -v
```

Artifact: `tests/test_arabic.py`

---

### TASK 18.3 — Production Configuration

Location:

- `config/production.yaml`

Steps:

1. Create `config/production.yaml` as a `settings.yaml` override file:
   ```yaml
   models:
     default: "gemma3:4b"
     timeout_s: 45
   execution:
     mode: "BALANCED"
     total_turn_timeout_s: 120
   observability:
     log_level: "WARNING"
     metrics_enabled: true
     trace_enabled: false
     replay_enabled: false
   ```
2. `load_config` supports `load_config("config/production.yaml")` — loads production overrides merged with defaults from `settings.yaml`.
3. Merge strategy: production.yaml values override settings.yaml values (deep merge).

Validation:

```bash
python -c "
from src.core.config import load_config
s = load_config('config/production.yaml')
assert s.execution.mode == 'BALANCED'
assert s.observability.log_level == 'WARNING'
print('Production config OK')
"
```

Artifact: `config/production.yaml`

---

### TASK 18.4 — Full Test Suite Run

Steps:

1. `pytest tests/ -v --tb=short` — all tests pass.
2. `pytest tests/ --cov=src --cov-report=term-missing` — coverage > 80%.
3. Fix any failures. No exceptions.
4. Verify no deprecated `open_app()` calls remain (grep codebase).
5. Verify no `utils`, `misc`, `helpers`, `brain` directories exist.
6. Verify `web ui` (with space) directory does not exist.

Validation:

```bash
pytest tests/ -v --tb=short
pytest tests/ --cov=src --cov-report=term-missing | grep TOTAL
# TOTAL should show > 80%
grep -r "open_app(" src/ app/ --include="*.py"  # should only appear in apps.py definition
```

---

### TASK 18.5 — Version and Release

Location:

- `VERSION`
- `RELEASE_NOTES.md`

Steps:

1. Create `VERSION` file containing `3.0.0`.
2. Create `RELEASE_NOTES.md`:
   - Features: all 18 phases, capabilities list, supported models.
   - Breaking changes: Phase 0 rebuilt with contract-first design. `DecisionOutput`, `LLMOutput`, `ToolResult` enforced from day 0.
   - Hardware requirements: RTX 3050 6GB VRAM minimum.
   - Startup: `pip install -e . && python app/main.py --interface cli`.
   - Known limitations: Stable Diffusion CPU fallback is slow (~5min per image), llava requires 4.5GB VRAM.
   - Configuration: copy `settings.example.yaml` → `settings.yaml`.
3. Remove all `print()` debug statements from non-CLI code.
4. Ensure no hardcoded paths (all from config).

Artifacts: `VERSION`, `RELEASE_NOTES.md`

---

### TASK 18.6 — Determinism Verification

Location:

- `tests/test_determinism.py`

Tests:

1. Same input → same fast-path decision (deterministic regex matching).
2. Same input + same VRAM → same model selected (deterministic scoring — no randomization unless `variability_margin` explicitly enabled).
3. Same state → same transition allowed (ALLOWED_TRANSITIONS is a static dict).
4. Same `InputPacket` → same `ContextAssembler` output (no timestamps in output structure).
5. `RetryManager.consume()` decrements predictably.
6. `ModelScorer.rank_models()` with same inputs → same ordered list across 10 runs.

Validation:

```bash
pytest tests/test_determinism.py -v
```

Artifact: `tests/test_determinism.py`

---

### Definition of Done — Phase 18

All tests pass. Coverage > 80%. Performance targets met. Arabic verified. Determinism verified. Release artifacts created.

---

### 📊 Summary

| Metric                             | Count                          |
| ---------------------------------- | ------------------------------ |
| Total phases                       | 20 (0 through 18 + Phase 14.5) |
| Total tasks                        | ~133                           |
| New tasks vs v2.0                  | +13                            |
| Critical defects fixed (v2.1→v3.0) | 25                             |
| Test files                         | 15                             |
| Config files                       | 8                              |
| Source modules                     | ~60                            |

### Validation Checklist (v3.0 Final)

- [ ] No `utils`, `misc`, `helpers`, `brain`, `common` folders
- [ ] No space in `web_ui` directory name
- [ ] `capabilities/web/` used (not `web_automation/`)
- [ ] `src/core/sandbox/` and `src/core/safety/` in structure
- [ ] `src/core/observability/` in structure
- [ ] EventBus defined before first reference (Phase 1)
- [ ] All exceptions in `src/core/exceptions.py`
- [ ] `SchemaValidator` stub exists before Phase 6
- [ ] Factor names in scorer match `config/models.yaml` keys exactly
- [ ] `AppLauncher.execute()` interface used everywhere after Phase 9
- [ ] Phase 0 uses contracts (DecisionOutput, LLMOutput, ToolResult) from day 0
- [ ] Phase 0 enforces Observe → Decide → Think → Act → Evaluate
- [ ] `config/settings.yaml` exists (not just `.example`)
- [ ] Telegram phase exists and is sequenced correctly
- [ ] `check_limit` semantics: current < max → True, current >= max → False
- [ ] `pytest tests/ -v` passes all tests
- [ ] `pytest tests/ --cov=src` shows > 80% coverage
- [ ] All three specs (TASKS.md, STRUCTURE.md, README.md) share `spec_version: v3.0`
- [ ] VERSION file exists with `project_version: 3.0.0`
- [ ] Config precedence: CLI > ENV > .env > YAML (enforced)
- [ ] Security: blocked_commands includes PowerShell + Unix equivalents
- [ ] DecisionOutput includes `score_breakdown` and `candidate_list` for model-path decisions

---

**JARVIS v3.0 — Execution Plan v3.0**
_Last updated: 2026-05-02_
_Contract-first. Single source of truth. No drift._
