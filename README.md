# JARVIS — Production-Ready Local AI Assistant

## Project Specification v1.0

**Last Updated:** 2026-04-24  
**Hardware Profile:** RTX 3050 (6GB VRAM), 16GB RAM, Intel i5 12th Gen  
**Spec Version:** final

---

## 1. System Overview

### What JARVIS Is

JARVIS is a local-first AI assistant that runs entirely on local hardware. It accepts text input in Arabic or English and produces either conversational answers or real system actions (open applications, manage files, send notifications).

### What JARVIS Is NOT

JARVIS is NOT a cloud service. It does NOT require internet connectivity for core functions. The core is fully local. External integrations (Google APIs, Telegram, browser automation, voice input/output, image generation) are optional modules that must be explicitly enabled.

### Core Philosophy

- **Local-first:** All core processing occurs on the local machine.
- **Modular:** Each layer has a single defined responsibility.
- **Controllable:** Execution modes determine confirmation requirements.
- **Hardware-aware:** Optimized for 6GB VRAM constraint.

---

## 2. Architecture

### Layer Responsibilities

| Layer | Location | Responsibility | Allowed Behavior | Forbidden Behavior |
|-------|----------|----------------|------------------|-------------------|
| **Interface** | `src/interfaces/` | Input/Output | Display output, receive input | Make decisions, route requests |
| **Context** | `src/core/context/` | Bundle InputPacket | Assemble data for current turn | Store across turns |
| **Decision** | `src/core/decision/` | Intent classification | Select intent, model, mode | Generate content |
| **Runtime** | `src/core/runtime/` | State machine, loop control | Control execution flow | Implement tool logic |
| **Tools** | `src/core/tools/` | Registry, safety, execution | Validate and execute tools | Call LLM or make routing |
| **Skills** | `src/skills/` | Tool implementations | Execute specific actions | Make routing decisions |
| **Memory** | `src/core/memory/` | Data persistence | Store/retrieve data | Control runtime |
| **Models** | `src/models/` | LLM wrapper | Call local Ollama | Make decisions |
| **Identity** | `src/core/identity/` | Prompt building | Build system prompts | Execute tools |

### Runtime Authority

The Runtime is the sole authority controlling:
- Flow execution direction
- Retry decisions and limits
- Model switching
- Loop termination
- State transitions

No other module may control these aspects.

---

## 3. Runtime State Machine

### States

| State | Description | Allowed Next States |
|-------|-------------|-------------------|
| `IDLE` | Waiting for input | `DECIDING` |
| `DECIDING` | Running decision classifier | `EXECUTING_MODEL`, `ERROR`, `IDLE` |
| `EXECUTING_MODEL` | Calling LLM | `EVALUATING`, `EXECUTING_TOOL`, `ERROR` |
| `EXECUTING_TOOL` | Running approved tool | `EVALUATING`, `ERROR` |
| `WAITING_CONFIRMATION` | Paused for user approval | `EXECUTING_TOOL`, `IDLE` |
| `EVALUATING` | Checking response quality | `DECIDING`, `COMPLETED`, `ERROR` |
| `ERROR` | Failure state | `IDLE` |
| `COMPLETED` | Success state | `IDLE` |

### Valid Transitions

```
IDLE → DECIDING → EXECUTING_MODEL → EVALUATING → COMPLETED → IDLE
                                                ↓
                                           EXECUTING_TOOL → EVALUATING
                                                ↓
                                          WAITING_CONFIRMATION → EXECUTING_TOOL

Any state → ERROR → IDLE (safe exit)
```

### Invalid Transitions (Rejected)

| From | To | Handling |
|------|-----|----------|
| IDLE | EXECUTING_TOOL | Must go through DECIDING |
| EXECUTING_MODEL | IDLE | Invalid without EVALUATING |
| WAITING_CONFIRMATION | EXECUTING_TOOL | Only after user response |

---

## 4. Execution Flow

### Hard Limits

| Limit | Value | Purpose |
|-------|-------|---------|
| `max_iterations` | 5 | Maximum retry loops per turn |
| `max_tool_depth` | 3 | Maximum nested tool calls |
| `max_retries` | 2 | Model call retries per attempt |
| `tool_timeout_s` | 30 | Tool execution timeout (seconds) |
| `model_timeout_s` | 120 | LLM call timeout (seconds) |
| `total_turn_timeout_s` | 300 | Maximum turn time (seconds) |

### Execution Loop Pseudocode

```
run_turn(user_input, session_id):
  SET iteration = 0
  SET tool_depth = 0
  SET state = IDLE

  input = assemble_context(user_input, session_id)

  WHILE iteration < max_iterations:
    TRANSITION to DECIDING
    decision = decide(input)

    IF invalid decision:
      force to defaults (intent=chat, mode=normal)

    TRANSITION to EXECUTING_MODEL
    output = execute_turn(decision, input)

    IF elapsed > total_turn_timeout:
      RETURN timeout_response

    IF output.type == "tool_call":
      IF tool_depth >= max_tool_depth:
        RETURN error("tool depth exceeded")

      TRANSITION to EXECUTING_TOOL
      result = execute_tool(output.tool, output.args)

      tool_depth += 1

      IF repeated_tool(output.tool):
        RETURN warning_response

      IF result.success == false:
        input.tool_results.append(result)
        iteration += 1
        CONTINUE

      input.tool_results.append(result)
      TRANSITION to EVALUATING
      CONTINUE

    IF output.type == "answer":
      TRANSITION to EVALUATING
      eval = evaluate(output, decision)

      IF eval.should_retry AND iteration < max_iterations - 1:
        iteration += 1
        TRANSITION to DECIDING
        CONTINUE

      TRANSITION to COMPLETED
      BREAK

  IF iteration >= max_iterations:
    RETURN exhaustion_response

  save to memory
  RETURN FinalResponse
```

---

## 5. Data Contracts

### InputPacket

**Purpose:** Bundles all input data for a turn.  
**Produced by:** `context.assembler.assemble_context()`  
**Consumed by:** `runtime.loop.run_turn()`

```json
{
  "user_message": "string (required)",
  "session_id": "string (required)",
  "attachments": "list[Attachment] (default: [])",
  "memory_snippets": "list[str] (default: [])",
  "recent_history": "list[Message] (default: [])",
  "user_profile": "UserProfile (required)",
  "tool_results": "list[ToolResult] (default: [])",
  "turn_number": "int (default: 0)"
}
```

### DecisionOutput

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
  "risk_level": "low|medium|high (required)"
}
```

**Validation Notes:** Intent must be one of the allowed values. Tool_name must be null if requires_tools is false.

### LLMOutput

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

**Enforcement Rule:** When `requires_tools=True`, the model MUST produce `tool_call` type. Free text when tool required is a parse failure that triggers retry.

### ToolResult

**Purpose:** Result from tool execution.  
**Produced by:** `tools.executor.execute_tool()`  
**Consumed by:** `runtime.loop`

```json
{
  "tool": "string (required)",
  "success": "bool (required)",
  "data": "dict (default: {})",
  "error": "string (default: '')",
  "duration_ms": "float (default: 0.0)"
}
```

### FinalResponse

**Purpose:** Final output to the user.  
**Produced by:** `runtime.loop`  
**Consumed by:** Interface layer

```json
{
  "text": "string (required)",
  "session_id": "string (required)",
  "model": "string (required)",
  "mode": "string (required)",
  "quality": "float 0.0-1.0 (required)"
}
```

---

## 6. Safety and Permission Model

### Execution Modes

| Mode | Description | Behavior |
|------|-------------|----------|
| `SAFE` | Confirm all | Every tool requires explicit user confirmation |
| `BALANCED` | Smart default | Low auto-executes; medium requires confirmation; high blocked |
| `UNRESTRICTED` | Full access | No confirmation (path/pattern validation still applies) |

**Default:** `BALANCED`

### Risk Classification

| Risk Level | SAFE | BALANCED | UNRESTRICTED |
|------------|------|----------|--------------|
| `low` | Confirm | Auto-execute | Auto-execute |
| `medium` | Confirm | Confirm | Auto-execute |
| `high` | Confirm | Blocked* | Auto-execute |

*In BALANCED mode, high-risk tools can execute if the user explicitly types the approval phrase: `confirm: {tool_name}`

### Tool Permission Layer

Three gates MUST pass before any tool executes:

**Gate 1: Decision Consistency**
- Does the tool match the declared intent?
- Does the tool align with what the model committed to?

**Gate 2: Argument Safety**
- Are paths within allowed roots?
- Do commands contain dangerous patterns?

**Gate 3: User Context**
- Does the tool match user intent?
- Do recent messages conflict?

### Dangerous Patterns (Always Blocked)

These patterns are blocked regardless of risk level or execution mode:

```
rm -rf /, format c:, del /s /q, :(){:|:&};:, shutdown, reboot, mkfs, dd if=, curl | bash, wget | bash, chmod 777
```

---

## 7. Hardware-Aware Model Strategy

### Target Hardware

- GPU: NVIDIA RTX 3050 (6GB VRAM)
- RAM: 16 GB
- CPU: Intel Core i5 12th Gen

### VRAM Budget

| Model | VRAM Used | Safe? |
|-------|-----------|-------|
| `gemma3:4b` | 3.0 GB | Yes (3GB headroom) |
| `qwen3:8b` | 5.0 GB | Tight (1GB headroom) |
| `qwen2.5-coder:7b` | 4.7 GB | Tight |
| `llava:7b` | 4.5 GB | Tight |

### Strict Rules

1. **ONE model at a time.** Unload before loading a new model.
2. **No concurrent model calls.**
3. **Automatic downgrade** when VRAM < 1GB available.

### Model Selection Priority

| Use Case | Preferred | Fallback | Notes |
|---------|-----------|----------|-------|
| Fast classification (<20 chars) | gemma3:4b | None | Use fast-path |
| General chat | qwen3:8b | gemma3:4b | Swap needed |
| Complex reasoning | qwen3:8b | gemma3:4b | May retry |
| Code | qwen2.5-coder:7b | qwen3:8b | Requires swap |
| Vision | llava:7b | Error | Requires swap (optional) |

### Optional Heavier Modules

These modules require additional resources and should be used selectively:

| Module | Additional VRAM | Additional RAM | Notes |
|--------|----------------|----------------|--------------|------|
| Browser (Playwright) | +500 MB | +2 GB | Launch separate process |
| Voice (Whisper) | +500 MB | +1 GB | Optional |
| Image Generation | +2 GB | +2 GB | CPU fallback possible |

---

## 8. Logging, Tracing, and Replay

### Structured Logs

Every log entry includes:
- `timestamp`
- `level`
- `event`
- `session_id`
- `turn_id`
- `phase`
- `data` (key=value pairs)

### Event Types

| Event | Fields |
|-------|--------|
| `runtime.state` | from, to, timestamp |
| `turn.start` | session, input_len, turn |
| `decision` | intent, model, risk_level |
| `tool.start` | name, args |
| `tool.done` | name, success, duration_ms |
| `tool.loop_detected` | name, call_history |
| `parse.failure` | attempt, raw_length |
| `model.swap` | from, to |
| `model.error` | model, error_type |
| `timeout` | phase, elapsed |
| `turn.end` | quality, total_ms |

### Debug Modes

| Mode | Enabled Via | Output |
|------|------------|--------|
| OFF | Default | No debug info |
| BASIC | `--debug` | Key decisions |
| TRACE | `--trace` | Full step trace |
| RAW | `--debug --raw` | LLM input/output shown |

### Replay Support

`/replay <turn_id>` shows complete turn trace including:
- All state transitions
- Raw LLM input/output
- Parsed decisions
- Tool calls with arguments
- Tool results

---

## 9. Failure Handling

### Model Failure

**Detection:** No response within model_timeout_s.

**Handling:**
1. Retry once with the same model.
2. If still failing: swap to fallback model (gemma3:4b).
3. If fallback also fails: return error response.

**Runtime never crashes.**

### Parse Failure

**Detection:** Invalid JSON when tool is required.

**Handling:**
1. Retry with correction prompt (up to max_retries).
2. If all retries exhausted: return answer without tool.
3. Log: parse.failure, raw_output.

### Tool Failure

**Detection:** ToolResult.success == false.

**Handling:**
- Log the failure.
- Add error context to input.
- Allow continuation with a different tool.
- DO NOT retry the same tool (prevents infinite loops).

### Timeout

**Detection:** Elapsed > total_turn_timeout_s.

**Handling:**
- Complete current step if possible.
- Append "(partial)" to response.
- Return best-effort response.

### Invalid Decision

**Detection:** DecisionOutput has invalid fields.

**Handling:**
- Force to defaults (intent=chat, mode=normal, model=default).
- Log decision.invalid.

### Memory Failure

**Detection:** SQLite connection fails.

**Handling:**
- Continue without persistence.
- Log warning.
- Return valid response.

---

## 10. Optional Modules

### Core (Always Active)

| Module | Description |
|--------|-------------|
| Interface | CLI chat |
| Context | InputPacket assembly |
| Decision | Intent classification |
| Runtime | State machine, loop |
| Tools | Registry, validation |
| Skills | Local tool implementations |
| Memory | SQLite persistence |
| Models | Ollama wrapper |
| Identity | Prompt building |

### Optional (Must Enable)

| Module | Description | Requires |
|--------|-------------|----------|
| Web UI | Browser interface | FastAPI |
| Telegram | Telegram bot | Bot token |
| Google APIs | Calendar, Gmail, Drive | OAuth credentials |
| Browser | Playwright automation | Playwright |
| Voice | STT/TTS pipeline | Whisper, Piper |
| Vision | Image understanding | llava:7b |
| Image Gen | Stable Diffusion | GPU memory |

---

## 11. Implementation Mapping

| Phase | Description | Files Created |
|-------|--------------|---------------|
| 0 | First Working System | engine.py, classifier.py, apps.py, jarvis_slice.py |
| 1 | Foundation | config.py, logging_setup.py, main.py |
| 2 | Execution Contract | bundle.py, decision.py, llm_output.py, result.py |
| 3 | Runtime State Machine | loop.py, state.py, state_manager.py |
| 4 | Decision System | classifier.py, decision.py |
| 5 | Prompt Builder | builder.py, identity.yaml |
| 6 | Tool System | base.py, registry.py, executor.py |
| 7 | Safety Modes | mode_enforcer.py, config |
| 8 | System Skills | apps.py, sysinfo.py, clipboard.py, etc. |
| 9 | Runtime Hardening | permission.py, recovery.py |
| 10 | Memory (Simplified) | database.py |
| 11 | Debug System | debug.py |
| 12 | Browser & Web | browser.py, session.py |
| 13 | Google APIs | google_auth.py, calendar.py, etc. |
| 14 | CLI Interface | interface.py |
| 15 | Web UI | app.py, ws.py |
| 16 | Voice Pipeline | stt.py, tts.py, wake_word.py |
| 17 | Vision + Image | llava.py, sd.py |
| 18 | QA + Production | tests/, VERSION |

---

## 12. Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Pull required models (choose based on VRAM)
ollama pull gemma3:4b   # 3GB - always available
ollama pull qwen3:8b     # 5GB - primary

# Configure
cp config/settings.example.yaml config/settings.yaml
cp .env.example .env

# Run with debug
python app/main.py --interface cli --debug
```

---

**Version 1.0** — Spec version final — For RTX 3050 (6GB VRAM) system