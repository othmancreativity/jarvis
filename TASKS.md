# JARVIS — Execution Engine (Expanded)

## Project Status

```yaml
project:
  name: JARVIS
  version: "1.0"
  spec_version: "final"
  last_updated: "2026-04-28"
  current_phase: 1
  overall_progress_percent: 0
  risk_level: "medium"
  hardware_profile:
    gpu: "RTX 3050 6GB VRAM"
    ram: "16 GB"
    cpu: "Intel Core i5 12th Gen"
  current_blocker: "none"
  next_action: "Start Phase 1"
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
| 0 | First Working System | P0 | [x] | 100% | 5/5 | none | Phase 0 complete | 2026-04-26 |
| 1 | Foundation | P0 | [ ] | 0% | 0/9 | none | Start TASK 1.1 | - |
| 2 | Execution Contract | P0 | [ ] | 0% | 0/6 | none | Start TASK 2.1 | - |
| 3 | Runtime State Machine | P0 | [ ] | 0% | 0/9 | none | Start TASK 3.1 | - |
| 4 | Decision System | P1 | [ ] | 0% | 0/5 | none | Start TASK 4.1 | - |
| 5 | Prompt Builder | P1 | [ ] | 0% | 0/5 | none | Start TASK 5.1 | - |
| 6 | Capability System | P1 | [ ] | 0% | 0/7 | none | Start TASK 6.1 | - |
| 7 | Safety Modes | P1 | [ ] | 0% | 0/4 | none | Start TASK 7.1 | - |
| 8 | System Control Capabilities | P1 | [ ] | 0% | 0/8 | none | Start TASK 8.1 | - |
| 9 | Runtime Hardening | P0 | [ ] | 0% | 0/6 | none | Start TASK 9.1 | - |
| 10 | Memory (Simplified) | P1 | [ ] | 0% | 0/3 | none | Start TASK 10.1 | - |
| 11 | Debug System | P0 | [ ] | 0% | 0/4 | none | Start TASK 11.1 | - |
| 12 | Web Automation & Browser | P2 | [ ] | 0% | 0/3 | none | Start TASK 12.1 | - |
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
status: "completed"
progress_percent: 100
done_tasks: 5
total_tasks: 5
blocker: "none"
next_action: "Start Phase 1"
last_updated: "2026-04-26"
validation_status: "not_started"
```

### Objective

Create a minimal working system that proves the core pipeline works: text input reaches the LLM and returns a response, and a capability command is classified, routed, and executed.

### Tasks

**TASK 0.1 — Connect to Ollama and get a response**

Location:
- `src/models/llm/engine.py`

Purpose:
- Establish LLM communication layer for local Ollama instance

Steps:
1. Create `src/models/llm/` directory
2. Create `src/models/llm/engine.py` file
3. Define `OllamaEngine` class with `chat(message, model)` method
4. Implement Ollama Python client connection
5. Handle connection errors with try/except
6. Return response content as string
7. Set default timeout to 60 seconds

Input:
- `message`: string (user input)
- `model`: string (model tag, default: gemma3:4b)

Output:
- `response`: string (non-empty LLM response)

Dependencies:
- Phase 0 (none - starting phase)

Validation:
```bash
python -c "from src.models.llm.engine import chat; print(chat('hello'))"
```
- Expected: Non-empty string response within 60s
- Failure: Empty response, exception reaches terminal, timeout > 60s

Artifact: `src/models/llm/engine.py`

---

**TASK 0.2 — Classify a command and return structured output**

Location:
- `src/core/decision/classifier.py`

Purpose:
- Implement intent classification using LLM to determine user intent and extract tool calls

Steps:
1. Create `src/core/decision/` directory
2. Create `src/core/decision/classifier.py` file
3. Define `Classifier` class with `classify(message)` method
4. Use gemma3:4b with JSON-forcing system prompt
5. Implement JSON parsing with error handling
6. Add retry logic (max 2 attempts)
7. Return dict with keys: intent, tool_name, tool_args
8. Implement safe fallback dict on all failures

Input:
- `message`: string (user command)

Output:
- `dict`: {intent: str, tool_name: str|null, tool_args: dict}

Dependencies:
- TASK 0.1 (Ollama connection)

Validation:
```bash
python -c "from src.core.decision.classifier import classify; print(classify('open chrome'))"
```
- Expected: dict with intent, tool_name, tool_args
- Failure: Invalid dict, wrong intent mapping, exception

Artifact: `src/core/decision/classifier.py`

---

**TASK 0.3 — Execute an application by name**

Location:
- `src/capabilities/system/apps.py`

Purpose:
- Implement system capability to launch applications by name across platforms

Steps:
1. Create `src/capabilities/system/` directory
2. Create `src/capabilities/system/apps.py` file
3. Define `AppLauncher` class with `open_app(name)` method
4. Implement Windows search (PATH, Program Files, Start Menu)
5. Implement Linux search (PATH, /usr/share/applications)
6. Implement macOS search (PATH, /Applications)
7. Return success/error dict without raising exceptions
8. Include PID in success response

Input:
- `name`: string (application name)

Output:
- `dict`: {success: bool, pid: int|null, error: str|null}

Dependencies:
- None (can run independently)

Validation:
```bash
python -c "from src.capabilities.system.apps import open_app; print(open_app('notepad'))"
```
- Expected: `{"success": true, "pid": N}` or `{"success": false, "error": "..."}`
- Failure: Exception reaches terminal, wrong app opened

Artifact: `src/capabilities/system/apps.py`

---

**TASK 0.4 — Wire classifier to capability: text input → action**

Location:
- `app/jarvis_slice.py`

Purpose:
- Connect all Phase 0 components into a working CLI loop

Steps:
1. Create `app/` directory
2. Create `app/jarvis_slice.py` file
3. Implement `run(user_input)` function
4. Wire: input → classify → route to tool or LLM → output
5. Implement terminal input loop
6. Add "quit" command to exit cleanly
7. Print tool execution results or LLM response

Input:
- Terminal text input from user

Output:
- Tool execution result or LLM response printed to terminal

Dependencies:
- TASK 0.1 (Ollama connection)
- TASK 0.2 (Classifier)
- TASK 0.3 (App launcher)

Validation:
```bash
python app/jarvis_slice.py
# Type: "open notepad" → should open Notepad
# Type: "what is AI?" → response
# Type: "quit" → exit
```
- Expected: Tool executes or response printed
- Failure: Loop doesn't exit on "quit", no response

Artifact: `app/jarvis_slice.py`

---

**TASK 0.5 — Verify Arabic input**

Location:
- Test task (no file creation)

Purpose:
- Ensure Arabic language commands produce identical behavior to English

Steps:
1. Test Arabic command: "افتح المفكرة" (open notepad)
2. Verify same intent classification as "open notepad"
3. Test Arabic question: "ما هو الذكاء الاصطناعي؟"
4. Verify same response behavior as "what is AI?"

Input:
- Arabic text commands

Output:
- Same intents/responses as English equivalents

Dependencies:
- TASK 0.2 (Classifier)
- TASK 0.3 (App launcher)

Validation:
- Arabic "افتح المفكرة" → intent=tool_use, tool_name=open_app
- Arabic "ما هو الذكاء الاصطناعي؟" → intent=chat
- Failure: Different intent for Arabic vs English

---

### Definition of Done

1. "hello" returns non-empty text response.
2. "open notepad" opens Notepad.
3. Arabic equivalents produce identical behavior.
4. "quit" exits cleanly.

### Artifacts

- `src/models/llm/engine.py`
- `src/core/decision/classifier.py`
- `src/capabilities/system/apps.py`
- `app/jarvis_slice.py`

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

### Tasks

**TASK 1.1 — Settings YAML and Pydantic loader**

Location:
- `config/settings.yaml`
- `src/core/config.py`

Purpose:
- Create configuration system with YAML settings and Pydantic validation

Steps:
1. Create `config/` directory
2. Create `config/settings.example.yaml` with all default settings
3. Define settings structure: models, paths, execution modes, safety
4. Create `src/core/config.py`
5. Define Pydantic `Settings` model matching YAML structure
6. Implement `load_config(path)` function
7. Add environment variable override support
8. Validate required fields on load

Input:
- YAML file path

Output:
- Validated `Settings` object

Dependencies:
- Phase 0 complete

Validation:
```bash
python -c "from src.core.config import load_config; s = load_config('config/settings.yaml'); print(s.models.default)"
```

Artifact: `src/core/config.py`, `config/settings.yaml`

---

**TASK 1.2 — Logging setup**

Location:
- `src/core/logging_setup.py`

Purpose:
- Implement structured logging with Loguru matching README spec

Steps:
1. Create `src/core/logging_setup.py`
2. Define `setup_logging(level, format)` function
3. Configure Loguru with structured output
4. Include required fields: timestamp, level, event, session_id, turn_id, phase, data
5. Add file and console sinks
6. Implement log rotation

Input:
- Log level, format string

Output:
- Configured logger instance

Dependencies:
- TASK 1.1 (config system)

Validation:
```bash
python -c "from src.core.logging_setup import setup_logging; setup_logging('INFO')"
# Verify log output contains all required fields
```

Artifact: `src/core/logging_setup.py`

---

**TASK 1.3 — Package skeleton**

Location:
- `src/__init__.py`
- `src/core/__init__.py`
- `src/capabilities/__init__.py`
- `src/interfaces/__init__.py`
- `src/services/__init__.py`
- `src/models/__init__.py`
- `src/memory/__init__.py`

Purpose:
- Create proper Python package structure matching STRUCTURE.md

Steps:
1. Create all `__init__.py` files in each package
2. Define proper imports for public API
3. Add version info to `src/__init__.py`
4. Ensure all packages are importable

Input:
- None (initialization task)

Output:
- Valid Python package structure

Dependencies:
- None

Validation:
```bash
python -c "import src; import src.core; import src.capabilities; import src.interfaces; import src.services; import src.models; import src.memory; print('All packages importable')"
```

---

**TASK 1.4 — Model capability profiles**

Location:
- `src/models/profiles.py`

Purpose:
- Define model capability profiles for dynamic model selection

Steps:
1. Create `src/models/profiles.py`
2. Define `ModelProfile` dataclass: name, vram_required, capabilities, latency_tier, reasoning_tier
3. Create profile for each model: gemma3:4b, qwen3:8b, qwen2.5-coder:7b, llava:7b
4. Implement `get_profile(model_name)` lookup function
5. Add VRAM budget validation per profile

Input:
- Model name string

Output:
- `ModelProfile` object with capabilities

Dependencies:
- TASK 1.1 (config for model list)

Validation:
```bash
python -c "from src.models.profiles import get_profile; p = get_profile('gemma3:4b'); print(p.vram_required)"
```

Artifact: `src/models/profiles.py`

---

**TASK 1.5 — LLM engine with VRAM guard**

Location:
- `src/models/llm/engine.py` (expand TASK 0.1)

Purpose:
- Enhance LLM engine with VRAM monitoring and model lifecycle management

Steps:
1. Expand `src/models/llm/engine.py`
2. Add `unload_model()` method
3. Implement VRAM check before model load
4. Add `swap_model(from, to)` with unload/load sequence
5. Implement concurrent call prevention (only one model call at a time)
6. Add timeout handling (model_timeout_s from config)
7. Track current loaded model state

Input:
- Model name, message

Output:
- LLM response or timeout error

Dependencies:
- TASK 0.1 (base engine)
- TASK 1.4 (model profiles)

Validation:
```bash
python -c "from src.models.llm.engine import OllamaEngine; e = OllamaEngine(); e.swap_model('gemma3:4b', 'qwen3:8b')"
```

Artifact: `src/models/llm/engine.py`

---

**TASK 1.6 — Environment variables**

Location:
- `.env.example`
- `.env`

Purpose:
- Set up environment variable configuration for secrets

Steps:
1. Create `.env.example` with all required variables
2. Variables: TELEGRAM_BOT_TOKEN, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, etc.
3. Document each variable's purpose
4. Add python-dotenv loading in config system
5. Create `.env` from example (gitignored)

Input:
- None

Output:
- `.env` file with secrets

Dependencies:
- TASK 1.1 (config system)

Validation:
```bash
python -c "from dotenv import load_dotenv; load_dotenv(); print('Env loaded')"
```

---

**TASK 1.7 — User profile**

Location:
- `src/memory/user_profile.py`

Purpose:
- Implement user profile storage for personalization

Steps:
1. Create `src/memory/` directory
2. Create `src/memory/user_profile.py`
3. Define `UserProfile` dataclass: user_id, name, language, preferences, execution_mode
4. Implement `load_profile(user_id)` function
5. Implement `save_profile(profile)` function
6. Add default profile creation

Input:
- user_id string

Output:
- `UserProfile` object

Dependencies:
- TASK 1.1 (config for storage path)

Validation:
```bash
python -c "from src.memory.user_profile import load_profile; p = load_profile('default'); print(p.language)"
```

Artifact: `src/memory/user_profile.py`

---

**TASK 1.8 — Capabilities manifest**

Location:
- `config/capabilities.yaml`

Purpose:
- Define all system capabilities with metadata for registry

Steps:
1. Create `config/capabilities.yaml`
2. Define each capability: name, domain, risk_level, description, module_path
3. Include: system, files, web_automation, screen, vision, voice, notify, search
4. Add input/output schema references
5. Define cross-platform support per capability

Input:
- None (manifest definition)

Output:
- YAML manifest file

Dependencies:
- None

Validation:
```bash
python -c "import yaml; m = yaml.safe_load(open('config/capabilities.yaml')); print(len(m['capabilities']))"
```

Artifact: `config/capabilities.yaml`

---

**TASK 1.9 — main.py entry point**

Location:
- `app/main.py`

Purpose:
- Create main application entry point with CLI argument parsing

Steps:
1. Create `app/main.py`
2. Implement `main()` function
3. Add argparse for: --interface (cli/web), --debug, --trace, --mode
4. Add boot sequence: config → logging → validate → start interface
5. Implement Ctrl+C graceful exit
6. Print "Jarvis ready" on successful start

Input:
- CLI arguments

Output:
- Running Jarvis instance

Dependencies:
- TASK 1.1 (config)
- TASK 1.2 (logging)
- TASK 1.3 (packages)

Validation:
```bash
python app/main.py --interface cli
# Should see: jarvis starting → directories created → logging init → jarvis ready
# Ctrl+C should exit without traceback
```

Artifact: `app/main.py`

---

### Definition of Done

`python app/main.py --interface cli` runs all boot steps and prints "Jarvis ready".

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

### Tasks

**TASK 2.1 — Define InputPacket**

Location:
- `src/core/context/bundle.py`

Purpose:
- Create InputPacket dataclass matching README spec exactly

Steps:
1. Create `src/core/context/` directory
2. Create `src/core/context/bundle.py`
3. Define `InputPacket` dataclass with all required fields:
   - user_message: str (required)
   - session_id: str (required)
   - attachments: list[Attachment] (default: [])
   - memory_snippets: list[str] (default: [])
   - recent_history: list[Message] (default: [])
   - user_profile: UserProfile (required)
   - tool_results: list[ToolResult] (default: [])
   - turn_number: int (default: 0)
4. Add validation on instantiation
5. Add `to_dict()` and `from_dict()` methods

Input:
- Keyword arguments matching fields

Output:
- Validated InputPacket object

Dependencies:
- TASK 1.7 (UserProfile)

Validation:
```bash
python -c "from src.core.context.bundle import InputPacket; p = InputPacket(user_message='hello', session_id='s1'); print(p.user_message)"
```

Artifact: `src/core/context/bundle.py`

---

**TASK 2.2 — Define DecisionOutput**

Location:
- `src/core/decision/decision.py`

Purpose:
- Create DecisionOutput dataclass matching README spec exactly

Steps:
1. Create `src/core/decision/decision.py` (expand from TASK 0.2)
2. Define `DecisionOutput` dataclass:
   - intent: enum(chat|code|tool_use|search|vision|research|voice)
   - complexity: enum(low|medium|high)
   - mode: enum(fast|normal|deep|planning|research)
   - model: str (model tag)
   - requires_tools: bool
   - requires_planning: bool (default: false)
   - tool_name: str|null (default: null)
   - tool_args: dict (default: {})
   - confidence: float (0.0-1.0)
   - risk_level: enum(low|medium|high)
   - score_breakdown: dict (required for validation)
   - candidate_list: list (required for validation)
3. Add validation: intent must be valid, tool_name null if requires_tools=false
4. Add scoring metadata fields

Input:
- Keyword arguments matching fields

Output:
- Validated DecisionOutput object

Dependencies:
- TASK 2.1 (InputPacket for context)

Validation:
```bash
python -c "from src.core.decision.decision import DecisionOutput; d = DecisionOutput(intent='chat', complexity='low', mode='fast', model='gemma3:4b', requires_tools=False, requires_planning=False, confidence=0.9, risk_level='low', score_breakdown={}, candidate_list=[]); print(d.intent)"
```

Artifact: `src/core/decision/decision.py`

---

**TASK 2.3 — Define LLMOutput**

Location:
- `src/core/runtime/llm_output.py`

Purpose:
- Create LLMOutput dataclass matching README spec exactly

Steps:
1. Create `src/core/runtime/` directory
2. Create `src/core/runtime/llm_output.py`
3. Define `LLMOutput` dataclass:
   - type: enum(answer|tool_call)
   - content: str (required if type=answer)
   - tool: str|null (required if type=tool_call)
   - args: dict (default: {})
4. Add validation: enforce type-content/tool consistency
5. Add `requires_tools` enforcement logic

Input:
- Keyword arguments matching fields

Output:
- Validated LLMOutput object

Dependencies:
- None (standalone contract)

Validation:
```bash
python -c "from src.core.runtime.llm_output import LLMOutput; o = LLMOutput(type='answer', content='hello'); print(o.type)"
```

Artifact: `src/core/runtime/llm_output.py`

---

**TASK 2.4 — Define ToolResult**

Location:
- `src/capabilities/result.py`

Purpose:
- Create ToolResult dataclass matching README spec exactly

Steps:
1. Create `src/capabilities/result.py`
2. Define `ToolResult` dataclass:
   - tool: str (required)
   - success: bool (required)
   - data: dict (default: {})
   - error: str (default: '')
   - duration_ms: float (default: 0.0)
3. Add validation on required fields

Input:
- Keyword arguments matching fields

Output:
- Validated ToolResult object

Dependencies:
- None (standalone contract)

Validation:
```bash
python -c "from src.capabilities.result import ToolResult; r = ToolResult(tool='open_app', success=True); print(r.success)"
```

Artifact: `src/capabilities/result.py`

---

**TASK 2.5 — Define FinalResponse**

Location:
- `src/core/runtime/final_response.py`

Purpose:
- Create FinalResponse dataclass matching README spec exactly

Steps:
1. Create `src/core/runtime/final_response.py`
2. Define `FinalResponse` dataclass:
   - text: str (required)
   - session_id: str (required)
   - model: str (required)
   - mode: str (required)
   - quality: float (0.0-1.0) (required)
3. Add validation on required fields

Input:
- Keyword arguments matching fields

Output:
- Validated FinalResponse object

Dependencies:
- None (standalone contract)

Validation:
```bash
python -c "from src.core.runtime.final_response import FinalResponse; r = FinalResponse(text='hi', session_id='s1', model='gemma3:4b', mode='fast', quality=0.9); print(r.text)"
```

Artifact: `src/core/runtime/final_response.py`

---

**TASK 2.6 — Contract tests**

Location:
- `tests/test_contracts.py`

Purpose:
- Verify all contracts instantiate correctly and reject invalid data

Steps:
1. Create `tests/` directory
2. Create `tests/test_contracts.py`
3. Write test: InputPacket valid instantiation
4. Write test: InputPacket reject missing required fields
5. Write test: DecisionOutput valid instantiation
6. Write test: DecisionOutput reject invalid intent
7. Write test: LLMOutput valid answer type
8. Write test: LLMOutput valid tool_call type
9. Write test: LLMOutput reject mismatched type/content
10. Write test: ToolResult valid instantiation
11. Write test: FinalResponse valid instantiation

Input:
- pytest run

Output:
- All tests pass

Dependencies:
- TASK 2.1 through 2.5

Validation:
```bash
pytest tests/test_contracts.py -v
```

Artifact: `tests/test_contracts.py`

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

### Tasks

**TASK 3.1 — RuntimeState enum**

Location:
- `src/core/runtime/state.py`

Purpose:
- Define all runtime states from README state machine table

Steps:
1. Create `src/core/runtime/state.py`
2. Define `RuntimeState` enum with values:
   - IDLE, DECIDING, EXECUTING_MODEL, EXECUTING_TOOL, WAITING_CONFIRMATION, EVALUATING, ERROR, COMPLETED
3. Add `allowed_next_states` mapping for each state
4. Implement `can_transition(from, to)` validation function

Input:
- State enum values

Output:
- Enum definition with validation

Dependencies:
- None

Validation:
```bash
python -c "from src.core.runtime.state import RuntimeState; print(RuntimeState.IDLE.can_transition(RuntimeState.DECIDING))"
```

Artifact: `src/core/runtime/state.py`

---

**TASK 3.2 — State manager**

Location:
- `src/core/runtime/state_manager.py`

Purpose:
- Implement state manager to control transitions and track state history

Steps:
1. Create `src/core/runtime/state_manager.py`
2. Define `StateManager` class
3. Implement `current_state` property
4. Implement `transition_to(new_state)` with validation
5. Add state history tracking
6. Implement `force_state(state)` for error recovery
7. Add logging on each transition

Input:
- Target state for transition

Output:
- Valid state transition or error

Dependencies:
- TASK 3.1 (RuntimeState)

Validation:
```bash
python -c "from src.core.runtime.state_manager import StateManager; sm = StateManager(); sm.transition_to(RuntimeState.DECIDING); print(sm.current_state)"
```

Artifact: `src/core/runtime/state_manager.py`

---

**TASK 3.3 — Hard limits**

Location:
- `src/core/runtime/limits.py`

Purpose:
- Define and enforce all hard limits from README execution flow

Steps:
1. Create `src/core/runtime/limits.py`
2. Define limit constants:
   - max_iterations = 5
   - max_tool_calls = 3
   - max_tool_depth = 3
   - max_retries = 2
   - tool_timeout_s = 30
   - model_timeout_s = 120
   - step_timeout_s = 60
   - total_turn_timeout_s = 300
3. Implement `Limits` class that loads from config
4. Add `check_limit(limit_name, current_value)` validation

Input:
- Limit name, current value

Output:
- True if within limit, False if exceeded

Dependencies:
- TASK 1.1 (config system)

Validation:
```bash
python -c "from src.core.runtime.limits import Limits; l = Limits(); print(l.max_iterations)"
```

Artifact: `src/core/runtime/limits.py`

---

**TASK 3.4 — Context assembler**

Location:
- `src/core/context/assembler.py`

Purpose:
- Implement InputPacket assembly from user input and system state

Steps:
1. Create `src/core/context/assembler.py`
2. Define `ContextAssembler` class
3. Implement `assemble_context(user_input, session_id)` method
4. Load user profile
5. Fetch memory snippets (recent)
6. Build recent history from memory
7. Return complete InputPacket

Input:
- user_input: str, session_id: str

Output:
- InputPacket object

Dependencies:
- TASK 2.1 (InputPacket)
- TASK 1.7 (UserProfile)
- TASK 10.1 (Memory retrieval - can use stub)

Validation:
```bash
python -c "from src.core.context.assembler import ContextAssembler; a = ContextAssembler(); p = a.assemble_context('hello', 's1'); print(p.user_message)"
```

Artifact: `src/core/context/assembler.py`

---

**TASK 3.5 — Decision function**

Location:
- `src/core/decision/decision.py` (expand TASK 2.2)

Purpose:
- Implement decision function with dynamic scoring

Steps:
1. Expand `src/core/decision/decision.py`
2. Define `decide(input_packet)` function
3. Implement dynamic weighted scoring:
   - fit_complexity: 1.0
   - fit_mode: 1.0
   - cost_penalty: 0.35
   - quality_need: 1.2
   - memory_bias: 0.25
4. Evaluate all candidate models
5. Apply tie-break logic (cost → latency → success rate)
6. Return DecisionOutput with score_breakdown and candidate_list
7. Add validation: reject if score_breakdown missing

Input:
- InputPacket

Output:
- DecisionOutput with full scoring metadata

Dependencies:
- TASK 2.2 (DecisionOutput)
- TASK 1.4 (Model profiles)
- TASK 3.3 (limits for retry counting)

Validation:
```bash
python -c "from src.core.decision.decision import decide; from src.core.context.bundle import InputPacket; p = InputPacket(user_message='hello', session_id='s1'); d = decide(p); print(d.model, d.score_breakdown)"
```

Artifact: `src/core/decision/decision.py`

---

**TASK 3.6 — Executor**

Location:
- `src/core/runtime/executor.py`

Purpose:
- Implement LLM execution with model calling and output parsing

Steps:
1. Create `src/core/runtime/executor.py`
2. Define `Executor` class
3. Implement `execute_turn(decision, input_packet)` method
4. Call LLM with decision.model
5. Parse output to LLMOutput
6. Handle JSON extraction from messy text
7. Apply timeout from limits
8. Return LLMOutput

Input:
- DecisionOutput, InputPacket

Output:
- LLMOutput

Dependencies:
- TASK 2.3 (LLMOutput)
- TASK 1.5 (LLM engine)
- TASK 3.3 (limits)

Validation:
```bash
python -c "from src.core.runtime.executor import Executor; e = Executor(); print('Executor created')"
```

Artifact: `src/core/runtime/executor.py`

---

**TASK 3.7 — Evaluator**

Location:
- `src/core/runtime/evaluator.py`

Purpose:
- Implement response quality evaluation

Steps:
1. Create `src/core/runtime/evaluator.py`
2. Define `Evaluator` class
3. Implement `evaluate(output, decision)` method
4. Check completeness (answer not truncated)
5. Check coherence (logical consistency)
6. Check relevance (addresses input)
7. Apply ONLY on: long responses (>500 tokens), complex tasks, fallback outputs
8. Return evaluation result with should_retry flag

Input:
- LLMOutput, DecisionOutput

Output:
- EvaluationResult with should_retry flag

Dependencies:
- TASK 2.3 (LLMOutput)

Validation:
```bash
python -c "from src.core.runtime.evaluator import Evaluator; e = Evaluator(); print('Evaluator created')"
```

Artifact: `src/core/runtime/evaluator.py`

---

**TASK 3.8 — Runtime loop**

Location:
- `src/core/runtime/loop.py`

Purpose:
- Implement main runtime loop enforcing Observe → Decide → Think → Act → Evaluate

Steps:
1. Create `src/core/runtime/loop.py`
2. Define `run_turn(user_input, session_id)` function
3. Implement loop with states:
   - Assemble context (Observe)
   - Run decision (Decide)
   - Execute model (Think)
   - Execute tool if needed (Act)
   - Evaluate response (Evaluate)
4. Enforce max_iterations, max_tool_depth
5. Handle state transitions via StateManager
6. Return FinalResponse

Input:
- user_input: str, session_id: str

Output:
- FinalResponse

Dependencies:
- TASK 3.1-3.7 (all runtime components)

Validation:
```bash
python -c "from src.core.runtime.loop import run_turn; r = run_turn('hello', 'test'); print(r.text)"
```

Artifact: `src/core/runtime/loop.py`

---

**TASK 3.9 — EventBus**

Location:
- `src/core/events.py`

Purpose:
- Implement event system for loose coupling between components

Steps:
1. Create `src/core/events.py`
2. Define `EventBus` class
3. Implement `subscribe(event_type, handler)` method
4. Implement `publish(event_type, data)` method
5. Add event types from README: runtime.state, turn.start, decision, tool.start, tool.done, etc.
6. Support async handlers

Input:
- Event type and data

Output:
- Event published to all subscribers

Dependencies:
- None (standalone infrastructure)

Validation:
```bash
python -c "from src.core.events import EventBus; eb = EventBus(); print('EventBus created')"
```

Artifact: `src/core/events.py`

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

Harden decision system with robust classification and dynamic scoring.

### Tasks

**TASK 4.1 — Classifier robust JSON parsing**

Location:
- `src/core/decision/classifier.py` (expand TASK 0.2)

Purpose:
- Enhance classifier with robust JSON extraction and repair

Steps:
1. Expand `src/core/decision/classifier.py`
2. Implement `extract_json(text)` function
3. Handle: markdown code blocks, trailing text, malformed JSON
4. Add JSON repair for common issues (missing quotes, trailing commas)
5. Retry with exponential backoff (max 2 retries)
6. Return safe fallback on all failures: {intent: "chat", tool_name: null, tool_args: {}}

Input:
- Raw LLM text output

Output:
- Parsed dict or fallback dict

Dependencies:
- TASK 0.2 (base classifier)

Validation:
```bash
python -c "from src.core.decision.classifier import extract_json; print(extract_json('```json\n{\"intent\": \"chat\"}\n```'))"
```

Artifact: `src/core/decision/classifier.py`

---

**TASK 4.2 — Fast-path rules**

Location:
- `src/core/decision/fast_path.py`

Purpose:
- Implement rule-based fast path for common intents to avoid LLM call

Steps:
1. Create `src/core/decision/fast_path.py`
2. Define `FastPath` class
3. Implement rules for:
   - "open X" → intent=tool_use, tool_name=open_app
   - "what is/who is" → intent=chat
   - "search for" → intent=search
4. Return DecisionOutput if matched, None if not
5. Skip LLM call when fast path matches

Input:
- user_message string

Output:
- DecisionOutput or None

Dependencies:
- TASK 2.2 (DecisionOutput)

Validation:
```bash
python -c "from src.core.decision.fast_path import FastPath; fp = FastPath(); print(fp.check('open notepad'))"
```

Artifact: `src/core/decision/fast_path.py`

---

**TASK 4.3 — Risk level population**

Location:
- `src/core/decision/risk.py`

Purpose:
- Determine risk level based on intent, tool, and arguments

Steps:
1. Create `src/core/decision/risk.py`
2. Define `RiskAssessor` class
3. Implement `assess(decision)` method
4. Rules: system tools = medium/high, file ops = medium, search = low
5. Check arguments for dangerous patterns
6. Return risk_level: low|medium|high

Input:
- DecisionOutput

Output:
- risk_level string

Dependencies:
- TASK 2.2 (DecisionOutput)

Validation:
```bash
python -c "from src.core.decision.risk import RiskAssessor; ra = RiskAssessor(); print(ra.assess(...))"
```

Artifact: `src/core/decision/risk.py`

---

**TASK 4.4 — Escalation chain**

Location:
- `src/core/runtime/escalation.py`

Purpose:
- Implement decision retry with scoring weight adjustment

Steps:
1. Create `src/core/runtime/escalation.py`
2. Define `EscalationChain` class
3. Implement `retry_decision(input, attempt_number)` method
4. Adjust scoring weights slightly per retry
5. Reduce constraints on subsequent retries
6. After 3 attempts, trigger fallback system (gemma3:4b)
7. Log all retry attempts

Input:
- InputPacket, attempt number

Output:
- DecisionOutput or fallback

Dependencies:
- TASK 3.5 (decision function)
- TASK 3.3 (max_decision_retries = 3)

Validation:
```bash
python -c "from src.core.runtime.escalation import EscalationChain; ec = EscalationChain(); print('EscalationChain created')"
```

Artifact: `src/core/runtime/escalation.py`

---

**TASK 4.5 — Decision tests**

Location:
- `tests/test_decision.py`

Purpose:
- Comprehensive tests for decision system including dynamic scoring

Steps:
1. Create `tests/test_decision.py`
2. Test: fast path matches "open notepad"
3. Test: classifier parses valid JSON
4. Test: classifier handles malformed JSON with retry
5. Test: decision includes score_breakdown
6. Test: decision includes candidate_list
7. Test: invalid decision rejected (no score_breakdown)
8. Test: model choice varies with input complexity
9. Test: tie-break logic (cost, latency, success rate)
10. Test: escalation retries 3 times then falls back

Input:
- pytest run

Output:
- All tests pass

Dependencies:
- TASK 4.1 through 4.4

Validation:
```bash
pytest tests/test_decision.py -v
```

Artifact: `tests/test_decision.py`

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

Build identity and prompt assembly system.

### Tasks

**TASK 5.1 — Jarvis identity YAML**

Location:
- `config/jarvis_identity.yaml`

Purpose:
- Define Jarvis identity, personality, and behavior constraints

Steps:
1. Create `config/jarvis_identity.yaml`
2. Define: name, role, personality traits, capabilities list
3. Add language support: English, Arabic
4. Define behavior constraints (local-first, no cloud fallback)
5. Add mode-specific behavior fragments

Input:
- None (definition file)

Output:
- YAML identity file

Dependencies:
- None

Validation:
```bash
python -c "import yaml; i = yaml.safe_load(open('config/jarvis_identity.yaml')); print(i['name'])"
```

Artifact: `config/jarvis_identity.yaml`

---

**TASK 5.2 — Mode fragments**

Location:
- `config/mode_fragments.yaml`

Purpose:
- Define prompt fragments for each execution mode

Steps:
1. Create `config/mode_fragments.yaml`
2. Define fragments for modes: fast, normal, deep, planning, research
3. Each fragment: system prompt addition, behavior rules, output format
4. Add mode-specific constraints

Input:
- None (definition file)

Output:
- YAML fragments file

Dependencies:
- None

Validation:
```bash
python -c "import yaml; f = yaml.safe_load(open('config/mode_fragments.yaml')); print(len(f['fragments']))"
```

Artifact: `config/mode_fragments.yaml`

---

**TASK 5.3 — System prompt builder**

Location:
- `src/core/context/builder.py`

Purpose:
- Assemble system prompt from identity, mode, and context

Steps:
1. Create `src/core/context/builder.py`
2. Define `PromptBuilder` class
3. Implement `build_prompt(decision, input_packet)` method
4. Load identity from YAML
5. Load mode fragment
6. Add context (history, memory snippets)
7. Return complete system prompt string

Input:
- DecisionOutput, InputPacket

Output:
- Complete prompt string

Dependencies:
- TASK 5.1 (identity YAML)
- TASK 5.2 (mode fragments)
- TASK 2.1, 2.2 (contracts)

Validation:
```bash
python -c "from src.core.context.builder import PromptBuilder; pb = PromptBuilder(); print('PromptBuilder created')"
```

Artifact: `src/core/context/builder.py`

---

**TASK 5.4 — Wire into executor**

Location:
- `src/core/runtime/executor.py` (expand TASK 3.6)

Purpose:
- Integrate prompt builder into LLM execution

Steps:
1. Expand `src/core/runtime/executor.py`
2. Add `PromptBuilder` instance
3. Call `build_prompt()` before LLM call
4. Pass complete prompt to LLM engine
5. Ensure identity block in every LLM call

Input:
- DecisionOutput, InputPacket (same as TASK 3.6)

Output:
- LLMOutput (same as TASK 3.6)

Dependencies:
- TASK 5.3 (PromptBuilder)
- TASK 3.6 (Executor base)

Validation:
```bash
python -c "from src.core.runtime.executor import Executor; e = Executor(); print('Executor with prompt builder')"
```

Artifact: `src/core/runtime/executor.py`

---

**TASK 5.5 — Identity test**

Location:
- `tests/test_identity_enforcement.py`

Purpose:
- Verify identity block present in all LLM calls

Steps:
1. Create `tests/test_identity_enforcement.py`
2. Test: system prompt contains Jarvis identity
3. Test: identity present in all modes (fast, normal, deep, etc.)
4. Test: Arabic identity works
5. Test: mode fragments applied correctly

Input:
- pytest run

Output:
- All tests pass

Dependencies:
- TASK 5.1 through 5.4

Validation:
```bash
pytest tests/test_identity_enforcement.py -v
```

Artifact: `tests/test_identity_enforcement.py`

---

## Phase 6 — Capability System

```
phase_id: 6
title: "Capability System"
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

Build complete capability execution pipeline.

### Tasks

**TASK 6.1 — BaseCapability abstract class**

Location:
- `src/capabilities/base.py`

Purpose:
- Define abstract base class for all capabilities

Steps:
1. Create `src/capabilities/base.py`
2. Define `BaseCapability` abstract class
3. Abstract methods: `execute(args)`, `validate(args)`, `get_risk_level()`
4. Properties: name, domain, description, risk_level
5. Implement `to_dict()` for manifest registration

Input:
- Capability-specific args dict

Output:
- ToolResult (from TASK 2.4)

Dependencies:
- TASK 2.4 (ToolResult)

Validation:
```bash
python -c "from src.capabilities.base import BaseCapability; print('BaseCapability defined')"
```

Artifact: `src/capabilities/base.py`

---

**TASK 6.2 — Capability registry**

Location:
- `src/capabilities/registry.py`

Purpose:
- Implement registry to manage all capabilities

Steps:
1. Create `src/capabilities/registry.py`
2. Define `CapabilityRegistry` class
3. Implement `register(capability)` method
4. Implement `get(name)` method
5. Implement `list_all()` method
6. Load capabilities from `config/capabilities.yaml` manifest
7. Auto-discover capability modules

Input:
- Capability name or manifest

Output:
- Registered capability instance or list

Dependencies:
- TASK 6.1 (BaseCapability)
- TASK 1.8 (capabilities manifest)

Validation:
```bash
python -c "from src.capabilities.registry import CapabilityRegistry; r = CapabilityRegistry(); print('Registry created')"
```

Artifact: `src/capabilities/registry.py`

---

**TASK 6.3 — Safety classifier**

Location:
- `src/core/safety/classifier.py`

Purpose:
- Classify capability calls by risk level based on arguments

Steps:
1. Create `src/core/safety/` directory
2. Create `src/core/safety/classifier.py`
3. Define `SafetyClassifier` class
4. Implement `classify(capability, args)` method
5. Check paths (must be within allowed roots)
6. Check commands for dangerous patterns (rm -rf, format, etc.)
7. Return risk_level: low|medium|high

Input:
- Capability instance, args dict

Output:
- risk_level string

Dependencies:
- TASK 6.1 (BaseCapability)

Validation:
```bash
python -c "from src.core.safety.classifier import SafetyClassifier; sc = SafetyClassifier(); print('SafetyClassifier created')"
```

Artifact: `src/core/safety/classifier.py`

---

**TASK 6.4 — Mode enforcement**

Location:
- `src/core/safety/mode_enforcer.py`

Purpose:
- Enforce execution modes (SAFE/BALANCED/UNRESTRICTED) per README spec

Steps:
1. Create `src/core/safety/mode_enforcer.py`
2. Define `ModeEnforcer` class
3. Implement `check_permission(capability, risk_level, mode)` method
4. SAFE mode: confirm all tools
5. BALANCED mode: low=auto, medium=confirm, high=blocked (with override phrase)
6. UNRESTRICTED: auto-execute all
7. Return: allow|confirm|block

Input:
- Capability, risk_level, execution mode

Output:
- Permission decision

Dependencies:
- TASK 6.3 (SafetyClassifier)

Validation:
```bash
python -c "from src.core.safety.mode_enforcer import ModeEnforcer; me = ModeEnforcer(); print('ModeEnforcer created')"
```

Artifact: `src/core/safety/mode_enforcer.py`

---

**TASK 6.5 — Schema validator**

Location:
- `src/capabilities/validator.py`

Purpose:
- Validate capability arguments against schema

Steps:
1. Create `src/capabilities/validator.py`
2. Define `SchemaValidator` class
3. Implement `validate(capability, args)` method
4. Check required fields present
5. Check field types match schema
6. Return validation result with error messages

Input:
- Capability, args dict

Output:
- ValidationResult (valid: bool, errors: list)

Dependencies:
- TASK 6.1 (BaseCapability)

Validation:
```bash
python -c "from src.capabilities.validator import SchemaValidator; sv = SchemaValidator(); print('SchemaValidator created')"
```

Artifact: `src/capabilities/validator.py`

---

**TASK 6.6 — Capability executor**

Location:
- `src/capabilities/executor.py`

Purpose:
- Execute capabilities with full safety pipeline

Steps:
1. Create `src/capabilities/executor.py`
2. Define `CapabilityExecutor` class
3. Implement `execute(name, args, mode)` method
4. Gate 1: Check capability exists in registry
5. Gate 2: Validate args schema
6. Gate 3: Run safety classifier for risk level
7. Gate 4: Check mode enforcement permission
8. Execute capability if allowed
9. Return ToolResult

Input:
- Capability name, args, execution mode

Output:
- ToolResult

Dependencies:
- TASK 6.1 through 6.5 (all capability system components)

Validation:
```bash
python -c "from src.capabilities.executor import CapabilityExecutor; ce = CapabilityExecutor(); print('CapabilityExecutor created')"
```

Artifact: `src/capabilities/executor.py`

---

**TASK 6.7 — Parse retry**

Location:
- `src/core/runtime/llm_output.py` (expand TASK 2.3)

Purpose:
- Enhance LLM output parsing with retry and recovery

Steps:
1. Expand `src/core/runtime/llm_output.py`
2. Implement `parse_with_retry(raw_text, max_retries=2)` function
3. Extract JSON from messy LLM output
4. If parse fails, retry with correction prompt
5. Fallback to text mode if all retries fail
6. Log all parse failures

Input:
- Raw LLM text output

Output:
- LLMOutput or fallback answer

Dependencies:
- TASK 2.3 (LLMOutput base)

Validation:
```bash
python -c "from src.core.runtime.llm_output import parse_with_retry; print(parse_with_retry('invalid json'))"
```

Artifact: `src/core/runtime/llm_output.py`

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

Implement three-mode policy with risk classification.

### Tasks

**TASK 7.1 — Execution mode in config**

Location:
- `config/settings.yaml` (expand TASK 1.1)

Purpose:
- Add execution mode settings to configuration

Steps:
1. Expand `config/settings.yaml`
2. Add `execution_mode: BALANCED` (default)
3. Add `allowed_modes: [SAFE, BALANCED, UNRESTRICTED]`
4. Add `dangerous_patterns` list from README
5. Update `src/core/config.py` to include new fields

Input:
- None (config expansion)

Output:
- Updated config with execution mode

Dependencies:
- TASK 1.1 (base config)

Validation:
```bash
python -c "from src.core.config import load_config; s = load_config('config/settings.yaml'); print(s.execution_mode)"
```

Artifact: `config/settings.yaml`, `src/core/config.py`

---

**TASK 7.2 — Risk levels on all capabilities**

Location:
- `config/capabilities.yaml` (expand TASK 1.8)

Purpose:
- Ensure every capability has explicit risk_level in manifest

Steps:
1. Expand `config/capabilities.yaml`
2. Add `risk_level` to each capability (low|medium|high)
3. Define risk criteria per domain:
   - system: medium-high
   - files: medium
   - web_automation: medium
   - screen: low
   - vision: low
   - voice: low
4. Validate all capabilities have risk_level

Input:
- None (manifest update)

Output:
- Updated manifest with risk levels

Dependencies:
- TASK 1.8 (base manifest)

Validation:
```bash
python -c "import yaml; m = yaml.safe_load(open('config/capabilities.yaml')); [print(c['name'], c['risk_level']) for c in m['capabilities']]"
```

Artifact: `config/capabilities.yaml`

---

**TASK 7.3 — CLI mode toggle**

Location:
- `src/interfaces/cli/commands.py`

Purpose:
- Allow execution mode toggle via CLI

Steps:
1. Create `src/interfaces/cli/` directory
2. Create `src/interfaces/cli/commands.py`
3. Implement `--mode` CLI argument
4. Add `/mode SAFE|BALANCED|UNRESTRICTED` command in chat
5. Validate mode change
6. Persist mode to user profile

Input:
- CLI argument or chat command

Output:
- Mode changed confirmation

Dependencies:
- TASK 1.7 (user profile for persistence)
- TASK 7.1 (mode config)

Validation:
```bash
python app/main.py --interface cli --mode SAFE
# In chat: /mode BALANCED
```

Artifact: `src/interfaces/cli/commands.py`

---

**TASK 7.4 — Safety tests**

Location:
- `tests/test_safety.py`

Purpose:
- Comprehensive tests for safety modes and risk classification

Steps:
1. Create `tests/test_safety.py`
2. Test: SAFE mode confirms all tools
3. Test: BALANCED mode auto-executes low risk
4. Test: BALANCED mode requires confirmation for medium
5. Test: BALANCED mode blocks high (with override phrase check)
6. Test: UNRESTRICTED auto-executes all
7. Test: dangerous patterns always blocked
8. Test: risk levels correctly assigned per capability

Input:
- pytest run

Output:
- All tests pass

Dependencies:
- TASK 7.1 through 7.3

Validation:
```bash
pytest tests/test_safety.py -v
```

Artifact: `tests/test_safety.py`

---

## Phase 8 — System Control Capabilities

```
phase_id: 8
title: "System Control Capabilities"
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

Implement system control capabilities for cross-platform OS interaction.

### Tasks

**TASK 8.1 — App launcher capability**

Location:
- `src/capabilities/system/apps.py` (expand TASK 0.3)

Purpose:
- Full app launcher capability with cross-platform support and safety

Steps:
1. Expand `src/capabilities/system/apps.py`
2. Inherit from `BaseCapability`
3. Implement `execute(args)` with args: name (app name)
4. Windows: search PATH, Program Files, Start Menu, registry
5. Linux: search PATH, /usr/share/applications, /usr/local/bin
6. macOS: search PATH, /Applications, ~/Applications
7. Return ToolResult with success/error and PID
8. Add safety: block dangerous apps (format, mkfs, etc.)

Input:
- args: {name: str}

Output:
- ToolResult with PID or error

Dependencies:
- TASK 6.1 (BaseCapability)
- TASK 0.3 (base implementation)

Validation:
```bash
python -c "from src.capabilities.system.apps import AppLauncher; al = AppLauncher(); print(al.execute({'name': 'notepad'}))"
```

Artifact: `src/capabilities/system/apps.py`

---

**TASK 8.2 — System info capability**

Location:
- `src/capabilities/system/sysinfo.py`

Purpose:
- Gather system information (OS, CPU, RAM, GPU)

Steps:
1. Create `src/capabilities/system/sysinfo.py`
2. Define `SystemInfoCapability` inheriting BaseCapability
3. Implement `execute(args)` with args: info_type (all|cpu|ram|gpu|os)
4. Use platform, psutil, GPUtil for detection
5. Cross-platform: Windows, Linux, macOS
6. Return ToolResult with system info dict

Input:
- args: {info_type: str}

Output:
- ToolResult with system info

Dependencies:
- TASK 6.1 (BaseCapability)

Validation:
```bash
python -c "from src.capabilities.system.sysinfo import SystemInfoCapability; si = SystemInfoCapability(); print(si.execute({'info_type': 'all'}))"
```

Artifact: `src/capabilities/system/sysinfo.py`

---

**TASK 8.3 — Clipboard capability**

Location:
- `src/capabilities/system/clipboard.py`

Purpose:
- Read from and write to system clipboard

Steps:
1. Create `src/capabilities/system/clipboard.py`
2. Define `ClipboardCapability` inheriting BaseCapability
3. Implement `execute(args)` with args: action (read|write), content (for write)
4. Use pyperclip for cross-platform support
5. Windows/Linux/macOS: same API via pyperclip
6. Return ToolResult with clipboard content or success

Input:
- args: {action: str, content: str|null}

Output:
- ToolResult with clipboard data

Dependencies:
- TASK 6.1 (BaseCapability)

Validation:
```bash
python -c "from src.capabilities.system.clipboard import ClipboardCapability; cb = ClipboardCapability(); print(cb.execute({'action': 'read'}))"
```

Artifact: `src/capabilities/system/clipboard.py`

---

**TASK 8.4 — Notifications capability**

Location:
- `src/capabilities/notify/toasts.py`

Purpose:
- Send system notifications to user

Steps:
1. Create `src/capabilities/notify/` directory
2. Create `src/capabilities/notify/toasts.py`
3. Define `NotificationCapability` inheriting BaseCapability
4. Implement `execute(args)` with args: title, message, duration
5. Windows: use win10toast or plyer
6. Linux: use notify-send or plyer
7. macOS: use osascript or plyer
8. Return ToolResult with success

Input:
- args: {title: str, message: str, duration: int}

Output:
- ToolResult with success/error

Dependencies:
- TASK 6.1 (BaseCapability)

Validation:
```bash
python -c "from src.capabilities.notify.toasts import NotificationCapability; n = NotificationCapability(); print(n.execute({'title': 'Test', 'message': 'Hello'}))"
```

Artifact: `src/capabilities/notify/toasts.py`

---

**TASK 8.5 — Screenshot/OCR capability**

Location:
- `src/capabilities/screen/capture.py`

Purpose:
- Capture screen and optionally extract text via OCR

Steps:
1. Create `src/capabilities/screen/` directory
2. Create `src/capabilities/screen/capture.py`
3. Define `ScreenshotCapability` inheriting BaseCapability
4. Implement `execute(args)` with args: ocr (bool), region (x,y,w,h or full)
5. Use PIL/Pillow for screenshot
6. Use pytesseract for OCR (optional)
7. Windows/Linux/macOS: use appropriate screenshot method
8. Return ToolResult with image path or OCR text

Input:
- args: {ocr: bool, region: list|null}

Output:
- ToolResult with image path or text

Dependencies:
- TASK 6.1 (BaseCapability)

Validation:
```bash
python -c "from src.capabilities.screen.capture import ScreenshotCapability; sc = ScreenshotCapability(); print(sc.execute({'ocr': False}))"
```

Artifact: `src/capabilities/screen/capture.py`

---

**TASK 8.6 — File operations capability**

Location:
- `src/capabilities/files/file_ops.py`

Purpose:
- Perform file operations: read, write, list, delete, move, copy

Steps:
1. Create `src/capabilities/files/` directory
2. Create `src/capabilities/files/file_ops.py`
3. Define `FileOpsCapability` inheriting BaseCapability
4. Implement `execute(args)` with args: action (read|write|list|delete|move|copy), path, content (for write)
5. Safety: enforce path within allowed roots
6. Safety: block dangerous operations (delete system files)
7. Cross-platform path handling
8. Return ToolResult with file data or success

Input:
- args: {action: str, path: str, content: str|null}

Output:
- ToolResult with file data or success

Dependencies:
- TASK 6.1 (BaseCapability)
- TASK 6.3 (safety classifier for path checks)

Validation:
```bash
python -c "from src.capabilities.files.file_ops import FileOpsCapability; fo = FileOpsCapability(); print(fo.execute({'action': 'list', 'path': '.'}))"
```

Artifact: `src/capabilities/files/file_ops.py`

---

**TASK 8.7 — Code executor capability**

Location:
- `src/capabilities/coder/executor.py`

Purpose:
- Execute code snippets in sandboxed environment

Steps:
1. Create `src/capabilities/coder/` directory
2. Create `src/capabilities/coder/executor.py`
3. Define `CodeExecutorCapability` inheriting BaseCapability
4. Implement `execute(args)` with args: language (python|javascript|bash), code
5. Use subprocess with timeout for execution
6. Capture stdout, stderr, return code
7. Safety: restrict to temp directory, limit resources
8. Return ToolResult with execution output

Input:
- args: {language: str, code: str}

Output:
- ToolResult with execution result

Dependencies:
- TASK 6.1 (BaseCapability)

Validation:
```bash
python -c "from src.capabilities.coder.executor import CodeExecutorCapability; ce = CodeExecutorCapability(); print(ce.execute({'language': 'python', 'code': 'print(1+1)'}))"
```

Artifact: `src/capabilities/coder/executor.py`

---

**TASK 8.8 — Web search capability**

Location:
- `src/capabilities/search/web_search.py`

Purpose:
- Perform web searches and return results

Steps:
1. Create `src/capabilities/search/` directory
2. Create `src/capabilities/search/web_search.py`
3. Define `WebSearchCapability` inheriting BaseCapability
4. Implement `execute(args)` with args: query, count (results count)
5. Use requests + BeautifulSoup for scraping (no API key required)
6. Parse search results: title, url, snippet
7. Return ToolResult with results list

Input:
- args: {query: str, count: int}

Output:
- ToolResult with search results

Dependencies:
- TASK 6.1 (BaseCapability)

Validation:
```bash
python -c "from src.capabilities.search.web_search import WebSearchCapability; ws = WebSearchCapability(); print(ws.execute({'query': 'python', 'count': 3}))"
```

Artifact: `src/capabilities/search/web_search.py`

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

Add recovery systems and protection to runtime.

### Tasks

**TASK 9.1 — LLM Output Recovery**

Location:
- `src/core/runtime/llm_output.py` (expand TASK 6.7)

Purpose:
- Enhance LLM output parsing with advanced recovery mechanisms

Steps:
1. Further expand `src/core/runtime/llm_output.py`
2. Implement `extract_json_advanced(text)` with multiple strategies:
   - Strategy 1: Direct JSON parse
   - Strategy 2: Extract JSON from markdown blocks
   - Strategy 3: Find JSON-like structure with regex
   - Strategy 4: Repair common JSON errors
3. Implement `auto_repair_json(text)` for common issues
4. Fallback to text mode with `type=answer, content=raw_text`
5. Log all recovery attempts

Input:
- Raw LLM text

Output:
- LLMOutput or repaired LLMOutput

Dependencies:
- TASK 6.7 (base parse retry)

Validation:
```bash
python -c "from src.core.runtime.llm_output import extract_json_advanced; print(extract_json_advanced('{invalid json}'))"
```

Artifact: `src/core/runtime/llm_output.py`

---

**TASK 9.2 — Tool Permission Layer**

Location:
- `src/core/safety/permission.py`

Purpose:
- Implement three-gate permission system from README

Steps:
1. Create `src/core/safety/permission.py`
2. Define `PermissionLayer` class
3. Implement `check_permission(tool_name, args, decision, user_context)` method
4. Gate 1: Decision consistency - does tool match intent?
5. Gate 2: Argument safety - paths within roots, no dangerous patterns
6. Gate 3: User context - does tool match user intent?
7. Return: allow|block with reason

Input:
- Tool name, args, DecisionOutput, user context

Output:
- Permission result with allow/block and reason

Dependencies:
- TASK 6.3 (safety classifier)
- TASK 6.4 (mode enforcer)

Validation:
```bash
python -c "from src.core.safety.permission import PermissionLayer; pl = PermissionLayer(); print('PermissionLayer created')"
```

Artifact: `src/core/safety/permission.py`

---

**TASK 9.3 — Tool Chain Control**

Location:
- `src/core/safety/chain_control.py`

Purpose:
- Detect and prevent tool loops and depth violations

Steps:
1. Create `src/core/safety/chain_control.py`
2. Define `ChainController` class
3. Implement `check_depth(tool_history)` - max depth = 3
4. Implement `detect_loop(tool_history)` - same tool 3+ times
5. Implement `track_tool(tool_name)` to update history
6. Return: allow|block with reason
7. Log loop_detected events

Input:
- Tool history list

Output:
- Chain control result

Dependencies:
- TASK 3.3 (limits for max_tool_depth)

Validation:
```bash
python -c "from src.core.safety.chain_control import ChainController; cc = ChainController(); print('ChainController created')"
```

Artifact: `src/core/safety/chain_control.py`

---

**TASK 9.4 — Timeout Handling**

Location:
- `src/core/runtime/timeout.py`

Purpose:
- Implement timeout handling for all execution phases

Steps:
1. Create `src/core/runtime/timeout.py`
2. Define `TimeoutHandler` class
3. Implement `check_timeout(phase, start_time)` for each phase:
   - model: model_timeout_s = 120
   - tool: tool_timeout_s = 30
   - step: step_timeout_s = 60
   - total: total_turn_timeout_s = 300
4. Implement `enforce_timeout(phase)` decorator
5. Return: timeout exceeded boolean

Input:
- Phase name, start time

Output:
- Timeout check result

Dependencies:
- TASK 3.3 (limits for timeout values)

Validation:
```bash
python -c "from src.core.runtime.timeout import TimeoutHandler; th = TimeoutHandler(); print('TimeoutHandler created')"
```

Artifact: `src/core/runtime/timeout.py`

---

**TASK 9.5 — Graceful Degradation**

Location:
- `src/core/runtime/degradation.py`

Purpose:
- Handle failures gracefully with fallback responses

Steps:
1. Create `src/core/runtime/degradation.py`
2. Define `DegradationHandler` class
3. Implement `handle_model_failure(model, error)` - swap to fallback
4. Implement `handle_tool_failure(tool, error)` - log and continue
5. Implement `generate_error_response(error_type)` - user-friendly message
6. Ensure runtime never crashes
7. Log all degradation events

Input:
- Error type and details

Output:
- Fallback response or error message

Dependencies:
- TASK 4.4 (escalation chain for fallbacks)

Validation:
```bash
python -c "from src.core.runtime.degradation import DegradationHandler; dh = DegradationHandler(); print('DegradationHandler created')"
```

Artifact: `src/core/runtime/degradation.py`

---

**TASK 9.6 — State Machine Tests**

Location:
- `tests/test_state_machine.py`

Purpose:
- Comprehensive tests for state machine and all transitions

Steps:
1. Create `tests/test_state_machine.py`
2. Test: all valid transitions work
3. Test: invalid transitions rejected (IDLE → EXECUTING_TOOL)
4. Test: max_iterations enforcement stops loop
5. Test: max_tool_depth enforcement stops nesting
6. Test: timeout enforcement
7. Test: error state transitions to IDLE
8. Test: all limits from TASK 3.3 enforced

Input:
- pytest run

Output:
- All tests pass

Dependencies:
- TASK 3.1 through 3.9 (all runtime components)

Validation:
```bash
pytest tests/test_state_machine.py -v
```

Artifact: `tests/test_state_machine.py`

---

## Phase 10 — Memory (Simplified)

```
phase_id: 10
title: "Memory (Simplified)"
priority: "P1"
status: "not_started"
progress_percent: 0
done_tasks: 0
total_tasks: 3
blocker: "Phase 9 must complete"
next_action: "Start TASK 10.1"
last_updated: "-"
validation_status: "not_started"
```

### Objective

Implement simple memory system with short-term and long-term storage.

### Tasks

**TASK 10.1 — Memory database**

Location:
- `src/memory/database.py`

Purpose:
- Implement SQLite-based memory storage

Steps:
1. Expand `src/memory/` directory
2. Create `src/memory/database.py`
3. Define `MemoryDB` class
4. Implement `store(session_id, turn_data)` method
5. Implement `retrieve(session_id, limit)` method
6. Implement `search(keywords)` method for long-term memory
7. Use SQLite with tables: turns, memory_snippets
8. Handle short-term (recent turns) and long-term (searchable)

Input:
- Session ID, turn data

Output:
- Stored/retrieved memory data

Dependencies:
- TASK 1.1 (config for DB path)

Validation:
```bash
python -c "from src.memory.database import MemoryDB; db = MemoryDB(); print('MemoryDB created')"
```

Artifact: `src/memory/database.py`

---

**TASK 10.2 — Context retriever**

Location:
- `src/memory/retriever.py`

Purpose:
- Retrieve relevant context for current turn

Steps:
1. Create `src/memory/retriever.py`
2. Define `ContextRetriever` class
3. Implement `get_context(session_id, query)` method
4. Fetch recent history (short-term)
5. Search relevant snippets (long-term)
6. Return bundled context for InputPacket

Input:
- Session ID, current query

Output:
- Context data for InputPacket

Dependencies:
- TASK 10.1 (MemoryDB)
- TASK 3.4 (ContextAssembler integration)

Validation:
```bash
python -c "from src.memory.retriever import ContextRetriever; cr = ContextRetriever(); print('ContextRetriever created')"
```

Artifact: `src/memory/retriever.py`

---

**TASK 10.3 — Memory tests**

Location:
- `tests/test_memory.py`

Purpose:
- Test memory storage and retrieval

Steps:
1. Create `tests/test_memory.py`
2. Test: store turn data
3. Test: retrieve recent turns
4. Test: search long-term memory
5. Test: context retriever returns relevant data
6. Test: cold start (no memory available)

Input:
- pytest run

Output:
- All tests pass

Dependencies:
- TASK 10.1, 10.2

Validation:
```bash
pytest tests/test_memory.py -v
```

Artifact: `tests/test_memory.py`

---

## Phase 11 — Debug System

```
phase_id: 11
title: "Debug System"
priority: "P0"
status: "not_started"
progress_percent: 0
done_tasks: 0
total_tasks: 4
blocker: "Phase 10 must complete"
next_action: "Start TASK 11.1"
last_updated: "-"
validation_status: "not_started"
```

### Objective

Implement comprehensive debug and trace system.

### Tasks

**TASK 11.1 — Debug logger**

Location:
- `src/core/debug/logger.py`

Purpose:
- Enhanced logging with debug modes from README

Steps:
1. Create `src/core/debug/` directory
2. Create `src/core/debug/logger.py`
3. Define `DebugLogger` class
4. Implement debug modes: OFF, BASIC, TRACE, RAW
5. BASIC: log key decisions
6. TRACE: full step trace
7. RAW: LLM input/output shown
8. Integrate with Loguru from TASK 1.2

Input:
- Debug mode, log data

Output:
- Formatted log output based on mode

Dependencies:
- TASK 1.2 (logging setup)

Validation:
```bash
python app/main.py --debug --trace
# Verify full step trace output
```

Artifact: `src/core/debug/logger.py`

---

**TASK 11.2 — Replay system**

Location:
- `src/core/debug/replay.py`

Purpose:
- Implement /replay command to show complete turn trace

Steps:
1. Create `src/core/debug/replay.py`
2. Define `ReplaySystem` class
3. Implement `replay(turn_id)` method
4. Show all state transitions
5. Show raw LLM input/output
6. Show parsed decisions
7. Show tool calls with arguments
8. Show tool results
9. Read from event log or memory

Input:
- turn_id

Output:
- Complete turn trace display

Dependencies:
- TASK 11.1 (debug logger for event storage)

Validation:
```bash
# In chat: /replay <turn_id>
# Verify complete trace shown
```

Artifact: `src/core/debug/replay.py`

---

**TASK 11.3 — Event tracing**

Location:
- `src/core/debug/trace.py`

Purpose:
- Trace all events during execution for debugging

Steps:
1. Create `src/core/debug/trace.py`
2. Define `EventTracer` class
3. Subscribe to all events from EventBus (TASK 3.9)
4. Record full event data with timestamps
5. Store trace for replay system
6. Implement trace export (JSON)

Input:
- Events from EventBus

Output:
- Stored trace data

Dependencies:
- TASK 3.9 (EventBus)
- TASK 11.2 (replay system)

Validation:
```bash
python -c "from src.core.debug.trace import EventTracer; et = EventTracer(); print('EventTracer created')"
```

Artifact: `src/core/debug/trace.py`

---

**TASK 11.4 — Debug tests**

Location:
- `tests/test_debug.py`

Purpose:
- Test debug system functionality

Steps:
1. Create `tests/test_debug.py`
2. Test: debug modes filter output correctly
3. Test: replay shows complete trace
4. Test: event tracing captures all events
5. Test: RAW mode shows LLM input/output

Input:
- pytest run

Output:
- All tests pass

Dependencies:
- TASK 11.1 through 11.3

Validation:
```bash
pytest tests/test_debug.py -v
```

Artifact: `tests/test_debug.py`

---

## Phase 12 — Web Automation & Browser

```
phase_id: 12
title: "Web Automation & Browser"
priority: "P2"
status: "not_started"
progress_percent: 0
done_tasks: 0
total_tasks: 3
blocker: "Phase 11 must complete"
next_action: "Start TASK 12.1"
last_updated: "-"
validation_status: "not_started"
```

### Objective

Implement web automation capabilities using Playwright.

### Tasks

**TASK 12.1 — Browser capability**

Location:
- `src/capabilities/web_automation/browser.py`

Purpose:
- Implement browser automation capability with Playwright

Steps:
1. Create `src/capabilities/web_automation/` directory
2. Create `src/capabilities/web_automation/browser.py`
3. Define `BrowserCapability` inheriting BaseCapability
4. Implement `execute(args)` with actions: navigate, click, type, screenshot, extract_text
5. Use Playwright for browser control
6. Launch separate browser process (+500MB VRAM, +2GB RAM)
7. Handle page load, waits, timeouts
8. Return ToolResult with action result

Input:
- args: {action: str, url: str, selector: str, text: str}

Output:
- ToolResult with action result or page data

Dependencies:
- TASK 6.1 (BaseCapability)
- Optional: Hardware check for resource usage

Validation:
```bash
python -c "from src.capabilities.web_automation.browser import BrowserCapability; bc = BrowserCapability(); print(bc.execute({'action': 'navigate', 'url': 'https://example.com'}))"
```

Artifact: `src/capabilities/web_automation/browser.py`

---

**TASK 12.2 — Web session manager**

Location:
- `src/capabilities/web_automation/session.py`

Purpose:
- Manage browser sessions and cookies

Steps:
1. Create `src/capabilities/web_automation/session.py`
2. Define `WebSessionManager` class
3. Implement `create_session()` method
4. Implement `close_session(session_id)`
5. Manage cookies, localStorage
6. Handle multiple sessions
7. Integrate with BrowserCapability

Input:
- Session creation/closure requests

Output:
- Session handle

Dependencies:
- TASK 12.1 (BrowserCapability)

Validation:
```bash
python -c "from src.capabilities.web_automation.session import WebSessionManager; wsm = WebSessionManager(); print('WebSessionManager created')"
```

Artifact: `src/capabilities/web_automation/session.py`

---

**TASK 12.3 — Web automation tests**

Location:
- `tests/test_web_automation.py`

Purpose:
- Test web automation capabilities

Steps:
1. Create `tests/test_web_automation.py`
2. Test: browser navigation
3. Test: click elements
4. Test: type text
5. Test: screenshot capture
6. Test: text extraction
7. Test: session management

Input:
- pytest run

Output:
- All tests pass

Dependencies:
- TASK 12.1, 12.2

Validation:
```bash
pytest tests/test_web_automation.py -v
```

Artifact: `tests/test_web_automation.py`

---

## Phase 13 — Google APIs

```
phase_id: 13
title: "Google APIs"
priority: "P2"
status: "not_started"
progress_percent: 0
done_tasks: 0
total_tasks: 4
blocker: "Phase 12 must complete"
next_action: "Start TASK 13.1"
last_updated: "-"
validation_status: "not_started"
```

### Objective

Implement Google API integrations as services.

### Tasks

**TASK 13.1 — Google Auth service**

Location:
- `src/services/google/auth.py`

Purpose:
- Handle OAuth2 authentication for Google APIs

Steps:
1. Create `src/services/google/` directory
2. Create `src/services/google/auth.py`
3. Define `GoogleAuth` class
4. Implement `authenticate(credentials_path)` method
5. Handle OAuth2 flow with refresh tokens
6. Store tokens securely
7. Implement `get_credentials()` for API calls

Input:
- Credentials path or token

Output:
- Authenticated credentials

Dependencies:
- Google API client library

Validation:
```bash
python -c "from src.services.google.auth import GoogleAuth; ga = GoogleAuth(); print('GoogleAuth created')"
```

Artifact: `src/services/google/auth.py`

---

**TASK 13.2 — Google Calendar service**

Location:
- `src/services/google/calendar.py`

Purpose:
- Integrate with Google Calendar API

Steps:
1. Create `src/services/google/calendar.py`
2. Define `GoogleCalendar` class
3. Implement `list_events(start, end)` method
4. Implement `create_event(summary, start, end, description)`
5. Implement `delete_event(event_id)`
6. Use credentials from GoogleAuth
7. Return ToolResult-compatible data

Input:
- Calendar query or event data

Output:
- Calendar data or operation result

Dependencies:
- TASK 13.1 (GoogleAuth)

Validation:
```bash
python -c "from src.services.google.calendar import GoogleCalendar; gc = GoogleCalendar(); print('GoogleCalendar created')"
```

Artifact: `src/services/google/calendar.py`

---

**TASK 13.3 — Gmail service**

Location:
- `src/services/google/gmail.py`

Purpose:
- Integrate with Gmail API

Steps:
1. Create `src/services/google/gmail.py`
2. Define `GmailService` class
3. Implement `list_messages(query, max_results)`
4. Implement `get_message(message_id)`
5. Implement `send_message(to, subject, body)`
6. Use credentials from GoogleAuth
7. Return ToolResult-compatible data

Input:
- Gmail query or message data

Output:
- Message data or send result

Dependencies:
- TASK 13.1 (GoogleAuth)

Validation:
```bash
python -c "from src.services.google.gmail import GmailService; gs = GmailService(); print('GmailService created')"
```

Artifact: `src/services/google/gmail.py`

---

**TASK 13.4 — Google Drive service**

Location:
- `src/services/google/drive.py`

Purpose:
- Integrate with Google Drive API

Steps:
1. Create `src/services/google/drive.py`
2. Define `GoogleDrive` class
3. Implement `list_files(query)`
4. Implement `download_file(file_id, destination)`
5. Implement `upload_file(name, content, mime_type)`
6. Use credentials from GoogleAuth
7. Return ToolResult-compatible data

Input:
- Drive query or file data

Output:
- File list or operation result

Dependencies:
- TASK 13.1 (GoogleAuth)

Validation:
```bash
python -c "from src.services.google.drive import GoogleDrive; gd = GoogleDrive(); print('GoogleDrive created')"
```

Artifact: `src/services/google/drive.py`

---

## Phase 14 — CLI Interface

```
phase_id: 14
title: "CLI Interface"
priority: "P2"
status: "not_started"
progress_percent: 0
done_tasks: 0
total_tasks: 2
blocker: "Phase 13 must complete"
next_action: "Start TASK 14.1"
last_updated: "-"
validation_status: "not_started"
```

### Objective

Implement CLI interface for user interaction.

### Tasks

**TASK 14.1 — CLI chat loop**

Location:
- `src/interfaces/cli/chat.py`

Purpose:
- Implement main CLI chat loop

Steps:
1. Expand `src/interfaces/cli/` directory
2. Create `src/interfaces/cli/chat.py`
3. Define `CLIChat` class
4. Implement `start()` method with input loop
5. Display prompts and responses
6. Handle special commands: /quit, /mode, /replay
7. Wire to `run_turn()` from runtime loop
8. Print FinalResponse text to terminal

Input:
- Terminal user input

Output:
- Displayed responses and results

Dependencies:
- TASK 3.8 (runtime loop)
- TASK 7.3 (CLI mode toggle)

Validation:
```bash
python app/main.py --interface cli
# Type: "hello" → response
# Type: "/mode SAFE" → mode changed
# Type: "/quit" → exit
```

Artifact: `src/interfaces/cli/chat.py`

---

**TASK 14.2 — CLI formatting**

Location:
- `src/interfaces/cli/formatting.py`

Purpose:
- Format terminal output for readability

Steps:
1. Create `src/interfaces/cli/formatting.py`
2. Define `CLIFormatter` class
3. Implement `format_response(FinalResponse)` method
4. Add colors with colorama
5. Format tool results
6. Format error messages
7. Support Arabic text display

Input:
- FinalResponse or other data

Output:
- Formatted string for terminal

Dependencies:
- None (standalone formatting)

Validation:
```bash
python -c "from src.interfaces.cli.formatting import CLIFormatter; cf = CLIFormatter(); print(cf.format_response(...))"
```

Artifact: `src/interfaces/cli/formatting.py`

---

## Phase 15 — Web UI

```
phase_id: 15
title: "Web UI"
priority: "P2"
status: "not_started"
progress_percent: 0
done_tasks: 0
total_tasks: 3
blocker: "Phase 14 must complete"
next_action: "Start TASK 15.1"
last_updated: "-"
validation_status: "not_started"
```

### Objective

Implement Web UI interface using FastAPI and WebSockets.

### Tasks

**TASK 15.1 — Web UI backend**

Location:
- `src/interfaces/web/app.py`

Purpose:
- Implement FastAPI backend for Web UI

Steps:
1. Create `src/interfaces/web/` directory
2. Create `src/interfaces/web/app.py`
3. Define FastAPI app
4. Implement REST endpoints: POST /chat, GET /history
5. Implement WebSocket endpoint: /ws for real-time communication
6. Wire to `run_turn()` from runtime loop
7. Handle FinalResponse and stream updates

Input:
- HTTP requests or WebSocket messages

Output:
- JSON responses or WebSocket messages

Dependencies:
- TASK 3.8 (runtime loop)

Validation:
```bash
# Start: python app/main.py --interface web
# Open: http://localhost:8000
# Test chat via UI
```

Artifact: `src/interfaces/web/app.py`

---

**TASK 15.2 — Web UI frontend**

Location:
- `src/interfaces/web/static/index.html`

Purpose:
- Create simple web frontend for chat

Steps:
1. Create `src/interfaces/web/static/` directory
2. Create `index.html` with chat interface
3. Implement WebSocket client for real-time updates
4. Add message display (user + Jarvis)
5. Add input box and send button
6. Support Arabic text input/display
7. Add mode toggle button

Input:
- User messages via UI

Output:
- Displayed chat interface

Dependencies:
- TASK 15.1 (Web UI backend)

Validation:
- Open http://localhost:8000, send messages, verify responses

Artifact: `src/interfaces/web/static/index.html`

---

**TASK 15.3 — Web UI tests**

Location:
- `tests/test_web_ui.py`

Purpose:
- Test Web UI functionality

Steps:
1. Create `tests/test_web_ui.py`
2. Test: FastAPI endpoints respond correctly
3. Test: WebSocket connection and messaging
4. Test: mode toggle via API
5. Use httpx for testing

Input:
- pytest run

Output:
- All tests pass

Dependencies:
- TASK 15.1, 15.2

Validation:
```bash
pytest tests/test_web_ui.py -v
```

Artifact: `tests/test_web_ui.py`

---

## Phase 16 — Voice Pipeline

```
phase_id: 16
title: "Voice Pipeline"
priority: "P3"
status: "not_started"
progress_percent: 0
done_tasks: 0
total_tasks: 4
blocker: "Phase 15 must complete"
next_action: "Start TASK 16.1"
last_updated: "-"
validation_status: "not_started"
```

### Objective

Implement voice input (STT) and output (TTS) capabilities.

### Tasks

**TASK 16.1 — STT capability (Whisper)**

Location:
- `src/capabilities/voice/stt.py`

Purpose:
- Implement Speech-to-Text using Whisper

Steps:
1. Create `src/capabilities/voice/` directory
2. Create `src/capabilities/voice/stt.py`
3. Define `STTCapability` inheriting BaseCapability
4. Implement `execute(args)` with args: audio_path or audio_data
5. Use Whisper for transcription (+500MB VRAM, +1GB RAM)
6. Support multiple languages (English, Arabic)
7. Return ToolResult with transcribed text

Input:
- args: {audio_path: str} or {audio_data: bytes}

Output:
- ToolResult with transcribed text

Dependencies:
- TASK 6.1 (BaseCapability)
- Optional: Hardware check for resource usage

Validation:
```bash
python -c "from src.capabilities.voice.stt import STTCapability; stt = STTCapability(); print('STTCapability created')"
```

Artifact: `src/capabilities/voice/stt.py`

---

**TASK 16.2 — TTS capability (Piper)**

Location:
- `src/capabilities/voice/tts.py`

Purpose:
- Implement Text-to-Speech using Piper

Steps:
1. Create `src/capabilities/voice/tts.py`
2. Define `TTSCapability` inheriting BaseCapability
3. Implement `execute(args)` with args: text, voice (optional)
4. Use Piper for synthesis
5. Support multiple languages (English, Arabic)
6. Return ToolResult with audio file path

Input:
- args: {text: str, voice: str}

Output:
- ToolResult with audio file path

Dependencies:
- TASK 6.1 (BaseCapability)

Validation:
```bash
python -c "from src.capabilities.voice.tts import TTSCapability; tts = TTSCapability(); print('TTSCapability created')"
```

Artifact: `src/capabilities/voice/tts.py`

---

**TASK 16.3 — Wake word detection**

Location:
- `src/capabilities/voice/wake_word.py`

Purpose:
- Detect wake word to activate voice input

Steps:
1. Create `src/capabilities/voice/wake_word.py`
2. Define `WakeWordDetector` class
3. Implement `listen_for_wake_word(word)` method
4. Use speech_recognition library
5. Trigger callback when wake word detected
6. Integrate with STT capability

Input:
- Wake word string

Output:
- Callback when wake word detected

Dependencies:
- TASK 16.1 (STT capability)

Validation:
```bash
python -c "from src.capabilities.voice.wake_word import WakeWordDetector; wwd = WakeWordDetector(); print('WakeWordDetector created')"
```

Artifact: `src/capabilities/voice/wake_word.py`

---

**TASK 16.4 — Voice pipeline tests**

Location:
- `tests/test_voice.py`

Purpose:
- Test voice pipeline components

Steps:
1. Create `tests/test_voice.py`
2. Test: STT transcription
3. Test: TTS synthesis
4. Test: wake word detection (mock)
5. Test: integration with runtime loop

Input:
- pytest run

Output:
- All tests pass

Dependencies:
- TASK 16.1 through 16.3

Validation:
```bash
pytest tests/test_voice.py -v
```

Artifact: `tests/test_voice.py`

---

## Phase 17 — Vision + Image

```
phase_id: 17
title: "Vision + Image"
priority: "P3"
status: "not_started"
progress_percent: 0
done_tasks: 0
total_tasks: 2
blocker: "Phase 16 must complete"
next_action: "Start TASK 17.1"
last_updated: "-"
validation_status: "not_started"
```

### Objective

Implement vision capabilities and image generation.

### Tasks

**TASK 17.1 — Vision capability (llava:7b)**

Location:
- `src/capabilities/vision/vision.py`

Purpose:
- Implement image understanding using llava:7b model

Steps:
1. Create `src/capabilities/vision/` directory
2. Create `src/capabilities/vision/vision.py`
3. Define `VisionCapability` inheriting BaseCapability
4. Implement `execute(args)` with args: image_path, prompt
5. Use llava:7b through Ollama (+4.5GB VRAM)
6. Return image description or answer to prompt
7. Return ToolResult with vision output

Input:
- args: {image_path: str, prompt: str}

Output:
- ToolResult with vision analysis

Dependencies:
- TASK 6.1 (BaseCapability)
- TASK 1.5 (LLM engine for model calling)

Validation:
```bash
python -c "from src.capabilities.vision.vision import VisionCapability; v = VisionCapability(); print(v.execute({'image_path': 'test.jpg', 'prompt': 'describe'}))"
```

Artifact: `src/capabilities/vision/vision.py`

---

**TASK 17.2 — Image generation capability (Stable Diffusion)**

Location:
- `src/capabilities/vision/image_gen.py`

Purpose:
- Generate images using Stable Diffusion

Steps:
1. Create `src/capabilities/vision/image_gen.py`
2. Define `ImageGenCapability` inheriting BaseCapability
3. Implement `execute(args)` with args: prompt, size, style
4. Use Stable Diffusion (+2GB VRAM, +2GB RAM)
5. CPU fallback possible
6. Return ToolResult with generated image path

Input:
- args: {prompt: str, size: str, style: str}

Output:
- ToolResult with image file path

Dependencies:
- TASK 6.1 (BaseCapability)
- Optional: Hardware check for resource usage

Validation:
```bash
python -c "from src.capabilities.vision.image_gen import ImageGenCapability; ig = ImageGenCapability(); print('ImageGenCapability created')"
```

Artifact: `src/capabilities/vision/image_gen.py`

---

## Phase 18 — QA + Production

```
phase_id: 18
title: "QA + Production"
priority: "P0"
status: "not_started"
progress_percent: 0
done_tasks: 0
total_tasks: 5
blocker: "Phase 17 must complete"
next_action: "Start TASK 18.1"
last_updated: "-"
validation_status: "not_started"
```

### Objective

Final QA, testing, and production readiness.

### Tasks

**TASK 18.1 — Integration tests**

Location:
- `tests/test_integration.py`

Purpose:
- End-to-end integration tests for full system

Steps:
1. Create `tests/test_integration.py`
2. Test: Full flow from input to FinalResponse
3. Test: All capabilities integrated and working
4. Test: All interfaces (CLI, Web UI) functional
5. Test: Memory persists across turns
6. Test: Safety modes enforced throughout

Input:
- pytest run

Output:
- All integration tests pass

Dependencies:
- All previous phases

Validation:
```bash
pytest tests/test_integration.py -v
```

Artifact: `tests/test_integration.py`

---

**TASK 18.2 — Performance tests**

Location:
- `tests/test_performance.py`

Purpose:
- Test system performance within hardware constraints

Steps:
1. Create `tests/test_performance.py`
2. Test: Response time < 5s for simple queries
3. Test: VRAM usage stays within 6GB
4. Test: RAM usage stays within 16GB
5. Test: Concurrent request handling

Input:
- pytest run with performance benchmarks

Output:
- All performance tests pass

Dependencies:
- TASK 18.1 (integration tests)

Validation:
```bash
pytest tests/test_performance.py -v
```

Artifact: `tests/test_performance.py`

---

**TASK 18.3 — Arabic language tests**

Location:
- `tests/test_arabic.py`

Purpose:
- Verify full Arabic language support

Steps:
1. Create `tests/test_arabic.py`
2. Test: Arabic input classification
3. Test: Arabic responses
4. Test: Arabic UI display
5. Test: Arabic voice (STT/TTS)
6. Test: Arabic vision prompts

Input:
- pytest run

Output:
- All Arabic tests pass

Dependencies:
- All capability phases

Validation:
```bash
pytest tests/test_arabic.py -v
```

Artifact: `tests/test_arabic.py`

---

**TASK 18.4 — Production configuration**

Location:
- `config/production.yaml`

Purpose:
- Create production-ready configuration

Steps:
1. Create `config/production.yaml`
2. Set production values: mode=BALANCED, logging level=WARNING
3. Disable debug modes
4. Set appropriate timeouts
5. Configure fallback models
6. Document production deployment steps

Input:
- None (configuration file)

Output:
- Production config file

Dependencies:
- TASK 1.1 (config system)

Validation:
```bash
python -c "from src.core.config import load_config; s = load_config('config/production.yaml'); print(s.execution_mode)"
```

Artifact: `config/production.yaml`

---

**TASK 18.5 — VERSION and release**

Location:
- `VERSION`
- `RELEASE_NOTES.md`

Purpose:
- Finalize version and release documentation

Steps:
1. Create `VERSION` file with "1.0"
2. Create `RELEASE_NOTES.md` with:
   - Features implemented
   - Known limitations
   - Hardware requirements
   - How to run
3. Final code cleanup
4. Remove debug prints
5. Ensure all tests pass

Input:
- None (release artifacts)

Output:
- VERSION file, RELEASE_NOTES.md

Dependencies:
- All previous tasks

Validation:
```bash
cat VERSION
pytest tests/ -v  # All tests pass
```

Artifacts: `VERSION`, `RELEASE_NOTES.md`

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
last_updated: "2026-04-28"
validation_status: "not_started"
```

### Objective

Fix execution gaps to ensure stable, deterministic, fully controlled behavior.

### Tasks

**TASK VALIDATOR — Capability Validator**

Location:
- `src/capabilities/validator.py` (expand TASK 6.5)

Purpose:
- Enhance validator with DecisionOutput alignment checks

Steps:
1. Further expand `src/capabilities/validator.py`
2. Implement `validate_decision_alignment(tool_name, decision)` method
3. Verify tool matches declared intent
4. Validate schema validity against capability manifest
5. Validate risk level matches capability manifest
6. Validate tool availability in registry
7. Return: approved tool or rejection with reason

Input:
- Tool name, DecisionOutput

Output:
- Validation result with approval/rejection

Dependencies:
- TASK 6.5 (base validator)

Validation:
```bash
python -c "from src.capabilities.validator import SchemaValidator; v = SchemaValidator(); print('Enhanced validator created')"
```

Artifact: `src/capabilities/validator.py`

---

**TASK LOGGING — Enhanced Logging System**

Location:
- `src/core/logging.py`

Purpose:
- Implement comprehensive logging for all runtime events

Steps:
1. Create `src/core/logging.py`
2. Define `RuntimeLogger` class
3. Implement `log_decision(decision)` - log decision results with scoring
4. Implement `log_model_selected(model, score)` - log selected model with reason
5. Implement `log_tool_call(name, args)` - log tool calls
6. Implement `log_tool_result(result)` - log tool results
7. Implement `log_failure(phase, error)` - log all failures
8. Implement `log_retry(attempt, reason)` - log retries
9. Implement `log_escalation(level, action)` - log escalations
10. Ensure all events include: timestamp, level, event, session_id, turn_id, phase, data

Input:
- Runtime events

Output:
- Structured log entries

Dependencies:
- TASK 1.2 (base logging setup)

Validation:
```bash
python app/main.py --debug
# Verify all runtime events logged
```

Artifact: `src/core/logging.py`

---

**TASK FAILURE_H — Failure Handling System**

Location:
- `src/core/failure.py`

Purpose:
- Centralized failure handling for all failure modes

Steps:
1. Create `src/core/failure.py`
2. Define `FailureHandler` class
3. Implement `handle_model_timeout(model)` - retry once, then swap to fallback
4. Implement `handle_invalid_output(raw_text)` - force defaults, retry with correction
5. Implement `handle_tool_failure(tool, error)` - log, add context, allow different tool
6. Implement `handle_loop_detected(tool, history)` - block, return warning
7. Ensure runtime never crashes
8. Use escalation chain (TASK 4.4) for fallbacks

Input:
- Failure type and details

Output:
- Recovery action or error response

Dependencies:
- TASK 4.4 (escalation chain)
- TASK 9.5 (graceful degradation)

Validation:
```bash
python -c "from src.core.failure import FailureHandler; fh = FailureHandler(); print('FailureHandler created')"
```

Artifact: `src/core/failure.py`

---

**TASK IDENTITY — Identity Verification**

Location:
- `src/core/context/verify.py`

Purpose:
- Verify identity block in all LLM calls

Steps:
1. Create `src/core/context/verify.py`
2. Define `IdentityVerifier` class
3. Implement `verify_llm_call(prompt)` - check identity block present
4. Implement `verify_all_calls()` - scan codebase for LLM calls
5. Verify prompt has Jarvis identity from YAML
6. Verify mode enforcement in prompt
7. Log verification results

Input:
- LLM prompt or codebase

Output:
- Verification result

Dependencies:
- TASK 5.1 (identity YAML)
- TASK 5.3 (prompt builder)

Validation:
```bash
python -c "from src.core.context.verify import IdentityVerifier; iv = IdentityVerifier(); print('IdentityVerifier created')"
```

Artifact: `src/core/context/verify.py`

---

**TASK EXEC_LIMITS — Execution Limits Enforcement**

Location:
- `src/core/runtime/limits.py` (expand TASK 3.3)

Purpose:
- Enhance limits enforcement in runtime loop

Steps:
1. Further expand `src/core/runtime/limits.py`
2. Implement `enforce_max_iterations(current)` decorator
3. Implement `enforce_max_tool_calls(current)` decorator
4. Implement `enforce_step_timeout(phase)` decorator
5. Integrate with runtime loop (TASK 3.8)
6. Force exit with safe response when limits exceeded

Input:
- Runtime state

Output:
- Limit check result

Dependencies:
- TASK 3.3 (base limits)
- TASK 3.8 (runtime loop)

Validation:
```bash
# Run system, verify loop stops after max_iterations
# Verify tool calls stop after max_tool_calls
```

Artifact: `src/core/runtime/limits.py`

---

**TASK DECISION_V — Decision Validation (Dynamic Scoring)**

Location:
- `tests/test_decision_dynamic.py`

Purpose:
- Verify decision system uses dynamic scoring (not hardcoded)

Steps:
1. Create `tests/test_decision_dynamic.py`
2. Test: Decision output changes when inputs slightly vary
3. Test: Varying complexity produces different models
4. Test: Varying modality produces different models
5. Test: Varying cost constraints changes selection
6. Test: Multiple models can win based on input
7. Test: Scoring is explained in logs (verify log output)

Input:
- pytest run

Output:
- All dynamic scoring tests pass

Dependencies:
- TASK 4.1 through 4.5 (decision system)

Validation:
```bash
pytest tests/test_decision_dynamic.py -v
```

Artifact: `tests/test_decision_dynamic.py`

---

**TASK DECISION_E — Decision Enforcement**

Location:
- `src/core/runtime/validate_decision.py`

Purpose:
- Enforce decision validation rules from README

Steps:
1. Create `src/core/runtime/validate_decision.py`
2. Define `DecisionEnforcer` class
3. Implement `validate(decision)` method
4. Verify DecisionOutput includes score_breakdown
5. Verify candidate list exists and has multiple entries
6. Verify final score exists
7. Reject invalid decisions (no score_breakdown → reject)
8. Verify decision.fail_safe triggers after 3 failures
9. Integrate with runtime loop

Input:
- DecisionOutput

Output:
- Validation result (valid/invalid)

Dependencies:
- TASK 2.2 (DecisionOutput)
- TASK 3.5 (decision function)

Validation:
```bash
python -c "from src.core.runtime.validate_decision import DecisionEnforcer; de = DecisionEnforcer(); print('DecisionEnforcer created')"
```

Artifact: `src/core/runtime/validate_decision.py`

---

**TASK FALLBACK — Tiered Fallback System**

Location:
- `src/core/runtime/fallback.py`

Purpose:
- Implement tiered fallback system from README

Steps:
1. Create `src/core/runtime/fallback.py`
2. Define `FallbackSystem` class
3. Implement Tier 1: qwen2.5:7b fallback (reasoning, planning)
4. Implement Tier 2: gemma3:4b fallback (simple responses, complete failure)
5. Implement `attempt_fallback(tier)` method
6. Verify Tier 1 attempted before Tier 2
7. Verify fallback chain works end-to-end
8. Log all fallback activations

Input:
- Fallback tier or trigger event

Output:
- Fallback model or response

Dependencies:
- TASK 1.5 (LLM engine for model swapping)
- TASK 4.4 (escalation chain)

Validation:
```bash
python -c "from src.core.runtime.fallback import FallbackSystem; fs = FallbackSystem(); print('FallbackSystem created')"
```

Artifact: `src/core/runtime/fallback.py`

---

**TASK RETRY — Decision Retry Logic**

Location:
- `src/core/runtime/retry.py`

Purpose:
- Implement decision retry with weight adjustment

Steps:
1. Create `src/core/runtime/retry.py`
2. Define `RetryManager` class
3. Implement `max_decision_retries = 3` enforcement
4. Implement `retry_with_adjustment(attempt_number, weights)` method
5. Adjust scoring weights slightly per retry
6. Or reduce constraints on subsequent retries
7. Verify fallback triggered after retries exhausted
8. Log all retry attempts

Input:
- Retry attempt number, current weights

Output:
- Adjusted weights or fallback trigger

Dependencies:
- TASK 3.5 (decision function)
- TASK 4.4 (escalation chain)

Validation:
```bash
python -c "from src.core.runtime.retry import RetryManager; rm = RetryManager(); print('RetryManager created')"
```

Artifact: `src/core/runtime/retry.py`

---

**TASK RESPONSE_Q — Response Quality Guard**

Location:
- `src/core/runtime/response_guard.py`

Purpose:
- Enforce response quality standards

Steps:
1. Create `src/core/runtime/response_guard.py`
2. Define `ResponseGuard` class
3. Implement `validate(response, decision)` method
4. Apply ONLY on:
   - Long responses (>500 tokens)
   - Complex tasks (reasoning, planning, research)
   - Fallback outputs
5. Validate completeness (answer not truncated)
6. Validate coherence (logical consistency)
7. Validate relevance (addresses input)
8. If validation fails → retry with stronger model
9. Log quality checks

Input:
- FinalResponse or LLMOutput, DecisionOutput

Output:
- Quality validation result with retry flag

Dependencies:
- TASK 3.7 (evaluator)
- TASK 1.5 (LLM engine for retry)

Validation:
```bash
python -c "from src.core.runtime.response_guard import ResponseGuard; rg = ResponseGuard(); print('ResponseGuard created')"
```

Artifact: `src/core/runtime/response_guard.py`

---

**TASK DEGRADE — Degradation Flag**

Location:
- `src/core/runtime/degradation.py` (expand TASK 9.5)

Purpose:
- Track and log system degradation state

Steps:
1. Further expand `src/core/runtime/degradation.py`
2. Implement `track_degradation(event_type)` method
3. Track: fallback activation, retries exceeded, weak model used
4. Set `system_state: degraded` flag when any occur
5. Log `system_state: degraded` with event details
6. Integrate with runtime loop
7. Reset degradation flag on successful turn

Input:
- Degradation event type

Output:
- Degradation flag state

Dependencies:
- TASK 9.5 (base degradation handler)

Validation:
```bash
python app/main.py --debug
# Trigger fallback, verify "system_state: degraded" logged
```

Artifact: `src/core/runtime/degradation.py`

---

### Definition of Done

1. No hardcoded routing
2. No direct tool execution outside capability system
3. All actions validated
4. All steps logged
5. All failures handled
6. System deterministic

---

## Summary

Total tasks: 95 (including expanded sub-tasks and execution gaps)
All tasks mapped to STRUCTURE.md layers
All tasks decomposed into atomic steps
All terminology normalized (capabilities not skills/tools)
All paths aligned with STRUCTURE.md

---

**End of Execution Plan**
