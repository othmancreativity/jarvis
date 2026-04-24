# 🤖 JARVIS

## Local AI Assistant System — Arabic + English — Free, Unlimited, Private

---

## 1. System Overview

Jarvis is a fully local AI assistant system. It accepts text, voice, or file input in Arabic or English and produces either a conversational answer or a real system action — opening applications, searching the web, managing files, sending notifications.

**Core Philosophy:**
- **Local-first:** All processing occurs on the local machine. No cloud connection is required. No data leaves the device.
- **Modular:** Each layer has a single defined responsibility. No layer crosses into another's scope.
- **Controllable:** Execution modes determine what actions require confirmation.

---

## 2. Architecture

### Layer Responsibilities

| Layer | Location | Responsibility | Does |
|-------|----------|--------------|-------|
| **Interface** | `src/interfaces/` | Receive input, display output | Classify, route, or store |
| **Context** | `src/core/context/` | Bundle this turn's inputs into InputPacket | Store across turns |
| **Decision Engine** | `src/core/decision/` | Classify intent, select model and mode | Think or generate content |
| **Runtime** | `src/core/runtime/` | Drive the execution loop | Implement intelligence |
| **Agents** | `src/core/agents/` | Multi-step reasoning and planning | Route requests |
| **Tools** | `src/core/tools/` | Registry, validation, execution bridge | Implement tool logic |
| **Skills** | `src/skills/` | One specific action per file | Decisions or routing |
| **Memory** | `src/core/memory/` | Persist data across turns | Participate in routing |
| **Models** | `src/models/` | Wrap AI model I/O | Decisions or memory |
| **Identity** | `src/core/identity/` | Build system prompts | Route or decide |

### Runtime Authority

**The Runtime is the ONLY authority controlling:**
- Flow execution direction
- Retry decisions and limits
- Model switching
- Loop termination

**No other module may control these aspects.**

### Tool Execution Boundaries

**Tools MUST NOT:**
- Call any LLM
- Make routing decisions
- Access the Runtime loop
- Modify execution flow

Tools are pure executors. They receive input, produce output, and return.

---

## 3. Execution Flow

### Step-by-Step Flow

```
User Input → Context → Decision → Model → Tool (optional) → Runtime → Final Response
```

1. **User Input:** Received by Interface layer
2. **Context:** InputPacket assembled with user message, session data, memory
3. **Decision:** Intent classified, model and mode selected
4. **Model:** LLM generates response or tool call
5. **Tool (optional):** Tool executes if needed, returns result
6. **Runtime:** Evaluates response, decides to retry or approve
7. **FinalResponse:** Returned to Interface for display

### Runtime Loop

```
START turn
  input = assemble_context(user_input, session_id)
  LOOP (max_iterations = 5):
    decision = decide(input)
    output   = execute_turn(decision, input)
    IF output.type == "tool_call":
      result = execute_tool(output.tool, output.args)
      input.tool_results.append(result)
      CONTINUE loop
    IF output.type == "answer":
      eval = evaluate(output, decision)
      IF eval.should_retry:
        CONTINUE loop
      ELSE:
        BREAK
  END LOOP
  save to memory
  return FinalResponse
END turn
```

---

## 4. Data Contracts

All data shapes exchanged between stages are **binding**. No stage may pass data outside this contract.

### InputPacket

**Produced by:** `context.assembler.assemble_context()`  
**Consumed by:** `runtime.loop.run_turn()`

```json
{
  "user_message": "string",
  "session_id": "string",
  "attachments": [],
  "memory_snippets": [],
  "recent_history": [],
  "user_profile": {"language": "string", "style": "string", "technical_level": "string"},
  "tool_results": [],
  "turn_number": 0
}
```

### DecisionOutput

**Produced by:** `core.decision.decision.decide()`  
**Consumed by:** `runtime.executor.execute_turn()`

```json
{
  "intent": "chat|code|tool_use|search|vision|research|voice",
  "complexity": "low|medium|high",
  "mode": "fast|normal|deep|planning|research",
  "model": "qwen3:8b",
  "requires_tools": true,
  "requires_planning": false,
  "tool_name": "open_app",
  "tool_args": {"name": "string"},
  "confidence": 0.9,
  "risk_level": "low|medium|high"
}
```

### LLMOutput

**Produced by:** `runtime.executor.execute_turn()` after calling the model  
**Consumed by:** `runtime.loop` to branch between direct answer and tool execution

```json
{
  "type": "answer|tool_call",
  "content": "string",
  "tool": "string",
  "args": {}
}
```

**Enforcement Rule:** When `requires_tools=True` in `DecisionOutput`, the model **MUST** produce a `tool_call` type response. Any free-text response when a tool is required is a **parse failure** and triggers a retry.

### ToolResult

**Produced by:** `core.tools.executor.execute_tool()`  
**Consumed by:** `runtime.loop` as the next observation

```json
{
  "tool": "string",
  "success": true,
  "data": {},
  "error": "",
  "duration_ms": 0.0
}
```

### FinalResponse

**Produced by:** `runtime.loop` when evaluator approves  
**Consumed by:** Interface layer for display

```json
{
  "text": "string",
  "session_id": "string",
  "model": "qwen3:8b",
  "mode": "normal",
  "quality": 0.85
}
```

---

## 5. Execution Modes

Every tool execution is governed by an Execution Mode. The mode determines whether confirmation is required before running a tool.

### Mode Definitions

| Mode | Value | Behavior |
|------|-------|----------|
| **SAFE** | `safe` | Every tool call requires explicit user confirmation before execution |
| **BALANCED** | `balanced` | Low-risk tools auto-execute; medium-risk require confirmation; high-risk are blocked |
| **UNRESTRICTED** | `unrestricted` | All tools execute without confirmation |

**Default mode:** `BALANCED`

The active mode is stored in `config/settings.yaml` under `runtime.execution_mode`.

### Risk Classification

| Risk Level | SAFE | BALANCED | UNRESTRICTED |
|------------|------|----------|--------------|
| **low** | Requires confirmation | Auto-executes | Auto-executes |
| **medium** | Requires confirmation | Requires confirmation | Auto-executes |
| **high** | Requires confirmation | Blocked | Auto-executes |

**Blocked behavior for `high` in BALANCED:** The tool does not execute. The runtime returns a message explaining that this action requires either switching to UNRESTRICTED mode or typing the explicit approval phrase: `"confirm: {tool_name}"`.

### Explicit Approval Phrase

When the user types `"confirm: {tool_name}"` as their next message, the high-risk tool is treated as medium-risk for that one call only.

---

## 6. Tools System

### Tool Structure

Every tool is a `BaseTool` subclass with:
- `name`: Unique identifier
- `description`: Human-readable description
- `category`: Grouping (system, files, browser, search, api, coder, etc.)
- `risk_level`: low | medium | high
- `requires_confirmation`: bool
- `platform`: list of supported platforms

### Registry

Tools are auto-discovered from `src/skills/` directory and registered at startup.

### Execution Pipeline

```
LLM output → Parse → Validate schema → Safety check → Mode enforcement → Execute → Return ToolResult
```

### Parse Failure Handling

When the LLM output cannot be parsed as valid tool call JSON:
1. Log the failure with raw text
2. Re-send request with explicit JSON instruction
3. Retry maximum 2 times
4. If still failing: return `ToolResult(success=False, error="Model did not produce valid tool call")`

---

## 7. Model Strategy

### Model Selection

| Ollama Tag | Role | VRAM | Use Case |
|-----------|------|------|----------|
| `qwen3:8b` | Main brain | 5.0 GB | Arabic, reasoning, planning, general |
| `gemma3:4b` | Fast responder | 3.0 GB | Quick answers, classification |
| `qwen2.5-coder:7b` | Code specialist | 4.7 GB | Code generation, debugging |
| `llava:7b` | Vision | 4.5 GB | Image understanding, OCR |

### VRAM Rule

**One model loaded at a time.** Before loading a new model, unload the current one. Two models must never be loaded simultaneously on a 6 GB GPU.

### Fallback Logic

On model failure:
1. Retry with the same model (max 2 times)
2. If still failing: switch to fallback model (gemma3:4b)
3. If fallback fails: return error message to user

---

## 8. Error Handling

| Error | Cause | Action |
|-------|-------|--------|
| `model_error` | Ollama unreachable or OOM | Retry with smaller model |
| `tool_not_found` | Tool name not in registry | Return error to LLM |
| `parse_failure` | LLM output not valid JSON | Retry with JSON instruction (max 2) |
| `validation_error` | Args fail JSON Schema | Return error; LLM can retry |
| `safety_blocked` | risk=high in BALANCED | Explain; require approval phrase |
| `user_declined` | User rejected confirmation | Return "Action cancelled" |
| `tool_timeout` | Execution exceeded time limit | Return error; continue turn |
| `vram_oom` | GPU out of memory | Unload all; load smallest; retry |

---

## 9. Logging System

Logging is a **CORE** runtime layer. Structured logs use key=value format.

### Event Types

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
| `model.error` | model, error_type, details |
| `retry` | attempt, reason, success |
| `escalation` | from_mode, from_model, to_mode, to_model |
| `turn.end` | session, quality, total_ms |

### Log File

`logs/jarvis.log` — INFO and above, 10 MB rotation, 7-day retention.

---

## 10. Security Model

### File Restrictions

- All paths must be under user's home directory or configured `data/` directory
- Paths outside these roots are rejected at the tool level

### Dangerous Command Blocking

Blocked patterns (any tool argument containing these is blocked regardless of risk level):
- `rm -rf`
- `format c:`
- `del /s /q`
- `:(){:|:&};:`
- `shutdown /`
- `mkfs`
- `dd if=`

### Confirmation Phrases

- `"confirm: {tool_name}"` — grants one-time execution for high-risk tools

### Secrets Protection

- `.env` file contains all secrets
- File is gitignored
- No secrets logged or exposed in responses

---

## 11. Local vs External Modules

### Core (Local - Always Active)

| Module | Description |
|--------|-------------|
| Interface | CLI, Web UI, Voice |
| Context | InputPacket assembly |
| Decision | Intent classification |
| Runtime | Execution loop |
| Agents | Multi-step reasoning |
| Tools | Registry, validation |
| Skills | Local tool implementations |
| Memory | Redis, ChromaDB, SQLite |
| Models | Ollama wrapper |
| Identity | Prompt building |

### External (Optional Modules)

| Module | Description | Enable |
|--------|-------------|--------|
| Telegram | Telegram bot interface | Optional |
| Google APIs | Calendar, Gmail, Drive | Optional |
| Browser | Playwright automation | Optional |
| Voice | STT/TTS pipeline | Optional |

---

## 12. Implementation Mapping

### Phase → Architecture

| Phase | Component | Files Created |
|-------|-----------|---------------|
| 0 | Core | engine.py, classifier.py, apps.py, jarvis_slice.py |
| 1 | Config, Logging | config.py, logging_setup.py |
| 2 | Contracts | InputPacket, DecisionOutput, LLMOutput, ToolResult, FinalResponse |
| 3 | Runtime Loop | assembler.py, decision.py, executor.py, evaluator.py, loop.py |
| 4 | Decision System | Classifier hardening, fast-path, risk levels |
| 5 | Identity | identity.yaml, prompt builder |
| 6 | Tool System | BaseTool, registry, safety, executor |
| 7 | Safety Modes | Execution mode enforcement |
| 8 | System Skills | App, system info, clipboard, notifications, file ops |
| 9 | Browser | Playwright automation |
| 10 | Google APIs | OAuth + Calendar, Gmail, Drive |
| 11 | Memory | Short-term, long-term, SQLite |
| 12 | Agents | Thinker, Planner, Researcher |
| 13-17 | Interfaces | CLI, Web, Voice, Telegram, GUI |

---

## 13. Quick Start

```bash
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

## 14. Tech Stack

| Layer | Technology |
|-------|-----------|
| LLM Runtime | Ollama |
| Web Framework | FastAPI + Uvicorn |
| Vector DB | ChromaDB |
| Cache | Redis |
| SQL | SQLite |
| STT | OpenAI Whisper |
| TTS | Piper TTS |
| Browser | Playwright |
| Terminal UI | Rich |
| Config | PyYAML + Pydantic |
| Logging | Loguru |
| Testing | pytest |

---

*Version 1.0.0-alpha*