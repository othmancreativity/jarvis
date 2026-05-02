# 🏗️ JARVIS v3.0 — Architecture Specification

> **spec_version:** `v3.0` | **project_version:** `3.0.0` | **structure_version:** `2`

---

## 📑 Table of Contents

1. [System Principles](#-1-system-principles)
2. [Root Structure](#-2-root-structure)
3. [Layer Definitions](#-3-layer-definitions-critical)
4. [Naming Rules](#-4-naming-rules)
5. [Capability System Rules](#-5-capability-system-rules)
6. [Execution Flow Mapping](#-6-execution-flow-mapping)
7. [Forbidden Patterns](#-7-forbidden-patterns)
8. [State Machine Enforcement](#-8-state-machine-enforcement)
9. [Migration Rules](#-9-migration-rules-important)
10. [Validation Checklist](#-10-validation-checklist)
11. [Spec Alignment (v3.0)](#-11-spec-alignment-v30)

---

## 📐 1. SYSTEM PRINCIPLES

| # | Principle | Description |
|:-:|:----------|:------------|
| 1 | **State Machine is Single Source of Truth** | All execution flow is controlled by the runtime state machine. Layers implement behavior; the state machine controls when that behavior executes. There is no layer-to-layer direct calling. |
| 2 | **Determinism Over Cleverness** | Identical inputs produce identical execution paths. No randomization, no implicit behavior, no hidden logic. |
| 3 | **Observability-First Design** | Every state transition, tool call, model swap, and failure MUST be logged with structured data. If it is not logged, it did not happen. |
| 4 | **Fail-Safe Defaults** | The system degrades gracefully. It never crashes. It never executes irreversible actions without explicit approval. |
| 5 | **Isolation of Side-Effects** | Capabilities are the ONLY layer that may execute actions. Capabilities MUST NOT call LLMs, make decisions, or access memory directly. Capability execution uses `subprocess` with strict resource limits (`timeout`, `memory_limit`, isolated temp dirs with `0o700` permissions). |
| 6 | **Single Responsibility per Layer** | Each layer has exactly one defined responsibility. No cross-layer duplication. |
| 7 | **No Vague Naming** | No folders named `utils`, `misc`, `helpers`, or `brain`. Every folder name must describe its specific responsibility. |

---

## 📦 2. ROOT STRUCTURE

```
jarvis/
│
├── app/
├── config/
│   ├── build/
│   ├── env/
│   │   ├── .env
│   │   └── .env.example
│   └── runtime/
├── data/
│   ├── memory.db
│   └── profiles/
├── docs/
│   ├── README.md
│   ├── requirements.txt
│   ├── STRUCTURE.md
│   └── TASKS.md
├── logs/
├── meta/
│   ├── .editorconfig
│   ├── .gitignore
│   └── LICENSE
├── scripts/
└── src/
    ├── capabilities/
    │   ├── api/
    │   ├── coder/
    │   ├── files/
    │   ├── notify/
    │   ├── screen/
    │   ├── search/
    │   ├── system/
    │   ├── vision/
    │   ├── voice/
    │   └── web/
    ├── core/
    │   ├── context/
    │   ├── decision/
    │   ├── observability/
    │   ├── runtime/
    │   ├── safety/
    │   └── sandbox/
    ├── interfaces/
    │   ├── cli/
    │   ├── gui/
    │   └── web_ui/
    ├── memory/
    ├── models/
    │   ├── llm/
    │   ├── speech/
    │   └── vision/
    └── services/
        ├── google/
        ├── integrations/
        └── telegram/
```

---

## 🏛️ 3. LAYER DEFINITIONS (CRITICAL)

### 🧠 `core/`

> **Purpose:** System orchestration and execution control. Controls WHEN and HOW other layers execute via the state machine.

| | |
|:--|:--|
| **Owns** | • Runtime state machine and loop control<br>• Decision system (intent classification, model selection, scoring)<br>• Context handling (InputPacket assembly, prompt building)<br>• Safety enforcement (`safety/` — structured validation, permission checks, command allow/deny)<br>• Execution sandbox (`sandbox/` — `subprocess` with resource limits, timeout, isolated temp dirs)<br>• Observability (`observability/` — metrics, tracing, replay, EventBus with `queue.Queue`-based dispatch) |
| **Must NOT contain** | • Tool implementations<br>• External API clients<br>• UI logic<br>• Model loading/unloading logic (belongs in `models/`) |

---

### ⚡ `capabilities/`

> **Purpose:** ALL executable actions in the system. The ONLY layer that may perform side-effects.

| | |
|:--|:--|
| **Owns** | • System control (app launching, system info, clipboard)<br>• File operations (read, write, list, delete, move, copy)<br>• Web automation (Playwright browser control)<br>• Screen/vision/audio actions (screenshot, OCR, STT, TTS)<br>• Code execution (sandboxed via `subprocess`)<br>• Web search<br>• Notifications<br>• API-based integrations |
| **Must NOT contain** | • Decision logic<br>• Model selection<br>• LLM calls<br>• Memory access<br>• Routing logic |

---

### 🖥️ `interfaces/`

> **Purpose:** User interaction layer. Converts user input into runtime requests and displays runtime responses.

| | |
|:--|:--|
| **Owns** | • CLI interface (chat loop, formatting, special commands)<br>• GUI interface (desktop application)<br>• Web UI (FastAPI backend, WebSocket, frontend) |
| **Must NOT contain** | • Business logic<br>• Tool execution<br>• Decision making<br>• State management |

---

### 🔌 `services/`

> **Purpose:** External system connectors. Provides data sources that capabilities may use.

| | |
|:--|:--|
| **Owns** | • Telegram bot integration<br>• Google APIs (Calendar, Gmail, Drive)<br>• Third-party integrations |
| **Must NOT contain** | • Core logic<br>• Decision making<br>• Tool execution (services provide data; capabilities execute actions) |

---

### 🤖 `models/`

> **Purpose:** Model adapters and model lifecycle management.

| | |
|:--|:--|
| **Owns** | • Model Manager (VRAM monitoring, model lifecycle, concurrency control)<br>• LLM adapters (Ollama wrapper)<br>• Speech model adapters<br>• Vision model adapters<br>• Model capability profiles |
| **Must NOT contain** | • Routing logic<br>• Tool logic<br>• Decision making<br>• Model selection (belongs in `core/decision/`) |

---

### 🧩 `memory/`

> **Purpose:** Memory Engine — retrieval, scoring, decay/TTL, indexing. Not just storage.

| | |
|:--|:--|
| **Owns** | • SQLite persistence (short-term and long-term storage)<br>• Context retrieval with relevance scoring<br>• Memory relevance scoring system<br>• Time-to-live and decay management<br>• Keyword indexing<br>• User profile storage |
| **Must NOT contain** | • Execution logic<br>• Runtime control<br>• Decision making |

---

## 🏷️ 4. NAMING RULES

| Rule | Requirement |
|:-----|:------------|
| **No duplicates** | No duplicate semantic names across the project. |
| **No vague folders** | No folders named `utils`, `misc`, `helpers`, `brain`, `common`. |
| **Consistent style** | `snake_case` for files and directories, `PascalCase` for classes. |
| **Clear distinction** | `web_ui` (interface) vs `web` (capability). |
| **File-class match** | Files must match their class name: `state_manager.py` contains `StateManager`. |

---

## ⚙️ 5. CAPABILITY SYSTEM RULES

| # | Rule |
|:--|:-----|
| 1 | ALL actions MUST exist inside `capabilities/`. |
| 2 | Capabilities represent domains, not individual functions. |
| 3 | No logic outside `capabilities/` may perform actions or side-effects. |
| 4 | Every capability MUST inherit from `BaseCapability`. |
| 5 | Every capability MUST implement: `execute()`, `validate(self, args: dict) -> ValidationResult`, `get_risk_level()`. |
| 6 | Every capability MUST support dry-run mode. |
| 7 | Capabilities are registered via the CapabilityRegistry, not imported directly. |

---

## 🔄 6. EXECUTION FLOW MAPPING

> Execution flows through the state machine, not directly between layers:

```
Interface → Runtime (IDLE → DECIDING)
         → Decision (produces DecisionOutput)
         → Runtime (DECIDING → EXECUTING_MODEL)
         → Models (via Model Manager)
         → Runtime (EXECUTING_MODEL → EVALUATING or EXECUTING_TOOL)
         → Sandbox (tool execution via subprocess with resource limits)
         → Capabilities (actual tool logic)
         → Runtime (EXECUTING_TOOL → WAITING_CONFIRMATION if risk=medium/high in BALANCED mode)
         → Runtime (WAITING_CONFIRMATION → EXECUTING_TOOL on confirmation, or IDLE on cancel)
         → Runtime (EVALUATING → COMPLETED or back to DECIDING)
         → Memory (store turn data)
         → Interface (display FinalResponse)
```

> **Rule:** No layer calls another layer directly. All calls are routed through the Runtime state machine.

---

## 🚫 7. FORBIDDEN PATTERNS

| # | Pattern | Why |
|:--|:--------|:----|
| 1 | `brain` folder or any folder with ambiguous purpose | Violates naming clarity |
| 2 | Duplicate tool locations | Each tool exists in exactly one capability |
| 3 | Agents before stable runtime | State machine must exist first |
| 4 | Mixing UI with logic | Interfaces are thin, core handles all logic |
| 5 | Mixing models with decision | Models provide adapters; decision does scoring |
| 6 | Direct layer-to-layer calls | All flow through state machine |
| 7 | Prompt-based safety approval | Safety is enforced by the Safety layer |
| 8 | String pattern matching for path validation | Use `Path.resolve()` + `os.path.commonpath()` |
| 9 | Hardcoded model routing | Use dynamic weighted scoring with `VRAMMonitor().get_total_vram_mb()` |
| 10 | Infinite retry loops | Enforced by global retry budget |

---

## 🔒 8. STATE MACHINE ENFORCEMENT

| Rule | Detail |
|:-----|:-------|
| **Single source of truth** | The state machine in `src/core/runtime/state.py` and `state_manager.py`. |
| **Transition enforcement** | All state transitions MUST go through `StateManager.transition_to()`. |
| **Invalid transitions** | Rejected, logged, and the system remains in the current state. |
| **Error recovery** | `ERROR` state always transitions to `IDLE` (safe exit). |
| **Confirmation state** | `WAITING_CONFIRMATION` state used when `ModeEnforcer` returns `confirm` for medium/high risk in `BALANCED`/`SAFE` modes. |
| **No bypasses** | No layer may bypass the state machine to directly invoke another layer. |

---

## 🔄 9. MIGRATION RULES (IMPORTANT)

| Rule | Detail |
|:-----|:-------|
| **Complete mapping** | Any old folder MUST be mapped to the new structure or removed. |
| **No legacy** | No legacy structure is allowed. |
| **No partial migration** | All files must be placed in their correct location. |
| **Rewrite, don't move** | Legacy files that no longer fit the architecture must be rewritten, not moved. |

---

## ✅ 10. VALIDATION CHECKLIST

| # | Check | Result |
|:--|:------|:-------|
| 1 | Can a new developer understand structure in <2 minutes? | ✅ |
| 2 | Does every folder have a single responsibility? | ✅ |
| 3 | Is any action outside capabilities? | ❌ FAIL |
| 4 | Any duplication? | ❌ FAIL |
| 5 | Any layer bypassing the state machine? | ❌ FAIL |
| 6 | Any hardcoded model routing? | ❌ FAIL |
| 7 | Any prompt-based safety approval? | ❌ FAIL |
| 8 | Any infinite retry paths? | ❌ FAIL |
| 9 | Any folder named `utils`, `misc`, `helpers`, `brain`, `common`? | ❌ FAIL |

---

## 🔗 11. SPEC ALIGNMENT (v3.0)

| Principle | Detail |
|:----------|:-------|
| **Single source of truth** | `TASKS.md` is the authoritative execution plan. `STRUCTURE.md` defines the canonical directory layout and layer boundaries. `README.md` describes user-facing behavior. |
| **Version discipline** | All three files share `spec_version: "v3.0"` and `project_version: "3.0.0"`. Breaking changes require major version bump. |
| **No drift** | STRUCTURE.md directory tree must match TASKS.md canonical structure exactly. Any structural change requires updating both files. |
| **Migration rule** | Legacy structure (v1.0/v2.0) is archived. All new work targets v3.0 contracts. |
