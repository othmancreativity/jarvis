# 📋 JARVIS — Execution Plan

> **spec_version:** `v3.0` | **project_version:** `3.0.0` | **structure_version:** `2`

---

## 📑 Table of Contents

- [Project Status](#project-status)
- [Canonical Directory Structure](#canonical-directory-structure)
- [Status Legend](#status-legend)
- [Phase Progress Summary](#phase-progress-summary)
- [Phase 0](#phase-0--first-working-system-vertical-slice) — First Working System
- [Phase 1](#phase-1--foundation--observability) — Foundation + Observability
- [Phase 2](#phase-2--execution-contract) — Execution Contract
- [Phase 3](#phase-3--model-manager--vram) — Model Manager + VRAM
- [Phase 4](#phase-4--runtime-state-machine) — Runtime State Machine
- [Phase 5](#phase-5--decision-system) — Decision System
- [Phase 6](#phase-6--sandbox--safety) — Sandbox + Safety
- [Phase 7](#phase-7--memory-engine) — Memory Engine
- [Phase 8](#phase-8--capability-system) — Capability System
- [Phase 9](#phase-9--system-control-capabilities) — System Control Capabilities
- [Phase 10](#phase-10--prompt-builder) — Prompt Builder
- [Phase 11](#phase-11--execution-hardening) — Execution Hardening
- [Phase 12](#phase-12--cli-interface) — CLI Interface
- [Phase 13](#phase-13--web-automation--browser) — Web Automation & Browser
- [Phase 14](#phase-14--google-apis) — Google APIs
- [Phase 14.5](#phase-145--telegram-integration) — Telegram Integration
- [Phase 15](#phase-15--web-ui) — Web UI
- [Phase 16](#phase-16--voice-pipeline) — Voice Pipeline
- [Phase 17](#phase-17--vision--image) — Vision + Image
- [Phase 18](#phase-18--qa--production) — QA + Production
- [Summary](#summary)

---

## Project Status

```yaml
project:
  name: JARVIS
  version: "3.0.0"
  spec_version: "v3.0"
  structure_version: "2"
  last_updated: "2026-05-02"
  current_phase: 1
  overall_progress_percent: 5
  risk_level: "medium"
  hardware_profile:
    gpu: "RTX 3050 6GB VRAM"
    ram: "16 GB"
    cpu: "Intel Core i5 12th Gen"
  current_blocker: "none"
  next_action: "TASK 1.0"
  config_root: "config/runtime/"
  env_root: "config/env/"
```

---

## Canonical Directory Structure

```
jarvis/
│
├── app/
│   ├── main.py
│   └── jarvis_slice.py
│
├── config/
│   ├── build/
│   ├── env/
│   │   ├── .env
│   │   └── .env.example
│   └── runtime/
│       ├── capabilities.yaml
│       ├── jarvis_identity.yaml
│       ├── mode_fragments.yaml
│       ├── models.yaml
│       ├── production.yaml
│       ├── settings.example.yaml
│       └── settings.yaml
│
├── data/
│   ├── images/
│   ├── memory.db
│   ├── audit.db
│   ├── profiles/
│   └── screenshots/
│
├── docs/
│   ├── README.md
│   ├── STRUCTURE.md
│   └── TASKS.md
│
├── logs/
│
├── meta/
│   ├── .editorconfig
│   ├── .gitignore
│   ├── LICENSE
│   ├── pyproject.toml
│   ├── requirements.txt
│   └── .gitkeep
│
├── scripts/
│   └── setup.sh
│
├── tests/
│   ├── conftest.py
│   ├── test_arabic.py
│   ├── test_capabilities.py
│   ├── test_contracts.py
│   ├── test_decision.py
│   ├── test_determinism.py
│   ├── test_identity_enforcement.py
│   ├── test_integration.py
│   ├── test_memory.py
│   ├── test_observability.py
│   ├── test_performance.py
│   ├── test_safety.py
│   ├── test_sandbox.py
│   ├── test_state_machine.py
│   ├── test_telegram.py
│   ├── test_voice.py
│   └── test_web_ui.py
│
└── src/
    ├── __init__.py          ← الملف الوحيد المتبقي في المشروع كله
    │
    ├── capabilities/
    │   ├── base.py
    │   ├── executor.py
    │   ├── registry.py
    │   ├── result.py
    │   ├── validator.py
    │   ├── api/
    │   ├── coder/
    │   │   └── executor.py
    │   ├── files/
    │   │   └── file_ops.py
    │   ├── notify/
    │   │   └── toasts.py
    │   ├── screen/
    │   │   └── capture.py
    │   ├── search/
    │   │   └── web_search.py
    │   ├── system/
    │   │   ├── apps.py
    │   │   ├── clipboard.py
    │   │   └── sysinfo.py
    │   ├── vision/
    │   │   ├── image_gen.py
    │   │   └── vision.py
    │   ├── voice/
    │   │   ├── stt.py
    │   │   ├── tts.py
    │   │   └── wake_word.py
    │   └── web/
    │       ├── browser.py
    │       └── session.py
    │
    ├── core/
    │   ├── config.py
    │   ├── exceptions.py
    │   ├── logging_setup.py
    │   ├── context/
    │   │   ├── assembler.py
    │   │   ├── builder.py
    │   │   └── bundle.py
    │   ├── decision/
    │   │   ├── classifier.py
    │   │   ├── decision.py
    │   │   ├── fast_path.py
    │   │   ├── model_score.py
    │   │   ├── output.py
    │   │   ├── risk.py
    │   │   └── scorer.py
    │   ├── observability/
    │   │   ├── event_bus.py
    │   │   └── metrics.py
    │   ├── runtime/
    │   │   ├── degradation.py
    │   │   ├── escalation.py
    │   │   ├── evaluation_result.py
    │   │   ├── evaluator.py
    │   │   ├── executor.py
    │   │   ├── fallback.py
    │   │   ├── final_response.py
    │   │   ├── limits.py
    │   │   ├── llm_output.py
    │   │   ├── loop.py
    │   │   ├── retry.py
    │   │   ├── state.py
    │   │   ├── state_manager.py
    │   │   ├── timeout.py
    │   │   └── validate_decision.py
    │   ├── safety/
    │   │   ├── audit.py
    │   │   ├── classifier.py
    │   │   ├── mode_enforcer.py
    │   │   └── permission.py
    │   └── sandbox/
    │       └── sandbox.py
    │
    ├── interfaces/
    │   ├── cli/
    │   │   ├── chat.py
    │   │   ├── commands.py
    │   │   └── formatting.py
    │   ├── gui/
    │   └── web_ui/
    │       ├── app.py
    │       └── static/
    │           └── index.html
    │
    ├── memory/
    │   ├── database.py
    │   ├── indexer.py
    │   ├── retriever.py
    │   ├── scorer.py
    │   ├── ttl.py
    │   └── user_profile.py
    │
    ├── models/
    │   ├── availability.py
    │   ├── manager.py
    │   ├── profiles.py
    │   ├── vram_monitor.py
    │   ├── llm/
    │   │   └── engine.py
    │   ├── speech/
    │   └── vision/
    │
    └── services/
        ├── google/
        │   ├── auth.py
        │   ├── calendar.py
        │   ├── drive.py
        │   └── gmail.py
        ├── integrations/
        └── telegram/
            ├── bot.py
            └── commands.py
```

---

## Phase Progress

| #    | Phase                       | Priority | Progress   | Ratio | Next Action |
| ---- | --------------------------- | -------- | ---------- | ----- | ----------- |
| 0    | First Working System        | P0       | ██████████ | 5/5   | —           |
| 1    | Foundation + Observability  | P0       | ██████████ | 13/13 | —           |
| 2    | Execution Contract          | P0       | ░░░░░░░░░░ | 0/10  | TASK 2.0    |
| 3    | Model Manager + VRAM        | P0       | ██████████ | 5/5   | —           |
| 4    | Runtime State Machine       | P0       | ██████████ | 8/8   | —           |
| 5    | Decision System             | P1       | ░░░░░░░░░░ | 0/7   | TASK 5.1    |
| 6    | Sandbox + Safety            | P0       | ░░░░░░░░░░ | 0/7   | TASK 6.1    |
| 7    | Memory Engine               | P1       | ░░░░░░░░░░ | 0/6   | TASK 7.1    |
| 8    | Capability System           | P1       | ░░░░░░░░░░ | 0/6   | TASK 8.1    |
| 9    | System Control Capabilities | P1       | ░░░░░░░░░░ | 0/8   | TASK 9.1    |
| 10   | Prompt Builder              | P1       | ░░░░░░░░░░ | 0/5   | TASK 10.1   |
| 11   | Execution Hardening         | P0       | ░░░░░░░░░░ | 0/6   | TASK 11.1   |
| 12   | CLI Interface               | P2       | ░░░░░░░░░░ | 0/3   | TASK 12.1   |
| 13   | Web Automation & Browser    | P2       | ░░░░░░░░░░ | 0/3   | TASK 13.1   |
| 14   | Google APIs                 | P2       | ░░░░░░░░░░ | 0/4   | TASK 14.1   |
| 14.5 | Telegram Integration        | P2       | ░░░░░░░░░░ | 0/3   | TASK 14.5.1 |
| 15   | Web UI                      | P2       | ░░░░░░░░░░ | 0/3   | TASK 15.1   |
| 16   | Voice Pipeline              | P3       | ░░░░░░░░░░ | 0/4   | TASK 16.1   |
| 17   | Vision + Image              | P3       | ░░░░░░░░░░ | 0/2   | TASK 17.1   |
| 18   | QA + Production             | P0       | ░░░░░░░░░░ | 0/6   | TASK 18.1   |

## Legend

[Priority Levels]
P0 = Critical/Urgent | P1 = High | P2 = Medium | P3 = Low

[Progress Bar]
█ = Completed segment | ░ = Remaining segment
Fixed 10-unit scale for visual consistency (ratio shown numerically)

## Phase 0 — First Working System (Vertical Slice)

```yaml
phase_id: 0
status: "done"
progress_percent: 100
total_tasks: 5
validation_status: "passed"
last_updated: "2026-05-02"
```

> Phase 0 complete. All v3.0 contract requirements met:
>
> - ✅ DecisionOutput with score_breakdown and candidate_list
> - ✅ LLMOutput contract implemented
> - ✅ ToolResult contract implemented
> - ✅ InputPacket and FinalResponse contracts
> - ✅ CapabilityExecutor replaces direct open_app() calls
> - ✅ Observe → Decide → Think → Act → Evaluate flow enforced
> - ✅ Vertical slice demo working (app/jarvis_slice.py)
> - ✅ 17 contract tests passing
>
> **BREAKING CHANGE NOTICE:** Phase 0 `AppLauncher` uses `open_app(name)`. Phase 9 TASK 9.1
> replaces this with `execute(args)` inheriting `BaseCapability`. All callers in
> `app/jarvis_slice.py` must be updated in Phase 9.

Artifacts: `app/jarvis_slice.py`, `src/models/llm/engine.py`, `src/core/decision/classifier.py`, `src/capabilities/system/apps.py`, `src/capabilities/base.py`, `src/capabilities/executor.py`, `src/capabilities/result.py`

---

## Phase 1 — Foundation + Observability

```yaml
phase_id: 1
title: "Foundation + Observability"
priority: "P0"
status: "not_started"
total_tasks: 13
blocker: "Phase 0 complete"
next_action: "TASK 1.0"
config_paths:
  settings: "config/runtime/settings.yaml"
  models: "config/runtime/models.yaml"
  capabilities: "config/runtime/capabilities.yaml"
  env: "config/env/.env"
```

### Objective

Establish project packaging, configuration, logging, observability, and shared infrastructure. Every task here is a hard prerequisite for Phases 2+. No subsequent phase may begin until all 13 tasks are complete and validated.

---

### TASK 1.0 — Project Scaffolding

**Location:** `pyproject.toml`, `requirements.txt`, all `__init__.py` files, full directory tree

**Purpose:** Create installable Python package, declare all dependencies, and establish the complete directory skeleton matching `STRUCTURE.md`.

**Steps:**

1. Create `pyproject.toml` with `[project]` table:
   - `name = "jarvis"`
   - `version = "3.0.0"`
   - `requires-python = ">=3.10"`
   - `description = "Local-first AI assistant for desktop control and automation"`

2. Declare `[project.dependencies]`:

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
   pytest-cov>=4.0.0
   ```

3. Declare `[project.optional-dependencies]`:

   ```toml
   [project.optional-dependencies]
   vision = ["diffusers>=0.27.0", "transformers>=4.38.0", "torch>=2.2.0"]
   voice = ["openai-whisper>=20231117", "piper-tts>=1.2.0"]
   full = ["jarvis[vision,voice]"]
   ```

4. Add `[tool.pytest.ini_options]`:

   ```toml
   testpaths = ["tests"]
   asyncio_mode = "auto"
   addopts = "--tb=short"
   ```

5. Create `requirements.txt` as pinned export comment-header:

   ```
   # Generated from pyproject.toml. Run: pip install -e .
   # For pinned environment: pip freeze > requirements.txt
   ```

6. Create every directory in the canonical structure with `.gitkeep` placeholders if empty. Directories to create:
   - `app/`, `config/env/`, `config/runtime/`, `data/images/`, `data/profiles/`, `data/screenshots/`
   - `docs/`, `logs/`, `meta/`, `scripts/`
   - `src/capabilities/api/`, `src/capabilities/coder/`, `src/capabilities/files/`
   - `src/capabilities/notify/`, `src/capabilities/screen/`, `src/capabilities/search/`
   - `src/capabilities/system/`, `src/capabilities/vision/`, `src/capabilities/voice/`
   - `src/capabilities/web/`
   - `src/core/context/`, `src/core/decision/`, `src/core/observability/`
   - `src/core/runtime/`, `src/core/safety/`, `src/core/sandbox/`
   - `src/interfaces/cli/`, `src/interfaces/gui/`, `src/interfaces/web_ui/static/`
   - `src/memory/`, `src/models/llm/`, `src/models/speech/`, `src/models/vision/`
   - `src/services/google/`, `src/services/integrations/`, `src/services/telegram/`
   - `tests/`

7. Create `app/__init__.py` (empty — marks `app/` as package).

8. Create `tests/__init__.py` (empty).

9. Create all `src/**/__init__.py` stub files (empty unless specified in TASK 1.3).

10. Install in development mode: `pip install -e ".[vision,voice]"`.

11. Verify top-level imports: `python -c "import src; import app; print('packages OK')"`.

**Success case:**

- `pip install -e .` exits 0.
- `python -c "import src; import app"` succeeds.
- All directories exist matching canonical structure.
- `find . -name "__init__.py" | wc -l` returns ≥ 25.

**Failure case:**

- Missing system dependency (tesseract, node, etc.) → document in `docs/README.md` Requirements section. Do NOT fail silently.

**Validation:**

```bash
pip install -e .
python -c "import src; import app; print('packages OK')"
find . -name "__init__.py" | sort
```

**Artifacts:** `pyproject.toml`, `requirements.txt`, all `__init__.py` files, full directory tree

---

### TASK 1.1 — Settings YAML and Pydantic Loader

**Location:** `config/runtime/settings.example.yaml`, `config/runtime/settings.yaml`, `src/core/config.py`

**Purpose:** Create the validated configuration system. `settings.yaml` is the live file. `settings.example.yaml` is the committed template. All subsequent modules load settings through `load_config()`.

**Steps:**

1. Create `config/runtime/settings.example.yaml` with exact content:

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
     mode: "BALANCED"
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
     blocked_paths:
       - "/etc"
       - "/sys"
       - "/proc"
       - "/boot"
       - "C:\\Windows\\System32"
       - "C:\\Windows\\SysWOW64"
     blocked_commands:
       - "rm -rf"
       - "rm -r"
       - "shred"
       - "wipe"
       - "dd"
       - "mkfs"
       - "fdisk"
       - "parted"
       - "mkswap"
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

2. Copy `settings.example.yaml` → `config/runtime/settings.yaml`. This file is gitignored and user-customized.

3. Add `config/runtime/settings.yaml` to `.gitignore`.

4. Create `src/core/config.py`.

5. Define nested Pydantic `BaseModel` hierarchy matching every YAML key above. Required models:
   - `ModelsConfig` with `default: str`, `timeout_s: int`, `fallback_chain: list[str]`
   - `PathsConfig` with `allowed_roots: list[str]`, `memory_db: str`, `audit_db: str`, `logs_dir: str`
   - `ExecutionConfig` with all numeric limits and `mode: Literal["SAFE","BALANCED","UNRESTRICTED"]`
   - `SafetyConfig` with `blocked_apps: list[str]`, `blocked_paths: list[str]`, `blocked_commands: list[str]`, `allowed_commands: list[str]`
   - `ObservabilityConfig` with `log_level: str`, all boolean flags, rotation settings
   - `Settings` top-level model containing all above

6. Define `load_config(path: str = "config/runtime/settings.yaml", cli_overrides: dict | None = None) -> Settings`.

7. Inside `load_config`, implement the following load order (last wins):
   - Step 1: Load YAML defaults from `path`.
   - Step 2: Apply `.env` via `load_dotenv("config/env/.env", override=False)` — does NOT override already-set shell vars.
   - Step 3: Apply shell ENV vars with prefix `JARVIS_` and nested delimiter `__` via Pydantic's `SettingsConfigDict`.
   - Step 4: Apply `cli_overrides` dict — always wins.

8. After loading, expand `~` in all path fields using `Path(v).expanduser()` for every value in `PathsConfig`.

9. Validate `config/runtime/models.yaml` weights sum to 1.0 (within 0.001 tolerance) — raise `ValidationError` if not.

10. Implement singleton pattern: first call loads and caches; subsequent calls return cached instance. Provide `reload_config()` to force re-load (for tests).

**Success case:**

- `load_config()` returns `Settings` with `models.default == "gemma3:4b"`.
- `JARVIS_EXECUTION__MODE=SAFE python -c "from src.core.config import load_config; s=load_config(); assert s.execution.mode=='SAFE'"` passes.
- `safety.blocked_commands` is a non-empty list.
- `paths.allowed_roots` values are expanded (no `~`).

**Failure cases:**

- `settings.yaml` missing → `FileNotFoundError("config/runtime/settings.yaml not found. Copy settings.example.yaml to settings.yaml and configure.")`.
- Invalid `execution.mode` → Pydantic `ValidationError` listing allowed values.
- `models.yaml` weights ≠ 1.0 → `ValidationError("models.yaml weights sum to X, must be 1.0")`.

**Validation:**

```bash
python -c "
from src.core.config import load_config
s = load_config('config/runtime/settings.yaml')
assert s.models.default is not None
assert s.execution.mode in ('SAFE', 'BALANCED', 'UNRESTRICTED')
assert len(s.execution.fallback_chain) >= 1
assert len(s.safety.blocked_commands) > 0
assert '~' not in str(s.paths.allowed_roots)
print(f'Config OK: mode={s.execution.mode}, model={s.models.default}')
"
```

**Artifacts:** `config/runtime/settings.example.yaml`, `config/runtime/settings.yaml`, `src/core/config.py`

---

### TASK 1.2 — Structured Logging Setup

**Location:** `src/core/logging_setup.py`

**Purpose:** Implement structured logging with mandatory context fields. All modules use `from loguru import logger` after `setup_logging()` is called once at boot.

**Steps:**

1. Create `src/core/logging_setup.py`.

2. Define `setup_logging(level: str, logs_dir: str) -> None`:
   - Step 1: Remove Loguru's default handler: `logger.remove()`.
   - Step 2: Create `logs_dir` if it does not exist. If not writable, fall back to stderr only and log a warning.
   - Step 3: Add console sink with format `"{time:ISO8601} | {level:<8} | {message}"`.
   - Step 4: Add structured file sink with rotation:
     ```python
     logger.add(
         f"{logs_dir}/jarvis_{{time}}.log",
         level=level,
         rotation="100 MB",
         retention=5,
         serialize=True,  # JSON output
         enqueue=True,    # thread-safe async writes
     )
     ```
   - Step 5: Track setup with a module-level `_setup_done: bool` flag — subsequent calls are no-ops (idempotent).

3. Define `log_event(event: str, phase: str, session_id: str = "", turn_id: int = 0, trace_id: str = "", data: dict | None = None) -> None`:
   - Calls `logger.bind(event=event, session_id=session_id, turn_id=turn_id, phase=phase, trace_id=trace_id, data=data or {}).info(event)`.
   - This is the canonical structured log call used by all other modules.

4. `setup_logging` is called exactly once from `app/main.py`. Subsequent modules call `from loguru import logger` directly.

**Success case:**

- JSON log file contains keys: `record.extra.event`, `record.extra.session_id`, `record.extra.turn_id`, `record.extra.phase`, `record.extra.trace_id`, `record.extra.data`.
- Second call to `setup_logging` is a no-op (no duplicate handlers).

**Failure case:**

- `logs/` not writable → stderr-only mode, logs `WARNING: logs/ not writable, logging to stderr only`.

**Validation:**

```bash
python -c "
import json, tempfile, os
from src.core.logging_setup import setup_logging, log_event
with tempfile.TemporaryDirectory() as d:
    setup_logging('DEBUG', d)
    setup_logging('DEBUG', d)  # second call must be no-op
    log_event('test_event', phase='test', session_id='s1', turn_id=1, trace_id='t1', data={'k': 'v'})
    log_files = [f for f in os.listdir(d) if f.endswith('.log')]
    assert len(log_files) > 0
    line = open(os.path.join(d, log_files[0])).readline()
    parsed = json.loads(line)
    assert parsed['record']['extra']['event'] == 'test_event'
    print('Logging OK')
"
```

**Artifact:** `src/core/logging_setup.py`

---

### TASK 1.3 — Package `__init__.py` Public API

**Location:** `src/__init__.py` and all sub-package `__init__.py` files

**Purpose:** Define stable public imports so internal refactoring does not break callers.

**Steps:**

1. `src/__init__.py`: set `__version__ = "3.0.0"`.
2. `src/core/__init__.py`: export `load_config`, `setup_logging`.
3. `src/capabilities/__init__.py`: export `BaseCapability`, `CapabilityRegistry`, `CapabilityExecutor`, `ToolResult`, `ValidationResult`.
4. `src/memory/__init__.py`: export `MemoryDB`, `ContextRetriever`.
5. `src/models/__init__.py`: export `ModelManager`, `VRAMMonitor`.
6. `src/interfaces/__init__.py`: empty (interfaces are started, not imported).
7. `src/services/__init__.py`: empty.
8. All leaf package `__init__.py` files: empty unless there is a clear public export.

**Validation:**

```bash
python -c "
from src import __version__
assert __version__ == '3.0.0'
from src.core import load_config
from src.capabilities import BaseCapability, ToolResult
print('Public API OK')
"
```

---

### TASK 1.4 — Model Capability Profiles

**Location:** `src/models/profiles.py`

**Purpose:** Single source of truth for model metadata. Consumed by the Decision scorer (Phase 5). No duplication with `config/runtime/models.yaml` (which holds weights only).

**Steps:**

1. Create `src/models/profiles.py`.

2. Define `ModelProfile` as a frozen dataclass:

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

3. Define `PROFILES: dict[str, ModelProfile]` with entries:
   - `gemma3:4b`: vram=3200, caps=["reasoning","multilingual"], latency="fast", reasoning="medium", ctx=8192, arabic=True
   - `qwen3:8b`: vram=5000, caps=["reasoning","multilingual"], latency="medium", reasoning="high", ctx=32768, arabic=True
   - `qwen2.5-coder:7b`: vram=4800, caps=["code","reasoning"], latency="medium", reasoning="medium", ctx=16384, arabic=False
   - `llava:7b`: vram=4500, caps=["vision","reasoning"], latency="slow", reasoning="medium", ctx=4096, arabic=False
   - `qwen2.5:7b`: vram=4600, caps=["reasoning","multilingual"], latency="medium", reasoning="high", ctx=32768, arabic=True

4. Implement `get_profile(model_name: str) -> ModelProfile | None` — returns None for unknown models.

5. Implement `list_profiles() -> list[ModelProfile]` — returns all profiles as a list.

**Validation:**

```bash
python -c "
from src.models.profiles import get_profile, list_profiles
p = get_profile('gemma3:4b')
assert p.vram_required_mb == 3200
assert p.latency_tier == 'fast'
assert get_profile('nonexistent') is None
print(f'{len(list_profiles())} profiles loaded OK')
"
```

**Artifact:** `src/models/profiles.py`

---

### TASK 1.5 — Model Scoring Weights YAML

**Location:** `config/runtime/models.yaml`

**Purpose:** Define scoring weights and fallback chain used by the Decision scorer. Weights are tunable without code changes. Must sum to exactly 1.0.

**Steps:**

1. Create `config/runtime/models.yaml`:

   ```yaml
   # Scoring weights must sum to 1.0. Validated at config load time.
   weights:
     fit_complexity: 0.30 # how well reasoning_tier matches input complexity
     fit_mode: 0.20 # how well latency_tier matches execution mode
     cost_penalty: 0.20 # lower VRAM = higher score
     quality_need: 0.20 # absolute reasoning quality
     memory_bias: 0.10 # historical success rate recency

   variability_margin: 0.05 # tie-break randomization — disabled by default

   fallback:
     tier_1: "qwen2.5:7b"
     tier_2: "gemma3:4b"
   ```

2. In `src/core/config.py` (TASK 1.1), load this file and validate sum:
   ```python
   total = sum(weights.values())
   if abs(total - 1.0) > 0.001:
       raise ValidationError(f"models.yaml weights sum to {total:.4f}, must be 1.0")
   ```

**Validation:**

```bash
python -c "
import yaml
m = yaml.safe_load(open('config/runtime/models.yaml'))
w = m['weights']
total = sum(w.values())
assert abs(total - 1.0) < 0.001, f'Weights sum to {total}'
assert set(w.keys()) == {'fit_complexity','fit_mode','cost_penalty','quality_need','memory_bias'}
assert m['fallback']['tier_1'] and m['fallback']['tier_2']
print('models.yaml OK')
"
```

**Artifact:** `config/runtime/models.yaml`

---

### TASK 1.6 — Environment Variables

**Location:** `config/env/.env.example`, `config/env/.env`

**Purpose:** All secrets live here. Never in YAML. Never committed to git.

**Steps:**

1. Create `config/env/.env.example`:

   ```ini
   # Telegram
   TELEGRAM_BOT_TOKEN=your_token_here

   # Google OAuth
   GOOGLE_CLIENT_ID=your_client_id
   GOOGLE_CLIENT_SECRET=your_client_secret
   GOOGLE_REDIRECT_URI=http://localhost:8080

   # Ollama base URL (override if non-default)
   OLLAMA_BASE_URL=http://localhost:11434

   # Runtime overrides — applied over YAML defaults
   JARVIS_EXECUTION__MODE=BALANCED
   ```

2. Copy `config/env/.env.example` → `config/env/.env`.

3. Add `config/env/.env` and `config/runtime/settings.yaml` to `.gitignore`.

4. In `load_config()` (TASK 1.1), call `load_dotenv("config/env/.env", override=False)` as step 2 of the load order.

**Validation:**

```bash
python -c "
from dotenv import load_dotenv
import os
load_dotenv('config/env/.env.example')
print('dotenv OK:', os.environ.get('OLLAMA_BASE_URL', 'not set'))
"
```

---

### TASK 1.7 — User Profile

**Location:** `src/memory/user_profile.py`

**Purpose:** Persistent user profile. Used by `InputPacket` (Phase 2). Must exist before Phase 2 begins.

**Steps:**

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

3. Set `PROFILE_STORE_PATH = Path("data/profiles/")`.

4. Implement `load_profile(user_id: str) -> UserProfile`:
   - Look for `data/profiles/{user_id}.json`.
   - If file missing → return `UserProfile(user_id=user_id)` (default profile, not an error).
   - If JSON parse fails → log `WARNING: corrupted profile for {user_id}, using defaults` → return default.

5. Implement `save_profile(profile: UserProfile) -> None`:
   - Create `data/profiles/` directory if absent.
   - Update `profile.updated_at = datetime.utcnow().isoformat()`.
   - Write `profile.__dict__` as JSON with `indent=2`.

6. Implement `update_mode(user_id: str, mode: str) -> UserProfile`:
   - Validate `mode in ("SAFE", "BALANCED", "UNRESTRICTED")` — raise `ValueError` if not.
   - `load_profile(user_id)` → set `mode` → `save_profile()` → return updated profile.

**Validation:**

```bash
python -c "
from src.memory.user_profile import load_profile, save_profile, UserProfile
p = UserProfile(user_id='test_u1', name='Test', language='ar')
save_profile(p)
loaded = load_profile('test_u1')
assert loaded.language == 'ar'
assert loaded.name == 'Test'
default = load_profile('nonexistent_user_xyz')
assert default.user_id == 'nonexistent_user_xyz'
print('UserProfile OK')
"
```

**Artifact:** `src/memory/user_profile.py`

---

### TASK 1.8 — Capabilities Manifest YAML

**Location:** `config/runtime/capabilities.yaml`

**Purpose:** Registry source-of-truth. The `CapabilityRegistry` (Phase 8) loads from this file. Every capability entry defines its name, domain, risk level, module path, and input schema.

**Steps:**

1. Create `config/runtime/capabilities.yaml` with all 13 capability entries. Each entry must have:
   - `name`: unique string identifier
   - `domain`: capability domain (system, files, web, etc.)
   - `risk_level`: one of `low | medium | high`
   - `description`: one-line human-readable description
   - `module_path`: fully qualified Python class path
   - `input_schema`: dict of field definitions
   - `platforms`: list of `[windows, linux, macos]`

2. Entries (full schema for each):

   ```yaml
   capabilities:
     - name: open_app
       domain: system
       risk_level: medium
       description: "Launch an application by name on the host OS"
       module_path: "src.capabilities.system.apps.AppLauncher"
       input_schema:
         name:
           {
             type: string,
             required: true,
             description: "Application name to launch",
           }
       platforms: [windows, linux, macos]

     - name: system_info
       domain: system
       risk_level: low
       description: "Return current system hardware and OS information"
       module_path: "src.capabilities.system.sysinfo.SystemInfoCapability"
       input_schema:
         info_type:
           {
             type: string,
             required: false,
             default: "all",
             enum: [all, cpu, ram, gpu, os],
           }
       platforms: [windows, linux, macos]

     - name: clipboard
       domain: system
       risk_level: low
       description: "Read from or write to the system clipboard"
       module_path: "src.capabilities.system.clipboard.ClipboardCapability"
       input_schema:
         action: { type: string, required: true, enum: [read, write] }
         content:
           {
             type: string,
             required: false,
             description: "Content to write (required for write action)",
           }
       platforms: [windows, linux, macos]

     - name: notify
       domain: notify
       risk_level: low
       description: "Send a desktop notification with title and message"
       module_path: "src.capabilities.notify.toasts.NotificationCapability"
       input_schema:
         title: { type: string, required: true }
         message: { type: string, required: true }
         duration: { type: integer, required: false, default: 5 }
       platforms: [windows, linux, macos]

     - name: screenshot
       domain: screen
       risk_level: low
       description: "Capture the screen, optionally with OCR text extraction"
       module_path: "src.capabilities.screen.capture.ScreenshotCapability"
       input_schema:
         ocr: { type: boolean, required: false, default: false }
         region:
           {
             type: object,
             required: false,
             description: "Optional region {x,y,width,height}",
           }
       platforms: [windows, linux, macos]

     - name: file_ops
       domain: files
       risk_level: medium
       description: "Read, write, list, delete, move, or copy files within allowed paths"
       module_path: "src.capabilities.files.file_ops.FileOpsCapability"
       input_schema:
         action:
           {
             type: string,
             required: true,
             enum: [read, write, list, delete, move, copy],
           }
         path:
           {
             type: string,
             required: true,
             description: "Target file or directory path",
           }
         content:
           {
             type: string,
             required: false,
             description: "Content to write (required for write action)",
           }
         destination:
           {
             type: string,
             required: false,
             description: "Destination path (required for move/copy)",
           }
       platforms: [windows, linux, macos]

     - name: code_exec
       domain: coder
       risk_level: high
       description: "Execute code in an isolated subprocess with timeout enforcement"
       module_path: "src.capabilities.coder.executor.CodeExecutorCapability"
       input_schema:
         language:
           { type: string, required: true, enum: [python, javascript, bash] }
         code:
           {
             type: string,
             required: true,
             description: "Source code to execute",
           }
         timeout_s: { type: integer, required: false, default: 30 }
       platforms: [windows, linux, macos]

     - name: web_search
       domain: search
       risk_level: low
       description: "Search the web and return structured results (title, URL, snippet)"
       module_path: "src.capabilities.search.web_search.WebSearchCapability"
       input_schema:
         query: { type: string, required: true }
         count:
           {
             type: integer,
             required: false,
             default: 5,
             description: "Max results to return",
           }
       platforms: [windows, linux, macos]

     - name: browser
       domain: web
       risk_level: medium
       description: "Automate a browser via Playwright (navigate, click, type, screenshot, extract)"
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
       description: "Transcribe speech to text from an audio file or microphone"
       module_path: "src.capabilities.voice.stt.STTCapability"
       input_schema:
         audio_path:
           {
             type: string,
             required: false,
             description: "Path to audio file; if omitted, record from mic",
           }
       platforms: [windows, linux, macos]

     - name: tts
       domain: voice
       risk_level: low
       description: "Synthesize speech from text using Piper TTS"
       module_path: "src.capabilities.voice.tts.TTSCapability"
       input_schema:
         text: { type: string, required: true }
         voice:
           { type: string, required: false, default: "en_US-lessac-medium" }
       platforms: [windows, linux, macos]

     - name: vision_analyze
       domain: vision
       risk_level: low
       description: "Analyze an image using the llava:7b vision model"
       module_path: "src.capabilities.vision.vision.VisionCapability"
       input_schema:
         image_path: { type: string, required: true }
         prompt:
           { type: string, required: false, default: "describe this image" }
       platforms: [windows, linux, macos]

     - name: image_gen
       domain: vision
       risk_level: low
       description: "Generate an image from a text prompt using Stable Diffusion"
       module_path: "src.capabilities.vision.image_gen.ImageGenCapability"
       input_schema:
         prompt: { type: string, required: true }
         size:
           {
             type: string,
             required: false,
             default: "512x512",
             enum: ["512x512", "768x768", "1024x1024"],
           }
       platforms: [windows, linux, macos]
   ```

3. Validate on load: every entry must have `name`, `risk_level` in `[low,medium,high]`, `module_path`, `input_schema`.

**Validation:**

```bash
python -c "
import yaml
caps = yaml.safe_load(open('config/runtime/capabilities.yaml'))['capabilities']
assert all('risk_level' in c for c in caps)
assert all(c['risk_level'] in ('low','medium','high') for c in caps)
assert all('module_path' in c for c in caps)
assert all('input_schema' in c for c in caps)
print(f'{len(caps)} capabilities defined and valid')
"
```

**Artifact:** `config/runtime/capabilities.yaml`

---

### TASK 1.9 — Observability: Metrics Collector

**Location:** `src/core/observability/metrics.py`

**Purpose:** Thread-safe metrics collection. Tracks latency percentiles, error rates, and model usage across all phases.

**Steps:**

1. Create `src/core/observability/metrics.py`.

2. Define `MetricsCollector` as a thread-safe singleton using `threading.Lock`:

   ```python
   _instance: ClassVar['MetricsCollector | None'] = None
   _lock: ClassVar[threading.Lock] = threading.Lock()
   ```

3. Internal state (initialized in `__init__` only if `_instance is None`):

   ```python
   self.latency: dict[str, list[float]] = {}     # phase → [ms values]
   self.errors: dict[str, dict[str, int]] = {}   # phase → {error_type → count}
   self.model_usage: dict[str, dict] = {}        # model → {calls, successes, failures}
   self.turn_count: int = 0
   self._data_lock = threading.Lock()
   ```

4. Implement `record_latency(phase: str, ms: float) -> None` — thread-safe append.

5. Implement `record_error(phase: str, error_type: str) -> None` — thread-safe increment.

6. Implement `record_model_usage(model_name: str, success: bool) -> None` — increment calls/successes/failures.

7. Implement `increment_turn() -> int` — increment turn_count, return new value.

8. Implement `get_summary() -> dict`:
   - For each phase in latency: compute p50 and p95 using `statistics.quantiles(data, n=100)`.
   - Handle fewer than 2 data points gracefully (return 0.0).
   - Include `model_usage` with `success_rate` computed as `successes / calls` (0.0 if calls == 0).

9. Implement `reset() -> None` — clears all state. Used between tests.

**Validation:**

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
mc.reset()
assert mc.turn_count == 0
print('MetricsCollector OK')
"
```

**Artifact:** `src/core/observability/metrics.py`

---

### TASK 1.10 — `app/main.py` Entry Point

**Location:** `app/main.py`

**Purpose:** Canonical application entry point with boot sequence, argument parsing, signal handling, and graceful shutdown.

**Steps:**

1. Create `app/main.py`.

2. Implement `boot_sequence(config) -> None`:
   - Call `setup_logging(level=config.observability.log_level, logs_dir=config.paths.logs_dir)`.
   - Initialize `MetricsCollector()` singleton (no-op since it's singleton, but explicit for boot clarity).
   - Check Ollama: `GET {OLLAMA_BASE_URL}/api/tags` with 2s timeout. If unreachable → print `WARNING: Ollama not reachable. LLM features will fail.` and continue.
   - Create required data directories: `Path("data/profiles/").mkdir(parents=True, exist_ok=True)`, same for `data/images/`, `data/screenshots/`.
   - Print `"JARVIS v3.0 ready"` to stdout.

3. Implement `main() -> None`:
   - Parse `argparse` arguments:
     - `--interface {cli,web}` (default: `cli`)
     - `--debug` flag → override log level to `DEBUG`
     - `--trace` flag → enable per-turn trace replay
     - `--mode {SAFE,BALANCED,UNRESTRICTED}` → override execution mode
     - `--config PATH` → alternate config path (default: `config/runtime/settings.yaml`)
   - Build `cli_overrides` dict from parsed args.
   - Call `load_config(path=args.config, cli_overrides=cli_overrides)`.
   - Call `boot_sequence(config)`.
   - Dispatch: `CLIChat().start()` or `WebApp().start()`.

4. Register shutdown handlers:

   ```python
   _shutdown = False
   def _handle_signal(sig, frame):
       global _shutdown
       _shutdown = True
   signal.signal(signal.SIGINT, _handle_signal)
   signal.signal(signal.SIGTERM, _handle_signal)
   ```

5. Wrap `main()` call in `if __name__ == "__main__": try: main() except KeyboardInterrupt: sys.exit(0)`.

**Failure cases:**

- `settings.yaml` missing → print `ERROR: config/runtime/settings.yaml not found. Copy settings.example.yaml.` → `sys.exit(1)`.
- Any `ValidationError` at boot → print full error → `sys.exit(1)`.

**Validation:**

```bash
python app/main.py --help
# Verify all arguments shown
# Manual test: python app/main.py --interface cli → "JARVIS v3.0 ready" → Ctrl+C exits cleanly
```

**Artifact:** `app/main.py`

---

### TASK 1.11 — EventBus

**Location:** `src/core/observability/event_bus.py`

**Purpose:** In-process publish/subscribe bus for decoupled cross-layer event notification. Used for observability, NOT for control flow. Events are fire-and-forget notifications.

**Steps:**

1. Create `src/core/observability/event_bus.py`.

2. Define `EventBus` as a thread-safe singleton:

   ```python
   class EventBus:
       _instance: ClassVar['EventBus | None'] = None
       _class_lock: ClassVar[threading.Lock] = threading.Lock()

       def __new__(cls):
           with cls._class_lock:
               if cls._instance is None:
                   cls._instance = super().__new__(cls)
                   cls._instance._subscribers: dict[str, list[Callable]] = {}
                   cls._instance._event_lock = threading.Lock()
           return cls._instance
   ```

3. Implement `subscribe(event_type: str, callback: Callable[[dict], None]) -> None`:
   - Thread-safe append to `_subscribers[event_type]`.

4. Implement `publish(event_type: str, data: dict) -> None`:
   - Build event: `{"type": event_type, "data": data, "timestamp": datetime.utcnow().isoformat()}`.
   - Iterate subscriber list for `event_type` (copy list before iterating to avoid mutation during dispatch).
   - Call each callback wrapped in `try/except` — exceptions are caught, logged with `logger.warning`, and NEVER propagated to publisher.
   - `publish` with no subscribers → no-op, no error.

5. Implement `unsubscribe(event_type: str, callback: Callable) -> None` — removes first match.

6. Implement `clear(event_type: str | None = None) -> None`:
   - If `event_type` provided → clear only that event's subscribers.
   - If None → clear all subscribers.
   - Used in test teardown.

7. Define module-level event type constants:
   ```python
   EVT_STATE_TRANSITION = "runtime.state"
   EVT_MODEL_SWAP = "models.swap"
   EVT_TOOL_EXECUTED = "capabilities.executed"
   EVT_TURN_COMPLETE = "runtime.turn_complete"
   EVT_SAFETY_BLOCK = "safety.blocked"
   EVT_DEGRADATION = "runtime.degraded"
   EVT_WAITING_CONFIRMATION = "runtime.waiting_confirmation"
   ```

**Validation:**

```bash
python -c "
from src.core.observability.event_bus import EventBus, EVT_STATE_TRANSITION
bus = EventBus()
received = []
bus.subscribe(EVT_STATE_TRANSITION, lambda e: received.append(e))
bus.publish(EVT_STATE_TRANSITION, {'from': 'IDLE', 'to': 'DECIDING'})
assert len(received) == 1
assert received[0]['data']['to'] == 'DECIDING'
bus.subscribe(EVT_STATE_TRANSITION, lambda e: 1/0)  # bad callback
bus.publish(EVT_STATE_TRANSITION, {'from': 'DECIDING', 'to': 'EXECUTING_MODEL'})
assert len(received) == 2  # publisher was not blocked
bus.clear()
print('EventBus OK')
"
```

**Artifact:** `src/core/observability/event_bus.py`

---

### TASK 1.12 — Custom Exceptions

**Location:** `src/core/exceptions.py`

**Purpose:** Centralized exception hierarchy. All custom errors inherit from `JarvisError`. Prevents catching the wrong exception type.

**Steps:**

1. Create `src/core/exceptions.py`.

2. Define hierarchy (every exception accepts optional `detail: str` kwarg stored as `self.detail`):

   ```python
   class JarvisError(Exception):
       def __init__(self, *args, detail: str = "", **kwargs):
           super().__init__(*args, **kwargs)
           self.detail = detail

   # ── Runtime ──────────────────────────────
   class InvalidTransitionError(JarvisError): ...
   class RetryBudgetExhaustedError(JarvisError): ...
   class TurnTimeoutError(JarvisError): ...

   # ── Models ───────────────────────────────
   class ModelCallError(JarvisError): ...
   class ModelUnavailableError(ModelCallError): ...
   class VRAMInsufficientError(ModelCallError): ...

   # ── Capabilities ─────────────────────────
   class CapabilityNotFoundError(JarvisError): ...
   class CapabilityValidationError(JarvisError): ...
   class CapabilityTimeoutError(JarvisError): ...

   # ── Safety ───────────────────────────────
   class PermissionDeniedError(JarvisError): ...
   class PathTraversalError(PermissionDeniedError): ...

   # ── Decision ─────────────────────────────
   class ParseError(JarvisError): ...
   class ClassifierError(JarvisError): ...
   ```

**Validation:**

```bash
python -c "
from src.core.exceptions import (
    JarvisError, VRAMInsufficientError, ModelCallError, PermissionDeniedError, PathTraversalError
)
assert issubclass(VRAMInsufficientError, ModelCallError)
assert issubclass(ModelCallError, JarvisError)
assert issubclass(PathTraversalError, PermissionDeniedError)
assert issubclass(PermissionDeniedError, JarvisError)
e = VRAMInsufficientError('not enough', detail='need 3200MB, have 512MB')
assert e.detail == 'need 3200MB, have 512MB'
print('Exceptions OK')
"
```

**Artifact:** `src/core/exceptions.py`

---

### TASK 1.13 — `tests/conftest.py` Shared Fixtures

**Location:** `tests/conftest.py`

**Purpose:** Shared pytest fixtures to eliminate duplication across all 15 test files.

**Steps:**

1. Create `tests/conftest.py`.

2. Define all fixtures with lazy imports inside fixture bodies (to avoid circular imports at collection time):

   ```python
   import pytest

   @pytest.fixture
   def default_profile():
       from src.memory.user_profile import UserProfile
       return UserProfile(user_id="test_user", language="en")

   @pytest.fixture
   def default_packet(default_profile):
       from src.core.context.bundle import InputPacket
       return InputPacket(
           user_message="hello",
           session_id="test_session",
           user_profile=default_profile
       )

   @pytest.fixture(autouse=True)
   def reset_metrics():
       yield
       from src.core.observability.metrics import MetricsCollector
       MetricsCollector().reset()

   @pytest.fixture(autouse=True)
   def clear_event_bus():
       yield
       from src.core.observability.event_bus import EventBus
       EventBus().clear()

   @pytest.fixture
   def tmp_db(tmp_path):
       return str(tmp_path / "test_memory.db")

   @pytest.fixture
   def tmp_audit_db(tmp_path):
       return str(tmp_path / "test_audit.db")

   @pytest.fixture
   def mock_ollama(monkeypatch):
       from src.models.llm.engine import OllamaEngine
       monkeypatch.setattr(
           OllamaEngine, "chat_with_model",
           lambda self, model, messages, system="": "mocked response"
       )
       return "mocked response"

   @pytest.fixture
   def balanced_decision():
       from src.core.decision.output import (
           DecisionOutput, Intent, Complexity, ExecutionMode, RiskLevel, DecisionSource
       )
       return DecisionOutput(
           intent=Intent.chat, complexity=Complexity.low, mode=ExecutionMode.fast,
           model="gemma3:4b", requires_tools=False, confidence=0.9,
           risk_level=RiskLevel.low, decision_source=DecisionSource.fast_path
       )
   ```

**Validation:**

```bash
pytest tests/ --collect-only 2>&1 | head -20
# Must show no import errors
```

**Artifact:** `tests/conftest.py`

---

### Definition of Done — Phase 1

- [ ] `python app/main.py --interface cli` prints `JARVIS v3.0 ready`, Ctrl+C exits with code 0.
- [ ] `pytest tests/ --collect-only` runs with 0 errors.
- [ ] `config/runtime/settings.yaml` loads all fields without ValidationError.
- [ ] `from src import __version__` returns `"3.0.0"`.
- [ ] EventBus, exceptions, profiles, and logging all importable.
- [ ] `logs/` directory contains a JSON log file after first run.

---

## Phase 2 — Execution Contract

```yaml
phase_id: 2
priority: "P0"
total_tasks: 10
blocker: "Phase 1 complete"
```

### Objective

Define strict data contracts binding all components. Every contract validates on instantiation and rejects invalid data with a clear error message. These are load-bearing types — all phases depend on them.

---

### TASK 2.0 — Capability Validator Stub

**Location:** `src/capabilities/validator.py`

**Purpose:** Create the `ValidationResult` type and a `SchemaValidator` stub that always returns valid. Phase 6 TASK 6.6 expands this to full schema validation. The stub allows Phase 8 `CapabilityExecutor` to import `SchemaValidator` without waiting for Phase 6.

**Steps:**

1. Create `src/capabilities/validator.py`.

2. Define `ValidationResult` dataclass:

   ```python
   @dataclass
   class ValidationResult:
       valid: bool
       errors: list[str] = field(default_factory=list)

       def first_error(self) -> str | None:
           return self.errors[0] if self.errors else None

       def all_errors(self) -> str:
           return "; ".join(self.errors) if self.errors else ""
   ```

3. Define `SchemaValidator` stub:
   ```python
   class SchemaValidator:
       def validate(self, capability_name: str, args: dict) -> ValidationResult:
           """Stub: always returns valid. Expanded in Phase 6 TASK 6.6."""
           return ValidationResult(valid=True)
   ```

**Validation:**

```bash
python -c "
from src.capabilities.validator import SchemaValidator, ValidationResult
r = SchemaValidator().validate('open_app', {'name': 'notepad'})
assert r.valid
vr = ValidationResult(valid=False, errors=['name is required'])
assert vr.first_error() == 'name is required'
print('Validator stub OK')
"
```

**Artifact:** `src/capabilities/validator.py`

---

### TASK 2.1 — Define `InputPacket`

**Location:** `src/core/context/bundle.py`

**Purpose:** Canonical input container passed through the entire runtime loop. Every component that needs user context receives an `InputPacket`.

**Steps:**

1. Create `src/core/context/bundle.py`.

2. Define `InputPacket` as Pydantic `BaseModel`:

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
       def message_not_empty(cls, v: str) -> str:
           if not v or not v.strip():
               raise ValueError("user_message cannot be empty or whitespace")
           return v.strip()

       @field_validator('session_id')
       @classmethod
       def session_id_not_empty(cls, v: str) -> str:
           if not v:
               raise ValueError("session_id cannot be empty")
           return v
   ```

3. `trace_id` is auto-generated as UUIDv4 if not supplied.

4. `user_message` is stripped of leading/trailing whitespace.

**Success cases:**

- Valid `InputPacket` instantiates without error.
- `trace_id` is auto-populated.

**Failure cases:**

- `user_message=""` → `ValidationError`.
- `user_message="   "` (whitespace-only) → `ValidationError`.
- `session_id=""` → `ValidationError`.

**Validation:**

```bash
python -c "
from src.core.context.bundle import InputPacket
from src.memory.user_profile import UserProfile
p = InputPacket(user_message='  hello  ', session_id='s1', user_profile=UserProfile(user_id='u1'))
assert p.user_message == 'hello'  # stripped
assert len(p.trace_id) == 36      # UUID format
try:
    InputPacket(user_message='', session_id='s1', user_profile=UserProfile(user_id='u1'))
    assert False
except Exception:
    pass
print('InputPacket OK')
"
```

**Artifact:** `src/core/context/bundle.py`

---

### TASK 2.2 — Define `DecisionOutput`

**Location:** `src/core/decision/output.py`

**Purpose:** Structured output of the decision system. Separated from `decision.py` to avoid circular imports.

**Steps:**

1. Create `src/core/decision/output.py`.

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

3. Define `DecisionOutput` as Pydantic `BaseModel` with cross-field validation:

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
       def validate_consistency(self) -> 'DecisionOutput':
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

**Validation:**

```bash
python -c "
from src.core.decision.output import DecisionOutput, Intent, Complexity, ExecutionMode, RiskLevel, DecisionSource
d = DecisionOutput(
    intent=Intent.chat, complexity=Complexity.low, mode=ExecutionMode.fast,
    model='gemma3:4b', requires_tools=False, confidence=0.9,
    risk_level=RiskLevel.low, decision_source=DecisionSource.fast_path
)
assert d.intent == Intent.chat
for bad in [
    dict(confidence=1.5),
    dict(requires_tools=True, tool_name=None),
    dict(decision_source=DecisionSource.model, score_breakdown={}, candidate_list=[]),
]:
    try:
        DecisionOutput(**{**d.model_dump(), **bad}); assert False
    except Exception: pass
print('DecisionOutput OK')
"
```

**Artifact:** `src/core/decision/output.py`

---

### TASK 2.3 — Define `LLMOutput`

**Location:** `src/core/runtime/llm_output.py`

**Steps:**

1. Create `src/core/runtime/llm_output.py`.

2. Define `LLMOutputType(str, Enum)`: values `answer`, `tool_call`.

3. Define `LLMOutput` as Pydantic `BaseModel`:

   ```python
   class LLMOutput(BaseModel):
       type: LLMOutputType
       content: str | None = None
       tool: str | None = None
       args: dict = {}
       raw: str = ""

       @model_validator(mode='after')
       def validate_type_fields(self) -> 'LLMOutput':
           if self.type == LLMOutputType.answer and not self.content:
               raise ValueError("content required when type=answer")
           if self.type == LLMOutputType.tool_call and not self.tool:
               raise ValueError("tool required when type=tool_call")
           return self
   ```

**Validation:**

```bash
python -c "
from src.core.runtime.llm_output import LLMOutput, LLMOutputType
a = LLMOutput(type=LLMOutputType.answer, content='hi')
t = LLMOutput(type=LLMOutputType.tool_call, tool='open_app', args={'name': 'notepad'})
assert a.content == 'hi'
assert t.tool == 'open_app'
for bad_type, bad_kwargs in [
    (LLMOutputType.answer, {}),
    (LLMOutputType.tool_call, {}),
]:
    try: LLMOutput(type=bad_type, **bad_kwargs); assert False
    except Exception: pass
print('LLMOutput OK')
"
```

**Artifact:** `src/core/runtime/llm_output.py`

---

### TASK 2.4 — Define `ToolResult`

**Location:** `src/capabilities/result.py`

**Steps:**

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
       risk_level: str = "low"
       turn_id: int = 0

       @classmethod
       def failure(cls, tool: str, error: str, duration_ms: float = 0.0) -> 'ToolResult':
           return cls(tool=tool, success=False, error=error, duration_ms=duration_ms)

       @classmethod
       def success_result(cls, tool: str, data: dict, duration_ms: float = 0.0, risk_level: str = "low") -> 'ToolResult':
           return cls(tool=tool, success=True, data=data, duration_ms=duration_ms, risk_level=risk_level)
   ```

**Validation:**

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

**Artifact:** `src/capabilities/result.py`

---

### TASK 2.5 — Define `FinalResponse`

**Location:** `src/core/runtime/final_response.py`

**Steps:**

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

       @classmethod
       def error_response(cls, session_id: str, error_text: str, turn_id: int) -> 'FinalResponse':
           """Factory for degraded error responses."""
           return cls(
               text=error_text, session_id=session_id, model="none", mode="error",
               quality=0.0, decision_source=DecisionSource.fast_path,
               degraded=True, turn_id=turn_id
           )
   ```

**Validation:**

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
except Exception: pass
print('FinalResponse OK')
"
```

**Artifact:** `src/core/runtime/final_response.py`

---

### TASK 2.6 — Define `ModelScore`

**Location:** `src/core/decision/model_score.py`

**Steps:**

1. Create `src/core/decision/model_score.py`.

2. Define `ModelScore` as Pydantic `BaseModel`:

   ```python
   class ModelScore(BaseModel):
       model: str
       score: float = Field(ge=0.0, le=1.0)
       factor_scores: dict[str, float]
       vram_available_mb: int = 0
       is_available: bool = True

       @field_validator('factor_scores')
       @classmethod
       def validate_factor_keys(cls, v: dict) -> dict:
           required = {'fit_complexity', 'fit_mode', 'cost_penalty', 'quality_need', 'memory_bias'}
           missing = required - v.keys()
           if missing:
               raise ValueError(f"factor_scores missing required keys: {missing}")
           return v
   ```

**Artifact:** `src/core/decision/model_score.py`

---

### TASK 2.7 — Define `EvaluationResult`

**Location:** `src/core/runtime/evaluation_result.py`

**Steps:**

1. Create `src/core/runtime/evaluation_result.py`.

2. Define `EvaluationResult` as Pydantic `BaseModel`:
   ```python
   class EvaluationResult(BaseModel):
       should_retry: bool
       quality_score: float = Field(ge=0.0, le=1.0)
       issues: list[str] = []
       retry_reason: str = ""
   ```

**Artifact:** `src/core/runtime/evaluation_result.py`

---

### TASK 2.8 — Add `first_error()` to `ValidationResult`

**Location:** `src/capabilities/validator.py` (expand TASK 2.0)

**Steps:**

1. Verify `ValidationResult` has `first_error()` and `all_errors()` methods.
2. If missing, add them (they were defined in TASK 2.0 — this task confirms and tests).

**Validation:**

```bash
python -c "
from src.capabilities.validator import ValidationResult
ok = ValidationResult(valid=True)
assert ok.first_error() is None
err = ValidationResult(valid=False, errors=['name required', 'type invalid'])
assert err.first_error() == 'name required'
assert 'type invalid' in err.all_errors()
print('ValidationResult OK')
"
```

---

### TASK 2.9 — Contract Tests

**Location:** `tests/test_contracts.py`

**Steps:**

1. Create `tests/test_contracts.py` with 20 tests covering all failure and success cases for every contract defined in Phase 2. Use `pytest.raises` for all negative cases.

Required tests:

- `InputPacket` valid instantiation with defaults
- `InputPacket` rejects `user_message=""`
- `InputPacket` rejects `user_message="   "` (whitespace-only)
- `InputPacket` rejects `session_id=""`
- `InputPacket` trace_id is UUID format
- `InputPacket` user_message is stripped
- `DecisionOutput` valid chat instantiation
- `DecisionOutput` rejects `confidence=1.5`
- `DecisionOutput` rejects `requires_tools=True, tool_name=None`
- `DecisionOutput` rejects `decision_source=model` with empty `score_breakdown`
- `LLMOutput` valid answer type
- `LLMOutput` valid tool_call type
- `LLMOutput` rejects `type=answer` with no content
- `LLMOutput` rejects `type=tool_call` with no tool
- `ToolResult` valid instantiation
- `ToolResult.failure()` sets success=False and error correctly
- `FinalResponse` valid instantiation
- `FinalResponse` rejects `quality=1.5`
- `ModelScore` rejects `factor_scores` missing required key
- `ValidationResult.first_error()` returns None when no errors

**Validation:**

```bash
pytest tests/test_contracts.py -v
# Expected: 20 passed
```

**Artifact:** `tests/test_contracts.py`

---

### Definition of Done — Phase 2

`pytest tests/test_contracts.py -v` passes all 20 contract tests.

---

## Phase 3 — Model Manager + VRAM

```yaml
phase_id: 3
priority: "P0"
total_tasks: 5
blocker: "Phase 2 complete"
```

### Objective

VRAM monitoring, model lifecycle management with Ollama's API, and serialized concurrency control.

---

### TASK 3.1 — VRAM Monitor

**Location:** `src/models/vram_monitor.py`

**Purpose:** Real-time VRAM monitoring with caching and hardware fallback. Used by model loader and decision scorer.

**Steps:**

1. Create `src/models/vram_monitor.py`.

2. Define `VRAMMonitor` class with internal state:
   - `_cache_time: float = 0.0`
   - `_cache_available: int = 0`
   - `_cache_total: int = 0`
   - `_cache_ttl: float = 5.0` (seconds)

3. Implement `_read_from_hardware() -> tuple[int, int]` (available_mb, total_mb):

   ```python
   try:
       import pynvml
       pynvml.nvmlInit()
       handle = pynvml.nvmlDeviceGetHandleByIndex(0)
       info = pynvml.nvmlDeviceGetMemoryInfo(handle)
       return info.free // (1024*1024), info.total // (1024*1024)
   except Exception:
       logger.warning("pynvml unavailable, using heuristic VRAM values")
       return 4096, 6144  # RTX 3050 conservative heuristic
   ```

4. Implement `get_available_vram_mb() -> int` — use cache if age < `_cache_ttl`, else re-read.

5. Implement `get_total_vram_mb() -> int` — same caching logic.

6. Implement `is_model_loadable(required_vram_mb: int) -> bool`:
   - Returns `get_available_vram_mb() >= required_vram_mb + 512` (512MB safety margin).

7. Implement `force_refresh() -> None` — sets `_cache_time = 0.0` to force re-read on next call.

**Validation:**

```bash
python -c "
from src.models.vram_monitor import VRAMMonitor
vm = VRAMMonitor()
avail = vm.get_available_vram_mb()
total = vm.get_total_vram_mb()
assert avail > 0
assert total >= avail
assert not vm.is_model_loadable(10000)  # impossible on any consumer GPU
print(f'VRAM: {avail}/{total} MB')
"
```

**Artifact:** `src/models/vram_monitor.py`

---

### TASK 3.2 — Model Lifecycle Manager

**Location:** `src/models/manager.py`

**Purpose:** Load, unload, and swap models via Ollama's API. Enforces one-model-at-a-time with a threading.Lock. All state mutations go through the lock.

**Steps:**

1. Create `src/models/manager.py`.

2. Define `ModelManager` as a singleton class with internal state:
   - `_current_model: str | None = None`
   - `_lock: threading.Lock`
   - `_busy: bool = False`
   - `_call_count: int = 0`

3. Implement `load_model(model_name: str) -> None`:
   - Acquire lock (with 120s timeout — raise `TimeoutError` if exceeded).
   - If `_current_model == model_name`: release lock, return (no-op).
   - If `_current_model is not None`: call `unload_model(_current_model)`.
   - Check VRAM: `VRAMMonitor().is_model_loadable(profile.vram_required_mb)` → raise `VRAMInsufficientError` if insufficient.
   - Send warm-up: `POST {OLLAMA_URL}/api/generate {"model": model_name, "keep_alive": "10m", "prompt": ""}`.
   - Set `_current_model = model_name`.
   - Publish `EVT_MODEL_SWAP` to EventBus.
   - Release lock.

4. Implement `unload_model(model_name: str) -> None`:
   - Send: `POST {OLLAMA_URL}/api/generate {"model": model_name, "keep_alive": 0, "prompt": ""}` — Ollama's official unload mechanism.
   - Set `_current_model = None`.
   - Publish `EVT_MODEL_SWAP` to EventBus.

5. Implement `swap_model(to_model: str) -> None` — single lock acquisition for unload+load.

6. Implement `get_current_model() -> str | None`.
7. Implement `is_model_loaded(model_name: str) -> bool`.
8. Implement `is_busy() -> bool`.

**Failure cases:**

- VRAM insufficient → `VRAMInsufficientError`.
- Ollama connection error → `ModelCallError("Ollama not reachable")`.
- Lock timeout → `TimeoutError("ModelManager lock timeout after 120s")`.

**Artifact:** `src/models/manager.py`

---

### TASK 3.3 — Concurrency Control

**Location:** `src/models/manager.py` (expand TASK 3.2)

**Purpose:** Verify that concurrent model load requests serialize correctly — the second waits for the first to complete.

**Steps:**

1. All `ModelManager` methods already use the lock from TASK 3.2.
2. Add `_queue_depth: int = 0` counter to track waiters.
3. Write concurrency test inline in task validation.

**Validation:**

```python
import threading
from src.models.manager import ModelManager
results = []
errors = []

def load_and_record():
    try:
        mm = ModelManager()
        mm.load_model('gemma3:4b')
        results.append(mm.get_current_model())
    except Exception as e:
        errors.append(str(e))

t1 = threading.Thread(target=load_and_record)
t2 = threading.Thread(target=load_and_record)
t1.start(); t2.start(); t1.join(); t2.join()
assert not errors, f"Errors: {errors}"
assert all(r == 'gemma3:4b' for r in results)
```

---

### TASK 3.4 — Model Availability Registry

**Location:** `src/models/availability.py`

**Purpose:** Query Ollama for installed models and cross-reference with VRAM availability. Cached for 30 seconds.

**Steps:**

1. Create `src/models/availability.py`.

2. Define `ModelAvailability` with state:
   - `_available: list[str] = []`
   - `_cache_time: float = 0.0`
   - `_cache_ttl: float = 30.0`

3. Implement `refresh() -> None`:
   - `GET {OLLAMA_URL}/api/tags` → parse `{"models": [{"name": ...}, ...]}`.
   - Filter to models in `PROFILES` (known models only).
   - Further filter to `VRAMMonitor().is_model_loadable(profile.vram_required_mb)`.
   - Store result in `_available`.
   - If Ollama unreachable → set `_available = []`, log WARNING.

4. Implement `get_available_models() -> list[str]` — auto-refresh if cache expired.

5. Implement `is_available(model_name: str) -> bool`.

**Artifact:** `src/models/availability.py`

---

### TASK 3.5 — LLM Engine Expansion

**Location:** `src/models/llm/engine.py` (expand Phase 0 artifact)

**Purpose:** Add `chat_with_model()` with full error handling, timeout, and metrics recording. Retain `chat()` for backward compatibility during Phase 0 → Phase 9 migration.

**Steps:**

1. Expand `src/models/llm/engine.py`.

2. Add `ModelManager` instance: `self._manager = ModelManager()`.

3. Implement `chat_with_model(model_name: str, messages: list[dict], system: str = "") -> str`:
   - Call `self._manager.load_model(model_name)` (no-op if already loaded).
   - Build messages array: prepend `{"role": "system", "content": system}` if `system` is non-empty.
   - `POST {OLLAMA_URL}/api/chat {"model": model_name, "messages": [...], "stream": False}` with `timeout=config.models.timeout_s`.
   - Handle errors:
     - `requests.Timeout` → raise `ModelCallError("model timeout")`
     - `requests.ConnectionError` → raise `ModelCallError("Ollama not reachable")`
     - Non-200 response → raise `ModelCallError(f"Ollama HTTP {status_code}")`
   - Return `response.json()["message"]["content"]`.
   - Record latency to `MetricsCollector.record_latency("model", elapsed_ms)`.
   - Record model usage to `MetricsCollector.record_model_usage(model_name, success=True/False)`.

4. Mark existing `chat()` as deprecated: `warnings.warn("chat() deprecated, use chat_with_model()", DeprecationWarning)`.

**Artifact:** `src/models/llm/engine.py`

---

### Definition of Done — Phase 3

VRAM monitor returns valid readings. `ModelManager` loads, unloads, and swaps. Concurrency is serialized. Availability registry returns correct list.

---

## Phase 4 — Runtime State Machine

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

**Location:** `src/core/runtime/state.py`

**Steps:**

1. Create `src/core/runtime/state.py`.

2. Define `RuntimeState(str, Enum)` with values: `IDLE`, `DECIDING`, `EXECUTING_MODEL`, `EXECUTING_TOOL`, `WAITING_CONFIRMATION`, `EVALUATING`, `ERROR`, `COMPLETED`.

3. Define `ALLOWED_TRANSITIONS: dict[RuntimeState, frozenset[RuntimeState]]`:

   ```python
   ALLOWED_TRANSITIONS = {
       RuntimeState.IDLE:                 frozenset({RuntimeState.DECIDING}),
       RuntimeState.DECIDING:             frozenset({RuntimeState.EXECUTING_MODEL, RuntimeState.EXECUTING_TOOL, RuntimeState.ERROR}),
       RuntimeState.EXECUTING_MODEL:      frozenset({RuntimeState.EVALUATING, RuntimeState.EXECUTING_TOOL, RuntimeState.ERROR}),
       RuntimeState.EXECUTING_TOOL:       frozenset({RuntimeState.WAITING_CONFIRMATION, RuntimeState.EVALUATING, RuntimeState.ERROR}),
       RuntimeState.WAITING_CONFIRMATION: frozenset({RuntimeState.EXECUTING_TOOL, RuntimeState.ERROR, RuntimeState.IDLE}),
       RuntimeState.EVALUATING:           frozenset({RuntimeState.COMPLETED, RuntimeState.DECIDING, RuntimeState.ERROR}),
       RuntimeState.ERROR:                frozenset({RuntimeState.IDLE}),
       RuntimeState.COMPLETED:            frozenset({RuntimeState.IDLE}),
   }
   ```

4. Implement `can_transition(from_state: RuntimeState, to_state: RuntimeState) -> bool`.

**Artifact:** `src/core/runtime/state.py`

---

### TASK 4.2 — State Manager

**Location:** `src/core/runtime/state_manager.py`

**Steps:**

1. Create `src/core/runtime/state_manager.py`.

2. Define `StateManager` class with:
   - `_state: RuntimeState = RuntimeState.IDLE`
   - `_history: list[tuple[RuntimeState, RuntimeState, str, str]]` (from, to, timestamp, reason)
   - `_lock: threading.Lock`

3. Property `current_state -> RuntimeState`.

4. Implement `transition_to(new_state: RuntimeState, reason: str = "") -> None`:
   - Acquire lock.
   - Check `can_transition(self._state, new_state)` → if invalid: raise `InvalidTransitionError(f"{self._state} → {new_state} not allowed")`.
   - Record `(old_state, new_state, datetime.utcnow().isoformat(), reason)` in history.
   - Set `self._state = new_state`.
   - Call `log_event(f"state.transition", phase="runtime", data={"from": old_state, "to": new_state, "reason": reason})`.
   - Publish `EVT_STATE_TRANSITION` to EventBus.
   - Release lock.

5. Implement `force_state(state: RuntimeState, reason: str = "force") -> None`:
   - Log WARNING: `f"FORCED STATE TRANSITION: {self._state} → {state} reason={reason}"`.
   - Set state directly without validation. For error recovery only.

6. Implement `get_history() -> list[tuple]`.
7. Implement `reset() -> None` → `force_state(IDLE, "reset")` + clear history.

**Artifact:** `src/core/runtime/state_manager.py`

---

### TASK 4.3 — Hard Limits

**Location:** `src/core/runtime/limits.py`

**Purpose:** Single authoritative source for all numeric execution limits. Loaded from config. Consumed by the runtime loop.

**Steps:**

1. Create `src/core/runtime/limits.py`.

2. Define `Limits` class:

   ```python
   class Limits:
       def __init__(self, config=None):
           cfg = config or load_config().execution
           self.max_iterations: int = cfg.max_iterations
           self.max_tool_calls: int = cfg.max_tool_calls
           self.max_tool_depth: int = cfg.max_tool_depth
           self.max_decision_retries: int = cfg.max_decision_retries
           self.max_model_retries: int = cfg.max_model_retries
           self.global_retry_budget: int = cfg.global_retry_budget
           self.tool_timeout_s: int = cfg.tool_timeout_s
           self.model_timeout_s: int = cfg.model_timeout_s
           self.step_timeout_s: int = cfg.step_timeout_s
           self.total_turn_timeout_s: int = cfg.total_turn_timeout_s
   ```

3. Implement `check_limit(limit_name: str, current_value: int) -> bool`:
   - Returns `True` if `current_value < getattr(self, limit_name)` — still within limit, OK to continue.
   - Returns `False` if `current_value >= getattr(self, limit_name)` — limit reached, must stop.
   - Raises `AttributeError` if `limit_name` not a known attribute — this is a programming error.
   - **Semantics:** `check_limit("max_iterations", 4)` → True (4 < 5). `check_limit("max_iterations", 5)` → False (5 >= 5).

**Artifact:** `src/core/runtime/limits.py`

---

### TASK 4.4 — Context Assembler

**Location:** `src/core/context/assembler.py`

**Steps:**

1. Create `src/core/context/assembler.py`.

2. Define `ContextAssembler` class.

3. Implement `assemble(user_input: str, session_id: str, turn_number: int = 0) -> InputPacket`:
   - Load profile: `load_profile("default")` — cold start returns default profile.
   - Fetch history: attempt `MemoryDB().retrieve_recent(session_id, limit=5)` — empty list on cold start.
   - Return `InputPacket(user_message=user_input, session_id=session_id, user_profile=profile, recent_history=history, turn_number=turn_number)`.

4. Cold start (no DB, no history) is not an error — empty lists are valid.

**Artifact:** `src/core/context/assembler.py`

---

### TASK 4.5 — Executor (LLM call layer)

**Location:** `src/core/runtime/executor.py`

**Purpose:** Execute a single LLM call based on a `DecisionOutput`. Returns `LLMOutput`. Does not handle retries — caller manages that.

**Steps:**

1. Create `src/core/runtime/executor.py`.

2. Define `Executor` class with `_prompt_builder` (stub until Phase 10).

3. Implement `execute(decision: DecisionOutput, input_packet: InputPacket) -> LLMOutput`:
   - Build system prompt: stub returns `"You are JARVIS."` until Phase 10 wires `PromptBuilder`.
   - Build messages from `input_packet.recent_history` + current user message.
   - Call `OllamaEngine().chat_with_model(decision.model, messages, system=prompt)`.
   - Attempt JSON parse of response:
     - If response contains `{"tool": ..., "args": ...}` → return `LLMOutput(type=tool_call, tool=..., args=..., raw=raw_text)`.
     - Else → return `LLMOutput(type=answer, content=raw_text, raw=raw_text)`.
   - On `ModelCallError` → re-raise (caller handles via fallback).
   - On JSON parse failure → return `LLMOutput(type=answer, content=raw_text, raw=raw_text)`.
   - Record latency to `MetricsCollector`.

**Artifact:** `src/core/runtime/executor.py`

---

### TASK 4.6 — Evaluator

**Location:** `src/core/runtime/evaluator.py`

**Purpose:** Heuristic quality evaluation. No LLM call. Used to decide whether to retry.

**Steps:**

1. Create `src/core/runtime/evaluator.py`.

2. Implement `should_evaluate(output: LLMOutput, decision: DecisionOutput) -> bool`:
   - Returns True if: `len(output.content or "") > 500`, OR `decision.complexity == "high"`, OR `decision.degraded` (attribute check, may not exist — use `getattr`).

3. Implement `evaluate(output: LLMOutput, decision: DecisionOutput, input_packet: InputPacket) -> EvaluationResult`:
   - **Completeness** (weight 0.4): content ends with `.`, `!`, `?`, or common conclusion word → 1.0; else 0.5.
   - **Relevance** (weight 0.4): count key terms from `user_message` that appear in content. Divide by total terms. Clamp to [0, 1].
   - **Coherence** (weight 0.2): content length > 10 chars AND not starting with "Error" or "I cannot" → 1.0; else 0.3.
   - `quality_score = completeness * 0.4 + relevance * 0.4 + coherence * 0.2`.
   - `should_retry = quality_score < 0.4`.

**Artifact:** `src/core/runtime/evaluator.py`

---

### TASK 4.7 — Runtime Loop

**Location:** `src/core/runtime/loop.py`

**Purpose:** The main `run_turn()` function. Orchestrates all components through state transitions. Never raises exceptions — always returns `FinalResponse`.

**Steps:**

1. Create `src/core/runtime/loop.py`.

2. Define `run_turn(user_input: str, session_id: str, mode_override: str | None = None) -> FinalResponse`.

3. Instantiate per-turn: `StateManager`, `Limits`, `ContextAssembler`, `Executor`, `Evaluator`, `RetryManager` (stub until Phase 11).

4. Track: `iteration_count = 0`, `tool_call_count = 0`, `turn_start_time = time.time()`, `turn_id = MetricsCollector().increment_turn()`.

5. **Decision stub** (used until Phase 5 replaces it):

   ```python
   def _stub_decide(input_packet: InputPacket) -> DecisionOutput:
       return DecisionOutput(
           intent=Intent.chat, complexity=Complexity.low, mode=ExecutionMode.fast,
           model=load_config().models.default, requires_tools=False, confidence=0.9,
           risk_level=RiskLevel.low, decision_source=DecisionSource.fast_path
       )
   ```

6. **Tool execution stub** (used until Phase 8 provides `CapabilityExecutor`):

   ```python
   def _stub_execute_tool(decision: DecisionOutput) -> ToolResult:
       return ToolResult(tool=decision.tool_name or "unknown", success=True, data={"stub": True})
   ```

7. Main loop:

   ```
   transition IDLE → DECIDING
   assemble InputPacket
   call decide() (stub)
   if intent == tool_use:
       transition DECIDING → EXECUTING_TOOL
       execute tool (stub)
       transition EXECUTING_TOOL → EVALUATING
   else:
       transition DECIDING → EXECUTING_MODEL
       call Executor.execute()
       transition EXECUTING_MODEL → EVALUATING
   evaluate if should_evaluate()
   if should_retry and check_limit("max_iterations", iteration_count):
       transition EVALUATING → DECIDING; iteration_count += 1; continue
   transition EVALUATING → COMPLETED
   transition COMPLETED → IDLE
   publish EVT_TURN_COMPLETE
   return FinalResponse
   ```

8. Turn timeout: after each iteration, check `time.time() - turn_start_time > limits.total_turn_timeout_s` → raise `TurnTimeoutError`.

9. Exception handler: on any `JarvisError` → `transition_to(ERROR)` → `transition_to(IDLE)` → return `FinalResponse.error_response(session_id, degradation_message, turn_id)`.

**Artifact:** `src/core/runtime/loop.py`

---

### TASK 4.8 — State Machine Tests

**Location:** `tests/test_state_machine.py`

**Required tests (12 total):**

1. `IDLE → DECIDING` allowed
2. `IDLE → EXECUTING_TOOL` raises `InvalidTransitionError`
3. `ERROR → IDLE` allowed
4. `COMPLETED → IDLE` allowed
5. `COMPLETED → DECIDING` raises `InvalidTransitionError`
6. `force_state()` bypasses validation
7. `StateManager.reset()` returns to IDLE and clears history
8. History records all transitions with timestamps
9. `check_limit("max_iterations", 4)` → True; `("max_iterations", 5)` → False
10. `run_turn("hello", "test_session")` returns `FinalResponse` with non-empty text
11. `run_turn` when Ollama unavailable → returns degraded `FinalResponse` without crash
12. EventBus receives `EVT_STATE_TRANSITION` on each transition

**Artifact:** `tests/test_state_machine.py`

---

### Definition of Done — Phase 4

`run_turn("hello", "test")` returns `FinalResponse`. All transitions enforced. All limits checked. `pytest tests/test_state_machine.py -v` passes all 12 tests.

---

## Phase 5 — Decision System

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

**Location:** `src/core/decision/classifier.py`

**Steps:**

1. Expand `src/core/decision/classifier.py`.

2. Define `extract_json(text: str) -> dict | None`:
   - Step 1: Strip markdown fences: `re.sub(r'```json\s*|```\s*', '', text).strip()`.
   - Step 2: `json.loads(stripped)` — if success, return result.
   - Step 3: On `JSONDecodeError` — find first `{` and last `}`, try parsing substring.
   - Step 4: If still failing → call `repair_json(text)` and try once more.
   - Step 5: Return None on all failures.

3. Define `repair_json(text: str) -> str | None`:
   - Remove trailing commas before `}` or `]`: `re.sub(r',\s*([}\]])', r'\1', text)`.
   - Replace unquoted single-quote strings with double-quotes: `re.sub(r"'([^']*)'", r'"\1"', text)`.
   - Try `json.loads(repaired)` — return repaired string if success, None otherwise.

4. Implement `Classifier` class with `classify(message: str) -> DecisionOutput`:
   - Build system prompt: `"Respond ONLY with valid JSON. Keys: intent (chat|tool_use|planning|search), complexity (low|medium|high), tool_name (string or null), tool_args (object), confidence (float 0.0-1.0). No other text."`.
   - Call `OllamaEngine().chat_with_model(default_model, [{"role":"user","content":message}], system=prompt)`.
   - Try `extract_json(response)`.
   - On None: log warning, sleep 1s (exponential backoff), retry once.
   - On second failure: return `_safe_fallback()`.
   - Map JSON to `DecisionOutput`.

5. Define `_safe_fallback() -> DecisionOutput`:
   - Always returns `intent=chat, model=default, confidence=0.5, decision_source=fast_path`.

**Artifact:** `src/core/decision/classifier.py`

---

### TASK 5.2 — Fast-Path Rules

**Location:** `src/core/decision/fast_path.py`

**Purpose:** Zero-latency decision for common patterns. Regex-based matching, no LLM call. Bilingual English/Arabic.

**Steps:**

1. Create `src/core/decision/fast_path.py`.

2. Define `FastPath` class. Compile all rules at instantiation time.

3. Rules list (each is a `(compiled_pattern, factory_function)` tuple):

   ```python
   rules = [
       # App launch — English
       (re.compile(r"^(open|launch|start|run)\s+(.+)", re.I), lambda m: _make_tool("open_app", {"name": m.group(2)})),
       # App launch — Arabic
       (re.compile(r"^(افتح|شغّل|شغل|ابدأ)\s+(.+)"), lambda m: _make_tool("open_app", {"name": m.group(2)})),
       # General question — English
       (re.compile(r"^(what is|what's|who is|define|explain|tell me about)\s+(.+)", re.I), lambda m: _make_chat()),
       # General question — Arabic
       (re.compile(r"^(ما هو|ما هي|من هو|اشرح|عرّف)\s+(.+)"), lambda m: _make_chat()),
       # Web search — English
       (re.compile(r"^(search for|find|look up|search)\s+(.+)", re.I), lambda m: _make_tool("web_search", {"query": m.group(2)})),
       # Web search — Arabic
       (re.compile(r"^(ابحث عن|ابحث|ابحث في)\s+(.+)"), lambda m: _make_tool("web_search", {"query": m.group(2)})),
       # Screenshot
       (re.compile(r"^(take a screenshot|screenshot|capture screen)", re.I), lambda m: _make_tool("screenshot", {})),
       # System info
       (re.compile(r"^(system info|cpu usage|ram usage|what's my (cpu|ram|memory|gpu))", re.I), lambda m: _make_tool("system_info", {})),
       # Clipboard read
       (re.compile(r"^(read clipboard|what's in (my )?clipboard|paste)", re.I), lambda m: _make_tool("clipboard", {"action": "read"})),
   ]
   ```

4. Implement `check(message: str) -> DecisionOutput | None`:
   - Iterate rules, return first match.
   - Return None if no match.
   - All fast-path outputs: `decision_source=fast_path`, `score_breakdown={}`, `candidate_list=[]`, `complexity=low`, `mode=fast`, `confidence=0.95`.

**Artifact:** `src/core/decision/fast_path.py`

---

### TASK 5.3 — Dynamic Model Scorer

**Location:** `src/core/decision/scorer.py`

**Purpose:** Weighted scoring of all available models. Factor names MUST match `config/runtime/models.yaml` weight keys exactly.

**Steps:**

1. Create `src/core/decision/scorer.py`.

2. Define `ModelScorer`. Load weights from `config/runtime/models.yaml` at instantiation.

3. Normalization tables:

   ```python
   REASONING_SCORES = {"low": 0.3, "medium": 0.7, "high": 1.0}
   LATENCY_SCORES   = {"fast": 1.0, "medium": 0.6, "slow": 0.3}
   COMPLEXITY_MAP   = {"low": 0.3, "medium": 0.6, "high": 1.0}
   MODE_LATENCY_MAP = {"fast": 1.0, "normal": 0.6, "deep": 0.3, "planning": 0.4, "research": 0.3}
   MAX_VRAM_MB      = 6144  # RTX 3050 max for normalization
   ```

4. Implement `score(model_name: str, complexity: str, mode: str, vram_available_mb: int, memory_bias: float = 0.5) -> ModelScore`:
   - If profile is None or model unavailable → return zero-score ModelScore with `is_available=False`.
   - `fit_complexity = 1.0 - abs(REASONING_SCORES[profile.reasoning_tier] - COMPLEXITY_MAP[complexity])`
   - `fit_mode = 1.0 - abs(LATENCY_SCORES[profile.latency_tier] - MODE_LATENCY_MAP[mode])`
   - `cost_penalty = 1.0 - (profile.vram_required_mb / MAX_VRAM_MB)`
   - `quality_need = REASONING_SCORES[profile.reasoning_tier]`
   - `memory_bias = memory_bias` (already normalized)
   - `weighted_score = sum(weights[k] * factor_scores[k] for k in weights)`

5. Implement `rank_models(complexity: str, mode: str, vram_available_mb: int) -> list[ModelScore]`:
   - Score all profiles from `list_profiles()`.
   - Filter to `is_available=True` (cross-reference with `ModelAvailability()`).
   - Sort descending by score.
   - Tie-break: lower `cost_penalty` → lower vram → alphabetical. This ensures determinism.

**Artifact:** `src/core/decision/scorer.py`

---

### TASK 5.4 — Risk Assessment

**Location:** `src/core/decision/risk.py`

**Steps:**

1. Create `src/core/decision/risk.py`.

2. Define `RiskAssessor` with risk tables:

   ```python
   TOOL_RISK = {
       "open_app": "medium", "system_info": "low", "clipboard": "low",
       "notify": "low", "screenshot": "low", "file_ops": "medium",
       "code_exec": "high", "web_search": "low", "browser": "medium",
       "stt": "low", "tts": "low", "vision_analyze": "low", "image_gen": "low",
   }
   FILE_ACTION_RISK = {
       "delete": "high", "write": "medium", "move": "medium",
       "copy": "medium", "read": "low", "list": "low",
   }
   ```

3. Implement `assess(decision: DecisionOutput) -> RiskLevel`:
   - No tool → `RiskLevel.low`.
   - Look up base risk from `TOOL_RISK.get(decision.tool_name, "high")`.
   - `file_ops` + action in `FILE_ACTION_RISK` → use override.
   - Path contains `..` → `high`.
   - Path starts with blocked path → `high`.
   - Return highest of all computed levels.

**Artifact:** `src/core/decision/risk.py`

---

### TASK 5.5 — Unified `decide()` Function

**Location:** `src/core/decision/decision.py`

**Steps:**

1. Create `src/core/decision/decision.py`.

2. Define `decide(input_packet: InputPacket) -> DecisionOutput`:
   - Step 1: FastPath check → if matched, assess risk, return immediately.
   - Step 2: Classifier call → partial DecisionOutput.
   - Step 3: Get VRAM → rank models → select best.
   - Step 4: Risk assessment on final decision.
   - Step 5: Construct DecisionOutput with `score_breakdown`, `candidate_list` (top 3), `decision_source=model`.
   - Step 6: Validate → if invalid, return `_safe_default(input_packet)`.

3. Define `_safe_default(input_packet: InputPacket) -> DecisionOutput`:
   - Returns chat intent, tier_2 fallback model, confidence=0.3, `decision_source=fast_path`.

**Artifact:** `src/core/decision/decision.py`

---

### TASK 5.6 — Escalation Chain

**Location:** `src/core/runtime/escalation.py`

**Steps:**

1. Create `src/core/runtime/escalation.py`.

2. Define `EscalationChain` with `retry(input_packet: InputPacket, attempt: int) -> DecisionOutput`:
   - attempt 1 → standard `decide()`.
   - attempt 2 → adjust weights +0.05 `fit_complexity`, -0.05 `cost_penalty`, re-decide.
   - attempt 3 → force `tier_1` model from config, re-decide.
   - attempt >= 4 → `_safe_default()` with `tier_2` model.

**Artifact:** `src/core/runtime/escalation.py`

---

### TASK 5.7 — Decision Tests

**Location:** `tests/test_decision.py`

**Required tests (14):**

1. Fast path: `"open notepad"` → `tool_use, open_app`
2. Fast path: `"افتح المفكرة"` → `tool_use, open_app`
3. Fast path: `"system info"` → `tool_use, system_info`
4. Fast path: `"tell me a joke"` → None
5. `extract_json` handles markdown fences
6. `extract_json` handles trailing comma
7. `extract_json` returns None for garbage
8. `ModelScorer.score` returns all 5 required factor keys
9. `ModelScorer.rank_models` returns highest score first
10. `RiskAssessor` returns `high` for `code_exec`
11. `RiskAssessor` returns `high` for `file_ops` + `delete` action
12. `decide("open notepad")` → `decision_source=fast_path`
13. `decide()` returns `score_breakdown` and `candidate_list` for model-path
14. Escalation attempt 3 forces tier_1 model

**Artifact:** `tests/test_decision.py`

---

### Definition of Done — Phase 5

Fast path operational. Dynamic scoring uses all 5 factors with exact key names. All 14 tests pass.

---

## Phase 6 — Sandbox + Safety

```yaml
phase_id: 6
priority: "P0"
total_tasks: 7
blocker: "Phase 5 complete"
```

---

### TASK 6.1 — Execution Sandbox

**Location:** `src/core/sandbox/sandbox.py`

**Purpose:** Execute capabilities in isolation with timeout enforcement, exception wrapping, and duration tracking.

**Steps:**

1. Create `src/core/sandbox/sandbox.py`.

2. Define `Sandbox` class.

3. Implement `execute(capability: BaseCapability, args: dict, timeout_s: int) -> ToolResult`:
   - Record `start = time.time()`.
   - Submit `capability.execute(args)` to `concurrent.futures.ThreadPoolExecutor(max_workers=1)`.
   - Wait with `future.result(timeout=timeout_s)`.
   - On `concurrent.futures.TimeoutError` → return `ToolResult.failure(capability.name, f"timeout after {timeout_s}s")`.
   - On any other `Exception` → log error → return `ToolResult.failure(capability.name, str(e))`.
   - On success → set `result.duration_ms = (time.time() - start) * 1000`.
   - Optional: after execution, check `psutil.Process().memory_info().rss` — if > 2GB, log WARNING.
   - Publish `EVT_TOOL_EXECUTED` to EventBus on success.

4. Implement `dry_run(capability: BaseCapability, args: dict) -> ToolResult`:
   - Call `capability.dry_run(args)` directly (no timeout wrapping — dry run must be fast).
   - Set `result.dry_run = True`.

5. Maintain `_rollback_log: list[str]` — capabilities append rollback descriptors (e.g., `"file_write:/path/to/file"`).

**Artifact:** `src/core/sandbox/sandbox.py`

---

### TASK 6.2 — Safety Classifier

**Location:** `src/core/safety/classifier.py`

**Purpose:** Classify the risk of a capability execution based on structured argument inspection.

**Steps:**

1. Create `src/core/safety/classifier.py`.

2. Define `SafetyClassifier`. Load `blocked_paths` and `allowed_roots` from config.

3. Implement `classify(capability_name: str, args: dict) -> RiskLevel`:
   - Step 1: Load base risk from `config/runtime/capabilities.yaml` for `capability_name`. Unknown capability → `high`.
   - Step 2: Path traversal check — iterate all string arg values. If any contains `..` → return `high`.
   - Step 3: Blocked path check — if any string arg value starts with a blocked path string → return `high`. Use case-insensitive comparison on Windows.
   - Step 4: For `code_exec` — inspect `args.get("code", "")` for dangerous patterns: `__import__`, `subprocess`, `os.system`, `exec(`, `eval(` → return `high`.
   - Step 5: Return base risk if no overrides triggered.

4. Use structured argument checking only — NEVER pattern-match on the user's original message.

**Artifact:** `src/core/safety/classifier.py`

---

### TASK 6.3 — Mode Enforcer

**Location:** `src/core/safety/mode_enforcer.py`

**Steps:**

1. Create `src/core/safety/mode_enforcer.py`.

2. Define `Permission(str, Enum)`: `allow`, `confirm`, `block`.

3. Define `ModeEnforcer`. Implement `check_permission(capability_name: str, risk_level: RiskLevel, mode: str) -> Permission`:

   ```
   SAFE:
     all risk levels → confirm

   BALANCED:
     low  → allow
     medium → confirm
     high → block
     (exception: if args contains _override_phrase="I understand the risk" → confirm for high)

   UNRESTRICTED:
     all → allow  (schema and path validation still apply)
   ```

4. Publish `EVT_SAFETY_BLOCK` when returning `block`.

**Artifact:** `src/core/safety/mode_enforcer.py`

---

### TASK 6.4 — Permission Layer (Three-Gate System)

**Location:** `src/core/safety/permission.py`

**Purpose:** Single entry point for all permission decisions. Combines decision consistency, argument safety, and schema validation into three sequential gates.

**Steps:**

1. Create `src/core/safety/permission.py`.

2. Define `PermissionLayer`. Implement `check(tool_name: str, args: dict, decision: DecisionOutput, mode: str) -> tuple[Permission, str]`:
   - **Gate 1 — Decision Consistency:** `tool_name == decision.tool_name` → pass. Mismatch → return `(block, "tool mismatch: expected {decision.tool_name}, got {tool_name}")`.
   - **Gate 2 — Argument Safety:** `SafetyClassifier().classify(tool_name, args)` → risk. `ModeEnforcer().check_permission(tool_name, risk, mode)` → permission. If permission is `block` → return `(block, "permission denied by mode {mode} for risk {risk}")`.
   - **Gate 3 — Schema Validity:** `SchemaValidator().validate(tool_name, args)` → if not valid → return `(block, result.all_errors())`.
   - All gates pass → return `(permission_from_gate2, "")`.

3. Log every gate result to `AuditLogger` (TASK 6.5).

**Artifact:** `src/core/safety/permission.py`

---

### TASK 6.5 — Audit Logger

**Location:** `src/core/safety/audit.py`

**Steps:**

1. Create `src/core/safety/audit.py`.

2. Define `AuditLogger` with SQLite at `config.paths.audit_db`. Enable WAL journal mode.

3. Schema:

   ```sql
   CREATE TABLE IF NOT EXISTS audit_log (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       timestamp TEXT NOT NULL,
       session_id TEXT NOT NULL,
       turn_id INTEGER,
       tool_name TEXT,
       args TEXT,
       gate1 TEXT,
       gate2 TEXT,
       gate3 TEXT,
       final_decision TEXT,
       reason TEXT
   )
   ```

4. Implement `log_action(tool_name: str, args: dict, gate_results: dict, decision: str, session_id: str, turn_id: int, reason: str = "") -> None`.

5. Implement `get_audit_log(session_id: str, limit: int = 50) -> list[dict]`.

**Artifact:** `src/core/safety/audit.py`

---

### TASK 6.6 — Schema Validator (Full Implementation)

**Location:** `src/capabilities/validator.py` (expand TASK 2.0 stub)

**Steps:**

1. Expand `SchemaValidator` class:
   - Load `config/runtime/capabilities.yaml` at instantiation.
   - Build lookup: `{capability_name: input_schema}`.

2. Expand `validate(capability_name: str, args: dict) -> ValidationResult`:
   - Unknown capability → `ValidationResult(valid=False, errors=["unknown capability: {capability_name}"])`.
   - For each field in `input_schema`:
     - If `required=True` and key absent from args → `errors.append(f"field '{name}' is required")`.
     - If `type=string` and value is not `str` → `errors.append(f"field '{name}' must be string")`.
     - If `type=integer` and value is not `int` → `errors.append(f"field '{name}' must be integer")`.
     - If `enum` list defined and value not in list → `errors.append(f"field '{name}' must be one of {enum_values}")`.
   - Return `ValidationResult(valid=len(errors)==0, errors=errors)`.

**Artifact:** `src/capabilities/validator.py`

---

### TASK 6.7 — Safety Tests

**Location:** `tests/test_safety.py`

**Required tests (12):**

1. SAFE mode → all risk levels return `confirm`
2. BALANCED low → `allow`
3. BALANCED medium → `confirm`
4. BALANCED high → `block`
5. BALANCED high + override phrase → `confirm`
6. UNRESTRICTED high → `allow`
7. Path `../etc/shadow` classified as `high`
8. Path `/etc/passwd` classified as `high`
9. `code_exec` with `subprocess` in code → `high`
10. Gate 1 fail (tool mismatch) → `block` with clear reason
11. Gate 3 fail (missing required arg) → `block` with field name in reason
12. Audit log entry created after each permission check

**Artifact:** `tests/test_safety.py`

---

### Definition of Done — Phase 6

Three-gate permission enforced. Sandbox runs with timeout. Schema validation rejects invalid args. Audit log records all actions. All 12 tests pass.

---

## Phase 7 — Memory Engine

```yaml
phase_id: 7
priority: "P1"
total_tasks: 6
blocker: "Phase 6 complete"
```

---

### TASK 7.1 — Memory Database

**Location:** `src/memory/database.py`

**Steps:**

1. Create `src/memory/database.py`.

2. Define `MemoryDB` with thread-local connection pooling:

   ```python
   import threading
   _local = threading.local()
   ```

3. Initialize SQLite at `config.paths.memory_db`. Enable WAL mode: `conn.execute("PRAGMA journal_mode=WAL")`.

4. Schema:

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
       keywords TEXT,
       created_at TEXT,
       expires_at TEXT,
       interaction_count INTEGER DEFAULT 0,
       relevance_score REAL DEFAULT 1.0
   );
   CREATE INDEX IF NOT EXISTS idx_turns_session ON turns(session_id);
   CREATE INDEX IF NOT EXISTS idx_snippets_session ON memory_snippets(session_id);
   ```

5. Implement `store(session_id: str, turn_data: dict) -> None`.
6. Implement `retrieve_recent(session_id: str, limit: int = 5) -> list[dict]` — newest first.
7. Implement `search_snippets(keywords: list[str]) -> list[dict]`.
8. Implement `store_snippet(snippet: dict) -> None`.
9. Handle corrupted DB: on `sqlite3.DatabaseError` at open → rename file to `{name}.corrupted.{timestamp}` → create fresh DB → log WARNING.
10. Implement `get_schema_version() -> int` and `set_schema_version(v: int)` using `PRAGMA user_version`.

**Artifact:** `src/memory/database.py`

---

### TASK 7.2 — Memory Scorer

**Location:** `src/memory/scorer.py`

**Steps:**

1. Create `src/memory/scorer.py`.

2. Define `MemoryScorer`. Implement `score(snippet: dict, query: str) -> float`:

   ```python
   keywords = set(k.strip() for k in snippet.get('keywords', '').lower().split(',') if k.strip())
   query_words = set(w for w in query.lower().split() if len(w) > 2)  # skip stop words
   overlap = len(keywords & query_words) / max(len(query_words), 1)

   created = datetime.fromisoformat(snippet['created_at'])
   age_hours = max(0, (datetime.utcnow() - created).total_seconds() / 3600)
   recency = max(0.0, 1.0 - age_hours / 168.0)  # decay over 7 days

   interactions = min(snippet.get('interaction_count', 0) / 10.0, 1.0)

   return round(0.5 * overlap + 0.3 * recency + 0.2 * interactions, 4)
   ```

**Artifact:** `src/memory/scorer.py`

---

### TASK 7.3 — TTL and Decay Manager

**Location:** `src/memory/ttl.py`

**Steps:**

1. Create `src/memory/ttl.py`. Define `TTLManager` with `MemoryDB` dependency.
2. Constants: `SHORT_TERM_TTL_HOURS = 24`, `LONG_TERM_TTL_DAYS = 30`.
3. `set_ttl(snippet_id, ttl_hours)` → UPDATE `expires_at`.
4. `get_expired_ids()` → SELECT where `expires_at < utcnow()`.
5. `apply_decay(factor=0.95)` → UPDATE `relevance_score *= factor` where age > 24h.
6. `cleanup() -> int` → DELETE expired, return count. Called by background thread every 1 hour.

**Artifact:** `src/memory/ttl.py`

---

### TASK 7.4 — Keyword Indexer

**Location:** `src/memory/indexer.py`

**Steps:**

1. Create `src/memory/indexer.py`. Define `KeywordIndexer`.
2. Table: `keyword_index(keyword TEXT, snippet_id TEXT, PRIMARY KEY(keyword, snippet_id))`.
3. `index(snippet_id, keywords)`, `lookup(keyword) -> list[str]`, `remove(snippet_id)`, `rebuild_index()`.

**Artifact:** `src/memory/indexer.py`

---

### TASK 7.5 — Context Retriever

**Location:** `src/memory/retriever.py`

**Steps:**

1. Create `src/memory/retriever.py`. Define `ContextRetriever`.
2. `get_context(session_id, query, limit=5) -> list[dict]`:
   - Fetch recent turns from DB.
   - Extract query keywords (split, remove words < 3 chars).
   - Look up snippet IDs via `KeywordIndexer`.
   - Score each snippet via `MemoryScorer`.
   - Sort descending, return top `limit`.
   - Update `interaction_count` for returned snippets.
3. Cold start → return `[]`, no error.

**Artifact:** `src/memory/retriever.py`

---

### TASK 7.6 — Memory Tests

**Location:** `tests/test_memory.py`

**Required tests (10):**

1. `store` persists turn; `retrieve_recent` returns it
2. `retrieve_recent` returns newest first
3. Cold start returns empty list
4. `MemoryScorer` scores relevant snippet higher than irrelevant
5. Score always in [0.0, 1.0]
6. `KeywordIndexer.index` → `lookup` returns correct IDs
7. `TTLManager.get_expired_ids` returns expired entries
8. `TTLManager.cleanup` removes expired, returns count
9. `ContextRetriever.get_context` returns sorted results
10. `ContextRetriever` cold start returns empty list

**Artifact:** `tests/test_memory.py`

---

### Definition of Done — Phase 7

Memory stores, retrieves, scores, and expires. ContextRetriever returns relevant snippets. All 10 tests pass.

---

## Phase 8 — Capability System

```yaml
phase_id: 8
priority: "P1"
total_tasks: 6
blocker: "Phase 7 complete"
```

---

### TASK 8.1 — `BaseCapability` Abstract Class

**Location:** `src/capabilities/base.py`

**Purpose:** Defines the capability contract. Every capability must implement all four methods. No exception may propagate from `execute()` to the caller — all errors return `ToolResult.failure(...)`.

**Steps:**

1. Expand/create `src/capabilities/base.py`.

2. Define `BaseCapability(ABC)`:

   ```python
   class BaseCapability(ABC):
       name: str           # Must match capabilities.yaml entry
       domain: str
       description: str

       @abstractmethod
       def execute(self, args: dict) -> ToolResult:
           """Execute the capability. Must never raise — wrap all exceptions in ToolResult.failure()."""
           ...

       @abstractmethod
       def validate(self, args: dict) -> ValidationResult:
           """Validate args before execution. Must be fast and side-effect-free."""
           ...

       @abstractmethod
       def get_risk_level(self, args: dict | None = None) -> RiskLevel:
           """Return risk level. Some capabilities compute it dynamically based on args."""
           ...

       @abstractmethod
       def dry_run(self, args: dict) -> ToolResult:
           """Return what would happen without side effects. Must set ToolResult.dry_run=True."""
           ...

       def to_dict(self) -> dict:
           return {
               "name": self.name,
               "domain": self.domain,
               "description": self.description,
               "risk_level": self.get_risk_level().value,
           }
   ```

3. Note: `execute()` method docstring enforces the no-exception contract. Sandboxing provides a safety net, but capabilities must also internally `try/except` all logic.

**Artifact:** `src/capabilities/base.py`

---

### TASK 8.2 — Capability Registry

**Location:** `src/capabilities/registry.py`

**Steps:**

1. Create `src/capabilities/registry.py`. Define `CapabilityRegistry` as a singleton.

2. `register(capability: BaseCapability) -> None` — reject duplicates with `ValueError`.

3. `get(name: str) -> BaseCapability | None`.

4. `list_all() -> list[str]`.

5. `load_from_manifest(path: str = "config/runtime/capabilities.yaml") -> None`:
   - Parse YAML → for each entry → `importlib.import_module(...)` → instantiate class → `register()`.
   - Log WARNING for failed imports. Do not crash the registry.

**Artifact:** `src/capabilities/registry.py`

---

### TASK 8.3 — Capability Executor

**Location:** `src/capabilities/executor.py`

**Purpose:** Orchestrate all capability execution gates. The ONLY entry point for running a capability.

**Steps:**

1. Expand `src/capabilities/executor.py`.

2. `execute(name: str, args: dict, decision: DecisionOutput, mode: str, dry_run: bool = False) -> ToolResult`:
   - Gate 1: `registry.get(name)` — if None → `ToolResult.failure(name, "capability not found")`.
   - Gate 2: `capability.validate(args)` — if invalid → `ToolResult.failure(name, result.first_error())`.
   - Gate 3: `PermissionLayer().check(name, args, decision, mode)` — if block → `ToolResult.failure(name, f"blocked: {reason}")`.
   - Gate 4: if `confirm`: publish `EVT_WAITING_CONFIRMATION`, wait up to 60s for confirmation signal.
   - Gate 5: if `dry_run=True` → `Sandbox().dry_run(capability, args)`, return.
   - Gate 6: `Sandbox().execute(capability, args, timeout_s=limits.tool_timeout_s)`.
   - Set `tool_result.risk_level = capability.get_risk_level(args).value`.
   - Call `AuditLogger().log_action(...)`.
   - Return result.

**Artifact:** `src/capabilities/executor.py`

---

### TASK 8.4 — Capability Validation Tests

**Location:** `tests/test_capabilities.py`

**Required tests (8):**

1. Concrete subclass missing `execute` → `TypeError` at instantiation
2. Registry `register` + `get` round trip succeeds
3. Registry rejects duplicate name with `ValueError`
4. Registry `get` unknown name → None
5. `CapabilityExecutor` returns failure for unknown capability (gate 1)
6. `CapabilityExecutor` returns failure for invalid args (gate 2)
7. `CapabilityExecutor` returns failure for blocked action in BALANCED mode (gate 3)
8. `CapabilityExecutor` dry_run returns `ToolResult` with `dry_run=True`

**Artifact:** `tests/test_capabilities.py`

---

### TASK 8.5 — Sandbox Tests

**Location:** `tests/test_sandbox.py`

**Required tests (4):**

1. Slow capability exceeds timeout → returns `ToolResult.failure` with "timeout" in error
2. Capability that raises exception → wrapped in `ToolResult.failure`
3. Dry-run calls `dry_run()` not `execute()`
4. `duration_ms` is set and > 0

**Artifact:** `tests/test_sandbox.py`

---

### TASK 8.6 — Observability Tests

**Location:** `tests/test_observability.py`

**Required tests (6):**

1. `MetricsCollector` records latency and appears in summary
2. `MetricsCollector.reset()` clears all state
3. `EventBus` delivers to all subscribers
4. `EventBus` isolates callback exceptions from publisher
5. `EVT_TOOL_EXECUTED` published after successful capability execution
6. `EVT_STATE_TRANSITION` published on each state transition

**Artifact:** `tests/test_observability.py`

---

### Definition of Done — Phase 8

Full capability pipeline operational. All gates enforced. EventBus integrated. All tests pass.

---

## Phase 9 — System Control Capabilities

```yaml
phase_id: 9
priority: "P1"
total_tasks: 8
blocker: "Phase 8 complete"
```

### Objective

Implement all eight system-level capabilities. Each capability is treated as a complete, standalone tool — fully specified with its own contract, platform handling, validation, error handling, dry-run mode, and tests. No shortcutting.

---

### TASK 9.1 — App Launcher Capability (`open_app`)

**Location:** `src/capabilities/system/apps.py`

**Domain:** system | **Risk Level:** medium | **Priority:** standalone tool

#### 9.1.1 — Contract and Interface

- Class: `AppLauncher(BaseCapability)`
- `name = "open_app"`, `domain = "system"`
- Input contract: `{"name": str}` — required, non-empty
- Output: `ToolResult(success=True, data={"pid": int, "name": str, "path": str})` on success
- Error: `ToolResult.failure("open_app", "Application not found: {name}")` on failure
- Dry-run: `ToolResult(success=True, data={"would_launch": name}, dry_run=True)`

#### 9.1.2 — Validation

Implement `validate(args) -> ValidationResult`:

- Check `"name"` key is present and non-empty string.
- Check name is not in `config.safety.blocked_apps` (case-insensitive).
- Return `ValidationResult(valid=True)` if all checks pass.

#### 9.1.3 — Windows Implementation

Search order:

1. `shutil.which(name)` — if found, use PATH directly.
2. `%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\` — scan for `{name}.lnk` (case-insensitive).
3. `C:\\Program Files\\` — scan top-level for `{name}.exe`.
4. `C:\\Program Files (x86)\\` — same.
5. Launch with `subprocess.Popen([executable])`, capture `pid`.

#### 9.1.4 — Linux Implementation

Search order:

1. `shutil.which(name)` — PATH search.
2. `/usr/share/applications/` — scan `*.desktop` files for `Name=` or `Exec=` matching `name` (case-insensitive).
3. Extract `Exec=` value from matching `.desktop` file, strip `%U`, `%F` placeholders.
4. Launch with `subprocess.Popen([executable])`.

#### 9.1.5 — macOS Implementation

Search order:

1. `shutil.which(name)` — PATH search.
2. `/Applications/{name}.app` — case-insensitive glob.
3. `subprocess.run(["open", "-a", name])` as fallback.
4. Parse `open -a` output for PID.

#### 9.1.6 — Error Handling

All platform exceptions (FileNotFoundError, PermissionError, OSError) → caught → `ToolResult.failure("open_app", descriptive_message)`. Never re-raise.

#### 9.1.7 — Update jarvis_slice.py

Replace `open_app(name)` calls with `CapabilityExecutor().execute("open_app", {"name": name}, ...)` in `app/jarvis_slice.py`.

**Artifact:** `src/capabilities/system/apps.py`

---

### TASK 9.2 — System Info Capability (`system_info`)

**Location:** `src/capabilities/system/sysinfo.py`

**Domain:** system | **Risk Level:** low | **Priority:** standalone tool

#### 9.2.1 — Contract and Interface

- Class: `SystemInfoCapability(BaseCapability)`
- `name = "system_info"`, `domain = "system"`
- Input: `{"info_type": "all" | "cpu" | "ram" | "gpu" | "os"}` — optional, default `"all"`
- Output: structured dict with requested section(s)

#### 9.2.2 — Data Collection

- **CPU**: `psutil.cpu_percent(interval=0.5)`, `psutil.cpu_freq().current`, `psutil.cpu_count()`, `platform.processor()`
- **RAM**: `psutil.virtual_memory()` → `total_mb`, `used_mb`, `available_mb`, `percent`
- **GPU**: `VRAMMonitor().get_available_vram_mb()`, `get_total_vram_mb()`. Include GPU name via pynvml if available.
- **OS**: `platform.system()`, `platform.release()`, `platform.version()`, `platform.machine()`
- `info_type="all"` returns all four sections merged into one dict.

#### 9.2.3 — Error Handling

Any `psutil` or platform exception → log warning → include `{"error": str(e)}` in that section. Never fail the whole call.

#### 9.2.4 — Dry Run

Return `ToolResult(success=True, data={"would_collect": info_type}, dry_run=True)`.

**Artifact:** `src/capabilities/system/sysinfo.py`

---

### TASK 9.3 — Clipboard Capability (`clipboard`)

**Location:** `src/capabilities/system/clipboard.py`

**Domain:** system | **Risk Level:** low | **Priority:** standalone tool

#### 9.3.1 — Contract and Interface

- Class: `ClipboardCapability(BaseCapability)`
- `name = "clipboard"`, `domain = "system"`
- Input: `{"action": "read" | "write", "content": str}` — `content` required for write
- Read output: `ToolResult(success=True, data={"content": str})`
- Write output: `ToolResult(success=True, data={"written": True})`

#### 9.3.2 — Validation

- `action` must be `"read"` or `"write"`.
- `action="write"` requires `content` key to be present and non-empty.

#### 9.3.3 — Implementation

- `read`: `pyperclip.paste()` → return content.
- `write`: `pyperclip.copy(args["content"])` → return success.
- On `pyperclip.PyperclipException` → `ToolResult.failure("clipboard", "clipboard not available on this system")`.

#### 9.3.4 — Dry Run

- Read → `ToolResult(success=True, data={"would_read": True}, dry_run=True)`.
- Write → `ToolResult(success=True, data={"would_write": args.get("content", "")[:50]}, dry_run=True)`.

**Artifact:** `src/capabilities/system/clipboard.py`

---

### TASK 9.4 — Notifications Capability (`notify`)

**Location:** `src/capabilities/notify/toasts.py`

**Domain:** notify | **Risk Level:** low | **Priority:** standalone tool

#### 9.4.1 — Contract and Interface

- Class: `NotificationCapability(BaseCapability)`
- `name = "notify"`, `domain = "notify"`
- Input: `{"title": str, "message": str, "duration": int}` — title and message required
- Output: `ToolResult(success=True, data={"sent": True})`

#### 9.4.2 — Implementation

- Primary: `from plyer import notification; notification.notify(title=..., message=..., timeout=duration)`.
- Fallback (plyer unavailable or unsupported platform): `print(f"[NOTIFY] {title}: {message}")` + log to console.
- `duration` defaults to 5 seconds.

#### 9.4.3 — Platform Notes

- Windows: native toast via plyer.
- Linux: `notify-send` via plyer or subprocess fallback.
- macOS: `osascript` via plyer or subprocess fallback.

#### 9.4.4 — Dry Run

Return `ToolResult(success=True, data={"would_notify": {"title": title, "message": message}}, dry_run=True)`.

**Artifact:** `src/capabilities/notify/toasts.py`

---

### TASK 9.5 — Screenshot Capability (`screenshot`)

**Location:** `src/capabilities/screen/capture.py`

**Domain:** screen | **Risk Level:** low | **Priority:** standalone tool

#### 9.5.1 — Contract and Interface

- Class: `ScreenshotCapability(BaseCapability)`
- `name = "screenshot"`, `domain = "screen"`
- Input: `{"ocr": bool, "region": dict}` — both optional
- Output: `ToolResult(success=True, data={"path": str, "ocr_text": str | None})`

#### 9.5.2 — Screen Capture

- Default (whole screen): `from PIL import ImageGrab; img = ImageGrab.grab()`.
- Region specified: `ImageGrab.grab(bbox=(x, y, x+width, y+height))`.
- Multi-monitor alternative: use `mss` library if available.
- Save path: `data/screenshots/{timestamp_uuid}.png`.
- Create `data/screenshots/` if not exists.

#### 9.5.3 — OCR (Optional)

- If `args.get("ocr", False)`:
  - Try `import pytesseract; text = pytesseract.image_to_string(img)`.
  - If pytesseract unavailable → `ocr_text = None`, log WARNING.

#### 9.5.4 — Dry Run

Return `ToolResult(success=True, data={"would_capture": True, "region": args.get("region")}, dry_run=True)`.

#### 9.5.5 — Error Handling

`ImageGrab` not available on headless servers → `ToolResult.failure("screenshot", "screen capture not available (headless environment)")`.

**Artifact:** `src/capabilities/screen/capture.py`

---

### TASK 9.6 — File Operations Capability (`file_ops`)

**Location:** `src/capabilities/files/file_ops.py`

**Domain:** files | **Risk Level:** dynamic (read/list=low, write/move/copy=medium, delete=high) | **Priority:** standalone tool

#### 9.6.1 — Contract and Interface

- Class: `FileOpsCapability(BaseCapability)`
- `name = "file_ops"`, `domain = "files"`
- Actions: `read | write | list | delete | move | copy`
- Input: `{"action": str, "path": str, "content": str?, "destination": str?}`

#### 9.6.2 — Validation (Critical)

Implement `validate(args) -> ValidationResult`:

1. `action` must be in allowed enum.
2. `path` must be provided.
3. `path` must resolve within an `allowed_root`:
   ```python
   resolved = Path(args["path"]).resolve()
   allowed = any(
       os.path.commonpath([resolved, Path(root).expanduser().resolve()]) == str(Path(root).expanduser().resolve())
       for root in config.paths.allowed_roots
   )
   if not allowed:
       errors.append(f"path '{args['path']}' is outside allowed roots")
   ```
4. `write` requires `content`.
5. `move`/`copy` requires `destination`.

#### 9.6.3 — Implementation

- `list`: `[{"name": e.name, "type": "dir" if e.is_dir() else "file", "size_bytes": e.stat().st_size} for e in Path(path).iterdir()]`
- `read`: `Path(path).read_text(encoding="utf-8")`
- `write`: `Path(path).write_text(args["content"], encoding="utf-8")`
- `delete`: `Path(path).unlink()` (files) or `shutil.rmtree(path)` (directories — only after explicit user confirmation)
- `move`: `shutil.move(src, dst)` — validate destination is also within allowed roots
- `copy`: `shutil.copy2(src, dst)` — same destination validation

#### 9.6.4 — Dynamic Risk Level

```python
def get_risk_level(self, args: dict | None = None) -> RiskLevel:
    action = (args or {}).get("action", "read")
    return {"delete": RiskLevel.high, "write": RiskLevel.medium, "move": RiskLevel.medium,
            "copy": RiskLevel.medium, "read": RiskLevel.low, "list": RiskLevel.low}.get(action, RiskLevel.medium)
```

#### 9.6.5 — Dry Run

Return description of what would happen: `{"would_execute": action, "on": path}`.

#### 9.6.6 — Error Handling

`FileNotFoundError`, `PermissionError`, `IsADirectoryError`, `UnicodeDecodeError` → all caught → `ToolResult.failure`.

**Artifact:** `src/capabilities/files/file_ops.py`

---

### TASK 9.7 — Code Executor Capability (`code_exec`)

**Location:** `src/capabilities/coder/executor.py`

**Domain:** coder | **Risk Level:** high | **Priority:** standalone tool

#### 9.7.1 — Contract and Interface

- Class: `CodeExecutorCapability(BaseCapability)`
- `name = "code_exec"`, `domain = "coder"`
- Input: `{"language": "python"|"javascript"|"bash", "code": str, "timeout_s": int}`
- Output: `ToolResult(success=returncode==0, data={"stdout": str, "stderr": str, "returncode": int})`

#### 9.7.2 — Validation (Security-Critical)

Implement `validate(args) -> ValidationResult`:

1. `language` must be in `["python", "javascript", "bash"]`.
2. `code` must be non-empty.
3. Baseline security scan on code string:
   - `__import__('os').system` → reject
   - Raw `import subprocess` → reject
   - `open('/etc` or `open('/proc` → reject
   - `os.system(` → reject
   - Note: This is a baseline check only. Full sandboxing is handled at the OS level.

#### 9.7.3 — Execution

- Create an isolated temporary directory with `tempfile.mkdtemp()` — permissions `0o700`.
- Write code to `{tmpdir}/code.{ext}`.
- Execute:
  - Python: `subprocess.run(["python3", code_file], capture_output=True, timeout=timeout_s, cwd=tmpdir, env={})`
  - JavaScript: `subprocess.run(["node", code_file], capture_output=True, timeout=timeout_s, cwd=tmpdir, env={})`
  - Bash: `subprocess.run(["bash", "-e", code_file], capture_output=True, timeout=timeout_s, cwd=tmpdir, env={})`
- Use `env={}` to prevent inheriting environment variables.
- After execution: `shutil.rmtree(tmpdir)` — always clean up.

#### 9.7.4 — Timeout and Error Handling

- `subprocess.TimeoutExpired` → `ToolResult.failure("code_exec", f"execution timeout after {timeout_s}s")`.
- `FileNotFoundError` (interpreter not found) → `ToolResult.failure("code_exec", f"{language} interpreter not found")`.

#### 9.7.5 — Dry Run

Return `ToolResult(success=True, data={"would_execute": language, "code_length": len(code)}, dry_run=True)`.

**Artifact:** `src/capabilities/coder/executor.py`

---

### TASK 9.8 — Web Search Capability (`web_search`)

**Location:** `src/capabilities/search/web_search.py`

**Domain:** search | **Risk Level:** low | **Priority:** standalone tool

#### 9.8.1 — Contract and Interface

- Class: `WebSearchCapability(BaseCapability)`
- `name = "web_search"`, `domain = "search"`
- Input: `{"query": str, "count": int}` — query required, count defaults to 5
- Output: `ToolResult(success=True, data={"results": [{"title", "url", "snippet"}]})`

#### 9.8.2 — Implementation

- Use DuckDuckGo HTML endpoint: `GET https://html.duckduckgo.com/html/?q={quote(query)}`.
- Set `User-Agent: Mozilla/5.0 (JARVIS/3.0)` header.
- Parse with BeautifulSoup:
  - Titles: `.result__title > a`
  - URLs: `.result__url` or from anchor href
  - Snippets: `.result__snippet`
- Return top `count` results.

#### 9.8.3 — Error Handling

- `requests.ConnectionError` → `ToolResult.failure("web_search", "network unavailable")`.
- `requests.Timeout` → `ToolResult.failure("web_search", "search timed out")`.
- Empty results → `ToolResult(success=True, data={"results": [], "message": "no results found"})`.

#### 9.8.4 — Dry Run

Return `ToolResult(success=True, data={"would_search": query}, dry_run=True)`.

**Artifact:** `src/capabilities/search/web_search.py`

---

### Definition of Done — Phase 9

All 8 capabilities: inherit `BaseCapability`, implement all 4 required methods, return `ToolResult` (never raise), handle all platforms. `app/jarvis_slice.py` updated to new `execute()` interface.

---

## Phase 10 — Prompt Builder

```yaml
phase_id: 10
priority: "P1"
total_tasks: 5
blocker: "Phase 9 complete"
```

---

### TASK 10.1 — Jarvis Identity YAML

**Location:** `config/runtime/jarvis_identity.yaml`

**Steps:**

1. Create `config/runtime/jarvis_identity.yaml`:
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
     - "If uncertain about an action's safety, ask for confirmation"
   local_first: true
   cloud_fallback: false
   ```

**Artifact:** `config/runtime/jarvis_identity.yaml`

---

### TASK 10.2 — Mode Fragments YAML

**Location:** `config/runtime/mode_fragments.yaml`

**Steps:**

1. Create `config/runtime/mode_fragments.yaml` with exactly 5 mode entries:
   ```yaml
   fragments:
     fast:
       system_addition: "Respond concisely. Prioritize speed. No unnecessary explanation."
       output_format: "plain text, 1-3 sentences max"
       behavior: "direct answer, no chain-of-thought"
     normal:
       system_addition: "Balance detail with clarity. Briefly explain your reasoning."
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

**Artifact:** `config/runtime/mode_fragments.yaml`

---

### TASK 10.3 — System Prompt Builder

**Location:** `src/core/context/builder.py`

**Steps:**

1. Create `src/core/context/builder.py`. Define `PromptBuilder`.

2. Load identity and fragments at instantiation (cached as class attributes).

3. Implement `build(decision: DecisionOutput, input_packet: InputPacket) -> str`:
   - Identity block: `f"You are {identity['name']}, {identity['role']}. Constraints: {'; '.join(identity['constraints'])}."`
   - Mode fragment: `fragments[decision.mode.value]['system_addition']`
   - Context block: if `input_packet.memory_snippets` non-empty → `"Relevant context:\n" + formatted snippets`
   - History block: last 3 turns from `input_packet.recent_history` as `"User: ...\nJARVIS: ..."`
   - Language hint: if `input_packet.user_profile.language == "ar"` → append `"Always respond in Arabic."`
   - Return all blocks joined with `"\n\n"`.

**Artifact:** `src/core/context/builder.py`

---

### TASK 10.4 — Wire PromptBuilder into Executor

**Location:** `src/core/runtime/executor.py` (expand TASK 4.5)

**Steps:**

1. Import `PromptBuilder`.
2. Add `self._prompt_builder = PromptBuilder()` in `Executor.__init__`.
3. Replace stub system string with `self._prompt_builder.build(decision, input_packet)`.

---

### TASK 10.5 — Identity Enforcement Tests

**Location:** `tests/test_identity_enforcement.py`

**Required tests (7):**

1. `build()` output contains `"JARVIS"`
2. `fast` mode prompt contains fast fragment text
3. `deep` mode prompt contains deep fragment text
4. `language=ar` → prompt contains "Arabic"
5. Non-empty `memory_snippets` → prompt contains context block
6. Non-empty `recent_history` → prompt contains prior turn
7. All 5 modes produce non-empty distinct prompts

**Artifact:** `tests/test_identity_enforcement.py`

---

### Definition of Done — Phase 10

All LLM calls include JARVIS identity and mode fragment. All 7 tests pass.

---

## Phase 11 — Execution Hardening

```yaml
phase_id: 11
priority: "P0"
total_tasks: 6
blocker: "Phase 10 complete"
```

---

### TASK 11.1 — Timeout Handler

**Location:** `src/core/runtime/timeout.py`

**Steps:**

1. Create `src/core/runtime/timeout.py`. Define `TimeoutHandler(Limits)`.

2. `check(phase: str, start_time: float) -> None`:
   - Map: `{"tool": tool_timeout_s, "step": step_timeout_s, "model": model_timeout_s, "turn": total_turn_timeout_s}`.
   - If `time.time() - start_time >= threshold` → publish `EVT_DEGRADATION` → raise `TurnTimeoutError`.

3. Context manager:
   ```python
   @contextmanager
   def phase_timeout(self, phase: str):
       start = time.time()
       try:
           yield
       finally:
           self.check(phase, start)
   ```

**Artifact:** `src/core/runtime/timeout.py`

---

### TASK 11.2 — Graceful Degradation

**Location:** `src/core/runtime/degradation.py`

**Steps:**

1. Create `src/core/runtime/degradation.py`. Define `DegradationHandler`.

2. `handle_model_failure(model: str, error: Exception) -> str | None`:
   - Log error → publish `EVT_DEGRADATION` → return next fallback model (tier_1 → tier_2 → None).

3. `handle_tool_failure(tool: str, error: Exception) -> None`:
   - Log warning. If `PermissionDeniedError` → publish `EVT_SAFETY_BLOCK`.

4. `generate_error_response(error_type: str, detail: str = "") -> str`:
   - `"model_unavailable"` → user-friendly message.
   - `"timeout"` → suggest simpler request.
   - `"permission_denied"` → explain elevated permission required.
   - `"budget_exhausted"` → retry limit message.

5. Track `_degraded: bool`. `is_degraded() -> bool`.

**Artifact:** `src/core/runtime/degradation.py`

---

### TASK 11.3 — Tiered Fallback System

**Location:** `src/core/runtime/fallback.py`

**Steps:**

1. Create `src/core/runtime/fallback.py`. Define `FallbackSystem`.
2. Load `tier_1` and `tier_2` from `config/runtime/models.yaml`.
3. `attempt(input_packet: InputPacket, tier: int, decision: DecisionOutput) -> FinalResponse`:
   - tier=1: force `decision.model = tier_1`. Call `Executor().execute()`. Return FinalResponse with `degraded=True`.
   - tier=2: force `decision.model = tier_2`. Same.
4. Tier 1 always tried before tier 2.

**Artifact:** `src/core/runtime/fallback.py`

---

### TASK 11.4 — Retry Manager

**Location:** `src/core/runtime/retry.py`

**Steps:**

1. Create `src/core/runtime/retry.py`. Define `RetryManager` (per-turn, not singleton).
2. `_budget: int = config.execution.global_retry_budget` (8 default).
3. `consume(n=1) -> int` — decrement, log remaining, return remaining.
4. `can_retry() -> bool` → `_budget > 0`.
5. `reset() -> None` → restore to initial budget.

**Artifact:** `src/core/runtime/retry.py`

---

### TASK 11.5 — Decision Validation Enforcer

**Location:** `src/core/runtime/validate_decision.py`

**Steps:**

1. Create `src/core/runtime/validate_decision.py`. Define `DecisionEnforcer`.

2. `validate(decision: DecisionOutput) -> bool`:
   - If `decision_source==model` → `score_breakdown` non-empty AND `candidate_list` non-empty.
   - `model` in `ModelAvailability().get_available_models()` → log WARNING if not, return False.
   - `confidence < 0.3` → log WARNING but return True (low confidence is valid data).
   - Return True if structural checks pass.

3. If returns False → caller uses `_safe_default()` immediately. No retry.

**Artifact:** `src/core/runtime/validate_decision.py`

---

### TASK 11.6 — Integration Tests

**Location:** `tests/test_integration.py`

**Required tests (10):**

1. `run_turn("hello", "s1")` → FinalResponse with non-empty text
2. `run_turn("open notepad", "s1")` → fast path, tool_use decision
3. Mock slow model → timeout → degraded FinalResponse (no crash)
4. Mock model failure → fallback chain activates (tier_1 first)
5. Mock all models fail → budget exhausted → error FinalResponse
6. `run_turn("delete /etc/passwd", "s1")` → permission denied ToolResult
7. Two turns → second has `recent_history` from first
8. All state transitions logged to EventBus
9. Mode SAFE → every tool requires confirmation
10. `run_turn` never raises uncaught exception under any failure mode

**Artifact:** `tests/test_integration.py`

---

### Definition of Done — Phase 11

Runtime handles all failure modes. Fallback chain works. Budget enforced. `run_turn` never crashes. All 10 tests pass.

---

## Phase 12 — CLI Interface

```yaml
phase_id: 12
priority: "P2"
total_tasks: 3
blocker: "Phase 11 complete"
```

---

### TASK 12.1 — CLI Chat Loop

**Location:** `src/interfaces/cli/chat.py`

- `CLIChat.start()`: print banner `"JARVIS v3.0 — type /help for commands"`.
- Loop: read input → if `/` command → dispatch to `CommandHandler` → else `run_turn()` → print response.
- Session ID: UUIDv4 generated at start, persisted for session.
- Thinking indicator: `print("Thinking...", end="\r", flush=True)` before `run_turn()`.
- Check `_shutdown` flag from `app/main.py` in loop condition.

**Artifact:** `src/interfaces/cli/chat.py`

---

### TASK 12.2 — CLI Command Handlers

**Location:** `src/interfaces/cli/commands.py`

- Commands: `/help`, `/mode SAFE|BALANCED|UNRESTRICTED`, `/replay [turn_id]`, `/debug`, `/status`, `/quit`.
- All commands case-insensitive. Invalid mode value → print error.

**Artifact:** `src/interfaces/cli/commands.py`

---

### TASK 12.3 — CLI Formatting

**Location:** `src/interfaces/cli/formatting.py`

- `CLIFormatter.format_response(FinalResponse) -> str`: colorama colors, `[DEGRADED]` prefix if degraded.
- `format_tool_result(ToolResult) -> str`: ✓ green / ✗ red.
- Arabic: prepend `\u200f` (RLM mark) to Arabic content.

**Artifact:** `src/interfaces/cli/formatting.py`

---

### Definition of Done — Phase 12

Full CLI chat loop operational. All commands functional. Arabic displays with correct RTL mark.

---

## Phase 13 — Web Automation & Browser

```yaml
phase_id: 13
priority: "P2"
total_tasks: 3
blocker: "Phase 12 complete"
```

**Note:** Directory is `src/capabilities/web/` (not `web_automation/`).

---

### TASK 13.1 — Browser Capability (`browser`)

**Location:** `src/capabilities/web/browser.py`

**Domain:** web | **Risk Level:** medium | **Priority:** standalone tool

#### 13.1.1 — Contract and Interface

- Class: `BrowserCapability(BaseCapability)`
- `name = "browser"`, `domain = "web"`
- Actions: `navigate | click | type | screenshot | extract_text`
- Playwright lifecycle managed per instance. `__del__` closes browser.

#### 13.1.2 — Actions

- `navigate`: `page.goto(url, timeout=30000)` → `{"url": page.url, "title": page.title()}`
- `click`: `page.click(selector)`
- `type`: `page.fill(selector, text)`
- `screenshot`: `page.screenshot(path=save_path)` → `{"path": str(save_path)}`
- `extract_text`: `page.inner_text(selector or "body")` → `{"text": content}`

#### 13.1.3 — Resource Management

- Launch: `self._playwright = sync_playwright().start(); self._browser = self._playwright.chromium.launch(headless=False)`.
- Log memory usage on launch: `psutil.Process().memory_info().rss // (1024*1024)` MB.

#### 13.1.4 — Dry Run

Return `ToolResult(success=True, data={"would_execute": action, "url": args.get("url")}, dry_run=True)`.

**Artifact:** `src/capabilities/web/browser.py`

---

### TASK 13.2 — Web Session Manager

**Location:** `src/capabilities/web/session.py`

- `WebSessionManager`: `create_session(browser) -> BrowserContext` (isolated cookies/storage).
- `close_session(context_id)`, `get_session(context_id)`, `list_sessions()`.
- Session IDs are UUIDs.

**Artifact:** `src/capabilities/web/session.py`

---

### TASK 13.3 — Web Automation Tests

**Location:** `tests/test_web_automation.py`

Tests (mock Playwright or use pytest-playwright):

1. Navigate returns page title
2. Screenshot returns valid file path
3. Extract text returns non-empty string
4. Session create/close lifecycle
5. Timeout → `ToolResult.failure`

**Artifact:** `tests/test_web_automation.py`

---

## Phase 14 — Google APIs

```yaml
phase_id: 14
priority: "P2"
total_tasks: 4
blocker: "Phase 13 complete"
```

---

### TASK 14.1 — Google Auth Service

**Location:** `src/services/google/auth.py`

- `GoogleAuth.authenticate(credentials_path)` — OAuth2 flow, save/load token.
- `get_credentials()` — cached/refreshed.
- Scopes: Calendar, Gmail, Drive.
- Missing credentials → `PermissionDeniedError("Google credentials not configured")`.

**Artifact:** `src/services/google/auth.py`

---

### TASK 14.2 — Google Calendar Service

**Location:** `src/services/google/calendar.py`

- `list_events(start, end)`, `create_event(summary, start, end, description)`, `delete_event(event_id)`.
- All `HttpError` → `JarvisError` with user-friendly message.

**Artifact:** `src/services/google/calendar.py`

---

### TASK 14.3 — Gmail Service

**Location:** `src/services/google/gmail.py`

- `list_messages(query, max_results)`, `get_message(id)`, `send_message(to, subject, body)`.

**Artifact:** `src/services/google/gmail.py`

---

### TASK 14.4 — Google Drive Service

**Location:** `src/services/google/drive.py`

- `list_files(query, max_results)`, `download_file(id, destination)`, `upload_file(name, content, mime_type)`.

**Artifact:** `src/services/google/drive.py`

---

## Phase 14.5 — Telegram Integration

```yaml
phase_id: 14.5
priority: "P2"
total_tasks: 3
blocker: "Phase 14 complete"
```

---

### TASK 14.5.1 — Telegram Bot Service

**Location:** `src/services/telegram/bot.py`

- `TelegramBot` class. Token from `TELEGRAM_BOT_TOKEN` env var.
- `async handle_message(update, context)` → `run_turn()` via `asyncio.to_thread` → reply.
- Missing token → log ERROR, skip start. No crash.
- Ollama unavailable → degraded FinalResponse sent to user.

**Artifact:** `src/services/telegram/bot.py`

---

### TASK 14.5.2 — Telegram Command Handlers

**Location:** `src/services/telegram/commands.py`

- `/start`, `/mode`, `/status`, `/quit` handlers.
- `/mode` validates mode value before calling `update_mode()`.
- `/quit` replies "Goodbye" — bot continues for other users.

**Artifact:** `src/services/telegram/commands.py`

---

### TASK 14.5.3 — Telegram Tests

**Location:** `tests/test_telegram.py`

Tests (mock Application):

1. `handle_message` calls `run_turn` with correct args
2. Response text sent to chat
3. `/mode SAFE` updates mode and replies
4. Missing token → no crash
5. `run_turn` failure → degraded response, not exception

**Artifact:** `tests/test_telegram.py`

---

## Phase 15 — Web UI

```yaml
phase_id: 15
priority: "P2"
total_tasks: 3
blocker: "Phase 14.5 complete"
```

**Note:** Directory is `src/interfaces/web_ui/` (underscore, not space).

---

### TASK 15.1 — Web UI Backend

**Location:** `src/interfaces/web_ui/app.py`

- FastAPI app with: `POST /chat`, `GET /history/{session_id}`, `GET /status`, `POST /mode`, `WebSocket /ws/{session_id}`.
- WebSocket streams `EVT_STATE_TRANSITION` events, sends FinalResponse on complete.
- `WebApp.start(host, port)` → `uvicorn.run(app, ...)`.

**Artifact:** `src/interfaces/web_ui/app.py`

---

### TASK 15.2 — Web UI Frontend

**Location:** `src/interfaces/web_ui/static/index.html`

- Single-file HTML/CSS/JS, no build step, no CDN.
- Chat display, WebSocket client, mode dropdown, status bar, Arabic `dir="auto"` input.

**Artifact:** `src/interfaces/web_ui/static/index.html`

---

### TASK 15.3 — Web UI Tests

**Location:** `tests/test_web_ui.py`

Tests (httpx AsyncClient + ASGITransport):

1. `POST /chat` returns FinalResponse JSON
2. `GET /history/{session_id}` returns list
3. `GET /status` returns model/mode/vram
4. `POST /mode` with SAFE updates mode
5. WebSocket connects and receives state events

**Artifact:** `tests/test_web_ui.py`

---

## Phase 16 — Voice Pipeline

```yaml
phase_id: 16
priority: "P3"
total_tasks: 4
blocker: "Phase 15 complete"
```

---

### TASK 16.1 — STT Capability (`stt`)

**Location:** `src/capabilities/voice/stt.py`

**Domain:** voice | **Risk Level:** low | **Priority:** standalone tool

#### 16.1.1 — Contract

- Input: `{"audio_path": str?}` — optional; if None, record from microphone.
- Output: `ToolResult(success=True, data={"text": str, "language": str})`

#### 16.1.2 — Implementation

- Model: `openai-whisper` `base` (~1GB VRAM). Load lazily on first call.
- If `audio_path` provided: `result = model.transcribe(audio_path)`.
- If None: record 5s from microphone via `speech_recognition.Recognizer`.
- Return `{"text": result["text"], "language": result["language"]}`.

#### 16.1.3 — Error Handling

- Whisper not installed → `ToolResult.failure("stt", "openai-whisper not installed")`.
- Microphone unavailable → `ToolResult.failure("stt", "microphone not available")`.
- Audio file not found → `ToolResult.failure("stt", "audio file not found: {path}")`.

**Artifact:** `src/capabilities/voice/stt.py`

---

### TASK 16.2 — TTS Capability (`tts`)

**Location:** `src/capabilities/voice/tts.py`

**Domain:** voice | **Risk Level:** low | **Priority:** standalone tool

#### 16.2.1 — Contract

- Input: `{"text": str, "voice": str?}` — text required.
- Output: `ToolResult(success=True, data={"audio_path": str})`

#### 16.2.2 — Implementation

- Use Piper TTS (CPU-side): `piper --model {voice} --output_file {output_path}` via subprocess.
- Default voice: `en_US-lessac-medium`. Arabic: `ar_JO-kareem-medium`.
- Output path: `data/audio/{uuid}.wav`.
- Play: `subprocess.Popen(["aplay"|"afplay"|"start", output_path])` (platform-dependent).

#### 16.2.3 — Error Handling

- Piper not installed → `ToolResult.failure("tts", "piper-tts not installed")`.
- Subprocess error → `ToolResult.failure("tts", str(e))`.

**Artifact:** `src/capabilities/voice/tts.py`

---

### TASK 16.3 — Wake Word Detection

**Location:** `src/capabilities/voice/wake_word.py`

- `WakeWordDetector` (not `BaseCapability` — it is a continuous listener, not an action).
- `listen_for_wake_word(wake_word: str, callback: Callable) -> None` — background thread loop.
- `stop() -> None` — set stop flag.
- Integrates with CLI and WebApp for voice-activated mode.

**Artifact:** `src/capabilities/voice/wake_word.py`

---

### TASK 16.4 — Voice Pipeline Tests

**Location:** `tests/test_voice.py`

Tests (mock audio files):

1. STT transcribes WAV to text
2. STT returns language field
3. TTS generates audio file
4. Wake word fires callback on match
5. Wake word does not fire on non-match

**Artifact:** `tests/test_voice.py`

---

## Phase 17 — Vision + Image

```yaml
phase_id: 17
priority: "P3"
total_tasks: 2
blocker: "Phase 16 complete"
```

---

### TASK 17.1 — Vision Capability (`vision_analyze`)

**Location:** `src/capabilities/vision/vision.py`

**Domain:** vision | **Risk Level:** low | **Priority:** standalone tool

#### 17.1.1 — Contract

- Input: `{"image_path": str, "prompt": str?}`
- Output: `ToolResult(success=True, data={"description": str})`

#### 17.1.2 — Implementation

- Model: `llava:7b` (4500MB VRAM). Check `VRAMMonitor().is_model_loadable(4500)` before calling.
- Encode image: `base64.b64encode(Path(image_path).read_bytes()).decode()`.
- POST to Ollama: `{"model": "llava:7b", "messages": [{"role": "user", "content": prompt, "images": [b64]}]}`.
- VRAM insufficient → `ToolResult.failure("vision_analyze", "VRAM insufficient for llava:7b (requires 4500MB)")`.

**Artifact:** `src/capabilities/vision/vision.py`

---

### TASK 17.2 — Image Generation Capability (`image_gen`)

**Location:** `src/capabilities/vision/image_gen.py`

**Domain:** vision | **Risk Level:** low | **Priority:** standalone tool

#### 17.2.1 — Contract

- Input: `{"prompt": str, "size": "512x512"|"768x768"|"1024x1024"}`
- Output: `ToolResult(success=True, data={"image_path": str})`

#### 17.2.2 — Implementation

- Use `diffusers` + `StableDiffusionPipeline` with `runwayml/stable-diffusion-v1-5`.
- VRAM sufficient (>2GB): `torch_dtype=torch.float16`. Else: CPU float32 fallback.
- Save to `data/images/{uuid}.png`.

**Artifact:** `src/capabilities/vision/image_gen.py`

---

## Phase 18 — QA + Production

```yaml
phase_id: 18
priority: "P0"
total_tasks: 6
blocker: "Phase 17 complete"
```

---

### TASK 18.1 — Performance Tests

**Location:** `tests/test_performance.py`

Tests:

1. Fast path latency < 100ms for `"open notepad"`
2. `run_turn("what is 2+2", "s1")` completes < 5000ms
3. After `gemma3:4b` loaded → `VRAMMonitor().get_available_vram_mb() >= 512`
4. MetricsCollector p95 < 5000ms for decision phase after 10 turns
5. 3 concurrent `POST /chat` requests all return within 30s

**Artifact:** `tests/test_performance.py`

---

### TASK 18.2 — Arabic Language Tests

**Location:** `tests/test_arabic.py`

Tests:

1. `"افتح المفكرة"` → `tool_use, open_app`
2. `"ابحث عن الذكاء الاصطناعي"` → `search`
3. Arabic input no encoding error
4. `language=ar` → prompt contains "Arabic"
5. Arabic text in InputPacket passes validation
6. CLI formatter: Arabic preceded by RLM mark
7. STT: Arabic audio → Arabic text

**Artifact:** `tests/test_arabic.py`

---

### TASK 18.3 — Production Configuration

**Location:** `config/runtime/production.yaml`

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

`load_config("config/runtime/production.yaml")` deep-merges over `settings.yaml` defaults.

**Artifact:** `config/runtime/production.yaml`

---

### TASK 18.4 — Full Test Suite Run

```bash
pytest tests/ -v --tb=short
pytest tests/ --cov=src --cov-report=term-missing
# TOTAL must show > 80%
grep -r "open_app(" src/ app/ --include="*.py"
# Must only appear in apps.py definition
```

---

### TASK 18.5 — Version and Release

**Location:** `VERSION`, `RELEASE_NOTES.md`

- `VERSION` contains `3.0.0`.
- `RELEASE_NOTES.md`: full feature list, breaking changes, hardware requirements, startup instructions, known limitations.
- Remove all `print()` debug statements from non-CLI code.
- No hardcoded paths anywhere.

**Artifacts:** `VERSION`, `RELEASE_NOTES.md`

---

### TASK 18.6 — Determinism Verification

**Location:** `tests/test_determinism.py`

Tests:

1. Same input → same fast-path decision
2. Same VRAM + same input → same model ranking
3. Same state → same transitions (static dict)
4. `ModelScorer.rank_models()` same result across 10 calls
5. `RetryManager.consume()` decrements predictably
6. `check_limit()` produces identical results for identical inputs

**Artifact:** `tests/test_determinism.py`

---

### Definition of Done — Phase 18

All tests pass. Coverage > 80%. Performance targets met. Arabic verified. Determinism verified. Release artifacts created.

---

## Summary

| Metric         | Count                                        |
| -------------- | -------------------------------------------- |
| Total phases   | 20 (0–18 + 14.5)                             |
| Total tasks    | ~135                                         |
| Test files     | 15                                           |
| Config files   | 8                                            |
| Source modules | ~65                                          |
| Capabilities   | 13 (8 core + 2 voice + 2 vision + 1 browser) |

---

### Final Validation Checklist

- [ ] No `utils`, `misc`, `helpers`, `brain`, `common` folders anywhere
- [ ] No spaces in directory names (`web_ui` not `web ui`)
- [ ] `capabilities/web/` used (not `web_automation/`)
- [ ] `src/core/sandbox/` and `src/core/safety/` exist
- [ ] `src/core/observability/` exists
- [ ] All config in `config/runtime/` and `config/env/`
- [ ] EventBus defined in Phase 1 before first reference in Phase 4
- [ ] All exceptions in `src/core/exceptions.py`
- [ ] `SchemaValidator` stub exists before Phase 6 (created in Phase 2)
- [ ] Factor names in scorer exactly match `config/runtime/models.yaml` weight keys
- [ ] `AppLauncher.execute()` used everywhere after Phase 9
- [ ] `config/runtime/settings.yaml` exists (not just `.example`)
- [ ] Safety YAML has both `blocked_apps` and `blocked_commands` (not nested under execution)
- [ ] `check_limit` semantics: current < max → True, current >= max → False
- [ ] All capabilities implement all 4 `BaseCapability` abstract methods
- [ ] All capabilities return `ToolResult` — never raise to caller
- [ ] Config precedence: CLI > ENV > .env > YAML enforced
- [ ] `src/__version__ == "3.0.0"`
- [ ] `pytest tests/ -v` passes all tests
- [ ] `pytest tests/ --cov=src` shows > 80% coverage
- [ ] All three spec files share `spec_version: v3.0`

---

**JARVIS v3.0 — Execution Plan v3.0**
_Last updated: 2026-05-02 | Contract-first. Capabilities sovereign. No drift._
