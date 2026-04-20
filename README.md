<div align="center">

# 🤖 JARVIS
### Local AI Assistant — Arabic + English — Free, Unlimited, Private

![Version](https://img.shields.io/badge/version-0.4.0--alpha-blue)
![Python](https://img.shields.io/badge/python-3.10+-green)
![License](https://img.shields.io/badge/license-MIT-orange)
![Platform](https://img.shields.io/badge/platform-Windows%2011-lightblue)
![Arabic](https://img.shields.io/badge/language-Arabic%20%2B%20English-red)

**A local AI assistant that understands Arabic and English, controls your computer, calls APIs, and thinks in multiple steps — all on your machine, no cloud.**

</div>

---

## What Jarvis Does

You give Jarvis a command — in Arabic or English — and it figures out what to do:

```
"افتح Chrome وابحث عن أحدث أخبار الذكاء الاصطناعي"
→ Jarvis opens Chrome, navigates to a search, returns a summary

"Send an email to Ahmed and add a calendar reminder for Friday"
→ Jarvis calls Gmail + Google Calendar in sequence
```

Everything runs **locally on your machine**. No API subscriptions. No token limits.

---

## Hardware This Runs On

| Component | Spec |
|-----------|------|
| CPU | Intel i5-12450HX |
| RAM | 16 GB |
| GPU | RTX 3050 — 6 GB VRAM |
| OS | Windows 11 |

**VRAM rule:** One large model at a time. Jarvis swaps automatically.

```
qwen3:8b         → 5.0 GB  (main brain, Arabic+EN, reasoning)
qwen2.5-coder:7b → 4.7 GB  (code tasks)
gemma3:4b        → 3.0 GB  (fast replies, simple questions)
llava:7b         → 4.5 GB  (image understanding)
SD 1.5 float16   → 4.0 GB  (image generation, unload LLM first)
```

---

## How the System Works

### The Single Flow

Every user input follows exactly one path:

```
User Input
    ↓
Context Assembly       ← combine: message + session history + relevant memory
    ↓
Decision              ← classify: what type of task? which model? need tools?
    ↓
Think (LLM Call)      ← selected model generates: answer or tool calls
    ↓
Act (Tool Execution)  ← run tools with validated args; results feed back
    ↓
Evaluate              ← is the answer good enough? retry or finish?
    ↓
Output                ← stream to interface + save to memory
```

That's it. Every feature in Jarvis is an expansion of one of these steps — not a new parallel system.

---

## Layer Definitions (No Overlap)

These are the **only** layers in Jarvis. Each has exactly one job.

### `src/models/` — Model Wrappers
**What:** Python wrappers around AI models. Nothing more.
**Responsibility:** Send input, get output, handle connection errors.
- `llm/` — Ollama text models (qwen3, gemma3, coder)
- `vision/` — LLaVA image understanding
- `speech/` — Whisper STT + Piper TTS
- `diffusion/` — Stable Diffusion image generation

**Does NOT:** make decisions, read memory, or know about tools.

---

### `src/core/context/` — Current Turn Input
**What:** Everything that happened in the **current turn** before the LLM is called.
**Responsibility:** Collect and normalize this turn's inputs: the user message, attached files, images, audio transcripts, and results from the last tool call.

**Does NOT:** store anything across turns (that's Memory). Does NOT decide anything (that's Decision).

```python
Context = {
    "user_message": str,
    "attachments": [File | Image | Audio],
    "tool_results": [ToolResult],
    "memory_snippets": [str],   # injected from Memory layer
}
```

---

### `src/core/memory/` — Cross-Session Persistence
**What:** Data that survives across conversations.
**Responsibility:** Store and retrieve facts, conversation history, user preferences.
- Short-term: Redis (current session messages, trimmed to token budget)
- Long-term: ChromaDB (semantic search over past facts and summaries)
- Structured: SQLite (conversations, tasks, feedback scores)

**Does NOT:** participate in routing or decision-making. Provides snippets to Context when asked.

---

### `src/core/decision/` — Routing Only
**What:** Classifies the current turn and decides what resources to use.
**Responsibility:** Given the assembled Context, output a routing decision.

```python
DecisionOutput = {
    "intent": "chat | code | tool_use | research | vision | voice",
    "complexity": "low | medium | high",
    "mode": "fast | normal | deep | planning",
    "model": "gemma3:4b | qwen3:8b | qwen2.5-coder:7b | llava:7b",
    "requires_tools": bool,
    "requires_planning": bool,
}
```

**Does NOT:** think, plan, or execute anything. Pure classification and resource selection.

---

### `src/core/agents/` — Thinking and Planning
**What:** Multi-step reasoning and task decomposition.
**Responsibility:** When a task is too complex for a single LLM call, agents break it into steps and sequence them.
- `planner.py` — break goal into ordered steps
- `thinker.py` — extended chain-of-thought reasoning
- `researcher.py` — multi-source web research
- `computer_use.py` — autonomous screen + app control loop

**Does NOT:** route requests (that's Decision) or execute tools directly (that's the Executor).

---

### `src/core/tools/` — Tool Registry and Execution
**What:** The system that manages all callable tools.
**Responsibility:**
- `registry.py` — discover and register all tools from `src/skills/`
- `validator.py` — validate tool args against JSON Schema before execution
- `executor.py` — run the tool, catch errors, return structured result
- `safety.py` — classify operations as safe / risky / critical; block or prompt for confirmation

**Does NOT:** decide which tool to use (that comes from the LLM's output). Does NOT implement tool logic (that's `src/skills/`).

---

### `src/skills/` — Tool Implementations
**What:** The actual code that does things in the world.
**Responsibility:** Each skill is one tool. It receives validated args, does one thing, returns a result.

```
src/skills/
  files/        — read, write, search, delete files
  system/       — processes, volume, startup items, apps
  browser/      — Playwright navigation, click, fill, download
  search/       — DuckDuckGo web search
  social/       — WhatsApp Web
  api/          — Google Calendar, Gmail, Drive, Contacts, YouTube
  pdf/          — PDF text + table extraction
  office/       — Word, Excel, PowerPoint read/write
  screen/       — screenshot, OCR
  notify/       — Windows Toast notifications
  coder/        — Python + shell code execution
```

**Does NOT:** make decisions, manage routing, or store memory.

---

### `src/core/runtime/` — Execution Loop
**What:** The engine that drives the Context → Decision → Think → Act → Evaluate cycle.
**Responsibility:** Run one user turn end-to-end. Manage iterations, timeouts, escalation, and model swaps.

**Does NOT:** implement any intelligence — it calls Decision, then models, then tools, in the correct order.

---

### `src/interfaces/` — User Interfaces
**What:** How the user talks to Jarvis.
**Responsibility:** Receive input from user, pass to runtime, display output.
- `cli/` — terminal chat (Rich)
- `web/` — FastAPI + WebSocket browser chat
- `voice/` — wake word + STT + TTS pipeline
- `telegram/` — Telegram bot
- `gui/` — PyQt6 desktop app

**Does NOT:** contain any logic beyond input/output formatting.

---

## Identity

Jarvis is one system with one identity, regardless of which model is handling the current request.

```python
# config/jarvis_identity.yaml defines:
name: "Jarvis"
role: "Personal AI assistant"
# Every LLM call receives this framing + user profile + task context
# No model is a standalone product — all are components of one system
```

User profile (language preference, technical level, recurring tasks) is stored in Memory and injected into every prompt via the Identity layer.

---

## Models

| Model | Role | VRAM |
|-------|------|------|
| `qwen3:8b` | Main brain: Arabic+EN conversation, reasoning, planning | ~5.0 GB |
| `gemma3:4b` | Fast responses, simple questions, classification | ~3.0 GB |
| `qwen2.5-coder:7b` | Code generation, debugging, shell commands | ~4.7 GB |
| `llava:7b` | Image understanding, OCR, screen description | ~4.5 GB |

The Decision layer selects the model. The router validates VRAM availability and swaps if needed.

---

## Quick Start

```powershell
# 1. Install Ollama + pull models
winget install Ollama.Ollama
ollama pull qwen3:8b
ollama pull qwen2.5-coder:7b
ollama pull gemma3:4b
ollama pull llava:7b

# 2. Clone and install
git clone <repo>
cd jarvis
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install chromium

# 3. Configure
copy config\settings.example.yaml config\settings.yaml
copy .env.example .env
# Edit .env: add TELEGRAM_BOT_TOKEN, GOOGLE_CLIENT_ID, etc.

# 4. Run
python app/main.py --interface cli
```

---

## Project Structure

```
jarvis/
├── app/
│   └── main.py              ← entry point: --interface [cli|web|telegram|gui|voice|all]
├── config/
│   ├── settings.yaml        ← all runtime config (YAML, no code)
│   ├── models.yaml          ← model capability profiles + routing weights
│   ├── skills.yaml          ← tool registry manifest
│   ├── jarvis_identity.yaml ← who Jarvis is
│   └── schemas/             ← JSON Schema per tool (validated before execution)
├── src/
│   ├── core/
│   │   ├── context/         ← assemble current-turn input bundle
│   │   ├── decision/        ← classify intent, select model + tools
│   │   ├── runtime/         ← drive the Think → Act → Evaluate loop
│   │   ├── agents/          ← planner, thinker, researcher, computer_use
│   │   ├── memory/          ← short-term, long-term, user profile
│   │   ├── tools/           ← registry, validator, executor, safety
│   │   └── identity/        ← system prompt builder, user profile injector
│   ├── models/
│   │   ├── llm/             ← Ollama wrapper (chat, generate, stream)
│   │   ├── vision/          ← LLaVA wrapper
│   │   ├── speech/          ← Whisper STT + Piper TTS
│   │   └── diffusion/       ← Stable Diffusion wrapper
│   ├── skills/              ← tool implementations (one file per tool)
│   │   ├── files/, system/, browser/, search/, social/
│   │   ├── api/, pdf/, office/, screen/, notify/, coder/
│   └── interfaces/
│       ├── cli/, web/, voice/, telegram/, gui/
├── data/                    ← runtime data (gitignored)
├── logs/                    ← log files (gitignored)
├── tests/
├── scripts/
│   ├── install.sh
│   └── install.ps1
├── requirements.txt
├── .env.example
└── TASKS.md
```

---

## Roadmap

| Phase | What Gets Built | Status |
|-------|----------------|--------|
| 0 | Vertical Slice: "Hey Jarvis, open Chrome" works end-to-end | ⏳ |
| 1 | Foundation: config, logging, skeleton, model wrappers | ⏳ |
| 2 | Runtime loop: Context → Decision → Think → Output (text only) | ⏳ |
| 3 | Memory: session history + cross-session semantic recall | ⏳ |
| 4 | CLI interface: rich terminal chat | ⏳ |
| 5 | Tool registry + executor + safety gate | ⏳ |
| 6 | System control skills: files, apps, clipboard, notifications | ⏳ |
| 7 | Browser skills: navigate, click, session persistence, WhatsApp | ⏳ |
| 8 | Google APIs: Calendar, Gmail, Drive, Contacts | ⏳ |
| 9 | Agents: planner, thinker, computer use loop | ⏳ |
| 10 | Task decomposition: DAG execution for complex goals | ⏳ |
| 11 | Feedback loop: outcomes update routing weights | ⏳ |
| 12 | Web UI + Voice + Vision (multimodal interfaces) | ⏳ |
| 13 | Telegram + GUI desktop | ⏳ |
| 14 | QA, optimization, security hardening | ⏳ |
| 15 | Personality layer (tone, style, adaptation) | ⏳ |

See [TASKS.md](./TASKS.md) for the detailed task list with success criteria.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| LLM | Ollama (local) |
| Web framework | FastAPI + Uvicorn |
| WebSocket | FastAPI WebSocket |
| Vector DB | ChromaDB |
| Cache | Redis |
| SQL | SQLite |
| STT | OpenAI Whisper (medium) |
| TTS | Piper TTS (Arabic + English) |
| Wake word | openWakeWord |
| Image gen | Diffusers — Stable Diffusion 1.5 |
| Browser | Playwright (Chromium) |
| Terminal UI | Rich |
| Desktop GUI | PyQt6 |
| Telegram | python-telegram-bot |
| Google APIs | google-api-python-client |
| Config | PyYAML + python-dotenv + Pydantic |
| Logging | Loguru |
| Windows APIs | pywin32, pycaw, pystray, winotify |
| Screen | mss + pytesseract |
| Clipboard | pyperclip + win32clipboard |
| Hotkeys | keyboard + pynput |

---

## License

MIT — free to use, modify, and distribute.
