# 🗂️ JARVIS — Execution Plan

> **Format:** Every task contains: DESCRIPTION · INPUT · OUTPUT · FILES · REQUIREMENTS · SUCCESS CRITERIA
>
> **No code in this file.** All implementation belongs in source files.
>
> **No examples in this file.** Success criteria state observable outcomes only.

---

## ⛔ MANDATORY GATE — Phase 0

**Phase 0 is a hard prerequisite. No other phase may begin until Phase 0 is fully complete.**

Verification: both manual tests in Tasks 0.4 and 0.5 must pass without error before proceeding to Phase 1.

Enforcement: mark Phase 0 done in the progress tracker only after both tests pass on the actual machine.

---

## 📊 Progress Tracker

| Phase | Name | Tasks | Done |
|-------|------|-------|------|
| 0 | First Working System **(MANDATORY FIRST)** | 5 | 0 |
| 1 | Foundation | 9 | 0 |
| 2 | Execution Contract | 6 | 0 |
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
| 14 | Web UI | 8 | 0 |
| 15 | Voice Pipeline | 5 | 0 |
| 16 | Vision + Image Generation | 4 | 0 |
| 17 | Telegram + GUI | 4 | 0 |
| 18 | QA + Security | 7 | 0 |

---

## 🚀 Phase 0 — First Working System

> **End state:** Two things work end-to-end — a message produces an LLM response, and "open chrome" executes the tool.
> **⛔ You may not start any other phase until this phase is complete.**

---

### TASK 0.1 — LLM connection

**DESCRIPTION:** Prove Ollama is reachable and a model produces text.

**INPUT:** The string "hello" passed programmatically.

**OUTPUT:** A non-empty string printed to the terminal.

**FILES:**
- CREATE: `src/models/llm/engine.py`

**REQUIREMENTS:**
- 0.1.1 — Define a `chat` function accepting a message string and an optional model string.
- 0.1.2 — The function must call the Ollama Python client with the provided model.
- 0.1.3 — The function must return the response content as a string.
- 0.1.4 — The function must not raise on connection failure — return an error string instead.
- 0.1.5 — The file must be runnable directly and print the result of `chat("hello")` when executed.

**SUCCESS CRITERIA:**
- Running the file directly prints a non-empty, coherent response.
- No exception reaches the terminal.
- Response arrives within 60 seconds.

---

### TASK 0.2 — Intent classifier

**DESCRIPTION:** Given a user message, return a structured classification describing what action to take.

**INPUT:** The string "open chrome".

**OUTPUT:** A Python dict containing at minimum: `intent`, `requires_tools`, `tool_name`, `tool_args`.

**FILES:**
- CREATE: `src/core/decision/classifier.py`

**REQUIREMENTS:**
- 0.2.1 — Define a `classify` function accepting a message string and returning a dict.
- 0.2.2 — Use `gemma3:4b` with a system prompt that instructs the model to return only JSON.
- 0.2.3 — The system prompt must define the expected JSON schema explicitly.
- 0.2.4 — The system prompt must include examples in both Arabic and English.
- 0.2.5 — Strip markdown code block markers from the model response before parsing.
- 0.2.6 — Extract JSON by finding the first `{` and last `}` in the response string.
- 0.2.7 — Retry up to 2 times on JSON parse failure, appending a correction instruction.
- 0.2.8 — Return a safe fallback dict with `intent="chat"` if all retries fail.
- 0.2.9 — Log each retry and each fallback event.
- 0.2.10 — The function must not raise on any input.

**SUCCESS CRITERIA:**
- `classify("open chrome")` returns a dict with `intent="tool_use"` and `tool_name="open_app"`.
- `classify("افتح Chrome")` returns the same result as `classify("open chrome")`.
- `classify("what is AI?")` returns a dict with `intent="chat"`.
- No exception is raised on any of the three inputs.

---

### TASK 0.3 — Application launcher

**DESCRIPTION:** Open a named application on the current operating system.

**INPUT:** A dict `{"name": "notepad"}` (or the platform-appropriate test app).

**OUTPUT:** The application opens visibly. A dict is returned with `success=True` and the process PID.

**FILES:**
- CREATE: `src/skills/system/apps.py`

**REQUIREMENTS:**
- 0.3.1 — Define an `open_app(name)` function returning a dict with `success` and either `pid` or `error`.
- 0.3.2 — Search in this order: PATH via `shutil.which`, then platform-specific directories.
- 0.3.3 — On Windows: search `PROGRAMFILES`, `PROGRAMFILES(X86)`, `LOCALAPPDATA`.
- 0.3.4 — On Linux: attempt `subprocess.Popen` directly with the name.
- 0.3.5 — On macOS: use the `open -a` command.
- 0.3.6 — Return `{"success": False, "error": "..."}` if not found, without raising.
- 0.3.7 — Define a `close_app(name)` function using `taskkill` on Windows, `pkill` on Linux/macOS.

**SUCCESS CRITERIA:**
- `open_app("notepad")` on Windows opens Notepad and returns `{"success": True, "pid": <number>}`.
- `open_app("xyznonexistent")` returns `{"success": False, "error": "..."}` without raising.

---

### TASK 0.4 — Wire classifier to tool

**DESCRIPTION:** Connect input, classifier, and tool into a single runnable script.

**INPUT:** A string typed at a terminal prompt.

**OUTPUT:** If classified as tool call, the tool executes and prints a confirmation. Otherwise, prints a chat response.

**FILES:**
- CREATE: `app/jarvis_slice.py`

**REQUIREMENTS:**
- 0.4.1 — Define a `run(user_input)` function.
- 0.4.2 — Call `classify(user_input)` from Task 0.2.
- 0.4.3 — If `requires_tools=True` and `tool_name` is in the supported map, call the tool function.
- 0.4.4 — If `requires_tools=False`, call `chat(user_input)` from Task 0.1 and print the result.
- 0.4.5 — Handle a malformed or unexpected dict from `classify()` without crashing.
- 0.4.6 — Run in a terminal loop until the user types "quit".
- 0.4.7 — No exception may reach the terminal for any input.

**SUCCESS CRITERIA:**
- Typing "open notepad" opens Notepad and prints a confirmation.
- Typing "what is machine learning?" prints a text answer.
- Typing "quit" exits cleanly.
- No exception is visible in the terminal for any input tested.

---

### TASK 0.5 — Arabic input verification

**DESCRIPTION:** Confirm that Arabic commands produce the same behavior as their English equivalents.

**INPUT:** Arabic text at the `jarvis_slice.py` terminal prompt.

**OUTPUT:** Same behavior as the English equivalent.

**FILES:**
- MODIFY: `src/core/decision/classifier.py` — add Arabic examples to the system prompt if needed.

**REQUIREMENTS:**
- 0.5.1 — Test the Arabic equivalent of "open notepad" at the terminal.
- 0.5.2 — If the classifier does not return `intent="tool_use"`, add at least three Arabic tool examples to the system prompt and re-test.
- 0.5.3 — Test an Arabic question and confirm it returns a text answer.
- 0.5.4 — No new files are needed unless the classifier fails.

**SUCCESS CRITERIA:**
- Arabic command for "open notepad" opens Notepad.
- Arabic question returns a text answer.
- The classifier does not return `intent="chat"` for a clear Arabic tool command.

---

## 🏗️ Phase 1 — Foundation

> **End state:** `python app/main.py --interface cli` executes all Boot Flow steps and prints "Jarvis ready."

---

### TASK 1.1 — Settings file and loader

**DESCRIPTION:** Create the configuration file and typed Python loader.

**INPUT:** `config/settings.yaml`.

**OUTPUT:** A cached `get_settings()` function returning a fully typed settings object.

**FILES:**
- CREATE: `config/settings.example.yaml`
- CREATE: `config/settings.yaml`
- CREATE: `src/core/config.py`

**REQUIREMENTS:**
- 1.1.1 — `settings.example.yaml` must contain all sections: jarvis, models, hardware, interfaces, paths, hotkeys, runtime.
- 1.1.2 — The `runtime` section must include: `max_iterations`, `max_tool_retries`, `tool_timeout_s`, `execution_mode`.
- 1.1.3 — `execution_mode` must default to `"balanced"` and accept only: safe, balanced, unrestricted.
- 1.1.4 — Define one Pydantic model per YAML section in `src/core/config.py`.
- 1.1.5 — `get_settings()` must be a cached singleton — reads the file exactly once.
- 1.1.6 — Missing optional fields must not raise — Pydantic defaults apply.
- 1.1.7 — Define `create_directories()` that creates all paths from the `paths` section.

**SUCCESS CRITERIA:**
- `get_settings().jarvis.name` returns `"Jarvis"`.
- `get_settings().runtime.execution_mode` returns `"balanced"`.
- `get_settings()` called twice returns the same object instance.
- `create_directories()` creates all configured directories.

---

### TASK 1.2 — Logging setup

**DESCRIPTION:** Configure structured logging to terminal and rotating file.

**INPUT:** A call to `setup_logging()` at startup.

**OUTPUT:** Log entries appear in terminal and in `logs/jarvis.log`.

**FILES:**
- CREATE: `src/core/logging_setup.py`

**REQUIREMENTS:**
- 1.2.1 — Configure Loguru with two sinks: colored terminal and rotating file.
- 1.2.2 — File rotation at 10 MB. Retention 7 days. Encoding UTF-8.
- 1.2.3 — Log format: timestamp, level, message.
- 1.2.4 — Accept a `level` string parameter (default `"INFO"`) and a `debug` boolean.
- 1.2.5 — When `debug=True`, add a second file sink at DEBUG level writing to `logs/debug.log`.
- 1.2.6 — Create the `logs/` directory if it does not exist.

**SUCCESS CRITERIA:**
- After calling `setup_logging()`, an INFO log call appears in both terminal and `logs/jarvis.log`.
- `logs/` directory is created automatically if missing.

---

### TASK 1.3 — Package skeleton

**DESCRIPTION:** Create all Python package directories.

**INPUT:** Nothing.

**OUTPUT:** All source directories are importable Python packages.

**FILES:**
- CREATE: `__init__.py` in every directory under `src/` as listed in `STRUCTURE.md`.

**REQUIREMENTS:**
- 1.3.1 — Every subdirectory under `src/` must have an empty `__init__.py`.
- 1.3.2 — No directory listed in `STRUCTURE.md` may be skipped.

**SUCCESS CRITERIA:**
- `python -c "import src.core.decision"` succeeds without error.
- `python -c "import src.skills.system"` succeeds without error.
- `python -c "import src.interfaces.cli"` succeeds without error.

---

### TASK 1.4 — Model capability profiles

**DESCRIPTION:** Create the model metadata YAML and a Python loader.

**INPUT:** `config/models.yaml`.

**OUTPUT:** `get_model_profile(tag)` returns a dict of capability fields.

**FILES:**
- CREATE: `config/models.yaml`
- CREATE: `src/models/profiles.py`

**REQUIREMENTS:**
- 1.4.1 — Entries for: `qwen3:8b`, `gemma3:4b`, `qwen2.5-coder:7b`, `llava:7b`.
- 1.4.2 — Each entry must include: temperature, top_p, max_tokens, vram_gb, arabic_quality, reasoning, code_bias, vision, latency.
- 1.4.3 — Define `get_model_profile(model_tag)` returning the dict.
- 1.4.4 — Return empty dict (not raise) for unknown tags.

**SUCCESS CRITERIA:**
- `get_model_profile("qwen3:8b")["vram_gb"]` returns `5.0`.
- `get_model_profile("llava:7b")["vision"]` returns `True`.
- `get_model_profile("nonexistent")` returns `{}`.

---

### TASK 1.5 — LLM engine with VRAM guard

**DESCRIPTION:** Expand the engine with model tracking and safe swapping.

**INPUT:** Sequential calls to `swap_to()` with different model names.

**OUTPUT:** Only one model active at a time. No OOM error.

**FILES:**
- MODIFY: `src/models/llm/engine.py`

**REQUIREMENTS:**
- 1.5.1 — Add a module-level variable tracking the currently active model name.
- 1.5.2 — Define `get_active_model()` returning the current model tag or `None`.
- 1.5.3 — Define `unload_current_model()` calling the Ollama API to release the model.
- 1.5.4 — Define `swap_to(model)` that unloads the current model if it differs, then updates the tracker.
- 1.5.5 — `swap_to` must log a `model.swap` event with `from` and `to` fields.
- 1.5.6 — No function may raise on failure — log the error and return gracefully.
- 1.5.7 — Define `stream_chat(message, model, system)` as a generator yielding response tokens.

**SUCCESS CRITERIA:**
- After `swap_to("gemma3:4b")`, `get_active_model()` returns `"gemma3:4b"`.
- After `swap_to("qwen3:8b")`, `get_active_model()` returns `"qwen3:8b"`.
- No OOM error during the sequence.

---

### TASK 1.6 — Environment variables

**DESCRIPTION:** Document and load all required secrets.

**INPUT:** `.env` file with keys set.

**OUTPUT:** Variables accessible via `os.environ`.

**FILES:**
- CREATE: `.env.example`
- CREATE: `.env` (copied from example by user)

**REQUIREMENTS:**
- 1.6.1 — `.env.example` must list all keys with empty values and a comment explaining each.
- 1.6.2 — Required keys: `TELEGRAM_BOT_TOKEN`, `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `YOUTUBE_API_KEY`, `SESSION_ENCRYPTION_KEY`, `JARVIS_DEBUG`, `OLLAMA_HOST`.
- 1.6.3 — `JARVIS_DEBUG` default: `0`. `OLLAMA_HOST` default: `http://localhost:11434`.
- 1.6.4 — `SESSION_ENCRYPTION_KEY` comment must describe how to generate the value.
- 1.6.5 — `.env` must appear in `.gitignore`.
- 1.6.6 — `app/main.py` must call `load_dotenv()` before any `src.*` import.

**SUCCESS CRITERIA:**
- `os.environ.get("JARVIS_DEBUG")` returns `"0"` after loading a default `.env`.
- `.env` does not appear in `git status`.

---

### TASK 1.7 — User profile

**DESCRIPTION:** Create a persistent JSON store for user preferences.

**INPUT:** A dict of preference updates.

**OUTPUT:** Saved to `data/user_profile.json` and loadable after restart.

**FILES:**
- CREATE: `src/core/memory/user_profile.py`

**REQUIREMENTS:**
- 1.7.1 — Define `load_profile()` returning a dict. Return defaults if file does not exist.
- 1.7.2 — Define `save_profile(updates)` merging updates into the existing profile and writing to disk.
- 1.7.3 — Define `get_profile_value(key, default)`.
- 1.7.4 — Default profile must include: name, language, style, tone, technical_level, timezone.
- 1.7.5 — Default language: `"ar"`. Default style: `"balanced"`.
- 1.7.6 — File path must be read from `get_settings().paths.data`.

**SUCCESS CRITERIA:**
- `save_profile({"language": "en"})` writes to disk.
- After Python restarts, `load_profile()["language"]` returns `"en"`.
- `load_profile()` returns defaults when no file exists.

---

### TASK 1.8 — Skills manifest

**DESCRIPTION:** Create the tool registry manifest declaring all tools with their metadata.

**INPUT:** Nothing.

**OUTPUT:** `config/skills.yaml` with every tool declared.

**FILES:**
- CREATE: `config/skills.yaml`

**REQUIREMENTS:**
- 1.8.1 — Every tool in README Section 14 must have an entry.
- 1.8.2 — Each entry must include: id, enabled, category, module path, platform list, risk_level, schema path.
- 1.8.3 — `risk_level` must match README Section 9 Risk Classification table exactly.
- 1.8.4 — `delete_file`, `kill_process`, `send_email`, `send_message`, `whatsapp_send` → `risk_level: high`.
- 1.8.5 — `execute_python`, `run_shell`, `open_app`, `close_app` → `risk_level: medium`.
- 1.8.6 — `web_search`, `read_file`, `system_info`, `take_screenshot` → `risk_level: low`.
- 1.8.7 — Tools with `enabled: false` must not be loaded by the registry.
- 1.8.8 — File must be valid YAML parseable without error.

**SUCCESS CRITERIA:**
- Every tool in README Section 14 has an entry.
- No entry has a missing or empty `risk_level`.
- File parses without YAML error.

---

### TASK 1.9 — main.py entry point

**DESCRIPTION:** Create the single entry point that executes all Boot Flow steps.

**INPUT:** `--interface cli` command-line argument.

**OUTPUT:** All 12 Boot Flow steps from README Section 7 execute in order. "Jarvis ready" is logged.

**FILES:**
- CREATE: `app/main.py`

**REQUIREMENTS:**
- 1.9.1 — Accept `--interface` with choices: cli, web, voice, telegram, gui, all.
- 1.9.2 — Accept `--debug` flag.
- 1.9.3 — Call `load_dotenv()` as the very first action before any `src.*` import.
- 1.9.4 — Add project root to `sys.path` so `src.*` imports work.
- 1.9.5 — Execute Boot Flow steps 1 through 12 in order.
- 1.9.6 — Log each step's completion.
- 1.9.7 — Catch `KeyboardInterrupt` and log "Jarvis stopped by user" before exiting cleanly.
- 1.9.8 — Step 11 (memory) must not abort on Redis or ChromaDB failure — switch to fallback and log warning.
- 1.9.9 — Step 11 must abort if SQLite fails.

**SUCCESS CRITERIA:**
- `python app/main.py --interface cli` executes all steps without error.
- "Jarvis ready" appears in `logs/jarvis.log`.
- `Ctrl+C` exits without a traceback.

---

## 📦 Phase 2 — Execution Contract

> **End state:** All five contract types are defined as Pydantic models and used across all phases. No raw dicts flow between layers.

---

### TASK 2.1 — InputPacket model

**DESCRIPTION:** Define the `InputPacket` Pydantic model as specified in README Section 3.

**INPUT:** User message and session ID.

**OUTPUT:** An `InputPacket` instance with all fields populated and type-safe.

**FILES:**
- CREATE: `src/core/context/bundle.py`

**REQUIREMENTS:**
- 2.1.1 — Define `InputPacket` with all fields from README Section 3: user_message, session_id, attachments, memory_snippets, recent_history, user_profile, tool_results, turn_number.
- 2.1.2 — Define supporting types: `Attachment`, `Message`, `UserProfile` as Pydantic models.
- 2.1.3 — Import `ToolResult` from `src/core/tools/result.py` (created in Task 2.4) to avoid duplication.
- 2.1.4 — All list fields must default to empty lists.
- 2.1.5 — No field may use `Any` as a type.
- 2.1.6 — All optional fields must have explicit defaults.

**SUCCESS CRITERIA:**
- `InputPacket(user_message="hello", session_id="s1")` instantiates without error.
- All fields are accessible with their declared types.
- Assigning a wrong type raises a Pydantic `ValidationError`.

---

### TASK 2.2 — DecisionOutput model

**DESCRIPTION:** Define the `DecisionOutput` Pydantic model as specified in README Section 3.

**INPUT:** Raw classification dict.

**OUTPUT:** A typed `DecisionOutput` instance.

**FILES:**
- CREATE: `src/core/decision/decision.py`

**REQUIREMENTS:**
- 2.2.1 — Define `DecisionOutput` with all fields from README Section 3.
- 2.2.2 — `intent` must be constrained to the allowed values list.
- 2.2.3 — `complexity` must be constrained to: low, medium, high.
- 2.2.4 — `mode` must be constrained to: fast, normal, deep, planning, research.
- 2.2.5 — `risk_level` must be constrained to: low, medium, high.
- 2.2.6 — `tool_name` must allow `None`.
- 2.2.7 — `tool_args` must default to `{}`.
- 2.2.8 — `confidence` must be a float between 0.0 and 1.0 (use Pydantic validator).

**SUCCESS CRITERIA:**
- A valid `DecisionOutput` instantiates without error.
- Setting `intent="invalid_value"` raises a `ValidationError`.
- Setting `confidence=1.5` raises a `ValidationError`.

---

### TASK 2.3 — LLMOutput model and parser

**DESCRIPTION:** Define the `LLMOutput` model and the function that parses raw LLM text into it.

**INPUT:** Raw LLM response string and a `requires_tools` bool.

**OUTPUT:** `LLMOutput` with `type` set to either `"answer"` or `"tool_call"`.

**FILES:**
- CREATE: `src/core/runtime/llm_output.py`

**REQUIREMENTS:**
- 2.3.1 — Define `LLMOutput` with fields: type, content, tool, args.
- 2.3.2 — `type` must be constrained to: `"answer"` or `"tool_call"`.
- 2.3.3 — Define `parse_llm_output(raw_text, requires_tools)` returning `LLMOutput`.
- 2.3.4 — Attempt to extract a JSON block from the raw text using first `{` to last `}`.
- 2.3.5 — If JSON found and `requires_tools=True`: return `LLMOutput(type="tool_call", ...)`.
- 2.3.6 — If no JSON and `requires_tools=False`: return `LLMOutput(type="answer", content=raw_text)`.
- 2.3.7 — If `requires_tools=True` and no valid JSON found: return `LLMOutput(type="tool_call", tool="")` as the parse failure indicator.
- 2.3.8 — No exception may escape this function.

**SUCCESS CRITERIA:**
- Valid tool call JSON in input → `LLMOutput(type="tool_call", tool="open_app")`.
- Plain text with `requires_tools=False` → `LLMOutput(type="answer")`.
- Non-JSON text with `requires_tools=True` → `LLMOutput(type="tool_call", tool="")` (parse failure marker).

---

### TASK 2.4 — ToolResult model

**DESCRIPTION:** Define the `ToolResult` Pydantic model as specified in README Section 3.

**INPUT:** Output from `tool.execute()`.

**OUTPUT:** A typed `ToolResult` instance.

**FILES:**
- CREATE: `src/core/tools/result.py`

**REQUIREMENTS:**
- 2.4.1 — Define `ToolResult` with fields: tool, success, data, error, duration_ms.
- 2.4.2 — `data` defaults to `{}`.
- 2.4.3 — `error` defaults to `""`.
- 2.4.4 — `duration_ms` defaults to `0.0`.
- 2.4.5 — This is the single definition. Import it in `bundle.py` to avoid duplication.

**SUCCESS CRITERIA:**
- `ToolResult(tool="open_app", success=True, data={"pid": 123})` instantiates without error.
- `ToolResult(tool="open_app", success=False, error="Not found")` instantiates without error.

---

### TASK 2.5 — FinalResponse model

**DESCRIPTION:** Define the `FinalResponse` type used as the output of `run_turn()`.

**INPUT:** Approved response text with metadata.

**OUTPUT:** A typed `FinalResponse` instance returned to the interface.

**FILES:**
- CREATE: `src/core/runtime/final_response.py`

**REQUIREMENTS:**
- 2.5.1 — Define `FinalResponse` with fields: text, session_id, model, mode, quality.
- 2.5.2 — All fields are required with no defaults.
- 2.5.3 — The interface layer must only access `FinalResponse.text` for display.

**SUCCESS CRITERIA:**
- `FinalResponse(text="hello", session_id="s1", model="qwen3:8b", mode="normal", quality=0.85)` instantiates without error.

---

### TASK 2.6 — Contract validation tests

**DESCRIPTION:** Verify all five contract types enforce their schemas.

**INPUT:** Valid and invalid field combinations for each type.

**OUTPUT:** Pydantic raises on invalid input. Accepts valid input.

**FILES:**
- CREATE: `tests/test_contracts.py`

**REQUIREMENTS:**
- 2.6.1 — Test each model with at least one valid instantiation.
- 2.6.2 — Test each model with at least one invalid field value that should raise `ValidationError`.
- 2.6.3 — Test `parse_llm_output` with all three cases from Task 2.3.
- 2.6.4 — No Ollama calls in this test file — pure Pydantic tests.

**SUCCESS CRITERIA:**
- `pytest tests/test_contracts.py` passes with 0 failures.

---

## 🔄 Phase 3 — Runtime Loop

> **End state:** A complete turn executes end-to-end through all five stages: assemble → decide → think → act → evaluate → return.

---

### TASK 3.1 — Context assembler

**DESCRIPTION:** Implement the function that builds an `InputPacket` from user input.

**INPUT:** User message string, session ID, optional attachment list.

**OUTPUT:** A populated `InputPacket`.

**FILES:**
- CREATE: `src/core/context/assembler.py`

**REQUIREMENTS:**
- 3.1.1 — Define `assemble_context(user_message, session_id, attachments)` returning `InputPacket`.
- 3.1.2 — Load user profile via `load_profile()` and attach to `user_profile` field.
- 3.1.3 — Set `memory_snippets` and `recent_history` to empty lists. Phase 11 wires in the real calls.
- 3.1.4 — Track `turn_number` per session using a module-level dict. Increment on each call.
- 3.1.5 — Never raise on valid input.

**SUCCESS CRITERIA:**
- `assemble_context("hello", "s1")` returns an `InputPacket` with `user_message="hello"`.
- `turn_number` increments across calls with the same session ID.
- `user_profile.language` is populated from the profile file.

---

### TASK 3.2 — Decision function

**DESCRIPTION:** Implement `decide()` that produces `DecisionOutput` from an `InputPacket`.

**INPUT:** `InputPacket`.

**OUTPUT:** `DecisionOutput`.

**FILES:**
- MODIFY: `src/core/decision/decision.py`

**REQUIREMENTS:**
- 3.2.1 — Define `decide(packet) → DecisionOutput`.
- 3.2.2 — Implement fast-path rules before any LLM call, as defined in README Section 11.
- 3.2.3 — For non-fast-path cases, call `classify(packet.user_message)`.
- 3.2.4 — Map the returned dict to a `DecisionOutput` instance.
- 3.2.5 — On classifier failure, return a safe default `DecisionOutput` with `intent="chat"`.
- 3.2.6 — Populate `risk_level` by looking up `tool_name` in `config/skills.yaml`. Default to `"low"` if not found.

**SUCCESS CRITERIA:**
- `decide(assemble_context("hello", "s1"))` returns `intent="chat"`.
- `decide(assemble_context("open chrome", "s1"))` returns `tool_name="open_app"`.
- A classifier exception does not propagate — fallback is returned.

---

### TASK 3.3 — Executor (think step)

**DESCRIPTION:** Implement `execute_turn()` that calls the model and returns `LLMOutput`.

**INPUT:** `DecisionOutput`, `InputPacket`.

**OUTPUT:** `LLMOutput`.

**FILES:**
- CREATE: `src/core/runtime/executor.py`

**REQUIREMENTS:**
- 3.3.1 — Define `execute_turn(decision, packet) → LLMOutput`.
- 3.3.2 — Call `swap_to(decision.model)` before calling the model.
- 3.3.3 — Call `build_system_prompt()` from the Prompt Builder. Use a stub returning empty string until Phase 5.
- 3.3.4 — Construct the message list from the system prompt and user message.
- 3.3.5 — Call `stream_chat()` and collect all tokens into a complete string.
- 3.3.6 — Pass the complete string to `parse_llm_output(raw, decision.requires_tools)`.
- 3.3.7 — Return the resulting `LLMOutput`.
- 3.3.8 — On any Ollama error, return `LLMOutput(type="answer", content="<error message>")` without raising.

**SUCCESS CRITERIA:**
- `execute_turn(decision, packet)` returns an `LLMOutput` with non-empty `content` or valid `tool` name.
- An Ollama error returns an `LLMOutput(type="answer")` rather than raising.

---

### TASK 3.4 — Evaluator

**DESCRIPTION:** Implement the function that scores a response and decides if retry is needed.

**INPUT:** `LLMOutput`, `DecisionOutput`.

**OUTPUT:** `EvalResult` with quality score and retry flag.

**FILES:**
- CREATE: `src/core/runtime/evaluator.py`

**REQUIREMENTS:**
- 3.4.1 — Define `EvalResult` as a Pydantic model with fields: quality (float 0–1), should_retry (bool), reason (str).
- 3.4.2 — Define `evaluate(output, decision) → EvalResult`.
- 3.4.3 — Empty or whitespace-only `content` → quality=0.0, retry=True, reason="empty response".
- 3.4.4 — `complexity == "high"` and `len(content) < 80` → quality=0.3, retry=True, reason="too short for complex task".
- 3.4.5 — `requires_tools=True` and `output.type="answer"` and `len(content) < 50` → quality=0.4, retry=True, reason="expected tool call".
- 3.4.6 — All other cases → quality=0.85, retry=False.
- 3.4.7 — No model calls or external calls.

**SUCCESS CRITERIA:**
- Empty content → `should_retry=True`.
- Valid answer for a simple question → `should_retry=False`.

---

### TASK 3.5 — Runtime loop

**DESCRIPTION:** Implement `run_turn()` driving the full cycle as defined in README Section 4.

**INPUT:** User message string, session ID, optional attachments.

**OUTPUT:** `FinalResponse`.

**FILES:**
- CREATE: `src/core/runtime/loop.py`

**REQUIREMENTS:**
- 3.5.1 — Define `run_turn(user_input, session_id, attachments) → FinalResponse`.
- 3.5.2 — Define `run_turn_streaming(user_input, session_id, attachments)` as a generator yielding string tokens.
- 3.5.3 — Implement the loop exactly as described in README Section 4.
- 3.5.4 — Read `max_iterations` from `get_settings().runtime.max_iterations`.
- 3.5.5 — On tool call: call `execute_tool(output.tool, output.args)`, append `ToolResult` to `packet.tool_results`, continue loop.
- 3.5.6 — On tool call with empty `tool` field (parse failure): return error `FinalResponse` immediately.
- 3.5.7 — On approved answer: return `FinalResponse`.
- 3.5.8 — On loop exhaustion: return `FinalResponse` with last content and exhaustion note.
- 3.5.9 — Emit EventBus events: `turn.start`, `decision`, `turn.end`.
- 3.5.10 — Memory saves are stub calls in this phase. Phase 11 replaces the stubs.

**SUCCESS CRITERIA:**
- `run_turn("what is AI?", "s1")` returns a `FinalResponse` with non-empty `text`.
- `run_turn("open notepad", "s1")` triggers the tool path and opens Notepad.
- The loop runs at most `max_iterations` times.

---

### TASK 3.6 — EventBus

**DESCRIPTION:** Implement the publish-subscribe event system.

**INPUT:** Event name string and data dict.

**OUTPUT:** All registered handlers receive the data.

**FILES:**
- CREATE: `src/core/events.py`

**REQUIREMENTS:**
- 3.6.1 — Define `EventBus` with methods: `subscribe(event, handler)`, `unsubscribe(event, handler)`, `emit(event, data)`.
- 3.6.2 — Define a module-level singleton `bus`.
- 3.6.3 — `emit` must not raise if a handler raises — log the error and continue to remaining handlers.
- 3.6.4 — No external dependencies.

**SUCCESS CRITERIA:**
- Subscribe a handler to `"turn.end"`. Call `bus.emit("turn.end", {"text": "hi"})`. Handler is called with the dict.
- A handler that raises does not prevent remaining handlers from running.

---

## 🎯 Phase 4 — Decision System

> **End state:** All intent types classified correctly. Correct model selected per intent. Risk level populated on every `DecisionOutput`.

---

### TASK 4.1 — Classifier hardening

**DESCRIPTION:** Harden the classifier to handle all LLM output variations without failure.

**INPUT:** Any non-empty user message.

**OUTPUT:** Always returns a valid dict matching the `DecisionOutput` schema fields.

**FILES:**
- MODIFY: `src/core/decision/classifier.py`

**REQUIREMENTS:**
- 4.1.1 — Extract JSON by finding first `{` and last `}` in the response.
- 4.1.2 — Strip all markdown code block markers before parsing.
- 4.1.3 — Verify all required fields are present after parsing.
- 4.1.4 — Retry with explicit correction instruction if any required field is missing.
- 4.1.5 — Return safe fallback dict after 2 retries.
- 4.1.6 — Log each retry and each fallback at WARNING level.
- 4.1.7 — No exception may escape the function.

**SUCCESS CRITERIA:**
- Returns valid dict for any non-empty string input.
- Returns fallback dict when model responds with pure prose.
- No exception reaches the caller.

---

### TASK 4.2 — Fast-path rules

**DESCRIPTION:** Implement the no-LLM fast path for obvious classification cases.

**INPUT:** `InputPacket`.

**OUTPUT:** `DecisionOutput` without calling any model.

**FILES:**
- MODIFY: `src/core/decision/decision.py`

**REQUIREMENTS:**
- 4.2.1 — Implement all fast-path rules from README Section 11.
- 4.2.2 — Fast path must run before any LLM call attempt.
- 4.2.3 — Log each fast-path match at DEBUG level.
- 4.2.4 — Do not apply fast path if message contains any of these keywords: open, close, send, search, find, create, delete, run.

**SUCCESS CRITERIA:**
- A 5-character message with no action keywords routes to fast chat without triggering an Ollama call.
- An image in attachments routes to `llava:7b` via fast path.

---

### TASK 4.3 — Risk level population

**DESCRIPTION:** Populate `risk_level` on `DecisionOutput` from the skills manifest.

**INPUT:** `tool_name` from classification result.

**OUTPUT:** `DecisionOutput.risk_level` set to the correct value.

**FILES:**
- MODIFY: `src/core/decision/decision.py`

**REQUIREMENTS:**
- 4.3.1 — Load `config/skills.yaml` once at module import time.
- 4.3.2 — Look up `risk_level` for the classified `tool_name`.
- 4.3.3 — If `tool_name` is `None` or not found, set `risk_level="low"`.

**SUCCESS CRITERIA:**
- A decision for `delete_file` returns `risk_level="high"`.
- A decision for a conversational message returns `risk_level="low"`.

---

### TASK 4.4 — Escalation chain

**DESCRIPTION:** Define the mode and model escalation sequence.

**INPUT:** Current mode and model strings.

**OUTPUT:** Next mode and model, or `None` if at maximum.

**FILES:**
- CREATE: `src/core/runtime/escalation.py`

**REQUIREMENTS:**
- 4.4.1 — Define the chain as three levels: fast/gemma3:4b → normal/qwen3:8b → deep/qwen3:8b.
- 4.4.2 — Define `get_next_escalation(current_mode, current_model) → tuple | None`.
- 4.4.3 — The function must be pure (no side effects, no external calls).

**SUCCESS CRITERIA:**
- `get_next_escalation("fast", "gemma3:4b")` returns `("normal", "qwen3:8b")`.
- `get_next_escalation("deep", "qwen3:8b")` returns `None`.

---

### TASK 4.5 — Decision system tests

**DESCRIPTION:** Test all routing rules and the escalation chain.

**INPUT:** Various test message strings.

**OUTPUT:** Correct `DecisionOutput` for each.

**FILES:**
- CREATE: `tests/test_decision.py`

**REQUIREMENTS:**
- 4.5.1 — Test that code-intent messages route to `qwen2.5-coder:7b`.
- 4.5.2 — Test that Arabic tool commands route to `intent="tool_use"`.
- 4.5.3 — Test that image-attached packets route to `model="llava:7b"`.
- 4.5.4 — Test the fast path produces output without an Ollama call.
- 4.5.5 — Test the escalation chain from Task 4.4.
- 4.5.6 — Mock `classify()` — no real Ollama calls.

**SUCCESS CRITERIA:**
- `pytest tests/test_decision.py` passes with 0 failures.

---

## 📝 Phase 5 — Prompt Builder

> **End state:** Every LLM call receives a system prompt assembled from the components in README Section 10 in the defined order.

---

### TASK 5.1 — Jarvis identity YAML

**DESCRIPTION:** Create the identity definition file.

**INPUT:** Nothing.

**OUTPUT:** `config/jarvis_identity.yaml` with all required fields.

**FILES:**
- CREATE: `config/jarvis_identity.yaml`

**REQUIREMENTS:**
- 5.1.1 — Include: name, role, component_notice, safety_rules (list), language_behavior.
- 5.1.2 — `component_notice` must state that the model is a component of Jarvis, not the underlying weights.
- 5.1.3 — `safety_rules` must include rules on: credentials, destructive actions, uncertainty, and privacy.
- 5.1.4 — `language_behavior` must have entries for both `ar` and `en` with: greeting, affirmation, style.

**SUCCESS CRITERIA:**
- File is valid YAML.
- All required keys are present and non-empty.

---

### TASK 5.2 — Mode fragments

**DESCRIPTION:** Create the instruction fragments for each thinking mode.

**INPUT:** A mode string.

**OUTPUT:** The corresponding instruction text.

**FILES:**
- CREATE: `src/core/identity/personality.py`

**REQUIREMENTS:**
- 5.2.1 — Define `MODE_FRAGMENTS` dict with entries for: fast, normal, deep, planning, research.
- 5.2.2 — Each value must be a one-to-three sentence instruction matching README Section 10.
- 5.2.3 — Define `get_mode_fragment(mode)` returning the fragment or `""` for unknown modes.

**SUCCESS CRITERIA:**
- `get_mode_fragment("fast")` returns a non-empty string.
- `get_mode_fragment("unknown")` returns `""` without raising.
- All five modes have distinct, non-empty fragments.

---

### TASK 5.3 — System prompt builder

**DESCRIPTION:** Implement the central `build_system_prompt()` function.

**INPUT:** task_context, mode, tools list, previous_model, current_model.

**OUTPUT:** A complete system prompt string.

**FILES:**
- CREATE: `src/core/identity/builder.py`

**REQUIREMENTS:**
- 5.3.1 — Define `build_system_prompt(task_context, mode, tools, previous_model, current_model) → str`.
- 5.3.2 — Assemble blocks in the exact order from README Section 10.
- 5.3.3 — Load identity from `config/jarvis_identity.yaml` once at import time.
- 5.3.4 — Load user profile on each call via `load_profile()`.
- 5.3.5 — Include block 6 (tool list) only if `tools` is non-empty.
- 5.3.6 — Include block 7 (handoff note) only if `previous_model` differs from `current_model` and is not `None`.
- 5.3.7 — Tool list must include tool name and description only — no schema details.

**SUCCESS CRITERIA:**
- `build_system_prompt("open chrome", "fast", [], None, "gemma3:4b")` returns a non-empty string.
- Returned string contains "Jarvis".
- Returned string contains the fast-mode fragment.
- Handoff note is absent when `previous_model=None`.
- Handoff note is present when `previous_model="gemma3:4b"` and `current_model="qwen3:8b"`.

---

### TASK 5.4 — Wire prompt builder into executor

**DESCRIPTION:** Replace the stub in `executor.py` with the real prompt builder.

**INPUT:** `DecisionOutput`, `InputPacket`.

**OUTPUT:** LLM receives the correct assembled system prompt.

**FILES:**
- MODIFY: `src/core/runtime/executor.py`

**REQUIREMENTS:**
- 5.4.1 — Remove the stub that returned empty string.
- 5.4.2 — Call `build_system_prompt()` with all parameters from the current decision and packet.
- 5.4.3 — Pass the built prompt as the first system message.
- 5.4.4 — Pass the tool list from `registry.to_ollama_format()` only when `decision.requires_tools=True`.

**SUCCESS CRITERIA:**
- After wiring, LLM responses do not identify the model by its weights name.
- System prompt contains the correct mode fragment.

---

## 🛠️ Phase 6 — Tool System

> **End state:** Any registered skill is callable through the full pipeline: LLM output → parse → registry → safety → validate → execute → ToolResult.

---

### TASK 6.1 — BaseTool class

**DESCRIPTION:** Define the abstract base class all tools must extend.

**INPUT:** A Python class extending `BaseTool`.

**OUTPUT:** Class is discoverable and executable.

**FILES:**
- CREATE: `src/core/tools/base.py`

**REQUIREMENTS:**
- 6.1.1 — Define `BaseTool` as abstract with abstract method `execute(**kwargs) → ToolResult`.
- 6.1.2 — Required class attributes: name, description, category, requires_confirmation, platform.
- 6.1.3 — Define `is_available()` returning `True` by default; subclasses override.
- 6.1.4 — Define `get_schema()` loading JSON Schema from `config/schemas/{category}/{name}.schema.json`; return `{}` if missing.
- 6.1.5 — Define `to_ollama_format()` returning the Ollama tool-calling dict format.

**SUCCESS CRITERIA:**
- A minimal subclass with name, description, category, and `execute()` can be instantiated.
- Instantiating `BaseTool()` directly raises `TypeError`.

---

### TASK 6.2 — Tool registry

**DESCRIPTION:** Implement the registry that scans `src/skills/` and registers all `BaseTool` subclasses.

**INPUT:** `src/skills/` directory.

**OUTPUT:** All available tools registered and accessible by name.

**FILES:**
- CREATE: `src/core/tools/registry.py`

**REQUIREMENTS:**
- 6.2.1 — Define `ToolRegistry` with: `discover()`, `get(name)`, `all_names()`, `all_available()`, `to_ollama_format()`, `get_schema(name)`.
- 6.2.2 — `discover()` uses `pkgutil.walk_packages` to find all modules under `src/skills/`.
- 6.2.3 — `discover()` imports each module and inspects for `BaseTool` subclasses.
- 6.2.4 — `discover()` registers only tools where `is_available()` returns `True`.
- 6.2.5 — `discover()` must be idempotent.
- 6.2.6 — Define a module-level singleton `registry`.
- 6.2.7 — Log the count of registered tools after discovery.

**SUCCESS CRITERIA:**
- `registry.discover()` finds `open_app` tool from Phase 8.
- `registry.get("open_app")` returns the tool instance.
- `registry.get("nonexistent")` returns `None`.

---

### TASK 6.3 — Safety classifier

**DESCRIPTION:** Implement risk classification for tool execution requests.

**INPUT:** Tool name string and args dict.

**OUTPUT:** `SafetyResult` with level and allowed status.

**FILES:**
- CREATE: `src/core/tools/safety.py`

**REQUIREMENTS:**
- 6.3.1 — Define `SafetyResult` as a Pydantic model: level (str), allowed (bool | None), reason (str).
- 6.3.2 — Define `classify_safety(tool_name, args) → SafetyResult`.
- 6.3.3 — Read risk_level from `config/skills.yaml` for the given tool name.
- 6.3.4 — Implement shell command blocklist: scan all string values in `args` for: `rm -rf`, `format c:`, `del /s /q`, `:(){:|:&};:`, `shutdown /`, `mkfs`, `dd if=`.
- 6.3.5 — Blocked pattern match → `allowed=False` regardless of mode.
- 6.3.6 — Do not hardcode tool names — use the manifest exclusively.

**SUCCESS CRITERIA:**
- A `high` risk tool in BALANCED mode returns `allowed=None`.
- A `low` risk tool in BALANCED mode returns `allowed=True`.
- Args containing `"rm -rf"` return `allowed=False`.

---

### TASK 6.4 — Execution mode enforcer

**DESCRIPTION:** Apply the three-mode policy to determine execution permission.

**INPUT:** `SafetyResult`, `execution_mode` string.

**OUTPUT:** `True` (auto-execute), `False` (block), or `"confirm"` (pause for user).

**FILES:**
- CREATE: `src/core/tools/mode_enforcer.py`

**REQUIREMENTS:**
- 6.4.1 — Define `should_execute(safety_result, execution_mode) → bool | str`.
- 6.4.2 — SAFE: return `"confirm"` for all risk levels.
- 6.4.3 — BALANCED: return `True` for low, `"confirm"` for medium, `False` for high.
- 6.4.4 — UNRESTRICTED: return `True` for all risk levels.
- 6.4.5 — Define `is_explicit_override(user_message, tool_name) → bool` checking for `"confirm: {tool_name}"`.

**SUCCESS CRITERIA:**
- `should_execute(high_risk_result, "balanced")` returns `False`.
- `should_execute(low_risk_result, "safe")` returns `"confirm"`.
- `should_execute(high_risk_result, "unrestricted")` returns `True`.

---

### TASK 6.5 — Schema validator

**DESCRIPTION:** Validate tool args against the tool's JSON Schema before execution.

**INPUT:** Args dict, JSON Schema dict.

**OUTPUT:** `None` if valid, error string if invalid.

**FILES:**
- CREATE: `src/core/tools/validator.py`

**REQUIREMENTS:**
- 6.5.1 — Define `validate_args(args, schema) → str | None`.
- 6.5.2 — Check all `required` fields are present.
- 6.5.3 — Check field types match schema declarations for: string, integer, boolean, number.
- 6.5.4 — Do not require the `jsonschema` library — implement manually.
- 6.5.5 — Return a descriptive error string naming the failing field.

**SUCCESS CRITERIA:**
- Valid args matching schema → returns `None`.
- Missing required field → returns error string containing the field name.
- Wrong type for a field → returns error string containing the field name.

---

### TASK 6.6 — Tool executor

**DESCRIPTION:** Implement the single execution gate for all tool calls.

**INPUT:** Tool name string, args dict.

**OUTPUT:** `ToolResult`.

**FILES:**
- CREATE: `src/core/tools/executor.py`

**REQUIREMENTS:**
- 6.6.1 — Define `execute_tool(tool_name, args) → ToolResult`.
- 6.6.2 — Execute the pipeline in order: find → safety → mode enforcement → validate → execute.
- 6.6.3 — Tool not found → `ToolResult(success=False, error="Tool not found")`.
- 6.6.4 — Blocked → `ToolResult(success=False, error="Blocked by safety policy")`.
- 6.6.5 — Confirmation required → prompt terminal; user decline → `ToolResult(success=False, error="User declined")`.
- 6.6.6 — Validation fail → `ToolResult(success=False, error=f"Invalid args: {detail}")`.
- 6.6.7 — Execution exception → `ToolResult(success=False, error=str(exception))`.
- 6.6.8 — Record `duration_ms` on the returned `ToolResult`.
- 6.6.9 — Log `tool.start`, `tool.done` or `tool.error` with duration_ms.

**SUCCESS CRITERIA:**
- `execute_tool("open_app", {"name": "notepad"})` opens Notepad and returns `success=True`.
- `execute_tool("nonexistent", {})` returns `success=False` without raising.
- `execute_tool("delete_file", {"path": "test.txt"})` in BALANCED mode prompts for confirmation.

---

### TASK 6.7 — Tool call parser and retry

**DESCRIPTION:** Implement the retry logic when parse fails on a required tool call.

**INPUT:** Raw LLM output string, `requires_tools` bool.

**OUTPUT:** Valid `LLMOutput` or parse failure indicator.

**FILES:**
- MODIFY: `src/core/runtime/llm_output.py`

**REQUIREMENTS:**
- 6.7.1 — Implement as defined in Task 2.3.
- 6.7.2 — When `requires_tools=True` and parsing fails, the caller must retry the LLM call with an appended instruction stating the required format.
- 6.7.3 — Maximum retries read from `get_settings().runtime.max_tool_retries`.
- 6.7.4 — After max retries, return parse failure indicator (`tool=""`).
- 6.7.5 — The runtime loop must check for the parse failure indicator and return a user-facing error.

**SUCCESS CRITERIA:**
- Valid JSON tool call → `LLMOutput(type="tool_call", tool="open_app")`.
- Plain text when `requires_tools=True` → triggers retry; exhausted retries → parse failure indicator.
- No exception escapes.

---

## 🔒 Phase 7 — Safety Modes

> **End state:** Execution mode is configurable. All tool executions apply the correct policy. Risk levels are present on all tools.

---

### TASK 7.1 — Execution mode in config

**DESCRIPTION:** Add and enforce `execution_mode` in settings.

**INPUT:** `config/settings.yaml` with `runtime.execution_mode` set.

**OUTPUT:** `get_settings().runtime.execution_mode` returns the configured value.

**FILES:**
- MODIFY: `config/settings.example.yaml`
- MODIFY: `src/core/config.py`

**REQUIREMENTS:**
- 7.1.1 — Add `execution_mode` to the `runtime` YAML section with default `"balanced"`.
- 7.1.2 — Add to the `RuntimeConfig` Pydantic model.
- 7.1.3 — Validate that the value is one of: safe, balanced, unrestricted. Reject others.

**SUCCESS CRITERIA:**
- `get_settings().runtime.execution_mode` returns `"balanced"` from default config.
- Setting `execution_mode: "invalid"` raises a Pydantic `ValidationError` on load.

---

### TASK 7.2 — Risk levels audit

**DESCRIPTION:** Verify every tool entry in `config/skills.yaml` has a correct `risk_level`.

**INPUT:** `config/skills.yaml`.

**OUTPUT:** Every entry has a `risk_level` matching README Section 9 exactly.

**FILES:**
- MODIFY: `config/skills.yaml`

**REQUIREMENTS:**
- 7.2.1 — Every entry must have a `risk_level` field.
- 7.2.2 — Values must match README Section 9 Risk Classification table exactly.
- 7.2.3 — No entry may have a missing, empty, or invalid `risk_level`.

**SUCCESS CRITERIA:**
- YAML parses without error.
- Every entry has one of: low, medium, high.

---

### TASK 7.3 — Mode enforcement integration test

**DESCRIPTION:** Verify the three modes produce the correct behavior in the executor.

**INPUT:** Tool calls of different risk levels under each mode.

**OUTPUT:** Correct behavior per mode/risk combination.

**FILES:**
- CREATE: `tests/test_safety_modes.py`

**REQUIREMENTS:**
- 7.3.1 — Test low-risk tool in SAFE mode → confirmation prompt (mock `input()`).
- 7.3.2 — Test low-risk tool in BALANCED mode → auto-executes.
- 7.3.3 — Test high-risk tool in BALANCED mode → blocked.
- 7.3.4 — Test high-risk tool in UNRESTRICTED mode → auto-executes.
- 7.3.5 — Mock actual tool execution — only test the mode enforcement decision.

**SUCCESS CRITERIA:**
- `pytest tests/test_safety_modes.py` passes with 0 failures.

---

### TASK 7.4 — Explicit override phrase

**DESCRIPTION:** Implement and test the high-risk override mechanism for BALANCED mode.

**INPUT:** User message containing `"confirm: {tool_name}"`.

**OUTPUT:** `is_explicit_override()` returns `True`.

**FILES:**
- MODIFY: `src/core/tools/mode_enforcer.py`

**REQUIREMENTS:**
- 7.4.1 — Define `is_explicit_override(user_message, tool_name) → bool`.
- 7.4.2 — Check if the user message exactly matches the pattern `"confirm: {tool_name}"` (case-insensitive).
- 7.4.3 — The executor must call this before blocking a high-risk tool in BALANCED mode.
- 7.4.4 — If override detected, proceed with the confirmation flow rather than blocking.

**SUCCESS CRITERIA:**
- `is_explicit_override("confirm: delete_file", "delete_file")` returns `True`.
- `is_explicit_override("please delete_file", "delete_file")` returns `False`.

---

### TASK 7.5 — Mode change at runtime

**DESCRIPTION:** Allow the execution mode to be changed without restarting.

**INPUT:** A `/mode safe|balanced|unrestricted` command from any interface.

**OUTPUT:** The executor uses the new mode for all subsequent tool calls.

**FILES:**
- CREATE: `src/core/tools/mode_manager.py`

**REQUIREMENTS:**
- 7.5.1 — Maintain the active execution mode in a module-level variable, initialized from `get_settings()`.
- 7.5.2 — Define `get_execution_mode() → str`.
- 7.5.3 — Define `set_execution_mode(mode)` that updates the variable and logs the change.
- 7.5.4 — Reject invalid mode values with a `ValueError`.
- 7.5.5 — The executor must call `get_execution_mode()` rather than reading from settings directly.

**SUCCESS CRITERIA:**
- `set_execution_mode("safe")` then `get_execution_mode()` returns `"safe"`.
- `set_execution_mode("invalid")` raises `ValueError`.

---

## 🖥️ Phase 8 — System Control Skills

> **End state:** OS-level operations work: open/close apps, file operations, clipboard, notifications, screenshots, code execution.

---

### TASK 8.1 — App launcher (BaseTool subclass)

**DESCRIPTION:** Refactor the Phase 0 app launcher as a proper `BaseTool` subclass.

**INPUT:** `{"name": "chrome"}`.

**OUTPUT:** App opens. `ToolResult(success=True)` returned.

**FILES:**
- MODIFY: `src/skills/system/apps.py`

**REQUIREMENTS:**
- 8.1.1 — Define `AppLauncherTool(BaseTool)` with name="open_app".
- 8.1.2 — Define `AppCloseTool(BaseTool)` with name="close_app", requires_confirmation=True.
- 8.1.3 — Wrap existing functions from Phase 0.
- 8.1.4 — `is_available()` must return `True` on all platforms.
- 8.1.5 — Also define: `BringToFrontTool` (name="bring_to_front"), `ListProcessesTool` (name="list_processes").
- 8.1.6 — Create `config/schemas/system/open_app.schema.json`.
- 8.1.7 — Create `config/schemas/system/close_app.schema.json`.

**SUCCESS CRITERIA:**
- `registry.discover()` finds `open_app` and `close_app`.
- `execute_tool("open_app", {"name": "notepad"})` returns `success=True` and Notepad is open.
- `execute_tool("close_app", {"name": "notepad"})` prompts, then closes.

---

### TASK 8.2 — System info and process control

**DESCRIPTION:** Implement tools for system monitoring and process management.

**INPUT:** Various args per tool.

**OUTPUT:** `ToolResult` with system data or operation confirmation.

**FILES:**
- CREATE: `src/skills/system/sysinfo.py`

**REQUIREMENTS:**
- 8.2.1 — Define `SystemInfoTool` (name="system_info"): returns CPU%, RAM used/total GB, disk free GB.
- 8.2.2 — Add GPU VRAM used/total if `pynvml` is available; skip gracefully if not.
- 8.2.3 — Define `KillProcessTool` (name="kill_process", risk_level=high, requires_confirmation=True).
- 8.2.4 — On Windows use `taskkill /IM {name}.exe /F`. On Linux/macOS use `pkill {name}`.
- 8.2.5 — Create JSON Schema files for all tools.

**SUCCESS CRITERIA:**
- `execute_tool("system_info", {})` returns valid numeric CPU and RAM values.
- `execute_tool("kill_process", {"name": "notepad.exe"})` prompts, then closes Notepad.

---

### TASK 8.3 — Clipboard

**DESCRIPTION:** Implement clipboard read and write tools.

**INPUT:** Empty dict (read) or `{"text": "..."}` (write).

**OUTPUT:** `ToolResult` with clipboard content or write confirmation.

**FILES:**
- CREATE: `src/skills/system/clipboard.py`

**REQUIREMENTS:**
- 8.3.1 — Define `ReadClipboardTool` (name="read_clipboard") using `pyperclip`.
- 8.3.2 — Define `WriteClipboardTool` (name="write_clipboard") using `pyperclip`.
- 8.3.3 — Create JSON Schema files for both tools.

**SUCCESS CRITERIA:**
- Copy text in any app. `execute_tool("read_clipboard", {})` returns that text.
- `execute_tool("write_clipboard", {"text": "test"})` → pasting anywhere yields "test".

---

### TASK 8.4 — System notifications

**DESCRIPTION:** Implement a cross-platform notification tool.

**INPUT:** `{"title": "...", "message": "...", "type": "info|success|warning|error"}`.

**OUTPUT:** Notification appears. `ToolResult(success=True)`.

**FILES:**
- CREATE: `src/skills/notify/toasts.py`

**REQUIREMENTS:**
- 8.4.1 — Define `SendNotificationTool` (name="send_notification").
- 8.4.2 — On Windows: use `winotify`. On Linux: use `notify-send`. On macOS: use `osascript`.
- 8.4.3 — On any failure: print to console as fallback and return `success=True`.
- 8.4.4 — Create JSON Schema file.

**SUCCESS CRITERIA:**
- `execute_tool("send_notification", {"title": "Test", "message": "Hello", "type": "info"})` produces a visible notification or console fallback.

---

### TASK 8.5 — Screen capture and OCR

**DESCRIPTION:** Implement screenshot and OCR tools.

**INPUT:** Empty dict (full screen) or `{"region": {"x":0,"y":0,"w":800,"h":600}}`.

**OUTPUT:** `ToolResult` with screenshot path and extracted text.

**FILES:**
- CREATE: `src/skills/screen/capture.py`

**REQUIREMENTS:**
- 8.5.1 — Define `ScreenshotTool` (name="take_screenshot") using `mss`.
- 8.5.2 — Save PNG to `data/screenshots/`.
- 8.5.3 — Define `OCRTool` (name="read_screen_text") combining screenshot + `pytesseract`.
- 8.5.4 — Create JSON Schema files.

**SUCCESS CRITERIA:**
- `execute_tool("take_screenshot", {})` creates a PNG file in `data/screenshots/`.
- `execute_tool("read_screen_text", {})` returns a non-empty text string from a screen with visible text.

---

### TASK 8.6 — File operations

**DESCRIPTION:** Implement file management tools.

**INPUT:** Operation-specific args.

**OUTPUT:** `ToolResult` with file content, confirmation, or error.

**FILES:**
- CREATE: `src/skills/files/file_ops.py`

**REQUIREMENTS:**
- 8.6.1 — Define: `ReadFileTool`, `WriteFileTool`, `ListDirectoryTool`, `SearchFilesTool`, `MoveFileTool`, `CopyFileTool`, `DeleteFileTool`.
- 8.6.2 — `DeleteFileTool`: use `send2trash`, not `os.remove`. Set `requires_confirmation=True`.
- 8.6.3 — All write and delete operations must verify the path is within `ALLOWED_ROOTS` (user home and `data/`).
- 8.6.4 — Return `ToolResult(success=False)` for paths outside allowed roots.
- 8.6.5 — Create JSON Schema files for all tools.

**SUCCESS CRITERIA:**
- `execute_tool("read_file", {"path": "config/settings.yaml"})` returns file content.
- `execute_tool("delete_file", {"path": "data/test.txt"})` after prompting sends file to recycle bin.
- Path outside `ALLOWED_ROOTS` returns `success=False`.

---

### TASK 8.7 — Code execution

**DESCRIPTION:** Implement safe Python and shell code execution.

**INPUT:** `{"language": "python", "code": "print(2+2)"}`.

**OUTPUT:** `ToolResult` with stdout, stderr, and return code.

**FILES:**
- CREATE: `src/skills/coder/executor.py`

**REQUIREMENTS:**
- 8.7.1 — Define `RunPythonTool` (name="execute_python", requires_confirmation=True).
- 8.7.2 — Execute in a subprocess with a configurable timeout (default from settings).
- 8.7.3 — Scan code for blocked patterns before execution: `os.remove`, `shutil.rmtree`, `subprocess.run`, `sys.exit`.
- 8.7.4 — Return `ToolResult(success=False)` if a blocked pattern is found.
- 8.7.5 — Return `ToolResult(success=False)` on timeout.
- 8.7.6 — Create JSON Schema file.

**SUCCESS CRITERIA:**
- Code `print(2+2)` returns `data.stdout = "4\n"` and `success=True`.
- Code containing `os.remove(...)` returns `success=False` without execution.

---

### TASK 8.8 — Web search

**DESCRIPTION:** Implement a web search tool with no API key required.

**INPUT:** `{"query": "latest AI news", "max_results": 5}`.

**OUTPUT:** `ToolResult` with list of results.

**FILES:**
- CREATE: `src/skills/search/web_search.py`

**REQUIREMENTS:**
- 8.8.1 — Define `WebSearchTool` (name="web_search") using DuckDuckGo HTML search.
- 8.8.2 — Return at most `max_results` entries, each with title, url, snippet.
- 8.8.3 — Cache identical queries for 5 minutes using a module-level dict.
- 8.8.4 — Return `ToolResult(success=False)` on network error.
- 8.8.5 — Create JSON Schema file.

**SUCCESS CRITERIA:**
- `execute_tool("web_search", {"query": "Python tutorial"})` returns 5 results with valid URLs.
- Identical query within 5 minutes returns from cache without HTTP request.

---

## 🌐 Phase 9 — Browser & Web Skills

> **End state:** Playwright browser with persistent sessions, downloads, auth wall detection, and WhatsApp automation.

---

### TASK 9.1 — Playwright browser core

**DESCRIPTION:** Implement core browser tools using a singleton Playwright instance.

**INPUT:** URL, selector, or text strings.

**OUTPUT:** `ToolResult` with page state or content.

**FILES:**
- CREATE: `src/skills/browser/browser.py`

**REQUIREMENTS:**
- 9.1.1 — Use a single Playwright Chromium instance (singleton).
- 9.1.2 — Register `atexit` cleanup to close browser on process exit.
- 9.1.3 — Define: `NavigateTool`, `ClickTool`, `FillTool`, `GetTextTool`, `BrowserScreenshotTool`.
- 9.1.4 — `GetTextTool` must return page content as clean text, stripping navigation and ads.
- 9.1.5 — Create JSON Schema files for all tools.

**SUCCESS CRITERIA:**
- `execute_tool("browser_navigate", {"url": "https://example.com"})` returns page title "Example Domain".
- Browser instance persists between consecutive tool calls.

---

### TASK 9.2 — Session persistence

**DESCRIPTION:** Save and load browser sessions so Jarvis stays logged in between restarts.

**INPUT:** Domain string.

**OUTPUT:** Session saved to encrypted file. Loaded on next browser open.

**FILES:**
- CREATE: `src/skills/browser/session.py`

**REQUIREMENTS:**
- 9.2.1 — Define `save_session(domain)` saving Playwright storage state to `data/sessions/{domain}.json`.
- 9.2.2 — Define `load_session(domain)` returning the storage state dict or `None`.
- 9.2.3 — Encrypt session files using Fernet with `SESSION_ENCRYPTION_KEY` from env. Skip encryption if key not set.
- 9.2.4 — Sessions path must come from `get_settings().paths.sessions`.

**SUCCESS CRITERIA:**
- Log into a site. Call `save_session`. Kill Python. Restart. Load session. Navigate to site. Not prompted for login.

---

### TASK 9.3 — File download and upload

**DESCRIPTION:** Implement file download interception and file upload via Playwright.

**INPUT:** URL for download, or selector + path for upload.

**OUTPUT:** `ToolResult` with file path (download) or confirmation (upload).

**FILES:**
- CREATE: `src/skills/browser/transfer.py`

**REQUIREMENTS:**
- 9.3.1 — Define `DownloadTool` (name="browser_download"): intercept download events, save to `data/downloads/`.
- 9.3.2 — Define `UploadTool` (name="browser_upload"): use `page.set_input_files(selector, path)`.
- 9.3.3 — Validate file exists before upload attempt.
- 9.3.4 — Create JSON Schema files.

**SUCCESS CRITERIA:**
- Download a public PDF → file exists in `data/downloads/`.
- Upload a local file via a file input element → DOM state confirms upload.

---

### TASK 9.4 — Auth wall detection

**DESCRIPTION:** Detect login and captcha pages and pause automation.

**INPUT:** Currently open browser page.

**OUTPUT:** User notified. Automation resumes after user signals completion.

**FILES:**
- CREATE: `src/skills/browser/auth_handler.py`

**REQUIREMENTS:**
- 9.4.1 — Define `check_for_auth_wall(page) → bool` checking URL and title for auth keywords.
- 9.4.2 — Auth keywords: login, sign in, تسجيل الدخول, captcha, verify.
- 9.4.3 — Define `handle_auth_wall(page)`: send notification via `send_notification`, block until user presses Enter, save session.
- 9.4.4 — Never silently proceed past an auth wall.

**SUCCESS CRITERIA:**
- Navigating to a login-required page triggers notification and blocks.
- After user presses Enter, session is saved and automation continues.

---

### TASK 9.5 — WhatsApp Web automation

**DESCRIPTION:** Implement sending messages via WhatsApp Web using Playwright.

**INPUT:** `{"contact": "Ahmed", "message": "Hello"}`.

**OUTPUT:** Message sent. `ToolResult(success=True)`.

**FILES:**
- CREATE: `src/skills/social/whatsapp.py`

**REQUIREMENTS:**
- 9.5.1 — Define `WhatsAppSendTool` (name="whatsapp_send", risk_level=high, requires_confirmation=True).
- 9.5.2 — Load session for `web.whatsapp.com`.
- 9.5.3 — If no session: take screenshot of QR, display path to terminal, wait 30 seconds, save session.
- 9.5.4 — Search for contact via WhatsApp search input.
- 9.5.5 — Type and send message.
- 9.5.6 — Create JSON Schema file.

**SUCCESS CRITERIA:**
- `execute_tool("whatsapp_send", {"contact": "Ahmed", "message": "Test"})` after prompting sends the message.

---

### TASK 9.6 — PDF and Office readers

**DESCRIPTION:** Implement document reading tools.

**INPUT:** File path.

**OUTPUT:** `ToolResult` with extracted text.

**FILES:**
- CREATE: `src/skills/pdf/reader.py`
- CREATE: `src/skills/office/reader.py`

**REQUIREMENTS:**
- 9.6.1 — Define `PdfReadTextTool` (name="pdf_read_text") using `pdfplumber`.
- 9.6.2 — Define `DocxReadTool`, `XlsxReadTool`, `PptxReadTool` using respective libraries.
- 9.6.3 — Define `DocxWriteTool` (name="docx_write") for creating simple Word documents.
- 9.6.4 — Create JSON Schema files.

**SUCCESS CRITERIA:**
- `execute_tool("pdf_read_text", {"path": "test.pdf"})` returns non-empty text from a known PDF.
- `execute_tool("docx_read", {"path": "test.docx"})` returns the document text.

---

## 🔌 Phase 10 — Google APIs

> **End state:** One OAuth consent flow grants access to all Google services. Calendar, Gmail, Drive, Contacts, YouTube all work via tool calls.

---

### TASK 10.1 — Unified Google OAuth

**DESCRIPTION:** Implement a single OAuth flow covering all Google API scopes.

**INPUT:** `credentials.json` from Google Cloud Console.

**OUTPUT:** `data/google_token.json` saved. All Google APIs accessible.

**FILES:**
- CREATE: `src/skills/api/google_auth.py`

**REQUIREMENTS:**
- 10.1.1 — Combine scopes for: Calendar, Gmail, Drive, Contacts, YouTube.
- 10.1.2 — Save token to `data/google_token.json`. This file must be in `.gitignore`.
- 10.1.3 — Load and auto-refresh expired token silently.
- 10.1.4 — If token is invalid: open browser for consent, save new token.
- 10.1.5 — Define `get_google_credentials()` returning a valid `Credentials` object.

**SUCCESS CRITERIA:**
- First run: browser opens for consent, token saved.
- Second run: no browser, token loaded from file.

---

### TASK 10.2 — Google Calendar

**DESCRIPTION:** Implement Calendar CRUD operations as tools.

**INPUT:** Action-specific args.

**OUTPUT:** `ToolResult` with event data or confirmation.

**FILES:**
- CREATE: `src/skills/api/calendar.py`

**REQUIREMENTS:**
- 10.2.1 — Define tools: `CalendarListTool`, `CalendarCreateTool`, `CalendarUpdateTool`, `CalendarDeleteTool`, `CalendarSearchTool`.
- 10.2.2 — `CalendarDeleteTool`: requires_confirmation=True, risk_level=high.
- 10.2.3 — All tools must use `get_google_credentials()`.
- 10.2.4 — Create JSON Schema files.

**SUCCESS CRITERIA:**
- Create test event → list → event found. Delete → list again → event gone.

---

### TASK 10.3 — Gmail

**DESCRIPTION:** Implement Gmail read, search, send, and reply as tools.

**INPUT:** Action-specific args.

**OUTPUT:** `ToolResult` with email data or confirmation.

**FILES:**
- CREATE: `src/skills/api/gmail.py`

**REQUIREMENTS:**
- 10.3.1 — Define tools: `GmailListTool`, `GmailSearchTool`, `GmailSendTool`, `GmailReplyTool`, `GmailMarkTool`.
- 10.3.2 — `GmailSendTool` and `GmailReplyTool`: requires_confirmation=True, risk_level=high.
- 10.3.3 — Create JSON Schema files.

**SUCCESS CRITERIA:**
- Send email to self → appears in inbox. Search → found. Mark read → unread count decreases.

---

### TASK 10.4 — Google Drive

**DESCRIPTION:** Implement Drive file management as tools.

**INPUT:** Action-specific args.

**OUTPUT:** `ToolResult` with file data or confirmation.

**FILES:**
- CREATE: `src/skills/api/drive.py`

**REQUIREMENTS:**
- 10.4.1 — Define tools: `DriveListTool`, `DriveSearchTool`, `DriveUploadTool`, `DriveDownloadTool`, `DriveShareTool`.
- 10.4.2 — Save downloads to `data/downloads/`.
- 10.4.3 — Create JSON Schema files.

**SUCCESS CRITERIA:**
- Upload a local file → appears in Drive. Download it back → content matches.

---

### TASK 10.5 — Google Contacts

**DESCRIPTION:** Implement Contacts lookup and name-to-email resolution.

**INPUT:** Search query or contact fields.

**OUTPUT:** `ToolResult` with contact data.

**FILES:**
- CREATE: `src/skills/api/contacts.py`

**REQUIREMENTS:**
- 10.5.1 — Define tools: `ContactsSearchTool`, `ContactsGetTool`, `ContactsCreateTool`.
- 10.5.2 — Define `resolve_name(name) → str | None` returning the email for a given name.
- 10.5.3 — Create JSON Schema files.

**SUCCESS CRITERIA:**
- Search known contact by name → email returned.
- "Send email to Ahmed" → Contacts resolves name → Gmail sends to correct address.

---

### TASK 10.6 — YouTube

**DESCRIPTION:** Implement YouTube search and video opening.

**INPUT:** Search query or video ID.

**OUTPUT:** `ToolResult` with video data or browser opened.

**FILES:**
- CREATE: `src/skills/api/youtube.py`

**REQUIREMENTS:**
- 10.6.1 — Define tools: `YouTubeSearchTool`, `YouTubeGetInfoTool`, `YouTubeOpenTool`.
- 10.6.2 — Create JSON Schema files.

**SUCCESS CRITERIA:**
- `execute_tool("youtube_search", {"query": "machine learning"})` returns 5 results with valid URLs.

---

### TASK 10.7 — Media and Network tools

**DESCRIPTION:** Implement media control and network info tools.

**INPUT:** Action-specific args.

**OUTPUT:** `ToolResult` with confirmation or data.

**FILES:**
- CREATE: `src/skills/media/player.py`
- CREATE: `src/skills/network/network.py`

**REQUIREMENTS:**
- 10.7.1 — Define `SetVolumeTool` (name="set_volume"): platform-specific volume control.
- 10.7.2 — Define `PlayPauseTool` (name="play_pause"): system media key.
- 10.7.3 — Define `CheckConnectionTool` (name="check_connection"): ping test.
- 10.7.4 — Define `GetIPTool` (name="get_ip"): local and public IP.
- 10.7.5 — Create JSON Schema files.

**SUCCESS CRITERIA:**
- `execute_tool("set_volume", {"level": 50})` sets system volume to 50%.
- `execute_tool("check_connection", {})` returns `True` when internet is available.

---

## 💾 Phase 11 — Context + Memory

> **End state:** Facts told in session 1 are recalled in session 2. Memory is injected into every turn. Feedback collected.

---

### TASK 11.1 — Short-term memory

**DESCRIPTION:** Implement session history using Redis with in-memory fallback.

**INPUT:** Role string, content string, session ID.

**OUTPUT:** Message saved. Retrievable after restart (with Redis).

**FILES:**
- CREATE: `src/core/memory/short_term.py`

**REQUIREMENTS:**
- 11.1.1 — Define `save_message(session_id, role, content)`.
- 11.1.2 — Define `get_history(session_id, n=10) → list[dict]`.
- 11.1.3 — Use Redis as primary backend. On connection failure: switch to in-memory dict and log warning.
- 11.1.4 — Set Redis TTL to 24 hours per session key.
- 11.1.5 — Trim to last 50 messages per session.

**SUCCESS CRITERIA:**
- Save 3 messages. `get_history()` returns all 3 in order.
- With Redis: restart Python. `get_history()` still returns the 3 messages.
- Without Redis: in-memory fallback works without crashing.

---

### TASK 11.2 — Long-term semantic memory

**DESCRIPTION:** Implement persistent semantic memory using ChromaDB.

**INPUT:** Text string and metadata dict.

**OUTPUT:** Stored and retrievable via semantic search.

**FILES:**
- CREATE: `src/core/memory/long_term.py`

**REQUIREMENTS:**
- 11.2.1 — Define `remember(text, metadata)` adding to ChromaDB collection.
- 11.2.2 — Define `recall(query, n=5) → list[str]` returning top-N semantically similar snippets.
- 11.2.3 — Use `sentence-transformers` for embeddings.
- 11.2.4 — Persist to `data/chroma/`.

**SUCCESS CRITERIA:**
- `remember("User prefers concise Arabic answers")`. Restart Python. `recall("user preferences")` returns that text.

---

### TASK 11.3 — SQLite store

**DESCRIPTION:** Implement the structured relational store.

**INPUT:** SQL operations via wrapper functions.

**OUTPUT:** Data persists across restarts.

**FILES:**
- CREATE: `src/core/memory/database.py`

**REQUIREMENTS:**
- 11.3.1 — Create tables on init: conversations, feedback, tasks.
- 11.3.2 — Define `insert_conversation(session_id, role, content)`.
- 11.3.3 — Define `insert_feedback(session_id, model, mode, score)`.
- 11.3.4 — Auto-create tables if missing. Migration-safe (additive only).

**SUCCESS CRITERIA:**
- Insert one row per table. Restart Python. Query all tables. Rows present.

---

### TASK 11.4 — Memory injection into context assembler

**DESCRIPTION:** Wire memory retrieval into `assemble_context()`.

**INPUT:** User message and session ID.

**OUTPUT:** `InputPacket` with `memory_snippets` and `recent_history` populated.

**FILES:**
- MODIFY: `src/core/context/assembler.py`

**REQUIREMENTS:**
- 11.4.1 — Call `get_history(session_id, n=10)` and assign to `recent_history`.
- 11.4.2 — Call `recall(user_message, n=3)` and assign to `memory_snippets`.
- 11.4.3 — Both calls must fail gracefully (empty list returned if backend unavailable).

**SUCCESS CRITERIA:**
- Tell Jarvis "my name is Ahmed" in turn 1. Turn 2: "what is my name?" returns "Ahmed".

---

### TASK 11.5 — Auto-save after turns

**DESCRIPTION:** Save every turn to memory stores after `run_turn()` completes.

**INPUT:** Completed turn data.

**OUTPUT:** User message and response saved to short-term, SQLite, and long-term memory.

**FILES:**
- MODIFY: `src/core/runtime/loop.py`

**REQUIREMENTS:**
- 11.5.1 — After every turn: call `save_message(session_id, "user", user_input)`.
- 11.5.2 — After every turn: call `save_message(session_id, "assistant", response_text)`.
- 11.5.3 — After every turn: call `insert_conversation()` for both messages.
- 11.5.4 — When `eval.quality > 0.8`: call `remember()` with the outcome.

**SUCCESS CRITERIA:**
- Run 5 turns. SQLite `conversations` table has 10 rows.

---

### TASK 11.6 — Feedback collection and weight updates

**DESCRIPTION:** Collect turn outcomes and update routing weights.

**INPUT:** Turn quality score and model/mode used.

**OUTPUT:** Feedback rows in SQLite. Routing weights updated every 20 turns.

**FILES:**
- CREATE: `src/core/memory/feedback.py`
- CREATE: `src/core/decision/weight_updater.py`

**REQUIREMENTS:**
- 11.6.1 — Define `record_feedback(session_id, model, mode, intent, score)` inserting into the feedback table.
- 11.6.2 — Call `record_feedback()` from `run_turn()` after evaluation.
- 11.6.3 — Every 20 turns: compute average score per (intent, model) pair and nudge weights via exponential moving average.
- 11.6.4 — Max delta per update: ±0.15 to prevent thrashing.

**SUCCESS CRITERIA:**
- 5 turns → 5 rows in feedback table.
- After simulating poor performance on code tasks with `gemma3:4b`, that pair's weight decreases.

---

## 🤖 Phase 12 — Agents

> **End state:** Multi-step goals execute autonomously without step-by-step guidance.

---

### TASK 12.1 — Thinker agent

**DESCRIPTION:** Implement chain-of-thought reasoning with self-critique.

**INPUT:** A complex question string.

**OUTPUT:** Higher-quality answer than a direct LLM call.

**FILES:**
- CREATE: `src/core/agents/thinker.py`

**REQUIREMENTS:**
- 12.1.1 — Define `think(question, model) → str`.
- 12.1.2 — Use a system prompt that requires: reasoning steps, then answer, then self-critique.
- 12.1.3 — Extract the final answer from the response after the self-critique marker.

**SUCCESS CRITERIA:**
- `think("trade-offs between RAG and fine-tuning")` produces a more detailed answer than direct `chat()` on the same question.

---

### TASK 12.2 — Planner agent

**DESCRIPTION:** Decompose a complex goal into ordered executable steps.

**INPUT:** Goal string and list of available tool names.

**OUTPUT:** Ordered list of step dicts with: id, description, tool, args, depends_on.

**FILES:**
- CREATE: `src/core/agents/planner.py`

**REQUIREMENTS:**
- 12.2.1 — Define `plan(goal, available_tools) → list[dict]`.
- 12.2.2 — Use `qwen3:8b` in planning mode.
- 12.2.3 — System prompt must instruct the model to return a JSON array of step objects.
- 12.2.4 — Handle JSON parse failure with retry (max 2).

**SUCCESS CRITERIA:**
- `plan("search AI news and save to file", ["web_search", "write_file"])` returns 2+ steps in dependency order.

---

### TASK 12.3 — Step executor

**DESCRIPTION:** Execute a planned step list with dependency-based output passing.

**INPUT:** List of step dicts from the planner.

**OUTPUT:** All steps executed. Results from each step available to dependent steps.

**FILES:**
- CREATE: `src/core/agents/step_executor.py`

**REQUIREMENTS:**
- 12.3.1 — Define `execute_plan(steps) → dict` returning results keyed by step ID.
- 12.3.2 — Execute in topological order based on `depends_on` field.
- 12.3.3 — Inject results from prior steps into args of dependent steps.

**SUCCESS CRITERIA:**
- 3-step plan (search → summarize → save) executes fully. File exists with search content after completion.

---

### TASK 12.4 — Researcher agent

**DESCRIPTION:** Implement multi-source web research producing a structured report.

**INPUT:** Research topic string.

**OUTPUT:** Markdown report with content from multiple sources.

**FILES:**
- CREATE: `src/core/agents/researcher.py`

**REQUIREMENTS:**
- 12.4.1 — Define `research(topic) → str` returning a Markdown report.
- 12.4.2 — Generate 3 distinct search queries from the topic via LLM.
- 12.4.3 — Search each query, fetch the top result content.
- 12.4.4 — Summarize and combine sources via LLM.

**SUCCESS CRITERIA:**
- `research("local AI 2025")` returns Markdown with content from at least 3 distinct URLs.

---

### TASK 12.5 — Computer use agent

**DESCRIPTION:** Implement autonomous screen observation and action loop.

**INPUT:** A goal string.

**OUTPUT:** Goal accomplished or failure message.

**FILES:**
- CREATE: `src/core/agents/computer_use.py`

**REQUIREMENTS:**
- 12.5.1 — Define `computer_use(goal) → str` looping: screenshot → describe/OCR → decide action → execute.
- 12.5.2 — Max iterations: read from config.
- 12.5.3 — All pyautogui actions require confirmation.
- 12.5.4 — Return a success or failure string.

**SUCCESS CRITERIA:**
- Goal "open Notepad and type hello" → Notepad opens → "hello" typed → success returned.

---

## 💻 Phase 13 — CLI Interface

> **End state:** `python app/main.py --interface cli` shows a Rich terminal chat. Arabic RTL. Slash commands work.

---

### TASK 13.1 — Rich streaming chat loop

**DESCRIPTION:** Implement the terminal chat interface.

**INPUT:** User types in terminal.

**OUTPUT:** Streaming response rendered with Rich.

**FILES:**
- CREATE: `src/interfaces/cli/interface.py`

**REQUIREMENTS:**
- 13.1.1 — Define `run_cli(cfg)` as the main loop.
- 13.1.2 — Use `rich.live.Live` to stream response tokens.
- 13.1.3 — Detect Arabic text by counting Arabic-range characters (above 30% → RTL).
- 13.1.4 — Apply RTL alignment for Arabic messages.
- 13.1.5 — Handle `KeyboardInterrupt` and `EOFError` cleanly.

**SUCCESS CRITERIA:**
- Arabic message → response with RTL alignment.
- Streaming shows tokens appearing progressively.
- Ctrl+C exits without traceback.

---

### TASK 13.2 — Slash commands

**DESCRIPTION:** Implement all slash command handlers.

**INPUT:** Commands starting with `/`.

**OUTPUT:** Command executes and output printed.

**FILES:**
- CREATE: `src/interfaces/cli/commands.py`

**REQUIREMENTS:**
- 13.2.1 — Handle: `/clear`, `/model`, `/mode`, `/memory`, `/tools`, `/status`, `/profile`, `/config`, `/help`.
- 13.2.2 — `/clear` asks for confirmation before clearing history.
- 13.2.3 — `/model` validates against available models.
- 13.2.4 — `/mode` calls `set_execution_mode()` or sets thinking mode depending on value.
- 13.2.5 — `/tools` lists all registered tools with name, description, risk_level.

**SUCCESS CRITERIA:**
- All 9 commands execute without error.
- `/model invalid_name` returns an error without crashing.

---

### TASK 13.3 — Global hotkeys

**DESCRIPTION:** Register system-wide keyboard shortcuts.

**INPUT:** Hotkey pressed anywhere on the OS.

**OUTPUT:** Configured action fires.

**FILES:**
- CREATE: `src/interfaces/cli/hotkeys.py`

**REQUIREMENTS:**
- 13.3.1 — Read hotkey bindings from `get_settings().hotkeys`.
- 13.3.2 — Register in a background thread at CLI startup.
- 13.3.3 — On failure: log warning and continue without the hotkey (no crash).

**SUCCESS CRITERIA:**
- Ctrl+Alt+J (or configured hotkey) from another window brings CLI to focus.
- CLI starts successfully even if hotkey registration fails.

---

### TASK 13.4 — Input history

**DESCRIPTION:** Persist CLI input history across sessions.

**INPUT:** Arrow up/down keys during input.

**OUTPUT:** Previous inputs recalled.

**FILES:**
- MODIFY: `src/interfaces/cli/interface.py`

**REQUIREMENTS:**
- 13.4.1 — Store each user input to `data/cli_history.txt`.
- 13.4.2 — Load history on startup.
- 13.4.3 — Support up/down arrow navigation through history.

**SUCCESS CRITERIA:**
- Type 3 messages. Press up 3 times. All 3 recalled in reverse order. Survives restart.

---

### TASK 13.5 — Status bar

**DESCRIPTION:** Display runtime status after each response.

**INPUT:** Current session state.

**OUTPUT:** One-line status bar showing model, mode, and turn count.

**FILES:**
- MODIFY: `src/interfaces/cli/interface.py`

**REQUIREMENTS:**
- 13.5.1 — Display after each response: active model, current mode, turn count, session ID.
- 13.5.2 — Update automatically — never requires user command.

**SUCCESS CRITERIA:**
- Status bar updates after every turn with correct values.

---

## 🌐 Phase 14 — Web UI

> **End state:** Browser chat at localhost:8080 with streaming, RTL Arabic support, file upload, conversation sidebar.

---

### TASK 14.1 — FastAPI app and WebSocket endpoint

**DESCRIPTION:** Create the web server and WebSocket handler.

**INPUT:** Browser connects to `http://localhost:8080`.

**OUTPUT:** Chat page loads. Messages stream in real time.

**FILES:**
- CREATE: `src/interfaces/web/app.py`
- CREATE: `src/interfaces/web/ws.py`
- CREATE: `app/server.py`

**REQUIREMENTS:**
- 14.1.1 — FastAPI app serving static files and templates.
- 14.1.2 — WebSocket endpoint at `/ws/{session_id}`.
- 14.1.3 — Receive JSON message with `message` and `mode` fields.
- 14.1.4 — Stream tokens back as `{"type": "token", "data": "..."}` frames.
- 14.1.5 — Send `{"type": "done"}` after all tokens.
- 14.1.6 — Handle disconnection gracefully.

**SUCCESS CRITERIA:**
- Navigate to localhost:8080 → chat page loads.
- Send message → streamed response appears.

---

### TASK 14.2 — HTML structure

**DESCRIPTION:** Create the single-page chat application HTML skeleton.

**INPUT:** Browser request.

**OUTPUT:** All structural elements rendered.

**FILES:**
- CREATE: `src/interfaces/web/templates/index.html`

**REQUIREMENTS:**
- 14.2.1 — Elements required: sidebar (conversation list, search, settings), main area (header, messages, input bar), toast container.
- 14.2.2 — Input bar elements: attachment button, mode selector row, text area, send/mic button.
- 14.2.3 — No JavaScript in this file beyond minimal DOM setup.

**SUCCESS CRITERIA:**
- All structural elements present in DOM on page load.
- No JavaScript errors in browser console.

---

### TASK 14.3 — CSS: design system

**DESCRIPTION:** Implement the complete visual design system.

**INPUT:** Browser renders the page.

**OUTPUT:** Glassmorphism dark UI with all components styled.

**FILES:**
- CREATE: `src/interfaces/web/static/style.css`

**REQUIREMENTS:**
- 14.3.1 — Define all CSS custom properties: background colors, glass effects, accent gradient, text colors, radii, fonts.
- 14.3.2 — Dark theme default. Light theme as `[data-theme="light"]` overrides.
- 14.3.3 — Glass panels: `backdrop-filter: blur()`, semi-transparent background, subtle border.
- 14.3.4 — Message bubbles: user (accent gradient), assistant (glass panel).
- 14.3.5 — Input bar: auto-expanding textarea, mode selector buttons, dynamic send/mic button.
- 14.3.6 — Toast notifications: 4 types (success, error, info, warning) with slide-in animation.
- 14.3.7 — Responsive layout for mobile and desktop.
- 14.3.8 — Arabic messages apply RTL direction and Arabic font.

**SUCCESS CRITERIA:**
- Dark theme renders correctly.
- Arabic text in a message bubble renders right-to-left.
- Mode buttons visually distinct when active.

---

### TASK 14.4 — JavaScript: WebSocket and streaming

**DESCRIPTION:** Implement client-side WebSocket connection and token streaming.

**INPUT:** User sends a message.

**OUTPUT:** Tokens appear progressively. RTL detected automatically.

**FILES:**
- CREATE: `src/interfaces/web/static/chat.js`

**REQUIREMENTS:**
- 14.4.1 — Establish WebSocket connection on page load.
- 14.4.2 — Reconnect automatically with exponential backoff (1s, 2s, 4s, 8s, max 30s).
- 14.4.3 — Display connection status indicator (green/yellow/red dot).
- 14.4.4 — Append tokens as they arrive. Show cursor animation during streaming.
- 14.4.5 — Detect RTL: if more than 30% Arabic characters → apply `direction: rtl`.
- 14.4.6 — Render Markdown in assistant responses.
- 14.4.7 — Add syntax highlighting to code blocks with copy button.
- 14.4.8 — Scroll to bottom on new messages.

**SUCCESS CRITERIA:**
- Arabic response renders RTL.
- Streaming tokens appear progressively.
- Reconnect after server restart.

---

### TASK 14.5 — JavaScript: input bar interactions

**DESCRIPTION:** Implement all input bar behaviors.

**INPUT:** User interacts with input controls.

**OUTPUT:** Message sent with correct mode and attachments.

**FILES:**
- MODIFY: `src/interfaces/web/static/chat.js`

**REQUIREMENTS:**
- 14.5.1 — Mode selector: 5 buttons (fast, normal, deep, planning, research). Active state on click. Mode sent with message.
- 14.5.2 — Textarea: auto-expand up to 8 lines. Enter sends. Shift+Enter adds newline.
- 14.5.3 — Send/mic button: empty input → mic icon. Typing → send arrow. Smooth morph.
- 14.5.4 — Attachment menu: upload file, upload image, paste clipboard image.
- 14.5.5 — Drag-and-drop file onto chat area → auto-attach.
- 14.5.6 — Attachment preview strip above input with remove button per item.

**SUCCESS CRITERIA:**
- Mode selection updates server behavior (verify via model indicator).
- Drag file → preview card appears → send → server receives attachment.

---

### TASK 14.6 — REST API routes

**DESCRIPTION:** Implement all REST endpoints for conversation management.

**INPUT:** HTTP requests from browser JavaScript.

**OUTPUT:** JSON responses.

**FILES:**
- CREATE: `src/interfaces/web/routes.py`

**REQUIREMENTS:**
- 14.6.1 — Implement: `GET /`, `GET /api/conversations`, `GET /api/conversations/:id`, `PUT /api/conversations/:id`, `DELETE /api/conversations/:id`.
- 14.6.2 — Implement: `DELETE /api/memory`, `POST /api/upload`, `GET /api/settings`, `PUT /api/settings`, `GET /api/status`.
- 14.6.3 — `/api/status` must return: active model, execution mode, VRAM used/total (if available), registered tool count.
- 14.6.4 — `/api/upload` saves file to `data/temp/`, returns `{id, name, type, size}`.

**SUCCESS CRITERIA:**
- All endpoints return correct HTTP status codes.
- `/api/status` returns valid JSON with current system state.

---

### TASK 14.7 — Sidebar: conversations and search

**DESCRIPTION:** Implement the conversation history sidebar.

**INPUT:** User interacts with conversation list.

**OUTPUT:** History shown, search works, CRUD operations complete.

**FILES:**
- MODIFY: `src/interfaces/web/static/chat.js`

**REQUIREMENTS:**
- 14.7.1 — Load and display conversation list grouped by date: Today, Yesterday, Previous 7 days, Older.
- 14.7.2 — New conversation button, inline rename, delete with confirmation, pin.
- 14.7.3 — Search: filter by title on keystroke, by content via server-side call.
- 14.7.4 — Keyboard shortcut Ctrl+K opens search.
- 14.7.5 — Persist expanded/collapsed state in localStorage.

**SUCCESS CRITERIA:**
- Create 5 conversations. Rename one. Pin one. Delete one. All operations persist after page reload.
- Search "test" filters the list to matching conversations.

---

### TASK 14.8 — Settings panel and feedback

**DESCRIPTION:** Implement the settings panel and per-message feedback.

**INPUT:** User interacts with settings or feedback buttons.

**OUTPUT:** Settings saved. Feedback recorded in database.

**FILES:**
- MODIFY: `src/interfaces/web/static/chat.js`

**REQUIREMENTS:**
- 14.8.1 — Settings panel sections: Appearance (theme, font size), Behavior (default mode, language, enter key), Model (active model, temperature), Data (export, clear).
- 14.8.2 — All settings persist in localStorage and apply immediately.
- 14.8.3 — Per-message 👍/👎 buttons visible on hover. Click → POST to `/api/feedback` → toast confirmation.
- 14.8.4 — Toast notifications: 4 types, auto-dismiss after 4 seconds.

**SUCCESS CRITERIA:**
- Toggle theme → changes immediately. Persists on reload.
- Click 👍 → feedback recorded → toast appears.

---

## 🎙️ Phase 15 — Voice Pipeline

> **End state:** "Hey Jarvis" → speak command → hear spoken answer.

---

### TASK 15.1 — Whisper STT

**DESCRIPTION:** Implement speech-to-text using Whisper.

**INPUT:** Audio from microphone.

**OUTPUT:** Transcribed text with detected language.

**FILES:**
- CREATE: `src/models/speech/stt.py`

**REQUIREMENTS:**
- 15.1.1 — Load `whisper.load_model("medium")` once at import, cached.
- 15.1.2 — Define `record_audio(duration) → numpy array` capturing from default microphone.
- 15.1.3 — Define `transcribe(audio_array) → dict` with keys: text, language.
- 15.1.4 — Auto-detect language.

**SUCCESS CRITERIA:**
- 5 seconds of Arabic speech → correct Arabic transcription.
- 5 seconds of English speech → correct English transcription.

---

### TASK 15.2 — Piper TTS

**DESCRIPTION:** Implement text-to-speech using Piper.

**INPUT:** Text string and language string.

**OUTPUT:** Audio played through speakers.

**FILES:**
- CREATE: `src/models/speech/tts.py`

**REQUIREMENTS:**
- 15.2.1 — Load Arabic voice model (`ar_JO-kareem-medium.onnx`) and English voice model.
- 15.2.2 — Define `speak(text, language)` synthesizing and playing audio.
- 15.2.3 — Auto-select voice based on language parameter.

**SUCCESS CRITERIA:**
- `speak("مرحباً", "ar")` produces natural Arabic audio.
- `speak("Hello", "en")` produces natural English audio.

---

### TASK 15.3 — Wake word detection

**DESCRIPTION:** Implement continuous wake word monitoring.

**INPUT:** Continuous microphone audio.

**OUTPUT:** EventBus event emitted when "Hey Jarvis" detected.

**FILES:**
- CREATE: `src/interfaces/voice/wake_word.py`

**REQUIREMENTS:**
- 15.3.1 — Load openWakeWord model for "hey_jarvis".
- 15.3.2 — Process audio in 1280-frame chunks.
- 15.3.3 — Trigger when score exceeds 0.5.
- 15.3.4 — Emit `bus.emit("wake_word", {})` on detection.

**SUCCESS CRITERIA:**
- "Hey Jarvis" spoken → event fires within 1 second.
- 60 seconds of random speech → no false triggers.

---

### TASK 15.4 — Voice Activity Detection

**DESCRIPTION:** Auto-stop recording when the user stops speaking.

**INPUT:** Microphone stream post-wake-word.

**OUTPUT:** Audio segment ending at speech completion.

**FILES:**
- CREATE: `src/interfaces/voice/vad.py`

**REQUIREMENTS:**
- 15.4.1 — Use `webrtcvad` at aggressiveness level 2.
- 15.4.2 — Stop recording after 1 second of continuous silence.
- 15.4.3 — Define `record_with_vad() → numpy array`.

**SUCCESS CRITERIA:**
- Speak 3 seconds, pause 1 second → recording stops. Audio array length corresponds to speech duration.

---

### TASK 15.5 — Full voice pipeline

**DESCRIPTION:** Integrate all voice components into one pipeline.

**INPUT:** "Hey Jarvis" spoken by user.

**OUTPUT:** Spoken response from Jarvis.

**FILES:**
- CREATE: `src/interfaces/voice/pipeline.py`

**REQUIREMENTS:**
- 15.5.1 — Define `run_voice_pipeline(cfg)` looping: wait for wake word → record with VAD → transcribe → `run_turn()` → speak.
- 15.5.2 — Play an activation chime after wake word detection.
- 15.5.3 — Auto-select TTS language from transcription result.

**SUCCESS CRITERIA:**
- "Hey Jarvis, what is the capital of Egypt?" → spoken answer within 15 seconds.

---

## 👁️ Phase 16 — Vision + Image Generation

> **End state:** Images are understood and described. Text prompts produce generated images.

---

### TASK 16.1 — LLaVA image understanding

**DESCRIPTION:** Implement image description using LLaVA via Ollama.

**INPUT:** Image path and optional question string.

**OUTPUT:** Text description.

**FILES:**
- CREATE: `src/models/vision/llava.py`

**REQUIREMENTS:**
- 16.1.1 — Define `describe_image(image_path, question) → str`.
- 16.1.2 — Encode image as base64 for Ollama vision API.
- 16.1.3 — Swap to `llava:7b` before calling. VRAM guard applies.
- 16.1.4 — No exception on valid image path.

**SUCCESS CRITERIA:**
- Screenshot of code → LLaVA identifies the programming language.
- Arabic text in image → LLaVA reads the text correctly.

---

### TASK 16.2 — Stable Diffusion image generation

**DESCRIPTION:** Implement image generation using Stable Diffusion 1.5.

**INPUT:** Prompt string (any language).

**OUTPUT:** Generated PNG file path.

**FILES:**
- CREATE: `src/models/diffusion/sd.py`

**REQUIREMENTS:**
- 16.2.1 — Define `generate_image(prompt, steps, width, height) → str`.
- 16.2.2 — Translate Arabic prompts to English via LLM before generation.
- 16.2.3 — Unload the current LLM before loading SD. Unload SD after generation.
- 16.2.4 — Save output to `data/generated/`.

**SUCCESS CRITERIA:**
- English prompt → PNG file created in `data/generated/`.
- Arabic prompt → translated and image generated.
- VRAM released after generation.

---

### TASK 16.3 — Vision integration into runtime

**DESCRIPTION:** Wire image understanding into context assembly.

**INPUT:** `InputPacket` with image attachment.

**OUTPUT:** LLaVA description included in `memory_snippets`.

**FILES:**
- MODIFY: `src/core/context/assembler.py`

**REQUIREMENTS:**
- 16.3.1 — When `attachments` contains image paths, call `describe_image()` for each.
- 16.3.2 — Append descriptions to `memory_snippets`.
- 16.3.3 — Only call LLaVA if the image path exists and is valid.

**SUCCESS CRITERIA:**
- Upload a chart image. Ask "what trend does this show?" → answer based on image content.

---

### TASK 16.4 — Screen description tool

**DESCRIPTION:** Implement a tool that describes the current screen using LLaVA.

**INPUT:** Empty dict or question string.

**OUTPUT:** `ToolResult` with screen description.

**FILES:**
- CREATE: `src/skills/screen/describe.py`

**REQUIREMENTS:**
- 16.4.1 — Define `DescribeScreenTool` (name="describe_screen").
- 16.4.2 — Take screenshot via `ScreenshotTool`, then call `describe_image()`.
- 16.4.3 — Create JSON Schema file.

**SUCCESS CRITERIA:**
- `execute_tool("describe_screen", {})` returns an accurate description of visible content.

---

## 📱 Phase 17 — Telegram + GUI

> **End state:** Telegram bot handles all message types. PyQt6 desktop app with tray icon works.

---

### TASK 17.1 — Telegram bot

**DESCRIPTION:** Implement the Telegram bot handling text, photo, voice, and document messages.

**INPUT:** Various Telegram message types.

**OUTPUT:** Jarvis responds correctly to each type.

**FILES:**
- CREATE: `src/interfaces/telegram/bot.py`
- CREATE: `src/interfaces/telegram/handlers.py`
- CREATE: `src/interfaces/telegram/commands.py`

**REQUIREMENTS:**
- 17.1.1 — Text messages → `run_turn()` → reply.
- 17.1.2 — Photos → download → `describe_image()` → reply.
- 17.1.3 — Voice notes → download → `transcribe()` → `run_turn()` → reply.
- 17.1.4 — Documents → download → appropriate reader tool → summary reply.
- 17.1.5 — Commands: `/start`, `/clear`, `/model`, `/mode`, `/image`, `/search`.

**SUCCESS CRITERIA:**
- Arabic voice note → correct transcription and answer.
- Photo upload → image described in user's language.

---

### TASK 17.2 — PyQt6 desktop app

**DESCRIPTION:** Implement the native desktop chat window.

**INPUT:** User interaction with desktop window.

**OUTPUT:** Chat works. Arabic RTL correct.

**FILES:**
- CREATE: `src/interfaces/gui/main_window.py`
- CREATE: `src/interfaces/gui/settings_dialog.py`

**REQUIREMENTS:**
- 17.2.1 — Scrollable chat area, expanding input, send and mic buttons.
- 17.2.2 — Model dropdown populated from available models.
- 17.2.3 — Mode toolbar with 5 mode options.
- 17.2.4 — Arabic text in chat bubble renders RTL.

**SUCCESS CRITERIA:**
- Arabic message → RTL rendering correct.
- Voice button activates STT and sends transcription.

---

### TASK 17.3 — System tray

**DESCRIPTION:** Run Jarvis as a background daemon with system tray icon.

**INPUT:** App started with `--background` flag or minimized.

**OUTPUT:** Tray icon visible. Wake word active in background.

**FILES:**
- CREATE: `src/interfaces/gui/tray.py`
- CREATE: `src/interfaces/gui/autostart.py`

**REQUIREMENTS:**
- 17.3.1 — Pystray icon with right-click menu: Open GUI, Open Web UI, Settings, Quit.
- 17.3.2 — Wake word listener runs in background thread.
- 17.3.3 — Wake word detection brings GUI window to front.
- 17.3.4 — Define `set_autostart(enabled)` for platform-specific auto-start registration.

**SUCCESS CRITERIA:**
- App in tray. "Hey Jarvis" → GUI window appears.
- Toggle auto-start → registry/plist entry added/removed.

---

### TASK 17.4 — Task decomposition

**DESCRIPTION:** Implement DAG-based task execution with parallel steps and selective retry.

**INPUT:** Goal string.

**OUTPUT:** All subtasks executed. Only failed subtasks retry.

**FILES:**
- CREATE: `src/core/agents/decomposer.py`
- CREATE: `src/core/agents/graph_executor.py`

**REQUIREMENTS:**
- 17.4.1 — Define `Subtask` with fields: id, title, tool, args, depends_on, status, result.
- 17.4.2 — Define `decompose(goal) → TaskGraph` using LLM in planning mode.
- 17.4.3 — Define `execute_graph(graph) → dict` using topological sort and `asyncio.gather()` for the parallel frontier.
- 17.4.4 — Save graph state to SQLite after each subtask. Define `resume(run_id)` to restart from checkpoint.

**SUCCESS CRITERIA:**
- 3 independent tasks show concurrent execution in logs.
- Force-fail one task. Call retry. Only that task re-runs.
- Kill process mid-execution. Resume with same `run_id`. Skips completed tasks.

---

## ✅ Phase 18 — QA + Security

> **End state:** All tests pass. No credentials in logs. Performance benchmarks met.

---

### TASK 18.1 — Test suite structure

**DESCRIPTION:** Create all test files covering every phase.

**INPUT:** `pytest tests/` command.

**OUTPUT:** All tests pass. Coverage ≥ 70%.

**FILES:**
- CREATE: `tests/test_contracts.py` (Phase 2)
- CREATE: `tests/test_decision.py` (Phase 4)
- CREATE: `tests/test_safety_modes.py` (Phase 7)
- CREATE: `tests/test_runtime.py` (Phase 3)
- CREATE: `tests/test_tools.py` (Phase 6)
- CREATE: `tests/test_skills.py` (Phases 8–10)
- CREATE: `tests/test_memory.py` (Phase 11)
- CREATE: `tests/test_agents.py` (Phase 12)

**REQUIREMENTS:**
- 18.1.1 — All tests listed in earlier phases must be present.
- 18.1.2 — Tests must not make real network calls unless tagged `@pytest.mark.integration`.
- 18.1.3 — Mock all Ollama calls in unit tests.
- 18.1.4 — Each test file must have a docstring describing what it covers.

**SUCCESS CRITERIA:**
- `pytest tests/ --cov=src -x` passes with 0 failures and ≥ 70% coverage.

---

### TASK 18.2 — Security audit: credentials

**DESCRIPTION:** Verify no credentials appear in log files or source code.

**INPUT:** All log files and source files.

**OUTPUT:** Zero credential matches found.

**FILES:**
- CREATE: `scripts/credential_audit.py`

**REQUIREMENTS:**
- 18.2.1 — Scan `logs/` for patterns: Google API key format, OAuth token format, generic token/key patterns.
- 18.2.2 — Scan `src/` for hardcoded values matching the same patterns.
- 18.2.3 — Print each match with file, line number, and masked value.
- 18.2.4 — Exit with code 1 if any match found.

**SUCCESS CRITERIA:**
- `python scripts/credential_audit.py` exits with code 0 after a complete test run.

---

### TASK 18.3 — Security audit: tool safety

**DESCRIPTION:** Verify all safety requirements are enforced.

**INPUT:** Code review of `src/skills/` and `src/core/tools/`.

**OUTPUT:** Security checklist fully verified.

**FILES:**
- No new files — audit and fix existing files.

**REQUIREMENTS:**
- 18.3.1 — `delete_file` uses `send2trash` — verify no `os.remove` on user files.
- 18.3.2 — `run_shell` checks blocklist before any subprocess call.
- 18.3.3 — `send_email` always has `requires_confirmation=True`.
- 18.3.4 — Session files encrypted when `SESSION_ENCRYPTION_KEY` is set.
- 18.3.5 — All tool args pass through the schema validator before execution.
- 18.3.6 — File paths checked against `ALLOWED_ROOTS` before write/delete.
- 18.3.7 — No stack traces logged at INFO level (only at DEBUG).

**SUCCESS CRITERIA:**
- All 7 items manually verified and checked off.

---

### TASK 18.4 — Performance benchmarks

**DESCRIPTION:** Measure and verify system performance against defined targets.

**INPUT:** `python scripts/benchmark.py`.

**OUTPUT:** All metrics within target values.

**FILES:**
- CREATE: `scripts/benchmark.py`

**REQUIREMENTS:**
- 18.4.1 — Measure: cold start time (process start to "Jarvis ready" logged).
- 18.4.2 — Measure: simple chat response time with `gemma3:4b`.
- 18.4.3 — Measure: file read tool execution time.
- 18.4.4 — Measure: peak VRAM during normal chat.
- 18.4.5 — Write results to `data/benchmark_results.json`.

**Targets:**

| Metric | Target |
|--------|--------|
| Cold start | < 10 seconds |
| Simple chat (gemma3:4b) | < 5 seconds |
| File read tool | < 1 second |
| VRAM peak during chat | < 5.5 GB |

**SUCCESS CRITERIA:**
- `python scripts/benchmark.py` exits with code 0 when all targets are met.
- Results written to `data/benchmark_results.json`.

---

### TASK 18.5 — Windows 11 clean install verification

**DESCRIPTION:** Verify the full install and feature set on a clean Windows 11 system.

**INPUT:** Clean Windows 11 machine (physical or VM).

**OUTPUT:** All features work after running install script.

**FILES:**
- MODIFY: `scripts/install.ps1` (finalize)

**REQUIREMENTS:**
- 18.5.1 — Run `install.ps1` on a machine without any prior Jarvis installation.
- 18.5.2 — Verify: CLI chat in Arabic, file operations, app launch, notifications, clipboard.
- 18.5.3 — Verify: Web UI at localhost:8080.
- 18.5.4 — Verify: Voice pipeline activates.

**SUCCESS CRITERIA:**
- All steps complete without manual intervention beyond entering API keys.

---

### TASK 18.6 — Linux verification

**DESCRIPTION:** Verify core features on Ubuntu 22.04 or later.

**INPUT:** Ubuntu 22.04 machine.

**OUTPUT:** Platform-independent features work. Windows-only features report as unavailable.

**FILES:**
- MODIFY: `scripts/install.sh` (finalize)

**REQUIREMENTS:**
- 18.6.1 — Core chat, tool execution, file ops, browser, APIs all work.
- 18.6.2 — Windows-only tools (winotify, pycaw) return `is_available()=False` without error.

**SUCCESS CRITERIA:**
- Platform check: `winotify`-based notification tool is not in `registry.all_available()` on Linux.
- Core functionality works without any Windows-specific tool.

---

### TASK 18.7 — CI setup

**DESCRIPTION:** Configure automated CI to run tests on every push.

**INPUT:** Git push to main branch.

**OUTPUT:** Lint, type check, and tests run automatically.

**FILES:**
- CREATE: `.github/workflows/ci.yml`
- CREATE: `.pre-commit-config.yaml`

**REQUIREMENTS:**
- 18.7.1 — CI workflow: checkout, Python setup, install requirements, run `ruff check src/`, run `pytest tests/ --cov=src -x`.
- 18.7.2 — CI runs on push and pull_request events.
- 18.7.3 — Pre-commit hooks: ruff format check, import sort.
- 18.7.4 — CI must not require real Ollama or Google API access.

**SUCCESS CRITERIA:**
- Push triggers CI. All checks pass on a clean run.
- Failed test blocks merge (CI returns exit code 1).

---

## 📌 Implementation Reference

### Layer Responsibilities

| Layer | Only Does | Never Does |
|-------|-----------|-----------|
| `src/interfaces/` | Receive input, display output | Classify, route, store |
| `src/core/context/` | Build InputPacket for current turn | Store across turns |
| `src/core/decision/` | Classify intent, select model, assign risk | Generate content |
| `src/core/runtime/` | Drive the execution loop | Implement intelligence |
| `src/core/agents/` | Multi-step reasoning and planning | Route requests |
| `src/core/tools/` | Registry, safety, validation, execution bridge | Implement tool logic |
| `src/skills/` | One specific action | Route, decide, store |
| `src/models/` | Wrap AI model I/O | Decide, route, store |
| `src/core/memory/` | Persist and retrieve data | Route or classify |
| `src/core/identity/` | Build system prompts | Make decisions |

### Model Selection

| Signal | Model |
|--------|-------|
| Image in attachments | `llava:7b` |
| intent == "code" | `qwen2.5-coder:7b` |
| complexity == "low" AND mode == "fast" | `gemma3:4b` |
| All other cases | `qwen3:8b` |

### Execution Mode Policy

| Risk | SAFE | BALANCED | UNRESTRICTED |
|------|------|----------|-------------|
| low | confirm | auto | auto |
| medium | confirm | confirm | auto |
| high | confirm | blocked* | auto |

*Unblocked by `"confirm: {tool_name}"` override phrase.

### Data Flow Summary

```
Interface input
  → assemble_context() → InputPacket
  → decide() → DecisionOutput
  → execute_turn() → LLMOutput
  → [if tool_call] → execute_tool() → ToolResult → re-observe
  → [if answer] → evaluate() → EvalResult
  → [if approved] → FinalResponse → Interface output
```
