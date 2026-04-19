# 🤖 JARVIS

**Personal AI Assistant — Local, Free, Unlimited**

[![Version](https://img.shields.io/badge/version-0.4.0--alpha-blue)](.)
[![Python](https://img.shields.io/badge/python-3.10+-green)](.)
[![Platform](https://img.shields.io/badge/platform-Windows%2011-lightblue)](.)
[![Status](https://img.shields.io/badge/status-in--development-yellow)](.)

> Jarvis is a fully local AI assistant that runs on consumer hardware. It accepts text, voice, and files — understands Arabic and English — and can control your computer, browser, files, and external services.

---

## ⚡ How It Works (The Simple Version)

Every user request follows this exact path:

```
User Input
    │
    ▼
Context  ──→  captures current turn inputs (text, files, images)
    │
    ▼
Runtime  ──→  drives the loop: Observe → Decide → Act → Evaluate
    │
    ▼
Orchestrator  ──→  routes to the right agent or tool
    │
    ├──→  Agent  ──→  thinks and plans multi-step tasks
    │
    └──→  Tool   ──→  executes a concrete action
    │
    ▼
Output  ──→  streamed back to the user
```

That's the entire system. Every layer below serves this flow.

---

## 🏗️ Architecture

### Layers (no overlap between them)

```
┌──────────────────────────────────────────────────────┐
│                    INTERFACES                        │
│         CLI │ Web │ GUI │ Telegram │ Voice           │
└─────────────────────┬────────────────────────────────┘
                      │ raw input
┌─────────────────────▼────────────────────────────────┐
│                    CONTEXT                           │
│      Captures current-turn inputs before execution   │
│           text │ files │ images │ audio              │
└─────────────────────┬────────────────────────────────┘
                      │ merged snapshot
┌─────────────────────▼────────────────────────────────┐
│                    RUNTIME                           │
│     Observe → Decide → Act → Evaluate → Finish       │
│              (or Escalate and repeat)                │
└──────┬──────────────┬───────────────────────────────┘
       │              │
       ▼              ▼
┌──────────┐  ┌───────────────────────────────────────┐
│  MEMORY  │  │             ORCHESTRATOR               │
│          │  │  Routes: Agent selector │ Tool router  │
│ Short:   │  └──────────────┬────────────────────────┘
│  session │                 │
│ Long:    │        ┌────────┴────────┐
│  semantic│        ▼                 ▼
└──────────┘   ┌─────────┐    ┌─────────────┐
               │  AGENTS │    │    TOOLS    │
               │ Planner │    │  Registry   │
               │ Thinker │    │  Validator  │
               │Research │    │  Executor   │
               └────┬────┘    └──────┬──────┘
                    │                │
               ┌────▼────────────────▼──────┐
               │           MODELS           │
               │  LLM │ Vision │ Speech │SD  │
               └────────────────────────────┘
```

### Layer Definitions (strict — no overlap)

| Layer | What it IS | What it is NOT |
|---|---|---|
| **Context** | Inputs of the **current turn only** — text, file paths, images staged before execution starts | Not memory. Not identity. Cleared after every turn. |
| **Memory** | Persistent data across turns and sessions — short-term (last N messages) + long-term (semantic facts in ChromaDB) | Not context. Memory persists; context does not. |
| **Identity** | Who Jarvis is (system profile) + who the user is (user profile). Injected into every model prompt. | Not a UI concept. Not stored in context or memory directly. |
| **Runtime** | The execution loop — drives Observe → Decide → Act → Evaluate. Owns turn lifecycle and iteration limits. | Not a model. Not a router. Does not contain business logic. |
| **Orchestrator** | Routes a classified intent to the right agent or tool. Contains dispatcher + agent selector + tool router. | Not a loop. Does not evaluate quality. Does not store state. |
| **Agents** | Thinking and planning logic — planner decomposes tasks, thinker reasons step by step, researcher queries multiple sources. | Not tools. Agents call tools but are not tools themselves. |
| **Tools** | Callable capabilities with a name, schema, and `execute()` — file ops, browser, APIs, code runner. | Not agents. Tools are stateless, single-action. |
| **Models** | AI model wrappers — LLM (Ollama), Vision (LLaVA), Speech (Whisper/Piper), Diffusion (SD). | Not the brain. Models are called BY the runtime, not in control of it. |

---

## ✅ Minimal Working System (Build This First)

Before any complexity is added, this path must work end-to-end:

```
"open Chrome"
      │
      ▼
Context: [text: "open Chrome"]
      │
      ▼
Runtime → Observe (read context)
        → Decide  (intent: action, complexity: low, requires_tool: true)
        → Act     (orchestrator → tool router → app_launcher.execute())
        → Evaluate (Chrome opened? yes → Finish)
      │
      ▼
Output: "Chrome is now open."
```

This is Phase 2 in TASKS.md. Everything else is built on top of this.

---

## 🧩 Project Structure

```
jarvis/
├── app/
│   └── main.py                  # Entry point: --interface cli|web|telegram|gui|all
│
├── config/
│   ├── settings.yaml            # All tunable parameters — no magic constants in Python
│   ├── models.yaml              # Model capability profiles + routing weights
│   ├── identity.yaml            # Jarvis system identity definition
│   └── schemas/                 # JSON Schemas for all tool input/output contracts
│       ├── system/
│       ├── browser/
│       ├── api/
│       └── ...
│
├── src/
│   ├── core/
│   │   ├── runtime/             # Loop driver: observe, decide, act, evaluate, escalate
│   │   │   ├── loop.py
│   │   │   ├── state.py
│   │   │   └── evaluate.py
│   │   │
│   │   ├── orchestrator/        # Routing: intent → agent or tool
│   │   │   ├── dispatcher.py
│   │   │   ├── agent_selector.py
│   │   │   └── tool_router.py
│   │   │
│   │   ├── agents/              # Thinking and planning
│   │   │   ├── planner.py       # Decomposes multi-step tasks
│   │   │   ├── thinker.py       # Chain-of-thought reasoning
│   │   │   └── researcher.py    # Multi-source research
│   │   │
│   │   ├── tools/               # Tool infrastructure (not implementations)
│   │   │   ├── registry.py      # Discovery + registration
│   │   │   ├── validator.py     # Schema enforcement before execution
│   │   │   └── executor.py      # Runs tools, wraps results, handles errors
│   │   │
│   │   ├── memory/              # Persistence across turns
│   │   │   ├── short_term.py    # Session history (Redis or in-memory)
│   │   │   ├── long_term.py     # Semantic memory (ChromaDB)
│   │   │   ├── database.py      # Structured storage (SQLite)
│   │   │   └── manager.py       # Unified interface to all memory backends
│   │   │
│   │   ├── context/             # Current-turn input staging
│   │   │   └── buffer.py        # Accumulates inputs; cleared after each turn
│   │   │
│   │   └── identity/            # Who Jarvis is + who the user is
│   │       ├── jarvis_profile.py
│   │       ├── user_profile.py
│   │       └── prompt_builder.py  # Assembles system prompt for every model call
│   │
│   ├── models/                  # AI model wrappers
│   │   ├── base/
│   │   │   ├── llm_base.py      # Abstract: chat(), generate(), tool_call()
│   │   │   ├── vision_base.py   # Abstract: describe(image, question)
│   │   │   └── speech_base.py   # Abstract: transcribe(), synthesize()
│   │   ├── llm/
│   │   │   ├── engine.py        # Ollama client
│   │   │   ├── router.py        # Dynamic model selector (reads config/models.yaml)
│   │   │   └── prompts.py       # Mode packs (fast/normal/deep/planning/research)
│   │   ├── vision/
│   │   │   └── llava.py
│   │   ├── speech/
│   │   │   ├── stt.py           # Whisper
│   │   │   └── tts.py           # Piper
│   │   └── diffusion/
│   │       └── sd.py            # Stable Diffusion 1.5
│   │
│   ├── skills/                  # Tool implementations (registered via tools/registry.py)
│   │   ├── base.py              # BaseTool abstract class
│   │   ├── system/              # app_launcher, file_ops, clipboard, notifications
│   │   ├── browser/             # playwright, session_manager, downloader
│   │   ├── search/              # web_search
│   │   ├── coder/               # code_executor
│   │   ├── screen/              # screenshot, ocr, screen_agent
│   │   ├── api/                 # google_auth, calendar, gmail, drive, contacts, youtube
│   │   ├── office/              # docx, xlsx, pptx readers
│   │   └── social/              # whatsapp
│   │
│   └── interfaces/              # User-facing surfaces
│       ├── cli/
│       ├── web/
│       ├── telegram/
│       ├── gui/
│       └── voice/
│
├── tests/
├── scripts/
│   ├── install.sh
│   └── install.ps1
├── data/                        # Runtime data (gitignored)
├── logs/                        # Rotating logs (gitignored)
├── .env                         # API keys and secrets (gitignored)
├── requirements.txt
├── README.md
└── TASKS.md
```

---

## 🤖 AI Models

**Hardware:** RTX 3050 (6 GB VRAM) — only **one heavy model loads at a time**.

| Model | Role | VRAM | When Used |
|---|---|---|---|
| `qwen3:8b` | Main reasoning, Arabic, deep/planning | ~5.0 GB | Default for complex tasks |
| `gemma3:4b` | Fast responses, classification | ~3.0 GB | Fast mode, simple questions |
| `qwen2.5-coder:7b` | Code synthesis and execution | ~4.7 GB | Code intent detected |
| `llava:7b` | Image understanding | ~4.5 GB | Image attached to message |
| Whisper medium | Speech-to-text (AR + EN) | CPU/CUDA | Voice input |
| Piper TTS | Text-to-speech Arabic | CPU | Voice output |
| Stable Diffusion 1.5 | Image generation | ~4.0 GB | Image generation requests |

**Routing rule:** The `models/llm/router.py` scores candidates from `config/models.yaml` capability profiles. No model is hardcoded to a task in Python — all weights are in config.

---

## 🖥️ Interfaces

| Interface | How to Run |
|---|---|
| CLI | `python app/main.py --interface cli` |
| Web UI | `python app/main.py --interface web` → http://localhost:8080 |
| Telegram Bot | `python app/main.py --interface telegram` |
| Desktop GUI | `python app/main.py --interface gui` |
| All | `python app/main.py --interface all` |

---

## 🚀 Quick Start

```bash
# 1. Install Ollama and pull models
winget install Ollama.Ollama
ollama pull qwen3:8b
ollama pull gemma3:4b
ollama pull qwen2.5-coder:7b
ollama pull llava:7b

# 2. Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1    # Windows
# source venv/bin/activate     # Linux/WSL

# 3. Install dependencies
pip install -r requirements.txt
playwright install chromium

# 4. Configure
copy config\settings.yaml.example config\settings.yaml
copy .env.example .env
# Edit .env with your API keys (optional — only needed for Google APIs)

# 5. Run
python app/main.py --interface cli
```

---

## ⚙️ Configuration

All tunable parameters are in `config/settings.yaml`. No magic constants in Python code.

```yaml
jarvis:
  name: "Jarvis"
  language: ["ar", "en"]
  wake_word: "hey_jarvis"

runtime:
  max_iterations: 5        # max loop iterations per user turn
  max_escalation_depth: 2  # max model escalations per turn
  tool_timeout_s: 30       # max seconds for a single tool execution

models:
  default: "qwen3:8b"
  fast: "gemma3:4b"
  code: "qwen2.5-coder:7b"
  vision: "llava:7b"

hardware:
  gpu_vram_limit_gb: 5.5
  max_concurrent_models: 1

interfaces:
  web:
    host: "127.0.0.1"
    port: 8080

paths:
  data: "data/"
  logs: "logs/"
  sessions: "data/sessions/"
  downloads: "data/downloads/"
```

---

## 🗺️ Roadmap

See [TASKS.md](./TASKS.md) for the full implementation checklist.

| Phase | Description | Status |
|---|---|---|
| 1 | Foundation — skeleton, config, logging | ⏳ In Progress |
| 2 | Minimal Working System — text → LLM → response | ⏳ Pending |
| 3 | Runtime — full loop with decision + evaluate | ⏳ Pending |
| 4 | Decision Layer — intent, complexity, routing | ⏳ Pending |
| 5 | Context Buffer — multimodal input staging | ⏳ Pending |
| 6 | Memory — short-term + long-term + user profile | ⏳ Pending |
| 7 | Tools — registry, validator, executor | ⏳ Pending |
| 8 | Agents — planner, thinker, researcher | ⏳ Pending |
| 9 | Skills — system, browser, APIs, office | ⏳ Pending |
| 10 | Safety — classification, confirmation gates | ⏳ Pending |
| 11 | Logging + Observability | ⏳ Pending |
| 12 | CLI Interface | ⏳ Pending |
| 13 | Web UI | ⏳ Pending |
| 14 | Voice Pipeline | ⏳ Pending |
| 15 | Telegram + GUI | ⏳ Pending |
| 16 | Optimization + QA | ⏳ Pending |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| LLM Runtime | Ollama |
| LLM Models | qwen3:8b, gemma3:4b, qwen2.5-coder:7b, llava:7b |
| STT | OpenAI Whisper (medium) |
| TTS | Piper TTS (Arabic: ar_JO-kareem) |
| Wake Word | openWakeWord |
| Image Gen | Stable Diffusion 1.5 (diffusers) |
| Vector Memory | ChromaDB + sentence-transformers |
| Session Memory | Redis (fallback: in-memory) |
| Structured DB | SQLite |
| Browser | Playwright (Chromium) |
| Web Framework | FastAPI + WebSocket |
| Terminal UI | Rich |
| Desktop GUI | PyQt6 |
| Telegram | python-telegram-bot |
| Config | PyYAML + pydantic-settings |
| Logging | Loguru |
| Google APIs | google-api-python-client |

---

## 📝 License

MIT — free to use, modify, and distribute.

---

*Built to run locally. No cloud. No API costs. No data leaves your machine.*
