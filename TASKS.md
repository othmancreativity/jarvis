# 🗂️ JARVIS — Task Board
> Full development roadmap from zero to complete system  
> Update checkboxes as you complete each task  
> **Phase order:** Foundation → **Runtime + Decision** → Memory (**incl. Context Buffer + Identity & Profiles**) → CLI → **Tool System** → **Basic Agents** → **Task Decomposition** → **Feedback & Learning** → **Web / Voice / Vision** → Integrations → **Optimization & QA** → **Personality**  
> **Intelligence is cross-cutting:** systems below are wired together — **feedback → memory** (signals update profiles and priors); **memory → decision** (preferences, failures, patterns); **decision → routing** (mode, model, tools); **runtime → evaluation** (turn outcomes feed self-eval, escalation, and feedback); **context buffer → observe → decision** (staged multimodal inputs before heavy work); **identity & profiles → every model call** (Jarvis + user + task context — models are **components**, not standalone products).  
> **Repo layout:** YAML under `config/`; Python settings (loader, Pydantic, paths, logging) under `settings/` — see [README.md](./README.md) (Project Structure).

---

## 🔗 System integration (non-optional)

- **Feedback & Learning** ↔ **Adaptive Memory:** implicit signals and explicit outcomes update user profile, tool/model priors, and recall of “what worked.”
- **Adaptive Memory** ↔ **Decision Layer:** retrieved facts + profile bias **intent**, **complexity**, **mode**, and **confidence** priors.
- **Decision Layer** ↔ **Model Router:** `DecisionOutput` + memory context → model selection and mode packs; **Error Intelligence** can override (retry / switch model / switch mode).
- **Runtime loop** ↔ **Self-Evaluation:** Evaluate stage consumes structured signals; persistence enables **resume** and **long-running** tracking.
- **Task Decomposition** ↔ **Parallel execution:** execution graph schedules concurrent steps where dependencies allow; failures map to **error class** + selective retry.
- **Personality Layer** ↔ **prompts + memory:** tone/style constraints compose with mode packs and learned preferences (without breaking safety caps).
- **Context Buffer** ↔ **Runtime (Observe)** ↔ **Decision** ↔ **Tools:** interfaces enqueue text/files/images/audio into a **staging** layer; **Observe** reads a **merged snapshot**; **Decision** uses that as the primary input signal; **heavy** models and tool-side readers run **only after** Decide (buffer remains **preparation-only**).
- **Identity & Profiles** ↔ **Memory (3.7 / 3.14)** ↔ **Decision** ↔ **Runtime** ↔ **Context Buffer:** **user profile** + **Jarvis system identity** feed **Observe** and **Decision** priors; **system prompt builder** (3.17) ensures **every** model sees **who Jarvis is**, **who the user is**, and **shared conversation/tool state** — **consistent** behavior across **all** routed models; buffer and memory supply **task** and **history** slices into the same builder.

---

## 📊 Progress Overview

| Phase | Tasks | Done | Progress |
|-------|-------|------|----------|
| Phase 1: Foundation | 8 | 8 | ██████████ 100% |
| Phase 2: LLM + Runtime + Decision | 26 | 22 | █████████░ ~85% |
| Phase 3: Memory (+ Adaptive + Context Buffer + Identity) | 20 | 0 | ░░░░░░░░░░ 0% |
| Phase 4: CLI Interface | 5 | 0 | ░░░░░░░░░░ 0% |
| Phase 5: Tool System (+ Parallel) | 16 | 0 | ░░░░░░░░░░ 0% |
| Phase 6: Agents (Basic → Advanced) | 6 | 0 | ░░░░░░░░░░ 0% |
| Phase 7: Task Decomposition Engine | 8 | 0 | ░░░░░░░░░░ 0% |
| Phase 8: Feedback & Learning | 9 | 0 | ░░░░░░░░░░ 0% |
| Phase 9: Web + Voice + Vision | 23 | 0 | ░░░░░░░░░░ 0% |
| Phase 10: Integrations | 11 | 0 | ░░░░░░░░░░ 0% |
| Phase 11: QA + Optimize | 8 | 0 | ░░░░░░░░░░ 0% |
| Phase 12: Personality Layer | 5 | 0 | ░░░░░░░░░░ 0% |

---

## 🏗️ Phase 1 — Foundation & Project Setup
> **Goal:** Working project skeleton, config system, logging, and base classes

- [x] **1.1** — Create `config/settings.yaml` with all app settings (models, interfaces, hardware limits)
  - [x] 1.1.1 — Add Jarvis name, language, wake_word settings
  - [x] 1.1.2 — Add model names **that match your Ollama pulls** (see **Notes → Model roles**): e.g. `gemma3:4b` (fast), `qwen3:8b` (general / balanced / deep), `qwen2.5-coder:7b` (coder), `llava:7b` (vision) — **no** hard-coded assumption of models you have not installed
  - [x] 1.1.3 — Add interface ports and hosts
  - [x] 1.1.4 — Add storage paths

- [x] **1.2** — Create `config/models.yaml` with model-specific parameters
  - [x] 1.2.1 — Temperature, top_p, max_tokens per model
  - [x] 1.2.2 — **Capability profiles** (reasoning tier, Arabic, code bias, latency, VRAM estimate) for **dynamic** routing — not static if→model rules
  - [x] 1.2.3 — Optional **routing weights** / thresholds (tunable without code changes)

- [x] **1.3** — Create `.env.example` with all required environment variables
  - [x] 1.3.1 — TELEGRAM_BOT_TOKEN
  - [x] 1.3.2 — GOOGLE_CLIENT_ID / SECRET
  - [x] 1.3.3 — YOUTUBE_API_KEY

- [x] **1.4** — Create `config/skills.yaml` — **tool/skill registry** (enable/disable, categories) and pointers to JSON schemas

- [x] **1.5** — Setup `requirements.txt` — complete and pinned dependencies
  - [x] 1.5.1 — Core: ollama, fastapi, uvicorn, pydantic
  - [x] 1.5.2 — Memory: chromadb, redis, sqlite3
  - [x] 1.5.3 — Audio: openai-whisper, piper-tts, openwakeword, pyaudio, sounddevice
  - [x] 1.5.4 — Vision: diffusers, torch, torchvision, Pillow
  - [x] 1.5.5 — Tools/skills: playwright, psutil, pyautogui, google-api-python-client
  - [x] 1.5.6 — Interfaces: python-telegram-bot, rich, tkinter/PyQt6
  - [x] 1.5.7 — Utils: loguru, pyyaml, python-dotenv, sentence-transformers

- [x] **1.6** — Create `app/main.py` — entry point with `--interface` argument parser
  - [x] 1.6.1 — Parse CLI args: `--interface [cli|web|telegram|gui|all]`
  - [x] 1.6.2 — Initialize logging with Loguru
  - [x] 1.6.3 — Load config from settings.yaml
  - [x] 1.6.4 — Launch selected interface(s)

- [x] **1.7** — Setup `scripts/install.sh` — full automated installation
  - [x] 1.7.1 — System packages (portaudio, ffmpeg, redis)
  - [x] 1.7.2 — Python venv creation
  - [x] 1.7.3 — pip install requirements
  - [x] 1.7.4 — Playwright browser install
  - [x] 1.7.5 — Whisper model download
  - [x] 1.7.6 — Piper voice download (Arabic)
  - [x] 1.7.7 — openWakeWord model download

- [x] **1.8** — Rename/clean `core/agents/New folder/` → meaningful name
  - [x] 1.8.1 — Decide purpose and rename accordingly
  - [x] 1.8.2 — Create placeholder `__init__.py` in all core subdirs (including `core/runtime/` skeleton)

---

## 🧠 Phase 2 — LLM Engine, Model Router, Decision Layer & Runtime
> **Goal:** Ollama access, **adaptive** routing via **Decision Layer** + **confidence** + **cost estimates** + **memory-informed priors**, **VRAM-safe** swaps, **Evaluate → Escalate|Finish**, and the **Observe → Decide → Think → Act → Evaluate** loop. **Extend** with **Error Intelligence** (2.23), **Self-Evaluation** (2.24), and **Persistent Runtime State** (2.25) so the stack behaves like a **real intelligent system**, not a one-shot script runner.

- [x] **2.1** — Create `models/llm/engine.py` — base Ollama interface
  - [x] 2.1.1 — `chat(messages, model)` — streaming + non-streaming
  - [x] 2.1.2 — `generate(prompt, model)` — single completion
  - [x] 2.1.3 — Handle connection errors + retry logic
  - [x] 2.1.4 — Support Arabic system prompts

- [x] **2.2** — Create `models/llm/router.py` — **dynamic** model selector (no fixed task→model map)
  - [x] 2.2.1 — Ingest **DecisionOutput** + **capability profiles** (from config) + modalities (vision bits) + **`cost_estimate`** (apply **cost penalty** vs **quality need**)
  - [x] 2.2.2 — **Score** candidate models by intent fit, complexity, **mode**, latency budget, reasoning ceiling, **prior confidence**
  - [x] 2.2.3 — Prefer **coder** profile when code/execution signals dominate; **vision** when pixels present
  - [x] 2.2.4 — Prefer **fast** profile (`gemma3`) when complexity low + mode `fast` + latency tight
  - [x] 2.2.5 — Prefer **deep** profile (`qwen3`) when complexity high or mode `deep` / escalation
  - [x] 2.2.6 — Default **balanced** / general profile (`qwen3:8b` per **Notes**) when no stronger signal wins — **or** whatever tag is configured as `balanced` in `config/models.yaml` (must exist in `ollama list`)
  - [x] 2.2.7 — VRAM guard — only one heavy Ollama model loaded at a time; serialize swaps; **mid-loop** switch when Decision/escalation demands it
  - [x] 2.2.8 — Expose **override** hooks (user / interface) without bypassing safety caps

- [x] **2.3** — Create `models/llm/prompts.py` — system prompt templates
  - [x] 2.3.1 — Jarvis Arabic personality prompt
  - [x] 2.3.2 — Jarvis English personality prompt
  - [x] 2.3.3 — Code-mode system prompt
  - [x] 2.3.4 — Planning-mode system prompt
  - [x] 2.3.5 — **Mode packs** — composable fragments for `fast` / `normal` / `deep` / `planning` / `research` (same model, different behavior)

- [x] **2.4** — Create `core/runtime/runtime_manager.py` — session lifecycle, turn orchestration, iteration/time limits
  - [x] 2.4.1 — Start/end “run” per user turn; hook interfaces → brain
  - [x] 2.4.2 — Enforce max loop iterations and timeouts
  - [x] 2.4.3 — Coordinate with model router for VRAM (before tool/vision steps)

- [x] **2.5** — Create `core/runtime/state/` — conversation + run state
  - [x] 2.5.1 — Track messages, pending tool calls, step index
  - [x] 2.5.2 — Serializable snapshots for debugging (optional)

- [x] **2.6** — Create `core/runtime/loop/` — **Observe → Decide → Think → Act → Evaluate → (Escalate \| Finish)** driver
  - [x] 2.6.1 — **Observe:** ingest user input + tool results + memory snippets + prior step metadata
  - [x] 2.6.2 — **Decide:** run Decision Layer; inject mode + budgets + **prior confidence** + **cost_estimate** into state
  - [x] 2.6.3 — **Think:** call LLM via **dynamic** router + mode-appropriate prompts
  - [x] 2.6.4 — **Act:** delegate to executor stub (no-op until Phase 5)
  - [x] 2.6.5 — **Evaluate:** compute **posterior confidence** + answer/tool **quality**; apply **threshold bands** (high/medium/low)
  - [x] 2.6.6 — **Branch:** **Finish** OR **Escalate** (re-enter **Decide** with updated observations—bounded)
  - [x] 2.6.7 — Failure: surface errors as observations; **fallback** safe response when max depth/iterations reached
  - [ ] 2.6.8 — **Context Buffer (Phase 3.9+):** **Observe** reads from **buffer snapshot** / merged staging — not from raw single-message input alone when buffer is active
  - [ ] 2.6.9 — **Merge** multiple buffered inputs (text + files + images + audio refs) into **one unified observation** for the turn
  - [ ] 2.6.10 — Pass merged bundle to **Decision Layer** as structured input (modalities + ordering + lightweight metadata); **no heavy models** in Observe

- [x] **2.7** — Create `core/runtime/executor/` — tool execution façade (thin until Phase 5)
  - [x] 2.7.1 — Interface for “execute tool(name, args)” with validation hooks
  - [x] 2.7.2 — Policy placeholder (permissions, sandbox flags)

- [x] **2.8** — Create `core/brain/orchestrator.py` — bridges runtime ↔ LLM ↔ memory (stub memory)
  - [x] 2.8.1 — Receive input from any interface via runtime manager
  - [x] 2.8.2 — Detect high-level intent (chat / tool / plan / search)
  - [x] 2.8.3 — Return unified response format (stream-friendly)
  - [ ] 2.8.4 — **Context Buffer:** accept **enqueue / commit** flows from interfaces; hand **buffer snapshot** into runtime **Observe** (see **3.9–3.13**)

- [x] **2.9** — Create `core/brain/dispatcher.py` — intent → handler (skills/tools wired in Phase 5)
  - [x] 2.9.1 — Map intent → tool or agent path
  - [x] 2.9.2 — Pass context and history
  - [x] 2.9.3 — Handle handler errors gracefully

- [x] **2.10** — Create `core/events/event_bus.py` — pub/sub event system
  - [x] 2.10.1 — Simple async event emitter
  - [x] 2.10.2 — Events: on_message, on_response, on_wake_word, on_error, on_tool_start, on_tool_end, **on_decision**, **on_evaluate**, **on_escalation**

- [x] **2.11** — Create `core/runtime/decision/` — **Decision Layer** (policy; no hardcoded model names)
  - [x] 2.11.1 — Define **DecisionOutput** schema: intent, complexity, mode, requires_tools, requires_planning, **`confidence` (prior)**, **`cost_estimate` { tokens, latency, gpu_load }**, `model_preference=auto`
  - [x] 2.11.2 — **Intent classification** — `chat | code | research | action` (+ multimodal hints)
  - [x] 2.11.3 — **Complexity estimation** — `low | medium | high` (signals: length, structure, ambiguity, retries)
  - [x] 2.11.4 — **Time / effort estimation** — expected steps/tokens/tools; feeds timeouts & planning triggers
  - [x] 2.11.5 — **Tool necessity** — `requires_tools` when external facts, FS, browser, APIs likely needed
  - [x] 2.11.6 — **Planning trigger** — `requires_planning` for multi-step / non-linear tasks
  - [x] 2.11.7 — **Prior confidence** — 0.0–1.0 estimate *before* main generation (ambiguity, missing info, contradiction signals)
  - [x] 2.11.8 — **Cost estimate** — pre-execution **token** budget + **latency** tier + **gpu_load** tier (inputs to router tradeoff)
  - [ ] 2.11.9 — **Context Buffer as input source** — `DecisionOutput` driven from **merged buffer summary** + modality flags (text length, attachment types); keep classification **lightweight** (rules / small classifier **optional** — **no** heavy LLM pass dedicated to buffer)
  - [ ] 2.11.10 — **Identity priors** — optional fields or sidecar from **User profile** (**3.14**) / **3.7** (e.g. expertise tier, goals, style) — bias **intent** / **complexity** / **mode** without a second LLM call; **feed** **System Prompt Builder** (**3.17**)

- [x] **2.12** — **Mode controller** — bind **Thinking Modes** to prompt packs + decode params (orthogonal to model ID)
  - [x] 2.12.1 — Map `fast | normal | deep | planning | research` → template + parameter set
  - [x] 2.12.2 — Allow **same model** to switch modes between turns or mid-escalation

- [x] **2.13** — **Escalation engine** — ties to **Evaluate** outcomes (adaptive; not scripted)
  - [x] 2.13.1 — Triggers: **low posterior** confidence, incomplete answer, tool failure, repeated failure, memory “similar failures”
  - [x] 2.13.2 — Actions: deeper mode, stronger model via router, enable planning, alternate tool strategy
  - [x] 2.13.3 — **max_escalation_depth** + **max_iterations** + **per-step timeouts**
  - [x] 2.13.4 — **Retry policy** — bounded retries with backoff; each retry re-enters **Decide** with new observations

- [x] **2.14** — **Capability profiles** — structured metadata per model (in `config/models.yaml` or sidecar)
  - [x] 2.14.1 — Fields: reasoning strength, Arabic quality, latency tier, code bias, vision required, VRAM estimate
  - [x] 2.14.2 — Router reads profiles; **weights/thresholds** configurable (no code fork for tuning)

- [x] **2.15** — Integrate **Decision Layer** ↔ **router** ↔ **loop** (end-to-end turn)
  - [x] 2.15.1 — Decision injects mode + flags before **Think**; router scores **auto** model selection
  - [x] 2.15.2 — **Mid-loop** model switch when escalation fires (respect VRAM guard)
  - [ ] 2.15.3 — **Context Buffer path** — end-to-end: interface → **enqueue** → **Observe** (merged snapshot) → **Decide** → **Think** (first heavy LLM) / **Act** (tools + heavy modality readers **only** after decision)

- [x] **2.16** — Limits & **fallback** policy
  - [x] 2.16.1 — Per-turn / per-tool / per-load **timeouts**
  - [x] 2.16.2 — **Safe fallback** response when caps hit (graceful degradation)

- [x] **2.17** — Test LLM + runtime + **decision** wiring
  - [x] 2.17.1 — Arabic chat with adaptive mode selection
  - [x] 2.17.2 — Code path: verify **scoring** favors coder profile when signals warrant (not name-only)
  - [x] 2.17.3 — Deep escalation: low-confidence → deeper mode or `qwen3` path
  - [x] 2.17.4 — Single-GPU constraint + **mid-loop** swap under escalation
  - [x] 2.17.5 — **DecisionOutput** contract tests (schema + bounds)

- [x] **2.18** — **Confidence system** — prior + posterior
  - [x] 2.18.1 — **Prior** in Decision Layer (`confidence` field)
  - [x] 2.18.2 — **Posterior** in **Evaluate** (self-critique / consistency / task rubrics / tool outcomes)
  - [x] 2.18.3 — **Threshold bands** (high/medium/low) as config; drive Finish vs Refine vs Escalate

- [x] **2.19** — **Cost estimation system** — pre-action budgets
  - [x] 2.19.1 — Populate **`cost_estimate.tokens`** from planned context + mode + tool rounds
  - [x] 2.19.2 — Map model choice + mode → **latency** / **gpu_load** tiers (scoring-based, not static)
  - [x] 2.19.3 — Router uses **cost × quality** tradeoff (cheap when safe, expensive when signals demand)

- [x] **2.20** — **Evaluate stage** — first-class module under `core/runtime/loop/` or `evaluate/`
  - [x] 2.20.1 — Inputs: candidate answer, tool traces, `DecisionOutput`, memory hints
  - [x] 2.20.2 — Outputs: **quality score**, **posterior confidence**, **stop/escalate** recommendation

- [x] **2.21** — **Memory-influenced decision** — integrate with Phase 3 when available
  - [x] 2.21.1 — Feed **user preferences** + **language** bias into Decision (e.g. Arabic quality weight)
  - [x] 2.21.2 — Track **repeated patterns** (e.g. code-heavy user) → adjust priors / escalation aggressiveness
  - [x] 2.21.3 — Log **failures/successes** for similar queries → bias tools/planning early
  - [x] 2.21.4 — Define stable **interfaces** so Phase 2 runs with stubs before full memory

- [x] **2.22** — **Integration test** — confidence + cost + evaluate + escalation
  - [x] 2.22.1 — Low prior → cheap route; high complexity → accepts higher cost_estimate
  - [x] 2.22.2 — Posterior low → escalation within **max_escalation_depth**
  - [x] 2.22.3 — Limits hit → **fallback** path

- [ ] **2.23** — **Error Intelligence System** — classify failures and drive **smart retry** (extends escalation; does not replace it)
  - [ ] 2.23.1 — **Error taxonomy** — `model_error | tool_error | timeout | invalid_input | unknown` (extensible; logged with structured fields)
  - [ ] 2.23.2 — **Tool error** — surface provider/HTTP/schema errors as observations; attach to **tool id** + args hash for analytics
  - [ ] 2.23.3 — **Model error** — parse Ollama/LLM failures (empty output, parse failure, refusal) → observation + class
  - [ ] 2.23.4 — **Timeout** — distinguish per-step vs global; feed **cost_estimate** and **retry budget**
  - [ ] 2.23.5 — **Invalid input** — validation before execute; optional **repair** pass (model or template) with bounded attempts
  - [ ] 2.23.6 — **Smart retry strategy** — policy matrix: retry **same model**, **switch model** (router), **switch mode** (mode controller), **decompose** (hand off to Phase 7 when available)
  - [ ] 2.23.7 — **Integration** — connect to **DecisionLayer** + **router** + **escalation**; emit events on `event_bus` for **Feedback** (Phase 8)

- [ ] **2.24** — **Self-Evaluation System** — extend **Evaluate** (quality + posterior) with **answer-level** checks
  - [ ] 2.24.1 — **Completeness check** — rubric: addresses all sub-questions; optional checklist from Decision / decomposition
  - [ ] 2.24.2 — **Correctness estimation** — consistency with tool traces + retrieved facts; flag **unsupported claims** when evidence missing
  - [ ] 2.24.3 — **Hallucination / grounding detection** — cite-or-abstain for factual queries; confidence penalty when evidence is thin
  - [ ] 2.24.4 — **Outputs** — merge into `Evaluate` result: `quality_score`, `posterior confidence`, **refusal/hedge** recommendation, **escalate** reason codes
  - [ ] 2.24.5 — **Integration** — feeds **escalation**, **Feedback** (Phase 8), and **memory** (store “high uncertainty” patterns)

- [ ] **2.25** — **Persistent Runtime State** — long-lived execution context (beyond single-turn state)
  - [ ] 2.25.1 — **Execution history** — append-only log of runs: `run_id`, steps, tool calls, decisions, evaluate scores, error classes (queryable)
  - [ ] 2.25.2 — **Resume interrupted tasks** — persist pending plans / graph nodes (with Phase 7); reconnect interfaces (CLI/Web) to same `run_id`
  - [ ] 2.25.3 — **Long-running task tracking** — `background` / `await_user` / `polling` states; heartbeats; cancellation
  - [ ] 2.25.4 — **Storage** — SQLite or existing DB layer; align with memory tables where appropriate; **no secrets** in logs
  - [ ] 2.25.5 — **Integration** — orchestrator + **event_bus** + Phase 8 **feedback** hooks; **Personality** (Phase 12) reads style prefs from memory, not from run state

- [ ] **2.26** — **Identity-aware LLM invocation** — models are **never** prompted as standalone assistants
  - [ ] 2.26.1 — Route **every** `chat` / `generate` (all models, all routes) through **System Prompt Builder** (**3.17**) + **model awareness** (**3.16**) — **no** ad-hoc system strings that omit Jarvis/user context
  - [ ] 2.26.2 — **Router** + **mode controller** (2.2, 2.12) apply **on top** of identity layer (quality/latency — **not** a separate “personality” per model)
  - [ ] 2.26.3 — **Regression tests** — swap model id; **Jarvis identity** + **user profile** + **shared state** remain stable in system prompt contract

---

## 💾 Phase 3 — Memory System (incl. Adaptive Memory)
> **Goal:** Jarvis remembers conversations and facts across sessions; **learned preferences** and **memory-informed decisions** connect to Decision + Router (see **System integration** above). **Identity & Profiles** (below) defines **who Jarvis is** and **who the user is** for **consistent** behavior across **all** models — distinct from raw fact recall (3.2–3.4) but stored/loaded via the same stack where appropriate.

- [ ] **3.1** — Create `core/memory/short_term.py` — in-session memory
  - [ ] 3.1.1 — Store conversation history as list of messages
  - [ ] 3.1.2 — Token-aware trimming (keep within context window)
  - [ ] 3.1.3 — Redis backend for persistence

- [ ] **3.2** — Create `core/memory/long_term.py` — persistent semantic memory
  - [ ] 3.2.1 — ChromaDB collection for semantic search
  - [ ] 3.2.2 — `remember(text, metadata)` — store a fact
  - [ ] 3.2.3 — `recall(query, n=5)` — semantic similarity search
  - [ ] 3.2.4 — Auto-save important facts from conversations

- [ ] **3.3** — Create `core/memory/database.py` — SQLite structured storage
  - [ ] 3.3.1 — conversations table (id, role, content, timestamp)
  - [ ] 3.3.2 — facts table (id, content, source, created_at)
  - [ ] 3.3.3 — tasks table (id, title, status, created_at)

- [ ] **3.4** — Create `core/memory/manager.py` — unified memory interface
  - [ ] 3.4.1 — `save_interaction(role, content)`
  - [ ] 3.4.2 — `get_context(n_messages)` — for LLM context
  - [ ] 3.4.3 — `search(query)` — search all memory types

- [ ] **3.5** — Integrate memory into orchestrator + runtime **Observe** step
  - [ ] 3.5.1 — Auto-inject relevant memories into LLM context
  - [ ] 3.5.2 — Auto-save each interaction

- [ ] **3.6** — Test memory system
  - [ ] 3.6.1 — Store and retrieve conversation
  - [ ] 3.6.2 — Semantic search test
  - [ ] 3.6.3 — Cross-session memory persistence test

- [ ] **3.7** — **User profiling (adaptive memory)** — structured preferences separate from raw chat
  - [ ] 3.7.1 — **Preferred language** — primary UI/response language; Arabic vs English bias for router prompts
  - [ ] 3.7.2 — **Preferred response style** — concise vs verbose, formal vs casual (enum + free-text notes)
  - [ ] 3.7.3 — **Common tasks / intents** — recurring patterns (code-heavy, research-heavy) → **prior** for Decision Layer
  - [ ] 3.7.4 — **Storage** — profile document keyed by user/session; versioned updates; GDPR-style delete path (optional)

- [ ] **3.8** — **Memory-driven decisions** — close the loop with Phase 2
  - [ ] 3.8.1 — **Influence model selection** — boost/penalize profiles per **task pattern** + language needs (interfaces with **router** scoring)
  - [ ] 3.8.2 — **Influence thinking mode** — bias toward `fast` vs `deep` / `planning` from history + explicit prefs
  - [ ] 3.8.3 — **Integration** — `memory.manager` exposes hooks consumed by **Decision** (2.11) and **orchestrator** Observe step; works with **Feedback** (Phase 8) updates

### 📥 Context Buffer System (temporary input staging)
> **Goal:** **Multimodal** staging before execution — accept **multiple** inputs per turn; **temporarily** hold text, files, images, and audio **references**; provide **lightweight** context for **Observe** and **Decision**; **no heavy models** in this layer (no Whisper, no LLaVA, no embeddings — those run **after** Decide / in **Act**). Distinct from **long-term memory** (3.1–3.4): buffer is **ephemeral session staging**, not semantic recall.

- [ ] **3.9** — Create `core/context/buffer.py` (or `core/context/` package) — **Context Buffer module**
  - [ ] 3.9.1 — **Temporary storage** for user inputs until **commit** / **execute** (per session or per `run_id`)
  - [ ] 3.9.2 — Allow **multiple** inputs to accumulate before the runtime run (queue, batch, or “send” semantics per interface)
  - [ ] 3.9.3 — Support **text** (including partial / draft), **files** (PDF, Office), **images**, **audio** (store paths, handles, or bounded blobs — **no** transcription or vision inference here)

- [ ] **3.10** — **Input registration**
  - [ ] 3.10.1 — Assign a **stable `input_id`** per item
  - [ ] 3.10.2 — Track **input type** (`text | file | image | audio | …`)
  - [ ] 3.10.3 — **Timestamp** each entry (ordering, TTL, and debugging)

- [ ] **3.11** — **Lightweight preprocessing** (preparation **only**)
  - [ ] 3.11.1 — **Basic parsing for text** — normalize whitespace, optional simple chunking; **no** LLM summarization in buffer
  - [ ] 3.11.2 — **File metadata** — size, extension, mime / magic-byte **detection**
  - [ ] 3.11.3 — **Extract cheap metadata only** (e.g. image dimensions, page count where available without heavy libs); **do not** run heavy models

- [ ] **3.12** — **Buffer lifecycle**
  - [ ] 3.12.1 — **Clear** after successful **execute** / turn completion (policy: also clear on explicit user “reset”)
  - [ ] 3.12.2 — **Persist for session** — in-memory with optional Redis/session backing; survives multiple messages until cleared
  - [ ] 3.12.3 — **Optional timeout cleanup** — evict stale items; configurable idle TTL

- [ ] **3.13** — **Integration** (mandatory wiring)
  - [ ] 3.13.1 — **Runtime loop** — **Observe** uses buffer per **2.6.8–2.6.10** (read snapshot, merge, pass forward)
  - [ ] 3.13.2 — **Decision Layer** — primary signals from **merged buffer** + **2.11.9** (intent / complexity / modality without heavy preprocessing)
  - [ ] 3.13.3 — **Tool system** — **Act** phase resolves buffer **refs** to paths / safe temp files for tool args (**5.16**); heavy readers (PDF text, STT, vision) run **only** when tools or **Think** require them — **not** inside buffer

### 🪪 Identity & Profiles System (who Jarvis is — who the user is)
> **Rules:** **No** model is a standalone product or “the real Jarvis” in isolation; **every** inference is **part of one system** with a **single** coherent identity. **System prompts are dynamic** (built from config + session + task + mode), **not** one static paragraph. **Safety:** never expose raw filesystem, secrets, or unrestricted host introspection — **summarized** / **allow-listed** context only (**3.19**).

- [ ] **3.14** — **User profile** (identity-aware; complements **3.7** adaptive fields)
  - [ ] 3.14.1 — **Create** `core/identity/user_profile.py` (or `core/identity/`) — load/save per **user id** / session
  - [ ] 3.14.2 — **Store:** **display name**, **language preferences**, **behavior style** (concise/verbose…), **technical level** (beginner…expert), **stated goals** (optional structured fields)
  - [ ] 3.14.3 — **Merge strategy** with **3.7** — avoid duplicate sources of truth; migrate or unify fields; profile drives **Decision** + **prompt builder**
  - [ ] 3.14.4 — **Load into runtime** — available to **Observe**, **Decision** (2.11), and **3.17** on each turn
  - [ ] 3.14.5 — **Dynamic updates** — CLI/Web/commands edit profile; **Feedback** (Phase 8) may suggest updates (bounded)

- [ ] **3.15** — **Jarvis profile (system identity)**
  - [ ] 3.15.1 — **Define** canonical identity: **name** = Jarvis; **role** = AI assistant **system** (not a single model); **architecture** = multi-model + tools + memory + reasoning loop
  - [ ] 3.15.2 — **Capabilities** — tools, memory, planning, multimodal (summarized list — not raw registry dumps in prompt)
  - [ ] 3.15.3 — **Default tone & behavior** — baseline before **Personality** (Phase 12) overlays
  - [ ] 3.15.4 — **Store in config** — e.g. `config/jarvis_identity.yaml` + Pydantic model in `settings/`; versioned; hot-reload optional

- [ ] **3.16** — **Model awareness layer** (what each model *must* know before token 1)
  - [ ] 3.16.1 — **Inject on every call:** **Jarvis identity** (3.15), **user profile** (3.14), **system context** (short: runtime phase, tool availability summary — not secrets)
  - [ ] 3.16.2 — **Required framing** — e.g. “You are a **component** of **Jarvis**”; “You are **not** a standalone product”; “You may **use tools** when selected”; “You **collaborate** with other models/handlers under the same orchestrator”
  - [ ] 3.16.3 — **Consistency** — same framing across **fast/deep/coder/vision** routes; only **task** and **mode** sections differ — **identity** block is stable

- [ ] **3.17** — **System Prompt Builder** (dynamic generator)
  - [ ] 3.17.1 — **Combine** — Jarvis identity (3.15) + user profile (3.14) + **task context** (buffer 3.9–3.13, memory snippets 3.5, **DecisionOutput** hints) + **mode** (`fast` / `deep` / `planning` — 2.12)
  - [ ] 3.17.2 — **Inject into every model call** — single pipeline used by **LLM engine** (2.1) per **2.26**
  - [ ] 3.17.3 — **Deterministic ordering** — identity → safety → user prefs → task → mode fragments; testable snapshots (redact secrets)

- [ ] **3.18** — **Shared context awareness** (cross-model continuity)
  - [ ] 3.18.1 — **Same conversation state** — rolling summary + message window + tool traces (aligned with **2.5**, **2.25**)
  - [ ] 3.18.2 — **Previous actions** — compact list of recent tool calls / outcomes so the next model **does not** contradict or forget without reason
  - [ ] 3.18.3 — **Handoff discipline** — when **router** switches models mid-run, **identity + user + state** carry forward unchanged (**3.16**)

- [ ] **3.19** — **File & system awareness (controlled)**
  - [ ] 3.19.1 — **Abstract project view** — allow-listed roots, depth limits, **summarized** tree or key paths (no recursive dump of home dir)
  - [ ] 3.19.2 — **Available tools** — names + one-line purpose from **registry** (5.2) — not full JSON spam unless mode requires
  - [ ] 3.19.3 — **Environment capabilities** — OS class, GPU tier summary (from config), **no** blind `/etc` or env leakage
  - [ ] 3.19.4 — **Explicit non-goals** — **do not** expose raw system blindly; redact secrets; user-approved scope only

- [ ] **3.20** — **Integration** (mandatory wiring)
  - [ ] 3.20.1 — **Decision Layer** — consume user expertise / goals as **priors** (extend **2.11** schema or sidecar); align with **memory-driven** (3.8)
  - [ ] 3.20.2 — **Runtime loop** — **Observe** merges **buffer** + **memory** + **identity** slices into one **prompt build request** for **3.17**
  - [ ] 3.20.3 — **Context Buffer** — staged attachments described in **task context** section of **3.17** (metadata-first; heavy extraction later)
  - [ ] 3.20.4 — **Memory system** — long-term facts (3.2) + profile (3.14) + **3.7** unified read path for prompt composition
  - [ ] 3.20.5 — **Engine** — implement **2.26**; document contract for **Phase 12** (Personality) as **overlay**, not replacement of **3.15**

---

## 💻 Phase 4 — CLI Interface
> **Goal:** Full-featured terminal chat with Rich formatting

- [ ] **4.1** — Create `interfaces/cli/interface.py` — main CLI class
  - [ ] 4.1.1 — Rich panel-based UI
  - [ ] 4.1.2 — Streaming response display (token by token)
  - [ ] 4.1.3 — Arabic text rendering support (RTL)
  - [ ] 4.1.4 — Keyboard shortcuts (Ctrl+C exit, Ctrl+L clear)

- [ ] **4.2** — Create `interfaces/cli/commands.py` — slash commands
  - [ ] 4.2.1 — `/clear` — clear conversation history
  - [ ] 4.2.2 — `/model [name]` — switch active model
  - [ ] 4.2.3 — `/memory` — show recent memories
  - [ ] 4.2.4 — `/tools` — list available tools (formerly `/skills`)
  - [ ] 4.2.5 — `/help` — show all commands

- [ ] **4.3** — Connect CLI to runtime manager / orchestrator
  - [ ] 4.3.1 — Pass user input to orchestrator
  - [ ] 4.3.2 — Display streaming response
  - [ ] 4.3.3 — Show typing indicator

- [ ] **4.4** — Create `app/cli.py` entry point

- [ ] **4.5** — Test CLI
  - [ ] 4.5.1 — Arabic conversation test
  - [ ] 4.5.2 — Streaming response test
  - [ ] 4.5.3 — Commands test

---

## 🛠️ Phase 5 — Tool System
> **Goal:** Real-world actions as **callable tools** — registry, **structured I/O**, **tool calling**, execution pipeline (code under `skills/`)

- [ ] **5.1** — Create `skills/base.py` — BaseTool (formerly BaseSkill) abstract class
  - [ ] 5.1.1 — `name: str` property
  - [ ] 5.1.2 — `description: str` property (for LLM tool list)
  - [ ] 5.1.3 — **Input/output schema** (JSON Schema or Pydantic model) per tool
  - [ ] 5.1.4 — `execute(params: dict)` — validated structured input → structured result
  - [ ] 5.1.5 — `is_available()` — check prerequisites

- [ ] **5.2** — Create `skills/registry.py` — tool registry + discovery
  - [ ] 5.2.1 — Scan `skills/` for BaseTool subclasses
  - [ ] 5.2.2 — Register all available tools with schemas
  - [ ] 5.2.3 — Export tool list + schemas to LLM (Ollama tools / JSON)

- [ ] **5.3** — **Tool calling pipeline** — LLM selects tool + arguments
  - [ ] 5.3.1 — Map registry to Ollama/OpenAI-compatible tool definitions
  - [ ] 5.3.2 — Parse model tool calls from responses (streaming-safe)
  - [ ] 5.3.3 — Validate args → execute → feed **observation** back into runtime loop

- [ ] **5.4** — Wire `core/runtime/executor/` to registry (validate, timeout, sandbox)
  - [ ] 5.4.1 — Unified `execute_tool(name, args)` with error wrapping
  - [ ] 5.4.2 — Log tool latency and outcomes (for Phase 11)

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

- [ ] **5.15** — **Parallel execution system** — throughput without breaking **VRAM** / **sandbox** rules
  - [ ] 5.15.1 — **Concurrent tool execution** — when **no** shared mutable resource or ordering constraint; **merge** results deterministically (define ordering for UI)
  - [ ] 5.15.2 — **Async runtime tasks** — `asyncio` integration in executor; **backpressure** + cancellation; propagate **Error Intelligence** (2.23) per task
  - [ ] 5.15.3 — **Background jobs** — long I/O (browser, downloads) off hot path; status channel to **Persistent Runtime State** (2.25) + event bus
  - [ ] 5.15.4 — **Integration** — **Task Decomposition** (Phase 7) schedules parallel vs serial; **router** still enforces single heavy model on GPU when applicable

- [ ] **5.16** — **Context Buffer ↔ executor / tools**
  - [ ] 5.16.1 — Resolve **buffer references** to concrete, validated paths or sandboxed temp files for `execute_tool(name, args)`
  - [ ] 5.16.2 — **Enforcement** — no tool execution during **staging**; heavy pipelines (readers, STT, vision) run **only** in **Act** after **Decision** — consistent with **3.11–3.13**

---

## 🤖 Phase 6 — Agents (Basic → Advanced)
> **Goal:** Multi-step autonomy **after** tools exist — basic planner/thinker/ReAct early; **advanced** research/screen **later in this phase**. **Structured decomposition, dependency graphs, and selective retry** belong to **Phase 7** (engine-level); this phase delivers **behaviors** and agents that **call** Phase 7 when needed.

### Basic (core autonomy)
- [ ] **6.1** — Create `core/agents/planner/planner.py` — step decomposition + sequencing
  - [ ] 6.1.1 — Break complex request into ordered steps
  - [ ] 6.1.2 — Assign each step to a **tool** or model role
  - [ ] 6.1.3 — Execute steps sequentially via runtime
  - [ ] 6.1.4 — Pass output of step N as input to step N+1
  - [ ] 6.1.5 — Report progress to user

- [ ] **6.2** — Create `core/agents/thinker/thinker.py` — deeper reasoning
  - [ ] 6.2.1 — Extended Chain-of-Thought reasoning
  - [ ] 6.2.2 — Prefer **`qwen3:8b`** for heavy thinking; default general chat uses **`qwen3:8b`** (or **`gemma3:4b`** when latency/mode `fast` — per router); **do not** assume **`qwen2.5:7b`** unless you add it to Ollama and config
  - [ ] 6.2.3 — Self-verification of answers
  - [ ] 6.2.4 — Confidence scoring

- [ ] **6.3** — ReAct loop integration (Reason + Act) with runtime
  - [ ] 6.3.1 — Observe → Think → Act → Observe with **tool calls**
  - [ ] 6.3.2 — Max iterations guard (ties to runtime limits)
  - [ ] 6.3.3 — Optional: show reasoning steps to user (CLI/Web)

### Advanced
- [ ] **6.4** — Create `core/agents/researcher.py` — deep research agent
  - [ ] 6.4.1 — Multi-query web search
  - [ ] 6.4.2 — Scrape and summarize multiple sources
  - [ ] 6.4.3 — Cross-reference and fact-check
  - [ ] 6.4.4 — Generate structured report

- [ ] **6.5** — `skills/screen/screen_agent.py` — visual computer control
  - [ ] 6.5.1 — Take screenshot
  - [ ] 6.5.2 — Describe screen via vision (`llava`)
  - [ ] 6.5.3 — Move mouse and click based on vision
  - [ ] 6.5.4 — Type text
  - [ ] 6.5.5 — Full GUI automation loop (guarded)

- [ ] **6.6** — Test agents
  - [ ] 6.6.1 — Multi-step task test (research + summarize)
  - [ ] 6.6.2 — ReAct + tool calling test
  - [ ] 6.6.3 — Screen agent test (optional hardware)

---

## 🧩 Phase 7 — Task Decomposition Engine
> **Goal:** Turn a goal into a **structured plan** — **execution graph**, **dependencies**, **selective retry** of failed steps only; composes with **Parallel execution** (5.15) and **Error Intelligence** (2.23)

- [ ] **7.1** — **Decomposition API** — input: user goal + `DecisionOutput` + memory context; output: **DAG** or layered graph of steps
  - [ ] 7.1.1 — **Subtask schema** — id, type (`tool|llm|branch|merge|human`), inputs/outputs, **depends_on**, **retry_group**
  - [ ] 7.1.2 — **Break tasks into subtasks** — LLM- or template-assisted; cap **max_nodes** + **max_depth** from config
  - [ ] 7.1.3 — **Human-in-the-loop** nodes — optional approval gates for destructive tools

- [ ] **7.2** — **Execution graph runtime** — deterministic scheduler
  - [ ] 7.2.1 — **Topological order** with **parallel frontier** (where 5.15 applies)
  - [ ] 7.2.2 — **Handle dependencies** — pass outputs as typed artifacts (files, JSON, text) between nodes
  - [ ] 7.2.3 — **Idempotency** — stable keys for re-run after resume (2.25)

- [ ] **7.3** — **Retry only failed steps**
  - [ ] 7.3.1 — Mark failed node with **error class**; skip successful siblings when safe
  - [ ] 7.3.2 — **Partial replan** — optional subgraph regeneration on repeated failure (bounded)

- [ ] **7.4** — **Integration with agents + runtime**
  - [ ] 7.4.1 — Planner (6.1) can **delegate** to engine instead of ad-hoc lists
  - [ ] 7.4.2 — **Dispatcher** routes “complex plan” intents here; results feed **Observe** as structured observations

- [ ] **7.5** — **Observability** — export graph to logs/UI (Mermaid or JSON) for debugging

- [ ] **7.6** — **Tests**
  - [ ] 7.6.1 — Diamond dependency graph (parallel then join)
  - [ ] 7.6.2 — Failure mid-graph → retry one branch only
  - [ ] 7.6.3 — Resume after disconnect (2.25) with same `run_id`

- [ ] **7.7** — **Feedback hooks** — on node success/failure emit signals for Phase 8 (model/tool attribution)

- [ ] **7.8** — **Cost / budget awareness** — inherit **cost_estimate** (2.19); prune or shorten plan when over budget

---

## 📈 Phase 8 — Feedback & Learning System
> **Goal:** Learn from **implicit** and **explicit** signals; persist **attributed** outcomes for **memory** and **decision** priors — not a separate silo

- [ ] **8.1** — **Implicit feedback detection**
  - [ ] 8.1.1 — **User continues** — new message within τ without correction → weak positive engagement signal
  - [ ] 8.1.2 — **User repeats question** — rephrase or same intent → negative / confusion signal; boost clarification behavior
  - [ ] 8.1.3 — **User ignores response** — no follow-up within session window → weak negative (interface-dependent)

- [ ] **8.2** — **Explicit feedback** (optional UI later) — 👍/👎, “this was wrong,” correction messages

- [ ] **8.3** — **Success / failure scoring** — map events + **Evaluate** (2.20, 2.24) + **error class** (2.23) to scalar or label per **turn** and per **node** (Phase 7)

- [ ] **8.4** — **Store feedback linked to:**
  - [ ] 8.4.1 — **Decisions** — snapshot `DecisionOutput` id / hash
  - [ ] 8.4.2 — **Models** — resolved model id + mode pack
  - [ ] 8.4.3 — **Tools** — tool name + version + args fingerprint (no secrets)

- [ ] **8.5** — **Learning surfaces (incremental, safe)**
  - [ ] 8.5.1 — **Router weights** — nudge scores from rolling aggregates (with floors/ceilings; no unbounded drift)
  - [ ] 8.5.2 — **Escalation aggressiveness** — tune thresholds from repeated low posteriors
  - [ ] 8.5.3 — **Memory writes** — “what worked” summaries into long-term (Phase 3)

- [ ] **8.6** — **Privacy & controls** — per-user opt-out; retention TTL; export/delete

- [ ] **8.7** — **Integration tests** — synthetic sessions; verify attribution chain **decision → model → tool → outcome**

- [ ] **8.8** — **Anti-feedback hacking** — detect spam toggles; rate-limit weight updates

- [ ] **8.9** — **Dashboard hooks (optional)** — expose aggregates to Phase 11 monitoring

---

## 🌐 Phase 9 — Web + Voice + Vision
> **Goal:** Multimodal surfaces on top of the same **runtime**, **tools**, **memory**, and **feedback** loops

### Web UI — real-time web chat
- [ ] **9.1** — Create `interfaces/web/app.py` — FastAPI application
  - [ ] 9.1.1 — Static files serving
  - [ ] 9.1.2 — Template rendering (Jinja2)
  - [ ] 9.1.3 — CORS configuration

- [ ] **9.2** — Create `interfaces/web/websocket.py` — WebSocket handler
  - [ ] 9.2.1 — Accept connection
  - [ ] 9.2.2 — Receive message → pass to **runtime** / orchestrator
  - [ ] 9.2.3 — Stream response tokens back to client
  - [ ] 9.2.4 — Handle disconnection

- [ ] **9.3** — Create `interfaces/web/templates/index.html` — chat UI
  - [ ] 9.3.1 — Clean modern chat interface
  - [ ] 9.3.2 — Arabic RTL support
  - [ ] 9.3.3 — Streaming message display
  - [ ] 9.3.4 — Code blocks with syntax highlighting
  - [ ] 9.3.5 — Dark/Light theme toggle

- [ ] **9.4** — Create `interfaces/web/static/` — CSS + JS
  - [ ] 9.4.1 — `style.css` — chat UI styling
  - [ ] 9.4.2 — `chat.js` — WebSocket client + message handling
  - [ ] 9.4.3 — `markdown.js` — render markdown responses

- [ ] **9.5** — Create `interfaces/web/routes/` — REST API routes
  - [ ] 9.5.1 — `GET /` — serve chat page
  - [ ] 9.5.2 — `GET /api/models` — list available models
  - [ ] 9.5.3 — `GET /api/memory` — get conversation history
  - [ ] 9.5.4 — `DELETE /api/memory` — clear conversation

- [ ] **9.6** — Create `app/server.py` entry point

- [ ] **9.7** — Test Web UI
  - [ ] 9.7.1 — WebSocket connection test
  - [ ] 9.7.2 — Streaming response test
  - [ ] 9.7.3 — Arabic rendering test

- [ ] **9.8** — Add file upload support
  - [ ] 9.8.1 — Upload endpoint for images
  - [ ] 9.8.2 — Upload endpoint for documents
  - [ ] 9.8.3 — Pass files to vision/reader **tools**

### Voice pipeline — speak and listen (Arabic + English)
- [ ] **9.9** — Create `models/speech/stt.py` — Speech-to-Text (Whisper)
  - [ ] 9.9.1 — Load Whisper medium model
  - [ ] 9.9.2 — `record_audio(duration)` — capture from microphone
  - [ ] 9.9.3 — `transcribe(audio)` — convert speech to text
  - [ ] 9.9.4 — Auto-detect language (Arabic/English)
  - [ ] 9.9.5 — Handle background noise

- [ ] **9.10** — Create `models/speech/tts.py` — Text-to-Speech (Piper)
  - [ ] 9.10.1 — Load Piper Arabic voice model
  - [ ] 9.10.2 — Load Piper English voice model
  - [ ] 9.10.3 — `synthesize(text, lang)` → audio bytes
  - [ ] 9.10.4 — `play(audio)` — play audio output
  - [ ] 9.10.5 — Language auto-detect → select voice

- [ ] **9.11** — Create `interfaces/voice/wake_word.py` — Wake Word listener
  - [ ] 9.11.1 — Load openWakeWord model
  - [ ] 9.11.2 — Continuous microphone monitoring
  - [ ] 9.11.3 — Detect "Hey Jarvis" trigger
  - [ ] 9.11.4 — Fire event on wake word detection
  - [ ] 9.11.5 — Visual + audio confirmation feedback

- [ ] **9.12** — Create `interfaces/voice/voice_interface.py` — full pipeline
  - [ ] 9.12.1 — Wait for wake word
  - [ ] 9.12.2 — Record user speech (with silence detection)
  - [ ] 9.12.3 — Transcribe via Whisper
  - [ ] 9.12.4 — Send to **runtime** / orchestrator
  - [ ] 9.12.5 — Synthesize response via Piper
  - [ ] 9.12.6 — Play audio response
  - [ ] 9.12.7 — Return to listening state

- [ ] **9.13** — Silence detection for auto-stop recording
  - [ ] 9.13.1 — Detect end of speech (VAD)
  - [ ] 9.13.2 — Auto-stop after N seconds of silence

- [ ] **9.14** — Integrate voice with other interfaces
  - [ ] 9.14.1 — Voice input → Web UI (show transcription)
  - [ ] 9.14.2 — Voice input → CLI (show transcription)

- [ ] **9.15** — Test voice pipeline
  - [ ] 9.15.1 — Wake word detection test
  - [ ] 9.15.2 — Arabic STT accuracy test
  - [ ] 9.15.3 — TTS output quality test
  - [ ] 9.15.4 — Full pipeline end-to-end test

- [ ] **9.16** — Noise cancellation
  - [ ] 9.16.1 — Apply noise reduction filter
  - [ ] 9.16.2 — Gain normalization

- [ ] **9.17** — Voice settings in config
  - [ ] 9.17.1 — Microphone device selection
  - [ ] 9.17.2 — TTS speed and pitch controls

### Vision & image generation
- [ ] **9.18** — Create `models/vision/engine.py` — image understanding
  - [ ] 9.18.1 — Load LLaVA via Ollama
  - [ ] 9.18.2 — `describe(image_path, question)` → text description
  - [ ] 9.18.3 — Encode image to base64 for Ollama
  - [ ] 9.18.4 — Arabic response support
  - [ ] 9.18.5 — OCR capability (read text in images)

- [ ] **9.19** — Create `models/diffusion/generator.py` — image generation
  - [ ] 9.19.1 — Load Stable Diffusion 1.5 with float16
  - [ ] 9.19.2 — `generate(prompt, width, height, steps)` → PIL Image
  - [ ] 9.19.3 — VRAM management (unload when not in use)
  - [ ] 9.19.4 — Save generated images to disk
  - [ ] 9.19.5 — Negative prompt support

- [ ] **9.20** — Arabic prompt translation for image generation
  - [ ] 9.20.1 — Detect Arabic prompt
  - [ ] 9.20.2 — Translate to English via LLM before passing to SD
  - [ ] 9.20.3 — Return image + translated prompt

- [ ] **9.21** — Integrate vision into orchestrator + router
  - [ ] 9.21.1 — Detect image attached to message
  - [ ] 9.21.2 — Auto-route to vision engine (`llava`)
  - [ ] 9.21.3 — Combine vision output with LLM response

- [ ] **9.22** — Screen capture for vision
  - [ ] 9.22.1 — Screenshot capture tool
  - [ ] 9.22.2 — "What's on my screen?" → vision engine

- [ ] **9.23** — Test vision pipeline
  - [ ] 9.23.1 — Image description test (Arabic + English)
  - [ ] 9.23.2 — Image generation test
  - [ ] 9.23.3 — OCR test on Arabic text

---

## 🔌 Phase 10 — Integrations (Telegram + GUI)
> **Goal:** Secondary surfaces sharing the same **runtime** and **tools**

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
  - [ ] 10.6.1 — Arabic conversation test
  - [ ] 10.6.2 — Image upload test
  - [ ] 10.6.3 — Voice message test

### GUI Desktop
- [ ] **10.7** — Choose framework: PyQt6 (recommended) or Tkinter
  - [ ] 10.7.1 — Install PyQt6
  - [ ] 10.7.2 — Create main window class

- [ ] **10.8** — Create `interfaces/gui/main_window.py`
  - [ ] 10.8.1 — Chat message area (scrollable)
  - [ ] 10.8.2 — Input text box
  - [ ] 10.8.3 — Send button
  - [ ] 10.8.4 — Model selector dropdown
  - [ ] 10.8.5 — Microphone button (voice input)

- [ ] **10.9** — Create `interfaces/gui/settings_dialog.py`
  - [ ] 10.9.1 — Model selection
  - [ ] 10.9.2 — Language preference
  - [ ] 10.9.3 — Voice settings

- [ ] **10.10** — Arabic RTL text rendering in GUI
  - [ ] 10.10.1 — Set Qt layout direction for Arabic
  - [ ] 10.10.2 — RTL text alignment in chat bubbles

- [ ] **10.11** — System tray integration
  - [ ] 10.11.1 — Minimize to system tray
  - [ ] 10.11.2 — Wake word activates window
  - [ ] 10.11.3 — Tray menu: Open, Settings, Quit

---

## ✅ Phase 11 — Optimization, QA & Production Hardening
> **Goal:** Production-ready, fast, stable, and documented — **performance**, **reliability**, **security**, **observability**

- [ ] **11.1** — Create `tests/` test suite
  - [ ] 11.1.1 — `tests/test_llm.py` — LLM engine tests
  - [ ] 11.1.2 — `tests/test_memory.py` — memory system tests
  - [ ] 11.1.3 — `tests/test_tools.py` — tool registry + representative tools
  - [ ] 11.1.4 — `tests/test_voice.py` — STT/TTS pipeline test
  - [ ] 11.1.5 — `tests/test_vision.py` — vision engine test
  - [ ] 11.1.6 — `tests/test_runtime.py` — loop + executor boundaries

- [ ] **11.2** — Performance optimization
  - [ ] 11.2.1 — Profile slow operations
  - [ ] 11.2.2 — Model preloading strategy (still VRAM-safe)
  - [ ] 11.2.3 — Response caching for repeated queries
  - [ ] 11.2.4 — Async all I/O operations

- [ ] **11.3** — Error handling and resilience (aligns with **Error Intelligence** 2.23; avoid duplicate policies)
  - [ ] 11.3.1 — Graceful Ollama connection failure
  - [ ] 11.3.2 — Model loading failure fallback (`gemma3` / `qwen3` policy)
  - [ ] 11.3.3 — Tool execution error recovery
  - [ ] 11.3.4 — Retry logic with exponential backoff
  - [ ] 11.3.5 — End-to-end tests for **error class** → **retry / switch model / switch mode** matrix

- [ ] **11.4** — Logging and monitoring
  - [ ] 11.4.1 — Structured logging (Loguru)
  - [ ] 11.4.2 — Log all model calls with latency
  - [ ] 11.4.3 — Log all tool executions
  - [ ] 11.4.4 — Log errors with full stack trace

- [ ] **11.5** — Windows compatibility
  - [ ] 11.5.1 — Test all features on Windows 11 + PowerShell
  - [ ] 11.5.2 — Path handling (Windows vs Linux)
  - [ ] 11.5.3 — Audio device detection on Windows
  - [ ] 11.5.4 — Create `scripts/install.ps1` for Windows

- [ ] **11.6** — Security review
  - [ ] 11.6.1 — Sandbox code execution (no system access)
  - [ ] 11.6.2 — Validate all user inputs and **tool args**
  - [ ] 11.6.3 — Secure API key storage

- [ ] **11.7** — Update documentation
  - [ ] 11.7.1 — Update README.md with final instructions
  - [ ] 11.7.2 — Add docstrings to all modules
  - [ ] 11.7.3 — Update TASKS.md progress table (all **12** phases)

- [ ] **11.8** — Final integration test
  - [ ] 11.8.1 — Full conversation in Arabic
  - [ ] 11.8.2 — Voice → response → TTS full cycle
  - [ ] 11.8.3 — Multi-step agent task
  - [ ] 11.8.4 — Telegram + Web simultaneously

---

## 🎭 Phase 12 — Personality Layer (tone, style, adaptation)
> **Goal:** Consistent **Jarvis** voice across interfaces while **adapting** to user prefs — composes with **prompt packs** (2.3, 2.12) and **Adaptive Memory** (3.7–3.8); **does not** bypass safety, caps, or tool policy

- [ ] **12.1** — **Tone control** — formal/casual/warm; locale-aware (Arabic diglossy considerations optional); user override via config + memory profile

- [ ] **12.2** — **Response style** — length presets; bullet vs prose; “teacher mode” vs “executive summary”; tie to **Self-Evaluation** (2.24) targets (e.g. completeness)

- [ ] **12.3** — **Adaptive personality** — drift **slowly** from **Feedback** (Phase 8) + explicit prefs; bounded deltas; audit log of changes

- [ ] **12.4** — **Integration** — inject **Personality** fragments into **mode packs** + system prompts (via **3.17**); CLI/Web optional toggles; ensure **router** still picks model by capability; **do not** override **Jarvis core identity** (**3.15**) — adaptation is **bounded** on top of **Identity & Profiles**

- [ ] **12.5** — **Tests** — A/B prompt fixtures; regression that safety refusals still occur when required

---

## 📌 Notes

### Model roles (match `ollama list`)
**Capability profiles** in `config/models.yaml` must use **exact** Ollama tag names for models you have pulled — the router has no use for names that are not installed.

**Current inventory (example — verify with `ollama list` on your machine):**
```
gemma3:4b          — Fast / lightweight; tight latency or low complexity
qwen3:8b           — General / balanced / deep reasoning (default “main” brain when no separate base model)
qwen2.5-coder:7b   — Code + execution tasks
llava:7b           — Vision
```

**Optional later pulls** (only if you add them to Ollama **and** config): e.g. `qwen2.5:7b` as a lighter general alternative to `qwen3:8b` — **not** required for the roadmap.

### VRAM Budget (6GB RTX 3050)
```
One heavy Ollama model at a time + unload before SD/vision swap
qwen3:8b        → ~5.0 GB
qwen2.5-coder:7b → ~4.7 GB
llava:7b        → ~4.5 GB
gemma3:4b       → ~3.0 GB
SD 1.5          → ~4.0 GB (float16)  — optional; unload Ollama first
```

### Priority Order for Development
1. Phases 1–3 (Foundation → LLM + **Runtime** → Memory + **adaptive** hooks)
2. Phase 4 CLI (fast feedback)
3. Phase 5 **Tool System** + **parallel execution** (enables real autonomy)
4. Phase 6 **Agents** (behaviors on top of tools)
5. Phase 7 **Task Decomposition Engine** (graphs, dependencies, selective retry)
6. Phase 8 **Feedback & Learning** (close the loop with memory + decision)
7. Phase 9 **Web + Voice + Vision** (multimodal surfaces)
8. Phase 10 Integrations
9. Phase 11 **Optimization & QA**
10. Phase 12 **Personality** (polish and adaptation last — builds on stable prompts + memory)

---

*Last updated: 2026 — Version 0.2.0-alpha (intelligence roadmap)*
