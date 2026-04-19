# 📁 JARVIS — Structure Reference

> This document defines: **what each folder does**, **who owns what**, and **how data flows** between layers.

---

## Guiding Principles

1. **One role per folder.** If you can't describe a folder's job in one sentence, it's wrong.
2. **No circular dependencies.** `runtime` → `orchestrator` → `agents` → `tools`. Not the reverse.
3. **Config drives behavior.** No magic numbers or hardcoded model names in Python.
4. **Skills register themselves into Tools.** Tools don't import Skills directly.

---

## Data Flow (turn lifecycle)

```
Interface receives input
    │
    ▼
context/buffer.py     ← stages input (text/file/image)
    │ snapshot()
    ▼
runtime/loop.py       ← observe()
    │ builds observation string from: input + memory + context + tool traces
    ▼
runtime/decision.py   ← decide()
    │ returns DecisionOutput (no LLM called here)
    ▼
models/llm/router.py  ← select(decision)
    │ returns model name
    ▼
identity/prompt_builder.py ← build(mode, profile)
    │ returns system prompt
    ▼
models/llm/engine.py  ← chat(messages, model, system)
    │ yields tokens OR returns tool_call JSON
    ├── [text] → runtime/evaluate.py → finish or escalate
    └── [tool_call]
              │
              ▼
    core/orchestrator/dispatcher.py ← route(decision)
              │
              ├── requires_planning=True → core/agents/planner.py
              ├── intent=research       → core/agents/researcher.py
              └── requires_tools=True   → core/tools/executor.py
                                                │
                                    registry.get(tool_name)
                                    validator.validate(params)
                                    safety.classifier.classify()
                                    confirmation.request() [if critical]
                                    skill.execute(params)
                                                │
                                         ToolResult
                                                │
                                    state.add_tool_result(result)
                                    → next observe() includes result
                                    → LLM generates final response
    │
    ▼
memory/manager.py     ← save_turn(role, content, session_id)
    │
    ▼
Interface streams response to user
```

---

## Layer Ownership

| Folder | Owns | Does NOT own |
|---|---|---|
| `core/runtime/` | Loop execution, state, iteration limits, evaluation, escalation | Agent selection, tool execution, model selection |
| `core/orchestrator/` | Routing DecisionOutput to agent or tool executor | Loop control, quality eval, model calls |
| `core/agents/` | Multi-step thinking, planning, research logic | Tool implementations, loop state |
| `core/tools/` | Tool discovery, schema validation, execution infrastructure | Skill implementations |
| `core/memory/` | Storing and retrieving data across turns | Current-turn inputs |
| `core/context/` | Staging current-turn inputs before execution | Persistence |
| `core/identity/` | Jarvis profile, user profile, prompt assembly | Memory storage |
| `core/safety/` | Action classification, confirmation gates | Tool execution |
| `models/` | AI model wrappers | Control flow, routing |
| `skills/` | Callable capability implementations | Tool system management |
| `interfaces/` | User-facing I/O, converting input to runtime calls | Business logic |

---

## Dependency Graph (allowed imports)

```
interfaces/  →  runtime/
runtime/     →  decision, memory, context, identity, models, orchestrator
orchestrator →  agents, tools
agents       →  models, tools, memory
tools        →  skills (via registry discovery, not direct import)
skills       →  (no imports from core/)
models/      →  (no imports from core/)
identity/    →  memory (read-only, for profile loading)
safety/      →  (no core imports)
```

❌ **Forbidden:**
- `models/` importing from `runtime/` or `orchestrator/`
- `skills/` importing from `core/`
- `memory/` importing from `runtime/`

---

## Full Directory Tree

```
jarvis/
│
├── app/
│   └── main.py
│       Role: Entry point only. Parses --interface, initializes logger+settings,
│             delegates to the right interface class. No business logic here.
│
├── config/
│   ├── settings.yaml       ← All tunable params. No Python constants.
│   ├── models.yaml         ← Model capability profiles + routing table.
│   ├── identity.yaml       ← Jarvis system identity (name, role, tone).
│   └── schemas/            ← JSON Schema per tool input contract.
│       ├── system/
│       │   ├── app_launcher.schema.json
│       │   ├── file_ops.schema.json
│       │   ├── clipboard.schema.json
│       │   └── code_executor.schema.json
│       ├── browser/
│       │   └── browser.schema.json
│       ├── search/
│       │   └── web_search.schema.json
│       └── api/
│           ├── calendar.schema.json
│           ├── gmail.schema.json
│           └── drive.schema.json
│
├── src/
│   │
│   ├── settings.py
│   │   Role: Pydantic settings loader. `from settings import settings` everywhere.
│   │
│   ├── logger.py
│   │   Role: Loguru config. `from logger import logger` everywhere.
│   │
│   ├── core/
│   │   │
│   │   ├── runtime/
│   │   │   ├── loop.py
│   │   │   │   Role: THE LOOP. observe→decide→think→act→evaluate.
│   │   │   │         Owns max_iterations, escalation, fallback.
│   │   │   │
│   │   │   ├── state.py
│   │   │   │   Role: TurnState dataclass. Messages, tool_traces, iteration, mode.
│   │   │   │         Mutable during a turn. One instance per turn.
│   │   │   │
│   │   │   ├── decision.py
│   │   │   │   Role: DecisionLayer + DecisionOutput.
│   │   │   │         Classifies input with keyword matching. No LLM call.
│   │   │   │         Returns: intent, complexity, mode, requires_tools, etc.
│   │   │   │
│   │   │   └── evaluate.py
│   │   │       Role: Evaluator. Scores candidate answer. Returns finish|escalate.
│   │   │             No LLM call — uses heuristics (empty, too short, tool failure).
│   │   │
│   │   ├── orchestrator/
│   │   │   ├── dispatcher.py
│   │   │   │   Role: Reads DecisionOutput. Returns route string:
│   │   │   │         "planner" | "researcher" | "tool_executor" | "direct_llm"
│   │   │   │
│   │   │   ├── agent_selector.py
│   │   │   │   Role: Given route="planner"|"researcher", returns correct Agent instance.
│   │   │   │
│   │   │   └── tool_router.py
│   │   │       Role: Given a tool_call from LLM, passes it to ToolExecutor.
│   │   │             Handles multi-tool calls if needed (future).
│   │   │
│   │   ├── agents/
│   │   │   ├── planner.py
│   │   │   │   Role: Breaks multi-step goals into ordered Steps.
│   │   │   │         Executes them sequentially. Passes Step N result to Step N+1.
│   │   │   │
│   │   │   ├── thinker.py
│   │   │   │   Role: Chain-of-thought reasoning for complex single questions.
│   │   │   │         Uses qwen3:8b in deep mode. Returns {answer, reasoning, confidence}.
│   │   │   │
│   │   │   └── researcher.py
│   │   │       Role: Multi-query research. Runs 3-5 web searches.
│   │   │             Cross-references. Returns {summary, key_points, sources}.
│   │   │
│   │   ├── tools/                 ← TOOL SYSTEM (infrastructure, not implementations)
│   │   │   ├── registry.py
│   │   │   │   Role: Auto-discovers BaseTool subclasses in skills/.
│   │   │   │         Registers them by name. Exports Ollama-compatible tool list.
│   │   │   │
│   │   │   ├── validator.py
│   │   │   │   Role: Validates tool call args against JSON Schema before execution.
│   │   │   │         Returns (is_valid: bool, errors: list[str]).
│   │   │   │
│   │   │   └── executor.py
│   │   │       Role: Runs a tool with timeout. Calls safety classifier first.
│   │   │             Returns ToolResult. Logs every execution.
│   │   │
│   │   ├── memory/
│   │   │   ├── short_term.py
│   │   │   │   Role: Session message history. Redis backend, in-memory fallback.
│   │   │   │         Max 50 messages per session. Auto-reconnects Redis.
│   │   │   │
│   │   │   ├── long_term.py
│   │   │   │   Role: Semantic fact storage. ChromaDB + sentence-transformers.
│   │   │   │         remember(text) + recall(query) → top-N similar facts.
│   │   │   │
│   │   │   ├── database.py
│   │   │   │   Role: SQLite structured storage.
│   │   │   │         Tables: conversations, facts, tasks, feedback.
│   │   │   │         All queries parameterized.
│   │   │   │
│   │   │   └── manager.py
│   │   │       Role: Unified interface to all memory backends.
│   │   │             save_turn() / get_context() / search() / remember()
│   │   │
│   │   ├── context/
│   │   │   └── buffer.py
│   │   │       Role: Stages current-turn inputs before execution.
│   │   │             add(item) → snapshot() → clear() after turn.
│   │   │             In-memory only. TTL eviction for stale inputs.
│   │   │
│   │   ├── identity/
│   │   │   ├── jarvis_profile.py
│   │   │   │   Role: Loads and validates config/identity.yaml.
│   │   │   │         Provides JARVIS_IDENTITY string for prompt builder.
│   │   │   │
│   │   │   ├── user_profile.py
│   │   │   │   Role: Per-user preferences (language, style, level).
│   │   │   │         Load from data/profiles/{user_id}.json. Default if missing.
│   │   │   │
│   │   │   └── prompt_builder.py
│   │   │       Role: Assembles system prompt for EVERY model call.
│   │   │             Order: identity → safety → user prefs → mode → tools → task
│   │   │             No model call bypasses this.
│   │   │
│   │   └── safety/
│   │       ├── classifier.py
│   │       │   Role: Classifies tool+params as safe|risky|critical.
│   │       │         Rules loaded from config. Unknown tool → risky.
│   │       │
│   │       └── confirmation.py
│   │           Role: For critical actions, pauses and asks user yes/no.
│   │                 safe → auto-approve. critical → prompt user.
│   │
│   ├── models/                    ← AI MODEL WRAPPERS
│   │   ├── base/
│   │   │   ├── llm_base.py        Abstract: chat(), generate()
│   │   │   ├── vision_base.py     Abstract: describe(image, question)
│   │   │   └── speech_base.py     Abstract: transcribe(), synthesize()
│   │   │
│   │   ├── llm/
│   │   │   ├── engine.py
│   │   │   │   Role: Ollama HTTP client. Streaming via generator.
│   │   │   │         Retry with exponential backoff. VRAM guard (unload before load).
│   │   │   │
│   │   │   ├── router.py
│   │   │   │   Role: Selects model name from DecisionOutput + config/models.yaml.
│   │   │   │         Hard rules: vision→llava, code→coder.
│   │   │   │         Mode rules: fast→gemma, deep/normal→qwen3.
│   │   │   │
│   │   │   └── prompts.py
│   │   │       Role: MODE_PACKS dict. Helper functions for prompt assembly.
│   │   │
│   │   ├── vision/
│   │   │   └── llava.py           LLaVA via Ollama. describe(image_path, question).
│   │   │
│   │   ├── speech/
│   │   │   ├── stt.py             Whisper. transcribe(audio) → {text, language, confidence}
│   │   │   └── tts.py             Piper. synthesize(text, lang) → audio → play()
│   │   │
│   │   └── diffusion/
│   │       └── sd.py              SD 1.5. generate(prompt) → PIL.Image. VRAM guard.
│   │
│   ├── skills/                    ← SKILL IMPLEMENTATIONS
│   │   │                            Registered into tool system via registry.discover()
│   │   ├── base.py                BaseTool(ABC) + ToolResult dataclass
│   │   │
│   │   ├── system/
│   │   │   ├── app_launcher.py    Open/close Windows apps by name
│   │   │   ├── file_ops.py        List/read/write/move/delete files
│   │   │   ├── clipboard.py       Read/write/monitor clipboard
│   │   │   ├── notifications.py   Windows Toast alerts
│   │   │   └── system_info.py     CPU/RAM/GPU/disk status
│   │   │
│   │   ├── browser/
│   │   │   ├── browser.py         Playwright: navigate/click/fill/extract/screenshot
│   │   │   └── session_manager.py Save/load Playwright storage state per domain
│   │   │
│   │   ├── search/
│   │   │   └── web_search.py      DuckDuckGo HTML. No API key. TTL cache.
│   │   │
│   │   ├── coder/
│   │   │   └── code_executor.py   Python + shell sandbox. Timeout. Blocklist.
│   │   │
│   │   ├── screen/
│   │   │   ├── screenshot.py      Full/region screenshots via mss
│   │   │   └── ocr.py             Tesseract OCR. No LLM needed.
│   │   │
│   │   ├── api/
│   │   │   ├── google_auth.py     Single OAuth2 for all Google APIs
│   │   │   ├── calendar.py        CRUD events
│   │   │   ├── gmail.py           Read/send/search emails
│   │   │   ├── drive.py           List/upload/download files
│   │   │   └── youtube.py         Search videos
│   │   │
│   │   └── office/
│   │       └── readers.py         docx/xlsx/pptx/pdf text extraction
│   │
│   └── interfaces/
│       ├── cli/
│       │   ├── interface.py       Rich terminal. Streaming. Arabic RTL. Slash commands.
│       │   └── commands.py        /clear /model /mode /memory /tools /status /help
│       │
│       ├── web/
│       │   ├── app.py             FastAPI + static files + session middleware
│       │   ├── websocket.py       WebSocket handler → orchestrator → stream tokens
│       │   ├── routes/            REST API: conversations, memory, settings, status
│       │   ├── static/            CSS + JS (single-file)
│       │   └── templates/
│       │       └── index.html     Single-page chat UI
│       │
│       ├── telegram/
│       │   ├── bot.py             python-telegram-bot Application setup
│       │   ├── handlers.py        text/photo/voice/document handlers
│       │   └── commands.py        /start /clear /model /image /search
│       │
│       ├── gui/
│       │   ├── main_window.py     PyQt6 chat window. Arabic RTL. System tray.
│       │   └── settings_dialog.py Model/language/theme/startup settings
│       │
│       └── voice/
│           ├── wake_word.py       openWakeWord. Background thread. EventBus event.
│           └── voice_interface.py Pipeline: wake→VAD→STT→runtime→TTS→play→listen
│
├── tests/
│   ├── test_phase1.py             Minimal working system: text → LLM → response
│   ├── test_decision.py           All intent/mode/complexity classifications
│   ├── test_router.py             Model selection from DecisionOutput
│   ├── test_tools.py              Registry discovery, schema validation, execution
│   ├── test_memory.py             Short+long term, cross-session, Redis fallback
│   ├── test_safety.py             Classification + confirmation gate
│   ├── test_agents.py             Planner step decomp, Thinker confidence, Researcher sources
│   └── test_e2e.py                Vertical slices: "say hello", "open notepad"
│
├── scripts/
│   ├── install.sh                 Linux/WSL: apt + venv + pip + playwright + Ollama pulls
│   └── install.ps1                Windows: winget + venv + pip + playwright + Ollama pulls
│
├── data/                          ← gitignored runtime data
│   ├── profiles/                  User profiles (JSON per user_id)
│   ├── sessions/                  Browser sessions (JSON per domain)
│   ├── downloads/
│   ├── screenshots/
│   ├── chroma/                    ChromaDB vector store
│   └── jarvis.db                  SQLite
│
├── logs/                          ← gitignored
│   ├── jarvis.log                 All logs (JSON Lines, daily rotation)
│   ├── decisions.log              One JSON entry per DecisionLayer.decide() call
│   ├── tools.log                  One JSON entry per tool execution
│   └── models.log                 One JSON entry per LLM call
│
├── .env                           API keys (gitignored)
├── .env.example                   Template (committed)
├── .gitignore
├── requirements.txt
├── README.md
└── TASKS.md
```

---

## Key Contracts (interfaces between layers)

### Runtime → Decision
```python
# runtime/loop.py calls:
decision: DecisionOutput = self.decision.decide(observation: str)
```

### Runtime → Router
```python
model: str = self.router.select(decision: DecisionOutput)
```

### Runtime → PromptBuilder
```python
system: str = self.prompt_builder.build(mode=decision.mode, profile=state.profile)
```

### Runtime → LLM
```python
# yields str tokens OR returns LLMOutput with has_tool_call=True
output = self.llm.chat(messages: list[dict], model: str, system: str)
```

### Runtime → Orchestrator (for tool calls)
```python
result: ToolResult = self.orchestrator.run_tool(tool_call: dict)
```

### Orchestrator → Executor
```python
result: ToolResult = self.executor.execute(tool_name: str, params: dict)
```

### Executor → Registry → Skill
```python
tool: BaseTool = self.registry.get(tool_name)
result: ToolResult = tool._run(params)
```

### Memory → Runtime (observe)
```python
history: list[dict] = self.memory.get_context(session_id, n=10)
snippets: list[str] = self.memory.search(user_input, n=3)
```

---

## What Changed from Previous Version

| Change | Reason |
|---|---|
| Removed `src/ai/` | No defined role. All AI logic is in `src/models/`. |
| Removed `src/core/brain/` | Duplicate of `src/core/orchestrator/`. "Brain" is not an engineering concept. |
| Added `src/core/safety/` | Safety logic was scattered. Now centralized with clear classifier + gate. |
| Added `src/models/base/` | Abstract contracts make models swappable (replace Whisper without breaking STT callers). |
| Split `tools/` from `skills/` | Tool system (registry/validator/executor) is infrastructure. Skills are implementations. Separation prevents circular imports. |
| Separated `context/` from `memory/` | Context = current turn only (cleared). Memory = persistent. Previously mixed. |
| Separated `identity/` from `memory/` | User profile (identity) ≠ conversation history (memory). |
| Logs split into 4 files | One file per concern: decisions, tools, models, general. Enables grep/monitoring per layer. |
