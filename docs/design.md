# JARVIS 4.0 — System Redesign Specification

## Document Control

| Version | Date | Author | Description |
|---------|------|--------|-------------|
| 4.0 | 2026-06-08 | AI Architect | Complete redesign: router + specialized agents, local device control, single-user |

---

## 1. Executive Summary

JARVIS 3.0 is a monolithic n8n workflow (73 nodes) that is **non-functional** due to 13 critical structural defects, most notably a missing `Merge Inputs` node that severs the media pipeline from the context/AI pipeline. The AI agent has zero tool connections, making it a chat-only bot with no action capability. There is no Google service integration, no local device control, and no modularity.

This specification redesigns JARVIS into a **modular, router-driven, single-user automation system** with:
- **Router + Specialized Agent Architecture** — one agent per Google service
- **Local Device Control** — Python desktop companion app with secure command bridge
- **Three Entry Points** — Telegram, Website Webhook, Local Script
- **Deterministic Tool Registry** — no guesswork, explicit operation routing
- **Safety-First Design** — explicit user confirmation for all risky operations

---

## 2. Audit Summary (JARVIS 3.0)

### 2.1 Critical Errors Found (13)

| # | Severity | Issue | Impact |
|---|----------|-------|--------|
| 1 | **CRITICAL** | `Merge Inputs` node does not exist but is referenced by 6 media path nodes | **Entire media pipeline dead-ends** — no text/voice/photo/doc/location ever reaches AI |
| 2 | **CRITICAL** | Task Manager node exists but is **never connected** to workflow | Task CRUD code is unreachable dead code |
| 3 | **CRITICAL** | Open Loop Manager node exists but is **never connected** | Open loop detection is unreachable dead code |
| 4 | **CRITICAL** | AI Agent has **zero tool connections** | Agent cannot perform any actions — chat-only |
| 5 | HIGH | Workflow has `active: false` | Workflow is not running |
| 6 | HIGH | `Unsupported Type Handler` has no outgoing connections | Flow terminates without response for unsupported types |
| 7 | HIGH | `Execution Logger` is a dead end | Logging blocks are terminal — should be non-blocking |
| 8 | HIGH | `STM Update After Summary` has no outgoing connections | Post-summary STM update is a terminal operation |
| 9 | HIGH | `Typing Indicator` lacks `continueOnFail` | A single Telegram API failure blocks the entire pipeline |
| 10 | MEDIUM | Only single entry point (Telegram) | No website webhook, no local script entry |
| 11 | MEDIUM | 73 nodes in monolithic workflow | No modularity, difficult maintenance |
| 12 | MEDIUM | Zero Google service integration | No YouTube, Drive, Gmail, Calendar, etc. |
| 13 | LOW | Rate limit circuit breaker opens for 60s+ | Can permanently deny legitimate users on transient DB failures |

### 2.2 Redundancy Issues
- 8 separate HTTP Request nodes hitting Telegram API (consolidate to 1 reusable function/sub-workflow)
- 5 separate Postgres INSERT/UPSERT nodes with similar patterns (use parameterized operations)
- Duplicate error handling patterns across code nodes

### 2.3 Missing Features (Required by New Architecture)
- No tool/operation registry
- No router pattern for service selection
- No Google OAuth credential management
- No sub-workflow structure
- No local device bridge
- No website webhook entrypoint
- No local script entrypoint

---

## 3. Target Architecture Overview

### 3.1 High-Level Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                        ENTRY POINTS                                  │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────────────┐   │
│  │  Telegram   │  │   Website    │  │    Local Python Script   │   │
│  │   Trigger   │  │   Webhook    │  │       (Webhook)          │   │
│  └──────┬──────┘  └──────┬───────┘  └────────────┬─────────────┘   │
└─────────┼────────────────┼───────────────────────┼─────────────────┘
          │                │                       │
          └────────────────┴───────────────────────┘
                              │
                    ┌─────────▼──────────┐
                    │  Request Normalizer │  ← Normalizes all inputs to common schema
                    └─────────┬──────────┘
                              │
                    ┌─────────▼──────────┐
                    │    Auth & Rate      │  ← Single-user: simplified auth
                    │     Limit Gate      │
                    └─────────┬──────────┘
                              │
                    ┌─────────▼──────────┐
                    │  INPUT ROUTER       │  ← LLM-based intent classification
                    │  (Intent Detector)  │
                    └─────────┬──────────┘
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
    ┌─────▼──────┐    ┌──────▼───────┐   ┌──────▼───────┐
    │  General   │    │   Google     │   │   Local      │
    │   Chat     │    │   Service    │   │   Device     │
    │  Handler   │    │   Router     │   │   Bridge     │
    └────────────┘    └──────┬───────┘   └──────┬───────┘
                             │                    │
              ┌──────────────┼──────────┐        │
              │              │          │        │
        ┌─────▼────┐  ┌─────▼────┐ ┌───▼────┐ ┌─▼──────────┐
        │ YouTube  │  │  Drive   │ │ Gmail  │ │ Calendar   │
        │  Agent   │  │  Agent   │ │ Agent  │ │  Agent     │
        └──────────┘  └──────────┘ └────────┘ └────────────┘
        ┌──────────┐  ┌──────────┐ ┌────────┐ ┌────────────┐
        │Translate │  │ Contacts │ │  Docs  │ │  Sheets    │
        │  Agent   │  │  Agent   │ │ Agent  │ │  Agent     │
        └──────────┘  └──────────┘ └────────┘ └────────────┘
        ┌──────────┐  ┌──────────┐
        │  Tasks   │  │  Slides  │
        │  Agent   │  │  Agent   │
        └──────────┘  └──────────┘
                             │
                    ┌────────▼────────┐
                    │ Response Builder │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Reply Sender   │  ← Routes back to correct entry source
                    └─────────────────┘
```

### 3.2 Design Principles

1. **Single-User Only** — No multi-tenant storage, no per-user partitions, no team assumptions
2. **Router + Agents** — One dedicated agent per Google service, deterministic tool registry
3. **Local-First Safety** — All risky operations require explicit laptop UI confirmation
4. **Modular Sub-Workflows** — Each service agent is a sub-workflow; router is a sub-workflow
5. **Fail Fast, Recover Clean** — `continueOnFail` on all non-critical nodes, clear error propagation
6. **Minimal Token Usage** — Context compression, no redundant LLM calls, cached where possible
7. **Deterministic Routing** — Intent classification → explicit service selection → operation lookup

---

## 4. Module Specifications

### 4.1 Module: Entry Points & Request Normalizer

**File:** `workflow/01-entry-points.json` (sub-workflow)

**Entry Points:**

| Entry | Node Type | Config | Status |
|-------|-----------|--------|--------|
| Telegram | `telegramTrigger` | Webhook mode, credential ref | Active |
| Website | `webhook` | Path: `/jarvis/webhook`, method: POST | Placeholder — empty |
| Local Script | `webhook` | Path: `/jarvis/local`, method: POST | Placeholder — empty |

**Request Normalizer Output Schema:**
```json
{
  "source": "telegram|website|local",
  "userId": "string (single-user: always 'default')",
  "sessionId": "string (UUID per conversation)",
  "messageId": "string (source-specific)",
  "inputType": "text|voice|photo|document|location|command",
  "inputText": "string (normalized text content)",
  "inputBinary": "null|{base64, mimeType, fileName}",
  "metadata": {
    "chatId": "string (for Telegram replies)",
    "replyEndpoint": "string (for website/local replies)",
    "timestamp": "ISO 8601",
    "clientInfo": "object"
  }
}
```

### 4.2 Module: Auth & Rate Limit Gate

**File:** `workflow/02-auth-gate.json` (sub-workflow)

**Single-User Simplifications:**
- `ALLOWED_USER_IDS` → replaced with `OWNER_USER_ID` (single string, not list)
- `ADMIN_USER_IDS` → removed (single user is always admin)
- `AUTH_MODE` → simplified to `open|protected` (protected = only OWNER_USER_ID)
- Rate limit: in-memory only, no PostgREST dependency
- Webhook secret validation: fail-fast at entry

**Rate Limit Config:**
- Window: 60 seconds
- Max requests: configurable via `RATE_LIMIT_PER_MINUTE` (default: 30)
- Storage: in-memory ring buffer (resets on restart — acceptable for single-user)
- No distributed/circuit-breaker complexity

### 4.3 Module: Intent Router

**File:** `workflow/03-intent-router.json` (sub-workflow)

**Purpose:** Classify user intent and route to the correct service handler.

**Implementation:** LLM-based zero-shot classification with constrained output.

**Intent Categories:**

| Intent | Target | Description |
|--------|--------|-------------|
| `general_chat` | General Chat Handler | Casual conversation, questions |
| `youtube_*` | YouTube Agent | Video search, info, download |
| `drive_*` | Drive Agent | File listing, upload, download, search |
| `gmail_*` | Gmail Agent | Email search, send, read, delete |
| `calendar_*` | Calendar Agent | Event listing, creation, deletion |
| `translate` | Translate Agent | Text translation |
| `contacts_*` | Contacts Agent | Contact listing, search, creation |
| `docs_*` | Docs Agent | Document creation, editing |
| `slides_*` | Slides Agent | Presentation creation, editing |
| `tasks_*` | Tasks Agent | Task creation, completion, listing |
| `sheets_*` | Sheets Agent | Spreadsheet operations |
| `local_*` | Local Device Bridge | Laptop control, automation |

**Router LLM Prompt:**
```
You are an intent classifier for JARVIS, a personal AI assistant.
Analyze the user's message and classify it into exactly one category.

Available categories:
- general_chat: casual conversation, questions, advice
- youtube_search: find videos, get video info
- youtube_download: download a video
- drive_list: list files in Google Drive
- drive_search: search for files
- drive_upload: upload a file
- drive_download: download a file
- drive_delete: delete a file
- gmail_search: search emails
- gmail_read: read an email
- gmail_send: send an email
- gmail_delete: delete an email
- calendar_list: list events
- calendar_create: create an event
- calendar_delete: delete an event
- translate: translate text
- contacts_list: list contacts
- contacts_search: search contacts
- contacts_create: create a contact
- docs_create: create a document
- docs_read: read a document
- docs_edit: edit a document
- slides_create: create a presentation
- sheets_read: read spreadsheet data
- sheets_write: write spreadsheet data
- local_screenshot: capture screen
- local_browser: open browser, navigate
- local_app: open/close application
- local_file: file operations
- local_shell: run commands
- local_system: system info, settings

Output ONLY a JSON object:
{"intent": "category_name", "confidence": 0.0-1.0, "params": {"key": "value"}}
```

### 4.4 Module: Tool/Operation Registry

**File:** `workflow/tool-registry.json` (static configuration)

This is the source of truth for all available operations. The router and all agents reference this registry.

```json
{
  "registry_version": "4.0.0",
  "services": {
    "youtube": {
      "operations": {
        "search": {"params": ["query", "max_results"], "method": "GET", "endpoint": "/youtube/v3/search"},
        "get_video": {"params": ["video_id"], "method": "GET", "endpoint": "/youtube/v3/videos"},
        "get_channel": {"params": ["channel_id"], "method": "GET", "endpoint": "/youtube/v3/channels"},
        "list_playlists": {"params": ["channel_id"], "method": "GET", "endpoint": "/youtube/v3/playlists"}
      }
    },
    "drive": {
      "operations": {
        "list": {"params": ["page_size", "q"], "method": "GET", "endpoint": "/drive/v3/files"},
        "get": {"params": ["file_id"], "method": "GET", "endpoint": "/drive/v3/files/{file_id}"},
        "create": {"params": ["name", "mime_type", "parents"], "method": "POST", "endpoint": "/drive/v3/files"},
        "update": {"params": ["file_id", "name"], "method": "PATCH", "endpoint": "/drive/v3/files/{file_id}"},
        "delete": {"params": ["file_id"], "method": "DELETE", "endpoint": "/drive/v3/files/{file_id}", "risky": true},
        "upload": {"params": ["name", "content", "mime_type"], "method": "POST", "endpoint": "/upload/drive/v3/files"},
        "download": {"params": ["file_id"], "method": "GET", "endpoint": "/drive/v3/files/{file_id}?alt=media"}
      }
    },
    "gmail": {
      "operations": {
        "list": {"params": ["max_results", "q"], "method": "GET", "endpoint": "/gmail/v1/users/me/messages"},
        "get": {"params": ["message_id"], "method": "GET", "endpoint": "/gmail/v1/users/me/messages/{message_id}"},
        "send": {"params": ["to", "subject", "body"], "method": "POST", "endpoint": "/gmail/v1/users/me/messages/send", "risky": true},
        "trash": {"params": ["message_id"], "method": "POST", "endpoint": "/gmail/v1/users/me/messages/{message_id}/trash", "risky": true},
        "delete": {"params": ["message_id"], "method": "DELETE", "endpoint": "/gmail/v1/users/me/messages/{message_id}", "risky": true}
      }
    },
    "calendar": {
      "operations": {
        "list": {"params": ["calendar_id", "time_min", "time_max", "max_results"], "method": "GET", "endpoint": "/calendar/v3/calendars/{calendar_id}/events"},
        "get": {"params": ["calendar_id", "event_id"], "method": "GET", "endpoint": "/calendar/v3/calendars/{calendar_id}/events/{event_id}"},
        "create": {"params": ["calendar_id", "summary", "start", "end", "description"], "method": "POST", "endpoint": "/calendar/v3/calendars/{calendar_id}/events"},
        "update": {"params": ["calendar_id", "event_id", "summary", "start", "end"], "method": "PATCH", "endpoint": "/calendar/v3/calendars/{calendar_id}/events/{event_id}"},
        "delete": {"params": ["calendar_id", "event_id"], "method": "DELETE", "endpoint": "/calendar/v3/calendars/{calendar_id}/events/{event_id}", "risky": true}
      }
    },
    "translate": {
      "operations": {
        "translate": {"params": ["text", "target_language", "source_language"], "method": "POST", "endpoint": "/language/translate/v2"},
        "detect": {"params": ["text"], "method": "POST", "endpoint": "/language/translate/v2/detect"},
        "list_languages": {"params": ["target"], "method": "GET", "endpoint": "/language/translate/v2/languages"}
      }
    },
    "contacts": {
      "operations": {
        "list": {"params": ["page_size"], "method": "GET", "endpoint": "/people/v1/people/me/connections"},
        "get": {"params": ["resource_name"], "method": "GET", "endpoint": "/people/v1/{resource_name}"},
        "create": {"params": ["names", "email_addresses", "phone_numbers"], "method": "POST", "endpoint": "/people/v1/people:createContact"},
        "update": {"params": ["resource_name", "names", "email_addresses"], "method": "PATCH", "endpoint": "/people/v1/{resource_name}:updateContact"},
        "delete": {"params": ["resource_name"], "method": "DELETE", "endpoint": "/people/v1/{resource_name}:deleteContact", "risky": true}
      }
    },
    "docs": {
      "operations": {
        "create": {"params": ["title"], "method": "POST", "endpoint": "/docs/v1/documents"},
        "get": {"params": ["document_id"], "method": "GET", "endpoint": "/docs/v1/documents/{document_id}"},
        "batch_update": {"params": ["document_id", "requests"], "method": "POST", "endpoint": "/docs/v1/documents/{document_id}:batchUpdate"}
      }
    },
    "slides": {
      "operations": {
        "create": {"params": ["title"], "method": "POST", "endpoint": "/slides/v1/presentations"},
        "get": {"params": ["presentation_id"], "method": "GET", "endpoint": "/slides/v1/presentations/{presentation_id}"},
        "batch_update": {"params": ["presentation_id", "requests"], "method": "POST", "endpoint": "/slides/v1/presentations/{presentation_id}:batchUpdate"}
      }
    },
    "tasks": {
      "operations": {
        "list_tasklists": {"params": ["max_results"], "method": "GET", "endpoint": "/tasks/v1/users/@me/lists"},
        "list_tasks": {"params": ["tasklist_id"], "method": "GET", "endpoint": "/tasks/v1/lists/{tasklist_id}/tasks"},
        "get": {"params": ["tasklist_id", "task_id"], "method": "GET", "endpoint": "/tasks/v1/lists/{tasklist_id}/tasks/{task_id}"},
        "create": {"params": ["tasklist_id", "title", "notes", "due"], "method": "POST", "endpoint": "/tasks/v1/lists/{tasklist_id}/tasks"},
        "update": {"params": ["tasklist_id", "task_id", "title", "status"], "method": "PATCH", "endpoint": "/tasks/v1/lists/{tasklist_id}/tasks/{task_id}"},
        "delete": {"params": ["tasklist_id", "task_id"], "method": "DELETE", "endpoint": "/tasks/v1/lists/{tasklist_id}/tasks/{task_id}", "risky": true}
      }
    },
    "sheets": {
      "operations": {
        "create": {"params": ["title"], "method": "POST", "endpoint": "/sheets/v4/spreadsheets"},
        "get": {"params": ["spreadsheet_id"], "method": "GET", "endpoint": "/sheets/v4/spreadsheets/{spreadsheet_id}"},
        "read_values": {"params": ["spreadsheet_id", "range"], "method": "GET", "endpoint": "/sheets/v4/spreadsheets/{spreadsheet_id}/values/{range}"},
        "write_values": {"params": ["spreadsheet_id", "range", "values"], "method": "PUT", "endpoint": "/sheets/v4/spreadsheets/{spreadsheet_id}/values/{range}"},
        "append_values": {"params": ["spreadsheet_id", "range", "values"], "method": "POST", "endpoint": "/sheets/v4/spreadsheets/{spreadsheet_id}/values/{range}:append"}
      }
    }
  }
}
```

**Risky Operations:** Marked with `"risky": true`. These require confirmation before execution.

### 4.5 Module: Service Agents (10 Sub-Workflows)

Each service agent follows the same pattern:

```
Sub-Workflow Input:  {intent, params, auth_token, context}
Sub-Workflow Output: {success, data, error, human_readable}
```

**Agent Template:**

1. **Parameter Validation** — Validate required params against registry schema
2. **Auth Check** — Ensure valid Google OAuth token (refresh if needed)
3. **Operation Execution** — Make API call via HTTP Request node
4. **Response Formatting** — Convert API response to human-readable text
5. **Error Handling** — Structured error with fallback message

**Agent Nodes (per agent):**
- 1x `code` — Parameter validator
- 1x `httpRequest` — Google API call
- 1x `code` — Response formatter
- Total: ~3 nodes per agent × 10 agents = 30 nodes (vs. 73 in monolith)

### 4.6 Module: Local Device Bridge

**File:** `workflow/07-local-bridge.json` (sub-workflow)

**Purpose:** Send commands to the Python desktop app and receive results.

**Communication Protocol:** WebSocket over local network (or HTTP long-polling fallback)

**Command Schema (n8n → Laptop):**
```json
{
  "command_id": "uuid",
  "action": "screenshot|browser_open|browser_navigate|app_open|app_close|file_list|file_move|file_delete|shell_exec|system_info|screen_record_start|screen_record_stop",
  "params": {},
  "requires_confirmation": true|false,
  "timeout_ms": 30000
}
```

**Response Schema (Laptop → n8n):**
```json
{
  "command_id": "uuid",
  "status": "success|error|denied|timeout",
  "result": {},
  "screenshot_base64": "...",
  "execution_ms": 1234
}
```

**Safety Gate:** All `risky` operations require user confirmation on the laptop UI before execution.

### 4.7 Module: Response Builder & Sender

**File:** `workflow/08-response.json` (sub-workflow)

- Formats agent output into appropriate response format
- Routes response to correct entry point (Telegram vs. website vs. local)
- Handles markdown → HTML conversion for Telegram
- Handles message splitting for long responses
- Error message formatting

### 4.8 Module: Memory System (Simplified)

**File:** `workflow/09-memory.json` (sub-workflow)

**Single-User Simplifications:**
- Remove `user_id` from all DB queries (single user)
- STM: single JSON file or SQLite table
- LTM: single table, no user partition
- Memory classifier: keep but simplified (no per-user context)
- Summary: run on threshold, simpler schema

**Schema (Single Table):**
```sql
CREATE TABLE IF NOT EXISTS jarvis_memory (
  id SERIAL PRIMARY KEY,
  category TEXT NOT NULL,  -- PROFILE, PREFERENCES, GOALS, TASKS, FACTS, CONTEXT
  key TEXT NOT NULL,
  value JSONB NOT NULL,
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
  intent TEXT,
  input_text TEXT,
  response_text TEXT,
  execution_ms INT,
  error TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 5. Python Desktop Companion App

### 5.1 Architecture

```
python-app/
├── main.py              # Application entry point
├── bridge_server.py     # WebSocket server for n8n communication
├── ui/
│   ├── main_window.py   # Main application window (PyQt6)
│   ├── chat_panel.py    # Chat/conversation display
│   ├── audio_viz.py     # Real-time audio frequency visualization
│   ├── model_display.py # Bottom-left model indicator
│   └── safety_dialog.py # Confirmation dialog for risky operations
├── automation/
│   ├── browser.py       # Browser control (selenium/playwright)
│   ├── apps.py          # Application open/close
│   ├── files.py         # File operations (with safety)
│   ├── screen.py        # Screenshot & screen recording
│   ├── shell.py         # Shell command execution (with safety)
│   └── system_info.py   # System information
├── locales/
│   ├── en.json          # English strings
│   └── ar.json          # Arabic strings
└── assets/
    └── icon.png
```

### 5.2 Technology Stack

| Component | Choice | Rationale |
|-----------|--------|-----------|
| UI Framework | **PyQt6** | Best-in-class Python UI, native widgets, RTL support, mature |
| Audio Visualization | **pyqtgraph** + **pyaudio** | Real-time FFT visualization, free, performant |
| WebSocket Server | **websockets** library | Async, lightweight, bidirectional |
| Browser Control | **playwright** | Modern, fast, headless Chrome control |
| Screen Capture | **mss** + **Pillow** | Fast multi-monitor screenshot |
| Screen Recording | **opencv-python** | Video encoding, widely supported |
| Internationalization | **PyQt6 QTranslator** | Native Qt i18n with RTL layout support |

### 5.3 UI Layout

```
┌─────────────────────────────────────────────────────────────┐
│  JARVIS Companion App                              [EN/AR]  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                                                     │   │
│  │         Conversation / Chat History                 │   │
│  │                                                     │   │
│  │                                                     │   │
│  │                                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  🎤 Real-Time Audio Frequency Visualization         │   │
│  │  ││││ ││ │││││ │ │││││ ││││ │││││ │ │││││ ││││   │   │
│  │  │││││││ │││││ ││││││││ │││││ │││││││ │││││││││   │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  [Text Input Field]              [Send] [Voice] 📎 │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  🤖 Model: llama-4-scout-17b-16e-instruct          │   │
│  │  🔗 Bridge: Connected | 2 pending confirmations     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 5.4 Multilingual Support

- All UI strings externalized to `locales/{lang}.json`
- Runtime language switching via `QTranslator`
- **RTL Support:** `setLayoutDirection(Qt.LayoutDirection.RightToLeft)` for Arabic
- Arabic font: Noto Sans Arabic (bundled or system)
- Date/time formatting: `QLocale` for locale-aware formatting

### 5.5 Safety Dialog System

All risky operations trigger a modal confirmation dialog:

```
┌─────────────────────────────────────────┐
│  ⚠️  Action Requires Confirmation      │
├─────────────────────────────────────────┤
│                                         │
│  Action: Delete file                    │
│  Target: /home/user/documents/report.pdf│
│  Risk:  File deletion cannot be undone  │
│                                         │
│  Requested by: n8n (JARVIS Agent)       │
│  Time: 2026-06-08 14:32:05              │
│                                         │
│  [ ❌ Deny ]              [ ✅ Allow ]  │
│                                         │
│  ☑️ Remember my choice for 5 minutes   │
└─────────────────────────────────────────┘
```

**Safety Policy:**
- Deny-by-default: No response = deny
- Audit log: Every request logged with timestamp, action, result
- Timeout: 60 seconds auto-deny
- Whitelist mode: User can pre-approve certain action types
- No covert monitoring: Screen recording only when explicitly requested
- No credential access: Passwords, tokens never accessible to automation
- No network exfiltration: Only localhost communication

### 5.6 Bridge Protocol (WebSocket)

**Connection:** `ws://localhost:8765/jarvis-bridge`

**Authentication:** Shared secret (`JARVIS_BRIDGE_SECRET` env var), validated on connection.

**Message Format:**
```json
{
  "type": "command|response|event|ping|pong",
  "payload": {},
  "timestamp": "ISO 8601",
  "signature": "HMAC-SHA256"
}
```

**Command Types:**

| Command | Params | Confirmation | Description |
|---------|--------|-------------|-------------|
| `screenshot` | `monitor` (optional) | No | Capture screenshot |
| `screen_record_start` | `duration_max` | Yes | Start screen recording |
| `screen_record_stop` | — | No | Stop recording |
| `browser_open` | `url` | No | Open Chrome |
| `browser_navigate` | `url` | No | Navigate to URL |
| `browser_close` | — | No | Close browser |
| `app_open` | `app_name` | No | Open application |
| `app_close` | `app_name` | No | Close application |
| `file_list` | `path` | No | List directory |
| `file_move` | `src`, `dst` | Yes | Move file |
| `file_delete` | `path` | Yes | Delete file |
| `shell_exec` | `command` | Yes | Run shell command |
| `system_info` | — | No | Get system info |
| `audio_play` | `text` | No | TTS output |

---

## 6. Local Device Automation Scripts

### 6.1 Module: Browser Control (`automation/browser.py`)

```python
class BrowserController:
    """Control Chrome browser via Playwright."""
    
    async def open(self, url: str = None) -> dict:
        """Open Chrome. Optionally navigate to URL."""
        
    async def navigate(self, url: str) -> dict:
        """Navigate to URL in existing browser."""
        
    async def get_page_info(self) -> dict:
        """Get page title, URL, meta description."""
        
    async def screenshot(self) -> dict:
        """Capture browser screenshot as base64."""
        
    async def close(self) -> dict:
        """Close browser."""
        
    async def scroll(self, direction: str, amount: int) -> dict:
        """Scroll page."""
```

### 6.2 Module: Application Control (`automation/apps.py`)

```python
class AppController:
    """Open and close applications."""
    
    async def open(self, app_name: str) -> dict:
        """Open an application by name."""
        
    async def close(self, app_name: str) -> dict:
        """Close an application."""
        
    async def list_running(self) -> dict:
        """List running applications."""
```

### 6.3 Module: File Operations (`automation/files.py`)

```python
class FileController:
    """File operations with safety constraints."""
    
    RISKY_PATTERNS = [
        r'^/',           # System root
        r'\.ssh',       # SSH keys
        r'\.gnupg',     # GPG keys
        r'\.config',    # App configs (may contain tokens)
        r'\.env',       # Environment files
        r'password',     # Password files
        r'token',        # Token files
    ]
    
    async def list_dir(self, path: str) -> dict:
        """List directory contents. Safe — no confirmation."""
        
    async def read_file(self, path: str, max_bytes: int = 100000) -> dict:
        """Read file contents. Requires confirmation for sensitive paths."""
        
    async def move(self, src: str, dst: str) -> dict:
        """Move file. Requires confirmation."""
        
    async def delete(self, path: str) -> dict:
        """Delete file. Requires confirmation."""
```

### 6.4 Module: Screen Capture (`automation/screen.py`)

```python
class ScreenController:
    """Screenshot and screen recording."""
    
    async def screenshot(self, monitor: int = 0) -> dict:
        """Capture screenshot as base64 PNG."""
        
    async def record_start(self, duration_max: int = 60) -> dict:
        """Start screen recording. Requires confirmation."""
        
    async def record_stop(self) -> dict:
        """Stop recording and return video path."""
```

### 6.5 Module: Shell Execution (`automation/shell.py`)

```python
class ShellController:
    """Shell command execution with deny-by-default policy."""
    
    BLOCKED_COMMANDS = [
        'rm -rf /', 'mkfs', 'dd if=', '>:', '> :',
        'curl.*\|.*bash', 'wget.*\|.*sh',
        'nc -l', 'ncat -l', 'netcat',
        'password', 'token', 'secret',
    ]
    
    ALLOWED_COMMANDS = [
        'ls', 'pwd', 'echo', 'cat', 'head', 'tail',
        'ps', 'top', 'df', 'du', 'free', 'uptime',
        'mkdir', 'touch', 'cp', 'mv', 'find', 'grep',
        'git status', 'git log', 'git diff',
        'ping', 'curl -I', 'nslookup', 'dig',
    ]
    
    async def execute(self, command: str, timeout: int = 30) -> dict:
        """Execute shell command. Requires confirmation."""
```

### 6.6 Safety Audit Log

All actions are logged to `~/.jarvis/audit.log`:

```json
{"timestamp":"2026-06-08T14:32:05Z","action":"file_delete","params":{"path":"/tmp/old.txt"},"confirmed":true,"result":"success","duration_ms":45}
{"timestamp":"2026-06-08T14:33:12Z","action":"shell_exec","params":{"command":"ls -la"},"confirmed":true,"result":"success","duration_ms":120}
```

---

## 7. Complete Workflow Architecture

### 7.1 Main Workflow (Entry Orchestrator)

```
┌─────────────────────────────────────────────────────────────┐
│                    MAIN WORKFLOW                             │
│                    ~15 nodes                                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  [Telegram Trigger] ──┐                                      │
│  [Website Webhook]  ──┼──► [Request Normalizer]            │
│  [Local Webhook]    ──┘                                      │
│                           │                                  │
│                           ▼                                  │
│                     [Auth & Rate Limit Gate]                │
│                           │                                  │
│                           ▼                                  │
│                     [Intent Router] ──► LLM classification  │
│                           │                                  │
│              ┌────────────┼────────────┐                    │
│              │            │            │                     │
│              ▼            ▼            ▼                     │
│         [General    [Service      [Local Device]            │
│          Chat]       Router]       [Bridge]                  │
│              │            │            │                     │
│              │     ┌─────┴─────┐      │                     │
│              │     │  Service  │      │                     │
│              │     │ Sub-Workflows   │                     │
│              │     └─────┬─────┘      │                     │
│              │           │            │                     │
│              └───────────┴────────────┘                     │
│                           │                                  │
│                           ▼                                  │
│                     [Response Builder]                      │
│                           │                                  │
│              ┌────────────┼────────────┐                    │
│              ▼            ▼            ▼                     │
│         [Telegram   [Website    [Local                      │
│          Send]       Send]      Send]                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 7.2 Sub-Workflow Inventory

| # | File | Purpose | Nodes (est.) |
|---|------|---------|-------------|
| 1 | `01-entry-points.json` | Triggers + normalizer | 5 |
| 2 | `02-auth-gate.json` | Auth + rate limiting | 4 |
| 3 | `03-intent-router.json` | LLM intent classification | 3 |
| 4 | `04-general-chat.json` | General conversation handler | 3 |
| 5 | `05-youtube-agent.json` | YouTube operations | 4 |
| 6 | `06-drive-agent.json` | Google Drive operations | 4 |
| 7 | `07-gmail-agent.json` | Gmail operations | 4 |
| 8 | `08-calendar-agent.json` | Calendar operations | 4 |
| 9 | `09-translate-agent.json` | Translation operations | 3 |
| 10 | `10-contacts-agent.json` | Contacts operations | 4 |
| 11 | `11-docs-agent.json` | Docs operations | 4 |
| 12 | `12-slides-agent.json` | Slides operations | 4 |
| 13 | `13-tasks-agent.json` | Tasks operations | 4 |
| 14 | `14-sheets-agent.json` | Sheets operations | 4 |
| 15 | `15-local-bridge.json` | Local device command bridge | 5 |
| 16 | `16-response.json` | Response formatting + sending | 6 |
| 17 | `17-memory.json` | STM/LTM persistence | 8 |
| | **TOTAL** | | **~77 nodes across 17 sub-workflows** |

### 7.3 Node Count Comparison

| Metric | JARVIS 3.0 | JARVIS 4.0 |
|--------|-----------|-----------|
| Total Nodes | 73 (monolith) | ~77 (distributed) |
| Workflow Files | 1 | 17 |
| Max nodes per workflow | 73 | ~8 |
| Avg nodes per workflow | 73 | ~4.5 |
| Tool connections | 0 | 10+ |
| Google services | 0 | 10 |
| Entry points | 1 | 3 |
| Local device control | No | Yes |
| Safety confirmation | No | Yes |

---

## 8. Environment Variables

### 8.1 Required

| Variable | Description |
|----------|-------------|
| `TELEGRAM_BOT_TOKEN` | Telegram bot token from BotFather |
| `GROQ_API_KEY` | Groq API key for LLM + Whisper |
| `GOOGLE_CLIENT_ID` | Google OAuth client ID |
| `GOOGLE_CLIENT_SECRET` | Google OAuth client secret |
| `GOOGLE_REFRESH_TOKEN` | Google OAuth refresh token |
| `OWNER_USER_ID` | Single allowed Telegram user ID |
| `JARVIS_BRIDGE_SECRET` | Shared secret for laptop bridge |

### 8.2 Optional

| Variable | Default | Description |
|----------|---------|-------------|
| `AUTH_MODE` | `protected` | `open` or `protected` |
| `RATE_LIMIT_PER_MINUTE` | `30` | Max requests per minute |
| `BRIDGE_PORT` | `8765` | WebSocket port for laptop bridge |
| `MEMORY_ENABLED` | `true` | Enable memory persistence |
| `LOG_LEVEL` | `info` | Logging verbosity |

---

## 9. Database Schema (Simplified Single-User)

```sql
-- Single-user memory store
CREATE TABLE IF NOT EXISTS jarvis_memory (
  id SERIAL PRIMARY KEY,
  category TEXT NOT NULL CHECK (category IN ('PROFILE','PREFERENCES','GOALS','TASKS','FACTS','CONTEXT','INSTRUCTIONS')),
  key TEXT NOT NULL,
  value JSONB NOT NULL DEFAULT '{}',
  confidence FLOAT DEFAULT 0.5 CHECK (confidence >= 0 AND confidence <= 1),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(category, key)
);

-- Short-term memory (single row, single user)
CREATE TABLE IF NOT EXISTS jarvis_stm (
  id SERIAL PRIMARY KEY,
  messages JSONB DEFAULT '[]',
  rolling_summary TEXT DEFAULT '',
  active_tasks JSONB DEFAULT '{}',
  open_loops JSONB DEFAULT '[]',
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Execution logs
CREATE TABLE IF NOT EXISTS jarvis_logs (
  id SERIAL PRIMARY KEY,
  session_key TEXT,
  source TEXT, -- telegram, website, local
  intent TEXT,
  input_text TEXT,
  response_text TEXT,
  execution_ms INT,
  error TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Device command log (audit trail)
CREATE TABLE IF NOT EXISTS jarvis_device_commands (
  id SERIAL PRIMARY KEY,
  command_id TEXT UNIQUE,
  action TEXT NOT NULL,
  params JSONB,
  confirmed BOOLEAN,
  result JSONB,
  execution_ms INT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Initialize STM
INSERT INTO jarvis_stm (messages, rolling_summary) VALUES ('[]', '') ON CONFLICT DO NOTHING;
```

---

## 10. Security Considerations

### 10.1 Authentication
- Single-owner model: only `OWNER_USER_ID` can interact
- Webhook secret validation on all entry points
- Bridge uses HMAC-signed messages with shared secret

### 10.2 Authorization
- Google OAuth scope-limited tokens
- Local device: deny-by-default for all risky operations
- Shell: command whitelist + pattern blacklist

### 10.3 Data Protection
- No credentials in logs
- Audit log for all device actions
- No network exfiltration from local bridge
- In-memory rate limiting (no sensitive data persistence)

### 10.4 Input Validation
- All inputs sanitized (length limits, encoding normalization)
- Prompt injection detection (pattern-based)
- URL validation strict allowlist
- File path validation (no traversal)

---

## 11. Implementation Priority

### Phase 1: Foundation (Week 1)
- [x] Audit JARVIS 3.0
- [x] Write design specification
- [ ] Build main workflow skeleton
- [ ] Implement entry points + normalizer
- [ ] Implement auth gate (simplified)

### Phase 2: Core Intelligence (Week 1-2)
- [ ] Build intent router
- [ ] Create tool registry
- [ ] Implement general chat handler
- [ ] Set up Groq LLM integration

### Phase 3: Google Service Agents (Week 2-3)
- [ ] Build YouTube agent
- [ ] Build Drive agent
- [ ] Build Gmail agent
- [ ] Build Calendar agent
- [ ] Build remaining agents (Translate, Contacts, Docs, Slides, Tasks, Sheets)

### Phase 4: Local Device Control (Week 3-4)
- [ ] Scaffold Python desktop app
- [ ] Implement audio visualization
- [ ] Build WebSocket bridge
- [ ] Implement automation modules (browser, apps, files, screen, shell)
- [ ] Build safety confirmation system

### Phase 5: Memory & Polish (Week 4)
- [ ] Implement simplified memory system
- [ ] Add multilingual support (English + Arabic)
- [ ] RTL layout support
- [ ] End-to-end testing
- [ ] Documentation

---

## 12. Files Delivered

| File | Description |
|------|-------------|
| `docs/audit-report.md` | Full audit with error list and fix list |
| `docs/design.md` | This document — complete redesign spec |
| `workflow/jarvis-4-0-main.json` | Redesigned main workflow (entry orchestrator) |
| `workflow/tool-registry.json` | Operation registry for all Google services |
| `python-app/main.py` | Desktop app entry point |
| `python-app/bridge_server.py` | WebSocket bridge server |
| `python-app/ui/` | UI modules (main window, audio viz, safety dialog) |
| `python-app/automation/` | Device automation modules |
| `python-app/locales/` | i18n files (en, ar) |
