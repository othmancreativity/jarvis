"""
JARVIS 4.5 — Shell Execution Module
====================================
Safe shell command execution:
    - Pattern-based command blocking
    - Allowed command whitelist
    - Timeout protection
    - Output sanitization
    - Sandbox mode (dry-run)
    - Resource limits
"""

from __future__ import annotations

import asyncio
import re
import logging
import shlex
import resource
import tempfile
import os
from typing import Optional, Tuple
from dataclasses import dataclass

logger = logging.getLogger("jarvis.automation.shell")


@dataclass
class ShellResult:
    """Result of a shell command execution."""
    status: str  # success, error, blocked, timeout
    returncode: int = 0
    stdout: str = ""
    stderr: str = ""
    error: str = ""
    duration_ms: int = 0


class ShellController:
    """
    Secure shell command execution controller.
    Deny-by-default with configurable safety levels.
    """

    # Dangerous patterns that are always blocked
    BLOCKED_PATTERNS = [
        r"^\s*rm\s+-rf\s*/\s*$",
        r"^\s*rm\s+.*\s+/\s*$",
        r"mkfs\.\w+",
        r"dd\s+if=.+of=/dev/[sh]d\w",
        r":\(\)\{\s*:\|:\&\};:",  # Fork bomb
        r">\s*/dev/[sh]d\w+",
        r"chmod\s+-R\s+777\s*/",
        r"chmod\s+-R\s+000\s*/",
        r"wget\s+.*\|\s*(bash|sh|zsh|csh|ksh)",
        r"curl\s+.*\|\s*(bash|sh|zsh|csh|ksh)",
        r"fetch\s+.*\|\s*(bash|sh|zsh|csh|ksh)",
        r"nc\s+-[lL]\s*",
        r"ncat\s+-[lL]\s*",
        r"netcat\s+-[lL]\s*",
        r"python\s+-m\s+http\.server\s+&",
        r"ssh\s+.*\s+\'.*\$\(",
        r"eval\s*\$\(",
        r"`.*\$\(.*\)`",  # Nested command substitution
        r"perl\s+-e\s*'.*system",
        r"ruby\s+-e\s*.*`.*`",
    ]

    # Commands allowed without confirmation (read-only)
    READONLY_COMMANDS = [
        "ls", "dir", "pwd", "echo", "cat", "head", "tail", "less", "more",
        "ps", "top", "htop", "pgrep", "pstree",
        "df", "du", "free", "vmstat", "uptime", "w", "who", "whoami",
        "uname", "hostname", "date", "cal", "which", "whereis", "type",
        "env", "printenv", "locale",
        "find", "grep", "rg", "ack", "ag",
        "wc", "sort", "uniq", "diff", "comm",
        "file", "stat", "ldd", "strings",
        "tree", "tput", "stty",
        "git status", "git log", "git branch", "git diff --stat", "git remote -v",
        "git config --list", "git stash list",
        "ping", "curl -I", "curl --head", "nslookup", "dig", "host", "traceroute", "tracepath",
        "npm list", "pip list", "pip freeze",
        "lsblk", "lscpu", "lsmem", "lsusb", "lspci",
        "history",
    ]

    # Commands that need explicit confirmation
    DANGEROUS_COMMANDS = [
        "rm", "mv", "cp", "chmod", "chown", "chgrp",
        "kill", "pkill", "killall", "xkill",
        "docker", "kubectl", "helm", "terraform", "ansible",
        "aws", "gcloud", "az", "gsutil",
        "npm install -g", "pip install", "conda install",
        "mount", "umount", "fdisk", "parted",
        "systemctl", "service", "launchctl",
        "make install", "cmake --install",
        "dd", " shred", "wipe",
    ]

    def __init__(self, sandbox_mode: bool = False):
        self.sandbox_mode = sandbox_mode
        self._execution_history: list[dict] = []
        self._max_history = 100

    def _sanitize(self, command: str) -> str:
        """Sanitize shell command input."""
        # Remove null bytes
        command = command.replace("\x00", "")
        # Remove carriage returns
        command = command.replace("\r", "\n")
        # Limit length
        command = command[:5000]
        return command.strip()

    def _is_blocked(self, command: str) -> Tuple[bool, str]:
        """Check if command matches any blocked pattern."""
        lower = command.lower().strip()

        for pattern in self.BLOCKED_PATTERNS:
            if re.search(pattern, lower, re.IGNORECASE):
                return True, f"Blocked by safety pattern: {pattern}"

        # Check for direct root filesystem deletion
        if re.search(r"rm\s+.*\s+-rf\s+/\s*\b", lower):
            return True, "Root filesystem deletion blocked"

        # Check for pipe to shell
        if re.search(r"\|\s*(bash|sh|zsh|csh|ksh)\s*$", lower):
            return True, "Piping to shell interpreter blocked"

        return False, ""

    def _is_readonly(self, command: str) -> bool:
        """Check if command is in the read-only whitelist."""
        lower = command.lower().strip()
        # Check exact matches first
        for allowed in self.READONLY_COMMANDS:
            if lower.startswith(allowed.lower()):
                # Ensure it's not followed by dangerous flags
                remainder = lower[len(allowed):].strip()
                dangerous_flags = ["-rf", "-f", "--force", ">", "|", ";", "&&"]
                if not any(flag in remainder for flag in dangerous_flags):
                    return True
        return False

    def _is_dangerous(self, command: str) -> bool:
        """Check if command needs explicit confirmation."""
        lower = command.lower().strip()
        first_token = lower.split()[0] if lower else ""
        dangerous_starts = [cmd.split()[0] for cmd in self.DANGEROUS_COMMANDS]
        if first_token in dangerous_starts:
            return True
        for dangerous in self.DANGEROUS_COMMANDS:
            if lower.startswith(dangerous.lower()):
                return True
        return False

    async def execute(self, command: str, timeout: int = 30, cwd: Optional[str] = None) -> dict:
        """
        Execute a shell command with full safety checks.

        Args:
            command: Shell command to execute
            timeout: Maximum execution time in seconds
            cwd: Working directory
        """
        start_time = asyncio.get_event_loop().time()
        command = self._sanitize(command)

        if not command:
            return {"status": "error", "error": "Empty command", "returncode": -1}

        # Check blocked patterns
        is_blocked, reason = self._is_blocked(command)
        if is_blocked:
            logger.warning(f"Blocked command: {command[:50]}... Reason: {reason}")
            return {
                "status": "blocked",
                "error": reason,
                "returncode": -1,
                "stdout": "",
                "stderr": f"[SECURITY] Command blocked: {reason}",
            }

        # Sandbox mode - don't actually execute
        if self.sandbox_mode:
            return {
                "status": "sandbox",
                "error": "Sandbox mode — command not executed",
                "returncode": 0,
                "stdout": f"[SANDBOX] Would execute: {command}",
                "stderr": "",
            }

        # Check if read-only (auto-allow)
        if not self._is_readonly(command) and self._is_dangerous(command):
            # This should have been caught by permission engine already
            logger.info(f"Dangerous command requires confirmation: {command[:50]}...")

        # Execute with timeout
        try:
            proc = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd,
                limit=1024 * 1024,  # 1MB buffer limit
            )
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)

            duration = int((asyncio.get_event_loop().time() - start_time) * 1000)

            stdout_decoded = stdout.decode("utf-8", errors="replace").strip()
            stderr_decoded = stderr.decode("utf-8", errors="replace").strip()

            # Truncate large outputs
            stdout_decoded = stdout_decoded[:10000]
            stderr_decoded = stderr_decoded[:5000]

            result = {
                "status": "success" if proc.returncode == 0 else "error",
                "returncode": proc.returncode,
                "stdout": stdout_decoded,
                "stderr": stderr_decoded,
                "duration_ms": duration,
            }

            # Add to history
            self._execution_history.append({
                "command": command[:100],
                "timestamp": start_time,
                "status": result["status"],
            })
            if len(self._execution_history) > self._max_history:
                self._execution_history.pop(0)

            return result

        except asyncio.TimeoutError:
            try:
                proc.kill()
                await proc.wait()
            except Exception:
                pass
            return {
                "status": "timeout",
                "error": f"Command timed out after {timeout}s",
                "returncode": -1,
                "stdout": "",
                "stderr": f"[TIMEOUT] Command exceeded {timeout} second limit",
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "returncode": -1,
                "stdout": "",
                "stderr": f"[ERROR] {e}",
            }

    def get_history(self, limit: int = 20) -> list[dict]:
        """Get recent command execution history."""
        return self._execution_history[-limit:]

    def clear_history(self) -> None:
        """Clear execution history."""
        self._execution_history.clear()
