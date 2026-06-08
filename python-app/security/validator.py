"""
JARVIS 4.5 — Input Validator
=============================
Comprehensive input validation and sanitization.
Protects against: path traversal, injection attacks, oversized inputs,
malicious patterns, and malformed data.
"""

from __future__ import annotations

import re
import os
from pathlib import Path
from typing import Optional, Tuple
from urllib.parse import urlparse


class InputValidator:
    """Central input validation and sanitization."""

    # Patterns that indicate potential attacks
    DANGEROUS_PATTERNS = [
        r"[\x00-\x08\x0b\x0c\x0e-\x1f]",  # Control characters
        r"\$\{.*\}",                        # Shell interpolation
        r"`.*`",                            # Command substitution
        r"\|\s*(bash|sh|zsh|python|ruby|perl)",  # Pipe to interpreter
        r";\s*(rm|mv|cp|cat|echo|wget|curl)",    # Command chaining
        r"\b(?:DELETE|DROP|TRUNCATE)\b",    # SQL keywords
        r"<script",                         # XSS attempt
        r"javascript:",                     # JS protocol
        r"data:text/html",                  # Data URI
    ]

    # Protected path patterns
    PROTECTED_PATHS = [
        "/etc", "/sys", "/proc", "/dev",
        ".ssh", ".gnupg", ".aws", ".kube",
        ".config", ".env", ".docker",
        "password", "token", "secret", "credential",
        "id_rsa", "id_dsa", "id_ecdsa", "id_ed25519",
        ".pem", ".key", ".p12", ".pfx",
        "/boot", "/bin", "/sbin", "/lib", "/lib64",
    ]

    @classmethod
    def sanitize_string(cls, value: str, max_length: int = 10000) -> str:
        """Sanitize a string input."""
        if not isinstance(value, str):
            value = str(value)
        # Remove null bytes
        value = value.replace("\x00", "")
        # Remove control characters except newlines and tabs
        value = "".join(c for c in value if c == "\n" or c == "\t" or ord(c) >= 32)
        # Limit length
        value = value[:max_length]
        return value.strip()

    @classmethod
    def check_dangerous_patterns(cls, value: str) -> Tuple[bool, list[str]]:
        """Check for dangerous patterns. Returns (is_safe, matches)."""
        matches = []
        for pattern in cls.DANGEROUS_PATTERNS:
            if re.search(pattern, value, re.IGNORECASE):
                matches.append(pattern)
        return len(matches) == 0, matches

    @classmethod
    def validate_path(cls, path: str, allow_create: bool = False) -> Tuple[bool, str, Optional[str]]:
        """
        Validate a file path for traversal attacks.
        Returns (is_valid, sanitized_path, error_message).
        """
        if not path:
            return False, "", "Empty path"

        # Expand user home
        expanded = os.path.expanduser(path)

        # Check for path traversal
        normalized = os.path.normpath(expanded)
        if ".." in normalized.split(os.sep):
            # Only allow .. if the final resolved path is within home
            try:
                resolved = Path(normalized).resolve()
                home = Path.home().resolve()
                if not str(resolved).startswith(str(home)):
                    return False, normalized, "Path traversal detected — path escapes home directory"
            except (OSError, ValueError):
                return False, normalized, "Invalid path"

        # Check against protected paths
        path_lower = normalized.lower()
        for protected in cls.PROTECTED_PATHS:
            if protected.lower() in path_lower:
                return False, normalized, f"Access to protected path blocked: {protected}"

        # Check for system paths
        try:
            abs_path = os.path.abspath(normalized)
            if any(abs_path.startswith(p) for p in ["/sys", "/proc", "/dev"]):
                return False, normalized, "System paths are protected"
        except (OSError, ValueError):
            pass

        return True, normalized, None

    @classmethod
    def validate_url(cls, url: str, allowed_schemes: Optional[list[str]] = None) -> Tuple[bool, Optional[str]]:
        """Validate a URL. Returns (is_valid, error_message)."""
        if not url:
            return False, "Empty URL"

        allowed = allowed_schemes or ["http", "https"]

        try:
            parsed = urlparse(url)
            if not parsed.scheme:
                return False, "URL missing scheme"
            if parsed.scheme not in allowed:
                return False, f"URL scheme not allowed: {parsed.scheme}"
            if not parsed.netloc:
                return False, "URL missing host"
            # Block localhost/private IPs in production
            hostname = parsed.hostname or ""
            if hostname in ("localhost", "127.0.0.1", "::1", "0.0.0.0"):
                return False, "Localhost URLs are blocked"
            return True, None
        except ValueError as e:
            return False, f"Invalid URL: {e}"

    @classmethod
    def validate_shell_command(cls, command: str) -> Tuple[bool, Optional[str]]:
        """
        Validate a shell command for dangerous patterns.
        Returns (is_valid, error_message).
        """
        if not command:
            return False, "Empty command"

        command = command.strip()

        # Block dangerous commands
        blocked_commands = [
            r"^rm\s+-rf\s*/",
            r"^rm\s+.*\s+/\s*$",
            r"mkfs",
            r"dd\s+if=.*of=/dev/",
            r":\(\)\{\s*:\|:\&\};:",  # Fork bomb
            r">\s*/dev/[sh]da",
            r"chmod\s+-R\s+777\s*/",
        ]

        lower = command.lower()
        for pattern in blocked_commands:
            if re.search(pattern, lower):
                return False, f"Blocked dangerous command pattern: {pattern}"

        # Check for pipe to shell
        if re.search(r"\|\s*(bash|sh|zsh|csh|ksh)\s*$", lower):
            return False, "Piping to shell interpreter is blocked"

        # Check for dangerous patterns
        is_safe, matches = cls.check_dangerous_patterns(command)
        if not is_safe:
            return False, f"Dangerous patterns detected: {matches[:3]}"

        return True, None

    @classmethod
    def truncate_output(cls, text: str, max_length: int = 10000) -> str:
        """Truncate output to safe length with indicator."""
        if len(text) <= max_length:
            return text
        return text[:max_length] + f"\n\n... [truncated from {len(text)} chars]"

    @classmethod
    def validate_json_size(cls, data: dict, max_keys: int = 100, max_value_length: int = 100000) -> Tuple[bool, Optional[str]]:
        """Validate JSON object size."""
        if len(data) > max_keys:
            return False, f"JSON object exceeds max keys: {len(data)} > {max_keys}"

        for key, value in data.items():
            if isinstance(value, str) and len(value) > max_value_length:
                return False, f"Value for key '{key}' exceeds max length: {len(value)} > {max_value_length}"
        return True, None
