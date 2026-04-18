<div align="center">

# 🤖 JARVIS
### Personal AI Assistant — Local, Free, Unlimited

![Version](https://img.shields.io/badge/version-0.3.0--alpha-blue)
![Python](https://img.shields.io/badge/python-3.10+-green)
![License](https://img.shields.io/badge/license-MIT-orange)
![Status](https://img.shields.io/badge/status-in--development-yellow)
![Arabic](https://img.shields.io/badge/language-Arabic%20%2B%20English-red)
![Platform](https://img.shields.io/badge/platform-Windows%2011-lightblue)

**A fully local, privacy-first AI assistant with adaptive intelligence, multi-model routing, and autonomous reasoning — built for consumer hardware.**

[Quick Start](#-quick-start) • [Features](#-features) • [Architecture](#-architecture) • [Runtime System](#-runtime-system) • [Decision Layer](#-decision-layer) • [Confidence & Cost](#-confidence-system) • [Model Routing](#-dynamic-model-routing) • [Thinking Modes](#-thinking-modes) • [Evaluation & Escalation](#-runtime-evaluation--escalation) • [Models](#-ai-models) • [Configuration](#-configuration) • [Roadmap](#-roadmap)

</div>

---

## 🌟 Overview

Jarvis is a fully local, free, and unlimited personal AI assistant designed to run on consumer hardware. It supports Arabic and English natively, integrates multiple AI models for different tasks, and exposes multiple interfaces (CLI, Web, GUI, Telegram, Voice).

**Core principles:**
- 🖥️ **Local execution** — no cloud, no API costs, no data leaves your machine
- 🧠 **Adaptive routing** — models chosen from capability profiles + runtime signals (complexity, mode, latency, tools) — not a fixed task→model map
- 🔌 **Multiple interfaces** — one brain, many faces (CLI, Web, GUI, Telegram, Voice)
- 🛠️ **Tool system** — capabilities exposed as callable tools with structured I/O; the LLM plans which tool to run with validated arguments
- 🌍 **Multilingual** — Arabic-first design with full English support

---

## 💻 Hardware Target

| Component | Specification |
|-----------|--------------|
| CPU | 12th Gen Intel Core i5-12450HX |
| RAM | 16 GB |
| GPU | NVIDIA RTX 3050 — 6 GB VRAM |
| Storage | 512 GB |
| OS | Windows 11 + WSL2 / Linux |

---

## ✨ Features

### Core Capabilities
- 💬 **Conversational AI** — Dialogue in Arabic + English via adaptive model routing
- 🧠 **Deep Thinking** — Multi-tier reasoning modes (fast / normal / deep / planning / research)
- 📋 **Task Planning** — Multi-step plans coordinated by the runtime loop + agents
- 🔍 **Web Search** — Local search without API limits (as a callable tool)
- 💾 **Persistent Memory** — Short-term (Redis) + Long-term (ChromaDB) + Structured (SQLite)
- 🪪 **Identity System** — Consistent personality across all models via dynamic system prompt construction

### Multimodal
- 👁️ **Vision** — Image understanding and description (LLaVA)
- 🎨 **Image Generation** — Stable Diffusion 1.5 on local GPU
- 🎙️ **Speech-to-Text** — Whisper Medium (Arabic + English)
- 🔊 **Text-to-Speech** — Piper TTS with Arabic voice
- 👂 **Wake Word** — "Hey Jarvis" activation (openWakeWord)

### System Control
- 🖥️ **OS Control** — Files, processes, system settings, startup items, scheduled tasks
- 🚀 **App Launcher** — Open/close any Windows app by name (searches PATH, Start Menu, Program Files)
- 📋 **Clipboard** — Read, write, and monitor clipboard content
- 🔔 **Notifications** — Native Windows Toast alerts for task completion and reminders
- 🌐 **Browser Automation** — Full Playwright control: navigate, click, fill, download, upload, multi-tab
- 🔐 **Session Persistence** — Browser sessions saved between runs — stays logged in
- 💻 **Code Execution** — Python + Shell sandbox with timeout and structured output
- 🖼️ **Screen Capture** — Screenshots + lightweight OCR (no LLM needed for text reading)
- ⌨️ **Global Hotkeys** — System-wide shortcuts to activate Jarvis from any context

### External APIs
- 📅 **Google Calendar** — Read, create, update, delete events
- 📧 **Gmail** — Read, search, send, and reply to emails
- 📁 **Google Drive** — List, search, upload, download, and share files
- 👤 **Google Contacts** — Search and retrieve contact information
- 📺 **YouTube** — Search videos, get info, open in browser
- 💬 **WhatsApp Web** — Send messages and read conversations via browser automation

### Interfaces
- 🖥️ **CLI** — Terminal interface with Rich formatting
- 🌐 **Web UI** — FastAPI + WebSocket real-time chat with Glassmorphism design
- 🖼️ **GUI** — Desktop app (PyQt6)
- 📱 **Telegram** — Full bot integration
- 🎤 **Voice** — Wake word + STT + TTS pipeline

---

## 🤖 AI Models

### Local Models (via Ollama)

**Physical constraint:** On a 6 GB VRAM GPU, only **one heavy Ollama model** should be resident at a time; the runtime coordinates swap/idle before loading another.

**Logical constraint:** Selection is not static. Each model has a **capability profile** (structured metadata). The Decision Layer + dynamic router score candidates against intent, complexity, mode, latency budget, and tool/vision needs — there is no single "if task X then always model Y" rule.

| Model | Capability Profile | Reasoning | Speed | Typical Use |
|-------|-------------------|-----------|-------|-------------|
| `qwen3:8b` | Deep reasoning; best Arabic + EN; planning | **High** | Moderate | Main brain — deep mode, escalation, planning |
| `gemma3:4b` | Very fast; weaker long-horizon reasoning | Lower | **Fastest** | Fast mode, classification, quick answers |
| `qwen2.5-coder:7b` | Code synthesis/analysis; tool-friendly | Medium (code) | Very Fast | Code intent, execution, structured patches |
| `llava:7b` | Vision + image-grounded QA | N/A (vision) | Medium | When pixels are present |

> `qwen2.5:7b` removed — superseded by `qwen3:8b` in all capability profiles.

*Profiles are data (YAML in `config/models.yaml`) — weights and thresholds evolve without code forks.*

### Specialized Models

| Model | Purpose | Runtime |
|-------|---------|---------|
| Whisper Medium | Speech-to-Text (AR+EN) | CPU/CUDA |
| Piper TTS | Text-to-Speech Arabic | CPU |
| Stable Diffusion 1.5 | Image Generation | CUDA (6 GB) |
| openWakeWord | Wake word detection | CPU |
| ChromaDB + sentence-transformers | Semantic memory | CPU |

### VRAM Strategy (6 GB RTX 3050)

> **Rule:** Never load more than one large Ollama model at a time. Queue or serialize vision / chat / code requests if needed. Diffusion (SD) competes for the same GPU — unload LLM/vision before image generation.

```
Default/deep chat:  qwen3:8b         (~5.0 GB VRAM — primary brain)
Code / tools:       qwen2.5-coder:7b (~4.7 GB VRAM)
Fast / light:       gemma3:4b        (~3.0 GB VRAM)
Vision tasks:       llava:7b         (~4.5 GB VRAM)
Image gen:          SD 1.5           (~4.0 GB VRAM float16) — unload LLM first
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                   INTERFACES                        │
│   CLI  │  Web UI  │  GUI  │  Telegram  │  Voice    │
└─────────────────────┬───────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────┐
│                  app/main.py                        │
│              Entry Point + Router                   │
└─────────────────────┬───────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────┐
│               core/runtime/                         │
│  Runtime Manager → Loop (Observe→Decide→Think→Act→  │
│  Evaluate) → decision/ → State → Tool Executor     │
└─────────────────────┬───────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────┐
│                  core/brain/                        │
│   Orchestrator  ↔  Planner / Thinker  ↔  Memory   │
└──────┬──────────────┬──────────────┬────────────────┘
       │              │              │
┌──────▼──────┐ ┌─────▼──────┐ ┌────▼────────────────┐
│  models/    │ │  skills/   │ │  core/memory/       │
│  llm/       │ │  (tools)   │ │  Short: Redis       │
│  speech/    │ │  control/  │ │  Long:  ChromaDB    │
│  vision/    │ │  web/      │ │  Files: SQLite      │
│  diffusion/ │ │  search/   │ └─────────────────────┘
└─────────────┘ └────────────┘
```

### Runtime Loop

```
     ┌──────────┐
     │ Observe  │◄────────────────────────────────────────┐
     └────┬─────┘                                         │
          ▼                                               │
     ┌──────────┐     ┌──────────┐     ┌──────────┐     │
     │  Decide  │────►│  Think   │────►│    Act   │     │
     │ (policy) │     │  (LLM)   │     │ (tools)  │     │
     └──────────┘     └──────────┘     └────┬─────┘     │
                              ┌──────────────▼──────────┴─┐
                              │        Evaluate           │
                              │  (quality + confidence)   │
                              └────────────┬──────────────┘
                                           │
                               ┌──────────┴──────────┐
                               ▼                     ▼
                          ┌─────────┐          ┌──────────┐
                          │ Finish  │          │ Escalate │
                          └─────────┘          └────┬─────┘
                                                  │
                                                  └──► Decide…
```

---

## ⚙️ Runtime System

Jarvis behaves as an **autonomous loop**, not a one-shot request/response handler. The runtime owns session lifecycle, iteration limits, and recovery when tools or models fail.

| Component | Responsibility |
|-----------|----------------|
| **Runtime Manager** | Owns the run: starts/stops a turn, ties interfaces → brain → tools, enforces max steps/timeouts, coordinates VRAM with the model router |
| **State Management** | Holds conversation state, run state (step index, pending tool calls, last observation), and pointers into memory (short/long) for context assembly |
| **Execution Flow** | Drives **Observe → Decide → Think → Act → Evaluate → (Escalate \| Finish)** |

**Core loop (one logical turn may repeat internally):**

```
Observe → Decide → Think → Act → Evaluate → Escalate? → …
                                    └──────── Finish →
```

- **Observe** — User message, memory, tool results, vision/audio transcripts, system events, prior step outcomes.
- **Decide** — Decision Layer produces `DecisionOutput` (intent, complexity, mode, tool/planning flags, prior confidence, cost estimate, model preference = auto).
- **Think** — LLM call selected dynamically (capability fit + cost/quality tradeoff + VRAM + mode + latency); may emit structured tool calls or a candidate answer.
- **Act** — Tool executor runs tools with validated arguments; results are observations for the next cycle.
- **Evaluate** — Score response quality + posterior confidence. Decides Finish (return to user) vs Escalate (retry, deeper mode, different model, planning).
- **Escalate / Finish** — If escalate: re-enter Decide with updated signals — subject to max iterations, max escalation depth, and timeouts. If finish: stream result and update memory.

---

## 🧭 Decision Layer

Located under `core/runtime/decision/`, the Decision Layer is the policy front-end for the runtime. It estimates what kind of turn this is and what resources it deserves — it does not call a model by name from a fixed table.

**Decision output contract:**

```json
{
  "intent": "chat | code | research | action",
  "complexity": "low | medium | high",
  "mode": "fast | normal | deep | planning | research",
  "requires_tools": true,
  "requires_planning": false,
  "confidence": 0.72,
  "cost_estimate": {
    "tokens": 2048,
    "latency": "low | medium | high",
    "gpu_load": "low | medium | high"
  },
  "model_preference": "auto"
}
```

| Concern | Role |
|---------|------|
| **Intent classification** | Map utterance + context to coarse intents (`chat`, `code`, `research`, `action`) |
| **Complexity estimation** | Infer `low` / `medium` / `high` from length, structure, ambiguity, dependencies |
| **Time/effort estimation** | Predict expected steps, tool calls, or tokens; feeds timeout and planning triggers |
| **Tool necessity** | `requires_tools` when external facts, filesystem, browser, or APIs are required |
| **Planning trigger** | `requires_planning` when the task is multi-step or non-linear |

---

## ✅ Confidence System

**Before execution (prior):** Estimated by the Decision Layer using lightweight analysis — ambiguity, missing info, contradiction with memory. Stored in `DecisionOutput.confidence`.

**After response (posterior):** Produced in Evaluate using task-appropriate checks — self-critique, answer–question consistency, tool success/failure, coverage heuristics.

| Band | Behavior |
|------|----------|
| **High** | Finish — return response to user |
| **Medium** | Refine — optional single retry with tighter instructions |
| **Low** | Escalate — deeper mode, stronger model, or planning |

Thresholds are configurable per-intent and per-user via config and memory.

---

## 💰 Cost Awareness System

Prefer cheaper (smaller/faster/lower-GPU) runs when risk is low; spend budget only when signals demand quality.

| Field | Meaning |
|-------|---------|
| `tokens` | Rough prompt+completion budget |
| `latency` | Expected wall-clock tier |
| `gpu_load` | Expected VRAM/time pressure |

The router combines fit score with a cost penalty and a quality need derived from complexity + prior confidence + user stakes from memory.

---

## 🎚️ Thinking Modes

Modes are orthogonal to model IDs. A mode defines how the assistant should think, not which weights file to load.

| Mode | Behavior |
|------|----------|
| **fast** | Short answers, minimal deliberation |
| **normal** | Balanced depth and length |
| **deep** | Multi-step reasoning, self-check |
| **planning** | Decompose into steps before execution |
| **research** | Multi-source, tool-heavy, cite sources |

Same model, different modes — e.g. `qwen3:8b` can run fast or normal by swapping system prompt fragments and sampling parameters.

---

## 🔀 Dynamic Model Routing

The router consumes `DecisionOutput` + capability profiles + runtime signals (VRAM, queue depth, latency SLO, modality) + memory-informed priors.

**Scoring:** Each candidate model receives a fit score minus a cost penalty, adjusted by quality need. No single hard rule — signals are weighted through config and learned counters.

---

## 🔄 Runtime Evaluation & Escalation

**Evaluate stage:** computes quality and posterior confidence; compares to thresholds; checks task satisfaction.

| Condition | Typical Action |
|-----------|----------------|
| Posterior low | Deeper mode or stronger model |
| Repeated failure | Switch model or strategy |
| Incomplete answer | Enable planning or add tool round |
| Tool failure | Retry with revised args or alternate tool |

**Limits (configurable in YAML):**

| Limit | Default |
|-------|---------|
| max_iterations | 5 per user turn |
| max_escalation_depth | 2 |
| timeout | per Decide / Think / Act / Evaluate step |
| fallback | short safe answer + error context |

---

## 🔧 Tool System

Capabilities live in the `skills/` tree as a callable tool system:

- Each capability is a callable tool with a stable name, description, and input/output schema
- The tool registry lists enabled tools and their schemas
- The LLM (via tool-calling or structured output) chooses which tool and with what arguments
- The runtime executor validates args, runs the tool, and returns a normalized result

---

## 📁 Project Structure

```
(project root)/
├── 📄 README.md, TASKS.md, requirements.txt, pyproject.toml
├── 📁 settings/              ← Python app settings (YAML loader, Pydantic, paths, logging)
│   ├── app_settings.py       ← AppSettings + sub-blocks (mirrors config/settings.yaml)
│   ├── loader.py             ← load_settings() + .env
│   ├── paths.py              ← PROJECT_ROOT, config_dir, logs_dir
│   ├── logging.py            ← Loguru setup
│   └── chat_types.py         ← Decision / RouteKind for API/UI
├── 📁 app/                   ← Entry points (main, cli, server, __main__)
├── 📁 config/                ← YAML + JSON Schemas (not Python)
│   ├── settings.yaml         ← Main app config
│   ├── models.yaml           ← Per-model capability profiles + routing weights
│   ├── skills.yaml           ← Tool registry + schema paths
│   ├── jarvis_identity.yaml  ← Jarvis system identity definition
│   └── schemas/              ← JSON Schema for tools
├── 📁 core/                  ← Brain + runtime + memory + identity
│   ├── bootstrap.py          ← get_chat_service → orchestrator
│   ├── brain/                ← orchestrator, dispatcher
│   ├── runtime/              ← decision/, evaluate/, loop/, state/, executor/
│   ├── events/               ← EventBus
│   ├── agents/               ← planner/, thinker/, extensions/ (placeholder)
│   ├── memory/               ← short_term, long_term, database, manager, user_profile
│   ├── context/              ← Context buffer (multimodal input staging)
│   └── identity/             ← Jarvis profile, user profile, prompt builder, model awareness
├── 📁 interfaces/            ← cli/, web/, telegram/, gui/, voice/
├── 📁 models/                ← llm/, speech/, vision/, diffusion/
├── 📁 skills/                ← Tool implementations (Phase 5+)
├── 📁 tests/                 ← pytest suites per phase
├── 📁 scripts/               ← install.sh, install.ps1
├── 📁 data/, 📁 logs/        ← Runtime data (gitignored except .gitkeep)
```

### Implementation Status

| Area | What Shipped |
|------|-------------|
| **Phase 1** | `config/*.yaml`, `.env.example`, `requirements.txt`, `app/main.py` entry points, `scripts/install.sh` + `install.ps1`, `settings/` loaders, skeleton directories |
| **Phase 2** | `models/llm/` engine + router + prompts + profiles; `core/runtime/` decision, evaluate, escalation, limits; `core/brain/` orchestrator + dispatcher; `core/events/` event_bus; `core/bootstrap`; test suite phase 2 |
| **Phase 3** | `core/memory/` short-term + long-term + database + manager + user profiling; `core/context/` buffer system; `core/identity/` Jarvis profile + user identity + prompt builder + model awareness + system awareness |
| **Phases 4–16** | Roadmap — see TASKS.md |

---

## 🚀 Quick Start

### Prerequisites

```powershell
# 1. Install Ollama
winget install Ollama.Ollama

# 2. Pull required models (qwen2.5:7b removed — superseded by qwen3:8b)
ollama pull qwen3:8b
ollama pull qwen2.5-coder:7b
ollama pull gemma3:4b
ollama pull llava:7b

# 3. Install Python dependencies
pip install -r requirements.txt
```

### Run Jarvis

```powershell
# CLI mode
python app/main.py --interface cli

# Web UI mode
python app/main.py --interface web
# Then open: http://localhost:8080

# Telegram mode
python app/main.py --interface telegram

# All interfaces simultaneously
python app/main.py --interface all
```

---

## ⚙️ Configuration

Copy and edit the config files:

```powershell
copy config\settings.example.yaml config\settings.yaml
copy .env.example .env
```

Key settings in `config/settings.yaml`:

```yaml
jarvis:
  name: "Jarvis"
  language: ["ar", "en"]
  wake_word: "hey_jarvis"

models:
  default_llm: "qwen3:8b"
  code_llm: "qwen2.5-coder:7b"
  fast_llm: "gemma3:4b"
  vision_llm: "llava:7b"

hardware:
  gpu_vram_limit_gb: 5.5
  use_half_precision: true
```

---

## 🗺️ Roadmap

See [TASKS.md](./TASKS.md) for the full checklist with checkboxes updated as work completes.

| Phase | Description | Status |
|-------|-------------|--------|
| Phase 1 | Foundation — config, logging, project skeleton | ✅ Complete |
| Phase 2 | LLM + Runtime + Decision Layer + Dynamic Router | ✅ Complete |
| Phase 3 | Memory + Adaptive Memory + Context Buffer + Identity | ✅ Complete |
| Phase 4 | CLI Interface — Rich UX, slash commands, hotkeys | ⏳ Next |
| Phase 5 | Tool System — registry, schemas, calling pipeline | ⏳ Pending |
| Phase 6 | System Control — apps, files, clipboard, notifications, OCR | ⏳ Pending |
| Phase 7 | Browser & Web — Playwright + sessions + WhatsApp | ⏳ Pending |
| Phase 8 | External APIs — Gmail, Calendar, Drive, Contacts, YouTube | ⏳ Pending |
| Phase 9 | Agents — Planner / Thinker / ReAct / Computer Use | ⏳ Pending |
| Phase 10 | Task Decomposition Engine | ⏳ Pending |
| Phase 11 | Feedback & Learning | ⏳ Pending |
| Phase 12 | Web UI + Voice + Vision (multimodal surfaces) | ⏳ Pending |
| Phase 13 | Telegram Interface | ⏳ Pending |
| Phase 14 | GUI Desktop App + System Tray | ⏳ Pending |
| Phase 15 | QA + Optimization + Security | ⏳ Pending |
| Phase 16 | Personality Layer | ⏳ Pending |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| LLM Runtime | Ollama |
| Web Framework | FastAPI + Uvicorn |
| WebSocket | FastAPI WebSocket |
| Vector DB | ChromaDB |
| Cache | Redis |
| SQL DB | SQLite |
| STT | OpenAI Whisper |
| TTS | Piper TTS |
| Wake Word | openWakeWord |
| Image Gen | Diffusers (Stable Diffusion) |
| Browser | Playwright |
| Terminal UI | Rich |
| Desktop GUI | PyQt6 |
| Telegram | python-telegram-bot |
| Config | PyYAML + python-dotenv |
| Logging | Loguru |
| Decision / Routing | Policy layer + capability-weighted model scoring |
| Clipboard | pyperclip + win32clipboard |
| Global Hotkeys | pynput / keyboard |
| System Tray | pystray |
| Windows Notifications | winotify |
| Screen Capture | mss + Pillow |
| Lightweight OCR | pytesseract (Tesseract) |
| Gmail / Drive / Contacts | google-api-python-client |
| WhatsApp | Playwright (WhatsApp Web) |

---

## 📝 License

MIT License — Free to use, modify, and distribute.

---

<div align="center">
Built with precision — Local AI, No Limits
</div>
