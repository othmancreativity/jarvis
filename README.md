# JARVIS — Production-Ready AI Assistant System

## System Overview

Jarvis is a local-first AI assistant system with strict runtime bounds, hardware awareness, and comprehensive failure handling.

**Hardware Constraints:**
- GPU: NVIDIA RTX 3050 (6GB VRAM)
- RAM: 16 GB
- CPU: Intel i5 12th Gen

**Core Guarantees:**
- No infinite loops
- No unbounded recursion
- Graceful degradation on failure
- Full debuggability
- Hardware-safe model management

---

## 1. Architecture

### Layer Responsibilities

| Layer | Location | Responsibility | Does NOT Do |
|-------|----------|---------------|--------------|
| **Interface** | `src/interfaces/` | Input/Output | Decision, routing |
| **Context** | `src/core/context/` | Bundle InputPacket | Store across turns |
| **Decision** | `src/core/decision/` | Intent classification | Content generation |
| **Runtime** | `src/core/runtime/` | State machine, loop control | Tool implementation |
| **Agents** | `src/core/agents/` | Multi-step planning | Direct tool execution |
| **Tools** | `src/core/tools/` | Registry, safety, execution | LLM calls |
| **Skills** | `src/skills/` | Tool implementations | Routing decisions |
| **Memory** | `src/core/memory/` | Data persistence | Runtime control |
| **Models** | `src/models/` | LLM wrapper | Decision making |
| **Identity** | `src/core/identity/` | Prompt building | Execution control |

---

## 2. Runtime State Machine

The runtime operates as a finite state machine. Each state has defined transitions.

### States

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│    ┌──────────┐    ┌──────────┐    ┌──────────────┐       │
│    │          │    │          │    │              │       │
│    ▼          ▼    ▼          ▼    ▼              ▼       │
│  IDLE ──► DECIDING ──► EXECUTING_MODEL ──► EVALUATING      │
│    ▲                                           │          │
│    │              ┌──────────────┐              │          │
│    │              │              │              │          │
│    │              ▼              ▼              ▼          │
│    │          WAITING_     EXECUTING_      COMPLETED       │
│    │         CONFIRMATION    TOOL                         │
│    │              │              │              │          │
│    │              ▼              ▼              │          │
│    └───────── ERROR ◄─────────┴─────────────────┘          │
│         (safe exit to IDLE with error response)             │
└─────────────────────────────────────────────────────────────┘
```

### State Definitions

| State | Description | Allowed Next States |
|-------|-------------|-----------------|
| **IDLE** | Waiting for input | DECIDING |
| **DECIDING** | Running decision classifier | EXECUTING_MODEL, ERROR, IDLE |
| **EXECUTING_MODEL** | Calling LLM | EVALUATING, EXECUTING_TOOL, ERROR |
| **EXECUTING_TOOL** | Running approved tool | EVALUATING, ERROR |
| **WAITING_CONFIRMATION** | Paused for user approval | EXECUTING_TOOL, IDLE (if declined) |
| **EVALUATING** | Checking response quality | DECIDING (retry), COMPLETED, ERROR |
| **ERROR** | Failure state | IDLE |
| **COMPLETED** | Success state | IDLE |

### Invalid Transitions

| From | To | Handling |
|------|-----|----------|
| IDLE | EXECUTING_TOOL | Reject - must go through DECIDING |
| EXECUTING_MODEL | IDLE | Reject - invalid without EVALUATING |
| WAITING_CONFIRMATION | EXECUTING_TOOL | Only after user response |
| Any | Any with no path | ERROR state + log |

### State Logging

Every state transition logs:
- `runtime.state` = from_state → to_state
- `runtime.iteration` = current turn iteration
- `runtime.tool_depth` = nested tool call depth

---

## 3. Execution Flow (Runtime-Safe)

### Hard Limits

| Limit | Value | Purpose |
|-------|-------|---------|
| `max_iterations` | 5 | Maximum retry loops per turn |
| `max_tool_depth` | 3 | Maximum nested tool calls |
| `max_retries` | 2 | Model call retries per attempt |
| `tool_timeout_s` | 30 | Tool execution timeout |
| `model_timeout_s` | 120 | LLM call timeout |
| `total_turn_timeout_s` | 300 | Maximum turn time (5 min) |

### Execution Loop

```
START run_turn(user_input, session_id)
  ┌─────────────────────────────────────────────┐
  │ SET turn_start_time = now()                  │
  │ SET current_state = IDLE                   │
  │ SET iteration = 0                         │
  │ SET tool_depth = 0                         │
  └─────────────────────────────────────────────┘
                                                    
  input = assemble_context(user_input, session_id)
  
  ┌─────────────────────────────────────────────┐
  │ TRANSITION: IDLE → DECIDING                  │
  │ LOG: state.transition, iteration            │
  └─────────────────────────────────────────────┘
                                                    
  LOOP (iteration < max_iterations):
    decision = decide(input)
    
    ┌─────────────────────────────────────────────┐
    │ VALIDATE decision:                        │
    │ - intent is valid enum value           │
    │ - model is available                  │
    │ - tool_name matches intent            │
    │ IF invalid: force intent=chat        │
    └─────────────────────────────────────────────┘
                                                    
    ┌─────────────────────────────────────────────┐
    │ TRANSITION: DECIDING → EXECUTING_MODEL       │
    │ LOG: decision.intent, decision.model    │
    └─────────────────────────────────────────────┘
                                                    
    output = execute_turn(decision, input)
    
    ┌─────────────────────────────────────────────┐
    │ CHECK timeout:                         │
    │ IF elapsed > total_turn_timeout:      │
    │   RETURN timeout_error_response     │
    │ END                                  │
    └─────────────────────────────────────────────┘
                                                    
    IF output.type == "tool_call":
      ┌──────────────���─��────────────────────────┐
      │ TOOL CHAIN PROTECTION:                │
      │ IF tool_depth >= max_tool_depth:       │
      │   RETURN error: "tool depth exceeded"│
      │ END                                │
      └─────────────────────────────────────────┘
                                               
      ┌─────────────────────────────────────────┐
      │ TRANSITION: EXECUTING_MODEL →         │
      │ EXECUTING_TOOL                        │
      │ LOG: output.tool, output.args         │
      └─────────────────────────────────────────┘
                                               
      result = execute_tool(output.tool, output.args)
      
      ┌─────────────────────────────────────────┐
      │ VALIDATE result:                      │
      │ - success must be boolean            │
      │ - error must be string           │
      │ - data must be dict             │
      └─────────────────────────────────────────┘
                                               
      input.tool_results.append(result)
      tool_depth += 1
      
      ┌─────────────────────────────────────────┐
      │ TOOL CHAIN DETECTION:                │
      │ IF repeated_tool(output.tool):      │
      │   BREAK with warning               │
      │ END                                │
      └─────────────────────────────────────────┘
                                               
      IF result.success == false:
        ┌─────────────────────────────────────┐
        │ TOOL FAILURE HANDLING:             │
        │ Log: tool, error                 │
        │ Add error context to input       │
        │ CONTINUE (up to max_iterations)│
        └─────────────────────────────────────┘
        CONTINUE
      
      ┌─────────────────────────────────────┐
      │ TRANSITION: EXECUTING_TOOL →         │
      │ EVALUATING                        │
      └─────────────────────────────────────┘
      CONTINUE
    
    IF output.type == "answer":
      ┌────────────────────────────────────────────────┐
      │ TRANSITION: EXECUTING_MODEL → EVALUATING      │
      │ LOG: output.content[:100]                  │
      └──────────────────────────────────────────┘
      
      eval = evaluate(output, decision)
      
      IF eval.should_retry AND iteration < max_iterations - 1:
        ┌────────────────────────────────────────┐
        │ LOG: retry.reason                     │
        │ ESCALATE if needed:                  │
        │ - increase mode depth                │
        │ - swap to smarter model              │
        │ CONTINUE                           │
        └��─────────────────────────────────────┘
        iteration += 1
        CONTINUE
      
      ┌────────────────────────────────────────┐
      │ TRANSITION: EVALUATING → COMPLETED     │
      │ BREAK                             │
      └────────────────────────────────────┘
      BREAK
  
  ┌────────────────────────────────────────┐
  │ EXIT LOOP                            │
  │ IF iteration >= max_iterations:      │
  │   RETURN exhaustion_response     │
  │ END                              │
  └────────────────────────────────────────┘
  
  ┌────────────────────────────────────────┐
  │ POST-TURN:                          │
  │ - save to memory                 │
  │ - log turn.end with quality      │
  │ - UPDATE: state = COMPLETED      │
  └────────────────────────────────────────┘
  
  RETURN FinalResponse
END run_turn
```

---

## 4. Tool Permission Layer (CRITICAL SECURITY)

Before ANY tool executes, three validation gates pass.

### Gate 1: Decision Consistency

```
VALIDATE decision_consistency(decision, output):
  IF decision.requires_tools == true:
    IF output.type != "tool_call":
      REJECT: "Model promised tool but returned text"
    
    IF decision.tool_name != output.tool:
      LOG: "Tool mismatch: expected {decision.tool_name}, got {output.tool}"
      IF output.tool is valid:
        # Tool substitution is sometimes valid
        LOG: "tool_substitution"
        ALLOW with warning
      ELSE:
        REJECT: "Invalid tool substitution"
  
  IF decision.requires_tools == false:
    IF output.type == "tool_call":
      LOG: "Unexpected tool call when not required"
      # Check if it's a reasonable safety check
      IF output.tool == "system_info":
        ALLOW
      ELSE:
        REJECT: "Tool not requested"
```

### Gate 2: Argument Safety

```
VALIDATE argument_safety(tool_name, args):
  FOR each key, value in args:
    IF value is string:
      # Path validation
      IF key contains "path" OR key contains "file":
        resolved = resolve_path(value)
        IF NOT is_safe_path(resolved):
          REJECT: "Unsafe path: {value}"
        
        IF is_dangerous_path(resolved):
          REJECT: "Dangerous path type"
      
      # Command validation
      IF key contains "command" OR key contains "code":
        FOR pattern in DANGEROUS_PATTERNS:
          IF pattern in value:
            REJECT: "Dangerous pattern in {key}"
  
  RETURN ALLOW
```

### Gate 3: User Context

```
VALIDATE user_context(tool_name, user_message):
  # Tools should match user intent
  IF is_standalone_tool(tool_name):
    IF user_message does not imply tool_name:
      # Log warning but allow (user might want this)
      LOG: "unexpected_tool"
  
  # Recent messages check
  recent = get_recent_messages(session_id)
  IF has_conflicting_tools(recent, tool_name):
    LOG: "recent_tool_conflict"
    ALLOW with warning
```

### Dangerous Patterns (Blocked in Gate 2)

```python
DANGEROUS_PATTERNS = [
    "rm -rf /",
    "rm -rf /home",
    "format c:",
    "del /s /q",
    ":(){:|:&};:",
    "shutdown",
    "reboot",
    "mkfs",
    "dd if=",
    "> /dev/sd",
    "curl | bash",
    "wget | bash",
    "chmod 777",
    "chown -R",
]
```

---

## 5. LLM Output Recovery System

LLMs produce unstructured output. This system recovers usable JSON.

### Recovery Pipeline

```
PARSE llm_output(raw_text, requires_tools):
  
  # Step 1: Extract JSON from text
  extracted = extract_json(raw_text)
  
  IF extraction failed:
    GO TO repair_attempt
  
  # Step 2: Validate structure
  validated = validate_structure(extracted, requires_tools)
  
  IF validation failed:
    GO TO repair_attempt
  
  RETURN validated
  
  # --- REPAIR PATH ---
  REPAIR_ATTEMPT:
  ┌──────────────────────────────────┐
  │ Attempt 1: Clean extraction      │
  │ - Remove markdown wrappers     │
  │ - Remove stray text        │
  │ - Find first { and last } │
  │ RETRY                      │
  └──────────────────────────────────┘
  
  IF required_tools == true:
    ┌────────────────────────────────┐
    │ Attempt 2: Force JSON mode     │
    │ - Send correction prompt    │
    │ - "Respond with ONLY JSON" │
    │ RETRY                       │
    └────────────────────────────────┘
  
  ┌──────────────────────────────────┐
  │ Attempt 3: Fallback           │
  │ - Return safe text response │
  │ - Log parse_failure       │
  │ - Mark for retry        │
  └──────────────────────────────────┘
  
  IF all_retries_exhausted:
    ┌─────────────────────────────────┐
    │ FINAL DEGRADATION:            │
    │ IF required_tools == true:    │
    │   Return tool_call with       │
    │   tool="unknown"           │
    │   Parse failure marker      │
    │ ELSE:                      │
    │   Return answer with       │
    │   partial content        │
    └─────────────────────────────────┘
```

### JSON Extraction Algorithm

```python
def extract_json(raw_text):
  # 1. Remove markdown code blocks
  cleaned = remove_markdown(raw_text)
  
  # 2. Find JSON boundaries
  start = cleaned.find('{')
  end = cleaned.rfind('}')
  
  IF start == -1 OR end == -1:
    RETURN failure
  
  # 3. Extract substring
  json_str = cleaned[start:end+1]
  
  # 4. Validate it's parseable
  TRY:
    parsed = json.loads(json_str)
    RETURN success(parsed)
  EXCEPT:
    RETURN failure
```

### Structured Retry Prompt

When parse fails, send this to the model:

```
Your previous response was not valid JSON. 
Respond with ONLY a JSON object and nothing else.
Required format: {"type": "tool_call", "tool": "tool_name", "args": {...}}
Do not include any text before or after the JSON.
```

---

## 6. Debug System

### Debug Modes

| Mode | Enabled Via | Output |
|------|------------|--------|
| **OFF** | Default | No debug info |
| **BASIC** | `--debug` | Key decisions logged |
| **TRACE** | `--trace` | Full step trace |
| **RAW** | `--debug --raw` | LLM output shown |

### Debug Output (when enabled)

```
═══════════════════════════════════════
[TURN START] session=abc123 iteration=0
───────────────────────────────────
[DECISION] intent=tool_use tool=open_app confidence=0.85
[MODEL] loading=gemma3:4b
[OUTPUT RAW] {"type":"tool_call","tool":"open_app","args":{"name":"chrome"}}
[TOOL CALL] open_app(name=chrome)
[TOOL RESULT] success=true duration=1.2s
[EVALUATE] quality=0.9 should_retry=false
[TURN END] quality=0.9 total_time=2.3s
═══════════════════════════════════════
```

### Trace System

Full execution trace stored in memory for replay:

```python
class TurnTrace:
  session_id: str
  turn_number: int
  start_time: datetime
  end_time: datetime
  states: List[StateTransition]  # from, to, timestamp
  decisions: List[DecisionOutput]
  model_calls: List[ModelCall]  # prompt, response
  tool_calls: List[ToolCall]   # tool, args, result
  errors: List[Error]
  final_state: str
```

### Replay Command

```
/replay <session_id> <turn_number>
# Shows complete turn trace
# Can Step-through each state
```

---

## 7. Latency Control

### Time Budgets

| Phase | Timeout | Early Exit |
|-------|---------|-----------|
| Decision (fast path) | 2s | Use default |
| Decision (LLM) | 30s | Retry once |
| Model call | 120s | Fallback to fast model |
| Tool execution | 30s | Timeout error |
| Total turn | 300s (5min) | Return best response |

### Strategy

```
CHECK timeout at each phase:

IF elapsed > soft_limit:
  # Start warning
  LOG: "approaching_timeout"

IF elapsed > hard_limit:
  # Force exit
  IF output.type == "answer":
    RETURN current + "(timeout)"
  ELSE:
    RETURN error_response("timeout")

ALWAYS check before next iteration:
  remaining = total_turn_timeout - elapsed
  IF remaining < expected_min:
    ALLOW final attempt only
```

---

## 8. Hardware-Aware Model Strategy

Given 6GB VRAM constraint STRICT rules apply.

### VRAM Budget

| Model | VRAM Used | Available Headroom |
|-------|----------|-------------------|
| gemma3:4b | 3.0 GB | 3.0 GB (safe) |
| qwen3:8b | 5.0 GB | 1.0 GB (tight) |
| qwen2.5-coder:7b | 4.7 GB | 1.3 GB (tight) |
| llava:7b | 4.5 GB | 1.5 GB (tight) |

### Strict Rules

1. **ONE model at a time** — Unload before loading new model
2. **No concurrent model calls**
3. **Automatic downgrade when VRAM low**

### Model Selection Priority

| Use Case | Preferred | Fallback | Notes |
|---------|-----------|----------|---------|
| Fast classification | gemma3:4b | none | Use fast-path first |
| General chat | qwen3:8b | gemma3:4b | Swap needed |
| Complex reasoning | qwen3:8b | gemma3:4b | May retry once |
| Code | qwen2.5-coder:7b | qwen3:8b | Requires swap |
| Vision | llava:7b | error | Requires swap |

### Model Swap Protocol

```python
def swap_to(model_tag):
  IF model_tag == get_active_model():
    RETURN  # No swap needed
  
  current = get_active_model()
  
  ┌────────────────────────────────┐
  │ CHECK VRAM:                   │
  │ estimated = get_vram_needed(model_tag)│
  │ available = get_vram_available()   │
  │                               │
  │ IF available < estimated:     │
  │   # Force unload all first   │
  │   unload_all_models()        │
  │   IF still not enough:    │
  │     RETURN              │
  │     error("VRAM insufficient")│
  └────────────────────────────────┘
  
  unload_model(current)  # If loaded
  load_model(model_tag)
  
  LOG: model.swap from={current} to={model_tag}
  
  SET active_model = model_tag
```

### Swap Cooldown

After model swap, minimum 5 second cooldown before another swap (prevents thrashing).

### VRAM Monitoring

Before each model call, check available VRAM. If < 1GB, force fallback to gemma3:4b without attempting larger model.

---

## 9. Memory System (Simplified)

### Clear Roles

| Memory Type | Backend | Purpose | Scope |
|------------|---------|---------|--------|
| **Short-term** | In-memory dict | Session messages | Session only |
| **Long-term** | SQLite (simple) | Facts, preferences | Cross-session |
| **Working** | None | Current turn context | In InputPacket |

### What NOT to Implement

- Redis (adds complexity, not needed for single-user)
- ChromaDB embeddings (overkill for local assistant)
- Complex vector search (simple LIKE queries sufficient)

### Implementation

```python
# Simple SQLite schema
TABLE facts (
  id INTEGER PRIMARY KEY,
  key TEXT,
  value TEXT,
  created_at TIMESTAMP
)

TABLE conversation_history (
  id INTEGER PRIMARY KEY,
  session_id TEXT,
  role TEXT,
  content TEXT,
  created_at TIMESTAMP
)
```

---

## 10. Tool Chain Control

Prevent infinite tool loops.

### Chain Detection

```python
def detect_tool_loop(tool_calls):
  # Track last N tool calls
  last_n = tool_calls[-5:]
  
  # Check for repetition
  if len(set(last_n)) == 1 and len(last_n) == 5:
    # Same tool called 5 times
    RETURN blocked("tool_loop_detected")
  
  # Check for alternating pattern
  if is_alternating(last_n):
    RETURN blocked("alternating_tool_loop")
  
  RETURN allowed
```

### Max Chain Depth

| Depth | Behavior |
|-------|----------|
| 0 | No tools called yet |
| 1-2 | Normal execution |
| 3 | Warning issued |
| 4+ | BLOCKED |

---

## 11. Failure Modes

Each failure mode has explicit handling.

### Model Failure

```
DETECT: No response within model_timeout_s

RETRY: 
  1. Retry once with same model
  2. If still failing: swap to fallback (gemma3:4b)
  3. If fallback failing: RETURN error_response
  
LOG: model.error, model, error_type
```

### Tool Failure

```
DETECT: ToolResult.success == false

HANDLING:
  - Log: tool, error message
  - Add context: "Tool X failed: {error}"
  - Allow continuation (can retry with different tool)
  - DO NOT retry the same tool (infinite loop risk)

RETURN: partial response with tool error
```

### Parse Failure

```
DETECT: Invalid JSON from model when tool required

RETRY: max_retries times with retry prompt

IF exhausted:
  - Mark as parse_failure
  - Fallback to answering without tool
  - Log: parse.failure, raw_output
```

### Timeout

```
DETECT: Elapsed > total_turn_timeout_s

HANDLING:
  - Complete current step if possible
  - Add "(partial)" to response
  - LOG: timeout at phase=X
  
RETURN: best_effort_response
```

### Invalid Decision

```
DETECT: DecisionOutput has invalid fields

HANDLING:
  - Force to defaults:
    - intent = "chat"
    - mode = "normal"
    - model = default
    - requires_tools = false
  - Log: decision.invalid, original
  
CONTINUE with safe defaults
```

---

## 12. Data Contracts

### InputPacket

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

```json
{
  "type": "answer|tool_call",
  "content": "string",
  "tool": "string",
  "args": {}
}
```

### ToolResult

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

## 13. Logging Event Types

| Event | Fields |
|-------|--------|
| `runtime.state` | from, to, timestamp |
| `runtime.iteration` | current, max |
| `runtime.tool_depth` | current, max |
| `turn.start` | session, input_len, turn |
| `decision` | intent, model, risk_level |
| `tool.start` | name, args |
| `tool.done` | name, success, duration_ms |
| `tool.blocked` | name, reason |
| `tool.loop_detected` | name, call_history |
| `parse.failure` | attempt, raw_length |
| `model.swap` | from, to, reason |
| `model.error` | model, error_type |
| `retry` | attempt, reason |
| `timeout` | phase, elapsed |
| `turn.end` | quality, total_ms, state |

---

## 14. Execution Modes

| Mode | Description | Behavior |
|------|-------------|----------|
| **SAFE** | Confirm all | Every tool requires confirmation |
| **BALANCED** | Smart default | Low auto, med confirm, high blocked |
| **UNRESTRICTED** | Full access | No confirmation |

### Default: BALANCED

Only change if user explicitly requests otherwise.

---

## 15. Tech Stack

| Component | Technology |
|-----------|------------|
| LLM Runtime | Ollama |
| Web | FastAPI + Uvicorn |
| Database | SQLite |
| Config | PyYAML + Pydantic |
| Logging | Loguru |
| Testing | pytest |

---

## 16. Quick Start

```bash
# Install
pip install -r requirements.txt

# Pull models (choose based on VRAM)
ollama pull gemma3:4b   # 3GB - always available
ollama pull qwen3:8b     # 5GB - primary model

# For code (optional)
ollama pull qwen2.5-coder:7b

# Configure
cp config/settings.example.yaml config/settings.yaml
cp .env.example .env

# Run
python app/main.py --interface cli --debug
```

---

*Version 1.0.0-production*