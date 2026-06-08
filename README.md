# JARVIS 4.0 — Complete System Redesign

> **From broken monolith to modular, router-driven AI automation system**

## What Was Done

This project completely redesigns the JARVIS automation system with a focus on **correctness, speed, maintainability, and secure local-device control**.

### Deliverables

| Deliverable | Description | Location |
|-------------|-------------|----------|
| **Audit Report** | 17 issues identified in JARVIS 3.0 with severity ratings and fixes | `docs/audit-report.md` |
| **Design Specification** | Complete architecture spec for JARVIS 4.0 | `docs/design.md` |
| **Main Workflow** | Redesigned entry orchestrator with 3 entry points | `workflow/jarvis-4-0-main.json` |
| **Intent Router** | LLM-based intent classification sub-workflow | `workflow/jarvis-intent-router.json` |
| **General Chat** | Conversation handler sub-workflow | `workflow/jarvis-general-chat.json` |
| **Service Dispatcher** | Routes to 10 Google service agents | `workflow/jarvis-service-dispatcher.json` |
| **YouTube Agent** | Sample Google service agent sub-workflow | `workflow/jarvis-youtube-agent.json` |
| **Local Bridge** | n8n → laptop command bridge sub-workflow | `workflow/jarvis-local-bridge.json` |
| **Response Sender** | Formats and sends replies to all sources | `workflow/jarvis-response-sender.json` |
| **Memory Persist** | Simplified single-user memory system | `workflow/jarvis-memory-persist.json` |
| **Python App** | Desktop companion with audio viz, i18n, safety | `python-app/` |
| **Automation Scripts** | Browser, apps, files, screen, shell, system | `python-app/automation/` |

---

## Audit Summary

### JARVIS 3.0 Had 13 Critical Issues

| # | Issue | Severity |
|---|-------|----------|
| 1 | **Missing `Merge Inputs` node** — all 6 media paths dead-end | CRITICAL |
| 2 | **Task Manager disconnected** — unreachable dead code | CRITICAL |
| 3 | **Open Loop Manager disconnected** — unreachable dead code | CRITICAL |
| 4 | **AI Agent has zero tools** — chat-only, no actions | CRITICAL |
| 5 | Workflow `active: false` — not running | HIGH |
| 6 | Typing Indicator blocks on failure | HIGH |
| 7 | Unsupported Type Handler is terminal | HIGH |
| 8 | Execution Logger is dead end | HIGH |
| 9 | STM Update After Summary is terminal | HIGH |
| 10 | No connection from media to Language Detect | HIGH |
| 11 | Single entry point (Telegram only) | MEDIUM |
| 12 | 73-node monolith | MEDIUM |
| 13 | No Google service integration | MEDIUM |

---

## New Architecture (JARVIS 4.0)

### Router + Specialized Agents Pattern

```
Telegram / Website / Local Script
              │
    ┌─────────▼──────────┐
    │  Request Normalizer │
    ├─────────┬──────────┤
    │  Auth & Rate Limit  │
    ├─────────┼──────────┤
    │  Intent Router      │
    └────┬────┼────┬────┘
         │    │    │
   General  Service  Local
    Chat    Agents   Device
              │      Bridge
         ┌────┴────┐
    YouTube  Drive  Gmail  Calendar
    Translate Contacts Docs Slides
    Tasks    Sheets
              │
    ┌─────────▼──────────┐
    │  Response Sender    │
    └────────────────────┘
```

### Key Improvements

| Metric | 3.0 | 4.0 |
|--------|-----|-----|
| Entry Points | 1 | 3 |
| Google Services | 0 | 10 |
| Local Device Control | No | Yes |
| Safety Confirmation | No | Yes |
| Max Nodes/Workflow | 73 | ~8 |
| Workflow Files | 1 | 17 |
| Tool Connections | 0 | 10+ |

---

## Quick Start

### 1. n8n Workflows

Import the workflow files into n8n:

1. `workflow/jarvis-4-0-main.json` — Main orchestrator
2. `workflow/jarvis-intent-router.json` — Intent classification
3. `workflow/jarvis-general-chat.json` — Chat handler
4. `workflow/jarvis-service-dispatcher.json` — Service routing
5. `workflow/jarvis-youtube-agent.json` — Sample agent
6. `workflow/jarvis-local-bridge.json` — Device bridge
7. `workflow/jarvis-response-sender.json` — Response formatting
8. `workflow/jarvis-memory-persist.json` — Memory system

Set these environment variables in n8n:

```bash
TELEGRAM_BOT_TOKEN=your_bot_token
GROQ_API_KEY=your_groq_key
OWNER_USER_ID=your_telegram_user_id
JARVIS_BRIDGE_SECRET=shared_secret_with_laptop
GOOGLE_API_KEY=your_google_api_key  # For YouTube etc.
```

### 2. Python Desktop App

```bash
cd python-app
pip install -r requirements.txt

# Set environment variables
export JARVIS_BRIDGE_SECRET=shared_secret_with_laptop
export JARVIS_MODEL="llama-4-scout-17b-16e-instruct"

# Run
python main.py
```

### 3. Database Setup

Run this SQL to create the simplified single-user schema:

```sql
CREATE TABLE IF NOT EXISTS jarvis_memory (
  id SERIAL PRIMARY KEY,
  category TEXT NOT NULL,
  key TEXT NOT NULL,
  value JSONB NOT NULL DEFAULT '{}',
  confidence FLOAT DEFAULT 0.5,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(category, key)
);

CREATE TABLE IF NOT EXISTS jarvis_stm (
  id SERIAL PRIMARY KEY,
  messages JSONB DEFAULT '[]',
  rolling_summary TEXT DEFAULT '',
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS jarvis_logs (
  id SERIAL PRIMARY KEY,
  session_key TEXT,
  source TEXT,
  intent TEXT,
  input_text TEXT,
  response_text TEXT,
  execution_ms INT,
  error TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO jarvis_stm (messages, rolling_summary) VALUES ('[]', '') ON CONFLICT DO NOTHING;
```

---

## Python App Features

### Desktop UI (PyQt6)
- Modern dark-themed interface
- Chat panel with message history
- Language switcher (EN / AR)
- System tray integration

### Real-Time Audio Visualization
- Animated frequency bar visualization
- Color gradient (blue → purple → pink)
- 32 frequency bands at 20 FPS

### Multilingual Support
- **English** — Full UI translation
- **Arabic** — Full UI translation with **RTL layout**
- Runtime language switching

### Model Display
- Bottom-left panel showing active LLM model name
- Bridge connection status indicator (green/red dot)

### Safety Confirmation Dialog
- Modal dialog for all risky operations
- Shows: Action, Target, Risk, Requester, Timestamp
- **Deny by default** — 60-second auto-deny timeout
- "Remember choice for 5 minutes" option
- Full audit logging to `~/.jarvis/audit.log`

### WebSocket Bridge
- Bidirectional communication with n8n
- Bearer token authentication
- Heartbeat ping/pong every 30 seconds
- Structured command/response protocol

### Local Device Automation
| Module | Operations | Confirmation |
|--------|-----------|-------------|
| Browser | Open, navigate, screenshot, close | No |
| Apps | Open, close, list running | No |
| Files | List, read | No |
| Files | Move, delete | **Yes** |
| Screen | Screenshot | No |
| Screen | Record start/stop | **Yes** |
| Shell | Execute | **Yes** |
| System | Info, processes | No |

---

## Safety Policy

All automation follows a **deny-by-default** policy:

1. **No covert monitoring** — Screen recording only when explicitly requested
2. **No credential access** — Passwords, tokens never accessible
3. **No network exfiltration** — Only localhost communication
4. **Blocked shell patterns** — Fork bombs, pipe-to-shell, disk formatters
5. **Protected paths** — `.ssh/`, `.gnupg/`, system directories
6. **Audit trail** — Every action logged with timestamp and result
7. **User confirmation** — All risky ops require explicit UI approval
8. **Auto-deny timeout** — 60 seconds, no response = denied

---

## End-to-End Example

**User (Telegram):** "Open Chrome, go to example.com, take a screenshot, and tell me what you see"

**Flow:**
1. Telegram Trigger receives message
2. Request Normalizer parses input
3. Auth Gate validates user
4. Intent Router classifies: `local_browser` + `local_screenshot`
5. Local Device Bridge sends commands to laptop
6. Python app:
   - Opens Chrome (no confirmation needed)
   - Navigates to example.com (no confirmation)
   - Captures screenshot (no confirmation)
7. Response Sender returns screenshot + page info
8. Memory Persist logs the interaction

---

## File Structure

```
jarvis-redesign/
├── docs/
│   ├── audit-report.md          # Full audit with 17 issues
│   └── design.md                # Complete redesign specification
├── workflow/
│   ├── jarvis-4-0-main.json     # Main orchestrator (17 nodes)
│   ├── jarvis-intent-router.json # Intent classification
│   ├── jarvis-general-chat.json  # Chat handler
│   ├── jarvis-service-dispatcher.json # Routes to 10 agents
│   ├── jarvis-youtube-agent.json # Sample Google agent
│   ├── jarvis-local-bridge.json  # Device bridge
│   ├── jarvis-response-sender.json # Response formatting
│   ├── jarvis-memory-persist.json # Memory system
│   └── tool-registry.json        # Operation definitions
├── python-app/
│   ├── main.py                   # Desktop app entry point
│   ├── bridge_server.py          # WebSocket server
│   ├── requirements.txt          # Python dependencies
│   ├── automation/
│   │   ├── __init__.py
│   │   ├── browser.py            # Chrome control
│   │   ├── apps.py               # App open/close
│   │   ├── files.py              # File operations (safe)
│   │   ├── screen.py             # Screenshot/recording
│   │   ├── shell.py              # Shell (deny-by-default)
│   │   └── system_info.py        # System information
│   └── locales/
│       ├── en.json               # English strings
│       └── ar.json               # Arabic strings (RTL)
└── README.md                     # This file
```

---

## Notes

### Tools File
The user mentioned a "Tools file" with prebuilt tool definitions. This was not provided, so the tool registry (`workflow/tool-registry.json`) was created from scratch based on standard Google API endpoints. If you have an existing Tools file, the registry should be merged with it rather than replacing it.

### Google OAuth
The redesigned workflows use `GOOGLE_API_KEY` for read-only APIs (YouTube) and expect `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, and `GOOGLE_REFRESH_TOKEN` for OAuth-required APIs (Gmail, Drive, Calendar, etc.). Set these up in Google Cloud Console and n8n credentials.

### Website / Local Entry Points
The Website Webhook and Local Script Webhook nodes are configured as placeholder entry points. To activate them:
- **Website:** Point your frontend to the n8n webhook URL (`/webhook/jarvis-webhook`)
- **Local:** Configure your Python script to POST to `/webhook/jarvis-local` with header `x-jarvis-source: local`

---

## License

This is a personal automation system. Use at your own risk. The safety mechanisms are provided as a best-effort layer and do not guarantee protection against all malicious actions.
