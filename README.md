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

Jarvis is a fully local AI assistant. It accepts text, voice, or file input in Arabic or English and produces either a conversational answer or a real system action.

All processing happens on the local machine. No cloud connection is required. No data leaves the device.

---

## 2. System Architecture

### Layer Map

| Layer | Location | Responsibility | Does NOT |
|-------|----------|----------------|----------|
| Interface | `src/interfaces/` | Receive input, display output | Classify, route, store |
| Context | `src/core/context/` | Assemble InputPacket for current turn | Store across turns |
| Decision | `src/core/decision/` | Classify intent, select model, assign risk | Think, generate |
| Runtime | `src/core/runtime/` | Drive the execution loop | Implement intelligence |
| Agents | `src/core/agents/` | Multi-step reasoning and planning | Route requests |
| Tools (mgmt) | `src/core/tools/` | Registry, validation, safety, execution | Implement tool logic |
| Skills (impl) | `src/skills/` | One specific action per file | Route, decide, store |
| Models | `src/models/` | Wrap AI model I/O | Decide, route, store |
| Memory | `src/core/memory/` | Persist data across turns | Route or classify |
| Identity | `src/core/identity/` | Build system prompts | Make decisions |

---

## 3. Execution Contract

Every stage of the runtime loop exchanges data through one of these four types. These types are binding. No stage passes data outside this contract.

### InputPacket

Produced by: `context.assembler.assemble_context()`
Consumed by: `runtime.loop.run_turn()`

| Field | Type | Description |
|-------|------|-------------|
| user_message | str | Raw text from user |
| session_id | str | Unique session identifier |
| attachments | list[Attachment] | Files, images, audio — paths only, no content |
| memory_snippets | list[str] | Top-N semantic matches from long-term memory |
| recent_history | list[Message] | Last N turns from short-term memory |
| user_profile | UserProfile | Language, style, technical level |
| tool_results | list[ToolResult] | Results from Act steps this turn |
| turn_number | int | Monotonically increasing per session |

### DecisionOutput

Produced by: `core.decision.decision.decide()`
Consumed by: `runtime.executor.execute_turn()`

| Field | Type | Allowed Values |
|-------|------|----------------|
| intent | str | chat · code · tool_use · search · vision · research · voice |
| complexity | str | low · medium · high |
| mode | str | fast · normal · deep · planning · research |
| model | str | Exact Ollama model tag |
| requires_tools | bool | — |
| requires_planning | bool | — |
| tool_name | str or null | — |
| tool_args | dict | — |
| confidence | float | 0.0 to 1.0 |
| risk_level | str | low · medium · high |

### LLMOutput

Produced by: `runtime.executor.execute_turn()` after calling the model
Consumed by: `runtime.loop` to branch between answer and tool execution

| Field | Type | Description |
|-------|------|-------------|
| type | str | "answer" or "tool_call" |
| content | str | Populated when type="answer" |
| tool | str | Populated when type="tool_call" |
| args | dict | Populated when type="tool_call" |

**Enforcement rule:** When `requires_tools=True` in the `DecisionOutput`, the model must produce `type="tool_call"`. Any free-text response when a tool is required is a parse failure and triggers a retry.

### ToolResult

Produced by: `core.tools.executor.execute_tool()`
Consumed by: `runtime.loop` as the next observation

| Field | Type | Description |
|-------|------|-------------|
| tool | str | Tool name that was called |
| success | bool | — |
| data | dict | Tool-specific result payload |
| error | str | Empty string when success=True |
| duration_ms | float | Execution time in milliseconds |

### FinalResponse

Produced by: `runtime.loop` when the evaluator approves
Consumed by: Interface layer for display

| Field | Type | Description |
|-------|------|-------------|
| text | str | The response text |
| session_id | str | — |
| model | str | Model that produced the response |
| mode | str | Mode used |
| quality | float | Evaluator score 0.0 to 1.0 |

---

## 4. Runtime Loop

The loop runs for every user turn. It terminates when the evaluator approves the response or when `max_iterations` is reached.

```
START turn
  packet = assemble_context(user_input, session_id)

  LOOP (max_iterations from config):
    decision = decide(packet)
    output   = execute_turn(decision, packet)

    IF output.type == "tool_call":
      IF output.tool is empty (parse failure):
        → return user-facing error message
      result = execute_tool(output.tool, output.args)
      packet.tool_results.append(result)
      CONTINUE (tool result becomes next observation)

    IF output.type == "answer":
      eval = evaluate(output, decision)
      IF eval.should_retry:
        next = get_next_escalation(decision.mode, decision.model)
        IF next is None:
          BREAK (already at max escalation)
        decision.mode, decision.model = next
        CONTINUE
      ELSE:
        BREAK (approved)

  END LOOP

  IF no approved answer after loop: return FinalResponse with last content
  save_to_memory(session_id, user_input, response)
  return FinalResponse
END turn
```

**Stop conditions:**

| Condition | Action |
|-----------|--------|
| Evaluator returns `should_retry=False` | Break, return response |
| `max_iterations` reached | Return best available with exhaustion note |
| Parse failure after `max_tool_retries` retries | Return error message |
| All escalation levels exhausted | Return best available |

**Fallback:** When all iterations are exhausted without an approved answer, return the last generated content with the note: "This response may be incomplete."

---

## 5. Tool Execution Flow

Every tool call follows this exact path. No shortcut is permitted.

```
LLM produces output
  ↓
parse_llm_output(raw_text, requires_tools)
  ↓
IF parse fails AND requires_tools=True:
  → retry with explicit JSON instruction (max_tool_retries)
  → if still fails: return ToolResult(success=False, error="parse failure")
  ↓
Registry lookup: registry.get(output.tool)
  ↓
IF tool not found:
  → return ToolResult(success=False, error="Tool not found")
  ↓
classify_safety(tool_name, args) → SafetyResult
  ↓
should_execute(safety_result, execution_mode)
  ↓
IF False (blocked): return ToolResult(success=False, error="Blocked by safety policy")
IF "confirm": prompt user → if declined: return ToolResult(success=False, error="User declined")
IF True: proceed
  ↓
validate_args(args, tool.get_schema())
  ↓
IF validation fails: return ToolResult(success=False, error="Invalid args: {detail}")
  ↓
tool.execute(**args)
  ↓
Return ToolResult
  ↓
Append to packet.tool_results
  ↓
Re-enter observe step (CONTINUE loop)
```

---

## 6. Tool JSON Format

### Tool Call (LLM → Runtime)

When a tool is needed, the model must output exactly this JSON and nothing else. No surrounding text is permitted.

```
{
  "type": "tool_call",
  "tool": "<exact_tool_name>",
  "args": { "<param>": "<value>" }
}
```

**Rules:**
- `type` must equal the string `"tool_call"`.
- `tool` must match a registered tool name exactly (case-sensitive).
- `args` must be a JSON object. Empty args: `{}`.
- When `requires_tools=True`, any response that is not this JSON is a parse failure.

### Tool Result (Runtime → LLM)

After execution, the runtime injects this into the next loop iteration as a system message:

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

1. Log the failure.
2. Retry the LLM call with an appended instruction: output only JSON in the required format.
3. If still failing after `max_tool_retries`: return `ToolResult(success=False, error="Model did not produce valid tool call after {n} retries")`.
4. The runtime treats this as a tool failure and returns a user-facing error message.

---

## 7. Boot Flow

The following steps execute in order when `python app/main.py` is called. No step may be skipped. Each step must log its completion.

| Step | Action | Failure behavior |
|------|--------|-----------------|
| 1 | Parse CLI arguments (`--interface`, `--debug`) | Abort with usage message |
| 2 | Load `config/settings.yaml` and `.env` into `AppSettings` | Abort with clear error |
| 3 | Initialize Loguru logging to terminal + `logs/jarvis.log` | Abort with clear error |
| 4 | Create all directories from config `paths` section | Abort if cannot create |
| 5 | Connect to Redis (short-term memory) | Switch to in-memory fallback, log warning |
| 6 | Connect to ChromaDB (long-term memory) | Disable semantic recall, log warning |
| 7 | Connect to SQLite (`data/jarvis.db`) | Abort — SQLite is critical |
| 8 | Scan `src/skills/` and register available tools | Log count; continue on partial failure |
| 9 | Validate model tags from config against `ollama list` | Log warning per missing model; do not abort |
| 10 | Load user profile from `data/user_profile.json` | Create with defaults if missing |
| 11 | Start selected interface | Abort if interface fails to start |
| 12 | Log "Jarvis ready" and display ready message to user | — |

---

## 8. System Start Behavior

When the system receives the first message of a new session:

**Memory:** Empty. `recent_history=[]` and `memory_snippets=[]`. The system functions correctly in this state.

**Context:** Built from user message and user profile only.

**Identity:** System prompt uses Jarvis identity and user profile regardless of memory state.

**Models:** No model is pre-loaded. First `swap_to()` call triggers the actual model load. Expect latency on the first response.

**Behavior:** Absence of memory does not cause an error. The system produces a response based on the current message and identity alone.

---

## 9. Execution Modes (Safety)

Every tool execution is governed by an Execution Mode. The mode is read from `config/settings.yaml` under `runtime.execution_mode`. Default: `"balanced"`.

### Mode Definitions

| Mode | Value | Behavior |
|------|-------|----------|
| SAFE | `"safe"` | Every tool call requires confirmation before execution |
| BALANCED | `"balanced"` | Low-risk: auto-execute. Medium-risk: require confirmation. High-risk: blocked unless explicit override. |
| UNRESTRICTED | `"unrestricted"` | All tools execute without confirmation |

### Risk Classification

| Risk Level | Examples | SAFE | BALANCED | UNRESTRICTED |
|-----------|---------|------|----------|-------------|
| `low` | web_search, read_file, system_info, take_screenshot | Confirm | Auto-execute | Auto-execute |
| `medium` | open_app, execute_python, run_shell, send_notification | Confirm | Confirm | Auto-execute |
| `high` | delete_file, kill_process, send_email, send_message, whatsapp_send | Confirm | Blocked* | Auto-execute |

*In BALANCED mode, a high-risk tool is blocked until the user sends the explicit override phrase: `"confirm: {tool_name}"` as a separate message.

### Runtime Connection

- `Decision.risk_level` is set from `config/skills.yaml` for the classified `tool_name`.
- `mode_enforcer.should_execute()` reads the current `execution_mode` from config and returns: `True` (auto), `False` (block), or `"confirm"` (pause).
- The executor applies the result before calling `tool.execute()`.
- Mode can be changed at runtime via the CLI `/mode safe|balanced|unrestricted` command.

---

## 10. Prompt System

Every model call receives a system prompt assembled by the Prompt Builder. The prompt is not static — it is built from components in a fixed order on every call.

### Assembly Order

| Block | Source | Condition |
|-------|--------|-----------|
| 1. Jarvis identity | `config/jarvis_identity.yaml` | Always |
| 2. Safety rules | `config/jarvis_identity.yaml` | Always |
| 3. User profile | `data/user_profile.json` | Always |
| 4. Mode fragment | `src/core/identity/personality.py` | Always |
| 5. Task context | Current `user_message` | Always |
| 6. Tool list | `registry.to_ollama_format()` | Only when `requires_tools=True` |
| 7. Handoff note | Previous and current model names | Only when model was just swapped |

### Thinking Mode Fragments

| Mode | Instruction |
|------|-------------|
| `fast` | Answer in one to three sentences. No elaboration. |
| `normal` | Provide a complete, well-structured answer. |
| `deep` | Reason step by step. Show reasoning. Verify the answer before finalizing. |
| `planning` | Decompose the goal into numbered steps before executing any of them. |
| `research` | Use multiple sources. Attribute each claim. Summarize at the end. |

---

## 11. Decision System

The Decision Layer classifies the current turn and selects resources. It does not generate content. It does not call a model for reasoning.

### Classification Rules

| Signal | Decision |
|--------|----------|
| Image in `attachments` | intent=vision, model=llava:7b |
| Code keywords in message | intent=code, model=qwen2.5-coder:7b |
| Message length < 20 chars, no action keywords | intent=chat, mode=fast, model=gemma3:4b |
| Multi-step goal detected | mode=planning, model=qwen3:8b |
| Default | intent=chat, mode=normal, model=qwen3:8b |

### Model Selection Rules

| Signal | Model |
|--------|-------|
| Image present | `llava:7b` |
| intent == "code" | `qwen2.5-coder:7b` |
| complexity == "low" AND mode == "fast" | `gemma3:4b` |
| All other cases | `qwen3:8b` |

### Escalation Chain

When the evaluator rejects a response, the runtime escalates in this order:

| Level | Mode | Model |
|-------|------|-------|
| 0 | fast | gemma3:4b |
| 1 | normal | qwen3:8b |
| 2 | deep | qwen3:8b |

`get_next_escalation(mode, model)` returns the next level or `None` if already at the maximum.

---

## 12. Memory System

| Store | Backend | Scope | Contents | Failure behavior |
|-------|---------|-------|----------|-----------------|
| Short-term | Redis (in-memory fallback) | Current session | Last 50 messages per session | Switch to in-memory; log warning |
| Long-term | ChromaDB | Cross-session | Facts, outcomes, preferences | Disable semantic recall; log warning |
| Structured | SQLite | Permanent | Conversations, tasks, feedback | Abort — critical store |
| Profile | JSON file | Permanent | User preferences | Create with defaults |

Memory injection per turn:
- Short-term: last 10 messages from current session
- Long-term: top 3 semantically similar snippets for the current message
- Profile: injected into every turn via Prompt Builder

---

## 13. Models

| Ollama Tag | Role | VRAM | Best For |
|-----------|------|------|----------|
| `qwen3:8b` | Main brain | 5.0 GB | Arabic, deep reasoning, planning |
| `gemma3:4b` | Fast responder | 3.0 GB | Quick answers, classification |
| `qwen2.5-coder:7b` | Code specialist | 4.7 GB | Code generation and debugging |
| `llava:7b` | Vision | 4.5 GB | Image understanding, OCR |

**VRAM rule:** One model loaded at a time. Before loading a new model, unload the current one. Never load two models simultaneously.

---

## 14. Skills

All tool implementations are in `src/skills/`. Each file contains one or more `BaseTool` subclasses.

| Category | Location | Tools |
|----------|----------|-------|
| system | `src/skills/system/` | open_app, close_app, system_info, kill_process, clipboard |
| files | `src/skills/files/` | read_file, write_file, delete_file, list_directory, search_files |
| browser | `src/skills/browser/` | navigate, click, fill, get_text, download, upload, session |
| search | `src/skills/search/` | web_search, fetch_page |
| api | `src/skills/api/` | calendar, gmail, drive, contacts, youtube |
| screen | `src/skills/screen/` | take_screenshot, read_screen_text, describe_screen |
| coder | `src/skills/coder/` | execute_python, run_shell |
| notify | `src/skills/notify/` | send_notification |
| social | `src/skills/social/` | whatsapp_send, whatsapp_read |
| media | `src/skills/media/` | play_pause, set_volume, next_track |
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
| Volume | pycaw | pactl / amixer | osascript |
| Clipboard text | pyperclip | pyperclip | pyperclip |
| Clipboard image | win32clipboard | xclip | pbpaste |
| Hotkeys | keyboard lib | pynput | pynput |
| Auto-start | Registry Run key | ~/.config/autostart/ | ~/Library/LaunchAgents/ |

All file paths use `pathlib.Path`. No hardcoded path separators anywhere.

---

## 16. Error Handling

| Error Class | Cause | Action |
|-------------|-------|--------|
| `model_error` | Ollama unreachable or OOM | Retry with smaller model |
| `tool_not_found` | Tool name not in registry | Return ToolResult(success=False); LLM explains |
| `parse_failure` | LLM output not valid tool call JSON | Retry with explicit instruction (max_tool_retries) |
| `validation_error` | Args fail JSON Schema check | Return ToolResult(success=False); LLM retries with corrected args |
| `safety_blocked` | risk=high in BALANCED mode | Explain to user; require explicit override phrase |
| `user_declined` | User rejected confirmation | Return "Action cancelled" message |
| `tool_timeout` | Execution exceeded timeout | Return ToolResult with timeout error |
| `vram_oom` | GPU out of memory | Unload all models; load smallest; retry |

---

## 17. Configuration Reference

All configuration lives in `config/settings.yaml`. No tunable parameter exists as a Python constant.

| Section | Key fields |
|---------|-----------|
| `jarvis` | name, language, wake_word |
| `models` | default, fast, code, vision |
| `hardware` | gpu_vram_limit_gb, max_concurrent_models, model_idle_timeout_s |
| `interfaces` | web_host, web_port |
| `paths` | data, logs, chroma, sqlite, sessions, downloads, screenshots, generated |
| `hotkeys` | open_cli, start_voice |
| `runtime` | max_iterations, max_tool_retries, tool_timeout_s, execution_mode |

---

## 18. Logging

All log entries use key=value structured format.

| Event | Required fields |
|-------|----------------|
| `turn.start` | session, input_len, turn |
| `decision` | intent, model, mode, risk_level |
| `tool.start` | name, risk_level, execution_mode |
| `tool.done` | name, success, duration_ms |
| `tool.blocked` | name, reason |
| `tool.parse_failure` | attempt, raw_len |
| `eval` | quality, should_retry, reason |
| `model.swap` | from, to |
| `turn.end` | session, quality, total_ms |

Log file: `logs/jarvis.log` — INFO level, 10 MB rotation, 7-day retention.
Debug file: `logs/debug.log` — DEBUG level, enabled by `JARVIS_DEBUG=1`.

---

## 19. Quick Start

```
pip install -r requirements.txt
playwright install chromium

ollama pull qwen3:8b
ollama pull qwen2.5-coder:7b
ollama pull gemma3:4b
ollama pull llava:7b

cp config/settings.example.yaml config/settings.yaml
cp .env.example .env

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
| STT | OpenAI Whisper (medium) |
| TTS | Piper TTS |
| Wake Word | openWakeWord |
| Image Gen | Diffusers — Stable Diffusion 1.5 |
| Browser | Playwright (Chromium) |
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
