## 1. SYSTEM PRINCIPLES

- Single Responsibility per layer
- No cross-layer duplication
- Structure reflects execution flow
- Capabilities are the only action layer

## 2. ROOT STRUCTURE

jarvis/
├── app/
├── config/
├── src/
│   ├── core/
│   ├── capabilities/
│   ├── interfaces/
│   ├── services/
│   ├── models/
│   └── memory/
├── STRUCTURE.md
├── README.md
└── TASKS.md

## 3. LAYER DEFINITIONS (CRITICAL)

### core/

Purpose: system orchestration and execution control

Owns:
- runtime loop
- decision system
- context handling
- safety enforcement

Must NOT contain:
- tool implementations
- external APIs
- UI logic

### capabilities/

Purpose: ALL executable actions in the system

Owns:
- system control
- file operations
- web automation
- screen/vision/audio actions

Must NOT contain:
- decision logic
- model selection

### interfaces/

Purpose: user interaction layer

Owns:
- CLI / GUI / Web UI

Must NOT contain:
- business logic
- tool execution

### services/

Purpose: external system connectors

Owns:
- Telegram
- Google APIs
- third-party integrations

Must NOT contain:
- core logic
- decision making

### models/

Purpose: model adapters only

Owns:
- LLM wrappers
- speech models
- vision models

Must NOT contain:
- routing logic
- tool logic

### memory/

Purpose: data storage and retrieval

Owns:
- short-term context
- long-term memory

Must NOT contain:
- execution logic

## 4. NAMING RULES

- no duplicate semantic names
- no vague folders (utils, misc)
- consistent naming across system
- clear distinction (web_ui vs web_automation)

## 5. CAPABILITY SYSTEM RULES

- ALL actions MUST exist inside capabilities/
- capabilities represent domains, not functions
- no logic outside capabilities performs actions

## 6. EXECUTION FLOW MAPPING

interfaces → core/runtime → core/decision → models → capabilities → memory

## 7. FORBIDDEN PATTERNS

- brain folder
- duplicate tool locations
- agents before stable runtime
- mixing UI with logic
- mixing models with decision

## 8. MIGRATION RULES (IMPORTANT)

- any old folder MUST be mapped or removed
- no legacy structure allowed
- no partial migration

## 9. VALIDATION CHECKLIST

- Can a new developer understand structure in <2 minutes?
- Does every folder have a single responsibility?
- Is any action outside capabilities? → FAIL
- Any duplication? → FAIL
