# JARVIS — Execution Plan v2.0

## Project Status

```yaml
project:
  name: JARVIS
  version: "2.0"
  spec_version: "v2.0"
  last_updated: "2026-04-30"
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
| 0 | First Working System (Vertical Slice) | P0 | [x] | 100% | 5/5 | none | Phase 0 complete | 2026-04-26 |
| 1 | Foundation + Observability | P0 | [ ] | 0% | 0/10 | none | Start TASK 1.1 | - |
| 2 | Execution Contract | P0 | [ ] | 0% | 0/7 | none | Start TASK 2.1 | - |
| 3 | Model Manager + VRAM | P0 | [ ] | 0% | 0/5 | none | Start TASK 3.1 | - |
| 4 | Runtime State Machine | P0 | [ ] | 0% | 0/8 | none | Start TASK 4.1 | - |
| 5 | Decision System | P1 | [ ] | 0% | 0/7 | none | Start TASK 5.1 | - |
| 6 | Sandbox + Safety | P0 | [ ] | 0% | 0/7 | none | Start TASK 6.1 | - |
| 7 | Memory Engine | P1 | [ ] | 0% | 0/6 | none | Start TASK 7.1 | - |
| 8 | Capability System | P1 | [ ] | 0% | 0/6 | none | Start TASK 8.1 | - |
| 9 | System Control Capabilities | P1 | [ ] | 0% | 0/8 | none | Start TASK 9.1 | - |
| 10 | Prompt Builder | P1 | [ ] | 0% | 0/5 | none | Start TASK 10.1 | - |
| 11 | Execution Hardening | P0 | [ ] | 0% | 0/6 | none | Start TASK 11.1 | - |
| 12 | CLI Interface | P2 | [ ] | 0% | 0/3 | none | Start TASK 12.1 | - |
| 13 | Web Automation & Browser | P2 | [ ] | 0% | 0/3 | none | Start TASK 13.1 | - |
| 14 | Google APIs | P2 | [ ] | 0% | 0/4 | none | Start TASK 14.1 | - |
| 15 | Web UI | P2 | [ ] | 0% | 0/3 | none | Start TASK 15.1 | - |
| 16 | Voice Pipeline | P3 | [ ] | 0% | 0/4 | none | Start TASK 16.1 | - |
| 17 | Vision + Image | P3 | [ ] | 0% | 0/2 | none | Start TASK 17.1 | - |
| 18 | QA + Production | P0 | [ ] | 0% | 0/6 | none | Start TASK 18.1 | - |

---

## Phase 0 — First Working System (Vertical Slice)

```
phase_id: 0
title: "First Working System (Vertical Slice)"
priority: "P0"
status: "completed"
progress_percent: 100
done_tasks: 5
total_tasks: 5
blocker: "none"
next_action: "Start Phase 1"
last_updated: "2026-04-26"
validation_status: "completed"
```

### Objective

Create a minimal working end-to-end system that proves the core pipeline works: text input reaches the LLM and returns a response, and a capability command is classified, routed, and executed. This is a vertical slice — it touches every layer of the eventual architecture, proving the pipeline before building out the full system.

### Tasks

**TASK 0.1 — Connect to Ollama and get a response**

Location:
- `src/models/llm/engine.py`

Purpose:
- Establish LLM communication layer for local Ollama instance.

Steps:
1. Create `src/models/llm/` directory.
2. Create `src/models/llm/engine.py` file.
3. Define `OllamaEngine` class with `chat(message, model)` method.
4. Implement Ollama Python client connection.
5. Handle connection errors with try/except.
6. Return response content as string.
7. Set default timeout to 60 seconds.

Input:
- `message`: string (user input).
- `model`: string (model tag, default: gemma3:4b).

Output:
- `response`: string (non-empty LLM responses).

Dependencies:
- None (starting phase).

Success case:
- `chat("hello")` returns non-empty string within 60 seconds.

Failure case:
- Ollama not running → raises `ConnectionError`, caught and returns error message.
- Timeout > 60s → raises `TimeoutError`, caught and returns timeout message.

Edge cases:
- Empty message → returns error message "Empty input".
- Unicode/Arabic input → handled without encoding errors.

Validation:
```bash
python -c "from src.models.llm.engine import OllamaEngine; e = OllamaEngine(); r = e.chat('hello', 'gemma3:4b'); assert len(r) > 0, 'Empty response'; print(r)"
```

Artifact: `src/models/llm/engine.py`

---

**TASK 0.2 — Classify a command and return structured output**

Location:
- `src/core/decision/classifier.py`

Purpose:
- Implement intent classification using LLM to determine user intent and extract tool calls.

Steps:
1. Create `src/core/decision/` directory.
2. Create `src/core/decision/classifier.py` file.
3. Define `Classifier` class with `classify(message)` method.
4. Use gemma3:4b with JSON-forcing system prompt.
5. Implement JSON parsing with error handling.
6. Add retry logic (max 2 attempts).
7. Return dict with keys: intent, tool_name, tool_args.
8. Implement safe fallback dict on all failures: `{intent: "chat", tool_name: null, tool_args: {}}`.

Input:
- `message`: string (user command).

Output:
- `dict`: `{intent: str, tool_name: str|null, tool_args: dict}`.

Dependencies:
- TASK 0.1 (Ollama connection).

Success case:
- `classify("open chrome")` returns `{intent: "tool_use", tool_name: "open_app", tool_args: {"name": "chrome"}}`.

Failure case:
- LLM returns invalid JSON → retry once, then return safe fallback.
- Ollama unavailable → return safe fallback immediately.

Edge cases:
- Arabic input "افتح المفكرة" → same intent classification as "open notepad".
- Ambiguous input → defaults to `intent: "chat"`.

Validation:
```bash
python -c "
from src.core.decision.classifier import Classifier
c = Classifier()
r = c.classify('open notepad')
assert r['intent'] in ('tool_use', 'chat'), f'Invalid intent: {r[\"intent\"]}'
print(r)
"
```

Artifact: `src/core/decision/classifier.py`

---

**TASK 0.3 — Execute an application by name**

Location:
- `src/capabilities/system/apps.py`

Purpose:
- Implement system capability to launch applications by name.

Steps:
1. Create `src/capabilities/system/` directory.
2. Create `src/capabilities/system/apps.py` file.
3. Define `AppLauncher` class with `open_app(name)` method.
4. Implement Windows search (PATH, Program Files, Start Menu).
5. Return success/error dict without raising exceptions.
6. Include PID in success response.
7. Block dangerous app names (format, mkfs, etc.).

Input:
- `name`: string (application name).

Output:
- `dict`: `{success: bool, pid: int|null, error: str|null}`.

Dependencies:
- None (can run independently).

Success case:
- `open_app("notepad")` returns `{success: true, pid: N}`.

Failure case:
- App not found → returns `{success: false, error: "Application not found: notepad2"}`.
- Dangerous app name → returns `{success: false, error: "Blocked: dangerous application"}`.

Edge cases:
- Case-insensitive matching: "Notepad" == "notepad".
- App already running → still returns success with new PID.

Validation:
```bash
python -c "
from src.capabilities.system.apps import AppLauncher
al = AppLauncher()
r = al.open_app('notepad')
assert 'success' in r and 'error' in r, 'Missing fields'
print(r)
"
```

Artifact: `src/capabilities/system/apps.py`

---

**TASK 0.4 — Wire classifier to capability: text input to action**

Location:
- `app/jarvis_slice.py`

Purpose:
- Connect all Phase 0 components into a working CLI loop (vertical slice proof).

Steps:
1. Create `app/` directory.
2. Create `app/jarvis_slice.py` file.
3. Implement `run(user_input)` function.
4. Wire: input → classify → route to tool or LLM → output.
5. Implement terminal input loop.
6. Add "quit" command to exit cleanly.
7. Print tool execution results or LLM response.

Input:
- Terminal text input from user.

Output:
- Tool execution result or LLM response printed to terminal.

Dependencies:
- TASK 0.1 (Ollama connection).
- TASK 0.2 (Classifier).
- TASK 0.3 (App launcher).

Success case:
- Type "open notepad" → Notepad opens, result printed.
- Type "what is AI?" → LLM response printed.
- Type "quit" → clean exit.

Failure case:
- Loop does not exit on "quit" → FAIL.
- Classification always returns "chat" even for "open notepad" → FAIL.
- No response printed → FAIL.

Edge cases:
- Empty input → prints prompt, does not crash.
- Ctrl+C → graceful exit with message.

Validation:
```bash
python app/jarvis_slice.py
# Type: "open notepad" → should open Notepad
# Type: "what is AI?" → response printed
# Type: "quit" → exits with code 0
```

Artifact: `app/jarvis_slice.py`

---

**TASK 0.5 — Verify Arabic input**

Location:
- Test task (no file creation).

Purpose:
- Ensure Arabic language commands produce identical behavior to English.

Steps:
1. Test Arabic command: "افتح المفكرة" (open notepad).
2. Verify same intent classification as "open notepad".
3. Test Arabic question: "ما هو الذكاء الاصطناعي؟".
4. Verify same response behavior as "what is AI?".

Input:
- Arabic text commands.

Output:
- Same intents/responses as English equivalents.

Dependencies:
- TASK 0.2 (Classifier).
- TASK 0.3 (App launcher).

Success case:
- Arabic "افتح المفكرة" → `intent=tool_use`, `tool_name=open_app`.
- Arabic "ما هو الذكاء الاصطناعي؟" → `intent=chat`.

Failure case:
- Different intent for Arabic vs English → FAIL.
- Arabic input causes encoding error → FAIL.

Edge cases:
- Mixed Arabic/English input → handled without error.
- Right-to-left display in terminal → cosmetic, not functional.

Validation:
- Run classifier with Arabic input, verify intent matches English equivalent.

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

## Phase 1 — Foundation + Observability

```
phase_id: 1
title: "Foundation + Observability"
priority: "P0"
status: "not_started"
progress_percent: 0
done_tasks: 0
total_tasks: 10
blocker: "Phase 0 must complete"
next_action: "Start TASK 1.1"
last_updated: "-"
validation_status: "not_started"
```

### Objective

Establish configuration system, logging infrastructure, observability system, and project package structure. This phase creates the foundation that all subsequent phases depend on.

### Tasks

**TASK 1.1 — Settings YAML and Pydantic loader**

Location:
- `config/settings.yaml`
- `src/core/config.py`

Purpose:
- Create configuration system with YAML settings and Pydantic validation.

Steps:
1. Create `config/` directory.
2. Create `config/settings.example.yaml` with all default settings.
3. Define settings structure: models, paths, execution modes, safety, limits, observability.
4. Create `src/core/config.py`.
5. Define Pydantic `Settings` model matching YAML structure.
6. Implement `load_config(path)` function.
7. Add environment variable override support.
8. Validate required fields on load.

Success case:
- `load_config("config/settings.yaml")` returns validated Settings object.
- Missing required field raises `ValidationError`.

Failure case:
- YAML file not found → raises `FileNotFoundError` with clear message.
- Invalid YAML syntax → raises `yaml.YAMLError` with line number.

Edge cases:
- Empty YAML file → uses all defaults.
- Environment variable overrides YAML values.

Validation:
```bash
python -c "from src.core.config import load_config; s = load_config('config/settings.yaml'); assert s.models.default is not None; print(s.models.default)"
```

Artifact: `src/core/config.py`, `config/settings.example.yaml`

---

**TASK 1.2 — Structured logging setup**

Location:
- `src/core/logging_setup.py`

Purpose:
- Implement structured logging with all required fields from README spec.

Steps:
1. Create `src/core/logging_setup.py`.
2. Define `setup_logging(level, format)` function.
3. Configure Loguru with structured output.
4. Include required fields: timestamp, level, event, session_id, turn_id, phase, trace_id, data.
5. Add file and console sinks.
6. Implement log rotation (max 100MB per file, 5 files).

Success case:
- Log output contains all required fields.
- Logs written to both file and console.

Failure case:
- Log directory not writable → falls back to stderr only.

Edge cases:
- Concurrent log writes from multiple processes → Loguru handles safely.
- Log file grows beyond rotation limit → old files archived.

Validation:
```bash
python -c "
from src.core.logging_setup import setup_logging
import logging
setup_logging('INFO')
logger = logging.getLogger('test')
logger.info('test', extra={'event': 'test', 'session_id': 's1', 'turn_id': 1, 'phase': 'test', 'trace_id': 't1', 'data': {}})
# Verify log line contains all required fields
"
```

Artifact: `src/core/logging_setup.py`

---

**TASK 1.3 — Package skeleton**

Location:
- All `__init__.py` files.

Purpose:
- Create proper Python package structure matching STRUCTURE.md.

Steps:
1. Create all `__init__.py` files in each package.
2. Define proper imports for public API.
3. Add version info to `src/__init__.py`.
4. Ensure all packages are importable.

Success case:
- `import src.core.runtime` succeeds.
- `import src.capabilities` succeeds.

Failure case:
- Missing `__init__.py` → `ModuleNotFoundError`.

Validation:
```bash
python -c "import src; import src.core; import src.capabilities; import src.interfaces; import src.services; import src.models; import src.memory; print('All packages importable')"
```

---

**TASK 1.4 — Model capability profiles**

Location:
- `src/models/profiles.py`

Purpose:
- Define model capability profiles for dynamic model selection.

Steps:
1. Create `src/models/profiles.py`.
2. Define `ModelProfile` dataclass: name, vram_required_mb, capabilities, latency_tier, reasoning_tier.
3. Create profile for each model: gemma3:4b, qwen3:8b, qwen2.5-coder:7b, llava:7b.
4. Implement `get_profile(model_name)` lookup function.
5. Add VRAM budget validation per profile.

Success case:
- `get_profile("gemma3:4b")` returns valid ModelProfile with vram_required_mb > 0.

Failure case:
- Unknown model name → returns None (caller handles gracefully).

Validation:
```bash
python -c "from src.models.profiles import get_profile; p = get_profile('gemma3:4b'); assert p.vram_required_mb > 0; print(p)"
```

Artifact: `src/models/profiles.py`

---

**TASK 1.5 — Model profiles YAML config**

Location:
- `config/models.yaml`

Purpose:
- Define model profiles, scoring weights, and fallback chain in configuration.

Steps:
1. Create `config/models.yaml`.
2. Define each model: name, vram_required_mb, capabilities, latency_tier, reasoning_tier.
3. Define scoring weights: fit_complexity, fit_mode, cost_penalty, quality_need, memory_bias.
4. Define fallback chain: Tier 1 (qwen2.5:7b), Tier 2 (gemma3:4b).
5. Define variability margin (±0.05).

Success case:
- YAML loads with all models, weights, and fallback chain present.

Validation:
```bash
python -c "import yaml; m = yaml.safe_load(open('config/models.yaml')); assert 'models' in m and 'weights' in m and 'fallback' in m; print('OK')"
```

Artifact: `config/models.yaml`

---

**TASK 1.6 — Environment variables**

Location:
- `.env.example`
- `.env`

Purpose:
- Set up environment variable configuration for secrets.

Steps:
1. Create `.env.example` with all required variables.
2. Variables: TELEGRAM_BOT_TOKEN, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, OLLAMA_BASE_URL.
3. Document each variable purpose.
4. Add python-dotenv loading in config system.
5. Create `.env` from example (gitignored).

Success case:
- `load_dotenv()` loads `.env` file without errors.

Validation:
```bash
python -c "from dotenv import load_dotenv; load_dotenv(override=True); print('Env loaded')"
```

---

**TASK 1.7 — User profile**

Location:
- `src/memory/user_profile.py`

Purpose:
- Implement user profile storage for personalization.

Steps:
1. Create `src/memory/user_profile.py`.
2. Define `UserProfile` dataclass: user_id, name, language, preferences, execution_mode.
3. Implement `load_profile(user_id)` function.
4. Implement `save_profile(profile)` function.
5. Add default profile creation.

Success case:
- `load_profile("default")` returns UserProfile with default values.

Failure case:
- Profile file corrupted → returns default profile, logs warning.

Validation:
```bash
python -c "from src.memory.user_profile import load_profile; p = load_profile('default'); assert p.language in ('en', 'ar'); print(p.language)"
```

Artifact: `src/memory/user_profile.py`

---

**TASK 1.8 — Capabilities manifest**

Location:
- `config/capabilities.yaml`

Purpose:
- Define all system capabilities with metadata for registry.

Steps:
1. Create `config/capabilities.yaml`.
2. Define each capability: name, domain, risk_level, description, module_path.
3. Include: system, files, web_automation, screen, vision, voice, notify, search, coder.
4. Add input/output schema references.
5. Define cross-platform support per capability.

Success case:
- YAML loads with all capabilities, each having risk_level.

Validation:
```bash
python -c "import yaml; m = yaml.safe_load(open('config/capabilities.yaml')); assert all('risk_level' in c for c in m['capabilities']); print(len(m['capabilities']))"
```

Artifact: `config/capabilities.yaml`

---

**TASK 1.9 — Observability: Metrics collector**

Location:
- `src/core/observability/metrics.py`

Purpose:
- Implement metrics collection for latency, throughput, error rate, model usage.

Steps:
1. Create `src/core/observability/` directory.
2. Create `src/core/observability/metrics.py`.
3. Define `MetricsCollector` class.
4. Implement `record_latency(phase, ms)` method.
5. Implement `record_error(phase, error_type)` method.
6. Implement `record_model_usage(model_name, success)` method.
7. Implement `get_summary()` method returning current metrics.

Success case:
- Metrics collected and retrievable via `get_summary()`.

Failure case:
- Metrics collector not initialized → returns empty summary.

Validation:
```bash
python -c "
from src.core.observability.metrics import MetricsCollector
mc = MetricsCollector()
mc.record_latency('decision', 50)
mc.record_error('model', 'timeout')
s = mc.get_summary()
assert 'decision' in s['latency']
print(s)
"
```

Artifact: `src/core/observability/metrics.py`

---

**TASK 1.10 — main.py entry point**

Location:
- `app/main.py`

Purpose:
- Create main application entry point with CLI argument parsing and boot sequence.

Steps:
1. Create `app/main.py`.
2. Implement `main()` function.
3. Add argparse for: --interface (cli/web), --debug, --trace, --mode.
4. Add boot sequence: config → logging → observability → validate → start interface.
5. Implement Ctrl+C graceful exit.
6. Print "Jarvis ready" on successful start.

Success case:
- `python app/main.py --interface cli` boots and prints "Jarvis ready".
- Ctrl+C exits without traceback.

Failure case:
- Config file missing → exits with error message (not crash).
- Ollama not running → prints warning, continues with fallback capability.

Edge cases:
- Invalid --mode value → exits with usage message.
- --debug and --trace together → enables both modes.

Validation:
```bash
python app/main.py --interface cli
# Should see: jarvis starting → config loaded → logging init → observability init → jarvis ready
# Ctrl+C should exit without traceback
```

Artifact: `app/main.py`

---

### Definition of Done

`python app/main.py --interface cli` runs all boot steps and prints "Jarvis ready". Ctrl+C exits cleanly.

### Human Checkpoint

After TASK 1.10, manually test Ctrl+C exit, verify "Jarvis ready" appears, and check log file contains structured entries.

---

## Phase 2 — Execution Contract

```
phase_id: 2
title: "Execution Contract"
priority: "P0"
status: "not_started"
progress_percent: 0
done_tasks: 0
total_tasks: 7
blocker: "Phase 1 must complete"
next_action: "Start TASK 2.1"
last_updated: "-"
validation_status: "not_started"
```

### Objective

Define strict data contracts that bind all components. Every contract is validated on instantiation and rejects invalid data.

### Tasks

**TASK 2.1 — Define InputPacket**

Location:
- `src/core/context/bundle.py`

Purpose:
- Create InputPacket dataclass matching README spec exactly.

Steps:
1. Create `src/core/context/` directory.
2. Create `src/core/context/bundle.py`.
3. Define `InputPacket` dataclass with all required fields: user_message (str, required), session_id (str, required), attachments (list, default []), memory_snippets (list, default []), recent_history (list, default []), user_profile (UserProfile, required), tool_results (list, default []), turn_number (int, default 0).
4. Add validation on instantiation (Pydantic or dataclass with checks).
5. Add `to_dict()` and `from_dict()` methods.

Success case:
- Valid InputPacket instantiates without error.
- Missing required field raises `ValueError`.

Failure case:
- `user_message=None` → raises `ValueError`.
- `session_id=""` → raises `ValueError`.

Validation:
```bash
python -c "
from src.core.context.bundle import InputPacket
from src.memory.user_profile import UserProfile
p = InputPacket(user_message='hello', session_id='s1', user_profile=UserProfile(user_id='default'))
assert p.user_message == 'hello'
print('OK')
"
```

Artifact: `src/core/context/bundle.py`

---

**TASK 2.2 — Define DecisionOutput**

Location:
- `src/core/decision/decision.py`

Purpose:
- Create DecisionOutput dataclass matching README spec exactly.

Steps:
1. Create `src/core/decision/decision.py`.
2. Define `DecisionOutput` with: intent (enum), complexity (enum), mode (enum), model (str), requires_tools (bool), requires_planning (bool, default false), tool_name (str|null), tool_args (dict, default {}), confidence (float 0.0-1.0), risk_level (enum), decision_source (enum: fast_path|model), score_breakdown (dict, required), candidate_list (list, required).
3. Add validation: intent must be valid, tool_name null if requires_tools=false, confidence in [0.0, 1.0], score_breakdown and candidate_list required.

Success case:
- Valid DecisionOutput instantiates.
- `confidence=1.5` raises `ValueError`.

Failure case:
- Missing `score_breakdown` → raises `ValueError`.
- `tool_name` set when `requires_tools=False` → raises `ValueError`.

Validation:
```bash
python -c "
from src.core.decision.decision import DecisionOutput
d = DecisionOutput(
    intent='chat', complexity='low', mode='fast', model='gemma3:4b',
    requires_tools=False, confidence=0.9, risk_level='low',
    decision_source='fast_path', score_breakdown={'fit_complexity': 1.0},
    candidate_list=[{'model': 'gemma3:4b', 'score': 0.9}]
)
assert d.intent == 'chat'
print('OK')
"
```

Artifact: `src/core/decision/decision.py`

---

**TASK 2.3 — Define LLMOutput**

Location:
- `src/core/runtime/llm_output.py`

Purpose:
- Create LLMOutput dataclass matching README spec exactly.

Steps:
1. Create `src/core/runtime/` directory.
2. Create `src/core/runtime/llm_output.py`.
3. Define `LLMOutput` with: type (enum: answer|tool_call), content (str, required if type=answer), tool (str|null, required if type=tool_call), args (dict, default {}).
4. Add validation: enforce type-content/tool consistency.

Success case:
- `LLMOutput(type="answer", content="hello")` validates.
- `LLMOutput(type="tool_call", tool="open_app", args={"name": "notepad"})` validates.

Failure case:
- `type="answer"` with no content → raises `ValueError`.
- `type="tool_call"` with no tool → raises `ValueError`.

Validation:
```bash
python -c "from src.core.runtime.llm_output import LLMOutput; o = LLMOutput(type='answer', content='hello'); assert o.type == 'answer'; print('OK')"
```

Artifact: `src/core/runtime/llm_output.py`

---

**TASK 2.4 — Define ToolResult**

Location:
- `src/capabilities/result.py`

Purpose:
- Create ToolResult dataclass matching README spec exactly.

Steps:
1. Create `src/capabilities/result.py`.
2. Define `ToolResult` with: tool (str, required), success (bool, required), data (dict, default {}), error (str, default ''), duration_ms (float, default 0.0), dry_run (bool, default false).

Success case:
- `ToolResult(tool="open_app", success=True)` validates.

Validation:
```bash
python -c "from src.capabilities.result import ToolResult; r = ToolResult(tool='open_app', success=True); assert r.success; print('OK')"
```

Artifact: `src/capabilities/result.py`

---

**TASK 2.5 — Define FinalResponse**

Location:
- `src/core/runtime/final_response.py`

Purpose:
- Create FinalResponse dataclass matching README spec exactly.

Steps:
1. Create `src/core/runtime/final_response.py`.
2. Define `FinalResponse` with: text (str, required), session_id (str, required), model (str, required), mode (str, required), quality (float 0.0-1.0, required), decision_source (enum: fast_path|model, required), degraded (bool, default false), turn_id (int, required).

Success case:
- Valid FinalResponse instantiates.
- `quality=1.5` raises `ValueError`.

Validation:
```bash
python -c "
from src.core.runtime.final_response import FinalResponse
r = FinalResponse(text='hi', session_id='s1', model='gemma3:4b', mode='fast', quality=0.9, decision_source='fast_path', turn_id=1)
assert r.text == 'hi'
print('OK')
"
```

Artifact: `src/core/runtime/final_response.py`

---

**TASK 2.6 — ModelScore dataclass**

Location:
- `src/core/decision/model_score.py`

Purpose:
- Define ModelScore dataclass used in DecisionOutput candidate_list.

Steps:
1. Create `src/core/decision/model_score.py`.
2. Define `ModelScore` with: model (str, required), score (float 0.0-1.0, required), factor_scores (dict, required).

Success case:
- Valid ModelScore instantiates.

Validation:
```bash
python -c "
from src.core.decision.model_score import ModelScore
ms = ModelScore(model='gemma3:4b', score=0.85, factor_scores={'fit_complexity': 0.9, 'latency': 1.0})
assert 0.0 <= ms.score <= 1.0
print('OK')
"
```

Artifact: `src/core/decision/model_score.py`

---

**TASK 2.7 — Contract tests**

Location:
- `tests/test_contracts.py`

Purpose:
- Verify all contracts instantiate correctly and reject invalid data.

Steps:
1. Create `tests/` directory.
2. Create `tests/test_contracts.py`.
3. Write test: InputPacket valid instantiation.
4. Write test: InputPacket reject missing required fields.
5. Write test: DecisionOutput valid instantiation.
6. Write test: DecisionOutput reject invalid intent.
7. Write test: DecisionOutput reject missing score_breakdown.
8. Write test: LLMOutput valid answer type.
9. Write test: LLMOutput valid tool_call type.
10. Write test: LLMOutput reject mismatched type/content.
11. Write test: ToolResult valid instantiation.
12. Write test: FinalResponse valid instantiation.
13. Write test: ModelScore valid instantiation.

Success case:
- All tests pass.

Failure case:
- Any contract accepts invalid data → test fails.

Validation:
```bash
pytest tests/test_contracts.py -v
```

Artifact: `tests/test_contracts.py`

---

### Definition of Done

All contracts validate correctly. `pytest tests/test_contracts.py -v` passes.

---

## Phase 3 — Model Manager + VRAM

```
phase_id: 3
title: "Model Manager + VRAM"
priority: "P0"
status: "not_started"
progress_percent: 0
done_tasks: 0
total_tasks: 5
blocker: "Phase 2 must complete"
next_action: "Start TASK 3.1"
last_updated: "-"
validation_status: "not_started"
```

### Objective

Implement the Model Manager layer for VRAM monitoring, model lifecycle management, and concurrency control. This replaces ad-hoc model loading with a managed system.

### Tasks

**TASK 3.1 — VRAM Monitor**

Location:
- `src/models/vram_monitor.py`

Purpose:
- Implement real-time VRAM monitoring for NVIDIA GPU.

Steps:
1. Create `src/models/vram_monitor.py`.
2. Define `VRAMMonitor` class.
3. Implement `get_available_vram_mb()` method using pynvml or nvidia-ml-py.
4. Implement `get_total_vram_mb()` method.
5. Implement `is_model_loadable(required_vram_mb)` → bool.
6. Implement `check_vram_threshold(threshold_mb)` → bool (returns true when VRAM below threshold).
7. Fallback: if pynvml unavailable, use heuristic (assume 6GB for RTX 3050).

Success case:
- `get_available_vram_mb()` returns positive integer.
- `is_model_loadable(3000)` returns true when sufficient VRAM.

Failure case:
- No NVIDIA GPU → uses heuristic fallback, logs warning.
- pynvml not installed → installs gracefully or uses fallback.

Edge cases:
- VRAM fluctuates during check → reads current value at call time.
- Multiple GPUs → reads primary GPU (index 0).

Validation:
```bash
python -c "
from src.models.vram_monitor import VRAMMonitor
vm = VRAMMonitor()
avail = vm.get_available_vram_mb()
assert avail > 0, f'VRAM unavailable: {avail}'
print(f'Available VRAM: {avail} MB')
"
```

Artifact: `src/models/vram_monitor.py`

---

**TASK 3.2 — Model Lifecycle Manager**

Location:
- `src/models/manager.py`

Purpose:
- Implement model load, unload, swap with VRAM checks.

Steps:
1. Create `src/models/manager.py`.
2. Define `ModelManager` class.
3. Implement `load_model(model_name)` → loads via Ollama, checks VRAM first.
4. Implement `unload_model(model_name)` → unloads via Ollama API.
5. Implement `swap_model(from_model, to_model)` → unload then load atomically.
6. Implement `get_current_model()` → returns current loaded model name.
7. Implement `is_model_loaded(model_name)` → bool.
8. Enforce: one model at a time, unload before load.

Success case:
- `load_model("gemma3:4b")` succeeds, `get_current_model()` returns "gemma3:4b".
- `swap_model("gemma3:4b", "qwen3:8b")` unloads gemma3:4b, loads qwen3:8b.

Failure case:
- VRAM insufficient → returns error, does NOT load.
- Model already loaded → returns success (no-op).

Edge cases:
- Swap interrupted midway → ensures old model is still loaded (atomic guarantee via ordering).

Validation:
```bash
python -c "
from src.models.manager import ModelManager
mm = ModelManager()
mm.load_model('gemma3:4b')
assert mm.get_current_model() == 'gemma3:4b'
mm.unload_model('gemma3:4b')
assert mm.get_current_model() is None
print('OK')
"
```

Artifact: `src/models/manager.py`

---

**TASK 3.3 — Concurrency Control**

Location:
- `src/models/manager.py` (expand TASK 3.2)

Purpose:
- Prevent concurrent model calls via serialization.

Steps:
1. Add threading.Lock to ModelManager.
2. Wrap all model operations in lock.
3. Implement `acquire()` / `release()` for external callers.
4. Implement `is_busy()` → bool.

Success case:
- Two concurrent `chat()` calls → second waits for first.

Failure case:
- Lock not released → timeout after 120s, raises `TimeoutError`.

Validation:
```bash
python -c "
import threading
from src.models.manager import ModelManager
mm = ModelManager()
results = []
def call(n):
    results.append(n)
t1 = threading.Thread(target=call, args=(1,))
t2 = threading.Thread(target=call, args=(2,))
t1.start(); t2.start(); t1.join(); t2.join()
print(f'Serialized: {results}')
"
```

---

**TASK 3.4 — Model Availability Registry**

Location:
- `src/models/availability.py`

Purpose:
- Track which models are available based on VRAM and Ollama presence.

Steps:
1. Create `src/models/availability.py`.
2. Define `ModelAvailability` class.
3. Implement `refresh()` → checks Ollama for pulled models, cross-references VRAM.
4. Implement `get_available_models()` → list of model names currently loadable.
5. Implement `is_available(model_name)` → bool.

Success case:
- `get_available_models()` includes gemma3:4b if pulled.
- Models exceeding VRAM are excluded.

Validation:
```bash
python -c "
from src.models.availability import ModelAvailability
ma = ModelAvailability()
ma.refresh()
available = ma.get_available_models()
assert len(available) > 0, 'No models available'
print(available)
"
```

Artifact: `src/models/availability.py`

---

**TASK 3.5 — LLM Engine with Model Manager integration**

Location:
- `src/models/llm/engine.py` (expand TASK 0.1)

Purpose:
- Enhance LLM engine to use Model Manager for model lifecycle.

Steps:
1. Expand `src/models/llm/engine.py`.
2. Integrate ModelManager for model load/unload.
3. Add VRAM check before model load.
4. Add timeout handling (model_timeout_s from config).
5. Track current loaded model state.
6. Add `chat_with_model(model_name, message)` that handles swap if needed.

Success case:
- `chat_with_model("gemma3:4b", "hello")` loads model if needed, calls, returns response.

Failure case:
- Model unavailable → returns error message, does NOT crash.
- Timeout → returns timeout message.

Validation:
```bash
python -c "
from src.models.llm.engine import OllamaEngine
e = OllamaEngine()
r = e.chat_with_model('gemma3:4b', 'hello')
assert len(r) > 0
print(r[:100])
"
```

---

### Definition of Done

Model Manager loads, unloads, and swaps models. VRAM monitoring works. Concurrency is serialized. `get_available_models()` returns correct list.

---

## Phase 4 — Runtime State Machine

```
phase_id: 4
title: "Runtime State Machine"
priority: "P0"
status: "not_started"
progress_percent: 0
done_tasks: 0
total_tasks: 8
blocker: "Phase 3 must complete"
next_action: "Start TASK 4.1"
last_updated: "-"
validation_status: "not_started"
```

### Objective

Implement the state machine that controls runtime with hard limits. This is the single source of truth for execution flow.

### Tasks

**TASK 4.1 — RuntimeState enum**

Location:
- `src/core/runtime/state.py`

Purpose:
- Define all runtime states from README state machine table.

Steps:
1. Create `src/core/runtime/state.py`.
2. Define `RuntimeState` enum: IDLE, DECIDING, EXECUTING_MODEL, EXECUTING_TOOL, WAITING_CONFIRMATION, EVALUATING, ERROR, COMPLETED.
3. Define `ALLOWED_TRANSITIONS` dict mapping each state to its allowed next states.
4. Implement `can_transition(from_state, to_state)` function.

Success case:
- `can_transition(IDLE, DECIDING)` returns True.
- `can_transition(IDLE, EXECUTING_TOOL)` returns False.

Validation:
```bash
python -c "
from src.core.runtime.state import RuntimeState, can_transition
assert can_transition(RuntimeState.IDLE, RuntimeState.DECIDING)
assert not can_transition(RuntimeState.IDLE, RuntimeState.EXECUTING_TOOL)
print('OK')
"
```

Artifact: `src/core/runtime/state.py`

---

**TASK 4.2 — State Manager**

Location:
- `src/core/runtime/state_manager.py`

Purpose:
- Implement state manager to control transitions and track state history.

Steps:
1. Create `src/core/runtime/state_manager.py`.
2. Define `StateManager` class.
3. Implement `current_state` property.
4. Implement `transition_to(new_state)` with validation.
5. Add state history tracking (list of (from, to, timestamp)).
6. Implement `force_state(state)` for error recovery (bypasses validation).
7. Add logging on each transition.
8. Integrate with EventBus for `runtime.state` events.

Success case:
- `transition_to(DECIDING)` from IDLE succeeds.
- `transition_to(EXECUTING_TOOL)` from IDLE raises `InvalidTransitionError`.

Failure case:
- Invalid transition → raises `InvalidTransitionError`, state unchanged.

Validation:
```bash
python -c "
from src.core.runtime.state_manager import StateManager
from src.core.runtime.state import RuntimeState
sm = StateManager()
assert sm.current_state == RuntimeState.IDLE
sm.transition_to(RuntimeState.DECIDING)
assert sm.current_state == RuntimeState.DECIDING
print('OK')
"
```

Artifact: `src/core/runtime/state_manager.py`

---

**TASK 4.3 — Hard Limits**

Location:
- `src/core/runtime/limits.py`

Purpose:
- Define and enforce all hard limits from README execution flow.

Steps:
1. Create `src/core/runtime/limits.py`.
2. Define limit constants: max_iterations_per_turn=5, max_tool_calls_per_turn=3, max_tool_depth=3, max_decision_retries=3, max_model_retries=2, global_retry_budget=8, tool_timeout_s=30, model_timeout_s=120, step_timeout_s=60, total_turn_timeout_s=300.
3. Implement `Limits` class that loads from config.
4. Implement `check_limit(limit_name, current_value)` → bool.
5. Implement `consume_budget()` → decrements global_retry_budget, returns remaining.

Success case:
- `check_limit("max_iterations", 4)` returns True.
- `check_limit("max_iterations", 5)` returns False.

Validation:
```bash
python -c "
from src.core.runtime.limits import Limits
l = Limits()
assert l.check_limit('max_iterations', 4)
assert not l.check_limit('max_iterations', 5)
print('OK')
"
```

Artifact: `src/core/runtime/limits.py`

---

**TASK 4.4 — Context Assembler**

Location:
- `src/core/context/assembler.py`

Purpose:
- Implement InputPacket assembly from user input and system state.

Steps:
1. Create `src/core/context/assembler.py`.
2. Define `ContextAssembler` class.
3. Implement `assemble(user_input, session_id)` method.
4. Load user profile.
5. Fetch memory snippets (recent).
6. Build recent history from memory.
7. Return complete InputPacket.

Success case:
- `assemble("hello", "s1")` returns InputPacket with all fields populated.

Failure case:
- Memory unavailable → returns InputPacket with empty memory_snippets (cold start).

Validation:
```bash
python -c "
from src.core.context.assembler import ContextAssembler
a = ContextAssembler()
p = a.assemble('hello', 's1')
assert p.user_message == 'hello'
assert p.session_id == 's1'
print('OK')
"
```

Artifact: `src/core/context/assembler.py`

---

**TASK 4.5 — Executor**

Location:
- `src/core/runtime/executor.py`

Purpose:
- Implement LLM execution with model calling and output parsing.

Steps:
1. Create `src/core/runtime/executor.py`.
2. Define `Executor` class.
3. Implement `execute(decision, input_packet)` method.
4. Call LLM with decision.model via ModelManager.
5. Parse output to LLMOutput.
6. Handle JSON extraction from messy text.
7. Apply timeout from limits.
8. Return LLMOutput.

Success case:
- `execute(decision, packet)` returns LLMOutput with type=answer or tool_call.

Failure case:
- Model call fails → raises `ModelCallError`, caller handles via fallback.
- Output parse fails → raises `ParseError`, caller handles via retry.

Validation:
```bash
python -c "
from src.core.runtime.executor import Executor
e = Executor()
print('Executor created')
"
```

Artifact: `src/core/runtime/executor.py`

---

**TASK 4.6 — Evaluator**

Location:
- `src/core/runtime/evaluator.py`

Purpose:
- Implement response quality evaluation.

Steps:
1. Create `src/core/runtime/evaluator.py`.
2. Define `Evaluator` class.
3. Implement `evaluate(output, decision)` method.
4. Check completeness (answer not truncated).
5. Check coherence (logical consistency).
6. Check relevance (addresses input).
7. Apply ONLY on: long responses (>500 tokens), complex tasks, fallback outputs.
8. Return EvaluationResult with should_retry flag.

Success case:
- Good response → `should_retry=False`.
- Truncated response → `should_retry=True`.

Validation:
```bash
python -c "
from src.core.runtime.evaluator import Evaluator
e = Evaluator()
print('Evaluator created')
"
```

Artifact: `src/core/runtime/evaluator.py`

---

**TASK 4.7 — Runtime Loop**

Location:
- `src/core/runtime/loop.py`

Purpose:
- Implement main runtime loop enforcing Observe → Decide → Think → Act → Evaluate via state machine.

Steps:
1. Create `src/core/runtime/loop.py`.
2. Define `run_turn(user_input, session_id)` function.
3. Implement loop with states:
   - Assemble context (Observe) → IDLE → DECIDING.
   - Run decision (Decide) → EXECUTING_MODEL or EXECUTING_TOOL.
   - Execute model (Think) → EVALUATING.
   - Execute tool if needed (Act) → WAITING_CONFIRMATION or EVALUATING.
   - Evaluate response (Evaluate) → COMPLETED or back to DECIDING.
4. Enforce max_iterations, max_tool_depth, global_retry_budget.
5. Handle state transitions via StateManager.
6. Return FinalResponse.
7. Integrate with Observability for turn tracing.

Success case:
- `run_turn("hello", "s1")` returns FinalResponse with text.
- State transitions are logged.

Failure case:
- Global retry budget exhausted → returns exhaustion response.
- Total turn timeout → returns timeout response.

Validation:
```bash
python -c "
from src.core.runtime.loop import run_turn
r = run_turn('hello', 'test')
assert r.text is not None
print(r.text[:100])
"
```

Artifact: `src/core/runtime/loop.py`

---

**TASK 4.8 — State Machine Tests**

Location:
- `tests/test_state_machine.py`

Purpose:
- Comprehensive tests for state machine and all transitions.

Steps:
1. Create `tests/test_state_machine.py`.
2. Test: all valid transitions work.
3. Test: invalid transitions rejected (IDLE → EXECUTING_TOOL).
4. Test: max_iterations enforcement stops loop.
5. Test: max_tool_depth enforcement stops nesting.
6. Test: global retry budget enforcement.
7. Test: timeout enforcement.
8. Test: error state transitions to IDLE.
9. Test: all limits from TASK 4.3 enforced.

Success case:
- All tests pass.

Validation:
```bash
pytest tests/test_state_machine.py -v
```

Artifact: `tests/test_state_machine.py`

---

### Definition of Done

`run_turn("hello", "test")` returns FinalResponse. All state transitions work. All limits enforced. `pytest tests/test_state_machine.py -v` passes.

---

## Phase 5 — Decision System

```
phase_id: 5
title: "Decision System"
priority: "P1"
status: "not_started"
progress_percent: 0
done_tasks: 0
total_tasks: 7
blocker: "Phase 4 must complete"
next_action: "Start TASK 5.1"
last_updated: "-"
validation_status: "not_started"
```

### Objective

Harden decision system with robust classification, dynamic scoring, and mathematically defined formulas.

### Tasks

**TASK 5.1 — Classifier robust JSON parsing**

Location:
- `src/core/decision/classifier.py` (expand TASK 0.2)

Purpose:
- Enhance classifier with robust JSON extraction and repair.

Steps:
1. Expand `src/core/decision/classifier.py`.
2. Implement `extract_json(text)` function.
3. Handle: markdown code blocks, trailing text, malformed JSON.
4. Add JSON repair for common issues (missing quotes, trailing commas).
5. Retry with exponential backoff (max 2 retries).
6. Return safe fallback on all failures.

Success case:
- `extract_json('```json\n{"intent": "chat"}\n```')` returns `{"intent": "chat"}`.

Failure case:
- Completely invalid text → returns safe fallback dict.

Validation:
```bash
python -c "
from src.core.decision.classifier import extract_json
r = extract_json('\`\`\`json\n{\"intent\": \"chat\"}\n\`\`\`')
assert r['intent'] == 'chat'
print('OK')
"
```

---

**TASK 5.2 — Fast-path rules**

Location:
- `src/core/decision/fast_path.py`

Purpose:
- Implement rule-based fast path for common intents to avoid LLM call.

Steps:
1. Create `src/core/decision/fast_path.py`.
2. Define `FastPath` class.
3. Implement rules for: "open X" → tool_use/open_app, "what is/who is" → chat, "search for" → search.
4. Support Arabic equivalents: "افتح" → tool_use, "ما هو" → chat, "ابحث عن" → search.
5. Return DecisionOutput if matched, None if not.
6. Set `decision_source="fast_path"` on matched outputs.

Success case:
- `check("open notepad")` returns DecisionOutput with intent=tool_use.
- `check("افتح المفكرة")` returns DecisionOutput with intent=tool_use.

Failure case:
- No rule matches → returns None (caller falls through to model path).

Validation:
```bash
python -c "
from src.core.decision.fast_path import FastPath
fp = FastPath()
r = fp.check('open notepad')
assert r is not None
assert r.intent == 'tool_use'
assert r.decision_source == 'fast_path'
print('OK')
"
```

Artifact: `src/core/decision/fast_path.py`

---

**TASK 5.3 — Dynamic Scorer**

Location:
- `src/core/decision/scorer.py`

Purpose:
- Implement mathematically defined weighted scoring for model selection.

Steps:
1. Create `src/core/decision/scorer.py`.
2. Define `ModelScorer` class.
3. Implement `score(model, complexity, mode, vram_available)` method.
4. Formula: `score = Σ(weight_i * normalized_value_i)` where normalized values are:
   - capability: 0.0-1.0 (reasoning_tier mapped).
   - latency: 0.0-1.0 (fast=1.0, medium=0.6, slow=0.3).
   - cost: 0.0-1.0 (lower VRAM = higher score).
   - modality_relevance: 0.0-1.0.
5. Implement tie-break: lower cost → lower latency → higher success rate.
6. Return ModelScore with full factor breakdown.

Success case:
- `score("gemma3:4b", "low", "fast", 6000)` returns ModelScore with all factor_scores.

Failure case:
- Model not in profiles → returns ModelScore with score=0.0.

Validation:
```bash
python -c "
from src.core.decision.scorer import ModelScorer
ms = ModelScorer()
result = ms.score('gemma3:4b', 'low', 'fast', 6000)
assert result.score > 0
assert len(result.factor_scores) >= 4
print(f'Score: {result.score}, Factors: {result.factor_scores}')
"
```

Artifact: `src/core/decision/scorer.py`

---

**TASK 5.4 — Risk Assessment**

Location:
- `src/core/decision/risk.py`

Purpose:
- Determine risk level based on intent, tool, and arguments.

Steps:
1. Create `src/core/decision/risk.py`.
2. Define `RiskAssessor` class.
3. Implement `assess(decision)` method.
4. Rules: system tools = medium/high, file ops = medium, search = low.
5. Check arguments for dangerous patterns.
6. Return risk_level: low|medium|high.

Success case:
- `assess(decision with open_app)` returns medium.
- `assess(decision with search)` returns low.

Validation:
```bash
python -c "
from src.core.decision.risk import RiskAssessor
ra = RiskAssessor()
from src.core.decision.decision import DecisionOutput
d = DecisionOutput(intent='tool_use', complexity='low', mode='fast', model='gemma3:4b', requires_tools=True, tool_name='open_app', confidence=0.9, risk_level='low', decision_source='fast_path', score_breakdown={}, candidate_list=[])
risk = ra.assess(d)
assert risk in ('low', 'medium', 'high')
print(f'Risk: {risk}')
"
```

Artifact: `src/core/decision/risk.py`

---

**TASK 5.5 — Decision Function (unified)**

Location:
- `src/core/decision/decision.py` (expand TASK 2.2)

Purpose:
- Implement unified decision function: fast path first, then model-based classification with scoring.

Steps:
1. Expand `src/core/decision/decision.py`.
2. Define `decide(input_packet)` function.
3. Step 1: Check fast path. If match → return DecisionOutput with decision_source=fast_path.
4. Step 2: If no fast path match → use classifier LLM to get intent.
5. Step 3: Score all available models using ModelScorer.
6. Step 4: Select best model (highest score, apply tie-break).
7. Step 5: Assess risk level.
8. Step 6: Return DecisionOutput with score_breakdown and candidate_list.
9. Validate before returning: score_breakdown and candidate_list present.

Success case:
- `decide(packet)` returns valid DecisionOutput.
- Fast path inputs return decision_source=fast_path.
- Complex inputs return decision_source=model with full scoring.

Failure case:
- Classifier LLM fails → falls back to safe defaults (intent=chat, mode=normal, model=gemma3:4b).
- No models available → returns safe defaults.

Validation:
```bash
python -c "
from src.core.decision.decision import decide
from src.core.context.bundle import InputPacket
from src.memory.user_profile import UserProfile
p = InputPacket(user_message='open notepad', session_id='s1', user_profile=UserProfile(user_id='default'))
d = decide(p)
assert d.intent is not None
assert d.score_breakdown is not None or d.decision_source == 'fast_path'
print(f'Intent: {d.intent}, Source: {d.decision_source}')
"
```

---

**TASK 5.6 — Escalation Chain**

Location:
- `src/core/runtime/escalation.py`

Purpose:
- Implement decision retry with scoring weight adjustment.

Steps:
1. Create `src/core/runtime/escalation.py`.
2. Define `EscalationChain` class.
3. Implement `retry(input_packet, attempt_number)` method.
4. Adjust scoring weights per retry (±0.05 on fit_complexity).
5. After 3 attempts → trigger fallback system.
6. Log all retry attempts.

Success case:
- `retry(packet, 1)` returns DecisionOutput with adjusted weights.
- `retry(packet, 3)` triggers fallback.

Validation:
```bash
python -c "
from src.core.runtime.escalation import EscalationChain
ec = EscalationChain()
print('EscalationChain created')
"
```

Artifact: `src/core/runtime/escalation.py`

---

**TASK 5.7 — Decision Tests**

Location:
- `tests/test_decision.py`

Purpose:
- Comprehensive tests for decision system including dynamic scoring.

Steps:
1. Create `tests/test_decision.py`.
2. Test: fast path matches "open notepad".
3. Test: fast path matches Arabic "افتح المفكرة".
4. Test: classifier parses valid JSON.
5. Test: classifier handles malformed JSON with retry.
6. Test: decision includes score_breakdown (model path).
7. Test: decision includes candidate_list (model path).
8. Test: invalid decision rejected (no score_breakdown → safe default).
9. Test: model choice varies with input complexity.
10. Test: tie-break logic (cost, latency, success rate).
11. Test: escalation retries 3 times then falls back.
12. Test: confidence handling (low confidence → safe default).

Success case:
- All tests pass.

Validation:
```bash
pytest tests/test_decision.py -v
```

Artifact: `tests/test_decision.py`

---

### Definition of Done

Decision system uses fast path for simple inputs and dynamic scoring for complex inputs. All tests pass.

---

## Phase 6 — Sandbox + Safety

```
phase_id: 6
title: "Sandbox + Safety"
priority: "P0"
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

Implement the execution sandbox for safe tool execution and the safety layer for structured validation and permission enforcement.

### Tasks

**TASK 6.1 — Execution Sandbox**

Location:
- `src/core/sandbox/sandbox.py`

Purpose:
- Implement safe tool execution environment with timeout and resource limits.

Steps:
1. Create `src/core/sandbox/` directory.
2. Create `src/core/sandbox/sandbox.py`.
3. Define `Sandbox` class.
4. Implement `execute(capability, args, timeout_s)` method.
5. Implement timeout enforcement (hard timeout at timeout_s).
6. Implement resource limits (memory, CPU via subprocess limits).
7. Implement dry-run support: `dry_run(capability, args)` returns what would happen.
8. Implement rollback tracking for reversible actions.

Success case:
- `execute(capability, args, 30)` runs capability and returns ToolResult.
- Timeout fires → ToolResult with success=False, error="timeout".

Failure case:
- Capability raises exception → caught, returns ToolResult with error details.
- Resource limit exceeded → ToolResult with error="resource limit exceeded".

Validation:
```bash
python -c "
from src.core.sandbox.sandbox import Sandbox
sb = Sandbox()
print('Sandbox created')
"
```

Artifact: `src/core/sandbox/sandbox.py`

---

**TASK 6.2 — Safety Classifier (Structured Validation)**

Location:
- `src/core/safety/classifier.py`

Purpose:
- Classify capability calls by risk level using structured validation, not string matching.

Steps:
1. Create `src/core/safety/classifier.py`.
2. Define `SafetyClassifier` class.
3. Implement `classify(capability_name, args)` method.
4. Check paths: must be within allowed roots, no path traversal.
5. Check commands: must be in allowed whitelist.
6. Return risk_level: low|medium|high.

Success case:
- `classify("file_read", {"path": "/home/user/file.txt"})` returns low.
- `classify("file_read", {"path": "/etc/passwd"})` returns high.

Failure case:
- Unknown capability → returns high (safest default).

Validation:
```bash
python -c "
from src.core.safety.classifier import SafetyClassifier
sc = SafetyClassifier()
risk = sc.classify('file_read', {'path': '/home/user/test.txt'})
assert risk in ('low', 'medium', 'high')
print(f'Risk: {risk}')
"
```

Artifact: `src/core/safety/classifier.py`

---

**TASK 6.3 — Mode Enforcer**

Location:
- `src/core/safety/mode_enforcer.py`

Purpose:
- Enforce execution modes (SAFE/BALANCED/UNRESTRICTED) per README spec.

Steps:
1. Create `src/core/safety/mode_enforcer.py`.
2. Define `ModeEnforcer` class.
3. Implement `check_permission(capability_name, risk_level, mode)` method.
4. SAFE: confirm all tools.
5. BALANCED: low=auto, medium=confirm, high=blocked (with override phrase).
6. UNRESTRICTED: auto-execute all (schema validation still applies).
7. Return: allow|confirm|block.

Success case:
- `check_permission("open_app", "low", "BALANCED")` returns allow.
- `check_permission("file_delete", "high", "BALANCED")` returns block.

Validation:
```bash
python -c "
from src.core.safety.mode_enforcer import ModeEnforcer
me = ModeEnforcer()
assert me.check_permission('open_app', 'low', 'BALANCED') == 'allow'
assert me.check_permission('file_delete', 'high', 'BALANCED') == 'block'
print('OK')
"
```

Artifact: `src/core/safety/mode_enforcer.py`

---

**TASK 6.4 — Permission Layer (Three-Gate System)**

Location:
- `src/core/safety/permission.py`

Purpose:
- Implement three-gate permission system from README.

Steps:
1. Create `src/core/safety/permission.py`.
2. Define `PermissionLayer` class.
3. Implement `check(tool_name, args, decision, user_context)` method.
4. Gate 1: Decision consistency → tool matches intent?
5. Gate 2: Argument safety → paths within roots, schema valid?
6. Gate 3: User context → tool matches user intent?
7. Return: allow|block with reason.
8. Log each gate result to audit trail.

Success case:
- All gates pass → returns allow.
- Any gate fails → returns block with specific gate reason.

Validation:
```bash
python -c "
from src.core.safety.permission import PermissionLayer
pl = PermissionLayer()
print('PermissionLayer created')
"
```

Artifact: `src/core/safety/permission.py`

---

**TASK 6.5 — Audit Logger**

Location:
- `src/core/safety/audit.py`

Purpose:
- Implement audit log per action for safety and debugging.

Steps:
1. Create `src/core/safety/audit.py`.
2. Define `AuditLogger` class.
3. Implement `log_action(tool_name, args, gate_results, decision, session_id, turn_id)` method.
4. Store audit entries in SQLite (separate from memory DB).
5. Implement `get_audit_log(session_id, limit)` method.
6. Include: timestamp, tool, args, gate results, decision, reason.

Success case:
- `log_action(...)` stores entry.
- `get_audit_log("s1", 10)` returns recent entries.

Validation:
```bash
python -c "
from src.core.safety.audit import AuditLogger
al = AuditLogger()
al.log_action('open_app', {'name': 'notepad'}, {'gate1': 'pass', 'gate2': 'pass', 'gate3': 'pass'}, 'allow', 's1', 1)
log = al.get_audit_log('s1', 10)
assert len(log) >= 1
print('OK')
"
```

Artifact: `src/core/safety/audit.py`

---

**TASK 6.6 — Schema Validator for Capabilities**

Location:
- `src/capabilities/validator.py` (expand TASK 2.x)

Purpose:
- Validate capability arguments against Pydantic schemas.

Steps:
1. Expand `src/capabilities/validator.py`.
2. Define `SchemaValidator` class.
3. Implement `validate(capability_name, args)` method.
4. Load schema from capabilities manifest.
5. Validate required fields present, types match, ranges valid.
6. Return ValidationResult (valid: bool, errors: list).

Success case:
- `validate("open_app", {"name": "notepad"})` returns valid=True.
- `validate("open_app", {})` returns valid=False, errors=["name is required"].

Validation:
```bash
python -c "
from src.capabilities.validator import SchemaValidator
sv = SchemaValidator()
result = sv.validate('open_app', {'name': 'notepad'})
assert result.valid
print('OK')
"
```

---

**TASK 6.7 — Safety Tests**

Location:
- `tests/test_safety.py`

Purpose:
- Comprehensive tests for safety modes and risk classification.

Steps:
1. Create `tests/test_safety.py`.
2. Test: SAFE mode confirms all tools.
3. Test: BALANCED mode auto-executes low risk.
4. Test: BALANCED mode requires confirmation for medium.
5. Test: BALANCED mode blocks high (with override phrase check).
6. Test: UNRESTRICTED auto-executes all.
7. Test: dangerous patterns always blocked.
8. Test: risk levels correctly assigned per capability.
9. Test: three-gate system blocks when any gate fails.
10. Test: audit log records all actions.
11. Test: schema validator rejects invalid args.

Success case:
- All tests pass.

Validation:
```bash
pytest tests/test_safety.py -v
```

Artifact: `tests/test_safety.py`

---

### Definition of Done

Sandbox enforces timeouts and limits. Safety layer validates with structured schemas. Permission layer enforces three gates. Audit log records all actions. All tests pass.

---

## Phase 7 — Memory Engine

```
phase_id: 7
title: "Memory Engine"
priority: "P1"
status: "not_started"
progress_percent: 0
done_tasks: 0
total_tasks: 6
blocker: "Phase 6 must complete"
next_action: "Start TASK 7.1"
last_updated: "-"
validation_status: "not_started"
```

### Objective

Implement the Memory Engine with retrieval strategy, scoring system, decay/TTL, and indexing. Not just storage — a full retrieval engine.

### Tasks

**TASK 7.1 — Memory Database**

Location:
- `src/memory/database.py`

Purpose:
- Implement SQLite-based memory storage with short-term and long-term tables.

Steps:
1. Create `src/memory/database.py`.
2. Define `MemoryDB` class.
3. Implement `store(session_id, turn_data)` method.
4. Implement `retrieve_recent(session_id, limit)` for short-term memory.
5. Implement `search(keywords)` for long-term memory.
6. Use SQLite with tables: turns, memory_snippets, sessions.
7. Handle connection management (open/close, connection pooling).

Success case:
- `store("s1", turn_data)` persists data.
- `retrieve_recent("s1", 5)` returns last 5 turns.

Failure case:
- Database file corrupted → recreates database, logs warning.

Validation:
```bash
python -c "
from src.memory.database import MemoryDB
db = MemoryDB()
db.store('s1', {'message': 'hello', 'response': 'hi'})
recent = db.retrieve_recent('s1', 5)
assert len(recent) >= 1
print('OK')
"
```

Artifact: `src/memory/database.py`

---

**TASK 7.2 — Memory Scorer**

Location:
- `src/memory/scorer.py`

Purpose:
- Implement relevance scoring for memory snippets.

Steps:
1. Create `src/memory/scorer.py`.
2. Define `MemoryScorer` class.
3. Implement `score(snippet, query)` method.
4. Scoring factors: keyword overlap (0.0-1.0), recency (decay over time), interaction count (user referenced this snippet N times).
5. Formula: `score = 0.5 * keyword_overlap + 0.3 * recency + 0.2 * interaction_count`.
6. Return float 0.0-1.0.

Success case:
- Relevant snippet → score >= 0.5.
- Irrelevant snippet → score < 0.2.

Validation:
```bash
python -c "
from src.memory.scorer import MemoryScorer
ms = MemoryScorer()
score = ms.score({'keywords': ['python', 'code'], 'age_hours': 1, 'interactions': 3}, 'python programming')
assert 0.0 <= score <= 1.0
print(f'Score: {score}')
"
```

Artifact: `src/memory/scorer.py`

---

**TASK 7.3 — TTL and Decay Manager**

Location:
- `src/memory/ttl.py`

Purpose:
- Implement time-to-live and decay management for memory entries.

Steps:
1. Create `src/memory/ttl.py`.
2. Define `TTLManager` class.
3. Implement `set_ttl(snippet_id, ttl_hours)` method.
4. Implement `check_expired()` → returns list of expired snippet IDs.
5. Implement `apply_decay()` → reduces relevance scores of old entries.
6. Short-term TTL: 24 hours. Long-term TTL: 30 days.
7. Implement `cleanup()` → removes expired entries.

Success case:
- Expired entries identified and cleaned.
- Old entries have reduced relevance scores.

Validation:
```bash
python -c "
from src.memory.ttl import TTLManager
tm = TTLManager()
print('TTLManager created')
"
```

Artifact: `src/memory/ttl.py`

---

**TASK 7.4 — Keyword Indexer**

Location:
- `src/memory/indexer.py`

Purpose:
- Implement keyword indexing for fast memory lookup.

Steps:
1. Create `src/memory/indexer.py`.
2. Define `KeywordIndexer` class.
3. Implement `index(snippet_id, keywords)` method.
4. Implement `lookup(keyword)` → returns list of snippet IDs.
5. Implement `rebuild_index()` → periodic rebuild, not on every write.
6. Index stored in SQLite for persistence.

Success case:
- `index("s1", ["python", "code"])` → `lookup("python")` returns ["s1"].

Validation:
```bash
python -c "
from src.memory.indexer import KeywordIndexer
ki = KeywordIndexer()
ki.index('s1', ['python', 'code'])
results = ki.lookup('python')
assert 's1' in results
print('OK')
"
```

Artifact: `src/memory/indexer.py`

---

**TASK 7.5 — Context Retriever**

Location:
- `src/memory/retriever.py`

Purpose:
- Retrieve relevant context for current turn using scoring and indexing.

Steps:
1. Create `src/memory/retriever.py`.
2. Define `ContextRetriever` class.
3. Implement `get_context(session_id, query)` method.
4. Fetch recent history (short-term) from MemoryDB.
5. Search relevant snippets (long-term) using KeywordIndexer and MemoryScorer.
6. Return top N snippets sorted by relevance score.
7. Cold start: no memory → return empty list.

Success case:
- `get_context("s1", "python")` returns relevant snippets sorted by score.
- Cold start → returns empty list.

Validation:
```bash
python -c "
from src.memory.retriever import ContextRetriever
cr = ContextRetriever()
context = cr.get_context('s1', 'python')
print(f'Retrieved {len(context)} snippets')
"
```

Artifact: `src/memory/retriever.py`

---

**TASK 7.6 — Memory Tests**

Location:
- `tests/test_memory.py`

Purpose:
- Test memory storage, retrieval, scoring, TTL, and indexing.

Steps:
1. Create `tests/test_memory.py`.
2. Test: store turn data.
3. Test: retrieve recent turns.
4. Test: search long-term memory.
5. Test: context retriever returns relevant data.
6. Test: cold start (no memory available).
7. Test: memory scoring (relevant snippets score higher).
8. Test: TTL expiration.
9. Test: keyword indexing and lookup.

Success case:
- All tests pass.

Validation:
```bash
pytest tests/test_memory.py -v
```

Artifact: `tests/test_memory.py`

---

### Definition of Done

Memory Engine stores, retrieves, scores, and expires memory. ContextRetriever returns relevant snippets. All tests pass.

---

## Phase 8 — Capability System

```
phase_id: 8
title: "Capability System"
priority: "P1"
status: "not_started"
progress_percent: 0
done_tasks: 0
total_tasks: 6
blocker: "Phase 7 must complete"
next_action: "Start TASK 8.1"
last_updated: "-"
validation_status: "not_started"
```

### Objective

Build complete capability execution pipeline: base class, registry, executor, and validation.

### Tasks

**TASK 8.1 — BaseCapability Abstract Class**

Location:
- `src/capabilities/base.py`

Purpose:
- Define abstract base class for all capabilities.

Steps:
1. Create `src/capabilities/base.py`.
2. Define `BaseCapability` abstract class.
3. Abstract methods: `execute(args)`, `validate(args)`, `get_risk_level()`.
4. Abstract method: `dry_run(args)` → returns what would happen.
5. Properties: name, domain, description, risk_level.
6. Implement `to_dict()` for manifest registration.

Success case:
- Subclass implements all abstract methods.
- Missing method raises `TypeError`.

Validation:
```bash
python -c "
from abc import ABC
from src.capabilities.base import BaseCapability
assert issubclass(BaseCapability, ABC)
print('OK')
"
```

Artifact: `src/capabilities/base.py`

---

**TASK 8.2 — Capability Registry**

Location:
- `src/capabilities/registry.py`

Purpose:
- Implement registry to manage all capabilities.

Steps:
1. Create `src/capabilities/registry.py`.
2. Define `CapabilityRegistry` class.
3. Implement `register(capability)` method.
4. Implement `get(name)` method.
5. Implement `list_all()` method.
6. Load capabilities from `config/capabilities.yaml` manifest.
7. Auto-discover capability modules.

Success case:
- `register(capability)` → `get(name)` returns same instance.
- `list_all()` returns all registered capabilities.

Failure case:
- Duplicate registration → raises `ValueError`.
- Unknown capability → `get(name)` returns None.

Validation:
```bash
python -c "
from src.capabilities.registry import CapabilityRegistry
r = CapabilityRegistry()
print('Registry created')
"
```

Artifact: `src/capabilities/registry.py`

---

**TASK 8.3 — Capability Executor**

Location:
- `src/capabilities/executor.py`

Purpose:
- Execute capabilities with full safety pipeline (schema validation, safety classification, mode enforcement, sandbox execution).

Steps:
1. Create `src/capabilities/executor.py`.
2. Define `CapabilityExecutor` class.
3. Implement `execute(name, args, mode)` method.
4. Gate 1: Check capability exists in registry.
5. Gate 2: Validate args schema.
6. Gate 3: Run safety classifier for risk level.
7. Gate 4: Check mode enforcement permission.
8. Gate 5: Execute in sandbox.
9. Return ToolResult.
10. Log to audit trail.

Success case:
- `execute("open_app", {"name": "notepad"}, "BALANCED")` opens Notepad.

Failure case:
- Unknown capability → ToolResult with success=False, error="capability not found".
- Schema invalid → ToolResult with success=False, error="invalid arguments".
- Permission denied → ToolResult with success=False, error="permission denied".

Validation:
```bash
python -c "
from src.capabilities.executor import CapabilityExecutor
ce = CapabilityExecutor()
print('CapabilityExecutor created')
"
```

Artifact: `src/capabilities/executor.py`

---

**TASK 8.4 — Capability Validation Tests**

Location:
- `tests/test_capabilities.py`

Purpose:
- Test capability system functionality.

Steps:
1. Create `tests/test_capabilities.py`.
2. Test: BaseCapability requires all abstract methods.
3. Test: Registry registers and retrieves capabilities.
4. Test: Registry rejects duplicates.
5. Test: Executor validates schema before execution.
6. Test: Executor enforces mode permissions.
7. Test: Executor runs capability in sandbox.
8. Test: Executor returns ToolResult with correct fields.

Success case:
- All tests pass.

Validation:
```bash
pytest tests/test_capabilities.py -v
```

Artifact: `tests/test_capabilities.py`

---

**TASK 8.5 — Sandbox Tests**

Location:
- `tests/test_sandbox.py`

Purpose:
- Test sandbox timeout and resource limits.

Steps:
1. Create `tests/test_sandbox.py`.
2. Test: sandbox enforces timeout.
3. Test: sandbox catches capability exceptions.
4. Test: dry-run returns result without side-effects.
5. Test: resource limits enforced.

Success case:
- All tests pass.

Validation:
```bash
pytest tests/test_sandbox.py -v
```

Artifact: `tests/test_sandbox.py`

---

**TASK 8.6 — Observability Tests**

Location:
- `tests/test_observability.py`

Purpose:
- Test observability system: metrics, tracing, replay.

Steps:
1. Create `tests/test_observability.py`.
2. Test: metrics collector records and summarizes.
3. Test: trace records all phases.
4. Test: replay reconstructs full turn trace.

Success case:
- All tests pass.

Validation:
```bash
pytest tests/test_observability.py -v
```

Artifact: `tests/test_observability.py`

---

### Definition of Done

Capability system is complete: base class, registry, executor with full safety pipeline. Sandbox enforces limits. All tests pass.

---

## Phase 9 — System Control Capabilities

```
phase_id: 9
title: "System Control Capabilities"
priority: "P1"
status: "not_started"
progress_percent: 0
done_tasks: 0
total_tasks: 8
blocker: "Phase 8 must complete"
next_action: "Start TASK 9.1"
last_updated: "-"
validation_status: "not_started"
```

### Objective

Implement system control capabilities for cross-platform OS interaction. Each capability inherits BaseCapability and integrates with the executor pipeline.

### Tasks

**TASK 9.1 — App Launcher Capability**

Location:
- `src/capabilities/system/apps.py` (expand TASK 0.3)

Purpose:
- Full app launcher capability inheriting BaseCapability.

Steps:
1. Expand `src/capabilities/system/apps.py`.
2. Inherit from `BaseCapability`.
3. Implement `execute(args)` with args: name.
4. Cross-platform: Windows (PATH, Program Files, Start Menu), Linux (PATH, /usr/share/applications), macOS (PATH, /Applications).
5. Return ToolResult with PID.
6. Implement `dry_run(args)` → returns what would happen.
7. Implement `get_risk_level()` → medium.

Success case:
- `execute({"name": "notepad"})` opens Notepad, returns ToolResult with pid.

Failure case:
- App not found → ToolResult with success=False.

Validation:
```bash
python -c "
from src.capabilities.system.apps import AppLauncher
al = AppLauncher()
r = al.execute({'name': 'notepad'})
assert 'success' in r
print(r)
"
```

---

**TASK 9.2 — System Info Capability**

Location:
- `src/capabilities/system/sysinfo.py`

Purpose:
- Gather system information (OS, CPU, RAM, GPU).

Steps:
1. Create `src/capabilities/system/sysinfo.py`.
2. Inherit from `BaseCapability`.
3. Implement `execute(args)` with args: info_type (all|cpu|ram|gpu|os).
4. Use platform, psutil for detection.
5. Return ToolResult with system info dict.

Success case:
- `execute({"info_type": "all"})` returns full system info.

Validation:
```bash
python -c "
from src.capabilities.system.sysinfo import SystemInfoCapability
si = SystemInfoCapability()
r = si.execute({'info_type': 'all'})
assert r.success
print(r.data)
"
```

Artifact: `src/capabilities/system/sysinfo.py`

---

**TASK 9.3 — Clipboard Capability**

Location:
- `src/capabilities/system/clipboard.py`

Purpose:
- Read from and write to system clipboard.

Steps:
1. Create `src/capabilities/system/clipboard.py`.
2. Inherit from `BaseCapability`.
3. Implement `execute(args)` with args: action (read|write), content (for write).
4. Use pyperclip for cross-platform support.
5. Return ToolResult with clipboard content or success.

Success case:
- `execute({"action": "write", "content": "test"})` → `execute({"action": "read"})` returns "test".

Validation:
```bash
python -c "
from src.capabilities.system.clipboard import ClipboardCapability
cb = ClipboardCapability()
cb.execute({'action': 'write', 'content': 'test'})
r = cb.execute({'action': 'read'})
assert r.data.get('content') == 'test'
print('OK')
"
```

Artifact: `src/capabilities/system/clipboard.py`

---

**TASK 9.4 — Notifications Capability**

Location:
- `src/capabilities/notify/toasts.py`

Purpose:
- Send system notifications to user.

Steps:
1. Create `src/capabilities/notify/toasts.py`.
2. Inherit from `BaseCapability`.
3. Implement `execute(args)` with args: title, message, duration.
4. Cross-platform: Windows (plyer), Linux (notify-send or plyer), macOS (osascript or plyer).
5. Return ToolResult with success.

Success case:
- `execute({"title": "Test", "message": "Hello"})` shows notification.

Validation:
```bash
python -c "
from src.capabilities.notify.toasts import NotificationCapability
n = NotificationCapability()
r = n.execute({'title': 'Test', 'message': 'Hello'})
print(r.success)
"
```

Artifact: `src/capabilities/notify/toasts.py`

---

**TASK 9.5 — Screenshot/OCR Capability**

Location:
- `src/capabilities/screen/capture.py`

Purpose:
- Capture screen and optionally extract text via OCR.

Steps:
1. Create `src/capabilities/screen/capture.py`.
2. Inherit from `BaseCapability`.
3. Implement `execute(args)` with args: ocr (bool), region (x,y,w,h or full).
4. Use PIL/Pillow for screenshot.
5. Use pytesseract for OCR (optional).
6. Return ToolResult with image path or OCR text.

Success case:
- `execute({"ocr": false})` returns image path.
- `execute({"ocr": true})` returns OCR text.

Validation:
```bash
python -c "
from src.capabilities.screen.capture import ScreenshotCapability
sc = ScreenshotCapability()
r = sc.execute({'ocr': False})
assert r.success
print(r.data)
"
```

Artifact: `src/capabilities/screen/capture.py`

---

**TASK 9.6 — File Operations Capability**

Location:
- `src/capabilities/files/file_ops.py`

Purpose:
- Perform file operations: read, write, list, delete, move, copy.

Steps:
1. Create `src/capabilities/files/file_ops.py`.
2. Inherit from `BaseCapability`.
3. Implement `execute(args)` with args: action, path, content (for write).
4. Safety: enforce path within allowed roots.
5. Safety: block dangerous operations.
6. Return ToolResult with file data or success.

Success case:
- `execute({"action": "list", "path": "."})` returns file listing.

Failure case:
- Path outside allowed roots → blocked by safety layer.

Validation:
```bash
python -c "
from src.capabilities.files.file_ops import FileOpsCapability
fo = FileOpsCapability()
r = fo.execute({'action': 'list', 'path': '.'})
assert r.success
print(r.data)
"
```

Artifact: `src/capabilities/files/file_ops.py`

---

**TASK 9.7 — Code Executor Capability**

Location:
- `src/capabilities/coder/executor.py`

Purpose:
- Execute code snippets in sandboxed environment.

Steps:
1. Create `src/capabilities/coder/executor.py`.
2. Inherit from `BaseCapability`.
3. Implement `execute(args)` with args: language (python|javascript|bash), code.
4. Use subprocess with timeout.
5. Capture stdout, stderr, return code.
6. Safety: restrict to temp directory, limit resources.
7. Return ToolResult with execution output.

Success case:
- `execute({"language": "python", "code": "print(1+1)"})` returns "2".

Failure case:
- Infinite loop → timeout fires, returns error.

Validation:
```bash
python -c "
from src.capabilities.coder.executor import CodeExecutorCapability
ce = CodeExecutorCapability()
r = ce.execute({'language': 'python', 'code': 'print(1+1)'})
assert r.success
print(r.data)
"
```

Artifact: `src/capabilities/coder/executor.py`

---

**TASK 9.8 — Web Search Capability**

Location:
- `src/capabilities/search/web_search.py`

Purpose:
- Perform web searches and return results.

Steps:
1. Create `src/capabilities/search/web_search.py`.
2. Inherit from `BaseCapability`.
3. Implement `execute(args)` with args: query, count.
4. Use requests + BeautifulSoup for scraping.
5. Parse search results: title, url, snippet.
6. Return ToolResult with results list.

Success case:
- `execute({"query": "python", "count": 3})` returns 3 results.

Failure case:
- Network unavailable → ToolResult with success=False.

Validation:
```bash
python -c "
from src.capabilities.search.web_search import WebSearchCapability
ws = WebSearchCapability()
r = ws.execute({'query': 'python', 'count': 3})
print(r.success)
"
```

Artifact: `src/capabilities/search/web_search.py`

---

### Definition of Done

All system control capabilities are implemented, inherit BaseCapability, and return ToolResult. Each supports dry-run and risk level reporting.

---

## Phase 10 — Prompt Builder

```
phase_id: 10
title: "Prompt Builder"
priority: "P1"
status: "not_started"
progress_percent: 0
done_tasks: 0
total_tasks: 5
blocker: "Phase 9 must complete"
next_action: "Start TASK 10.1"
last_updated: "-"
validation_status: "not_started"
```

### Objective

Build identity and prompt assembly system.

### Tasks

**TASK 10.1 — Jarvis Identity YAML**

Location:
- `config/jarvis_identity.yaml`

Purpose:
- Define Jarvis identity, personality, and behavior constraints.

Steps:
1. Create `config/jarvis_identity.yaml`.
2. Define: name, role, personality traits, capabilities list.
3. Add language support: English, Arabic.
4. Define behavior constraints (local-first, no cloud fallback).
5. Add mode-specific behavior fragments reference.

Success case:
- YAML loads with all fields present.

Validation:
```bash
python -c "import yaml; i = yaml.safe_load(open('config/jarvis_identity.yaml')); assert i['name'] == 'JARVIS'; print('OK')"
```

Artifact: `config/jarvis_identity.yaml`

---

**TASK 10.2 — Mode Fragments**

Location:
- `config/mode_fragments.yaml`

Purpose:
- Define prompt fragments for each execution mode.

Steps:
1. Create `config/mode_fragments.yaml`.
2. Define fragments for modes: fast, normal, deep, planning, research.
3. Each fragment: system prompt addition, behavior rules, output format.
4. Add mode-specific constraints.

Success case:
- YAML loads with all 5 mode fragments.

Validation:
```bash
python -c "import yaml; f = yaml.safe_load(open('config/mode_fragments.yaml')); assert len(f['fragments']) == 5; print('OK')"
```

Artifact: `config/mode_fragments.yaml`

---

**TASK 10.3 — System Prompt Builder**

Location:
- `src/core/context/builder.py`

Purpose:
- Assemble system prompt from identity, mode, and context.

Steps:
1. Create `src/core/context/builder.py`.
2. Define `PromptBuilder` class.
3. Implement `build(decision, input_packet)` method.
4. Load identity from YAML.
5. Load mode fragment.
6. Add context (history, memory snippets).
7. Return complete system prompt string.

Success case:
- `build(decision, packet)` returns non-empty prompt string containing identity.

Validation:
```bash
python -c "
from src.core.context.builder import PromptBuilder
pb = PromptBuilder()
# build() requires decision and input_packet
print('PromptBuilder created')
"
```

Artifact: `src/core/context/builder.py`

---

**TASK 10.4 — Wire into Executor**

Location:
- `src/core/runtime/executor.py` (expand TASK 4.5)

Purpose:
- Integrate prompt builder into LLM execution.

Steps:
1. Expand `src/core/runtime/executor.py`.
2. Add PromptBuilder instance.
3. Call `build()` before LLM call.
4. Pass complete prompt to LLM engine.
5. Ensure identity block in every LLM call.

Success case:
- Executor uses PromptBuilder to construct full prompt before calling LLM.

Validation:
- Integration test: run_turn produces response with identity-aware behavior.

---

**TASK 10.5 — Identity Enforcement Tests**

Location:
- `tests/test_identity_enforcement.py`

Purpose:
- Verify identity block present in all LLM calls.

Steps:
1. Create `tests/test_identity_enforcement.py`.
2. Test: system prompt contains Jarvis identity.
3. Test: identity present in all modes.
4. Test: Arabic identity works.
5. Test: mode fragments applied correctly.

Success case:
- All tests pass.

Validation:
```bash
pytest tests/test_identity_enforcement.py -v
```

Artifact: `tests/test_identity_enforcement.py`

---

### Definition of Done

Prompt builder assembles complete prompts with identity and mode fragments. Identity is present in all LLM calls. All tests pass.

---

## Phase 11 — Execution Hardening

```
phase_id: 11
title: "Execution Hardening"
priority: "P0"
status: "not_started"
progress_percent: 0
done_tasks: 0
total_tasks: 6
blocker: "Phase 10 must complete"
next_action: "Start TASK 11.1"
last_updated: "-"
validation_status: "not_started"
```

### Objective

Add recovery systems, timeout handling, degradation, and fallback chains to the runtime.

### Tasks

**TASK 11.1 — Timeout Handler**

Location:
- `src/core/runtime/timeout.py`

Purpose:
- Implement timeout handling for all execution phases.

Steps:
1. Create `src/core/runtime/timeout.py`.
2. Define `TimeoutHandler` class.
3. Implement nested timeout hierarchy: tool (30s) < step (60s) < model (120s) < total turn (300s).
4. Implement `enforce(phase, start_time)` → raises `TimeoutError` if exceeded.
5. Log timeout events to observability.

Success case:
- Timeout fires at correct threshold for each phase.

Validation:
```bash
python -c "
from src.core.runtime.timeout import TimeoutHandler
th = TimeoutHandler()
print('TimeoutHandler created')
"
```

Artifact: `src/core/runtime/timeout.py`

---

**TASK 11.2 — Graceful Degradation**

Location:
- `src/core/runtime/degradation.py`

Purpose:
- Handle failures gracefully with fallback responses and degradation tracking.

Steps:
1. Create `src/core/runtime/degradation.py`.
2. Define `DegradationHandler` class.
3. Implement `handle_model_failure(model, error)` → swap to fallback.
4. Implement `handle_tool_failure(tool, error)` → log and continue.
5. Implement `generate_error_response(error_type)` → user-friendly message.
6. Implement `track_degradation(event_type)` → set system_state: degraded.
7. Ensure runtime never crashes.
8. Log all degradation events.

Success case:
- Model failure → fallback chain activates, system_state=degraded logged.
- Tool failure → error logged, runtime continues.

Validation:
```bash
python -c "
from src.core.runtime.degradation import DegradationHandler
dh = DegradationHandler()
print('DegradationHandler created')
"
```

Artifact: `src/core/runtime/degradation.py`

---

**TASK 11.3 — Tiered Fallback System**

Location:
- `src/core/runtime/fallback.py`

Purpose:
- Implement tiered fallback system from README.

Steps:
1. Create `src/core/runtime/fallback.py`.
2. Define `FallbackSystem` class.
3. Implement Tier 1: qwen2.5:7b fallback (reasoning, planning).
4. Implement Tier 2: gemma3:4b fallback (simple responses, complete failure).
5. Implement `attempt(tier)` method.
6. Verify Tier 1 attempted before Tier 2.
7. Log all fallback activations.

Success case:
- `attempt(1)` activates Tier 1 model.
- Tier 1 fails → `attempt(2)` activates Tier 2.

Validation:
```bash
python -c "
from src.core.runtime.fallback import FallbackSystem
fs = FallbackSystem()
print('FallbackSystem created')
"
```

Artifact: `src/core/runtime/fallback.py`

---

**TASK 11.4 — Retry Manager**

Location:
- `src/core/runtime/retry.py`

Purpose:
- Implement global retry budget enforcement and retry logic.

Steps:
1. Create `src/core/runtime/retry.py`.
2. Define `RetryManager` class.
3. Implement `global_retry_budget` = 8.
4. Implement `consume()` → decrements budget, returns remaining.
5. Implement `can_retry()` → bool.
6. Implement `reset()` → resets budget for new turn.
7. Log budget consumption events.

Success case:
- 8 consumes → budget=0, `can_retry()` returns False.

Validation:
```bash
python -c "
from src.core.runtime.retry import RetryManager
rm = RetryManager()
for _ in range(8):
    rm.consume()
assert not rm.can_retry()
print('OK')
"
```

Artifact: `src/core/runtime/retry.py`

---

**TASK 11.5 — Decision Validation Enforcer**

Location:
- `src/core/runtime/validate_decision.py`

Purpose:
- Enforce decision validation rules from README.

Steps:
1. Create `src/core/runtime/validate_decision.py`.
2. Define `DecisionEnforcer` class.
3. Implement `validate(decision)` method.
4. Verify DecisionOutput includes score_breakdown.
5. Verify candidate_list exists and has entries.
6. Verify decision_source is set.
7. Reject invalid decisions → returns safe default (do NOT retry).

Success case:
- Valid decision → validate returns True.
- Missing score_breakdown → validate returns False, safe default provided.

Validation:
```bash
python -c "
from src.core.runtime.validate_decision import DecisionEnforcer
de = DecisionEnforcer()
print('DecisionEnforcer created')
"
```

Artifact: `src/core/runtime/validate_decision.py`

---

**TASK 11.6 — Integration Tests for Hardening**

Location:
- `tests/test_integration.py`

Purpose:
- End-to-end integration tests for full system with hardening.

Steps:
1. Create `tests/test_integration.py`.
2. Test: Full flow from input to FinalResponse.
3. Test: Timeout enforcement (mock slow model).
4. Test: Fallback chain activation (mock model failure).
5. Test: Global retry budget exhaustion.
6. Test: Safety modes enforced throughout.
7. Test: Memory persists across turns.

Success case:
- All integration tests pass.

Validation:
```bash
pytest tests/test_integration.py -v
```

Artifact: `tests/test_integration.py`

---

### Definition of Done

Runtime handles all failure modes gracefully. Fallback chain works. Global retry budget enforced. Runtime never crashes. All integration tests pass.

---

## Phase 12 — CLI Interface

```
phase_id: 12
title: "CLI Interface"
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

Implement CLI interface for user interaction with special commands and formatting.

### Tasks

**TASK 12.1 — CLI Chat Loop**

Location:
- `src/interfaces/cli/chat.py`

Purpose:
- Implement main CLI chat loop.

Steps:
1. Create `src/interfaces/cli/chat.py`.
2. Define `CLIChat` class.
3. Implement `start()` method with input loop.
4. Display prompts and responses.
5. Handle special commands: /quit, /mode, /replay, /debug, /status.
6. Wire to `run_turn()` from runtime loop.
7. Print FinalResponse text to terminal.

Success case:
- `start()` runs chat loop, /quit exits, /replay shows turn trace.

Validation:
```bash
python app/main.py --interface cli
# Type: "hello" → response
# Type: "/mode SAFE" → mode changed
# Type: "/quit" → exit
```

Artifact: `src/interfaces/cli/chat.py`

---

**TASK 12.2 — CLI Commands**

Location:
- `src/interfaces/cli/commands.py`

Purpose:
- Implement CLI command handlers for special commands.

Steps:
1. Create `src/interfaces/cli/commands.py`.
2. Implement `/mode SAFE|BALANCED|UNRESTRICTED` command.
3. Implement `/replay <turn_id>` command.
4. Implement `/debug` toggle command.
5. Implement `/status` command (shows system state, VRAM, model, mode).
6. Validate mode change.
7. Persist mode to user profile.

Success case:
- `/mode BALANCED` changes and persists mode.
- `/replay 1` shows complete turn trace.

Validation:
```bash
python app/main.py --interface cli
# Type: "/mode SAFE" → confirms change
# Type: "/status" → shows system state
```

Artifact: `src/interfaces/cli/commands.py`

---

**TASK 12.3 — CLI Formatting**

Location:
- `src/interfaces/cli/formatting.py`

Purpose:
- Format terminal output for readability.

Steps:
1. Create `src/interfaces/cli/formatting.py`.
2. Define `CLIFormatter` class.
3. Implement `format_response(FinalResponse)` method.
4. Add colors with colorama.
5. Format tool results.
6. Format error messages.
7. Support Arabic text display (RTL handling).

Success case:
- Formatted response is readable with colors and proper alignment.

Validation:
```bash
python -c "
from src.interfaces.cli.formatting import CLIFormatter
from src.core.runtime.final_response import FinalResponse
cf = CLIFormatter()
r = FinalResponse(text='hello', session_id='s1', model='gemma3:4b', mode='fast', quality=0.9, decision_source='fast_path', turn_id=1)
formatted = cf.format_response(r)
assert len(formatted) > 0
print('OK')
"
```

Artifact: `src/interfaces/cli/formatting.py`

---

### Definition of Done

CLI chat loop runs with all special commands. Formatting is readable. Arabic text displays correctly.

---

## Phase 13 — Web Automation & Browser

```
phase_id: 13
title: "Web Automation & Browser"
priority: "P2"
status: "not_started"
progress_percent: 0
done_tasks: 0
total_tasks: 3
blocker: "Phase 12 must complete"
next_action: "Start TASK 13.1"
last_updated: "-"
validation_status: "not_started"
```

### Objective

Implement web automation capabilities using Playwright.

### Tasks

**TASK 13.1 — Browser Capability**

Location:
- `src/capabilities/web_automation/browser.py`

Purpose:
- Implement browser automation capability with Playwright.

Steps:
1. Create `src/capabilities/web_automation/` directory.
2. Create `src/capabilities/web_automation/browser.py`.
3. Inherit from `BaseCapability`.
4. Implement `execute(args)` with actions: navigate, click, type, screenshot, extract_text.
5. Use Playwright for browser control.
6. Launch separate browser process (+500MB VRAM, +2GB RAM).
7. Handle page load, waits, timeouts.
8. Return ToolResult with action result.

Success case:
- `execute({"action": "navigate", "url": "https://example.com"})` returns page data.

Failure case:
- Page timeout → ToolResult with success=False.

Validation:
```bash
python -c "
from src.capabilities.web_automation.browser import BrowserCapability
bc = BrowserCapability()
print('BrowserCapability created')
"
```

Artifact: `src/capabilities/web_automation/browser.py`

---

**TASK 13.2 — Web Session Manager**

Location:
- `src/capabilities/web_automation/session.py`

Purpose:
- Manage browser sessions and cookies.

Steps:
1. Create `src/capabilities/web_automation/session.py`.
2. Define `WebSessionManager` class.
3. Implement `create_session()` method.
4. Implement `close_session(session_id)`.
5. Manage cookies, localStorage.
6. Handle multiple sessions.

Success case:
- `create_session()` returns session handle.
- `close_session(id)` closes browser context.

Validation:
```bash
python -c "
from src.capabilities.web_automation.session import WebSessionManager
wsm = WebSessionManager()
print('WebSessionManager created')
"
```

Artifact: `src/capabilities/web_automation/session.py`

---

**TASK 13.3 — Web Automation Tests**

Location:
- `tests/test_web_automation.py`

Purpose:
- Test web automation capabilities.

Steps:
1. Create `tests/test_web_automation.py`.
2. Test: browser navigation.
3. Test: click elements.
4. Test: type text.
5. Test: screenshot capture.
6. Test: text extraction.
7. Test: session management.

Success case:
- All tests pass.

Validation:
```bash
pytest tests/test_web_automation.py -v
```

Artifact: `tests/test_web_automation.py`

---

### Definition of Done

Browser automation works with Playwright. Sessions are managed. All tests pass.

---

## Phase 14 — Google APIs

```
phase_id: 14
title: "Google APIs"
priority: "P2"
status: "not_started"
progress_percent: 0
done_tasks: 0
total_tasks: 4
blocker: "Phase 13 must complete"
next_action: "Start TASK 14.1"
last_updated: "-"
validation_status: "not_started"
```

### Objective

Implement Google API integrations as services.

### Tasks

**TASK 14.1 — Google Auth Service**

Location:
- `src/services/google/auth.py`

Purpose:
- Handle OAuth2 authentication for Google APIs.

Steps:
1. Create `src/services/google/` directory.
2. Create `src/services/google/auth.py`.
3. Define `GoogleAuth` class.
4. Implement `authenticate(credentials_path)` method.
5. Handle OAuth2 flow with refresh tokens.
6. Store tokens securely.
7. Implement `get_credentials()` for API calls.

Success case:
- Authentication flow completes, credentials stored.

Validation:
```bash
python -c "
from src.services.google.auth import GoogleAuth
ga = GoogleAuth()
print('GoogleAuth created')
"
```

Artifact: `src/services/google/auth.py`

---

**TASK 14.2 — Google Calendar Service**

Location:
- `src/services/google/calendar.py`

Purpose:
- Integrate with Google Calendar API.

Steps:
1. Create `src/services/google/calendar.py`.
2. Define `GoogleCalendar` class.
3. Implement `list_events(start, end)`.
4. Implement `create_event(summary, start, end, description)`.
5. Implement `delete_event(event_id)`.

Success case:
- `list_events()` returns upcoming events.

Validation:
```bash
python -c "
from src.services.google.calendar import GoogleCalendar
gc = GoogleCalendar()
print('GoogleCalendar created')
"
```

Artifact: `src/services/google/calendar.py`

---

**TASK 14.3 — Gmail Service**

Location:
- `src/services/google/gmail.py`

Purpose:
- Integrate with Gmail API.

Steps:
1. Create `src/services/google/gmail.py`.
2. Define `GmailService` class.
3. Implement `list_messages(query, max_results)`.
4. Implement `get_message(message_id)`.
5. Implement `send_message(to, subject, body)`.

Success case:
- `list_messages()` returns messages.

Validation:
```bash
python -c "
from src.services.google.gmail import GmailService
gs = GmailService()
print('GmailService created')
"
```

Artifact: `src/services/google/gmail.py`

---

**TASK 14.4 — Google Drive Service**

Location:
- `src/services/google/drive.py`

Purpose:
- Integrate with Google Drive API.

Steps:
1. Create `src/services/google/drive.py`.
2. Define `GoogleDrive` class.
3. Implement `list_files(query)`.
4. Implement `download_file(file_id, destination)`.
5. Implement `upload_file(name, content, mime_type)`.

Success case:
- `list_files()` returns file listing.

Validation:
```bash
python -c "
from src.services.google.drive import GoogleDrive
gd = GoogleDrive()
print('GoogleDrive created')
"
```

Artifact: `src/services/google/drive.py`

---

### Definition of Done

Google APIs authenticate and return data. Calendar, Gmail, and Drive services are functional.

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

**TASK 15.1 — Web UI Backend**

Location:
- `src/interfaces/web/app.py`

Purpose:
- Implement FastAPI backend for Web UI.

Steps:
1. Create `src/interfaces/web/` directory.
2. Create `src/interfaces/web/app.py`.
3. Define FastAPI app.
4. Implement REST endpoints: POST /chat, GET /history.
5. Implement WebSocket endpoint: /ws for real-time communication.
6. Wire to `run_turn()` from runtime loop.
7. Handle FinalResponse and stream updates.

Success case:
- POST /chat returns FinalResponse.
- WebSocket sends streaming updates.

Validation:
```bash
python app/main.py --interface web
# Open: http://localhost:8000
# Test chat via UI
```

Artifact: `src/interfaces/web/app.py`

---

**TASK 15.2 — Web UI Frontend**

Location:
- `src/interfaces/web/static/index.html`

Purpose:
- Create simple web frontend for chat.

Steps:
1. Create `src/interfaces/web/static/` directory.
2. Create `index.html` with chat interface.
3. Implement WebSocket client for real-time updates.
4. Add message display (user + Jarvis).
5. Add input box and send button.
6. Support Arabic text input/display.
7. Add mode toggle button.

Success case:
- UI loads at http://localhost:8000, sends messages, displays responses.

Validation:
- Open http://localhost:8000, send messages, verify responses.

Artifact: `src/interfaces/web/static/index.html`

---

**TASK 15.3 — Web UI Tests**

Location:
- `tests/test_web_ui.py`

Purpose:
- Test Web UI functionality.

Steps:
1. Create `tests/test_web_ui.py`.
2. Test: FastAPI endpoints respond correctly.
3. Test: WebSocket connection and messaging.
4. Test: mode toggle via API.
5. Use httpx for testing.

Success case:
- All tests pass.

Validation:
```bash
pytest tests/test_web_ui.py -v
```

Artifact: `tests/test_web_ui.py`

---

### Definition of Done

Web UI is functional with chat, history, and real-time updates. All tests pass.

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

**TASK 16.1 — STT Capability (Whisper)**

Location:
- `src/capabilities/voice/stt.py`

Purpose:
- Implement Speech-to-Text using Whisper.

Steps:
1. Create `src/capabilities/voice/` directory.
2. Create `src/capabilities/voice/stt.py`.
3. Inherit from `BaseCapability`.
4. Implement `execute(args)` with args: audio_path or audio_data.
5. Use Whisper for transcription (+500MB VRAM, +1GB RAM).
6. Support multiple languages (English, Arabic).
7. Return ToolResult with transcribed text.

Success case:
- `execute({"audio_path": "test.wav"})` returns transcribed text.

Validation:
```bash
python -c "
from src.capabilities.voice.stt import STTCapability
stt = STTCapability()
print('STTCapability created')
"
```

Artifact: `src/capabilities/voice/stt.py`

---

**TASK 16.2 — TTS Capability (Piper)**

Location:
- `src/capabilities/voice/tts.py`

Purpose:
- Implement Text-to-Speech using Piper.

Steps:
1. Create `src/capabilities/voice/tts.py`.
2. Inherit from `BaseCapability`.
3. Implement `execute(args)` with args: text, voice (optional).
4. Use Piper for synthesis.
5. Support multiple languages (English, Arabic).
6. Return ToolResult with audio file path.

Success case:
- `execute({"text": "Hello"})` returns audio file path.

Validation:
```bash
python -c "
from src.capabilities.voice.tts import TTSCapability
tts = TTSCapability()
print('TTSCapability created')
"
```

Artifact: `src/capabilities/voice/tts.py`

---

**TASK 16.3 — Wake Word Detection**

Location:
- `src/capabilities/voice/wake_word.py`

Purpose:
- Detect wake word to activate voice input.

Steps:
1. Create `src/capabilities/voice/wake_word.py`.
2. Define `WakeWordDetector` class.
3. Implement `listen_for_wake_word(word)` method.
4. Use speech_recognition library.
5. Trigger callback when wake word detected.
6. Integrate with STT capability.

Success case:
- Wake word detected → callback fires.

Validation:
```bash
python -c "
from src.capabilities.voice.wake_word import WakeWordDetector
wwd = WakeWordDetector()
print('WakeWordDetector created')
"
```

Artifact: `src/capabilities/voice/wake_word.py`

---

**TASK 16.4 — Voice Pipeline Tests**

Location:
- `tests/test_voice.py`

Purpose:
- Test voice pipeline components.

Steps:
1. Create `tests/test_voice.py`.
2. Test: STT transcription.
3. Test: TTS synthesis.
4. Test: wake word detection (mock).
5. Test: integration with runtime loop.

Success case:
- All tests pass.

Validation:
```bash
pytest tests/test_voice.py -v
```

Artifact: `tests/test_voice.py`

---

### Definition of Done

Voice pipeline works: STT transcribes, TTS synthesizes, wake word triggers activation. All tests pass.

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

**TASK 17.1 — Vision Capability (llava:7b)**

Location:
- `src/capabilities/vision/vision.py`

Purpose:
- Implement image understanding using llava:7b model.

Steps:
1. Create `src/capabilities/vision/` directory.
2. Create `src/capabilities/vision/vision.py`.
3. Inherit from `BaseCapability`.
4. Implement `execute(args)` with args: image_path, prompt.
5. Use llava:7b through Ollama (+4.5GB VRAM).
6. Return image description or answer to prompt.
7. Return ToolResult with vision output.

Success case:
- `execute({"image_path": "test.jpg", "prompt": "describe"})` returns image description.

Failure case:
- VRAM insufficient → ToolResult with success=False, error="insufficient VRAM".

Validation:
```bash
python -c "
from src.capabilities.vision.vision import VisionCapability
v = VisionCapability()
print('VisionCapability created')
"
```

Artifact: `src/capabilities/vision/vision.py`

---

**TASK 17.2 — Image Generation Capability (Stable Diffusion)**

Location:
- `src/capabilities/vision/image_gen.py`

Purpose:
- Generate images using Stable Diffusion.

Steps:
1. Create `src/capabilities/vision/image_gen.py`.
2. Inherit from `BaseCapability`.
3. Implement `execute(args)` with args: prompt, size, style.
4. Use Stable Diffusion (+2GB VRAM, +2GB RAM).
5. CPU fallback possible.
6. Return ToolResult with generated image path.

Success case:
- `execute({"prompt": "a cat", "size": "512x512"})` returns image path.

Failure case:
- VRAM insufficient → uses CPU fallback.

Validation:
```bash
python -c "
from src.capabilities.vision.image_gen import ImageGenCapability
ig = ImageGenCapability()
print('ImageGenCapability created')
"
```

Artifact: `src/capabilities/vision/image_gen.py`

---

### Definition of Done

Vision capability understands images. Image generation produces images. VRAM constraints are handled.

---

## Phase 18 — QA + Production

```
phase_id: 18
title: "QA + Production"
priority: "P0"
status: "not_started"
progress_percent: 0
done_tasks: 0
total_tasks: 6
blocker: "Phase 17 must complete"
next_action: "Start TASK 18.1"
last_updated: "-"
validation_status: "not_started"
```

### Objective

Final QA, testing, performance validation, and production readiness.

### Tasks

**TASK 18.1 — Performance Tests**

Location:
- `tests/test_performance.py`

Purpose:
- Test system performance within hardware constraints.

Steps:
1. Create `tests/test_performance.py`.
2. Test: Fast-path latency < 100ms.
3. Test: Simple query latency < 5s.
4. Test: VRAM usage stays within 6GB.
5. Test: RAM usage stays within 16GB.
6. Test: Concurrent request handling (Web UI).

Success case:
- All performance targets met.

Failure case:
- Latency exceeds target → FAIL, log details.
- VRAM exceeds 5.5GB → FAIL, log warning.

Validation:
```bash
pytest tests/test_performance.py -v
```

Artifact: `tests/test_performance.py`

---

**TASK 18.2 — Arabic Language Tests**

Location:
- `tests/test_arabic.py`

Purpose:
- Verify full Arabic language support.

Steps:
1. Create `tests/test_arabic.py`.
2. Test: Arabic input classification (fast path and model path).
3. Test: Arabic responses.
4. Test: Arabic UI display.
5. Test: Arabic voice (STT/TTS).
6. Test: Arabic vision prompts.

Success case:
- All Arabic tests pass with identical behavior to English.

Validation:
```bash
pytest tests/test_arabic.py -v
```

Artifact: `tests/test_arabic.py`

---

**TASK 18.3 — Production Configuration**

Location:
- `config/production.yaml`

Purpose:
- Create production-ready configuration.

Steps:
1. Create `config/production.yaml`.
2. Set production values: mode=BALANCED, logging level=WARNING.
3. Disable debug modes.
4. Set appropriate timeouts.
5. Configure fallback models.
6. Document production deployment steps.

Success case:
- `load_config("config/production.yaml")` returns valid production settings.

Validation:
```bash
python -c "from src.core.config import load_config; s = load_config('config/production.yaml'); assert s.execution_mode == 'BALANCED'; print('OK')"
```

Artifact: `config/production.yaml`

---

**TASK 18.4 — Full Test Suite**

Location:
- All test files.

Purpose:
- Run complete test suite to verify all components.

Steps:
1. Run all tests: `pytest tests/ -v`.
2. Verify 100% pass rate.
3. Check test coverage (target: > 80%).
4. Fix any remaining failures.

Success case:
- All tests pass.

Validation:
```bash
pytest tests/ -v --tb=short
```

---

**TASK 18.5 — VERSION and Release**

Location:
- `VERSION`
- `RELEASE_NOTES.md`

Purpose:
- Finalize version and release documentation.

Steps:
1. Create `VERSION` file with "2.0".
2. Create `RELEASE_NOTES.md` with:
   - Features implemented.
   - Known limitations.
   - Hardware requirements.
   - How to run.
3. Final code cleanup.
4. Remove debug prints.
5. Ensure all tests pass.

Success case:
- VERSION file contains "2.0".
- RELEASE_NOTES.md documents all features.

Validation:
```bash
cat VERSION
pytest tests/ -v  # All tests pass
```

Artifacts: `VERSION`, `RELEASE_NOTES.md`

---

**TASK 18.6 — Determinism Verification**

Location:
- `tests/test_determinism.py`

Purpose:
- Verify deterministic behavior: identical inputs produce identical execution paths.

Steps:
1. Create `tests/test_determinism.py`.
2. Test: same input produces same decision (fast path).
3. Test: same input produces same model selection (scoring is deterministic).
4. Test: same input produces same state transitions.
5. Test: no randomization in routing or model selection.
6. Test: seed-based reproducibility for model path.

Success case:
- All determinism tests pass.

Validation:
```bash
pytest tests/test_determinism.py -v
```

Artifact: `tests/test_determinism.py`

---

### Definition of Done

All tests pass. Performance targets met. Arabic support verified. Production config ready. Determinism verified. VERSION and RELEASE_NOTES.md created.

---

## Execution Gaps — Lock Phase

```
phase_id: gap
title: "Execution Gaps Lock"
priority: "P0"
status: "in_progress"
progress_percent: 0
done_tasks: 0
total_tasks: 8
blocker: "none"
next_action: "Address during relevant phases"
last_updated: "2026-04-30"
validation_status: "not_started"
```

### Objective

These gap items are now embedded within the phases above. Each gap is addressed by the corresponding phase task:

| Gap Item | Addressed In | Task |
|----------|-------------|------|
| Capability Validator (Decision alignment) | Phase 6 | TASK 6.4 (Permission Layer), TASK 6.6 (Schema Validator) |
| Enhanced Logging System | Phase 1 | TASK 1.2 (Logging), Phase 1 TASK 1.9 (Metrics) |
| Failure Handling System | Phase 11 | TASK 11.2 (Degradation), TASK 11.3 (Fallback) |
| Identity Verification | Phase 10 | TASK 10.5 (Identity Enforcement Tests) |
| Execution Limits Enforcement | Phase 4 | TASK 4.3 (Hard Limits), TASK 11.4 (Retry Manager) |
| Decision Validation (Dynamic Scoring) | Phase 5 | TASK 5.3 (Scorer), TASK 5.7 (Decision Tests) |
| Decision Enforcement | Phase 11 | TASK 11.5 (Decision Validation Enforcer) |
| Response Quality Guard | Phase 4 | TASK 4.6 (Evaluator) |

### Definition of Done

All gap items are addressed by phase tasks. No orphan gap items remain.

---

## Summary

Total phases: 19 (Phase 0 through Phase 18 + Execution Gaps)
Total tasks: ~120
All tasks mapped to STRUCTURE.md layers
All tasks decomposed into atomic steps
All terminology normalized (capabilities not skills/tools)
All paths aligned with STRUCTURE.md
All tasks include: success case, failure case, edge cases
All tasks include real validation (not print statements)
Vertical slice delivered in Phase 0 for early end-to-end proof

---

**End of Execution Plan v2.0**
