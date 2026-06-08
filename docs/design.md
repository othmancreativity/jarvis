# JARVIS 4.5 — Design Document

## Overview

JARVIS 4.5 is a comprehensive AI Operating Assistant with a multi-layer architecture integrating cloud-based LLM intelligence with local device automation through a bidirectional bridge protocol.

## Architecture

```
                    ┌─────────────┐
                    │   Telegram  │
                    └──────┬──────┘
                           │
                    ┌──────┴──────┐
                    │   Website   │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
         ┌────┴──┐  ┌────┴────┐  ┌─────┴──┐
         │Main   │  │Website  │  │Local   │
         │Orche. │  │Webhook  │  │Webhook │
         └───┬───┘  └─────────┘  └────────┘
             │
        ┌────┴────┐
        │ Request │
        │Normalizer│
        └────┬────┘
             │
        ┌────┴────┐
        │  Auth   │
        │  Gate   │
        └────┬────┘
             │
        ┌────┴────┐
        │Rate     │
        │Limiter  │
        └────┬────┘
             │
        ┌────┴─────────┐
        │ Intent Router │
        └───┬─────┬────┘
            │     │
     ┌──────┘     └──────┐
     │                   │
┌────┴────┐       ┌─────┴────┐
│General  │       │ Service  │
│Chat     │       │Dispatcher│
│(LLM)    │       └────┬─────┘
└────┬────┘            │
     │            ┌────┼────┬────┬────┬────┬────┬────┬────┬────┐
     │            │    │    │    │    │    │    │    │    │
     │           You  Dri  Gma  Cal  Tra  Con  Doc  Sli  Tas  She
     │           Tube  ve   il   end  nsl  tac  s    des  ks   ets
     │
     │            ┌──────────┐
     │            │  Local   │
     └────────────┤  Device  │
                  │  Bridge  │
                  └────┬─────┘
                       │ ws://localhost:8765
                  ┌────┴──────────────────────────────────────────┐
                  │              Python Companion                   │
                  │  ┌──────────────────────────────────────┐     │
                  │  │         Agent Runtime                 │     │
                  │  │   Idle → Understanding → Planning     │     │
                  │  │   → Executing → Monitoring → Idle     │     │
                  │  └──────────────────────────────────────┘     │
                  │  ┌─────────┐  ┌─────────┐  ┌─────────┐       │
                  │  │planner  │  │executor │  │browser  │       │
                  │  ├─────────┤  ├─────────┤  ├─────────┤       │
                  │  │memory   │  │vision   │  │coding   │       │
                  │  ├─────────┤  ├─────────┤  ├─────────┤       │
                  │  │google   │  │security │  │scheduler│       │
                  │  └─────────┘  └─────────┘  └─────────┘       │
                  │  ┌──────────────────────────────────────┐     │
                  │  │         Security Engine               │     │
                  │  │  PermissionEngine + AuditLogger       │     │
                  │  └──────────────────────────────────────┘     │
                  │  ┌──────────────────────────────────────┐     │
                  │  │         Memory System                 │     │
                  │  │  Working | Episodic | Semantic        │     │
                  │  │  | Procedural                        │     │
                  │  └──────────────────────────────────────┘     │
                  │  ┌──────────────────────────────────────┐     │
                  │  │         Tool Registry (25+ tools)     │     │
                  │  └──────────────────────────────────────┘     │
                  └───────────────────────────────────────────────┘
```

## Multi-Agent Architecture

### Agents (9 total)

| Agent | ID | Capabilities | Description |
|-------|-----|-------------|-------------|
| Planner | `planner` | task_decomposition, plan_validation, step_ordering | Decomposes tasks into executable steps |
| Executor | `executor` | tool_execution, retry_management, parallel_execution | Coordinates tool execution |
| Browser | `browser` | web_navigation, page_extraction, web_search, screenshot | Web automation tasks |
| Memory | `memory` | fact_storage, episode_recording, procedure_learning | Memory management |
| Vision | `vision` | screenshot_analysis, ocr, element_detection | Screen analysis |
| Coding | `coding` | code_generation, code_review, syntax_check | Code assistance |
| Google | `google` | youtube_search, drive_list, gmail_search, calendar_list, translate, contacts_list, docs_create, sheets_read, sheets_write, tasks_list, slides_create | Google services |
| Security | `security` | threat_detection, policy_enforcement, emergency_response | Security monitoring |
| Scheduler | `scheduler` | schedule_task, cancel_task, list_tasks | Task scheduling |

## Agent Runtime States

```
IDLE ←──────────┐
  │               │
  ↓ USER_INPUT    │
UNDERSTANDING     │
  │               │
  ↓ INTENT_CLASSIFIED
PLANNING          │
  │               │
  ↓ PLAN_CREATED  │
EXECUTING ←───────┤
  │       ↑ TOOL_RESULT
  ↓ EXECUTION_COMPLETE
MONITORING        │
  │               │
  ↓ TIMEOUT       │
  (back to IDLE)  │

ERROR_RECOVERY ←──┘ (on any error)
  │
  ↓ EMERGENCY_TRIGGERED
EMERGENCY_STOP
  │
  ↓ SHUTDOWN_REQUESTED
SHUTDOWN (terminal)
```

## Memory Architecture

### Four Layers

1. **Working Memory** — LRU cache with TTL for current context (5 min default)
2. **Episodic Memory** — SQLite-backed session history with actions and results
3. **Semantic Memory** — Long-term facts, user preferences, and profile data
4. **Procedural Memory** — Learned workflows and reusable patterns with success tracking

### Data Flow
```
User Input → Working Memory → LLM Context
    ↓
Tool Result → Episodic Memory (session log)
    ↓
Fact Extraction → Semantic Memory (facts, preferences)
    ↓
Repeated Pattern → Procedural Memory (learned workflow)
```

## Security Architecture

### Permission Engine
- Deny by default
- Five permission levels: `none`, `notify`, `confirm`, `whitelist`, `deny`
- Emergency stop (global kill switch)
- Whitelist manager with configurable TTL

### Audit Logger
- Chain-hashed log entries for tamper resistance
- Log rotation by size and date
- Compression of old logs
- Auto-cleanup after 30 days
- All operations logged with: timestamp, event_type, action, target, decision

### Input Validation
- Path traversal prevention
- Protected path blocking (system dirs, SSH keys, credentials)
- Shell command pattern blocking (dangerous patterns denied)
- URL scheme validation
- Size limits on all inputs and outputs

## Local Device Operations

### Browser (playwright)
- open, navigate, close, new_tab, close_tab, list_tabs, switch_tab
- screenshot, scroll, download, cookie management
- Session persistence to disk

### Applications
- open, close, restart, focus
- list_running, is_running
- Cross-platform: macOS, Linux, Windows

### Files
- list, read, write, move, copy, delete, search
- compress (zip, tar, tar.gz), extract
- Protected path detection
- Size limits and truncation

### Screen
- screenshot (monitor/region), record_start/stop
- OCR (tesseract-based)
- Color sampling, mouse position

### Shell
- execute with timeout, cwd support
- Pattern-based command blocking (deny-by-default for dangerous patterns)
- Read-only command whitelist (auto-allow safe commands)
- Sandbox mode (dry-run)
- Output sanitization and truncation

### System
- info (CPU, memory, disk, battery)
- processes (list, filter, sort)
- kill_process (by PID or name)

## Bridge Protocol

### WebSocket
- Endpoint: `ws://localhost:8765/jarvis-bridge`
- Auth: Bearer token via `JARVIS_BRIDGE_SECRET` env var
- Heartbeat: ping/pong every 30 seconds
- Max connections: 5

### Message Types
```json
{"type": "command", "payload": {"command_id": "...", "action": "...", "params": {}, "requires_confirmation": false}}
{"type": "response", "payload": {"command_id": "...", "status": "success", "result": {}, "stdout": "", "stderr": ""}}
{"type": "ping"}
{"type": "pong", "timestamp": 1234567890}
{"type": "heartbeat"}
{"type": "auth", "payload": {"token": "..."}}
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `TELEGRAM_BOT_TOKEN` | Yes | Telegram bot token |
| `GROQ_API_KEY` | Yes | Groq API key |
| `GOOGLE_API_KEY` | Yes | Google API key |
| `JARVIS_BRIDGE_SECRET` | Yes | Bridge auth secret |
| `OWNER_USER_ID` | Optional | Telegram owner user ID |
| `TELEGRAM_WEBHOOK_SECRET` | Optional | Webhook secret |
| `RATE_LIMIT_PER_MINUTE` | Optional | Rate limit (default: 30) |
| `BRIDGE_PORT` | Optional | Bridge port (default: 8765) |
| `JARVIS_MODEL` | Optional | LLM model name |
| `JARVIS_LANG` | Optional | UI language (en/ar) |

## Version History

- 4.0 → 4.5: Complete overhaul — multi-agent architecture, security subsystem, memory system, WebSocket bridge, full device automation
