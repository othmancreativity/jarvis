# JARVIS 4.5 — AI Operating Assistant

A comprehensive, production-grade AI Operating Assistant that combines cloud-based LLM intelligence with local device automation through a multi-agent architecture.

## What's New in 4.5

### Multi-Agent Architecture
9 specialized agents communicating via a centralized message bus:
- **Planner** — Task decomposition and planning
- **Executor** — Tool execution and coordination
- **Browser** — Web automation via Playwright
- **Memory** — Multi-layer memory system (working, episodic, semantic, procedural)
- **Vision** — Screen analysis and OCR
- **Coding** — Code generation and syntax checking
- **Google** — Unified Google services (YouTube, Drive, Gmail, Calendar, Translate, Contacts, Docs, Sheets, Slides, Tasks)
- **Security** — Permission engine and audit logging
- **Scheduler** — Task scheduling and reminders

### Security Subsystem
- **Permission Engine** — Deny-by-default with 5 permission levels
- **Audit Logger** — Chain-hashed, tamper-resistant logging
- **Emergency Stop** — Global kill switch
- **Input Validation** — Path traversal prevention, shell injection blocking

### Memory Architecture
- **Working Memory** — LRU cache with TTL for current context
- **Episodic Memory** — Session history with outcomes
- **Semantic Memory** — Long-term facts and user preferences
- **Procedural Memory** — Learned workflows with success tracking

### Local Device Automation (25+ tools)
- **Browser** — Open, navigate, tabs, screenshot, download
- **Applications** — Open, close, restart, focus, list (cross-platform)
- **Files** — List, read, write, move, copy, delete, search, compress, extract
- **Screen** — Screenshot, recording, OCR
- **Shell** — Safe execution with pattern blocking
- **System** — Info, processes, monitoring

### WebSocket Bridge
- Bidirectional communication between n8n and local device
- Bearer token authentication
- Heartbeat mechanism
- Auto-reconnect support

## Architecture

```
User → Telegram / Website / Local
         ↓
    n8n Orchestrator
         ↓
    Intent Router → General Chat / Service Dispatcher / Local Bridge
                        ↓                    ↓                  ↓
                      LLM               Google Agents     Device Bridge
                        ↓                    ↓                  ↓
                 Response ←───────── Response ←────────── Response
```

## Quick Start

### Prerequisites
- Python 3.10+
- n8n instance (cloud or self-hosted)
- Telegram bot token
- Groq API key
- Google API key

### 1. Install Dependencies

```bash
cd python-app
pip install -r requirements.txt
playwright install chromium
```

### 2. Set Environment Variables

```bash
export TELEGRAM_BOT_TOKEN="your_telegram_bot_token"
export GROQ_API_KEY="your_groq_api_key"
export GOOGLE_API_KEY="your_google_api_key"
export JARVIS_BRIDGE_SECRET="your_secure_secret"
export OWNER_USER_ID="your_telegram_user_id"
```

### 3. Run the Desktop Companion

```bash
python main.py
```

### 4. Import Workflows into n8n

Import all JSON files from the `workflow/` directory into your n8n instance:

1. `jarvis-4-5-main.json` — Main orchestrator
2. `jarvis-intent-router.json` — Intent classification
3. `jarvis-general-chat.json` — General chat handler
4. `jarvis-service-dispatcher.json` — Routes to Google service agents
5. `jarvis-youtube-agent.json` — YouTube search
6. `jarvis-drive-agent.json` — Google Drive
7. `jarvis-gmail-agent.json` — Gmail
8. `jarvis-calendar-agent.json` — Google Calendar
9. `jarvis-translate-agent.json` — Translation
10. `jarvis-contacts-agent.json` — Google Contacts
11. `jarvis-docs-agent.json` — Google Docs
12. `jarvis-slides-agent.json` — Google Slides
13. `jarvis-tasks-agent.json` — Google Tasks
14. `jarvis-sheets-agent.json` — Google Sheets
15. `jarvis-local-bridge.json` — Local device bridge
16. `jarvis-response-sender.json` — Response delivery
17. `jarvis-memory-persist.json` — Memory persistence

### 5. Connect Workflows

In n8n, connect workflow executions:
- Main orchestrator → Intent Router (sub-workflow)
- Main orchestrator → General Chat (sub-workflow)
- Main orchestrator → Service Dispatcher (sub-workflow)
- Main orchestrator → Local Bridge (sub-workflow)
- Service Dispatcher → Individual service agents

## File Structure

```
jarvis-4.5/
├── python-app/
│   ├── main.py                    # PyQt6 desktop application
│   ├── bridge_server.py           # WebSocket bridge server
│   ├── requirements.txt           # Python dependencies
│   ├── core/
│   │   ├── __init__.py
│   │   ├── tool_registry.py       # 25+ tool definitions with schemas
│   │   ├── agent_runtime.py       # State machine with 11 states
│   │   └── message_bus.py         # Inter-agent communication
│   ├── security/
│   │   ├── __init__.py
│   │   ├── permissions.py         # Permission engine (5 levels)
│   │   ├── audit.py              # Chain-hashed audit logger
│   │   └── validator.py          # Input validation & sanitization
│   ├── memory/
│   │   ├── __init__.py
│   │   └── memory_system.py      # 4-layer memory architecture
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base_agent.py         # Abstract base for all agents
│   │   ├── planner_agent.py      # Task decomposition
│   │   ├── execution_agent.py    # Tool execution coordinator
│   │   ├── browser_agent.py      # Web automation
│   │   ├── memory_agent.py       # Memory operations
│   │   ├── vision_agent.py       # Screen analysis
│   │   ├── coding_agent.py       # Code generation
│   │   ├── google_agent.py       # Google services
│   │   ├── security_agent.py     # Security monitoring
│   │   └── scheduler_agent.py    # Task scheduling
│   ├── automation/
│   │   ├── __init__.py
│   │   ├── browser.py            # Full browser control (Playwright)
│   │   ├── apps.py               # Application lifecycle
│   │   ├── files.py              # File operations with safety
│   │   ├── screen.py             # Screenshot, recording, OCR
│   │   ├── shell.py              # Safe shell execution
│   │   └── system_info.py        # System monitoring
│   ├── ui/
│   │   └── (Qt UI components)
│   └── locales/
│       ├── en.json               # English translations
│       └── ar.json               # Arabic translations
├── workflow/
│   ├── jarvis-4-5-main.json
│   ├── jarvis-intent-router.json
│   ├── jarvis-general-chat.json
│   ├── jarvis-service-dispatcher.json
│   ├── jarvis-youtube-agent.json
│   ├── jarvis-drive-agent.json
│   ├── jarvis-gmail-agent.json
│   ├── jarvis-calendar-agent.json
│   ├── jarvis-translate-agent.json
│   ├── jarvis-contacts-agent.json
│   ├── jarvis-docs-agent.json
│   ├── jarvis-slides-agent.json
│   ├── jarvis-tasks-agent.json
│   ├── jarvis-sheets-agent.json
│   ├── jarvis-local-bridge.json
│   ├── jarvis-response-sender.json
│   ├── jarvis-memory-persist.json
│   └── tool-registry.json
├── docs/
│   ├── design.md                 # Architecture documentation
│   └── README.md
└── README.md
```

## Security Features

- **Deny-by-default** permission system
- **5 permission levels**: none, notify, confirm, whitelist, deny
- **Pattern-based blocking** for dangerous shell commands
- **Path traversal prevention** in all file operations
- **Protected path detection** (SSH keys, credentials, system dirs)
- **Chain-hashed audit logging** for tamper resistance
- **Emergency stop** button in desktop app
- **Rate limiting** (default: 30 req/min)
- **Owner-only access** for Telegram mode

## License

MIT

## Version

4.5.0
