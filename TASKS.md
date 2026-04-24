# JARVIS — Execution Plan

## Execution Rules

**STRICT RULES - No exceptions, no phase skipping:**

1. **No skipping phases** — Phase 0 must be completed before Phase 1, and so on
2. **No adding features outside scope** — Each phase must stay within its defined scope
3. **Each phase must produce a working system** — The system must be runnable after each phase
4. **No breaking architecture** — Data contracts must be maintained across all phases
5. **Progressive implementation** — Build incrementally, never rewrite previous work
6. **Test after each task** — Verify success criteria before proceeding

---

## Progress Tracking

| Phase | Name | Status |
|-------|------|--------|
| 0 | First Working System | [ ] |
| 1 | Foundation | [ ] |
| 2 | Execution Contract Implementation | [ ] |
| 3 | Runtime Loop | [ ] |
| 4 | Decision System | [ ] |
| 5 | Prompt Builder | [ ] |
| 6 | Tool System | [ ] |
| 7 | Safety Modes | [ ] |
| 8 | System Control Skills | [ ] |
| 9 | Browser & Web Skills | [ ] |
| 10 | Google APIs | [ ] |
| 11 | Context + Memory | [ ] |
| 12 | Agents | [ ] |
| 13 | CLI Interface | [ ] |
| 14 | Web UI | [ ] |
| 15 | Voice Pipeline | [ ] |
| 16 | Vision + Image Generation | [ ] |
| 17 | Telegram + GUI | [ ] |
| 18 | QA + Security | [ ] |

---

## Phase 0 — First Working System

> **MANDATORY FIRST - No other phase may be started until Phase 0 is complete and verified**

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
- Safety enforcement (Phase 7+)
- Interfaces (CLI, Web, Voice)

### Dependencies

None — this is the starting phase.

### Tasks

- [ ] TASK 0.1 — Connect to Ollama and get a response
  - Create `src/models/llm/engine.py`
  - Implement `chat(message, model)` function
  - Call Ollama Python client
  - Return response content as string

- [ ] TASK 0.2 — Classify a command and return structured output
  - Create `src/core/decision/classifier.py`
  - Implement `classify(message)` function
  - Use gemma3:4b with JSON-forcing system prompt
  - Handle malformed JSON with retry (max 2)
  - Return safe fallback dict on all failures

- [ ] TASK 0.3 — Execute an application by name
  - Create `src/skills/system/apps.py`
  - Implement `open_app(name)` function
  - Cross-platform search (PATH, program directories)
  - Return success/error dict without raising

- [ ] TASK 0.4 — Wire classifier to tool: text input → action
  - Create `app/jarvis_slice.py`
  - Implement `run(user_input)` function
  - Connect: input → classify → tool/LLM → output
  - Loop on terminal input until "quit"

- [ ] TASK 0.5 — Verify Arabic input
  - Test Arabic commands produce same behavior as English
  - Add Arabic examples to classifier if needed

### Definition of Done

**Phase 0 is complete when:**
1. Running "hello" returns a non-empty text response
2. Running "open notepad" opens Notepad
3. Running Arabic equivalents produces identical behavior
4. "quit" exits cleanly

### Validation Steps

```bash
# Test 1: LLM response
python -c "from src.models.llm.engine import chat; print(chat('hello'))"

# Test 2: Tool execution
python -c "from src.skills.system.apps import open_app; print(open_app('notepad'))"

# Test 3: Full pipeline
python app/jarvis_slice.py
# Type: "open notepad" → should open Notepad
# Type: "what is AI?" → should return text answer
# Type: "quit" → should exit
```

### Failure Conditions

- Any exception reaches the terminal
- "open notepad" does not open Notepad
- "what is AI?" returns empty or error
- Arabic input produces different intent than English

### Artifacts

- `src/models/llm/engine.py`
- `src/core/decision/classifier.py`
- `src/skills/system/apps.py`
- `app/jarvis_slice.py`

---

## Phase 1 — Foundation

> **End state:** `python app/main.py --interface cli` runs without crashing, loads config, initializes logging, and prints "Jarvis ready."

### Objective

Establish the configuration system, logging infrastructure, and project structure required for all subsequent phases.

### Scope

- Settings YAML and Pydantic loader
- Logging setup with Loguru
- Package skeleton with all directories
- Model profiles YAML
- Environment variables
- User profile JSON storage
- Skills manifest YAML
- main.py entry point

### Out of Scope

- No runtime loop implementation
- No tool execution pipeline
- No memory backends
- No interfaces

### Dependencies

- Phase 0 (completed)

### Tasks

- [ ] TASK 1.1 — Settings YAML and Pydantic loader
  - Create `config/settings.example.yaml`
  - Create `config/settings.yaml`
  - Create `src/core/config.py` with Pydantic models
  - Implement `get_settings()` cached singleton
  - Implement `create_directories()` function

- [ ] TASK 1.2 — Logging setup
  - Create `src/core/logging_setup.py`
  - Configure Loguru with terminal and file sinks
  - 10 MB rotation, 7-day retention
  - Debug sink when debug=True

- [ ] TASK 1.3 — Package skeleton
  - Create `__init__.py` in all src/ subdirectories
  - All directories importable

- [ ] TASK 1.4 — Model capability profiles
  - Create `config/models.yaml`
  - Create `src/models/profiles.py`
  - Implement `get_model_profile(tag)` function

- [ ] TASK 1.5 — LLM engine with VRAM guard
  - Create `src/models/llm/engine.py` (enhanced from Phase 0)
  - Track active model
  - Implement `swap_to(model)`, `get_active_model()`, `unload_current_model()`

- [ ] TASK 1.6 — Environment variables
  - Create `.env.example`
  - Create `.env` (gitignored)
  - Call load_dotenv() in main.py

- [ ] TASK 1.7 — User profile
  - Create `src/core/memory/user_profile.py`
  - Implement `load_profile()`, `save_profile(updates)`, `get_profile_value(key, default)`

- [ ] TASK 1.8 — Skills manifest
  - Create `config/skills.yaml`
  - Declare all tools with risk_level

- [ ] TASK 1.9 — main.py entry point
  - Create `app/main.py`
  - Parse --interface and --debug flags
  - Execute boot flow steps 1-10

### Definition of Done

Phase 1 is complete when:
1. `python app/main.py --interface cli` executes all boot steps
2. "Jarvis ready" appears in log
3. Ctrl+C exits cleanly

### Validation Steps

```bash
python app/main.py --interface cli
# Should see: jarvis starting → directories created → logging init → jarvis ready
# Ctrl+C should exit without traceback
```

### Failure Conditions

- Boot sequence crashes
- "Jarvis ready" not printed
- Ctrl+C produces traceback

### Artifacts

- `config/settings.yaml`
- `config/models.yaml`
- `config/skills.yaml`
- `.env`
- `src/core/config.py`
- `src/core/logging_setup.py`
- `src/models/profiles.py`
- `src/models/llm/engine.py`
- `src/core/memory/user_profile.py`
- `app/main.py`

---

## Phase 2 — Execution Contract Implementation

> **End state:** All five contract types defined as Pydantic models and used across all phases.

### Objective

Define the strict data contracts that bind all components together.

### Scope

- InputPacket Pydantic model
- DecisionOutput Pydantic model
- LLMOutput Pydantic model with parser
- ToolResult Pydantic model
- FinalResponse Pydantic model

### Out of Scope

- Contract enforcement in runtime (Phase 3)
- Schema validation for tools (Phase 6)

### Dependencies

- Phase 1 (completed)

### Tasks

- [ ] TASK 2.1 — Define InputPacket
  - Create `src/core/context/bundle.py`
  - Define InputPacket with all fields
  - Define supporting types (Attachment, Message, UserProfile)

- [ ] TASK 2.2 — Define DecisionOutput
  - Create `src/core/decision/decision.py`
  - Define DecisionOutput with constrained fields

- [ ] TASK 2.3 — Define LLMOutput
  - Create `src/core/runtime/llm_output.py`
  - Define LLMOutput
  - Implement `parse_llm_output(raw, requires_tools)`

- [ ] TASK 2.4 — Define ToolResult
  - Create `src/core/tools/result.py`
  - Define ToolResult

- [ ] TASK 2.5 — Define FinalResponse
  - Create `src/core/runtime/final_response.py`
  - Define FinalResponse

- [ ] TASK 2.6 — Contract validation tests
  - Create `tests/test_contracts.py`
  - Test all models raise/accept correctly

### Definition of Done

All five contract types:
1. Instantiate with valid data without error
2. Raise Pydantic validation error on invalid data
3. Are imported and used by appropriate modules

### Validation Steps

```bash
python -c "
from src.core.context.bundle import InputPacket
from src.core.decision.decision import DecisionOutput
from src.core.runtime.llm_output import LLMOutput
from src.core.tools.result import ToolResult
from src.core.runtime.final_response import FinalResponse
# All instantiations should work
p = InputPacket(user_message='hello', session_id='s1')
d = DecisionOutput(intent='chat', complexity='low', mode='fast', model='gemma3:4b', requires_tools=False, requires_planning=False, confidence=0.9, risk_level='low')
print('All contracts valid')
"
```

### Failure Conditions

- Any contract type fails to instantiate
- Invalid data does not raise validation error

### Artifacts

- `src/core/context/bundle.py`
- `src/core/decision/decision.py`
- `src/core/runtime/llm_output.py`
- `src/core/tools/result.py`
- `src/core/runtime/final_response.py`
- `tests/test_contracts.py`

---

## Phase 3 — Runtime Loop

> **End state:** A complete turn executes: InputPacket assembled → decision made → LLM called → response or tool call returned → evaluator approves or escalates → FinalResponse returned.

### Objective

Implement the main execution loop that drives the entire system.

### Scope

- Context assembler
- Decision function
- Executor (LLM call)
- Evaluator
- Runtime loop
- EventBus

### Out of Scope

- Hardened classifier (Phase 4)
- Identity/prompt builder (Phase 5)
- Full tool pipeline (Phase 6)

### Dependencies

- Phase 2 (completed)

### Tasks

- [ ] TASK 3.1 — Context assembler
  - Create `src/core/context/assembler.py`
  - Implement `assemble_context(user_message, session_id, attachments)`

- [ ] TASK 3.2 — Decision function
  - Implement `decide(packet: InputPacket) → DecisionOutput`
  - Fast-path rules before LLM call
  - Call classifier.py from Phase 0

- [ ] TASK 3.3 — Executor (think step)
  - Create `src/core/runtime/executor.py`
  - Implement `execute_turn(decision, packet) → LLMOutput`
  - Call model, parse output

- [ ] TASK 3.4 — Evaluator
  - Create `src/core/runtime/evaluator.py`
  - Implement `evaluate(output, decision) → EvalResult`

- [ ] TASK 3.5 — Runtime loop
  - Create `src/core/runtime/loop.py`
  - Implement `run_turn(user_input, session_id, attachments)`
  - Implement loop with max_iterations
  - Handle tool calls and response approvals

- [ ] TASK 3.6 — EventBus
  - Create `src/core/events.py`
  - Implements publish-subscribe event system

### Definition of Done

```python
from src.core.runtime.loop import run_turn
response = run_turn("what is AI?", "s1")
# Returns FinalResponse with non-empty text
```

### Validation Steps

```bash
python -c "
from src.core.runtime.loop import run_turn
r = run_turn('what is AI?', 'test_session')
print(f'Response: {r.text[:50]}...')
print(f'Model: {r.model}')
"
```

### Failure Conditions

- run_turn raises exception
- Returns empty response
- Loop runs more than max_iterations times

### Artifacts

- `src/core/context/assembler.py`
- `src/core/decision/decision.py` (modified)
- `src/core/runtime/executor.py`
- `src/core/runtime/evaluator.py`
- `src/core/runtime/loop.py`
- `src/core/events.py`

---

## Phase 4 — Decision System

> **End state:** All intent types classified correctly. Correct model selected for each intent. Risk level populated on every DecisionOutput.

### Objective

Harden the decision system with robust classification, fast-path rules, risk levels, and escalation.

### Scope

- Robust classifier with JSON parsing
- Fast-path classification rules
- Risk level population from manifest
- Escalation chain
- Decision tests

### Out of Scope

- Identity prompt builder
- Tool validation

### Dependencies

- Phase 3 (completed)

### Tasks

- [ ] TASK 4.1 — Classifier with robust JSON parsing
  - Modify `src/core/decision/classifier.py`
  - Extract JSON from any position in response
  - Handle markdown code blocks
  - Retry with correction instructions
  - Return fallback on failure

- [ ] TASK 4.2 — Fast-path classification rules
  - Modify `src/core/decision/decision.py`
  - Implement fast-path: image → vision intent
  - Implement fast-path: short message + no action → fast chat
  - Log each fast-path decision

- [ ] TASK 4.3 — Risk level population
  - Modify `src/core/decision/decision.py`
  - Load skills.yaml at module level
  - Populate risk_level from manifest for tool_name
  - Default to "low" for no tool

- [ ] TASK 4.4 — Escalation chain
  - Create `src/core/runtime/escalation.py`
  - Define escalation: fast/gemma3:4b → normal/qwen3:8b → deep/qwen3:8b
  - Implement `get_next_escalation(current_mode, current_model)`

- [ ] TASK 4.5 — Decision system tests
  - Create `tests/test_decision.py`
  - Test all routing rules
  - Mock Ollama, test in isolation

### Definition of Done

1. All test inputs route correctly
2. Risk levels populated from manifest
3. Escalation chain returns correct next step

### Validation Steps

```bash
python -c "
from src.core.decision.decision import decide
from src.core.context.assembler import assemble_context
d = decide(assemble_context('open chrome', 's1'))
print(f'Intent: {d.intent}, Tool: {d.tool_name}, Risk: {d.risk_level}')
"
```

### Failure Conditions

- Classifier returns invalid dict
- Risk level missing on tool decision
- Escalation returns wrong step

### Artifacts

- `src/core/decision/classifier.py` (modified)
- `src/core/decision/decision.py` (modified)
- `src/core/runtime/escalation.py`
- `tests/test_decision.py`

---

## Phase 5 — Prompt Builder

> **End state:** Every LLM call receives a system prompt assembled from blocks in the correct order.

### Objective

Build the identity and prompt assembly system that defines Jarvis's behavior.

### Scope

- Jarvis identity YAML
- Mode fragments
- System prompt builder
- Wire into executor
- Identity enforcement test
- Tool validation layer

### Out of Scope

- No new contract types

### Dependencies

- Phase 4 (completed)

### Tasks

- [ ] TASK 5.1 — Jarvis identity YAML
  - Create `config/jarvis_identity.yaml`
  - Add: name, role, component_notice, safety_rules, language_behavior

- [ ] TASK 5.2 — Mode fragments
  - Create `src/core/identity/personality.py`
  - Define MODE_FRAGMENTS for all five modes
  - Implement `get_mode_fragment(mode)`

- [ ] TASK 5.3 — System prompt builder
  - Create `src/core/identity/builder.py`
  - Implement `build_system_prompt(task_context, mode, tools, previous_model, current_model)`
  - Inject blocks in correct order

- [ ] TASK 5.4 — Wire prompt builder into executor
  - Modify `src/core/runtime/executor.py`
  - Call build_system_prompt()
  - Pass prompt as system message

- [ ] TASK 5.5 — Identity Enforcement Test
  - Create `tests/test_identity_enforcement.py`
  - Verify identity block in all LLM calls

- [ ] TASK 5.6 — Tool Validation Layer
  - Create `src/core/tools/validator.py`
  - Validate tool aligns with DecisionOutput
  - Validate JSON schema
  - Check availability

### Definition of Done

1. Every model call includes identity block
2. Response reflects identity as Jarvis, not raw model
3. Modes affect response style correctly

### Validation Steps

```bash
python -c "
from src.core.identity.builder import build_system_prompt
p = build_system_prompt('hello', 'fast', [], None, 'gemma3:4b')
print('Jarvis' in p, 'component' in p)
"
```

### Failure Conditions

- Identity block missing from prompt
- Model identifies as raw model name
- Mode fragments not applying

### Artifacts

- `config/jarvis_identity.yaml`
- `src/core/identity/personality.py`
- `src/core/identity/builder.py`
- `src/core/runtime/executor.py` (modified)
- `src/core/tools/validator.py`
- `tests/test_identity_enforcement.py`

---

## Phase 6 — Tool System

> **End state:** Any registered skill is callable through the full pipeline: classify → registry → safety → validate → execute → ToolResult.

### Objective

Build the complete tool execution pipeline with safety and validation.

### Scope

- BaseTool abstract class
- Tool registry with auto-discovery
- Safety classifier
- Execution mode enforcement
- Schema validator
- Tool executor
- Tool call parser and retry

### Out of Scope

- Safety modes GUI (Phase 7)
- Specific tool implementations (Phase 8+)

### Dependencies

- Phase 5 (completed)

### Tasks

- [ ] TASK 6.1 — BaseTool abstract class
  - Create `src/core/tools/base.py`
  - Define BaseTool abstract class
  - Define required class attributes
  - Implement to_ollama_format()

- [ ] TASK 6.2 — Tool registry with auto-discovery
  - Create `src/core/tools/registry.py`
  - Implement ToolRegistry with discover()
  - Use pkgutil.walk_packages
  - Create singleton registry

- [ ] TASK 6.3 — Safety classifier
  - Create `src/core/tools/safety.py`
  - Implement classify_safety(tool_name, args)
  - Check shell command blocklist

- [ ] TASK 6.4 — Execution mode enforcement
  - Create `src/core/tools/mode_enforcer.py`
  - Implement should_execute(safety_result, execution_mode)
  - Implement is_explicit_override()

- [ ] TASK 6.5 — Schema validator
  - Modify `src/core/tools/validator.py`
  - Implement validate_args(args, schema)

- [ ] TASK 6.6 — Tool executor
  - Create `src/core/tools/executor.py`
  - Implement execute_tool(tool_name, args)
  - Full execution pipeline
  - Logging for tool.start/done/error

- [ ] TASK 6.7 — Tool call parser and retry
  - Modify `src/core/runtime/llm_output.py`
  - Enhance parse_llm_output with retry logic
  - Return parse failure indicator

### Definition of Done

1. All Phase 0 tools work through registry
2. Safety checks applied before execution
3. Parse failures trigger retry

### Validation Steps

```bash
python -c "
from src.core.tools.registry import registry
registry.discover()
print(f'Registered tools: {len(registry.all_names())}')
"
python -c "
from src.core.tools.executor import execute_tool
r = execute_tool('open_app', {'name': 'notepad'})
print(f'Success: {r.success}')
"
```

### Failure Conditions

- Tool not found in registry
- Tool executes without safety check
- Parse failure does not retry

### Artifacts

- `src/core/tools/base.py`
- `src/core/tools/registry.py`
- `src/core/tools/safety.py`
- `src/core/tools/mode_enforcer.py`
- `src/core/tools/validator.py` (modified)
- `src/core/tools/executor.py`
- `src/core/runtime/llm_output.py` (modified)

---

## Phase 7 — Safety Modes

> **End state:** Execution mode is configurable. All tool executions apply the correct policy. Risk levels are populated on all tools.

### Objective

Implement the three-mode policy system that controls tool execution.

### Scope

- Execution mode in config
- Risk levels on all tool entries
- CLI execution mode toggle
- Safety tests
- High-risk explicit approval flow

### Out of Scope

- Telegram/GUI mode change
- Persistent mode storage

### Dependencies

- Phase 6 (completed)

### Tasks

- [ ] TASK 7.1 — Execution mode in config
  - Modify `config/settings.yaml`
  - Add runtime.execution_mode field
  - Modify `src/core/config.py` RuntimeConfig

- [ ] TASK 7.2 — Risk levels on all tool entries
  - Modify `config/skills.yaml`
  - Ensure risk_level on every tool
  - Match Risk Classification table

- [ ] TASK 7.3 — CLI execution mode toggle
  - Create `src/interfaces/cli/commands.py`
  - Implement /mode command

- [ ] TASK 7.4 — Safety tests
  - Create `tests/test_safety.py`
  - Test all mode/risk combinations

- [ ] TASK 7.5 — High-risk explicit approval flow
  - Modify `src/core/tools/mode_enforcer.py`
  - Implement is_explicit_override(user_message, tool_name)

### Definition of Done

1. SAFE mode requires confirmation for all tools
2. BALANCED mode blocks high-risk without phrase
3. /mode command changes execution mode

### Validation Steps

```bash
python -c "
from src.core.config import get_settings
print(get_settings().runtime.execution_mode)
"
python -c "
from src.core.tools.mode_enforcer import should_execute
from src.core.tools.safety import SafetyResult
result = should_execute(SafetyResult(level='high', allowed=None, reason='test'), 'balanced')
print(f'Result: {result}')
"
```

### Failure Conditions

- Mode not in config
- High-risk tool executes without phrase in BALANCED

### Artifacts

- `config/settings.yaml` (modified)
- `src/core/config.py` (modified)
- `src/interfaces/cli/commands.py`
- `tests/test_safety.py`
- `src/core/tools/mode_enforcer.py` (modified)

---

## Phase 8 — System Control Skills

> **End state:** All OS-level operations work correctly on Windows, Linux, and macOS.

### Objective

Implement all system control tools that jarvis uses to interact with the operating system.

### Scope

- App launcher
- System information
- Clipboard
- Notifications
- Screenshot and OCR
- File operations
- Code executor
- Web search

### Out of Scope

- Browser automation
- Google APIs

### Dependencies

- Phase 7 (completed)

### Tasks

- [ ] TASK 8.1 — App launcher as BaseTool
  - Modify `src/skills/system/apps.py`
  - Convert to BaseTool subclasses
  - Create JSON Schema files

- [ ] TASK 8.2 — System information tool
  - Create `src/skills/system/sysinfo.py`
  - Implement system_info, list_processes, kill_process

- [ ] TASK 8.3 — Clipboard tool
  - Create `src/skills/system/clipboard.py`
  - Implement read_clipboard, write_clipboard

- [ ] TASK 8.4 — Notification tool
  - Create `src/skills/notify/toasts.py`
  - Cross-platform notifications

- [ ] TASK 8.5 — Screenshot and OCR tools
  - Create `src/skills/screen/capture.py`
  - Implement take_screenshot, read_screen_text

- [ ] TASK 8.6 — File operations tools
  - Create `src/skills/files/file_ops.py`
  - Implement read, write, list, search, move, copy, delete

- [ ] TASK 8.7 — Code executor tool
  - Create `src/skills/coder/executor.py`
  - Implement execute_python, run_shell

- [ ] TASK 8.8 — Web search tool
  - Create `src/skills/search/web_search.py`
  - Implement web_search with DuckDuckGo

### Definition of Done

1. All tools registered in Phase 6 registry
2. Each tool executes without error
3. Paths outside allowed roots are rejected

### Validation Steps

```bash
python -c "
from src.core.tools.executor import execute_tool
# Test each tool category
r = execute_tool('open_app', {'name': 'notepad'})
print(f'open_app: {r.success}')
r = execute_tool('system_info', {})
print(f'system_info: {r.success}')
r = execute_tool('read_clipboard', {})
print(f'read_clipboard: {r.success}')
"
```

### Failure Conditions

- Tool not in registry
- Cross-platform not working
- Path outside roots allowed

### Artifacts

- `src/skills/system/apps.py` (modified)
- `src/skills/system/sysinfo.py`
- `src/skills/system/clipboard.py`
- `src/skills/notify/toasts.py`
- `src/skills/screen/capture.py`
- `src/skills/files/file_ops.py`
- `src/skills/coder/executor.py`
- `src/skills/search/web_search.py`
- JSON Schema files in `config/schemas/`

---

## Phase 9 — Browser & Web Skills

> **End state:** Playwright browser with persistent sessions, file transfers, and WhatsApp automation.

### Objective

Implement browser automation tools for web interaction.

### Scope

- Playwright browser core
- Session persistence
- File download and upload
- Auth wall detection
- WhatsApp Web automation
- Session manager integration

### Out of Scope

- Google Chrome extension
- Browser extensions

### Dependencies

- Phase 8 (completed)

### Tasks

- [ ] TASK 9.1 — Playwright browser core
  - Create `src/skills/browser/browser.py`
  - Implement navigate, click, fill, get_text, screenshot

- [ ] TASK 9.2 — Session persistence
  - Create `src/skills/browser/session.py`
  - Save/load browser sessions with encryption

- [ ] TASK 9.3 — File download and upload
  - Create `src/skills/browser/transfer.py`
  - Handle downloads, file uploads

- [ ] TASK 9.4 — Auth wall detection and pause
  - Create `src/skills/browser/auth_handler.py`
  - Detect login pages, pause for user

- [ ] TASK 9.5 — WhatsApp Web automation
  - Create `src/skills/social/whatsapp.py`
  - Send/read messages via WhatsApp Web

- [ ] TASK 9.6 — Session manager integration
  - Modify `src/skills/browser/browser.py`
  - Auto-load sessions on navigation

### Definition of Done

1. Browser tools registered in Phase 6 registry
2. Navigate to page, stay logged in after restart

### Validation Steps

```bash
python -c "
from src.core.tools.executor import execute_tool
r = execute_tool('browser_navigate', {'url': 'https://example.com'})
print(f'Navigate: {r.success}')
"
```

### Failure Conditions

- Playwright not installed
- Session not persisted
- Auth wall not detected

### Artifacts

- `src/skills/browser/browser.py`
- `src/skills/browser/session.py`
- `src/skills/browser/transfer.py`
- `src/skills/browser/auth_handler.py`
- `src/skills/social/whatsapp.py`

---

## Phase 10 — Google APIs

> **End state:** Single OAuth consent flow provides access to Calendar, Gmail, Drive, Contacts, and YouTube.

### Objective

Implement Google API integrations with unified OAuth.

### Scope

- Unified Google OAuth
- Google Calendar
- Gmail
- Google Drive
- Google Contacts
- YouTube
- PDF and Office readers

### Dependencies

- Phase 9 (completed)

### Tasks

- [ ] TASK 10.1 — Unified Google OAuth
  - Create `src/skills/api/google_auth.py`
  - Combined scopes, token refresh

- [ ] TASK 10.2 — Google Calendar
  - Create `src/skills/api/calendar.py`
  - CRUD operations

- [ ] TASK 10.3 — Gmail
  - Create `src/skills/api/gmail.py`
  - List, send, read, manage

- [ ] TASK 10.4 — Google Drive
  - Create `src/skills/api/drive.py`
  - Upload, download, share

- [ ] TASK 10.5 — Google Contacts
  - Create `src/skills/api/contacts.py`
  - Search, resolve names

- [ ] TASK 10.6 — YouTube
  - Create `src/skills/api/youtube.py`
  - Search, get info, open

- [ ] TASK 10.7 — PDF and Office readers
  - Create `src/skills/pdf/reader.py`
  - Create `src/skills/office/reader.py`

### Definition of Done

1. All Google tools registered in Phase 6 registry
2. OAuth flow works end-to-end

### Validation Steps

```bash
python -c "
from src.core.tools.executor import execute_tool
r = execute_tool('calendar_list', {})
print(f'calendar_list: {r.success}')
"
```

### Failure Conditions

- OAuth credentials missing
- API calls fail

### Artifacts

- `src/skills/api/google_auth.py`
- `src/skills/api/calendar.py`
- `src/skills/api/gmail.py`
- `src/skills/api/drive.py`
- `src/skills/api/contacts.py`
- `src/skills/api/youtube.py`
- `src/skills/pdf/reader.py`
- `src/skills/office/reader.py`

---

## Phase 11 — Context + Memory

> **End state:** Facts from session 1 are recalled in session 2. Every turn auto-saves.

### Objective

Implement memory systems that persist data across turns.

### Scope

- Short-term memory (Redis/in-memory)
- Long-term semantic memory (ChromaDB)
- SQLite structured store
- Memory injection into assembler
- Auto-save after turn
- Feedback collection

### Dependencies

- Phase 3 (completed for assembler stub)

### Tasks

- [ ] TASK 11.1 — Short-term memory
  - Create `src/core/memory/short_term.py`
  - Implement save_message, get_history

- [ ] TASK 11.2 — Long-term semantic memory
  - Create `src/core/memory/long_term.py`
  - Implement remember, recall with ChromaDB

- [ ] TASK 11.3 — SQLite structured store
  - Create `src/core/memory/database.py`
  - CRUD for conversations, feedback, tasks

- [ ] TASK 11.4 — Memory injection into Context assembler
  - Modify `src/core/context/assembler.py`
  - Inject memory_snippets, recent_history

- [ ] TASK 11.5 — Auto-save after every turn
  - Modify `src/core/runtime/loop.py`
  - Save to all backends after turn

- [ ] TASK 11.6 — Feedback collection
  - Create `src/core/memory/feedback.py`
  - Implicit and explicit feedback

### Definition of Done

1. After telling Jarvis "my name is Ahmed", recall works in next session
2. SQLite contains conversation records after turns

### Validation Steps

```bash
python -c "
from src.core.context.assembler import assemble_context
p = assemble_context('hello', 'test_session')
print(f'Memory snippets: {len(p.memory_snippets)}')
print(f'History: {len(p.recent_history)}')
"
```

### Failure Conditions

- Memory not injecting
- Cross-session recall fails

### Artifacts

- `src/core/memory/short_term.py`
- `src/core/memory/long_term.py`
- `src/core/memory/database.py`
- `src/core/context/assembler.py` (modified)
- `src/core/runtime/loop.py` (modified)
- `src/core/memory/feedback.py`

---

## Phase 12 — Agents

> **End state:** Multi-step goals execute without step-by-step user guidance.

### Objective

Implement agents that handle complex multi-step reasoning.

### Scope

- Thinker agent (chain-of-thought)
- Planner agent (task decomposition)
- Step executor
- Researcher agent
- Computer use agent

### Dependencies

- Phase 11 (completed)

### Tasks

- [ ] TASK 12.1 — Thinker agent
  - Create `src/core/agents/thinker.py`
  - Implement chain-of-thought reasoning

- [ ] TASK 12.2 — Planner agent
  - Create `src/core/agents/planner.py`
  - Decompose goal into steps

- [ ] TASK 12.3 — Step executor
  - Create `src/core/agents/step_executor.py`
  - Execute steps in dependency order

- [ ] TASK 12.4 — Researcher agent
  - Create `src/core/agents/researcher.py`
  - Multi-source web research

- [ ] TASK 12.5 — Computer use agent
  - Create `src/core/agents/computer_use.py`
  - Autonomous screen control

### Definition of Done

1. Planner decomposes multi-step goals
2. Researcher returns multi-source report

### Validation Steps

```bash
python -c "
from src.core.agents.planner import plan
steps = plan('search AI news and save summary', ['web_search', 'write_file'])
print(f'Steps: {len(steps)}')
"
```

### Failure Conditions

- Planner returns empty for valid goal
- Researcher single-source only

### Artifacts

- `src/core/agents/thinker.py`
- `src/core/agents/planner.py`
- `src/core/agents/step_executor.py`
- `src/core/agents/researcher.py`
- `src/core/agents/computer_use.py`

---

## Phase 13 — CLI Interface

> **End state:** Rich terminal chat with streaming, Arabic RTL, slash commands, and hotkeys.

### Objective

Build the command-line interface.

### Scope

- Rich chat loop
- Slash commands
- Global hotkeys
- Input history
- Status bar

### Dependencies

- Phase 7 (for /mode command)

### Tasks

- [ ] TASK 13.1 — Rich chat loop
  - Create `src/interfaces/cli/interface.py`
  - Streaming display, Arabic RTL

- [ ] TASK 13.2 — Slash commands
  - Create `src/interfaces/cli/commands.py`
  - All commands from Phase 7 + more

- [ ] TASK 13.3 — Global hotkeys
  - Create `src/interfaces/cli/hotkeys.py`
  - System-wide keyboard shortcuts

- [ ] TASK 13.4 — Input history
  - Modify `src/interfaces/cli/interface.py`
  - Arrow key navigation

- [ ] TASK 13.5 — Status bar
  - Modify `src/interfaces/cli/interface.py`
  - Model, mode, turn count display

### Definition of Done

1. CLI runs without error
2. Slash commands work
3. Arabic RTL displays correctly

### Validation Steps

```bash
python app/main.py --interface cli
# Type: /help, /mode safe, /clear
# Type Arabic message
```

### Failure Conditions

- CLI crashes on start
- Arabic not RTL aligned

### Artifacts

- `src/interfaces/cli/interface.py`
- `src/interfaces/cli/commands.py`
- `src/interfaces/cli/hotkeys.py`

---

## Phase 14 — Web UI

> **End state:** Glassmorphism chat interface in browser with streaming, file upload, conversation management, and dashboard.

### Objective

Build the web-based user interface.

### Scope

- FastAPI application
- WebSocket endpoint
- HTML document
- CSS design system
- JavaScript: chat core
- JavaScript: markdown/code/math
- JavaScript: attachments
- JavaScript: sidebar
- JavaScript: settings panel
- REST API routes
- Connection status
- Dashboard panel
- Feedback actions

### Dependencies

- Phase 11 (for conversation storage)

### Tasks

- [ ] TASK 14.1 — FastAPI application and WebSocket endpoint
  - Create `src/interfaces/web/app.py`
  - Create `src/interfaces/web/ws.py`
  - Create `app/server.py`

- [ ] TASK 14.2 — HTML document structure
  - Create `src/interfaces/web/templates/index.html`

- [ ] TASK 14.3 — CSS design system
  - Create `src/interfaces/web/static/style.css`
  - Glassmorphism dark/light themes

- [ ] TASK 14.4 — JavaScript: WebSocket and chat core
  - Create `src/interfaces/web/static/chat.js`
  - WebSocket connection, token streaming

- [ ] TASK 14.5 — JavaScript: Markdown, code, and math rendering
  - Modify `src/interfaces/web/static/chat.js`
  - marked.js, highlight.js, KaTeX

- [ ] TASK 14.6 — JavaScript: Attachment system
  - Modify `src/interfaces/web/static/chat.js`
  - File drag-drop, paste, upload

- [ ] TASK 14.7 — JavaScript: Sidebar and conversation management
  - Modify `src/interfaces/web/static/chat.js`
  - List, search, pin, delete conversations

- [ ] TASK 14.8 — JavaScript: Settings panel
  - Modify `src/interfaces/web/static/chat.js`
  - Theme toggle, persist settings

- [ ] TASK 14.9 — REST API routes
  - Create `src/interfaces/web/routes.py`
  - Conversation CRUD, upload, status

- [ ] TASK 14.10 — Connection status and error handling
  - Modify `src/interfaces/web/static/chat.js`
  - Status indicator, reconnect logic

- [ ] TASK 14.11 — Dashboard panel
  - Modify `src/interfaces/web/static/chat.js`
  - VRAM, CPU, RAM displayed

- [ ] TASK 14.12 — Feedback and message actions
  - Modify `src/interfaces/web/static/chat.js`
  - Thumbs up/down, copy, regenerate

### Definition of Done

1. Web UI loads at http://localhost:8080
2. Streaming works
3. Conversation management works
4. Dashboard updates

### Validation Steps

```bash
python app/server.py
# Open http://localhost:8080
# Send message, verify streaming
# Check dashboard
```

### Failure Conditions

- Page fails to load
- WebSocket disconnects

### Artifacts

- `src/interfaces/web/app.py`
- `src/interfaces/web/ws.py`
- `src/interfaces/web/routes.py`
- `app/server.py`
- `src/interfaces/web/templates/index.html`
- `src/interfaces/web/static/style.css`
- `src/interfaces/web/static/chat.js`

---

## Phase 15 — Voice Pipeline

> **End state:** "Hey Jarvis" → speech command → spoken response.

### Objective

Implement voice input and output.

### Scope

- Whisper STT
- Piper TTS
- Wake word detection
- Voice Activity Detection
- Full voice pipeline

### Dependencies

- Phase 3 (for run_turn integration)

### Tasks

- [ ] TASK 15.1 — Whisper STT
  - Create `src/models/speech/stt.py`
  - Implement transcribe(audio)

- [ ] TASK 15.2 — Piper TTS
  - Create `src/models/speech/tts.py`
  - Implement speak(text, language)

- [ ] TASK 15.3 — Wake word detection
  - Create `src/interfaces/voice/wake_word.py`
  - Detect "Hey Jarvis"

- [ ] TASK 15.4 — Voice Activity Detection
  - Create `src/interfaces/voice/vad.py`
  - Auto-stop recording

- [ ] TASK 15.5 — Full voice pipeline
  - Create `src/interfaces/voice/pipeline.py`
  - Integrate all components

### Definition of Done

1. Wake word triggers listening
2. Speech transcribed correctly
3. Response spoken back

### Validation Steps

```bash
# Say "Hey Jarvis, what is the time?"
# Verify response is spoken
```

### Failure Conditions

- Wake word not detected
- Transcription wrong language

### Artifacts

- `src/models/speech/stt.py`
- `src/models/speech/tts.py`
- `src/interfaces/voice/wake_word.py`
- `src/interfaces/voice/vad.py`
- `src/interfaces/voice/pipeline.py`

---

## Phase 16 — Vision + Image Generation

> **End state:** Images described in Arabic. Images generated from text prompts.

### Objective

Add vision capabilities.

### Scope

- LLaVA image understanding
- Stable Diffusion image generation
- Vision integration into runtime
- Screen description tool

### Dependencies

- Phase 8 (for screenshot tool)

### Tasks

- [ ] TASK 16.1 — LLaVA image understanding
  - Create `src/models/vision/llava.py`
  - Implement describe_image

- [ ] TASK 16.2 — Stable Diffusion image generation
  - Create `src/models/diffusion/sd.py`
  - Implement generate_image

- [ ] TASK 16.3 — Vision integration into runtime
  - Modify `src/core/context/assembler.py`
  - Inject image descriptions

- [ ] TASK 16.4 — Screen description tool
  - Create `src/skills/screen/describe.py`
  - Implement describe_screen

### Definition of Done

1. Upload image, ask "what is this?" → description returned
2. Generate image prompt → PNG created

### Validation Steps

```bash
python -c "
from src.models.vision.llava import describe_image
print(describe_image('test.png', 'what is this'))
"
```

### Failure Conditions

- LLaVA model not available
- Image generation OOM

### Artifacts

- `src/models/vision/llava.py`
- `src/models/diffusion/sd.py`
- `src/skills/screen/describe.py`

---

## Phase 17 — Telegram + GUI

> **End state:** Telegram bot handles text, photos, and voice. PyQt6 desktop app with tray.

### Objective

Add additional interfaces.

### Scope

- Telegram bot
- PyQt6 desktop app
- System tray

### Dependencies

- Phase 14 (for WebSocket reference)

### Tasks

- [ ] TASK 17.1 — Telegram bot
  - Create `src/interfaces/telegram/bot.py`
  - Create `src/interfaces/telegram/handlers.py`
  - Handle text, photo, voice

- [ ] TASK 17.2 — PyQt6 desktop app
  - Create `src/interfaces/gui/app.py`
  - Window with chat display

- [ ] TASK 17.3 — System tray
  - Create `src/interfaces/gui/tray.py`
  - Tray icon with menu

- [ ] TASK 17.4 — Integrate all interfaces in main.py
  - Modify `app/main.py`
  - Support --interface all

### Definition of Done

1. Telegram bot responds to messages
2. Desktop app shows in tray

### Validation Steps

```bash
# Send message to Telegram bot
# App appears in system tray
```

### Failure Conditions

- Telegram token missing
- PyQt6 not installed

### Artifacts

- `src/interfaces/telegram/bot.py`
- `src/interfaces/telegram/handlers.py`
- `src/interfaces/gui/app.py`
- `src/interfaces/gui/tray.py`

---

## Phase 18 — QA + Security

> **End state:** Comprehensive test suite passes. Security audit complete. Production-ready.

### Objective

Finalize the system with testing and security.

### Scope

- Comprehensive test suite
- Security audit
- Error handling improvements
- Performance optimization
- Documentation

### Dependencies

- Phase 17 (completed)

### Tasks

- [ ] TASK 18.1 — Test suite
  - Create `tests/test_integration.py`
  - Test full pipeline end-to-end

- [ ] TASK 18.2 — Security audit
  - Check all dangerous command blocks
  - Verify confirmation phrases work

- [ ] TASK 18.3 — Error handling improvements
  - Enhance error messages
  - Ensure all errors logged

- [ ] TASK 18.4 — Performance optimization
  - Profile runtime
  - Optimize hot paths

- [ ] TASK 18.5 — Documentation
  - Complete ARCHITECTURE.md
  - API documentation

- [ ] TASK 18.6 — Final integration test
  - Run full test suite
  - Fix all failures

- [ ] TASK 18.7 — Production readiness checklist
  - Verify all phases complete
  - Create VERSION file

### Definition of Done

1. All tests pass
2. Security audit clean
3. Documentation complete

### Validation Steps

```bash
pytest tests/ -v
```

### Failure Conditions

- Test failures
- Security issues found
- Documentation incomplete

### Artifacts

- `tests/test_integration.py`
- `ARCHITECTURE.md`
- `VERSION`

---

## End of Execution Plan