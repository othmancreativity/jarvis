<div align="center">

# 🤖 JARVIS
### Local AI Assistant — Arabic + English — Free, Unlimited, Private

![Version](https://img.shields.io/badge/version-1.0.0--alpha-blue)
![Python](https://img.shields.io/badge/python-3.10+-green)
![License](https://img.shields.io/badge/license-MIT-orange)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightblue)
![Arabic](https://img.shields.io/badge/language-Arabic%20%2B%20English-red)

</div>

---

## 1. Overview

Jarvis is a fully local AI assistant. It accepts text, voice, or file input in Arabic or English, and produces either a conversational answer or a real system action (opening apps, sending emails, searching the web, managing files).

All processing happens on the local machine. No cloud connection is required. No data leaves the device.

---

## 2. System Architecture

### Layers (strict — no overlap)

| Layer | Location | Responsibility | Does NOT |
|-------|----------|----------------|----------|
| Interface | `src/interfaces/` | Receive input, display output | Classify, route, store |
| Context | `src/core/context/` | Bundle this turn's inputs | Store across turns |
| Decision | `src/core/decision/` | Classify intent, select model and mode | Think, generate content |
| Runtime | `src/core/runtime/` | Drive the execution loop | Implement intelligence |
| Agents | `src/core/agents/` | Multi-step reasoning and planning | Route requests |
| Tools (mgmt) | `src/core/tools/` | Registry, validation, execution bridge | Implement tool logic |
| Skills (impl) | `src/skills/` | One specific action per file | Decisions, routing |
| Models | `src/models/` | Wrap AI model I/O | Decisions, memory |
| Memory | `src/core/memory/` | Persist data across turns | Participate in routing |
| Identity | `src/core/identity/` | Build system prompts | Route or decide |

---

## 3. Execution Contract

This section defines the data shapes exchanged between every stage of the runtime loop. These types are binding. No stage may pass data outside this contract.

### InputPacket

Produced by: `context.assembler.assemble_context()`
Consumed by: `runtime.loop.run_turn()`

```
InputPacket {
  user_message     : str            — raw text from user
  session_id       : str            — unique session identifier
  attachments      : list[Attachment] — files, images, audio (paths only)
  memory_snippets  : list[str]      — top-N semantic matches from long-term memory
  recent_history   : list[Message]  — last N turns from short-term memory
  user_profile     : UserProfile    — language, style, technical_level
  tool_results     : list[ToolResult] — results from Act steps this turn
  turn_number      : int
}
```

### DecisionOutput

Produced by: `core.decision.decision.decide()`
Consumed by: `runtime.executor.execute_turn()`

```
DecisionOutput {
  intent           : str   — one of: chat | code | tool_use | search | vision | research | voice
  complexity       : str   — one of: low | medium | high
  mode             : str   — one of: fast | normal | deep | planning | research
  model            : str   — exact Ollama model tag (e.g. "qwen3:8b")
  requires_tools   : bool
  requires_planning: bool
  tool_name        : str | null
  tool_args        : dict
  confidence       : float — 0.0 to 1.0
  risk_level       : str   — one of: low | medium | high
}
```

### LLMOutput

Produced by: `runtime.executor.execute_turn()` after calling the model
Consumed by: `runtime.loop` to branch between direct answer and tool execution

```
LLMOutput {
  type     : str   — one of: "answer" | "tool_call"
  content  : str   — if type="answer": the final response text
  tool     : str   — if type="tool_call": tool name
  args     : dict  — if type="tool_call": validated arguments
}
```

**Parsing rule:** If `requires_tools=True` in `DecisionOutput`, the model MUST produce a `tool_call` type response. Any free-text response when a tool is required is treated as a parse failure and triggers a retry.

### ToolResult

Produced by: `core.tools.executor.execute_tool()`
Consumed by: `runtime.loop` as the next observation

```
ToolResult {
  tool        : str   — tool name that was called
  success     : bool
  data        : dict  — tool-specific result payload
  error       : str   — empty string if success=True
  duration_ms : float
}
```

### FinalResponse

Produced by: `runtime.loop` when type="answer" and evaluator approves
Consumed by: Interface layer for display

```
FinalResponse {
  text       : str   — the response text
  session_id : str
  model      : str   — model that produced this response
  mode       : str   — mode used
  quality    : float — evaluator score (0.0 to 1.0)
}
```

---

## 4. Runtime Loop

The loop runs for every user turn. It terminates when the evaluator approves the response or when `max_iterations` is reached.

```
START turn
  input = observe(InputPacket)
  LOOP (max_iterations = 5):
    decision = decide(input)
    output   = think(decision, input)
    IF output.type == "tool_call":
      result = act(output)
      input.tool_results.append(result)
      CONTINUE loop (tool result becomes next observation)
    IF output.type == "answer":
      eval = evaluate(output, decision)
      IF eval.should_retry:
        escalate(decision)  → increase mode/model
        CONTINUE loop
      ELSE:
        BREAK
  END LOOP
  IF no approved answer: return fallback response
  save to memory
  return FinalResponse
END turn
```

**Stop conditions:**
- Evaluator returns `should_retry=False`
- `max_iterations` reached (returns best available response)
- Tool returns `success=False` after `max_tool_retries` (returns error message)

**Fallback:** When all iterations exhausted, return the last generated text with a note that the answer may be incomplete.

---

## 5. Tool Execution Flow

Every tool call follows this exact path. No shortcut is allowed.

```
LLM generates output
  ↓
Parse: extract JSON from LLM output text
  ↓
Validate: check JSON has required fields {type, tool, args}
  ↓
IF parse fails → retry LLM call (max 2 retries) → if still fails: return error
  ↓
Registry lookup: find tool by name
  ↓
IF tool not found → return ToolResult(success=False, error="Tool not found")
  ↓
Safety classify: assign risk_level (low | medium | high)
  ↓
Apply Execution Mode rules (see Section 8)
  ↓
Schema validate: check args against tool's JSON Schema
  ↓
IF schema fails → return ToolResult(success=False, error="Invalid args: {details}")
  ↓
Execute: call tool.execute(**args)
  ↓
Return ToolResult
  ↓
Append to InputPacket.tool_results
  ↓
Re-enter observe() step
```

---

## 6. Tool JSON Format

### Tool Call (LLM → Runtime)

When a tool is needed, the model must output exactly this JSON and nothing else:

```
{
  "type": "tool_call",
  "tool": "<tool_name>",
  "args": {
    "<param>": "<value>"
  }
}
```

**Rules:**
- The JSON must be the entire model output when a tool is required. No surrounding text.
- `type` must equal the string `"tool_call"`.
- `tool` must match a registered tool name exactly.
- `args` must be a JSON object (even if empty: `{}`).
- If the model returns anything else when `requires_tools=True`, it is a parse failure.

### Tool Result (Runtime → LLM)

After tool execution, the runtime injects this into the next message:

```
{
  "type": "tool_result",
  "tool": "<tool_name>",
  "success": true | false,
  "data": { ... },
  "error": "" | "<error message>"
}
```

### Parse Failure Handling

If the LLM output cannot be parsed as valid tool call JSON:
1. Log the failure.
2. Re-send the request with an explicit instruction to output only JSON.
3. If still failing after 2 retries: return `ToolResult(success=False, error="Model did not produce valid tool call")`.
4. Runtime treats this as a tool failure and follows the tool failure path.

---

## 7. Boot Flow

The following steps execute in order when `python app/main.py` is called. No step may be skipped.

```
Step 1 — Parse arguments
  Read --interface flag and --debug flag

Step 2 — Load config
  Load config/settings.yaml into AppSettings
  Load .env variables
  Validate: required keys present, model names non-empty

Step 3 — Initialize logging
  Configure Loguru to logs/jarvis.log with rotation
  Log: "Jarvis starting, interface={}, version={}"

Step 4 — Create directories
  Ensure all paths from config exist: data/, logs/, data/chroma/, data/sessions/, etc.

Step 5 — Initialize memory
  Connect to Redis (short-term). On failure: switch to in-memory dict, log warning.
  Connect to ChromaDB (long-term). On failure: disable semantic recall, log warning.
  Connect to SQLite (structured). On failure: crash with clear message (SQLite is critical).

Step 6 — Initialize tool registry
  Scan src/skills/ for BaseTool subclasses
  Register all tools where is_available() returns True
  Log count of registered tools

Step 7 — Validate models
  For each model in config (default, fast, code, vision):
    Check if model is present in `ollama list`
    Log warning if missing (do not crash — model loads on first use)

Step 8 — Load user profile
  Read data/user_profile.json
  If missing: create with defaults (language=ar, style=balanced)

Step 9 — Start interface
  Launch the selected interface (cli | web | voice | telegram | gui | all)
  Each interface starts its own input loop

Step 10 — Ready
  Log: "Jarvis ready"
  Interface displays ready message to user
```

---

## 8. System Start Behavior (First Message)

When the system receives the first message of a new session, the following applies:

**Memory state:** Empty. No history. No semantic memories. The InputPacket is assembled with `recent_history=[]` and `memory_snippets=[]`.

**Context state:** Built fresh from the user message and user profile only.

**Identity:** The system prompt is built using the Jarvis identity definition and the user profile, regardless of memory state.

**Model state:** No model is pre-loaded. The first call to `swap_to(model)` triggers the actual load. Expect latency on the first response.

**Behavior:** The system functions identically whether memory is empty or populated. The absence of memory snippets means the model has no prior context — it does not cause an error.

---

## 9. Execution Modes (Safety)

Every tool execution is governed by an Execution Mode. The mode determines whether confirmation is required before running a tool.

### Mode Definitions

| Mode | Value | Behavior |
|------|-------|----------|
| SAFE | `"safe"` | Every tool call requires explicit user confirmation before execution |
| BALANCED | `"balanced"` | Low-risk tools auto-execute; medium-risk require confirmation; high-risk are blocked unless user explicitly overrides |
| UNRESTRICTED | `"unrestricted"` | All tools execute without confirmation |

**Default mode:** `BALANCED`

The active mode is stored in `config/settings.yaml` under `runtime.execution_mode`. It can be changed at runtime via the `/mode safe|balanced|unrestricted` CLI command or equivalent Web UI setting.

### Risk Classification

Every tool has a fixed `risk_level` defined in `config/skills.yaml`. The classification is:

| Risk Level | Examples | SAFE behavior | BALANCED behavior | UNRESTRICTED behavior |
|-----------|---------|---------------|-------------------|----------------------|
| `low` | web_search, read_file, system_info, take_screenshot | Requires confirmation | Auto-executes | Auto-executes |
| `medium` | open_app, execute_python, run_shell, send_notification | Requires confirmation | Requires confirmation | Auto-executes |
| `high` | delete_file, kill_process, send_email, send_message | Requires confirmation | Blocked unless user typed explicit override phrase | Auto-executes |

**Blocked behavior for `high` in BALANCED:** The tool is not executed. The runtime returns a message explaining that this action requires switching to UNRESTRICTED mode or using the explicit approval phrase. The explicit approval phrase is the user typing "confirm: {tool_name}" as a follow-up message.

### Connection to Runtime

The Decision Layer sets `risk_level` on `DecisionOutput`. The Executor reads the current mode from config and applies the rules above before calling `tool.execute()`.

---

## 10. Prompt System

Every model call receives a system prompt built by the Prompt Builder. The prompt is not static text — it is assembled from components in a fixed order.

### Assembly Order

```
1. Jarvis identity block     — who Jarvis is, its role, the component notice
2. Safety rules block        — what Jarvis must never do
3. User profile block        — user's language, style, technical level
4. Mode fragment             — how to respond based on current thinking mode
5. Task context              — what the user is trying to accomplish this turn
6. Tool list                 — available tools (only if requires_tools=True)
7. Handoff note              — present only when model was just swapped
```

Each block is a text fragment loaded from `config/jarvis_identity.yaml` or computed at runtime. No block is optional except blocks 6 and 7.

### Thinking Mode Fragments

The mode fragment changes the model's reasoning style. The mode is set by `DecisionOutput.mode`.

| Mode | Effect on response |
|------|--------------------|
| `fast` | Concise, one to three sentences, no elaboration |
| `normal` | Complete and well-structured |
| `deep` | Step-by-step reasoning with self-verification |
| `planning` | Decompose into numbered steps before acting |
| `research` | Multi-source, cite each claim, summarize at end |

---

## 11. Decision System

The Decision Layer classifies the current turn and selects resources. It does not generate content and does not call a model for reasoning.

### Classification Rules

| Signal | Decision |
|--------|----------|
| Image in attachments | intent=vision, model=llava:7b |
| Message contains code keywords | intent=code, model=qwen2.5-coder:7b |
| Message length < 20 chars, no action keywords | intent=chat, mode=fast, model=gemma3:4b |
| Multi-step goal detected | intent=research, mode=planning, model=qwen3:8b |
| Default | intent=chat, mode=normal, model=qwen3:8b |

### Model Selection Rules

```
image present                   → llava:7b
intent == "code"                → qwen2.5-coder:7b
complexity == "low" AND mode == "fast"  → gemma3:4b
all other cases                 → qwen3:8b
```

---

## 12. Memory System

| Store | Backend | Scope | Contents |
|-------|---------|-------|----------|
| Short-term | Redis (in-memory fallback) | Current session | Last 50 messages |
| Long-term | ChromaDB | Cross-session | Facts, outcomes, preferences |
| Structured | SQLite | Permanent | Conversations, tasks, feedback |
| Profile | JSON file | Permanent | User preferences |

Memory injection into Context:
- Short-term: last 10 messages from current session
- Long-term: top 3 semantically similar snippets for the current message
- Profile: always injected into every turn

---

## 13. Models

| Ollama Tag | Role | VRAM | Use Case |
|-----------|------|------|----------|
| `qwen3:8b` | Main brain | 5.0 GB | Arabic, reasoning, planning, general |
| `gemma3:4b` | Fast responder | 3.0 GB | Quick answers, classification |
| `qwen2.5-coder:7b` | Code specialist | 4.7 GB | Code generation, debugging |
| `llava:7b` | Vision | 4.5 GB | Image understanding, OCR |

**VRAM rule:** One model loaded at a time. Before loading a new model, unload the current one. Never load two models simultaneously on 6 GB GPU.

---

## 14. Skills

All tool implementations live in `src/skills/`. Each file implements one or more `BaseTool` subclasses. Skills are grouped by category:

| Category | Location | Examples |
|----------|----------|---------|
| system | `src/skills/system/` | open_app, close_app, system_info, clipboard |
| files | `src/skills/files/` | read_file, write_file, delete_file, search_files |
| browser | `src/skills/browser/` | navigate, click, fill, download, upload |
| search | `src/skills/search/` | web_search, fetch_page |
| api | `src/skills/api/` | calendar, gmail, drive, contacts, youtube |
| screen | `src/skills/screen/` | take_screenshot, read_screen_text, describe_screen |
| coder | `src/skills/coder/` | execute_python, run_shell |
| notify | `src/skills/notify/` | send_notification |
| social | `src/skills/social/` | whatsapp_send, whatsapp_read |
| media | `src/skills/media/` | play_pause, set_volume |
| network | `src/skills/network/` | check_connection, get_ip |
| pdf | `src/skills/pdf/` | pdf_read_text, pdf_summarize |
| office | `src/skills/office/` | docx_read, xlsx_read, docx_write |

---

## 15. Cross-Platform Support

| Action | Windows | Linux | macOS |
|--------|---------|-------|-------|
| Kill process | taskkill /IM | pkill | kill -9 |
| Open app | ShellExecute | subprocess | open -a |
| Notifications | winotify | notify-send | osascript |
| Volume | pycaw | pactl/amixer | osascript |
| Clipboard | pyperclip + win32clipboard | pyperclip + xclip | pyperclip |
| Hotkeys | keyboard lib | pynput | pynput |
| Auto-start | Registry Run key | ~/.config/autostart/ | ~/Library/LaunchAgents/ |

All file paths use `pathlib.Path`. No hardcoded path separators.

---

## 16. Error Handling

| Error Class | Cause | Action |
|-------------|-------|--------|
| `model_error` | Ollama unreachable or OOM | Retry with smaller model |
| `tool_not_found` | Tool name not in registry | Return error to LLM; LLM explains |
| `parse_failure` | LLM output not valid tool call JSON | Retry with explicit JSON instruction (max 2) |
| `validation_error` | Args fail JSON Schema | Return error; LLM can retry with corrected args |
| `safety_blocked` | risk=high in BALANCED mode | Explain to user; require explicit approval phrase |
| `user_declined` | User rejected RISKY confirmation | Return message: "Action cancelled" |
| `tool_timeout` | Execution exceeded time limit | Return ToolResult with error; continue turn |
| `vram_oom` | GPU out of memory | Unload all; load smallest available model; retry |

---

## 17. Configuration Reference

All configuration lives in `config/settings.yaml`. No tunable parameters exist as Python constants.

Key sections:

| Section | Purpose |
|---------|---------|
| `jarvis` | name, language list, wake_word |
| `models` | default, fast, code, vision model tags |
| `hardware` | gpu_vram_limit_gb, max_concurrent_models |
| `interfaces` | web_host, web_port |
| `paths` | data, logs, chroma, sqlite |
| `hotkeys` | open_cli, start_voice |
| `runtime` | max_iterations, max_tool_retries, tool_timeout_s, execution_mode |

---

## 18. Logging

All log entries use key=value structured format. Every entry has a timestamp and level.

| Event | Fields |
|-------|--------|
| `turn.start` | session, input_len, turn |
| `decision` | intent, model, mode, risk_level |
| `tool.start` | name, risk_level, mode |
| `tool.done` | name, success, duration_ms |
| `tool.blocked` | name, reason |
| `tool.parse_failure` | attempt, error |
| `eval` | quality, should_retry |
| `model.swap` | from, to |
| `turn.end` | session, quality, total_ms |

Log files: `logs/jarvis.log` (INFO+, 10 MB rotation, 7-day retention).

---

## 19. Quick Start

```
# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Pull models
ollama pull qwen3:8b
ollama pull qwen2.5-coder:7b
ollama pull gemma3:4b
ollama pull llava:7b

# Configure
cp config/settings.example.yaml config/settings.yaml
cp .env.example .env

# Run
python app/main.py --interface cli
```

---

## 20. Tech Stack

| Layer | Technology |
|-------|-----------|
| LLM Runtime | Ollama |
| Web Framework | FastAPI + Uvicorn |
| Vector DB | ChromaDB |
| Cache | Redis |
| SQL | SQLite |
| STT | OpenAI Whisper |
| TTS | Piper TTS |
| Wake Word | openWakeWord |
| Image Gen | Diffusers (SD 1.5) |
| Browser | Playwright |
| Terminal UI | Rich |
| Desktop GUI | PyQt6 |
| Telegram | python-telegram-bot |
| Google APIs | google-api-python-client |
| Config | PyYAML + Pydantic |
| Logging | Loguru |
| Windows-specific | pywin32, pycaw, pystray, winotify |
| Cross-platform | pyperclip, pynput, keyboard, mss, pytesseract |
| Security | cryptography (Fernet) |
| Testing | pytest + pytest-asyncio + pytest-cov |
