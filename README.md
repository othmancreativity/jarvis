# 🤖 JARVIS

**Personal AI Assistant — Local, Free, Unlimited**

[![Python](https://img.shields.io/badge/python-3.10+-green)](.)
[![Platform](https://img.shields.io/badge/platform-Windows%2011-lightblue)](.)
[![Status](https://img.shields.io/badge/status-in--development-yellow)](.)

> Fully local AI assistant. No cloud. No API costs. Runs on consumer hardware (RTX 3050, 16 GB RAM).  
> Arabic and English. Controls your computer, browser, files, and Google services.

---

## 1. Minimal Working System

**Build this first. Everything else is built on top of it.**

The simplest path through Jarvis:

```
User:  "مرحبا"
         │
  observe()   →  reads message, assembles context
  decide()    →  intent=chat, mode=normal, model=qwen3:8b
  think()     →  calls LLM → gets response text
  evaluate()  →  answer non-empty → finish
         │
Output: "مرحبا! كيف يمكنني مساعدتك؟"
```

No tools. No memory. No agents. Just: input → LLM → output.

This is Phase 1 in TASKS.md. It must work before anything else is built.

### First Boot

On first run Jarvis has no memory and no user profile. This is expected:

```python
# runtime/loop.py
state = TurnState(session_id=session_id)
history  = memory.get_history(session_id) or []       # empty list → fine
profile  = UserProfile.load(user_id) or UserProfile.default()
prompt   = prompt_builder.build(mode="normal", profile=profile)
response = llm.chat([{"role": "user", "content": user_input}], model="qwen3:8b")
```

Jarvis never refuses to answer because memory is empty.

---

## 2. Full System Flow

```
┌──────────────────────────────────────────┐
│             USER INPUT                   │
│  text │ voice │ file │ image             │
└─────────────────┬────────────────────────┘
                  │
┌─────────────────▼────────────────────────┐
│          CONTEXT BUFFER                  │
│  Stages inputs for this turn only.       │
│  Cleared after every turn completes.     │
└─────────────────┬────────────────────────┘
                  │ snapshot
┌─────────────────▼────────────────────────┐
│           RUNTIME LOOP                   │
│                                          │
│  observe()  →  decide()  →  think()      │
│      ↑              │           │        │
│   evaluate()        ▼        act()       │
│  (finish or     DecisionOutput  │        │
│   escalate)                     │        │
└────────────────────┬────────────┘        │
                     │ DecisionOutput       │
┌────────────────────▼─────────────────────┘
│          ORCHESTRATOR                    │
│  Reads DecisionOutput.                   │
│  Picks: Agent │ Tool Executor │ LLM      │
└──────────────┬──────────────┬────────────┘
               │              │
    ┌──────────▼──┐   ┌───────▼────────────┐
    │   AGENTS    │   │    TOOL SYSTEM      │
    │  Planner    │   │  registry           │
    │  Thinker    │   │  → validator        │
    │  Researcher │   │  → executor         │
    └──────────┬──┘   └───────┬────────────┘
               │              │
               └──────┬───────┘
                      │ calls
       ┌──────────────▼──────────────────────┐
       │              MODELS                 │
       │  LLM (Ollama)  │  Vision (LLaVA)   │
       │  Speech        │  Diffusion (SD)    │
       └──────────────────────────────────────┘

  All layers read from / write to:
  ┌──────────────────────────────────────────┐
  │              MEMORY                      │
  │  Short-term: session history (Redis)     │
  │  Long-term:  semantic facts (ChromaDB)   │
  │  Structured: tasks, feedback (SQLite)    │
  └──────────────────────────────────────────┘
```

---

## 3. Layer Definitions (strict — no overlap)

| Layer | Single Role | NOT responsible for |
|---|---|---|
| **Context** | Stages inputs of the **current turn** (text, files, images). Cleared after every turn. | Persistence, identity |
| **Memory** | Stores data across turns and sessions. Short-term (recent messages) + long-term (facts). | Current-turn inputs |
| **Identity** | Defines who Jarvis is and who the user is. Injected into every prompt. | Storing conversation history |
| **Runtime** | Drives the loop: `observe → decide → think → act → evaluate`. Owns max_iterations and timeouts. | Selecting agents, running tools |
| **Decision** | Classifies input (intent, complexity, mode). Selects model. No LLM call. | Executing actions, thinking |
| **Orchestrator** | Reads `DecisionOutput`. Routes to agent or tool executor. | Loop control, quality evaluation |
| **Agents** | Thinking and multi-step planning. Planner / Thinker / Researcher. | Executing OS commands, they call tools |
| **Tools** | Tool system infrastructure: registry + validator + executor. The plumbing. | Skill implementations |
| **Skills** | The actual callable capabilities: `app_launcher.py`, `web_search.py`, etc. | Tool system management |
| **Models** | Thin wrappers around AI models. Called by runtime or agents. | Control flow |

---

## 4. Runtime Loop (function-level)

```python
# src/core/runtime/loop.py

class RuntimeLoop:

    def run(self, user_input: str, session_id: str) -> Generator[str, None, None]:
        state = TurnState(session_id=session_id)

        for iteration in range(self.max_iterations):

            # ── OBSERVE ──────────────────────────────────────────────
            # Collect: user input + memory snippets + context buffer + tool traces
            observation = self.observe(user_input, state)

            # ── DECIDE ───────────────────────────────────────────────
            # Classify without calling LLM. Returns DecisionOutput.
            decision = self.decision.decide(observation)

            # ── THINK ────────────────────────────────────────────────
            # Select model, build system prompt, call LLM.
            # LLM returns: plain text OR a tool_call JSON block.
            model = self.router.select(decision)
            system_prompt = self.prompt_builder.build(decision.mode, state.profile)
            llm_output = self.llm.chat(state.messages, model, system_prompt)

            # ── ACT ──────────────────────────────────────────────────
            if llm_output.has_tool_call:
                # Run the tool, feed result back as next observation
                result = self.orchestrator.run_tool(llm_output.tool_call)
                state.add_tool_result(result)
                continue  # loop again with tool result in observation

            candidate = llm_output.text

            # ── EVALUATE ─────────────────────────────────────────────
            eval_result = self.evaluate(candidate, state, decision)

            if eval_result.recommendation == "finish":
                self.memory.save_turn("assistant", candidate, session_id)
                yield candidate
                return

            # Escalate: upgrade mode and retry
            state.mode = self._next_mode(state.mode)
            state.iteration += 1

        # Fallback after max iterations
        yield "لم أتمكن من توليد إجابة مناسبة. يرجى إعادة الصياغة."

    def observe(self, user_input: str, state: TurnState) -> str:
        history  = self.memory.get_history(state.session_id, n=10)
        snippets = self.memory.search(user_input, n=3)
        context  = self.context_buffer.snapshot()
        return build_observation(user_input, history, snippets, context, state.tool_traces)

    def evaluate(self, answer: str, state: TurnState, decision) -> EvalResult:
        if not answer.strip():
            return EvalResult("escalate", 0.0, "empty answer")
        if any(not t.success for t in state.tool_traces):
            return EvalResult("escalate", 0.3, "tool failed")
        return EvalResult("finish", 0.85)

    def _next_mode(self, current: str) -> str:
        chain = ["fast", "normal", "deep", "planning"]
        idx = chain.index(current) if current in chain else 1
        return chain[min(idx + 1, len(chain) - 1)]
```

---

## 5. Decision Layer

Classifies input **without calling an LLM**. Uses keyword matching. Fast.

```python
# src/core/runtime/decision.py

class DecisionLayer:
    def decide(self, observation: str) -> DecisionOutput:
        text = observation.lower()

        # Intent
        if any(w in text for w in ["افتح","شغّل","open","launch","run","start","close"]):
            intent, requires_tools = "action", True
        elif any(w in text for w in ["كود","code","function","implement","debug","class"]):
            intent, requires_tools = "code", False
        elif any(w in text for w in ["ابحث","search","research","find info"]):
            intent, requires_tools = "research", True
        else:
            intent, requires_tools = "chat", False

        # Complexity
        words = len(observation.split())
        multi_step = any(w in text for w in ["then","ثم","after","بعدها","and also"])
        complexity = "high" if (words > 50 or multi_step) else "medium" if words > 20 else "low"

        # Mode
        mode = "planning" if multi_step else \
               "deep"     if complexity == "high" else \
               "fast"     if complexity == "low" and intent == "chat" else "normal"

        return DecisionOutput(
            intent=intent,
            complexity=complexity,
            mode=mode,
            requires_tools=requires_tools,
            requires_planning=multi_step,
            prior_confidence=0.8 if intent == "chat" else 0.6,
        )
```

---

## 6. Model Routing

```python
# src/models/llm/router.py

# Hard rules — override everything
HARD_RULES = {
    "vision": "llava:7b",
    "code":   "qwen2.5-coder:7b",
}

# Mode-based preferences
MODE_PREFS = {
    "fast":     "gemma3:4b",
    "normal":   "qwen3:8b",
    "deep":     "qwen3:8b",
    "planning": "qwen3:8b",
    "research": "qwen3:8b",
}

class ModelRouter:
    def select(self, decision: DecisionOutput) -> str:
        if decision.intent in HARD_RULES:
            return HARD_RULES[decision.intent]
        return MODE_PREFS.get(decision.mode, "qwen3:8b")
```

Model names are config keys — they map to actual Ollama tags in `config/models.yaml`.

---

## 7. Tool Execution Flow

```
LLM emits tool_call JSON
        │
        ▼
validator.validate(name, args)   ← checks against config/schemas/{tool}.json
        │
        ├── invalid → ToolResult(success=False, error="validation: ...")
        │             → fed back as observation → LLM retries
        ▼
safety_classifier.classify(name, args)
        │
        ├── SAFE     → auto-execute
        ├── RISKY    → execute + log warning
        └── CRITICAL → pause, emit confirmation request, wait for user
        ▼
executor.run(tool, args, timeout=30s)
        │
        ▼
ToolResult{tool, success, result, error, duration_ms}
        │
        ▼
state.add_tool_result(result)
        │
        ▼
Next observe() includes: "Tool X returned: ..."
LLM generates final natural-language response
```

### Real example — "open chrome"

**LLM output:**
```json
{"tool_call": {"name": "app_launcher", "args": {"app_name": "chrome"}}}
```

**Schema validation** (`config/schemas/system/app_launcher.schema.json`):
```json
{"type": "object", "required": ["app_name"],
 "properties": {"app_name": {"type": "string", "minLength": 1}}}
```
→ passes ✓

**Safety:** `app_launcher` → SAFE → auto-execute

**Execution:**
```python
result = AppLauncherTool().execute({"app_name": "chrome"})
# → ToolResult(success=True, result="Chrome launched (PID 4821)", duration_ms=312)
```

**Next observation contains:**
```
Tool app_launcher returned: Chrome launched (PID 4821)
```

**LLM final response:** `"Chrome is now open."`

---

## 8. Prompt System

Every model call goes through `PromptBuilder`. No exceptions.

```python
# src/core/identity/prompt_builder.py

MODE_PACKS = {
    "fast":     "أجب مباشرةً وبإيجاز. بدون مقدمات.",
    "normal":   "أعطِ إجابة واضحة وكاملة.",
    "deep":     "فكّر خطوة بخطوة. راجع إجابتك.",
    "planning": "قسّم المهمة إلى خطوات مرقّمة قبل التنفيذ.",
    "research": "اجمع من زوايا متعددة. أشر إلى المصادر.",
}

def build(mode: str, profile: UserProfile, tools: list[str] = [], task: str = "") -> str:
    # Assembly order is fixed:
    # 1. Jarvis identity   (always)
    # 2. Safety rules      (always)
    # 3. User preferences  (language, style, level)
    # 4. Mode fragment     (fast / normal / deep / planning / research)
    # 5. Tool list         (only when tools available)
    # 6. Task context      (only for multi-step tasks)
    ...
```

---

## 9. Error Handling

```python
# retry with exponential backoff
for attempt in range(3):
    try:
        return self.llm.chat(messages, model, system_prompt)
    except OllamaConnectionError:
        if attempt == 2:
            return self.llm.chat(messages, "gemma3:4b", ...)  # fallback model
        time.sleep(2 ** attempt)
    except VRAMOOMError:
        self.llm.unload(model)
        model = "gemma3:4b"
        continue

# tool failure → observation, not crash
if not result.success:
    state.add_observation(f"Tool {result.tool} failed: {result.error}")
    # loop continues — LLM decides what to do next
```

---

## 10. Vertical Slice Examples

### "Say Hello" (Chat — no tools)
```
Input:   "Hello"
Decide:  intent=chat, mode=normal, model=qwen3:8b, requires_tools=False
Think:   LLM generates greeting
Act:     no tool call
Eval:    non-empty → finish
Output:  "Hello! How can I help you today?"
Files:   runtime/loop.py, runtime/decision.py, models/llm/engine.py
```

### "Open Chrome" (Action — tool required)
```
Input:   "open chrome"
Decide:  intent=action, mode=fast, model=gemma3:4b, requires_tools=True
Think:   LLM emits tool_call {name: "app_launcher", args: {app_name: "chrome"}}
Act:     validate ✓ → safety=SAFE → execute → Chrome opens
Eval:    tool success → finish
Output:  "Chrome is now open."
Files:   runtime/loop.py, runtime/decision.py, core/tools/registry.py,
         core/tools/validator.py, core/tools/executor.py,
         skills/system/app_launcher.py
```

### "Search Python news and summarize" (Research — agent)
```
Input:   "search python 3.13 features and summarize them"
Decide:  intent=research, mode=research, requires_planning=True
Orchestrator: routes to Researcher agent
Agent:   web_search("python 3.13 features") → results
         LLM summarizes results
Eval:    answer complete → finish
Output:  "Python 3.13 introduced..."
Files:   + core/agents/researcher.py, skills/search/web_search.py
```

---

## 11. AI Models

**Only one model > 3 GB VRAM at a time.**

| Model | Role | VRAM | When Loaded |
|---|---|---|---|
| `qwen3:8b` | Default — reasoning, Arabic | ~5.0 GB | mode=normal/deep/planning |
| `gemma3:4b` | Fast responses | ~3.0 GB | mode=fast, complexity=low |
| `qwen2.5-coder:7b` | Code | ~4.7 GB | intent=code |
| `llava:7b` | Vision | ~4.5 GB | intent=vision |
| Whisper medium | STT | CPU | voice input |
| Piper TTS | TTS | CPU | voice output |
| SD 1.5 | Image gen | ~4.0 GB | image generation |

---

## 12. Quick Start

```bash
# Ollama + models
winget install Ollama.Ollama
ollama pull qwen3:8b && ollama pull gemma3:4b
ollama pull qwen2.5-coder:7b && ollama pull llava:7b

# Python setup
python -m venv venv && .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install chromium

# Configure
copy config\settings.yaml.example config\settings.yaml
copy .env.example .env

# Run (Phase 1 — minimal)
python app/main.py --interface cli
```

---

## 13. Roadmap → see TASKS.md

| Phase | Build | Status |
|---|---|---|
| 1 | Minimal Working System | ⬜ |
| 2 | Runtime loop + evaluate | ⬜ |
| 3 | Decision + model routing | ⬜ |
| 4 | Tool system | ⬜ |
| 5 | Context buffer | ⬜ |
| 6 | Memory | ⬜ |
| 7 | Agents | ⬜ |
| 8 | Skills (system + browser + search) | ⬜ |
| 9 | Safety | ⬜ |
| 10 | Google APIs | ⬜ |
| 11–16 | Interfaces + optimization | ⬜ |

---

*Local. Private. No API costs.*
