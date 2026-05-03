# 📋 JARVIS v3.0 — Execution Plan

> **spec_version:** `v3.0` | **project_version:** `3.0.0` | **structure_version:** `3`
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
  version: "3.0.0"
  spec_version: "v3.0"
  structure_version: "3"
  last_updated: "2026-05-03"
  current_phase: 2
  overall_progress_percent: 23
  risk_level: "medium"
  hardware_profile:
    gpu: "RTX 3050 6GB VRAM"
    ram: "16 GB"
    cpu: "Intel Core i5 12th Gen"
  current_blocker: "none"
  next_action: "TASK 2.0"
  config_root: "config/runtime/"
  env_root: "config/env/"
  phases_complete:
  phases_pending:
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, "14.5", 15, 16, 17, 18]
  notes:
    - "Phase 9 must migrate app/jarvis_slice.py open_app() calls to CapabilityExecutor.execute()."
    - "data/audio/ directory added in v3 structure for TTS output files."
    - "RELEASE_NOTES.md added to docs/ in v3 structure."
```

---

## Dependency Graph

```
Phase 0
  └─→ Phase 1
        └─→ Phase 2 ─→ Phase 5 ─→ Phase 6
                                            └─→ Phase 7
                                                  └─→ Phase 8
                                                        └─→ Phase 9
                                                              └─→ Phase 10
                                                                    └─→ Phase 11
                                                                          └─→ Phase 12
                                                                                └─→ Phase 13
                                                                                      └─→ Phase 14
                                                                                            └─→ Phase 14.5
                                                                                                  └─→ Phase 15
                                                                                                        └─→ Phase 16
                                                                                                              └─→ Phase 17
                                                                                                                    └─→ Phase 18


Critical Path: 0 → 1 → 2 → 5 → 6 → 7 → 8 → 9 → 10 → 11 → 18
```

---

## Canonical Directory Structure

```
jarvis/
│
├── VERSION
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
│   ├── memory.db
│   ├── audit.db
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
    ├── __init__.py
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
| 0     | First Working System        | P0       | ░░░░░░░░░░ | 0/5   | PENDING |
| 1     | Foundation + Observability  | P0       | ░░░░░░░░░░ | 0/13  | PENDING |
| 2     | Execution Contract          | P0       | ░░░░░░░░░░ | 0/10  | PENDING |
| 3     | Model Manager + VRAM        | P0       | ░░░░░░░░░░ | 0/5   | PENDING |
| 4     | Runtime State Machine       | P0       | ░░░░░░░░░░ | 0/8   | PENDING |
| 5     | Decision System             | P1       | ░░░░░░░░░░ | 0/7   | PENDING |
| 6     | Sandbox + Safety            | P0       | ░░░░░░░░░░ | 0/7   | PENDING |
| 7     | Memory Engine               | P1       | ░░░░░░░░░░ | 0/6   | PENDING |
| 9     | System Control Capabilities | P1       | ░░░░░░░░░░ | 0/8   | PENDING |
| 10    | Prompt Builder              | P1       | ░░░░░░░░░░ | 0/5   | PENDING |
| 11    | Execution Hardening         | P0       | ░░░░░░░░░░ | 0/6   | PENDING |
| 8     | Capability System           | P1       | ░░░░░░░░░░ | 0/6   | PENDING |
| 12    | CLI Interface               | P2       | ░░░░░░░░░░ | 0/3   | PENDING |
| 13    | Web Automation & Browser    | P2       | ░░░░░░░░░░ | 0/3   | PENDING |
| 14    | Google APIs                 | P2       | ░░░░░░░░░░ | 0/4   | PENDING |
| 14.5  | Telegram Integration        | P2       | ░░░░░░░░░░ | 0/3   | PENDING |
| 15    | Web UI                      | P2       | ░░░░░░░░░░ | 0/3   | PENDING |
| 16    | Voice Pipeline              | P3       | ░░░░░░░░░░ | 0/4   | PENDING |
| 17    | Vision + Image              | P3       | ░░░░░░░░░░ | 0/2   | PENDING |
| 18    | QA + Production             | P0       | ░░░░░░░░░░ | 0/6   | PENDING |

---

## Phase 0 — First Working System (Vertical Slice)

```yaml
phase_id: 0
priority: "P0"
status: "not_started"
total_tasks: 5
validation_status: "!!!"
last_updated: "2026-05-02"
```

Phase 0 proved the full Observe → Decide → Think → Act → Evaluate loop executes end-to-end on real hardware. It deliberately used simplified contracts in favor of speed of proof. All shortcuts are resolved in later phases.

**Verified:** DecisionOutput with score_breakdown/candidate_list, LLMOutput, ToolResult, InputPacket, FinalResponse contracts (pre-formal), CapabilityExecutor replacing direct open_app() calls, 17 contract tests passing.

**Breaking change:** Phase 0 `AppLauncher` uses `open_app(name)`. Phase 9 TASK 9.1 replaces this with `execute(args)` inheriting `BaseCapability`. All callers in `app/jarvis_slice.py` updated in Phase 9.

**Artifacts:** `app/jarvis_slice.py`, `src/models/llm/engine.py`, `src/core/decision/classifier.py`, `src/capabilities/system/apps.py`, `src/capabilities/base.py`, `src/capabilities/executor.py`, `src/capabilities/result.py`

---

## Phase 1 — Foundation + Observability

```yaml
phase_id: 1
priority: "P0"
status: "not_started"
total_tasks: 13
validation_status: "Phase 0 complete"
last_updated: "2026-05-03"
```

All 13 tasks complete. The project is an installable Python package with validated configuration, structured logging, observability infrastructure (EventBus, MetricsCollector), custom exception hierarchy, model profiles, capabilities manifest, user profiles, and shared test fixtures. Every subsequent phase builds on this foundation.

**Artifacts:** `pyproject.toml`, `requirements.txt`, all `__init__.py` files, `config/runtime/settings.yaml`, `config/runtime/settings.example.yaml`, `src/core/config.py`, `src/core/logging_setup.py`, `src/models/profiles.py`, `config/runtime/models.yaml`, `config/env/.env`, `config/env/.env.example`, `src/memory/user_profile.py`, `config/runtime/capabilities.yaml`, `src/core/observability/metrics.py`, `app/main.py`, `src/core/observability/event_bus.py`, `src/core/exceptions.py`, `tests/conftest.py`

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
    tool_results: list[ToolResult] = []
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
    issues: list[str] = []
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
validation_status: "Phase 22 complete"
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
validation_status: "Phase 3 complete"
completion_note: >
  Completed ahead of Phase 2 via vertical slice extension.
  TASK 2.8 migrates loop.py and executor.py to formal Phase 2 contracts.
  Phase 4 decision stub is replaced by Phase 5 decide().
```

**Artifacts:** `src/core/runtime/state.py`, `src/core/runtime/state_manager.py`, `src/core/runtime/limits.py`, `src/core/context/assembler.py`, `src/core/runtime/executor.py`, `src/core/runtime/evaluator.py`, `src/core/runtime/loop.py`, `tests/test_state_machine.py`

**Key implementations:**

- `RuntimeState` enum: IDLE, DECIDING, EXECUTING_MODEL, EXECUTING_TOOL, WAITING_CONFIRMATION, EVALUATING, ERROR, COMPLETED
- `ALLOWED_TRANSITIONS` frozenset map — all transitions defined and enforced
- `StateManager.transition_to()` with lock, history recording, EventBus publication
- `Limits` class loaded from `config.execution` with `check_limit(name, current) → bool` (current < max → True)
- `ContextAssembler.assemble()` returning `InputPacket` — cold start returns empty history, no error
- `Evaluator`: completeness (0.4) + relevance (0.4) + coherence (0.2) heuristic scoring
- `run_turn()`: full state machine loop with `_stub_decide()` (replaced in Phase 5) and `_stub_execute_tool()`

**Transition map:**

```
IDLE → DECIDING
DECIDING → EXECUTING_MODEL | EXECUTING_TOOL | ERROR
EXECUTING_MODEL → EVALUATING | EXECUTING_TOOL | ERROR
EXECUTING_TOOL → WAITING_CONFIRMATION | EVALUATING | ERROR
WAITING_CONFIRMATION → EXECUTING_TOOL | ERROR | IDLE
EVALUATING → COMPLETED | DECIDING | ERROR
ERROR → IDLE
COMPLETED → IDLE
```

---

## Phase 5 — Decision System

```yaml
phase_id: 5
priority: "P1"
status: "not_started"
total_tasks: 7
blocker: "Phase 4 complete"
next_action: "TASK 5.1"
```

### Theoretical Foundation

Three design constraints govern the decision system: (1) **Fast path first** — regex-based rule engine handles common patterns in <1ms without invoking any model. (2) **Dynamic scoring** — when fast path misses, a 5-factor weighted scorer selects the best available model based on VRAM, task complexity, latency requirements, and historical performance. (3) **Graceful fallback** — if the LLM classifier fails to return valid JSON, the system falls back to a safe default rather than crashing. This phase replaces the Phase 4 `_stub_decide()` in `loop.py`.

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
    "browser":"medium","stt":"low","tts":"low","vision_analyze":"low","image_gen":"low",
}
FILE_ACTION_RISK = {
    "delete":"high","write":"medium","move":"medium","copy":"medium","read":"low","list":"low",
}
```

#### Subtask 5.4.2 — Implement `assess()` with escalation logic

No tool → `RiskLevel.low`. Collect base risk + file action override + path traversal check + blocked path check. Return highest level using `RISK_RANK = {"low":0, "medium":1, "high":2}`.

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

### TASK 5.7 — Decision System Tests (14 tests)

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

```bash
pytest tests/test_decision.py -v
# Expected: 14 passed
```

**Artifact:** `tests/test_decision.py`

### Definition of Done — Phase 5

- [ ] Fast path handles all 9 rules including Arabic bilingual patterns
- [ ] `extract_json` passes all repair scenarios, returns None on total failure
- [ ] `ModelScorer.rank_models()` always returns all 5 required factor keys
- [ ] `decide()` wired into `loop.py` replacing `_stub_decide()`
- [ ] `pytest tests/test_decision.py -v` → 14 passed

---

## Phase 6 — Sandbox + Safety

```yaml
phase_id: 6
priority: "P0"
status: "not_started"
total_tasks: 7
blocker: "Phase 5 complete"
next_action: "TASK 6.1"
```

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
total_tasks: 6
blocker: "Phase 6 complete"
next_action: "TASK 7.1"
```

### Theoretical Foundation

Memory is an active retrieval engine, not passive storage. Three relevance signals: keyword overlap (does this memory relate to the current query?), recency (how fresh?), interaction frequency (how often accessed?). SQLite WAL mode provides thread-safe concurrent reads without blocking the runtime. Corruption handling moves the bad DB aside and creates a fresh one — the system never crashes on DB corruption.

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

### TASK 7.6 — Memory Tests (10 tests)

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

```bash
pytest tests/test_memory.py -v
# Expected: 10 passed
```

**Artifact:** `tests/test_memory.py`

### Definition of Done — Phase 7

- [ ] `MemoryDB` stores, retrieves, handles corruption with no crash
- [ ] `MemoryScorer` values always in [0.0, 1.0]
- [ ] `TTLManager.cleanup()` removes expired entries and returns count
- [ ] `ContextRetriever` returns empty list on cold start
- [ ] `pytest tests/test_memory.py -v` → 10 passed

---

## Phase 8 — Capability System

```yaml
phase_id: 8
priority: "P1"
status: "not_started"
total_tasks: 6
blocker: "Phase 7 complete"
next_action: "TASK 8.1"
```

### Theoretical Foundation

Two invariants: all side-effects flow through `BaseCapability.execute()`, and all invocations flow through `CapabilityExecutor`'s 6-gate pipeline. No capability can be imported and called directly — it must be retrieved from `CapabilityRegistry` by name. This indirection enables hot-reloading, mocking in tests, and future remote sandboxing without changing calling code.

### TASK 8.1 — `BaseCapability` Abstract Class

**Location:** `src/capabilities/base.py`
**Purpose:** Defines the capability contract. ABC enforcement catches missing implementations at class definition time, not at runtime.

#### Subtask 8.1.1 — Define `BaseCapability(ABC)` with 4 abstract methods

```python
from abc import ABC, abstractmethod
from src.capabilities.result import ToolResult
from src.capabilities.validator import ValidationResult
from src.core.decision.output import RiskLevel

class BaseCapability(ABC):
    name: str
    domain: str
    description: str

    @abstractmethod
    def execute(self, args: dict) -> ToolResult:
        """MUST NEVER RAISE — wrap all exceptions in ToolResult.failure()."""
        ...

    @abstractmethod
    def validate(self, args: dict) -> ValidationResult:
        """Synchronous, fast, side-effect-free."""
        ...

    @abstractmethod
    def get_risk_level(self, args: dict | None = None) -> RiskLevel:
        """Override to compute dynamically from args."""
        ...

    @abstractmethod
    def dry_run(self, args: dict) -> ToolResult:
        """Must set result.dry_run=True. No side effects."""
        ...

    def to_dict(self) -> dict:
        return {"name": self.name, "domain": self.domain,
                "description": self.description,
                "risk_level": self.get_risk_level().value}
```

**Artifact:** `src/capabilities/base.py`

---

### TASK 8.2 — Capability Registry

**Location:** `src/capabilities/registry.py`
**Purpose:** Singleton registry. `load_from_manifest()` dynamically imports and instantiates all capabilities from `capabilities.yaml`. Failed imports are logged as warnings — the registry continues loading other capabilities.

#### Subtask 8.2.1 — Implement singleton registry

```python
class CapabilityRegistry:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._capabilities: dict[str, BaseCapability] = {}
        return cls._instance

    def register(self, capability: BaseCapability) -> None:
        if capability.name in self._capabilities:
            raise ValueError(f"Capability '{capability.name}' already registered")
        self._capabilities[capability.name] = capability

    def get(self, name: str) -> BaseCapability | None:
        return self._capabilities.get(name)

    def list_all(self) -> list[str]:
        return list(self._capabilities.keys())

    def load_from_manifest(self, path: str = "config/runtime/capabilities.yaml") -> None:
        import yaml, importlib
        with open(path) as f:
            caps = yaml.safe_load(f).get("capabilities", [])
        for entry in caps:
            module_path, class_name = entry["module_path"].rsplit(".", 1)
            try:
                module = importlib.import_module(module_path)
                cls = getattr(module, class_name)
                self.register(cls())
            except Exception as e:
                logger.warning(f"Failed to load '{entry['name']}': {e}")

    def reset(self) -> None:
        self._capabilities.clear()
```

**Artifact:** `src/capabilities/registry.py`

---

### TASK 8.3 — Capability Executor (Full 6-Gate Pipeline)

**Location:** `src/capabilities/executor.py`
**Purpose:** ONLY entry point for running any capability. Orchestrates all gates in order.

#### Subtask 8.3.1 — Implement `execute()` with all 6 gates

```
Gate 1: CapabilityRegistry.get(name) → not None
Gate 2: capability.validate(args) → valid
Gate 3: PermissionLayer.check(name, args, decision, mode) → allow/confirm/block
Gate 4: if confirm → publish EVT_WAITING_CONFIRMATION, log
Gate 5: if dry_run=True → Sandbox.dry_run(capability, args) → return
Gate 6: Sandbox.execute(capability, args, timeout_s=limits.tool_timeout_s)
```

After Gate 6: set `result.risk_level`, set `result.turn_id`, call `AuditLogger.log_action()`.

All gate failures return `ToolResult.failure(name, reason)` — never raise.

**Artifact:** `src/capabilities/executor.py`

---

### TASK 8.4 — Capability Validation Tests (8 tests)

**Location:** `tests/test_capabilities.py`

Required tests:

1. Concrete subclass missing `execute` → `TypeError` at instantiation
2. Registry `register` + `get` round-trip
3. Registry rejects duplicate name with `ValueError`
4. Registry `get` unknown name → `None`
5. `CapabilityExecutor` unknown capability → `ToolResult.failure` (gate 1)
6. `CapabilityExecutor` invalid args → `ToolResult.failure` (gate 2)
7. `CapabilityExecutor` blocked in BALANCED mode → `ToolResult.failure` (gate 3)
8. `CapabilityExecutor` dry_run=True → `ToolResult` with `dry_run=True`

**Artifact:** `tests/test_capabilities.py`

---

### TASK 8.5 — Sandbox Tests (4 tests)

**Location:** `tests/test_sandbox.py`

Required tests:

1. Slow capability exceeds timeout → `ToolResult.failure` with "timeout" in error
2. Capability that raises → wrapped in `ToolResult.failure`
3. Dry-run calls `dry_run()` not `execute()`
4. `duration_ms` set and > 0 after execution

**Artifact:** `tests/test_sandbox.py`

---

### TASK 8.6 — Observability Tests (6 tests)

**Location:** `tests/test_observability.py`

Required tests:

1. `MetricsCollector` records latency and appears in summary
2. `MetricsCollector.reset()` clears all state
3. `EventBus` delivers to all subscribers
4. `EventBus` isolates bad callback from publisher
5. `EVT_TOOL_EXECUTED` published after successful execution
6. `EVT_STATE_TRANSITION` published on each state transition

**Artifact:** `tests/test_observability.py`

### Definition of Done — Phase 8

- [ ] `BaseCapability` ABC enforces all 4 abstract methods
- [ ] `CapabilityRegistry` singleton prevents duplicates
- [ ] `CapabilityExecutor` runs all 6 gates in order; failures return `ToolResult.failure`
- [ ] Dry-run returns `ToolResult` with `dry_run=True`
- [ ] All phase tests pass

---

## Phase 9 — System Control Capabilities

```yaml
phase_id: 9
priority: "P1"
status: "not_started"
total_tasks: 8
blocker: "Phase 8 complete"
next_action: "TASK 9.1"
```

### Theoretical Foundation

Each capability is a complete, independently deployable tool with its own contract, validation, platform branching, error handling, and dry-run. No OS call exists outside `src/capabilities/`. `file_ops` path validation uses `Path.resolve()` + `os.path.commonpath()` exclusively — string prefix matching is explicitly forbidden and has known bypass vectors.

### TASK 9.1 — App Launcher (`open_app`) — Migrate from Phase 0

**Location:** `src/capabilities/system/apps.py`
**Depends on:** Phase 8 `BaseCapability`
**Purpose:** Migration of Phase 0 stub to full `BaseCapability` contract. Platform-aware discovery: PATH → OS-specific locations.

#### Subtask 9.1.1 — Implement `validate()`

Check `name` key present, non-empty string, not in `config.safety.blocked_apps` (case-insensitive).

#### Subtask 9.1.2 — Windows discovery order

1. `shutil.which(name)` — PATH
2. `%APPDATA%\Microsoft\Windows\Start Menu\Programs\` — scan for `{name}.lnk`
3. `C:\Program Files\` and `C:\Program Files (x86)\` — scan for `{name}.exe`
4. Launch with `subprocess.Popen([executable])`, capture pid

#### Subtask 9.1.3 — Linux discovery order

1. `shutil.which(name)` — PATH
2. `~/.local/share/applications/` + `/usr/share/applications/` — scan `*.desktop`, match `Name=` or `Exec=`
3. Extract and clean `Exec=` value, strip `%U`, `%F` placeholders
4. Launch with `subprocess.Popen([executable])`

#### Subtask 9.1.4 — macOS discovery order

1. `shutil.which(name)` — PATH
2. `/Applications/{name}.app` — case-insensitive glob
3. `subprocess.run(["open", "-a", name])` — fallback

#### Subtask 9.1.5 — Migrate `app/jarvis_slice.py`

Replace all `open_app(name)` calls with:

```python
from src.capabilities.executor import CapabilityExecutor
result = CapabilityExecutor().execute("open_app", {"name": name}, decision, mode)
```

**Output:** `ToolResult(success=True, data={"pid": int, "name": str, "path": str})`
**Dry-run:** `ToolResult(success=True, data={"would_launch": name}, dry_run=True)`
**All errors:** caught → `ToolResult.failure("open_app", descriptive_message)`

**Artifact:** `src/capabilities/system/apps.py`, updated `app/jarvis_slice.py`

---

### TASK 9.2 — System Info Capability (`system_info`)

**Location:** `src/capabilities/system/sysinfo.py`

**Input:** `{"info_type": "all"|"cpu"|"ram"|"gpu"|"os"}` (optional, default `"all"`)

**Data sources per section:**

- `cpu`: `psutil.cpu_percent(interval=0.5)`, `cpu_freq().current`, `cpu_count()`, `platform.processor()`
- `ram`: `psutil.virtual_memory()` → `{total_mb, used_mb, available_mb, percent}`
- `gpu`: `VRAMMonitor().get_available_vram_mb()`, `get_total_vram_mb()`, pynvml GPU name if available
- `os`: `platform.system()`, `platform.release()`, `platform.version()`, `platform.machine()`
- `all`: merge all four sections

Any section-level exception → `{"error": str(e)}` in that section only; other sections unaffected.

**Artifact:** `src/capabilities/system/sysinfo.py`

---

### TASK 9.3 — Clipboard Capability (`clipboard`)

**Location:** `src/capabilities/system/clipboard.py`

**Input:** `{"action": "read"|"write", "content": str?}`
**Validation:** `action` in enum; `write` requires non-empty `content`
**Implementation:** `pyperclip.paste()` / `pyperclip.copy(content)`
**Error:** `pyperclip.PyperclipException` → `ToolResult.failure("clipboard", "clipboard not available")`
**Dry-run:** `read` → `{"would_read": True}`; `write` → `{"would_write": content[:50]}`

**Artifact:** `src/capabilities/system/clipboard.py`

---

### TASK 9.4 — Notifications Capability (`notify`)

**Location:** `src/capabilities/notify/toasts.py`

**Input:** `{"title": str, "message": str, "duration": int?}` (duration defaults to 5)
**Primary:** `plyer.notification.notify(title=..., message=..., timeout=duration)`
**Fallback:** `print(f"[NOTIFY] {title}: {message}")` + loguru log
**Dry-run:** `{"would_notify": {"title": title, "message": message}}`

**Artifact:** `src/capabilities/notify/toasts.py`

---

### TASK 9.5 — Screenshot Capability (`screenshot`)

**Location:** `src/capabilities/screen/capture.py`

**Input:** `{"ocr": bool?, "region": {"x":int,"y":int,"width":int,"height":int}?}`
**Capture:** `PIL.ImageGrab.grab()` full screen; `grab(bbox=(x,y,x+w,y+h))` for region
**Save path:** `data/screenshots/{YYYYMMDD_HHMMSS}_{uuid4()[:8]}.png`
**OCR:** `pytesseract.image_to_string(img)` if `ocr=True` and pytesseract available; else `ocr_text=None` + log WARNING
**Error:** Headless environment → `ToolResult.failure("screenshot", "screen capture not available (headless)")`
**Dry-run:** `{"would_capture": True, "region": args.get("region")}`

**Artifact:** `src/capabilities/screen/capture.py`

---

### TASK 9.6 — File Operations Capability (`file_ops`)

**Location:** `src/capabilities/files/file_ops.py`
**Critical security:** Path validation MUST use `Path.resolve()` + `os.path.commonpath()`. No string prefix matching.

**Input:** `{"action": "read"|"write"|"list"|"delete"|"move"|"copy", "path": str, "content": str?, "destination": str?}`

**Validation (`validate()`):**

1. `action` in allowed enum
2. `path` provided
3. `path` resolves within an `allowed_root` using `os.path.commonpath()`
4. `write` requires `content`; `move`/`copy` require `destination`
5. For `move`/`copy`: `destination` must also be within allowed roots

**Actions:**

- `list`: `[{"name", "type", "size_bytes"} for e in Path(path).iterdir()]`
- `read`: `Path(path).read_text(encoding="utf-8")`
- `write`: `Path(path).write_text(content, encoding="utf-8")`
- `delete`: `Path(path).unlink()` (files) or `shutil.rmtree()` (directories)
- `move`: `shutil.move(src, dst)`
- `copy`: `shutil.copy2(src, dst)`

**Dynamic risk:**

```python
def get_risk_level(self, args=None):
    return {"delete": RiskLevel.high, "write": RiskLevel.medium,
            "move": RiskLevel.medium, "copy": RiskLevel.medium,
            "read": RiskLevel.low, "list": RiskLevel.low}.get(
                (args or {}).get("action", "read"), RiskLevel.medium)
```

All errors (`FileNotFoundError`, `PermissionError`, `IsADirectoryError`, `UnicodeDecodeError`) → `ToolResult.failure`.

**Artifact:** `src/capabilities/files/file_ops.py`

---

### TASK 9.7 — Code Executor Capability (`code_exec`)

**Location:** `src/capabilities/coder/executor.py`

**Input:** `{"language": "python"|"javascript"|"bash", "code": str, "timeout_s": int?}` (default timeout: 30)

**Validation (security-critical):**

1. `language` in allowed enum
2. `code` non-empty
3. Baseline scan: reject if code contains `__import__('os').system`, raw `import subprocess`, `open('/etc`, `open('/proc`, `os.system(`

**Execution:**

1. `tmpdir = tempfile.mkdtemp()` with permissions `0o700`
2. Write code to `{tmpdir}/code.{ext}`
3. `subprocess.run([interpreter, code_file], capture_output=True, timeout=timeout_s, cwd=tmpdir, env={})`
4. Always `shutil.rmtree(tmpdir)` in `finally` block

**Output:** `ToolResult(success=(returncode==0), data={"stdout": str, "stderr": str, "returncode": int})`

**Errors:**

- `subprocess.TimeoutExpired` → `ToolResult.failure("code_exec", f"timeout after {timeout_s}s")`
- `FileNotFoundError` → `ToolResult.failure("code_exec", f"{language} interpreter not found")`

**Dry-run:** `{"would_execute": language, "code_length": len(code)}`

**Artifact:** `src/capabilities/coder/executor.py`

---

### TASK 9.8 — Web Search Capability (`web_search`)

**Location:** `src/capabilities/search/web_search.py`

**Input:** `{"query": str, "count": int?}` (count defaults to 5)
**Implementation:** `GET https://html.duckduckgo.com/html/?q={quote(query)}` with `User-Agent: Mozilla/5.0 (JARVIS/3.0)`

**Parse with BeautifulSoup:**

- Titles: `.result__title > a`
- URLs: `.result__url` or anchor href
- Snippets: `.result__snippet`

**Output:** `ToolResult(success=True, data={"results": [{"title", "url", "snippet"}]})`

**Errors:**

- `requests.ConnectionError` → `ToolResult.failure("web_search", "network unavailable")`
- `requests.Timeout` → `ToolResult.failure("web_search", "search request timed out")`
- Empty results → `ToolResult(success=True, data={"results": [], "message": "no results found"})`

**Dry-run:** `{"would_search": query}`

**Artifact:** `src/capabilities/search/web_search.py`

### Definition of Done — Phase 9

- [ ] All 8 capabilities inherit `BaseCapability`, implement all 4 methods
- [ ] All capabilities return `ToolResult` — never raise to caller
- [ ] `file_ops` uses `Path.resolve()` + `os.path.commonpath()` — no string prefix matching
- [ ] `code_exec` always cleans up temp dir in `finally`
- [ ] `app/jarvis_slice.py` migrated — `grep -r "open_app(" src/ app/` returns only definition in `apps.py`

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

### TASK 11.4 — Retry Manager

**Location:** `src/core/runtime/retry.py`
**Purpose:** Per-turn budget counter. One instance per `run_turn()` call — never singleton.

#### Subtask 11.4.1 — Implement `RetryManager`

```python
class RetryManager:
    def __init__(self):
        self._initial = load_config().execution.global_retry_budget  # 8
        self._budget = self._initial

    def consume(self, n: int = 1) -> int:
        self._budget = max(0, self._budget - n)
        return self._budget

    def can_retry(self) -> bool:
        return self._budget > 0

    def reset(self) -> None:
        self._budget = self._initial
```

**Artifact:** `src/core/runtime/retry.py`

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

**Location:** `src/services/telegram/bot.py`
**Purpose:** Async message handler that routes Telegram messages through `run_turn()` via `asyncio.to_thread`.

#### Subtask 14.5.1 — Implement `TelegramBot`

```python
import asyncio
from src.core.runtime.loop import run_turn

class TelegramBot:
    def __init__(self):
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
        response = await asyncio.to_thread(run_turn, user_input, session_id)
        await update.message.reply_text(response.text)

    def start(self) -> None:
        if self._app is None:
            return
        from telegram.ext import MessageHandler, filters
        self._app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        self._app.run_polling()
```

**Artifact:** `src/services/telegram/bot.py`

---

### TASK 14.5.2 — Telegram Command Handlers

**Location:** `src/services/telegram/commands.py`

| Command                              | Action                                                  |
| :----------------------------------- | :------------------------------------------------------ |
| `/start`                             | Reply with JARVIS version and available commands        |
| `/mode SAFE\|BALANCED\|UNRESTRICTED` | Validate mode, call `update_mode()`, reply confirmation |
| `/status`                            | Reply with current model, mode, turn count              |
| `/quit`                              | Reply "Goodbye." — bot continues for other users        |

**Artifact:** `src/services/telegram/commands.py`

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
    async def send_event(event):
        await websocket.send_json(event)
    EventBus().subscribe(EVT_STATE_TRANSITION, lambda e: asyncio.create_task(send_event(e)))
    EventBus().subscribe(EVT_TURN_COMPLETE, lambda e: asyncio.create_task(send_event(e)))
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
        r = sr.Recognizer()
        while not self._stop.is_set():
            try:
                with sr.Microphone() as source:
                    audio = r.listen(source, timeout=3, phrase_time_limit=3)
                try:
                    text = r.recognize_google(audio).lower()
                    if wake_word in text:
                        callback(text)
                except sr.UnknownValueError:
                    pass
            except Exception:
                pass

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

## Phase 18 — QA + Production

```yaml
phase_id: 18
priority: "P0"
status: "not_started"
total_tasks: 6
blocker: "Phase 17 complete"
next_action: "TASK 18.1"
```

### Theoretical Foundation

Production readiness requires four proofs: performance targets met (fast-path <100ms, simple query <5s), Arabic bilingual operation verified end-to-end, determinism confirmed (identical inputs → identical outputs), and total test coverage above 80%. The release cannot ship without passing all 6 tasks in this phase.

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
# Must contain exactly: 3.0.0
```

**Pass condition:** All tests pass, coverage ≥ 80%, no forbidden patterns found.

---

### TASK 18.5 — VERSION File and Release Notes

**Location:** `VERSION`, `docs/RELEASE_NOTES.md`

#### Subtask 18.5.1 — Create VERSION file

```
3.0.0
```

Single line, no trailing whitespace.

#### Subtask 18.5.2 — Write `docs/RELEASE_NOTES.md`

Required sections:

- **Version:** 3.0.0
- **Release Date:** {date}
- **Hardware Requirements:** RTX 3050 6GB VRAM minimum, 16GB RAM, Intel i5 12th Gen
- **New in v3.0:** Full capability list (13 capabilities), state machine, formal contracts, bilingual support, three safety modes
- **Breaking Changes from v2.x:** Complete architectural rewrite; no migration path from v2.x
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

### Definition of Done — Phase 18

- [ ] `pytest tests/ -v` → all tests pass, 0 failures
- [ ] `pytest tests/ --cov=src` → TOTAL ≥ 80%
- [ ] Fast-path latency < 100ms confirmed by `test_performance.py`
- [ ] Arabic verified end-to-end by `test_arabic.py`
- [ ] Determinism verified by `test_determinism.py`
- [ ] `VERSION` file contains `3.0.0`
- [ ] `docs/RELEASE_NOTES.md` complete
- [ ] No debug `print()` statements in non-interface code
- [ ] No hardcoded paths anywhere in `src/`

---

## Summary

| Metric          | Value                                                                                               |
| :-------------- | :-------------------------------------------------------------------------------------------------- |
| Total phases    | 20 (0–18 + 14.5)                                                                                    |
| Total tasks     | ~135                                                                                                |
| Total subtasks  | ~310                                                                                                |
| Test files      | 18                                                                                                  |
| Config files    | 8                                                                                                   |
| Source modules  | ~65                                                                                                 |
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
[ ] All capabilities implement all 4 abstract methods
[ ] All capabilities return ToolResult — never raise to caller
[ ] AppLauncher.execute(args) used everywhere after Phase 9
[ ] grep -r "open_app(" src/ app/ returns only apps.py definition

Code Quality
[ ] src/__version__ == "3.0.0"
[ ] VERSION file contains 3.0.0
[ ] No debug print() in non-interface code
[ ] No hardcoded paths

Tests
[ ] pytest tests/ -v → all tests pass
[ ] pytest tests/ --cov=src → TOTAL >= 80%
[ ] All three spec files share spec_version: v3.0
[ ] AuditLogger creates data/audit.db after first capability execution
```

---

**JARVIS v3.0 — Execution Plan**
_spec_version: v3.0 | structure_version: 3 | last_updated: 2026-05-03_
_Contract-first. Capabilities sovereign. State machine authoritative. No drift._
