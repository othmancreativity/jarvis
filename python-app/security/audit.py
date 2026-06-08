"""
JARVIS 4.5 — Audit Logger
==========================
Tamper-resistant audit logging for all operations.
Supports: file-based logging, structured JSON, log rotation, and integrity verification.
"""

from __future__ import annotations

import json
import time
import hashlib
import threading
import gzip
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional, Any
from enum import Enum


class AuditEventType(str, Enum):
    """Types of audit events."""
    COMMAND = "command"
    PERMISSION_REQUEST = "permission_request"
    PERMISSION_RESULT = "permission_result"
    TOOL_EXECUTION = "tool_execution"
    SYSTEM_EVENT = "system_event"
    SECURITY_ALERT = "security_alert"
    EMERGENCY_STOP = "emergency_stop"
    BRIDGE_CONNECT = "bridge_connect"
    BRIDGE_DISCONNECT = "bridge_disconnect"
    ERROR = "error"


class SecuritySeverity(str, Enum):
    """Severity levels for security events."""
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class AuditEntry:
    """Single audit log entry."""
    timestamp: str
    event_type: str
    action: str
    target: str
    source: str
    user_id: str
    decision: str
    result: str
    duration_ms: int
    details: dict = field(default_factory=dict)
    severity: str = "info"
    hash: str = ""

    def compute_hash(self, previous_hash: str = "") -> str:
        """Compute chain hash for tamper resistance."""
        data = f"{self.timestamp}:{self.event_type}:{self.action}:{self.target}:{previous_hash}"
        return hashlib.sha256(data.encode()).hexdigest()[:32]


class AuditLogger:
    """
    Production-grade audit logger with chain hashing for integrity.
    Features:
        - Structured JSON logging
        - Log rotation by size and date
        - Tamper-resistant chain hashing
        - Compression of old logs
        - Thread-safe operations
    """

    MAX_LOG_SIZE = 10 * 1024 * 1024  # 10 MB
    MAX_LOG_AGE_DAYS = 30

    def __init__(self, log_dir: Optional[Path] = None):
        self.log_dir = log_dir or (Path.home() / ".jarvis" / "audit")
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.current_log = self.log_dir / f"audit_{datetime.now().strftime('%Y%m%d')}.log"
        self._lock = threading.RLock()
        self._previous_hash = ""
        self._entries_today = 0

    def _get_log_file(self) -> Path:
        """Get the current log file, rotating if needed."""
        today = datetime.now().strftime('%Y%m%d')
        log_file = self.log_dir / f"audit_{today}.log"

        # Rotate if current log is too large
        if log_file.exists() and log_file.stat().st_size > self.MAX_LOG_SIZE:
            timestamp = datetime.now().strftime('%H%M%S')
            rotated = self.log_dir / f"audit_{today}_{timestamp}.log.gz"
            with open(log_file, 'rb') as f_in:
                with gzip.open(rotated, 'wb') as f_out:
                    f_out.write(f_in.read())
            log_file.unlink()
            self._previous_hash = ""

        return log_file

    def _cleanup_old_logs(self) -> int:
        """Remove logs older than MAX_LOG_AGE_DAYS. Returns count removed."""
        cutoff = datetime.now() - timedelta(days=self.MAX_LOG_AGE_DAYS)
        removed = 0
        for log_file in self.log_dir.glob("audit_*.log*"):
            try:
                # Extract date from filename
                date_str = log_file.stem.split('_')[1]
                file_date = datetime.strptime(date_str[:8], '%Y%m%d')
                if file_date < cutoff:
                    log_file.unlink()
                    removed += 1
            except (ValueError, IndexError, OSError):
                continue
        return removed

    def log(self, event_type: AuditEventType, action: str, target: str = "",
            source: str = "local", user_id: str = "default",
            decision: str = "", result: str = "", duration_ms: int = 0,
            details: Optional[dict] = None, severity: SecuritySeverity = SecuritySeverity.INFO) -> None:
        """
        Write an audit entry.
        This is the primary logging method — all operations must call this.
        """
        with self._lock:
            log_file = self._get_log_file()

            entry = AuditEntry(
                timestamp=datetime.utcnow().isoformat() + "Z",
                event_type=event_type.value,
                action=action,
                target=target,
                source=source,
                user_id=user_id,
                decision=decision,
                result=result,
                duration_ms=duration_ms,
                details=details or {},
                severity=severity.value,
            )

            # Compute chain hash
            entry.hash = entry.compute_hash(self._previous_hash)
            self._previous_hash = entry.hash

            # Append to log file
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(asdict(entry), ensure_ascii=False) + "\n")

            self._entries_today += 1

            # Periodic cleanup
            if self._entries_today % 100 == 0:
                self._cleanup_old_logs()

    def log_command(self, command_id: str, action: str, params: dict,
                    confirmed: bool, result: str, duration_ms: int,
                    source: str = "bridge") -> None:
        """Log a device command execution."""
        self.log(
            event_type=AuditEventType.COMMAND,
            action=action,
            target=str(params)[:500],
            source=source,
            decision="confirmed" if confirmed else "denied",
            result=result,
            duration_ms=duration_ms,
            details={"command_id": command_id, "params": params, "confirmed": confirmed},
        )

    def log_permission(self, request_id: str, tool_name: str, action: str,
                       decision: str, target: str = "", reason: str = "") -> None:
        """Log a permission check."""
        self.log(
            event_type=AuditEventType.PERMISSION_RESULT,
            action=f"{tool_name}.{action}",
            target=target,
            decision=decision,
            details={"request_id": request_id, "reason": reason},
            severity=SecuritySeverity.MEDIUM if decision == "denied" else SecuritySeverity.INFO,
        )

    def log_security_alert(self, message: str, severity: SecuritySeverity = SecuritySeverity.HIGH,
                           details: Optional[dict] = None) -> None:
        """Log a security alert."""
        self.log(
            event_type=AuditEventType.SECURITY_ALERT,
            action="security_alert",
            target=message,
            decision="alert",
            details=details or {},
            severity=severity,
        )

    def log_emergency_stop(self, triggered_by: str) -> None:
        """Log emergency stop activation."""
        self.log(
            event_type=AuditEventType.EMERGENCY_STOP,
            action="emergency_stop_activated",
            target=triggered_by,
            decision="stop",
            severity=SecuritySeverity.CRITICAL,
            details={"triggered_by": triggered_by},
        )

    def read_recent(self, n: int = 50) -> list[dict]:
        """Read the most recent n audit entries."""
        with self._lock:
            log_file = self._get_log_file()
            if not log_file.exists():
                return []

            try:
                with open(log_file, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                entries = []
                for line in reversed(lines[-n:]):
                    line = line.strip()
                    if line:
                        try:
                            entries.append(json.loads(line))
                        except json.JSONDecodeError:
                            continue
                return entries
            except OSError:
                return []

    def verify_chain(self, date_str: Optional[str] = None) -> tuple[bool, int, Optional[str]]:
        """
        Verify the integrity of the audit chain.
        Returns (is_valid, entry_count, first_broken_hash).
        """
        log_file = self.log_dir / f"audit_{date_str or datetime.now().strftime('%Y%m%d')}.log"
        if not log_file.exists():
            return True, 0, None

        previous_hash = ""
        count = 0

        try:
            with open(log_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        entry = json.loads(line)
                        expected_hash = hashlib.sha256(
                            f"{entry['timestamp']}:{entry['event_type']}:{entry['action']}:{entry['target']}:{previous_hash}"
                            .encode()
                        ).hexdigest()[:32]

                        if entry.get("hash") != expected_hash:
                            return False, count, entry.get("hash")

                        previous_hash = expected_hash
                        count += 1
                    except (json.JSONDecodeError, KeyError):
                        continue

            return True, count, None
        except OSError:
            return False, 0, None

    def get_stats(self) -> dict:
        """Get audit logger statistics."""
        with self._lock:
            total_entries = 0
            for log_file in self.log_dir.glob("audit_*.log"):
                try:
                    with open(log_file, "r", encoding="utf-8") as f:
                        total_entries += sum(1 for _ in f if _.strip())
                except OSError:
                    continue

            return {
                "entries_today": self._entries_today,
                "total_entries": total_entries,
                "log_dir": str(self.log_dir),
                "current_log": str(self.current_log),
            }


# Singleton
audit_logger = AuditLogger()
