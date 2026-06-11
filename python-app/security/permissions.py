"""
JARVIS 4.5 — Permission Engine
===============================
Capability-based access control with deny-by-default policy.
Supports: none, notify, confirm, whitelist, deny permission levels.
"""

from __future__ import annotations

import json
import time
import hashlib
import threading
from enum import Enum
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Callable, Any


class PermissionLevel(str, Enum):
    """Permission requirement levels."""
    NONE = "none"
    NOTIFY = "notify"
    CONFIRM = "confirm"
    WHITELIST = "whitelist"
    DENY = "deny"


class Decision(str, Enum):
    """Permission decision outcomes."""
    ALLOW = "allow"
    DENY = "deny"
    CONFIRM = "confirm"
    TIMEOUT = "timeout"
    ERROR = "error"


@dataclass
class PermissionRequest:
    """A permission request for an operation."""
    request_id: str
    tool_name: str
    action: str
    target: str
    risk_level: str
    permission_level: str
    params: dict = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    source: str = "unknown"  # telegram, website, local
    user_id: str = "default"


@dataclass
class PermissionResult:
    """Result of a permission check."""
    decision: Decision
    request_id: str
    tool_name: str
    action: str
    target: str
    confirmed: bool = False
    remember_duration: int = 0  # seconds to remember choice
    reason: str = ""
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> dict:
        return {
            "decision": self.decision.value,
            "request_id": self.request_id,
            "tool_name": self.tool_name,
            "action": self.action,
            "target": self.target,
            "confirmed": self.confirmed,
            "reason": self.reason,
            "timestamp": datetime.fromtimestamp(self.timestamp).isoformat(),
        }


class WhitelistManager:
    """Manages temporarily whitelisted operations."""

    def __init__(self):
        self._entries: dict[str, float] = {}  # key -> expiry_timestamp
        self._lock = threading.RLock()

    def _make_key(self, tool_name: str, action: str, user_id: str = "default") -> str:
        """Create a whitelist key."""
        raw = f"{user_id}:{tool_name}:{action}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def add(self, tool_name: str, action: str, duration_seconds: int = 300, user_id: str = "default") -> None:
        """Add an entry to the whitelist for a duration."""
        key = self._make_key(tool_name, action, user_id)
        with self._lock:
            self._entries[key] = time.time() + duration_seconds

    def is_whitelisted(self, tool_name: str, action: str, user_id: str = "default") -> bool:
        """Check if an operation is currently whitelisted."""
        key = self._make_key(tool_name, action, user_id)
        with self._lock:
            expiry = self._entries.get(key, 0)
            if expiry > time.time():
                return True
            # Clean up expired entry
            if key in self._entries:
                del self._entries[key]
            return False

    def remove(self, tool_name: str, action: str, user_id: str = "default") -> None:
        """Remove a whitelist entry."""
        key = self._make_key(tool_name, action, user_id)
        with self._lock:
            self._entries.pop(key, None)

    def clear(self) -> None:
        """Clear all whitelist entries."""
        with self._lock:
            self._entries.clear()

    def cleanup_expired(self) -> int:
        """Remove expired entries. Returns count removed."""
        now = time.time()
        with self._lock:
            expired = [k for k, v in self._entries.items() if v <= now]
            for k in expired:
                del self._entries[k]
            return len(expired)


class PermissionEngine:
    """
    Central permission engine for JARVIS.
    Deny-by-default with configurable escalation.
    """

    def __init__(self):
        self.whitelist = WhitelistManager()
        self.confirmation_callback: Optional[Callable[[PermissionRequest], PermissionResult]] = None
        self._emergency_stop = False
        self._auto_stop_threshold = 5  # Auto emergency stop after N threats
        self._lock = threading.RLock()
        self._stats = {
            "total_requests": 0,
            "allowed": 0,
            "denied": 0,
            "confirmed": 0,
            "timeouts": 0,
        }

    def set_confirmation_callback(self, callback: Callable[[PermissionRequest], PermissionResult]) -> None:
        """Set the UI callback for user confirmation."""
        self.confirmation_callback = callback

    def trigger_emergency_stop(self) -> None:
        """Activate emergency stop — deny all operations."""
        with self._lock:
            self._emergency_stop = True

    def clear_emergency_stop(self) -> None:
        """Clear emergency stop."""
        with self._lock:
            self._emergency_stop = False

    @property
    def is_emergency_stopped(self) -> bool:
        """Check if emergency stop is active."""
        with self._lock:
            return self._emergency_stop

    def check_permission(self, request: PermissionRequest) -> PermissionResult:
        """
        Check permission for an operation.
        Returns a PermissionResult with the decision.
        """
        with self._lock:
            self._stats["total_requests"] += 1

        # Emergency stop overrides everything
        if self._emergency_stop:
            self._stats["denied"] += 1
            return PermissionResult(
                decision=Decision.DENY,
                request_id=request.request_id,
                tool_name=request.tool_name,
                action=request.action,
                target=request.target,
                reason="EMERGENCY_STOP active — all operations denied",
            )

        permission_level = PermissionLevel(request.permission_level)

        # DENY: Always reject
        if permission_level == PermissionLevel.DENY:
            self._stats["denied"] += 1
            return PermissionResult(
                decision=Decision.DENY,
                request_id=request.request_id,
                tool_name=request.tool_name,
                action=request.action,
                target=request.target,
                reason="Operation is permanently denied by policy",
            )

        # NONE: Always allow
        if permission_level == PermissionLevel.NONE:
            self._stats["allowed"] += 1
            return PermissionResult(
                decision=Decision.ALLOW,
                request_id=request.request_id,
                tool_name=request.tool_name,
                action=request.action,
                target=request.target,
                confirmed=True,
                reason="No permission required",
            )

        # NOTIFY: Log and allow
        if permission_level == PermissionLevel.NOTIFY:
            self._stats["allowed"] += 1
            return PermissionResult(
                decision=Decision.ALLOW,
                request_id=request.request_id,
                tool_name=request.tool_name,
                action=request.action,
                target=request.target,
                confirmed=True,
                reason="Auto-allowed with notification",
            )

        # WHITELIST: Check whitelist
        if permission_level == PermissionLevel.WHITELIST:
            if self.whitelist.is_whitelisted(request.tool_name, request.action, request.user_id):
                self._stats["allowed"] += 1
                return PermissionResult(
                    decision=Decision.ALLOW,
                    request_id=request.request_id,
                    tool_name=request.tool_name,
                    action=request.action,
                    target=request.target,
                    confirmed=True,
                    reason="Whitelisted",
                )
            # Fall through to confirmation if not whitelisted

        # CONFIRM (or WHITELIST not on list): Request user confirmation
        if self.confirmation_callback:
            try:
                result = self.confirmation_callback(request)
                if result.decision == Decision.ALLOW:
                    self._stats["confirmed"] += 1
                    if result.remember_duration > 0:
                        self.whitelist.add(
                            request.tool_name, request.action,
                            result.remember_duration, request.user_id
                        )
                elif result.decision == Decision.DENY:
                    self._stats["denied"] += 1
                elif result.decision == Decision.TIMEOUT:
                    self._stats["timeouts"] += 1
                return result
            except Exception as e:
                return PermissionResult(
                    decision=Decision.ERROR,
                    request_id=request.request_id,
                    tool_name=request.tool_name,
                    action=request.action,
                    target=request.target,
                    reason=f"Confirmation callback error: {e}",
                )
        else:
            # No callback configured — deny by default
            self._stats["denied"] += 1
            return PermissionResult(
                decision=Decision.DENY,
                request_id=request.request_id,
                tool_name=request.tool_name,
                action=request.action,
                target=request.target,
                reason="No confirmation handler configured — deny by default",
            )

    def get_stats(self) -> dict:
        """Get permission engine statistics."""
        with self._lock:
            return dict(self._stats)

    def reset_stats(self) -> None:
        """Reset statistics."""
        with self._lock:
            self._stats = {"total_requests": 0, "allowed": 0, "denied": 0, "confirmed": 0, "timeouts": 0}


# Singleton
permission_engine = PermissionEngine()
