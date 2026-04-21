# 🗂️ JARVIS — Execution Plan

> **Format:** Every task contains: DESCRIPTION · INPUT · OUTPUT · FILES · REQUIREMENTS · SUCCESS CRITERIA
>
> **No code in this file.** Implementation details are in source files.

---

## ⛔ MANDATORY GATE

**Phase 0 is a hard prerequisite. You may not begin Phase 1 or any other phase until Phase 0 is fully complete and both success criteria pass.**

Verify Phase 0 by running the two manual tests described in Tasks 0.4 and 0.5. Both must pass without error before proceeding.

---

## 📊 Progress Tracker

| Phase | Name | Tasks | Done |
|-------|------|-------|------|
| 0 | First Working System (MANDATORY FIRST) | 5 | 0 |
| 1 | Foundation | 9 | 0 |
| 2 | Execution Contract Implementation | 6 | 0 |
| 3 | Runtime Loop | 6 | 0 |
| 4 | Decision System | 5 | 0 |
| 5 | Prompt Builder | 4 | 0 |
| 6 | Tool System | 7 | 0 |
| 7 | Safety Modes | 5 | 0 |
| 8 | System Control Skills | 8 | 0 |
| 9 | Browser & Web Skills | 6 | 0 |
| 10 | Google APIs | 7 | 0 |
| 11 | Context + Memory | 6 | 0 |
| 12 | Agents | 5 | 0 |
| 13 | CLI Interface | 5 | 0 |
| 14 | Web UI | 12 | 0 |
| 15 | Voice Pipeline | 5 | 0 |
| 16 | Vision + Image Generation | 4 | 0 |
| 17 | Telegram + GUI | 4 | 0 |
| 18 | QA + Security | 7 | 0 |

---

## 🚀 Phase 0 — First Working System

> **⛔ MANDATORY. Must be completed before any other phase. No exceptions.**
>
> **End state:** Two things work end-to-end — text to LLM, and "open chrome" executes.

---

### TASK 0.1 — Connect to Ollama and get a response

**DESCRIPTION:** Prove that Ollama is reachable and a model returns text.

**INPUT:** The string "hello" passed programmatically.

**OUTPUT:** A non-empty string response printed to the terminal.

**FILES:**
- CREATE: `src/models/llm/engine.py`

**REQUIREMENTS:**
- The file must define a `chat` function that accepts a message string and an optional model string.
- The function must call the Ollama Python client.
- The function must return the response content as a string.
- The file must be executable directly with Python and print the result of `chat("hello")`.

**SUCCESS CRITERIA:**
- Running the file directly prints a non-empty response.
- No exception is raised.
- The response arrives within 60 seconds.

---

### TASK 0.2 — Classify a command and return structured output

**DESCRIPTION:** Given a user message, return a structured classification describing what action to take.

**INPUT:** The string "open chrome".

**OUTPUT:** A Python dict containing at minimum: `intent`, `tool_name`, `tool_args`.

**FILES:**
- CREATE: `src/core/decision/classifier.py`

**REQUIREMENTS:**
- The file must define a `classify` function that accepts a message string and returns a dict.
- The function must use `gemma3:4b` with a system prompt that forces JSON-only output.
- The function must handle malformed JSON from the model by retrying up to 2 times.
- If all retries fail, the function must return a safe fallback dict with `intent="chat"`.
- The system prompt must include Arabic and English examples.
- The function must strip any markdown code block formatting before parsing JSON.

**SUCCESS CRITERIA:**
- `classify("open chrome")` returns a dict with `intent="tool_use"` and `tool_name="open_app"`.
- `classify("افتح Chrome")` returns the same result as `classify("open chrome")`.
- `classify("what is AI?")` returns a dict with `intent="chat"`.
- No exception is raised on any of the three inputs.

---

### TASK 0.3 — Execute an application by name

**DESCRIPTION:** Open a named application on the current operating system.

**INPUT:** A dict `{"name": "notepad"}` (or the platform-appropriate app name).

**OUTPUT:** The application opens visibly. A dict is returned with `success=True` and the process PID.

**FILES:**
- CREATE: `src/skills/system/apps.py`

**REQUIREMENTS:**
- The file must define an `open_app(name)` function.
- The function must search in this order: PATH via `shutil.which`, then platform-specific program directories.
- On Windows: search `PROGRAMFILES`, `PROGRAMFILES(X86)`, `LOCALAPPDATA`.
- On Linux: attempt `subprocess.Popen([name])` directly.
- On macOS: use `open -a {name}`.
- If the app is not found after all searches, return a dict with `success=False` and an `error` key.
- The function must not raise an exception on failure.

**SUCCESS CRITERIA:**
- Calling `open_app("notepad")` on Windows opens Notepad and returns `{"success": True, "pid": <number>}`.
- Calling `open_app("xyznonexistent")` returns `{"success": False, "error": "..."}` without raising.

---

### TASK 0.4 — Wire classifier to tool: text input → action

**DESCRIPTION:** Connect the three components — input, classifier, tool — into a single runnable script.

**INPUT:** A string typed at a terminal prompt.

**OUTPUT:** If the input is classified as a tool call, the tool executes and a confirmation is printed. Otherwise, a chat response is printed.

**FILES:**
- CREATE: `app/jarvis_slice.py`

**REQUIREMENTS:**
- The file must define a `run(user_input)` function.
- The function must call `classify(user_input)` from Task 0.2.
- If `requires_tools=True` and `tool_name` is in the supported tool map, the function must call the corresponding tool function.
- If `requires_tools=False`, the function must call `chat(user_input)` from Task 0.1 and print the result.
- The file must be executable directly and loop on terminal input until "quit" is typed.
- The file must handle `classify()` returning a malformed or unexpected dict without crashing.

**SUCCESS CRITERIA:**
- Typing "open notepad" opens Notepad and prints a confirmation.
- Typing "what is machine learning?" prints a text answer.
- Typing "quit" exits cleanly.
- No exception reaches the terminal for any input.

---

### TASK 0.5 — Verify Arabic input

**DESCRIPTION:** Confirm that Arabic commands produce the same behavior as their English equivalents.

**INPUT:** Arabic text at the `jarvis_slice.py` terminal prompt.

**OUTPUT:** Same behavior as the English equivalent.

**FILES:**
- MODIFY: `src/core/decision/classifier.py` — add Arabic examples to the system prompt if needed.

**REQUIREMENTS:**
- The Arabic command for "open notepad" must produce the same classification as the English command.
- If it does not, add at least three Arabic examples to the classifier system prompt and re-test.
- No new files are needed unless the classifier fails on Arabic.

**SUCCESS CRITERIA:**
- Typing the Arabic equivalent of "open notepad" opens Notepad.
- Typing an Arabic question returns a text answer.
- The classifier does not return `intent="chat"` for a clear Arabic tool command.

---

## 🏗️ Phase 1 — Foundation

> **End state:** `python app/main.py --interface cli` runs without crashing, loads config, initializes logging, and prints "Jarvis ready."

---

### TASK 1.1 — Settings YAML and Pydantic loader

**DESCRIPTION:** Create the configuration file and a typed Python loader for it.

**INPUT:** `config/settings.yaml`.

**OUTPUT:** A callable `get_settings()` function that returns a fully typed settings object.

**FILES:**
- CREATE: `config/settings.example.yaml`
- CREATE: `config/settings.yaml` (copy from example, fill in values)
- CREATE: `src/core/config.py`

**REQUIREMENTS:**
- `settings.example.yaml` must contain all sections: jarvis, models, hardware, interfaces, paths, hotkeys, runtime.
- The `runtime` section must include: `max_iterations`, `max_tool_retries`, `tool_timeout_s`, `execution_mode`.
- `execution_mode` must default to `"balanced"`.
- `src/core/config.py` must define one Pydantic model per YAML section.
- `get_settings()` must be a cached singleton — it reads the file once only.
- `get_settings()` must not raise on missing optional fields — use Pydantic defaults.
- A `create_directories()` function must create all paths defined in the `paths` section.

**SUCCESS CRITERIA:**
- `get_settings().jarvis.name` returns `"Jarvis"`.
- `get_settings().runtime.execution_mode` returns `"balanced"`.
- `create_directories()` creates all configured directories without error.
- Calling `get_settings()` twice returns the same object (cached).

---

### TASK 1.2 — Logging setup

**DESCRIPTION:** Configure structured logging to both terminal and file.

**INPUT:** A call to `setup_logging()` at startup.

**OUTPUT:** Log entries appear in the terminal and in `logs/jarvis.log`.

**FILES:**
- CREATE: `src/core/logging_setup.py`

**REQUIREMENTS:**
- The function must configure Loguru with two sinks: terminal (colored) and file.
- File rotation must trigger at 10 MB. Retention must be 7 days.
- Log format must include: timestamp, level, message.
- The function must accept a `level` parameter (default `"INFO"`) and a `debug` boolean.
- When `debug=True`, a second file sink at DEBUG level must be added to `logs/debug.log`.
- The function must create the `logs/` directory if it does not exist.

**SUCCESS CRITERIA:**
- After calling `setup_logging()`, a log call at INFO level appears in both terminal and file.
- The `logs/` directory is created automatically.
- File rotation parameters are confirmed in the Loguru configuration.

---

### TASK 1.3 — Package skeleton

**DESCRIPTION:** Create all Python package directories with `__init__.py` files.

**INPUT:** Nothing.

**OUTPUT:** All source directories exist and are importable Python packages.

**FILES:**
- CREATE: All directories listed in `STRUCTURE.md` under `src/`, each with an empty `__init__.py`.

**REQUIREMENTS:**
- Every subdirectory under `src/` must have an `__init__.py` file.
- The files must be empty (no imports, no code).
- No directory may be skipped.

**SUCCESS CRITERIA:**
- `python -c "import src.core.decision"` succeeds.
- `python -c "import src.skills.system"` succeeds.
- `python -c "import src.interfaces.cli"` succeeds.

---

### TASK 1.4 — Model capability profiles

**DESCRIPTION:** Create the model metadata file and a Python loader.

**INPUT:** `config/models.yaml`.

**OUTPUT:** A `get_model_profile(tag)` function returning a dict of capability fields.

**FILES:**
- CREATE: `config/models.yaml`
- CREATE: `src/models/profiles.py`

**REQUIREMENTS:**
- `models.yaml` must contain entries for: `qwen3:8b`, `gemma3:4b`, `qwen2.5-coder:7b`, `llava:7b`.
- Each entry must include: temperature, top_p, max_tokens, vram_gb, arabic_quality, reasoning, code_bias, vision, latency.
- `src/models/profiles.py` must define `get_model_profile(model_tag)` returning the dict for that model.
- The function must return an empty dict (not raise) for an unknown model tag.

**SUCCESS CRITERIA:**
- `get_model_profile("qwen3:8b")["vram_gb"]` returns `5.0`.
- `get_model_profile("llava:7b")["vision"]` returns `True`.
- `get_model_profile("nonexistent")` returns `{}` without raising.

---

### TASK 1.5 — LLM engine with VRAM guard

**DESCRIPTION:** Expand the engine from Task 0.1 with model tracking and safe swapping.

**INPUT:** A call to `swap_to("qwen3:8b")` followed by `swap_to("gemma3:4b")`.

**OUTPUT:** Models swap without error. Only one model is active at a time.

**FILES:**
- MODIFY: `src/models/llm/engine.py`

**REQUIREMENTS:**
- Add a module-level variable tracking the currently active model name.
- Add `get_active_model()` returning the current model tag or `None`.
- Add `unload_current_model()` that calls the Ollama API to release the model from memory.
- Add `swap_to(model)` that unloads the current model if it differs from the requested model, then sets the active model tracker.
- `swap_to` must log the swap event.
- No function may raise an exception on failure — log and return gracefully.

**SUCCESS CRITERIA:**
- After `swap_to("gemma3:4b")`, `get_active_model()` returns `"gemma3:4b"`.
- After `swap_to("qwen3:8b")`, `get_active_model()` returns `"qwen3:8b"`.
- No OOM error occurs during the sequence.

---

### TASK 1.6 — Environment variables

**DESCRIPTION:** Document and load all required secrets from a `.env` file.

**INPUT:** `.env` file with keys filled in.

**OUTPUT:** Environment variables accessible via `os.environ`.

**FILES:**
- CREATE: `.env.example`
- CREATE: `.env` (copy from example; user fills in values)

**REQUIREMENTS:**
- `.env.example` must list all required keys with empty values.
- Required keys: `TELEGRAM_BOT_TOKEN`, `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `YOUTUBE_API_KEY`, `SESSION_ENCRYPTION_KEY`, `JARVIS_DEBUG`, `OLLAMA_HOST`.
- `SESSION_ENCRYPTION_KEY` must have a comment explaining how to generate it.
- `JARVIS_DEBUG` must default to `0`.
- `OLLAMA_HOST` must default to `http://localhost:11434`.
- `.env` must be listed in `.gitignore`.
- `app/main.py` must call `load_dotenv()` before any other import.

**SUCCESS CRITERIA:**
- `os.environ.get("JARVIS_DEBUG")` returns `"0"` after loading a `.env` file with that value.
- `.env` does not appear in `git status` output.

---

### TASK 1.7 — User profile

**DESCRIPTION:** Create a persistent JSON store for user preferences.

**INPUT:** A dict of preference updates.

**OUTPUT:** Preferences saved to `data/user_profile.json` and loadable after restart.

**FILES:**
- CREATE: `src/core/memory/user_profile.py`

**REQUIREMENTS:**
- Define `load_profile()` returning a dict. Return defaults if file does not exist.
- Define `save_profile(updates)` merging updates into the existing profile and writing to disk.
- Define `get_profile_value(key, default)` for reading individual values.
- Default profile must include: name, language, style, tone, technical_level, timezone.
- Language default must be `"ar"`. Style default must be `"balanced"`.
- The file path must come from `get_settings().paths.data`.

**SUCCESS CRITERIA:**
- `save_profile({"language": "en"})` writes to disk.
- After Python restarts, `load_profile()["language"]` returns `"en"`.
- `load_profile()` returns default values when no file exists.

---

### TASK 1.8 — Skills manifest

**DESCRIPTION:** Create the tool registry manifest YAML that declares all tools.

**INPUT:** Nothing.

**OUTPUT:** `config/skills.yaml` with all tools declared.

**FILES:**
- CREATE: `config/skills.yaml`

**REQUIREMENTS:**
- Every tool in the system must have an entry.
- Each entry must include: id (snake_case), enabled (bool), category, module path, platform list, risk_level (low|medium|high), schema path.
- `risk_level` must be set based on the Risk Classification table in README Section 8.
- Tools with `enabled: false` must not be loaded by the registry.
- `delete_file`, `kill_process`, `send_email`, `send_message` must have `risk_level: high`.
- `execute_python`, `run_shell`, `open_app` must have `risk_level: medium`.
- `web_search`, `read_file`, `system_info` must have `risk_level: low`.

**SUCCESS CRITERIA:**
- Every tool mentioned in README Section 14 has an entry in the YAML.
- No tool has a missing or empty `risk_level` field.
- File is valid YAML (parseable without error).

---

### TASK 1.9 — main.py entry point

**DESCRIPTION:** Create the single executable entry point for the system.

**INPUT:** `--interface cli` command-line argument.

**OUTPUT:** The system boots through all 10 steps in the Boot Flow (README Section 7) and prints "Jarvis ready."

**FILES:**
- CREATE: `app/main.py`

**REQUIREMENTS:**
- Must parse `--interface` argument with choices: cli, web, voice, telegram, gui, all.
- Must parse `--debug` flag.
- Must execute Boot Flow steps 1 through 10 in order.
- Must catch `KeyboardInterrupt` and log "Jarvis stopped by user" before exiting.
- Must add the project root to `sys.path` so `src.*` imports work.
- Must call `load_dotenv()` before importing anything from `src/`.
- Each boot step must log its completion.

**SUCCESS CRITERIA:**
- `python app/main.py --interface cli` executes all boot steps without error.
- "Jarvis ready" appears in the log.
- `Ctrl+C` exits without a traceback.

---

## 📦 Phase 2 — Execution Contract Implementation

> **End state:** All four contract types (`InputPacket`, `DecisionOutput`, `LLMOutput`, `ToolResult`) are defined as Pydantic models and used across all phases.

---

### TASK 2.1 — Define InputPacket

**DESCRIPTION:** Create the `InputPacket` Pydantic model as defined in README Section 3.

**INPUT:** A user message string and session ID.

**OUTPUT:** An `InputPacket` instance with all fields populated.

**FILES:**
- CREATE: `src/core/context/bundle.py`

**REQUIREMENTS:**
- Define `InputPacket` with all fields from the Execution Contract: user_message, session_id, attachments, memory_snippets, recent_history, user_profile, tool_results, turn_number.
- Define supporting types: `Attachment`, `Message`, `UserProfile`, `ToolResult` as Pydantic models.
- All list fields must default to empty lists.
- All optional fields must have explicit defaults.
- No field may have an ambiguous type (no `Any`).

**SUCCESS CRITERIA:**
- `InputPacket(user_message="hello", session_id="s1")` instantiates without error.
- All fields accessible with correct types.
- Attempting to assign a wrong type to a field raises a Pydantic validation error.

---

### TASK 2.2 — Define DecisionOutput

**DESCRIPTION:** Create the `DecisionOutput` Pydantic model as defined in README Section 3.

**INPUT:** Raw classification output.

**OUTPUT:** A `DecisionOutput` instance with all required fields.

**FILES:**
- CREATE: `src/core/decision/decision.py`

**REQUIREMENTS:**
- Define `DecisionOutput` with all fields from the Execution Contract: intent, complexity, mode, model, requires_tools, requires_planning, tool_name, tool_args, confidence, risk_level.
- `intent` must be constrained to the allowed values.
- `complexity` must be constrained to: low, medium, high.
- `mode` must be constrained to: fast, normal, deep, planning, research.
- `risk_level` must be constrained to: low, medium, high.
- `tool_name` must allow `None`.
- `tool_args` must default to `{}`.

**SUCCESS CRITERIA:**
- `DecisionOutput(intent="chat", complexity="low", mode="fast", model="gemma3:4b", requires_tools=False, requires_planning=False, confidence=0.9, risk_level="low")` instantiates without error.
- Setting `intent="invalid"` raises a validation error.

---

### TASK 2.3 — Define LLMOutput

**DESCRIPTION:** Create the `LLMOutput` Pydantic model as defined in README Section 3.

**INPUT:** Raw string from an LLM response.

**OUTPUT:** An `LLMOutput` instance with `type` set to either `"answer"` or `"tool_call"`.

**FILES:**
- CREATE: `src/core/runtime/llm_output.py`

**REQUIREMENTS:**
- Define `LLMOutput` with fields: type, content, tool, args.
- `type` must be constrained to: `"answer"` | `"tool_call"`.
- `content` is populated when `type="answer"`.
- `tool` and `args` are populated when `type="tool_call"`.
- Define `parse_llm_output(raw_text, requires_tools)` that:
  - Attempts to extract JSON matching `{"type": "tool_call", "tool": "...", "args": {...}}` from the text.
  - Returns `LLMOutput(type="tool_call", ...)` if JSON found and `requires_tools=True`.
  - Returns `LLMOutput(type="answer", content=raw_text)` if no JSON found and `requires_tools=False`.
  - Returns `LLMOutput(type="tool_call", tool="", args={})` with a parse failure marker if `requires_tools=True` but no valid JSON found.

**SUCCESS CRITERIA:**
- Parsing `'{"type":"tool_call","tool":"open_app","args":{"name":"chrome"}}'` returns `LLMOutput(type="tool_call", tool="open_app")`.
- Parsing `"Paris is the capital of France."` with `requires_tools=False` returns `LLMOutput(type="answer")`.
- Parsing non-JSON text with `requires_tools=True` returns a `tool_call` type with empty tool name (parse failure marker).

---

### TASK 2.4 — Define ToolResult (execution layer)

**DESCRIPTION:** Create the `ToolResult` Pydantic model as defined in README Section 3.

**INPUT:** Results from `tool.execute()`.

**OUTPUT:** A `ToolResult` instance with success status, data, and metadata.

**FILES:**
- CREATE: `src/core/tools/result.py`

**REQUIREMENTS:**
- Define `ToolResult` with fields: tool, success, data, error, duration_ms.
- `data` must default to `{}`.
- `error` must default to `""`.
- `duration_ms` must default to `0.0`.
- Import `ToolResult` from `src/core/context/bundle.py` OR define it once here and import it in `bundle.py` — no duplicate definitions.

**SUCCESS CRITERIA:**
- `ToolResult(tool="open_app", success=True, data={"pid": 123})` instantiates without error.
- `ToolResult(tool="open_app", success=False, error="Not found")` instantiates without error.

---

### TASK 2.5 — Define FinalResponse

**DESCRIPTION:** Create the `FinalResponse` type used as the output of `run_turn()`.

**INPUT:** Approved response text with metadata.

**OUTPUT:** A `FinalResponse` instance returned to the interface layer.

**FILES:**
- CREATE: `src/core/runtime/final_response.py`

**REQUIREMENTS:**
- Define `FinalResponse` with fields: text, session_id, model, mode, quality.
- All fields are required. No defaults.
- The interface layer must accept `FinalResponse` and display `text` to the user.

**SUCCESS CRITERIA:**
- `FinalResponse(text="hello", session_id="s1", model="qwen3:8b", mode="normal", quality=0.85)` instantiates without error.

---

### TASK 2.6 — Contract validation tests

**DESCRIPTION:** Write tests confirming all five contract types enforce their schemas correctly.

**INPUT:** Valid and invalid field combinations.

**OUTPUT:** Pydantic raises on invalid; accepts on valid.

**FILES:**
- CREATE: `tests/test_contracts.py`

**REQUIREMENTS:**
- Test that each model raises `ValidationError` on invalid field values.
- Test that each model accepts valid field values.
- Test `parse_llm_output` with all three cases from Task 2.3.
- No real Ollama calls in this test file — pure type system tests.

**SUCCESS CRITERIA:**
- `pytest tests/test_contracts.py` passes with 0 failures.

---

## 🔄 Phase 3 — Runtime Loop

> **End state:** A complete turn executes: InputPacket assembled → decision made → LLM called → response or tool call returned → evaluator approves or escalates → FinalResponse returned.

---

### TASK 3.1 — Context assembler

**DESCRIPTION:** Implement the function that builds an `InputPacket` from user input.

**INPUT:** User message string, session ID, optional attachment list.

**OUTPUT:** A populated `InputPacket`.

**FILES:**
- CREATE: `src/core/context/assembler.py`

**REQUIREMENTS:**
- Define `assemble_context(user_message, session_id, attachments)` returning `InputPacket`.
- Must load user profile via `load_profile()`.
- Memory fields (`memory_snippets`, `recent_history`) must be populated with empty lists in this phase. Phase 11 will wire in the actual memory calls.
- Must track and increment `turn_number` per session using a module-level dict.
- Must not raise on any valid input.

**SUCCESS CRITERIA:**
- `assemble_context("hello", "s1")` returns an `InputPacket` with `user_message="hello"`.
- `turn_number` increments on repeated calls with the same session ID.
- `user_profile.language` is populated from the user profile file.

---

### TASK 3.2 — Decision function

**DESCRIPTION:** Implement the `decide()` function that produces `DecisionOutput` from an `InputPacket`.

**INPUT:** `InputPacket`.

**OUTPUT:** `DecisionOutput`.

**FILES:**
- MODIFY: `src/core/decision/decision.py`

**REQUIREMENTS:**
- Define `decide(packet: InputPacket) → DecisionOutput`.
- Implement fast-path rules first (no LLM call): image in attachments → vision; message < 20 chars and no action keywords → fast chat.
- For all other cases, call `classify(packet.user_message)` from `classifier.py`.
- Map the raw classification dict to a `DecisionOutput` instance.
- Handle classifier failure by returning a safe default `DecisionOutput`.
- The `risk_level` on `DecisionOutput` must be read from `config/skills.yaml` for the classified `tool_name`. If no tool or tool not found, default to `"low"`.

**SUCCESS CRITERIA:**
- `decide(assemble_context("hello", "s1"))` returns `DecisionOutput` with `intent="chat"`.
- `decide(assemble_context("open chrome", "s1"))` returns `tool_name="open_app"`.
- A classifier exception does not propagate — a fallback `DecisionOutput` is returned.

---

### TASK 3.3 — Executor (think step)

**DESCRIPTION:** Implement the `execute_turn()` function that calls the LLM and returns `LLMOutput`.

**INPUT:** `DecisionOutput`, `InputPacket`.

**OUTPUT:** `LLMOutput`.

**FILES:**
- CREATE: `src/core/runtime/executor.py`

**REQUIREMENTS:**
- Define `execute_turn(decision, packet)` returning `LLMOutput`.
- Must call `swap_to(decision.model)` before calling the LLM.
- Must call `build_system_prompt()` from the Prompt Builder (Phase 5) — use a stub that returns an empty string until Phase 5 is complete.
- Must construct the message list from the system prompt and the user message.
- Must call `stream_chat()` and collect all tokens into a full string.
- Must pass the full string to `parse_llm_output(raw, decision.requires_tools)`.
- Must return the parsed `LLMOutput`.

**SUCCESS CRITERIA:**
- `execute_turn(decision, packet)` returns an `LLMOutput` with a non-empty `content` or a valid `tool` name.
- An Ollama error returns `LLMOutput(type="answer", content="I encountered an error...")` rather than raising.

---

### TASK 3.4 — Evaluator

**DESCRIPTION:** Implement the evaluator that scores a response and decides if retry is needed.

**INPUT:** `LLMOutput`, `DecisionOutput`.

**OUTPUT:** `EvalResult(quality, should_retry, reason)`.

**FILES:**
- CREATE: `src/core/runtime/evaluator.py`

**REQUIREMENTS:**
- Define `EvalResult` as a Pydantic model with fields: quality (float 0–1), should_retry (bool), reason (str).
- Define `evaluate(output, decision) → EvalResult`.
- Rules:
  - `output.content` empty or whitespace only → quality=0.0, retry=True.
  - `decision.complexity == "high"` and `len(output.content) < 80` → quality=0.3, retry=True.
  - `decision.requires_tools=True` and `output.type="answer"` and response is short → quality=0.4, retry=True.
  - All other cases → quality=0.85, retry=False.
- Must not call any model or external service.

**SUCCESS CRITERIA:**
- Empty content → `should_retry=True`.
- Valid answer for simple question → `should_retry=False`.
- Rules match the conditions listed above exactly.

---

### TASK 3.5 — Runtime loop

**DESCRIPTION:** Implement the main `run_turn()` function that drives the full cycle.

**INPUT:** User message string, session ID.

**OUTPUT:** `FinalResponse`.

**FILES:**
- CREATE: `src/core/runtime/loop.py`

**REQUIREMENTS:**
- Define `run_turn(user_input, session_id, attachments) → FinalResponse`.
- Define `run_turn_streaming(user_input, session_id, attachments)` as a generator yielding string tokens.
- Implement the loop exactly as described in README Section 4 (Runtime Loop).
- Read `max_iterations` from `get_settings().runtime.max_iterations`.
- On tool call: call `execute_tool(output.tool, output.args)` from Phase 6, append result to `packet.tool_results`, and continue the loop.
- On approved answer: build and return `FinalResponse`.
- When `max_iterations` is exhausted: return `FinalResponse` with the last generated content and a note that iterations were exhausted.
- Emit EventBus events: `turn.start`, `decision`, `turn.end`.
- All memory saving (Phase 11) is wired here as stub calls that do nothing until Phase 11 is implemented.

**SUCCESS CRITERIA:**
- `run_turn("what is AI?", "s1")` returns a `FinalResponse` with non-empty `text`.
- `run_turn("open notepad", "s1")` triggers the tool path and opens Notepad.
- Loop does not run more than `max_iterations` times.

---

### TASK 3.6 — EventBus

**DESCRIPTION:** Implement the publish-subscribe event system.

**INPUT:** An event name and a data dict.

**OUTPUT:** All registered handlers for that event receive the data.

**FILES:**
- CREATE: `src/core/events.py`

**REQUIREMENTS:**
- Define `EventBus` class with `subscribe(event, handler)`, `unsubscribe(event, handler)`, and `emit(event, data)` methods.
- Define a module-level singleton `bus`.
- `emit` must not raise if a handler raises — log the error and continue to other handlers.
- No external dependencies — pure Python.

**SUCCESS CRITERIA:**
- Subscribe a handler to `"turn.end"`. Call `bus.emit("turn.end", {"text": "hi"})`. Handler is called with the dict.
- A handler that raises does not prevent other handlers from running.

---

## 🎯 Phase 4 — Decision System

> **End state:** All intent types classified correctly. Correct model selected for each intent. Risk level populated on every `DecisionOutput`.

---

### TASK 4.1 — Classifier with robust JSON parsing

**DESCRIPTION:** Harden the classifier to handle all LLM output variations.

**INPUT:** Any user message string.

**OUTPUT:** Always returns a valid dict matching the `DecisionOutput` schema fields.

**FILES:**
- MODIFY: `src/core/decision/classifier.py`

**REQUIREMENTS:**
- Extract JSON from LLM output by finding the first `{` and last `}` in the response string.
- Strip markdown code block markers before parsing.
- Validate that all required fields are present in the parsed dict.
- Retry with an explicit correction instruction if any required field is missing.
- Return a safe fallback dict after 2 failed retries.
- Log each retry and each fallback event.

**SUCCESS CRITERIA:**
- Classifier returns a valid dict for any non-empty string input.
- Classifier returns the fallback dict when the model responds with free text.
- No exception escapes the function.

---

### TASK 4.2 — Fast-path classification rules

**DESCRIPTION:** Implement the no-LLM fast path for obvious cases.

**INPUT:** `InputPacket`.

**OUTPUT:** `DecisionOutput` without calling any model.

**FILES:**
- MODIFY: `src/core/decision/decision.py`

**REQUIREMENTS:**
- Implement all fast-path rules from README Section 11.
- Fast path must run before any LLM call.
- Each fast-path rule must have a corresponding log line at DEBUG level.
- Fast path must not be applied if the message contains known tool action keywords (open, close, send, search, find, create, delete, run).

**SUCCESS CRITERIA:**
- A message of 5 characters with no action keywords routes to fast chat without any Ollama call (verify by checking `get_active_model()` is unchanged).
- An image in attachments routes to `llava:7b` via fast path.

---

### TASK 4.3 — Risk level population

**DESCRIPTION:** Populate `risk_level` on `DecisionOutput` based on `config/skills.yaml`.

**INPUT:** `tool_name` from classification.

**OUTPUT:** `DecisionOutput.risk_level` set to the correct value from the manifest.

**FILES:**
- MODIFY: `src/core/decision/decision.py`

**REQUIREMENTS:**
- Load `config/skills.yaml` once at module import time.
- When a `tool_name` is present on `DecisionOutput`, look up its `risk_level` in the loaded manifest.
- If `tool_name` is `None` or not found in the manifest, set `risk_level="low"`.

**SUCCESS CRITERIA:**
- `decide(assemble_context("delete my desktop files", "s1"))` returns `risk_level="high"`.
- `decide(assemble_context("what is AI?", "s1"))` returns `risk_level="low"`.

---

### TASK 4.4 — Escalation chain

**DESCRIPTION:** Define and implement the mode/model escalation sequence used by the runtime loop.

**INPUT:** Current mode and model strings.

**OUTPUT:** Next mode and model strings, or `None` if already at maximum.

**FILES:**
- CREATE: `src/core/runtime/escalation.py`

**REQUIREMENTS:**
- Define the chain as: fast/gemma3:4b → normal/qwen3:8b → deep/qwen3:8b.
- Define `get_next_escalation(current_mode, current_model)` returning a tuple `(mode, model)` or `None`.
- The function must be pure (no side effects, no external calls).

**SUCCESS CRITERIA:**
- `get_next_escalation("fast", "gemma3:4b")` returns `("normal", "qwen3:8b")`.
- `get_next_escalation("deep", "qwen3:8b")` returns `None`.

---

### TASK 4.5 — Decision system tests

**DESCRIPTION:** Test all routing rules and the escalation chain.

**INPUT:** Various test messages.

**OUTPUT:** Correct `DecisionOutput` for each.

**FILES:**
- CREATE: `tests/test_decision.py`

**REQUIREMENTS:**
- Test that "code"-intent messages route to `qwen2.5-coder:7b`.
- Test that Arabic tool commands route to `tool_use` intent.
- Test that image-attached packets route to `llava:7b`.
- Test the fast path (short message, no action keywords, no LLM call).
- Test the escalation chain from Task 4.4.
- No real Ollama calls — mock the `classify` function.

**SUCCESS CRITERIA:**
- `pytest tests/test_decision.py` passes with 0 failures.

---

## 📝 Phase 5 — Prompt Builder

> **End state:** Every LLM call receives a system prompt assembled from the components in README Section 10 in the correct order.

---

### TASK 5.1 — Jarvis identity YAML

**DESCRIPTION:** Create the identity definition file.

**INPUT:** Nothing.

**OUTPUT:** `config/jarvis_identity.yaml` with all required fields.

**FILES:**
- CREATE: `config/jarvis_identity.yaml`

**REQUIREMENTS:**
- Must include: name, role, component_notice, safety_rules (list), language_behavior (per language: greeting, affirmation, style).
- `component_notice` must state that the model is a component of Jarvis, not the underlying model.
- `safety_rules` must include at least 4 rules covering: credentials, destructive actions, uncertainty, and privacy.
- Language behavior entries must exist for both `ar` and `en`.

**SUCCESS CRITERIA:**
- File is valid YAML.
- All required keys are present and non-empty.

---

### TASK 5.2 — Mode fragments

**DESCRIPTION:** Create the text fragments that define each thinking mode's behavior.

**INPUT:** A mode string.

**OUTPUT:** The corresponding instruction fragment.

**FILES:**
- CREATE: `src/core/identity/personality.py`

**REQUIREMENTS:**
- Define a dict `MODE_FRAGMENTS` with entries for: fast, normal, deep, planning, research.
- Each value must be a one-to-three sentence instruction.
- The fragments must match the descriptions in README Section 10.
- Define `get_mode_fragment(mode)` returning the fragment or an empty string for unknown modes.

**SUCCESS CRITERIA:**
- `get_mode_fragment("fast")` returns a non-empty string.
- `get_mode_fragment("unknown_mode")` returns `""` without raising.
- All five modes have distinct, non-empty fragments.

---

### TASK 5.3 — System prompt builder

**DESCRIPTION:** Implement the central function that builds the complete system prompt.

**INPUT:** task context, mode, tool list, previous model, current model.

**OUTPUT:** A complete system prompt string.

**FILES:**
- CREATE: `src/core/identity/builder.py`

**REQUIREMENTS:**
- Define `build_system_prompt(task_context, mode, tools, previous_model, current_model)` returning a string.
- Assemble blocks in the exact order defined in README Section 10: identity → safety → user profile → mode fragment → task context → tool list → handoff note.
- Load identity from `config/jarvis_identity.yaml` once at import time (cached).
- Load user profile via `load_profile()` on each call (profile can change at runtime).
- Include the tool list block only if `tools` is non-empty.
- Include the handoff note only if `previous_model` is not `None` and differs from `current_model`.
- The tool list must list tool names and descriptions only — no schema details.

**SUCCESS CRITERIA:**
- `build_system_prompt("open chrome", "fast", [], None, "gemma3:4b")` returns a non-empty string.
- The returned string contains the identity name ("Jarvis").
- The returned string contains the mode fragment for "fast".
- The handoff note is absent when `previous_model=None`.
- The handoff note is present when `previous_model="gemma3:4b"` and `current_model="qwen3:8b"`.

---

### TASK 5.4 — Wire prompt builder into executor

**DESCRIPTION:** Replace the stub in `executor.py` with the real prompt builder call.

**INPUT:** `DecisionOutput`, `InputPacket`.

**OUTPUT:** LLM receives the correct system prompt.

**FILES:**
- MODIFY: `src/core/runtime/executor.py`

**REQUIREMENTS:**
- Remove the stub that returned an empty string.
- Call `build_system_prompt()` with all parameters from the current decision and packet.
- Pass the built prompt as the system message in the messages list.
- Pass the tool list from `registry.to_ollama_format()` only when `decision.requires_tools=True`.

**SUCCESS CRITERIA:**
- After wiring, the LLM response demonstrates awareness of its identity (does not identify as the raw model).
- The system prompt contains the correct mode fragment for the current decision mode.

---

## 🛠️ Phase 6 — Tool System

> **End state:** Any registered skill is callable through the full pipeline: classify → registry → safety → validate → execute → ToolResult.

---

### TASK 6.1 — BaseTool abstract class

**DESCRIPTION:** Define the base class that all tools must extend.

**INPUT:** A Python class that extends `BaseTool`.

**OUTPUT:** The class is discoverable and executable.

**FILES:**
- CREATE: `src/core/tools/base.py`

**REQUIREMENTS:**
- Define `BaseTool` as an abstract class with abstract method `execute(**kwargs) → ToolResult`.
- Required class attributes: name (str), description (str), category (str), requires_confirmation (bool), platform (list[str]).
- Define `is_available()` returning `True` by default; subclasses override to check dependencies.
- Define `get_schema()` loading the JSON Schema from `config/schemas/{category}/{name}.schema.json`; return `{}` if missing.
- Define `to_ollama_format()` returning the tool in Ollama tool-calling dict format.

**SUCCESS CRITERIA:**
- A minimal subclass with `name`, `description`, `category`, and `execute()` defined can be instantiated.
- `isinstance(subclass_instance, BaseTool)` returns `True`.
- Attempting to instantiate `BaseTool()` directly raises `TypeError`.

---

### TASK 6.2 — Tool registry with auto-discovery

**DESCRIPTION:** Implement the registry that scans `src/skills/` and registers all `BaseTool` subclasses.

**INPUT:** `src/skills/` directory containing `BaseTool` subclasses.

**OUTPUT:** All available tools registered and retrievable by name.

**FILES:**
- CREATE: `src/core/tools/registry.py`

**REQUIREMENTS:**
- Define `ToolRegistry` class with `discover()`, `get(name)`, `all_names()`, `all_available()`, `to_ollama_format()`, `get_schema(name)` methods.
- `discover()` must use `pkgutil.walk_packages` to find all modules under `src/skills/`.
- `discover()` must import each module and inspect for `BaseTool` subclasses.
- `discover()` must call `is_available()` on each candidate; register only those returning `True`.
- `discover()` must be idempotent (calling it twice produces the same registry).
- Define a module-level singleton `registry`.
- Log the count of registered tools after discovery.

**SUCCESS CRITERIA:**
- `registry.discover()` finds all tools where `is_available()=True`.
- `registry.get("open_app")` returns the tool instance after discovery.
- `registry.get("nonexistent")` returns `None`.

---

### TASK 6.3 — Safety classifier

**DESCRIPTION:** Implement the function that classifies tool risk and determines execution permission.

**INPUT:** Tool name string, args dict.

**OUTPUT:** `SafetyResult` with level and allowed status.

**FILES:**
- CREATE: `src/core/tools/safety.py`

**REQUIREMENTS:**
- Define `SafetyResult` as a Pydantic model with fields: level (str), allowed (bool | None), reason (str).
- Define `classify_safety(tool_name, args) → SafetyResult`.
- `allowed=True` means auto-execute. `allowed=False` means block. `allowed=None` means ask user.
- Read risk_level for the tool from the skills manifest loaded from `config/skills.yaml`.
- Implement shell command blocklist check: scan all string values in `args` for blocked patterns.
- Blocked patterns: `rm -rf`, `format c:`, `del /s /q`, `:(){:|:&};:`, `shutdown /`, `mkfs`, `dd if=`.
- Do not hardcode tool names in this module — use the manifest exclusively.

**SUCCESS CRITERIA:**
- A tool with `risk_level: high` in BALANCED mode returns `allowed=None` (require confirmation).
- A tool with `risk_level: low` in BALANCED mode returns `allowed=True`.
- Args containing `"rm -rf"` return `allowed=False` regardless of mode.

---

### TASK 6.4 — Execution mode enforcement

**DESCRIPTION:** Apply the three-mode policy (SAFE, BALANCED, UNRESTRICTED) inside the tool executor.

**INPUT:** Current `execution_mode` from settings, `SafetyResult`.

**OUTPUT:** Decision to proceed, confirm, or block.

**FILES:**
- CREATE: `src/core/tools/mode_enforcer.py`

**REQUIREMENTS:**
- Define `should_execute(safety_result, execution_mode) → bool | "confirm"`.
  - Returns `True` to auto-execute.
  - Returns `False` to block.
  - Returns `"confirm"` to pause and ask user.
- SAFE mode: return `"confirm"` for all risk levels.
- BALANCED mode: return `True` for low, `"confirm"` for medium, `False` for high (unless explicit override phrase detected).
- UNRESTRICTED mode: return `True` for all risk levels.
- Define `is_explicit_override(user_message, tool_name) → bool` that checks if the user typed `"confirm: {tool_name}"` as their last message.

**SUCCESS CRITERIA:**
- `should_execute(SafetyResult(level="high", ...), "balanced")` returns `False`.
- `should_execute(SafetyResult(level="low", ...), "safe")` returns `"confirm"`.
- `should_execute(SafetyResult(level="high", ...), "unrestricted")` returns `True`.

---

### TASK 6.5 — Schema validator

**DESCRIPTION:** Validate tool args against the tool's JSON Schema before execution.

**INPUT:** Args dict, JSON Schema dict.

**OUTPUT:** `None` if valid, error string if invalid.

**FILES:**
- CREATE: `src/core/tools/validator.py`

**REQUIREMENTS:**
- Define `validate_args(args, schema) → str | None`.
- Check that all `required` fields are present in args.
- Check that field types match schema type declarations for: string, integer, boolean, number.
- Do not require the `jsonschema` library — implement basic required + type checks manually.
- Return a descriptive error string naming the failing field.

**SUCCESS CRITERIA:**
- Validates `{"name": "chrome"}` against a schema requiring `name: string` → returns `None`.
- Validates `{}` against a schema requiring `name` → returns an error string containing "name".
- Validates `{"name": 123}` against a schema requiring `name: string` → returns an error string.

---

### TASK 6.6 — Tool executor

**DESCRIPTION:** Implement the single execution gate for all tool calls.

**INPUT:** Tool name string, args dict.

**OUTPUT:** `ToolResult`.

**FILES:**
- CREATE: `src/core/tools/executor.py`

**REQUIREMENTS:**
- Define `execute_tool(tool_name, args) → ToolResult`.
- Pipeline in order: find tool → classify safety → apply mode enforcement → validate args → execute → return.
- If tool not found: return `ToolResult(tool=tool_name, success=False, error="Tool not found")`.
- If blocked: return `ToolResult(tool=tool_name, success=False, error="Blocked by safety policy")`.
- If user confirmation required: print confirmation prompt to terminal; if user declines: return `ToolResult(success=False, error="User declined")`.
- If validation fails: return `ToolResult(success=False, error=f"Invalid args: {validation_error}")`.
- If `tool.execute()` raises: catch the exception; return `ToolResult(success=False, error=str(exception))`.
- Log: `tool.start`, `tool.done` or `tool.error`, with duration_ms.
- Record duration_ms on the returned `ToolResult`.

**SUCCESS CRITERIA:**
- `execute_tool("open_app", {"name": "notepad"})` opens Notepad and returns `success=True`.
- `execute_tool("nonexistent", {})` returns `success=False` without raising.
- `execute_tool("delete_file", {"path": "test.txt"})` in BALANCED mode prompts for confirmation.

---

### TASK 6.7 — Tool call parser and retry

**DESCRIPTION:** Implement the parser that extracts tool call JSON from LLM output and retries on failure.

**INPUT:** Raw LLM output string, `requires_tools` bool.

**OUTPUT:** Parsed `LLMOutput`.

**FILES:**
- MODIFY: `src/core/runtime/llm_output.py`

**REQUIREMENTS:**
- Implement `parse_llm_output(raw_text, requires_tools)` as defined in Task 2.3.
- When `requires_tools=True` and parsing fails, the caller must retry the LLM call with an explicit instruction appended.
- The retry instruction must state: "You must respond with only a JSON object in the format: `{type, tool, args}`. No other text."
- Maximum retries: 2 (read from settings: `runtime.max_tool_retries`).
- After max retries, return `LLMOutput` with a parse failure indicator in the `tool` field (empty string).
- The runtime loop must check for the parse failure indicator and return a user-facing error message.

**SUCCESS CRITERIA:**
- Valid tool call JSON in raw text → `LLMOutput(type="tool_call", tool="open_app")`.
- Plain text when `requires_tools=True` → triggers retry; after max retries → parse failure indicator.
- No exception escapes from any parsing path.

---

## 🔒 Phase 7 — Safety Modes

> **End state:** Execution mode is configurable. All tool executions apply the correct policy. Risk levels are populated on all tools.

---

### TASK 7.1 — Execution mode in config

**DESCRIPTION:** Add the `execution_mode` field to settings and ensure it is read at runtime.

**INPUT:** `config/settings.yaml` with `runtime.execution_mode` set.

**OUTPUT:** `get_settings().runtime.execution_mode` returns the configured value.

**FILES:**
- MODIFY: `config/settings.example.yaml`
- MODIFY: `src/core/config.py`

**REQUIREMENTS:**
- Add `execution_mode` to the `runtime` section of the settings YAML with default `"balanced"`.
- Add `execution_mode` to the `RuntimeConfig` Pydantic model.
- Validate that the value is one of: `"safe"`, `"balanced"`, `"unrestricted"`. Reject others with a validation error.

**SUCCESS CRITERIA:**
- `get_settings().runtime.execution_mode` returns `"balanced"` with a default settings file.
- Setting `execution_mode: "invalid"` in the YAML raises a Pydantic validation error on load.

---

### TASK 7.2 — Risk levels on all tool entries

**DESCRIPTION:** Ensure every tool in `config/skills.yaml` has a correctly classified `risk_level`.

**INPUT:** `config/skills.yaml`.

**OUTPUT:** Every entry has a `risk_level` field.

**FILES:**
- MODIFY: `config/skills.yaml`

**REQUIREMENTS:**
- Add `risk_level` to every entry that lacks it.
- Classification must follow README Section 8 Risk Classification table exactly.
- No entry may have an empty or missing `risk_level`.

**SUCCESS CRITERIA:**
- Parsing the YAML and checking all entries confirms `risk_level` is present on every tool.
- `delete_file` has `risk_level: high`.
- `web_search` has `risk_level: low`.

---

### TASK 7.3 — CLI execution mode toggle

**DESCRIPTION:** Add a `/mode` slash command to change execution mode at runtime.

**INPUT:** `/mode safe` or `/mode balanced` or `/mode unrestricted` typed in CLI.

**OUTPUT:** Mode updated in settings; confirmation printed.

**FILES:**
- MODIFY: `src/interfaces/cli/commands.py`

**REQUIREMENTS:**
- Add `/mode {value}` command to the CLI command handler.
- The command must update `execution_mode` in the in-memory settings object.
- The command must print a confirmation: `"Execution mode set to: {value}"`.
- The command must reject invalid values with a message listing valid options.
- Mode change applies to all subsequent tool calls in the current session only. It does not write to the YAML file.

**SUCCESS CRITERIA:**
- Typing `/mode safe` prints confirmation and subsequent tool calls require confirmation.
- Typing `/mode invalid` prints an error listing valid modes.

---

### TASK 7.4 — Safety tests

**DESCRIPTION:** Test the three-mode policy with all risk levels.

**INPUT:** All combinations of mode and risk level.

**OUTPUT:** Correct `should_execute()` return value for each combination.

**FILES:**
- CREATE: `tests/test_safety.py`

**REQUIREMENTS:**
- Test all 9 combinations (3 modes × 3 risk levels).
- Test that blocked shell patterns block execution regardless of mode.
- No real tool execution in these tests — test `should_execute()` and `classify_safety()` in isolation.

**SUCCESS CRITERIA:**
- `pytest tests/test_safety.py` passes with 0 failures.

---

### TASK 7.5 — High-risk explicit approval flow

**DESCRIPTION:** Implement the explicit approval phrase check for high-risk tools in BALANCED mode.

**INPUT:** User message containing `"confirm: {tool_name}"`.

**OUTPUT:** High-risk tool executes without additional confirmation prompt.

**FILES:**
- MODIFY: `src/core/tools/mode_enforcer.py`

**REQUIREMENTS:**
- `is_explicit_override(user_message, tool_name)` must return `True` only when the message is exactly `"confirm: {tool_name}"` (case-insensitive).
- The runtime loop must pass the original user message to `is_explicit_override` before blocking a high-risk tool.
- If `is_explicit_override` returns `True`, treat the tool as medium-risk for this call only.

**SUCCESS CRITERIA:**
- User types `"confirm: delete_file"` → `is_explicit_override` returns `True` → tool proceeds to confirmation prompt.
- User types anything else → `is_explicit_override` returns `False` → high-risk blocked in BALANCED mode.

---

## 🖥️ Phase 8 — System Control Skills

> **End state:** All OS-level operations work correctly on Windows, Linux, and macOS.

---

### TASK 8.1 — App launcher as BaseTool

**DESCRIPTION:** Refactor the `open_app` and `close_app` functions from Phase 0 into `BaseTool` subclasses.

**INPUT:** `{"name": "notepad"}`.

**OUTPUT:** App opens. `ToolResult(success=True, data={"pid": ...})`.

**FILES:**
- MODIFY: `src/skills/system/apps.py`

**REQUIREMENTS:**
- Define `AppLauncherTool` extending `BaseTool` with `name="open_app"`.
- Define `AppCloseTool` extending `BaseTool` with `name="close_app"` and `requires_confirmation=True`.
- Define `BringToFrontTool` with `name="bring_to_front"` for Windows only.
- All existing logic from Phase 0 must be preserved and wrapped in `execute()`.
- Add `platform` list to each tool. `bring_to_front` is `["windows"]` only.
- Create JSON Schema files for each tool.

**SUCCESS CRITERIA:**
- `registry.discover()` registers `open_app` and `close_app`.
- `execute_tool("open_app", {"name": "notepad"})` opens Notepad and returns `success=True`.
- `execute_tool("close_app", {"name": "notepad"})` triggers confirmation prompt.

---

### TASK 8.2 — System information tool

**DESCRIPTION:** Implement tools to retrieve system metrics.

**INPUT:** `{}` or `{"metric": "cpu"}`.

**OUTPUT:** `ToolResult(data={"cpu_percent": ..., "ram_used_gb": ..., ...})`.

**FILES:**
- CREATE: `src/skills/system/sysinfo.py`

**REQUIREMENTS:**
- Define `SystemInfoTool` with `name="system_info"` returning CPU%, RAM used/total, disk free.
- Define `ListProcessesTool` with `name="list_processes"` returning a list of running processes.
- Define `KillProcessTool` with `name="kill_process"` and `requires_confirmation=True`.
- Use `psutil` for all metrics.
- GPU VRAM: use `pynvml` if available; skip silently if not installed.
- Cross-platform: all three tools must work on Windows, Linux, and macOS.

**SUCCESS CRITERIA:**
- `system_info()` returns a dict with at least `cpu_percent`, `ram_used_gb`, `disk_free_gb`.
- `list_processes()` returns a list with at least 5 entries.
- `kill_process()` requires confirmation before executing.

---

### TASK 8.3 — Clipboard tool

**DESCRIPTION:** Implement read and write clipboard operations.

**INPUT:** `{}` for read, `{"text": "hello"}` for write.

**OUTPUT:** `ToolResult(data={"content": "clipboard text"})` for read.

**FILES:**
- CREATE: `src/skills/system/clipboard.py`

**REQUIREMENTS:**
- Define `ReadClipboardTool` with `name="read_clipboard"`.
- Define `WriteClipboardTool` with `name="write_clipboard"`.
- Use `pyperclip` for text operations.
- If clipboard contains an image (Windows only), save to `data/temp/clipboard_image.png` and return the path.
- Return `success=False` gracefully if the clipboard is empty or unreadable.

**SUCCESS CRITERIA:**
- Copy text in any app. Call `read_clipboard()`. Returns that text.
- Call `write_clipboard({"text": "test"})`. Paste in any app. "test" appears.

---

### TASK 8.4 — Notification tool

**DESCRIPTION:** Send a system notification on Windows, Linux, and macOS.

**INPUT:** `{"title": "Done", "message": "Task complete", "type": "success"}`.

**OUTPUT:** Notification appears. `ToolResult(success=True)`.

**FILES:**
- CREATE: `src/skills/notify/toasts.py`

**REQUIREMENTS:**
- Define `SendNotificationTool` with `name="send_notification"`.
- On Windows: use `winotify`.
- On Linux: use `notify-send` via subprocess.
- On macOS: use `osascript` via subprocess.
- If the platform library is unavailable, fall back to printing to console and return `success=True` with a `fallback="console"` field in data.
- `type` must accept: info, success, warning, error.

**SUCCESS CRITERIA:**
- Notification appears within 3 seconds on the test platform.
- No exception raised on any platform, even if the native notification system is unavailable.

---

### TASK 8.5 — Screenshot and OCR tools

**DESCRIPTION:** Capture the screen and extract text using OCR.

**INPUT:** `{}` for full screen, `{"region": {"x": 0, "y": 0, "w": 800, "h": 600}}` for region.

**OUTPUT:** `ToolResult(data={"path": "data/screenshots/...", "text": "..."})`.

**FILES:**
- CREATE: `src/skills/screen/capture.py`

**REQUIREMENTS:**
- Define `ScreenshotTool` with `name="take_screenshot"` using `mss`.
- Define `OCRTool` with `name="read_screen_text"` using `pytesseract`.
- Screenshots saved to `data/screenshots/` with timestamp filename.
- OCR must specify both Arabic and English language codes for Tesseract.
- Return `success=False` if Tesseract binary is not installed, with a clear error message.

**SUCCESS CRITERIA:**
- `take_screenshot()` creates a PNG file in `data/screenshots/`.
- `read_screen_text()` on a screen with visible text returns non-empty extracted text.

---

### TASK 8.6 — File operations tools

**DESCRIPTION:** Implement all file operation tools.

**INPUT:** Operation-specific args (path, content, etc.).

**OUTPUT:** Operation-specific `ToolResult`.

**FILES:**
- CREATE: `src/skills/files/file_ops.py`

**REQUIREMENTS:**
- Define tools: `ReadFileTool`, `WriteFileTool`, `ListDirectoryTool`, `SearchFilesTool`, `MoveFileTool`, `CopyFileTool`, `DeleteFileTool`.
- `DeleteFileTool` must use `send2trash` — never `os.remove`. Set `requires_confirmation=True`.
- `WriteFileTool` must set `requires_confirmation=True` if the file already exists.
- Implement path safety: all paths must be under the user's home directory or under the configured `data/` directory. Reject paths outside these roots.
- Create JSON Schema files for each tool.

**SUCCESS CRITERIA:**
- Read a known text file. Content returned correctly.
- Write `data/test_write.txt`. File exists with correct content.
- Delete a file. File appears in system Recycle Bin (not permanently deleted).
- Attempt to read a path outside allowed roots. Returns `success=False`.

---

### TASK 8.7 — Code executor tool

**DESCRIPTION:** Execute Python code or shell commands in a controlled subprocess.

**INPUT:** `{"code": "print(2+2)"}` or `{"command": "ls"}`.

**OUTPUT:** `ToolResult(data={"stdout": "4\n", "stderr": "", "returncode": 0})`.

**FILES:**
- CREATE: `src/skills/coder/executor.py`

**REQUIREMENTS:**
- Define `RunPythonTool` with `name="execute_python"` and `requires_confirmation=True`.
- Define `RunShellTool` with `name="run_shell"` and `requires_confirmation=True`.
- Both must run in a subprocess with a configurable timeout (default 30s from settings).
- Both must check for blocked patterns before execution: `os.remove`, `shutil.rmtree`, `os.system`, `sys.exit` (Python); `rm -rf`, `format`, `del /s`, `shutdown`, `reboot` (shell).
- Capture stdout and stderr. Return both in `data`.
- On timeout: return `success=False` with error `"Timeout after {n}s"`.

**SUCCESS CRITERIA:**
- `execute_python({"code": "print(2+2)"})` returns `stdout="4\n"` and `success=True`.
- Code containing `os.remove` is blocked before subprocess is created.
- Infinite loop code is killed after timeout.

---

### TASK 8.8 — Web search tool

**DESCRIPTION:** Search the web using DuckDuckGo and return results.

**INPUT:** `{"query": "Python tutorial", "max_results": 5}`.

**OUTPUT:** `ToolResult(data={"results": [{title, url, snippet}]})`.

**FILES:**
- CREATE: `src/skills/search/web_search.py`

**REQUIREMENTS:**
- Define `WebSearchTool` with `name="web_search"`.
- Use DuckDuckGo HTML search endpoint — no API key required.
- Parse results with `BeautifulSoup`.
- Cache identical queries for 5 minutes using a module-level dict.
- Return `success=False` on network error — do not raise.

**SUCCESS CRITERIA:**
- `web_search({"query": "Python tutorial"})` returns at least 3 results with non-empty titles and URLs.
- The same query within 5 minutes returns `data.cached=True` and makes no HTTP request.

---

## 🌐 Phase 9 — Browser & Web Skills

> **End state:** Playwright browser with persistent sessions, file transfers, and WhatsApp automation.

---

### TASK 9.1 — Playwright browser core

**DESCRIPTION:** Implement browser navigation and interaction tools.

**INPUT:** `{"url": "https://example.com"}` for navigate.

**OUTPUT:** `ToolResult(data={"title": "Example Domain"})`.

**FILES:**
- CREATE: `src/skills/browser/browser.py`

**REQUIREMENTS:**
- Use a module-level singleton for the Playwright instance — not recreated per call.
- Define tools: `NavigateTool`, `ClickTool`, `FillTool`, `GetTextTool`, `BrowserScreenshotTool`.
- Register `atexit` cleanup to close the browser on exit.
- All tools must return `success=False` on Playwright exception — do not raise.

**SUCCESS CRITERIA:**
- `browser_navigate({"url": "https://example.com"})` returns `data.title="Example Domain"`.
- Browser instance persists between tool calls (singleton verified by checking instance identity).

---

### TASK 9.2 — Session persistence

**DESCRIPTION:** Save and load browser sessions so the user stays logged in between Jarvis restarts.

**INPUT:** Domain string.

**OUTPUT:** Session saved to `data/sessions/{domain}.json`; restored on next launch.

**FILES:**
- CREATE: `src/skills/browser/session.py`

**REQUIREMENTS:**
- Define `save_session(domain)` and `load_session(domain)`.
- If `SESSION_ENCRYPTION_KEY` is set in `.env`, encrypt the session file using Fernet.
- If the key is not set, save as plain JSON with a warning log.
- `load_session` returns `None` if file does not exist or decryption fails.

**SUCCESS CRITERIA:**
- Log into a test site. Save session. Restart Python. Load session. Navigate to site. Still logged in.

---

### TASK 9.3 — File download and upload

**DESCRIPTION:** Handle file downloads triggered by browser navigation, and file uploads via file input fields.

**INPUT:** Download: triggered by page. Upload: `{"selector": "#upload", "path": "data/test.txt"}`.

**OUTPUT:** `ToolResult(data={"path": "data/downloads/...", "filename": "..."})`.

**FILES:**
- CREATE: `src/skills/browser/transfer.py`

**REQUIREMENTS:**
- Intercept downloads via `page.on("download")` and save to `data/downloads/`.
- Handle filename conflicts by appending a timestamp.
- For uploads, use `page.set_input_files(selector, path)`.
- Validate that the local file path exists before attempting upload.

**SUCCESS CRITERIA:**
- Click a download link on a test page. File appears in `data/downloads/`.
- Upload a local file to a file input field. DOM reflects the upload.

---

### TASK 9.4 — Auth wall detection and pause

**DESCRIPTION:** Detect when the browser hits a login page and pause automation for the user.

**INPUT:** Current browser page state.

**OUTPUT:** Automation paused; user notified; resumes after user signals completion.

**FILES:**
- CREATE: `src/skills/browser/auth_handler.py`

**REQUIREMENTS:**
- Define `check_for_auth_wall(page) → bool` that checks URL and title for auth keywords.
- Auth keywords: login, sign in, تسجيل الدخول, captcha, verify, authenticate.
- Define `handle_auth_wall(page)` that sends a notification and blocks until user presses Enter.
- After user presses Enter, save the session for the current domain.

**SUCCESS CRITERIA:**
- Navigate to a login-required page. Notification appears. User logs in. Enter pressed. Session saved. Next navigation succeeds without login prompt.

---

### TASK 9.5 — WhatsApp Web automation

**DESCRIPTION:** Send messages and read conversations through WhatsApp Web.

**INPUT:** `{"action": "send", "contact": "Ahmed", "message": "Hello"}`.

**OUTPUT:** `ToolResult(success=True)` and message visible in WhatsApp Web.

**FILES:**
- CREATE: `src/skills/social/whatsapp.py`

**REQUIREMENTS:**
- Define `WhatsAppSendTool` and `WhatsAppReadTool`.
- Load session for `web.whatsapp.com` on first use.
- If session missing or expired: take screenshot of QR code, display in terminal, wait for scan, save session.
- Find contact via WhatsApp search. Send message via keyboard input.
- `WhatsAppSendTool` has `risk_level: medium`.

**SUCCESS CRITERIA:**
- Command "send Ahmed: Meeting at 3pm" → message visible in WhatsApp Web contact chat.

---

### TASK 9.6 — Session manager integration

**DESCRIPTION:** Wire session loading into the browser singleton so all browser tools use sessions automatically.

**INPUT:** Domain of the current page.

**OUTPUT:** Browser context initialized with saved session if available.

**FILES:**
- MODIFY: `src/skills/browser/browser.py`

**REQUIREMENTS:**
- When creating the browser page for a domain, call `load_session(domain)`.
- If session loaded: initialize context with `storage_state` from the session.
- If no session: create default context.
- After each successful navigation, call `save_session(domain)` to keep session fresh.

**SUCCESS CRITERIA:**
- Login to a test site. Restart Jarvis. Navigate to the same site. No login prompt.

---

## 🔌 Phase 10 — Google APIs

> **End state:** Single OAuth consent flow provides access to Calendar, Gmail, Drive, Contacts, and YouTube.

---

### TASK 10.1 — Unified Google OAuth

**DESCRIPTION:** Implement a single OAuth manager for all Google APIs.

**INPUT:** `credentials.json` from Google Cloud Console.

**OUTPUT:** `data/google_token.json` saved; token auto-refreshes.

**FILES:**
- CREATE: `src/skills/api/google_auth.py`

**REQUIREMENTS:**
- Use combined scopes covering: Calendar, Gmail, Drive, Contacts, YouTube.
- On first run: open browser for consent, save token.
- On subsequent runs: load token, refresh silently if expired.
- If refresh fails: trigger consent flow again.
- Token path: `data/google_token.json`. This file must be gitignored.

**SUCCESS CRITERIA:**
- First run: browser opens → consent → token saved.
- Second run: no browser → token loaded → API call succeeds.

---

### TASK 10.2 — Google Calendar

**DESCRIPTION:** Implement Calendar CRUD tools.

**INPUT:** Tool-specific args.

**OUTPUT:** `ToolResult` with event data or operation confirmation.

**FILES:**
- CREATE: `src/skills/api/calendar.py`

**REQUIREMENTS:**
- Define: `CalendarListTool`, `CalendarCreateTool`, `CalendarUpdateTool`, `CalendarDeleteTool`, `CalendarSearchTool`.
- `CalendarDeleteTool` has `risk_level: medium`.
- All tools call `get_google_credentials()` on each use — credentials auto-refresh.

**SUCCESS CRITERIA:**
- Create event → list → found → delete → list → gone.

---

### TASK 10.3 — Gmail

**DESCRIPTION:** Implement Gmail send, read, and management tools.

**INPUT:** Tool-specific args.

**OUTPUT:** `ToolResult` with message data or operation confirmation.

**FILES:**
- CREATE: `src/skills/api/gmail.py`

**REQUIREMENTS:**
- Define: `GmailListTool`, `GmailSearchTool`, `GmailSendTool`, `GmailReplyTool`, `GmailMarkTool`, `GmailMoveTool`.
- `GmailSendTool` and `GmailReplyTool` have `risk_level: high`.

**SUCCESS CRITERIA:**
- Send email to self → found in inbox → mark read → unread count decreases.

---

### TASK 10.4 — Google Drive

**DESCRIPTION:** Implement Drive file management tools.

**INPUT:** Tool-specific args.

**OUTPUT:** `ToolResult` with file data or transfer confirmation.

**FILES:**
- CREATE: `src/skills/api/drive.py`

**REQUIREMENTS:**
- Define: `DriveListTool`, `DriveSearchTool`, `DriveUploadTool`, `DriveDownloadTool`, `DriveShareTool`, `DriveCreateFolderTool`.
- `DriveShareTool` has `risk_level: medium`.

**SUCCESS CRITERIA:**
- Upload file → list → found → download → content matches original.

---

### TASK 10.5 — Google Contacts

**DESCRIPTION:** Implement Contacts search and name resolution.

**INPUT:** `{"action": "search", "query": "Ahmed"}`.

**OUTPUT:** `ToolResult(data={"contacts": [{"name": "...", "email": "..."}]})`.

**FILES:**
- CREATE: `src/skills/api/contacts.py`

**REQUIREMENTS:**
- Define: `ContactsListTool`, `ContactsSearchTool`, `ContactsGetTool`, `ContactsCreateTool`.
- Define `resolve_name(name) → str | None` returning email for a given display name.
- `resolve_name` is used by Gmail tools when `to` field contains a name instead of an email.

**SUCCESS CRITERIA:**
- `contacts_search({"query": "Ahmed"})` returns matching contact with email.
- "Send email to Ahmed about the meeting" → Gmail resolves Ahmed's email via Contacts.

---

### TASK 10.6 — YouTube

**DESCRIPTION:** Implement YouTube search and video info tools.

**INPUT:** `{"query": "machine learning tutorial", "max_results": 5}`.

**OUTPUT:** `ToolResult(data={"videos": [{title, url, duration, views}]})`.

**FILES:**
- CREATE: `src/skills/api/youtube.py`

**REQUIREMENTS:**
- Define: `YouTubeSearchTool`, `YouTubeGetInfoTool`, `YouTubeOpenTool`.
- `YouTubeOpenTool` opens the video URL in the default browser.

**SUCCESS CRITERIA:**
- Search returns 5 results with valid YouTube URLs.
- Open tool opens the URL in the browser.

---

### TASK 10.7 — PDF and Office readers

**DESCRIPTION:** Implement document reading and writing tools.

**INPUT:** File path.

**OUTPUT:** Extracted text or structured data.

**FILES:**
- CREATE: `src/skills/pdf/reader.py`
- CREATE: `src/skills/office/reader.py`

**REQUIREMENTS:**
- PDF: `PdfReadTextTool` (pdfplumber), `PdfSummarizeTool` (LLM-assisted, chunked).
- Office: `DocxReadTool`, `XlsxReadTool`, `PptxReadTool`, `DocxWriteTool`, `XlsxWriteTool`.
- All read tools return the extracted content as a string or structured dict.
- Write tools have `requires_confirmation=True`.

**SUCCESS CRITERIA:**
- Read a multi-page PDF. Non-empty text returned.
- Read a .docx file. Text content returned.
- Create a .docx with one paragraph. File exists and is readable by Word.

---

## 💾 Phase 11 — Context + Memory

> **End state:** Facts from session 1 are recalled in session 2. Every turn auto-saves.

---

### TASK 11.1 — Short-term memory

**DESCRIPTION:** Implement Redis-backed session history with in-memory fallback.

**INPUT:** Role and content strings.

**OUTPUT:** Message saved; retrievable by session ID.

**FILES:**
- CREATE: `src/core/memory/short_term.py`

**REQUIREMENTS:**
- Define `save_message(session_id, role, content)`.
- Define `get_history(session_id, n=10) → list[dict]`.
- Use Redis if available; fall back to module-level dict on connection failure.
- Log a warning (not error) when falling back to in-memory.
- Maximum 50 messages per session; trim oldest when exceeded.
- Redis TTL: 24 hours per session key.

**SUCCESS CRITERIA:**
- Save 3 messages. Get history. 3 returned in order.
- With Redis: restart Python. History still present.
- Without Redis: no crash; in-memory history works.

---

### TASK 11.2 — Long-term semantic memory

**DESCRIPTION:** Implement ChromaDB-backed semantic search.

**INPUT:** Text string and metadata dict.

**OUTPUT:** Stored; retrievable by semantic query.

**FILES:**
- CREATE: `src/core/memory/long_term.py`

**REQUIREMENTS:**
- Define `remember(text, metadata)`.
- Define `recall(query, n=5) → list[str]`.
- Use `all-MiniLM-L6-v2` embeddings via `sentence-transformers`.
- Persist to `data/chroma/` directory.

**SUCCESS CRITERIA:**
- `remember("User prefers concise responses")`. Restart Python. `recall("user style preferences")` returns that text in top results.

---

### TASK 11.3 — SQLite structured store

**DESCRIPTION:** Implement SQLite-backed structured storage for conversations and metadata.

**INPUT:** SQL operations via wrapper functions.

**OUTPUT:** Data persists across restarts.

**FILES:**
- CREATE: `src/core/memory/database.py`

**REQUIREMENTS:**
- Define tables: conversations, feedback, tasks, routing_weights.
- Auto-create tables on first connection.
- Define CRUD functions for each table.
- Use parameterized queries throughout — no string formatting in SQL.
- Database path from `get_settings().paths.sqlite`.

**SUCCESS CRITERIA:**
- Insert row in each table. Restart. All rows present.

---

### TASK 11.4 — Memory injection into Context assembler

**DESCRIPTION:** Wire memory retrieval into `assemble_context()`.

**INPUT:** User message and session ID.

**OUTPUT:** `InputPacket` with `memory_snippets` and `recent_history` populated.

**FILES:**
- MODIFY: `src/core/context/assembler.py`

**REQUIREMENTS:**
- Replace the empty list stubs from Phase 3 with real calls:
  - `get_history(session_id, n=10)` → `recent_history`.
  - `recall(user_message, n=3)` → `memory_snippets`.
- If Redis or ChromaDB is unavailable, `assemble_context` still returns a valid `InputPacket` (empty lists for unavailable sources).

**SUCCESS CRITERIA:**
- After telling Jarvis "my name is Ahmed" in turn 1, turn 2 "what is my name?" returns "Ahmed" without explicit repetition.

---

### TASK 11.5 — Auto-save after every turn

**DESCRIPTION:** Save each turn's interaction to all memory backends automatically.

**INPUT:** Completed turn (user message, response, session ID, decision metadata).

**OUTPUT:** All backends updated.

**FILES:**
- MODIFY: `src/core/runtime/loop.py`

**REQUIREMENTS:**
- After every `run_turn()` completion, call:
  - `save_message(session_id, "user", user_input)`
  - `save_message(session_id, "assistant", response.text)`
  - `insert_conversation(session_id, "user", user_input)`
  - `insert_conversation(session_id, "assistant", response.text)`
- If response quality > 0.8: call `remember(f"[{decision.intent}] '{user_input[:80]}' received positive response", metadata)`.
- Memory saves must not block the response — use `asyncio.create_task` or a background thread.

**SUCCESS CRITERIA:**
- After 5 turns, SQLite `conversations` table has 10 rows.
- Good-quality responses appear in ChromaDB after the turn.

---

### TASK 11.6 — Feedback collection

**DESCRIPTION:** Collect implicit and explicit feedback signals and save to the database.

**INPUT:** Turn outcome, evaluator result, explicit user rating.

**OUTPUT:** Feedback row inserted in SQLite.

**FILES:**
- CREATE: `src/core/memory/feedback.py`

**REQUIREMENTS:**
- Define `record_feedback(session_id, model, mode, intent, score)`.
- Implicit signals: evaluator quality score → record after each turn.
- Explicit: `/thumbsup` and `/thumbsdown` CLI commands set score to 1.0 and 0.0 respectively.
- Trigger weight recalculation every 20 turns.
- Privacy: define `disable_feedback(session_id)` and `clear_all_feedback()`.

**SUCCESS CRITERIA:**
- After 5 turns, 5 rows appear in the feedback table.
- `/thumbsup` inserts a row with score=1.0.

---

## 🤖 Phase 12 — Agents

> **End state:** Multi-step goals execute without step-by-step user guidance.

---

### TASK 12.1 — Thinker agent

**DESCRIPTION:** Implement chain-of-thought reasoning with self-critique.

**INPUT:** Question string.

**OUTPUT:** Higher-quality answer than a direct LLM call.

**FILES:**
- CREATE: `src/core/agents/thinker.py`

**REQUIREMENTS:**
- Define `think(question, model) → str`.
- Use a system prompt that instructs: reason step-by-step, self-critique, then provide final answer after a delimiter.
- Extract only the final answer from the response.
- Fall back to full response if delimiter not found.

**SUCCESS CRITERIA:**
- `think("What are the trade-offs between SQL and NoSQL?")` returns a more complete answer than `chat("What are the trade-offs between SQL and NoSQL?")`.
- Measured by: response contains at least 3 distinct points.

---

### TASK 12.2 — Planner agent

**DESCRIPTION:** Decompose a multi-step goal into an ordered list of steps.

**INPUT:** Goal string, list of available tool names.

**OUTPUT:** List of Step objects with tool assignments.

**FILES:**
- CREATE: `src/core/agents/planner.py`

**REQUIREMENTS:**
- Define `Step` as a Pydantic model: id, description, tool (str|None), args (dict), depends_on (list[str]).
- Define `plan(goal, available_tools) → list[Step]`.
- Use `qwen3:8b` in planning mode.
- Parse the LLM response as a JSON list of steps.
- Return an empty list on parse failure — do not raise.

**SUCCESS CRITERIA:**
- `plan("search AI news and save a summary to a file", ["web_search", "write_file"])` returns at least 2 steps in dependency order.

---

### TASK 12.3 — Step executor

**DESCRIPTION:** Execute a list of Steps, passing outputs between dependent steps.

**INPUT:** `list[Step]`.

**OUTPUT:** Dict of step results.

**FILES:**
- CREATE: `src/core/agents/step_executor.py`

**REQUIREMENTS:**
- Execute steps in topological order (dependencies first).
- For each step: if `step.tool` is set, call `execute_tool(step.tool, resolved_args)`.
- Inject prior step results into args using `$step_id.field` placeholder syntax.
- Stop on first failure; return results so far with failure details.

**SUCCESS CRITERIA:**
- 3-step plan (search → summarize → save) executes all three steps. File created with search content.

---

### TASK 12.4 — Researcher agent

**DESCRIPTION:** Perform multi-source web research and produce a summary report.

**INPUT:** Topic string.

**OUTPUT:** Markdown report string.

**FILES:**
- CREATE: `src/core/agents/researcher.py`

**REQUIREMENTS:**
- Generate 3 distinct search queries from the topic using an LLM call.
- Execute each search query.
- Fetch top result page content for each query.
- Summarize all sources into a single Markdown report using an LLM call.
- Include source URLs in the report.

**SUCCESS CRITERIA:**
- `research("local AI models 2025")` returns a Markdown string containing content from at least 2 distinct domains.

---

### TASK 12.5 — Computer use agent

**DESCRIPTION:** Autonomously control the screen to accomplish a goal.

**INPUT:** Goal string.

**OUTPUT:** Goal accomplished or failure message.

**FILES:**
- CREATE: `src/core/agents/computer_use.py`

**REQUIREMENTS:**
- Loop: take screenshot → describe (OCR first; LLaVA if semantic understanding needed) → ask LLM for next action → execute via `pyautogui` → repeat.
- Maximum 10 iterations from settings.
- Every action requires user confirmation in BALANCED mode.
- Maintain an audit log of all actions taken.

**SUCCESS CRITERIA:**
- Goal "open Notepad and type hello" → Notepad opens → "hello" typed → success returned.

---

## 💻 Phase 13 — CLI Interface

> **End state:** Rich terminal chat with streaming, Arabic RTL, slash commands, and hotkeys.

---

### TASK 13.1 — Rich chat loop

**DESCRIPTION:** Implement the terminal chat interface.

**INPUT:** Text typed at terminal prompt.

**OUTPUT:** Streaming response displayed in Rich formatting.

**FILES:**
- CREATE: `src/interfaces/cli/interface.py`

**REQUIREMENTS:**
- Define `run_cli(cfg)`.
- Use `rich.live.Live` for streaming display.
- Detect Arabic text (>30% Arabic characters) and set text justification to right.
- Handle `/` prefix to route to command handler.
- Handle `KeyboardInterrupt` cleanly (print goodbye, exit without traceback).

**SUCCESS CRITERIA:**
- Arabic message → response displayed with RTL alignment.
- Streaming shows tokens progressively.
- Ctrl+C exits cleanly.

---

### TASK 13.2 — Slash commands

**DESCRIPTION:** Implement all CLI slash commands.

**INPUT:** Command string starting with `/`.

**OUTPUT:** Command-specific output.

**FILES:**
- CREATE: `src/interfaces/cli/commands.py`

**REQUIREMENTS:**
- Implement: `/clear`, `/model`, `/mode`, `/memory`, `/tools`, `/status`, `/profile`, `/help`, `/thumbsup`, `/thumbsdown`.
- `/mode` updates `execution_mode` from Phase 7.
- `/thumbsup` and `/thumbsdown` call `record_feedback()` from Phase 11.
- Each command must print a clear result message.
- Unknown commands must print "Unknown command. Type /help for list."

**SUCCESS CRITERIA:**
- All listed commands execute without error.
- `/mode invalid` prints error listing valid values.
- `/mode safe` changes mode; subsequent tool call requires confirmation.

---

### TASK 13.3 — Global hotkeys

**DESCRIPTION:** Register system-wide keyboard shortcuts.

**INPUT:** Hotkey combinations from config.

**OUTPUT:** Shortcuts active system-wide while Jarvis is running.

**FILES:**
- CREATE: `src/interfaces/cli/hotkeys.py`

**REQUIREMENTS:**
- Register hotkeys from `get_settings().hotkeys`.
- Use `keyboard` library on Windows, `pynput` on Linux/macOS.
- Hotkey registration must run in a background thread — not block the main loop.
- Registration failure must log a warning, not crash.

**SUCCESS CRITERIA:**
- Ctrl+Alt+J (or configured key) brings CLI to focus from another window.

---

### TASK 13.4 — Input history

**DESCRIPTION:** Persist and navigate command history across sessions.

**INPUT:** Up/down arrow keys in terminal.

**OUTPUT:** Previous inputs recalled.

**FILES:**
- MODIFY: `src/interfaces/cli/interface.py`

**REQUIREMENTS:**
- Save each user input to `data/cli_history.txt`.
- Support arrow key navigation using `prompt_toolkit` or readline.
- Maximum 500 entries in history file.

**SUCCESS CRITERIA:**
- Type 3 messages. Press up arrow 3 times. All 3 recalled in reverse order. History present after restart.

---

### TASK 13.5 — Status bar

**DESCRIPTION:** Display current system state below the chat area.

**INPUT:** State after each turn completion.

**OUTPUT:** One-line status bar showing model, mode, execution_mode, and turn count.

**FILES:**
- MODIFY: `src/interfaces/cli/interface.py`

**REQUIREMENTS:**
- Display after each response: `[model: qwen3:8b] [mode: normal] [safety: balanced] [turn: 5]`.
- Update after every turn.

**SUCCESS CRITERIA:**
- Status bar shows correct values after each response.
- Changing mode via `/mode` updates the status bar on next turn.

---

## 🌐 Phase 14 — Web UI

> **End state:** Glassmorphism chat interface in browser with streaming, file upload, conversation management, and dashboard.

---

### TASK 14.1 — FastAPI application and WebSocket endpoint

**DESCRIPTION:** Create the web server and WebSocket connection for real-time chat.

**INPUT:** Browser connects to `http://localhost:8080`.

**OUTPUT:** Chat page served; messages stream via WebSocket.

**FILES:**
- CREATE: `src/interfaces/web/app.py`
- CREATE: `src/interfaces/web/ws.py`
- CREATE: `app/server.py`

**REQUIREMENTS:**
- Define FastAPI app with static files and Jinja2 templates.
- WebSocket endpoint at `/ws/{session_id}`.
- WebSocket must receive `{"message": str, "mode": str}` and stream tokens back as `{"type": "token", "data": str}`.
- Send `{"type": "done"}` when streaming completes.
- Handle `WebSocketDisconnect` gracefully — log, do not raise.
- Support multiple concurrent sessions (multiple browser tabs).

**SUCCESS CRITERIA:**
- Navigate to `http://localhost:8080`. Page loads.
- Send message. Tokens stream to the browser and display progressively.

---

### TASK 14.2 — HTML document structure

**DESCRIPTION:** Create the single-page HTML document for the chat interface.

**INPUT:** Browser request for `/`.

**OUTPUT:** HTML document with all required DOM elements.

**FILES:**
- CREATE: `src/interfaces/web/templates/index.html`

**REQUIREMENTS:**
- Required elements by ID: `sidebar`, `search-bar`, `conversation-list`, `settings-btn`, `main`, `header`, `model-indicator`, `messages`, `input-bar`, `attach-btn`, `mode-selector`, `message-input`, `send-btn`, `settings-panel`, `toast-container`, `dashboard`.
- Load CSS from `/static/style.css` and JS from `/static/chat.js`.
- Load external libraries via CDN: marked.js (Markdown), highlight.js (syntax), KaTeX (math).
- No inline JavaScript.
- No inline styles.

**SUCCESS CRITERIA:**
- All listed IDs present in DOM (verifiable with browser DevTools).
- No console errors on page load.

---

### TASK 14.3 — CSS design system

**DESCRIPTION:** Implement the complete glassmorphism design system.

**INPUT:** Nothing — this is the stylesheet.

**OUTPUT:** All UI components styled correctly in dark and light themes.

**FILES:**
- CREATE: `src/interfaces/web/static/style.css`

**REQUIREMENTS:**
- Define all CSS custom properties (variables) for: colors, blur values, gradients, radius, fonts, shadows.
- Dark theme variables: `--bg-primary: #0a0a1a`, `--glass-bg: rgba(255,255,255,0.05)`, accent gradient blue→teal.
- Light theme: override variables under `[data-theme="light"]`.
- Glassmorphism class `.glass`: `backdrop-filter: blur(16px)` + rgba background + border.
- Sidebar: fixed width 280px, collapsible via `.collapsed` class.
- Messages: user bubble (gradient background), assistant bubble (glass panel).
- Typing indicator: three-dot animation.
- Message entry animation: fade + scale from below.
- Mode buttons: row with active state highlighted.
- Send button: round gradient with hover glow.
- Toast notifications: positioned top-right, color-coded by type.
- Dashboard stat cards: glass panel with label and value.
- Responsive: on viewport < 768px, sidebar overlays full width.

**SUCCESS CRITERIA:**
- Dark theme renders correctly in Chrome and Firefox.
- Light theme switches correctly when `data-theme` attribute changes.
- Message bubbles visually distinct (user vs assistant).
- No horizontal scroll at any viewport width.

---

### TASK 14.4 — JavaScript: WebSocket and chat core

**DESCRIPTION:** Implement WebSocket connection, message sending, and token streaming display.

**INPUT:** User types a message and presses Enter or clicks send.

**OUTPUT:** Message appears in chat. Response streams token by token.

**FILES:**
- CREATE: `src/interfaces/web/static/chat.js`

**REQUIREMENTS:**
- Connect WebSocket on page load. Reconnect on close with exponential backoff (1s, 2s, 4s, max 30s).
- Detect Arabic text (>30% Arabic chars) → set `direction: rtl` on message element.
- Token streaming: append each token to the active assistant message element as it arrives.
- Show typing indicator (three dots) while waiting for first token.
- Hide typing indicator when first token arrives.
- `send_btn` shows mic icon when input is empty; switches to arrow icon when user types.
- Mode selector: clicking a mode button sets it as active; sends mode with next message.
- Enter key sends message. Shift+Enter inserts newline.

**SUCCESS CRITERIA:**
- Arabic message → assistant response displays RTL.
- Streaming shows tokens appearing progressively.
- Mode selector updates active mode visually and functionally.

---

### TASK 14.5 — JavaScript: Markdown, code, and math rendering

**DESCRIPTION:** Render Markdown, code syntax highlighting, and math in assistant messages.

**INPUT:** Markdown-formatted text in assistant response.

**OUTPUT:** Rendered HTML with styled code blocks and math.

**FILES:**
- MODIFY: `src/interfaces/web/static/chat.js`

**REQUIREMENTS:**
- Use `marked.js` to parse assistant message content as Markdown before inserting into DOM.
- After Markdown parse, apply `highlight.js` to all `code` elements within the message.
- Add a "Copy" button to each code block. Button shows "Copied!" for 2 seconds after click.
- Render KaTeX for `$...$` (inline) and `$$...$$` (block) math expressions.

**SUCCESS CRITERIA:**
- Response with markdown headings, bold, lists, and code block renders correctly.
- Code block has syntax colors and Copy button.
- Math expression `$E=mc^2$` renders as formatted equation.

---

### TASK 14.6 — JavaScript: Attachment system

**DESCRIPTION:** Allow file and image attachments before sending a message.

**INPUT:** File selected via "+" menu, drag-and-drop, or Ctrl+V paste.

**OUTPUT:** Attachment preview card above input bar. Attachment sent with message.

**FILES:**
- MODIFY: `src/interfaces/web/static/chat.js`

**REQUIREMENTS:**
- "+" button opens a menu with options: Upload File, Upload Image.
- Drag-and-drop anywhere on the chat area attaches the file.
- Ctrl+V with an image on the clipboard attaches it.
- Each attachment shows a preview card with filename, type icon, size, and a remove (×) button.
- On send: upload file to `/api/upload` → receive `{id, name, type, size}` → include in WebSocket message.
- Image attachments show a thumbnail preview.

**SUCCESS CRITERIA:**
- Drag a file onto chat area. Preview card appears.
- Send message with attachment. Server receives the attachment ID.
- Remove button removes the attachment from the preview strip.

---

### TASK 14.7 — JavaScript: Sidebar and conversation management

**DESCRIPTION:** Display and manage conversation history in the sidebar.

**INPUT:** User interaction with sidebar elements.

**OUTPUT:** Conversations listed, searchable, manageable.

**FILES:**
- MODIFY: `src/interfaces/web/static/chat.js`

**REQUIREMENTS:**
- Load conversation list from `/api/conversations` on page load.
- Group conversations by date: Today, Yesterday, Previous 7 days, Previous 30 days, Older.
- New Chat button: generate new session ID, clear message area.
- Click conversation: load messages from `/api/conversations/{id}`.
- Inline rename: click title → contenteditable → Enter to save → PUT request.
- Delete: confirm dialog → DELETE request → remove from list.
- Pin: toggle → re-sort list (pinned at top).
- Search: Ctrl+K focuses search bar → filter by title (instant, client-side).

**SUCCESS CRITERIA:**
- Create, rename, pin, and delete conversations all work.
- Pinned conversation stays at top after page reload (persisted server-side).
- Search filters list instantly as user types.

---

### TASK 14.8 — JavaScript: Settings panel

**DESCRIPTION:** Implement the settings panel with all configuration options.

**INPUT:** User interaction with settings controls.

**OUTPUT:** Settings applied immediately and persisted.

**FILES:**
- MODIFY: `src/interfaces/web/static/chat.js`

**REQUIREMENTS:**
- Settings panel opens/closes via gear icon.
- Sections: Appearance (theme, font size, blur, animations), Behavior (default mode, language, enter key), Model (selector, temperature), Data (export JSON, clear conversations, clear memory).
- Theme toggle: dark/light — applies immediately by toggling `data-theme` attribute.
- All settings persisted to `localStorage`.
- Settings loaded from `localStorage` on page load.

**SUCCESS CRITERIA:**
- Toggle dark/light → changes immediately without reload.
- Reload page → settings restored from storage.
- Export conversations downloads a JSON file.

---

### TASK 14.9 — REST API routes

**DESCRIPTION:** Implement all HTTP endpoints used by the Web UI JavaScript.

**INPUT:** HTTP requests from browser.

**OUTPUT:** JSON responses.

**FILES:**
- CREATE: `src/interfaces/web/routes.py`

**REQUIREMENTS:**
- Implement all endpoints:
  - `GET /api/conversations` → paginated list
  - `GET /api/conversations/{id}` → messages
  - `PUT /api/conversations/{id}` → update title, pin, archive
  - `DELETE /api/conversations/{id}` → delete
  - `DELETE /api/memory` → clear session memory
  - `POST /api/upload` → file upload → returns `{id, name, type, size}`
  - `GET /api/settings`, `PUT /api/settings` → user settings CRUD
  - `GET /api/status` → active model, VRAM usage, active tool, CPU%, RAM%
  - `POST /api/feedback` → record thumbs up/down
- All endpoints return JSON. Use correct HTTP status codes (200, 400, 404).

**SUCCESS CRITERIA:**
- All endpoints return correct HTTP status codes.
- Conversation CRUD works end-to-end.
- `/api/status` returns a valid dict with at least `model` and `mode` fields.

---

### TASK 14.10 — Connection status and error handling

**DESCRIPTION:** Display connection status and handle errors gracefully in the UI.

**INPUT:** WebSocket connection state changes.

**OUTPUT:** Status indicator updates; errors shown as toasts.

**FILES:**
- MODIFY: `src/interfaces/web/static/chat.js`

**REQUIREMENTS:**
- Connection status indicator in header: green (connected), yellow (reconnecting), red (offline).
- When offline: disable input bar and show "Reconnecting..." text.
- When reconnected: re-enable input bar and show "Connected" toast.
- Message send failure: show error toast with retry button.
- Toast system: success (green), error (red), info (blue), warning (orange). Auto-dismiss after 4 seconds.

**SUCCESS CRITERIA:**
- Stop server. Yellow dot + "Reconnecting..." shown immediately.
- Restart server. Green dot restored within reconnect interval.
- Error from server received as WebSocket message → error toast shown.

---

### TASK 14.11 — Dashboard panel

**DESCRIPTION:** Display live system metrics above the chat area.

**INPUT:** `/api/status` polled every 3 seconds.

**OUTPUT:** Live stat cards with current values.

**FILES:**
- MODIFY: `src/interfaces/web/static/chat.js`

**REQUIREMENTS:**
- Poll `/api/status` every 3 seconds.
- Display: VRAM used/total (with progress bar), active model, active tool, CPU%, RAM%.
- VRAM bar color: green < 70%, amber 70-90%, red > 90%.
- Dashboard is collapsible (click to hide/show).

**SUCCESS CRITERIA:**
- Dashboard updates every 3 seconds.
- VRAM bar fills proportionally to actual usage.
- While a tool runs, "Active Tool" shows the tool name.

---

### TASK 14.12 — Feedback and message actions

**DESCRIPTION:** Add per-message feedback and action buttons.

**INPUT:** User hovers over a message; clicks an action.

**OUTPUT:** Action executes; feedback recorded.

**FILES:**
- MODIFY: `src/interfaces/web/static/chat.js`

**REQUIREMENTS:**
- Actions visible on hover for each message.
- Assistant messages: 👍, 👎, Copy, Regenerate.
- User messages: Edit.
- 👍/👎 → POST to `/api/feedback`.
- Copy → copies message text to clipboard; shows "Copied!" briefly.
- Regenerate → resends the user message; replaces the assistant response.
- Edit → makes user message editable; resubmits on Enter.

**SUCCESS CRITERIA:**
- Click 👍 → feedback recorded → button highlighted.
- Click Copy → message text in clipboard.
- Click Regenerate → new response replaces old.

---

## 🎙️ Phase 15 — Voice Pipeline

> **End state:** "Hey Jarvis" → speech command → spoken response.

---

### TASK 15.1 — Whisper STT

**DESCRIPTION:** Implement speech-to-text using Whisper.

**INPUT:** Audio from microphone (numpy array).

**OUTPUT:** `{"text": "open chrome", "language": "ar"}`.

**FILES:**
- CREATE: `src/models/speech/stt.py`

**REQUIREMENTS:**
- Define `load_model(size)` that loads and caches the Whisper model.
- Define `record_audio(duration)` capturing from the default microphone via `sounddevice`.
- Define `transcribe(audio_array) → dict` with `text` and `language` fields.
- Model size from settings: default `"medium"`.
- Do not reload the model on each call — cache after first load.

**SUCCESS CRITERIA:**
- 5 seconds of Arabic speech → correct Arabic transcription.
- 5 seconds of English speech → correct English transcription.

---

### TASK 15.2 — Piper TTS

**DESCRIPTION:** Implement text-to-speech using Piper.

**INPUT:** Text string, language string.

**OUTPUT:** Audio played through speakers.

**FILES:**
- CREATE: `src/models/speech/tts.py`

**REQUIREMENTS:**
- Define `load_voice(language)` loading the appropriate Piper ONNX voice file.
- Define `synthesize(text, language) → bytes` returning audio bytes.
- Define `speak(text, language)` playing audio via `sounddevice`.
- Arabic voice: `ar_JO-kareem-medium.onnx`.
- Auto-select voice based on `is_arabic(text)` detection.

**SUCCESS CRITERIA:**
- `speak("مرحباً", "ar")` produces audible Arabic speech.
- `speak("Hello", "en")` produces audible English speech.

---

### TASK 15.3 — Wake word detection

**DESCRIPTION:** Detect "Hey Jarvis" from continuous microphone input.

**INPUT:** Continuous audio stream.

**OUTPUT:** Event emitted when wake word detected.

**FILES:**
- CREATE: `src/interfaces/voice/wake_word.py`

**REQUIREMENTS:**
- Load openWakeWord `hey_jarvis` model.
- Run detection on 1280-sample audio chunks.
- Emit `bus.emit("wake_word.detected", {})` when score > 0.5.
- Run in a daemon thread — does not block the main loop.

**SUCCESS CRITERIA:**
- "Hey Jarvis" spoken → event fires within 1 second.
- Random speech for 60 seconds → no false triggers.

---

### TASK 15.4 — Voice Activity Detection

**DESCRIPTION:** Auto-stop recording when the user stops speaking.

**INPUT:** Microphone audio stream.

**OUTPUT:** Audio segment ending at speech boundary.

**FILES:**
- CREATE: `src/interfaces/voice/vad.py`

**REQUIREMENTS:**
- Use `webrtcvad` at aggressiveness level 2.
- Stop recording after 1 second of continuous silence.
- Minimum recording length: 0.5 seconds.
- Maximum recording length: configurable from settings.

**SUCCESS CRITERIA:**
- Speak 3 seconds then pause 1 second → recording stops at that boundary.
- Short phrase + pause → captured correctly.

---

### TASK 15.5 — Full voice pipeline

**DESCRIPTION:** Assemble the complete voice interaction loop.

**INPUT:** Wake word detected.

**OUTPUT:** Spoken response played to user.

**FILES:**
- CREATE: `src/interfaces/voice/pipeline.py`

**REQUIREMENTS:**
- Define `run_voice_pipeline(cfg)`.
- Loop: wait for wake word → play confirmation chime → record with VAD → transcribe → `run_turn()` → speak response.
- After speaking, return to listening state.
- Session ID persists across voice turns for the same session.

**SUCCESS CRITERIA:**
- "Hey Jarvis, what is the capital of France?" → "Paris" (or equivalent) spoken within 15 seconds.

---

## 👁️ Phase 16 — Vision + Image Generation

> **End state:** Images described in Arabic. Images generated from text prompts.

---

### TASK 16.1 — LLaVA image understanding

**DESCRIPTION:** Describe images using the LLaVA model.

**INPUT:** Image file path, question string.

**OUTPUT:** Text description string.

**FILES:**
- CREATE: `src/models/vision/llava.py`

**REQUIREMENTS:**
- Define `describe_image(image_path, question) → str`.
- Encode image as base64 before passing to Ollama.
- Call `swap_to("llava:7b")` before the model call; restore previous model after.
- Return a fallback message if the model call fails.

**SUCCESS CRITERIA:**
- Upload a screenshot of code → LLaVA identifies the language and describes what the code does.

---

### TASK 16.2 — Stable Diffusion image generation

**DESCRIPTION:** Generate images from text prompts using Stable Diffusion 1.5.

**INPUT:** Prompt string (any language).

**OUTPUT:** PNG file saved to `data/generated/`; path returned.

**FILES:**
- CREATE: `src/models/diffusion/sd.py`

**REQUIREMENTS:**
- Define `generate_image(prompt, steps, width, height) → str` (file path).
- Translate Arabic prompts to English via LLM before generation.
- Unload the current LLM via `unload_current_model()` before loading SD.
- Delete the pipeline and call `torch.cuda.empty_cache()` after generation.
- Save output to `data/generated/image_{timestamp}.png`.

**SUCCESS CRITERIA:**
- `generate_image("a sunset over the Nile")` → PNG file created and path returned.
- Arabic prompt produces an image (translation confirmed by checking English prompt in log).

---

### TASK 16.3 — Vision integration into runtime

**DESCRIPTION:** Wire image description into the Context assembler.

**INPUT:** `InputPacket` with image attachments.

**OUTPUT:** Image descriptions injected into `memory_snippets`.

**FILES:**
- MODIFY: `src/core/context/assembler.py`

**REQUIREMENTS:**
- For each image attachment in the packet, call `describe_image(path, "Describe this image")`.
- Prepend the description to `memory_snippets`.
- If LLaVA is unavailable, skip silently — do not block context assembly.

**SUCCESS CRITERIA:**
- Upload a chart image. Ask "what trend does this show?" Response reflects image content.

---

### TASK 16.4 — Screen description tool

**DESCRIPTION:** Describe the current screen using vision.

**INPUT:** `{}`.

**OUTPUT:** Natural language description of screen contents.

**FILES:**
- CREATE: `src/skills/screen/describe.py`

**REQUIREMENTS:**
- Define `DescribeScreenTool` with `name="describe_screen"`.
- Take screenshot via `ScreenshotTool`.
- Pass screenshot to `describe_image()`.
- Return description in `ToolResult.data`.

**SUCCESS CRITERIA:**
- "What's on my screen?" → accurate description of visible windows.

---

## 📱 Phase 17 — Telegram + GUI

> **End state:** Telegram bot handles text, photos, and voice. PyQt6 desktop app with tray.

---

### TASK 17.1 — Telegram bot

**DESCRIPTION:** Implement the full Telegram bot interface.

**INPUT:** Messages received via Telegram.

**OUTPUT:** Responses sent back via Telegram.

**FILES:**
- CREATE: `src/interfaces/telegram/bot.py`
- CREATE: `src/interfaces/telegram/handlers.py`
- CREATE: `src/interfaces/telegram/commands.py`

**REQUIREMENTS:**
- Text → `run_turn()` → reply.
- Photo → download to temp → `describe_image()` → reply.
- Voice note → download → `transcribe()` → `run_turn()` → reply.
- Document → download → `pdf_read_text()` or `docx_read()` → summary reply.
- Commands: `/start`, `/clear`, `/model`, `/mode`, `/image`.
- Simulate streaming by sending "Typing..." then editing with full response.

**SUCCESS CRITERIA:**
- Send Arabic voice note → transcription + Arabic answer returned.
- Send photo → image described.

---

### TASK 17.2 — PyQt6 desktop app

**DESCRIPTION:** Implement the desktop GUI application.

**INPUT:** User interaction with desktop window.

**OUTPUT:** Chat works with Arabic RTL.

**FILES:**
- CREATE: `src/interfaces/gui/main_window.py`
- CREATE: `src/interfaces/gui/settings_dialog.py`

**REQUIREMENTS:**
- Chat area, expanding input, send/mic buttons, model dropdown, mode toolbar.
- Arabic RTL rendering via `Qt.RightToLeft` layout direction.
- Settings dialog for model, language, voice, theme, startup.

**SUCCESS CRITERIA:**
- Launch GUI. Type Arabic message. RTL correct. Response appears.

---

### TASK 17.3 — System tray daemon

**DESCRIPTION:** Run Jarvis as a background tray process.

**INPUT:** App minimized or `--background` flag.

**OUTPUT:** Tray icon visible; wake word active in background.

**FILES:**
- CREATE: `src/interfaces/gui/tray.py`
- CREATE: `src/interfaces/gui/autostart.py`

**REQUIREMENTS:**
- `pystray` tray icon with menu: Open GUI, Open Web UI, Settings, Quit.
- Wake word listener in background thread.
- Wake word detection → bring main window to foreground.
- Auto-start: Windows registry, Linux `.config/autostart/`, macOS `LaunchAgents`.

**SUCCESS CRITERIA:**
- App in tray. Say "Hey Jarvis". GUI appears.
- Auto-start enabled. Reboot. Jarvis starts automatically.

---

### TASK 17.4 — Task decomposition engine

**DESCRIPTION:** Execute complex goals using a DAG of subtasks with parallel execution.

**INPUT:** Goal string.

**OUTPUT:** All subtasks executed; failed ones retried selectively.

**FILES:**
- CREATE: `src/core/agents/decomposer.py`
- CREATE: `src/core/agents/graph_executor.py`

**REQUIREMENTS:**
- `Subtask` Pydantic model: id, title, tool, args, depends_on, status, result.
- `TaskGraph` Pydantic model: goal, run_id, subtasks.
- `decompose(goal) → TaskGraph`.
- `execute_graph(graph)` using topological sort + `asyncio.gather()` for parallel frontier.
- Save graph state to SQLite after each subtask for resume support.
- `resume(run_id)` loads graph and skips completed subtasks.

**SUCCESS CRITERIA:**
- "Book meeting and send agenda email" → Calendar + Gmail tools used in correct order.
- Force-fail one subtask. Restart with run_id. Only that subtask re-executes.

---

## ✅ Phase 18 — QA + Security

> **End state:** Tests pass. No credentials in logs. Performance benchmarks met.

---

### TASK 18.1 — Test suite

**DESCRIPTION:** Write comprehensive tests for all phases.

**INPUT:** `pytest tests/` command.

**OUTPUT:** All tests pass; coverage ≥ 70%.

**FILES:**
- CREATE: `tests/test_contracts.py` (Phase 2)
- CREATE: `tests/test_decision.py` (Phase 4)
- CREATE: `tests/test_safety.py` (Phase 7)
- CREATE: `tests/test_tools.py` (Phase 6)
- CREATE: `tests/test_runtime.py` (Phase 3)
- CREATE: `tests/test_memory.py` (Phase 11)
- CREATE: `tests/test_skills.py` (Phase 8)
- CREATE: `tests/test_browser.py` (Phase 9)
- CREATE: `tests/test_apis.py` (Phase 10)
- CREATE: `tests/test_agents.py` (Phase 12)
- CREATE: `tests/test_voice.py` (Phase 15)
- CREATE: `tests/test_vision.py` (Phase 16)

**REQUIREMENTS:**
- No hardcoded credentials in test files.
- Tests that require Ollama must be marked with `@pytest.mark.integration` and skipped in CI.
- All pure logic tests (contracts, safety, decision rules) must work without Ollama.

**SUCCESS CRITERIA:**
- `pytest tests/ --cov=src -m "not integration"` → 0 failures, ≥ 70% coverage.

---

### TASK 18.2 — Security hardening

**DESCRIPTION:** Verify and fix all security requirements.

**INPUT:** Code review of all skills and config.

**OUTPUT:** Security checklist complete.

**FILES:**
- MODIFY: Multiple files as needed.

**REQUIREMENTS:**
- `delete_file` uses `send2trash` — never `os.remove` on user-specified paths.
- `run_shell` checks blocked patterns before `subprocess.Popen`.
- `send_email` always triggers confirmation in BALANCED mode.
- `google_token.json` path never appears in any log line.
- Browser session files encrypted when `SESSION_ENCRYPTION_KEY` set.
- All tool args validated against JSON Schema before execution.
- File paths checked against allowed roots.
- Error messages passed to LLM do not contain stack traces.
- `.env` in `.gitignore`.

**SUCCESS CRITERIA:**
- Each item above verified by code inspection and checked off.

---

### TASK 18.3 — Performance benchmarks

**DESCRIPTION:** Measure and verify system performance against targets.

**INPUT:** `python scripts/benchmark.py`.

**OUTPUT:** All metrics within defined targets.

**FILES:**
- CREATE: `scripts/benchmark.py`

**REQUIREMENTS:**
- Measure:
  - Cold start time (first response): target < 10 seconds.
  - Simple chat response (gemma3:4b): target < 5 seconds.
  - File read tool execution: target < 1 second.
  - VRAM peak during chat: target < 5.5 GB.
  - Voice round-trip (wake to spoken answer): target < 15 seconds.
- Output results as JSON to `data/benchmark_results.json`.

**SUCCESS CRITERIA:**
- All metrics within targets.
- Results file created and readable.

---

### TASK 18.4 — Windows 11 clean install test

**DESCRIPTION:** Verify full installation and operation on a clean Windows 11 system.

**INPUT:** Clean Windows 11 machine (or VM).

**OUTPUT:** All features work after fresh install.

**FILES:**
- MODIFY: `scripts/install.ps1` (finalize)

**REQUIREMENTS:**
- `install.ps1` completes without manual steps beyond entering API keys.
- Text chat, file operations, app launch, notification, and clipboard all work.
- Web UI accessible at localhost:8080.
- No `ModuleNotFoundError` at any point.

**SUCCESS CRITERIA:**
- All listed features work on the clean machine without manual troubleshooting.

---

### TASK 18.5 — Credential audit

**DESCRIPTION:** Verify no credentials appear in log files.

**INPUT:** All files in `logs/`.

**OUTPUT:** Zero credential matches.

**FILES:**
- CREATE: `scripts/credential_audit.py`

**REQUIREMENTS:**
- Scan all files in `logs/` for patterns matching: API keys, OAuth tokens, email+password combinations.
- Print each match found with file name and line number.
- Exit with code 1 if any match found; exit 0 if clean.

**SUCCESS CRITERIA:**
- Script exits with code 0 after running a full conversation session.

---

### TASK 18.6 — CI setup

**DESCRIPTION:** Configure automated testing on every push.

**INPUT:** Git push to main branch.

**OUTPUT:** Lint + type check + tests run automatically.

**FILES:**
- CREATE: `.github/workflows/ci.yml`
- CREATE: `.pre-commit-config.yaml`

**REQUIREMENTS:**
- CI runs on Ubuntu latest.
- Steps: checkout, setup Python 3.11, pip install, ruff lint, pytest (non-integration only).
- Credential audit runs in CI: `python scripts/credential_audit.py`.
- Pre-commit hooks: ruff format check, no trailing whitespace.

**SUCCESS CRITERIA:**
- Push to main triggers CI run.
- All checks pass on a clean push.
- A push with a linting error causes CI to fail.

---

### TASK 18.7 — Documentation finalization

**DESCRIPTION:** Update README and STRUCTURE.md to reflect the final implemented system.

**INPUT:** Completed implementation.

**OUTPUT:** Documentation matches actual behavior.

**FILES:**
- MODIFY: `README.md`
- MODIFY: `STRUCTURE.md`

**REQUIREMENTS:**
- Update version badge to reflect actual release.
- Update Implementation Status table with actual completed phases.
- Verify every file path mentioned in STRUCTURE.md exists.
- Verify every tool mentioned in README Section 14 has an entry in `config/skills.yaml`.

**SUCCESS CRITERIA:**
- No discrepancy between documentation and actual file structure.
- All listed tools verified to be registered and callable.
