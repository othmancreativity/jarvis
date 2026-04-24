# JARVIS — Execution Plan

## Execution Rules

**STRICT RULES - No exceptions, no phase skipping:**

1. **No skipping phases** — Phase 0 must be completed before Phase 1
2. **No adding features outside scope** — Each phase stays within its defined scope
3. **Each phase must produce a working system** — Must be runnable after each phase
4. **No breaking architecture** — Data contracts must be maintained across all phases
5. **Progressive implementation** — Build incrementally, never rewrite previous work
6. **Test after each task** — Verify success criteria before proceeding

---

## Priority System

| Priority | Description | Examples |
|----------|--------------|----------|
| **P0** | Core survival | State machine, limits, error handling |
| **P1** | Core features | Decision, tool execution, memory |
| **P2** | Expansion | Browser, Google APIs, Agents |
| **P3** | Advanced | Voice, Vision, GUI |

---

## Progress Tracking

| Phase | Name | Priority | Status |
|-------|------|----------|--------|
| 0 | First Working System | P0 | [ ] |
| 1 | Foundation | P0 | [ ] |
| 2 | Execution Contract | P0 | [ ] |
| 3 | Runtime State Machine | P0 | [ ] |
| 4 | Decision System | P1 | [ ] |
| 5 | Prompt Builder | P1 | [ ] |
| 6 | Tool System | P1 | [ ] |
| 7 | Safety Modes | P1 | [ ] |
| 8 | System Control Skills | P1 | [ ] |
| 9 | Runtime Hardening | P0 | [ ] |
| 10 | Memory (Simplified) | P1 | [ ] |
| 11 | Debug System | P0 | [ ] |
| 12 | Browser & Web | P2 | [ ] |
| 13 | Google APIs | P2 | [ ] |
| 14 | CLI Interface | P2 | [ ] |
| 15 | Web UI | P2 | [ ] |
| 16 | Voice Pipeline | P3 | [ ] |
| 17 | Vision + Image | P3 | [ ] |
| 18 | QA + Production | P0 | [ ] |

---

## Phase 0 — First Working System

> **MANDATORY FIRST - No other phase may be started until Phase 0 is complete and verified**

### Objective

Create a minimal working system that proves the core pipeline works: text input reaches the LLM and returns a response, and a tool command is classified, routed, and executed.

### Scope

- Text input → LLM call → response output
- Tool command classification → tool execution
- Arabic command support

### Out of Scope

- Full context assembly
- Memory systems
- Multiple execution modes

### Dependencies

None — this is the starting phase.

### Tasks

- [ ] TASK 0.1 — Connect to Ollama and get a response
  - Create `src/models/llm/engine.py`
  - Implement `chat(message, model)` function
  - Call Ollama Python client
  - Return response content as string
  - **Expected output:** Non-empty string response
  - **Failure:** Empty response, exception, timeout > 60s

- [ ] TASK 0.2 — Classify a command and return structured output
  - Create `src/core/decision/classifier.py`
  - Implement `classify(message)` function
  - Use gemma3:4b with JSON-forcing system prompt
  - Handle malformed JSON with retry (max 2)
  - Return safe fallback dict on all failures
  - **Expected output:** dict with intent, tool_name, tool_args
  - **Failure:** Invalid dict, wrong intent mapping, exception

- [ ] TASK 0.3 — Execute an application by name
  - Create `src/skills/system/apps.py`
  - Implement `open_app(name)` function
  - Cross-platform search (PATH, program directories)
  - Return success/error dict without raising
  - **Expected output:** {"success": true, "pid": N} or {"success": false, "error": "..."}
  - **Failure:** Exception reaches terminal, wrong app opened

- [ ] TASK 0.4 — Wire classifier to tool: text input → action
  - Create `app/jarvis_slice.py`
  - Implement `run(user_input)` function
  - Connect: input → classify → tool/LLM → output
  - Loop on terminal input until "quit"
  - **Expected output:** Tool executes or LLM response printed
  - **Failure:** Loop doesn't exit, no response

- [ ] TASK 0.5 — Verify Arabic input
  - Test Arabic commands produce same behavior as English
  - Add Arabic examples to classifier if needed
  - **Expected output:** Same intent as English equivalent
  - **Failure:** Different intent for Arabic

### Validation Steps

```bash
python -c "from src.models.llm.engine import chat; print(chat('hello'))"
python -c "from src.skills.system.apps import open_app; print(open_app('notepad'))"
python app/jarvis_slice.py
# Type: "open notepad" → opens Notepad
# Type: "what is AI?" → text response
# Type: "quit" → exits
```

### Failure Conditions

- Any exception reaches the terminal
- "open notepad" does not work
- Response is empty

### Artifacts

- `src/models/llm/engine.py`
- `src/core/decision/classifier.py`
- `src/skills/system/apps.py`
- `app/jarvis_slice.py`

---

## Phase 1 — Foundation

> **End state:** `python app/main.py --interface cli` runs, loads config, initializes logging, prints "Jarvis ready."

### Objective

Establish configuration system, logging infrastructure, and project structure.

### Scope

- Settings YAML and Pydantic loader
- Logging setup with Loguru
- Package skeleton with all directories
- Model profiles YAML
- Environment variables
- User profile storage
- Skills manifest YAML
- main.py entry point

### Dependencies

- Phase 0 (completed)

### Tasks

- [ ] TASK 1.1 — Settings YAML and Pydantic loader
  - Create `config/settings.yaml`
  - Create `src/core/config.py` with Pydantic models
  - Implement `get_settings()` cached singleton
  - Implement `create_directories()` function
  - **Expected output:** Settings object with all fields accessible
  - **Failure:** Missing fields cause crash

- [ ] TASK 1.2 — Logging setup
  - Create `src/core/logging_setup.py`
  - Configure Loguru with terminal and file sinks
  - 10 MB rotation, 7-day retention
  - Debug sink when debug=True
  - **Expected output:** Logs appear in terminal and file
  - **Failure:** No file logs created

- [ ] TASK 1.3 — Package skeleton
  - Create `__init__.py` in all src/ subdirectories
  - **Expected output:** All directories importable
  - **Failure:** ImportError

- [ ] TASK 1.4 — Model capability profiles
  - Create `config/models.yaml`
  - Create `src/models/profiles.py`
  - Implement `get_model_profile(tag)` function
  - **Expected output:** Dict with vram_gb, etc.
  - **Failure:** Returns empty dict for unknown

- [ ] TASK 1.5 — LLM engine with VRAM guard
  - Create `src/models/llm/engine.py` (enhanced)
  - Track active model
  - Implement `swap_to(model)`, `get_active_model()`
  - **Expected output:** Only one model active
  - **Failure:** Multiple models loaded

- [ ] TASK 1.6 — Environment variables
  - Create `.env.example`
  - Create `.env` (gitignored)
  - Call load_dotenv() in main.py
  - **Expected output:** Variables accessible via os.environ
  - **Failure:** .env in git

- [ ] TASK 1.7 — User profile
  - Create `src/core/memory/user_profile.py`
  - Implement `load_profile()`, `save_profile()`
  - **Expected output:** Profile persists across restarts
  - **Failure:** Profile lost on restart

- [ ] TASK 1.8 — Skills manifest
  - Create `config/skills.yaml`
  - Declare all tools with risk_level
  - **Expected output:** All tools declared
  - **Failure:** Missing tools at runtime

- [ ] TASK 1.9 — main.py entry point
  - Create `app/main.py`
  - Parse --interface and --debug flags
  - Execute boot flow steps 1-10
  - **Expected output:** "Jarvis ready" printed
  - **Failure:** Crash, no ready message

### Validation Steps

```bash
python app/main.py --interface cli
# Should see: jarvis starting → directories created → logging init → jarvis ready
# Ctrl+C should exit without traceback
```

### Failure Conditions

- Boot crashes
- No "Jarvis ready"

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

---

## Phase 2 — Execution Contract Implementation

> **End state:** All five contract types defined as Pydantic models.

### Objective

Define strict data contracts that bind all components together.

### Scope

- InputPacket Pydantic model
- DecisionOutput Pydantic model
- LLMOutput Pydantic model with parser
- ToolResult Pydantic model
- FinalResponse Pydantic model

### Dependencies

- Phase 1 (completed)

### Tasks

- [ ] TASK 2.1 — Define InputPacket
  - Create `src/core/context/bundle.py`
  - Define InputPacket with all fields
  - **Expected output:** Valid InputPacket instance
  - **Failure:** Missing fields, wrong types

- [ ] TASK 2.2 — Define DecisionOutput
  - Create `src/core/decision/decision.py`
  - Define DecisionOutput with constrained fields
  - **Expected output:** Valid DecisionOutput instance
  - **Failure:** Invalid enum values accepted

- [ ] TASK 2.3 — Define LLMOutput
  - Create `src/core/runtime/llm_output.py`
  - Define LLMOutput
  - Implement `parse_llm_output(raw, requires_tools)`
  - **Expected output:** Parsed LLMOutput
  - **Failure:** Invalid JSON not caught

- [ ] TASK 2.4 — Define ToolResult
  - Create `src/core/tools/result.py`
  - Define ToolResult
  - **Expected output:** Valid ToolResult instance
  - **Failure:** Missing fields

- [ ] TASK 2.5 — Define FinalResponse
  - Create `src/core/runtime/final_response.py`
  - Define FinalResponse
  - **Expected output:** Valid FinalResponse instance
  - **Failure:** Missing fields

- [ ] TASK 2.6 — Contract validation tests
  - Create `tests/test_contracts.py`
  - Test all models raise/accept correctly
  - **Expected output:** All tests pass
  - **Failure:** Tests fail

### Validation Steps

```bash
python -c "
from src.core.context.bundle import InputPacket
from src.core.decision.decision import DecisionOutput
from src.core.runtime.llm_output import LLMOutput
p = InputPacket(user_message='hello', session_id='s1')
d = DecisionOutput(intent='chat', complexity='low', mode='fast', model='gemma3:4b', requires_tools=False, requires_planning=False, confidence=0.9, risk_level='low')
print('Contracts valid')
"
```

### Failure Conditions

- Contract types fail to instantiate
- Invalid data not rejected

### Artifacts

- `src/core/context/bundle.py`
- `src/core/decision/decision.py`
- `src/core/runtime/llm_output.py`
- `src/core/tools/result.py`
- `src/core/runtime/final_response.py`
- `tests/test_contracts.py`

---

## Phase 3 — Runtime State Machine

> **End state:** Runtime operates as explicit state machine with bounded transitions.

### Objective

Implement the state machine that controls the runtime with hard limits.

### Scope

- State definition (IDLE, DECIDING, EXECUTING_MODEL, etc.)
- State transitions with validation
- State logging
- Hard limits (max_iterations=5, max_tool_depth=3)

### Dependencies

- Phase 2 (completed)

### Tasks

- [ ] TASK 3.1 — Define RuntimeState enum
  - Create `src/core/runtime/state.py`
  - Define RuntimeState enum with all states
  - States: IDLE, DECIDING, EXECUTING_MODEL, EXECUTING_TOOL, WAITING_CONFIRMATION, EVALUATING, ERROR, COMPLETED
  - **Expected output:** Enum with all states
  - **Failure:** Missing states

- [ ] TASK 3.2 — State manager class
  - Create `src/core/runtime/state_manager.py`
  - Implement RuntimeStateManager class
  - Track current state, iteration, tool_depth
  - Implement `transition_to(new_state)` with validation
  - **Expected output:** State transitions logged, invalid transitions rejected
  - **Failure:** Invalid transitions allowed

- [ ] TASK 3.3 — Hard limits enforcement
  - Add max_iterations=5 check
  - Add max_tool_depth=3 check
  - Add max_retries=2 check
  - Implement force_exit on limit exceeded
  - **Expected output:** Loop exits at limit
  - **Failure:** Infinite loop

- [ ] TASK 3.4 — Context assembler
  - Create `src/core/context/assembler.py`
  - Implement `assemble_context(user_message, session_id, attachments)`
  - **Expected output:** Valid InputPacket
  - **Failure:** Missing required fields

- [ ] TASK 3.5 — Decision function
  - Implement `decide(packet: InputPacket) → DecisionOutput`
  - **Expected output:** Valid DecisionOutput
  - **Failure:** Invalid decision

- [ ] TASK 3.6 — Executor (think step)
  - Create `src/core/runtime/executor.py`
  - Implement `execute_turn(decision, packet) → LLMOutput`
  - **Expected output:** Valid LLMOutput
  - **Failure:** No output

- [ ] TASK 3.7 — Evaluator
  - Create `src/core/runtime/evaluator.py`
  - Implement `evaluate(output, decision) → EvalResult`
  - **Expected output:** EvalResult with quality, should_retry
  - **Failure:** Always returns same value

- [ ] TASK 3.8 — Runtime loop
  - Create `src/core/runtime/loop.py`
  - Implement `run_turn(user_input, session_id, attachments)`
  - Integrate state machine
  - **Expected output:** FinalResponse returned
  - **Failure:** No output, infinite loop

- [ ] TASK 3.9 — EventBus
  - Create `src/core/events.py`
  - Implement publish-subscribe event system
  - **Expected output:** Events logged
  - **Failure:** Events not fired

### Validation Steps

```bash
python -c "
from src.core.runtime.loop import run_turn
from src.core.runtime.state import RuntimeState
r = run_turn('hello', 'test')
print(f'Response: {r.text[:50]}')
print(f'State: COMPLETED')
"
# Test limits
python -c "
from src.core.runtime.state_manager import RuntimeStateManager
rm = RuntimeStateManager()
# Force 5 iterations - should exit
"
```

### Failure Conditions

- State machine doesn't control flow
- Infinite loop possible
- No state logging

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

> **End state:** All intents classified correctly. Model selected per intent.

### Objective

Harden decision system with robust classification.

### Scope

- Robust classifier with JSON parsing
- Fast-path rules
- Risk level from manifest
- Escalation chain

### Dependencies

- Phase 3 (completed)

### Tasks

- [ ] TASK 4.1 — Classifier robust JSON parsing
  - Modify `src/core/decision/classifier.py`
  - Extract JSON from any position
  - Handle markdown code blocks
  - Retry with correction
  - Return fallback on failure
  - **Expected output:** Valid dict for any input
  - **Failure:** Random dict on bad input

- [ ] TASK 4.2 — Fast-path rules
  - Modify `src/core/decision/decision.py`
  - Image → vision intent (no LLM)
  - Short + no action → fast chat
  - **Expected output:** Fast return for fast inputs
  - **Failure:** LLM called unnecessarily

- [ ] TASK 4.3 — Risk level population
  - Modify `src/core/decision/decision.py`
  - Load skills.yaml
  - Populate risk_level from manifest
  - **Expected output:** risk_level always set
  - **Failure:** risk_level = None

- [ ] TASK 4.4 — Escalation chain
  - Create `src/core/runtime/escalation.py`
  - Define chain: fast → normal → deep
  - Implement `get_next_escalation()`
  - **Expected output:** Next mode/model
  - **Failure:** Wrong escalation

- [ ] TASK 4.5 — Decision tests
  - Create `tests/test_decision.py`
  - **Expected output:** Tests pass
  - **Failure:** Tests fail

### Validation Steps

```bash
python -c "
from src.core.decision.decision import decide
d = decide(assemble_context('open chrome', 's1'))
print(f'Intent: {d.intent}, Tool: {d.tool_name}')
"
```

### Failure Conditions

- Invalid classifier output
- Missing risk levels

### Artifacts

- `src/core/decision/classifier.py`
- `src/core/decision/decision.py`
- `src/core/runtime/escalation.py`
- `tests/test_decision.py`

---

## Phase 5 — Prompt Builder

> **End state:** Every LLM call receives assembled prompt.

### Objective

Build identity and prompt assembly.

### Scope

- Jarvis identity YAML
- Mode fragments
- System prompt builder

### Dependencies

- Phase 4 (completed)

### Tasks

- [ ] TASK 5.1 — Jarvis identity YAML
  - Create `config/jarvis_identity.yaml`
  - Add: name, role, component_notice, safety_rules
  - **Expected output:** Valid YAML
  - **Failure:** Missing fields

- [ ] TASK 5.2 — Mode fragments
  - Create `src/core/identity/personality.py`
  - Define MODE_FRAGMENTS
  - **Expected output:** All modes defined
  - **Failure:** Missing modes

- [ ] TASK 5.3 — System prompt builder
  - Create `src/core/identity/builder.py`
  - Implement build_system_prompt()
  - **Expected output:** Complete prompt
  - **Failure:** Missing blocks

- [ ] TASK 5.4 — Wire into executor
  - Modify `src/core/runtime/executor.py`
  - **Expected output:** Prompt sent to LLM
  - **Failure:** Empty prompt

- [ ] TASK 5.5 — Identity test
  - Create `tests/test_identity_enforcement.py`
  - **Expected output:** Tests pass
  - **Failure:** Identity not verified

### Validation Steps

```bash
python -c "
from src.core.identity.builder import build_system_prompt
p = build_system_prompt('hello', 'fast', [], None, 'gemma3:4b')
print('Jarvis' in p)
"
```

### Failure Conditions

- Identity not in prompt

### Artifacts

- `config/jarvis_identity.yaml`
- `src/core/identity/personality.py`
- `src/core/identity/builder.py`
- `src/core/runtime/executor.py`
- `tests/test_identity_enforcement.py`

---

## Phase 6 — Tool System

> **End state:** Tool pipeline: classify → registry → safety → validate → execute.

### Objective

Build complete tool execution pipeline.

### Scope

- BaseTool abstract class
- Tool registry
- Safety classifier
- Mode enforcement
- Schema validator
- Tool executor

### Dependencies

- Phase 5 (completed)

### Tasks

- [ ] TASK 6.1 — BaseTool abstract class
  - Create `src/core/tools/base.py`
  - Define BaseTool
  - **Expected output:** Tool class defined
  - **Failure:** Not importable

- [ ] TASK 6.2 — Tool registry
  - Create `src/core/tools/registry.py`
  - Implement discover()
  - **Expected output:** Tools registered
  - **Failure:** No tools found

- [ ] TASK 6.3 — Safety classifier
  - Create `src/core/tools/safety.py`
  - Implement classify_safety()
  - **Expected output:** Risk level returned
  - **Failure:** Always low

- [ ] TASK 6.4 — Mode enforcement
  - Create `src/core/tools/mode_enforcer.py`
  - Implement should_execute()
  - **Expected output:** Correct allow/confirm/block
  - **Failure:** Wrong behavior

- [ ] TASK 6.5 — Schema validator
  - Modify `src/core/tools/validator.py`
  - Implement validate_args()
  - **Expected output:** Validation errors caught
  - **Failure:** Invalid args pass

- [ ] TASK 6.6 — Tool executor
  - Create `src/core/tools/executor.py`
  - Implement execute_tool()
  - Full pipeline
  - **Expected output:** ToolResult returned
  - **Failure:** No result

- [ ] TASK 6.7 — Parse retry
  - Modify `src/core/runtime/llm_output.py`
  - Retry logic
  - **Expected output:** Recovery on bad JSON
  - **Failure:** No recovery

### Validation Steps

```bash
python -c "
from src.core.tools.registry import registry
registry.discover()
print(f'Tools: {len(registry.all_names())}')
"
python -c "
from src.core.tools.executor import execute_tool
r = execute_tool('open_app', {'name': 'notepad'})
print(f'Success: {r.success}')
"
```

### Failure Conditions

- Tool not found
- No safety check

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

> **End state:** Execution mode configurable. Policy applied.

### Objective

Implement three-mode policy.

### Scope

- Execution mode in config
- Risk levels on tools
- CLI mode toggle

### Dependencies

- Phase 6 (completed)

### Tasks

- [ ] TASK 7.1 — Execution mode in config
  - Modify config
  - **Expected output:** Mode configurable
  - **Failure:** Not saved

- [ ] TASK 7.2 — Risk levels on all tools
  - Modify `config/skills.yaml`
  - **Expected output:** All tools have risk_level
  - **Failure:** Missing levels

- [ ] TASK 7.3 — CLI mode toggle
  - Create `src/interfaces/cli/commands.py`
  - **Expected output:** /mode command works
  - **Failure:** No command

- [ ] TASK 7.4 — Safety tests
  - Create `tests/test_safety.py`
  - **Expected output:** Tests pass
  - **Failure:** Tests fail

### Validation Steps

```bash
python -c "
from src.core.config import get_settings
print(get_settings().runtime.execution_mode)
"
python -c "
from src.core.tools.mode_enforcer import should_execute
from src.core.tools.safety import SafetyResult
r = should_execute(SafetyResult(level='high', allowed=None), 'balanced')
print(f'Result: {r}')
"
```

### Failure Conditions

- Mode not changeable

### Artifacts

- `config/settings.yaml`
- `src/core/config.py`
- `src/interfaces/cli/commands.py`
- `tests/test_safety.py`

---

## Phase 8 — System Control Skills

> **End state:** OS-level operations work correctly.

### Objective

Implement system control tools.

### Scope

- App launcher, system info
- Clipboard, notifications
- Screenshot, file ops
- Code executor, web search

### Dependencies

- Phase 7 (completed)

### Tasks

- [ ] TASK 8.1 — App launcher
  - Modify `src/skills/system/apps.py`
  - **Expected output:** App opens
  - **Failure:** Wrong app

- [ ] TASK 8.2 — System info
  - Create `src/skills/system/sysinfo.py`
  - **Expected output:** CPU, RAM returned
  - **Failure:** Empty data

- [ ] TASK 8.3 — Clipboard
  - Create `src/skills/system/clipboard.py`
  - **Expected output:** Read/write works
  - **Failure:** No access

- [ ] TASK 8.4 — Notifications
  - Create `src/skills/notify/toasts.py`
  - **Expected output:** Notification shown
  - **Failure:** No notification

- [ ] TASK 8.5 — Screenshot/OCR
  - Create `src/skills/screen/capture.py`
  - **Expected output:** Screenshot and OCR work
  - **Failure:** No image

- [ ] TASK 8.6 — File ops
  - Create `src/skills/files/file_ops.py`
  - **Expected output:** File operations work
  - **Failure:** Wrong permissions

- [ ] TASK 8.7 — Code executor
  - Create `src/skills/coder/executor.py`
  - **Expected output:** Code executes
  - **Failure:** Dangerous code allowed

- [ ] TASK 8.8 — Web search
  - Create `src/skills/search/web_search.py`
  - **Expected output:** Search results
  - **Failure:** No results

### Validation Steps

```bash
python -c "
from src.core.tools.executor import execute_tool
r = execute_tool('open_app', {'name': 'notepad'})
print(f'Success: {r.success}')
r = execute_tool('system_info', {})
print(f'Data: {r.data}')
"
```

### Failure Conditions

- Tools don't work

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

> **End state:** Runtime is resilient to failures.

### Objective

Add recovery systems and protection.

### Scope

- LLM output recovery
- Tool permission layer
- Tool chain control
- Timeout handling
- Graceful degradation

### Dependencies

- Phase 8 (completed)

### Tasks

- [ ] TASK 9.1 — LLM Output Recovery
  - Enhance parse in `src/core/runtime/llm_output.py`
  - JSON extraction from messy text
  - Auto-repair
  - Fallback to text
  - **Expected output:** Recovery on bad JSON
  - **Failure:** No recovery

- [ ] TASK 9.2 — Tool Permission Layer
  - Create `src/core/tools/permission.py`
  - Gate 1: Decision consistency
  - Gate 2: Argument safety (dangerous patterns)
  - Gate 3: User context
  - **Expected output:** Bad tools rejected
  - **Failure:** Dangerous tool runs

- [ ] TASK 9.3 — Tool Chain Control
  - Detect tool loops
  - Max depth = 3
  - Repeated tool detection
  - **Expected output:** Loop detected and blocked
  - **Failure:** Infinite tool loop

- [ ] TASK 9.4 — Timeout Handling
  - Add timeouts to config
  - model_timeout_s = 120
  - tool_timeout_s = 30
  - total_turn_timeout_s = 300
  - **Expected output:** Timeout exits cleanly
  - **Failure:** Hangs forever

- [ ] TASK 9.5 — Graceful Degradation
  - Fallback on model failure
  - Error responses
  - Never crash runtime
  - **Expected output:** Error response returned
  - **Failure:** Exception reaches user

- [ ] TASK 9.6 — State Machine Tests
  - Create `tests/test_state_machine.py`
  - Test all transitions
  - Test limit enforcement
  - **Expected output:** Tests pass
  - **Failure:** Tests fail

### Validation Steps

```bash
# Test bad JSON recovery
python -c "
from src.core.runtime.llm_output import parse_llm_output
r = parse_llm_output('Here is JSON: {"type":"tool_call","tool":"test","args":{}}}', True)
print(f'Parsed: {r.type}')
"
# Test tool loop detection
python -c "
from src.core.tools.permission import detect_tool_loop
result = detect_tool_loop(['test'] * 5)
print(f'Blocked: {result}')
"
# Test timeout
python -c "
from src.core.config import get_settings
print(get_settings().runtime.model_timeout_s)
"
```

### Failure Conditions

- Bad JSON crashes
- Dangerous tools run
- Infinite loops

### Artifacts

- `src/core/runtime/llm_output.py`
- `src/core/tools/permission.py`
- `src/core/tools/chain_control.py`
- `tests/test_state_machine.py`

---

## Phase 10 — Memory (Simplified)

> **End state:** Clear memory roles implemented.

### Objective

Simplify memory to avoid overcomplexity.

### Scope

- Simple SQLite only
- No Redis, no ChromaDB
- Session history in SQLite

### Dependencies

- Phase 3 (completed)

### Tasks

- [ ] TASK 10.1 — SQLite Database
  - Create `src/core/memory/database.py`
  - Schema: facts, conversation_history
  - **Expected output:** Tables created
  - **Failure:** No tables

- [ ] TASK 10.2 — Memory functions
  - Implement save_message, get_history
  - Implement remember, recall (simple)
  - **Expected output:** Data persists
  - **Failure:** Data lost

- [ ] TASK 10.3 — Auto-save
  - Modify `src/core/runtime/loop.py`
  - Save after turn
  - **Expected output:** Conversations saved
  - **Failure:** Not saved

### Validation Steps

```bash
python -c "
from src.core.m.database import save_message, get_history
save_message('test', 'user', 'hello')
h = get_history('test')
print(f'History: {len(h)}')
"
```

### Failure Conditions

- Memory not working

### Artifacts

- `src/core/memory/database.py`
- `src/core/runtime/loop.py`

---

## Phase 11 — Debug System

> **End state:** Fully debuggable runtime.

### Objective

Add debug capabilities.

### Scope

- Debug modes (OFF, BASIC, TRACE, RAW)
- Trace system
- Replay capability

### Dependencies

- Phase 9 (completed)

### Tasks

- [ ] TASK 11.1 — Debug Mode
  - Create `src/core/debug.py`
  - Define debug levels
  - Implement is_debug(), is_trace()
  - **Expected output:** Debug detection works
  - **Failure:** Always off

- [ ] TASK 11.2 — Debug Output
  - Add debug logging
  - Show decisions, states, tool calls
  - Show raw LLM when is_raw()
  - **Expected output:** Debug output when enabled
  - **Failure:** No output

- [ ] TASK 11.3 — Trace System
  - Create TurnTrace class
  - Store full execution
  - **Expected output:** Can replay
  - **Failure:** Not stored

- [ ] TASK 11.4 — Replay Command
  - Add /replay CLI command
  - Show turn trace
  - **Expected output:** Replay works
  - **Failure:** No command

### Validation Steps

```bash
python app/main.py --interface cli --debug
# Enable debug mode
# Should see state transitions
python app/main.py --interface cli --trace
# Should see full trace
```

### Failure Conditions

- Debug doesn't show

### Artifacts

- `src/core/debug.py`
- `src/interfaces/cli/commands.py`

---

## Phase 12 — Browser & Web Skills

> **End state:** Playwright browser works.

### Objective

Implement browser automation.

### Scope

- Playwright core
- Session persistence
- File transfer

### Dependencies

- Phase 11 (completed)

### Tasks

- [ ] TASK 12.1 — Playwright core
  - Create `src/skills/browser/browser.py`
  - **Expected output:** Browser works
  - **Failure:** Broken

- [ ] TASK 12.2 — Session
  - Create `src/skills/browser/session.py`
  - **Expected output:** Session saved
  - **Failure:** Not saved

- [ ] TASK 12.3 — File transfer
  - Create `src/skills/browser/transfer.py`
  - **Expected output:** File transfer works
  - **Failure:** Cannot transfer

### Validation Steps

```bash
python -c "
from src.core.tools.executor import execute_tool
r = execute_tool('browser_navigate', {'url': 'https://example.com'})
print(f'Success: {r.success}')
"
```

### Failure Conditions

- Browser not working

### Artifacts

- `src/skills/browser/browser.py`
- `src/skills/browser/session.py`
- `src/skills/browser/transfer.py`

---

## Phase 13 — Google APIs

> **End state:** OAuth + Calendar, Gmail, Drive.

### Objective

Implement Google integrations.

### Scope

- OAuth
- Calendar, Gmail, Drive

### Dependencies

- Phase 12 (completed)

### Tasks

- [ ] TASK 13.1 — OAuth
  - Create `src/skills/api/google_auth.py`
  - **Expected output:** OAuth flow works
  - **Failure:** Cannot authenticate

- [ ] TASK 13.2 — Calendar
  - Create `src/skills/api/calendar.py`
  - **Expected output:** CRUD works
  - **Failure:** Cannot connect

- [ ] TASK 13.3 — Gmail
  - Create `src/skills/api/gmail.py`
  - **Expected output:** Send works
  - **Failure:** Cannot send

- [ ] TASK 13.4 — Drive
  - Create `src/skills/api/drive.py`
  - **Expected output:** Upload works
  - **Failure:** Cannot upload

### Validation Steps

```bash
python -c "
from src.core.tools.executor import execute_tool
r = execute_tool('calendar_list', {})
print(f'Result: {r.success}')
"
```

### Failure Conditions

- API not working

### Artifacts

- `src/skills/api/google_auth.py`
- `src/skills/api/calendar.py`
- `src/skills/api/gmail.py`
- `src/skills/api/drive.py`

---

## Phase 14 — CLI Interface

> **End state:** Rich terminal interface.

### Objective

Build CLI.

### Scope

- Rich chat loop
- Slash commands

### Dependencies

- Phase 11 (completed)

### Tasks

- [ ] TASK 14.1 — Rich chat loop
  - Create `src/interfaces/cli/interface.py`
  - **Expected output:** Works
  - **Failure:** Not working

- [ ] TASK 14.2 — Commands
  - Create `src/interfaces/cli/commands.py`
  - **Expected output:** Commands work
  - **Failure:** No commands

### Validation Steps

```bash
python app/main.py --interface cli
# Test commands
```

### Failure Conditions

- CLI crashes

### Artifacts

- `src/interfaces/cli/interface.py`
- `src/interfaces/cli/commands.py`

---

## Phase 15 — Web UI

> **End state:** Browser interface.

### Objective

Build Web UI.

### Scope

- FastAPI
- WebSocket
- HTML/CSS/JS

### Dependencies

- Phase 14 (completed)

### Tasks

- [ ] TASK 15.1 — FastAPI app
  - Create `src/interfaces/web/app.py`
  - **Expected output:** App runs
  - **Failure:** Not running

- [ ] TASK 15.2 — WebSocket
  - Create `src/interfaces/web/ws.py`
  - **Expected output:** Streaming works
  - **Failure:** No streaming

- [ ] TASK 15.3 — Frontend
  - Create HTML, CSS, JS
  - **Expected output:** Works in browser
  - **Failure:** Broken

### Validation Steps

```bash
python app/server.py
# Open browser, test
```

### Failure Conditions

- Not loading

### Artifacts

- `src/interfaces/web/app.py`
- `src/interfaces/web/ws.py`
- `src/interfaces/web/templates/`
- `src/interfaces/web/static/`

---

## Phase 16 — Voice Pipeline

> **End state:** Wake word → speech → response → TTS.

### Objective

Add voice.

### Dependencies

- Phase 15 (completed)

### Tasks

- [ ] TASK 16.1 — STT
  - Create `src/models/speech/stt.py`
  - **Expected output:** Transcription works

- [ ] TASK 16.2 — TTS
  - Create `src/models/speech/tts.py`
  - **Expected output:** Speech works

- [ ] TASK 16.3 — Wake word
  - Create `src/interfaces/voice/wake_word.py`
  - **Expected output:** Detects wake word

- [ ] TASK 16.4 — Pipeline
  - Create `src/interfaces/voice/pipeline.py`
  - **Expected output:** Full pipeline works

### Failure Conditions

- Not working

### Artifacts

- `src/models/speech/stt.py`
- `src/models/speech/tts.py`
- `src/interfaces/voice/wake_word.py`
- `src/interfaces/voice/pipeline.py`

---

## Phase 17 — Vision + Image Generation

> **End state:** Image understanding and generation.

### Objective

Add vision.

### Dependencies

- Phase 16 (completed)

### Tasks

- [ ] TASK 17.1 — LLaVA
  - Create `src/models/vision/llava.py`
  - **Expected output:** Image described

- [ ] TASK 17.2 — Stable Diffusion
  - Create `src/models/diffusion/sd.py`
  - **Expected output:** Image generated

### Failure Conditions

- Not working

### Artifacts

- `src/models/vision/llava.py`
- `src/models/diffusion/sd.py`

---

## Phase 18 — QA + Production

> **End state:** Test suite passes. Production-ready.

### Objective

Finalize for production.

### Dependencies

- Phase 17 (completed)

### Tasks

- [ ] TASK 18.1 — Test suite
  - Create `tests/test_integration.py`
  - **Expected output:** All tests pass
  - **Failure:** Tests fail

- [ ] TASK 18.2 — Security audit
  - Verify dangerous patterns blocked
  - Verify confirmation works
  - **Expected output:** Clean audit
  - **Failure:** Issues found

- [ ] TASK 18.3 — Error handling
  - All errors logged
  - No exceptions to user
  - **Expected output:** Clean errors
  - **Failure:** Crashes

- [ ] TASK 18.4 — Integration test
  - Run full system
  - **Expected output:** Works end-to-end
  - **Failure:** Breaks

- [ ] TASK 18.5 — Production ready
  - Verify all phases
  - Create VERSION
  - **Expected output:** Ready
  - **Failure:** Not ready

### Validation Steps

```bash
pytest tests/ -v
# All tests pass
```

### Failure Conditions

- Test failures

### Artifacts

- `tests/test_integration.py`
- `VERSION`

---

## End of Execution Plan