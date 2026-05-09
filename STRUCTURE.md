# 🏗️ JARVIS v3.2 — Architecture Specification

> **spec_version:** `v3.2` | **project_version:** `3.2.0` | **structure_version:** `3.2`
> **last_updated:** `2026-05-03`

---

## 📑 Table of Contents

1. [System Principles](#1-system-principles)
2. [Root Structure](#2-root-structure)
3. [Layer Definitions](#3-layer-definitions)
4. [Naming Rules](#4-naming-rules)
5. [Capability System Rules](#5-capability-system-rules)
6. [Execution Flow Mapping](#6-execution-flow-mapping)
7. [Forbidden Patterns](#7-forbidden-patterns)
8. [State Machine Enforcement](#8-state-machine-enforcement)
9. [Migration Rules](#9-migration-rules)
10. [Validation Checklist](#10-validation-checklist)
11. [Spec Alignment and Phase Status](#11-spec-alignment-and-phase-status)

---

## 1. SYSTEM PRINCIPLES

|  #  | Principle                                   | Description                                                                                                                                                                              |
| :-: | :------------------------------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|  1  | **State Machine is Single Decision Authority** | ALL decisions originate from StateMachine. No component may self-decide — including SLA, scheduler, sandbox, or execution engine. ALL actions route via `StateManager.transition_to()`. |
|  2  | **ExecutionEngine is Executor ONLY**        | ExecutionEngine accepts tasks ONLY from StateMachine, executes ONLY, returns structured results. MUST NOT: decide, route, retry, or change execution mode.                                |
|  3  | **Scheduler is Placement ONLY**             | Scheduler handles task placement, queue insertion, and pre-computed dependency resolution ONLY. Priority is computed in DECIDING state — scheduler makes NO priority decisions.          |
|  4  | **SLAEnforcer is Passive Observer**         | SLAEnforcer emits events ONLY. It CANNOT cancel tasks, trigger retries, or select fallbacks. StateMachine receives SLAEvent and decides the action (cancel/fallback/retry/ignore).      |
|  5  | **Determinism Contract**                    | Two modes: `deterministic` (strict ordering, no parallelism, fixed retry) and `performance` (relaxed ordering, bounded parallelism, adaptive retry). StateMachine enforces mode rules.  |
|  6  | **No Bypass Rule**                          | No layer may call capabilities, models, or execution_engine directly. ALL calls go through `StateManager.transition_to()`.                                                               |
|  7  | **Dual-Mode Cancellation**                  | Soft cancel (SIGTERM, 2s grace) → hard kill (SIGKILL). ExecutionEngine MUST confirm termination_status. Process tree killed. Cleanup always follows.                                     |
|  8  | **Capability Boundary Enforcement**         | Runtime validates capability.scope BEFORE execution. Violations → block + emit CapabilityViolationEvent. Each capability defines: allowed_ops, forbidden_ops, resource_limits.            |
|  9  | **Concurrency Mode-Bound**                  | Parallelism allowed ONLY in performance mode AND when no shared_resource_conflict. Blocked in deterministic mode OR when shared_lock_required. Lock ordering enforced globally.          |
| 10  | **Observability-First Design**              | Every state transition, tool call, model swap, and failure MUST be logged with structured data.                                                                                          |
| 11  | **Fail-Safe Defaults**                      | The system degrades gracefully. Never crashes. Never executes irreversible actions without explicit approval.                                                                            |
| 12  | **Capabilities are Sovereign**              | Capabilities are the ONLY layer that may execute side-effects. Each capability is a complete, standalone tool with its own validation, error handling, dry-run, and risk classification. |
| 13  | **CapabilityRuntime is Internal**           | CapabilityRuntime CANNOT be imported by interfaces, decision, or services. The ONLY call path is: StateManager.transition_to(EXECUTING) → run_turn() → ExecutionEngine → CapabilityRuntime → CapabilityExecutor → Capability. |
| 14  | **Single Responsibility per Layer**         | Each layer has exactly one defined responsibility. No cross-layer duplication.                                                                                                           |
| 15  | **No Vague Folders**                        | No folders named `utils`, `misc`, `helpers`, `brain`, or `common`. Every folder name describes its specific responsibility.                                                              |
| 16  | **Contract-First Design**                   | All data contracts (`InputPacket`, `DecisionOutput`, `ToolResult`, `FinalResponse`) are defined and validated before any logic uses them.                                                |
| 17  | **Config Precedence**                       | CLI args > shell ENV > `.env` file > YAML defaults. No exceptions.                                                                                                                       |
| 18  | **Security by Structure**                   | Safety is enforced by the Safety layer, not by prompting the model. Path validation uses `Path.resolve()` + `os.path.commonpath()`.                                                      |

---

## 2. ROOT STRUCTURE

```
jarvis/
│
├── VERSION                          ← Single-line version string: "3.2.0"
│
├── app/
│   ├── __init__.py
│   ├── main.py                      ← Canonical entry point, boot sequence, argparse, signal handling
│   └── jarvis_slice.py              ← Phase 0 vertical slice demo (migrated to full executor in Phase 9)
│
├── config/
│   ├── build/                       ← Build scripts, CI config (future)
│   ├── env/
│   │   ├── .env                     ← GITIGNORED. Live secrets. Copy from .env.example
│   │   └── .env.example             ← Committed template. All secret keys with placeholder values
│   └── runtime/
│       ├── capabilities.yaml        ← Registry manifest: 13 capability entries with full schema
│       ├── jarvis_identity.yaml     ← JARVIS persona, constraints, tone, language config
│       ├── mode_fragments.yaml      ← Per-mode system prompt fragments (fast/normal/deep/planning/research)
│       ├── models.yaml              ← Scoring weights (must sum 1.0), fallback chain tiers
│       ├── production.yaml          ← Production overrides: lower log level, tighter timeouts
│       ├── settings.example.yaml    ← Committed template for user configuration
│       └── settings.yaml            ← GITIGNORED. Live runtime configuration
│
├── data/
│   ├── audio/                       ← TTS output audio files (WAV format, UUID-named)
│   ├── images/                      ← Image generation output (PNG, UUID-named)
│   ├── memory.db                    ← SQLite: turn history, memory snippets (WAL mode)
│   ├── audit.db                     ← SQLite: capability execution audit log (WAL mode)
│   ├── metrics.db                   ← SQLite: real-time system metrics time-series (WAL mode)
│   ├── profiles/                    ← Per-user JSON profiles ({user_id}.json)
│   └── screenshots/                 ← Screen captures (PNG, timestamp-UUID named)
│
├── docs/
│   ├── README.md                    ← User-facing documentation (capabilities, usage, hardware)
│   ├── RELEASE_NOTES.md             ← Feature list, breaking changes, known limitations per version
│   ├── STRUCTURE.md                 ← THIS FILE. Architecture authority.
│   └── TASKS.md                     ← Execution plan authority. All pending work.
│
├── logs/                            ← Structured JSON log files (auto-rotated, gitignored)
│
├── meta/
│   ├── .editorconfig
│   ├── .gitignore                   ← Includes: settings.yaml, .env, logs/, data/*.db, __pycache__ (data/*.db covers memory.db, audit.db, metrics.db)
│   ├── LICENSE
│   ├── pyproject.toml               ← Package definition, dependencies, pytest config
│   ├── requirements.txt             ← Comment header: "pip install -e ."
│   └── .gitkeep
│
├── scripts/
│   └── setup.sh                     ← First-run: venv creation, pip install, Ollama model pulls
│
├── tests/
│   ├── conftest.py                  ← Shared fixtures: default_profile, default_packet, mock_ollama, etc.
│   ├── test_arabic.py               ← Bilingual input/output validation (EN + AR)
│   ├── test_capabilities.py         ← BaseCapability contract, Registry, CapabilityExecutor gates
│   ├── test_contracts.py            ← All Pydantic contract models: valid/invalid instantiation
│   ├── test_decision.py             ← FastPath rules, Classifier, ModelScorer, RiskAssessor, decide()
│   ├── test_determinism.py          ← Identical inputs → identical outputs across all layers
│   ├── test_identity_enforcement.py ← PromptBuilder output contains correct identity + mode fragments
│   ├── test_integration.py          ← End-to-end run_turn() scenarios under all failure modes
│   ├── test_memory.py               ← MemoryDB store/retrieve, Scorer, TTL, Indexer, Retriever
│   ├── test_observability.py        ← MetricsCollector, EventBus, EVT_* event delivery
│   ├── test_performance.py          ← Latency targets: fast-path <100ms, simple query <5s
│   ├── test_safety.py               ← SafetyClassifier, ModeEnforcer, PermissionLayer three gates
│   ├── test_sandbox.py              ← Timeout wrapping, exception catching, dry-run isolation
│   ├── test_state_machine.py        ← All valid/invalid transitions, StateManager, Limits.check_limit()
│   ├── test_telegram.py             ← Bot message handling, command handlers, missing token
│   ├── test_voice.py                ← STT transcription, TTS generation, wake word detection
│   ├── test_web_automation.py       ← BrowserCapability actions, session manager, Playwright timeouts
│   └── test_web_ui.py               ← FastAPI endpoints, WebSocket state streaming
│
└── src/
    ├── __init__.py                  ← ONLY __init__.py at this level. Sets __version__ = "3.2.0"
    │
    ├── capabilities/                ← SOVEREIGN LAYER: all side-effectful actions live here exclusively
    │   ├── base.py                  ← BaseCapability ABC: execute, validate, get_risk_level, dry_run
    │   ├── executor.py              ← CapabilityExecutor: 6-gate pipeline (registry→validate→permission→confirm→dryrun→sandbox)
    │   ├── registry.py              ← CapabilityRegistry singleton: register, get, load_from_manifest
    │   ├── result.py                ← ToolResult Pydantic model + failure/success_result factories
    │   ├── validator.py             ← ValidationResult dataclass + SchemaValidator (YAML-driven)
    │   ├── runtime/                  ← CAPABILITY RUNTIME: INTERNAL ONLY — cannot be imported by interfaces/decision/services
    │   │   ├── capability_runtime.py ← CapabilityRuntime: execute_async(), execute_batch(), stream_results(), cancel()
    │   │   ├── progress.py          ← ProgressTracker: percentage, ETA, status updates via EventBus
    │   │   ├── stream.py            ← StreamBuffer: chunked output for long-running capabilities
    │   │   └── cancellation.py      ← CancellationToken: cooperative asyncio cancellation (event flag + callbacks). Used by capabilities to check for user-initiated cancellation mid-execution.
    │   ├── api/                     ← Reserved: future external API capability modules
    │   ├── coder/
    │   │   └── executor.py          ← CodeExecutorCapability: python/js/bash in isolated subprocess
    │   ├── files/
    │   │   └── file_ops.py          ← FileSystemEngine: batch operations (ONLY where needed), indexing, search
    │   ├── notify/
    │   │   └── toasts.py            ← EventNotificationSystem: queue, priority, grouping, cross-platform
    │   ├── screen/
    │   │   └── capture.py           ← VisionPipeline: region capture, multi-monitor, OCR, image analysis hooks
    │   ├── search/
    │   │   └── web_search.py        ← DataExtractionEngine: multi-engine fallback, parsing, structured data, caching
    │   ├── system/
    │   │   ├── apps.py              ← SystemProcessManager: open/close/restart, detect running, batch launch, monitoring
    │   │   ├── clipboard.py         ← SmartDataChannel: history tracking, multi-format, sync pipeline, transformations
    │   │   └── sysinfo.py           ← RealTimeSystemMonitor: live streaming stats, threshold alerts, historical tracking
    │   ├── vision/
    │   │   ├── image_gen.py         ← ImageGenCapability: Stable Diffusion via diffusers
    │   │   └── vision.py            ← VisionCapability: llava:7b image analysis via Ollama
    │   ├── voice/
    │   │   ├── stt.py               ← STTCapability: openai-whisper transcription
    │   │   ├── tts.py               ← TTSCapability: piper-tts speech synthesis
    │   │   └── wake_word.py         ← WakeWordDetector: continuous background listener (not BaseCapability)
    │   └── web/
    │       ├── browser.py           ← BrowserCapability: Playwright navigate/click/type/screenshot/extract
    │       └── session.py           ← WebSessionManager: isolated browser contexts (UUID-keyed)
    │
    ├── core/                        ← ORCHESTRATION LAYER: controls WHEN and HOW layers execute
    │   ├── config.py                ← load_config() with Pydantic validation + 4-level precedence + execution_mode
    │   ├── exceptions.py            ← JarvisError hierarchy: Runtime, Models, Capabilities, Safety, Decision
    │   ├── logging_setup.py         ← setup_logging() + log_event() structured logging via loguru
    │   ├── context/
    │   │   ├── assembler.py         ← ContextAssembler: builds InputPacket from raw user input + profile + memory
    │   │   ├── builder.py           ← PromptBuilder: assembles system prompt from identity + mode + context
    │   │   └── bundle.py            ← InputPacket Pydantic model (canonical runtime input container)
    │   ├── decision/
    │   │   ├── classifier.py        ← LLM-based intent classifier with JSON extraction + repair
    │   │   ├── decision.py          ← decide(): FastPath → Classifier → Scorer → RiskAssessor pipeline
    │   │   ├── fast_path.py         ← FastPath: compiled regex rules for zero-latency decisions (EN + AR)
    │   │   ├── model_score.py       ← ModelScore Pydantic model with 5 required factor keys
    │   │   ├── output.py            ← DecisionOutput + all enums: Intent, Complexity, ExecutionMode, RiskLevel, DecisionSource
    │   │   ├── risk.py              ← RiskAssessor: tool-level and arg-level risk classification
    │   │   └── scorer.py            ← ModelScorer: weighted multi-factor scoring + deterministic ranking
    │   ├── execution_engine/        ← EXECUTOR ONLY: accepts tasks from StateMachine, executes, confirms termination
    │   │   ├── scheduler.py        ← TaskScheduler: task placement + queue insertion + pre-computed dependency resolution ONLY
    │   │   ├── async_executor.py   ← AsyncExecutor: non-blocking capability execution with Future pattern
    │   │   ├── batch_processor.py  ← BatchProcessor: multi-item capability execution (ONLY where needed)
    │   │   ├── cancellation.py     ← ProcessCancellationController: OS-level dual-mode cancel (SIGTERM 2s grace → SIGKILL → confirm). Used by ExecutionEngine for subprocess management ONLY.
    │   │   └── concurrency.py      ← ConcurrencyController: mode-bound parallelism + deadlock/starvation/priority inversion safeguards
    │   ├── observability/
    │   │   ├── event_bus.py         ← EventBus singleton: pub/sub, EventEnvelope, EVT_* constants, subscriber isolation
    │   │   ├── metrics.py           ← MetricsCollector singleton: latency percentiles, errors, model usage
    │   │   ├── tracing.py          ← TracingSystem: trace_id + span_id propagation, span lifecycle
    │   │   └── alerting.py         ← AlertManager: passive alert rules, EVT_THRESHOLD_ALERT emission, cooldown
    │   ├── performance/            ← PASSIVE MONITORING: SLA events, rule-based profiling, bounded cache
    │   │   ├── profiler.py         ← ExecutionProfiler: per-capability latency/cpu/memory metrics, violation_count tracking
    │   │   ├── sla_enforcer.py     ← SLAEnforcer: PASSIVE — emits SLAEvent ONLY. NEVER cancels/retries. StateMachine decides.
    │   │   ├── benchmark.py        ← BenchmarkRunner: automated performance regression testing
    │   │   └── cache.py            ← SmartCache: TTL + LRU eviction, dynamic TTL for hot paths
    │   ├── runtime/
    │   │   ├── capability_validator.py ← RuntimeValidator: validates capability.scope BEFORE execution. Blocks + emits event on violation.
    │   │   ├── degradation.py       ← DegradationHandler: model/tool failure → user-friendly fallback
    │   │   ├── escalation.py        ← EscalationChain: tiered retry with weight adjustment + forced fallback
    │   │   ├── evaluation_result.py ← EvaluationResult Pydantic model
    │   │   ├── evaluator.py         ← Evaluator: heuristic quality scoring (completeness + relevance + coherence)
    │   │   ├── executor.py          ← Executor: LLM call layer → LLMOutput (does NOT handle retries)
    │   │   ├── fallback.py          ← FallbackSystem: tier-1 then tier-2 model substitution
    │   │   ├── final_response.py    ← FinalResponse Pydantic model + error_response() factory
    │   │   ├── limits.py            ← Limits: all numeric execution ceilings loaded from config
    │   │   ├── llm_output.py        ← LLMOutput Pydantic model (answer | tool_call)
    │   │   ├── loop.py              ← run_turn(): state machine orchestration loop with streaming (ONLY for heavy tasks)
    │   │   ├── retry.py             ← RetryManager: centralized global budget + exponential backoff (StateMachine-controlled)
    │   │   ├── state.py             ← RuntimeState enum + ALLOWED_TRANSITIONS map + execution_mode bindings
    │   │   ├── state_manager.py     ← StateManager: transition_to(), force_state(), history, retry authority, SLA handler, mode enforcer
    │   │   ├── timeout.py           ← TimeoutHandler + phase_timeout() context manager + SLA enforcement
    │   │   └── validate_decision.py ← DecisionEnforcer: structural validation of DecisionOutput
    │   ├── safety/
    │   │   ├── audit.py             ← AuditLogger: SQLite log of every capability execution attempt
    │   │   ├── classifier.py        ← SafetyClassifier: path traversal, blocked path, code pattern checks
    │   │   ├── mode_enforcer.py     ← ModeEnforcer: SAFE/BALANCED/UNRESTRICTED permission matrix
    │   │   └── permission.py        ← PermissionLayer: Gate1(consistency) + Gate2(safety) + Gate3(schema)
    │   └── sandbox/                ← HARDENED ISOLATION: process isolation, privilege drop, filesystem sandbox, network policy
    │       ├── sandbox.py           ← Sandbox: ThreadPoolExecutor isolation + timeout + exception wrapping
    │       ├── resource_monitor.py  ← ResourceMonitor: CPU/RAM tracking per execution
    │       ├── process_pool.py      ← ProcessPool: isolated subprocess + privilege drop + syscall restrictions + tree kill (soft→hard)
    │       └── filesystem.py        ← FilesystemRestrictor: allowlist paths + chroot-like restrictions
    │
     ├── interfaces/                  ← THIN DISPLAY LAYER: converts user I/O to/from runtime requests
     │   ├── cli/
     │   │   ├── chat.py              ← CLIChat: main REPL loop with thinking indicator and session management
     │   │   ├── commands.py          ← CommandHandler: /help /mode /replay /debug /status /quit
     │   │   └── formatting.py        ← CLIFormatter: colorama output, [DEGRADED] prefix, RTL Arabic mark
     │   ├── gui/                     ← Reserved: future desktop GUI (Tkinter/PyQt)
     │   ├── telegram/                ← MOVED from services/ (thin I/O interface, not a data service)
     │   │   ├── bot.py               ← TelegramBot: async message handler → run_turn via injected callable
     │   │   └── commands.py          ← Telegram command handlers: /start /mode /status /quit
     │   └── web_ui/
     │       ├── app.py               ← FastAPI app: POST /chat, GET /history, WebSocket /ws/{session_id}
     │       └── static/
     │           └── index.html       ← Single-file SPA: WebSocket client, mode dropdown, dir="auto" input
     │
    ├── memory/                      ← MEMORY ENGINE: retrieval, scoring, decay — not just storage
    │   ├── database.py              ← MemoryDB: SQLite WAL, turns table, snippets table, thread-local pool
    │   ├── indexer.py               ← KeywordIndexer: keyword → snippet_id inverted index
    │   ├── retriever.py             ← ContextRetriever: keyword lookup → score → sort → return top-N
    │   ├── scorer.py                ← MemoryScorer: overlap + recency + interaction weighted scoring
    │   ├── ttl.py                   ← TTLManager: expires_at enforcement, relevance decay, hourly cleanup
    │   └── user_profile.py          ← UserProfile dataclass: load/save/update_mode with JSON persistence
    │
    ├── models/                      ← MODEL ADAPTERS: lifecycle management and hardware awareness
    │   ├── availability.py          ← ModelAvailability: Ollama /api/tags + VRAM filter (30s cache)
    │   ├── manager.py               ← ModelManager singleton: load/unload/swap with threading.Lock
    │   ├── profiles.py              ← PROFILES dict: frozen ModelProfile dataclasses (VRAM, caps, tiers)
    │   ├── vram_monitor.py          ← VRAMMonitor: pynvml with heuristic fallback, 5s cache
    │   ├── llm/
    │   │   └── engine.py            ← OllamaEngine: chat_with_model() with timeout, metrics, deprecation shim
    │   ├── speech/                  ← Reserved: Whisper and Piper adapter wrappers (future)
    │   └── vision/                  ← Reserved: LLaVA and Stable Diffusion adapter wrappers (future)
    │
    └── services/                    ← PASSIVE DATA CONNECTORS: provide data, never execute actions
        ├── google/
        │   ├── auth.py              ← GoogleAuth: OAuth2 flow, token persistence, scope management
        │   ├── calendar.py          ← GoogleCalendar: list/create/delete events via Calendar API
        │   ├── drive.py             ← GoogleDrive: list/download/upload files via Drive API
        │   └── gmail.py             ← Gmail: list/get/send messages via Gmail API
        └── integrations/            ← Reserved: future third-party service connectors
```

---

## 3. LAYER DEFINITIONS

### `core/` — Orchestration Layer

**Purpose:** Controls WHEN and HOW all other layers execute. The runtime state machine lives here. No business logic, no tool implementations, no external API clients.

| Owns                                                                                   | Must NOT Contain                                                |
| :------------------------------------------------------------------------------------- | :-------------------------------------------------------------- |
| Runtime state machine (`loop.py`, `state.py`, `state_manager.py`)                      | Tool implementations                                            |
| Decision pipeline (`decision.py`, `classifier.py`, `fast_path.py`, `scorer.py`)        | External API clients                                            |
| Context assembly (`assembler.py`, `builder.py`, `bundle.py`)                           | UI / display logic                                              |
| Safety enforcement (`classifier.py`, `mode_enforcer.py`, `permission.py`)              | Model loading/unloading                                         |
| Hardened Sandbox (`sandbox.py`, `process_pool.py`, `resource_monitor.py`, `filesystem.py`) | Direct capability invocation (must go via `CapabilityExecutor`) |
| Observability (`event_bus.py`, `metrics.py`, `tracing.py`, `alerting.py`)   | Domain-specific business logic                                  |
| Hardening (`timeout.py`, `degradation.py`, `fallback.py`, `retry.py`, `escalation.py`) |                                                                 |
| ExecutionEngine (`execution_engine/`) — executor ONLY, no decisions                    | Independent retry logic, dynamic routing                        |
| Performance (`performance/`) — SLA enforcer, rule-based optimization                   | Adaptive optimizer (auto-switching)                             |

---

### `capabilities/` — Sovereign Action Layer

**Purpose:** The ONLY layer permitted to perform side-effects on the real world (filesystem, processes, network, display). Every capability is a self-contained, testable tool.

**Sovereignty Rules:**

- Each capability owns its full input contract (schema, required fields, enum values).
- Each capability owns its own risk classification logic.
- Each capability implements `dry_run()` without side effects.
- Each capability returns `ToolResult` — **never raises** exceptions to the caller.
- Each capability validates args **before** executing — `validate()` is synchronous and fast.
- Each capability handles all platform variations internally.
- Capabilities **never** call LLMs, access memory, or invoke other capabilities.
- Each capability defines scope: `allowed_operations`, `forbidden_operations`, `resource_limits`.
- `CapabilityRuntime` is INTERNAL — cannot be imported by interfaces, decision, or services.

| Owns                                                     | Must NOT Contain       |
| :------------------------------------------------------- | :--------------------- |
| System control (`apps.py`, `sysinfo.py`, `clipboard.py`) | Decision logic         |
| File operations (`file_ops.py`)                          | Model selection        |
| Web automation (`browser.py`, `session.py`)              | LLM calls              |
| Screen capture, OCR (`capture.py`)                       | Memory access          |
| Code execution (`coder/executor.py`)                     | Routing logic          |
| Web search (`web_search.py`)                             | Cross-capability calls |
| Notifications (`toasts.py`)                              | State machine access   |
| Voice I/O (`stt.py`, `tts.py`, `wake_word.py`)           |                        |
| Vision (`vision.py`, `image_gen.py`)                     |                        |

---

### `interfaces/` — Display Layer

**Purpose:** Thin boundary between the user and the runtime. Converts raw user input into `run_turn()` calls and displays `FinalResponse`. Contains **zero** business logic.

| Owns                                  | Must NOT Contain      |
| :------------------------------------ | :-------------------- |
| CLI chat loop (`chat.py`)             | Business logic        |
| CLI commands (`commands.py`)          | Tool execution        |
| CLI formatting (`formatting.py`)      | Decision making       |
| Web UI FastAPI backend (`app.py`)     | State management      |
| Web UI frontend (`static/index.html`) | Memory access         |
| Signal handling and graceful shutdown | Capability invocation |

---

### `services/` — Passive Connector Layer

**Purpose:** External system connectors. Services provide **data** — they never execute actions. Capabilities that need external data call services; capabilities never call external APIs directly.

| Owns                                 | Must NOT Contain         |
| :----------------------------------- | :----------------------- |
| Google APIs (Calendar, Gmail, Drive) | Decision making          |
| OAuth token management               | Tool execution           |
| Third-party service clients          | State management         |

---

### `models/` — Model Adapter Layer

**Purpose:** Model lifecycle management (load, unload, swap) and hardware-aware selection. Does **not** decide which model to use — that is `core/decision/scorer.py`.

| Owns                                                       | Must NOT Contain                       |
| :--------------------------------------------------------- | :------------------------------------- |
| `ModelManager` singleton (VRAM monitoring, threading.Lock) | Routing logic                          |
| `OllamaEngine` adapter                                     | Tool logic                             |
| `VRAMMonitor` with caching and hardware fallback           | Model selection (belongs in scorer.py) |
| `ModelAvailability` registry with 30s cache                | Decision making                        |
| `ModelProfile` frozen dataclasses                          |                                        |

---

### `memory/` — Memory Engine Layer

**Purpose:** Not passive storage — active retrieval, relevance scoring, decay management, and keyword indexing. The engine provides enriched context to the runtime, not raw rows.

| Owns                                                    | Must NOT Contain       |
| :------------------------------------------------------ | :--------------------- |
| SQLite persistence (WAL mode, thread-local connections) | Execution logic        |
| Context retrieval with relevance scoring                | Runtime control        |
| TTL and decay management                                | Decision making        |
| Keyword inverted index                                  | Capability invocations |
| User profile persistence                                |                        |

---

## 4. NAMING RULES

| Rule              | Requirement                                                                       |
| :---------------- | :-------------------------------------------------------------------------------- |
| No duplicates     | No duplicate semantic names across the project                                    |
| No vague folders  | No folders named `utils`, `misc`, `helpers`, `brain`, `common`                    |
| Consistent style  | `snake_case` for files and directories; `PascalCase` for classes                  |
| Clear distinction | `web_ui` (interface layer) vs `web` (capability domain)                           |
| No spaces         | Directory names never contain spaces                                              |
| File-class match  | `state_manager.py` → `StateManager`; `file_ops.py` → `FileOpsCapability`          |
| Config location   | All config in `config/runtime/`. Secrets only in `config/env/`                    |
| Test location     | All tests in `tests/`. One test file per test domain. No test files in `src/`     |
| Data outputs      | Audio → `data/audio/`; Images → `data/images/`; Screenshots → `data/screenshots/` |

---

## 5. CAPABILITY SYSTEM RULES

| #   | Rule                                                                                                                                                 |
| :-- | :--------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| 1   | ALL actions MUST exist inside `src/capabilities/`. No exceptions.                                                                                    |
| 2   | Each capability subdirectory represents a domain. Domain names are singular nouns.                                                                   |
| 3   | No logic outside `src/capabilities/` may perform actions or side-effects.                                                                            |
| 4   | Every capability MUST inherit from `BaseCapability`.                                                                                                 |
| 5   | Every capability MUST implement all four methods: (1) `execute(args)→ToolResult`, (2) `validate(args)→ValidationResult`, (3) `get_risk_level(args?)→RiskLevel` (args optional, may be None), (4) `dry_run(args)→ToolResult`. |
| 6   | Capabilities return `ToolResult` — they **NEVER** raise exceptions to the caller. All exceptions caught internally → `ToolResult.failure(...)`.      |
| 7   | Capabilities are registered via `CapabilityRegistry` loaded from `config/runtime/capabilities.yaml`. Never imported directly by non-capability code. |
| 8   | Each capability's `validate()` is called before `execute()`. Failed validation blocks execution.                                                     |
| 9   | Dynamic risk: `file_ops` computes risk per action inside `get_risk_level(args)` override.                                                            |
| 10  | Capabilities handle all platforms (Windows, Linux, macOS) internally.                                                                                |
| 11  | `WakeWordDetector` is NOT a `BaseCapability` — it is a continuous listener service, not a discrete action.                                           |

---

## 6. EXECUTION FLOW MAPPING

```
─────────────────────────────────────────────────────────────────
INTERFACE LAYER  (CLI / Web UI / Telegram)
  │
  │  user_input: str  +  session_id: str
  ▼
─────────────────────────────────────────────────────────────────
RUNTIME LOOP  src/core/runtime/loop.py  run_turn()
  │
  ├─ [1] StateManager.transition_to(IDLE → DECIDING)
  │
  ├─ [2] DECIDING: ContextAssembler + decision + priority computation
  │        ├─ ContextAssembler.assemble(user_input, session_id)
  │        │    └─ → InputPacket (with trace_id, span_id)
  │        ├─ FastPath.check(message) / Classifier.classify(message)
  │        ├─ ModelScorer.rank_models() → best model selected
  │        ├─ RiskAssessor.assess(decision)
  │        ├─ DecisionEnforcer.validate()
  │        └─ PRIORITY COMPUTED HERE (not in scheduler)
  │
  ├─ [3] StateManager.transition_to(DECIDING → SCHEDULING)
  │        └─ Scheduler: task placement + queue insertion + pre-computed deps ONLY
  │             ├─ NO priority decision (computed in DECIDING)
  │             ├─ NO retry logic (StateMachine-controlled)
  │             ├─ NO routing (pre-determined)
  │             └─ → task_id
  │
  ├─ [4] StateManager.transition_to(SCHEDULING → EXECUTING)
  │        └─ ExecutionEngine accepts task (executor ONLY)
  │             ├─ RuntimeValidator.validate(capability.scope) BEFORE execution
  │             ├─ If scope violation → BLOCK + emit CapabilityViolationEvent → ERROR
  │             ├─ ConcurrencyController.acquire_slot() (mode-bound)
  │             └─ SLAEnforcer starts monitoring (PASSIVE — emits events ONLY)
  │
  ├─ [5a] intent == tool_use → (within EXECUTING state)
  │        └─ ExecutionEngine → CapabilityRuntime (INTERNAL) → Capability
  │             ├─ Gate 1–6 pipeline (see below)
  │             └─ Results returned to EXECUTING state for evaluation
  │
  ├─ [5b] intent == chat → (within EXECUTING state)
  │        └─ Executor.execute(decision, input_packet)
  │             ├─ PromptBuilder.build(decision, input_packet)
  │             ├─ OllamaEngine.chat_with_model(model, messages, system)
  │             └─ → LLMOutput (answer | tool_call)
  │
  ├─ [6] STREAMING (OPTIONAL — ONLY for heavy tasks)
  │        └─ StreamBuffer streams chunks → EXECUTING continues
  │
  ├─ [7] StateManager.transition_to(EXECUTING → EVALUATING)
  │        └─ Evaluator.evaluate(output, decision, input_packet)
  │
  ├─ [8a] quality < 0.4 AND retry_budget > 0 → EVALUATING → DECIDING
  │        └─ StateMachine triggers retry (ONLY authority)
  │        └─ EscalationChain.retry(input_packet, attempt)
  │        └─ RetryManager.consume(1) + exponential backoff
  │
  ├─ [8b] quality OK → EVALUATING → COMPLETED → IDLE
  │
  ├─ [SLA] EXECUTING → SLAEnforcer detects timeout → emits SLAEvent
  │        └─ SLAEvent: {type, task_id, elapsed_time, threshold}
  │        └─ StateMachine receives event → decides: cancel/fallback/retry/ignore
  │        └─ SLAEnforcer NEVER cancels or retries directly
  │
  ├─ [CANCEL] ANY STATE → CANCELLED → CLEANUP → IDLE
  │        └─ StateManager.transition_to(CANCELLED, reason="user_cancel")
  │        └─ ExecutionEngine.signal(SIGTERM) → wait(2s grace) → if alive → SIGKILL
  │        └─ ExecutionEngine.confirm_termination() → {confirmed | failed}
  │        └─ ProcessPool.kill_tree() → parent + children killed
  │        └─ CLEANUP → IDLE
  │
  ├─ [ERR] ANY FAILURE → ERROR → RECOVERY → DECIDING | IDLE
  │        └─ StateMachine.transition_to(ERROR → RECOVERY)
  │        └─ if recoverable → DECIDING, else → IDLE
  │
  └─ [BATCH] (ONLY where needed — multi-item file ops)
           └─ BatchProcessor.execute() → sequential (deterministic) or bounded parallel (performance)
─────────────────────────────────────────────────────────────────

INVARIANTS (v3.2):
  1. StateMachine is ONLY decision authority — no component self-decides
  2. Scheduler handles placement ONLY — priority computed in DECIDING
  3. SLAEnforcer is PASSIVE — emits events ONLY, never cancels/retries
  4. ExecutionEngine is executor ONLY — confirms termination, no decisions
  5. RuntimeValidator validates capability.scope BEFORE execution
  6. Concurrency is mode-bound — parallelism ONLY in performance mode
  7. Dual-mode cancellation: soft(SIGTERM, 2s) → hard(SIGKILL) → confirmed
  8. ALL actions traceable to StateMachine.transition_to()
```

---

## 7. FORBIDDEN PATTERNS

| #   | Pattern                                                     | Why Forbidden                                            |
| :-- | :---------------------------------------------------------- | :------------------------------------------------------- |
| 1   | Folders named `utils`, `misc`, `helpers`, `brain`, `common` | Violates naming clarity principle                        |
| 2   | Directory names with spaces (`web ui`)                      | Breaks imports, tooling, and shell scripts               |
| 3   | Capabilities calling LLMs                                   | Capabilities execute actions, not decisions              |
| 4   | Capabilities accessing memory directly                      | Memory is an orchestration concern                       |
| 5   | Interfaces containing business logic                        | Interfaces are thin display adapters                     |
| 6   | Services executing actions                                  | Services provide data; capabilities act                  |
| 7   | Direct layer-to-layer calls bypassing state machine         | Breaks observability and auditability                    |
| 8   | Prompt-based safety approval                                | Safety enforced structurally, never by model instruction |
| 9   | String pattern matching for path validation                 | Use `Path.resolve()` + `os.path.commonpath()`            |
| 10  | Hardcoded model routing                                     | Use dynamic weighted scoring                             |
| 11  | Infinite retry loops                                        | Enforced by global retry budget (StateMachine-controlled)|
| 12  | Silent failures                                             | All errors logged with structured data                   |
| 13  | Capabilities raising exceptions to caller                   | Return `ToolResult.failure(...)`                         |
| 14  | Config files outside `config/`                              | All config in `config/runtime/` or `config/env/`         |
| 15  | Secrets in YAML files                                       | Secrets only in `config/env/.env`                        |
| 16  | Test files in `src/`                                        | All tests in `tests/`                                    |
| 17  | Importing capabilities directly (non-capability code)       | Use `CapabilityRegistry.get()`                           |
| 18  | Multiple `__init__.py` with logic in leaf packages          | Only `src/__init__.py` has content                       |
| 19  | ExecutionEngine making decisions or routing                 | ExecutionEngine is executor ONLY                         |
| 20  | ExecutionEngine triggering independent retries              | ALL retries controlled by StateMachine                   |
| 21  | Importing CapabilityRuntime from interfaces/decision/services| CapabilityRuntime is INTERNAL ONLY                      |
| 22  | Capability expanding beyond defined scope                   | Each capability has bounded allowed/forbidden operations |
| 23  | Adaptive optimizer (auto-switching strategies)              | Keep rule-based optimization only                        |
| 24  | Streaming for non-heavy tasks                               | Streaming ONLY for heavy tasks                           |
| 25  | Batching for single-item operations                         | Batching ONLY where needed (multi-item)                  |
| 26  | Scheduler making priority decisions                         | Priority computed in DECIDING state only                 |
| 27  | Scheduler implementing retry logic                          | Retry is StateMachine authority only                     |
| 28  | SLAEnforcer cancelling tasks directly                       | SLAEnforcer emits events ONLY; StateMachine decides       |
| 29  | SLAEnforcer triggering retries                              | SLAEnforcer is passive observer only                     |
| 30  | Cancellation without termination confirmation               | ExecutionEngine MUST confirm termination_status          |
| 31  | Parallel execution in deterministic mode                    | Concurrency is mode-bound                                |
| 32  | ExecutionEngine or capabilities changing execution mode     | Mode enforced by StateMachine only                       |
| 33  | Execution without capability scope validation               | RuntimeValidator MUST validate scope BEFORE execution    |

---

## 7.1 CAPABILITY BOUNDARY ENFORCEMENT

Each capability MUST define a scope contract:

```yaml
capability_scope:
  open_app:
    allowed_operations: [launch, close, restart, list_running]
    forbidden_operations: [file_access, network_access, code_execution]
    resource_limits:
      cpu_percent: 10
      memory_mb: 128
  file_ops:
    allowed_operations: [read, write, move, copy, delete, list, search]
    forbidden_operations: [execute_binary, network_access, modify_system_files]
    resource_limits:
      cpu_percent: 20
      memory_mb: 256
  code_exec:
    allowed_operations: [run_python, run_js, run_bash]
    forbidden_operations: [file_access_outside_sandbox, network_access, escalate_privileges]
    resource_limits:
      cpu_percent: 50
      memory_mb: 512
```

**Runtime Validation (v3.2):**

```
Runtime → validate(capability.scope) BEFORE execution
  → if violation → BLOCK execution + emit CapabilityViolationEvent
  → Event: {capability_name, violation_type, attempted_operation, timestamp}
```

**Rules:**
- RuntimeValidator (`src/core/runtime/capability_validator.py`) validates scope BEFORE every execution
- No capability may expand beyond its defined scope
- Cross-domain logic = NEW capability (not scope expansion)
- Resource limits enforced by Sandbox at execution time
- Violations → block + emit `CapabilityViolationEvent` → StateMachine transitions to ERROR

---

## 7.2 SLA ENFORCEMENT (PASSIVE — v3.2)

SLAEnforcer is a **passive observer** that emits events ONLY:

```yaml
SLAEvent:
  type: timeout | degradation
  task_id: str
  elapsed_time: float
  threshold: float
```

**StateMachine handles SLAEvent:**

```yaml
on_sla_event:
  actions:
    - cancel_task      → transition to ERROR → RECOVERY
    - fallback         → simpler path, continue executing
    - retry            → StateMachine-controlled retry (if budget available)
    - ignore           → log and continue (for non-critical SLA misses)
```

**Forbidden:**
- SLAEnforcer cancelling tasks directly
- SLAEnforcer triggering retries
- SLAEnforcer selecting fallback paths

---

## 7.3 CANCELLATION MODEL (DUAL-MODE — v3.2)

```yaml
cancellation:
  soft:
    signal: SIGTERM
    grace_period: 2s
  hard:
    signal: SIGKILL
```

**Execution Flow:**

```
CANCEL REQUEST → StateManager.transition_to(CANCELLED, reason="user_cancel")
  → StateManager records transition in history
  → EventBus.publish(EVT_STATE_TRANSITION, {from: EXECUTING, to: CANCELLED})
  → ExecutionEngine receives CANCELLED signal via event subscription
  → ExecutionEngine.signal(SIGTERM)
  → wait(grace_period: 2s)
  → if alive → ExecutionEngine.signal(SIGKILL)
  → ExecutionEngine.confirm_termination() → {confirmed | failed}
  → ProcessPool.kill_tree() → parent + all children killed
  → CLEANUP → IDLE
```

**Mandatory Rule:**
ExecutionEngine MUST confirm `termination_status: confirmed | failed` after every cancellation attempt.

---

## 7.4 EXECUTION MODE ENFORCEMENT (v3.2)

StateMachine enforces mode rules:

| Rule           | Deterministic              | Performance                |
| -------------- | -------------------------- | -------------------------- |
| Parallel Tasks | ❌ Blocked                  | ✅ Allowed (bounded)        |
| Task Ordering  | Strict                     | Relaxed                    |
| Retry Behavior | Fixed backoff              | Adaptive backoff           |
| Concurrency    | Disabled                   | Enabled (if no conflict)   |

**Enforcement Rules:**
- `execution_mode` (deterministic ↔ performance) is set at startup via config and CANNOT be changed at runtime
- A full process restart is required to change execution mode
- Safety mode (SAFE ↔ BALANCED ↔ UNRESTRICTED) CAN be changed at runtime via `/mode` command
- Safety mode is NOT an execution mode
- StateMachine validates mode on every transition
- ExecutionEngine CANNOT change mode
- Capabilities CANNOT alter execution mode

---

## 8. STATE MACHINE ENFORCEMENT

| Rule                   | Detail                                                                             |
| :--------------------- | :--------------------------------------------------------------------------------- |
| Single decision authority | `StateMachine` is the ONLY component that may make decisions. No self-deciding components. |
| Transition authority   | All transitions MUST go through `StateManager.transition_to()`                     |
| Invalid transitions    | Rejected, logged, system remains in current state, `InvalidTransitionError` raised |
| Error recovery         | `ERROR → RECOVERY → DECIDING | IDLE` (StateMachine decides based on recoverability) |
| Cancellation           | `ANY STATE → CANCELLED → CLEANUP → IDLE` (dual-mode: soft→hard, termination confirmed) |
| Retry authority        | ONLY StateMachine may trigger retries — no layer may retry independently           |
| SLA handling           | SLAEnforcer emits events ONLY; StateMachine decides cancel/fallback/retry/ignore   |
| Scheduler role         | Task placement + queue insertion + pre-computed dependency resolution ONLY. Priority is computed in DECIDING state and passed to scheduler as data. Scheduler NEVER computes, adjusts, or overrides task priority. |
| Mode enforcement       | StateMachine enforces deterministic/performance mode rules on every transition     |
| Capability validation  | RuntimeValidator validates scope BEFORE execution — violations block and error     |
| Forced transitions     | `force_state()` bypasses validation — for error recovery only, logs WARNING        |
| No bypasses            | No layer may bypass the state machine to invoke another layer directly             |
| History tracking       | All transitions recorded with `(from, to, timestamp, reason)` tuples               |
| Determinism mode       | `execution_mode.deterministic`: strict ordering, no parallelism, fixed retry       |
| Performance mode       | `execution_mode.performance`: relaxed ordering, bounded parallelism, adaptive retry|
| Concurrency rules      | Parallelism ONLY in performance mode AND no shared_resource_conflict               |

**Complete Transition Map (v3.2 Hardened):**

```
IDLE                 → DECIDING
DECIDING             → SCHEDULING | ERROR
SCHEDULING           → EXECUTING | ERROR
EXECUTING            → STREAMING | EVALUATING | ERROR
STREAMING            → EVALUATING | ERROR          (optional — ONLY for heavy tasks)
EVALUATING           → COMPLETED | DECIDING | ERROR  (DECIDING = StateMachine-controlled retry)
ERROR                → RECOVERY
RECOVERY             → DECIDING | IDLE              (based on recoverability)
COMPLETED            → IDLE
CANCELLED            → CLEANUP
CLEANUP              → IDLE

ANY STATE            → CANCELLED → CLEANUP → IDLE   (cancellation flow, dual-mode, confirmed)
ANY FAILURE          → ERROR → RECOVERY → ...       (error flow)

SLA EVENT HANDLING (not a state — in-band event during EXECUTING):
  SLAEnforcer emits SLAEvent → StateMachine decides:
  ├─ cancel  → EXECUTING → ERROR → RECOVERY → IDLE
  ├─ fallback→ EXECUTING → ERROR → RECOVERY → DECIDING (downgraded path)
  ├─ retry   → EXECUTING → EVALUATING → DECIDING (if retry budget > 0)
  └─ ignore  → EXECUTING continues (log event, no state change)
```

---

## 9. MIGRATION RULES

| Rule                 | Detail                                                                                              |
| :------------------- | :-------------------------------------------------------------------------------------------------- |
| Complete mapping     | Every legacy file MUST map to new structure or be explicitly deleted                                |
| No legacy            | No v2.x or v3.0-pre structure allowed alongside v3.0                                                |
| No partial migration | All files in correct location before any phase is marked complete                                   |
| Rewrite, don't move  | Legacy files that no longer fit must be rewritten, not moved                                        |
| Config relocation    | All config in `config/runtime/`. Secrets in `config/env/`                                           |
| Phase 0 migration    | `app/jarvis_slice.py` must migrate `open_app(name)` to `CapabilityExecutor.execute(...)` in Phase 9 |

---

## 10. VALIDATION CHECKLIST

| #   | Check                                         | Pass Condition                                                   |
| :-- | :-------------------------------------------- | :--------------------------------------------------------------- |
| 1   | No vague folder names                         | No `utils`, `misc`, `helpers`, `brain`, `common` anywhere        |
| 2   | No spaces in directory names                  | `web_ui` not `web ui`; `web` not `web_automation`                |
| 3   | Capability directory name                     | `web` not `web_automation`                                       |
| 4   | Safety + Sandbox present                      | `src/core/safety/` and `src/core/sandbox/` exist                 |
| 5   | Observability present                         | `src/core/observability/` with `event_bus.py`, `metrics.py`, `tracing.py`, `alerting.py` |
| 6   | All capabilities inherit BaseCapability       | Verified by ABC: all abstract methods implemented                |
| 7   | No capability raises exceptions to caller     | Verified by Sandbox/ProcessPool wrapping                       |
| 8   | All state transitions through StateManager    | No direct `self._state =` assignments outside `state_manager.py` |
| 9   | Config precedence enforced                    | CLI > ENV > .env > YAML                                          |
| 10  | Secrets only in `.env`                        | No API keys or tokens in YAML files                              |
| 11  | All tests in `tests/`                         | No `test_*.py` files in `src/`                                   |
| 12  | VERSION file exists                           | Root-level `VERSION` contains exactly `3.2.0`                    |
| 13  | All three spec files share spec_version v3.2  | Unix/macOS: `grep spec_version docs/*.md`<br>Windows: `Select-String spec_version docs/*.md`<br>All results must contain: `spec_version: v3.2` |
| 14  | `data/audio/` directory exists                | Created by setup or TTS on first use                             |
| 15  | `models.yaml` weights sum to 1.0              | Validated at `load_config()` time                                |
| 16  | `__version__ == "3.2.0"`                      | `from src import __version__; assert __version__ == "3.2.0"`     |
| 17  | AuditLogger creates `data/audit.db`           | File exists after first capability execution                     |
| 18  | ExecutionEngine is executor ONLY              | No decision/routing/retry logic in `execution_engine/`           |
| 19  | CapabilityRuntime is internal                 | Not importable by interfaces/decision/services                   |
| 20  | SLAEnforcer is passive                        | Emits events ONLY; no direct cancel/retry/fallback logic         |
| 21  | Scheduler is placement ONLY                   | No priority decision, retry logic, routing, or fallback selection |
| 22  | Priority computed in DECIDING                 | Not in scheduler                                                 |
| 23  | Sandbox hardened (system-level)               | Process isolation, privilege drop, filesystem sandbox, network policy |
| 24  | Capability scopes defined + runtime validated | RuntimeValidator validates scope BEFORE every execution          |
| 25  | Concurrency safeguards                        | Deadlock prevention, starvation prevention, priority inversion   |
| 26  | Retry controlled by StateMachine ONLY         | No independent retry loops in any layer                          |
| 27  | Streaming ONLY for heavy tasks                | No streaming for fast/medium capabilities                        |
| 28  | Batching ONLY where needed                    | Multi-item operations only, no single-item batching              |
| 29  | No adaptive optimizer                         | Rule-based optimization only, no auto-switching strategies       |
| 30  | Cancellation dual-mode                        | Soft(SIGTERM, 2s grace) → Hard(SIGKILL) → termination confirmed  |
| 31  | Error flow complete                           | ANY FAILURE → ERROR → RECOVERY → DECIDING \| IDLE               |
| 32  | Determinism mode configurable                 | `execution_mode.deterministic` and `execution_mode.performance`  |
| 33  | Mode enforcement                              | StateMachine enforces mode on every transition                   |
| 34  | Parallelism mode-bound                        | Blocked in deterministic mode; bounded in performance mode       |
| 35  | No orphan processes after cancellation        | Process tree kill + termination confirmation verified            |
| 36  | SLA isolation                                 | SLAEnforcer cannot cancel tasks or trigger retries independently |

---

## 11. SPEC ALIGNMENT AND PHASE STATUS

### Document Authority

| Document            | Purpose                                                              | Authority                |
| :------------------ | :------------------------------------------------------------------- | :----------------------- |
| `docs/TASKS.md`     | Authoritative execution plan with phase-by-phase task specifications | Implementation authority |
| `docs/STRUCTURE.md` | Canonical directory layout and layer boundaries                      | Architecture authority   |
| `docs/README.md`    | User-facing description of behavior, capabilities, and usage         | Documentation authority  |

### Alignment Rules

- All three files share `spec_version: v3.2` and `project_version: 3.2.0`.
- `STRUCTURE.md` directory tree must match `TASKS.md` canonical structure exactly.
- Breaking changes require a major version bump in all three files simultaneously.
- Structural changes update `STRUCTURE.md` first, then `TASKS.md`, then `README.md`.
- No drift between files is tolerated. Drift is a spec violation.

### Phase Completion Status (as of 2026-05-03 — v3.2 Hardening)

| Phase | Title                       | Status     | Tasks Done | Notes                                                                      |
| :---- | :-------------------------- | :--------- | :--------- | :------------------------------------------------------------------------- |
| 0     | State Machine Boot          | NEXT       | 0/4        | Hardened: single decision authority, no self-deciding components           |
| 1     | Foundation + Observability  | PENDING    | 0/15       | Extended: tracing (trace_id/span_id), replay system                         |
| 2     | Execution Contract          | PENDING    | 0/10       | Added: SystemError unified error, global error flow                         |
| 3     | Model Manager + VRAM        | PENDING    | 0/5        | Added: global model lock for concurrency                                   |
| 4     | Runtime State Machine       | PENDING    | 0/8        | Corrected flow: IDLE→DECIDING→SCHEDULING→EXECUTING→EVALUATING→COMPLETED    |
| 5     | Decision System             | PENDING    | 0/8        | Priority computed in DECIDING (not scheduler)                              |
| 6     | Sandbox + Safety (Hardened) | PENDING    | 0/9        | **HARDENED:** process isolation, privilege drop, filesystem sandbox, network policy |
| 7     | Memory Engine               | PENDING    | 0/9        | Added: concurrency model, async strategy, request queue hooks               |
| 8     | Capability System           | PENDING    | 0/12       | **RESTRICTED:** CapabilityRuntime internal-only, scope enforcement          |
| 9     | System Control Capabilities | PENDING    | 0/16       | Upgraded: intelligent modules with bounded scope                            |
| X1    | Execution Engine            | PENDING    | 0/6        | **RESTRICTED:** executor ONLY, confirms termination, no decisions/retries   |
| X2    | Sandbox System (Hardened)   | PENDING    | 0/5        | **HARDENED:** syscall restrictions, process tree kill, dual-mode cancellation |
| X3    | Performance (SLA Passive)   | PENDING    | 0/5        | **PASSIVE:** SLAEnforcer emits events ONLY, StateMachine decides + alerting |
| 10    | Prompt Builder              | PENDING    | 0/5        | Blocker: Phase 9                                                            |
| 11    | Execution Hardening         | PENDING    | 0/8        | Added: centralized retry (StateMachine-controlled), exponential backoff     |
| 12    | CLI Interface               | PENDING    | 0/3        | Blocker: Phase 11                                                           |
| 13    | Web Automation & Browser    | PENDING    | 0/3        | Blocker: Phase 12                                                           |
| 14    | Google APIs                 | PENDING    | 0/4        | Blocker: Phase 13                                                           |
| 14.5  | Telegram Integration        | PENDING    | 0/3        | Blocker: Phase 14                                                           |
| 15    | Web UI                      | PENDING    | 0/3        | Blocker: Phase 14.5                                                         |
| 16    | Voice Pipeline              | PENDING    | 0/4        | Blocker: Phase 15                                                           |
| 17    | Vision + Image              | PENDING    | 0/2        | Blocker: Phase 16                                                           |
| 18    | QA + Production             | PENDING    | 0/14       | **EXTENDED:** scheduling integrity, SLA isolation, cancellation, mode enforcement, scope violation tests |

**Hardening changes (v3.2):**
- Scheduler strictly defined: placement ONLY, priority in DECIDING
- SLAEnforcer converted to passive: emits events ONLY, StateMachine decides
- Dual-mode cancellation: soft(SIGTERM/2s grace) → hard(SIGKILL) → confirmed
- Runtime validator added: validates capability.scope BEFORE execution
- Concurrency explicitly mode-bound with safeguards
- 5 new test suites: scheduling integrity, SLA isolation, cancellation, mode enforcement, capability scope violation

> **NOTE on Phases 3 and 4:** These phases were completed ahead of Phase 2 as an extension of the Phase 0 vertical slice. They operate on stub contracts (basic dataclasses and minimal Pydantic models). Phase 2 formalizes these contracts into production-grade validated models. After Phase 2, any Phase 3/4 code that uses stub contracts MUST be updated to use the new formal contracts. This is a required migration step within Phase 2.
