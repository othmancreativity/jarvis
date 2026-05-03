# 🏗️ JARVIS v3.0 — Architecture Specification

> **spec_version:** `v3.0` | **project_version:** `3.0.0` | **structure_version:** `3`
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
|  1  | **State Machine is Single Source of Truth** | All execution flow is controlled by the runtime state machine. No layer may call another layer directly.                                                                                 |
|  2  | **Determinism Over Cleverness**             | Identical inputs produce identical execution paths. No randomization, no implicit behavior.                                                                                              |
|  3  | **Observability-First Design**              | Every state transition, tool call, model swap, and failure MUST be logged with structured data.                                                                                          |
|  4  | **Fail-Safe Defaults**                      | The system degrades gracefully. Never crashes. Never executes irreversible actions without explicit approval.                                                                            |
|  5  | **Capabilities are Sovereign**              | Capabilities are the ONLY layer that may execute side-effects. Each capability is a complete, standalone tool with its own validation, error handling, dry-run, and risk classification. |
|  6  | **Single Responsibility per Layer**         | Each layer has exactly one defined responsibility. No cross-layer duplication.                                                                                                           |
|  7  | **No Vague Naming**                         | No folders named `utils`, `misc`, `helpers`, `brain`, or `common`. Every folder name describes its specific responsibility.                                                              |
|  8  | **Contract-First Design**                   | All data contracts (`InputPacket`, `DecisionOutput`, `ToolResult`, `FinalResponse`) are defined and validated before any logic uses them.                                                |
|  9  | **Config Precedence**                       | CLI args > shell ENV > `.env` file > YAML defaults. No exceptions.                                                                                                                       |
| 10  | **Security by Structure**                   | Safety is enforced by the Safety layer, not by prompting the model. Path validation uses `Path.resolve()` + `os.path.commonpath()`.                                                      |

---

## 2. ROOT STRUCTURE

```
jarvis/
│
├── VERSION                          ← Single-line version string: "3.0.0"
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
│   ├── .gitignore                   ← Includes: settings.yaml, .env, logs/, data/*.db, __pycache__
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
    ├── __init__.py                  ← ONLY __init__.py at this level. Sets __version__ = "3.0.0"
    │
    ├── capabilities/                ← SOVEREIGN LAYER: all side-effectful actions live here exclusively
    │   ├── base.py                  ← BaseCapability ABC: execute, validate, get_risk_level, dry_run
    │   ├── executor.py              ← CapabilityExecutor: 6-gate pipeline (registry→validate→permission→confirm→dryrun→sandbox)
    │   ├── registry.py              ← CapabilityRegistry singleton: register, get, load_from_manifest
    │   ├── result.py                ← ToolResult Pydantic model + failure/success_result factories
    │   ├── validator.py             ← ValidationResult dataclass + SchemaValidator (YAML-driven)
    │   ├── api/                     ← Reserved: future external API capability modules
    │   ├── coder/
    │   │   └── executor.py          ← CodeExecutorCapability: python/js/bash in isolated subprocess
    │   ├── files/
    │   │   └── file_ops.py          ← FileOpsCapability: read/write/list/delete/move/copy with path validation
    │   ├── notify/
    │   │   └── toasts.py            ← NotificationCapability: desktop toast via plyer with fallback
    │   ├── screen/
    │   │   └── capture.py           ← ScreenshotCapability: PIL ImageGrab + optional pytesseract OCR
    │   ├── search/
    │   │   └── web_search.py        ← WebSearchCapability: DuckDuckGo HTML parse → structured results
    │   ├── system/
    │   │   ├── apps.py              ← AppLauncher: platform-aware app discovery and launch
    │   │   ├── clipboard.py         ← ClipboardCapability: pyperclip read/write
    │   │   └── sysinfo.py           ← SystemInfoCapability: psutil CPU/RAM/GPU/OS metrics
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
    │   ├── config.py                ← load_config() with Pydantic validation + 4-level precedence
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
    │   │   ├── output.py            ← DecisionOutput + all enums: Intent, Complexity, ExecutionMode, etc.
    │   │   ├── risk.py              ← RiskAssessor: tool-level and arg-level risk classification
    │   │   └── scorer.py            ← ModelScorer: weighted multi-factor scoring + deterministic ranking
    │   ├── observability/
    │   │   ├── event_bus.py         ← EventBus singleton: pub/sub with isolated exception handling
    │   │   └── metrics.py           ← MetricsCollector singleton: latency percentiles, errors, model usage
    │   ├── runtime/
    │   │   ├── degradation.py       ← DegradationHandler: model/tool failure → user-friendly fallback
    │   │   ├── escalation.py        ← EscalationChain: tiered retry with weight adjustment + forced fallback
    │   │   ├── evaluation_result.py ← EvaluationResult Pydantic model
    │   │   ├── evaluator.py         ← Evaluator: heuristic quality scoring (completeness + relevance + coherence)
    │   │   ├── executor.py          ← Executor: LLM call layer → LLMOutput (does NOT handle retries)
    │   │   ├── fallback.py          ← FallbackSystem: tier-1 then tier-2 model substitution
    │   │   ├── final_response.py    ← FinalResponse Pydantic model + error_response() factory
    │   │   ├── limits.py            ← Limits: all numeric execution ceilings loaded from config
    │   │   ├── llm_output.py        ← LLMOutput Pydantic model (answer | tool_call)
    │   │   ├── loop.py              ← run_turn(): main orchestration loop, never raises, always returns FinalResponse
    │   │   ├── retry.py             ← RetryManager: per-turn budget counter
    │   │   ├── state.py             ← RuntimeState enum + ALLOWED_TRANSITIONS map
    │   │   ├── state_manager.py     ← StateManager: transition_to(), force_state(), history tracking
    │   │   ├── timeout.py           ← TimeoutHandler + phase_timeout() context manager
    │   │   └── validate_decision.py ← DecisionEnforcer: structural validation of DecisionOutput
    │   ├── safety/
    │   │   ├── audit.py             ← AuditLogger: SQLite log of every capability execution attempt
    │   │   ├── classifier.py        ← SafetyClassifier: path traversal, blocked path, code pattern checks
    │   │   ├── mode_enforcer.py     ← ModeEnforcer: SAFE/BALANCED/UNRESTRICTED permission matrix
    │   │   └── permission.py        ← PermissionLayer: Gate1(consistency) + Gate2(safety) + Gate3(schema)
    │   └── sandbox/
    │       └── sandbox.py           ← Sandbox: ThreadPoolExecutor isolation + timeout + exception wrapping
    │
    ├── interfaces/                  ← THIN DISPLAY LAYER: converts user I/O to/from runtime requests
    │   ├── cli/
    │   │   ├── chat.py              ← CLIChat: main REPL loop with thinking indicator and session management
    │   │   ├── commands.py          ← CommandHandler: /help /mode /replay /debug /status /quit
    │   │   └── formatting.py        ← CLIFormatter: colorama output, [DEGRADED] prefix, RTL Arabic mark
    │   ├── gui/                     ← Reserved: future desktop GUI (Tkinter/PyQt)
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
        ├── integrations/            ← Reserved: future third-party service connectors
        └── telegram/
            ├── bot.py               ← TelegramBot: async message handler → run_turn() via asyncio.to_thread
            └── commands.py          ← Telegram command handlers: /start /mode /status /quit
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
| Execution sandbox (`sandbox.py`)                                                       | Direct capability invocation (must go via `CapabilityExecutor`) |
| Observability (`event_bus.py`, `metrics.py`)                                           | Domain-specific business logic                                  |
| Hardening (`timeout.py`, `degradation.py`, `fallback.py`, `retry.py`, `escalation.py`) |                                                                 |

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
| Telegram bot handler                 | Core orchestration logic |
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
| 5   | Every capability MUST implement: `execute(args: dict) → ToolResult`, `validate(args: dict) → ValidationResult`, `get_risk_level(args: dict           | None) → RiskLevel`, `dry_run(args: dict) → ToolResult`. |
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
  ├─ [2] ContextAssembler.assemble(user_input, session_id)
  │        └─ load_profile(user_id)
  │        └─ MemoryDB.retrieve_recent(session_id, limit=5)
  │        └─ → InputPacket
  │
  ├─ [3] decide(input_packet) → DecisionOutput
  │        ├─ FastPath.check(message)          ← regex, <1ms, bilingual
  │        │    └─ if match → assess_risk → return immediately
  │        ├─ Classifier.classify(message)     ← LLM call, JSON extract+repair
  │        ├─ VRAMMonitor.get_available_vram_mb()
  │        ├─ ModelScorer.rank_models()        ← weighted 5-factor scoring
  │        ├─ RiskAssessor.assess(decision)
  │        └─ DecisionEnforcer.validate()
  │
  ├─ [4a] intent == tool_use → DECIDING → EXECUTING_TOOL
  │        └─ CapabilityExecutor.execute(name, args, decision, mode)
  │             ├─ Gate 1: CapabilityRegistry.get(name) → not None
  │             ├─ Gate 2: capability.validate(args) → valid
  │             ├─ Gate 3: PermissionLayer.check() → allow/confirm/block
  │             │            ├─ SubGate A: tool_name consistency
  │             │            ├─ SubGate B: SafetyClassifier + ModeEnforcer
  │             │            └─ SubGate C: SchemaValidator
  │             ├─ Gate 4: if confirm → publish EVT_WAITING_CONFIRMATION → wait
  │             ├─ Gate 5: if dry_run → Sandbox.dry_run() → return
  │             └─ Gate 6: Sandbox.execute(capability, args, timeout_s)
  │                           └─ ThreadPoolExecutor(max_workers=1)
  │                           └─ capability.execute(args) → ToolResult
  │
  ├─ [4b] intent == chat → DECIDING → EXECUTING_MODEL
  │        └─ Executor.execute(decision, input_packet)
  │             ├─ PromptBuilder.build(decision, input_packet)
  │             │    ├─ Identity block (jarvis_identity.yaml)
  │             │    ├─ Mode fragment (mode_fragments.yaml)
  │             │    ├─ Context block (memory_snippets)
  │             │    ├─ History block (recent_history[-3:])
  │             │    └─ Language hint (if language=ar)
  │             ├─ OllamaEngine.chat_with_model(model, messages, system)
  │             └─ → LLMOutput (answer | tool_call)
  │
  ├─ [5] EXECUTING_* → EVALUATING
  │        └─ Evaluator.evaluate(output, decision, input_packet)
  │             ├─ Completeness score  (weight: 0.40)
  │             ├─ Relevance score     (weight: 0.40)
  │             └─ Coherence score     (weight: 0.20)
  │
  ├─ [6a] quality < 0.4 AND retry_budget > 0 → EVALUATING → DECIDING
  │        └─ EscalationChain.retry(input_packet, attempt)
  │        └─ RetryManager.consume(1)
  │
  ├─ [6b] quality OK → EVALUATING → COMPLETED
  │
  ├─ [7] COMPLETED → IDLE
  │        ├─ MemoryDB.store(session_id, turn_data)
  │        ├─ AuditLogger.log_action(...)
  │        ├─ MetricsCollector.record_latency(...)
  │        └─ publish EVT_TURN_COMPLETE
  │
  └─ [ERR] Any JarvisError → ERROR → IDLE
             └─ DegradationHandler.generate_error_response()
             └─ return FinalResponse.error_response(...)
─────────────────────────────────────────────────────────────────

INVARIANT: No layer calls another layer directly.
           All calls route through the Runtime state machine.
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
| 11  | Infinite retry loops                                        | Enforced by global retry budget (8 default)              |
| 12  | Silent failures                                             | All errors logged with structured data                   |
| 13  | Capabilities raising exceptions to caller                   | Return `ToolResult.failure(...)`                         |
| 14  | Config files outside `config/`                              | All config in `config/runtime/` or `config/env/`         |
| 15  | Secrets in YAML files                                       | Secrets only in `config/env/.env`                        |
| 16  | Test files in `src/`                                        | All tests in `tests/`                                    |
| 17  | Importing capabilities directly (non-capability code)       | Use `CapabilityRegistry.get()`                           |
| 18  | Multiple `__init__.py` with logic in leaf packages          | Only `src/__init__.py` has content                       |

---

## 8. STATE MACHINE ENFORCEMENT

| Rule                   | Detail                                                                             |
| :--------------------- | :--------------------------------------------------------------------------------- |
| Single source of truth | `src/core/runtime/state.py` defines states and transition map                      |
| Transition authority   | All transitions MUST go through `StateManager.transition_to()`                     |
| Invalid transitions    | Rejected, logged, system remains in current state, `InvalidTransitionError` raised |
| Error recovery         | `ERROR → IDLE` is the only recovery path from ERROR                                |
| Forced transitions     | `force_state()` bypasses validation — for error recovery only, logs WARNING        |
| Confirmation state     | `WAITING_CONFIRMATION` entered when `ModeEnforcer` returns `confirm`               |
| No bypasses            | No layer may bypass the state machine to invoke another layer directly             |
| History tracking       | All transitions recorded with `(from, to, timestamp, reason)` tuples               |

**Complete Transition Map:**

```
IDLE                 → DECIDING
DECIDING             → EXECUTING_MODEL | EXECUTING_TOOL | ERROR
EXECUTING_MODEL      → EVALUATING | EXECUTING_TOOL | ERROR
EXECUTING_TOOL       → WAITING_CONFIRMATION | EVALUATING | ERROR
WAITING_CONFIRMATION → EXECUTING_TOOL | ERROR | IDLE
EVALUATING           → COMPLETED | DECIDING | ERROR
ERROR                → IDLE
COMPLETED            → IDLE
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
| 5   | Observability present                         | `src/core/observability/` with `event_bus.py` and `metrics.py`   |
| 6   | All capabilities inherit BaseCapability       | Verified by ABC import test                                      |
| 7   | All capabilities implement 4 required methods | Verified by ABC enforcement                                      |
| 8   | No capability raises exceptions to caller     | Verified by Sandbox wrapping                                     |
| 9   | All state transitions through StateManager    | No direct `self._state =` assignments outside `state_manager.py` |
| 10  | Config precedence enforced                    | CLI > ENV > .env > YAML                                          |
| 11  | Secrets only in `.env`                        | No API keys or tokens in YAML files                              |
| 12  | All tests in `tests/`                         | No `test_*.py` files in `src/`                                   |
| 13  | VERSION file exists                           | Root-level `VERSION` contains exactly `3.0.0`                    |
| 14  | All three spec files share spec_version v3.0  | `grep spec_version docs/*.md` all return `v3.0`                  |
| 15  | `data/audio/` directory exists                | Created by setup or TTS on first use                             |
| 16  | `models.yaml` weights sum to 1.0              | Validated at `load_config()` time                                |
| 17  | `__version__ == "3.0.0"`                      | `from src import __version__; assert __version__ == "3.0.0"`     |
| 18  | AuditLogger creates `data/audit.db`           | File exists after first capability execution                     |

---

## 11. SPEC ALIGNMENT AND PHASE STATUS

### Document Authority

| Document            | Purpose                                                              | Authority                |
| :------------------ | :------------------------------------------------------------------- | :----------------------- |
| `docs/TASKS.md`     | Authoritative execution plan with phase-by-phase task specifications | Implementation authority |
| `docs/STRUCTURE.md` | Canonical directory layout and layer boundaries                      | Architecture authority   |
| `docs/README.md`    | User-facing description of behavior, capabilities, and usage         | Documentation authority  |

### Alignment Rules

- All three files share `spec_version: v3.0` and `project_version: 3.0.0`.
- `STRUCTURE.md` directory tree must match `TASKS.md` canonical structure exactly.
- Breaking changes require a major version bump in all three files simultaneously.
- Structural changes update `STRUCTURE.md` first, then `TASKS.md`, then `README.md`.
- No drift between files is tolerated. Drift is a spec violation.

### Phase Completion Status (as of 2026-05-03)

| Phase | Title                       | Status     | Tasks Done | Notes                                                                      |
| :---- | :-------------------------- | :--------- | :--------- | :------------------------------------------------------------------------- |
| 0     | First Working System        | ✅ DONE    | 5/5        | Vertical slice. Phase 9 must migrate `open_app()` calls.                   |
| 1     | Foundation + Observability  | ✅ DONE    | 13/13      | All infrastructure, config, logging, EventBus, exceptions operational.     |
| 2     | Execution Contract          | 🔴 NEXT    | 0/10       | **Current blocker.** Formalizes all Pydantic contracts.                    |
| 3     | Model Manager + VRAM        | ✅ DONE    | 5/5        | Completed ahead of Phase 2 via vertical slice work. Uses stub contracts.   |
| 4     | Runtime State Machine       | ✅ DONE    | 8/8        | Completed ahead of Phase 2. State machine operational with stub contracts. |
| 5     | Decision System             | ⬜ PENDING | 0/7        | Blocker: Phase 2                                                           |
| 6     | Sandbox + Safety            | ⬜ PENDING | 0/7        | Blocker: Phase 5                                                           |
| 7     | Memory Engine               | ⬜ PENDING | 0/6        | Blocker: Phase 6                                                           |
| 8     | Capability System           | ⬜ PENDING | 0/6        | Blocker: Phase 7                                                           |
| 9     | System Control Capabilities | ⬜ PENDING | 0/8        | Blocker: Phase 8                                                           |
| 10    | Prompt Builder              | ⬜ PENDING | 0/5        | Blocker: Phase 9                                                           |
| 11    | Execution Hardening         | ⬜ PENDING | 0/6        | Blocker: Phase 10                                                          |
| 12    | CLI Interface               | ⬜ PENDING | 0/3        | Blocker: Phase 11                                                          |
| 13    | Web Automation & Browser    | ⬜ PENDING | 0/3        | Blocker: Phase 12                                                          |
| 14    | Google APIs                 | ⬜ PENDING | 0/4        | Blocker: Phase 13                                                          |
| 14.5  | Telegram Integration        | ⬜ PENDING | 0/3        | Blocker: Phase 14                                                          |
| 15    | Web UI                      | ⬜ PENDING | 0/3        | Blocker: Phase 14.5                                                        |
| 16    | Voice Pipeline              | ⬜ PENDING | 0/4        | Blocker: Phase 15                                                          |
| 17    | Vision + Image              | ⬜ PENDING | 0/2        | Blocker: Phase 16                                                          |
| 18    | QA + Production             | ⬜ PENDING | 0/6        | Blocker: Phase 17                                                          |

> **NOTE on Phases 3 and 4:** These phases were completed ahead of Phase 2 as an extension of the Phase 0 vertical slice. They operate on stub contracts (basic dataclasses and minimal Pydantic models). Phase 2 formalizes these contracts into production-grade validated models. After Phase 2, any Phase 3/4 code that uses stub contracts MUST be updated to use the new formal contracts. This is a required migration step within Phase 2.
