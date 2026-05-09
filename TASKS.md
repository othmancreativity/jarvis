# 📋 JARVIS v3.2 — Execution Plan

> **spec_version:** `v3.2` | **project_version:** `3.2.0` | **structure_version:** `3.2`
> **last_updated:** `2026-05-03`

---

## 📑 Table of Contents

- [Project Status](#project-status)
- [Dependency Graph](#dependency-graph)
- [Canonical Directory Structure](#canonical-directory-structure)
- [Legend](#legend)
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
- [Final Validation Checklist](#final-validation-checklist)

---

## Project Status

```yaml
project:
  name: JARVIS
  version: "3.2.0"
  spec_version: "v3.2"
  structure_version: "3.2"
  last_updated: "2026-05-03"
  current_phase: 2
  overall_progress_percent: 0
  risk_level: "medium"
  hardware_profile:
    gpu: "RTX 3050 6GB VRAM"
    ram: "16 GB"
    cpu: "Intel Core i5 12th Gen"
  current_blocker: "none"
  next_action: "TASK 2.0"
  config_root: "config/runtime/"
  env_root: "config/env/"
  hardening_pass: true
  key_changes_v3_2:
    - "Scheduler strictly defined: placement ONLY, priority in DECIDING state"
    - "SLAEnforcer converted to passive: emits SLAEvent ONLY, StateMachine decides"
    - "Dual-mode cancellation: soft(SIGTERM, 2s grace) → hard(SIGKILL) → termination confirmed"
    - "RuntimeValidator added: validates capability.scope BEFORE execution"
    - "Concurrency explicitly mode-bound with deadlock/starvation/priority safeguards"
    - "5 new test suites: scheduling integrity, SLA isolation, cancellation, mode enforcement, capability scope violation"
  phases_complete:
  phases_pending:
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, "14.5", 15, 16, 17, 18]
  notes:
    - "23% was a planning estimate for spec completeness, not implementation progress."
    - "Implementation progress starts at Phase 0."
    - "v3.2 hardening: strict enforcement + ambiguity removal. Control > power."
    - "Phase 9 must migrate app/jarvis_slice.py open_app() calls to CapabilityExecutor.execute()."
    - "data/audio/ directory added in v3 structure for TTS output files."
    - "RELEASE_NOTES.md added to docs/ in v3 structure."
```

---

## Dependency Graph

```
Phase 0 (State Machine Boot)
  └─→ Phase 1 (Foundation + Observability)
        └─→ Phase 2 (Execution Contract)
              └─→ Phase 3 (Model Manager + VRAM)
                    └─→ Phase 4 (Runtime State Machine — corrected flow)
                          └─→ Phase 5 (Decision System)
                                └─→ Phase 6 (Sandbox + Safety — HARDENED)
                                      └─→ Phase 7 (Memory Engine)
                                            └─→ Phase 8 (Capability System — RESTRICTED)
                                                  └─→ Phase 9 (System Control — BOUNDED SCOPE)
                                                        └─→ Phase X1 (Execution Engine — EXECUTOR ONLY)
                                                              └─→ Phase X2 (Sandbox System — HARDENED)
                                                                    └─→ Phase X3 (Performance — SLA ENFORCED)
                                                                          └─→ Phase 10 (Prompt Builder)
                                                                                └─→ Phase 11 (Execution Hardening)
                                                                                      └─→ Phase 12 (CLI Interface)
                                                                                            └─→ Phase 13 (Web Automation & Browser)
                                                                                                  └─→ Phase 14 (Google APIs)
                                                                                                        └─→ Phase 14.5 (Telegram Integration)
                                                                                                              └─→ Phase 15 (Web UI)
                                                                                                                    └─→ Phase 16 (Voice Pipeline)
                                                                                                                          └─→ Phase 17 (Vision + Image)
                                                                                                                                └─→ Phase 18 (QA + Production — EXTENDED TESTING)

Critical Path: 0 → 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9 → X1 → X2 → X3 → 10 → 11 → 12 → 13 → 14 → 14.5 → 15 → 16 → 17 → 18
```

**Design Order Rationale:**

1. State Machine (Phase 0) — foundation of all execution flow, single controller
2. Observability (Phase 1) — trace everything from day one (tracing + replay)
3. Contracts (Phase 2) — formalize all data shapes (Pydantic + SystemError)
4. Models (Phase 3) — hardware-aware model management
5. Runtime Loop (Phase 4) — wire state machine to contracts with corrected flow
6. Decision (Phase 5) — fast-path deterministic first, LLM fallback
7. Sandbox (Phase 6) — isolate ALL capability executions (HARDENED: system-level)
8. Memory (Phase 7) — active retrieval with scoring + decay + concurrency
9. **Capability System (Phase 8)** — RESTRICTED: CapabilityRuntime internal-only, scope enforcement
10. **System Control (Phase 9)** — bounded scope, intelligent modules with defined limits
11. **Execution Engine (Phase X1)** — EXECUTOR ONLY: no decisions, no retries, no routing
12. **Sandbox System (Phase X2)** — HARDENED: syscall restrictions, process tree kill
13. **Performance (Phase X3)** — SLA enforced: fast=100ms, medium=500ms, heavy=5000ms
14. Hardening (Phase 11) — centralized retry (StateMachine-controlled), exponential backoff

---

## Canonical Directory Structure

```
jarvis/
│
├── VERSION    ← Single-line version string: "3.2.0"
├── app/
│   ├── __init__.py
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
│   ├── audio/
│   ├── images/
│   ├── memory.db       ← SQLite: turn history, memory snippets (WAL mode)
│   ├── audit.db        ← SQLite: capability execution audit log (WAL mode)
│   ├── metrics.db      ← SQLite: real-time system metrics, historical tracking (WAL)
│   │   Schema: `system_metrics(id, session_id, timestamp, metric_type, value, threshold, alert_fired, trace_id)`
│   │   Indexes: `idx_metrics_timestamp`, `idx_metrics_type`
│   │   PRAGMA journal_mode=WAL
│   ├── profiles/
│   └── screenshots/
│
├── docs/
│   ├── README.md
│   ├── RELEASE_NOTES.md
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
│   ├── test_web_automation.py
│   └── test_web_ui.py
│
└── src/
    ├── __init__.py                  ← ONLY __init__.py at this level. Sets __version__ = "3.2.0"
    ├── capabilities/
    │   ├── base.py
    │   ├── executor.py
    │   ├── registry.py
    │   ├── result.py
    │   ├── validator.py
    │   ├── runtime/               ← CAPABILITY RUNTIME: INTERNAL ONLY
    │   │   ├── capability_runtime.py ← CapabilityRuntime: execute_async, batch, stream, cancel
    │   │   ├── progress.py        ← ProgressTracker: percentage, ETA, status updates
    │   │   ├── stream.py          ← StreamBuffer: chunked output for long-running tasks
    │   │   └── cancellation.py    ← CancellationToken: cooperative async cancellation
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
    │   ├── execution_engine/      ← EXECUTOR ONLY: no decisions, no retries, no routing
    │   │   ├── scheduler.py       ← TaskScheduler: placement + queue insertion ONLY
    │   │   ├── async_executor.py  ← AsyncExecutor: non-blocking capability execution
    │   │   ├── batch_processor.py ← BatchProcessor: multi-item execution
    │   │   ├── cancellation.py    ← ProcessCancellationController: SIGTERM→SIGKILL dual-mode
    │   │   └── concurrency.py     ← ConcurrencyController: mode-bound parallelism
    │   ├── observability/
    │   │   ├── event_bus.py         ← EventBus singleton: pub/sub, EventEnvelope, EVT_* constants
    │   │   ├── metrics.py           ← MetricsCollector singleton: latency percentiles, errors
    │   │   ├── tracing.py           ← TracingSystem: trace_id + span_id propagation
    │   │   └── alerting.py          ← AlertManager: passive alert rules, EVT_THRESHOLD_ALERT
    │   ├── performance/           ← PASSIVE MONITORING: SLA events, rule-based profiling
    │   │   ├── profiler.py        ← ExecutionProfiler: per-capability metrics
    │   │   ├── sla_enforcer.py    ← SLAEnforcer: PASSIVE — emits SLAEvent ONLY
    │   │   ├── benchmark.py       ← BenchmarkRunner: performance regression testing
    │   │   └── cache.py           ← SmartCache: TTL + LRU eviction
    │   ├── runtime/
    │   │   ├── capability_validator.py ← RuntimeValidator: validates scope BEFORE execution
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
    │   └── sandbox/               ← HARDENED ISOLATION: process isolation, privilege drop
    │       ├── sandbox.py         ← Sandbox: ThreadPoolExecutor isolation + timeout
    │       ├── resource_monitor.py← ResourceMonitor: CPU/RAM tracking per execution
    │       ├── process_pool.py    ← ProcessPool: isolated subprocess + tree kill
    │       └── filesystem.py      ← FilesystemRestrictor: allowlist paths
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
    ├── memory/
    │   ├── database.py
    │   ├── indexer.py
    │   ├── retriever.py
    │   ├── scorer.py
    │   ├── ttl.py
    │   └── user_profile.py
    ├── models/
    │   ├── availability.py
    │   ├── manager.py
    │   ├── profiles.py
    │   ├── vram_monitor.py
    │   ├── llm/
    │   │   └── engine.py
    │   ├── speech/
    │   └── vision/
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

## Legend

```
[Priority]
P0 = Critical — system cannot function without this
P1 = High — core functionality blocked
P2 = Medium — significant feature, deferrable
P3 = Low — enhancement, post-MVP

[Progress Bar]
█ = Completed | ░ = Remaining (10-unit scale; ratio shown numerically)

[Phase Status]
 DONE     — all tasks validated
 NEXT     — immediate next to implement
 PENDING  — blocked by prior phase
```

---

## Phase Progress Summary

| Phase | Title                       | Priority | Progress   | Ratio | Status  |
| :---- | :-------------------------- | :------- | :--------- | :---- | :------ |
| 0     | State Machine Boot          | P0       | ░░░░░░░░░░ | 0/5   | NEXT    |
| 1     | Foundation + Observability  | P0       | ░░░░░░░░░░ | 0/16  | PENDING |
| 2     | Execution Contract          | P0       | ░░░░░░░░░░ | 0/10  | PENDING |
| 3     | Model Manager + VRAM        | P0       | ░░░░░░░░░░ | 0/5   | PENDING |
| 4     | Runtime State Machine       | P0       | ░░░░░░░░░░ | 0/8   | PENDING |
| 5     | Decision System             | P1       | ░░░░░░░░░░ | 0/8   | PENDING |
| 6     | Sandbox + Safety (Hardened) | P0       | ░░░░░░░░░░ | 0/9   | PENDING |
| 7     | Memory Engine               | P1       | ░░░░░░░░░░ | 0/9   | PENDING |
| 8     | Capability System           | P1       | ░░░░░░░░░░ | 0/12  | PENDING |
| 9     | System Control              | P1       | ░░░░░░░░░░ | 0/16  | PENDING |
| 10    | Prompt Builder              | P1       | ░░░░░░░░░░ | 0/5   | PENDING |
| 11    | Execution Hardening         | P0       | ░░░░░░░░░░ | 0/6   | PENDING |
| 12    | CLI Interface               | P2       | ░░░░░░░░░░ | 0/3   | PENDING |
| 13    | Web Automation & Browser    | P2       | ░░░░░░░░░░ | 0/3   | PENDING |
| 14    | Google APIs                 | P2       | ░░░░░░░░░░ | 0/4   | PENDING |
| 14.5  | Telegram Integration        | P2       | ░░░░░░░░░░ | 0/3   | PENDING |
| 15    | Web UI                      | P2       | ░░░░░░░░░░ | 0/3   | PENDING |
| 16    | Voice Pipeline              | P3       | ░░░░░░░░░░ | 0/4   | PENDING |
| 17    | Vision + Image              | P3       | ░░░░░░░░░░ | 0/2   | PENDING |
| 18    | QA + Production             | P0       | ░░░░░░░░░░ | 0/9   | PENDING |

**Hardening changes (v3.2):**
- Single controller authority (StateMachine ONLY)
- ExecutionEngine restricted to executor role
- Scheduler restricted to placement ONLY (priority in DECIDING)
- CapabilityRuntime internal-only with RuntimeValidator
- Sandbox hardened to system-level with dual-mode cancellation
- SLA passive events (SLAEnforcer emits ONLY, StateMachine decides)
- Capability boundary enforcement with pre-execution validation
- Concurrency safeguards mode-bound (deadlock, starvation, priority inversion)
- 5 new test suites: scheduling integrity, SLA isolation, cancellation, mode enforcement, capability scope
- Rule-based optimization only (no adaptive optimizer)
- Extended testing: chaos, fault injection, load, timeout, sandbox escape

---

## Phase 0 — Minimal State Machine Boot

```yaml
phase_id: 0
priority: "P0"
status: "not_started"
total_tasks: 5
validation_status: "pending"
last_updated: "2026-05-03"
```

Phase 0 establish the runtime state machine as the **single decision authority**. No direct layer-to-layer calls are permitted — all interactions route through `StateManager.transition_to()`. Implements minimal deterministic state transitions: `IDLE → DECIDING → SCHEDULING → EXECUTING → EVALUATING → COMPLETED`. Stub contracts are used for rapid boot; formal contracts are introduced in Phase 2.

**Prohibitions:**

- No direct wiring between input → classifier → tool
- No layer may invoke another layer directly
- No capabilities execute outside the sandbox
- All state transitions must pass through `StateManager`
- No component may self-decide (including SLA, scheduler, sandbox)

**Tasks:**

1. Define `RuntimeState` enum and `ALLOWED_TRANSITIONS` frozenset map (corrected v3.2 flow)
2. Implement `StateManager.transition_to()` with thread lock and transition history
3. Implement minimal `run_turn()` loop enforcing state machine flow
4. Validate all layer interactions route through state machine (no direct assignments)
5. Implement `FORBIDDEN_LOOPS` + `MAX_TRANSITIONS_PER_TURN` guard rails (TASK 0.5)

**Artifacts:** `src/core/runtime/state.py` (RuntimeState, ALLOWED_TRANSITIONS, FORBIDDEN_LOOPS, MAX_TRANSITIONS_PER_TURN), `src/core/runtime/state_manager.py` (transition_to, reset_turn_counter, force_state, transition history, cycle guard), `src/core/runtime/loop.py` (minimal boot version with turn counter reset)

---

### TASK 0.5 — Transition Guard Rails + Cycle Detection

**Location:** `src/core/runtime/state.py`, `src/core/runtime/state_manager.py`
**Depends on:** TASK 0.2 (`StateManager.transition_to()`)
**Purpose:** With 11 states and cascading error/cancellation paths, unbounded re-entry creates infinite loops. Hard limits per cycle and explicit forbidden loop table prevent state explosion at the enforcement layer — not just in documentation.

#### Subtask 0.5.1 — Add `FORBIDDEN_LOOPS` to `state.py`

```python
# src/core/runtime/state.py — extend existing module

# Transitions that form illegal cycles (e.g. ERROR → ERROR means
# the system is stuck and must force-transition to RECOVERY or IDLE)
FORBIDDEN_LOOPS: frozenset[tuple[RuntimeState, RuntimeState]] = frozenset({
    (RuntimeState.ERROR,    RuntimeState.ERROR),
    (RuntimeState.RECOVERY, RuntimeState.RECOVERY),
    (RuntimeState.CLEANUP,  RuntimeState.CLEANUP),
    (RuntimeState.DECIDING, RuntimeState.DECIDING),   # re-entry without SCHEDULING
})

# Hard ceiling: how many transitions are allowed within one run_turn() call
MAX_TRANSITIONS_PER_TURN: int = 20
```

**Rule:** `FORBIDDEN_LOOPS` is checked inside `StateManager.transition_to()` BEFORE the transition executes. Violation → `InvalidTransitionError` + force to `RECOVERY`.

#### Subtask 0.5.2 — Enforce in `StateManager.transition_to()`

```python
# src/core/runtime/state_manager.py — extend existing transition_to()

def transition_to(self, new_state: RuntimeState, reason: str = "") -> None:
    with self._lock:
        # --- NEW: cycle guard ---
        pair = (self._state, new_state)
        if pair in FORBIDDEN_LOOPS:
            self._log_warning(f"Forbidden loop detected: {pair}")
            self._force_to_recovery()
            raise InvalidTransitionError(f"Forbidden loop: {pair}")

        # --- NEW: turn transition ceiling ---
        self._turn_transitions += 1
        if self._turn_transitions > MAX_TRANSITIONS_PER_TURN:
            self._log_error("MAX_TRANSITIONS_PER_TURN exceeded — forcing IDLE")
            self._force_state(RuntimeState.IDLE, reason="transition_limit_exceeded")
            return

        # ... existing transition logic ...

def reset_turn_counter(self) -> None:
    """Call at the START of every run_turn() invocation."""
    self._turn_transitions = 0
```

#### Subtask 0.5.3 — Test coverage (3 tests)

Add to `tests/test_state_machine.py`:

```python
def test_forbidden_loop_error_to_error_raises():
    sm = StateManager()
    sm.force_state(RuntimeState.ERROR)
    with pytest.raises(InvalidTransitionError):
        sm.transition_to(RuntimeState.ERROR)

def test_forbidden_loop_recovery_to_recovery_raises():
    sm = StateManager()
    sm.force_state(RuntimeState.RECOVERY)
    with pytest.raises(InvalidTransitionError):
        sm.transition_to(RuntimeState.RECOVERY)

def test_max_transitions_per_turn_triggers_idle():
    sm = StateManager()
    sm.reset_turn_counter()
    # Exhaust budget with valid transitions
    for _ in range(MAX_TRANSITIONS_PER_TURN + 1):
        try:
            sm.transition_to(RuntimeState.DECIDING)
            sm.force_state(RuntimeState.IDLE)
        except Exception:
            break
    assert sm.current_state == RuntimeState.IDLE
```

**Artifacts:** Updated `src/core/runtime/state.py`, `src/core/runtime/state_manager.py`, `tests/test_state_machine.py`

**Definition of Done:**
- [ ] `FORBIDDEN_LOOPS` frozenset defined in `state.py`
- [ ] `MAX_TRANSITIONS_PER_TURN = 20` enforced in `StateManager`
- [ ] All 3 new tests pass alongside existing state machine tests

---

## Phase 1 — Foundation + Observability

```yaml
phase_id: 1
priority: "P0"
status: "not_started"
total_tasks: 16
validation_status: "Phase 0 complete"
last_updated: "2026-05-03"
```

All 16 tasks complete. The project is an installable Python package with validated configuration, structured logging, full observability infrastructure (EventBus, MetricsCollector, structured tracing with trace_id/span_id, execution replay system, EventEnvelope delivery contract), custom exception hierarchy, model profiles, capabilities manifest, user profiles, and shared test fixtures.

**Key additions over previous version:**

- Structured tracing: every state transition logged with `trace_id`, `span_id`, `from_state`, `to_state`
- Replay system: `EventBus` persists events to `data/audit.db` for full execution replay
- Trace context propagation through all layer boundaries

**Artifacts:** `pyproject.toml`, `requirements.txt`, all `__init__.py` files, `config/runtime/settings.yaml`, `config/runtime/settings.example.yaml`, `src/core/config.py`, `src/core/logging_setup.py`, `src/models/profiles.py`, `config/runtime/models.yaml`, `config/env/.env`, `config/env/.env.example`, `src/memory/user_profile.py`, `config/runtime/capabilities.yaml`, `src/core/observability/metrics.py`, `src/core/observability/tracing.py`, `src/core/observability/alerting.py`, `app/main.py`, `src/core/observability/event_bus.py` (with replay, EventEnvelope, delivery contract, EVT_* constants), `src/core/exceptions.py` (with SystemError), `tests/conftest.py`

---

### TASK 1.14 — Structured Tracing System

**Location:** `src/core/observability/tracing.py`
**Depends on:** TASK 1.1–1.13 complete
**Purpose:** Every execution path is traced with `trace_id` (from `InputPacket`) and `span_id` (generated per layer crossing). Enables full replay and debugging.

#### Subtask 1.14.1 — Define `TraceContext` and `TracingSystem`

```python
# src/core/observability/tracing.py
import uuid
from dataclasses import dataclass, field

@dataclass
class TraceContext:
    trace_id: str
    span_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    parent_span_id: str | None = None

class TracingSystem:
    def __init__(self, event_bus):
        self.event_bus = event_bus

    def start_span(self, trace_id: str, operation: str, parent_span: str | None = None) -> TraceContext:
        ctx = TraceContext(trace_id=trace_id, parent_span_id=parent_span)
        self.event_bus.publish("EVT_TRACE_START", {
            "trace_id": trace_id, "span_id": ctx.span_id,
            "parent_span_id": parent_span, "operation": operation
        })
        return ctx

    def end_span(self, ctx: TraceContext, status: str = "ok"):
        self.event_bus.publish("EVT_TRACE_END", {
            "trace_id": ctx.trace_id, "span_id": ctx.span_id, "status": status
        })
```

**Artifact:** `src/core/observability/tracing.py`

---

### TASK 1.15 — Execution Replay System

**Location:** `src/core/observability/event_bus.py` (extend)
**Depends on:** TASK 1.14
**Purpose:** Persist all events to `data/audit.db` and provide `replay_trace(trace_id)` for debugging.

#### Subtask 1.15.1 — Extend `EventBus` with persistence

Events stored in `audit.db` `events` table: `(trace_id, span_id, event_type, timestamp, payload_json)`.

#### Subtask 1.15.2 — Implement `replay_trace(trace_id)`

Returns ordered list of all events for a trace, enabling full execution replay.

**Artifact:** Updated `src/core/observability/event_bus.py`

---

### TASK 1.16 — EventBus Operational Contract

**Location:** `src/core/observability/event_bus.py`
**Depends on:** TASK 1.15 (replay system)
**Purpose:** EventBus is the backbone for SLAEvents, CapabilityViolationEvents, cancellation signals, and state transitions. Without a contract defining delivery semantics, ordering guarantees, and mandatory event envelope, events silently drop or arrive out of order — making debugging impossible and SLA enforcement unreliable.

#### Subtask 1.16.1 — Define `EventEnvelope` (mandatory wrapper for ALL events)

```python
# src/core/observability/event_bus.py — add to existing module

import uuid as _uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone

@dataclass
class EventEnvelope:
    """Every event published on EventBus MUST be wrapped in this envelope."""
    event_id:   str = field(default_factory=lambda: str(_uuid.uuid4())[:12])
    event_type: str = ""
    source:     str = ""          # e.g. "state_manager", "sla_enforcer"
    trace_id:   str = ""          # propagated from InputPacket
    timestamp:  str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    payload:    dict = field(default_factory=dict)
    sequence:   int = 0           # monotonic counter per-trace_id
```

**Rule:** `EventBus.publish()` MUST accept either a raw dict (legacy, wrapped internally) or an `EventEnvelope`. Subscribers always receive an `EventEnvelope`.

#### Subtask 1.16.2 — Enforce delivery + ordering guarantees

```python
class EventBus:
    """
    Delivery contract:
    - at-least-once:  failed subscriber callbacks are retried once
    - per-trace ordering: events with the same trace_id are delivered
      in sequence order (sequence field monotonically increasing)
    - isolation:      subscriber exception CANNOT affect other subscribers
    - persistence:    all events written to audit.db (existing TASK 1.15)
    """

    _RETRY_ON_FAILURE: bool = True   # retry subscriber once on exception
    _MAX_QUEUE_SIZE: int = 10_000    # drop oldest if exceeded (emit EVT_BUS_OVERFLOW)

    def publish(self, event_type: str, payload: dict,
                source: str = "", trace_id: str = "") -> EventEnvelope:
        env = EventEnvelope(
            event_type=event_type,
            source=source,
            trace_id=trace_id,
            payload=payload,
            sequence=self._next_sequence(trace_id),
        )
        # 1. persist to audit.db (existing)
        self._persist(env)
        # 2. deliver to subscribers with isolation
        for handler in self._subscribers.get(event_type, []):
            self._deliver(handler, env)
        return env

    def _deliver(self, handler, env: EventEnvelope) -> None:
        try:
            handler(env)
        except Exception as exc:
            self._log_error(f"Subscriber {handler} failed: {exc}")
            if self._RETRY_ON_FAILURE:
                try:
                    handler(env)          # one retry
                except Exception:
                    pass                  # swallow — isolation preserved

    def _next_sequence(self, trace_id: str) -> int:
        self._seq_counters[trace_id] = self._seq_counters.get(trace_id, 0) + 1
        return self._seq_counters[trace_id]
```

#### Subtask 1.16.3 — Define mandatory system-wide event types

```python
# src/core/observability/event_bus.py — canonical event type constants

# State machine
EVT_STATE_TRANSITION       = "EVT_STATE_TRANSITION"
EVT_INVALID_TRANSITION     = "EVT_INVALID_TRANSITION"
EVT_FORBIDDEN_LOOP         = "EVT_FORBIDDEN_LOOP"
EVT_TRANSITION_LIMIT       = "EVT_TRANSITION_LIMIT"

# Execution
EVT_TOOL_EXECUTED          = "EVT_TOOL_EXECUTED"
EVT_TOOL_FAILED            = "EVT_TOOL_FAILED"
EVT_TURN_COMPLETE          = "EVT_TURN_COMPLETE"
EVT_WAITING_CONFIRMATION   = "EVT_WAITING_CONFIRMATION"

# Safety / sandbox
EVT_SAFETY_BLOCK           = "EVT_SAFETY_BLOCK"
EVT_CAPABILITY_VIOLATION   = "EVT_CAPABILITY_VIOLATION"

# Performance / SLA
EVT_SLA_BREACH             = "EVT_SLA_BREACH"
EVT_DEGRADATION            = "EVT_DEGRADATION"
EVT_PROGRESS               = "EVT_PROGRESS"
EVT_TASK_COMPLETE          = "EVT_TASK_COMPLETE"

# Observability
EVT_TRACE_START            = "EVT_TRACE_START"
EVT_TRACE_END              = "EVT_TRACE_END"
EVT_BUS_OVERFLOW           = "EVT_BUS_OVERFLOW"
EVT_SYSTEM_UPDATE          = "EVT_SYSTEM_UPDATE"
EVT_THRESHOLD_ALERT        = "EVT_THRESHOLD_ALERT"
```

**Rule:** No string literals for event types anywhere in `src/`. Import constants from `event_bus.py`.

#### Subtask 1.16.4 — Test coverage (4 tests)

Add to `tests/test_observability.py`:

```python
def test_event_envelope_has_required_fields():
    from src.core.observability.event_bus import EventBus, EVT_TOOL_EXECUTED
    bus = EventBus()
    received = []
    bus.subscribe(EVT_TOOL_EXECUTED, received.append)
    env = bus.publish(EVT_TOOL_EXECUTED, {"tool": "open_app"}, source="test", trace_id="t1")
    assert env.event_id and env.timestamp and env.sequence == 1

def test_subscriber_exception_does_not_affect_others():
    from src.core.observability.event_bus import EventBus, EVT_TOOL_EXECUTED
    bus = EventBus()
    good_results = []
    bus.subscribe(EVT_TOOL_EXECUTED, lambda e: (_ for _ in ()).throw(RuntimeError("boom")))
    bus.subscribe(EVT_TOOL_EXECUTED, good_results.append)
    bus.publish(EVT_TOOL_EXECUTED, {})
    assert len(good_results) == 1   # second subscriber still received

def test_per_trace_sequence_monotonic():
    from src.core.observability.event_bus import EventBus, EVT_TRACE_START
    bus = EventBus()
    seqs = []
    bus.subscribe(EVT_TRACE_START, lambda e: seqs.append(e.sequence))
    for _ in range(5):
        bus.publish(EVT_TRACE_START, {}, trace_id="trace_abc")
    assert seqs == [1, 2, 3, 4, 5]

def test_all_event_type_constants_are_strings():
    import src.core.observability.event_bus as eb
    constants = [v for k, v in vars(eb).items() if k.startswith("EVT_")]
    assert all(isinstance(c, str) for c in constants)
    assert len(constants) >= 18   # enforce completeness
```

**Artifacts:** Updated `src/core/observability/event_bus.py`, `tests/test_observability.py`

**Definition of Done:**
- [ ] `EventEnvelope` dataclass with `event_id`, `source`, `trace_id`, `sequence`, `timestamp`
- [ ] `publish()` always wraps in `EventEnvelope`, persists, isolates subscribers
- [ ] At-least-once retry on subscriber failure
- [ ] All 22 `EVT_*` constants defined; no string literals in `src/`
- [ ] All 4 new tests pass

---

## Phase 2 — Execution Contract

```yaml
phase_id: 2
priority: "P0"
status: "not_started"
total_tasks: 10
blocker: "Phase 1 complete"
next_action: "TASK 2.0"
last_updated: "2026-05-03"
migration_note: >
  Phases 3 and 4 used stub contracts from Phase 0. TASK 2.8 migrates those
  files to formal Pydantic models. This migration must complete before Phase 5.
```

### Theoretical Foundation

A distributed system's correctness depends entirely on contracts between its components. Without formal contracts, each layer makes implicit assumptions about incoming data shapes — leading to silent type errors, partial failures that propagate, and untestable boundaries. Pydantic v2 validates on instantiation, generates clear error messages, supports cross-field validation, and integrates with JSON schema generation. The contracts defined here are load-bearing types — the single source of truth for every message crossing a layer boundary in JARVIS.

---

### TASK 2.0 — `ValidationResult` and `SchemaValidator` Stub

**Location:** `src/capabilities/validator.py`
**Depends on:** Phase 1 complete
**Purpose:** `SchemaValidator` is referenced by `CapabilityExecutor` (Phase 8 Gate 2) and `PermissionLayer` (Phase 6 Gate 3). It must exist as an importable stub so those phases don't break during development. The stub always returns `valid=True`; it is replaced with YAML-driven validation in TASK 6.6.

#### Subtask 2.0.1 — Define `ValidationResult` dataclass

```python
# src/capabilities/validator.py
from dataclasses import dataclass, field

@dataclass
class ValidationResult:
    valid: bool
    errors: list[str] = field(default_factory=list)

    def first_error(self) -> str | None:
        return self.errors[0] if self.errors else None

    def all_errors(self) -> str:
        return "; ".join(self.errors) if self.errors else ""
```

#### Subtask 2.0.2 — Define `SchemaValidator` stub

```python
class SchemaValidator:
    def validate(self, capability_name: str, args: dict) -> ValidationResult:
        """Stub — always valid. Full implementation in TASK 6.6."""
        return ValidationResult(valid=True)
```

**Validation:**

```bash
python -c "
from src.capabilities.validator import SchemaValidator, ValidationResult
r = SchemaValidator().validate('open_app', {'name': 'notepad'})
assert r.valid
vr = ValidationResult(valid=False, errors=['name required', 'type invalid'])
assert vr.first_error() == 'name required'
assert 'type invalid' in vr.all_errors()
print('TASK 2.0 OK')
"
```

**Artifact:** `src/capabilities/validator.py`

---

### TASK 2.1 — `InputPacket` Contract

**Location:** `src/core/context/bundle.py`
**Depends on:** TASK 2.0, `src/memory/user_profile.py`
**Purpose:** Canonical container flowing through the entire runtime loop. Validated Pydantic model ensures malformed inputs are rejected at `ContextAssembler` entry, not discovered deep in the pipeline. `trace_id` is auto-generated as UUIDv4. `user_message` is stripped and whitespace-only messages are rejected.

#### Subtask 2.1.1 — Create and define `InputPacket`

```python
# src/core/context/bundle.py
import uuid
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, field_validator
from src.memory.user_profile import UserProfile

class InputPacket(BaseModel):
    user_message: str
    session_id: str
    attachments: list[dict] = Field(default_factory=list)
    memory_snippets: list[dict] = Field(default_factory=list)
    recent_history: list[dict] = Field(default_factory=list)
    user_profile: UserProfile
    tool_results: list[dict] = Field(default_factory=list)
    turn_number: int = 0
    trace_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator('user_message')
    @classmethod
    def message_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("user_message cannot be empty or whitespace-only")
        return v.strip()

    @field_validator('session_id')
    @classmethod
    def session_id_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("session_id cannot be empty")
        return v
```

**Validation:**

```bash
python -c "
from src.core.context.bundle import InputPacket
from src.memory.user_profile import UserProfile
p = InputPacket(user_message='  hello  ', session_id='s1', user_profile=UserProfile(user_id='u1'))
assert p.user_message == 'hello'
assert len(p.trace_id) == 36
for bad in ['', '   ', '\t\n']:
    try: InputPacket(user_message=bad, session_id='s1', user_profile=UserProfile(user_id='u1')); assert False
    except Exception: pass
print('TASK 2.1 OK')
"
```

**Artifact:** `src/core/context/bundle.py`

---

### TASK 2.2 — `DecisionOutput` Contract

**Location:** `src/core/decision/output.py`
**Depends on:** TASK 2.0
**Purpose:** Output of the decision pipeline and input to every execution path. Cross-field validation is critical: `requires_tools=True` with no `tool_name` is structurally incoherent and must be rejected at the contract boundary, not propagated silently.

#### Subtask 2.2.1 — Define all enums

```python
# src/core/decision/output.py
from enum import Enum
from pydantic import BaseModel, Field, model_validator

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

#### Subtask 2.2.2 — Define `DecisionOutput` with cross-field validation

```python
class DecisionOutput(BaseModel):
    intent: Intent
    complexity: Complexity
    mode: ExecutionMode
    model: str
    requires_tools: bool
    requires_planning: bool = False
    tool_name: str | None = None
    tool_args: dict = Field(default_factory=dict)
    confidence: float = Field(ge=0.0, le=1.0)
    risk_level: RiskLevel
    decision_source: DecisionSource
    score_breakdown: dict = Field(default_factory=dict)
    candidate_list: list[dict] = Field(default_factory=list)

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
d = DecisionOutput(intent=Intent.chat, complexity=Complexity.low, mode=ExecutionMode.fast,
    model='gemma3:4b', requires_tools=False, confidence=0.9,
    risk_level=RiskLevel.low, decision_source=DecisionSource.fast_path)
assert d.intent == Intent.chat
for bad in [{'confidence':1.5}, {'requires_tools':True,'tool_name':None},
            {'decision_source':DecisionSource.model,'score_breakdown':{},'candidate_list':[]}]:
    try: DecisionOutput(**{**d.model_dump(), **bad}); assert False
    except Exception: pass
print('TASK 2.2 OK')
"
```

**Artifact:** `src/core/decision/output.py`

---

### TASK 2.3 — `LLMOutput` Contract

**Location:** `src/core/runtime/llm_output.py`
**Depends on:** TASK 2.0
**Purpose:** Normalises raw LLM text into one of two typed responses: `answer` (rendered to user) or `tool_call` (routed to CapabilityExecutor). Without this contract the executor must guess — leading to brittle string matching.

#### Subtask 2.3.1 — Define `LLMOutputType` and `LLMOutput`

```python
# src/core/runtime/llm_output.py
from enum import Enum
from pydantic import BaseModel, model_validator

class LLMOutputType(str, Enum):
    answer = "answer"
    tool_call = "tool_call"

class LLMOutput(BaseModel):
    type: LLMOutputType
    content: str | None = None
    tool: str | None = None
    args: dict = Field(default_factory=dict)
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
a = LLMOutput(type=LLMOutputType.answer, content='42')
t = LLMOutput(type=LLMOutputType.tool_call, tool='open_app', args={'name':'notepad'})
for bad_type, kw in [(LLMOutputType.answer,{}),(LLMOutputType.tool_call,{})]:
    try: LLMOutput(type=bad_type, **kw); assert False
    except Exception: pass
print('TASK 2.3 OK')
"
```

**Artifact:** `src/core/runtime/llm_output.py`

---

### TASK 2.4 — `ToolResult` Contract

**Location:** `src/capabilities/result.py`
**Depends on:** TASK 2.0
**Purpose:** Universal return type for all 13 capability executions. Factory methods `failure()` and `success_result()` ensure consistent construction and prevent field omissions.

#### Subtask 2.4.1 — Define `ToolResult` with factories

```python
# src/capabilities/result.py
from pydantic import BaseModel

class ToolResult(BaseModel):
    tool: str
    success: bool
    data: dict = Field(default_factory=dict)
    error: str = ""
    duration_ms: float = 0.0
    dry_run: bool = False
    risk_level: str = "low"
    turn_id: int = 0

    @classmethod
    def failure(cls, tool: str, error: str, duration_ms: float = 0.0) -> 'ToolResult':
        return cls(tool=tool, success=False, error=error, duration_ms=duration_ms)

    @classmethod
    def success_result(cls, tool: str, data: dict,
                       duration_ms: float = 0.0, risk_level: str = "low") -> 'ToolResult':
        return cls(tool=tool, success=True, data=data,
                   duration_ms=duration_ms, risk_level=risk_level)
```

**Validation:**

```bash
python -c "
from src.capabilities.result import ToolResult
r = ToolResult(tool='open_app', success=True, data={'pid':1234})
assert r.success
f = ToolResult.failure('open_app', 'not found', duration_ms=5.2)
assert not f.success and f.error == 'not found'
print('TASK 2.4 OK')
"
```

**Artifact:** `src/capabilities/result.py`

---

### TASK 2.5 — `FinalResponse` Contract

**Location:** `src/core/runtime/final_response.py`
**Depends on:** TASK 2.2 (DecisionSource), TASK 2.4 (ToolResult)
**Purpose:** Single output type of `run_turn()`. All interfaces (CLI, Web UI, Telegram) consume a `FinalResponse`. The `error_response()` factory guarantees a valid response even under total failure.

#### Subtask 2.5.1 — Define `FinalResponse` with error factory

```python
# src/core/runtime/final_response.py
from pydantic import BaseModel, Field
from src.core.decision.output import DecisionSource
from src.capabilities.result import ToolResult

class FinalResponse(BaseModel):
    text: str
    session_id: str
    model: str
    mode: str
    quality: float = Field(ge=0.0, le=1.0)
    decision_source: DecisionSource
    degraded: bool = False
    turn_id: int
    tool_results: list[ToolResult] = Field(default_factory=list)
    duration_ms: float = 0.0
    trace_id: str = ""

    @classmethod
    def error_response(cls, session_id: str, error_text: str, turn_id: int) -> 'FinalResponse':
        return cls(text=error_text, session_id=session_id, model="none", mode="error",
                   quality=0.0, decision_source=DecisionSource.fast_path,
                   degraded=True, turn_id=turn_id)
```

**Validation:**

```bash
python -c "
from src.core.runtime.final_response import FinalResponse
from src.core.decision.output import DecisionSource
r = FinalResponse(text='hi', session_id='s1', model='gemma3:4b', mode='fast',
    quality=0.9, decision_source=DecisionSource.fast_path, turn_id=1)
assert not r.degraded
e = FinalResponse.error_response('s1', 'Model unavailable.', turn_id=2)
assert e.degraded and e.quality == 0.0
try: FinalResponse(text='hi', session_id='s1', model='m', mode='f', quality=1.5,
    decision_source=DecisionSource.fast_path, turn_id=1); assert False
except Exception: pass
print('TASK 2.5 OK')
"
```

**Artifact:** `src/core/runtime/final_response.py`

---

### TASK 2.6 — `ModelScore` Contract

**Location:** `src/core/decision/model_score.py`
**Depends on:** TASK 2.0
**Purpose:** Encodes multi-factor weighted scoring result for one model. `factor_scores` must contain exactly the five keys from `config/runtime/models.yaml` — a structural contract that catches misconfiguration at score-evaluation time.

#### Subtask 2.6.1 — Define `ModelScore`

```python
# src/core/decision/model_score.py
from pydantic import BaseModel, Field, field_validator

class ModelScore(BaseModel):
    model: str
    score: float = Field(ge=0.0, le=1.0)
    factor_scores: dict[str, float]
    vram_available_mb: int = 0
    is_available: bool = True

    REQUIRED_FACTORS: frozenset = frozenset({
        'fit_complexity', 'fit_mode', 'cost_penalty', 'quality_need', 'memory_bias'
    })

    @field_validator('factor_scores')
    @classmethod
    def validate_factor_keys(cls, v: dict) -> dict:
        missing = cls.REQUIRED_FACTORS - v.keys()
        if missing:
            raise ValueError(f"factor_scores missing required keys: {sorted(missing)}")
        return v
```

**Validation:**

```bash
python -c "
from src.core.decision.model_score import ModelScore
valid = {'fit_complexity':0.8,'fit_mode':0.6,'cost_penalty':0.7,'quality_need':0.5,'memory_bias':0.5}
ms = ModelScore(model='gemma3:4b', score=0.75, factor_scores=valid)
assert ms.score == 0.75
try: ModelScore(model='m', score=0.5, factor_scores={'fit_complexity':0.8}); assert False
except Exception as e: assert 'missing required keys' in str(e)
print('TASK 2.6 OK')
"
```

**Artifact:** `src/core/decision/model_score.py`

---

### TASK 2.7 — `EvaluationResult` Contract

**Location:** `src/core/runtime/evaluation_result.py`
**Depends on:** TASK 2.0
**Purpose:** Output of the heuristic quality evaluator. Controls whether the runtime loop retries. Three guaranteed fields: `should_retry`, `quality_score`, `issues`.

#### Subtask 2.7.1 — Define `EvaluationResult`

```python
# src/core/runtime/evaluation_result.py
from pydantic import BaseModel, Field

class EvaluationResult(BaseModel):
    should_retry: bool
    quality_score: float = Field(ge=0.0, le=1.0)
    issues: list[str] = Field(default_factory=list)
    retry_reason: str = ""
```

**Validation:**

```bash
python -c "
from src.core.runtime.evaluation_result import EvaluationResult
ok = EvaluationResult(should_retry=False, quality_score=0.85)
assert not ok.should_retry
retry = EvaluationResult(should_retry=True, quality_score=0.3, issues=['truncated'])
assert retry.should_retry
try: EvaluationResult(should_retry=False, quality_score=1.5); assert False
except Exception: pass
print('TASK 2.7 OK')
"
```

**Artifact:** `src/core/runtime/evaluation_result.py`

---

### TASK 2.8 — Migrate Phase 3 and Phase 4 to Formal Contracts

**Location:** `src/models/`, `src/core/runtime/`
**Depends on:** TASKS 2.1–2.7 complete
**Purpose:** Phases 3 and 4 were built on Phase 0 stub contracts. Now that formal Pydantic models exist, all Phase 3 and 4 code that uses plain dicts at layer boundaries must be updated. This is mandatory before Phase 5 begins.

#### Subtask 2.8.1 — Audit and fix Phase 3 files

Scan for plain dict usage at boundary points in:

- `src/models/manager.py` — verify return types use formal contracts
- `src/models/llm/engine.py` — verify `chat_with_model()` return aligns with `LLMOutput`
- `src/models/availability.py` — verify model list structure

#### Subtask 2.8.2 — Audit and fix Phase 4 files

Scan for plain dict usage at boundary points in:

- `src/core/runtime/loop.py` — verify `run_turn()` returns `FinalResponse`
- `src/core/runtime/executor.py` — verify `execute()` returns `LLMOutput`
- `src/core/context/assembler.py` — verify returns `InputPacket`

#### Subtask 2.8.3 — Run regression tests

```bash
pytest tests/test_state_machine.py tests/test_contracts.py -v
# All must pass after migration
```

**Artifacts:** Updated Phase 3 and Phase 4 files

---

### TASK 2.9 — Contract Test Suite (22 tests)

**Location:** `tests/test_contracts.py`
**Depends on:** TASKS 2.0–2.8 complete
**Purpose:** These 22 tests are the contract specification in executable form. When all pass, the system has a machine-verified data foundation.

```python
# tests/test_contracts.py
import pytest
from src.memory.user_profile import UserProfile
from src.core.context.bundle import InputPacket
from src.core.decision.output import (DecisionOutput, Intent, Complexity,
    ExecutionMode, RiskLevel, DecisionSource)
from src.core.runtime.llm_output import LLMOutput, LLMOutputType
from src.capabilities.result import ToolResult
from src.core.runtime.final_response import FinalResponse
from src.core.decision.model_score import ModelScore
from src.core.runtime.evaluation_result import EvaluationResult
from src.capabilities.validator import ValidationResult

PROFILE = UserProfile(user_id="test_u1")
VALID_KWARGS = dict(intent=Intent.chat, complexity=Complexity.low, mode=ExecutionMode.fast,
    model='gemma3:4b', requires_tools=False, confidence=0.9,
    risk_level=RiskLevel.low, decision_source=DecisionSource.fast_path)
VALID_FACTORS = {'fit_complexity':0.8,'fit_mode':0.6,'cost_penalty':0.7,
                 'quality_need':0.5,'memory_bias':0.5}

# InputPacket (6 tests)
def test_input_packet_valid():
    p = InputPacket(user_message="hello", session_id="s1", user_profile=PROFILE)
    assert p.user_message == "hello"

def test_input_packet_trace_id_is_uuid():
    p = InputPacket(user_message="hi", session_id="s1", user_profile=PROFILE)
    assert len(p.trace_id) == 36 and p.trace_id.count('-') == 4

def test_input_packet_message_stripped():
    p = InputPacket(user_message="  hi  ", session_id="s1", user_profile=PROFILE)
    assert p.user_message == "hi"

def test_input_packet_rejects_empty_message():
    with pytest.raises(Exception): InputPacket(user_message="", session_id="s1", user_profile=PROFILE)

def test_input_packet_rejects_whitespace_message():
    with pytest.raises(Exception): InputPacket(user_message="   ", session_id="s1", user_profile=PROFILE)

def test_input_packet_rejects_empty_session():
    with pytest.raises(Exception): InputPacket(user_message="hi", session_id="", user_profile=PROFILE)

# DecisionOutput (6 tests)
def test_decision_output_valid_chat():
    d = DecisionOutput(**VALID_KWARGS)
    assert d.intent == Intent.chat

def test_decision_output_valid_tool_use():
    d = DecisionOutput(**{**VALID_KWARGS,'intent':Intent.tool_use,'requires_tools':True,
                          'tool_name':'open_app','tool_args':{'name':'notepad'}})
    assert d.tool_name == 'open_app'

def test_decision_output_rejects_confidence_over_1():
    with pytest.raises(Exception): DecisionOutput(**{**VALID_KWARGS,'confidence':1.5})

def test_decision_output_rejects_tools_without_tool_name():
    with pytest.raises(Exception):
        DecisionOutput(**{**VALID_KWARGS,'requires_tools':True,'tool_name':None})

def test_decision_output_rejects_model_source_empty_breakdown():
    with pytest.raises(Exception):
        DecisionOutput(**{**VALID_KWARGS,'decision_source':DecisionSource.model,
                         'score_breakdown':{},'candidate_list':[]})

def test_decision_output_model_source_valid():
    d = DecisionOutput(**{**VALID_KWARGS,'decision_source':DecisionSource.model,
        'score_breakdown':{'fit':0.8},'candidate_list':[{'model':'gemma3:4b'}]})
    assert d.decision_source == DecisionSource.model

# LLMOutput (4 tests)
def test_llm_output_valid_answer():
    o = LLMOutput(type=LLMOutputType.answer, content="42")
    assert o.content == "42"

def test_llm_output_valid_tool_call():
    o = LLMOutput(type=LLMOutputType.tool_call, tool='open_app', args={'name':'notepad'})
    assert o.tool == 'open_app'

def test_llm_output_rejects_answer_without_content():
    with pytest.raises(Exception): LLMOutput(type=LLMOutputType.answer)

def test_llm_output_rejects_tool_call_without_tool():
    with pytest.raises(Exception): LLMOutput(type=LLMOutputType.tool_call)

# ToolResult (2 tests)
def test_tool_result_valid():
    r = ToolResult(tool='open_app', success=True, data={'pid':1234})
    assert r.success

def test_tool_result_failure_factory():
    f = ToolResult.failure('open_app', 'not found', duration_ms=3.5)
    assert not f.success and f.error == 'not found' and f.duration_ms == 3.5

# FinalResponse (2 tests)
def test_final_response_valid():
    r = FinalResponse(text='hi', session_id='s1', model='gemma3:4b', mode='fast',
        quality=0.9, decision_source=DecisionSource.fast_path, turn_id=1)
    assert r.text == 'hi'

def test_final_response_rejects_quality_over_1():
    with pytest.raises(Exception):
        FinalResponse(text='hi', session_id='s1', model='m', mode='f', quality=1.5,
                      decision_source=DecisionSource.fast_path, turn_id=1)

# ModelScore (2 tests)
def test_model_score_valid():
    ms = ModelScore(model='gemma3:4b', score=0.75, factor_scores=VALID_FACTORS)
    assert ms.score == 0.75

def test_model_score_rejects_missing_factor_key():
    with pytest.raises(Exception):
        ModelScore(model='m', score=0.5, factor_scores={'fit_complexity':0.8})

# ValidationResult (2 tests)
def test_validation_result_first_error_none_when_valid():
    vr = ValidationResult(valid=True)
    assert vr.first_error() is None

def test_validation_result_first_error_returns_first():
    vr = ValidationResult(valid=False, errors=['err1', 'err2'])
    assert vr.first_error() == 'err1'
```

**Run:**

```bash
pytest tests/test_contracts.py -v
# Expected: 22 passed, 0 failed
```

**Artifact:** `tests/test_contracts.py`

---

### TASK 2.10 — Unified SystemError + Error Flow

**Location:** `src/core/exceptions.py`
**Depends on:** TASK 2.0
**Purpose:** Unified error class with type, source_layer, severity, recoverable. All errors route to `ERROR` state via `StateManager`.

#### Subtask 2.10.1 — Define `SystemError`

```python
# src/core/exceptions.py
class SystemError(Exception):
    def __init__(self, type: str, source_layer: str, message: str,
                 severity: str = "medium", recoverable: bool = True):
        self.type = type
        self.source_layer = source_layer
        self.message = message
        self.severity = severity
        self.recoverable = recoverable
        super().__init__(f"[{source_layer}] {type}: {message}")
```

#### Subtask 2.10.2 — Enforce global error flow

All layers raise `SystemError` → Runtime catches → `StateManager.transition_to(ERROR)` → `DegradationHandler` generates `FinalResponse.error_response()`.

**Validation:**

```bash
python -c "
from src.core.exceptions import SystemError
e = SystemError(type='validation', source_layer='capabilities', message='invalid args')
assert e.type == 'validation' and e.recoverable
print('TASK 2.10 OK')
"
```

**Artifact:** `src/core/exceptions.py`

---

### Definition of Done — Phase 2

- [ ] `pytest tests/test_contracts.py -v` → 22 passed, 0 failed
- [ ] All contract models importable from their canonical locations
- [ ] Phase 3 and Phase 4 files migrated to formal contracts (TASK 2.8)
- [ ] No plain-dict usage remaining at layer boundaries

---

## Phase 3 — Model Manager + VRAM

```yaml
phase_id: 3
priority: "P0"
status: "not_started"
total_tasks: 5
validation_status: "Phase 2 complete"
completion_note: >
  Completed ahead of Phase 2 via vertical slice extension.
  TASK 2.8 migrates this code to formal Phase 2 contracts.
```

**Artifacts:** `src/models/vram_monitor.py`, `src/models/manager.py`, `src/models/availability.py`, `src/models/llm/engine.py` (expanded with `chat_with_model()`)

**Key implementations:**

- `VRAMMonitor`: pynvml with 5s cache and RTX 3050 heuristic fallback (4096/6144 MB)
- `ModelManager` singleton: `threading.Lock`, load/unload/swap via Ollama `/api/generate` with `keep_alive`
- `ModelAvailability`: 30s cached `/api/tags` cross-referenced with VRAM headroom (requires +512 MB margin)
- `OllamaEngine.chat_with_model()`: timeout enforcement, `MetricsCollector` integration, `DeprecationWarning` on `chat()`

---

## Phase 4 — Runtime State Machine

```yaml
phase_id: 4
priority: "P0"
status: "not_started"
total_tasks: 8
validation_status: "Phase 3 "
completion_note: >
  Completed ahead of Phase 2 via vertical slice extension.
  TASK 2.8 migrates loop.py and executor.py to formal Phase 2 contracts.
  Phase 4 decision stub is replaced by Phase 5 decide().
  v3.2 hardening: SCHEDULING state strictly defined, dual-mode cancellation, SLA passive events.
```

**Artifacts:** `src/core/runtime/state.py`, `src/core/runtime/state_manager.py`, `src/core/runtime/limits.py`, `src/core/context/assembler.py`, `src/core/runtime/executor.py`, `src/core/runtime/evaluator.py`, `src/core/runtime/loop.py`, `tests/test_state_machine.py`

**Key implementations:**

- `RuntimeState` enum: IDLE, DECIDING, SCHEDULING, EXECUTING, STREAMING, EVALUATING, ERROR, RECOVERY, COMPLETED, CANCELLED, CLEANUP
- `ALLOWED_TRANSITIONS` frozenset map — all transitions defined and enforced (v3.2 corrected flow)
- `StateManager.transition_to()` with lock, history recording, EventBus publication
- `Limits` class loaded from `config.execution` with `check_limit(name, current) → bool` (current < max → True)
- `ContextAssembler.assemble()` returning `InputPacket` — cold start returns empty history, no error
- `Evaluator`: completeness (0.4) + relevance (0.4) + coherence (0.2) heuristic scoring
- `run_turn()`: full state machine loop with `_stub_decide()` (replaced in Phase 5) and `_stub_execute_tool()`
- Cancellation flow: ANY STATE → CANCELLED → CLEANUP → IDLE (dual-mode: soft→hard, termination confirmed)
- Error flow: ANY FAILURE → ERROR → RECOVERY → DECIDING | IDLE
- Retry authority: ONLY StateMachine may trigger retries
- SLA handling: SLAEnforcer emits SLAEvent → StateMachine decides cancel/fallback/retry/ignore
- Execution mode enforcement: StateMachine validates mode on every transition

**Transition map (v3.2 Hardened):**

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

ANY STATE            → CANCELLED → CLEANUP → IDLE   (dual-mode cancellation, termination confirmed)
ANY FAILURE          → ERROR → RECOVERY → ...       (error flow)

SLA EVENT HANDLING (not a state — in-band event during EXECUTING):
  SLAEnforcer emits SLAEvent → StateMachine decides:
  ├─ cancel  → EXECUTING → ERROR → RECOVERY → IDLE
  ├─ fallback→ EXECUTING → ERROR → RECOVERY → DECIDING (downgraded model)
  ├─ retry   → EXECUTING → EVALUATING → DECIDING (if retry budget > 0)
  └─ ignore  → EXECUTING continues (log event, no state change)
```

---

## Phase 5 — Decision System

```yaml
phase_id: 5
priority: "P1"
status: "not_started"
total_tasks: 8
blocker: "Phase 4 complete"
next_action: "TASK 5.1"
deterministic_mode: "bounded"
```

### Theoretical Foundation

Three design constraints govern the decision system: (1) **Deterministic mode (bounded)** — fast-path regex rules handle common patterns in <1ms WITHOUT invoking any model. This is the priority path. LLM classification is ONLY used as a fallback when fast-path misses. Identical inputs → identical outputs. (2) **Dynamic scoring** — when fast path misses, a 5-factor weighted scorer selects the best available model based on VRAM, task complexity, latency requirements, and historical performance. (3) **Graceful fallback** — if the LLM classifier fails to return valid JSON, the system falls back to a safe default rather than crashing. This phase replaces the Phase 4 `_stub_decide()` in `loop.py`.

**Determinism Enforcement:**

- `deterministic_mode: bounded` — fast-path rules are deterministic; LLM fallback is the ONLY non-deterministic element
- Same input → same fast-path output always
- LLM output cached by input hash for retry scenarios (future enhancement)

### TASK 5.1 — LLM Classifier with Robust JSON Parsing

**Location:** `src/core/decision/classifier.py`
**Depends on:** Phase 2 contracts, Phase 3 `OllamaEngine`
**Purpose:** LLMs frequently produce malformed JSON — extra commas, markdown fences, truncated output. `extract_json()` implements a progressive repair pipeline: strip fences → parse directly → find {…} substring → repair trailing commas → one retry. Only after all attempts fail does it return None and trigger the safe fallback.

#### Subtask 5.1.1 — Implement `extract_json()` with 4-step pipeline

````python
import re, json

def extract_json(text: str) -> dict | None:
    # Step 1: strip markdown fences
    cleaned = re.sub(r'```(?:json)?\s*|```\s*', '', text).strip()
    # Step 2: direct parse
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass
    # Step 3: extract first {...} substring
    start, end = cleaned.find('{'), cleaned.rfind('}')
    if start != -1 and end > start:
        try:
            return json.loads(cleaned[start:end+1])
        except json.JSONDecodeError:
            pass
    # Step 4: repair and retry
    repaired = _repair_json(cleaned)
    if repaired:
        try:
            return json.loads(repaired)
        except json.JSONDecodeError:
            pass
    return None

def _repair_json(text: str) -> str | None:
    r = re.sub(r',\s*([}\]])', r'\1', text)    # trailing commas
    r = re.sub(r"'([^']*)'", r'"\1"', r)       # single → double quotes
    try:
        json.loads(r)
        return r
    except json.JSONDecodeError:
        return None
````

#### Subtask 5.1.2 — Implement `Classifier` class

System prompt instructs model to return ONLY JSON with keys: `intent`, `complexity`, `tool_name`, `tool_args`, `confidence`. Two-attempt pipeline with 1s backoff. Falls back to `_safe_fallback()` returning `intent=chat, confidence=0.5, decision_source=fast_path` on double failure.

#### Subtask 5.1.3 — Map parsed JSON to `DecisionOutput`

Validate all enum values against their respective enum classes. Unknown values default to safe choices (e.g., unknown intent → `chat`).

**Artifact:** `src/core/decision/classifier.py`

---

### TASK 5.2 — Fast-Path Rules Engine

**Location:** `src/core/decision/fast_path.py`
**Depends on:** Phase 2 `DecisionOutput` enums
**Purpose:** Zero-latency decision for the most common user intents. Regex rules compiled at class instantiation. Returns in <1ms. All patterns are bilingual (English + Arabic). Fast-path outputs always set `decision_source=fast_path, confidence=0.95`.

#### Subtask 5.2.1 — Define 9 bilingual rules

All rules use `re.compile()` at class instantiation. Lambda factories call `_make_tool()` or `_make_chat()` helpers.

**Rules (in match order):**

| Pattern                                                                    | Language | Tool          | Args             |
| :------------------------------------------------------------------------- | :------- | :------------ | :--------------- |
| `^(open\|launch\|start\|run)\s+(.+)`                                       | EN       | `open_app`    | `name=group(1)`  |
| `^(افتح\|شغّل\|شغل\|ابدأ)\s+(.+)`                                          | AR       | `open_app`    | `name=group(1)`  |
| `^(search(\s+for)?\|find\|look\s+up)\s+(.+)`                               | EN       | `web_search`  | `query=group(3)` |
| `^(ابحث(\s+عن)?\|ابحث\s+في)\s+(.+)`                                        | AR       | `web_search`  | `query=group(3)` |
| `^(take\s+a?\s*screenshot\|screenshot\|capture\s+screen)`                  | EN       | `screenshot`  | `{}`             |
| `^(system\s+info\|cpu\s+usage\|what'?s?\s+my\s+(cpu\|ram\|gpu))`           | EN       | `system_info` | `info_type=all`  |
| `^(read\s+clipboard\|what'?s?\s+in.*clipboard\|paste)`                     | EN       | `clipboard`   | `action=read`    |
| `^(what\s+is\|what'?s\|who\s+is\|define\|explain\|tell\s+me\s+about)\s+.+` | EN       | —             | `_make_chat()`   |
| `^(ما\s+هو\|ما\s+هي\|من\s+هو\|اشرح\|عرّف)\s+.+`                            | AR       | —             | `_make_chat()`   |

> **Note:** The `\|` characters in the table above are markdown table escaping (`|` is a column separator). In actual Python source code, regex alternation uses unescaped `|`: `r"^(افتح|شغّل|شغل|ابدأ)\s+(.+)"`.

#### Subtask 5.2.2 — Implement `check()` method

Iterates rules list, returns `DecisionOutput` on first match. Returns `None` if no rule matches.

**Artifact:** `src/core/decision/fast_path.py`

---

### TASK 5.3 — Dynamic Model Scorer

**Location:** `src/core/decision/scorer.py`
**Depends on:** Phase 2 `ModelScore`, Phase 3 `VRAMMonitor` + `ModelAvailability`, Phase 1 `models.yaml`
**Purpose:** 5-factor weighted scoring with deterministic tie-breaking. Factor names MUST match `config/runtime/models.yaml` weight keys exactly. Same inputs always produce same ranking.

#### Subtask 5.3.1 — Load weights from `models.yaml` at instantiation

Weights validated by `load_config()` to sum to 1.0. Scorer reads them once and caches.

#### Subtask 5.3.2 — Implement `score()` for one model

| Factor           | Formula                                                                    |
| :--------------- | :------------------------------------------------------------------------- |
| `fit_complexity` | `1.0 - abs(REASONING_SCORES[reasoning_tier] - COMPLEXITY_MAP[complexity])` |
| `fit_mode`       | `1.0 - abs(LATENCY_SCORES[latency_tier] - MODE_LATENCY_MAP[mode])`         |
| `cost_penalty`   | `1.0 - (vram_required_mb / 6144)`                                          |
| `quality_need`   | `REASONING_SCORES[reasoning_tier]`                                         |
| `memory_bias`    | `clamp(memory_bias_input, 0.0, 1.0)`                                       |

`weighted_score = sum(weights[k] * factor_scores[k] for k in weights)`

Returns `ModelScore` with `is_available=False` and zero score if profile not found or VRAM insufficient.

#### Subtask 5.3.3 — Implement `rank_models()` with deterministic tie-break

Scores all profiles → filters to `is_available=True` → sorts by `(-score, -cost_penalty, model_name_alpha)`.

**Normalisation tables:**

```python
REASONING_SCORES = {"low": 0.3, "medium": 0.7, "high": 1.0}
LATENCY_SCORES   = {"fast": 1.0, "medium": 0.6, "slow": 0.3}
COMPLEXITY_MAP   = {"low": 0.3, "medium": 0.6, "high": 1.0}
MODE_LATENCY_MAP = {"fast": 1.0, "normal": 0.6, "deep": 0.3, "planning": 0.4, "research": 0.3}
MAX_VRAM_MB      = 6144
```

**Artifact:** `src/core/decision/scorer.py`

---

### TASK 5.4 — Risk Assessor

**Location:** `src/core/decision/risk.py`
**Depends on:** Phase 2 `DecisionOutput`, `RiskLevel`
**Purpose:** Inspects decided action arguments to escalate risk level beyond the tool's base risk. `file_ops` + `delete` escalates to `high`. Any path containing `..` escalates to `high`. Any path matching `blocked_paths` escalates to `high`. Returns highest of all computed levels.

#### Subtask 5.4.1 — Define risk tables

```python
TOOL_RISK = {
    "open_app":"medium","system_info":"low","clipboard":"low","notify":"low",
    "screenshot":"low","file_ops":"medium","code_exec":"high","web_search":"low",
    "browser":"medium","stt":"low","tts":"low","vision_analyze":"medium","image_gen":"low",
}
FILE_ACTION_RISK = {
    "delete":"high","write":"medium","move":"medium","copy":"medium","read":"low","list":"low",
}
```

#### Subtask 5.4.2 — Implement `assess()` with escalation logic

No tool → `RiskLevel.low`. Collect base risk + file action override + path traversal check + blocked path check. Return highest level using `RISK_RANK = {"low":0, "medium":1, "high":2}`.

For `vision_analyze` specifically: check `image_path` argument for path traversal (`..` → escalate to `high`). Resolve the path and compare against `blocked_paths` using `os.path.commonpath` — match → escalate to `high`.

**Artifact:** `src/core/decision/risk.py`

---

### TASK 5.5 — Unified `decide()` Function

**Location:** `src/core/decision/decision.py`
**Depends on:** TASKS 5.1–5.4, Phase 3 `VRAMMonitor`
**Purpose:** Single callable invoked during DECIDING state. Encapsulates the full pipeline: fast path → classifier → scorer → risk → validate. Never raises — `_safe_default()` is the unconditional fallback.

#### Subtask 5.5.1 — Implement 6-step `decide()` pipeline

1. FastPath check → if matched, fill model from scorer, assess risk, return immediately
2. Classifier call → partial DecisionOutput
3. Get VRAM → rank models → select best
4. Risk assessment on final decision
5. Construct DecisionOutput with `score_breakdown`, `candidate_list` (top 3), `decision_source=model`
6. DecisionEnforcer.validate() → if invalid, return `_safe_default()`

#### Subtask 5.5.2 — Wire into `loop.py`

Remove `_stub_decide()` from `src/core/runtime/loop.py`. Import and call `decide(input_packet)`.

**Artifact:** `src/core/decision/decision.py`, updated `src/core/runtime/loop.py`

---

### TASK 5.6 — Escalation Chain

**Location:** `src/core/runtime/escalation.py`
**Depends on:** TASK 5.5
**Purpose:** Intelligent retry with weight adjustment to avoid re-selecting the same failing model.

#### Subtask 5.6.1 — Implement `EscalationChain.retry(packet, attempt)`

| Attempt | Behaviour                                                                    |
| :------ | :--------------------------------------------------------------------------- |
| 1       | Standard `decide()`                                                          |
| 2       | `fit_complexity += 0.05`, `cost_penalty -= 0.05`, re-decide, restore weights |
| 3       | Force `tier_1` model from `models.yaml`                                      |
| 4+      | Force `tier_2` model (guaranteed available lightweight fallback)             |

**Artifact:** `src/core/runtime/escalation.py`

---

### TASK 5.7 — Decision System Tests (15 tests)

**Location:** `tests/test_decision.py`

Required test coverage:

1. Fast path EN: `"open notepad"` → `tool_use, open_app`
2. Fast path AR: `"افتح المفكرة"` → `tool_use, open_app`
3. Fast path: `"system info"` → `tool_use, system_info`
4. Fast path miss: `"tell me a joke"` → `None`
5. `extract_json` handles markdown fences
6. `extract_json` handles trailing comma
7. `extract_json` returns `None` for garbage input
8. `ModelScorer.score()` returns all 5 required factor keys
9. `ModelScorer.rank_models()` returns highest score first
10. `RiskAssessor` returns `high` for `code_exec`
11. `RiskAssessor` returns `high` for `file_ops` + `delete`
12. `decide("open notepad")` → `decision_source=fast_path`
13. `decide()` model-path returns non-empty `score_breakdown` and `candidate_list`
14. Escalation attempt 3 forces tier_1 model
15. Deterministic mode: fast-path returns same output for same input (bounded determinism)

```bash
pytest tests/test_decision.py -v
# Expected: 15 passed
```

**Artifact:** `tests/test_decision.py`

---

### TASK 5.8 — Deterministic Mode Enforcement

**Location:** `src/core/decision/fast_path.py` (extend)
**Depends on:** TASK 5.2
**Purpose:** Ensure fast-path rules produce identical outputs for identical inputs. Bypass LLM when fast-path matches — this is the deterministic (bounded) path.

#### Subtask 5.8.1 — Implement deterministic guarantee

- Fast-path rules are compiled once at class init (deterministic)
- No random choices, no timestamps, no external state in rule matching
- `decision_source=fast_path` explicitly marks deterministic path
- Log `deterministic=true` in `DecisionOutput` metadata (future: add field)

#### Subtask 5.8.2 — Add test for determinism

```python
def test_fast_path_deterministic():
    fp = FastPath()
    result1 = fp.check("open notepad")
    result2 = fp.check("open notepad")
    assert result1.tool_name == result2.tool_name
    assert result1.decision_source == DecisionSource.fast_path
```

**Artifact:** Updated `src/core/decision/fast_path.py`, `tests/test_decision.py`

---

### Definition of Done — Phase 5

- [ ] Fast path handles all 9 rules including Arabic bilingual patterns
- [ ] `extract_json` passes all repair scenarios, returns None on total failure
- [ ] `ModelScorer.rank_models()` always returns all 5 required factor keys
- [ ] `decide()` wired into `loop.py` replacing `_stub_decide()`
- [ ] Deterministic mode: fast-path always returns identical output for identical input
- [ ] `pytest tests/test_decision.py -v` → 15 passed

---

## Phase 6 — Sandbox + Safety (HARDENED)

```yaml
phase_id: 6
priority: "P0"
status: "not_started"
total_tasks: 9
blocker: "Phase 5 complete"
next_action: "TASK 6.1"
stabilization: "v3.2 hardened sandbox — system-level isolation"
```

**Enforcement Rules:**

- ALL capabilities MUST execute inside `Sandbox.execute()` — no direct Python execution
- `Sandbox` uses `ThreadPoolExecutor` with timeout wrapping
- Process/container isolation for code execution capabilities
- Resource limits: CPU quota, RAM cap, execution time limit
- File system restrictions: path validation via `Path.resolve()` + `os.path.commonpath()`
- **v3.2 HARDENING:** process isolation (separate PID), privilege drop (no admin/root), filesystem sandbox (allowlist paths), network policy (deny by default), syscall restrictions (where possible), dual-mode cancellation (SIGTERM → 2s grace → SIGKILL), process tree kill (parent + children)

**SLA Enforcement:**

- Global SLA targets: fast=100ms, medium=500ms, heavy=5000ms
- Runtime monitors execution time; on_timeout: cancel_task, fallback to simpler path, log_event
- `src/core/performance/sla_enforcer.py` monitors execution vs targets

---

### TASK 6.8 — Capability Isolation Layer

**Location:** `src/core/sandbox/sandbox.py`
**Purpose:** ALL capability executions route through sandbox. Direct calls are architecture violations.

```python
class Sandbox:
    def execute(self, capability, args: dict, timeout_s: float = 30.0) -> ToolResult:
        # ThreadPoolExecutor isolation
        # Timeout wrapping via concurrent.futures
        # Exception catching → ToolResult.failure()
        # Resource monitoring (optional future)
```

---

### TASK 6.9 — Resource Limits Enforcement

**Location:** `src/core/sandbox/sandbox.py`
**Purpose:** Enforce CPU, RAM, and time limits on capability executions.

- `max_cpu_percent: float` (default 50.0)
- `max_memory_mb: int` (default 512)
- `max_execution_time_s: float` (default 30.0)
- Violations → `ToolResult.failure("resource limit exceeded")`

**Artifact:** Updated `src/core/sandbox/sandbox.py`

### Theoretical Foundation

Three independent safety guarantees: (1) **Structural isolation** — capabilities run in `ThreadPoolExecutor(max_workers=1)` with enforced timeout. (2) **Permission gates** — three sequential gates check consistency, argument safety, and schema validity before any execution. (3) **Audit trail** — every gate outcome logged to SQLite regardless of execution outcome. Safety is enforced by code structure, not model instruction. A model cannot bypass safety through prompt injection.

### TASK 6.1 — Execution Sandbox

**Location:** `src/core/sandbox/sandbox.py`
**Depends on:** Phase 2 `ToolResult`, Phase 1 `EventBus`
**Purpose:** Prevents hanging capabilities from blocking the event loop. `ThreadPoolExecutor(max_workers=1)` with `future.result(timeout=timeout_s)` cancels overdue capabilities. Exception wrapping ensures `ToolResult.failure()` is always returned — the contract is never broken by a capability crash.

#### Subtask 6.1.1 — Implement `Sandbox.execute()`

```python
# src/core/sandbox/sandbox.py
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeout
from src.capabilities.result import ToolResult
from src.core.observability.event_bus import EventBus, EVT_TOOL_EXECUTED

class Sandbox:
    def execute(self, capability, args: dict, timeout_s: int) -> ToolResult:
        start = time.time()
        executor = ThreadPoolExecutor(max_workers=1)
        future = executor.submit(capability.execute, args)
        try:
            result = future.result(timeout=timeout_s)
            result = result.model_copy(
                update={"duration_ms": (time.time() - start) * 1000}
            )
            EventBus().publish(EVT_TOOL_EXECUTED,
                {"tool": capability.name, "success": result.success,
                 "duration_ms": result.duration_ms})
            return result
        except FuturesTimeout:
            executor.shutdown(wait=False)
            return ToolResult.failure(capability.name,
                f"execution timed out after {timeout_s}s",
                duration_ms=(time.time() - start) * 1000)
        except Exception as e:
            return ToolResult.failure(capability.name, str(e),
                duration_ms=(time.time() - start) * 1000)
        finally:
            executor.shutdown(wait=False)

    def dry_run(self, capability, args: dict) -> ToolResult:
        try:
            result = capability.dry_run(args)
            return result.model_copy(update={"dry_run": True})
        except Exception as e:
            return ToolResult.failure(capability.name, f"dry_run failed: {e}")
```

**Artifact:** `src/core/sandbox/sandbox.py`

---

### TASK 6.2 — Safety Classifier

**Location:** `src/core/safety/classifier.py`
**Depends on:** Phase 1 `load_config()`, Phase 2 `RiskLevel`
**Purpose:** Inspects capability arguments using structured logic — NOT regex on the user's raw message. Uses `os.path.commonpath()` for path checks (string prefix matching has known bypass vectors). Code pattern scanning uses exact substring matching.

#### Subtask 6.2.1 — Implement `SafetyClassifier.classify()`

Steps executed in order:

1. Load base risk from `capabilities.yaml`. Unknown capability → `high`
2. Path traversal: any string arg value containing `..` → `high`
3. Blocked path: `os.path.commonpath([resolved_arg, blocked_path]) == blocked_path` → `high`
4. Code safety: `code_exec` capability → scan code string for `__import__`, `subprocess`, `os.system`, `exec(`, `eval(`, `open('/etc`, `open('/proc` → `high`
5. Return base risk if no escalation triggered

**Artifact:** `src/core/safety/classifier.py`

---

### TASK 6.3 — Mode Enforcer

**Location:** `src/core/safety/mode_enforcer.py`
**Depends on:** Phase 2 `RiskLevel`, Phase 1 `EventBus`
**Purpose:** Translates `(risk_level, mode)` into `Permission` enum. Three-tier matrix. Override phrase in args provides explicit escape hatch for BALANCED+high (requires deliberate user intent in args, not chat).

#### Subtask 6.3.1 — Define `Permission` enum and permission matrix

```python
class Permission(str, Enum):
    allow = "allow"
    confirm = "confirm"
    block = "block"
```

Matrix:

| Mode         | Low     | Medium  | High                    |
| :----------- | :------ | :------ | :---------------------- |
| SAFE         | confirm | confirm | confirm                 |
| BALANCED     | allow   | confirm | block (unless override) |
| UNRESTRICTED | allow   | allow   | allow                   |

Publishes `EVT_SAFETY_BLOCK` when returning `block`.

**Artifact:** `src/core/safety/mode_enforcer.py`

---

### TASK 6.4 — Permission Layer (Three-Gate System)

**Location:** `src/core/safety/permission.py`
**Depends on:** TASKS 6.2, 6.3, TASK 2.0 `SchemaValidator`
**Purpose:** Single entry point for all pre-execution authorization. Returns `(Permission, reason_str)`. The CapabilityExecutor never needs to know which specific check failed.

#### Subtask 6.4.1 — Implement `PermissionLayer.check()`

```python
def check(self, tool_name: str, args: dict,
          decision: DecisionOutput, mode: str) -> tuple[Permission, str]:
    # Gate 1: tool_name must match decision.tool_name
    if tool_name != decision.tool_name:
        return Permission.block, f"tool mismatch: expected '{decision.tool_name}', got '{tool_name}'"
    # Gate 2: safety classification + mode enforcement
    risk = self._classifier.classify(tool_name, args)
    perm = self._enforcer.check_permission(tool_name, risk, mode, args)
    if perm == Permission.block:
        return Permission.block, f"permission denied: mode={mode}, risk={risk.value}"
    # Gate 3: schema validation
    validation = self._validator.validate(tool_name, args)
    if not validation.valid:
        return Permission.block, f"schema invalid: {validation.all_errors()}"
    return perm, ""
```

**Artifact:** `src/core/safety/permission.py`

---

### TASK 6.5 — Audit Logger

**Location:** `src/core/safety/audit.py`
**Depends on:** Phase 1 `load_config()` for `audit_db` path
**Purpose:** Append-only SQLite log of every permission check outcome. WAL mode for concurrent writes. Every blocked, confirmed, and allowed action is recorded with full gate results.

#### Subtask 6.5.1 — Implement `AuditLogger` with SQLite schema

Table: `audit_log(id, timestamp, session_id, turn_id, tool_name, args, gate1, gate2, gate3, final_decision, reason)`

Methods: `log_action(...)`, `get_audit_log(session_id, limit=50) → list[dict]`

**Artifact:** `src/core/safety/audit.py`

---

### TASK 6.6 — Schema Validator (Full Implementation)

**Location:** `src/capabilities/validator.py` (expand TASK 2.0 stub)
**Depends on:** Phase 1 `capabilities.yaml`
**Purpose:** Replaces the always-valid stub with YAML-driven validation. Validates field presence, type correctness, and enum membership against the manifest loaded at startup.

#### Subtask 6.6.1 — Load manifest and implement full `validate()`

```python
# Expanded SchemaValidator
class SchemaValidator:
    def __init__(self):
        with open("config/runtime/capabilities.yaml") as f:
            caps = yaml.safe_load(f).get("capabilities", [])
        self._schemas = {c["name"]: c.get("input_schema", {}) for c in caps}

    def validate(self, capability_name: str, args: dict) -> ValidationResult:
        if capability_name not in self._schemas:
            return ValidationResult(valid=False,
                errors=[f"unknown capability: '{capability_name}'"])
        schema = self._schemas[capability_name]
        errors = []
        for field_name, field_def in schema.items():
            if field_def.get("required", False) and field_name not in args:
                errors.append(f"field '{field_name}' is required")
                continue
            if field_name not in args:
                continue
            value = args[field_name]
            etype = field_def.get("type")
            if etype == "string" and not isinstance(value, str):
                errors.append(f"field '{field_name}' must be a string")
            elif etype == "integer" and not isinstance(value, int):
                errors.append(f"field '{field_name}' must be an integer")
            elif etype == "boolean" and not isinstance(value, bool):
                errors.append(f"field '{field_name}' must be a boolean")
            if field_def.get("enum") and value not in field_def["enum"]:
                errors.append(f"field '{field_name}' must be one of {field_def['enum']}")
        return ValidationResult(valid=not errors, errors=errors)
```

**Artifact:** `src/capabilities/validator.py`

---

### TASK 6.7 — Safety Tests (13 tests)

**Location:** `tests/test_safety.py`

Required tests:

1. SAFE mode + low risk → `confirm`
2. SAFE mode + high risk → `confirm`
3. BALANCED + low → `allow`
4. BALANCED + medium → `confirm`
5. BALANCED + high → `block`
6. BALANCED + high + override phrase → `confirm`
7. UNRESTRICTED + high → `allow`
8. Path `"../etc/shadow"` → `high`
9. Path `"/etc/passwd"` → `high`
10. `code_exec` with `subprocess` → `high`
11. Gate 1 fail (tool mismatch) → `block` with "mismatch" in reason
12. Gate 3 fail (missing required arg) → `block` with field name in reason
13. Audit log entry created after each permission check

```bash
pytest tests/test_safety.py -v
# Expected: 13 passed
```

**Artifact:** `tests/test_safety.py`

### Definition of Done — Phase 6

- [ ] Sandbox wraps all capabilities with `ThreadPoolExecutor` + timeout
- [ ] Three-gate permission enforced in order
- [ ] Audit log records every permission check
- [ ] `SchemaValidator` validates against `capabilities.yaml` manifest
- [ ] `pytest tests/test_safety.py -v` → 13 passed

---

## Phase 7 — Memory Engine

```yaml
phase_id: 7
priority: "P1"
status: "not_started"
total_tasks: 9
blocker: "Phase 6 complete"
next_action: "TASK 7.1"
```

### Theoretical Foundation

Memory is an active retrieval engine, not passive storage. Three relevance signals: keyword overlap (does this memory relate to the current query?), recency (how fresh?), interaction frequency (how often accessed?). SQLite WAL mode provides thread-safe concurrent reads without blocking the runtime. Corruption handling moves the bad DB aside and creates a fresh one — the system never crashes on DB corruption.

**Key additions for v3.0 compliance:**

- Relevance scoring with weighted formula (overlap + recency + interaction)
- TTL decay: `relevance_score *= 0.95` for snippets older than 24h
- Indexing system: inverted keyword → snippet_id index for O(1) lookup
- Concurrency model: global model lock in `ModelManager`, async execution strategy for capabilities (future), request queue (future)

### TASK 7.1 — Memory Database

**Location:** `src/memory/database.py`
**Purpose:** SQLite persistence with WAL mode, thread-local connection pooling, corruption recovery, and schema versioning.

#### Subtask 7.1.1 — Implement DB initialisation with WAL mode

```python
import sqlite3, threading
from pathlib import Path
_local = threading.local()
```

Thread-local connection: one connection per thread, created lazily on first `_get_conn()` call.

#### Subtask 7.1.2 — Define schema

```sql
CREATE TABLE IF NOT EXISTS turns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL, turn_number INTEGER,
    user_message TEXT, assistant_response TEXT,
    model TEXT, timestamp TEXT, trace_id TEXT
);
CREATE TABLE IF NOT EXISTS memory_snippets (
    id TEXT PRIMARY KEY, session_id TEXT, content TEXT, keywords TEXT,
    created_at TEXT, expires_at TEXT,
    interaction_count INTEGER DEFAULT 0, relevance_score REAL DEFAULT 1.0
);
CREATE TABLE IF NOT EXISTS keyword_index (
    keyword TEXT, snippet_id TEXT, PRIMARY KEY (keyword, snippet_id)
);
CREATE INDEX IF NOT EXISTS idx_turns_session ON turns(session_id);
CREATE INDEX IF NOT EXISTS idx_snippets_session ON memory_snippets(session_id);
```

#### Subtask 7.1.3 — Implement CRUD methods

- `store(session_id, turn_data)` — INSERT into turns
- `retrieve_recent(session_id, limit=5)` — ORDER BY id DESC (newest first)
- `store_snippet(snippet)` — INSERT OR REPLACE
- `search_snippets(keywords)` — via keyword_index → snippets join
- `_handle_corruption()` — rename to `.corrupted.{timestamp}`, create fresh
- `get_schema_version() / set_schema_version(v)` — via `PRAGMA user_version`

**Artifact:** `src/memory/database.py`

---

### TASK 7.2 — Memory Scorer

**Location:** `src/memory/scorer.py`
**Purpose:** Weighted relevance scoring for memory retrieval.

#### Subtask 7.2.1 — Implement scoring formula

```python
score = round(0.5 * overlap + 0.3 * recency + 0.2 * interactions, 4)
```

- `overlap`: `len(snippet_keywords ∩ query_words) / max(len(query_words), 1)`. Skip words ≤ 2 chars.
- `recency`: `max(0.0, 1.0 - age_hours / 168.0)` — decays to 0 over 7 days
- `interactions`: `min(interaction_count / 10.0, 1.0)` — capped at 10

**Artifact:** `src/memory/scorer.py`

---

### TASK 7.3 — TTL and Decay Manager

**Location:** `src/memory/ttl.py`
**Purpose:** Enforces time-based expiry and relevance decay.

#### Subtask 7.3.1 — Implement TTL operations

- `set_ttl(snippet_id, ttl_hours)` — UPDATE `expires_at`
- `get_expired_ids()` — SELECT where `expires_at < utcnow()`
- `apply_decay(factor=0.95)` — UPDATE `relevance_score *= factor` for snippets older than 24h
- `cleanup() → int` — DELETE expired, return count

**Artifact:** `src/memory/ttl.py`

---

### TASK 7.4 — Keyword Indexer

**Location:** `src/memory/indexer.py`
**Purpose:** Inverted index mapping keywords to snippet IDs for fast lookup.

#### Subtask 7.4.1 — Implement `KeywordIndexer`

- `index(snippet_id, keywords)` — INSERT OR IGNORE into keyword_index
- `lookup(keyword) → list[str]` — SELECT snippet_ids for keyword
- `remove(snippet_id)` — DELETE from keyword_index
- `rebuild_index()` — clear + re-index all snippets from DB

**Artifact:** `src/memory/indexer.py`

---

### TASK 7.5 — Context Retriever

**Location:** `src/memory/retriever.py`
**Purpose:** Keyword lookup → score → rank → return top-N. Cold start (empty DB) returns `[]` — not an error.

#### Subtask 7.5.1 — Implement `get_context()` pipeline

1. Extract keywords from query (skip words ≤ 2 chars)
2. Look up candidate snippet IDs via `KeywordIndexer`
3. Fetch and score each snippet via `MemoryScorer`
4. Sort descending by score, return top `limit`
5. Increment `interaction_count` for returned snippets

Wrap entire pipeline in `try/except` — returns `[]` on any failure.

**Artifact:** `src/memory/retriever.py`

---

### TASK 7.6 — Memory Tests (12 tests)

**Location:** `tests/test_memory.py`

Required tests:

1. `store` + `retrieve_recent` round-trip
2. `retrieve_recent` returns newest first
3. Cold start returns empty list (not error)
4. Scorer: relevant snippet scores higher than irrelevant
5. Scorer: score always in [0.0, 1.0]
6. `KeywordIndexer.index` → `lookup` returns correct IDs
7. `TTLManager.get_expired_ids` returns expired entries
8. `TTLManager.cleanup` removes expired, returns count
9. `ContextRetriever.get_context` returns sorted results
10. `ContextRetriever` cold start returns empty list
11. `MemoryScorer` relevance scoring with TTL decay: older snippets score lower
12. `KeywordIndexer.rebuild_index()` rebuilds from scratch

```bash
pytest tests/test_memory.py -v
# Expected: 12 passed
```

**Artifact:** `tests/test_memory.py`

---

### TASK 7.7 — Concurrency Model (Global Model Lock)

**Location:** `src/models/manager.py` (extend)
**Purpose:** Ensure only ONE model loaded at a time. `threading.Lock` prevents concurrent load/unload.

- `ModelManager` uses `threading.Lock` for all load/unload operations
- `ModelManager.load(name)` acquires lock, checks VRAM, loads, releases
- Prevents VRAM over-commit from concurrent requests

**Artifact:** Updated `src/models/manager.py`

---

### TASK 7.8 — Async Execution Strategy (Future Hook)

**Location:** `src/core/runtime/executor.py` (extend)
**Purpose:** Prepare for non-blocking capability execution. Phase 7 defines the interface; full async in Phase 11.

- Define `execute_async()` interface (returns `Future[ToolResult]`)
- Default sync implementation wraps in `ThreadPoolExecutor`
- Enables future async capability implementations

**Artifact:** Updated `src/core/runtime/executor.py`

---

### TASK 7.9 — Request Queue (Future Hook)

**Location:** `src/core/runtime/loop.py` (extend)
**Purpose:** Queue incoming requests when system is busy. Prevents overload.

- Define `RequestQueue` with `max_size` from config
- `enqueue(user_input, session_id)` → `turn_id`
- `process_next()` called by main loop when IDLE
- Phase 7 defines interface; full implementation in Phase 11

**Artifact:** Updated `src/core/runtime/loop.py`

---

### Definition of Done — Phase 7

- [ ] `MemoryDB` stores, retrieves, handles corruption with no crash
- [ ] `MemoryScorer` values always in [0.0, 1.0]
- [ ] `TTLManager.cleanup()` removes expired entries and returns count
- [ ] `ContextRetriever` returns empty list on cold start
- [ ] `pytest tests/test_memory.py -v` → 12 passed

---

## Phase 8 — Capability System (RESTRICTED)

```yaml
phase_id: 8
priority: "P1"
status: "not_started"
total_tasks: 12
blocker: "Phase 7 complete"
next_action: "TASK 8.1"
stabilization: "v3.2 — CapabilityRuntime internal-only, scope enforcement, runtime validator, streaming/batching restricted"
performance_targets:
  fast_tools: "<100ms"
  medium_tools: "<500ms"
  heavy_tools: "async + streaming (ONLY heavy tasks)"
  non_blocking: "default"
```

### Theoretical Foundation

Capabilities are intelligent execution modules with **bounded scope**:

- **Async execution** via `CapabilityRuntime` (INTERNAL ONLY — cannot be imported by interfaces/decision/services)
- **Batch processing** for multi-item operations (ONLY where needed)
- **Streaming output** for long-running tasks (ONLY for heavy tasks)
- **Cancellation support** via `CancellationToken`
- **Progress reporting** via `ProgressTracker`
- **Performance metrics** logged via `ExecutionProfiler`
- **Sandbox isolation** enforced for ALL executions
- **Capability scope** defined: allowed_operations, forbidden_operations, resource_limits

**Architecture Layers:**

- `core/execution_engine/` — EXECUTOR ONLY: no decisions, no retries, no routing
- `core/performance/` — SLA enforcement, rule-based optimization, bounded cache
- `capabilities/runtime/` — INTERNAL ONLY: async execution, batch, streaming, cancellation

---

### TASK 8.1 — Enhanced `BaseCapability` (Async-Ready ABC)

**Location:** `src/capabilities/base.py`
**Purpose:** Defines the HIGH-PERFORMANCE capability contract with async support.

#### Subtask 8.1.1 — Define `BaseCapability(ABC)` with 6 abstract methods

```python
from abc import ABC, abstractmethod
from src.capabilities.result import ToolResult
from src.capabilities.validator import ValidationResult
from src.core.decision.output import RiskLevel
from src.capabilities.runtime.cancellation import CancellationToken

class BaseCapability(ABC):
    name: str
    domain: str
    description: str
    supports_async: bool = False
    supports_batch: bool = False
    supports_streaming: bool = False

    @abstractmethod
    async def execute_async(self, args: dict,
                           cancel_token: CancellationToken | None = None) -> ToolResult:
        """Async execution with cancellation support. MUST NEVER RAISE."""
        ...

    @abstractmethod
    def validate(self, args: dict) -> ValidationResult:
        """Synchronous, fast, side-effect-free."""
        ...

    @abstractmethod
    def get_risk_level(self, args: dict | None = None) -> RiskLevel:
        """Compute dynamically from args."""
        ...

    @abstractmethod
    def dry_run(self, args: dict) -> ToolResult:
        """Must set result.dry_run=True. No side effects."""
        ...

    # Batch support (optional override)
    async def execute_batch(self, items: list[dict],
                             cancel_token: CancellationToken | None = None) -> list[ToolResult]:
        """Default: sequential execution. Override for parallel."""
        return [await self.execute_async(item, cancel_token) for item in items]

    # Sync wrapper (default) — MUST be called from synchronous contexts only
    def execute(self, args: dict) -> ToolResult:
        """
        Sync wrapper for execute_async().
        MUST be called from synchronous contexts only.
        From async contexts, call execute_async() directly.
        """
        import asyncio
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                raise RuntimeError(
                    f"{self.name}.execute() called from async context. "
                    "Use execute_async() instead."
                )
            return loop.run_until_complete(self.execute_async(args))
        except RuntimeError:
            raise
        except Exception as e:
            return ToolResult.failure(self.name, str(e))

    """
    DESIGN CONTRACT:
    - Sync contexts (CLI, tests): call execute(args)
    - Async contexts (FastAPI, Telegram, CapabilityRuntime): call execute_async(args)
    - Sandbox.execute() is sync — it wraps execute() via ThreadPoolExecutor
    - CapabilityRuntime.execute_async() calls Sandbox via asyncio.to_thread()
    """
```

**Artifact:** `src/capabilities/base.py`

---

### TASK 8.2 — Capability Runtime (Async Execution Layer)

**Location:** `src/capabilities/runtime/capability_runtime.py`
**Purpose:** High-performance execution layer with async, batch, streaming, cancellation.

#### Subtask 8.2.1 — Implement `CapabilityRuntime`

```python
class CapabilityRuntime:
    def __init__(self, executor, profiler):
        self._executor = executor  # CapabilityExecutor (6-gate)
        self._profiler = profiler  # ExecutionProfiler
        self._stream_buffer = StreamBuffer()

    async def execute_async(self, name: str, args: dict,
                            cancel_token: CancellationToken | None = None,
                            decision=None, mode="balanced") -> ToolResult:
        """Non-blocking execution with cancellation."""
        start = time.time()
        try:
            # Run through 6-gate pipeline (non-blocking via to_thread)
            import asyncio
            result = await asyncio.to_thread(
                self._executor.execute, name, args, decision, mode
            )
            # Record metrics
            latency_ms = (time.time() - start) * 1000
            self._profiler.record(name, latency_ms,
                                  result.success, result.risk_level)
            return result
        except asyncio.CancelledError:
            return ToolResult.failure(name, "cancelled")

    async def execute_batch(self, name: str, items: list[dict],
                            parallel: bool = True,
                            cancel_token: CancellationToken | None = None) -> list[ToolResult]:
        """Batch execution with optional parallelism."""
        if parallel:
            import asyncio
            tasks = [self.execute_async(name, item, cancel_token)
                      for item in items]
            return await asyncio.gather(*tasks)
        else:
            return [await self.execute_async(name, item, cancel_token)
                    for item in items]

    def stream_results(self, name: str, args: dict):
        """Generator for streaming output (if capability supports)."""
        return self._stream_buffer.stream(name, args)

    def cancel(self, task_id: str) -> bool:
        """Cancel a running task via CancellationToken."""
        # Cooperative cancellation
        ...
```

**Artifact:** `src/capabilities/runtime/capability_runtime.py`

---

### TASK 8.3 — Progress Tracker + Stream Buffer

**Location:** `src/capabilities/runtime/progress.py`, `stream.py`
**Purpose:** Real-time progress reporting and chunked output for long-running capabilities.

#### Subtask 8.3.1 — Implement `ProgressTracker`

```python
class ProgressTracker:
    def __init__(self, event_bus):
        self._event_bus = event_bus
        self._tasks: dict[str, dict] = {}

    def start(self, task_id: str, total: int = 100):
        self._tasks[task_id] = {"current": 0, "total": total, "status": "running"}

    def update(self, task_id: str, current: int, message: str = ""):
        if task_id in self._tasks:
            self._tasks[task_id]["current"] = current
            pct = int((current / max(self._tasks[task_id]["total"], 1)) * 100)
            self._event_bus.publish("EVT_PROGRESS", {
                "task_id": task_id, "percentage": pct, "message": message
            })

    def complete(self, task_id: str):
        self._tasks.pop(task_id, None)
        self._event_bus.publish("EVT_TASK_COMPLETE", {"task_id": task_id})
```

**Artifact:** `src/capabilities/runtime/progress.py`, `stream.py`

---

### TASK 8.4 — Cancellation Token

**Location:** `src/capabilities/runtime/cancellation.py`
**Purpose:** Cooperative cancellation for long-running tasks.

```python
class CancellationToken:
    def __init__(self):
        self._cancelled = False
        self._callbacks: list[callable] = []

    def cancel(self):
        self._cancelled = True
        for cb in self._callbacks:
            cb()

    def is_cancelled(self) -> bool:
        return self._cancelled

    def register_callback(self, callback: callable):
        self._callbacks.append(callback)

    def check(self):
        if self._cancelled:
            raise asyncio.CancelledError("Task cancelled by user")
```

**Artifact:** `src/capabilities/runtime/cancellation.py`

---

### TASK 8.5 — Reference: TaskScheduler (Implemented in Phase X1)

**Location:** `src/core/execution_engine/scheduler.py`
**Status:** Deferred to Phase X1. Phase 8 uses CapabilityRuntime directly.
CapabilityRuntime.execute_async() calls CapabilityExecutor without scheduling.
Full task scheduling with priority queue and dependency resolution: Phase X1.

---

### TASK 8.6 — Reference: Async Executor (Implemented in Phase X1)

**Location:** `src/core/execution_engine/async_executor.py`
**Status:** Deferred to Phase X1. Stub: pass.

---

### TASK 8.7 — Reference: Concurrency Controller (Implemented in Phase X1)

**Location:** `src/core/execution_engine/concurrency.py`
**Status:** Deferred to Phase X1. Stub: pass.

---

### TASK 8.8 — Execution Profiler (Performance Layer)

**Location:** `src/core/performance/profiler.py`
**Purpose:** Per-capability latency/CPU/memory metrics. Auto-optimization hooks.

#### Subtask 8.8.1 — Implement `ExecutionProfiler`

```python
class ExecutionProfiler:
    def __init__(self):
        self._metrics: dict[str, list[dict]] = {}
        self._cache = SmartCache()

    def record(self, capability: str, latency_ms: float,
                success: bool, risk_level: str):
        if capability not in self._metrics:
            self._metrics[capability] = []
        self._metrics[capability].append({
            "latency_ms": latency_ms, "success": success,
            "risk_level": risk_level, "timestamp": time.time()
        })
        # Auto-optimization: cache if frequent + fast
        recent = self._metrics[capability][-10:]
        if len(recent) >= 10 and all(r["success"] for r in recent):
            avg_latency = sum(r["latency_ms"] for r in recent) / 10
            if avg_latency < 100:  # Fast path
                self._cache.mark_hot_path(capability)

    def get_stats(self, capability: str) -> dict:
        """Return latency percentiles, success rate, avg CPU/memory."""
        ...

    def get_all_stats(self) -> dict:
        """Return stats for all capabilities."""
        ...
```

**Artifact:** `src/core/performance/profiler.py`

---

### TASK 8.9 — Rule-Based Optimization Hooks (REPLACES AdaptiveOptimizer)

**Location:** `src/core/performance/profiler.py` (extend existing)
**Purpose:** Rule-based thresholds that emit EVT_DEGRADATION events.
StateMachine decides action. No auto-switching. No strategy overrides.

Rules (read-only evaluation, emit event, stop):
- p95 latency > 1000ms for a capability → emit EVT_DEGRADATION
  `{capability, metric: "latency_p95_ms", value, suggested_action: "switch_model"}`
- success_rate < 0.8 → emit EVT_DEGRADATION
  `{capability, metric: "success_rate", value, suggested_action: "inspect_capability"}`
- hot_path detection (avg < 100ms, all success) → emit EVT_HOT_PATH
  `{capability}` — StateMachine may choose to pre-warm

These are observations, not actions. StateMachine is the ONLY actor.

**Artifact:** Updated `src/core/performance/profiler.py` (NO `src/core/performance/optimizer.py`)

---

### TASK 8.10 — Smart Cache

**Location:** `src/core/performance/cache.py`
**Purpose:** TTL + LRU for frequent operations. Reduces latency for repeated calls.

**Artifact:** `src/core/performance/cache.py`

---

### TASK 8.11 — Capability System Tests (15 tests)

**Location:** `tests/test_capabilities.py`

Required tests:

1. `BaseCapability` enforces all 6 abstract methods
2. `CapabilityRuntime.execute_async` returns `ToolResult`
3. `CapabilityRuntime.execute_batch` parallel returns N results
4. `ProgressTracker` publishes `EVT_PROGRESS` events
5. `CancellationToken.cancel()` triggers `CancelledError`
6. `TaskScheduler` priority ordering correct
7. `TaskScheduler` waits for dependencies
8. `ExecutionProfiler` records metrics correctly
9. `SmartCache` returns cached result for hot path
10. `CapabilityExecutor` async + cancellation works
11. Streaming output chunks delivered in order
12. Batch execution with partial failure handled
13. Concurrency limiter blocks overflow
14. Performance stats appear in `MetricsCollector`
15. `CancellationToken` callback triggered on cancel

**Artifact:** `tests/test_capabilities.py`

---

### TASK 8.12 — Performance Benchmarks

**Location:** `tests/test_performance.py`
**Purpose:** Automated performance regression testing.

**Artifact:** `src/core/performance/benchmark.py`, `tests/test_performance.py`

---

### Definition of Done — Phase 8

- [ ] All capabilities inherit enhanced `BaseCapability` with async support
- [ ] `CapabilityRuntime` provides async, batch, streaming, cancellation
- [ ] `TaskScheduler` handles priority queue + dependencies
- [ ] `ExecutionProfiler` records per-capability metrics
- [ ] `SmartCache` optimizes hot paths automatically
- [ ] All 15 tests pass
- [ ] Performance benchmarks establish baselines

---

## Phase 9 — System Control Capabilities (High-Performance Upgrade)

```yaml
phase_id: 9
priority: "P1"
status: "not_started"
total_tasks: 16
blocker: "Phase 8 complete"
next_action: "TASK 9.1"
performance_targets:
  fast_tools: "<100ms"
  medium_tools: "<500ms"
  heavy_tools: "async + streaming"
  non_blocking: "default"
```

### Theoretical Foundation

Each capability is NOW a **multi-operation, context-aware, optimized system component**:

- **Async execution** via `CapabilityRuntime`
- **Batch processing** for multi-item operations
- **Streaming output** for long-running tasks
- **Cancellation support** via `CancellationToken`
- **Progress reporting** via `ProgressTracker`
- **Performance metrics** logged via `ExecutionProfiler`
- **Sandbox isolation** enforced for ALL executions

**Upgrades from basic tools:**

- Simple function → Intelligent execution module
- Blocking → Non-blocking (async)
- Single operation → Batch + parallel
- No metrics → Full profiler integration

---

### TASK 9.1 — System Process Manager (was AppLauncher)

**Location:** `src/capabilities/system/apps.py`
**Depends on:** Phase 8 `BaseCapability` (enhanced async version)
**Purpose:** Full process lifecycle management with monitoring, not just launching.

#### Subtask 9.1.1 — Implement `execute_async()` (async)

```python
async def execute_async(self, args: dict, cancel_token=None) -> ToolResult:
    name = args.get("name", "")
    action = args.get("action", "open")  # open/close/restart

    if action == "open":
        return await self._launch_app(name, cancel_token)
    elif action == "close":
        return await self._close_app(name)
    elif action == "restart":
        return await self._restart_app(name)
    elif action == "list_running":
        return await self._list_running()
```

#### Subtask 9.1.2 — Add process monitoring

- `detect_running(name)` → `list[int]` (PIDs)
- `attach_to_process(pid)` → `ToolResult` with process info
- `batch_launch(names: list[str])` → `list[ToolResult]` (parallel)

#### Subtask 9.1.3 — Add execution profiles

- `priority_control`: low/normal/high priority via `psutil.Process().nice()`
- `auto_retry`: if crash detected, relaunch with exponential backoff
- `monitor_health`: periodic check every 5s, report CPU/memory usage

**Performance:** Launch <200ms, batch launch (5 apps) <500ms (parallel)
**Artifact:** `src/capabilities/system/apps.py`

---

### TASK 9.2 — Real-Time System Monitor (was SystemInfo)

**Location:** `src/capabilities/system/sysinfo.py`
**Upgrade:** Live streaming stats, threshold alerts, historical tracking.

#### Subtask 9.2.1 — Implement streaming stats

```python
async def execute_async(self, args: dict, cancel_token=None) -> ToolResult:
    info_type = args.get("info_type", "all")
    stream = args.get("stream", False)

    if stream:
        # Stream updates every 500ms via EventBus
        tracker = ProgressTracker(event_bus)
        tracker.start("sysinfo", total=100)
        while not cancel_token.is_cancelled():
            data = self._collect_stats(info_type)
            self._event_bus.publish("EVT_SYSTEM_UPDATE", data)
            tracker.update("sysinfo", ...)
            await asyncio.sleep(0.5)
```

#### Subtask 9.2.2 — Add threshold alerts

- Configurable thresholds in `config/runtime/settings.yaml`
- `cpu_threshold: 90%`, `ram_threshold: 85%`, `gpu_threshold: 80%`
- Exceed → publish `EVT_THRESHOLD_ALERT` with metric name + value

#### Subtask 9.2.3 — Add historical tracking

- Store metrics to `data/metrics.db` (SQLite, WAL mode, thread-local pool, same pattern as memory.db)
- `get_history(hours: int = 24)` → returns time-series data
- Performance analysis: min/max/avg for each metric

```python
# Schema for data/metrics.db (WAL mode, thread-local pool)
CREATE TABLE IF NOT EXISTS system_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    timestamp TEXT NOT NULL,
    metric_type TEXT NOT NULL CHECK(metric_type IN ('cpu','ram','gpu','disk','network')),
    value REAL NOT NULL,
    threshold REAL,
    alert_fired INTEGER DEFAULT 0,
    trace_id TEXT
);
CREATE INDEX IF NOT EXISTS idx_metrics_timestamp ON system_metrics(timestamp);
CREATE INDEX IF NOT EXISTS idx_metrics_type ON system_metrics(metric_type);
PRAGMA journal_mode=WAL;
```

Corruption recovery: same pattern as memory.db — rename to `.corrupted.{timestamp}`, create fresh.

**Performance:** Snapshot <50ms, streaming ~2ms/update
**Artifact:** `src/capabilities/system/sysinfo.py`

---

### TASK 9.3 — Smart Data Channel (was Clipboard)

**Location:** `src/capabilities/system/clipboard.py`
**Upgrade:** History tracking, multi-format support, sync pipeline, transformations.

#### Subtask 9.3.1 — Implement history tracking

- `history: list[dict]` (last 50 entries)
- Each entry: `{timestamp, action, content_preview, size_bytes}`
- `get_history(limit: int = 10)` → returns last N entries

#### Subtask 9.3.2 — Add multi-format support

- Text: `pyperclip.paste()` / `pyperclip.copy(text)`
- Image: `PIL.ImageGrab.clipboard()` / `pyperclip.copy(image)` (if supported)
- File refs: detect file paths in clipboard, return `{paths: list[str]}`

#### Subtask 9.3.3 — Add sync pipeline + transformations

- `sync_to_file(path: str)` → write clipboard history to file
- `transform(operation: str)` → `clean` (strip whitespace), `format_json`, `translate(target_lang)`

**Performance:** Read/write <20ms, history lookup <10ms
**Artifact:** `src/capabilities/system/clipboard.py`

---

### TASK 9.4 — Event Notification System (was Notifications)

**Location:** `src/capabilities/notify/toasts.py`
**Upgrade:** Queue system, priority levels, grouped notifications, cross-platform delivery.

#### Subtask 9.4.1 — Implement notification queue

```python
class NotificationQueue:
    def __init__(self):
        self._queue: list[dict] = []
        self._max_pending = 10

    async def enqueue(self, title: str, message: str,
                       priority: int = 1, duration: int = 5):
        item = {"title": title, "message": message,
                "priority": priority, "duration": duration,
                "timestamp": time.time()}
        # Insert sorted by priority (higher first)
        ...
```

#### Subtask 9.4.2 — Add priority levels

- `0`: Low (batch with others)
- `1`: Normal (default)
- `2`: High (display immediately)
- `3`: Critical (override DND mode)

#### Subtask 9.4.3 — Add grouped notifications

- Group by `title` if same within 60 seconds
- Display: "Title: 3 new messages" instead of 3 separate toasts

#### Subtask 9.4.4 — Cross-platform delivery

- Primary: `plyer.notification.notify()`
- Fallback: `print(f"[NOTIFY] {title}: {message}")`
- Windows: Toast via `win10toast` (if available)
- Linux: `notify-send` command
- macOS: `osascript -e 'display notification'`

**Performance:** Queue enqueue <5ms, display <100ms
**Artifact:** `src/capabilities/notify/toasts.py`

---

### TASK 9.5 — Vision Pipeline (was Screenshot)

**Location:** `src/capabilities/screen/capture.py`
**Upgrade:** Region capture, multi-monitor, OCR pipeline, image analysis hooks.

#### Subtask 9.5.1 — Implement multi-monitor support

- `ImageGrab.grab(bbox=monitor.bbox)` for specific monitor
- `list_monitors()` → returns `list[{id, width, height, x, y}]`
- Default: primary monitor, or `monitor_id` in args

#### Subtask 9.5.2 — Add OCR pipeline (streaming)

```python
async def execute_async(self, args: dict, cancel_token=None) -> ToolResult:
    img = self._capture(args.get("region"))

    if args.get("ocr", False):
        # Stream OCR progress
        tracker = ProgressTracker(self._event_bus)
        tracker.start("ocr", total=100)
        text = await self._ocr_with_progress(img, tracker)
        tracker.complete("ocr")
    ...
```

#### Subtask 9.5.3 — Add image analysis hooks

- After capture → publish `EVT_SCREENSHOT_CAPTURED` with image path
- Vision capability can subscribe → auto-analyze screenshots
- `analyze_after_capture: bool` flag in args

**Performance:** Capture <100ms, OCR <500ms (streaming updates)
**Artifact:** `src/capabilities/screen/capture.py`

---

### TASK 9.6 — File System Engine (was FileOps)

**Location:** `src/capabilities/files/file_ops.py`
**Upgrade:** Batch operations, indexing, search engine, watch, transactional operations.

#### Subtask 9.6.1 — Implement batch operations

```python
async def execute_batch(self, items: list[dict],
                        cancel_token=None) -> list[ToolResult]:
    """Parallel batch execution with error aggregation."""
    import asyncio
    tasks = [self._execute_single(item) for item in items]
    return await asyncio.gather(*tasks, return_exceptions=True)
```

#### Subtask 9.6.2 — Add file indexing + search

- Background indexer: scan `allowed_roots` → SQLite FTS5 index
- `search(query: str, limit: int = 10)` → returns matching files with snippets
- Index updated on every write/delete operation

#### Subtask 9.6.3 — Add file system watch

- `watch(path: str, callback: callable)` → monitor for changes
- Events: `created`, `modified`, `deleted`, `moved`
- Uses `watchdog` library (cross-platform)

#### Subtask 9.6.4 — Add transactional operations

- `begin_transaction()` → lock affected paths
- `commit()` / `rollback()` → all-or-nothing semantics
- On crash → auto-rollback, no partial state

**Performance:** Single op <100ms, batch (10 files) <500ms (parallel)
**Artifact:** `src/capabilities/files/file_ops.py`

---

### TASK 9.7 — Sandboxed Compute Engine (was CodeExecutor)

**Location:** `src/capabilities/coder/executor.py`
**Upgrade:** Multi-language, async execution, resource limits, streaming output, job queue.

#### Subtask 9.7.1 — Implement strict sandbox isolation

```python
async def execute_async(self, args: dict, cancel_token=None) -> ToolResult:
    # ALL code runs in ProcessPool (isolated subprocess)
    from src.core.sandbox.process_pool import ProcessPool

    pool = ProcessPool(max_memory_mb=512, timeout_s=args.get("timeout_s", 30))
    return await pool.execute_secure(
        language=args["language"],
        code=args["code"],
        cancel_token=cancel_token
    )
```

#### Subtask 9.7.2 — Add streaming output

- `stream_output: bool` flag → yield stdout/stderr chunks as they appear
- Progress updates via `ProgressTracker` (for long-running code)

#### Subtask 9.7.3 — Add job queue + resource limits

- `queue_job(language, code)` → returns `job_id`
- `get_job_status(job_id)` → pending/running/completed/failed
- Resource limits enforced: CPU 50%, RAM 512MB, timeout 30s

#### Subtask 9.7.4 — Add kill switch

- `cancel_job(job_id)` → `SIGTERM` → `SIGKILL` after 2s grace period
- Cooperative cancellation via `CancellationToken` in code

**CRITICAL:** No direct subprocess calls — ALL via `ProcessPool`
**Performance:** Launch <500ms, streaming ~10ms/chunk
**Artifact:** `src/capabilities/coder/executor.py`, `src/core/sandbox/process_pool.py`

---

### TASK 9.8 — Data Extraction Engine (was WebSearch)

**Location:** `src/capabilities/search/web_search.py`
**Upgrade:** Multi-engine fallback, parsing engine, structured data extraction, caching, rate limiting.

#### Subtask 9.8.1 — Implement multi-engine fallback

```python
async def execute_async(self, args: dict, cancel_token=None) -> ToolResult:
    engines = ["duckduckgo", "bing", "google"]  # In order
    for engine in engines:
        try:
            results = await self._search_engine(engine, args["query"])
            if results:
                return ToolResult(success=True, data={"results": results})
        except Exception as e:
            logger.warning(f"{engine} failed: {e}, trying next...")
    return ToolResult.failure("web_search", "all engines failed")
```

#### Subtask 9.8.2 — Add parsing engine

- Extract: titles, URLs, snippets, publish dates
- Structured data: if search result is a product → `{price, rating, availability}`
- Clean HTML → plain text, remove ads

#### Subtask 9.8.3 — Add caching + rate limiting

- `SmartCache`: cache results by query hash, TTL = 1 hour
- Rate limiter: max 10 requests/minute per engine
- On rate limit → return cached or fallback to next engine

**Performance:** First search ~2s, cached <50ms
**Artifact:** `src/capabilities/search/web_search.py`

---

### TASK 9.9 — Batch Execution Tests (6 tests)

**Location:** `tests/test_batch.py`

Required tests:

1. `execute_batch()` with 5 items → returns 5 results
2. Batch with partial failure → successful items returned, failures in `ToolResult`
3. Parallel batch faster than sequential (>30% improvement)
4. `CancellationToken` cancels all batch items
5. Progress tracking reports percentage for batch
6. Batch with dependency resolution (item 2 waits for item 1)

**Artifact:** `tests/test_batch.py`

---

### TASK 9.10 — Streaming Output Tests (4 tests)

**Location:** `tests/test_streaming.py`

Required tests:

1. Long-running capability streams chunks in order
2. `ProgressTracker` publishes updates at 10%/50%/90%
3. Streaming cancelled mid-way → partial results returned
4. `StreamBuffer` handles backpressure (slow consumer)

**Artifact:** `tests/test_streaming.py`

---

### TASK 9.11 — Performance Regression Tests (5 tests)

**Location:** `tests/test_performance.py`

Required tests:

1. Fast tools (system_info) <100ms average
2. Medium tools (screenshot) <500ms average
3. Batch (5 file_ops) completes in <2x single op time
4. `ExecutionProfiler` records metrics for all capabilities
5. `SmartCache` improves repeated calls by >50%

**Artifact:** `tests/test_performance.py`

---

### TASK 9.12 — Sandbox Isolation Tests (6 tests)

**Location:** `tests/test_sandbox.py`

Required tests (in addition to previous 4):

5. `ProcessPool` kills runaway code after timeout
6. `ProcessPool` enforces memory limit (512MB)
7. Code cannot access files outside allowed roots
8. `kill_switch()` terminates process immediately
9. `ResourceMonitor` tracks CPU/RAM during execution
10. Sandbox isolation: code crash doesn't affect main process

**Artifact:** `tests/test_sandbox.py`

---

### TASK 9.13 — Advanced FileOps Tests (7 tests)

**Location:** `tests/test_file_engine.py`

Required tests:

1. Batch file write (5 files) → all written
2. File search by content → returns matching files
3. File watch triggers on create/modify/delete
4. Transaction: partial failure → rollback, no files changed
5. Transaction: success → all files committed
6. Index updated after write
7. `Path.resolve()` + `os.path.commonpath()` blocks traversal

**Artifact:** `tests/test_file_engine.py`

---

### TASK 9.14 — Notification Queue Tests (4 tests)

**Location:** `tests/test_notifications.py`

Required tests:

1. High priority notification displayed before low priority
2. Grouped notifications: 3 similar → 1 grouped
3. Queue max_pending: 11th drops oldest low-priority
4. Cross-platform fallback works when plyer unavailable

**Artifact:** `tests/test_notifications.py`

---

### TASK 9.15 — Vision Pipeline Tests (5 tests)

**Location:** `tests/test_vision_pipeline.py`

Required tests:

1. Multi-monitor: capture specific monitor by ID
2. OCR progress streaming: updates at 25%/50%/75%/100%
3. Screenshot → auto-analyze hook (mock vision capability)
4. Region capture returns correct bbox
5. Headless environment → graceful failure

**Artifact:** `tests/test_vision_pipeline.py`

---

### TASK 9.16 — Data Extraction Tests (6 tests)

**Location:** `tests/test_data_extraction.py`

Required tests:

1. DuckDuckGo → Bing fallback on failure
2. Cached result returned for repeat query <1hr
3. Rate limiter blocks 11th request in 1 minute
4. Structured data extraction: product → price/rating
5. HTML cleaning removes ads, keeps main content
6. All engines fail → graceful error, no crash

**Artifact:** `tests/test_data_extraction.py`

---

### Definition of Done — Phase 9

- [ ] All 16 tasks complete (8 upgraded capabilities + 8 test suites)
- [ ] ALL capabilities use `execute_async()` via `CapabilityRuntime`
- [ ] ALL capabilities support batch mode (where applicable)
- [ ] ALL long-running capabilities support streaming
- [ ] ALL capabilities log metrics via `ExecutionProfiler`
- [ ] `code_exec` uses `ProcessPool` — NO direct subprocess
- [ ] `file_ops` batch (5 files) completes in <2x single file time
- [ ] `web_search` has multi-engine fallback + caching
- [ ] All performance targets met (fast <100ms, medium <500ms)
- [ ] `pytest tests/test_batch.py tests/test_streaming.py tests/test_performance.py tests/test_sandbox.py tests/test_file_engine.py tests/test_notifications.py tests/test_vision_pipeline.py tests/test_data_extraction.py -v` → ALL pass

---

## Phase X1 — Execution Engine (EXECUTOR ONLY)

```yaml
phase_id: "X1"
priority: "P1"
status: "not_started"
total_tasks: 6
blocker: "Phase 9 complete"
next_action: "TASK X1.1"
stabilization: "v3.2 — ExecutionEngine is executor ONLY, no decisions/retries/routing, termination confirmation required"
```

### Theoretical Foundation

The Execution Engine is the **controlled execution layer** that handles task scheduling and concurrency. It transforms the runtime from a simple sequential executor to a **non-blocking system**.

**CRITICAL RESTRICTIONS (v3.2):**

- ExecutionEngine accepts tasks ONLY from StateMachine/runtime
- ExecutionEngine executes ONLY — returns structured results
- ExecutionEngine MUST NOT: decide, route, retry independently
- ALL decisions return to StateMachine
- Retries are controlled ONLY by StateMachine

**Key Capabilities:**

- Priority-based task scheduling (StateMachine-controlled)
- Parallel execution with semaphore-based limits
- Dependency resolution (task B waits for task A)
- Future/promise pattern for async results

---

### TASK X1.1 — Task Scheduler

**Location:** `src/core/execution_engine/scheduler.py`
**Purpose:** Priority queue with dependency resolution and parallel execution.

#### Subtask X1.1.1 — Implement `TaskScheduler`

```python
import heapq
from dataclasses import dataclass, field
import asyncio

@dataclass(order=True)
class Task:
    priority: int
    name: str = field(compare=False)
    args: dict = field(compare=False)
    task_id: str = field(compare=False, default_factory=lambda: str(uuid4()))
    dependencies: list[str] = field(default_factory=list)
    cancel_token: CancellationToken | None = field(compare=False, default=None)

class TaskScheduler:
    def __init__(self, runtime: CapabilityRuntime, concurrency: int = 4):
        self._runtime = runtime
        self._concurrency = concurrency
        self._queue: list[Task] = []
        self._running: dict[str, asyncio.Task] = {}
        self._semaphore = asyncio.Semaphore(concurrency)
        self._completed: dict[str, ToolResult] = {}
        self._event_bus = EventBus()

    async def schedule(self, task: Task) -> str:
        """Schedule a task, return task_id."""
        heapq.heappush(self._queue, task)
        await self._process_queue()
        return task.task_id

    async def _process_queue(self):
        """Process queue, respecting dependencies and concurrency limits."""
        while self._queue and len(self._running) < self._concurrency:
            task = heapq.heappop(self._queue)
            if all(dep in self._completed for dep in task.dependencies):
                self._running[task.task_id] = asyncio.create_task(
                    self._execute_task(task)
                )
            else:
                heapq.heappush(self._queue, task)  # Re-queue if deps not met

    async def _execute_task(self, task: Task):
        async with self._semaphore:
            try:
                result = await self._runtime.execute_async(
                    task.name, task.args, task.cancel_token
                )
                self._completed[task.task_id] = result
                self._event_bus.publish("EVT_TASK_COMPLETE", {
                    "task_id": task.task_id, "success": result.success
                })
            except Exception as e:
                self._completed[task.task_id] = ToolResult.failure(
                    task.name, str(e)
                )
            finally:
                self._running.pop(task.task_id, None)
                await self._process_queue()  # Check if new tasks can run

    def get_status(self, task_id: str) -> str:
        if task_id in self._completed:
            return "completed"
        if task_id in self._running:
            return "running"
        return "pending"
```

**Artifact:** `src/core/execution_engine/scheduler.py`

---

### TASK X1.2 — Async Executor

**Location:** `src/core/execution_engine/async_executor.py`
**Purpose:** Non-blocking capability execution with Future pattern.

#### Subtask X1.2.1 — Implement `AsyncExecutor`

```python
class AsyncExecutor:
    def __init__(self, runtime: CapabilityRuntime):
        self._runtime = runtime
        self._futures: dict[str, asyncio.Future] = {}

    async def execute(self, name: str, args: dict,
                     cancel_token: CancellationToken | None = None) -> ToolResult:
        """Non-blocking execution returning ToolResult."""
        loop = asyncio.get_event_loop()
        future = loop.create_future()
        self._futures[f"{name}_{id(args)}"] = future

        try:
            result = await self._runtime.execute_async(name, args, cancel_token)
            future.set_result(result)
            return result
        except Exception as e:
            future.set_exception(e)
            raise

    def cancel_all(self):
        """Cancel all pending futures."""
        for f in self._futures.values():
            f.cancel()
        self._futures.clear()
```

**Artifact:** `src/core/execution_engine/async_executor.py`

---

### TASK X1.3 — Batch Processor

**Location:** `src/core/execution_engine/batch_processor.py`
**Purpose:** Multi-item capability execution with aggregation.

#### Subtask X1.3.1 — Implement `BatchProcessor`

```python
class BatchProcessor:
    def __init__(self, runtime: CapabilityRuntime, scheduler: TaskScheduler):
        self._runtime = runtime
        self._scheduler = scheduler

    async def execute_parallel(self, name: str, items: list[dict],
                                max_parallel: int = 4) -> list[ToolResult]:
        """Execute all items in parallel (up to max_parallel)."""
        semaphore = asyncio.Semaphore(max_parallel)

        async def _execute_with_limit(item):
            async with semaphore:
                return await self._runtime.execute_async(name, item)

        tasks = [_execute_with_limit(item) for item in items]
        return await asyncio.gather(*tasks, return_exceptions=True)

    async def execute_sequential(self, name: str, items: list[dict]) -> list[ToolResult]:
        """Execute items one by one."""
        results = []
        for item in items:
            result = await self._runtime.execute_async(name, item)
            results.append(result)
        return results

    async def execute_with_aggregation(self, name: str, items: list[dict]) -> dict:
        """Execute and aggregate results."""
        results = await self.execute_parallel(name, items)
        return {
            "total": len(results),
            "successful": sum(1 for r in results if r.success),
            "failed": sum(1 for r in results if not r.success),
            "results": results
        }
```

**Artifact:** `src/core/execution_engine/batch_processor.py`

---

### TASK X1.4 — Concurrency Controller

**Location:** `src/core/execution_engine/concurrency.py`
**Purpose:** Semaphore-based parallelism limits. Prevents system overload.

#### Subtask X1.4.1 — Implement `ConcurrencyController`

```python
class ConcurrencyController:
    def __init__(self, default_limit: int = 4):
        self._semaphores: dict[str, asyncio.Semaphore] = {}
        self._default_limit = default_limit

    def get_semaphore(self, capability: str) -> asyncio.Semaphore:
        if capability not in self._semaphores:
            # Different limits for different capability types
            limit = self._get_limit_for_capability(capability)
            self._semaphores[capability] = asyncio.Semaphore(limit)
        return self._semaphores[capability]

    def _get_limit_for_capability(self, name: str) -> int:
        limits = {
            "code_exec": 1,      # Heavy, limit to 1
            "screenshot": 2,     # Medium
            "web_search": 3,     # Light
            "open_app": 5,       # Very light
        }
        return limits.get(name, self._default_limit)

    async def acquire(self, capability: str):
        sem = self.get_semaphore(capability)
        await sem.acquire()

    def release(self, capability: str):
        sem = self.get_semaphore(capability)
        sem.release()
```

**Artifact:** `src/core/execution_engine/concurrency.py`

---

### TASK X1.5 — Execution Engine Tests (8 tests)

**Location:** `tests/test_execution_engine.py`

Required tests:

1. `TaskScheduler.schedule()` returns valid `task_id`
2. Priority ordering: higher priority tasks execute first
3. Dependency resolution: task B waits for task A
4. `ConcurrencyController` limits parallel executions
5. `BatchProcessor.parallel()` runs faster than sequential
6. `AsyncExecutor.cancel_all()` cancels pending tasks
7. Task completion event published to EventBus
8. Semaphore prevents overload (>limit tasks blocked)

**Artifact:** `tests/test_execution_engine.py`

---

### TASK X1.6 — Integration with Runtime Loop

**Location:** `src/core/runtime/loop.py`
**Purpose:** Wire Execution Engine into main loop.

#### Subtask X1.6.1 — Update `run_turn()`

```python
# In loop.py
from src.core.execution_engine.scheduler import TaskScheduler
from src.core.execution_engine.batch_processor import BatchProcessor

class RuntimeLoop:
    def __init__(self):
        self._scheduler = TaskScheduler(CapabilityRuntime(...))
        self._batch_processor = BatchProcessor(...)

    async def run_turn(self, input_packet) -> FinalResponse:
        # Schedule as task instead of direct call
        task = Task(priority=1, name="decide", args={...})
        task_id = await self._scheduler.schedule(task)
        # Wait for completion
        while self._scheduler.get_status(task_id) != "completed":
            await asyncio.sleep(0.01)
        ...
```

**Artifact:** Updated `src/core/runtime/loop.py`

---

### Definition of Done — Phase X1

- [ ] `TaskScheduler` handles priority queue + dependencies
- [ ] `AsyncExecutor` provides non-blocking execution
- [ ] `BatchProcessor` supports parallel + sequential + aggregation
- [ ] `ConcurrencyController` prevents system overload
- [ ] Runtime loop wired to Execution Engine
- [ ] All 8 tests pass

---

## Phase X2 — Sandbox System (HARDENED)

```yaml
phase_id: "X2"
priority: "P0"
status: "not_started"
total_tasks: 5
blocker: "Phase X1 complete"
next_action: "TASK X2.1"
stabilization: "v3.2 — system-level sandbox hardening, dual-mode cancellation"
```

### Theoretical Foundation

The Sandbox System provides **strict system-level isolation** for ALL capability executions. No capability runs outside the sandbox. This includes:

- **Process isolation**: separate PID for each execution
- **Privilege drop**: no admin/root access in sandbox
- **Filesystem sandbox**: allowlist paths only
- **Network policy**: deny by default
- **Syscall restrictions**: where possible (platform-dependent)
- **Execution timeout**: hard kill on exceeding SLA
- **Process tree kill**: parent + children killed on cancellation

---

### TASK X2.1 — Process Pool (Isolated Subprocess)

**Location:** `src/core/sandbox/process_pool.py`
**Purpose:** Execute untrusted code in isolated subprocess with resource limits.

#### Subtask X2.1.1 — Implement `ProcessPool`

```python
import subprocess
import resource
import os

class ProcessPool:
    def __init__(self, max_memory_mb: int = 512, timeout_s: int = 30):
        self._max_memory_mb = max_memory_mb
        self._timeout_s = timeout_s
        self._active: dict[str, subprocess.Popen] = {}

    async def execute_secure(self, language: str, code: str,
                            cancel_token=None) -> ToolResult:
        """Execute code in isolated subprocess with resource limits."""
        import tempfile
        import uuid

        tmpdir = tempfile.mkdtemp(prefix="jarvis_sandbox_")
        ext = {"python": ".py", "javascript": ".js", "bash": ".sh"}[language]
        code_file = os.path.join(tmpdir, f"code{ext}")

        with open(code_file, "w") as f:
            f.write(code)

        interpreter = {"python": "python3", "javascript": "node", "bash": "bash"}[language]

        try:
            # Set resource limits (Unix only, Windows needs different approach)
            if os.name == "posix":
                def _set_limits():
                    # Memory limit (MB → bytes)
                    resource.setrlimit(resource.RLIMIT_AS,
                                    (self._max_memory_mb * 1024 * 1024, -1))
                    # CPU time limit
                    resource.setrlimit(resource.RLIMIT_CPU, (self._timeout_s, -1))
            else:
                _set_limits = None  # Windows: use subprocess timeout

            proc = subprocess.Popen(
                [interpreter, code_file],
                capture_output=True,
                timeout=self._timeout_s,
                cwd=tmpdir,
                env={"PATH": "/usr/bin:/bin", "HOME": tmpdir},  # Minimal env
                preexec_fn=_set_limits if os.name == "posix" else None
            )

            task_id = str(uuid.uuid4())
            self._active[task_id] = proc

            try:
                stdout, stderr = proc.communicate(timeout=self._timeout_s)
                return ToolResult(
                    success=(proc.returncode == 0),
                    data={
                        "stdout": stdout.decode("utf-8", errors="replace"),
                        "stderr": stderr.decode("utf-8", errors="replace"),
                        "returncode": proc.returncode
                    }
                )
            except subprocess.TimeoutExpired:
                import signal, time as _time
                # Dual-mode cancellation per Architecture Principle 7
                try:
                    proc.send_signal(signal.SIGTERM)   # soft: SIGTERM
                    _time.sleep(2.0)                    # grace period: 2 seconds
                    if proc.poll() is None:
                        proc.kill()                     # hard: SIGKILL if still alive
                except OSError:
                    pass
                # Kill entire process tree (children too)
                try:
                    import psutil
                    parent = psutil.Process(proc.pid)
                    for child in parent.children(recursive=True):
                        child.kill()
                    parent.kill()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
                termination_confirmed = proc.poll() is not None
                return ToolResult.failure(
                    "code_exec",
                    f"timeout after {self._timeout_s}s — "
                    f"termination {'confirmed' if termination_confirmed else 'failed'}"
                )
            finally:
                self._active.pop(task_id, None)
                import shutil
                shutil.rmtree(tmpdir, ignore_errors=True)

        except Exception as e:
            return ToolResult.failure("code_exec", str(e))
```

**Artifact:** `src/core/sandbox/process_pool.py`

---

### TASK X2.2 — Resource Monitor

**Location:** `src/core/sandbox/resource_monitor.py`
**Purpose:** Track CPU/RAM usage per execution.

#### Subtask X2.2.1 — Implement `ResourceMonitor`

```python
import psutil

class ResourceMonitor:
    def __init__(self):
        self._process_stats: dict[int, list[dict]] = {}  # pid -> stats history

    def start_monitoring(self, pid: int):
        """Start tracking resource usage for a process."""
        if pid not in self._process_stats:
            self._process_stats[pid] = []

        try:
            proc = psutil.Process(pid)
            stats = {
                "cpu_percent": proc.cpu_percent(interval=0.1),
                "memory_mb": proc.memory_info().rss / 1024 / 1024,
                "num_threads": proc.num_threads(),
                "timestamp": time.time()
            }
            self._process_stats[pid].append(stats)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    def stop_monitoring(self, pid: int) -> dict:
        """Stop tracking and return summary."""
        stats = self._process_stats.pop(pid, [])
        if not stats:
            return {}

        return {
            "peak_cpu": max(s["cpu_percent"] for s in stats),
            "peak_memory_mb": max(s["memory_mb"] for s in stats),
            "avg_cpu": sum(s["cpu_percent"] for s in stats) / len(stats),
            "samples": len(stats)
        }
```

**Artifact:** `src/core/sandbox/resource_monitor.py`

---

### TASK X2.3 — Filesystem Restrictor

**Location:** `src/core/sandbox/filesystem.py`
**Purpose:** Chroot-like path restrictions for sandbox.

#### Subtask X2.3.1 — Implement `FilesystemRestrictor`

```python
class FilesystemRestrictor:
    def __init__(self, allowed_roots: list[str] | None = None):
        self._allowed_roots = allowed_roots or [
            tempfile.gettempdir(),
            os.path.expanduser("~/.jarvis/sandbox")
        ]

    def validate_path(self, path: str) -> tuple[bool, str]:
        """Check if path is within allowed roots."""
        resolved = Path(path).resolve()

        for root in self._allowed_roots:
            root_resolved = Path(root).resolve()
            try:
                resolved.relative_to(root_resolved)
                return True, str(resolved)
            except ValueError:
                continue

        return False, f"Path {path} is outside allowed roots"

    def restrict_environment(self, env: dict) -> dict:
        """Remove sensitive env vars."""
        restricted = env.copy()
        # Remove sensitive vars
        for var in ["HOME", "USER", "PATH", "LD_LIBRARY_PATH"]:
            if var in restricted:
                del restricted[var]
        # Set sandbox-safe values
        restricted["HOME"] = tempfile.gettempdir()
        restricted["PATH"] = "/usr/bin:/bin"
        return restricted
```

**Artifact:** `src/core/sandbox/filesystem.py`

---

### TASK X2.4 — Sandbox Integration Tests (6 tests)

**Location:** `tests/test_sandbox_system.py`

Required tests:

1. `ProcessPool` executes code in isolated subprocess
2. Memory limit enforced (512MB)
3. Timeout kills runaway code
4. `ResourceMonitor` tracks CPU/RAM correctly
5. `FilesystemRestrictor` blocks paths outside allowed roots
6. Code crash doesn't affect main process

**Artifact:** `tests/test_sandbox_system.py`

---

### TASK X2.5 — Wire Sandbox into CapabilityExecutor

**Location:** `src/capabilities/executor.py`
**Purpose:** Ensure ALL capabilities run through sandbox.

#### Subtask X2.5.1 — Update Gate 6

```python
# In CapabilityExecutor.execute()
# Gate 6: Sandbox execution
if name == "code_exec":
    # Use ProcessPool for code execution
    pool = ProcessPool(
        max_memory_mb=limits.code_memory_mb,
        timeout_s=limits.code_timeout_s
    )
    result = await pool.execute_secure(
        args.get("language"), args.get("code"), cancel_token
    )
else:
    # Use ThreadPoolExecutor for other capabilities
    result = Sandbox.execute(capability, args, timeout_s)
```

**Artifact:** Updated `src/capabilities/executor.py`

---

### Definition of Done — Phase X2

- [ ] `ProcessPool` provides isolated subprocess execution
- [ ] Resource limits (CPU, RAM, time) enforced
- [ ] `FilesystemRestrictor` blocks unauthorized paths
- [ ] `ResourceMonitor` tracks usage per execution
- [ ] ALL capabilities route through sandbox
- [ ] All 6 tests pass

---

## Phase X3 — Performance (SLA Enforced)

```yaml
phase_id: "X3"
priority: "P1"
status: "not_started"
total_tasks: 5
blocker: "Phase X2 complete"
next_action: "TASK X3.1"
stabilization: "v3.2 — passive SLA events, StateMachine decision authority"
```

### Theoretical Foundation

Performance Monitoring provides **real-time SLA enforcement** and controlled optimization:

- Per-capability latency/CPU/memory metrics
- **SLA Enforcer**: monitors execution vs targets (fast=100ms, medium=500ms, heavy=5000ms)
- **Rule-based optimization**: simple thresholds, no auto-switching strategies
- **Bounded cache**: TTL + LRU eviction, dynamic TTL for hot paths
- **Degradation strategy**: on_degradation → reduce_quality, switch_strategy

**Global SLA Config:**

```yaml
sla:
  fast: 100ms
  medium: 500ms
  heavy: 5000ms
```

**Cache Policy:**

```yaml
cache:
  ttl: dynamic
  eviction: LRU
```

**Complexity Control (v3.2):**

- No adaptive optimizer — keep rule-based only
- Streaming ONLY for heavy tasks
- Batching ONLY where needed (multi-item operations)

---

### TASK X3.1 — Execution Profiler

**Location:** `src/core/performance/profiler.py`
**Purpose:** Per-capability latency/CPU/memory metrics with auto-optimization hooks.

#### Subtask X3.1.1 — Implement `ExecutionProfiler` (enhanced from Phase 8)

```python
class ExecutionProfiler:
    def __init__(self):
        self._metrics: dict[str, list[dict]] = {}
        self._cache = SmartCache()
        self._hot_paths: set[str] = set()

    def record(self, capability: str, latency_ms: float,
                success: bool, risk_level: str):
        if capability not in self._metrics:
            self._metrics[capability] = []

        self._metrics[capability].append({
            "latency_ms": latency_ms,
            "success": success,
            "risk_level": risk_level,
            "timestamp": time.time()
        })

        # Keep only last 1000 entries per capability
        if len(self._metrics[capability]) > 1000:
            self._metrics[capability] = self._metrics[capability][-1000:]

        # Auto-optimization: mark hot paths
        self._check_hot_path(capability)

    def _check_hot_path(self, capability: str):
        """Mark capability as hot path if frequently used + fast."""
        recent = self._metrics[capability][-10:]
        if len(recent) >= 10:
            avg_latency = sum(r["latency_ms"] for r in recent) / 10
            all_success = all(r["success"] for r in recent)

            if avg_latency < 100 and all_success:
                self._hot_paths.add(capability)
                self._cache.mark_hot_path(capability)

    def get_stats(self, capability: str) -> dict:
        """Return latency percentiles, success rate, avg CPU/memory."""
        if capability not in self._metrics or not self._metrics[capability]:
            return {}

        latencies = [r["latency_ms"] for r in self._metrics[capability]]
        return {
            "count": len(latencies),
            "avg_ms": sum(latencies) / len(latencies),
            "p50_ms": sorted(latencies)[len(latencies)//2],
            "p95_ms": sorted(latencies)[int(len(latencies)*0.95)],
            "p99_ms": sorted(latencies)[int(len(latencies)*0.99)],
            "success_rate": sum(1 for r in self._metrics[capability]
                                 if r["success"]) / len(self._metrics[capability])
        }

    def get_all_stats(self) -> dict:
        """Return stats for all capabilities."""
        return {cap: self.get_stats(cap) for cap in self._metrics}
```

**Artifact:** `src/core/performance/profiler.py`

---

### TASK X3.2 — Rule-Based Optimization Hooks (REPLACES AdaptiveOptimizer)

**Location:** `src/core/performance/profiler.py` (extend existing)
**Purpose:** Rule-based thresholds that emit EVT_DEGRADATION events.
StateMachine decides action. No auto-switching. No strategy overrides.

#### Subtask X3.2.1 — Implement rule-based profiler hooks

Rules (read-only evaluation, emit event, stop):
- p95 latency > 1000ms for a capability → emit EVT_DEGRADATION
  `{capability, metric: "latency_p95_ms", value, suggested_action: "switch_model"}`
- success_rate < 0.8 → emit EVT_DEGRADATION
  `{capability, metric: "success_rate", value, suggested_action: "inspect_capability"}`
- hot_path detection (avg < 100ms, all success) → emit EVT_HOT_PATH
  `{capability}` — StateMachine may choose to pre-warm

These are observations, not actions. StateMachine is the ONLY actor.

**Artifact:** `src/core/performance/profiler.py` (extended)

---

### TASK X3.3 — Smart Cache

**Location:** `src/core/performance/cache.py`
**Purpose:** TTL + LRU for frequent operations. Reduces latency for repeated calls.

#### Subtask X3.3.1 — Implement `SmartCache`

```python
from collections import OrderedDict

class SmartCache:
    def __init__(self, max_size: int = 100, ttl_seconds: int = 3600):
        self._cache: OrderedDict[str, tuple[Any, float]] = OrderedDict()
        self._max_size = max_size
        self._ttl = ttl_seconds
        self._hot_paths: set[str] = set()

    def mark_hot_path(self, key: str):
        """Mark a key pattern as hot path."""
        self._hot_paths.add(key)

    def get(self, key: str) -> Any | None:
        """Get cached value if not expired."""
        if key not in self._cache:
            return None

        value, timestamp = self._cache[key]

        if time.time() - timestamp > self._ttl:
            del self._cache[key]
            return None

        # Move to end (LRU)
        self._cache.move_to_end(key)
        return value

    def set(self, key: str, value: Any):
        """Cache value with TTL."""
        if len(self._cache) >= self._max_size:
            # Evict LRU (first item)
            self._cache.popitem(last=False)

        self._cache[key] = (value, time.time())

        # Hot paths get extended TTL
        if key in self._hot_paths:
            # Re-set with longer TTL
            self._cache[key] = (value, time.time())

    def clear(self):
        self._cache.clear()
```

**Artifact:** `src/core/performance/cache.py`

---

### TASK X3.4 — Benchmark Runner

**Location:** `src/core/performance/benchmark.py`
**Purpose:** Automated performance regression testing.

#### Subtask X3.4.1 — Implement `BenchmarkRunner`

```python
class BenchmarkRunner:
    def __init__(self, profiler: ExecutionProfiler):
        self._profiler = profiler
        self._baselines: dict[str, dict] = {}

    def record_baseline(self, capability: str):
        """Record current performance as baseline."""
        stats = self._profiler.get_stats(capability)
        if stats:
            self._baselines[capability] = {
                "p50_ms": stats["p50_ms"],
                "p95_ms": stats["p95_ms"],
                "success_rate": stats["success_rate"]
            }

    def check_regression(self, capability: str) -> tuple[bool, str]:
        """Check if capability performance regressed."""
        if capability not in self._baselines:
            return False, "No baseline recorded"

        current = self._profiler.get_stats(capability)
        baseline = self._baselines[capability]

        # Regression if p95 > baseline p95 * 1.5
        if current["p95_ms"] > baseline["p95_ms"] * 1.5:
            return True, f"p95 regression: {current['p95_ms']} > {baseline['p95_ms'] * 1.5}"

        # Regression if success rate drops > 10%
        if current["success_rate"] < baseline["success_rate"] - 0.1:
            return True, f"Success rate drop: {current['success_rate']} < {baseline['success_rate'] - 0.1}"

        return False, "No regression detected"

    def run_benchmark_suite(self) -> dict:
        """Run automated benchmark suite."""
        results = {}
        for cap in ["open_app", "system_info", "screenshot"]:
            has_regression, msg = self.check_regression(cap)
            results[cap] = {"regression": has_regression, "message": msg}
        return results
```

**Artifact:** `src/core/performance/benchmark.py`

---

### TASK X3.5 — Alerting + Anomaly Detection Layer

**Location:** `src/core/performance/sla_enforcer.py` (extend), new `src/core/observability/alerting.py`
**Depends on:** TASK X3.1 (`ExecutionProfiler`), TASK 1.16 (`EventBus` contract)
**Purpose:** Without proactive alerting, production failures surface only after user impact. Three signal types — latency spike, repeated capability failure, sandbox violation rate — cover the dominant failure modes. Alerts publish `EVT_THRESHOLD_ALERT` (passive, per principle 4); StateMachine decides action. No alert system modifies execution.

#### Subtask X3.5.1 — Define `AlertRule` and `AlertManager`

```python
# src/core/observability/alerting.py

from dataclasses import dataclass
from src.core.observability.event_bus import EventBus, EVT_THRESHOLD_ALERT

@dataclass
class AlertRule:
    name:        str
    metric:      str    # "latency_p95_ms" | "error_rate_pct" | "violation_count"
    threshold:   float
    window_size: int    # number of recent samples to evaluate
    severity:    str    # "warning" | "critical"

# Production defaults — override via settings.yaml
DEFAULT_ALERT_RULES: list[AlertRule] = [
    AlertRule("high_latency",     "latency_p95_ms",   500.0,  20,  "warning"),
    AlertRule("critical_latency", "latency_p95_ms",  5000.0,  10,  "critical"),
    AlertRule("high_error_rate",  "error_rate_pct",     5.0,  50,  "warning"),
    AlertRule("sandbox_abuse",    "violation_count",    3.0,  10,  "critical"),
]

class AlertManager:
    """
    PASSIVE — emits EVT_THRESHOLD_ALERT only.
    Never cancels tasks, never retries, never changes execution mode.
    StateMachine receives alert events and decides action.
    """
    def __init__(self, profiler, event_bus: EventBus,
                 rules: list[AlertRule] | None = None):
        self._profiler  = profiler
        self._bus       = event_bus
        self._rules     = rules or DEFAULT_ALERT_RULES
        self._fired:    dict[str, float] = {}   # rule_name → last_fired_timestamp
        self._cooldown_s: float = 60.0           # suppress duplicate alerts

    def evaluate(self, capability: str) -> list[dict]:
        """
        Called by ExecutionProfiler.record() after every execution.
        Returns list of fired alerts (for logging). Side-effect: publishes events.
        """
        stats  = self._profiler.get_stats(capability)
        if not stats:
            return []
        fired = []
        now = __import__("time").time()
        for rule in self._rules:
            value = self._extract_metric(stats, rule.metric)
            if value is None:
                continue
            if value > rule.threshold:
                key = f"{rule.name}:{capability}"
                if now - self._fired.get(key, 0) > self._cooldown_s:
                    self._fired[key] = now
                    alert = {
                        "rule":       rule.name,
                        "capability": capability,
                        "metric":     rule.metric,
                        "value":      value,
                        "threshold":  rule.threshold,
                        "severity":   rule.severity,
                    }
                    self._bus.publish(
                        EVT_THRESHOLD_ALERT, alert,
                        source="alert_manager"
                    )
                    fired.append(alert)
        return fired

    def _extract_metric(self, stats: dict, metric: str) -> float | None:
        mapping = {
            "latency_p95_ms":  stats.get("p95_ms"),
            "error_rate_pct":  (1 - stats.get("success_rate", 1)) * 100,
            "violation_count": stats.get("violation_count", 0),
        }
        return mapping.get(metric)
```

#### Subtask X3.5.2 — Wire AlertManager into ExecutionProfiler

```python
# src/core/performance/profiler.py — extend record()

class ExecutionProfiler:
    def __init__(self, alert_manager=None):
        ...
        self._alert_manager = alert_manager   # injected; None = no alerting

    def record(self, capability: str, latency_ms: float,
               success: bool, risk_level: str) -> None:
        ...
        # existing hot-path logic
        ...
        # NEW: evaluate alerts after every write
        if self._alert_manager:
            self._alert_manager.evaluate(capability)
```

#### Subtask X3.5.3 — Add `violation_count` tracking to profiler

```python
# In ExecutionProfiler — track CapabilityViolationEvent
def record_violation(self, capability: str) -> None:
    """Called by RuntimeValidator on scope violation."""
    if capability not in self._metrics:
        self._metrics[capability] = []
    # piggyback violation into existing stats
    self._metrics[capability].append({
        "latency_ms": 0, "success": False,
        "risk_level": "high", "timestamp": time.time(),
        "violation": True
    })
    if self._alert_manager:
        self._alert_manager.evaluate(capability)

def get_stats(self, capability: str) -> dict:
    ...
    # extend existing return dict
    entries  = self._metrics.get(capability, [])
    violations = sum(1 for e in entries if e.get("violation"))
    return {
        ...existing fields...,
        "violation_count": violations,
    }
```

#### Subtask X3.5.4 — Test coverage (4 tests)

Add to `tests/test_performance.py`:

```python
def test_alert_fires_on_high_latency():
    from src.core.performance.profiler import ExecutionProfiler
    from src.core.observability.alerting import AlertManager, AlertRule
    from src.core.observability.event_bus import EventBus, EVT_THRESHOLD_ALERT
    bus  = EventBus()
    alerts = []
    bus.subscribe(EVT_THRESHOLD_ALERT, alerts.append)
    rule = AlertRule("test_latency", "latency_p95_ms", 100.0, 5, "warning")
    am   = AlertManager(None, bus, [rule])  # profiler injected below
    prof = ExecutionProfiler(alert_manager=am)
    am._profiler = prof
    for _ in range(10):
        prof.record("open_app", latency_ms=999.0, success=True, risk_level="low")
    assert any(a.payload["rule"] == "test_latency" for a in alerts)

def test_alert_cooldown_suppresses_duplicates():
    from src.core.performance.profiler import ExecutionProfiler
    from src.core.observability.alerting import AlertManager, AlertRule
    from src.core.observability.event_bus import EventBus, EVT_THRESHOLD_ALERT
    bus, alerts = EventBus(), []
    bus.subscribe(EVT_THRESHOLD_ALERT, alerts.append)
    rule = AlertRule("dup_test", "latency_p95_ms", 50.0, 5, "warning")
    am   = AlertManager(None, bus, [rule])
    am._cooldown_s = 9999  # force cooldown active
    prof = ExecutionProfiler(alert_manager=am)
    am._profiler = prof
    for _ in range(20):
        prof.record("open_app", 999.0, True, "low")
    # Despite many breaches, only 1 alert fires per cooldown window
    rule_alerts = [a for a in alerts if a.payload["rule"] == "dup_test"]
    assert len(rule_alerts) == 1

def test_violation_count_increments_on_record_violation():
    from src.core.performance.profiler import ExecutionProfiler
    prof = ExecutionProfiler()
    prof.record_violation("file_ops")
    prof.record_violation("file_ops")
    assert prof.get_stats("file_ops")["violation_count"] == 2

def test_alert_manager_is_passive_no_side_effects():
    """AlertManager must NOT modify any execution state."""
    from src.core.performance.profiler import ExecutionProfiler
    from src.core.observability.alerting import AlertManager
    from src.core.observability.event_bus import EventBus
    prof = ExecutionProfiler()
    am   = AlertManager(prof, EventBus())
    # After evaluation, no state change on profiler internals beyond metrics
    before = dict(prof._metrics)
    am.evaluate("nonexistent_cap")
    assert prof._metrics == before
```

**Artifacts:** `src/core/observability/alerting.py`, updated `src/core/performance/profiler.py`, `tests/test_performance.py`

**Definition of Done:**
- [ ] `AlertManager` is passive: emits `EVT_THRESHOLD_ALERT` only
- [ ] 3 default rules: `latency_p95_ms`, `error_rate_pct`, `violation_count`
- [ ] 60s cooldown prevents alert storms
- [ ] `record_violation()` feeds `violation_count` into stats
- [ ] `AlertManager` wired into `ExecutionProfiler` via injection (not hard-dependency)
- [ ] All 4 new tests pass

---

### Definition of Done — Phase X3

- [ ] `ExecutionProfiler` records per-capability metrics
- [ ] Rule-based profiler emits EVT_DEGRADATION on threshold breach — StateMachine decides
- [ ] `SmartCache` reduces latency for hot paths
- [ ] `BenchmarkRunner` detects performance regressions
- [ ] All capabilities have performance baselines
- [ ] AlertManager passive: emits EVT_THRESHOLD_ALERT only — StateMachine decides action
- [ ] 3 default alert rules with configurable thresholds + 60s cooldown
- [ ] violation_count tracked in ExecutionProfiler stats
- [ ] All 4 alerting tests pass
- [ ] `src/core/performance/optimizer.py` does NOT exist

---

## Phase 10 — Prompt Builder

```yaml
phase_id: 10
priority: "P1"
status: "not_started"
total_tasks: 5
blocker: "Phase 9 complete"
next_action: "TASK 10.1"
```

### Theoretical Foundation

The system prompt is JARVIS's primary behaviour control surface. Separating prompt content into four independent concerns — identity, mode fragment, context, history — allows each to be tuned and tested independently. Arabic language detection adds a language hint without requiring separate Arabic-only model variants.

### TASK 10.1 — Jarvis Identity YAML

**Location:** `config/runtime/jarvis_identity.yaml`

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

Exactly 5 fragments matching `ExecutionMode` enum values: `fast`, `normal`, `deep`, `planning`, `research`.

Each entry has: `system_addition` (instruction text), `output_format` (format guidance), `behavior` (depth description).

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
**Purpose:** Assembles system prompt from 5 independent blocks: identity, mode fragment, context (memory snippets), history (last 3 turns), language hint.

#### Subtask 10.3.1 — Load YAML files with `@lru_cache(maxsize=1)`

Both `jarvis_identity.yaml` and `mode_fragments.yaml` loaded once at process start. Cache invalidated only on reload.

#### Subtask 10.3.2 — Implement `PromptBuilder.build(decision, input_packet) → str`

Block assembly:

1. **Identity:** `"You are {name} v{version}, {role}. Constraints: {'; '.join(constraints)}."`
2. **Mode fragment:** `fragments[decision.mode.value]['system_addition']`
3. **Context block:** if `input_packet.memory_snippets` → `"Relevant context:\n- {content}"` (top 3)
4. **History block:** if `input_packet.recent_history` → last 3 turns as `"User: ...\nJARVIS: ..."`
5. **Language hint:** if `user_profile.language == "ar"` → `"Always respond in Arabic. Use formal Modern Standard Arabic."`

Join non-empty blocks with `"\n\n"`.

**Artifact:** `src/core/context/builder.py`

---

### TASK 10.4 — Wire PromptBuilder into Executor

**Location:** `src/core/runtime/executor.py`
**Purpose:** Replace the Phase 4 stub string `"You are JARVIS."` with live `PromptBuilder.build()` output.

```python
# In Executor.__init__
from src.core.context.builder import PromptBuilder
self._prompt_builder = PromptBuilder()

# In Executor.execute()
system_prompt = self._prompt_builder.build(decision, input_packet)
# Use system_prompt in OllamaEngine.chat_with_model() call
```

**Artifact:** Updated `src/core/runtime/executor.py`

---

### TASK 10.5 — Identity Enforcement Tests (7 tests)

**Location:** `tests/test_identity_enforcement.py`

Required tests:

1. `build()` output contains `"JARVIS"`
2. `fast` mode → prompt contains fast fragment text
3. `deep` mode → prompt contains deep fragment text
4. `language=ar` → prompt contains "Arabic"
5. Non-empty `memory_snippets` → prompt contains context block
6. Non-empty `recent_history` → prompt contains prior turn text
7. All 5 modes produce 5 distinct non-empty prompts

```bash
pytest tests/test_identity_enforcement.py -v
# Expected: 7 passed
```

**Artifact:** `tests/test_identity_enforcement.py`

### Definition of Done — Phase 10

- [ ] Both YAML files created with correct keys
- [ ] `PromptBuilder.build()` produces distinct output for all 5 modes
- [ ] Arabic hint present when `profile.language == "ar"`
- [ ] `Executor` uses `PromptBuilder` (not hardcoded stub string)
- [ ] `pytest tests/test_identity_enforcement.py -v` → 7 passed

---

## Phase 11 — Execution Hardening

```yaml
phase_id: 11
priority: "P0"
status: "not_started"
total_tasks: 6
blocker: "Phase 10 complete"
next_action: "TASK 11.1"
```

### Theoretical Foundation

Production readiness means handling every failure mode gracefully. Phase 11 adds four resilience mechanisms: timeout enforcement (every phase has a hard deadline), degradation (model failures trigger tier-1 then tier-2 fallback), retry budgeting (prevents infinite loops), and decision validation (rejects structurally incoherent decisions before they reach the executor). After Phase 11, `run_turn()` is unconditionally safe — it can never raise an uncaught exception.

### TASK 11.1 — Timeout Handler

**Location:** `src/core/runtime/timeout.py`
**Purpose:** Per-phase deadline enforcement. Raises `TurnTimeoutError` when a phase exceeds its configured limit.

#### Subtask 11.1.1 — Implement `TimeoutHandler` with context manager

```python
class TimeoutHandler(Limits):
    _PHASE_MAP = {
        "tool": "tool_timeout_s", "step": "step_timeout_s",
        "model": "model_timeout_s", "turn": "total_turn_timeout_s",
    }

    def check(self, phase: str, start_time: float) -> None:
        threshold = getattr(self, self._PHASE_MAP[phase])
        if time.time() - start_time >= threshold:
            EventBus().publish(EVT_DEGRADATION, {"phase": phase})
            raise TurnTimeoutError(f"Phase '{phase}' timeout")

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

### TASK 11.2 — Graceful Degradation Handler

**Location:** `src/core/runtime/degradation.py`
**Purpose:** Model and tool failure handler. Maintains ordered fallback chain: primary → tier_1 → tier_2 → None (exhausted).

#### Subtask 11.2.1 — Implement `DegradationHandler`

- `handle_model_failure(model, error) → str | None`: returns next fallback model or None if exhausted. Logs error, publishes `EVT_DEGRADATION`, marks `_degraded=True`.
- `handle_tool_failure(tool, error)`: logs warning; publishes `EVT_SAFETY_BLOCK` if `PermissionDeniedError`.
- `generate_error_response(error_type, detail="") → str`: returns user-friendly message for `model_unavailable`, `timeout`, `permission_denied`, `budget_exhausted`, `unknown`.
- `is_degraded() → bool`

**Artifact:** `src/core/runtime/degradation.py`

---

### TASK 11.3 — Tiered Fallback System

**Location:** `src/core/runtime/fallback.py`
**Purpose:** Forces a specific fallback model when primary model fails. Always returns `FinalResponse` with `degraded=True`.

#### Subtask 11.3.1 — Implement `FallbackSystem.attempt(packet, tier, decision, turn_id)`

- `tier=1`: force `decision.model = tier_1`, call `Executor().execute()`
- `tier=2`: force `decision.model = tier_2`, call `Executor().execute()`
- Any exception in attempt → `FinalResponse.error_response()`

Tier 1 always tried before tier 2.

**Artifact:** `src/core/runtime/fallback.py`

---

### TASK 11.4 — Central Retry Manager (Global)

**Location:** `src/core/runtime/retry.py` (update)
**Depends on:** Phase 2 `load_config()`
**Purpose:** Centralized retry management with global budget. Replaces scattered retry logic.

#### Subtask 11.4.1 — Implement global retry config

```yaml
# config/runtime/settings.yaml
execution:
  mode: "BALANCED"
  max_iterations: 5
  total_turn_timeout_s: 120
  global_retry_budget: 3
  backoff_strategy: "exponential"
  base_backoff_ms: 1000
  max_backoff_ms: 30000

execution_mode:
  deterministic:
    parallelism: disabled
    ordering: strict
  performance:
    parallelism: enabled
    ordering: relaxed

sla:
  fast: 100
  medium: 500
  heavy: 5000

cache:
  ttl: dynamic
  eviction: LRU
```

#### Subtask 11.4.2 — Update `RetryManager`

```python
class RetryManager:
    def __init__(self):
        config = load_config().execution
        self._initial = config.global_retry_budget  # 3
        self._budget = self._initial
        self.backoff = config.backoff_strategy  # exponential
        self.base_backoff_ms = config.base_backoff_ms  # 1000
        self.max_backoff_ms = config.max_backoff_ms  # 30000

    def consume(self, n: int = 1) -> int:
        self._budget = max(0, self._budget - n)
        return self._budget

    def can_retry(self) -> bool:
        return self._budget > 0

    def get_backoff_ms(self, attempt: int) -> float:
        if self.backoff == "exponential":
            return min(self.base_backoff_ms * (2 ** attempt), self.max_backoff_ms)
        return self.base_backoff_ms

    def reset(self) -> None:
        self._budget = self._initial
```

**Artifact:** Updated `src/core/runtime/retry.py`

---

### TASK 11.5 — Decision Validation Enforcer

**Location:** `src/core/runtime/validate_decision.py`
**Purpose:** Structural validation of `DecisionOutput` before execution begins. Returns `False` to trigger immediate `_safe_default()` — no retry.

#### Subtask 11.5.1 — Implement `DecisionEnforcer.validate()`

Checks:

1. `decision_source==model` → `score_breakdown` non-empty AND `candidate_list` non-empty → return False if missing
2. `ModelAvailability().is_available(decision.model)` → log WARNING and return False if unavailable
3. `confidence < 0.3` → log WARNING but return True (low confidence is valid data, not an error)

**Artifact:** `src/core/runtime/validate_decision.py`

---

### TASK 11.6 — Integration Tests (10 tests)

**Location:** `tests/test_integration.py`

Required tests:

1. `run_turn("hello", "s1")` → `FinalResponse` with non-empty text
2. `run_turn("open notepad", "s1")` → fast path decision used
3. Mock model failure → returns degraded `FinalResponse` (no crash)
4. Mock all models fail → fallback chain activates tier_1 first
5. Mock all models fail always → budget exhausted → degraded `FinalResponse`
6. `run_turn("delete /etc/passwd", "s1")` → blocked, no crash
7. Two sequential turns → second turn has `recent_history` from first
8. All state transitions published to EventBus
9. SAFE mode → `EVT_WAITING_CONFIRMATION` published for tool actions
10. `run_turn()` never raises uncaught exception under any failure mode

```bash
pytest tests/test_integration.py -v
# Expected: 10 passed
```

**Artifact:** `tests/test_integration.py`

### Definition of Done — Phase 11

- [ ] `phase_timeout()` context manager raises `TurnTimeoutError` on expiry
- [ ] `DegradationHandler` returns tier-1 then tier-2 in order, then None
- [ ] `RetryManager.can_retry()` returns False when budget reaches 0
- [ ] `run_turn()` never raises under any failure mode
- [ ] `pytest tests/test_integration.py -v` → 10 passed

---

## Phase 12 — CLI Interface

```yaml
phase_id: 12
priority: "P2"
status: "not_started"
total_tasks: 3
blocker: "Phase 11 complete"
next_action: "TASK 12.1"
```

### Theoretical Foundation

The CLI is a thin display adapter. It converts raw user input into `run_turn()` calls and renders `FinalResponse` to the terminal. Zero business logic lives here. The "thinking" indicator provides feedback during LLM latency. Session ID is generated once per CLI session and reused across all turns to enable history retrieval.

### TASK 12.1 — CLI Chat Loop

**Location:** `src/interfaces/cli/chat.py`
**Purpose:** Main REPL loop. Handles startup banner, input reading, command dispatch, thinking indicator, and graceful shutdown.

#### Subtask 12.1.1 — Implement `CLIChat.start()`

```python
import uuid
from src.core.runtime.loop import run_turn

class CLIChat:
    BANNER = "JARVIS v3.0 — type /help for commands, Ctrl+C to quit"

    def start(self) -> None:
        print(self.BANNER)
        session_id = str(uuid.uuid4())
        handler = CommandHandler()
        formatter = CLIFormatter()
        from app.main import _shutdown

        while not _shutdown:
            try:
                user_input = input("\nYou: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye.")
                break

            if not user_input:
                continue

            if user_input.startswith("/"):
                handler.handle(user_input, session_id)
                continue

            print("Thinking...", end="\r", flush=True)
            response = run_turn(user_input, session_id)
            print(" " * 12, end="\r")  # clear thinking indicator
            print(f"JARVIS: {formatter.format_response(response)}")
```

**Artifact:** `src/interfaces/cli/chat.py`

---

### TASK 12.2 — CLI Command Handlers

**Location:** `src/interfaces/cli/commands.py`
**Purpose:** Handles all `/commands`. All commands are case-insensitive.

#### Subtask 12.2.1 — Implement `CommandHandler.handle()`

| Command                              | Action                                                                                              |
| :----------------------------------- | :-------------------------------------------------------------------------------------------------- |
| `/help`                              | Print all available commands                                                                        |
| `/mode SAFE\|BALANCED\|UNRESTRICTED` | Validate and update execution mode via `update_mode()`. Print error on invalid value.               |
| `/replay [turn_id]`                  | Print turn history from `MemoryDB.retrieve_recent()`. If `turn_id` given, print that specific turn. |
| `/debug`                             | Toggle DEBUG log level                                                                              |
| `/status`                            | Print current model, mode, VRAM, turn count from `MetricsCollector`                                 |
| `/quit`                              | Set `_shutdown = True`, print "Goodbye."                                                            |

**Artifact:** `src/interfaces/cli/commands.py`

---

### TASK 12.3 — CLI Formatting

**Location:** `src/interfaces/cli/formatting.py`
**Purpose:** Terminal output with colour, degradation indicators, and Arabic RTL support.

#### Subtask 12.3.1 — Implement `CLIFormatter`

```python
from colorama import Fore, Style, init
init(autoreset=True)

class CLIFormatter:
    def format_response(self, response: FinalResponse) -> str:
        prefix = f"{Fore.YELLOW}[DEGRADED]{Style.RESET_ALL} " if response.degraded else ""
        text = response.text
        # Prepend RTL mark for Arabic content
        if self._is_arabic(text):
            text = "\u200f" + text
        return f"{prefix}{text}"

    def format_tool_result(self, result: ToolResult) -> str:
        if result.success:
            return f"{Fore.GREEN}✓{Style.RESET_ALL} {result.tool}: {result.data}"
        return f"{Fore.RED}✗{Style.RESET_ALL} {result.tool}: {result.error}"

    def _is_arabic(self, text: str) -> bool:
        return any('\u0600' <= c <= '\u06ff' for c in text)
```

**Artifact:** `src/interfaces/cli/formatting.py`

### Definition of Done — Phase 12

- [ ] `python app/main.py --interface cli` prints banner, accepts input, shows responses
- [ ] All `/commands` functional
- [ ] Arabic text preceded by RTL mark `\u200f`
- [ ] Ctrl+C exits cleanly with code 0

---

## Phase 13 — Web Automation & Browser

```yaml
phase_id: 13
priority: "P2"
status: "not_started"
total_tasks: 3
blocker: "Phase 12 complete"
next_action: "TASK 13.1"
```

**Directory note:** `src/capabilities/web/` — NOT `web_automation/`.

### TASK 13.1 — Browser Capability (`browser`)

**Location:** `src/capabilities/web/browser.py`
**Depends on:** Phase 8 `BaseCapability`, Playwright

**Input:** `{"action": "navigate"|"click"|"type"|"screenshot"|"extract_text", "url": str?, "selector": str?, "text": str?}`

#### Subtask 13.1.1 — Implement Playwright lifecycle management

```python
from playwright.sync_api import sync_playwright

class BrowserCapability(BaseCapability):
    name = "browser"
    domain = "web"
    description = "Automate browser via Playwright"

    def __init__(self):
        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(headless=False)
        self._page = self._browser.new_page()

    def __del__(self):
        try:
            self._browser.close()
            self._playwright.stop()
        except Exception:
            pass
```

#### Subtask 13.1.2 — Implement each action

| Action         | Implementation                        | Output data                                |
| :------------- | :------------------------------------ | :----------------------------------------- |
| `navigate`     | `page.goto(url, timeout=30000)`       | `{"url": page.url, "title": page.title()}` |
| `click`        | `page.click(selector)`                | `{"clicked": selector}`                    |
| `type`         | `page.fill(selector, text)`           | `{"typed": True}`                          |
| `screenshot`   | `page.screenshot(path=save_path)`     | `{"path": str(save_path)}`                 |
| `extract_text` | `page.inner_text(selector or "body")` | `{"text": content}`                        |

Screenshot save path: `data/screenshots/browser_{uuid4()[:8]}.png`

**Dry-run:** `{"would_execute": action, "url": args.get("url")}`

**Artifact:** `src/capabilities/web/browser.py`

---

### TASK 13.2 — Web Session Manager

**Location:** `src/capabilities/web/session.py`
**Purpose:** Manages isolated browser contexts (separate cookies, localStorage per session). Session IDs are UUIDs.

#### Subtask 13.2.1 — Implement `WebSessionManager`

- `create_session(browser) → (session_id: str, context: BrowserContext)` — UUID keyed
- `get_session(session_id) → BrowserContext | None`
- `close_session(session_id) → None` — calls `context.close()`
- `list_sessions() → list[str]`

**Artifact:** `src/capabilities/web/session.py`

---

### TASK 13.3 — Web Automation Tests (5 tests)

**Location:** `tests/test_web_automation.py`

Required tests (mock Playwright or use `pytest-playwright`):

1. Navigate action returns page title
2. Screenshot action returns valid file path string
3. Extract text action returns non-empty string
4. Session create → get → close lifecycle
5. Playwright timeout → `ToolResult.failure`

**Artifact:** `tests/test_web_automation.py`

### Definition of Done — Phase 13

- [ ] `BrowserCapability` executes all 5 actions
- [ ] Session manager creates and closes isolated contexts
- [ ] All 5 tests pass

---

## Phase 14 — Google APIs

```yaml
phase_id: 14
priority: "P2"
status: "not_started"
total_tasks: 4
blocker: "Phase 13 complete"
next_action: "TASK 14.1"
```

### Theoretical Foundation

Google services are passive data connectors — they provide data to capabilities, never execute actions themselves. OAuth2 credentials live in `config/env/.env`. Missing credentials raise `PermissionDeniedError` immediately on `authenticate()` — no silent degradation.

### TASK 14.1 — Google Auth Service

**Location:** `src/services/google/auth.py`

#### Subtask 14.1.1 — Implement `GoogleAuth`

- `authenticate(credentials_path: str) → Credentials`
  - Load credentials from `credentials_path` (OAuth2 JSON file)
  - If file missing → `PermissionDeniedError("Google credentials not configured")`
  - Load/refresh token from `data/profiles/google_token.json`
  - Scopes: `['https://www.googleapis.com/auth/calendar', 'https://mail.google.com/', 'https://www.googleapis.com/auth/drive']`
- `get_credentials() → Credentials` — cached; refresh if expired

**Artifact:** `src/services/google/auth.py`

---

### TASK 14.2 — Google Calendar Service

**Location:** `src/services/google/calendar.py`

#### Subtask 14.2.1 — Implement Calendar operations

- `list_events(start: str, end: str) → list[dict]` — ISO8601 datetime strings
- `create_event(summary: str, start: str, end: str, description: str = "") → dict`
- `delete_event(event_id: str) → None`

All `googleapiclient.errors.HttpError` → `JarvisError` with user-friendly message.

**Artifact:** `src/services/google/calendar.py`

---

### TASK 14.3 — Gmail Service

**Location:** `src/services/google/gmail.py`

#### Subtask 14.3.1 — Implement Gmail operations

- `list_messages(query: str, max_results: int = 10) → list[dict]`
- `get_message(message_id: str) → dict` — returns `{subject, from, date, body}`
- `send_message(to: str, subject: str, body: str) → dict` — returns `{id, status}`

**Artifact:** `src/services/google/gmail.py`

---

### TASK 14.4 — Google Drive Service

**Location:** `src/services/google/drive.py`

#### Subtask 14.4.1 — Implement Drive operations

- `list_files(query: str = "", max_results: int = 10) → list[dict]`
- `download_file(file_id: str, destination: str) → str` — returns local path
- `upload_file(name: str, content: bytes, mime_type: str) → dict`

**Artifact:** `src/services/google/drive.py`

### Definition of Done — Phase 14

- [ ] `GoogleAuth.authenticate()` raises `PermissionDeniedError` on missing credentials
- [ ] Calendar, Gmail, Drive services wrap all `HttpError` into `JarvisError`
- [ ] No credentials committed to version control

---

## Phase 14.5 — Telegram Integration

```yaml
phase_id: "14.5"
priority: "P2"
status: "not_started"
total_tasks: 3
blocker: "Phase 14 complete"
next_action: "TASK 14.5.1"
```

### TASK 14.5.1 — Telegram Bot Service

**Location:** `src/interfaces/telegram/bot.py`
**Purpose:** Async message handler that routes Telegram messages through `run_turn()` via `asyncio.to_thread`.

#### Subtask 14.5.1 — Implement `TelegramBot`

```python
import asyncio

class TelegramBot:
    def __init__(self, run_turn_fn):
        self._run_turn = run_turn_fn
        token = os.environ.get("TELEGRAM_BOT_TOKEN")
        if not token:
            logger.error("TELEGRAM_BOT_TOKEN not set. Telegram integration disabled.")
            self._app = None
            return
        from telegram.ext import Application
        self._app = Application.builder().token(token).build()

    async def handle_message(self, update, context) -> None:
        user_input = update.message.text
        session_id = f"telegram_{update.effective_user.id}"
        response = await asyncio.to_thread(self._run_turn, user_input, session_id)
        await update.message.reply_text(response.text)

    def start(self) -> None:
        if self._app is None:
            return
        from telegram.ext import MessageHandler, filters
        self._app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        self._app.run_polling()
```

**Artifact:** `src/interfaces/telegram/bot.py`

---

### TASK 14.5.2 — Telegram Command Handlers

**Location:** `src/interfaces/telegram/commands.py`

| Command                              | Action                                                  |
| :----------------------------------- | :------------------------------------------------------ |
| `/start`                             | Reply with JARVIS version and available commands        |
| `/mode SAFE\|BALANCED\|UNRESTRICTED` | Validate mode, call `update_mode()`, reply confirmation |
| `/status`                            | Reply with current model, mode, turn count              |
| `/quit`                              | Reply "Goodbye." — bot continues for other users        |

**Artifact:** `src/interfaces/telegram/commands.py`

---

### TASK 14.5.3 — Telegram Tests (5 tests)

**Location:** `tests/test_telegram.py`

Required tests (mock `Application`):

1. `handle_message` calls `run_turn` with correct args
2. Response text sent to chat via `reply_text`
3. `/mode SAFE` updates mode and replies with confirmation
4. Missing token → no crash, bot disabled gracefully
5. `run_turn` failure → degraded response sent, not exception propagated

**Artifact:** `tests/test_telegram.py`

### Definition of Done — Phase 14.5

- [ ] Missing `TELEGRAM_BOT_TOKEN` → log ERROR, no crash
- [ ] `handle_message` routes to `run_turn()` via `asyncio.to_thread`
- [ ] All 5 tests pass

---

## Phase 15 — Web UI

```yaml
phase_id: 15
priority: "P2"
status: "not_started"
total_tasks: 3
blocker: "Phase 14.5 complete"
next_action: "TASK 15.1"
```

**Directory note:** `src/interfaces/web_ui/` — underscore, not space.

### TASK 15.1 — Web UI Backend

**Location:** `src/interfaces/web_ui/app.py`
**Purpose:** FastAPI backend exposing REST and WebSocket endpoints. WebSocket streams `EVT_STATE_TRANSITION` events to the client in real time.

#### Subtask 15.1.1 — Implement FastAPI app with 5 endpoints

```python
from fastapi import FastAPI, WebSocket
from src.core.runtime.loop import run_turn
import uvicorn

app = FastAPI(title="JARVIS Web UI")

@app.post("/chat")
async def chat(body: dict):
    import asyncio
    response = await asyncio.to_thread(run_turn, body["message"], body.get("session_id","default"))
    return response.model_dump()

@app.get("/history/{session_id}")
async def history(session_id: str):
    from src.memory.database import MemoryDB
    return MemoryDB().retrieve_recent(session_id, limit=20)

@app.get("/status")
async def status():
    from src.models.manager import ModelManager
    from src.models.vram_monitor import VRAMMonitor
    from src.core.config import load_config
    return {
        "model": ModelManager().get_current_model(),
        "mode": load_config().execution.mode,
        "vram_available_mb": VRAMMonitor().get_available_vram_mb(),
    }

@app.post("/mode")
async def set_mode(body: dict):
    from src.memory.user_profile import update_mode
    mode = body.get("mode", "BALANCED")
    if mode not in ("SAFE", "BALANCED", "UNRESTRICTED"):
        return {"error": f"Invalid mode: {mode}"}
    update_mode("default", mode)
    return {"mode": mode}

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    from src.core.observability.event_bus import EventBus, EVT_STATE_TRANSITION, EVT_TURN_COMPLETE
    await websocket.accept()

    loop = asyncio.get_event_loop()

    def on_event(env):
        # thread-safe: schedule send_event on the websocket's event loop
        asyncio.run_coroutine_threadsafe(send_event(env), loop)

    async def send_event(env):
        try:
            payload = env.payload if hasattr(env, 'payload') else env
            await websocket.send_json(payload)
        except Exception:
            pass

    bus = EventBus()
    bus.subscribe(EVT_STATE_TRANSITION, on_event)
    bus.subscribe(EVT_TURN_COMPLETE, on_event)
    try:
        while True:
            await websocket.receive_text()  # keep alive
    except Exception:
        pass

class WebApp:
    def start(self, host: str = "0.0.0.0", port: int = 8000):
        uvicorn.run(app, host=host, port=port)
```

**Artifact:** `src/interfaces/web_ui/app.py`

---

### TASK 15.2 — Web UI Frontend

**Location:** `src/interfaces/web_ui/static/index.html`
**Purpose:** Single-file SPA. No build step, no CDN. Vanilla HTML/CSS/JS.

#### Subtask 15.2.1 — Implement SPA features

- Chat message display (user + JARVIS bubbles)
- WebSocket client connecting to `/ws/{session_id}`
- Input field with `dir="auto"` for Arabic input
- Mode dropdown (`SAFE`, `BALANCED`, `UNRESTRICTED`) calling `POST /mode`
- Status bar showing model name and current mode
- State event display (show `EVT_STATE_TRANSITION` events as status updates)
- No external CDN dependencies — all styling inline

**Artifact:** `src/interfaces/web_ui/static/index.html`

---

### TASK 15.3 — Web UI Tests (5 tests)

**Location:** `tests/test_web_ui.py`

Required tests (using `httpx.AsyncClient` + `ASGITransport`):

1. `POST /chat` returns JSON with `text` field
2. `GET /history/{session_id}` returns list
3. `GET /status` returns `model`, `mode`, `vram_available_mb`
4. `POST /mode` with `"SAFE"` updates mode and returns `{"mode":"SAFE"}`
5. WebSocket connects and receives at least one event after a chat call

**Artifact:** `tests/test_web_ui.py`

### Definition of Done — Phase 15

- [ ] `python app/main.py --interface web` starts FastAPI on port 8000
- [ ] All 5 REST/WS endpoints functional
- [ ] Frontend loads and sends chat messages without build step
- [ ] All 5 tests pass

---

## Phase 16 — Voice Pipeline

```yaml
phase_id: 16
priority: "P3"
status: "not_started"
total_tasks: 4
blocker: "Phase 15 complete"
next_action: "TASK 16.1"
```

### Theoretical Foundation

Voice I/O is implemented as capabilities (`stt`, `tts`) within the existing capability framework. `WakeWordDetector` is NOT a capability — it is a continuous background listener that cannot be modelled as a discrete action with input/output. It is a service-like object that fires a callback when the wake word is detected, triggering `run_turn()` in the CLI loop.

### TASK 16.1 — STT Capability (`stt`)

**Location:** `src/capabilities/voice/stt.py`

**Input:** `{"audio_path": str?}` — if None, record 5s from microphone
**Output:** `ToolResult(success=True, data={"text": str, "language": str})`

#### Subtask 16.1.1 — Implement Whisper-based transcription

```python
# Lazy load — import whisper on first call only
def _get_model():
    try:
        import whisper
        return whisper.load_model("base")
    except ImportError:
        return None

class STTCapability(BaseCapability):
    name = "stt"
    domain = "voice"
    description = "Transcribe speech to text using OpenAI Whisper"

    def execute(self, args: dict) -> ToolResult:
        try:
            model = _get_model()
            if model is None:
                return ToolResult.failure(self.name, "openai-whisper not installed")

            audio_path = args.get("audio_path")
            if audio_path is None:
                audio_path = self._record_from_mic()
                if audio_path is None:
                    return ToolResult.failure(self.name, "microphone not available")

            result = model.transcribe(str(audio_path))
            return ToolResult.success_result(self.name,
                {"text": result["text"].strip(), "language": result["language"]})
        except FileNotFoundError:
            return ToolResult.failure(self.name, f"audio file not found: {args.get('audio_path')}")
        except Exception as e:
            return ToolResult.failure(self.name, str(e))
```

#### Subtask 16.1.2 — Implement `_record_from_mic()`

```python
def _record_from_mic(self, duration_s: int = 5) -> str | None:
    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source, timeout=duration_s)
        tmp = tempfile.mktemp(suffix=".wav")
        with open(tmp, "wb") as f:
            f.write(audio.get_wav_data())
        return tmp
    except Exception:
        return None
```

**Artifact:** `src/capabilities/voice/stt.py`

---

### TASK 16.2 — TTS Capability (`tts`)

**Location:** `src/capabilities/voice/tts.py`

**Input:** `{"text": str, "voice": str?}` (voice defaults to `"en_US-lessac-medium"`)
**Output:** `ToolResult(success=True, data={"audio_path": str})`

#### Subtask 16.2.1 — Implement Piper TTS synthesis

```python
import subprocess, tempfile
from pathlib import Path

class TTSCapability(BaseCapability):
    name = "tts"
    domain = "voice"
    description = "Synthesize speech using Piper TTS"

    DEFAULT_VOICE = "en_US-lessac-medium"
    ARABIC_VOICE  = "ar_JO-kareem-medium"

    def execute(self, args: dict) -> ToolResult:
        try:
            text  = args["text"]
            voice = args.get("voice", self.DEFAULT_VOICE)
            Path("data/audio").mkdir(parents=True, exist_ok=True)
            output = f"data/audio/{uuid.uuid4()}.wav"
            result = subprocess.run(
                ["piper", "--model", voice, "--output_file", output],
                input=text.encode(), capture_output=True, timeout=30
            )
            if result.returncode != 0:
                return ToolResult.failure(self.name, result.stderr.decode())
            # Play audio platform-specifically
            self._play(output)
            return ToolResult.success_result(self.name, {"audio_path": output})
        except FileNotFoundError:
            return ToolResult.failure(self.name, "piper-tts not installed")
        except subprocess.TimeoutExpired:
            return ToolResult.failure(self.name, "TTS synthesis timed out")
        except Exception as e:
            return ToolResult.failure(self.name, str(e))

    def _play(self, path: str) -> None:
        import sys
        if sys.platform == "win32":
            subprocess.Popen(["start", path], shell=True)
        elif sys.platform == "darwin":
            subprocess.Popen(["afplay", path])
        else:
            subprocess.Popen(["aplay", path])
```

**Artifact:** `src/capabilities/voice/tts.py`

---

### TASK 16.3 — Wake Word Detector

**Location:** `src/capabilities/voice/wake_word.py`
**Purpose:** Continuous background listener. NOT a `BaseCapability`. Runs in daemon thread, fires callback when wake word detected.

#### Subtask 16.3.1 — Implement `WakeWordDetector`

```python
import threading
import speech_recognition as sr

class WakeWordDetector:
    def __init__(self):
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

    def listen_for_wake_word(self, wake_word: str, callback) -> None:
        """Start background listener thread. Returns immediately."""
        self._stop.clear()
        self._thread = threading.Thread(
            target=self._listen_loop, args=(wake_word.lower(), callback), daemon=True
        )
        self._thread.start()

    def _listen_loop(self, wake_word: str, callback) -> None:
        """
        Local wake word detection using offline recognition only.
        No external API calls — local-first principle enforced.
        """
        r = sr.Recognizer()
        while not self._stop.is_set():
            try:
                with sr.Microphone() as source:
                    audio = r.listen(source, timeout=3, phrase_time_limit=3)
                text = self._recognize_locally(r, audio)
                if text and wake_word in text:
                    callback(text)
            except Exception:
                pass

    def _recognize_locally(self, recognizer, audio) -> str | None:
        """
        Attempt local recognition in priority order:
        1. Vosk (offline, fast, accurate)
        2. CMU Sphinx (offline, lightweight)
        3. Return None if neither available — no fallback to online services
        """
        try:
            return recognizer.recognize_vosk(audio).lower()
        except Exception:
            pass
        try:
            return recognizer.recognize_sphinx(audio).lower()
        except Exception:
            pass
        return None  # never call recognize_google or any online service

    def stop(self) -> None:
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=5)
```

**Artifact:** `src/capabilities/voice/wake_word.py`

---

### TASK 16.4 — Voice Pipeline Tests (5 tests)

**Location:** `tests/test_voice.py`

Required tests (mock audio files):

1. STT: transcribe WAV file → returns non-empty text string
2. STT: returns language field in result data
3. TTS: generates audio file at expected path
4. Wake word detector: fires callback when wake word present in audio
5. Wake word detector: does NOT fire callback on non-matching audio

**Artifact:** `tests/test_voice.py`

### Definition of Done — Phase 16

- [ ] `stt` transcribes audio file using Whisper base model
- [ ] `tts` generates WAV file in `data/audio/`
- [ ] `WakeWordDetector` runs in daemon thread, fires callback correctly
- [ ] Missing `openai-whisper` → `ToolResult.failure` (not ImportError)
- [ ] All 5 tests pass

---

## Phase 17 — Vision + Image

```yaml
phase_id: 17
priority: "P3"
status: "not_started"
total_tasks: 2
blocker: "Phase 16 complete"
next_action: "TASK 17.1"
```

### Theoretical Foundation

Both vision capabilities delegate to Ollama (llava:7b) and diffusers (Stable Diffusion) respectively. VRAM check is performed before any model load — insufficient VRAM returns `ToolResult.failure` immediately. Image output paths use `data/images/` for generated images and `data/screenshots/` for vision analysis inputs.

### TASK 17.1 — Vision Capability (`vision_analyze`)

**Location:** `src/capabilities/vision/vision.py`

**Input:** `{"image_path": str, "prompt": str?}` (prompt defaults to `"describe this image"`)
**Output:** `ToolResult(success=True, data={"description": str})`

#### Subtask 17.1.1 — Implement `VisionCapability`

```python
import base64
from pathlib import Path
import requests

class VisionCapability(BaseCapability):
    name = "vision_analyze"
    domain = "vision"
    VRAM_REQUIRED = 4500

    def execute(self, args: dict) -> ToolResult:
        try:
            from src.models.vram_monitor import VRAMMonitor
            if not VRAMMonitor().is_model_loadable(self.VRAM_REQUIRED):
                return ToolResult.failure(self.name,
                    f"VRAM insufficient for llava:7b (requires {self.VRAM_REQUIRED}MB)")

            image_path = Path(args["image_path"])
            if not image_path.exists():
                return ToolResult.failure(self.name, f"image not found: {image_path}")

            b64 = base64.b64encode(image_path.read_bytes()).decode()
            prompt = args.get("prompt", "describe this image")

            from src.core.config import load_config
            base_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
            resp = requests.post(f"{base_url}/api/chat", json={
                "model": "llava:7b",
                "messages": [{"role": "user", "content": prompt, "images": [b64]}],
                "stream": False
            }, timeout=60)
            resp.raise_for_status()
            description = resp.json()["message"]["content"]
            return ToolResult.success_result(self.name, {"description": description})
        except Exception as e:
            return ToolResult.failure(self.name, str(e))
```

**Artifact:** `src/capabilities/vision/vision.py`

---

### TASK 17.2 — Image Generation Capability (`image_gen`)

**Location:** `src/capabilities/vision/image_gen.py`

**Input:** `{"prompt": str, "size": "512x512"|"768x768"|"1024x1024"}` (size defaults to `"512x512"`)
**Output:** `ToolResult(success=True, data={"image_path": str})`

#### Subtask 17.2.1 — Implement `ImageGenCapability`

```python
import uuid
from pathlib import Path

class ImageGenCapability(BaseCapability):
    name = "image_gen"
    domain = "vision"

    def execute(self, args: dict) -> ToolResult:
        try:
            from src.models.vram_monitor import VRAMMonitor
            import torch
            from diffusers import StableDiffusionPipeline

            prompt = args["prompt"]
            size_str = args.get("size", "512x512")
            width, height = map(int, size_str.split("x"))

            vram_ok = VRAMMonitor().get_available_vram_mb() >= 2048
            dtype = torch.float16 if vram_ok else torch.float32
            device = "cuda" if vram_ok else "cpu"

            pipe = StableDiffusionPipeline.from_pretrained(
                "runwayml/stable-diffusion-v1-5", torch_dtype=dtype
            ).to(device)

            image = pipe(prompt, width=width, height=height).images[0]

            Path("data/images").mkdir(parents=True, exist_ok=True)
            output_path = f"data/images/{uuid.uuid4()}.png"
            image.save(output_path)

            return ToolResult.success_result(self.name, {"image_path": output_path})
        except ImportError:
            return ToolResult.failure(self.name,
                "diffusers or torch not installed — run: pip install 'jarvis[vision]'")
        except Exception as e:
            return ToolResult.failure(self.name, str(e))
```

**Artifact:** `src/capabilities/vision/image_gen.py`

### Definition of Done — Phase 17

- [ ] `vision_analyze` checks VRAM before loading llava:7b
- [ ] `image_gen` falls back to CPU float32 when VRAM < 2GB
- [ ] Missing `diffusers` → `ToolResult.failure` (not ImportError)
- [ ] Output images saved to `data/images/`

---

## Phase 18 — QA + Production (EXTENDED TESTING)

```yaml
phase_id: 18
priority: "P0"
status: "not_started"
total_tasks: 9
blocker: "Phase 17 complete"
next_action: "TASK 18.1"
stabilization: "v3.2 — extended testing: chaos, fault injection, load, timeout, sandbox escape, scheduling integrity, SLA isolation, cancellation, mode enforcement, capability scope"
```

### Theoretical Foundation

Production readiness requires four proofs: performance targets met (fast-path <100ms, simple query <5s), Arabic bilingual operation verified end-to-end, determinism confirmed (identical inputs → identical outputs), and total test coverage above 80%. **v3.2 extends testing** with chaos testing, fault injection, load testing, timeout testing, sandbox escape tests, plus 5 new suites: scheduling integrity, SLA isolation, cancellation confirmation, mode enforcement, and capability scope violation. The release cannot ship without passing all 14 tasks in this phase.

### TASK 18.1 — Performance Tests

**Location:** `tests/test_performance.py`

#### Subtask 18.1.1 — Write 5 latency target tests

```python
# tests/test_performance.py
import time
import pytest

def test_fast_path_under_100ms():
    from src.core.decision.fast_path import FastPath
    fp = FastPath()
    start = time.time()
    for _ in range(100):
        fp.check("open notepad")
    avg_ms = (time.time() - start) * 1000 / 100
    assert avg_ms < 100, f"Fast path avg {avg_ms:.1f}ms exceeds 100ms target"

def test_simple_run_turn_under_5000ms(mock_ollama):
    from src.core.runtime.loop import run_turn
    start = time.time()
    run_turn("what is 2 plus 2", "perf_s1")
    elapsed_ms = (time.time() - start) * 1000
    assert elapsed_ms < 5000, f"run_turn took {elapsed_ms:.0f}ms, exceeds 5000ms target"

def test_vram_headroom_after_model_load():
    from src.models.vram_monitor import VRAMMonitor
    assert VRAMMonitor().get_available_vram_mb() >= 512

def test_metrics_p95_under_5000ms():
    from src.core.observability.metrics import MetricsCollector
    from src.core.runtime.loop import run_turn
    mc = MetricsCollector()
    mc.reset()
    for i in range(10):
        run_turn(f"hello {i}", f"perf_s{i}")
    summary = mc.get_summary()
    if "decision" in summary.get("latency", {}):
        p95 = summary["latency"]["decision"].get("p95", 0)
        assert p95 < 5000, f"Decision p95 {p95:.0f}ms exceeds 5000ms"

def test_concurrent_chat_requests():
    import threading
    from src.core.runtime.loop import run_turn
    from src.core.runtime.final_response import FinalResponse
    results = []
    errors = []
    def make_request(i):
        try:
            r = run_turn(f"hello from thread {i}", f"concurrent_s{i}")
            results.append(r)
        except Exception as e:
            errors.append(str(e))

    threads = [threading.Thread(target=make_request, args=(i,)) for i in range(3)]
    start = time.time()
    for t in threads: t.start()
    for t in threads: t.join(timeout=30)
    elapsed = time.time() - start
    assert not errors, f"Errors in concurrent requests: {errors}"
    assert all(isinstance(r, FinalResponse) for r in results)
    assert elapsed < 30, f"3 concurrent requests took {elapsed:.1f}s, exceeds 30s"
```

**Artifact:** `tests/test_performance.py`

---

### TASK 18.2 — Arabic Language Tests (7 tests)

**Location:** `tests/test_arabic.py`

#### Subtask 18.2.1 — Write Arabic bilingual verification tests

```python
# tests/test_arabic.py
import pytest

def test_arabic_open_app_fast_path():
    from src.core.decision.fast_path import FastPath
    d = FastPath().check("افتح المفكرة")
    assert d is not None
    assert d.tool_name == "open_app"
    assert d.tool_args.get("name") == "المفكرة"

def test_arabic_web_search_fast_path():
    from src.core.decision.fast_path import FastPath
    d = FastPath().check("ابحث عن الذكاء الاصطناعي")
    assert d is not None
    assert d.tool_name == "web_search"

def test_arabic_input_no_encoding_error():
    from src.core.context.bundle import InputPacket
    from src.memory.user_profile import UserProfile
    p = InputPacket(
        user_message="مرحبا جارفيس",
        session_id="ar_s1",
        user_profile=UserProfile(user_id="ar_user", language="ar")
    )
    assert p.user_message == "مرحبا جارفيس"

def test_arabic_language_prompt_contains_arabic_hint():
    from src.core.context.builder import PromptBuilder
    from src.core.decision.output import DecisionOutput, Intent, Complexity, ExecutionMode, RiskLevel, DecisionSource
    from src.core.context.bundle import InputPacket
    from src.memory.user_profile import UserProfile
    ar_profile = UserProfile(user_id="ar_u", language="ar")
    packet = InputPacket(user_message="مرحبا", session_id="ar_s2", user_profile=ar_profile)
    d = DecisionOutput(intent=Intent.chat, complexity=Complexity.low, mode=ExecutionMode.normal,
        model='gemma3:4b', requires_tools=False, confidence=0.9,
        risk_level=RiskLevel.low, decision_source=DecisionSource.fast_path)
    prompt = PromptBuilder().build(d, packet)
    assert "arabic" in prompt.lower() or "Arabic" in prompt

def test_arabic_input_packet_passes_validation():
    from src.core.context.bundle import InputPacket
    from src.memory.user_profile import UserProfile
    p = InputPacket(user_message="ما هو الذكاء الاصطناعي؟",
        session_id="ar_s3", user_profile=UserProfile(user_id="ar_u2"))
    assert len(p.user_message) > 0

def test_cli_formatter_arabic_rtl_mark():
    from src.interfaces.cli.formatting import CLIFormatter
    from src.core.runtime.final_response import FinalResponse
    from src.core.decision.output import DecisionSource
    response = FinalResponse(text="مرحبا بك", session_id="s1", model="m", mode="fast",
        quality=0.9, decision_source=DecisionSource.fast_path, turn_id=1)
    formatted = CLIFormatter().format_response(response)
    assert formatted.startswith("\u200f"), "Arabic response must begin with RTL mark"

def test_arabic_question_fast_path():
    from src.core.decision.fast_path import FastPath
    d = FastPath().check("ما هو الذكاء الاصطناعي")
    # Should match general question rule and return chat decision
    assert d is not None
    assert d.tool_name is None  # chat, not tool
```

```bash
pytest tests/test_arabic.py -v
# Expected: 7 passed
```

**Artifact:** `tests/test_arabic.py`

---

### TASK 18.3 — Production Configuration

**Location:** `config/runtime/production.yaml`

#### Subtask 18.3.1 — Create production overrides

```yaml
# config/runtime/production.yaml
# Production overrides — deep-merged over settings.yaml defaults.
# Start with: load_config("config/runtime/production.yaml")

execution_mode:
  deterministic:
    parallelism: disabled
    ordering: strict
  performance:
    parallelism: enabled
    ordering: relaxed

sla:
  fast: 100ms
  medium: 500ms
  heavy: 5000ms

models:
  default: "gemma3:4b"
  timeout_s: 45
  fallback_chain: ["qwen2.5:7b", "gemma3:4b"]

execution:
  mode: "BALANCED"
  max_iterations: 5
  total_turn_timeout_s: 120

observability:
  log_level: "WARNING"
  metrics_enabled: true
  trace_enabled: false
  replay_enabled: false
  log_rotation_mb: 100
  log_rotation_count: 5
```

**Validation:**

```bash
python -c "
from src.core.config import load_config
cfg = load_config('config/runtime/production.yaml')
assert cfg.observability.log_level == 'WARNING'
assert cfg.execution.total_turn_timeout_s == 120
print('Production config OK')
"
```

**Artifact:** `config/runtime/production.yaml`

---

### TASK 18.4 — Full Test Suite Execution

**Location:** All test files in `tests/`

#### Subtask 18.4.1 — Run full suite and verify coverage

```bash
# Run full suite
pytest tests/ -v --tb=short 2>&1 | tee /tmp/test_output.txt

# Run with coverage
pytest tests/ --cov=src --cov-report=term-missing 2>&1 | tee /tmp/coverage_output.txt

# Verify coverage threshold
grep "TOTAL" /tmp/coverage_output.txt
# TOTAL line must show >= 80%

# Verify no stray open_app() calls
grep -r "open_app(" src/ app/ --include="*.py" | grep -v "apps.py" | grep -v "test_"
# Must return empty (only apps.py definition allowed)

# Verify no utils/misc/helpers/brain/common folders
find . -type d -name "utils" -o -name "misc" -o -name "helpers" -o -name "brain" -o -name "common"
# Must return empty

# Verify VERSION file
cat VERSION
# Must contain exactly: 3.2.0
```

**Pass condition:** All tests pass, coverage ≥ 80%, no forbidden patterns found.

---

### TASK 18.5 — VERSION File and Release Notes

**Location:** `VERSION`, `docs/RELEASE_NOTES.md`

#### Subtask 18.5.1 — Create VERSION file

```
3.2.0
```

Single line, no trailing whitespace.

#### Subtask 18.5.2 — Write `docs/RELEASE_NOTES.md`

Required sections:

- **Version:** 3.2.0
- **Release Date:** {date}
- **Hardware Requirements:** RTX 3050 6GB VRAM minimum, 16GB RAM, Intel i5 12th Gen
- **New in v3.2:** Hardening pass — scheduler restricted to placement, passive SLA events, dual-mode cancellation, runtime capability validator, execution mode enforcement, extended test suites (scheduling integrity, SLA isolation, cancellation, mode enforcement, capability scope)
- **Breaking Changes from v3.0:** State machine flow corrected (SCHEDULING state added), ExecutionEngine stripped of decision/routing/retry logic, adaptive optimizer removed, streaming restricted to heavy tasks only, batching restricted to multi-item operations
- **Setup Instructions:** `git clone` → `pip install -e .` → `cp settings.example.yaml settings.yaml` → `cp .env.example .env` → `python app/main.py`
- **Known Limitations:** Hardware-bound performance, Ollama must be running locally, voice and vision require optional dependencies
- **Debug Checklist:** Ollama connectivity, VRAM headroom, allowed_roots config

#### Subtask 18.5.3 — Remove all debug `print()` calls

```bash
# Find debug prints in non-CLI, non-interface code
grep -rn "print(" src/core/ src/capabilities/ src/memory/ src/models/ src/services/ --include="*.py"
# Review each: legitimate user-facing output vs debug print
# Remove all debug prints; replace with logger.debug()
```

**Artifacts:** `VERSION`, `docs/RELEASE_NOTES.md`

---

### TASK 18.6 — Determinism Verification Tests (6 tests)

**Location:** `tests/test_determinism.py`

#### Subtask 18.6.1 — Write 6 determinism proof tests

```python
# tests/test_determinism.py
import pytest

def test_same_input_same_fast_path_decision():
    from src.core.decision.fast_path import FastPath
    fp = FastPath()
    results = [fp.check("open notepad") for _ in range(10)]
    # All must be identical
    assert all(r.tool_name == results[0].tool_name for r in results)
    assert all(r.tool_args == results[0].tool_args for r in results)

def test_same_vram_same_model_ranking():
    from src.core.decision.scorer import ModelScorer
    scorer = ModelScorer()
    rankings_1 = [s.model for s in scorer.rank_models("low", "fast", 4096)]
    rankings_2 = [s.model for s in scorer.rank_models("low", "fast", 4096)]
    assert rankings_1 == rankings_2

def test_state_machine_transitions_are_deterministic():
    from src.core.runtime.state import ALLOWED_TRANSITIONS, RuntimeState, can_transition
    # Same state always produces same allowed transitions
    for state in RuntimeState:
        allowed_1 = ALLOWED_TRANSITIONS.get(state, frozenset())
        allowed_2 = ALLOWED_TRANSITIONS.get(state, frozenset())
        assert allowed_1 == allowed_2

def test_model_scorer_rank_identical_across_10_calls():
    from src.core.decision.scorer import ModelScorer
    scorer = ModelScorer()
    rankings = [
        [s.model for s in scorer.rank_models("medium", "normal", 4500)]
        for _ in range(10)
    ]
    assert all(r == rankings[0] for r in rankings)

def test_retry_manager_decrements_predictably():
    from src.core.runtime.retry import RetryManager
    rm = RetryManager()
    initial = rm.remaining
    rm.consume(1)
    assert rm.remaining == initial - 1
    rm.consume(2)
    assert rm.remaining == initial - 3

def test_check_limit_identical_results_identical_inputs():
    from src.core.runtime.limits import Limits
    limits = Limits()
    results = [limits.check_limit("max_iterations", 4) for _ in range(10)]
    assert all(r == results[0] for r in results)
    # Semantics: current < max → True
    assert limits.check_limit("max_iterations", 4) == True   # 4 < 5
    assert limits.check_limit("max_iterations", 5) == False  # 5 >= 5
```

```bash
pytest tests/test_determinism.py -v
# Expected: 6 passed
```

**Artifact:** `tests/test_determinism.py`

---

### TASK 18.7 — Chaos Testing (5 tests)

**Location:** `tests/test_chaos.py`

**Purpose:** Random failure injection to verify system resilience under unpredictable conditions.

Required tests:
1. Random capability failure → system recovers gracefully, no crash
2. Random model failure during DECIDING → fallback activates, no crash
3. Random sandbox timeout → task cancelled, StateMachine transitions to ERROR → RECOVERY
4. Multiple simultaneous failures → system degrades gracefully, produces FinalResponse
5. Random EventBus failure → system continues, errors logged but not propagated

**Artifact:** `tests/test_chaos.py`

---

### TASK 18.8 — Fault Injection Testing (5 tests)

**Location:** `tests/test_fault_injection.py`

**Purpose:** Simulate specific failure modes to verify recovery paths.

Required tests:
1. Simulate Ollama service down → degraded FinalResponse returned
2. Simulate VRAM exhaustion → model downgrade attempted, fallback chain activated
3. Simulate database corruption → DB moved aside, fresh DB created, system continues
4. Simulate filesystem full → ToolResult.failure returned, no crash
5. Simulate network failure during web_search → graceful fallback, error logged

**Artifact:** `tests/test_fault_injection.py`

---

### TASK 18.9 — Load Testing (4 tests)

**Location:** `tests/test_load.py`

**Purpose:** Verify system behavior under concurrent load.

Required tests:
1. 10 concurrent chat requests → all return FinalResponse, no deadlock
2. 5 concurrent capability executions → ConcurrencyController limits parallelism
3. Rapid sequential requests (100 in 10s) → no resource exhaustion, system stable
4. Priority aging test: low-priority tasks eventually execute (no starvation)

**Artifact:** `tests/test_load.py`

---

### TASK 18.10 — Timeout Testing (4 tests)

**Location:** `tests/test_timeout.py`

**Purpose:** Verify SLA enforcement and timeout handling.

Required tests:
1. Fast task exceeds 100ms SLA → logged, system continues
2. Medium task exceeds 500ms SLA → cancelled, fallback to simpler path
3. Heavy task exceeds 5000ms SLA → hard kill, process tree terminated
4. Timeout during DECIDING → ERROR → RECOVERY → IDLE transition verified

**Artifact:** `tests/test_timeout.py`

---

### TASK 18.11 — Sandbox Escape Tests (5 tests)

**Location:** `tests/test_sandbox_escape.py`

**Purpose:** Verify sandbox isolation cannot be bypassed.

Required tests:
1. Code execution attempts to access `/etc/passwd` → blocked by FilesystemRestrictor
2. Code execution attempts network access → blocked by network policy
3. Code execution attempts privilege escalation → blocked by privilege drop
4. Code execution attempts to spawn child process → blocked or tracked by process tree
5. Code execution exceeds memory limit → killed by ResourceMonitor, no main process impact

**Artifact:** `tests/test_sandbox_escape.py`

---

### Definition of Done — Phase 18

- [ ] `pytest tests/ -v` → all tests pass, 0 failures
- [ ] `pytest tests/ --cov=src` → TOTAL ≥ 80%
- [ ] Fast-path latency < 100ms confirmed by `test_performance.py`
- [ ] Arabic verified end-to-end by `test_arabic.py`
- [ ] Determinism verified by `test_determinism.py`
- [ ] Chaos testing passes: system resilient under random failures
- [ ] Fault injection passes: all simulated failures recover gracefully
- [ ] Load testing passes: no deadlocks, no starvation, no resource exhaustion
- [ ] Timeout testing passes: SLA enforced, timeouts handled correctly
- [ ] Sandbox escape tests pass: no isolation bypass possible
- [ ] `VERSION` file contains `3.2.0`
- [ ] `docs/RELEASE_NOTES.md` complete
- [ ] No debug `print()` statements in non-interface code
- [ ] No hardcoded paths anywhere in `src/`

---

## Summary

| Metric          | Value                                                                                               |
| :-------------- | :-------------------------------------------------------------------------------------------------- |
| Total phases    | 20 (0–18 + 14.5)                                                                                    |
| Total tasks     | ~153 (v3.2: +5 new test suites + 3 operational hardening tasks: guard rails, EventBus contract, alerting) |
| Total subtasks  | ~332                                                                                                |
| Test files      | 23 (tests added to existing files: +11 new tests across state_machine, observability, performance)  |
| Config files    | 9 (+1: execution_mode config)                                                                       |
| Source modules  | ~68 (+3: alerting.py, FORBIDDEN_LOOPS, EventEnvelope contract)                                      |
| Capabilities    | 13 (8 core + 2 voice + 2 vision + 1 browser)                                                        |
| Contract models | 7 (InputPacket, DecisionOutput, LLMOutput, ToolResult, FinalResponse, ModelScore, EvaluationResult) |

---

## Final Validation Checklist

```
Architecture
[ ] No utils, misc, helpers, brain, common folders anywhere
[ ] No spaces in directory names (web_ui not "web ui")
[ ] capabilities/web/ used (not web_automation/)
[ ] src/core/sandbox/ and src/core/safety/ exist
[ ] src/core/observability/ with event_bus.py and metrics.py
[ ] data/audio/ directory exists (TTS output)
[ ] docs/RELEASE_NOTES.md exists

CONTROL FLOW (v3.2)
[ ] Single controller: StateMachine is ONLY orchestrator
[ ] ExecutionEngine is executor ONLY — no decisions, routing, retries
[ ] CapabilityRuntime is INTERNAL — not importable by interfaces/decision/services
[ ] All calls route through StateManager.transition_to()
[ ] Corrected flow: IDLE→DECIDING→SCHEDULING→EXECUTING→EVALUATING→COMPLETED
[ ] Cancellation flow: ANY STATE→CANCELLED→CLEANUP→IDLE
[ ] Error flow: ANY FAILURE→ERROR→RECOVERY→DECIDING|IDLE
[ ] StateMachine controls ALL retries
[ ] EventBus: EventEnvelope enforced — event_id + source + trace_id + sequence on every event
[ ] EventBus: subscriber isolation — one subscriber failure cannot affect others
[ ] State machine: FORBIDDEN_LOOPS enforced in StateManager.transition_to()
[ ] State machine: MAX_TRANSITIONS_PER_TURN = 20 hard ceiling per run_turn()
[ ] AlertManager: passive — emits EVT_THRESHOLD_ALERT only, no execution side effects
[ ] AlertManager: 3 default rules (latency, error_rate, violation_count) with cooldown
[ ] No EVT_* string literals anywhere in src/ — all imports from event_bus.py

DETERMINISM (v3.2)
[ ] execution_mode config exists: deterministic and performance modes
[ ] Fast-path produces identical outputs for identical inputs
[ ] Model scorer ranking is deterministic
[ ] State machine transitions are deterministic

SANDBOX (v3.2 HARDENED)
[ ] Process isolation (separate PID)
[ ] Privilege drop (no admin/root)
[ ] Filesystem sandbox (allowlist paths)
[ ] Network policy (deny by default)
[ ] Syscall restrictions (where possible)
[ ] Execution timeout (hard kill)
[ ] Process tree kill (parent + children)

SLA ENFORCEMENT (v3.2 PASSIVE)
[ ] SLA config: fast=100ms, medium=500ms, heavy=5000ms
[ ] SLAEnforcer monitors execution vs targets
[ ] On timeout: cancel_task, fallback, log_event

CONCURRENCY (v3.2)
[ ] Deadlock prevention: lock ordering rules
[ ] Starvation prevention: priority aging
[ ] Priority inversion handling: temporary priority boost

CAPABILITY BOUNDARIES (v3.2)
[ ] Each capability defines scope: allowed/forbidden operations
[ ] Resource limits per capability: cpu%, memory MB
[ ] No capability expands beyond defined scope
[ ] Cross-domain logic = NEW capability

COMPLEXITY CONTROL (v3.2)
[ ] No adaptive optimizer — rule-based only
[ ] Streaming ONLY for heavy tasks
[ ] Batching ONLY where needed (multi-item)

Contracts
[ ] All 7 contract models importable from canonical locations
[ ] ValidationResult.first_error() and all_errors() implemented
[ ] SchemaValidator stub exists before Phase 6 (created in Phase 2)
[ ] Factor names in scorer exactly match models.yaml weight keys

Safety
[ ] Three-gate permission enforced in CapabilityExecutor
[ ] file_ops path validation uses Path.resolve() + os.path.commonpath() only
[ ] Safety YAML has blocked_apps AND blocked_commands (not nested under execution)
[ ] code_exec always cleans tmpdir in finally block

State Machine
[ ] All state transitions through StateManager.transition_to()
[ ] No direct self._state = assignments outside state_manager.py
[ ] check_limit semantics: current < max → True, current >= max → False

Configuration
[ ] Config precedence: CLI > ENV > .env > YAML enforced
[ ] Secrets only in config/env/.env — never in YAML
[ ] models.yaml weights sum to 1.0 (validated at load_config())
[ ] settings.yaml exists (not just .example)

Capabilities
[ ] All capabilities inherit BaseCapability
[ ] All capabilities implement all abstract methods
[ ] All capabilities return ToolResult — never raise to caller
[ ] AppLauncher.execute(args) used everywhere after Phase 9
[ ] grep -r "open_app(" src/ app/ returns only apps.py definition

Code Quality
[ ] src/__version__ == "3.2.0"
[ ] VERSION file contains 3.2.0
[ ] No debug print() in non-interface code
[ ] No hardcoded paths

Tests
[ ] pytest tests/ -v → all tests pass
[ ] pytest tests/ --cov=src → TOTAL >= 80%
[ ] All three spec files share spec_version: v3.2
[ ] AuditLogger creates data/audit.db after first capability execution
[ ] Chaos testing passes
[ ] Fault injection passes
[ ] Load testing passes
[ ] Timeout testing passes
[ ] Sandbox escape tests pass
```

---

**JARVIS v3.2 — Execution Plan**
_spec_version: v3.2 | structure_version: 3.2 | last_updated: 2026-05-03_
_Contract-first. Capabilities sovereign. State machine authoritative. No bypass paths. Controlled determinism. Hardened sandbox. SLA enforced._
