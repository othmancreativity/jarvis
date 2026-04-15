<div align="center">

# 🤖 JARVIS
### Personal AI Assistant — Local, Free, Unlimited

![Version](https://img.shields.io/badge/version-0.1.0--alpha-blue)
![Python](https://img.shields.io/badge/python-3.10+-green)
![License](https://img.shields.io/badge/license-MIT-orange)
![Status](https://img.shields.io/badge/status-in--development-yellow)
![Arabic](https://img.shields.io/badge/language-Arabic%20%2B%20English-red)

**مساعد ذكاء اصطناعي شخصي يعمل محلياً بالكامل — مجاني — بلا حدود**

[Quick Start](#-quick-start) • [Features](#-features) • [Runtime System](#-runtime-system) • [Decision Layer](#-decision-layer) • [Signals](#-adaptive-intelligence-signals) • [Confidence](#-confidence-system) • [Cost](#-cost-awareness-system) • [Memory decisions](#-memory-aware-decision-making) • [Thinking Modes](#-thinking-modes) • [Dynamic Model Routing](#-dynamic-model-routing) • [Adaptive Intelligence](#-adaptive-intelligence-system) • [Evaluate & Escalate](#-runtime-evaluation--escalation) • [System Flow](#-system-flow) • [Architecture](#-architecture) • [Models](#-ai-models) • [Roadmap](#-roadmap)

</div>

---

## 🌟 Overview

Jarvis is a fully local, free, and unlimited personal AI assistant designed to run on consumer hardware. It supports Arabic and English natively, integrates multiple AI models for different tasks, and exposes multiple interfaces (CLI, Web, GUI, Telegram, Voice).

**Built for:**
- 🖥️ Local execution — no cloud, no API costs, no limits
- 🇸🇦 Arabic-first design with full English support  
- 🧠 **Adaptive routing** — models chosen from **capability profiles** + runtime signals (complexity, mode, latency, tools)—not a fixed task→model map
- 🔌 Multiple interfaces — one brain, many faces
- 🛠️ **Tool system** — capabilities exposed as callable tools (implemented under `skills/`); the LLM plans *which* tool to run with structured arguments

---

## 💻 Hardware Target

| Component | Spec |
|-----------|------|
| CPU | 12th Gen Intel Core i5-12450HX |
| RAM | 16 GB |
| GPU | NVIDIA RTX 3050 — 6 GB VRAM |
| Storage | 512 GB |
| OS | Windows 11 + WSL2 / Linux |

---

## ✨ Features

### Core Capabilities
- 💬 **Conversational AI** — Primary dialogue in Arabic + English via **Qwen2.5** (main “brain”)
- 🧠 **Deep Thinking** — Hard problems and fallback reasoning via **Qwen3** when depth beats speed  
- 📋 **Task Planning** — Multi-step plans coordinated by the **runtime loop** + agents
- 🔍 **Web Search** — Fast local search without API limits (as a **tool**)
- 💾 **Persistent Memory** — Short-term (Redis) + Long-term (ChromaDB) memory

### Multimodal
- 👁️ **Vision** — Image understanding and description (LLaVA / Qwen-VL)
- 🎨 **Image Generation** — Stable Diffusion 1.5 on local GPU
- 🎙️ **Speech-to-Text** — Whisper Medium (Arabic + English)
- 🔊 **Text-to-Speech** — Piper TTS with Arabic voice
- 👂 **Wake Word** — "Hey Jarvis" activation (openWakeWord)

### System Control
- 🖥️ **OS Control** — Files, processes, system settings
- 🌐 **Browser Automation** — Playwright-based web control
- 💻 **Code Execution** — Python + Shell sandbox
- 📅 **Google Calendar** — Create and read events
- 📺 **YouTube** — Search and control

### Interfaces
- 🖥️ **CLI** — Terminal interface with Rich formatting
- 🌐 **Web UI** — FastAPI + WebSocket real-time chat
- 🖼️ **GUI** — Desktop app (Tkinter/PyQt)
- 📱 **Telegram** — Full bot integration
- 🎤 **Voice** — Wake word + STT + TTS pipeline

---

## 🤖 AI Models

### Local Models (via Ollama)

**Physical constraint:** on a **6GB VRAM** GPU, only **one heavy Ollama model** should be resident at a time; the runtime coordinates swap/idle before loading another.

**Logical constraint:** **Selection is not static.** Each model has a **capability profile** (structured metadata). The **Decision Layer** + **dynamic router** score candidates against **intent, complexity, mode, latency budget, and tool/vision needs**—there is no single “if task X then always model Y” rule in the architecture.

| Model | Capability profile (summary) | Arabic | Reasoning | Speed | Typical use |
|-------|------------------------------|--------|-----------|-------|-------------|
| `qwen2.5:7b` | Strong **AR/EN** understanding; balanced reasoning; good default breadth | ⭐⭐⭐⭐⭐ | Medium–high | Fast | **Normal** dialogue, general assistance when complexity is low–medium |
| `qwen3:8b` | **Deep** reasoning; heavier; best when chains are long or ambiguity is high | ⭐⭐⭐⭐⭐ | **High** | Fast (heavier) | **Deep** mode, escalation, replanning after low confidence |
| `gemma3:4b` | **Very fast**; weaker long-horizon reasoning; great for tight latency | ⭐⭐⭐⭐ | Lower | **Fastest** | **Fast** mode, classification, cheap pre-checks |
| `qwen2.5-coder:7b` | **Code** synthesis/analysis; tool-friendly execution workflows | ⭐⭐⭐ | Medium (code) | Very Fast | **Code** intent, execution/analysis, structured patches |
| `llava:7b` | **Vision** + image-grounded QA (not text-only strengths) | ⭐⭐⭐ | N/A (vision) | Medium | When **pixels** are present or screen understanding is required |

*Profiles are data—e.g. YAML/JSON alongside `config/models.yaml`—so weights and thresholds can evolve without code forks.*

### Specialized Models

| Model | Purpose | Runtime |
|-------|---------|---------|
| Whisper Medium | Speech-to-Text (AR+EN) | CPU/CUDA |
| Piper TTS | Text-to-Speech Arabic | CPU |
| Stable Diffusion 1.5 | Image Generation | CUDA (6GB) |
| openWakeWord | Wake word detection | CPU |
| ChromaDB + sentence-transformers | Semantic memory | CPU |

### ⚠️ VRAM Strategy (6GB RTX 3050)

> **Rule:** Never load more than **one** large Ollama model at a time. Queue or serialize vision / chat / code requests if needed.  
> Diffusion (SD) competes for the same GPU — unload LLM/vision before image generation.

```
Default chat:     qwen2.5:7b       (~4–5 GB VRAM — primary brain)
Code / tools:     qwen2.5-coder:7b (~4–5 GB VRAM)
Fast / light:     gemma3:4b        (~3.0 GB VRAM)
Deep reasoning:   qwen3:8b         (~5.0 GB VRAM — use when depth required)
Vision:           llava:7b         (~4.5 GB VRAM)
Image gen:        SD 1.5           (~4.0 GB VRAM float16)
```

---

## ⚙️ Runtime System

Jarvis behaves as an **autonomous loop**, not a one-shot request/response handler. The **runtime** owns session lifecycle, iteration limits, and recovery when tools or models fail.

| Component | Responsibility |
|-----------|------------------|
| **Runtime Manager** | Owns the run: starts/stops a “turn”, ties interfaces → brain → tools, enforces max steps/timeouts, coordinates **VRAM** with the model router |
| **State Management** | Holds **conversation state**, **run state** (step index, pending tool calls, last observation), and pointers into **memory** (short/long) for context assembly |
| **Execution Flow** | Drives **Observe → Decide → Think → Act → Evaluate → (Escalate \| Finish)** (see below) |

**Core loop (one logical “turn” may repeat internally):**

```
Observe → Decide → Think → Act → Evaluate → Escalate? → …
                                    └──────── Finish →
```

- **Observe** — User message, memory, tool results, vision/audio transcripts, system events, prior step outcomes.  
- **Decide** — **Decision Layer** produces `DecisionOutput` (intent, complexity, **mode**, tool/planning flags, **prior confidence**, **cost_estimate**, **model_preference = auto**). Injects **prompt templates**, **budgets**, and **memory-informed biases** into the run.  
- **Think** — LLM call **selected dynamically** (capability fit + cost/quality tradeoff + VRAM + mode + latency); may emit **structured tool calls** or a candidate answer.  
- **Act** — Tool executor runs tools with validated JSON-like args; results are **observations** for the next cycle.  
- **Evaluate** — Score **response quality** + **posterior confidence** (self-critique, consistency checks, task satisfaction heuristics, tool success). Decides **Finish** (return to user) vs **Escalate** (retry, deeper mode, different model, planning).  
- **Escalate / Finish** — If escalate: re-enter **Decide** with updated signals (failed attempt, low confidence, incomplete coverage)—subject to **max_iterations**, **max_escalation_depth**, **timeouts**. If finish: stream result and update memory.

**Lifecycle:** interface connects → runtime session created → loop runs per user turn → state persisted (memory) → optional shutdown/cleanup (unload models, flush logs).

**Failure handling:** retries with backoff for transient Ollama errors; tool errors returned as observations (not silent); **escalation** may increase depth or switch to a stronger profile; **fallback** may return a safe minimal answer if limits are hit—always bounded by iteration, escalation depth, and timeouts.

---

## 🔁 System Flow

1. **Input** arrives from any interface (CLI, Web, Voice, …).  
2. **Runtime Manager** builds context from **state** + **memory** (including **learned preferences** and **past outcomes** when available).  
3. **Decision Layer** classifies **intent**, estimates **complexity**, **prior confidence**, **`cost_estimate`** (tokens / latency / GPU load tier), sets **mode**, and sets flags for **tools** and **planning**.  
4. **Dynamic model router** scores **candidate models** using **capability profiles**, **cost vs quality** tradeoff, **mode**, **latency tolerance**, **VRAM policy**, and **modalities**—not a static task name.  
5. **LLM** runs with **mode-appropriate prompts**; may emit **tool calls** (name + structured arguments).  
6. **Tool executor** runs tools; outputs are **observations** (JSON-serializable).  
7. **Evaluate** computes **posterior confidence** and **quality** of the candidate answer (and tool outcomes).  
8. **Branch:** **Finish** if thresholds met; else **Escalate** (retry, deeper mode, stronger model, planning)—until caps or stop conditions.  
9. Loop continues until **final reply** or **limits** exceeded.  
10. **Response** streams back to the interface; **memory** is updated (including traces useful for future **memory-informed** decisions).

---

## 🧭 Decision Layer

Located under **`core/runtime/decision/`**, the Decision Layer is the **policy front-end** for the runtime: it does **not** call a model by name from a fixed table. It **estimates** what kind of turn this is and what resources it deserves.

**Responsibilities:**

| Concern | Role |
|--------|------|
| **Intent classification** | Map utterance + context to coarse intents (e.g. `chat`, `code`, `research`, `action`) using lightweight signals (embeddings, classifier, small model, or heuristic ensemble—implementation choice is open). |
| **Complexity estimation** | Infer `low` / `medium` / `high` from length, structure, ambiguity, dependencies, and prior failures. |
| **Time / effort estimation** | Predict expected steps, tool calls, or tokens; feeds **timeout** and **planning** triggers. |
| **Tool necessity detection** | `requires_tools` when external facts, filesystem, browser, or APIs are required—may combine with **retrieval** from memory. |
| **Planning trigger** | `requires_planning` when the task is multi-step or non-linear. |

**Decision output (conceptual contract):**

```json
{
  "intent": "chat | code | research | action",
  "complexity": "low | medium | high",
  "mode": "fast | normal | deep | planning | research",
  "requires_tools": true,
  "requires_planning": false,
  "confidence": 0.0,
  "cost_estimate": {
    "tokens": 0,
    "latency": "low | medium | high",
    "gpu_load": "low | medium | high"
  },
  "model_preference": "auto"
}
```

- **`confidence`** — **Prior** belief (0.0–1.0) about how hard/ambiguous the turn is *before* the main LLM call; refined **after** generation in the **Evaluate** stage.  
- **`cost_estimate`** — **Pre-execution** expectation of spend: rough **token** budget, expected **latency** tier, and **GPU load** tier (feeds **cheap-first** routing when quality allows).  
- **`model_preference: "auto"`** — **downstream** scoring picks the model; user overrides remain possible at the interface layer.

---

## 📡 Adaptive Intelligence Signals

The runtime combines **signals**—not single rules—to stay adaptive:

| Signal | Role |
|--------|------|
| **Complexity** | Drives mode, planning, and expected depth |
| **Confidence** | **Prior** in `DecisionOutput`; **posterior** after **Evaluate**; gates Finish vs Escalate |
| **Cost** | `cost_estimate` biases toward **cheaper** profiles when complexity is low and quality risk is acceptable |
| **Memory influence** | User prefs, recurring patterns, past failures/successes shift **priorities** and **escalation aggressiveness** |

Signals are **weighted** through config and learned counters over time, not hardcoded `if task X then Y`.

---

## ✅ Confidence System

**Before execution (prior confidence):** Estimated by the Decision Layer using lightweight analysis—e.g. ambiguity, missing info, contradiction with memory, need for tools, or a small “judge” pass. Stored in `DecisionOutput.confidence` as a **prior**.

**After response (posterior confidence):** Produced in **Evaluate** using task-appropriate checks—e.g. self-critique prompt, answer–question consistency, structured rubric for code, tool success/failure, length/complete coverage heuristics.

**Threshold bands (tunable):**

| Band | Typical behavior |
|------|------------------|
| **High** | **Finish** — return response to user (possibly with minor polish) |
| **Medium** | **Refine** — optional single retry with tighter instructions, or one extra tool round if `requires_tools` |
| **Low** | **Escalate** — deeper **mode**, **stronger** model profile, or **planning** / replanning |

Thresholds are **not** fixed floats in product logic forever—they live in config and may be **per-intent** or **per-user** via memory.

---

## 💰 Cost Awareness System

**Goal:** prefer **cheaper** (smaller/faster/lower-GPU) runs when **risk is low**; spend **budget** only when signals demand quality.

**Pre-action estimates (in `cost_estimate`):**

| Field | Meaning |
|-------|---------|
| **tokens** | Rough prompt+completion budget (from length, mode, planned tools) |
| **latency** | Expected wall-clock tier given model tier + mode |
| **gpu_load** | Expected VRAM/time pressure (incl. swaps) |

**Selection:** The router combines **fit score** (capability) with a **cost penalty** and a **quality need** derived from complexity + prior confidence + user stakes (from memory). **No static** “simple = always gemma”—if memory shows repeated failures on similar prompts, **cost penalty** relaxes automatically.

---

## 🧠 Memory-Aware Decision Making

**Extended inputs** to the Decision Layer (when memory exists):

- **User preferences** — language, verbosity, risk tolerance (from profile + prior turns)  
- **Repeated task patterns** — e.g. frequent **code** requests → slightly higher **code-profile** prior  
- **Previous failures** — tool errors, low posterior confidence on similar queries → **escalate earlier** or pre-select safer tools  
- **Successful strategies** — patterns that worked (e.g. “search then summarize”) → bias **planning** or tool order  

This is **feature injection**, not a static table: weights are configurable and can be **updated** from outcomes logged after **Evaluate**.

---

## 🎚️ Thinking Modes

**Modes are orthogonal to model IDs.** A mode defines **how the assistant should think**, not which weights file to load.

| Mode | Behavior | Prompt / decode knobs (illustrative) |
|------|----------|----------------------------------------|
| **fast** | Short answers, minimal deliberation | Low max tokens, tighter temperature, optional “answer in one paragraph” |
| **normal** | Balanced | Default settings; standard Jarvis persona |
| **deep** | Multi-step reasoning, self-check | Explicit CoT or verification instructions; higher token budget |
| **planning** | Decompose into steps before execution | Plan-first templates; may invoke planner agent |
| **research** | Multi-source, tool-heavy | Web/search tools; cite or summarize sources; longer context assembly |

**Same model, different modes:** e.g. `qwen2.5:7b` can run **fast** (brief) or **normal** (full) by swapping **system prompt fragments** and **sampling parameters**. **Deep** mode may still prefer **`qwen3:8b`** for capability reasons, but the **mode** remains a first-class dial the Decision Layer sets.

---

## 🔀 Dynamic Model Routing

The **router** consumes `DecisionOutput` (incl. **`confidence`** prior + **`cost_estimate`**) + **capability profiles** + **runtime signals** (VRAM headroom, queue depth, latency SLO, modality) + **memory-informed** priors when available.

**Scoring (conceptual):**

- Each candidate model receives a **fit score** minus a **cost penalty** derived from `cost_estimate` (tokens / latency / gpu_load tiers), adjusted by **quality need** (complexity + prior confidence + user stakes from memory).
- Alignment with **intent** (e.g. code bias toward coder), **complexity** vs **reasoning ceiling**, **mode** (deep → higher reasoning weight), **vision** (pixels → `llava` mandatory).
- **No single hard rule** like “code ⇒ always coder”; if complexity is low and cost_estimate is tight, a **lighter** profile can win unless execution or risk signals outweigh savings.
- **VRAM** acts as a **constraint**, not a route: if the best-scoring model is loaded, keep it; otherwise **swap** per the single-GPU policy.

**Examples of signals (not fixed code):**

- High complexity + deep mode → raise `qwen3` weight.  
- Low complexity + fast mode → raise `gemma3` weight.  
- Code + execution/analysis → raise `qwen2.5-coder` weight.  
- Image present → **vision** model segment; text may be fused in a follow-up pass.

---

## 🎯 Adaptive Intelligence System

Umbrella for **auto-escalation**, **limits**, and **safe fallback**—so the assistant feels **self-correcting** rather than brittle. Detailed signal design lives in **[Adaptive Intelligence Signals](#-adaptive-intelligence-signals)**, **[Confidence System](#-confidence-system)**, **[Cost Awareness](#-cost-awareness-system)**, **[Memory-Aware Decision Making](#-memory-aware-decision-making)**, and **[Runtime Evaluation & Escalation](#-runtime-evaluation--escalation)** above.

**Auto-escalation triggers (examples):**

| Signal | Response |
|--------|----------|
| Low **confidence** (self-verification, consistency checks, or critic pass) | Increase **mode** depth or switch to a **stronger** profile |
| Multi-step or **incomplete** answer | Enable **planning** or add **tool** round |
| Tool failure / empty retrieval | **Retry** with different tool args or **replan** with deeper reasoning |
| User stress patterns (repeated reformulation) | Escalate without asking |

**Limits & control (always configured, never unbounded):**

| Limit | Purpose |
|-------|---------|
| **max_iterations** | Cap Observe→… cycles per user turn |
| **max_escalation_depth** | Cap nested escalations (e.g. fast→normal→deep) |
| **max_tool_rounds** | Prevent tool spam |
| **timeouts** | Per-turn, per-tool, per-model load |
| **fallback** | If limits hit: concise safe summary, offer to continue in a new turn, or degrade gracefully |

---

## 🔄 Runtime Evaluation & Escalation

**Evaluate stage** (after **Think** / **Act**): computes **quality** and **posterior confidence**; compares to **thresholds**; checks **task satisfaction** (answered the question? tools succeeded?).

**Escalation triggers (non-exhaustive):**

| Condition | Typical action |
|-----------|----------------|
| Posterior **low** | Deeper mode or stronger model |
| **Repeated failure** (same turn) | Switch model or switch strategy |
| **Incomplete** answer | Enable **planning** or add tool round |
| **Tool failure** | Retry with revised args, alternate tool, or fallback narrative |

**Retry logic:** bounded retries with **backoff**; each retry **re-enters Decide** with updated observations (not silent loops).

**Stop conditions:** **Finish** when high confidence **or** acceptable medium with no improvement signal; **abort** to **fallback** when **max_iterations** (e.g. **5**), **max_escalation_depth** (e.g. **2**), or **step timeouts** hit.

**Example limits (defaults are illustrative; configure in YAML):**

| Limit | Example |
|-------|---------|
| max_iterations | 5 per user turn |
| max_escalation_depth | 2 |
| timeout | per Decide / Think / Act / Evaluate step |
| fallback | short safe answer + “what failed” + optional new turn |

---

## 🔧 Tool System

Capabilities live in the `skills/` tree but are conceptually a **tool system**:

- Each capability is a **callable tool** with a stable **name**, **description** (for the LLM), and **input/output schema** (JSON-like).  
- The **tool registry** lists enabled tools and their schemas.  
- The **LLM** (via tool-calling or structured output) chooses **which** tool and **with what arguments**.  
- The **runtime executor** validates args, runs the tool, and returns a **normalized result** to the loop.

This separates *policy* (what the model wants) from *mechanism* (how tools run safely).

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
│   Runtime Manager → Loop (Observe→Decide→Think→Act→Evaluate)│
│   decision/ → State → Tool Executor                │
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

### Runtime loop (high level)

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

### Tool execution flow

```
LLM proposes tool call (name + args)
        │
        ▼
Schema validate + policy check (permissions, sandbox)
        │
        ▼
Executor runs tool implementation (under skills/)
        │
        ▼
Normalized result → State + next Observe
```

---

## 📁 Project Structure

Layout (no nested `jarvis/` Python package—repo root is the project):

```
(project root)/
├── 📄 README.md, TASKS.md, requirements.txt, pyproject.toml
├── 📁 settings/              ← Python app settings (YAML loader, Pydantic, paths, logging, chat route types)
│   ├── app_settings.py       ← AppSettings + blocks (mirrors config/settings.yaml)
│   ├── loader.py             ← load_settings() + .env
│   ├── paths.py              ← PROJECT_ROOT, config_dir, logs_dir
│   ├── logging.py            ← Loguru setup
│   └── chat_types.py         ← Decision / RouteKind for API/UI
├── 📁 app/                   ← Entry points (main, cli, server, __main__)
├── 📁 config/                ← YAML + JSON Schemas (not Python)
│   ├── settings.yaml        ← Main app config (copy from settings.example.yaml)
│   ├── models.yaml          ← Per-model capability profiles + routing weights
│   ├── skills.yaml          ← Tool registry + schema paths
│   ├── schemas/             ← JSON Schema for tools (api/, coder/, control/, …)
│   └── .env                 ← Secrets (gitignored; copy from .env.example)
├── 📁 core/                  ← Brain + runtime
│   ├── bootstrap.py         ← get_chat_service → orchestrator
│   ├── brain/               ← orchestrator, dispatcher
│   ├── runtime/             ← decision/, evaluate/, loop/, state/, executor/, …
│   ├── events/              ← EventBus
│   ├── agents/              ← planner/, thinker/, extensions/ (placeholder)
│   └── memory/              ← Phase 3
├── 📁 interfaces/            ← cli, web, telegram, gui, (voice later)
├── 📁 models/                ← llm/, speech/, vision/, diffusion/ (stubs where not built)
├── 📁 skills/                ← Tool implementations (Phase 5+)
├── 📁 tests/                 ← pytest (Phase 2 wiring + decision/router)
├── 📁 scripts/               ← install.sh
├── 📁 data/, 📁 logs/        ← Runtime data (gitignored except .gitkeep)
```

### Phase 1 & 2 (done)

| Area | What shipped |
|------|----------------|
| **Phase 1** | `config/*.yaml`, `.env.example`, `requirements.txt`, `app/main.py` interfaces, `scripts/install.sh`, `settings/` loaders, `core/agents/extensions` (replaces old “New folder”), `skills/` + `config/schemas/` skeleton |
| **Phase 2** | `models/llm/` engine + router + prompts + profiles; `core/runtime/` decision, evaluate, escalation, limits, memory hints stub; `core/brain/orchestrator` + dispatcher; `core/events/event_bus`; `core/bootstrap`; `tests/test_phase2_*.py` |

**Efficiency note:** Phase 1–2 reuse one **decision → score → stream** path for CLI/Web; heavy work is centralized in `core/brain/orchestrator.py` and `models/llm/`, so interfaces stay thin.

---

## 🚀 Quick Start

### Prerequisites
```powershell
# 1. Install Ollama
winget install Ollama.Ollama

# 2. Pull required models (roles: main / code / fast / deep / vision)
ollama pull qwen2.5:7b
ollama pull qwen2.5-coder:7b
ollama pull gemma3:4b
ollama pull qwen3:8b
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
  default_llm: "qwen2.5:7b"       # main conversational brain (AR + EN)
  code_llm: "qwen2.5-coder:7b"   # code + execution
  fast_llm: "gemma3:4b"           # lightweight / fast
  deep_llm: "qwen3:8b"            # deep reasoning + fallback
  vision_llm: "llava:7b"
  # Full capability profiles + routing weights live in models.yaml (see README)

hardware:
  gpu_vram_limit_gb: 5.5
  use_half_precision: true
```

---

## 🗺️ Roadmap

See [TASKS.md](./TASKS.md) for the full checklist (checkboxes updated as work completes).

| Phase | Description | Status |
|-------|-------------|--------|
| Phase 1 | Foundation + config + logging | ✅ Complete |
| Phase 2 | LLM + **runtime** + **decision layer** + dynamic router + evaluate/escalate loop | ✅ Complete |
| Phase 3 | Memory (short + long + structured) | ⏳ Pending |
| Phase 4 | CLI interface (rich UX, slash commands) | ⏳ Pending |
| Phase 5 | **Tool system** (registry, schemas, calling pipeline) | ⏳ Pending |
| Phase 6 | **Agents** — Planner/Thinker/ReAct | ⏳ Pending |
| Phase 7 | Web UI (templates/static) | ⏳ Pending |
| Phase 8 | Voice pipeline | ⏳ Pending |
| Phase 9 | Vision + image generation | ⏳ Pending |
| Phase 10 | Integrations (Telegram + GUI) | ⏳ Pending |
| Phase 11 | QA, optimization, security, polish | ⏳ Pending |

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
| Desktop GUI | Tkinter / PyQt6 |
| Telegram | python-telegram-bot |
| Config | PyYAML + python-dotenv |
| Logging | Loguru |
| Decision / routing | Policy layer (intent, complexity, mode) + capability-weighted model scoring |

---

## 📝 License

MIT License — Free to use, modify, and distribute.

---

<div align="center">
Built with ❤️ — Local AI, No Limits
</div>
