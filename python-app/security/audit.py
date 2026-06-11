from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Optional, Any

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from jarvis.cross_platform_paths import paths

logger = logging.getLogger("jarvis.security.audit")


class AuditEventType(str, Enum):
    COMMAND = "command"
    PERMISSION_REQUEST = "permission_request"
    PERMISSION_RESULT = "permission_result"
    TOOL_EXECUTION = "tool_execution"
    SYSTEM_EVENT = "system_event"
    SECURITY_ALERT = "security_alert"
    EMERGENCY_STOP = "emergency_stop"
    ERROR = "error"


class SecuritySeverity(str, Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class AuditEntry:
    timestamp: str = ""
    event_type: str = ""
    action: str = ""
    target: str = ""
    source: str = ""
    user_id: str = ""
    decision: str = ""
    result: str = ""
    duration_ms: int = 0
    details: dict = field(default_factory=dict)
    severity: str = "info"
    signature: str = ""


class AuditLogger:
    def __init__(self) -> None:
        self.log_dir: Path = paths.audit_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self._private_key: Optional[Any] = None
        self._public_key: Optional[Any] = None
        self._init_keys()

    def _init_keys(self) -> None:
        key_path = self.log_dir / "audit_key.pem"
        pub_key_path = self.log_dir / "audit_key_pub.pem"
        try:
            if not key_path.exists():
                private = rsa.generate_private_key(
                    public_exponent=65537,
                    key_size=2048,
                    backend=default_backend(),
                )
                pem = private.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption(),
                )
                key_path.write_bytes(pem)
                pub_pem = private.public_key().public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo,
                )
                pub_key_path.write_bytes(pub_pem)
                self._private_key = private
                self._public_key = private.public_key()
            else:
                pem = key_path.read_bytes()
                self._private_key = serialization.load_pem_private_key(pem, None, backend=default_backend())
                pub_pem = pub_key_path.read_bytes()
                from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
                self._public_key = serialization.load_pem_public_key(pub_pem, backend=default_backend())
        except Exception as e:
            logger.warning("Could not initialize audit keys: %s", e)

    def _sign(self, data: str) -> str:
        if self._private_key:
            try:
                sig = self._private_key.sign(
                    data.encode(),
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH,
                    ),
                    hashes.SHA256(),
                )
                return sig.hex()
            except Exception:
                pass
        return ""

    def log(self, event_type: AuditEventType, action: str, target: str = "",
            source: str = "local", user_id: str = "default",
            decision: str = "", result: str = "", duration_ms: int = 0,
            details: Optional[dict] = None,
            severity: SecuritySeverity = SecuritySeverity.INFO) -> None:
        entry = AuditEntry(
            timestamp=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
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
        data_str = json.dumps(asdict(entry), sort_keys=True, ensure_ascii=False)
        entry.signature = self._sign(data_str)

        log_file = self.log_dir / f"audit_{datetime.now().strftime('%Y%m%d')}.log"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(entry), ensure_ascii=False) + "\n")

    def log_permission(self, request_id: str, tool_name: str, action: str,
                       decision: str, target: str = "", reason: str = "") -> None:
        self.log(
            event_type=AuditEventType.PERMISSION_RESULT,
            action=f"{tool_name}.{action}",
            target=target,
            decision=decision,
            details={"request_id": request_id, "reason": reason},
            severity=SecuritySeverity.MEDIUM if decision == "denied" else SecuritySeverity.INFO,
        )

    def log_security_alert(self, message: str,
                           severity: SecuritySeverity = SecuritySeverity.HIGH,
                           details: Optional[dict] = None) -> None:
        self.log(
            event_type=AuditEventType.SECURITY_ALERT,
            action="security_alert",
            target=message,
            decision="alert",
            details=details or {},
            severity=severity,
        )

    def log_emergency_stop(self, triggered_by: str) -> None:
        self.log(
            event_type=AuditEventType.EMERGENCY_STOP,
            action="emergency_stop_activated",
            target=triggered_by,
            decision="stop",
            severity=SecuritySeverity.CRITICAL,
            details={"triggered_by": triggered_by},
        )

    def read_recent(self, n: int = 50) -> list[dict]:
        log_file = self.log_dir / f"audit_{datetime.now().strftime('%Y%m%d')}.log"
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


audit_logger = AuditLogger()
