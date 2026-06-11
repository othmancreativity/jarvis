# JARVIS 4.5 — AI Operating Assistant

A comprehensive, production-grade AI Operating Assistant that combines cloud-based LLM intelligence with local device automation through a multi-agent architecture.

## What's New in 4.5

### Multi-Agent Architecture
9 specialized agents communicating via a centralized message bus:
- **Planner** — Task decomposition and planning
- **Executor** — Tool execution and coordination
- **Browser** — Web automation via Playwright
- **Memory** — 6-layer memory system (working, episodic, semantic, procedural, preference, project)
- **Vision** — Screen analysis and OCR
- **Coding** — Code generation and syntax checking
- **Google** — Full Google services with real API calls (YouTube, Drive, Gmail, Calendar, Translate, Contacts, Docs, Sheets, Slides, Tasks)
- **Security** — Permission engine and audit logging
- **Scheduler** — Task scheduling and reminders with background execution

### Central Orchestrator (JarvisCore)
- Unified intent classification and routing
- Continuous agent loop with state machine
- Session management with automatic context trimming
- Multi-step plan execution with error recovery

### Security Subsystem
- **Permission Engine** — Deny-by-default with 5 permission levels
- **Audit Logger** — Chain-hashed, tamper-resistant logging
- **Emergency Stop** — Global kill switch with auto-threshold
- **Input Validation** — Path traversal prevention, shell injection blocking

### Memory Architecture
- **Working Memory** — LRU cache with TTL for current context
- **Episodic Memory** — Session history with outcomes
- **Semantic Memory** — Long-term facts and user preferences
- **Procedural Memory** — Learned workflows with success tracking
- **Preference Memory** — User preference learning
- **Project Memory** — Project-specific context retention

### Wake Word System
- **Keyboard shortcut** — Ctrl+Shift+J activation
- **UDP trigger** — Remote activation via port 19876
- **Text trigger** — Detects "Jarvis" in messages
- **Optional voice** — Porcupine integration for voice wake word

### Local Device Automation (30+ tools)
- **Browser** — Open, navigate, tabs, screenshot, download, scroll
- **Applications** — Open, close, restart, focus, list (cross-platform)
- **Files** — List, read, write, move, copy, delete, search, compress, extract
- **Screen** — Screenshot, recording, OCR, color sampling
- **Shell** — Safe execution with pattern blocking
- **System** — Info, processes, monitoring, kill

### Desktop UI
- PyQt6 interface with dark theme
- Real-time audio visualization
- Multilingual support (EN + AR with RTL)
- Safety confirmation dialogs with auto-timeout
- System tray integration
- Emergency stop button
- Status panel with live system monitoring

## Architecture

```
User Input (Text / Voice / Hotkey / UDP)
    ↓
JarvisCore (Central Orchestrator)
    ↓
Intent Classifier → Agent Router
    ↓
Agent(s) via Message Bus
    ↓
Automation Layer / Google API / LLM
    ↓
Response to User
```

## Quick Start

### Prerequisites
- Python 3.10+
- n8n instance (optional, for workflow integration)

### 1. Install

```bash
cd python-app
pip install -r requirements.txt
# Or install as package:
pip install -e .
playwright install chromium
```

### 2. Configure

```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Run

```bash
python main.py
```

## Configuration

Configuration priority: Environment variables > `.env` file > `~/.jarvis/config.yaml` > defaults

| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | Yes* | Groq API key for LLM |
| `GOOGLE_API_KEY` | Yes* | Google API key |
| `GOOGLE_ACCESS_TOKEN` | Optional | Google OAuth token |
| `TELEGRAM_BOT_TOKEN` | Optional | Telegram bot token |
| `JARVIS_BRIDGE_SECRET` | Yes | Bridge auth secret |
| `JARVIS_LANG` | Optional | UI language (en/ar) |

*Required for full functionality. JARVIS works in limited mode without them.

## File Structure

```
jarvis-4.5/
├── python-app/
│   ├── main.py                    # PyQt6 desktop application
│   ├── bridge_server.py           # WebSocket bridge server
│   ├── pyproject.toml             # Package config
│   ├── requirements.txt           # Dependencies
│   ├── .env.example               # Environment template
│   ├── core/
│   │   ├── __init__.py
│   │   ├── jarvis_core.py         # Central orchestrator (NEW)
│   │   ├── agent_runtime.py       # State machine
│   │   └── tool_registry.py       # 30+ tool definitions
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base_agent.py          # Abstract base
│   │   ├── message_bus.py         # Inter-agent communication
│   │   ├── planner_agent.py
│   │   ├── execution_agent.py
│   │   ├── browser_agent.py
│   │   ├── memory_agent.py
│   │   ├── vision_agent.py
│   │   ├── coding_agent.py
│   │   ├── google_agent.py        # Full API implementation (NEW)
│   │   ├── security_agent.py
│   │   └── scheduler_agent.py
│   ├── automation/
│   │   ├── __init__.py
│   │   ├── browser.py             # Playwright controller
│   │   ├── apps.py                # App lifecycle
│   │   ├── files.py               # File operations
│   │   ├── screen.py              # Screenshot/OCR
│   │   ├── shell.py               # Safe shell
│   │   └── system_info.py         # System monitoring
│   ├── security/
│   │   ├── __init__.py
│   │   ├── permissions.py         # Permission engine
│   │   ├── audit.py               # Audit logger
│   │   └── validator.py           # Input validation
│   ├── memory/
│   │   ├── __init__.py
│   │   └── memory_system.py       # 6-layer memory
│   ├── wake_word/
│   │   └── __init__.py            # Wake word system (NEW)
│   ├── config/
│   │   └── __init__.py            # Configuration manager (NEW)
│   ├── ui/
│   │   └── __init__.py
│   ├── locales/
│   │   ├── en.json                # English
│   │   └── ar.json                # Arabic
│   └── tests/                     # Test suite (NEW)
│       ├── test_security.py
│       ├── test_memory.py
│       ├── test_tool_registry.py
│       └── test_automation.py
├── workflow/                      # n8n workflow JSONs
└── docs/
    └── COMPREHENSIVE_AUDIT_JARVIS_4.5.md
```

## Testing

```bash
cd python-app
pytest tests/ -v
```

## Security

- Deny-by-default permission system
- 5 permission levels: none, notify, confirm, whitelist, deny
- Pattern-based blocking for dangerous commands
- Path traversal prevention
- Chain-hashed audit logging
- Emergency stop with auto-threshold

## License

MIT

## Version

4.5.0
