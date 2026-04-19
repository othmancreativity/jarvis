# 📁 Jarvis — Refactored Directory Structure

## What Changed (and Why)

### REMOVED
- `src/ai/` → **deleted** — had no clear role. All AI model logic lives in `src/models/`
- `src/core/brain/` → **deleted** — duplicate of `src/core/orchestrator/`. "Brain" is a vague metaphor, not an engineering concept.

### ADDED
- `src/core/tools/` → **new** — tool infrastructure (registry + validator + executor) separated from tool implementations (skills/)
- `src/core/safety/` → **new** — action classification + confirmation gates
- `src/models/base/` → **new** — abstract base classes (llm_base, vision_base, speech_base)

### RENAMED/CLARIFIED
- `src/core/orchestrator/` now contains exactly: `dispatcher.py`, `agent_selector.py`, `tool_router.py`
- `src/core/runtime/` now contains exactly: `loop.py`, `state.py`, `evaluate.py`, `decision.py`
- `src/core/identity/` separated from `src/core/memory/` — they are different concerns

---

## Final Structure

```
jarvis/
│
├── app/
│   └── main.py                          # --interface cli|web|telegram|gui|all
│
├── config/
│   ├── settings.yaml                    # All tunable params (no magic constants in Python)
│   ├── models.yaml                      # Capability profiles + routing weights
│   ├── identity.yaml                    # Jarvis system identity
│   └── schemas/                         # JSON Schemas for tool I/O contracts
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
│   ├── settings.py                      # Pydantic settings loader
│   ├── logger.py                        # Loguru config (console + file)
│   │
│   ├── core/
│   │   │
│   │   ├── runtime/                     # THE LOOP — owns turn lifecycle
│   │   │   ├── __init__.py
│   │   │   ├── loop.py                  # Observe → Decide → Act → Evaluate → Finish/Escalate
│   │   │   ├── state.py                 # TurnState (step_index, messages, tool_traces, etc.)
│   │   │   ├── evaluate.py              # Quality scorer → finish or escalate recommendation
│   │   │   └── decision.py              # DecisionLayer + DecisionOutput schema
│   │   │
│   │   ├── orchestrator/                # ROUTING — decides who handles the intent
│   │   │   ├── __init__.py
│   │   │   ├── dispatcher.py            # intent → agent | tool | direct LLM
│   │   │   ├── agent_selector.py        # selects which agent based on intent
│   │   │   └── tool_router.py           # routes to correct tool(s)
│   │   │
│   │   ├── agents/                      # THINKING — multi-step reasoning
│   │   │   ├── __init__.py
│   │   │   ├── planner.py               # Decomposes multi-step goals into ordered steps
│   │   │   ├── thinker.py               # Chain-of-thought for complex single questions
│   │   │   └── researcher.py            # Multi-source research with cross-referencing
│   │   │
│   │   ├── tools/                       # TOOL INFRASTRUCTURE — not implementations
│   │   │   ├── __init__.py
│   │   │   ├── registry.py              # Discovery, registration, LLM export
│   │   │   ├── validator.py             # Schema validation before execution
│   │   │   └── executor.py              # Runs tools, wraps results, logs, timeout
│   │   │
│   │   ├── memory/                      # PERSISTENCE across turns and sessions
│   │   │   ├── __init__.py
│   │   │   ├── short_term.py            # Session history (Redis → in-memory fallback)
│   │   │   ├── long_term.py             # Semantic memory (ChromaDB)
│   │   │   ├── database.py              # Structured storage (SQLite)
│   │   │   └── manager.py               # Unified interface
│   │   │
│   │   ├── context/                     # CURRENT-TURN inputs only — cleared after each turn
│   │   │   ├── __init__.py
│   │   │   └── buffer.py                # Stages text, files, images before execution
│   │   │
│   │   ├── identity/                    # WHO IS JARVIS + WHO IS THE USER
│   │   │   ├── __init__.py
│   │   │   ├── jarvis_profile.py        # Loads config/identity.yaml
│   │   │   ├── user_profile.py          # User preferences (language, style, level)
│   │   │   └── prompt_builder.py        # Assembles system prompt for EVERY model call
│   │   │
│   │   └── safety/                      # SAFETY — classification + confirmation
│   │       ├── __init__.py
│   │       ├── classifier.py            # safe | risky | critical
│   │       └── confirmation.py          # pause + user approval for critical actions
│   │
│   ├── models/                          # AI MODEL WRAPPERS — called by runtime, not in control
│   │   │
│   │   ├── base/                        # Abstract interfaces
│   │   │   ├── __init__.py
│   │   │   ├── llm_base.py              # chat(), generate(), tool_call()
│   │   │   ├── vision_base.py           # describe(image, question)
│   │   │   └── speech_base.py           # transcribe(), synthesize()
│   │   │
│   │   ├── llm/
│   │   │   ├── __init__.py
│   │   │   ├── engine.py                # Ollama client (streaming + retry)
│   │   │   ├── router.py                # Scores models from config/models.yaml profiles
│   │   │   └── prompts.py               # Mode packs (fast/normal/deep/planning/research)
│   │   │
│   │   ├── vision/
│   │   │   ├── __init__.py
│   │   │   └── llava.py                 # LLaVA via Ollama
│   │   │
│   │   ├── speech/
│   │   │   ├── __init__.py
│   │   │   ├── stt.py                   # Whisper (Arabic + English)
│   │   │   └── tts.py                   # Piper TTS
│   │   │
│   │   └── diffusion/
│   │       ├── __init__.py
│   │       └── sd.py                    # Stable Diffusion 1.5
│   │
│   ├── skills/                          # TOOL IMPLEMENTATIONS — registered in tools/registry.py
│   │   ├── base.py                      # BaseTool abstract class + ToolResult
│   │   │
│   │   ├── system/
│   │   │   ├── __init__.py
│   │   │   ├── app_launcher.py          # Open/close Windows apps
│   │   │   ├── file_ops.py              # List/read/write/move/delete files
│   │   │   ├── clipboard.py             # Read/write clipboard
│   │   │   ├── notifications.py         # Windows Toast alerts
│   │   │   └── system_info.py           # CPU/RAM/GPU/disk status
│   │   │
│   │   ├── browser/
│   │   │   ├── __init__.py
│   │   │   ├── browser.py               # Playwright actions (navigate/click/fill/extract)
│   │   │   ├── session_manager.py       # Persistent browser sessions (no re-login)
│   │   │   └── downloader.py            # File downloads
│   │   │
│   │   ├── search/
│   │   │   ├── __init__.py
│   │   │   └── web_search.py            # DuckDuckGo (no API key)
│   │   │
│   │   ├── coder/
│   │   │   ├── __init__.py
│   │   │   └── code_executor.py         # Python + shell sandbox
│   │   │
│   │   ├── screen/
│   │   │   ├── __init__.py
│   │   │   ├── screenshot.py            # Full/region screenshots
│   │   │   └── ocr.py                   # Tesseract OCR
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── google_auth.py           # Single OAuth flow for all Google services
│   │   │   ├── calendar.py
│   │   │   ├── gmail.py
│   │   │   ├── drive.py
│   │   │   ├── contacts.py
│   │   │   └── youtube.py
│   │   │
│   │   ├── office/
│   │   │   ├── __init__.py
│   │   │   └── readers.py               # docx / xlsx / pptx / pdf
│   │   │
│   │   └── social/
│   │       ├── __init__.py
│   │       └── whatsapp.py              # WhatsApp Web via Playwright
│   │
│   └── interfaces/                      # USER-FACING SURFACES
│       ├── cli/
│       │   ├── __init__.py
│       │   ├── interface.py             # Rich terminal chat
│       │   └── commands.py              # /clear /model /mode /memory /tools /status /help
│       │
│       ├── web/
│       │   ├── __init__.py
│       │   ├── app.py                   # FastAPI app
│       │   ├── websocket.py             # WebSocket handler
│       │   ├── routes/
│       │   ├── static/
│       │   └── templates/
│       │       └── index.html
│       │
│       ├── telegram/
│       │   ├── __init__.py
│       │   ├── bot.py
│       │   ├── handlers.py
│       │   └── commands.py
│       │
│       ├── gui/
│       │   ├── __init__.py
│       │   └── main_window.py           # PyQt6 desktop app
│       │
│       └── voice/
│           ├── __init__.py
│           ├── wake_word.py             # openWakeWord listener
│           └── voice_interface.py       # Full pipeline: wake → STT → LLM → TTS
│
├── tests/
│   ├── test_llm.py
│   ├── test_memory.py
│   ├── test_tools.py
│   ├── test_runtime.py
│   ├── test_decision.py
│   ├── test_voice.py
│   └── test_e2e.py
│
├── scripts/
│   ├── install.sh                       # Linux/WSL setup
│   └── install.ps1                      # Windows setup
│
├── data/                                # Runtime data (gitignored)
│   ├── profiles/                        # User profiles (JSON)
│   ├── sessions/                        # Browser sessions (JSON)
│   ├── downloads/
│   ├── screenshots/
│   ├── chroma/                          # ChromaDB vector store
│   └── jarvis.db                        # SQLite database
│
├── logs/                                # Rotating logs (gitignored)
│   ├── jarvis.log
│   ├── decisions.log
│   ├── tools.log
│   └── models.log
│
├── .env                                 # API keys (gitignored)
├── .env.example                         # Template (committed)
├── .gitignore
├── requirements.txt
├── README.md
└── TASKS.md
```

---

## Layer Responsibility Summary

| Layer | Single Responsibility |
|---|---|
| `core/runtime/` | Drives the loop. Owns turn lifecycle. |
| `core/orchestrator/` | Routes classified intent to the right handler. |
| `core/agents/` | Multi-step thinking and planning. |
| `core/tools/` | Infrastructure for discovering, validating, running tools. |
| `core/memory/` | Persistence across turns and sessions. |
| `core/context/` | Current-turn input staging. Cleared every turn. |
| `core/identity/` | Who Jarvis is + who the user is + prompt assembly. |
| `core/safety/` | Classify actions. Block or confirm dangerous ones. |
| `models/` | Thin wrappers around AI models. Called by runtime. |
| `skills/` | Concrete tool implementations. Registered in tools/registry. |
| `interfaces/` | User-facing surfaces. Convert I/O to runtime calls. |
