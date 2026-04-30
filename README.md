# JARVIS — Production-Ready Local AI Assistant

## Project Specification v2.0

**Last Updated:** 2026-04-30  
**Hardware Profile:** RTX 3050 (6GB VRAM), 16GB RAM, Intel i5 12th Gen  
**Spec Version:** v2.0 — Production Architecture

---

## 1. System Overview

### What JARVIS Is

JARVIS is a local-first AI assistant that runs entirely on local hardware. It accepts text input in Arabic or English and produces either conversational answers or real system actions (open applications, manage files, send notifications).

### What JARVIS Is NOT

JARVIS is NOT a cloud service. It does NOT require internet connectivity for core functions. The core is fully local. External integrations (Google APIs, Telegram, browser automation, voice input/output, image generation) are optional modules that must be explicitly enabled.

### Core Philosophy

- **Local-first:** All core processing occurs on the local machine.
- **State-machine-first:** The runtime state machine is the single source of truth for execution flow. Layers are implementation detail, not execution control.
- **Deterministic over cleverness:** Identical inputs must produce identical execution paths. No hidden logic, no implicit behavior.
- **Observability-first:** Every state transition, tool call, model swap, and failure MUST be logged with structured data. If it is not logged, it did not happen.
- **Fail-safe defaults:** The system degrades gracefully. It never crashes. It never executes irreversible actions without explicit approval.
- **Isolation of side-effects:** Capabilities execute in a sandbox. Tool execution is separated from reasoning. No capability may call an LLM or make decisions.

---

## 2. System Principles

### 2.1 Determinism Over Cleverness

- Identical inputs produce identical execution paths.
- Scoring formulas are mathematically defined, not heuristic.
- Fallback chains are fixed, not adaptive.
- No randomization in routing or model selection.

### 2.2 Observability-First Design

- Every state transition emits an event.
- Every tool call records arguments, result, and duration.
- Every model call records input length, output length, latency, and VRAM state.
- Every failure records the full context for replay.
- Debug modes (OFF, BASIC, TRACE, RAW) filter existing data; they do not change behavior.

### 2.3 Fail-Safe Defaults

- Execution mode defaults to BALANCED.
- Model fallback chain is Tier 1 (qwen2.5:7b) then Tier 2 (gemma3:4b).
- Invalid decisions are replaced with safe defaults, not retried infinitely.
- The runtime never crashes. All exceptions are caught and handled.

### 2.4 Isolation of Side-Effects

- Capabilities are the ONLY layer that may execute actions.
- Capabilities MUST NOT call LLMs.
- Capabilities MUST NOT make decisions.
- Capabilities MUST NOT access memory directly.
- The execution sandbox isolates each tool call with timeouts and resource limits.

### 2.5 No Hidden Logic

- All routing is defined by the state machine, not by layer code.
- All model selection is defined by weighted scoring, not by hardcoded if/else.
- All safety checks are structured validation, not string pattern matching.
- All approval decisions are enforced by the safety layer, not by prompts.

---

## 3. Architecture

### 3.1 Layer Responsibilities

| Layer | Location | Responsibility | Allowed Behavior | Forbidden Behavior |
|-------|----------|----------------|------------------|-------------------|
| **Interface** | `src/interfaces/` | Input/Output | Display output, receive input, route to runtime | Make decisions, route requests, execute tools |
| **Context** | `src/core/context/` | Context handling, InputPacket assembly | Assemble data for current turn, manage short/long-term context, build prompts | Execute actions, make decisions, access models |
| **Decision** | `src/core/decision/` | Intent classification, model selection via scoring | Select intent, model, mode, estimate risk, compute scores | Execute tools, generate responses, call LLMs |
| **Runtime** | `src/core/runtime/` | State machine orchestration, loop control, execution authority | Control flow via states, enforce limits, coordinate subsystems | Implement tool logic, make decisions, call models directly |
| **Model Manager** | `src/models/manager.py` | VRAM monitoring, model lifecycle, concurrency control | Load/unload models, monitor VRAM, enforce one-model-at-a-time | Make decisions, execute tools, route requests |
| **Models** | `src/models/` | LLM/speech/vision model adapters | Call local Ollama, wrap models, return structured output | Make decisions, route requests, execute tools |
| **Capabilities** | `src/capabilities/` | All executable actions | Execute approved tools within sandbox, return ToolResult | Decision logic, model selection, LLM calls |
| **Memory Engine** | `src/memory/` | Retrieval, scoring, decay/TTL, indexing | Store/retrieve with relevance scoring, apply TTL, maintain indexes | Control runtime, execute actions, make decisions |
| **Safety** | `src/core/safety/` | Structured validation, permission enforcement | Validate args against schemas, enforce execution modes, audit log actions | Execute tools, make decisions, call LLMs |
| **Sandbox** | `src/core/sandbox/` | Safe tool execution environment | Dry-run support, timeout enforcement, resource limits, rollback tracking | Make decisions, route requests |
| **Observability** | `src/core/observability/` | Metrics, tracing, replay, failure analysis | Record traces, compute metrics, enable replay, analyze failures | Control runtime, execute tools, make decisions |
| **Services** | `src/services/` | External system connectors | Telegram, Google APIs, third-party integrations | Core logic, decision making, tool execution |

### 3.2 Decision Boundaries

Decision MUST:
- Select model using dynamic weighted scoring (capability, latency, cost, modality).
- Select mode based on input complexity.
- Estimate risk using structured rules.
- Populate `score_breakdown` and `candidate_list` for validation.
- Set `decision_source` to `fast_path` or `model`.

Decision MUST NOT:
- Execute tools.
- Generate responses.
- Use hard-coded priority tables.
- Apply implicit bias without scoring basis.
- Call LLMs (uses models adapter only for classification if needed).

### 3.3 Runtime Decision Validation

Before using DecisionOutput, Runtime MUST verify:
- `score_breakdown` exists (all factor weights and values recorded).
- `candidate_list` exists (at least 2 models evaluated).
- `decision_source` is set (`fast_path` or `model`).
- `confidence` is a float between 0.0 and 1.0.

**Reject Invalid Decisions:**
- If DecisionOutput lacks `score_breakdown` → replace with safe default (intent=chat, mode=normal, model=gemma3:4b). Do NOT retry.
- If DecisionOutput lacks `candidate_list` → replace with safe default. Do NOT retry.

**Deterministic Fallback Logic:**
1. Decision validation fails → safe default immediately.
2. Model call fails → Tier 1 fallback (qwen2.5:7b).
3. Tier 1 fails → Tier 2 fallback (gemma3:4b).
4. Tier 2 fails → return error response.

**Logging:**
- All candidate scores.
- Selected model.
- Scoring factors used.
- Validation status.
- `decision_source` value.

### 3.4 Runtime Authority

The Runtime state machine is the SOLE authority controlling:
- Flow execution direction (via state transitions).
- Retry decisions and limits (via global retry budget).
- Model switching (via Model Manager).
- Loop termination (via hard limits).
- State transitions (via StateManager).

No other module may control these aspects. Layers implement behavior; the state machine controls when that behavior executes.

### 3.5 Capability Boundaries

Capabilities MUST:
- Execute only (validate and run approved tools within the sandbox).
- Return ToolResult with success/failure status.
- Respect timeout and resource limits.

Capabilities MUST NOT:
- Call LLMs.
- Make decisions.
- Access memory directly.
- Route to other capabilities.

### 3.6 Memory Engine (NOT Just Storage)

The Memory Engine provides:
- **Retrieval strategy:** Keyword-based search with relevance scoring. Short-term (recent turns, session-scoped) and long-term (persistent, searchable across sessions).
- **Scoring system:** Each memory snippet receives a relevance score based on keyword overlap, recency, and user interaction history.
- **Decay / TTL:** Memory entries have a time-to-live. Short-term entries expire after N turns. Long-term entries decay in relevance over time.
- **Indexing:** Keywords are indexed for fast lookup. Index rebuilds periodically, not on every write.

---

## 4. Execution Model: State Machine First

### 4.1 Single Source of Truth

The runtime state machine is the single source of truth for execution flow. Layers implement functionality; the state machine controls when and how that functionality is invoked. There is no layer-to-layer direct calling. All execution flows through state transitions.

### 4.2 States

| State | Description | Allowed Next States |
|-------|-------------|-------------------|
| `IDLE` | Waiting for input | `DECIDING` |
| `DECIDING` | Running decision classifier | `EXECUTING_MODEL`, `ERROR`, `IDLE` |
| `EXECUTING_MODEL` | Calling LLM | `EVALUATING`, `EXECUTING_TOOL`, `ERROR` |
| `EXECUTING_TOOL` | Running approved tool in sandbox | `EVALUATING`, `WAITING_CONFIRMATION`, `ERROR` |
| `WAITING_CONFIRMATION` | Paused for user approval | `EXECUTING_TOOL`, `IDLE` |
| `EVALUATING` | Checking response quality | `DECIDING`, `COMPLETED`, `ERROR` |
| `ERROR` | Failure state | `IDLE` |
| `COMPLETED` | Success state | `IDLE` |

### 4.3 Valid Transitions

```
IDLE → DECIDING → EXECUTING_MODEL → EVALUATING → COMPLETED → IDLE
                                                ↓
                                           EXECUTING_TOOL → EVALUATING
                                                ↓
                                          WAITING_CONFIRMATION → EXECUTING_TOOL

Any state → ERROR → IDLE (safe exit)
```

### 4.4 Invalid Transitions (Rejected)

| From | To | Handling |
|------|-----|----------|
| IDLE | EXECUTING_TOOL | Must go through DECIDING |
| EXECUTING_MODEL | IDLE | Invalid without EVALUATING |
| WAITING_CONFIRMATION | EXECUTING_TOOL | Only after user response |
| Any state | Any non-listed state | Transition rejected, log event, remain in current state |

### 4.5 Execution Flow

Single enforced path per turn: `Observe → Decide → Think → Act → Evaluate`

No phase may proceed before the previous phase is validated. The state machine enforces this ordering.

---

## 5. Hard Limits

| Limit | Value | Purpose |
|-------|-------|---------|
| `max_iterations_per_turn` | 5 | Maximum retry loops per turn |
| `max_tool_calls_per_turn` | 3 | Maximum tool calls per turn |
| `max_tool_depth` | 3 | Maximum nested tool calls |
| `max_decision_retries` | 3 | Maximum decision re-runs (with weight adjustment) |
| `max_model_retries` | 2 | Model call retries per attempt |
| `global_retry_budget` | 8 | Total retries allowed per request (decision + model + tool combined). Prevents infinite loops. |
| `tool_timeout_s` | 30 | Tool execution timeout (seconds) |
| `model_timeout_s` | 120 | LLM call timeout (seconds) |
| `step_timeout_s` | 60 | Timeout per execution step |
| `total_turn_timeout_s` | 300 | Maximum turn time (seconds) |

### 5.1 Global Retry Budget

Every retry (decision retry, model retry, tool retry) consumes from the global retry budget. When the budget reaches 0, the runtime MUST exit with a safe error response. This prevents infinite loops regardless of individual limit enforcement.

Budget consumption:
- Decision retry: -1
- Model retry: -1
- Tool retry: -1 (same tool MUST NOT be retried; different tool is allowed)
- Evaluation retry: -1

### 5.2 Loop Protection

- Same tool called 3+ times in one turn → block, return warning response.
- Repeated pattern in tool history → detect and block.
- `max_same_action_repeats` = 3.

### 5.3 Timeout Hierarchy

Timeouts are nested. The innermost timeout fires first:

1. `tool_timeout_s` (30s) — per tool call.
2. `step_timeout_s` (60s) — per execution step.
3. `model_timeout_s` (120s) — per model call.
4. `total_turn_timeout_s` (300s) — entire turn.

When a timeout fires, the runtime transitions to ERROR and returns a safe response.

---

## 6. Decision System

### 6.1 Fast Path vs Model Path

The decision system has two paths:

- **Fast path (`decision_source = fast_path`):** Rule-based matching for common intents. Does NOT call an LLM. Returns a DecisionOutput immediately. Examples: "open X" → tool_use, "what is" → chat.
- **Model path (`decision_source = model`):** Uses a lightweight LLM to classify intent when fast path does not match. Returns a DecisionOutput with full scoring.

The fast path is NOT hardcoded routing. It is an optimization for well-defined patterns. When fast path does not match, the system falls through to model-based classification. Both paths produce identical DecisionOutput structures.

### 6.2 Dynamic Weighted Scoring

Model selection uses weighted scoring:

```
score(model) = Σ (weight_factor_i * normalized_value_i)
```

**Normalization:**
- `capability`: 0.0–1.0 (reasoning_tier mapped: low=0.3, medium=0.6, high=1.0)
- `latency`: 0.0–1.0 (fast=1.0, medium=0.6, slow=0.3)
- `cost`: 0.0–1.0 (VRAM estimate normalized: lower VRAM = higher score)
- `modality_relevance`: 0.0–1.0 (1.0 if modality matches input type, 0.0 otherwise)

**Weights (from config/models.yaml):**
- `fit_complexity`: 1.0
- `fit_mode`: 1.0
- `cost_penalty`: 0.35
- `quality_need`: 1.2
- `memory_bias`: 0.25

**Variability Margin:**
±0.05 margin where multiple models are valid. Prevents deterministic lock when scores are effectively equal.

**Tie-Break Logic (applied when scores within margin):**
1. Lower cost (VRAM) wins.
2. Lower latency wins.
3. Recent success rate wins.

**Confidence Handling:**
- Confidence >= 0.8: Use decision as-is.
- Confidence 0.5–0.8: Apply gracefully (proceed but log lower confidence).
- Confidence < 0.5: Trigger graceful degradation — use safe defaults, log warning.
- Missing confidence: Treat as 0.0, apply safe defaults.

### 6.3 Decision Retry Strategy

`max_decision_retries` = 3. Each retry MUST:
- Adjust scoring weights slightly (±0.05 on fit_complexity), OR
- Reduce constraints (accept lower confidence threshold).

After retries exhausted:
- Trigger tiered fallback system.
- Do NOT retry beyond 3 attempts.

### 6.4 Tiered Fallback System

**Fallback Tier 1:** qwen2.5:7b
- Use for: reasoning, planning, complex responses.
- Attempt before Tier 2.

**Fallback Tier 2:** gemma3:4b
- Use for: simple responses, complete failure.
- ONLY used if Tier 1 fails.

### 6.5 Mode Degradation

Only degrade mode IF:
- Failure occurred, OR
- Retry triggered.

Progression: `deep → normal → fast`

If failure persists → reduce mode complexity step-by-step.

### 6.6 Response Quality Guard

Apply ONLY on:
- Long responses (>500 tokens).
- Complex tasks (reasoning, planning, research).
- Fallback outputs.

Validate:
- Completeness (answer is not truncated).
- Coherence (logical consistency).
- Relevance (addresses input).

If validation fails → retry with stronger model (consuming global retry budget).

---

## 7. Model Manager

### 7.1 Purpose

The Model Manager centralizes model lifecycle, VRAM monitoring, and concurrency control. It replaces ad-hoc model loading with a managed system.

### 7.2 Responsibilities

- **VRAM Monitoring:** Continuous monitoring of GPU memory. Triggers automatic downgrade when available VRAM < 1GB.
- **Model Lifecycle:** Load, unload, swap models. Ensures one model at a time. Unload before loading a new model.
- **Concurrency Control:** Prevents concurrent model calls. Serializes all model requests.
- **Dynamic Availability:** Models that exceed available VRAM are marked unavailable and excluded from scoring.

### 7.3 VRAM Budget (Dynamic, Not Static)

The system does NOT use static VRAM assumptions. VRAM availability is checked at runtime:

| Model | Approx. VRAM | Notes |
|-------|-------------|-------|
| `gemma3:4b` | ~3.0 GB | Always available (base model) |
| `qwen3:8b` | ~5.0 GB | Available when VRAM permits |
| `qwen2.5-coder:7b` | ~4.7 GB | Available when VRAM permits |
| `llava:7b` | ~4.5 GB | Available when VRAM permits |

**Heavy Module VRAM (added when active):**
- Browser (Playwright): +500 MB VRAM, +2 GB RAM.
- Voice (Whisper): +500 MB VRAM, +1 GB RAM.
- Image Generation: +2 GB VRAM, +2 GB RAM (CPU fallback possible).

### 7.4 Coexistence Strategy

Lightweight and heavy models may coexist via sequential loading:
1. Heavy model loads for complex task.
2. Heavy model unloads after completion.
3. Lightweight model (gemma3:4b) loads for follow-up.
4. Model Manager tracks current loaded state and transition cost.

---

## 8. Execution Sandbox

### 8.1 Purpose

The Execution Sandbox provides a safe environment for tool execution with timeout enforcement, resource limits, dry-run support, and rollback tracking.

### 8.2 Features

- **Timeout Enforcement:** Each tool call is wrapped with a timeout. Hard timeout at `tool_timeout_s` (30s).
- **Resource Limits:** Memory and CPU limits per tool execution. Prevents runaway processes.
- **Dry-Run Support:** Every capability supports a dry-run mode that returns what WOULD happen without executing. Used for confirmation prompts.
- **Rollback Tracking:** Reversible vs irreversible actions are tracked. Irreversible actions require explicit user approval in BALANCED mode.

### 8.3 Action Classification

| Type | Examples | Approval Required (BALANCED) |
|------|----------|----------------------------|
| **Reversible** | File read, clipboard read, screenshot, search | Low risk: auto-execute |
| **Reversible with side-effect** | File write, clipboard write, notification | Medium risk: confirm |
| **Irreversible** | File delete, app launch (cannot undo launch) | High risk: confirm or block |

### 8.4 Audit Log

Every tool execution records:
- Timestamp.
- Tool name and arguments.
- Result (success/failure, data, error).
- Duration.
- Dry-run or actual execution.
- Approval status (auto/confirmed/blocked).

---

## 9. Safety System

### 9.1 Structured Validation (Not String Matching)

Safety validation uses structured schema validation, not string pattern matching:

1. **Schema Validation:** Tool arguments are validated against a Pydantic schema defined per capability. Invalid types, missing fields, or out-of-range values are rejected.
2. **Path Validation:** File paths are validated against allowed root directories. Path traversal attacks (../) are blocked.
3. **Command Validation:** Shell commands are validated against a whitelist of allowed operations. Dangerous patterns are blocked by the sandbox, not by string matching.

### 9.2 Approval Outside Model

Approval decisions are enforced by the Safety layer, NOT by prompts. The model cannot override safety rules. The approval flow is:

1. Runtime receives tool call from LLM output.
2. Safety layer validates schema, paths, and risk level.
3. Safety layer checks execution mode (SAFE/BALANCED/UNRESTRICTED).
4. If approval required → transition to WAITING_CONFIRMATION state.
5. User approves or denies → runtime continues or aborts.

### 9.3 Execution Modes

| Mode | Description | Behavior |
|------|-------------|----------|
| `SAFE` | Confirm all | Every tool requires explicit user confirmation |
| `BALANCED` | Smart default | Low risk: auto-execute; Medium risk: confirm; High risk: blocked (override via `confirm: {tool_name}`) |
| `UNRESTRICTED` | Full access | No confirmation (schema and path validation still apply) |

**Default:** `BALANCED`

### 9.4 Risk Classification

| Risk Level | SAFE | BALANCED | UNRESTRICTED |
|------------|------|----------|--------------|
| `low` | Confirm | Auto-execute | Auto-execute |
| `medium` | Confirm | Confirm | Auto-execute |
| `high` | Confirm | Blocked* | Auto-execute |

*In BALANCED mode, high-risk tools can execute if the user explicitly types: `confirm: {tool_name}`

### 9.5 Three-Gate Permission System

Before any tool executes, THREE gates MUST pass:

**Gate 1: Decision Consistency**
- Does the tool match the declared intent?
- Does the tool align with what the model committed to?

**Gate 2: Argument Safety**
- Are paths within allowed roots?
- Does the argument schema validate?
- Are commands within the allowed whitelist?

**Gate 3: User Context**
- Does the tool match user intent from recent history?
- Do recent messages conflict with this tool call?

### 9.6 Audit Log Per Action

Every action (allowed or blocked) is logged to the audit trail with:
- Timestamp, session_id, turn_id.
- Tool name and arguments.
- Gate results (Gate 1: pass/fail, Gate 2: pass/fail, Gate 3: pass/fail).
- Final decision (allow/confirm/block).
- Reason for block (if applicable).

---

## 10. Observability System

### 10.1 Purpose

The Observability System provides metrics, tracing, replay, and failure analysis. It replaces the basic logging approach with production-grade observability.

### 10.2 Metrics

- **Latency:** Per-phase latency (decision, model, tool, evaluation).
- **Throughput:** Turns per minute, tool calls per minute.
- **Error Rate:** Failures per turn, by phase.
- **Model Usage:** Calls per model, swap frequency, VRAM utilization.
- **Retry Rate:** Retries per turn, by type (decision/model/tool).

### 10.3 Tracing

Every turn generates a trace with:
- Trace ID (unique per turn).
- Span for each phase (decision, model, tool, evaluation).
- Span attributes: input, output, latency, state transitions.
- Parent-child relationships for nested operations.

### 10.4 Replay

`/replay <turn_id>` shows complete turn trace:
- All state transitions with timestamps.
- Raw LLM input/output (in RAW debug mode).
- Parsed decisions with score breakdowns.
- Tool calls with arguments and results.
- Safety gate results.
- Final response.

### 10.5 Failure Analysis

The Observability System maintains a failure index:
- Aggregates failures by type, phase, and tool.
- Identifies recurring failure patterns.
- Provides context for each failure (input, state, decision).

### 10.6 Structured Log Format

Every log entry includes:
- `timestamp` (ISO 8601).
- `level` (DEBUG, INFO, WARNING, ERROR, CRITICAL).
- `event` (event type name).
- `session_id` (string).
- `turn_id` (integer).
- `phase` (current execution phase).
- `trace_id` (unique per turn).
- `data` (key=value pairs, event-specific).

### 10.7 Event Types

| Event | Fields |
|-------|--------|
| `runtime.state` | from, to, timestamp |
| `turn.start` | session, input_len, turn, trace_id |
| `decision` | intent, model, risk_level, decision_source, confidence |
| `decision.validation` | valid, score_breakdown, candidate_count |
| `model.start` | model, input_len, timeout |
| `model.done` | model, output_len, duration_ms, success |
| `model.swap` | from, to, reason |
| `model.error` | model, error_type, retry_count |
| `tool.start` | name, args, dry_run |
| `tool.done` | name, success, duration_ms |
| `tool.loop_detected` | name, call_count, call_history |
| `tool.timeout` | name, timeout_s, elapsed |
| `safety.gate` | gate_number, tool, result, reason |
| `safety.approval` | tool, decision (allow/confirm/block), mode |
| `parse.failure` | attempt, raw_length, error_type |
| `timeout` | phase, elapsed, limit |
| `degradation` | event_type, system_state |
| `turn.end` | quality, total_ms, state, retry_budget_remaining |

### 10.8 Debug Modes

| Mode | Enabled Via | Output |
|------|------------|--------|
| OFF | Default | Error and warning events only |
| BASIC | `--debug` | Key decisions, model swaps, tool calls |
| TRACE | `--trace` | Full step trace, all events, state transitions |
| RAW | `--debug --raw` | LLM input/output shown, full trace |

---

## 11. Data Contracts

### 11.1 InputPacket

**Purpose:** Bundles all input data for a turn.  
**Produced by:** `context.assembler.assemble_context()`  
**Consumed by:** `runtime.loop.run_turn()`

```json
{
  "user_message": "string (required)",
  "session_id": "string (required)",
  "attachments": "list[Attachment] (default: [])",
  "memory_snippets": "list[MemorySnippet] (default: [])",
  "recent_history": "list[Message] (default: [])",
  "user_profile": "UserProfile (required)",
  "tool_results": "list[ToolResult] (default: [])",
  "turn_number": "int (default: 0)"
}
```

### 11.2 DecisionOutput

**Purpose:** Contains the decision on how to handle the input.  
**Produced by:** `decision.decide()`  
**Consumed by:** `runtime.executor.execute_turn()`

```json
{
  "intent": "chat|code|tool_use|search|vision|research|voice (required)",
  "complexity": "low|medium|high (required)",
  "mode": "fast|normal|deep|planning|research (required)",
  "model": "string (required, model tag)",
  "requires_tools": "bool (required)",
  "requires_planning": "bool (default: false)",
  "tool_name": "string|null (default: null)",
  "tool_args": "dict (default: {})",
  "confidence": "float 0.0-1.0 (required)",
  "risk_level": "low|medium|high (required)",
  "decision_source": "fast_path|model (required)",
  "score_breakdown": "dict (required)",
  "candidate_list": "list[ModelScore] (required)"
}
```

**Validation Notes:**
- `intent` must be one of the allowed values.
- `tool_name` must be null if `requires_tools` is false.
- `score_breakdown` must contain all scoring factors with weights and normalized values.
- `candidate_list` must contain at least 2 model scores.
- `decision_source` must be `fast_path` or `model`.

### 11.3 LLMOutput

**Purpose:** Output from the LLM.  
**Produced by:** `runtime.executor.execute_turn()`  
**Consumed by:** `runtime.loop`

```json
{
  "type": "answer|tool_call (required)",
  "content": "string (required if type=answer)",
  "tool": "string|null (required if type=tool_call)",
  "args": "dict (default: {})"
}
```

**Enforcement Rule:** When `requires_tools=True`, the model MUST produce `tool_call` type. Free text when tool required is a parse failure that triggers retry (consuming global retry budget).

### 11.4 ToolResult

**Purpose:** Result from tool execution.  
**Produced by:** `capabilities.executor.execute()`  
**Consumed by:** `runtime.loop`

```json
{
  "tool": "string (required)",
  "success": "bool (required)",
  "data": "dict (default: {})",
  "error": "string (default: '')",
  "duration_ms": "float (default: 0.0)",
  "dry_run": "bool (default: false)"
}
```

### 11.5 FinalResponse

**Purpose:** Final output to the user.  
**Produced by:** `runtime.loop`  
**Consumed by:** Interface layer

```json
{
  "text": "string (required)",
  "session_id": "string (required)",
  "model": "string (required)",
  "mode": "string (required)",
  "quality": "float 0.0-1.0 (required)",
  "decision_source": "fast_path|model (required)",
  "degraded": "bool (default: false)",
  "turn_id": "int (required)"
}
```

---

## 12. Hardware-Aware Model Strategy

### 12.1 Target Hardware

- GPU: NVIDIA RTX 3050 (6GB VRAM)
- RAM: 16 GB
- CPU: Intel Core i5 12th Gen

### 12.2 Performance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| Fast-path latency | < 100ms | Decision to response (no model call) |
| Simple query latency | < 5s | Input to FinalResponse (single model call) |
| Complex query latency | < 30s | Input to FinalResponse (with tool calls) |
| VRAM peak | < 5.5 GB | 0.5 GB headroom for OS |
| RAM peak | < 14 GB | 2 GB headroom for OS |
| Tool execution | < 30s | Per tool call timeout |

### 12.3 Strict Rules

1. **ONE model at a time.** Unload before loading a new model.
2. **No concurrent model calls.** Serialized by Model Manager.
3. **Automatic downgrade** when available VRAM < 1GB.
4. **Dynamic VRAM checks** at runtime, not static assumptions.
5. **Heavy modules** (Browser, Voice, Image Gen) are optional and must be explicitly enabled.

---

## 13. Failure Modes

### 13.1 Model Timeout

**Detection:** No response within `model_timeout_s` (120s).

**Fallback:**
1. Retry once with the same model (max_model_retries = 2, consumes global budget).
2. Swap to Tier 1 fallback (qwen2.5:7b).
3. Swap to Tier 2 fallback (gemma3:4b).
4. Return error response.

### 13.2 Invalid Output

**Detection:** DecisionOutput has invalid fields OR LLMOutput fails JSON parsing.

**Fallback:**
1. Replace with safe defaults (intent=chat, mode=normal, model=default). Do NOT retry decision.
2. If LLMOutput parse fails → retry with correction prompt (max 2 attempts, consumes global budget).
3. If all retries fail → return answer without tool.

### 13.3 Tool Failure

**Detection:** ToolResult.success == false.

**Fallback:**
1. Log the failure with full context.
2. Add error context to input.
3. Allow continuation with a different tool (DO NOT retry same tool).
4. Consume from global retry budget.

### 13.4 Loop Detection

**Detection:** Same tool called 3+ times OR repeated pattern in tool history.

**Fallback:**
1. Block execution immediately.
2. Return warning response.
3. Log `tool.loop_detected` event.
4. Do NOT retry.

### 13.5 Global Budget Exhaustion

**Detection:** Global retry budget reaches 0.

**Fallback:**
1. Stop all retries immediately.
2. Return exhaustion response.
3. Log `turn.end` with retry_budget_remaining = 0.

### 13.6 Runtime Guarantee

The runtime never crashes. All exceptions are caught at the state machine level and transition to ERROR state, then to IDLE.

---

## 14. Optional Modules

### 14.1 Core (Always Active)

| Module | Description | Location |
|--------|-------------|----------|
| Interface | CLI chat | `src/interfaces/cli/` |
| Context | InputPacket assembly | `src/core/context/` |
| Decision | Intent classification | `src/core/decision/` |
| Runtime | State machine, loop | `src/core/runtime/` |
| Model Manager | VRAM, lifecycle, concurrency | `src/models/manager.py` |
| Models | Ollama wrapper | `src/models/` |
| Capabilities | Action implementations | `src/capabilities/` |
| Memory Engine | Retrieval, scoring, TTL, indexing | `src/memory/` |
| Safety | Permission, mode enforcement | `src/core/safety/` |
| Sandbox | Safe tool execution | `src/core/sandbox/` |
| Observability | Metrics, tracing, replay | `src/core/observability/` |

### 14.2 Optional (Must Enable)

| Module | Description | Requires | Location |
|--------|-------------|----------|----------|
| Web UI | Browser interface | FastAPI | `src/interfaces/web/` |
| Telegram | Telegram bot | Bot token | `src/services/telegram/` |
| Google APIs | Calendar, Gmail, Drive | OAuth credentials | `src/services/google/` |
| Web Automation | Playwright automation | Playwright | `src/capabilities/web_automation/` |
| Voice | STT/TTS pipeline | Whisper, Piper | `src/capabilities/voice/` |
| Vision | Image understanding | llava:7b | `src/capabilities/vision/` |
| Image Gen | Stable Diffusion | GPU memory | `src/capabilities/vision/image_gen.py` |

---

## 15. Implementation Mapping

| Phase | Description | Files Created | Location |
|-------|--------------|---------------|----------|
| 0 | First Working System | engine.py, classifier.py, apps.py, jarvis_slice.py | `src/models/llm/`, `src/core/decision/`, `src/capabilities/system/`, `app/` |
| 1 | Foundation + Observability | config.py, logging_setup.py, main.py, metrics.py, tracer.py | `src/core/`, `src/core/observability/`, `app/` |
| 2 | Execution Contract | bundle.py, decision.py, llm_output.py, result.py | `src/core/context/`, `src/core/decision/`, `src/core/runtime/`, `src/capabilities/` |
| 3 | Model Manager + VRAM | manager.py, profiles.py, vram_monitor.py | `src/models/` |
| 4 | Runtime State Machine | loop.py, state.py, state_manager.py, limits.py | `src/core/runtime/` |
| 5 | Decision System | classifier.py, decision.py, fast_path.py, risk.py, scorer.py | `src/core/decision/` |
| 6 | Sandbox + Safety | sandbox.py, permission.py, mode_enforcer.py, classifier.py | `src/core/sandbox/`, `src/core/safety/` |
| 7 | Memory Engine | database.py, retriever.py, scorer.py, ttl.py, indexer.py | `src/memory/` |
| 8 | Capability System | base.py, registry.py, executor.py, validator.py | `src/capabilities/` |
| 9 | System Control Capabilities | apps.py, sysinfo.py, clipboard.py, file_ops.py, toasts.py, capture.py | `src/capabilities/system/`, `src/capabilities/notify/`, `src/capabilities/screen/`, `src/capabilities/files/` |
| 10 | Prompt Builder | builder.py, identity.yaml, mode_fragments.yaml | `src/core/context/`, `config/` |
| 11 | Execution Hardening | timeout.py, degradation.py, escalation.py, fallback.py | `src/core/runtime/` |
| 12 | CLI Interface | chat.py, commands.py, formatting.py | `src/interfaces/cli/` |
| 13 | Web Automation & Browser | browser.py, session.py | `src/capabilities/web_automation/` |
| 14 | Google APIs | auth.py, calendar.py, gmail.py, drive.py | `src/services/google/` |
| 15 | Web UI | app.py, static/index.html | `src/interfaces/web/` |
| 16 | Voice Pipeline | stt.py, tts.py, wake_word.py | `src/capabilities/voice/` |
| 17 | Vision + Image | vision.py, image_gen.py | `src/capabilities/vision/` |
| 18 | QA + Production | tests/, VERSION, RELEASE_NOTES.md | `tests/`, root |

---

## 16. Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Pull required models (choose based on VRAM)
ollama pull gemma3:4b   # ~3GB - always available (Tier 2 fallback)
ollama pull qwen3:8b     # ~5GB - primary model

# Configure
cp config/settings.example.yaml config/settings.yaml
cp .env.example .env

# Run with debug
python app/main.py --interface cli --debug
```

---

**Version 2.0** — Spec version v2.0 — Production Architecture — For RTX 3050 (6GB VRAM) system
