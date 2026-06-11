from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Optional, Tuple
from urllib.parse import urlparse


class InputValidator:
    DANGEROUS_PATTERNS = [
        r"[\x00-\x08\x0b\x0c\x0e-\x1f]",
        r"\$\{.*\}",
        r"`.*`",
        r"\|\s*(bash|sh|zsh|python|ruby|perl)",
        r";\s*(rm|mv|cp|cat|echo|wget|curl)",
        r"\b(?:DELETE|DROP|TRUNCATE)\b",
        r"<script",
        r"javascript:",
        r"data:text/html",
    ]

    @classmethod
    def sanitize_string(cls, value: str, max_length: int = 10000) -> str:
        if not isinstance(value, str):
            value = str(value)
        value = value.replace("\x00", "")
        value = "".join(c for c in value if c == "\n" or c == "\t" or ord(c) >= 32)
        return value[:max_length].strip()

    @classmethod
    def check_dangerous_patterns(cls, value: str) -> Tuple[bool, list[str]]:
        matches = []
        for pattern in cls.DANGEROUS_PATTERNS:
            if re.search(pattern, value, re.IGNORECASE):
                matches.append(pattern)
        return len(matches) == 0, matches

    @classmethod
    def validate_path(cls, path: str) -> Tuple[bool, str, Optional[str]]:
        if not path:
            return False, "", "Empty path"
        expanded = os.path.expanduser(path)
        normalized = os.path.normpath(expanded)
        try:
            resolved = Path(normalized).resolve()
            home = Path.home().resolve()
            if not str(resolved).startswith(str(home)):
                return False, normalized, "Path traversal detected"
        except (OSError, ValueError):
            return False, normalized, "Invalid path"
        return True, normalized, None

    @classmethod
    def validate_shell_command(cls, command: str) -> Tuple[bool, Optional[str]]:
        if not command:
            return False, "Empty command"
        lower = command.strip().lower()
        blocked_commands = [
            r"^rm\s+-rf\s*/",
            r"mkfs",
            r"dd\s+if=.*of=/dev/",
        ]
        for pattern in blocked_commands:
            if re.search(pattern, lower):
                return False, f"Blocked dangerous command pattern"
        if re.search(r"\|\s*(bash|sh|zsh|csh|ksh)\s*$", lower):
            return False, "Piping to shell interpreter is blocked"
        is_safe, matches = cls.check_dangerous_patterns(command)
        if not is_safe:
            return False, f"Dangerous patterns detected"
        return True, None

    @classmethod
    def truncate_output(cls, text: str, max_length: int = 10000) -> str:
        if len(text) <= max_length:
            return text
        return text[:max_length] + f"\n... [truncated from {len(text)} chars]"
