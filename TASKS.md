# 🗂️ JARVIS — Task Board

> **Rule:** Every task has INPUT, OUTPUT, FILES, and SUCCESS CRITERIA.  
> Tasks are ordered by dependency — each phase unlocks the next.  
> Do not start Phase N until Phase N-1 is complete.

---

## 📊 Progress

| Phase | Description | Status |
|---|---|---|
| 1 | Foundation | ⏳ In Progress |
| 2 | Minimal Working System | ⬜ Pending |
| 3 | Runtime Loop | ⬜ Pending |
| 4 | Decision Layer | ⬜ Pending |
| 5 | Context Buffer | ⬜ Pending |
| 6 | Memory | ⬜ Pending |
| 7 | Tools Infrastructure | ⬜ Pending |
| 8 | Agents | ⬜ Pending |
| 9 | Skills (System + Browser + APIs) | ⬜ Pending |
| 10 | Safety | ⬜ Pending |
| 11 | Logging + Observability | ⬜ Pending |
| 12 | CLI Interface | ⬜ Pending |
| 13 | Web UI | ⬜ Pending |
| 14 | Voice Pipeline | ⬜ Pending |
| 15 | Telegram + GUI | ⬜ Pending |
| 16 | Optimization + QA | ⬜ Pending |

---

## 🏗️ Phase 1 — Foundation

> **Goal:** A bootable project skeleton. Config loads. Logging writes. Every directory exists.  
> **Done when:** `python app/main.py --interface cli` runs without crashing (even if it just prints "Jarvis ready").

---

### TASK 1.1 — Create directory structure

**INPUT:** Nothing (empty repo)  
**OUTPUT:** All directories exist with `__init__.py` files  
**FILES TO CREATE:**
```
src/core/runtime/__init__.py
src/core/orchestrator/__init__.py
src/core/agents/__init__.py
src/core/tools/__init__.py
src/core/memory/__init__.py
src/core/context/__init__.py
src/core/identity/__init__.py
src/models/base/__init__.py
src/models/llm/__init__.py
src/models/vision/__init__.py
src/models/speech/__init__.py
src/models/diffusion/__init__.py
src/skills/__init__.py
src/skills/system/__init__.py
src/skills/browser/__init__.py
src/skills/search/__init__.py
src/skills/coder/__init__.py
src/skills/screen/__init__.py
src/skills/api/__init__.py
src/skills/office/__init__.py
src/skills/social/__init__.py
src/interfaces/cli/__init__.py
src/interfaces/web/__init__.py
src/interfaces/telegram/__init__.py
src/interfaces/gui/__init__.py
src/interfaces/voice/__init__.py
data/.gitkeep
logs/.gitkeep
```

**SUCCESS CRITERIA:**
- [ ] All directories exist
- [ ] All `__init__.py` files are present
- [ ] `import src.core.runtime` works from repo root with `PYTHONPATH=src`

---

### TASK 1.2 — Create `config/settings.yaml`

**INPUT:** Nothing  
**OUTPUT:** A valid settings file that pydantic-settings can load  
**FILES TO CREATE:** `config/settings.yaml`

```yaml
jarvis:
  name: "Jarvis"
  language: ["ar", "en"]
  wake_word: "hey_jarvis"

runtime:
  max_iterations: 5
  max_escalation_depth: 2
  tool_timeout_s: 30
  step_timeout_s: 60

models:
  default: "qwen3:8b"
  fast: "gemma3:4b"
  code: "qwen2.5-coder:7b"
  vision: "llava:7b"

hardware:
  gpu_vram_limit_gb: 5.5
  max_concurrent_models: 1
  model_swap_timeout_s: 30

interfaces:
  web:
    host: "127.0.0.1"
    port: 8080
  telegram:
    polling_timeout: 30

paths:
  data: "data/"
  logs: "logs/"
  sessions: "data/sessions/"
  downloads: "data/downloads/"
  screenshots: "data/screenshots/"
  chroma_db: "data/chroma/"
  sqlite_db: "data/jarvis.db"

hotkeys:
  open_cli: "ctrl+alt+j"
  start_voice: "ctrl+alt+s"
```

**SUCCESS CRITERIA:**
- [ ] File is valid YAML
- [ ] All keys documented in README.md match file content

---

### TASK 1.3 — Create `config/models.yaml`

**INPUT:** Nothing  
**OUTPUT:** Capability profiles for all 4 LLM models  
**FILES TO CREATE:** `config/models.yaml`

```yaml
routing_weights:
  reasoning_weight: 0.35
  arabic_weight: 0.20
  latency_weight: 0.25
  cost_weight: 0.20

models:
  qwen3:8b:
    ollama_tag: "qwen3:8b"
    reasoning_tier: high
    arabic_quality: 0.95
    code_bias: 0.4
    latency_tier: medium
    vram_estimate_gb: 5.0
    vision_required: false
    max_tokens: 8192
    temperature: 0.7
    top_p: 0.9

  gemma3:4b:
    ollama_tag: "gemma3:4b"
    reasoning_tier: low
    arabic_quality: 0.70
    code_bias: 0.2
    latency_tier: fast
    vram_estimate_gb: 3.0
    vision_required: false
    max_tokens: 4096
    temperature: 0.7
    top_p: 0.9

  qwen2.5-coder:7b:
    ollama_tag: "qwen2.5-coder:7b"
    reasoning_tier: medium
    arabic_quality: 0.60
    code_bias: 0.95
    latency_tier: fast
    vram_estimate_gb: 4.7
    vision_required: false
    max_tokens: 8192
    temperature: 0.2
    top_p: 0.95

  llava:7b:
    ollama_tag: "llava:7b"
    reasoning_tier: medium
    arabic_quality: 0.65
    code_bias: 0.1
    latency_tier: medium
    vram_estimate_gb: 4.5
    vision_required: true
    max_tokens: 4096
    temperature: 0.7
    top_p: 0.9
```

**SUCCESS CRITERIA:**
- [ ] File is valid YAML
- [ ] All 4 models have all required capability fields
- [ ] `routing_weights` sum direction is sensible (all > 0)

---

### TASK 1.4 — Create `config/identity.yaml`

**INPUT:** Nothing  
**OUTPUT:** Jarvis system identity definition  
**FILES TO CREATE:** `config/identity.yaml`

```yaml
name: "Jarvis"
version: "0.4.0"
role: "Personal AI assistant running fully locally"
architecture: "Multi-model local system with tool execution"

capabilities:
  - "Conversational AI in Arabic and English"
  - "Computer and file control"
  - "Browser automation"
  - "Google services integration"
  - "Voice interaction"
  - "Image understanding and generation"
  - "Multi-step task planning"

tone:
  default: "Professional, concise, helpful"
  arabic: "Natural Modern Standard Arabic, formal but approachable"

behavior:
  always_confirm_destructive_actions: true
  default_language: "auto-detect"
  show_reasoning: false
```

**SUCCESS CRITERIA:**
- [ ] File is valid YAML
- [ ] Identity loads without error in `src/core/identity/jarvis_profile.py` (Phase 1.6)

---

### TASK 1.5 — Create `.env.example`

**INPUT:** Nothing  
**OUTPUT:** Template for all required environment variables  
**FILES TO CREATE:** `.env.example`

```env
# Telegram Bot (required for Telegram interface)
TELEGRAM_BOT_TOKEN=

# Google APIs (required for Calendar, Gmail, Drive, Contacts, YouTube)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
YOUTUBE_API_KEY=

# Redis (optional — falls back to in-memory if not set)
REDIS_URL=redis://localhost:6379

# Environment
JARVIS_ENV=development
```

**SUCCESS CRITERIA:**
- [ ] File exists
- [ ] Every variable has a comment explaining where to get it
- [ ] `.env` (without `.example`) is in `.gitignore`

---

### TASK 1.6 — Create settings loader

**INPUT:** `config/settings.yaml`, `.env`  
**OUTPUT:** A Python module that loads all config into typed Pydantic models  
**FILES TO CREATE:** `src/settings.py`

```python
# Pydantic Settings model that reads from config/settings.yaml + .env
# Accessible anywhere via: from settings import settings
```

Requirements:
- Use `pydantic-settings` with `BaseSettings`
- Load YAML file path from env var `JARVIS_CONFIG` (default: `config/settings.yaml`)
- Nested models for each section (runtime, models, hardware, etc.)
- Fail fast with a clear error if required fields are missing

**SUCCESS CRITERIA:**
- [ ] `from settings import settings; print(settings.jarvis.name)` prints "Jarvis"
- [ ] Missing required field raises `ValidationError` with a clear message
- [ ] Runs without error: `python -c "from settings import settings"`

---

### TASK 1.7 — Create logging setup

**INPUT:** `config/settings.yaml` (log path)  
**OUTPUT:** Loguru configured for file + console output  
**FILES TO CREATE:** `src/logger.py`

```python
# from logger import logger
# logger.info("Jarvis started")
```

Requirements:
- Console: colored, human-readable, INFO level
- File: `logs/jarvis.log`, JSON format, DEBUG level, daily rotation, 7-day retention
- Expose a single `logger` object importable from anywhere

**SUCCESS CRITERIA:**
- [ ] `from logger import logger; logger.info("test")` writes to both console and file
- [ ] Log file created at `logs/jarvis.log`
- [ ] JSON log entries have: `timestamp`, `level`, `message`, `module`

---

### TASK 1.8 — Create `app/main.py` entry point

**INPUT:** `src/settings.py`, `src/logger.py`  
**OUTPUT:** A bootable entry point that accepts `--interface` flag  
**FILES TO CREATE:** `app/main.py`

```python
# python app/main.py --interface cli
# python app/main.py --interface web
# python app/main.py --interface all
```

Requirements:
- Parse `--interface` argument: `cli | web | telegram | gui | voice | all`
- Initialize logger
- Load settings
- Print "Jarvis ready. Interface: {interface}" to console
- Graceful `Ctrl+C` exit with cleanup message

**SUCCESS CRITERIA:**
- [ ] `python app/main.py --interface cli` runs without crashing
- [ ] `python app/main.py --help` shows available options
- [ ] `Ctrl+C` exits cleanly with no traceback

---

### TASK 1.9 — Create `requirements.txt`

**INPUT:** All phases planned  
**OUTPUT:** Version-pinned dependency list  
**FILES TO MODIFY:** `requirements.txt`

Group by purpose with comments. Include all packages needed for all phases.

**SUCCESS CRITERIA:**
- [ ] `pip install -r requirements.txt` completes without errors in a clean venv
- [ ] No `pip` warnings about conflicting versions

---

## ⚡ Phase 2 — Minimal Working System

> **Goal:** One complete path works end-to-end: user types text → LLM responds → output shown.  
> No tools, no memory, no agents. Just: input → LLM → output.  
> **Done when:** `python app/main.py --interface cli` accepts user input and streams a real LLM response.

---

### TASK 2.1 — Create LLM engine

**INPUT:** A model name (string) + a list of messages  
**OUTPUT:** Streamed text response from Ollama  
**FILES TO CREATE:** `src/models/llm/engine.py`

```python
class OllamaEngine:
    def chat(self, messages: list[dict], model: str, stream: bool = True) -> Generator[str, None, None]
    def generate(self, prompt: str, model: str) -> str
    def is_available(self) -> bool  # ping Ollama API
```

Requirements:
- Connects to Ollama at `http://localhost:11434`
- Streaming via generator (yield token by token)
- Retry on connection failure: 3 attempts, exponential backoff
- Return structured response: `{text, model, tokens_used, latency_ms}`
- Parse tool calls from response if present (`tool_calls` block)

**SUCCESS CRITERIA:**
- [ ] `engine.is_available()` returns `True` when Ollama is running
- [ ] `engine.chat([{"role":"user","content":"Hello"}], "gemma3:4b")` yields tokens
- [ ] Arabic input produces Arabic output
- [ ] Connection failure raises `LLMConnectionError` with useful message

---

### TASK 2.2 — Create base model abstractions

**INPUT:** Nothing  
**OUTPUT:** Abstract base classes for all model types  
**FILES TO CREATE:**
- `src/models/base/llm_base.py`
- `src/models/base/vision_base.py`
- `src/models/base/speech_base.py`

```python
# llm_base.py
class LLMBase(ABC):
    @abstractmethod
    def chat(self, messages: list[dict], model: str) -> Generator[str, None, None]: ...
    @abstractmethod
    def generate(self, prompt: str, model: str) -> str: ...
```

**SUCCESS CRITERIA:**
- [ ] `OllamaEngine` inherits from `LLMBase` without error
- [ ] Abstract methods are enforced (instantiating `LLMBase` directly raises `TypeError`)

---

### TASK 2.3 — Create prompt mode packs

**INPUT:** A mode name (`fast | normal | deep | planning | research`)  
**OUTPUT:** System prompt fragment for that mode  
**FILES TO CREATE:** `src/models/llm/prompts.py`

```python
MODE_PACKS = {
    "fast": "Be concise. Answer directly. No preamble.",
    "normal": "Give a clear, complete answer.",
    "deep": "Think step by step. Show your reasoning. Check your work.",
    "planning": "Decompose the task into numbered steps before executing.",
    "research": "Query multiple angles. Cite sources. Acknowledge uncertainty.",
}

def build_system_prompt(mode: str, identity: str, user_context: str) -> str:
    ...
```

**SUCCESS CRITERIA:**
- [ ] `build_system_prompt("fast", ...)` returns a non-empty string
- [ ] All 5 modes produce distinct prompt fragments
- [ ] Arabic personality included when `identity` parameter is passed

---

### TASK 2.4 — Create minimal runtime loop (stub)

**INPUT:** User text message  
**OUTPUT:** Streamed LLM response  
**FILES TO CREATE:** `src/core/runtime/loop.py`

This is the simplified version — no decision layer, no tools, no memory:

```python
class RuntimeLoop:
    def run(self, user_input: str, session_id: str) -> Generator[str, None, None]:
        # 1. Observe: construct messages list from user_input
        # 2. Think: call LLM engine with default model
        # 3. Stream response back
```

**SUCCESS CRITERIA:**
- [ ] `loop.run("Hello")` yields streamed text
- [ ] `loop.run("مرحبا")` responds in Arabic
- [ ] Loop does not crash on empty input (returns polite error message)

---

### TASK 2.5 — Wire CLI to runtime loop

**INPUT:** `RuntimeLoop` from Task 2.4  
**OUTPUT:** A working interactive CLI session  
**FILES TO CREATE:** `src/interfaces/cli/interface.py`

```python
class CLIInterface:
    def start(self):
        # Show prompt → get input → call runtime loop → print streamed response → repeat
```

Requirements:
- Use `Rich` for display
- Stream tokens as they arrive (no waiting for full response)
- Handle `Ctrl+C` gracefully
- Show thinking indicator while LLM is working

**FILES TO MODIFY:** `app/main.py` — connect `--interface cli` to `CLIInterface`

**SUCCESS CRITERIA:**
- [ ] `python app/main.py --interface cli` shows a prompt
- [ ] Typing "Hello" produces a real streamed LLM response
- [ ] Typing in Arabic produces an Arabic response
- [ ] `Ctrl+C` exits cleanly

---

## 🔄 Phase 3 — Runtime Loop

> **Goal:** The full Observe → Decide → Act → Evaluate loop with escalation.  
> **Done when:** The loop can escalate from fast mode to deep mode when confidence is low.

---

### TASK 3.1 — Create runtime state

**INPUT:** A session ID and turn data  
**OUTPUT:** A state object that tracks the current turn  
**FILES TO CREATE:** `src/core/runtime/state.py`

```python
@dataclass
class TurnState:
    session_id: str
    step_index: int = 0
    messages: list[dict] = field(default_factory=list)
    pending_tool_calls: list[dict] = field(default_factory=list)
    last_observation: str = ""
    tool_traces: list[dict] = field(default_factory=list)
    confidence: float = 0.0
    mode: str = "normal"
    model: str = ""
    
    def to_dict(self) -> dict: ...  # for JSON serialization
```

**SUCCESS CRITERIA:**
- [ ] `TurnState` serializes to JSON without error
- [ ] `step_index` increments correctly through the loop
- [ ] State is independent per session (no shared state between sessions)

---

### TASK 3.2 — Create evaluate module

**INPUT:** Candidate answer (str) + tool traces + decision output  
**OUTPUT:** `EvaluationResult` with quality score + recommendation  
**FILES TO CREATE:** `src/core/runtime/evaluate.py`

```python
@dataclass
class EvaluationResult:
    quality_score: float        # 0.0 to 1.0
    posterior_confidence: float # 0.0 to 1.0
    recommendation: Literal["finish", "escalate"]
    reason: str

class Evaluator:
    def evaluate(self, answer: str, state: TurnState, decision: DecisionOutput) -> EvaluationResult:
        ...
```

Scoring heuristics (no LLM call needed here):
- Empty answer → quality 0.0, escalate
- Answer shorter than question → quality 0.3
- Tool call failed → quality 0.4, escalate
- Answer contains question keywords → quality 0.8+
- Threshold: quality < 0.5 → escalate

**SUCCESS CRITERIA:**
- [ ] Empty answer → `recommendation == "escalate"`
- [ ] Solid answer → `recommendation == "finish"`
- [ ] Tool failure sets `quality_score < 0.5`

---

### TASK 3.3 — Upgrade RuntimeLoop to full Observe→Decide→Act→Evaluate

**INPUT:** `TurnState` + `Evaluator` + `DecisionLayer` (stub from Phase 4)  
**OUTPUT:** Full loop with escalation  
**FILES TO MODIFY:** `src/core/runtime/loop.py`

```python
class RuntimeLoop:
    def run(self, user_input: str, session_id: str) -> Generator[str, None, None]:
        state = TurnState(session_id=session_id)
        
        for iteration in range(self.max_iterations):
            # 1. Observe: build observation from state + input
            observation = self._observe(user_input, state)
            
            # 2. Decide: classify intent and select mode/model
            decision = self.decision_layer.decide(observation)
            
            # 3. Act: call LLM (tools are no-op stubs until Phase 7)
            answer = yield from self._think_and_act(observation, decision, state)
            
            # 4. Evaluate: score quality
            result = self.evaluator.evaluate(answer, state, decision)
            
            if result.recommendation == "finish":
                return
            
            # Escalate: try again with deeper mode
            state.mode = self._escalate_mode(state.mode)
            state.step_index += 1
        
        # Fallback after max iterations
        yield "I was unable to generate a satisfactory response. Please try rephrasing."
```

**SUCCESS CRITERIA:**
- [ ] Low-quality answer triggers escalation (mode upgrades: fast → normal → deep)
- [ ] Max iterations respected (no infinite loop)
- [ ] Fallback message shown when all iterations exhausted
- [ ] `step_index` increments each iteration

---

## 🧭 Phase 4 — Decision Layer

> **Goal:** Classify every input before acting on it.  
> **Done when:** "open Chrome" is classified as `action`, and "what is Python?" is classified as `chat`.

---

### TASK 4.1 — Create DecisionOutput schema

**INPUT:** Nothing  
**OUTPUT:** Pydantic model for decision output  
**FILES TO CREATE:** `src/core/runtime/decision.py`

```python
class IntentType(str, Enum):
    CHAT = "chat"
    CODE = "code"
    ACTION = "action"        # OS/tool/computer control
    RESEARCH = "research"
    VISION = "vision"

class ComplexityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class ThinkingMode(str, Enum):
    FAST = "fast"
    NORMAL = "normal"
    DEEP = "deep"
    PLANNING = "planning"
    RESEARCH = "research"

@dataclass
class CostEstimate:
    tokens: int
    latency_tier: Literal["low", "medium", "high"]
    gpu_load_tier: Literal["low", "medium", "high"]

@dataclass
class DecisionOutput:
    intent: IntentType
    complexity: ComplexityLevel
    mode: ThinkingMode
    requires_tools: bool
    requires_planning: bool
    prior_confidence: float
    cost_estimate: CostEstimate
    model_preference: str = "auto"
```

**SUCCESS CRITERIA:**
- [ ] All fields have type annotations
- [ ] `DecisionOutput` serializes to dict/JSON without error
- [ ] Invalid enum value raises `ValidationError`

---

### TASK 4.2 — Create DecisionLayer classifier

**INPUT:** User message (str) + optional context hints  
**OUTPUT:** `DecisionOutput`  
**FILES TO CREATE:** `src/core/runtime/decision.py` (extend from 4.1)

```python
class DecisionLayer:
    def decide(self, user_input: str, context_hints: dict = {}) -> DecisionOutput:
        ...
```

Classification rules (no LLM call — use keyword/pattern matching for speed):

| Pattern | Intent | Complexity | Mode |
|---|---|---|---|
| افتح / open / launch / run / start | action | low | fast |
| اكتب كود / write code / implement / function | code | medium | normal |
| ابحث / search / research / find info | research | high | research |
| صورة / image / picture in context | vision | medium | normal |
| Multi-step, "and then", "after that" | any | high | planning |
| Everything else | chat | low→medium | normal |

**SUCCESS CRITERIA:**
- [ ] `decide("open Chrome")` → `intent=action, requires_tools=True`
- [ ] `decide("what is Python?")` → `intent=chat, requires_tools=False`
- [ ] `decide("write a function to sort a list")` → `intent=code`
- [ ] `decide("search for the latest news and summarize it")` → `mode=research, requires_planning=True`

---

### TASK 4.3 — Create model router

**INPUT:** `DecisionOutput` + capability profiles from `config/models.yaml`  
**OUTPUT:** Model name to use for this turn  
**FILES TO CREATE:** `src/models/llm/router.py`

```python
class ModelRouter:
    def select(self, decision: DecisionOutput) -> str:
        # Score each model against decision signals
        # Return model name (e.g., "qwen3:8b")
```

Scoring formula (all weights from `config/models.yaml`):
```
score = (reasoning_match × reasoning_weight)
      + (arabic_match × arabic_weight)
      - (latency_penalty × latency_weight)
      - (cost_penalty × cost_weight)
```

Hard rules (override scoring):
- `intent == vision` → always `llava:7b`
- `intent == code` → prefer `qwen2.5-coder:7b`
- `mode == fast` and `complexity == low` → prefer `gemma3:4b`

**SUCCESS CRITERIA:**
- [ ] Vision intent → returns `"llava:7b"`
- [ ] Code intent → returns `"qwen2.5-coder:7b"`
- [ ] Fast + low complexity → returns `"gemma3:4b"`
- [ ] Deep + Arabic → returns `"qwen3:8b"`
- [ ] No model name is hardcoded in Python (all come from config)

---

## 📥 Phase 5 — Context Buffer

> **Goal:** Stage inputs from the current turn before the loop runs.  
> **Done when:** User can attach a file and it's available to the runtime during the turn.

---

### TASK 5.1 — Create context buffer

**INPUT:** Text, file path, image path, or audio path  
**OUTPUT:** A staged snapshot ready for the runtime to read  
**FILES TO CREATE:** `src/core/context/buffer.py`

```python
class InputItem:
    id: str              # UUID
    type: Literal["text", "file", "image", "audio"]
    content: str         # text content OR file path (for non-text types)
    mime_type: str
    source: str          # which interface submitted this
    timestamp: float

class ContextBuffer:
    def add(self, item: InputItem) -> str          # returns item.id
    def snapshot(self) -> list[InputItem]           # read-only view
    def clear(self)                                 # called after turn completes
    def get(self, input_id: str) -> InputItem | None
```

Requirements:
- In-memory only (no persistence — context is turn-scoped)
- Configurable idle TTL: auto-evict stale inputs
- Thread-safe (multiple interface threads may write simultaneously)

**SUCCESS CRITERIA:**
- [ ] `buffer.add(text_item)` returns a UUID string
- [ ] `buffer.snapshot()` returns all staged items
- [ ] `buffer.clear()` empties the buffer
- [ ] TTL eviction: item not accessed for 60s is removed

---

### TASK 5.2 — Wire context buffer into runtime

**INPUT:** `ContextBuffer` from Task 5.1  
**OUTPUT:** Runtime reads from buffer at Observe step  
**FILES TO MODIFY:** `src/core/runtime/loop.py`

In `_observe()`:
```python
def _observe(self, user_input: str, state: TurnState) -> str:
    items = self.context_buffer.snapshot()
    
    observation = user_input
    
    for item in items:
        if item.type == "file":
            observation += f"\n[Attached file: {item.content}]"
        elif item.type == "image":
            observation += f"\n[Attached image: {item.content}]"
    
    return observation
```

**SUCCESS CRITERIA:**
- [ ] File attached to buffer → appears in observation string
- [ ] Buffer cleared after turn completes
- [ ] Empty buffer → observation equals raw user input

---

## 💾 Phase 6 — Memory

> **Goal:** Jarvis remembers conversations. Facts from Session 1 are recalled in Session 2.  
> **Done when:** Telling Jarvis your name in one session allows it to recall your name in another.

---

### TASK 6.1 — Create short-term memory

**INPUT:** A conversation turn (role + content + session_id)  
**OUTPUT:** Retrievable conversation history  
**FILES TO CREATE:** `src/core/memory/short_term.py`

```python
class ShortTermMemory:
    def save(self, role: str, content: str, session_id: str): ...
    def get_history(self, session_id: str, max_messages: int = 20) -> list[dict]: ...
    def clear(self, session_id: str): ...
```

Requirements:
- Primary backend: Redis (`REDIS_URL` from `.env`)
- Fallback: in-memory dict (if Redis unavailable)
- Token-aware trimming: drop oldest messages when history exceeds 4000 tokens
- Auto-reconnect to Redis on failure

**SUCCESS CRITERIA:**
- [ ] `save("user", "Hello", "session_1")` stores the message
- [ ] `get_history("session_1")` returns stored messages in order
- [ ] Redis failure → automatic fallback to in-memory (no crash)
- [ ] Messages persist across function calls within a session

---

### TASK 6.2 — Create long-term memory

**INPUT:** A fact or outcome string + optional metadata  
**OUTPUT:** Semantically searchable memory store  
**FILES TO CREATE:** `src/core/memory/long_term.py`

```python
class LongTermMemory:
    def remember(self, text: str, metadata: dict = {}): ...
    def recall(self, query: str, n: int = 5) -> list[dict]: ...
    def clear(self): ...
```

Requirements:
- Backend: ChromaDB with `sentence-transformers` embeddings (`all-MiniLM-L6-v2`)
- One ChromaDB collection per user
- `recall()` returns top-N results sorted by semantic similarity
- Collection survives restart

**SUCCESS CRITERIA:**
- [ ] `remember("User's name is Ahmed")` stores the fact
- [ ] `recall("what is the user's name?")` returns the stored fact as top result
- [ ] Facts from previous session are recalled in a new session
- [ ] `recall()` returns results in descending similarity order

---

### TASK 6.3 — Create structured database

**INPUT:** Conversation turns, facts, tasks, feedback  
**OUTPUT:** SQLite database with correct schema  
**FILES TO CREATE:** `src/core/memory/database.py`

Tables:
```sql
CREATE TABLE conversations (
    id TEXT PRIMARY KEY,
    session_id TEXT,
    role TEXT,
    content TEXT,
    timestamp REAL,
    model TEXT
);

CREATE TABLE facts (
    id TEXT PRIMARY KEY,
    content TEXT,
    source TEXT,
    category TEXT,
    created_at REAL,
    importance REAL DEFAULT 0.5
);

CREATE TABLE tasks (
    id TEXT PRIMARY KEY,
    title TEXT,
    status TEXT,  -- pending | running | done | failed
    priority INTEGER,
    created_at REAL,
    updated_at REAL,
    run_id TEXT
);

CREATE TABLE feedback (
    id TEXT PRIMARY KEY,
    turn_id TEXT,
    model TEXT,
    mode TEXT,
    score REAL,
    timestamp REAL
);
```

**SUCCESS CRITERIA:**
- [ ] Schema auto-created on first `import database`
- [ ] CRUD operations work for all 4 tables
- [ ] No raw string SQL formatting (all parameterized queries)
- [ ] Schema survives restart (data persists)

---

### TASK 6.4 — Create memory manager (unified interface)

**INPUT:** Query or save request  
**OUTPUT:** Results from the appropriate memory backend  
**FILES TO CREATE:** `src/core/memory/manager.py`

```python
class MemoryManager:
    def save_turn(self, role: str, content: str, session_id: str): ...
    def get_context(self, session_id: str, n: int = 10) -> list[dict]: ...
    def search(self, query: str, n: int = 5) -> list[str]: ...
    def remember(self, text: str, metadata: dict = {}): ...
```

**SUCCESS CRITERIA:**
- [ ] `manager.search("user name")` queries both short-term and long-term
- [ ] `manager.get_context("session_1")` returns messages formatted for LLM
- [ ] All backends lazy-initialize (connect only when first used)

---

### TASK 6.5 — Create user profile

**INPUT:** Observations from conversation history  
**OUTPUT:** User preferences stored as JSON file  
**FILES TO CREATE:** `src/core/identity/user_profile.py`

```python
@dataclass
class UserProfile:
    user_id: str
    display_name: str = ""
    language: str = "auto"           # ar | en | auto
    response_style: str = "balanced" # concise | balanced | detailed
    technical_level: str = "auto"    # beginner | intermediate | expert | auto
    timezone: str = "UTC"
    
    def save(self): ...   # saves to data/profiles/{user_id}.json
    def load(cls, user_id: str) -> "UserProfile": ...
```

**SUCCESS CRITERIA:**
- [ ] `UserProfile.load("default")` creates a new profile if one doesn't exist
- [ ] Saved profile persists across restarts
- [ ] Profile updates are reflected immediately on next load

---

### TASK 6.6 — Create identity prompt builder

**INPUT:** Jarvis identity + user profile + task context + mode  
**OUTPUT:** A fully assembled system prompt string  
**FILES TO CREATE:** `src/core/identity/prompt_builder.py`

```python
class PromptBuilder:
    def build(
        self,
        mode: str,
        user_profile: UserProfile,
        task_context: str = "",
        available_tools: list[str] = [],
    ) -> str:
        # Assembly order (mandatory):
        # 1. Jarvis identity (from config/identity.yaml)
        # 2. Safety constraints
        # 3. User preferences (language, style, level)
        # 4. Task context (current turn summary)
        # 5. Mode fragment (from prompts.py)
        # 6. Available tools (names + one-line descriptions)
```

Requirements:
- Every model call goes through this builder — no exceptions
- Token budget awareness: trim lower-priority sections if total > 2000 tokens
- Deterministic output for same inputs (no randomness)

**SUCCESS CRITERIA:**
- [ ] Output always starts with Jarvis identity block
- [ ] Arabic user → Arabic instructions in prompt
- [ ] Expert user → no "explain step by step" padding
- [ ] Tool list correctly formatted for Ollama tool-calling

---

## 🔧 Phase 7 — Tools Infrastructure

> **Goal:** Every capability in the system is a registered, callable tool.  
> **Done when:** The LLM can call a tool, the executor runs it, and the result feeds back into the loop.

---

### TASK 7.1 — Create BaseTool abstract class

**INPUT:** Nothing  
**OUTPUT:** Abstract class that all skills must implement  
**FILES TO CREATE:** `src/skills/base.py`

```python
class ToolResult:
    tool: str
    success: bool
    result: Any
    error: str | None
    duration_ms: int

class BaseTool(ABC):
    name: str          # snake_case, unique
    description: str   # one sentence for LLM
    category: str      # system | browser | api | coder | search | screen
    requires_confirmation: bool = False  # True for destructive operations
    
    @property
    @abstractmethod
    def input_schema(self) -> dict: ...  # JSON Schema
    
    @abstractmethod
    def execute(self, params: dict) -> ToolResult: ...
    
    def is_available(self) -> bool: return True  # override to check prerequisites
```

**SUCCESS CRITERIA:**
- [ ] Subclassing without implementing `execute` raises `TypeError`
- [ ] `ToolResult` serializes to dict without error
- [ ] `requires_confirmation` defaults to `False`

---

### TASK 7.2 — Create tool registry

**INPUT:** `src/skills/` directory  
**OUTPUT:** Dict of all registered tools by name  
**FILES TO CREATE:** `src/core/tools/registry.py`

```python
class ToolRegistry:
    def discover(self, skills_dir: str = "src/skills"): ...  # auto-scan for BaseTool subclasses
    def register(self, tool: BaseTool): ...
    def get(self, name: str) -> BaseTool | None: ...
    def list_enabled(self) -> list[dict]: ...          # [{name, description, schema}]
    def export_for_llm(self) -> list[dict]: ...        # Ollama-compatible tool format
```

**SUCCESS CRITERIA:**
- [ ] `registry.discover()` finds all `BaseTool` subclasses in `src/skills/`
- [ ] `registry.export_for_llm()` returns Ollama-compatible `tools` array
- [ ] Unavailable tool (`is_available()` returns False) is excluded from LLM export
- [ ] Duplicate tool names raise `ValueError`

---

### TASK 7.3 — Create tool validator

**INPUT:** Tool name + params dict  
**OUTPUT:** Validation result (valid or error list)  
**FILES TO CREATE:** `src/core/tools/validator.py`

```python
class ToolValidator:
    def validate(self, tool_name: str, params: dict) -> tuple[bool, list[str]]:
        # Returns (is_valid, error_list)
        # Validates params against tool.input_schema using jsonschema
```

**SUCCESS CRITERIA:**
- [ ] Valid params → `(True, [])`
- [ ] Missing required field → `(False, ["field 'path' is required"])`
- [ ] Wrong type → `(False, ["field 'count' must be integer"])`
- [ ] Unknown tool name → `(False, ["tool 'xyz' not found"])`

---

### TASK 7.4 — Create tool executor

**INPUT:** Tool name + validated params  
**OUTPUT:** `ToolResult`  
**FILES TO CREATE:** `src/core/tools/executor.py`

```python
class ToolExecutor:
    def execute(self, tool_name: str, params: dict) -> ToolResult:
        # 1. Look up tool in registry
        # 2. Validate params (via validator)
        # 3. If requires_confirmation → pause and ask user (Phase 10)
        # 4. Execute with timeout wrapper
        # 5. Return ToolResult
```

Requirements:
- Timeout: configurable per-tool, default 30s
- Log every execution: tool name, args hash, duration, success/failure
- `requires_confirmation` tools: pause execution and emit a confirmation request event (stub for now — auto-approve until Phase 10)

**SUCCESS CRITERIA:**
- [ ] Valid tool call → returns `ToolResult(success=True, result=...)`
- [ ] Tool raises exception → returns `ToolResult(success=False, error="...")`
- [ ] Timeout exceeded → returns `ToolResult(success=False, error="timeout")`
- [ ] All executions logged to `logs/tools.log`

---

### TASK 7.5 — Wire tools into runtime Act step

**INPUT:** `DecisionOutput` with `requires_tools=True` + LLM tool call output  
**OUTPUT:** Tool result injected as next observation  
**FILES TO MODIFY:** `src/core/runtime/loop.py`

In `_think_and_act()`:
```python
# If LLM emits a tool_call in its response:
if tool_calls := self._parse_tool_calls(llm_response):
    for call in tool_calls:
        result = self.tool_executor.execute(call["name"], call["args"])
        state.tool_traces.append(result.to_dict())
        # Feed result as next observation → loop continues
```

**SUCCESS CRITERIA:**
- [ ] LLM tool call → executor runs → result feeds back into loop
- [ ] Failed tool call → error appears in observation, loop continues (not crash)
- [ ] `state.tool_traces` populated after tool execution

---

## 🤖 Phase 8 — Agents

> **Goal:** Multi-step reasoning and planning.  
> **Done when:** "Search the web for X and summarize it" executes without step-by-step guidance.

---

### TASK 8.1 — Create Planner agent

**INPUT:** A complex goal (str) + `DecisionOutput`  
**OUTPUT:** Ordered list of steps, each with a tool assignment  
**FILES TO CREATE:** `src/core/agents/planner.py`

```python
class Step:
    id: str
    title: str
    tool: str | None        # tool name, or None for LLM-only step
    inputs: dict
    depends_on: list[str]   # step IDs that must complete first

class Planner:
    def decompose(self, goal: str, decision: DecisionOutput) -> list[Step]: ...
    def execute(self, steps: list[Step], state: TurnState) -> Generator[str, None, None]: ...
```

**SUCCESS CRITERIA:**
- [ ] "Search X and summarize it" → 2 steps: [search, summarize]
- [ ] Step dependencies respected (summarize runs after search)
- [ ] Each step result passed to dependent steps

---

### TASK 8.2 — Create Thinker agent

**INPUT:** A question requiring extended reasoning  
**OUTPUT:** Reasoned answer with confidence score  
**FILES TO CREATE:** `src/core/agents/thinker.py`

```python
class Thinker:
    def reason(self, question: str, context: str, state: TurnState) -> dict:
        # Returns: {answer: str, reasoning_steps: list[str], confidence: float}
```

Requirements:
- Use `qwen3:8b` with `deep` mode
- Chain-of-thought: break into sub-questions before answering
- Self-verification: ask "Is this answer complete and correct?"
- VRAM guard: respect single-model constraint

**SUCCESS CRITERIA:**
- [ ] Multi-part question → reasoning shows sub-steps
- [ ] Confidence score present in output
- [ ] VRAM guard: no second heavy model loads while Thinker runs

---

### TASK 8.3 — Create Researcher agent

**INPUT:** A research topic  
**OUTPUT:** Structured report with sources  
**FILES TO CREATE:** `src/core/agents/researcher.py`

```python
class Researcher:
    def research(self, topic: str, state: TurnState) -> dict:
        # Returns: {summary: str, key_points: list[str], sources: list[str]}
```

Requirements:
- Run 3–5 distinct web search queries on the topic
- Scrape and summarize top results
- Cross-reference: flag contradictions between sources
- Requires `web_search` tool to be available

**SUCCESS CRITERIA:**
- [ ] `research("latest Python features")` returns at least 3 key points
- [ ] Sources list contains real URLs
- [ ] Works even if one search query returns no results

---

### TASK 8.4 — Wire orchestrator

**INPUT:** `DecisionOutput`  
**OUTPUT:** Correct agent or tool executor selected  
**FILES TO CREATE:**
- `src/core/orchestrator/dispatcher.py`
- `src/core/orchestrator/agent_selector.py`
- `src/core/orchestrator/tool_router.py`

```python
class Dispatcher:
    def route(self, decision: DecisionOutput, state: TurnState) -> Callable:
        # Returns the appropriate handler:
        # requires_planning=True → Planner
        # intent=research → Researcher
        # requires_tools=True → ToolExecutor
        # else → direct LLM
```

**SUCCESS CRITERIA:**
- [ ] `decision.requires_planning=True` → Planner called
- [ ] `decision.intent=RESEARCH` → Researcher called
- [ ] `decision.requires_tools=True, requires_planning=False` → ToolExecutor called
- [ ] `decision.intent=CHAT` → direct LLM, no agent

---

## 🛠️ Phase 9 — Skills

> **Goal:** Implement the concrete tool capabilities.  
> **Done when:** "Open Chrome", "search the web", "read clipboard" all work via natural language.

---

### TASK 9.1 — App launcher tool

**INPUT:** `{app_name: str}`  
**OUTPUT:** `ToolResult` with success/failure  
**FILES TO CREATE:** `src/skills/system/app_launcher.py`

```python
class AppLauncherTool(BaseTool):
    name = "app_launcher"
    description = "Open a Windows application by name"
    requires_confirmation = False
    
    def execute(self, params: dict) -> ToolResult:
        # Search: PATH → Start Menu → Program Files → AppData
```

**SUCCESS CRITERIA:**
- [ ] `execute({"app_name": "notepad"})` opens Notepad
- [ ] `execute({"app_name": "chrome"})` opens Chrome (if installed)
- [ ] Unknown app → `ToolResult(success=False, error="App 'xyz' not found")`

---

### TASK 9.2 — File operations tool

**INPUT:** Operation + path + optional content  
**OUTPUT:** `ToolResult` with file content or operation result  
**FILES TO CREATE:** `src/skills/system/file_ops.py`

Operations: `list | read | write | move | copy | delete | search`

**SUCCESS CRITERIA:**
- [ ] `read("README.md")` returns file content
- [ ] `write("test.txt", "hello")` creates file
- [ ] `delete()` moves to recycle bin (not permanent delete)
- [ ] Path outside allowed roots → `ToolResult(success=False, error="access denied")`

---

### TASK 9.3 — Web search tool

**INPUT:** `{query: str, max_results: int = 5}`  
**OUTPUT:** List of results with title + snippet + URL  
**FILES TO CREATE:** `src/skills/search/web_search.py`

Requirements:
- Use DuckDuckGo HTML (no API key required)
- Optional content extraction via `trafilatura`
- TTL cache: same query within 5 minutes returns cached result

**SUCCESS CRITERIA:**
- [ ] `execute({"query": "Python 3.13 features"})` returns ≥3 results
- [ ] Each result has `title`, `snippet`, `url` fields
- [ ] Works without any API key

---

### TASK 9.4 — Clipboard tool

**INPUT:** `{operation: "read" | "write", content: str | None}`  
**OUTPUT:** Clipboard content or write confirmation  
**FILES TO CREATE:** `src/skills/system/clipboard.py`

**SUCCESS CRITERIA:**
- [ ] `read` operation returns current clipboard text
- [ ] `write` operation sets clipboard content
- [ ] Image on clipboard → returns `"[IMAGE: saved to data/clipboard_image.png]"`

---

### TASK 9.5 — Code executor tool

**INPUT:** `{language: "python" | "shell", code: str}`  
**OUTPUT:** `{stdout, stderr, returncode, duration_ms}`  
**FILES TO CREATE:** `src/skills/coder/code_executor.py`

Requirements:
- Python: subprocess isolation, 30s timeout
- Shell/PowerShell: blocklist dangerous patterns before execution
- `requires_confirmation = True` for shell commands

**SUCCESS CRITERIA:**
- [ ] `execute({"language": "python", "code": "print('hello')"})` → `stdout: "hello\n"`
- [ ] Timeout → returns `ToolResult(success=False, error="timeout after 30s")`
- [ ] Blocked pattern → `ToolResult(success=False, error="blocked: dangerous pattern")`

---

### TASK 9.6 — Browser tool (Playwright)

**INPUT:** `{action: str, ...action_params}`  
**OUTPUT:** `ToolResult` with page content or action confirmation  
**FILES TO CREATE:**
- `src/skills/browser/browser.py`
- `src/skills/browser/session_manager.py`

Actions: `navigate | click | fill | extract | screenshot | download`

Session manager: save/load Playwright storage state per domain.

**SUCCESS CRITERIA:**
- [ ] `navigate(url)` opens page and returns title
- [ ] Session saved after login → reloaded on next run (no re-login)
- [ ] `extract()` returns page content as Markdown

---

### TASK 9.7 — Google APIs (Calendar + Gmail + Drive)

**INPUT:** OAuth credentials + operation params  
**OUTPUT:** `ToolResult` with API response  
**FILES TO CREATE:**
- `src/skills/api/google_auth.py`
- `src/skills/api/calendar.py`
- `src/skills/api/gmail.py`
- `src/skills/api/drive.py`

Requirements:
- Single OAuth consent screen for all Google APIs
- Token auto-refresh
- Token stored in `data/google_token.json` (gitignored)

**SUCCESS CRITERIA:**
- [ ] OAuth flow completes and token saved
- [ ] Calendar: create + read + delete event
- [ ] Gmail: send + read emails
- [ ] Drive: upload + download file
- [ ] All three work with the same token (no duplicate consent)

---

## 🛡️ Phase 10 — Safety

> **Goal:** Dangerous operations require confirmation. All actions are classified.  
> **Done when:** "delete all files in Downloads" pauses and asks for confirmation.

---

### TASK 10.1 — Action classifier

**INPUT:** Tool name + params  
**OUTPUT:** Safety classification  
**FILES TO CREATE:** `src/core/safety/classifier.py`

```python
class SafetyClass(str, Enum):
    SAFE = "safe"           # read operations, informational
    RISKY = "risky"         # writes, network calls
    CRITICAL = "critical"   # delete, send email, kill process, shell commands

class SafetyClassifier:
    def classify(self, tool_name: str, params: dict) -> SafetyClass: ...
```

Classification rules (from config — no hardcoding):
- Read operations → `SAFE`
- Write/create operations → `RISKY`
- Delete/kill/send/format → `CRITICAL`

**SUCCESS CRITERIA:**
- [ ] `file_ops.read` → `SAFE`
- [ ] `file_ops.write` → `RISKY`
- [ ] `file_ops.delete` → `CRITICAL`
- [ ] `gmail.send` → `CRITICAL`
- [ ] `code_executor` (shell) → `CRITICAL`

---

### TASK 10.2 — Confirmation gate

**INPUT:** `SafetyClass` + tool + params  
**OUTPUT:** User approval or denial  
**FILES TO CREATE:** `src/core/safety/confirmation.py`

```python
class ConfirmationGate:
    def request(self, tool_name: str, params: dict, safety_class: SafetyClass) -> bool:
        # SAFE → auto-approve
        # RISKY → log but auto-approve (with config option to require confirmation)
        # CRITICAL → emit confirmation request event, wait for user response
```

**SUCCESS CRITERIA:**
- [ ] `SAFE` action → proceeds immediately
- [ ] `CRITICAL` action → loop pauses, confirmation message shown, proceeds only on "yes"
- [ ] Denied action → `ToolResult(success=False, error="user denied")`

---

## 📊 Phase 11 — Logging + Observability

> **Goal:** Every decision, tool call, and model call is logged in structured format.  
> **Done when:** Running `grep "tool_name" logs/tools.log` returns actual tool execution records.

---

### TASK 11.1 — Structured decision logging

**INPUT:** `DecisionOutput` per turn  
**OUTPUT:** JSON log entry in `logs/decisions.log`  
**FILES TO MODIFY:** `src/core/runtime/decision.py`

Log format:
```json
{
  "timestamp": 1234567890.123,
  "session_id": "abc123",
  "intent": "action",
  "complexity": "low",
  "mode": "fast",
  "model_selected": "gemma3:4b",
  "requires_tools": true,
  "prior_confidence": 0.85
}
```

**SUCCESS CRITERIA:**
- [ ] Every `DecisionLayer.decide()` call produces a log entry
- [ ] Log file exists and is readable JSON Lines format
- [ ] `session_id` is always present

---

### TASK 11.2 — Structured tool execution logging

**INPUT:** `ToolResult` per execution  
**OUTPUT:** JSON log entry in `logs/tools.log`  
**FILES TO MODIFY:** `src/core/tools/executor.py`

Log format:
```json
{
  "timestamp": 1234567890.123,
  "tool": "app_launcher",
  "args_hash": "abc123",
  "success": true,
  "duration_ms": 245,
  "error": null
}
```

**SUCCESS CRITERIA:**
- [ ] Every tool execution produces a log entry
- [ ] Failed executions have `error` field populated
- [ ] `args_hash` is SHA256 of args dict (no raw credentials logged)

---

### TASK 11.3 — Structured model call logging

**INPUT:** Model name + mode + token counts + latency  
**OUTPUT:** JSON log entry in `logs/models.log`  
**FILES TO MODIFY:** `src/models/llm/engine.py`

**SUCCESS CRITERIA:**
- [ ] Every LLM call produces a log entry
- [ ] Log contains: model, mode, prompt_tokens, completion_tokens, latency_ms
- [ ] VRAM load/unload events logged

---

## 💻 Phase 12 — CLI Interface

> **Goal:** Full-featured terminal chat with streaming, Arabic RTL, and slash commands.  
> **Done when:** Arabic conversation works with RTL display, all slash commands respond correctly.

---

### TASK 12.1 — Full CLI interface

**INPUT:** User text via terminal  
**OUTPUT:** Streamed response with Rich formatting  
**FILES TO MODIFY:** `src/interfaces/cli/interface.py`

Requirements:
- Token-by-token streaming (no flicker)
- Arabic RTL detection per message
- Typing indicator while LLM generates
- Status bar: current model, mode, session stats

**SUCCESS CRITERIA:**
- [ ] Arabic text displays right-aligned
- [ ] Response streams token by token
- [ ] Status bar shows correct model name

---

### TASK 12.2 — Slash command system

**INPUT:** User types `/command [args]`  
**OUTPUT:** Command executes and shows result  
**FILES TO CREATE:** `src/interfaces/cli/commands.py`

Commands:
- `/clear` — clear conversation history (with confirmation)
- `/model [name]` — switch model (validates against `ollama list`)
- `/mode [fast|normal|deep|planning|research]` — switch thinking mode
- `/memory` — show recent memories
- `/tools` — list registered tools with status
- `/status` — current model, mode, VRAM, session info
- `/help` — show all commands

**SUCCESS CRITERIA:**
- [ ] All commands respond without error
- [ ] `/model invalid_name` shows error, doesn't switch
- [ ] `/tools` lists at least the tools from Phase 9

---

## 🌐 Phase 13 — Web UI

> **Goal:** Real-time streaming chat in browser with Arabic RTL support.  
> **Done when:** Browser chat works with streaming, file upload, and Arabic text.

---

### TASK 13.1 — FastAPI backend + WebSocket

**INPUT:** User message via WebSocket  
**OUTPUT:** Streamed tokens via WebSocket  
**FILES TO CREATE:**
- `src/interfaces/web/app.py`
- `src/interfaces/web/websocket.py`

**SUCCESS CRITERIA:**
- [ ] WebSocket connects and stays alive
- [ ] Tokens stream in real time
- [ ] Disconnection handled gracefully (no crash)

---

### TASK 13.2 — Chat UI (single HTML file)

**INPUT:** Nothing (static file)  
**OUTPUT:** Working chat interface  
**FILES TO CREATE:** `src/interfaces/web/templates/index.html`

Requirements:
- Single-file (HTML + CSS + JS in one file)
- Dark theme, clean design
- Arabic RTL support per message
- Streaming display with cursor
- File attachment support

**SUCCESS CRITERIA:**
- [ ] Loads at `http://localhost:8080`
- [ ] Arabic messages display RTL
- [ ] File attached → appears in input area → sent to backend
- [ ] Works on mobile (375px viewport)

---

## 🎤 Phase 14 — Voice Pipeline

> **Goal:** "Hey Jarvis" → record → transcribe → respond → speak.  
> **Done when:** Full voice cycle works in under 15 seconds total.

---

### TASK 14.1 — STT (Whisper)

**INPUT:** Audio array from microphone  
**OUTPUT:** `{text: str, language: str, confidence: float}`  
**FILES TO CREATE:** `src/models/speech/stt.py`

**SUCCESS CRITERIA:**
- [ ] Arabic phrase transcribed correctly
- [ ] Language auto-detected (ar vs en)
- [ ] Works on CPU (CUDA optional)

---

### TASK 14.2 — TTS (Piper)

**INPUT:** Text string + language  
**OUTPUT:** Audio played through speakers  
**FILES TO CREATE:** `src/models/speech/tts.py`

**SUCCESS CRITERIA:**
- [ ] Arabic text spoken in Arabic voice
- [ ] English text spoken in English voice
- [ ] No audio artifacts or clipping

---

### TASK 14.3 — Wake word detection

**INPUT:** Continuous microphone stream  
**OUTPUT:** Event when "Hey Jarvis" detected  
**FILES TO CREATE:** `src/interfaces/voice/wake_word.py`

**SUCCESS CRITERIA:**
- [ ] "Hey Jarvis" triggers activation within 1 second
- [ ] Background noise does not trigger false positives
- [ ] Runs on background thread without blocking

---

### TASK 14.4 — Full voice pipeline

**INPUT:** Wake word event  
**OUTPUT:** Spoken LLM response  
**FILES TO CREATE:** `src/interfaces/voice/voice_interface.py`

```
wake word → VAD record → Whisper STT → runtime loop → Piper TTS → play audio → return to listening
```

**SUCCESS CRITERIA:**
- [ ] Full cycle completes in under 15 seconds
- [ ] Arabic "Hey Jarvis, what time is it?" → spoken Arabic response
- [ ] Returns to listening state after responding

---

## 📱 Phase 15 — Telegram + GUI

> **Goal:** Jarvis accessible via Telegram bot and desktop app.

---

### TASK 15.1 — Telegram bot

**FILES TO CREATE:**
- `src/interfaces/telegram/bot.py`
- `src/interfaces/telegram/handlers.py`

**SUCCESS CRITERIA:**
- [ ] Text message → LLM response
- [ ] Voice note → STT → LLM → text reply
- [ ] Photo → vision description

---

### TASK 15.2 — PyQt6 desktop app

**FILES TO CREATE:** `src/interfaces/gui/main_window.py`

**SUCCESS CRITERIA:**
- [ ] App opens and accepts text input
- [ ] Arabic RTL layout correct
- [ ] Minimizes to system tray

---

## ⚙️ Phase 16 — Optimization + QA

> **Goal:** Production-hardened. All end-to-end scenarios pass. VRAM stays under 5.5 GB.

---

### TASK 16.1 — End-to-end tests

**FILES TO CREATE:** `tests/test_e2e.py`

Scenarios:
1. "Open Chrome" → app opens
2. "Search for Python and summarize" → search + summarize
3. "Send an email to [name]" → confirmation required → sends
4. Arabic voice → spoken Arabic response
5. File attached → content used in response

**SUCCESS CRITERIA:**
- [ ] All 5 scenarios pass without manual intervention
- [ ] VRAM never exceeds 5.5 GB during any scenario
- [ ] Total test suite runs in under 5 minutes

---

### TASK 16.2 — Performance benchmarks

**SUCCESS CRITERIA:**
- [ ] Cold start to first response: < 10 seconds
- [ ] Simple fast-mode response (`gemma3:4b`): < 5 seconds
- [ ] Voice pipeline round-trip: < 15 seconds
- [ ] VRAM peak never > 5.5 GB

---

### TASK 16.3 — Security review

**SUCCESS CRITERIA:**
- [ ] No credentials appear in any log file
- [ ] All tool inputs validated against schema before execution
- [ ] Shell commands blocked list tested
- [ ] `data/google_token.json` not in git history
- [ ] Prompt injection: user input sanitized before injecting into system prompts

---

*Last updated: refactor v2 — build executable, not theoretical.*
