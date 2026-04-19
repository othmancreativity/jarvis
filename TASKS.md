# 🗂️ JARVIS — Task Board
> Full development roadmap from zero to complete system
> Update checkboxes as you complete each task
> **Repo layout:** YAML + JSON Schemas under `config/`; Python packages under `src/` (`core/`, `models/`, `interfaces/`, `skills/`); entry points under `app/`; settings loader package under `settings/` (planned) — see [README.md](./README.md) (Project Structure).

---

## 🔗 System Integration Map (non-optional wiring)

Every system below is cross-cutting. These dependencies are **mandatory** — not optional optimizations:

- **Feedback & Learning** ↔ **Adaptive Memory** — implicit signals + explicit outcomes update user profile, tool/model priors, and "what worked" recall.
- **Adaptive Memory** ↔ **Decision Layer** — retrieved facts + profile bias intent, complexity, mode, and confidence priors.
- **Decision Layer** ↔ **Model Router** — `DecisionOutput` + memory context → model selection + mode packs; Error Intelligence can override (retry / switch model / switch mode).
- **Runtime loop** ↔ **Self-Evaluation** — Evaluate stage consumes structured signals; persistence enables resume and long-running tracking.
- **Task Decomposition** ↔ **Parallel execution** — execution graph schedules concurrent steps where dependencies allow; failures map to error class + selective retry.
- **Personality Layer** ↔ **prompts + memory** — tone/style constraints compose with mode packs and learned preferences (without breaking safety caps).
- **Context Buffer** ↔ **Runtime (Observe)** ↔ **Decision** ↔ **Tools** — interfaces enqueue text/files/images/audio into a staging layer; Observe reads a merged snapshot; Decision uses that as primary input; heavy models and tool-side readers run only after Decide (buffer is preparation-only).
- **Identity & Profiles** ↔ **Memory** ↔ **Decision** ↔ **Runtime** ↔ **Context Buffer** — user profile + Jarvis system identity feed Observe and Decision priors; system prompt builder ensures every model sees who Jarvis is, who the user is, and shared state — consistent behavior across all routed models.
- **Tool Registry** ↔ **Executor** ↔ **All Skills** — every skill is a registered tool; executor validates args, runs, and returns structured results; no skill bypasses the registry.
- **EventBus** ↔ **All Components** — all state transitions (wake word, tool start/end, escalation, decision, error) are events; components subscribe rather than call each other directly.
- **Config System** ↔ **Everything** — all tunable parameters (routing weights, VRAM limits, thresholds, hotkeys, paths) are YAML; no magic constants in Python.

> **Phase order rationale (dependency-driven):**
> - CLI first (Phase 4) = fastest feedback loop, no frontend complexity
> - Tool system (Phase 5) = prerequisite for everything — agents need tools, APIs need registry
> - System Control (Phase 6) + Browser (Phase 7) = core "computer use" skills, built on tool registry
> - External APIs (Phase 8) = depends on tool registry (Phase 5) + browser OAuth (Phase 7)
> - Agents (Phase 9) = need tools (5,6,7) and APIs (8) to be useful
> - Task Decomposition (Phase 10) = extends agents, needs agents first
> - Feedback (Phase 11) = closes the loop, needs agents + tools producing outcomes
> - Multimodal surfaces (Phase 12) = Web/Voice/Vision — highest UX value, built on top of everything
> - Telegram (Phase 13) + GUI (Phase 14) = extra interfaces, lower priority than core function
> - QA (Phase 15) = after feature-complete
> - Personality (Phase 16) = polish last, overlays everything

---

## 📊 Progress Overview

| Phase | Description | Tasks | Done | Progress |
|-------|-------------|-------|------|----------|
| Phase 1 | Foundation & Project Setup | 8 | 0 | ░░░░░░░░░░ 0% |
| Phase 2 | LLM Engine + Runtime + Decision Layer | 26 | 0 | ░░░░░░░░░░ 0% |
| Phase 3 | Memory + Context Buffer + Identity | 20 | 0 | ░░░░░░░░░░ 0% |
| Phase 4 | CLI Interface | 8 | 0 | ░░░░░░░░░░ 0% |
| Phase 5 | Tool System (registry + pipeline) | 7 | 0 | ░░░░░░░░░░ 0% |
| Phase 6 | System Control Skills | 9 | 0 | ░░░░░░░░░░ 0% |
| Phase 7 | Browser & Web Skills | 9 | 0 | ░░░░░░░░░░ 0% |
| Phase 8 | External APIs & Integrations | 9 | 0 | ░░░░░░░░░░ 0% |
| Phase 9 | Agents (Basic → Advanced) | 8 | 0 | ░░░░░░░░░░ 0% |
| Phase 10 | Task Decomposition Engine | 9 | 0 | ░░░░░░░░░░ 0% |
| Phase 11 | Feedback & Learning | 9 | 0 | ░░░░░░░░░░ 0% |
| Phase 12 | Web UI + Voice + Vision | 23 | 0 | ░░░░░░░░░░ 0% |
| Phase 13 | Telegram Interface | 6 | 0 | ░░░░░░░░░░ 0% |
| Phase 14 | GUI Desktop App + System Tray | 7 | 0 | ░░░░░░░░░░ 0% |
| Phase 15 | QA + Optimization + Security | 12 | 0 | ░░░░░░░░░░ 0% |
| Phase 16 | Personality Layer | 5 | 0 | ░░░░░░░░░░ 0% |

---

## 🏗️ Phase 1 — Foundation & Project Setup
> **Goal:** Working project skeleton, config system, logging, and all base infrastructure in place before a single Python module is written.
> **Definition of done:** `python app/main.py --interface cli` boots without crashing (even if it just prints "Jarvis ready"); all config loads; logging writes to `logs/`; all `__init__.py` files exist.

- [ ] **1.1** — `config/settings.yaml` — main application settings
  - [ ] 1.1.1 — Jarvis name, languages (`["ar","en"]`), wake_word
  - [ ] 1.1.2 — Model names matching exact Ollama tags: `gemma3:4b`, `qwen3:8b`, `qwen2.5-coder:7b`, `llava:7b`
  - [ ] 1.1.3 — Interface ports and hosts (web: 127.0.0.1:8080, telegram: polling_timeout)
  - [ ] 1.1.4 — Storage paths: data/, logs/, chroma/, sqlite DB path
  - [ ] 1.1.5 — Hardware limits: `gpu_vram_limit_gb: 5.5`, `max_ollama_concurrent: 1`, `model_swap_timeout_s: 30`
  - [ ] 1.1.6 — Hotkeys section: `open_cli: "ctrl+alt+j"`, `start_voice: "ctrl+alt+s"` (configurable)
  - [ ] 1.1.7 — Session settings: `max_iterations: 5`, `max_escalation_depth: 2`

- [ ] **1.2** — `config/models.yaml` — per-model parameters + capability profiles
  - [ ] 1.2.1 — Generation defaults per model: temperature, top_p, max_tokens
  - [ ] 1.2.2 — Capability profile fields: `reasoning_tier`, `arabic_quality` (0–1), `code_bias` (0–1), `latency_tier`, `vram_estimate_gb`, `vision_required`
  - [ ] 1.2.3 — **Remove `qwen2.5:7b`** — replaced by `qwen3:8b` in all profiles
  - [ ] 1.2.4 — Routing weights and thresholds as tunable YAML keys (no magic constants in Python)

- [ ] **1.3** — `.env.example` — all required environment variables documented
  - [ ] 1.3.1 — `TELEGRAM_BOT_TOKEN`
  - [ ] 1.3.2 — `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`
  - [ ] 1.3.3 — `YOUTUBE_API_KEY`
  - [ ] 1.3.4 — `JARVIS_ENV` (development | production)
  - [ ] 1.3.5 — `REDIS_URL` (default: `redis://localhost:6379`)

- [ ] **1.4** — `config/skills.yaml` — tool registry manifest
  - [ ] 1.4.1 — Entry per tool: id, enabled (bool), category, module path, JSON schema pointer
  - [ ] 1.4.2 — All Phase 5–8 tools pre-declared here (enabled: false until implemented)
  - [ ] 1.4.3 — `schemas_dir: config/schemas` pointer

- [ ] **1.5** — `requirements.txt` — complete and version-pinned
  - [ ] 1.5.1 — Core: `ollama`, `fastapi`, `uvicorn[standard]`, `pydantic>=2`, `pydantic-settings`, `jinja2`
  - [ ] 1.5.2 — Memory: `chromadb`, `redis`, `sentence-transformers`
  - [ ] 1.5.3 — Audio: `openai-whisper`, `piper-tts`, `openwakeword`, `pyaudio`, `sounddevice`, `webrtcvad`
  - [ ] 1.5.4 — Vision + Image gen: `diffusers`, `torch`, `torchvision`, `accelerate`, `Pillow`
  - [ ] 1.5.5 — Browser + automation: `playwright`, `psutil`, `pyautogui`, `pyperclip`
  - [ ] 1.5.6 — Google APIs: `google-auth`, `google-auth-oauthlib`, `google-api-python-client`
  - [ ] 1.5.7 — Interfaces: `python-telegram-bot`, `rich`, `PyQt6`
  - [ ] 1.5.8 — Utils: `loguru`, `pyyaml`, `python-dotenv`, `httpx`, `aiofiles`
  - [ ] 1.5.9 — Windows-specific: `pywin32`, `pycaw`, `pystray`, `winotify`, `keyboard`, `pynput`, `mss`, `pytesseract`
  - [ ] 1.5.10 — Document readers: `pypdf`, `pdfplumber`, `python-docx`, `openpyxl`, `python-pptx`
  - [ ] 1.5.11 — Dev/test: `pytest`, `pytest-asyncio`, `pytest-cov`

- [ ] **1.6** — `app/main.py` — primary entry point
  - [ ] 1.6.1 — `--interface [cli|web|telegram|gui|voice|all]` argument parser
  - [ ] 1.6.2 — Loguru initialization: file rotation, log level from config
  - [ ] 1.6.3 — Config loader: load `config/settings.yaml` + `.env` into Pydantic settings
  - [ ] 1.6.4 — Validate model names against `ollama list` on startup; warn if missing
  - [ ] 1.6.5 — Launch selected interface(s) — async or subprocess per interface

- [ ] **1.7** — Installation scripts
  - [ ] 1.7.1 — `scripts/install.sh` — Linux/WSL: apt packages (portaudio, ffmpeg, tesseract, redis), venv, pip, `playwright install chromium`, Ollama model pulls
  - [ ] 1.7.2 — `scripts/install.ps1` — Windows: winget Ollama, model pulls, venv, pip, playwright, Tesseract installer
  - [ ] 1.7.3 — Whisper model pre-download: `python -c "import whisper; whisper.load_model('medium')"`
  - [ ] 1.7.4 — Piper Arabic voice download: `ar_JO-kareem-medium.onnx`
  - [ ] 1.7.5 — openWakeWord model download: `hey_jarvis` ONNX file

- [ ] **1.8** — Project skeleton cleanup
  - [ ] 1.8.1 — Rename any leftover `New folder/` → `src/core/agents/extensions/`
  - [ ] 1.8.2 — `__init__.py` in every `src/` subdirectory (including all nested skill dirs)
  - [ ] 1.8.3 — `config/schemas/` — JSON Schema files for all skills pre-declared even if empty
  - [ ] 1.8.4 — `data/.gitkeep`, `logs/.gitkeep`, `.gitignore` covers: venv, `__pycache__`, `data/`, `logs/`, `.env`, `data/google_token.json`, `sessions/`
  - [ ] 1.8.5 — `pyproject.toml` or `setup.cfg` with `[tool.pytest.ini_options]` and `PYTHONPATH = src`

---

## 🧠 Phase 2 — LLM Engine, Model Router, Decision Layer & Runtime
> **Goal:** A working autonomous loop: Observe → Decide → Think → Act → Evaluate → (Escalate | Finish). Adaptive model routing. VRAM-safe swaps. Confidence + cost estimation. Error Intelligence. Self-Evaluation. Persistent state.
> **Definition of done:** A text input reaches the loop, is classified by the Decision Layer, routed to the correct model, evaluated, and returns a response — all wired and testable end-to-end.

- [ ] **2.1** — `src/models/llm/engine.py` — base Ollama interface
  - [ ] 2.1.1 — `chat(messages, model, stream=True)` — streaming + non-streaming support
  - [ ] 2.1.2 — `generate(prompt, model)` — single completion
  - [ ] 2.1.3 — Connection error handling + exponential backoff retry (max 3 attempts)
  - [ ] 2.1.4 — Arabic system prompt support (UTF-8, RTL-safe)
  - [ ] 2.1.5 — Return structured response: `{text, model, tokens_used, latency_ms}`
  - [ ] 2.1.6 — Tool call parsing from Ollama response (extract `tool_calls` block if present)

- [ ] **2.2** — `src/models/llm/router.py` — dynamic model selector
  - [ ] 2.2.1 — Ingest `DecisionOutput` + capability profiles + modalities + `cost_estimate`
  - [ ] 2.2.2 — Score candidate models: fit_complexity × fit_mode − cost_penalty × quality_need (all from config weights)
  - [ ] 2.2.3 — Code/execution signal → prefer `qwen2.5-coder:7b`
  - [ ] 2.2.4 — Vision signal (pixels present) → prefer `llava:7b`
  - [ ] 2.2.5 — Fast mode + low complexity → prefer `gemma3:4b`
  - [ ] 2.2.6 — Deep mode / high complexity / escalation → prefer `qwen3:8b`
  - [ ] 2.2.7 — VRAM guard: serialize model swaps; only one heavy model at a time; unload before loading
  - [ ] 2.2.8 — User/interface override hooks without bypassing safety caps
  - [ ] 2.2.9 — Memory-informed bias: boost/penalize models based on prior outcomes from Phase 3 hooks

- [ ] **2.3** — `src/models/llm/prompts.py` — system prompt templates
  - [ ] 2.3.1 — Jarvis Arabic personality prompt
  - [ ] 2.3.2 — Jarvis English personality prompt
  - [ ] 2.3.3 — Code-mode system prompt (structured output, no prose fluff)
  - [ ] 2.3.4 — Planning-mode system prompt (step decomposition, numbered lists)
  - [ ] 2.3.5 — Mode packs — composable fragments: fast / normal / deep / planning / research
  - [ ] 2.3.6 — Tool-use prompt fragment: how to call tools, how to format tool arguments

- [ ] **2.4** — `src/core/runtime/runtime_manager.py` — session lifecycle + turn orchestration
  - [ ] 2.4.1 — Start/end "run" per user turn; hook interfaces → brain → tools
  - [ ] 2.4.2 — Enforce max loop iterations and per-step timeouts (from config)
  - [ ] 2.4.3 — Coordinate with model router for VRAM budget
  - [ ] 2.4.4 — Expose `run(user_input, session_id, interface_id)` → async generator of response chunks

- [ ] **2.5** — `src/core/runtime/state/` — conversation + run state
  - [ ] 2.5.1 — Track: messages, pending tool calls, step index, last observation, tool traces
  - [ ] 2.5.2 — Serializable snapshots (JSON) for debugging and resume

- [ ] **2.6** — `src/core/runtime/loop/` — Observe → Decide → Think → Act → Evaluate driver
  - [ ] 2.6.1 — **Observe:** ingest user input + tool results + memory snippets + context buffer snapshot
  - [ ] 2.6.2 — **Decide:** run Decision Layer; inject mode + budgets + prior confidence + identity priors
  - [ ] 2.6.3 — **Think:** call LLM via dynamic router + mode-appropriate system prompt; may emit tool calls or candidate answer
  - [ ] 2.6.4 — **Act:** delegate to executor (no-op stub until Phase 5 wired); feed results as next observation
  - [ ] 2.6.5 — **Evaluate:** compute posterior confidence + answer quality + task satisfaction
  - [ ] 2.6.6 — **Branch:** Finish (stream to user + save memory) OR Escalate (re-enter Decide with updated signals)
  - [ ] 2.6.7 — **Failure path:** surface errors as structured observations; emit fallback safe response
  - [ ] 2.6.8 — Context Buffer integration: Observe reads from buffer snapshot when inputs staged
  - [ ] 2.6.9 — Merge multiple buffered inputs (text + image + file) into one unified observation bundle
  - [ ] 2.6.10 — Pass merged bundle to Decision Layer as structured multimodal input

- [ ] **2.7** — `src/core/runtime/executor/` — tool execution facade
  - [ ] 2.7.1 — `execute_tool(name, args)` interface with validation hooks
  - [ ] 2.7.2 — Permission policy placeholder: allowlist, confirm-first flags
  - [ ] 2.7.3 — Timeout wrapper per tool execution (configurable default: 30s)
  - [ ] 2.7.4 — Return structured result: `{tool, args, result, error, duration_ms}`

- [ ] **2.8** — `src/core/brain/orchestrator.py` — bridges runtime ↔ LLM ↔ memory
  - [ ] 2.8.1 — Receive input from any interface via runtime manager
  - [ ] 2.8.2 — Detect high-level intent: chat / tool / plan / search / vision / voice
  - [ ] 2.8.3 — Return unified response format (stream-friendly async generator)
  - [ ] 2.8.4 — Accept enqueue/commit flows from interfaces (context buffer staging)

- [ ] **2.9** — `src/core/brain/dispatcher.py` — intent → handler routing
  - [ ] 2.9.1 — Map intent → tool path / agent path / direct LLM
  - [ ] 2.9.2 — Pass context, history, and identity priors
  - [ ] 2.9.3 — Graceful error handling: failed dispatch → fallback to LLM with error context

- [ ] **2.10** — `src/core/events/event_bus.py` — async pub/sub event system
  - [ ] 2.10.1 — Async event emitter with subscribe/publish API
  - [ ] 2.10.2 — Events: `on_message`, `on_response`, `on_wake_word`, `on_error`, `on_tool_start`, `on_tool_end`, `on_decision`, `on_evaluate`, `on_escalation`, `on_model_swap`, `on_feedback`

- [ ] **2.11** — `src/core/runtime/decision/` — Decision Layer
  - [ ] 2.11.1 — `DecisionOutput` Pydantic schema: intent, complexity, mode, requires_tools, requires_planning, confidence, cost_estimate, model_preference
  - [ ] 2.11.2 — Intent classification: chat / code / research / action / vision / voice
  - [ ] 2.11.3 — Complexity estimation: low / medium / high (from message length, structure, ambiguity)
  - [ ] 2.11.4 — Time/effort estimation: expected tokens, tool rounds, planning steps
  - [ ] 2.11.5 — Tool necessity detection: set `requires_tools=True` when external facts/APIs/FS needed
  - [ ] 2.11.6 — Planning trigger: set `requires_planning=True` for multi-step non-linear goals
  - [ ] 2.11.7 — Prior confidence: estimated answer reliability before any LLM call
  - [ ] 2.11.8 — Cost estimate: `{tokens, latency_tier, gpu_load_tier}` — feeds router scoring
  - [ ] 2.11.9 — Context Buffer as primary input source (merged multimodal bundle)
  - [ ] 2.11.10 — Identity priors from user profile (language bias, technical level, recurring patterns)

- [ ] **2.12** — Mode controller — bind Thinking Modes to prompt packs + decode params
  - [ ] 2.12.1 — Map `fast | normal | deep | planning | research` → prompt fragment + temperature/top_p override
  - [ ] 2.12.2 — Same model, different modes → different system prompt composition

- [ ] **2.13** — Escalation engine
  - [ ] 2.13.1 — Triggers: posterior confidence low / incomplete answer / tool failure / repeated user rephrase
  - [ ] 2.13.2 — Actions: deeper mode / stronger model / enable planning / add tool round
  - [ ] 2.13.3 — `max_escalation_depth` + `max_iterations` + per-step timeouts from config
  - [ ] 2.13.4 — Bounded retries with exponential backoff

- [ ] **2.14** — Capability profiles — structured metadata per model
  - [ ] 2.14.1 — Fields: reasoning_tier, arabic_quality, latency_tier, code_bias, vision_required, vram_estimate_gb
  - [ ] 2.14.2 — Router reads from `config/models.yaml`; no hardcoded model logic in Python

- [ ] **2.15** — Integrate Decision Layer ↔ router ↔ loop
  - [ ] 2.15.1 — Decision injects mode + flags before Think; router scores all candidates
  - [ ] 2.15.2 — Mid-loop model swap when escalation fires (VRAM guard active)
  - [ ] 2.15.3 — Full context buffer path: interface → enqueue → Observe → Decide → Think

- [ ] **2.16** — Limits & fallback policy
  - [ ] 2.16.1 — Per-turn / per-tool / per-model-load timeouts (all configurable)
  - [ ] 2.16.2 — Safe fallback response when any cap is hit (no silent failures)

- [ ] **2.17** — Test LLM + runtime + decision wiring
  - [ ] 2.17.1 — Arabic chat → Decision routes to `qwen3:8b`
  - [ ] 2.17.2 — Code signal → scoring favors `qwen2.5-coder:7b`
  - [ ] 2.17.3 — Low confidence → escalation fires → deeper mode
  - [ ] 2.17.4 — VRAM guard: two heavy models cannot load simultaneously
  - [ ] 2.17.5 — `DecisionOutput` schema validation tests

- [ ] **2.18** — Confidence system — prior + posterior
  - [ ] 2.18.1 — Prior: estimated in Decision Layer from ambiguity / missing info signals
  - [ ] 2.18.2 — Posterior: produced in Evaluate from task-specific quality checks
  - [ ] 2.18.3 — Threshold bands (high/medium/low) configurable per intent type

- [ ] **2.19** — Cost estimation system
  - [ ] 2.19.1 — Populate `cost_estimate.tokens` from prompt length estimate
  - [ ] 2.19.2 — Map model + mode → `latency_tier` / `gpu_load_tier`
  - [ ] 2.19.3 — Router uses cost × quality tradeoff from config weights

- [ ] **2.20** — Evaluate stage — first-class module (`src/core/runtime/evaluate/`)
  - [ ] 2.20.1 — Inputs: candidate answer, tool traces, `DecisionOutput`, memory hints
  - [ ] 2.20.2 — Outputs: quality_score (0–1), posterior_confidence, `stop | escalate` recommendation
  - [ ] 2.20.3 — Task satisfaction check: did answer address all sub-questions?

- [ ] **2.21** — Memory-influenced decision (stub interface for Phase 3)
  - [ ] 2.21.1 — Decision layer accepts `memory_hints` dict (injected from Phase 3 once built)
  - [ ] 2.21.2 — Router accepts `profile_bias` dict (model boost/penalize from history)
  - [ ] 2.21.3 — Define stable interface so Phase 2 runs with empty stubs; Phase 3 fills them

- [ ] **2.22** — Integration test — confidence + cost + evaluate + escalation
  - [ ] 2.22.1 — Low prior → cheap route; high complexity → higher cost allocation
  - [ ] 2.22.2 — Posterior low → escalation within depth limit
  - [ ] 2.22.3 — Limits hit → fallback path executes

- [ ] **2.23** — Error Intelligence System — classify failures, drive smart retry
  - [ ] 2.23.1 — Error taxonomy: `model_error | tool_error | timeout | invalid_input | vram_oom | network | unknown`
  - [ ] 2.23.2 — Tool error: surface provider/HTTP/schema errors as structured observations
  - [ ] 2.23.3 — Model error: parse Ollama failures → observation + error class
  - [ ] 2.23.4 — Timeout: distinguish per-step vs global; surface which step timed out
  - [ ] 2.23.5 — VRAM OOM: detect Ollama CUDA OOM → force unload → retry with smaller model
  - [ ] 2.23.6 — Invalid input: validate before execute; optional LLM repair pass on malformed tool args
  - [ ] 2.23.7 — Smart retry: retry same model → switch model → switch mode → decompose task → give up
  - [ ] 2.23.8 — Connect to Decision Layer + router + escalation

- [ ] **2.24** — Self-Evaluation System — extend Evaluate with answer-level checks
  - [ ] 2.24.1 — Completeness: does answer address all sub-questions in the original message?
  - [ ] 2.24.2 — Correctness estimation: consistency with tool traces and memory
  - [ ] 2.24.3 — Hallucination / grounding detection: flag unsupported claims
  - [ ] 2.24.4 — Merge output into Evaluate result; feed escalation + Phase 11 feedback hooks
  - [ ] 2.24.5 — Self-critique prompt: ask same model "rate this answer 0–10, identify gaps"

- [ ] **2.25** — Persistent Runtime State — long-lived execution context
  - [ ] 2.25.1 — Append-only execution log per `run_id` (SQLite)
  - [ ] 2.25.2 — Resume interrupted tasks: load state by `run_id`, re-enter loop at last checkpoint
  - [ ] 2.25.3 — Long-running task states: `running | background | await_user | polling | done | failed`
  - [ ] 2.25.4 — Integrate with orchestrator + event_bus + Phase 11 feedback hooks

- [ ] **2.26** — Identity-aware LLM invocation — models are never prompted as standalone
  - [ ] 2.26.1 — Route every `chat/generate` through System Prompt Builder (3.17) + model awareness (3.16)
  - [ ] 2.26.2 — Router + mode controller apply on top of identity layer (not instead of it)
  - [ ] 2.26.3 — Regression tests: swap model id; identity framing remains stable

---

## 💾 Phase 3 — Memory System (incl. Adaptive Memory + Context Buffer + Identity)
> **Goal:** Jarvis remembers conversations and facts across sessions; learned preferences and outcomes feed the Decision Layer and router. Identity system ensures consistent behavior across all model calls.
> **Definition of done:** A fact learned in session 1 can be recalled in session 2 via semantic search; user profile influences model selection; every LLM call receives the correct identity + user + task context.

- [ ] **3.1** — `src/core/memory/short_term.py` — in-session memory
  - [ ] 3.1.1 — Conversation history as list of `{role, content, timestamp}` dicts
  - [ ] 3.1.2 — Token-aware trimming: keep most recent messages within configurable token budget
  - [ ] 3.1.3 — In-memory backend with optional Redis persistence
  - [ ] 3.1.4 — Redis connection: auto-reconnect, fallback to memory-only on failure
  - [ ] 3.1.5 — Configurable max history length and token budget from settings

- [ ] **3.2** — `src/core/memory/long_term.py` — persistent semantic memory
  - [ ] 3.2.1 — ChromaDB collection per user/workspace
  - [ ] 3.2.2 — `remember(text, metadata)` — embed and store a fact or outcome
  - [ ] 3.2.3 — `recall(query, n=5)` — semantic similarity search; return ranked snippets
  - [ ] 3.2.4 — Auto-save important facts from conversations (fact extraction heuristic)
  - [ ] 3.2.5 — Configurable embedding model (default: `all-MiniLM-L6-v2`)
  - [ ] 3.2.6 — Collection lifecycle: create, clear, delete; survive restart

- [ ] **3.3** — `src/core/memory/database.py` — SQLite structured storage
  - [ ] 3.3.1 — `conversations` table: id, role, content, timestamp, session_id
  - [ ] 3.3.2 — `facts` table: id, content, source, category, created_at, importance
  - [ ] 3.3.3 — `tasks` table: id, title, status, priority, created_at, updated_at, run_id
  - [ ] 3.3.4 — `feedback` table: id, turn_id, model, mode, score, timestamp (for Phase 11)
  - [ ] 3.3.5 — Schema auto-creation on init; migration-friendly (additive only)
  - [ ] 3.3.6 — CRUD with parameterized queries (no string formatting → SQL injection safe)

- [ ] **3.4** — `src/core/memory/manager.py` — unified memory interface
  - [ ] 3.4.1 — `save_interaction(role, content, session_id)`
  - [ ] 3.4.2 — `get_context(n_messages, session_id)` — for LLM context window assembly
  - [ ] 3.4.3 — `search(query, n=5)` — search across short-term + long-term + database
  - [ ] 3.4.4 — Lazy initialization: backends only connect when first needed
  - [ ] 3.4.5 — `export_session(session_id)` → JSON (for conversation export feature)

- [ ] **3.5** — Integrate memory into orchestrator + runtime Observe step
  - [ ] 3.5.1 — Auto-inject top-N relevant memories into LLM context at Observe stage
  - [ ] 3.5.2 — Auto-save each interaction after turn completion (async, non-blocking)

- [ ] **3.6** — Test memory system
  - [ ] 3.6.1 — Store and retrieve exact conversation
  - [ ] 3.6.2 — Semantic search returns relevant (not exact) matches
  - [ ] 3.6.3 — Cross-session memory persistence (write session 1, read session 2)
  - [ ] 3.6.4 — Redis failure → graceful fallback to in-memory

- [ ] **3.7** — `src/core/memory/user_profile.py` — adaptive memory / user profiling
  - [ ] 3.7.1 — Preferred language (auto-detect from history, user override)
  - [ ] 3.7.2 — Preferred response style: concise / balanced / detailed
  - [ ] 3.7.3 — Technical level: beginner / intermediate / expert (inferred from interactions)
  - [ ] 3.7.4 — Common intents: recurring task patterns as prior biases
  - [ ] 3.7.5 — JSON file storage keyed by user/session; versioned updates; merge on conflict

- [ ] **3.8** — Memory-driven decisions — close the loop with Phase 2
  - [ ] 3.8.1 — Influence model selection: boost/penalize profiles per task pattern history
  - [ ] 3.8.2 — Influence thinking mode: bias toward fast/deep from session history
  - [ ] 3.8.3 — Expose hooks: `memory.manager.get_decision_hints(session_id)` → consumed by `2.21`

### Context Buffer System
> **Goal:** Multimodal input staging before execution. Accept multiple inputs per turn; hold text, files, images, and audio references temporarily; provide lightweight context for Observe and Decision. No heavy models in this layer — inference happens later.

- [ ] **3.9** — `src/core/context/buffer.py` — Context Buffer
  - [ ] 3.9.1 — Temporary storage for inputs until commit/execute
  - [ ] 3.9.2 — Accumulate multiple inputs before the runtime run fires
  - [ ] 3.9.3 — Support types: text, file (PDF/Office), image, audio — store paths/handles only

- [ ] **3.10** — Input registration
  - [ ] 3.10.1 — Assign stable `input_id` per item (UUID)
  - [ ] 3.10.2 — Track type, size, mime, source interface
  - [ ] 3.10.3 — Timestamp each entry for ordering, TTL, and debugging

- [ ] **3.11** — Lightweight preprocessing (cheap metadata only)
  - [ ] 3.11.1 — Text: normalize whitespace, detect language, optional chunking
  - [ ] 3.11.2 — File: size, extension, mime detection (no content parsing here)
  - [ ] 3.11.3 — Image: dimensions, format — no vision model invoked at this stage
  - [ ] 3.11.4 — Audio: duration estimate — no STT at this stage

- [ ] **3.12** — Buffer lifecycle
  - [ ] 3.12.1 — Clear after successful execute / turn completion
  - [ ] 3.12.2 — In-memory with optional session-scoped backing
  - [ ] 3.12.3 — Configurable idle TTL: evict stale inputs automatically

- [ ] **3.13** — Integration wiring (mandatory)
  - [ ] 3.13.1 — Runtime loop: Observe reads buffer snapshot per 2.6.8–2.6.10
  - [ ] 3.13.2 — Decision Layer: primary signals from merged buffer (2.11.9)
  - [ ] 3.13.3 — Tool executor: Act phase resolves buffer refs to concrete file paths (5.16); heavy readers run in Act, not in buffer

### Identity & Profiles System
> **Goal:** Every LLM call in Jarvis carries a coherent, consistent identity. Models are components of one system — not standalone products. System prompts are dynamic (built from config + session + task + mode), not static strings.
> **Safety contract:** Never expose raw filesystem paths, API keys, credentials, or unrestricted host introspection in any model-facing prompt.

- [ ] **3.14** — `src/core/identity/user_profile.py` — identity-aware user profile
  - [ ] 3.14.1 — Load/save per user_id / session_id
  - [ ] 3.14.2 — Fields: display_name, language_preferences, behavior_style, technical_level, timezone
  - [ ] 3.14.3 — Merge strategy with 3.7 (avoid duplicate sources of truth — one canonical profile)
  - [ ] 3.14.4 — Load into runtime: available to Observe, Decision, prompt builder at every turn
  - [ ] 3.14.5 — Dynamic updates: CLI / Web `/profile` commands edit profile in real time

- [ ] **3.15** — `config/jarvis_identity.yaml` — Jarvis system identity definition
  - [ ] 3.15.1 — `name`, `role`, `architecture`, `version`
  - [ ] 3.15.2 — Capabilities summary (tools, memory, planning, multimodal) — kept current as phases ship
  - [ ] 3.15.3 — Default tone and behavior baseline
  - [ ] 3.15.4 — Pydantic model in `src/core/identity/jarvis_profile.py` to load and validate

- [ ] **3.16** — `src/core/identity/model_awareness.py` — per-call identity injection
  - [ ] 3.16.1 — Inject on every call: Jarvis identity + user profile + system context
  - [ ] 3.16.2 — Required framing: "You are a component of Jarvis AI assistant system"
  - [ ] 3.16.3 — Same framing across fast/deep/coder/vision — only task and mode sections differ

- [ ] **3.17** — `src/core/identity/prompt_builder.py` — System Prompt Builder
  - [ ] 3.17.1 — Combine: Jarvis identity → safety constraints → user profile → task context → mode fragment → tool list
  - [ ] 3.17.2 — Inject into every model call via single pipeline (no calls bypass this)
  - [ ] 3.17.3 — Deterministic assembly order (identity → safety → user prefs → task → mode)
  - [ ] 3.17.4 — Token budget awareness: trim lower-priority sections if total exceeds limit

- [ ] **3.18** — Shared context awareness
  - [ ] 3.18.1 — Rolling conversation summary + message window + tool traces in every prompt
  - [ ] 3.18.2 — Previous actions: compact list of recent tool calls + outcomes
  - [ ] 3.18.3 — Model handoff discipline: when router switches models, identity + user + state carry forward

- [ ] **3.19** — `src/core/identity/system_awareness.py` — controlled environment awareness
  - [ ] 3.19.1 — Abstract project view: allow-listed roots, depth limits, summarized tree (no raw FS)
  - [ ] 3.19.2 — Available tools: names + one-line purpose from registry
  - [ ] 3.19.3 — Environment summary: OS class, GPU tier — no raw hardware details
  - [ ] 3.19.4 — Explicit non-goals: never expose raw secrets; redact credentials from prompts

- [ ] **3.20** — Integration wiring (mandatory)
  - [ ] 3.20.1 — Decision Layer: consume user expertise + goals as priors (2.11.10)
  - [ ] 3.20.2 — Runtime loop Observe: merge buffer + memory + identity into prompt build request
  - [ ] 3.20.3 — Context Buffer: staged attachments described in task context section
  - [ ] 3.20.4 — Memory: long-term facts + profile + adaptive hooks unified via manager
  - [ ] 3.20.5 — Phase 16 (Personality): document overlay contract so personality composes cleanly

---

## 💻 Phase 4 — CLI Interface
> **Goal:** Full-featured terminal chat with Rich formatting, streaming, Arabic RTL, global hotkeys, and background daemon.
> **Definition of done:** `python app/main.py --interface cli` shows a chat prompt; user types in Arabic or English; response streams token by token with correct RTL; slash commands work; Ctrl+C exits cleanly.
> **Dependency:** Phases 1–3 complete (config + runtime + memory must be bootable).

- [ ] **4.1** — `src/interfaces/cli/interface.py` — main CLI class
  - [ ] 4.1.1 — Rich panel-based UI: bordered message areas for user/assistant/system
  - [ ] 4.1.2 — Streaming response: token-by-token with `Live` update (no full repaint)
  - [ ] 4.1.3 — Arabic RTL detection: auto-detect direction per message, align correctly
  - [ ] 4.1.4 — Keyboard shortcuts: Ctrl+C (exit with cleanup), Ctrl+L (clear screen), Ctrl+K (search history)
  - [ ] 4.1.5 — Syntax-highlighted code blocks in responses (`rich.syntax`)
  - [ ] 4.1.6 — Status bar: current model, mode, session stats, VRAM estimate
  - [ ] 4.1.7 — Typing indicator: animated dots during LLM generation

- [ ] **4.2** — `src/interfaces/cli/commands.py` — slash command system
  - [ ] 4.2.1 — `/clear` — clear conversation history (with confirmation prompt)
  - [ ] 4.2.2 — `/model [name]` — switch active model (validates against `ollama list`)
  - [ ] 4.2.3 — `/mode [fast|normal|deep|planning|research]` — switch thinking mode
  - [ ] 4.2.4 — `/memory` — show recent memories (short-term + top long-term matches)
  - [ ] 4.2.5 — `/tools` — list all registered tools with status (enabled/disabled/unavailable)
  - [ ] 4.2.6 — `/status` — show current model, mode, VRAM usage, session stats, uptime
  - [ ] 4.2.7 — `/profile` — show and edit user profile (language, style, technical level)
  - [ ] 4.2.8 — `/config` — show current configuration summary (non-sensitive keys)
  - [ ] 4.2.9 — `/help` — show all commands with descriptions
  - [ ] 4.2.10 — Tab-completion for slash commands (using `prompt_toolkit` or `readline`)
  - [ ] 4.2.11 — `/export` — export current session to Markdown file

- [ ] **4.3** — Connect CLI to runtime manager / orchestrator
  - [ ] 4.3.1 — Pass user input to orchestrator with session context and interface_id=`cli`
  - [ ] 4.3.2 — Render streaming response with real-time Rich `Live` display
  - [ ] 4.3.3 — Display decision metadata in status bar (model, mode, confidence, latency)
  - [ ] 4.3.4 — Handle tool execution display: show tool name + args + result inline

- [ ] **4.4** — `app/cli.py` — CLI entry point (delegates to main.py with `--interface cli`)

- [ ] **4.5** — Input history and navigation
  - [ ] 4.5.1 — Arrow key history navigation (up/down through previous inputs)
  - [ ] 4.5.2 — History persistence across sessions (`data/cli_history.txt`)
  - [ ] 4.5.3 — Multi-line input: Shift+Enter or backslash continuation

- [ ] **4.6** — Test CLI
  - [ ] 4.6.1 — Arabic conversation end-to-end (input → RTL display → Arabic response)
  - [ ] 4.6.2 — Streaming response renders correctly without flicker
  - [ ] 4.6.3 — All slash commands execute without error
  - [ ] 4.6.4 — History navigation works across restart

- [ ] **4.7** — Global hotkey registration (Windows + Linux)
  - [ ] 4.7.1 — Ctrl+Alt+J → bring Jarvis CLI to focus / open new session
  - [ ] 4.7.2 — Ctrl+Alt+S → trigger voice input from any active context
  - [ ] 4.7.3 — Use `keyboard` library (Windows) + `pynput` fallback (Linux)
  - [ ] 4.7.4 — Hotkey bindings configurable in `config/settings.yaml → hotkeys`
  - [ ] 4.7.5 — Graceful failure: log warning if hotkey registration fails (no crash)

- [ ] **4.8** — Windows system tray daemon
  - [ ] 4.8.1 — Run Jarvis as background process (pystray tray icon)
  - [ ] 4.8.2 — Right-click tray menu: Open CLI / Open Web UI / Open GUI / Settings / Quit
  - [ ] 4.8.3 — Use `pystray` + `Pillow` for icon rendering
  - [ ] 4.8.4 — Optional auto-start on Windows login (registry key, user-controlled toggle in settings)
  - [ ] 4.8.5 — Wake word detection in background activates CLI / GUI from tray

---

## 🛠️ Phase 5 — Tool System (Registry + Pipeline)
> **Goal:** Every capability in Jarvis is a registered, callable tool with a stable name, validated input/output schema, and lifecycle management. The LLM chooses tools; the executor runs them; results feed the loop.
> **Definition of done:** The registry discovers all tools in `src/skills/`; a dummy tool can be called end-to-end through the executor; tool schemas export in Ollama-compatible format.
> **Dependency:** Phase 2 (executor stub must be wired); Phase 3 (buffer refs resolved to paths).

- [ ] **5.1** — `src/skills/base.py` — `BaseTool` abstract class
  - [ ] 5.1.1 — `name: str` property (unique, snake_case, no spaces)
  - [ ] 5.1.2 — `description: str` property (one sentence for LLM tool list)
  - [ ] 5.1.3 — `input_schema: dict` — JSON Schema or Pydantic model (validated before execute)
  - [ ] 5.1.4 — `execute(params: dict) → ToolResult` — structured input → structured result
  - [ ] 5.1.5 — `is_available() → bool` — check prerequisites (binary exists, API key set, etc.)
  - [ ] 5.1.6 — `version: str` — semver for tracking and compatibility
  - [ ] 5.1.7 — `category: str` — grouping (search / control / web / api / coder / reader / screen)
  - [ ] 5.1.8 — `requires_confirmation: bool` — flag for destructive operations (delete, send, kill)

- [ ] **5.2** — `src/skills/registry.py` — tool discovery + registry
  - [ ] 5.2.1 — Auto-scan `src/skills/` for `BaseTool` subclasses using importlib
  - [ ] 5.2.2 — Register all available tools with name, schema, category, version
  - [ ] 5.2.3 — Export tool list in Ollama/OpenAI-compatible `tools` format for LLM calls
  - [ ] 5.2.4 — Hot-reload: detect file changes in `src/skills/` and re-register without restart

- [ ] **5.3** — Tool calling pipeline — LLM → tool → loop
  - [ ] 5.3.1 — Map registry to Ollama-compatible tool definition format
  - [ ] 5.3.2 — Parse model tool calls from streaming responses (handle partial JSON)
  - [ ] 5.3.3 — Validate args against schema → execute → feed structured result as next observation
  - [ ] 5.3.4 — Schema validation middleware: reject malformed calls before execution (no silent guessing)

- [ ] **5.4** — Wire `src/core/runtime/executor/` to registry
  - [ ] 5.4.1 — `execute_tool(name, args) → ToolResult` with full error wrapping
  - [ ] 5.4.2 — Log tool latency, args fingerprint (hash), outcome per call
  - [ ] 5.4.3 — Metrics: success_rate, avg_latency, error_frequency per tool (for Phase 11)
  - [ ] 5.4.4 — Confirmation gate: if `requires_confirmation=True`, pause and prompt user before execute

- [ ] **5.5** — Parallel execution system
  - [ ] 5.5.1 — Concurrent tool execution for independent tools (no shared mutable state)
  - [ ] 5.5.2 — Async runtime with backpressure + cancellation on timeout
  - [ ] 5.5.3 — Background jobs for long I/O (download, PDF extract) — non-blocking
  - [ ] 5.5.4 — Integration with Task Decomposition (Phase 10) execution graph

- [ ] **5.6** — Context Buffer ↔ executor bridge
  - [ ] 5.6.1 — Resolve buffer `input_id` references to concrete file paths before tool execution
  - [ ] 5.6.2 — Enforce: no heavy tool execution during buffer staging phase; only in Act step

- [ ] **5.7** — Tool lifecycle management
  - [ ] 5.7.1 — Health check: verify external dependencies (binary, port, API key) before first use
  - [ ] 5.7.2 — Graceful degradation: mark unavailable tools as disabled; report status in `/tools`
  - [ ] 5.7.3 — Resource cleanup: release browser instances, temp file handles on session end or shutdown

---

## 🖥️ Phase 6 — System Control Skills
> **Goal:** Full OS-level control on Windows: open/close apps, file operations, clipboard, notifications, screen capture, code execution, hotkey management — all registered as tools in Phase 5 registry.
> **Definition of done:** Jarvis can open Notepad, type a file path, send a Windows notification, read the clipboard, take a screenshot, and execute a Python snippet — all via natural language commands.
> **Dependency:** Phase 5 (tool registry must exist before any skill registers).

- [ ] **6.1** — `src/skills/files/` — file operations tool
  - [ ] 6.1.1 — List directory contents (name, size, type, modified date)
  - [ ] 6.1.2 — Read file content (text files; binary files return metadata only)
  - [ ] 6.1.3 — Write/create file with path safety checks (allowlisted root dirs only)
  - [ ] 6.1.4 — Move/copy/delete (delete → recycle bin via `send2trash`, not permanent delete)
  - [ ] 6.1.5 — Search files by name (glob) or content (grep/ripgrep)
  - [ ] 6.1.6 — Windows path normalization: accept both `\` and `/`; always output normalized paths
  - [ ] 6.1.7 — Register schema: `config/schemas/control/files.schema.json` — update with new operations

- [ ] **6.2** — `src/skills/system/` — system control tool
  - [ ] 6.2.1 — Get system info: CPU %, RAM used/total, disk space, GPU VRAM (via psutil + pynvml)
  - [ ] 6.2.2 — List running processes: name, PID, CPU%, RAM%, start time
  - [ ] 6.2.3 — Kill process by name or PID (`taskkill /IM name.exe /F` on Windows, `kill` on Linux)
  - [ ] 6.2.4 — Get/set system volume (Windows: `pycaw`; Linux: `amixer`)
  - [ ] 6.2.5 — Run shell/PowerShell command in controlled sandbox (allowlist enforced; destructive ops need confirmation)
  - [ ] 6.2.6 — Network status: adapter list, IP addresses, connectivity check (ping test)
  - [ ] 6.2.7 — List Windows startup items (registry `HKCU/HKLM Run` keys)
  - [ ] 6.2.8 — List Windows Scheduled Tasks (read + basic create via `schtasks`)
  - [ ] 6.2.9 — Register schema: `config/schemas/control/system.schema.json`

- [ ] **6.3** — `src/skills/system/apps.py` — Windows application launcher
  - [ ] 6.3.1 — Open app by name: `ShellExecute` / `subprocess.Popen`; search PATH first
  - [ ] 6.3.2 — Search app in `%APPDATA%`, `Program Files`, `Program Files (x86)`, `LocalAppData`
  - [ ] 6.3.3 — Parse Windows Start Menu `.lnk` shortcuts by display name (using `win32com`)
  - [ ] 6.3.4 — Close app by name (`taskkill /IM name.exe /F`) or by PID
  - [ ] 6.3.5 — List installed applications from registry (`HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall`)
  - [ ] 6.3.6 — Bring window to foreground: `SetForegroundWindow` via `pywin32` / `ctypes`
  - [ ] 6.3.7 — Minimize / maximize / restore window by name or PID
  - [ ] 6.3.8 — Graceful shutdown: send WM_CLOSE first, then force kill after timeout
  - [ ] 6.3.9 — Register schema: `config/schemas/control/apps.schema.json`

- [ ] **6.4** — `src/skills/coder/executor.py` — code execution tool
  - [ ] 6.4.1 — Execute Python code safely in isolated subprocess with timeout
  - [ ] 6.4.2 — Execute shell/PowerShell commands (confirm-first for any destructive pattern)
  - [ ] 6.4.3 — Capture stdout/stderr; return structured result: `{stdout, stderr, returncode, duration_ms}`
  - [ ] 6.4.4 — Timeout protection: configurable (default: 30s); kills subprocess on timeout
  - [ ] 6.4.5 — Blocklist: reject commands matching dangerous patterns (`rm -rf /`, `format`, `del /s`)
  - [ ] 6.4.6 — Optional: virtual environment isolation for Python execution

- [ ] **6.5** — `src/skills/system/clipboard.py` — Clipboard manager tool
  - [ ] 6.5.1 — Read current clipboard: text content or `[IMAGE]` placeholder if image
  - [ ] 6.5.2 — Write text to clipboard
  - [ ] 6.5.3 — Monitor clipboard for changes (background thread; emit EventBus event on change)
  - [ ] 6.5.4 — Image clipboard: detect and save to temp file; return path
  - [ ] 6.5.5 — Use `pyperclip` (cross-platform text) + `win32clipboard` (Windows images)
  - [ ] 6.5.6 — Integration flows: "translate clipboard" → read → send to LLM → write back

- [ ] **6.6** — `src/skills/notify/notifications.py` — Windows notification tool
  - [ ] 6.6.1 — Send Windows Toast notification: title + body + optional icon
  - [ ] 6.6.2 — Use `winotify` (preferred) with `win10toast` as fallback
  - [ ] 6.6.3 — Notification types: info / warning / success / reminder (different icons)
  - [ ] 6.6.4 — Integration: task completion alerts, Calendar reminders, long-task "done" alerts
  - [ ] 6.6.5 — Fallback: `rich.print` console notification if Windows toast unavailable

- [ ] **6.7** — `src/skills/screen/` — Screen capture + lightweight OCR
  - [ ] 6.7.1 — Full screenshot capture using `mss` (fastest) + save as PNG
  - [ ] 6.7.2 — Region screenshot: user-defined bounding box `{x, y, width, height}`
  - [ ] 6.7.3 — Lightweight OCR via `pytesseract` (requires Tesseract binary) — no LLM needed
  - [ ] 6.7.4 — "Read what's on my screen" fast path: OCR only, no vision model loaded
  - [ ] 6.7.5 — Screenshots saved to `data/screenshots/` with timestamp filename
  - [ ] 6.7.6 — Vision model path: pass screenshot to LLaVA when semantic understanding requested
  - [ ] 6.7.7 — Register schemas: `config/schemas/screen/screenshot.schema.json`, `config/schemas/screen/ocr.schema.json`

- [ ] **6.8** — `src/skills/system/hotkeys.py` — runtime hotkey management tool
  - [ ] 6.8.1 — Register/unregister hotkey bindings at runtime as a tool (not just at startup)
  - [ ] 6.8.2 — Read bindings from `config/settings.yaml → hotkeys`
  - [ ] 6.8.3 — Emit `EventBus` event when hotkey fires (consumers: CLI, voice, tray)
  - [ ] 6.8.4 — List all active hotkeys via `/tools` or `/status`

- [ ] **6.9** — Test Phase 6 tools end-to-end
  - [ ] 6.9.1 — Open Notepad by name → verify window appears → close Notepad
  - [ ] 6.9.2 — Write text to clipboard → read back → verify match
  - [ ] 6.9.3 — Send Windows Toast notification → verify appears in notification center
  - [ ] 6.9.4 — Take screenshot → OCR → verify text extracted from known test image
  - [ ] 6.9.5 — Kill process by name → verify no longer in process list
  - [ ] 6.9.6 — Execute Python `print("hello")` → verify stdout captured correctly

---

## 🌐 Phase 7 — Browser & Web Skills
> **Goal:** Full browser control via Playwright with persistent sessions (no re-login every run), file download/upload, multi-tab management, WhatsApp Web automation, and auth-wall handling.
> **Definition of done:** Jarvis navigates to a URL, logs in once, saves the session, restarts, and reuses the session without prompting for login again.
> **Dependency:** Phase 5 (tool registry), Phase 6 (file paths for downloads/sessions).

- [ ] **7.1** — `src/skills/search/web_search.py` — web search tool
  - [ ] 7.1.1 — DuckDuckGo HTML search (no API key, no rate limits)
  - [ ] 7.1.2 — Return top-N results: title + snippet + URL + domain
  - [ ] 7.1.3 — Optional: full-page content extraction via `trafilatura` or `readability-lxml`
  - [ ] 7.1.4 — Optional: self-hosted SearxNG integration (configured via settings)
  - [ ] 7.1.5 — TTL-based result caching (avoid repeat identical searches within same session)
  - [ ] 7.1.6 — Register schema: `config/schemas/search/web_search.schema.json`

- [ ] **7.2** — `src/skills/browser/browser.py` — browser automation core
  - [ ] 7.2.1 — Launch Playwright Chromium (headless default; headed mode configurable for debugging)
  - [ ] 7.2.2 — Navigate to URL with configurable wait strategy (load / domcontentloaded / networkidle)
  - [ ] 7.2.3 — Click element: by text, CSS selector, XPath, or ARIA label
  - [ ] 7.2.4 — Fill form fields: text input, checkbox, radio, select dropdown
  - [ ] 7.2.5 — Extract page content as clean Markdown (readability parsing, removes nav/ads)
  - [ ] 7.2.6 — Take viewport or full-page screenshot; save to `data/screenshots/browser/`
  - [ ] 7.2.7 — Scroll page (down by pixels or to element)
  - [ ] 7.2.8 — Register schema: `config/schemas/browser/browser.schema.json`

- [ ] **7.3** — `src/skills/browser/session_manager.py` — persistent browser sessions
  - [ ] 7.3.1 — Save Playwright storage state (cookies + localStorage) to `data/sessions/{domain}.json`
  - [ ] 7.3.2 — Load saved session on browser open: reuse cookies → no re-login required
  - [ ] 7.3.3 — Session keyed by domain: `google.com.json`, `whatsapp.com.json`, etc.
  - [ ] 7.3.4 — Auto-detect session expiry: check for login redirect → prompt user once → re-save
  - [ ] 7.3.5 — Session vault path configured in settings; gitignored
  - [ ] 7.3.6 — All browser tools route through session manager by default

- [ ] **7.4** — `src/skills/browser/downloader.py` — file download management
  - [ ] 7.4.1 — Intercept Playwright download events (`page.on("download", ...)`)
  - [ ] 7.4.2 — Save to `data/downloads/` with original filename + timestamp on conflict
  - [ ] 7.4.3 — Return structured result: `{path, filename, size_bytes, duration_ms}`
  - [ ] 7.4.4 — Progress feedback for large files (log every 10%)

- [ ] **7.5** — `src/skills/browser/uploader.py` — file upload via browser
  - [ ] 7.5.1 — Set file input with `page.set_input_files(selector, file_path)`
  - [ ] 7.5.2 — Handle multiple file uploads (list of paths)
  - [ ] 7.5.3 — Validate file exists and is within allowed size before attempting upload
  - [ ] 7.5.4 — Confirm upload success (check for success indicator on page)

- [ ] **7.6** — Multi-tab and multi-window management
  - [ ] 7.6.1 — Open new tab; switch tabs by index or title substring
  - [ ] 7.6.2 — Close specific tab; list all open tabs
  - [ ] 7.6.3 — Handle new window popups (attach to popup context)
  - [ ] 7.6.4 — Handle alert / confirm / prompt dialogs (auto-accept configurable or ask user)

- [ ] **7.7** — Human-in-the-loop auth pause
  - [ ] 7.7.1 — Detect login/captcha wall: check URL patterns + page title keywords
  - [ ] 7.7.2 — Pause automation: send notification (6.6) + block in CLI until user signals done
  - [ ] 7.7.3 — Resume command: user presses Enter in CLI or clicks "Continue" in Web UI
  - [ ] 7.7.4 — Never silently fail on auth wall; always surface to user with clear message

- [ ] **7.8** — `src/skills/social/whatsapp.py` — WhatsApp Web automation
  - [ ] 7.8.1 — Open WhatsApp Web using saved session (7.3 session manager)
  - [ ] 7.8.2 — Search contact by name (use WhatsApp search box)
  - [ ] 7.8.3 — Send text message to contact
  - [ ] 7.8.4 — Read last N messages from active conversation (extract text from DOM)
  - [ ] 7.8.5 — QR code login: detect QR page → take screenshot → display in terminal → wait for scan → save session
  - [ ] 7.8.6 — Natural language integration: "Send [contact] a message: [text]"
  - [ ] 7.8.7 — Register schema: `config/schemas/social/whatsapp.schema.json`

- [ ] **7.9** — Test Phase 7 tools end-to-end
  - [ ] 7.9.1 — Web search: query → top-5 results with URLs
  - [ ] 7.9.2 — Session persistence: login to test site → restart → verify session reloaded
  - [ ] 7.9.3 — File download: click download link → verify file in `data/downloads/`
  - [ ] 7.9.4 — File upload: upload test file → verify success indicator on page
  - [ ] 7.9.5 — Multi-tab: open 3 tabs → switch between by title
  - [ ] 7.9.6 — WhatsApp: send message to self (saved number) and verify delivery

---

## 🔌 Phase 8 — External APIs & Integrations
> **Goal:** Jarvis connects to the full Google ecosystem (Calendar, Gmail, Drive, Contacts, YouTube) plus Office document reading/writing — all via a unified OAuth token.
> **Definition of done:** One OAuth consent screen grants access to all Google services; token auto-refreshes; Calendar CRUD, Gmail send/read, Drive upload/download all work via natural language.
> **Dependency:** Phase 5 (tool registry); Phase 7 (browser for OAuth redirect).

- [ ] **8.1** — `src/skills/api/google_auth.py` — Unified Google OAuth manager
  - [ ] 8.1.1 — Single OAuth2 flow for all Google APIs in one consent screen
  - [ ] 8.1.2 — Scopes: Calendar + Gmail + Drive + Contacts + YouTube (combined)
  - [ ] 8.1.3 — Token persistence: `data/google_token.json` (gitignored)
  - [ ] 8.1.4 — Auto-refresh expired access tokens silently (using refresh token)
  - [ ] 8.1.5 — Re-auth flow: open browser → user consents → token saved → all services ready
  - [ ] 8.1.6 — Error: invalid/revoked token → trigger re-auth automatically with user notification

- [ ] **8.2** — `src/skills/api/calendar.py` — Google Calendar
  - [ ] 8.2.1 — List upcoming events (configurable N days, all calendars or specific)
  - [ ] 8.2.2 — Create event: title, datetime, timezone, description, attendees, location
  - [ ] 8.2.3 — Update existing event by ID
  - [ ] 8.2.4 — Delete event by ID (with confirmation)
  - [ ] 8.2.5 — Search events by keyword + date range
  - [ ] 8.2.6 — Natural language: "Book a meeting with X about Y on Friday at 3pm Cairo time"
  - [ ] 8.2.7 — Register schema: `config/schemas/api/google_calendar.schema.json` (expand existing)

- [ ] **8.3** — `src/skills/api/gmail.py` — Gmail
  - [ ] 8.3.1 — Read latest N emails: sender, subject, body preview, date, thread_id
  - [ ] 8.3.2 — Search emails using Gmail query syntax (`from:X subject:Y after:2024/01/01`)
  - [ ] 8.3.3 — Send email: to, subject, body (plain text + HTML), optional attachments
  - [ ] 8.3.4 — Reply to email by thread_id / message_id
  - [ ] 8.3.5 — Mark as read / unread / starred / important
  - [ ] 8.3.6 — Move to label/folder; create label if not exists
  - [ ] 8.3.7 — Natural language: "Read my latest emails" / "Send email to X saying Y"
  - [ ] 8.3.8 — Register schema: `config/schemas/api/gmail.schema.json`

- [ ] **8.4** — `src/skills/api/drive.py` — Google Drive
  - [ ] 8.4.1 — List files in root or specific folder (name, type, size, modified)
  - [ ] 8.4.2 — Search files by name or full-text content
  - [ ] 8.4.3 — Download file by name or ID to `data/downloads/`
  - [ ] 8.4.4 — Upload local file to Drive (in root or specified folder)
  - [ ] 8.4.5 — Share file: set permission (viewer/editor) for email address
  - [ ] 8.4.6 — Create folder
  - [ ] 8.4.7 — Register schema: `config/schemas/api/google_drive.schema.json`

- [ ] **8.5** — `src/skills/api/contacts.py` — Google Contacts
  - [ ] 8.5.1 — List contacts (name, email, phone) with pagination
  - [ ] 8.5.2 — Search by name, email, or phone
  - [ ] 8.5.3 — Get full contact details
  - [ ] 8.5.4 — Create new contact
  - [ ] 8.5.5 — Update contact fields
  - [ ] 8.5.6 — Integration: "Send email to [contact name]" → resolve name to email via Contacts

- [ ] **8.6** — `src/skills/api/youtube.py` — YouTube
  - [ ] 8.6.1 — Search videos (YouTube Data API v3)
  - [ ] 8.6.2 — Get video info: title, duration, channel, views, description
  - [ ] 8.6.3 — Get channel info and recent uploads
  - [ ] 8.6.4 — Open video in default browser
  - [ ] 8.6.5 — Register schema: update `config/schemas/api/youtube.schema.json`

- [ ] **8.7** — `src/skills/pdf/` — PDF reading tool
  - [ ] 8.7.1 — Extract text from PDF (`pdfplumber` for layout-aware, `pypdf` fallback)
  - [ ] 8.7.2 — Extract images from PDF pages → save to temp dir → return paths
  - [ ] 8.7.3 — Summarize long PDF: chunk text → LLM summarize each chunk → combine
  - [ ] 8.7.4 — Extract tables as structured data (dict/CSV)
  - [ ] 8.7.5 — Register schema: `config/schemas/reader/pdf.schema.json`

- [ ] **8.8** — `src/skills/office/` — Office document reader/writer
  - [ ] 8.8.1 — Read `.docx` (python-docx): extract text, headings, tables
  - [ ] 8.8.2 — Read `.xlsx` (openpyxl): extract sheets, rows, cell values
  - [ ] 8.8.3 — Read `.pptx` (python-pptx): extract slide titles and text
  - [ ] 8.8.4 — Write simple `.docx`: create document with title, paragraphs, bullet lists
  - [ ] 8.8.5 — Write simple `.xlsx`: create spreadsheet with headers and data rows
  - [ ] 8.8.6 — Register schemas: `config/schemas/reader/office.schema.json`

- [ ] **8.9** — Test Phase 8 integrations end-to-end
  - [ ] 8.9.1 — Google OAuth: full consent flow; token saved; all services accessible
  - [ ] 8.9.2 — Calendar CRUD: create → list → update → delete test event
  - [ ] 8.9.3 — Gmail: send test email to self → search for it → read → mark as read
  - [ ] 8.9.4 — Drive: upload test file → list → download → verify content
  - [ ] 8.9.5 — Contacts: search for a known contact by name → get email
  - [ ] 8.9.6 — "Send an email to [contact name] and add a calendar reminder" — 2 tools, 1 token

---

## 🤖 Phase 9 — Agents (Basic → Advanced)
> **Goal:** Multi-step autonomous behavior. Agents coordinate tools (Phases 6–8), plan subtasks, reason with CoT, execute ReAct loops, and perform full computer control.
> **Definition of done:** "Research X, summarize it, and save to Drive" executes without step-by-step user guidance.
> **Dependency:** Phases 5–8 (all tools must be registered and callable).

### Basic Agents

- [ ] **9.1** — `src/core/agents/planner/planner.py` — step decomposition + sequencing
  - [ ] 9.1.1 — Break complex request into ordered steps using LLM (planning mode)
  - [ ] 9.1.2 — Assign each step to a specific tool, model role, or sub-agent
  - [ ] 9.1.3 — Execute steps sequentially via runtime loop
  - [ ] 9.1.4 — Pass step N output as typed artifact to step N+1 input
  - [ ] 9.1.5 — Report progress to user after each step (streaming status updates)

- [ ] **9.2** — `src/core/agents/thinker/thinker.py` — extended reasoning
  - [ ] 9.2.1 — Chain-of-Thought: multi-step internal reasoning before final answer
  - [ ] 9.2.2 — Self-verification: ask model to critique its own answer and identify gaps
  - [ ] 9.2.3 — Confidence scoring: numeric estimate attached to each thinker output
  - [ ] 9.2.4 — Use `qwen3:8b` with deep mode; respect VRAM guard

- [ ] **9.3** — ReAct loop integration (Reason + Act)
  - [ ] 9.3.1 — Observe → Think (reason about what to do) → Act (call tool) → Observe (tool result) loop
  - [ ] 9.3.2 — Max iterations guard: configurable (default: 10 tool-call rounds)
  - [ ] 9.3.3 — Optional: stream reasoning steps to user (debug mode or user setting)

### Advanced Agents

- [ ] **9.4** — `src/core/agents/researcher.py` — deep research agent
  - [ ] 9.4.1 — Multi-query web search (3–5 distinct queries per topic)
  - [ ] 9.4.2 — Scrape and summarize top-N result pages
  - [ ] 9.4.3 — Cross-reference sources: identify agreement / contradiction
  - [ ] 9.4.4 — Generate structured research report: summary + key points + sources

- [ ] **9.5** — `src/skills/screen/screen_agent.py` — visual computer control
  - [ ] 9.5.1 — Take screenshot via 6.7
  - [ ] 9.5.2 — Describe screen content via LLaVA (vision tool)
  - [ ] 9.5.3 — Decide next mouse/keyboard action using LLM
  - [ ] 9.5.4 — Execute via `pyautogui`: move, click, type, scroll, hotkey
  - [ ] 9.5.5 — Loop: screenshot → describe → decide → execute → screenshot (with step limit)

- [ ] **9.6** — Test agents
  - [ ] 9.6.1 — Multi-step task: "Search X → summarize → save to file"
  - [ ] 9.6.2 — ReAct + tool calling: tool result feeds next Think correctly
  - [ ] 9.6.3 — Screen agent: open app via screen control and verify

- [ ] **9.7** — `src/core/agents/extensions/` — pluggable agent extensions
  - [ ] 9.7.1 — `AgentExtension` base class: hooks `before_plan` / `after_plan` / `on_step_complete`
  - [ ] 9.7.2 — Extension: auto-summarize completed plan → save to long-term memory
  - [ ] 9.7.3 — Extension: send completion notification via 6.6 when long task finishes

- [ ] **9.8** — Full computer use agent loop
  - [ ] 9.8.1 — Orchestrate: screen capture (6.7) → OCR or LLaVA → LLM decision → pyautogui action
  - [ ] 9.8.2 — Support: app launcher (6.3), browser control (Phase 7), file ops (6.1)
  - [ ] 9.8.3 — Safety gate: `requires_confirmation=True` for any action with side effects
  - [ ] 9.8.4 — Max-step guard (configurable) to prevent runaway loops
  - [ ] 9.8.5 — Audit log: record every action taken for user review

---

## 🧩 Phase 10 — Task Decomposition Engine
> **Goal:** Convert a high-level natural language goal into a structured DAG (Directed Acyclic Graph) of executable steps, run them in correct order with parallelism where possible, and retry only failed branches.
> **Definition of done:** "Book a meeting with X about Y on Friday and email the agenda to all attendees" decomposes into Calendar + Gmail steps, executes correctly, and retries only the failed step if one fails.
> **Dependency:** Phase 9 (agents as execution units), Phase 8 (APIs to call).

- [ ] **10.1** — Decomposition API
  - [ ] 10.1.1 — Input: natural language goal + `DecisionOutput` context
  - [ ] 10.1.2 — Output: DAG of subtasks — schema: `{id, title, type, inputs, outputs, depends_on, retry_group, requires_confirmation}`
  - [ ] 10.1.3 — LLM-assisted decomposition (planning mode) + template library for common patterns
  - [ ] 10.1.4 — Human-in-the-loop nodes: optional approval gate before executing a subtask

- [ ] **10.2** — Execution graph runtime — deterministic scheduler
  - [ ] 10.2.1 — Topological sort; execute nodes at the parallel frontier concurrently (via Phase 5.5)
  - [ ] 10.2.2 — Pass typed artifacts: output of node A becomes input of dependent node B
  - [ ] 10.2.3 — Idempotency: stable `node_key` for safe re-run after interrupt

- [ ] **10.3** — Selective retry — only failed nodes
  - [ ] 10.3.1 — Mark failed node with error class; skip already-successful siblings
  - [ ] 10.3.2 — Partial replan: regenerate failed subgraph from last good checkpoint

- [ ] **10.4** — Integration with agents + runtime
  - [ ] 10.4.1 — Planner (9.1) can delegate complex goals to decomposition engine
  - [ ] 10.4.2 — Dispatcher routes `requires_planning=True` intents here

- [ ] **10.5** — Observability — graph export
  - [ ] 10.5.1 — Export current graph as Mermaid diagram (for Web UI dashboard)
  - [ ] 10.5.2 — Export as JSON for logging and debugging

- [ ] **10.6** — Tests
  - [ ] 10.6.1 — Diamond dependency: A → (B, C parallel) → D — verify B and C run concurrently
  - [ ] 10.6.2 — Failure mid-graph → retry only failed branch, not full graph
  - [ ] 10.6.3 — Resume after disconnect: same `run_id`, restart from last checkpoint

- [ ] **10.7** — Natural language → plan → execute (end-to-end scenarios)
  - [ ] 10.7.1 — "Book a meeting with X about Y on Friday" → Calendar tool
  - [ ] 10.7.2 — "Summarize my last 5 emails and save to Drive" → Gmail + Drive tools
  - [ ] 10.7.3 — "Open Chrome, go to YouTube, search for X, click first result" → browser agent

- [ ] **10.8** — Feedback hooks: emit success/failure signals per node for Phase 11

- [ ] **10.9** — Cost/budget awareness: inherit `cost_estimate`; skip expensive steps if budget exhausted

---

## 🔁 Phase 11 — Feedback & Learning
> **Goal:** Close the loop. Turn outcomes (tool success/failure, user continuation, explicit ratings) into durable learning that improves routing, mode selection, and memory over time — without requiring retraining.
> **Definition of done:** After 5 sessions of preferring Arabic deep answers, the Decision Layer bias measurably shifts toward `qwen3:8b` + deep mode for that user.
> **Dependency:** Phases 9–10 (agents + decomposition produce outcomes); Phase 3 (memory stores learned priors).

- [ ] **11.1** — Implicit feedback detection
  - [ ] 11.1.1 — Positive signal: user continues conversation naturally after response
  - [ ] 11.1.2 — Negative signal: user rephrases same question → confusion detected
  - [ ] 11.1.3 — Weak negative: no follow-up within session after assistant response

- [ ] **11.2** — Explicit feedback
  - [ ] 11.2.1 — CLI: `👍/👎` keyboard shortcut after each response
  - [ ] 11.2.2 — Web UI: thumbs up/down per message (12.8.3)
  - [ ] 11.2.3 — Correction message: "That's wrong, the answer is X" → negative signal

- [ ] **11.3** — Success/failure scoring
  - [ ] 11.3.1 — Map implicit/explicit signals + `Evaluate` posterior + error class → scalar score (0–1) per turn
  - [ ] 11.3.2 — Store in `feedback` table (3.3.4)

- [ ] **11.4** — Store feedback linked to decision context
  - [ ] 11.4.1 — `DecisionOutput` snapshot at time of turn
  - [ ] 11.4.2 — Resolved model id + mode pack used
  - [ ] 11.4.3 — Tool name + version + args fingerprint for tool-specific attribution

- [ ] **11.5** — Learning surfaces (incremental, bounded)
  - [ ] 11.5.1 — Router weight nudge: adjust model score multipliers from rolling 20-turn average
  - [ ] 11.5.2 — Escalation threshold tuning: lower threshold if repeated low posterior
  - [ ] 11.5.3 — Long-term memory writes: "what worked" summaries → `long_term.remember()`
  - [ ] 11.5.4 — Bounds: max delta per update step (prevent thrashing); audit log of all changes

- [ ] **11.6** — Privacy and controls
  - [ ] 11.6.1 — Per-user opt-out: disable feedback collection
  - [ ] 11.6.2 — Retention TTL: auto-delete feedback older than N days
  - [ ] 11.6.3 — Export/delete: user can export or wipe all feedback data

- [ ] **11.7** — Integration tests
  - [ ] 11.7.1 — Synthetic session: force low-confidence turns → verify weight nudge recorded
  - [ ] 11.7.2 — Full attribution chain: turn → score → feedback row → weight update

- [ ] **11.8** — Anti-gaming: rate-limit weight updates; detect rapid toggle spam

- [ ] **11.9** — Dashboard hooks: expose aggregated metrics to Phase 15 monitoring + Web UI dashboard

---

## 🌐 Phase 12 — Web UI + Voice + Vision
> **Goal:** Premium multimodal interfaces: real-time streaming chat with Glassmorphism design, full voice pipeline (wake word → STT → LLM → TTS), image understanding, image generation, and a live system dashboard.
> **Definition of done:** User speaks "Hey Jarvis, summarize my emails"; Jarvis responds via TTS with a spoken summary; Web UI shows all interactions with RTL Arabic support.
> **Dependency:** Phases 1–11 complete (all brain systems must exist for interfaces to have real functionality).

### Web UI — Premium Glassmorphism Chat Interface

- [ ] **12.1** — `src/interfaces/web/app.py` — FastAPI application backend
  - [ ] 12.1.1 — Static file serving (CSS, JS, fonts, icons)
  - [ ] 12.1.2 — Jinja2 template rendering
  - [ ] 12.1.3 — CORS configuration (same-origin for production; open for dev)
  - [ ] 12.1.4 — Session management middleware (session_id in cookie, configurable expiry)
  - [ ] 12.1.5 — Rate limiting per session/IP
  - [ ] 12.1.6 — Gzip compression for static assets

- [ ] **12.2** — `src/interfaces/web/websocket.py` — WebSocket handler
  - [ ] 12.2.1 — Accept connection with session validation
  - [ ] 12.2.2 — Receive message → orchestrator → stream tokens back as JSON frames
  - [ ] 12.2.3 — Handle disconnection gracefully (state cleanup)
  - [ ] 12.2.4 — Auto-reconnect: client detects drop → reconnect → resume
  - [ ] 12.2.5 — Heartbeat/ping-pong keep-alive
  - [ ] 12.2.6 — Support concurrent sessions (multiple browser tabs)

- [ ] **12.3** — Chat page (`src/interfaces/web/templates/index.html`)
  - [ ] 12.3.1 — Single-page app: vanilla JS (no heavy framework dependency)
  - [ ] 12.3.2 — Responsive: mobile-first, desktop-optimized
  - [ ] 12.3.3 — Arabic RTL: auto-detect text direction per message; correct alignment
  - [ ] 12.3.4 — Streaming display with animated cursor on active token
  - [ ] 12.3.5 — Code blocks: syntax highlighting (Highlight.js) + copy-to-clipboard button
  - [ ] 12.3.6 — Markdown rendering: headings, lists, bold, links, tables
  - [ ] 12.3.7 — LaTeX rendering: KaTeX for math expressions
  - [ ] 12.3.8 — Image preview: lightbox for generated/uploaded images
  - [ ] 12.3.9 — File attachment cards: filename, size, type icon, remove button
  - [ ] 12.3.10 — Message actions: copy, regenerate, edit user message, delete

- [ ] **12.4** — Design system: Glassmorphism + Frosted Acrylic (`src/interfaces/web/static/style.css`)
  - [ ] 12.4.1 — Dark theme (default): `#0a0a1a / #12122a` base; frosted glass panels (`rgba(255,255,255,0.04–0.08)`)
  - [ ] 12.4.2 — Accent gradient: electric blue → teal → violet (`#3b82f6 → #06b6d4 → #8b5cf6`)
  - [ ] 12.4.3 — Light theme: soft white/cream base, warm gray panels
  - [ ] 12.4.4 — Theme toggle with smooth 0.4s CSS transition; persist in localStorage
  - [ ] 12.4.5 — CSS custom properties: full token system (`--color-bg-primary`, `--glass-blur`, `--border-glow`, `--shadow-depth`)
  - [ ] 12.4.6 — Multi-layer blur: ambient 24px / sidebar 16px / card 12px / input 8px
  - [ ] 12.4.7 — Frosted glass panels: `backdrop-filter: blur()` + `rgba()` bg + 1px rgba border
  - [ ] 12.4.8 — Primary font: Inter; monospace: JetBrains Mono; Arabic: IBM Plex Arabic
  - [ ] 12.4.9 — Icons: Lucide Icons (consistent weight, 16px inline / 20px buttons / 24px nav)
  - [ ] 12.4.10 — Micro-animations: message fade+scale entry, 3-dot typing pulse, shimmer skeleton, button glow hover

- [ ] **12.5** — Input bar system (`src/interfaces/web/static/chat.js`)
  - [ ] 12.5.1 — Auto-expanding textarea: grows 1–8 lines, then scrolls internally
  - [ ] 12.5.2 — RTL auto-detect: switch direction based on first character
  - [ ] 12.5.3 — Attachment "+" button: opens menu (Upload File, Upload Image, Paste Clipboard)
  - [ ] 12.5.4 — Attachment preview strip above input: per-item remove button
  - [ ] 12.5.5 — Drag-and-drop: any file dragged to chat area auto-attaches
  - [ ] 12.5.6 — Clipboard paste: Ctrl+V with image on clipboard → auto-attach
  - [ ] 12.5.7 — Mode selector icon row: fast (⚡) / normal (🧠) / deep (⚛) / planning (📋) / research (🔭)
  - [ ] 12.5.8 — Dynamic send/mic button: empty input → microphone icon; typing → send arrow; smooth morph animation
  - [ ] 12.5.9 — Recording state: pulsing red ring on mic; waveform in input area
  - [ ] 12.5.10 — Keyboard: Enter → send; Shift+Enter → newline; Escape → clear; Ctrl+K → search

- [ ] **12.6** — Sidebar system
  - [ ] 12.6.1 — Collapsible left sidebar: 280px desktop; full-width overlay on mobile
  - [ ] 12.6.2 — Conversation list: title, last message preview, timestamp; grouped by day (Today / Yesterday / Last 7 days / Older)
  - [ ] 12.6.3 — New Chat button; inline title edit; delete with confirmation; pin to top; archive
  - [ ] 12.6.4 — Search: Ctrl+K opens search bar; filter by title (instant) or content (server-side)
  - [ ] 12.6.5 — Settings panel: appearance (theme, font size, blur, animations), behavior (default mode, language, enter-key), model (selector, temperature, override toggle), data (export, clear, reset profile)

- [ ] **12.7** — REST API routes (`src/interfaces/web/routes/`)
  - [ ] 12.7.1 — `GET /` — chat page
  - [ ] 12.7.2 — `GET /api/models` — list Ollama models with status
  - [ ] 12.7.3 — `GET /api/conversations` — paginated conversation list
  - [ ] 12.7.4 — `GET /api/conversations/:id` — messages for conversation
  - [ ] 12.7.5 — `PUT /api/conversations/:id` — update title / archive / pin
  - [ ] 12.7.6 — `DELETE /api/conversations/:id` — delete conversation
  - [ ] 12.7.7 — `GET /api/memory` — conversation history summary
  - [ ] 12.7.8 — `DELETE /api/memory` — clear memory
  - [ ] 12.7.9 — `POST /api/upload` — file upload → returns buffer input_id
  - [ ] 12.7.10 — `GET /api/settings` / `PUT /api/settings` — user settings CRUD
  - [ ] 12.7.11 — `GET /api/search` — full-text search across conversations
  - [ ] 12.7.12 — `GET /api/status` — VRAM, active model, tool queue, system health

- [ ] **12.8** — Notification and feedback system
  - [ ] 12.8.1 — Toast notifications: success / error / info / warning (slide in top-right, auto-dismiss 4s)
  - [ ] 12.8.2 — Connection status badge: Connected / Reconnecting / Offline
  - [ ] 12.8.3 — Per-message feedback: 👍/👎 → emit feedback event to Phase 11
  - [ ] 12.8.4 — Error messages with retry button
  - [ ] 12.8.5 — Session timeout warning with extend option

- [ ] **12.9** — `app/server.py` — Web UI entry point

- [ ] **12.10** — Test Web UI
  - [ ] 12.10.1 — WebSocket connect + reconnect on drop
  - [ ] 12.10.2 — Streaming response renders without flicker
  - [ ] 12.10.3 — Arabic RTL display correct for Arabic messages
  - [ ] 12.10.4 — File upload → preview → send → tool receives correct path
  - [ ] 12.10.5 — Settings persist across browser reload
  - [ ] 12.10.6 — Conversation CRUD (create, rename, pin, archive, delete)
  - [ ] 12.10.7 — Responsive layout on 375px / 768px / 1440px

- [ ] **12.11** — System Dashboard panel (Web UI)
  - [ ] 12.11.1 — Real-time VRAM meter: poll `/api/status` every 2s; progress bar
  - [ ] 12.11.2 — Active tool panel: show tool name + status (running/done/failed)
  - [ ] 12.11.3 — Task queue viewer: pending/running/completed decomposition tasks
  - [ ] 12.11.4 — Memory browser: search long-term memory from Web UI
  - [ ] 12.11.5 — System status card: CPU%, RAM, disk, GPU — live update

### Voice Pipeline

- [ ] **12.12** — `src/models/speech/stt.py` — Speech-to-Text (Whisper)
  - [ ] 12.12.1 — Load `whisper medium` model on demand (CPU or CUDA)
  - [ ] 12.12.2 — `record_audio()` — capture from default microphone
  - [ ] 12.12.3 — `transcribe(audio_array)` → `{text, language, confidence}`
  - [ ] 12.12.4 — Auto-detect language (Arabic vs English)
  - [ ] 12.12.5 — Handle background noise (normalize audio before transcription)

- [ ] **12.13** — `src/models/speech/tts.py` — Text-to-Speech (Piper)
  - [ ] 12.13.1 — Load Piper Arabic voice model (`ar_JO-kareem-medium.onnx`)
  - [ ] 12.13.2 — Load Piper English voice model
  - [ ] 12.13.3 — `synthesize(text, lang) → audio_bytes`
  - [ ] 12.13.4 — `play(audio_bytes)` — play via sounddevice
  - [ ] 12.13.5 — Language auto-select from STT detected language

- [ ] **12.14** — `src/interfaces/voice/wake_word.py` — Wake Word listener
  - [ ] 12.14.1 — Load openWakeWord `hey_jarvis` model
  - [ ] 12.14.2 — Continuous mic monitoring on background thread
  - [ ] 12.14.3 — Trigger: score > 0.5 on `hey_jarvis`
  - [ ] 12.14.4 — Emit `on_wake_word` event on EventBus
  - [ ] 12.14.5 — Visual feedback (CLI status indicator) + audio chime on detection

- [ ] **12.15** — `src/interfaces/voice/voice_interface.py` — full voice pipeline
  - [ ] 12.15.1 — Wait for wake word → start recording
  - [ ] 12.15.2 — VAD-based auto-stop: end recording when silence detected (12.16)
  - [ ] 12.15.3 — Transcribe via Whisper → pass text to orchestrator
  - [ ] 12.15.4 — Synthesize LLM response via Piper → play audio
  - [ ] 12.15.5 — Return to listening state

- [ ] **12.16** — Voice Activity Detection (VAD)
  - [ ] 12.16.1 — Use `webrtcvad` for frame-level speech detection
  - [ ] 12.16.2 — Configurable silence threshold and min/max recording duration
  - [ ] 12.16.3 — Auto-stop when N consecutive silent frames detected
  - [ ] 12.16.4 — Replaces fixed-duration recording completely

- [ ] **12.17** — Mid-sentence language detection
  - [ ] 12.17.1 — Extract detected language from Whisper output
  - [ ] 12.17.2 — Select TTS voice based on detected language
  - [ ] 12.17.3 — Handle code-switching (Arabic sentence with English terms) gracefully

- [ ] **12.18** — Test voice pipeline
  - [ ] 12.18.1 — Wake word detection: say "Hey Jarvis" → pipeline activates
  - [ ] 12.18.2 — Arabic STT accuracy: record Arabic phrase → correct transcription
  - [ ] 12.18.3 — TTS output: synthesize and play Arabic response without artifacts
  - [ ] 12.18.4 — Full cycle: wake → speak → transcribe → LLM → TTS → play

### Vision & Image Generation

- [ ] **12.19** — `src/models/vision/engine.py` — image understanding (LLaVA)
  - [ ] 12.19.1 — Load LLaVA via Ollama (model: `llava:7b`)
  - [ ] 12.19.2 — `describe(image_path, question) → str`
  - [ ] 12.19.3 — Encode image as base64 for Ollama vision API
  - [ ] 12.19.4 — OCR capability: "read the text in this image"
  - [ ] 12.19.5 — VRAM guard: unload text LLM before loading LLaVA

- [ ] **12.20** — `src/models/diffusion/generator.py` — image generation (SD 1.5)
  - [ ] 12.20.1 — Load Stable Diffusion 1.5 with `torch.float16` (fits in 4GB VRAM)
  - [ ] 12.20.2 — `generate(prompt, width=512, height=512, steps=20) → PIL.Image`
  - [ ] 12.20.3 — VRAM management: unload LLM before loading SD; reload after
  - [ ] 12.20.4 — Save output to `data/generated_images/` with timestamp filename
  - [ ] 12.20.5 — Negative prompt support for quality control

- [ ] **12.21** — Arabic prompt translation for image generation
  - [ ] 12.21.1 — Detect Arabic prompt text
  - [ ] 12.21.2 — Translate to English via LLM before passing to SD (SD trained on English)
  - [ ] 12.21.3 — Return generated image + translated prompt as context

- [ ] **12.22** — Integrate vision into orchestrator + router
  - [ ] 12.22.1 — Detect image attached to message (via context buffer)
  - [ ] 12.22.2 — Auto-route to vision engine; VRAM guard fires
  - [ ] 12.22.3 — Combine vision description with LLM response in single answer

- [ ] **12.23** — Test vision pipeline
  - [ ] 12.23.1 — Image description: upload test image → LLaVA describes it in Arabic
  - [ ] 12.23.2 — Image generation: Arabic prompt → translated → SD → image saved + displayed
  - [ ] 12.23.3 — OCR: test image with Arabic text → extracted correctly

---

## 📱 Phase 13 — Telegram Interface
> **Goal:** Full Jarvis assistant accessible via Telegram: text, photos, voice notes, documents — all handled correctly.
> **Definition of done:** Send a voice note in Arabic → Jarvis transcribes it, answers via text (and optionally audio).
> **Dependency:** Phase 12 (voice pipeline for voice message handling); Phase 8 (APIs callable from Telegram commands).

- [ ] **13.1** — `src/interfaces/telegram/bot.py` — bot setup
  - [ ] 13.1.1 — Initialize `python-telegram-bot` Application
  - [ ] 13.1.2 — Register all handlers
  - [ ] 13.1.3 — Start polling with timeout from config

- [ ] **13.2** — `src/interfaces/telegram/handlers.py` — message handlers
  - [ ] 13.2.1 — Text message → orchestrator → reply (with typing action)
  - [ ] 13.2.2 — Photo → download → vision engine → text reply
  - [ ] 13.2.3 — Voice note → download → STT → orchestrator → text reply (optionally TTS)
  - [ ] 13.2.4 — Document → download → reader tool (PDF/Office) → summary reply

- [ ] **13.3** — `src/interfaces/telegram/commands.py` — bot commands
  - [ ] 13.3.1 — `/start` — welcome + capability overview
  - [ ] 13.3.2 — `/clear` — clear conversation history
  - [ ] 13.3.3 — `/model [name]` — switch model
  - [ ] 13.3.4 — `/image [prompt]` — generate image and send back
  - [ ] 13.3.5 — `/search [query]` — web search + send results

- [ ] **13.4** — Streaming simulation for Telegram
  - [ ] 13.4.1 — Send "Typing..." action while generating
  - [ ] 13.4.2 — Edit message progressively as tokens arrive (Telegram edit API)

- [ ] **13.5** — Media handling
  - [ ] 13.5.1 — Download Telegram photos/files to temp dir; pass to tools
  - [ ] 13.5.2 — Send generated images back to user

- [ ] **13.6** — Test Telegram bot
  - [ ] 13.6.1 — Arabic text conversation end-to-end
  - [ ] 13.6.2 — Photo upload → vision description
  - [ ] 13.6.3 — Voice note → transcription → answer

---

## 🖼️ Phase 14 — GUI Desktop App + System Tray
> **Goal:** Native PyQt6 desktop window with chat UI, Arabic RTL, voice input button, and full system tray integration.
> **Definition of done:** App launches from tray icon; user chats in Arabic or English; window hides to tray on minimize; wake word from background activates window.
> **Dependency:** Phase 4 (CLI patterns to reuse); Phase 12 (voice integration).

- [ ] **14.1** — `src/interfaces/gui/main_window.py` — PyQt6 main window
  - [ ] 14.1.1 — Scrollable chat message area with bubble-style messages
  - [ ] 14.1.2 — Auto-expanding input text box
  - [ ] 14.1.3 — Send button + microphone button
  - [ ] 14.1.4 — Model selector dropdown (populated from `ollama list`)
  - [ ] 14.1.5 — Mode selector toolbar: fast / normal / deep / planning / research

- [ ] **14.2** — `src/interfaces/gui/settings_dialog.py` — settings window
  - [ ] 14.2.1 — Model selection
  - [ ] 14.2.2 — Language preference (Arabic / English / Auto)
  - [ ] 14.2.3 — Voice settings: microphone device, TTS speed
  - [ ] 14.2.4 — Theme: Dark / Light
  - [ ] 14.2.5 — Startup behavior: tray / window

- [ ] **14.3** — Arabic RTL text rendering
  - [ ] 14.3.1 — `Qt.RightToLeft` layout direction for Arabic messages
  - [ ] 14.3.2 — Per-message direction detection

- [ ] **14.4** — System tray integration
  - [ ] 14.4.1 — Minimize to tray (hide main window, keep tray icon)
  - [ ] 14.4.2 — Tray right-click menu: Open / Settings / Quit
  - [ ] 14.4.3 — Wake word detection activates window from tray
  - [ ] 14.4.4 — Windows Toast from 6.6 shown when window minimized

- [ ] **14.5** — Clipboard integration in GUI
  - [ ] 14.5.1 — "Analyze clipboard" button: read clipboard → send to Jarvis
  - [ ] 14.5.2 — Auto-detect type: code / URL / text / image

- [ ] **14.6** — Auto-start on Windows login
  - [ ] 14.6.1 — Add/remove registry key `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`
  - [ ] 14.6.2 — Controlled via settings toggle

- [ ] **14.7** — Test GUI
  - [ ] 14.7.1 — Launch, type Arabic message, receive response — RTL correct
  - [ ] 14.7.2 — Minimize to tray → tray icon appears → double-click → window restores
  - [ ] 14.7.3 — Settings dialog opens and saves correctly

---

## ✅ Phase 15 — QA + Optimization + Security
> **Goal:** Production-hardened system: comprehensive tests, performance profiling, Windows compatibility verified, security review complete.
> **Definition of done:** All end-to-end scenarios pass; VRAM stays within 5.5GB; no credentials appear in logs; CI runs green.
> **Dependency:** All phases feature-complete.

- [ ] **15.1** — Test suite (`tests/`)
  - [ ] 15.1.1 — `test_llm.py` — engine streaming, retry, VRAM guard
  - [ ] 15.1.2 — `test_memory.py` — short/long term, cross-session, Redis fallback
  - [ ] 15.1.3 — `test_tools.py` — registry discovery, schema validation, execute + result
  - [ ] 15.1.4 — `test_voice.py` — STT transcription, TTS synthesis, VAD
  - [ ] 15.1.5 — `test_vision.py` — LLaVA describe, SD generate
  - [ ] 15.1.6 — `test_runtime.py` — loop iterations, escalation, fallback, timeouts
  - [ ] 15.1.7 — `test_identity.py` — prompt builder output consistency across model swaps
  - [ ] 15.1.8 — `test_context_buffer.py` — buffer lifecycle, TTL eviction, Act-phase resolution
  - [ ] 15.1.9 — `test_agents.py` — planner decomposition, ReAct loop, screen agent guard

- [ ] **15.2** — Performance optimization
  - [ ] 15.2.1 — Profile all phases with `cProfile` / `py-spy`; identify top-3 bottlenecks
  - [ ] 15.2.2 — Model preloading strategy: keep most-used model warm; unload on inactivity timeout
  - [ ] 15.2.3 — Response caching: TTL-based cache for identical queries within session
  - [ ] 15.2.4 — Async I/O: all file, DB, Redis, HTTP operations fully async
  - [ ] 15.2.5 — ChromaDB: batched embedding ingestion to prevent RAM spikes on large documents
  - [ ] 15.2.6 — Context compression: auto-summarize mid-history beyond token budget
  - [ ] 15.2.7 — Tool parallelism: independent I/O tools run concurrently (Phase 5.5)
  - [ ] 15.2.8 — Flash Attention: enable via Ollama CUDA options for deep/planning modes
  - [ ] 15.2.9 — KV cache management: dynamic context window based on real-time VRAM

- [ ] **15.3** — Error handling and resilience
  - [ ] 15.3.1 — Graceful Ollama connection failure (retry + fallback message)
  - [ ] 15.3.2 — Model loading failure: fallback to smaller model
  - [ ] 15.3.3 — Tool execution error: structured error → observation → LLM retry
  - [ ] 15.3.4 — Redis failure: in-memory fallback (no crash)
  - [ ] 15.3.5 — ChromaDB failure: long-term memory disabled gracefully

- [ ] **15.4** — Logging and monitoring
  - [ ] 15.4.1 — Structured JSON logging via Loguru to `logs/jarvis.log` (daily rotation)
  - [ ] 15.4.2 — Log every model call with: model, mode, tokens, latency_ms, cost estimate
  - [ ] 15.4.3 — Log every tool execution with: tool, args_hash, result_summary, duration_ms
  - [ ] 15.4.4 — Log every error with full stack trace + session context

- [ ] **15.5** — Windows 11 compatibility
  - [ ] 15.5.1 — All features tested on clean Windows 11 + PowerShell 7
  - [ ] 15.5.2 — Path handling: consistent `pathlib.Path` throughout; no hardcoded separators
  - [ ] 15.5.3 — Audio device detection on Windows (correct device index)
  - [ ] 15.5.4 — `scripts/install.ps1` tested on clean VM

- [ ] **15.6** — Security review
  - [ ] 15.6.1 — Code execution sandbox: blocklist dangerous patterns; subprocess isolation
  - [ ] 15.6.2 — Input validation: all tool args validated before execution (schema enforcement)
  - [ ] 15.6.3 — Credentials: `.env` and `data/google_token.json` never logged; gitignored
  - [ ] 15.6.4 — Browser sessions: `data/sessions/*.json` encrypted at rest with Fernet key from `.env`
  - [ ] 15.6.5 — Prompt injection guard: sanitize user input before injecting into system prompts

- [ ] **15.7** — Documentation
  - [ ] 15.7.1 — README.md finalized with accurate Quick Start for current state
  - [ ] 15.7.2 — Docstrings on all public functions and classes
  - [ ] 15.7.3 — TASKS.md progress table updated to reflect actual completion

- [ ] **15.8** — End-to-end scenario tests
  - [ ] 15.8.1 — Full Arabic conversation: voice → STT → LLM → TTS → spoken answer
  - [ ] 15.8.2 — "Send email to [contact] and add Calendar reminder" → Gmail + Calendar
  - [ ] 15.8.3 — "Open Notepad, type test, save to Desktop" → app + keyboard + file tool
  - [ ] 15.8.4 — "Search YouTube for X, open first result" → search + browser
  - [ ] 15.8.5 — Multi-agent: research + summarize + save to Drive

- [ ] **15.9** — Continuous integration
  - [ ] 15.9.1 — GitHub Actions: lint (ruff) + type check (mypy) + pytest on push
  - [ ] 15.9.2 — Code coverage report (minimum 70%)
  - [ ] 15.9.3 — Pre-commit hooks: ruff format + import sort

- [ ] **15.10** — Phase 6–8 skill integration tests
  - [ ] 15.10.1 — Open app → window active → close app (Windows)
  - [ ] 15.10.2 — Browser session: login → restart Jarvis → verify session reloaded
  - [ ] 15.10.3 — Gmail + Calendar same OAuth token (no double consent)
  - [ ] 15.10.4 — Clipboard read → LLM process → write back result
  - [ ] 15.10.5 — Windows Toast appears and is acknowledged

- [ ] **15.11** — Security hardening for system control tools
  - [ ] 15.11.1 — Confirm-before-execute gates: delete file, kill process, send email, shell command
  - [ ] 15.11.2 — Shell allowlist: reject patterns matching `rm -rf`, `format`, `del /s /q`
  - [ ] 15.11.3 — Google OAuth token: only in `data/` (gitignored); never in `config/`

- [ ] **15.12** — Performance benchmarks
  - [ ] 15.12.1 — Cold start time: < 10s from `python app/main.py` to first response ready
  - [ ] 15.12.2 — VRAM peak: never exceeds 5.5GB during normal operation
  - [ ] 15.12.3 — Simple response latency: < 5s for `gemma3:4b` fast-mode answer
  - [ ] 15.12.4 — Voice pipeline round-trip: wake word → spoken response < 15s total

---

## 🎭 Phase 16 — Personality Layer
> **Goal:** Consistent Jarvis voice across all interfaces — adapts tone and style to user preferences while maintaining safety and capability constraints.
> **Definition of done:** After 10 sessions preferring concise answers, Jarvis automatically reduces response length without being told. Arabic vs English tone feels native, not translated.
> **Dependency:** All phases complete. This layer overlays everything else — it is the last thing applied before output.

- [ ] **16.1** — Tone control
  - [ ] 16.1.1 — Tone modes: formal / casual / warm / technical — configurable per user
  - [ ] 16.1.2 — Locale-aware: Arabic responses feel culturally natural; English responses feel direct
  - [ ] 16.1.3 — User override: `/profile tone=casual` or settings dialog

- [ ] **16.2** — Response style
  - [ ] 16.2.1 — Length presets: concise / balanced / detailed (learnable from feedback)
  - [ ] 16.2.2 — Format preference: bullet lists vs prose vs mixed
  - [ ] 16.2.3 — "Teacher mode" (explain with examples) vs "executive summary" (brief with action)

- [ ] **16.3** — Adaptive personality
  - [ ] 16.3.1 — Drift slowly from Phase 11 feedback signals + explicit preference changes
  - [ ] 16.3.2 — Bounded deltas per update (prevent jarring personality shifts)
  - [ ] 16.3.3 — Audit log: all personality parameter changes with timestamp and trigger

- [ ] **16.4** — Integration
  - [ ] 16.4.1 — Inject Personality fragments into System Prompt Builder (3.17) as the last layer
  - [ ] 16.4.2 — Router still picks model by capability; personality does not affect routing
  - [ ] 16.4.3 — Safety constraints: personality never overrides refusals or tool policies

- [ ] **16.5** — Tests
  - [ ] 16.5.1 — A/B prompt fixtures: same query, different personality settings → verify output style difference
  - [ ] 16.5.2 — Regression: safety refusals still occur regardless of personality settings
  - [ ] 16.5.3 — Arabic/English tone: verify native feel in both languages

---

## 📌 Notes

### Model Inventory (current — verify with `ollama list`)
```
gemma3:4b          — Fast / lightweight; tight latency or low complexity; 3.0 GB VRAM
qwen3:8b           — Main brain: general / deep reasoning / Arabic; 5.0 GB VRAM
qwen2.5-coder:7b   — Code + execution tasks; 4.7 GB VRAM
llava:7b           — Vision tasks; 4.5 GB VRAM
```
> `qwen2.5:7b` removed permanently — superseded by `qwen3:8b` in all capability profiles. Delete from `config/models.yaml`.

### VRAM Budget (6 GB RTX 3050)
```
Rule: one heavy model at a time; unload before swapping; SD requires LLM unload first.

qwen3:8b         ~5.0 GB  — main brain
qwen2.5-coder:7b ~4.7 GB  — code tasks
llava:7b         ~4.5 GB  — vision (unload text LLM first)
gemma3:4b        ~3.0 GB  — fast responses (can coexist with some tools)
SD 1.5 float16   ~4.0 GB  — image gen (unload everything else first)
```

### New Skill/Schema Files Required
```
config/schemas/control/apps.schema.json        — app launcher
config/schemas/control/clipboard.schema.json   — clipboard read/write
config/schemas/notify/notifications.schema.json — Windows toast
config/schemas/screen/screenshot.schema.json   — screen capture
config/schemas/screen/ocr.schema.json          — OCR text extraction
config/schemas/browser/browser.schema.json     — browser automation
config/schemas/browser/session.schema.json     — session management
config/schemas/browser/download.schema.json    — file download
config/schemas/browser/upload.schema.json      — file upload
config/schemas/social/whatsapp.schema.json     — WhatsApp Web
config/schemas/api/gmail.schema.json           — Gmail
config/schemas/api/google_drive.schema.json    — Google Drive
config/schemas/api/google_contacts.schema.json — Contacts
config/schemas/reader/pdf.schema.json          — PDF reader
config/schemas/reader/office.schema.json       — Office reader/writer
```

### Windows-Specific Dependencies (add to requirements.txt)
```
pywin32>=306        — Windows API: window control, registry, COM
pycaw>=0.4.3        — Windows audio API (volume control)
pystray>=0.19       — System tray icon
winotify>=1.1.3     — Windows Toast notifications
pyperclip>=1.9.0    — Cross-platform clipboard (text)
pynput>=1.7.6       — Global keyboard/mouse listener
keyboard>=0.13.5    — Global hotkey registration (Windows)
mss>=9.0.1          — Fast multi-monitor screen capture
pytesseract>=0.3.13 — Tesseract OCR Python wrapper
send2trash>=1.8.2   — Safe file delete (to recycle bin)
win32com            — bundled with pywin32; used for .lnk parsing
```

### Phase Dependency Map
```
Phase 1 (Foundation)           ← no dependencies
Phase 2 (Runtime + LLM)        ← Phase 1
Phase 3 (Memory + Identity)    ← Phase 1, 2
Phase 4 (CLI)                  ← Phase 1, 2, 3
Phase 5 (Tool Registry)        ← Phase 2, 3
Phase 6 (System Control)       ← Phase 5
Phase 7 (Browser + Web)        ← Phase 5, 6
Phase 8 (External APIs)        ← Phase 5, 7
Phase 9 (Agents)               ← Phase 5, 6, 7, 8
Phase 10 (Decomposition)       ← Phase 9
Phase 11 (Feedback)            ← Phase 9, 10, 3
Phase 12 (Web + Voice + Vision) ← Phase 1–11
Phase 13 (Telegram)            ← Phase 12
Phase 14 (GUI)                 ← Phase 4, 12
Phase 15 (QA)                  ← All phases complete
Phase 16 (Personality)         ← All phases complete
```

### Priority Order for Active Development
```
1. Phase 1 — Foundation (skeleton + config)
2. Phase 2 — Runtime + LLM (core loop)
3. Phase 3 — Memory + Identity (context + persistence)
4. Phase 4 — CLI (test loop fast without a browser)
5. Phase 5 — Tool Registry (prerequisite for all skills)
6. Phase 6 — System Control (real computer use begins here)
7. Phase 7 — Browser + Web (automation + sessions)
8. Phase 8 — External APIs (Google suite)
9. Phase 9 — Agents (autonomy layer)
10. Phase 10 — Decomposition (complex multi-step goals)
11. Phase 11 — Feedback (learning loop)
12. Phase 12 — Web + Voice + Vision (premium interfaces)
13. Phase 13 — Telegram
14. Phase 14 — GUI Desktop
15. Phase 15 — QA + Security
16. Phase 16 — Personality
```

---

*Last updated: 2026-04-19 — Version 0.3.0-alpha — Production foundation release*
*All 16 phases defined. All missing capabilities added. All dependencies mapped. Build order locked.*
