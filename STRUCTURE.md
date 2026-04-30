## 1. SYSTEM PRINCIPLES

- **State Machine is Single Source of Truth:** All execution flow is controlled by the runtime state machine. Layers implement behavior; the state machine controls when that behavior executes. There is no layer-to-layer direct calling.
- **Determinism Over Cleverness:** Identical inputs produce identical execution paths. No randomization, no implicit behavior, no hidden logic.
- **Observability-First Design:** Every state transition, tool call, model swap, and failure MUST be logged with structured data. If it is not logged, it did not happen.
- **Fail-Safe Defaults:** The system degrades gracefully. It never crashes. It never executes irreversible actions without explicit approval.
- **Isolation of Side-Effects:** Capabilities are the ONLY layer that may execute actions. Capabilities MUST NOT call LLMs, make decisions, or access memory directly.
- **Single Responsibility per Layer:** Each layer has exactly one defined responsibility. No cross-layer duplication.
- **No Vague Naming:** No folders named `utils`, `misc`, `helpers`, or `brain`. Every folder name must describe its specific responsibility.

## 2. ROOT STRUCTURE

```
jarvis/
├── app/                          # Application entry points
│   ├── main.py                   # Main CLI/Web entry point
│   └── jarvis_slice.py           # Phase 0 minimal working system (legacy proof)
├── config/                       # All configuration files
│   ├── settings.yaml             # Runtime settings (gitignored)
│   ├── settings.example.yaml     # Template with all defaults
│   ├── capabilities.yaml         # Capability manifest with risk levels
│   ├── models.yaml               # Model profiles and scoring weights
│   ├── jarvis_identity.yaml      # Jarvis identity and personality
│   ├── mode_fragments.yaml       # Prompt fragments per execution mode
│   └── production.yaml           # Production-ready configuration
├── src/
│   ├── core/                     # System orchestration and execution control
│   │   ├── context/              # InputPacket assembly, prompt building
│   │   ├── decision/             # Intent classification, model selection, scoring
│   │   ├── runtime/              # State machine, loop control, limits, timeouts
│   │   ├── safety/               # Structured validation, permission enforcement
│   │   ├── sandbox/              # Safe tool execution environment
│   │   ├── observability/        # Metrics, tracing, replay, failure analysis
│   │   └── events.py             # EventBus for loose coupling
│   ├── capabilities/             # ALL executable actions (and ONLY actions)
│   │   ├── base.py               # Abstract BaseCapability class
│   │   ├── registry.py           # Capability registry and discovery
│   │   ├── executor.py           # Capability execution pipeline
│   │   ├── validator.py          # Schema validation for capability arguments
│   │   ├── result.py             # ToolResult dataclass
│   │   ├── system/               # System control: apps, sysinfo, clipboard
│   │   ├── files/                # File operations
│   │   ├── notify/               # Notifications
│   │   ├── screen/               # Screenshot, OCR
│   │   ├── coder/                # Code execution
│   │   ├── search/               # Web search
│   │   ├── web_automation/       # Playwright browser automation
│   │   ├── voice/                # STT, TTS, wake word
│   │   └── vision/               # Image understanding, image generation
│   ├── interfaces/               # User interaction layer
│   │   ├── cli/                  # CLI interface
│   │   └── web/                  # Web UI (FastAPI + WebSocket)
│   ├── services/                 # External system connectors
│   │   ├── telegram/             # Telegram bot
│   │   └── google/               # Google APIs (Calendar, Gmail, Drive)
│   ├── models/                   # Model adapters and management
│   │   ├── manager.py            # Model Manager: VRAM, lifecycle, concurrency
│   │   ├── profiles.py           # Model capability profiles
│   │   ├── llm/                  # LLM adapters (Ollama)
│   │   ├── speech/               # Speech model adapters
│   │   └── vision_models/        # Vision model adapters
│   └── memory/                   # Memory Engine: retrieval, scoring, TTL, indexing
│       ├── database.py           # SQLite persistence
│       ├── retriever.py          # Context retrieval with relevance scoring
│       ├── scorer.py             # Memory relevance scoring
│       ├── ttl.py                # Time-to-live and decay management
│       ├── indexer.py            # Keyword indexing
│       └── user_profile.py       # User profile storage
├── tests/                        # All test files
│   ├── test_contracts.py
│   ├── test_state_machine.py
│   ├── test_decision.py
│   ├── test_decision_dynamic.py
│   ├── test_safety.py
│   ├── test_memory.py
│   ├── test_capabilities.py
│   ├── test_integration.py
│   ├── test_performance.py
│   ├── test_arabic.py
│   ├── test_observability.py
│   └── test_sandbox.py
├── STRUCTURE.md
├── README.md
└── TASKS.md
```

## 3. LAYER DEFINITIONS (CRITICAL)

### core/

**Purpose:** System orchestration and execution control. Controls WHEN and HOW other layers execute via the state machine.

**Owns:**
- Runtime state machine and loop control.
- Decision system (intent classification, model selection, scoring).
- Context handling (InputPacket assembly, prompt building).
- Safety enforcement (structured validation, permission checks).
- Execution sandbox (safe tool execution environment).
- Observability (metrics, tracing, replay).

**Must NOT contain:**
- Tool implementations.
- External API clients.
- UI logic.
- Model loading/unloading logic (belongs in `models/manager.py`).

### capabilities/

**Purpose:** ALL executable actions in the system. The ONLY layer that may perform side-effects.

**Owns:**
- System control (app launching, system info, clipboard).
- File operations (read, write, list, delete, move, copy).
- Web automation (Playwright browser control).
- Screen/vision/audio actions (screenshot, OCR, STT, TTS).
- Code execution (sandboxed).
- Web search.
- Notifications.

**Must NOT contain:**
- Decision logic.
- Model selection.
- LLM calls.
- Memory access.
- Routing logic.

### interfaces/

**Purpose:** User interaction layer. Converts user input into runtime requests and displays runtime responses.

**Owns:**
- CLI interface (chat loop, formatting, special commands).
- Web UI (FastAPI backend, WebSocket, frontend).

**Must NOT contain:**
- Business logic.
- Tool execution.
- Decision making.
- State management.

### services/

**Purpose:** External system connectors. Provides data sources that capabilities may use.

**Owns:**
- Telegram bot integration.
- Google APIs (Calendar, Gmail, Drive).
- Third-party integrations.

**Must NOT contain:**
- Core logic.
- Decision making.
- Tool execution (services provide data; capabilities execute actions).

### models/

**Purpose:** Model adapters and model lifecycle management.

**Owns:**
- Model Manager (VRAM monitoring, model lifecycle, concurrency control).
- LLM adapters (Ollama wrapper).
- Speech model adapters.
- Vision model adapters.
- Model capability profiles.

**Must NOT contain:**
- Routing logic.
- Tool logic.
- Decision making.
- Model selection (belongs in `core/decision/`).

### memory/

**Purpose:** Memory Engine — retrieval, scoring, decay/TTL, indexing. Not just storage.

**Owns:**
- SQLite persistence (short-term and long-term storage).
- Context retrieval with relevance scoring.
- Memory relevance scoring system.
- Time-to-live and decay management.
- Keyword indexing.
- User profile storage.

**Must NOT contain:**
- Execution logic.
- Runtime control.
- Decision making.

## 4. NAMING RULES

- No duplicate semantic names across the project.
- No vague folders (`utils`, `misc`, `helpers`, `brain`, `common`).
- Consistent naming: `snake_case` for files and directories, `PascalCase` for classes.
- Clear distinction between similar concepts: `web_ui` (interface) vs `web_automation` (capability).
- Files must match their class name: `state_manager.py` contains `StateManager`.

## 5. CAPABILITY SYSTEM RULES

- ALL actions MUST exist inside `capabilities/`.
- Capabilities represent domains, not individual functions.
- No logic outside `capabilities/` may perform actions or side-effects.
- Every capability MUST inherit from `BaseCapability`.
- Every capability MUST implement: `execute()`, `validate()`, `get_risk_level()`.
- Every capability MUST support dry-run mode.
- Capabilities are registered via the CapabilityRegistry, not imported directly.

## 6. EXECUTION FLOW MAPPING

Execution flows through the state machine, not directly between layers:

```
Interface → Runtime (IDLE → DECIDING)
         → Decision (produces DecisionOutput)
         → Runtime (DECIDING → EXECUTING_MODEL)
         → Models (via Model Manager)
         → Runtime (EXECUTING_MODEL → EVALUATING or EXECUTING_TOOL)
         → Sandbox (tool execution)
         → Capabilities (actual tool logic)
         → Runtime (EVALUATING → COMPLETED or back to DECIDING)
         → Memory (store turn data)
         → Interface (display FinalResponse)
```

No layer calls another layer directly. All calls are routed through the Runtime state machine.

## 7. FORBIDDEN PATTERNS

- `brain` folder or any folder with ambiguous purpose.
- Duplicate tool locations (each tool exists in exactly one capability).
- Agents before stable runtime (state machine must exist first).
- Mixing UI with logic (interfaces are thin, core handles all logic).
- Mixing models with decision (models provide adapters; decision does scoring).
- Direct layer-to-layer calls (all flow through state machine).
- Prompt-based safety approval (safety is enforced by the Safety layer).
- String pattern matching for safety validation (use structured schema validation).
- Hardcoded model routing (use dynamic weighted scoring).
- Infinite retry loops (enforced by global retry budget).

## 8. STATE MACHINE ENFORCEMENT

- The state machine in `src/core/runtime/state.py` and `state_manager.py` is the single source of truth.
- All state transitions MUST go through `StateManager.transition_to()`.
- Invalid transitions are rejected, logged, and the system remains in the current state.
- `ERROR` state always transitions to `IDLE` (safe exit).
- No layer may bypass the state machine to directly invoke another layer.

## 9. MIGRATION RULES (IMPORTANT)

- Any old folder MUST be mapped to the new structure or removed.
- No legacy structure is allowed.
- No partial migration — all files must be placed in their correct location.
- Legacy files that no longer fit the architecture must be rewritten, not moved.

## 10. VALIDATION CHECKLIST

- Can a new developer understand structure in <2 minutes?
- Does every folder have a single responsibility?
- Is any action outside capabilities? → FAIL
- Any duplication? → FAIL
- Any layer bypassing the state machine? → FAIL
- Any hardcoded model routing? → FAIL
- Any prompt-based safety approval? → FAIL
- Any infinite retry paths? → FAIL
- Any folder named `utils`, `misc`, `helpers`, `brain`, `common`? → FAIL
