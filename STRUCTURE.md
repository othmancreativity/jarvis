# 🏗️ JARVIS v3.0 — Architecture Specification

> **spec_version:** `v3.0` | **project_version:** `3.0.0` | **structure_version:** `2`

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
11. [Spec Alignment](#11-spec-alignment)

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
|  8  | **Contract-First Design**                   | All data contracts (InputPacket, DecisionOutput, ToolResult, FinalResponse) are defined and validated before any logic uses them.                                                        |
|  9  | **Config Precedence**                       | CLI args > shell ENV > .env file > YAML defaults. No exceptions.                                                                                                                         |
| 10  | **Security by Structure**                   | Safety is enforced by the Safety layer, not by prompting the model. Path validation uses `Path.resolve()` + `os.path.commonpath()`.                                                      |

---

## 2. ROOT STRUCTURE

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

## 3. LAYER DEFINITIONS

### `core/`

**Purpose:** System orchestration and execution control. Controls WHEN and HOW other layers execute via the state machine.

| Owns                                                          | Must NOT Contain                        |
| :------------------------------------------------------------ | :-------------------------------------- |
| Runtime state machine and loop control                        | Tool implementations                    |
| Decision system (intent, model selection, scoring)            | External API clients                    |
| Context handling (InputPacket assembly, prompt building)      | UI logic                                |
| Safety enforcement (structured validation, permission checks) | Model loading/unloading logic           |
| Execution sandbox (subprocess with resource limits)           | Direct capability invocation            |
| Observability (metrics, tracing, EventBus)                    | Business logic tied to specific domains |

---

### `capabilities/`

**Purpose:** ALL executable actions in the system. The ONLY layer that may perform side-effects. Each capability is a complete, self-contained tool with its own contract, validation, error handling, dry-run mode, risk classification, and tests.

**Capability Sovereignty Rules:**

- Each capability owns its full input contract (schema, required fields, enum values).
- Each capability owns its own risk classification logic.
- Each capability implements dry-run without side effects.
- Each capability returns `ToolResult` — never raises exceptions to the caller.
- Each capability validates args before executing — validation is synchronous and fast.
- Each capability handles all platform variations internally.

| Owns                                                    | Must NOT Contain       |
| :------------------------------------------------------ | :--------------------- |
| System control (apps, system info, clipboard)           | Decision logic         |
| File operations (read, write, list, delete, move, copy) | Model selection        |
| Web automation (Playwright browser control)             | LLM calls              |
| Screen capture, OCR                                     | Memory access          |
| Code execution (sandboxed subprocess)                   | Routing logic          |
| Web search                                              | Cross-capability calls |
| Notifications                                           | State machine access   |
| Voice I/O (STT, TTS, wake word)                         |                        |
| Vision (image analysis, image generation)               |                        |

---

### `interfaces/`

**Purpose:** User interaction layer. Thin — converts user input into runtime requests and displays runtime responses. Contains no business logic.

| Owns                                                 | Must NOT Contain |
| :--------------------------------------------------- | :--------------- |
| CLI interface (chat loop, formatting, commands)      | Business logic   |
| GUI interface (desktop application shell)            | Tool execution   |
| Web UI (FastAPI backend, WebSocket, static frontend) | Decision making  |
| Signal handling and graceful shutdown                | State management |

---

### `services/`

**Purpose:** External system connectors. Provides data sources that capabilities may use. Services are passive — they provide data; capabilities execute actions.

| Owns                                 | Must NOT Contain |
| :----------------------------------- | :--------------- |
| Telegram bot integration             | Core logic       |
| Google APIs (Calendar, Gmail, Drive) | Decision making  |
| Third-party service clients          | Tool execution   |
| OAuth token management               | State management |

---

### `models/`

**Purpose:** Model adapters and model lifecycle management. Does not select models — that belongs in `core/decision/`.

| Owns                                                    | Must NOT Contain                                       |
| :------------------------------------------------------ | :----------------------------------------------------- |
| Model Manager (VRAM monitoring, lifecycle, concurrency) | Routing logic                                          |
| LLM adapters (Ollama wrapper)                           | Tool logic                                             |
| Speech model adapters                                   | Decision making                                        |
| Vision model adapters                                   | Model selection (belongs in `core/decision/scorer.py`) |
| Model capability profiles                               |                                                        |

---

### `memory/`

**Purpose:** Memory Engine — not just storage. Retrieval, scoring, decay/TTL, keyword indexing.

| Owns                                          | Must NOT Contain |
| :-------------------------------------------- | :--------------- |
| SQLite persistence (short-term and long-term) | Execution logic  |
| Context retrieval with relevance scoring      | Runtime control  |
| Memory relevance scoring                      | Decision making  |
| TTL and decay management                      |                  |
| Keyword indexing                              |                  |
| User profile persistence                      |                  |

---

## 4. NAMING RULES

| Rule              | Requirement                                                                             |
| :---------------- | :-------------------------------------------------------------------------------------- |
| No duplicates     | No duplicate semantic names across the project.                                         |
| No vague folders  | No folders named `utils`, `misc`, `helpers`, `brain`, `common`.                         |
| Consistent style  | `snake_case` for files and directories, `PascalCase` for classes.                       |
| Clear distinction | `web_ui` (interface) vs `web` (capability). No spaces in directory names.               |
| File-class match  | `state_manager.py` contains `StateManager`. `file_ops.py` contains `FileOpsCapability`. |
| Config location   | All config files in `config/runtime/`. Secrets in `config/env/`.                        |
| Test location     | All tests in `tests/`. One test file per domain.                                        |

---

## 5. CAPABILITY SYSTEM RULES

| #   | Rule                                                                                                                                                                                    |
| :-- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | ALL actions MUST exist inside `src/capabilities/`. No exceptions.                                                                                                                       |
| 2   | Each capability subdirectory represents a domain. Domain names are singular nouns.                                                                                                      |
| 3   | No logic outside `src/capabilities/` may perform actions or side-effects.                                                                                                               |
| 4   | Every capability MUST inherit from `BaseCapability`.                                                                                                                                    |
| 5   | Every capability MUST implement: `execute(args: dict) -> ToolResult`, `validate(args: dict) -> ValidationResult`, `get_risk_level() -> RiskLevel`, `dry_run(args: dict) -> ToolResult`. |
| 6   | Capabilities return `ToolResult` — they NEVER raise exceptions to the caller. All exceptions are caught internally and wrapped into `ToolResult.failure(...)`.                          |
| 7   | Capabilities are registered via `CapabilityRegistry` loaded from `config/runtime/capabilities.yaml`. They are never imported directly by non-capability code.                           |
| 8   | Each capability's `validate()` is called before `execute()`. If validation fails, execution is blocked.                                                                                 |
| 9   | Each capability defines its own risk level. Dynamic risk (e.g., `file_ops` delete vs read) is resolved inside the capability's `get_risk_level(args)` override.                         |
| 10  | Capabilities must handle all supported platforms (Windows, Linux, macOS) internally. Platform detection is done inside the capability.                                                  |

---

## 6. EXECUTION FLOW MAPPING

```
Interface Layer
  │
  └─→ Runtime Loop (IDLE → DECIDING)
        │
        ├─→ ContextAssembler → InputPacket
        │
        ├─→ Decision System → DecisionOutput
        │     ├─ FastPath (regex rules, <1ms)
        │     ├─ Classifier (LLM call)
        │     ├─ ModelScorer (weighted scoring)
        │     └─ RiskAssessor (risk classification)
        │
        ├─→ (DECIDING → EXECUTING_MODEL)
        │     └─→ Executor → OllamaEngine → LLMOutput
        │
        ├─→ (DECIDING → EXECUTING_TOOL)
        │     └─→ CapabilityExecutor
        │           ├─ Gate 1: Decision Consistency
        │           ├─ Gate 2: SafetyClassifier + ModeEnforcer
        │           ├─ Gate 3: SchemaValidator
        │           ├─ Gate 4: Confirmation (if mode requires)
        │           ├─ Gate 5: Dry Run (if requested)
        │           └─ Gate 6: Sandbox.execute() → Capability.execute() → ToolResult
        │
        ├─→ (EXECUTING_TOOL → WAITING_CONFIRMATION)
        │     └─→ Wait for user signal → Resume or Cancel
        │
        ├─→ (EXECUTING_MODEL/TOOL → EVALUATING)
        │     └─→ Evaluator → EvaluationResult
        │
        ├─→ (EVALUATING → COMPLETED or → DECIDING for retry)
        │
        └─→ (COMPLETED → IDLE)
              ├─→ Memory.store(turn)
              └─→ Interface.display(FinalResponse)
```

**Invariant:** No layer calls another layer directly. All calls route through the Runtime state machine.

---

## 7. FORBIDDEN PATTERNS

| #   | Pattern                                                     | Why Forbidden                                    |
| :-- | :---------------------------------------------------------- | :----------------------------------------------- |
| 1   | Folders named `utils`, `misc`, `helpers`, `brain`, `common` | Violates naming clarity                          |
| 2   | Directory names with spaces (e.g., `web ui`)                | Breaks imports and tooling                       |
| 3   | Capabilities calling LLMs                                   | Capabilities execute actions, not decisions      |
| 4   | Capabilities accessing memory directly                      | Memory is a Core concern                         |
| 5   | Interfaces containing business logic                        | Interfaces are thin display layers               |
| 6   | Services executing actions                                  | Services provide data, capabilities act          |
| 7   | Direct layer-to-layer calls bypassing state machine         | Breaks observability and control                 |
| 8   | Prompt-based safety approval                                | Safety enforced structurally, not by model       |
| 9   | String pattern matching for path validation                 | Use `Path.resolve()` + `os.path.commonpath()`    |
| 10  | Hardcoded model routing                                     | Use dynamic weighted scoring                     |
| 11  | Infinite retry loops                                        | Enforced by global retry budget                  |
| 12  | Silent failures                                             | All errors logged with structured data           |
| 13  | Capabilities raising exceptions to caller                   | Capabilities return `ToolResult.failure(...)`    |
| 14  | Config files outside `config/`                              | All config in `config/runtime/` or `config/env/` |
| 15  | Secrets in YAML files                                       | Secrets only in `config/env/.env`                |

---

## 8. STATE MACHINE ENFORCEMENT

| Rule                   | Detail                                                                                     |
| :--------------------- | :----------------------------------------------------------------------------------------- |
| Single source of truth | `src/core/runtime/state.py` and `state_manager.py`.                                        |
| Transition enforcement | All transitions MUST go through `StateManager.transition_to()`.                            |
| Invalid transitions    | Rejected, logged, system remains in current state, `InvalidTransitionError` raised.        |
| Error recovery         | `ERROR → IDLE` is the only recovery path.                                                  |
| Confirmation state     | `WAITING_CONFIRMATION` is used when `ModeEnforcer` returns `confirm` for medium/high risk. |
| No bypasses            | No layer may bypass the state machine to invoke another layer directly.                    |
| History tracking       | All transitions are recorded with timestamp and reason.                                    |

**Transition Map:**

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

| Rule                 | Detail                                                                                           |
| :------------------- | :----------------------------------------------------------------------------------------------- |
| Complete mapping     | Every old file MUST map to the new structure or be deleted.                                      |
| No legacy            | No legacy structure allowed alongside v3.0.                                                      |
| No partial migration | All files must be in their correct location before testing.                                      |
| Rewrite, don't move  | Legacy files that no longer fit must be rewritten, not moved.                                    |
| Config relocation    | All config files move from `config/` root to `config/runtime/`. Env files move to `config/env/`. |

---

## 10. VALIDATION CHECKLIST

| #   | Check                                         | Pass Condition                                            |
| :-- | :-------------------------------------------- | :-------------------------------------------------------- |
| 1   | No vague folder names                         | No `utils`, `misc`, `helpers`, `brain`, `common` anywhere |
| 2   | No spaces in directory names                  | `web_ui` not `web ui`                                     |
| 3   | Capability directory name                     | `web` not `web_automation`                                |
| 4   | Safety + Sandbox exist                        | `src/core/safety/` and `src/core/sandbox/` present        |
| 5   | Observability exists                          | `src/core/observability/` present                         |
| 6   | All capabilities inherit BaseCapability       | Verified by import test                                   |
| 7   | All capabilities implement 4 required methods | Verified by ABC enforcement                               |
| 8   | No capability raises exceptions to caller     | Verified by sandbox wrapping                              |
| 9   | All state transitions through StateManager    | Verified by no direct `_state =` assignments              |
| 10  | Config precedence enforced                    | CLI > ENV > .env > YAML                                   |
| 11  | Secrets only in .env                          | No API keys in YAML files                                 |
| 12  | All tests in `tests/`                         | No test files in `src/`                                   |
| 13  | VERSION file exists                           | Contains `3.0.0`                                          |
| 14  | All three spec files share spec_version v3.0  | Verified by grep                                          |

---

## 11. SPEC ALIGNMENT (v3.0)

| Document       | Purpose                                                                                    | Authority                |
| :------------- | :----------------------------------------------------------------------------------------- | :----------------------- |
| `TASKS.md`     | Authoritative execution plan. Phase-by-phase task specifications with validation criteria. | Implementation authority |
| `STRUCTURE.md` | Canonical directory layout and layer boundaries.                                           | Architecture authority   |
| `README.md`    | User-facing description of behavior, capabilities, and usage.                              | Documentation authority  |

**Alignment Rules:**

- All three files share `spec_version: v3.0` and `project_version: 3.0.0`.
- `STRUCTURE.md` directory tree must match `TASKS.md` canonical structure exactly.
- Breaking changes require major version bump in all three files simultaneously.
- Any structural change updates `STRUCTURE.md` first, then `TASKS.md`, then `README.md`.
- No drift between files is tolerated. Drift is a spec violation.
