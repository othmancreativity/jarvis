# Jarvis

**Personal AI assistant** on your machine: **Telegram** (always on) and optional **local web UI**. Uses **Groq** and/or **Google Gemini** (and optional **local OpenAI-compatible** models), with **SQLite** memory, optional **Firebase** sync, and **tools** (shell, files, browser, Google APIs, image/video generation, and more).

| Document | Language |
|----------|----------|
| **This file** | English |
| [README.ar.md](./README.ar.md) | العربية (دليل كامل) |
| [JARVIS_INDEX.md](./JARVIS_INDEX.md) | File/path index (Arabic notes + technical paths) |

---

## Table of contents

1. [What it does](#what-it-does)  
2. [Requirements](#requirements)  
3. [Quick start & verification](#quick-start--verification)  
4. [Configuration](#configuration)  
5. [How to run](#how-to-run)  
6. [Path files (`paths.json` / `more_paths.json`)](#path-files-pathsjson--more_pathsjson)  
7. [Telegram commands](#telegram-commands)  
8. [Web UI](#web-ui)  
9. [End-to-end flow](#end-to-end-flow)  
10. [LLM routing](#llm-routing)  
11. [Agent loop & modes](#agent-loop--modes)  
12. [Memory: SQLite & Firebase](#memory-sqlite--firebase)  
13. [Google OAuth (Gmail, Calendar, Drive, …)](#google-oauth-gmail-calendar-drive-)  
14. [Tools reference](#tools-reference)  
15. [Security](#security)  
16. [Docker, PM2, deploy](#docker-pm2-deploy)  
17. [Adding a new tool](#adding-a-new-tool)  
18. [Troubleshooting (extended)](#troubleshooting-extended)  
19. [Tech stack](#tech-stack)  

---

## What it does

- Receives messages on **Telegram** (text and **voice** → transcribed via **Groq Whisper**).
- Builds context from **recent messages** stored in the database.
- Sends messages to the LLM with a **tool list**; the model may answer directly or call **tools** (terminal, files, browser, Google, etc.).
- Repeats until a final answer or **`MAX_AGENT_ITERATIONS`** is reached.
- Optional **web server**: chat UI over **WebSocket**, engine mode (auto/local/api), uploads, Google connect, settings.

**Important:** Normal startup always runs the **Telegram bot**. Adding `--web` runs **Telegram + web together**, not web instead of Telegram.

---

## Requirements

- **Node.js 20+** (`engines` in `package.json`).
- A **Telegram** bot token from BotFather.
- **`GROQ_API_KEY`** (required in code even if Gemini is primary — also used for Whisper).
- **`GEMINI_API_KEY`** (optional; if set and valid, Gemini is tried first, Groq as fallback).
- **Windows:** some tools (desktop, notifications) are OS-specific; in Docker/Linux they may behave differently or be unavailable.

---

## Quick start & verification

### 1) Install

```bash
cd /path/to/jarvis
npm install
```

You must be in the directory that contains **`package.json`**, **`paths.json`**, and **`more_paths.json`**.

### 2) Environment

```bash
copy .env.example .env
```

Edit `.env` and set at least:

- `TELEGRAM_BOT_TOKEN`
- `GROQ_API_KEY`
- `ALLOWED_USER_IDS` — your numeric Telegram user ID (comma-separated for several). **Empty = anyone can use the bot** (only for quick tests).

### 3) Secrets layout (recommended)

Place files under **`tokens/`** (see `more_paths.json`):

| File | Purpose |
|------|---------|
| `tokens/google-oauth.json` | Google OAuth client JSON (`installed` or `web`) |
| `tokens/google-token.json` | Created after OAuth flow |
| `tokens/firebase.json` | Firebase service account (optional) |
| `tokens/google-oauth-alt.json` | Optional second OAuth client |

### 4) Run (development)

```bash
npm run dev
```

**Successful startup** should end with lines similar to:

```text
[telegram] Starting long polling...
[telegram] Online.
```

**Verified** on Windows from repo root: `npx tsx src/index.ts` loads tools, opens DB, and reaches `[telegram] Online.`

### 5) Windows launch scripts (`run/` folder)

| Script | Action |
|--------|--------|
| **`run/dev.bat`** | `npx tsx src/index.ts` (Telegram only) from project root |
| **`run/web.bat`** | `npm run build` then `node dist/index.js --web` + browser |
| **`run/pm2.bat`** | build + PM2 background |
| **`run/stop-pm2.bat`** | `pm2 stop jarvis` — use before `dev` if PM2 is already running the same bot |
| Root **`dev.bat` / `web.bat` / `pm2.bat`** | Same idea without entering `run/` |

**Do not run PM2 and `npm run dev` at the same time** for the same bot token — Telegram will return **409 Conflict**. See **`run/README.txt`**.

If something “does nothing”, you were probably not in the project root — use **`dev.bat`** in the root folder or `cd` to the folder that contains `package.json`.

---

## Configuration

### Required (from `config.ts`)

- `TELEGRAM_BOT_TOKEN`
- `GROQ_API_KEY`

### Common optional variables

- `ALLOWED_USER_IDS` — whitelist (empty = open bot)
- `DB_PATH` — SQLite file (default from `paths.json`, usually `data/memory.db`)
- `GEMINI_API_KEY`, `GROQ_MODEL`, `GEMINI_MODEL`
- `GOOGLE_CREDENTIALS_PATH`, `GOOGLE_TOKEN_PATH` — override OAuth file paths
- `FIREBASE_PROJECT_ID`, `FIREBASE_SERVICE_ACCOUNT_PATH`
- `WEB_PORT`, `WEB_HOST`
- `LOCAL_OPENAI_BASE_URL`, `LOCAL_OPENAI_API_KEY`, `LOCAL_LLM_MODELS`
- `MAX_AGENT_ITERATIONS`
- `DEFAULT_LLM_PROVIDER`, `DEFAULT_LLM_MODEL`, `DEFAULT_DEEP_SEARCH`, `DEFAULT_THINKING`, `DEFAULT_ASSIST_ONLY`

See **`.env.example`** for comments.

**Firebase JSON:** fields like `project_id` and `client_email` inside `tokens/firebase.json` **must match** your real Google Cloud project. Do not rename them to random strings or Firebase will stop working unless you create a matching new project.

---

## How to run

```bash
npm run dev          # Telegram only, TypeScript via tsx
npm run dev:web      # Telegram + web UI
npm run build
npm start            # Telegram only, compiled JS
npm run start:web    # Telegram + web
npm run start:bg     # PM2: ecosystem.config.cjs
```

**PM2** app name: **`jarvis`** → `pm2 logs jarvis`

**Docker:**

```bash
docker compose up -d --build
```

Default container command is **without** `--web` unless you change the Dockerfile `CMD`.

---

## Path files (`paths.json` / `more_paths.json`)

- **`paths.json`** — main folders (`tokens`, `data`, `uploads`, `logs`) and default DB path.
- **`more_paths.json`** — Google OAuth paths, Firebase JSON path, optional alt OAuth file, web/public hints.

The app loads them in **`src/project-paths.ts`** and **`ensureProjectDirs()`** creates missing folders on startup. **Change these files when you move directories** instead of hardcoding paths in code.

---

## Telegram commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome, Google status, help |
| `/tools` | List registered tool names |
| `/google_auth` | Start OAuth (browser → `http://localhost:49152/callback`) |
| `/clear` | Clear conversation history for this chat |
| `/ping` | `Pong.` |
| `/id` | Show your Telegram user id (for `ALLOWED_USER_IDS`) |

---

## Web UI

- Open `http://WEB_HOST:WEB_PORT` (default `http://localhost:3000`) after `dev:web` or `start:web`.
- **WebSocket** chat payload example: `{ "type": "chat", "text": "...", "deepSearch": true, "thinking": true, "assistOnly": false, "files": [...] }`
- **`{ "type": "cancel" }`** cancels the in-flight request.

**Warning:** the web app does **not** replicate Telegram’s user whitelist. Do not expose the port publicly without a reverse proxy and authentication.

---

## End-to-end flow

1. Process starts → `ensureProjectDirs()` → `initDatabase()` (SQLite + optional Firebase).
2. Tools register via `src/tools/index.ts` → `registry.ts`.
3. Telegram long polling starts (and HTTP server if `--web`).
4. User message → authorization check → optional voice transcription → **`runAgentLoop`**.
5. Loop loads recent messages, calls LLM, runs **tool calls** until done or max iterations.
6. Reply sent to Telegram (and/or web), including media when tools return files.

---

## LLM routing

- If **Gemini** key is present and not a placeholder: **Gemini first**, then **Groq**.
- Otherwise **Groq** (and local provider if configured).
- **`chatWithRouting`** respects explicit provider/model from the web UI or env defaults.
- On rate limits, the code may wait and retry; errors may include `RATE_LIMITED:`.

---

## Agent loop & modes

- **Max iterations:** `MAX_AGENT_ITERATIONS` / `config.agent.maxIterations`.
- **`deepSearch`:** extra instructions to use `web_search` more thoroughly.
- **`thinking`:** encourages step-by-step reasoning in the reply.
- **`assistOnly`:** strips “risky” tools from the list sent to the model (`execute_command`, `desktop_control`, `browser`, `notification`, `clipboard`) until the user clearly asks for execution (per system prompt).

Layers: **`planner.ts`**, **`loop.ts`**, **`context.ts`**, **`reflection.ts`** (see source for details).

---

## Memory: SQLite & Firebase

- **`conversations`** / **`chats`** / **`memory`** tables in SQLite (see `memory/store.ts`).
- **Firestore** optional: writes attempted when Firebase is configured; hot path still reads SQLite for speed.
- If an old **`memory.db`** exists in the **project root** and the new path (e.g. `data/memory.db`) does not, it is **copied once** on startup.

---

## Google OAuth (Gmail, Calendar, Drive, …)

1. Create OAuth client in Google Cloud; download JSON → **`tokens/google-oauth.json`** (or path in `more_paths.json` / `.env`).
2. In Telegram run **`/google_auth`**, complete login; callback uses **port 49152**.
3. Tokens saved to **`tokens/google-token.json`** (needs `refresh_token` for “connected” state).

---

## Tools reference

| Tool name | Source file | Role |
|-----------|-------------|------|
| `get_current_time` | `time.ts` | Current time |
| `set_memory`, `get_memory`, `get_all_memory` | `memory.ts` | Long-term key/value memory |
| `generate_image` | `image-gen.ts` | Image generation |
| `generate_video` | `video-gen.ts` | Video generation |
| `web_search` | `web-search.ts` | Web search |
| `execute_command` | `terminal.ts` | Shell (e.g. PowerShell on Windows) |
| `take_screenshot` | `screenshot.ts` | Screenshot |
| `gmail` | `gmail.ts` | Gmail |
| `google_calendar` | `gcal.ts` | Calendar |
| `google_contacts` | `gcontacts.ts` | Contacts |
| `google_drive` | `gdrive.ts` | Drive |
| `youtube_analytics` | `youtube.ts` | YouTube analytics |
| `browser` | `browser.ts` | Playwright automation |
| `analyze_screen` | `screen.ts` | Screen / UI analysis |
| `desktop_control` | `desktop.ts` | Mouse, keyboard, windows |
| `file_manager` | `files.ts` | File operations |
| `system_info` | `sysinfo.ts` | System info |
| `clipboard` | `clipboard.ts` | Clipboard |
| `notification` | `notification.ts` | Notifications |
| `ollama` | `ollama.ts` | Ollama integration |

---

## Security

- The agent can **run commands** and **control the desktop** on the host. Use **`ALLOWED_USER_IDS`** in production.
- Never commit **`.env`** or **`tokens/*.json`**.
- OAuth opens a **local** listener on **49152** during auth.
- **Playwright** can load arbitrary web content.

---

## Docker, PM2, deploy

- **`Dockerfile`**: Node 20, builds native deps for `better-sqlite3`, copies `paths.json` / `more_paths.json`.
- **`docker-compose.yml`**: mounts `data/memory.db` and token files under `./tokens/`.
- **`deploy.sh`**: run from **project root** (where `package.json` + `paths.json` live) on Ubuntu-style servers.
- **`ecosystem.config.cjs`**: reads `paths.json` for the **logs** directory.

---

## Adding a new tool

1. Add `src/tools/my-tool.ts` with `registerTool({ definition, execute })`.
2. Add `import "./my-tool.js";` in `src/tools/index.ts`.
3. Rebuild or restart.

---

## Troubleshooting (extended)

| Symptom | What to check |
|---------|----------------|
| **`Missing required environment variable`** | `TELEGRAM_BOT_TOKEN` and `GROQ_API_KEY` in `.env` in **project root**. |
| **`Cannot find module`** / **`paths.json`** errors | Current directory must be the **repo root** (`package.json` visible). Use root **`dev.bat`** or `cd` correctly. |
| **Process exits immediately** | Read the error text — usually env or syntax in `.env`. |
| **`[telegram] Online` but bot ignores you** | Your user id must be in **`ALLOWED_USER_IDS`**, or leave it empty only for testing. Use **`/id`** in Telegram. |
| **Telegram 401 / not starting** | Regenerate token in BotFather; no extra spaces/quotes mistakes in `.env`. |
| **Google auth fails** | `tokens/google-oauth.json` exists; port **49152** free; finish browser consent. |
| **Web UI won’t load** | You must use **`npm run dev:web`** or **`npm run start:web`** (or `web.bat`). Plain `dev` does not start HTTP. |
| **Port 3000 in use** | Set **`WEB_PORT`** in `.env`. |
| **`better-sqlite3` install/build fails (Windows)** | Install **Visual Studio Build Tools** with C++ workload, or use **WSL** / Docker. |
| **Rate limit / slow** | Switch keys or provider; logs may show retries. |
| **Old chats “missing”** | DB may have moved to **`data/memory.db`**; root `memory.db` is migrated once if the new file did not exist. |
| **`409 Conflict` / `getUpdates` / `only one bot instance`** | Two processes use the **same bot token** with **long polling** (e.g. **PM2** `jarvis` **and** **`npm run dev`**). Telegram allows **only one** `getUpdates` session. **Fix:** `pm2 stop jarvis` or run **`run/stop-pm2.bat`**, then start dev again — or stop dev if you only want PM2. See **`run/README.txt`**. |

---

## Tech stack

| Layer | Technology |
|-------|------------|
| Runtime | Node 20+, TypeScript, ESM |
| Telegram | grammy (long polling) |
| Web | Express 5, `ws`, multer |
| LLM | Groq SDK, Google GenAI APIs |
| Voice | Groq Whisper |
| DB | better-sqlite3; optional Firebase Admin |
| Google | googleapis + OAuth2 |
| Browser automation | Playwright |

---

*When you change folder layout or filenames, update **`paths.json`**, **`more_paths.json`**, and **[JARVIS_INDEX.md](./JARVIS_INDEX.md)** together.*
