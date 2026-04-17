# 🗂️ JARVIS — Task Board
> Full development roadmap from zero to complete system
> Update checkboxes as you complete each task
> **Phase order:** Foundation → Runtime + Decision → Memory (incl. Context Buffer + Identity & Profiles) → CLI → Tool System → Basic Agents → Task Decomposition → Feedback & Learning → Web / Voice / Vision → Integrations → Optimization & QA → Personality
> **Intelligence is cross-cutting:** systems below are wired together — **feedback → memory** (signals update profiles and priors); **memory → decision** (preferences, failures, patterns); **decision → routing** (mode, model, tools); **runtime → evaluation** (turn outcomes feed self-eval, escalation, and feedback); **context buffer → observe → decision** (staged multimodal inputs before heavy work); **identity & profiles → every model call** (Jarvis + user + task context — models are **components**, not standalone products).
> **Repo layout:** YAML under `config/`; Python settings (loader, Pydantic, paths, logging) under `settings/` — see [README.md](./README.md) (Project Structure).

---

## 🔗 System Integration (non-optional)

- **Feedback & Learning** ↔ **Adaptive Memory:** implicit signals and explicit outcomes update user profile, tool/model priors, and recall of "what worked."
- **Adaptive Memory** ↔ **Decision Layer:** retrieved facts + profile bias intent, complexity, mode, and confidence priors.
- **Decision Layer** ↔ **Model Router:** `DecisionOutput` + memory context → model selection and mode packs; Error Intelligence can override (retry / switch model / switch mode).
- **Runtime loop** ↔ **Self-Evaluation:** Evaluate stage consumes structured signals; persistence enables resume and long-running tracking.
- **Task Decomposition** ↔ **Parallel execution:** execution graph schedules concurrent steps where dependencies allow; failures map to error class + selective retry.
- **Personality Layer** ↔ **prompts + memory:** tone/style constraints compose with mode packs and learned preferences (without breaking safety caps).
- **Context Buffer** ↔ **Runtime (Observe)** ↔ **Decision** ↔ **Tools:** interfaces enqueue text/files/images/audio into a staging layer; Observe reads a merged snapshot; Decision uses that as the primary input signal; heavy models and tool-side readers run only after Decide (buffer remains preparation-only).
- **Identity & Profiles** ↔ **Memory** ↔ **Decision** ↔ **Runtime** ↔ **Context Buffer:** user profile + Jarvis system identity feed Observe and Decision priors; system prompt builder ensures every model sees who Jarvis is, who the user is, and shared conversation/tool state — consistent behavior across all routed models.

> **Phase order rationale:**
> - CLI first (Phase 4) = fastest feedback loop, no frontend complexity
> - Tool system (Phase 5) = prerequisite for everything else — agents need tools, APIs need registry
> - System Control (Phase 6) + Browser (Phase 7) = core "computer use" skills, built on tool registry
> - External APIs (Phase 8) = depends on tool registry (Phase 5)
> - Agents (Phase 9) = need tools (5,6,7) and APIs (8) to be useful
> - Task Decomposition (Phase 10) = extends agents, needs agents first
> - Feedback (Phase 11) = closes the loop, needs agents + tools working
> - Multimodal surfaces (Phase 12) = Web/Voice/Vision — highest value, built on top of everything
> - Telegram (Phase 13) + GUI (Phase 14) = extra interfaces, lower priority than core function
> - QA (Phase 15) = after feature-complete
> - Personality (Phase 16) = polish last


---
## 📊 Progress Overview

| Phase | Tasks | Done | Progress |
|-------|-------|------|----------|
| Phase 1: Foundation | 8 | 8 | ██████████ 100% |
| Phase 2: LLM + Runtime + Decision | 26 | 22 | █████████░ 85% |
| Phase 3: Memory + Context Buffer + Identity | 20 | 20 | ██████████ 100% |
| Phase 4: CLI Interface | 8 | 0 | ░░░░░░░░░░ 0% |
| Phase 5: Tool System | 7 | 0 | ░░░░░░░░░░ 0% |
| Phase 6: System Control Skills | 9 | 0 | ░░░░░░░░░░ 0% |
| Phase 7: Browser & Web Skills | 9 | 0 | ░░░░░░░░░░ 0% |
| Phase 8: External APIs & Integrations | 9 | 0 | ░░░░░░░░░░ 0% |
| Phase 9: Agents | 8 | 0 | ░░░░░░░░░░ 0% |
| Phase 10: Task Decomposition Engine | 9 | 0 | ░░░░░░░░░░ 0% |
| Phase 11: Feedback & Learning | 9 | 0 | ░░░░░░░░░░ 0% |
| Phase 12: Web UI + Voice + Vision | 23 | 0 | ░░░░░░░░░░ 0% |
| Phase 13: Telegram Interface | 6 | 0 | ░░░░░░░░░░ 0% |
| Phase 14: GUI Desktop App | 7 | 0 | ░░░░░░░░░░ 0% |
| Phase 15: QA + Optimization + Security | 12 | 0 | ░░░░░░░░░░ 0% |
| Phase 16: Personality Layer | 5 | 0 | ░░░░░░░░░░ 0% |

---
## 🏗️ Phase 1 — Foundation & Project Setup
> **Goal:** Working project skeleton, config system, logging, and base classes

- [x] **1.1** — Create `config/settings.yaml` with all app settings (models, interfaces, hardware limits)
  - [x] 1.1.1 — Add Jarvis name, language, wake_word settings
  - [x] 1.1.2 — Add model names that match Ollama pulls: `gemma3:4b` (fast), `qwen3:8b` (general / balanced / deep), `qwen2.5-coder:7b` (coder), `llava:7b` (vision)
  - [x] 1.1.3 — Add interface ports and hosts
  - [x] 1.1.4 — Add storage paths

- [x] **1.2** — Create `config/models.yaml` with model-specific parameters
  - [x] 1.2.1 — Temperature, top_p, max_tokens per model
  - [x] 1.2.2 — Capability profiles (reasoning tier, Arabic quality, code bias, latency, VRAM estimate)
  - [x] 1.2.3 — Optional routing weights / thresholds (tunable without code changes)

- [x] **1.3** — Create `.env.example` with all required environment variables
  - [x] 1.3.1 — TELEGRAM_BOT_TOKEN
  - [x] 1.3.2 — GOOGLE_CLIENT_ID / SECRET
  - [x] 1.3.3 — YOUTUBE_API_KEY

- [x] **1.4** — Create `config/skills.yaml` — tool/skill registry (enable/disable, categories) and pointers to JSON schemas

- [x] **1.5** — Setup `requirements.txt` — complete and pinned dependencies
  - [x] 1.5.1 — Core: ollama, fastapi, uvicorn, pydantic
  - [x] 1.5.2 — Memory: chromadb, redis, sqlite3
  - [x] 1.5.3 — Audio: openai-whisper, piper-tts, openwakeword, pyaudio, sounddevice
  - [x] 1.5.4 — Vision: diffusers, torch, torchvision, Pillow
  - [x] 1.5.5 — Tools/skills: playwright, psutil, pyautogui, google-api-python-client
  - [x] 1.5.6 — Interfaces: python-telegram-bot, rich, PyQt6
  - [x] 1.5.7 — Utils: loguru, pyyaml, python-dotenv, sentence-transformers

- [x] **1.6** — Create `app/main.py` — entry point with `--interface` argument parser
  - [x] 1.6.1 — Parse CLI args: `--interface [cli|web|telegram|gui|all]`
  - [x] 1.6.2 — Initialize logging with Loguru
  - [x] 1.6.3 — Load config from settings.yaml
  - [x] 1.6.4 — Launch selected interface(s)

- [x] **1.7** — Setup installation scripts — full automated installation
  - [x] 1.7.1 — `scripts/install.sh` — Linux/WSL: system packages, venv, pip, Playwright, Ollama model pulls
  - [x] 1.7.2 — `scripts/install.ps1` — Windows: Ollama install, model pulls, venv, pip, Playwright
  - [x] 1.7.3 — Whisper model download instructions
  - [x] 1.7.4 — Piper voice download instructions
  - [x] 1.7.5 — openWakeWord model download instructions

- [x] **1.8** — Clean up project skeleton
  - [x] 1.8.1 — Rename `core/agents/New folder/` → `core/agents/extensions/`
  - [x] 1.8.2 — Create placeholder `__init__.py` in all core subdirs (including `core/runtime/` skeleton)
  - [x] 1.8.3 — Verify all `__init__.py` export correct public API symbols

---

## 🧠 Phase 2 — LLM Engine, Model Router, Decision Layer & Runtime
> **Goal:** Ollama access, adaptive routing via Decision Layer + confidence + cost estimates + memory-informed priors, VRAM-safe swaps, Evaluate → Escalate|Finish, and the Observe → Decide → Think → Act → Evaluate loop. Extend with Error Intelligence (2.23), Self-Evaluation (2.24), and Persistent Runtime State (2.25).

- [x] **2.1** — Create `models/llm/engine.py` — base Ollama interface
  - [x] 2.1.1 — `chat(messages, model)` — streaming + non-streaming
  - [x] 2.1.2 — `generate(prompt, model)` — single completion
  - [x] 2.1.3 — Handle connection errors + retry logic
  - [x] 2.1.4 — Support Arabic system prompts

- [x] **2.2** — Create `models/llm/router.py` — dynamic model selector
  - [x] 2.2.1 — Ingest DecisionOutput + capability profiles + modalities + cost_estimate
  - [x] 2.2.2 — Score candidate models by intent fit, complexity, mode, latency, reasoning ceiling
  - [x] 2.2.3 — Prefer coder profile when code/execution signals dominate; vision when pixels present
  - [x] 2.2.4 — Prefer fast profile (`gemma3`) when complexity low + mode `fast` + latency tight
  - [x] 2.2.5 — Prefer deep profile (`qwen3`) when complexity high or mode `deep` / escalation
  - [x] 2.2.6 — Default balanced profile when no stronger signal wins
  - [x] 2.2.7 — VRAM guard — only one heavy Ollama model at a time; serialize swaps
  - [x] 2.2.8 — Expose override hooks (user / interface) without bypassing safety caps

- [x] **2.3** — Create `models/llm/prompts.py` — system prompt templates
  - [x] 2.3.1 — Jarvis Arabic personality prompt
  - [x] 2.3.2 — Jarvis English personality prompt
  - [x] 2.3.3 — Code-mode system prompt
  - [x] 2.3.4 — Planning-mode system prompt
  - [x] 2.3.5 — Mode packs — composable fragments for fast / normal / deep / planning / research

- [x] **2.4** — Create `core/runtime/runtime_manager.py` — session lifecycle, turn orchestration
  - [x] 2.4.1 — Start/end "run" per user turn; hook interfaces → brain
  - [x] 2.4.2 — Enforce max loop iterations and timeouts
  - [x] 2.4.3 — Coordinate with model router for VRAM

- [x] **2.5** — Create `core/runtime/state/` — conversation + run state
  - [x] 2.5.1 — Track messages, pending tool calls, step index
  - [x] 2.5.2 — Serializable snapshots for debugging

- [x] **2.6** — Create `core/runtime/loop/` — Observe → Decide → Think → Act → Evaluate driver
  - [x] 2.6.1 — Observe: ingest user input + tool results + memory snippets
  - [x] 2.6.2 — Decide: run Decision Layer; inject mode + budgets + prior confidence
  - [x] 2.6.3 — Think: call LLM via dynamic router + mode-appropriate prompts
  - [x] 2.6.4 — Act: delegate to executor stub (no-op until Phase 5)
  - [x] 2.6.5 — Evaluate: compute posterior confidence + answer quality
  - [x] 2.6.6 — Branch: Finish OR Escalate (bounded)
  - [x] 2.6.7 — Failure: surface errors as observations; fallback safe response
  - [x] 2.6.8 — Context Buffer: Observe reads from buffer snapshot when active
  - [x] 2.6.9 — Merge multiple buffered inputs into one unified observation
  - [x] 2.6.10 — Pass merged bundle to Decision Layer as structured input

- [x] **2.7** — Create `core/runtime/executor/` — tool execution facade
  - [x] 2.7.1 — Interface for "execute tool(name, args)" with validation hooks
  - [x] 2.7.2 — Policy placeholder (permissions, sandbox flags)

- [x] **2.8** — Create `core/brain/orchestrator.py` — bridges runtime ↔ LLM ↔ memory
  - [x] 2.8.1 — Receive input from any interface via runtime manager
  - [x] 2.8.2 — Detect high-level intent (chat / tool / plan / search)
  - [x] 2.8.3 — Return unified response format (stream-friendly)
  - [x] 2.8.4 — Context Buffer: accept enqueue / commit flows from interfaces

- [x] **2.9** — Create `core/brain/dispatcher.py` — intent → handler
  - [x] 2.9.1 — Map intent → tool or agent path
  - [x] 2.9.2 — Pass context and history
  - [x] 2.9.3 — Handle handler errors gracefully

- [x] **2.10** — Create `core/events/event_bus.py` — pub/sub event system
  - [x] 2.10.1 — Simple async event emitter
  - [x] 2.10.2 — Events: on_message, on_response, on_wake_word, on_error, on_tool_start, on_tool_end, on_decision, on_evaluate, on_escalation

- [x] **2.11** — Create `core/runtime/decision/` — Decision Layer
  - [x] 2.11.1 — Define DecisionOutput schema
  - [x] 2.11.2 — Intent classification
  - [x] 2.11.3 — Complexity estimation
  - [x] 2.11.4 — Time / effort estimation
  - [x] 2.11.5 — Tool necessity detection
  - [x] 2.11.6 — Planning trigger
  - [x] 2.11.7 — Prior confidence
  - [x] 2.11.8 — Cost estimate
  - [x] 2.11.9 — Context Buffer as input source for Decision
  - [x] 2.11.10 — Identity priors from User profile

- [x] **2.12** — Mode controller — bind Thinking Modes to prompt packs + decode params
  - [x] 2.12.1 — Map fast | normal | deep | planning | research → template + parameter set
  - [x] 2.12.2 — Allow same model to switch modes between turns

- [x] **2.13** — Escalation engine
  - [x] 2.13.1 — Triggers: low posterior, incomplete answer, tool failure
  - [x] 2.13.2 — Actions: deeper mode, stronger model, enable planning
  - [x] 2.13.3 — max_escalation_depth + max_iterations + per-step timeouts
  - [x] 2.13.4 — Retry policy — bounded retries with backoff

- [x] **2.14** — Capability profiles — structured metadata per model
  - [x] 2.14.1 — Fields: reasoning strength, Arabic quality, latency tier, code bias, vision, VRAM estimate
  - [x] 2.14.2 — Router reads profiles; weights/thresholds configurable

- [x] **2.15** — Integrate Decision Layer ↔ router ↔ loop
  - [x] 2.15.1 — Decision injects mode + flags before Think; router scores auto model selection
  - [x] 2.15.2 — Mid-loop model switch when escalation fires
  - [x] 2.15.3 — Context Buffer path: end-to-end interface → enqueue → Observe → Decide → Think

- [x] **2.16** — Limits & fallback policy
  - [x] 2.16.1 — Per-turn / per-tool / per-load timeouts
  - [x] 2.16.2 — Safe fallback response when caps hit

- [x] **2.17** — Test LLM + runtime + decision wiring
  - [x] 2.17.1 — Arabic chat with adaptive mode selection
  - [x] 2.17.2 — Code path: verify scoring favors coder profile
  - [x] 2.17.3 — Deep escalation: low-confidence → deeper mode
  - [x] 2.17.4 — Single-GPU constraint + mid-loop swap
  - [x] 2.17.5 — DecisionOutput contract tests

- [x] **2.18** — Confidence system — prior + posterior
  - [x] 2.18.1 — Prior in Decision Layer
  - [x] 2.18.2 — Posterior in Evaluate
  - [x] 2.18.3 — Threshold bands (high/medium/low) as config

- [x] **2.19** — Cost estimation system
  - [x] 2.19.1 — Populate cost_estimate.tokens
  - [x] 2.19.2 — Map model choice + mode → latency / gpu_load tiers
  - [x] 2.19.3 — Router uses cost × quality tradeoff

- [x] **2.20** — Evaluate stage — first-class module
  - [x] 2.20.1 — Inputs: candidate answer, tool traces, DecisionOutput, memory hints
  - [x] 2.20.2 — Outputs: quality score, posterior confidence, stop/escalate recommendation

- [x] **2.21** — Memory-influenced decision — integrate with Phase 3
  - [x] 2.21.1 — Feed user preferences + language bias into Decision
  - [x] 2.21.2 — Track repeated patterns → adjust priors
  - [x] 2.21.3 — Log failures/successes → bias tools/planning
  - [x] 2.21.4 — Define stable interfaces so Phase 2 runs with stubs

- [x] **2.22** — Integration test — confidence + cost + evaluate + escalation
  - [x] 2.22.1 — Low prior → cheap route; high complexity → higher cost
  - [x] 2.22.2 — Posterior low → escalation within depth limit
  - [x] 2.22.3 — Limits hit → fallback path

- [ ] **2.23** — Error Intelligence System — classify failures and drive smart retry
  - [ ] 2.23.1 — Error taxonomy: model_error | tool_error | timeout | invalid_input | unknown
  - [ ] 2.23.2 — Tool error: surface provider/HTTP/schema errors as observations
  - [ ] 2.23.3 — Model error: parse Ollama/LLM failures → observation + class
  - [ ] 2.23.4 — Timeout: distinguish per-step vs global
  - [ ] 2.23.5 — Invalid input: validation before execute; optional repair pass
  - [ ] 2.23.6 — Smart retry strategy: retry same model, switch model, switch mode, decompose
  - [ ] 2.23.7 — Integration: connect to DecisionLayer + router + escalation

- [ ] **2.24** — Self-Evaluation System — extend Evaluate with answer-level checks
  - [ ] 2.24.1 — Completeness check (addresses all sub-questions)
  - [ ] 2.24.2 — Correctness estimation (consistency with tool traces)
  - [ ] 2.24.3 — Hallucination / grounding detection
  - [ ] 2.24.4 — Outputs: merge into Evaluate result
  - [ ] 2.24.5 — Integration: feeds escalation, Feedback (Phase 8), memory

- [ ] **2.25** — Persistent Runtime State — long-lived execution context
  - [ ] 2.25.1 — Execution history: append-only log of runs
  - [ ] 2.25.2 — Resume interrupted tasks
  - [ ] 2.25.3 — Long-running task tracking: background / await_user / polling states
  - [ ] 2.25.4 — Storage: SQLite; align with memory tables
  - [ ] 2.25.5 — Integration: orchestrator + event_bus + feedback hooks

- [ ] **2.26** — Identity-aware LLM invocation — models are never prompted as standalone
  - [ ] 2.26.1 — Route every chat/generate through System Prompt Builder (3.17) + model awareness (3.16)
  - [ ] 2.26.2 — Router + mode controller apply on top of identity layer
  - [ ] 2.26.3 — Regression tests: swap model id; identity remains stable

---

## 💾 Phase 3 — Memory System (incl. Adaptive Memory + Context Buffer + Identity)
> **Goal:** Jarvis remembers conversations and facts across sessions; learned preferences and memory-informed decisions connect to Decision + Router. Identity & Profiles defines who Jarvis is and who the user is for consistent behavior across all models.

- [x] **3.1** — Create `core/memory/short_term.py` — in-session memory
  - [x] 3.1.1 — Store conversation history as list of messages
  - [x] 3.1.2 — Token-aware trimming (keep within context window)
  - [x] 3.1.3 — In-memory backend with optional Redis persistence
  - [x] 3.1.4 — Redis connection management: auto-reconnect, fallback to memory-only on failure
  - [x] 3.1.5 — Configurable max history length and token budget

- [x] **3.2** — Create `core/memory/long_term.py` — persistent semantic memory
  - [x] 3.2.1 — ChromaDB collection for semantic search
  - [x] 3.2.2 — `remember(text, metadata)` — store a fact
  - [x] 3.2.3 — `recall(query, n=5)` — semantic similarity search
  - [x] 3.2.4 — Auto-save important facts from conversations
  - [x] 3.2.5 — Configurable embedding model (default: all-MiniLM-L6-v2)
  - [x] 3.2.6 — Collection lifecycle: create, clear, delete

- [x] **3.3** — Create `core/memory/database.py` — SQLite structured storage
  - [x] 3.3.1 — conversations table (id, role, content, timestamp, session_id)
  - [x] 3.3.2 — facts table (id, content, source, category, created_at)
  - [x] 3.3.3 — tasks table (id, title, status, priority, created_at, updated_at)
  - [x] 3.3.4 — Schema auto-creation on init
  - [x] 3.3.5 — CRUD operations with parameterized queries

- [x] **3.4** — Create `core/memory/manager.py` — unified memory interface
  - [x] 3.4.1 — `save_interaction(role, content, session_id)`
  - [x] 3.4.2 — `get_context(n_messages)` — for LLM context window
  - [x] 3.4.3 — `search(query)` — search all memory types (short + long + database)
  - [x] 3.4.4 — Lazy initialization of backends (only connect when first needed)

- [x] **3.5** — Integrate memory into orchestrator + runtime Observe step
  - [x] 3.5.1 — Auto-inject relevant memories into LLM context
  - [x] 3.5.2 — Auto-save each interaction after turn completion

- [x] **3.6** — Test memory system
  - [x] 3.6.1 — Store and retrieve conversation
  - [x] 3.6.2 — Semantic search test
  - [x] 3.6.3 — Cross-session memory persistence test

- [x] **3.7** — User profiling (adaptive memory) — `core/memory/user_profile.py`
  - [x] 3.7.1 — Preferred language (primary UI/response language)
  - [x] 3.7.2 — Preferred response style (concise vs verbose, formal vs casual)
  - [x] 3.7.3 — Common tasks / intents (recurring patterns for Decision Layer priors)
  - [x] 3.7.4 — JSON file storage keyed by user/session; versioned updates

- [x] **3.8** — Memory-driven decisions — close the loop with Phase 2
  - [x] 3.8.1 — Influence model selection (boost/penalize profiles per task pattern)
  - [x] 3.8.2 — Influence thinking mode (bias toward fast vs deep from history)
  - [x] 3.8.3 — Integration: memory.manager exposes hooks consumed by Decision (2.11)

### Context Buffer System (temporary input staging)
> **Goal:** Multimodal staging before execution — accept multiple inputs per turn; temporarily hold text, files, images, and audio references; provide lightweight context for Observe and Decision; no heavy models in this layer.

- [x] **3.9** — Create `core/context/buffer.py` — Context Buffer module
  - [x] 3.9.1 — Temporary storage for user inputs until commit / execute
  - [x] 3.9.2 — Allow multiple inputs to accumulate before the runtime run
  - [x] 3.9.3 — Support text, files (PDF, Office), images, audio (store paths, handles — no inference here)

- [x] **3.10** — Input registration
  - [x] 3.10.1 — Assign a stable `input_id` per item
  - [x] 3.10.2 — Track input type (text | file | image | audio)
  - [x] 3.10.3 — Timestamp each entry (ordering, TTL, debugging)

- [x] **3.11** — Lightweight preprocessing (preparation only)
  - [x] 3.11.1 — Basic parsing for text: normalize whitespace, optional chunking
  - [x] 3.11.2 — File metadata: size, extension, mime detection
  - [x] 3.11.3 — Extract cheap metadata only (image dimensions, page count); no heavy models

- [x] **3.12** — Buffer lifecycle
  - [x] 3.12.1 — Clear after successful execute / turn completion
  - [x] 3.12.2 — Persist for session: in-memory with optional backing
  - [x] 3.12.3 — Optional timeout cleanup: evict stale items; configurable idle TTL

- [x] **3.13** — Integration (mandatory wiring)
  - [x] 3.13.1 — Runtime loop: Observe uses buffer per 2.6.8–2.6.10
  - [x] 3.13.2 — Decision Layer: primary signals from merged buffer + 2.11.9
  - [x] 3.13.3 — Tool system: Act phase resolves buffer refs to paths (5.16); heavy readers run only when tools require them

### Identity & Profiles System (who Jarvis is — who the user is)
> **Rules:** No model is a standalone product. Every inference is part of one system with a single coherent identity. System prompts are dynamic (built from config + session + task + mode), not one static paragraph. Safety: never expose raw filesystem, secrets, or unrestricted host introspection.

- [x] **3.14** — User profile (identity-aware) — `core/identity/user_profile.py`
  - [x] 3.14.1 — Load/save per user id / session
  - [x] 3.14.2 — Store: display name, language preferences, behavior style, technical level
  - [x] 3.14.3 — Merge strategy with 3.7 (avoid duplicate sources of truth)
  - [x] 3.14.4 — Load into runtime: available to Observe, Decision, prompt builder
  - [x] 3.14.5 — Dynamic updates: CLI/Web commands edit profile

- [x] **3.15** — Jarvis profile (system identity) — `config/jarvis_identity.yaml`
  - [x] 3.15.1 — Define canonical identity: name = Jarvis; role = AI assistant system
  - [x] 3.15.2 — Capabilities summary (tools, memory, planning, multimodal)
  - [x] 3.15.3 — Default tone & behavior baseline
  - [x] 3.15.4 — Store in config with Pydantic model in `core/identity/`

- [x] **3.16** — Model awareness layer — `core/identity/model_awareness.py`
  - [x] 3.16.1 — Inject on every call: Jarvis identity + user profile + system context
  - [x] 3.16.2 — Required framing: "You are a component of Jarvis"; consistency across all routes
  - [x] 3.16.3 — Same framing across fast/deep/coder/vision; only task and mode sections differ

- [x] **3.17** — System Prompt Builder — `core/identity/prompt_builder.py`
  - [x] 3.17.1 — Combine: Jarvis identity + user profile + task context + mode fragments
  - [x] 3.17.2 — Inject into every model call (single pipeline)
  - [x] 3.17.3 — Deterministic ordering: identity → safety → user prefs → task → mode

- [x] **3.18** — Shared context awareness
  - [x] 3.18.1 — Same conversation state: rolling summary + message window + tool traces
  - [x] 3.18.2 — Previous actions: compact list of recent tool calls / outcomes
  - [x] 3.18.3 — Handoff discipline: when router switches models, identity + user + state carry forward

- [x] **3.19** — File & system awareness (controlled) — `core/identity/system_awareness.py`
  - [x] 3.19.1 — Abstract project view: allow-listed roots, depth limits, summarized tree
  - [x] 3.19.2 — Available tools: names + one-line purpose from registry
  - [x] 3.19.3 — Environment capabilities: OS class, GPU tier summary
  - [x] 3.19.4 — Explicit non-goals: do not expose raw system; redact secrets

- [x] **3.20** — Integration (mandatory wiring)
  - [x] 3.20.1 — Decision Layer: consume user expertise / goals as priors
  - [x] 3.20.2 — Runtime loop: Observe merges buffer + memory + identity into prompt build request
  - [x] 3.20.3 — Context Buffer: staged attachments described in task context section
  - [x] 3.20.4 — Memory system: long-term facts + profile + adaptive unified read path
  - [x] 3.20.5 — Engine: document contract for Phase 12 (Personality) as overlay

---

## 💻 Phase 4 — CLI Interface
> **Goal:** Full-featured terminal chat with Rich formatting

- [ ] **4.1** — Create `interfaces/cli/interface.py` — main CLI class
  - [ ] 4.1.1 — Rich panel-based UI with bordered message areas
  - [ ] 4.1.2 — Streaming response display (token by token with live update)
  - [ ] 4.1.3 — Arabic text rendering support (RTL detection and alignment)
  - [ ] 4.1.4 — Keyboard shortcuts (Ctrl+C exit, Ctrl+L clear)
  - [ ] 4.1.5 — Syntax-highlighted code blocks in responses
  - [ ] 4.1.6 — Model and mode indicator in prompt status bar

- [ ] **4.2** — Create `interfaces/cli/commands.py` — slash commands
  - [ ] 4.2.1 — `/clear` — clear conversation history
  - [ ] 4.2.2 — `/model [name]` — switch active model
  - [ ] 4.2.3 — `/mode [fast|normal|deep|planning|research]` — switch thinking mode
  - [ ] 4.2.4 — `/memory` — show recent memories
  - [ ] 4.2.5 — `/tools` — list available tools
  - [ ] 4.2.6 — `/status` — show current model, mode, session stats
  - [ ] 4.2.7 — `/profile` — show/edit user profile
  - [ ] 4.2.8 — `/config` — show current configuration summary
  - [ ] 4.2.9 — `/help` — show all commands with descriptions
  - [ ] 4.2.10 — Auto-complete for slash commands (Tab completion)

- [ ] **4.3** — Connect CLI to runtime manager / orchestrator
  - [ ] 4.3.1 — Pass user input to orchestrator with session context
  - [ ] 4.3.2 — Display streaming response with real-time Rich rendering
  - [ ] 4.3.3 — Show typing indicator (animated dots)
  - [ ] 4.3.4 — Display decision metadata (model, mode, confidence) in status line

- [ ] **4.4** — Create `app/cli.py` entry point

- [ ] **4.5** — Input history and navigation
  - [ ] 4.5.1 — Arrow key history navigation (up/down)
  - [ ] 4.5.2 — History persistence across sessions (file-backed)
  - [ ] 4.5.3 — Multi-line input support (Shift+Enter or backslash continuation)

- [ ] **4.6** — Test CLI
  - [ ] 4.6.1 — Arabic conversation test
  - [ ] 4.6.2 — Streaming response test
  - [ ] 4.6.3 — Commands test
  - [ ] 4.6.4 — History navigation test

- [ ] **4.7** — Global hotkey registration (Windows + Linux)
  - [ ] 4.7.1 — Register Ctrl+Alt+J to bring Jarvis CLI to focus / open new session
  - [ ] 4.7.2 — Register Ctrl+Alt+S to start voice input from any context
  - [ ] 4.7.3 — Use `keyboard` or `pynput` library (Windows-compatible)
  - [ ] 4.7.4 — Configurable hotkeys in config/settings.yaml

- [ ] **4.8** — Windows system tray process (background daemon)
  - [ ] 4.8.1 — Run Jarvis as background process on startup
  - [ ] 4.8.2 — System tray icon with right-click menu (Open CLI, Open Web, Quit)
  - [ ] 4.8.3 — Use `pystray` + `Pillow` for tray icon
  - [ ] 4.8.4 — Auto-start on Windows login (optional, user-controlled)

---
## 🛠️ Phase 5 — Tool System
> **Goal:** Real-world actions as callable tools — registry, structured I/O, tool calling, execution pipeline
> **Solution applied (Security & Scope):** Safely breaks the LLM out of its local box by granting controlled API access. Solves real-world execution limits by introducing human-in-the-loop pauses for auth/captchas, rather than failing silently.

- [ ] **5.1** — Create `skills/base.py` — BaseTool abstract class
  - [ ] 5.1.1 — `name: str` property
  - [ ] 5.1.2 — `description: str` property (for LLM tool list)
  - [ ] 5.1.3 — Input/output schema (JSON Schema or Pydantic model)
  - [ ] 5.1.4 — `execute(params: dict)` — validated structured input → structured result
  - [ ] 5.1.5 — `is_available()` — check prerequisites
  - [ ] 5.1.6 — `version: str` — semantic version for tool tracking
  - [ ] 5.1.7 — `category: str` — grouping for registry and UI

- [ ] **5.2** — Create `skills/registry.py` — tool registry + discovery
  - [ ] 5.2.1 — Scan `skills/` for BaseTool subclasses
  - [ ] 5.2.2 — Register all available tools with schemas
  - [ ] 5.2.3 — Export tool list + schemas to LLM (Ollama/OpenAI-compatible format)
  - [ ] 5.2.4 — Hot-reload tool modules without restart

- [ ] **5.3** — Tool calling pipeline — LLM selects tool + arguments
  - [ ] 5.3.1 — Map registry to Ollama-compatible tool definitions
  - [ ] 5.3.2 — Parse model tool calls from responses (streaming-safe)
  - [ ] 5.3.3 — Validate args → execute → feed observation back into runtime loop
  - [ ] 5.3.4 — Schema validation middleware: reject malformed tool calls before execution

- [ ] **5.4** — Wire `core/runtime/executor/` to registry
  - [ ] 5.4.1 — Unified `execute_tool(name, args)` with error wrapping
  - [ ] 5.4.2 — Log tool latency, outcomes, and args fingerprint (for Phase 15 metrics)
  - [ ] 5.4.3 — Tool metrics collection: success rate, avg latency, error frequency per tool

- [ ] **5.15** — Parallel execution system
  - [ ] 5.15.1 — Concurrent tool execution (no shared mutable resource)
  - [ ] 5.15.2 — Async runtime tasks with backpressure + cancellation
  - [ ] 5.15.3 — Background jobs for long I/O
  - [ ] 5.15.4 — Integration with Task Decomposition (Phase 10) scheduler

- [ ] **5.16** — Context Buffer ↔ executor / tools
  - [ ] 5.16.1 — Resolve buffer references to concrete file paths
  - [ ] 5.16.2 — Enforcement: no tool execution during staging; heavy pipelines only in Act

- [ ] **5.17** — Tool lifecycle management
  - [ ] 5.17.1 — Health check: verify external dependencies before first use
  - [ ] 5.17.2 — Graceful degradation: disable unavailable tools, report status
  - [ ] 5.17.3 — Resource cleanup: release browser instances, temp files on shutdown

---
## 💻 Phase 6 — System Control Skills
> **Goal:** Full OS and application control on Windows — open/close apps, clipboard, notifications, file ops, code execution, and global hotkeys as registered tools in the skill registry.
> **Dependency:** Phase 5 (Tool registry must exist before registering these tools)

- [ ] **6.1** — `skills/control/files/` — file operations tool (from old 5.7)
  - [ ] 6.1.1 — List directory contents
  - [ ] 6.1.2 — Read file content (text files; binary metadata only)
  - [ ] 6.1.3 — Write/create file with path safety checks
  - [ ] 6.1.4 — Move/copy/delete file (with undo-safe trash on Windows)
  - [ ] 6.1.5 — Search files by name/content (glob + grep)
  - [ ] 6.1.6 — Windows path normalization (backslash ↔ forward slash)

- [ ] **6.2** — `skills/control/system/` — system control tool (from old 5.8)
  - [ ] 6.2.1 — Get system info (CPU %, RAM used/total, disk space, GPU VRAM)
  - [ ] 6.2.2 — List running processes (name, PID, CPU%, RAM%)
  - [ ] 6.2.3 — Kill process by name or PID (`taskkill` on Windows, `kill` on Linux)
  - [ ] 6.2.4 — Get/set system volume (Windows: `pycaw`; Linux: `amixer`)
  - [ ] 6.2.5 — Run shell command in controlled sandbox (allowlist or confirm-first)
  - [ ] 6.2.6 — Get/set environment variables (session-scoped only)
  - [ ] 6.2.7 — List and manage Windows startup items
  - [ ] 6.2.8 — List and manage Windows Scheduled Tasks (read + basic create)
  - [ ] 6.2.9 — Network status: adapter list, IP addresses, connectivity check

- [ ] **6.3** — `skills/control/apps/` — Windows application launcher (from old 5.9 + expanded)
  - [ ] 6.3.1 — Open application by name using `ShellExecute` / `subprocess.Popen`
  - [ ] 6.3.2 — Search for app in `%APPDATA%`, `Program Files`, `Program Files (x86)`, PATH
  - [ ] 6.3.3 — Search Windows Start Menu shortcuts (.lnk files) by name
  - [ ] 6.3.4 — Close application by name or PID (`taskkill /IM name.exe /F`)
  - [ ] 6.3.5 — List installed applications (registry `HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall`)
  - [ ] 6.3.6 — Bring application window to foreground (`pywin32` / `ctypes`)
  - [ ] 6.3.7 — Minimize/maximize/restore application window
  - [ ] 6.3.8 — Graceful shutdown: try close message first, then force kill

- [ ] **6.4** — `skills/coder/executor.py` — code execution tool (from old 5.10)
  - [ ] 6.4.1 — Execute Python code safely in subprocess with timeout
  - [ ] 6.4.2 — Execute shell/PowerShell commands (confirm-first for destructive ops)
  - [ ] 6.4.3 — Capture stdout/stderr; return structured result
  - [ ] 6.4.4 — Timeout protection (configurable, default 30s)
  - [ ] 6.4.5 — Return structured result: {stdout, stderr, returncode, duration}

- [ ] **6.5** — `skills/control/clipboard.py` — Clipboard manager tool (NEW)
  - [ ] 6.5.1 — Read current clipboard content (text, image detection)
  - [ ] 6.5.2 — Write text to clipboard
  - [ ] 6.5.3 — Monitor clipboard for changes (background thread, event on change)
  - [ ] 6.5.4 — Use `pyperclip` (cross-platform) + `win32clipboard` for images
  - [ ] 6.5.5 — Integration: "translate what I copied", "explain this code" flows

- [ ] **6.6** — `skills/control/notifications.py` — Windows notification tool (NEW)
  - [ ] 6.6.1 — Send Windows Toast notification (title + body + optional icon)
  - [ ] 6.6.2 — Use `win10toast` or `winotify` library
  - [ ] 6.6.3 — Notification types: info / warning / success / reminder
  - [ ] 6.6.4 — Integration: task completion alerts, Calendar reminders, long-task done
  - [ ] 6.6.5 — Fallback: print to console if Windows toast fails

- [ ] **6.7** — `skills/screen/` — Screen capture and lightweight OCR (NEW)
  - [ ] 6.7.1 — Full screenshot capture (`Pillow` + `mss` for speed)
  - [ ] 6.7.2 — Region screenshot (user-defined bounding box)
  - [ ] 6.7.3 — Lightweight OCR without vision model: `pytesseract` / `easyocr`
  - [ ] 6.7.4 — "Read what's on my screen" without loading LLaVA (fast path)
  - [ ] 6.7.5 — Save screenshots to configurable output folder
  - [ ] 6.7.6 — Pass screenshot to vision model (LLaVA) when semantic understanding needed

- [ ] **6.8** — Global hotkey tool registration
  - [ ] 6.8.1 — Register hotkeys as a registered tool in the skill registry
  - [ ] 6.8.2 — `skills/control/hotkeys.py` — manage hotkey bindings at runtime
  - [ ] 6.8.3 — Configurable bindings in config/settings.yaml → hotkeys section
  - [ ] 6.8.4 — Emit events via EventBus when hotkey fires

- [ ] **6.9** — Test Phase 6 tools
  - [ ] 6.9.1 — Open and close Notepad by name
  - [ ] 6.9.2 — Read + write clipboard
  - [ ] 6.9.3 — Send Windows notification
  - [ ] 6.9.4 — Screenshot + OCR test
  - [ ] 6.9.5 — Kill process by name test

---

## 🌐 Phase 7 — Browser & Web Skills
> **Goal:** Full browser control via Playwright — navigate, interact, extract, download, upload — with persistent sessions so Jarvis stays logged in between runs.
> **Dependency:** Phase 5 (Tool registry), Phase 6 (system control for file paths)

- [ ] **7.1** — `skills/search/web_search.py` — web search tool (from old 5.5)
  - [ ] 7.1.1 — DuckDuckGo search (no API key needed)
  - [ ] 7.1.2 — Return top N results: title + snippet + URL
  - [ ] 7.1.3 — Fast page content extraction (readability or trafilatura)
  - [ ] 7.1.4 — Local SearxNG integration (optional, self-hosted)
  - [ ] 7.1.5 — Result caching (TTL-based, avoid duplicate searches)

- [ ] **7.2** — `skills/web/browser.py` — browser automation core (from old 5.6, expanded)
  - [ ] 7.2.1 — Launch Playwright browser (Chromium headless/headed, configurable)
  - [ ] 7.2.2 — Navigate to URL and wait for load
  - [ ] 7.2.3 — Click element by text, CSS selector, or XPath
  - [ ] 7.2.4 — Fill input fields (text, checkbox, select dropdown)
  - [ ] 7.2.5 — Extract page content as clean text/Markdown (readability)
  - [ ] 7.2.6 — Take full-page or viewport screenshot

- [ ] **7.3** — `skills/web/session_manager.py` — persistent browser session (NEW)
  - [ ] 7.3.1 — Save browser storage state (cookies + localStorage) to JSON file per site
  - [ ] 7.3.2 — Load saved session on browser open (stay logged in between Jarvis restarts)
  - [ ] 7.3.3 — Session keyed by domain: e.g. `sessions/google.com.json`
  - [ ] 7.3.4 — Auto-detect if session expired → prompt user to re-login once, then save again
  - [ ] 7.3.5 — Session vault in config-defined path (not in git, gitignored)
  - [ ] 7.3.6 — Integration: all browser tools use session manager by default

- [ ] **7.4** — `skills/web/downloader.py` — file download management (NEW)
  - [ ] 7.4.1 — Intercept Playwright download events
  - [ ] 7.4.2 — Save to configured download folder with original filename
  - [ ] 7.4.3 — Return download result: {path, filename, size, duration}
  - [ ] 7.4.4 — Progress feedback for large files

- [ ] **7.5** — `skills/web/uploader.py` — file upload via browser (NEW)
  - [ ] 7.5.1 — Set file input fields with local file path (`page.set_input_files`)
  - [ ] 7.5.2 — Handle multiple file uploads
  - [ ] 7.5.3 — Validate file exists before upload attempt

- [ ] **7.6** — Multi-tab and multi-window support (NEW)
  - [ ] 7.6.1 — Open new tab / switch between tabs by index or title
  - [ ] 7.6.2 — Close specific tab
  - [ ] 7.6.3 — Handle popup windows and new window events
  - [ ] 7.6.4 — Handle alert/confirm/prompt dialogs (auto-accept or ask user)

- [ ] **7.7** — Human-in-the-loop pause for auth (NEW)
  - [ ] 7.7.1 — Detect login/captcha pages (title check + URL patterns)
  - [ ] 7.7.2 — Pause automation and notify user via notification + CLI prompt
  - [ ] 7.7.3 — Resume after user signals completion (press Enter / button)
  - [ ] 7.7.4 — Do not silently fail on auth walls — always surface to user

- [ ] **7.8** — WhatsApp Web automation (NEW)
  - [ ] 7.8.1 — Open WhatsApp Web using saved session
  - [ ] 7.8.2 — Search for contact by name
  - [ ] 7.8.3 — Send text message to contact
  - [ ] 7.8.4 — Read last N messages from a conversation
  - [ ] 7.8.5 — Handle QR code login (show QR, wait for scan, save session)
  - [ ] 7.8.6 — Integration: "send X a message saying Y" natural language command

- [ ] **7.9** — Test Phase 7 tools
  - [ ] 7.9.1 — Web search + content extraction test
  - [ ] 7.9.2 — Session persistence test (login, restart, verify still logged in)
  - [ ] 7.9.3 — File download test
  - [ ] 7.9.4 — File upload test
  - [ ] 7.9.5 — Multi-tab navigation test
  - [ ] 7.9.6 — WhatsApp send message test

---

## 🔌 Phase 8 — External APIs & Integrations
> **Goal:** Connect Jarvis to Google services, YouTube, and other external APIs. All integrations registered as tools in Phase 5 registry.
> **Dependency:** Phase 5 (Tool registry), Phase 7 (browser session for OAuth flows)

- [ ] **8.1** — `skills/api/google_calendar.py` — Google Calendar (from old 5.11)
  - [ ] 8.1.1 — OAuth2 authentication flow (browser-based, save token to file)
  - [ ] 8.1.2 — List upcoming events (configurable N days)
  - [ ] 8.1.3 — Create new event (title, datetime, description, attendees)
  - [ ] 8.1.4 — Delete event by ID
  - [ ] 8.1.5 — Search events by keyword and date range
  - [ ] 8.1.6 — Update existing event fields

- [ ] **8.2** — `skills/api/youtube.py` — YouTube (from old 5.12)
  - [ ] 8.2.1 — Search videos by query (YouTube Data API v3)
  - [ ] 8.2.2 — Get video info (title, duration, channel, views)
  - [ ] 8.2.3 — Open video in default browser
  - [ ] 8.2.4 — Get channel info and recent uploads

- [ ] **8.3** — `skills/reader/pdf/` — PDF reading tool (from old 5.13)
  - [ ] 8.3.1 — Extract text from PDF (pypdf / pdfplumber)
  - [ ] 8.3.2 — Extract images from PDF pages
  - [ ] 8.3.3 — Summarize PDF via LLM (chunked for long docs)
  - [ ] 8.3.4 — Extract tables from PDF as structured data

- [ ] **8.4** — `skills/reader/office/` — Office documents (from old 5.14)
  - [ ] 8.4.1 — Read Word (.docx) files (python-docx)
  - [ ] 8.4.2 — Read Excel (.xlsx) files (openpyxl / pandas)
  - [ ] 8.4.3 — Read PowerPoint (.pptx) files (python-pptx)
  - [ ] 8.4.4 — Write/create simple Word documents
  - [ ] 8.4.5 — Write/create simple Excel spreadsheets

- [ ] **8.5** — `skills/api/gmail.py` — Gmail integration (NEW)
  - [ ] 8.5.1 — OAuth2 auth (reuse Google token from Calendar if same account)
  - [ ] 8.5.2 — Read latest N emails (sender, subject, preview, date)
  - [ ] 8.5.3 — Search emails by query (Gmail search syntax)
  - [ ] 8.5.4 — Send email (to, subject, body, optional attachments)
  - [ ] 8.5.5 — Reply to email by message ID
  - [ ] 8.5.6 — Mark email as read/unread/starred
  - [ ] 8.5.7 — Move email to label/folder
  - [ ] 8.5.8 — Integration: "read my latest emails" / "send email to X about Y"

- [ ] **8.6** — `skills/api/google_drive.py` — Google Drive (NEW)
  - [ ] 8.6.1 — OAuth2 auth (reuse Google token)
  - [ ] 8.6.2 — List files in Drive root and folders
  - [ ] 8.6.3 — Search files by name or content
  - [ ] 8.6.4 — Download file by name or ID
  - [ ] 8.6.5 — Upload local file to Drive
  - [ ] 8.6.6 — Share file with email address (view/edit permission)

- [ ] **8.7** — `skills/api/google_contacts.py` — Google Contacts (NEW)
  - [ ] 8.7.1 — OAuth2 auth (reuse Google token, People API)
  - [ ] 8.7.2 — List contacts (name, email, phone)
  - [ ] 8.7.3 — Search contacts by name or email
  - [ ] 8.7.4 — Get contact details
  - [ ] 8.7.5 — Create new contact

- [ ] **8.8** — Unified Google OAuth manager (NEW)
  - [ ] 8.8.1 — Single `skills/api/google_auth.py` that handles OAuth2 for all Google APIs
  - [ ] 8.8.2 — Scopes: Calendar + Gmail + Drive + Contacts + YouTube in one token
  - [ ] 8.8.3 — Token persistence: save/load from `data/google_token.json`
  - [ ] 8.8.4 — Auto-refresh expired tokens silently
  - [ ] 8.8.5 — Re-auth flow: open browser → user consents → token saved

- [ ] **8.9** — Test Phase 8 integrations
  - [ ] 8.9.1 — Google OAuth flow end-to-end
  - [ ] 8.9.2 — Calendar CRUD test
  - [ ] 8.9.3 — Gmail send + read test
  - [ ] 8.9.4 — Drive upload + download test
  - [ ] 8.9.5 — Contacts search test

---

## 🤖 Phase 9 — Agents (Basic → Advanced)
> **Goal:** Multi-step autonomy. Agents coordinate tools (Phases 6–8), plan subtasks, reason, and execute complex goals without step-by-step user guidance.
> **Dependency:** Phases 5–8 (tools + browser + APIs must exist before agents can use them)

### Basic (core autonomy)
- [ ] **9.1** — Create `core/agents/planner/planner.py` — step decomposition + sequencing
  - [ ] 9.1.1 — Break complex request into ordered steps
  - [ ] 9.1.2 — Assign each step to a tool or model role
  - [ ] 9.1.3 — Execute steps sequentially via runtime
  - [ ] 9.1.4 — Pass output of step N as input to step N+1
  - [ ] 9.1.5 — Report progress to user

- [ ] **9.2** — Create `core/agents/thinker/thinker.py` — deeper reasoning
  - [ ] 9.2.1 — Extended Chain-of-Thought reasoning
  - [ ] 9.2.2 — Self-verification of answers
  - [ ] 9.2.3 — Confidence scoring

- [ ] **9.3** — ReAct loop integration (Reason + Act) with runtime
  - [ ] 9.3.1 — Observe → Think → Act → Observe with tool calls
  - [ ] 9.3.2 — Max iterations guard
  - [ ] 9.3.3 — Optional: show reasoning steps to user

### Advanced
- [ ] **9.4** — Create `core/agents/researcher.py` — deep research agent
  - [ ] 9.4.1 — Multi-query web search
  - [ ] 9.4.2 — Scrape and summarize multiple sources
  - [ ] 9.4.3 — Cross-reference and fact-check
  - [ ] 9.4.4 — Generate structured report

- [ ] **9.5** — `skills/screen/screen_agent.py` — visual computer control
  - [ ] 9.5.1 — Take screenshot
  - [ ] 9.5.2 — Describe screen via vision
  - [ ] 9.5.3 — Move mouse and click based on vision
  - [ ] 9.5.4 — Type text
  - [ ] 9.5.5 — Full GUI automation loop (guarded)

- [ ] **9.6** — Test agents
  - [ ] 9.6.1 — Multi-step task test
  - [ ] 9.6.2 — ReAct + tool calling test
  - [ ] 9.6.3 — Screen agent test

- [ ] **9.7** — `core/agents/extensions/` — pluggable agent extensions (was "New folder")
  - [ ] 9.7.1 — Define AgentExtension base class (hook: before/after plan execution)
  - [ ] 9.7.2 — Example extension: auto-summarize completed plan to memory
  - [ ] 9.7.3 — Example extension: post-plan notification via 6.6

- [ ] **9.8** — Computer use agent — full autonomous loop (NEW)
  - [ ] 9.8.1 — Observe screen via 6.7 (screenshot)
  - [ ] 9.8.2 — Describe what's visible using LLaVA (vision tool)
  - [ ] 9.8.3 — Decide next action (click, type, open app, search) using LLM
  - [ ] 9.8.4 — Execute via pyautogui (mouse + keyboard control)
  - [ ] 9.8.5 — Loop: screenshot → describe → decide → execute → screenshot
  - [ ] 9.8.6 — Safety: require user confirmation before destructive actions
  - [ ] 9.8.7 — Max-step guard (configurable) to prevent infinite loops
  - [ ] 9.8.8 — Integration: uses app launcher (6.3), browser (Phase 7), OCR (6.7)

---

## 🧩 Phase 10 — Task Decomposition Engine
> **Goal:** Turn a high-level goal into a structured execution graph. Enables complex multi-step automation.
> **Dependency:** Phase 9 (Agents must exist as execution units)
> **Solution applied (Zero-Shot Limits):** Overcomes local LLM logic failure limits by breaking massive, abstract tasks (which crash 8B models) into tiny, measurable micro-tasks that small models excel at.

- [ ] **10.1** — Decomposition API — input: user goal + DecisionOutput; output: DAG of steps
  - [ ] 10.1.1 — Subtask schema: id, type, inputs/outputs, depends_on, retry_group
  - [ ] 10.1.2 — Break tasks into subtasks (LLM or template-assisted)
  - [ ] 10.1.3 — Human-in-the-loop nodes (optional approval gates)

- [ ] **10.2** — Execution graph runtime — deterministic scheduler
  - [ ] 10.2.1 — Topological order with parallel frontier
  - [ ] 10.2.2 — Handle dependencies: pass outputs as typed artifacts
  - [ ] 10.2.3 — Idempotency: stable keys for re-run after resume

- [ ] **10.3** — Retry only failed steps
  - [ ] 10.3.1 — Mark failed node with error class; skip successful siblings
  - [ ] 10.3.2 — Partial replan: optional subgraph regeneration

- [ ] **10.4** — Integration with agents + runtime
  - [ ] 10.4.1 — Planner (9.1) can delegate to engine
  - [ ] 10.4.2 — Dispatcher routes "complex plan" intents here

- [ ] **10.5** — Observability — export graph to logs/UI (Mermaid or JSON)

- [ ] **10.6** — Tests
  - [ ] 10.6.1 — Diamond dependency graph (parallel then join)
  - [ ] 10.6.2 — Failure mid-graph → retry one branch only
  - [ ] 10.6.3 — Resume after disconnect with same run_id

- [ ] **10.7** — Natural language goal → plan (end-to-end)
  - [ ] 10.7.1 — "Book a meeting with X about Y on Friday" → decompose → Calendar tool
  - [ ] 10.7.2 — "Summarize my last 5 emails and save to Drive" → Gmail + Drive tools
  - [ ] 10.7.3 — "Open Chrome, go to YouTube, search for X, click first result" → browser agent
  - [ ] 10.7.4 — Test that decomposition uses available tools correctly (tool registry must be consulted)

- [ ] **10.8** — Feedback hooks — on node success/failure emit signals for Phase 11

- [ ] **10.9** — Cost / budget awareness — inherit cost_estimate; prune when over budget

---

## 🔁 Phase 11 — Feedback & Learning
> **Goal:** Close the loop — outcomes feed back into memory, model priors, and decision weights.
> **Dependency:** Phase 9 (Agents) + Phase 10 (Decomposition) must produce outcomes to learn from.

- [ ] **11.1** — Implicit feedback detection
  - [ ] 11.1.1 — User continues: new message within τ → weak positive
  - [ ] 11.1.2 — User repeats question: rephrase → negative / confusion signal
  - [ ] 11.1.3 — User ignores response: no follow-up within session → weak negative

- [ ] **11.2** — Explicit feedback (optional UI) — thumbs up/down, correction messages

- [ ] **11.3** — Success / failure scoring — map events + Evaluate + error class to scalar per turn

- [ ] **11.4** — Store feedback linked to:
  - [ ] 11.4.1 — Decisions: snapshot DecisionOutput
  - [ ] 11.4.2 — Models: resolved model id + mode pack
  - [ ] 11.4.3 — Tools: tool name + version + args fingerprint

- [ ] **11.5** — Learning surfaces (incremental, safe)
  - [ ] 11.5.1 — Router weights: nudge scores from rolling aggregates
  - [ ] 11.5.2 — Escalation aggressiveness: tune thresholds
  - [ ] 11.5.3 — Memory writes: "what worked" summaries into long-term

- [ ] **11.6** — Privacy & controls — per-user opt-out; retention TTL; export/delete

- [ ] **11.7** — Integration tests — synthetic sessions; verify attribution chain

- [ ] **11.8** — Anti-feedback hacking — detect spam toggles; rate-limit weight updates

- [ ] **11.9** — Dashboard hooks (optional) — expose aggregates to Phase 15 monitoring

---

## 🌐 Phase 12 — Web UI + Voice + Vision
> **Goal:** Rich multimodal interfaces — real-time web chat, voice pipeline, image understanding, image generation.
> **Dependency:** Core brain (Phases 1–11) must be complete for interfaces to have real capabilities.

### Web UI — Glassmorphism + Frosted Acrylic AI Chat Interface
> **Design philosophy:** A premium, state-of-the-art chat interface that synthesizes the best UX patterns from modern AI platforms (ChatGPT, Claude, Gemini, Perplexity, HuggingChat) into a unified, beautiful, and cohesive design. Core aesthetic: **Glassmorphism** panels with **Frosted Acrylic/Lucite** depth layers, heavy blur compositing, and sophisticated micro-animations.

#### 12.1 — Backend: FastAPI Application (`interfaces/web/app.py`)
- [ ] 12.1.1 — Static files serving (CSS, JS, fonts, icons)
- [ ] 12.1.2 — Jinja2 template rendering with SSR fallback
- [ ] 12.1.3 — CORS configuration for development and production
- [ ] 12.1.4 — Session management middleware (session ID, expiry, cookie-based)
- [ ] 12.1.5 — Rate limiting middleware (per-session, per-IP)
- [ ] 12.1.6 — Gzip compression for static assets

#### 12.2 — WebSocket Handler (`interfaces/web/websocket.py`)
- [ ] 12.2.1 — Accept connection with session validation
- [ ] 12.2.2 — Receive message → pass to runtime / orchestrator with session context
- [ ] 12.2.3 — Stream response tokens back to client (JSON text frames)
- [ ] 12.2.4 — Handle disconnection gracefully (cleanup state, log)
- [ ] 12.2.5 — Auto-reconnect protocol: client detects disconnect → reconnect → resume stream
- [ ] 12.2.6 — Heartbeat / ping-pong keep-alive to detect stale connections
- [ ] 12.2.7 — Support concurrent sessions per user (multiple tabs)

#### 12.3 — Chat Page (`interfaces/web/templates/index.html`)
- [ ] 12.3.1 — Single-page chat application (no framework, vanilla JS)
- [ ] 12.3.2 — Responsive layout: fluid mobile-first, desktop-optimized
- [ ] 12.3.3 — Arabic RTL support: auto-detect text direction, proper alignment
- [ ] 12.3.4 — Streaming message display with real-time animated cursor
- [ ] 12.3.5 — Code blocks with syntax highlighting (Highlight.js or Prism) + copy-to-clipboard button
- [ ] 12.3.6 — Markdown rendering for assistant responses (headings, lists, bold, links, tables)
- [ ] 12.3.7 — LaTeX / math equation rendering (KaTeX inline)
- [ ] 12.3.8 — Image preview for uploaded / generated images (lightbox on click)
- [ ] 12.3.9 — File attachment cards: filename, size, type icon, remove button
- [ ] 12.3.10 — Message actions: copy full message, regenerate, edit user message, delete

#### 12.4 — Design System: Glassmorphism + Frosted Acrylic Aesthetic (`interfaces/web/static/style.css`)

##### 12.4.1 — Color System & Theme Engine
- [ ] 12.4.1.1 — **Dark theme (default):** deep navy/charcoal base (`#0a0a1a`, `#12122a`), frosted glass panels with `rgba(255,255,255,0.04–0.08)` backgrounds
- [ ] 12.4.1.2 — **Accent gradients:** electric blue → teal → violet (`#3b82f6` → `#06b6d4` → `#8b5cf6`), used in action buttons, active states, and glow effects
- [ ] 12.4.1.3 — **Light theme:** soft white/cream base, warm gray panels with frosted overlays, muted accents
- [ ] 12.4.1.4 — **Theme toggle:** smooth CSS transition (0.4s ease) between dark↔light; persist in localStorage
- [ ] 12.4.1.5 — **CSS custom properties:** full token system (`--color-bg-primary`, `--glass-blur`, `--border-glow`, `--shadow-depth`) for easy theme extension
- [ ] 12.4.1.6 — **Luminous glow effects:** subtle box-shadow halos on active elements (`0 0 20px rgba(59,130,246,0.15)`)

##### 12.4.2 — Glass & Blur Compositing
- [ ] 12.4.2.1 — **Multi-layer blur depth:** ambient background blur (24px), sidebar glass (16px), card-level blur (12px), input bar blur (8px)
- [ ] 12.4.2.2 — **Frosted glass panels:** `backdrop-filter: blur()` + `background: rgba()` + subtle `border: 1px solid rgba(255,255,255,0.06)`
- [ ] 12.4.2.3 — **Depth layers:** z-index system with opacity gradient — deeper = more opaque, surface = more transparent
- [ ] 12.4.2.4 — **Inner light borders:** 1px top/left border with `rgba(255,255,255,0.08)` to simulate light refraction
- [ ] 12.4.2.5 — **Background ambient mesh:** CSS radial gradients at positions behind content (moving or fixed), creating a living background under glass

##### 12.4.3 — Typography
- [ ] 12.4.3.1 — **Primary font:** Inter (Google Fonts) — fallback: system-ui, -apple-system, sans-serif
- [ ] 12.4.3.2 — **Monospace font:** JetBrains Mono or Fira Code — for code blocks and technical output
- [ ] 12.4.3.3 — **Type scale:** 12px / 14px / 16px / 18px / 24px / 32px with proper line-height and letter-spacing
- [ ] 12.4.3.4 — **Arabic typography:** Noto Sans Arabic or IBM Plex Arabic for RTL content with correct bidi handling

##### 12.4.4 — Icons
- [ ] 12.4.4.1 — **Icon library:** Lucide Icons (consistent weight, radius, and style)
- [ ] 12.4.4.2 — **Icon sizing:** 16px (inline), 20px (buttons), 24px (navigation), 32px (features)
- [ ] 12.4.4.3 — **Icon colors:** inherit from text color; accent color on hover/active states
- [ ] 12.4.4.4 — **Mode icons:** unique icon per thinking mode — lightning (fast), brain (normal), atom (deep), layers (planning), telescope (research)
- [ ] 12.4.4.5 — **Animated icons:** subtle scale (1.1×) + color transition on hover

##### 12.4.5 — Animations & Micro-Interactions
- [ ] 12.4.5.1 — **Message entry:** staggered scale+fade from bottom (0→1 opacity, 0.95→1 scale, 0.3s cubic-bezier)
- [ ] 12.4.5.2 — **Typing indicator:** 3-dot pulse animation with sequential delay (0.6s period)
- [ ] 12.4.5.3 — **Loading skeleton:** shimmer gradient sweep (left→right, 1.5s, infinite) on glassmorphic placeholder cards
- [ ] 12.4.5.4 — **Button hover:** glow intensify (box-shadow spread), border brighten, background lighten — smooth 0.2s transition
- [ ] 12.4.5.5 — **Sidebar open/close:** slide + fade (transform: translateX + opacity, 0.3s ease-out)
- [ ] 12.4.5.6 — **Theme transition:** cross-fade all color custom properties with 0.4s ease
- [ ] 12.4.5.7 — **Scroll-to-bottom:** smooth scroll with CSS `scroll-behavior: smooth`; auto-scroll on new messages
- [ ] 12.4.5.8 — **Input focus:** border glow intensify + subtle shadow expansion
- [ ] 12.4.5.9 — **Toast notifications:** slide-in from top-right with fade, auto-dismiss after 4s
- [ ] 12.4.5.10 — **Parallax ambient background:** subtle movement on mouse move (CSS transform or JS requestAnimationFrame)

#### 12.5 — Input Bar System (`interfaces/web/static/chat.js`)

##### 12.5.1 — Smart Text Input
- [ ] 12.5.1.1 — **Multilingual text bar:** contenteditable div or textarea with full Unicode support (Arabic, English, Chinese, etc.)
- [ ] 12.5.1.2 — **Auto-expanding height:** grow with content (min 1 line → max 8 lines), then scroll internally
- [ ] 12.5.1.3 — **Placeholder text:** "Message Jarvis..." (disappears on focus/type)
- [ ] 12.5.1.4 — **RTL auto-detection:** switch text direction based on first character typed
- [ ] 12.5.1.5 — **Keyboard shortcuts:** Enter to send, Shift+Enter for newline, Escape to clear

##### 12.5.2 — Attachment System (+ Button)
- [ ] 12.5.2.1 — **"+" button:** positioned left of the text input; opens attachment menu on click
- [ ] 12.5.2.2 — **Attachment menu:** popup with options: Upload File, Upload Image, Take Photo (mobile), Paste from Clipboard
- [ ] 12.5.2.3 — **File upload:** accept any file type; drag-and-drop support on entire chat area
- [ ] 12.5.2.4 — **Image upload:** accept images with inline preview thumbnail above the input bar
- [ ] 12.5.2.5 — **Clipboard paste:** auto-detect image paste (Ctrl+V) and attach
- [ ] 12.5.2.6 — **Attachment preview strip:** horizontal row above input showing attached files with remove (×) button per item
- [ ] 12.5.2.7 — **Multiple attachments:** allow stacking multiple files/images before sending
- [ ] 12.5.2.8 — **File type icons:** show appropriate icon per file type (PDF, doc, image, audio, code, etc.)
- [ ] 12.5.2.9 — **Size validation:** reject files over configurable max size; show friendly error toast
- [ ] 12.5.2.10 — **Upload progress:** animated progress bar on large files

##### 12.5.3 — Mode Selector (Icon Row)
- [ ] 12.5.3.1 — **Mode icon bar:** row of clickable icons next to the "+" button, each representing a thinking mode
- [ ] 12.5.3.2 — **Normal mode icon (default):** brain icon — balanced response
- [ ] 12.5.3.3 — **Deep thinking icon:** atom/nucleus icon — extended chain-of-thought
- [ ] 12.5.3.4 — **Research mode icon:** telescope/magnifying glass — multi-source, tool-heavy
- [ ] 12.5.3.5 — **Planning mode icon:** layers/stack icon — decompose into steps
- [ ] 12.5.3.6 — **Fast mode icon:** lightning bolt — quick, concise answers
- [ ] 12.5.3.7 — **Active mode indicator:** highlighted/glowing icon with accent color when selected
- [ ] 12.5.3.8 — **Mode tooltip:** hover shows mode name and brief description
- [ ] 12.5.3.9 — **Mode persists:** selected mode persists until user changes it
- [ ] 12.5.3.10 — **Compact/expand:** on small screens, collapse into a single dropdown selector

##### 12.5.4 — Send / Voice Button (Dynamic)
- [ ] 12.5.4.1 — **Empty input → microphone icon:** when text bar is empty, show a microphone icon as send button
- [ ] 12.5.4.2 — **Typing → send arrow icon:** when user types any character, morph into a send (arrow-up) icon
- [ ] 12.5.4.3 — **Icon morph animation:** smooth transition between mic ↔ send (scale + fade crossover, 0.2s)
- [ ] 12.5.4.4 — **Voice mode activation:** clicking mic icon activates speech-to-text recording mode
- [ ] 12.5.4.5 — **Recording indicator:** pulsing red ring around mic icon; waveform visualization in input area
- [ ] 12.5.4.6 — **Stop recording:** click mic again or press Enter to send transcribed text
- [ ] 12.5.4.7 — **Send button states:** idle, hover (glow), active (pressed scale), loading (spinner while processing)
- [ ] 12.5.4.8 — **Disable on empty:** send button is non-interactive when input is empty (mic mode takes priority)

#### 12.6 — Sidebar System

##### 12.6.1 — Sidebar Layout & Structure
- [ ] 12.6.1.1 — **Collapsible sidebar:** left-side panel with frosted glass background, slide animation
- [ ] 12.6.1.2 — **Toggle button:** hamburger / X icon at top of sidebar or main area
- [ ] 12.6.1.3 — **Sidebar width:** 280px desktop; full-width overlay on mobile
- [ ] 12.6.1.4 — **Persistent state:** remember open/closed state in localStorage
- [ ] 12.6.1.5 — **Resize handle:** optional drag-to-resize sidebar width (min 240px, max 400px)

##### 12.6.2 — Conversation History Section
- [ ] 12.6.2.1 — **Conversation list:** scrollable list of past conversations, sorted by last activity (newest first)
- [ ] 12.6.2.2 — **Conversation card:** title (auto-generated or user-edited), last message preview, timestamp, message count
- [ ] 12.6.2.3 — **Active conversation highlight:** accent border-left or background tint
- [ ] 12.6.2.4 — **New conversation button:** prominent "+" or "New Chat" button at top
- [ ] 12.6.2.5 — **Edit title:** inline edit (click pencil icon → contenteditable → Enter to save)
- [ ] 12.6.2.6 — **Delete conversation:** swipe or right-click context menu → confirmation dialog → delete
- [ ] 12.6.2.7 — **Archive conversation:** move to archive section (collapsible "Archived" folder at bottom)
- [ ] 12.6.2.8 — **Pin conversation:** pin to top of list (star icon toggle)
- [ ] 12.6.2.9 — **Conversation grouping:** auto-group by date: Today, Yesterday, Previous 7 Days, Previous 30 Days, Older
- [ ] 12.6.2.10 — **Bulk actions:** multi-select with checkboxes → bulk delete / archive / export

##### 12.6.3 — Search System
- [ ] 12.6.3.1 — **Search bar:** positioned above conversation list; frosted glass input with search icon
- [ ] 12.6.3.2 — **Search by title:** filter conversations by matching title text (instant, client-side)
- [ ] 12.6.3.3 — **Search within conversations:** full-text search across all message content (server-side via memory)
- [ ] 12.6.3.4 — **Search results:** highlighted matching text snippets with conversation title and date
- [ ] 12.6.3.5 — **Search keyboard shortcut:** Ctrl+K or Cmd+K opens search with focus
- [ ] 12.6.3.6 — **Clear search:** X button or Escape to clear and return to full list

##### 12.6.4 — Settings Panel
- [ ] 12.6.4.1 — **Settings button:** gear icon at bottom of sidebar; opens settings panel (slide-in overlay or modal)
- [ ] 12.6.4.2 — **Appearance settings:**
  - [ ] 12.6.4.2.1 — Theme selector: Dark / Light / System (auto)
  - [ ] 12.6.4.2.2 — Accent color picker: preset palette or custom hex
  - [ ] 12.6.4.2.3 — Font size: slider (Small / Medium / Large / Extra Large)
  - [ ] 12.6.4.2.4 — Message density: Compact / Comfortable / Spacious
  - [ ] 12.6.4.2.5 — Blur intensity: slider (None / Light / Medium / Heavy) for accessibility
  - [ ] 12.6.4.2.6 — Animation toggle: enable/disable all animations (reduce motion preference)
  - [ ] 12.6.4.2.7 — Chat bubble style: rounded / squared / minimal
- [ ] 12.6.4.3 — **Behavior settings:**
  - [ ] 12.6.4.3.1 — Default thinking mode selector
  - [ ] 12.6.4.3.2 — Default language: Arabic / English / Auto-detect
  - [ ] 12.6.4.3.3 — Response style: Concise / Balanced / Detailed
  - [ ] 12.6.4.3.4 — Auto-scroll on new messages: toggle
  - [ ] 12.6.4.3.5 — Sound notifications: toggle + volume
  - [ ] 12.6.4.3.6 — Enter key behavior: Send message / New line
  - [ ] 12.6.4.3.7 — Show model/mode indicator in chat: toggle
  - [ ] 12.6.4.3.8 — Show confidence scores: toggle
- [ ] 12.6.4.4 — **Model settings:**
  - [ ] 12.6.4.4.1 — Active model selector (dropdown of available Ollama models)
  - [ ] 12.6.4.4.2 — Temperature slider (0.0 – 1.5)
  - [ ] 12.6.4.4.3 — Max tokens slider
  - [ ] 12.6.4.4.4 — Model override toggle: always use selected model vs auto-route
- [ ] 12.6.4.5 — **Data & Privacy:**
  - [ ] 12.6.4.5.1 — Export all conversations (JSON/Markdown)
  - [ ] 12.6.4.5.2 — Clear all conversations (with confirmation)
  - [ ] 12.6.4.5.3 — Clear memory (short-term / long-term / all)
  - [ ] 12.6.4.5.4 — Reset user profile to defaults
- [ ] 12.6.4.6 — **About section:** version, build info, system status, link to documentation

#### 12.7 — REST API Routes (`interfaces/web/routes/`)
- [ ] 12.7.1 — `GET /` — serve chat page
- [ ] 12.7.2 — `GET /api/models` — list available models with status
- [ ] 12.7.3 — `GET /api/conversations` — list all conversations (paginated)
- [ ] 12.7.4 — `GET /api/conversations/:id` — get conversation messages
- [ ] 12.7.5 — `PUT /api/conversations/:id` — update conversation title
- [ ] 12.7.6 — `DELETE /api/conversations/:id` — delete conversation
- [ ] 12.7.7 — `POST /api/conversations/:id/archive` — archive/unarchive conversation
- [ ] 12.7.8 — `GET /api/memory` — get conversation history summary
- [ ] 12.7.9 — `DELETE /api/memory` — clear conversation memory
- [ ] 12.7.10 — `POST /api/upload` — file upload endpoint (returns file reference ID)
- [ ] 12.7.11 — `GET /api/settings` — get user settings
- [ ] 12.7.12 — `PUT /api/settings` — update user settings
- [ ] 12.7.13 — `GET /api/search` — search across conversations

#### 12.8 — Notification & Feedback System
- [ ] 12.8.1 — Toast notification system (success, error, info, warning)
- [ ] 12.8.2 — Connection status indicator (connected / reconnecting / offline badge)
- [ ] 12.8.3 — Message feedback: thumbs up/down per assistant message
- [ ] 12.8.4 — Error messages with retry button
- [ ] 12.8.5 — Session timeout warning with extend option

#### 12.9 — Create `app/server.py` entry point

#### 12.10 — Test Web UI
- [ ] 12.10.1 — WebSocket connection + reconnect test
- [ ] 12.10.2 — Streaming response rendering test
- [ ] 12.10.3 — Arabic RTL rendering test
- [ ] 12.10.4 — File upload flow test
- [ ] 12.10.5 — Settings persistence test
- [ ] 12.10.6 — Conversation CRUD test
- [ ] 12.10.7 — Responsive layout test (mobile / tablet / desktop)

### Voice pipeline — speak and listen (Arabic + English)
- [ ] **12.11** — Create `models/speech/stt.py` — Speech-to-Text (Whisper)
  - [ ] 12.11.1 — Load Whisper medium model
  - [ ] 12.11.2 — `record_audio(duration)` — capture from microphone
  - [ ] 12.11.3 — `transcribe(audio)` — convert speech to text
  - [ ] 12.11.4 — Auto-detect language (Arabic/English)
  - [ ] 12.11.5 — Handle background noise

- [ ] **12.12** — Create `models/speech/tts.py` — Text-to-Speech (Piper)
  - [ ] 12.12.1 — Load Piper Arabic voice model
  - [ ] 12.12.2 — Load Piper English voice model
  - [ ] 12.12.3 — `synthesize(text, lang)` → audio bytes
  - [ ] 12.12.4 — `play(audio)` — play audio output
  - [ ] 12.12.5 — Language auto-detect → select voice

- [ ] **12.13** — Create `interfaces/voice/wake_word.py` — Wake Word listener
  - [ ] 12.13.1 — Load openWakeWord model
  - [ ] 12.13.2 — Continuous microphone monitoring
  - [ ] 12.13.3 — Detect "Hey Jarvis" trigger
  - [ ] 12.13.4 — Fire event on wake word detection
  - [ ] 12.13.5 — Visual + audio confirmation feedback

- [ ] **12.14** — Create `interfaces/voice/voice_interface.py` — full pipeline
  - [ ] 12.14.1 — Wait for wake word → record → transcribe → orchestrator → synthesize → play → listen

- [ ] **12.15** — Silence detection and noise handling
  - [ ] 12.15.1 — VAD-based end-of-speech detection
  - [ ] 12.15.2 — Noise reduction filter + gain normalization

- [ ] **12.16** — Test voice pipeline
  - [ ] 12.16.1 — Wake word detection test
  - [ ] 12.16.2 — Arabic STT accuracy test
  - [ ] 12.16.3 — TTS output quality test

### Vision & image generation
- [ ] **12.17** — Create `models/vision/engine.py` — image understanding
  - [ ] 12.17.1 — Load LLaVA via Ollama
  - [ ] 12.17.2 — `describe(image_path, question)` → text description
  - [ ] 12.17.3 — Encode image to base64 for Ollama
  - [ ] 12.17.4 — OCR capability (read text in images)

- [ ] **12.18** — Create `models/diffusion/generator.py` — image generation
  - [ ] 12.18.1 — Load Stable Diffusion 1.5 with float16
  - [ ] 12.18.2 — `generate(prompt, width, height, steps)` → PIL Image
  - [ ] 12.18.3 — VRAM management (unload when not in use)
  - [ ] 12.18.4 — Save generated images to disk
  - [ ] 12.18.5 — Negative prompt support

- [ ] **12.19** — Integrate vision into orchestrator + router
  - [ ] 12.19.1 — Detect image attached to message
  - [ ] 12.19.2 — Auto-route to vision engine
  - [ ] 12.19.3 — Combine vision output with LLM response

- [ ] **12.20** — Test vision pipeline
  - [ ] 12.20.1 — Image description test
  - [ ] 12.20.2 — Image generation test
  - [ ] 12.20.3 — OCR test

- [ ] **12.21** — Web UI Dashboard panel (NEW)
  - [ ] 12.21.1 — Real-time VRAM meter (poll Ollama API for GPU stats)
  - [ ] 12.21.2 — Active tool panel: show which tool is currently running
  - [ ] 12.21.3 — Task queue viewer: list of pending/running/completed tasks
  - [ ] 12.21.4 — Memory browser: search long-term memory from Web UI
  - [ ] 12.21.5 — Model selector panel: switch active model from Web UI
  - [ ] 12.21.6 — System status card: CPU%, RAM, disk, GPU all in one view

- [ ] **12.22** — Voice: Voice Activity Detection (VAD) (NEW)
  - [ ] 12.22.1 — Auto-stop recording when user stops speaking (silence detection)
  - [ ] 12.22.2 — Use `webrtcvad` or energy threshold method
  - [ ] 12.22.3 — Configurable silence threshold and min/max recording duration
  - [ ] 12.22.4 — Integrate into voice_interface.py pipeline (replaces fixed-duration recording)

- [ ] **12.23** — Voice: Mid-sentence language detection (NEW)
  - [ ] 12.23.1 — Detect dominant language in Whisper output (Arabic vs English)
  - [ ] 12.23.2 — Auto-select TTS voice: Arabic Piper voice OR English voice
  - [ ] 12.23.3 — Handle code-switching (Arabic sentence with English terms)

---

## 📱 Phase 13 — Telegram Interface
> **Goal:** Full Jarvis capabilities via Telegram bot.
> **Dependency:** Phase 12 (voice pipeline for voice message handling)

- [ ] **13.1** — Create `interfaces/telegram/bot.py` — bot setup
  - [ ] 13.1.1 — Initialize python-telegram-bot Application
  - [ ] 13.1.2 — Register all handlers
  - [ ] 13.1.3 — Start polling

- [ ] **13.2** — Create `interfaces/telegram/handlers.py` — message handlers
  - [ ] 13.2.1 — Text message → orchestrator → reply
  - [ ] 13.2.2 — Photo message → vision engine → reply
  - [ ] 13.2.3 — Voice message → STT → orchestrator → reply
  - [ ] 13.2.4 — Document message → reader tool → reply

- [ ] **13.3** — Create `interfaces/telegram/commands.py` — bot commands
  - [ ] 13.3.1 — `/start` — welcome message
  - [ ] 13.3.2 — `/clear` — clear conversation
  - [ ] 13.3.3 — `/model` — switch model
  - [ ] 13.3.4 — `/image [prompt]` — generate image
  - [ ] 13.3.5 — `/search [query]` — web search

- [ ] **13.4** — Streaming response simulation for Telegram
  - [ ] 13.4.1 — "Typing..." indicator while generating
  - [ ] 13.4.2 — Edit message as tokens arrive

- [ ] **13.5** — Media handling
  - [ ] 13.5.1 — Download photos and pass to vision
  - [ ] 13.5.2 — Download voice notes and pass to STT
  - [ ] 13.5.3 — Send generated images back to user

- [ ] **13.6** — Test Telegram bot
  - [ ] 13.6.1 — Conversation test
  - [ ] 13.6.2 — Image upload test
  - [ ] 13.6.3 — Voice message test

---

## 🖥️ Phase 14 — GUI Desktop App
> **Goal:** Native Windows desktop window with full Jarvis interface.
> **Dependency:** Phase 4 (CLI patterns), Phase 12 (voice integration)

- [ ] **14.1** — Create `interfaces/gui/main_window.py` — PyQt6 desktop app
  - [ ] 14.1.1 — Chat message area (scrollable)
  - [ ] 14.1.2 — Input text box
  - [ ] 14.1.3 — Send button
  - [ ] 14.1.4 — Model selector dropdown
  - [ ] 14.1.5 — Microphone button (voice input)

- [ ] **14.2** — Create `interfaces/gui/settings_dialog.py`
  - [ ] 14.2.1 — Model selection
  - [ ] 14.2.2 — Language preference
  - [ ] 14.2.3 — Voice settings

- [ ] **14.3** — Arabic RTL text rendering in GUI
  - [ ] 14.3.1 — Set Qt layout direction for Arabic
  - [ ] 14.3.2 — RTL text alignment in chat bubbles

- [ ] **14.4** — System tray integration
  - [ ] 14.4.1 — Minimize to system tray
  - [ ] 14.4.2 — Wake word activates window
  - [ ] 14.4.3 — Tray menu: Open, Settings, Quit

- [ ] **14.5** — Test GUI
  - [ ] 14.5.1 — Conversation test
  - [ ] 14.5.2 — Settings dialog test

- [ ] **14.12** — Jarvis system tray (Windows)
  - [ ] 14.12.1 — Run as background process: pystray tray icon
  - [ ] 14.12.2 — Right-click tray menu: Open GUI / Open Web UI / Settings / Quit
  - [ ] 14.12.3 — Wake word detection activates GUI window from tray
  - [ ] 14.12.4 — Notification integration: tray shows Windows toast via 6.6
  - [ ] 14.12.5 — Auto-start on Windows login (optional, user-toggle in settings)

- [ ] **14.13** — Clipboard integration in GUI
  - [ ] 14.13.1 — "Analyze clipboard" button: send clipboard content to Jarvis
  - [ ] 14.13.2 — Auto-detect clipboard type: code / URL / plain text / image
  - [ ] 14.13.3 — One-click: translate clipboard, summarize clipboard, explain clipboard

---

## ✅ Phase 15 — QA + Optimization + Security
> **Goal:** Production-hardened, fast, safe, and fully documented.
> **Dependency:** All phases complete.

- [ ] **15.1** — Create `tests/` test suite
  - [ ] 15.1.1 — `tests/test_llm.py` — LLM engine tests
  - [ ] 15.1.2 — `tests/test_memory.py` — memory system tests
  - [ ] 15.1.3 — `tests/test_tools.py` — tool registry + representative tools
  - [ ] 15.1.4 — `tests/test_voice.py` — STT/TTS pipeline test
  - [ ] 15.1.5 — `tests/test_vision.py` — vision engine test
  - [ ] 15.1.6 — `tests/test_runtime.py` — loop + executor boundaries
  - [ ] 15.1.7 — `tests/test_identity.py` — prompt builder output consistency
  - [ ] 15.1.8 — `tests/test_context_buffer.py` — buffer lifecycle tests

- [ ] **15.2** — Performance optimization (Overcoming Hardware Constraints)
  - [ ] 15.2.1 — Profile slow operations
  - [ ] 15.2.2 — Model preloading strategy (VRAM-safe)
  - [ ] 15.2.3 — Response caching for repeated queries
  - [ ] 15.2.4 — Async all I/O operations
  - [ ] 15.2.5 — Vector Database Speed Optimization (Batched embedding ingestion to prevent RAM spikes on large PDFs)
  - [ ] 15.2.6 — Context Window Compression (Auto-summarize middle-history so the GPU avoids re-processing 8k+ tokens)
  - [ ] 15.2.7 — Tool Execution Parallelism (Run multiple independent I/O tools simultaneously without locking the orchestrator)
  - [ ] 15.2.8 — Hardware Control: Enforce Flash Attention locally on Ollama runtimes for deep/planning modes
  - [ ] 15.2.9 — Auto-KV Cache Management: dynamically adjust context window limits based on real-time VRAM usage

- [ ] **15.3** — Error handling and resilience
  - [ ] 15.3.1 — Graceful Ollama connection failure
  - [ ] 15.3.2 — Model loading failure fallback
  - [ ] 15.3.3 — Tool execution error recovery
  - [ ] 15.3.4 — Retry logic with exponential backoff
  - [ ] 15.3.5 — End-to-end error class → retry / switch model tests

- [ ] **15.4** — Logging and monitoring
  - [ ] 15.4.1 — Structured logging (Loguru)
  - [ ] 15.4.2 — Log all model calls with latency
  - [ ] 15.4.3 — Log all tool executions
  - [ ] 15.4.4 — Log errors with full stack trace

- [ ] **15.5** — Windows compatibility
  - [ ] 15.5.1 — Test all features on Windows 11 + PowerShell
  - [ ] 15.5.2 — Path handling (Windows vs Linux)
  - [ ] 15.5.3 — Audio device detection on Windows
  - [ ] 15.5.4 — Verify `scripts/install.ps1` on clean system

- [ ] **15.6** — Security review
  - [ ] 15.6.1 — Sandbox code execution (no system access)
  - [ ] 15.6.2 — Validate all user inputs and tool args
  - [ ] 15.6.3 — Secure API key storage

- [ ] **15.7** — Update documentation
  - [ ] 15.7.1 — Update README.md with final instructions
  - [ ] 15.7.2 — Add docstrings to all modules
  - [ ] 15.7.3 — Update TASKS.md progress table (all 16 phases)

- [ ] **15.8** — Final integration test
  - [ ] 15.8.1 — Full conversation in Arabic
  - [ ] 15.8.2 — Voice → response → TTS full cycle
  - [ ] 15.8.3 — Multi-step agent task
  - [ ] 15.8.4 — Telegram + Web simultaneously

- [ ] **15.9** — Continuous integration
  - [ ] 15.9.1 — GitHub Actions or pre-commit hooks for linting
  - [ ] 15.9.2 — Automated test run on push
  - [ ] 15.9.3 — Code coverage reporting

- [ ] **15.10** — Phase 6–8 skill integration tests
  - [ ] 15.10.1 — Open app → verify window active → close app test
  - [ ] 15.10.2 — Browser session → login → restart → verify session preserved
  - [ ] 15.10.3 — Gmail + Calendar same OAuth token test
  - [ ] 15.10.4 — Clipboard read → translate → write back test
  - [ ] 15.10.5 — Notification → user sees toast → acknowledged test

- [ ] **15.11** — Security review for system control tools
  - [ ] 15.11.1 — Confirm-before-execute for: delete file, kill process, send email, run shell
  - [ ] 15.11.2 — Allowlist for shell commands: reject rm -rf, format, etc.
  - [ ] 15.11.3 — Browser credential vault: encrypt session JSON at rest (Fernet)
  - [ ] 15.11.4 — Google OAuth token: stored in data/ (gitignored), not config/

- [ ] **15.12** — End-to-end integration tests (full scenarios)
  - [ ] 15.12.1 — "Send an email to X and add a Calendar reminder" — 2 tools, 1 OAuth token
  - [ ] 15.12.2 — "Open Notepad, type Hello, save as test.txt on Desktop" — app + keyboard + file
  - [ ] 15.12.3 — Voice → "what's on my screen?" → OCR + LLaVA → spoken answer
  - [ ] 15.12.4 — "Search YouTube for X, open first result" — search + browser
  - [ ] 15.12.5 — Multi-agent task: research + summarize + save to Drive

---

## 🎭 Phase 16 — Personality Layer
> **Goal:** Consistent Jarvis voice across all interfaces with adaptive tone.
> **Dependency:** All phases complete — this is polish, not function.

- [ ] **16.1** — Tone control — formal/casual/warm; locale-aware; user override via config + memory profile

- [ ] **16.2** — Response style — length presets; bullet vs prose; "teacher mode" vs "executive summary"

- [ ] **16.3** — Adaptive personality — drift slowly from Feedback (Phase 11) + explicit prefs; bounded deltas; audit log

- [ ] **16.4** — Integration — inject Personality fragments into mode packs + system prompts via 3.17; ensure router still picks model by capability

- [ ] **16.5** — Tests — A/B prompt fixtures; regression that safety refusals still occur when required

---

## 📌 Notes

### Model roles (match `ollama list`)
**Capability profiles** in `config/models.yaml` must use exact Ollama tag names for models you have pulled — the router has no use for names that are not installed.

**Current inventory (verify with `ollama list`):**
```
gemma3:4b          — Fast / lightweight; tight latency or low complexity
qwen3:8b           — General / balanced / deep reasoning (default "main" brain)
qwen2.5-coder:7b   — Code + execution tasks
llava:7b           — Vision
```

**Optional later pulls:** e.g. `qwen2.5:7b` as a lighter general alternative — not required for the roadmap.

### VRAM Budget (6 GB RTX 3050)
```
One heavy Ollama model at a time + unload before SD/vision swap
qwen3:8b        → ~5.0 GB
qwen2.5-coder:7b → ~4.7 GB
llava:7b        → ~4.5 GB
gemma3:4b       → ~3.0 GB
SD 1.5          → ~4.0 GB (float16)  — optional; unload Ollama first
```

### Priority Order for Development
1. Phases 1–3 (Foundation → LLM + Runtime → Memory + adaptive hooks)
2. Phase 4 CLI (fast feedback)
3. Phase 5 Tool System + parallel execution (enables real autonomy)
4. Phase 6 System Control Skills (apps, files, clipboard, notifications, OCR)
5. Phase 7 Browser & Web Skills
6. Phase 8 External APIs & Integrations
7. Phase 9 Agents (behaviors on top of tools)
8. Phase 10 Task Decomposition Engine (graphs, dependencies, selective retry)
9. Phase 11 Feedback & Learning (close the loop with memory + decision)
10. Phase 12 Web + Voice + Vision (multimodal surfaces)
11. Phase 13 Telegram Interface
12. Phase 14 GUI Desktop App
13. Phase 15 Optimization & QA
14. Phase 16 Personality (polish and adaptation last)

### Model Inventory (final — as of Phase 1 completion)
```
gemma3:4b          — Fast / lightweight; tight latency or low complexity
qwen3:8b           — General / balanced / deep reasoning (main brain)
qwen2.5-coder:7b   — Code + execution tasks
llava:7b           — Vision tasks
```
> `qwen2.5:7b` has been removed — superseded by `qwen3:8b` in all profiles.

### New Phase Skill Dependencies
```
Phase 6 requires: Phase 5 (tool registry)
Phase 7 requires: Phase 5 (tool registry), Phase 6 (file paths)
Phase 8 requires: Phase 5 (tool registry), Phase 7 (OAuth browser flow)
Phase 9 requires: Phases 5–8 (tools + browser + APIs)
Phase 10 requires: Phase 9 (agents as execution units)
Phase 11 requires: Phase 9 + 10 (outcomes to learn from)
Phase 12 requires: Phase 5+ (interfaces need real tools behind them)
Phase 13 requires: Phase 12 (voice pipeline for voice messages)
Phase 14 requires: Phase 4 + 12
Phase 15 requires: All phases feature-complete
Phase 16 requires: All phases complete
```

### Windows-Specific Libraries Required (add to requirements.txt)
```
pywin32        — Windows API (app window control, registry)
pycaw          — Windows audio (volume control)
pystray        — System tray icon
winotify       — Windows Toast notifications (or win10toast)
pyperclip      — Cross-platform clipboard (text)
pynput         — Global keyboard/mouse hooks
keyboard       — Global hotkey registration
mss            — Fast screen capture
pytesseract    — Lightweight OCR (requires Tesseract binary)
```

---

*Last updated: 2026-04-17 — Version 0.3.0-alpha (intelligence + identity roadmap)*
