"""
JARVIS 4.0 — Local Device Automation Modules
=============================================
Safe, auditable local device control with explicit user confirmation.

Modules:
    browser.py  — Chrome control via Playwright
    apps.py     — Application open/close
    files.py    — File operations with safety constraints
    screen.py   — Screenshot & screen recording
    shell.py    — Shell execution with deny-by-default policy
    system_info.py — System information

Safety Policy:
    - Deny-by-default for all risky operations
    - Explicit user confirmation required for: file_delete, file_move, shell_exec, screen_record
    - Audit logging of every action
    - No credential access, no network exfiltration
"""
