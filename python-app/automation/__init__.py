"""
JARVIS 4.5 — Local Device Automation Modules
=============================================
Safe, auditable local device control with explicit user confirmation.

Modules:
    browser.py     — Full browser automation (Chrome via Playwright)
    apps.py        — Application control (open, close, restart, focus, list)
    files.py       — File operations with safety constraints
    screen.py      — Screenshot, recording, OCR, UI element detection
    shell.py       — Shell execution with deny-by-default policy
    system_info.py — System information and process management

Safety Policy:
    - Deny-by-default for all risky operations
    - Explicit user confirmation required for: delete, move, shell, record
    - Audit logging of every action
    - No credential access, no network exfiltration
    - Path traversal protection
    - Command injection prevention

Version: 4.5.0
"""

__version__ = "4.5.0"
