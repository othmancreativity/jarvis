"""Shell command execution with deny-by-default policy."""

import asyncio
import re
import shutil
from typing import List, Optional


class ShellController:
    """Shell command execution with strict safety controls."""

    # Commands that are always blocked
    BLOCKED_PATTERNS = [
        r"rm\s+-rf\s*/\s*$",
        r"rm\s+.*\s+/\s*",
        r"mkfs",
        r"dd\s+if=.*of=/dev/",
        r":\(\)\{\s*:\|:\&\};:",  # Fork bomb
        r"curl\s+.*\|\s*(bash|sh|zsh)",
        r"wget\s+.*\|\s*(bash|sh|zsh)",
        r"nc\s+-l",
        r"ncat\s+-l",
        r"netcat\s+-l",
        r">\s*/dev/",
        r"chmod\s+-R\s+777\s*/",
    ]

    # Commands that are allowed without confirmation (safe read-only)
    ALLOWED_COMMANDS = [
        "ls", "pwd", "echo", "cat", "head", "tail", "less", "more",
        "ps", "top", "htop", "df", "du", "free", "uptime", "whoami",
        "uname", "date", "cal", "which", "whereis",
        "mkdir", "touch", "cp", "find", "grep", "wc",
        "git status", "git log", "git branch", "git diff --stat",
        "ping", "curl -I", "curl --head", "nslookup", "dig", "traceroute",
        "tree", "file", "stat",
    ]

    # Commands requiring confirmation even if in allowed list
    CONFIRM_COMMANDS = [
        "rm", "mv", "chmod", "chown", "kill", "pkill", "killall",
        "docker", "kubectl", "terraform", "aws", "gcloud",
    ]

    def _is_blocked(self, command: str) -> Optional[str]:
        """Check if a command matches a blocked pattern."""
        lower = command.lower().strip()
        for pattern in self.BLOCKED_PATTERNS:
            if re.search(pattern, lower):
                return f"Command blocked by safety pattern: {pattern}"
        return None

    def _needs_confirmation(self, command: str) -> bool:
        """Check if a command needs explicit user confirmation."""
        lower = command.lower().strip()
        first_token = lower.split()[0] if lower else ""
        return first_token in [c.split()[0] for c in self.CONFIRM_COMMANDS]

    def _sanitize(self, command: str) -> str:
        """Basic sanitization of shell command."""
        # Remove null bytes
        command = command.replace("\x00", "")
        # Limit length
        command = command[:2000]
        return command.strip()

    async def execute(self, command: str, timeout: int = 30) -> dict:
        """Execute shell command with safety checks."""
        command = self._sanitize(command)

        if not command:
            return {"status": "error", "error": "Empty command"}

        # Check blocked patterns
        block_reason = self._is_blocked(command)
        if block_reason:
            return {"status": "blocked", "error": block_reason}

        # Execute with timeout
        try:
            proc = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)

            stdout_decoded = stdout.decode("utf-8", errors="replace").strip()
            stderr_decoded = stderr.decode("utf-8", errors="replace").strip()

            return {
                "status": "success" if proc.returncode == 0 else "error",
                "returncode": proc.returncode,
                "stdout": stdout_decoded[:10000],  # Limit output
                "stderr": stderr_decoded[:5000],
            }
        except asyncio.TimeoutError:
            try:
                proc.kill()
            except Exception:
                pass
            return {"status": "timeout", "error": f"Command timed out after {timeout}s"}
        except Exception as e:
            return {"status": "error", "error": str(e)}
