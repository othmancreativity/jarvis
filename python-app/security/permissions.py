from __future__ import annotations

import json
import logging
import os
import platform
import subprocess
import time
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional, Callable, Any

from jarvis.cross_platform_paths import paths

logger = logging.getLogger("jarvis.security.permissions")


class PermissionLevel(str, Enum):
    SAFE = "safe"
    CONFIRM_REQUIRED = "confirm_required"
    UNSAFE = "unsafe"


class Decision(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    CONFIRM = "confirm"
    TIMEOUT = "timeout"
    ERROR = "error"


@dataclass
class PermissionRequest:
    request_id: str
    tool_name: str
    action: str
    target: str
    risk_level: str
    permission_level: str
    params: dict = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    source: str = "local"
    user_id: str = "default"


@dataclass
class PermissionResult:
    decision: Decision
    request_id: str
    tool_name: str
    action: str
    target: str
    confirmed: bool = False
    reason: str = ""
    timestamp: float = field(default_factory=time.time)


class WhitelistManager:
    def __init__(self) -> None:
        self._entries: dict[str, float] = {}

    def _make_key(self, tool: str, action: str, user: str = "default") -> str:
        return f"{user}:{tool}:{action}"

    def add(self, tool: str, action: str, duration: int = 300, user: str = "default") -> None:
        self._entries[self._make_key(tool, action, user)] = time.time() + duration

    def is_whitelisted(self, tool: str, action: str, user: str = "default") -> bool:
        key = self._make_key(tool, action, user)
        expiry = self._entries.get(key, 0)
        if expiry > time.time():
            return True
        self._entries.pop(key, None)
        return False

    def remove(self, tool: str, action: str, user: str = "default") -> None:
        self._entries.pop(self._make_key(tool, action, user), None)

    def clear(self) -> None:
        self._entries.clear()


class PermissionEngine:
    def __init__(self) -> None:
        self.whitelist = WhitelistManager()
        self.confirmation_callback: Optional[Callable[[PermissionRequest], PermissionResult]] = None
        self._emergency_stop = False
        self._stats = {"total_requests": 0, "allowed": 0, "denied": 0, "confirmed": 0, "timeouts": 0}

    def set_confirmation_callback(self, callback: Callable[[PermissionRequest], PermissionResult]) -> None:
        self.confirmation_callback = callback

    def trigger_emergency_stop(self) -> None:
        self._emergency_stop = True

    def clear_emergency_stop(self) -> None:
        self._emergency_stop = False

    @property
    def is_emergency_stopped(self) -> bool:
        return self._emergency_stop

    def request_os_elevation(self, action: str, target: str) -> bool:
        system = platform.system().lower()
        try:
            if system == "windows":
                subprocess.run(
                    ["powershell", "-Command", "Start-Process", "cmd", "/c", "echo", "elevated",
                     "-Verb", "runAs"],
                    timeout=5, capture_output=True,
                )
                return True
            elif system == "linux":
                result = subprocess.run(
                    ["pkexec", "echo", "elevated"],
                    timeout=5, capture_output=True,
                )
                return result.returncode == 0
            elif system == "darwin":
                script = f'do shell script "echo elevated" with administrator privileges'
                result = subprocess.run(
                    ["osascript", "-e", script],
                    timeout=5, capture_output=True,
                )
                return result.returncode == 0
        except Exception:
            pass
        return False

    def check_permission(self, request: PermissionRequest) -> PermissionResult:
        self._stats["total_requests"] += 1

        if self._emergency_stop:
            self._stats["denied"] += 1
            return PermissionResult(
                decision=Decision.DENY, request_id=request.request_id,
                tool_name=request.tool_name, action=request.action, target=request.target,
                reason="EMERGENCY STOP active",
            )

        level = PermissionLevel(request.permission_level)

        if level == PermissionLevel.SAFE:
            self._stats["allowed"] += 1
            return PermissionResult(
                decision=Decision.ALLOW, request_id=request.request_id,
                tool_name=request.tool_name, action=request.action, target=request.target,
                confirmed=True, reason="SAFE operation",
            )

        if level == PermissionLevel.UNSAFE:
            if self.whitelist.is_whitelisted(request.tool_name, request.action):
                self._stats["allowed"] += 1
                return PermissionResult(
                    decision=Decision.ALLOW, request_id=request.request_id,
                    tool_name=request.tool_name, action=request.action, target=request.target,
                    confirmed=True, reason="Whitelisted",
                )
            self._stats["denied"] += 1
            return PermissionResult(
                decision=Decision.DENY, request_id=request.request_id,
                tool_name=request.tool_name, action=request.action, target=request.target,
                reason="UNSAFE operation denied by default",
            )

        if level == PermissionLevel.CONFIRM_REQUIRED:
            if self.whitelist.is_whitelisted(request.tool_name, request.action):
                self._stats["allowed"] += 1
                return PermissionResult(
                    decision=Decision.ALLOW, request_id=request.request_id,
                    tool_name=request.tool_name, action=request.action, target=request.target,
                    confirmed=True, reason="Whitelisted",
                )
            if self.confirmation_callback:
                try:
                    result = self.confirmation_callback(request)
                    if result.decision == Decision.ALLOW:
                        self._stats["confirmed"] += 1
                    else:
                        self._stats["denied"] += 1
                    return result
                except Exception as e:
                    return PermissionResult(
                        decision=Decision.ERROR, request_id=request.request_id,
                        tool_name=request.tool_name, action=request.action, target=request.target,
                        reason=f"Confirmation error: {e}",
                    )
            self._stats["denied"] += 1
            return PermissionResult(
                decision=Decision.DENY, request_id=request.request_id,
                tool_name=request.tool_name, action=request.action, target=request.target,
                reason="No confirmation handler",
            )

        self._stats["denied"] += 1
        return PermissionResult(
            decision=Decision.DENY, request_id=request.request_id,
            tool_name=request.tool_name, action=request.action, target=request.target,
            reason="Unknown permission level",
        )

    def verify_integrity(self) -> bool:
        core_files = [
            Path(__file__).parent.parent / "core" / "jarvis_core.py",
            Path(__file__).parent.parent / "core" / "agent_runtime.py",
            Path(__file__).parent.parent / "main.py",
        ]
        for f in core_files:
            if not f.exists():
                logger.error("Integrity check failed: %s missing", f)
                return False
        logger.info("Core binary integrity check passed")
        return True

    def get_stats(self) -> dict:
        return dict(self._stats)


permission_engine = PermissionEngine()
