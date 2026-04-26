# JARVIS — Execution Engine

## Project Status

```yaml
project:
  name: JARVIS
  version: "1.0"
  spec_version: "final"
  last_updated: "2026-04-24"
  current_phase: 0
  overall_progress_percent: 0
  risk_level: "medium"
  hardware_profile:
    gpu: "RTX 3050 6GB VRAM"
    ram: "16 GB"
    cpu: "Intel Core i5 12th Gen"
  current_blocker: "none"
  next_action: "Start Phase 0"
  validation_status: "not_started"
```

---

## Status Legend

| Marker | Status | Description |
|--------|--------|-------------|
| `[ ]` | not_started | Task not yet started |
| `[~]` | in_progress | Task actively being worked on |
| `[!]` | blocked | Task blocked, needs resolution |
| `[x]` | done | Task verified complete |
| `[>]` | needs_review | Task complete, needs verification |

---

## Phase Progress Summary

| ID | Title | Priority | Status | % | Done/Total | Blocker | Next Action | Last Updated |
|----|-------|----------|--------|---|------------|---------|-------------|--------------|
| 0 | First Working System | P0 | [ ] | 0% | 0/5 | none | Start TASK 0.1 | - |
| 1 | Foundation | P0 | [ ] | 0% | 0/9 | none | Start TASK 1.1 | - |
| 2 | Execution Contract | P0 | [ ] | 0% | 0/6 | none | Start TASK 2.1 | - |
| 3 | Runtime State Machine | P0 | [ ] | 0% | 0/9 | none | Start TASK 3.1 | - |
| 4 | Decision System | P1 | [ ] | 0% | 0/5 | none | Start TASK 4.1 | - |
| 5 | Prompt Builder | P1 | [ ] | 0% | 0/5 | none | Start TASK 5.1 | - |
| 6 | Tool System | P1 | [ ] | 0% | 0/7 | none | Start TASK 6.1 | - |
| 7 | Safety Modes | P1 | [ ] | 0% | 0/4 | none | Start TASK 7.1 | - |
| 8 | System Control Skills | P1 | [ ] | 0% | 0/8 | none | Start TASK 8.1 | - |
| 9 | Runtime Hardening | P0 | [ ] | 0% | 0/6 | none | Start TASK 9.1 | - |
| 10 | Memory (Simplified) | P1 | [ ] | 0% | 0/3 | none | Start TASK 10.1 | - |
| 11 | Debug System | P0 | [ ] | 0% | 0/4 | none | Start TASK 11.1 | - |
| 12 | Browser & Web | P2 | [ ] | 0% | 0/3 | none | Start TASK 12.1 | - |
| 13 | Google APIs | P2 | [ ] | 0% | 0/4 | none | Start TASK 13.1 | - |
| 14 | CLI Interface | P2 | [ ] | 0% | 0/2 | none | Start TASK 14.1 | - |
| 15 | Web UI | P2 | [ ] | 0% | 0/3 | none | Start TASK 15.1 | - |
| 16 | Voice Pipeline | P3 | [ ] | 0% | 0/4 | none | Start TASK 16.1 | - |
| 17 | Vision + Image | P3 | [ ] | 0% | 0/2 | none | Start TASK 17.1 | - |
| 18 | QA + Production | P0 | [ ] | 0% | 0/5 | none | Start TASK 18.1 | - |

---

## Phase 0 — First Working System

```
phase_id: 0
title: "First Working System"
priority: "P0"
status: "not_started"
progress_percent: 0
done_tasks: 0
total_tasks: 5
blocker: "none"
next_action: "Start TASK 0.1"
last_updated: "-"
validation_status: "not_started"
```

### Objective

Create a minimal working system that proves the core pipeline works: text input reaches the LLM and returns a response, and a tool command is classified, routed, and executed.

### Scope

- Text input → LLM call → response output
- Tool command classification → tool execution
- Arabic command support equivalent to English

### Out of Scope

- Full context assembly
- Memory systems
- Multiple execution modes

### Dependencies

None — this is the starting phase.

### Tasks

**TASK 0.1 — Connect to Ollama and get a response**
- [ ] Status: not_started
- Create `src/models/llm/engine.py`
- Implement `chat(message, model)` function
- Call Ollama Python client
- Return response content as string
- **Expected output:** Non-empty string response within 60s
- **Failure cases:** Empty response, exception reaches terminal, timeout > 60s
- **Verification method:** `python -c "from src.models.llm.engine import chat; print(chat('hello'))"`
- **Artifact:** `src/models/llm/engine.py`

**TASK 0.2 — Classify a command and return structured output**
- [ ] Status: not_started
- Create `src/core/decision/classifier.py`
- Implement `classify(message)` function
- Use gemma3:4b with JSON-forcing system prompt
- Handle malformed JSON with retry (max 2)
- Return safe fallback dict on all failures
- **Expected output:** dict with intent, tool_name, tool_args
- **Failure cases:** Invalid dict, wrong intent mapping, exception
- **Verification method:** `python -c "from src.core.decision.classifier import classify; print(classify('open chrome'))"`
- **Artifact:** `src/core/decision/classifier.py`

**TASK 0.3 — Execute an application by name**
- [ ] Status: not_started
- Create `src/skills/system/apps.py`
- Implement `open_app(name)` function
- Cross-platform search (PATH, program directories)
- Return success/error dict without raising
- **Expected output:** `{"success": true, "pid": N}` or `{"success": false, "error": "..."}`
- **Failure cases:** Exception reaches terminal, wrong app opened
- **Verification method:** `python -c "from src.skills.system.apps import open_app; print(open_app('notepad'))"`
- **Artifact:** `src/skills/system/apps.py`

**TASK 0.4 — Wire classifier to tool: text input → action**
- [ ] Status: not_started
- Create `app/jarvis_slice.py`
- Implement `run(user_input)` function
- Connect: input → classify → tool/LLM → output
- Loop on terminal input until "quit"
- **Expected output:** Tool executes or response printed
- **Failure cases:** Loop doesn't exit on "quit", no response
- **Verification method:** Run and type: "open notepad", "what is AI?", "quit"
- **Artifact:** `app/jarvis_slice.py`

**TASK 0.5 — Verify Arabic input**
- [ ] Status: not_started
- Test Arabic commands produce same behavior as English
- Add Arabic examples to classifier if needed
- **Expected output:** Same intent as English equivalent
- **Failure cases:** Different intent for Arabic command vs English
- **Verification method:** Test Arabic equivalent

### Definition of Done

1. "hello" returns non-empty text response.
2. "open notepad" opens Notepad.
3. Arabic equivalents produce identical behavior.
4. "quit" exits cleanly.

### Validation Steps

```bash
python -c "from src.models.llm.engine import chat; print(chat('hello'))"
python -c "from src.skills.system.apps import open_app; print(open_app('notepad'))"
python app/jarvis_slice.py
# Type: "open notepad" → should open Notepad
# Type: "what is AI?" → response
# Type: "quit" → exit
```

### Artifacts

- `src/models/llm/engine.py`
- `src/core/decision/classifier.py`
- `src/skills/system/apps.py`
- `app/jarvis_slice.py`

### AI Instructions

This phase establishes the minimum viable system. Start with TASK 0.1 (Ollama connection) and proceed sequentially. TASK 0.4 wires everything together.

---

## Phase 1 — Foundation

```
phase_id: 1
title: "Foundation"
priority: "P0"
status: "not_started"
progress_percent: 0
done_tasks: 0
total_tasks: 9
blocker: "Phase 0 must complete"
next_action: "Start TASK 1.1"
last_updated: "-"
validation_status: "not_started"
```

### Objective

Establish configuration system, logging infrastructure, and project structure.

### Scope

- Settings YAML and Pydantic loader
- Logging setup with Loguru
- Package skeleton
- Model profiles
- Environment variables
- User profile storage
- Skills manifest
- main.py entry point

### Dependencies

- Phase 0 (completed)

### Tasks

**TASK 1.1 — Settings YAML and Pydantic loader**  
**TASK 1.2 — Logging setup**  
**TASK 1.3 — Package skeleton**  
**TASK 1.4 — Model capability profiles**  
**TASK 1.5 �� LLM engine with VRAM guard**  
**TASK 1.6 — Environment variables**  
**TASK 1.7 — User profile**  
**TASK 1.8 — Skills manifest**  
**TASK 1.9 — main.py entry point**

### Definition of Done

`python app/main.py --interface cli` runs all boot steps and prints "Jarvis ready".

### Validation Steps

```bash
python app/main.py --interface cli
# Should see: jarvis starting → directories created → logging init → jarvis ready
# Ctrl+C should exit without traceback
```

### Artifacts

- `config/settings.yaml`
- `src/core/config.py`
- `src/core/logging_setup.py`
- `src/models/profiles.py`
- `src/models/llm/engine.py`
- `src/core/memory/user_profile.py`
- `config/skills.yaml`
- `.env`
- `app/main.py`

### Human Checkpoint

After TASK 1.9, manually test Ctrl+C exit and verify "Jarvis ready" appears.

---

## Phase 2 — Execution Contract

```
phase_id: 2
title: "Execution Contract"
priority: "P0"
status: "not_started"
progress_percent: 0
done_tasks: 0
total_tasks: 6
blocker: "Phase 1 must complete"
next_action: "Start TASK 2.1"
last_updated: "-"
validation_status: "not_started"
```

### Objective

Define strict data contracts that bind all components.

### Dependencies

- Phase 1 (completed)

### Tasks

**TASK 2.1 — Define InputPacket**  
**TASK 2.2 — Define DecisionOutput**  
**TASK 2.3 — Define LLMOutput**  
**TASK 2.4 — Define ToolResult**  
**TASK 2.5 — Define FinalResponse**  
**TASK 2.6 — Contract tests**

### Definition of Done

All five contract types instantiate correctly and reject invalid data.

### Validation Steps

```bash
python -c "
from src.core.context.bundle import InputPacket
from src.core.decision.decision import DecisionOutput
from src.core.runtime.llm_output import LLMOutput
from src.core.tools.result import ToolResult
from src.core.runtime.final_response import FinalResponse

p = InputPacket(user_message='hello', session_id='s1')
d = DecisionOutput(intent='chat', complexity='low', mode='fast', model='gemma3:4b', requires_tools=False, requires_planning=False, confidence=0.9, risk_level='low')
print('Contracts valid')
"
```

### Artifacts

- `src/core/context/bundle.py`
- `src/core/decision/decision.py`
- `src/core/runtime/llm_output.py`
- `src/core/tools/result.py`
- `src/core/runtime/final_response.py`
- `tests/test_contracts.py`

---

## Phase 3 — Runtime State Machine

```
phase_id: 3
title: "Runtime State Machine"
priority: "P0"
status: "not_started"
progress_percent: 0
done_tasks: 0
total_tasks: 9
blocker: "Phase 2 must complete"
next_action: "Start TASK 3.1"
last_updated: "-"
validation_status: "not_started"
```

### Objective

Implement the state machine that controls runtime with hard limits.

### Dependencies

- Phase 2 (completed)

### Tasks

**TASK 3.1 — RuntimeState enum**  
**TASK 3.2 — State manager**  
**TASK 3.3 — Hard limits**  
**TASK 3.4 — Context assembler**  
**TASK 3.5 — Decision function**  
**TASK 3.6 — Executor**  
**TASK 3.7 — Evaluator**  
**TASK 3.8 — Runtime loop**  
**TASK 3.9 — EventBus**

### Definition of Done

`run_turn("hello", "s1")` returns FinalResponse without infinite loop.

### Validation Steps

```bash
python -c "
from src.core.runtime.loop import run_turn
r = run_turn('hello', 'test')
print(f'Response: {r.text}')
print(f'State: COMPLETED')
"
```

### Artifacts

- `src/core/runtime/state.py`
- `src/core/runtime/state_manager.py`
- `src/core/context/assembler.py`
- `src/core/decision/decision.py`
- `src/core/runtime/executor.py`
- `src/core/runtime/evaluator.py`
- `src/core/runtime/loop.py`
- `src/core/events.py`

---

## Phase 4 — Decision System

```
phase_id: 4
title: "Decision System"
priority: "P1"
status: "not_started"
progress_percent: 0
done_tasks: 0
total_tasks: 5
blocker: "Phase 3 must complete"
next_action: "Start TASK 4.1"
last_updated: "-"
validation_status: "not_started"
```

### Objective

Harden decision system with robust classification.

### Dependencies

- Phase 3 (completed)

### Tasks

**TASK 4.1 — Classifier robust JSON parsing**  
**TASK 4.2 — Fast-path rules**  
**TASK 4.3 — Risk level population**  
**TASK 4.4 — Escalation chain**  
**TASK 4.5 — Decision tests**

### Artifacts

- `src/core/decision/classifier.py`
- `src/core/decision/decision.py`
- `src/core/runtime/escalation.py`
- `tests/test_decision.py`

---

## Phase 5 — Prompt Builder

```
phase_id: 5
title: "Prompt Builder"
priority: "P1"
status: "not_started"
progress_percent: 0
done_tasks: 0
total_tasks: 5
blocker: "Phase 4 must complete"
next_action: "Start TASK 5.1"
last_updated: "-"
validation_status: "not_started"
```

### Objective

Build identity and prompt assembly.

### Dependencies

- Phase 4 (completed)

### Tasks

**TASK 5.1 — Jarvis identity YAML**  
**TASK 5.2 — Mode fragments**  
**TASK 5.3 — System prompt builder**  
**TASK 5.4 — Wire into executor**  
**TASK 5.5 — Identity test**

### Artifacts

- `config/jarvis_identity.yaml`
- `src/core/identity/personality.py`
- `src/core/identity/builder.py`
- `src/core/runtime/executor.py`
- `tests/test_identity_enforcement.py`

---

## Phase 6 — Tool System

```
phase_id: 6
title: "Tool System"
priority: "P1"
status: "not_started"
progress_percent: 0
done_tasks: 0
total_tasks: 7
blocker: "Phase 5 must complete"
next_action: "Start TASK 6.1"
last_updated: "-"
validation_status: "not_started"
```

### Objective

Build complete tool execution pipeline.

### Dependencies

- Phase 5 (completed)

### Tasks

**TASK 6.1 — BaseTool abstract class**  
**TASK 6.2 — Tool registry**  
**TASK 6.3 — Safety classifier**  
**TASK 6.4 — Mode enforcement**  
**TASK 6.5 — Schema validator**  
**TASK 6.6 — Tool executor**  
**TASK 6.7 — Parse retry**

### Artifacts

- `src/core/tools/base.py`
- `src/core/tools/registry.py`
- `src/core/tools/safety.py`
- `src/core/tools/mode_enforcer.py`
- `src/core/tools/validator.py`
- `src/core/tools/executor.py`
- `src/core/runtime/llm_output.py`

---

## Phase 7 — Safety Modes

```
phase_id: 7
title: "Safety Modes"
priority: "P1"
status: "not_started"
progress_percent: 0
done_tasks: 0
total_tasks: 4
blocker: "Phase 6 must complete"
next_action: "Start TASK 7.1"
last_updated: "-"
validation_status: "not_started"
```

### Objective

Implement three-mode policy.

### Dependencies

- Phase 6 (completed)

### Tasks

**TASK 7.1 — Execution mode in config**  
**TASK 7.2 — Risk levels on all tools**  
**TASK 7.3 — CLI mode toggle**  
**TASK 7.4 — Safety tests**

### Artifacts

- `config/settings.yaml`
- `src/core/config.py`
- `src/interfaces/cli/commands.py`
- `tests/test_safety.py`

---

## Phase 8 — System Control Skills

```
phase_id: 8
title: "System Control Skills"
priority: "P1"
status: "not_started"
progress_percent: 0
done_tasks: 0
total_tasks: 8
blocker: "Phase 7 must complete"
next_action: "Start TASK 8.1"
last_updated: "-"
validation_status: "not_started"
```

### Objective

Implement system control tools.

### Dependencies

- Phase 7 (completed)

### Tasks

**TASK 8.1 — App launcher**  
**TASK 8.2 — System info**  
**TASK 8.3 — Clipboard**  
**TASK 8.4 — Notifications**  
**TASK 8.5 — Screenshot/OCR**  
**TASK 8.6 — File ops**  
**TASK 8.7 — Code executor**  
**TASK 8.8 — Web search**

### Artifacts

- `src/skills/system/apps.py`
- `src/skills/system/sysinfo.py`
- `src/skills/system/clipboard.py`
- `src/skills/notify/toasts.py`
- `src/skills/screen/capture.py`
- `src/skills/files/file_ops.py`
- `src/skills/coder/executor.py`
- `src/skills/search/web_search.py`

---

## Phase 9 — Runtime Hardening

```
phase_id: 9
title: "Runtime Hardening"
priority: "P0"
status: "not_started"
progress_percent: 0
done_tasks: 0
total_tasks: 6
blocker: "Phase 8 must complete"
next_action: "Start TASK 9.1"
last_updated: "-"
validation_status: "not_started"
```

### Objective

Add recovery systems and protection.

### Dependencies

- Phase 8 (completed)

### Tasks

**TASK 9.1 — LLM Output Recovery**
- [ ] Status: not_started
- Enhance parse in `src/core/runtime/llm_output.py`
- JSON extraction from messy text
- Auto-repair mechanism
- Fallback to text mode
- **Expected output:** Recovery from malformed JSON
- **Failure cases:** No recovery, crashes
- **Artifact:** `src/core/runtime/llm_output.py`

**TASK 9.2 — Tool Permission Layer**
- [ ] Status: not_started
- Create `src/core/tools/permission.py`
- Gate 1: Decision consistency
- Gate 2: Argument safety
- Gate 3: User context
- **Expected output:** Bad tools rejected
- **Failure cases:** Dangerous tool executes
- **Artifact:** `src/core/tools/permission.py`

**TASK 9.3 — Tool Chain Control**
- [ ] Status: not_started
- Detect tool loops
- Max depth = 3 enforcement
- Repeated tool detection
- **Expected output:** Infinite loop blocked
- **Failure cases:** Infinite tool loop
- **Artifact:** `src/core/tools/chain_control.py`

**TASK 9.4 — Timeout Handling**
- [ ] Status: not_started
- Add timeouts to config
- model_timeout_s = 120
- tool_timeout_s = 30
- total_turn_timeout_s = 300
- **Expected output:** Timeout exits cleanly
- **Failure cases:** Hangs forever

**TASK 9.5 — Graceful Degradation**
- [ ] Status: not_started
- Fallback on model failure
- Error responses that never crash runtime
- **Expected output:** Error response returned
- **Failure cases:** Exception reaches user

**TASK 9.6 — State Machine Tests**
- [ ] Status: not_started
- Create `tests/test_state_machine.py`
- Test all transitions
- Test limit enforcement
- **Expected output:** Tests pass

### Artifacts

- `src/core/runtime/llm_output.py`
- `src/core/tools/permission.py`
- `src/core/tools/chain_control.py`
- `tests/test_state_machine.py`

---

## Execution Gaps — Lock Phase

```
phase_id: gap
title: "Execution Gaps Lock"
priority: "P0"
status: "in_progress"
progress_percent: 0
done_tasks: 0
total_tasks: 12
blocker: "none"
next_action: "Start execution gap fixes"
last_updated: "2026-04-26"
validation_status: "not_started"
```

### Objective

Fix execution gaps to ensure stable, deterministic, fully controlled behavior.

### Tasks

**TASK VALIDATOR — Tool Validator**
- [ ] Status: not_started
- Create `src/core/tools/validator.py`
- Validate DecisionOutput alignment
- Validate schema validity
- Validate risk level
- Validate tool availability
- **Expected output:** Approved tool or rejection with reason
- **Artifact:** `src/core/tools/validator.py`

**TASK LOGGING — Logging System**
- [ ] Status: not_started
- Create `src/core/logging.py`
- Log decision results
- Log selected model
- Log tool calls
- Log failures
- Log retries
- Log escalations
- **Expected output:** All runtime events logged
- **Artifact:** `src/core/logging.py`

**TASK FAILURE_H — Failure Handling**
- [ ] Status: not_started
- Create `src/core/failure.py`
- Model timeout handling
- Invalid output handling
- Tool failure handling
- Loop detection with fallback
- **Expected output:** All failure modes handled
- **Artifact:** `src/core/failure.py`

**TASK IDENTITY — Identity Verification**
- [ ] Status: not_started
- Verify ALL model calls include identity block
- Verify prompt has Jarvis identity
- Verify mode enforcement
- **Expected output:** Every LLM call has identity
- **Artifact:** `src/core/identity/verify.py`

**TASK EXEC_LIMITS — Execution Limits**
- [ ] Status: not_started
- Add max_iterations enforcement
- Add max_tool_calls enforcement
- Add step timeout enforcement
- **Expected output:** Limits enforced at runtime
- **Artifact:** `src/core/runtime/limits.py`

**TASK DECISION_V — Decision Validation**
- [ ] Status: not_started
- Verify Decision output changes when inputs slightly vary
- Test with varying complexity, modality, cost constraints
- Verify multiple models can win based on input
- Verify scoring is explained in logs
- **Expected output:** Model choice varies with input characteristics
- **Artifact:** `tests/test_decision_dynamic.py`

**TASK DECISION_E — Decision Enforcement**
- [ ] Status: not_started
- Verify every DecisionOutput includes scoring metadata
- Verify candidate list exists
- Verify invalid decisions are rejected
- Verify decision.fail_safe triggers after 3 failures
- **Expected output:** No decision without scoring proof
- **Artifact:** `src/core/runtime/validate_decision.py`

**TASK FALLBACK — Tiered Fallback System**
- [ ] Status: not_started
- Implement Tier 1: qwen2.5:7b fallback
- Implement Tier 2: gemma3:4b fallback
- Verify Tier 1 attempted before Tier 2
- Verify fallback chain works
- **Expected output:** Strong fallback chain
- **Artifact:** `src/core/runtime/fallback.py`

**TASK RETRY — Decision Retry Logic**
- [ ] Status: not_started
- Implement max_decision_retries = 3
- Implement weight adjustment per retry
- Verify fallback triggered after retries
- **Expected output:** Controlled retries
- **Artifact:** `src/core/runtime/retry.py`

**TASK RESPONSE_Q — Response Quality Guard**
- [ ] Status: not_started
- Validate completeness
- Validate coherence
- Validate relevance
- Retry with stronger model on failure
- **Expected output:** Quality enforced
- **Artifact:** `src/core/runtime/response_guard.py`

**TASK DEGRADE — Degradation Flag**
- [ ] Status: not_started
- Track fallback activation
- Track retries exceeded
- Track weak model used
- Log system_state: degraded
- **Expected output:** Degradation visible and logged
- **Artifact:** `src/core/runtime/degradation.py`

### Definition of Done

1. No hardcoded routing
2. No direct tool execution
3. All actions validated
4. All steps logged
5. All failures handled
6. System deterministic

### Validation Steps

```bash
# Verify no hardcoded model routing in decision
# Verify all tool calls go through validator
# Verify logging outputs events
# Verify failure modes handle all cases
# Verify identity block in prompts
# Verify execution limits stop loops
```

---

## End of Execution Plan