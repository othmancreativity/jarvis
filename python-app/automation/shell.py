from __future__ import annotations

import asyncio
import logging
import re
from typing import Optional, Tuple

from security.validator import InputValidator

logger = logging.getLogger("jarvis.automation.shell")


class ShellError(Exception):
    def __init__(self, message: str, error_code: int = -1, details: str = "") -> None:
        self.message = message
        self.error_code = error_code
        self.details = details
        super().__init__(message)


class ShellResult:
    def __init__(self, status: str = "success", returncode: int = 0,
                 stdout: str = "", stderr: str = "", error: str = "",
                 duration_ms: int = 0):
        self.status = status
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        self.error = error
        self.duration_ms = duration_ms

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "returncode": self.returncode,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "error": self.error,
            "duration_ms": self.duration_ms,
        }


class ShellController:
    BLOCKED_PATTERNS = [
        r"^\s*rm\s+-rf\s*/\s*$",
        r"mkfs\.\w+",
        r"dd\s+if=.+of=/dev/[sh]d\w",
        r":\(\)\{\s*:\|:\&\};:",
        r">\s*/dev/[sh]d\w+",
        r"chmod\s+-R\s+777\s*/",
        r"wget\s+.*\|\s*(bash|sh|zsh)",
        r"curl\s+.*\|\s*(bash|sh|zsh)",
        r"nc\s+-[lL]\s*",
    ]

    def __init__(self, sandbox_mode: bool = False) -> None:
        self.sandbox_mode = sandbox_mode

    def _sanitize(self, command: str) -> str:
        command = command.replace("\x00", "").replace("\r", "\n")
        return InputValidator.sanitize_string(command.strip(), 5000)

    def _is_blocked(self, command: str) -> Tuple[bool, str]:
        lower = command.lower().strip()
        for pattern in self.BLOCKED_PATTERNS:
            if re.search(pattern, lower, re.IGNORECASE):
                return True, f"Blocked by safety pattern"
        if re.search(r"\|\s*(bash|sh|zsh|csh|ksh)\s*$", lower):
            return True, "Piping to shell blocked"
        if re.search(            r"rm\s+.*-rf\s+/\s*\b", lower):
            return True, "Root filesystem deletion blocked"
        return False, ""

    async def execute(self, command: str, timeout: int = 30,
                      cwd: Optional[str] = None) -> dict:
        start_time = asyncio.get_event_loop().time()
        command = self._sanitize(command)

        if not command:
            return {"status": "error", "error": "Empty command", "returncode": -1}

        if self.sandbox_mode:
            return {"status": "sandbox", "error": "", "returncode": 0,
                    "stdout": f"[SANDBOX] Would execute: {command}", "stderr": ""}

        is_blocked, reason = self._is_blocked(command)
        if is_blocked:
            logger.warning("Blocked command: %s", command[:50])
            return {"status": "blocked", "error": reason, "returncode": -1, "stdout": "", "stderr": f"[BLOCKED] {reason}"}

        try:
            proc = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd,
            )
            try:
                stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
            except asyncio.TimeoutError:
                try:
                    proc.kill()
                    await proc.wait()
                except Exception:
                    pass
                return {"status": "timeout", "error": f"Timed out after {timeout}s",
                        "returncode": -1, "stdout": "", "stderr": ""}

            duration = int((asyncio.get_event_loop().time() - start_time) * 1000)
            stdout_str = stdout.decode("utf-8", errors="replace").strip()[:10000]
            stderr_str = stderr.decode("utf-8", errors="replace").strip()[:5000]

            return {
                "status": "success" if proc.returncode == 0 else "error",
                "returncode": proc.returncode,
                "stdout": stdout_str,
                "stderr": stderr_str,
                "duration_ms": duration,
            }
        except ShellError:
            raise
        except Exception as e:
            return {"status": "error", "error": str(e), "returncode": -1, "stdout": "", "stderr": str(e)}
