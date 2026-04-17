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

---

## 📊 Progress Overview

| Phase | Tasks | Done | Progress |
|-------|-------|------|----------|
| Phase 1: Foundation | 8 | 8 | ██████████ 100% |
| Phase 2: LLM + Runtime + Decision | 26 | 26 | ██████████ 100% |
| Phase 3: Memory + Context Buffer + Identity | 20 | 20 | ██████████ 100% |
| Phase 4: CLI Interface | 6 | 0 | ░░░░░░░░░░ 0% |
| Phase 5: Tool System | 17 | 0 | ░░░░░░░░░░ 0% |
| Phase 6: Agents (Basic → Advanced) | 6 | 0 | ░░░░░░░░░░ 0% |
| Phase 7: Task Decomposition Engine | 8 | 0 | ░░░░░░░░░░ 0% |
| Phase 8: Feedback & Learning | 9 | 0 | ░░░░░░░░░░ 0% |
| Phase 9: Web + Voice + Vision | 32 | 0 | ░░░░░░░░░░ 0% |
| Phase 10: Integrations | 11 | 0 | ░░░░░░░░░░ 0% |
| Phase 11: QA + Optimize | 9 | 0 | ░░░░░░░░░░ 0% |
| Phase 12: Personality Layer | 5 | 0 | ░░░░░░░░░░ 0% |

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
  - [ ] 5.4.2 — Log tool latency, outcomes, and args fingerprint (for Phase 11 metrics)
  - [ ] 5.4.3 — Tool metrics collection: success rate, avg latency, error frequency per tool

- [ ] **5.5** — `skills/search/web_search.py` — web search tool
  - [ ] 5.5.1 — DuckDuckGo search (no API key needed)
  - [ ] 5.5.2 — Return top N results with title + snippet + URL
  - [ ] 5.5.3 — Fast scraping of result pages
  - [ ] 5.5.4 — Local SearxNG integration (optional)

- [ ] **5.6** — `skills/web/browser.py` — browser automation tool
  - [ ] 5.6.1 — Open URL in Playwright browser
  - [ ] 5.6.2 — Click elements by text/selector
  - [ ] 5.6.3 — Fill forms
  - [ ] 5.6.4 — Extract page content as text/markdown
  - [ ] 5.6.5 — Take screenshot of page

- [ ] **5.7** — `skills/control/files/` — file operations
  - [ ] 5.7.1 — List directory contents
  - [ ] 5.7.2 — Read file content
  - [ ] 5.7.3 — Write/create file
  - [ ] 5.7.4 — Move/copy/delete file
  - [ ] 5.7.5 — Search files by name/content

- [ ] **5.8** — `skills/control/system/` — system control
  - [ ] 5.8.1 — Get system info (CPU, RAM, disk)
  - [ ] 5.8.2 — List running processes
  - [ ] 5.8.3 — Kill process by name/PID
  - [ ] 5.8.4 — Get/set volume
  - [ ] 5.8.5 — Run shell command (sandboxed)

- [ ] **5.9** — `skills/control/apps/` — application control
  - [ ] 5.9.1 — Open application by name
  - [ ] 5.9.2 — Close application
  - [ ] 5.9.3 — List installed apps

- [ ] **5.10** — `skills/coder/executor.py` — code execution tool
  - [ ] 5.10.1 — Execute Python code safely
  - [ ] 5.10.2 — Execute shell commands
  - [ ] 5.10.3 — Capture stdout/stderr
  - [ ] 5.10.4 — Timeout protection
  - [ ] 5.10.5 — Return structured result to LLM

- [ ] **5.11** — `skills/api/google_calendar.py` — Google Calendar
  - [ ] 5.11.1 — OAuth2 authentication flow
  - [ ] 5.11.2 — List upcoming events
  - [ ] 5.11.3 — Create new event
  - [ ] 5.11.4 — Delete event
  - [ ] 5.11.5 — Search events

- [ ] **5.12** — `skills/api/youtube.py` — YouTube
  - [ ] 5.12.1 — Search videos
  - [ ] 5.12.2 — Get video info
  - [ ] 5.12.3 — Open video in browser

- [ ] **5.13** — `skills/reader/pdf/` — PDF reading
  - [ ] 5.13.1 — Extract text from PDF
  - [ ] 5.13.2 — Extract images from PDF
  - [ ] 5.13.3 — Summarize PDF via LLM

- [ ] **5.14** — `skills/reader/office/` — Office documents
  - [ ] 5.14.1 — Read Word (.docx) files
  - [ ] 5.14.2 — Read Excel (.xlsx) files
  - [ ] 5.14.3 — Read PowerPoint (.pptx) files

- [ ] **5.15** — Parallel execution system
  - [ ] 5.15.1 — Concurrent tool execution (no shared mutable resource)
  - [ ] 5.15.2 — Async runtime tasks with backpressure + cancellation
  - [ ] 5.15.3 — Background jobs for long I/O
  - [ ] 5.15.4 — Integration with Task Decomposition (Phase 7) scheduler

- [ ] **5.16** — Context Buffer ↔ executor / tools
  - [ ] 5.16.1 — Resolve buffer references to concrete file paths
  - [ ] 5.16.2 — Enforcement: no tool execution during staging; heavy pipelines only in Act

- [ ] **5.17** — Tool lifecycle management
  - [ ] 5.17.1 — Health check: verify external dependencies before first use
  - [ ] 5.17.2 — Graceful degradation: disable unavailable tools, report status
  - [ ] 5.17.3 — Resource cleanup: release browser instances, temp files on shutdown

---

## 🤖 Phase 6 — Agents (Basic → Advanced)
> **Goal:** Multi-step autonomy after tools exist

### Basic (core autonomy)
- [ ] **6.1** — Create `core/agents/planner/planner.py` — step decomposition + sequencing
  - [ ] 6.1.1 — Break complex request into ordered steps
  - [ ] 6.1.2 — Assign each step to a tool or model role
  - [ ] 6.1.3 — Execute steps sequentially via runtime
  - [ ] 6.1.4 — Pass output of step N as input to step N+1
  - [ ] 6.1.5 — Report progress to user

- [ ] **6.2** — Create `core/agents/thinker/thinker.py` — deeper reasoning
  - [ ] 6.2.1 — Extended Chain-of-Thought reasoning
  - [ ] 6.2.2 — Self-verification of answers
  - [ ] 6.2.3 — Confidence scoring

- [ ] **6.3** — ReAct loop integration (Reason + Act) with runtime
  - [ ] 6.3.1 — Observe → Think → Act → Observe with tool calls
  - [ ] 6.3.2 — Max iterations guard
  - [ ] 6.3.3 — Optional: show reasoning steps to user

### Advanced
- [ ] **6.4** — Create `core/agents/researcher.py` — deep research agent
  - [ ] 6.4.1 — Multi-query web search
  - [ ] 6.4.2 — Scrape and summarize multiple sources
  - [ ] 6.4.3 — Cross-reference and fact-check
  - [ ] 6.4.4 — Generate structured report

- [ ] **6.5** — `skills/screen/screen_agent.py` — visual computer control
  - [ ] 6.5.1 — Take screenshot
  - [ ] 6.5.2 — Describe screen via vision
  - [ ] 6.5.3 — Move mouse and click based on vision
  - [ ] 6.5.4 — Type text
  - [ ] 6.5.5 — Full GUI automation loop (guarded)

- [ ] **6.6** — Test agents
  - [ ] 6.6.1 — Multi-step task test
  - [ ] 6.6.2 — ReAct + tool calling test
  - [ ] 6.6.3 — Screen agent test

---

## 🧩 Phase 7 — Task Decomposition Engine
> **Goal:** Turn a goal into a structured plan — execution graph, dependencies, selective retry
> **Solution applied (Zero-Shot Limits):** Overcomes local LLM logic failure limits by breaking massive, abstract tasks (which crash 8B models) into tiny, measurable micro-tasks that small models excel at.

- [ ] **7.1** — Decomposition API — input: user goal + DecisionOutput; output: DAG of steps
  - [ ] 7.1.1 — Subtask schema: id, type, inputs/outputs, depends_on, retry_group
  - [ ] 7.1.2 — Break tasks into subtasks (LLM or template-assisted)
  - [ ] 7.1.3 — Human-in-the-loop nodes (optional approval gates)

- [ ] **7.2** — Execution graph runtime — deterministic scheduler
  - [ ] 7.2.1 — Topological order with parallel frontier
  - [ ] 7.2.2 — Handle dependencies: pass outputs as typed artifacts
  - [ ] 7.2.3 — Idempotency: stable keys for re-run after resume

- [ ] **7.3** — Retry only failed steps
  - [ ] 7.3.1 — Mark failed node with error class; skip successful siblings
  - [ ] 7.3.2 — Partial replan: optional subgraph regeneration

- [ ] **7.4** — Integration with agents + runtime
  - [ ] 7.4.1 — Planner (6.1) can delegate to engine
  - [ ] 7.4.2 — Dispatcher routes "complex plan" intents here

- [ ] **7.5** — Observability — export graph to logs/UI (Mermaid or JSON)

- [ ] **7.6** — Tests
  - [ ] 7.6.1 — Diamond dependency graph (parallel then join)
  - [ ] 7.6.2 — Failure mid-graph → retry one branch only
  - [ ] 7.6.3 — Resume after disconnect with same run_id

- [ ] **7.7** — Feedback hooks — on node success/failure emit signals for Phase 8

- [ ] **7.8** — Cost / budget awareness — inherit cost_estimate; prune when over budget

---

## 📈 Phase 8 — Feedback & Learning System
> **Goal:** Learn from implicit and explicit signals; persist attributed outcomes for memory and decision priors

- [ ] **8.1** — Implicit feedback detection
  - [ ] 8.1.1 — User continues: new message within τ → weak positive
  - [ ] 8.1.2 — User repeats question: rephrase → negative / confusion signal
  - [ ] 8.1.3 — User ignores response: no follow-up within session → weak negative

- [ ] **8.2** — Explicit feedback (optional UI) — thumbs up/down, correction messages

- [ ] **8.3** — Success / failure scoring — map events + Evaluate + error class to scalar per turn

- [ ] **8.4** — Store feedback linked to:
  - [ ] 8.4.1 — Decisions: snapshot DecisionOutput
  - [ ] 8.4.2 — Models: resolved model id + mode pack
  - [ ] 8.4.3 — Tools: tool name + version + args fingerprint

- [ ] **8.5** — Learning surfaces (incremental, safe)
  - [ ] 8.5.1 — Router weights: nudge scores from rolling aggregates
  - [ ] 8.5.2 — Escalation aggressiveness: tune thresholds
  - [ ] 8.5.3 — Memory writes: "what worked" summaries into long-term

- [ ] **8.6** — Privacy & controls — per-user opt-out; retention TTL; export/delete

- [ ] **8.7** — Integration tests — synthetic sessions; verify attribution chain

- [ ] **8.8** — Anti-feedback hacking — detect spam toggles; rate-limit weight updates

- [ ] **8.9** — Dashboard hooks (optional) — expose aggregates to Phase 11 monitoring

---

## 🌐 Phase 9 — Web + Voice + Vision
> **Goal:** Multimodal surfaces on top of the same runtime, tools, memory, and feedback loops

### Web UI — Glassmorphism + Frosted Acrylic AI Chat Interface
> **Design philosophy:** A premium, state-of-the-art chat interface that synthesizes the best UX patterns from modern AI platforms (ChatGPT, Claude, Gemini, Perplexity, HuggingChat) into a unified, beautiful, and cohesive design. Core aesthetic: **Glassmorphism** panels with **Frosted Acrylic/Lucite** depth layers, heavy blur compositing, and sophisticated micro-animations.

#### 9.1 — Backend: FastAPI Application (`interfaces/web/app.py`)
- [ ] 9.1.1 — Static files serving (CSS, JS, fonts, icons)
- [ ] 9.1.2 — Jinja2 template rendering with SSR fallback
- [ ] 9.1.3 — CORS configuration for development and production
- [ ] 9.1.4 — Session management middleware (session ID, expiry, cookie-based)
- [ ] 9.1.5 — Rate limiting middleware (per-session, per-IP)
- [ ] 9.1.6 — Gzip compression for static assets

#### 9.2 — WebSocket Handler (`interfaces/web/websocket.py`)
- [ ] 9.2.1 — Accept connection with session validation
- [ ] 9.2.2 — Receive message → pass to runtime / orchestrator with session context
- [ ] 9.2.3 — Stream response tokens back to client (JSON text frames)
- [ ] 9.2.4 — Handle disconnection gracefully (cleanup state, log)
- [ ] 9.2.5 — Auto-reconnect protocol: client detects disconnect → reconnect → resume stream
- [ ] 9.2.6 — Heartbeat / ping-pong keep-alive to detect stale connections
- [ ] 9.2.7 — Support concurrent sessions per user (multiple tabs)

#### 9.3 — Chat Page (`interfaces/web/templates/index.html`)
- [ ] 9.3.1 — Single-page chat application (no framework, vanilla JS)
- [ ] 9.3.2 — Responsive layout: fluid mobile-first, desktop-optimized
- [ ] 9.3.3 — Arabic RTL support: auto-detect text direction, proper alignment
- [ ] 9.3.4 — Streaming message display with real-time animated cursor
- [ ] 9.3.5 — Code blocks with syntax highlighting (Highlight.js or Prism) + copy-to-clipboard button
- [ ] 9.3.6 — Markdown rendering for assistant responses (headings, lists, bold, links, tables)
- [ ] 9.3.7 — LaTeX / math equation rendering (KaTeX inline)
- [ ] 9.3.8 — Image preview for uploaded / generated images (lightbox on click)
- [ ] 9.3.9 — File attachment cards: filename, size, type icon, remove button
- [ ] 9.3.10 — Message actions: copy full message, regenerate, edit user message, delete

#### 9.4 — Design System: Glassmorphism + Frosted Acrylic Aesthetic (`interfaces/web/static/style.css`)

##### 9.4.1 — Color System & Theme Engine
- [ ] 9.4.1.1 — **Dark theme (default):** deep navy/charcoal base (`#0a0a1a`, `#12122a`), frosted glass panels with `rgba(255,255,255,0.04–0.08)` backgrounds
- [ ] 9.4.1.2 — **Accent gradients:** electric blue → teal → violet (`#3b82f6` → `#06b6d4` → `#8b5cf6`), used in action buttons, active states, and glow effects
- [ ] 9.4.1.3 — **Light theme:** soft white/cream base, warm gray panels with frosted overlays, muted accents
- [ ] 9.4.1.4 — **Theme toggle:** smooth CSS transition (0.4s ease) between dark↔light; persist in localStorage
- [ ] 9.4.1.5 — **CSS custom properties:** full token system (`--color-bg-primary`, `--glass-blur`, `--border-glow`, `--shadow-depth`) for easy theme extension
- [ ] 9.4.1.6 — **Luminous glow effects:** subtle box-shadow halos on active elements (`0 0 20px rgba(59,130,246,0.15)`)

##### 9.4.2 — Glass & Blur Compositing
- [ ] 9.4.2.1 — **Multi-layer blur depth:** ambient background blur (24px), sidebar glass (16px), card-level blur (12px), input bar blur (8px)
- [ ] 9.4.2.2 — **Frosted glass panels:** `backdrop-filter: blur()` + `background: rgba()` + subtle `border: 1px solid rgba(255,255,255,0.06)`
- [ ] 9.4.2.3 — **Depth layers:** z-index system with opacity gradient — deeper = more opaque, surface = more transparent
- [ ] 9.4.2.4 — **Inner light borders:** 1px top/left border with `rgba(255,255,255,0.08)` to simulate light refraction
- [ ] 9.4.2.5 — **Background ambient mesh:** CSS radial gradients at positions behind content (moving or fixed), creating a living background under glass

##### 9.4.3 — Typography
- [ ] 9.4.3.1 — **Primary font:** Inter (Google Fonts) — fallback: system-ui, -apple-system, sans-serif
- [ ] 9.4.3.2 — **Monospace font:** JetBrains Mono or Fira Code — for code blocks and technical output
- [ ] 9.4.3.3 — **Type scale:** 12px / 14px / 16px / 18px / 24px / 32px with proper line-height and letter-spacing
- [ ] 9.4.3.4 — **Arabic typography:** Noto Sans Arabic or IBM Plex Arabic for RTL content with correct bidi handling

##### 9.4.4 — Icons
- [ ] 9.4.4.1 — **Icon library:** Lucide Icons (consistent weight, radius, and style)
- [ ] 9.4.4.2 — **Icon sizing:** 16px (inline), 20px (buttons), 24px (navigation), 32px (features)
- [ ] 9.4.4.3 — **Icon colors:** inherit from text color; accent color on hover/active states
- [ ] 9.4.4.4 — **Mode icons:** unique icon per thinking mode — lightning (fast), brain (normal), atom (deep), layers (planning), telescope (research)
- [ ] 9.4.4.5 — **Animated icons:** subtle scale (1.1×) + color transition on hover

##### 9.4.5 — Animations & Micro-Interactions
- [ ] 9.4.5.1 — **Message entry:** staggered scale+fade from bottom (0→1 opacity, 0.95→1 scale, 0.3s cubic-bezier)
- [ ] 9.4.5.2 — **Typing indicator:** 3-dot pulse animation with sequential delay (0.6s period)
- [ ] 9.4.5.3 — **Loading skeleton:** shimmer gradient sweep (left→right, 1.5s, infinite) on glassmorphic placeholder cards
- [ ] 9.4.5.4 — **Button hover:** glow intensify (box-shadow spread), border brighten, background lighten — smooth 0.2s transition
- [ ] 9.4.5.5 — **Sidebar open/close:** slide + fade (transform: translateX + opacity, 0.3s ease-out)
- [ ] 9.4.5.6 — **Theme transition:** cross-fade all color custom properties with 0.4s ease
- [ ] 9.4.5.7 — **Scroll-to-bottom:** smooth scroll with CSS `scroll-behavior: smooth`; auto-scroll on new messages
- [ ] 9.4.5.8 — **Input focus:** border glow intensify + subtle shadow expansion
- [ ] 9.4.5.9 — **Toast notifications:** slide-in from top-right with fade, auto-dismiss after 4s
- [ ] 9.4.5.10 — **Parallax ambient background:** subtle movement on mouse move (CSS transform or JS requestAnimationFrame)

#### 9.5 — Input Bar System (`interfaces/web/static/chat.js`)

##### 9.5.1 — Smart Text Input
- [ ] 9.5.1.1 — **Multilingual text bar:** contenteditable div or textarea with full Unicode support (Arabic, English, Chinese, etc.)
- [ ] 9.5.1.2 — **Auto-expanding height:** grow with content (min 1 line → max 8 lines), then scroll internally
- [ ] 9.5.1.3 — **Placeholder text:** "Message Jarvis..." (disappears on focus/type)
- [ ] 9.5.1.4 — **RTL auto-detection:** switch text direction based on first character typed
- [ ] 9.5.1.5 — **Keyboard shortcuts:** Enter to send, Shift+Enter for newline, Escape to clear

##### 9.5.2 — Attachment System (+ Button)
- [ ] 9.5.2.1 — **"+" button:** positioned left of the text input; opens attachment menu on click
- [ ] 9.5.2.2 — **Attachment menu:** popup with options: Upload File, Upload Image, Take Photo (mobile), Paste from Clipboard
- [ ] 9.5.2.3 — **File upload:** accept any file type; drag-and-drop support on entire chat area
- [ ] 9.5.2.4 — **Image upload:** accept images with inline preview thumbnail above the input bar
- [ ] 9.5.2.5 — **Clipboard paste:** auto-detect image paste (Ctrl+V) and attach
- [ ] 9.5.2.6 — **Attachment preview strip:** horizontal row above input showing attached files with remove (×) button per item
- [ ] 9.5.2.7 — **Multiple attachments:** allow stacking multiple files/images before sending
- [ ] 9.5.2.8 — **File type icons:** show appropriate icon per file type (PDF, doc, image, audio, code, etc.)
- [ ] 9.5.2.9 — **Size validation:** reject files over configurable max size; show friendly error toast
- [ ] 9.5.2.10 — **Upload progress:** animated progress bar on large files

##### 9.5.3 — Mode Selector (Icon Row)
- [ ] 9.5.3.1 — **Mode icon bar:** row of clickable icons next to the "+" button, each representing a thinking mode
- [ ] 9.5.3.2 — **Normal mode icon (default):** brain icon — balanced response
- [ ] 9.5.3.3 — **Deep thinking icon:** atom/nucleus icon — extended chain-of-thought
- [ ] 9.5.3.4 — **Research mode icon:** telescope/magnifying glass — multi-source, tool-heavy
- [ ] 9.5.3.5 — **Planning mode icon:** layers/stack icon — decompose into steps
- [ ] 9.5.3.6 — **Fast mode icon:** lightning bolt — quick, concise answers
- [ ] 9.5.3.7 — **Active mode indicator:** highlighted/glowing icon with accent color when selected
- [ ] 9.5.3.8 — **Mode tooltip:** hover shows mode name and brief description
- [ ] 9.5.3.9 — **Mode persists:** selected mode persists until user changes it
- [ ] 9.5.3.10 — **Compact/expand:** on small screens, collapse into a single dropdown selector

##### 9.5.4 — Send / Voice Button (Dynamic)
- [ ] 9.5.4.1 — **Empty input → microphone icon:** when text bar is empty, show a microphone icon as send button
- [ ] 9.5.4.2 — **Typing → send arrow icon:** when user types any character, morph into a send (arrow-up) icon
- [ ] 9.5.4.3 — **Icon morph animation:** smooth transition between mic ↔ send (scale + fade crossover, 0.2s)
- [ ] 9.5.4.4 — **Voice mode activation:** clicking mic icon activates speech-to-text recording mode
- [ ] 9.5.4.5 — **Recording indicator:** pulsing red ring around mic icon; waveform visualization in input area
- [ ] 9.5.4.6 — **Stop recording:** click mic again or press Enter to send transcribed text
- [ ] 9.5.4.7 — **Send button states:** idle, hover (glow), active (pressed scale), loading (spinner while processing)
- [ ] 9.5.4.8 — **Disable on empty:** send button is non-interactive when input is empty (mic mode takes priority)

#### 9.6 — Sidebar System

##### 9.6.1 — Sidebar Layout & Structure
- [ ] 9.6.1.1 — **Collapsible sidebar:** left-side panel with frosted glass background, slide animation
- [ ] 9.6.1.2 — **Toggle button:** hamburger / X icon at top of sidebar or main area
- [ ] 9.6.1.3 — **Sidebar width:** 280px desktop; full-width overlay on mobile
- [ ] 9.6.1.4 — **Persistent state:** remember open/closed state in localStorage
- [ ] 9.6.1.5 — **Resize handle:** optional drag-to-resize sidebar width (min 240px, max 400px)

##### 9.6.2 — Conversation History Section
- [ ] 9.6.2.1 — **Conversation list:** scrollable list of past conversations, sorted by last activity (newest first)
- [ ] 9.6.2.2 — **Conversation card:** title (auto-generated or user-edited), last message preview, timestamp, message count
- [ ] 9.6.2.3 — **Active conversation highlight:** accent border-left or background tint
- [ ] 9.6.2.4 — **New conversation button:** prominent "+" or "New Chat" button at top
- [ ] 9.6.2.5 — **Edit title:** inline edit (click pencil icon → contenteditable → Enter to save)
- [ ] 9.6.2.6 — **Delete conversation:** swipe or right-click context menu → confirmation dialog → delete
- [ ] 9.6.2.7 — **Archive conversation:** move to archive section (collapsible "Archived" folder at bottom)
- [ ] 9.6.2.8 — **Pin conversation:** pin to top of list (star icon toggle)
- [ ] 9.6.2.9 — **Conversation grouping:** auto-group by date: Today, Yesterday, Previous 7 Days, Previous 30 Days, Older
- [ ] 9.6.2.10 — **Bulk actions:** multi-select with checkboxes → bulk delete / archive / export

##### 9.6.3 — Search System
- [ ] 9.6.3.1 — **Search bar:** positioned above conversation list; frosted glass input with search icon
- [ ] 9.6.3.2 — **Search by title:** filter conversations by matching title text (instant, client-side)
- [ ] 9.6.3.3 — **Search within conversations:** full-text search across all message content (server-side via memory)
- [ ] 9.6.3.4 — **Search results:** highlighted matching text snippets with conversation title and date
- [ ] 9.6.3.5 — **Search keyboard shortcut:** Ctrl+K or Cmd+K opens search with focus
- [ ] 9.6.3.6 — **Clear search:** X button or Escape to clear and return to full list

##### 9.6.4 — Settings Panel
- [ ] 9.6.4.1 — **Settings button:** gear icon at bottom of sidebar; opens settings panel (slide-in overlay or modal)
- [ ] 9.6.4.2 — **Appearance settings:**
  - [ ] 9.6.4.2.1 — Theme selector: Dark / Light / System (auto)
  - [ ] 9.6.4.2.2 — Accent color picker: preset palette or custom hex
  - [ ] 9.6.4.2.3 — Font size: slider (Small / Medium / Large / Extra Large)
  - [ ] 9.6.4.2.4 — Message density: Compact / Comfortable / Spacious
  - [ ] 9.6.4.2.5 — Blur intensity: slider (None / Light / Medium / Heavy) for accessibility
  - [ ] 9.6.4.2.6 — Animation toggle: enable/disable all animations (reduce motion preference)
  - [ ] 9.6.4.2.7 — Chat bubble style: rounded / squared / minimal
- [ ] 9.6.4.3 — **Behavior settings:**
  - [ ] 9.6.4.3.1 — Default thinking mode selector
  - [ ] 9.6.4.3.2 — Default language: Arabic / English / Auto-detect
  - [ ] 9.6.4.3.3 — Response style: Concise / Balanced / Detailed
  - [ ] 9.6.4.3.4 — Auto-scroll on new messages: toggle
  - [ ] 9.6.4.3.5 — Sound notifications: toggle + volume
  - [ ] 9.6.4.3.6 — Enter key behavior: Send message / New line
  - [ ] 9.6.4.3.7 — Show model/mode indicator in chat: toggle
  - [ ] 9.6.4.3.8 — Show confidence scores: toggle
- [ ] 9.6.4.4 — **Model settings:**
  - [ ] 9.6.4.4.1 — Active model selector (dropdown of available Ollama models)
  - [ ] 9.6.4.4.2 — Temperature slider (0.0 – 1.5)
  - [ ] 9.6.4.4.3 — Max tokens slider
  - [ ] 9.6.4.4.4 — Model override toggle: always use selected model vs auto-route
- [ ] 9.6.4.5 — **Data & Privacy:**
  - [ ] 9.6.4.5.1 — Export all conversations (JSON/Markdown)
  - [ ] 9.6.4.5.2 — Clear all conversations (with confirmation)
  - [ ] 9.6.4.5.3 — Clear memory (short-term / long-term / all)
  - [ ] 9.6.4.5.4 — Reset user profile to defaults
- [ ] 9.6.4.6 — **About section:** version, build info, system status, link to documentation

#### 9.7 — REST API Routes (`interfaces/web/routes/`)
- [ ] 9.7.1 — `GET /` — serve chat page
- [ ] 9.7.2 — `GET /api/models` — list available models with status
- [ ] 9.7.3 — `GET /api/conversations` — list all conversations (paginated)
- [ ] 9.7.4 — `GET /api/conversations/:id` — get conversation messages
- [ ] 9.7.5 — `PUT /api/conversations/:id` — update conversation title
- [ ] 9.7.6 — `DELETE /api/conversations/:id` — delete conversation
- [ ] 9.7.7 — `POST /api/conversations/:id/archive` — archive/unarchive conversation
- [ ] 9.7.8 — `GET /api/memory` — get conversation history summary
- [ ] 9.7.9 — `DELETE /api/memory` — clear conversation memory
- [ ] 9.7.10 — `POST /api/upload` — file upload endpoint (returns file reference ID)
- [ ] 9.7.11 — `GET /api/settings` — get user settings
- [ ] 9.7.12 — `PUT /api/settings` — update user settings
- [ ] 9.7.13 — `GET /api/search` — search across conversations

#### 9.8 — Notification & Feedback System
- [ ] 9.8.1 — Toast notification system (success, error, info, warning)
- [ ] 9.8.2 — Connection status indicator (connected / reconnecting / offline badge)
- [ ] 9.8.3 — Message feedback: thumbs up/down per assistant message
- [ ] 9.8.4 — Error messages with retry button
- [ ] 9.8.5 — Session timeout warning with extend option

#### 9.9 — Create `app/server.py` entry point

#### 9.10 — Test Web UI
- [ ] 9.10.1 — WebSocket connection + reconnect test
- [ ] 9.10.2 — Streaming response rendering test
- [ ] 9.10.3 — Arabic RTL rendering test
- [ ] 9.10.4 — File upload flow test
- [ ] 9.10.5 — Settings persistence test
- [ ] 9.10.6 — Conversation CRUD test
- [ ] 9.10.7 — Responsive layout test (mobile / tablet / desktop)

### Voice pipeline — speak and listen (Arabic + English)
- [ ] **9.11** — Create `models/speech/stt.py` — Speech-to-Text (Whisper)
  - [ ] 9.11.1 — Load Whisper medium model
  - [ ] 9.11.2 — `record_audio(duration)` — capture from microphone
  - [ ] 9.11.3 — `transcribe(audio)` — convert speech to text
  - [ ] 9.11.4 — Auto-detect language (Arabic/English)
  - [ ] 9.11.5 — Handle background noise

- [ ] **9.12** — Create `models/speech/tts.py` — Text-to-Speech (Piper)
  - [ ] 9.12.1 — Load Piper Arabic voice model
  - [ ] 9.12.2 — Load Piper English voice model
  - [ ] 9.12.3 — `synthesize(text, lang)` → audio bytes
  - [ ] 9.12.4 — `play(audio)` — play audio output
  - [ ] 9.12.5 — Language auto-detect → select voice

- [ ] **9.13** — Create `interfaces/voice/wake_word.py` — Wake Word listener
  - [ ] 9.13.1 — Load openWakeWord model
  - [ ] 9.13.2 — Continuous microphone monitoring
  - [ ] 9.13.3 — Detect "Hey Jarvis" trigger
  - [ ] 9.13.4 — Fire event on wake word detection
  - [ ] 9.13.5 — Visual + audio confirmation feedback

- [ ] **9.14** — Create `interfaces/voice/voice_interface.py` — full pipeline
  - [ ] 9.14.1 — Wait for wake word → record → transcribe → orchestrator → synthesize → play → listen

- [ ] **9.15** — Silence detection and noise handling
  - [ ] 9.15.1 — VAD-based end-of-speech detection
  - [ ] 9.15.2 — Noise reduction filter + gain normalization

- [ ] **9.16** — Test voice pipeline
  - [ ] 9.16.1 — Wake word detection test
  - [ ] 9.16.2 — Arabic STT accuracy test
  - [ ] 9.16.3 — TTS output quality test

### Vision & image generation
- [ ] **9.17** — Create `models/vision/engine.py` — image understanding
  - [ ] 9.17.1 — Load LLaVA via Ollama
  - [ ] 9.17.2 — `describe(image_path, question)` → text description
  - [ ] 9.17.3 — Encode image to base64 for Ollama
  - [ ] 9.17.4 — OCR capability (read text in images)

- [ ] **9.18** — Create `models/diffusion/generator.py` — image generation
  - [ ] 9.18.1 — Load Stable Diffusion 1.5 with float16
  - [ ] 9.18.2 — `generate(prompt, width, height, steps)` → PIL Image
  - [ ] 9.18.3 — VRAM management (unload when not in use)
  - [ ] 9.18.4 — Save generated images to disk
  - [ ] 9.18.5 — Negative prompt support

- [ ] **9.19** — Integrate vision into orchestrator + router
  - [ ] 9.19.1 — Detect image attached to message
  - [ ] 9.19.2 — Auto-route to vision engine
  - [ ] 9.19.3 — Combine vision output with LLM response

- [ ] **9.20** — Test vision pipeline
  - [ ] 9.20.1 — Image description test
  - [ ] 9.20.2 — Image generation test
  - [ ] 9.20.3 — OCR test

---

## 🔌 Phase 10 — Integrations (Telegram + GUI)
> **Goal:** Secondary surfaces sharing the same runtime and tools

### Telegram
- [ ] **10.1** — Create `interfaces/telegram/bot.py` — bot setup
  - [ ] 10.1.1 — Initialize python-telegram-bot Application
  - [ ] 10.1.2 — Register all handlers
  - [ ] 10.1.3 — Start polling

- [ ] **10.2** — Create `interfaces/telegram/handlers.py` — message handlers
  - [ ] 10.2.1 — Text message → orchestrator → reply
  - [ ] 10.2.2 — Photo message → vision engine → reply
  - [ ] 10.2.3 — Voice message → STT → orchestrator → reply
  - [ ] 10.2.4 — Document message → reader tool → reply

- [ ] **10.3** — Create `interfaces/telegram/commands.py` — bot commands
  - [ ] 10.3.1 — `/start` — welcome message
  - [ ] 10.3.2 — `/clear` — clear conversation
  - [ ] 10.3.3 — `/model` — switch model
  - [ ] 10.3.4 — `/image [prompt]` — generate image
  - [ ] 10.3.5 — `/search [query]` — web search

- [ ] **10.4** — Streaming response simulation for Telegram
  - [ ] 10.4.1 — "Typing..." indicator while generating
  - [ ] 10.4.2 — Edit message as tokens arrive

- [ ] **10.5** — Media handling
  - [ ] 10.5.1 — Download photos and pass to vision
  - [ ] 10.5.2 — Download voice notes and pass to STT
  - [ ] 10.5.3 — Send generated images back to user

- [ ] **10.6** — Test Telegram bot
  - [ ] 10.6.1 — Conversation test
  - [ ] 10.6.2 — Image upload test
  - [ ] 10.6.3 — Voice message test

### GUI Desktop
- [ ] **10.7** — Create `interfaces/gui/main_window.py` — PyQt6 desktop app
  - [ ] 10.7.1 — Chat message area (scrollable)
  - [ ] 10.7.2 — Input text box
  - [ ] 10.7.3 — Send button
  - [ ] 10.7.4 — Model selector dropdown
  - [ ] 10.7.5 — Microphone button (voice input)

- [ ] **10.8** — Create `interfaces/gui/settings_dialog.py`
  - [ ] 10.8.1 — Model selection
  - [ ] 10.8.2 — Language preference
  - [ ] 10.8.3 — Voice settings

- [ ] **10.9** — Arabic RTL text rendering in GUI
  - [ ] 10.9.1 — Set Qt layout direction for Arabic
  - [ ] 10.9.2 — RTL text alignment in chat bubbles

- [ ] **10.10** — System tray integration
  - [ ] 10.10.1 — Minimize to system tray
  - [ ] 10.10.2 — Wake word activates window
  - [ ] 10.10.3 — Tray menu: Open, Settings, Quit

- [ ] **10.11** — Test GUI
  - [ ] 10.11.1 — Conversation test
  - [ ] 10.11.2 — Settings dialog test

---

## ✅ Phase 11 — Optimization, QA & Production Hardening
> **Goal:** Production-ready, fast, stable, documented — performance, reliability, security, observability

- [ ] **11.1** — Create `tests/` test suite
  - [ ] 11.1.1 — `tests/test_llm.py` — LLM engine tests
  - [ ] 11.1.2 — `tests/test_memory.py` — memory system tests
  - [ ] 11.1.3 — `tests/test_tools.py` — tool registry + representative tools
  - [ ] 11.1.4 — `tests/test_voice.py` — STT/TTS pipeline test
  - [ ] 11.1.5 — `tests/test_vision.py` — vision engine test
  - [ ] 11.1.6 — `tests/test_runtime.py` — loop + executor boundaries
  - [ ] 11.1.7 — `tests/test_identity.py` — prompt builder output consistency
  - [ ] 11.1.8 — `tests/test_context_buffer.py` — buffer lifecycle tests

- [ ] **11.2** — Performance optimization (Overcoming Hardware Constraints)
  - [ ] 11.2.1 — Profile slow operations
  - [ ] 11.2.2 — Model preloading strategy (VRAM-safe)
  - [ ] 11.2.3 — Response caching for repeated queries
  - [ ] 11.2.4 — Async all I/O operations
  - [ ] 11.2.5 — Vector Database Speed Optimization (Batched embedding ingestion to prevent RAM spikes on large PDFs)
  - [ ] 11.2.6 — Context Window Compression (Auto-summarize middle-history so the GPU avoids re-processing 8k+ tokens)
  - [ ] 11.2.7 — Tool Execution Parallelism (Run multiple independent I/O tools simultaneously without locking the orchestrator)
  - [ ] 11.2.8 — Hardware Control: Enforce Flash Attention locally on Ollama runtimes for deep/planning modes
  - [ ] 11.2.9 — Auto-KV Cache Management: dynamically adjust context window limits based on real-time VRAM usage

- [ ] **11.3** — Error handling and resilience
  - [ ] 11.3.1 — Graceful Ollama connection failure
  - [ ] 11.3.2 — Model loading failure fallback
  - [ ] 11.3.3 — Tool execution error recovery
  - [ ] 11.3.4 — Retry logic with exponential backoff
  - [ ] 11.3.5 — End-to-end error class → retry / switch model tests

- [ ] **11.4** — Logging and monitoring
  - [ ] 11.4.1 — Structured logging (Loguru)
  - [ ] 11.4.2 — Log all model calls with latency
  - [ ] 11.4.3 — Log all tool executions
  - [ ] 11.4.4 — Log errors with full stack trace

- [ ] **11.5** — Windows compatibility
  - [ ] 11.5.1 — Test all features on Windows 11 + PowerShell
  - [ ] 11.5.2 — Path handling (Windows vs Linux)
  - [ ] 11.5.3 — Audio device detection on Windows
  - [ ] 11.5.4 — Verify `scripts/install.ps1` on clean system

- [ ] **11.6** — Security review
  - [ ] 11.6.1 — Sandbox code execution (no system access)
  - [ ] 11.6.2 — Validate all user inputs and tool args
  - [ ] 11.6.3 — Secure API key storage

- [ ] **11.7** — Update documentation
  - [ ] 11.7.1 — Update README.md with final instructions
  - [ ] 11.7.2 — Add docstrings to all modules
  - [ ] 11.7.3 — Update TASKS.md progress table (all 12 phases)

- [ ] **11.8** — Final integration test
  - [ ] 11.8.1 — Full conversation in Arabic
  - [ ] 11.8.2 — Voice → response → TTS full cycle
  - [ ] 11.8.3 — Multi-step agent task
  - [ ] 11.8.4 — Telegram + Web simultaneously

- [ ] **11.9** — Continuous integration
  - [ ] 11.9.1 — GitHub Actions or pre-commit hooks for linting
  - [ ] 11.9.2 — Automated test run on push
  - [ ] 11.9.3 — Code coverage reporting

---

## 🎭 Phase 12 — Personality Layer (tone, style, adaptation)
> **Goal:** Consistent Jarvis voice across interfaces while adapting to user prefs — composes with prompt packs and Adaptive Memory; does not bypass safety, caps, or tool policy

- [ ] **12.1** — Tone control — formal/casual/warm; locale-aware; user override via config + memory profile

- [ ] **12.2** — Response style — length presets; bullet vs prose; "teacher mode" vs "executive summary"

- [ ] **12.3** — Adaptive personality — drift slowly from Feedback (Phase 8) + explicit prefs; bounded deltas; audit log

- [ ] **12.4** — Integration — inject Personality fragments into mode packs + system prompts via 3.17; ensure router still picks model by capability

- [ ] **12.5** — Tests — A/B prompt fixtures; regression that safety refusals still occur when required

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
4. Phase 6 Agents (behaviors on top of tools)
5. Phase 7 Task Decomposition Engine (graphs, dependencies, selective retry)
6. Phase 8 Feedback & Learning (close the loop with memory + decision)
7. Phase 9 Web + Voice + Vision (multimodal surfaces)
8. Phase 10 Integrations
9. Phase 11 Optimization & QA
10. Phase 12 Personality (polish and adaptation last)

---

*Last updated: 2026-04-17 — Version 0.3.0-alpha (intelligence + identity roadmap)*
