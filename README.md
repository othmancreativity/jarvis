<div align="center">

# 🤖 JARVIS
### Local AI Assistant — Arabic + English — Free, Unlimited, Private

![Version](https://img.shields.io/badge/version-1.0.0--alpha-blue)
![Python](https://img.shields.io/badge/python-3.10+-green)
![License](https://img.shields.io/badge/license-MIT-orange)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightblue)
![Arabic](https://img.shields.io/badge/language-Arabic%20%2B%20English-red)

**A fully local, private AI assistant that understands commands, controls your computer, calls APIs, and reasons in multiple steps — no cloud, no limits, no cost.**

</div>

---

## 1. Overview

### What is Jarvis?

Jarvis is a **local AI assistant** that runs entirely on your machine. It accepts input from voice, text, or file — in Arabic or English — and either answers conversationally or executes real actions (open apps, send emails, search the web, generate images, manage files).

### What makes it different?

| Feature | Jarvis | Cloud Assistants |
|---------|--------|-----------------|
| Privacy | 100% local | Your data sent to servers |
| Cost | Free, unlimited | Per-token billing |
| Computer control | Full OS access | Sandboxed/none |
| Arabic | Native | Approximate |
| Offline | Yes | No |
| Customizable | Full source | No |

### How it works (one sentence)

User input → classified by intent → routed to the right model in the right mode → model either answers directly or calls a tool → result returned and saved to memory.

---

## 2. Minimal Working System

### Stage 1: Hello World

```
User types: "what is AI?"

→ Context assembles: {message: "what is AI?"}
→ Decision: {intent: "chat", model: "gemma3:4b", mode: "fast"}
→ Model called: gemma3:4b generates answer
→ Answer streamed to terminal
```

### Stage 2: Tool Execution

```
User types: "open chrome"

→ Context assembles: {message: "open chrome"}
→ Decision: {intent: "tool_use", tool: "open_app", args: {name: "chrome"}}
→ Safety check: SAFE
→ Tool executed: subprocess opens Chrome
→ Response: "✓ Opened Chrome (pid: 4521)"
```

### Stage 3: Multi-Step

```
User types: "research AI news and save a summary to my desktop"

→ Intent: "research" → triggers Planner agent
→ Plan: [web_search("AI news"), summarize(results), write_file("Desktop/summary.txt", content)]
→ Steps execute sequentially; output of step N → input of step N+1
→ Response: "Done. Summary saved to Desktop/summary.txt"
```

---

## 3. System Architecture

### Layer Map (no overlap — each layer has exactly one job)

```
┌─────────────────────────────────────────────────┐
│                  INTERFACES                     │
│  CLI │ Web UI │ Voice │ Telegram │ GUI           │
│  (receive input, display output — nothing else) │
└──────────────────────┬──────────────────────────┘
                       │ raw user input
┌──────────────────────▼──────────────────────────┐
│                   CONTEXT                       │
│  Assemble this turn's input bundle              │
│  (message + attachments + memory snippets)      │
└──────────────────────┬──────────────────────────┘
                       │ ContextBundle
┌──────────────────────▼──────────────────────────┐
│                   RUNTIME                       │
│  Drive the Observe→Decide→Think→Act→Evaluate    │
│  loop. Manage iterations, timeouts, escalation  │
└──────┬───────────────┬───────────────┬──────────┘
       │               │               │
┌──────▼──────┐ ┌──────▼──────┐ ┌─────▼──────────┐
│  DECISION   │ │   AGENTS    │ │    TOOLS        │
│  (routing   │ │  (thinking  │ │  registry +     │
│   only)     │ │   planning) │ │  executor)      │
└──────┬──────┘ └──────┬──────┘ └─────┬──────────┘
       │               │               │
       └───────────────┼───────────────┘
                       │
┌──────────────────────▼──────────────────────────┐
│                   MODELS                        │
│  Thin wrappers: send input, get output          │
│  (LLM / Vision / Speech / Diffusion)           │
└──────────────────────┬──────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────┐
│                   SKILLS                        │
│  Tool implementations (one file = one tool)     │
│  (files, system, browser, API, screen, coder)  │
└──────────────────────┬──────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────┐
│                   MEMORY                        │
│  Short-term (Redis) + Long-term (ChromaDB)      │
│  + Structured (SQLite) + User Profile (JSON)    │
└─────────────────────────────────────────────────┘
```

### Layer Definitions (strict — no overlap)

#### INTERFACES
**Job:** Receive raw input from user. Display output to user. Nothing else.
- Does NOT: classify, route, store, or process data
- Passes to: Context assembler

#### CONTEXT
**Job:** Bundle everything needed for this turn into one object.
```python
class ContextBundle:
    user_message: str
    session_id: str
    attachments: list[Attachment]    # images, files, audio
    tool_results: list[ToolResult]   # from previous Act step
    memory_snippets: list[str]       # retrieved from Memory
    user_profile: UserProfile
    turn_number: int
```
- Does NOT: store anything, make decisions
- Valid for: current turn only; discarded after response

#### RUNTIME
**Job:** Drive the execution loop. Manage iterations, timeouts, retries, model swaps.
- Does NOT: implement intelligence; just calls the right things in the right order
- Owns: the Observe→Decide→Think→Act→Evaluate cycle

#### DECISION
**Job:** Classify the current turn and select resources. Pure routing, no thinking.
```python
class DecisionOutput:
    intent: str        # chat|code|tool_use|search|vision|research|voice
    complexity: str    # low|medium|high
    mode: str          # fast|normal|deep|planning|research
    model: str         # exact Ollama tag
    requires_tools: bool
    requires_planning: bool
    tool_name: str | None
    tool_args: dict
    confidence: float  # 0-1, how certain the classifier is
```
- Does NOT: think, plan, or call any model for reasoning
- Uses: gemma3:4b (fast classifier with JSON system prompt)

#### AGENTS
**Job:** Multi-step reasoning and task decomposition.
- Does NOT: route requests (Decision does that), execute tools directly
- Types: `Thinker` (CoT reasoning), `Planner` (step decomposition), `Researcher` (multi-source)

#### TOOLS (concept layer)
**Job:** Manage the tool ecosystem. Registry, validation, execution bridge.
- `registry.py` — discover and register all skills
- `validator.py` — validate args against JSON Schema
- `executor.py` — run tool, catch errors, return ToolResult
- `safety.py` — classify: safe / risky / critical

#### SKILLS (implementation layer)
**Job:** The actual code that does things. One file = one tool.
- Does NOT: make decisions, manage routing, store memory
- Each skill is a `BaseTool` subclass with `execute(**kwargs) → ToolResult`

#### MODELS
**Job:** Thin wrappers around AI models. Send input, get output.
- Does NOT: make decisions, read memory, know about tools
- Types: LLM (Ollama), Vision (LLaVA), Speech (Whisper+Piper), Diffusion (SD 1.5)

#### MEMORY
**Job:** Persist data across turns and sessions.
- Short-term: Redis (current session message history)
- Long-term: ChromaDB (semantic search over facts and outcomes)
- Structured: SQLite (conversations, tasks, feedback, run history)
- Profile: JSON file (user preferences)

#### IDENTITY
**Job:** Build the system prompt that goes into every LLM call.
- Combines: Jarvis identity + user profile + task context + mode fragment
- Ensures: every model sees the same coherent identity regardless of which model is active

---

## 4. Data Flow (complete, step-by-step)

```
User speaks/types/uploads
        │
        ▼
┌───────────────────┐
│  INTERFACE        │
│  Normalize input  │ ← text | audio file | image | file path
│  Generate session_id if new
└────────┬──────────┘
         │ raw_input: str | bytes | Path
         ▼
┌───────────────────┐
│  CONTEXT          │
│  1. Wrap message  │
│  2. Retrieve last │ ← short_term.get_history(session_id, n=10)
│     N messages    │
│  3. Semantic      │ ← long_term.recall(query=message, n=3)
│     recall        │
│  4. Attach user   │ ← user_profile.load()
│     profile       │
│  5. Process       │ ← if audio: STT.transcribe() → text
│     attachments   │   if image: store path (vision called later)
└────────┬──────────┘
         │ ContextBundle
         ▼
┌───────────────────┐
│  RUNTIME.observe()│
│  Read ContextBundle│
│  Check for tool   │
│  results from     │
│  previous Act step│
└────────┬──────────┘
         │ observation: Observation
         ▼
┌───────────────────┐
│  RUNTIME.decide() │
│  → calls Decision │
│  → returns        │
│    DecisionOutput │
└────────┬──────────┘
         │ DecisionOutput
         ▼
┌───────────────────┐
│  RUNTIME.think()  │
│  → build system   │ ← identity.builder.build_prompt(decision)
│    prompt         │
│  → swap model if  │ ← llm.engine.swap_to(decision.model)
│    needed         │
│  → call LLM       │ ← llm.engine.chat(messages, model)
│  → parse response │ ← extract text OR tool_call JSON
└────────┬──────────┘
         │ raw_response: str | ToolCallRequest
         ▼
┌───────────────────────────────────┐
│  RUNTIME.act()                    │
│  if raw_response is ToolCallRequest:
│    → safety.classify(tool, args)  │
│    → if CRITICAL: block           │
│    → if RISKY: confirm with user  │
│    → validator.check(args, schema)│
│    → executor.run(tool, args)     │ ← calls skill.execute(**args)
│    → append ToolResult to context │
│    → re-enter observe()           │ ← tool result becomes next observation
│  else:                            │
│    → response is the final answer │
└────────┬──────────────────────────┘
         │ final_response: str
         ▼
┌───────────────────┐
│  RUNTIME.evaluate()
│  → score quality  │ ← heuristic: empty? too short? tool failed?
│  → if low: retry  │ ← switch to deeper mode / stronger model
│  → if ok: finish  │
└────────┬──────────┘
         │ approved response
         ▼
┌───────────────────┐
│  MEMORY.save()    │
│  → short_term     │ ← save user message + response
│  → long_term      │ ← if quality > 0.8: remember(outcome)
│  → SQLite         │ ← log conversation row
└────────┬──────────┘
         │ saved
         ▼
┌───────────────────┐
│  INTERFACE        │
│  Stream response  │
│  to user          │
└───────────────────┘
```

---

## 5. Runtime System

### The Loop

```python
def run_turn(user_input: str, session_id: str) -> str:
    context = context.assemble(user_input, session_id)
    
    for iteration in range(MAX_ITERATIONS):          # default: 5
        observation = runtime.observe(context)
        decision    = runtime.decide(observation)
        raw_response = runtime.think(decision, context)
        
        if is_tool_call(raw_response):
            tool_result = runtime.act(raw_response)
            context.tool_results.append(tool_result)
            continue                                  # re-observe with tool result
        
        eval_result = runtime.evaluate(raw_response, decision)
        
        if eval_result.should_retry:
            decision.mode  = escalate_mode(decision.mode)
            decision.model = escalate_model(decision.model)
            continue
        
        break
    
    memory.save(session_id, user_input, raw_response)
    return raw_response
```

### observe()
```python
def observe(context: ContextBundle) -> Observation:
    # Merge: user message + memory snippets + tool results + user profile
    # Return structured input for Decision
    return Observation(
        text=context.user_message,
        history=context.memory_snippets,
        tool_results=context.tool_results,
        has_image=any(a.type == "image" for a in context.attachments),
        user_profile=context.user_profile,
    )
```

### decide()
```python
def decide(observation: Observation) -> DecisionOutput:
    # Fast path: obvious cases without LLM call
    if len(observation.text) < 20 and not observation.has_image:
        return DecisionOutput(intent="chat", model="gemma3:4b", mode="fast", ...)
    
    if observation.has_image:
        return DecisionOutput(intent="vision", model="llava:7b", ...)
    
    # General case: use gemma3:4b as fast classifier
    prompt = CLASSIFIER_SYSTEM_PROMPT + observation.text
    raw = llm.chat(prompt, model="gemma3:4b")
    return parse_decision_json(raw)
```

### think()
```python
def think(decision: DecisionOutput, context: ContextBundle) -> str:
    system_prompt = identity.builder.build(
        task=context.user_message,
        mode=decision.mode,
        tools=registry.to_ollama_format() if decision.requires_tools else [],
    )
    
    llm.engine.swap_to(decision.model)   # VRAM guard: unload prev if different
    
    messages = [
        {"role": "system", "content": system_prompt},
        *history_to_messages(context.memory_snippets),
        {"role": "user", "content": context.user_message},
    ]
    
    response = llm.engine.chat(messages, model=decision.model, stream=True)
    return response   # may contain tool_call JSON block
```

### act()
```python
def act(tool_call_str: str) -> ToolResult:
    call = parse_tool_call(tool_call_str)
    # call = {"tool": "open_app", "args": {"name": "chrome"}}
    
    safety_result = safety.classify(call.tool, call.args)
    if safety_result.level == CRITICAL:
        return ToolResult(success=False, error="Blocked by safety policy")
    if safety_result.level == RISKY:
        if not ask_user_confirmation(call.tool, call.args):
            return ToolResult(success=False, error="User declined")
    
    validation_error = validator.check(call.args, registry.get_schema(call.tool))
    if validation_error:
        return ToolResult(success=False, error=f"Invalid args: {validation_error}")
    
    return executor.run(call.tool, call.args)
```

### evaluate()
```python
def evaluate(response: str, decision: DecisionOutput) -> EvalResult:
    if not response or len(response) < 5:
        return EvalResult(quality=0.0, should_retry=True, reason="empty response")
    
    if decision.complexity == "high" and len(response) < 100:
        return EvalResult(quality=0.3, should_retry=True, reason="too short for complex task")
    
    if decision.requires_tools and "error" in response.lower():
        return EvalResult(quality=0.4, should_retry=True, reason="tool error in response")
    
    return EvalResult(quality=0.85, should_retry=False)
```

---

## 6. Decision System

### What it does (only this)

Given the assembled observation, output a routing decision. No reasoning. No generation. Pure classification.

### Classifier prompt

```python
CLASSIFIER_SYSTEM_PROMPT = """
You are a command classifier. Given a user message, return ONLY valid JSON:

{
  "intent": "chat|code|tool_use|search|vision|research|voice",
  "complexity": "low|medium|high",
  "mode": "fast|normal|deep|planning|research",
  "model": "gemma3:4b|qwen3:8b|qwen2.5-coder:7b|llava:7b",
  "requires_tools": true|false,
  "requires_planning": true|false,
  "tool_name": "tool_name_or_null",
  "tool_args": {}
}

Rules:
- short/simple → fast + gemma3:4b
- code/programming → code + qwen2.5-coder:7b
- image attached → vision + llava:7b
- multi-step goal → planning + qwen3:8b
- deep reasoning needed → deep + qwen3:8b
- everything else → normal + qwen3:8b

Arabic examples:
"افتح Chrome" → intent=tool_use, tool=open_app, args={name:"chrome"}
"ما هو الذكاء الاصطناعي؟" → intent=chat, mode=fast, model=gemma3:4b
"اكتب كود Python لفرز قائمة" → intent=code, model=qwen2.5-coder:7b
"""
```

### Model Selection Rules

```
message is short AND no tool signal     → gemma3:4b (fast, cheap)
intent == "code"                        → qwen2.5-coder:7b
image in attachments                    → llava:7b
complexity == "high" OR mode == "deep"  → qwen3:8b
anything else                           → qwen3:8b (default)
```

---

## 7. Thinking Modes

| Mode | Behavior | Model Preference | Use When |
|------|----------|-----------------|----------|
| `fast` | Short answer, no elaboration | gemma3:4b | Simple factual questions |
| `normal` | Balanced depth and length | qwen3:8b | General conversation |
| `deep` | Chain-of-thought, self-critique | qwen3:8b | Complex reasoning |
| `planning` | Decompose before execute | qwen3:8b | Multi-step goals |
| `research` | Multi-source, cite everything | qwen3:8b | Research tasks |

Each mode maps to a **prompt fragment** added to the system prompt:

```python
MODE_FRAGMENTS = {
    "fast":     "Answer concisely. One to three sentences maximum.",
    "normal":   "Provide a complete, well-structured answer.",
    "deep":     "Think step by step. Show your reasoning. Self-critique your answer.",
    "planning": "Decompose the goal into numbered steps before executing.",
    "research": "Use multiple sources. Cite each claim. Summarize at the end.",
}
```

Same model + different mode = different behavior. Mode changes the **system prompt**, not the model weights.

---

## 8. Model System

### Available Models

| Ollama Tag | Role | VRAM | Arabic | Speed | Use Case |
|-----------|------|------|--------|-------|----------|
| `qwen3:8b` | Main brain | 5.0 GB | ⭐⭐⭐⭐⭐ | Medium | Deep reasoning, Arabic, planning |
| `gemma3:4b` | Fast responder | 3.0 GB | ⭐⭐⭐⭐ | Fast | Quick answers, classification |
| `qwen2.5-coder:7b` | Code specialist | 4.7 GB | ⭐⭐⭐ | Fast | Code generation, debugging |
| `llava:7b` | Vision | 4.5 GB | ⭐⭐⭐ | Medium | Image understanding, OCR |

### VRAM Management (6 GB GPU)

**Rule:** One heavy model at a time. Swap explicitly before loading another.

```python
def swap_to(new_model: str):
    current = get_active_model()
    if current and current != new_model:
        ollama_unload(current)   # free VRAM
        wait_for_unload()
    ollama_load(new_model)
```

**Priority when VRAM is tight:**
1. Unload current model
2. Load needed model
3. After use, keep loaded (warm) for 5 minutes of inactivity
4. Then unload

### Model Limitations

- `llava:7b`: Cannot process audio. Cannot generate code reliably. Vision only.
- `gemma3:4b`: Weak on Arabic long-form. Poor on multi-step reasoning. Fast responses only.
- `qwen2.5-coder:7b`: Weak on Arabic. Poor on general conversation. Code tasks only.
- `qwen3:8b`: Slower than others. Cannot process images directly. Best general + Arabic.

---

## 9. Tool System

### Tool JSON Contract

Every tool call from the LLM must follow this format:

```json
{
  "type": "tool_call",
  "tool": "open_app",
  "args": {
    "name": "chrome"
  }
}
```

Every tool result returned to the LLM:

```json
{
  "type": "tool_result",
  "tool": "open_app",
  "success": true,
  "data": {
    "pid": 4521,
    "name": "chrome"
  },
  "error": null,
  "duration_ms": 312
}
```

### Tool Schema (JSON Schema)

Each tool has a JSON Schema file at `config/schemas/{category}/{tool_name}.schema.json`:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "open_app",
  "description": "Open an application by name",
  "type": "object",
  "properties": {
    "name": {
      "type": "string",
      "description": "Application name or executable name (e.g. 'chrome', 'notepad')"
    }
  },
  "required": ["name"],
  "additionalProperties": false
}
```

### BaseTool Contract

```python
class BaseTool(ABC):
    name: str                      # snake_case, globally unique
    description: str               # ≤ 1 sentence, for LLM tool list
    category: str                  # system|files|browser|api|screen|coder|search|social|notify
    requires_confirmation: bool    # True = pause and ask user before executing
    platform: list[str]            # ["windows","linux","macos"] or ["windows"] only

    @abstractmethod
    def execute(self, **kwargs) -> ToolResult: ...

    def is_available(self) -> bool:
        """Check: binary exists? API key set? Platform matches?"""
        return True

    @classmethod
    def get_schema(cls) -> dict:
        """Load JSON Schema from config/schemas/"""
        ...
```

### Tool Registry

```python
# Auto-discovery: scans src/skills/ for BaseTool subclasses
registry = ToolRegistry()
registry.discover()

registry.get("open_app")          # → AppLauncherTool instance
registry.all_names()              # → ["open_app", "read_file", "web_search", ...]
registry.to_ollama_format()       # → Ollama-compatible tool list for LLM calls
registry.enabled_for_platform()  # → only tools available on current OS
```

### Tool Execution Pipeline

```
LLM output → parse tool call JSON
          → find tool in registry
          → safety.classify(tool, args) → SAFE|RISKY|CRITICAL
          → if RISKY: confirm with user
          → if CRITICAL: block (return error)
          → validator.check(args, schema) → valid|ValidationError
          → if invalid: return error (no execution)
          → executor.run(tool, args) → ToolResult
          → append to context.tool_results
          → re-enter loop (tool result becomes next observation)
```

---

## 10. Skills System

Each skill is a standalone tool. One file = one tool = one responsibility.

### System Skills (`src/skills/system/`)

#### `apps.py` — Application Launcher
- `open_app(name)` — Search PATH → Program Files → Start Menu → launch
- `close_app(name)` — `taskkill /IM {name}.exe` (Windows) / `pkill {name}` (Linux/Mac)
- `list_running()` — psutil process list: name, PID, CPU%, RAM%
- `bring_to_front(name)` — SetForegroundWindow (Windows) / wmctrl (Linux)
- Platform: Windows (full), Linux (partial), macOS (partial)

#### `sysinfo.py` — System Information
- `get_info()` — CPU%, RAM used/total, disk space, GPU VRAM (pynvml)
- `get_network()` — adapter list, IP addresses, internet connectivity
- `list_startup()` — Windows: registry Run keys; Linux: systemd services
- Platform: all (some features Windows-only)

#### `clipboard.py` — Clipboard Manager
- `read()` — read text or detect image → save to temp → return path
- `write(text)` — write text to clipboard
- `monitor(callback)` — background thread watching for changes
- Platform: all (pyperclip for text; win32clipboard/xclip/pbpaste for images)

#### `hotkeys.py` — Global Hotkeys
- `register(key, callback)` — system-wide hotkey binding
- `unregister(key)` — remove binding
- `list_active()` — current active bindings
- Platform: Windows (keyboard lib), Linux (pynput), macOS (pynput)

### File Skills (`src/skills/files/`)

#### `file_ops.py` — File Operations
- `read(path)` → file content as string
- `write(path, content)` → saves file (confirm if overwriting)
- `list(path)` → directory listing: name, size, type, modified
- `search(root, query)` → glob by name + grep by content
- `move(src, dst)` → move file/directory
- `copy(src, dst)` → copy file/directory
- `delete(path)` → send to recycle bin via send2trash (NEVER permanent delete)
- Safety: `delete` always requires_confirmation; paths checked against allowlist

### Browser Skills (`src/skills/browser/`)

#### `browser.py` — Playwright Browser Core
- `navigate(url)` → open URL, wait for load
- `click(selector)` → click by CSS, XPath, text, or ARIA label
- `fill(selector, text)` → fill input field
- `get_text(selector)` → extract text from element
- `get_page_content()` → full page as clean Markdown (via readability)
- `screenshot()` → save viewport PNG to data/screenshots/browser/
- `scroll(direction, amount)` → scroll page

#### `session.py` — Session Persistence
- `save(domain)` → save cookies+localStorage to `data/sessions/{domain}.json`
- `load(domain)` → load saved session (stay logged in)
- `is_expired(domain)` → detect login redirect → return True if expired

#### `transfer.py` — Downloads + Uploads
- `download(url)` → intercept download, save to `data/downloads/`
- `upload(selector, path)` → `page.set_input_files(selector, path)`

#### `auth_handler.py` — Auth Wall Detection
- `check(page)` → detect login/captcha page
- `pause_and_wait()` → notify user + wait for Enter → resume + save session

### API Skills (`src/skills/api/`)

#### `google_auth.py` — Unified Google OAuth
- Single token for: Calendar + Gmail + Drive + Contacts + YouTube
- `get_credentials()` → load from `data/google_token.json` or run consent flow
- `refresh()` → auto-refresh expired access token
- File: `data/google_token.json` (gitignored)

#### `calendar.py` — Google Calendar
- `list(days=7)` → upcoming events
- `create(title, datetime, timezone, attendees, description)` → new event
- `update(event_id, fields)` → modify event
- `delete(event_id)` → remove event (requires_confirmation)
- `search(query, date_range)` → find events

#### `gmail.py` — Gmail
- `list(n=10)` → latest N emails: sender, subject, preview, thread_id
- `search(query)` → Gmail query syntax (from:, subject:, after:, etc.)
- `send(to, subject, body, attachments=[])` → send email (requires_confirmation)
- `reply(thread_id, body)` → reply to thread (requires_confirmation)
- `mark(message_id, action)` → read|unread|starred|important
- `move(message_id, label)` → move to label

#### `drive.py` — Google Drive
- `list(folder=None)` → files in root or folder
- `search(query)` → find by name or content
- `upload(local_path, folder=None)` → upload file
- `download(file_id, dest=None)` → download to `data/downloads/`
- `share(file_id, email, role)` → viewer|editor permission
- `create_folder(name, parent=None)` → new folder

#### `contacts.py` — Google Contacts
- `list(n=100)` → all contacts: name, email, phone
- `search(query)` → search by name/email/phone
- `get(contact_id)` → full contact details
- `create(name, email, phone)` → new contact
- `resolve_name(name)` → name → email (for "send email to Ahmed")

#### `youtube.py` — YouTube
- `search(query, max_results=5)` → videos: title, URL, duration, views
- `get_info(video_id)` → detailed video info
- `open(video_id_or_url)` → open in default browser

### Screen Skills (`src/skills/screen/`)

#### `capture.py` — Screenshot + OCR
- `screenshot(region=None)` → PNG to `data/screenshots/`; full screen or region
- `ocr(image_path)` → pytesseract text extraction (no LLM needed)
- `describe(image_path)` → LLaVA semantic description (requires vision model)
- `read_screen()` → screenshot + OCR combined (fast path, no LLM)

### Coder Skills (`src/skills/coder/`)

#### `executor.py` — Code Execution
- `run_python(code, timeout=30)` → subprocess Python; capture stdout/stderr
- `run_shell(command, timeout=30)` → shell command; blocklist enforced
- Blocklist: `rm -rf`, `format`, `del /s /q`, `:(){:|:&};:`, `shutdown`
- requires_confirmation: True for both

### Search Skills (`src/skills/search/`)

#### `web_search.py` — Web Search
- `search(query, max_results=5)` → DuckDuckGo HTML (no API key)
- `fetch_content(url)` → full page content as Markdown (trafilatura)
- `cached_search(query)` → TTL-based cache (5 min) for identical queries

### Social Skills (`src/skills/social/`)

#### `whatsapp.py` — WhatsApp Web
- `send(contact, message)` → find contact → type message → send
- `read(contact, n=10)` → last N messages from conversation
- `login()` → QR code screenshot → display → wait for scan → save session

### Notification Skills (`src/skills/notify/`)

#### `toasts.py` — System Notifications
- `send(title, message, type)` → Windows Toast (winotify) / notify-send (Linux) / osascript (macOS)
- Types: info | success | warning | error

### Media Skills (`src/skills/media/`)

#### `player.py` — Media Control
- `play_pause()` → system media key
- `next_track()` / `prev_track()` → system media keys
- `set_volume(level)` → 0-100%
- `get_current_track()` → currently playing (Windows: win32api; Linux: dbus)

### Network Skills (`src/skills/network/`)

#### `network.py` — Network Operations
- `check_connection()` → ping test → True/False
- `get_ip()` → local + public IP
- `list_adapters()` → network interface list
- `speed_test()` → download/upload speed via fast.com API

### Document Skills (`src/skills/pdf/` + `src/skills/office/`)

#### `pdf_reader.py` — PDF Processing
- `read_text(path)` → full text extraction (pdfplumber)
- `extract_tables(path)` → structured table data
- `summarize(path)` → chunk → LLM summarize each → combine

#### `office_reader.py` — Office Documents
- `read_docx(path)` → Word text + headings + tables
- `read_xlsx(path)` → Excel sheets, rows, values (openpyxl)
- `read_pptx(path)` → slide titles + text (python-pptx)
- `write_docx(path, content)` → create Word document
- `write_xlsx(path, data)` → create Excel spreadsheet

---

## 11. Prompt System

### Prompt Assembly Order (deterministic)

Every LLM call receives a system prompt built in this exact order:

```
[1] Jarvis Identity        ← who Jarvis is, what it can do
[2] Safety Rules           ← what it must never do
[3] User Profile           ← user preferences, language, style
[4] Mode Fragment          ← how to respond (fast/normal/deep/planning/research)
[5] Task Context           ← what the user is trying to do this turn
[6] Tool List              ← available tools (only if requires_tools=True)
[7] Handoff Note           ← if model was just switched (for continuity)
```

### Example Built Prompt

```
You are Jarvis, a personal AI assistant system.
You are a component of Jarvis — not a standalone product.

Safety:
- Never expose credentials, API keys, or file paths in responses
- Confirm before destructive actions
- Admit uncertainty rather than fabricate

User: Ahmed | Language: Arabic | Style: concise | Level: intermediate

Mode: deep — Think step by step. Show reasoning. Self-critique before finalizing.

Task: The user wants to research AI news and summarize it

Available tools:
- web_search: Search the web using DuckDuckGo
- write_file: Write content to a file

[Previous model: gemma3:4b | Current model: qwen3:8b — maintain conversation context]
```

---

## 12. Identity System

### Jarvis Identity (`config/jarvis_identity.yaml`)

```yaml
name: "Jarvis"
role: "Personal AI assistant system"
version: "1.0.0"
capabilities:
  - "Natural Arabic and English conversation"
  - "Computer control (apps, files, browser)"
  - "Google APIs (Calendar, Gmail, Drive, Contacts)"
  - "Web search and research"
  - "Image understanding and generation"
  - "Voice interaction"
safety_rules:
  - "Never expose credentials, API keys, passwords, or raw file paths"
  - "Confirm before: delete, send email, send message, run code, kill process"
  - "Admit when uncertain — never fabricate information"
  - "Respect user privacy — all data stays local"
component_notice: |
  You are a component of Jarvis AI assistant.
  You are not the underlying model (qwen, gemma, llava).
  You are Jarvis. Behave consistently regardless of which model is active.
```

### User Profile (`data/user_profile.json`)

```json
{
  "name": "User",
  "language": "ar",
  "style": "balanced",
  "tone": "casual",
  "technical_level": "intermediate",
  "preferred_model": null,
  "preferred_mode": null,
  "timezone": "Africa/Cairo"
}
```

---

## 13. Memory System

### Short-Term Memory (Redis)
- **What:** Current session message history
- **Format:** List of `{role, content, timestamp}` dicts per session_id
- **TTL:** Session expires after 24h inactivity
- **Fallback:** In-memory dict if Redis unavailable (no crash)
- **Max:** 50 messages per session (trim oldest when exceeded)

### Long-Term Memory (ChromaDB)
- **What:** Semantic facts, user preferences, outcomes, "what worked"
- **Search:** Cosine similarity over sentence-transformers embeddings
- **Write:** `remember(text, metadata)` — called after successful interactions
- **Read:** `recall(query, n=5)` — top-N semantically similar snippets
- **Persistence:** `data/chroma/` directory (survives restarts)

### Structured Store (SQLite)
- **Tables:**
  - `conversations(id, session_id, role, content, timestamp)`
  - `feedback(id, session_id, model, mode, score, timestamp)`
  - `tasks(id, run_id, title, status, result, created_at, updated_at)`
  - `routing_weights(id, intent, model, weight, updated_at)`
- **File:** `data/jarvis.db`

### User Profile (JSON)
- **File:** `data/user_profile.json`
- **Updated by:** `/profile` command, implicit learning from feedback

---

## 14. Context System

### Scope: This turn only

The Context lives for exactly one turn. It is assembled at the start and discarded after the response is delivered.

```python
class ContextBundle:
    # Input
    user_message: str
    session_id: str
    attachments: list[Attachment]    # {type: image|file|audio, path: str}

    # Injected from Memory
    memory_snippets: list[str]       # ≤ 5 relevant past facts
    recent_history: list[Message]    # ≤ 10 recent messages

    # Accumulated during execution
    tool_results: list[ToolResult]   # grows as tools are called this turn

    # From Profile
    user_profile: UserProfile

    # Metadata
    turn_number: int
    started_at: float                # timestamp
```

Context is **NOT** stored. Memory is stored.

---

## 15. Capability System

### Model Capabilities

```yaml
# config/models.yaml — source of truth for all routing decisions

qwen3:8b:
  arabic_quality: 0.95      # 0-1
  reasoning: "high"         # low|medium|high
  code_bias: 0.50
  vision: false
  vram_gb: 5.0
  latency: "medium"         # fast|medium|slow

gemma3:4b:
  arabic_quality: 0.85
  reasoning: "low"
  code_bias: 0.35
  vision: false
  vram_gb: 3.0
  latency: "fast"

qwen2.5-coder:7b:
  arabic_quality: 0.75
  reasoning: "medium"
  code_bias: 0.95
  vision: false
  vram_gb: 4.7
  latency: "fast"

llava:7b:
  arabic_quality: 0.70
  reasoning: "medium"
  code_bias: 0.20
  vision: true
  vram_gb: 4.5
  latency: "medium"
```

### Tool Capabilities

```yaml
# config/skills.yaml

tools:
  - id: open_app
    enabled: true
    category: system
    platform: [windows, linux, macos]
    requires_confirmation: false
    schema: system/open_app.schema.json

  - id: delete_file
    enabled: true
    category: files
    platform: [windows, linux, macos]
    requires_confirmation: true
    schema: files/delete_file.schema.json

  - id: send_email
    enabled: false           # disabled until Google OAuth configured
    category: api
    platform: [windows, linux, macos]
    requires_confirmation: true
    schema: api/send_email.schema.json
```

---

## 16. Error Handling System

### Error Classes

| Class | Cause | Action |
|-------|-------|--------|
| `model_error` | Ollama connection failed / OOM | Retry with smaller model |
| `tool_error` | Skill raised exception | Return error to LLM; LLM explains to user |
| `validation_error` | Args don't match schema | Return error; LLM can retry with fixed args |
| `safety_blocked` | CRITICAL safety classification | Block; tell user it's not allowed |
| `user_declined` | User rejected RISKY confirmation | Return graceful message |
| `timeout` | Step exceeded time limit | Return partial result or timeout message |
| `vram_oom` | GPU OOM during model load | Unload all; load smallest model; retry |

### Retry Logic

```python
ESCALATION_CHAIN = [
    ("fast",     "gemma3:4b"),
    ("normal",   "qwen3:8b"),
    ("deep",     "qwen3:8b"),
]

def escalate(current_mode, current_model):
    current_idx = find_escalation_level(current_mode)
    if current_idx < len(ESCALATION_CHAIN) - 1:
        next_mode, next_model = ESCALATION_CHAIN[current_idx + 1]
        return next_mode, next_model
    return current_mode, current_model  # already at max
```

### Fallback Response

When all retries exhausted:
```python
FALLBACK = "I encountered an issue completing that request. Could you try rephrasing, or break it into smaller steps?"
```

---

## 17. Logging System

### Log Levels

| Level | When | Content |
|-------|------|---------|
| DEBUG | Development only | Full prompts, raw responses, tool args |
| INFO | Always | Turn start/end, decisions, tool calls, latency |
| WARNING | Recoverable errors | Retry fired, tool failed, model swapped |
| ERROR | Unrecoverable | Exception with full stack trace |

### Structured Log Format

```
2025-01-15 14:23:01 | INFO  | turn.start session=abc123 input_len=45
2025-01-15 14:23:01 | INFO  | decision intent=tool_use model=gemma3:4b mode=fast tool=open_app
2025-01-15 14:23:02 | INFO  | tool.start name=open_app args_hash=a3f4b2
2025-01-15 14:23:02 | INFO  | tool.done name=open_app success=True duration_ms=312
2025-01-15 14:23:02 | INFO  | turn.done session=abc123 quality=0.90 total_ms=1450
```

### Log Files
- `logs/jarvis.log` — all levels INFO+; daily rotation; 7-day retention
- `logs/debug.log` — DEBUG level; only when `JARVIS_DEBUG=1`; 1-day retention

---

## 18. Cross-Platform Support

### Platform Detection

```python
import platform

PLATFORM = platform.system().lower()  # "windows" | "linux" | "darwin"

def is_windows(): return PLATFORM == "windows"
def is_linux():   return PLATFORM == "linux"
def is_macos():   return PLATFORM == "darwin"
```

### Platform-Specific Implementations

| Feature | Windows | Linux | macOS |
|---------|---------|-------|-------|
| App launch | `ShellExecute` / `subprocess` | `subprocess` | `open -a` |
| App close | `taskkill /IM name.exe /F` | `pkill name` | `osascript quit` |
| Volume | `pycaw` | `amixer` / `pactl` | `osascript set volume` |
| Notifications | `winotify` | `notify-send` | `osascript display notification` |
| Clipboard (text) | `pyperclip` | `pyperclip` | `pyperclip` |
| Clipboard (image) | `win32clipboard` | `xclip` | `pbpaste` |
| Hotkeys | `keyboard` lib | `pynput` | `pynput` |
| Screen capture | `mss` | `mss` | `mss` |
| OCR | `pytesseract` | `pytesseract` | `pytesseract` |
| Tray icon | `pystray` | `pystray` | `pystray` |
| Auto-start | Registry Run key | `~/.config/autostart/` | `LaunchAgents` plist |
| Paths | `C:\Users\...` | `/home/...` | `/Users/...` |

### Path Handling

```python
from pathlib import Path

# Always use pathlib — works on all platforms
DATA_DIR = Path("data")
LOGS_DIR = Path("logs")
SESSIONS_DIR = DATA_DIR / "sessions"
DOWNLOADS_DIR = DATA_DIR / "downloads"

# Never hardcode separators
# WRONG: path = "data\\sessions\\google.com.json"
# RIGHT: path = DATA_DIR / "sessions" / "google.com.json"
```

---

## 19. Runtime Lifecycle

```
python app/main.py --interface cli
        │
        ▼
1. PARSE ARGS
   --interface: cli|web|voice|telegram|gui|all
        │
        ▼
2. LOAD CONFIG
   src/core/config.py → load config/settings.yaml + .env
   Validate: required fields, valid model names
        │
        ▼
3. SETUP LOGGING
   src/core/logging_setup.py → loguru to logs/jarvis.log
        │
        ▼
4. INIT MEMORY
   short_term.connect() → Redis or in-memory fallback
   long_term.connect()  → ChromaDB at data/chroma/
   database.init()      → SQLite at data/jarvis.db (create tables if missing)
        │
        ▼
5. INIT TOOL REGISTRY
   registry.discover()  → scan src/skills/ → register all BaseTool subclasses
   registry.health_check() → test is_available() for each tool
        │
        ▼
6. VALIDATE MODELS
   for model in [default, fast, code, vision]:
       check ollama list | verify model is pulled
   warn (not crash) if model missing
        │
        ▼
7. LOAD USER PROFILE
   user_profile.load() → data/user_profile.json or create default
        │
        ▼
8. START INTERFACE
   if cli: run_cli(cfg)
   if web: uvicorn FastAPI app on port cfg.interfaces.web_port
   if voice: start wake_word listener thread + run_voice_pipeline()
   if telegram: bot.start_polling()
   if gui: PyQt6 app.exec()
        │
        ▼
9. WAIT FOR INPUT
   (each interface has its own input loop)
        │
        ▼
10. PROCESS TURN
    runtime.run_turn(user_input, session_id)
        │
        ▼
11. RETURN RESPONSE
    stream tokens to interface as they arrive
        │
        ▼
12. SAVE TO MEMORY
    auto-save after every turn
        │
        ▼
    (back to step 9)
        │
        ▼
Ctrl+C / shutdown signal
        │
        ▼
13. GRACEFUL SHUTDOWN
    close browser instances
    flush memory writes
    release audio devices
    log "Jarvis stopped"
```

---

## 20. Example End-to-End Execution

**User says:** "ابحث عن آخر أخبار الذكاء الاصطناعي وأرسل ملخصاً لـ ahmed@example.com"
(Search for the latest AI news and send a summary to ahmed@example.com)

```
1. INTERFACE (voice or CLI)
   Receives text: "ابحث عن آخر أخبار الذكاء الاصطناعي وأرسل ملخصاً لـ ahmed@example.com"
   session_id: "session_abc123"

2. CONTEXT
   ContextBundle {
     user_message: "ابحث عن آخر أخبار الذكاء الاصطناعي...",
     memory_snippets: ["User prefers concise Arabic summaries"],
     recent_history: [...last 5 messages...],
     user_profile: {language: "ar", style: "concise"},
   }

3. DECISION
   Classifier (gemma3:4b, fast):
   {
     "intent": "research",
     "complexity": "high",
     "mode": "planning",
     "model": "qwen3:8b",
     "requires_tools": true,
     "requires_planning": true,
     "tool_name": null
   }

4. THINK (iteration 1) — qwen3:8b, planning mode
   System prompt includes: tool list [web_search, send_email, contacts.resolve_name]
   LLM output:
   {
     "type": "tool_call",
     "tool": "web_search",
     "args": {"query": "latest AI news 2025", "max_results": 5}
   }

5. ACT (iteration 1)
   safety: SAFE
   validation: PASS
   web_search executes → returns 5 results with titles + snippets + URLs
   ToolResult appended to context

6. OBSERVE (iteration 2)
   Context now includes: tool_results = [web_search results]

7. THINK (iteration 2)
   LLM summarizes 5 results into Arabic paragraph:
   "في آخر أخبار الذكاء الاصطناعي: شركة X أعلنت عن نموذج جديد..."
   Then emits:
   {
     "type": "tool_call",
     "tool": "send_email",
     "args": {
       "to": "ahmed@example.com",
       "subject": "ملخص آخر أخبار الذكاء الاصطناعي",
       "body": "في آخر أخبار الذكاء الاصطناعي: ..."
     }
   }

8. ACT (iteration 2)
   safety: RISKY (send_email requires_confirmation=True)
   ⚠️ Confirm: Send email to ahmed@example.com? [y/N]: y
   validation: PASS
   Gmail API: email sent → message_id returned
   ToolResult: {success: true, data: {message_id: "msg_xyz"}}

9. THINK (iteration 3)
   LLM sees tool_results = [web_search OK, send_email OK]
   Generates final response:
   "تم البحث عن آخر أخبار الذكاء الاصطناعي وإرسال الملخص إلى ahmed@example.com ✓"

10. EVALUATE
    quality: 0.90 (success, correct language, complete task)
    should_retry: False

11. MEMORY SAVE
    short_term.save("session_abc123", "user", original_message)
    short_term.save("session_abc123", "assistant", final_response)
    long_term.remember("User asked to search and email AI news summary — success", {type: "outcome"})
    SQLite: conversation rows inserted

12. INTERFACE
    Streams final response to terminal/speaker
```

---

## Quick Start

```bash
# 1. Clone and setup
git clone <repo>
cd jarvis
python -m venv venv
source venv/bin/activate        # Linux/macOS
.\venv\Scripts\Activate.ps1    # Windows

pip install -r requirements.txt
playwright install chromium

# 2. Pull models
ollama pull qwen3:8b
ollama pull qwen2.5-coder:7b
ollama pull gemma3:4b
ollama pull llava:7b

# 3. Configure
cp config/settings.example.yaml config/settings.yaml
cp .env.example .env
# Edit .env: add TELEGRAM_BOT_TOKEN, GOOGLE_CLIENT_ID, etc.

# 4. Run
python app/main.py --interface cli       # terminal chat
python app/main.py --interface web       # browser at http://localhost:8080
python app/main.py --interface voice     # voice pipeline
python app/main.py --interface all       # everything simultaneously
```

---

## Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| LLM Runtime | Ollama | latest |
| Web Framework | FastAPI + Uvicorn | 0.104+ |
| WebSocket | FastAPI WebSocket | — |
| Vector DB | ChromaDB | 0.4+ |
| Cache | Redis | 5.0+ |
| SQL | SQLite | built-in |
| STT | OpenAI Whisper | medium model |
| TTS | Piper TTS | Arabic + EN |
| Wake Word | openWakeWord | — |
| Image Gen | Diffusers (SD 1.5) | 0.24+ |
| Browser | Playwright (Chromium) | 1.40+ |
| Terminal UI | Rich | 13+ |
| Desktop GUI | PyQt6 | 6.6+ |
| Telegram | python-telegram-bot | 20+ |
| Google APIs | google-api-python-client | 2.100+ |
| Config | PyYAML + Pydantic | — |
| Logging | Loguru | 0.7+ |
| PDF | pdfplumber | — |
| Office | python-docx, openpyxl, python-pptx | — |
| OCR | pytesseract (+ Tesseract binary) | — |
| Screen | mss + Pillow | — |
| Windows | pywin32, pycaw, pystray, winotify | — |
| Cross-platform | pyperclip, pynput, keyboard | — |
| Security | cryptography (Fernet) | — |
| Testing | pytest + pytest-asyncio + pytest-cov | — |

---

## License

MIT — free to use, modify, distribute.
