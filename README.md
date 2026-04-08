# Jarvis

**Personal AI assistant** that runs on your machine: **Telegram** (always started) and an optional **local web UI**. It uses **SQLite** for chat memory, optional **Firebase** sync, and a wide **tool** set (shell, files, browser, Google APIs, image/video generation, desktop control, and more).

LLM backends: **local Ollama / vLLM** (OpenAI-compatible `chat/completions` at `LOCAL_LLM_BASE_URL`) and optional cloud APIs (**Google Gemini**, **Groq**). There is **no** OpenAI SDK or OpenAI-hosted API in this codebase.

> **Release status:** This is a **personal / private codebase**, not a published product. There are **no semver releases** (no v1, v2, etc.). The `version` field in `package.json` is for local convenience only.

---

## Related documentation

| Location | Contents |
|----------|----------|
| **[`src/README.txt`](./src/README.txt)** | High-level layout of `src/` (folders and bootstrap). |
| **[`src/ui/README.txt`](./src/ui/README.txt)** | Static web UI: assets, build copy to `dist/ui`, HTTP entry. |
| **[`user/README.txt`](./user/README.txt)** | Runtime data under `user/` (database, uploads). |
| **`run/README.txt`** | Windows launch scripts, PM2 vs dev conflict. |

---

## Table of contents

1. [What it does](#what-it-does)
2. [Architecture overview](#architecture-overview)
3. [Repository layout](#repository-layout)
4. [Requirements](#requirements)
5. [Quick start](#quick-start)
6. [Configuration & environment](#configuration--environment)
7. [`paths.json`](#pathsjson)
8. [Shared tooling root (`NODE_PATH` / npm prefix)](#shared-tooling-root-node_path--npm-prefix)
9. [TypeScript & build](#typescript--build)
10. [How to run](#how-to-run)
11. [Telegram commands](#telegram-commands)
12. [Web UI](#web-ui)
13. [Agent pipeline](#agent-pipeline)
14. [Intent classification](#intent-classification)
15. [LLM routing](#llm-routing)
16. [Structured execution](#structured-execution)
17. [Safety layer](#safety-layer)
18. [Agent modes](#agent-modes)
19. [Memory: SQLite & migration](#memory-sqlite--migration)
20. [Google OAuth](#google-oauth)
21. [Tools reference](#tools-reference)
22. [Security](#security)
23. [Docker, PM2, deploy](#docker-pm2-deploy)
24. [Adding a new tool](#adding-a-new-tool)
25. [Troubleshooting](#troubleshooting)
26. [Tech stack](#tech-stack)

---

## What it does

- Listens on **Telegram** (text; **voice** is transcribed with **Groq Whisper** when `GROQ_API_KEY` is set).
- Loads **recent conversation context** from SQLite.
- Classifies user **intent** (type, complexity, tool needs) via hybrid heuristic + local LLM.
- Routes to the best **LLM provider & model** based on intent, engine mode, and availability.
- For **complex tasks**: generates a structured plan, then executes step-by-step with verification and self-correction.
- For **simple tasks**: lightweight single-pass LLM loop.
- Every tool call passes through a **safety layer** — risk classification, parameter validation, rate limiting, and user confirmation for dangerous actions.
- Optional **HTTP + WebSocket** server for the browser UI (settings, uploads, Google connect, chat).

**Important:** A normal start **always** runs the **Telegram** bot. The flag **`--web`** means **Telegram + web together**, not web instead of Telegram.

---

## Architecture overview

```
User Input (Telegram / Web)
    │
    ▼
① Intent Detection ─────────── engine/intent.ts
    │                           SINGLE SOURCE OF TRUTH for task type
    ▼
② Model Routing ────────────── engine/manager.ts + task-models.ts
    │                           Unified: both Telegram & Web use resolveRoute()
    ▼
③ Memory Retrieval ─────────── memory/store.ts + memory/retrieval.ts
    │
    ▼
④ Planning Decision ────────── planner.ts (driven by intent only)
    │
    ├─── Complex (shouldPlan = true):
    │    ④a Structured plan generation (typed steps + expected results)
    │    ④b executor.ts — step-by-step execution:
    │        → Build step context → LLM → Safety gate → Tool → Verify → Retry
    │    ④c Synthesize final response from all step results
    │
    └─── Simple (shouldPlan = false):
         ⑤ Context management (context.ts)
         ⑥ Lightweight LLM loop (iterate until text response)
    │
    ▼
⑦ Reflection ───────────────── reflection.ts (post-execution quality check)
    │
    ▼
⑧ Degraded Fallback ────────── degrade.ts (last resort on local LLM failure)
```

**Authority hierarchy:**

| Module | Decides |
|--------|---------|
| `intent.ts` | **WHAT** the task is (type, complexity, tools) |
| `manager.ts` | **WHERE** to run it (provider, model) |
| `planner.ts` | **HOW** to structure execution (plan steps) |
| `executor.ts` | Executes steps with verification and self-correction |
| `safety.ts` | **IF** a tool is allowed to run (risk, validation, confirmation) |
| `loop.ts` | Orchestrates the sequence, owns the branching decision |

---

## Repository layout

```
jarvis/
├── paths.json              # Central path config (dirs, DB, google, firebase, tooling)
├── package.json
├── .env                    # Your secrets (not committed)
├── .env.example
├── user/                   # Runtime data: DB, uploads (see user/README.txt)
│   ├── data/               # Default SQLite: memory.db (via paths.json)
│   └── uploads/
├── src/
│   ├── index.ts            # Entry: dirs, DB, tools, Telegram, optional web
│   ├── node-env.d.ts       # Pulls in Node typings for the TS project
│   ├── config/             # config.ts (env), project-paths.ts, tool-process-env.ts
│   ├── agent/
│   │   ├── loop.ts         # Top-level orchestrator — branches simple vs structured
│   │   ├── planner.ts      # Structured plan generation (typed steps + expected results)
│   │   ├── executor.ts     # Step-by-step execution engine with verify + retry
│   │   ├── safety.ts       # Risk classification, validation, rate limiting, confirmation
│   │   ├── reflection.ts   # Post-execution quality evaluation
│   │   ├── context.ts      # LLM context window management
│   │   ├── proactive.ts    # Scheduling/calendar detection
│   │   ├── degrade.ts      # Degraded fallback for local LLM failures
│   │   ├── types.ts        # All agent/execution types
│   │   └── engine/
│   │       ├── intent.ts       # Hybrid intent classification (SINGLE SOURCE OF TRUTH)
│   │       ├── manager.ts      # Unified LLM routing (provider + model selection)
│   │       └── task-models.ts  # Model registry + intent→model mapping
│   ├── llm/                # Groq, Gemini, local provider, routing, retry helpers
│   ├── memory/             # SQLite store, retrieval, profile, learning
│   ├── integrations/       # google/auth, voice/transcribe
│   ├── security/           # Telegram allow-list
│   ├── tools/              # One module per tool + registry + pipeline
│   ├── gateways/           # telegram.ts; http/server.ts (Express + WebSocket)
│   ├── ui/                 # Static web UI → copied to dist/ui on build
│   │   ├── assets/         # Jarvis.png (logo), Jarvis.ico (favicon)
│   │   ├── index.html, styles/, scripts/
│   └── tokens/             # OAuth / Firebase JSON (gitignored; paths in paths.json)
├── dist/                   # Produced by `npm run build` (JS + dist/ui)
└── run/                    # Optional Windows .bat helpers
```

---

## Requirements

- **Node.js 20+** (see `engines` in `package.json`).
- **Telegram** bot token (**required** at startup — `TELEGRAM_BOT_TOKEN`).
- **`GROQ_API_KEY`**: **not** required to boot, but needed for **voice messages** (Whisper) and for using **Groq** as an API LLM. Without it, use text-only on Telegram and/or rely on Gemini/local.
- **`GEMINI_API_KEY`**: optional; when set (and not a placeholder), Gemini participates in API routing.
- **Local LLM**: configure `LOCAL_LLM_BASE_URL` (e.g. `http://127.0.0.1:11434/v1` for Ollama) for local/engine modes and for the **web UI** (web chat is **local-first**; see below).
- **Windows:** desktop, notifications, and some automation tools are built for Windows; on Linux/Docker behavior may differ or be limited.

---

## Quick start

### 1) Install

```bash
cd /path/to/jarvis
npm install
```

Run commands from the directory that contains **`package.json`** and **`paths.json`**.

### 2) Environment

```bash
copy .env.example .env   # Windows
# cp .env.example .env   # Unix
```

Set at least **`TELEGRAM_BOT_TOKEN`**. Add **`GROQ_API_KEY`** if you want voice and/or Groq. See **`.env.example`** for the full list.

### 3) Secrets (recommended paths)

Default JSON locations are driven by **`paths.json`** (typically under **`src/tokens/`**):

| File | Role |
|------|------|
| `google-oauth.json` | Google OAuth client (`installed` or `web`) |
| `google-token.json` | Filled after OAuth |
| `firebase.json` | Firebase service account (optional) |
| `google-oauth-alt.json` | Optional second OAuth client |

### 4) Run (development)

```bash
npm run dev
```

You should see **`[telegram] Online.`** among the logs.

### 5) Windows helpers (`run/` and repo root)

| Script | Role |
|--------|------|
| **`run/dev.bat`** | Telegram only via `tsx` |
| **`run/web.bat`** | Build + `node dist/index.js --web` (+ browser) |
| **`run/pm2.bat`** / **`run/stop-pm2.bat`** | PM2 lifecycle |

**Do not** run **PM2** and **`npm run dev`** with the **same bot token** at once — Telegram long polling will **409 Conflict**. See **`run/README.txt`**.

---

## Configuration & environment

### Strictly required at startup (`src/config/config.ts`)

- **`TELEGRAM_BOT_TOKEN`**

### Strongly recommended

- **`GROQ_API_KEY`** — Whisper + Groq chat when API/engine mode uses Groq.
- **`ALLOWED_USER_IDS`** — Comma-separated numeric Telegram user IDs. **Empty = anyone** can use the bot (testing only).

### Common optional variables

| Variable | Purpose |
|----------|---------|
| `DB_PATH` | SQLite path (default from `paths.json` → `user/data/memory.db`) |
| `GEMINI_API_KEY`, `GEMINI_MODEL` | Gemini API |
| `GROQ_MODEL` | Groq chat model name |
| `GOOGLE_CREDENTIALS_PATH`, `GOOGLE_TOKEN_PATH` | Override OAuth file paths |
| `FIREBASE_PROJECT_ID`, `FIREBASE_SERVICE_ACCOUNT_PATH` | Firebase |
| `WEB_PORT`, `WEB_HOST` | Web UI bind |
| `LOCAL_LLM_BASE_URL`, `LOCAL_LLM_API_KEY`, `LOCAL_LLM_MODELS` | Local OpenAI-compatible API |
| `LOCAL_MODEL_REASONING`, `LOCAL_MODEL_CODING`, `LOCAL_MODEL_FAST`, `LOCAL_MODEL_AUTOMATION`, `LOCAL_INTENT_MODEL` | Task-specific local model tags |
| `DEFAULT_LLM_PROVIDER`, `DEFAULT_LLM_MODEL` | Defaults when routing allows |
| `DEFAULT_DEEP_SEARCH`, `DEFAULT_THINKING`, `DEFAULT_ASSIST_ONLY` | UI/agent flags defaults |
| `MAX_AGENT_ITERATIONS` | Agent loop cap |
| `SAFE_MODE` | When `true`, all non-SAFE tool executions require user confirmation |
| `IMAGE_MODEL`, `VIDEO_MODEL`, `WHISPER_MODEL` | Media / voice model ids |
| **`SHARED_TOOLING_ROOT`** | Overrides `paths.json` → `tooling.sharedRoot` for shared `node_modules` (see below) |

**Firebase:** Fields inside `firebase.json` (**`project_id`**, **`client_email`**, etc.) must match a real GCP project.

---

## `paths.json`

Single source of truth for:

- **`dirs`**: `tokens`, `uploads`, `logs`, `data` (defaults: `src/tokens`, `user/uploads`, `logs`, `user/data`)
- **`files.database`**: SQLite file (default `user/data/memory.db`)
- **`google`**, **`firebase`**, **`optionalOAuthAlt`**
- **`tooling.sharedRoot`**: optional shared folder whose `node_modules` is prepended to tool subprocess **`NODE_PATH`** (and npm prefix). Example in repo: `C:/dev` — change or clear on machines that do not use this layout.
- **`node.sourceRoot`**, **`node.buildOutput`**
- Optional **`web.uiRoot`**: override static UI directory (default: `src/ui` in dev; **`dist/ui`** when `NODE_ENV=production` and `dist/ui/index.html` exists)

Loaded in **`src/config/project-paths.ts`**. **`ensureProjectDirs()`** creates missing directories and runs **legacy migrations** (old root `tokens/`, `data/`, `uploads/` → configured targets when safe).

---

## Shared tooling root (`NODE_PATH` / npm prefix)

When **`tooling.sharedRoot`** (or env **`SHARED_TOOLING_ROOT`**) is set, **`mergeToolEnvironment()`** in **`src/config/tool-process-env.ts`** prepares child processes so **`npm install`**, **`npx`**, and **`node`** can use one shared library tree (used from tools such as **terminal**, **sysinfo**, **screenshot**, **screen**, **desktop**, **notification**, **clipboard**, **ollama**).

Clear **`sharedRoot`** in `paths.json` (or leave env unset) if you do not use a shared dev drive.

---

## TypeScript & build

- **`tsconfig.json`**: `strict`, ESM, **`types`: `["node"]`**, **`src/ui`** excluded from `tsc` (static assets only).
- **`src/node-env.d.ts`**: `/// <reference types="node" />` so editors and `tsc` agree on Node globals (`process`, etc.).
- **`npm run build`**: compiles `src/**/*.ts` → **`dist/`** and recursively copies **`src/ui/`** → **`dist/ui/`**.

---

## How to run

| Command | Result |
|---------|--------|
| `npm run dev` | Telegram only (`tsx`) |
| `npm run dev:web` | Telegram + web UI |
| `npm run build` | `tsc` + copy UI |
| `npm start` | Telegram only (`node dist/index.js`) |
| `npm run start:web` | Telegram + web |
| `npm run start:bg` | PM2 (`ecosystem.config.cjs`) |

PM2 app name: **`jarvis`** → `pm2 logs jarvis`.

**Docker:** `docker compose up -d --build` — default image command may omit `--web`; adjust Dockerfile `CMD` if you need the web server in containers.

---

## Telegram commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome, Google status, help |
| `/tools` | Registered tool names |
| `/engine` | Switch engine (local/api/auto) |
| `/model` | Select local model |
| `/mode` | Show current engine status |
| `/offline` | Toggle offline mode |
| `/google_auth` | OAuth (callback `http://localhost:49152/callback`) |
| `/clear` | Clear this chat's history |
| `/ping` | `Pong.` |
| `/id` | Your numeric user id (for `ALLOWED_USER_IDS`) |

---

## Web UI

- **Frontend:** **`src/ui/`** — `index.html`, `styles/*.css`, `scripts/*.js` (ES modules). **Branding:** `assets/Jarvis.png` (sidebar logo), `assets/Jarvis.ico` + PNG **favicon** / **apple-touch-icon** in `index.html`.
- **Backend:** **`src/gateways/http/server.ts`** — serves static files from **`projectPaths.webUiDir`**, WebSocket chat, REST, uploads.
- Open **`http://WEB_HOST:WEB_PORT`** (default `http://localhost:3000`) after `dev:web` / `start:web`.
- **WebSocket** chat messages support flags such as `deepSearch`, `thinking`, `assistOnly`, and file payloads; **`{ "type": "cancel" }`** cancels the in-flight generation.
- **Safety confirmations** arrive as `{ "type": "confirmation_required", ... }` — the client responds with `{ "type": "confirmation_response", "approved": true/false }`.

**Security:** The web app does **not** implement Telegram's user whitelist. Do not expose the port publicly without a reverse proxy and authentication.

---

## Agent pipeline

The pipeline runs inside `loop.ts`. Every user message passes through the same deterministic sequence.

### Step flow

1. **Cache check** — short, flag-free, previously-seen queries get an instant cached response.
2. **Intent detection** — `engine/intent.ts` classifies the message (type, complexity, tools, priority).
3. **Model routing** — `engine/manager.ts` picks the best provider + model using intent data.
4. **Memory retrieval** — recent messages + keyword-relevant snippets from past conversations.
5. **Planning decision** — `shouldPlan(intent)` branches into two execution paths:
   - **Structured path** (complex tasks) — plan → step-by-step executor → verify → synthesize
   - **Simple path** (lightweight queries) — direct LLM loop
6. **Reflection** — post-execution quality evaluation; may trigger a retry.
7. **Degraded fallback** — if the local LLM fails completely, attempts a tool-free response.

### Structured vs simple path

| Criteria | Structured | Simple |
|----------|-----------|--------|
| `intent.complexity === "high"` | yes | — |
| `intent.needs_tools && complexity !== "low"` | yes | — |
| `intent.priority === "high" && type === "automation"` | yes | — |
| Everything else | — | yes |

---

## Intent classification

**File:** `src/agent/engine/intent.ts`

Intent is the **single source of truth** for task understanding. All downstream decisions (planning, model selection, prompt tone) read from the intent object — they never re-derive these signals.

### Strategy: hybrid detection

1. **Fast heuristic** (regex, no network) — always runs. Returns confidence 0.35–0.92.
2. **Local LLM refinement** — only when heuristic confidence is low, complexity is high, or tools are likely needed. API providers are **never** used for intent classification.

### Output

```typescript
{
  type: "coding" | "reasoning" | "simple" | "automation",
  complexity: "low" | "medium" | "high",
  needs_tools: boolean,
  confidence: number,     // 0.0 – 1.0
  priority: "normal" | "high"
}
```

---

## LLM routing

**Files:** `src/agent/engine/manager.ts`, `src/agent/engine/task-models.ts`

Both Telegram and Web use a single **`resolveRoute(intent, source, chatId)`** function. No separate routing paths.

### Flow

1. Check **pinned model** (user override via `/model` command) — use directly if set.
2. Read **intent classification** → `resolveModelForIntent()` picks the best local model and preferred API provider.
3. Determine **provider** based on engine mode (`local` / `api` / `auto`) + availability.
4. Apply **source-specific constraints** (Web UI is local-first by default).
5. **Log** the routing decision with intent, model, provider, and reason.

### Model selection strategy

| Task type | Local model | API preference |
|-----------|------------|----------------|
| **coding** | `LOCAL_MODEL_CODING` | Gemini (better at code) |
| **reasoning** (complex) | `LOCAL_MODEL_REASONING` | Gemini (long context) |
| **reasoning** (simple) | `LOCAL_MODEL_FAST` | Groq (speed) |
| **automation** | `LOCAL_MODEL_AUTOMATION` or reasoning | Gemini (tool reliability) |
| **simple** | `LOCAL_MODEL_FAST` | Groq (low latency) |

### Engine modes

| Mode | Behavior |
|------|----------|
| **`auto`** (default) | Intent-driven: picks the best available provider |
| **`local`** | Forces local LLM only |
| **`api`** | Forces API providers (Gemini → Groq fallback) |
| **offline** | Blocks all API and online tools |

---

## Structured execution

**Files:** `src/agent/planner.ts`, `src/agent/executor.ts`

When `shouldPlan(intent)` returns true, the system generates a structured plan and executes it step-by-step with verification.

### Plan structure

Each step is independently executable:

```typescript
{
  stepNumber: 1,
  goal: "Search the web for recent news about X",
  action: "tool_call",        // "tool_call" | "llm_reasoning" | "synthesize"
  tool: "web_search",         // required when action is "tool_call"
  expectedResult: "A list of recent articles with titles and URLs",
  dependsOn: []               // step numbers whose output this step needs
}
```

### Execution loop (per step)

1. **Build step context** — plan overview, previous step results, current step goal.
2. **LLM call** — focused prompt scoped to the current step.
3. **Safety gate** — `safety.ts` evaluates every tool call (unchanged from simple path).
4. **Verify result** — deterministic heuristic check against `expectedResult`:
   - Did the tool succeed (no error)?
   - Was the expected tool actually called?
   - Is the output non-empty and usable?
5. **Retry if failed** — up to 2 retries per step with feedback about what went wrong.
6. **Dependency check** — steps with unmet dependencies are skipped with a clear reason.

### After all steps

A **synthesis LLM call** combines all step results into a natural, polished response. If all steps fail, partial results and failure explanations are returned.

### Fallback

If structured plan generation itself fails, the system falls back to the simple execution path.

---

## Safety layer

**File:** `src/agent/safety.ts`

Every tool execution — in both the simple and structured paths — passes through the safety layer. No tool bypasses it.

### Risk classification

| Level | Tools | Behavior |
|-------|-------|----------|
| **SAFE** | `web_search`, `system_info`, `take_screenshot`, memory, time | Auto-approved always |
| **MODERATE** | Gmail (read), Calendar (create), clipboard, file_manager (write) | Auto-approved; confirmation if `SAFE_MODE=true` |
| **DANGEROUS** | Gmail (send), file_manager (delete), browser (click/fill) | **Requires user confirmation** |
| **CRITICAL** | `execute_command`, `desktop_control` (mouse/keyboard), browser (evaluate) | **Requires confirmation + detailed explanation** |

Risk is **action-aware**: `file_manager(action=read)` is SAFE, `file_manager(action=delete)` is DANGEROUS.

### Evaluation pipeline

1. **Parameter validation** — hard block on destructive patterns (`rm -rf /`, `format C:`, `diskpart`, fork bombs, registry deletion, etc.) and system path writes.
2. **Risk classification** — base risk per tool, refined by action/parameters.
3. **Rate limiting** — sliding window per tool+risk category prevents runaway loops (CRITICAL: 5/min, DANGEROUS: 8/min, MODERATE: 20/min, SAFE: 50/min).
4. **Permission decision** — SAFE/MODERATE auto-approved; DANGEROUS/CRITICAL require confirmation.
5. **User confirmation** — sent via Telegram reply or WebSocket prompt; 2-minute timeout; defaults to deny.
6. **Logging** — every decision is logged with tool, args, risk, trigger, and outcome.

### `SAFE_MODE` environment variable

When `SAFE_MODE=true`, **all** non-SAFE tool executions require user confirmation (including MODERATE tools like clipboard writes or calendar creates).

### Confirmation flow

**Telegram:** Bot sends a formatted confirmation message, waits for the user to reply "yes"/"no" (or variants). If no reply in 2 minutes, the action is cancelled.

**Web UI:** Server sends `{ "type": "confirmation_required", tool, risk, explanation, ... }` over WebSocket. The client responds with `{ "type": "confirmation_response", "approved": true/false }`.

---

## Agent modes

Modes modify agent behavior without changing the pipeline:

| Mode | Effect |
|------|--------|
| **`deepSearch`** | Instructs LLM to use `web_search` multiple times, cross-reference sources |
| **`thinking`** | Chain-of-thought reasoning before answering |
| **`assistOnly`** | Blocks execution tools (`execute_command`, `desktop_control`, `browser`, etc.); provides instructions instead |

Modes can be set as defaults via env (`DEFAULT_DEEP_SEARCH`, `DEFAULT_THINKING`, `DEFAULT_ASSIST_ONLY`) or per-message from the Web UI.

---

## Memory: SQLite & migration

- Tables and access: **`src/memory/store.ts`** (`conversations`, chats, memory, logs, tool stats, cache, behavior insights).
- Optional **Firestore** sync when Firebase is configured; hot path still uses SQLite.
- On startup, **legacy** paths are handled: old repo-root **`memory.db`**, **`data/`**, **`uploads/`**, **`tokens/`** may be copied/migrated once into the configured **`user/data`**, **`user/uploads`**, **`src/tokens`** when targets are missing (see **`ensureProjectDirs`** / migration helpers in **`project-paths.ts`**).

---

## Google OAuth

1. Create an OAuth client in Google Cloud; download JSON → **`src/tokens/google-oauth.json`** (or path from `paths.json` / `.env`).
2. In Telegram: **`/google_auth`** and complete the browser flow (**port 49152** must be free).
3. Tokens are stored in **`google-token.json`**; a valid **`refresh_token`** is required for long-lived "connected" status.

---

## Tools reference

Registered from **`src/tools/index.ts`** (each file uses **`registerTool`**):

| Tool name | Source file | Risk | Role |
|-----------|-------------|------|------|
| `get_current_time` | `time.ts` | SAFE | Current time |
| `set_memory`, `get_memory`, `get_all_memory` | `memory.ts` | SAFE | Long-term memory |
| `web_search` | `web-search.ts` | SAFE | Web search |
| `take_screenshot` | `screenshot.ts` | SAFE | Screenshots |
| `analyze_screen` | `screen.ts` | SAFE | Screen / UI analysis |
| `system_info` | `sysinfo.ts` | SAFE | System information |
| `youtube_analytics` | `youtube.ts` | SAFE | YouTube analytics |
| `ollama` | `ollama.ts` | SAFE | Ollama management helpers |
| `generate_image` | `image-gen.ts` | MODERATE | Image generation |
| `generate_video` | `video-gen.ts` | MODERATE | Video generation |
| `clipboard` | `clipboard.ts` | MODERATE | Clipboard read/write |
| `notification` | `notification.ts` | MODERATE | Toast / notifications |
| `gmail` | `gmail.ts` | MODERATE–DANGEROUS | Gmail (read=SAFE, send=DANGEROUS) |
| `google_calendar` | `gcal.ts` | MODERATE–DANGEROUS | Calendar (read=SAFE, delete=DANGEROUS) |
| `google_contacts` | `gcontacts.ts` | MODERATE | Contacts |
| `google_drive` | `gdrive.ts` | MODERATE–DANGEROUS | Drive (read=SAFE, delete=DANGEROUS) |
| `file_manager` | `files.ts` | SAFE–DANGEROUS | File ops (read=SAFE, delete=DANGEROUS) |
| `browser` | `browser.ts` | SAFE–CRITICAL | Browser (get_text=SAFE, evaluate=CRITICAL) |
| `execute_command` | `terminal.ts` | CRITICAL | Shell (PowerShell on Windows) |
| `desktop_control` | `desktop.ts` | CRITICAL | Mouse, keyboard, windows |

Risk levels shown are the **refined** risk (action-dependent). See [Safety layer](#safety-layer) for details.

---

## Security

- **Safety layer** (`safety.ts`) evaluates every tool call before execution — risk classification, parameter validation, rate limiting, and mandatory user confirmation for dangerous/critical actions.
- **`SAFE_MODE=true`** requires confirmation for all non-SAFE tools.
- **Destructive command patterns** are hard-blocked regardless of confirmation (e.g. `rm -rf /`, `format C:`, `diskpart`).
- **System paths** (`C:\Windows\System32`, `/usr/bin`, `/boot`, etc.) are protected from writes.
- The agent can **execute shell commands** and **control the desktop** on the host. Use **`ALLOWED_USER_IDS`** in production.
- Never commit **`.env`** or **`src/tokens/*.json`** with real secrets.
- OAuth uses a **local** listener on **49152** during login.
- **Playwright** can load arbitrary web content; browsing tools are classified as DANGEROUS/CRITICAL.
- The **Web UI** does not implement Telegram's user whitelist — do not expose the port publicly without a reverse proxy and authentication.

---

## Docker, PM2, deploy

- **`Dockerfile`**: Node 20, builds native deps (`better-sqlite3`), copies `src/` (including **`src/ui/`**), `paths.json`, runs **`npm run build`** → **`dist/`** + **`dist/ui/`**.
- **`docker-compose.yml`**: mounts **`./user/data/memory.db`** and token JSON files under **`./src/tokens/`**.
- **`ecosystem.config.cjs`**: uses `paths.json` for the **logs** directory.
- **`deploy.sh`**: intended to run from **project root** on Ubuntu-style hosts (if present in your tree).

---

## Adding a new tool

1. Add **`src/tools/my-tool.ts`** with **`registerTool({ definition, execute })`**.
2. Import it in **`src/tools/index.ts`**: `import "./my-tool.js";`
3. Add the tool's base risk level in **`src/agent/safety.ts`** → `BASE_TOOL_RISK` map.
4. If the tool has mixed-risk actions (e.g. read vs delete), add action-aware refinement in `refineRiskByAction()`.
5. Restart or rebuild.

---

## Troubleshooting

| Symptom | What to check |
|---------|----------------|
| **`Missing required environment variable: TELEGRAM_BOT_TOKEN`** | `.env` in **project root** next to `package.json`. |
| **Voice fails** | **`GROQ_API_KEY`** set; otherwise use text only. |
| **Module / path errors** | Current working directory is the **repo root**. |
| **Bot online but ignores you** | **`ALLOWED_USER_IDS`** includes your id, or leave empty only for testing. Use **`/id`**. |
| **Telegram 401** | Token from BotFather; no stray spaces/quotes in `.env`. |
| **Google auth fails** | `google-oauth.json` present; port **49152** free; complete consent. |
| **Web UI not served** | Use **`dev:web`** / **`start:web`** / **`web.bat`** — plain **`dev`** does not start HTTP. |
| **Web chat errors** | Local LLM URL reachable; Ollama model pulled; web uses **local** only. |
| **Port 3000 in use** | Set **`WEB_PORT`**. |
| **`better-sqlite3` build fails (Windows)** | VS Build Tools (C++), or WSL / Docker. |
| **Rate limits** | Provider quotas; logs may show retries / `RATE_LIMITED:`. |
| **Tool blocked by safety** | Check `[safety]` logs; adjust `SAFE_MODE` or confirm when prompted. |
| **Missing old chats** | DB path is **`user/data/memory.db`** by default; check migration from legacy paths. |
| **409 / `getUpdates` conflict** | Two processes polling the **same** bot token — stop PM2 or stop `dev`. See **`run/README.txt`**. |
| **`tsc` / `process` not found in IDE** | Run **`npm install`**; open folder at repo root; `tsconfig` includes **`types: ["node"]`** and **`src/node-env.d.ts`**. |

---

## Tech stack

| Layer | Technology |
|-------|------------|
| Runtime | Node 20+, TypeScript (ESM), `tsx` for dev |
| Telegram | grammY (long polling) |
| Web | Express 5, `ws`, multer |
| LLM | Local OpenAI-compatible HTTP; Groq SDK; `@google/generative-ai` / `@google/genai` for API features |
| Voice | Groq Whisper |
| DB | `better-sqlite3`; optional Firebase Admin |
| Google | `googleapis` + OAuth2 |
| Browser automation | Playwright |

---

*When you move directories or rename layout entries, update **`paths.json`** and the small **`README.txt`** files under **`src/`**, **`src/ui/`**, and **`user/`** alongside this file.*
