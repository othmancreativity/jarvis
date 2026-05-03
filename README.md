# JARVIS

**Local-First AI Assistant for Desktop Control and Automation**

JARVIS is a production-grade AI assistant that runs entirely on your local machine. It understands natural language in English and Arabic, then acts on your system — opening applications, managing files, automating workflows, and integrating with external services — without sending your data to the cloud.

**Version: 3.2.0** — Hardened architecture with passive SLA, strict scheduler role, dual-mode cancellation, and capability scope enforcement.

---

## Introduction

Modern AI assistants are either cloud-based (sacrificing privacy) or limited to text chat (sacrificing usefulness). JARVIS exists to bridge that gap: a local AI that can reason, plan, and execute real actions on your computer.

It runs on modest hardware — an NVIDIA RTX 3050 with 6GB VRAM is enough to get started. No API keys required for core functionality. No subscription. No data leaving your machine.

JARVIS is built for people who want their computer to understand them, not the other way around.

---

## Core Capabilities

### System Control

JARVIS can interact with your operating system directly. Launch applications, monitor system resources, access the clipboard, and send desktop notifications — all through natural language.

> "Open Visual Studio Code" → JARVIS finds and launches the application.  
> "What's my CPU usage?" → JARVIS returns live system metrics.

### File Operations

Read, write, organize, and manage files across your system with intelligent path validation and safety checks built in.

> "List all PDFs in my Downloads folder" → JARVIS returns a filtered listing.  
> "Move all screenshots to a new folder called 'Screenshots'" → JARVIS organizes them automatically.

### Web Automation

JARVIS can control a browser to navigate websites, extract information, fill forms, and take screenshots — all autonomously.

> "Open Chrome and search for the latest AI news" → JARVIS navigates, searches, and returns results.

### Voice Interaction

Speak to JARVIS and hear its responses. Built-in speech-to-text and text-to-speech pipelines support both English and Arabic.

> "Jarvis, what's on my calendar today?" → Spoken query, spoken response.

### Vision and Image Understanding

JARVIS can analyze images, screenshots, and visual content. It can also generate images from text descriptions.

> "What's in this screenshot?" → JARVIS describes the visual content.

### External Integrations

Connect to the services you already use. JARVIS integrates with Telegram for remote access, and Google APIs for Calendar, Gmail, and Drive — all as optional modules you enable when ready.

> "Send a Telegram message to my team" → JARVIS delivers it through your bot.  
> "What meetings do I have tomorrow?" → JARVIS reads your Google Calendar.

---

## How JARVIS Thinks

Every interaction follows a clear, auditable, and controlled process:

1. **Observe** — JARVIS gathers your input, recent conversation history, and relevant context from memory.
2. **Decide** — It determines your intent, computes task priority, selects the best approach, and identifies any actions needed.
3. **Schedule** — Tasks are placed in the execution queue by the scheduler (placement only; no decisions, no priority changes).
4. **Execute** — Actions run through hardened sandbox isolation with capability scope validation before execution.
5. **Evaluate** — It verifies the result, and if something went wrong, the state machine controls recovery.

This cycle is deterministic (in deterministic mode) and fully logged. You can always see what JARVIS decided, why it decided it, and what happened next.

---

## Architecture Overview

JARVIS is built on a modular, layered architecture designed for reliability, control, and safety:

- **State Machine Core** — Every action flows through a controlled execution pipeline. Single controller authority (StateMachine ONLY). No shortcuts, no bypass paths, no uncontrolled behavior. All state transitions enforced.
- **Execution Engine** — Executor ONLY. Accepts tasks from the state machine, executes them, returns results, confirms termination. No independent decisions, routing, retries, or mode changes.
- **Scheduler** — Task placement and queue management ONLY. Priority is computed in the DECIDING state, not by the scheduler.
- **Capability System** — All actions live in isolated, sandboxed modules with defined scope boundaries. CapabilityRuntime is internal-only. RuntimeValidator enforces scope before execution, blocking violations immediately.
- **Hardened Sandbox** — System-level isolation: process isolation, privilege drop, filesystem allowlists, network deny-by-default, execution timeouts, dual-mode cancellation (soft SIGTERM → hard SIGKILL → termination confirmed).
- **SLA Events (Passive)** — Global performance targets: fast=100ms, medium=500ms, heavy=5000ms. SLAEnforcer emits events ONLY; StateMachine decides whether to cancel, fallback, retry, or ignore.
- **Execution Mode Enforcement** — `deterministic` mode: strict ordering, no parallelism, fixed retry limits. `performance` mode: relaxed ordering, bounded parallelism with deadlock/starvation safeguards, adaptive retry limits.
- **Local-First Design** — Every core component runs on your machine. External services are optional and must be explicitly enabled.
- **Separation of Concerns** — Reasoning is separated from execution. Decision-making is separated from action. This makes the system debuggable, testable, and trustworthy.

The result is an AI assistant you can inspect, control, and extend — not a black box.

---

## Execution Modes

JARVIS offers two execution modes that control how the runtime processes tasks:

| Mode | Behavior | Best For |
|------|----------|----------|
| **Deterministic** | Strict ordering, no parallelism, fixed retry limits. Every execution is reproducible. | Debugging, testing, high-reliability environments. |
| **Performance** | Relaxed ordering, bounded parallelism (only if no shared resource conflict), adaptive retry with limits. Optimized for throughput. | Daily use, multi-task workflows. |

In addition, JARVIS offers three safety modes that control user confirmation:

| Mode | Behavior | Best For |
|------|----------|----------|
| **SAFE** | Every action requires your explicit confirmation before execution. | First-time users, testing new capabilities, high-risk environments. |
| **BALANCED** | Low-risk actions execute automatically. Medium-risk actions require confirmation. High-risk actions are blocked unless you explicitly approve them. | Daily use. The default mode. |
| **UNRESTRICTED** | All actions execute automatically. Schema and path validation still apply — JARVIS will never execute structurally invalid commands. | Trusted environments, automated workflows, advanced users. |

Execution mode (`deterministic`/`performance`) is set at startup and requires a restart to change. Safety mode (`SAFE`/`BALANCED`/`UNRESTRICTED`) can be switched at any time using the `/mode` command in the chat interface.

---

## Performance & Hardware Awareness

JARVIS is designed to run on real hardware, not idealized server environments:

- **GPU-Aware Model Selection** — JARVIS monitors available VRAM in real time and selects models that fit your hardware. It automatically downgrades when resources are constrained.
- **One Model at a Time** — Models are loaded and unloaded as needed, maximizing the use of limited VRAM. Heavy tasks use powerful models; simple tasks use lightweight ones.
- **Efficient Execution** — Simple requests are resolved through fast-path rules without calling a model at all. Complex requests get the full reasoning pipeline.
- **SLA Events** — Global performance targets: fast=100ms, medium=500ms, heavy=5000ms. SLAEnforcer emits events on threshold breach; StateMachine decides whether to cancel, fallback, retry, or ignore. No autonomous action.
- **Dual-Mode Cancellation** — When a task is cancelled: soft kill (SIGTERM, 2s grace period) → hard kill (SIGKILL) → execution confirms termination → cleanup. No orphan processes.
- **Two Execution Modes** — `deterministic` mode (strict ordering, no parallelism, reproducible) and `performance` mode (relaxed ordering, bounded parallelism with deadlock/starvation safeguards, optimized throughput).

Target hardware: NVIDIA RTX 3050 (6GB VRAM), 16GB RAM, Intel Core i5 12th Gen. JARVIS works on this configuration and scales upward from there.

---

## Safety Philosophy

JARVIS is built with a simple principle: **trust must be earned, and control must always remain with the user.**

- **Structured Validation** — Every action is validated against strict schemas before execution. Invalid arguments are rejected before they can cause harm.
- **Risk-Aware Execution** — Actions are classified by risk level. Destructive operations require explicit approval. Path traversal, system-level commands, and irreversible actions are handled with extra scrutiny.
- **Hardened Sandbox** — All capabilities execute in isolated sandboxes: process isolation, privilege drop, filesystem allowlists, network deny-by-default, execution timeouts, and dual-mode cancellation (SIGTERM → 2s grace → SIGKILL → termination confirmed).
- **Audit Trail** — Every action JARVIS takes is logged with full context: what it did, why it did it, and what the result was. Nothing happens in the dark.
- **No Prompt-Based Safety** — Safety rules are enforced by the system itself, not by asking the model to behave. This means safety cannot be bypassed through clever prompting.
- **Capability Boundaries** — Each capability has a defined scope: allowed operations, forbidden operations, and resource limits. No capability can expand beyond its scope. RuntimeValidator enforces scope before execution and blocks violations immediately.
- **Single Controller** — StateMachine is the ONLY decision authority. SLAEnforcer, scheduler, sandbox, and executor all emit events or results — they never make autonomous decisions.

---

## Example Use Cases

**"Open Chrome and search for AI news"**  
JARVIS launches your browser, navigates to a search engine, performs the query, and returns the top results — all in one command.

**"Organize my Downloads folder"**  
JARVIS scans your downloads, groups files by type, creates labeled folders, and moves everything into place. You approve the plan before it executes.

**"Send a message via Telegram"**  
JARVIS composes and sends a message through your configured Telegram bot. It confirms delivery and logs the action.

**"What did I ask you yesterday?"**  
JARVIS retrieves your conversation history from memory and provides a summary of previous interactions.

**"Take a screenshot and tell me what's on screen"**  
JARVIS captures your display, analyzes the visual content, and describes what it sees.

**"Check my calendar for today"**  
JARVIS connects to your Google Calendar and lists your upcoming events in natural language.

---

## Extensibility

JARVIS is designed to grow with your needs:

- **Capability Modules** — Every action is a self-contained module. Adding a new capability means creating a module, registering it, and JARVIS can use it immediately.
- **Service Integrations** — External services (Telegram, Google APIs, custom tools) plug in through a clean interface. Enable what you need, ignore what you don't.
- **Multiple Interfaces** — CLI is the default. Web UI, Telegram bot, and custom interfaces can all connect to the same core engine.
- **Configurable Behavior** — Model selection weights, safety thresholds, execution modes, and memory settings are all configurable through YAML files.

The system is built so that new features don't require architectural changes — they require new modules.

---

## Limitations

JARVIS is powerful, but honest about its boundaries:

- **Hardware-Dependent** — JARVIS runs on your machine, which means its performance is bound by your hardware. Large models require significant VRAM. The target specification (RTX 3050, 6GB VRAM) is the minimum, not the ideal.
- **Setup Required** — Unlike cloud assistants, JARVIS requires local setup: installing dependencies, pulling models, and configuring settings. This is the trade-off for full local control.
- **Optional Features Need Configuration** — Voice, vision, web automation, Telegram, and Google integrations are all optional modules that require additional setup and, in some cases, API credentials.
- **Local-Only by Default** — JARVIS does not connect to the internet for core functions. This is intentional, but it means features requiring external access must be explicitly enabled.

---

## Vision

JARVIS is more than a chat interface. It is the foundation for a fully autonomous desktop AI layer:

- **Autonomous Workflows** — JARVIS will execute multi-step tasks without step-by-step guidance. You describe the outcome; it figures out the path.
- **Cross-Application Intelligence** — JARVIS will understand the relationships between your applications, files, and services, and act across them seamlessly.
- **Persistent Memory** — JARVIS will remember your preferences, habits, and context across sessions, becoming more useful over time.
- **Scalable Intelligence** — As hardware improves, JARVIS will take advantage of more powerful models and additional capabilities without requiring architectural changes.

The end goal is simple: a local AI that makes your computer work for you, not the other way around.

---

**JARVIS v3.2** — Local-first. Deterministic. Contract-enforced. Hardened sandbox. Passive SLA. Under your control.

---

## Spec Authority

- **Single source of truth:** `TASKS.md` is the authoritative execution plan (spec_version: v3.2).
- **Structure definition:** `STRUCTURE.md` defines the canonical directory layout and layer boundaries.
- **User-facing docs:** `README.md` describes behavior, capabilities, and usage.
- **Version discipline:** `project_version: 3.2.0`, `spec_version: v3.2`, `structure_version: 3.2`. Breaking changes require major version bump.
- All three files must align. Drift is a spec violation.

**Architecture Highlights (v3.2 Hardened):**
- Single controller: StateMachine is ONLY decision authority — no component may self-decide
- ExecutionEngine restricted to executor role ONLY — no decisions, routing, retries, mode changes
- Scheduler restricted to placement ONLY — priority computed in DECIDING state, not scheduler
- CapabilityRuntime is INTERNAL — RuntimeValidator enforces scope BEFORE execution
- Corrected flow: IDLE → DECIDING → SCHEDULING → EXECUTING → EVALUATING → COMPLETED
- Hardened sandbox: process isolation, privilege drop, filesystem allowlist, network deny-by-default
- Passive SLA: SLAEnforcer emits events ONLY — StateMachine decides cancel/fallback/retry/ignore
- Dual-mode cancellation: SIGTERM → 2s grace → SIGKILL → termination confirmed
- Execution mode enforcement: StateMachine validates mode on every transition
- Deterministic mode: strict/no-parallelism/fixed-retry; Performance mode: relaxed/bounded/adaptive-retry
- Concurrency mode-bound: parallelism ONLY if performance mode AND no shared_resource_conflict
- Capability scope violation blocks execution immediately, emits CapabilityViolationEvent
- Extended testing: scheduling integrity, SLA isolation, cancellation, mode enforcement, capability scope violation
