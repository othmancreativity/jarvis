from __future__ import annotations

import time
from unittest.mock import MagicMock, patch

import pytest

from security.permissions import PermissionEngine, PermissionRequest, PermissionResult, PermissionLevel, Decision
from security.validator import InputValidator
from security.audit import AuditLogger, AuditEventType, SecuritySeverity


class TestPermissionEngine:
    @pytest.fixture
    def engine(self):
        return PermissionEngine()

    def test_safe_always_allows(self, engine):
        req = PermissionRequest(
            request_id="r1", tool_name="test", action="read",
            target="file.txt", risk_level="none",
            permission_level="safe",
        )
        result = engine.check_permission(req)
        assert result.decision == Decision.ALLOW

    def test_unsafe_denied_by_default(self, engine):
        req = PermissionRequest(
            request_id="r2", tool_name="test", action="delete",
            target="/important", risk_level="high",
            permission_level="unsafe",
        )
        result = engine.check_permission(req)
        assert result.decision == Decision.DENY

    def test_unsafe_allowed_when_whitelisted(self, engine):
        engine.whitelist.add("test", "delete", duration=60)
        req = PermissionRequest(
            request_id="r3", tool_name="test", action="delete",
            target="/tmp", risk_level="high",
            permission_level="unsafe",
        )
        result = engine.check_permission(req)
        assert result.decision == Decision.ALLOW

    def test_emergency_stop_denies_all(self, engine):
        engine.trigger_emergency_stop()
        req = PermissionRequest(
            request_id="r4", tool_name="test", action="read",
            target="x.txt", risk_level="none",
            permission_level="safe",
        )
        result = engine.check_permission(req)
        assert result.decision == Decision.DENY
        assert "EMERGENCY" in result.reason

    def test_confirm_required_with_callback(self, engine):
        engine.set_confirmation_callback(lambda r: PermissionResult(
            decision=Decision.ALLOW, request_id=r.request_id,
            tool_name=r.tool_name, action=r.action, target=r.target,
            confirmed=True, reason="user confirmed",
        ))
        req = PermissionRequest(
            request_id="r5", tool_name="test", action="write",
            target="x.txt", risk_level="medium",
            permission_level="confirm_required",
        )
        result = engine.check_permission(req)
        assert result.decision == Decision.ALLOW

    def test_confirm_required_no_callback(self, engine):
        req = PermissionRequest(
            request_id="r6", tool_name="test", action="write",
            target="x.txt", risk_level="medium",
            permission_level="confirm_required",
        )
        result = engine.check_permission(req)
        assert result.decision == Decision.DENY

    def test_stats(self, engine):
        req = PermissionRequest(
            request_id="r1", tool_name="test", action="read",
            target="x", risk_level="none",
            permission_level="safe",
        )
        engine.check_permission(req)
        stats = engine.get_stats()
        assert stats["total_requests"] >= 1
        assert stats["allowed"] >= 1

    def test_integrity_check(self, engine):
        result = engine.verify_integrity()
        assert result is True


class TestInputValidator:
    def test_sanitize_string(self):
        assert InputValidator.sanitize_string("hello\x00world") == "helloworld"
        assert InputValidator.sanitize_string("  hello  ") == "hello"

    def test_dangerous_patterns(self):
        is_safe, matches = InputValidator.check_dangerous_patterns("normal text")
        assert is_safe
        assert matches == []

        is_safe, matches = InputValidator.check_dangerous_patterns("hello; rm -rf /")
        assert not is_safe
        assert len(matches) >= 1

    def test_shell_command_validation(self):
        valid, err = InputValidator.validate_shell_command("ls -la")
        assert valid

        valid, err = InputValidator.validate_shell_command("rm -rf /")
        assert not valid

    def test_truncate_output(self):
        short = "hello"
        assert InputValidator.truncate_output(short, 100) == short
        long_text = "a" * 1000
        truncated = InputValidator.truncate_output(long_text, 100)
        assert len(truncated) < len(long_text)


class TestAuditLogger:
    @pytest.fixture
    def logger(self, tmp_path):
        audit = AuditLogger()
        audit.log_dir = tmp_path / "audit"
        audit.log_dir.mkdir(parents=True, exist_ok=True)
        return audit

    def test_log_entry(self, logger):
        logger.log(AuditEventType.COMMAND, "test_action", "test_target")
        entries = logger.read_recent(10)
        assert len(entries) >= 1
        assert entries[0]["action"] == "test_action"

    def test_log_permission(self, logger):
        logger.log_permission("req1", "tool1", "write", "allowed")
        entries = logger.read_recent(10)
        assert len(entries) >= 1
        assert entries[0]["event_type"] == "permission_result"

    def test_log_security_alert(self, logger):
        logger.log_security_alert("Threat detected", SecuritySeverity.HIGH)
        entries = logger.read_recent(10)
        assert entries[0]["severity"] == "high"

    def test_log_emergency_stop(self, logger):
        logger.log_emergency_stop("user_test")
        entries = logger.read_recent(10)
        assert entries[0]["event_type"] == "emergency_stop"
