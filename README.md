# JARVIS

**Local-First AI Assistant for Desktop Control and Automation**

JARVIS is a production-grade AI assistant that runs entirely on your local machine. It understands natural language in English and Arabic, then acts on your system — opening applications, managing files, automating workflows, and integrating with external services — without sending your data to the cloud.

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

Every interaction follows a clear, auditable process:

1. **Observe** — JARVIS gathers your input, recent conversation history, and relevant context from memory.
2. **Decide** — It determines your intent, selects the best approach, and identifies any actions needed.
3. **Think** — It constructs the optimal model prompt, selects the best model via weighted scoring, and plans multi-step execution if needed.
4. **Act** — It executes approved actions through its capability system, with safety checks at every step.
5. **Evaluate** — It verifies the result, and if something went wrong, adapts and tries a different approach.

This cycle is deterministic and fully logged. You can always see what JARVIS decided, why it decided it, and what happened next.

---

## Architecture Overview

JARVIS is built on a modular, layered architecture designed for reliability and control:

- **State Machine Core** — Every action flows through a controlled execution pipeline. There are no shortcuts, no hidden paths, and no unpredictable behavior.
- **Capability System** — All actions live in isolated, interchangeable modules. Adding a new capability means JARVIS instantly gains a new skill.
- **Local-First Design** — Every core component runs on your machine. External services are optional and must be explicitly enabled.
- **Separation of Concerns** — Reasoning is separated from execution. Decision-making is separated from action. This makes the system debuggable, testable, and trustworthy.

The result is an AI assistant you can inspect, control, and extend — not a black box.

---

## Execution Modes

JARVIS offers three execution modes that control how much autonomy it has:

| Mode | Behavior | Best For |
|------|----------|----------|
| **SAFE** | Every action requires your explicit confirmation before execution. | First-time users, testing new capabilities, high-risk environments. |
| **BALANCED** | Low-risk actions execute automatically. Medium-risk actions require confirmation. High-risk actions are blocked unless you explicitly approve them. | Daily use. The default mode. |
| **UNRESTRICTED** | All actions execute automatically. Schema and path validation still apply — JARVIS will never execute structurally invalid commands. | Trusted environments, automated workflows, advanced users. |

You can switch modes at any time using the `/mode` command in the chat interface.

---

## Performance & Hardware Awareness

JARVIS is designed to run on real hardware, not idealized server environments:

- **GPU-Aware Model Selection** — JARVIS monitors available VRAM in real time and selects models that fit your hardware. It automatically downgrades when resources are constrained.
- **One Model at a Time** — Models are loaded and unloaded as needed, maximizing the use of limited VRAM. Heavy tasks use powerful models; simple tasks use lightweight ones.
- **Efficient Execution** — Simple requests are resolved through fast-path rules without calling a model at all. Complex requests get the full reasoning pipeline.
- **Measured Latency** — Fast-path responses return in under 100ms. Simple queries resolve in under 5 seconds. Complex multi-step tasks complete within 30 seconds.

Target hardware: NVIDIA RTX 3050 (6GB VRAM), 16GB RAM, Intel Core i5 12th Gen. JARVIS works on this configuration and scales upward from there.

---

## Safety Philosophy

JARVIS is built with a simple principle: **trust must be earned, and control must always remain with the user.**

- **Structured Validation** — Every action is validated against strict schemas before execution. Invalid arguments are rejected before they can cause harm.
- **Risk-Aware Execution** — Actions are classified by risk level. Destructive operations require explicit approval. Path traversal, system-level commands, and irreversible actions are handled with extra scrutiny.
- **Audit Trail** — Every action JARVIS takes is logged with full context: what it did, why it did it, and what the result was. Nothing happens in the dark.
- **No Prompt-Based Safety** — Safety rules are enforced by the system itself, not by asking the model to behave. This means safety cannot be bypassed through clever prompting.

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

**JARVIS v3.0** — Local-first. Deterministic. Contract-enforced. Under your control.

---

## Spec Authority

- **Single source of truth:** `TASKS.md` is the authoritative execution plan (spec_version: v3.0).
- **Structure definition:** `STRUCTURE.md` defines the canonical directory layout and layer boundaries.
- **User-facing docs:** `README.md` describes behavior, capabilities, and usage.
- **Version discipline:** `project_version: 3.0.0`, `spec_version: v3.0`, `structure_version: 1`. Breaking changes require major version bump.
- All three files must align. Drift is a spec violation.
